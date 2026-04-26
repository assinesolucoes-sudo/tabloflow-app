"""
test_t_eixo.py — Testes de T-EIXO · eixo sequencial ordenado · D-061
Casos: TEMPORAL mês pt-BR · ORDINAL com prefixo · MANUAL fallback · lacuna ·
       intervalo declarado vs efetivo · bloqueio De > Até.
"""
import pandas as pd
import pytest

from transversais.t_eixo import ConfigEixo, IntervaloEixo, aplicar_eixo, inferir_tipo_eixo


# ---------------------------------------------------------------------------
# Inferência de tipo
# ---------------------------------------------------------------------------

def test_inferir_temporal_meses_pt():
    valores = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    tipo, confianca = inferir_tipo_eixo(valores)
    assert tipo == "TEMPORAL"
    assert confianca >= 0.80


def test_inferir_ordinal_com_prefixo():
    valores = ["Etapa 1", "Etapa 2", "Etapa 3", "Etapa 4", "Etapa 5"]
    tipo, confianca = inferir_tipo_eixo(valores)
    assert tipo == "ORDINAL"
    assert confianca >= 0.80


def test_inferir_manual_fallback():
    valores = ["Alpha", "Beta", "Gamma", "Delta"]
    tipo, confianca = inferir_tipo_eixo(valores)
    assert tipo == "MANUAL"


def test_inferir_vazio_retorna_manual():
    tipo, confianca = inferir_tipo_eixo([])
    assert tipo == "MANUAL"
    assert confianca == 0.0


# ---------------------------------------------------------------------------
# Aplicação de eixo TEMPORAL
# ---------------------------------------------------------------------------

def test_eixo_temporal_coluna_ordem_adicionada():
    df = pd.DataFrame({
        "mes": ["jan", "fev", "mar", "abr"],
        "valor": [10, 20, 30, 40],
    })
    config = ConfigEixo(
        coluna_eixo="mes",
        tipo_declarado="TEMPORAL",
        ordem_aplicada=["jan", "fev", "mar", "abr"],
        intervalo_declarado=IntervaloEixo(de="jan", ate="abr"),
    )
    df_res, result = aplicar_eixo(df, config, "V3")
    assert "_ordem_eixo" in df_res.columns
    assert df_res.loc[df_res["mes"] == "jan", "_ordem_eixo"].values[0] == 1
    assert df_res.loc[df_res["mes"] == "abr", "_ordem_eixo"].values[0] == 4


def test_eixo_temporal_tipo_aplicado():
    df = pd.DataFrame({"mes": ["jan", "fev"], "val": [1, 2]})
    config = ConfigEixo(
        coluna_eixo="mes",
        tipo_declarado="TEMPORAL",
        ordem_aplicada=["jan", "fev"],
        intervalo_declarado=IntervaloEixo(de="jan", ate="fev"),
    )
    _, result = aplicar_eixo(df, config, "V3")
    assert result.tipo_aplicado == "TEMPORAL"


# ---------------------------------------------------------------------------
# Aplicação de eixo ORDINAL com prefixo
# ---------------------------------------------------------------------------

def test_eixo_ordinal_prefixo():
    df = pd.DataFrame({
        "etapa": ["Etapa 1", "Etapa 2", "Etapa 3"],
        "val": [10, 20, 30],
    })
    config = ConfigEixo(
        coluna_eixo="etapa",
        tipo_declarado="ORDINAL",
        ordem_aplicada=["Etapa 1", "Etapa 2", "Etapa 3"],
        intervalo_declarado=IntervaloEixo(de="Etapa 1", ate="Etapa 3"),
    )
    df_res, result = aplicar_eixo(df, config, "V3")
    assert result.tipo_aplicado == "ORDINAL"
    assert "_ordem_eixo" in df_res.columns


def test_eixo_ordinal_detecta_lacuna():
    df = pd.DataFrame({
        "etapa": ["Etapa 1", "Etapa 3"],  # lacuna na Etapa 2
        "val": [10, 30],
    })
    config = ConfigEixo(
        coluna_eixo="etapa",
        tipo_declarado="ORDINAL",
        ordem_aplicada=["Etapa 1", "Etapa 2", "Etapa 3"],
        intervalo_declarado=IntervaloEixo(de="Etapa 1", ate="Etapa 3"),
    )
    _, result = aplicar_eixo(df, config, "V3")
    assert result.deteccao_de_lacuna_disponivel is True
    assert "2" in result.pontos_ausentes_detectados


# ---------------------------------------------------------------------------
# Aplicação de eixo MANUAL
# ---------------------------------------------------------------------------

def test_eixo_manual_sem_deteccao_lacuna():
    df = pd.DataFrame({"cat": ["Alpha", "Beta", "Gamma"], "val": [1, 2, 3]})
    config = ConfigEixo(
        coluna_eixo="cat",
        tipo_declarado="MANUAL",
        ordem_aplicada=["Alpha", "Beta", "Gamma"],
        intervalo_declarado=IntervaloEixo(de="Alpha", ate="Gamma"),
    )
    _, result = aplicar_eixo(df, config, "V3")
    assert result.deteccao_de_lacuna_disponivel is False
    assert result.pontos_ausentes_detectados == []


# ---------------------------------------------------------------------------
# Intervalo declarado vs efetivo com ajuste-limite
# ---------------------------------------------------------------------------

def test_intervalo_ajuste_inicio_warning():
    """Ponto 'jan' declarado não está na base → ajuste com warning."""
    df = pd.DataFrame({"mes": ["fev", "mar", "abr"], "val": [1, 2, 3]})
    config = ConfigEixo(
        coluna_eixo="mes",
        tipo_declarado="MANUAL",
        ordem_aplicada=["jan", "fev", "mar", "abr"],
        intervalo_declarado=IntervaloEixo(de="jan", ate="abr"),
    )
    _, result = aplicar_eixo(df, config, "V3")
    assert result.intervalo_efetivo.de == "fev"
    assert any("AJUSTE-INICIO" in w.codigo for w in result.warnings_gerados)


# ---------------------------------------------------------------------------
# Bloqueio De > Até
# ---------------------------------------------------------------------------

def test_bloqueio_de_maior_que_ate():
    df = pd.DataFrame({"mes": ["jan", "fev", "mar"], "val": [1, 2, 3]})
    config = ConfigEixo(
        coluna_eixo="mes",
        tipo_declarado="MANUAL",
        ordem_aplicada=["jan", "fev", "mar"],
        intervalo_declarado=IntervaloEixo(de="mar", ate="jan"),  # Invertido
    )
    with pytest.raises(ValueError, match="INTERVALO-INVALIDO"):
        aplicar_eixo(df, config, "V3")


# ---------------------------------------------------------------------------
# _ordem_eixo = -1 para pontos fora do intervalo
# ---------------------------------------------------------------------------

def test_pontos_fora_intervalo_recebem_menos_1():
    df = pd.DataFrame({"mes": ["jan", "fev", "mar", "abr"], "val": [1, 2, 3, 4]})
    config = ConfigEixo(
        coluna_eixo="mes",
        tipo_declarado="MANUAL",
        ordem_aplicada=["jan", "fev", "mar", "abr"],
        intervalo_declarado=IntervaloEixo(de="fev", ate="mar"),
    )
    df_res, _ = aplicar_eixo(df, config, "V3")
    assert df_res.loc[df_res["mes"] == "jan", "_ordem_eixo"].values[0] == -1
    assert df_res.loc[df_res["mes"] == "abr", "_ordem_eixo"].values[0] == -1
    assert df_res.loc[df_res["mes"] == "fev", "_ordem_eixo"].values[0] == 1
