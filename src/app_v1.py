"""
app_v1.py — V1 · Conciliação de Bases · Streamlit
Bloco A-V1 · 4º artefato do ciclo §15.1 (Fase 2).

Orquestra a sequência canônica:
    motor_upload.processar_upload  →  motor_base.processar_base  →  executar_v1
                                                                  →  exportar_resultado_v1

O app NUNCA calcula · NUNCA infere classificação · NUNCA reconstrói leitura
qualitativa. Toda leitura analítica vem de ConciliacaoV1Result (C.3 · Lei 1
do prompt A-V1). Espelha estruturalmente `app_v2.py` (canônico · suite verde).
"""
from __future__ import annotations

import json
import sys
import tempfile
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Path setup (permite execução via `streamlit run src/app_v1.py`)
# ---------------------------------------------------------------------------
_SRC_DIR = Path(__file__).resolve().parent
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from contratos import (  # noqa: E402
    ArquivoInfo,
    BloqueioOperacional,
    MotorResult,
    UploadResult,
)
from motor_base import processar_base  # noqa: E402
from motor_upload import ArquivoEntrada, processar_upload  # noqa: E402
from apresentacao.formatos import (  # noqa: E402
    formatar_diferenca_por_unidade,
    formatar_percentual_br,
    formatar_valor_por_unidade,
)
from visoes.exportacao_v1 import exportar_resultado_v1  # noqa: E402
from visoes.visao_v1 import (  # noqa: E402
    AgrupadorMatchV1,
    CampoComparadoV1,
    CasoLogicoV1,
    ClassificacaoRegistroV1,
    ConciliacaoV1Result,
    DEFAULT_EPSILON_POR_UNIDADE,
    DEFAULT_UNIDADE_POR_TIPO,
    ModoMatchV1,
    StatusPonteV1,
    TipoCampoV1,
    UnidadeCanonica,
    executar_v1,
)


# ---------------------------------------------------------------------------
# Constantes user-facing (P-V1 §2.7 · D-212)
# ---------------------------------------------------------------------------

ETAPAS_STEPPER = [
    "1 · Escolher arquivo(s)",
    "2 · Identificar lados",
    "3 · Configurar análise",
    "4 · Agrupadores executivos",
    "Revisar e executar",
]

ETAPA_ORDEM = [
    "vazio",
    "E1_OK",
    "E2",
    "E3",
    "E4",
    "E5",
    "PROCESSANDO",
    "RESULTADO",
    "ERRO",
]

# Tipos de campo · S-V1 §1.7 · 7 valores
TIPOS_CAMPO_V1: List[Tuple[str, str]] = [
    ("VALOR_MONETARIO", "Valor financeiro (receita, custo, valor contábil)"),
    ("QUANTIDADE", "Quantidade absoluta"),
    ("VOLUME", "Volume (litros, kg, m³)"),
    ("PERCENTUAL", "Percentual ou taxa (margem %, taxa, índice)"),
    ("PRAZO", "Prazo em dias"),
    ("INDICE", "Índice ou multiplicador"),
    ("ESTADO_SITUACAO", "Categoria ou rótulo (status, classificação)"),
]

# Modos de match · S-V1 §1.5 · 4 valores
MODOS_MATCH_V1: List[Tuple[str, str]] = [
    ("EXATO", "Exato (igualdade total)"),
    ("CONTEM", "Contém"),
    ("INICIA_COM", "Inicia com"),
    ("TERMINA_COM", "Termina com"),
]

# Unidades canônicas · S-V1 §1.22 · 8 valores
UNIDADES_V1: List[Tuple[str, str]] = [
    ("MONETARIO_BRL", "Reais (R$)"),
    ("PERCENTUAL", "Percentual (%)"),
    ("QUANTIDADE", "Quantidade absoluta"),
    ("TEMPO_DIAS", "Tempo em dias"),
    ("TEMPO_HORAS", "Tempo em horas"),
    ("MULTIPLICADOR", "Multiplicador (x)"),
    ("RAZAO", "Razão (decimal)"),
    ("ADIMENSIONAL", "Outro / sem unidade definida"),
]

# Paletas executivas · P-V1 §1 · D-168 · default Azul
PALETAS_DISPONIVEIS = ["Azul executivo", "Cinza executivo", "Verde executivo", "Vinho executivo"]
PALETA_DEFAULT = "Azul executivo"

# Mapa de paleta user-facing → nome técnico passado a exportar_resultado_v1
PALETA_TECH = {
    "Azul executivo": "azul",
    "Cinza executivo": "cinza",
    "Verde executivo": "verde",
    "Vinho executivo": "vinho",
}

# Defaults TED · S-V1 §2.8
THRESHOLDS_DEFAULT_V1: Dict[str, Any] = {
    "chave_nulos_max": 0.50,
    "volume_max": 500_000,
    "concentracao_agrupador_principal_min": 0.70,
}


# Chaves de session_state por etapa (para invalidação cascata · S-V1 §3.12)
CHAVES_E1_OK: List[str] = [
    "abas_origem_disponiveis",
    "abas_comparado_disponiveis",
    "aba_escolhida_unica_caso1",
    "abas_escolhidas_caso1_2abas",
    "aba_origem_caso2",
    "aba_comparado_caso2",
    "motor_result",
]
CHAVES_E2: List[str] = ["origem_ux", "comparado_ux"]
CHAVES_E3: List[str] = [
    "agrupadores_match",
    "campos_comparados",
    "n_agrupadores_visiveis",
    "n_campos_visiveis",
    "caso_logico_inferido",
]
CHAVES_E4: List[str] = ["agrupadores_executivos"]
CHAVES_E5: List[str] = ["v1_result", "_excel_cache_keys", "_erro_msg"]


# Conjunto de chaves do session_state que compõem um modelo T-MODELO (V1).
# Não inclui v1_result · motor_result · upload_result · hashes · flags UX.
_MODELO_CHAVES_V1: List[str] = [
    "n_arquivos",
    "origem_ux",
    "comparado_ux",
    "agrupadores_match",
    "campos_comparados",
    "agrupadores_executivos",
    "ted_chave_nulos_max",
    "ted_volume_max",
    "ted_concentracao_agrupador_min",
]


# ---------------------------------------------------------------------------
# Session state helpers (S-V1 §3.12 · invalidação cascata)
# ---------------------------------------------------------------------------


