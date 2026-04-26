"""
app_v2.py — V2 · Análise Comparativa entre Referências · Streamlit
Bloco A-V2 · 4º artefato do ciclo §15.1 (Fase 2).

Orquestra a sequência canônica:
    motor_upload.processar_upload  →  motor_base.processar_base  →  executar_v2  →  exportar_resultado

O app NUNCA calcula · NUNCA infere classificação estrutural / semântica / warnings.
Toda leitura analítica vem de V2Result (C.3). Gate B.4 · checklist 4/4 habilita download.
"""
from __future__ import annotations

import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Path setup (permite execução via `streamlit run src/app_v2.py`)
# ---------------------------------------------------------------------------
_SRC_DIR = Path(__file__).resolve().parent
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from contratos import BloqueioOperacional, MotorResult, UploadResult
from exportacao import exportar_resultado
from motor_base import processar_base
from motor_upload import ArquivoEntrada, processar_upload
from apresentacao.formatos import (
    default_unidade_para_tipo_campo,
    formatar_diferenca_por_unidade,
    formatar_percentual_br,
    formatar_valor_por_unidade,
    label_total_card,
    rotulo_diferenca,
    rotulo_variacao,
    valor_total_card,
)
from visoes.exportacao_v2 import (
    _LABEL_SEMANTICA_SAUDE,
    _categorias_saude_para_exibir,
    exportar_resultado_v2,
)
from visoes.visao_v2 import (
    V2Result,
    _classificar_patamar_agrupadores,
    executar_v2,
)

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

# Stepper user-facing "4 etapas + Revisão" · D-167 · vocabulario_bilingue v2 Bloco 1
ETAPAS_STEPPER = [
    "1 · Escolher arquivo",
    "2 · Reconhecer estrutura",
    "3 · Configurar análise",
    "4 · Agrupar",
    "Revisar e executar",
]

ETAPA_ORDEM = ["vazio", "E1_OK", "E2", "E3", "E4", "RESOL_CASO", "E5",
               "PROCESSANDO", "RESULTADO", "CHECKLIST", "ERRO"]

# Tipos de campo · user-facing via P-V2 §2.5 (microcopy contextual de seleção)
TIPOS_CAMPO = [
    ("NUMERICO_ADITIVO", "Valor somável (receita, custo, quantidade, volume)"),
    ("NUMERICO_RELATIVO", "Valor percentual ou taxa (margem %, taxa, índice)"),
    ("NUMERICO_NAO_ADITIVO", "Indicador não somável (saldo, estoque, preço unitário)"),
    ("ESTADO_SITUACAO", "Categoria ou rótulo (status, classificação)"),
]

SEMANTICAS = [
    ("MAIOR_MELHOR", "Subir é bom (maior é melhor)"),
    ("MENOR_MELHOR", "Subir é ruim (menor é melhor)"),
    ("NEUTRO", "Neutro · sem viés"),
]

# Unidades canônicas · D-190 · C.D8 · default por tipo derivado em E3
UNIDADES = [
    ("MONETARIO_BRL", "Reais (R$)"),
    ("PERCENTUAL",    "Percentual (%)"),
    ("QUANTIDADE",    "Quantidade absoluta"),
    ("TEMPO_DIAS",    "Tempo em dias"),
    ("TEMPO_HORAS",   "Tempo em horas"),
    ("MULTIPLICADOR", "Multiplicador (x)"),
    ("RAZAO",         "Razão (decimal)"),
    ("ADIMENSIONAL",  "Outro / sem unidade definida"),
]


REGRAS_AGREGACAO = ["SOMA", "MEDIA", "MAXIMO", "MINIMO", "CONTAGEM"]
REGRAS_LABELS = {
    "SOMA": "Soma",
    "MEDIA": "Média",
    "MAXIMO": "Máximo",
    "MINIMO": "Mínimo",
    "CONTAGEM": "Contagem",
}

METODOS_CONSOLIDACAO = [
    ("MEDIA_SIMPLES", "Média simples"),
    ("MEDIA_PONDERADA", "Média ponderada (exige campo de peso)"),
    ("NAO_CONSOLIDAR", "Não consolidar (exige base sem agrupadores)"),
]

# Paleta executiva · P-V2 §1.1 · D-168 · default universal Azul · ordem fixa
PALETAS_DISPONIVEIS = ["Azul", "Cinza", "Verde", "Vinho"]
PALETA_DEFAULT = "Azul"

THRESHOLDS_DEFAULT = {
    "limiar_estabilidade_pct": 0.01,
    "limiar_nulo_massivo_pct": 0.20,
    "limite_valores_discriminador_alerta": 50,
    "limite_variacao_extrema_pct": 10.0,
}

# Chaves de session_state por etapa (tabela §3.10)
CHAVES_E2 = [
    "estrutura_entrada", "coluna_discriminadora",
    "origem_rotulo_tecnico", "comparado_rotulo_tecnico",
    "origem_rotulo_ux", "comparado_rotulo_ux",
    "modo_4_ativado", "estados_nao_escolhidos",
]
CHAVES_E3 = [
    "campo_analisado", "tipo_campo", "semantica_campo", "unidade",
    "metodo_consolidacao_relativo", "campo_peso", "modo_pre_agregado",
    "thresholds_editados",
]
CHAVES_E4 = ["agrupadores", "regra_agregacao", "agrupador_destacado", "confirmacao_p3_agrupadores"]
CHAVES_E5 = ["v2_result", "checklist_marcacoes", "caminho_excel_exportado",
             "caso_estrutural_detectado", "resolucao_estrutural",
             "analise_aprovada", "_hash_config_executada"]

# Textos do checklist (§3.9 · 1:1 com casos_esperados.yaml bloco visoes.V2)
CHECKLIST_ITENS = [
    (
        "item_1",
        "Item 1 (V2-A01 · contagem_categoria) · O resultado mostra entre 2 e 4 "
        "elementos ausentes em um lado em Produto na aba vendas_padrao "
        "(warning associado: W-V2-AUSENTE-EM-UM-LADO)?"
    ),
    (
        "item_2",
        "Item 2 (V2-A02 · warning_presente) · O warning W-NULO-MEDIDA aparece no "
        "Diagnóstico com 3–4 ocorrência(s)?"
    ),
    (
        "item_3",
        "Item 3 (V2-A03 · estrutura_saida) · O Excel tem Resumo Executivo com 6 "
        "blocos e aba Coração Visual nomeada \"Matriz de Confronto\"?"
    ),
    (
        "item_4",
        "Item 4 (V2-A04 · contagem_exata) · O resultado mostra exatamente 2 "
        "estados distintos (2025-01 e 2025-02) em Mes na aba vendas_padrao?"
    ),
]

# ---------------------------------------------------------------------------
# Humanização de nomes técnicos para a superfície (C-5 · Sessão 4-ter-bis)
# ---------------------------------------------------------------------------


def _rotular_agrupador_ui(nome_tec: str) -> str:
    """Humaniza nome de coluna técnica para renderização em tela (Streamlit).

    Aplica o mesmo contrato de `exportacao_v2._rotular_agrupador` na superfície
    do app (headers de st.dataframe, rótulos de eixo, multiselects). Evita que
    nomes como `Centro_Custo` vazem com underscore em tabelas e gráficos.

    TODO-FAPRESENT-CLEANUP: promover para capability 2 (traduzir) ou criar
    capability auxiliar 'rotular_coluna_tecnica' · consumida também pelo
    exportacao_v2 e pelas versões VN futuras. Tabela de especiais bilíngue
    (Centro_Custo, Mes, ...) deve morar no vocabulário canônico F-APRESENT.
    """
    if not nome_tec:
        return ""
    especiais = {
        "Centro_Custo": "Centro de Custo",
        "centro_custo": "Centro de Custo",
        "CENTRO_CUSTO": "Centro de Custo",
        "Mes": "Mês",
        "mes": "Mês",
    }
    if nome_tec in especiais:
        return especiais[nome_tec]
    texto = nome_tec.replace("_", " ").strip()
    if not texto:
        return nome_tec
    return texto[0].upper() + texto[1:]


# ---------------------------------------------------------------------------
# Session state helpers
# ---------------------------------------------------------------------------


