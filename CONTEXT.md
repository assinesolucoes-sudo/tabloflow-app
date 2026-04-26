# CONTEXT.md — TabloFlow

Documento de referência do projeto. Contém o método, a arquitetura, as fontes de verdade e os princípios invioláveis que regem toda sessão de trabalho.

**Versão:** v3.5 (ALINHA-Lições-Família-A · 26/04/2026)
**Mudanças desde v3.4:** absorção de 6 D-XXX novas (D-202 a D-207). §16 reescrita (substitui escopo D-197 com escopo D-202 detalhado · modalidade Refactor Dirigido D-206). §17 nova (Cláusulas anti-vazamento Fundação→Visão · A+B+C). §18 nova (Princípios consolidados Família A). §15 ganha sub-itens "Mockup Excel-alvo · gate β.3" e "Refactor Dirigido · 5ª modalidade".

**Última atualização:** 26/04/2026 · ALINHA-Lições-Família-A concluída como 6ª aplicação ALINHA · 1ª aplicação completa do ciclo de 6 artefatos sob método novo (V2) consolidada · inventário V2→Fundação produzido (5 críticos + 3 altos · não 1 como D-197 sugeria) · 6 D-XXX novas formalizadas · método ganha Refactor Dirigido (D-206) como 5ª modalidade · Cláusulas anti-vazamento (D-204) como tripla proteção · 4 princípios canônicos (D-207) consolidados para Famílias B/C/D/E.

**Próximo passo:** **Sessão de Promoção de Fundação · 26/04/2026 tarde-noite** (D-202 · Refactor Dirigido · 1 sessão Claude Code grande · 4 salvaguardas) executa os 5 itens críticos + 3 altos do inventário · após validação Camada 2 curta · V1 destrancada → Mockup-V1 (D-203 · modalidade β.3) → P-V1 / S-V1 / V-V1 / A-V1 / VV-V1 → V11 sob método novo → Auditoria pós-V11 (D-204 cláusula B) → Família C abre.

**Suite pytest atual:** 731/731 verdes (preservada ao longo de 4 sub-sessões cirúrgicas V2 + ALINHA-Lições-Família-A · zero regressão · gabarito objetivo de pronto para D-202).

**Lições metodológicas fundamentais consolidadas em D-207 · 4 princípios canônicos:**
1. Excel é o produto · Spec textual não basta (operacionalizada por D-203 · gate D-204 cláusula A)
2. Cada família tem checkpoint estrutural depois da 1ª visão (D-204 cláusula B · ALINHA-Lições-Família-A é a aplicação retroativa para Família A)
3. Decisão estrutural não pode viver só em comentário de código (D-204 cláusula C · cleanup de 86 comentários V2 absorvido em D-202)
4. Refactor ≠ Invenção · método deve diferenciar (D-206 cristaliza Refactor Dirigido como 5ª modalidade)

Histórico recente (ordem cronológica reversa): **ALINHA-Lições-Família-A (26/04/2026 manhã · 6ª aplicação ALINHA · D-202 a D-207)** · V2 retroativa fechada (25/04/2026 noite · D-201 · D-199 · 4 sub-sessões cirúrgicas 8.1-8.4) · Sessão 8.1 (25/04/2026 fim de tarde · 7 fixes pós-Camada 2) · Sessão 8 (25/04/2026 tarde · 5 evoluções V2 · D-194/D-195) · Sessão 7 (25/04/2026 manhã · ALINHA-Descoberta-Unidade · D-191/D-192/D-193) · Sessão 6 (24-25/04/2026 · investigação meta-estrutural · D-189/D-190) · Sessão 5 (24/04/2026 · D-186/D-187) · ALINHA-Retroação-V2 (24/04/2026 · D-184/D-185) · Sessão 4-ter-bis (23/04/2026) · Sessão 4-ter (23/04/2026) · F-APRESENT P1 (23/04/2026 · D-169/D-176) · ALINHA-Descoberta-Camada-Produto (23/04/2026 · D-157 a D-166).

---

## 1. O que é o TabloFlow

O TabloFlow é uma plataforma analítica dividida em dois módulos:

- **Módulo 1 · TabloAnálise** — 11 visões analíticas que leem bases tabulares e entregam leitura estruturada, auditável e exportável em Excel executivo. As visões cobrem confronto entre bases, comparação entre estados, análise sequencial, composição, ranking, desvio, dispersão e cruzamento.
- **Módulo 2 · TabloPrep** — operações de preparação de dados (filtro, deduplicação, normalização, enriquecimento) que alimentam o Módulo 1.

A plataforma atua como **camada intermediária** entre dados tabulares recebidos do usuário e análise estruturada.

### 1.1 · Excel executivo é o produto (D-163)

**O Excel gerado por cada visão é o produto principal do TabloAnálise.** Não é entregável técnico · não é output · não é saída de processamento. Cliente recebe o Excel · apresenta em reunião · decide a partir dele · compartilha com stakeholders. A app Streamlit é **instrumento de configuração e preparação** do Excel, não o produto entregue.

Consequência estrutural: qualidade do Excel é critério primário de sucesso do TabloFlow · não derivado. Se o Excel não encanta · o cliente volta a fazer a análise na mão · e o TabloFlow morre (declaração constitutiva da Usuária em VV-V2 · 23/04/2026).

Esta posição orienta toda camada seguinte: F-APRESENT (§6) é subsistema-produto · P-VN (§15.11) dedica seção inteira à arquitetura do Excel · validação visual (§9 B.4) valida majoritariamente o Excel.

### 1.2 · Três princípios de posicionamento

1. **O sistema não valida a verdade do dado.** Ele processa exatamente o que recebe.
2. **Determinismo absoluto.** Mesma entrada + mesma configuração = mesma saída, sempre.
3. **IA sugere, Usuária confirma, Motor executa.** A IA nunca toma decisão analítica; ela apenas propõe preenchimento de campos. **Receptividade nos contratos da Fundação é declarada no G-FUND (D-130)** · implementação de IA acontece em bloco dedicado pós-Família A validada.

---

## 2. Papéis nesta operação

**Usuária (Elaine)** — produto, estratégia, validação visual final, aprovação de artefatos. Operação solo. Declarou explicitamente zona de decisão em negócio, não desenvolvimento técnico · padrão D-131 de condução aplicado durante a Fase 1 e mantido na Fase 2 para operacionalizar essa distinção.

**Arquiteto (Claude no Projects)** — produção de artefatos técnicos, manutenção de coerência entre documentos, proposição de decisões com trade-offs, condução metodológica. **Você, agora, neste chat.** Na Fase 1 e Fase 2, tem responsabilidade adicional formalizada em D-131 · traduzir decisões técnicas que impactem negócio para linguagem decisional antes de apresentá-las à Usuária.

**Claude Code** — execução de blocos de implementação em sessão dedicada, a partir de prompts produzidos pelo Arquiteto. **Não toma decisão arquitetural** — ambiguidade retorna como pergunta ao Arquiteto.

**ChatGPT** — analista técnico de apoio para rascunhos iniciais (DCVs prévios). Opera sob diretriz da Usuária, com refino posterior obrigatório pelo Arquiteto. **Exceção:** quando o Arquiteto capta melhor um tema específico durante sessão de abertura de escopo, pode produzir um DCV prévio excepcionalmente — como ocorreu com V11 (D-047). Papel reduzido na Fase 1 e Fase 2 (não há DCVs novos · pode ser consultado pontualmente para rascunhos de prompts ou análise de código, sob diretriz da Usuária).

**Gamma** — ferramenta de **formatação de documentos finais apresentáveis** (Blueprint polido, material externo). **Não gera artefato técnico do projeto** — essa responsabilidade é exclusiva do Arquiteto.

---

## 3. O método em 3 fases

A construção do Módulo 1 segue três fases sequenciais. **Nenhuma fase inicia sem a anterior estar completa.** O Módulo 2 reutiliza a mesma estrutura em menor escala.

### Fase 0 · Compreensão

**Objetivo:** capturar, em prosa curta e aprovada pela Usuária, o que cada visão faz, recebe, entrega e quais pendências precisam ser decididas antes da implementação.

**Artefato único:** DCV (Documento de Compreensão da Visão), em `/specs/dcv/dcv_vN.md`.

**Status · CONCLUÍDA (20/04/2026).** 11 de 11 DCVs aprovados: V2 · V1 · V11 · V4 · V10 · V3 · V8 · V7 · V9 · V5 · V6.

### Fase 1 · Fundação

**Objetivo:** consolidar os requisitos de motor, contratos, transversais e exportação que emergem dos 11 DCVs aprovados e implementar a fundação que sustenta **todas** as visões.

**Artefatos originais da Fase 1:**
- Spec consolidada dos motores (`motor_upload`, `motor_base`)
- Spec de contratos de resultado com **receptividade a IA declarada** (D-130/D-144)
- Spec dos componentes transversais (ver § 6)
- Spec da exportação Excel padrão (Resumo Executivo em 6 Blocos · Coração Visual · filtros · formatos)
- Base sintética de fundação única · 14 abas · SEED=42

**Status · CONCLUÍDA (21/04/2026).** 5 de 5 blocos verdes (G-FUND · ALINHA-Fundação-Design→F-MOT · F-MOT · F-TRANS · F-EXP · F-BASE). Suite: 232/232 em 4.89s.

**Extensão pós-ALINHA-Descoberta-Camada-Produto · F-APRESENT (D-159 · D-157) · CONCLUÍDA 23/04/2026:**

**Adição · não reescrita.** A Fase 1 ganha 5º subsistema **F-APRESENT** (camada de apresentação executiva) sem invalidar os 4 subsistemas existentes. F-APRESENT foi executado em 2 blocos Claude Code dedicados (P0 fim da tarde de 23/04/2026 · P1 noite/madrugada de 23/04/2026 · Sessão 3 da fila V2 retroativa). Subsistema completo · 10 capabilities operacionais · consumido transversalmente por 11 visões. Detalhes operacionais em §6.2 · capabilities em §15.12.

### Fase 2 · Visões

**Objetivo:** implementar as 11 visões sobre a fundação aprovada, na ordem lógica por famílias conceituais.

**Para cada visão N, seis artefatos sequenciais (D-158 · reescrita de §15.1):**

1. **P-VN (Spec de Produto)** — paleta executiva · vocabulário bilingue · narrativa do Excel · arquitetura de abas · microcopy de telas · checklist user-facing. **Produzida antes de S-VN** para que vocabulário user-facing molde os contratos técnicos · não o contrário.
2. **S-VN (Spec técnica)** — três seções obrigatórias: contratos lógicos · regras de cálculo · wireframe funcional (textual em prosa · reforçado por HTML na Família A · D-149). Consome P-VN.
3. **B-VN (Base sintética específica)** — condicional ao critério de D-147. Quando dispensado, visão consome `base_fundacao.xlsx`.
4. **V-VN (`visao_vN.py`)** — motor da visão sobre a fundação.
5. **A-VN (`app_vN.py`)** — app Streamlit aplicando P-VN + S-VN · consome `base_vN_cliente.xlsx` como entrada canônica da Validação Visual.
6. **VV-VN · Validação Visual Construtora (VVC)** — Usuária construtora carrega base, marca checklist derivado (D-148) em ✅/❌ · modalidade C mista com Arquiteto presente (D-156). Gate da camada construtora de B.4 (D-162). **Não atesta prontidão para cliente final** · essa é camada VVP, parqueada.

**Ordem oficial de implementação por famílias:**

