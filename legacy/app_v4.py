"""
app_v4.py — Streamlit · Visão V4: Composição e Participação (Bloco 7)
TabloFlow · Módulo 1 · TabloAnálise

Fluxo obrigatório:
    Arquivo → motor_upload.process_file → UploadResult
           → motor_base.processar_motor_base → MotorResult
           → visao_v4.executar_v4 → V4Result
           → Exportação Excel
"""

from __future__ import annotations

import io
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st

from motor_upload import UploadResult, process_file
from motor_base import MotorResult, processar_motor_base
from visao_v4 import (
    AgrupadorConfig,
    DistribuicaoPorDimensao,
    MedidaConfig,
    V4Config,
    V4Result,
    executar_v4,
)


# ---------------------------------------------------------------------------
# Configuração da página
# ---------------------------------------------------------------------------

st.set_page_config(page_title="TabloFlow — V4 Composição", layout="wide")
st.title("TabloFlow — V4: Composição e Participação")
st.caption(
    "Revela como um total é composto: quanto cada elemento representa dentro do todo."
)


MODO_LABELS: dict[str, int] = {
    "Composição Simples": 1,
    "Curva ABC": 2,
    "Comparação de Distribuição": 3,
}

ESTRUTURA_LABELS: dict[str, str] = {
    "Por Coluna": "coluna",
    "Por Linha": "linha",
}

MODO_SLUGS: dict[int, str] = {
    1: "comp_simples",
    2: "curva_abc",
    3: "comp_dist",
}


# ---------------------------------------------------------------------------
# Helpers de estado
# ---------------------------------------------------------------------------

def _init_state() -> None:
    """Inicializa session_state com valores padrão (evita KeyError)."""
    defaults: dict[str, object] = {
        "tmp_path": None,
        "file_name": None,
        "file_size": None,
        "upload_result": None,
        "motor_result": None,
        "step2_ready": False,
        "step3_ready": False,
        "v4_result": None,
        "v4_config": None,
        "estrutura_label": "Por Coluna",
        "modo_label": "Composição Simples",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _reset_downstream() -> None:
    """Zera todos os estados derivados quando o arquivo ou a aba muda."""
    st.session_state.motor_result = None
    st.session_state.step2_ready = False
    st.session_state.step3_ready = False
    st.session_state.v4_result = None
    st.session_state.v4_config = None


def _save_tmp_file(data: bytes, suffix: str) -> str:
    """Grava bytes num arquivo temporário e retorna o caminho absoluto."""
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "wb") as f:
        f.write(data)
    return path


# ---------------------------------------------------------------------------
# Helpers analíticos
# ---------------------------------------------------------------------------

def _colunas_por_tipo(motor_result: MotorResult) -> tuple[list[str], list[str]]:
    """Retorna (categóricas, numéricas) a partir do MotorResult."""
    categoricas: list[str] = []
    numericas: list[str] = []
    for c in motor_result.colunas:
        if c.tipo == "numeric":
            numericas.append(c.nome)
        elif c.tipo in ("text", "boolean", "date", "mixed"):
            categoricas.append(c.nome)
    return categoricas, numericas


def _classificar_simples(part_pct: float) -> str:
    """Classifica participação % em faixas DOMINANTE/ALTO/MÉDIO/BAIXO/ZERO."""
    if part_pct == 0.0:
        return "ZERO"
    if part_pct > 50.0:
        return "DOMINANTE"
    if part_pct > 20.0:
        return "ALTO"
    if part_pct > 5.0:
        return "MÉDIO"
    return "BAIXO"


def _dist_to_df(dist: DistribuicaoPorDimensao, modo: int) -> pd.DataFrame:
    """Converte uma DistribuicaoPorDimensao em DataFrame para exibição."""
    rows: list[dict[str, object]] = []
    for e in dist.elementos:
        row: dict[str, object] = {
            dist.dimensao: e.agrupador,
            "valor": round(e.valor_agregado, 2),
            "participação%": round(e.participacao_pct, 2),
            "acumulado%": round(e.participacao_acumulada_pct, 2),
            "ranking": e.ranking,
        }
        if modo == 1:
            row["classificação"] = _classificar_simples(e.participacao_pct)
        else:
            row["faixa_abc"] = e.classe_abc or ""
        rows.append(row)
    return pd.DataFrame(rows)


