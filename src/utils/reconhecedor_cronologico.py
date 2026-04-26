"""
reconhecedor_cronologico.py — Reconhecedor canônico de padrões cronológicos · D-026
Módulo único consumido por motor_base · T-AGRUPA · T-EIXO · herança zero-duplicação.

7 padrões reconhecidos (pt-BR e pt-EN):
  ISO_DATE · PT_BR_DATE · MONTH_NAME_PT · MONTH_NAME_EN ·
  COMPACT_MONTHYEAR · YEAR_ONLY · Q_TRIMESTRE

Prioridade em ambiguidade:
  ISO_DATE > PT_BR_DATE > COMPACT_MONTHYEAR > MONTH_NAME_PT
  > MONTH_NAME_EN > Q_TRIMESTRE > YEAR_ONLY
"""
from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

from contratos import PadraoCronologicoEnum


# ---------------------------------------------------------------------------
# Regex canônicos
# ---------------------------------------------------------------------------

_RE_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}.*)?$")
_RE_PT_BR_DATE = re.compile(r"^\d{1,2}[/-]\d{1,2}[/-]\d{4}$")
_RE_COMPACT_MONTHYEAR = re.compile(r"^\d{4}-\d{2}$|^\d{6}$|^\d{2}/\d{4}$")
_RE_Q_TRIMESTRE = re.compile(
    r"^[QqTt]\d(\s+\d{2,4})?$|^\d\s*[°ºo°]*\s*[Tt]rim", re.IGNORECASE
)
_RE_MONTH_PT = re.compile(
    r"^(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez"
    r"|janeiro|fevereiro|mar[cç]o|abril|maio|junho|julho|agosto"
    r"|setembro|outubro|novembro|dezembro)"
    r"([/-]|\s+)?\d{0,4}$",
    re.IGNORECASE,
)
_RE_MONTH_EN = re.compile(
    r"^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec"
    r"|january|february|march|april|june|july|august"
    r"|september|october|november|december)"
    r"([/-]|\s+)?\d{0,4}$",
    re.IGNORECASE,
)

_PRIORIDADE: List[PadraoCronologicoEnum] = [
    PadraoCronologicoEnum.ISO_DATE,
    PadraoCronologicoEnum.PT_BR_DATE,
    PadraoCronologicoEnum.COMPACT_MONTHYEAR,
    PadraoCronologicoEnum.MONTH_NAME_PT,
    PadraoCronologicoEnum.MONTH_NAME_EN,
    PadraoCronologicoEnum.Q_TRIMESTRE,
    PadraoCronologicoEnum.YEAR_ONLY,
]


def casar_padrao_cronologico(
    valor: str,
    cardinalidade: int,
) -> Optional[PadraoCronologicoEnum]:
    """Testa um valor único contra os 7 padrões em ordem de prioridade."""
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

    if re.match(r"^\d{4}$", v):
        yr = int(v)
        if 1900 <= yr <= 2099 and cardinalidade <= 30:
            return PadraoCronologicoEnum.YEAR_ONLY

    return None


def detectar_padrao_em_lista(
    valores: List[str],
    cardinalidade: int,
    threshold_forte: float = 0.80,
    threshold_parcial: float = 0.50,
) -> Tuple[Optional[PadraoCronologicoEnum], float]:
    """
    Detecta padrão cronológico em lista de strings (não-nulas já filtradas).
    Retorna (padrão_dominante, proporção) ou (None, 0.0).

    threshold_forte: proporção mínima para confirmar o padrão (default 80%).
    threshold_parcial: proporção mínima para retornar com flag parcial (não aplicado aqui —
      caller decide o que fazer com a proporção retornada).
    """
    if not valores:
        return None, 0.0

    contagens: Dict[PadraoCronologicoEnum, int] = {}
    for v in valores:
        padrao = casar_padrao_cronologico(str(v), cardinalidade)
        if padrao is not None:
            contagens[padrao] = contagens.get(padrao, 0) + 1

    if not contagens:
        return None, 0.0

    melhor = max(contagens, key=lambda p: (contagens[p], -_PRIORIDADE.index(p)))
    proporcao = contagens[melhor] / len(valores)
    return melhor, proporcao


# ---------------------------------------------------------------------------
# Ordenação cronológica de valores (consumida por T-AGRUPA e T-EIXO)
# ---------------------------------------------------------------------------