| Ordem | Família | Visões | Racional |
|---|---|---|---|
| 1 | A · Confronto | **V2 retroativo** (P-V2 ✅ · F-APRESENT P1 ✅) → V1 → V11 | V2 retroativo em curso (P-V2 aprovada 23/04/2026 noite · F-APRESENT P1 concluído noite/madrugada · D-167 · D-168 · D-169) · 3 sessões restantes para fechar (Adendo S-V2 · A-V2 refatorada · VV-V2 nova). V1 estende para duas bases com chave (T-DUAL). V11 trata duas bases sem chave via aderência. Padrão Família A canonizado pela P-V2 retroativo (vocabulário Origem/Comparado · 6 classificações estruturais · Coração Visual · arquitetura 4 abas · stepper 4+Revisão). |
| 2 | C · Composição | V4 → V10 | V4 cobre composição completa incluindo ABC; V10 é especialização Pareto |
| 3 | B · Sequência | V3 → V8 | V3 acompanha valor em eixo ordenado; V8 acompanha presença no mesmo eixo |
| 4 | D · Posição relativa | V7 → V9 | V7 é desvio simples da média do grupo; V9 é ranking multidimensional |
| 5 | E · Estrutura interna do recorte | V5, V6 | V5 univariado numérico; V6 bivariado categórico |

**Nota V2 · MVP técnico (pós-VV-V2) · retroação em curso (D-167):** V2 ficou em `✅✅✅✅⚠️⬜` após VV-V2 de 23/04/2026 manhã. Aplicação do método novo em curso · **ALINHA-Retroação-V2 antecipada** (D-167 · antes de V1/V11). Escopo cirúrgico (5 sessões · estado atualizado pós-Sessão 3):

1. ✅ **P-V2 retroativo** · concluída 23/04/2026 noite · 5 seções canônicas · paleta Azul default · stepper 4+Revisão · tom narrativo descritivo · D-168 nova
2. ▶ **Adendo §2.4 a S-V2** · próxima sessão · contrato de unidade D-166 + notas D-165/D-166 nas seções afetadas · destrava Sessão 4
3. ✅ **F-APRESENT P1** · concluída 23/04/2026 noite/madrugada · sessão combinada Claude Code · 3 capabilities (badges · hierarquia tipográfica · diagnóstico narrativo D-165) · 127 testes novos verdes · D-169 nova (débito técnico 13 testes P0)
4. ⏸ **A-V2 refatorada** · sessão combinada Claude Code · consome P-V2 + S-V2 com adendo + V-V2 intacto (301/301 verdes preservados) + F-APRESENT P0+P1 + separação download/aprovação D-162 · sub-bloco de cleanup dos 13 testes P0 · D-169 vence aqui
5. ⏸ **VV-V2 retroativa** · Usuária opera · Arquiteto presente · modalidade C mista D-156 · gate B.4 camada 1 D-162

Após Sessão 5: 6º quadrado verde · ALINHA-Retroação-V2 fechada · P-V1 abre como 2ª aplicação do método novo.

**Bloco IA-Família-A** (D-130) · após Família A validada sob método novo (V1 e V11 em VVC ✅ + V2 retroagida em ALINHA-Retroação-V2) · adiciona Papel A + Papel B da IA às 3 visões.

**Critério de conclusão da Fase 2:** 11 visões com VVC ✅ (6 quadrados verdes) + ALINHA-Retroação-V2 concluída para V2.

**Condução da Fase 2 · §15.** Processo operacional completo formalizado em §15 · ciclo de 6 artefatos por visão · convenções de P-VN (§15.11) · convenções de F-APRESENT (§15.12) · convenções de S-VN (§15.3) · critério de base (§15.4) · derivação do checklist (§15.7) · wireframe HTML (§15.6) · plano operacional (§15.2). Padrão D-131 permanece vigente sem modificações estruturais.

---

## 4. Famílias conceituais do Módulo 1

As 11 visões se agrupam em 5 famílias conceituais. Essa divisão guia a reutilização de transversais e a ordem de implementação.

- **Família A · Confronto entre universos** — V2 (dois estados de uma base), V1 (duas bases com chave), V11 (duas bases sem chave, por aderência). Família mais rica do Módulo 1 em função do peso do confronto no uso contábil brasileiro. V1 e V11 compartilham T-DUAL mas operam com motores distintos. V11 **não** é view especializada de V1.
- **Família B · Sequência ao longo de eixo ordenado** — V3 (valor no tempo), V8 (presença no tempo). Visões autônomas unidas por consumo de T-EIXO. V8 não consome T-SEMA (D-071). DCV-V8 cumpre retroação diferida D-060.
- **Família C · Composição e participação** — V4 (participação, ABC, multi-métrica), V10 (Pareto puro). V10 é view especializada sobre V4 Modo 2 com preset Pareto 80/95 (D-035).
- **Família D · Posição relativa** — V7 (desvio da média do grupo), V9 (ranking multidimensional). Ambas consomem T-SEMA/T-AGRUPA/T-RANK com adaptações D-073. **Não há view especializada entre elas.** DCV-V9 §2.3 cumpre retroação D-081 (D-091). **Família D fechada em Fase 0.**
- **Família E · Estrutura interna do recorte** — V5 (dispersão e outliers · univariado numérico), V6 (cruzamento · bivariado categórico). Par operacionalmente distante · sem transversais centrais comuns. **Família E fechada em Fase 0.**

---

## 5. Fontes de verdade

Hierarquia autoritativa dos documentos do projeto:

| Fonte | Papel | Autoridade |
|---|---|---|
| **Blueprint (Gamma)** | Referência estratégica completa das visões, mantida pela Usuária | Intenção |
| **CONTEXT.md** (este) | Método, arquitetura, princípios invioláveis | Regra permanente |
| **DECISIONS.md** | Log cronológico de decisões com rationale | Histórico e porquê |
| **TabloFlow_Estado_do_Projeto.xlsx** | Estado vivo · 5 abas com papéis explícitos · aba 1 Onde estou no todo (Horizontes Futuros · D-150) · aba 2 Painel da fase ativa (dashboard da Fase 2 · **6 quadrados por visão** · D-158) · aba 3 Detalhe técnico · abas 4-5 arquivo Fases 0-1 | Estado atual |
| **DCVs em `/specs/dcv/`** | Compreensão validada de cada visão | Requisito (o quê) |
| **P-VNs em `/specs/produto/`** | **Spec de Produto** por visão (D-158) · paleta · vocabulário · narrativa Excel · arquitetura de abas · microcopy · checklist user-facing | Implementação (o como · camada de produto) |
| **Specs (S-VN) em `/specs/`** | Contratos técnicos + regras + wireframe funcional | Implementação (o como · camada técnica) |
| **Wireframes visuais em `/specs/wireframe_vN.html`** | Representação visual do wireframe funcional (D-149 · obrigatório Família A) | Apoio à aprovação |
| **`/specs/vocabulario_bilingue.md`** | **Tabela canônica transversal** técnico ↔ user-facing (D-160) · consumido por toda P-VN · aplicado por F-APRESENT | Regra permanente |
| **`/bases/base_fundacao.xlsx`** | Dataset sintético único da Fundação · 14 abas SEED=42 (D-140) | Estado atual |
| **`/bases/casos_esperados.yaml`** | Gabarito canônico de validação · 61 assertions (D-141) | Regra permanente |
| **`/bases/base_vN_cliente.xlsx`** | Recorte cliente-friendly (D-149) · entrada canônica de VVC | Apoio à VVC |
| **GLOSSARIO.md** | Vocabulário canônico do projeto | Terminologia |

**Regras de conflito:**

- Se CONTEXT e planilha divergirem sobre regra permanente → CONTEXT prevalece.
- Se CONTEXT e planilha divergirem sobre estado atual → planilha prevalece.
- Se Blueprint e spec local divergirem → spec prevalece para execução; Blueprint prevalece para intenção.
- Se DCV e spec divergirem → DCV prevalece.
- Se P-VN e S-VN divergirem sobre vocabulário/microcopy/arquitetura de abas → P-VN prevalece (camada de produto é fonte).
- Se P-VN e S-VN divergirem sobre contrato lógico/regra de cálculo → S-VN prevalece (camada técnica é fonte).
- Se spec e código divergirem → investigar antes de assumir prevalência.
- Se `base_fundacao.xlsx` e `base_vN_cliente.xlsx` divergirem → base mestre prevalece · regenerar.
- Se `/specs/vocabulario_bilingue.md` e P-VN divergirem → vocabulário transversal prevalece · P-VN ajusta ou justifica extensão em seção própria.

---

## 6. Componentes transversais da Fundação

Durante a leitura consolidada dos DCVs emergiram componentes compartilhados. Todos estão **implementados e testados em F-TRANS**. A Fundação ganha ainda, a partir de ALINHA-Descoberta-Camada-Produto, um **5º subsistema · F-APRESENT** (D-159).

### 6.1 · Transversais analíticos (T-*)

| Sigla | Nome | Usado por |
|---|---|---|
| **T-AGRUPA** | Consolidação por agrupadores antes do cálculo · padrão CPCO · C.D1 | TODAS exceto V1/V11 |
| **T-DIAG** | Diagnóstico estrutural · **última aba** (D-017) · serialização JSON-compatível para IA (D-130) | TODAS |
| **T-SEMA** | Semântica maior-é-melhor / menor-é-melhor / neutro | V2, V3, V7, V9 |
| **T-EIXO** | Eixo sequencial ordenado · 3 tipos canônicos (temporal · lógico/ordinal · manual) | V3, V8 |
| **T-RANK** | Ranking determinístico com regra de desempate | V1, V4, V7, V9, V10, V11, V6 |
| **T-ACUM** | Acumulado progressivo monotônico | V4, V10 |
| **T-ABC** | Classificação A/B/C por limiares de acumulado | V4, V10 |
| **T-PIVOT** | Pivot POR_LINHAS → POR_COLUNAS · 3 semânticas | V2, V3, V4 |
| **T-DUAL** | Upload dual (2 arquivos OU 1 arquivo com 2 abas) | V1, V11 |
| **T-MODELO** | Salvar e aplicar configuração como modelo · persistência de TED (C.D2) | TODAS |
| **T-FUZZY** | Similaridade textual entre strings | V11 (MVP) · V1 (roadmap) |
| **T-CONCAT** | Composição de campos textuais (D-135) | V11 (MVP) · M2.CONCAT futuro |

12 transversais implementados em `/src/transversais/` · 127 testes verdes em F-TRANS.

### 6.2 · F-APRESENT · Subsistema de apresentação executiva (D-159 · P0+P1+capability 11 · 11 capabilities canônicas · 24/04/2026)

5º subsistema da Fundação · adição · implementado em 2 blocos Claude Code dedicados (P0 fim da tarde · P1 noite/madrugada). Código em `/src/apresentacao/`. Capabilities transversais consumidas por todas as 11 visões via P-VN + S-VN + A-VN.

**Status atual:**
- **P0 · CONCLUÍDO (23/04/2026 fim da tarde)** · 7 capabilities P0 implementadas · 179 testes novos verdes · 4 amostras visuais aprovadas pela Usuária · 3 rodadas de correção visual emergentes absorvidas (larguras de coluna Resumo Executivo · contraste de cabeçalho de tabela · `Table.autoFilter` forçado ativo por default)
- **P1 · CONCLUÍDO (23/04/2026 noite/madrugada · Sessão 3 V2 retroativa)** · 3 capabilities P1 implementadas · 127 testes novos verdes (36 badges + 40 tipografia + 51 diagnóstico) · 0 regressão nos testes herdados · `aplicar_hierarquia_tipografica(ws, paleta)` mantido como wrapper canônico no-op (helpers individuais cobrem 100% dos casos atuais · interface D-159 preservada para evolução futura)

**10 capabilities canônicas (subsistema completo):**

