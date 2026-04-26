"""
t_eixo.py — Eixo sequencial ordenado · T-EIXO · D-061 · E.1
3 tipos canônicos: TEMPORAL · ORDINAL · MANUAL
Herda reconhecedor cronológico de D-026 · zero reimplementação.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Literal, Optional, Tuple

import pandas as pd
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).parent.parent))

from contratos import CategoriaWarning, PadraoCronologicoEnum, WarningEstrutural
from utils.reconhecedor_cronologico import (
    detectar_padrao_em_lista,
    ordenar_cronologicamente,
)

TipoEixo = Literal["TEMPORAL", "ORDINAL", "MANUAL"]

_RE_PREFIXO_ORDINAL = re.compile(r"^(\d+)[^\d]|^[^\d]*(\d+)$")


class IntervaloEixo(BaseModel):
    de: str = Field(..., description="Ponto inicial · string no vocabulário do eixo")
    ate: str = Field(..., description="Ponto final")


class ConfigEixo(BaseModel):
    coluna_eixo: str = Field(..., description="Coluna que representa o eixo sequencial")
    tipo_declarado: TipoEixo = Field(
        ..., description="Declaração final do usuário após default proposto pelo motor"
    )
    ordem_aplicada: List[str] = Field(
        ..., description="Ordem final dos pontos · motor propõe · usuário confirma/edita"
    )
    intervalo_declarado: IntervaloEixo = Field(
        ..., description="De/Até declarado · preservado para auditoria"
    )


class EixoResult(BaseModel):
    tipo_aplicado: TipoEixo
    tipo_inferido_pelo_motor: TipoEixo
    ordem_aplicada: List[str]
    intervalo_declarado: IntervaloEixo
    intervalo_efetivo: IntervaloEixo
    pontos_no_intervalo: List[str]
    pontos_ausentes_detectados: List[str]
    deteccao_de_lacuna_disponivel: bool
    densidade_de_lacuna: Optional[float]
    warnings_gerados: List[WarningEstrutural]


def _extrair_prefixo_numerico(valor: str) -> Optional[int]:
    """Extrai prefixo ou sufixo numérico de um rótulo ordinal."""
    m = re.match(r"^(\d+)", valor.strip())
    if m:
        return int(m.group(1))
    m2 = re.search(r"(\d+)$", valor.strip())
    if m2:
        return int(m2.group(1))
    return None


def inferir_tipo_eixo(
    valores_unicos: List[str],
    threshold: float = 0.80,
) -> Tuple[TipoEixo, float]:
    """
    Detecta tipo do eixo pela heurística de prioridade TEMPORAL > ORDINAL > MANUAL.
    Retorna (tipo_inferido, confiança_0_a_1).
    """
    if not valores_unicos:
        return "MANUAL", 0.0

    n = len(valores_unicos)
    cardinalidade = n

    # 1. TEMPORAL
    padrao, proporcao = detectar_padrao_em_lista(valores_unicos, cardinalidade)
    if padrao is not None and proporcao >= threshold:
        return "TEMPORAL", proporcao

    # 2. ORDINAL com prefixo numérico
    com_prefixo = sum(
        1 for v in valores_unicos if _extrair_prefixo_numerico(v) is not None
    )
    proporcao_ordinal = com_prefixo / n
    if proporcao_ordinal >= threshold:
        return "ORDINAL", proporcao_ordinal

    return "MANUAL", 0.0


def _construir_sequencia_esperada_temporal(
    pontos: List[str],
    padrao: PadraoCronologicoEnum,
) -> Optional[List[str]]:
    """Para padrões de mês, gera a sequência completa entre o primeiro e último ponto."""
    # Para MONTH_NAME_PT: constrói sequência de meses pt-BR
    if padrao == PadraoCronologicoEnum.MONTH_NAME_PT:
        meses_ordem = [
            "jan", "fev", "mar", "abr", "mai", "jun",
            "jul", "ago", "set", "out", "nov", "dez",
        ]
        meses_presentes = []
        for p in pontos:
            partes = re.split(r"[/\-\s]", p.lower().strip())
            nome = partes[0][:3] if partes else ""
            if nome in meses_ordem:
                meses_presentes.append(nome)
        if len(meses_presentes) < 2:
            return None
        i_inicio = meses_ordem.index(meses_presentes[0])
        i_fim = meses_ordem.index(meses_presentes[-1])
        return meses_ordem[i_inicio: i_fim + 1]
    return None


def _detectar_lacunas_ordinal(pontos: List[str]) -> List[str]:
    """Detecta lacunas em sequência ordinal com prefixo numérico."""
    prefixos = []
    for p in pontos:
        n = _extrair_prefixo_numerico(p)
        if n is not None:
            prefixos.append(n)

    if len(prefixos) < 2:
        return []

    minimo = min(prefixos)
    maximo = max(prefixos)
    esperados = set(range(minimo, maximo + 1))
    presentes = set(prefixos)
    ausentes_nums = sorted(esperados - presentes)
    return [str(n) for n in ausentes_nums]


def aplicar_eixo(
    df: pd.DataFrame,
    config: ConfigEixo,
    nome_visao: str,
    threshold_lacuna_massiva: float = 0.30,
) -> Tuple[pd.DataFrame, EixoResult]:
    """
    Aplica tipo declarado + ordem + intervalo ao DataFrame.
    Adiciona coluna auxiliar `_ordem_eixo` (int64 posicional, -1 para fora do intervalo).
    Retorna (df_enriquecido, EixoResult).
    """
    warnings: List[WarningEstrutural] = []
    coluna = config.coluna_eixo

    valores_na_base = df[coluna].dropna().astype(str).unique().tolist()
    tipo_inferido, _ = inferir_tipo_eixo(sorted(valores_na_base))

    # Valida bloqueio De > Até
    ordem = config.ordem_aplicada
    if config.intervalo_declarado.de not in ordem or config.intervalo_declarado.ate not in ordem:
        idx_de = -1
        idx_ate = len(ordem)
    else:
        idx_de = ordem.index(config.intervalo_declarado.de)
        idx_ate = ordem.index(config.intervalo_declarado.ate)

    if idx_de > idx_ate:
        raise ValueError(
            f"B-V{nome_visao}-INTERVALO-INVALIDO: "
            f"'{config.intervalo_declarado.de}' > '{config.intervalo_declarado.ate}' na ordem do eixo."
        )

    # Pontos no intervalo
    pontos_intervalo = ordem[idx_de: idx_ate + 1]

    # Intervalo efetivo: ajusta se De/Até não estão na base
    primeiro_na_base = next((p for p in pontos_intervalo if p in valores_na_base), None)
    ultimo_na_base = next((p for p in reversed(pontos_intervalo) if p in valores_na_base), None)

    if primeiro_na_base and primeiro_na_base != config.intervalo_declarado.de:
        warnings.append(WarningEstrutural(
            codigo=f"W-V{nome_visao}-INTERVALO-AJUSTE-INICIO",
            categoria=CategoriaWarning.AJUSTE_LEVE,
            microcopy=f"Ponto inicial '{config.intervalo_declarado.de}' não encontrado na base. "
                      f"Ajustado para '{primeiro_na_base}'.",
            contexto={"declarado": config.intervalo_declarado.de, "efetivo": primeiro_na_base},
        ))
    if ultimo_na_base and ultimo_na_base != config.intervalo_declarado.ate:
        warnings.append(WarningEstrutural(
            codigo=f"W-V{nome_visao}-INTERVALO-AJUSTE-FIM",
            categoria=CategoriaWarning.AJUSTE_LEVE,
            microcopy=f"Ponto final '{config.intervalo_declarado.ate}' não encontrado na base. "
                      f"Ajustado para '{ultimo_na_base}'.",
            contexto={"declarado": config.intervalo_declarado.ate, "efetivo": ultimo_na_base},
        ))

    intervalo_efetivo = IntervaloEixo(
        de=primeiro_na_base or config.intervalo_declarado.de,
        ate=ultimo_na_base or config.intervalo_declarado.ate,
    )

    # Detecção de lacunas
    # Valores efetivamente presentes no df dentro do intervalo
    valores_presentes_no_intervalo = set(str(v) for v in df[coluna].dropna() if str(v) in set(pontos_intervalo))
    deteccao_disponivel = False
    ausentes: List[str] = []
    densidade: Optional[float] = None

    if config.tipo_declarado == "TEMPORAL":
        deteccao_disponivel = True
        # Tenta construir sequência esperada para padrão de mês
        cardinalidade = len(valores_na_base)
        padrao, _ = detectar_padrao_em_lista(valores_na_base, cardinalidade)
        if padrao:
            seq_esperada = _construir_sequencia_esperada_temporal(pontos_intervalo, padrao)
            if seq_esperada:
                presentes_set = {p.lower()[:3] for p in valores_presentes_no_intervalo}
                ausentes = [m for m in seq_esperada if m not in presentes_set]

    elif config.tipo_declarado == "ORDINAL":
        # Verifica se tem prefixo numérico nos valores da base no intervalo
        tem_prefixo = any(_extrair_prefixo_numerico(p) is not None for p in valores_presentes_no_intervalo)
        if tem_prefixo:
            deteccao_disponivel = True
            # Detecta lacunas: prefixos esperados vs presentes na base
            ausentes = _detectar_lacunas_ordinal(list(valores_presentes_no_intervalo))

    if deteccao_disponivel and ausentes:
        densidade = len(ausentes) / max(len(pontos_intervalo) + len(ausentes), 1)
        warnings.append(WarningEstrutural(
            codigo=f"W-V{nome_visao}-EIXO-LACUNA",
            categoria=CategoriaWarning.INFORMATIVO,
            microcopy=f"Lacunas detectadas no eixo: {ausentes}.",
            contexto={"pontos_ausentes": ausentes, "densidade": round(densidade, 4)},
        ))
        if densidade > threshold_lacuna_massiva:
            warnings.append(WarningEstrutural(
                codigo=f"W-V{nome_visao}-EIXO-LACUNA-MASSIVA",
                categoria=CategoriaWarning.ALERTA_ESTRUTURAL_LEVE,
                microcopy=f"Lacuna massiva no eixo: {densidade:.1%} dos pontos esperados ausentes.",
                contexto={"densidade": round(densidade, 4), "threshold": threshold_lacuna_massiva},
            ))

    # Monta mapa de ordem
    ordem_map = {p: i + 1 for i, p in enumerate(pontos_intervalo)}
    df_resultado = df.copy()
    df_resultado["_ordem_eixo"] = (
        df_resultado[coluna].astype(str).map(ordem_map).fillna(-1).astype("int64")
    )

    return df_resultado, EixoResult(
        tipo_aplicado=config.tipo_declarado,
        tipo_inferido_pelo_motor=tipo_inferido,
        ordem_aplicada=config.ordem_aplicada,
        intervalo_declarado=config.intervalo_declarado,
        intervalo_efetivo=intervalo_efetivo,
        pontos_no_intervalo=pontos_intervalo,
        pontos_ausentes_detectados=ausentes,
        deteccao_de_lacuna_disponivel=deteccao_disponivel,
        densidade_de_lacuna=densidade,
        warnings_gerados=warnings,
    )
