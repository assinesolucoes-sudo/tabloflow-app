"""
test_t_diag.py — Testes de T-DIAG · coletor canônico de diagnóstico · D-017
Casos: coleta warning · coleta ajuste · coleta bloqueio escapado · consolidação ·
       ordem determinística.
"""
import pytest

from contratos import (
    AjusteMotor,
    BloqueioOperacional,
    CategoriaWarning,
    DecisaoUsuario,
    IntegridadeEstrutural,
    WarningEstrutural,
)
from transversais.t_diag import TDIAG


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def diag():
    return TDIAG("V3")


@pytest.fixture
def warning_info():
    return WarningEstrutural(
        codigo="W-V3-TEST-INFO",
        categoria=CategoriaWarning.INFORMATIVO,
        microcopy="Warning informativo de teste",
        contexto={"chave": "valor"},
    )


@pytest.fixture
def warning_alerta():
    return WarningEstrutural(
        codigo="W-V3-TEST-ALERTA",
        categoria=CategoriaWarning.ALERTA_ESTRUTURAL,
        microcopy="Warning de alerta estrutural",
        contexto={},
    )


@pytest.fixture
def ajuste():
    return AjusteMotor(
        tipo_ajuste="INTERVALO_AJUSTADO_INICIO",
        linhas_afetadas=5,
        descricao="Ajuste de intervalo inicial",
    )


@pytest.fixture
def bloqueio_escapado():
    return BloqueioOperacional(
        codigo="B-V3-INTERVALO-INVALIDO",
        condicao_disparo="Ponto inicial posterior ao final",
        escapavel=True,
        escape_acionado=True,
        contexto_disparo={"de": "dez", "ate": "jan"},
    )


# ---------------------------------------------------------------------------
# Testes básicos de registro
# ---------------------------------------------------------------------------

def test_registrar_warning(diag, warning_info):
    diag.registrar_warning(warning_info)
    diag_resultado = diag.consolidar()
    todos_warnings = [
        w for wlist in diag_resultado.warnings_por_categoria.values() for w in wlist
    ]
    assert any(w.codigo == "W-V3-TEST-INFO" for w in todos_warnings)


def test_registrar_dois_warnings(diag, warning_info, warning_alerta):
    diag.registrar_warning(warning_info)
    diag.registrar_warning(warning_alerta)
    resultado = diag.consolidar()
    todos = [w for wlist in resultado.warnings_por_categoria.values() for w in wlist]
    codigos = [w.codigo for w in todos]
    assert "W-V3-TEST-INFO" in codigos
    assert "W-V3-TEST-ALERTA" in codigos


def test_registrar_ajuste(diag, ajuste):
    diag.registrar_ajuste(ajuste)
    resultado = diag.consolidar()
    assert len(resultado.ajustes_aplicados) == 1
    assert resultado.ajustes_aplicados[0].tipo_ajuste == "INTERVALO_AJUSTADO_INICIO"
    assert resultado.ajustes_aplicados[0].linhas_afetadas == 5


def test_registrar_bloqueio_escapado(diag, bloqueio_escapado):
    diag.registrar_bloqueio_escapado(bloqueio_escapado)
    resultado = diag.consolidar()
    assert len(resultado.bloqueios_informativos) == 1
    assert resultado.bloqueios_informativos[0].escape_acionado is True


def test_registrar_decisao_usuario(diag):
    d = DecisaoUsuario(
        contexto="threshold_editado",
        valor_default=80.0,
        valor_escolhido=70.0,
    )
    diag.registrar_decisao_usuario(d)
    resultado = diag.consolidar()
    assert len(resultado.decisoes_usuario) == 1
    assert resultado.decisoes_usuario[0].valor_escolhido == 70.0


# ---------------------------------------------------------------------------
# Consolidação em DiagnosticoVN
# ---------------------------------------------------------------------------

def test_consolidar_vazio():
    diag = TDIAG("V2")
    resultado = diag.consolidar()
    assert resultado.ajustes_aplicados == []
    assert resultado.warnings_por_categoria == {}
    assert resultado.decisoes_usuario == []
    assert resultado.bloqueios_informativos == []
    assert resultado.integridade is None


def test_consolidar_com_integridade(diag):
    integ = IntegridadeEstrutural(
        total_linhas_base_original=1000,
        total_linhas_processadas=995,
        total_linhas_excluidas=5,
        motivo_exclusao_por_categoria={"nulo": 5},
    )
    diag.setar_integridade(integ)
    resultado = diag.consolidar()
    assert resultado.integridade is not None
    assert resultado.integridade.total_linhas_base_original == 1000
    assert resultado.integridade.total_linhas_excluidas == 5


def test_warnings_agrupados_por_categoria(diag, warning_info, warning_alerta):
    diag.registrar_warning(warning_info)
    diag.registrar_warning(warning_alerta)
    resultado = diag.consolidar()
    assert CategoriaWarning.INFORMATIVO.value in resultado.warnings_por_categoria
    assert CategoriaWarning.ALERTA_ESTRUTURAL.value in resultado.warnings_por_categoria


# ---------------------------------------------------------------------------
# Ordem determinística (C.1)
# ---------------------------------------------------------------------------

def test_ordem_deterministica_warnings(diag):
    """Dois warnings na mesma categoria devem aparecer na ordem de registro."""
    w1 = WarningEstrutural(
        codigo="W-PRIMEIRO",
        categoria=CategoriaWarning.INFORMATIVO,
        microcopy="Primeiro",
        contexto={},
    )
    w2 = WarningEstrutural(
        codigo="W-SEGUNDO",
        categoria=CategoriaWarning.INFORMATIVO,
        microcopy="Segundo",
        contexto={},
    )
    diag.registrar_warning(w1)
    diag.registrar_warning(w2)
    resultado = diag.consolidar()
    lista_info = resultado.warnings_por_categoria[CategoriaWarning.INFORMATIVO.value]
    assert lista_info[0].codigo == "W-PRIMEIRO"
    assert lista_info[1].codigo == "W-SEGUNDO"


def test_fabrica_warning_estatica():
    w = TDIAG.w(
        codigo="W-TEST",
        categoria=CategoriaWarning.AJUSTE_LEVE,
        microcopy="Teste de fábrica",
        campo="valor",
    )
    assert w.codigo == "W-TEST"
    assert w.contexto["campo"] == "valor"


def test_multiplas_consolidacoes_independentes():
    """Dois TDIAG distintos são independentes entre si."""
    d1 = TDIAG("V3")
    d2 = TDIAG("V4")
    d1.registrar_warning(WarningEstrutural(
        codigo="W-D1", categoria=CategoriaWarning.INFORMATIVO,
        microcopy="d1", contexto={},
    ))
    r1 = d1.consolidar()
    r2 = d2.consolidar()
    assert any("W-D1" in w.codigo for wlist in r1.warnings_por_categoria.values() for w in wlist)
    assert r2.warnings_por_categoria == {}