| # | Capability | Prioridade | Status | Arquivo |
|---|---|---|---|---|
| 1 | Catálogo de 4 paletas executivas (D-164 · Azul · Verde · Cinza · Vinho · default universal Azul · D-168) | P0 | ✅ | `/src/apresentacao/paletas.py` |
| 2 | Rótulos user-facing universais (consome `/specs/vocabulario_bilingue.md` v2 · D-160) | P0 | ✅ | `/src/apresentacao/vocabulario.py` |
| 3 | Tabela Excel nativa com linha de totais dinâmicos (ListObject · D-166) | P0 | ✅ | `/src/apresentacao/tabela_executiva.py` |
| 4 | Formatação monetária BR (D-166) | P0 | ✅ | `/src/apresentacao/formatacao_monetaria.py` |
| 5 | Formatação percentual (D-166 · conversão fração→% na exportação) | P0 | ✅ | `/src/apresentacao/formatacao_percentual.py` |
| 6 | Colunas adaptativas ao cenário (D-166 · montagem dinâmica) | P0 | ✅ | `/src/apresentacao/colunas_adaptativas.py` |
| 7 | Resumo Executivo narrativo em 6 blocos (renderiza ResumoExecutivo em prosa · não JSON) | P0 | ✅ | `/src/apresentacao/resumo_executivo.py` |
| 8 | Badges semânticos (`BadgeStyle` frozen + catálogo 4×4 paleta×semântica + mapeamento por visão injetável) | P1 | ✅ | `/src/apresentacao/badges.py` |
| 9 | Hierarquia tipográfica (4 helpers: `aplicar_titulo_aba` · `aplicar_secao` · `aplicar_campo` · `aplicar_valor` + `escrever_*` wrappers + wrapper canônico no-op reservado) | P1 | ✅ | `/src/apresentacao/tipografia.py` |
| 10 | Diagnóstico narrativo em 6 seções fixas user-facing (D-165 · `formatar_valor_ou_traco` para `None` · `_normalizar_categoria` para Enum/string · genérica para qualquer visão) | P1 | ✅ | `/src/apresentacao/diagnostico_narrativo.py` |

Detalhamento técnico em §15.12. **Suite atual: 594/607 verdes** (467 baseline preservado + 127 novos da Sessão 3 P1). 13 testes em vermelho em `test_apresentacao.py` (P0) · pré-existentes desde drift `vocabulario_bilingue.md` v1→v2 · **D-169 · débito técnico formalizado** · vencimento na Sessão 4 ou sessão dedicada antes.

**Refinamento técnico conhecido absorvido em P0 (não vira D-XXX):** Table nativa openpyxl exige `Table.autoFilter = AutoFilter(ref=...)` explícito para Excel exibir botões de filtro ▼ por default · `autoFilter.ref` cobre header + dados **excluindo** linha de totais. `TableColumn.showFilterButton` não existe em openpyxl 3.1.5 · candidato a refactor em versões ≥ 3.2. Coberto pelo teste de regressão `test_amostras_filtro_ativo_em_todas_as_colunas`.

**Refinamento técnico conhecido absorvido em P1 (não vira D-XXX):** Badges (`PatternFill`) aplicados DENTRO de `openpyxl.Table` não quebram `autoFilter` · confirmado por teste de regressão `test_badge_dentro_de_table_nao_quebra_autofilter`. Categoria de warning em renderização aceita Enum OU string (`_normalizar_categoria`) · resiliente à diferença entre Pydantic com `use_enum_values=False` e dicts construídos manualmente em testes/upstream.

**Recomendação arquitetural para A-V2 refatorada (Sessão 4) e A-VN futuras:** Capability 10 (Diagnóstico narrativo) espera 12 campos canônicos achatados em `config_usada` (campos declarados em §15.12). 7 desses campos não estão hoje em `config_usada` do `V2Result` · estão dispersos em `comparacao_realizada` · `agrupadores_aplicados` · upstream (motor/app) · ou são derivados. Capability 10 segue genérica e trata ausência como `—` via `formatar_valor_ou_traco(None, "ausencia")` · "— (não consta)". **Cada A-VN deve criar função `_extrair_config_para_diagnostico(vN_result) -> dict`** que monta o dict canônico achatado a partir dos múltiplos campos do `VNResult`. Sem mudança em V2Result · sem mudança em motor.

**Capability 11 · Gráficos executivos + nomenclatura de arquivo** (D-176 · NOVO · 24/04/2026):
- `/src/apresentacao/graficos.py`: `criar_grafico_distribuicao()` (PieChart) · `criar_grafico_top_variacoes()` (BarChart horizontal por sinal · verde/vermelho/cinza)
- `/src/apresentacao/nomenclatura.py`: `nomear_excel_executivo()` (padrão: `{Família} - {Contexto} - {DD-MM-AAAA}.xlsx`)
- Default cross-visão: BarChart horizontal para top variações; PieChart para distribuição categórica somente quando categoria principal < 60%
- Refinamento pendente em sessão F-APRESENT-cleanup (D-180): parâmetro `unidade_valor` em `criar_grafico_top_variacoes` para aplicar `number_format` correspondente ao eixo

**Princípio operacional cross-visão (D-175 · P-UNIF · NOVO · referenciado em §13.8):** toda visão consome F-APRESENT · `exportacao_vN.py` consome capabilities · zero formatação direta com openpyxl · zero hardcode de cor/string/formato. Bespoke transitório permitido apenas com comentário `# TODO-FAPRESENT-CLEANUP: <descrição>` consumido por sessão F-APRESENT-cleanup periódica.

### 6.3 · Requisitos consolidados da Fundação existente

1. **motor_base com `column_meta.tipo_estrutural`** (5 valores enum · D-113/D-133/D-146)
2. **exportacao.py com formatação condicional + ColumnChart empilhado 100% + paginação** (D-118)
3. **exportacao.py com aba "Combinações Ausentes" V6** (D-119)
4. **Receptividade a IA (D-130 · refinado em D-144)** — 3 requisitos para Results analíticos · 2 requisitos para Results operacionais

---

## 7. Tipos de bloco de execução

Um bloco é uma sessão de trabalho dedicada a um artefato específico. **Nunca misturar tipos diferentes na mesma sessão.**

| Prefixo | Significado | Fase |
|---|---|---|
| `DCV-VN` | Refino de DCV pelo Arquiteto | Fase 0 |
| `DCV-OPN` | DCV equivalente para operação N do Módulo 2 | Fase 0 (M2) |
| `G-FUND` | Gate de Fundação | Fase 1 |
| `ALINHA-<Marco>→<próximo>` | Sessão dedicada ao fechar Marco (D-142) · 4 sub-blocos α·β·γ·δ | Transversal |
| `F-MOT` · `F-TRANS` · `F-EXP` · `F-BASE` | Implementação da Fundação original · CONCLUÍDOS | Fase 1 |
| **`F-APRESENT`** 🆕 | **Implementação do subsistema de apresentação executiva** (D-159) | Fase 1 (extensão) |
| `IA-Família-A` | Implementação de Papel A + B da IA em V2/V1/V11 pós-validação | Pós-Família A |
| `IA-Meta` | Implementação de Papel C da IA (recomendação de visão) | Pós-Família C validada |
| **`P-VN`** 🆕 | **Spec de Produto por visão** (D-158) | Fase 2 |
| `S-VN` | Spec técnica da visão N | Fase 2 |
| `B-VN` | Base específica (condicional D-147) | Fase 2 |
| `V-VN` | `visao_vN.py` · sessão combinada (D-155) | Fase 2 |
| `A-VN` | `app_vN.py` · sessão combinada (D-155) | Fase 2 |
| `VV-VN` | **Validação Visual Construtora (VVC)** · modalidade C mista (D-156 · opera em VVC · D-162) | Fase 2 |

**Horizontes futuros declarados:**
- `ALINHA-Retroação-V2` · Marco · aplica método novo em V2 · ativa após V1 e V11 validadas em VVC
- Sessão futura `Definição operacional VVP` · protocolo VVP · ativa quando Família A completa
- `VVP · Validação Visual de Produto` · cliente real · horizonte parqueado pós-Família A (D-162)

**Blocos descontinuados:** `B-NR` · `V-Nb` · `N-Motores` · `G-MOT` · `N-VN` · `V-0c` · `T-XXX` · "onda padrão" · "Validação Visual solo" (substituída por VV-VN em D-156).

---

## 8. Estrutura de pastas

```
/tabloflow/
├── CONTEXT.md                          ← este arquivo
├── DECISIONS.md                        ← log cronológico de decisões
├── GLOSSARIO.md                        ← vocabulário canônico
├── Instrucoes_do_Projeto.md            ← como operar o projeto
├── TabloFlow_Estado_do_Projeto.xlsx    ← estado vivo · 5 abas · aba 2 com 6 quadrados por visão
│
├── /specs/
│   ├── vocabulario_bilingue.md         ← tabela canônica transversal técnico ↔ user-facing (D-160) · NOVO
│   ├── /dcv/                           ← DCVs aprovados (Fase 0)
│   │   ├── dcv_v1.md ... dcv_v11.md
│   │   └── MODELO_DCV_PREVIO.md
│   ├── /produto/                       ← NOVO · Specs de Produto (D-158)
│   │   └── p_v1.md ... p_v11.md        ← produzidos na Fase 2
│   ├── spec_fundacao.md                ← spec consolidada da Fundação (Fase 1)
│   ├── spec_v1.md ... spec_v11.md      ← specs técnicas das visões (Fase 2)
│   └── wireframe_v1.html ... wireframe_v11.html  ← D-149
│
├── /src/
│   ├── motor_upload.py                 ← Fundação
│   ├── motor_base.py                   ← Fundação
│   ├── contratos.py                    ← Fundação (D-130/D-144)
│   ├── exportacao.py                   ← Fundação
│   ├── /transversais/                  ← 12 T-* implementados (F-TRANS)
│   ├── /apresentacao/                  ← F-APRESENT (D-159) · 10 capabilities · P0+P1 ✅ subsistema completo
│   ├── /utils/                         ← normalizacao_texto.py · reconhecedor_cronologico.py
│   ├── /geradores/                     ← gerar_base_fundacao.py · gerar_base_cliente.py (D-149)
│   ├── visao_v1.py ... visao_v11.py    ← Fase 2
│   ├── app_v1.py ... app_v11.py        ← Fase 2
│   └── testes/                         ← 594/607 verdes (13 vermelhos pré-existentes · D-169)
│
├── /bases/
│   ├── base_fundacao.xlsx              ← dataset único · 14 abas · SEED=42 (D-140)
│   ├── casos_esperados.yaml            ← gabarito · 61 assertions (D-141)
│   └── base_v1_cliente.xlsx ... base_v11_cliente.xlsx  ← D-149
│
├── /legacy/                            ← artefatos pré-D-014
├── /files/                             ← material de produto (Blueprint)
└── /.claude/, /.vscode/                ← configuração
```

---

## 9. Princípios invioláveis

Dez princípios invioláveis organizados em três camadas, estendidos por **7 princípios derivados formalizados em 20-24/04/2026** que operacionalizam a Camada C. Rationale e histórico preservados em DECISIONS.md.

### Camada A · Princípios de método

**A.1 — Três fases sequenciais, sem sobreposição.**
Fase 0 → Fase 1 → Fase 2. Nenhuma fase inicia sem a anterior estar 100% concluída. Tentar antecipar produz retrabalho, não velocidade.

**A.2 — Toda visão começa com DCV aprovado.**
Sem DCV aprovado, nenhuma P-VN, S-VN, base ou código pode ser escrito.

**A.3 — Arquiteto é o único gerador de artefato técnico.**
P-VNs, Specs, bases sintéticas, prompts de bloco e refino de DCVs são produzidos pelo Arquiteto. ChatGPT apoia no rascunho de DCV prévio. Gamma é ferramenta de formatação final, nunca gerador de contrato técnico.

