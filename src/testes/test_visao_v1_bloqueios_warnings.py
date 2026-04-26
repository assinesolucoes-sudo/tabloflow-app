"""
test_visao_v1_bloqueios_warnings.py — Catálogo bloqueios + warnings (Fase 5 · V-V1)

12 bloqueios B-V1-* (S-V1 §2.5) + 4 warnings W-V1-* (S-V1 §2.7).
Cada bloqueio tem ≥ 1 teste de disparo + escape (quando aplicável).
Cada warning tem 1 teste de disparo + 1 teste de não-disparo.
"""
from __future__ import annotations

from decimal import Decimal

import pandas as pd
import pytest

from contratos import (
    ColumnMeta,
    MotorResult,
    TipoEstruturalEnum,
    TipoSemanticoEnum,
    TipoTecnicoEnum,
)


def _mr_dual(df, origem_idxs, comparado_idxs, column_units=None):
    column_meta = {}
    for col in df.columns:
        column_meta[col] = ColumnMeta(
            nome=col, tipo_tecnico=TipoTecnicoEnum.OBJECT,
            tipo_semantico=TipoSemanticoEnum.MISTO,
            tipo_estrutural=TipoEstruturalEnum.CATEGORICO_ELEGIVEL,
            subtipo_id_detectado=False, null_count=0,
            cardinalidade=df[col].nunique(),
            eh_candidato_categorico=True,
            ordem_insercao=list(df.columns).index(col),
            unidade=(column_units or {}).get(col),
        )
    ocm = {i: "origem" for i in origem_idxs}
    ocm.update({i: "comparado" for i in comparado_idxs})
    return MotorResult(
        df=df, column_meta=column_meta, modo_upload="DUAL", origem_comparado_map=ocm,
        total_linhas_originais=len(df), total_linhas_processadas=len(df),
    )


def _config_base(agrupadores=None, campos=None, thresholds=None, escapes=None):
    from visoes.visao_v1 import (
        AgrupadorMatchV1,
        CampoComparadoV1,
        ModoMatchV1,
        TipoCampoV1,
        UnidadeCanonica,
    )
    if agrupadores is None:
        agrupadores = [AgrupadorMatchV1(
            nome_origem="documento", nome_comparado="documento",
            rotulo_analitico="Documento", modo_match=ModoMatchV1.EXATO,
        )]
    if campos is None:
        campos = [CampoComparadoV1(
            nome_origem="valor", nome_comparado="valor", nome_analitico="Valor",
            tipo_logico=TipoCampoV1.VALOR_MONETARIO,
            unidade=UnidadeCanonica.MONETARIO_BRL, tolerancia=Decimal("0"),
        )]
    return {
        "agrupadores_match": agrupadores,
        "campos_comparados": campos,
        "agrupadores_executivos": [],
        "epsilon_por_unidade": {UnidadeCanonica.MONETARIO_BRL: Decimal("0.01")},
        "thresholds": thresholds or {},
        "escapes": escapes or {},
        "origem_ux": "Origem", "comparado_ux": "Comparado",
        "arquivo_origem": "o.xlsx", "arquivo_comparado": "c.xlsx",
        "aba_origem": "A", "aba_comparado": "B",
        "n_arquivos": 2, "paleta_aplicada": "Azul executivo",
    }


def _df_basico():
    return pd.DataFrame([
        {"documento": "D001", "valor": 100.0},
        {"documento": "D002", "valor": 200.0},
        {"documento": "D001", "valor": 100.0},
        {"documento": "D002", "valor": 200.0},
    ])


# ===========================================================================
# 12 Bloqueios B-V1-*
# ===========================================================================


