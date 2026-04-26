"""
t_acum.py — Acumulado progressivo monotônico · T-ACUM · E.3
Consumidores: V4 (Modo 2/3) · V10. Transversal simples sem adaptações.
"""
from __future__ import annotations

from typing import List, Literal, Optional, Tuple

import pandas as pd
from pydantic import BaseModel, Field

from contratos import CategoriaWarning, WarningEstrutural


class ConfigAcum(BaseModel):
    coluna_valor: str = Field(..., description="Coluna numérica a acumular · geralmente Participação")
    coluna_rank: str = Field(..., description="Coluna de rank produzida por T-RANK · determina ordem")
    escopo: Literal["global", "intra_grupo"] = Field("global")
    coluna_grupo: Optional[str] = None


class AcumResult(BaseModel):
    coluna_acumulado_adicionada: str
    monotonicidade_verificada: bool
    warnings_gerados: List[WarningEstrutural]


def aplicar_acumulado(
    df: pd.DataFrame,
    config: ConfigAcum,
    nome_visao: str,
    nome_coluna_acum: str = "acumulado",
) -> Tuple[pd.DataFrame, AcumResult]:
    """
    Aplica cumsum sobre coluna_valor na ordem do rank crescente.
    Invariante: acumulado é monotônico crescente (valores não-negativos esperados).
    """
    warnings: List[WarningEstrutural] = []
    df_resultado = df.copy()

    def _acumular_subset(subset: pd.DataFrame) -> pd.Series:
        ordenado = subset.sort_values(config.coluna_rank, ascending=True)
        acum = ordenado[config.coluna_valor].cumsum()
        return acum

    if config.escopo == "intra_grupo" and config.coluna_grupo:
        acum_series = df_resultado.groupby(config.coluna_grupo, sort=False, group_keys=False).apply(
            lambda g: _acumular_subset(g)
        )
    else:
        acum_series = _acumular_subset(df_resultado)

    df_resultado[nome_coluna_acum] = acum_series

    # Verifica monotonicidade
    monotonica = True
    if config.escopo == "intra_grupo" and config.coluna_grupo:
        for _, grp in df_resultado.groupby(config.coluna_grupo, sort=False):
            vals = grp.sort_values(config.coluna_rank)[nome_coluna_acum].dropna()
            if not (vals.diff().dropna() >= -1e-9).all():
                monotonica = False
                break
    else:
        vals = df_resultado.sort_values(config.coluna_rank)[nome_coluna_acum].dropna()
        monotonica = bool((vals.diff().dropna() >= -1e-9).all())

    # Detecta valores negativos na coluna valor (caso teórico)
    negativos = int((df_resultado[config.coluna_valor] < 0).sum())
    if negativos > 0:
        monotonica = False
        warnings.append(WarningEstrutural(
            codigo=f"W-V{nome_visao}-ACUM-NEGATIVO",
            categoria=CategoriaWarning.ALERTA_ESTRUTURAL_LEVE,
            microcopy=f"{negativos} linhas com valor negativo em '{config.coluna_valor}'. "
                      "Monotonicidade não garantida.",
            contexto={"n_negativos": negativos},
        ))

    return df_resultado, AcumResult(
        coluna_acumulado_adicionada=nome_coluna_acum,
        monotonicidade_verificada=monotonica,
        warnings_gerados=warnings,
    )