### Camada B · Princípios de artefato

**B.1 — Um bloco por sessão.**
Cada sessão (Claude Code, Arquiteto, ChatGPT) executa exatamente um tipo de bloco.

**B.2 — P-VN e S-VN têm seções obrigatórias.**
P-VN tem 5 seções (D-158): (1) Paleta executiva · (2) Vocabulário bilingue · (3) Arquitetura de abas do Excel · (4) Microcopy de telas · (5) Checklist user-facing. S-VN tem 3 seções: (a) contratos lógicos · (b) regras de cálculo · (c) wireframe funcional (reforçado por HTML na Família A · D-149). Dupla aprovação agora é **tripla**: P-VN + S-VN + wireframe HTML.

**B.3 — Base sintética exige volume realista.**
Mínimo 50 linhas por aba, com aba CASOS_ESPERADOS auditada. Critério D-147 decide B-VN vs. consumo direto.

**B.4 — Nenhum artefato é concluído sem Validação Visual (desdobrado em 2 camadas · D-162).**

**Camada 1 · VVC · Validação Visual Construtora** (escopo ativo · Família A):
- Quem opera: Usuária construtora (Elaine)
- Base: `base_vN_cliente.xlsx` (sintética · D-149)
- Vocabulário permitido: técnico OU user-facing (construtora entende ambos)
- Checklist: técnico · derivação mecânica de `casos_esperados.yaml` via 5 templates (D-148)
- Modalidade: C mista com Arquiteto presente (D-156)
- Gate: visão construtoramente validada · 6º quadrado ✅ · desbloqueia próxima visão
- **Não atesta prontidão para cliente final**

**Critérios de aprovação VVC (D-162):**
1. Checklist técnico derivado · todos os itens ✅
2. Excel baixado e inspecionado visualmente · 3 pontos de conferência (Coração Visual nomeado · 6 blocos do Resumo Executivo em prosa user-facing · Diagnóstico fundido em 6 seções)
3. Paleta executiva efetivamente aplicada ao Excel
4. **Gate desacoplado** · download de Excel disponível antes de checklist ✅ (Usuária precisa ver o produto para validar · elimina falso acoplamento entre "avançar" e "aprovar")
5. Registro: planilha aba 2 · 6º quadrado ✅

**Camada 2 · VVP · Validação Visual de Produto** (horizonte parqueado · pós-Família A):
- Quem opera: cliente final real · não Usuária construtora
- Base: bases reais de cliente
- Vocabulário permitido: **exclusivamente user-facing**
- Checklist: user-facing · derivado da tabela de vocabulário bilingue (D-160)
- Ativação: após Família A completa em VVC (V2 pós-retroação + V1 + V11)
- Gate: produto validado para go-to-market · bloqueia lançamento se falhar

**Critérios de aprovação VVP (D-162 · declarados para anti-esquecimento · C.2):**
1. Checklist user-facing · todos os itens ✅ (por amostra de cliente)
2. Base real de cliente · não sintética · mínimo 1 por vertical-alvo
3. Cliente real opera sem assistência técnica
4. Excel aberto por executivo sem contexto prévio (teste de clareza standalone)
5. 3 vertical-alvos testados · amostra mínima para declarar produto validado
6. Registro: planilha aba 1 · Zona 3 · linha VVP

**Critérios de ativação de ALINHA-Retroação-V2 (originais D-162 · superados por D-167):**
- *Originais (D-162):* V1 aprovada em VVC · V11 aprovada em VVC · Família A completa sob método novo (6/6 quadrados verdes em V1 e V11)
- *Revisados (D-167 · 23/04/2026):* **Antecipação formal** · ALINHA-Retroação-V2 é a primeira aplicação do ciclo de 6 artefatos · precede V1 e V11 · justificativa: toda descoberta de ALINHA-Descoberta-Camada-Produto nasceu sobre V2 · aplicar método novo nela fecha a dívida técnica mais nítida do projeto · calibração inicial em visão de complexidade analítica menor (comparação entre estados) antes de V1 (conciliação com chave).
- Usuária pode declarar adiamento via D-XXX (anti-esquecimento silencioso · C.2) mas não pular sem decisão formal.

### Camada C · Princípios de operação

**C.1 — Determinismo absoluto nos motores.**

**C.2 — Nada silencioso.**
Todo ajuste estrutural visível no diagnóstico. Nenhuma transformação invisível. Compromissos declarados não podem desaparecer (VVP parqueada mas com critérios declarados).

**C.3 — Sem invenção de comportamento.**
Ambiguidade vira pendência P-NN ou D-XXX.

**C.4 — Decisão estrutural vira D-XXX.**

**C.5 — TabloFlow analisa sobre o dado informado, nunca decide por ele.**
Quando houver ambiguidade entre "o sistema decide X" e "o sistema apresenta o caso para o usuário ver", escolha correta é sempre a segunda.

### Camada C · Princípios derivados formalizados (20-23/04/2026)

**C.D1 · CPCO — Consolidação Pré-Cálculo Obrigatória** (D-122)
Modo da base declarado · T-AGRUPA invocada obrigatoriamente. 9 das 11 visões.

**C.D2 · TED — Thresholds Editáveis Declarados** (D-123 · refinado por D-153/D-160/D-161)
Defaults declarados visíveis · editáveis em sidebar global (D-153) · labels consumindo vocabulário bilingue (D-160) · defaults aplicando C.D6 (D-161) quando motor tem evidência. Todas as 11 visões.

**C.D3 · BAD — Base Analítica e Diagnóstico** (D-124 · refinado por D-165)
Base Analítica (1 linha por unidade consolidada) + Diagnóstico (sempre última aba · D-017 · 6 seções user-facing após fusão de Parâmetros · D-165). Sem aba "Dados Brutos". Todas as 11 visões.

**C.D4 · MBO — Matriz de Bloqueios Operacionais** (D-127 · D-134)
Bloqueios declarados com 5 campos (condição · comportamento · escapável · microcopy · warning). `BloqueioOperacional` contrato único. Todas as 11 visões.

**C.D5 · ECP — Escala de Cardinalidade com Patamares** (D-128)
Escala em 3+ eixos · patamares P1 normal · P2 alerta leve · P3 alerta forte · P4 bloqueio escapável. Todas as 11 visões.

**C.D6 · DDU — Default Declarado Universal** (D-161 · NOVO · 23/04/2026)

*Enunciado:* Toda vez que o motor tem evidência para sugerir preenchimento de seletor ou configuração, DEVE aplicar default declarado com a evidência visível ao usuário e opção fácil de alterar. A decisão nunca é silenciosa · o usuário vê o default, vê por que foi sugerido, pode sobrescrever em um clique.

*Deriva de:* C.2 + C.5.
*Escopo:* Todas as 11 visões. Qualquer seletor configurável no app.
*Promoção:* D-024 era padrão consolidado cristalizado em V2 · elevado a universal em D-161.
*5 pontos de aplicação obrigatória identificados:* rótulos user-friendly · checkbox base pré-agregada · modo da base · agrupadores candidatos · TED.

**C.D7 · Motor primeiro, apresentação depois** (D-183 · NOVO · 24/04/2026)

*Enunciado:* Validação empírica de corretude do motor analítico precede validação empírica de apresentação. Em qualquer visão, a primeira sessão de validação (VV-VN camada 2) que a Usuária executa deve incluir inspeção explícita dos valores calculados e das classificações semânticas antes da inspeção estética do produto. Excel formatado corretamente com número errado é pior que Excel mal formatado com número certo · porque o primeiro passa despercebido e propaga erro silenciosamente (violação retroativa de C.2).

*Deriva de:* C.1 + C.2 + C.5.
*Escopo:* Todas as 11 visões. Toda VV-VN camada 2. Toda V-VN (testes do motor).
*Promoção:* Princípio empírico aprendido na descoberta de P-23 (semântica T-SEMA invertida no motor V2 · 24/04/2026 · 301 testes do motor não pegaram cenário MENOR_MELHOR).

*4 regras operacionais derivadas:*
1. **VV-VN camada 2** inspeciona Matriz de Confronto / Coração Visual com sanity check numérico ANTES de Resumo Executivo / Diagnóstico
2. **A-VN antes do gate duplo** produz amostra com tabela de sanity check do motor · 10 combinações com `classificacao_semantica` declarada explicitamente
3. **V-VN testes do motor** cobrem matriz cartesiana T-SEMA completa (12 casos mínimos: 3 valores de `semantica_campo` × 4 valores de `classificacao_estrutural`)
4. **F-APRESENT capabilities** incluem fixture com caso `MENOR_MELHOR` · não apenas `MAIOR_MELHOR`

**C.D8 · Unidade declarada universal** (D-190 · NOVO · 25/04/2026)

*Enunciado:* Toda comparação numérica em qualquer visão TabloFlow declara explicitamente a unidade do campo analisado · F-APRESENT consulta unidade para escolher formato e rótulos · zero hardcode de unidade em camada de apresentação · zero inferência implícita de unidade por `tipo_campo`.

*Deriva de:* C.1 + C.2 + C.5 + C.D6 (DDU).
*Escopo:* Todas as 11 visões · qualquer ponto de apresentação numérica (Excel · tela do app · narrativas).
*Promoção:* Princípio empírico aprendido no achado-mãe da Família A (Sessão 6 · 25/04/2026) · F-APRESENT formatava tudo como monetário hardcoded · ignorando `tipo_campo` · resultando em "R$ 0,21" em campo percentual.

*Implementação obrigatória em V2 (Sessão 8 + 8.1) e cascata para V1/V11/restantes:*
1. **Contrato declara unidade explícita** · campo `unidade` em ComparacaoV2 (V2) · candidato a campo genérico em contrato de Fundação pós-D-197 (V1/V11/restantes)
2. **8 valores canônicos da unidade:** MONETARIO_BRL · PERCENTUAL · QUANTIDADE · TEMPO_DIAS · TEMPO_HORAS · MULTIPLICADOR · RAZAO · ADIMENSIONAL (catalogados em vocabulario_bilingue Bloco 10)
3. **Default declarado** (C.D6) · inferido de `tipo_campo` · MONETARIO_BRL para NUMERICO_ADITIVO/NAO_ADITIVO · PERCENTUAL para NUMERICO_RELATIVO · ADIMENSIONAL para ESTADO_SITUACAO · Usuária pode trocar com 1 clique
4. **F-APRESENT consulta unidade** via helpers de despacho em `src/apresentacao/formatos.py` (`number_format_valor` · `number_format_diferenca` · `number_format_variacao` · `rotulo_diferenca` · `rotulo_variacao` · `label_total_card` · `valor_total_card` · `valor_diferenca_para_celula` · `formatar_valor_por_unidade`)
5. **Tela do app consome os mesmos helpers** que o Excel · zero código de formatação duplicado entre app e Excel (D-198 · reforço)

*Débito atual (D-197):* implementação V2 é V2-específica · helpers existem em F-APRESENT mas pontos de consumo são bespoke · sessão de Promoção de Fundação (pós-ALINHA-Lições-Família-A) deve promover capability genérica.

### Camada C · Derivados informais

**Padrão "herança adaptada à natureza analítica"** (cristalizado em V8 · D-073 · ~15 aplicações documentadas): visões da mesma família conceitual não herdam padrões cegamente; herdam o que cabe à natureza analítica.

**Padrão "o que é warning em uma visão pode ser conteúdo em outra"** (D-076 · 4 aplicações).

---

## 10. Ritual de abertura de sessão do Arquiteto

Toda conversa nova começa com esta sequência:

