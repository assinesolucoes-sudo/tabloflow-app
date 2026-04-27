# A-V1 · Relatório Final · 4º quadrado V1

**Sessão:** A-V1 (sessão combinada D-155 · prompt + retrospectiva em 1 bloco)
**Predecessores:** DCV-V1 ✅ · P-V1 v1.1 ✅ · S-V1 v2.0 ✅ · V-V1 ✅
**Data:** 2026-04-26
**Camada 1 Mecânica D-174:** ✅ (com 1 desvio justificado · cobertura `app_v1.py` 78% vs gate 85% · ver §5)

---

## 1 · Resumo

A-V1 entregue · `src/app_v1.py` (~1.959 linhas) espelha `app_v2.py` em 8 estados macro
(vazio · E1_OK · E2 · E3 · E4 · E5 · PROCESSANDO · RESULTADO · ERRO) · 5-etapas-stepper
adaptado V1 (D-212). `src/visoes/exportacao_v1.py` (~1.201 linhas) gera Excel de 6 abas
(5 sem agrupador executivo) consumindo F-APRESENT integralmente (capabilities 1, 2, 4, 5,
11). Suite passou de **978/979 → 1096/1097 verde** · +118 testes novos (alvo 120 ±).
1 vermelho herdado D-220 preservado intocado. Cobertura: `app_v1.py` 78% · `exportacao_v1.py`
94%. Excel-de-exemplo + 3 paletas alternativas em `outputs/exemplo_v1_camada2*.xlsx`
(23-24 KB cada · 6 abas). Pipeline validado contra `casos_esperados.yaml` entrada V1
(V1-A02 · V1-A06 · V1-A11 batem · status Ponte FECHA confirmado).

## 2 · Bifurcações catalogadas

Decisões de UI/ergonomia tomadas durante Fase b sem perguntar (Lei 4 do prompt).
Custo de retrabalho baixo · sujeitas a revisão na retrospectiva.

### BIF-1 · Microcopy do botão "Aplicar modelo" pré-E5
**Contexto:** S-V1 §3.2 declara "habilita expander de upload de modelo · disabled em
estado vazio" mas não detalha em E2/E3/E4.
**Opções:** (A) habilita em todas as etapas pós-vazio · (B) habilita só em ≥E5.
**Escolha:** **A** · espelha V2 literalmente (`disabled = etapa == "vazio"`).
**Custo retrabalho:** baixo · 1 linha.
**Pode ser revogada:** sim.

### BIF-2 · Default `n_arquivos` ao reabrir tela vazio
**Contexto:** Após Nova análise, n_arquivos volta ao default 1 ou último escolhido?
**Opções:** (A) sempre 1 · (B) preserva último.
**Escolha:** **A** (default 1) · `_init_state` impõe defaults canônicos · Nova análise
chama `_reset_completo`.
**Custo:** baixo.
**Pode ser revogada:** sim.

### BIF-3 · Ordem dos cards do repeater (E3 sub-3.1 e 3.2)
**Contexto:** Adicionar agrupador/campo · novo card vai para o topo ou para baixo?
**Opções:** (A) último adicionado embaixo · (B) último em cima.
**Escolha:** **A** · espelha padrão de listas em UI · também espelha lógica V2.
**Custo:** baixo.
**Pode ser revogada:** sim.

### BIF-4 · `B-V1-CHAVE-INVALIDA` warning sem prompt de override
**Contexto:** S-V1 §2.5 diz que B-V1-CHAVE-INVALIDA é "escapável (Sim · ECP P3)".
**Opções:** (A) só `st.warning` inline · (B) `st.warning` + checkbox "Confirmo override"
+ disable Avançar.
**Escolha:** **A** · warning visível mas Avançar permanece habilitado. Razão:
override implícito · Usuária está consciente do warning · MVP simples.
**Custo:** médio (se Usuária pedir gate explícito).
**Pode ser revogada:** sim.

