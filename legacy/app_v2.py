"""
app_v2.py — Streamlit · Visão V2: Análise Comparativa entre Referências (Bloco 8)
TabloFlow · Módulo 1 · TabloAnálise

Fluxo obrigatório:
    Arquivo → motor_upload.process_file → UploadResult
           → motor_base.processar_motor_base → MotorResult
           → visao_v2.executar_v2 → V2Result
           → Exportação Excel (4 abas)

Decisões respeitadas: D-001 (SURGIMENTO/DESAPARECIMENTO), D-002 (W07),
D-003 (sem arredondar variacao_percentual no contrato), D-004 (nulo ≠ zero).
"""

from __future__ import annotations

import io
import os
import re
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import pandas as pd
import streamlit as st

from motor_upload import UploadResult, process_file
from motor_base import MotorResult, processar_motor_base
from visao_v2 import V2Result, executar_v2


# ---------------------------------------------------------------------------
# Configuração da página
# ---------------------------------------------------------------------------

st.set_page_config(page_title="TabloFlow — V2 Comparativa", layout="wide")
st.title("TabloFlow — V2: Análise Comparativa entre Referências")
st.caption(
    "Compara dois estados (Referência A e B) de um mesmo campo dentro de um "
    "mesmo recorte analítico."
)


ESTRUTURA_LABELS: dict[str, str] = {
    "Por Colunas": "POR_COLUNAS",
    "Por Linhas": "POR_LINHAS",
}

TIPO_CAMPO_OPTIONS: list[str] = ["VALOR", "PERCENTUAL", "INDICE"]
SEMANTICA_OPTIONS: list[str] = ["MAIOR_E_MELHOR", "MENOR_E_MELHOR", "NEUTRO"]

CORES_CLASSIFICACAO: dict[str, str] = {
    "MELHORA": "#1b7e3d",
    "PIORA": "#b42a2a",
    "SEM_VARIACAO": "#5c5c5c",
    "VARIACAO_NEUTRA": "#2a4fa3",
    "SURGIMENTO": "#7a2ea6",
    "DESAPARECIMENTO": "#b8590e",
}

ICONES_FLAG: dict[str, str] = {
    "SURGIMENTO": "🟣",
    "DESAPARECIMENTO": "🟠",
}

MAX_CAMPOS = 10
MAX_AGRUPADORES = 5


# ---------------------------------------------------------------------------
# Helpers de estado
# ---------------------------------------------------------------------------

def _init_state() -> None:
    """Inicializa session_state com valores padrão."""
    defaults: dict[str, object] = {
        "tmp_path": None,
        "file_name": None,
        "file_size": None,
        "file_ext": None,
        "selected_sheet": None,
        "upload_result": None,
        "motor_result": None,
        "full_df": None,
        "estrutura_entrada": "POR_COLUNAS",
        "campo_discriminador": None,
        "valor_ref_a": None,
        "valor_ref_b": None,
        "nome_ref_a": "Referência A",
        "nome_ref_b": "Referência B",
        "n_campos": 1,
        "campos_cfg": [],
        "agrupadores_sel": [],
        "v2_result": None,
        "tema_excel": "Claro",
        "nome_visao": "analise_v2",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _reset_downstream_from_file() -> None:
    """Zera estados derivados quando o arquivo muda."""
    st.session_state.selected_sheet = None
    st.session_state.upload_result = None
    _reset_downstream_from_sheet()


def _reset_downstream_from_sheet() -> None:
    """Zera estados derivados quando a aba muda."""
    st.session_state.motor_result = None
    st.session_state.full_df = None
    _reset_downstream_from_config()


def _reset_downstream_from_config() -> None:
    """Zera o resultado analítico quando a configuração muda."""
    st.session_state.v2_result = None


def _save_tmp_file(data: bytes, suffix: str) -> str:
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "wb") as f:
        f.write(data)
    return path


# ---------------------------------------------------------------------------
# Workaround pré-existente: motor_base.df contém apenas o preview (5 linhas).
# Para habilitar análise real, app_v2 re-lê o arquivo original e substitui
# motor_result.df pelo DataFrame completo — sem modificar os motores.
# ---------------------------------------------------------------------------

def _carregar_df_completo(tmp_path: str, ext: str, sheet_name: Optional[str]) -> pd.DataFrame:
    """Re-lê o arquivo bruto para obter o DataFrame completo."""
    if ext.lower() in (".xlsx", ".xls"):
        return pd.read_excel(tmp_path, sheet_name=sheet_name)
    if ext.lower() == ".csv":
        return pd.read_csv(tmp_path)
    raise ValueError(f"Extensão não suportada: {ext}")


