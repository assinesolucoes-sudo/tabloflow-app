"""
Visão V6 — Análise de Relacionamento entre Dimensões.

Executa o motor analítico que identifica como dois campos categóricos
se relacionam, calculando densidade de cruzamento via produto cartesiano.
"""

from __future__ import annotations

from enum import Enum
from typing import List, Optional

import pandas as pd
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Contratos de Entrada
# ---------------------------------------------------------------------------


class TipoMedida(str, Enum):
    CONTAGEM = "CONTAGEM"
    SOMA = "SOMA"
    MEDIA = "MEDIA"


class ConfigV6(BaseModel):
    eixo1: str
    eixo2: str
    tipo_medida: TipoMedida
    campo_medida: Optional[str] = None
    nome_analitico_medida: str
    limiar_dominante: float = 0.20
    limiar_residual: float = 0.02


# ---------------------------------------------------------------------------
# Contratos de Saída
# ---------------------------------------------------------------------------


class ClassificacaoDensidade(str, Enum):
    DOMINANTE = "DOMINANTE"
    RELEVANTE = "RELEVANTE"
    RESIDUAL = "RESIDUAL"
    AUSENTE = "AUSENTE"


class CombinacaoCruzamento(BaseModel):
    eixo1_valor: str
    eixo2_valor: str
    valor_medida: Optional[float]
    participacao_percentual: Optional[float]
    ranking: Optional[int]
    classificacao: ClassificacaoDensidade


class ResumoV6(BaseModel):
    total_combinacoes_possiveis: int
    total_combinacoes_presentes: int
    total_combinacoes_ausentes: int
    total_dominantes: int
    total_relevantes: int
    total_residuais: int
    valor_total_medida: float
    top5_dominantes: List[CombinacaoCruzamento]
    combinacoes_ausentes: List[CombinacaoCruzamento]


class V6Result(BaseModel):
    config: ConfigV6
    combinacoes: List[CombinacaoCruzamento]
    resumo: ResumoV6
    warnings: List[str]
    errors: List[str]
    success: bool


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------


def _resultado_erro(
    config: ConfigV6,
    errors: List[str],
    warnings: List[str],
) -> V6Result:
    """Retorna V6Result de falha com resumo vazio."""
    return V6Result(
        config=config,
        combinacoes=[],
        resumo=ResumoV6(
            total_combinacoes_possiveis=0,
            total_combinacoes_presentes=0,
            total_combinacoes_ausentes=0,
            total_dominantes=0,
            total_relevantes=0,
            total_residuais=0,
            valor_total_medida=0.0,
            top5_dominantes=[],
            combinacoes_ausentes=[],
        ),
        warnings=warnings,
        errors=errors,
        success=False,
    )


def _agregar(
    df: pd.DataFrame,
    eixo1: str,
    eixo2: str,
    tipo_medida: TipoMedida,
    campo_medida: Optional[str],
) -> pd.DataFrame:
    """Agrega o DataFrame por (eixo1, eixo2) conforme o tipo de medida."""
    if tipo_medida == TipoMedida.CONTAGEM:
        return (
            df.groupby([eixo1, eixo2], sort=False)
            .size()
            .reset_index(name="valor_medida")
        )
    if tipo_medida == TipoMedida.SOMA:
        return (
            df.groupby([eixo1, eixo2], sort=False)[campo_medida]
            .sum()
            .reset_index(name="valor_medida")
        )
    # MEDIA
    return (
        df.groupby([eixo1, eixo2], sort=False)[campo_medida]
        .mean()
        .reset_index(name="valor_medida")
    )


def _classificar_dominante(
    df_sorted: pd.DataFrame,
    limiar_dominante: float,
    valor_total: float,
) -> set[int]:
    """
    Retorna o conjunto de índices (posicionais) das combinações DOMINANTES.

    Acumula valores em ordem decrescente até atingir limiar_dominante * valor_total.
    A combinação que faz o acumulado cruzar o limiar também é incluída.
    """
    if valor_total <= 0:
        return set()

    alvo = limiar_dominante * valor_total
    acumulado = 0.0
    dominantes: set[int] = set()

    for pos, (_, row) in enumerate(df_sorted.iterrows()):
        acumulado += float(row["valor_medida"])
        dominantes.add(pos)
        if acumulado >= alvo:
            break

    return dominantes


def _verificar_concentracao_extrema(
    df_sorted: pd.DataFrame,
    valor_total: float,
) -> Optional[int]:
    """
    Retorna quantas combinações representam >80% do total se esse número for < 3.
    Retorna None caso contrário.
    """
    if valor_total <= 0:
        return None

    acumulado = 0.0
    for pos, (_, row) in enumerate(df_sorted.iterrows()):
        acumulado += float(row["valor_medida"])
        if acumulado / valor_total > 0.80:
            n = pos + 1
            return n if n < 3 else None

    return None


# ---------------------------------------------------------------------------
# Função principal
# ---------------------------------------------------------------------------