def _init_state() -> None:
    defaults: Dict[str, Any] = {
        "etapa": "vazio",
        "nome_arquivo": "",
        "aba_selecionada": "",
        "upload_result": None,
        "motor_result": None,
        "abas_disponiveis": [],
        # E2
        "estrutura_entrada": "POR_COLUNAS",
        "coluna_discriminadora": None,
        "origem_rotulo_tecnico": "",
        "comparado_rotulo_tecnico": "",
        "origem_rotulo_ux": "",
        "comparado_rotulo_ux": "",
        "modo_4_ativado": False,
        "estados_nao_escolhidos": [],
        # E3
        "campo_analisado": "",
        "tipo_campo": "NUMERICO_ADITIVO",
        "semantica_campo": "MAIOR_MELHOR",
        "unidade": "MONETARIO_BRL",
        "metodo_consolidacao_relativo": None,
        "campo_peso": None,
        "modo_pre_agregado": False,
        "thresholds_editados": dict(THRESHOLDS_DEFAULT),
        # TED widget keys (persistem mesmo quando expander colapsado · C.5)
        "ted_estab": float(THRESHOLDS_DEFAULT["limiar_estabilidade_pct"]),
        "ted_null": float(THRESHOLDS_DEFAULT["limiar_nulo_massivo_pct"]),
        "ted_disc": int(THRESHOLDS_DEFAULT["limite_valores_discriminador_alerta"]),
        "ted_var": float(THRESHOLDS_DEFAULT["limite_variacao_extrema_pct"]),
        # E4
        "agrupadores": [],
        "regra_agregacao": "SOMA",
        "agrupador_destacado": None,
        "confirmacao_p3_agrupadores": False,
        # E5 / resultado
        "v2_result": None,
        "checklist_marcacoes": {k: False for k, _ in CHECKLIST_ITENS},
        "caminho_excel_exportado": None,
        "caso_estrutural_detectado": None,
        "resolucao_estrutural": None,
        # Paleta executiva · P-V2 §1.1 · D-168 · default universal Azul
        "paleta_selecionada": PALETA_DEFAULT,
        # Flag de aprovação separada do download · D-162
        "analise_aprovada": False,
        # D-186 · gate de stale na tela RESULTADO · hash dos campos críticos
        # da config no momento da execução · comparado com hash atual em
        # _tela_resultado para detectar mudanças não reprocessadas.
        "_hash_config_executada": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _invalidar_a_partir(etapa_alvo: str) -> None:
    """Zera chaves de etapa_alvo em diante · §3.10 invalidação cascata."""
    ordem = {"E2": 2, "E3": 3, "E4": 4, "E5": 5}
    if etapa_alvo not in ordem:
        return
    n = ordem[etapa_alvo]
    mapa = {2: CHAVES_E2, 3: CHAVES_E3, 4: CHAVES_E4, 5: CHAVES_E5}

    defaults: Dict[str, Any] = {
        "estrutura_entrada": "POR_COLUNAS",
        "coluna_discriminadora": None,
        "origem_rotulo_tecnico": "",
        "comparado_rotulo_tecnico": "",
        "origem_rotulo_ux": "",
        "comparado_rotulo_ux": "",
        "modo_4_ativado": False,
        "estados_nao_escolhidos": [],
        "campo_analisado": "",
        "tipo_campo": "NUMERICO_ADITIVO",
        "semantica_campo": "MAIOR_MELHOR",
        "unidade": "MONETARIO_BRL",
        "metodo_consolidacao_relativo": None,
        "campo_peso": None,
        "modo_pre_agregado": False,
        "thresholds_editados": dict(THRESHOLDS_DEFAULT),
        "agrupadores": [],
        "regra_agregacao": "SOMA",
        "agrupador_destacado": None,
        "confirmacao_p3_agrupadores": False,
        "v2_result": None,
        "checklist_marcacoes": {k: False for k, _ in CHECKLIST_ITENS},
        "caminho_excel_exportado": None,
        "caso_estrutural_detectado": None,
        "resolucao_estrutural": None,
        "analise_aprovada": False,
        "_hash_config_executada": None,
    }
    for n_etapa in range(n, 6):
        for k in mapa[n_etapa]:
            if k in defaults:
                st.session_state[k] = defaults[k]


def _reset_completo(preservar_modelo: bool = True) -> None:
    """Reset para nova análise · preserva modelos T-MODELO em memória."""
    for k in list(st.session_state.keys()):
        if preservar_modelo and str(k).startswith("_modelo_"):
            continue
        del st.session_state[k]
    _init_state()


# ---------------------------------------------------------------------------
# Ordenação inteligente (Modo 4 · extremos default · D-026)
# ---------------------------------------------------------------------------


def _ordenar_inteligente(valores: List[Any]) -> List[Any]:
    """Tenta ordenação numérica · cronológica · alfabética (nesta ordem · C.5)."""
    if not valores:
        return []
    # numérico
    try:
        pares = [(float(v), v) for v in valores]
        pares.sort(key=lambda p: p[0])
        return [p[1] for p in pares]
    except (TypeError, ValueError):
        pass
    # cronológico (YYYY-MM, YYYY-MM-DD, etc.)
    try:
        pares_dt = [(pd.to_datetime(v), v) for v in valores]
        pares_dt.sort(key=lambda p: p[0])
        return [p[1] for p in pares_dt]
    except (TypeError, ValueError):
        pass
    # alfabético fallback
    return sorted(valores, key=lambda v: str(v))


# ---------------------------------------------------------------------------
# Salvar / Aplicar modelo · Sessão 8.2 · C-2 (P-31)
# ---------------------------------------------------------------------------

# Conjunto de chaves do session_state que compõem um modelo de análise.
# Usado para serializar (Salvar) e re-popular (Aplicar). Mantém versão para
# evolução futura · NÃO inclui v2_result, motor_result, hashes nem flags UX.
_MODELO_CHAVES: List[str] = [
    "estrutura_entrada",
    "coluna_discriminadora",
    "origem_rotulo_tecnico", "comparado_rotulo_tecnico",
    "origem_rotulo_ux", "comparado_rotulo_ux",
    "modo_4_ativado", "estados_nao_escolhidos",
    "campo_analisado", "tipo_campo", "semantica_campo", "unidade",
    "metodo_consolidacao_relativo", "campo_peso", "modo_pre_agregado",
    "thresholds_editados",
    "agrupadores", "regra_agregacao", "agrupador_destacado",
]


def _modelo_atual_bytes() -> bytes:
    """Serializa configuração corrente como JSON (para download)."""
    payload: Dict[str, Any] = {"_modelo_versao": 1}
    for k in _MODELO_CHAVES:
        v = st.session_state.get(k)
        if isinstance(v, (list, tuple)):
            v = list(v)
        elif isinstance(v, dict):
            v = dict(v)
        payload[k] = v
    return json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")


def _aplicar_modelo_bytes(data: bytes) -> None:
    """Lê bytes JSON e popula session_state · valida estrutura mínima."""
    modelo = json.loads(data.decode("utf-8"))
    if not isinstance(modelo, dict):
        raise ValueError("Modelo inválido · não é um objeto JSON.")
    for k in _MODELO_CHAVES:
        if k in modelo:
            st.session_state[k] = modelo[k]
    # Espelha unidade/agrupadores nos widgets keys onde aplicável
    if "unidade" in modelo:
        st.session_state["sel_unidade"] = modelo["unidade"]


# ---------------------------------------------------------------------------
# Header persistente · stepper
# ---------------------------------------------------------------------------


def _render_header() -> None:
    st.title("V2 · Análise Comparativa entre Referências")

    col_obj, col_mod_aplic, col_mod_salv, col_new = st.columns([1, 1, 1, 1])
    with col_obj:
        if st.button("Objetivo da Visão", key="btn_objetivo"):
            st.session_state["_show_objetivo"] = not st.session_state.get("_show_objetivo", False)
    with col_mod_aplic:
        # Sessão 8.2 · C-2 (P-31) · botão agora abre painel inline com
        # file_uploader (CASO A · implementação leve via JSON).
        if st.button("Aplicar modelo", key="btn_aplicar_modelo",
                     disabled=st.session_state["etapa"] == "vazio"):
            st.session_state["_show_aplicar_modelo"] = True
    with col_mod_salv:
        etapa = st.session_state["etapa"]
        idx_etapa = ETAPA_ORDEM.index(etapa) if etapa in ETAPA_ORDEM else 0
        # Sessão 8.2 · C-2 (P-31) · download_button substitui botão sem ação ·
        # gera JSON da config corrente quando habilitado (idx_etapa >= E5).
        st.download_button(
            "Salvar como modelo",
            data=_modelo_atual_bytes(),
            file_name="tabloflow_modelo_v2.json",
            mime="application/json",
            key="btn_salvar_modelo",
            disabled=idx_etapa < ETAPA_ORDEM.index("E5"),
        )
    with col_new:
        if st.button("Nova análise", key="btn_nova_analise"):
            _reset_completo()
            st.rerun()

    if st.session_state.get("_show_objetivo", False):
        with st.expander("Objetivo da V2", expanded=True):
            st.markdown(
                "**O que faz:** compara dois estados de um mesmo universo (Origem × Comparado) "
                "sobre um campo escolhido, agrupado pelas dimensões que você escolher.\n\n"
                "**Quando usar:** Orçado × Realizado, Mês A × Mês B, Cenário 1 × Cenário 2, etc.\n\n"
                "**O que obtém:** 4 KPIs-âncora, Resumo Executivo (6 blocos), Matriz de Confronto "
                "(Coração Visual), Top 10 variações, aba Diagnóstico.\n\n"
                "**Como funciona:** você declara Origem e Comparado (em colunas ou em linhas), "
                "escolhe o campo, tipo, semântica e agrupadores. O motor executa o pipeline "
                "canônico de 6 etapas (A-F) e devolve um V2Result determinístico."
            )

    # Sessão 8.2 · C-2 (P-31) · painel "Aplicar modelo" · uploader inline
    if st.session_state.get("_show_aplicar_modelo", False):
        with st.expander("Aplicar modelo · escolha um arquivo .json", expanded=True):
            arquivo_modelo = st.file_uploader(
                "Modelo previamente salvo (.json)",
                type=["json"],
                key="upload_modelo_json",
                accept_multiple_files=False,
            )
            col_apl_a, col_apl_b = st.columns([1, 1])
            with col_apl_a:
                if arquivo_modelo is not None and st.button(
                    "Confirmar aplicação", key="btn_confirmar_aplicar_modelo",
                    type="primary",
                ):
                    try:
                        _aplicar_modelo_bytes(arquivo_modelo.getvalue())
                        st.session_state["_show_aplicar_modelo"] = False
                        st.success(
                            "Modelo aplicado · revise as etapas e prossiga."
                        )
                        st.rerun()
                    except Exception as exc:  # noqa: BLE001
                        st.error(f"Falha ao aplicar modelo: {exc}")
            with col_apl_b:
                if st.button("Cancelar", key="btn_cancelar_aplicar_modelo"):
                    st.session_state["_show_aplicar_modelo"] = False
                    st.rerun()

    # Stepper user-facing · D-167 · sem código técnico visível (vocab v2 §8)
    if st.session_state["etapa"] not in ("vazio", "ERRO"):
        idx_atual = _indice_stepper()
        cols = st.columns(len(ETAPAS_STEPPER))
        for i, titulo in enumerate(ETAPAS_STEPPER):
            with cols[i]:
                if i < idx_atual:
                    marcador = "✅"
                elif i == idx_atual:
                    marcador = "▶"
                else:
                    marcador = "·"
                st.markdown(f"**{marcador} {titulo}**")

    st.divider()


def _render_expander_ted() -> None:
    """
    TED · Configurações avançadas em expander no topo da tela (D-178 · revoga
    parcialmente D-153 · sai da sidebar global). Colapsado por default.

    Não renderiza a paleta aqui — paleta é escolhida no rodapé da tela
    Resultado, ao lado do botão Baixar Excel (D-175 · §5.3).
    """
    with st.expander("⚙️ Configurações avançadas", expanded=False):
        st.caption(
            "Edições aqui afetam apenas a leitura qualitativa do Resumo Executivo. "
            "Os cálculos principais (Diferença, Variação %, Classificação) não são afetados."
        )
        col_a, col_b = st.columns(2)
        with col_a:
            st.number_input(
                "Limite de estabilidade",
                min_value=0.0, max_value=1.0,
                step=0.005, format="%.4f", key="ted_estab",
                help="Variações menores que este valor são classificadas como estáveis.",
            )
            st.number_input(
                "Limite de nulos massivos",
                min_value=0.0, max_value=1.0,
                step=0.01, format="%.2f", key="ted_null",
                help="Acima deste percentual de nulos em uma coluna, o sistema alerta sobre qualidade.",
            )
        with col_b:
            st.number_input(
                "Limite de valores na coluna de comparação",
                min_value=2, max_value=10_000, key="ted_disc",
                help="Acima deste número de valores distintos, o sistema sugere filtragem.",
            )
            st.number_input(
                "Limite de variação extrema",
                min_value=0.0, max_value=100.0,
                step=0.5, format="%.2f", key="ted_var",
                help="Variações maiores que este percentual são destacadas como extremas.",
            )
    st.session_state["thresholds_editados"] = {
        "limiar_estabilidade_pct": float(st.session_state["ted_estab"]),
        "limiar_nulo_massivo_pct": float(st.session_state["ted_null"]),
        "limite_valores_discriminador_alerta": int(st.session_state["ted_disc"]),
        "limite_variacao_extrema_pct": float(st.session_state["ted_var"]),
    }


def _indice_stepper() -> int:
    """Mapeia etapa atual para o índice 0-4 do stepper."""
    etapa = st.session_state["etapa"]
    if etapa in ("vazio",):
        return 0
    if etapa == "E1_OK":
        return 0
    if etapa == "E2":
        return 1
    if etapa == "E3":
        return 2
    if etapa == "E4":
        return 3
    if etapa in ("RESOL_CASO", "E5", "PROCESSANDO", "RESULTADO", "CHECKLIST"):
        return 4
    return 0


# ---------------------------------------------------------------------------
# Tela 0 · Vazio
# ---------------------------------------------------------------------------


def _tela_vazio() -> None:
    st.subheader("Escolher arquivo")
    st.markdown("Suba o arquivo Excel ou CSV com os dados que você quer comparar.")
    st.caption(
        "Aceita Excel (.xlsx, .xls) e CSV. O arquivo pode ter múltiplas abas — "
        "você escolherá qual analisar no próximo passo."
    )
    up = st.file_uploader(
        "Arquivo",
        type=["xlsx", "xls", "csv", "tsv"],
        key="file_uploader",
    )
    if up is not None:
        try:
            # Persistir bytes em temp file (motor_upload exige caminho físico)
            suffix = "." + up.name.rsplit(".", 1)[-1].lower()
            tmp = tempfile.NamedTemporaryFile(
                delete=False, suffix=suffix, prefix="tabloflow_v2_"
            )
            tmp.write(up.getvalue())
            tmp.flush()
            tmp.close()
            entrada = ArquivoEntrada(caminho_fisico=tmp.name, caminho_logico="unico")
            upload_result = processar_upload([entrada], modo="SIMPLES")
            st.session_state["upload_result"] = upload_result
            st.session_state["nome_arquivo"] = up.name
            info = upload_result.arquivo_unico
            abas = info.abas_disponiveis or []
            st.session_state["abas_disponiveis"] = abas
            st.session_state["aba_selecionada"] = info.aba_selecionada or (
                abas[0] if abas else ""
            )
            st.session_state["etapa"] = "E1_OK"
            st.rerun()
        except Exception as exc:  # noqa: BLE001
            st.error(f"Erro ao ler o arquivo: {exc}")


# ---------------------------------------------------------------------------
# Tela 1 · E1_OK (pós-upload · confirmar aba)
# ---------------------------------------------------------------------------


def _tela_e1_ok() -> None:
    st.subheader("Escolher arquivo")
    upload_result: UploadResult = st.session_state["upload_result"]
    info = upload_result.arquivo_unico
    st.success(f"Arquivo: **{st.session_state['nome_arquivo']}** · Formato: {info.formato}")

    abas = st.session_state.get("abas_disponiveis", []) or []
    aba_atual = st.session_state.get("aba_selecionada", "")
    if abas:
        nova_aba = st.selectbox(
            "Aba a analisar",
            abas,
            index=abas.index(aba_atual) if aba_atual in abas else 0,
            key="sel_aba",
        )
        if nova_aba != aba_atual:
            st.session_state["aba_selecionada"] = nova_aba
            _invalidar_a_partir("E2")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Voltar · trocar arquivo", key="btn_voltar_upload"):
            _reset_completo()
            st.rerun()
    with col_b:
        if st.button("Confirmar e processar base", key="btn_confirmar_e1", type="primary"):
            try:
                aba_escolhida = st.session_state["aba_selecionada"]
                if aba_escolhida and aba_escolhida != info.aba_selecionada:
                    upload_result = processar_upload(
                        [ArquivoEntrada(
                            caminho_fisico=_extrair_caminho(info),
                            caminho_logico="unico",
                            aba_solicitada=aba_escolhida,
                        )],
                        modo="SIMPLES",
                    )
                    st.session_state["upload_result"] = upload_result
                motor_result = processar_base(upload_result)
                st.session_state["motor_result"] = motor_result
                if motor_result.bloqueios:
                    st.session_state["v2_result"] = None
                    st.session_state["etapa"] = "ERRO"
                    st.session_state["_erro_origem"] = "motor_base"
                    st.rerun()
                st.session_state["etapa"] = "E2"
                _invalidar_a_partir("E2")
                st.rerun()
            except Exception as exc:  # noqa: BLE001
                st.error(f"Falha ao processar a base: {exc}")


def _extrair_caminho(info) -> str:
    """Recupera caminho físico do arquivo temp · info.nome_arquivo é apenas o nome."""
    # Motor_upload preserva arquivo_bytes · regravar em novo temp preserva comportamento
    tmp = tempfile.NamedTemporaryFile(
        delete=False, suffix="." + info.formato, prefix="tabloflow_v2_aba_"
    )
    tmp.write(info.arquivo_bytes)
    tmp.flush()
    tmp.close()
    return tmp.name


# ---------------------------------------------------------------------------
# Tela 2 · E2 · Estrutura da comparação
# ---------------------------------------------------------------------------


def _tela_e2() -> None:
    st.subheader("Reconhecer estrutura")
    st.caption("Indique como a comparação está organizada na sua base.")
    motor_result: MotorResult = st.session_state["motor_result"]
    df = motor_result.df

    estrutura_atual = st.session_state["estrutura_entrada"]
    estrutura = st.radio(
        "Como os dois lados da comparação estão organizados?",
        ["POR_COLUNAS", "POR_LINHAS"],
        index=["POR_COLUNAS", "POR_LINHAS"].index(estrutura_atual),
        format_func=lambda s: {
            "POR_COLUNAS": "Cada lado em uma coluna distinta (ex: Orçado e Realizado lado a lado)",
            "POR_LINHAS": "Os dois lados empilhados em uma coluna identificadora (ex: Cenário com Orçado/Realizado nas linhas)",
        }[s],
        key="rad_estrutura",
    )
    if estrutura != estrutura_atual:
        st.session_state["estrutura_entrada"] = estrutura
        _invalidar_a_partir("E3")

    colunas = list(df.columns)

    if estrutura == "POR_LINHAS":
        col_disc = st.selectbox(
            "Coluna discriminadora",
            [""] + colunas,
            index=(([""] + colunas).index(st.session_state["coluna_discriminadora"])
                   if st.session_state["coluna_discriminadora"] in colunas else 0),
            key="sel_disc",
        )
        st.session_state["coluna_discriminadora"] = col_disc or None

        if col_disc:
            valores = df[col_disc].dropna().unique().tolist()
            valores_ord = _ordenar_inteligente(valores)
            n_vals = len(valores_ord)
            st.caption(f"{n_vals} valor(es) único(s) detectado(s) na coluna {col_disc!r}")

            if n_vals < 2:
                st.error(
                    f"A coluna de comparação {col_disc!r} tem menos de 2 valores únicos · "
                    "não é possível comparar dois lados. Escolha outra coluna."
                )
            elif n_vals == 2:
                orig_default = str(valores_ord[0])
                comp_default = str(valores_ord[1])
                origem = st.selectbox(
                    "Comparar de (valor 1)", valores_ord, index=0, key="sel_orig_lin"
                )
                comparado = st.selectbox(
                    "Comparar com (valor 2)", valores_ord, index=1, key="sel_comp_lin"
                )
                st.session_state["origem_rotulo_tecnico"] = str(origem)
                st.session_state["comparado_rotulo_tecnico"] = str(comparado)
                st.session_state["modo_4_ativado"] = False
                st.session_state["estados_nao_escolhidos"] = []
            else:
                st.info(
                    f"A coluna {col_disc!r} tem {n_vals} valores diferentes. "
                    "Selecione 2 para comparar · a sugestão são os extremos por ordenação inteligente."
                )
                default_escolha = [str(valores_ord[0]), str(valores_ord[-1])]
                escolha = st.multiselect(
                    "Escolha 2 valores para comparar",
                    [str(v) for v in valores_ord],
                    default=default_escolha,
                    max_selections=2,
                    key="ms_modo4",
                )
                if len(escolha) == 2:
                    st.session_state["origem_rotulo_tecnico"] = escolha[0]
                    st.session_state["comparado_rotulo_tecnico"] = escolha[1]
                    st.session_state["modo_4_ativado"] = True
                    st.session_state["estados_nao_escolhidos"] = [
                        str(v) for v in valores_ord if str(v) not in escolha
                    ]
                else:
                    st.warning("Escolha exatamente 2 valores.")
    else:
        # Dois lados em colunas distintas (cada lado em uma coluna)
        st.session_state["coluna_discriminadora"] = None
        st.session_state["modo_4_ativado"] = False
        st.session_state["estados_nao_escolhidos"] = []
        col_orig = st.selectbox(
            "Comparar de (coluna)",
            [""] + colunas,
            index=(([""] + colunas).index(st.session_state["origem_rotulo_tecnico"])
                   if st.session_state["origem_rotulo_tecnico"] in colunas else 0),
            key="sel_orig_col",
        )
        col_comp = st.selectbox(
            "Comparar com (coluna)",
            [""] + colunas,
            index=(([""] + colunas).index(st.session_state["comparado_rotulo_tecnico"])
                   if st.session_state["comparado_rotulo_tecnico"] in colunas else 0),
            key="sel_comp_col",
        )
        st.session_state["origem_rotulo_tecnico"] = col_orig or ""
        st.session_state["comparado_rotulo_tecnico"] = col_comp or ""

    # Rótulos amigáveis · C.D6 · DDU · pré-preenchidos com a detecção (D-161)
    st.markdown("**Rótulos amigáveis** — como os dois lados aparecerão no Excel")
    st.caption("Detectados automaticamente · você pode alterar.")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        origem_ux = st.text_input(
            "Como chamar este lado (Origem)",
            value=st.session_state["origem_rotulo_ux"] or st.session_state["origem_rotulo_tecnico"],
            placeholder="Ex: Orçado, Antes, Mês A",
            key="txt_orig_ux",
        )
        st.session_state["origem_rotulo_ux"] = origem_ux
    with col_r2:
        comparado_ux = st.text_input(
            "Como chamar este lado (Comparado)",
            value=st.session_state["comparado_rotulo_ux"] or st.session_state["comparado_rotulo_tecnico"],
            placeholder="Ex: Realizado, Depois, Mês B",
            key="txt_comp_ux",
        )
        st.session_state["comparado_rotulo_ux"] = comparado_ux

    st.divider()
    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("← Voltar", key="btn_voltar_e2"):
            st.session_state["etapa"] = "E1_OK"
            st.rerun()
    with col_b:
        pode_avancar = (
            bool(st.session_state["origem_rotulo_tecnico"])
            and bool(st.session_state["comparado_rotulo_tecnico"])
            and st.session_state["origem_rotulo_tecnico"]
            != st.session_state["comparado_rotulo_tecnico"]
        )
        if st.button("Próximo · Configurar análise", key="btn_avancar_e3",
                     type="primary", disabled=not pode_avancar):
            st.session_state["etapa"] = "E3"
            _invalidar_a_partir("E3")
            st.rerun()


# ---------------------------------------------------------------------------
# Tela 3 · E3 · Configurar análise
# ---------------------------------------------------------------------------


def _tela_e3() -> None:
    st.subheader("Configurar análise")
    st.caption("Escolha o campo a analisar e como ele se comporta.")
    motor_result: MotorResult = st.session_state["motor_result"]
    df = motor_result.df
    estrutura = st.session_state["estrutura_entrada"]

    # Campo analisado
    if estrutura == "POR_COLUNAS":
        st.markdown(
            "Como os dois lados já estão em colunas distintas, informe o nome conceitual "
            "do que está sendo comparado (ex: *Receita*, *Quantidade*)."
        )
        campo = st.text_input(
            "Nome conceitual do campo",
            value=st.session_state["campo_analisado"] or "Valor",
            key="txt_campo_concept",
        )
    else:
        colunas_numericas = [
            c for c in df.columns
            if pd.api.types.is_numeric_dtype(df[c])
            and c != st.session_state["coluna_discriminadora"]
        ]
        opcoes_campo = colunas_numericas + [
            c for c in df.columns
            if c not in colunas_numericas and c != st.session_state["coluna_discriminadora"]
        ]
        idx = (opcoes_campo.index(st.session_state["campo_analisado"])
               if st.session_state["campo_analisado"] in opcoes_campo else 0)
        campo = st.selectbox(
            "Campo a analisar", opcoes_campo or [""], index=idx, key="sel_campo"
        )
    st.session_state["campo_analisado"] = campo or ""

    # Tipo
    idx_tipo = [t[0] for t in TIPOS_CAMPO].index(st.session_state["tipo_campo"])
    tipo_anterior = st.session_state["tipo_campo"]
    tipo = st.radio(
        "Como esse campo se comporta?",
        [t[0] for t in TIPOS_CAMPO],
        index=idx_tipo,
        format_func=lambda k: dict(TIPOS_CAMPO)[k],
        key="rad_tipo",
    )
    st.session_state["tipo_campo"] = tipo
    # Sessão 8.3 · C-2 (P-35) · Quando tipo muda, força reset da Unidade ao
    # default DDU (C.D6 · D-161). Atualiza tanto `unidade` quanto `sel_unidade`
    # porque Streamlit prioriza session_state[key] sobre `index=` no widget.
    # Usuária preserva direito de sobrescrever manualmente após o reset
    # (próxima rerender com tipo igual não dispara este branch).
    if tipo != tipo_anterior:
        unidade_default = default_unidade_para_tipo_campo(tipo)
        st.session_state["unidade"] = unidade_default
        st.session_state["sel_unidade"] = unidade_default

    # Semântica
    if tipo == "ESTADO_SITUACAO":
        st.caption("Semântica não se aplica a categoria/rótulo · o resultado compara mudança × estabilidade.")
        st.session_state["semantica_campo"] = "NEUTRO"
    else:
        idx_sem = [s[0] for s in SEMANTICAS].index(st.session_state["semantica_campo"])
        sem = st.radio(
            "Subir é bom, ruim ou neutro?",
            [s[0] for s in SEMANTICAS],
            index=idx_sem,
            format_func=lambda k: dict(SEMANTICAS)[k],
            key="rad_sem",
        )
        st.session_state["semantica_campo"] = sem

    # Unidade · E1 · widget aparece quando tipo_campo != ESTADO_SITUACAO ·
    # default inferido do tipo · usuária pode sobrescrever (princípio C.D6 DDU).
    if tipo == "ESTADO_SITUACAO":
        st.session_state["unidade"] = "ADIMENSIONAL"
    else:
        unid_atual = st.session_state.get("unidade") or default_unidade_para_tipo_campo(tipo)
        if unid_atual not in [u[0] for u in UNIDADES]:
            unid_atual = default_unidade_para_tipo_campo(tipo)
        idx_unid = [u[0] for u in UNIDADES].index(unid_atual)
        unid = st.selectbox(
            "Em qual unidade o campo é expresso?",
            [u[0] for u in UNIDADES],
            index=idx_unid,
            format_func=lambda k: dict(UNIDADES)[k],
            key="sel_unidade",
            help=(
                "Define como Diferença, Variação e Total aparecem no Excel · "
                "preenche automaticamente conforme o tipo escolhido acima · "
                "pode ser ajustado manualmente."
            ),
        )
        st.session_state["unidade"] = unid

    # Consolidação (apenas relativo/não-aditivo)
    if tipo in ("NUMERICO_RELATIVO", "NUMERICO_NAO_ADITIVO"):
        default_metodo = st.session_state["metodo_consolidacao_relativo"] or "MEDIA_SIMPLES"
        idx_met = [m[0] for m in METODOS_CONSOLIDACAO].index(default_metodo)
        metodo = st.radio(
            "Como consolidar esse campo quando você agrupa?",
            [m[0] for m in METODOS_CONSOLIDACAO],
            index=idx_met,
            format_func=lambda k: dict(METODOS_CONSOLIDACAO)[k],
            key="rad_metodo",
        )
        st.session_state["metodo_consolidacao_relativo"] = metodo
        if metodo == "MEDIA_PONDERADA":
            col_numericas = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
            peso = st.selectbox(
                "Campo de peso", [""] + col_numericas,
                index=((([""] + col_numericas).index(st.session_state["campo_peso"]))
                       if st.session_state["campo_peso"] in col_numericas else 0),
                key="sel_peso",
            )
            st.session_state["campo_peso"] = peso or None
        else:
            st.session_state["campo_peso"] = None
    else:
        st.session_state["metodo_consolidacao_relativo"] = None
        st.session_state["campo_peso"] = None

    # Pré-agregado (toggle informativo)
    st.session_state["modo_pre_agregado"] = st.checkbox(
        "Minha base já está pré-agregada (1 linha por combinação)",
        value=st.session_state["modo_pre_agregado"],
        key="chk_preagr",
    )

    # Configurações avançadas (thresholds) estão no expander no topo (D-178)
    st.caption(
        "Configurações avançadas (limites editáveis) disponíveis no expander "
        "'⚙️ Configurações avançadas' no topo desta tela."
    )

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("← Voltar", key="btn_voltar_e3"):
            st.session_state["etapa"] = "E2"
            st.rerun()
    with col_b:
        pode_avancar = bool(st.session_state["campo_analisado"])
        if st.button("Próximo · Agrupar", key="btn_avancar_e4",
                     type="primary", disabled=not pode_avancar):
            st.session_state["etapa"] = "E4"
            _invalidar_a_partir("E4")
            st.rerun()


# ---------------------------------------------------------------------------
# Tela 4 · E4 · Agrupadores
# ---------------------------------------------------------------------------


def _tela_e4() -> None:
    st.subheader("Agrupar")
    st.caption("Defina por quais dimensões a comparação será feita.")
    motor_result: MotorResult = st.session_state["motor_result"]
    df = motor_result.df

    colunas_disponiveis = [
        c for c in df.columns
        if c != st.session_state["coluna_discriminadora"]
        and c != st.session_state["campo_analisado"]
        and c != st.session_state["origem_rotulo_tecnico"]
        and c != st.session_state["comparado_rotulo_tecnico"]
    ]

    agrupadores = st.multiselect(
        "Agrupar por (1 a 9 dimensões)",
        colunas_disponiveis,
        default=st.session_state["agrupadores"],
        key="ms_agrup",
        help="Cada combinação dos agrupadores escolhidos vira uma linha do resultado.",
    )
    st.session_state["agrupadores"] = agrupadores

    # Agrupador destacado · E3b · só aparece para tipo numérico
    if agrupadores and st.session_state["tipo_campo"] != "ESTADO_SITUACAO":
        default_dest = st.session_state.get("agrupador_destacado") or agrupadores[0]
        if default_dest not in agrupadores:
            default_dest = agrupadores[0]
        idx_dest = agrupadores.index(default_dest)
        dest = st.selectbox(
            "Qual dimensão destacar no Resumo Executivo?",
            agrupadores,
            index=idx_dest,
            format_func=_rotular_agrupador_ui,
            key="sel_agrupador_destacado",
            help=(
                "A dimensão escolhida será analisada no bloco 'Onde se concentra' "
                "do Resumo Executivo · mostrando as 3 categorias que mais "
                "influenciaram o resultado."
            ),
        )
        st.session_state["agrupador_destacado"] = dest
    elif not agrupadores:
        st.session_state["agrupador_destacado"] = None

    # Regra de agregação
    if st.session_state["tipo_campo"] == "ESTADO_SITUACAO":
        st.caption("Regra fixa em 'Contagem' para categoria/rótulo.")
        st.session_state["regra_agregacao"] = "CONTAGEM"
    else:
        idx = REGRAS_AGREGACAO.index(st.session_state["regra_agregacao"])
        regra = st.radio(
            "Como consolidar valores quando há múltiplas linhas por combinação?",
            REGRAS_AGREGACAO,
            index=idx,
            horizontal=True,
            format_func=lambda k: REGRAS_LABELS.get(k, k),
            key="rad_regra",
        )
        st.session_state["regra_agregacao"] = regra

    # Estimativa conservadora de linhas (D-027)
    estimativa = _estimar_linhas_saida(df, agrupadores)
    patamar = _classificar_patamar_agrupadores(len(agrupadores))

    if patamar == "P2-AGRUP-ALERTA-LEVE":
        st.info(f"Estimativa: {estimativa:,} linhas no resultado · granularidade média.")
    elif patamar == "P3-AGRUP-ALERTA-FORTE":
        st.warning(
            f"Estimativa: {estimativa:,} linhas · análise com granularidade fina · "
            "confirme que é o que pretende."
        )
        st.session_state["confirmacao_p3_agrupadores"] = st.checkbox(
            f"Entendi o impacto · seguir com {estimativa:,} linhas",
            value=st.session_state["confirmacao_p3_agrupadores"],
            key="chk_p3",
        )
    elif patamar == "P4-AGRUP-BLOQUEIO":
        st.error(
            f"Você selecionou {len(agrupadores)} agrupadores · acima do máximo de 9. "
            "Para cruzamento multidimensional considere uma análise diferente."
        )
        st.session_state["confirmacao_p3_agrupadores"] = False
    else:
        st.success(f"Estimativa: {estimativa:,} linhas no resultado.")

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("← Voltar", key="btn_voltar_e4"):
            st.session_state["etapa"] = "E3"
            st.rerun()
    with col_b:
        if patamar == "P3-AGRUP-ALERTA-FORTE":
            pode_avancar = (
                bool(agrupadores)
                and st.session_state["confirmacao_p3_agrupadores"]
            )
        elif patamar == "P4-AGRUP-BLOQUEIO":
            pode_avancar = False
        else:
            pode_avancar = bool(agrupadores)
        if st.button("Próximo · Revisar e executar", key="btn_avancar_e5",
                     type="primary", disabled=not pode_avancar):
            st.session_state["etapa"] = "E5"
            _invalidar_a_partir("E5")
            st.rerun()


def _estimar_linhas_saida(df: pd.DataFrame, agrupadores: List[str]) -> int:
    """Estimativa conservadora sem materializar · §2.12 Eixo 3."""
    if not agrupadores:
        return 1
    prod = 1
    for a in agrupadores:
        if a in df.columns:
            prod *= max(1, int(df[a].nunique(dropna=True)))
    return prod


# ---------------------------------------------------------------------------
# Tela 6 · E5 · Revisão e execução
# ---------------------------------------------------------------------------


def _tela_e5() -> None:
    st.subheader("Revisar e executar")
    st.caption("Confira a configuração antes de processar.")

    # Labels de estrutura user-facing
    estrutura_label = {
        "POR_COLUNAS": "dois lados em colunas distintas",
        "POR_LINHAS": "dois lados empilhados em coluna identificadora",
    }.get(st.session_state["estrutura_entrada"], st.session_state["estrutura_entrada"])
    modo_4_sufixo = " · 2 valores escolhidos" if st.session_state["modo_4_ativado"] else ""
    tipo_label = dict(TIPOS_CAMPO).get(
        st.session_state["tipo_campo"], st.session_state["tipo_campo"]
    )
    sem_label = dict(SEMANTICAS).get(
        st.session_state["semantica_campo"], st.session_state["semantica_campo"]
    )
    regra_label = REGRAS_LABELS.get(
        st.session_state["regra_agregacao"], st.session_state["regra_agregacao"]
    )

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"**Arquivo**\n\n{st.session_state['nome_arquivo']}\n\nAba: "
                    f"{st.session_state['aba_selecionada'] or '—'}")
    with c2:
        st.markdown(f"**Estrutura**\n\n{estrutura_label}{modo_4_sufixo}\n\n"
                    f"Comparar de: {st.session_state['origem_rotulo_ux'] or '—'}\n\n"
                    f"Comparar com: {st.session_state['comparado_rotulo_ux'] or '—'}")
    with c3:
        st.markdown(f"**Campo**\n\n{st.session_state['campo_analisado'] or '—'}\n\n"
                    f"{tipo_label}\n\n{sem_label}")
    with c4:
        st.markdown(f"**Agrupadores**\n\n{len(st.session_state['agrupadores'])} dimensão(ões)\n\n"
                    f"{', '.join(st.session_state['agrupadores']) or '—'}\n\n"
                    f"Agregação: {regra_label}")
    with c5:
        st.markdown(f"**Paleta**\n\n{st.session_state.get('paleta_selecionada', PALETA_DEFAULT)}")

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("← Voltar", key="btn_voltar_e5"):
            st.session_state["etapa"] = "E4"
            st.rerun()
    with col_b:
        if st.button("Processar análise", key="btn_processar", type="primary"):
            _executar_pipeline_v2()
            st.rerun()


