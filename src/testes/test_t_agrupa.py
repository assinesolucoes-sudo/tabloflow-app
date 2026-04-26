"""
test_t_agrupa.py — Testes de T-AGRUPA · Consolidação Pré-Cálculo Obrigatória · D-122
Casos: TRANSACIONAL soma · regra por métrica · PRE_AGREGADO sem duplicata ·
       PRE_AGREGADO com duplicata · ordenação cronológica pt-BR.
"""
import pandas as pd
import pytest

from contratos import ColumnMeta, PadraoCronologicoEnum, TipoEstruturalEnum, TipoSemanticoEnum, TipoTecnicoEnum
from transversais.t_agrupa import consolidar_com_modo


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _meta_temporal(nome: str, padrao: PadraoCronologicoEnum) -> ColumnMeta:
    return ColumnMeta(
        nome=nome,
        tipo_tecnico=TipoTecnicoEnum.STRING,
        tipo_semantico=TipoSemanticoEnum.TEMPORAL,
        tipo_estrutural=TipoEstruturalEnum.TEMPORAL,
        subtipo_id_detectado=False,
        null_count=0,
        cardinalidade=12,
        eh_candidato_categorico=False,
        padrao_cronologico_detectado=padrao,
        ordem_insercao=0,
    )


# ---------------------------------------------------------------------------
# TRANSACIONAL com soma simples
# ---------------------------------------------------------------------------

def test_transacional_soma_agrupa(df_vendas):
    df_res, warns = consolidar_com_modo(
        df_vendas, agrupadores=["produto"], regras="soma", modo_base="TRANSACIONAL"
    )
    assert set(df_res["produto"].tolist()) == {"A", "B", "C"}
    # A: 100+120=220, B: 200+80=280, C: 150
    soma_a = df_res.loc[df_res["produto"] == "A", "valor"].values[0]
    assert abs(soma_a - 220.0) < 1e-9


def test_transacional_soma_dois_agrupadores(df_vendas):
    df_res, warns = consolidar_com_modo(
        df_vendas, agrupadores=["produto", "regiao"], regras="soma", modo_base="TRANSACIONAL"
    )
    # df_vendas: A-Norte, B-Sul, C-Norte, A-Sul, B-Norte → 5 combinações únicas
    assert len(df_res) == 5
    linha_a_norte = df_res[(df_res["produto"] == "A") & (df_res["regiao"] == "Norte")]
    assert len(linha_a_norte) == 1
    assert abs(linha_a_norte["valor"].values[0] - 100.0) < 1e-9


def test_transacional_sem_warnings_simples(df_vendas):
    _, warns = consolidar_com_modo(
        df_vendas, agrupadores=["produto"], regras="soma", modo_base="TRANSACIONAL"
    )
    assert len(warns) == 0


# ---------------------------------------------------------------------------
# TRANSACIONAL com regra por métrica (Extensão 2)
# ---------------------------------------------------------------------------

def test_regra_por_metrica_dict(df_vendas):
    regras_dict = {"valor": "soma", "qtd": "media"}
    df_res, warns = consolidar_com_modo(
        df_vendas, agrupadores=["produto"], regras=regras_dict, modo_base="TRANSACIONAL"
    )
    # Warning W-T-AGRUPA-REGRA-POR-METRICA deve ser emitido
    assert any(w.codigo == "W-T-AGRUPA-REGRA-POR-METRICA" for w in warns)
    # A: soma valor = 220, media qtd = (10+12)/2 = 11
    linha_a = df_res[df_res["produto"] == "A"]
    assert abs(linha_a["valor"].values[0] - 220.0) < 1e-9
    assert abs(linha_a["qtd"].values[0] - 11.0) < 1e-9


def test_regra_por_metrica_maximo():
    df = pd.DataFrame({
        "cat": ["X", "X", "Y"],
        "val": [10.0, 50.0, 30.0],
    })
    df_res, warns = consolidar_com_modo(
        df, agrupadores=["cat"], regras={"val": "maximo"}, modo_base="TRANSACIONAL"
    )
    assert df_res.loc[df_res["cat"] == "X", "val"].values[0] == 50.0


def test_regra_por_metrica_contagem():
    df = pd.DataFrame({
        "cat": ["X", "X", "Y"],
        "val": [10.0, 50.0, 30.0],
    })
    df_res, warns = consolidar_com_modo(
        df, agrupadores=["cat"], regras={"val": "contagem"}, modo_base="TRANSACIONAL"
    )
    assert df_res.loc[df_res["cat"] == "X", "val"].values[0] == 2


# ---------------------------------------------------------------------------
# PRE_AGREGADO sem duplicata (Extensão 3 · no-op)
# ---------------------------------------------------------------------------

def test_pre_agregado_sem_duplicata(df_pre_agregado):
    df_res, warns = consolidar_com_modo(
        df_pre_agregado, agrupadores=["produto"], regras="soma", modo_base="PRE_AGREGADO"
    )
    assert len(warns) == 0
    assert len(df_res) == len(df_pre_agregado)
    # DataFrame retornado é cópia idêntica
    pd.testing.assert_frame_equal(df_res.reset_index(drop=True), df_pre_agregado.reset_index(drop=True))


# ---------------------------------------------------------------------------
# PRE_AGREGADO com duplicata → warning
# ---------------------------------------------------------------------------

def test_pre_agregado_com_duplicata(df_pre_agregado_com_duplicata):
    df_res, warns = consolidar_com_modo(
        df_pre_agregado_com_duplicata,
        agrupadores=["produto"],
        regras="soma",
        modo_base="PRE_AGREGADO",
    )
    assert any(w.codigo == "W-T-AGRUPA-DUPLICATA-PRE-AGREGADO" for w in warns)
    assert len(df_res) == len(df_pre_agregado_com_duplicata)


# ---------------------------------------------------------------------------
# Ordenação cronológica pt-BR via column_meta (Extensão 1)
# ---------------------------------------------------------------------------

def test_ordenacao_cronologica_mes_pt_br(df_temporal):
    meta = {"mes": _meta_temporal("mes", PadraoCronologicoEnum.MONTH_NAME_PT)}
    df_res, warns = consolidar_com_modo(
        df_temporal,
        agrupadores=["mes"],
        regras="soma",
        modo_base="TRANSACIONAL",
        column_meta=meta,
    )
    ordem_meses = df_res["mes"].tolist()
    # jan deve vir antes de mai
    assert ordem_meses.index("jan") < ordem_meses.index("mai")


def test_sem_column_meta_nao_reordena():
    df = pd.DataFrame({
        "mes": ["mai", "jan", "mar"],
        "valor": [1.0, 2.0, 3.0],
    })
    df_res, _ = consolidar_com_modo(
        df, agrupadores=["mes"], regras="soma", modo_base="TRANSACIONAL", column_meta=None
    )
    # Sem column_meta, ordem é a de chegada do groupby
    assert set(df_res["mes"].tolist()) == {"jan", "mai", "mar"}


def test_df_sem_agrupadores_retorna_original():
    df = pd.DataFrame({"valor": [1.0, 2.0]})
    df_res, warns = consolidar_com_modo(
        df, agrupadores=[], regras="soma", modo_base="TRANSACIONAL"
    )
    assert len(df_res) == 2
    assert warns == []