def _init_state() -> None:
    """Inicializa st.session_state com defaults V1."""
    defaults: Dict[str, Any] = {
        "etapa": "vazio",
        # E0 · upload físico
        "n_arquivos": 1,
        "upload_unico_bytes": None,
        "upload_unico_nome": "",
        "upload_origem_bytes": None,
        "upload_origem_nome": "",
        "upload_comparado_bytes": None,
        "upload_comparado_nome": "",
        "upload_result": None,
        # E1_OK · escolha de aba(s)
        "abas_origem_disponiveis": [],
        "abas_comparado_disponiveis": [],
        "aba_escolhida_unica_caso1": None,
        "abas_escolhidas_caso1_2abas": [],
        "aba_origem_caso2": None,
        "aba_comparado_caso2": None,
        "motor_result": None,
        # E2 · rótulos amigáveis
        "origem_ux": "",
        "comparado_ux": "",
        # E3 · agrupadores match (1-5) e campos comparados (1-10)
        "agrupadores_match": [],
        "campos_comparados": [],
        "n_agrupadores_visiveis": 1,
        "n_campos_visiveis": 1,
        "caso_logico_inferido": None,
        # E4 · agrupadores executivos (0-5)
        "agrupadores_executivos": [],
        # TED widgets (persistem)
        "ted_chave_nulos_max": float(THRESHOLDS_DEFAULT_V1["chave_nulos_max"]),
        "ted_volume_max": int(THRESHOLDS_DEFAULT_V1["volume_max"]),
        "ted_concentracao_agrupador_min": float(
            THRESHOLDS_DEFAULT_V1["concentracao_agrupador_principal_min"]
        ),
        # Resultado
        "v1_result": None,
        "_excel_cache_keys": [],  # lista de cache_keys atualmente populados
        "_erro_msg": "",
        # Paleta · D-175 · rodapé do RESULTADO
        "paleta_selecionada": PALETA_DEFAULT,
        # Header flags
        "_show_objetivo": False,
        "_show_aplicar_modelo": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _invalidar_a_partir(etapa_alvo: str) -> None:
    """Invalida estado downstream conforme S-V1 §3.12."""
    ordem = {"E1_OK": 1, "E2": 2, "E3": 3, "E4": 4, "E5": 5}
    if etapa_alvo not in ordem:
        return
    n = ordem[etapa_alvo]
    mapa = {1: CHAVES_E1_OK, 2: CHAVES_E2, 3: CHAVES_E3, 4: CHAVES_E4, 5: CHAVES_E5}

    defaults: Dict[str, Any] = {
        "abas_origem_disponiveis": [],
        "abas_comparado_disponiveis": [],
        "aba_escolhida_unica_caso1": None,
        "abas_escolhidas_caso1_2abas": [],
        "aba_origem_caso2": None,
        "aba_comparado_caso2": None,
        "motor_result": None,
        "origem_ux": "",
        "comparado_ux": "",
        "agrupadores_match": [],
        "campos_comparados": [],
        "n_agrupadores_visiveis": 1,
        "n_campos_visiveis": 1,
        "caso_logico_inferido": None,
        "agrupadores_executivos": [],
        "v1_result": None,
        "_excel_cache_keys": [],
        "_erro_msg": "",
    }
    for n_etapa in range(n, 6):
        for k in mapa[n_etapa]:
            if k in defaults:
                st.session_state[k] = defaults[k]
    # Também limpa cache de Excel quando invalidamos qualquer downstream
    _limpar_cache_excel()


def _reset_completo(preservar_modelo: bool = True) -> None:
    """Reset preservando T-MODELO em memória · espelho V2."""
    for k in list(st.session_state.keys()):
        if preservar_modelo and str(k).startswith("_modelo_"):
            continue
        del st.session_state[k]
    _init_state()


def _limpar_cache_excel() -> None:
    """Remove todas as chaves de cache do Excel gerado."""
    chaves_existentes = list(st.session_state.get("_excel_cache_keys", []))
    for k in chaves_existentes:
        if k in st.session_state:
            del st.session_state[k]
    st.session_state["_excel_cache_keys"] = []


# ---------------------------------------------------------------------------
# T-MODELO · serialização leve (CASO A · espelho V2)
# ---------------------------------------------------------------------------


def _modelo_atual_bytes() -> bytes:
    """Serializa configuração corrente como JSON (para download)."""
    payload: Dict[str, Any] = {"_modelo_versao": 1, "_visao": "V1"}
    for k in _MODELO_CHAVES_V1:
        v = st.session_state.get(k)
        if isinstance(v, list):
            v_serial = []
            for item in v:
                if isinstance(item, dict):
                    item_copy = {}
                    for ik, iv in item.items():
                        if isinstance(iv, Decimal):
                            item_copy[ik] = str(iv)
                        else:
                            item_copy[ik] = iv
                    v_serial.append(item_copy)
                else:
                    v_serial.append(item)
            v = v_serial
        elif isinstance(v, dict):
            v = dict(v)
        elif isinstance(v, Decimal):
            v = str(v)
        payload[k] = v
    return json.dumps(payload, ensure_ascii=False, indent=2, default=str).encode("utf-8")


def _aplicar_modelo_bytes(data: bytes) -> None:
    """Lê bytes JSON e popula session_state V1 · valida estrutura mínima."""
    modelo = json.loads(data.decode("utf-8"))
    if not isinstance(modelo, dict):
        raise ValueError("Modelo inválido · não é um objeto JSON.")
    if modelo.get("_visao") not in (None, "V1"):
        raise ValueError(
            f"Modelo é da visão {modelo.get('_visao')!r} · esperado V1."
        )
    for k in _MODELO_CHAVES_V1:
        if k in modelo:
            st.session_state[k] = modelo[k]
    # Re-popula contadores visíveis quando aplicável
    if "agrupadores_match" in modelo and isinstance(modelo["agrupadores_match"], list):
        st.session_state["n_agrupadores_visiveis"] = max(1, len(modelo["agrupadores_match"]))
    if "campos_comparados" in modelo and isinstance(modelo["campos_comparados"], list):
        st.session_state["n_campos_visiveis"] = max(1, len(modelo["campos_comparados"]))


# ---------------------------------------------------------------------------
# Header persistente · 4 botões + Stepper · espelho V2 (S-V1 §3.2)
# ---------------------------------------------------------------------------


def _render_header() -> None:
    """Header persistente · S-V1 §3.2 · 4 botões + stepper."""
    st.title("V1 · Conciliação de Bases")

    col_obj, col_mod_aplic, col_mod_salv, col_new = st.columns([1, 1, 1, 1])
    with col_obj:
        if st.button("Objetivo da Visão", key="btn_objetivo"):
            st.session_state["_show_objetivo"] = not st.session_state.get(
                "_show_objetivo", False
            )
    with col_mod_aplic:
        if st.button(
            "Aplicar modelo",
            key="btn_aplicar_modelo",
            disabled=st.session_state["etapa"] == "vazio",
        ):
            st.session_state["_show_aplicar_modelo"] = True
    with col_mod_salv:
        etapa = st.session_state["etapa"]
        idx_etapa = ETAPA_ORDEM.index(etapa) if etapa in ETAPA_ORDEM else 0
        st.download_button(
            "Salvar como modelo",
            data=_modelo_atual_bytes(),
            file_name="tabloflow_modelo_v1.json",
            mime="application/json",
            key="btn_salvar_modelo",
            disabled=idx_etapa < ETAPA_ORDEM.index("E5"),
        )
    with col_new:
        if st.button("Nova análise", key="btn_nova_analise"):
            _reset_completo()
            st.rerun()

    if st.session_state.get("_show_objetivo", False):
        with st.expander("Objetivo da V1", expanded=True):
            # Microcopy literal de S-V1 §3.2
            st.markdown(
                "**O que faz:** confronta duas bases (Origem × Comparado) e responde "
                "se elas representam o mesmo universo de dados.\n\n"
                "**Quando usar:** Conciliação contábil mensal · Sistema A × Sistema B · "
                "validação de migração · auditoria de integração · conciliação bancária.\n\n"
                "**O que obtém:** Taxa de Conciliação · Mapa de Conciliação · "
                "Análise Analítica por campo · Ponte de Conciliação · Diagnóstico estrutural.\n\n"
                "**Como funciona:** você sobe 1 ou 2 arquivos · escolhe abas · identifica "
                "lados · declara agrupadores de match e campos comparados. O motor casa "
                "registros (modo exato/contém/inicia/termina) ou trata como pares já "
                "casados quando você aponta colunas distintas da mesma aba · classifica "
                "em 6 categorias (ou 2 reduzidas) · gera Excel executivo de 6 abas."
            )

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
                    "Confirmar aplicação",
                    key="btn_confirmar_aplicar_modelo",
                    type="primary",
                ):
                    try:
                        _aplicar_modelo_bytes(arquivo_modelo.getvalue())
                        st.session_state["_show_aplicar_modelo"] = False
                        st.success("Modelo aplicado · revise as etapas e prossiga.")
                        st.rerun()
                    except Exception as exc:  # noqa: BLE001
                        st.error(f"Falha ao aplicar modelo: {exc}")
            with col_apl_b:
                if st.button("Cancelar", key="btn_cancelar_aplicar_modelo"):
                    st.session_state["_show_aplicar_modelo"] = False
                    st.rerun()

    # Stepper · 5 etapas
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


def _indice_stepper() -> int:
    """Mapeia etapa atual para índice 0-4 do stepper · 5 etapas V1."""
    etapa = st.session_state["etapa"]
    if etapa in ("vazio", "E1_OK"):
        return 0
    if etapa == "E2":
        return 1
    if etapa == "E3":
        return 2
    if etapa == "E4":
        return 3
    if etapa in ("E5", "PROCESSANDO", "RESULTADO"):
        return 4
    return 0


# ---------------------------------------------------------------------------
# TED · expander "⚙️ Configurações avançadas" no topo (D-178 · S-V1 §3.3)
# ---------------------------------------------------------------------------


def _unidades_em_uso_atual() -> List[UnidadeCanonica]:
    """Extrai unidades efetivamente declaradas em st.session_state['campos_comparados']."""
    campos = st.session_state.get("campos_comparados", []) or []
    unidades_set = set()
    for c in campos:
        if isinstance(c, dict):
            u = c.get("unidade")
            if u:
                try:
                    unidades_set.add(UnidadeCanonica(u))
                except ValueError:
                    continue
    # Ordem canônica para estabilidade visual
    return [u for u in UnidadeCanonica if u in unidades_set]


def _render_expander_ted() -> None:
    """TED · S-V1 §3.3 · D-178."""
    with st.expander("⚙️ Configurações avançadas", expanded=False):
        st.caption(
            "Edições aqui afetam apenas a leitura qualitativa do Resumo Executivo "
            "e tolerâncias de fechamento da Ponte. Cálculos principais (Match, "
            "Classificação) não são afetados."
        )
        col_a, col_b = st.columns(2)
        with col_a:
            st.number_input(
                "Limite de células vazias em coluna de chave",
                min_value=0.0,
                max_value=1.0,
                step=0.01,
                format="%.2f",
                key="ted_chave_nulos_max",
                help=(
                    "Acima deste percentual de nulos em coluna usada como agrupador, "
                    "o sistema alerta (B-V1-CHAVE-INVALIDA · escapável)."
                ),
            )
            st.number_input(
                "Limite de registros processados",
                min_value=1_000,
                max_value=5_000_000,
                step=10_000,
                key="ted_volume_max",
                help=(
                    "Acima deste volume, sistema bloqueia execução "
                    "(B-V1-RESULTADO-EXCEDE · escapável via ECP)."
                ),
            )
        with col_b:
            st.number_input(
                "Limite de concentração para citar agrupador principal",
                min_value=0.0,
                max_value=1.0,
                step=0.05,
                format="%.2f",
                key="ted_concentracao_agrupador_min",
                help=(
                    "Concentração mínima da divergência para mencionar agrupador "
                    "principal na leitura qualitativa."
                ),
            )

        unidades_em_uso = _unidades_em_uso_atual()
        if unidades_em_uso:
            st.markdown(
                "**Épsilon por unidade** · tolerância para fechamento da Ponte (D-211)"
            )
            for unidade in unidades_em_uso:
                key_eps = f"ted_eps_{unidade.value}"
                if key_eps not in st.session_state:
                    st.session_state[key_eps] = float(
                        DEFAULT_EPSILON_POR_UNIDADE[unidade]
                    )
                st.number_input(
                    f"Épsilon · {unidade.value}",
                    min_value=0.0,
                    step=0.0001,
                    format="%.4f",
                    key=key_eps,
                )