def _montar_motor_result_completo(
    motor_result: MotorResult, full_df: pd.DataFrame
) -> MotorResult:
    """Cria um MotorResult idêntico ao recebido, porém com df completo."""
    return MotorResult(
        success=motor_result.success,
        source_file=motor_result.source_file,
        aba_processada=motor_result.aba_processada,
        n_linhas=len(full_df),
        n_colunas=len(full_df.columns),
        colunas=motor_result.colunas,
        warnings=motor_result.warnings,
        errors=motor_result.errors,
        df=full_df,
    )


# ---------------------------------------------------------------------------
# Helpers analíticos
# ---------------------------------------------------------------------------

def _colunas_por_tipo(motor_result: MotorResult) -> tuple[list[str], list[str]]:
    """Separa colunas em (categóricas, numéricas) a partir do MotorResult."""
    categoricas: list[str] = []
    numericas: list[str] = []
    for c in motor_result.colunas:
        if c.tipo == "numeric":
            numericas.append(c.nome)
        else:
            categoricas.append(c.nome)
    return categoricas, numericas


def _todas_colunas(motor_result: MotorResult) -> list[str]:
    return [c.nome for c in motor_result.colunas]


def _sugerir_tipo(nome_col: str) -> str:
    """Heurística leve a partir do nome da coluna."""
    nome_low = nome_col.lower()
    if any(p in nome_low for p in ("margem", "taxa", "percent", "pct", "%")):
        return "PERCENTUAL"
    if any(p in nome_low for p in ("nps", "indice", "índice", "score", "rating")):
        return "INDICE"
    return "VALOR"


def _sugerir_semantica(nome_analitico: str) -> str:
    """Sugere semântica com base em palavras comuns do nome analítico."""
    nome_low = nome_analitico.lower()
    if any(p in nome_low for p in ("custo", "despesa", "prazo", "defeito", "erro", "cancelamento")):
        return "MENOR_E_MELHOR"
    if any(p in nome_low for p in ("headcount", "quantidade", "qtd", "sku")):
        return "NEUTRO"
    return "MAIOR_E_MELHOR"


def _fmt_num(v: Optional[float]) -> str:
    """Formata um float numérico para exibição (None → '—')."""
    if v is None or pd.isna(v):
        return "—"
    return f"{v:,.2f}"


def _fmt_pct(v: Optional[float]) -> str:
    """Formata variação percentual (D-003: formato 2 casas — {:.2%})."""
    if v is None or pd.isna(v):
        return "—"
    return f"{v:.2%}"


def _slug(value: str) -> str:
    """Remove caracteres não seguros para um nome de arquivo."""
    cleaned = re.sub(r"[^A-Za-z0-9_\-]+", "_", value.strip())
    return cleaned.strip("_") or "sem_nome"


# ---------------------------------------------------------------------------
# Construção de DataFrames para exibição
# ---------------------------------------------------------------------------

def _registros_para_df(v2: V2Result) -> pd.DataFrame:
    """Converte registros do V2Result em DataFrame linear para exibição/exportação."""
    rows: list[dict[str, Any]] = []
    for r in v2.registros:
        base: dict[str, Any] = dict(r.agrupadores)
        base.update({
            "campo": r.campo,
            "tipo_campo": r.tipo_campo,
            "semantica": r.semantica,
            "valor_a": r.valor_a,
            "valor_b": r.valor_b,
            "variacao_absoluta": r.variacao_absoluta,
            "variacao_percentual": r.variacao_percentual,
            "classificacao": r.classificacao,
            "flag": r.flag or "",
        })
        rows.append(base)
    if not rows:
        return pd.DataFrame()
    colunas_ag = v2.agrupadores
    colunas_fixas = [
        "campo", "tipo_campo", "semantica",
        "valor_a", "valor_b",
        "variacao_absoluta", "variacao_percentual",
        "classificacao", "flag",
    ]
    df = pd.DataFrame(rows)
    ordem = [c for c in colunas_ag if c in df.columns] + [
        c for c in colunas_fixas if c in df.columns
    ]
    return df[ordem]


def _resumo_para_df(v2: V2Result) -> pd.DataFrame:
    """Converte o resumo por agrupador em DataFrame."""
    rows = [{
        "agrupador": r.agrupador,
        "valor": r.valor,
        "campo": r.campo,
        "total_a": r.total_a,
        "total_b": r.total_b,
        "variacao_absoluta": r.variacao_absoluta,
        "variacao_percentual": r.variacao_percentual,
        "classificacao_predominante": r.classificacao_predominante,
    } for r in v2.resumo_por_agrupador]
    return pd.DataFrame(rows)


