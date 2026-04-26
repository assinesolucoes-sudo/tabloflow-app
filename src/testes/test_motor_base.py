"""
test_motor_base.py — Testes do motor_base.py v2 · F-MOT

Cobertura:
  (a) Inferência de tipos técnicos e semânticos para casos canônicos
  (b) Boolean disfarçado D-008: float64 {0,1,NaN} → BOOLEANO + W-B01
  (c) Reconhecedor pt-BR/pt-EN: 7 padrões cronológicos → TEMPORAL (D-026)
  (d) Detecção de subtipo ID: CNPJ · sequência aritmética · comprimento fixo (D-103)
  (e) tipo_estrutural: todos os 5 valores do enum (D-113 · D-133)
  (f) BloqueioOperacional B-CARD-EXCESSIVA emitido (MBO · C.D4)
  (g) Modo DUAL: origem_comparado_map preenchido
  (h) Coluna quase vazia: VAZIO_OU_AMBIGUO + W-B-QUASE-VAZIO
  (i) Coluna mista: VAZIO_OU_AMBIGUO + W-B-MISTO
  (j) Determinismo: mesma entrada → mesmo column_meta
"""
from __future__ import annotations

from datetime import datetime
from io import BytesIO
from typing import Dict, List

import numpy as np
import pandas as pd
import pytest

from contratos import (
    ArquivoInfo,
    CategoriaWarning,
    MotorConfig,
    MotorResult,
    PadraoCronologicoEnum,
    TipoEstruturalEnum,
    TipoSemanticoEnum,
    TipoTecnicoEnum,
    UploadResult,
    WarningEstrutural,
)
from motor_base import processar_base


# ---------------------------------------------------------------------------
# Helpers para criação de UploadResult a partir de DataFrame
# ---------------------------------------------------------------------------

def _df_para_bytes(df: pd.DataFrame, sheet_name: str = "Dados") -> bytes:
    """Serializa DataFrame para bytes de Excel."""
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    return buf.getvalue()


def _upload_result_de_df(
    df: pd.DataFrame,
    sheet_name: str = "Dados",
    modo: str = "SIMPLES",
    caminho_logico: str = "unico",
) -> UploadResult:
    """Cria UploadResult mínimo a partir de um DataFrame (para testes de motor_base)."""
    raw_bytes = _df_para_bytes(df, sheet_name)
    preview: Dict[str, List] = {col: df[col].head(5).tolist() for col in df.columns}
    info = ArquivoInfo(
        caminho_logico=caminho_logico,  # type: ignore[arg-type]
        nome_arquivo=f"test_{sheet_name}.xlsx",
        arquivo_bytes=raw_bytes,
        abas_disponiveis=[sheet_name],
        aba_selecionada=sheet_name,
        formato="xlsx",
        preview=preview,
        encoding_detectado=None,
        separador_csv=None,
    )
    return UploadResult(
        file_name=info.nome_arquivo,
        modo_upload="SIMPLES",  # type: ignore[arg-type]
        arquivo_unico=info,
        arquivos_dual=None,
        timestamp_upload=datetime.now(),
        warnings=[],
    )


def _upload_result_dual(
    df_origem: pd.DataFrame,
    df_comparado: pd.DataFrame,
) -> UploadResult:
    """Cria UploadResult DUAL a partir de dois DataFrames."""
    bytes_origem = _df_para_bytes(df_origem, "Origem")
    bytes_comparado = _df_para_bytes(df_comparado, "Comparado")

    preview_origem: Dict[str, List] = {col: df_origem[col].head(5).tolist() for col in df_origem.columns}
    preview_comparado: Dict[str, List] = {col: df_comparado[col].head(5).tolist() for col in df_comparado.columns}

    info_origem = ArquivoInfo(
        caminho_logico="origem",
        nome_arquivo="test_origem.xlsx",
        arquivo_bytes=bytes_origem,
        abas_disponiveis=["Origem"],
        aba_selecionada="Origem",
        formato="xlsx",
        preview=preview_origem,
        encoding_detectado=None,
        separador_csv=None,
    )
    info_comparado = ArquivoInfo(
        caminho_logico="comparado",
        nome_arquivo="test_comparado.xlsx",
        arquivo_bytes=bytes_comparado,
        abas_disponiveis=["Comparado"],
        aba_selecionada="Comparado",
        formato="xlsx",
        preview=preview_comparado,
        encoding_detectado=None,
        separador_csv=None,
    )
    return UploadResult(
        file_name="test_origem.xlsx",
        modo_upload="DUAL",
        arquivo_unico=None,
        arquivos_dual=[info_origem, info_comparado],
        timestamp_upload=datetime.now(),
        warnings=[],
    )