# ---------------------------------------------------------------------------
# Helpers de upload físico · usados em _tela_vazio e _tela_e1_ok
# ---------------------------------------------------------------------------


def _persistir_bytes_temp(nome_original: str, bytes_dados: bytes) -> str:
    """Grava bytes em arquivo temporário e retorna o caminho físico."""
    suffix = "." + nome_original.rsplit(".", 1)[-1].lower()
    tmp = tempfile.NamedTemporaryFile(
        delete=False, suffix=suffix, prefix="tabloflow_v1_"
    )
    tmp.write(bytes_dados)
    tmp.flush()
    tmp.close()
    return tmp.name


def _abas_de_arquivo(info: ArquivoInfo) -> List[str]:
    """Retorna abas disponíveis · '' (CSV) → ['(arquivo único · CSV)']."""
    abas = list(info.abas_disponiveis or [])
    if not abas:
        return []
    return abas


# ---------------------------------------------------------------------------
# Construção da config a partir de st.session_state (consumida por executar_v1)
# ---------------------------------------------------------------------------


def _construir_agrupadores_match() -> List[AgrupadorMatchV1]:
    """Converte lista de dicts em st.session_state para AgrupadorMatchV1."""
    out: List[AgrupadorMatchV1] = []
    for d in st.session_state.get("agrupadores_match", []) or []:
        if not isinstance(d, dict):
            continue
        rotulo = d.get("rotulo_analitico") or d.get("nome_origem") or ""
        out.append(
            AgrupadorMatchV1(
                nome_origem=d.get("nome_origem", ""),
                nome_comparado=d.get("nome_comparado", ""),
                rotulo_analitico=rotulo,
                modo_match=ModoMatchV1(d.get("modo_match", "EXATO")),
            )
        )
    return out


def _construir_campos_comparados() -> List[CampoComparadoV1]:
    """Converte lista de dicts em st.session_state para CampoComparadoV1."""
    out: List[CampoComparadoV1] = []
    for d in st.session_state.get("campos_comparados", []) or []:
        if not isinstance(d, dict):
            continue
        nome = d.get("nome_analitico") or d.get("nome_origem") or ""
        tipo_str = d.get("tipo_logico", "VALOR_MONETARIO")
        unidade_str = d.get(
            "unidade",
            DEFAULT_UNIDADE_POR_TIPO[TipoCampoV1(tipo_str)].value,
        )
        tol = d.get("tolerancia", "0")
        try:
            tol_dec = Decimal(str(tol))
        except Exception:
            tol_dec = Decimal("0")
        out.append(
            CampoComparadoV1(
                nome_origem=d.get("nome_origem", ""),
                nome_comparado=d.get("nome_comparado", ""),
                nome_analitico=nome,
                tipo_logico=TipoCampoV1(tipo_str),
                unidade=UnidadeCanonica(unidade_str),
                tolerancia=tol_dec,
            )
        )
    return out


def _construir_epsilon_por_unidade() -> Dict[UnidadeCanonica, Decimal]:
    """Coleta os valores TED epsilon por unidade efetivamente em uso."""
    eps: Dict[UnidadeCanonica, Decimal] = {}
    for unidade in _unidades_em_uso_atual():
        key_eps = f"ted_eps_{unidade.value}"
        valor_widget = st.session_state.get(key_eps)
        if valor_widget is None:
            valor_widget = float(DEFAULT_EPSILON_POR_UNIDADE[unidade])
        try:
            eps[unidade] = Decimal(str(valor_widget))
        except Exception:
            eps[unidade] = DEFAULT_EPSILON_POR_UNIDADE[unidade]
    return eps


def _construir_config_v1() -> Dict[str, Any]:
    """Monta o dict canônico consumido por `executar_v1`."""
    n_arq = int(st.session_state.get("n_arquivos", 1))
    if n_arq == 1:
        nome_arq = st.session_state.get("upload_unico_nome", "")
        arquivo_origem = nome_arq
        arquivo_comparado = nome_arq
        if st.session_state.get("aba_escolhida_unica_caso1"):
            aba_origem = st.session_state["aba_escolhida_unica_caso1"]
            aba_comparado = st.session_state["aba_escolhida_unica_caso1"]
        else:
            abas = list(st.session_state.get("abas_escolhidas_caso1_2abas", []) or [])
            aba_origem = abas[0] if abas else ""
            aba_comparado = abas[1] if len(abas) > 1 else aba_origem
    else:
        arquivo_origem = st.session_state.get("upload_origem_nome", "")
        arquivo_comparado = st.session_state.get("upload_comparado_nome", "")
        aba_origem = st.session_state.get("aba_origem_caso2", "") or ""
        aba_comparado = st.session_state.get("aba_comparado_caso2", "") or ""

    origem_ux = st.session_state.get("origem_ux", "") or "Origem"
    comparado_ux = st.session_state.get("comparado_ux", "") or "Comparado"

    return {
        "agrupadores_match": _construir_agrupadores_match(),
        "campos_comparados": _construir_campos_comparados(),
        "agrupadores_executivos": list(
            st.session_state.get("agrupadores_executivos", []) or []
        ),
        "epsilon_por_unidade": _construir_epsilon_por_unidade(),
        "thresholds": {
            "chave_nulos_max": float(st.session_state.get("ted_chave_nulos_max", 0.50)),
            "volume_max": int(st.session_state.get("ted_volume_max", 500_000)),
            "concentracao_agrupador_principal_min": float(
                st.session_state.get("ted_concentracao_agrupador_min", 0.70)
            ),
        },
        "origem_ux": origem_ux,
        "comparado_ux": comparado_ux,
        "arquivo_origem": arquivo_origem,
        "arquivo_comparado": arquivo_comparado,
        "aba_origem": aba_origem,
        "aba_comparado": aba_comparado,
        "n_arquivos": n_arq,
        "paleta_aplicada": st.session_state.get("paleta_selecionada", PALETA_DEFAULT),
    }


# ---------------------------------------------------------------------------
# STUBS · telas (preenchidas nas Fases 3-6)
# ---------------------------------------------------------------------------


def _tela_vazio() -> None:
    """E0 · upload físico (S-V1 §3.4)."""
    st.subheader("Escolher arquivo(s)")
    st.markdown(
        "Suba o(s) arquivo(s) Excel ou CSV com os dados que você quer comparar."
    )
    st.caption(
        "Aceita Excel (.xlsx, .xls) e CSV. Pode ser 1 ou 2 arquivos · você decide abaixo."
    )

    n_atual = int(st.session_state.get("n_arquivos", 1))
    n_arquivos = st.radio(
        "Quantos arquivos você vai usar?",
        options=[1, 2],
        index=0 if n_atual == 1 else 1,
        horizontal=True,
        format_func=lambda n: "1 arquivo" if n == 1 else "2 arquivos",
        key="radio_n_arquivos",
    )
    if n_arquivos != n_atual:
        st.session_state["n_arquivos"] = n_arquivos

    if n_arquivos == 1:
        up = st.file_uploader(
            "Arquivo",
            type=["xlsx", "xls", "csv", "tsv"],
            key="up_unico",
        )
        if up is not None:
            if st.button(
                "Avançar · escolher aba(s)",
                type="primary",
                key="btn_avancar_e1ok_caso1",
            ):
                _processar_upload_caso1(up)
                st.rerun()
    else:
        col1, col2 = st.columns(2)
        with col1:
            up_origem = st.file_uploader(
                "Arquivo da Origem",
                type=["xlsx", "xls", "csv", "tsv"],
                key="up_origem",
            )
        with col2:
            up_comparado = st.file_uploader(
                "Arquivo do Comparado",
                type=["xlsx", "xls", "csv", "tsv"],
                key="up_comparado",
            )
        if up_origem is not None and up_comparado is not None:
            if st.button(
                "Avançar · escolher aba(s)",
                type="primary",
                key="btn_avancar_e1ok_caso2",
            ):
                _processar_upload_caso2(up_origem, up_comparado)
                st.rerun()


def _processar_upload_caso1(up) -> None:
    """1 arquivo · chama motor_upload SIMPLES · lê abas · vai para E1_OK."""
    bytes_dados = up.getvalue()
    nome = up.name
    try:
        caminho = _persistir_bytes_temp(nome, bytes_dados)
        upload_result = processar_upload(
            [ArquivoEntrada(caminho_fisico=caminho, caminho_logico="unico")],
            modo="SIMPLES",
        )
    except Exception as exc:  # noqa: BLE001
        st.error(f"Erro ao ler o arquivo: {exc}")
        return
    info = upload_result.arquivo_unico
    abas = _abas_de_arquivo(info)

    st.session_state["upload_unico_bytes"] = bytes_dados
    st.session_state["upload_unico_nome"] = nome
    st.session_state["upload_result"] = upload_result
    st.session_state["abas_origem_disponiveis"] = abas
    st.session_state["abas_comparado_disponiveis"] = abas
    st.session_state["aba_escolhida_unica_caso1"] = (
        abas[0] if abas else None
    )
    st.session_state["abas_escolhidas_caso1_2abas"] = []
    st.session_state["aba_origem_caso2"] = None
    st.session_state["aba_comparado_caso2"] = None
    st.session_state["motor_result"] = None
    st.session_state["etapa"] = "E1_OK"