def _executar_pipeline_v2() -> None:
    """Executa executar_v2 e ajusta etapa para RESULTADO ou ERRO."""
    config = _construir_config()
    motor_result: MotorResult = st.session_state["motor_result"]
    try:
        v2_result: V2Result = executar_v2(motor_result, config)
    except Exception as exc:  # noqa: BLE001
        st.session_state["v2_result"] = None
        st.session_state["_erro_processamento"] = str(exc)
        st.session_state["etapa"] = "ERRO"
        return
    # Enriquecer config_usada com paleta + adaptador do diagnóstico narrativo.
    # config_usada é Dict[str, Any] · mutável · sem alteração em contratos/exportacao.
    if not v2_result.bloqueios_disparados:
        _enriquecer_config_usada_pos_pipeline(v2_result)
    st.session_state["v2_result"] = v2_result
    if v2_result.bloqueios_disparados:
        st.session_state["etapa"] = "ERRO"
        st.session_state["_hash_config_executada"] = None
    else:
        st.session_state["etapa"] = "RESULTADO"
        # D-186 · marca o hash da config no momento desta execução · usado
        # como referência pelo gate de stale em _tela_resultado.
        st.session_state["_hash_config_executada"] = _hash_config_critica()


def _enriquecer_config_usada_pos_pipeline(v2_result: V2Result) -> None:
    """
    Injeta paleta selecionada e config achatada do diagnóstico narrativo em
    config_usada (Dict[str, Any] · mutável). Sem alteração de contrato Pydantic.

    Paleta: aba Parâmetros do Excel consome config_usada · valor registrado.
    Aplicação visual efetiva aguarda extensão de ConfigExportacao (candidato D-XXX).

    Config diagnóstico: 12 campos achatados esperados por capability 10
    (renderizar_diagnostico · D-165). Disponível para consumo quando exportacao.py
    integrar a capability.
    """
    v2_result.config_usada["paleta_aplicada"] = st.session_state.get(
        "paleta_selecionada", PALETA_DEFAULT
    )
    v2_result.config_usada["_config_diagnostico"] = _extrair_config_para_diagnostico(
        v2_result=v2_result,
        paleta_selecionada=st.session_state.get("paleta_selecionada", PALETA_DEFAULT),
        arquivo_nome=st.session_state.get("nome_arquivo", ""),
        aba_consumida=st.session_state.get("aba_selecionada", ""),
    )


