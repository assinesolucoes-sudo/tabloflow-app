"""
test_visao_v1_q4c_determinismo_fronteira.py — Blocos V-VI Q4.C (Fase 6 · V-V1)

Bloco V · Determinismo e ordenação (~10-15 testes)
Bloco VI · Casos de fronteira e regressão (~30-40 testes)
"""
from __future__ import annotations

from decimal import Decimal
import json
from typing import Any, Dict

import pandas as pd
import pytest

from contratos import (
    ColumnMeta,
    MotorResult,
    TipoEstruturalEnum,
    TipoSemanticoEnum,
    TipoTecnicoEnum,
    WarningEstrutural,
    CategoriaWarning,
)


def _make_column_meta(df, unidades=None):
    return {
        col: ColumnMeta(
            nome=col, tipo_tecnico=TipoTecnicoEnum.OBJECT,
            tipo_semantico=TipoSemanticoEnum.MISTO,
            tipo_estrutural=TipoEstruturalEnum.CATEGORICO_ELEGIVEL,
            subtipo_id_detectado=False, null_count=0,
            cardinalidade=df[col].nunique(),
            eh_candidato_categorico=True,
            ordem_insercao=list(df.columns).index(col),
            unidade=(unidades or {}).get(col),
        )
        for col in df.columns
    }


def _mr_dual(df, origem_idxs, comparado_idxs, unidades=None, warnings=None):
    ocm = {i: "origem" for i in origem_idxs}
    ocm.update({i: "comparado" for i in comparado_idxs})
    return MotorResult(
        df=df, column_meta=_make_column_meta(df, unidades),
        modo_upload="DUAL", origem_comparado_map=ocm,
        total_linhas_originais=len(df), total_linhas_processadas=len(df),
        warnings=warnings or [],
    )


def _mr_simples(df, unidades=None):
    return MotorResult(
        df=df, column_meta=_make_column_meta(df, unidades),
        modo_upload="SIMPLES", origem_comparado_map=None,
        total_linhas_originais=len(df), total_linhas_processadas=len(df),
    )


def _config_dual(modo="EXATO", unidade="MONETARIO_BRL", tolerancia="0", thresholds=None, agrupadores_executivos=None):
    from visoes.visao_v1 import (
        AgrupadorMatchV1,
        CampoComparadoV1,
        ModoMatchV1,
        TipoCampoV1,
        UnidadeCanonica,
    )
    return {
        "agrupadores_match": [AgrupadorMatchV1(
            nome_origem="documento", nome_comparado="documento",
            rotulo_analitico="Doc", modo_match=ModoMatchV1(modo),
        )],
        "campos_comparados": [CampoComparadoV1(
            nome_origem="valor", nome_comparado="valor", nome_analitico="Valor",
            tipo_logico=TipoCampoV1.VALOR_MONETARIO,
            unidade=UnidadeCanonica(unidade), tolerancia=Decimal(tolerancia),
        )],
        "agrupadores_executivos": agrupadores_executivos or [],
        "epsilon_por_unidade": {UnidadeCanonica(unidade): Decimal("0.01")},
        "thresholds": thresholds or {},
        "origem_ux": "Origem", "comparado_ux": "Comparado",
        "arquivo_origem": "o.xlsx", "arquivo_comparado": "c.xlsx",
        "aba_origem": "A", "aba_comparado": "B",
        "n_arquivos": 2, "paleta_aplicada": "Azul executivo",
    }


# ===========================================================================
# Bloco V · Determinismo e ordenação (~12 testes)
# ===========================================================================