def _processar_upload_caso2(up_o, up_c) -> None:
    """2 arquivos · chama motor_upload DUAL · lê abas de cada · vai para E1_OK."""
    bytes_o = up_o.getvalue()
    bytes_c = up_c.getvalue()
    nome_o = up_o.name
    nome_c = up_c.name
    try:
        caminho_o = _persistir_bytes_temp(nome_o, bytes_o)
        caminho_c = _persistir_bytes_temp(nome_c, bytes_c)
        upload_result = processar_upload(
            [
                ArquivoEntrada(caminho_fisico=caminho_o, caminho_logico="origem"),
                ArquivoEntrada(caminho_fisico=caminho_c, caminho_logico="comparado"),
            ],
            modo="DUAL",
        )
    except Exception as exc:  # noqa: BLE001
        st.error(f"Erro ao ler arquivos: {exc}")
        return

    duais = upload_result.arquivos_dual or []
    info_o = next((i for i in duais if i.caminho_logico == "origem"), None)
    info_c = next((i for i in duais if i.caminho_logico == "comparado"), None)
    abas_o = _abas_de_arquivo(info_o) if info_o else []
    abas_c = _abas_de_arquivo(info_c) if info_c else []

    st.session_state["upload_origem_bytes"] = bytes_o
    st.session_state["upload_origem_nome"] = nome_o
    st.session_state["upload_comparado_bytes"] = bytes_c
    st.session_state["upload_comparado_nome"] = nome_c
    st.session_state["upload_result"] = upload_result
    st.session_state["abas_origem_disponiveis"] = abas_o
    st.session_state["abas_comparado_disponiveis"] = abas_c
    st.session_state["aba_origem_caso2"] = abas_o[0] if abas_o else None
    st.session_state["aba_comparado_caso2"] = abas_c[0] if abas_c else None
    st.session_state["aba_escolhida_unica_caso1"] = None
    st.session_state["abas_escolhidas_caso1_2abas"] = []
    st.session_state["motor_result"] = None
    st.session_state["etapa"] = "E1_OK"


def _tela_e1_ok() -> None:
    """E1_OK · escolher aba(s) e processar bases (S-V1 §3.5 + D-213)."""
    st.subheader("Escolher arquivo(s)")
    n_arq = int(st.session_state.get("n_arquivos", 1))

    if n_arq == 1:
        nome = st.session_state.get("upload_unico_nome", "")
        st.success(f"Arquivo: **{nome}**")
        abas = list(st.session_state.get("abas_origem_disponiveis", []) or [])
        if not abas:
            # CSV ou arquivo sem abas → modo MESMA_ABA_EM_COLUNAS único
            st.info(
                "Arquivo CSV/sem abas · será processado como aba única "
                "(Caso 3 · MESMA_ABA_EM_COLUNAS · cada linha já é par casado)."
            )
            st.session_state["aba_escolhida_unica_caso1"] = ""
            st.session_state["abas_escolhidas_caso1_2abas"] = []
            _antecipar_caso_logico_e1_ok([""])
        else:
            default_sel = (
                st.session_state.get("abas_escolhidas_caso1_2abas")
                or [st.session_state.get("aba_escolhida_unica_caso1") or abas[0]]
            )
            default_sel = [a for a in default_sel if a in abas]
            if not default_sel:
                default_sel = [abas[0]]
            escolha = st.multiselect(
                "Qual(is) aba(s) quer comparar?",
                options=abas,
                default=default_sel,
                max_selections=2,
                key="ms_abas_caso1",
                help=(
                    "Escolha 1 aba (Caso 3 · Origem e Comparado em colunas distintas "
                    "dentro da mesma aba) ou 2 abas (Caso 2 · Origem em uma aba · "
                    "Comparado em outra)."
                ),
            )
            if len(escolha) == 1:
                st.session_state["aba_escolhida_unica_caso1"] = escolha[0]
                st.session_state["abas_escolhidas_caso1_2abas"] = []
            elif len(escolha) == 2:
                st.session_state["abas_escolhidas_caso1_2abas"] = list(escolha)
                st.session_state["aba_escolhida_unica_caso1"] = None
            else:
                st.session_state["aba_escolhida_unica_caso1"] = None
                st.session_state["abas_escolhidas_caso1_2abas"] = []
            _antecipar_caso_logico_e1_ok(list(escolha))
    else:
        nome_o = st.session_state.get("upload_origem_nome", "")
        nome_c = st.session_state.get("upload_comparado_nome", "")
        col_a, col_b = st.columns(2)
        with col_a:
            st.success(f"Origem: **{nome_o}**")
            abas_o = list(st.session_state.get("abas_origem_disponiveis", []) or [])
            if abas_o:
                aba_atual = st.session_state.get("aba_origem_caso2") or abas_o[0]
                idx = abas_o.index(aba_atual) if aba_atual in abas_o else 0
                st.session_state["aba_origem_caso2"] = st.selectbox(
                    "Aba do arquivo de Origem",
                    abas_o,
                    index=idx,
                    key="sb_aba_origem_caso2",
                )
            else:
                st.session_state["aba_origem_caso2"] = ""
                st.caption("CSV · aba única")
        with col_b:
            st.success(f"Comparado: **{nome_c}**")
            abas_c = list(st.session_state.get("abas_comparado_disponiveis", []) or [])
            if abas_c:
                aba_atual = st.session_state.get("aba_comparado_caso2") or abas_c[0]
                idx = abas_c.index(aba_atual) if aba_atual in abas_c else 0
                st.session_state["aba_comparado_caso2"] = st.selectbox(
                    "Aba do arquivo do Comparado",
                    abas_c,
                    index=idx,
                    key="sb_aba_comparado_caso2",
                )
            else:
                st.session_state["aba_comparado_caso2"] = ""
                st.caption("CSV · aba única")
        # Antecipa caso lógico (sempre ABAS_DISTINTAS em n_arquivos==2 MVP)
        st.session_state["caso_logico_inferido"] = CasoLogicoV1.ABAS_DISTINTAS
        st.caption(
            "📋 Caso lógico antecipado: Origem e Comparado em arquivos/abas distintas · "
            "será executado match no E3."
        )

    st.divider()
    col_v, col_avanc = st.columns([1, 1])
    with col_v:
        if st.button("← Voltar · trocar arquivo(s)", key="btn_voltar_e1ok"):
            _reset_completo()
            st.rerun()
    with col_avanc:
        pode_avancar = _validar_e1_ok_pode_avancar()
        if st.button(
            "Confirmar e processar bases",
            type="primary",
            disabled=not pode_avancar,
            key="btn_confirmar_e1_ok",
        ):
            try:
                _processar_bases_pos_e1_ok()
                st.session_state["etapa"] = "E2"
                _invalidar_a_partir("E2")
                st.rerun()
            except Exception as exc:  # noqa: BLE001
                st.session_state["_erro_msg"] = str(exc)
                st.session_state["etapa"] = "ERRO"
                st.rerun()


def _antecipar_caso_logico_e1_ok(abas_escolhidas: List[str]) -> None:
    """Antecipa caso lógico em E1_OK · info-box discreta (definitivo só em E3)."""
    if len(abas_escolhidas) == 1:
        st.session_state["caso_logico_inferido"] = CasoLogicoV1.MESMA_ABA_EM_COLUNAS
        st.caption(
            "📋 Caso lógico antecipado: 1 aba escolhida · Origem e Comparado em "
            "colunas distintas da mesma aba (Caso 3 · D-213) · cada linha já é "
            "par casado por construção."
        )
    elif len(abas_escolhidas) == 2:
        st.session_state["caso_logico_inferido"] = CasoLogicoV1.ABAS_DISTINTAS
        st.caption(
            "📋 Caso lógico antecipado: 2 abas escolhidas · Origem em uma aba · "
            "Comparado em outra (Caso 2 · D-213) · será executado match no E3."
        )
    else:
        st.session_state["caso_logico_inferido"] = None


def _validar_e1_ok_pode_avancar() -> bool:
    """Verifica se há aba(s) válida(s) para processar."""
    n_arq = int(st.session_state.get("n_arquivos", 1))
    if n_arq == 1:
        if st.session_state.get("aba_escolhida_unica_caso1") is not None:
            return True
        if len(st.session_state.get("abas_escolhidas_caso1_2abas") or []) == 2:
            return True
        return False
    return bool(st.session_state.get("aba_origem_caso2") is not None) and bool(
        st.session_state.get("aba_comparado_caso2") is not None
    )