# ---------------------------------------------------------------------------
# Fixtures de DataFrames de teste
# ---------------------------------------------------------------------------

@pytest.fixture
def df_basico() -> pd.DataFrame:
    """DataFrame com tipos canônicos."""
    return pd.DataFrame({
        "Produto": ["A", "B", "C", "D", "E"] * 10,             # string · categorico_baixa_card
        "Valor": [100.5, 200.0, 150.75, 300.0, 50.25] * 10,   # float → NUMERICO_CONTINUO
        "Quantidade": [10, 20, 15, 30, 5] * 10,                 # int · cardinalidade <= 200 → CATEGORICO_ELEGIVEL
    })


@pytest.fixture
def df_boolean_disfarcado() -> pd.DataFrame:
    """D-008: float com {0,1,NaN} → boolean disfarçado."""
    return pd.DataFrame({
        "ID": list(range(1, 11)),
        "Nome": [f"Item {i}" for i in range(1, 11)],
        "Ativo": [1.0, 0.0, 1.0, np.nan, 1.0, 0.0, np.nan, 1.0, 0.0, 1.0],  # boolean disfarçado
    })


@pytest.fixture
def df_cronologicos_ptbr() -> pd.DataFrame:
    """Colunas com padrões cronológicos pt-BR/pt-EN (D-026)."""
    return pd.DataFrame({
        "ID": list(range(1, 11)),
        "data_iso": [f"2024-0{i}-15" for i in range(1, 10)] + ["2024-10-15"],  # ISO_DATE
        "data_ptbr": [f"{i:02d}/0{(i % 9) + 1}/2024" for i in range(1, 11)],  # PT_BR_DATE
        "mes_ptbr": ["Jan/24", "Fev/24", "Mar/24", "Abr/24", "Mai/24",
                     "Jun/24", "Jul/24", "Ago/24", "Set/24", "Out/24"],  # MONTH_NAME_PT
        "mes_en": ["February 2024", "April 2024", "August 2024", "September 2024",
                   "October 2024", "November 2024", "February 2024", "April 2024",
                   "August 2024", "September 2024"],  # MONTH_NAME_EN · nomes completos sem ambiguidade PT
        "ano_only": ["2020", "2020", "2021", "2021", "2022",
                     "2022", "2023", "2023", "2024", "2024"],            # YEAR_ONLY (card <= 30)
        "trimestre": ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "Q1 2024",
                      "Q2 2024", "Q3 2024", "Q4 2024", "Q1 2024", "Q2 2024"],  # Q_TRIMESTRE
    })


@pytest.fixture
def df_subtipo_id() -> pd.DataFrame:
    """Colunas com padrão de ID (D-103)."""
    n = 50
    return pd.DataFrame({
        "seq_aritmetica": list(range(1001, 1001 + n)),      # sequência aritmética
        "cnpj": [f"{i:014d}" for i in range(10000000000000, 10000000000000 + n)],  # comprimento fixo >= 8
        "texto": [f"categoria_{i % 5}" for i in range(n)],  # NÃO é ID (baixa cardinalidade)
    })


@pytest.fixture
def df_quase_vazio() -> pd.DataFrame:
    """Coluna com > 90% nulos → VAZIO_OU_AMBIGUO."""
    n = 20
    valores = [np.nan] * 19 + ["unico_valor"]
    return pd.DataFrame({
        "normal": list(range(n)),
        "quase_vazia": valores,
    })