### BIF-5 · KPI primário em RESULTADO com >1 campo
**Contexto:** S-V1 §3.11 declara 4 cards · em V2 cards 1-3 mostram totais. Em V1, com
N campos, qual campo virar referência dos cards 1-3 (Total Origem · Total Comparado ·
Diferença líquida)?
**Opções:** (A) primeiro campo da lista · (B) dropdown "Mostrar totais de:" · (C)
N×3 cards.
**Escolha:** **A** · primeiro campo da lista · MVP simples. Card 4 (Taxa de Conciliação)
é KPI primário independentemente.
**Custo:** médio (Usuária pode querer dropdown).
**Pode ser revogada:** sim.

### BIF-6 · Microcopy de Caso Lógico user-facing em E5/Aba 1
**Contexto:** "MESMA_ABA_EM_COLUNAS" técnico precisa de tradução.
**Opções:** literal técnico · "Mesma aba em colunas" · "Mesma aba · em colunas distintas"
**Escolha:** **"Mesma aba · Origem e Comparado em colunas distintas"** (caso 3) e
**"Abas distintas · match executado"** (caso 1/2). Razão: P-V1 §2.2-§2.3 + microcopy de
S-V1 §3.7 inline.
**Custo:** baixo.
**Pode ser revogada:** sim.

### BIF-7 · Tela ERRO · botão "Voltar para revisar"
**Contexto:** S-V1 §3.1 lista ERRO como estado mas não detalha escape.
**Opções:** (A) só mensagem · (B) botão para E5 · (C) botão Nova análise.
**Escolha:** **B** · botão "Voltar para revisar configuração" transita para E5 e limpa
`_erro_msg`. Permite Usuária ajustar config sem perder upload/etapa anterior.
**Custo:** baixo.
**Pode ser revogada:** sim.

### BIF-8 · Cache de Excel por paleta no RESULTADO
**Contexto:** S-V1 §3.11 implica que trocar paleta regenera Excel.
**Opções:** (A) regenera ao trocar · (B) cache por paleta · (C) regenera ao baixar.
**Escolha:** **B** · `_excel_cache_{paleta_tech}` em session_state. Trocar paleta não
limpa caches de outras paletas (re-download da mesma paleta usa cache · econômico).
Cache invalidado em `_invalidar_a_partir` (qualquer edição downstream).
**Custo:** baixo.
**Pode ser revogada:** sim.

### BIF-9 · Aba 5 (Ponte) sempre presente · mesmo em MESMA_ABA_EM_COLUNAS
**Contexto:** Em MESMA_ABA_EM_COLUNAS, `ajuste_so_*` é Decimal('0') por construção.
A Ponte ainda faz sentido (decompõe diferença líquida)?
**Opções:** (A) sempre 6 abas · (B) omitir Aba 5 em MESMA_ABA.
**Escolha:** **A** · sempre 6 abas (5 sem agrupador executivo). Razão: ordem fixa de
abas é invariante (S-V1 §2.11 + Mockup §2). Em MESMA_ABA_EM_COLUNAS a Ponte mostra os 7
componentes com SO_* zerados · auditável e consistente.
**Custo:** baixo.
**Pode ser revogada:** sim.

### BIF-10 · "Salvar como modelo" em E4 vazia (sem agrupadores executivos)
**Contexto:** S-V1 declara que modelo é exportável em ≥E5. E4 com 0 executivos é
configuração válida.
**Opções:** (A) gate por etapa · (B) gate por config completa.
**Escolha:** **A** · disabled em < E5 · espelha V2 literalmente. Modelo salvo na E5
preserva `agrupadores_executivos: []` corretamente.
**Custo:** baixo.
**Pode ser revogada:** sim.

