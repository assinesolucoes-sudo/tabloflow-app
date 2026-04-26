"""
Motor de Upload — TabloFlow
Recebe, valida, interpreta e normaliza arquivos enviados pelo usuário.
Produz UploadResult padronizado consumido pelo Motor Base.
"""

import csv
from pathlib import Path
from typing import Any, Optional

import pandas as pd
from pydantic import BaseModel

SUPPORTED_FORMATS = {"xlsx", "xls", "csv"}


# ---------------------------------------------------------------------------
# Contratos de saída
# ---------------------------------------------------------------------------

class ColumnInfo(BaseModel):
    name: str
    inferred_type: str  # "numeric", "text", "date", "boolean", "mixed"
    null_count: int
    unique_count: int
    sample_values: list[str]  # até 3 valores de exemplo como string


class UploadResult(BaseModel):
    file_name: str
    file_format: str            # "xlsx", "xls", "csv"
    sheet_name: Optional[str]   # None se CSV
    available_sheets: list[str] # vazia se CSV
    row_count: int
    column_count: int
    columns: list[ColumnInfo]
    preview: list[dict[str, Any]]  # primeiras 5 linhas
    encoding_detected: str
    separator_detected: Optional[str]  # apenas CSV
    warnings: list[str]
    errors: list[str]
    success: bool
    # Bytes do arquivo original para o Motor Base carregar o DataFrame completo.
    # Preview (acima) continua servindo ao app na etapa de configuração.
    arquivo_bytes: Optional[bytes] = None


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

def _infer_column_type(series: pd.Series) -> str:
    """Infere o tipo semântico de uma coluna: numeric, date, boolean, text ou mixed."""
    non_null = series.dropna()
    if len(non_null) == 0:
        return "text"

    if pd.api.types.is_bool_dtype(series):
        return "boolean"

    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    if pd.api.types.is_datetime64_any_dtype(series):
        return "date"

    str_vals = non_null.astype(str).str.strip()

    bool_keywords = {"true", "false", "yes", "no", "sim", "não", "nao"}
    if set(str_vals.str.lower().unique()).issubset(bool_keywords):
        return "boolean"

    numeric_mask = pd.to_numeric(str_vals, errors="coerce").notna()
    numeric_ratio = numeric_mask.sum() / len(str_vals)

    if numeric_ratio == 1.0:
        return "numeric"

    date_mask = pd.to_datetime(str_vals, errors="coerce").notna()
    date_ratio = date_mask.sum() / len(str_vals)

    if date_ratio >= 0.9:
        return "date"

    if 0.0 < numeric_ratio < 1.0:
        return "mixed"

    return "text"


_NULL_STRINGS_UPLOAD: frozenset[str] = frozenset(
    {"", "n/a", "na", "null", "none", "-", "--", "---"}
)


def _build_column_info(name: str, series: pd.Series) -> ColumnInfo:
    """Constrói ColumnInfo com metadados e amostras de uma coluna."""
    inferred_type = _infer_column_type(series)
    # Conta nulos incluindo null-strings para consistência com motor_base
    def _is_null(v: object) -> bool:
        try:
            if pd.isna(v):  # type: ignore[arg-type]
                return True
        except (TypeError, ValueError):
            pass
        return str(v).strip().lower() in _NULL_STRINGS_UPLOAD

    null_count = int(sum(1 for v in series if _is_null(v)))
    unique_count = int(series.nunique(dropna=True))
    sample_values = [str(v) for v in series.dropna().head(3).tolist()]
    return ColumnInfo(
        name=name,
        inferred_type=inferred_type,
        null_count=null_count,
        unique_count=unique_count,
        sample_values=sample_values,
    )


def _rename_unnamed_columns(df: pd.DataFrame, warnings: list[str]) -> pd.DataFrame:
    """Renomeia colunas sem nome para Coluna_N e registra warnings."""
    new_columns: list[str] = []
    counter = 0
    for col in df.columns:
        col_str = str(col).strip()
        if col_str == "" or col_str.startswith("Unnamed:") or col_str == "nan":
            counter += 1
            new_name = f"Coluna_{counter}"
            warnings.append(f"Coluna sem nome renomeada para '{new_name}'")
            new_columns.append(new_name)
        else:
            new_columns.append(col_str)
    df.columns = new_columns
    return df


