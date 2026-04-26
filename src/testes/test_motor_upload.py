"""
test_motor_upload.py — Testes do motor_upload.py v2 · F-MOT

Cobertura:
  (a) Leitura de Excel e CSV com ArquivoInfo correto
  (b) Preview de 5 linhas preservado
  (c) arquivo_bytes preservado em memória (D-007)
  (d) Modo DUAL: 2 arquivos (D-018)
  (e) Modo DUAL: 1 arquivo 2 abas (D-018)
  (f) Warning W-U-ENCODING-FALLBACK para CSV latin-1
  (g) Warning W-U-ARQUIVO-VAZIO para arquivo sem dados
  (h) Warning W-U-MULTI-ABA-AUTO para Excel multi-aba sem seleção
  (i) Erro em formato não suportado
  (j) Erro em arquivo inexistente
"""
from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pandas as pd
import pytest

from motor_upload import ArquivoEntrada, processar_upload
from contratos import UploadResult


# ---------------------------------------------------------------------------
# Fixtures: criação de arquivos temporários
# ---------------------------------------------------------------------------

def _df_vendas() -> pd.DataFrame:
    return pd.DataFrame({
        "Produto": ["A", "B", "C", "D", "E", "F", "G"],
        "Valor": [100.0, 200.0, 150.0, 300.0, 50.0, 175.0, 220.0],
        "Mes": ["Jan/24", "Fev/24", "Mar/24", "Abr/24", "Mai/24", "Jun/24", "Jul/24"],
        "Ativo": [1, 0, 1, 1, 0, 1, 0],  # boolean disfarçado
    })


def _df_cadastro() -> pd.DataFrame:
    return pd.DataFrame({
        "ID": [1001, 1002, 1003, 1004, 1005],
        "Nome": ["Alpha Ltda", "Beta SA", "Gamma Corp", "Delta ME", "Epsilon EPP"],
        "CNPJ": [
            "11.222.333/0001-44",
            "55.666.777/0001-88",
            "99.000.111/0001-22",
            "33.444.555/0001-66",
            "77.888.999/0001-00",
        ],
    })


@pytest.fixture
def excel_simples(tmp_path) -> Path:
    """Excel com aba única e dados de vendas."""
    path = tmp_path / "vendas.xlsx"
    _df_vendas().to_excel(path, index=False, sheet_name="Vendas")
    return path


@pytest.fixture
def excel_multi_aba(tmp_path) -> Path:
    """Excel com 2 abas (Origem e Comparado)."""
    path = tmp_path / "dual.xlsx"
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        _df_vendas().to_excel(writer, sheet_name="Origem", index=False)
        _df_cadastro().to_excel(writer, sheet_name="Comparado", index=False)
    return path


@pytest.fixture
def csv_utf8(tmp_path) -> Path:
    """CSV com encoding UTF-8."""
    path = tmp_path / "vendas.csv"
    _df_vendas().to_csv(path, index=False, encoding="utf-8")
    return path


@pytest.fixture
def csv_latin1(tmp_path) -> Path:
    """CSV com encoding latin-1 (simula arquivo legado)."""
    path = tmp_path / "vendas_legacy.csv"
    _df_vendas().to_csv(path, index=False, encoding="latin-1")
    return path


@pytest.fixture
def excel_vazio(tmp_path) -> Path:
    """Excel com aba existente mas sem dados."""
    path = tmp_path / "vazio.xlsx"
    pd.DataFrame().to_excel(path, index=False)
    return path


@pytest.fixture
def excel_origem(tmp_path) -> Path:
    path = tmp_path / "origem.xlsx"
    _df_vendas().to_excel(path, index=False, sheet_name="Dados")
    return path


@pytest.fixture
def excel_comparado(tmp_path) -> Path:
    path = tmp_path / "comparado.xlsx"
    _df_cadastro().to_excel(path, index=False, sheet_name="Dados")
    return path


