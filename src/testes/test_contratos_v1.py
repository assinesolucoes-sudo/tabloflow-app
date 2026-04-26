"""
test_contratos_v1.py — Testes de contratos Pydantic V1 (Fase 1 · V-V1)

Cobertura:
- Bloco A · Existência e tipagem das enums e constantes
- Bloco B · Invariantes Pydantic dos contratos V1
- Bloco C · Smoke import do módulo
"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal

import pandas as pd
import pytest
from pydantic import ValidationError

from contratos import (
    CabecalhoExecucao,
    CoracaoVisualRef,
    DiagnosticoVN,
    LeituraQualitativa,
    MotorResultMeta,
    QualidadeEstrutural,
    ResumoExecutivoPadrao,
)


# ===========================================================================
# Bloco A · Existência e tipagem
# ===========================================================================


class TestEnumsV1:
    def test_enum_caso_logico_v1_tem_2_valores(self):
        from visoes.visao_v1 import CasoLogicoV1
        assert len(list(CasoLogicoV1)) == 2
        assert CasoLogicoV1.ABAS_DISTINTAS.value == "ABAS_DISTINTAS"
        assert CasoLogicoV1.MESMA_ABA_EM_COLUNAS.value == "MESMA_ABA_EM_COLUNAS"

    def test_enum_modo_match_v1_tem_4_valores(self):
        from visoes.visao_v1 import ModoMatchV1
        assert len(list(ModoMatchV1)) == 4
        valores = {m.value for m in ModoMatchV1}
        assert valores == {"EXATO", "CONTEM", "INICIA_COM", "TERMINA_COM"}

    def test_enum_tipo_campo_v1_tem_7_valores(self):
        from visoes.visao_v1 import TipoCampoV1
        assert len(list(TipoCampoV1)) == 7

    def test_enum_classificacao_registro_v1_tem_6_valores(self):
        from visoes.visao_v1 import ClassificacaoRegistroV1
        assert len(list(ClassificacaoRegistroV1)) == 6

    def test_enum_status_campo_v1_tem_6_valores(self):
        from visoes.visao_v1 import StatusCampoV1
        assert len(list(StatusCampoV1)) == 6

    def test_enum_status_ponte_v1_tem_2_valores(self):
        from visoes.visao_v1 import StatusPonteV1
        assert len(list(StatusPonteV1)) == 2

    def test_enum_unidade_canonica_local_tem_8_valores(self):
        from visoes.visao_v1 import UnidadeCanonica
        assert len(list(UnidadeCanonica)) == 8


class TestConstantesV1:
    def test_default_unidade_por_tipo_cobre_7_tipos(self):
        from visoes.visao_v1 import DEFAULT_UNIDADE_POR_TIPO, TipoCampoV1
        assert len(DEFAULT_UNIDADE_POR_TIPO) == len(list(TipoCampoV1))
        for tipo in TipoCampoV1:
            assert tipo in DEFAULT_UNIDADE_POR_TIPO

    def test_default_epsilon_por_unidade_cobre_8_unidades(self):
        from visoes.visao_v1 import DEFAULT_EPSILON_POR_UNIDADE, UnidadeCanonica
        assert len(DEFAULT_EPSILON_POR_UNIDADE) == 8
        for unidade in UnidadeCanonica:
            assert unidade in DEFAULT_EPSILON_POR_UNIDADE

    def test_default_epsilon_monetario_brl_001(self):
        from visoes.visao_v1 import DEFAULT_EPSILON_POR_UNIDADE, UnidadeCanonica
        assert DEFAULT_EPSILON_POR_UNIDADE[UnidadeCanonica.MONETARIO_BRL] == Decimal("0.01")

    def test_ordem_classificacao_cobre_6_classes(self):
        from visoes.visao_v1 import ORDEM_CLASSIFICACAO, ClassificacaoRegistroV1
        assert len(ORDEM_CLASSIFICACAO) == 6
        for c in ClassificacaoRegistroV1:
            assert c in ORDEM_CLASSIFICACAO
        # Conciliado deve ter prioridade 0 (primeiro na ordem canônica)
        assert ORDEM_CLASSIFICACAO[ClassificacaoRegistroV1.CONCILIADO] == 0

    def test_unidades_inelegiveis_ponte_3_valores(self):
        from visoes.visao_v1 import UNIDADES_INELEGIVEIS_PONTE, UnidadeCanonica
        assert len(UNIDADES_INELEGIVEIS_PONTE) == 3
        assert UnidadeCanonica.PERCENTUAL in UNIDADES_INELEGIVEIS_PONTE
        assert UnidadeCanonica.ADIMENSIONAL in UNIDADES_INELEGIVEIS_PONTE
        assert UnidadeCanonica.RAZAO in UNIDADES_INELEGIVEIS_PONTE


# ===========================================================================
# Bloco B · Invariantes Pydantic
# ===========================================================================


def _agrupador_simples(modo="EXATO"):
    from visoes.visao_v1 import AgrupadorMatchV1, ModoMatchV1
    return AgrupadorMatchV1(
        nome_origem="documento",
        nome_comparado="documento",
        rotulo_analitico="Documento",
        modo_match=ModoMatchV1(modo),
    )


def _campo_simples(unidade="MONETARIO_BRL", nome="valor", tolerancia="0"):
    from visoes.visao_v1 import CampoComparadoV1, TipoCampoV1, UnidadeCanonica
    return CampoComparadoV1(
        nome_origem=f"{nome}_origem",
        nome_comparado=f"{nome}_comparado",
        nome_analitico=nome.title(),
        tipo_logico=TipoCampoV1.VALOR_MONETARIO,
        unidade=UnidadeCanonica(unidade),
        tolerancia=Decimal(tolerancia),
    )


def _conciliacao_realizada_abas_distintas():
    from visoes.visao_v1 import CasoLogicoV1, ConciliacaoRealizadaV1
    return ConciliacaoRealizadaV1(
        n_arquivos=2,
        arquivo_origem="origem.xlsx",
        aba_origem="Sheet1",
        arquivo_comparado="comparado.xlsx",
        aba_comparado="Sheet2",
        caso_logico_inferido=CasoLogicoV1.ABAS_DISTINTAS,
        origem_ux="Origem",
        comparado_ux="Comparado",
        rotulo_amigavel_declarado=False,
        agrupadores_match=[_agrupador_simples()],
        campos_comparados=[_campo_simples()],
        agrupadores_resumo_executivo=[],
        n_registros_origem=10,
        n_registros_comparado=10,
        n_processados=10,
    )


def _conciliacao_realizada_mesma_aba(unidade_campo="MONETARIO_BRL"):
    from visoes.visao_v1 import (
        AgrupadorMatchV1,
        CampoComparadoV1,
        CasoLogicoV1,
        ConciliacaoRealizadaV1,
        ModoMatchV1,
        TipoCampoV1,
        UnidadeCanonica,
    )
    return ConciliacaoRealizadaV1(
        n_arquivos=1,
        arquivo_origem="dados.xlsx",
        aba_origem="UnicaAba",
        arquivo_comparado="dados.xlsx",
        aba_comparado="UnicaAba",
        caso_logico_inferido=CasoLogicoV1.MESMA_ABA_EM_COLUNAS,
        origem_ux="Origem",
        comparado_ux="Comparado",
        rotulo_amigavel_declarado=False,
        agrupadores_match=[
            AgrupadorMatchV1(
                nome_origem="docOrigem",
                nome_comparado="docComparado",
                rotulo_analitico="Documento",
                modo_match=ModoMatchV1.EXATO,
            )
        ],
        campos_comparados=[
            CampoComparadoV1(
                nome_origem="valorOrigem",
                nome_comparado="valorComparado",
                nome_analitico="Valor",
                tipo_logico=TipoCampoV1.VALOR_MONETARIO,
                unidade=UnidadeCanonica(unidade_campo),
                tolerancia=Decimal("0"),
            )
        ],
        agrupadores_resumo_executivo=[],
        n_registros_origem=5,
        n_registros_comparado=5,
        n_processados=5,
    )


def _registro_conciliado_simples(
    chave="K001",
    classificacao=None,
    n_campos=1,
    com_diferenca=True,
):
    from visoes.visao_v1 import (
        CelulaCampoV1,
        ClassificacaoRegistroV1,
        RegistroConciliadoV1,
        StatusCampoV1,
    )
    cls = classificacao or ClassificacaoRegistroV1.CONCILIADO
    celulas = [
        CelulaCampoV1(
            campo_indice=i,
            valor_origem=Decimal("100.00") if com_diferenca else None,
            valor_comparado=Decimal("100.00") if com_diferenca else None,
            diferenca=Decimal("0.00") if com_diferenca else None,
            status_campo=StatusCampoV1.IGUAL if com_diferenca else StatusCampoV1.SEM_VALOR_AMBOS,
        )
        for i in range(n_campos)
    ]
    diff = Decimal("0") if cls in (ClassificacaoRegistroV1.CONCILIADO, ClassificacaoRegistroV1.DIVERGENTE_VALOR) else None
    return RegistroConciliadoV1(
        chave_consolidada=chave,
        valores_agrupadores={"Documento": chave},
        classificacao_estrutural=cls,
        valores_por_campo=celulas,
        diferenca_total_registro=diff,
        sigma_diferenca_total_registro=diff,
        variacao_total_registro_pct=None,
        observacoes=None,
    )


def _valor_por_campo_simples(unidade="MONETARIO_BRL", nome="Valor"):
    from visoes.visao_v1 import UnidadeCanonica, ValorPorCampoV1
    return ValorPorCampoV1(
        nome_analitico=nome,
        unidade=UnidadeCanonica(unidade),
        soma_origem=Decimal("100"),
        soma_comparado=Decimal("100"),
        diferenca_liquida=Decimal("0"),
        sigma_diferenca=Decimal("0"),
        n_tolerancia_absorvida=0,
        valor_tolerancia_absorvida=Decimal("0"),
    )


def _ponte_campo_simples(nome="Valor", unidade="MONETARIO_BRL", residuo="0", fecha=True):
    from visoes.visao_v1 import PonteCampoV1, UnidadeCanonica
    return PonteCampoV1(
        nome_analitico=nome,
        unidade=UnidadeCanonica(unidade),
        saldo_origem=Decimal("100"),
        ajuste_so_origem=Decimal("0"),
        ajuste_so_comparado=Decimal("0"),
        ajuste_divergentes_valor=Decimal("0"),
        ajuste_tolerancia_absorvida=Decimal("0"),
        saldo_comparado_esperado=Decimal("100"),
        saldo_comparado_real=Decimal("100"),
        residuo=Decimal(residuo),
        fecha=fecha,
    )


def _sintese_simples():
    from visoes.visao_v1 import SinteseDiagnosticoV1
    return SinteseDiagnosticoV1(
        n_tolerancia_absorvida=0,
        valor_tolerancia_absorvida=Decimal("0"),
        n_chaves_duplicadas=0,
        n_registros_afetados_duplicidade=0,
        n_chaves_ambiguas=0,
        n_registros_afetados_ambiguidade=0,
        n_warnings_ativos=0,
    )


def _config_aplicada_simples(caso="ABAS_DISTINTAS", agrupadores=None, campos=None, eps=None):
    from visoes.visao_v1 import (
        CasoLogicoV1,
        ConfigAplicadaV1,
        UnidadeCanonica,
    )
    return ConfigAplicadaV1(
        arquivo_origem="o.xlsx",
        aba_origem="A",
        arquivo_comparado="c.xlsx",
        aba_comparado="B",
        n_arquivos=2,
        caso_logico_inferido=CasoLogicoV1(caso),
        agrupadores_match=agrupadores or [_agrupador_simples()],
        campos_comparados=campos or [_campo_simples()],
        agrupadores_resumo_executivo=[],
        paleta_aplicada="Azul executivo",
        epsilon_por_unidade=eps or {UnidadeCanonica.MONETARIO_BRL: Decimal("0.01")},
        defaults_sobrescritos={},
        nulos_por_classificacao={},
    )


def _leitura_qualitativa_simples():
    from visoes.visao_v1 import LeituraQualitativaV1
    return LeituraQualitativaV1(
        texto="Texto parametrizado de 3 frases.",
        faixa_taxa="ALTA",
        modificadores_aplicados=[],
        agrupador_principal_citado=None,
    )


def _resumo_executivo_padrao_dummy(visao="V1"):
    return ResumoExecutivoPadrao(
        bloco_1_cabecalho=CabecalhoExecucao(
            visao=visao,
            data_execucao=datetime(2026, 4, 26, 12, 0, 0),
            modo_upload="DUAL",
            agrupadores=[],
            medida_principal=None,
        ),
        bloco_2_numeros_ancora={"taxa_conciliacao": 1.0},
        bloco_3_distribuicao={},
        bloco_4_elementos_destacados={},
        bloco_5_leitura_qualitativa=LeituraQualitativa(
            classificacao_ativa="ALTA",
            thresholds_usados={},
            alguma_leitura_alterada_por_edicao=False,
        ),
        bloco_6_qualidade_estrutural=QualidadeEstrutural(
            total_warnings=0,
            warnings_por_categoria={},
            ajustes_aplicados=0,
            tem_bloqueios_escapados=False,
        ),
    )


def _motor_meta_dummy():
    return MotorResultMeta(
        total_linhas_originais=10,
        total_linhas_processadas=10,
        modo_upload="DUAL",
    )


def _result_minimo_abas_distintas():
    """Cria ConciliacaoV1Result mínimo · 1 registro · 1 campo · 1 ponte · ABAS_DISTINTAS."""
    from visoes.visao_v1 import (
        ClassificacaoRegistroV1,
        ConciliacaoV1Result,
        CoberturaV1,
        StatusPonteV1,
    )
    cr = _conciliacao_realizada_abas_distintas()
    registros = [_registro_conciliado_simples()]
    return ConciliacaoV1Result(
        config_usada={"caso": "ABAS_DISTINTAS"},
        motor_result_meta=_motor_meta_dummy(),
        base_analitica=pd.DataFrame([{"chave": "K001"}]),
        resumo_executivo=_resumo_executivo_padrao_dummy("V1"),
        coracao_visual=CoracaoVisualRef(
            nome_aba="Mapa de Conciliação",
            tipo="TABELA_HEATMAP",
            capabilities_requeridas=[],
        ),
        bloqueios_disparados=[],
        warnings=[],
        diagnostico=DiagnosticoVN(),
        conciliacao_realizada=cr,
        classificacao_por_registro=registros,
        contagem_por_classificacao={
            ClassificacaoRegistroV1.CONCILIADO: 1,
            ClassificacaoRegistroV1.DIVERGENTE_VALOR: 0,
            ClassificacaoRegistroV1.SO_ORIGEM: 0,
            ClassificacaoRegistroV1.SO_COMPARADO: 0,
            ClassificacaoRegistroV1.DIVERGENCIA_DUPLICIDADE: 0,
            ClassificacaoRegistroV1.DIVERGENCIA_AMBIGUIDADE: 0,
        },
        cobertura=CoberturaV1(
            n_origem_com_par=1,
            n_origem_sem_par=0,
            cobertura_origem_pct=Decimal("1"),
            n_comparado_com_par=1,
            n_comparado_sem_par=0,
            cobertura_comparado_pct=Decimal("1"),
        ),
        valor_por_campo=[_valor_por_campo_simples()],
        resumo_por_agrupador_executivo=None,
        pontes=[_ponte_campo_simples()],
        status_ponte_geral=StatusPonteV1.FECHA,
        sintese_diagnostico=_sintese_simples(),
        config_aplicada=_config_aplicada_simples(),
        leitura_qualitativa=_leitura_qualitativa_simples(),
        warnings_emitidos=[],
        modelo_aplicado=None,
    )


class TestInvariantesContratoPrincipal:

    def test_conciliacao_v1_result_aceita_construcao_minima_abas_distintas(self):
        result = _result_minimo_abas_distintas()
        assert result.visao == "V1"
        assert result.visao_id == "V1"
        assert len(result.classificacao_por_registro) == 1

    def test_conciliacao_v1_result_zera_4_classes_em_mesma_aba(self):
        from visoes.visao_v1 import (
            ClassificacaoRegistroV1,
            ConciliacaoV1Result,
            StatusPonteV1,
        )
        cr = _conciliacao_realizada_mesma_aba()
        registros = [
            _registro_conciliado_simples(),
            _registro_conciliado_simples(
                chave="K002",
                classificacao=ClassificacaoRegistroV1.DIVERGENTE_VALOR,
            ),
        ]
        # As 4 classes inaplicáveis ZERADAS
        contagem = {
            ClassificacaoRegistroV1.CONCILIADO: 1,
            ClassificacaoRegistroV1.DIVERGENTE_VALOR: 1,
            ClassificacaoRegistroV1.SO_ORIGEM: 0,
            ClassificacaoRegistroV1.SO_COMPARADO: 0,
            ClassificacaoRegistroV1.DIVERGENCIA_DUPLICIDADE: 0,
            ClassificacaoRegistroV1.DIVERGENCIA_AMBIGUIDADE: 0,
        }
        result = ConciliacaoV1Result(
            config_usada={},
            motor_result_meta=_motor_meta_dummy(),
            base_analitica=pd.DataFrame([{"chave": "K001"}]),
            resumo_executivo=_resumo_executivo_padrao_dummy("V1"),
            coracao_visual=CoracaoVisualRef(
                nome_aba="Mapa de Conciliação", tipo="TABELA_HEATMAP", capabilities_requeridas=[]
            ),
            diagnostico=DiagnosticoVN(),
            conciliacao_realizada=cr,
            classificacao_por_registro=registros,
            contagem_por_classificacao=contagem,
            cobertura=None,  # invariante MESMA_ABA
            valor_por_campo=[_valor_por_campo_simples()],
            pontes=[_ponte_campo_simples()],
            status_ponte_geral=StatusPonteV1.FECHA,
            sintese_diagnostico=_sintese_simples(),
            config_aplicada=_config_aplicada_simples(caso="MESMA_ABA_EM_COLUNAS"),
            leitura_qualitativa=_leitura_qualitativa_simples(),
        )
        assert result.contagem_por_classificacao[ClassificacaoRegistroV1.SO_ORIGEM] == 0

    def test_conciliacao_v1_result_falha_se_so_origem_nao_zerado_em_mesma_aba(self):
        from visoes.visao_v1 import (
            ClassificacaoRegistroV1,
            ConciliacaoV1Result,
            StatusPonteV1,
        )
        cr = _conciliacao_realizada_mesma_aba()
        contagem = {
            ClassificacaoRegistroV1.CONCILIADO: 1,
            ClassificacaoRegistroV1.DIVERGENTE_VALOR: 0,
            ClassificacaoRegistroV1.SO_ORIGEM: 1,  # ← inválido em MESMA_ABA
            ClassificacaoRegistroV1.SO_COMPARADO: 0,
            ClassificacaoRegistroV1.DIVERGENCIA_DUPLICIDADE: 0,
            ClassificacaoRegistroV1.DIVERGENCIA_AMBIGUIDADE: 0,
        }
        with pytest.raises(ValidationError, match="MESMA_ABA_EM_COLUNAS exige contagem"):
            ConciliacaoV1Result(
                config_usada={},
                motor_result_meta=_motor_meta_dummy(),
                base_analitica=pd.DataFrame([{"chave": "K001"}, {"chave": "K002"}]),
                resumo_executivo=_resumo_executivo_padrao_dummy("V1"),
                coracao_visual=CoracaoVisualRef(
                    nome_aba="Mapa de Conciliação", tipo="TABELA_HEATMAP", capabilities_requeridas=[]
                ),
                diagnostico=DiagnosticoVN(),
                conciliacao_realizada=cr,
                classificacao_por_registro=[
                    _registro_conciliado_simples(),
                    _registro_conciliado_simples(chave="K002"),
                ],
                contagem_por_classificacao=contagem,
                cobertura=None,
                valor_por_campo=[_valor_por_campo_simples()],
                pontes=[_ponte_campo_simples()],
                status_ponte_geral=StatusPonteV1.FECHA,
                sintese_diagnostico=_sintese_simples(),
                config_aplicada=_config_aplicada_simples(caso="MESMA_ABA_EM_COLUNAS"),
                leitura_qualitativa=_leitura_qualitativa_simples(),
            )

    def test_conciliacao_v1_result_cobertura_obrigatoriamente_none_em_mesma_aba(self):
        from visoes.visao_v1 import (
            ClassificacaoRegistroV1,
            ConciliacaoV1Result,
            CoberturaV1,
            StatusPonteV1,
        )
        cr = _conciliacao_realizada_mesma_aba()
        cobertura_invalida = CoberturaV1(
            n_origem_com_par=1, n_origem_sem_par=0, cobertura_origem_pct=Decimal("1"),
            n_comparado_com_par=1, n_comparado_sem_par=0, cobertura_comparado_pct=Decimal("1"),
        )
        contagem = {c: 0 for c in ClassificacaoRegistroV1}
        contagem[ClassificacaoRegistroV1.CONCILIADO] = 1
        with pytest.raises(ValidationError, match="MESMA_ABA_EM_COLUNAS exige cobertura == None"):
            ConciliacaoV1Result(
                config_usada={},
                motor_result_meta=_motor_meta_dummy(),
                base_analitica=pd.DataFrame([{"chave": "K001"}]),
                resumo_executivo=_resumo_executivo_padrao_dummy("V1"),
                coracao_visual=CoracaoVisualRef(
                    nome_aba="Mapa de Conciliação", tipo="TABELA_HEATMAP", capabilities_requeridas=[]
                ),
                diagnostico=DiagnosticoVN(),
                conciliacao_realizada=cr,
                classificacao_por_registro=[_registro_conciliado_simples()],
                contagem_por_classificacao=contagem,
                cobertura=cobertura_invalida,  # ← inválido em MESMA_ABA
                valor_por_campo=[_valor_por_campo_simples()],
                pontes=[_ponte_campo_simples()],
                status_ponte_geral=StatusPonteV1.FECHA,
                sintese_diagnostico=_sintese_simples(),
                config_aplicada=_config_aplicada_simples(caso="MESMA_ABA_EM_COLUNAS"),
                leitura_qualitativa=_leitura_qualitativa_simples(),
            )

    def test_conciliacao_v1_result_falha_se_soma_contagem_difere_de_classificacao(self):
        from visoes.visao_v1 import (
            ClassificacaoRegistroV1,
            ConciliacaoV1Result,
            StatusPonteV1,
        )
        cr = _conciliacao_realizada_abas_distintas()
        # 1 registro mas contagem soma 2
        contagem = {c: 0 for c in ClassificacaoRegistroV1}
        contagem[ClassificacaoRegistroV1.CONCILIADO] = 2
        with pytest.raises(ValidationError, match="!= len"):
            ConciliacaoV1Result(
                config_usada={},
                motor_result_meta=_motor_meta_dummy(),
                base_analitica=pd.DataFrame([{"chave": "K001"}]),
                resumo_executivo=_resumo_executivo_padrao_dummy("V1"),
                coracao_visual=CoracaoVisualRef(
                    nome_aba="Mapa de Conciliação", tipo="TABELA_HEATMAP", capabilities_requeridas=[]
                ),
                diagnostico=DiagnosticoVN(),
                conciliacao_realizada=cr,
                classificacao_por_registro=[_registro_conciliado_simples()],
                contagem_por_classificacao=contagem,
                cobertura=None,
                valor_por_campo=[_valor_por_campo_simples()],
                pontes=[_ponte_campo_simples()],
                status_ponte_geral=StatusPonteV1.FECHA,
                sintese_diagnostico=_sintese_simples(),
                config_aplicada=_config_aplicada_simples(caso="ABAS_DISTINTAS"),
                leitura_qualitativa=_leitura_qualitativa_simples(),
            )

    def test_conciliacao_v1_result_falha_se_pontes_nao_bate_campos_elegiveis(self):
        from visoes.visao_v1 import (
            CampoComparadoV1,
            ClassificacaoRegistroV1,
            ConciliacaoV1Result,
            StatusPonteV1,
            TipoCampoV1,
            UnidadeCanonica,
        )
        # Config tem 2 campos: 1 monetário (elegível) + 1 percentual (inelegível)
        # → pontes esperadas: 1
        cr = _conciliacao_realizada_abas_distintas()
        cr_dict = cr.model_dump()
        cr_dict["campos_comparados"] = [
            cr.campos_comparados[0],
            CampoComparadoV1(
                nome_origem="taxa_o", nome_comparado="taxa_c", nome_analitico="Taxa",
                tipo_logico=TipoCampoV1.PERCENTUAL,
                unidade=UnidadeCanonica.PERCENTUAL,
                tolerancia=Decimal("0"),
            ),
        ]
        # Reconstruct with model
        from visoes.visao_v1 import ConciliacaoRealizadaV1
        cr2 = ConciliacaoRealizadaV1.model_validate(cr_dict)
        contagem = {c: 0 for c in ClassificacaoRegistroV1}
        contagem[ClassificacaoRegistroV1.CONCILIADO] = 1
        # Provo: 0 pontes (incorrect · esperado 1)
        with pytest.raises(ValidationError, match="len\\(pontes\\)"):
            ConciliacaoV1Result(
                config_usada={},
                motor_result_meta=_motor_meta_dummy(),
                base_analitica=pd.DataFrame([{"k": "K001"}]),
                resumo_executivo=_resumo_executivo_padrao_dummy("V1"),
                coracao_visual=CoracaoVisualRef(
                    nome_aba="Mapa de Conciliação", tipo="TABELA_HEATMAP", capabilities_requeridas=[]
                ),
                diagnostico=DiagnosticoVN(),
                conciliacao_realizada=cr2,
                classificacao_por_registro=[_registro_conciliado_simples(n_campos=2)],
                contagem_por_classificacao=contagem,
                cobertura=None,
                valor_por_campo=[
                    _valor_por_campo_simples(),
                    _valor_por_campo_simples(unidade="PERCENTUAL", nome="Taxa"),
                ],
                pontes=[],  # ← inválido (esperado 1)
                status_ponte_geral=StatusPonteV1.FECHA,
                sintese_diagnostico=_sintese_simples(),
                config_aplicada=_config_aplicada_simples(caso="ABAS_DISTINTAS"),
                leitura_qualitativa=_leitura_qualitativa_simples(),
            )


class TestInvariantesContratosFilhos:

    def test_conciliacao_realizada_v1_aceita_minimo(self):
        cr = _conciliacao_realizada_abas_distintas()
        assert cr.n_arquivos == 2

    def test_conciliacao_realizada_v1_falha_se_agrupadores_zero(self):
        from visoes.visao_v1 import CasoLogicoV1, ConciliacaoRealizadaV1
        with pytest.raises(ValidationError, match="agrupadores_match"):
            ConciliacaoRealizadaV1(
                n_arquivos=2,
                arquivo_origem="o.xlsx", aba_origem="A",
                arquivo_comparado="c.xlsx", aba_comparado="B",
                caso_logico_inferido=CasoLogicoV1.ABAS_DISTINTAS,
                origem_ux="Origem", comparado_ux="Comparado",
                rotulo_amigavel_declarado=False,
                agrupadores_match=[],  # ← inválido
                campos_comparados=[_campo_simples()],
                n_registros_origem=10, n_registros_comparado=10, n_processados=10,
            )

    def test_conciliacao_realizada_v1_falha_se_agrupadores_excede_5(self):
        from visoes.visao_v1 import CasoLogicoV1, ConciliacaoRealizadaV1
        with pytest.raises(ValidationError, match="agrupadores_match"):
            ConciliacaoRealizadaV1(
                n_arquivos=2,
                arquivo_origem="o.xlsx", aba_origem="A",
                arquivo_comparado="c.xlsx", aba_comparado="B",
                caso_logico_inferido=CasoLogicoV1.ABAS_DISTINTAS,
                origem_ux="Origem", comparado_ux="Comparado",
                rotulo_amigavel_declarado=False,
                agrupadores_match=[_agrupador_simples() for _ in range(6)],  # ← inválido
                campos_comparados=[_campo_simples()],
                n_registros_origem=10, n_registros_comparado=10, n_processados=10,
            )

    def test_conciliacao_realizada_v1_falha_se_campos_excede_10(self):
        from visoes.visao_v1 import CasoLogicoV1, ConciliacaoRealizadaV1
        with pytest.raises(ValidationError, match="campos_comparados"):
            ConciliacaoRealizadaV1(
                n_arquivos=2,
                arquivo_origem="o.xlsx", aba_origem="A",
                arquivo_comparado="c.xlsx", aba_comparado="B",
                caso_logico_inferido=CasoLogicoV1.ABAS_DISTINTAS,
                origem_ux="Origem", comparado_ux="Comparado",
                rotulo_amigavel_declarado=False,
                agrupadores_match=[_agrupador_simples()],
                campos_comparados=[_campo_simples(nome=f"v{i}") for i in range(11)],  # ← inválido
                n_registros_origem=10, n_registros_comparado=10, n_processados=10,
            )

    def test_conciliacao_realizada_v1_falha_se_n_arquivos_1_mas_arquivos_diferem(self):
        from visoes.visao_v1 import CasoLogicoV1, ConciliacaoRealizadaV1
        with pytest.raises(ValidationError, match="n_arquivos==1 exige"):
            ConciliacaoRealizadaV1(
                n_arquivos=1,
                arquivo_origem="o.xlsx", aba_origem="A",
                arquivo_comparado="c.xlsx",  # ← diferente · inválido
                aba_comparado="B",
                caso_logico_inferido=CasoLogicoV1.ABAS_DISTINTAS,
                origem_ux="Origem", comparado_ux="Comparado",
                rotulo_amigavel_declarado=False,
                agrupadores_match=[_agrupador_simples()],
                campos_comparados=[_campo_simples()],
                n_registros_origem=10, n_registros_comparado=10, n_processados=10,
            )

    def test_conciliacao_realizada_v1_falha_mesma_aba_com_abas_diferentes(self):
        from visoes.visao_v1 import CasoLogicoV1, ConciliacaoRealizadaV1
        with pytest.raises(ValidationError, match="MESMA_ABA_EM_COLUNAS exige aba_origem"):
            ConciliacaoRealizadaV1(
                n_arquivos=1,
                arquivo_origem="o.xlsx", aba_origem="A",
                arquivo_comparado="o.xlsx", aba_comparado="B",  # ← diferente · inválido em MESMA_ABA
                caso_logico_inferido=CasoLogicoV1.MESMA_ABA_EM_COLUNAS,
                origem_ux="Origem", comparado_ux="Comparado",
                rotulo_amigavel_declarado=False,
                agrupadores_match=[_agrupador_simples()],
                campos_comparados=[_campo_simples()],
                n_registros_origem=10, n_registros_comparado=10, n_processados=10,
            )

    def test_conciliacao_realizada_v1_rotulo_amigavel_validado(self):
        from visoes.visao_v1 import CasoLogicoV1, ConciliacaoRealizadaV1
        # rotulo_amigavel_declarado deve ser True dado os UX customizados
        with pytest.raises(ValidationError, match="rotulo_amigavel_declarado"):
            ConciliacaoRealizadaV1(
                n_arquivos=2,
                arquivo_origem="o.xlsx", aba_origem="A",
                arquivo_comparado="c.xlsx", aba_comparado="B",
                caso_logico_inferido=CasoLogicoV1.ABAS_DISTINTAS,
                origem_ux="ERP", comparado_ux="DW",  # ambos != defaults
                rotulo_amigavel_declarado=False,  # ← inconsistente
                agrupadores_match=[_agrupador_simples()],
                campos_comparados=[_campo_simples()],
                n_registros_origem=10, n_registros_comparado=10, n_processados=10,
            )

    def test_campo_comparado_v1_aceita_default(self):
        c = _campo_simples()
        assert c.tolerancia == Decimal("0")

    def test_campo_comparado_v1_falha_se_tolerancia_negativa(self):
        from visoes.visao_v1 import CampoComparadoV1, TipoCampoV1, UnidadeCanonica
        with pytest.raises(ValidationError, match="tolerancia deve ser >= 0"):
            CampoComparadoV1(
                nome_origem="o", nome_comparado="c", nome_analitico="X",
                tipo_logico=TipoCampoV1.VALOR_MONETARIO,
                unidade=UnidadeCanonica.MONETARIO_BRL,
                tolerancia=Decimal("-0.01"),
            )

    def test_warning_v1_codigo_aceita_w_v1(self):
        from visoes.visao_v1 import WarningV1
        w = WarningV1(codigo="W-V1-TOL", severidade="INFORMATIVO", n_ocorrencias=3)
        assert w.codigo == "W-V1-TOL"

    def test_warning_v1_codigo_aceita_w_herdado_motor(self):
        from visoes.visao_v1 import WarningV1
        w = WarningV1(codigo="W-B01", severidade="ALERTA_ESTRUTURAL", n_ocorrencias=1)
        assert w.codigo == "W-B01"

    def test_warning_v1_codigo_falha_se_nao_w(self):
        from visoes.visao_v1 import WarningV1
        with pytest.raises(ValidationError, match="codigo deve começar"):
            WarningV1(codigo="X-V1-TOL", severidade="INFORMATIVO", n_ocorrencias=0)

    def test_celula_campo_v1_aceita_decimal_none(self):
        from visoes.visao_v1 import CelulaCampoV1, StatusCampoV1
        c = CelulaCampoV1(
            campo_indice=0,
            valor_origem=None,
            valor_comparado=None,
            diferenca=None,
            status_campo=StatusCampoV1.SEM_VALOR_AMBOS,
        )
        assert c.valor_origem is None

    def test_registro_conciliado_v1_aceita_diferenca_none(self):
        from visoes.visao_v1 import (
            CelulaCampoV1,
            ClassificacaoRegistroV1,
            RegistroConciliadoV1,
            StatusCampoV1,
        )
        r = RegistroConciliadoV1(
            chave_consolidada="K-SO",
            valores_agrupadores={"x": "y"},
            classificacao_estrutural=ClassificacaoRegistroV1.SO_ORIGEM,
            valores_por_campo=[
                CelulaCampoV1(
                    campo_indice=0,
                    valor_origem=Decimal("10"),
                    valor_comparado=None,
                    diferenca=None,
                    status_campo=StatusCampoV1.SEM_VALOR_COMPARADO,
                )
            ],
            diferenca_total_registro=None,
            sigma_diferenca_total_registro=None,
            variacao_total_registro_pct=None,
        )
        assert r.diferenca_total_registro is None


# ===========================================================================
# Bloco C · Smoke import
# ===========================================================================


class TestSmokeImportVisaoV1:

    def test_visao_v1_module_imports_sem_erro(self):
        import visoes.visao_v1  # noqa: F401

    def test_executar_v1_levanta_b_v1_no_upload_quando_motor_result_none(self):
        from visoes.visao_v1 import executar_v1
        with pytest.raises(ValueError, match="B-V1-NO-UPLOAD"):
            executar_v1(motor_result=None, config={})  # type: ignore[arg-type]