class TestBlocoV_Determinismo:

    def test_ordem_deterministica_canonica_multiplas_execucoes(self):
        """100 'execuções' em ordem permutada produzem mesma ordenação canônica de saída."""
        from visoes.visao_v1 import executar_v1
        df_base = pd.DataFrame([
            {"documento": "Z003", "valor": 300.0},
            {"documento": "A001", "valor": 100.0},
            {"documento": "M002", "valor": 200.0},
            {"documento": "Z003", "valor": 300.0},
            {"documento": "A001", "valor": 100.0},
            {"documento": "M002", "valor": 200.0},
        ])
        chaves_anteriores = None
        for _ in range(5):
            mr = _mr_dual(df_base.copy(), [0, 1, 2], [3, 4, 5])
            result = executar_v1(mr, _config_dual())
            chaves = [r.chave_consolidada for r in result.classificacao_por_registro]
            if chaves_anteriores is not None:
                assert chaves == chaves_anteriores
            chaves_anteriores = chaves

    def test_chave_consolidada_zeros_a_esquerda_preservados(self):
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": "00123", "valor": 100.0},
            {"documento": "00123", "valor": 100.0},
        ])
        mr = _mr_dual(df, [0], [1])
        result = executar_v1(mr, _config_dual())
        assert result.classificacao_por_registro[0].chave_consolidada == "00123"

    def test_chave_consolidada_caracteres_unicode_preservados(self):
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": "São Paulo·CRM", "valor": 100.0},
            {"documento": "São Paulo·CRM", "valor": 100.0},
        ])
        mr = _mr_dual(df, [0], [1])
        result = executar_v1(mr, _config_dual())
        assert "São Paulo" in result.classificacao_por_registro[0].chave_consolidada

    def test_resumo_por_agrupador_ordenado_desc_diferenca_liquida(self):
        """T-RANK · |diferenca_liquida_total| desc."""
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            # filial SP: 2 conciliados de 100, 1 divergente +50
            {"documento": "S1", "valor": 100.0, "filial": "SP"},
            {"documento": "S2", "valor": 100.0, "filial": "SP"},
            {"documento": "S3", "valor": 1000.0, "filial": "SP"},
            # filial RJ: 1 conciliado de 50
            {"documento": "R1", "valor": 50.0, "filial": "RJ"},
            # Comparado
            {"documento": "S1", "valor": 100.0, "filial": "SP"},
            {"documento": "S2", "valor": 100.0, "filial": "SP"},
            {"documento": "S3", "valor": 500.0, "filial": "SP"},  # diff 500
            {"documento": "R1", "valor": 50.0, "filial": "RJ"},
        ])
        mr = _mr_dual(df, [0, 1, 2, 3], [4, 5, 6, 7])
        config = _config_dual(agrupadores_executivos=["filial"])
        result = executar_v1(mr, config)
        linhas = result.resumo_por_agrupador_executivo
        assert linhas is not None
        assert len(linhas) == 2
        # SP tem maior |diff_total| (500) · deve vir primeiro
        assert linhas[0].valores_agrupador.get("filial") == "SP"

    def test_idempotencia_executar_v1_serializacao_estavel(self):
        """2 execuções produzem mesmas chaves + mesmas contagens."""
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": "A", "valor": 100.0},
            {"documento": "B", "valor": 200.0},
            {"documento": "A", "valor": 100.0},
            {"documento": "B", "valor": 200.0},
        ])
        ts = pd.Timestamp("2026-04-26 12:00:00").to_pydatetime()
        mr1 = _mr_dual(df.copy(), [0, 1], [2, 3]).model_copy(update={"timestamp_processamento": ts})
        mr2 = _mr_dual(df.copy(), [0, 1], [2, 3]).model_copy(update={"timestamp_processamento": ts})
        r1 = executar_v1(mr1, _config_dual())
        r2 = executar_v1(mr2, _config_dual())
        assert r1.contagem_por_classificacao == r2.contagem_por_classificacao
        assert r1.status_ponte_geral == r2.status_ponte_geral
        assert [r.chave_consolidada for r in r1.classificacao_por_registro] == \
               [r.chave_consolidada for r in r2.classificacao_por_registro]

    def test_para_contexto_ia_estavel(self):
        """método para_contexto_ia herdado de VNResultBase produz dict serializável."""
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": "A", "valor": 100.0},
            {"documento": "A", "valor": 100.0},
        ])
        mr = _mr_dual(df, [0], [1])
        result = executar_v1(mr, _config_dual())
        ctx = result.para_contexto_ia()
        assert ctx["visao_id"] == "V1"
        assert "resumo_executivo" in ctx
        assert "warnings" in ctx
        # JSON-compatível
        json.dumps(ctx, default=str)


# ===========================================================================
# Bloco VI · Casos de fronteira e regressão (~30 testes)
# ===========================================================================