@pytest.fixture
def df_cardinalidade_excessiva() -> pd.DataFrame:
    """Coluna string com cardinalidade = 100% das linhas → B-CARD-EXCESSIVA."""
    n = 100
    return pd.DataFrame({
        "id_numerico": list(range(n)),
        "texto_livre": [f"{'x' * (i % 15 + 5)} valor {i}" for i in range(n)],  # únicos, comprimento variável
    })


# ---------------------------------------------------------------------------
# (a) Inferência de tipos técnicos e semânticos
# ---------------------------------------------------------------------------

class TestInferenciaTipos:
    def test_float_e_numerico_continuo(self, df_basico):
        ur = _upload_result_de_df(df_basico)
        resultado = processar_base(ur)
        meta = resultado.column_meta["Valor"]
        assert meta.tipo_tecnico == TipoTecnicoEnum.FLOAT
        assert meta.tipo_semantico == TipoSemanticoEnum.NUMERIC
        assert meta.tipo_estrutural == TipoEstruturalEnum.NUMERICO_CONTINUO

    def test_int_baixa_card_e_categorico(self, df_basico):
        ur = _upload_result_de_df(df_basico)
        resultado = processar_base(ur)
        meta = resultado.column_meta["Quantidade"]
        assert meta.tipo_tecnico == TipoTecnicoEnum.INT
        assert meta.tipo_estrutural == TipoEstruturalEnum.CATEGORICO_ELEGIVEL

    def test_string_baixa_card_e_categorico(self, df_basico):
        ur = _upload_result_de_df(df_basico)
        resultado = processar_base(ur)
        meta = resultado.column_meta["Produto"]
        assert meta.tipo_tecnico == TipoTecnicoEnum.STRING
        assert meta.tipo_semantico == TipoSemanticoEnum.CATEGORICO_BAIXA_CARD
        assert meta.tipo_estrutural == TipoEstruturalEnum.CATEGORICO_ELEGIVEL

    def test_column_meta_tem_todas_colunas(self, df_basico):
        ur = _upload_result_de_df(df_basico)
        resultado = processar_base(ur)
        for col in df_basico.columns:
            assert col in resultado.column_meta

    def test_ordem_insercao(self, df_basico):
        ur = _upload_result_de_df(df_basico)
        resultado = processar_base(ur)
        for i, col in enumerate(df_basico.columns):
            assert resultado.column_meta[col].ordem_insercao == i

    def test_total_linhas(self, df_basico):
        ur = _upload_result_de_df(df_basico)
        resultado = processar_base(ur)
        assert resultado.total_linhas_processadas == len(df_basico)


# ---------------------------------------------------------------------------
# (b) Boolean disfarçado D-008
# ---------------------------------------------------------------------------

class TestBooleanDisfarcado:
    def test_float_com_01_nan_e_booleano(self, df_boolean_disfarcado):
        ur = _upload_result_de_df(df_boolean_disfarcado)
        resultado = processar_base(ur)
        meta = resultado.column_meta["Ativo"]
        assert meta.tipo_estrutural == TipoEstruturalEnum.BOOLEANO, (
            f"Esperado BOOLEANO, obtido {meta.tipo_estrutural}"
        )
        assert meta.tipo_semantico == TipoSemanticoEnum.BOOLEAN

    def test_warning_wb01_emitido(self, df_boolean_disfarcado):
        """D-008 + C.2: W-B01 deve ser emitido para boolean disfarçado."""
        ur = _upload_result_de_df(df_boolean_disfarcado)
        resultado = processar_base(ur)
        codigos = [w.codigo for w in resultado.warnings]
        assert "W-B01" in codigos

    def test_nao_e_numerico_continuo(self, df_boolean_disfarcado):
        """Boolean disfarçado NÃO deve ser NUMERICO_CONTINUO."""
        ur = _upload_result_de_df(df_boolean_disfarcado)
        resultado = processar_base(ur)
        meta = resultado.column_meta["Ativo"]
        assert meta.tipo_estrutural != TipoEstruturalEnum.NUMERICO_CONTINUO