### BIF-11 · Cobertura `app_v1.py` 78% vs gate 85%
**Contexto:** Paths de upload físico (`_processar_upload_caso1` etc.) e renderização de
download_button via cache não são triviais de cobrir via AppTest. Streamlit AppTest
não simula bem `st.file_uploader.getvalue()`.
**Opções:** (A) aceitar 78% como teto pragmático · (B) escrever fixture pesado com mocks
para empurrar cobertura para ≥85%.
**Escolha:** **A** · documentar como desvio. Toda lógica analítica de A-V1 está coberta
(navegação · invalidação · construção de config · pipeline real via E2E). Paths não
cobertos são interações UI raras (errors de leitura de arquivo · CSV sem aba).
**Custo retrabalho:** médio (sub-sessão de cobertura ~1h se Usuária pedir).
**Pode ser revogada:** sim · ESCALAR PARA ARQUITETO se gate 85% for inegociável.

## 3 · Output do `grep -rn "TODO-FAPRESENT-CLEANUP" src/`

```
src/app_v2.py:178:    TODO-FAPRESENT-CLEANUP: promover para capability 2 (traduzir) ou criar
src/testes/test_exportacao_v2.py:523:    offset bespoke em exportacao_v2.py (TODO-FAPRESENT-CLEANUP capability 11).
src/testes/V-V1_RELATORIO.md:128:## 4 · Output `grep -r "TODO-FAPRESENT-CLEANUP" src/`
src/testes/V-V1_RELATORIO.md:131:$ grep -rn "TODO-FAPRESENT-CLEANUP" src/
src/testes/V-V1_RELATORIO.md:138:**0 novos marcadores `TODO-FAPRESENT-CLEANUP`** adicionados em V-V1
src/visoes/exportacao_v2.py:854:    # TODO-FAPRESENT-CLEANUP: promover para capability 3 (criar_tabela_executiva
src/visoes/exportacao_v2.py:943:    # TODO-FAPRESENT-CLEANUP: promover para capability 3 (criar_tabela_executiva
```

**0 novos `TODO-FAPRESENT-CLEANUP` adicionados em A-V1** · todas as 7 ocorrências são
pré-existentes (V2 + ancoragem V-V1). Razão:
- `exportacao_v1.py` usa F-APRESENT integralmente (capability 1 paletas · capability 11
  formato adaptativo via `number_format_valor`/`number_format_diferenca` · capability 4-5
  formatação monetária/percentual)
- `app_v1.py` consome `formatar_valor_por_unidade` · `formatar_diferenca_por_unidade`
  · `formatar_percentual_br` direto de `apresentacao.formatos`
- Helpers visuais (`_renderizar_cabecalho_secao` · `_renderizar_secao_como_tabela` ·
  `_mesclar_card` · `bordas_finas`) são importados de `apresentacao.templates.familia_a._shared`

Único helper bespoke local em `exportacao_v1.py`: `_escrever_minitabela` (mini-tabela
inline para Resumo Executivo). Não promovido a capability porque é específico do leiaute
de Aba 1 V1 e a S-V1 §2.10 não exige reuso. Catalogado como candidato a promoção em
sub-sessão F-APRESENT futura (sem TODO marcador · decisão consciente).

## 4 · Checklist Mecânico D-174 · Camada 1 (cópia consolidada)

Ver `src/testes/CHECKLIST_MECANICO.md` (sobrescreve V-V1).

Resumo: **24/25 ✅ · 1 desvio justificado** (cobertura `app_v1` 78% vs gate 85% · BIF-11).

## 5 · Sugestões para a Camada 2 da Usuária

### 5.1 · Roteiro sugerido para validação visual

1. Abrir `outputs/exemplo_v1_camada2.xlsx` (paleta Azul executivo · default).
2. **Aba 1 · Resumo Executivo** · conferir as 9 seções na ordem (Mockup-V1 §3):
   - § Cabeçalho identificador · "Conciliação de Bases · Razão × Balancete"
   - § Taxa de Conciliação · card único centralizado + tabela 6 classes + Total
   - § Volumetria · 3 linhas (Razão · Balancete · Processados)
   - § Status da Ponte · banner verde "✅ Ponte fecha em todos os campos"
   - § Valor por campo comparado · 1 linha (Valor) · MONETARIO_BRL
   - § Cobertura por base · 2 linhas
   - § Resumo por agrupador · "Resumo por Centro_Custo" (CONDICIONAL · presente)
   - § Síntese do Diagnóstico · 4 linhas
   - § Configuração aplicada · agrupadores match · campos · caso lógico · paleta
   - Bloco final · Leitura Qualitativa (texto consolidado · 3-6 frases)
