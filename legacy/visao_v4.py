"""
visao_v4.py — V4: Composição e Participação
TabloFlow · Módulo 1 · TabloAnálise

Fluxo: MotorResult → executar_v4(config) → V4Result
"""

from __future__ import annotations

from typing import List, Optional, Literal
import pandas as pd
from pydantic import BaseModel, Field

from motor_base import MotorResult


# ---------------------------------------------------------------------------
# Modelos de Configuração
# ---------------------------------------------------------------------------


class MedidaConfig(BaseModel):
    """Configuração de uma medida a ser analisada."""

    campo: str
    nome_analitico: str
    tipo: Literal["moeda", "numero", "percentual"]


class AgrupadorConfig(BaseModel):
    """Configuração de um agrupador (dimensão de análise)."""

    campo: str
    nome: str


class V4Config(BaseModel):
    """Configuração completa para execução da V4."""

    modo: Literal[1, 2, 3]
    estrutura_entrada: Literal["coluna", "linha"]
    medidas: List[MedidaConfig]
    agrupadores: List[AgrupadorConfig]
    limiar_a: float = Field(default=0.80, ge=0.0, le=1.0)
    limiar_b: float = Field(default=0.95, ge=0.0, le=1.0)


# ---------------------------------------------------------------------------
# Modelos de Saída — Contrato V4Result (spec_v4.md §8)
# ---------------------------------------------------------------------------


class ElementoComposicao(BaseModel):
    """Um elemento dentro de uma distribuição."""

    agrupador: str
    valor_agregado: float
    participacao_pct: float
    ranking: int
    participacao_acumulada_pct: float
    classe_abc: Optional[str] = None  # "A", "B", "C" — None no Modo 1


class DivergenciaMedida(BaseModel):
    """Divergência de posição de um elemento entre duas medidas (Modo 3)."""

    agrupador: str
    medida_a: str
    medida_b: str
    classe_medida_a: str
    classe_medida_b: str
    delta_ranking: int  # ranking(medida_a) − ranking(medida_b)
    inverteu_posicao: bool  # True se mudou de classe ABC entre as medidas


class DistribuicaoPorDimensao(BaseModel):
    """Distribuição completa de uma medida dentro de uma dimensão."""

    dimensao: str
    medida: str
    total_geral: float
    n_elementos: int
    elementos: List[ElementoComposicao]
    limiar_a: Optional[float] = None
    limiar_b: Optional[float] = None
    n_classe_a: Optional[int] = None
    n_classe_b: Optional[int] = None
    n_classe_c: Optional[int] = None
    pct_total_classe_a: Optional[float] = None
    alerta_concentracao_critica: bool = False


class V4Result(BaseModel):
    """Resultado completo da V4 — Composição e Participação."""

    modo: Literal[1, 2, 3]
    estrutura_entrada: Literal["coluna", "linha"]
    distribuicoes: List[DistribuicaoPorDimensao]
    divergencias: Optional[List[DivergenciaMedida]] = None  # apenas Modo 3
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    success: bool = True


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

# Palavras-chave que indicam medida não aditiva (média, percentual, índice)
_KEYWORDS_NAO_ADITIVO = (
    "pct", "perc", "percent", "taxa", "media", "média",
    "avg", "mean", "indice", "índice", "index", "ratio",
    "tick", "ticket", "margem_pct", "yield",
)


def _preparar_tabela(df: pd.DataFrame, config: V4Config) -> pd.DataFrame:
    """
    Prepara o DataFrame para análise.

    Se estrutura_entrada == 'linha', executa pivot transformando os valores
    de uma coluna-tipo em colunas de medida. Registros sem valor em alguma
    medida recebem 0 após o pivot (nunca descartados).
    Se estrutura_entrada == 'coluna', retorna cópia sem alteração.
    """
    if config.estrutura_entrada == "coluna":
        return df.copy()

    campos_agrupador = [a.campo for a in config.agrupadores]
    campos_medida_nomes = {m.campo for m in config.medidas}

    # Identificar coluna cujos valores coincidem com os campos de medida configurados
    col_tipo: Optional[str] = None
    for col in df.columns:
        if col in campos_agrupador:
            continue
        valores = set(df[col].dropna().astype(str).unique())
        if campos_medida_nomes and campos_medida_nomes.issubset(valores):
            col_tipo = col
            break

    if col_tipo is None:
        # Fallback: tratar como "coluna" — medidas já são colunas diretas
        return df.copy()

    # Identificar coluna de valor numérico restante
    cols_restantes = [
        c for c in df.columns if c not in campos_agrupador and c != col_tipo
    ]
    col_valor: Optional[str] = next(
        (c for c in cols_restantes if pd.api.types.is_numeric_dtype(df[c])), None
    )
    if col_valor is None:
        return df.copy()

    pivot = df.pivot_table(
        index=campos_agrupador,
        columns=col_tipo,
        values=col_valor,
        aggfunc="sum",
        fill_value=0,
    ).reset_index()
    pivot.columns.name = None
    return pivot


