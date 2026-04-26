"""
test_t_rank.py — Testes de T-RANK · ranking determinístico · D-041/D-088/D-096/D-115
Casos: default 3 níveis · V7 4 níveis (abs) · V9 4 níveis (min) · V6 4 níveis ·
       enum escopo · empate massivo.
"""
import pandas as pd
import pytest

from transversais.t_rank import (
    ConfigRank,
    CriterioDesempate,
    CriterioOrdenacao,
    aplicar_rank,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def df_rank():
    return pd.DataFrame({
        "elemento": ["A", "B", "C", "D"],
        "valor": [100.0, 200.0, 100.0, 300.0],
        "grupo": ["G1", "G1", "G2", "G2"],
        "nome": ["Alpha", "Beta", "Gamma", "Delta"],
    })


@pytest.fixture
def config_default():
    """Default 3 níveis: valor desc · concat agrupadores · ordem inserção."""
    return ConfigRank(
        escopo="global",
        criterio_primario=CriterioOrdenacao(coluna_ou_expressao="valor", direcao="decrescente"),
        regras_desempate=[
            CriterioDesempate(tipo="concatenacao_agrupadores"),
            CriterioDesempate(tipo="ordem_de_insercao"),
        ],
        agrupadores=["elemento"],
    )


# ---------------------------------------------------------------------------
# Default 3 níveis (V4)
# ---------------------------------------------------------------------------

def test_rank_default_ordena_decrescente(df_rank, config_default):
    df_res, result = aplicar_rank(df_rank, config_default, "V4", "rank_v4")
    assert "rank_v4" in df_res.columns
    # D: 300 deve ter rank menor (melhor)
    rank_d = df_res.loc[df_res["elemento"] == "D", "rank_v4"].values[0]
    rank_a = df_res.loc[df_res["elemento"] == "A", "rank_v4"].values[0]
    assert rank_d < rank_a


def test_rank_determinismo_mesma_entrada(df_rank, config_default):
    df1, _ = aplicar_rank(df_rank.copy(), config_default, "V4")
    df2, _ = aplicar_rank(df_rank.copy(), config_default, "V4")
    pd.testing.assert_series_equal(df1["rank"], df2["rank"])


# ---------------------------------------------------------------------------
# V7 · 4 níveis · abs do desvio (D-088)
# ---------------------------------------------------------------------------

def test_rank_v7_abs_desvio():
    df = pd.DataFrame({
        "elemento": ["X", "Y", "Z"],
        "desvio_percentual": [-0.5, 0.3, -0.8],
        "desvio_absoluto": [50.0, 30.0, 80.0],
        "nome_elemento": ["x", "y", "z"],
        "grupo": ["G", "G", "G"],
    })
    config = ConfigRank(
        escopo="intra_grupo",
        coluna_grupo="grupo",
        criterio_primario=CriterioOrdenacao(
            coluna_ou_expressao="desvio_percentual",
            direcao="decrescente",
            transformacao="abs",
        ),
        regras_desempate=[
            CriterioDesempate(tipo="coluna_valor", parametros={
                "coluna": "desvio_absoluto", "direcao": "decrescente", "transformacao": "abs"
            }),
            CriterioDesempate(tipo="coluna_texto_alfabetico", parametros={
                "coluna": "nome_elemento", "direcao": "crescente"
            }),
            CriterioDesempate(tipo="ordem_de_insercao"),
        ],
    )
    df_res, result = aplicar_rank(df, config, "V7", "rank_v7")
    # Z tem abs(desvio)=0.8 → rank 1; X=0.5 → rank 2; Y=0.3 → rank 3
    rank_z = df_res.loc[df_res["elemento"] == "Z", "rank_v7"].values[0]
    rank_y = df_res.loc[df_res["elemento"] == "Y", "rank_v7"].values[0]
    assert rank_z < rank_y


# ---------------------------------------------------------------------------
# V9 · metodo min (D-096)
# ---------------------------------------------------------------------------

def test_rank_v9_empate_preservado_min():
    df = pd.DataFrame({
        "id": ["A", "B", "C"],
        "score": [10.0, 10.0, 5.0],
        "nome": ["alpha", "beta", "gamma"],
    })
    config = ConfigRank(
        escopo="global",
        criterio_primario=CriterioOrdenacao(coluna_ou_expressao="score", direcao="decrescente"),
        regras_desempate=[CriterioDesempate(tipo="ordem_de_insercao")],
        metodo_rank_para_empate_preservado="min",
    )
    df_res, _ = aplicar_rank(df, config, "V9", "rank_v9")
    # A e B empatados com score 10 → ambos devem ter rank 1 ou 2 (min → ambos 1)
    rank_a = df_res.loc[df_res["id"] == "A", "rank_v9"].values[0]
    rank_b = df_res.loc[df_res["id"] == "B", "rank_v9"].values[0]
    assert rank_a == rank_b  # empate preservado


# ---------------------------------------------------------------------------
# V6 · 4 níveis · global células (D-115)
# ---------------------------------------------------------------------------

def test_rank_v6_global_celulas():
    df = pd.DataFrame({
        "eixo1": ["Cat1", "Cat1", "Cat2"],
        "eixo2": ["Sub1", "Sub2", "Sub1"],
        "medida": [50.0, 100.0, 50.0],
    })
    config = ConfigRank(
        escopo="global",
        criterio_primario=CriterioOrdenacao(coluna_ou_expressao="medida", direcao="decrescente"),
        regras_desempate=[
            CriterioDesempate(tipo="coluna_texto_alfabetico", parametros={
                "coluna": "eixo1", "direcao": "crescente"
            }),
            CriterioDesempate(tipo="coluna_texto_alfabetico", parametros={
                "coluna": "eixo2", "direcao": "crescente"
            }),
            CriterioDesempate(tipo="ordem_de_insercao"),
        ],
    )
    df_res, result = aplicar_rank(df, config, "V6", "rank_v6")
    rank_top = df_res.loc[df_res["medida"] == 100.0, "rank_v6"].values[0]
    rank_outras = df_res.loc[df_res["medida"] == 50.0, "rank_v6"].min()
    assert rank_top < rank_outras


# ---------------------------------------------------------------------------
# Escopo enum: 3 valores (D-137)
# ---------------------------------------------------------------------------

def test_escopo_global():
    config = ConfigRank(
        escopo="global",
        criterio_primario=CriterioOrdenacao(coluna_ou_expressao="valor", direcao="decrescente"),
        regras_desempate=[CriterioDesempate(tipo="ordem_de_insercao")],
    )
    assert config.escopo == "global"


def test_escopo_intra_grupo():
    config = ConfigRank(
        escopo="intra_grupo",
        criterio_primario=CriterioOrdenacao(coluna_ou_expressao="valor", direcao="decrescente"),
        regras_desempate=[CriterioDesempate(tipo="ordem_de_insercao")],
        coluna_grupo="grupo",
    )
    assert config.escopo == "intra_grupo"


def test_escopo_cross_elementos():
    config = ConfigRank(
        escopo="cross_elementos_dentro_do_agrupador",
        criterio_primario=CriterioOrdenacao(coluna_ou_expressao="valor", direcao="decrescente"),
        regras_desempate=[CriterioDesempate(tipo="ordem_de_insercao")],
        coluna_grupo="grupo",
    )
    assert config.escopo == "cross_elementos_dentro_do_agrupador"


# ---------------------------------------------------------------------------
# Empate massivo (> 50% das linhas)
# ---------------------------------------------------------------------------

def test_empate_massivo_warning():
    df = pd.DataFrame({
        "id": ["A", "B", "C", "D", "E"],
        "valor": [100.0, 100.0, 100.0, 100.0, 50.0],  # 4/5 = 80% empatados
    })
    config = ConfigRank(
        escopo="global",
        criterio_primario=CriterioOrdenacao(coluna_ou_expressao="valor", direcao="decrescente"),
        regras_desempate=[CriterioDesempate(tipo="ordem_de_insercao")],
    )
    _, result = aplicar_rank(df, config, "V6")
    assert any("EMPATE-MASSIVO" in w.codigo for w in result.warnings_gerados)