def _estilizar_registros(df: pd.DataFrame) -> Any:
    """Aplica cor por classificação e destaque para SURGIMENTO/DESAPARECIMENTO (D-001)."""
    if df.empty:
        return df

    def _cor_linha(row: pd.Series) -> list[str]:
        flag = row.get("flag", "")
        classif = row.get("classificacao", "")
        if flag in ("SURGIMENTO", "DESAPARECIMENTO"):
            bg = "#f6e1a7" if flag == "SURGIMENTO" else "#f4c9a3"
            return [f"background-color: {bg}; font-weight: 600"] * len(row)
        cor = CORES_CLASSIFICACAO.get(classif)
        if cor:
            return [f"color: {cor}"] * len(row)
        return [""] * len(row)

    styler = df.style.apply(_cor_linha, axis=1)
    styler = styler.format({
        "valor_a": lambda v: _fmt_num(v),
        "valor_b": lambda v: _fmt_num(v),
        "variacao_absoluta": lambda v: _fmt_num(v),
        "variacao_percentual": lambda v: _fmt_pct(v),
    })
    return styler


# ---------------------------------------------------------------------------
# Exportação Excel (4 abas + tema claro/escuro)
# ---------------------------------------------------------------------------

def _paleta_tema(tema: str) -> dict[str, str]:
    if tema == "Escuro":
        return {
            "header_bg": "#1f2937",
            "header_fg": "#ffffff",
            "row_alt": "#111827",
            "row_txt": "#e5e7eb",
            "surgimento": "#3b2a5b",
            "desaparecimento": "#5b3a1a",
        }
    return {
        "header_bg": "#1f4e79",
        "header_fg": "#ffffff",
        "row_alt": "#f5f7fa",
        "row_txt": "#1a1a1a",
        "surgimento": "#f6e1a7",
        "desaparecimento": "#f4c9a3",
    }


