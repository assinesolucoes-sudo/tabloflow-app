"""
test_visao_v1_mesma_aba.py — Smoke tests do ramo MESMA_ABA_EM_COLUNAS (Fase 3 · V-V1)

Cobre cenários canônicos da S-V1 v2 §2.1 ramo 4-B (D-213 caso 3):
- Pareamento linha-a-linha por construção
- Cobertura None (invariante)
- SO_ORIGEM/SO_COMPARADO zerados (invariante)
- Ajustes de Ponte ajuste_so_*=0 (invariante)
- W-V1-DUP/AMB sempre 0 com microcopy "não aplicável"
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


def _fake_motor_result_simples(df: pd.DataFrame) -> MotorResult:
    """Cria MotorResult artificial · modo SIMPLES · 1 aba única."""
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
    return MotorResult(
        df=df,
        column_meta=column_meta,
        modo_upload="SIMPLES",
        origem_comparado_map=None,
        total_linhas_originais=len(df),
        total_linhas_processadas=len(df),
    )


def _config_mesma_aba(unidade="MONETARIO_BRL"):
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
                nome_origem="docOrigem",
                nome_comparado="docComparado",
                rotulo_analitico="Documento",
                modo_match=ModoMatchV1.EXATO,
            )
        ],
        "campos_comparados": [
            CampoComparadoV1(
                nome_origem="valorOrigem",
                nome_comparado="valorComparado",
                nome_analitico="Valor",
                tipo_logico=TipoCampoV1.VALOR_MONETARIO,
                unidade=UnidadeCanonica(unidade),
                tolerancia=Decimal("0"),
            )
        ],
        "agrupadores_executivos": [],
        "epsilon_por_unidade": {UnidadeCanonica.MONETARIO_BRL: Decimal("0.01")},
        "thresholds": {},
        "origem_ux": "Origem",
        "comparado_ux": "Comparado",
        "arquivo_origem": "dados.xlsx",
        "arquivo_comparado": "dados.xlsx",
        "aba_origem": "UnicaAba",
        "aba_comparado": "UnicaAba",
        "n_arquivos": 1,
        "paleta_aplicada": "Azul executivo",
    }


class TestMesmaAbaCenariosBase:

    def test_executar_v1_mesma_aba_todos_conciliados(self):
        """3 linhas · valorOrigem == valorComparado em todas · esperado 3 CONCILIADO."""
        from visoes.visao_v1 import (
            CasoLogicoV1,
            ClassificacaoRegistroV1,
            executar_v1,
        )
        df = pd.DataFrame([
            {"docOrigem": "D001", "docComparado": "D001", "valorOrigem": 100.00, "valorComparado": 100.00},
            {"docOrigem": "D002", "docComparado": "D002", "valorOrigem": 200.00, "valorComparado": 200.00},
            {"docOrigem": "D003", "docComparado": "D003", "valorOrigem": 300.00, "valorComparado": 300.00},
        ])
        mr = _fake_motor_result_simples(df)
        result = executar_v1(mr, _config_mesma_aba())

        assert result.conciliacao_realizada.caso_logico_inferido == CasoLogicoV1.MESMA_ABA_EM_COLUNAS
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.CONCILIADO] == 3
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.DIVERGENTE_VALOR] == 0

    def test_executar_v1_mesma_aba_alguns_divergentes(self):
        """3 linhas · 2 iguais · 1 divergente · esperado 2 CONCILIADO + 1 DIVERGENTE_VALOR."""
        from visoes.visao_v1 import ClassificacaoRegistroV1, executar_v1
        df = pd.DataFrame([
            {"docOrigem": "D001", "docComparado": "D001", "valorOrigem": 100.00, "valorComparado": 100.00},
            {"docOrigem": "D002", "docComparado": "D002", "valorOrigem": 200.00, "valorComparado": 200.00},
            {"docOrigem": "D003", "docComparado": "D003", "valorOrigem": 300.00, "valorComparado": 350.00},
        ])
        mr = _fake_motor_result_simples(df)
        result = executar_v1(mr, _config_mesma_aba())

        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.CONCILIADO] == 2
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.DIVERGENTE_VALOR] == 1


class TestMesmaAbaInvariantes:

    def test_executar_v1_mesma_aba_cobertura_none(self):
        """Invariante S-V1 §1.1: cobertura == None em MESMA_ABA_EM_COLUNAS."""
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"docOrigem": "D001", "docComparado": "D001", "valorOrigem": 100.00, "valorComparado": 100.00},
        ])
        mr = _fake_motor_result_simples(df)
        result = executar_v1(mr, _config_mesma_aba())
        assert result.cobertura is None

    def test_executar_v1_mesma_aba_4_classes_zeradas(self):
        """Invariante: SO_ORIGEM, SO_COMPARADO, DIVERGENCIA_DUPLICIDADE, DIVERGENCIA_AMBIGUIDADE = 0."""
        from visoes.visao_v1 import ClassificacaoRegistroV1, executar_v1
        df = pd.DataFrame([
            {"docOrigem": "D001", "docComparado": "D001", "valorOrigem": 100.00, "valorComparado": 100.00},
            {"docOrigem": "D002", "docComparado": "D002", "valorOrigem": 200.00, "valorComparado": 250.00},
        ])
        mr = _fake_motor_result_simples(df)
        result = executar_v1(mr, _config_mesma_aba())

        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.SO_ORIGEM] == 0
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.SO_COMPARADO] == 0
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.DIVERGENCIA_DUPLICIDADE] == 0
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.DIVERGENCIA_AMBIGUIDADE] == 0

    def test_executar_v1_mesma_aba_ponte_ajuste_so_zerado(self):
        """Invariante S-V1 §1.16: ajuste_so_origem == 0 e ajuste_so_comparado == 0 em MESMA_ABA."""
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"docOrigem": "D001", "docComparado": "D001", "valorOrigem": 100.00, "valorComparado": 100.00},
            {"docOrigem": "D002", "docComparado": "D002", "valorOrigem": 200.00, "valorComparado": 200.00},
        ])
        mr = _fake_motor_result_simples(df)
        result = executar_v1(mr, _config_mesma_aba())

        assert len(result.pontes) == 1
        ponte = result.pontes[0]
        assert ponte.ajuste_so_origem == Decimal("0")
        assert ponte.ajuste_so_comparado == Decimal("0")

    def test_executar_v1_mesma_aba_warnings_dup_amb_microcopy(self):
        """W-V1-DUP e W-V1-AMB sempre com 0 ocorrências e microcopy 'não aplicável'."""
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"docOrigem": "D001", "docComparado": "D001", "valorOrigem": 100.00, "valorComparado": 100.00},
        ])
        mr = _fake_motor_result_simples(df)
        result = executar_v1(mr, _config_mesma_aba())

        w_dup = next(w for w in result.warnings_emitidos if w.codigo == "W-V1-DUP")
        w_amb = next(w for w in result.warnings_emitidos if w.codigo == "W-V1-AMB")
        assert w_dup.n_ocorrencias == 0
        assert w_amb.n_ocorrencias == 0
        # Microcopy "não aplicável"
        assert any("não aplicável" in str(d) for d in w_dup.detalhes)
        assert any("não aplicável" in str(d) for d in w_amb.detalhes)

    def test_executar_v1_mesma_aba_n_processados_iguala_linhas(self):
        """n_processados == n° de linhas da aba (S-V1 §1.2)."""
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"docOrigem": f"D{i:03d}", "docComparado": f"D{i:03d}",
             "valorOrigem": 100.0 * i, "valorComparado": 100.0 * i}
            for i in range(1, 8)  # 7 linhas
        ])
        mr = _fake_motor_result_simples(df)
        result = executar_v1(mr, _config_mesma_aba())

        assert result.conciliacao_realizada.n_processados == 7
        assert result.conciliacao_realizada.n_registros_origem == 7
        assert result.conciliacao_realizada.n_registros_comparado == 7