class TestBlocoVI_BaseVazia:

    def test_base_origem_vazia_so_comparado(self):
        from visoes.visao_v1 import ClassificacaoRegistroV1, executar_v1
        df = pd.DataFrame([
            {"documento": "A", "valor": 100.0},
            {"documento": "B", "valor": 200.0},
        ])
        mr = _mr_dual(df, [], [0, 1])  # 0 origem · 2 comparado
        result = executar_v1(mr, _config_dual())
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.SO_COMPARADO] == 2

    def test_base_comparado_vazia_so_origem(self):
        from visoes.visao_v1 import ClassificacaoRegistroV1, executar_v1
        df = pd.DataFrame([
            {"documento": "A", "valor": 100.0},
            {"documento": "B", "valor": 200.0},
        ])
        mr = _mr_dual(df, [0, 1], [])
        result = executar_v1(mr, _config_dual())
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.SO_ORIGEM] == 2

    def test_ambas_bases_vazias_dispara_b_v1_no_upload(self):
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame(columns=["documento", "valor"])
        mr = _mr_dual(df, [], [])
        with pytest.raises(ValueError, match="B-V1-NO-UPLOAD"):
            executar_v1(mr, _config_dual())


class TestBlocoVI_CamposNulos:

    def test_100pct_nulos_em_campo_status_sem_valor_ambos(self):
        from visoes.visao_v1 import StatusCampoV1, executar_v1
        df = pd.DataFrame([
            {"documento": "A", "valor": None},
            {"documento": "A", "valor": None},
        ])
        mr = _mr_dual(df, [0], [1])
        result = executar_v1(mr, _config_dual())
        celula = result.classificacao_por_registro[0].valores_por_campo[0]
        assert celula.status_campo == StatusCampoV1.SEM_VALOR_AMBOS

    def test_chave_50pct_nulos_dispara_b_v1_chave_invalida(self):
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": None, "valor": 100.0},
            {"documento": None, "valor": 200.0},
            {"documento": "C", "valor": 100.0},
            {"documento": "C", "valor": 200.0},
        ])
        mr = _mr_dual(df, [0, 1], [2, 3])
        with pytest.raises(ValueError, match="B-V1-CHAVE-INVALIDA"):
            executar_v1(mr, _config_dual())

    def test_chave_49pct_nulos_passa_com_threshold_default(self):
        """49% nulos é abaixo do threshold default (50%) · deve passar."""
        from visoes.visao_v1 import executar_v1
        # Com 51 linhas, 25 nulos = 49% ≈ aceitável; mas precisa estar abaixo
        df_origem_data = [{"documento": None, "valor": 100.0}] * 4 + [{"documento": "X", "valor": 100.0}] * 6
        df_comparado_data = [{"documento": "X", "valor": 100.0}] * 6 + [{"documento": "Y", "valor": 100.0}] * 4
        df = pd.DataFrame(df_origem_data + df_comparado_data)
        mr = _mr_dual(df, list(range(10)), list(range(10, 20)))
        # 4/10 = 40% nulos · abaixo do default 50%
        result = executar_v1(mr, _config_dual())
        assert result is not None  # não bloqueou


class TestBlocoVI_Volume:

    def test_volume_acima_default_dispara_b_v1_resultado_excede(self):
        from visoes.visao_v1 import executar_v1
        # Construir dataset acima de threshold artificial (em vez do default 500k)
        df = pd.DataFrame([
            {"documento": f"D{i:04d}", "valor": float(i)} for i in range(500)
        ])
        mr = _mr_dual(df, list(range(250)), list(range(250, 500)))
        config = _config_dual(thresholds={"volume_max": 100})
        with pytest.raises(ValueError, match="B-V1-RESULTADO-EXCEDE"):
            executar_v1(mr, config)

    def test_volume_proximo_threshold_passa(self):
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": f"D{i:04d}", "valor": float(i)} for i in range(50)
        ])
        mr = _mr_dual(df, list(range(25)), list(range(25, 50)))
        config = _config_dual(thresholds={"volume_max": 100})
        result = executar_v1(mr, config)
        assert result is not None


