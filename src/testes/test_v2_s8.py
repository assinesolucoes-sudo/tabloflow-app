"""
test_v2_s8.py — Suite Sessão 8 · ALINHA-Descoberta-Unidade · 5 evoluções V2.

Cobre:
  - E1 · Campo `unidade` em ComparacaoV2 + defaults inferidos · helpers de despacho
  - E2 · Saúde da comparação (delta_por_classificacao_semantica)
  - E3a · Concentração (top_5_pct · top_10_pct · interpretacao)
  - E3b · Onde se concentra (top 3 + outras)
  - E3c · Leitura qualitativa parametrizada
  - Integração via executar_v2 com bases sintéticas para cada unidade canônica
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import pytest

_SRC = Path(__file__).parent.parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from contratos import (
    ColumnMeta,
    MotorResult,
    TipoEstruturalEnum,
    TipoSemanticoEnum,
    TipoTecnicoEnum,
)
from apresentacao.formatos import (
    FORMATO_CONTAGEM,
    FORMATO_MONETARIO_BR,
    FORMATO_PERCENTUAL,
    formatar_valor_por_unidade,
    label_total_card,
    number_format_diferenca,
    number_format_valor,
    number_format_variacao,
    rotulo_diferenca,
    rotulo_variacao,
    valor_total_card,
)
from visoes.exportacao_v2 import (
    _construir_leitura_qualitativa_v2,
    _resolver_number_format,
)
from apresentacao.formatos import default_unidade_para_tipo_campo as _default_unidade_para_tipo
from visoes.visao_v2 import (
    ComparacaoV2,
    V2Result,
    _resolver_agrupador_destacado,
    executar_v2,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _col_meta(nome: str, tipo_tecnico: str = "float", tipo_estrutural: str = "NUMERICO_CONTINUO") -> ColumnMeta:
    return ColumnMeta(
        nome=nome,
        tipo_tecnico=TipoTecnicoEnum(tipo_tecnico),
        tipo_semantico=(
            TipoSemanticoEnum("numeric")
            if tipo_estrutural == "NUMERICO_CONTINUO"
            else TipoSemanticoEnum("categorico_baixa_card")
        ),
        tipo_estrutural=TipoEstruturalEnum(tipo_estrutural),
        subtipo_id_detectado=False,
        null_count=0,
        cardinalidade=10,
        eh_candidato_categorico=tipo_estrutural == "CATEGORICO_ELEGIVEL",
        padrao_cronologico_detectado=None,
        ordem_insercao=0,
    )


def _motor_result(df: pd.DataFrame) -> MotorResult:
    col_meta = {}
    for i, col in enumerate(df.columns):
        if pd.api.types.is_numeric_dtype(df[col]):
            meta = _col_meta(col, "float", "NUMERICO_CONTINUO")
        else:
            meta = _col_meta(col, "string", "CATEGORICO_ELEGIVEL")
        meta = meta.model_copy(update={
            "nome": col, "ordem_insercao": i,
            "null_count": int(df[col].isna().sum()),
            "cardinalidade": int(df[col].nunique()),
        })
        col_meta[col] = meta
    return MotorResult(
        df=df,
        column_meta=col_meta,
        modo_upload="SIMPLES",
        total_linhas_originais=len(df),
        total_linhas_processadas=len(df),
    )


def _config_por_colunas(
    campo: str,
    unidade: str = "MONETARIO_BRL",
    semantica: str = "MAIOR_MELHOR",
    agrupadores: Optional[List[str]] = None,
    agrupador_destacado: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "estrutura_entrada": "POR_COLUNAS",
        "origem_rotulo_tecnico": "Origem",
        "comparado_rotulo_tecnico": "Comparado",
        "origem_rotulo_ux": "Janeiro",
        "comparado_rotulo_ux": "Fevereiro",
        "coluna_discriminadora": None,
        "modo_4_ativado": False,
        "estados_nao_escolhidos": [],
        "campo_analisado": campo,
        "tipo_campo": "NUMERICO_ADITIVO",
        "semantica_campo": semantica,
        "unidade": unidade,
        "regra_agregacao": "SOMA",
        "metodo_consolidacao_relativo": None,
        "campo_peso": None,
        "modo_pre_agregado": False,
        "agrupadores": agrupadores or ["Categoria"],
        "agrupador_destacado": agrupador_destacado,
        "resolucao_estrutural": None,
        "thresholds": {
            "limiar_estabilidade_pct": 0.01,
            "limiar_nulo_massivo_pct": 0.20,
            "limite_valores_discriminador_alerta": 50,
            "limite_variacao_extrema_pct": 10.0,
        },
        "modelo_aplicado": None,
    }


def _df_por_colunas(linhas: int = 12) -> pd.DataFrame:
    """Base sintética POR_COLUNAS · 1 categoria 1 ano."""
    cats = ["A", "B", "C", "D"][: max(2, min(4, linhas // 3))]
    rows = []
    for i in range(linhas):
        cat = cats[i % len(cats)]
        rows.append({
            "Categoria": cat,
            "Origem": float(100 + i * 17),
            "Comparado": float(110 + i * 19),
        })
    return pd.DataFrame(rows)


# ===========================================================================
# E1 · Defaults declarados de unidade
# ===========================================================================


def test_e1_default_unidade_aditivo_eh_monetario():
    assert _default_unidade_para_tipo("NUMERICO_ADITIVO") == "MONETARIO_BRL"


def test_e1_default_unidade_relativo_eh_percentual():
    assert _default_unidade_para_tipo("NUMERICO_RELATIVO") == "PERCENTUAL"


def test_e1_default_unidade_estado_eh_adimensional():
    assert _default_unidade_para_tipo("ESTADO_SITUACAO") == "ADIMENSIONAL"


def test_e1_default_unidade_nao_aditivo_eh_monetario():
    assert _default_unidade_para_tipo("NUMERICO_NAO_ADITIVO") == "MONETARIO_BRL"


# ===========================================================================
# E1 · Tabela canônica de formatos por unidade
# ===========================================================================


@pytest.mark.parametrize("unidade,esperado", [
    ("MONETARIO_BRL", FORMATO_MONETARIO_BR),
    ("PERCENTUAL", FORMATO_PERCENTUAL),
    ("QUANTIDADE", FORMATO_CONTAGEM),
])
def test_e1_number_format_valor(unidade, esperado):
    assert number_format_valor(unidade) == esperado


def test_e1_number_format_diferenca_percentual_tem_sinal_explicito():
    # Sessão 8.1 · C-1: formato 'p.p' literal (não % nativo do Excel) para
    # alinhar com cabeçalho "Variação absoluta (p.p)". Caller deve aplicar
    # `valor_diferenca_para_celula` ao valor cru antes da escrita.
    fmt = number_format_diferenca("PERCENTUAL")
    assert fmt.startswith("+")  # explicit positive sign
    assert "p.p" in fmt


def test_e1_number_format_diferenca_monetario_preserva_legado():
    """Garante zero regressão para bases monetárias."""
    assert number_format_diferenca("MONETARIO_BRL") == FORMATO_MONETARIO_BR


def test_e1_number_format_variacao_sempre_percentual():
    for unidade in (
        "MONETARIO_BRL", "PERCENTUAL", "QUANTIDADE",
        "TEMPO_DIAS", "TEMPO_HORAS", "MULTIPLICADOR", "RAZAO", "ADIMENSIONAL",
    ):
        assert "%" in number_format_variacao(unidade)


def test_e1_rotulo_diferenca_percentual_diz_pp():
    assert "p.p" in rotulo_diferenca("PERCENTUAL")


def test_e1_rotulo_diferenca_monetario_padrao():
    assert rotulo_diferenca("MONETARIO_BRL") == "Diferença"


def test_e1_rotulo_diferenca_tempo_dias_inclui_unidade():
    assert "dias" in rotulo_diferenca("TEMPO_DIAS")


def test_e1_rotulo_variacao_percentual_explicita_relativa():
    rot = rotulo_variacao("PERCENTUAL")
    assert "relativa" in rot.lower()


def test_e1_label_total_card_percentual_eh_media():
    assert label_total_card("PERCENTUAL") == "Média"


def test_e1_label_total_card_demais_eh_total():
    for unidade in ("MONETARIO_BRL", "QUANTIDADE", "TEMPO_DIAS", "ADIMENSIONAL"):
        assert label_total_card(unidade) == "Total"


def test_e1_valor_total_card_percentual_divide_por_count():
    soma = 7.5  # somatório de 5 frações 1.5 cada (total 7.5)
    media = valor_total_card(soma, count_presente=5, unidade="PERCENTUAL")
    assert media == pytest.approx(1.5)


def test_e1_valor_total_card_monetario_preserva_soma():
    soma = 1500.0
    total = valor_total_card(soma, count_presente=5, unidade="MONETARIO_BRL")
    assert total == 1500.0


def test_e1_valor_total_card_none_retorna_none():
    assert valor_total_card(None, 5, "MONETARIO_BRL") is None


def test_e1_formatar_valor_por_unidade_monetario_string_br():
    assert formatar_valor_por_unidade(1234.5, "MONETARIO_BRL") == "R$ 1.234,50"


def test_e1_formatar_valor_por_unidade_quantidade_inteiro_br():
    assert formatar_valor_por_unidade(1234.5, "QUANTIDADE") == "1.234"


def test_e1_formatar_valor_por_unidade_tempo_horas():
    assert "h" in formatar_valor_por_unidade(36.0, "TEMPO_HORAS")


def test_e1_resolver_number_format_tags_adaptativas():
    # tag "valor" + unidade percentual → formato percentual
    assert _resolver_number_format("valor", "PERCENTUAL") == FORMATO_PERCENTUAL
    # tag "valor" + unidade monetária → formato monetário
    assert _resolver_number_format("valor", "MONETARIO_BRL") == FORMATO_MONETARIO_BR
    # tag "diferenca" + percentual → formato 'p.p' literal com sinal explícito
    # (Sessão 8.1 · C-1: literal substitui % nativo do Excel · valor é
    # pré-multiplicado por 100 pelo caller via `valor_diferenca_para_celula`)
    fmt = _resolver_number_format("diferenca", "PERCENTUAL")
    assert fmt is not None and "p.p" in fmt and fmt.startswith("+")


def test_e1_resolver_number_format_tags_legadas_preservadas():
    """Tags antigas continuam funcionando · zero regressão."""
    assert _resolver_number_format("monetario", "ADIMENSIONAL") == FORMATO_MONETARIO_BR
    assert _resolver_number_format("percentual", "ADIMENSIONAL") == FORMATO_PERCENTUAL
    assert _resolver_number_format("contagem", "ADIMENSIONAL") == FORMATO_CONTAGEM


def test_e1_resolver_number_format_tags_sem_formato():
    assert _resolver_number_format("texto", "MONETARIO_BRL") is None
    assert _resolver_number_format("classificacao", "MONETARIO_BRL") is None


# ===========================================================================
# E1 · Contrato ComparacaoV2 com unidade
# ===========================================================================


def test_e1_comparacao_v2_default_unidade_monetario_brl():
    comp = ComparacaoV2(
        estrutura_entrada="POR_COLUNAS",
        origem_rotulo_tecnico="A", comparado_rotulo_tecnico="B",
        origem_rotulo_ux="A", comparado_rotulo_ux="B",
        campo_analisado="X", tipo_campo="NUMERICO_ADITIVO",
        semantica_campo="MAIOR_MELHOR",
    )
    assert comp.unidade == "MONETARIO_BRL"


def test_e1_comparacao_v2_aceita_todas_unidades():
    for unidade in (
        "MONETARIO_BRL", "PERCENTUAL", "QUANTIDADE", "TEMPO_DIAS",
        "TEMPO_HORAS", "MULTIPLICADOR", "RAZAO", "ADIMENSIONAL",
    ):
        comp = ComparacaoV2(
            estrutura_entrada="POR_COLUNAS",
            origem_rotulo_tecnico="A", comparado_rotulo_tecnico="B",
            origem_rotulo_ux="A", comparado_rotulo_ux="B",
            campo_analisado="X", tipo_campo="NUMERICO_ADITIVO",
            semantica_campo="MAIOR_MELHOR", unidade=unidade,
        )
        assert comp.unidade == unidade


def test_e1_comparacao_v2_rejeita_unidade_invalida():
    with pytest.raises(Exception):
        ComparacaoV2(
            estrutura_entrada="POR_COLUNAS",
            origem_rotulo_tecnico="A", comparado_rotulo_tecnico="B",
            origem_rotulo_ux="A", comparado_rotulo_ux="B",
            campo_analisado="X", tipo_campo="NUMERICO_ADITIVO",
            semantica_campo="MAIOR_MELHOR", unidade="GIGAWATTS",
        )


def test_e1_comparacao_v2_default_agrupador_destacado_none():
    comp = ComparacaoV2(
        estrutura_entrada="POR_COLUNAS",
        origem_rotulo_tecnico="A", comparado_rotulo_tecnico="B",
        origem_rotulo_ux="A", comparado_rotulo_ux="B",
        campo_analisado="X", tipo_campo="NUMERICO_ADITIVO",
        semantica_campo="MAIOR_MELHOR",
    )
    assert comp.agrupador_destacado is None


# ===========================================================================
# E3b · Resolução de agrupador destacado
# ===========================================================================


def test_e3b_resolver_agrupador_destacado_default_eh_primeiro():
    config = {"agrupador_destacado": None}
    assert _resolver_agrupador_destacado(["A", "B", "C"], config) == "A"


def test_e3b_resolver_agrupador_destacado_preserva_se_valido():
    config = {"agrupador_destacado": "B"}
    assert _resolver_agrupador_destacado(["A", "B", "C"], config) == "B"


def test_e3b_resolver_agrupador_destacado_fallback_se_invalido():
    config = {"agrupador_destacado": "Z"}
    assert _resolver_agrupador_destacado(["A", "B"], config) == "A"


def test_e3b_resolver_agrupador_destacado_lista_vazia_eh_none():
    assert _resolver_agrupador_destacado([], {}) is None


# ===========================================================================
# Integração · executar_v2 produz novos campos do V2Result
# ===========================================================================


def test_int_executar_v2_monetario_preserva_legado():
    df = _df_por_colunas(linhas=12)
    config = _config_por_colunas("Receita", unidade="MONETARIO_BRL")
    v2 = executar_v2(_motor_result(df), config)
    assert v2.comparacao_realizada.unidade == "MONETARIO_BRL"
    assert v2.delta_por_classificacao_semantica is not None
    # 7 chaves canônicas D-187
    assert set(v2.delta_por_classificacao_semantica.keys()) == {
        "POSITIVO", "NEGATIVO", "NEUTRO", "NAO_APLICAVEL",
        "AUMENTOU", "REDUZIU", "ESTAVEL",
    }


def test_int_executar_v2_percentual_unidade_propaga():
    df = _df_por_colunas(linhas=12)
    config = _config_por_colunas("Margem", unidade="PERCENTUAL")
    v2 = executar_v2(_motor_result(df), config)
    assert v2.comparacao_realizada.unidade == "PERCENTUAL"


def test_int_executar_v2_quantidade_unidade_propaga():
    df = _df_por_colunas(linhas=12)
    config = _config_por_colunas("Volume", unidade="QUANTIDADE")
    v2 = executar_v2(_motor_result(df), config)
    assert v2.comparacao_realizada.unidade == "QUANTIDADE"


def test_int_executar_v2_estado_unidade_eh_adimensional():
    """Tipo ESTADO_SITUACAO deve aceitar `unidade=ADIMENSIONAL` no contrato."""
    df = pd.DataFrame({
        "Categoria": ["A", "B", "C", "D", "A", "B"],
        "Estado_Origem": ["OK", "OK", "FAIL", "OK", "FAIL", "OK"],
        "Estado_Comparado": ["OK", "FAIL", "FAIL", "OK", "OK", "OK"],
    })
    cfg = _config_por_colunas("Estado", unidade="ADIMENSIONAL")
    cfg["tipo_campo"] = "ESTADO_SITUACAO"
    cfg["semantica_campo"] = "NEUTRO"
    cfg["origem_rotulo_tecnico"] = "Estado_Origem"
    cfg["comparado_rotulo_tecnico"] = "Estado_Comparado"
    cfg["agrupadores"] = ["Categoria"]
    cfg["regra_agregacao"] = "CONTAGEM"
    v2 = executar_v2(_motor_result(df), cfg)
    assert v2.comparacao_realizada.unidade == "ADIMENSIONAL"


# ===========================================================================
# E2 · Saúde da comparação · delta por classificacao_semantica
# ===========================================================================


def test_e2_delta_por_classificacao_semantica_e_distribuicao_consistentes():
    df = _df_por_colunas(linhas=12)
    config = _config_por_colunas("Receita")
    v2 = executar_v2(_motor_result(df), config)
    dist = v2.distribuicao_classificacoes_semanticas or {}
    delta = v2.delta_por_classificacao_semantica or {}
    # quando dist[k] = 0, delta[k] também deve ser 0
    for k, n in dist.items():
        if n == 0:
            assert delta.get(k, 0) == 0.0


def test_e2_delta_por_classificacao_estado_situacao_eh_none():
    df = pd.DataFrame({
        "Categoria": ["A", "B"],
        "Estado_Origem": ["OK", "FAIL"],
        "Estado_Comparado": ["OK", "OK"],
    })
    cfg = _config_por_colunas("Estado", unidade="ADIMENSIONAL")
    cfg["tipo_campo"] = "ESTADO_SITUACAO"
    cfg["semantica_campo"] = "NEUTRO"
    cfg["origem_rotulo_tecnico"] = "Estado_Origem"
    cfg["comparado_rotulo_tecnico"] = "Estado_Comparado"
    cfg["regra_agregacao"] = "CONTAGEM"
    v2 = executar_v2(_motor_result(df), cfg)
    assert v2.delta_por_classificacao_semantica is None


# ===========================================================================
# E3a · Concentração
# ===========================================================================


def test_e3a_concentracao_oculta_quando_menos_que_5_pa():
    df = _df_por_colunas(linhas=4)  # menos que 5 PRESENTE_AMBOS
    config = _config_por_colunas("Receita")
    v2 = executar_v2(_motor_result(df), config)
    assert v2.concentracao is None


def test_e3a_concentracao_alta_top5_acima_80pct():
    """Outliers gigantes · top5 deve representar a maior parte do impacto."""
    rows = []
    for i in range(20):
        rows.append({"Categoria": f"K{i % 4}", "Origem": 100.0, "Comparado": 100.5})
    # 5 outliers com diferenças massivas
    for i in range(5):
        rows.append({"Categoria": "BIG", "Origem": 100.0, "Comparado": 10000.0})
    df = pd.DataFrame(rows)
    config = _config_por_colunas("Receita", agrupadores=["Categoria"])
    v2 = executar_v2(_motor_result(df), config)
    assert v2.concentracao is not None
    assert v2.concentracao["interpretacao"] == "alta"
    assert v2.concentracao["top_5_pct"] >= 0.80


def test_e3a_concentracao_distribuida_quando_paritaria():
    """20 linhas com diferenças similares · distribuição uniforme."""
    rows = []
    for i in range(20):
        rows.append({"Categoria": f"K{i}", "Origem": 100.0, "Comparado": 110.0 + i * 0.1})
    df = pd.DataFrame(rows)
    config = _config_por_colunas("Receita", agrupadores=["Categoria"])
    v2 = executar_v2(_motor_result(df), config)
    assert v2.concentracao is not None
    assert v2.concentracao["interpretacao"] == "distribuida"


def test_e3a_concentracao_estado_situacao_eh_none():
    df = pd.DataFrame({
        "Categoria": ["A", "B"],
        "Estado_Origem": ["OK", "FAIL"],
        "Estado_Comparado": ["OK", "OK"],
    })
    cfg = _config_por_colunas("Estado", unidade="ADIMENSIONAL")
    cfg["tipo_campo"] = "ESTADO_SITUACAO"
    cfg["semantica_campo"] = "NEUTRO"
    cfg["origem_rotulo_tecnico"] = "Estado_Origem"
    cfg["comparado_rotulo_tecnico"] = "Estado_Comparado"
    cfg["regra_agregacao"] = "CONTAGEM"
    v2 = executar_v2(_motor_result(df), cfg)
    assert v2.concentracao is None


# ===========================================================================
# E3b · Onde se concentra · top 3
# ===========================================================================


def test_e3b_onde_se_concentra_default_primeiro_agrupador():
    df = _df_por_colunas(linhas=12)
    config = _config_por_colunas("Receita", agrupadores=["Categoria"])
    v2 = executar_v2(_motor_result(df), config)
    assert v2.onde_se_concentra is not None
    assert v2.onde_se_concentra["agrupador"] == "Categoria"


def test_e3b_onde_se_concentra_top_3_ordenado_por_abs_delta():
    rows = []
    for i in range(40):
        cat = f"K{i % 5}"
        rows.append({"Categoria": cat, "Origem": 100.0, "Comparado": 100.0 + (i % 5) * 50})
    df = pd.DataFrame(rows)
    config = _config_por_colunas("Receita", agrupadores=["Categoria"])
    v2 = executar_v2(_motor_result(df), config)
    osc = v2.onde_se_concentra
    assert osc is not None
    # top deve ter no máximo 3 itens
    assert len(osc["top"]) <= 3
    # ordem decrescente em |delta|
    deltas = [abs(t["delta"]) for t in osc["top"]]
    assert deltas == sorted(deltas, reverse=True)


def test_e3b_onde_se_concentra_outras_count_correto():
    """5 categorias · top 3 + 2 outras."""
    rows = []
    for i in range(20):
        cat = f"K{i % 5}"
        rows.append({"Categoria": cat, "Origem": 100.0, "Comparado": 100.0 + (i % 5) * 10})
    df = pd.DataFrame(rows)
    config = _config_por_colunas("Receita", agrupadores=["Categoria"])
    v2 = executar_v2(_motor_result(df), config)
    osc = v2.onde_se_concentra
    assert osc["outras_count"] == 2


def test_e3b_onde_se_concentra_estado_situacao_eh_none():
    df = pd.DataFrame({
        "Categoria": ["A", "B"],
        "Estado_Origem": ["OK", "FAIL"],
        "Estado_Comparado": ["OK", "OK"],
    })
    cfg = _config_por_colunas("Estado", unidade="ADIMENSIONAL")
    cfg["tipo_campo"] = "ESTADO_SITUACAO"
    cfg["semantica_campo"] = "NEUTRO"
    cfg["origem_rotulo_tecnico"] = "Estado_Origem"
    cfg["comparado_rotulo_tecnico"] = "Estado_Comparado"
    cfg["regra_agregacao"] = "CONTAGEM"
    v2 = executar_v2(_motor_result(df), cfg)
    assert v2.onde_se_concentra is None


def test_e3b_onde_se_concentra_agrupador_destacado_explicito():
    df = _df_por_colunas(linhas=12)
    df["Loja"] = ["X", "Y", "Z"] * 4
    config = _config_por_colunas(
        "Receita",
        agrupadores=["Categoria", "Loja"],
        agrupador_destacado="Loja",
    )
    v2 = executar_v2(_motor_result(df), config)
    assert v2.onde_se_concentra["agrupador"] == "Loja"


# ===========================================================================
# E3c · Leitura qualitativa parametrizada
# ===========================================================================


def test_e3c_leitura_qualitativa_inclui_origem_e_comparado_ux():
    df = _df_por_colunas(linhas=12)
    config = _config_por_colunas("Receita")
    v2 = executar_v2(_motor_result(df), config)
    texto = _construir_leitura_qualitativa_v2(v2, "Janeiro", "Fevereiro")
    assert "Janeiro" in texto or "Fevereiro" in texto


def test_e3c_leitura_qualitativa_estado_situacao_template_separado():
    df = pd.DataFrame({
        "Categoria": ["A", "B", "C", "D"],
        "Estado_Origem": ["OK", "OK", "FAIL", "OK"],
        "Estado_Comparado": ["OK", "FAIL", "FAIL", "OK"],
    })
    cfg = _config_por_colunas("Estado", unidade="ADIMENSIONAL")
    cfg["tipo_campo"] = "ESTADO_SITUACAO"
    cfg["semantica_campo"] = "NEUTRO"
    cfg["origem_rotulo_tecnico"] = "Estado_Origem"
    cfg["comparado_rotulo_tecnico"] = "Estado_Comparado"
    cfg["regra_agregacao"] = "CONTAGEM"
    v2 = executar_v2(_motor_result(df), cfg)
    texto = _construir_leitura_qualitativa_v2(v2, "Janeiro", "Fevereiro")
    # Template ESTADO_SITUACAO menciona estado/mudaram/estável
    assert any(p in texto.lower() for p in ("mudaram", "estável", "permaneceram"))


def test_e3c_leitura_qualitativa_termina_em_ponto():
    df = _df_por_colunas(linhas=12)
    config = _config_por_colunas("Receita")
    v2 = executar_v2(_motor_result(df), config)
    texto = _construir_leitura_qualitativa_v2(v2, "A", "B")
    assert texto.rstrip().endswith(".")


# ===========================================================================
# Integração E2E · Excel exportável para 3 unidades canônicas
# ===========================================================================


def _exportar_smoke(unidade: str, sufixo: str) -> Path:
    from visoes.exportacao_v2 import exportar_resultado_v2
    df = _df_por_colunas(linhas=12)
    config = _config_por_colunas("Receita", unidade=unidade)
    v2 = executar_v2(_motor_result(df), config)
    saida = Path(__file__).parent / "outputs" / f"_smoke_s8_{sufixo}.xlsx"
    saida.parent.mkdir(parents=True, exist_ok=True)
    res = exportar_resultado_v2(v2, str(saida), paleta_nome="azul")
    assert Path(res.caminho_arquivo).exists()
    assert res.tamanho_bytes > 0
    return Path(res.caminho_arquivo)


def test_int_excel_exportavel_monetario():
    _exportar_smoke("MONETARIO_BRL", "monetario")


def test_int_excel_exportavel_percentual():
    _exportar_smoke("PERCENTUAL", "percentual")


def test_int_excel_exportavel_quantidade():
    _exportar_smoke("QUANTIDADE", "quantidade")


def test_int_excel_exportavel_tempo_dias():
    _exportar_smoke("TEMPO_DIAS", "tempo_dias")


def test_int_excel_exportavel_multiplicador():
    _exportar_smoke("MULTIPLICADOR", "multiplicador")