def _get_column_types(motor_result: MotorResult) -> dict[str, str]:
    """Extrai mapeamento {campo: inferred_type} a partir do MotorResult."""
    col_types: dict[str, str] = {}
    columns = getattr(motor_result, "columns", None)
    if not columns:
        return col_types
    for col in columns:
        name = getattr(col, "name", None)
        itype = getattr(col, "inferred_type", None)
        if name and itype:
            col_types[name] = itype
    return col_types


def _detectar_limitadores(
    df: pd.DataFrame,
    config: V4Config,
    motor_result: MotorResult,
) -> tuple[list[str], list[str]]:
    """
    Detecta todos os limitadores técnicos definidos em spec_v4.md §7.

    Retorna (warnings, errors). Apenas total_geral zero é erro bloqueante
    (tratado em _calcular_distribuicao). Demais são warnings não bloqueantes.
    """
    warnings: list[str] = []
    errors: list[str] = []

    col_types = _get_column_types(motor_result)

    # 1. Medidas não aditivas
    for medida in config.medidas:
        if medida.tipo == "percentual":
            warnings.append(
                f"Medida '{medida.nome_analitico}' ({medida.campo}) é do tipo percentual — "
                "percentuais não podem ser somados para gerar um total válido. "
                "Use a medida base (ex: Receita Total) em vez da medida derivada."
            )
        elif any(kw in medida.campo.lower() for kw in _KEYWORDS_NAO_ADITIVO):
            warnings.append(
                f"Campo '{medida.campo}' pode ser uma medida não aditiva "
                "(nome sugere percentual, média ou índice). Verifique se a soma faz sentido analítico."
            )
        # Detectar via classificação semântica do MotorResult
        tipo_motor = col_types.get(medida.campo, "")
        if tipo_motor and tipo_motor not in ("numeric", ""):
            warnings.append(
                f"Campo '{medida.campo}' possui tipo '{tipo_motor}' no MotorResult — "
                "esperado 'numeric' para cálculo de participação."
            )

    # 2. Valores negativos significativos (> 5% dos registros)
    for medida in config.medidas:
        if medida.campo not in df.columns:
            continue
        col = pd.to_numeric(df[medida.campo], errors="coerce")
        total_validos = int(col.notna().sum())
        neg_count = int((col < 0).sum())
        if total_validos > 0 and neg_count / total_validos > 0.05:
            warnings.append(
                f"Medida '{medida.nome_analitico}' contém {neg_count} valores negativos "
                f"({neg_count / total_validos:.1%} dos registros) — "
                "participação % pode ser instável. Considere usar valor absoluto ou filtrar negativos."
            )

    # 3. Alta cardinalidade nos agrupadores
    for agrup in config.agrupadores:
        if agrup.campo not in df.columns:
            continue
        n_unique = int(df[agrup.campo].nunique())
        if n_unique > 100:
            warnings.append(
                f"Agrupador '{agrup.nome}' possui {n_unique} valores únicos (> 100) — "
                "Curva ABC perde legibilidade com muitos elementos Classe C."
            )

    # 4. Registros duplicados no agrupador (indica que haverá agregação)
    for agrup in config.agrupadores:
        if agrup.campo not in df.columns:
            continue
        dup_count = int(df[agrup.campo].duplicated().sum())
        if dup_count > 0:
            warnings.append(
                f"Agrupador '{agrup.nome}' possui {dup_count} registros duplicados — "
                "os valores serão somados na agregação. Verifique se o comportamento é esperado."
            )

    return warnings, errors


def _classificar_abc(acumulado_pct: float, limiar_a: float, limiar_b: float) -> str:
    """
    Classifica elemento como A, B ou C com base na participação acumulada (0–100).

    A = acumulado ≤ limiar_a×100
    B = acumulado ≤ limiar_b×100
    C = demais
    """
    if acumulado_pct <= limiar_a * 100.0:
        return "A"
    if acumulado_pct <= limiar_b * 100.0:
        return "B"
    return "C"