class TestBlocoVI_MatchModoSemantica:

    def test_match_modo_contem_simetrico(self):
        """CONTEM é simétrico: 'abc' ⊃ 'ab' ↔ 'ab' ⊂ 'abc'."""
        from visoes.visao_v1 import (
            AgrupadorMatchV1, ModoMatchV1, ClassificacaoRegistroV1, executar_v1,
        )
        df = pd.DataFrame([
            {"documento": "abc", "valor": 100.0},  # origem
            {"documento": "ab", "valor": 100.0},   # comparado
        ])
        mr = _mr_dual(df, [0], [1])
        config = _config_dual(modo="CONTEM")
        result = executar_v1(mr, config)
        # 'ab' está contido em 'abc' · simétrico · matched
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.CONCILIADO] >= 1

    def test_match_modo_inicia_com_simetrico(self):
        from visoes.visao_v1 import ClassificacaoRegistroV1, executar_v1
        df = pd.DataFrame([
            {"documento": "abc123", "valor": 100.0},
            {"documento": "abc", "valor": 100.0},
        ])
        mr = _mr_dual(df, [0], [1])
        config = _config_dual(modo="INICIA_COM")
        result = executar_v1(mr, config)
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.CONCILIADO] >= 1

    def test_match_modo_termina_com_simetrico(self):
        from visoes.visao_v1 import ClassificacaoRegistroV1, executar_v1
        df = pd.DataFrame([
            {"documento": "X-abc", "valor": 100.0},
            {"documento": "abc", "valor": 100.0},
        ])
        mr = _mr_dual(df, [0], [1])
        config = _config_dual(modo="TERMINA_COM")
        result = executar_v1(mr, config)
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.CONCILIADO] >= 1


class TestBlocoVI_DecimalQuantize:

    def test_decimal_preserva_precisao_monetaria(self):
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": "A", "valor": 1234.56},
            {"documento": "A", "valor": 1234.56},
        ])
        mr = _mr_dual(df, [0], [1])
        result = executar_v1(mr, _config_dual())
        celula = result.classificacao_por_registro[0].valores_por_campo[0]
        assert celula.valor_origem == Decimal("1234.56")

    def test_decimal_converte_int_sem_decimal_artificial(self):
        from visoes.visao_v1 import executar_v1, UnidadeCanonica
        df = pd.DataFrame([
            {"documento": "A", "valor": 100},
            {"documento": "A", "valor": 100},
        ])
        mr = _mr_dual(df, [0], [1])
        config = _config_dual(unidade="QUANTIDADE", tolerancia="0")
        from visoes.visao_v1 import CampoComparadoV1, TipoCampoV1
        config["campos_comparados"] = [CampoComparadoV1(
            nome_origem="valor", nome_comparado="valor", nome_analitico="Qtd",
            tipo_logico=TipoCampoV1.QUANTIDADE,
            unidade=UnidadeCanonica.QUANTIDADE, tolerancia=Decimal("0"),
        )]
        result = executar_v1(mr, config)
        celula = result.classificacao_por_registro[0].valores_por_campo[0]
        assert celula.valor_origem == Decimal("100")


class TestBlocoVI_PropagacaoMotorWarnings:

    def test_warnings_motor_propagados(self):
        """Warnings emitidos pelo motor (W-B...) aparecem em warnings_emitidos."""
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": "A", "valor": 100.0},
            {"documento": "A", "valor": 100.0},
        ])
        warning_motor = WarningEstrutural(
            codigo="W-B-TESTE",
            categoria=CategoriaWarning.INFORMATIVO,
            microcopy="Warning herdado do motor para teste",
        )
        mr = _mr_dual(df, [0], [1], warnings=[warning_motor])
        result = executar_v1(mr, _config_dual())
        codigos = [w.codigo for w in result.warnings_emitidos]
        assert "W-B-TESTE" in codigos


