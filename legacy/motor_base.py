"""
Motor Base — TabloFlow
Segunda camada da pipeline. Recebe UploadResult, normaliza dados e produz MotorResult.
Pipeline: Arquivo bruto → motor_upload → UploadResult → motor_base → MotorResult → Visão
"""

import re
from io import BytesIO
from typing import Any, Optional

import numpy as np
import pandas as pd
from pydantic import BaseModel

from motor_upload import ColumnInfo, UploadResult

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

CATEGORICAL_THRESHOLD = 50

NULL_STRINGS: frozenset[str] = frozenset(
    {"", "n/a", "na", "null", "none", "-", "--", "---"}
)

DATE_FORMATS: list[str] = [
    "%d/%m/%Y",
    "%Y-%m-%d",
    "%Y-%m-%d %H:%M:%S",
    "%d-%m-%Y",
    "%m/%d/%Y",
    "%Y%m%d",
]

BOOL_MAP: dict[str, bool] = {
    "true": True,  "false": False,
    "sim": True,   "não": False, "nao": False,
    "s": True,     "n": False,
    "yes": True,   "no": False,
    "1": True,     "0": False,
    "1.0": True,   "0.0": False,
}

_CURRENCY_RE = re.compile(r"R\$|[$€£]|\s")


# ---------------------------------------------------------------------------
# Contratos de saída
# ---------------------------------------------------------------------------

class ColumnMeta(BaseModel):
    nome: str
    tipo: str                   # "numeric"|"text"|"date"|"boolean"|"mixed"|"empty"
    null_count: int
    null_pct: float             # 0.0 a 1.0
    n_unique: int
    sample_values: list[str]    # até 5 valores de exemplo como string
    is_candidate_key: bool
    is_candidate_numeric: bool
    is_candidate_date: bool
    is_candidate_categorical: bool


class MotorResult(BaseModel):
    success: bool
    source_file: str
    aba_processada: Optional[str]
    n_linhas: int
    n_colunas: int
    colunas: list[ColumnMeta]
    warnings: list[str]
    errors: list[str]
    df: Optional[object]        # DataFrame pandas normalizado — não serializar em JSON

    model_config = {"arbitrary_types_allowed": True}


# ---------------------------------------------------------------------------
# Helpers de conversão numérica
# ---------------------------------------------------------------------------

def _clean_numeric(s: str) -> Optional[float]:
    """
    Tenta converter string para float removendo símbolos de moeda e separadores
    de milhar; aceita ponto e vírgula como separador decimal.

    Returns float ou None se a conversão falhar.
    """
    cleaned = _CURRENCY_RE.sub("", s.strip())
    if not cleaned:
        return None

    try:
        return float(cleaned)
    except ValueError:
        pass

    has_dot = "." in cleaned
    has_comma = "," in cleaned

    if has_dot and has_comma:
        last_dot = cleaned.rfind(".")
        last_comma = cleaned.rfind(",")
        if last_comma > last_dot:
            # padrão BR: 1.234,56 → decimal é vírgula
            normalized = cleaned.replace(".", "").replace(",", ".")
        else:
            # padrão US: 1,234.56 → decimal é ponto
            normalized = cleaned.replace(",", "")
    elif has_comma:
        after_comma = cleaned.rsplit(",", 1)[-1]
        if len(after_comma) == 3 and cleaned.count(",") == 1:
            # provavelmente separador de milhar: 1,234
            normalized = cleaned.replace(",", "")
        else:
            # provavelmente separador decimal: 1,56
            normalized = cleaned.replace(",", ".")
    else:
        return None

    try:
        return float(normalized)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Helpers de data
# ---------------------------------------------------------------------------

def _try_parse_date(s: str) -> Optional[pd.Timestamp]:
    """
    Tenta converter string para pd.Timestamp usando os formatos definidos em DATE_FORMATS.

    Returns pd.Timestamp ou None se nenhum formato funcionar.
    """
    for fmt in DATE_FORMATS:
        try:
            return pd.to_datetime(s, format=fmt)
        except (ValueError, TypeError):
            continue
    return None


# ---------------------------------------------------------------------------
# Helpers de normalização de nulos
# ---------------------------------------------------------------------------

def _is_null_like(val: Any) -> bool:
    """Retorna True se o valor é considerado nulo per spec seção 5."""
    if val is None:
        return True
    try:
        if pd.isna(val):
            return True
    except (TypeError, ValueError):
        pass
    return str(val).strip().lower() in NULL_STRINGS