def _build_excel(
    v2: V2Result,
    cfg_parametros: dict[str, Any],
    tema: str,
) -> bytes:
    """Gera o Excel com 4 abas e formatação de tema."""
    buffer = io.BytesIO()
    paleta = _paleta_tema(tema)

    try:
        import xlsxwriter  # noqa: F401
        engine = "xlsxwriter"
    except ImportError:
        engine = "openpyxl"

    df_registros = _registros_para_df(v2)
    df_resumo = _resumo_para_df(v2)
    df_flags = (
        df_registros[df_registros["flag"].isin(["SURGIMENTO", "DESAPARECIMENTO"])]
        if not df_registros.empty and "flag" in df_registros.columns
        else pd.DataFrame()
    )

    # Parâmetros
    param_rows: list[dict[str, Any]] = [
        {"parâmetro": "visao", "valor": "V2"},
        {"parâmetro": "nome_visao", "valor": cfg_parametros.get("nome_visao", "")},
        {"parâmetro": "estrutura_entrada", "valor": v2.estrutura_entrada},
        {"parâmetro": "nome_referencia_a", "valor": v2.nome_referencia_a},
        {"parâmetro": "nome_referencia_b", "valor": v2.nome_referencia_b},
    ]
    if v2.estrutura_entrada == "POR_LINHAS":
        param_rows.extend([
            {"parâmetro": "campo_discriminador",
             "valor": cfg_parametros.get("campo_discriminador", "")},
            {"parâmetro": "valor_ref_a",
             "valor": cfg_parametros.get("valor_ref_a", "")},
            {"parâmetro": "valor_ref_b",
             "valor": cfg_parametros.get("valor_ref_b", "")},
        ])
    for i, campo in enumerate(cfg_parametros.get("campos_cfg", []), start=1):
        param_rows.append({
            "parâmetro": f"campo_{i}",
            "valor": (
                f"{campo['nome_analitico']} "
                f"({campo['tipo_campo']}, {campo['semantica']})"
            ),
        })
    for i, ag in enumerate(v2.agrupadores, start=1):
        param_rows.append({"parâmetro": f"agrupador_{i}", "valor": ag})
    for w in v2.warnings:
        param_rows.append({"parâmetro": "warning", "valor": w})
    df_params = pd.DataFrame(param_rows)

    with pd.ExcelWriter(buffer, engine=engine) as writer:
        df_registros.to_excel(writer, sheet_name="Análise Detalhada", index=False)
        df_resumo.to_excel(writer, sheet_name="Resumo por Agrupador", index=False)
        df_flags.to_excel(writer, sheet_name="Surgimentos e Desaparecimentos", index=False)
        df_params.to_excel(writer, sheet_name="Parâmetros", index=False)

        if engine == "xlsxwriter":
            wb = writer.book
            header_fmt = wb.add_format({
                "bold": True,
                "bg_color": paleta["header_bg"],
                "font_color": paleta["header_fg"],
                "border": 1,
                "align": "center",
                "valign": "vcenter",
            })
            pct_fmt = wb.add_format({"num_format": "0.00%"})  # D-003
            num_fmt = wb.add_format({"num_format": "#,##0.00"})
            surg_fmt = wb.add_format({"bg_color": paleta["surgimento"]})
            desap_fmt = wb.add_format({"bg_color": paleta["desaparecimento"]})

            # Formatação por aba
            for sheet_name, df in [
                ("Análise Detalhada", df_registros),
                ("Resumo por Agrupador", df_resumo),
                ("Surgimentos e Desaparecimentos", df_flags),
                ("Parâmetros", df_params),
            ]:
                ws = writer.sheets[sheet_name]
                if df.empty:
                    ws.write(0, 0, "(sem registros)")
                    continue
                # Cabeçalho
                for col_idx, col_name in enumerate(df.columns):
                    ws.write(0, col_idx, col_name, header_fmt)
                ws.set_row(0, 22)
                # Larguras
                for col_idx, col_name in enumerate(df.columns):
                    largura = max(12, min(28, int(df[col_name].astype(str).str.len().max() or 12) + 2))
                    ws.set_column(col_idx, col_idx, largura)
                # Formato percentual e numérico (D-003: 0.00% preserva float original)
                if "variacao_percentual" in df.columns:
                    idx = df.columns.get_loc("variacao_percentual")
                    ws.set_column(idx, idx, 14, pct_fmt)
                for col in ("valor_a", "valor_b", "variacao_absoluta",
                            "total_a", "total_b"):
                    if col in df.columns:
                        idx = df.columns.get_loc(col)
                        ws.set_column(idx, idx, 14, num_fmt)
                # Destaque SURGIMENTO/DESAPARECIMENTO
                if "flag" in df.columns:
                    for r_idx, flag in enumerate(df["flag"].tolist(), start=1):
                        if flag == "SURGIMENTO":
                            ws.set_row(r_idx, None, surg_fmt)
                        elif flag == "DESAPARECIMENTO":
                            ws.set_row(r_idx, None, desap_fmt)
                ws.freeze_panes(1, 0)

    buffer.seek(0)
    return buffer.getvalue()


# ---------------------------------------------------------------------------
# Inicialização
# ---------------------------------------------------------------------------

_init_state()


# ---------------------------------------------------------------------------
# ETAPA 1 — Upload e Estrutura
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

file_bytes = uploaded.getvalue()
file_name = uploaded.name
file_size = len(file_bytes)
ext = Path(file_name).suffix

file_changed = (
    st.session_state.file_name != file_name
    or st.session_state.file_size != file_size
)

if file_changed:
    st.session_state.tmp_path = _save_tmp_file(file_bytes, ext)
    st.session_state.file_name = file_name
    st.session_state.file_size = file_size
    st.session_state.file_ext = ext
    st.session_state.upload_result = process_file(st.session_state.tmp_path)
    _reset_downstream_from_file()
    st.session_state.upload_result = process_file(st.session_state.tmp_path)

upload_result: Optional[UploadResult] = st.session_state.upload_result
if upload_result is None or not upload_result.success:
    st.error("Falha no Motor de Upload:")
    if upload_result is not None:
        for err in upload_result.errors:
            st.error(err)
    st.stop()

# Seletor de aba (quando múltiplas)
abas = upload_result.available_sheets
if abas and len(abas) > 1:
    default_idx = (
        abas.index(st.session_state.selected_sheet)
        if st.session_state.selected_sheet in abas else 0
    )
    sheet_choice = st.selectbox("Aba a processar", abas, index=default_idx, key="sel_sheet")
    if sheet_choice != st.session_state.selected_sheet:
        st.session_state.selected_sheet = sheet_choice
        _reset_downstream_from_sheet()
        st.session_state.upload_result = process_file(
            st.session_state.tmp_path, sheet_name=sheet_choice
        )
        upload_result = st.session_state.upload_result
else:
    st.session_state.selected_sheet = upload_result.sheet_name

if not upload_result.success:
    for err in upload_result.errors:
        st.error(err)
    st.stop()