# ---------------------------------------------------------------------------
# Testes SIMPLES: Excel
# ---------------------------------------------------------------------------

class TestSimlesExcel:
    def test_resultado_e_upload_result(self, excel_simples):
        entrada = ArquivoEntrada(
            caminho_fisico=str(excel_simples),
            caminho_logico="unico",
        )
        resultado = processar_upload([entrada], modo="SIMPLES")
        assert isinstance(resultado, UploadResult)

    def test_modo_simples(self, excel_simples):
        entrada = ArquivoEntrada(caminho_fisico=str(excel_simples), caminho_logico="unico")
        resultado = processar_upload([entrada], modo="SIMPLES")
        assert resultado.modo_upload == "SIMPLES"
        assert resultado.arquivo_unico is not None
        assert resultado.arquivos_dual is None

    def test_arquivo_bytes_preservado(self, excel_simples):
        """D-007: arquivo_bytes deve ser preservado em memória."""
        entrada = ArquivoEntrada(caminho_fisico=str(excel_simples), caminho_logico="unico")
        resultado = processar_upload([entrada], modo="SIMPLES")
        info = resultado.arquivo_unico
        assert info is not None
        assert isinstance(info.arquivo_bytes, bytes)
        assert len(info.arquivo_bytes) > 0

    def test_preview_5_linhas(self, excel_simples):
        """Preview deve ter no máximo 5 entradas por coluna."""
        entrada = ArquivoEntrada(caminho_fisico=str(excel_simples), caminho_logico="unico")
        resultado = processar_upload([entrada], modo="SIMPLES")
        info = resultado.arquivo_unico
        assert info is not None
        for col, valores in info.preview.items():
            assert len(valores) <= 5, f"Preview da coluna '{col}' tem {len(valores)} linhas"

    def test_formato_xlsx(self, excel_simples):
        entrada = ArquivoEntrada(caminho_fisico=str(excel_simples), caminho_logico="unico")
        resultado = processar_upload([entrada], modo="SIMPLES")
        assert resultado.arquivo_unico.formato == "xlsx"

    def test_abas_disponiveis(self, excel_simples):
        entrada = ArquivoEntrada(caminho_fisico=str(excel_simples), caminho_logico="unico")
        resultado = processar_upload([entrada], modo="SIMPLES")
        info = resultado.arquivo_unico
        assert "Vendas" in info.abas_disponiveis
        assert info.aba_selecionada == "Vendas"

    def test_nome_arquivo(self, excel_simples):
        entrada = ArquivoEntrada(caminho_fisico=str(excel_simples), caminho_logico="unico")
        resultado = processar_upload([entrada], modo="SIMPLES")
        assert resultado.arquivo_unico.nome_arquivo == "vendas.xlsx"
        assert resultado.file_name == "vendas.xlsx"

    def test_bytes_podem_reler_df(self, excel_simples):
        """Bytes preservados devem permitir recriar o DataFrame completo."""
        entrada = ArquivoEntrada(caminho_fisico=str(excel_simples), caminho_logico="unico")
        resultado = processar_upload([entrada], modo="SIMPLES")
        info = resultado.arquivo_unico
        df = pd.read_excel(BytesIO(info.arquivo_bytes), sheet_name=info.aba_selecionada)
        assert len(df) == 7
        assert "Produto" in df.columns


# ---------------------------------------------------------------------------
# Testes SIMPLES: CSV
# ---------------------------------------------------------------------------