def _build_excel(v4: V4Result, config: V4Config) -> bytes:
    """Gera o arquivo Excel com abas Análise / Resumo / Configuração (+Divergências no Modo 3)."""
    try:
        import xlsxwriter  # noqa: F401
        engine = "xlsxwriter"
    except ImportError:
        engine = "openpyxl"

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine=engine) as writer:
        # Aba Análise — todas as distribuições concatenadas
        analise_rows: list[dict[str, object]] = []
        for dist in v4.distribuicoes:
            for e in dist.elementos:
                analise_rows.append({
                    "dimensão": dist.dimensao,
                    "medida": dist.medida,
                    "elemento": e.agrupador,
                    "valor": e.valor_agregado,
                    "participação%": round(e.participacao_pct, 4),
                    "ranking": e.ranking,
                    "acumulado%": round(e.participacao_acumulada_pct, 4),
                    "faixa_abc": e.classe_abc or "",
                    "classificação": (
                        _classificar_simples(e.participacao_pct) if v4.modo == 1 else ""
                    ),
                })
        pd.DataFrame(analise_rows).to_excel(writer, sheet_name="Análise", index=False)

        # Aba Resumo — totalizadores por distribuição
        resumo_rows: list[dict[str, object]] = []
        for dist in v4.distribuicoes:
            resumo_rows.append({
                "dimensão": dist.dimensao,
                "medida": dist.medida,
                "total_geral": dist.total_geral,
                "n_elementos": dist.n_elementos,
                "n_classe_a": dist.n_classe_a if dist.n_classe_a is not None else "",
                "n_classe_b": dist.n_classe_b if dist.n_classe_b is not None else "",
                "n_classe_c": dist.n_classe_c if dist.n_classe_c is not None else "",
                "pct_total_classe_a": (
                    round(dist.pct_total_classe_a, 4)
                    if dist.pct_total_classe_a is not None else ""
                ),
                "alerta_concentracao_critica": dist.alerta_concentracao_critica,
            })
        pd.DataFrame(resumo_rows).to_excel(writer, sheet_name="Resumo", index=False)

        # Aba Divergências — apenas Modo 3
        if v4.modo == 3 and v4.divergencias:
            div_rows = [{
                "agrupador": d.agrupador,
                "medida_a": d.medida_a,
                "medida_b": d.medida_b,
                "classe_a": d.classe_medida_a,
                "classe_b": d.classe_medida_b,
                "delta_ranking": d.delta_ranking,
                "inverteu_posicao": d.inverteu_posicao,
            } for d in v4.divergencias]
            pd.DataFrame(div_rows).to_excel(writer, sheet_name="Divergências", index=False)

        # Aba Configuração — parâmetros usados
        cfg_rows: list[dict[str, object]] = [
            {"parâmetro": "modo", "valor": config.modo},
            {"parâmetro": "estrutura_entrada", "valor": config.estrutura_entrada},
            {"parâmetro": "limiar_a", "valor": config.limiar_a},
            {"parâmetro": "limiar_b", "valor": config.limiar_b},
        ]
        for m in config.medidas:
            cfg_rows.append({
                "parâmetro": f"medida[{m.campo}]",
                "valor": f"{m.nome_analitico} ({m.tipo})",
            })
        for a in config.agrupadores:
            cfg_rows.append({"parâmetro": f"agrupador[{a.campo}]", "valor": a.nome})
        pd.DataFrame(cfg_rows).to_excel(writer, sheet_name="Configuração", index=False)

    buffer.seek(0)
    return buffer.getvalue()


# ---------------------------------------------------------------------------
# Inicialização
# ---------------------------------------------------------------------------

_init_state()


# ---------------------------------------------------------------------------
# ETAPA 1 — Upload e Identificação
# ---------------------------------------------------------------------------

st.header("Etapa 1 — Upload e Identificação")

uploaded = st.file_uploader(
    "Envie um arquivo .xlsx, .xls ou .csv",
    type=["xlsx", "xls", "csv"],
    key="uploader",
)

if uploaded is None:
    st.info("Selecione um arquivo para começar.")
    st.stop()

# Detectar arquivo novo — salvar em tmp e reprocessar
file_bytes = uploaded.getvalue()
file_name = uploaded.name
file_size = len(file_bytes)
file_changed = (
    st.session_state.file_name != file_name
    or st.session_state.file_size != file_size
)