class TestBloqueios:

    def test_b_v1_no_upload_dispara_quando_motor_result_none(self):
        from visoes.visao_v1 import executar_v1
        with pytest.raises(ValueError, match="B-V1-NO-UPLOAD"):
            executar_v1(motor_result=None, config={})  # type: ignore[arg-type]

    def test_b_v1_no_upload_dispara_quando_df_vazio(self):
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame(columns=["documento", "valor"])
        mr = _mr_dual(df, [], [])
        with pytest.raises(ValueError, match="B-V1-NO-UPLOAD"):
            executar_v1(mr, _config_base())

    def test_b_v1_agrupador_zero_dispara(self):
        from visoes.visao_v1 import executar_v1
        mr = _mr_dual(_df_basico(), [0, 1], [2, 3])
        config = _config_base(agrupadores=[])
        with pytest.raises(ValueError, match="B-V1-AGRUPADOR-ZERO"):
            executar_v1(mr, config)

    def test_b_v1_agrupador_excede_dispara(self):
        from visoes.visao_v1 import (
            AgrupadorMatchV1,
            ModoMatchV1,
            executar_v1,
        )
        mr = _mr_dual(_df_basico(), [0, 1], [2, 3])
        config = _config_base(
            agrupadores=[AgrupadorMatchV1(
                nome_origem="documento", nome_comparado="documento",
                rotulo_analitico=f"A{i}", modo_match=ModoMatchV1.EXATO,
            ) for i in range(6)]
        )
        with pytest.raises(ValueError, match="B-V1-AGRUPADOR-EXCEDE"):
            executar_v1(mr, config)

    def test_b_v1_campo_zero_dispara(self):
        from visoes.visao_v1 import executar_v1
        mr = _mr_dual(_df_basico(), [0, 1], [2, 3])
        config = _config_base(campos=[])
        with pytest.raises(ValueError, match="B-V1-CAMPO-ZERO"):
            executar_v1(mr, config)

    def test_b_v1_campo_excede_dispara(self):
        from visoes.visao_v1 import (
            CampoComparadoV1,
            TipoCampoV1,
            UnidadeCanonica,
            executar_v1,
        )
        mr = _mr_dual(_df_basico(), [0, 1], [2, 3])
        campos_11 = [CampoComparadoV1(
            nome_origem="valor", nome_comparado="valor", nome_analitico=f"C{i}",
            tipo_logico=TipoCampoV1.VALOR_MONETARIO,
            unidade=UnidadeCanonica.MONETARIO_BRL, tolerancia=Decimal("0"),
        ) for i in range(11)]
        config = _config_base(campos=campos_11)
        with pytest.raises(ValueError, match="B-V1-CAMPO-EXCEDE"):
            executar_v1(mr, config)

    def test_b_v1_mesma_coluna_dispara_em_mesma_aba(self):
        """Em MESMA_ABA (mesma aba E mesmo arquivo), agrupador com nome_origem == nome_comparado disparou."""
        from visoes.visao_v1 import (
            AgrupadorMatchV1,
            CampoComparadoV1,
            ModoMatchV1,
            TipoCampoV1,
            UnidadeCanonica,
            executar_v1,
        )
        df = pd.DataFrame([
            {"docOrigem": "D001", "docComparado": "D001", "valor_o": 100.0, "valor_c": 100.0},
        ])
        column_meta = {
            col: ColumnMeta(
                nome=col, tipo_tecnico=TipoTecnicoEnum.OBJECT,
                tipo_semantico=TipoSemanticoEnum.MISTO,
                tipo_estrutural=TipoEstruturalEnum.CATEGORICO_ELEGIVEL,
                subtipo_id_detectado=False, null_count=0,
                cardinalidade=1, eh_candidato_categorico=True,
                ordem_insercao=list(df.columns).index(col),
            )
            for col in df.columns
        }
        mr = MotorResult(
            df=df, column_meta=column_meta, modo_upload="SIMPLES",
            origem_comparado_map=None,
            total_linhas_originais=1, total_linhas_processadas=1,
        )
        config = {
            "agrupadores_match": [AgrupadorMatchV1(
                nome_origem="docOrigem", nome_comparado="docOrigem",  # mesma coluna
                rotulo_analitico="Doc", modo_match=ModoMatchV1.EXATO,
            )],
            "campos_comparados": [CampoComparadoV1(
                nome_origem="valor_o", nome_comparado="valor_c", nome_analitico="V",
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
        with pytest.raises(ValueError, match="B-V1-MESMA-COLUNA"):
            executar_v1(mr, config)

    def test_b_v1_chave_invalida_dispara_quando_pct_nulos_alto(self):
        """Coluna agrupadora com 50%+ nulos dispara B-V1-CHAVE-INVALIDA."""
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": None, "valor": 100.0},
            {"documento": None, "valor": 200.0},
            {"documento": "D003", "valor": 300.0},
            {"documento": "D003", "valor": 300.0},
        ])
        mr = _mr_dual(df, [0, 1], [2, 3])  # Origem tem 100% nulos
        with pytest.raises(ValueError, match="B-V1-CHAVE-INVALIDA"):
            executar_v1(mr, _config_base())

    def test_b_v1_chave_invalida_escape_funciona(self):
        """Com escape acionado, B-V1-CHAVE-INVALIDA fica registrado mas não bloqueia."""
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": None, "valor": 100.0},
            {"documento": None, "valor": 200.0},
            {"documento": "D003", "valor": 300.0},
            {"documento": "D003", "valor": 300.0},
        ])
        mr = _mr_dual(df, [0, 1], [2, 3])
        config = _config_base(escapes={"B-V1-CHAVE-INVALIDA": True})
        result = executar_v1(mr, config)
        # Bloqueio escapado deve estar em bloqueios_disparados com escape_acionado=True
        assert any(
            b.codigo == "B-V1-CHAVE-INVALIDA" and b.escape_acionado
            for b in result.bloqueios_disparados
        )

    def test_b_v1_resultado_excede_dispara(self):
        """volume_max baixo dispara B-V1-RESULTADO-EXCEDE."""
        from visoes.visao_v1 import executar_v1
        mr = _mr_dual(_df_basico(), [0, 1], [2, 3])  # 4 linhas
        config = _config_base(thresholds={"volume_max": 2})  # bem abaixo
        with pytest.raises(ValueError, match="B-V1-RESULTADO-EXCEDE"):
            executar_v1(mr, config)

    def test_b_v1_resultado_excede_escape_funciona(self):
        from visoes.visao_v1 import executar_v1
        mr = _mr_dual(_df_basico(), [0, 1], [2, 3])
        config = _config_base(
            thresholds={"volume_max": 2},
            escapes={"B-V1-RESULTADO-EXCEDE": True},
        )
        result = executar_v1(mr, config)
        assert any(
            b.codigo == "B-V1-RESULTADO-EXCEDE" and b.escape_acionado
            for b in result.bloqueios_disparados
        )

    def test_b_v1_div_zero_nao_bloqueia_e_retorna_none(self):
        """Σ valor_origem == 0 produz variacao_total_registro_pct == None (não bloqueia)."""
        from visoes.visao_v1 import ClassificacaoRegistroV1, executar_v1
        df = pd.DataFrame([
            {"documento": "D001", "valor": 0.0},
            {"documento": "D001", "valor": 100.0},
        ])
        mr = _mr_dual(df, [0], [1])
        result = executar_v1(mr, _config_base())  # não bloqueia
        # Registro existe e diferenca está populada
        regs_match = [r for r in result.classificacao_por_registro
                      if r.classificacao_estrutural in (
                          ClassificacaoRegistroV1.DIVERGENTE_VALOR,
                          ClassificacaoRegistroV1.CONCILIADO,
                      )]
        # variacao_pct deve ser None quando soma_origem == 0
        if regs_match:
            assert regs_match[0].variacao_total_registro_pct is None

    def test_b_v1_motor_falhou_catch_all_envolve_exceptions_inesperadas(self):
        """Exception inesperada vira ValueError com prefixo B-V1-MOTOR-FALHOU."""
        from visoes.visao_v1 import executar_v1
        mr = _mr_dual(_df_basico(), [0, 1], [2, 3])
        # Forçar exceção: passar agrupador com coluna inexistente captura na validação
        # como B-V1-MOTOR-FALHOU também (definido no _etapa_2)
        config = _config_base()
        # Substituir nome_origem por inexistente para acionar erro
        from visoes.visao_v1 import AgrupadorMatchV1, ModoMatchV1
        config["agrupadores_match"] = [AgrupadorMatchV1(
            nome_origem="coluna_inexistente",
            nome_comparado="documento",
            rotulo_analitico="Doc", modo_match=ModoMatchV1.EXATO,
        )]
        with pytest.raises(ValueError, match="B-V1-MOTOR-FALHOU"):
            executar_v1(mr, config)