3. **Aba 2 · Resumo por Agrupador** · 1 linha por valor único de Centro_Custo · com
   colunas N Conciliados · N Divergentes · Soma Razão/Balancete · Diferença líquida ·
   Σ |Diferença| do campo Valor.
4. **Aba 3 · Mapa de Conciliação** · 1 linha por registro processado · coluna
   Classificação com vocabulário user-facing (ex: "Saiu do Razão" · "Apareceu no Balancete"
   · "Divergente por valor" · "Divergência por duplicidade").
5. **Aba 4 · Análise Analítica** · 1 linha por registro · 4 colunas dedicadas ao campo
   Valor (Valor Razão · Valor Balancete · Diferença · Status).
6. **Aba 5 · Ponte de Conciliação** · sub-Ponte para o campo Valor (único elegível) · 7
   linhas de decomposição + verificação ✅ Fecha.
7. **Aba 6 · Diagnóstico** · 6 seções · ÚLTIMA aba (D-017) · contém configuração técnica
   completa + status da Ponte.
8. **Trocar paletas** · abrir `outputs/exemplo_v1_camada2_verde.xlsx` (Verde) ·
   `_cinza.xlsx` (Cinza) · `_vinho.xlsx` (Vinho). Mesma estrutura · cores diferentes.

### 5.2 · Sanity checks numéricos explícitos (D-183)

Pipeline executou sobre `bases/base_fundacao.xlsx` (abas `dual_origem_crm` · `dual_comparado_erp`):

| Métrica | Valor esperado | Validado em |
|---|---|---|
| Caso lógico inferido | `ABAS_DISTINTAS` | ✅ test_e2e_abas_distintas_pipeline_completo |
| Registros processados | 205 | ✅ pipeline real |
| `CONCILIADO` | 0 | ✅ V1-A05 (faixa 0-2) · valor exato 0 |
| `DIVERGENTE_VALOR` | 10 | ✅ V1-A01 (faixa 8-12) |
| `SO_ORIGEM` | 36 | ✅ V1-A02 (faixa 34-38) |
| `SO_COMPARADO` | 44 | ✅ V1-A03 (faixa 42-46) |
| `DIVERGENCIA_DUPLICIDADE` | 44 | ✅ V1-A04 (faixa 42-46) |
| `DIVERGENCIA_AMBIGUIDADE` | 0 | ✅ V1-A06 (exato 0 em modo EXATO) |
| Status Ponte geral | `FECHA` | ✅ V1-A11 |
| Cobertura · não-None em ABAS_DISTINTAS | sim | ✅ invariante I7 do motor |
| 4 paletas geram Excel ≥ 5KB | sim | ✅ TestExportacaoPaletas |
| 6 abas em ordem fixa | sim | ✅ test_ordem_abas_canonica |
| Aba 6 sempre Diagnóstico (D-017) | sim | ✅ test_diagnostico_eh_ultima_aba_d017 |

## 6 · Anomalias e ressalvas

### 6.1 · Cobertura `app_v1.py` 78% (BIF-11)
Documentada acima · não bloqueia entrega Camada 1 mas é desvio do gate 85% do prompt §14.

### 6.2 · `_escrever_minitabela` é helper bespoke local
Não promovido a capability F-APRESENT · candidato para sub-sessão F-APRESENT futura.
Nenhum `TODO-FAPRESENT-CLEANUP` adicionado · decisão consciente (uso restrito ao Resumo
Executivo V1 · S-V1 §2.10 não exige reuso).

