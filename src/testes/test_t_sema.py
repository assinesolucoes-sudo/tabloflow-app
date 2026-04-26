"""
test_t_sema.py — Testes de T-SEMA · classificação semântica · D-067/D-087
Casos: contrato 1 (12 casos determinísticos) · contrato 2 (Dict + default NEUTRA).
"""
import pytest

from transversais.t_sema import ResultadoMetrica, classificar_semantica, classificar_semantica_por_metrica


# ---------------------------------------------------------------------------
# Contrato 1 · semântica única · 12 casos determinísticos
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("estrutural,semantica,esperado", [
    ("AUMENTOU", "MAIOR_MELHOR", "Melhorou"),
    ("AUMENTOU", "MENOR_MELHOR", "Piorou"),
    ("AUMENTOU", "NEUTRA", "Aumentou"),
    ("REDUZIU", "MAIOR_MELHOR", "Piorou"),
    ("REDUZIU", "MENOR_MELHOR", "Melhorou"),
    ("REDUZIU", "NEUTRA", "Reduziu"),
    ("ESTAVEL", "MAIOR_MELHOR", "Estável"),
    ("ESTAVEL", "MENOR_MELHOR", "Estável"),
    ("ESTAVEL", "NEUTRA", "Estável"),
    ("NAO_APLICAVEL", "MAIOR_MELHOR", "Não aplicável"),
    ("NAO_APLICAVEL", "MENOR_MELHOR", "Não aplicável"),
    ("NAO_APLICAVEL", "NEUTRA", "Não aplicável"),
])
def test_contrato1_tabela_deterministica(estrutural, semantica, esperado):
    resultado = classificar_semantica(estrutural, semantica)
    assert resultado == esperado


def test_contrato1_determinismo_repetido():
    """Mesma entrada → mesma saída em chamadas repetidas."""
    r1 = classificar_semantica("AUMENTOU", "MAIOR_MELHOR")
    r2 = classificar_semantica("AUMENTOU", "MAIOR_MELHOR")
    assert r1 == r2 == "Melhorou"


# ---------------------------------------------------------------------------
# Contrato 2 · semântica por métrica · D-087
# ---------------------------------------------------------------------------

def test_contrato2_dict_basico():
    resultados = {
        "vendas": ResultadoMetrica("AUMENTOU"),
        "custo": ResultadoMetrica("REDUZIU"),
    }
    semanticas = {
        "vendas": "MAIOR_MELHOR",
        "custo": "MENOR_MELHOR",
    }
    rotulos, warns = classificar_semantica_por_metrica(resultados, semanticas)
    assert rotulos["vendas"] == "Melhorou"
    assert rotulos["custo"] == "Melhorou"
    assert len(warns) == 0


def test_contrato2_default_neutra_quando_ausente():
    resultados = {
        "vendas": ResultadoMetrica("AUMENTOU"),
        "desconto": ResultadoMetrica("AUMENTOU"),
    }
    semanticas = {"vendas": "MAIOR_MELHOR"}  # desconto sem semântica
    rotulos, warns = classificar_semantica_por_metrica(resultados, semanticas)
    # desconto sem semântica → NEUTRA → "Aumentou"
    assert rotulos["desconto"] == "Aumentou"
    assert any(w.codigo == "W-T-SEMA-METRICA-SEM-SEMANTICA" for w in warns)
    assert "desconto" in warns[0].contexto["metricas"]


def test_contrato2_todas_sem_semantica():
    resultados = {"m1": ResultadoMetrica("ESTAVEL"), "m2": ResultadoMetrica("REDUZIU")}
    rotulos, warns = classificar_semantica_por_metrica(resultados, {})
    assert rotulos["m1"] == "Estável"
    assert rotulos["m2"] == "Reduziu"
    assert any(w.codigo == "W-T-SEMA-METRICA-SEM-SEMANTICA" for w in warns)


def test_contrato2_sem_warning_quando_todas_declaradas():
    resultados = {"m1": ResultadoMetrica("ESTAVEL")}
    rotulos, warns = classificar_semantica_por_metrica(resultados, {"m1": "NEUTRA"})
    assert rotulos["m1"] == "Estável"
    assert len(warns) == 0


def test_contrato2_ordem_deterministica():
    """Métricas sem semântica listadas em ordem estável no warning."""
    resultados = {
        "zz": ResultadoMetrica("AUMENTOU"),
        "aa": ResultadoMetrica("REDUZIU"),
        "mm": ResultadoMetrica("ESTAVEL"),
    }
    _, warns = classificar_semantica_por_metrica(resultados, {})
    metricas_no_warning = warns[0].contexto["metricas"]
    assert metricas_no_warning == sorted(["zz", "aa", "mm"])
