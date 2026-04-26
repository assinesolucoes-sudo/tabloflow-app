"""
test_visao_v1_resumo_executivo.py — Resumo Executivo + agregações (Fase 4 · V-V1)

Cobre o mapeamento contrato → 9 seções de S-V1 §2.10 e os contratos
LeituraQualitativaV1 · ConfigAplicadaV1 · CoracaoVisualRef.
"""
from __future__ import annotations

from decimal import Decimal

import pandas as pd

from contratos import (
    ColumnMeta,
    MotorResult,
    TipoEstruturalEnum,
    TipoSemanticoEnum,
    TipoTecnicoEnum,
)


def _mr_dual(df, origem_idxs, comparado_idxs):
    column_meta = {
        col: ColumnMeta(
            nome=col, tipo_tecnico=TipoTecnicoEnum.OBJECT,
            tipo_semantico=TipoSemanticoEnum.MISTO,
            tipo_estrutural=TipoEstruturalEnum.CATEGORICO_ELEGIVEL,
            subtipo_id_detectado=False, null_count=0,
            cardinalidade=df[col].nunique(),
            eh_candidato_categorico=True,
            ordem_insercao=list(df.columns).index(col),
        )
        for col in df.columns
    }
    ocm = {i: "origem" for i in origem_idxs}
    ocm.update({i: "comparado" for i in comparado_idxs})
    return MotorResult(
        df=df, column_meta=column_meta, modo_upload="DUAL", origem_comparado_map=ocm,
        total_linhas_originais=len(df), total_linhas_processadas=len(df),
    )


def _config(agrupadores_executivos=None, campos=None):
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
            rotulo_analitico="Documento", modo_match=ModoMatchV1.EXATO,
        )],
        "campos_comparados": campos or [CampoComparadoV1(
            nome_origem="valor", nome_comparado="valor", nome_analitico="Valor",
            tipo_logico=TipoCampoV1.VALOR_MONETARIO,
            unidade=UnidadeCanonica.MONETARIO_BRL, tolerancia=Decimal("0"),
        )],
        "agrupadores_executivos": agrupadores_executivos or [],
        "epsilon_por_unidade": {UnidadeCanonica.MONETARIO_BRL: Decimal("0.01")},
        "thresholds": {},
        "origem_ux": "Origem", "comparado_ux": "Comparado",
        "arquivo_origem": "o.xlsx", "arquivo_comparado": "c.xlsx",
        "aba_origem": "A", "aba_comparado": "B",
        "n_arquivos": 2, "paleta_aplicada": "Azul executivo",
    }


def _df_basico_3match():
    return pd.DataFrame([
        {"documento": "D001", "valor": 100.00, "filial": "SP"},
        {"documento": "D002", "valor": 200.00, "filial": "RJ"},
        {"documento": "D003", "valor": 300.00, "filial": "SP"},
        {"documento": "D001", "valor": 100.00, "filial": "SP"},
        {"documento": "D002", "valor": 200.00, "filial": "RJ"},
        {"documento": "D003", "valor": 300.00, "filial": "SP"},
    ])