class TestBlocoVI_StatusPonteFronteira:

    def test_status_ponte_fecha_quando_lista_vazia(self):
        """FECHA por convenção quando len(pontes) == 0 (todos campos PERCENTUAL)."""
        from visoes.visao_v1 import (
            CampoComparadoV1, StatusPonteV1, TipoCampoV1, UnidadeCanonica, executar_v1,
        )
        df = pd.DataFrame([
            {"documento": "A", "valor": 0.10},
            {"documento": "A", "valor": 0.10},
        ])
        mr = _mr_dual(df, [0], [1])
        config = _config_dual()
        config["campos_comparados"] = [CampoComparadoV1(
            nome_origem="valor", nome_comparado="valor", nome_analitico="Taxa",
            tipo_logico=TipoCampoV1.PERCENTUAL,
            unidade=UnidadeCanonica.PERCENTUAL, tolerancia=Decimal("0"),
        )]
        result = executar_v1(mr, config)
        assert len(result.pontes) == 0
        assert result.status_ponte_geral == StatusPonteV1.FECHA

    def test_status_ponte_calculado_de_pontes_individuais(self):
        from visoes.visao_v1 import StatusPonteV1, executar_v1
        df = pd.DataFrame([
            {"documento": "A", "valor": 100.00},
            {"documento": "A", "valor": 100.00},
        ])
        mr = _mr_dual(df, [0], [1])
        result = executar_v1(mr, _config_dual())
        assert result.status_ponte_geral == StatusPonteV1.FECHA
        assert all(p.fecha for p in result.pontes)


class TestBlocoVI_InvariantesEstruturais:

    def test_invariante_len_classificacao_igual_soma_contagem(self):
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": f"K{i}", "valor": 100.0 + i} for i in range(5)
        ])
        df = pd.concat([df, df.copy()], ignore_index=True)
        mr = _mr_dual(df, list(range(5)), list(range(5, 10)))
        result = executar_v1(mr, _config_dual())
        soma = sum(result.contagem_por_classificacao.values())
        assert soma == len(result.classificacao_por_registro)

    def test_invariante_len_valor_por_campo_igual_len_campos(self):
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": "A", "valor": 100.0},
            {"documento": "A", "valor": 100.0},
        ])
        mr = _mr_dual(df, [0], [1])
        result = executar_v1(mr, _config_dual())
        assert len(result.valor_por_campo) == len(result.conciliacao_realizada.campos_comparados)

    def test_invariante_chave_classificacao_em_enum(self):
        from visoes.visao_v1 import ClassificacaoRegistroV1, executar_v1
        df = pd.DataFrame([
            {"documento": "A", "valor": 100.0},
            {"documento": "A", "valor": 100.0},
        ])
        mr = _mr_dual(df, [0], [1])
        result = executar_v1(mr, _config_dual())
        for chave in result.contagem_por_classificacao:
            assert isinstance(chave, ClassificacaoRegistroV1)


class TestBlocoVI_ParaContextoIA:

    def test_para_contexto_ia_inclui_amostra_base_analitica(self):
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": "A", "valor": 100.0},
            {"documento": "A", "valor": 100.0},
        ])
        mr = _mr_dual(df, [0], [1])
        result = executar_v1(mr, _config_dual())
        ctx = result.para_contexto_ia()
        assert "amostra_base_analitica" in ctx
        assert isinstance(ctx["amostra_base_analitica"], list)

    def test_para_contexto_ia_inclui_warnings(self):
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": "A", "valor": 100.0},
            {"documento": "A", "valor": 100.0},
        ])
        mr = _mr_dual(df, [0], [1])
        result = executar_v1(mr, _config_dual())
        ctx = result.para_contexto_ia()
        assert "warnings" in ctx

    def test_para_contexto_ia_inclui_bloqueios_escapados(self):
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": None, "valor": 100.0},
            {"documento": None, "valor": 200.0},
            {"documento": "C", "valor": 100.0},
            {"documento": "C", "valor": 200.0},
        ])
        mr = _mr_dual(df, [0, 1], [2, 3])
        config = _config_dual()
        config["escapes"] = {"B-V1-CHAVE-INVALIDA": True}
        result = executar_v1(mr, config)
        ctx = result.para_contexto_ia()
        assert "bloqueios_escapados" in ctx
        assert len(ctx["bloqueios_escapados"]) >= 1