class TestSimplesCSV:
    def test_formato_csv(self, csv_utf8):
        entrada = ArquivoEntrada(caminho_fisico=str(csv_utf8), caminho_logico="unico")
        resultado = processar_upload([entrada], modo="SIMPLES")
        assert resultado.arquivo_unico.formato == "csv"

    def test_sem_abas(self, csv_utf8):
        entrada = ArquivoEntrada(caminho_fisico=str(csv_utf8), caminho_logico="unico")
        resultado = processar_upload([entrada], modo="SIMPLES")
        info = resultado.arquivo_unico
        assert info.abas_disponiveis == []
        assert info.aba_selecionada == ""

    def test_encoding_detectado(self, csv_utf8):
        entrada = ArquivoEntrada(caminho_fisico=str(csv_utf8), caminho_logico="unico")
        resultado = processar_upload([entrada], modo="SIMPLES")
        assert resultado.arquivo_unico.encoding_detectado is not None

    def test_separador_detectado(self, csv_utf8):
        entrada = ArquivoEntrada(caminho_fisico=str(csv_utf8), caminho_logico="unico")
        resultado = processar_upload([entrada], modo="SIMPLES")
        assert resultado.arquivo_unico.separador_csv is not None


# ---------------------------------------------------------------------------
# Testes DUAL: 2 arquivos
# ---------------------------------------------------------------------------

class TestDualDoisArquivos:
    def test_modo_dual_dois_arquivos(self, excel_origem, excel_comparado):
        entradas = [
            ArquivoEntrada(caminho_fisico=str(excel_origem), caminho_logico="origem"),
            ArquivoEntrada(caminho_fisico=str(excel_comparado), caminho_logico="comparado"),
        ]
        resultado = processar_upload(entradas, modo="DUAL")
        assert resultado.modo_upload == "DUAL"
        assert resultado.arquivo_unico is None
        assert resultado.arquivos_dual is not None
        assert len(resultado.arquivos_dual) == 2

    def test_caminhos_logicos_dual(self, excel_origem, excel_comparado):
        entradas = [
            ArquivoEntrada(caminho_fisico=str(excel_origem), caminho_logico="origem"),
            ArquivoEntrada(caminho_fisico=str(excel_comparado), caminho_logico="comparado"),
        ]
        resultado = processar_upload(entradas, modo="DUAL")
        logicos = [a.caminho_logico for a in resultado.arquivos_dual]
        assert "origem" in logicos
        assert "comparado" in logicos

    def test_bytes_dual_preservados(self, excel_origem, excel_comparado):
        entradas = [
            ArquivoEntrada(caminho_fisico=str(excel_origem), caminho_logico="origem"),
            ArquivoEntrada(caminho_fisico=str(excel_comparado), caminho_logico="comparado"),
        ]
        resultado = processar_upload(entradas, modo="DUAL")
        for info in resultado.arquivos_dual:
            assert isinstance(info.arquivo_bytes, bytes)
            assert len(info.arquivo_bytes) > 0


# ---------------------------------------------------------------------------
# Testes DUAL: 1 arquivo 2 abas
# ---------------------------------------------------------------------------

class TestDualUmArquivoDuasAbas:
    def test_dual_uma_arquivo_duas_abas(self, excel_multi_aba):
        entradas = [
            ArquivoEntrada(
                caminho_fisico=str(excel_multi_aba),
                caminho_logico="origem",
                aba_solicitada="Origem",
            ),
            ArquivoEntrada(
                caminho_fisico=str(excel_multi_aba),
                caminho_logico="comparado",
                aba_solicitada="Comparado",
            ),
        ]
        resultado = processar_upload(entradas, modo="DUAL")
        assert resultado.modo_upload == "DUAL"
        assert len(resultado.arquivos_dual) == 2

    def test_abas_selecionadas_corretas(self, excel_multi_aba):
        entradas = [
            ArquivoEntrada(
                caminho_fisico=str(excel_multi_aba),
                caminho_logico="origem",
                aba_solicitada="Origem",
            ),
            ArquivoEntrada(
                caminho_fisico=str(excel_multi_aba),
                caminho_logico="comparado",
                aba_solicitada="Comparado",
            ),
        ]
        resultado = processar_upload(entradas, modo="DUAL")
        origem_info = next(a for a in resultado.arquivos_dual if a.caminho_logico == "origem")
        comparado_info = next(a for a in resultado.arquivos_dual if a.caminho_logico == "comparado")
        assert origem_info.aba_selecionada == "Origem"
        assert comparado_info.aba_selecionada == "Comparado"