# Motor base + workaround para df completo
if st.session_state.motor_result is None:
    mr = processar_motor_base(upload_result)
    if mr.success:
        full_df = _carregar_df_completo(
            st.session_state.tmp_path,
            st.session_state.file_ext,
            st.session_state.selected_sheet,
        )
        mr = _montar_motor_result_completo(mr, full_df)
    st.session_state.motor_result = mr
    st.session_state.full_df = mr.df

motor_result: MotorResult = st.session_state.motor_result
if not motor_result.success:
    st.error("Falha no Motor Base:")
    for err in motor_result.errors:
        st.error(err)
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Arquivo", motor_result.source_file)
col2.metric("Aba", motor_result.aba_processada or "—")
col3.metric("Linhas", motor_result.n_linhas)
col4.metric("Colunas", motor_result.n_colunas)

for w in upload_result.warnings:
    st.warning(f"[upload] {w}")
for w in motor_result.warnings:
    st.warning(f"[motor_base] {w}")

with st.expander("Tipos detectados por coluna", expanded=False):
    cols_info = pd.DataFrame([
        {"coluna": c.nome, "tipo": c.tipo, "n_unique": c.n_unique,
         "nulls": c.null_count}
        for c in motor_result.colunas
    ])
    st.dataframe(cols_info, use_container_width=True)


# ---------------------------------------------------------------------------
# ETAPA 1.2 — Estrutura de Entrada
# ---------------------------------------------------------------------------

st.subheader("Etapa 1.2 — Estrutura de Entrada")

estrutura_label = st.radio(
    "Como estão organizadas as referências A e B?",
    list(ESTRUTURA_LABELS.keys()),
    horizontal=True,
    index=list(ESTRUTURA_LABELS.values()).index(st.session_state.estrutura_entrada),
    help=(
        "Por Colunas: cada referência ocupa uma coluna distinta na mesma linha "
        "(ex.: Orçado × Realizado).\n"
        "Por Linhas: as referências compartilham a mesma coluna de valor, "
        "separadas por um campo discriminador (ex.: Periodo = Jan/24 / Jan/25)."
    ),
    key="radio_estrutura",
)
estrutura_nova = ESTRUTURA_LABELS[estrutura_label]
if estrutura_nova != st.session_state.estrutura_entrada:
    st.session_state.estrutura_entrada = estrutura_nova
    st.session_state.campos_cfg = []
    st.session_state.n_campos = 1
    _reset_downstream_from_config()

todas_cols = _todas_colunas(motor_result)
categoricas, numericas = _colunas_por_tipo(motor_result)

if st.session_state.estrutura_entrada == "POR_LINHAS":
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        disc_default = (
            st.session_state.campo_discriminador
            if st.session_state.campo_discriminador in todas_cols
            else (todas_cols[0] if todas_cols else None)
        )
        discriminador = st.selectbox(
            "Campo discriminador",
            todas_cols,
            index=todas_cols.index(disc_default) if disc_default in todas_cols else 0,
            key="sel_discriminador",
        )
    if discriminador != st.session_state.campo_discriminador:
        st.session_state.campo_discriminador = discriminador
        st.session_state.valor_ref_a = None
        st.session_state.valor_ref_b = None
        _reset_downstream_from_config()

    valores_distintos = sorted(
        motor_result.df[discriminador].dropna().astype(str).unique().tolist()
    )
    with col_d2:
        va_default = (
            st.session_state.valor_ref_a
            if st.session_state.valor_ref_a in valores_distintos
            else (valores_distintos[0] if valores_distintos else None)
        )
        valor_a = st.selectbox(
            "Valor que identifica a Referência A",
            valores_distintos,
            index=valores_distintos.index(va_default) if va_default in valores_distintos else 0,
            key="sel_val_ref_a",
        )
    with col_d3:
        # Default do B = segundo valor distinto, se houver
        demais = [v for v in valores_distintos if v != valor_a]
        vb_default = (
            st.session_state.valor_ref_b
            if st.session_state.valor_ref_b in demais
            else (demais[0] if demais else None)
        )
        opcoes_b = demais if demais else valores_distintos
        valor_b = st.selectbox(
            "Valor que identifica a Referência B",
            opcoes_b,
            index=opcoes_b.index(vb_default) if vb_default in opcoes_b else 0,
            key="sel_val_ref_b",
        )
    if (valor_a != st.session_state.valor_ref_a
            or valor_b != st.session_state.valor_ref_b):
        st.session_state.valor_ref_a = valor_a
        st.session_state.valor_ref_b = valor_b
        _reset_downstream_from_config()

    col_n1, col_n2 = st.columns(2)
    st.session_state.nome_ref_a = col_n1.text_input(
        "Nome analítico da Referência A",
        value=str(st.session_state.valor_ref_a or "Referência A"),
        key="in_nome_ref_a",
    )
    st.session_state.nome_ref_b = col_n2.text_input(
        "Nome analítico da Referência B",
        value=str(st.session_state.valor_ref_b or "Referência B"),
        key="in_nome_ref_b",
    )
