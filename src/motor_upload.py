"""
motor_upload.py v2 — TabloFlow · Fase 1 · F-MOT
Lê arquivos Excel/CSV e produz UploadResult com preview e bytes preservados.

API pública: processar_upload(arquivos, modo, abas_selecionadas) → UploadResult

Decisões implementadas:
  D-007 · arquivo_bytes preservado em memória
  D-008 · boolean disfarçado sinalizado em preview (classificação completa fica em motor_base)
  D-018 · T-DUAL: 2 arquivos OU 1 arquivo 2 abas · Motor não distingue formatos
  D-026 · reconhecedor cronológico DEFERIDO para motor_base (exige coluna completa · D-133)
  D-103 · subtipo ID DEFERIDO para motor_base (D-133)
  B.5  · encoding csv: utf-8 → fallback latin-1 · csv.Sniffer para separador
"""
from __future__ import annotations

import csv
import re
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Literal, Optional

import pandas as pd
from pydantic import BaseModel, Field

from contratos import (
    ArquivoInfo,
    CategoriaWarning,
    UploadResult,
    WarningEstrutural,
)

# Formatos suportados
_FORMATOS_EXCEL = {"xlsx", "xlsm"}
_FORMATOS_CSV = {"csv", "tsv"}
_FORMATOS_SUPORTADOS = _FORMATOS_EXCEL | _FORMATOS_CSV

# Null-strings normalizados no preview (mesma lista do motor_base)
_NULL_STRINGS: frozenset[str] = frozenset(
    {"", "n/a", "na", "null", "none", "-", "--", "---"}
)


# ---------------------------------------------------------------------------
# Contrato de entrada
# ---------------------------------------------------------------------------

class ArquivoEntrada(BaseModel):
    """Descritor de um arquivo a ser processado pelo motor_upload."""
    caminho_fisico: str = Field(
        ...,
        description="Caminho físico do arquivo no sistema de arquivos"
    )
    caminho_logico: Literal["origem", "comparado", "unico"] = Field(
        ...,
        description="Papel lógico do arquivo · T-DUAL: 'origem' ou 'comparado' · simples: 'unico'"
    )
    aba_solicitada: Optional[str] = Field(
        None,
        description="Aba do Excel a ler · None = primeira aba disponível · obrigatório em T-DUAL com 1 arquivo 2 abas"
    )


# ---------------------------------------------------------------------------
# Helpers privados
# ---------------------------------------------------------------------------

def _warning(codigo: str, categoria: CategoriaWarning, microcopy: str, **ctx) -> WarningEstrutural:
    return WarningEstrutural(codigo=codigo, categoria=categoria, microcopy=microcopy, contexto=dict(ctx))


def _is_null_like(v: object) -> bool:
    if v is None:
        return True
    try:
        if pd.isna(v):  # type: ignore[arg-type]
            return True
    except (TypeError, ValueError):
        pass
    return str(v).strip().lower() in _NULL_STRINGS


def _build_preview(df: pd.DataFrame) -> Dict[str, List]:
    """5 linhas em orientação column → [values] · valores None para nulos."""
    sample = df.head(5)
    result: Dict[str, List] = {}
    for col in sample.columns:
        result[col] = [
            None if _is_null_like(v) else (v if isinstance(v, (int, float, bool, str)) else str(v))
            for v in sample[col].tolist()
        ]
    return result


def _rename_unnamed(df: pd.DataFrame, warnings: list) -> pd.DataFrame:
    """Renomeia colunas sem nome para Coluna_N · C.2 nada silencioso."""
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
        warnings.append(_warning(
            "W-U-COLUNA-SEM-NOME",
            CategoriaWarning.AJUSTE_LEVE,
            f"Cabeçalho com células vazias — {counter} coluna(s) renomeada(s) para 'Coluna_N'.",
            quantidade=counter,
        ))
    df = df.copy()
    df.columns = new_cols  # type: ignore[assignment]
    return df


