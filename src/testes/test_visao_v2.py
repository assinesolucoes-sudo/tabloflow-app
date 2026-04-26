"""
test_visao_v2.py — Suite V-V2 · Análise Comparativa entre Referências
5 grupos: Unitários por etapa · Integração E2E · Catálogo MBO · Catálogo warnings · Determinismo+IA
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import pytest
import yaml

# Garantir que /src e /src/transversais estão no path
_SRC = Path(__file__).parent.parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

YAML_PATH = Path(__file__).parent.parent.parent / "bases" / "casos_esperados.yaml"
BASE_V2_PATH = Path(__file__).parent.parent.parent / "bases" / "base_v2_cliente.xlsx"

from contratos import (
    BloqueioOperacional,
    CategoriaWarning,
    ColumnMeta,
    MotorResult,
    MotorResultMeta,
    TipoEstruturalEnum,
    TipoSemanticoEnum,
    TipoTecnicoEnum,
    WarningEstrutural,
)
from visoes.visao_v2 import (
    ComparacaoV2,
    LinhaTopVariacao,
    ModeloAplicadoV2,
    NumerosAncoraV2,
    ResolucaoEstruturalV2,
    V2Result,
    _classificar_patamar_agrupadores,
    _classificar_patamar_discriminador,
    _classificar_patamar_resultado,
    executar_v2,
)


# ---------------------------------------------------------------------------
# Helpers de fixtures
# ---------------------------------------------------------------------------


def _carregar_assertions_v2() -> List[Dict[str, Any]]:
    with open(YAML_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["visoes"]["V2"]["assertions"]


def _col_meta(nome: str, tipo_tecnico: str = "float", tipo_estrutural: str = "NUMERICO_CONTINUO") -> ColumnMeta:
    return ColumnMeta(
        nome=nome,
        tipo_tecnico=TipoTecnicoEnum(tipo_tecnico),
        tipo_semantico=TipoSemanticoEnum("numeric") if tipo_estrutural == "NUMERICO_CONTINUO" else TipoSemanticoEnum("categorico_baixa_card"),
        tipo_estrutural=TipoEstruturalEnum(tipo_estrutural),
        subtipo_id_detectado=False,
        null_count=0,
        cardinalidade=10,
        eh_candidato_categorico=tipo_estrutural == "CATEGORICO_ELEGIVEL",
        padrao_cronologico_detectado=None,
        ordem_insercao=0,
    )


def _motor_result(df: pd.DataFrame, modo: str = "SIMPLES") -> MotorResult:
    col_meta = {}
    for i, col in enumerate(df.columns):
        if pd.api.types.is_numeric_dtype(df[col]):
            meta = _col_meta(col, "float", "NUMERICO_CONTINUO")
        else:
            meta = _col_meta(col, "string", "CATEGORICO_ELEGIVEL")
        meta = meta.model_copy(update={"nome": col, "ordem_insercao": i, "null_count": int(df[col].isna().sum()), "cardinalidade": int(df[col].nunique())})
        col_meta[col] = meta
    return MotorResult(
        df=df,
        column_meta=col_meta,
        modo_upload=modo,
        total_linhas_originais=len(df),
        total_linhas_processadas=len(df),
    )


def _config_base(
    estrutura: str = "POR_LINHAS",
    campo: str = "Vendas",
    tipo: str = "NUMERICO_ADITIVO",
    agrupadores: Optional[List[str]] = None,
    coluna_disc: Optional[str] = "Mes",
    orig_tech: str = "2025-01",
    comp_tech: str = "2025-02",
    semantica: str = "MAIOR_MELHOR",
) -> Dict[str, Any]:
    return {
        "estrutura_entrada": estrutura,
        "origem_rotulo_tecnico": orig_tech,
        "comparado_rotulo_tecnico": comp_tech,
        "origem_rotulo_ux": "Janeiro 2025",
        "comparado_rotulo_ux": "Fevereiro 2025",
        "coluna_discriminadora": coluna_disc,
        "modo_4_ativado": False,
        "estados_nao_escolhidos": [],
        "campo_analisado": campo,
        "tipo_campo": tipo,
        "semantica_campo": semantica,
        "regra_agregacao": "SOMA",
        "metodo_consolidacao_relativo": None,
        "campo_peso": None,
        "modo_pre_agregado": False,
        "agrupadores": agrupadores or ["Loja", "Produto"],
        "resolucao_estrutural": None,
        "thresholds": {
            "limiar_estabilidade_pct": 0.01,
            "limiar_nulo_massivo_pct": 0.20,
            "limite_valores_discriminador_alerta": 50,
            "limite_variacao_extrema_pct": 10.0,
        },
        "modelo_aplicado": None,
    }


# Config canônica para V2-A01 / V2-A02 / V2-A04
config_v2_a01_a02_a04 = {
    "estrutura_entrada": "POR_LINHAS",
    "origem_rotulo_tecnico": "2025-01",
    "comparado_rotulo_tecnico": "2025-02",
    "origem_rotulo_ux": "Janeiro 2025",
    "comparado_rotulo_ux": "Fevereiro 2025",
    "coluna_discriminadora": "Mes",
    "modo_4_ativado": False,
    "estados_nao_escolhidos": [],
    "campo_analisado": "Vendas",
    "tipo_campo": "NUMERICO_ADITIVO",
    "semantica_campo": "MAIOR_MELHOR",
    "regra_agregacao": "SOMA",
    "metodo_consolidacao_relativo": None,
    "campo_peso": None,
    "modo_pre_agregado": False,
    "agrupadores": ["Loja", "Produto"],
    "resolucao_estrutural": None,
    "thresholds": {
        "limiar_estabilidade_pct": 0.01,
        "limiar_nulo_massivo_pct": 0.20,
        "limite_valores_discriminador_alerta": 50,
        "limite_variacao_extrema_pct": 10.0,
    },
    "modelo_aplicado": None,
}


@pytest.fixture(scope="module")
def df_vendas_padrao():
    return pd.read_excel(str(BASE_V2_PATH), sheet_name="vendas_padrao")


@pytest.fixture(scope="module")
def motor_result_vendas(df_vendas_padrao):
    return _motor_result(df_vendas_padrao)


@pytest.fixture(scope="module")
def result_v2_integracao(motor_result_vendas):
    return executar_v2(motor_result_vendas, config_v2_a01_a02_a04)


# ---------------------------------------------------------------------------
# GRUPO 1 · Unitários por etapa
# ---------------------------------------------------------------------------


class TestEtapaA:
    def test_por_linhas_filtra_para_2_valores(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02", "2025-03"] * 3,
            "Loja": ["A"] * 9,
            "Vendas": range(9),
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        # Mes=2025-03 excluído; base_analitica deve ter apenas (Loja A) com os 2 meses
        assert not result.bloqueios_disparados
        assert "Mes" not in result.base_analitica.columns  # disc. consumida

    def test_modo_4_registra_excluidos_no_diagnostico(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02", "2025-03"] * 2,
            "Loja": ["A", "B"] * 3,
            "Vendas": [100.0] * 6,
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        config["modo_4_ativado"] = True
        config["estados_nao_escolhidos"] = ["2025-03"]
        result = executar_v2(mr, config)
        ajustes = result.diagnostico.ajustes_aplicados
        assert any("MODO_4" in a.tipo_ajuste for a in ajustes)

    def test_por_colunas_noop(self):
        df = pd.DataFrame({
            "Produto": ["A", "B", "C"],
            "Receita_Jan": [100.0, 200.0, 150.0],
            "Receita_Fev": [120.0, 180.0, 160.0],
        })
        mr = _motor_result(df)
        config = {
            "estrutura_entrada": "POR_COLUNAS",
            "origem_rotulo_tecnico": "Receita_Jan",
            "comparado_rotulo_tecnico": "Receita_Fev",
            "origem_rotulo_ux": "Janeiro",
            "comparado_rotulo_ux": "Fevereiro",
            "coluna_discriminadora": None,
            "modo_4_ativado": False,
            "estados_nao_escolhidos": [],
            "campo_analisado": "Receita",
            "tipo_campo": "NUMERICO_ADITIVO",
            "semantica_campo": "MAIOR_MELHOR",
            "regra_agregacao": "SOMA",
            "metodo_consolidacao_relativo": None,
            "campo_peso": None,
            "modo_pre_agregado": False,
            "agrupadores": ["Produto"],
            "resolucao_estrutural": None,
            "thresholds": {
                "limiar_estabilidade_pct": 0.01,
                "limiar_nulo_massivo_pct": 0.20,
                "limite_valores_discriminador_alerta": 50,
                "limite_variacao_extrema_pct": 10.0,
            },
            "modelo_aplicado": None,
        }
        result = executar_v2(mr, config)
        assert not result.bloqueios_disparados
        assert len(result.base_analitica) == 3

    def test_discriminador_vazio_bloqueia(self):
        df = pd.DataFrame({"Mes": [None, None], "Loja": ["A", "B"], "Vendas": [1.0, 2.0]})
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        assert any(b.codigo == "B-V2-DISCRIMINADOR-0" for b in result.bloqueios_disparados)

    def test_discriminador_um_valor_bloqueia(self):
        df = pd.DataFrame({"Mes": ["2025-01"] * 4, "Loja": ["A", "B", "C", "D"], "Vendas": [1.0] * 4})
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        assert any(b.codigo == "B-V2-DISCRIMINADOR-1" for b in result.bloqueios_disparados)


class TestEtapaB:
    def test_cancelamento_usuario_retorna_bloqueio(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02"] * 2,
            "Loja": ["A", "A", "B", "B"],
            "Vendas": [100.0, 120.0, 200.0, 180.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        config["resolucao_estrutural"] = {
            "tipo_caso": "NIVEL_AGRUPAMENTO_DIFERENTE",
            "opcoes_oferecidas": ["agregar lado fino", "cancelar"],
            "escolha_usuario": "cancelar",
            "contexto_caso": {"detalhe": "teste"},
            "registrada_como": "DECISAO_USUARIO",
        }
        result = executar_v2(mr, config)
        assert any(b.codigo == "B-V2-CASO-ESTRUTURAL-CANCELADO" for b in result.bloqueios_disparados)

    def test_resolucao_usuario_registrada(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02"] * 2,
            "Loja": ["A", "A", "B", "B"],
            "Vendas": [100.0, 120.0, 200.0, 180.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        config["resolucao_estrutural"] = {
            "tipo_caso": "TIPO_CAMPO_INCOMPATIVEL",
            "opcoes_oferecidas": ["tratar como ESTADO_SITUACAO", "cancelar"],
            "escolha_usuario": "tratar como ESTADO_SITUACAO",
            "contexto_caso": {},
            "registrada_como": "DECISAO_USUARIO",
        }
        result = executar_v2(mr, config)
        assert not any(b.codigo == "B-V2-CASO-ESTRUTURAL-CANCELADO" for b in result.bloqueios_disparados)
        assert result.resolucao_estrutural is not None
        assert result.resolucao_estrutural.tipo_caso == "TIPO_CAMPO_INCOMPATIVEL"


class TestEtapaC:
    def test_transacional_soma(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-01", "2025-02", "2025-02"],
            "Loja": ["A", "A", "A", "A"],
            "Vendas": [100.0, 50.0, 200.0, 80.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        assert not result.bloqueios_disparados
        ba = result.base_analitica
        assert len(ba) == 1
        row = ba.iloc[0]
        assert row["valor_origem"] == pytest.approx(150.0)
        assert row["valor_comparado"] == pytest.approx(280.0)

    def test_pre_agregado_sem_duplicata(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02"],
            "Loja": ["A", "A"],
            "Vendas": [100.0, 120.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        config["modo_pre_agregado"] = True
        result = executar_v2(mr, config)
        assert not result.bloqueios_disparados
        assert not any(w.codigo == "W-V2-PAGREG-DUP" for w in result.warnings)

    def test_pre_agregado_com_duplicata_emite_warning(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-01", "2025-02"],
            "Loja": ["A", "A", "A"],
            "Vendas": [100.0, 50.0, 120.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        config["modo_pre_agregado"] = True
        result = executar_v2(mr, config)
        assert any(w.codigo == "W-V2-PAGREG-DUP" for w in result.warnings)

    def test_nulo_preservado_apos_agregacao(self):
        # Loja B garante que origem não é 100% nula (evita B-V2-CAMPO-100-NULO)
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-01", "2025-02", "2025-02"],
            "Loja": ["A", "B", "A", "B"],
            "Vendas": [None, 50.0, 120.0, 80.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        assert not result.bloqueios_disparados
        ba = result.base_analitica
        nulo_row = ba[ba["Loja"] == "A"].iloc[0]
        assert nulo_row["classificacao_estrutural"] == "NULO_ORIGEM"
        assert pd.isna(nulo_row["valor_origem"])


class TestEtapaD:
    def _build_result(self, df_data: Dict) -> V2Result:
        df = pd.DataFrame(df_data)
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        return executar_v2(mr, config)

    def test_seis_categorias_estruturais_presentes_ambos(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02"],
            "Loja": ["A", "A"],
            "Vendas": [100.0, 120.0],
        })
        result = self._build_result({"Mes": ["2025-01", "2025-02"], "Loja": ["A", "A"], "Vendas": [100.0, 120.0]})
        ba = result.base_analitica
        assert ba.iloc[0]["classificacao_estrutural"] == "PRESENTE_AMBOS"

    def test_ausente_comparado(self):
        # B presente em 2025-01 mas ausente em 2025-02 → AUSENTE_COMPARADO
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-01", "2025-02"],
            "Loja": ["A", "B", "A"],
            "Vendas": [100.0, 200.0, 110.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        ba = result.base_analitica
        assert "AUSENTE_COMPARADO" in ba["classificacao_estrutural"].values

    def test_ausente_origem(self):
        # B presente em 2025-02 mas ausente em 2025-01 → AUSENTE_ORIGEM
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02", "2025-02"],
            "Loja": ["A", "A", "B"],
            "Vendas": [100.0, 120.0, 150.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        ba = result.base_analitica
        assert "AUSENTE_ORIGEM" in ba["classificacao_estrutural"].values

    def test_nulo_origem(self):
        # Loja B garante que origem não é 100% nula (evita B-V2-CAMPO-100-NULO)
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-01", "2025-02", "2025-02"],
            "Loja": ["A", "B", "A", "B"],
            "Vendas": [None, 50.0, 120.0, 80.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        ba = result.base_analitica
        assert ba[ba["Loja"] == "A"].iloc[0]["classificacao_estrutural"] == "NULO_ORIGEM"

    def test_nulo_comparado(self):
        # Loja B garante que comparado não é 100% nulo
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-01", "2025-02", "2025-02"],
            "Loja": ["A", "B", "A", "B"],
            "Vendas": [100.0, 50.0, None, 80.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        ba = result.base_analitica
        assert ba[ba["Loja"] == "A"].iloc[0]["classificacao_estrutural"] == "NULO_COMPARADO"

    def test_nulo_ambos(self):
        # Loja B garante que nem origem nem comparado são 100% nulos
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-01", "2025-02", "2025-02"],
            "Loja": ["A", "B", "A", "B"],
            "Vendas": [None, 50.0, None, 80.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        ba = result.base_analitica
        assert ba[ba["Loja"] == "A"].iloc[0]["classificacao_estrutural"] == "NULO_AMBOS"

    def test_delta_bz_origem_zero_comparado_nao_zero(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02"],
            "Loja": ["A", "A"],
            "Vendas": [0.0, 100.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        ba = result.base_analitica
        row = ba[ba["classificacao_estrutural"] == "PRESENTE_AMBOS"].iloc[0]
        assert row["diferenca"] == pytest.approx(100.0)
        assert pd.isna(row["variacao_percentual"])
        assert any(w.codigo == "W-V2-BZ" for w in result.warnings)


class TestEtapaE:
    """
    Cobertura T-SEMA · matriz cartesiana 12/12 (D-183 · D-187).

    Eixos:
      semantica_campo ∈ {MAIOR_MELHOR, MENOR_MELHOR, NEUTRO}
      estrutural ∈ {AUMENTOU, REDUZIU, ESTAVEL, NAO_APLICAVEL}

    Para semantica_campo=NEUTRO os 4 estruturais aparecem distintos · não
    colapsam em "NEUTRO" (D-187 · spec_fundacao §D.3).
    """

    # variacao_percentual que dispara cada estrutural assumindo limiar 1%
    _VAR_AUMENTOU = 0.20   # 20% > 1%
    _VAR_REDUZIU = -0.20   # -20% < -1%
    _VAR_ESTAVEL = 0.005   # 0.5% ≤ 1%

    def _run(self, orig: float, comp: float, semantica: str) -> str:
        df = pd.DataFrame({"Mes": ["2025-01", "2025-02"], "Loja": ["A", "A"], "Vendas": [orig, comp]})
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"], semantica=semantica)
        result = executar_v2(mr, config)
        return result.base_analitica.iloc[0]["classificacao_semantica"]

    def _run_nao_aplicavel(self, semantica: str) -> Optional[str]:
        """Força variacao_percentual=None via AUSENTE_ORIGEM (linha existe só
        no comparado · vp=None · tipo_estru=NAO_APLICAVEL na etapa E)."""
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02", "2025-02"],
            "Loja": ["A", "A", "B"],          # B aparece só em 2025-02
            "Vendas": [100.0, 120.0, 500.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"], semantica=semantica)
        result = executar_v2(mr, config)
        ba = result.base_analitica
        linha_ausente = ba[ba["classificacao_estrutural"] == "AUSENTE_ORIGEM"]
        assert not linha_ausente.empty, "fixture AUSENTE_ORIGEM não materializada"
        return linha_ausente.iloc[0]["classificacao_semantica"]

    # MAIOR_MELHOR ----------------------------------------------------------
    def test_maior_melhor_aumentou_positivo(self):
        assert self._run(100.0, 120.0, "MAIOR_MELHOR") == "POSITIVO"

    def test_maior_melhor_reduziu_negativo(self):
        assert self._run(100.0, 80.0, "MAIOR_MELHOR") == "NEGATIVO"

    def test_maior_melhor_estavel_estavel(self):
        # 0.5% < 1% limiar · estrutural ESTAVEL · semantica ESTAVEL
        assert self._run(100.0, 100.5, "MAIOR_MELHOR") == "ESTAVEL"

    def test_maior_melhor_naoaplicavel_naoaplicavel(self):
        assert self._run_nao_aplicavel("MAIOR_MELHOR") == "NAO_APLICAVEL"

    # MENOR_MELHOR ----------------------------------------------------------
    def test_menor_melhor_aumentou_negativo(self):
        assert self._run(100.0, 120.0, "MENOR_MELHOR") == "NEGATIVO"

    def test_menor_melhor_reduziu_positivo(self):
        assert self._run(100.0, 80.0, "MENOR_MELHOR") == "POSITIVO"

    def test_menor_melhor_estavel_estavel(self):
        assert self._run(100.0, 100.5, "MENOR_MELHOR") == "ESTAVEL"

    def test_menor_melhor_naoaplicavel_naoaplicavel(self):
        assert self._run_nao_aplicavel("MENOR_MELHOR") == "NAO_APLICAVEL"

    # NEUTRO · 4 estruturais distintos (D-187) ------------------------------
    def test_neutro_aumentou_aumentou(self):
        assert self._run(100.0, 120.0, "NEUTRO") == "AUMENTOU"

    def test_neutro_reduziu_reduziu(self):
        assert self._run(100.0, 80.0, "NEUTRO") == "REDUZIU"

    def test_neutro_estavel_estavel(self):
        assert self._run(100.0, 100.5, "NEUTRO") == "ESTAVEL"

    def test_neutro_naoaplicavel_naoaplicavel(self):
        assert self._run_nao_aplicavel("NEUTRO") == "NAO_APLICAVEL"

    # ESTADO_SITUACAO · semantica não se aplica -----------------------------
    def test_estado_situacao_sem_classificacao_semantica(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02"],
            "Loja": ["A", "A"],
            "Status": ["Ativo", "Inativo"],
        })
        mr = _motor_result(df)
        config = {
            "estrutura_entrada": "POR_LINHAS",
            "origem_rotulo_tecnico": "2025-01",
            "comparado_rotulo_tecnico": "2025-02",
            "origem_rotulo_ux": "Jan",
            "comparado_rotulo_ux": "Fev",
            "coluna_discriminadora": "Mes",
            "modo_4_ativado": False,
            "estados_nao_escolhidos": [],
            "campo_analisado": "Status",
            "tipo_campo": "ESTADO_SITUACAO",
            "semantica_campo": "NEUTRO",
            "regra_agregacao": "CONTAGEM",
            "metodo_consolidacao_relativo": None,
            "campo_peso": None,
            "modo_pre_agregado": False,
            "agrupadores": ["Loja"],
            "resolucao_estrutural": None,
            "thresholds": {
                "limiar_estabilidade_pct": 0.01,
                "limiar_nulo_massivo_pct": 0.20,
                "limite_valores_discriminador_alerta": 50,
                "limite_variacao_extrema_pct": 10.0,
            },
            "modelo_aplicado": None,
        }
        result = executar_v2(mr, config)
        ba = result.base_analitica
        assert ba.iloc[0].get("classificacao_semantica") is None or pd.isna(ba.iloc[0].get("classificacao_semantica", None))


class TestEtapaF:
    def test_numeros_ancora_numericos(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02", "2025-01", "2025-02"],
            "Loja": ["A", "A", "B", "B"],
            "Vendas": [100.0, 120.0, 200.0, 180.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        na = result.numeros_ancora
        assert na.total_origem == pytest.approx(300.0)
        assert na.total_comparado == pytest.approx(300.0)
        assert na.diferenca_total == pytest.approx(0.0)
        assert na.total_combinacoes_analisadas is None

    def test_numeros_ancora_estado_situacao(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02", "2025-01", "2025-02"],
            "Loja": ["A", "A", "B", "B"],
            "Status": ["Ativo", "Inativo", "Ativo", "Ativo"],
        })
        mr = _motor_result(df)
        config = {
            "estrutura_entrada": "POR_LINHAS",
            "origem_rotulo_tecnico": "2025-01",
            "comparado_rotulo_tecnico": "2025-02",
            "origem_rotulo_ux": "Jan",
            "comparado_rotulo_ux": "Fev",
            "coluna_discriminadora": "Mes",
            "modo_4_ativado": False,
            "estados_nao_escolhidos": [],
            "campo_analisado": "Status",
            "tipo_campo": "ESTADO_SITUACAO",
            "semantica_campo": "NEUTRO",
            "regra_agregacao": "CONTAGEM",
            "metodo_consolidacao_relativo": None,
            "campo_peso": None,
            "modo_pre_agregado": False,
            "agrupadores": ["Loja"],
            "resolucao_estrutural": None,
            "thresholds": {
                "limiar_estabilidade_pct": 0.01,
                "limiar_nulo_massivo_pct": 0.20,
                "limite_valores_discriminador_alerta": 50,
                "limite_variacao_extrema_pct": 10.0,
            },
            "modelo_aplicado": None,
        }
        result = executar_v2(mr, config)
        na = result.numeros_ancora
        assert na.total_combinacoes_analisadas == 2
        assert na.combinacoes_com_mudanca == 1
        assert na.total_origem is None


# ---------------------------------------------------------------------------
# GRUPO 2 · Integração E2E com base_v2_cliente.xlsx
# ---------------------------------------------------------------------------


class TestIntegracaoE2E:
    def test_v2_a01_ausentes_em_produto(self, result_v2_integracao):
        assertions = _carregar_assertions_v2()
        a01 = next(a for a in assertions if a["id"] == "V2-A01")
        min_val = a01["esperado"]["min"]
        max_val = a01["esperado"]["max"]

        ba = result_v2_integracao.base_analitica
        ausentes = ba[ba["classificacao_estrutural"].isin(["AUSENTE_ORIGEM", "AUSENTE_COMPARADO"])]
        n_produtos = int(ausentes["Produto"].nunique()) if "Produto" in ausentes.columns else 0
        assert min_val <= n_produtos <= max_val, (
            f"V2-A01: esperado {min_val}-{max_val} produtos ausentes, obtido {n_produtos}"
        )
        warning_codes = [w.codigo for w in result_v2_integracao.warnings]
        assert a01["warning_associado"] in warning_codes, (
            f"V2-A01: warning {a01['warning_associado']} não emitido"
        )

    def test_v2_a02_warning_nulo_medida(self, result_v2_integracao):
        assertions = _carregar_assertions_v2()
        a02 = next(a for a in assertions if a["id"] == "V2-A02")
        min_val = a02["esperado"]["min"]
        max_val = a02["esperado"]["max"]
        warning_code = a02["esperado"]["warning_code"]

        nulo_warns = [w for w in result_v2_integracao.warnings if w.codigo == warning_code]
        assert len(nulo_warns) >= 1, f"V2-A02: warning {warning_code} não emitido"

        # Contar linhas com nulo na medida
        ba = result_v2_integracao.base_analitica
        n_nulos = int(
            ba["classificacao_estrutural"]
            .isin(["NULO_ORIGEM", "NULO_COMPARADO", "NULO_AMBOS"])
            .sum()
        )
        assert min_val <= n_nulos <= max_val, (
            f"V2-A02: esperado {min_val}-{max_val} nulos, obtido {n_nulos}"
        )

    def test_v2_a03_estrutura_saida(self, result_v2_integracao):
        assertions = _carregar_assertions_v2()
        a03 = next(a for a in assertions if a["id"] == "V2-A03")

        re = result_v2_integracao.resumo_executivo
        campos_re = [
            re.bloco_1_cabecalho,
            re.bloco_2_numeros_ancora,
            re.bloco_3_distribuicao,
            re.bloco_4_elementos_destacados,
            re.bloco_5_leitura_qualitativa,
            re.bloco_6_qualidade_estrutural,
        ]
        n_blocos = sum(1 for b in campos_re if b is not None)
        assert n_blocos == a03["esperado"]["resumo_blocos"], (
            f"V2-A03: esperado {a03['esperado']['resumo_blocos']} blocos RE, obtido {n_blocos}"
        )
        assert result_v2_integracao.coracao_visual.nome_aba == a03["esperado"]["coracao_visual"], (
            f"V2-A03: coracao_visual.nome_aba esperado '{a03['esperado']['coracao_visual']}', "
            f"obtido '{result_v2_integracao.coracao_visual.nome_aba}'"
        )

    def test_v2_a04_discriminador_dois_estados(self):
        assertions = _carregar_assertions_v2()
        a04 = next(a for a in assertions if a["id"] == "V2-A04")
        coluna = a04["coluna"]
        aba = a04["aba"]
        esperado = a04["esperado"]["valor"]

        df = pd.read_excel(str(BASE_V2_PATH), sheet_name=aba)
        n_estados = int(df[coluna].nunique())
        assert n_estados == esperado, (
            f"V2-A04: esperado {esperado} estado(s) em '{coluna}', obtido {n_estados}"
        )


# ---------------------------------------------------------------------------
# GRUPO 3 · Catálogo MBO (10 bloqueios)
# ---------------------------------------------------------------------------


class TestCatalogoBloqueios:
    def _assert_bloqueio(self, result: V2Result, codigo: str) -> BloqueioOperacional:
        matches = [b for b in result.bloqueios_disparados if b.codigo == codigo]
        assert matches, f"Bloqueio {codigo} não encontrado em {[b.codigo for b in result.bloqueios_disparados]}"
        b = matches[0]
        assert b.escapavel is False
        assert b.escape_acionado is None
        assert b.warning_pos_escape is None
        return b

    def test_b_arquivo_ilegivel(self):
        mr = _motor_result(pd.DataFrame())
        config = _config_base()
        result = executar_v2(mr, config)
        b = self._assert_bloqueio(result, "B-V2-ARQUIVO-ILEGIVEL")
        assert "formato_detectado" in b.contexto_disparo

    def test_b_estrutura_invalida(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02"],
            "Loja": ["A", "A"],
        })
        mr = _motor_result(df)
        config = _config_base()  # campo_analisado='Vendas' que não existe
        result = executar_v2(mr, config)
        b = self._assert_bloqueio(result, "B-V2-ESTRUTURA-INVALIDA")
        assert "colunas_numericas" in b.contexto_disparo

    def test_b_discriminador_0(self):
        df = pd.DataFrame({"Mes": [None, None], "Loja": ["A", "B"], "Vendas": [1.0, 2.0]})
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        b = self._assert_bloqueio(result, "B-V2-DISCRIMINADOR-0")
        assert "coluna_discriminadora" in b.contexto_disparo

    def test_b_discriminador_1(self):
        df = pd.DataFrame({"Mes": ["2025-01"] * 4, "Loja": list("ABCD"), "Vendas": [1.0] * 4})
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        b = self._assert_bloqueio(result, "B-V2-DISCRIMINADOR-1")
        assert "valor_unico" in b.contexto_disparo

    def test_b_campo_100_nulo(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02"],
            "Loja": ["A", "A"],
            "Vendas": [None, 120.0],
        })
        # Para testar 100% nulo na origem: todas as linhas de 2025-01 têm null
        df_100 = pd.DataFrame({
            "Mes": ["2025-01", "2025-01", "2025-02", "2025-02"],
            "Loja": ["A", "B", "A", "B"],
            "Vendas": [None, None, 100.0, 200.0],
        })
        mr = _motor_result(df_100)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        b = self._assert_bloqueio(result, "B-V2-CAMPO-100-NULO")
        assert "lado_vazio" in b.contexto_disparo

    def test_b_agrup_excesso(self):
        df = pd.DataFrame({"Mes": ["2025-01", "2025-02"], **{f"C{i}": ["A", "B"] for i in range(10)}, "Vendas": [1.0, 2.0]})
        mr = _motor_result(df)
        config = _config_base(agrupadores=[f"C{i}" for i in range(10)])
        result = executar_v2(mr, config)
        b = self._assert_bloqueio(result, "B-V2-AGRUP-EXCESSO")
        assert b.contexto_disparo.get("n_agrupadores", 0) >= 10

    def test_b_peso_invalido(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02"],
            "Loja": ["A", "A"],
            "Taxa": [0.05, 0.04],
            "Peso": [0.0, 0.0],
        })
        mr = _motor_result(df)
        config = {
            "estrutura_entrada": "POR_LINHAS",
            "origem_rotulo_tecnico": "2025-01",
            "comparado_rotulo_tecnico": "2025-02",
            "origem_rotulo_ux": "Jan",
            "comparado_rotulo_ux": "Fev",
            "coluna_discriminadora": "Mes",
            "modo_4_ativado": False,
            "estados_nao_escolhidos": [],
            "campo_analisado": "Taxa",
            "tipo_campo": "NUMERICO_RELATIVO",
            "semantica_campo": "NEUTRO",
            "regra_agregacao": "MEDIA",
            "metodo_consolidacao_relativo": "MEDIA_PONDERADA",
            "campo_peso": "Peso",
            "modo_pre_agregado": False,
            "agrupadores": ["Loja"],
            "resolucao_estrutural": None,
            "thresholds": {
                "limiar_estabilidade_pct": 0.01,
                "limiar_nulo_massivo_pct": 0.20,
                "limite_valores_discriminador_alerta": 50,
                "limite_variacao_extrema_pct": 10.0,
            },
            "modelo_aplicado": None,
        }
        result = executar_v2(mr, config)
        b = self._assert_bloqueio(result, "B-V2-PESO-INVALIDO")
        assert "campo_peso" in b.contexto_disparo

    def test_b_consol_impossivel(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02"],
            "Loja": ["A", "A"],
            "Taxa": [0.05, 0.04],
        })
        mr = _motor_result(df)
        config = {
            "estrutura_entrada": "POR_LINHAS",
            "origem_rotulo_tecnico": "2025-01",
            "comparado_rotulo_tecnico": "2025-02",
            "origem_rotulo_ux": "Jan",
            "comparado_rotulo_ux": "Fev",
            "coluna_discriminadora": "Mes",
            "modo_4_ativado": False,
            "estados_nao_escolhidos": [],
            "campo_analisado": "Taxa",
            "tipo_campo": "NUMERICO_RELATIVO",
            "semantica_campo": "NEUTRO",
            "regra_agregacao": "MEDIA",
            "metodo_consolidacao_relativo": "NAO_CONSOLIDAR",
            "campo_peso": None,
            "modo_pre_agregado": False,
            "agrupadores": ["Loja"],
            "resolucao_estrutural": None,
            "thresholds": {
                "limiar_estabilidade_pct": 0.01,
                "limiar_nulo_massivo_pct": 0.20,
                "limite_valores_discriminador_alerta": 50,
                "limite_variacao_extrema_pct": 10.0,
            },
            "modelo_aplicado": None,
        }
        result = executar_v2(mr, config)
        b = self._assert_bloqueio(result, "B-V2-CONSOL-IMPOSSIVEL")
        assert "agrupadores_declarados" in b.contexto_disparo

    def test_b_resultado_excede(self):
        # Criar df com produto cartesiano estimado > 500.000
        # 1000 lojas × 501 produtos = 501.000 > 500.000
        n_lojas = 300
        n_produtos = 170  # 300 × 170 = 51.000 (precisa mais)
        # Usar outer join criando ausências para forçar > 500K
        # Alternativa simples: criar um df que após outer join resulta em muitas linhas
        # Com 710 lojas × 710 produtos > 504.100 > 500.000
        lojas = [f"L{i:04d}" for i in range(710)]
        produtos = [f"P{i:04d}" for i in range(710)]
        # 710 lojas em origem, 710 produtos diferentes em comparado → outer join = 710×710 = 504.100
        df_orig = pd.DataFrame({
            "Loja": lojas,
            "Produto": [f"P{i:04d}" for i in range(710)],
            "Mes": ["2025-01"] * 710,
            "Vendas": [100.0] * 710,
        })
        df_comp = pd.DataFrame({
            "Loja": [f"L{i+710:04d}" for i in range(710)],
            "Produto": [f"P{i+710:04d}" for i in range(710)],
            "Mes": ["2025-02"] * 710,
            "Vendas": [120.0] * 710,
        })
        df = pd.concat([df_orig, df_comp], ignore_index=True)
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja", "Produto"])
        result = executar_v2(mr, config)
        b = self._assert_bloqueio(result, "B-V2-RESULTADO-EXCEDE")
        assert b.contexto_disparo.get("linhas_estimadas", 0) > 500_000

    def test_b_caso_estrutural_cancelado(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02"],
            "Loja": ["A", "A"],
            "Vendas": [100.0, 120.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        config["resolucao_estrutural"] = {
            "tipo_caso": "NIVEL_AGRUPAMENTO_DIFERENTE",
            "opcoes_oferecidas": ["agregar", "cancelar"],
            "escolha_usuario": "cancelar",
            "contexto_caso": {"detalhe": "granularidade diferente"},
            "registrada_como": "DECISAO_USUARIO",
        }
        result = executar_v2(mr, config)
        b = self._assert_bloqueio(result, "B-V2-CASO-ESTRUTURAL-CANCELADO")
        assert "tipo_caso" in b.contexto_disparo


# ---------------------------------------------------------------------------
# GRUPO 4 · Catálogo warnings
# ---------------------------------------------------------------------------


class TestCatalogoWarnings:
    def _codes(self, result: V2Result) -> List[str]:
        return [w.codigo for w in result.warnings]

    def test_w_ausente_em_um_lado(self):
        # B presente em 2025-01 mas ausente em 2025-02 → W-V2-AUSENTE-EM-UM-LADO
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-01", "2025-02"],
            "Loja": ["A", "B", "A"],
            "Vendas": [100.0, 200.0, 110.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        assert "W-V2-AUSENTE-EM-UM-LADO" in self._codes(result)

    def test_w_nulo_medida(self):
        # Loja B garante que origem não é 100% nula (evita B-V2-CAMPO-100-NULO)
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-01", "2025-02", "2025-02"],
            "Loja": ["A", "B", "A", "B"],
            "Vendas": [None, 200.0, 120.0, 150.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        assert "W-NULO-MEDIDA" in self._codes(result)

    def test_w_bz(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02"],
            "Loja": ["A", "A"],
            "Vendas": [0.0, 100.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        assert "W-V2-BZ" in self._codes(result)

    def test_w_null_mass(self):
        n = 20
        df = pd.DataFrame({
            "Mes": ["2025-01"] * n + ["2025-02"] * n,
            "Loja": list(range(n)) * 2,
            "Vendas": [None] * 18 + [100.0] * 2 + [100.0] * n,
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        config["thresholds"]["limiar_nulo_massivo_pct"] = 0.50
        result = executar_v2(mr, config)
        assert "W-V2-NULL-MASS" in self._codes(result)

    def test_w_agg_relativo(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02"],
            "Loja": ["A", "A"],
            "Taxa": [0.05, 0.04],
        })
        mr = _motor_result(df)
        config = {
            "estrutura_entrada": "POR_LINHAS",
            "origem_rotulo_tecnico": "2025-01",
            "comparado_rotulo_tecnico": "2025-02",
            "origem_rotulo_ux": "Jan",
            "comparado_rotulo_ux": "Fev",
            "coluna_discriminadora": "Mes",
            "modo_4_ativado": False,
            "estados_nao_escolhidos": [],
            "campo_analisado": "Taxa",
            "tipo_campo": "NUMERICO_RELATIVO",
            "semantica_campo": "NEUTRO",
            "regra_agregacao": "MEDIA",
            "metodo_consolidacao_relativo": "MEDIA_SIMPLES",
            "campo_peso": None,
            "modo_pre_agregado": False,
            "agrupadores": ["Loja"],
            "resolucao_estrutural": None,
            "thresholds": {
                "limiar_estabilidade_pct": 0.01,
                "limiar_nulo_massivo_pct": 0.20,
                "limite_valores_discriminador_alerta": 50,
                "limite_variacao_extrema_pct": 10.0,
            },
            "modelo_aplicado": None,
        }
        result = executar_v2(mr, config)
        assert "W-V2-AGG" in self._codes(result)

    def test_w_mix_tipos(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", 2025, "2025-02"],
            "Loja": ["A", "A", "A"],
            "Vendas": [100.0, 200.0, 150.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        assert "W-V2-MIX" in self._codes(result)

    def test_w_nmany(self):
        # 60 valores intermediários + "2025-01" + "2025-02" = 62 únicos > 50 → W-V2-NMANY
        vals = [f"v{i}" for i in range(60)]
        df = pd.DataFrame({
            "Mes": ["2025-01"] + vals + ["2025-02"],
            "Loja": ["A"] * 62,
            "Vendas": [100.0] * 62,
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        config["thresholds"]["limite_valores_discriminador_alerta"] = 50
        result = executar_v2(mr, config)
        assert "W-V2-NMANY" in self._codes(result)

    def test_w_agrup_muitos(self):
        cols = {f"C{i}": ["A", "A", "B", "B"] for i in range(6)}
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02", "2025-01", "2025-02"],
            **cols,
            "Vendas": [100.0, 120.0, 200.0, 180.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=[f"C{i}" for i in range(6)])
        result = executar_v2(mr, config)
        assert "W-V2-AGRUP-MUITOS" in self._codes(result)

    def test_w_mod_parcial(self):
        from transversais.t_modelo import ModeloConfig, limpar_store, salvar_modelo

        limpar_store()
        mc = ModeloConfig(
            nome_modelo="modelo_teste_parcial",
            visao_origem="V2",
            agrupadores=["ColunaInexistente"],
            campos_principais={"campo_analisado": "Vendas"},
        )
        mid = salvar_modelo(mc)

        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02"],
            "Loja": ["A", "A"],
            "Vendas": [100.0, 120.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        config["modelo_aplicado"] = {"modelo_id": mid}
        result = executar_v2(mr, config)
        limpar_store()
        assert "W-V2-MOD-PARCIAL" in self._codes(result)

    def test_w_mod_incomp(self):
        from transversais.t_modelo import ModeloConfig, limpar_store, salvar_modelo

        limpar_store()
        mc = ModeloConfig(
            nome_modelo="modelo_incompativel",
            visao_origem="V3",  # incompatível com V2
            agrupadores=["Loja"],
            campos_principais={},
        )
        mid = salvar_modelo(mc)

        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02"],
            "Loja": ["A", "A"],
            "Vendas": [100.0, 120.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        config["modelo_aplicado"] = {"modelo_id": mid}
        result = executar_v2(mr, config)
        limpar_store()
        assert "W-V2-MOD-INCOMP" in self._codes(result)

    def test_w_ajuste_leve_nulos_agrupador(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-01", "2025-02", "2025-02"],
            "Loja": ["A", None, "A", None],
            "Vendas": [100.0, 50.0, 120.0, 60.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        result = executar_v2(mr, config)
        assert "W-V2-AJUSTE-LEVE" in self._codes(result)

    def test_w_decisao_usuario(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02"],
            "Loja": ["A", "A"],
            "Vendas": [100.0, 120.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        config["resolucao_estrutural"] = {
            "tipo_caso": "ORDEM_MAGNITUDE_DIVERGENTE",
            "opcoes_oferecidas": ["seguir mesmo assim", "cancelar"],
            "escolha_usuario": "seguir mesmo assim",
            "contexto_caso": {},
            "registrada_como": "DECISAO_USUARIO",
        }
        result = executar_v2(mr, config)
        assert "W-V2-DECISAO-USUARIO" in self._codes(result)

    def test_w_pagreg_dup(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-01", "2025-02"],
            "Loja": ["A", "A", "A"],
            "Vendas": [100.0, 50.0, 120.0],
        })
        mr = _motor_result(df)
        config = _config_base(agrupadores=["Loja"])
        config["modo_pre_agregado"] = True
        result = executar_v2(mr, config)
        assert "W-V2-PAGREG-DUP" in self._codes(result)


# ---------------------------------------------------------------------------
# GRUPO 5 · Determinismo + Receptividade IA
# ---------------------------------------------------------------------------


class TestDeterminismoIA:
    def _run_twice(self, df: pd.DataFrame, config: Dict[str, Any]):
        mr = _motor_result(df)
        r1 = executar_v2(mr, config)
        mr2 = _motor_result(df)
        r2 = executar_v2(mr2, config)
        return r1, r2

    def test_determinismo_c1(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02", "2025-01", "2025-02"],
            "Loja": ["A", "A", "B", "B"],
            "Vendas": [100.0, 120.0, 200.0, 180.0],
        })
        config = _config_base(agrupadores=["Loja"])
        r1, r2 = self._run_twice(df, config)

        # base_analitica idêntica
        ba1 = r1.base_analitica.reset_index(drop=True)
        ba2 = r2.base_analitica.reset_index(drop=True)
        assert list(ba1.columns) == list(ba2.columns)
        for col in ba1.columns:
            s1 = ba1[col].fillna("__NAN__").tolist()
            s2 = ba2[col].fillna("__NAN__").tolist()
            assert s1 == s2, f"Coluna {col} diverge entre execuções"

        # numeros_ancora idênticos
        assert r1.numeros_ancora.model_dump() == r2.numeros_ancora.model_dump()

        # top_variacoes idênticas
        assert len(r1.top_variacoes) == len(r2.top_variacoes)

        # bloqueios e warnings idênticos
        assert [b.codigo for b in r1.bloqueios_disparados] == [b.codigo for b in r2.bloqueios_disparados]
        assert [w.codigo for w in r1.warnings] == [w.codigo for w in r2.warnings]

    def test_receptividade_ia_d130(self):
        df = pd.DataFrame({
            "Mes": ["2025-01", "2025-02", "2025-01", "2025-02"],
            "Loja": ["A", "A", "B", "B"],
            "Vendas": [100.0, 120.0, 200.0, 180.0],
        })
        config = _config_base(agrupadores=["Loja"])
        mr = _motor_result(df)
        result = executar_v2(mr, config)

        ctx = result.para_contexto_ia()
        assert isinstance(ctx, dict)
        # Deve ser JSON-serializável
        serialized = json.dumps(ctx, default=str)
        assert len(serialized) > 0

        # Verificar campos esperados
        assert "visao_id" in ctx
        assert ctx["visao_id"] == "V2"
        assert "resumo_executivo" in ctx
        assert "coracao_visual" in ctx


# ---------------------------------------------------------------------------
# GRUPO ECP · Patamares de cardinalidade
# ---------------------------------------------------------------------------


class TestECP:
    def test_patamar_agrupadores(self):
        assert _classificar_patamar_agrupadores(1) == "P1-AGRUP-NORMAL"
        assert _classificar_patamar_agrupadores(3) == "P1-AGRUP-NORMAL"
        assert _classificar_patamar_agrupadores(4) == "P2-AGRUP-ALERTA-LEVE"
        assert _classificar_patamar_agrupadores(5) == "P2-AGRUP-ALERTA-LEVE"
        assert _classificar_patamar_agrupadores(6) == "P3-AGRUP-ALERTA-FORTE"
        assert _classificar_patamar_agrupadores(8) == "P3-AGRUP-ALERTA-FORTE"
        assert _classificar_patamar_agrupadores(9) == "P4-AGRUP-BLOQUEIO"

    def test_patamar_discriminador(self):
        assert _classificar_patamar_discriminador(2, 50) == "P1-DISCR-NORMAL"
        assert _classificar_patamar_discriminador(5, 50) == "P2-DISCR-ALERTA-LEVE"
        assert _classificar_patamar_discriminador(30, 50) == "P3-DISCR-ALERTA-FORTE"
        assert _classificar_patamar_discriminador(51, 50) == "P4-DISCR-BLOQUEIO-LEVE"

    def test_patamar_resultado(self):
        assert _classificar_patamar_resultado(5_000) == "P1-RES-NORMAL"
        assert _classificar_patamar_resultado(50_000) == "P2-RES-ALERTA-LEVE"
        assert _classificar_patamar_resultado(200_000) == "P3-RES-ALERTA-FORTE"
        assert _classificar_patamar_resultado(600_000) == "P4-RES-BLOQUEIO"
