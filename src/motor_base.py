"""
motor_base.py v2 — TabloFlow · Fase 1 · F-MOT
Processa UploadResult e produz MotorResult com column_meta completa.

API pública: processar_base(upload_result, config?) → MotorResult

Decisões implementadas:
  D-007 · DataFrame completo lido de arquivo_bytes (não do preview)
  D-008 · boolean disfarçado: float64 {0,1,NaN} → tipo_semantico=boolean → BOOLEANO + W-B01
  D-026 · reconhecedor pt-BR/pt-EN · 7 padrões · threshold 80%
  D-103 · subtipo ID: heurística 3 condições sobre coluna completa
  D-113 · tipo_estrutural: 5 valores · algoritmo canônico C.2
  D-133 · tipo_estrutural SEMPRE computado · não lazy · não opcional
  D-134 · BloqueioOperacional emitido quando cardinalidade excessiva detectada
  C.1   · determinismo absoluto · sem random · sem ordenação instável
  C.2   · nada silencioso · toda inferência não-perfeita emite warning
  C.5   · base < 2M linhas ou bloqueio sem escape
"""
from __future__ import annotations

import re
from datetime import datetime
from io import BytesIO
from typing import Dict, List, Literal, Optional, Tuple

import numpy as np
import pandas as pd

from contratos import (
    AjusteMotor,
    BloqueioOperacional,
    CategoriaWarning,
    ColumnMeta,
    MotorConfig,
    MotorResult,
    PadraoCronologicoEnum,
    TipoEstruturalEnum,
    TipoSemanticoEnum,
    TipoTecnicoEnum,
    UploadResult,
    WarningEstrutural,
)

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

_NULL_STRINGS: frozenset[str] = frozenset(
    {"", "n/a", "na", "null", "none", "-", "--", "---"}
)

_BOOL_VALORES: frozenset = frozenset({0, 1, 0.0, 1.0, True, False})

_BOOL_STRINGS: frozenset[str] = frozenset({
    "true", "false", "sim", "não", "nao", "s", "n", "yes", "no",
    "1", "0", "1.0", "0.0",
})

_CURRENCY_RE = re.compile(r"[R$€£\s]")

# Meses pt-BR (abreviações e nomes completos em lowercase)
_MESES_PT = {
    "jan", "fev", "mar", "abr", "mai", "jun",
    "jul", "ago", "set", "out", "nov", "dez",
    "janeiro", "fevereiro", "março", "marco", "abril", "maio",
    "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
}

# Meses en (abreviações e nomes completos em lowercase)
_MESES_EN = {
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec",
    "january", "february", "march", "april", "june",
    "july", "august", "september", "october", "november", "december",
}

# Padrões regex para reconhecimento cronológico (D-026)
_RE_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}.*)?$")
_RE_PT_BR_DATE = re.compile(r"^\d{1,2}[/-]\d{1,2}[/-]\d{4}$")
_RE_COMPACT_MONTHYEAR = re.compile(r"^\d{4}-\d{2}$|^\d{6}$|^\d{2}/\d{4}$")
_RE_Q_TRIMESTRE = re.compile(
    r"^[QqTt]\d(\s+\d{2,4})?$|^\d\s*[°ºo°]*\s*[Tt]rim", re.IGNORECASE
)

# Padrão regex para meses PT com ano opcional
_RE_MONTH_PT = re.compile(
    r"^(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez"
    r"|janeiro|fevereiro|mar[cç]o|abril|maio|junho|julho|agosto"
    r"|setembro|outubro|novembro|dezembro)"
    r"([/-]|\s+)?\d{0,4}$",
    re.IGNORECASE,
)

# Padrão regex para meses EN com ano opcional
_RE_MONTH_EN = re.compile(
    r"^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec"
    r"|january|february|march|april|june|july|august"
    r"|september|october|november|december)"
    r"([/-]|\s+)?\d{0,4}$",
    re.IGNORECASE,
)

# Padrão regex para IDs
_RE_CPF = re.compile(r"^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$")
_RE_CNPJ = re.compile(r"^\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}$")
_RE_UUID = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)
_RE_MATRICULA = re.compile(r"^[A-Z]{0,3}\d{5,}$")


# ---------------------------------------------------------------------------
# Helpers de warning e bloqueio
# ---------------------------------------------------------------------------