def _extrair_config_para_diagnostico(
    v2_result: V2Result,
    paleta_selecionada: str,
    arquivo_nome: str,
    aba_consumida: str,
) -> Dict[str, Any]:
    """
    Monta o dict canônico achatado esperado por F-APRESENT capability 10
    (renderizar_diagnostico · D-165) a partir dos múltiplos campos do V2Result
    + parâmetros upstream do app.

    Sem mudança em V2Result · sem mudança em motor · sem mudança em F-APRESENT.
    Capability 10 é genérica · trata None como '—' via formatar_valor_ou_traco.

    Achado da Sessão 3 (F-APRESENT P1) · aplicado aqui como adaptador em app_v2.
    Colunas técnicas ausentes no contrato real (ex: nulos_por_classificacao)
    passam None · capability 10 exibe '—'.
    """
    comp = v2_result.comparacao_realizada
    qualidade = v2_result.resumo_executivo.bloco_6_qualidade_estrutural
    thresholds = v2_result.config_usada.get("thresholds", {}) or {}
    return {
        # Seção 1 · Como foi analisado
        "arquivo": arquivo_nome or None,
        "aba_consumida": aba_consumida or None,
        "modo_base": v2_result.config_usada.get("modo_pre_agregado"),
        "agrupadores": v2_result.agrupadores_aplicados,
        "campo_analisado": comp.campo_analisado,
        "tipo_medida": comp.tipo_campo,
        "colunas_mapeadas": {
            "origem_rotulo_ux": comp.origem_rotulo_ux,
            "comparado_rotulo_ux": comp.comparado_rotulo_ux,
            "origem_rotulo_tecnico": comp.origem_rotulo_tecnico,
            "comparado_rotulo_tecnico": comp.comparado_rotulo_tecnico,
        },
        # Seção 4 · Decisões do usuário
        "estados_nao_escolhidos": list(comp.estados_nao_escolhidos or []),
        # Seção 5 · Configurações avançadas aplicadas
        "paleta_aplicada": paleta_selecionada,
        "thresholds_usados": dict(thresholds),
        "defaults_sobrescritos": None,  # motor não expõe · capability 10 trata como '—'
        # Seção 6 · Qualidade estrutural
        "nulos_por_classificacao": None,  # ausente no contrato real · '—'
        "total_warnings": qualidade.total_warnings,
        "warnings_por_categoria": dict(qualidade.warnings_por_categoria),
        "ajustes_aplicados": qualidade.ajustes_aplicados,
    }


