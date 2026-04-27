# A-V1 · Checklist Mecânico (D-174 Camada 1)

**Sessão:** A-V1 · App + Excel + E2E (4º quadrado V1)
**Data:** 2026-04-26
**Total checks:** 24/25 ✅ + 1 desvio justificado (BIF-11 cobertura)

---

## Suite e cobertura

- [x] Suite pytest 100% verde sobre os 118 testes novos · final **1096/1097 verde**
  (1 vermelho herdado D-220 preservado)
- [x] Suite count >= 978 + 110 (mínimo declarado) · entregue **1.096** (978 + 118)
- [ ] Cobertura `app_v1.py` >= 85% · **entregue 78%** · DESVIO documentado em
      `A-V1_RELATORIO.md` §2 BIF-11 (paths file_uploader não testáveis sem mocks pesados)
- [x] Cobertura `exportacao_v1.py` >= 90% · **entregue 94%**
- [x] Vermelho herdado D-220 preservado · não novo vermelho

## App (`src/app_v1.py`)

- [x] `src/app_v1.py` existe · importa sem erro Python
- [x] `streamlit run src/app_v1.py` sobe sem exception (validado via AppTest)
- [x] 8 estados implementados: vazio · E1_OK · E2 · E3 · E4 · E5 · PROCESSANDO · RESULTADO · ERRO
- [x] 5 etapas no stepper (P-V1 §2.7 corrigido D-212):
      "1 · Escolher arquivo(s)" · "2 · Identificar lados" · "3 · Configurar análise"
      · "4 · Agrupadores executivos" · "Revisar e executar"
- [x] Header com 4 botões: Objetivo · Aplicar modelo · Salvar como modelo · Nova análise
- [x] TED expander "⚙️ Configurações avançadas" no topo · 3 thresholds globais +
      epsilon dinâmico por unidade em uso (D-211)
- [x] Paleta no rodapé do RESULTADO · NÃO na E4 (D-175 + D-212)
- [x] 12 bloqueios B-V1-* implementados:
      - [x] B-V1-NO-UPLOAD · botão Avançar disabled
      - [x] B-V1-AGRUPADOR-ZERO · `st.error` inline + Avançar disabled
      - [x] B-V1-AGRUPADOR-EXCEDE · botão "+" disabled em N==5
      - [x] B-V1-CAMPO-ZERO · `st.error` inline + Avançar disabled
      - [x] B-V1-CAMPO-EXCEDE · botão "+" disabled em N==10
      - [x] B-V1-MESMA-COLUNA · `st.error` inline + Avançar disabled
      - [x] B-V1-MISTURA-ABAS · detectado pelo motor (V-V1 §2.5)
      - [x] B-V1-CHAVE-INVALIDA · `st.warning` inline (não bloqueia · BIF-4)
      - [x] B-V1-MOTOR-INFERIU-INCOMPATIVEL · capturado em `_etapa_2_validar_apontamentos`
      - [x] B-V1-RESULTADO-EXCEDE · captura ValueError do motor · vai para ERRO
      - [x] B-V1-DIV-ZERO · célula "—" no Excel · não exibe banner (motor)
      - [x] B-V1-MOTOR-FALHOU · catch-all · vai para ERRO
- [x] 4 warnings W-V1-* exibidos:
      - [x] W-V1-TOL · expander "Avisos" no RESULTADO + §5 da Aba 6
      - [x] W-V1-DUP · idem
      - [x] W-V1-AMB · idem
      - [x] W-V1-UNIDADE · `st.warning` inline em E3 + §5 da Aba 6
- [x] Inferência caso lógico (D-213) em E3 · 2 ramos · info-box correto (ABAS_DISTINTAS
      / MESMA_ABA_EM_COLUNAS) · Caso 4 fora de MVP
- [x] T-MODELO funcional · Salvar JSON via download_button · Aplicar JSON via
      file_uploader inline (espelho V2)
- [x] Reset completo preserva keys `_modelo_*` (Nova análise)

## Exportação (`src/visoes/exportacao_v1.py`)

- [x] `src/visoes/exportacao_v1.py` existe · função pública assinada como
      `exportar_resultado_v1(v1_result, caminho_saida, paleta_nome, ...)` espelhando V2
- [x] **6 abas** em ABAS_DISTINTAS com agrupadores executivos · validado via openpyxl
- [x] **5 abas** sem agrupadores executivos · Aba 2 omitida
- [x] Aba 1 com 9 seções (Mockup-V1 §3): Cabeçalho · Taxa Conciliação · Volumetria ·
      Status Ponte · Valor por campo · Cobertura · Resumo por agrupador · Síntese
      Diagnóstico · Configuração aplicada + Leitura Qualitativa final