def _processar_bases_pos_e1_ok() -> None:
    """Roda motor_upload + motor_base com a(s) aba(s) escolhida(s) · popula motor_result."""
    n_arq = int(st.session_state.get("n_arquivos", 1))
    if n_arq == 1:
        bytes_dados = st.session_state.get("upload_unico_bytes")
        nome = st.session_state.get("upload_unico_nome", "")
        if bytes_dados is None:
            raise ValueError("Bytes do arquivo perdidos · refaça o upload (Nova análise).")
        caminho = _persistir_bytes_temp(nome, bytes_dados)

        if st.session_state.get("aba_escolhida_unica_caso1") is not None:
            # Caso 3 · MESMA_ABA · SIMPLES
            aba = st.session_state["aba_escolhida_unica_caso1"]
            entries = [
                ArquivoEntrada(
                    caminho_fisico=caminho,
                    caminho_logico="unico",
                    aba_solicitada=aba or None,
                )
            ]
            modo = "SIMPLES"
        else:
            # Caso 2 · 1 arquivo, 2 abas · DUAL
            abas = st.session_state.get("abas_escolhidas_caso1_2abas") or []
            entries = [
                ArquivoEntrada(
                    caminho_fisico=caminho,
                    caminho_logico="origem",
                    aba_solicitada=abas[0],
                ),
                ArquivoEntrada(
                    caminho_fisico=caminho,
                    caminho_logico="comparado",
                    aba_solicitada=abas[1],
                ),
            ]
            modo = "DUAL"
    else:
        # Caso 1 · 2 arquivos · DUAL
        bytes_o = st.session_state.get("upload_origem_bytes")
        bytes_c = st.session_state.get("upload_comparado_bytes")
        if bytes_o is None or bytes_c is None:
            raise ValueError("Bytes dos arquivos perdidos · refaça o upload (Nova análise).")
        caminho_o = _persistir_bytes_temp(
            st.session_state["upload_origem_nome"], bytes_o
        )
        caminho_c = _persistir_bytes_temp(
            st.session_state["upload_comparado_nome"], bytes_c
        )
        entries = [
            ArquivoEntrada(
                caminho_fisico=caminho_o,
                caminho_logico="origem",
                aba_solicitada=st.session_state.get("aba_origem_caso2") or None,
            ),
            ArquivoEntrada(
                caminho_fisico=caminho_c,
                caminho_logico="comparado",
                aba_solicitada=st.session_state.get("aba_comparado_caso2") or None,
            ),
        ]
        modo = "DUAL"

    upload_result = processar_upload(entries, modo=modo)
    motor_result = processar_base(upload_result)

    if motor_result.bloqueios:
        codigos = ", ".join(b.codigo for b in motor_result.bloqueios)
        msgs = " · ".join(
            b.condicao_disparo for b in motor_result.bloqueios
        )
        raise ValueError(f"Bloqueios do motor_base [{codigos}]: {msgs}")

    st.session_state["upload_result"] = upload_result
    st.session_state["motor_result"] = motor_result


def _tela_e2() -> None:
    """E2 · identificar lados (S-V1 §3.6 · P-V1 §2.1)."""
    st.subheader("Identificar lados")
    st.caption(
        "Dê nomes amigáveis para os dois lados da comparação · aparecem no Excel."
    )
    col1, col2 = st.columns(2)
    with col1:
        origem_ux = st.text_input(
            "Como chamar a Origem",
            value=st.session_state.get("origem_ux", "") or "",
            placeholder="Ex: Razão · Sistema A · ERP",
            key="ti_origem_ux",
        )
        st.session_state["origem_ux"] = origem_ux
    with col2:
        comparado_ux = st.text_input(
            "Como chamar o Comparado",
            value=st.session_state.get("comparado_ux", "") or "",
            placeholder="Ex: Balancete · Sistema B · DW",
            key="ti_comparado_ux",
        )
        st.session_state["comparado_ux"] = comparado_ux

    st.caption(
        "Esses nomes aparecem em todas as telas e no Excel exportado. "
        "Se deixar em branco, o sistema usa 'Origem' e 'Comparado' como padrão."
    )

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Voltar", key="btn_voltar_e2"):
            st.session_state["etapa"] = "E1_OK"
            st.rerun()
    with c2:
        if st.button(
            "Próximo · Configurar análise",
            type="primary",
            key="btn_avancar_e3",
        ):
            st.session_state["etapa"] = "E3"
            _invalidar_a_partir("E3")
            st.rerun()


# ---------------------------------------------------------------------------
# E3 · helpers
# ---------------------------------------------------------------------------


def _colunas_origem_disponiveis() -> List[str]:
    """Colunas da aba Origem · após processamento do motor_base."""
    motor_result: Optional[MotorResult] = st.session_state.get("motor_result")
    if motor_result is None:
        return []
    df = motor_result.df
    n_arq = int(st.session_state.get("n_arquivos", 1))
    caso_logico = st.session_state.get("caso_logico_inferido")
    # Em SIMPLES (caso 3) · todas as colunas estão em df
    # Em DUAL · particionar por origem_comparado_map
    if motor_result.modo_upload == "SIMPLES":
        return list(df.columns)
    ocm = motor_result.origem_comparado_map or {}
    idx_origem = sorted(i for i, papel in ocm.items() if papel == "origem")
    if not idx_origem:
        return list(df.columns)
    df_o = df.iloc[idx_origem]
    return [c for c in df_o.columns if df_o[c].notna().any() or True]


def _colunas_comparado_disponiveis() -> List[str]:
    motor_result: Optional[MotorResult] = st.session_state.get("motor_result")
    if motor_result is None:
        return []
    df = motor_result.df
    if motor_result.modo_upload == "SIMPLES":
        return list(df.columns)
    ocm = motor_result.origem_comparado_map or {}
    idx_comparado = sorted(i for i, papel in ocm.items() if papel == "comparado")
    if not idx_comparado:
        return list(df.columns)
    df_c = df.iloc[idx_comparado]
    return [c for c in df_c.columns if df_c[c].notna().any() or True]


def _inferir_caso_logico_definitivo() -> Optional[CasoLogicoV1]:
    """Inferência definitiva do caso lógico baseada nos apontamentos atuais."""
    aba_o = st.session_state.get("aba_origem_caso2") or st.session_state.get(
        "aba_escolhida_unica_caso1"
    )
    aba_c = st.session_state.get("aba_comparado_caso2") or st.session_state.get(
        "aba_escolhida_unica_caso1"
    )
    n_arq = int(st.session_state.get("n_arquivos", 1))
    if n_arq == 1:
        if st.session_state.get("aba_escolhida_unica_caso1") is not None:
            # 1 aba única → MESMA_ABA_EM_COLUNAS (caso 3)
            return CasoLogicoV1.MESMA_ABA_EM_COLUNAS
        if len(st.session_state.get("abas_escolhidas_caso1_2abas") or []) == 2:
            return CasoLogicoV1.ABAS_DISTINTAS
        return None
    return CasoLogicoV1.ABAS_DISTINTAS


def _detectar_bloqueio_mesma_coluna() -> List[str]:
    """Retorna lista de mensagens de erro B-V1-MESMA-COLUNA para apontamentos."""
    erros: List[str] = []
    caso = st.session_state.get("caso_logico_inferido")
    if caso != CasoLogicoV1.MESMA_ABA_EM_COLUNAS:
        return erros
    for d in st.session_state.get("agrupadores_match", []) or []:
        if isinstance(d, dict):
            if d.get("nome_origem") and d.get("nome_origem") == d.get("nome_comparado"):
                erros.append(
                    f"Agrupador · coluna {d['nome_origem']!r} apontada como Origem e "
                    "Comparado simultaneamente."
                )
    for d in st.session_state.get("campos_comparados", []) or []:
        if isinstance(d, dict):
            if d.get("nome_origem") and d.get("nome_origem") == d.get("nome_comparado"):
                erros.append(
                    f"Campo · coluna {d['nome_origem']!r} apontada como Origem e "
                    "Comparado simultaneamente."
                )
    return erros