# Tabela de meses pt-BR
_MESES_PT_ORDEM: Dict[str, int] = {
    "jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
    "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12,
    "janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3, "abril": 4,
    "maio": 5, "junho": 6, "julho": 7, "agosto": 8, "setembro": 9,
    "outubro": 10, "novembro": 11, "dezembro": 12,
}

# Tabela de meses en
_MESES_EN_ORDEM: Dict[str, int] = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    "january": 1, "february": 2, "march": 3, "april": 4, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11,
    "december": 12,
}

_RE_MES_ANO = re.compile(
    r"^([a-záéíóúâêîôûãõàèìòùç]+)[/\-\s](\d{2,4})$",
    re.IGNORECASE,
)
_RE_ANO_MES = re.compile(r"^(\d{4})[/\-](\d{2})$")
_RE_TRIMESTRE = re.compile(
    r"^[QqTt](\d)[\s/\-]*(\d{2,4})?$|^(\d)[°ºo]*\s*[Tt]rim[\s/\-]*(\d{2,4})?$",
    re.IGNORECASE,
)


def _chave_ordem_cronologica(
    valor: str,
    padrao: PadraoCronologicoEnum,
) -> tuple:
    """Gera chave de ordenação para um valor dado o padrão detectado."""
    v = str(valor).strip()

    if padrao == PadraoCronologicoEnum.ISO_DATE:
        return (v,)

    if padrao == PadraoCronologicoEnum.PT_BR_DATE:
        partes = re.split(r"[/\-]", v)
        if len(partes) == 3:
            try:
                return (int(partes[2]), int(partes[1]), int(partes[0]))
            except ValueError:
                pass
        return (v,)

    if padrao in (PadraoCronologicoEnum.MONTH_NAME_PT, PadraoCronologicoEnum.MONTH_NAME_EN):
        tabela = (_MESES_PT_ORDEM if padrao == PadraoCronologicoEnum.MONTH_NAME_PT
                  else _MESES_EN_ORDEM)
        m = _RE_MES_ANO.match(v)
        if m:
            nome_mes = m.group(1).lower()
            ano_str = m.group(2)
            ano = int(ano_str) if len(ano_str) == 4 else 2000 + int(ano_str)
            mes_num = tabela.get(nome_mes, 0)
            return (ano, mes_num)
        # Apenas nome do mês sem ano
        nome_mes = v.lower().split("/")[0].split("-")[0].strip()
        mes_num = tabela.get(nome_mes, 0)
        return (0, mes_num)

    if padrao == PadraoCronologicoEnum.COMPACT_MONTHYEAR:
        m2 = _RE_ANO_MES.match(v)
        if m2:
            return (int(m2.group(1)), int(m2.group(2)))
        # yyyymm
        if re.match(r"^\d{6}$", v):
            return (int(v[:4]), int(v[4:]))
        # mm/yyyy
        m3 = re.match(r"^(\d{2})/(\d{4})$", v)
        if m3:
            return (int(m3.group(2)), int(m3.group(1)))
        return (v,)

    if padrao == PadraoCronologicoEnum.YEAR_ONLY:
        try:
            return (int(v),)
        except ValueError:
            return (v,)

    if padrao == PadraoCronologicoEnum.Q_TRIMESTRE:
        mt = _RE_TRIMESTRE.match(v)
        if mt:
            # Grupos: Q(\d) com ano opcional
            trimestre = int(mt.group(1) or mt.group(3) or 0)
            ano_str = mt.group(2) or mt.group(4) or "0"
            ano = int(ano_str) if len(ano_str) == 4 else (2000 + int(ano_str) if ano_str != "0" else 0)
            return (ano, trimestre)
        return (v,)

    return (v,)


def ordenar_cronologicamente(
    valores: List[str],
    padrao: PadraoCronologicoEnum,
) -> List[str]:
    """
    Ordena lista de strings de acordo com o padrão cronológico detectado.
    Valores não reconhecíveis ficam ao final em ordem lexicográfica.
    Determinismo C.1: desempate por valor original (lexicográfico).
    """
    def chave(v: str) -> tuple:
        k = _chave_ordem_cronologica(v, padrao)
        return (0, k, v)  # 0 = reconhecido · 1 = não reconhecido

    return sorted(valores, key=chave)
