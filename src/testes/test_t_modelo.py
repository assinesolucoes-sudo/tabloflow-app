"""
test_t_modelo.py — Testes de T-MODELO · persistência de configuração · D-015/D-046
Casos: salvar · aplicar base compatível · aplicar parcialmente incompatível ·
       aplicar visão incompatível · threshold fora do range.
"""
import pytest

from contratos import ArquivoInfo, UploadResult
from transversais.t_modelo import (
    ModeloConfig,
    ThresholdEditavel,
    aplicar_modelo,
    limpar_store,
    listar_modelos_aplicaveis,
    salvar_modelo,
)


# ---------------------------------------------------------------------------
# Setup / Teardown
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def limpa_store():
    limpar_store()
    yield
    limpar_store()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def modelo_v4():
    return ModeloConfig(
        nome_modelo="Modelo Vendas V4",
        visao_origem="V4",
        agrupadores=["produto", "regiao"],
        campos_principais={"medida": "valor_vendas"},
        thresholds_editaveis={
            "limiar_A": ThresholdEditavel(
                valor_default=80.0,
                valor_atual=80.0,
                range_permitido=(50.0, 95.0),
                unidade="percentual",
                descricao_uso="Limiar de Classe A",
            )
        },
    )


@pytest.fixture
def upload_compativel():
    """Upload com colunas que casam com o modelo."""
    info = ArquivoInfo(
        caminho_logico="unico",
        nome_arquivo="base.xlsx",
        arquivo_bytes=b"fake",
        abas_disponiveis=[],
        aba_selecionada="",
        formato="xlsx",
        preview={"produto": ["A"], "regiao": ["Norte"], "valor_vendas": [100]},
    )
    return UploadResult(
        file_name="base.xlsx",
        modo_upload="SIMPLES",
        arquivo_unico=info,
    )


@pytest.fixture
def upload_parcial():
    """Upload onde 'regiao' não existe."""
    info = ArquivoInfo(
        caminho_logico="unico",
        nome_arquivo="base2.xlsx",
        arquivo_bytes=b"fake",
        abas_disponiveis=[],
        aba_selecionada="",
        formato="xlsx",
        preview={"produto": ["A"], "valor_vendas": [100]},
    )
    return UploadResult(
        file_name="base2.xlsx",
        modo_upload="SIMPLES",
        arquivo_unico=info,
    )


# ---------------------------------------------------------------------------
# Salvar
# ---------------------------------------------------------------------------

def test_salvar_retorna_id(modelo_v4):
    modelo_id = salvar_modelo(modelo_v4)
    assert isinstance(modelo_id, str)
    assert len(modelo_id) > 0


def test_salvar_multiplos_ids_distintos(modelo_v4):
    id1 = salvar_modelo(modelo_v4)
    id2 = salvar_modelo(modelo_v4)
    assert id1 != id2


# ---------------------------------------------------------------------------
# Aplicar em base compatível
# ---------------------------------------------------------------------------

def test_aplicar_base_compativel(modelo_v4, upload_compativel):
    modelo_id = salvar_modelo(modelo_v4)
    config, warns = aplicar_modelo(modelo_id, "V4", upload_compativel)
    assert len(warns) == 0
    assert config["agrupadores"] == ["produto", "regiao"]
    assert config["campos_principais"]["medida"] == "valor_vendas"


# ---------------------------------------------------------------------------
# Aplicar em base parcialmente incompatível → warning
# ---------------------------------------------------------------------------

def test_aplicar_base_parcialmente_incompativel(modelo_v4, upload_parcial):
    modelo_id = salvar_modelo(modelo_v4)
    config, warns = aplicar_modelo(modelo_id, "V4", upload_parcial)
    assert any("MOD-PARCIAL" in w.codigo for w in warns)
    assert "regiao" in config["campos_incompativeis"]


# ---------------------------------------------------------------------------
# Aplicar em visão incompatível → bloqueio
# ---------------------------------------------------------------------------

def test_aplicar_visao_incompativel_levanta_valueerror(modelo_v4):
    modelo_id = salvar_modelo(modelo_v4)
    with pytest.raises(ValueError, match="ESTRUTURA-INCOMPATIVEL"):
        aplicar_modelo(modelo_id, "V7")  # V4 ↔ V7 não é view especializada


# ---------------------------------------------------------------------------
# Cross-visão permitida: V4 ↔ V10
# ---------------------------------------------------------------------------

def test_cross_visao_v4_para_v10(modelo_v4):
    modelo_id = salvar_modelo(modelo_v4)
    config, warns = aplicar_modelo(modelo_id, "V10")
    # Deve funcionar com warning de cross-visão
    assert any("CROSS-VISAO" in w.codigo for w in warns)


def test_cross_visao_v10_para_v4():
    modelo_v10 = ModeloConfig(
        nome_modelo="Pareto Padrão",
        visao_origem="V10",
        thresholds_editaveis={},
    )
    modelo_id = salvar_modelo(modelo_v10)
    config, warns = aplicar_modelo(modelo_id, "V4")
    assert any("CROSS-VISAO" in w.codigo for w in warns)


# ---------------------------------------------------------------------------
# Threshold fora do range → reset ao default
# ---------------------------------------------------------------------------

def test_threshold_fora_range_warning():
    modelo = ModeloConfig(
        nome_modelo="Modelo threshold fora",
        visao_origem="V4",
        thresholds_editaveis={
            "limiar_A": ThresholdEditavel(
                valor_default=80.0,
                valor_atual=99.0,  # fora do range [50, 95]
                range_permitido=(50.0, 95.0),
                descricao_uso="Limiar A",
            )
        },
    )
    modelo_id = salvar_modelo(modelo)
    config, warns = aplicar_modelo(modelo_id, "V4")
    assert any("THRESHOLD-FORA-RANGE" in w.codigo for w in warns)
    # Threshold deve ter sido resetado para o default
    thr = config["thresholds_editaveis"]["limiar_A"]
    assert thr["valor_atual"] == 80.0


# ---------------------------------------------------------------------------
# Listar modelos aplicáveis
# ---------------------------------------------------------------------------

def test_listar_modelos_aplicaveis_filtra_por_visao(modelo_v4):
    id_v4 = salvar_modelo(modelo_v4)
    modelo_v3 = ModeloConfig(nome_modelo="Modelo V3", visao_origem="V3")
    salvar_modelo(modelo_v3)

    modelos_v4 = listar_modelos_aplicaveis("V4")
    assert all(m.visao_origem in ("V4", "V10") for m in modelos_v4)
    assert any(m.nome_modelo == "Modelo Vendas V4" for m in modelos_v4)


def test_modelo_inexistente_levanta_keyerror():
    with pytest.raises(KeyError):
        aplicar_modelo("id-inexistente", "V4")