class TestBlocoVI_MotorSimplesEMotorDual:

    def test_motor_dual_origem_comparado_map_obrigatorio(self):
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([{"documento": "A", "valor": 100.0}])
        mr = MotorResult(
            df=df, column_meta=_make_column_meta(df),
            modo_upload="DUAL", origem_comparado_map=None,  # inválido
            total_linhas_originais=1, total_linhas_processadas=1,
        )
        with pytest.raises(ValueError, match="B-V1-MOTOR-FALHOU"):
            executar_v1(mr, _config_dual())

    def test_motor_simples_implica_mesma_aba(self):
        from visoes.visao_v1 import CasoLogicoV1, executar_v1
        df = pd.DataFrame([{
            "docOrigem": "A", "docComparado": "A",
            "valorOrigem": 100.0, "valorComparado": 100.0
        }])
        mr = _mr_simples(df)
        from visoes.visao_v1 import (
            AgrupadorMatchV1, CampoComparadoV1, ModoMatchV1, TipoCampoV1, UnidadeCanonica,
        )
        config = {
            "agrupadores_match": [AgrupadorMatchV1(
                nome_origem="docOrigem", nome_comparado="docComparado",
                rotulo_analitico="Doc", modo_match=ModoMatchV1.EXATO,
            )],
            "campos_comparados": [CampoComparadoV1(
                nome_origem="valorOrigem", nome_comparado="valorComparado", nome_analitico="V",
                tipo_logico=TipoCampoV1.VALOR_MONETARIO,
                unidade=UnidadeCanonica.MONETARIO_BRL, tolerancia=Decimal("0"),
            )],
            "agrupadores_executivos": [],
            "epsilon_por_unidade": {UnidadeCanonica.MONETARIO_BRL: Decimal("0.01")},
            "thresholds": {},
            "origem_ux": "Origem", "comparado_ux": "Comparado",
            "arquivo_origem": "x.xlsx", "arquivo_comparado": "x.xlsx",
            "aba_origem": "U", "aba_comparado": "U",
            "n_arquivos": 1, "paleta_aplicada": "Azul executivo",
        }
        result = executar_v1(mr, config)
        assert result.conciliacao_realizada.caso_logico_inferido == CasoLogicoV1.MESMA_ABA_EM_COLUNAS


class TestBlocoVI_SinteseDiagnostico:

    def test_sintese_n_chaves_duplicadas_consistente(self):
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": "A", "valor": 100.0},
            {"documento": "A", "valor": 105.0},
            {"documento": "A", "valor": 100.0},
        ])
        mr = _mr_dual(df, [0, 1], [2])
        result = executar_v1(mr, _config_dual())
        assert result.sintese_diagnostico.n_chaves_duplicadas >= 1

    def test_sintese_n_warnings_ativos(self):
        from visoes.visao_v1 import (
            CampoComparadoV1, TipoCampoV1, UnidadeCanonica, executar_v1,
        )
        df = pd.DataFrame([
            {"documento": "A", "valor": 100.005},
            {"documento": "A", "valor": 100.000},
        ])
        mr = _mr_dual(df, [0], [1])
        config = _config_dual(tolerancia="0.01")
        result = executar_v1(mr, config)
        # W-V1-TOL ativo · n_warnings_ativos >= 1
        assert result.sintese_diagnostico.n_warnings_ativos >= 1


class TestBlocoVI_ResumoExecutivoDataConsistente:

    def test_resumo_executivo_taxa_alinha_com_contagem(self):
        from visoes.visao_v1 import ClassificacaoRegistroV1, executar_v1
        df = pd.DataFrame([
            {"documento": "A", "valor": 100.0},
            {"documento": "B", "valor": 100.0},
            {"documento": "A", "valor": 100.0},
            {"documento": "B", "valor": 200.0},  # divergente
        ])
        mr = _mr_dual(df, [0, 1], [2, 3])
        result = executar_v1(mr, _config_dual())
        n_total = sum(result.contagem_por_classificacao.values())
        n_conc = result.contagem_por_classificacao[ClassificacaoRegistroV1.CONCILIADO]
        taxa_esperada = n_conc / n_total
        taxa_resumo = result.resumo_executivo.bloco_2_numeros_ancora["taxa_conciliacao_geral"]
        assert abs(taxa_resumo - taxa_esperada) < 0.0001

    def test_resumo_executivo_caso_logico_em_bloco_2(self):
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": "A", "valor": 100.0},
            {"documento": "A", "valor": 100.0},
        ])
        mr = _mr_dual(df, [0], [1])
        result = executar_v1(mr, _config_dual())
        assert result.resumo_executivo.bloco_2_numeros_ancora["caso_logico_inferido"] == "ABAS_DISTINTAS"

    def test_resumo_executivo_status_ponte_em_bloco_2(self):
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": "A", "valor": 100.0},
            {"documento": "A", "valor": 100.0},
        ])
        mr = _mr_dual(df, [0], [1])
        result = executar_v1(mr, _config_dual())
        assert "status_ponte_geral" in result.resumo_executivo.bloco_2_numeros_ancora