def _normalize_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Substitui todos os valores nulos e null-like por NaN em todas as colunas.
    Nunca remove linhas — apenas substitui valores.

    Returns novo DataFrame com nulos normalizados.
    """
    result = df.copy()
    for col in result.columns:
        result[col] = [np.nan if _is_null_like(v) else v for v in result[col]]
    return result


# ---------------------------------------------------------------------------
# Helpers de cabeçalho
# ---------------------------------------------------------------------------

def _rename_empty_columns(df: pd.DataFrame, warnings: list[str]) -> pd.DataFrame:
    """
    Renomeia colunas sem nome (vazias, Unnamed:N, nan) para Coluna_N.
    Registra warning se alguma renomeação ocorrer.

    Returns DataFrame com colunas renomeadas.
    """
    new_cols: list[str] = []
    counter = 0
    renamed = False
    for col in df.columns:
        s = str(col).strip()
        if s == "" or s == "nan" or s.startswith("Unnamed:"):
            counter += 1
            new_cols.append(f"Coluna_{counter}")
            renamed = True
        else:
            new_cols.append(s)
    if renamed:
        warnings.append(
            "Cabeçalho com células vazias — colunas renomeadas como 'Coluna_N'."
        )
    df.columns = new_cols
    return df


def _deduplicate_columns(df: pd.DataFrame, warnings: list[str]) -> pd.DataFrame:
    """
    Detecta nomes de colunas duplicados e adiciona sufixos _2, _3, etc.
    Registra warning se duplicatas forem encontradas.

    Returns DataFrame com colunas sem duplicatas.
    """
    seen: dict[str, int] = {}
    new_cols: list[str] = []
    has_dupes = False
    for col in df.columns:
        if col in seen:
            has_dupes = True
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 1
            new_cols.append(col)
    if has_dupes:
        warnings.append(
            "Cabeçalho com nomes duplicados detectado — sufixos _2, _3... adicionados."
        )
    df.columns = new_cols
    return df


# ---------------------------------------------------------------------------
# Inferência de tipo (seção 4)
# ---------------------------------------------------------------------------

_BOOL_NUMERIC_VALUES: frozenset = frozenset({0, 1, 0.0, 1.0, True, False})


def _infer_type_from_series(series: pd.Series) -> str:
    """
    Infere o tipo semântico de uma coluna conforme regras da spec seção 4.
    Tipos possíveis: "numeric", "text", "date", "boolean", "mixed", "empty".

    Returns string com o tipo inferido.
    """
    non_null = series.dropna()

    if len(non_null) == 0:
        return "empty"

    # boolean nativo
    if pd.api.types.is_bool_dtype(series):
        return "boolean"

    # numérico nativo
    if pd.api.types.is_numeric_dtype(series):
        # Bloco V-0c: Excel promove bool+null para float64 (valores em {0,1,NaN}).
        # Se a coluna é numérica, tem pelo menos 1 null e todos os não-nulos
        # são {0,1} (ou equivalentes float/bool), classifica como boolean.
        # Ver comentário cruzado com BOOL_MAP ("1.0"/"0.0").
        has_null = bool(series.isna().any())
        if has_null and set(non_null.unique()).issubset(_BOOL_NUMERIC_VALUES):
            return "boolean"
        return "numeric"

    # datetime nativo
    if pd.api.types.is_datetime64_any_dtype(series):
        return "date"

    # a partir daqui: inferência sobre strings
    str_vals = non_null.astype(str).str.strip()
    total = len(str_vals)

    # boolean por valor — inclui "1.0"/"0.0" (Excel converte bool+null para float)
    bool_keys = set(BOOL_MAP.keys()) | {"1.0", "0.0"}
    if all(v.lower() in bool_keys for v in str_vals):
        return "boolean"

    # numérico: ≥80% convertíveis (com limpeza de moeda/milhar)
    numeric_hits = sum(1 for v in str_vals if _clean_numeric(v) is not None)
    numeric_ratio = numeric_hits / total

    if numeric_ratio >= 0.8:
        return "numeric"

    # data: ≥80% convertíveis com os formatos permitidos
    date_hits = sum(1 for v in str_vals if _try_parse_date(v) is not None)
    date_ratio = date_hits / total

    if date_ratio >= 0.8:
        return "date"

    # misto: alguma proporção de numérico mas não atingiu 80%
    if numeric_ratio > 0.0:
        return "mixed"

    return "text"


# ---------------------------------------------------------------------------
# Conversão de tipos no DataFrame normalizado
# ---------------------------------------------------------------------------

def _apply_type_conversions(
    df: pd.DataFrame, columns_meta: list[ColumnMeta]
) -> pd.DataFrame:
    """
    Converte cada coluna do DataFrame para o tipo inferido em columns_meta.
    Nunca modifica os dados originais — trabalha sobre cópia.

    Returns DataFrame com colunas convertidas.
    """
    result = df.copy()
    for meta in columns_meta:
        col = meta.nome
        if col not in result.columns:
            continue
        series = result[col]

        if meta.tipo == "numeric":
            result[col] = series.apply(
                lambda v: _clean_numeric(str(v)) if pd.notna(v) else None
            )

        elif meta.tipo == "date":
            result[col] = series.apply(
                lambda v: _try_parse_date(str(v)) if pd.notna(v) else None
            )

        elif meta.tipo == "boolean":
            result[col] = series.apply(
                lambda v: BOOL_MAP.get(str(v).strip().lower()) if pd.notna(v) else None
            )

        elif meta.tipo == "text":
            result[col] = series.apply(
                lambda v: str(v).strip() if pd.notna(v) else None
            )
        # "empty" e "mixed": mantém como está (object)

    return result


# ---------------------------------------------------------------------------
# Seleção de aba (seção 6)
# ---------------------------------------------------------------------------

def _resolve_sheet(
    upload_result: UploadResult,
    sheet_name: Optional[str],
    warnings: list[str],
    errors: list[str],
) -> Optional[str]:
    """
    Resolve qual aba usar conforme regras da spec seção 6.

    Returns nome da aba selecionada ou None para CSV.
    Popula errors se a aba solicitada não for encontrada.
    """
    if upload_result.file_format == "csv":
        return None

    available = upload_result.available_sheets

    if sheet_name is not None:
        if available and sheet_name not in available:
            errors.append(
                f"Aba '{sheet_name}' não encontrada. Disponíveis: {available}"
            )
            return None
        return sheet_name

    # Auto-seleção
    if upload_result.sheet_name:
        return upload_result.sheet_name

    if not available:
        return None

    if len(available) == 1:
        return available[0]

    # Múltiplas abas: seleciona a primeira e avisa
    warnings.append(
        f"Múltiplas abas detectadas; primeira selecionada automaticamente: "
        f"'{available[0]}'."
    )
    return available[0]


# ---------------------------------------------------------------------------
# Construção de ColumnMeta (seção 3 + 5 + 7 + 8)
# ---------------------------------------------------------------------------

def _build_column_meta(
    col_name: str,
    series: pd.Series,
    col_info: Optional[ColumnInfo],
    total_rows: int,
    warnings: list[str],
) -> ColumnMeta:
    """
    Constrói ColumnMeta para uma coluna usando stats do UploadResult (dados completos)
    e inferência de tipo sobre a série normalizada do preview.

    Args:
        col_name: Nome da coluna.
        series: Série normalizada (preview).
        col_info: ColumnInfo do UploadResult com stats do arquivo completo.
        total_rows: Total de linhas do arquivo completo (sem cabeçalho).
        warnings: Lista de warnings a ser populada.

    Returns ColumnMeta completo.
    """
    # Preferir stats do arquivo completo (col_info) para null_count e unique_count.
    # col_info.null_count já inclui null-strings normalizados pelo motor_upload.
    # Fallback para a série de preview quando col_info não disponível.
    if col_info is not None and total_rows > 0:
        null_count = col_info.null_count
        unique_count = col_info.unique_count
    else:
        null_count = int(series.isna().sum())
        unique_count = int(series.nunique(dropna=True))

    null_pct = null_count / total_rows if total_rows > 0 else 0.0

    # Tipo: se null_count == total_rows → forçar "empty"
    if total_rows > 0 and null_count >= total_rows:
        inferred_type = "empty"
    else:
        inferred_type = _infer_type_from_series(series)

    # Warnings por tipo e nulos
    if inferred_type == "empty":
        warnings.append(f"Coluna '{col_name}' está completamente vazia.")
    elif inferred_type == "mixed":
        warnings.append(
            f"Coluna '{col_name}' tem tipos mistos — tratada como texto."
        )
    elif (
        inferred_type == "boolean"
        and not pd.api.types.is_bool_dtype(series)
        and pd.api.types.is_numeric_dtype(series)
    ):
        warnings.append(
            f"W-B01: Coluna '{col_name}' classificada como boolean por padrão "
            f"de valores {{0,1,NaN}}. Confirmar se a intenção analítica é de "
            f"flag binário ou de medida numérica."
        )

    if null_pct > 0.5:
        warnings.append(
            f"Coluna '{col_name}' tem {null_pct:.0%} de nulos."
        )

    # Amostras: até 5 valores não-nulos do preview
    sample_values = [str(v) for v in series.dropna().head(5).tolist()]

    # Flags de candidatos (seção 7)
    non_null_rows = total_rows - null_count
    is_candidate_key = (unique_count == non_null_rows) and non_null_rows > 0
    is_candidate_numeric = inferred_type == "numeric"
    is_candidate_date = inferred_type == "date"
    is_candidate_categorical = (
        inferred_type == "text" and unique_count <= CATEGORICAL_THRESHOLD
    )

    return ColumnMeta(
        nome=col_name,
        tipo=inferred_type,
        null_count=null_count,
        null_pct=round(null_pct, 4),
        n_unique=unique_count,
        sample_values=sample_values,
        is_candidate_key=is_candidate_key,
        is_candidate_numeric=is_candidate_numeric,
        is_candidate_date=is_candidate_date,
        is_candidate_categorical=is_candidate_categorical,
    )


# ---------------------------------------------------------------------------
# Helper de falha
# ---------------------------------------------------------------------------

def _fail_motor_result(
    source_file: str,
    selected_sheet: Optional[str],
    errors: list[str],
    warnings: Optional[list[str]] = None,
) -> MotorResult:
    """Retorna MotorResult com success=False e erros descritos."""
    return MotorResult(
        success=False,
        source_file=source_file,
        aba_processada=selected_sheet,
        n_linhas=0,
        n_colunas=0,
        colunas=[],
        warnings=warnings or [],
        errors=errors,
        df=None,
    )


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def processar_motor_base(
    upload_result: UploadResult,
    sheet_name: Optional[str] = None,
) -> MotorResult:
    """
    Recebe um UploadResult e retorna um MotorResult normalizado.

    Aplica: seleção de aba, normalização de nulos, inferência de tipos,
    renomeação de colunas problemáticas e cálculo de flags de candidatos.

    Args:
        upload_result: Resultado do motor_upload (deve ter success=True).
        sheet_name: Nome da aba a selecionar (None = automático).

    Returns:
        MotorResult com df normalizado, metadados por coluna, warnings e errors.
        Se success=False, df será None e errors descreverá o motivo.
    """
    warnings: list[str] = []
    errors: list[str] = []

    # --- Validação do UploadResult -----------------------------------------
    if not isinstance(upload_result, UploadResult):
        return _fail_motor_result(
            "", None, ["Parâmetro upload_result não é um UploadResult válido."]
        )

    if not upload_result.success:
        detail = "; ".join(upload_result.errors) if upload_result.errors else "sem detalhes"
        return _fail_motor_result(
            upload_result.file_name,
            None,
            [f"UploadResult com success=False: {detail}"],
        )

    # --- Seleção de aba -------------------------------------------------------
    selected_sheet = _resolve_sheet(upload_result, sheet_name, warnings, errors)
    if errors:
        return _fail_motor_result(
            upload_result.file_name, selected_sheet, errors, warnings
        )

    # --- Construção do DataFrame a partir do arquivo completo ----------------
    # Bloco V-0c: ler arquivo_bytes (arquivo completo) em vez de preview (5 linhas).
    # Preview continua exposto no UploadResult para a etapa de configuração no app.
    if not upload_result.arquivo_bytes:
        return _fail_motor_result(
            upload_result.file_name,
            selected_sheet,
            ["UploadResult sem arquivo_bytes — motor_upload não populou o campo."],
            warnings,
        )

    try:
        buffer = BytesIO(upload_result.arquivo_bytes)
        if upload_result.file_format == "csv":
            df = pd.read_csv(
                buffer,
                sep=upload_result.separator_detected or ",",
                encoding=upload_result.encoding_detected or "utf-8",
                skip_blank_lines=True,
            )
        else:
            df = pd.read_excel(buffer, sheet_name=selected_sheet)
    except Exception as exc:
        return _fail_motor_result(
            upload_result.file_name,
            selected_sheet,
            [f"Falha inesperada na leitura do DataFrame: {exc}"],
            warnings,
        )

    # --- Validação de dimensões -----------------------------------------------
    if upload_result.row_count == 0:
        errors.append("DataFrame resultante tem 0 linhas.")
        return _fail_motor_result(
            upload_result.file_name, selected_sheet, errors, warnings
        )

    if upload_result.column_count == 0:
        errors.append("DataFrame resultante tem 0 colunas.")
        return _fail_motor_result(
            upload_result.file_name, selected_sheet, errors, warnings
        )

    # --- Normalização do DataFrame -------------------------------------------
    df = _normalize_nulls(df)
    df = _rename_empty_columns(df, warnings)
    df = _deduplicate_columns(df, warnings)

    # --- Metadados de colunas ------------------------------------------------
    col_info_map: dict[str, ColumnInfo] = {ci.name: ci for ci in upload_result.columns}

    columns_meta: list[ColumnMeta] = [
        _build_column_meta(
            col_name=col,
            series=df[col],
            col_info=col_info_map.get(col),
            total_rows=upload_result.row_count,
            warnings=warnings,
        )
        for col in df.columns
    ]

    # --- Conversão de tipos no df --------------------------------------------
    df = _apply_type_conversions(df, columns_meta)

    return MotorResult(
        success=True,
        source_file=upload_result.file_name,
        aba_processada=selected_sheet,
        n_linhas=upload_result.row_count,
        n_colunas=upload_result.column_count,
        colunas=columns_meta,
        warnings=warnings,
        errors=[],
        df=df,
    )