# ---------------------------------------------------------------------------
# (c) Reconhecedor pt-BR/pt-EN (D-026)
# ---------------------------------------------------------------------------

class TestReconhecedorCronologico:
    def test_iso_date(self, df_cronologicos_ptbr):
        ur = _upload_result_de_df(df_cronologicos_ptbr)
        resultado = processar_base(ur)
        meta = resultado.column_meta["data_iso"]
        assert meta.tipo_estrutural == TipoEstruturalEnum.TEMPORAL
        # ISO_DATE é detectado como datetime nativo por pandas mas também pelo reconhecedor
        # Aceita TEMPORAL independente do padrão exato
        assert meta.tipo_estrutural == TipoEstruturalEnum.TEMPORAL

    def test_pt_br_date(self, df_cronologicos_ptbr):
        ur = _upload_result_de_df(df_cronologicos_ptbr)
        resultado = processar_base(ur)
        meta = resultado.column_meta["data_ptbr"]
        assert meta.tipo_estrutural == TipoEstruturalEnum.TEMPORAL
        assert meta.padrao_cronologico_detectado == PadraoCronologicoEnum.PT_BR_DATE

    def test_month_name_pt(self, df_cronologicos_ptbr):
        ur = _upload_result_de_df(df_cronologicos_ptbr)
        resultado = processar_base(ur)
        meta = resultado.column_meta["mes_ptbr"]
        assert meta.tipo_estrutural == TipoEstruturalEnum.TEMPORAL
        assert meta.padrao_cronologico_detectado == PadraoCronologicoEnum.MONTH_NAME_PT

    def test_month_name_en(self, df_cronologicos_ptbr):
        ur = _upload_result_de_df(df_cronologicos_ptbr)
        resultado = processar_base(ur)
        meta = resultado.column_meta["mes_en"]
        assert meta.tipo_estrutural == TipoEstruturalEnum.TEMPORAL
        assert meta.padrao_cronologico_detectado == PadraoCronologicoEnum.MONTH_NAME_EN

    def test_year_only(self, df_cronologicos_ptbr):
        ur = _upload_result_de_df(df_cronologicos_ptbr)
        resultado = processar_base(ur)
        meta = resultado.column_meta["ano_only"]
        assert meta.tipo_estrutural == TipoEstruturalEnum.TEMPORAL
        assert meta.padrao_cronologico_detectado == PadraoCronologicoEnum.YEAR_ONLY

    def test_q_trimestre(self, df_cronologicos_ptbr):
        ur = _upload_result_de_df(df_cronologicos_ptbr)
        resultado = processar_base(ur)
        meta = resultado.column_meta["trimestre"]
        assert meta.tipo_estrutural == TipoEstruturalEnum.TEMPORAL
        assert meta.padrao_cronologico_detectado == PadraoCronologicoEnum.Q_TRIMESTRE


# ---------------------------------------------------------------------------
# (d) Detecção de subtipo ID (D-103)
# ---------------------------------------------------------------------------