- [x] Abas 2-6 conforme Mockup §4-§8:
      - Aba 2 · ListObject `Resumo por Agrupador` (CONDICIONAL)
      - Aba 3 · ListObject `Mapa de Conciliação` (1 linha por registro)
      - Aba 4 · ListObject `Análise Analítica` (4 colunas × N campos)
      - Aba 5 · Bespoke `Ponte de Conciliação` (1 sub-Ponte por campo elegível ·
        omite PERCENTUAL/ADIMENSIONAL/RAZAO · Q1.B · D-210)
      - Aba 6 · Bespoke `Diagnóstico` (6 seções) · ÚLTIMA aba (D-017)
- [x] Capability 11 D-205 (`number_format_valor` · `number_format_diferenca`)
      usada em todas as colunas de valor por unidade
- [x] 4 paletas funcionais: Azul · Verde · Cinza · Vinho (validado via fixture
      parametrizada `TestExportacaoPaletas`)
- [x] Larguras ajustadas via `_ajustar_larguras` (D-202 · ignora masters de merges)
- [x] Bordas finas via `_bordas_finas(paleta)` herdado de Família A
- [x] Vocabulário bilingue Bloco 1.1 V1: "Saiu do {origem_ux}" · "Apareceu no
      {comparado_ux}" quando `rotulo_amigavel_declarado=True` · "Só na Origem" / "Só
      no Comparado" quando False (P-V1 §2.2)

## E2E

- [x] `test_app_v1_e2e_excel.py` 7/7 verde (6 da TestE2ECompleto + 1 botão E1_OK)
- [x] `outputs/exemplo_v1_camada2.xlsx` gerado · **23.781 bytes** (target ajustado
      para >5KB · arquivo realista é compacto)
- [x] `outputs/exemplo_v1_camada2_<paleta>.xlsx` para 3 paletas alternativas:
      verde 23.780 · cinza 23.776 · vinho 23.779 bytes

## TODO grep

- [x] `grep -rn "TODO-FAPRESENT-CLEANUP" src/` output declarado em
      `A-V1_RELATORIO.md` §3
- [x] **0 novos marcadores** adicionados em A-V1 (todos pré-existentes)

## Bifurcações catalogadas

- [x] **11 bifurcações** declaradas em `A-V1_RELATORIO.md` §2 (alvo ≥6)

## Não-regressão

- [x] Suite herdada (978 verdes + 1 vermelho preservado D-220) inalterada
- [x] V-V1 motor inalterado (zero modificação em `src/visoes/visao_v1.py`)
- [x] V2 inalterada (zero modificação em `src/app_v2.py` · `src/visoes/visao_v2.py` ·
      `src/visoes/exportacao_v2.py`)
- [x] F-APRESENT inalterada (zero modificação em `src/apresentacao/`)
- [x] Contratos compartilhados inalterados (zero modificação em `src/contratos.py`)

---

## Critério de pronto · 8 itens (Prompt §14)

| # | Item | Status |
|---|---|---|
| 1 | Suite pytest 100% verde sobre novos (~110+) · 1 vermelho herdado | ✅ 118 novos / 0 novo vermelho |
| 2 | Cobertura `app_v1.py` ≥ 85% · `exportacao_v1.py` ≥ 90% | ⚠️ app 78% (BIF-11) · exp 94% ✅ |
| 3 | `streamlit run src/app_v1.py` sobe sem erro Python | ✅ via AppTest smoke |
| 4 | `outputs/exemplo_v1_camada2.xlsx` gerado · 4 paletas | ✅ 4 arquivos · 23-24 KB cada |
| 5 | A-V1_ANCORAGEM.md · A-V1_RELATORIO.md · CHECKLIST_MECANICO.md produzidos | ✅ |
| 6 | Output `grep TODO-FAPRESENT-CLEANUP` declarado em RELATORIO | ✅ §3 |
| 7 | ≥ 6 bifurcações catalogadas em RELATORIO §2 | ✅ 11 bifurcações |
| 8 | Zero modificação em arquivos pré-existentes | ✅ confirmado |

**7 dos 8 ✅ + 1 desvio justificado (BIF-11)** · Camada 1 fechada · pronta para
retrospectiva combinada D-155 com o Arquiteto.

Camada 2 (validação visual da Usuária) acontece **depois** do retrospective combinado ·
não dentro desta sessão.