def _calcular_distribuicao(
    df: pd.DataFrame,
    agrup_config: AgrupadorConfig,
    medida_config: MedidaConfig,
    config: V4Config,
) -> tuple[Optional[DistribuicaoPorDimensao], list[str], list[str]]:
    """
    Calcula distribuição completa para um par (agrupador, medida).

    Retorna (DistribuicaoPorDimensao | None, warnings, errors).
    None indica erro bloqueante (total geral zero ou campo ausente).
    """
    warnings: list[str] = []
    errors: list[str] = []

    campo_agrup = agrup_config.campo
    campo_medida = medida_config.campo

    if campo_agrup not in df.columns:
        errors.append(
            f"Campo agrupador '{campo_agrup}' não encontrado no DataFrame."
        )
        return None, warnings, errors

    if campo_medida not in df.columns:
        errors.append(
            f"Campo de medida '{campo_medida}' não encontrado no DataFrame."
        )
        return None, warnings, errors

    df_work = df.copy()

    # Nulos no agrupador → "Não Informado"
    df_work[campo_agrup] = df_work[campo_agrup].fillna("Não Informado").astype(str)

    # Converter medida para numérico; nulos viram 0
    df_work[campo_medida] = pd.to_numeric(df_work[campo_medida], errors="coerce").fillna(0.0)

    # Agregação por agrupador
    agregado = (
        df_work.groupby(campo_agrup, as_index=False)[campo_medida]
        .sum()
        .rename(columns={campo_medida: "valor_agregado"})
    )
    agregado["valor_agregado"] = agregado["valor_agregado"].astype(float)

    total_geral = float(agregado["valor_agregado"].sum())

    # Erro bloqueante: total geral zero
    if total_geral == 0.0:
        errors.append(
            f"Total geral zero para medida '{medida_config.nome_analitico}' "
            f"na dimensão '{agrup_config.nome}' — processamento bloqueado para esta distribuição."
        )
        return None, warnings, errors

    # Participação %
    agregado["participacao_pct"] = (agregado["valor_agregado"] / total_geral) * 100.0

    # Ranking: posição 1 = maior valor; empate desempata por ordem alfabética
    agregado = agregado.sort_values(
        by=["valor_agregado", campo_agrup],
        ascending=[False, True],
    ).reset_index(drop=True)
    agregado["ranking"] = range(1, len(agregado) + 1)

    # Participação acumulada
    agregado["participacao_acumulada_pct"] = agregado["participacao_pct"].cumsum()

    # Ajuste de fechamento em 100% — corrige erros de ponto flutuante no último elemento
    soma_atual = float(agregado["participacao_pct"].sum())
    diff = 100.0 - soma_atual
    if abs(diff) > 1e-9 and len(agregado) > 0:
        agregado.loc[agregado.index[-1], "participacao_pct"] += diff
        agregado["participacao_acumulada_pct"] = agregado["participacao_pct"].cumsum()

    # Garantir fechamento exato no último elemento
    if len(agregado) > 0:
        agregado.loc[agregado.index[-1], "participacao_acumulada_pct"] = 100.0

    # Construir lista de elementos
    elementos: list[ElementoComposicao] = []
    for _, row in agregado.iterrows():
        classe: Optional[str] = None
        if config.modo in (2, 3):
            classe = _classificar_abc(
                float(row["participacao_acumulada_pct"]),
                config.limiar_a,
                config.limiar_b,
            )
        elementos.append(
            ElementoComposicao(
                agrupador=str(row[campo_agrup]),
                valor_agregado=round(float(row["valor_agregado"]), 6),
                participacao_pct=round(float(row["participacao_pct"]), 6),
                ranking=int(row["ranking"]),
                participacao_acumulada_pct=round(float(row["participacao_acumulada_pct"]), 6),
                classe_abc=classe,
            )
        )

    # KPIs ABC (Modos 2 e 3)
    n_classe_a = n_classe_b = n_classe_c = None
    pct_total_classe_a: Optional[float] = None
    if config.modo in (2, 3):
        n_classe_a = sum(1 for e in elementos if e.classe_abc == "A")
        n_classe_b = sum(1 for e in elementos if e.classe_abc == "B")
        n_classe_c = sum(1 for e in elementos if e.classe_abc == "C")
        soma_valor_a = sum(e.valor_agregado for e in elementos if e.classe_abc == "A")
        pct_total_classe_a = soma_valor_a / total_geral * 100.0

    alerta_critico = any(e.participacao_pct > 50.0 for e in elementos)

    return (
        DistribuicaoPorDimensao(
            dimensao=agrup_config.nome,
            medida=medida_config.nome_analitico,
            total_geral=total_geral,
            n_elementos=len(elementos),
            elementos=elementos,
            limiar_a=config.limiar_a if config.modo in (2, 3) else None,
            limiar_b=config.limiar_b if config.modo in (2, 3) else None,
            n_classe_a=n_classe_a,
            n_classe_b=n_classe_b,
            n_classe_c=n_classe_c,
            pct_total_classe_a=pct_total_classe_a,
            alerta_concentracao_critica=alerta_critico,
        ),
        warnings,
        errors,
    )


