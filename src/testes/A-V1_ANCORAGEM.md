# A-V1 · Ancoragem (D-185 Fase a · executada pelo Arquiteto · ratificada por mim na Fase b)

**Sessão:** A-V1 · 4º quadrado V1 · sessão combinada D-155
**Data da ancoragem:** 2026-04-26
**Predecessores verdes:** DCV-V1 ✅ · P-V1 v1.1 ✅ · S-V1 v2.0 ✅ · V-V1 ✅ (978/979 verde · 1 vermelho herdado D-220)

---

## 1 · O que A-V1 entrega

Um app Streamlit (`src/app_v1.py`) que orquestra a sequência canônica
`motor_upload → motor_base → executar_v1 → exportar_resultado_v1` em 8 estados macro
(vazio · E1_OK · E2 · E3 · E4 · E5 · PROCESSANDO · RESULTADO · ERRO),
espelhando estruturalmente `app_v2.py` (canônico · suite 746/746). Adiciona
`src/visoes/exportacao_v1.py` consumindo F-APRESENT integralmente para um Excel
de 6 abas (ou 5 quando agrupadores executivos não configurados). O app NÃO
calcula · NÃO infere · NÃO interpreta — toda leitura analítica vem de
`ConciliacaoV1Result`. Camada 1 D-174 totalmente mecânica · facilita Camada 2
da Usuária via Excel-de-exemplo.

## 2 · Contratos consumidos da V-V1

| Contrato | Chave de uso | Onde aparece no app/exportação |
|---|---|---|
| `ConciliacaoV1Result` | resultado canônico do motor | _tela_resultado · exportar_resultado_v1 |
| `ConciliacaoRealizadaV1` | declarativo (D-213) · n_arquivos · caso_logico_inferido · origem_ux · comparado_ux | Cabeçalho do RESULTADO · Aba 1 §1 · Aba 6 |
| `RegistroConciliadoV1` | 1 linha por registro processado | Aba 3 · Aba 4 |
| `ContagemPorClassificacao: Dict[ClassificacaoRegistroV1, int]` | 6 classes (4 zeradas em MESMA_ABA) | Bloco saúde do RESULTADO · §2 da Aba 1 |
| `CoberturaV1` | None em MESMA_ABA_EM_COLUNAS | §6 da Aba 1 |
| `ValorPorCampoV1` | 1 entrada por campo comparado | KPI cards · §5 da Aba 1 · Aba 2 |
| `LinhaResumoAgrupadorV1` (Optional) | None quando agrupadores executivos vazios | §7 da Aba 1 · Aba 2 (CONDICIONAL) |
| `PonteCampoV1` | omite PERCENTUAL/ADIMENSIONAL/RAZAO (Q1.B · D-210) | Bloco status no RESULTADO · §4 da Aba 1 · Aba 5 |
| `StatusPonteV1` (`FECHA` / `COM_RESIDUO`) | banner colorido | RESULTADO · §4 da Aba 1 |
| `SinteseDiagnosticoV1` | 7 contadores (4 zeram em MESMA_ABA) | §8 da Aba 1 · Aba 6 |
| `ConfigAplicadaV1` | reflexo declarativo | §9 da Aba 1 · Aba 6 |
| `LeituraQualitativaV1` | texto-livre parametrizado | Bloco final RESULTADO · final da Aba 1 |
| `WarningV1` | 4 W-V1-* + warnings herdados do motor | Expander avisos do RESULTADO · §5 da Aba 6 |
| `ModeloAplicadoV1` (Optional) | T-MODELO referência | §1 da Aba 1 quando aplicado |
| Enums: `CasoLogicoV1`, `ModoMatchV1`, `TipoCampoV1`, `UnidadeCanonica`, `ClassificacaoRegistroV1`, `StatusCampoV1`, `StatusPonteV1` | dispatch de microcopy/format | espalhados |

## 3 · 8 estados macro do app · espelho V2 + adaptações V1 (S-V1 §3.1)