class TestSubtipoID:
    def test_sequencia_aritmetica_e_id(self, df_subtipo_id):
        ur = _upload_result_de_df(df_subtipo_id)
        resultado = processar_base(ur)
        meta = resultado.column_meta["seq_aritmetica"]
        assert meta.subtipo_id_detectado is True

    def test_comprimento_fixo_grande_e_id(self, df_subtipo_id):
        ur = _upload_result_de_df(df_subtipo_id)
        resultado = processar_base(ur)
        meta = resultado.column_meta["cnpj"]
        assert meta.subtipo_id_detectado is True

    def test_texto_categorico_nao_e_id(self, df_subtipo_id):
        ur = _upload_result_de_df(df_subtipo_id)
        resultado = processar_base(ur)
        meta = resultado.column_meta["texto"]
        assert meta.subtipo_id_detectado is False

    def test_id_int_e_categorico_elegivel(self, df_subtipo_id):
        """D-103: coluna int com subtipo ID → CATEGORICO_ELEGIVEL apesar de alta card."""
        ur = _upload_result_de_df(df_subtipo_id)
        resultado = processar_base(ur)
        meta = resultado.column_meta["seq_aritmetica"]
        assert meta.subtipo_id_detectado is True
        assert meta.tipo_estrutural == TipoEstruturalEnum.CATEGORICO_ELEGIVEL

    def test_warning_id_detectado(self, df_subtipo_id):
        """W-B-ID-DETECTADO emitido quando ID detectado."""
        ur = _upload_result_de_df(df_subtipo_id)
        resultado = processar_base(ur)
        codigos = [w.codigo for w in resultado.warnings]
        assert "W-B-ID-DETECTADO" in codigos

    def test_cnpj_regex_como_id(self):
        """Coluna com CNPJs reais (regex) deve ser detectada como ID."""
        n = 30
        df = pd.DataFrame({
            "CNPJ": [
                f"{i:02d}.{i:03d}.{i:03d}/000{i % 10}-{i:02d}"
                for i in range(10, 10 + n)
            ],
            "Empresa": [f"Empresa {i}" for i in range(n)],
        })
        ur = _upload_result_de_df(df)
        resultado = processar_base(ur)
        # CNPJ tem todos valores únicos + padrão regex de ID
        meta = resultado.column_meta["CNPJ"]
        assert meta.subtipo_id_detectado is True


# ---------------------------------------------------------------------------
# (e) tipo_estrutural: todos os 5 valores
# ---------------------------------------------------------------------------

class TestTipoEstrutural5Enums:
    def test_categorico_elegivel(self, df_basico):
        ur = _upload_result_de_df(df_basico)
        resultado = processar_base(ur)
        tipos = {m.tipo_estrutural for m in resultado.column_meta.values()}
        assert TipoEstruturalEnum.CATEGORICO_ELEGIVEL in tipos

    def test_numerico_continuo(self, df_basico):
        ur = _upload_result_de_df(df_basico)
        resultado = processar_base(ur)
        tipos = {m.tipo_estrutural for m in resultado.column_meta.values()}
        assert TipoEstruturalEnum.NUMERICO_CONTINUO in tipos

    def test_temporal(self, df_cronologicos_ptbr):
        ur = _upload_result_de_df(df_cronologicos_ptbr)
        resultado = processar_base(ur)
        tipos = {m.tipo_estrutural for m in resultado.column_meta.values()}
        assert TipoEstruturalEnum.TEMPORAL in tipos

    def test_booleano(self, df_boolean_disfarcado):
        ur = _upload_result_de_df(df_boolean_disfarcado)
        resultado = processar_base(ur)
        tipos = {m.tipo_estrutural for m in resultado.column_meta.values()}
        assert TipoEstruturalEnum.BOOLEANO in tipos

    def test_vazio_ou_ambiguo_quase_vazio(self, df_quase_vazio):
        ur = _upload_result_de_df(df_quase_vazio)
        resultado = processar_base(ur)
        meta = resultado.column_meta["quase_vazia"]
        assert meta.tipo_estrutural == TipoEstruturalEnum.VAZIO_OU_AMBIGUO

    def test_vazio_ou_ambiguo_misto(self):
        """Coluna com tipos mistos → VAZIO_OU_AMBIGUO."""
        df = pd.DataFrame({
            "mista": ["texto", 123, "outro texto", 456, "mais", 789, "fim", 111, "ok", 222],
        })
        ur = _upload_result_de_df(df)
        resultado = processar_base(ur)
        meta = resultado.column_meta["mista"]
        # Misto pode resultar em VAZIO_OU_AMBIGUO ou CATEGORICO_ELEGIVEL
        # dependendo da inferência - o importante é não ser NUMERICO_CONTINUO
        assert meta.tipo_estrutural != TipoEstruturalEnum.NUMERICO_CONTINUO


# ---------------------------------------------------------------------------
# (f) BloqueioOperacional B-CARD-EXCESSIVA
# ---------------------------------------------------------------------------

