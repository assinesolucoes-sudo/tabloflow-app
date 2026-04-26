"""
test_app_v2.py — Suite A-V2 · app_v2.py Streamlit (gate B.4 · checklist · exportação)

Estratégia: streamlit.testing.v1.AppTest (stdlib oficial Streamlit · testa widgets ·
estados · transições de forma determinística).

Como o AppTest não suporta simulação direta de st.file_uploader, os testes que
exercitam o fluxo pós-upload injetam motor_result e upload_result diretamente em
st.session_state e iniciam o app em etapa `E2` ou `E3`.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict

import pandas as pd
import pytest

_SRC = Path(__file__).parent.parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from streamlit.testing.v1 import AppTest  # noqa: E402

from motor_base import processar_base  # noqa: E402
from motor_upload import ArquivoEntrada, processar_upload  # noqa: E402

APP_PATH = str(_SRC / "app_v2.py")
BASE_V2_PATH = Path(__file__).parent.parent.parent / "bases" / "base_v2_cliente.xlsx"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _motor_result_para_aba(aba: str):
    entrada = ArquivoEntrada(
        caminho_fisico=str(BASE_V2_PATH),
        caminho_logico="unico",
        aba_solicitada=aba,
    )
    ur = processar_upload([entrada], modo="SIMPLES")
    mr = processar_base(ur)
    return ur, mr


@pytest.fixture(scope="module")
def motor_result_padrao():
    return _motor_result_para_aba("vendas_padrao")


@pytest.fixture(scope="module")
def motor_result_por_colunas():
    return _motor_result_para_aba("vendas_por_colunas")


def _injetar_estado_e2(at: AppTest, ur, mr, aba: str) -> None:
    at.session_state["etapa"] = "E2"
    at.session_state["upload_result"] = ur
    at.session_state["motor_result"] = mr
    at.session_state["nome_arquivo"] = "base_v2_cliente.xlsx"
    at.session_state["aba_selecionada"] = aba
    at.session_state["abas_disponiveis"] = ["vendas_padrao", "vendas_por_colunas"]


def _injetar_estado_e3(at: AppTest, ur, mr, aba: str, **e2_cfg: Any) -> None:
    _injetar_estado_e2(at, ur, mr, aba)
    at.session_state["etapa"] = "E3"
    for k, v in e2_cfg.items():
        at.session_state[k] = v


# ---------------------------------------------------------------------------
# 1 · Import e startup
# ---------------------------------------------------------------------------


def test_app_startup_sem_excecao():
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()
    assert not at.exception, f"Exceção no startup: {at.exception}"
    assert at.session_state["etapa"] == "vazio"
    assert any("V2" in t.value for t in at.title)


# ---------------------------------------------------------------------------
# 2 · Fluxo feliz POR_LINHAS (aba vendas_padrao)
# ---------------------------------------------------------------------------


def test_fluxo_feliz_por_linhas_vendas_padrao(motor_result_padrao):
    ur, mr = motor_result_padrao
    at = AppTest.from_file(APP_PATH, default_timeout=60)
    _injetar_estado_e3(
        at, ur, mr, "vendas_padrao",
        estrutura_entrada="POR_LINHAS",
        coluna_discriminadora="Mes",
        origem_rotulo_tecnico="2025-01",
        comparado_rotulo_tecnico="2025-02",
        origem_rotulo_ux="Janeiro 2025",
        comparado_rotulo_ux="Fevereiro 2025",
    )
    at.run()
    assert not at.exception

    # E3 · campo + tipo + semantica
    at.selectbox(key="sel_campo").set_value("Vendas").run()
    at.radio(key="rad_tipo").set_value("NUMERICO_ADITIVO").run()
    at.radio(key="rad_sem").set_value("MAIOR_MELHOR").run()
    at.button(key="btn_avancar_e4").click().run()
    assert at.session_state["etapa"] == "E4"

    # E4 · agrupadores
    at.multiselect(key="ms_agrup").set_value(["Produto"]).run()
    at.radio(key="rad_regra").set_value("SOMA").run()
    at.button(key="btn_avancar_e5").click().run()
    assert at.session_state["etapa"] == "E5"

    # E5 · processar
    at.button(key="btn_processar").click().run()
    assert at.session_state["etapa"] == "RESULTADO"

    v2 = at.session_state["v2_result"]
    assert v2 is not None
    assert v2.numeros_ancora.total_origem is not None
    assert v2.numeros_ancora.total_comparado is not None
    assert len(v2.bloqueios_disparados) == 0
    # V2-A01 · AUSENTE_ORIGEM + AUSENTE_COMPARADO entre 2 e 4
    dist = v2.distribuicao_classificacoes_estruturais
    ausentes = dist.get("AUSENTE_ORIGEM", 0) + dist.get("AUSENTE_COMPARADO", 0)
    assert 2 <= ausentes <= 4, f"V2-A01 violado · ausentes={ausentes}"


# ---------------------------------------------------------------------------
# 3 · Fluxo feliz POR_COLUNAS (aba vendas_por_colunas)
# ---------------------------------------------------------------------------


def test_fluxo_feliz_por_colunas_vendas_por_colunas(motor_result_por_colunas):
    ur, mr = motor_result_por_colunas
    at = AppTest.from_file(APP_PATH, default_timeout=60)
    _injetar_estado_e3(
        at, ur, mr, "vendas_por_colunas",
        estrutura_entrada="POR_COLUNAS",
        origem_rotulo_tecnico="jan/2025",
        comparado_rotulo_tecnico="fev/2025",
        origem_rotulo_ux="Janeiro",
        comparado_rotulo_ux="Fevereiro",
    )
    at.run()
    assert not at.exception

    at.text_input(key="txt_campo_concept").set_value("Receita").run()
    at.radio(key="rad_tipo").set_value("NUMERICO_ADITIVO").run()
    at.radio(key="rad_sem").set_value("MAIOR_MELHOR").run()
    at.button(key="btn_avancar_e4").click().run()
    assert at.session_state["etapa"] == "E4"

    # E1 (Sessão 8) · workaround para bug conhecido do streamlit.testing v1:
    # widgets de E3 (chk_preagr · sel_unidade) vazam para a árvore de E4
    # quando estrutura_entrada=POR_COLUNAS · setar explicitamente as keys
    # antes do próximo run evita o KeyError em get_widget_states.
    at.session_state["chk_preagr"] = False
    at.session_state["sel_unidade"] = "MONETARIO_BRL"

    at.multiselect(key="ms_agrup").set_value(["Produto"]).run()
    at.radio(key="rad_regra").set_value("SOMA").run()
    at.button(key="btn_avancar_e5").click().run()
    at.button(key="btn_processar").click().run()
    assert at.session_state["etapa"] == "RESULTADO"

    v2 = at.session_state["v2_result"]
    assert v2 is not None
    assert len(v2.bloqueios_disparados) == 0
    assert v2.comparacao_realizada.estrutura_entrada == "POR_COLUNAS"
    # E1 · default declarado para NUMERICO_ADITIVO é MONETARIO_BRL
    assert v2.comparacao_realizada.unidade == "MONETARIO_BRL"


# ---------------------------------------------------------------------------
# 4 · P4 · excesso de agrupadores bloqueia (B-V2-AGRUP-EXCESSO)
# ---------------------------------------------------------------------------


def test_p4_agrupadores_bloqueia(motor_result_padrao):
    """>= 9 agrupadores · V2 deve bloquear com B-V2-AGRUP-EXCESSO.

    A UI não deixa clicar em E4 com 9+ agrupadores, então o disparo é testado
    passando a config direto para executar_v2 via session_state e acionando
    E5 → Processar.
    """
    ur, mr = motor_result_padrao
    at = AppTest.from_file(APP_PATH, default_timeout=60)
    # 10 agrupadores fictícios (a base só tem 6 candidatos · repetimos via session)
    agrupadores_fake = [f"Col_{i}" for i in range(10)]
    at.session_state["etapa"] = "E5"
    at.session_state["upload_result"] = ur
    at.session_state["motor_result"] = mr
    at.session_state["nome_arquivo"] = "base_v2_cliente.xlsx"
    at.session_state["aba_selecionada"] = "vendas_padrao"
    at.session_state["estrutura_entrada"] = "POR_LINHAS"
    at.session_state["coluna_discriminadora"] = "Mes"
    at.session_state["origem_rotulo_tecnico"] = "2025-01"
    at.session_state["comparado_rotulo_tecnico"] = "2025-02"
    at.session_state["origem_rotulo_ux"] = "Jan"
    at.session_state["comparado_rotulo_ux"] = "Fev"
    at.session_state["campo_analisado"] = "Vendas"
    at.session_state["tipo_campo"] = "NUMERICO_ADITIVO"
    at.session_state["semantica_campo"] = "MAIOR_MELHOR"
    at.session_state["agrupadores"] = agrupadores_fake
    at.session_state["regra_agregacao"] = "SOMA"
    at.run()
    at.button(key="btn_processar").click().run()
    assert at.session_state["etapa"] == "ERRO"
    v2 = at.session_state["v2_result"]
    assert v2 is not None
    codigos = [b.codigo for b in v2.bloqueios_disparados]
    assert "B-V2-AGRUP-EXCESSO" in codigos


# ---------------------------------------------------------------------------
# 5 · Checklist gate B.4 · download travado até 4/4 ✅
# ---------------------------------------------------------------------------


def test_download_livre_sem_checklist_d177(motor_result_padrao):
    """
    D-177 · tela 'Resultado da análise' com download livre · sem checklist VVC.

    Supersede D-162: o download é livre e não há gate; a tela de
    'Validação Visual' foi absorvida e suas checkboxes não existem mais
    na superfície cliente.
    """
    ur, mr = motor_result_padrao
    at = AppTest.from_file(APP_PATH, default_timeout=60)
    _injetar_estado_e3(
        at, ur, mr, "vendas_padrao",
        estrutura_entrada="POR_LINHAS",
        coluna_discriminadora="Mes",
        origem_rotulo_tecnico="2025-01",
        comparado_rotulo_tecnico="2025-02",
        origem_rotulo_ux="Jan",
        comparado_rotulo_ux="Fev",
    )
    at.run()
    at.selectbox(key="sel_campo").set_value("Vendas").run()
    at.radio(key="rad_tipo").set_value("NUMERICO_ADITIVO").run()
    at.radio(key="rad_sem").set_value("MAIOR_MELHOR").run()
    at.button(key="btn_avancar_e4").click().run()
    at.multiselect(key="ms_agrup").set_value(["Produto"]).run()
    at.button(key="btn_avancar_e5").click().run()
    at.button(key="btn_processar").click().run()
    assert at.session_state["etapa"] == "RESULTADO"

    # Download já disponível · caminho materializado na primeira render
    assert at.session_state["caminho_excel_exportado"] is not None, \
        "Download do Excel deve estar disponível imediato na tela Resultado (D-177)"
    assert Path(at.session_state["caminho_excel_exportado"]).exists()

    # D-177 · botões/elementos removidos não existem
    button_keys = [b.key for b in at.button]
    assert "btn_ir_checklist" not in button_keys, \
        "Botão 'Ir para Validação Visual' removido (D-177)"
    assert "btn_aprovar" not in button_keys, \
        "Botão 'Aprovar visão' removido (D-177)"

    # Checkboxes do checklist VVC não existem mais
    chk_keys = [c.key for c in at.checkbox]
    for i in range(1, 5):
        assert f"chk_item_{i}" not in chk_keys, \
            f"Checkbox 'chk_item_{i}' do VVC removido (D-177)"


def test_paleta_trocavel_apos_execucao(motor_result_padrao):
    """
    D-175 · §5.4 · P-3 · paleta pode ser trocada na tela Resultado após a
    execução · o download gera Excel com a paleta corrente (não congelada).
    """
    ur, mr = motor_result_padrao
    at = AppTest.from_file(APP_PATH, default_timeout=60)
    _injetar_estado_e3(
        at, ur, mr, "vendas_padrao",
        estrutura_entrada="POR_LINHAS",
        coluna_discriminadora="Mes",
        origem_rotulo_tecnico="2025-01",
        comparado_rotulo_tecnico="2025-02",
        origem_rotulo_ux="Jan",
        comparado_rotulo_ux="Fev",
    )
    at.run()
    at.selectbox(key="sel_campo").set_value("Vendas").run()
    at.radio(key="rad_tipo").set_value("NUMERICO_ADITIVO").run()
    at.radio(key="rad_sem").set_value("MAIOR_MELHOR").run()
    at.button(key="btn_avancar_e4").click().run()
    at.multiselect(key="ms_agrup").set_value(["Produto"]).run()
    at.button(key="btn_avancar_e5").click().run()
    at.button(key="btn_processar").click().run()
    assert at.session_state["etapa"] == "RESULTADO"

    caminho_inicial = (at.session_state["caminho_excel_exportado"] if "caminho_excel_exportado" in at.session_state else None)
    assert caminho_inicial is not None

    # Troca paleta na tela Resultado
    at.selectbox(key="paleta_selecionada").set_value("Verde").run()

    # Session state reflete a troca · novo caminho de cache (chave por paleta)
    assert at.session_state["paleta_selecionada"] == "Verde"
    # Ao rerenderizar, o download foi regenerado com nova paleta (cache por paleta)
    caminho_apos_troca = (at.session_state["caminho_excel_exportado"] if "caminho_excel_exportado" in at.session_state else None)
    assert caminho_apos_troca is not None
    # Verifica que o novo arquivo foi criado (pode ou não ser o mesmo path
    # dependendo de caching · mas existe)
    assert Path(caminho_apos_troca).exists()


# ---------------------------------------------------------------------------
# 6 · Invalidação cascata · editar E2 zera E3-E5
# ---------------------------------------------------------------------------


def test_invalidacao_cascata_editar_e2_zera_e3_em_diante(motor_result_padrao):
    ur, mr = motor_result_padrao
    at = AppTest.from_file(APP_PATH, default_timeout=60)
    # Preencher E1-E4 todo
    at.session_state["etapa"] = "E4"
    at.session_state["upload_result"] = ur
    at.session_state["motor_result"] = mr
    at.session_state["nome_arquivo"] = "base_v2_cliente.xlsx"
    at.session_state["aba_selecionada"] = "vendas_padrao"
    at.session_state["estrutura_entrada"] = "POR_LINHAS"
    at.session_state["coluna_discriminadora"] = "Mes"
    at.session_state["origem_rotulo_tecnico"] = "2025-01"
    at.session_state["comparado_rotulo_tecnico"] = "2025-02"
    at.session_state["origem_rotulo_ux"] = "Jan"
    at.session_state["comparado_rotulo_ux"] = "Fev"
    at.session_state["campo_analisado"] = "Vendas"
    at.session_state["tipo_campo"] = "NUMERICO_ADITIVO"
    at.session_state["semantica_campo"] = "MAIOR_MELHOR"
    at.session_state["agrupadores"] = ["Produto"]
    at.session_state["regra_agregacao"] = "SOMA"
    at.run()

    # Voltar a E3 e depois a E2 e alterar estrutura
    at.button(key="btn_voltar_e4").click().run()
    assert at.session_state["etapa"] == "E3"
    at.button(key="btn_voltar_e3").click().run()
    assert at.session_state["etapa"] == "E2"

    # Alterar estrutura · deve zerar a partir de E3 (cascata §3.10)
    at.radio(key="rad_estrutura").set_value("POR_COLUNAS").run()
    # campo_analisado deve ter voltado ao default vazio (E3 zerada)
    assert at.session_state["campo_analisado"] == ""
    # agrupadores zerados (E4)
    assert at.session_state["agrupadores"] == []


# ---------------------------------------------------------------------------
# 6.1 · D-186 · Gate de stale · mudança em campo crítico após execução
# ---------------------------------------------------------------------------


def test_d186_resultado_stale_quando_semantica_muda_apos_execucao(motor_result_padrao):
    """
    D-186 (Sessão 5) · ao trocar semantica_campo (ou outro campo crítico)
    DEPOIS de executar a análise, a tela RESULTADO deve sinalizar o resultado
    como stale (st.warning) e oferecer botão de re-execução.

    Reprodução do empírico relatado: rodar com MENOR_MELHOR · trocar para
    MAIOR_MELHOR direto via session_state · re-renderizar tela RESULTADO.
    """
    ur, mr = motor_result_padrao
    at = AppTest.from_file(APP_PATH, default_timeout=60)
    _injetar_estado_e3(
        at, ur, mr, "vendas_padrao",
        estrutura_entrada="POR_LINHAS",
        coluna_discriminadora="Mes",
        origem_rotulo_tecnico="2025-01",
        comparado_rotulo_tecnico="2025-02",
        origem_rotulo_ux="Jan",
        comparado_rotulo_ux="Fev",
    )
    at.run()
    at.selectbox(key="sel_campo").set_value("Vendas").run()
    at.radio(key="rad_tipo").set_value("NUMERICO_ADITIVO").run()
    at.radio(key="rad_sem").set_value("MENOR_MELHOR").run()
    at.button(key="btn_avancar_e4").click().run()
    at.multiselect(key="ms_agrup").set_value(["Produto"]).run()
    at.button(key="btn_avancar_e5").click().run()
    at.button(key="btn_processar").click().run()
    assert at.session_state["etapa"] == "RESULTADO"
    hash_pos_exec = at.session_state["_hash_config_executada"]
    assert hash_pos_exec is not None, "Hash da config executada deveria estar populado"

    # Sem mudança · não deve haver warning de stale
    button_keys_antes = [b.key for b in at.button]
    assert "btn_reexecutar_stale" not in button_keys_antes, \
        "Sem mudança · botão de re-execução não deve aparecer"

    # Troca semantica_campo direto no session_state (simula edição de E3 sem
    # clicar em executar) e força re-render da tela RESULTADO.
    at.session_state["semantica_campo"] = "MAIOR_MELHOR"
    at.run()

    # Aviso de stale presente
    warnings_renderizados = [w.value for w in at.warning]
    assert any("alterada após a última execução" in str(w) for w in warnings_renderizados), (
        f"Esperava st.warning de stale · warnings encontrados: {warnings_renderizados}"
    )
    # Botão de re-execução visível
    button_keys_depois = [b.key for b in at.button]
    assert "btn_reexecutar_stale" in button_keys_depois, \
        "Botão 'Executar análise com a configuração atual' deveria aparecer"


def test_d186_reexecucao_atualiza_resultado_para_config_corrente(motor_result_padrao):
    """
    D-186 · clicar em 'Executar análise com a configuração atual' deve
    re-rodar o motor com a config corrente e limpar o estado stale.
    """
    ur, mr = motor_result_padrao
    at = AppTest.from_file(APP_PATH, default_timeout=60)
    _injetar_estado_e3(
        at, ur, mr, "vendas_padrao",
        estrutura_entrada="POR_LINHAS",
        coluna_discriminadora="Mes",
        origem_rotulo_tecnico="2025-01",
        comparado_rotulo_tecnico="2025-02",
        origem_rotulo_ux="Jan",
        comparado_rotulo_ux="Fev",
    )
    at.run()
    at.selectbox(key="sel_campo").set_value("Vendas").run()
    at.radio(key="rad_tipo").set_value("NUMERICO_ADITIVO").run()
    at.radio(key="rad_sem").set_value("MENOR_MELHOR").run()
    at.button(key="btn_avancar_e4").click().run()
    at.multiselect(key="ms_agrup").set_value(["Produto"]).run()
    at.button(key="btn_avancar_e5").click().run()
    at.button(key="btn_processar").click().run()
    hash_inicial = at.session_state["_hash_config_executada"]

    at.session_state["semantica_campo"] = "MAIOR_MELHOR"
    at.run()
    at.button(key="btn_reexecutar_stale").click().run()

    # Re-execução: nova hash refletindo MAIOR_MELHOR · estado RESULTADO mantido
    assert at.session_state["etapa"] == "RESULTADO"
    hash_pos_reexec = at.session_state["_hash_config_executada"]
    assert hash_pos_reexec is not None
    assert hash_pos_reexec != hash_inicial, "Hash deveria mudar após re-execução com config alterada"
    # Warning de stale dissipou
    button_keys = [b.key for b in at.button]
    assert "btn_reexecutar_stale" not in button_keys, \
        "Após re-execução · botão de stale não deve mais aparecer"


# ---------------------------------------------------------------------------
# 7 · TED editado é passado adiante ao executar_v2
# ---------------------------------------------------------------------------


def test_ted_editado_chega_em_v2_result(motor_result_padrao):
    ur, mr = motor_result_padrao
    at = AppTest.from_file(APP_PATH, default_timeout=60)
    _injetar_estado_e3(
        at, ur, mr, "vendas_padrao",
        estrutura_entrada="POR_LINHAS",
        coluna_discriminadora="Mes",
        origem_rotulo_tecnico="2025-01",
        comparado_rotulo_tecnico="2025-02",
        origem_rotulo_ux="Jan",
        comparado_rotulo_ux="Fev",
    )
    at.run()

    # Editar TED no expander "Configurações avançadas" (D-178 · sai da sidebar)
    at.number_input(key="ted_estab").set_value(0.05).run()

    at.selectbox(key="sel_campo").set_value("Vendas").run()
    at.radio(key="rad_tipo").set_value("NUMERICO_ADITIVO").run()
    at.radio(key="rad_sem").set_value("MAIOR_MELHOR").run()
    at.button(key="btn_avancar_e4").click().run()
    at.multiselect(key="ms_agrup").set_value(["Produto"]).run()
    at.button(key="btn_avancar_e5").click().run()
    at.button(key="btn_processar").click().run()

    v2 = at.session_state["v2_result"]
    assert v2 is not None
    assert v2.config_usada["thresholds"]["limiar_estabilidade_pct"] == 0.05


# ---------------------------------------------------------------------------
# 8 · V2-A04 · Mes discriminador · exatamente 2 estados
# ---------------------------------------------------------------------------


def test_v2a04_discriminador_mes_dois_estados(motor_result_padrao):
    ur, mr = motor_result_padrao
    df = mr.df
    assert df["Mes"].dropna().nunique() == 2
    estados = sorted(df["Mes"].dropna().unique().tolist())
    assert estados == ["2025-01", "2025-02"]


# ---------------------------------------------------------------------------
# 9 · Tela ERRO renderiza quando motor dispara bloqueio
# ---------------------------------------------------------------------------


def test_tela_erro_renderiza_bloqueio(motor_result_padrao):
    """Config com 10 agrupadores · B-V2-AGRUP-EXCESSO · Tela 10 renderiza."""
    ur, mr = motor_result_padrao
    at = AppTest.from_file(APP_PATH, default_timeout=60)
    at.session_state["etapa"] = "E5"
    at.session_state["upload_result"] = ur
    at.session_state["motor_result"] = mr
    at.session_state["nome_arquivo"] = "base_v2_cliente.xlsx"
    at.session_state["aba_selecionada"] = "vendas_padrao"
    at.session_state["estrutura_entrada"] = "POR_LINHAS"
    at.session_state["coluna_discriminadora"] = "Mes"
    at.session_state["origem_rotulo_tecnico"] = "2025-01"
    at.session_state["comparado_rotulo_tecnico"] = "2025-02"
    at.session_state["origem_rotulo_ux"] = "Jan"
    at.session_state["comparado_rotulo_ux"] = "Fev"
    at.session_state["campo_analisado"] = "Vendas"
    at.session_state["tipo_campo"] = "NUMERICO_ADITIVO"
    at.session_state["semantica_campo"] = "MAIOR_MELHOR"
    at.session_state["agrupadores"] = [f"X_{i}" for i in range(10)]
    at.session_state["regra_agregacao"] = "SOMA"
    at.run()
    at.button(key="btn_processar").click().run()
    assert at.session_state["etapa"] == "ERRO"
    # Mensagem user-facing (P-V2 §2.8) deve aparecer · código técnico NÃO deve
    # vazar para a superfície principal (vocabulário_bilingue v2 Bloco 7 · §8)
    textos_erro = " ".join(e.value for e in at.error)
    assert "máximo de 9" in textos_erro, \
        "Mensagem user-facing do bloqueio deve citar o limite de 9 agrupadores"
    # Garantir que o código técnico NÃO está no texto do erro principal
    assert "B-V2-AGRUP-EXCESSO" not in textos_erro, \
        "Código técnico B-V2-* proibido na superfície cliente principal (vocab v2 §8)"


# ---------------------------------------------------------------------------
# 10 · Modo 4 · default declarado são extremos (não testado via UI porque a base
# canônica só tem 2 valores em Mes · validamos o helper diretamente).
# ---------------------------------------------------------------------------


def test_ordenacao_inteligente_numerica_e_cronologica():
    """Helper _ordenar_inteligente usa numérico > cronológico > alfabético."""
    from app_v2 import _ordenar_inteligente

    # numérico
    assert _ordenar_inteligente([10, 2, 30]) == [2, 10, 30]
    # cronológico
    assert _ordenar_inteligente(["2025-02", "2025-01", "2025-03"]) == [
        "2025-01", "2025-02", "2025-03",
    ]
    # alfabético fallback
    assert _ordenar_inteligente(["banana", "maçã", "abacate"]) == [
        "abacate", "banana", "maçã",
    ]


# ---------------------------------------------------------------------------
# 11 · Paleta · default Azul · widget persiste no session_state (D-168)
# ---------------------------------------------------------------------------


def test_paleta_default_azul_e_ordem_widget():
    """P-V2 §1.1 · D-168 · paleta default universal Azul · ordem fixa."""
    from app_v2 import PALETAS_DISPONIVEIS, PALETA_DEFAULT

    assert PALETA_DEFAULT == "Azul"
    assert PALETAS_DISPONIVEIS == ["Azul", "Cinza", "Verde", "Vinho"]


def test_paleta_persiste_em_session_state():
    """Startup · paleta_selecionada inicializada em 'Azul' · widget na sidebar."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()
    assert at.session_state["paleta_selecionada"] == "Azul"


