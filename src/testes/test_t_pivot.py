"""
test_t_pivot.py — Testes de T-PIVOT · pivot 3 semânticas · D-026/D-039/D-062
Casos: ESTADOS_EMPILHADOS (V2) · MULTI_MEDIDA (V4) · PONTOS_DO_EIXO (V3 ≥ 10).
"""
import pandas as pd
import pytest

from transversais.t_pivot import ConfigPivot, aplicar_pivot


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def df_estados():
    """V2 estados empilhados: Jan/24 vs Jan/25 para mesma medida."""
    return pd.DataFrame({
        "produto": ["A", "A", "B", "B"],
        "periodo": ["Jan/24", "Jan/25", "Jan/24", "Jan/25"],
        "valor": [100.0, 120.0, 200.0, 180.0],
    })


@pytest.fixture
def df_medidas():
    """V4 multi-medida: Receita / Custo / Margem."""
    return pd.DataFrame({
        "produto": ["A", "A", "A", "B", "B", "B"],
        "tipo_medida": ["Receita", "Custo", "Margem", "Receita", "Custo", "Margem"],
        "valor": [1000.0, 600.0, 400.0, 500.0, 300.0, 200.0],
    })


@pytest.fixture
def df_eixo_10_pontos():
    """V3 pontos-do-eixo com 10+ pontos."""
    meses = [f"M{i:02d}" for i in range(1, 13)]  # M01..M12
    return pd.DataFrame({
        "categoria": ["Cat1"] * 12 + ["Cat2"] * 12,
        "mes": meses * 2,
        "valor": list(range(1, 13)) + list(range(13, 25)),
    })


# ---------------------------------------------------------------------------
# Semântica 1: ESTADOS_EMPILHADOS
# ---------------------------------------------------------------------------

def test_pivot_estados_empilhados(df_estados):
    config = ConfigPivot(
        semantica="ESTADOS_EMPILHADOS",
        coluna_discriminadora="periodo",
        coluna_valor_a_agregar="valor",
        agrupadores=["produto"],
    )
    df_piv, result = aplicar_pivot(df_estados, config, "V2")
    assert "Jan/24" in result.colunas_geradas
    assert "Jan/25" in result.colunas_geradas
    # Produto A: Jan/24=100 Jan/25=120
    linha_a = df_piv[df_piv["produto"] == "A"]
    assert abs(linha_a["Jan/24"].values[0] - 100.0) < 1e-9
    assert abs(linha_a["Jan/25"].values[0] - 120.0) < 1e-9


def test_pivot_estados_sem_colisao(df_estados):
    config = ConfigPivot(
        semantica="ESTADOS_EMPILHADOS",
        coluna_discriminadora="periodo",
        coluna_valor_a_agregar="valor",
        agrupadores=["produto"],
    )
    _, result = aplicar_pivot(df_estados, config, "V2")
    assert result.linhas_colidas_consolidadas == 0


# ---------------------------------------------------------------------------
# Semântica 2: MULTI_MEDIDA
# ---------------------------------------------------------------------------

def test_pivot_multi_medida(df_medidas):
    config = ConfigPivot(
        semantica="MULTI_MEDIDA",
        coluna_discriminadora="tipo_medida",
        coluna_valor_a_agregar="valor",
        agrupadores=["produto"],
    )
    df_piv, result = aplicar_pivot(df_medidas, config, "V4")
    assert set(result.colunas_geradas) == {"Receita", "Custo", "Margem"}
    linha_a = df_piv[df_piv["produto"] == "A"]
    assert abs(linha_a["Receita"].values[0] - 1000.0) < 1e-9


def test_pivot_multi_medida_valores_selecionados(df_medidas):
    config = ConfigPivot(
        semantica="MULTI_MEDIDA",
        coluna_discriminadora="tipo_medida",
        valores_selecionados=["Receita", "Custo"],
        coluna_valor_a_agregar="valor",
        agrupadores=["produto"],
    )
    df_piv, result = aplicar_pivot(df_medidas, config, "V4")
    assert set(result.colunas_geradas) == {"Receita", "Custo"}
    assert "Margem" in result.valores_nao_pivotados
    assert any("NAO-SELECIONADOS" in w.codigo for w in result.warnings_gerados)


# ---------------------------------------------------------------------------
# Semântica 3: PONTOS_DO_EIXO
# ---------------------------------------------------------------------------

def test_pivot_pontos_eixo_10_pontos(df_eixo_10_pontos):
    config = ConfigPivot(
        semantica="PONTOS_DO_EIXO",
        coluna_discriminadora="mes",
        coluna_valor_a_agregar="valor",
        agrupadores=["categoria"],
        threshold_cardinalidade_eixo=10,
    )
    df_piv, result = aplicar_pivot(df_eixo_10_pontos, config, "V3")
    assert len(result.colunas_geradas) == 12  # M01..M12
    assert len(df_piv) == 2  # Cat1 e Cat2


def test_pivot_cardinalidade_alta_warning():
    """Mais de 50 valores únicos dispara warning de alta cardinalidade."""
    meses = [f"M{i:03d}" for i in range(1, 52)]  # 51 meses
    df = pd.DataFrame({
        "cat": ["X"] * 51,
        "mes": meses,
        "valor": list(range(51)),
    })
    config = ConfigPivot(
        semantica="PONTOS_DO_EIXO",
        coluna_discriminadora="mes",
        coluna_valor_a_agregar="valor",
        agrupadores=["cat"],
    )
    _, result = aplicar_pivot(df, config, "V3")
    assert any("CARDINALIDADE-ALTA" in w.codigo for w in result.warnings_gerados)
