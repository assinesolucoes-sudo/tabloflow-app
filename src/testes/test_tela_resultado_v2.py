"""
test_tela_resultado_v2.py — Sessão 4-ter · D-177 · tela 'Resultado da análise'.

5 invariantes da superfície cliente quando a tela Resultado é renderizada:
  - NÃO exibe st.json (formato técnico)
  - NÃO exibe códigos VVC (V2-A01 · W-V2-*)
  - Exibe 4 st.metric (números-âncora)
  - Expander 'Configurações avançadas' no topo (não na sidebar)
  - Rodapé tem paleta dropdown + botão de download
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest

_SRC = Path(__file__).parent.parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from streamlit.testing.v1 import AppTest  # noqa: E402

from motor_base import processar_base  # noqa: E402
from motor_upload import ArquivoEntrada, processar_upload  # noqa: E402

APP_PATH = str(_SRC / "app_v2.py")
BASE_V2_PATH = Path(__file__).parent.parent.parent / "bases" / "base_v2_cliente.xlsx"


@pytest.fixture(scope="module")
def motor_result_padrao():
    entrada = ArquivoEntrada(
        caminho_fisico=str(BASE_V2_PATH),
        caminho_logico="unico",
        aba_solicitada="vendas_padrao",
    )
    ur = processar_upload([entrada], modo="SIMPLES")
    mr = processar_base(ur)
    return ur, mr


def _executar_ate_resultado(motor_result_padrao):
    ur, mr = motor_result_padrao
    at = AppTest.from_file(APP_PATH, default_timeout=60)
    at.session_state["etapa"] = "E3"
    at.session_state["upload_result"] = ur
    at.session_state["motor_result"] = mr
    at.session_state["nome_arquivo"] = "base_v2_cliente.xlsx"
    at.session_state["aba_selecionada"] = "vendas_padrao"
    at.session_state["abas_disponiveis"] = ["vendas_padrao", "vendas_por_colunas"]
    at.session_state["estrutura_entrada"] = "POR_LINHAS"
    at.session_state["coluna_discriminadora"] = "Mes"
    at.session_state["origem_rotulo_tecnico"] = "2025-01"
    at.session_state["comparado_rotulo_tecnico"] = "2025-02"
    at.session_state["origem_rotulo_ux"] = "Janeiro"
    at.session_state["comparado_rotulo_ux"] = "Fevereiro"
    at.run()
    at.selectbox(key="sel_campo").set_value("Vendas").run()
    at.radio(key="rad_tipo").set_value("NUMERICO_ADITIVO").run()
    at.radio(key="rad_sem").set_value("MAIOR_MELHOR").run()
    at.button(key="btn_avancar_e4").click().run()
    at.multiselect(key="ms_agrup").set_value(["Produto"]).run()
    at.button(key="btn_avancar_e5").click().run()
    at.button(key="btn_processar").click().run()
    assert at.session_state["etapa"] == "RESULTADO"
    return at


def test_tela_resultado_nao_exibe_st_json(motor_result_padrao):
    """D-177 · tela não exibe nenhum st.json (superfície executiva)."""
    at = _executar_ate_resultado(motor_result_padrao)
    # AppTest expõe .json para elementos st.json
    jsons = getattr(at, "json", None)
    # Se a propriedade existir, deve vir vazia
    if jsons is not None:
        assert len(list(jsons)) == 0, \
            f"Tela Resultado contém {len(list(jsons))} st.json · deve ser 0 (D-177)"


def test_tela_resultado_nao_exibe_codigos_tecnicos(motor_result_padrao):
    """D-177 · nenhum código VVC (V2-A01, W-V2-*, B-V2-*) visível na superfície."""
    at = _executar_ate_resultado(motor_result_padrao)
    # Colecta todo texto visível
    textos = []
    for md in at.markdown:
        textos.append(str(md.value))
    for t in at.title:
        textos.append(str(t.value))
    for h in at.header:
        textos.append(str(h.value))
    for sh in at.subheader:
        textos.append(str(sh.value))
    for c in at.caption:
        textos.append(str(c.value))
    texto_total = " ".join(textos)
    proibidos_codigos = [
        "V2-A01", "V2-A02", "V2-A03", "V2-A04",
        "W-V2-", "B-V2-",
    ]
    violacoes = [p for p in proibidos_codigos if p in texto_total]
    assert not violacoes, f"Códigos técnicos visíveis: {violacoes}"


def test_tela_resultado_exibe_quatro_metrics(motor_result_padrao):
    """§5.1 · 4 st.metric (Total origem · Total comparado · Diferença · Variação %)."""
    at = _executar_ate_resultado(motor_result_padrao)
    metrics = list(at.metric)
    assert len(metrics) >= 4, f"Esperados 4 metrics · encontrados {len(metrics)}"


def test_expander_ted_no_topo_nao_na_sidebar(motor_result_padrao):
    """D-178 · expander 'Configurações avançadas' no topo · sidebar vazia de TED."""
    at = _executar_ate_resultado(motor_result_padrao)
    # Widgets TED acessíveis fora da sidebar (via global scope)
    keys_globais = [ni.key for ni in at.number_input]
    assert "ted_estab" in keys_globais, "ted_estab não encontrado no escopo global"
    # Sidebar não deve conter ted_*
    sb_keys = [ni.key for ni in at.sidebar.number_input]
    assert "ted_estab" not in sb_keys, "TED ainda está na sidebar (D-178 viola)"


def test_tela_resultado_tem_paleta_dropdown_e_download(motor_result_padrao):
    """§5.3 · rodapé com selectbox de paleta + botão download."""
    at = _executar_ate_resultado(motor_result_padrao)
    selectbox_keys = [sb.key for sb in at.selectbox]
    assert "paleta_selecionada" in selectbox_keys, \
        "Selectbox 'paleta_selecionada' não encontrado na tela Resultado"
    # Botão download (AppTest expõe via at.get("download_button")) · existe >=1
    download_elements = list(at.get("download_button")) if hasattr(at, "get") else []
    assert len(download_elements) >= 1, \
        f"Nenhum botão de download encontrado · {len(download_elements)} elementos"
    # Labels possíveis do download
    labels = [getattr(d, "label", "") for d in download_elements]
    assert any("Baixar" in (l or "") for l in labels), \
        f"Nenhum botão com label 'Baixar' · labels={labels}"


def test_tela_resultado_header_em_portugues_user_facing(motor_result_padrao):
    """D-177 · header user-facing 'Resultado da análise' (não 'Validação Visual')."""
    at = _executar_ate_resultado(motor_result_padrao)
    textos = [str(h.value) for h in at.header]
    textos += [str(sh.value) for sh in at.subheader]
    assert any("Resultado da análise" in t for t in textos), \
        f"Header 'Resultado da análise' não encontrado · textos={textos[:5]}"
    # Não pode ter "Validação Visual" como header
    assert not any("Validação Visual" == t.strip() for t in textos), \
        "Header 'Validação Visual' encontrado · deveria ter sido removido (D-177)"


def test_app_rotular_agrupador_ui_traduz_centro_custo():
    """C-5 · helper de tradução converte Centro_Custo → Centro de Custo na superfície."""
    from app_v2 import _rotular_agrupador_ui
    # Caso canônico identificado na camada 2 (Sessão 4-ter-bis)
    assert _rotular_agrupador_ui("Centro_Custo") == "Centro de Custo"
    assert _rotular_agrupador_ui("centro_custo") == "Centro de Custo"
    assert _rotular_agrupador_ui("Mes") == "Mês"
    # Casos genéricos · underscore → espaço + capitalize
    assert _rotular_agrupador_ui("linha_produto") == "Linha produto"
    assert _rotular_agrupador_ui("Produto") == "Produto"
    # Sem underscore · sem transformação forte
    assert _rotular_agrupador_ui("Loja") == "Loja"