else:
    col_n1, col_n2 = st.columns(2)
    st.session_state.nome_ref_a = col_n1.text_input(
        "Nome analítico da Referência A",
        value=st.session_state.nome_ref_a or "Referência A",
        key="in_nome_ref_a_pc",
    )
    st.session_state.nome_ref_b = col_n2.text_input(
        "Nome analítico da Referência B",
        value=st.session_state.nome_ref_b or "Referência B",
        key="in_nome_ref_b_pc",
    )


# ---------------------------------------------------------------------------
# ETAPA 2 — Configuração Principal
# ---------------------------------------------------------------------------

st.header("Etapa 2 — Configuração Principal")

# --- 2.1 Número de campos a comparar --------------------------------------
st.subheader("2.1 — Campos de comparação")

col_n, _ = st.columns([1, 3])
n_campos = col_n.number_input(
    "Quantos campos comparar?",
    min_value=1,
    max_value=MAX_CAMPOS,
    value=int(st.session_state.n_campos or 1),
    step=1,
    key="n_campos_input",
    help=f"Máximo: {MAX_CAMPOS} campos (limitador E06).",
)
if n_campos != st.session_state.n_campos:
    st.session_state.n_campos = int(n_campos)
    _reset_downstream_from_config()

campos_cfg: list[dict[str, Any]] = []
estrutura_atual = st.session_state.estrutura_entrada

if estrutura_atual == "POR_COLUNAS" and not numericas:
    st.error("Nenhuma coluna numérica detectada — V2 exige ao menos duas colunas numéricas.")
    st.stop()
if estrutura_atual == "POR_LINHAS" and not numericas:
    st.error("Nenhuma coluna numérica detectada — V2 exige ao menos uma coluna de valor numérica.")
    st.stop()

for i in range(int(st.session_state.n_campos)):
    with st.expander(f"Campo {i + 1}", expanded=(i == 0)):
        if estrutura_atual == "POR_COLUNAS":
            col_a, col_b, col_nome = st.columns(3)
            coluna_a = col_a.selectbox(
                f"Coluna da Referência A (campo {i+1})",
                numericas,
                key=f"cfg_col_a_{i}",
            )
            demais_b = [c for c in numericas if c != coluna_a] or numericas
            coluna_b = col_b.selectbox(
                f"Coluna da Referência B (campo {i+1})",
                demais_b,
                key=f"cfg_col_b_{i}",
            )
            nome_default = re.sub(r"_?(orcad[oa]|realizad[oa]|anterior|atual|a|b)$",
                                  "", coluna_a, flags=re.IGNORECASE) or coluna_a
            nome_analitico = col_nome.text_input(
                f"Nome analítico (campo {i+1})",
                value=nome_default,
                key=f"cfg_nome_{i}",
            )
            col_tipo, col_sem = st.columns(2)
            tipo_sugerido = _sugerir_tipo(nome_analitico)
            tipo_campo = col_tipo.selectbox(
                f"Tipo do campo (campo {i+1})",
                TIPO_CAMPO_OPTIONS,
                index=TIPO_CAMPO_OPTIONS.index(tipo_sugerido),
                key=f"cfg_tipo_{i}",
            )
            sem_sugerida = _sugerir_semantica(nome_analitico)
            semantica = col_sem.selectbox(
                f"Semântica (campo {i+1})",
                SEMANTICA_OPTIONS,
                index=SEMANTICA_OPTIONS.index(sem_sugerida),
                key=f"cfg_sem_{i}",
            )
            campos_cfg.append({
                "coluna_a": coluna_a,
                "coluna_b": coluna_b,
                "nome_analitico": nome_analitico or f"Campo_{i+1}",
                "tipo_campo": tipo_campo,
                "semantica": semantica,
            })
        else:  # POR_LINHAS
            col_v, col_nome = st.columns(2)
            coluna_valor = col_v.selectbox(
                f"Coluna de valor (campo {i+1})",
                numericas,
                key=f"cfg_col_v_{i}",
            )
            nome_analitico = col_nome.text_input(
                f"Nome analítico (campo {i+1})",
                value=coluna_valor,
                key=f"cfg_nome_pl_{i}",
            )
            col_tipo, col_sem = st.columns(2)
            tipo_sugerido = _sugerir_tipo(nome_analitico)
            tipo_campo = col_tipo.selectbox(
                f"Tipo do campo (campo {i+1})",
                TIPO_CAMPO_OPTIONS,
                index=TIPO_CAMPO_OPTIONS.index(tipo_sugerido),
                key=f"cfg_tipo_pl_{i}",
            )
            sem_sugerida = _sugerir_semantica(nome_analitico)
            semantica = col_sem.selectbox(
                f"Semântica (campo {i+1})",
                SEMANTICA_OPTIONS,
                index=SEMANTICA_OPTIONS.index(sem_sugerida),
                key=f"cfg_sem_pl_{i}",
            )
            campos_cfg.append({
                "coluna_valor": coluna_valor,
                "nome_analitico": nome_analitico or f"Campo_{i+1}",
                "tipo_campo": tipo_campo,
                "semantica": semantica,
            })