| Estado V1 | Análogo V2 | Conteúdo principal |
|---|---|---|
| `vazio` | `vazio` | Radio "Quantos arquivos? (1/2)" + 1 ou 2 file_uploaders. Sem stepper. |
| `E1_OK` | `E1_OK` | Pós-upload físico · multiselect 1-2 abas (n=1) ou 2 selectbox (n=2) · Confirmar e processar bases. |
| `E2` | `E2` reduzido | Identificar lados · 2 text_input rótulos amigáveis Origem/Comparado. |
| `E3` | `E3+E4` mergeado | Configurar análise: Sub-3.1 agrupadores match (repeater 1-5) · Sub-3.2 campos comparados (repeater 1-10) · info-box do caso lógico inferido (D-213). |
| `E4` | `E4` (Agrupar) | Agrupadores executivos · multiselect 0-5 · OPCIONAL · botão "Pular" disponível. |
| `E5` | `E5` Revisão | 5 colunas-resumo + botão Processar análise. |
| `PROCESSANDO` | `PROCESSANDO` | Spinner · `executar_v1` é chamado. Não-cancelável. |
| `RESULTADO` | `RESULTADO` | 5 blocos executivos + rodapé Voltar/Paleta/Baixar/Nova. |
| `ERRO` | `ERRO` | Mensagem de bloqueio B-V1-* · botão para voltar. |

**Não existe `RESOL_CASO`** (V2 tem · V1 não · S-V1 §3.1 explícito · D-213).

## 4 · Estrutura do Excel exportado · 6 abas (S-V1 §2.11 + Mockup-V1 + P-V1 §3)

| # | Nome user-facing (A1) | Natureza | Aparece | Contrato consumido |
|---|---|---|---|---|
| 1 | Resumo Executivo | Bespoke · 9 seções narrativas | Sempre | `ConciliacaoV1Result` integral |
| 2 | Resumo por Agrupador | Tabular ListObject · expandido | Quando `resumo_por_agrupador_executivo` ≠ None | `LinhaResumoAgrupadorV1` |
| 3 | Mapa de Conciliação | Tabular ListObject · todos os registros | Sempre | `RegistroConciliadoV1` (consolidado) |
| 4 | Análise Analítica | Tabular ListObject · expansão por campo | Sempre | `RegistroConciliadoV1.valores_por_campo` |
| 5 | Ponte de Conciliação | Bespoke · decomposição vertical | Sempre | `PonteCampoV1[*]` |
| 6 | Diagnóstico | Bespoke · 6 seções | Sempre · ÚLTIMA (D-017) | `SinteseDiagnosticoV1` · `WarningV1[*]` · `ConfigAplicadaV1` |

## 5 · 12 bloqueios B-V1-* · onde cada um é detectado e exibido (S-V1 §2.5)

| Código | Detecção (etapa) | Exibição (UI) |
|---|---|---|
| `B-V1-NO-UPLOAD` | E0 vazio sem arquivo | botão "Avançar" disabled (não banner) |
| `B-V1-AGRUPADOR-ZERO` | E3 sub-3.1 com 0 agrupadores | `st.error` inline + botão Avançar disabled |
| `B-V1-AGRUPADOR-EXCEDE` | E3 ao tentar adicionar 6º card | botão "+" desabilitado em N==5 (preventivo) |
| `B-V1-CAMPO-ZERO` | E3 sub-3.2 com 0 campos | `st.error` inline + Avançar disabled |
| `B-V1-CAMPO-EXCEDE` | E3 ao tentar adicionar 11º card | botão "+" desabilitado em N==10 |
| `B-V1-MESMA-COLUNA` | E3 com algum apontamento `nome_origem == nome_comparado` na mesma aba | `st.error` inline (local da edição) + Avançar disabled |
| `B-V1-MISTURA-ABAS` | E3 com apontamentos misturando aba_origem≠aba_comparado em 1 arquivo (parte mesma aba · parte abas distintas) | `st.error` inline + Avançar disabled |
| `B-V1-CHAVE-INVALIDA` | E3 quando coluna escolhida como agrupador tem ≥ TED `chave_nulos_max` | `st.warning` inline (não bloqueia · ECP P3 escapável) |
| `B-V1-MOTOR-INFERIU-INCOMPATIVEL` | E3 quando tipo declarado ≠ tipo inferido pelo motor_base | `st.warning` inline + override autorizado |
| `B-V1-RESULTADO-EXCEDE` | PROCESSANDO quando `n_processados > volume_max` | `st.error` em ERRO · escapável via TED |
| `B-V1-DIV-ZERO` | dentro do motor (Σ origem == 0) | célula "—" em RESULTADO/Excel · não exibe banner |
| `B-V1-MOTOR-FALHOU` | catch-all do motor (exception inesperada) | tela `ERRO` com microcopy + botão "Voltar" |