1. Ler `CONTEXT.md` (este), `DECISIONS.md`, planilha de estado (5 abas), `GLOSSARIO.md` e (quando aplicável) `/specs/vocabulario_bilingue.md`.
2. Ler o artefato principal da sessão se anexado (DCV · P-VN · S-VN · base · prompt).
3. Validar coerência entre fontes — sinalizar qualquer conflito.
4. Confirmar próximo passo operacional da planilha (aba 1) antes de agir.

Na **Fase 1 e Fase 2** o ritual ganha elemento adicional derivado do princípio 3 de D-131 (sinalização proativa de densidade técnica): ao final do ritual, o Arquiteto declara explicitamente o conteúdo decisional esperado da sessão em **4 categorias** (D-156 adicionou a 4ª):
- W decisões de negócio esperadas (Usuária decide · Arquiteto traduz)
- X decisões técnicas puras (Arquiteto resolve · sinaliza que resolveu)
- Y execuções de código supervisionadas (Arquiteto valida output do Claude Code)
- Z validação de produto (Usuária opera app em VV-VN · Arquiteto NÃO decide ✅/❌)

A Usuária pode acionar esta sequência a qualquer momento dizendo **"valide o estado"**.

---

## 11. Ritual de encerramento de sessão

Quando uma conversa gera decisão, artefato ou mudança de estado, o Arquiteto entrega proativamente o **kit de encerramento** (D-020 · D-033). Em fechamento de **Marco**, o kit vira sub-bloco δ de uma sessão ALINHA (§11.1 · D-142).

**Itens produzidos pelo Arquiteto como arquivo completo para download:**

1. **`CONTEXT.md`** · arquivo completo quando há mudança de método/estrutura.
2. **`Instrucoes_do_Projeto.md`** · arquivo completo quando há mudança em condução.
3. **Artefato(s) produzido(s) na sessão** (DCV · P-VN · S-VN · base · prompt · wireframe HTML · vocabulário bilingue).
4. **`GLOSSARIO.md`** · arquivo completo em mudanças significativas (5+ termos · reformulação · 8+ warnings).
5. **`TabloFlow_Estado_do_Projeto.xlsx`** · arquivo completo em mudança estrutural (precedentes D-150 · ALINHA-Descoberta-Camada-Produto que transitou de 5 para 6 quadrados).
6. **Prompt de abertura da próxima conversa** · inline · em Marcos pode ser dual (modo operacional seguinte + retrospectiva futura).

**Itens instruídos pelo Arquiteto, aplicados pela Usuária:**

7. **`DECISIONS.md`** · entradas D-XXX em texto pronto para colar + alterações de status.
8. **`TabloFlow_Estado_do_Projeto.xlsx` · edições rotineiras** · instruções de edição por aba/linha/célula.

**Ordem de aplicação:** (1) baixar categoria 1 · (2) substituir no painel · (3) aplicar D-XXX · (4) aplicar edições rotineiras · (5) abrir próxima conversa.

**Kit leve vs kit pesado (D-170 · FECHADA na ALINHA-Retroação-V2 · 24/04/2026):**

A escolha do kit segue 3 critérios:
1. Sessão encerra Marco? → kit pesado (ALINHA · sub-bloco δ · D-142)
2. Sessão é intermediária dentro de fila declarada? → kit leve (apenas artefatos da sessão + D-XXX para DECISIONS + edições rotineiras de planilha)
3. Sessão é única e autossuficiente? → kit completo (padrão D-033 original)

Em kit leve, D-XXX são provisionadas em DECISIONS.md desde a sessão (não silenciosas · C.2 preservado) mas CONTEXT/Instruções/GLOSSARIO/vocabulario_bilingue só absorvem no kit pesado seguinte.

**Gate duplo de A-VN (D-174 · NOVO · 24/04/2026):**

Toda A-VN encerra com gate duplo obrigatório (camada mecânica Claude Code + camada visual Usuária). Detalhes operacionais em §15.9.

### 11.1 · Padrão ALINHA · sessão dedicada ao fechar Marco (D-142)

Envelopa o kit D-033 como sub-bloco δ. Ativa-se quando 3 critérios são cumpridos: (a) encerra fase/subsistema · (b) transição para modo operacional diferente · (c) ≥ 3 pendências acumuladas.

**Escopo canônico · 4 sub-blocos sequenciais α · β · γ · δ:**

- **α · Consolidação retrospectiva**
- **β · Talk-through operacional**
- **γ · Formalização de decisões técnicas latentes** (produção de entradas D-XXX)
- **δ · Kit de encerramento D-033** (aplicação integral)

Ordem: α primeiro · δ último · β e γ intercambiáveis.

**Aplicações históricas:**
- **1ª · Sessão Fase 0 → Fase 1** (retroativamente categorizada) · produziu D-130/D-131/D-132
- **2ª · `ALINHA-Fundação-Design→F-MOT`** (21/04/2026) · produziu spec_fundacao consolidada + D-142
- **3ª · `ALINHA-Fase-1→Fase-2`** (21/04/2026) · produziu §15 novo + D-147/D-148/D-149/D-150
- **4ª · `ALINHA-Descoberta-Camada-Produto`** (23/04/2026 · esta · 1ª emergente) · produziu D-157 a D-166 + 4 revisões · `vocabulario_bilingue.md` v1 · reescrita da Fase 2 para 6 artefatos · F-APRESENT na Fundação

**Marcos futuros identificados:**
- `ALINHA-Retroação-V2` (após V1/V11 validadas sob método novo)
- `ALINHA-Família-A→IA-Família-A` (após V2 retroagida)
- Sessão futura "Definição operacional VVP" (protocolo · pós-Família A)
- `ALINHA-M1→M2` (fim do Módulo 1)

---

## 12. Como usar o Arquiteto

- **Validar DCV prévio** — Fase 0 concluída · retorna em DCV-OPN do Módulo 2.
- **Gerar P-VN** — peça "P-V[N]"; retorno é Spec de Produto aplicando §15.11 · consome DCV aprovado + tabela canônica transversal.
- **Gerar S-VN** — peça "spec da V[N]"; retorno é Spec técnica aplicando §15.3 · consome DCV + P-VN + spec_fundacao.
- **Gerar base específica** — peça "base da V[N]"; retorno é B-VN se D-147 exigir · senão regenera `base_vN_cliente.xlsx`.
- **Gerar wireframe HTML** — peça "wireframe HTML da V[N]"; obrigatório em Família A.
- **Gerar checklist VVC** — auto-produzido em S-VN como §3.x (D-148).
- **Gerar prompt de bloco V-VN/A-VN/F-APRESENT** — peça "prompt do [tipo-N]"; sessão combinada D-155.
- **Conduzir VV-VN (VVC)** — peça "inicia VV-V[N]"; modalidade C mista · 3 pontos-chave + gatilhos.
- **Atualizar vocabulário bilingue** — peça "estende vocabulário com termos de V[N]"; expansão incremental da tabela canônica.
- **Fechar pendência** — peça "decisão sobre P[NN]"; opções com trade-offs · Usuária decide.
- **Fechar conversa** — peça "fecha o bloco" ou "kit de encerramento"; kit D-033.
- **Validar estado** — peça "valide o estado".
- **Reestruturar planilha** — peça "nova análise da planilha" em mudança de fase.

---

## 13. Padrões estruturais de produto entre visões

Oito elementos são característica do produto TabloFlow e, portanto, **obrigatórios em toda visão** do Módulo 1.

**13.1 — Objetivo da Visão** · bloco de ajuda contextual em linguagem de negócio.

**13.2 — Fluxo de etapas progressivas** · etapas sequenciais com dependência · edição retroativa com aviso de impacto · resumo compacto de etapas concluídas.

**13.3 — Modelo de configuração (salvar e aplicar)** · T-MODELO · persiste etapas lógicas + TED (C.D2).

**13.4 — View especializada entre visões da mesma família** · V10 é view especializada sobre V4 Modo 2 (D-035). Modelos mutuamente aplicáveis via mapeamento declarado (D-046).

**13.5 — Resumo Executivo em 6 Blocos** (D-125)
Primeira aba do Excel · 6 blocos fixos: (1) Cabeçalho · (2) Números-âncora · (3) Distribuição · (4) Elementos destacados · (5) Leitura qualitativa com síntese · (6) Qualidade estrutural. **Renderizado em prosa executiva user-facing** (não JSON dump) por F-APRESENT capability 7.

**13.6 — Coração Visual da Visão** (D-126)
Aba que materializa visualmente a contribuição analítica primária. Corações declarados: V4 Composição Principal · V7 Mapa de Grupos · V8 Matriz de Presença · V9 Mapa de Perfil · V5 Mapa de Distribuição · V10 Curva Pareto · V6 Matriz de Cruzamento. Retroação diferida para V1/V2/V11 (Matriz de Confronto V2 · Mapa de Conciliação V1 · Mapa de Aderência V11).

**13.7 — Excel executivo é produto** (D-163 · D-166 · NOVO)

O Excel é o produto principal entregue. Toda visão exporta Excel executivo com:
- **Paleta aplicada** (1 de 4 · D-164 · catálogo canônico) · selecionada pela Usuária · **default universal Azul executivo** (D-168 · supera D-164 parcialmente) · ordem fixa do widget Azul · Cinza · Verde · Vinho
- **Arquitetura de abas canônica:** (1) Resumo Executivo narrativo · (2) Coração Visual da visão · (3) Base Analítica · (4) Diagnóstico (última aba · D-017 · 6 seções fundidas · D-165)
- **Tabela Excel nativa com totais dinâmicos** (D-166 · ListObject · totalsRowShown · função por coluna declarada em P-VN)
- **Formatação monetária BR e percentual** (D-166 · `R$ #,##0.00` · `0.00%`)
- **Colunas adaptativas ao cenário** (D-166 · montagem dinâmica · sem colunas vazias)
- **Contrato de unidade declarado por campo** em P-VN seção 3 (D-166 · monetário · percentual · contagem · texto · data · classificação · booleano)
- **Badges semânticos** (P1 de F-APRESENT · classificações com fill+fonte coerente à paleta)
- **Hierarquia tipográfica** (P1 de F-APRESENT · título_aba · seção · campo · valor)
- **Vocabulário user-facing exclusivo** (D-160 · zero vazamento técnico)

Especificação operacional das capabilities em §6.2 e §15.12.

**13.8 — P-UNIF · Princípio de Uniformidade Transversal F-APRESENT** (D-175 · NOVO · 24/04/2026)

Toda aba de produto Excel de toda visão consome F-APRESENT · não bespoke. Quando uma capability de F-APRESENT precisa ser estendida para suportar caso novo (ex: totalsRow com formato monetário · gráfico com unidade no eixo), a extensão acontece em F-APRESENT · nunca em `exportacao_vN.py` da visão. Defeito visual em uma aba é defeito de capability de F-APRESENT · correção sobe para F-APRESENT · todas as visões herdam correção automaticamente.

**Operacionalização:**
- `exportacao_v2.py`/`exportacao_v1.py`/etc consomem **apenas** funções de `/src/apresentacao/*` · zero formatação direta com openpyxl
- Toda string visível ao usuário passa por capability 2 (vocabulário bilingue) · zero hardcode
- Toda cor passa por paleta canônica (capability 1) · zero RGB hardcoded
- Toda formatação numérica passa por capabilities 4 (monetário) ou 5 (percentual) · zero `number_format` solto
- Bespoke transitório permitido **apenas** com comentário `# TODO-FAPRESENT-CLEANUP: <descrição>` · sessão F-APRESENT-cleanup (D-180) consome periodicamente

**Critério de fechamento:** uma visão N só fecha A-VN quando `grep -r "TODO-FAPRESENT-CLEANUP" /src/visoes/exportacao_vN.py` retorna **zero** ocorrências OU quando todas as ocorrências têm vencimento declarado em sessão F-APRESENT-cleanup futura próxima.

