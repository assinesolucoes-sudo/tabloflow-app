"""
t_agrupa.py — Consolidação Pré-Cálculo Obrigatória · T-AGRUPA · C.D1 · D-122
Suporte a 3 extensões: reconhecedor cronológico · regra por métrica · no-op validado.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List, Literal, Optional, Tuple, Union

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from contratos import CategoriaWarning, ColumnMeta, PadraoCronologicoEnum, WarningEstrutural
from utils.reconhecedor_cronologico import ordenar_cronologicamente

RegraAgregacao = Literal["soma", "media", "maximo", "minimo", "contagem", "primeiro"]

_AGGFUNC_MAP = {
    "soma": "sum",
    "media": "mean",
    "maximo": "max",
    "minimo": "min",
    "contagem": "count",
    "primeiro": "first",
}


def consolidar_com_modo(
    df: pd.DataFrame,
    agrupadores: List[str],
    regras: Union[RegraAgregacao, Dict[str, RegraAgregacao]],
    modo_base: Literal["TRANSACIONAL", "PRE_AGREGADO"],
    column_meta: Optional[Dict[str, ColumnMeta]] = None,
) -> Tuple[pd.DataFrame, List[WarningEstrutural]]:
    """
    Consolida DataFrame por agrupadores conforme modo declarado.

    Extensão 1 · reconhecedor cronológico: se column_meta fornecido e agrupador temporal
      detectado, ordenação cronológica é aplicada após consolidação.
    Extensão 2 · regra por métrica: regras aceita string ou Dict[metrica, regra].
    Extensão 3 · no-op validado: PRE_AGREGADO valida unicidade de chaves sem consolidar.

    Returns:
        (df_resultado, warnings)
    """
    warnings: List[WarningEstrutural] = []

    if not agrupadores:
        return df.copy(), warnings

    # ----------------------------------------------------------------
    # Extensão 3 · Modo PRE_AGREGADO (no-op validado)
    # ----------------------------------------------------------------
    if modo_base == "PRE_AGREGADO":
        duplicatas = df.duplicated(subset=agrupadores, keep=False)
        n_dup = int(duplicatas.sum())
        if n_dup > 0:
            warnings.append(WarningEstrutural(
                codigo="W-T-AGRUPA-DUPLICATA-PRE-AGREGADO",
                categoria=CategoriaWarning.ALERTA_ESTRUTURAL,
                microcopy=(
                    f"Modo Pré-agregado declarado mas {n_dup} linhas têm combinações "
                    f"duplicadas nos agrupadores {agrupadores}."
                ),
                contexto={"n_duplicatas": n_dup, "agrupadores": agrupadores},
            ))
        return df.copy(), warnings

    # ----------------------------------------------------------------
    # Modo TRANSACIONAL — consolidação real
    # ----------------------------------------------------------------
    # Determina colunas métricas (não agrupadores)
    colunas_metricas = [c for c in df.columns if c not in agrupadores]

    # Extensão 2 · normaliza regras para Dict[metrica, aggfunc_pandas]
    if isinstance(regras, str):
        aggfunc: Dict[str, str] = {m: _AGGFUNC_MAP[regras] for m in colunas_metricas}
        regras_efetivas: Dict[str, RegraAgregacao] = {m: regras for m in colunas_metricas}
    else:
        aggfunc = {}
        regras_efetivas = {}
        for m in colunas_metricas:
            regra = regras.get(m, "soma")
            aggfunc[m] = _AGGFUNC_MAP[regra]
            regras_efetivas[m] = regra

        warnings.append(WarningEstrutural(
            codigo="W-T-AGRUPA-REGRA-POR-METRICA",
            categoria=CategoriaWarning.INFORMATIVO,
            microcopy="Regras de agregação por métrica aplicadas.",
            contexto={"regras_efetivas": regras_efetivas},
        ))

    if not aggfunc:
        # Sem métricas: apenas deduplicar agrupadores
        df_resultado = df[agrupadores].drop_duplicates().reset_index(drop=True)
    else:
        df_resultado = (
            df.groupby(agrupadores, sort=False, as_index=False)
            .agg(aggfunc)
            .reset_index(drop=True)
        )

    # ----------------------------------------------------------------
    # Extensão 1 · Ordenação cronológica via column_meta
    # ----------------------------------------------------------------
    if column_meta:
        for agrup in agrupadores:
            meta = column_meta.get(agrup)
            if meta and meta.padrao_cronologico_detectado is not None:
                padrao = meta.padrao_cronologico_detectado
                valores_unicos = df_resultado[agrup].dropna().astype(str).tolist()
                ordem = ordenar_cronologicamente(valores_unicos, padrao)
                ordem_map = {v: i for i, v in enumerate(ordem)}
                df_resultado["_sort_key"] = (
                    df_resultado[agrup].astype(str).map(ordem_map).fillna(len(ordem))
                )
                df_resultado = (
                    df_resultado.sort_values("_sort_key")
                    .drop(columns=["_sort_key"])
                    .reset_index(drop=True)
                )
                break  # Ordena pelo primeiro agrupador temporal encontrado

    return df_resultado, warnings