def _w(codigo: str, categoria: CategoriaWarning, microcopy: str, **ctx) -> WarningEstrutural:
    return WarningEstrutural(
        codigo=codigo,
        categoria=categoria,
        microcopy=microcopy,
        contexto=dict(ctx),
    )


def _bloqueio(
    codigo: str,
    condicao: str,
    escapavel: bool,
    **ctx,
) -> BloqueioOperacional:
    return BloqueioOperacional(
        codigo=codigo,
        condicao_disparo=condicao,
        escapavel=escapavel,
        escape_acionado=None,
        contexto_disparo=dict(ctx),
    )


# ---------------------------------------------------------------------------
# Reconhecedor cronológico pt-BR/pt-EN (D-026)
# Prioridade: ISO_DATE > PT_BR_DATE > COMPACT_MONTHYEAR > MONTH_NAME_PT
#             > MONTH_NAME_EN > Q_TRIMESTRE > YEAR_ONLY
# ---------------------------------------------------------------------------

def _casar_padrao_cronologico(
    valor: str,
    cardinalidade: int,
) -> Optional[PadraoCronologicoEnum]:
    """Tenta casar um valor único com padrões cronológicos · em ordem de prioridade."""
    v = valor.strip()
    if not v:
        return None

    if _RE_ISO_DATE.match(v):
        return PadraoCronologicoEnum.ISO_DATE

    if _RE_PT_BR_DATE.match(v):
        return PadraoCronologicoEnum.PT_BR_DATE

    if _RE_COMPACT_MONTHYEAR.match(v):
        return PadraoCronologicoEnum.COMPACT_MONTHYEAR

    if _RE_MONTH_PT.match(v):
        return PadraoCronologicoEnum.MONTH_NAME_PT

    if _RE_MONTH_EN.match(v):
        return PadraoCronologicoEnum.MONTH_NAME_EN

    if _RE_Q_TRIMESTRE.match(v):
        return PadraoCronologicoEnum.Q_TRIMESTRE

    # YEAR_ONLY: 4 dígitos em 1900-2099 E cardinalidade <= 30
    if re.match(r"^\d{4}$", v):
        yr = int(v)
        if 1900 <= yr <= 2099 and cardinalidade <= 30:
            return PadraoCronologicoEnum.YEAR_ONLY

    return None


def detectar_padrao_cronologico(
    series: pd.Series,
    cardinalidade: int,
    config: MotorConfig,
) -> Tuple[Optional[PadraoCronologicoEnum], float]:
    """
    Detecta padrão cronológico em coluna de strings.
    Amostra: max(1000, 10% do total) linhas não-nulas.
    Retorna (padrão, proporção_de_match) · padrão=None se abaixo de 50%.
    """
    nao_nulos = series.dropna().astype(str)
    if len(nao_nulos) == 0:
        return None, 0.0

    n_amostra = max(config.max_amostras_cronologico_base, int(len(nao_nulos) * 0.10))
    amostra = nao_nulos.head(n_amostra)

    # Contagem por padrão (prioridade já encapsulada em _casar_padrao_cronologico)
    contagens: Dict[PadraoCronologicoEnum, int] = {}
    for v in amostra:
        padrao = _casar_padrao_cronologico(v, cardinalidade)
        if padrao is not None:
            contagens[padrao] = contagens.get(padrao, 0) + 1

    if not contagens:
        return None, 0.0

    # Padrão vencedor = maior proporção · desempate pela prioridade canônica
    _PRIORIDADE = [
        PadraoCronologicoEnum.ISO_DATE,
        PadraoCronologicoEnum.PT_BR_DATE,
        PadraoCronologicoEnum.COMPACT_MONTHYEAR,
        PadraoCronologicoEnum.MONTH_NAME_PT,
        PadraoCronologicoEnum.MONTH_NAME_EN,
        PadraoCronologicoEnum.Q_TRIMESTRE,
        PadraoCronologicoEnum.YEAR_ONLY,
    ]

    melhor = max(contagens, key=lambda p: (contagens[p], -_PRIORIDADE.index(p)))
    proporcao = contagens[melhor] / len(amostra)
    return melhor, proporcao


# ---------------------------------------------------------------------------
# Inferência de tipo técnico e semântico
# ---------------------------------------------------------------------------