def _construir_config() -> Dict[str, Any]:
    agrupadores_atuais = list(st.session_state["agrupadores"])
    destacado = st.session_state.get("agrupador_destacado")
    if not destacado or destacado not in agrupadores_atuais:
        destacado = agrupadores_atuais[0] if agrupadores_atuais else None
    return {
        "estrutura_entrada": st.session_state["estrutura_entrada"],
        "origem_rotulo_tecnico": st.session_state["origem_rotulo_tecnico"],
        "comparado_rotulo_tecnico": st.session_state["comparado_rotulo_tecnico"],
        "origem_rotulo_ux": st.session_state["origem_rotulo_ux"],
        "comparado_rotulo_ux": st.session_state["comparado_rotulo_ux"],
        "coluna_discriminadora": st.session_state["coluna_discriminadora"],
        "modo_4_ativado": st.session_state["modo_4_ativado"],
        "estados_nao_escolhidos": st.session_state["estados_nao_escolhidos"],
        "campo_analisado": st.session_state["campo_analisado"],
        "tipo_campo": st.session_state["tipo_campo"],
        "semantica_campo": st.session_state["semantica_campo"],
        "unidade": st.session_state.get("unidade") or default_unidade_para_tipo_campo(
            st.session_state["tipo_campo"]
        ),
        "regra_agregacao": st.session_state["regra_agregacao"],
        "metodo_consolidacao_relativo": st.session_state["metodo_consolidacao_relativo"],
        "campo_peso": st.session_state["campo_peso"],
        "modo_pre_agregado": st.session_state["modo_pre_agregado"],
        "agrupadores": agrupadores_atuais,
        "agrupador_destacado": destacado,
        "resolucao_estrutural": st.session_state["resolucao_estrutural"],
        "thresholds": dict(st.session_state["thresholds_editados"]),
        "modelo_aplicado": None,
    }