META-1 (rastreabilidade obrigatória) é o mecanismo operacional de P-UNIF.

---

## 14. Condução da Fase 1 e Fase 2 · Didática técnico-decisional (D-131 · estendida por D-156)

Padrão formalizado em 20/04/2026 · aplicado em 10+ sessões consecutivas · considerado **maduro**. Vigora integralmente na Fase 2. Complementar aos padrões D-019 + D-034 + D-033 + D-142.

### 5 princípios operacionais

**Princípio 1 · Tradução obrigatória técnico → decisional.**

**Princípio 2 · Acompanhamento visual primário · técnico secundário.** Planilha aba 1 (Horizontes) · aba 2 (Fase ativa · **6 quadrados por visão** · D-158) · aba 3 (Detalhe técnico).

**Princípio 3 · Sinalização proativa de densidade técnica · 4 categorias** (D-156 adicionou a 4ª):
- W decisões de negócio
- X decisões técnicas puras
- Y execuções de código supervisionadas
- Z validação de produto (VV-VN · VVC)

**Princípio 4 · Validação visual como único mecanismo de aprovação da Usuária.** Usuária carrega `base_vN_cliente.xlsx`, marca checklist derivado · opera em VVC com Arquiteto presente (D-156 · modalidade C mista). **Usuária não lê código em nenhuma sessão.**

**Princípio 5 · Transparência mútua sobre calibração.** Maduro após 10 aplicações consecutivas.

### Momentos técnicos resolvidos

- M1 · T-CONCAT e M2.STACK ✅ (D-135)
- M2 · F-EXP divisão ✅ (D-136)
- M3 · tipo_estrutural ✅ (D-133)
- M4 · Validação Visual · formalizada em D-148 + refinada em D-156 · opera em VVC (D-162)

### Complementaridade com outros padrões

D-131 complementa D-019 + D-034 + D-033 + D-142 · não substitui. Padrão ALINHA ativa-se adicionalmente em Marcos.

---

## 15. Condução da Fase 2 · Ciclo de 6 artefatos por visão (reescrito em 23/04/2026 · D-158)

Seção reescrita em ALINHA-Descoberta-Camada-Produto (4ª aplicação D-142). Absorve as 10 decisões-núcleo e 4 revisões. Estrutura anterior (5 artefatos · §15.1 original) superada por D-158.

### 15.1 · Ciclo canônico por visão · 6 artefatos sequenciais

Para cada visão N da Fase 2, sessão sequencial em ordem fixa (princípio B.1):

```
P-VN (Spec de Produto · paleta + vocabulário + arquitetura Excel + microcopy + checklist user-facing)
  ↓
S-VN (Spec técnica · contratos + regras + wireframe funcional [+ HTML Família A] + checklist derivado VVC)
  ↓
B-VN (condicional · critério D-147 · default = dispensado)
  ↓
V-VN (visao_vN.py · sessão combinada D-155)
  ↓
A-VN (app_vN.py · sessão combinada D-155 · aplica P-VN)
  ↓
VV-VN · VVC (Usuária opera · modalidade C mista · Arquiteto presente · 3 pontos-chave + gatilhos · D-156)
```

**Dependências duras:**
- P-VN aprovada antes de S-VN (vocabulário molda contrato · não o contrário)
- S-VN aprovada antes de B-VN / V-VN
- V-VN testado verde antes de A-VN
- A-VN rodando antes de VVC
- F-APRESENT P0 concluída antes de P-V1 (primeira visão)
- F-APRESENT P1 concluída antes de A-V1

**Quem faz o quê:**

| Bloco | Executor | Aprovação | Participação da Usuária |
|---|---|---|---|
| **P-VN** 🆕 | Arquiteto | Usuária (aprovação da camada de produto · precede S-VN) | Sessão completa · valida paleta · vocabulário · arquitetura Excel · microcopy |
| S-VN | Arquiteto | Usuária (dupla aprovação contrato + wireframe · tripla com HTML Família A) | Sessão completa · revisa wireframe · aprova checklist VVC |
| B-VN | Arquiteto (raro · só se D-147 exigir) | Usuária (auto-validação contra casos_esperados) | Sessão curta |
| V-VN | Claude Code (prompt em sessão combinada D-155) | Arquiteto valida testes verdes na retrospectiva | Não lê código (princípio 4) |
| A-VN | Claude Code (prompt em sessão combinada D-155) | Arquiteto valida App roda na retrospectiva · aplica P-VN | Não lê código · verá em VV-VN |
| **VV-VN (VVC)** | Usuária opera silenciosamente | **Usuária · gate final B.4 camada 1 · Arquiteto NÃO decide ✅/❌** | Sessão completa · modalidade C mista · 3 pontos-chave + gatilhos |

### 15.2 · Plano operacional · ~5-7 sessões por visão (pós-D-155/D-158)

Estimativa revisada em 23/04/2026 após D-158 consolidar 6 artefatos.

| Bloco | Sessões | Natureza |
|---|---|---|
| P-VN | 1-2 sessões | Produção da Spec de Produto |
| S-VN | 1-2 sessões | Produção da Spec técnica · dupla/tripla aprovação |
| B-VN | 0 sessões (Família A) · 1 sessão (se D-147 exigir) | Condicional |
| V-VN | 1 sessão combinada (D-155) | Claude Code + retrospectiva |
| A-VN | 1 sessão combinada (D-155) | Claude Code + retrospectiva |
| VV-VN (VVC · D-156) | 1 sessão acompanhada modalidade C | Usuária opera · Arquiteto presente |

**Total V1 (primeira aplicação do método novo):** ~7-8 sessões.
**Total V11 e demais (calibradas):** ~5-6 sessões.
**Família A completa pós-ALINHA (V1 + V11):** ~15-18 sessões.
**Sequência pós-ALINHA (A6 · estado atualizado pós-Sessão 3):** F-APRESENT P0 ✅ + F-APRESENT P1 ✅ (subsistema completo · pronto para consumo cross-visão) · P-V1 (próxima após fechamento de V2 retroativo) · S-V1 · V-V1 · A-V1 · VV-V1 (VVC) · · · V11 sequência análoga.

### 15.3 · Convenções de Spec técnica (S-VN)

**Estrutura canônica · 3 seções obrigatórias (B.2) + §13 + §9 Camada C:**

**Seção 1 · Contratos lógicos Pydantic**
- `V{N}Result` estendendo `VNResultBase`
- Requisitos D-130 integrais (analítico): `model_config` · `Field(..., description=...)` · `.para_contexto_ia()`
- Contratos auxiliares específicos
- Referência a contratos da Fundação

**Seção 2 · Regras de cálculo**
- Pipeline determinístico (C.1)
- Consumo de transversais com parâmetros declarados
- Bloqueios B-VN-* (MBO · C.D4) com 5 campos
- Catálogo de warnings W-VN-*
- TED (C.D2 · em sidebar global · D-153 · labels via vocabulário bilingue · D-160 · defaults via C.D6 · D-161)
- CPCO (C.D1) · modo da base

**Seção 3 · Wireframe funcional**
- Fluxo em etapas progressivas (§13.2)
- Estados da tela
- Microanálise progressiva
- Estrutura de exportação (referencia arquitetura da P-VN · não duplica)
- §3.x · Checklist VVC derivado mecanicamente (D-148)
- Aprovação explícita da Usuária (B.2 · reforçado por HTML em Família A · D-149)

**Checklist §13 · 7 padrões verificados:**
- 13.1 Objetivo · 13.2 Fluxo · 13.3 T-MODELO · 13.4 View especializada · 13.5 RE 6 Blocos · 13.6 Coração Visual · **13.7 Excel executivo é produto** (novo)

**Checklist §9 Camada C · 6 derivados verificados:**
- CPCO · TED · BAD · MBO · ECP · **DDU (novo · D-161)**

### 15.4 · Critério de base consumida (D-147)

Cada S-VN declara a base aplicando 3 perguntas: (1) cobertura de cenários · (2) volume para Validação Visual · (3) independência de evolução. Default: base mestre suficiente → B-VN dispensado. Família A: V2 · V1 · V11 consomem `base_fundacao.xlsx` diretamente.

### 15.5 · Recorte cliente-friendly (D-149)

Cada visão ganha `/bases/base_vN_cliente.xlsx` · reempacotamento mecânico · zero divergência. Arquivo canônico de entrada da VVC. Gerado por `/src/geradores/gerar_base_cliente.py`.

### 15.6 · Wireframe visual HTML (D-149 · obrigatório Família A)

HTML estático mínimo · neutro em identidade visual (Frente A parqueada · D-015 Camada B). Aprovação simultânea à Spec. Opcional a partir de S-V3.

### 15.7 · Checklist VVC derivado mecanicamente (D-148 · refinado por D-162)

Derivação 1:1 de `casos_esperados.yaml` via 5 templates canônicos (contagem_exata · contagem_categoria · warning_presente · estrutura_saida · bloqueio_emitido). Item não-coberto por assertion **não pode ser adicionado ad-hoc** · vira assertion nova + regenera. **Opera na camada VVC** (D-162) · VVP terá derivação user-facing própria (parqueada · ver §15.10).

### 15.8 · Padrão VV-VN · Validação Visual Construtora (VVC) modalidade C mista (D-156 · refinado por D-162)

Sessão Arquiteto + Usuária em chat concomitante. Usuária opera o app ao vivo · Arquiteto presente · modalidade C mista · opera integralmente na **camada VVC** de B.4 desdobrado (D-162).

**3 pontos-chave canônicos** (Usuária aciona):
1. Pós-processamento (Tela 8) · Usuária mostra KPIs + Resumo Executivo · Arquiteto comenta aderência
2. Pré-checklist (Tela 9) · Usuária mostra o que app exibe · Arquiteto comenta **sem induzir resposta**
3. Pós-exportação (Excel aberto) · Usuária relata estrutura · abas · Coração Visual · Arquiteto comenta conformidade

**Gatilhos livres:** travamento · observação · diagnóstico de ❌.

**4 tipos de intervenção do Arquiteto:** apoio operacional · resolução de ❌ · sugestão emergente (absorção silenciosa OU P-VN-Evo-NN OU D-XXX) · encerramento.

**Gate B.4 VVC inviolável:** Arquiteto comenta mas **NÃO decide ✅/❌** · autoridade 100% da Usuária.

**Separação estrutural de "baixar Excel" vs "aprovar visão" (D-162):** download de Excel disponível antes de checklist ✅. Aprovação ✅ é ato separado · independente do download.

Duração esperada ~1h visão nova · ~40min subsequentes.

### 15.9 · Retrospectivas pós-Claude Code (D-155)

Convenção Família A · V-VN e A-VN em **sessão combinada** · produção de prompt + pausa para Claude Code + retomada para retrospectiva + kit D-033. Aplicável a F-APRESENT também.

**Gate duplo D-174 (NOVO · 24/04/2026):** Retrospectiva pós-Claude Code passa a operar com 2 camadas obrigatórias antes de declarar A-VN concluída:
- **Camada 1 · Mecânica (Claude Code):** suite pytest 100% verde + `CHECKLIST_MECANICO.md` 100% ✅ + amostra Excel + `grep TODO-FAPRESENT-CLEANUP` declarado + bifurcações declaradas explicitamente
- **Camada 2 · Visual (Usuária):** inspeção Excel (todas abas + paletas) + inspeção app (`streamlit run`) + sanity check numérico C.D7 (D-183) + validação contra checklist VVC do DCV
- Sessão fecha apenas quando ambas aprovam · caso (b) camada 1 ✅ + camada 2 com defeitos → abre sub-sessão de correção dirigida
- Aplicado retroativamente a todas A-VN futuras · 1ª aplicação canônica foi A-V2 retroativa Sessão 4-ter+4-ter-bis