def test_paleta_aplicada_vai_para_config_usada(motor_result_padrao):
    """D-168 · escolha da paleta persiste em v2_result.config_usada após pipeline."""
    ur, mr = motor_result_padrao
    at = AppTest.from_file(APP_PATH, default_timeout=60)
    _injetar_estado_e3(
        at, ur, mr, "vendas_padrao",
        estrutura_entrada="POR_LINHAS",
        coluna_discriminadora="Mes",
        origem_rotulo_tecnico="2025-01",
        comparado_rotulo_tecnico="2025-02",
        origem_rotulo_ux="Jan",
        comparado_rotulo_ux="Fev",
    )
    at.session_state["paleta_selecionada"] = "Verde"
    at.run()
    at.selectbox(key="sel_campo").set_value("Vendas").run()
    at.radio(key="rad_tipo").set_value("NUMERICO_ADITIVO").run()
    at.radio(key="rad_sem").set_value("MAIOR_MELHOR").run()
    at.button(key="btn_avancar_e4").click().run()
    at.multiselect(key="ms_agrup").set_value(["Produto"]).run()
    at.button(key="btn_avancar_e5").click().run()
    at.button(key="btn_processar").click().run()
    v2 = at.session_state["v2_result"]
    assert v2.config_usada.get("paleta_aplicada") == "Verde"


