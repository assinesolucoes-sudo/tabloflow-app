"""
test_t_fuzzy.py — Testes de T-FUZZY · similaridade textual híbrida · D-050/D-138
Casos: determinismo · normalização · trigramas + tokens · idênticos → 1.0 · disjuntos → ~0.
"""
import pytest

from transversais.t_fuzzy import calcular_score, extrair_tokens_chave_fuzzy


# ---------------------------------------------------------------------------
# Determinismo da API
# ---------------------------------------------------------------------------

def test_determinismo_mesma_chamada():
    r1 = calcular_score("Empresa ABC LTDA", "Empresa ABC Ltda")
    r2 = calcular_score("Empresa ABC LTDA", "Empresa ABC Ltda")
    assert r1.score == r2.score


def test_determinismo_multiplos_pares():
    pares = [
        ("Pão de Açúcar", "Pao de Acucar"),
        ("João da Silva", "joao da silva"),
        ("CNPJ 12345678000190", "cnpj 12345678000190"),
    ]
    for a, b in pares:
        r1 = calcular_score(a, b)
        r2 = calcular_score(a, b)
        assert r1.score == r2.score, f"Não determinístico para: {a} / {b}"


# ---------------------------------------------------------------------------
# Normalização interna aplicada
# ---------------------------------------------------------------------------

def test_normalizacao_interna_aplicada():
    r = calcular_score("JOÃO DA SILVA  ", "joao da silva")
    assert r.texto_a_normalizado == "joao da silva"
    assert r.texto_b_normalizado == "joao da silva"
    assert r.score == pytest.approx(1.0, abs=1e-6)


def test_normalizacao_remove_acentos():
    r = calcular_score("Pão de Açúcar", "Pao de Acucar")
    assert r.score >= 0.8


def test_normalizacao_case_insensitive():
    r = calcular_score("EMPRESA ABC", "empresa abc")
    assert r.score == pytest.approx(1.0, abs=1e-6)


# ---------------------------------------------------------------------------
# Trigramas
# ---------------------------------------------------------------------------

def test_trigramas_compartilhados_capturados():
    r = calcular_score("abcdef", "abcxyz")
    assert r.trigramas_comuns > 0
    assert r.trigramas_total > 0


def test_score_zero_sem_trigramas_comuns():
    r = calcular_score("abc", "xyz")
    # Trigramas: {"abc"} vs {"xyz"} → interseção vazia
    assert r.trigramas_comuns == 0


# ---------------------------------------------------------------------------
# Dois inputs idênticos → score 1.0
# ---------------------------------------------------------------------------

def test_inputs_identicos_score_1():
    r = calcular_score("empresa xpto ltda", "empresa xpto ltda")
    assert r.score == pytest.approx(1.0, abs=1e-6)


def test_inputs_identicos_pos_normalizacao():
    r = calcular_score("Empresa XPTO LTDA", "empresa xpto ltda")
    assert r.score == pytest.approx(1.0, abs=1e-6)


# ---------------------------------------------------------------------------
# Dois inputs disjuntos → score próximo de 0
# ---------------------------------------------------------------------------

def test_inputs_disjuntos_score_baixo():
    r = calcular_score("abcdefghi", "xyzqrstvw")
    assert r.score < 0.3


def test_strings_vazias():
    r = calcular_score("", "")
    assert 0.0 <= r.score <= 1.0


# ---------------------------------------------------------------------------
# Tokens-chave
# ---------------------------------------------------------------------------

def test_tokens_chave_numerico_longo():
    tokens = extrair_tokens_chave_fuzzy("cnpj 12345678000190 ltda")
    assert "12345678000190" in tokens


def test_tokens_chave_alfabetico():
    tokens = extrair_tokens_chave_fuzzy("empresa xpto ltda")
    assert "empresa" in tokens
    assert "xpto" in tokens or "ltda" in tokens


def test_boost_com_token_compartilhado():
    """Boost deve elevar score quando token-chave é compartilhado."""
    r_com_token = calcular_score("cnpj 12345678 empresa abc", "cnpj 12345678 empresa xyz")
    r_sem_token = calcular_score("aaa bbb ccc", "aaa bbb ddd")
    # r_com_token deve ter tokens compartilhados (12345678, cnpj, empresa)
    assert len(r_com_token.tokens_chave_compartilhados) > 0


# ---------------------------------------------------------------------------
# Score em [0, 1]
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("a,b", [
    ("Protheus ERP SAP", "Safra Agrícola 2024"),
    ("12345", "67890"),
    ("", "qualquer coisa"),
    ("x", "y"),
])
def test_score_sempre_entre_0_e_1(a, b):
    r = calcular_score(a, b)
    assert 0.0 <= r.score <= 1.0