def _detect_encoding(file_path: str) -> str:
    """Detecta encoding: tenta utf-8 · fallback latin-1 (cp1252)."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            f.read(4_096)
        return "utf-8"
    except (UnicodeDecodeError, OSError):
        return "latin-1"


def _detect_separator(file_path: str, encoding: str) -> str:
    """Detecta separador CSV via Sniffer · fallback vírgula · segundo fallback ponto-e-vírgula."""
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


def _ler_csv(
    file_path: str,
    warnings: list,
) -> tuple[pd.DataFrame, str, str]:
    """Lê CSV detectando encoding e separador. Retorna (df, encoding, separador)."""
    encoding = _detect_encoding(file_path)
    separator = _detect_separator(file_path, encoding)

    try:
        df = pd.read_csv(
            file_path,
            sep=separator,
            encoding=encoding,
            skip_blank_lines=True,
            on_bad_lines="warn",
        )
        return df, encoding, separator
    except UnicodeDecodeError:
        pass

    # Fallback latin-1
    try:
        df = pd.read_csv(
            file_path,
            sep=separator,
            encoding="latin-1",
            skip_blank_lines=True,
            on_bad_lines="warn",
        )
        warnings.append(_warning(
            "W-U-ENCODING-FALLBACK",
            CategoriaWarning.INFORMATIVO,
            f"Arquivo CSV lido com fallback latin-1 (cp1252) — encoding utf-8 falhou.",
            encoding_tentado="utf-8",
            encoding_usado="latin-1",
        ))
        return df, "latin-1", separator
    except Exception as exc:
        raise RuntimeError(f"Falha de encoding mesmo com fallback latin-1: {exc}") from exc


def _ler_excel(
    file_path: str,
    aba_solicitada: Optional[str],
    warnings: list,
) -> tuple[pd.DataFrame, list[str], str]:
    """Lê Excel. Retorna (df, abas_disponiveis, aba_selecionada)."""
    xl = pd.ExcelFile(file_path)
    abas: list[str] = xl.sheet_names

    if not abas:
        raise RuntimeError("Arquivo Excel não contém abas.")

    if aba_solicitada is not None:
        if aba_solicitada not in abas:
            raise RuntimeError(
                f"Aba '{aba_solicitada}' não encontrada. Disponíveis: {abas}"
            )
        aba = aba_solicitada
    else:
        aba = abas[0]
        if len(abas) > 1:
            warnings.append(_warning(
                "W-U-MULTI-ABA-AUTO",
                CategoriaWarning.INFORMATIVO,
                f"Excel com {len(abas)} abas — aba '{aba}' selecionada automaticamente.",
                abas_disponiveis=abas,
                aba_selecionada=aba,
            ))

    df = pd.read_excel(file_path, sheet_name=aba, engine="openpyxl")
    return df, abas, aba


def _processar_arquivo_entrada(entrada: ArquivoEntrada) -> tuple[ArquivoInfo, list]:
    """Processa um único ArquivoEntrada e retorna (ArquivoInfo, warnings)."""
    warnings: list = []
    path = Path(entrada.caminho_fisico)

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {entrada.caminho_fisico}")

    extensao = path.suffix.lstrip(".").lower()
    if extensao not in _FORMATOS_SUPORTADOS:
        raise ValueError(
            f"Formato não suportado: '.{extensao}'. Aceitos: {sorted(_FORMATOS_SUPORTADOS)}"
        )

    arquivo_bytes = path.read_bytes()

    if extensao in _FORMATOS_CSV:
        df, encoding, separador = _ler_csv(str(path), warnings)
        df = _rename_unnamed(df, warnings)
        if len(df) == 0:
            warnings.append(_warning(
                "W-U-ARQUIVO-VAZIO",
                CategoriaWarning.ALERTA_ESTRUTURAL,
                f"Arquivo '{path.name}' sem dados após parse.",
            ))

        info = ArquivoInfo(
            caminho_logico=entrada.caminho_logico,
            nome_arquivo=path.name,
            arquivo_bytes=arquivo_bytes,
            abas_disponiveis=[],
            aba_selecionada="",
            formato="tsv" if extensao == "tsv" else "csv",
            preview=_build_preview(df),
            encoding_detectado=encoding,
            separador_csv=separador,
        )
    else:
        df, abas, aba = _ler_excel(str(path), entrada.aba_solicitada, warnings)
        df = _rename_unnamed(df, warnings)
        if len(df) == 0:
            warnings.append(_warning(
                "W-U-ARQUIVO-VAZIO",
                CategoriaWarning.ALERTA_ESTRUTURAL,
                f"Arquivo '{path.name}' aba '{aba}' sem dados após parse.",
            ))

        info = ArquivoInfo(
            caminho_logico=entrada.caminho_logico,
            nome_arquivo=path.name,
            arquivo_bytes=arquivo_bytes,
            abas_disponiveis=abas,
            aba_selecionada=aba,
            formato=extensao,  # type: ignore[arg-type]
            preview=_build_preview(df),
            encoding_detectado=None,
            separador_csv=None,
        )

    return info, warnings


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def processar_upload(
    arquivos: List[ArquivoEntrada],
    modo: Literal["SIMPLES", "DUAL"],
    abas_selecionadas: Optional[Dict[str, str]] = None,
) -> UploadResult:
    """
    Processa arquivos e retorna UploadResult com preview e bytes preservados.

    Args:
        arquivos:
            Modo SIMPLES: lista com 1 ArquivoEntrada (caminho_logico="unico").
            Modo DUAL: lista com 2 entradas — caminho_logico "origem" e "comparado".
            DUAL com 1 arquivo 2 abas: 2 entradas com mesmo caminho_fisico e abas distintas.
        modo: "SIMPLES" ou "DUAL" · declarado pelo chamador · motor não infere.
        abas_selecionadas: Opcional · {caminho_logico: nome_aba} · sobrescreve aba_solicitada.

    Returns:
        UploadResult com arquivo_unico (SIMPLES) ou arquivos_dual (DUAL).

    Raises:
        ValueError: modo inválido ou quantidade de arquivos incompatível.
        FileNotFoundError: arquivo físico não encontrado.
        RuntimeError: erro de leitura do arquivo.
    """
    if modo == "SIMPLES" and len(arquivos) != 1:
        raise ValueError(f"Modo SIMPLES requer exatamente 1 arquivo · recebidos: {len(arquivos)}")
    if modo == "DUAL" and len(arquivos) != 2:
        raise ValueError(f"Modo DUAL requer exatamente 2 entradas · recebidas: {len(arquivos)}")

    # Aplica abas_selecionadas se fornecido
    if abas_selecionadas:
        arquivos = [
            ArquivoEntrada(
                caminho_fisico=a.caminho_fisico,
                caminho_logico=a.caminho_logico,
                aba_solicitada=abas_selecionadas.get(a.caminho_logico, a.aba_solicitada),
            )
            for a in arquivos
        ]

    todos_warnings: list = []
    infos: list[ArquivoInfo] = []

    for entrada in arquivos:
        info, warnings = _processar_arquivo_entrada(entrada)
        todos_warnings.extend(warnings)
        infos.append(info)

    if modo == "SIMPLES":
        return UploadResult(
            file_name=infos[0].nome_arquivo,
            modo_upload="SIMPLES",
            arquivo_unico=infos[0],
            arquivos_dual=None,
            timestamp_upload=datetime.now(),
            warnings=todos_warnings,
        )
    else:
        # DUAL: ordena para garantir [origem, comparado]
        origem = next((i for i in infos if i.caminho_logico == "origem"), infos[0])
        comparado = next((i for i in infos if i.caminho_logico == "comparado"), infos[1])
        return UploadResult(
            file_name=origem.nome_arquivo,
            modo_upload="DUAL",
            arquivo_unico=None,
            arquivos_dual=[origem, comparado],
            timestamp_upload=datetime.now(),
            warnings=todos_warnings,
        )