# ---------------------------------------------------------------------------
# 12 · Adaptador _extrair_config_para_diagnostico (achado Sessão 3 · capability 10)
# ---------------------------------------------------------------------------


def test_adaptador_diagnostico_achata_12_campos(motor_result_padrao):
    """
    _extrair_config_para_diagnostico retorna dict canônico achatado esperado
    por F-APRESENT capability 10 (renderizar_diagnostico · D-165).
    Campos ausentes no contrato real são None · capability 10 trata como '—'.
    """
    from app_v2 import _extrair_config_para_diagnostico
    from visoes.visao_v2 import executar_v2

    ur, mr = motor_result_padrao
    config = {
        "estrutura_entrada": "POR_LINHAS",
        "origem_rotulo_tecnico": "2025-01",
        "comparado_rotulo_tecnico": "2025-02",
        "origem_rotulo_ux": "Janeiro",
        "comparado_rotulo_ux": "Fevereiro",
        "coluna_discriminadora": "Mes",
        "modo_4_ativado": False,
        "estados_nao_escolhidos": [],
        "campo_analisado": "Vendas",
        "tipo_campo": "NUMERICO_ADITIVO",
        "semantica_campo": "MAIOR_MELHOR",
        "regra_agregacao": "SOMA",
        "metodo_consolidacao_relativo": None,
        "campo_peso": None,
        "modo_pre_agregado": False,
        "agrupadores": ["Produto"],
        "resolucao_estrutural": None,
        "thresholds": {
            "limiar_estabilidade_pct": 0.01,
            "limiar_nulo_massivo_pct": 0.20,
            "limite_valores_discriminador_alerta": 50,
            "limite_variacao_extrema_pct": 10.0,
        },
        "modelo_aplicado": None,
    }
    v2 = executar_v2(mr, config)
    dig = _extrair_config_para_diagnostico(
        v2_result=v2,
        paleta_selecionada="Cinza",
        arquivo_nome="base_v2_cliente.xlsx",
        aba_consumida="vendas_padrao",
    )

    # Seção 1 · Como foi analisado
    assert dig["arquivo"] == "base_v2_cliente.xlsx"
    assert dig["aba_consumida"] == "vendas_padrao"
    assert dig["agrupadores"] == ["Produto"]
    assert dig["campo_analisado"] == "Vendas"
    assert dig["tipo_medida"] == "NUMERICO_ADITIVO"
    assert dig["colunas_mapeadas"]["origem_rotulo_ux"] == "Janeiro"
    assert dig["colunas_mapeadas"]["comparado_rotulo_ux"] == "Fevereiro"

    # Seção 4 · Decisões do usuário
    assert dig["estados_nao_escolhidos"] == []

    # Seção 5 · Configurações avançadas
    assert dig["paleta_aplicada"] == "Cinza"
    assert dig["thresholds_usados"]["limiar_estabilidade_pct"] == 0.01
    # defaults_sobrescritos · None aceito (capability 10 trata como '—')
    assert "defaults_sobrescritos" in dig

    # Seção 6 · Qualidade estrutural
    # nulos_por_classificacao · ausente no contrato real · None esperado
    assert dig["nulos_por_classificacao"] is None
    assert dig["total_warnings"] >= 0  # depende da base
    assert isinstance(dig["warnings_por_categoria"], dict)


