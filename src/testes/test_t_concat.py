"""
test_t_concat.py — Testes de T-CONCAT · composição declarada de campos · D-053/D-135
Casos: 3 campos · separador espaço · nulo pulado · todos nulos → string vazia + warning.
"""
import pandas as pd
import pytest

from transversais.t_concat import ConfigConcat, aplicar_concat


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def df_campos():
    return pd.DataFrame({
        "nome": ["João", "Maria", None],
        "sobrenome": ["Silva", None, "Costa"],
        "sufixo": ["Jr", "Dra", "Sr"],
    })


# ---------------------------------------------------------------------------
# 3 campos-fonte · separador espaço
# ---------------------------------------------------------------------------

def test_concat_tres_campos(df_campos):
    config = ConfigConcat(campos_fonte=["nome", "sobrenome", "sufixo"])
    df_res, result = aplicar_concat(df_campos, config, "V11", "contexto")
    assert "contexto" in df_res.columns
    # Linha 0: João Silva Jr (sem nulos)
    assert df_res["contexto"].iloc[0] == "João Silva Jr"


def test_concat_separador_espaco():
    df = pd.DataFrame({"a": ["hello"], "b": ["world"]})
    config = ConfigConcat(campos_fonte=["a", "b"])
    df_res, _ = aplicar_concat(df, config, "V11", "res")
    assert df_res["res"].iloc[0] == "hello world"


# ---------------------------------------------------------------------------
# Nulo pulado (PULAR)
# ---------------------------------------------------------------------------

def test_nulo_pulado_concatenacao(df_campos):
    config = ConfigConcat(campos_fonte=["nome", "sobrenome", "sufixo"])
    df_res, result = aplicar_concat(df_campos, config, "V11", "ctx")
    # Linha 1: Maria (sobrenome=None pulado) Dra
    assert df_res["ctx"].iloc[1] == "Maria Dra"
    # Linha 2: (nome=None pulado) Costa Sr
    assert df_res["ctx"].iloc[2] == "Costa Sr"


def test_nulo_parcial_warning(df_campos):
    config = ConfigConcat(campos_fonte=["nome", "sobrenome", "sufixo"])
    _, result = aplicar_concat(df_campos, config, "V11")
    # Linhas 1 e 2 têm nulo parcial
    assert result.valores_parcialmente_nulos >= 2
    assert any("COMP-PARCIAL" in w.codigo for w in result.warnings_gerados)


# ---------------------------------------------------------------------------
# Todos nulos → string vazia + warning
# ---------------------------------------------------------------------------

def test_todos_nulos_string_vazia():
    df = pd.DataFrame({
        "a": [None],
        "b": [None],
        "c": [None],
    })
    config = ConfigConcat(campos_fonte=["a", "b", "c"])
    df_res, result = aplicar_concat(df, config, "V11", "res")
    assert df_res["res"].iloc[0] == ""
    assert result.valores_vazios_todos_nulos == 1
    assert any("COMP-CAMPOS-NULOS" in w.codigo for w in result.warnings_gerados)


def test_alerta_sem_contexto_30_pct():
    """Mais de 30% das linhas com todos nulos dispara W-SEM-CONTEXTO."""
    df = pd.DataFrame({
        "a": [None, None, None, None, "X"],
        "b": [None, None, None, None, "Y"],
    })
    config = ConfigConcat(campos_fonte=["a", "b"])
    _, result = aplicar_concat(df, config, "V11")
    # 4/5 = 80% todos nulos > 30%
    assert any("SEM-CONTEXTO" in w.codigo for w in result.warnings_gerados)


# ---------------------------------------------------------------------------
# Normalização
# ---------------------------------------------------------------------------

def test_normalizar_true_aplica_normalizacao():
    df = pd.DataFrame({"a": ["JOÃO"], "b": ["SILVA"]})
    config = ConfigConcat(campos_fonte=["a", "b"], normalizar=True)
    df_res, _ = aplicar_concat(df, config, "V11", "res")
    assert df_res["res"].iloc[0] == "joao silva"


def test_normalizar_false_preserva_original():
    df = pd.DataFrame({"a": ["JOÃO"], "b": ["SILVA"]})
    config = ConfigConcat(campos_fonte=["a", "b"], normalizar=False)
    df_res, _ = aplicar_concat(df, config, "V11", "res")
    assert df_res["res"].iloc[0] == "JOÃO SILVA"


# ---------------------------------------------------------------------------
# Contagens
# ---------------------------------------------------------------------------

def test_valores_gerados_contagem(df_campos):
    config = ConfigConcat(campos_fonte=["nome", "sobrenome", "sufixo"])
    _, result = aplicar_concat(df_campos, config, "V11")
    # Nenhuma linha tem todos nulos nos 3 campos → 3 valores gerados
    assert result.valores_gerados == 3


def test_nome_coluna_gerado_automaticamente():
    df = pd.DataFrame({"x": ["A"], "y": ["B"]})
    config = ConfigConcat(campos_fonte=["x", "y"])
    df_res, result = aplicar_concat(df, config, "V11")
    assert result.coluna_concatenada_nome.startswith("concat_")
    assert result.coluna_concatenada_nome in df_res.columns