def _tela_e3() -> None:
    """E3 · configurar análise · 3 sub-blocos (S-V1 §3.7)."""
    st.subheader("Configurar análise")
    st.caption("Declare como casar registros e o que comparar entre eles.")

    cols_o = _colunas_origem_disponiveis()
    cols_c = _colunas_comparado_disponiveis()
    if not cols_o or not cols_c:
        st.error(
            "Colunas indisponíveis · motor_base não foi processado. "
            "Volte para escolher arquivo(s)."
        )
        if st.button("← Voltar para escolher arquivo(s)", key="btn_voltar_e3_sem_cols"):
            st.session_state["etapa"] = "E1_OK"
            st.rerun()
        return

    # Sub-bloco 3.1 · Agrupadores de match
    st.markdown(
        "##### Agrupadores de match · qual a chave para casar registros entre os dois lados?"
    )
    n_agrup = int(st.session_state.get("n_agrupadores_visiveis", 1))
    agrupadores_form: List[Dict[str, Any]] = []
    estado_atual = list(st.session_state.get("agrupadores_match", []) or [])
    for i in range(n_agrup):
        cur = estado_atual[i] if i < len(estado_atual) else {}
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([3, 3, 3, 2])
            with c1:
                nome_o = st.selectbox(
                    f"Coluna na Origem · agrupador {i + 1}",
                    options=[""] + cols_o,
                    index=(
                        cols_o.index(cur["nome_origem"]) + 1
                        if cur.get("nome_origem") in cols_o
                        else 0
                    ),
                    key=f"agrup_origem_{i}",
                )
            with c2:
                nome_c = st.selectbox(
                    f"Coluna no Comparado · agrupador {i + 1}",
                    options=[""] + cols_c,
                    index=(
                        cols_c.index(cur["nome_comparado"]) + 1
                        if cur.get("nome_comparado") in cols_c
                        else 0
                    ),
                    key=f"agrup_comparado_{i}",
                )
            with c3:
                rotulo = st.text_input(
                    f"Rótulo analítico · agrupador {i + 1}",
                    value=cur.get("rotulo_analitico", "") or "",
                    placeholder="Ex: Documento · CNPJ · Filial",
                    key=f"agrup_rotulo_{i}",
                )
            with c4:
                modo_default = cur.get("modo_match", "EXATO")
                modo_idx = (
                    [m[0] for m in MODOS_MATCH_V1].index(modo_default)
                    if modo_default in [m[0] for m in MODOS_MATCH_V1]
                    else 0
                )
                modo = st.selectbox(
                    f"Modo · agrupador {i + 1}",
                    options=[m[0] for m in MODOS_MATCH_V1],
                    index=modo_idx,
                    format_func=lambda m: dict(MODOS_MATCH_V1)[m],
                    key=f"agrup_modo_{i}",
                )
            agrupadores_form.append(
                {
                    "nome_origem": nome_o,
                    "nome_comparado": nome_c,
                    "rotulo_analitico": rotulo or nome_o,
                    "modo_match": modo,
                }
            )
    st.session_state["agrupadores_match"] = agrupadores_form

    c_add, c_rem = st.columns([1, 1])
    with c_add:
        if n_agrup < 5 and st.button("+ Adicionar agrupador", key="btn_add_agrup"):
            st.session_state["n_agrupadores_visiveis"] = n_agrup + 1
            st.rerun()
    with c_rem:
        if n_agrup > 1 and st.button("− Remover último", key="btn_rem_agrup"):
            st.session_state["n_agrupadores_visiveis"] = n_agrup - 1
            st.session_state["agrupadores_match"] = agrupadores_form[:-1]
            st.rerun()

    st.divider()

    # Sub-bloco 3.2 · Campos comparados
    st.markdown(
        "##### Campos comparados · quais valores devem bater entre os dois lados?"
    )
    n_campos = int(st.session_state.get("n_campos_visiveis", 1))
    campos_form: List[Dict[str, Any]] = []
    estado_atual_campos = list(st.session_state.get("campos_comparados", []) or [])
    for i in range(n_campos):
        cur = estado_atual_campos[i] if i < len(estado_atual_campos) else {}
        with st.container(border=True):
            r1c1, r1c2, r1c3 = st.columns([3, 3, 3])
            with r1c1:
                nome_o = st.selectbox(
                    f"Coluna na Origem · campo {i + 1}",
                    options=[""] + cols_o,
                    index=(
                        cols_o.index(cur["nome_origem"]) + 1
                        if cur.get("nome_origem") in cols_o
                        else 0
                    ),
                    key=f"campo_origem_{i}",
                )
            with r1c2:
                nome_c = st.selectbox(
                    f"Coluna no Comparado · campo {i + 1}",
                    options=[""] + cols_c,
                    index=(
                        cols_c.index(cur["nome_comparado"]) + 1
                        if cur.get("nome_comparado") in cols_c
                        else 0
                    ),
                    key=f"campo_comparado_{i}",
                )
            with r1c3:
                nome_analitico = st.text_input(
                    f"Nome analítico · campo {i + 1}",
                    value=cur.get("nome_analitico", "") or "",
                    placeholder="Ex: Valor · Quantidade · Margem",
                    key=f"campo_nome_{i}",
                )

            r2c1, r2c2, r2c3 = st.columns([3, 3, 3])
            with r2c1:
                tipo_default = cur.get("tipo_logico", "VALOR_MONETARIO")
                tipo_idx = (
                    [t[0] for t in TIPOS_CAMPO_V1].index(tipo_default)
                    if tipo_default in [t[0] for t in TIPOS_CAMPO_V1]
                    else 0
                )
                tipo = st.selectbox(
                    f"Tipo lógico · campo {i + 1}",
                    options=[t[0] for t in TIPOS_CAMPO_V1],
                    index=tipo_idx,
                    format_func=lambda t: dict(TIPOS_CAMPO_V1)[t],
                    key=f"campo_tipo_{i}",
                )
            with r2c2:
                # Default DDU: derivado de tipo_logico
                try:
                    unidade_default_enum = DEFAULT_UNIDADE_POR_TIPO[TipoCampoV1(tipo)]
                    unidade_default = unidade_default_enum.value
                except (KeyError, ValueError):
                    unidade_default = "MONETARIO_BRL"
                # Se tipo mudou desde último estado · força reset (espelho V2 P-35)
                if cur.get("tipo_logico") and cur["tipo_logico"] != tipo:
                    unidade_atual = unidade_default
                else:
                    unidade_atual = cur.get("unidade", unidade_default)
                if unidade_atual not in [u[0] for u in UNIDADES_V1]:
                    unidade_atual = unidade_default
                unidade_idx = [u[0] for u in UNIDADES_V1].index(unidade_atual)
                unidade = st.selectbox(
                    f"Unidade · campo {i + 1}",
                    options=[u[0] for u in UNIDADES_V1],
                    index=unidade_idx,
                    format_func=lambda u: dict(UNIDADES_V1)[u],
                    key=f"campo_unidade_{i}",
                )
            with r2c3:
                tol_default = cur.get("tolerancia", "0")
                try:
                    tol_default_float = float(tol_default)
                except Exception:
                    tol_default_float = 0.0
                tolerancia = st.number_input(
                    f"Tolerância absoluta · campo {i + 1}",
                    min_value=0.0,
                    value=tol_default_float,
                    step=0.01,
                    format="%.4f",
                    key=f"campo_tolerancia_{i}",
                    help="Diferença absoluta absorvida · campo conta como conciliado dentro deste limite.",
                )

            campos_form.append(
                {
                    "nome_origem": nome_o,
                    "nome_comparado": nome_c,
                    "nome_analitico": nome_analitico or nome_o,
                    "tipo_logico": tipo,
                    "unidade": unidade,
                    "tolerancia": str(tolerancia),
                }
            )
    st.session_state["campos_comparados"] = campos_form

    c_add_camp, c_rem_camp = st.columns([1, 1])
    with c_add_camp:
        if n_campos < 10 and st.button("+ Adicionar campo", key="btn_add_campo"):
            st.session_state["n_campos_visiveis"] = n_campos + 1
            st.rerun()
    with c_rem_camp:
        if n_campos > 1 and st.button("− Remover último campo", key="btn_rem_campo"):
            st.session_state["n_campos_visiveis"] = n_campos - 1
            st.session_state["campos_comparados"] = campos_form[:-1]
            st.rerun()

    st.divider()

    # Sub-bloco 3.3 · Inferência caso lógico (info-box)
    caso = _inferir_caso_logico_definitivo()
    st.session_state["caso_logico_inferido"] = caso
    if caso == CasoLogicoV1.ABAS_DISTINTAS:
        st.info(
            "📋 Caso detectado: Origem e Comparado em abas distintas · será executado "
            "match para casar registros."
        )
    elif caso == CasoLogicoV1.MESMA_ABA_EM_COLUNAS:
        st.info(
            "📋 Caso detectado: Origem e Comparado em colunas distintas da mesma aba · "
            "cada linha já é par casado por construção."
        )

    st.divider()

    # Validações inline (S-V1 §3.7)
    erros: List[str] = []
    avisos: List[str] = []

    agrups_validos = [
        a for a in agrupadores_form
        if a.get("nome_origem") and a.get("nome_comparado")
    ]
    campos_validos = [
        c for c in campos_form
        if c.get("nome_origem") and c.get("nome_comparado")
    ]
    if len(agrups_validos) == 0:
        erros.append("Configure ao menos 1 agrupador de match para casar registros.")
    if len(campos_validos) == 0:
        erros.append("Configure ao menos 1 campo comparado para a análise.")

    erros.extend(_detectar_bloqueio_mesma_coluna())

    # B-V1-CHAVE-INVALIDA (warning · não bloqueia)
    motor_result: Optional[MotorResult] = st.session_state.get("motor_result")
    if motor_result is not None:
        chave_nulos_max = float(st.session_state.get("ted_chave_nulos_max", 0.50))
        df = motor_result.df
        for a in agrups_validos:
            for col in {a["nome_origem"], a["nome_comparado"]}:
                if col in df.columns and len(df) > 0:
                    pct_null = float(df[col].isna().mean())
                    if pct_null >= chave_nulos_max:
                        avisos.append(
                            f"Coluna {col!r} tem {pct_null:.0%} de valores vazios · "
                            f"≥ limite {chave_nulos_max:.0%} (W-V1 · B-V1-CHAVE-INVALIDA)."
                        )

    # W-V1-UNIDADE (warning · não bloqueia)
    for c in campos_validos:
        try:
            tipo_enum = TipoCampoV1(c["tipo_logico"])
            unidade_default = DEFAULT_UNIDADE_POR_TIPO[tipo_enum].value
            if c["unidade"] != unidade_default:
                avisos.append(
                    f"Campo {c['nome_analitico']!r}: unidade declarada {c['unidade']} "
                    f"diverge da inferida {unidade_default} (W-V1-UNIDADE · não bloqueia)."
                )
        except (KeyError, ValueError):
            pass

    for e in erros:
        st.error(e)
    for w in avisos:
        st.warning(w)

    pode_avancar = len(erros) == 0

    cb1, cb2 = st.columns(2)
    with cb1:
        if st.button("← Voltar", key="btn_voltar_e3"):
            st.session_state["etapa"] = "E2"
            st.rerun()
    with cb2:
        if st.button(
            "Próximo · Agrupadores executivos",
            type="primary",
            disabled=not pode_avancar,
            key="btn_avancar_e4",
        ):
            st.session_state["etapa"] = "E4"
            _invalidar_a_partir("E4")
            st.rerun()


