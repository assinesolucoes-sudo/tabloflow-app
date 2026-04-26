"""
test_t_abc.py — Testes de T-ABC · classificação A/B/C · D-040
Casos: 80/95 default · threshold editado · limiares inválidos (A>=B) · classe vazia.
"""
import pandas as pd
import pytest

from transversais.t_abc import ConfigABC, aplicar_abc


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def df_acum():
    """DataFrame com participação acumulada progressiva."""
    return pd.DataFrame({
        "produto": ["P1", "P2", "P3", "P4", "P5"],
        "participacao": [50.0, 30.0, 10.0, 7.0, 3.0],
        "rank": [1, 2, 3, 4, 5],
        "participacao_acumulada": [50.0, 80.0, 90.0, 97.0, 100.0],
    })


# ---------------------------------------------------------------------------
# Classificação 80/95 default
# ---------------------------------------------------------------------------

def test_abc_default_80_95(df_acum):
    config = ConfigABC(coluna_acumulado="participacao_acumulada", coluna_rank="rank")
    df_res, result = aplicar_abc(df_acum, config, "V4", "classe")
    # P1 (50%) + P2 (80%) → A; P3 (90%) + P4 (97%) → B; P5 → C
    assert df_res.loc[df_res["produto"] == "P1", "classe"].values[0] == "A"
    assert df_res.loc[df_res["produto"] == "P2", "classe"].values[0] == "A"
    assert df_res.loc[df_res["produto"] == "P3", "classe"].values[0] == "B"
    assert df_res.loc[df_res["produto"] == "P5", "classe"].values[0] == "C"


def test_abc_contagem_por_classe(df_acum):
    config = ConfigABC(coluna_acumulado="participacao_acumulada")
    _, result = aplicar_abc(df_acum, config, "V4")
    assert result.contagem_por_classe.get("A", 0) > 0
    assert result.contagem_por_classe.get("C", 0) > 0


def test_abc_limiar_A_aplicado_corretamente(df_acum):
    config = ConfigABC(coluna_acumulado="participacao_acumulada", limiar_A=80.0, limiar_B=95.0)
    _, result = aplicar_abc(df_acum, config, "V4")
    assert result.limiar_A_aplicado == 80.0
    assert result.limiar_B_aplicado == 95.0


# ---------------------------------------------------------------------------
# Threshold editado → warning TED
# ---------------------------------------------------------------------------

def test_abc_limiar_editado_warning(df_acum):
    config = ConfigABC(coluna_acumulado="participacao_acumulada", limiar_A=70.0)
    _, result = aplicar_abc(df_acum, config, "V4")
    assert any("ABC-LIMIAR-CUSTOM" in w.codigo for w in result.warnings_gerados)


def test_abc_limiar_b_editado_warning(df_acum):
    config = ConfigABC(coluna_acumulado="participacao_acumulada", limiar_B=90.0)
    _, result = aplicar_abc(df_acum, config, "V4")
    assert any("ABC-LIMIAR-B-CUSTOM" in w.codigo for w in result.warnings_gerados)


# ---------------------------------------------------------------------------
# Limiares inválidos: limiar_A >= limiar_B → bloqueio
# ---------------------------------------------------------------------------

def test_abc_limiares_invalidos_a_maior_que_b(df_acum):
    config = ConfigABC(coluna_acumulado="participacao_acumulada", limiar_A=90.0, limiar_B=80.0)
    with pytest.raises(ValueError, match="ABC-LIMIARES-INVALIDOS"):
        aplicar_abc(df_acum, config, "V4")


def test_abc_limiares_invalidos_a_igual_b(df_acum):
    config = ConfigABC(coluna_acumulado="participacao_acumulada", limiar_A=80.0, limiar_B=80.0)
    with pytest.raises(ValueError, match="ABC-LIMIARES-INVALIDOS"):
        aplicar_abc(df_acum, config, "V4")


# ---------------------------------------------------------------------------
# Modo DICOTOMICO_V10
# ---------------------------------------------------------------------------

def test_abc_dicotomico_v10(df_acum):
    config = ConfigABC(
        coluna_acumulado="participacao_acumulada",
        limiar_A=80.0,
        modo="DICOTOMICO_V10",
    )
    df_res, result = aplicar_abc(df_acum, config, "V10", "classe_v10")
    # limiar_B deve ser fixado em 100%
    assert result.limiar_B_aplicado == 100.0
    classes = set(df_res["classe_v10"].tolist())
    assert classes.issubset({"VITAL", "DEMAIS"})


# ---------------------------------------------------------------------------
# Classe vazia → warning
# ---------------------------------------------------------------------------

def test_abc_classe_a_vazia_warning():
    """
    Distribuição onde a Classe B fica vazia:
    acumulado salta de abaixo de limiar_A direto para 100% (sem pontos entre A e B).
    """
    # P1 = 85% acumulado (ultrapassa A=80 diretamente), P2 = 100% → B fica vazia
    df = pd.DataFrame({
        "produto": ["P1", "P2"],
        "rank": [1, 2],
        "acum": [85.0, 100.0],
    })
    config = ConfigABC(coluna_acumulado="acum", limiar_A=80.0, limiar_B=95.0)
    df_res, result = aplicar_abc(df, config, "V4")
    # P1 (85%) → A; P2 (100%) → C (B vazia porque nenhum item tem acum entre 80 e 95)
    assert "classe_abc" in df_res.columns
    assert any("ABC-CLASSE-VAZIA" in w.codigo for w in result.warnings_gerados)