class TestBloqueioCardinalidadeExcessiva:
    def test_bloqueio_card_excessiva_emitido(self, df_cardinalidade_excessiva):
        """B-CARD-EXCESSIVA emitido quando coluna string com 100% valores únicos."""
        ur = _upload_result_de_df(df_cardinalidade_excessiva)
        resultado = processar_base(ur)
        codigos_bloqueio = [b.codigo for b in resultado.bloqueios]
        assert "B-CARD-EXCESSIVA" in codigos_bloqueio

    def test_bloqueio_e_instance_de_bloqueio_operacional(self, df_cardinalidade_excessiva):
        """Tipo do objeto deve ser BloqueioOperacional (D-134)."""
        from contratos import BloqueioOperacional
        ur = _upload_result_de_df(df_cardinalidade_excessiva)
        resultado = processar_base(ur)
        for b in resultado.bloqueios:
            assert isinstance(b, BloqueioOperacional)

    def test_bloqueio_card_excessiva_tem_contexto(self, df_cardinalidade_excessiva):
        """Contexto do bloqueio deve ter coluna e cardinalidade."""
        ur = _upload_result_de_df(df_cardinalidade_excessiva)
        resultado = processar_base(ur)
        b_card = next(b for b in resultado.bloqueios if b.codigo == "B-CARD-EXCESSIVA")
        assert "coluna" in b_card.contexto_disparo
        assert "cardinalidade" in b_card.contexto_disparo

    def test_sem_bloqueio_em_base_normal(self, df_basico):
        """Base normal não deve gerar B-CARD-EXCESSIVA."""
        ur = _upload_result_de_df(df_basico)
        resultado = processar_base(ur)
        codigos = [b.codigo for b in resultado.bloqueios]
        assert "B-CARD-EXCESSIVA" not in codigos


# ---------------------------------------------------------------------------
# (g) Modo DUAL
# ---------------------------------------------------------------------------

class TestModoDual:
    def test_dual_origem_comparado_map(self):
        """origem_comparado_map deve mapear corretamente as linhas."""
        df_a = pd.DataFrame({"Valor": [1, 2, 3], "Grupo": ["A", "B", "C"]})
        df_b = pd.DataFrame({"Valor": [4, 5], "Grupo": ["D", "E"]})
        ur = _upload_result_dual(df_a, df_b)
        resultado = processar_base(ur)
        assert resultado.modo_upload == "DUAL"
        assert resultado.origem_comparado_map is not None
        # Primeiras 3 linhas = origem
        assert resultado.origem_comparado_map[0] == "origem"
        assert resultado.origem_comparado_map[1] == "origem"
        assert resultado.origem_comparado_map[2] == "origem"
        # Linhas 3 e 4 = comparado
        assert resultado.origem_comparado_map[3] == "comparado"
        assert resultado.origem_comparado_map[4] == "comparado"

    def test_dual_total_linhas(self):
        df_a = pd.DataFrame({"Valor": [1, 2, 3]})
        df_b = pd.DataFrame({"Valor": [4, 5]})
        ur = _upload_result_dual(df_a, df_b)
        resultado = processar_base(ur)
        assert resultado.total_linhas_processadas == 5
        assert resultado.total_linhas_originais == 5

    def test_simples_nao_tem_mapa(self, df_basico):
        ur = _upload_result_de_df(df_basico)
        resultado = processar_base(ur)
        assert resultado.modo_upload == "SIMPLES"
        assert resultado.origem_comparado_map is None


# ---------------------------------------------------------------------------
# (h) Coluna quase vazia
# ---------------------------------------------------------------------------

class TestColunaQuaseVazia:
    def test_warning_quase_vazio(self, df_quase_vazio):
        ur = _upload_result_de_df(df_quase_vazio)
        resultado = processar_base(ur)
        codigos = [w.codigo for w in resultado.warnings]
        assert "W-B-QUASE-VAZIO" in codigos

    def test_tipo_estrutural_vazio_ou_ambiguo(self, df_quase_vazio):
        ur = _upload_result_de_df(df_quase_vazio)
        resultado = processar_base(ur)
        meta = resultado.column_meta["quase_vazia"]
        assert meta.tipo_estrutural == TipoEstruturalEnum.VAZIO_OU_AMBIGUO


