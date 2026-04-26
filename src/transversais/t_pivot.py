"""
t_pivot.py — Pivot POR_LINHAS → POR_COLUNAS · T-PIVOT · D-026/D-039/D-062 · E.5
3 semânticas formalizadas: ESTADOS_EMPILHADOS · MULTI_MEDIDA · PONTOS_DO_EIXO
"""
from __future__ import annotations

from typing import List, Literal, Optional, Tuple

import pandas as pd
from pydantic import BaseModel, Field

from contratos import CategoriaWarning, WarningEstrutural

SemanticaPivot = Literal["ESTADOS_EMPILHADOS", "MULTI_MEDIDA", "PONTOS_DO_EIXO"]
RegraAggPivot = Literal["SUM", "MEAN", "MAX", "MIN", "COUNT"]

_AGGFUNC_MAP: dict = {
    "SUM": "sum",
    "MEAN": "mean",
    "MAX": "max",
    "MIN": "min",
    "COUNT": "count",
}


class ConfigPivot(BaseModel):
    semantica: SemanticaPivot = Field(..., description="3 semânticas formalizadas")
    coluna_discriminadora: str = Field(
        ..., description="Coluna cujos valores viram cabeçalhos"
    )
    valores_selecionados: Optional[List[str]] = Field(
        None, description="Subset de valores a pivotar · None = todos"
    )
    coluna_valor_a_agregar: str = Field(
        ..., description="Coluna numérica que preenche a matriz"
    )
    agrupadores: List[str] = Field(
        default_factory=list, description="Colunas preservadas como índice"
    )
    regra_agregacao_em_colisao: RegraAggPivot = Field(
        "SUM", description="Aplicada em colisão (agrupadores + discriminadora com múltiplas linhas)"
    )
    threshold_cardinalidade_eixo: int = Field(
        10, description="TED · limiar para ativar seleção em PONTOS_DO_EIXO"
    )


class PivotResult(BaseModel):
    df_pivotado: pd.DataFrame
    colunas_geradas: List[str]
    valores_pivotados: List[str]
    valores_nao_pivotados: List[str]
    linhas_colidas_consolidadas: int
    warnings_gerados: List[WarningEstrutural]

    model_config = {"arbitrary_types_allowed": True}


def aplicar_pivot(
    df: pd.DataFrame,
    config: ConfigPivot,
    nome_visao: str,
) -> Tuple[pd.DataFrame, PivotResult]:
    """
    Aplica pivot usando pandas.pivot_table.
    Motor opera idêntico nas 3 semânticas · diferença é de vocabulário e contexto.
    """
    warnings: List[WarningEstrutural] = []

    todos_valores = sorted(df[config.coluna_discriminadora].dropna().unique().tolist(),
                           key=str)

    # Determina valores a pivotar
    if config.valores_selecionados is not None:
        valores_a_pivotar = [v for v in config.valores_selecionados if v in todos_valores]
        valores_nao_selecionados = [v for v in todos_valores if v not in config.valores_selecionados]
    else:
        valores_a_pivotar = todos_valores
        valores_nao_selecionados = []

    if valores_nao_selecionados:
        warnings.append(WarningEstrutural(
            codigo=f"W-V{nome_visao}-PIVOT-VALORES-NAO-SELECIONADOS",
            categoria=CategoriaWarning.INFORMATIVO,
            microcopy=f"Valores não incluídos no pivot: {sorted(str(v) for v in valores_nao_selecionados)}.",
            contexto={"valores_excluidos": [str(v) for v in sorted(valores_nao_selecionados, key=str)]},
        ))

    # PONTOS_DO_EIXO: alerta de alta cardinalidade
    if (
        config.semantica == "PONTOS_DO_EIXO"
        and len(todos_valores) > 50
    ):
        warnings.append(WarningEstrutural(
            codigo=f"W-V{nome_visao}-PIVOT-CARDINALIDADE-ALTA",
            categoria=CategoriaWarning.ALERTA_ESTRUTURAL_LEVE,
            microcopy=f"Coluna discriminadora tem {len(todos_valores)} valores únicos · resultado será muito largo.",
            contexto={"cardinalidade": len(todos_valores)},
        ))

    # Filtra df para valores selecionados
    df_filtrado = df[df[config.coluna_discriminadora].isin(valores_a_pivotar)].copy()

    # Conta linhas antes para detectar colisões
    n_antes = len(df_filtrado)

    aggfunc = _AGGFUNC_MAP[config.regra_agregacao_em_colisao]

    index_cols = config.agrupadores if config.agrupadores else None

    df_pivotado = pd.pivot_table(
        df_filtrado,
        values=config.coluna_valor_a_agregar,
        index=config.agrupadores if config.agrupadores else df_filtrado.index,
        columns=config.coluna_discriminadora,
        aggfunc=aggfunc,
        fill_value=0,
    ).reset_index()

    # Limpar nível de coluna gerado pelo pivot_table
    df_pivotado.columns.name = None

    # Detecta colisões: linhas consolidadas > linhas que teriam sem consolidação
    n_linhas_esperadas = len(df_filtrado.drop_duplicates(
        subset=(config.agrupadores + [config.coluna_discriminadora]) if config.agrupadores
        else [config.coluna_discriminadora]
    ))
    colisoes = max(0, n_antes - n_linhas_esperadas)

    if colisoes > 0:
        warnings.append(WarningEstrutural(
            codigo=f"W-V{nome_visao}-PIVOT-COLISAO",
            categoria=CategoriaWarning.INFORMATIVO,
            microcopy=f"{colisoes} linhas consolidadas por regra '{config.regra_agregacao_em_colisao}' em colisão.",
            contexto={"linhas_colisao": colisoes, "regra": config.regra_agregacao_em_colisao},
        ))

    colunas_geradas = [c for c in df_pivotado.columns if c not in config.agrupadores]

    return df_pivotado, PivotResult(
        df_pivotado=df_pivotado,
        colunas_geradas=colunas_geradas,
        valores_pivotados=[str(v) for v in valores_a_pivotar],
        valores_nao_pivotados=[str(v) for v in valores_nao_selecionados],
        linhas_colidas_consolidadas=colisoes,
        warnings_gerados=warnings,
    )