def _inferir_tipo_tecnico(series: pd.Series) -> TipoTecnicoEnum:
    """Infere tipo técnico a partir do dtype e conteúdo da série completa."""
    non_null = series.dropna()

    if pd.api.types.is_bool_dtype(series):
        return TipoTecnicoEnum.BOOL

    if pd.api.types.is_integer_dtype(series):
        return TipoTecnicoEnum.INT

    if pd.api.types.is_float_dtype(series):
        # D-008: float com apenas {0,1,NaN} → trata como BOOL no semântico mas
        # tipo_tecnico permanece FLOAT (informação técnica é preservada)
        return TipoTecnicoEnum.FLOAT

    if pd.api.types.is_datetime64_any_dtype(series):
        return TipoTecnicoEnum.DATETIME

    if len(non_null) == 0:
        return TipoTecnicoEnum.OBJECT

    # Object: inferência por conteúdo de string
    str_vals = non_null.astype(str).str.strip()
    total = len(str_vals)

    # Teste bool-string
    if all(v.lower() in _BOOL_STRINGS for v in str_vals):
        return TipoTecnicoEnum.BOOL

    # Teste numérico: tenta int depois float
    def _to_numeric(v: str) -> Optional[float]:
        cleaned = _CURRENCY_RE.sub("", v)
        # Trata separadores pt-BR (1.234,56 → 1234.56) e US (1,234.56 → 1234.56)
        if "," in cleaned and "." in cleaned:
            last_comma = cleaned.rfind(",")
            last_dot = cleaned.rfind(".")
            if last_comma > last_dot:
                cleaned = cleaned.replace(".", "").replace(",", ".")
            else:
                cleaned = cleaned.replace(",", "")
        elif "," in cleaned:
            after = cleaned.rsplit(",", 1)[-1]
            if len(after) == 3 and cleaned.count(",") == 1:
                cleaned = cleaned.replace(",", "")
            else:
                cleaned = cleaned.replace(",", ".")
        try:
            return float(cleaned)
        except (ValueError, TypeError):
            return None

    numeric_hits = sum(1 for v in str_vals if _to_numeric(v) is not None)
    numeric_ratio = numeric_hits / total

    if numeric_ratio >= 0.80:
        # Verifica se todos são inteiros (sem parte decimal relevante)
        vals = [_to_numeric(v) for v in str_vals]
        if all(v is not None and v == int(v) for v in vals if v is not None):
            return TipoTecnicoEnum.INT
        return TipoTecnicoEnum.FLOAT

    if numeric_ratio > 0.0:
        return TipoTecnicoEnum.MIXED

    return TipoTecnicoEnum.STRING


def _eh_booleano_disfarcado(series: pd.Series, tipo_tecnico: TipoTecnicoEnum) -> bool:
    """D-008: float64 {0,1,NaN} classificado como boolean."""
    if tipo_tecnico != TipoTecnicoEnum.FLOAT:
        return False
    non_null = series.dropna()
    if len(non_null) == 0:
        return False
    return bool(set(non_null.unique()).issubset(_BOOL_VALORES))


def _inferir_tipo_semantico(
    series: pd.Series,
    tipo_tecnico: TipoTecnicoEnum,
    cardinalidade: int,
    null_count: int,
    total_linhas: int,
) -> TipoSemanticoEnum:
    """Infere tipo semântico a partir do tipo técnico e características da série."""
    if tipo_tecnico == TipoTecnicoEnum.BOOL:
        return TipoSemanticoEnum.BOOLEAN

    if tipo_tecnico == TipoTecnicoEnum.DATETIME:
        return TipoSemanticoEnum.TEMPORAL

    if tipo_tecnico == TipoTecnicoEnum.MIXED:
        return TipoSemanticoEnum.MISTO

    if tipo_tecnico == TipoTecnicoEnum.OBJECT:
        return TipoSemanticoEnum.MISTO

    # Float: verifica boolean disfarçado (D-008)
    if tipo_tecnico == TipoTecnicoEnum.FLOAT:
        if _eh_booleano_disfarcado(series, tipo_tecnico):
            return TipoSemanticoEnum.BOOLEAN
        return TipoSemanticoEnum.NUMERIC

    # Int: sempre numeric no semântico (tipo_estrutural irá diferenciar)
    if tipo_tecnico == TipoTecnicoEnum.INT:
        return TipoSemanticoEnum.NUMERIC

    # String: categorico_baixa_card se cardinalidade < 50, senão textual
    if tipo_tecnico == TipoTecnicoEnum.STRING:
        if cardinalidade < 50:
            return TipoSemanticoEnum.CATEGORICO_BAIXA_CARD
        return TipoSemanticoEnum.TEXTUAL

    return TipoSemanticoEnum.MISTO