def _hash_config_critica() -> str:
    """
    Hash determinístico dos campos da config que entram em executar_v2.

    D-186 (Sessão 5) · gate de stale na tela RESULTADO. Quando qualquer um
    desses campos muda no session_state após a última execução do motor, o
    resultado armazenado deixa de refletir a config corrente · a tela RESULTADO
    deve marcar o resultado como stale e exigir nova execução. Inclui a aba
    selecionada e o nome do arquivo (Etapas 1-2) para captar troca de fonte.
    """
    import hashlib
    import json

    config = _construir_config()
    payload = {
        "config": config,
        "nome_arquivo": st.session_state.get("nome_arquivo"),
        "aba_selecionada": st.session_state.get("aba_selecionada"),
    }
    serializado = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(serializado.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Tela 8 · RESULTADO
# ---------------------------------------------------------------------------


def _tela_resultado() -> None:
    """
    Tela "Resultado da análise" · D-177 · microanálise executiva em tela.

    5 blocos executivos + rodapé com paleta + download:
      1. Cabeçalho executivo
      2. Números-âncora (st.metric)
      3. Distribuição estrutural + gráfico
      4. Top variações + gráfico de barras
      5. Leitura qualitativa + qualidade (+ expander detalhes do diagnóstico)
      · Rodapé: Voltar · Paleta · Baixar Excel
    """
    v2: V2Result = st.session_state["v2_result"]
    comp = v2.comparacao_realizada
    origem = comp.origem_rotulo_ux or comp.origem_rotulo_tecnico or "origem"
    comparado = comp.comparado_rotulo_ux or comp.comparado_rotulo_tecnico or "comparado"

    # --------------------------------------------------------------------
    # Gate de stale (D-186) · se a config crítica mudou desde a última
    # execução do motor, marcar o resultado em tela como desatualizado e
    # oferecer o botão de re-execução. Sem clicar, evitamos exibir números
    # incongruentes com a configuração corrente do session_state.
    # --------------------------------------------------------------------
    hash_atual = _hash_config_critica()
    hash_executado = st.session_state.get("_hash_config_executada")
    resultado_stale = (
        hash_executado is not None and hash_atual != hash_executado
    )
    if resultado_stale:
        st.warning(
            "⚠️ A configuração foi alterada após a última execução. "
            "O resultado abaixo reflete a configuração anterior · clique em "
            "**Executar análise** para atualizar."
        )
        if st.button(
            "🔄 Executar análise com a configuração atual",
            key="btn_reexecutar_stale",
            type="primary",
        ):
            _executar_pipeline_v2()
            st.rerun()

    # --------------------------------------------------------------------
    # 1 · Cabeçalho executivo
    # --------------------------------------------------------------------
    st.header("📊 Resultado da análise")
    agora = datetime.now()
    st.caption(
        f"Análise comparativa entre **{origem}** e **{comparado}** · "
        f"gerada em {agora.day:02d}/{agora.month:02d}/{agora.year:04d} às "
        f"{agora.hour:02d}:{agora.minute:02d}"
    )

    # --------------------------------------------------------------------
    # 2 · Números-âncora · 4 st.metric
    # Sessão 8.2 · C-1 (P-29) · cards consomem helpers de unidade · espelho
    # exato de exportacao_v2 (Resumo Executivo · "Números principais") para
    # evitar divergência tela × Excel quando unidade != MONETARIO_BRL.
    # --------------------------------------------------------------------
    ancora = v2.numeros_ancora
    unidade = comp.unidade
    st.markdown("#### Números principais")
    k1, k2, k3, k4 = st.columns(4)
    if ancora.total_origem is not None or ancora.total_comparado is not None:
        rot_card_total = label_total_card(unidade)
        # Conta linhas com diferenca não-nula (proxy de PRESENTE_AMBOS para média)
        n_pa = 0
        if v2.base_analitica is not None and "diferenca" in v2.base_analitica.columns:
            n_pa = int(v2.base_analitica["diferenca"].dropna().shape[0])
        valor_orig_card = valor_total_card(ancora.total_origem, n_pa, unidade)
        valor_comp_card = valor_total_card(ancora.total_comparado, n_pa, unidade)
        if unidade == "PERCENTUAL" and valor_orig_card is not None and valor_comp_card is not None:
            dif_card = valor_comp_card - valor_orig_card
            var_card = (dif_card / valor_orig_card) if valor_orig_card not in (None, 0) else None
        else:
            dif_card = ancora.diferenca_total
            var_card = ancora.variacao_total_pct
        with k1:
            st.metric(
                f"{rot_card_total} · {origem}",
                formatar_valor_por_unidade(valor_orig_card, unidade),
            )
        with k2:
            st.metric(
                f"{rot_card_total} · {comparado}",
                formatar_valor_por_unidade(valor_comp_card, unidade),
            )
        with k3:
            delta = None
            if var_card is not None:
                delta = formatar_percentual_br(var_card, conversao_fracao=True)
            st.metric(
                rotulo_diferenca(unidade),
                formatar_diferenca_por_unidade(dif_card, unidade),
                delta=delta,
            )
        with k4:
            st.metric(
                rotulo_variacao(unidade),
                formatar_percentual_br(var_card, conversao_fracao=True),
            )
    else:
        with k1:
            st.metric("Combinações analisadas", f"{ancora.total_combinacoes_analisadas or 0:,}".replace(",", "."))
        with k2:
            st.metric("Com mudança", f"{ancora.combinacoes_com_mudanca or 0:,}".replace(",", "."))
        with k3:
            st.metric("Estáveis", f"{ancora.combinacoes_estaveis or 0:,}".replace(",", "."))
        with k4:
            st.metric("% mudança", _fmt_pct_br(ancora.pct_mudanca))

    # --------------------------------------------------------------------
    # 3 · Saúde da comparação (numérico) ou Como os casos se distribuem (Estado)
    # Sessão 8.2 · C-1 (P-29) · roteamento por tipo_campo espelhando D-192:
    # ESTADO_SITUACAO mantém distribuição estrutural; tipos numéricos exibem
    # "Saúde da comparação" com 3 colunas (PERCENTUAL) ou 4 (demais unidades).
    # --------------------------------------------------------------------
    if comp.tipo_campo == "ESTADO_SITUACAO":
        st.markdown("#### Como os casos se distribuem")
        dist = v2.distribuicao_classificacoes_estruturais or {}
        rotulos_estru_ux = {
            "PRESENTE_AMBOS": "Presente nos dois lados",
            "AUSENTE_ORIGEM": "Ausente na origem",
            "AUSENTE_COMPARADO": "Ausente no comparado",
            "NULO_ORIGEM": "Sem valor na origem",
            "NULO_COMPARADO": "Sem valor no comparado",
            "NULO_AMBOS": "Sem valor nos dois lados",
        }
        total = sum(int(v or 0) for v in dist.values()) or 1
        dados_dist = pd.DataFrame([
            {
                "Categoria": rotulos_estru_ux.get(cat, cat),
                "Casos": int(qtd or 0),
                "Participação": (int(qtd or 0) / total),
            }
            for cat, qtd in dist.items() if cat
        ])
        col_d1, col_d2 = st.columns([1, 1])
        with col_d1:
            st.dataframe(
                dados_dist,
                column_config={
                    "Casos": st.column_config.NumberColumn("Casos", format="%d"),
                    "Participação": st.column_config.NumberColumn("Participação", format="%.2f%%"),
                },
                hide_index=True,
                width="stretch",
            )
        with col_d2:
            if not dados_dist.empty:
                grafico_dist = dados_dist.set_index("Categoria")[["Casos"]]
                st.bar_chart(grafico_dist, horizontal=False)
    else:
        st.markdown("#### Saúde da comparação")
        semantica = comp.semantica_campo
        dist_sem = v2.distribuicao_classificacoes_semanticas or {}
        delta_sem = v2.delta_por_classificacao_semantica or {}
        chaves_saude = _categorias_saude_para_exibir(semantica, dist_sem)
        total_pa = sum(int(dist_sem.get(k, 0)) for k in chaves_saude) or 1
        exibe_delta = unidade != "PERCENTUAL"

        linhas_saude = []
        for chave in chaves_saude:
            n_cat = int(dist_sem.get(chave, 0))
            delta_cat = float(delta_sem.get(chave, 0.0))
            part_cat = n_cat / total_pa if total_pa else 0
            rot_cat = _LABEL_SEMANTICA_SAUDE.get(chave, chave)
            linha_saude = {
                "Categoria": rot_cat,
                "Casos": n_cat,
                "Participação": part_cat,
            }
            if exibe_delta:
                linha_saude["Δ total"] = delta_cat
            linhas_saude.append(linha_saude)
        df_saude = pd.DataFrame(linhas_saude)

        col_config_saude = {
            "Categoria": st.column_config.TextColumn("Categoria"),
            "Casos": st.column_config.NumberColumn("Casos", format="%d"),
            "Participação": st.column_config.NumberColumn("Participação", format="%.2f%%"),
        }
        if exibe_delta:
            if unidade == "MONETARIO_BRL":
                fmt_delta = "R$ %.2f"
            elif unidade == "QUANTIDADE":
                fmt_delta = "%d"
            elif unidade == "TEMPO_DIAS":
                fmt_delta = "%d dias"
            elif unidade == "TEMPO_HORAS":
                fmt_delta = "%d h"
            elif unidade == "MULTIPLICADOR":
                fmt_delta = "%.2fx"
            elif unidade == "RAZAO":
                fmt_delta = "%.4f"
            else:
                fmt_delta = "%.2f"
            col_config_saude["Δ total"] = st.column_config.NumberColumn("Δ total", format=fmt_delta)

        col_s1, col_s2 = st.columns([1, 1])
        with col_s1:
            st.dataframe(
                df_saude,
                column_config=col_config_saude,
                hide_index=True,
                width="stretch",
            )
        with col_s2:
            if not df_saude.empty:
                grafico_saude = df_saude.set_index("Categoria")[["Casos"]]
                st.bar_chart(grafico_saude, horizontal=False)

    # --------------------------------------------------------------------
    # 4 · Top variações + gráfico de barras
    # --------------------------------------------------------------------
    st.markdown("#### Variações em destaque")
    top_list = list(getattr(v2, "top_variacoes", []) or [])
    agrupadores = list(v2.agrupadores_aplicados or [])
    if not top_list:
        st.caption("Nenhuma variação significativa para destacar.")
    else:
        # Headers user-facing: traduz cada agrupador (ex: "Centro_Custo" →
        # "Centro de Custo") antes de construir o DataFrame · headers e
        # formatos consomem unidade (P-29).
        agrupadores_ui = {a: _rotular_agrupador_ui(a) for a in agrupadores}
        rot_dif = rotulo_diferenca(unidade)
        rot_var = rotulo_variacao(unidade)
        linhas = []
        for t in top_list:
            chave = getattr(t, "chave_agrupadores", {}) or {}
            if not isinstance(chave, dict):
                chave = {}
            linha = {agrupadores_ui[a]: str(chave.get(a, "—")) for a in agrupadores}
            linha[f"Valor · {origem}"] = getattr(t, "valor_origem", None)
            linha[f"Valor · {comparado}"] = getattr(t, "valor_comparado", None)
            dif_raw = getattr(t, "diferenca", None)
            # Para PERCENTUAL · diferença é fração (-0.05); multiplicamos por
            # 100 para que o format string +%.2f p.p renderize "-5,00 p.p"
            # (espelha valor_diferenca_para_celula no Excel).
            if dif_raw is not None and unidade == "PERCENTUAL":
                linha[rot_dif] = float(dif_raw) * 100.0
            else:
                linha[rot_dif] = dif_raw
            linha[rot_var] = getattr(t, "variacao_percentual", None)
            linhas.append(linha)
        df_top = pd.DataFrame(linhas)
        column_config = {}
        for a in agrupadores:
            col_ui = agrupadores_ui[a]
            column_config[col_ui] = st.column_config.TextColumn(col_ui)
        # Format para colunas de Valor · adapta por unidade
        if unidade == "MONETARIO_BRL":
            fmt_valor = "R$ %.2f"
        elif unidade == "PERCENTUAL":
            fmt_valor = "%.2f%%"
        elif unidade == "QUANTIDADE":
            fmt_valor = "%d"
        elif unidade == "TEMPO_DIAS":
            fmt_valor = "%d dias"
        elif unidade == "TEMPO_HORAS":
            fmt_valor = "%d h"
        elif unidade == "MULTIPLICADOR":
            fmt_valor = "%.2fx"
        elif unidade == "RAZAO":
            fmt_valor = "%.4f"
        else:
            fmt_valor = "%.2f"
        for col_val in (f"Valor · {origem}", f"Valor · {comparado}"):
            if col_val in df_top.columns:
                column_config[col_val] = st.column_config.NumberColumn(
                    col_val, format=fmt_valor,
                )
        # Format para coluna Diferença · MONETARIO/QUANTIDADE seguem fmt_valor;
        # PERCENTUAL usa "+%.2f p.p" sobre o valor já multiplicado por 100.
        if rot_dif in df_top.columns:
            if unidade == "PERCENTUAL":
                fmt_dif = "%+.2f p.p"
            else:
                fmt_dif = fmt_valor
            column_config[rot_dif] = st.column_config.NumberColumn(
                rot_dif, format=fmt_dif,
            )
        if rot_var in df_top.columns:
            column_config[rot_var] = st.column_config.NumberColumn(
                rot_var, format="%.2f%%",
            )
        st.dataframe(
            df_top, column_config=column_config, hide_index=True, width="stretch",
        )
        # Barras horizontais · diferença por combinação · rótulos traduzidos
        df_barras = pd.DataFrame({
            "Combinação": [
                " · ".join(
                    str((getattr(t, "chave_agrupadores", {}) or {}).get(a, "—"))
                    for a in agrupadores
                )
                for t in top_list
            ],
            "Diferença": [getattr(t, "diferenca", 0) or 0 for t in top_list],
        }).set_index("Combinação")
        st.bar_chart(df_barras, horizontal=True)

    # --------------------------------------------------------------------
    # 5 · Leitura qualitativa + qualidade
    # --------------------------------------------------------------------
    st.markdown("#### Leitura qualitativa")
    classif = v2.resumo_executivo.bloco_5_leitura_qualitativa.classificacao_ativa
    leituras_ux = {
        "Melhoria Geral": "A comparação indica melhoria geral na maior parte dos casos.",
        "Deterioração Geral": "A comparação indica deterioração na maior parte dos casos.",
        "Resultado Misto": "O resultado é misto · há ganhos e perdas distribuídos entre os casos.",
        "Resultado Estável": "A maior parte dos casos ficou estável entre os dois lados.",
        "Alta Taxa de Mudança de Estado": "A maior parte das combinações mudou de estado.",
        "Mudanças Parciais": "Algumas combinações mudaram de estado · a maior parte permaneceu.",
        "Estados Estáveis": "Os estados permaneceram estáveis na maior parte das combinações.",
    }
    st.write(leituras_ux.get(classif, "A análise foi concluída com sucesso."))

    qualidade = v2.resumo_executivo.bloco_6_qualidade_estrutural
    total_av = int(qualidade.total_warnings or 0)
    if total_av == 0:
        st.info("Nenhum aviso estrutural gerado nesta análise.")
    else:
        plural = "s" if total_av != 1 else ""
        st.info(
            f"A análise gerou {total_av:,}".replace(",", ".")
            + f" aviso{plural} estrutural{'is' if plural else ''}. "
            "Nenhum bloqueio foi escapado."
        )

    with st.expander("Ver detalhes do diagnóstico"):
        agrupadores_traduzidos = [_rotular_agrupador_ui(a) for a in agrupadores]
        st.markdown("**Agrupadores aplicados:** " + (", ".join(agrupadores_traduzidos) if agrupadores else "—"))
        st.markdown(f"**Campo analisado:** {comp.campo_analisado or '—'}")
        tipo_labels = {
            "NUMERICO_ADITIVO": "Valor somável",
            "NUMERICO_RELATIVO": "Valor percentual ou taxa",
            "NUMERICO_NAO_ADITIVO": "Indicador não somável",
            "ESTADO_SITUACAO": "Categoria ou rótulo",
        }
        st.markdown(f"**Tipo de medida:** {tipo_labels.get(comp.tipo_campo, comp.tipo_campo)}")
        por_cat = dict(qualidade.warnings_por_categoria or {})
        if por_cat:
            st.markdown("**Avisos por categoria:**")
            cat_labels = {
                "informativo": "Informativo",
                "ajuste_leve": "Ajuste automático",
                "alerta_estrutural_leve": "Alerta estrutural leve",
                "alerta_estrutural": "Alerta estrutural",
                "decisao_usuario": "Decisão do usuário",
                "escape_acionado": "Escape acionado",
            }
            for cat, qtd in por_cat.items():
                st.markdown(f"- {cat_labels.get(cat, cat)}: **{qtd}**")

    # --------------------------------------------------------------------
    # Rodapé · Voltar · Paleta · Baixar (D-175 · §5.3 · §5.4)
    # --------------------------------------------------------------------
    st.divider()
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("← Voltar", key="btn_voltar_resultado"):
            st.session_state["etapa"] = "E5"
            st.rerun()
    with c2:
        # Paleta · troca livre a qualquer momento · lida no clique do download
        paleta_atual = st.session_state.get("paleta_selecionada", PALETA_DEFAULT)
        idx = (PALETAS_DISPONIVEIS.index(paleta_atual)
               if paleta_atual in PALETAS_DISPONIVEIS else 0)
        st.selectbox(
            "Paleta do Excel",
            PALETAS_DISPONIVEIS,
            index=idx,
            key="paleta_selecionada",
            help="Escolha a paleta antes de baixar. A troca é livre e não exige reprocessar.",
        )
    with c3:
        _render_botao_download_excel(key_sufixo="resultado")

    # Botão "Nova análise" em linha à parte
    if st.button("🔄 Nova análise", key="btn_nova_resultado"):
        _reset_completo()
        st.rerun()


def _fmt_moeda_br(valor) -> str:
    """Moeda BR user-facing para st.metric · '—' quando None."""
    if valor is None:
        return "—"
    try:
        n = float(valor)
    except (TypeError, ValueError):
        return "—"
    neg = n < 0
    n = abs(n)
    inteiro = int(n)
    centavos = round((n - inteiro) * 100)
    if centavos == 100:
        inteiro += 1
        centavos = 0
    inteiro_str = f"{inteiro:,}".replace(",", ".")
    texto = f"R$ {inteiro_str},{centavos:02d}"
    return f"-{texto}" if neg else texto


def _fmt_pct_br(valor) -> str:
    """Percentual BR user-facing · '—' quando None · assume fração (0.14 → 14,00%)."""
    if valor is None:
        return "—"
    try:
        n = float(valor) * 100
    except (TypeError, ValueError):
        return "—"
    return f"{n:.2f}%".replace(".", ",")


def _render_botao_download_excel(key_sufixo: str = "") -> None:
    """
    Download do Excel V2 · paleta lida do session_state NO MOMENTO DO CLIQUE
    (D-175 · §5.4 · corrige bug de paleta congelada). Excel é regenerado
    quando a paleta muda; caso contrário, usa cache por chave composta.
    """
    v2: V2Result = st.session_state["v2_result"]
    paleta_nome = st.session_state.get("paleta_selecionada", PALETA_DEFAULT)

    # Cache por (paleta, v2_id) · regenera quando paleta troca
    chave_cache = f"caminho_excel_{paleta_nome}_{id(v2)}"
    caminho_cache = st.session_state.get(chave_cache)
    if not caminho_cache or not Path(caminho_cache).exists():
        try:
            comp = v2.comparacao_realizada
            origem_ux = comp.origem_rotulo_ux or comp.origem_rotulo_tecnico or "origem"
            comparado_ux = comp.comparado_rotulo_ux or comp.comparado_rotulo_tecnico or "comparado"
            tmpdir = tempfile.mkdtemp(prefix="tabloflow_v2_exp_")
            # Caminho provisório · exportar_resultado_v2 reescreve com nome executivo
            caminho_provisorio = str(Path(tmpdir) / "provisorio.xlsx")
            resultado = exportar_resultado_v2(
                v2_result=v2,
                caminho_saida=caminho_provisorio,
                paleta_nome=paleta_nome.lower(),
                origem_rotulo=origem_ux,
                comparado_rotulo=comparado_ux,
                arquivo_nome_origem=st.session_state.get("nome_arquivo"),
                aba_consumida=st.session_state.get("aba_selecionada"),
                usar_nome_executivo=True,
            )
            caminho_cache = resultado.caminho_arquivo
            st.session_state[chave_cache] = caminho_cache
            # Backward-compat · testes legados leem esta chave direta
            st.session_state["caminho_excel_exportado"] = caminho_cache
        except Exception as exc:  # noqa: BLE001
            st.error(f"Falha na exportação: {exc}")
            return
    with open(caminho_cache, "rb") as f:
        data = f.read()
    chave_btn = f"dl_excel_{key_sufixo}" if key_sufixo else "dl_excel"
    st.download_button(
        "📥 Baixar Excel",
        data=data,
        file_name=Path(caminho_cache).name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=chave_btn,
        type="primary",
    )


# ---------------------------------------------------------------------------
# Tela 10 · ERRO
# ---------------------------------------------------------------------------


def _tela_erro() -> None:
    st.subheader("Não foi possível continuar")
    v2: Optional[V2Result] = st.session_state.get("v2_result")
    bloqueios: List[BloqueioOperacional] = []
    if v2 is not None:
        bloqueios = list(v2.bloqueios_disparados)
    motor_result: Optional[MotorResult] = st.session_state.get("motor_result")
    if not bloqueios and motor_result is not None:
        bloqueios = list(motor_result.bloqueios)

    if not bloqueios:
        erro_proc = st.session_state.get("_erro_processamento")
        if erro_proc:
            st.error(f"Erro inesperado no pipeline: {erro_proc}")
        else:
            st.error("Erro desconhecido.")
    for b in bloqueios:
        mensagem = _traduzir_bloqueio(b)
        st.error(mensagem)
        with st.expander("Detalhes técnicos (para revisão pela Usuária construtora)"):
            st.markdown(f"Código técnico: `{b.codigo}`")
            st.markdown(f"Condição: {b.condicao_disparo}")
            st.json(b.contexto_disparo)

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Voltar à etapa anterior", key="btn_voltar_erro"):
            if st.session_state.get("motor_result") is None:
                st.session_state["etapa"] = "vazio"
            else:
                st.session_state["etapa"] = "E5"
            st.rerun()
    with c2:
        if st.button("Nova análise", key="btn_nova_erro"):
            _reset_completo()
            st.rerun()


# Microcopy user-facing de bloqueios V2 · P-V2 §2.8 (10 bloqueios declarados)
_BLOQUEIOS_MICROCOPY: Dict[str, str] = {
    "B-V2-ARQUIVO-ILEGIVEL": (
        "Não foi possível ler o arquivo · formato não suportado ou arquivo corrompido. "
        "Verifique o arquivo e tente novamente."
    ),
    "B-V2-ESTRUTURA-INVALIDA": (
        "A aba escolhida não tem dados ou não tem coluna numérica esperada. "
        "Verifique a aba e selecione outra se necessário."
    ),
    "B-V2-DISCRIMINADOR-0": (
        "A coluna de comparação está vazia · não é possível comparar. "
        "Escolha outra coluna ou outra aba."
    ),
    "B-V2-DISCRIMINADOR-1": (
        "A coluna de comparação tem apenas 1 valor único · não é possível comparar "
        "dois estados. Escolha outra coluna."
    ),
    "B-V2-CAMPO-100-NULO": (
        "O campo analisado está totalmente vazio · não é possível calcular. "
        "Escolha outro campo."
    ),
    "B-V2-AGRUP-EXCESSO": (
        "Você selecionou agrupadores acima do máximo de 9. Para cruzamento "
        "multidimensional considere uma análise diferente."
    ),
    "B-V2-PESO-INVALIDO": (
        "O campo de peso escolhido tem todos os valores zero ou negativos · "
        "não é possível calcular média ponderada. Escolha outro campo de peso."
    ),
    "B-V2-CONSOL-IMPOSSIVEL": (
        "Você escolheu não consolidar mas declarou agrupadores · não é possível "
        "processar. Remova os agrupadores ou escolha outro método de consolidação."
    ),
    "B-V2-RESULTADO-EXCEDE": (
        "A análise gera mais de 500.000 linhas no resultado · acima do limite "
        "operacional. Reduza agrupadores ou aplique filtros prévios."
    ),
    "B-V2-CASO-ESTRUTURAL-CANCELADO": (
        "Análise cancelada por sua escolha no painel de resolução de caso "
        "estrutural. Ajuste a configuração e tente novamente."
    ),
}


def _traduzir_bloqueio(b: BloqueioOperacional) -> str:
    """Traduz código técnico de bloqueio para mensagem user-facing (P-V2 §2.8)."""
    return _BLOQUEIOS_MICROCOPY.get(b.codigo, b.condicao_disparo)


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------


def _dispatch() -> None:
    etapa = st.session_state["etapa"]
    if etapa == "vazio":
        _tela_vazio()
    elif etapa == "E1_OK":
        _tela_e1_ok()
    elif etapa == "E2":
        _tela_e2()
    elif etapa == "E3":
        _tela_e3()
    elif etapa == "E4":
        _tela_e4()
    elif etapa == "RESOL_CASO":
        # Tela 5 · não acionada automaticamente no fluxo atual (motor não pré-detecta
        # casos estruturais · C.3 · não inventar). Mantida no dispatcher para uso futuro.
        st.info("Resolução estrutural · não acionada no fluxo atual.")
        if st.button("Voltar a E4", key="btn_skip_resol"):
            st.session_state["etapa"] = "E4"
            st.rerun()
    elif etapa == "E5":
        _tela_e5()
    elif etapa == "PROCESSANDO":
        # Etapa transitória · pipeline executa em _tela_e5 ao clicar em "Processar".
        # Se alguém cair aqui, executa e redireciona.
        _executar_pipeline_v2()
        st.rerun()
    elif etapa == "RESULTADO":
        _tela_resultado()
    elif etapa == "CHECKLIST":
        # D-177 · checklist VVC removido da superfície cliente · redirect silencioso
        st.session_state["etapa"] = "RESULTADO"
        _tela_resultado()
    elif etapa == "ERRO":
        _tela_erro()
    else:
        st.error(f"Etapa desconhecida: {etapa}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    st.set_page_config(page_title="TabloFlow · V2", layout="wide")
    _init_state()
    _render_header()
    # Expander TED no topo após o header · apenas em etapas pós-upload
    # (na tela 'vazio' não faz sentido mostrar, ainda não há análise)
    if st.session_state.get("etapa") not in ("vazio",):
        _render_expander_ted()
    _dispatch()


main()
