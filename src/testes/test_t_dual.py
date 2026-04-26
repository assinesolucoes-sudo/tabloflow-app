"""
test_t_dual.py — Testes de T-DUAL · modo upload DUAL · D-018
Casos: 2 arquivos distintos · 1 arquivo 2 abas · validação de compatibilidade.
"""
import io

import pandas as pd
import pytest

from transversais.t_dual import ArquivoEscolhido, ConfigUploadDual, aplicar_upload_dual


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _criar_excel_bytes(dados: dict, sheet_name: str = "Sheet1") -> bytes:
    buf = io.BytesIO()
    pd.DataFrame(dados).to_excel(buf, index=False, sheet_name=sheet_name)
    return buf.getvalue()


def _criar_excel_duas_abas(dados_origem: dict, dados_comparado: dict) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        pd.DataFrame(dados_origem).to_excel(writer, sheet_name="Origem", index=False)
        pd.DataFrame(dados_comparado).to_excel(writer, sheet_name="Comparado", index=False)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Testes: 2 arquivos distintos
# ---------------------------------------------------------------------------

def test_dois_arquivos_upload_dual():
    dados = {"produto": ["A", "B"], "valor": [100, 200]}
    bytes_0 = _criar_excel_bytes(dados, "Sheet1")
    bytes_1 = _criar_excel_bytes({"produto": ["C"], "valor": [300]}, "Sheet1")

    config = ConfigUploadDual(
        estrutura="DOIS_ARQUIVOS",
        arquivo_origem=ArquivoEscolhido(indice_arquivo=0, aba_escolhida="Sheet1"),
        arquivo_comparado=ArquivoEscolhido(indice_arquivo=1, aba_escolhida="Sheet1"),
    )

    result = aplicar_upload_dual(
        config,
        arquivos_bytes={0: bytes_0, 1: bytes_1},
        nomes_arquivos={0: "base_jan.xlsx", 1: "base_fev.xlsx"},
    )

    assert result.modo_upload == "DUAL"
    assert result.arquivo_unico is None
    assert result.arquivos_dual is not None
    assert len(result.arquivos_dual) == 2

    origem = next(a for a in result.arquivos_dual if a.caminho_logico == "origem")
    comparado = next(a for a in result.arquivos_dual if a.caminho_logico == "comparado")
    assert origem.nome_arquivo == "base_jan.xlsx"
    assert comparado.nome_arquivo == "base_fev.xlsx"


def test_dois_arquivos_arquivo_bytes_preservado():
    dados = {"col": [1, 2]}
    bytes_orig = _criar_excel_bytes(dados)
    config = ConfigUploadDual(
        estrutura="DOIS_ARQUIVOS",
        arquivo_origem=ArquivoEscolhido(indice_arquivo=0, aba_escolhida="Sheet1"),
        arquivo_comparado=ArquivoEscolhido(indice_arquivo=0, aba_escolhida="Sheet1"),
    )
    result = aplicar_upload_dual(config, arquivos_bytes={0: bytes_orig})
    assert result.arquivos_dual[0].arquivo_bytes == bytes_orig


# ---------------------------------------------------------------------------
# Testes: 1 arquivo, 2 abas
# ---------------------------------------------------------------------------

def test_um_arquivo_duas_abas():
    bytes_dual = _criar_excel_duas_abas(
        {"id": [1, 2], "val": [10, 20]},
        {"id": [3, 4], "val": [30, 40]},
    )

    config = ConfigUploadDual(
        estrutura="UM_ARQUIVO_DUAS_ABAS",
        arquivo_origem=ArquivoEscolhido(indice_arquivo=0, aba_escolhida="Origem"),
        arquivo_comparado=ArquivoEscolhido(indice_arquivo=0, aba_escolhida="Comparado"),
    )

    result = aplicar_upload_dual(
        config,
        arquivos_bytes={0: bytes_dual},
        nomes_arquivos={0: "dual.xlsx"},
    )

    assert result.modo_upload == "DUAL"
    assert len(result.arquivos_dual) == 2
    abas_selecionadas = {a.aba_selecionada for a in result.arquivos_dual}
    assert "Origem" in abas_selecionadas
    assert "Comparado" in abas_selecionadas


def test_um_arquivo_duas_abas_mesma_aba_gera_warning():
    bytes_excel = _criar_excel_bytes({"val": [1]})
    config = ConfigUploadDual(
        estrutura="UM_ARQUIVO_DUAS_ABAS",
        arquivo_origem=ArquivoEscolhido(indice_arquivo=0, aba_escolhida="Sheet1"),
        arquivo_comparado=ArquivoEscolhido(indice_arquivo=0, aba_escolhida="Sheet1"),
    )
    result = aplicar_upload_dual(config, arquivos_bytes={0: bytes_excel})
    assert any(w.codigo == "W-T-DUAL-ABA-IDENTICA" for w in result.warnings)


# ---------------------------------------------------------------------------
# Validação de estrutura
# ---------------------------------------------------------------------------

def test_arquivo_faltando_levanta_valueerror():
    config = ConfigUploadDual(
        estrutura="DOIS_ARQUIVOS",
        arquivo_origem=ArquivoEscolhido(indice_arquivo=0, aba_escolhida="Sheet1"),
        arquivo_comparado=ArquivoEscolhido(indice_arquivo=1, aba_escolhida="Sheet1"),
    )
    with pytest.raises(ValueError, match="não fornecido"):
        aplicar_upload_dual(config, arquivos_bytes={0: b"fake"})


def test_rotulos_customizados_preservados():
    bytes_ = _criar_excel_bytes({"val": [1]})
    config = ConfigUploadDual(
        estrutura="DOIS_ARQUIVOS",
        arquivo_origem=ArquivoEscolhido(indice_arquivo=0, aba_escolhida="Sheet1"),
        arquivo_comparado=ArquivoEscolhido(indice_arquivo=0, aba_escolhida="Sheet1"),
        rotulo_origem="Base Jan",
        rotulo_comparado="Base Fev",
    )
    assert config.rotulo_origem == "Base Jan"
    assert config.rotulo_comparado == "Base Fev"


def test_modo_upload_sempre_dual():
    bytes_ = _criar_excel_bytes({"val": [1]})
    config = ConfigUploadDual(
        estrutura="DOIS_ARQUIVOS",
        arquivo_origem=ArquivoEscolhido(indice_arquivo=0, aba_escolhida="Sheet1"),
        arquivo_comparado=ArquivoEscolhido(indice_arquivo=0, aba_escolhida="Sheet1"),
    )
    result = aplicar_upload_dual(config, arquivos_bytes={0: bytes_})
    assert result.modo_upload == "DUAL"