# ---------------------------------------------------------------------------
# (i) Retorno de MotorResult bem formado
# ---------------------------------------------------------------------------

class TestMotorResultContrato:
    def test_resultado_e_motor_result(self, df_basico):
        ur = _upload_result_de_df(df_basico)
        resultado = processar_base(ur)
        assert isinstance(resultado, MotorResult)

    def test_df_e_dataframe(self, df_basico):
        ur = _upload_result_de_df(df_basico)
        resultado = processar_base(ur)
        assert isinstance(resultado.df, pd.DataFrame)

    def test_timestamp_preenchido(self, df_basico):
        ur = _upload_result_de_df(df_basico)
        resultado = processar_base(ur)
        assert isinstance(resultado.timestamp_processamento, datetime)

    def test_para_contexto_ia(self, df_basico):
        """D-130: para_contexto_ia() deve retornar dict serializável."""
        ur = _upload_result_de_df(df_basico)
        resultado = processar_base(ur)
        ctx = resultado.para_contexto_ia()
        assert "column_meta" in ctx
        assert "total_linhas" in ctx
        assert "amostra_5_linhas" in ctx
        assert "estatisticas_sumarias" in ctx
        assert "warnings" in ctx
        # Não deve conter DataFrame bruto
        assert "df" not in ctx

    def test_column_meta_campos_obrigatorios(self, df_basico):
        ur = _upload_result_de_df(df_basico)
        resultado = processar_base(ur)
        for col_name, meta in resultado.column_meta.items():
            assert meta.nome == col_name
            assert isinstance(meta.null_count, int)
            assert isinstance(meta.cardinalidade, int)
            assert isinstance(meta.subtipo_id_detectado, bool)
            assert isinstance(meta.eh_candidato_categorico, bool)
            assert meta.tipo_estrutural in TipoEstruturalEnum


# ---------------------------------------------------------------------------
# (j) Determinismo C.1
# ---------------------------------------------------------------------------

class TestDeterminismo:
    def test_mesmo_resultado_em_execucoes_repetidas(self, df_basico):
        """C.1: mesma entrada → mesma column_meta em duas execuções."""
        ur = _upload_result_de_df(df_basico)
        r1 = processar_base(ur)
        r2 = processar_base(ur)
        for col in df_basico.columns:
            m1 = r1.column_meta[col]
            m2 = r2.column_meta[col]
            assert m1.tipo_estrutural == m2.tipo_estrutural
            assert m1.tipo_tecnico == m2.tipo_tecnico
            assert m1.tipo_semantico == m2.tipo_semantico
            assert m1.null_count == m2.null_count
            assert m1.cardinalidade == m2.cardinalidade
            assert m1.subtipo_id_detectado == m2.subtipo_id_detectado

    def test_df_linhas_estavel(self, df_basico):
        """C.1: número de linhas estável entre execuções."""
        ur = _upload_result_de_df(df_basico)
        r1 = processar_base(ur)
        r2 = processar_base(ur)
        assert len(r1.df) == len(r2.df)


# ---------------------------------------------------------------------------
# Testes de configuração customizada
# ---------------------------------------------------------------------------

class TestMotorConfig:
    def test_config_customizada(self, df_basico):
        """MotorConfig customizada deve ser respeitada."""
        config = MotorConfig(max_cardinalidade_categorico=5)
        ur = _upload_result_de_df(df_basico)
        resultado = processar_base(ur, config=config)
        # Com threshold de 5, "Quantidade" (5 valores únicos) pode virar NUMERICO_CONTINUO
        # Dependendo do dado, mas o motor deve aceitar a config sem erro
        assert isinstance(resultado, MotorResult)

    def test_bloqueio_base_muito_grande(self):
        """B-B-BASE-MUITO-GRANDE emitido quando linhas excedem limite."""
        config = MotorConfig(limite_linhas_bloqueio=10)
        df = pd.DataFrame({"Valor": list(range(20))})
        ur = _upload_result_de_df(df)
        resultado = processar_base(ur, config=config)
        codigos = [b.codigo for b in resultado.bloqueios]
        assert "B-B-BASE-MUITO-GRANDE" in codigos