# ---------------------------------------------------------------------------
# Detecção de subtipo ID (D-103)
# ---------------------------------------------------------------------------

def _detectar_subtipo_id(
    series: pd.Series,
    tipo_tecnico: TipoTecnicoEnum,
    cardinalidade: int,
    null_count: int,
    total_linhas: int,
    config: MotorConfig,
) -> bool:
    """
    D-103 · heurística de subtipo ID.
    Condições obrigatórias:
      (1) tipo_tecnico em [int, string]
      (2) cardinalidade >= threshold * (total_linhas - null_count)
      (3) ao menos uma de: aritmética constante · comprimento fixo >= 8 · regex padrão
    """
    if tipo_tecnico not in (TipoTecnicoEnum.INT, TipoTecnicoEnum.STRING):
        return False

    nao_nulos = total_linhas - null_count
    if nao_nulos == 0:
        return False

    # Condição (2): cardinalidade suficientemente alta
    if cardinalidade < config.threshold_pct_id * nao_nulos:
        return False

    non_null = series.dropna()

    # Condição (3a): sequência aritmética (apenas int)
    if tipo_tecnico == TipoTecnicoEnum.INT:
        try:
            vals = sorted(non_null.astype(float).astype(int).tolist())
            if len(vals) >= 2:
                diffs = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
                if len(diffs) > 0:
                    diff_mais_comum = max(set(diffs), key=diffs.count)
                    pct_constante = diffs.count(diff_mais_comum) / len(diffs)
                    if pct_constante >= 0.80:
                        return True
        except (TypeError, ValueError):
            pass

    # Condição (3b): comprimento fixo >= 8 em 100% dos valores
    str_vals = non_null.astype(str).str.strip()
    # Remove pontuação comum em CPF/CNPJ para contagem de dígitos
    apenas_digitos = str_vals.str.replace(r"[.\-/]", "", regex=True)
    comprimentos = apenas_digitos.str.len()
    if len(comprimentos) > 0:
        min_len = comprimentos.min()
        max_len = comprimentos.max()
        if min_len == max_len and min_len >= 8:
            return True

    # Condição (3c): padrão regex de ID
    def _casa_padrao_id(v: str) -> bool:
        return bool(
            _RE_CPF.match(v)
            or _RE_CNPJ.match(v)
            or _RE_UUID.match(v)
            or _RE_MATRICULA.match(v)
        )

    pct_id = sum(1 for v in str_vals if _casa_padrao_id(v)) / len(str_vals)
    if pct_id >= 0.80:
        return True

    return False


# ---------------------------------------------------------------------------
# Classificação de tipo_estrutural (D-113 · D-133 · algoritmo C.2)
# ---------------------------------------------------------------------------

def _valores_em_conjunto_booleano(series: pd.Series) -> bool:
    """Verifica se todos os valores não-nulos estão em {0,1,0.0,1.0,"sim","não",...}."""
    non_null = series.dropna()
    if len(non_null) == 0:
        return False
    for v in non_null:
        if v not in _BOOL_VALORES and str(v).strip().lower() not in _BOOL_STRINGS:
            return False
    return True