### 15.10 · Validação Visual de Produto · VVP (D-162 · horizonte parqueado)

Camada 2 de B.4 desdobrado · distinta de VVC. Opera em cliente real com base real · vocabulário exclusivamente user-facing · checklist derivado da tabela de vocabulário bilingue (não do YAML direto). **Sessão "Definição operacional VVP" abre quando Família A completa em VVC** · produz protocolo operacional.

Não misturar VVC (mecânica · base sintética · vocabulário permitido técnico) com VVP (adequação · base real · vocabulário exclusivo user-facing).

### 15.11 · Convenções de Spec de Produto (P-VN · D-158)

**5 seções canônicas obrigatórias:**

**Seção 1 · Paleta executiva**
- Paleta default declarada (D-168 · supera D-164 parcialmente · **Azul executivo é default universal das 11 visões**)
- Catálogo canônico preservado (D-164 · 4 paletas: Azul · Cinza · Verde · Vinho)
- Ordem fixa do widget de seleção: **Azul · Cinza · Verde · Vinho** (sem microcopy semântica · só nomes)
- Justificativa breve da escolha · referencia §13.7
- Aplica C.D6 (D-161) · Usuária pode sobrescrever no momento da exportação
- P-VN apenas declara "default Azul" · não precisa justificar paleta semântica por visão (simplificação D-168)

**Seção 2 · Vocabulário bilingue da visão**
- Tabela técnico ↔ user-facing da visão
- Consome `/specs/vocabulario_bilingue.md` v2 (tabela canônica transversal · 8 blocos · estendida em P-V2 retroativo · D-167)
- Adiciona termos visão-específicos
- Microcopy para enums · warnings · classificações · bloqueios
- Stepper user-facing · Família A: **4 etapas + Revisão** (D-167 · alinha com motor real · bloco intermediário condicional parqueado como P-V*-Evo enquanto motor não pré-detectar casos estruturais)
- Substituição dinâmica de classificações com rótulos amigáveis quando aplicável (Bloco 3 estendido do `vocabulario_bilingue.md` v2)
- Exibição canônica de `None` como `—` (Bloco 8 NOVO do `vocabulario_bilingue.md` v2)

**Seção 3 · Arquitetura de abas do Excel**
- Ordem e nome user-facing das abas (Resumo Executivo · Coração Visual da visão · Base Analítica · Diagnóstico)
- Propósito de cada aba
- Coração Visual nomeado conforme §13.6
- **Contrato de unidade por campo** (D-166) · monetário · percentual · contagem · texto · data · classificação · booleano
- **Função de total por coluna** (D-166) · sum · average · count · custom · none
- **Colunas adaptativas declaradas** · condição de inclusão por coluna (D-166)

**Seção 4 · Microcopy de telas**
- Títulos · subtítulos · captions · labels
- Textos de ajuda contextual (13.1)
- Mensagens de erro e bloqueio
- Mensagens de warnings · ajustes · decisões do usuário

**Seção 5 · Checklist user-facing** (estruturado · aguarda protocolo VVP)
- Esqueleto derivado do checklist técnico VVC
- Tradução via tabela de vocabulário bilingue
- Aplicação operacional definida em sessão futura "Definição operacional VVP"

**Entrega:** markdown consolidado · amostras de paleta aplicada vivem como assets de F-APRESENT capability 1 · P-VN referencia sem duplicar.

**Aprovação:** Usuária · camada de produto é autoridade dela. P-VN aprovada antes de S-VN abrir.

### 15.12 · Convenções de F-APRESENT (D-159 · P0+P1 CONCLUÍDOS)

**Localização:** `/src/apresentacao/` · 2 blocos Claude Code dedicados (P0 e P1) · sessão combinada D-155.

**10 capabilities canônicas · subsistema completo · interfaces estáveis:**

| # | Capability | Interface mínima | Prioridade | Status |
|---|---|---|---|---|
| 1 | Catálogo de 4 paletas | classe `Paleta` (com `fonte_familia`) + `CATALOGO_PALETAS` · função `aplicar_paleta(workbook, paleta)` | P0 | ✅ |
| 2 | Rótulos user-facing | `carregar_vocabulario_bilingue()` · `traduzir(termo_tecnico, contexto)` | P0 | ✅ |
| 3 | Tabela Excel nativa + totais | `criar_tabela_executiva(ws, range, nome, totais_por_coluna)` | P0 | ✅ |
| 4 | Formatação monetária BR | `FORMATO_MONETARIO_BR` · `aplicar_formato_monetario(celulas)` | P0 | ✅ |
| 5 | Formatação percentual | `FORMATO_PERCENTUAL` · `aplicar_formato_percentual(celulas, conversao_fracao=True)` | P0 | ✅ |
| 6 | Colunas adaptativas | `montar_colunas_adaptativas(config_usada, esquema_colunas)` | P0 | ✅ |
| 7 | Resumo Executivo narrativo | `renderizar_resumo_executivo(ws, resumo, paleta, vocabulario)` | P0 | ✅ |
| 8 | Badges semânticos | `aplicar_badge(celula, classificacao, paleta, mapeamento=MAPEAMENTO_V2)` · `BadgeStyle` frozen + `CATALOGO_BADGES` (4 paletas × 4 semânticas: positivo/negativo/neutro/atenção · atenção universalmente âmbar) · mapeamento por visão injetável | P1 | ✅ |
| 9 | Hierarquia tipográfica | 4 helpers individuais: `aplicar_titulo_aba(cell, paleta)` · `aplicar_secao(cell, paleta)` · `aplicar_campo(cell, paleta)` · `aplicar_valor(cell, paleta)` + wrappers `escrever_titulo_aba(ws, row, col, texto, paleta)` etc · `aplicar_hierarquia_tipografica(ws, paleta)` mantido como wrapper canônico no-op (reservado para evolução por marcador) | P1 | ✅ |
| 10 | Diagnóstico narrativo | `renderizar_diagnostico(ws, config_usada, resolucao, modelo, t_diag, warnings, paleta, vocabulario)` · 6 seções fixas user-facing (D-165) · `formatar_valor_ou_traco(valor, origem)` para None com microcopy contextual · `_normalizar_categoria` para Enum/string · capability genérica · aceita dict OU Pydantic via `_get_cfg/_ler_campo` · split de warnings UMA vez (informativo+ajuste_leve→seção 2 · alerta_estrutural+decisao_usuario+escape→seção 3) · aceita `t_diag=None` e `warnings=None` sem quebrar | P1 | ✅ |

**Campos canônicos esperados em `config_usada` por capability 10 (12 campos achatados):**

```python
# Seção 1 · Como foi analisado
config_usada.arquivo: str
config_usada.aba_consumida: str
config_usada.modo_base: str  # SIMPLES | DUAL | POR_LINHAS · etc · enum mapeado para user-facing via vocabulario
config_usada.agrupadores: list[str]
config_usada.campo_analisado: str
config_usada.tipo_medida: str
config_usada.colunas_mapeadas: dict[str, str]  # técnico → user-facing

# Seção 4 · Decisões do usuário
config_usada.estados_nao_escolhidos: list  # estados Modo 4

# Seção 5 · Configurações avançadas aplicadas
config_usada.paleta_aplicada: str  # nome da paleta selecionada
config_usada.thresholds_usados: dict
config_usada.defaults_sobrescritos: dict

# Seção 6 · Qualidade estrutural
config_usada.nulos_por_classificacao: dict
```

**Adaptador A-VN específico (recomendado para Sessão 4 e A-VN futuras):**

Capability 10 é genérica · não conhece visão. Cada A-VN deve criar:

```python
def _extrair_config_para_diagnostico(vN_result) -> dict:
    """
    Monta dict canônico achatado para capability 10 a partir dos múltiplos
    campos do VNResult (config_usada + comparacao_realizada + agrupadores_aplicados
    + upstream meta + paleta selecionada do app).
    """
    return {
        "arquivo": ...,
        "aba_consumida": ...,
        "modo_base": vN_result.modo_upload,
        "agrupadores": vN_result.agrupadores_aplicados,
        "campo_analisado": vN_result.comparacao_realizada.campo_analisado,
        # ... etc
    }
```

Sem mudança em `VNResult` · sem mudança em motor · sem mudança em contratos. Capability 10 trata ausência via `formatar_valor_ou_traco(None, origem)` → `—` com microcopy contextual.

**Estratégia de testes consolidada (pós-P1):**

- P0: `/src/testes/test_apresentacao.py` · 179 testes (P0)
- P1: `/src/testes/test_apresentacao_p1_badges.py` (36) · `test_apresentacao_p1_tipografia.py` (40) · `test_apresentacao_p1_diagnostico.py` (51) · 127 testes
- Fixtures canônicas: `paleta_azul` · `paleta_cinza` · `paleta_verde` · `paleta_vinho` · `workbook_exemplo` · `v2_result_canonico`
- 4 tipos: interface · snapshot · regressão · invariantes
- **Suite total atual: 594/607 verdes** · 13 vermelhos pré-existentes formalizados em D-169

**Gate P0 (concluído):** 7 capabilities P0 · 4 Excel de demo (1 por paleta) · regressão preservada.

**Gate P1 (concluído):** 3 capabilities P1 · 127 testes novos verdes · 0 regressão nos testes herdados.

**Subsistema F-APRESENT pronto para consumo por A-V2 refatorada (Sessão 4) e por todas as A-VN futuras das 11 visões.**

### 15.13 · Convenções de acompanhamento operacional

**Aba 1 · Onde estou no todo** (D-150) · Usuária atualiza Horizontes Futuros (~10s por sessão).

**Aba 2 · Painel da fase ativa** · Usuária atualiza **6 quadrados por visão** (~30s por sessão · novo em D-158).

**Aba 3 · Detalhe técnico das visões** · consulta pontual.

**Planilha reestruturada quando muda de fase** ou em mudança estrutural de método (precedente D-150 · ALINHA-Descoberta-Camada-Produto transição 5→6 quadrados).

### 15.14 · Condução de sessões operacionais · padrão 3 fases (D-185 · NOVO · 24/04/2026)

A partir da Sessão 5 (correção P-22 + P-23), toda sessão operacional não-Marco opera em 3 fases explícitas:

**Fase (a) · Investigação e planejamento** (precede o prompt para Claude Code):
1. Investigação dirigida quando há suspeita de bug estrutural · Arquiteto propõe prompt de leitura apenas (sem correção) · Claude Code retorna diagnóstico antes de qualquer correção
2. Escopo consolidado · Arquiteto propõe ANTES de abrir o prompt toda a lista de pontos que serão cobertos · Usuária valida escopo como um todo · prompt único cobre tudo
3. Documentação anterior absorvida · todas decisões de sessões anteriores formalizadas como D-XXX ANTES da próxima sessão de implementação

**Fase (b) · Implementação Claude Code:** prompt único com escopo fechado · sem ajustes incrementais. Se nova questão emerge durante a execução, vira backlog para sessão seguinte (não puxa o prompt).

**Fase (c) · Validação camada 2:** Usuária valida o produto entregue · não abre escopo novo. Se aparece defeito durante a validação, abre nova sessão de correção dirigida · não reabre a sessão atual.

Padrão herdado e estendido de D-142 ALINHA (4 sub-blocos α·β·γ·δ) para sessões operacionais não-Marco. Aplicado pela primeira vez na Sessão 5 (investigação dirigida P-22 + P-23 antes de qualquer correção). Sessão F-APRESENT-cleanup (D-180) também segue o padrão.

**Princípio raiz:** correção iterativa fragmenta documentação e sobrecarrega Usuária na camada 2 · investigação + escopo consolidado + uma rodada de execução produz resultado mais limpo e mais rápido em horas reais.