def _calcular_divergencias(
    distribuicoes: list[DistribuicaoPorDimensao],
    config: V4Config,
) -> list[DivergenciaMedida]:
    """
    Calcula divergências de posição entre pares de medidas por agrupador (Modo 3).

    Compara a primeira medida (referência) contra cada medida subsequente.
    Delta de Ranking = ranking(medida_ref) − ranking(medida_b).
    inverteu_posicao = True se a classe ABC mudou entre as duas medidas.
    """
    if len(config.medidas) < 2:
        return []

    divergencias: list[DivergenciaMedida] = []
    medida_ref_nome = config.medidas[0].nome_analitico

    # Agrupar distribuições por dimensão
    dims: dict[str, dict[str, DistribuicaoPorDimensao]] = {}
    for dist in distribuicoes:
        dims.setdefault(dist.dimensao, {})[dist.medida] = dist

    for dimensao, dists_dim in dims.items():
        if medida_ref_nome not in dists_dim:
            continue
        ref_by_agrup = {e.agrupador: e for e in dists_dim[medida_ref_nome].elementos}

        for medida_b_config in config.medidas[1:]:
            medida_b_nome = medida_b_config.nome_analitico
            if medida_b_nome not in dists_dim:
                continue
            b_by_agrup = {e.agrupador: e for e in dists_dim[medida_b_nome].elementos}

            for agrup in set(ref_by_agrup) & set(b_by_agrup):
                e_a = ref_by_agrup[agrup]
                e_b = b_by_agrup[agrup]

                # Classe ABC só existe no Modo 3 (garantido pelo fluxo)
                if e_a.classe_abc is None or e_b.classe_abc is None:
                    continue

                divergencias.append(
                    DivergenciaMedida(
                        agrupador=agrup,
                        medida_a=medida_ref_nome,
                        medida_b=medida_b_nome,
                        classe_medida_a=e_a.classe_abc,
                        classe_medida_b=e_b.classe_abc,
                        delta_ranking=e_a.ranking - e_b.ranking,
                        inverteu_posicao=e_a.classe_abc != e_b.classe_abc,
                    )
                )

    return divergencias


# ---------------------------------------------------------------------------
# Função Principal
# ---------------------------------------------------------------------------


def executar_v4(motor_result: MotorResult, config: V4Config) -> V4Result:
    """
    Executa a V4 — Composição e Participação.

    Args:
        motor_result: Resultado do Motor Base contendo DataFrame e metadados.
        config: Configuração do usuário (modo, estrutura, medidas, agrupadores, limiares).

    Returns:
        V4Result com distribuições, divergências (Modo 3) e lista de warnings/errors.
    """
    all_warnings: list[str] = []
    all_errors: list[str] = []

    # Modo 3 exige mínimo de 2 medidas
    if config.modo == 3 and len(config.medidas) < 2:
        return V4Result(
            modo=config.modo,
            estrutura_entrada=config.estrutura_entrada,
            distribuicoes=[],
            divergencias=None,
            errors=["Modo 3 requer mínimo de 2 medidas configuradas."],
            success=False,
        )

    # Extrair DataFrame do MotorResult (suporta atributos 'df' ou 'dataframe')
    df: Optional[pd.DataFrame] = getattr(motor_result, "df", None)
    if df is None:
        df = getattr(motor_result, "dataframe", None)
    if not isinstance(df, pd.DataFrame):
        return V4Result(
            modo=config.modo,
            estrutura_entrada=config.estrutura_entrada,
            distribuicoes=[],
            divergencias=None,
            errors=["MotorResult não contém DataFrame válido (esperado atributo 'df')."],
            success=False,
        )

    # Preparar tabela (pivot se Por Linha)
    df_pronto = _preparar_tabela(df, config)

    # Detectar limitadores técnicos globais
    warns_lim, errs_lim = _detectar_limitadores(df_pronto, config, motor_result)
    all_warnings.extend(warns_lim)
    all_errors.extend(errs_lim)

    # Calcular distribuição para cada par (agrupador × medida)
    distribuicoes: list[DistribuicaoPorDimensao] = []
    for agrup_config in config.agrupadores:
        for medida_config in config.medidas:
            dist, warns, errs = _calcular_distribuicao(
                df_pronto, agrup_config, medida_config, config
            )
            all_warnings.extend(warns)
            all_errors.extend(errs)
            if dist is not None:
                distribuicoes.append(dist)

    # Calcular divergências (apenas Modo 3)
    divergencias: Optional[list[DivergenciaMedida]] = None
    if config.modo == 3:
        divergencias = _calcular_divergencias(distribuicoes, config)

    return V4Result(
        modo=config.modo,
        estrutura_entrada=config.estrutura_entrada,
        distribuicoes=distribuicoes,
        divergencias=divergencias,
        warnings=all_warnings,
        errors=all_errors,
        success=len(distribuicoes) > 0,
    )
