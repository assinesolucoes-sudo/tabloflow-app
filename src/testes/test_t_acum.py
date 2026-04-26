"""
test_t_acum.py — Testes de T-ACUM · acumulado progressivo monotônico · E.3
Casos: monotonicidade · nulos · tolerância float · valores negativos.
"""
import pandas as pd
import pytest

from transversais.t_acum import ConfigAcum, aplicar_acumulado


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def df_com_rank():
    return pd.DataFrame({
        "produto": ["D", "C", "B", "A"],
        "participacao": [40.0, 30.0, 20.0, 10.0],
        "rank": [1, 2, 3, 4],
    })


# ---------------------------------------------------------------------------
# Monotonicidade
# ---------------------------------------------------------------------------

def test_acumulado_monotônico(df_com_rank):
    config = ConfigAcum(coluna_valor="participacao", coluna_rank="rank")
    df_res, result = aplicar_acumulado(df_com_rank, config, "V4", "acum")
    assert result.monotonicidade_verificada is True
    acum = df_res.sort_values("rank")["acum"].tolist()
    for i in range(1, len(acum)):
        assert acum[i] >= acum[i - 1] - 1e-9


def test_acumulado_soma_total(df_com_rank):
    config = ConfigAcum(coluna_valor="participacao", coluna_rank="rank")
    df_res, _ = aplicar_acumulado(df_com_rank, config, "V4", "acum")
    total = df_res.sort_values("rank")["acum"].max()
    assert abs(total - 100.0) < 1e-9


# ---------------------------------------------------------------------------
# Comportamento com nulos
# ---------------------------------------------------------------------------

def test_acumulado_com_nulos_na_participacao():
    df = pd.DataFrame({
        "produto": ["A", "B", "C"],
        "participacao": [50.0, None, 30.0],
        "rank": [1, 2, 3],
    })
    config = ConfigAcum(coluna_valor="participacao", coluna_rank="rank")
    df_res, result = aplicar_acumulado(df, config, "V4", "acum")
    # Deve executar sem erro (cumsum trata NaN como 0 por padrão em pandas)
    assert "acum" in df_res.columns


# ---------------------------------------------------------------------------
# Tolerância float
# ---------------------------------------------------------------------------

def test_acumulado_tolerancia_float():
    """Valores com ruído de ponto flutuante não devem quebrar monotonicidade."""
    df = pd.DataFrame({
        "val": [33.333333, 33.333333, 33.333334],
        "rank": [1, 2, 3],
    })
    config = ConfigAcum(coluna_valor="val", coluna_rank="rank")
    df_res, result = aplicar_acumulado(df, config, "V4")
    assert result.monotonicidade_verificada is True


# ---------------------------------------------------------------------------
# Valores negativos → warning + monotonicidade False
# ---------------------------------------------------------------------------

def test_acumulado_negativo_warning():
    df = pd.DataFrame({
        "val": [50.0, -10.0, 40.0],
        "rank": [1, 2, 3],
    })
    config = ConfigAcum(coluna_valor="val", coluna_rank="rank")
    _, result = aplicar_acumulado(df, config, "V4")
    assert result.monotonicidade_verificada is False
    assert any("ACUM-NEGATIVO" in w.codigo for w in result.warnings_gerados)


# ---------------------------------------------------------------------------
# Coluna customizada
# ---------------------------------------------------------------------------

def test_nome_coluna_customizado(df_com_rank):
    config = ConfigAcum(coluna_valor="participacao", coluna_rank="rank")
    df_res, result = aplicar_acumulado(df_com_rank, config, "V4", "part_acum")
    assert "part_acum" in df_res.columns
    assert result.coluna_acumulado_adicionada == "part_acum"