### 15.15 · Sub-camada "smoke visual" no gate duplo D-174 (D-196 · NOVO · 25/04/2026)

**Contexto:** Sessão 8 entregou Camada 1 com 725 testes verdes mas Camada 2 (Usuária) descobriu que o Excel produzido com unidade=PERCENTUAL exibia valores absurdos (Média = 69.767%) · cabeçalho "p.p" com formato "%". Suite mecânica não pegou porque testes validavam estrutura/contrato · não valor renderizado em célula. Gap de método identificado: D-174 Camada 1 mecânica é insuficiente quando o sintoma é "número absurdo na apresentação".

**Decisão (D-196):** toda A-VN ganha arquivo `src/testes/test_vN_smoke_visual.py` com mínimo 4-6 testes de smoke que:
1. Geram amostra in-memory (sem salvar arquivo)
2. Lêem valor de célula-chave (cards do Resumo Executivo · primeira linha da Matriz · etc)
3. Aplicam number_format manualmente para obter valor visual renderizado
4. Assertam que valor está em range realista para a unidade declarada

**Cobertura mínima por visão (template V2 estabelecido na Sessão 8.1 · 6 testes):**
- Card "Total/Média" da unidade default · range realista
- Card de diferença · range realista por unidade
- Pelo menos 1 cenário PERCENTUAL (range 0-100%)
- Pelo menos 1 cenário MONETARIO (range R$ realista)
- Pelo menos 1 cenário QUANTIDADE (inteiros ≥0)
- Estrutura de blocos do Resumo Executivo (ex: Saúde da comparação tem 3 colunas em PERCENTUAL · 4 nas demais)

**Critério operacional:** smoke visual roda na suite normal `pytest -q` · gate camada 1 só fecha quando smoke também verde · custo ~3s por suite de smoke por visão.

**Padrão estende D-174 sem revogar:** D-174 camada 1 segue exigindo testes mecânicos do contrato/estrutura · D-196 adiciona sub-camada visual mínima como linha de defesa contra regressão de apresentação.

**Aplicação obrigatória:** A-V1 e A-V11 abrem com smoke visual incluído por default · 4-6 testes mínimos. Promoção em capability genérica de F-APRESENT (D-197) deve incluir helpers que facilitam smoke visual cross-visão.

### 15.16 · Mockup Excel-alvo · gate β.3 (D-203 · NOVO · 26/04/2026)

D-191 (provisória 25/04/2026) vence formalmente em ALINHA-Lições-Família-A. Mockup Excel-alvo é gate operacional para visões pioneiras de cada família.

**Escopo β.3 · 5 mockups totais ao longo do projeto:**
- V1 da Família A · V4 da Família C · V3 da Família B · V7 da Família D · V5 da Família E

**Visão filha herda visualmente** da pioneira:
- V11 ← V1 · V10 ← V4 · V8 ← V3 · V9 ← V7 · V6 ← V5

**Escape declarado:** se durante trabalho da visão filha aparecer divergência visual material com a mãe · mockup é puxado pontualmente.

**Modalidade de produção:** Usuária esboça seções (o que tem que aparecer · ordem · ênfase) · Arquiteto detalha (vocabulário bilingue · paleta · formatação numérica · contrato unidade · microcopy) · Usuária aprova.

**Gate (D-204 Cláusula A):** Arquiteto recusa gerar prompt Claude Code de A-VN pioneira sem mockup aprovado.

### 15.17 · Refactor Dirigido · 5ª modalidade canônica (D-206 · NOVO · 26/04/2026)

5ª modalidade canônica do método TabloFlow · ao lado de:
1. Sessão Marco (ALINHA · D-142 · 4 sub-blocos α/β/γ/δ)
2. Sessão A-VN (gate duplo D-174 · 3 fases D-185)
3. Sub-sessão cirúrgica (correção dirigida pós-Camada 2)
4. Sessão combinada (D-155)
5. **Refactor Dirigido (NOVO · D-206)**

**Definição:** sessão Claude Code única · escopo grande mas coerente em natureza · onde o produto a ser entregue já existe e funciona · refactor promove para arquitetura nova sem mudança de comportamento observável.

**4 salvaguardas obrigatórias:**
1. Suite atual é gabarito · sem testes novos exigidos
2. Ordem interna do refactor protege contra cascata · `pytest` entre etapas
3. Investigação prévia feita pelo Arquiteto · Claude Code só executa
4. Validação pós-refactor é objetiva · suite verde + 1 smoke visual curto

**1ª aplicação:** D-202 (Sessão Promoção de Fundação · 26/04 noite).

---

## 16. Sessão de Promoção de Fundação · escopo refinado (D-202 · substitui D-197)

D-197 (25/04/2026) declarou bloqueante pré-V1 com escopo provisório de 5 itens. Inventário V2→Fundação produzido em ALINHA-Lições-Família-A (D-200 · 26/04/2026 manhã) revelou **5 itens críticos + 3 altos** · escopo 5× maior. D-202 substitui D-197 com escopo detalhado e modalidade Refactor Dirigido (D-206).

### 16.1 · Inventário promovido · 8 itens

**🔴 Críticos (bloqueantes V1):**
1. Cria `ContratoComparativo` em `contratos.py` · `ComparacaoV2` herda
2. Adiciona `unidade` e `tipo_campo` ao `ColumnMeta`
3. Move `_default_unidade_para_tipo` para `apresentacao/formatos.py` · deduplica
4. Corrige bugs cap 7 e cap 10 da F-APRESENT (Resumo Executivo + Diagnóstico)
5. Extrai sub-templates de `_renderizar_resumo_executivo_v2` para `apresentacao/templates/familia_a/`

**🟠 Altos (não bloqueiam V1 mas vão doer):**
6. Promove `_construir_leitura_qualitativa_v2` para template parametrizado
7. Resolve P-37 (D-205) · capability 11 nova `formato_adaptativo_por_unidade`
8. Cleanup dos 86 comentários "Sessão X · C-N" (Cláusula C de D-204)

**🟡 Deferido (decisão consciente):**
9. D-189 vocabulário · NÃO entra · decisão fica para abertura de Família B

### 16.2 · 4 salvaguardas obrigatórias (D-206)

1. Suite atual 731 verde é gabarito de pronto
2. Ordem de refactor protege contra cascata · contratos → apresentação → cleanup
3. Investigação prévia já feita · D-200 inventário
4. Validação pós-refactor objetiva · suite verde + 1 smoke visual TEMPO_HORAS

### 16.3 · Roadmap operacional pós-Promoção

✅ V2 retroativa Excel funcional (Sessão 8.1-8.4 · D-201)
✅ ALINHA-Lições-Família-A (D-200 a D-207)
▶ **Sessão de Promoção de Fundação** (D-202 · 26/04 tarde-noite · Refactor Dirigido)
▶ Mockup-V1 (D-203 · modalidade β.3)
▶ P-V1 / S-V1 / V-V1 / A-V1 / VV-V1
▶ Auditoria pós-V1 (D-204 cláusula B · não · V1 não é pioneira refactorada · auditoria pós-V11 que é o gate)
▶ V11 sob método novo
▶ **Auditoria pós-V11** (D-204 cláusula B · gate antes de Família C)
▶ Família C abre · V4 (mockup β.3) · V10 (herda V4) · auditoria pós-V4
▶ Famílias seguintes · B → D → E (cada uma com mockup pioneiro + auditoria pós-1ª visão)

V1 não inicia sem D-202 concluída + Mockup-V1 aprovado. V11 não inicia sem V1 validada em VVC. Família C não inicia sem auditoria pós-V11 limpa.

---

## 17. Cláusulas anti-vazamento Fundação→Visão · tripla proteção (D-204)

V2 retroativa demonstrou empiricamente 3 falhas combinadas que produziram vazamento Fundação→Visão silencioso:
1. Spec não enxergava produto Excel · Claude Code interpretou
2. Sem checkpoint pós-V2 · ninguém perguntou "isso pertence aqui ou pertence à Fundação?"
3. Comentários de código (86 referências em V2) viraram registro silencioso

D-204 fecha as 3 falhas com cláusulas combinadas.

### 17.1 · Cláusula A · Mockup é gate · não recomendação

*Nenhuma sessão A-VN abre sem mockup Excel-alvo aprovado quando a visão é pioneira de família. Mockup ausente bloqueia a sessão · Arquiteto recusa gerar prompt Claude Code até existir.*

Operacionalizada por D-203 (escopo β.3 com escape · 5 mockups totais).

### 17.2 · Cláusula B · Auditoria estrutural pós-1ª visão de família

*Toda família · ao terminar 1ª visão completa em VV-VN ✅ · entra em sessão obrigatória de auditoria estrutural antes de abrir 2ª visão. Auditoria responde 1 pergunta por arquivo `*_vN.py`: "isso aqui pertence a esta visão · ou pertence à Fundação?". Promoções identificadas viram sub-sessão de Promoção · sem promoção identificada, declara-se "auditoria limpa" e segue.*

Aplicada **retroativamente em ALINHA-Lições-Família-A** (auditoria pós-V2 · ainda que tarde · D-200 inventário é o produto dela).

Aplicações futuras obrigatórias:
- Pós-V11 antes de Família C abrir
- Pós-V4 antes de V10 abrir
- Pós-V3 antes de V8 abrir
- Pós-V7 antes de V9 abrir
- Pós-V5 antes de V6 abrir

### 17.3 · Cláusula C · Comentário em código não substitui D-XXX

*Comentários do tipo "Sessão X · C-N" ou "D-XXX" no código de produção são marcadores temporários · não documentação. Toda decisão estrutural que aparece como comentário em código deve ter D-XXX correspondente em DECISIONS.md em até 24h após a sessão. Comentário sem D-XXX correspondente é débito de método · catalogado e resolvido na auditoria pós-família.*

Aplicação imediata: 86 comentários históricos atuais em V2 são absorvidos no cleanup da Sessão Promoção (item 8 do inventário · D-202).

### 17.4 · Como as 3 cláusulas conversam

| Cláusula | Quando atua | Tipo de proteção |
|---|---|---|
| A · Mockup é gate | **Antes** de A-VN abrir | Preventiva |
| B · Auditoria pós-família | **Depois** de 1ª visão fechar | Detectiva |
| C · Comentário ≠ D-XXX | **Durante** sessões + auditoria | Estrutural |

Vazamento bloqueado na entrada (A) · descoberto se passar (B) · documentado se aceito (C).

---

## 18. Princípios consolidados Família A · canônicos para famílias futuras (D-207)

ALINHA-Lições-Família-A destila 4 princípios que se promovem a canônicos. Quando Família B começar (após V11 fechar + auditoria pós-V11 limpa) · Arquiteto e Claude Code entram com os 4 princípios já internalizados.

### Princípio 1 · "Excel é o produto · Spec textual não basta"

Toda visão produz Excel · Excel é entrega final. Mockup Excel-alvo (D-203) operacionaliza · gate D-204 cláusula A torna obrigatório.

### Princípio 2 · "Cada família tem checkpoint estrutural depois da 1ª visão"

Vazamento de camada só é detectável pós-fato. D-204 cláusula B torna detecção obrigatória.

### Princípio 3 · "Decisão estrutural não pode viver só em comentário de código"

Conhecimento institucional preservado em D-XXX formal · não em comentários. D-204 cláusula C torna vinculante.

### Princípio 4 · "Refactor ≠ Invenção · método deve diferenciar"

Refactor tem critério de pronto objetivo (suite passa) e cerimonial menor que invenção. D-206 cristaliza Refactor Dirigido como 5ª modalidade.

---

O Arquiteto não pede confirmação para o óbvio. Interrompe apenas quando há decisão com impacto estrutural.