def analisar_v6(df: pd.DataFrame, config: ConfigV6) -> V6Result:
    """
    Executa a análise de relacionamento entre dimensões (V6).

    Args:
        df: DataFrame já processado pelo Motor Base
        config: configuração da análise (eixos, medida, limiares)

    Returns:
        V6Result com combinações classificadas, resumo e warnings/errors
    """
    warnings: List[str] = []
    errors: List[str] = []

    # ------------------------------------------------------------------
    # Validações (erros bloqueantes)
    # ------------------------------------------------------------------

    # E03 — mesmo campo nos dois eixos
    if config.eixo1 == config.eixo2:
        errors.append("E03: Eixo 1 e Eixo 2 não podem ser o mesmo campo.")
        return _resultado_erro(config, errors, warnings)

    # E01 — eixo1 não encontrado
    if config.eixo1 not in df.columns:
        errors.append(f"E01: Campo '{config.eixo1}' (eixo1) não encontrado na base.")
        return _resultado_erro(config, errors, warnings)

    # E02 — eixo2 não encontrado
    if config.eixo2 not in df.columns:
        errors.append(f"E02: Campo '{config.eixo2}' (eixo2) não encontrado na base.")
        return _resultado_erro(config, errors, warnings)

    # E04 — campo_medida ausente ou não encontrado quando necessário
    if config.tipo_medida != TipoMedida.CONTAGEM:
        if not config.campo_medida:
            errors.append(
                f"E04: 'campo_medida' é obrigatório quando tipo_medida é "
                f"'{config.tipo_medida.value}'."
            )
            return _resultado_erro(config, errors, warnings)
        if config.campo_medida not in df.columns:
            errors.append(
                f"E04: Campo de medida '{config.campo_medida}' não encontrado na base."
            )
            return _resultado_erro(config, errors, warnings)

    # E05 — campo_medida não numérico para SOMA/MEDIA
    if config.tipo_medida in (TipoMedida.SOMA, TipoMedida.MEDIA):
        if not pd.api.types.is_numeric_dtype(df[config.campo_medida]):
            errors.append(
                f"E05: Campo '{config.campo_medida}' não é numérico. "
                f"Tipo_medida '{config.tipo_medida.value}' requer coluna numérica."
            )
            return _resultado_erro(config, errors, warnings)

    # E06 — base vazia
    if df.empty:
        errors.append("E06: Base vazia após filtros.")
        return _resultado_erro(config, errors, warnings)

    # ------------------------------------------------------------------
    # Preparação do DataFrame de trabalho
    # ------------------------------------------------------------------

    df_trabalho = df.copy()
    df_trabalho[config.eixo1] = df_trabalho[config.eixo1].astype(str)
    df_trabalho[config.eixo2] = df_trabalho[config.eixo2].astype(str)

    # ------------------------------------------------------------------
    # Warnings que não bloqueiam
    # ------------------------------------------------------------------

    # W03 — base pequena
    if len(df_trabalho) < 50:
        warnings.append(
            f"W03: Base com {len(df_trabalho)} registros. "
            "A classificação de densidade pode ser instável."
        )

    # W06 — base pré-agregada com duplicatas (só para SOMA/MEDIA)
    if config.tipo_medida in (TipoMedida.SOMA, TipoMedida.MEDIA):
        if df_trabalho.duplicated(subset=[config.eixo1, config.eixo2]).any():
            warnings.append(
                "W06: Base parece pré-agregada mas contém combinações duplicadas. "
                "Os valores foram somados."
            )

    # Valores únicos dos eixos (após conversão para string)
    valores_eixo1: List[str] = df_trabalho[config.eixo1].unique().tolist()
    valores_eixo2: List[str] = df_trabalho[config.eixo2].unique().tolist()

    # W01 — cardinalidade excessiva
    if len(valores_eixo1) > 200:
        warnings.append(
            f"W01: Campo '{config.eixo1}' tem {len(valores_eixo1)} valores distintos. "
            "Matrizes muito grandes podem prejudicar a leitura."
        )
    if len(valores_eixo2) > 200:
        warnings.append(
            f"W01: Campo '{config.eixo2}' tem {len(valores_eixo2)} valores distintos. "
            "Matrizes muito grandes podem prejudicar a leitura."
        )

    total_possiveis: int = len(valores_eixo1) * len(valores_eixo2)

    # W02 — base trivial
    if total_possiveis < 10:
        warnings.append(
            f"W02: Apenas {total_possiveis} combinações possíveis. "
            "A análise pode ter valor limitado."
        )

    # W05 — medida não aditiva (SOMA em campo aparentemente percentual)
    if config.tipo_medida == TipoMedida.SOMA and config.campo_medida:
        col_vals = df[config.campo_medida].dropna()
        nome_lower = config.campo_medida.lower()
        termos_suspeitos = (
            "perc", "pct", "taxa", "rate", "ratio",
            "indice", "índice", "index", "prop", "share",
        )
        nome_suspeito = any(t in nome_lower for t in termos_suspeitos)
        entre_zero_um = bool(col_vals.between(0, 1).all())
        entre_zero_cem = bool(col_vals.between(0, 100).all()) and nome_suspeito
        if entre_zero_um or entre_zero_cem:
            warnings.append(
                f"W05: Campo '{config.campo_medida}' pode ser percentual ou índice. "
                "Soma pode não fazer sentido analítico."
            )

    # ------------------------------------------------------------------
    # Agregação
    # ------------------------------------------------------------------

    df_agg = _agregar(
        df_trabalho,
        config.eixo1,
        config.eixo2,
        config.tipo_medida,
        config.campo_medida,
    )
    df_agg["valor_medida"] = df_agg["valor_medida"].astype(float)

    valor_total: float = float(df_agg["valor_medida"].sum())

    # ------------------------------------------------------------------
    # Participação percentual (denominador = total das presentes)
    # ------------------------------------------------------------------

    if valor_total != 0:
        df_agg["participacao_percentual"] = df_agg["valor_medida"] / valor_total
    else:
        df_agg["participacao_percentual"] = 0.0

    # ------------------------------------------------------------------
    # Ordenação e ranking
    # Critério: valor_medida DESC; desempate: eixo1 ASC, eixo2 ASC
    # ------------------------------------------------------------------

    df_sorted = df_agg.sort_values(
        by=["valor_medida", config.eixo1, config.eixo2],
        ascending=[False, True, True],
    ).reset_index(drop=True)

    df_sorted["ranking"] = range(1, len(df_sorted) + 1)

    # ------------------------------------------------------------------
    # W04 — concentração extrema
    # ------------------------------------------------------------------

    n_concentrado = _verificar_concentracao_extrema(df_sorted, valor_total)
    if n_concentrado is not None:
        warnings.append(
            f"W04: Alta concentração: {n_concentrado} combinações representam mais de "
            "80% do total. O limiar padrão de Dominante pode não ser adequado."
        )

    # ------------------------------------------------------------------
    # Classificação DOMINANTE
    # ------------------------------------------------------------------

    dominantes_pos = _classificar_dominante(df_sorted, config.limiar_dominante, valor_total)

    # ------------------------------------------------------------------
    # Montar combinações presentes
    # ------------------------------------------------------------------

    combinacoes_presentes: List[CombinacaoCruzamento] = []

    for pos, row in df_sorted.iterrows():
        if pos in dominantes_pos:
            classificacao = ClassificacaoDensidade.DOMINANTE
        elif float(row["participacao_percentual"]) < config.limiar_residual:
            classificacao = ClassificacaoDensidade.RESIDUAL
        else:
            classificacao = ClassificacaoDensidade.RELEVANTE

        combinacoes_presentes.append(
            CombinacaoCruzamento(
                eixo1_valor=str(row[config.eixo1]),
                eixo2_valor=str(row[config.eixo2]),
                valor_medida=float(row["valor_medida"]),
                participacao_percentual=float(row["participacao_percentual"]),
                ranking=int(row["ranking"]),
                classificacao=classificacao,
            )
        )

    # ------------------------------------------------------------------
    # Identificar combinações ausentes
    # ------------------------------------------------------------------

    presentes_set: set[tuple[str, str]] = {
        (c.eixo1_valor, c.eixo2_valor) for c in combinacoes_presentes
    }

    combinacoes_ausentes: List[CombinacaoCruzamento] = []
    for v1 in sorted(valores_eixo1):
        for v2 in sorted(valores_eixo2):
            if (v1, v2) not in presentes_set:
                combinacoes_ausentes.append(
                    CombinacaoCruzamento(
                        eixo1_valor=v1,
                        eixo2_valor=v2,
                        valor_medida=None,
                        participacao_percentual=None,
                        ranking=None,
                        classificacao=ClassificacaoDensidade.AUSENTE,
                    )
                )

    # ------------------------------------------------------------------
    # Contagens e resumo
    # ------------------------------------------------------------------

    total_dominantes = sum(
        1 for c in combinacoes_presentes
        if c.classificacao == ClassificacaoDensidade.DOMINANTE
    )
    total_relevantes = sum(
        1 for c in combinacoes_presentes
        if c.classificacao == ClassificacaoDensidade.RELEVANTE
    )
    total_residuais = sum(
        1 for c in combinacoes_presentes
        if c.classificacao == ClassificacaoDensidade.RESIDUAL
    )

    # top5_dominantes: primeiras 5 do ranking geral (presentes, ordenadas por ranking)
    top5_dominantes = combinacoes_presentes[:5]

    resumo = ResumoV6(
        total_combinacoes_possiveis=total_possiveis,
        total_combinacoes_presentes=len(combinacoes_presentes),
        total_combinacoes_ausentes=len(combinacoes_ausentes),
        total_dominantes=total_dominantes,
        total_relevantes=total_relevantes,
        total_residuais=total_residuais,
        valor_total_medida=valor_total,
        top5_dominantes=top5_dominantes,
        combinacoes_ausentes=combinacoes_ausentes,
    )

    return V6Result(
        config=config,
        combinacoes=combinacoes_presentes,
        resumo=resumo,
        warnings=warnings,
        errors=errors,
        success=True,
    )