def _colunas_executivas_disponiveis() -> List[str]:
    """Colunas elegíveis como agrupadores executivos.

    União de colunas Origem ∪ Comparado · sem incluir colunas já apontadas
    em campos comparados (essas são valores · não recortes).
    """
    motor_result: Optional[MotorResult] = st.session_state.get("motor_result")
    if motor_result is None:
        return []
    cols_o = set(_colunas_origem_disponiveis())
    cols_c = set(_colunas_comparado_disponiveis())
    todas = sorted(cols_o | cols_c)
    # Excluir colunas usadas como valor (nome_origem dos campos)
    usadas_em_campos = {
        c.get("nome_origem")
        for c in (st.session_state.get("campos_comparados") or [])
        if isinstance(c, dict)
    }
    return [c for c in todas if c not in usadas_em_campos]


def _tela_e4() -> None:
    """E4 · agrupadores executivos · OPCIONAL (S-V1 §3.8 · D-212)."""
    st.subheader("Agrupadores executivos")
    st.caption("Opcional · quer ver o resultado consolidado por algum recorte?")
    st.markdown(
        "Quando configurado, gera tabela consolidada por filial / centro de "
        "custo / outro recorte na aba 'Resumo por Agrupador' do Excel."
    )

    colunas_disp = _colunas_executivas_disponiveis()
    default_atual = list(st.session_state.get("agrupadores_executivos", []) or [])
    default_atual = [c for c in default_atual if c in colunas_disp]
    agrupadores_executivos = st.multiselect(
        "Agrupar Resumo por (0 a 5 colunas)",
        options=colunas_disp,
        default=default_atual,
        max_selections=5,
        key="ms_agrupadores_executivos",
    )
    st.session_state["agrupadores_executivos"] = agrupadores_executivos

    if not agrupadores_executivos:
        st.info(
            "Nenhum agrupador executivo configurado · aba 'Resumo por Agrupador' "
            "não será gerada · análise consolidada disponível em 'Resumo Executivo'."
        )

    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("← Voltar", key="btn_voltar_e4"):
            st.session_state["etapa"] = "E3"
            st.rerun()
    with c2:
        if st.button("Pular · ir direto para Revisar", key="btn_pular_e5"):
            st.session_state["etapa"] = "E5"
            st.rerun()
    with c3:
        if st.button(
            "Próximo · Revisar e executar",
            type="primary",
            key="btn_avancar_e5",
        ):
            st.session_state["etapa"] = "E5"
            st.rerun()


def _caso_logico_userfacing() -> str:
    """Microcopy user-facing para o caso lógico atual."""
    caso = st.session_state.get("caso_logico_inferido")
    if caso == CasoLogicoV1.MESMA_ABA_EM_COLUNAS:
        return "Mesma aba · Origem e Comparado em colunas distintas"
    if caso == CasoLogicoV1.ABAS_DISTINTAS:
        return "Abas distintas · será executado match"
    return "(a inferir)"


def _tela_e5() -> None:
    """E5 · revisar e executar (S-V1 §3.9)."""
    st.subheader("Revisar e executar")
    st.caption("Confira a configuração antes de processar.")

    n_arq = int(st.session_state.get("n_arquivos", 1))
    if n_arq == 1:
        nome_arquivos = st.session_state.get("upload_unico_nome", "(sem nome)")
        if st.session_state.get("aba_escolhida_unica_caso1") is not None:
            abas_str = f"Aba: {st.session_state['aba_escolhida_unica_caso1']}"
        else:
            abas_lista = st.session_state.get("abas_escolhidas_caso1_2abas") or []
            abas_str = (
                f"Origem: {abas_lista[0] if abas_lista else '?'} · "
                f"Comparado: {abas_lista[1] if len(abas_lista) > 1 else '?'}"
            )
    else:
        nome_arquivos = (
            f"Origem: {st.session_state.get('upload_origem_nome', '?')} · "
            f"Comparado: {st.session_state.get('upload_comparado_nome', '?')}"
        )
        abas_str = (
            f"Aba Origem: {st.session_state.get('aba_origem_caso2', '?')} · "
            f"Aba Comparado: {st.session_state.get('aba_comparado_caso2', '?')}"
        )

    origem_ux = st.session_state.get("origem_ux") or "Origem"
    comparado_ux = st.session_state.get("comparado_ux") or "Comparado"
    agrups = st.session_state.get("agrupadores_match", []) or []
    campos = st.session_state.get("campos_comparados", []) or []
    execs = st.session_state.get("agrupadores_executivos", []) or []

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown("**Arquivo(s)**")
        st.write(nome_arquivos)
        st.caption(abas_str)
        st.caption(f"Caso: {_caso_logico_userfacing()}")
    with c2:
        st.markdown("**Lados**")
        st.write(f"Origem: {origem_ux}")
        st.write(f"Comparado: {comparado_ux}")
    with c3:
        st.markdown("**Agrupadores de match**")
        st.write(f"{len(agrups)} agrupador(es)")
        if agrups:
            st.caption(
                " · ".join(
                    a.get("rotulo_analitico") or a.get("nome_origem") or "?"
                    for a in agrups
                )
            )
    with c4:
        st.markdown("**Campos comparados**")
        st.write(f"{len(campos)} campo(s)")
        if campos:
            st.caption(
                " · ".join(
                    c.get("nome_analitico") or c.get("nome_origem") or "?"
                    for c in campos
                )
            )
    with c5:
        st.markdown("**Agrupadores executivos**")
        if execs:
            st.write(f"{len(execs)} configurado(s)")
            st.caption(" · ".join(execs))
        else:
            st.write("—")

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("← Voltar", key="btn_voltar_e5"):
            st.session_state["etapa"] = "E4"
            st.rerun()
    with col_b:
        if st.button(
            "Processar análise",
            type="primary",
            key="btn_processar",
        ):
            st.session_state["etapa"] = "PROCESSANDO"
            st.rerun()


def _label_classificacao_user(
    classificacao: ClassificacaoRegistroV1,
    origem_ux: str,
    comparado_ux: str,
    rotulo_amig: bool,
) -> str:
    """Substituição dinâmica conforme P-V1 §2.2 · Bloco 3 v4."""
    if classificacao == ClassificacaoRegistroV1.SO_ORIGEM:
        return f"Saiu do {origem_ux}" if rotulo_amig else "Só na Origem"
    if classificacao == ClassificacaoRegistroV1.SO_COMPARADO:
        return f"Apareceu no {comparado_ux}" if rotulo_amig else "Só no Comparado"
    return {
        ClassificacaoRegistroV1.CONCILIADO: "Conciliados",
        ClassificacaoRegistroV1.DIVERGENTE_VALOR: "Divergentes por valor",
        ClassificacaoRegistroV1.DIVERGENCIA_DUPLICIDADE: "Divergência por duplicidade",
        ClassificacaoRegistroV1.DIVERGENCIA_AMBIGUIDADE: "Divergência por ambiguidade de match",
    }.get(classificacao, classificacao.value)


def _renderizar_bloco_kpis_v1(v1_result: ConciliacaoV1Result) -> None:
    """Bloco 2 · 4 cards · Card 4 = Taxa de Conciliação (KPI primário V1)."""
    cr = v1_result.conciliacao_realizada
    origem_ux = cr.origem_ux or "Origem"
    comparado_ux = cr.comparado_ux or "Comparado"
    contagem = v1_result.contagem_por_classificacao
    n_concil = contagem.get(ClassificacaoRegistroV1.CONCILIADO, 0)
    n_total = sum(contagem.values()) or 1
    taxa = (n_concil / n_total) if n_total > 0 else 0.0

    # Escolha do campo principal: primeiro campo da lista
    valor_por_campo = list(v1_result.valor_por_campo or [])
    if valor_por_campo:
        primeiro = valor_por_campo[0]
        unid_str = primeiro.unidade.value
        total_o = formatar_valor_por_unidade(float(primeiro.soma_origem), unid_str)
        total_c = formatar_valor_por_unidade(float(primeiro.soma_comparado), unid_str)
        delta = formatar_diferenca_por_unidade(
            float(primeiro.diferenca_liquida), unid_str
        )
    else:
        total_o = total_c = delta = "—"

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label=f"Total · {origem_ux}", value=total_o)
    with c2:
        st.metric(label=f"Total · {comparado_ux}", value=total_c)
    with c3:
        st.metric(label="Diferença líquida", value=delta)
    with c4:
        st.metric(
            label="**Taxa de Conciliação**",
            value=formatar_percentual_br(taxa, conversao_fracao=True),
        )