class TestResumoExecutivo9Secoes:

    def test_resumo_executivo_secao_1_cabecalho_populado(self):
        from visoes.visao_v1 import executar_v1
        mr = _mr_dual(_df_basico_3match(), [0, 1, 2], [3, 4, 5])
        result = executar_v1(mr, _config())
        # §1 Cabeçalho: vem de conciliacao_realizada
        cr = result.conciliacao_realizada
        assert cr.arquivo_origem == "o.xlsx"
        assert cr.aba_origem == "A"
        assert cr.origem_ux == "Origem"

    def test_resumo_executivo_secao_2_tem_6_classes_em_abas_distintas(self):
        """§2 · contagem_por_classificacao tem 6 chaves em ABAS_DISTINTAS."""
        from visoes.visao_v1 import ClassificacaoRegistroV1, executar_v1
        mr = _mr_dual(_df_basico_3match(), [0, 1, 2], [3, 4, 5])
        result = executar_v1(mr, _config())
        assert len(result.contagem_por_classificacao) == 6
        for cls in ClassificacaoRegistroV1:
            assert cls in result.contagem_por_classificacao

    def test_resumo_executivo_secao_3_volumetria(self):
        """§3 · n_registros_origem, n_registros_comparado, n_processados."""
        from visoes.visao_v1 import executar_v1
        mr = _mr_dual(_df_basico_3match(), [0, 1, 2], [3, 4, 5])
        result = executar_v1(mr, _config())
        cr = result.conciliacao_realizada
        assert cr.n_registros_origem == 3
        assert cr.n_registros_comparado == 3
        assert cr.n_processados >= 3

    def test_resumo_executivo_secao_4_status_ponte(self):
        """§4 · status_ponte_geral declarado."""
        from visoes.visao_v1 import StatusPonteV1, executar_v1
        mr = _mr_dual(_df_basico_3match(), [0, 1, 2], [3, 4, 5])
        result = executar_v1(mr, _config())
        assert result.status_ponte_geral in (StatusPonteV1.FECHA, StatusPonteV1.COM_RESIDUO)
        assert len(result.pontes) == 1

    def test_resumo_executivo_secao_5_valor_por_campo(self):
        """§5 · 1 entrada por campo comparado."""
        from visoes.visao_v1 import executar_v1
        mr = _mr_dual(_df_basico_3match(), [0, 1, 2], [3, 4, 5])
        result = executar_v1(mr, _config())
        assert len(result.valor_por_campo) == 1
        assert result.valor_por_campo[0].nome_analitico == "Valor"
        assert result.valor_por_campo[0].soma_origem == Decimal("600")
        assert result.valor_por_campo[0].soma_comparado == Decimal("600")
        assert result.valor_por_campo[0].diferenca_liquida == Decimal("0")

    def test_resumo_executivo_secao_6_cobertura_em_abas_distintas(self):
        """§6 · cobertura populada em ABAS_DISTINTAS."""
        from visoes.visao_v1 import executar_v1
        mr = _mr_dual(_df_basico_3match(), [0, 1, 2], [3, 4, 5])
        result = executar_v1(mr, _config())
        assert result.cobertura is not None
        assert result.cobertura.n_origem_com_par == 3
        assert result.cobertura.cobertura_origem_pct == Decimal("1")

    def test_resumo_executivo_secao_7_resumo_por_agrupador_quando_configurado(self):
        """§7 · resumo_por_agrupador_executivo populado quando configurado."""
        from visoes.visao_v1 import executar_v1
        mr = _mr_dual(_df_basico_3match(), [0, 1, 2], [3, 4, 5])
        result = executar_v1(mr, _config(agrupadores_executivos=["filial"]))
        assert result.resumo_por_agrupador_executivo is not None
        assert len(result.resumo_por_agrupador_executivo) >= 1

    def test_resumo_executivo_secao_7_resumo_none_quando_nao_configurado(self):
        """§7 · None quando agrupadores_executivos vazio."""
        from visoes.visao_v1 import executar_v1
        mr = _mr_dual(_df_basico_3match(), [0, 1, 2], [3, 4, 5])
        result = executar_v1(mr, _config(agrupadores_executivos=[]))
        assert result.resumo_por_agrupador_executivo is None

    def test_resumo_executivo_secao_8_sintese_diagnostico(self):
        """§8 · 7 contadores síntese."""
        from visoes.visao_v1 import executar_v1
        mr = _mr_dual(_df_basico_3match(), [0, 1, 2], [3, 4, 5])
        result = executar_v1(mr, _config())
        s = result.sintese_diagnostico
        assert s.n_tolerancia_absorvida == 0
        assert s.n_chaves_duplicadas == 0
        assert s.n_chaves_ambiguas == 0
        assert s.n_warnings_ativos >= 0

    def test_resumo_executivo_secao_9_config_aplicada_microcopy_caso_logico(self):
        """§9 · config_aplicada inclui caso_logico_inferido para microcopy 'Caso lógico:...'."""
        from visoes.visao_v1 import CasoLogicoV1, executar_v1
        mr = _mr_dual(_df_basico_3match(), [0, 1, 2], [3, 4, 5])
        result = executar_v1(mr, _config())
        ca = result.config_aplicada
        assert ca.caso_logico_inferido == CasoLogicoV1.ABAS_DISTINTAS
        assert ca.paleta_aplicada == "Azul executivo"