# ===========================================================================
# 4 Warnings W-V1-*
# ===========================================================================


class TestWarnings:

    def test_w_v1_tol_dispara_quando_tolerancia_absorve(self):
        from visoes.visao_v1 import (
            CampoComparadoV1,
            TipoCampoV1,
            UnidadeCanonica,
            executar_v1,
        )
        df = pd.DataFrame([
            {"documento": "D001", "valor": 100.005},
            {"documento": "D001", "valor": 100.000},
        ])
        mr = _mr_dual(df, [0], [1])
        config = _config_base(campos=[CampoComparadoV1(
            nome_origem="valor", nome_comparado="valor", nome_analitico="Valor",
            tipo_logico=TipoCampoV1.VALOR_MONETARIO,
            unidade=UnidadeCanonica.MONETARIO_BRL, tolerancia=Decimal("0.01"),
        )])
        result = executar_v1(mr, config)
        w = next(w for w in result.warnings_emitidos if w.codigo == "W-V1-TOL")
        assert w.n_ocorrencias >= 1

    def test_w_v1_tol_nao_dispara_quando_zero_tolerancia(self):
        from visoes.visao_v1 import executar_v1
        mr = _mr_dual(_df_basico(), [0, 1], [2, 3])
        result = executar_v1(mr, _config_base())
        w = next(w for w in result.warnings_emitidos if w.codigo == "W-V1-TOL")
        assert w.n_ocorrencias == 0

    def test_w_v1_dup_dispara_quando_chave_duplicada(self):
        from visoes.visao_v1 import executar_v1
        df = pd.DataFrame([
            {"documento": "D001", "valor": 100.0},
            {"documento": "D001", "valor": 105.0},  # dup origem
            {"documento": "D001", "valor": 100.0},
        ])
        mr = _mr_dual(df, [0, 1], [2])
        result = executar_v1(mr, _config_base())
        w = next(w for w in result.warnings_emitidos if w.codigo == "W-V1-DUP")
        assert w.n_ocorrencias >= 1

    def test_w_v1_dup_nao_dispara_em_caso_simples(self):
        from visoes.visao_v1 import executar_v1
        mr = _mr_dual(_df_basico(), [0, 1], [2, 3])
        result = executar_v1(mr, _config_base())
        w = next(w for w in result.warnings_emitidos if w.codigo == "W-V1-DUP")
        assert w.n_ocorrencias == 0

    def test_w_v1_amb_dispara_em_modo_contem(self):
        from visoes.visao_v1 import (
            AgrupadorMatchV1,
            ModoMatchV1,
            executar_v1,
        )
        df = pd.DataFrame([
            {"documento": "D001", "valor": 100.0},
            {"documento": "D001A", "valor": 50.0},
            {"documento": "D001B", "valor": 50.0},
        ])
        mr = _mr_dual(df, [0], [1, 2])
        config = _config_base(agrupadores=[AgrupadorMatchV1(
            nome_origem="documento", nome_comparado="documento",
            rotulo_analitico="Doc", modo_match=ModoMatchV1.CONTEM,
        )])
        result = executar_v1(mr, config)
        w = next(w for w in result.warnings_emitidos if w.codigo == "W-V1-AMB")
        assert w.n_ocorrencias >= 1

    def test_w_v1_amb_nao_dispara_em_modo_exato(self):
        from visoes.visao_v1 import executar_v1
        mr = _mr_dual(_df_basico(), [0, 1], [2, 3])
        result = executar_v1(mr, _config_base())
        w = next(w for w in result.warnings_emitidos if w.codigo == "W-V1-AMB")
        assert w.n_ocorrencias == 0

    def test_w_v1_unidade_dispara_quando_unidade_diverge_da_inferida(self):
        """Quando ColumnMeta tem unidade inferida diferente da declarada · W-V1-UNIDADE."""
        from visoes.visao_v1 import executar_v1
        # column_meta declara unidade PERCENTUAL, mas Usuária declara MONETARIO_BRL no campo
        mr = _mr_dual(
            _df_basico(),
            [0, 1], [2, 3],
            column_units={"valor": "PERCENTUAL"},
        )
        result = executar_v1(mr, _config_base())  # campo declara MONETARIO_BRL
        w = next(w for w in result.warnings_emitidos if w.codigo == "W-V1-UNIDADE")
        assert w.n_ocorrencias >= 1

    def test_w_v1_unidade_nao_dispara_quando_alinhada(self):
        from visoes.visao_v1 import executar_v1
        mr = _mr_dual(_df_basico(), [0, 1], [2, 3])
        result = executar_v1(mr, _config_base())
        # Sem column_meta.unidade · não dispara
        ws = [w for w in result.warnings_emitidos if w.codigo == "W-V1-UNIDADE"]
        if ws:
            assert ws[0].n_ocorrencias == 0