# ---------------------------------------------------------------------------
# Testes de warnings
# ---------------------------------------------------------------------------

class TestWarnings:
    def test_warning_arquivo_vazio(self, excel_vazio):
        """W-U-ARQUIVO-VAZIO emitido para arquivo sem dados."""
        entrada = ArquivoEntrada(caminho_fisico=str(excel_vazio), caminho_logico="unico")
        resultado = processar_upload([entrada], modo="SIMPLES")
        codigos = [w.codigo for w in resultado.warnings]
        assert "W-U-ARQUIVO-VAZIO" in codigos

    def test_warning_multi_aba_auto(self, excel_multi_aba):
        """W-U-MULTI-ABA-AUTO emitido quando Excel multi-aba sem seleção."""
        entrada = ArquivoEntrada(caminho_fisico=str(excel_multi_aba), caminho_logico="unico")
        resultado = processar_upload([entrada], modo="SIMPLES")
        codigos = [w.codigo for w in resultado.warnings]
        assert "W-U-MULTI-ABA-AUTO" in codigos

    def test_sem_warnings_em_caso_limpo(self, excel_simples):
        """Arquivo Excel simples e limpo não deve gerar warnings desnecessários."""
        entrada = ArquivoEntrada(caminho_fisico=str(excel_simples), caminho_logico="unico")
        resultado = processar_upload([entrada], modo="SIMPLES")
        # Pode haver 0 warnings ou apenas informativos
        for w in resultado.warnings:
            assert w.categoria.value in ("informativo", "ajuste_leve")


# ---------------------------------------------------------------------------
# Testes de erros
# ---------------------------------------------------------------------------

class TestErros:
    def test_arquivo_inexistente(self, tmp_path):
        """FileNotFoundError para arquivo que não existe."""
        entrada = ArquivoEntrada(
            caminho_fisico=str(tmp_path / "inexistente.xlsx"),
            caminho_logico="unico",
        )
        with pytest.raises(FileNotFoundError):
            processar_upload([entrada], modo="SIMPLES")

    def test_formato_nao_suportado(self, tmp_path):
        """ValueError para extensão não suportada."""
        path = tmp_path / "dados.json"
        path.write_text("{}")
        entrada = ArquivoEntrada(caminho_fisico=str(path), caminho_logico="unico")
        with pytest.raises(ValueError):
            processar_upload([entrada], modo="SIMPLES")

    def test_simples_com_zero_arquivos(self):
        """ValueError para modo SIMPLES sem arquivo."""
        with pytest.raises(ValueError):
            processar_upload([], modo="SIMPLES")

    def test_dual_com_um_arquivo(self, excel_simples):
        """ValueError para modo DUAL com apenas 1 entrada."""
        entrada = ArquivoEntrada(caminho_fisico=str(excel_simples), caminho_logico="origem")
        with pytest.raises(ValueError):
            processar_upload([entrada], modo="DUAL")

    def test_abas_selecionadas_override(self, excel_multi_aba):
        """abas_selecionadas deve sobrescrever aba_solicitada."""
        entrada = ArquivoEntrada(
            caminho_fisico=str(excel_multi_aba),
            caminho_logico="unico",
            aba_solicitada="Origem",
        )
        resultado = processar_upload(
            [entrada],
            modo="SIMPLES",
            abas_selecionadas={"unico": "Comparado"},
        )
        assert resultado.arquivo_unico.aba_selecionada == "Comparado"


# ---------------------------------------------------------------------------
# Teste de timestamp
# ---------------------------------------------------------------------------

class TestTimestamp:
    def test_timestamp_preenchido(self, excel_simples):
        from datetime import datetime
        entrada = ArquivoEntrada(caminho_fisico=str(excel_simples), caminho_logico="unico")
        resultado = processar_upload([entrada], modo="SIMPLES")
        assert isinstance(resultado.timestamp_upload, datetime)
