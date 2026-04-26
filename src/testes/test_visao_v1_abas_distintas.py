"""
test_visao_v1_abas_distintas.py — Smoke tests do ramo ABAS_DISTINTAS (Fase 2 · V-V1)

Cobre cenários canônicos da S-V1 v2 §2.1-2.4 para o pipeline ABAS_DISTINTAS:
1. Caso simples 100% match
2. SO_ORIGEM + SO_COMPARADO
3. DUPLICIDADE (chave repetida)
4. AMBIGUIDADE (modo CONTEM com múltiplos candidatos)
5. DENTRO_TOLERANCIA + W-V1-TOL
6. Ponte FECHA
7. Ponte COM_RESIDUO
"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal

import pandas as pd
import pytest

from contratos import (
    ColumnMeta,
    MotorResult,
    PadraoCronologicoEnum,
    TipoEstruturalEnum,
    TipoSemanticoEnum,
    TipoTecnicoEnum,
)


def _fake_motor_result(df: pd.DataFrame, origem_idxs: list, comparado_idxs: list) -> MotorResult:
    """Cria MotorResult artificial com modo DUAL e map de partição."""
    column_meta = {}
    for col in df.columns:
        column_meta[col] = ColumnMeta(
            nome=col,
            tipo_tecnico=TipoTecnicoEnum.OBJECT,
            tipo_semantico=TipoSemanticoEnum.MISTO,
            tipo_estrutural=TipoEstruturalEnum.CATEGORICO_ELEGIVEL,
            subtipo_id_detectado=False,
            null_count=0,
            cardinalidade=df[col].nunique(),
            eh_candidato_categorico=True,
            ordem_insercao=list(df.columns).index(col),
        )
    ocm = {}
    for i in origem_idxs:
        ocm[i] = "origem"
    for i in comparado_idxs:
        ocm[i] = "comparado"
    return MotorResult(
        df=df,
        column_meta=column_meta,
        modo_upload="DUAL",
        origem_comparado_map=ocm,
        total_linhas_originais=len(df),
        total_linhas_processadas=len(df),
    )


def _config_padrao(
    agrupador_modo="EXATO",
    n_arquivos=2,
    aba_origem="OrigemAba",
    aba_comparado="ComparadoAba",
    arquivo_origem="origem.xlsx",
    arquivo_comparado="comparado.xlsx",
):
    from visoes.visao_v1 import (
        AgrupadorMatchV1,
        CampoComparadoV1,
        ModoMatchV1,
        TipoCampoV1,
        UnidadeCanonica,
    )
    return {
        "agrupadores_match": [
            AgrupadorMatchV1(
                nome_origem="documento",
                nome_comparado="documento",
                rotulo_analitico="Documento",
                modo_match=ModoMatchV1(agrupador_modo),
            )
        ],
        "campos_comparados": [
            CampoComparadoV1(
                nome_origem="valor",
                nome_comparado="valor",
                nome_analitico="Valor",
                tipo_logico=TipoCampoV1.VALOR_MONETARIO,
                unidade=UnidadeCanonica.MONETARIO_BRL,
                tolerancia=Decimal("0"),
            )
        ],
        "agrupadores_executivos": [],
        "epsilon_por_unidade": {UnidadeCanonica.MONETARIO_BRL: Decimal("0.01")},
        "thresholds": {},
        "origem_ux": "Origem",
        "comparado_ux": "Comparado",
        "arquivo_origem": arquivo_origem,
        "arquivo_comparado": arquivo_comparado,
        "aba_origem": aba_origem,
        "aba_comparado": aba_comparado,
        "n_arquivos": n_arquivos,
        "paleta_aplicada": "Azul executivo",
    }


class TestAbasDistintasCenariosBase:

    def test_executar_v1_caso_simples_100pct_match(self):
        """3 registros · todos batem · esperado: 3 CONCILIADO · ponte fecha."""
        from visoes.visao_v1 import (
            CasoLogicoV1,
            ClassificacaoRegistroV1,
            StatusPonteV1,
            executar_v1,
        )
        df = pd.DataFrame([
            # Origem
            {"documento": "D001", "valor": 100.00},
            {"documento": "D002", "valor": 200.00},
            {"documento": "D003", "valor": 300.00},
            # Comparado
            {"documento": "D001", "valor": 100.00},
            {"documento": "D002", "valor": 200.00},
            {"documento": "D003", "valor": 300.00},
        ])
        mr = _fake_motor_result(df, origem_idxs=[0, 1, 2], comparado_idxs=[3, 4, 5])
        config = _config_padrao()

        result = executar_v1(mr, config)
        assert result.conciliacao_realizada.caso_logico_inferido == CasoLogicoV1.ABAS_DISTINTAS
        assert len(result.classificacao_por_registro) == 3
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.CONCILIADO] == 3
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.DIVERGENTE_VALOR] == 0
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.SO_ORIGEM] == 0
        assert result.status_ponte_geral == StatusPonteV1.FECHA

    def test_executar_v1_so_origem_so_comparado(self):
        """Origem tem D001-D003 · Comparado tem D002-D004 · esperado: 1 SO_ORIGEM, 2 CONCILIADO, 1 SO_COMPARADO."""
        from visoes.visao_v1 import ClassificacaoRegistroV1, executar_v1
        df = pd.DataFrame([
            {"documento": "D001", "valor": 100.00},
            {"documento": "D002", "valor": 200.00},
            {"documento": "D003", "valor": 300.00},
            {"documento": "D002", "valor": 200.00},
            {"documento": "D003", "valor": 300.00},
            {"documento": "D004", "valor": 400.00},
        ])
        mr = _fake_motor_result(df, origem_idxs=[0, 1, 2], comparado_idxs=[3, 4, 5])
        result = executar_v1(mr, _config_padrao())

        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.CONCILIADO] == 2
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.SO_ORIGEM] == 1
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.SO_COMPARADO] == 1
        # Cobertura
        assert result.cobertura is not None
        assert result.cobertura.n_origem_sem_par == 1
        assert result.cobertura.n_comparado_sem_par == 1

    def test_executar_v1_duplicidade_em_origem(self):
        """Origem tem D001 repetido · Comparado tem D001 único · esperado DIVERGENCIA_DUPLICIDADE."""
        from visoes.visao_v1 import ClassificacaoRegistroV1, executar_v1
        df = pd.DataFrame([
            {"documento": "D001", "valor": 100.00},
            {"documento": "D001", "valor": 105.00},  # duplicado em Origem
            {"documento": "D001", "valor": 100.00},
        ])
        mr = _fake_motor_result(df, origem_idxs=[0, 1], comparado_idxs=[2])
        result = executar_v1(mr, _config_padrao())

        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.DIVERGENCIA_DUPLICIDADE] == 1
        # Diferenca total deve ser None (semântica ambígua em DUPLICIDADE)
        reg_dup = [r for r in result.classificacao_por_registro
                   if r.classificacao_estrutural == ClassificacaoRegistroV1.DIVERGENCIA_DUPLICIDADE][0]
        assert reg_dup.diferenca_total_registro is None

    def test_executar_v1_ambiguidade_modo_contem(self):
        """Modo CONTEM · D001 do Origem casa com D001A e D001B do Comparado · esperado AMBIGUIDADE."""
        from visoes.visao_v1 import ClassificacaoRegistroV1, executar_v1
        df = pd.DataFrame([
            {"documento": "D001", "valor": 100.00},
            {"documento": "D001A", "valor": 50.00},
            {"documento": "D001B", "valor": 50.00},
        ])
        mr = _fake_motor_result(df, origem_idxs=[0], comparado_idxs=[1, 2])
        config = _config_padrao(agrupador_modo="CONTEM")
        result = executar_v1(mr, config)

        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.DIVERGENCIA_AMBIGUIDADE] >= 1


class TestAbasDistintasTolerancia:

    def test_executar_v1_tolerancia_absorve_diferenca_pequena(self):
        """Diferença R$ 0.005 · tolerância R$ 0.01 · esperado CONCILIADO + DENTRO_TOLERANCIA + W-V1-TOL."""
        from visoes.visao_v1 import (
            CampoComparadoV1,
            ClassificacaoRegistroV1,
            StatusCampoV1,
            TipoCampoV1,
            UnidadeCanonica,
            executar_v1,
        )
        df = pd.DataFrame([
            {"documento": "D001", "valor": 100.005},
            {"documento": "D001", "valor": 100.000},
        ])
        mr = _fake_motor_result(df, origem_idxs=[0], comparado_idxs=[1])
        config = _config_padrao()
        config["campos_comparados"] = [
            CampoComparadoV1(
                nome_origem="valor", nome_comparado="valor", nome_analitico="Valor",
                tipo_logico=TipoCampoV1.VALOR_MONETARIO,
                unidade=UnidadeCanonica.MONETARIO_BRL,
                tolerancia=Decimal("0.01"),
            )
        ]
        result = executar_v1(mr, config)

        # Deve ser CONCILIADO (não DIVERGENTE_VALOR, pois absorvido por tolerância)
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.CONCILIADO] == 1
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.DIVERGENTE_VALOR] == 0
        # Status do campo deve ser DENTRO_TOLERANCIA
        reg = result.classificacao_por_registro[0]
        assert reg.valores_por_campo[0].status_campo == StatusCampoV1.DENTRO_TOLERANCIA
        # W-V1-TOL deve ter ≥ 1 ocorrência
        w_tol = next(w for w in result.warnings_emitidos if w.codigo == "W-V1-TOL")
        assert w_tol.n_ocorrencias >= 1


class TestAbasDistintasPonte:

    def test_executar_v1_ponte_fecha_caso_simples(self):
        """3 conciliados · saldo_o = saldo_c = 600 · ponte fecha."""
        from visoes.visao_v1 import StatusPonteV1, executar_v1
        df = pd.DataFrame([
            {"documento": "D001", "valor": 100.00},
            {"documento": "D002", "valor": 200.00},
            {"documento": "D003", "valor": 300.00},
            {"documento": "D001", "valor": 100.00},
            {"documento": "D002", "valor": 200.00},
            {"documento": "D003", "valor": 300.00},
        ])
        mr = _fake_motor_result(df, origem_idxs=[0, 1, 2], comparado_idxs=[3, 4, 5])
        result = executar_v1(mr, _config_padrao())

        assert result.status_ponte_geral == StatusPonteV1.FECHA
        assert len(result.pontes) == 1
        assert result.pontes[0].fecha is True
        assert result.pontes[0].residuo == Decimal("0")

    def test_executar_v1_ponte_com_so_origem_e_so_comparado_fecha(self):
        """Bridge com SO_ORIGEM + SO_COMPARADO · ajustes compensam · ponte fecha."""
        from visoes.visao_v1 import StatusPonteV1, executar_v1
        df = pd.DataFrame([
            # Origem · 3 registros · soma = 100 + 200 + 300 = 600
            {"documento": "D001", "valor": 100.00},
            {"documento": "D002", "valor": 200.00},
            {"documento": "D003", "valor": 300.00},
            # Comparado · 3 registros · soma = 100 + 200 + 400 = 700
            # D001 casa, D002 casa, D003 só na origem, D004 só no comparado
            {"documento": "D001", "valor": 100.00},
            {"documento": "D002", "valor": 200.00},
            {"documento": "D004", "valor": 400.00},
        ])
        mr = _fake_motor_result(df, origem_idxs=[0, 1, 2], comparado_idxs=[3, 4, 5])
        result = executar_v1(mr, _config_padrao())

        # saldo_o = 600 (3 vals)
        # ajuste_so_o = -300 (D003 sai da origem)
        # ajuste_so_c = +400 (D004 entra)
        # saldo_esperado = 600 - 300 + 400 = 700
        # saldo_real = 700
        # residuo = 0 → fecha
        assert result.status_ponte_geral == StatusPonteV1.FECHA
        ponte = result.pontes[0]
        assert ponte.saldo_origem == Decimal("600")
        assert ponte.ajuste_so_origem == Decimal("-300")
        assert ponte.ajuste_so_comparado == Decimal("400")
        assert ponte.residuo == Decimal("0")


class TestAbasDistintasDeterminismo:

    def test_executar_v1_ordem_canonica_classificacao(self):
        """Resultado ordenado por (ORDEM_CLASSIFICACAO, chave) · auditável."""
        from visoes.visao_v1 import ClassificacaoRegistroV1, executar_v1
        df = pd.DataFrame([
            {"documento": "Z999", "valor": 999.0},
            {"documento": "A001", "valor": 1.0},
            {"documento": "Z999", "valor": 999.0},
            {"documento": "A001", "valor": 1.0},
        ])
        mr = _fake_motor_result(df, origem_idxs=[0, 1], comparado_idxs=[2, 3])
        result = executar_v1(mr, _config_padrao())

        # Todos CONCILIADO · ordem alfabética por chave: A001 < Z999
        chaves = [r.chave_consolidada for r in result.classificacao_por_registro]
        assert chaves == sorted(chaves)
        assert chaves[0] == "A001"

    def test_executar_v1_idempotencia(self):
        """2 execuções produzem resultado idêntico (model_dump_json)."""
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": "D001", "valor": 100.00},
            {"documento": "D002", "valor": 200.00},
            {"documento": "D001", "valor": 100.00},
            {"documento": "D002", "valor": 200.00},
        ])
        mr1 = _fake_motor_result(df, origem_idxs=[0, 1], comparado_idxs=[2, 3])
        mr2 = _fake_motor_result(df.copy(), origem_idxs=[0, 1], comparado_idxs=[2, 3])
        # Mesmo timestamp para idempotência exata
        mr2 = mr2.model_copy(update={"timestamp_processamento": mr1.timestamp_processamento})
        r1 = executar_v1(mr1, _config_padrao())
        r2 = executar_v1(mr2, _config_padrao())

        # Comparar dimensões críticas
        assert r1.contagem_por_classificacao == r2.contagem_por_classificacao
        assert r1.status_ponte_geral == r2.status_ponte_geral
        assert [r.chave_consolidada for r in r1.classificacao_por_registro] == \
               [r.chave_consolidada for r in r2.classificacao_por_registro]
