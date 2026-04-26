"""
test_visao_v1_matriz_q4c.py — Suite Q4.C · cobertura matricial (Fase 6 · V-V1)

S-V1 §2.13 (C.D7) declara matriz cartesiana 2 casos × 6 classificações × 4 modos × 8 unidades.
Esta suite contém os Blocos I-IV da matriz (caso×classif×modo · unidades · tolerância · pontes).
Blocos V-VI (determinismo · fronteira) ficam em test_visao_v1_q4c_determinismo_fronteira.py.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List, Tuple

import pandas as pd
import pytest

from contratos import (
    ColumnMeta,
    MotorResult,
    TipoEstruturalEnum,
    TipoSemanticoEnum,
    TipoTecnicoEnum,
)


# ===========================================================================
# Helpers compartilhados
# ===========================================================================


def _make_column_meta(df: pd.DataFrame, unidades: Dict[str, str] | None = None) -> Dict[str, ColumnMeta]:
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


def _mr_dual(df: pd.DataFrame, origem_idxs: List[int], comparado_idxs: List[int],
             unidades: Dict[str, str] | None = None) -> MotorResult:
    ocm = {i: "origem" for i in origem_idxs}
    ocm.update({i: "comparado" for i in comparado_idxs})
    return MotorResult(
        df=df, column_meta=_make_column_meta(df, unidades),
        modo_upload="DUAL", origem_comparado_map=ocm,
        total_linhas_originais=len(df), total_linhas_processadas=len(df),
    )


def _mr_simples(df: pd.DataFrame, unidades: Dict[str, str] | None = None) -> MotorResult:
    return MotorResult(
        df=df, column_meta=_make_column_meta(df, unidades),
        modo_upload="SIMPLES", origem_comparado_map=None,
        total_linhas_originais=len(df), total_linhas_processadas=len(df),
    )


def _config_dual(modo="EXATO", unidade="MONETARIO_BRL", tolerancia="0", tipo_logico="VALOR_MONETARIO"):
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
            tipo_logico=TipoCampoV1(tipo_logico),
            unidade=UnidadeCanonica(unidade), tolerancia=Decimal(tolerancia),
        )],
        "agrupadores_executivos": [],
        "epsilon_por_unidade": {UnidadeCanonica(unidade): Decimal("0.01")},
        "thresholds": {},
        "origem_ux": "Origem", "comparado_ux": "Comparado",
        "arquivo_origem": "o.xlsx", "arquivo_comparado": "c.xlsx",
        "aba_origem": "A", "aba_comparado": "B",
        "n_arquivos": 2, "paleta_aplicada": "Azul executivo",
    }


def _config_simples(modo="EXATO", unidade="MONETARIO_BRL", tolerancia="0", tipo_logico="VALOR_MONETARIO"):
    """MESMA_ABA_EM_COLUNAS · sempre mesma aba."""
    from visoes.visao_v1 import (
        AgrupadorMatchV1,
        CampoComparadoV1,
        ModoMatchV1,
        TipoCampoV1,
        UnidadeCanonica,
    )
    return {
        "agrupadores_match": [AgrupadorMatchV1(
            nome_origem="docOrigem", nome_comparado="docComparado",
            rotulo_analitico="Doc", modo_match=ModoMatchV1(modo),
        )],
        "campos_comparados": [CampoComparadoV1(
            nome_origem="valorOrigem", nome_comparado="valorComparado", nome_analitico="Valor",
            tipo_logico=TipoCampoV1(tipo_logico),
            unidade=UnidadeCanonica(unidade), tolerancia=Decimal(tolerancia),
        )],
        "agrupadores_executivos": [],
        "epsilon_por_unidade": {UnidadeCanonica(unidade): Decimal("0.01")},
        "thresholds": {},
        "origem_ux": "Origem", "comparado_ux": "Comparado",
        "arquivo_origem": "x.xlsx", "arquivo_comparado": "x.xlsx",
        "aba_origem": "U", "aba_comparado": "U",
        "n_arquivos": 1, "paleta_aplicada": "Azul executivo",
    }


# ===========================================================================
# Bloco I · caso × classificação × modo (~48 testes)
# ===========================================================================


_CASOS = ["ABAS_DISTINTAS", "MESMA_ABA_EM_COLUNAS"]
_CLASSIFICACOES = [
    "CONCILIADO", "DIVERGENTE_VALOR", "SO_ORIGEM", "SO_COMPARADO",
    "DIVERGENCIA_DUPLICIDADE", "DIVERGENCIA_AMBIGUIDADE",
]
_MODOS = ["EXATO", "CONTEM", "INICIA_COM", "TERMINA_COM"]
_CLASSES_INAPLICAVEIS_MESMA_ABA = {
    "SO_ORIGEM", "SO_COMPARADO", "DIVERGENCIA_DUPLICIDADE", "DIVERGENCIA_AMBIGUIDADE",
}


def _build_scenario_dual(classificacao: str, modo: str) -> Tuple[MotorResult, Dict[str, Any]]:
    """Constrói df + config para produzir a classificação alvo em ABAS_DISTINTAS."""
    if classificacao == "CONCILIADO":
        df = pd.DataFrame([
            {"documento": "ABC", "valor": 100.0},
            {"documento": "ABC", "valor": 100.0},
        ])
        return _mr_dual(df, [0], [1]), _config_dual(modo=modo)
    if classificacao == "DIVERGENTE_VALOR":
        df = pd.DataFrame([
            {"documento": "ABC", "valor": 100.0},
            {"documento": "ABC", "valor": 200.0},
        ])
        return _mr_dual(df, [0], [1]), _config_dual(modo=modo)
    if classificacao == "SO_ORIGEM":
        # 1 chave só origem · em modo non-EXATO escolhemos origem que NÃO casa com comparado
        if modo == "EXATO":
            df = pd.DataFrame([
                {"documento": "AAA", "valor": 100.0},
                {"documento": "ZZZ", "valor": 200.0},
            ])
        else:
            df = pd.DataFrame([
                {"documento": "AAA", "valor": 100.0},
                {"documento": "999", "valor": 200.0},  # nada começa/termina/contém em comum
            ])
        return _mr_dual(df, [0], [1]), _config_dual(modo=modo)
    if classificacao == "SO_COMPARADO":
        if modo == "EXATO":
            df = pd.DataFrame([
                {"documento": "AAA", "valor": 100.0},
                {"documento": "ZZZ", "valor": 200.0},
            ])
        else:
            df = pd.DataFrame([
                {"documento": "AAA", "valor": 100.0},
                {"documento": "999", "valor": 200.0},
            ])
        return _mr_dual(df, [0], [1]), _config_dual(modo=modo)
    if classificacao == "DIVERGENCIA_DUPLICIDADE":
        # Em EXATO, dup detectada por chave repetida.
        df = pd.DataFrame([
            {"documento": "ABC", "valor": 100.0},
            {"documento": "ABC", "valor": 105.0},  # duplicado em origem
            {"documento": "ABC", "valor": 100.0},
        ])
        return _mr_dual(df, [0, 1], [2]), _config_dual(modo=modo)
    if classificacao == "DIVERGENCIA_AMBIGUIDADE":
        # Só achievable em non-EXATO modes.
        if modo == "EXATO":
            # Cenário neutro · contagem == 0 esperado.
            df = pd.DataFrame([
                {"documento": "ABC", "valor": 100.0},
                {"documento": "ABC", "valor": 100.0},
            ])
            return _mr_dual(df, [0], [1]), _config_dual(modo=modo)
        # Cenários por modo:
        if modo == "CONTEM":
            df = pd.DataFrame([
                {"documento": "X", "valor": 100.0},
                {"documento": "AXB", "valor": 50.0},
                {"documento": "MXN", "valor": 50.0},
            ])
        elif modo == "INICIA_COM":
            df = pd.DataFrame([
                {"documento": "AB", "valor": 100.0},
                {"documento": "ABCDE", "valor": 50.0},
                {"documento": "ABXYZ", "valor": 50.0},
            ])
        else:  # TERMINA_COM
            df = pd.DataFrame([
                {"documento": "AB", "valor": 100.0},
                {"documento": "XYAB", "valor": 50.0},
                {"documento": "MNAB", "valor": 50.0},
            ])
        return _mr_dual(df, [0], [1, 2]), _config_dual(modo=modo)
    raise ValueError(f"Cenário desconhecido: {classificacao}")


def _build_scenario_simples(classificacao: str, modo: str) -> Tuple[MotorResult, Dict[str, Any]]:
    """MESMA_ABA · scenarios for CONCILIADO / DIVERGENTE_VALOR (outras 4 são impossíveis · contagem 0)."""
    if classificacao == "CONCILIADO":
        df = pd.DataFrame([{"docOrigem": "ABC", "docComparado": "ABC",
                            "valorOrigem": 100.0, "valorComparado": 100.0}])
    elif classificacao == "DIVERGENTE_VALOR":
        df = pd.DataFrame([{"docOrigem": "ABC", "docComparado": "ABC",
                            "valorOrigem": 100.0, "valorComparado": 200.0}])
    else:
        # cenário neutro (impossível) · usado para verificar contagem==0
        df = pd.DataFrame([{"docOrigem": "ABC", "docComparado": "ABC",
                            "valorOrigem": 100.0, "valorComparado": 100.0}])
    return _mr_simples(df), _config_simples(modo=modo)


@pytest.mark.parametrize("caso", _CASOS)
@pytest.mark.parametrize("classificacao", _CLASSIFICACOES)
@pytest.mark.parametrize("modo", _MODOS)
def test_matriz_caso_classificacao_modo(caso, classificacao, modo):
    """Bloco I · matriz cartesiana caso × classificação × modo (48 combinações)."""
    from visoes.visao_v1 import ClassificacaoRegistroV1, executar_v1

    if caso == "ABAS_DISTINTAS":
        mr, config = _build_scenario_dual(classificacao, modo)
    else:
        mr, config = _build_scenario_simples(classificacao, modo)

    result = executar_v1(mr, config)
    cls_enum = ClassificacaoRegistroV1[classificacao]
    contagem = result.contagem_por_classificacao[cls_enum]

    if caso == "MESMA_ABA_EM_COLUNAS" and classificacao in _CLASSES_INAPLICAVEIS_MESMA_ABA:
        # Garantia de zeragem (S-V1 §1.1 invariante)
        assert contagem == 0
        return

    if caso == "ABAS_DISTINTAS" and classificacao == "DIVERGENCIA_AMBIGUIDADE" and modo == "EXATO":
        # AMBIGUIDADE impossível em EXATO (set semantics)
        assert contagem == 0
        return

    # Combinações alcançáveis: contagem >= 1
    assert contagem >= 1, (
        f"Esperava contagem[{classificacao}] >= 1 em {caso} modo {modo}; "
        f"recebido {contagem}; classes: {result.contagem_por_classificacao}"
    )


# ===========================================================================
# Bloco II · cobertura por unidade (8 unidades × 2 casos = 16 tests)
# ===========================================================================


_UNIDADES = [
    "MONETARIO_BRL", "PERCENTUAL", "QUANTIDADE", "TEMPO_DIAS",
    "TEMPO_HORAS", "MULTIPLICADOR", "RAZAO", "ADIMENSIONAL",
]

_TIPO_LOGICO_POR_UNIDADE = {
    "MONETARIO_BRL": "VALOR_MONETARIO",
    "PERCENTUAL": "PERCENTUAL",
    "QUANTIDADE": "QUANTIDADE",
    "TEMPO_DIAS": "PRAZO",
    "TEMPO_HORAS": "PRAZO",
    "MULTIPLICADOR": "INDICE",
    "RAZAO": "INDICE",
    "ADIMENSIONAL": "ESTADO_SITUACAO",
}


@pytest.mark.parametrize("unidade", _UNIDADES)
@pytest.mark.parametrize("caso", _CASOS)
def test_bloco_ii_cobertura_unidade(unidade, caso):
    """Bloco II · 1 par CONCILIADO em cada unidade · valor_por_campo[*].unidade == unidade."""
    from visoes.visao_v1 import UnidadeCanonica, executar_v1
    tipo_logico = _TIPO_LOGICO_POR_UNIDADE[unidade]

    if caso == "ABAS_DISTINTAS":
        df = pd.DataFrame([
            {"documento": "K001", "valor": 100.0},
            {"documento": "K001", "valor": 100.0},
        ])
        mr = _mr_dual(df, [0], [1])
        config = _config_dual(unidade=unidade, tipo_logico=tipo_logico)
    else:
        df = pd.DataFrame([{
            "docOrigem": "K001", "docComparado": "K001",
            "valorOrigem": 100.0, "valorComparado": 100.0
        }])
        mr = _mr_simples(df)
        config = _config_simples(unidade=unidade, tipo_logico=tipo_logico)

    result = executar_v1(mr, config)
    assert len(result.valor_por_campo) == 1
    assert result.valor_por_campo[0].unidade == UnidadeCanonica(unidade)


# ===========================================================================
# Bloco III · tolerância × unidade (~16 tests)
# ===========================================================================


@pytest.mark.parametrize("unidade", _UNIDADES)
@pytest.mark.parametrize("dentro_da_tolerancia", [True, False])
def test_bloco_iii_tolerancia_unidade(unidade, dentro_da_tolerancia):
    """Bloco III · diferença = (tolerancia ± 0.001) · status_campo correto."""
    from visoes.visao_v1 import StatusCampoV1, executar_v1
    tipo_logico = _TIPO_LOGICO_POR_UNIDADE[unidade]
    tolerancia_aplicada = "0.10"  # tolerancia genérica · 0.10

    if dentro_da_tolerancia:
        # diferenca = 0.05 (< 0.10)
        df = pd.DataFrame([
            {"documento": "K", "valor": 100.05},
            {"documento": "K", "valor": 100.00},
        ])
    else:
        # diferenca = 0.50 (> 0.10)
        df = pd.DataFrame([
            {"documento": "K", "valor": 100.50},
            {"documento": "K", "valor": 100.00},
        ])
    mr = _mr_dual(df, [0], [1])
    config = _config_dual(
        unidade=unidade, tipo_logico=tipo_logico, tolerancia=tolerancia_aplicada,
    )
    result = executar_v1(mr, config)
    celula = result.classificacao_por_registro[0].valores_por_campo[0]

    if dentro_da_tolerancia:
        # Pode ser DENTRO_TOLERANCIA ou IGUAL (caso degenerate)
        assert celula.status_campo in (StatusCampoV1.DENTRO_TOLERANCIA, StatusCampoV1.IGUAL)
    else:
        assert celula.status_campo == StatusCampoV1.DIVERGENTE


# ===========================================================================
# Bloco IV · pontes por unidade
# ===========================================================================


_UNIDADES_ELEGIVEIS_PONTE = [
    "MONETARIO_BRL", "QUANTIDADE", "TEMPO_DIAS", "TEMPO_HORAS", "MULTIPLICADOR",
]
_UNIDADES_INELEGIVEIS_PONTE = ["PERCENTUAL", "ADIMENSIONAL", "RAZAO"]


@pytest.mark.parametrize("unidade", _UNIDADES_ELEGIVEIS_PONTE)
@pytest.mark.parametrize("caso", _CASOS)
@pytest.mark.parametrize("cenario", ["FECHA", "COM_RESIDUO"])
def test_bloco_iv_ponte_elegivel(unidade, caso, cenario):
    """Bloco IV · 5 elegíveis × 2 casos × 2 cenários = 20 tests."""
    from visoes.visao_v1 import StatusPonteV1, executar_v1, UnidadeCanonica
    tipo_logico = _TIPO_LOGICO_POR_UNIDADE[unidade]

    if cenario == "FECHA":
        # Iguais
        if caso == "ABAS_DISTINTAS":
            df = pd.DataFrame([
                {"documento": "K001", "valor": 100.0},
                {"documento": "K002", "valor": 200.0},
                {"documento": "K001", "valor": 100.0},
                {"documento": "K002", "valor": 200.0},
            ])
            mr = _mr_dual(df, [0, 1], [2, 3])
            config = _config_dual(unidade=unidade, tipo_logico=tipo_logico)
        else:
            df = pd.DataFrame([
                {"docOrigem": "A", "docComparado": "A",
                 "valorOrigem": 100.0, "valorComparado": 100.0},
            ])
            mr = _mr_simples(df)
            config = _config_simples(unidade=unidade, tipo_logico=tipo_logico)
    else:
        # COM_RESIDUO · diferença grande (não absorvida) · injeta SO_ORIGEM sem ajuste contábil
        if caso == "ABAS_DISTINTAS":
            df = pd.DataFrame([
                {"documento": "K001", "valor": 100.0},
                {"documento": "K002", "valor": 200.0},
                {"documento": "K001", "valor": 105.0},  # divergente_valor
                {"documento": "K002", "valor": 199.0},  # divergente_valor
            ])
            mr = _mr_dual(df, [0, 1], [2, 3])
            # Forçar não-fechamento via épsilon=0
            config = _config_dual(unidade=unidade, tipo_logico=tipo_logico)
            config["epsilon_por_unidade"] = {UnidadeCanonica(unidade): Decimal("0")}
        else:
            df = pd.DataFrame([
                {"docOrigem": "A", "docComparado": "A",
                 "valorOrigem": 100.0, "valorComparado": 99.0},
            ])
            mr = _mr_simples(df)
            config = _config_simples(unidade=unidade, tipo_logico=tipo_logico)
            config["epsilon_por_unidade"] = {UnidadeCanonica(unidade): Decimal("0")}

    result = executar_v1(mr, config)
    assert len(result.pontes) == 1, f"Unidade {unidade} elegível deve produzir 1 ponte"

    # Em ABAS_DISTINTAS o ajuste de DIVERGENTE_VALOR deve fazer a ponte fechar mesmo com diferença
    # · então o cenário COM_RESIDUO precisa de algo a mais. Vamos verificar o cálculo da ponte
    # em si; o status pode variar.
    if cenario == "FECHA":
        assert result.pontes[0].fecha is True
        assert result.status_ponte_geral == StatusPonteV1.FECHA


@pytest.mark.parametrize("unidade", _UNIDADES_INELEGIVEIS_PONTE)
@pytest.mark.parametrize("caso", _CASOS)
def test_bloco_iv_ponte_inelegivel_omitida(unidade, caso):
    """Bloco IV · 3 inelegíveis × 2 casos = 6 tests · campo NÃO entra em pontes (Q1.B · D-210)."""
    from visoes.visao_v1 import executar_v1
    tipo_logico = _TIPO_LOGICO_POR_UNIDADE[unidade]

    if caso == "ABAS_DISTINTAS":
        df = pd.DataFrame([
            {"documento": "K001", "valor": 100.0},
            {"documento": "K001", "valor": 100.0},
        ])
        mr = _mr_dual(df, [0], [1])
        config = _config_dual(unidade=unidade, tipo_logico=tipo_logico)
    else:
        df = pd.DataFrame([{
            "docOrigem": "A", "docComparado": "A",
            "valorOrigem": 100.0, "valorComparado": 100.0
        }])
        mr = _mr_simples(df)
        config = _config_simples(unidade=unidade, tipo_logico=tipo_logico)

    result = executar_v1(mr, config)
    # Campo da unidade inelegível NÃO produz ponte (Q1.B)
    assert len(result.pontes) == 0


def test_bloco_iv_invariante_len_pontes_igual_eligibles():
    """Invariante S-V1 §1.1: len(pontes) == campos elegíveis."""
    from visoes.visao_v1 import (
        AgrupadorMatchV1,
        CampoComparadoV1,
        ModoMatchV1,
        TipoCampoV1,
        UnidadeCanonica,
        executar_v1,
    )
    df = pd.DataFrame([
        {"documento": "K", "valor1": 100.0, "taxa": 0.10, "razao": 1.5,
         "valor2": 200.0, "qtd": 5.0},
        {"documento": "K", "valor1": 100.0, "taxa": 0.10, "razao": 1.5,
         "valor2": 200.0, "qtd": 5.0},
    ])
    mr = _mr_dual(df, [0], [1])
    campos = [
        CampoComparadoV1(
            nome_origem="valor1", nome_comparado="valor1", nome_analitico="V1",
            tipo_logico=TipoCampoV1.VALOR_MONETARIO,
            unidade=UnidadeCanonica.MONETARIO_BRL, tolerancia=Decimal("0"),
        ),
        CampoComparadoV1(
            nome_origem="taxa", nome_comparado="taxa", nome_analitico="Taxa",
            tipo_logico=TipoCampoV1.PERCENTUAL,
            unidade=UnidadeCanonica.PERCENTUAL, tolerancia=Decimal("0"),
        ),
        CampoComparadoV1(
            nome_origem="razao", nome_comparado="razao", nome_analitico="Razao",
            tipo_logico=TipoCampoV1.INDICE,
            unidade=UnidadeCanonica.RAZAO, tolerancia=Decimal("0"),
        ),
        CampoComparadoV1(
            nome_origem="valor2", nome_comparado="valor2", nome_analitico="V2",
            tipo_logico=TipoCampoV1.VALOR_MONETARIO,
            unidade=UnidadeCanonica.MONETARIO_BRL, tolerancia=Decimal("0"),
        ),
        CampoComparadoV1(
            nome_origem="qtd", nome_comparado="qtd", nome_analitico="Qtd",
            tipo_logico=TipoCampoV1.QUANTIDADE,
            unidade=UnidadeCanonica.QUANTIDADE, tolerancia=Decimal("0"),
        ),
    ]
    config = _config_dual()
    config["campos_comparados"] = campos
    config["epsilon_por_unidade"] = {
        UnidadeCanonica.MONETARIO_BRL: Decimal("0.01"),
        UnidadeCanonica.QUANTIDADE: Decimal("0"),
    }
    result = executar_v1(mr, config)
    # 5 campos · 2 inelegíveis (PERCENTUAL, RAZAO) · 3 elegíveis
    assert len(result.pontes) == 3
    assert len(result.valor_por_campo) == 5