def test_diagnostico_anexado_a_config_usada_pos_pipeline(motor_result_padrao):
    """Após pipeline, v2_result.config_usada['_config_diagnostico'] preenchido."""
    ur, mr = motor_result_padrao
    at = AppTest.from_file(APP_PATH, default_timeout=60)
    _injetar_estado_e3(
        at, ur, mr, "vendas_padrao",
        estrutura_entrada="POR_LINHAS",
        coluna_discriminadora="Mes",
        origem_rotulo_tecnico="2025-01",
        comparado_rotulo_tecnico="2025-02",
        origem_rotulo_ux="Jan",
        comparado_rotulo_ux="Fev",
    )
    at.run()
    at.selectbox(key="sel_campo").set_value("Vendas").run()
    at.radio(key="rad_tipo").set_value("NUMERICO_ADITIVO").run()
    at.radio(key="rad_sem").set_value("MAIOR_MELHOR").run()
    at.button(key="btn_avancar_e4").click().run()
    at.multiselect(key="ms_agrup").set_value(["Produto"]).run()
    at.button(key="btn_avancar_e5").click().run()
    at.button(key="btn_processar").click().run()

    v2 = at.session_state["v2_result"]
    assert "_config_diagnostico" in v2.config_usada
    diag = v2.config_usada["_config_diagnostico"]
    assert diag["campo_analisado"] == "Vendas"
    assert diag["paleta_aplicada"] == "Azul"  # default
    assert diag["agrupadores"] == ["Produto"]


# ---------------------------------------------------------------------------
# 13 · Stepper user-facing · sem códigos técnicos visíveis (vocab v2 §8)
# ---------------------------------------------------------------------------


def test_stepper_user_facing_sem_codigos_tecnicos():
    """D-167 · stepper "4 etapas + Revisão" · ETAPAS_STEPPER lista de strings user-facing."""
    from app_v2 import ETAPAS_STEPPER

    assert ETAPAS_STEPPER == [
        "1 · Escolher arquivo",
        "2 · Reconhecer estrutura",
        "3 · Configurar análise",
        "4 · Agrupar",
        "Revisar e executar",
    ]