st.session_state.campos_cfg = campos_cfg

# --- 2.3 Agrupadores -------------------------------------------------------
st.subheader("2.3 — Agrupadores da análise")

colunas_ag_disponiveis = [c for c in categoricas]  # categóricas apenas
# Em POR_LINHAS, o discriminador e as colunas de valor não são agrupadores úteis
if estrutura_atual == "POR_LINHAS":
    disc = st.session_state.campo_discriminador
    cols_valor = {c.get("coluna_valor") for c in campos_cfg}
    colunas_ag_disponiveis = [
        c for c in colunas_ag_disponiveis if c != disc and c not in cols_valor
    ]

agrupadores_sel = st.multiselect(
    "Colunas categóricas que segmentam a análise (0 a 5)",
    colunas_ag_disponiveis,
    default=[
        c for c in st.session_state.agrupadores_sel
        if c in colunas_ag_disponiveis
    ],
    max_selections=MAX_AGRUPADORES,
    key="ms_agrupadores",
)
if agrupadores_sel != st.session_state.agrupadores_sel:
    st.session_state.agrupadores_sel = agrupadores_sel
    _reset_downstream_from_config()


# ---------------------------------------------------------------------------
# ETAPA 3 — Microanálise Prévia
# ---------------------------------------------------------------------------

st.header("Etapa 3 — Microanálise Prévia")

if st.button("Processar análise", type="primary", key="btn_processar"):
    try:
        kwargs: dict[str, Any] = dict(
            motor_result=motor_result,
            estrutura_entrada=st.session_state.estrutura_entrada,
            nome_referencia_a=st.session_state.nome_ref_a,
            nome_referencia_b=st.session_state.nome_ref_b,
            campos_comparados=campos_cfg,
            agrupadores=list(agrupadores_sel),
        )
        if st.session_state.estrutura_entrada == "POR_LINHAS":
            kwargs.update(
                campo_discriminador=st.session_state.campo_discriminador,
                valor_referencia_a=str(st.session_state.valor_ref_a),
                valor_referencia_b=str(st.session_state.valor_ref_b),
            )
        st.session_state.v2_result = executar_v2(**kwargs)
    except Exception as exc:
        st.error(f"Erro durante a análise: {exc}")
        st.session_state.v2_result = None

v2: Optional[V2Result] = st.session_state.v2_result

if v2 is None:
    st.info("Configure os parâmetros acima e clique em Processar análise.")
    st.stop()

# Warnings / Errors
for e in v2.errors:
    st.error(e)
for w in v2.warnings:
    st.warning(w)

if not v2.success:
    st.stop()

# Totalizadores
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Registros", v2.total_registros)
m2.metric("Melhoras", v2.total_melhoras)
m3.metric("Pioras", v2.total_pioras)
m4.metric("Sem variação", v2.total_sem_variacao)
m5.metric("Surgimentos", v2.total_surgimentos)
m6.metric("Desaparecimentos", v2.total_desaparecimentos)

# Tabela principal
st.subheader("Registros")
df_registros = _registros_para_df(v2)

if df_registros.empty:
    st.info("Nenhum registro gerado.")