if file_changed:
    suffix = Path(file_name).suffix
    st.session_state.tmp_path = _save_tmp_file(file_bytes, suffix)
    st.session_state.file_name = file_name
    st.session_state.file_size = file_size
    st.session_state.upload_result = process_file(st.session_state.tmp_path)
    _reset_downstream()

upload_result: Optional[UploadResult] = st.session_state.upload_result

if upload_result is None:
    st.error("Erro interno: UploadResult indisponível.")
    st.stop()

if not upload_result.success:
    st.error("Falha no Motor de Upload:")
    for err in upload_result.errors:
        st.error(err)
    st.stop()

# Seleção de aba para Excel multi-aba ainda não resolvida
needs_sheet = (
    len(upload_result.available_sheets) > 1
    and upload_result.row_count == 0
)

if needs_sheet:
    st.info(
        f"Arquivo com {len(upload_result.available_sheets)} abas — escolha qual processar."
    )
    sheet_choice = st.selectbox(
        "Aba", upload_result.available_sheets, key="sheet_picker"
    )
    if st.button("Carregar aba", key="btn_load_sheet"):
        st.session_state.upload_result = process_file(
            st.session_state.tmp_path, sheet_name=sheet_choice
        )
        _reset_downstream()
        upload_result = st.session_state.upload_result
        if not upload_result.success:
            for err in upload_result.errors:
                st.error(err)
            st.stop()
    else:
        st.stop()

# Processar Motor Base (uma única vez por arquivo/aba)
if st.session_state.motor_result is None:
    st.session_state.motor_result = processar_motor_base(upload_result)

motor_result: MotorResult = st.session_state.motor_result

if not motor_result.success:
    st.error("Falha no Motor Base:")
    for err in motor_result.errors:
        st.error(err)
    st.stop()

# Resumo
col1, col2, col3, col4 = st.columns(4)
col1.metric("Arquivo", motor_result.source_file)
col2.metric("Aba", motor_result.aba_processada or "—")
col3.metric("Linhas", motor_result.n_linhas)
col4.metric("Colunas", motor_result.n_colunas)

# Warnings (upload + motor_base)
for w in upload_result.warnings:
    st.warning(f"[upload] {w}")
for w in motor_result.warnings:
    st.warning(f"[motor_base] {w}")

if st.button("Confirmar estrutura", key="btn_confirma_estrutura"):
    st.session_state.step2_ready = True


# ---------------------------------------------------------------------------
# ETAPA 2 — Estrutura de Entrada e Modo de Análise
# ---------------------------------------------------------------------------

if st.session_state.step2_ready:
    st.header("Etapa 2 — Estrutura de Entrada e Modo de Análise")

    estrutura_label = st.selectbox(
        "Estrutura de Entrada",
        list(ESTRUTURA_LABELS.keys()),
        index=list(ESTRUTURA_LABELS.keys()).index(st.session_state.estrutura_label),
        key="sel_estrutura",
        help=(
            "Por Coluna: cada coluna é uma medida separada.\n"
            "Por Linha: medidas empilhadas numa coluna única de valor."
        ),
    )
    modo_label = st.selectbox(
        "Modo de Análise",
        list(MODO_LABELS.keys()),
        index=list(MODO_LABELS.keys()).index(st.session_state.modo_label),
        key="sel_modo",
        help=(
            "Composição Simples: participação % por elemento.\n"
            "Curva ABC: classificação A/B/C por concentração acumulada.\n"
            "Comparação de Distribuição: compara a Curva ABC entre múltiplas medidas."
        ),
    )

    if st.button("Confirmar modo", key="btn_confirma_modo"):
        st.session_state.estrutura_label = estrutura_label
        st.session_state.modo_label = modo_label
        st.session_state.step3_ready = True
        st.session_state.v4_result = None
        st.session_state.v4_config = None


# ---------------------------------------------------------------------------
# ETAPA 3 — Configuração Principal (varia por modo)
# ---------------------------------------------------------------------------