## 6 · 4 warnings W-V1-* · onde cada um é exibido (S-V1 §2.7)

| Código | Detecção | Exibição |
|---|---|---|
| `W-V1-TOL` | motor → `n_tolerancia_absorvida ≥ 1` | expander "⚠️ Avisos" no RESULTADO · §5 da Aba 6 |
| `W-V1-DUP` | só em ABAS_DISTINTAS · ≥ 1 chave duplicada | idem · com microcopy "0 ocorrências · não aplicável neste caso lógico" em MESMA_ABA |
| `W-V1-AMB` | só em ABAS_DISTINTAS · ≥ 1 chave com múltiplos candidatos | idem |
| `W-V1-UNIDADE` | E3 com tipo↔unidade divergente | `st.warning` inline em E3 · também aparece em §5 da Aba 6 |

## 7 · 8 thresholds TED · expander no topo (D-211 + D-178)

| Código técnico | Label user-facing | Default | Tipo |
|---|---|---|---|
| `chave_nulos_max` | "Limite de células vazias em coluna de chave" | `0.50` | Decimal/float |
| `volume_max` | "Limite de registros processados" | `500_000` | int |
| `concentracao_agrupador_principal_min` | "Limite de concentração para citar agrupador principal" | `0.70` | Decimal/float |
| `epsilon_por_unidade.MONETARIO_BRL` | "Tolerância de fechamento da Ponte · valores monetários" | `Decimal("0.01")` | Decimal |
| `epsilon_por_unidade.QUANTIDADE` | "Tolerância · quantidades" | `Decimal("0")` | Decimal |
| `epsilon_por_unidade.TEMPO_DIAS` | "Tolerância · prazos em dias" | `Decimal("0")` | Decimal |
| `epsilon_por_unidade.TEMPO_HORAS` | "Tolerância · prazos em horas" | `Decimal("0.01")` | Decimal |
| `epsilon_por_unidade.MULTIPLICADOR` | "Tolerância · índices" | `Decimal("0.0001")` | Decimal |

`epsilon_por_unidade.{X}` só aparece no expander quando E3 sub-3.2 declara
algum campo com a unidade `{X}` (Q2.C · D-211).

## 8 · O que A-V1 NÃO faz (recapitulação das 4 leis invioláveis)

1. **Não calcula · não infere · não interpreta** — todo número/categoria vem de `executar_v1` (Lei 1).
2. **O Excel é o produto** · app é instrumento de configuração (Lei 2 · D-163).
3. **`app_v2.py` é canônico estrutural** · `app_v1.py` espelha moldura · diferenças semânticas (5 etapas V1 vs 4+revisão V2 · N agrupadores match + N campos comparados V1 vs 1 campo + N agrupadores V2) ficam dentro das telas (Lei 3).
4. **Bifurcações de UI/ergonomia: Fase b decide e cataloga** · sem perguntar (Lei 4).

Mais 4 anti-padrões críticos:

5. NÃO tocar em `src/visoes/visao_v1.py` (motor congelado pós-V-V1).
6. NÃO inventar microcopy · tudo vem de P-V1 §2-§4 · vocabulário bilingue Bloco 1.1 V1 · Mockup-V1.
7. NÃO duplicar capability F-APRESENT · sempre usar `formatar_valor_por_unidade(valor, unidade)` etc. (D-175).
8. NÃO escrever IA (Fase 3 · não A-V1).

