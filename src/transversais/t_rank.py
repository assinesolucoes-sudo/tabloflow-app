"""
t_rank.py — Ranking determinístico com desempate configurável · T-RANK · D-041 · E.2
Default 3 níveis · adaptações V7/V9/V6 com 4 níveis · enum escopo 3 valores · D-137.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List, Literal, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).parent.parent))

from contratos import CategoriaWarning, WarningEstrutural
from utils.normalizacao_texto import normalizar_texto

EscopoRank = Literal["global", "intra_grupo", "cross_elementos_dentro_do_agrupador"]
DirecaoRank = Literal["decrescente", "crescente"]
TransformacaoRank = Literal["abs"]
TipoDesempate = Literal[
    "coluna_valor",
    "concatenacao_agrupadores",
    "coluna_texto_alfabetico",
    "ordem_de_insercao",
]
MetodoEmpate = Literal["standard", "min", "dense"]


class CriterioOrdenacao(BaseModel):
    coluna_ou_expressao: str
    direcao: DirecaoRank = "decrescente"
    transformacao: Optional[TransformacaoRank] = None


class CriterioDesempate(BaseModel):
    tipo: TipoDesempate
    parametros: Dict = Field(default_factory=dict)


class ConfigRank(BaseModel):
    escopo: EscopoRank = Field("global", description="D-137 · 3 valores canônicos")
    criterio_primario: CriterioOrdenacao
    regras_desempate: List[CriterioDesempate] = Field(default_factory=list)
    coluna_grupo: Optional[str] = Field(None, description="Obrigatório quando escopo != global")
    tolerancia_float: float = Field(1e-9, description="D-041 · tolerância absoluta para empate")
    metodo_rank_para_empate_preservado: MetodoEmpate = Field(
        "standard",
        description="V9 usa 'min' para preservar empate como fato analítico · D-096",
    )
    agrupadores: List[str] = Field(default_factory=list, description="Para nível de desempate concatenação")


class RankResult(BaseModel):
    coluna_rank_adicionada: str
    empates_detectados: int
    regras_desempate_acionadas: Dict[int, int]
    warnings_gerados: List[WarningEstrutural]


def _aplicar_transformacao(series: pd.Series, trans: Optional[str]) -> pd.Series:
    if trans == "abs":
        return series.abs()
    return series


def _construir_chave_sort(
    df: pd.DataFrame,
    config: ConfigRank,
) -> pd.DataFrame:
    """
    Constrói df de chaves de ordenação para determinar rank.
    Retorna df auxiliar com colunas _k0, _k1, _k2, ... e _orig_idx.
    """
    df_sort = df.copy()
    df_sort["_orig_idx"] = range(len(df_sort))

    chaves: List[str] = []
    ascendentes: List[bool] = []

    # Critério primário
    col_prim = config.criterio_primario.coluna_ou_expressao
    serie_prim = _aplicar_transformacao(df_sort[col_prim], config.criterio_primario.transformacao)
    df_sort["_k0"] = serie_prim
    chaves.append("_k0")
    ascendentes.append(config.criterio_primario.direcao == "crescente")

    # Regras de desempate
    for i, regra in enumerate(config.regras_desempate, start=1):
        k_col = f"_k{i}"
        if regra.tipo == "coluna_valor":
            col = regra.parametros.get("coluna", "")
            trans = regra.parametros.get("transformacao")
            serie = _aplicar_transformacao(df_sort[col], trans)
            df_sort[k_col] = serie
            asc = regra.parametros.get("direcao", "decrescente") == "crescente"

        elif regra.tipo == "concatenacao_agrupadores":
            agrup = config.agrupadores or regra.parametros.get("agrupadores", [])
            if agrup:
                df_sort[k_col] = (
                    df_sort[agrup]
                    .astype(str)
                    .apply(lambda row: " ".join(normalizar_texto(v) for v in row), axis=1)
                )
            else:
                df_sort[k_col] = ""
            asc = True

        elif regra.tipo == "coluna_texto_alfabetico":
            col = regra.parametros.get("coluna", "")
            df_sort[k_col] = df_sort[col].astype(str).apply(normalizar_texto)
            asc = regra.parametros.get("direcao", "crescente") == "crescente"

        elif regra.tipo == "ordem_de_insercao":
            df_sort[k_col] = df_sort["_orig_idx"]
            asc = True

        else:
            df_sort[k_col] = 0
            asc = True

        chaves.append(k_col)
        ascendentes.append(asc)

    return df_sort, chaves, ascendentes


def _rank_global(
    df: pd.DataFrame,
    config: ConfigRank,
    nome_coluna_rank: str,
) -> Tuple[pd.DataFrame, RankResult]:
    """Ranking global sobre todo o DataFrame."""
    warnings: List[WarningEstrutural] = []

    df_sort, chaves, ascendentes = _construir_chave_sort(df, config)

    df_sort["_rank_final"] = (
        df_sort.sort_values(chaves, ascending=ascendentes)
        .groupby(config.criterio_primario.coluna_ou_expressao, sort=False)
        .ngroup()
    )

    # pandas rank com método configurado sobre valor primário
    col_prim = config.criterio_primario.coluna_ou_expressao
    serie_prim = _aplicar_transformacao(df[col_prim].copy(), config.criterio_primario.transformacao)
    ascending_prim = config.criterio_primario.direcao == "crescente"

    if config.metodo_rank_para_empate_preservado == "min":
        rank_series = serie_prim.rank(
            method="min", ascending=ascending_prim, na_option="bottom"
        ).astype(int)
    else:
        # Usa ordenação completa por chaves para rank estável
        df_sorted = df_sort.sort_values(chaves, ascending=ascendentes)
        rank_series = pd.Series(
            range(1, len(df_sorted) + 1),
            index=df_sorted.index,
        )

    df_resultado = df.copy()
    df_resultado[nome_coluna_rank] = rank_series

    # Detecta empates (valores primários iguais dentro de tolerância)
    valores = _aplicar_transformacao(df[col_prim], config.criterio_primario.transformacao)
    diff = valores.sort_values().diff().abs()
    empates = int((diff <= config.tolerancia_float).sum()) - 1
    empates = max(0, empates)

    n_empatados = int((valores.groupby(
        valores.apply(lambda v: round(v / config.tolerancia_float) if config.tolerancia_float > 0 else v)
    ).transform("count") > 1).sum()) if empates > 0 else 0

    if empates > 0:
        warnings.append(WarningEstrutural(
            codigo="W-RANK-EMPATE",
            categoria=CategoriaWarning.INFORMATIVO,
            microcopy=f"{n_empatados} registros com valor primário empatado. Desempate por regras configuradas.",
            contexto={"n_empatados": n_empatados},
        ))

    return df_resultado, RankResult(
        coluna_rank_adicionada=nome_coluna_rank,
        empates_detectados=empates,
        regras_desempate_acionadas={},
        warnings_gerados=warnings,
    )


def _rank_com_ordenacao_completa(
    df: pd.DataFrame,
    config: ConfigRank,
    nome_coluna_rank: str,
    grupo_col: Optional[str] = None,
) -> Tuple[pd.DataFrame, RankResult]:
    """
    Ranking via ordenação completa por todas as chaves de desempate.
    Suporta escopo global, intra_grupo e cross_elementos_dentro_do_agrupador.
    """
    warnings: List[WarningEstrutural] = []

    df_resultado = df.copy()
    df_resultado["_orig_idx"] = range(len(df_resultado))

    col_prim = config.criterio_primario.coluna_ou_expressao

    def _rank_subset(subset: pd.DataFrame) -> pd.Series:
        df_s, chaves, ascendentes = _construir_chave_sort(subset, config)
        df_s = df_s.sort_values(chaves, ascending=ascendentes)

        if config.metodo_rank_para_empate_preservado == "min":
            col_val = _aplicar_transformacao(
                subset[col_prim], config.criterio_primario.transformacao
            )
            result_s = col_val.rank(
                method="min",
                ascending=(config.criterio_primario.direcao == "crescente")
            )
        else:
            result_s = pd.Series(
                range(1, len(df_s) + 1),
                index=df_s.index,
            )
        return result_s

    if grupo_col and grupo_col in df.columns:
        # Itera grupos explicitamente para evitar ambiguidade de apply
        rank_parts: List[pd.Series] = []
        for _, grp in df_resultado.groupby(grupo_col, sort=False):
            rank_parts.append(_rank_subset(grp))
        rank_series = pd.concat(rank_parts)
    else:
        rank_series = _rank_subset(df_resultado)

    df_resultado[nome_coluna_rank] = rank_series
    df_resultado = df_resultado.drop(columns=["_orig_idx"], errors="ignore")

    # Detecta empates no nível primário — conta linhas que compartilham valor com pelo menos outra
    def _contar_empatados(subset: pd.DataFrame) -> int:
        vals = _aplicar_transformacao(subset[col_prim], config.criterio_primario.transformacao)
        counts = vals.value_counts()
        return int((counts[counts > 1] * 1).sum())

    if grupo_col and grupo_col in df_resultado.columns:
        n_empatados = sum(
            _contar_empatados(grp)
            for _, grp in df_resultado.groupby(grupo_col, sort=False)
        )
    else:
        n_empatados = _contar_empatados(df_resultado)

    empates_total = n_empatados

    if empates_total > 0:
        warnings.append(WarningEstrutural(
            codigo="W-RANK-EMPATE",
            categoria=CategoriaWarning.INFORMATIVO,
            microcopy=f"{empates_total} empates no critério primário. Desempate aplicado.",
            contexto={"empates": empates_total},
        ))

    # Alerta de empate massivo (V6 · D-115): > 50% das linhas empatadas
    n_total = len(df_resultado)
    if n_total > 0:
        pct_empate = empates_total / n_total
        if pct_empate > 0.50:
            warnings.append(WarningEstrutural(
                codigo="W-RANK-EMPATE-MASSIVO",
                categoria=CategoriaWarning.ALERTA_ESTRUTURAL_LEVE,
                microcopy=f"{pct_empate:.1%} das linhas empatadas no critério primário.",
                contexto={"pct": round(pct_empate, 4)},
            ))

    return df_resultado, RankResult(
        coluna_rank_adicionada=nome_coluna_rank,
        empates_detectados=empates_total,
        regras_desempate_acionadas={},
        warnings_gerados=warnings,
    )


def aplicar_rank(
    df: pd.DataFrame,
    config: ConfigRank,
    nome_visao: str,
    nome_coluna_rank: str = "rank",
) -> Tuple[pd.DataFrame, RankResult]:
    """
    Aplica ranking determinístico com desempate configurável.
    Retorna df com coluna de rank + RankResult.

    Default 3 níveis (D-041): valor decrescente · concatenação agrupadores · ordem de inserção.
    Adaptações V7/V9/V6: 4 níveis via regras_desempate customizadas.
    """
    grupo_col = config.coluna_grupo if config.escopo != "global" else None

    df_resultado, result = _rank_com_ordenacao_completa(
        df, config, nome_coluna_rank, grupo_col=grupo_col
    )
    return df_resultado, result