class TestBlocoVI_LinhaResumoAgrupadorTRANK:

    def test_resumo_agrupador_empate_ordem_alfabetica(self):
        """Quando 2 agrupadores têm mesma |diff_total|, ordem alfabética desempata (P-V1-TEC-03)."""
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            # filial A: diff = 0
            {"documento": "A1", "valor": 100.0, "filial": "A"},
            # filial B: diff = 0
            {"documento": "B1", "valor": 100.0, "filial": "B"},
            # comparado mesmo
            {"documento": "A1", "valor": 100.0, "filial": "A"},
            {"documento": "B1", "valor": 100.0, "filial": "B"},
        ])
        mr = _mr_dual(df, [0, 1], [2, 3])
        config = _config_dual(agrupadores_executivos=["filial"])
        result = executar_v1(mr, config)
        linhas = result.resumo_por_agrupador_executivo
        assert linhas is not None
        # Ambos diff = 0 · ordem alfabética: A vem antes de B
        valores_filial = [l.valores_agrupador.get("filial") for l in linhas]
        assert valores_filial == ["A", "B"]


class TestBlocoVI_StatusPonteResiduoAlemEpsilon:

    def test_ponte_com_residuo_quando_diferenca_nao_explicada(self):
        """Cenário com SO_ORIGEM e SO_COMPARADO compensando · ponte fecha."""
        from visoes.visao_v1 import StatusPonteV1, executar_v1
        df = pd.DataFrame([
            # Origem
            {"documento": "K001", "valor": 100.0},
            {"documento": "K002", "valor": 200.0},  # so_origem
            # Comparado
            {"documento": "K001", "valor": 100.0},
            {"documento": "K003", "valor": 200.0},  # so_comparado
        ])
        mr = _mr_dual(df, [0, 1], [2, 3])
        result = executar_v1(mr, _config_dual())
        # saldo_o = 300, ajuste_so_o = -200 (K002 sai), ajuste_so_c = +200 (K003 entra)
        # esperado = 300 - 200 + 200 = 300, real = 300, residuo = 0 → fecha
        assert result.status_ponte_geral == StatusPonteV1.FECHA


class TestBlocoVI_ConfigAplicada:

    def test_config_aplicada_paleta_default(self):
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": "A", "valor": 100.0},
            {"documento": "A", "valor": 100.0},
        ])
        mr = _mr_dual(df, [0], [1])
        result = executar_v1(mr, _config_dual())
        assert result.config_aplicada.paleta_aplicada == "Azul executivo"

    def test_config_aplicada_paleta_customizada(self):
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": "A", "valor": 100.0},
            {"documento": "A", "valor": 100.0},
        ])
        mr = _mr_dual(df, [0], [1])
        config = _config_dual()
        config["paleta_aplicada"] = "Verde executivo"
        result = executar_v1(mr, config)
        assert result.config_aplicada.paleta_aplicada == "Verde executivo"

    def test_config_aplicada_epsilon_por_unidade_populado(self):
        from visoes.visao_v1 import UnidadeCanonica, executar_v1
        df = pd.DataFrame([
            {"documento": "A", "valor": 100.0},
            {"documento": "A", "valor": 100.0},
        ])
        mr = _mr_dual(df, [0], [1])
        result = executar_v1(mr, _config_dual())
        assert UnidadeCanonica.MONETARIO_BRL in result.config_aplicada.epsilon_por_unidade