## 9 · Bifurcações antecipadas (lista do que pode aparecer · não decidir aqui)

Catalogadas durante Fase b · viram Seção 2 do `A-V1_RELATORIO.md`. Esperado ~6-10 itens. Candidatas:

- **BIF-1 · Microcopy do botão "Aplicar modelo"** quando habilitado pós-vazio mas pré-E5
- **BIF-2 · Default `n_arquivos`** ao reabrir a tela de upload (1 ou último escolhido?)
- **BIF-3 · Ordem de exibição dos cards do repeater de agrupadores match** (último adicionado em cima ou embaixo?)
- **BIF-4 · Tratamento do botão "Avançar" quando há `B-V1-CHAVE-INVALIDA` (warning)** · pergunta de override explícita ou só warning visível?
- **BIF-5 · KPI primário em RESULTADO** · 4 cards (Total Origem · Total Comparado · Diferença líquida · Taxa Conciliação) — qual campo escolher quando há ≥2 campos comparados?
- **BIF-6 · Microcopy de Caso Lógico user-facing** em E5 e Aba 1 §1 · "Mesma aba · em colunas distintas" vs literal técnico
- **BIF-7 · Comportamento do `_tela_erro`** · só mensagem ou também botão "Voltar para E5"?
- **BIF-8 · Cache do Excel por paleta no RESULTADO** · regenera ao trocar paleta · até quando preservar?
- **BIF-9 · Aba 5 (Ponte) em MESMA_ABA_EM_COLUNAS** · mantém ordem fixa 6 abas mesmo quando `ajuste_so_*` é Decimal('0')?
- **BIF-10 · Comportamento de "Salvar como modelo"** quando E4 vazia (sem agrupadores executivos)

## 10 · Materiais lidos com timestamp

Todos lidos em 2026-04-26 antes de iniciar Fase 1:

| # | Arquivo | Status |
|---|---|---|
| 1 | `specs/dcv/DCV_V1.md` | lido integralmente (681 linhas) |
| 2 | `specs/produto/p_v1.md` v1.1 | lido §1-§3 (microcopy + arquitetura · 500 linhas) · §4-§6 amostra |
| 3 | `specs/spec_v1.md` v2.0 (S-V1) | lido integralmente §1-§3 + notas D-210/D-211/D-212/D-213 |
| 4 | `specs/produto/MOCKUP_V1_alpha2.md` | localizado · Mockup §3 (Resumo Executivo 9 seções) |
| 5 | `src/visoes/visao_v1.py` (V-V1) | lido API pública · enums · contratos · `executar_v1` signature · `_etapa_1_leitura` |
| 6 | `bases/casos_esperados.yaml` (entrada V1) | lido · 12 assertions (V1-A01..V1-A12) · config canônica para Excel-de-exemplo |
| 7 | `src/app_v2.py` (canônico estrutural) | lido lin 1-1000 · todas as funções a espelhar |
| 8 | `src/visoes/exportacao_v2.py` (canônico de exportação) | lido lin 1-300 + signature `exportar_resultado_v2` |
| 9 | `src/apresentacao/formatos.py` (capabilities) | lido lin 1-200 · helpers F-APRESENT |
| 10 | `src/apresentacao/templates/familia_a/` | listado · 5 templates (saude · concentracao · onde_se_concentra · variacoes_destaque · leitura_qualitativa · _shared) |
| 11 | `src/contratos.py` (tipos compartilhados) | lido `ArquivoInfo` · `UploadResult` · `MotorResult` · `ConfigExportacao` · `ExportacaoResult` · `BloqueioOperacional` |
| 12 | `specs/vocabulario_bilingue.md` | localizado · Bloco 1 (stepper) · Bloco 1.1 V1 (Origem/Comparado) · Bloco 3 estendido (6 classificações) |

**Checkpoint A · pytest --collect-only:** 979 testes coletados (= baseline). Pronto para Fase 1.