def classificar_tipo_estrutural(
    col: pd.Series,
    meta_parcial: dict,
    total_linhas: int,
    config: MotorConfig,
) -> TipoEstruturalEnum:
    """
    Algoritmo canônico C.2 · ordem determinística · não alterar ordem.
    meta_parcial contém: null_count, tipo_semantico, tipo_tecnico,
    subtipo_id_detectado, cardinalidade, padrao_cronologico_detectado.
    """
    null_count: int = meta_parcial["null_count"]
    tipo_semantico: TipoSemanticoEnum = meta_parcial["tipo_semantico"]
    tipo_tecnico: TipoTecnicoEnum = meta_parcial["tipo_tecnico"]
    subtipo_id: bool = meta_parcial["subtipo_id_detectado"]
    cardinalidade: int = meta_parcial["cardinalidade"]
    padrao_cron: Optional[PadraoCronologicoEnum] = meta_parcial["padrao_cronologico_detectado"]

    nulos_pct = null_count / total_linhas if total_linhas > 0 else 0.0

    # 1. VAZIO_OU_AMBIGUO
    if nulos_pct > config.threshold_pct_quase_vazio:
        return TipoEstruturalEnum.VAZIO_OU_AMBIGUO
    if tipo_semantico == TipoSemanticoEnum.MISTO:
        return TipoEstruturalEnum.VAZIO_OU_AMBIGUO

    # 2. BOOLEANO
    if tipo_semantico == TipoSemanticoEnum.BOOLEAN:
        return TipoEstruturalEnum.BOOLEANO
    if cardinalidade == 2 and _valores_em_conjunto_booleano(col):
        return TipoEstruturalEnum.BOOLEANO

    # 3. TEMPORAL
    if tipo_semantico == TipoSemanticoEnum.TEMPORAL:
        return TipoEstruturalEnum.TEMPORAL
    if padrao_cron is not None:
        return TipoEstruturalEnum.TEMPORAL

    # 4. NUMERICO_CONTINUO vs CATEGORICO_ELEGIVEL
    if tipo_tecnico in (TipoTecnicoEnum.INT, TipoTecnicoEnum.FLOAT):
        if tipo_tecnico == TipoTecnicoEnum.FLOAT:
            return TipoEstruturalEnum.NUMERICO_CONTINUO
        # int
        if subtipo_id:
            return TipoEstruturalEnum.CATEGORICO_ELEGIVEL
        if cardinalidade > config.max_cardinalidade_categorico:
            return TipoEstruturalEnum.NUMERICO_CONTINUO
        return TipoEstruturalEnum.CATEGORICO_ELEGIVEL

    # 5. String → sempre CATEGORICO_ELEGIVEL
    return TipoEstruturalEnum.CATEGORICO_ELEGIVEL


# ---------------------------------------------------------------------------
# Normalização do DataFrame
# ---------------------------------------------------------------------------

def _is_null_like(val: object) -> bool:
    if val is None:
        return True
    try:
        if pd.isna(val):  # type: ignore[arg-type]
            return True
    except (TypeError, ValueError):
        pass
    return str(val).strip().lower() in _NULL_STRINGS


def _normalizar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """Substitui null-strings por NaN · nunca remove linhas."""
    result = df.copy()
    for col in result.columns:
        result[col] = [np.nan if _is_null_like(v) else v for v in result[col]]
    return result


def _rename_unnamed(df: pd.DataFrame, ajustes: list) -> pd.DataFrame:
    new_cols: list[str] = []
    counter = 0
    renamed_count = 0
    for col in df.columns:
        s = str(col).strip()
        if s == "" or s == "nan" or s.startswith("Unnamed:"):
            counter += 1
            new_cols.append(f"Coluna_{counter}")
            renamed_count += 1
        else:
            new_cols.append(s)
    if renamed_count:
        ajustes.append(AjusteMotor(
            tipo_ajuste="COLUNA_RENOMEADA",
            linhas_afetadas=0,
            descricao=f"{renamed_count} coluna(s) sem nome renomeada(s) para Coluna_N.",
        ))
    df = df.copy()
    df.columns = new_cols  # type: ignore[assignment]
    return df


def _deduplicar_colunas(df: pd.DataFrame, ajustes: list) -> pd.DataFrame:
    seen: Dict[str, int] = {}
    new_cols: list[str] = []
    dupes = 0
    for col in df.columns:
        if col in seen:
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")
            dupes += 1
        else:
            seen[col] = 1
            new_cols.append(col)
    if dupes:
        ajustes.append(AjusteMotor(
            tipo_ajuste="COLUNA_DEDUPLICADA",
            linhas_afetadas=0,
            descricao=f"{dupes} coluna(s) duplicada(s) renomeada(s) com sufixo _N.",
        ))
    df = df.copy()
    df.columns = new_cols  # type: ignore[assignment]
    return df


# ---------------------------------------------------------------------------
# Leitura do DataFrame a partir de arquivo_bytes
# ---------------------------------------------------------------------------