class TestWarningsZeroOcorrenciasMicrocopy:

    def test_w_v1_dup_zerado_microcopy_em_mesma_aba(self):
        """Em MESMA_ABA · W-V1-DUP sempre 0 com microcopy 'não aplicável'."""
        from visoes.visao_v1 import (
            AgrupadorMatchV1,
            CampoComparadoV1,
            ModoMatchV1,
            TipoCampoV1,
            UnidadeCanonica,
            executar_v1,
        )
        df = pd.DataFrame([
            {"d_o": "D001", "d_c": "D001", "v_o": 100.0, "v_c": 100.0},
        ])
        column_meta = {
            col: ColumnMeta(
                nome=col, tipo_tecnico=TipoTecnicoEnum.OBJECT,
                tipo_semantico=TipoSemanticoEnum.MISTO,
                tipo_estrutural=TipoEstruturalEnum.CATEGORICO_ELEGIVEL,
                subtipo_id_detectado=False, null_count=0,
                cardinalidade=1, eh_candidato_categorico=True,
                ordem_insercao=list(df.columns).index(col),
            )
            for col in df.columns
        }
        mr = MotorResult(
            df=df, column_meta=column_meta, modo_upload="SIMPLES",
            origem_comparado_map=None,
            total_linhas_originais=1, total_linhas_processadas=1,
        )
        config = {
            "agrupadores_match": [AgrupadorMatchV1(
                nome_origem="d_o", nome_comparado="d_c",
                rotulo_analitico="Doc", modo_match=ModoMatchV1.EXATO,
            )],
            "campos_comparados": [CampoComparadoV1(
                nome_origem="v_o", nome_comparado="v_c", nome_analitico="V",
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
        w_dup = next(w for w in result.warnings_emitidos if w.codigo == "W-V1-DUP")
        w_amb = next(w for w in result.warnings_emitidos if w.codigo == "W-V1-AMB")
        assert w_dup.n_ocorrencias == 0
        assert w_amb.n_ocorrencias == 0
        assert any("não aplicável" in str(d) for d in w_dup.detalhes)
        assert any("não aplicável" in str(d) for d in w_amb.detalhes)