if st.session_state.step3_ready:
    st.header("Etapa 3 — Configuração")

    categoricas, numericas = _colunas_por_tipo(motor_result)
    modo = MODO_LABELS[st.session_state.modo_label]
    estrutura = ESTRUTURA_LABELS[st.session_state.estrutura_label]

    if not categoricas:
        st.error("Nenhuma coluna categórica detectada no arquivo.")
        st.stop()
    if not numericas:
        st.error("Nenhuma coluna numérica detectada no arquivo.")
        st.stop()

    # Placeholders (evita UnboundLocalError entre branches)
    dimensao: str = categoricas[0]
    medida_unica: str = numericas[0]
    nome_analitico: str = numericas[0]
    agrup_extras: list[str] = []
    medidas_sel: list[str] = numericas[:2] if len(numericas) >= 2 else numericas
    limiar_a: float = 0.80
    limiar_b: float = 0.95

    with st.form("form_config"):
        if modo == 1:
            st.subheader("Composição Simples")
            dimensao = st.selectbox("Dimensão", categoricas, key="cfg_dim_m1")
            medida_unica = st.selectbox("Medida", numericas, key="cfg_med_m1")
            nome_analitico = st.text_input(
                "Nome analítico da medida",
                value=medida_unica,
                key="cfg_nome_m1",
            )
            outras = [c for c in categoricas if c != dimensao]
            agrup_extras = st.multiselect(
                "Agrupadores adicionais (opcional)",
                outras,
                key="cfg_extras_m1",
            )

        elif modo == 2:
            st.subheader("Curva ABC")
            dimensao = st.selectbox("Item", categoricas, key="cfg_dim_m2")
            medida_unica = st.selectbox("Medida", numericas, key="cfg_med_m2")
            nome_analitico = st.text_input(
                "Nome analítico da medida",
                value=medida_unica,
                key="cfg_nome_m2",
            )
            c1, c2 = st.columns(2)
            limiar_a_pct = c1.number_input(
                "Limiar A (%)",
                value=80.0, min_value=1.0, max_value=99.0, step=1.0,
                key="cfg_la_m2",
            )
            limiar_b_pct = c2.number_input(
                "Limiar B (%)",
                value=95.0, min_value=1.0, max_value=99.9, step=1.0,
                key="cfg_lb_m2",
            )
            limiar_a = float(limiar_a_pct) / 100.0
            limiar_b = float(limiar_b_pct) / 100.0
            outras = [c for c in categoricas if c != dimensao]
            agrup_extras = st.multiselect(
                "Agrupadores adicionais (opcional)",
                outras,
                key="cfg_extras_m2",
            )

        else:  # modo == 3
            st.subheader("Comparação de Distribuição")
            st.caption(
                "Compara a Curva ABC da mesma dimensão entre múltiplas medidas "
                "(conforme spec_v4.md §3). Requer ao menos 2 medidas."
            )
            dimensao = st.selectbox("Dimensão", categoricas, key="cfg_dim_m3")
            medidas_sel = st.multiselect(
                "Medidas (mínimo 2)",
                numericas,
                default=numericas[:2] if len(numericas) >= 2 else numericas,
                key="cfg_medidas_m3",
            )
            c1, c2 = st.columns(2)
            limiar_a_pct = c1.number_input(
                "Limiar A (%)",
                value=80.0, min_value=1.0, max_value=99.0, step=1.0,
                key="cfg_la_m3",
            )
            limiar_b_pct = c2.number_input(
                "Limiar B (%)",
                value=95.0, min_value=1.0, max_value=99.9, step=1.0,
                key="cfg_lb_m3",
            )
            limiar_a = float(limiar_a_pct) / 100.0
            limiar_b = float(limiar_b_pct) / 100.0

        submitted = st.form_submit_button("Analisar")

    if submitted:
        try:
            if modo in (1, 2):
                medidas_cfg = [MedidaConfig(
                    campo=medida_unica,
                    nome_analitico=nome_analitico or medida_unica,
                    tipo="numero",
                )]
                agrups_cfg = [AgrupadorConfig(campo=dimensao, nome=dimensao)]
                for extra in agrup_extras:
                    agrups_cfg.append(AgrupadorConfig(campo=extra, nome=extra))
            else:
                if len(medidas_sel) < 2:
                    st.error("Modo 3 requer pelo menos 2 medidas selecionadas.")
                    st.stop()
                medidas_cfg = [
                    MedidaConfig(campo=m, nome_analitico=m, tipo="numero")
                    for m in medidas_sel
                ]
                agrups_cfg = [AgrupadorConfig(campo=dimensao, nome=dimensao)]

            config = V4Config(
                modo=modo,
                estrutura_entrada=estrutura,
                medidas=medidas_cfg,
                agrupadores=agrups_cfg,
                limiar_a=limiar_a,
                limiar_b=limiar_b,
            )
            st.session_state.v4_config = config
            st.session_state.v4_result = executar_v4(motor_result, config)
        except Exception as exc:
            st.error(f"Erro durante a análise: {exc}")
            st.stop()