### 6.3 · Caso 4 (D-213) fora de escopo MVP
Combinação `n_arquivos==2 + MESMA_ABA_EM_COLUNAS` (2 arquivos · 1 aba cada · em colunas)
não implementada · S-V1 §3.5 explicita "fora de MVP". Sem desvio do prompt.

### 6.4 · `MESMA_ABA_EM_COLUNAS` real testado só no motor (V-V1)
`test_exportacao_v1.py::TestExportacaoMesmaAba::test_placeholder_mesma_aba_documentado`
é placeholder · base_fundacao.xlsx não tem aba com 2 colunas de valor distintas
para exercitar o ramo MESMA_ABA realista na exportação. Cobertura desse ramo está em
`test_visao_v1_mesma_aba.py` (V-V1).

### 6.5 · Smoke do botão `btn_processar` em E5 confirma fluxo
`test_e5_botao_processar_aciona_pipeline_real` exercita o fluxo PROCESSANDO → RESULTADO
real (sem mock) usando base_fundacao + config canônica. Pipeline conclui em <1s.

## 7 · Próximo passo · VV-V1 (5º + 6º quadrados)

Conforme planilha v6 (89bb3e1) · ciclo V1 fica `✅✅✅✅⬜⬜` após A-V1 fechar.

Pendências pré-VV-V1 declaradas (registradas em S-V1 e V-V1 anteriores):
- **D-216** · `ESTADO_SITUACAO` categórico · ramo lógico para campo de tipo categoria
  (não numérico). Não exercitado em A-V1 · base_fundacao não tem campo `ESTADO_SITUACAO`
  na config canônica.
- **D-217** · aba MESMA_ABA sintética · base_fundacao precisa de aba dedicada para Caso 3
  realista (atualmente exercitado só por testes do motor com fixtures sintéticas).
- **R1-VV-V1** · auditoria epistemológica de `casos_esperados.yaml` entrada V1 · validar
  faixas empíricas (V1-A01..V1-A12) contra novas execuções.

VV-V1 pode usar `outputs/exemplo_v1_camada2.xlsx` como referência visual · pula geração de
Excel auxiliar.

## 8 · Materiais entregues

| Artefato | Linhas | Tipo |
|---|---|---|
| `src/app_v1.py` | 1.959 | novo (Streamlit app V1) |
| `src/visoes/exportacao_v1.py` | 1.201 | novo (Excel 6 abas) |
| `src/testes/test_app_v1_apptest.py` | 981 | novo (84 testes) |
| `src/testes/test_exportacao_v1.py` | 444 | novo (27 testes) |
| `src/testes/test_app_v1_e2e_excel.py` | 224 | novo (7 testes) |
| `src/scripts/gerar_exemplo_v1_camada2.py` | 135 | novo |
| `outputs/exemplo_v1_camada2.xlsx` | — | gerado (23.781 bytes · paleta azul) |
| `outputs/exemplo_v1_camada2_verde.xlsx` | — | gerado (23.780 bytes) |
| `outputs/exemplo_v1_camada2_cinza.xlsx` | — | gerado (23.776 bytes) |
| `outputs/exemplo_v1_camada2_vinho.xlsx` | — | gerado (23.779 bytes) |
| `src/testes/A-V1_ANCORAGEM.md` | — | novo (10 seções) |
| `src/testes/A-V1_RELATORIO.md` | — | este documento |
| `src/testes/CHECKLIST_MECANICO.md` | — | sobrescreve V-V1 |

**Suite final:** **1.097 testes** (1.096 verde + 1 vermelho herdado D-220).
**Suite delta:** baseline 978 verde → +118 novos · zero novo vermelho.
**Cobertura:** `app_v1.py` **78%** · `exportacao_v1.py` **94%**.
**Excel-de-exemplo gerado:** 4 paletas · 6 abas cada · ~23-24 KB.

---

*Fim do relatório A-V1.* Pronto para retrospectiva combinada D-155 com Arquiteto.