def _build_preview(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Retorna as primeiras 5 linhas como lista de dicts com valores serializáveis."""
    records = []
    for _, row in df.head(5).iterrows():
        records.append(
            {col: (None if pd.isna(val) else str(val)) for col, val in row.items()}
        )
    return records


def _detect_encoding(file_path: str) -> str:
    """Detecta encoding do arquivo; tenta chardet, depois UTF-8, fallback Latin-1."""
    try:
        import chardet  # type: ignore
        with open(file_path, "rb") as f:
            raw = f.read(10_000)
        result = chardet.detect(raw)
        return (result.get("encoding") or "utf-8").lower()
    except ImportError:
        pass

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            f.read(4_096)
        return "utf-8"
    except UnicodeDecodeError:
        return "latin-1"


def _detect_separator(file_path: str, encoding: str) -> str:
    """Detecta separador CSV via Sniffer; fallback por tentativa com separadores comuns."""
    try:
        with open(file_path, "r", encoding=encoding, errors="replace") as f:
            sample = f.read(4_096)
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        return dialect.delimiter
    except csv.Error:
        pass

    for sep in (",", ";", "\t"):
        try:
            df = pd.read_csv(file_path, sep=sep, encoding=encoding, nrows=3)
            if len(df.columns) > 1:
                return sep
        except Exception:
            continue
    return ","


def _read_csv(
    file_path: str,
) -> tuple[pd.DataFrame, str, str, list[str], list[str]]:
    """
    Lê um arquivo CSV detectando encoding e separador.

    Returns:
        (DataFrame, encoding, separator, warnings, errors)
    """
    warnings: list[str] = []
    errors: list[str] = []

    encoding = _detect_encoding(file_path)
    separator = _detect_separator(file_path, encoding)

    for enc in [encoding, "latin-1"]:
        try:
            df = pd.read_csv(
                file_path,
                sep=separator,
                encoding=enc,
                skip_blank_lines=True,
                on_bad_lines="warn",
            )
            return df, enc, separator, warnings, errors
        except UnicodeDecodeError:
            if enc == encoding:
                continue  # tenta latin-1
            errors.append(f"Falha de encoding mesmo com fallback Latin-1.")
            return pd.DataFrame(), enc, separator, warnings, errors
        except Exception as exc:
            errors.append(f"Erro ao ler CSV: {exc}")
            return pd.DataFrame(), enc, separator, warnings, errors

    errors.append("Não foi possível ler o arquivo CSV.")
    return pd.DataFrame(), encoding, separator, warnings, errors


def _read_excel(
    file_path: str,
    sheet_name: Optional[str],
) -> tuple[pd.DataFrame, list[str], Optional[str], str, list[str], list[str]]:
    """
    Lê um arquivo Excel, respeitando seleção de aba.

    Returns:
        (DataFrame, available_sheets, sheet_used, encoding, warnings, errors)
    """
    warnings: list[str] = []
    errors: list[str] = []
    encoding = "utf-8"  # Excel gerencia encoding internamente

    try:
        xl = pd.ExcelFile(file_path)
        available_sheets: list[str] = xl.sheet_names
    except Exception as exc:
        errors.append(f"Erro ao abrir arquivo Excel: {exc}")
        return pd.DataFrame(), [], None, encoding, warnings, errors

    if not available_sheets:
        errors.append("Arquivo Excel não contém abas.")
        return pd.DataFrame(), [], None, encoding, warnings, errors

    # Múltiplas abas sem seleção → aguardar escolha do usuário
    if len(available_sheets) > 1 and sheet_name is None:
        return pd.DataFrame(), available_sheets, None, encoding, warnings, errors

    target = sheet_name if sheet_name else available_sheets[0]

    if target not in available_sheets:
        errors.append(
            f"Aba '{target}' não encontrada. Disponíveis: {available_sheets}"
        )
        return pd.DataFrame(), available_sheets, None, encoding, warnings, errors

    try:
        df = pd.read_excel(file_path, sheet_name=target)
    except Exception as exc:
        errors.append(f"Erro ao ler aba '{target}': {exc}")
        return pd.DataFrame(), available_sheets, target, encoding, warnings, errors

    return df, available_sheets, target, encoding, warnings, errors


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def process_file(
    file_path: str,
    sheet_name: Optional[str] = None,
) -> UploadResult:
    """
    Processa um único arquivo e retorna UploadResult com metadados e preview.

    Args:
        file_path: Caminho para o arquivo (.xlsx, .xls ou .csv).
        sheet_name: Aba a ler em arquivos Excel com múltiplas abas.
                    Se None e houver múltiplas abas, retorna available_sheets
                    com success=False aguardando seleção.

    Returns:
        UploadResult preenchido; success=False indica erro ou seleção pendente.
    """
    warnings: list[str] = []
    errors: list[str] = []

    path = Path(file_path)
    file_name = path.name
    extension = path.suffix.lstrip(".").lower()

    def _fail(
        fmt: str,
        err: list[str],
        encoding: str = "unknown",
        sep: Optional[str] = None,
        available: Optional[list[str]] = None,
    ) -> UploadResult:
        return UploadResult(
            file_name=file_name,
            file_format=fmt,
            sheet_name=None,
            available_sheets=available or [],
            row_count=0,
            column_count=0,
            columns=[],
            preview=[],
            encoding_detected=encoding,
            separator_detected=sep,
            warnings=warnings,
            errors=err,
            success=False,
        )

    if not path.exists():
        return _fail(extension or "unknown", [f"Arquivo não encontrado: {file_path}"])

    if extension not in SUPPORTED_FORMATS:
        return _fail(
            extension or "unknown",
            [f"Formato não suportado: '.{extension}'. Aceitos: xlsx, xls, csv."],
        )

    try:
        arquivo_bytes = path.read_bytes()
    except Exception as exc:
        return _fail(extension, [f"Erro ao ler bytes do arquivo: {exc}"])

    # ---- CSV ---------------------------------------------------------------
    if extension == "csv":
        df, encoding, separator, w, e = _read_csv(file_path)
        warnings.extend(w)
        errors.extend(e)

        if errors:
            return _fail("csv", errors, encoding, separator)

        df = _rename_unnamed_columns(df, warnings)

        if len(df) > 100_000:
            warnings.append(
                f"Arquivo contém {len(df):,} linhas — volume acima de 100.000 pode impactar o desempenho."
            )

        return UploadResult(
            file_name=file_name,
            file_format="csv",
            sheet_name=None,
            available_sheets=[],
            row_count=len(df),
            column_count=len(df.columns),
            columns=[_build_column_info(c, df[c]) for c in df.columns],
            preview=_build_preview(df),
            encoding_detected=encoding,
            separator_detected=separator,
            warnings=warnings,
            errors=[],
            success=True,
            arquivo_bytes=arquivo_bytes,
        )

    # ---- Excel -------------------------------------------------------------
    df, available_sheets, sheet_used, encoding, w, e = _read_excel(
        file_path, sheet_name
    )
    warnings.extend(w)
    errors.extend(e)

    if errors:
        return _fail(extension, errors, encoding, available=available_sheets)

    # Múltiplas abas, aguardando seleção — Motor Base fará a seleção automática
    if len(available_sheets) > 1 and sheet_used is None:
        return UploadResult(
            file_name=file_name,
            file_format=extension,
            sheet_name=None,
            available_sheets=available_sheets,
            row_count=0,
            column_count=0,
            columns=[],
            preview=[],
            encoding_detected=encoding,
            separator_detected=None,
            warnings=["Arquivo com múltiplas abas. Especifique a aba desejada via sheet_name."],
            errors=[],
            success=True,
            arquivo_bytes=arquivo_bytes,
        )

    df = _rename_unnamed_columns(df, warnings)

    if len(df) > 100_000:
        warnings.append(
            f"Arquivo contém {len(df):,} linhas — volume acima de 100.000 pode impactar o desempenho."
        )

    return UploadResult(
        file_name=file_name,
        file_format=extension,
        sheet_name=sheet_used,
        available_sheets=available_sheets,
        row_count=len(df),
        column_count=len(df.columns),
        columns=[_build_column_info(c, df[c]) for c in df.columns],
        preview=_build_preview(df),
        encoding_detected=encoding,
        separator_detected=None,
        warnings=warnings,
        errors=[],
        success=True,
        arquivo_bytes=arquivo_bytes,
    )


def process_files(
    file_paths: list[str],
    sheet_names: Optional[dict[str, str]] = None,
) -> list[UploadResult]:
    """
    Processa múltiplos arquivos e retorna uma lista de UploadResult.

    Args:
        file_paths: Lista de caminhos de arquivos.
        sheet_names: Mapeamento opcional de file_path → sheet_name para Excel.

    Returns:
        Lista de UploadResult na mesma ordem dos file_paths.
    """
    return [
        process_file(fp, sheet_name=(sheet_names or {}).get(fp))
        for fp in file_paths
    ]