class TestResumoExecutivoMesmaAba:

    def test_resumo_secao_2_mesma_aba_4_classes_zeradas(self):
        """§2 em MESMA_ABA: 2 classes ativas + 4 zeradas (D-213)."""
        from visoes.visao_v1 import (
            AgrupadorMatchV1,
            CampoComparadoV1,
            ClassificacaoRegistroV1,
            ModoMatchV1,
            TipoCampoV1,
            UnidadeCanonica,
            executar_v1,
        )
        df = pd.DataFrame([
            {"d_o": "D001", "d_c": "D001", "v_o": 100.0, "v_c": 100.0},
            {"d_o": "D002", "d_c": "D002", "v_o": 200.0, "v_c": 200.0},
        ])
        column_meta = {
            col: ColumnMeta(
                nome=col, tipo_tecnico=TipoTecnicoEnum.OBJECT,
                tipo_semantico=TipoSemanticoEnum.MISTO,
                tipo_estrutural=TipoEstruturalEnum.CATEGORICO_ELEGIVEL,
                subtipo_id_detectado=False, null_count=0,
                cardinalidade=df[col].nunique(),
                eh_candidato_categorico=True,
                ordem_insercao=list(df.columns).index(col),
            )
            for col in df.columns
        }
        mr = MotorResult(
            df=df, column_meta=column_meta, modo_upload="SIMPLES",
            origem_comparado_map=None,
            total_linhas_originais=2, total_linhas_processadas=2,
        )
        config = {
            "agrupadores_match": [AgrupadorMatchV1(
                nome_origem="d_o", nome_comparado="d_c",
                rotulo_analitico="Doc", modo_match=ModoMatchV1.EXATO,
            )],
            "campos_comparados": [CampoComparadoV1(
                nome_origem="v_o", nome_comparado="v_c", nome_analitico="Valor",
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

        assert len(result.contagem_por_classificacao) == 6  # 6 chaves preservadas
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.SO_ORIGEM] == 0
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.SO_COMPARADO] == 0
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.DIVERGENCIA_DUPLICIDADE] == 0
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.DIVERGENCIA_AMBIGUIDADE] == 0


class TestLeituraQualitativa:

    def test_leitura_qualitativa_estrutura_fixa(self):
        """LeituraQualitativaV1 tem 4 campos · texto não-vazio · faixa em {ALTA,MEDIA,BAIXA}."""
        from visoes.visao_v1 import executar_v1
        mr = _mr_dual(_df_basico_3match(), [0, 1, 2], [3, 4, 5])
        result = executar_v1(mr, _config())
        lq = result.leitura_qualitativa
        assert isinstance(lq.texto, str)
        assert len(lq.texto) > 0
        assert lq.faixa_taxa in ("ALTA", "MEDIA", "BAIXA")

    def test_leitura_qualitativa_zero_invencao_prosa_parametrizada(self):
        """O texto referencia o caso lógico inferido (não inventa)."""
        from visoes.visao_v1 import executar_v1
        mr = _mr_dual(_df_basico_3match(), [0, 1, 2], [3, 4, 5])
        result = executar_v1(mr, _config())
        # Em ABAS_DISTINTAS o texto deve mencionar isso
        assert "ABAS_DISTINTAS" in result.leitura_qualitativa.texto


class TestCoracaoVisual:

    def test_coracao_visual_nome_aba_mapa_conciliacao(self):
        """CoracaoVisualRef.nome_aba == 'Mapa de Conciliação' por convenção V1."""
        from visoes.visao_v1 import executar_v1
        mr = _mr_dual(_df_basico_3match(), [0, 1, 2], [3, 4, 5])
        result = executar_v1(mr, _config())
        assert result.coracao_visual.nome_aba == "Mapa de Conciliação"