def _ler_df_de_bytes(info, ajustes: list) -> pd.DataFrame:
    """Lê DataFrame completo de arquivo_bytes preservado pelo motor_upload."""
    buf = BytesIO(info.arquivo_bytes)
    if info.formato in ("csv", "tsv"):
        df = pd.read_csv(
            buf,
            sep=info.separador_csv or ",",
            encoding=info.encoding_detectado or "utf-8",
            skip_blank_lines=True,
        )
    else:
        aba = info.aba_selecionada if info.aba_selecionada else None
        df = pd.read_excel(buf, sheet_name=aba, engine="openpyxl")
    return df


# ---------------------------------------------------------------------------
# Construção de ColumnMeta por coluna
# ---------------------------------------------------------------------------

def _build_column_meta(
    col_name: str,
    ordem: int,
    series: pd.Series,
    total_linhas: int,
    config: MotorConfig,
    warnings: list,
) -> ColumnMeta:
    """Computa todos os campos de ColumnMeta · D-133 · sempre sobre coluna completa."""

    # null_count (inclui null-strings já normalizados)
    null_count = int(series.isna().sum())
    cardinalidade = int(series.nunique(dropna=True))
    nao_nulos = total_linhas - null_count

    # Tipo técnico
    tipo_tecnico = _inferir_tipo_tecnico(series)

    # Tipo semântico (inclui D-008 boolean disfarçado)
    tipo_semantico = _inferir_tipo_semantico(
        series, tipo_tecnico, cardinalidade, null_count, total_linhas
    )

    # Emite W-B01 para boolean disfarçado (D-008)
    if _eh_booleano_disfarcado(series, tipo_tecnico):
        warnings.append(_w(
            "W-B01",
            CategoriaWarning.INFORMATIVO,
            f"Coluna '{col_name}': float64 com valores em {{0,1,NaN}} classificada como BOOLEANO. "
            f"Confirme se a intenção analítica é flag binário ou medida numérica.",
            coluna=col_name,
        ))

    # Detecção de padrão cronológico (D-026)
    padrao_cronologico: Optional[PadraoCronologicoEnum] = None
    if tipo_tecnico in (TipoTecnicoEnum.STRING, TipoTecnicoEnum.OBJECT):
        padrao_cand, pct = detectar_padrao_cronologico(series, cardinalidade, config)
        if pct >= config.threshold_pct_cronologico:
            padrao_cronologico = padrao_cand
        elif pct >= config.threshold_pct_cronologico_parcial and padrao_cand is not None:
            warnings.append(_w(
                "W-B-TEMPORAL-PARCIAL",
                CategoriaWarning.INFORMATIVO,
                f"Coluna '{col_name}': padrão cronológico '{padrao_cand.value}' detectado "
                f"em {pct:.0%} dos valores (abaixo do threshold de 80%).",
                coluna=col_name,
                padrao=padrao_cand.value,
                proporcao=round(pct, 3),
            ))
    elif tipo_tecnico == TipoTecnicoEnum.INT and cardinalidade <= 30:
        # YEAR_ONLY: coluna inteira 4 dígitos em 1900-2099 (comum após round-trip Excel)
        non_null_int = series.dropna()
        if len(non_null_int) > 0:
            try:
                int_vals = non_null_int.astype(int)
                if bool(int_vals.between(1900, 2099).all()):
                    padrao_cronologico = PadraoCronologicoEnum.YEAR_ONLY
            except (TypeError, ValueError):
                pass
    elif tipo_tecnico == TipoTecnicoEnum.DATETIME:
        # datetime nativo é TEMPORAL sem precisar do reconhecedor
        padrao_cronologico = PadraoCronologicoEnum.ISO_DATE  # representação canônica

    # Detecção de subtipo ID (D-103)
    subtipo_id = _detectar_subtipo_id(
        series, tipo_tecnico, cardinalidade, null_count, total_linhas, config
    )
    if subtipo_id:
        warnings.append(_w(
            "W-B-ID-DETECTADO",
            CategoriaWarning.INFORMATIVO,
            f"Coluna '{col_name}': subtipo ID detectado (alta cardinalidade + padrão ID).",
            coluna=col_name,
            cardinalidade=cardinalidade,
            total_nao_nulos=nao_nulos,
        ))

    # Emite W-B-MISTO
    if tipo_semantico == TipoSemanticoEnum.MISTO:
        warnings.append(_w(
            "W-B-MISTO",
            CategoriaWarning.ALERTA_ESTRUTURAL,
            f"Coluna '{col_name}': tipos técnicos divergentes detectados — classificada como VAZIO_OU_AMBIGUO.",
            coluna=col_name,
        ))

    # Emite W-B-QUASE-VAZIO
    nulos_pct = null_count / total_linhas if total_linhas > 0 else 0.0
    if nulos_pct > config.threshold_pct_quase_vazio:
        warnings.append(_w(
            "W-B-QUASE-VAZIO",
            CategoriaWarning.ALERTA_ESTRUTURAL_LEVE,
            f"Coluna '{col_name}': {nulos_pct:.0%} de nulos — classificada como VAZIO_OU_AMBIGUO.",
            coluna=col_name,
            pct_nulos=round(nulos_pct, 3),
        ))

    # meta_parcial para o algoritmo C.2
    meta_parcial = {
        "null_count": null_count,
        "tipo_semantico": tipo_semantico,
        "tipo_tecnico": tipo_tecnico,
        "subtipo_id_detectado": subtipo_id,
        "cardinalidade": cardinalidade,
        "padrao_cronologico_detectado": padrao_cronologico,
    }

    tipo_estrutural = classificar_tipo_estrutural(series, meta_parcial, total_linhas, config)

    # eh_candidato_categorico: CATEGORICO_ELEGIVEL ou BOOLEANO ou TEMPORAL
    eh_candidato = tipo_estrutural in (
        TipoEstruturalEnum.CATEGORICO_ELEGIVEL,
        TipoEstruturalEnum.BOOLEANO,
        TipoEstruturalEnum.TEMPORAL,
    )

    return ColumnMeta(
        nome=col_name,
        tipo_tecnico=tipo_tecnico,
        tipo_semantico=tipo_semantico,
        tipo_estrutural=tipo_estrutural,
        subtipo_id_detectado=subtipo_id,
        null_count=null_count,
        cardinalidade=cardinalidade,
        eh_candidato_categorico=eh_candidato,
        padrao_cronologico_detectado=padrao_cronologico,
        ordem_insercao=ordem,
    )