def _renderizar_bloco_saude_v1(v1_result: ConciliacaoV1Result) -> None:
    """Bloco 3 · saúde · 6 categorias (4 zeradas em MESMA_ABA)."""
    cr = v1_result.conciliacao_realizada
    origem_ux = cr.origem_ux or "Origem"
    comparado_ux = cr.comparado_ux or "Comparado"
    rotulo_amig = cr.rotulo_amigavel_declarado

    contagem = v1_result.contagem_por_classificacao
    n_total = sum(contagem.values()) or 1

    st.markdown("#### Saúde da comparação")
    rows = []
    for cls in [
        ClassificacaoRegistroV1.CONCILIADO,
        ClassificacaoRegistroV1.DIVERGENTE_VALOR,
        ClassificacaoRegistroV1.SO_ORIGEM,
        ClassificacaoRegistroV1.SO_COMPARADO,
        ClassificacaoRegistroV1.DIVERGENCIA_DUPLICIDADE,
        ClassificacaoRegistroV1.DIVERGENCIA_AMBIGUIDADE,
    ]:
        n = contagem.get(cls, 0)
        pct = (n / n_total) if n_total > 0 else 0.0
        rows.append(
            {
                "Categoria": _label_classificacao_user(
                    cls, origem_ux, comparado_ux, rotulo_amig
                ),
                "Casos": n,
                "Participação": formatar_percentual_br(pct, conversao_fracao=True),
            }
        )
    df_saude = pd.DataFrame(rows)
    st.dataframe(df_saude, hide_index=True, use_container_width=True)


def _renderizar_bloco_ponte_v1(v1_result: ConciliacaoV1Result) -> None:
    """Bloco 4 · banner colorido com status binário."""
    status = v1_result.status_ponte_geral
    if status == StatusPonteV1.FECHA:
        st.success(
            "✅ Ponte fecha em todos os campos comparados · "
            "diferença total decomposta integralmente"
        )
    else:
        # Lista resíduos por campo
        residuos = []
        for p in v1_result.pontes:
            if not p.fecha:
                residuo_fmt = formatar_valor_por_unidade(
                    float(p.residuo), p.unidade.value
                )
                residuos.append(f"**{p.nome_analitico}**: resíduo {residuo_fmt}")
        msg = " · ".join(residuos) if residuos else "ver detalhes na Aba 5"
        st.warning(f"⚠️ Ponte com resíduo · {msg}")


def _renderizar_bloco_leitura_v1(v1_result: ConciliacaoV1Result) -> None:
    """Bloco 5 · leitura qualitativa + warnings."""
    st.markdown("#### Leitura qualitativa")
    leitura = v1_result.leitura_qualitativa
    if leitura and leitura.texto:
        st.write(leitura.texto)
    else:
        st.caption("(sem leitura qualitativa disponível)")

    warnings_ativos = [
        w for w in (v1_result.warnings_emitidos or []) if w.n_ocorrencias > 0
    ]
    if warnings_ativos:
        with st.expander(
            f"⚠️ Avisos ({len(warnings_ativos)}) · ver detalhes",
            expanded=False,
        ):
            for w in warnings_ativos:
                st.markdown(
                    f"**{w.codigo}** · severidade {w.severidade} · "
                    f"{w.n_ocorrencias} ocorrência(s)"
                )


def _render_botao_download_excel_v1() -> None:
    """Gera Excel com a paleta atual e oferece download · espelho V2."""
    v1_result: ConciliacaoV1Result = st.session_state["v1_result"]
    paleta_user = st.session_state.get("paleta_selecionada", PALETA_DEFAULT)
    paleta_tech = PALETA_TECH.get(paleta_user, "azul")

    cache_key = f"_excel_cache_{paleta_tech}"
    if cache_key not in st.session_state:
        try:
            with tempfile.NamedTemporaryFile(
                suffix=".xlsx", delete=False, prefix="tabloflow_v1_export_"
            ) as tmp:
                tmp_path = tmp.name
            cr = v1_result.conciliacao_realizada
            export_result = exportar_resultado_v1(
                v1_result=v1_result,
                caminho_saida=tmp_path,
                paleta_nome=paleta_tech,
                origem_rotulo=cr.origem_ux,
                comparado_rotulo=cr.comparado_ux,
                arquivo_nome_origem=cr.arquivo_origem,
                aba_consumida=cr.aba_origem,
                usar_nome_executivo=True,
            )
            with open(export_result.caminho_arquivo, "rb") as f:
                st.session_state[cache_key] = (
                    f.read(),
                    Path(export_result.caminho_arquivo).name,
                )
            chaves = list(st.session_state.get("_excel_cache_keys", []))
            if cache_key not in chaves:
                chaves.append(cache_key)
            st.session_state["_excel_cache_keys"] = chaves
        except NotImplementedError:
            st.warning(
                "📥 Geração de Excel ainda não disponível (Fase 7 do A-V1)."
            )
            return
        except Exception as exc:  # noqa: BLE001
            st.error(f"Erro ao gerar Excel: {exc}")
            return

    bytes_excel, nome_arquivo = st.session_state[cache_key]
    st.download_button(
        "📥 Baixar Excel",
        data=bytes_excel,
        file_name=nome_arquivo,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
        key="btn_download_excel",
    )


def _tela_resultado() -> None:
    """RESULTADO · 5 blocos executivos + rodapé com paleta (S-V1 §3.11)."""
    v1_result: Optional[ConciliacaoV1Result] = st.session_state.get("v1_result")
    if v1_result is None:
        st.warning(
            "Nenhum resultado disponível · volte para Revisar e processar a análise."
        )
        if st.button("← Voltar para revisar", key="btn_voltar_resultado_vazio"):
            st.session_state["etapa"] = "E5"
            st.rerun()
        return

    cr = v1_result.conciliacao_realizada
    origem_ux = cr.origem_ux or "Origem"
    comparado_ux = cr.comparado_ux or "Comparado"

    # Bloco 1 · Cabeçalho executivo
    st.header("📊 Resultado da análise")
    timestamp = (
        v1_result.motor_result_meta.timestamp_processamento
        if v1_result.motor_result_meta and v1_result.motor_result_meta.timestamp_processamento
        else datetime.now()
    )
    st.caption(
        f"Conciliação entre **{origem_ux}** e **{comparado_ux}** · "
        f"gerada em {timestamp.strftime('%d/%m/%Y %H:%M')}"
    )

    # Bloco 2 · 4 KPI cards
    _renderizar_bloco_kpis_v1(v1_result)

    # Bloco 3 · Saúde da comparação
    _renderizar_bloco_saude_v1(v1_result)

    # Bloco 4 · Status da Ponte
    _renderizar_bloco_ponte_v1(v1_result)

    # Bloco 5 · Leitura qualitativa + warnings
    _renderizar_bloco_leitura_v1(v1_result)

    # Rodapé · Voltar · Paleta · Baixar Excel · Nova análise
    st.divider()
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("← Voltar", key="btn_voltar_resultado"):
            st.session_state["etapa"] = "E5"
            st.rerun()
    with c2:
        paleta_atual = st.session_state.get("paleta_selecionada", PALETA_DEFAULT)
        idx_p = (
            PALETAS_DISPONIVEIS.index(paleta_atual)
            if paleta_atual in PALETAS_DISPONIVEIS
            else 0
        )
        nova_paleta = st.selectbox(
            "Paleta do Excel",
            options=PALETAS_DISPONIVEIS,
            index=idx_p,
            key="sb_paleta_resultado",
        )
        if nova_paleta != paleta_atual:
            st.session_state["paleta_selecionada"] = nova_paleta
            # Não invalida cache de outras paletas · cache é por paleta
    with c3:
        _render_botao_download_excel_v1()

    if st.button("🔄 Nova análise", key="btn_nova_resultado"):
        _reset_completo()
        st.rerun()


def _tela_erro() -> None:
    """ERRO · mensagem de bloqueio + voltar."""
    st.subheader("Erro de processamento")
    msg = st.session_state.get("_erro_msg", "Erro desconhecido.")
    st.error(msg)
    if st.button("← Voltar para revisar configuração", key="btn_voltar_erro"):
        st.session_state["etapa"] = "E5"
        st.session_state["_erro_msg"] = ""
        st.rerun()


def _executar_pipeline_v1() -> None:
    """Constrói config · chama executar_v1 · trata bloqueios."""
    with st.spinner("Processando..."):
        config = _construir_config_v1()
        try:
            v1_result = executar_v1(st.session_state["motor_result"], config)
            st.session_state["v1_result"] = v1_result
            st.session_state["etapa"] = "RESULTADO"
            _limpar_cache_excel()
        except ValueError as exc:
            st.session_state["_erro_msg"] = str(exc)
            st.session_state["etapa"] = "ERRO"


# ---------------------------------------------------------------------------
# Dispatcher e main
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
    elif etapa == "E5":
        _tela_e5()
    elif etapa == "PROCESSANDO":
        _executar_pipeline_v1()
        st.rerun()
    elif etapa == "RESULTADO":
        _tela_resultado()
    elif etapa == "ERRO":
        _tela_erro()
    else:
        st.error(f"Etapa desconhecida: {etapa}")


def main() -> None:
    st.set_page_config(page_title="TabloFlow · V1 · Conciliação", layout="wide")
    _init_state()
    _render_header()
    if st.session_state.get("etapa") not in ("vazio",):
        _render_expander_ted()
    _dispatch()


main()