else:
    # Filtros dinâmicos
    col_f1, col_f2, col_f3 = st.columns(3)
    classifs = sorted(df_registros["classificacao"].unique().tolist())
    filtro_classif = col_f1.multiselect(
        "Filtrar por classificação", classifs, default=classifs, key="f_classif"
    )
    campos_disp = sorted(df_registros["campo"].unique().tolist())
    filtro_campo = col_f2.multiselect(
        "Filtrar por campo", campos_disp, default=campos_disp, key="f_campo"
    )
    filtro_agrup_ativo = None
    if v2.agrupadores:
        ag_esc = col_f3.selectbox(
            "Filtrar por agrupador (coluna)",
            ["(nenhum)"] + list(v2.agrupadores),
            key="f_agrup_col",
        )
        if ag_esc != "(nenhum)":
            valores_ag = sorted(df_registros[ag_esc].dropna().astype(str).unique().tolist())
            filtro_agrup_ativo = (ag_esc, col_f3.multiselect(
                f"Valores de {ag_esc}",
                valores_ag,
                default=valores_ag,
                key=f"f_agrup_val_{ag_esc}",
            ))

    df_view = df_registros[
        df_registros["classificacao"].isin(filtro_classif)
        & df_registros["campo"].isin(filtro_campo)
    ].copy()
    if filtro_agrup_ativo is not None:
        col_ag, vals_ag = filtro_agrup_ativo
        df_view = df_view[df_view[col_ag].astype(str).isin(vals_ag)]

    # Indicador legendado D-001 (destaque visual SURGIMENTO/DESAPARECIMENTO)
    if v2.total_surgimentos or v2.total_desaparecimentos:
        st.caption(
            f"{ICONES_FLAG['SURGIMENTO']} Surgimentos · "
            f"{ICONES_FLAG['DESAPARECIMENTO']} Desaparecimentos · "
            "linhas destacadas em amarelo/laranja."
        )

    st.dataframe(_estilizar_registros(df_view), use_container_width=True)

# Resumo por agrupador
if v2.resumo_por_agrupador:
    st.subheader("Resumo por agrupador")
    # Banner W07 com destaque (D-002)
    tipos_sensiveis = {
        c["tipo_campo"] for c in campos_cfg if c["tipo_campo"] in ("PERCENTUAL", "INDICE")
    }
    if tipos_sensiveis and v2.agrupadores:
        tem_w07 = any(w.startswith("W07") for w in v2.warnings)
        if tem_w07:
            st.warning(
                "⚠️ W07 — Campos do tipo PERCENTUAL/INDICE usam média simples no "
                "resumo por agrupador (D-002). Para análise rigorosa, considere "
                "ponderação manual."
            )
        else:
            st.info(
                "ℹ️ D-002 exige aviso W07 para campos PERCENTUAL/INDICE com "
                "agrupadores — não foi emitido pela visão nesta execução."
            )

    df_resumo = _resumo_para_df(v2)
    st.dataframe(
        df_resumo.style.format({
            "total_a": _fmt_num,
            "total_b": _fmt_num,
            "variacao_absoluta": _fmt_num,
            "variacao_percentual": _fmt_pct,
        }),
        use_container_width=True,
    )


# ---------------------------------------------------------------------------
# ETAPA 4 — Exportação Excel
# ---------------------------------------------------------------------------

st.header("Etapa 4 — Exportação Excel")

col_t, col_nv = st.columns([1, 2])
tema = col_t.radio(
    "Tema visual",
    ["Claro", "Escuro"],
    horizontal=True,
    index=0 if st.session_state.tema_excel == "Claro" else 1,
    key="radio_tema",
)
st.session_state.tema_excel = tema

nome_visao_default = st.session_state.nome_visao or "analise_v2"
nome_visao = col_nv.text_input(
    "Nome da visão (entra no nome do arquivo)",
    value=nome_visao_default,
    key="in_nome_visao",
)
st.session_state.nome_visao = nome_visao

data_str = datetime.now().strftime("%Y%m%d")
nome_arquivo = f"V2_{_slug(nome_visao)}_{data_str}.xlsx"

cfg_parametros = {
    "nome_visao": nome_visao,
    "campos_cfg": campos_cfg,
    "campo_discriminador": st.session_state.campo_discriminador,
    "valor_ref_a": st.session_state.valor_ref_a,
    "valor_ref_b": st.session_state.valor_ref_b,
}

try:
    xlsx_bytes = _build_excel(v2, cfg_parametros, tema)
    st.download_button(
        label="Baixar Excel",
        data=xlsx_bytes,
        file_name=nome_arquivo,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="btn_download_v2",
    )
    st.caption(f"Arquivo: `{nome_arquivo}` · tema: {tema}")
except Exception as exc:
    st.error(f"Erro ao gerar Excel: {exc}")