# ---------------------------------------------------------------------------
# Detecção de bloqueios de motor_base
# ---------------------------------------------------------------------------

def _detectar_bloqueios(
    df: pd.DataFrame,
    column_meta: Dict[str, ColumnMeta],
    total_linhas: int,
    config: MotorConfig,
) -> List[BloqueioOperacional]:
    """Emite BloqueioOperacional de motor_base · MBO · C.D4."""
    bloqueios: List[BloqueioOperacional] = []

    # B-B-BASE-MUITO-GRANDE: limite absoluto sem escape
    if total_linhas > config.limite_linhas_bloqueio:
        bloqueios.append(_bloqueio(
            "B-B-BASE-MUITO-GRANDE",
            f"Base com {total_linhas:,} linhas excede o limite absoluto de "
            f"{config.limite_linhas_bloqueio:,} linhas. Operação não pode prosseguir.",
            escapavel=False,
            total_linhas=total_linhas,
            limite=config.limite_linhas_bloqueio,
        ))

    # B-CARD-EXCESSIVA: coluna string com cardinalidade >= 98% das linhas sem ser ID
    # Indica coluna de texto livre sem valor analítico como categoria
    for col_name, meta in column_meta.items():
        if (
            meta.tipo_tecnico == TipoTecnicoEnum.STRING
            and not meta.subtipo_id_detectado
            and meta.null_count < total_linhas
        ):
            nao_nulos = total_linhas - meta.null_count
            if nao_nulos > 0 and meta.cardinalidade >= 0.98 * nao_nulos and meta.cardinalidade > 50:
                bloqueios.append(_bloqueio(
                    "B-CARD-EXCESSIVA",
                    f"Coluna '{col_name}' possui {meta.cardinalidade} valores únicos em "
                    f"{nao_nulos} registros não-nulos ({meta.cardinalidade/nao_nulos:.0%}). "
                    f"Cardinalidade excessiva para uso analítico como categoria.",
                    escapavel=True,
                    coluna=col_name,
                    cardinalidade=meta.cardinalidade,
                    total_nao_nulos=nao_nulos,
                    proporcao=round(meta.cardinalidade / nao_nulos, 3),
                ))

    return bloqueios


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def processar_base(
    upload_result: UploadResult,
    config: Optional[MotorConfig] = None,
) -> MotorResult:
    """
    Processa UploadResult e produz MotorResult com column_meta completa.

    Lê o DataFrame completo de arquivo_bytes (D-007) · computa tipo_estrutural,
    subtipo_id e padrao_cronologico para TODA coluna (D-133) · emite warnings
    e BloqueioOperacional conforme cabível (C.2 · C.D4).

    Args:
        upload_result: Resultado do motor_upload com arquivo_bytes preenchido.
        config: Configuração do motor · None = defaults da MotorConfig.

    Returns:
        MotorResult com df, column_meta, warnings e bloqueios.
    """
    if config is None:
        config = MotorConfig()

    warnings: List[WarningEstrutural] = []
    ajustes: List[AjusteMotor] = []

    # ---- Leitura do DataFrame a partir de arquivo_bytes ---------------------
    if upload_result.modo_upload == "SIMPLES":
        if upload_result.arquivo_unico is None:
            raise ValueError("UploadResult SIMPLES sem arquivo_unico preenchido.")
        info_lista = [upload_result.arquivo_unico]
    else:
        if upload_result.arquivos_dual is None or len(upload_result.arquivos_dual) != 2:
            raise ValueError("UploadResult DUAL requer arquivos_dual com 2 entradas.")
        info_lista = upload_result.arquivos_dual

    dfs: List[pd.DataFrame] = []
    origem_comparado_map: Optional[Dict[int, Literal["origem", "comparado"]]] = None

    for info in info_lista:
        df_part = _ler_df_de_bytes(info, ajustes)
        df_part = _normalizar_nulos(df_part)
        df_part = _rename_unnamed(df_part, ajustes)
        df_part = _deduplicar_colunas(df_part, ajustes)
        dfs.append(df_part)

    if upload_result.modo_upload == "SIMPLES":
        df = dfs[0]
        total_originais = len(df)
    else:
        # DUAL: concatena e constrói mapa de origem/comparado
        len_origem = len(dfs[0])
        len_comparado = len(dfs[1])
        df = pd.concat(dfs, ignore_index=True)
        origem_comparado_map = {}
        for i in range(len_origem):
            origem_comparado_map[i] = "origem"
        for i in range(len_comparado):
            origem_comparado_map[len_origem + i] = "comparado"
        total_originais = len_origem + len_comparado
        ajustes.append(AjusteMotor(
            tipo_ajuste="DUAL_CONCATENADO",
            linhas_afetadas=total_originais,
            descricao=f"Bases DUAL concatenadas: {len_origem} linhas (origem) + {len_comparado} linhas (comparado).",
        ))

    total_processadas = len(df)

    # ---- Verificação de tamanho: warning de base grande --------------------
    if total_processadas > config.limite_linhas_aviso:
        warnings.append(_w(
            "W-B-BASE-GRANDE",
            CategoriaWarning.ALERTA_ESTRUTURAL_LEVE,
            f"Base com {total_processadas:,} linhas acima do limite saudável de "
            f"{config.limite_linhas_aviso:,}. Processamento pode ser mais lento.",
            total_linhas=total_processadas,
        ))

    # ---- Construção de column_meta por coluna (D-133: sempre toda coluna) --
    column_meta: Dict[str, ColumnMeta] = {}
    for ordem, col_name in enumerate(df.columns):
        meta = _build_column_meta(
            col_name=str(col_name),
            ordem=ordem,
            series=df[col_name],
            total_linhas=total_processadas,
            config=config,
            warnings=warnings,
        )
        column_meta[str(col_name)] = meta

    # ---- Detecção de bloqueios (MBO · C.D4) --------------------------------
    bloqueios = _detectar_bloqueios(df, column_meta, total_processadas, config)

    return MotorResult(
        df=df,
        column_meta=column_meta,
        modo_upload=upload_result.modo_upload,
        origem_comparado_map=origem_comparado_map,
        total_linhas_originais=total_originais,
        total_linhas_processadas=total_processadas,
        timestamp_processamento=datetime.now(),
        warnings=warnings,
        bloqueios=bloqueios,
    )