# ---------------------------------------------------------------------------
# ETAPA 4 — Microanálise Prévia
# ---------------------------------------------------------------------------

if st.session_state.v4_result is not None:
    st.header("Etapa 4 — Microanálise Prévia")

    v4: V4Result = st.session_state.v4_result
    config: V4Config = st.session_state.v4_config

    for w in v4.warnings:
        st.warning(w)
    if v4.errors:
        for e in v4.errors:
            st.error(e)

    if not v4.success or not v4.distribuicoes:
        st.error("Análise não pôde ser concluída.")
        st.stop()

    if v4.modo == 1:
        for dist in v4.distribuicoes:
            st.subheader(f"{dist.dimensao} × {dist.medida}")
            st.metric("Total", f"{dist.total_geral:,.2f}")
            df = _dist_to_df(dist, 1)
            st.dataframe(df, use_container_width=True)
            dominantes = [
                e.agrupador for e in dist.elementos if e.participacao_pct > 50.0
            ]
            if dominantes:
                st.success(f"Elemento DOMINANTE: {', '.join(dominantes)}")
            if dist.alerta_concentracao_critica:
                st.warning("Concentração crítica (elemento > 50% do total).")

    elif v4.modo == 2:
        for dist in v4.distribuicoes:
            st.subheader(f"{dist.dimensao} × {dist.medida}")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total", f"{dist.total_geral:,.2f}")
            c2.metric("Itens A", dist.n_classe_a or 0)
            c3.metric("Itens B", dist.n_classe_b or 0)
            c4.metric("Itens C", dist.n_classe_c or 0)
            df = _dist_to_df(dist, 2)
            st.dataframe(df, use_container_width=True)
            if dist.pct_total_classe_a is not None:
                st.caption(
                    f"Classe A concentra {dist.pct_total_classe_a:.1f}% do total."
                )
            if dist.alerta_concentracao_critica:
                st.warning("Concentração crítica (elemento > 50% do total).")

    else:  # modo 3
        por_dim: dict[str, list[DistribuicaoPorDimensao]] = {}
        for d in v4.distribuicoes:
            por_dim.setdefault(d.dimensao, []).append(d)

        for dim, dists in por_dim.items():
            st.subheader(f"Dimensão: {dim}")
            for d in dists:
                st.markdown(f"**Medida: {d.medida}**")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Total", f"{d.total_geral:,.2f}")
                c2.metric("Itens A", d.n_classe_a or 0)
                c3.metric("Itens B", d.n_classe_b or 0)
                c4.metric("Itens C", d.n_classe_c or 0)
                df = _dist_to_df(d, 3)
                st.dataframe(df, use_container_width=True)

        if v4.divergencias:
            st.subheader("Mapa de Divergências")
            div_rows = [{
                "agrupador": d.agrupador,
                "medida_a": d.medida_a,
                "medida_b": d.medida_b,
                "classe_a": d.classe_medida_a,
                "classe_b": d.classe_medida_b,
                "delta_ranking": d.delta_ranking,
                "inverteu": d.inverteu_posicao,
            } for d in v4.divergencias]
            st.dataframe(pd.DataFrame(div_rows), use_container_width=True)


# ---------------------------------------------------------------------------
# ETAPA 5 — Exportação
# ---------------------------------------------------------------------------

if (
    st.session_state.v4_result is not None
    and st.session_state.v4_result.success
    and st.session_state.v4_result.distribuicoes
):
    st.header("Etapa 5 — Exportação")

    v4 = st.session_state.v4_result
    config = st.session_state.v4_config

    try:
        xlsx_bytes = _build_excel(v4, config)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"V4_{MODO_SLUGS[v4.modo]}_{ts}.xlsx"
        st.download_button(
            label="Exportar Excel",
            data=xlsx_bytes,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="btn_download",
        )
    except Exception as exc:
        st.error(f"Erro ao gerar Excel: {exc}")
