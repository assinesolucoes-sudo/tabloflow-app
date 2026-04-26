# GLOSSARIO.md — TabloFlow

Glossário completo de termos, nomenclaturas e convenções do projeto.

A versão completa vive neste arquivo, com exemplos e referências cruzadas — usada por sessões Claude Code, pelo Arquiteto, e como material de onboarding. Fonte canônica única de vocabulário do projeto.

**Última atualização:** 21/04/2026 — Sessão **ALINHA-Fundação-Design→F-MOT** (2ª aplicação do padrão ALINHA · retroativamente a 1ª é a Sessão Fase 0 → Fase 1). Incorpora decisão nova **D-142** (formalização do padrão ALINHA) e consolida retroativamente D-140 e D-141 de G-FUND parte 3. Mudanças principais:

(A) §1 · 2 verbetes novos · **`Marco` 🆕📌** (critério cumulativo de 3 condições para acionar padrão ALINHA) · **`Padrão ALINHA` 🆕📌** (sessão dedicada ao fechar Marco · 4 sub-blocos α·β·γ·δ · envelopa D-033 como último sub-bloco).

(B) §2 · 1 verbete novo · **`ALINHA-<Marco>→<próximo>` 🆕** (tipo de bloco de execução · nomeado com sufixo direcional).

(C) §7 · menção a D-142 em "Decisões estruturais de condução do método".

(D) §10bis · sem alteração (padrões consolidados permanecem como em 20/04/2026 · D-142 é metadecisão de método e vive em §1/§2 · não é padrão de produto).

---

**Histórico anterior preservado (20/04/2026):** Sessão de Alinhamento Técnico Fase 0 → Fase 1 (retroativamente categorizada como `ALINHA-Fase-0→Fase-1`). Incorporou decisões D-122 a D-132. **Formalização efetiva dos 7 padrões consolidados** que aguardavam formalização desde o fechamento da Fase 0 (Opção A escolhida pela Usuária · D-122 a D-128 com nome canônico e enunciado formal · D-129 sumário). Mudanças principais daquela atualização:

(1) §10bis nova · "Padrões consolidados formalizados" inserida entre §10 e §11 · 7 entradas canônicas com nome, abreviação, enunciado resumido, escopo, aplicações consolidadas, referência ao D-XXX de origem · **CPCO · Consolidação Pré-Cálculo Obrigatória** (D-122 · CONTEXT §9 Camada C) · **TED · Thresholds Editáveis Declarados** (D-123 · §9 Camada C) · **BAD · Base Analítica e Diagnóstico** (D-124 · §9 Camada C) · **Resumo Executivo em 6 Blocos** (D-125 · §13.5 padrão estrutural de produto) · **Coração Visual da Visão** (D-126 · §13.6 padrão estrutural de produto) · **MBO · Matriz de Bloqueios Operacionais** (D-127 · §9 Camada C) · **ECP · Escala de Cardinalidade com Patamares** (D-128 · §9 Camada C).

(2) §11 anti-glossário · "Dados Brutos Processados" formalmente rejeitado em favor do padrão BAD (D-124). Termo aparecia em prévios anteriores · substituído por Base Analítica (1 linha por unidade analítica consolidada) + Diagnóstico (contagens estruturais agregadas).

(3) §4 T-AGRUPA · entrada atualizada para citar formalização como CPCO (D-122) · V6 como 9ª consumidora com consumo padrão reforça o tronco comum.

(4) §4 T-MODELO · entrada atualizada para citar consumo obrigatório de TED (D-123) · persistência de thresholds editáveis por visão.

(5) §4 T-DIAG · entrada atualizada para citar serialização JSON-compatível obrigatória para receptividade a IA (D-130).

(6) §10 padrão "herança adaptada à natureza analítica" · contagem atualizada para ~15 aplicações documentadas (após refino V5 + V6).

(7) Decisões convergentes daquela sessão registradas em DECISIONS.md: D-130 receptividade a IA nos contratos da Fundação com implementação pós-Família A · D-131 padrão de condução da Fase 1 com 5 princípios didáticos · D-132 dashboard visual da Fase 1 na aba 1 da planilha.

**Gatilho de atualização desta versão (21/04/2026):** "novo padrão consolidado que merece entrada própria" (padrão ALINHA · D-142) + "termo novo formalizado" (Marco · critério cumulativo de 3 condições). Versão anterior (20/04/2026 · pós-sessão de alinhamento Fase 0→Fase 1) preservada em `/legacy/glossario_pos_alinha_fase0_fase1.md`. Fase 0 · Compreensão CONCLUÍDA permanece (11 de 11 DCVs aprovados). **Marco · Fundação-Design CONCLUÍDA (20/04/2026) · formalmente fechado em sessão ALINHA (21/04/2026).** Próximo bloco operacional: **F-MOT** (primeiro bloco de implementação da Fase 1 · sessão dedicada Claude Code).

---

**Materialização arquitetural na Fundação (G-FUND parte 1 · 20/04/2026):**

- **MBO (C.D4 · D-127)** ganhou materialização via `BloqueioOperacional` contrato único (D-134) — Specs S-VN declaram matriz V-específica como lista de dicionários · exportacao.py consome uniformemente.
- **CPCO (C.D1 · D-122)** reforçado por D-133 — `column_meta.tipo_estrutural` sempre computado no motor_base · consolidação pré-cálculo depende de metadados estáveis.
- **Resumo Executivo em 6 Blocos (§13.5 · D-125)** e **Coração Visual (§13.6 · D-126)** entraram no contrato `VNResultBase` como campos obrigatórios (`resumo_executivo: ResumoExecutivoPadrao` · `coracao_visual: CoracaoVisualRef`).
- **TED (C.D2 · D-123)** entrou no contrato `LeituraQualitativa` (`thresholds_usados: Dict[str, float]`) e em T-MODELO (persistência obrigatória · especificação na parte 2).
- **BAD (C.D3 · D-124)** entrou em `VNResultBase` como `base_analitica: pd.DataFrame` obrigatório + consolidação via T-DIAG para aba Diagnóstico.

---

## Como ler este documento

Seções temáticas. Dentro de cada seção, ordem lógica (não estritamente alfabética — os termos mais importantes aparecem primeiro). Quando um termo é definido em outro lugar (uma Regra do CONTEXT, uma Decisão D-XXX em DECISIONS, uma spec), há referência cruzada.

Convenção de marcação:

- 🆕 **Novo** — termo introduzido em data recente
- 📌 **Cito** — termo usado em comunicação direta com a Usuária; precisa estar claro
- ⚠️ **Cuidado** — termo onde já houve confusão; ler descrição completa
- 🔧 **Técnico** — termo usado em código/spec, raramente em conversa
- ❌ **Descontinuado** — termo que não deve ser usado no método atual

---

## 1. Método e processo

### `DCV` — Documento de Compreensão da Visão 📌

**Definição formal:** artefato curto em prosa, vivendo em `/specs/dcv/dcv_vN.md`, que captura:

1. **O que a visão faz** — em uma frase de negócio, na voz da Usuária
2. **O que a visão precisa receber** — estrutura de entrada, tipagem, casos especiais
3. **O que a visão precisa entregar** — estrutura de saída, classificações, warnings
4. **O que ainda não está claro** — pendências enumeradas P-NN que precisam de decisão antes de qualquer outra coisa

**Por que existe:** entre 13 e 17 de abril de 2026 ficou claro que entrar em spec/base/código sem alinhamento de compreensão prévio gerava ciclos repetidos de retrabalho. A introdução do DCV resolve estruturalmente esse problema (princípio A.2 do CONTEXT v2, formalizado originalmente pela D-011).

**Quem produz:**

- **DCV prévio** — Usuária produz com apoio do ChatGPT como analista técnico (D-012)
- **DCV refinado** — Arquiteto refina o prévio aplicando o método TabloFlow (formato padrão, contratos Pydantic latentes, pendências enumeradas, alinhamento com DCVs da mesma família já aprovados)
- **DCV aprovado** — Usuária valida e aprova

Vive em `/specs/dcv/dcv_vN.md` após aprovação.

### `Fase 0 · Compreensão` 📌

Primeira fase do método TabloFlow. **Objetivo:** aprovar os 11 DCVs do Módulo 1. **Critério de conclusão:** os 11 DCVs aprovados pela Usuária. Nenhuma outra fase inicia sem isso (princípio A.1). Definida no CONTEXT v2 §3.

### `Fase 1 · Fundação` 📌

Segunda fase do método. **Objetivo:** consolidar os requisitos comuns dos 11 DCVs aprovados e implementar a fundação que serve as 11 visões (motores, contratos, transversais, exportação Excel padrão). **Critério de conclusão:** motores + transversais + exportação validados por testes automatizados E inspecionados pela Usuária sobre a base de fundação multi-visão. Definida no CONTEXT v2 §3.

### `Fase 2 · Visões` 📌

Terceira fase do método. **Objetivo:** implementar as 10 visões sobre a Fundação aprovada, na ordem lógica por famílias. Para cada visão, 5 artefatos sequenciais: Spec (com wireframe funcional) → Base → `visao_vN.py` → `app_vN.py` → Validação Visual. **Critério de conclusão por visão:** Validação Visual registrada na planilha.

### `Família conceitual` 📌

Agrupamento de visões que compartilham natureza analítica. 5 famílias no Módulo 1:

- **Família A · Confronto entre universos** — V2 (dois estados de uma base), V1 (duas bases com chave), V11 (duas bases sem chave, por aderência contextual). Família mais rica do Módulo 1, refletindo o peso do confronto no uso contábil brasileiro. V1 e V11 compartilham T-DUAL mas operam com motores distintos — V1 determinístico por chave, V11 probabilístico por score textual. Não há relação de view especializada entre V1 e V11.
- **Família B · Sequência ao longo de eixo ordenado** — V3 (valor no tempo), V8 (presença no tempo)
- **Família C · Composição e participação** — V4 (participação, ABC, multi-métrica), V10 (Pareto)
- **Família D · Posição relativa** — V7 (desvio da média do grupo), V9 (ranking multidimensional)
- **Família E · Estrutura interna do recorte** 🆕 — V5 (dispersão e outliers · estatística descritiva univariada de um campo numérico), V6 (cruzamento de 2 campos categóricos · bivariado). Visões que **expõem propriedades estruturais internas de um recorte da base** sem comparar com referência externa, sem benchmark interno por grupo, sem eixo ordenado, sem total geral. Família com par operacionalmente distante — V5 e V6 não compartilham transversais centrais e não navegam fronteira em interface operacional. Reformulada de "Estrutura interna de um campo" para "Estrutura interna do recorte" no refino DCV-V5 (D-110) — formulação anterior tinha imprecisão (V6 é bivariada · não "de um campo"). Adaptação D-073 ao próprio método de posicionamento de família: famílias com par operacionalmente próximo (B · D) merecem tabela de retroação diferida; Família E (par distante) merece declaração enxuta de convivência sem retroação diferida formal.

A ordem de implementação segue A → C → B → D → E, porque começar pela família mais simples dentro de cada par gera transversais que a irmã reusa.

### `Wireframe funcional` 🆕📌

Descrição textual ou esquemática do fluxo de tela da visão: estados, configuração progressiva, microanálise, exportação. **Seção obrigatória da Spec** (princípio B.2 do CONTEXT v2) — não é bloco separado, mas recebe **aprovação explícita da Usuária antes do código iniciar**, dentro do mesmo bloco S-VN. Garante que UX e contrato lógico nasçam juntos, não se divergindo no app.

### `Validação Visual` · `VV-VN` 📌 (reformulado em 23/04/2026 · D-156)

Etapa exclusiva da Usuária (princípio B.4 do CONTEXT · gate final de aprovação de visão). **Reformulada em D-156** (23/04/2026) de sessão solo para **sessão acompanhada modalidade C mista** · nova nomenclatura oficial `VV-VN` (ex: `VV-V2` · `VV-V1` · `VV-V11`).

**Natureza:** sessão Arquiteto + Usuária em chat concomitante. Usuária opera `app_vN.py` silenciosamente no terminal · carrega `base_vN_cliente.xlsx` · configura análise · processa · marca cada item do checklist derivado (§3.x da Spec · derivado de `casos_esperados.yaml` via D-148) em ✅/❌.

**3 pontos-chave canônicos** em que Usuária aciona Arquiteto: (1) pós-processamento (Tela 8 · Resultado) · (2) pré-checklist (Tela 9 · antes de marcar) · (3) pós-exportação (Excel aberto). Fora dos 3 pontos, gatilhos livres ficam disponíveis (travamento · observação · diagnóstico de ❌).

**Gate B.4 inviolável:** Arquiteto pode comentar observações técnicas mas **NÃO decide ✅/❌** · autoridade de aprovação é 100% da Usuária. Princípio 4 de D-131 preservado (Usuária não lê código).

**Aprovação:** todos os itens ✅ → 5º quadrado ✅ na aba 2 da planilha · visão aprovada. Qualquer ❌ → Arquiteto diagnostica na mesma sessão (M4 de D-131 · bug · lacuna de Spec · interpretação divergente).

Detalhes em CONTEXT §15.8 + D-156. **Aplicações previstas:** VV-V2 (a partir de 23/04/2026) · VV-V1 · VV-V11 · maturação após Família A completa.

### `Validação de Produto` 📌 (frente parqueada · distinta de VV-VN)

Frente parqueada formalizada em ALINHA-Fase-1→Fase-2 · **inicia após Família A validada** (3 visões com 5/5 quadrados verdes). **Distinta de VV-VN:** valida **adequação** (não mecânica) · usa **bases reais de cliente** (não sintéticas) · pode revelar gaps de produto / out-of-scope / evolução · decisões de negócio pesadas. Horizonte 14 (Zona 2 · Produtização) na aba 1 da planilha (D-150).

### `Rebaseline`

Processo de "zerar a contagem do que está concluído" quando se descobre que artefatos antigos não passaram pelo método atual. Já aconteceu **três vezes**:

- 17/04/2026 (D-005) — V4, V6, V7 e specs antigas dos motores
- 17/04/2026 (D-013) — V2 (aplicação retroativa após adoção do método DCV)
- 18/04/2026 (D-014) — método inteiro (todas as visões), após leitura consolidada dos 10 DCVs prévios

### `Princípio C.5` 🆕📌

**TabloFlow analisa sobre o dado informado, nunca decide por ele.** Princípio fundamental do método, formalizado no CONTEXT §9 Camada C durante a Sessão 1 do DCV-V1. O sistema preserva e classifica de forma auditável; não interpreta, não consolida silenciosamente, não invoca default que decida por alguém. Quando houver ambiguidade de comportamento entre "o sistema decide X" e "o sistema apresenta o caso para o usuário ver", a escolha correta é sempre a segunda. Aplicado como primeira lente em cada pendência de DCV.

### `Marco` 🆕📌

**Ponto de fechamento estrutural** que dispara o padrão ALINHA (D-142). Distinto de fechamento de bloco rotineiro. Definido por **3 critérios cumulativos** (todos precisam estar presentes):

1. Encerra uma **fase inteira** ou **subsistema de design** (não apenas um bloco ou sub-bloco)
2. A transição seguinte é para um **modo operacional diferente** (ex: Arquiteto → Claude Code · Fase 0 → Fase 1 · design → implementação)
3. Acumulou-se **≥ 3 decisões ou artefatos pendentes** de consolidação

Exemplos históricos: fechamento da Fase 0 (disparou `ALINHA-Fase-0→Fase-1`) · fechamento da Fundação-Design (disparou `ALINHA-Fundação-Design→F-MOT`).

Marcos futuros identificados: fechamento da Fase 1 inteira (após F-MOT · F-TRANS · F-EXP · F-BASE) → `ALINHA-Fase-1→Fase-2` · fechamento da Família A em Fase 2 → `ALINHA-Família-A→IA-Família-A` · fechamento do Módulo 1 inteiro → `ALINHA-M1→M2`.

**Não acionam ALINHA:** refino de DCV individual · sub-bloco de G-FUND · sessão de spec de visão · bloco F-MOT isolado · retrospectiva de bloco rotineiro. Esses usam kit D-033 isolado.

### `Padrão ALINHA` 🆕📌

**Sessão dedicada ao fechar Marco** (D-142). Complementar aos padrões D-019 + D-034 + D-033 + D-131 · não substitui. Envelopa D-033 como seu último sub-bloco.

**Escopo canônico · 4 sub-blocos sequenciais nomeados com letras gregas:**

- **α · Consolidação retrospectiva** — unificação de artefatos de múltiplas sessões anteriores em arquivo único coerente · eliminação de referências estruturais residuais · validação cross-cuts
- **β · Talk-through operacional** — transferência estruturada de contexto para o modo operacional seguinte · protocolo · pré-requisitos técnicos · situações de exceção · entregáveis concretos (prompts prontos)
- **γ · Formalização de decisões técnicas latentes** — produção de entradas D-XXX com rationale completo para decisões que ficaram implícitas nas sessões anteriores do Marco
- **δ · Kit de encerramento D-033** — aplicação integral do padrão D-033 · prompt de abertura tipicamente **dual** (d1 · modo operacional seguinte · d2 · retrospectiva do Arquiteto quando o modo seguinte concluir)

**Ordem:** α primeiro · δ último · β e γ intercambiáveis entre si. Mini status-check entre sub-blocos recomendado.

**Conteúdo decisional típico:** 0 decisões de negócio · 1-3 decisões técnicas puras (formalizações de γ) · 0 execuções de código (validação fica para a retrospectiva pós-modo-seguinte).

**Nomeação canônica:** `ALINHA-<Marco fechado>→<próximo modo>`. Exemplos: `ALINHA-Fase-0→Fase-1` · `ALINHA-Fundação-Design→F-MOT`.

**Aplicações históricas:**
- 1ª · Sessão Fase 0 → Fase 1 (retroativamente categorizada) · produziu D-130 · D-131 · D-132
- 2ª · `ALINHA-Fundação-Design→F-MOT` (21/04/2026) · produziu `spec_fundacao.md` consolidado + talk-through Claude Code + D-142

Detalhes operacionais em CONTEXT §11.1 · definição canônica em D-142.

---

## 2. Blocos de execução (ativos)

Um bloco é uma sessão de trabalho dedicada a um artefato específico. **Nunca misturar tipos** na mesma sessão (princípio B.1).

### `DCV-VN` 📌

Refino pelo Arquiteto do DCV prévio da visão N. Produz o DCV final em `/specs/dcv/dcv_vN.md`. Output vai para aprovação da Usuária antes de virar canônico.

### `DCV-OPN`

Equivalente do DCV para operações do Módulo 2 (TabloPrep). Ex: DCV-OP-FILTER, DCV-OP-DEDUP. Ainda não ativos — começam após Módulo 1 avançar na Fase 2.

### `ALINHA-<Marco>→<próximo>` 🆕📌

Sessão dedicada ao fechar Marco (D-142). Tipo transversal · não pertence a uma fase específica · aciona-se sempre que os 3 critérios cumulativos de Marco estão presentes (ver verbete `Marco` em §1). Escopo canônico · 4 sub-blocos sequenciais α · β · γ · δ (consolidação retrospectiva · talk-through operacional · formalização de decisões latentes · kit D-033). Envelopa D-033 como último sub-bloco · complementa D-131 (os 5 princípios continuam vigentes dentro de cada sub-bloco).

Nomeação com sufixo direcional: `ALINHA-Fase-0→Fase-1` · `ALINHA-Fundação-Design→F-MOT` · `ALINHA-Fase-1→Fase-2` · etc.

Aplicações históricas: 2 até 21/04/2026 (Fase 0 → Fase 1 retroativamente · Fundação-Design → F-MOT). Marcos futuros identificados: Fase 1 → Fase 2 (após F-MOT · F-TRANS · F-EXP · F-BASE) · Família A → IA-Família-A · Módulo 1 → Módulo 2.

Definição canônica em §1 (verbete `Padrão ALINHA`) + CONTEXT §11.1 + D-142.

### `G-FUND` 🆕📌

Gate de Fundação. Bloco único que consolida requisitos de motor, contratos, transversais e exportação a partir dos 10 DCVs aprovados. **Entrega única:** `spec_fundacao.md` consolidada. Bloqueia o início da implementação da Fase 1 até o escopo estar fechado. Definido pelo princípio A.1 + §3 do CONTEXT v2.

### `F-MOT` 🆕

Bloco de implementação dos motores da Fundação (`motor_upload.py` v2, `motor_base.py` v2). Executado em Claude Code a partir de prompt produzido pelo Arquiteto após G-FUND.

### `F-TRANS` 🆕

Bloco de implementação dos componentes transversais da Fundação (T-AGRUPA, T-DIAG, T-SEMA, T-EIXO, T-RANK, T-ACUM, T-ABC, T-PIVOT). Pode ser um bloco único ou subdivido por transversal — a decidir no G-FUND.

### `F-EXP` 🆕

Bloco de implementação da exportação Excel padrão — estrutura de abas comum, filtros automáticos, formato numérico consistente.

### `F-BASE` 🆕

Bloco de geração da base sintética de fundação multi-visão — cobre todos os casos que os motores da Fundação precisam tratar (POR_COLUNAS, POR_LINHAS, pré-agregadas, com nulos, cardinalidade alta, boolean disfarçado, etc.).

### `S-VN` 🆕📌

Spec da visão N. Contém as 3 seções obrigatórias: (a) contratos lógicos Pydantic, (b) regras de cálculo, (c) wireframe funcional. O wireframe é aprovado pela Usuária **antes** do código começar, mesmo vivendo no mesmo arquivo.

### `B-VN` 🆕

Geração da base sintética da visão N, com aba CASOS_ESPERADOS contendo gabarito auditado. Volume mínimo 50 linhas por aba (princípio B.3).

### `V-VN` 🆕 (reformulado em 23/04/2026 · D-155)

Implementação de `visao_vN.py`. Executado em Claude Code via prompt produzido pelo Arquiteto. Consome contratos da Fundação (MotorResult) e entrega VNResult padronizado. **Convenção Família A (pós-D-155):** produção do prompt + retrospectiva acontecem no **mesmo bloco Arquiteto** · sessão combinada (~1 sessão em vez de 2). 1ª aplicação: V-V2 (22/04/2026 · produziu D-151). 2ª aplicação: A-V2. Convenção válida desde V-V1. Revisável após Família A completa.

### `A-VN` 🆕 (reformulado em 23/04/2026 · D-155)

Implementação de `app_vN.py` (Streamlit) executando o wireframe funcional aprovado. Consome `visao_vN.py`. Precede **VV-VN** (Validação Visual acompanhada · D-156). Segue mesma convenção de sessão combinada de V-VN (D-155 · prompt + retrospectiva no mesmo bloco Arquiteto). Testes via `streamlit.testing.v1.AppTest` (convenção Família A · D-152).

---

## 3. Blocos descontinuados (apenas histórico)

Termos que aparecem em DECISIONS.md antigos e em artefatos `/legacy/`, mas que **não devem ser usados** no método atual.

### `B-NR` ❌

Descontinuado em 17/04/2026 (D-013). Era "regeneração de base sintética". No método atual, base que precisa ser refeita usa `B-VN` em nova iteração.

### `V-Nb` ❌

Descontinuado em 17/04/2026 (D-013). Era "correção/ajuste em código existente de visão". No método atual, visão pós-DCV nasce do zero; mudanças refletem no DCV → nova Spec → novo `visao_vN.py`.

### `N-Motores` ❌

Descontinuado em 17/04/2026 (D-011). Era "reescrita das specs dos motores". Absorvido primeiro pelo `G-MOT` (D-011) e depois pelo `G-FUND` (D-014), que tem escopo mais amplo.

### `G-MOT` ❌

Descontinuado em 18/04/2026 (D-014). Era "Gate de Motores" — auditoria dos motores após uma onda de DCVs. Absorvido e ampliado pelo `G-FUND`, que cobre também contratos, transversais e exportação.

### `N-VN` ❌

Descontinuado em 18/04/2026 (D-014). Era "reescrita completa de visão do zero". Redundante: toda visão pós-DCV já nasce do zero a partir do DCV aprovado — não existe "evolução" de visão pré-DCV.

### `V-0c` ❌

Descontinuado em 18/04/2026 (D-014). Era "correção pontual em motor". No método atual não existe correção pontual — motor inteiro é reescrito na Fase 1 a partir dos requisitos consolidados dos 10 DCVs.

### `T-XXX` ❌

Descontinuado em 18/04/2026 (D-014). Era "extração tardia de componente transversal quando a terceira visão reusasse a mesma lógica". No método atual, transversais são identificados no G-FUND (antes de qualquer visão ser implementada) e implementados em F-TRANS durante a Fase 1.

### `Onda padrão` ❌

Descontinuado em 18/04/2026 (D-014). Era o conjunto V2 → V4 → V7 → V6 → V10 como sequência inicial de DCVs. Substituído pela ordem lógica por famílias conceituais, que reflete dependência técnica em vez de prioridade estratégica.

### `Onda futura` ❌

Mesmo status de "onda padrão". Desnecessário no método atual porque os 10 DCVs são produzidos em uma única fase (Fase 0).

### `Bloco N` ❌

Convenção antiga de nomear blocos por ordem cronológica ("Bloco 8 = app_v2.py"). Substituída pela nomenclatura por tipo + visão (ex: A-V2 em vez de "Bloco 8").

---

## 4. Componentes transversais da Fundação

Identificados na leitura consolidada dos 10 DCVs prévios. Todos entram no escopo da Fase 1 e são implementados em `F-TRANS`.

### `T-AGRUPA` 📌

Consolidação por agrupadores antes do cálculo, com regra de agregação configurável (soma, média, máximo, mínimo, contagem). Usado por **TODAS** as visões **exceto V1 e V11** (que preservam registros individuais em vez de consolidar, para não apagar informação de auditoria crítica no confronto). Princípio universal nas 9 visões que consolidam: "consolidar primeiro, calcular depois" — aparece explicitamente em cada um dos DCVs prévios.

**Modo no-op validado** (V7 D-082 · V8 D-074 · V9 D-092): quando a base é declarada como Pré-agregada (1 linha por combinação de chaves), T-AGRUPA opera como no-op validado — motor verifica unicidade em volume completo e registra no Diagnóstico em vez de consolidar. Violação (Pré-agregado declarado mas duplicatas detectadas) gera bloqueio estrutural (W-V{N}-MODO-VIOLACAO).

**Média ponderada em tipo Relativa** (V7 D-083): em tipo Relativa, usuário pode declarar campo de peso opcional; motor aplica `Σ(valor × peso)/Σpeso` em vez de média aritmética. Default é aritmética com alerta forte sobre distorção potencial. Primeira visão a usar extensão; generalizável para V4 Modo 3 em evolução futura.

**Aplicação em V9 (D-092):** V9 estende o contrato T-AGRUPA para aceitar **regra de agregação independente por métrica** — contrato passa a aceitar dicionário `{metrica: regra}` em vez de regra única. Default declarado por tipo de medida: Aditiva → Soma · Não-aditiva → Média · Relativa → Média. 5 regras oficiais: Soma · Média · Máximo · Mínimo · Contagem (Contagem como caso especial que dispensa campo de medida, análogo V7 §4.7). Primeira consumidora com contrato multi-regra; F-TRANS (Fundação) absorve a extensão.

**Aplicação em V5 (D-102) · 8ª consumidora · semântica V5-específica em 3 modos · em nenhum modo V5 consolida valores:**

| Modo V5 | Quando aplicado | Comportamento |
|---|---|---|
| **No-op puro** | Granularidade da base = Individual (default declarado V5) | Passa o conjunto de observações adiante sem operar |
| **Validação de chave** | Granularidade da base = Consolidada por chave declarada | Verifica unicidade da chave declarada · gera warning estrutural W-V5-CHAVE-NAO-UNICA se duplicada |
| **Particionamento por Agrupador** | Modo Segmentado declarado (independente da granularidade) | Particiona observações por valor único do Agrupador · sem consolidar valores dentro do segmento |

A regra de agregação que define T-AGRUPA em V4/V7/V8/V9 (soma · média · máximo · etc) **não se aplica em V5** — V5 é estatística descritiva univariada e qualquer agregação de valores deformaria a distribuição observada (Σ ou média de 100 vendas de R$ 50 + 1 venda de R$ 5.000 vira 1 valor consolidado · IQR/DP/quartis perdem sentido). Aplicação canônica de **D-073** ("herança adaptada à natureza analítica") · V5 herda **a estrutura** do padrão "consolidação obrigatória pré-cálculo" (declaração explícita do modo · validação · T-AGRUPA aplicada · diagnóstico) sem herdar **o comportamento de consolidar valores**. **4ª aplicação consecutiva** do padrão "consolidação obrigatória pré-cálculo" (V8 D-074 · V7 D-082 · V9 D-092 · V5 D-102) — candidato muito forte à formalização efetiva no próximo ajuste do CONTEXT.

### `T-DIAG` 📌

Diagnóstico estrutural obrigatório. Aba padronizada no Excel exportado (**sempre posicionada como última aba** por regra transversal — D-017) + bloco no Resumo Executivo. Registra: inconsistências detectadas, ajustes aplicados pelo motor, impacto, volume afetado. Usado por **TODAS** as visões. Garante o princípio C.2 (nada silencioso).

### `T-SEMA`

Semântica maior-é-melhor / menor-é-melhor / neutro. Regra de interpretação que transforma o resultado matemático em leitura de negócio. Usado por V2, V3, V7, V9. Ex: custo caiu 10% → matematicamente negativo, semanticamente (com "menor é melhor") positivo. **Não aplicável a V8** (D-071) — presença/ausência não tem direção universal; ganhar 50 clientes e perder 30 pode ser ótimo (crescimento) ou péssimo (churn mascarado), depende do contexto. V8 apresenta leitura de ciclo de vida com faixas editáveis no Resumo Executivo (não semântica direcional).

**Aplicação em V7 (D-087):** V7 é sexta consumidora de T-SEMA. **T-SEMA afeta apenas visualização e ordem de apresentação, não cálculo.** Default Neutro, editável. Motor classifica simetricamente (Acima/Na Média/Abaixo com base em `|desvio_percentual|` ante Tolerância) independentemente da semântica declarada. Efeitos concretos: (1) mapeamento de cores canônico (maior-é-melhor → Acima em cor positiva do sistema; menor-é-melhor → Acima em cor negativa; Neutro → direção neutra); (2) ordem de apresentação no Bloco 2 Números-âncora (maior-é-melhor → maior desvio positivo primeiro; menor-é-melhor → maior desvio negativo primeiro); (3) rótulos descritivos neutros preservados ("maior desvio positivo", não "ponto forte") — coerente com disjunção entre cálculo e interpretação. Persistida em T-MODELO (padrão V2/V3/V8).

**Aplicação em V9 (D-093 · padrão "herança adaptada à natureza analítica" D-073):** V9 é sétima consumidora de T-SEMA com **contrato estruturalmente distinto das anteriores** — **por métrica (2-6 direções simultâneas) com efeito direto no cálculo**. A Direção declarada determina a ordem de ordenação de cada métrica (decrescente para Maior-é-melhor, crescente para Menor-é-melhor), que determina Posição → Score → Classificação. **Sem default, declaração obrigatória por métrica em E3** — única quebra do padrão "default declarado" no método V9 (§4.4 do DCV-V9), justificada pela gravidade da inversão (errar Direção inverte ranking 100%). Divergência vs V7 justificada por D-073: V7 tem 1 medida e pode abstrair T-SEMA do cálculo; V9 tem 2-6 métricas e precisa da Direção para ordenar cada uma. Efeitos concretos: (1) parâmetro estrutural do Passo 2 (ordenação por métrica); (2) Posição 1 destacada como "líder daquela métrica" independentemente da direção (mapeamento visual coerente em ambas); (3) ícone ↑/↓ na saída Excel indicando Direção declarada; (4) persistida em T-MODELO como par Métrica↔Direção. Contrato T-SEMA V9: lista `[metrica, direcao]` em vez de valor único. F-TRANS absorve a extensão. **Quadro comparativo de consumo T-SEMA:** V2/V3 (global, afeta interpretação) · V7 (global, **não afeta cálculo**) · V9 (**por métrica, afeta cálculo diretamente**).

### `T-EIXO` 🆕

Transversal formalizada da Fundação para **eixo sequencial ordenado com intervalo De/Até, sem preenchimento de lacunas**. Usado por **V3 e V8** (segunda consumidora ativa após refino DCV-V8 · D-071 a D-080). A V3 estabelece o padrão (DCV-V3 §4.4); V8 herda integralmente (DCV-V8 §4.3).

**Três tipos canônicos de eixo:**

| Tipo | O que é | Como o motor detecta | Ordem default |
|---|---|---|---|
| **Temporal** | Eixo com semântica de tempo | Reconhecedor de padrões cronológicos pt-BR/pt-EN herdado de D-026 (T-AGRUPA): datas ISO, datas pt-BR, nomes de meses em português e inglês, anos, tokens Q1/Q2/Q3/Q4, formatos "Jan/24" | Cronológica crescente |
| **Lógico/ordinal** | Eixo com ordem declarada no rótulo (etapas, níveis, fases) | Prefixo ou sufixo numérico no rótulo | Pelo prefixo/sufixo crescente; alfabética quando não detectado |
| **Manual** | Eixo sem ordem inerente detectável | Fallback | Ordem de primeira ocorrência na base |

**Default declarado pelo motor:** motor detecta padrões na amostragem e propõe tipo + ordem; usuário confirma ou edita em um clique (padrão D-024). Prioridade quando múltiplos padrões detectados: temporal > lógico/ordinal > manual.

**Ordem final sempre confirmada pelo usuário** — reordenação manual permitida sempre. Reordenação sobre eixo temporal/ordinal dispara **W-V3-EIXO-ORDEM-MANUAL**.

**Detecção de lacunas depende do tipo:**
- Temporal e ordinal com prefixo numérico → detecção automática (comparação com sequência canônica)
- Ordinal sem prefixo e manual → sem detecção (sem referência semântica)

**Intervalo declarado vs intervalo efetivo:** motor preserva separadamente o que o usuário declarou (em T-MODELO e Parâmetros) e o que aplicou após ajustes-limite (registrados como AJUSTE_LEVE no Diagnóstico). Quando diferem, aba Parâmetros lista ambos.

**Herança zero-duplicação:** reconhecedor pt-BR/pt-EN de D-026 (T-AGRUPA) serve ao tipo temporal de T-EIXO sem reimplementação.

Formalizado em **D-061** (transversal de Fundação, origem DCV-V3).

### `T-RANK` 🆕

Ranking determinístico com regra de desempate explícita. **Configurável** via parâmetro `regra_desempate` opcional (D-041). Default de 3 níveis, fixado pela V4:

1. Maior valor agregado primeiro (decrescente)
2. Em empate: concatenação dos agrupadores na ordem declarada pelo usuário, ordem alfabética crescente, case-insensitive, acentos normalizados
3. Em empate ainda: ordem de inserção da linha original

Tolerância para floating point: `1e-9` absoluto. Se tolerância resolve, não é empate real.

Usado por V1, V4, **V7**, **V9**, V10, **V11**. V11 usa T-RANK para ranquear candidatos por score de aderência quando o mesmo valor tem múltiplos candidatos.

**Aplicação em V7 (D-088 · padrão "herança adaptada à natureza analítica" D-073):** V7 é sexta consumidora. Critério de ordenação: **magnitude (módulo) do desvio percentual decrescente** — posição 1 no grupo é o elemento que mais se afasta da média em qualquer direção. Regra de desempate V7-específica em **4 níveis**:

1. `abs(desvio_percentual)` decrescente (magnitude)
2. `abs(desvio_absoluto)` decrescente (desempate por magnitude em unidades absolutas)
3. Nome do Elemento alfabético case-insensitive
4. Ordem de inserção original

Escopo **intra-grupo exclusivamente** — ranking global (cross-grupo) fora de escopo V7 (preserva posicionamento analítico de benchmarking interno). Elementos NULO_MEDIDA e em grupos Não aplicável não recebem ranking.

**Aplicação em V9 (D-096 · padrão "herança adaptada à natureza analítica" D-073):** V9 é sétima consumidora. Contrato com 2 contextos de uso:

**(a) Atribuição de Posição por Métrica (Passo 3 do pipeline §5.2 do DCV-V9):** **rank mínimo** — elementos com mesmo valor consolidado em uma métrica recebem mesma Posição (a menor disponível); elementos subsequentes recebem rank continuando a partir de `(quantidade_de_elementos_anteriores + 1)`. Equivalente ao `pandas.Series.rank(method='min')`. Empate é **preservado como fato analítico**, não desempatado artificialmente.

**(b) Desempate visual determinístico das linhas** (ordenação no Excel e tela) em **4 níveis**:

1. Score Consolidado crescente (menor = melhor posicionamento)
2. Variação Máxima de Posição crescente (elemento mais equilibrado primeiro quando scores empatam)
3. Nome do Identificador alfabético case-insensitive
4. Ordem de inserção original

Tolerância floating point 1e-9.

**Novo escopo V9** adicionado ao enum `escopo` do contrato T-RANK: `cross_elementos_dentro_do_agrupador` (modo Segmentado V9) — distinto de `intra_grupo` (V7, onde Grupo é campo dedicado formando unidade Elemento+Grupo) e `global` (V4/V10/V11, sem segmentação). Modo Global V9 usa escopo `global` existente; modo Segmentado V9 usa o novo `cross_elementos_dentro_do_agrupador`.

**Empate no score consolidado não é desempatado para classificação** — dois elementos com mesmo score podem **ambos** ser Líderes (se caem no top 20%). Desempate é puramente cosmético para ordenação visual.

Warning padrão: **W-V{N}-EMPATE** (para V7: **W-V7-RANK-EMPATE** · para V9: **W-V9-RANK-EMPATE**) — lista casos com resolução por regra secundária ou terciária.

Formalizado em **D-041** (transversal de Fundação, origem DCV-V4).

### `T-ACUM`

Acumulado progressivo monotônico sobre ranking. Usado por V4 (modo 2 e 3) e V10. Requer que T-RANK esteja aplicado primeiro.

### `T-ABC`

Classificação A/B/C por limiares de acumulado. Default declarado: A ≤ 80%, B ≤ 95%, C > 95% (limiares editáveis pelo usuário — D-040). Usado por V4 (modos 2 e 3) e V10 (view especializada). Regra de corte: o item que faz o acumulado atingir ou ultrapassar o limiar pertence à faixa correspondente. No Modo 3 da V4, limiares são **globais** (mesmos para todas as medidas) para preservar comparabilidade da divergência.

### `T-PIVOT` 🆕

Pivot automático POR_LINHAS → POR_COLUNAS quando informação discriminadora está em coluna. Usado por V2, V3, V4. Dispara quando o motor detecta estrutura POR_LINHAS na configuração do usuário.

**Três semânticas formalizadas de pivot** (não é extensão estrutural — motor opera sobre dimensão em coluna discriminadora qualquer; as três semânticas formalizam o vocabulário):

- **V2 · Modo 4** (D-026) — pivot de **estados** empilhados (ex: `Periodo` com Jan/24 e Jan/25 discriminando a mesma medida). Parâmetro "valores selecionados" permite ao usuário escolher quais estados pivotar.
- **V4 · pivot multi-medida** (D-039) — pivot de **medidas** empilhadas (ex: `Tipo_Medida` com Receita, Custo, Margem). Requisito para G-FUND.
- **V3 · pivot de pontos do eixo** (D-062) — pivot de valores do **eixo sequencial** empilhados (ex: `Mes` com Jan, Fev, Mar). Bloco "Seleção de pontos do eixo em POR_LINHAS" ativado quando coluna discriminadora tem 10+ valores únicos.

### `T-DUAL` 🆕

Extensão do `motor_upload` para aceitar entrada em modo dual, exigida pelas visões **V1 e V11** da Família A (Módulo 1). Aceita duas estruturas:

- **Estrutura A · Dois arquivos distintos** — usuário sobe 2 arquivos separados; sistema lista abas de cada um; usuário escolhe uma aba de cada arquivo como Origem e Comparado
- **Estrutura B · Um único arquivo** — usuário sobe 1 arquivo; sistema lista todas as abas; usuário escolhe 2 abas do mesmo arquivo

Produz `UploadResult` unificado com referência aos dois lados nomeados (defaults Origem/Comparado, editáveis). **Dados empilhados em uma única aba com coluna discriminadora não são escopo do T-DUAL** — exigem RESHAPE prévio no Módulo 2.

Formalizado em **D-018**. Escopo estendido a V11 em **D-047**.

### `T-MODELO` 🆕

Salvar e aplicar configuração declarada como modelo reutilizável. Padrão estrutural de produto aplicado a **TODAS** as 11 visões (CONTEXT §13.3). O modelo persiste apenas a **configuração lógica** (agrupadores, campos, regras, tolerâncias, modos de match) — não persiste dado fonte. O usuário aplica o modelo em nova análise sobre novas bases e os campos da configuração são pré-preenchidos automaticamente, reproduzindo o mesmo comportamento determinístico (princípio C.1).

Formalizado em **D-015** (promovido de padrão visual do Figma Make para padrão estrutural de produto).

### `T-FUZZY` 🆕

Componente transversal da Fundação para **similaridade textual entre strings**. Usado no cálculo do score de aderência contextual da V11 — quanto mais um texto composto da Base Investigada "se parece" com o texto composto da Base de Busca, maior o score do par candidato. Disponível para V1 via P-V1-02-Evo quando ativado (zero retrabalho).

**Algoritmo (híbrido):**

- **Similaridade por trigramas de caracteres** — overlap de sequências de 3 caracteres entre os dois textos normalizados
- **Presença de tokens-chave** — sequências numéricas ≥ 4 dígitos e sequências alfabéticas maiúsculas ≥ 3 caracteres consecutivos; tokens presentes nos dois lados aumentam score

**Pesos internos fixos**, calibrados na implementação da Fundação, **não expostos ao usuário** (complexidade encapsulada na transversal).

**Normalização prévia interna** (invisível ao usuário, registrada no Diagnóstico da V11 em linha informativa única):

- lowercase
- remoção de acentos
- remoção de caracteres não-alfanuméricos exceto espaço

**API pura:** `(texto_A, texto_B) → score ∈ [0, 1]`, determinística (C.1).

Transformações textuais **semânticas** (unificação de abreviações, stop-words, regex) ficam **fora** de T-FUZZY — são operação declarada do usuário, território de M2.NORMALIZE (ver §5.V11 "Higiene textual vs NORMALIZE").

Status: **confirmado** como transversal da Fundação em **D-052** (promove D-050). Formalizado inicialmente em D-050 como candidato, confirmado após refino do DCV-V11.

### `T-CONCAT` 🆕📌 (Fundação confirmada · D-135)

Componente transversal fundamental confirmado na **G-FUND parte 1** via decisão D-135. Composição/concatenação declarada de múltiplos campos-fonte em um campo textual único. Implementação em F-TRANS.

**Dimensões consolidadas:**
- Até **3 campos-fonte** por composição
- **Separador fixo: espaço**, visível no preview da configuração
- **Assimetria permitida** — lados podem compor com quantidades diferentes de campos-fonte (V11)
- **Tratamento de nulos:** campos nulos são pulados; se todos os componentes são nulos, resultado é string vazia (warning W-V11-COMP-CAMPOS-NULOS)

**Posicionamento arquitetural (D-135):** Transversal puro da Fundação. V11 consome no MVP. Estrutura apta para renomeação/extração futura para operação M2.CONCAT sem reescrita (zero duplicação arquitetural · coerente com intenção de D-053). Especificação completa em `spec_fundacao.md` parte 2 · seção F.

**Consumidores:** V11 MVP (Família A) · M2.CONCAT futuro (herdará código pronto).

Formalizado inicialmente em **D-053** como candidato · posicionamento confirmado em **D-135** (Fundação).

### `M2.STACK` (movido para M2 · D-135 · fora do escopo Fundação)

Operação M2 confirmada via decisão **D-135** em G-FUND parte 1. Empilhamento de múltiplas abas estruturalmente idênticas em uma única aba com coluna discriminadora adicional contendo o nome da aba de origem. **Fora do escopo da Fundação.**

**Posicionamento arquitetural (D-135):** Operação M2 futura. Fase 1 não implementa. V3 · V6 · V8 mantêm multi-aba como roadmap pós-MVP conforme declarado nos DCVs aprovados (P-V3-01-Evo · P-V8-01-Evo · P-V6-02-MULTIABA-Evo). Implementação no M2 futuro com contexto completo do Módulo 2.

**Consumidores futuros declarados (mantidos · sem mudança):**
- V3 · P-V3-01-Evo (eixo sequencial multi-aba)
- V8 · P-V8-01-Evo (eixo sequencial multi-aba · rastreamento de presença)
- V6 · P-V6-02-MULTIABA-Evo (matriz de cruzamento multi-aba)

**Razão da decisão:** (1) Todos os consumidores em roadmap · nenhum MVP · sem urgência de entrega. (2) Implementação complexa (detecção estrutural · tratamento de divergência · vocabulário · warnings específicos) adicionaria 3-4 semanas à Fundação sem justificativa de negócio. (3) DCVs de V3/V6/V8 já declararam multi-aba como fora do escopo MVP · decisão ratifica posicionamento anterior.

Formalizado como candidato em **D-063** (V3) · **D-074** (V8) · **D-111** (V6) · posicionamento confirmado como M2 em **D-135**.

---

## 5. Conceitos de produto (V2 e transversais)

### `Estado` 📌⚠️

**Definição rigorosa:** referência do dado dentro de um contexto comparativo. **Sempre dois na V2.**

**O que NÃO é:**

- ❌ Não é valor (valor é o que se mede)
- ❌ Não é agrupador (agrupador é a dimensão)
- ❌ Não é filtro (filtro é o recorte)

**Exemplos:** Orçado / Realizado · Previsto / Executado · Antes / Depois · Meta / Resultado · Jan/24 / Jan/25

**Como aparece no upload:**

- Em **POR_COLUNAS** — cada estado é uma coluna distinta (ex: `Receita_Jan24` e `Receita_Jan25`)
- Em **POR_LINHAS** — os estados são valores de uma coluna discriminadora (ex: coluna `Periodo` com `"Jan/24"` e `"Jan/25"`)

### `Agrupador` 📌⚠️

Dimensão que define o nível da análise. **Pode ser um ou vários, combinados livremente.** Ex: Filial, Região, Conta Contábil, Produto.

**Diferente de filtro.** Agrupador define como a análise é segmentada (uma linha de saída por combinação). Filtro reduz quais linhas entram na análise.

### `Filtro` 📌⚠️

Recorte de **visualização**. Não muda a estrutura da análise, só reduz o conjunto exibido. Ex: "ver apenas Região Sul" não cria uma análise diferente — apenas exibe um subconjunto.

### `Semântica` 📌

Regra de interpretação informada pelo usuário. Três opções:

- **Maior é melhor** (positivo quando aumenta) — ex: Receita
- **Menor é melhor** (positivo quando diminui) — ex: Custo
- **Neutro** (apenas informar) — ex: Headcount

### `POR_COLUNAS`

Estrutura de entrada onde os dois estados estão em **colunas distintas** da mesma base. Ex: a base tem coluna `Receita_Orcado` e coluna `Receita_Realizado` — cada linha já contém os dois estados lado a lado.

### `POR_LINHAS`

Estrutura de entrada onde os estados aparecem como **valores de uma coluna discriminadora**. Ex: a base tem coluna `Cenario` com valores `"Orcado"` e `"Realizado"`, e coluna `Receita` com o valor. A V2 precisa pivotar (via T-PIVOT) antes de comparar.

### `Modo 4` (do motor_upload)

Caso especial em POR_LINHAS quando a coluna discriminadora tem **mais de 2 valores** (ex: "Jan", "Fev", "Mar", "Abr"). A V2 só compara 2 estados — então a UI pede ao usuário para escolher quais 2 antes de processar.

### `Tipo de campo` 📌

Classificação técnica que determina como a V2 calcula e classifica. **Consolidado em 4 tipos** pela D-025 (substitui tabela anterior de 7 tipos):

| Tipo | Cálculo | Consolidação por agrupador | Exemplos |
|---|---|---|---|
| **Numérico aditivo** | Diferença e variação % | Soma (default), via T-AGRUPA configurável (média, máx, mín, contagem) | Receita, custo, quantidade, volume, dias trabalhados, headcount acumulado |
| **Numérico relativo** | Diferença e variação % | **Default declarado**: média simples, com opção de média ponderada por campo ou não consolidar (D-024) | Margem %, taxa de conversão, índice de eficiência, NPS, score |
| **Numérico não-aditivo** 🆕 | Diferença e variação % | **Default declarado**: média simples, com opção de média ponderada ou não consolidar | Estoque pontual, saldo bancário, headcount em data específica, preço unitário |
| **Estado/Situação** | Sem aritmética; comparação textual ("mudou"/"manteve") | Contagem por categoria | Status de pedido, categoria de produto, classificação manual |

**Princípio de consolidação** (D-025): tipos numérico relativo e não-aditivo ativam UI de "Como consolidar?" (D-024) com defaults declarados. Tipo Estado/Situação tem fluxo simplificado sem semântica nem cálculo numérico. Tratamento de ambiguidade (motor sugere tipo provável, usuário confirma) entra como requisito da Spec, não detalhe do DCV.

Vocabulário base (4 tipos) é candidato a herança para outras visões com campo numérico configurável (V3, V4, V5, V6, V7, V8, V9, V10).

### `Eixo sequencial` (V3, V8)

Campo que define a sequência ordenada dos pontos analíticos. Pode ser:

- **Temporal** — datas, meses, trimestres
- **Lógico / ordinal** — etapas, ciclos, fases
- **Manual** — ordem definida pelo usuário

O motor respeita a ordem final confirmada pelo usuário (a IA pode sugerir, o usuário pode ajustar).

### `Classe ABC` (V4 modos 2 e 3, V10) 🆕

Classificação por acumulado progressivo sobre ranking decrescente. **Default declarado** (D-040): A até 80%, B de 80% a 95%, C acima de 95% — limiares editáveis pelo usuário. Usado para priorização, gestão de portfólio, leitura de concentração.

**V10 (view especializada) · apresentação dicotômica** consome T-ABC com os mesmos defaults de D-040 mas **colapsa Classes B e C em "Demais itens"** na apresentação (tela, Resumo Executivo, aba Análise Principal do Excel):

- **Classe A (vitais)** — itens até o limiar A (80% por default)
- **Demais itens** — tudo além do limiar A (colapso de B+C)

Só o limiar A é editável pela usuária em V10. Limiar B fica oculto da UI e fixado internamente em 100%. Usuária que precisa ver a distribuição A/B/C completa é redirecionada a V4 Modo 2 via microcopy explícito. Zero duplicação de lógica — V10 é view sobre V4 Modo 2 (D-035, D-045).

**No Modo 3 da V4**, limiares são globais (mesmos para todas as medidas selecionadas) — preserva comparabilidade da divergência entre medidas.

### Seção 5.V4 · Conceitos específicos da V4 🆕

#### `Medida` (V4) 📌

Campo numérico analisado na V4. Substitui "campo" no vocabulário V2 para enfatizar a natureza da análise (composição de uma medida sobre um total). Herda a taxonomia de 4 tipos de D-025.

#### `Valor Agregado` (V4) 📌

Resultado da consolidação por agrupador. Sempre o ponto de partida do cálculo de participação. Nunca é calculado sobre dados brutos — primeiro consolida, depois calcula.

#### `Total Geral` (V4) 📌

Soma dos valores agregados da medida. Base do cálculo de participação: Participação = Valor Agregado ÷ Total Geral × 100. Quando Total Geral = 0, motor aplica **bloqueio adaptativo por causa** (D-043): base toda nula, cancelamento positivo/negativo, ou outra razão — cada caso com microcopy específico.

#### `Participação` (V4) 📌

Razão Valor Agregado ÷ Total Geral expressa em percentual. Conceito central da V4. Só faz sentido matemático quando Total Geral ≠ 0 e quando a medida é somável (aditiva) — tipos relativo e não-aditivo ativam bloco de default declarado (D-036).

#### `Participação Acumulada` (V4) 📌

Soma progressiva das participações individuais na ordem do ranking decrescente. Insumo da Classe ABC.

#### `Medida de Referência` (V4 Modo 3) 🆕📌

Medida que desempenha **3 papéis** no Modo 3 (D-042):

1. Ordenação visual na tela e Excel
2. Eixo de leitura orientadora do resultado
3. Eixo de comparação par-a-par para a classificação de divergência

Default: primeira medida selecionada na E3. Editável pelo usuário.

#### `Divergência` (V4 Modo 3) 🆕📌

Classificação composta em dois níveis (D-042):

**Par-a-par contra medida de referência:**

| Situação | Classificação |
|---|---|
| Mesma classe da referência | Igual |
| 1 nível de diferença | Divergente |
| 2 níveis de diferença | Alta divergência |
| Ref tem classe, outra `—` | Ausente na [nome_medida] |
| Ref `—`, outra tem classe | Ausente na medida de referência |
| Ambas `—` | Elemento fora do Modo 3 |

**Síntese geral do elemento** (gap máximo entre classes):

- gap = 0 → Igual
- gap = 1 → Divergente
- gap ≥ 2 → Alta divergência
- Algum `—` → Ausência parcial

#### `Classificação da medida` (V4) 🆕🔧

Campo do contrato técnico da V4 aplicado a cada registro (D-038):

| Contrato técnico | Exibição ao usuário |
|---|---|
| `VALOR_VALIDO` | (omitido — caso normal) |
| `VALOR_NEGATIVO` | "Valor negativo" |
| `NULO_MEDIDA` | "Valor nulo na medida" |

Nulo em **agrupador** (diferente de nulo na medida) vira rótulo `(sem valor)` na coluna do agrupador — não é categoria em `classificacao_medida`, é tratamento na dimensão.

#### `Seleção de medidas em POR_LINHAS` (V4) 🆕📌

Bloco da E2 que ativa quando coluna discriminadora POR_LINHAS tem 3+ valores únicos na V4 (D-039). **Não é o "Modo 4" da V2** — lógica diferente, vocabulário próprio para evitar colisão:

| Modo V4 | Seleção mínima | Default declarado |
|---|---|---|
| 1 | 1 medida | Primeira da ordenação inteligente |
| 2 | 1 medida | Primeira da ordenação inteligente |
| 3 | 2 ou mais | Todas pré-selecionadas |

Ordenação inteligente herdada de D-026. Requer extensão de T-PIVOT para pivot multi-medida (D-039).

#### `Leitura de concentração` / `Leitura de coerência` (V4) 🆕

Frases descritivas do Bloco 5 do Resumo Executivo (D-044), baseadas em critérios matemáticos explícitos:

**Leitura de concentração** (Modos 1/2) baseada em % do total que os top 20% dos elementos representam:
- Concentrada (default): > 80%
- Equilibrada (default): 40%-80%
- Pulverizada (default): < 40%

**Leitura de coerência** (Modo 3) baseada em % elementos com classificação "Igual":
- Coerência alta (default): > 70%
- Coerência média (default): 40%-70%
- Coerência baixa (default): < 40%

Faixas **editáveis** em "Configurações avançadas" da E5. Microcopy explícito informa que edição não afeta cálculos principais — só a frase de síntese. W-V4-LEITURA-CUSTOM registra customização.

---

### Seção 5.V10 · Conceitos específicos da V10 🆕

#### `Vitais` / `Classe A (V10)` 📌🆕

Itens que concentram valor até o limiar A no acumulado progressivo (default 80%). Correspondem exatamente à Classe A de V4 Modo 2 (D-040), mas recebem rótulo explícito "Vitais" em V10 para reforçar a narrativa Pareto ("poucos vitais × muitos triviais"). Expostos em disclosure expandido por default na microanálise e em aba dedicada do Excel. D-045.

#### `Demais itens` 📌🆕

Rótulo V10 para o colapso das Classes B + C em uma única categoria (tudo acima de 80% acumulado, ou acima do limiar A efetivo). V10 não mostra B e C separadamente — o limiar B é fixado internamente em 100% e oculto da UI. Usuária que precisa da distribuição A/B/C completa é redirecionada para V4 Modo 2 via microcopy explícito. Exposto em disclosure recolhido por default, com contagem e % sempre visíveis no cabeçalho. D-045.

#### `Curva Pareto` (V10) 🆕

Visualização principal da V10, ocupa largura total no topo da microanálise. Combo chart clássico:
- Barras (eixo Y esquerdo) — valor individual em ordem decrescente
- Linha (eixo Y direito, 0-100%) — acumulado monotônico
- Linha horizontal pontilhada no limiar A
- Linha vertical pontilhada no ponto de cruzamento
- Regiões coloridas Vitais × Demais

Aceita cardinalidade configurável (default 50 barras individuais; itens além são agregados em barra "Demais" visualmente). Tabela abaixo sempre preserva todos os itens. No Excel, gráfico nativo via openpyxl (requisito novo para F-EXP). D-045.

#### `Limiar A` (V10) 📌🆕

Único limiar editável em V10 (default 80%). Define o corte entre Vitais e Demais itens. Limiar B existe no T-ABC consumido por baixo mas é fixado em 100% e não exposto na UI da V10. Honra padrão "default declarado" (C.5). D-045.

#### `Fronteira` (V10) 🆕

Último item da Classe A + os N próximos fora da Classe A (default N=3). Útil analiticamente para avaliar se o corte é apertado: diferença entre acumulado do último vital e do primeiro não-vital. Aparece no Bloco 4 do Resumo Executivo. D-045.

#### `Leitura de Corte` (V10) 🆕

Leitura secundária V10-específica do Bloco 5 do Resumo Executivo (ao lado da Leitura de concentração herdada de D-044). Classifica a diferença em pontos percentuais no acumulado entre último vital e primeiro não-vital:

- **Corte folgado** (default): ≥ 2 pp
- **Corte apertado** (default): < 2 pp
- **Empate exato**: = 0

Faixas editáveis em "Configurações avançadas" da E4. Afeta apenas a frase de síntese, não os cálculos. W-V10-CORTE-APERTADO dispara na faixa "apertado". D-045.

#### `Cardinalidade visual do gráfico Pareto` (V10) 🆕🔧

Parâmetro da configuração V10 que limita quantas barras individuais aparecem no gráfico Pareto (default 50). Itens além do limite aparecem agregados em barra única "Demais" na visualização, mas a curva acumulada sempre vai até 100% e a tabela/Excel sempre mostram todos os itens individualmente. Editável em "Configurações avançadas" da E4. W-V10-CURVA-TRUNC registra quando o limite foi acionado. D-045.

#### `Modelo cross-visão` (T-MODELO, view especializada) 🆕📌

Modelo salvo em uma visão que faz par de view especializada (V4 Modo 2 ↔ V10 hoje; V2 ↔ V1 via T-DUAL futuro) é aplicável na visão-par via mapeamento declarado. Ao aplicar cross-visão, diálogo de confirmação lista explicitamente:

- **Parâmetros transferidos** — os comuns
- **Parâmetros com default da visão-destino** — os específicos da origem sem equivalente
- **Parâmetros descartados** — os específicos da origem não aplicáveis

Aplicação intra-visão não dispara diálogo. Modelos de V4 Modo 1 ou Modo 3 **não** se convertem com V10. Warning W-V10-MODELO-CONVERTIDO (simétrico em V4) registra conversão. D-046 (transversal §13.4).

---

### Seção 5.V11 · Conceitos específicos da V11 🆕

**Status:** consolidada após aprovação do DCV-V11 (19/04/2026, 2 sessões de refino). Substitui a versão preliminar registrada na sessão de abertura V11.

#### `Conciliação por Aderência` 📌🆕

Nome canônico da V11. Terceira visão da Família A que confronta duas bases quando **não há chave confiável** para relacionar registros — o elo analítico é **valor + contexto textual** (histórico, documento, data). Par conceitual autônomo de V1 (Conciliação de Bases, com chave). Motor probabilístico com arquitetura de dois passes, oposto ao motor determinístico de V1. D-047 · dcv_v11.md §1.

#### `Arquitetura de dois passes texto→valor` 📌🆕

Contrato analítico canônico da V11. Ordem fixa, sem configuração (determinismo C.1):

1. **Passe 1 · Por texto, confere valor** — para cada registro da Base Investigada, calcula scores de aderência textual contra a Base de Busca; se melhor score ≥ Limiar P1, confere valor. Valor dentro da tolerância → Conciliado pleno; valor fora → Divergência de valor.
2. **Passe 2 · Por valor, com texto complementar** — sobre resíduos do Passe 1, busca candidatos por valor dentro da tolerância. Se há candidato, calcula score textual entre eles. Score ≥ Limiar P2 → Conciliado por valor; score < Limiar P2 → Pareamento frágil.

Resíduos após os dois passes → Sem par.

Estratégia de alocação em cada passe: **guloso com ordem por "melhor score disponível"** — empate resolvido por T-RANK. Global ótimo (algoritmo Húngaro) fica como P-V11-02-Evo. D-051.

#### `Taxonomia de 5 categorias` 📌🆕

Resultado estruturado da V11, emerge da arquitetura de dois passes:

| # | Categoria | Passe de origem | Condição |
|---|---|---|---|
| 1 | Conciliado pleno | Passe 1 | score texto ≥ Limiar P1 · valor dentro da tolerância |
| 2 | Divergência de valor | Passe 1 | score texto ≥ Limiar P1 · valor fora da tolerância |
| 3 | Conciliado por valor | Passe 2 | valor dentro da tolerância · score texto ≥ Limiar P2 |
| 4 | Pareamento frágil | Passe 2 | valor dentro da tolerância · score texto < Limiar P2 |
| 5 | Sem par | — | sem correspondência nos dois passes |

Análoga em papel às 6 classes estruturais da V1 — resultado classificado, auditável, sem síntese imposta. KPI principal da V11 **decompõe taxa de pareamento pelas categorias** (não sintetiza). D-051 · dcv_v11.md §5.2.

#### `Score de aderência` 📌🆕

Grau de semelhança textual entre texto composto da Base Investigada e texto composto de um candidato da Base de Busca. Valor em [0, 1], calculado pela transversal T-FUZZY (algoritmo híbrido trigramas + tokens-chave, pesos internos fixos, normalização encapsulada).

**Agregação entre campos contextuais:** scores parciais por par de campos, agregados com **média ponderada**. Pesos entre campos têm default declarado (heurística de distintividade — maior cardinalidade relativa → maior peso), editáveis com slider. Warning W-V11-PESOS-CUSTOM registra customização. dcv_v11.md §4.4.

#### `Limiar P1` · `Limiar P2` 📌🆕

Dois limiares **independentes** do score de aderência, com default declarado, editáveis:

- **Limiar P1 · default 0,70** — score mínimo para "evidência textual forte o suficiente para guiar a busca de valor" no Passe 1
- **Limiar P2 · default 0,30** — score mínimo para "evidência textual mínima complementando a correspondência de valor" no Passe 2

Editáveis independentemente. Warnings W-V11-LIMIAR-P1-CUSTOM e W-V11-LIMIAR-P2-CUSTOM registram customização no Diagnóstico. D-051 · dcv_v11.md §4.4.

#### `Aderência contextual` 📌🆕

Termo conceitual usado em microcopy ao usuário para se referir ao score de aderência. Diferente do score (número), a aderência contextual é **grau qualitativo de evidência** — "evidência forte", "evidência complementar", "sem evidência". Traduzida no produto através das 5 categorias. D-049 · dcv_v11.md §2.

#### `Mapeamento semântico de valor` 🆕🔧

Declaração do usuário sobre **qual coluna de uma base representa o mesmo fato financeiro que qual coluna da outra**, considerando dualidade (ENTRADAS/SAIDAS ↔ DEBITO/CREDITO), valor único ↔ dualistas, e polaridade (mesma ou invertida).

**4 combinações estruturais declarativas:**

| Combinação | Lado A | Lado B |
|---|---|---|
| Dual × Dual | ENTRADAS/SAIDAS | DEBITO/CREDITO |
| Dual × Único | ENTRADAS/SAIDAS | VALOR_LIQUIDO |
| Único × Dual | VALOR | DEBITO/CREDITO |
| Único × Único | VALOR_A | VALOR_B |

Polaridade (mesma/invertida) declarada por correspondência. Default declarado via heurística (nomes de coluna + distribuição de sinais); editável antes da execução. Peça central da V11 e **ausente em V1** (em V1, ligação primária é chave). Regra de dualidade (múltiplas correspondências via mesmo mapeamento) é **P-V11-05-Evo**. Warning W-V11-MAP-INFERIDO. dcv_v11.md §4.1.

#### `Composição de campos contextuais` 🆕🔧

Declaração pelo usuário de que um campo contextual de uma base corresponde à **concatenação de N campos da outra base**. Caso típico: `HISTORICO` contábil vs `OPERACAO + DOCUMENTO + PREFIXO/TITULO` financeiro.

**Escopo V11 MVP:**

- Até 5 campos contextuais por lado
- Até 3 campos-fonte por composição
- Separador fixo: espaço
- Assimetria permitida entre lados
- Nulos pulados (composição se reduz)

Implementado via **T-CONCAT candidato** (ver §4); código estruturado para extração futura como transversal da Fundação ou operação M2. Warnings W-V11-COMP-CAMPOS-NULOS e W-V11-SEM-CONTEXTO. D-053 · dcv_v11.md §4.2.

#### `Tolerância com papel duplo` 🆕🔧

Parâmetro único de tolerância absoluta (herança direta de V1 · P-V1-05), default zero, configurável por campo de valor. Em V11, **um só parâmetro exerce dois papéis** declarados em microcopy:

- **No Passe 1:** classifica match textual em "Conciliado pleno" (valor dentro) ou "Divergência de valor" (valor fora)
- **No Passe 2:** define o critério de "mesmo valor" para a busca por valor

Microcopy da configuração: "Tolerância aplicada: tanto na checagem de valor após match textual quanto na busca por valor entre os registros sem par textual. Valores típicos: 0,00 para dados contábeis; 0,50 a 2,00 para conciliação bancária."

Warning **W-V11-TOL** é **material** (não só informativo): registra soma da diferença absorvida + lista de casos no Diagnóstico. Tolerância percentual é P-V11-03-Evo. dcv_v11.md §4.3.

#### `Ponte de Conciliação V11` 🆕🔧

Aba **opcional** da V11, **complementar aos pareamentos** (não critério de fechamento da análise, diferente da Ponte de V1). Aparece apenas quando o usuário declara os 4 campos de saldo na etapa "Reconciliação de saldo" da configuração: saldo anterior Origem · saldo anterior Comparado · saldo final Origem · saldo final Comparado.

**Estrutura em 3 blocos** (herdada do caso-referência Protheus × Safra):

- **Bloco 1 · Diferença de saldo anterior** (Origem − Comparado)
- **Bloco 2 · Impacto líquido dos movimentos únicos** (soma "só em Origem" + soma "só em Comparado")
- **Bloco 3 · Conferência** (Diferença real − Diferença esperada; precisa zerar)

Síntese de 3-4 linhas aparece também no Resumo Executivo (seção 5B). Quando saldos não declarados: aba omitida, bloco omitido, Diagnóstico registra "Ponte não incluída — saldos não declarados" (sem conotação de dado faltando — é escolha legítima). Warning W-V11-PONTE-RESIDUO dispara se Bloco 3 não zera. Referência a coluna de saldo é P-V11-04-Evo. dcv_v11.md §4.6, §6.6.

#### `Higiene textual vs NORMALIZE` 🆕📌

Distinção aplicada ao Princípio C.5. A V11 lida com normalização textual em dois níveis:

- **Higiene básica** (lowercase, remoção de acentos, remoção de caracteres não-alfanuméricos) — encapsulada em **T-FUZZY**, aplicada invisivelmente antes do score. Não é decisão analítica, é "como o algoritmo lê". Diagnóstico registra em linha informativa única.
- **Transformações semânticas** (unificação de abreviações declaradas, remoção de stop-words, substituição por regex, truncamento de campo) — decisão analítica que **transforma o conteúdo**. Território natural de **M2.NORMALIZE** (operação candidata do Módulo 2 futuro). V11 **não** absorve nativo no MVP.

Microcopy no Diagnóstico (Seção 6 da aba) orienta analista a considerar M2.NORMALIZE futuro quando há alta incidência de "Pareamento frágil" indicando padronização textual inconsistente. Não há sugestão preventiva na configuração. dcv_v11.md §9.

---

### Seção 5.V3 · Conceitos específicos da V3 🆕

**Status:** consolidada no refino do DCV-V3 (19/04/2026, sessão única de 13 pendências). Primeira visão da **Família B · Sequência**.

#### `Família B · Sequência ao longo de eixo ordenado` 📌🆕

Segunda família conceitual do Módulo 1 a ser implementada. Agrupa V3 (rastreia valor ao longo do eixo) e V8 (rastreia presença/ausência ao longo do eixo). Visões autônomas — não há view especializada entre elas — unidas pelo consumo de T-EIXO. Vocabulário declarativo autossuficiente em cada visão, sem menção cruzada em interface operacional. Precedente do padrão: Família A V11↔V1 (D-058). D-060.

#### `Análise Sequencial` 📌🆕

Nome canônico da V3. Primeira visão da Família B e **primeira consumidora de T-EIXO** da Fundação. Responde "como um valor evoluiu ao longo de uma sequência ordenada?". Dois modos: Simples (um núcleo acompanhado) e Comparativo (dois núcleos Origem × Comparado em cada ponto). D-060 · dcv_v3.md §1.

#### `Ponto do eixo` 📌🆕

Cada valor único do eixo sequencial após pivot e ordenação. Unidade atômica da sequência V3. Granularidade-base do resultado: 1 linha por combinação de **agrupador + ponto do eixo**. Termo unificado da Família B (V8 também opera sobre pontos do eixo, por presença em vez de valor). D-061 · dcv_v3.md §4.4.

#### `Tipo do eixo` 📌🆕

Três tipos canônicos declarados na configuração:

- **Temporal** — semântica de tempo (data, mês, ano, período); motor detecta via reconhecedor pt-BR/pt-EN herdado de D-026
- **Lógico/ordinal** — ordem declarada no rótulo (Etapa 1, Fase 3, 1º Trimestre); motor detecta prefixo ou sufixo numérico
- **Manual** — sem ordem inerente detectável; motor não infere, usuário declara ordem

Default declarado pelo motor com prioridade temporal > ordinal > manual quando múltiplos padrões detectados. Fallback manual quando detecção falha. Warning W-V3-EIXO-TIPO-INFERIDO registra aceitação sem edição. D-061 · dcv_v3.md §4.4.

#### `Coluna discriminadora do eixo` 🆕🔧

Em POR_LINHAS, a coluna que identifica qual ponto do eixo cada linha representa (ex: coluna `Mes` contendo Jan, Fev, Mar). Análoga funcional da "coluna discriminadora" da V4, mas semanticamente sobre ponto do eixo (não medida). Quando tem 10+ valores únicos, ativa bloco "Seleção de pontos do eixo em POR_LINHAS" (configurável na Spec S-V3). Colisão com declaração do mesmo campo como agrupador é bloqueio operacional W-V3-EIXO-AGRUP-COLISAO. D-062 · dcv_v3.md §3.1, §4.7.

#### `Intervalo declarado` vs `Intervalo efetivo` 📌🆕

Distinção V3 para auditoria:

- **Intervalo declarado** — o que o usuário configurou em De/Até (preservado em T-MODELO e aba Parâmetros)
- **Intervalo efetivo** — o que o motor aplicou após ajustes-limite (quando De < primeiro ponto disponível ou Até > último ponto disponível, motor ajusta e registra como AJUSTE_LEVE no Diagnóstico)

Aba Parâmetros lista ambos lado a lado quando diferiram. Default declarado: De = primeiro ponto da base, Até = último ponto. Warnings W-V3-INTERVALO-DEFAULT, W-V3-INTERVALO-AJUSTE-INICIO, W-V3-INTERVALO-AJUSTE-FIM, W-V3-INTERVALO-INVALIDO (bloqueio quando De > Até). D-064 · dcv_v3.md §4.6.

#### `Lacuna do eixo` vs `Ausência do agrupador em ponto` 📌🆕

Dois fenômenos de ausência distintos em V3:

- **Lacuna do eixo** (macroscópica) — ponto ausente no universo consolidado como um todo. Detecção automática em eixo temporal e ordinal com prefixo numérico (comparação com sequência canônica); não detectada em eixo manual ou ordinal sem prefixo. Warning W-V3-EIXO-LACUNA.
- **Ausência do agrupador em ponto** (microscópica) — agrupador específico sem valor em ponto específico, enquanto outros agrupadores têm valor lá. Detecção independe do tipo de eixo. Warning W-V3-AGRUP-AUSENCIA-PONTO.

**Impacto analítico: zero no cálculo** — comparação consecutiva pula lacunas naturalmente (Fev → Mai quando Mar e Abr ausentes). **Visibilidade sim** — duas flags estruturais no V3Result (`lacuna_anterior`, `ausencia_ponto`) produzem coluna textual informativa na Base Analítica sem alterar cálculos.

Densidade > 30% de pontos esperados ausentes dispara W-V3-EIXO-LACUNA-MASSIVA (alerta, não bloqueio) — só em eixos com detecção ativa. Threshold configurável na Spec. D-065 · dcv_v3.md §4.5.

#### `Classificação estrutural` vs `Classificação semântica` (V3) 📌🆕

Separação consolidada V2 preservada em V3:

- **Classificação estrutural** — AUMENTOU · REDUZIU · ESTAVEL · NAO_APLICAVEL. Sempre calculada. Tolerância 1e-9 absoluto para ESTAVEL (herança T-RANK D-041).
- **Classificação semântica** — derivada de estrutural × semântica declarada (T-SEMA):

| Estrutural | Maior-é-melhor | Menor-é-melhor | Neutra |
|---|---|---|---|
| AUMENTOU | Melhorou | Piorou | Aumentou |
| REDUZIU | Piorou | Melhorou | Reduziu |
| ESTAVEL | Estável | Estável | Estável |
| NAO_APLICAVEL | Não aplicável | Não aplicável | Não aplicável |

Vocabulário exibido ao usuário segue a semântica declarada. **Semântica é da medida, não da direção da comparação** — princípio V2 preservado. D-067 · dcv_v3.md §5.4.

#### `Evolução complementar` 🆕🔧

Opção declarada no Modo Comparativo V3, **default desligado**. Quando ligada, Base Analítica ganha duas colunas adicionais "Evolução Origem (ponto anterior)" e "Evolução Comparado (ponto anterior)" permitindo leitura da evolução de cada núcleo individualmente além da comparação Origem vs Comparado. Não afeta classificação semântica principal. Warning W-V3-COMP-EVOLUCAO registra ligação. D-067 · dcv_v3.md §4.8.

#### `Leitura de tendência` · `Leitura de aderência` 🆕📌

Síntese qualitativa do Bloco 5 do Resumo Executivo, adaptada por modo:

- **Modo Simples — Leitura de tendência** por agrupador no intervalo: Crescente (> 70% dos pares AUMENTOU, default) · Decrescente (> 70% REDUZIU) · Estável (> 70% ESTAVEL) · Mista (caso contrário)
- **Modo Comparativo — Leitura de aderência** entre Origem e Comparado ao longo da sequência: Aderente (> 70% dos pontos com |Variação %| ≤ 5%, tolerância editável) · Divergente (caso contrário)

Faixas editáveis em "Configurações avançadas" (padrão V4 Bloco 5 · D-044). **Afetam apenas a frase de síntese, não os cálculos principais.** Warning W-V3-LEITURA-CUSTOM registra customização. D-069 · dcv_v3.md §6.2.

#### `Recorte ponto a ponto` 🆕📌

Aba adicional do Excel V3 (aba 3 da estrutura canônica de 7 abas). Contém uma linha por **par consecutivo** (ponto_de → ponto_ate) por agrupador, pré-calculada pelo motor, permitindo ao usuário filtrar recorte via filtros nativos do Excel — ex: filtrar "Ponto de ≥ Jan" e "Ponto até ≤ Abr" para ver apenas pares Jan→Fev, Fev→Mar, Mar→Abr.

**Implementação 1 no MVP** (aba estática pré-calculada + filtros nativos). Síntese agregada recalculada sobre subset dentro do Excel fica como **P-V3-02-Evo · Aba parametrizável com recálculo dinâmico** (Implementação 3 da discussão T-13). Nota no topo da aba orienta: para síntese agregada sobre subset específico, execute nova análise no TabloFlow ajustando De/Até. D-069 · dcv_v3.md §6.4.

#### `Bloco "Seleção de pontos do eixo em POR_LINHAS"` 🆕🔧

Bloco condicional da configuração V3 ativado quando a coluna discriminadora do eixo em POR_LINHAS tem **10 ou mais valores únicos**. Lista todos os pontos detectados, pré-selecionados por default (analisar todos); usuário pode desmarcar subset não desejado antes do pivot. Warning W-V3-EIXO-PONTOS-MUITOS registra ativação; W-V3-EIXO-SELECAO+INTERVALO registra uso combinado com De/Até. Threshold 10 configurável na Spec S-V3. D-062 · dcv_v3.md §3.1.

#### `Mínimo operacional de 3 pontos` 📌🆕

Princípio estrutural da V3 (P0.7 do prévio, preservado). Aplica-se ao **intervalo efetivo** após pivot, seleção prévia de pontos, e De/Até. Quando qualquer operação reduz o universo efetivo abaixo de 3 pontos → bloqueio operacional W-V3-PONTOS-MIN.

Aplica-se também por agrupador: agrupador com < 3 pontos efetivos aparece na Base Analítica com flag "Agrupador com < 3 pontos efetivos" mas sem colunas de Diferença/Variação/Classificação. Warning W-V3-AGRUP-POUCOS-PONTOS. **Não é bloqueio global** — é filtragem do agrupador específico. D-064 · D-070 · dcv_v3.md §4.6, §5.5.

---

### Seção 5.V8 · Conceitos específicos da V8 🆕

**Status:** consolidada no refino do DCV-V8 (19/04/2026, sessão única de 12 pendências). Segunda visão da **Família B · Sequência**. Cumpre retroação diferida D-060.

#### `Recorrência e Ciclo de Vida` 📌🆕

Nome canônico da V8. Segunda visão da Família B. Responde "quem apareceu, quem permaneceu, quem saiu, quem voltou ao longo de um eixo sequencial ordenado?". Rastreia **presença/ausência** de entidades (vs V3 que rastreia valor). Consome T-EIXO integralmente (D-061); não consome T-SEMA (D-071). D-072 · dcv_v8.md §1.

#### `Entidade` (V8) 📌🆕

Unidade rastreada pela V8 ao longo do eixo sequencial. Obrigatória, uma só por execução. Exemplos: cliente, fornecedor, produto, SKU, contrato, colaborador. **Distinta de agrupador** — entidade é o que está sendo rastreado (unidade primária); agrupadores são recortes opcionais pelos quais o rastreamento é segmentado. Mesma entidade pode ter classificações diferentes em grupos distintos (ex: cliente presente em todos os meses em Sudeste, ausente nos últimos 3 em Nordeste). D-072 · dcv_v8.md §2.4.

#### `Classificação por ponto (V8)` 📌🆕

4 classes primárias mutuamente exclusivas atribuídas a cada par (Entidade, Ponto do eixo) dentro do intervalo efetivo:

| Classe | Condição |
|---|---|
| **Novo** | Presente no ponto atual · sem presença em nenhum ponto anterior dentro do intervalo |
| **Contínuo** | Presente no ponto atual · presente no ponto imediatamente anterior |
| **Retornou** | Presente no ponto atual · ausente no ponto imediatamente anterior · com histórico prévio no intervalo |
| **Ausente** | Ausente no ponto atual · presente em pelo menos um ponto anterior do intervalo |

**Entidade presente no primeiro ponto do intervalo efetivo = Novo** (sem histórico anterior). **Entidade ausente em todos os pontos** de um grupo específico não ocupa linha na matriz daquele grupo (economia de matriz). D-072 · dcv_v8.md §5.2.

#### `Classificação consolidada (V8)` 📌🆕

Uma classe consolidada do intervalo completo:

- **Constante** — entidade presente em **todos** os pontos do intervalo efetivo.
- (Não aplicável) — qualquer outro padrão; campo `classificacao_consolidada` = Null.

Classes consolidadas adicionais (Intermitente, Decrescente, Sazonal) ficam como **P-V8-02-Evo**. D-072 · dcv_v8.md §5.3.

#### `Classificação atual` (V8) 📌🆕

Classificação da entidade no **último ponto do intervalo efetivo**. Rótulo usado no Resumo Executivo (Bloco 3) e microcopy executiva. Representa o status "agora" da entidade conforme recorte da análise. D-072 · dcv_v8.md §5.4.

#### `Vocabulário dual técnico/exibição` (V8) 🆕🔧

Contratos técnicos em maiúsculas; exibição capitalizada natural:

| Contrato técnico | Exibição |
|---|---|
| `NOVO` | Novo |
| `CONTINUO` | Contínuo |
| `RETORNOU` | Retornou |
| `AUSENTE` | Ausente |
| `CONSTANTE` | Constante |

**Termos descartados do prévio V8** (ver §11 anti-glossário): "Recorrente" (→ Contínuo), "Recuperado" (→ Retornou), "Perdido" (→ Ausente). "Ativa/Inativa" permanecem **não oficiais**. D-072.

#### `Matriz de Presença` 📌🆕

Representação bidimensional núcleo da V8: entidades nas linhas, pontos do eixo nas colunas, classificações por célula. **Aninhada por grupo** quando há agrupadores (uma matriz independente por grupo). Contrato lógico da célula no V8Result (campo `matriz_celula`):

- **Presente:** `{"presente": true, "classe": NOVO|CONTINUO|RETORNOU, "medida": valor|null}`
- **Ausente com histórico prévio:** `{"presente": false, "classe": AUSENTE, "medida": null}`
- **Antes da primeira aparição:** `{"presente": false, "classe": null, "medida": null}` (célula vazia sem classificação).

Representação visual concreta (pontos, cores, símbolos) fica para Spec S-V8. D-077 · dcv_v8.md §6.2.

#### `Ordenação tripla da matriz` 🆕🔧

Ordem determinística em 3 níveis:

1. **Primária — por classificação atual**, default declarado editável: **Constante → Contínuo → Retornou → Novo → Ausente**. Warning W-V8-MATRIZ-ORDEM-CUSTOM registra edição.
2. **Secundária — taxa de presença decrescente** dentro de cada classe. Fixa.
3. **Terciária — alfabética da entidade** (desempate C.1). Fixa.

**Rationale do default primário:** começa pelas entidades mais estáveis (Constante) e termina pelas que requerem atenção (Ausente — saídas recentes). Leitura narrativa "quem ficou → quem entrou → quem voltou → quem estreou → quem saiu". D-077 · dcv_v8.md §6.2.

#### `Economia de matriz` 🆕📌

Princípio V8: entidade com 100% de ausências em todos os pontos do intervalo efetivo **dentro de um grupo específico não ocupa linha** na matriz daquele grupo. Motor filtra cedo no pipeline (antes da construção da matriz). Sem warning — comportamento esperado. Se usuário quer ver "entidades presentes em outros grupos mas ausentes neste", filtro cruzado via agrupadores resolve; ou V6 (cruzamento) é caminho alternativo. D-076 · dcv_v8.md §4.4.

#### `Granularidade mista no eixo` 📌🆕

Fenômeno detectado automaticamente quando coluna do eixo temporal contém 2+ granularidades distintas (mistura de datas diárias e rótulos mensais; mistura de mensal e trimestral). Exemplo: coluna com "15/03/2024" (dia) e "Abril/2024" (mês) misturados.

**Tratamento:** alerta forte com **confirmação obrigatória**. Motor exibe amostra dos valores detectados em cada granularidade; usuário é obrigado a confirmar explicitamente antes de prosseguir. Sem correção automática (C.5). Warning **W-V8-EIXO-GRANULARIDADE-MISTA** (alerta) registra confirmação.

Alternativas orientativas: corrigir na base · usar M2.NORMALIZE futuro · aceitar com confirmação. Conceito não se aplica a eixos lógico/ordinal ou manual (sem referência de granularidade). D-076 · dcv_v8.md §4.4c.

#### `Modo Transacional` vs `Modo Pré-agregado` (V8) 📌🆕

Dois modos declarados da base V8:

- **Modo Transacional** — cada linha representa uma ocorrência individual (base transacional plana); duplicidades em (Entidade, Ponto do eixo, Agrupadores ativos) são esperadas e resolvidas por consolidação.
- **Modo Pré-agregado** — cada linha já representa a combinação consolidada; duplicidades não são esperadas. Quando há, W-V8-DUPLICIDADE-PREAGREGADA alerta.

**Modo é rótulo informativo.** Consolidação via T-AGRUPA é **lógica única**, independentemente do modo declarado — motor consolida sempre por (Entidade + Ponto do eixo + Agrupadores ativos). Modo declarado pelo usuário com default declarado do motor (detecção de duplicidade na amostragem). W-V8-MODO-INFERIDO registra aceitação por default. D-074 · dcv_v8.md §4.1.

#### `Regra de agregação V8 — aplicação condicional` 🆕🔧

Regra T-AGRUPA aplica-se **apenas quando há campo de medida opcional declarado**. 5 regras canônicas herdadas D-026: soma (default) · média · máximo · mínimo · contagem. Default varia por tipo de medida:

- **Aditivo:** default soma.
- **Relativo · Não-aditivo:** default **média** (somar percentuais não tem sentido analítico).
- **Estado/situação (categórico):** regra não aplicável; motor exibe primeira ocorrência ou concatenação (Spec S-V8 decide).

Quando **não há medida declarada**, consolidação resolve apenas presença (múltiplos registros → 1 par presente na matriz; regra fica inativa). **"Primeiro valor"** do prévio V8 descartado por conflito com C.1 (depende de ordem de leitura). D-074 · dcv_v8.md §4.1, §4.2.

#### `Medida contextual V8` 🆕📌

Campo de medida em V8 é **opcional e contextual** — enriquece leitura sem alterar classificação (que é por presença/ausência). Aparece na Base Analítica e no Histórico de Presença quando há presença; **vazio/não aplicável quando há ausência** (nunca convertido em zero).

**Tratamento por tipo (herança D-025 adaptada):**

| Tipo | Warning | Tratamento V8 |
|---|---|---|
| Aditivo | — | Execução normal; default soma |
| Relativo | W-V8-MEDIDA-RELATIVA | Default declarado: média |
| Não-aditivo | W-V8-MEDIDA-NAO-ADITIVA | Default declarado: média + alerta contextual |
| Estado/situação | W-V8-MEDIDA-CATEGORICA (alerta) | Valor categórico na Base Analítica; não agregável |

**Negativos não se aplicam** — V8 não calcula Diferença/Variação sobre medida; valores negativos aparecem como vieram. Nulos com presença preservados (não viram zero). Divergência com V3 (D-066) justificada pelo padrão herança adaptada. D-075 · dcv_v8.md §4.2.

#### `Leitura de ciclo de vida` 🆕📌

Síntese qualitativa do Bloco 5 do Resumo Executivo V8. 5 classes mutuamente exclusivas:

| Leitura | Condição default |
|---|---|
| **Estável** | > 60% das entidades têm consolidada Constante OU taxa de presença ≥ 80% |
| **Rotativa** | Novas + Ausentes no último ponto ≥ 30% do total |
| **Em retração** | Ausentes no último ponto > Novas em fator ≥ 1.5 |
| **Em expansão** | Novas no último ponto > Ausentes em fator ≥ 1.5 |
| **Mista** | Nenhuma das acima se aplica isoladamente |

Thresholds (60%, 80%, 30%, 1.5) **editáveis** em "Configurações avançadas". Warnings W-V8-LEITURA-DEFAULT (aceitação) e W-V8-LEITURA-CUSTOM (edição). Padrão herdado de V4 Bloco 5 · D-044 + V3 D-069. Nota estática final do bloco redireciona V6/V9 para análises aprofundadas. D-078 · dcv_v8.md §6.3.

#### `Movimentações` (V8) 🆕📌

Aba dedicada V8 (aba 5 da estrutura canônica de 7 abas). Contém entidades que **mudaram de classificação no último ponto**: novas entradas, retornadas, perdas recentes (Ausentes no último ponto). Insight analítico específico V8 — responde "o que mudou recentemente no ciclo?". Não absorvida em outras abas (Resumo Executivo é síntese; Base Analítica é granular) — justifica aba própria. Herança preservada do prévio V8 PARTE 10.3. D-078 · dcv_v8.md §6.4.

#### `Aba Dados Brutos do prévio V8 — descartada` 🆕

Decisão do refino: aba Dados Brutos do prévio V8 PARTE 10.3 **não é incorporada** no MVP. Rationale: Base Analítica dos dois tipos de visão (periódica em aba Histórico de Presença; consolidada em aba Resumo por Entidade) cobre toda a auditoria analítica; dados brutos normalizados são parte do upload, não da visão V8. Se usuário quer dados brutos, eles estão no arquivo original carregado. Aba Diagnóstico registra "linhas originais: X, linhas consolidadas: Y" para auditoria. D-078 · dcv_v8.md §6.4.

#### `Escala de cardinalidade em 3 eixos multiplicativos` 🆕🔧

Especificidade V8 inédita. Volume analítico V8 = **entidades × pontos do eixo × grupos** (quando há agrupadores). 5 patamares operacionais:

| Volume (células totais) | Comportamento |
|---|---|
| Até ~15.000 | Normal, sem aviso |
| 15.000 - 100.000 | Aviso + estimativa em tempo real |
| 100.000 - 500.000 | Confirmação obrigatória (W-V8-VOLUME-ALTO) |
| 500.000 - 1.000.000 | Confirmação forte (W-V8-VOLUME-CRITICO) |
| > 1.000.000 | **Bloqueio** (W-V8-VOLUME-INVIAVEL) — limite físico Excel |

Escala adicional específica de **entidades por grupo**: 100/500/2000/10.000 com warnings apropriados (W-V8-MATRIZ-PAGINACAO, W-V8-ENTIDADES-MUITAS, W-V8-ENTIDADES-CRITICO, W-V8-ENTIDADES-INVIAVEL). Escala de **pontos do eixo efetivo**: bloqueio em 200+ (W-V8-PONTOS-INVIAVEL). Escala de **agrupadores**: 1-3/4-5/6/7+ com bloqueio em 7+ (W-V8-AGRUP-MUITOS — mais conservador que V3 porque agrupadores V8 multiplicam grupos). D-079 · dcv_v8.md §4.6, §7.1.

#### `Colisões bloqueadas` (V8) 🆕🔧

Três colisões entre declarações de campo que disparam bloqueio operacional em V8:

| Colisão | Warning | Rationale |
|---|---|---|
| Eixo = Entidade | W-V8-EIXO-ENTIDADE-COLISAO | Rastreamento circular |
| Agrupador = Entidade | W-V8-AGRUP-ENTIDADE-COLISAO | Segmentação circular |
| Eixo = Agrupador | W-V8-EIXO-AGRUP-COLISAO | Herança V3 D-070 |

Motor não corrige silenciosamente (C.5) — pede ajuste do usuário. D-079 · dcv_v8.md §4.6.

---

### Seção 5.V7 · Conceitos específicos da V7 🆕

Vocabulário consolidado do DCV-V7 refinado (19/04/2026). V7 é a **primeira visão da Família D · Posição relativa**, única do Módulo 1 que usa o próprio conjunto de dados como referência interna de comparação (não há benchmark externo, meta externa ou comparação temporal). Termos canônicos definidos em dcv_v7.md §13.

### `Desvio em Relação à Média do Grupo` 🆕 (V7)

Nome oficial da V7. Pergunta-âncora: *"dentro de cada grupo, como cada elemento se posiciona em relação à média do seu próprio grupo?"*. Unidade analítica é **Elemento + Grupo**. dcv_v7.md §1.

### `Grupo` (V7)

Campo categórico obrigatório que segmenta a base em unidades independentes de comparação (região, categoria, linha de produção, carteira, centro). Cada valor único forma um grupo com sua própria média interna. Não aceita campo numérico contínuo. dcv_v7.md §4.5.

### `Elemento` (V7)

Campo categórico obrigatório, distinto do Grupo, que identifica a unidade posicionada dentro do grupo (vendedor, fornecedor, centro de custo, colaborador, linha). Mesmo nome de elemento em grupos distintos é tratado como duas unidades analíticas independentes. dcv_v7.md §4.5 · §10.

### `Unidade analítica` (V7)

Combinação **Elemento + Grupo** com valor consolidado pela regra de agregação declarada. Princípio **"consolidar primeiro, calcular depois"** (herança do prévio §4.3). dcv_v7.md §2.4.

### `Dupla agregação` 🆕 (V7 · armadilha estrutural)

Armadilha central da V7: calcular média do grupo sobre **linhas brutas** (em vez de elementos consolidados), produzindo classificação invertida. Exemplo: VendedorA com 2 linhas (100 + 200 = 300 consolidado) vs VendedorB com 1 linha (300). Caminho correto: média = (300+300)/2 = 300 · ambos Na Média. Caminho com dupla agregação: média = (100+200+300)/3 = 200 · VendedorA "Acima", VendedorB "Acima" — inversão total. F-MOT blinda em teste unitário que linhas brutas nunca entram no cálculo da média. D-082 · dcv_v7.md §1 · §4.3 · §5.1.

### `Tolerância` (V7)

Parâmetro declarado pelo usuário em E3 que define a Zona de Média. Default declarado **±5% simétrico em desvio percentual**, editável. Formato único — assimétrica e absoluta fora de escopo. Papel duplo: (1) define classe Na Média; (2) define atributo derivado Desvio Significativo (= Classificação ∈ {Acima, Abaixo}). D-084 · dcv_v7.md §4.4.

### `Zona de Média` 🆕 (V7)

Região classificatória derivada da Tolerância. Elementos com `|desvio_percentual| ≤ Tolerância` são classificados Na Média. Sinônimo pedagógico aceitável em microcopy: "Faixa de Tolerância". **Evitar:** "zona de equilíbrio", "região neutra", "alvo", "meta" (implicariam semântica não prevista). D-084 · dcv_v7.md §13.

### `Classes primárias V7` — Acima · Na Média · Abaixo 🆕

**3 classes mutuamente exclusivas** por elemento, derivadas da Tolerância:
- **Acima**: `desvio_percentual > +Tolerância`
- **Na Média**: `|desvio_percentual| ≤ Tolerância`
- **Abaixo**: `desvio_percentual < −Tolerância`

Estrutura enxuta adaptada à natureza univariada da V7, coerente com padrão "herança adaptada à natureza analítica" (D-073) — V7 tem 3 classes pela natureza univariada contínua, V8 tem 4 classes pela natureza sequencial com estados qualitativamente distintos. D-086 · dcv_v7.md §5.2.

### `Desvio Significativo` 🆕 (V7 · atributo derivado)

**Atributo boolean derivado**, não classe independente: `Classificação ∈ {Acima, Abaixo}`. Aba Excel "Desvios Significativos" (§6.3) é **recorte filtrado** da aba Detalhe por `desvio_significativo=True`, não cálculo autônomo. D-086 · dcv_v7.md §5.2 · §6.3.

### `NULO_MEDIDA` (V7 · classificação especial por elemento)

Classificação especial **paralela às 3 primárias**, aplicada quando consolidação T-AGRUPA retornou nulo (todas as linhas de uma combinação Elemento+Grupo tinham nulo na medida). Elemento preserva registro no V7Result mas recebe classificação NULO_MEDIDA em vez de Acima/Na Média/Abaixo. Herança integral de V4 D-038 adaptada. Warning: W-V7-NULO-MEDIDA (alerta forte). D-085 · dcv_v7.md §5.2 · §5.3.

### `Não aplicável` 🆕 (V7 · classificação especial por grupo)

Classificação especial **aplicada ao grupo inteiro** quando cálculo percentual é matematicamente indefinido ou não-interpretável:
- Grupo com média negativa — desvio percentual contraintuitivo (sinal inverte)
- Grupo com média zero homogênea (todos elementos=0) — 0/0 é indefinido
- Grupo com média zero heterogênea (positivos cancelam negativos, ou zeros "arrastam") — divisor zero

Grupo recebe `status_grupo = Não_Aplicavel`; todos os elementos do grupo herdam classificação Não aplicável. Desvios absoluto e percentual permanecem calculados no V7Result para inspeção, apenas classificação é substituída. Tolerância não se aplica; ranking intra-grupo não é gerado; grupo não entra na leitura qualitativa do Bloco 5 do Resumo Executivo. D-083 · D-085 · dcv_v7.md §5.3.

### `Leituras qualitativas de grupo` 🆕 (V7 · Bloco 5 do Resumo Executivo)

5 leituras qualitativas + 1 estrutural, aplicadas por grupo no Bloco 5 com faixas editáveis (padrão D-044 · V4/V8). **Não são classificação estrutural do V7Result** — vivem exclusivamente no Resumo Executivo.

| Leitura | Condição default |
|---|---|
| **Grupo Homogêneo** | ≥ 70% dos elementos são Na Média |
| **Grupo Assimétrico Acima** | ≥ 60% dos elementos são Acima OU Acima/(Acima+Abaixo) ≥ 75% |
| **Grupo Assimétrico Abaixo** | ≥ 60% dos elementos são Abaixo OU Abaixo/(Acima+Abaixo) ≥ 75% |
| **Grupo Polarizado** | Acima ≥ 25% E Abaixo ≥ 25% |
| **Grupo Misto** | Nenhuma das acima (residual) |
| **Grupo Não aplicável** | status_grupo = Não aplicável (estrutural, não editável) |

Ordem de teste: Não aplicável → Polarizado → Assimétrico Acima/Abaixo → Homogêneo → Misto. Thresholds (70%, 60%, 75%, 25%) editáveis em "Configurações avançadas"; W-V7-LEITURA-DEFAULT/CUSTOM registram. D-086 · dcv_v7.md §6.2 Bloco 5.

### `Modo da base` (V7 · Transacional × Pré-agregado)

Modo declarado com default detectado pelo motor na amostragem. Transacional: múltiplas linhas por (Grupo, Elemento); T-AGRUPA obrigatório com regra declarada. Pré-agregado: 1 linha por (Grupo, Elemento); T-AGRUPA como **no-op validado** — motor verifica unicidade em volume completo. Herança V8 D-074 adaptada. W-V7-MODO-VIOLACAO é bloqueio quando Pré-agregado declarado mas duplicatas detectadas. D-082 · dcv_v7.md §4.1.

### `Média ponderada em Relativa` 🆕 (V7)

Tipo Relativa (taxa, margem, índice) aceita **campo de peso opcional**. Default é média aritmética simples dos elementos consolidados, com W-V7-RELATIVA-MEDIA-ARIT (alerta forte). Se usuário declara campo de peso (quantidade, volume), motor aplica `Σ(valor × peso)/Σpeso`; W-V7-RELATIVA-MEDIA-POND (informativo). Decisão motor em E3 oferece opção sem forçar. D-083 · dcv_v7.md §4.2.

### `Ranking intra-grupo V7` (T-RANK · regra de desempate V7-específica)

V7 é **sexta consumidora de T-RANK**. Critério: magnitude (módulo) do desvio percentual decrescente. Regra de desempate **em 4 níveis**, adaptação V7 do contrato D-041 via padrão "herança adaptada à natureza analítica" D-073:

1. `abs(desvio_percentual)` decrescente
2. `abs(desvio_absoluto)` decrescente
3. Nome do Elemento alfabético case-insensitive
4. Ordem de inserção original

Tolerância floating point: 1e-9. Escopo intra-grupo; ranking global fora de escopo V7. Elementos NULO_MEDIDA e em grupos Não aplicável não recebem ranking. D-088 · dcv_v7.md §5.4.

### `Mapa de Grupos` 🆕 (V7 · aba Excel específica)

Aba 2 do Excel V7. Substitui "Resumo por Grupo" do prévio, absorvendo conteúdo original e adicionando **amplitude de desvio · leitura qualitativa · status Calculado/Não aplicável**. 1 linha por Grupo com: N Elementos · Média do Grupo · Maior desvio+/- · Amplitude · N por classe · Leitura qualitativa · status. Ordenação default por amplitude de desvio decrescente (grupos mais dispersos primeiro). Papel análogo à Matriz de Presença (V8) e ao Recorte ponto a ponto (V3) — aba específica que representa o coração visual da análise. D-089 · dcv_v7.md §6.3.

### `Aba Dados Brutos V7 — descartada` 🆕

Aba do prévio V7 (PARTE 10.2 aba 4) **descartada** no refino com rationale do padrão V8 D-078. Base Analítica (aba 3 Detalhe por Elemento) cobre auditoria analítica; dados brutos normalizados são parte do upload, não da visão. Diagnóstico registra "linhas originais vs consolidadas" para rastreabilidade. D-089 · dcv_v7.md §6.3.

### `Escala de cardinalidade V7 · 3 eixos hierárquicos` 🆕

Diferente de V8 (escala multiplicativa entidades × pontos × grupos), V7 tem **escala hierárquica-aditiva**: elementos estão **dentro de** grupos, não cruzados com. 3 eixos: (1) cardinalidade do Grupo — 1-20 normal · 51-200 alerta · 1.001+ bloqueio; (2) elementos por grupo — < 2 bloqueio · 500+ aviso · 10.000+ alerta; (3) total de elementos — ≤ 50.000 normal · 500.001-1.000.000 alerta forte · 1.000.001+ bloqueio (limite físico Excel). D-089 · dcv_v7.md §8.2.

### `Família D · Posição relativa` (V7 · par autônomo com V9)

Visões que analisam como cada elemento se posiciona em relação a um **benchmark calculado internamente sobre os próprios dados**. V7 calcula benchmark como média do grupo (univariado intra-grupo); V9 calcula como posição consolidada em múltiplas métricas (multidimensional cross-elementos). Ambas consomem T-SEMA, T-AGRUPA e T-RANK (cada uma com contratos adaptados à natureza analítica — padrão D-073). **Não há view especializada entre elas** — autônomas. Vocabulário declarativo autossuficiente — nenhuma menciona a outra em interface operacional. DCV-V7 §2.3 estabelece padrão com 3 células *(a confirmar em DCV-V9)*; **DCV-V9 §2.3 (D-091) cumpriu a retroação diferida D-081** preenchendo simetricamente as 3 células. **Família D fechada em Fase 0** após aprovação dos dois DCVs. D-081 · D-091 · dcv_v7.md §2.3 · dcv_v9.md §2.3.

---

### Seção 5.V9 · Conceitos específicos da V9 🆕

### `Perfil de Ranking por Métricas` 🆕 (V9)

Nome oficial da V9. Responde: *"dentro do meu conjunto de elementos, quem se destaca em cada métrica, quem apresenta melhor posicionamento consolidado e quem demonstra perfil de liderança, especialização, equilíbrio ou retaguarda?"* Visão de **posicionamento relativo multidimensional** — benchmarking interno em múltiplas métricas simultâneas. Para cada Identificador, calcula Posição em cada métrica (respeitando Direção declarada), consolida em Score Consolidado (média aritmética simples das posições válidas), calcula Variação Máxima de Posição, e classifica em 4 classes de perfil. Segunda e última visão da Família D (par autônomo com V7). dcv_v9.md §1.

### `Identificador` 📌 (V9)

Campo categórico obrigatório que identifica a unidade sendo ranqueada (vendedor, produto, filial, cliente, fornecedor, campanha, contrato). Exatamente 1 por execução. Não pode ser campo numérico contínuo usado como métrica; códigos e textos com aparência numérica são aceitos se Motor Base os classifica como categóricos. Identificador composto (múltiplos campos concatenados) fica em P-V9-07-Evo. dcv_v9.md §3.3.

### `Métrica` 📌 (V9)

Campo numérico alvo do ranking. 2 mínimo obrigatório, 6 máximo recomendado, 10 absoluto (11+ bloqueia). Cada Métrica tem: campo numérico, nome analítico editável, **Direção obrigatória** (Maior-é-melhor × Menor-é-melhor), regra de agregação declarada (default declarado por tipo). Termo V9 não se confunde com "medida" de V7 (que é única por execução). dcv_v9.md §3.3 · §4.5 · §4.7.

### `Direção da Métrica` 🆕 📌 (V9)

Declaração obrigatória por métrica: **Maior-é-melhor** (ordem decrescente na ordenação — Posição 1 é o maior valor) ou **Menor-é-melhor** (ordem crescente — Posição 1 é o menor valor). **Sem default, declaração obrigatória do usuário em E3** — única quebra do padrão "default declarado" no DCV-V9, justificada pela gravidade da inversão (Direção errada inverte o ranking 100%). Detecção automática por nome foi **rejeitada no MVP** (P-V9-02-Evo opt-in). Contrato V9 de T-SEMA: por métrica, com efeito direto no cálculo (§4.6 do DCV-V9 · D-093). dcv_v9.md §4.4.

### `Modo de Ranking` 🆕 📌 (V9)

Declaração obrigatória do usuário em E3: **Global** (ranking único sobre todo o conjunto · unidade analítica = Identificador) ou **Segmentado** (ranking recalculado dentro de cada valor do Agrupador · unidade analítica = Identificador + Agrupador ativo). No modo Segmentado, Agrupador é obrigatório (bloqueio W-V9-SEG-SEM-AGRUPADOR se ausente). MVP limita 1 Agrupador ativo; múltiplos em P-V9-08-Evo. dcv_v9.md §4.2.

### `Valor Consolidado da Métrica` (V9)

Valor da métrica por Identificador após aplicação da regra de agregação declarada (Passo 1 do pipeline §5.2 do DCV-V9). Regras oficiais: Soma · Média · Máximo · Mínimo · Contagem (cada métrica com regra independente — extensão D-092 do contrato T-AGRUPA). Default declarado por tipo: Aditiva → Soma · Não-aditiva e Relativa → Média. Valor consolidado é preservado na saída Excel lado a lado com Posição (nunca é descartado) — permite auditoria total. dcv_v9.md §4.7 · §5.2.

### `Posição por Métrica` 🆕 📌 (V9)

Rank do Identificador em uma métrica específica após ordenação pela Direção declarada. Usa **rank mínimo** (elementos empatados em valor consolidado recebem mesma Posição, a menor disponível; elementos seguintes continuam a partir de `N_anteriores + 1` — equivalente a `pandas.Series.rank(method='min')` e SQL `RANK()`). Empate preservado como fato analítico, não desempatado artificialmente. dcv_v9.md §5.2 · §5.4.

### `Score Consolidado` 🆕 📌 (V9)

Média aritmética simples das Posições por Métrica válidas de um Identificador: `score = soma(posicao_por_metrica_valida) / N_metricas_validas`. **Quanto menor, melhor o posicionamento geral.** Equal-weighted é arquitetura da visão — qualquer ponderação embute decisão sobre o dado do usuário (viola C.5) ou descaracteriza V9 como visão autônoma (candidato a nova visão futura). Alternativas rejeitadas no MVP: soma (monotonicamente equivalente · menos interpretável), mediana (descarta extremos · distorce especialização), média geométrica (penaliza posições ruins desproporcionalmente), média ponderada (P-V9-01-Evo). dcv_v9.md §5.3 · D-095.

### `Melhor Posição` e `Pior Posição` (V9)

**Melhor Posição** = `min(posicao_por_metrica_valida)` — menor valor entre as Posições do Identificador (a posição mais próxima do topo em qualquer métrica). **Pior Posição** = `max(posicao_por_metrica_valida)` — maior valor (mais afastada do topo). Ambos preservados na saída Excel por Identificador. dcv_v9.md §5.5.

### `Variação Máxima de Posição` 🆕 📌 (V9)

Amplitude ordinal das posições de um Identificador através de suas métricas válidas: `variacao_maxima = Pior Posição − Melhor Posição`. Unidade: número inteiro positivo (ou zero). **Indicador de especialização × equilíbrio:**

- Variação = 0 → perfil perfeitamente equilibrado (mesma posição em todas métricas válidas)
- Variação baixa em relação ao tamanho do conjunto → perfil equilibrado
- Variação alta → perfil especialista (líder numa métrica, retaguarda noutra)

Interpretação "alta × baixa" é **relativa ao tamanho do conjunto** (não ao número de métricas) — por isso threshold Especialista é percentual do N_elementos_validos. Alternativas rejeitadas: desvio padrão das posições (pressupõe distribuição, frágil com N pequeno), amplitude normalizada (perde grão interpretativo), coeficiente de variação (numericamente ruim com médias baixas). dcv_v9.md §5.5 · D-097.

### `Classes primárias V9` — Líder · Especialista · Equilibrado · Retaguarda 🆕 📌

4 classes mutuamente exclusivas aplicadas por **prioridade declarada** (Líder → Retaguarda → Especialista → Equilibrado):

- **Líder** — Identificador com `score_consolidado ≤ percentil_20` do conjunto analisado (top 20% default editável)
- **Retaguarda** — Identificador com `score_consolidado ≥ percentil_80` (bottom 20% default editável)
- **Especialista** — Identificador com `variacao_maxima_posicao ≥ 50% × N_elementos_validos`, desde que não já Líder ou Retaguarda. Leitura para elementos "do meio" com alta dispersão de posições.
- **Equilibrado** — classe residual (não classificado em 1, 2 ou 3)

**Prioridade vs simultâneo:** elemento que qualifica simultaneamente a Líder e Especialista é **Líder** (prioridade vence). Interpretação correta: Especialista não é "estrela em uma métrica mas ruim em outras" — é perfil residual com alta variação para elementos não-extremos do score.

Taxonomia divergente da V7 (3 primárias) justificada pelo padrão "herança adaptada à natureza analítica" D-073: V7 tem natureza univariada contínua com direção (3 classes simétricas); V9 tem natureza multidimensional com dois eixos (score + variação) produzindo 4 classes. dcv_v9.md §5.6 · D-098.

### `NULO_MEDIDA` (V9 · classificação especial paralela)

Elemento com **0 métricas válidas** (nulo em todas as N métricas consolidadas). Classificação especial paralela que substitui classe primária — elemento não recebe Posição em nenhuma métrica, Score e Variação Máxima são nulos. **Não entra no cálculo dos percentis 20/80** (conjunto analisado efetivo = N total − N NULO_MEDIDA). Aba Ranking Completo mostra "—" em todas as colunas; Diagnóstico registra causa. Herança adaptada V7 D-086: em V7 NULO_MEDIDA é binário (1 medida); em V9 NULO_MEDIDA só quando 0 métricas válidas, elementos com cobertura parcial (K ≥ 1) permanecem no ranking via **score parcial** (W-V9-METRICA-PARCIAL). dcv_v9.md §5.3 · §5.6.

### `Score parcial` 🆕 (V9 · cobertura K < N)

Elemento com valor válido em K de N métricas (K ≥ 1) permanece no ranking; score calculado como média sobre K métricas válidas. **Menos comparável** a score sobre N completo — elemento com K=1 tem "equilíbrio falso" (variação = 0 por construção; **não elegível a Especialista**). W-V9-METRICA-PARCIAL sinaliza o fato; `n_metricas_validas` registrado por elemento no V9Result. Divergência vs V7 justificada por D-073 (V7 binário; V9 nuançado por cobertura). dcv_v9.md §5.3 · §5.5.

### `Conjunto Analisado` (V9)

No **modo Global**: base inteira (todos os Identificadores válidos, exceto NULO_MEDIDA). No **modo Segmentado**: cada grupo separadamente (N_elementos_validos calculado por agrupador; thresholds recalculados por agrupador). Convenção importante quando se fala de "top 20%" — sempre sobre o conjunto, que pode ser diferente em cada execução. dcv_v9.md §5.6.

### `Leituras qualitativas de conjunto` 🆕 (V9 · Bloco 5 do Resumo Executivo)

5 leituras qualitativas do conjunto analisado, com thresholds editáveis em "Configurações avançadas" (padrão D-044):

| Leitura | Condição default | Interpretação |
|---|---|---|
| **Conjunto Homogêneo** | ≥ 70% Equilibrados | Poucos extremos · massa no meio |
| **Conjunto Concentrado** | N Líderes + N Retaguarda ≥ 50% | Polarização por score · poucos no meio |
| **Conjunto Especializado** | ≥ 30% Especialistas | Especialização é traço dominante |
| **Conjunto Misto** | Nenhuma das acima | Residual |
| **Conjunto Degenerado** | N < 5 OU ≥ 30% NULO_MEDIDA | Estrutural — leitura limitada |

Ordem de teste: Degenerado → Especializado → Concentrado → Homogêneo → Misto. No modo Segmentado: 1 leitura por agrupador. Análogo estrutural a V7 "Leituras qualitativas de grupo" (D-086) e V8 leituras de ciclo de vida (D-078). dcv_v9.md §5.6 · D-098.

### `Expansão por empate no corte percentual` 🆕 (V9)

Regra determinística: se elemento na fronteira do corte (percentil 20 ou 80) tem score empatado com elemento imediatamente posterior, **ambos entram na mesma classe** em vez de cortar arbitrariamente entre equivalentes matemáticos. Classes podem crescer além do threshold declarado. Exemplo: N=10, top 20% = 2 Líderes; se elemento 2 e 3 têm mesmo score, há 3 Líderes. W-V9-CLASSE-EXPANDIDA-POR-EMPATE (informativo) registra. Aplicação direta de C.5 (sistema não decide arbitrariamente entre equivalentes). dcv_v9.md §5.6.

### `Arredondamento ceil em N pequeno` 🆕 (V9)

Em conjunto com N < 5 elementos válidos, thresholds percentuais são aplicados via `ceil` (arredondamento para cima) para garantir pelo menos 1 Líder e 1 Retaguarda. Exemplo: N=3, top 20% = `ceil(0,6)` = 1 → 1 Líder + 1 Retaguarda + 1 Equilibrado/Especialista. Documentado como convenção canônica determinística (C.1). dcv_v9.md §5.6.

### `Mapa de Perfil` 🆕 (V9 · aba Excel específica · coração visual)

Aba específica V9 análoga estrutural a Matriz de Presença V8 (D-077) e Mapa de Grupos V7 (D-089). Matriz pivotada **Identificador × Métrica** com valor = Posição numérica, coloração condicional por célula respeitando Direção declarada (Maior-é-melhor bem posicionado em cor positiva; Menor-é-melhor bem posicionado em cor positiva coerente), destaque visual para Pos 1 e Pior Posição de cada elemento, coluna adicional Classificação. Linhas predominantemente em cor positiva = Líderes; predominantemente em cor negativa = Retaguarda; com forte variação de cor = Especialistas. Microcopy "Mapa de Perfil" (não "Matriz de Posições" que é linguagem motor). dcv_v9.md §5.8.

### `Aba Dados Brutos V9 — descartada` 🆕

Prévio V9 (Parte 10.2) declarava aba "Dados Brutos" como 4ª oficial. Refino descarta seguindo herança V8 D-078 + V7 D-089 — aba Ranking Completo cobre auditoria analítica (1 linha por Identificador com valor consolidado E posição E classificação E score); Diagnóstico registra "linhas originais vs consolidadas" para rastreabilidade. 3 aplicações consecutivas (V8 · V7 · V9) do padrão "Dados Brutos descartada em favor de Base Analítica + Diagnóstico" — candidato a formalização (CONTEXT §9 Camada C). dcv_v9.md §5.8 · D-099.

### `Escala de cardinalidade V9 · multi-eixo independente` 🆕

3 eixos ortogonais que se combinam sem aninhamento obrigatório: Eixo 1 (N Identificadores · 7 patamares com alertas de 501 até bloqueio 1.000.001+), Eixo 2 (N Métricas · 5 patamares), Eixo 3 (cardinalidade do Agrupador no modo Segmentado · 4 patamares). Estrutura distinta de V7 (**hierárquica-aditiva** · elementos dentro de grupos) e V8 (**multiplicativa** · matriz aninhada) — aplicação canônica D-073. Custo computacional escala como O(N · M log N) (ordenação por métrica). dcv_v9.md §8 · D-100.

### `Pesos por métrica · fora de escopo MVP` (V9)

V9 aplica equal-weighted por arquitetura — todas as métricas contribuem igualmente para o Score Consolidado. Peso automático seria decisão silenciosa do sistema sobre dado do usuário (viola C.5); peso manual declarado é sub-caso de "score composto ponderado" (descaracterizaria V9 como visão autônoma, candidato a nova visão futura). P-V9-01-Evo documenta para evolução futura com análise cuidadosa da fronteira V9 × V4 Modo 3. dcv_v9.md §4.10 · D-094.

### `Heterogeneidade de escalas` 🆕 (V9 · detecção sem correção)

V9 **não normaliza** valores de métrica em nenhuma hipótese — escalas heterogêneas (Faturamento em R$ de milhões, Taxa em decimais, Tempo em minutos) são **neutralizadas pela natureza ordinal da Posição**. Motor detecta heterogeneidade via **teste de razão de amplitude**: `max(amplitude_por_metrica) / min(amplitude_por_metrica) > 1000` (3 ordens de grandeza). Quando detectada, W-V9-ESCALAS-HETEROGENEAS (informativo) lembra usuário que score é por posição, não por valor. Threshold 1.000× é default editável. Alternativas rejeitadas no MVP: Z-score (P-V9-03), Min-max (P-V9-04), Log-scale (P-V9-05), Ranking padronizado (P-V9-06), Score composto ponderado (fora de V9). dcv_v9.md §4.9 · D-094.

---

### Seção 5.V5 · Conceitos específicos da V5 🆕

### `Comportamento e Dispersão` 🆕📌 (V5)

Nome canônico da V5. Visão de **estatística descritiva univariada com detecção de outliers configurável** sobre um campo numérico. Primeira visão da Família E · Estrutura interna do recorte. Responde *"como os valores de um campo numérico se distribuem dentro de um conjunto, onde está o centro da distribuição, qual é o grau de dispersão e quais valores são atípicos?"*. dcv_v5.md §1 · D-110.

### `Campo Principal` 📌 (V5)

Campo numérico sobre o qual a análise estatística é realizada. Único campo obrigatório (Modo Global). Em Modo Segmentado, Agrupador também é obrigatório. dcv_v5.md §3.2.

### `Modo da Visão` 📌 (V5)

V5 opera em dois modos: **Global** (análise sobre conjunto inteiro · uma única distribuição consolidada · default declarado editável) e **Segmentado** (análise particionada por Agrupador · uma distribuição independente por segmento). Espelha estrutura V9. dcv_v5.md §4.3.

### `Modo da Base` 🆕📌 (V5 · Granularidade declarada)

V5 declara explicitamente a granularidade da base em duas dimensões: **Individual** (cada linha é uma observação individual · default declarado editável · ex: extrato de transações) e **Consolidada por chave** (cada linha é uma observação consolidada por chave declarada · ex: planilha já agregada por filial-mês). Em nenhum modo V5 consolida valores — modo da base declara como interpretar a granularidade da entrada · não autoriza o motor a agregar valores. Quando granularidade é Consolidada, chave de consolidação (campo ou conjunto de campos) é declarada pelo usuário · T-AGRUPA verifica unicidade. Adaptação V5-específica do padrão "consolidação obrigatória pré-cálculo" (D-073 · 4ª aplicação consecutiva). dcv_v5.md §4.1 · D-102.

### `Unidade analítica V5` 🆕📌 (V5)

**A observação individual no campo numérico principal** — cada linha da base que tem valor válido (não-nulo · numérico) no campo principal é uma observação no conjunto sob análise. Distintiva de V5 em relação a V4/V7/V9 onde a unidade analítica é uma chave consolidada. V5 nunca consolida valores: 100 vendas de R$ 50 e 1 venda de R$ 5.000 entram como 101 observações, nunca como 1 valor consolidado. dcv_v5.md §2.4.

### `Tendência Central` 🆕 (V5 · categoria)

Categoria que reúne **Média · Mediana · Moda** — métricas que descrevem o centro da distribuição. Aparece como sub-bloco em Bloco 2 do Resumo Executivo (Números-âncora) e na aba Resumo Estatístico do Excel. dcv_v5.md §5.1.

### `Dispersão` 🆕 (V5 · categoria)

Categoria que reúne **Desvio Padrão · Variância · IQR · Coeficiente de Variação · Amplitude** — métricas que descrevem o grau de espalhamento dos valores. Aparece como sub-bloco em Bloco 2 do Resumo Executivo. dcv_v5.md §5.1.

### `Distribuição Multimodal` 🆕📌 (V5)

Distribuição com 2 ou mais modas detectadas. V5 retorna múltiplas modas com tratamento em 4 camadas (1 moda · 2-5 modas · ≥6 modas com contagem · caso degenerado sem moda). Warning W-V5-MULTIMODAL (informativo) sinaliza presença · W-V5-MULTIMODAL-EXCESSIVA quando ≥ 6. dcv_v5.md §5.3 · D-105.

### `Skewness` 🆕📌 (V5 · Assimetria)

Métrica calculada que mede a assimetria da distribuição (positivo = cauda longa direita · negativo = cauda longa esquerda). Fórmula amostral: `[N / ((N-1)(N-2))] × Σ((xᵢ - média) / s)³` onde s é DP amostral. Indefinido quando N < 3. Classificação automática em 3 faixas com thresholds default declarados editáveis: Aproximadamente simétrica (\|skew\| < 0,5) · Moderadamente assimétrica (0,5 ≤ \|skew\| < 1,0) · Fortemente assimétrica (\|skew\| ≥ 1,0). Alimenta a leitura "Assimétrica" no Bloco 5 do Resumo Executivo. dcv_v5.md §5.2 · D-105.

### `Critério de Outlier` 🆕📌 (V5 · 3 critérios oficiais)

V5 trabalha com 3 critérios de detecção de outliers · 1 critério ativo por execução · cada critério com threshold default declarado editável em Configurações avançadas:

| Critério | Default declarado | Range editável |
|---|---|---|
| **IQR (Tukey)** | multiplicador 1,5 | 1,0 a 3,0 (passo 0,1) |
| **Z-score** | \|z\| > 3 | 1,5 a 4,0 (passo 0,1) |
| **Percentil** | P5/P95 | P1/P99 · P5/P95 · P10/P90 ou par customizado |

5ª aplicação consecutiva do padrão "thresholds multi-camada editáveis" (V4 D-040 · V7 D-084 · V8 D-078 · V9 D-097 · V5 D-104) — candidato muito forte à formalização. Bloqueio B-V5-MULTIPLOS-CRITERIOS-SIMULTANEOS impede aplicar 2+ critérios simultaneamente. dcv_v5.md §4.10 · D-104.

### `Limite Inferior` e `Limite Superior` 🆕 (V5)

Fronteiras calculadas pelo critério de outlier ativo. Determinam quais valores são classificados como Outlier Superior (acima de Limite Superior) ou Outlier Inferior (abaixo de Limite Inferior). Cálculo:
- IQR: Limite Inferior = Q1 - mult × IQR · Limite Superior = Q3 + mult × IQR
- Z-score: Limite Inferior = média - z × DP · Limite Superior = média + z × DP
- Percentil: Limite Inferior = Pₐ · Limite Superior = Pᵦ
dcv_v5.md §4.10.

### `Classes primárias V5` 🆕 — Normal · Outlier Superior · Outlier Inferior

3 classes mutuamente exclusivas por registro. Vocabulário dual técnico/exibição (D-105):
- `NORMAL` (técnico) → "Dentro do padrão" (exibição)
- `OUTLIER_SUPERIOR` → "Acima do limite"
- `OUTLIER_INFERIOR` → "Abaixo do limite"

Critério: valor relativo a Limite Inferior/Superior calculados pelo critério ativo. dcv_v5.md §5.5 · §5.6.

### `VALOR_NAO_NUMERICO` 🆕 (V5 · classificação especial paralela)

Linha tem valor não-numérico no campo principal que escapou da pré-validação do upload (texto · "N/A" como string · etc). Linha aparece na Base Analítica com esta classe · contada em diagnóstico agregado · não entra no cálculo estatístico (igual a nulo · com nome distinto para auditoria). Adaptação V5 do padrão NULO_MEDIDA — em V4/V7/V9 NULO_MEDIDA aparece como classificação por linha; em V5 NULO genuíno aparece como contagem agregada em diagnóstico (D-073), enquanto VALOR_NAO_NUMERICO é a única classe especial paralela por linha. Warning W-V5-VALOR-NAO-NUMERICO (informativo) quando ≥ 1. dcv_v5.md §5.5 · D-105.

### `Distância do Limite` 🆕📌 (V5 · atributo derivado por registro)

Atributo numérico derivado, aplicável a todos os registros:
- Outlier Superior: `valor - Limite Superior` (positivo)
- Outlier Inferior: `Limite Inferior - valor` (positivo)
- Normal: `min(Limite Superior - valor, valor - Limite Inferior)` (negativo · indica margem para se tornar outlier)

Em critério Z-score, distância em unidades de DP. Em critério Percentil, distância em centiles. Útil para auditoria (quão extremo é cada outlier?) e para investigação (quão perto cada Normal está de virar outlier?). dcv_v5.md §5.5 · D-105.

### `Faixa Percentual` 🆕 (V5 · atributo derivado por registro)

Atributo categórico derivado: em qual decil/quartil cada valor caiu. 6 faixas: P0-P10 · P10-P25 · P25-P50 · P50-P75 · P75-P90 · P90-P100. Útil para leitura comparativa rápida e filtros na exportação Excel. dcv_v5.md §5.5 · D-105.

### `Leituras qualitativas de conjunto` 🆕📌 (V5 · 5 leituras + Equilibrada como default sem destaque)

5 leituras qualitativas multi-aplicáveis (não mutuamente exclusivas · podem coexistir) + 1 default sem destaque. Cada conjunto/segmento pode receber múltiplas leituras simultâneas. Critérios:

| Leitura | Critério | Threshold |
|---|---|---|
| `CONCENTRADA` ("Distribuição concentrada") | CV < 0,3 | Default declarado editável |
| `DISPERSA` ("Distribuição dispersa") | CV ≥ 0,7 | Default declarado editável |
| `ASSIMETRICA_POSITIVA` / `ASSIMETRICA_NEGATIVA` ("Distribuição assimétrica") | \|skewness\| ≥ 0,5 (sinal define positiva/negativa) | Decidido em §5.2 |
| `MULTIMODAL` ("Distribuição multimodal") | ≥ 2 modas detectadas | Decidido em §5.3 |
| `COM_CAUDA_RELEVANTE` ("Distribuição com cauda relevante") | ≥ 5% de outliers detectados | Default declarado editável |
| `EQUILIBRADA` (default sem destaque) | 0,3 ≤ CV < 0,7 e nenhuma outra leitura ativa | — |

Em Modo Segmentado, cada segmento recebe seu próprio conjunto de leituras independente — permite comparar perfis cross-segmentos. Alimenta o Bloco 5 do Resumo Executivo (Leitura qualitativa com síntese). dcv_v5.md §5.5 · §5.7 · D-105.

### `Mapa de Distribuição` 🆕📌 (V5 · aba Excel · coração visual)

Aba dedicada do Excel V5 com **Histograma** (gráfico nativo via openpyxl BarChart) + **Tabela detalhada de Distribuição por Faixas** (6 colunas: Faixa · Limite Inferior · Limite Superior · Frequência · % do Total · % Acumulada). Em Modo Segmentado: 1 conjunto (gráfico + tabela) por segmento. Coração visual da V5 — alinhamento com Mapa de Grupos V7 · Mapa de Perfil V9 · Matriz de Presença V8 · Curva Pareto V10. dcv_v5.md §5.8 · D-107.

### `Regra de binning automático` 🆕 (V5)

Regra que determina o número de faixas do histograma automaticamente. Default declarado: **Sturges** (`k = ⌈log2(N) + 1⌉` · universal · razoável para 90% dos casos). Configurações avançadas oferece: Sturges (default) · Freedman-Diaconis (`largura = 2 × IQR / N^(1/3)` · robusto a outliers) · Scott (`largura = 3,5 × DP / N^(1/3)`) · número fixo (10 · 15 · 20 · 25 · 30 · 50). 9ª aplicação consecutiva do padrão "default declarado editável". dcv_v5.md §5.9 · D-107.

### `Granularidade da base` 🆕 (V5 · default declarado em Modo da Base)

Dimensão declarada pelo usuário em E2: **Individual** (default declarado editável · cada linha é uma observação individual · ex: extrato de transações) ou **Consolidada por chave** (cada linha é uma observação consolidada por chave declarada · ex: planilha já agregada). T-AGRUPA verifica unicidade quando Consolidada. Warning W-V5-GRANULARIDADE-SUSPEITA (informativo) quando motor detecta possível incompatibilidade entre granularidade declarada e estrutura observada. dcv_v5.md §4.1 · D-102.

### `Detecção de subtipo ID` 🆕 (V5 · heurística declarada · requisito Fundação)

Heurística que detecta "ID disfarçado de número" (CPF · CNPJ · ID sequencial) e bloqueia uso como campo principal V5. Critério: campo numérico inteiro com cardinalidade ≥ 90% das linhas + (a) sequência aritmética detectável (incrementos de 1 ou constantes em ≥ 80% das diferenças consecutivas) **ou** (b) comprimento numérico fixo (8+ dígitos com mesma quantidade em 100% das linhas). Quando detectado, bloqueio B-V5-CAMPO-ID com escape "este campo é numérico de fato" (warning permanente W-V5-ID-FORCADO no diagnóstico). Implementação: extensão da inferência semântica (D-008) do motor_upload da Fundação. dcv_v5.md §3.4 · D-103.

### `Top-N · Bottom-N · Outliers detectados` 🆕 (V5 · Bloco 4 do Resumo Executivo)

Adaptação V5 do Bloco 4 padrão D-044 (que em V4/V7/V9 mostra "elementos destacados"). V5 não tem unidade analítica rotulada — adaptação D-073 reformula como "valores destacados" em 3 sub-blocos:
- **Top-N valores** · default N=5 editável (1-20). Em Modo Segmentado: top-N por segmento.
- **Bottom-N valores** · espelho. Em Modo Segmentado: bottom-N por segmento.
- **Outliers detectados** · todos os outliers (Superior + Inferior) ordenados por Distância do Limite decrescente · sem limite default · paginação se > 50.

8ª aplicação consecutiva do padrão "default declarado editável" (Top-N). dcv_v5.md §5.7 · D-106.

### `Aba Dados Brutos V5 — descartada` 🆕

V5 **não tem aba Dados Brutos** no Excel exportado. Linhas originais aparecem na **Base Analítica** (com colunas adicionais de classificação primária + atributos derivados). Contagens estruturais (N total · N válido · N nulos · N não-numérico · N zeros tratados como ausentes) aparecem no **Diagnóstico**. Rastreabilidade plena · sem aba duplicada. **4ª aplicação consecutiva** do padrão "Dados Brutos descartada em favor de Base Analítica + Diagnóstico" (V8 D-078 · V7 D-089 · V9 D-099 · V5 D-108) — candidato muito forte à formalização efetiva. dcv_v5.md §5.11.

### `Escala de cardinalidade V5 · 3 eixos multi-dimensionais independentes` 🆕

Adaptação D-073: V5 herda **estrutura multi-eixo independente de V9** (não hierárquico-aditivo de V7 · não multiplicativo de V8). Os 3 eixos são recortes ortogonais do dado:
- **Eixo 1 · N observações válidas** — Insuficiente (<5 · bloqueio) · Limitado (5-29 · alerta forte) · Adequado (30-499) · Robusto (500-9.999) · Volumoso (10.000-99.999 · alerta performance) · Extenso (100.000+ · alerta forte performance).
- **Eixo 2 · Cardinalidade do Agrupador** (Modo Segmentado) — Ideal (≤50) · Atenção (51-200) · Crítico (201-500) · Excessivo (>500 · bloqueio).
- **Eixo 3 · Diversidade do campo principal** (cardinalidade de valores únicos como % de N válido) — Concentrado (<10% · alerta) · Balanceado (10-90%) · Disperso (>90% · alerta informativo).

dcv_v5.md §8 · D-109.

### `Família E · Estrutura interna do recorte` 🆕📌 (V5 e V6 · par autônomo distante fechado em Fase 0 · 20/04/2026)

V5 e V6 convivem como visões da Família E. As duas operam sobre recortes distintos da base — V5 univariado numérico (um campo numérico por execução) · V6 bivariado categórico (cruzamento de dois campos categóricos). Não compartilham transversais centrais nem apresentam fronteira navegada operacionalmente. O que une V5 e V6 é o nível mais abstrato: ambas expõem propriedades estruturais internas de um recorte da base sem comparar com referência externa, sem benchmark interno por grupo, sem eixo ordenado, sem total geral. **Família com par operacionalmente distante** — sem retroação diferida formal V5→V6 (D-110 lado 1 via V5 · D-121 lado 2 via V6 cumprindo o gancho). Adaptação D-073 ao próprio método de posicionamento de família: famílias com par operacional próximo (B · D) merecem tabela de retroação diferida com células *(a confirmar)* (D-060 e D-081); Família E com par distante merece declaração enxuta de convivência sem retroação diferida. **Família E fechada em Fase 0 com par completo após aprovação de DCV-V6 em 20/04/2026.**

---

### Seção 5.V6 · Conceitos específicos da V6 🆕

V6 é a 2ª e última visão da Família E · Estrutura interna do recorte. DCV-V6 aprovado em 20/04/2026 com 16 pendências fechadas em sessão única e 11 decisões (D-111 a D-121). Vocabulário consolidado em §13 do DCV-V6 · ~24 termos canônicos + 6 pares duais + 6 anti-glossário.

### `Relacionamento entre Dimensões` 🆕📌 (V6)

Nome analítico da V6. Responde *"como dois campos categóricos se relacionam entre si dentro de uma base, quais combinações concentram valor, quais têm baixa relevância, quais não aparecem?"*. Opera sobre **matriz de cruzamento** formada pelo produto cartesiano observado entre dois campos categóricos da mesma base · com medida opcional (Contagem · Soma · Média). Entrega leitura estrutural do relacionamento bivariado, incluindo classificação de densidade por célula e exposição explícita de células ausentes como conteúdo primário.

### `Eixo 1` e `Eixo 2` 📌 (V6)

Os dois campos categóricos que formam os eixos da matriz. Eixo 1 ocupa as linhas · Eixo 2 ocupa as colunas. Ambos precisam ser classificados como **categórico-elegíveis** pelo motor_base (D-113). O mesmo campo não pode ocupar os dois eixos simultaneamente (B-V6-EIXOS-IGUAIS · invariante matemático). Campo numérico contínuo como Eixo é bloqueio escapável (B-V6-EIXO-NUMERICO-CONTINUO). Sinônimos conceituais: Dimensão Linha (Eixo 1) e Dimensão Coluna (Eixo 2) são aceitos em microcopy contextual mas termo canônico técnico é Eixo 1/Eixo 2 (neutros posicionalmente). Nome analítico configurado pelo usuário (ex: "Categoria", "Região") aparece na tela e no Excel em lugar dos rótulos técnicos.

### `Célula` 📌🆕 (V6 · unidade analítica)

Unidade analítica da V6. Slot da matriz representado pelo par (Eixo1=X ∧ Eixo2=Y) no produto cartesiano observado. Cada célula recebe classificação (estrutural + densidade), Valor da Medida (ou null se ausente), atributos derivados, e vira 1 linha na Base Analítica. Distinção vs *Combinação*: combinação é o par de valores (conceito genérico); célula é o slot posicional na matriz (conceito visual/operacional). Operacionalmente os dois termos são quase sinônimos, mas em prosa analítica usa-se **célula** para destacar o aspecto matricial e **combinação** para destacar o aspecto do par.

### `Combinação` 📌 (V6)

Par de valores (Eixo1=X, Eixo2=Y). Termo usado em microcopy de tela, Resumo Executivo e prosa. Tecnicamente equivalente a Célula; diferença é de contexto discursivo (ver Célula).

### `Produto Cartesiano Observado` 📌🆕 (V6 · D-114)

Produto cartesiano entre os **conjuntos de valores que aparecem em cada eixo na base ativa** (não o produto teórico entre domínios completos declarados externamente). Formalmente: se V_Eixo1 = {valores únicos em Eixo1 na base} e V_Eixo2 = {valores únicos em Eixo2 na base}, o produto cartesiano observado é V_Eixo1 × V_Eixo2. Cardinalidade = |V_Eixo1| × |V_Eixo2|. Nulos nos eixos não entram em V_Eixo1 nem V_Eixo2 (pré-excluídos com W-V6-EIXO-NULO-EXCLUIDO). **Domínio declarado pelo usuário** (para detectar ausências de negócio, não apenas observadas) fica em roadmap P-V6-03-DOMINIO-DECLARADO-Evo.

### `Combinação Presente` · `Combinação Ausente` 📌🆕 (V6)

Célula do produto cartesiano observado pode ser **Presente** (aparece ≥ 1 linha da base · classificação estrutural `PRESENTE`) ou **Ausente** (pertence ao produto cartesiano mas não aparece na base · classificação `AUSENTE`). Distinção formalizada como **camada primária estrutural** separada da classificação de densidade (Dominante/Relevante/Residual), que se aplica apenas a presentes. Célula ausente tem Valor da Medida = null (nunca 0 · honra D-023 V2) e não entra em ranking, participação ou total da matriz — mas **é conteúdo analítico primário** (D-076 na sua aplicação canônica mais forte · aba Excel dedicada "Combinações Ausentes").

### `Matriz` e `Total da Matriz` 📌 (V6)

**Matriz** é a estrutura completa: |V_Eixo1| × |V_Eixo2| células, incluindo presentes e ausentes. **Total da Matriz** é o somatório do Valor da Medida sobre todas as células **presentes** (ausentes têm valor null, não entram). Total da Matriz é o denominador da Participação Individual de cada célula presente.

### `Densidade` 🆕 (V6 · métrica de conjunto)

% de células presentes sobre total do produto cartesiano observado (N presentes / N possíveis × 100). Métrica de Bloco 2 do Resumo Executivo. Distingue matriz **densa** (alta % de presentes · poucas lacunas · tende a leitura "Dispersa" ou "Equilibrada") de matriz **esparsa** (baixa % de presentes · muitas lacunas · dispara leitura "Esparsa" quando densidade ≤ 30%).

### `Modo da Base V6` 🆕📌 (V6 · D-111)

Declaração explícita pelo usuário com default declarado pelo motor (heurística de cardinalidade da amostragem):
- **Transacional** (default quando média de linhas por par ≥ 1.5) · múltiplas linhas podem cair na mesma célula · T-AGRUPA consolida via regra correspondente à Medida
- **Pré-agregado** · cada célula já vem como linha única · T-AGRUPA em no-op validado (verifica unicidade · W-V6-CHAVE-NAO-UNICA se há duplicidade)

V6 é **9ª consumidora de T-AGRUPA com consumo padrão** — não adaptação V5-específica. Reforça o tronco comum da família V4/V7/V8/V9.

### `Classes primárias V6 · Dominante · Relevante · Residual` 🆕📌 (D-116)

3 classes de densidade aplicáveis apenas a **células presentes**. Vocabulário dual técnico/exibição:

| Técnico | Exibição | Critério |
|---|---|---|
| `DOMINANTE` | "No topo" · "Núcleo da matriz" | Participação Acumulada ≤ 20% (default editável) |
| `RELEVANTE` | "Corpo" · "Intermediária" | Nem Dominante nem Residual |
| `RESIDUAL` | "Periférica" · "Cauda" | Participação Individual < 2% (default editável) |

**Racional do 20% (vs V4/V10 com 80% ABC):** V6 é bivariada e matrizes densas têm muitas células competindo próximo ao topo · corte rigoroso (20%) destaca genuinamente o **núcleo** da matriz. Aplicação D-073 "herança adaptada à natureza analítica". Microcopy de exibição **nunca** sugere juízo de valor (Dominante ≠ boa · Residual ≠ ruim).

### `Classificações especiais paralelas V6` 🆕 (D-116)

**`AUSENTE`** · célula do produto cartesiano observado sem ocorrência na base · aplicação canônica D-076 · microcopy "Não observada" · "Sem ocorrência" (nunca "faltante").

**`PRESENTE_SEM_VALOR`** · célula presente estruturalmente com Valor da Medida null (raro em Pré-agregado · D-115). Não entra em ranking de densidade; fica no final com W-V6-CELULA-PRESENTE-SEM-VALOR.

### `Faixa de Participação` 🆕 (V6 · atributo derivado por célula · D-116)

Enum de 6 valores indicando em qual faixa do acumulado a célula caiu. Default declarado editável (9ª aplicação consecutiva do padrão "default declarado editável"):
- **TOPO** (0-20%)
- **ALTO** (20-40%)
- **MEDIO** (40-60%)
- **BAIXO** (60-80%)
- **CAUDA** (80-100%)
- **SEM_FAIXA** (células ausentes ou presentes sem valor)

Análogo a Faixa Percentual V5. Útil para leitura comparativa rápida na Base Analítica e no Resumo Executivo Bloco 3.

### `Leituras qualitativas da matriz V6` 🆕📌 (D-117 · 5 leituras + Equilibrada default)

5 leituras multi-aplicáveis que qualificam a matriz globalmente no Bloco 5 do Resumo Executivo. Thresholds default declarado editáveis em Configurações avançadas:

| Leitura | Critério (default editável) |
|---|---|
| **Concentrada** | Concentração no topo ≥ 50% |
| **Dispersa** | Densidade ≥ 75% AND Concentração no topo ≤ 25% |
| **Esparsa** | Densidade ≤ 30% (muitas lacunas) |
| **Assimétrica por Eixo** | Top-5 linhas ≥ 80% OR top-5 colunas ≥ 80% |
| **Com lacunas estruturais relevantes** | ≥ 20% de células ausentes em combinações de alto total |
| **Equilibrada** (default sem destaque) | Nenhuma outra leitura ativa |

Cada matriz pode receber **múltiplas leituras simultâneas** (ex: Concentrada + Assimétrica por Eixo + Com lacunas relevantes). Síntese narrativa de 1-2 frases é gerada a partir das leituras ativas.

### `Matriz de Cruzamento` 🆕📌 (V6 · aba Excel · coração visual · D-118)

Aba dedicada do Excel que materializa visualmente a contribuição analítica primária da V6. Alinhamento com padrão "coração visual" (7ª aplicação consecutiva após V4/V7/V8/V9/V5/V10). Componentes:
- Tabela matricial principal (Eixo 1 linhas · Eixo 2 colunas) com formatação condicional por classe de densidade (Dominante verde-intenso · Relevante verde-médio · Residual cinza · Ausente fundo diferenciado)
- Células ausentes com marcador visual distinto ("—" ou fundo cinza-claro · honra D-023 V2)
- Totais marginais opcionais (default ligado · editável)
- Gráfico ColumnChart empilhado 100% (heatmap real não suportado nativamente em openpyxl · roadmap P-V6-06-HEATMAP-NATIVO-Evo)
- Paginação quando matriz > 30×30

Requisito novo para `exportacao.py` da Fundação: formatação condicional de matriz + ColumnChart empilhado 100% + paginação.

### `Combinações Ausentes` 🆕📌 (V6 · aba Excel dedicada · D-119)

Aba Excel específica V6 · distintiva da visão · análoga à aba "Movimentações" específica V8. Lista todas as células ausentes do produto cartesiano observado · ordenadas por (Total do Eixo1 + Total do Eixo2) decrescente (heurística: ausências em eixos "grandes" aparecem primeiro · sinaliza lacunas analiticamente mais relevantes). Aplicação canônica de D-076 cristalizada em aba própria. Requisito novo para `exportacao.py`.

### `Escala de cardinalidade V6 · 3 eixos com produto da matriz como eixo V6-específico` 🆕🔧 (D-120)

Aplicação D-073 ao método de escala de cardinalidade · 15ª aplicação documentada. Natureza V6 é **bivariada simultânea** · diferente de V5 multi-eixo independente ortogonal, V7 hierárquica-aditiva, V8 multiplicativa. Três eixos independentes:

- **Eixo 1 · Cardinalidade de Eixo 1** · 4 patamares (P1 2-30 · P2 31-100 · P3 101-200 · P4 >200 escapável)
- **Eixo 2 · Cardinalidade de Eixo 2** · patamares idênticos · independente
- **Eixo 3 · Cardinalidade da Matriz (produto N × M)** · eixo estrutural V6-específico · 4 patamares (P1 ≤ 900 · P2 901-2.500 · P3 2.501-10.000 · P4 > 10.000 escapável)

### `Modo Transacional` vs `Modo Pré-agregado` (V6) 📌 (D-111)

Declaração do usuário sobre granularidade da base. Análogo ao conceito em V7/V8/V9. **Modo Transacional** (default) · T-AGRUPA consolida múltiplas linhas da mesma célula conforme regra derivada da Medida (Contagem/Soma/Média). **Modo Pré-agregado** · T-AGRUPA em no-op validado · cada célula já vem como linha única.

### `T-AGRUPA em V6 · consumo padrão` 🆕🔧 (V6 · 9ª consumidora · D-111)

V6 é **9ª consumidora de T-AGRUPA com consumo padrão** · não adaptação V5-específica. Usa 3 das 5 regras canônicas (Contagem · Soma · Média) no MVP. Máx/Mín em roadmap P-V6-04-MAX-MIN-Evo. Reforça o tronco comum da família V4/V7/V8/V9 onde T-AGRUPA consolida antes do cálculo · 5ª aplicação consecutiva do padrão "consolidação obrigatória pré-cálculo".

### `T-RANK em V6 · 4 níveis bivariado` 🆕🔧 (V6 · 8ª consumidora de T-RANK · D-115)

V6 é **8ª consumidora de T-RANK** com regra V6-específica em 4 níveis (aplicação D-073 · paridade estrutural com V7 D-088 e V9 D-096):
1. Valor da Medida · decrescente
2. Valor alfabético de Eixo 1 · crescente
3. Valor alfabético de Eixo 2 · crescente
4. Ordem de inserção da **primeira ocorrência do par** na base ativa · crescente

Tolerância de empate em valor: 1e-9 (herança T-RANK default). Escopo = global no MVP (modo Segmentado em roadmap).

### `Ordenação de cálculo vs ordenação de exibição` 🆕📌 (V6 · D-115)

V6 tem **duas ordenações coexistentes** com propósitos distintos:
- **Ordenação de cálculo** · T-RANK V6-específica 4 níveis · usada para ranking, participação acumulada, classificação de densidade
- **Ordenação de exibição da matriz** · default declarado editável em Configurações avançadas · 3 opções (alfabética crescente default · por total do eixo · manual) · para TEMPORAL detectado, default cronológico crescente (W-V6-EIXO-ORDEM-CRONOLOGICA)

Separação formalizada em D-115. Coração visual (Matriz de Cruzamento) usa ordenação de exibição; Ranking de Combinações (aba Excel) usa ordenação de cálculo.

### `Concentração no topo` 🆕 (V6 · métrica de Bloco 2 do Resumo Executivo)

Participação cumulativa das N% primeiras células, onde N = limiar Dominante (default 20%). Métrica de Bloco 2 que alimenta a leitura qualitativa **Concentrada** (≥ 50% · default editável).

### `Tipo de Medida em V6` 🆕📌 (V6 · D-112)

Separação explícita entre **tipo do campo** (natureza semântica D-025/D-036: Aditivo · Relativo · Não aditivo · Booleano · Estado) e **regra de agregação** (operação T-AGRUPA: Contagem · Soma · Média). 5ª aplicação cross-visão do padrão D-025/D-036. Em V6, a "Medida" inclui os dois planos:
- **Regra de agregação** declarada pelo usuário · Contagem (dispensa campo numérico) · Soma ou Média (exige Campo Numérico)
- **Tipo do campo** classificado pelo motor_base · determina comportamento (Aditivo execução normal · Relativo warning · Não-aditivo-ID bloqueio com escape herdado de V5 D-103 · Booleano só com Contagem · Estado bloqueado como Medida com redirecionamento)

### `Categórico-elegível` 🆕📌 (motor_base · requisito novo Fundação · D-113)

Classificação estrutural de coluna no motor_base · novo metadado `column_meta.tipo_estrutural` com 5 valores enum:
- `CATEGORICO_ELEGIVEL` · texto, subtipo ID (D-103), numérico inteiro com cardinalidade ≤ 200, Booleano · aceito como Eixo V6 sem warning
- `NUMERICO_CONTINUO` · numérico não-inteiro ou inteiro > 200 sem padrão ID · bloqueio B-V6-EIXO-NUMERICO-CONTINUO com escape
- `TEMPORAL` · data/timestamp · aceito com warning W-V6-EIXO-TEMPORAL e microcopy redirecional V3/V8
- `BOOLEANO` · 2 valores únicos · aceito sem warning (caso legítimo · matriz 2×N)
- `VAZIO` / `AMBIGUO` · >90% nulos ou tipo inconferível · bloqueio sem escape

Requisito útil para V6 (elegibilidade de eixo) e para M2 e visões futuras. Heurística detalhada fica no motor_base (spec_fundacao.md a escrever no G-FUND).

### `Anti-glossário V6` 🆕 (6 termos rejeitados · T-03 + §13.3 DCV-V6)

Termos explicitamente **a evitar** em V6 por violarem postura analítica declarativa (C.5 + D-076 + §8.2 do prévio V6):

| Termo | Por que evitar | Usar no lugar |
|---|---|---|
| *Faltante* | Sugere obrigatoriedade de existência · prescritivo | *Ausente* · *Não observada* |
| *Deveria existir* | V6 não declara expectativa de negócio | (conceito recusado) |
| *Erro de cruzamento* · *Combinação inválida* | V6 não diagnostica causa | *Combinação ausente* · *Célula vazia* |
| *Dominante = boa* · *Residual = ruim* | V6 não atribui qualidade | Código técnico em motor · microcopy neutra em tela |
| *Preenchimento esparso* | Linguagem de banco, não de análise | *Matriz pouco densa* · *Densidade baixa* |
| *Filtrar combinações ausentes* | Ausência é conteúdo primário (D-076) | *Exibir apenas combinações presentes* (com microcopy explícita) |

---



## 6. Warnings (códigos)

Warnings são **alertas não-bloqueantes** emitidos pelo motor ou pela visão. Não são erro — são aviso para o usuário revisar.

### Warnings da V2 🆕 (consolidados na Sessão 1 do DCV-V2)

Catálogo completo da V2 após refino do DCV. Substitui completamente warnings W01-W08 e W-AGG da spec antiga.

- **W-V2-EST** — ≥1 registro com classificação `AUSENTE_*`. Contagem detalhada por agrupador no Diagnóstico (substitui W06 antiga). D-022.
- **W-V2-BZ** — ≥1 registro `PRESENTE_AMBOS` com Origem=0 e Comparado≠0. Variação não calculável (base zero). D-022.
- **W-V2-NULL** — ≥1 registro com classificação `NULO_*`. Contagem por categoria + lista por agrupador (substitui W01 antiga, conceito reformulado). D-023.
- **W-V2-NULL-MASS** — >20% dos registros do campo analisado têm nulo. Sinaliza qualidade de dado deteriorada. D-023.
- **W-V2-AGG** — Tipo numérico relativo ou não-aditivo + agrupadores. Informativa: registra método de consolidação aplicado. Substitui W07 antiga, agora informativa não alerta de surpresa. D-024.
- **W-V2-MIX** — Coluna discriminadora POR_LINHAS com tipos mistos (numérico + texto + datas). Motor caiu em ordenação alfabética; pede revisão da base. D-026.
- **W-V2-NMANY** — Coluna discriminadora com >50 valores únicos em Modo 4. Sugere filtragem prévia. D-026.
- **W-V2-N1** — Coluna discriminadora POR_LINHAS com 1 valor único. Erro: impossível comparar (gatilho de bloqueio operacional). D-026, D-032.
- **W-V2-N0** — Coluna discriminadora POR_LINHAS vazia. Erro: estrutura inválida (gatilho de bloqueio operacional). D-026, D-032.
- **W-V2-AGRUP-MUITOS** — ≥6 agrupadores efetivamente usados. Confirma escolha de granularidade fina (substitui W03 antiga, lógica diferente: era >3, agora ≥6). D-027.
- **W-V2-MOD-PARCIAL** — Modelo aplicado mas algum campo não casou. Lista campos não-casados. D-030.
- **W-V2-MOD-INCOMP** — Modelo aplicado mas estrutura incompatível com nova base. Etapas dependentes zeradas. D-030.

### Warnings da V1 🆕

- **W-V1-TOL** — Tolerância absorveu diferenças em N registros classificados como Conciliado. Disparado por P-V1-05 quando ≥ 1 registro tem diferença não-zero dentro da tolerância declarada pelo usuário. Listagem detalhada no Diagnóstico: chave, campo, diferença absorvida.
- **W-V1-DUP** — Duplicidade em N chaves de Origem ou Comparado. Disparado por P-V1-03+04 quando ≥ 1 chave aparece duplicada. V1 preserva todas as ocorrências (Princípio C.5, sem T-AGRUPA). Listagem: chave, base, N° ocorrências, soma do valor.
- **W-V1-AMB** — Ambiguidade em N chaves em match não-exato produzindo múltiplos candidatos. Disparado por P-V1-03+04 quando ≥ 1 chave casa com mais de um candidato via modo Contém/Inicia com/Termina com. Listagem: chave Origem, chaves candidatas, campo responsável.

### Warnings da V4 🆕 (consolidados na Sessão DCV-V4)

Catálogo completo da V4 após refino do DCV. 20 warnings organizados em 3 tipos.

**Bloqueios (motor para execução):**

- **W-V4-N0** — Coluna discriminadora POR_LINHAS vazia. Estrutura inválida. D-039.
- **W-V4-N1** — Coluna discriminadora POR_LINHAS com 1 valor único. POR_LINHAS não faz sentido; reconfigurar. D-039.
- **W-V4-MEDIDAS-MIN** — Modo 3 configurado com menos de 2 medidas selecionadas no desempilhamento. D-039.
- **W-V4-TOTAL-ZERO** — Total Geral = 0, impossível calcular participação. Causa identificada: base toda nula, cancelamento positivo/negativo, ou outro. Microcopy adaptativo por causa. D-043.

**Alertas (motor avisa antes ou durante configuração; não bloqueia):**

- **W-V4-NULL-MASS** — >20% dos registros com NULO_MEDIDA. Sinaliza qualidade de dado deteriorada. D-038.
- **W-V4-MIX** — Tipos mistos na coluna discriminadora POR_LINHAS (numérico + texto + datas). Motor caiu em ordenação alfabética; pede revisão. D-039.
- **W-V4-NMANY** — Coluna discriminadora POR_LINHAS com >50 valores únicos. Sugere filtragem prévia. D-039.
- **W-V4-AGRUP-MUITOS** — ≥6 agrupadores efetivamente usados. Confirma escolha de granularidade fina. Herança de D-027.

**Informativas (motor registra fato no Diagnóstico):**

- **W-V4-TIPO-DECL** — Registra opção do default declarado para tipo relativo/não-aditivo. D-036.
- **W-V4-NULL** — Contagem de registros com NULO_MEDIDA (excluídos do cálculo, preservados na listagem). D-038.
- **W-V4-AGRUP-SEMVALOR** — Contagem de registros sob rótulo `(sem valor)` em agrupador. D-038.
- **W-V4-NEGATIVOS** — Registra opção escolhida no default declarado de negativos (valores líquidos / separar pos-neg / valor absoluto) + contagem. D-038.
- **W-V4-ABC-CUSTOM** — Limiares ABC diferentes do default (80/95) foram usados. D-040.
- **W-V4-EMPATE** — N empates resolvidos por regra secundária ou terciária de T-RANK. Lista casos. D-041.
- **W-V4-MD3-AUSENTE** — Contagem de elementos com ausência em alguma medida do Modo 3 (elemento existe em uma medida, não em outra). D-042.
- **W-V4-MD3-HETERO** — Modo 3 rodou com tipos heterogêneos + registra escolha do usuário no bloco declarado. D-042.
- **W-V4-LEITURA-CUSTOM** — Faixas de síntese do Bloco 5 do Resumo Executivo customizadas (diferentes do default 80/40 para concentração ou 70/40 para coerência). D-044.
- **W-V4-MOD-PARCIAL** — Modelo aplicado mas algum campo não casou com nova base. Lista campos não-casados. D-030 herdada.
- **W-V4-MOD-INCOMP** — Modelo aplicado mas estrutura incompatível (ex: Modo 2/3 em base sem medidas suficientes). Etapas dependentes zeradas. D-030 herdada.

### Warnings da V10 🆕 (consolidados na Sessão DCV-V10)

Catálogo da V10 após refino do DCV. 5 warnings V10-específicos, todos informativos. V10 **também herda** os warnings V4 aplicáveis (W-V4-NULL, W-V4-NULL-MASS, W-V4-AGRUP-SEMVALOR, W-V4-NEGATIVOS, W-V4-TIPO-DECL, W-V4-EMPATE, W-V4-TOTAL-ZERO com microcopy adaptado Pareto, W-V4-N0, W-V4-N1, W-V4-MIX, W-V4-NMANY, W-V4-ABC-CUSTOM quando limiar A é editado, W-V4-AGRUP-MUITOS, W-V4-MOD-PARCIAL, W-V4-MOD-INCOMP).

**Informativas (motor registra fato no Diagnóstico):**

- **W-V10-CURVA-TRUNC** — Visualização da Curva Pareto agregou itens além do limite de cardinalidade (default 50) em barra "Demais". Tabela e Excel mostram todos os itens individualmente. D-045.
- **W-V10-CORTE-APERTADO** — Diferença < 2 pp (default editável) no acumulado entre último vital e primeiro não-vital. Leitura secundária de Corte do Bloco 5 indica que o corte é apertado. D-045.
- **W-V10-CLASSE-A-VAZIA** — Nenhum item atinge o limiar A isoladamente. Distribuição muito pulverizada — Pareto não se aplica fortemente. Microcopy sugere V4 Modo 2 ou reduzir limiar. D-045.
- **W-V10-BASE-MINIMA** — Base com 1-2 itens. Todos na Classe A por construção. Pareto não significativo. D-045.
- **W-V10-MODELO-CONVERTIDO** — Modelo de outra visão foi aplicado com mapeamento cross-visão (V4 Modo 2 → V10 ou V10 → V4 Modo 2). Registra parâmetros defaulted e descartados. Warning simétrico registrado na visão pareada. D-046.

### Warnings da V11 🆕 (consolidados no DCV-V11 aprovado)

Catálogo completo da V11 após refino. 13 warnings organizados em 3 tipos. Substitui lista candidata preliminar.

**Alertas (motor avisa; não bloqueia):**

- **W-V11-SEM-CONTEXTO** — Menos de 2 campos contextuais configurados por lado. Score fica dependente de poucos sinais; analista informado proativamente na configuração. dcv_v11.md §4.2.
- **W-V11-VALOR-REPETIDO-MASS** — > 30% dos valores aparecem 3+ vezes em alguma das bases. Sinaliza cenário de ambiguidade estrutural alta; sugere revisão manual mais extensa. dcv_v11.md §5.4.
- **W-V11-PONTE-RESIDUO** — Conferência da Ponte (Bloco 3) não zera. Indica movimento conciliado com divergência de valor absorvendo parte da diferença, ou inconsistência entre saldos declarados e movimentos da base. dcv_v11.md §6.6.

**Material (registra fato relevante ao achado, com detalhamento):**

- **W-V11-TOL** — Tolerância absorveu diferenças em N pareamentos; registra soma da diferença absorvida + lista de casos no Diagnóstico. Herança conceitual de W-V1-TOL; em V11 papel duplo (Passe 1 classifica, Passe 2 filtra). dcv_v11.md §4.3.

**Informativas (motor registra fato no Diagnóstico):**

- **W-V11-MAP-INFERIDO** — Mapeamento semântico aceito por default sem edição explícita. Permite auditoria pós-análise. dcv_v11.md §4.1.
- **W-V11-COMP-CAMPOS-NULOS** — Composição contextual resultou em string vazia por nulos em todos os campos componentes de N registros. dcv_v11.md §4.2.
- **W-V11-PESOS-CUSTOM** — Pesos entre campos contextuais customizados pelo usuário (diferentes do default por heurística de distintividade). dcv_v11.md §4.4.
- **W-V11-LIMIAR-P1-CUSTOM** — Limiar do Passe 1 customizado (diferente de 0,70 default). dcv_v11.md §4.4.
- **W-V11-LIMIAR-P2-CUSTOM** — Limiar do Passe 2 customizado (diferente de 0,30 default). dcv_v11.md §4.4.
- **W-V11-MULT-CAND** — Registros com N ≥ 2 candidatos resolvidos por score + T-RANK. dcv_v11.md §5.4.
- **W-V11-SCORE-LIMITE** — Pareamentos com score na janela ±0,05 da fronteira entre categorias. Candidatos a revisão manual. dcv_v11.md §6.2.
- **W-V11-ALLOC-EMPATE** — Alocação gulosa resolveu empate de score por T-RANK; lista os casos. dcv_v11.md §5.1.
- **W-V11-PAREAMENTO-LARGO** — Excel gerado com > 50 colunas na aba Pareamentos. Sugere configurar subset na próxima execução; default persiste em "todas as colunas" (auditabilidade máxima — C.5). dcv_v11.md §6.4.

### Warnings da V3 🆕 (consolidados no refino DCV-V3)

**27 warnings V3** catalogados em 3 categorias (7 bloqueios · 3 alertas · 17 informativos).

**Bloqueios (7):**

- **W-V3-N0-EIXO** — Coluna discriminadora do eixo POR_LINHAS com 0 valores únicos. Bloqueio operacional. D-070.
- **W-V3-N1-EIXO** — Coluna discriminadora do eixo POR_LINHAS com 1 valor único. Bloqueio (impossível sequência). D-070.
- **W-V3-AGRUP-MUITOS** (bloqueio 8+) — 8 ou mais agrupadores declarados. Bloqueio com sugestão V6/V9. D-070.
- **W-V3-PONTOS-MIN** — Intervalo efetivo < 3 pontos após pivot, seleção prévia e De/Até. Bloqueio operacional (mínimo P0.7). D-064 · D-070.
- **W-V3-INTERVALO-INVALIDO** — De > Até (intervalo invertido). Bloqueio operacional. D-064.
- **W-V3-TIPO-INCOMPAT** — Medida de tipo estado/situação. Bloqueio com redirecionamento V8/V6. D-066.
- **W-V3-EIXO-AGRUP-COLISAO** — Mesmo campo declarado como eixo e agrupador simultaneamente. Bloqueio (motor não corrige silenciosamente). D-070.
- **W-V3-NMANY** — Resultado > 500.000 linhas. Bloqueio operacional. D-070.

**Alertas (3):**

- **W-V3-AGRUP-MUITOS** (alerta 6-7) — 6 ou 7 agrupadores declarados. Alerta + estimativa de linhas em tempo real. D-070.
- **W-V3-NULL-MASS** — > 20% dos registros com nulo na medida. Sinaliza qualidade de dado deteriorada. D-066.
- **W-V3-EIXO-LACUNA-MASSIVA** — > 30% dos pontos esperados no eixo ausentes (só eixos com detecção ativa: temporal e ordinal com prefixo). Alerta sem bloqueio — usuário decide. D-065.

**Informativos (17):**

- **W-V3-EIXO-TIPO-INFERIDO** — Tipo de eixo aceito por default sem edição. D-061.
- **W-V3-EIXO-ORDEM-MANUAL** — Ordem manual aplicada sobre eixo temporal/ordinal (desvio do default canônico). D-061.
- **W-V3-EIXO-PIVOT** — Pivot POR_LINHAS → POR_COLUNAS aplicado. D-062.
- **W-V3-EIXO-PONTOS-MUITOS** — Bloco de seleção de pontos ativado (10+ pontos únicos na discriminadora). D-062.
- **W-V3-EIXO-ESTRUTURA-INFERIDA** — Estrutura POR_COLUNAS/POR_LINHAS aceita por default sem edição. D-062.
- **W-V3-EIXO-SELECAO+INTERVALO** — Seleção prévia combinada com De/Até na mesma execução. D-062 · D-064.
- **W-V3-EIXO-LACUNA** — Lacunas detectadas no eixo (só eixos com detecção ativa). D-065.
- **W-V3-AGRUP-AUSENCIA-PONTO** — Par (agrupador × ponto) em ausência dentro do intervalo efetivo. D-065.
- **W-V3-AGRUP-POUCOS-PONTOS** — Agrupador com < 3 pontos efetivos; não produz análise sequencial mas aparece com flag. D-066.
- **W-V3-INTERVALO-DEFAULT** — De/Até aceitos por default sem edição explícita. D-064.
- **W-V3-INTERVALO-AJUSTE-INICIO** — De declarado anterior ao primeiro ponto da base; ajustado (AJUSTE_LEVE). D-064.
- **W-V3-INTERVALO-AJUSTE-FIM** — Até declarado posterior ao último ponto da base; ajustado (AJUSTE_LEVE). D-064.
- **W-V3-TIPO-DECL** — Tipo de medida aceito por default sem edição. D-066.
- **W-V3-TIPO-REL** — Tipo relativo/não-aditivo: opção declarada pelo usuário (analisar/outra/média ponderada). D-066.
- **W-V3-NEGATIVOS** — Opção de negativos declarada pelo usuário (líquidos/absoluto) + contagem. D-066.
- **W-V3-NULL** — Contagem de registros com nulo na medida. D-066.
- **W-V3-SEMA-DECL** — Semântica aceita por default sem edição. D-067.
- **W-V3-SEMA-CUSTOM** — Semântica declarada diferente do default proposto pelo motor. D-067.
- **W-V3-COMP-EVOLUCAO** — Evolução complementar de Origem/Comparado ligada no Modo Comparativo. D-067.
- **W-V3-LEITURA-CUSTOM** — Faixas de leitura descritiva customizadas (Bloco 5 do Resumo Executivo). D-069.

### Warnings da V8 🆕 (consolidados no refino DCV-V8)

**37 warnings V8** catalogados em 3 categorias (9 bloqueios · 10 alertas · 18 informativos). Maior volume de warnings até agora no projeto — justificado pela complexidade V8 de três eixos multiplicativos de cardinalidade (entidades × pontos × grupos).

**Bloqueios (9):**

- **W-V8-INTERVALO-INVALIDO** — De > Até (intervalo invertido). Bloqueio operacional. D-073.
- **W-V8-PONTOS-MIN** — Intervalo efetivo < 2 pontos. Bloqueio (com 1 ponto só, toda entidade é Novo; resultado analiticamente vazio). D-073.
- **W-V8-EIXO-ENTIDADE-COLISAO** — Mesmo campo declarado como eixo e entidade simultaneamente. Bloqueio (rastreamento circular). D-079.
- **W-V8-AGRUP-ENTIDADE-COLISAO** — Mesmo campo declarado como agrupador e entidade. Bloqueio (segmentação circular). D-079.
- **W-V8-EIXO-AGRUP-COLISAO** — Mesmo campo declarado como eixo e agrupador. Bloqueio herdado V3 D-070.
- **W-V8-AGRUP-MUITOS** — 7+ agrupadores declarados. Bloqueio com sugestão V6/V9. Escala mais conservadora que V3 (V3 bloqueia em 8+) porque agrupadores V8 multiplicam grupos. D-079.
- **W-V8-VOLUME-INVIAVEL** — Células totais (entidades × pontos × grupos) > 1.000.000. Limite físico Excel. D-079.
- **W-V8-ENTIDADES-INVIAVEL** — Entidades por grupo > 10.000. Leitura e paginação inviável. D-079.
- **W-V8-PONTOS-INVIAVEL** — Pontos do eixo efetivo > 200. Matriz horizontal não renderiza legível. D-079.

**Alertas (10):**

- **W-V8-PONTOS-LIMITADO** — Intervalo efetivo = 2 pontos. Executa com alerta (classificação estruturalmente válida mas leitura de ciclo de vida limitada). Divergência justificada com V3 (que bloqueia em < 3) via padrão "herança adaptada à natureza analítica". D-073.
- **W-V8-DUPLICIDADE-PREAGREGADA** — Duplicidade detectada em modo declarado pré-agregado. Usuário aceita e processa com regra escolhida, revisa base, ou alterna modo. D-074.
- **W-V8-MEDIDA-CATEGORICA** — Campo de medida declarado é tipo estado/situação. Executa com alerta; valor exibido como categórico na Base Analítica, não agregável. D-075.
- **W-V8-EIXO-LACUNA-MASSIVA** — > 30% dos pontos esperados ausentes (só eixos com detecção ativa: temporal e ordinal com prefixo). Alerta sem bloqueio. D-076.
- **W-V8-EIXO-GRANULARIDADE-MISTA** — 2+ granularidades distintas detectadas em eixo temporal. Alerta forte com confirmação obrigatória. D-076.
- **W-V8-ENTIDADES-MUITAS** — 500-2000 entidades por grupo. Alerta + sugestão de refinar recorte. D-077.
- **W-V8-ENTIDADES-CRITICO** — 2000-10.000 entidades por grupo. Alerta forte com confirmação. D-079.
- **W-V8-VOLUME-ALTO** — 100.000-500.000 células totais. Confirmação obrigatória. D-079.
- **W-V8-VOLUME-CRITICO** — 500.000-1.000.000 células totais. Confirmação forte + performance degradada esperada. D-079.
- **W-V8-AGRUP-MUITOS-CONFIRMA** — 6 agrupadores declarados (antes do bloqueio em 7+). Confirmação obrigatória extra. D-079.

**Informativos (18):**

- **W-V8-EIXO-TIPO-INFERIDO** — Tipo de eixo aceito por default sem edição. D-071 (herança T-EIXO · D-061).
- **W-V8-EIXO-ORDEM-MANUAL** — Ordem manual aplicada sobre eixo temporal/ordinal (desvio do default canônico). D-071.
- **W-V8-EIXO-ESTRUTURA-INFERIDA** — Estrutura POR_COLUNAS/POR_LINHAS aceita por default. Herança V3 (D-062).
- **W-V8-EIXO-PONTOS-MUITOS** — Bloco de seleção de pontos ativado (10+ valores únicos na discriminadora). Herança V3 (D-062).
- **W-V8-EIXO-SELECAO+INTERVALO** — Seleção prévia combinada com De/Até. Herança V3 (D-062 + D-064).
- **W-V8-INTERVALO-DEFAULT** — De/Até aceitos por default sem edição explícita. D-073.
- **W-V8-INTERVALO-AJUSTE-INICIO** — De declarado anterior ao primeiro ponto da base; ajustado (AJUSTE_LEVE). D-073.
- **W-V8-INTERVALO-AJUSTE-FIM** — Até declarado posterior ao último ponto da base; ajustado (AJUSTE_LEVE). D-073.
- **W-V8-MODO-INFERIDO** — Modo (transacional/pré-agregado) aceito por default sem edição. D-074.
- **W-V8-MEDIDA-TIPO-DECL** — Tipo de medida aceito por default sem edição. D-075.
- **W-V8-MEDIDA-RELATIVA** — Medida tipo relativo detectada; default de agregação alterado para média. D-075.
- **W-V8-MEDIDA-NAO-ADITIVA** — Medida tipo não-aditivo detectada; default de agregação alterado para média. D-075.
- **W-V8-MEDIDA-NULO-COM-PRESENCA** — N registros com presença + valor nulo na medida (preservado, não convertido em zero). D-075.
- **W-V8-EIXO-LACUNA** — Lacunas detectadas no eixo (só eixos com detecção ativa: temporal e ordinal com prefixo). Herança V3 (D-065), mesma detecção. D-076.
- **W-V8-MATRIZ-ORDEM-CUSTOM** — Ordem da matriz editada pelo usuário (desvio do default "Constante → Contínuo → Retornou → Novo → Ausente"). D-077.
- **W-V8-MATRIZ-PAGINACAO** — Paginação ativa (> 100 entidades por grupo; threshold configurável). D-077.
- **W-V8-LEITURA-DEFAULT** — Faixas de leitura de ciclo de vida aceitas por default. D-078.
- **W-V8-LEITURA-CUSTOM** — Faixas de leitura de ciclo de vida editadas pelo usuário. D-078.

### Warnings da V7 🆕 (consolidados no refino DCV-V7)

Catálogo completo dos 35 warnings da V7 após refino em sessão única (19/04/2026). **6 bloqueios · 11 alertas · 18 informativos.** V7 entre V3 (27) e V8 (37) — consistente com complexidade média-alta da primeira visão de família nova.

**Bloqueios (6):**

- **W-V7-MODO-VIOLACAO** — Modo Pré-agregado declarado mas duplicatas de (Grupo, Elemento) detectadas. Motor não prossegue sem confirmação de regra de agregação. D-082.
- **W-V7-MEDIDA-ESTADO** — Tipo Estado/Situação detectado/declarado na medida; redirecionamento para V6 (herança V3/V4/V8). D-083.
- **W-V7-GRUPOS-INVIAVEL** — Cardinalidade do campo Grupo excede 1.000 valores únicos. D-089.
- **W-V7-ELEMENTOS-INSUFICIENTES** — Todos os grupos com < 2 elementos válidos (sem comparação relativa possível em nenhum grupo). D-089.
- **W-V7-VOLUME-INVIAVEL** — Total de elementos > 1.000.000 (limite físico Excel ~1.048.576 linhas). D-089.

**Bloqueios estruturais adicionais sem código W-V7-*** (numerados em dcv_v7.md §8.1): arquivo ilegível · estrutura inválida · ausência de Grupo/Elemento/Medida · medida 100% nulos · tolerância inválida. Total de bloqueios incluindo estruturais: **12** (alinhado com V4).

**Alertas fortes (8):**

- **W-V7-NEG-MEDIDA** — Presença de valores negativos na medida. Sinal preservado no cálculo; grupos com média negativa geram classificação Não aplicável. D-083.
- **W-V7-GRUPO-MEDIA-NEG** — Grupo com média do grupo negativa. Classificação Não aplicável para o grupo inteiro (desvio percentual contraintuitivo quando sinal inverte). D-083 · D-085.
- **W-V7-GRUPO-MEDIA-ZERO-HOMO** — Grupo com média=0 e todos elementos=0. Classificação Não aplicável. D-085.
- **W-V7-GRUPO-MEDIA-ZERO-HETERO** — Grupo com média=0 heterogênea (positivos cancelam negativos, ou zeros "arrastam"). Classificação Não aplicável. D-085.
- **W-V7-RELATIVA-MEDIA-ARIT** — Média aritmética aceita em tipo Relativa sem ponderação. Alerta explícito sobre distorção potencial. D-083.
- **W-V7-NULO-MEDIDA** — Elemento com consolidação nula (todas as linhas da combinação Elemento+Grupo tinham nulo na medida). Classificação NULO_MEDIDA. Herança V4 D-038. D-085.
- **W-V7-GRUPOS-CRITICO** — Cardinalidade do campo Grupo 201-1.000 valores únicos. Confirmação obrigatória + sugestão de campo alternativo. D-089.
- **W-V7-VOLUME-ALERTA** — Total de elementos 200.001-500.000 (performance pode degradar). D-089.
- **W-V7-VOLUME-CRITICO** — Total de elementos 500.001-1.000.000 (Excel pode não abrir). D-089.

**Alertas regulares (3):**

- **W-V7-GRUPO-UNITARIO** — Grupo com 1 único elemento. Classificação Na Média por definição (desvio=0) + flag "baixa utilidade comparativa". D-085.
- **W-V7-GRUPOS-MUITOS-ALERTA** — Cardinalidade do campo Grupo 51-200 (benchmarking granular dilui leitura). D-089.
- **W-V7-GRUPO-CRITICO** — Grupo com 10.000+ elementos (grupo muito grande). D-089.

**Informativos (18):**

- **W-V7-MODO-TRANS-DEFAULT** — Modo Transacional aceito sem edição. D-082.
- **W-V7-MODO-TRANS-CUSTOM** — Usuário editou para Transacional. D-082.
- **W-V7-MODO-PREAGG-DEFAULT** — Modo Pré-agregado aceito sem edição. D-082.
- **W-V7-MODO-PREAGG-CUSTOM** — Usuário editou para Pré-agregado. D-082.
- **W-V7-TIPO-DEFAULT** — Tipo da medida aceito como sugerido pelo motor. D-083.
- **W-V7-TIPO-CUSTOM** — Tipo da medida editado pelo usuário. D-083.
- **W-V7-RELATIVA-MEDIA-POND** — Média ponderada declarada em Relativa com campo de peso. D-083.
- **W-V7-TOLERANCIA-DEFAULT** — Tolerância ±5% aceita sem edição. D-084.
- **W-V7-TOLERANCIA-CUSTOM** — Tolerância editada para valor distinto. D-084.
- **W-V7-SEMA-DEFAULT** — Semântica Neutro aceita sem edição. D-087.
- **W-V7-SEMA-CUSTOM** — Semântica editada para Maior/Menor-é-melhor. D-087.
- **W-V7-GRUPO-HOMOGENEO** — Grupo com todos os valores iguais à média. Homogeneidade perfeita; todos Na Média. D-085.
- **W-V7-RANK-EMPATE** — Empates resolvidos pela regra de desempate em 4 níveis. Herança V4 D-041. D-088.
- **W-V7-LEITURA-DEFAULT** — Thresholds do Bloco 5 aceitos como default (70%/60%/75%/25%). D-086.
- **W-V7-LEITURA-CUSTOM** — Thresholds do Bloco 5 editados pelo usuário. D-086.
- **W-V7-GRUPOS-MUITOS-AVISO** — Cardinalidade do Grupo 21-50 (muitos grupos · benchmarking granular). D-089.
- **W-V7-GRUPO-VOLUMOSO** — Grupo com 500+ elementos (média pode ser achatada). D-089.
- **W-V7-VOLUME-AVISO** — Total de elementos 50.001-200.000. D-089.

### Warnings da V9 🆕 (consolidados no refino DCV-V9)

Catálogo completo dos 40 warnings da V9 após refino em sessão única (19/04/2026). **12 bloqueios · 11 alertas · 17 informativos.** V9 na faixa alta do projeto (V8=37 · V7=35) — coerente com natureza multidimensional e casos-limite articulados em 2 camadas de cobertura de nulos.

**Bloqueios (12):**

- **W-V9-ARQUIVO-INVALIDO** — Arquivo ilegível ou corrompido. dcv_v9.md §7 #1.
- **W-V9-ESTRUTURA-INVALIDA** — Estrutura inválida (arquivo vazio, aba sem dado, sem coluna numérica para métricas). §7 #2.
- **W-V9-SEM-IDENTIFICADOR** — Nenhum campo categórico elegível como Identificador. §7 #3.
- **W-V9-METRICAS-INSUFICIENTES** — Menos de 2 métricas numéricas elegíveis (ranking monomensional não é V9). D-093 · §7 #4.
- **W-V9-DIRECAO-FALTANDO** — Pelo menos 1 métrica sem Direção declarada ao entrar em E4. Bloqueia avanço. D-093 · §7 #5.
- **W-V9-METRICA-TOTAL-NULA** — Pelo menos 1 métrica com 100% valores nulos. Bloqueia em E3 até usuário remover a métrica ou cancelar execução. D-095 · §7 #6.
- **W-V9-SEG-SEM-AGRUPADOR** — Modo de Ranking = Segmentado declarado sem Agrupador ativo. D-092 · §7 #7.
- **W-V9-MODO-VIOLACAO** — Modo Pré-agregado declarado mas duplicatas da unidade analítica detectadas no volume completo. D-092 · §7 #8.
- **W-V9-ELEMENTOS-INSUFICIENTES** — Menos de 2 Identificadores válidos no conjunto analisado (após consolidação). No modo Segmentado: bloqueio quando qualquer agrupador tem < 2 elementos. D-098 · §7 #9.
- **W-V9-THRESHOLDS-INVALIDOS** — Thresholds `lider_pct + retaguarda_pct > 90%` do conjunto (viola constraint operacional que garante pelo menos 10% para Equilibrado/Especialista). Bloqueia em E3. D-098 · §7 #10.
- **W-V9-METRICAS-INVIAVEL** — Mais de 10 métricas ativas (limite operacional de tela legível e score discriminante). D-093 · §7 #11.
- **W-V9-VOLUME-INVIAVEL** — Total de Identificadores > 1.000.000 (limite físico Excel). D-100 · §7 #12.

**Alertas fortes (8):**

- **W-V9-ELEMENTO-NULO** — Elemento com 0 métricas válidas (nulo em todas as N). Classificação NULO_MEDIDA; não entra no ranking. D-095.
- **W-V9-METRICA-ZERADA** — Métrica com 100% valores zerados. Não discrimina (todos elementos recebem Pos 1 naquela métrica); execução prossegue. D-095.
- **W-V9-CONJUNTO-PEQUENO** — Conjunto com 2-4 Identificadores válidos. Classificação aplicada com leitura limitada; arredondamento `ceil` nos thresholds. D-097 · D-098.
- **W-V9-IDENTIFICADORES-CRITICO** — N Identificadores 10.001-100.000 · confirmação obrigatória. D-100.
- **W-V9-IDENTIFICADORES-EXTREMO** — N Identificadores 100.001-1.000.000 · performance degradada. D-100.
- **W-V9-AGRUPADOR-CRITICO** — Cardinalidade do Agrupador ≥ 501 valores únicos no modo Segmentado. Cada grupo com poucos Identificadores · leitura degradada. D-100.
- **W-V9-METRICAS-EXCESSO-AVISO** — 7-10 métricas ativas · confirmação recomendada. D-093.
- **W-V9-MODELO-METRICA-AUSENTE** — Ao aplicar T-MODELO em nova base, métrica configurada não encontrada no arquivo; solicita seleção manual. D-093.

**Alertas regulares (3):**

- **W-V9-METRICA-PARCIAL** — Elemento com K < N métricas válidas. Score parcial calculado sobre K válidas; elemento com K=1 não elegível a Especialista. D-095.
- **W-V9-METRICAS-MIN** — Exatamente 2 métricas ativas (mínimo estrutural). Variação Máxima de Posição com interpretação reduzida. D-093.
- **W-V9-IDENTIFICADORES-MUITOS-ALERTA** — N Identificadores 501-10.000 · confirmação recomendada. D-100.
- **W-V9-AGRUPADOR-MUITOS-ALERTA** — Cardinalidade do Agrupador 101-500 no modo Segmentado. Sugere revisar escopo de segmentação. D-100.

**Informativos (17):**

- **W-V9-MODO-TRANS-DEFAULT** — Modo Transacional aceito sem edição. D-092.
- **W-V9-MODO-TRANS-CUSTOM** — Usuário editou para Transacional. D-092.
- **W-V9-MODO-PREAGG-DEFAULT** — Modo Pré-agregado aceito sem edição. D-092.
- **W-V9-MODO-PREAGG-CUSTOM** — Usuário editou para Pré-agregado. D-092.
- **W-V9-RANKING-GLOBAL** — Modo de Ranking = Global declarado. D-092.
- **W-V9-RANKING-SEGMENTADO** — Modo de Ranking = Segmentado declarado com Agrupador ativo. D-092.
- **W-V9-DIRECAO-DECLARADA** — Configuração de Direção por métrica registrada. D-093.
- **W-V9-NOME-DEFAULT** — Nome analítico aceito da coluna original em todas as métricas. D-093.
- **W-V9-NOME-CUSTOM** — Pelo menos 1 nome analítico editado pelo usuário. D-093.
- **W-V9-AGREG-DEFAULT** — Regras de agregação aceitas como default em todas as métricas. D-092.
- **W-V9-AGREG-CUSTOM** — Pelo menos 1 regra de agregação editada pelo usuário. D-092.
- **W-V9-ESCALAS-HETEROGENEAS** — Razão de amplitude entre métricas > 1.000× detectada. Score consolidado preservado (posições ordinais neutralizam escalas); lembrete explícito no Diagnóstico. D-094.
- **W-V9-RANK-EMPATE** — Empates no Passo 3 (Posição por Métrica) ou no score consolidado resolvidos por regra de desempate V9 em 4 níveis. D-096.
- **W-V9-THRESHOLD-LIDER-DEFAULT** · **W-V9-THRESHOLD-LIDER-CUSTOM** — Threshold 20% top aceito/editado. D-098.
- **W-V9-THRESHOLD-RETAGUARDA-DEFAULT** · **W-V9-THRESHOLD-RETAGUARDA-CUSTOM** — Threshold 20% bottom aceito/editado. D-098.
- **W-V9-THRESHOLD-ESPECIALISTA-DEFAULT** · **W-V9-THRESHOLD-ESPECIALISTA-CUSTOM** — Threshold 50% Especialista aceito/editado. D-097 · D-098.
- **W-V9-LEITURA-DEFAULT** · **W-V9-LEITURA-CUSTOM** — Thresholds de leitura qualitativa do conjunto aceitos/editados. D-098.
- **W-V9-CLASSE-EXPANDIDA-POR-EMPATE** — Classe primária expandida além do threshold declarado por empate de score no ponto de corte percentual. D-098.
- **W-V9-CONJUNTO-HOMOGENEO** — Conjunto com todos os Identificadores empatados em todas as métricas. Todos Equilibrados; classificação por score também pode empatar. D-097.
- **W-V9-IDENTIFICADORES-MUITOS-AVISO** — N Identificadores 51-500 · aviso informativo. D-100.
- **W-V9-AGRUPADOR-MUITOS-AVISO** — Cardinalidade do Agrupador 21-100 no modo Segmentado. D-100.
- **W-V9-SCORE-CALCULADO** — Informativo de execução normal; score calculado para todos os Identificadores elegíveis. D-095.

### Warnings da V5 🆕 (consolidados no refino DCV-V5 · ~37 catalogados)

**Bloqueios (12 estruturais · §7 do DCV):**

- **B-V5-CAMPO-PRINCIPAL-NAO-NUMERICO** — Campo principal não é numérico (texto · data · binário puro).
- **B-V5-CAMPO-BOOLEANO** — Campo principal é booleano (0/1 disfarçado de numérico). Espelha V7 D-083 (booleano não cabe na natureza analítica). D-103.
- **B-V5-CAMPO-ID** (escapável) — Campo principal detectado como ID via heurística (cardinalidade ≥ 90% + sequência ou comprimento fixo). Escape "este campo é numérico de fato" disponível com warning permanente W-V5-ID-FORCADO. D-103.
- **B-V5-MINIMO-OPERACIONAL** — N válido < 5 (após exclusão de nulos).
- **B-V5-AGRUP-EXCESSO** — Agrupador com > 500 valores únicos.
- **B-V5-CAMPO-PRINCIPAL-COMO-AGRUP** — Campo principal selecionado também como agrupador.
- **B-V5-AGRUPADOR-NULO-EXCESSIVO** — Agrupador com > 30% de valores nulos (segmentação degenerada). D-073 herdado V4 D-038.
- **B-V5-DISTRIBUICAO-DEGENERADA** — Distribuição inteiramente degenerada (todos valores idênticos · DP = 0 · IQR = 0).
- **B-V5-NULOS-EXCESSIVOS-CRITICO** — > 80% dos registros com valor nulo no campo principal (impossibilidade analítica).
- **B-V5-AGRUPADOR-NUMERICO** — Agrupador é campo numérico contínuo (semântica errada).
- **B-V5-MULTIPLOS-CRITERIOS-SIMULTANEOS** — Tentativa de aplicar 2+ critérios de outlier simultaneamente em uma execução. D-104.
- **B-V5-MOTOR-INFERIU-TIPO-INCOMPATIVEL** — Motor inferiu tipo Booleano ou ID com confiança alta · usuário não confirmou escape.

**Alertas (10):**

- **W-V5-N-PEQUENO** — N válido entre 5 e 29 · alerta forte de limitação estatística.
- **W-V5-NULOS-EXCESSIVOS** — ≥ 30% dos registros têm valor nulo no campo principal.
- **W-V5-AGRUP-CARDINALIDADE-MEDIA** — Agrupador com 51-200 valores únicos.
- **W-V5-AGRUP-CARDINALIDADE-ALTA** — Agrupador com 201-500 valores únicos.
- **W-V5-SEGMENTO-INSUFICIENTE** — Segmento individual com < 5 observações · não calculado · cálculo prossegue nos demais segmentos.
- **W-V5-SEGMENTO-PEQUENO** — Segmento com 5-29 observações · alerta forte de limitação estatística no segmento.
- **W-V5-MULTIMODAL-EXCESSIVA** — ≥ 6 modas detectadas · contagem retornada · provavelmente sem moda dominante.
- **W-V5-VOLUME-MEDIO** — N válido entre 10.000 e 99.999 · alerta de performance.
- **W-V5-VOLUME-ALTO** — N válido ≥ 100.000 · alerta forte de performance.
- **W-V5-DIVERSIDADE-BAIXA** — Cardinalidade do campo principal < 10% de N válido · interpretação cuidadosa de IQR/quartis (poucos valores únicos · quartis podem coincidir).

**Informativos (15):**

- **W-V5-RELATIVO** — Campo principal é tipo Relativo · interpretação de dispersão é dos valores como observados (não dispersão ponderada por volume). D-103.
- **W-V5-NAO-ADITIVO** — Campo principal é tipo Não aditivo (subtipo estoque ou contagem) · interpretação de dispersão tem natureza específica. D-103.
- **W-V5-ID-FORCADO** (permanente quando ativado) — Usuário forçou cálculo em campo detectado como ID via escape "este campo é numérico de fato". D-103.
- **W-V5-NULOS-EXCLUIDOS** — ≥ 1 nulo no campo principal foi excluído do cálculo · contagem agregada em diagnóstico.
- **W-V5-CONCENTRACAO-EXTREMA** — ≥ 90% das observações estão no mesmo valor único · IQR/DP perdem sentido prático.
- **W-V5-ZEROS-COMO-NULOS** (permanente quando ativada a opção) — Usuário ativou "Tratar zeros como valores ausentes".
- **W-V5-THRESHOLD-NAO-DEFAULT** — Usuário editou threshold do critério de outlier para valor diferente do default. D-104.
- **W-V5-MULTIMODAL** — 2-5 modas detectadas · distribuição multimodal. D-105.
- **W-V5-SEM-MODA-DEFINIDA** — Caso degenerado · todos os valores observados ocorrem com mesma frequência · moda não tem interpretação útil.
- **W-V5-DP-POPULACIONAL** (permanente quando ativada) — Usuário ativou cálculo de DP populacional (n) em vez de amostral (n-1).
- **W-V5-VALOR-NAO-NUMERICO** — ≥ 1 registro com valor não-numérico que passou da pré-validação · classificado como VALOR_NAO_NUMERICO na Base Analítica. D-105.
- **W-V5-DIVERSIDADE-ALTA** — Cardinalidade do campo principal > 90% de N válido · raros valores repetidos · pode acionar W-V5-SEM-MODA-DEFINIDA.
- **W-V5-CHAVE-NAO-UNICA** — Em granularidade Consolidada por chave · chave declarada tem duplicatas detectadas (warning estrutural). D-102.
- **W-V5-GRANULARIDADE-SUSPEITA** — Motor detectou possível incompatibilidade entre granularidade declarada e estrutura observada (ex: usuário declarou Individual mas existe coluna ID claramente identificadora). D-102.
- **W-V5-CONFIG-AVANCADA-USADA** — Usuário acessou Configurações avançadas em algum momento da configuração (registro de auditoria · não-bloqueante).

### Warnings da V6 🆕 (consolidados no refino DCV-V6 · 43 catalogados · maior volume do projeto)

**Bloqueios (13 estruturais · §7 do DCV · D-120):**

- **B-V6-EIXO-NUMERICO-CONTINUO** (escapável) — Eixo declarado sobre campo classificado como NUMERICO_CONTINUO pelo motor_base. Escape "este campo é categórico de fato" disponível com warning permanente W-V6-EIXO-FORCADO-CATEGORICO. D-113.
- **B-V6-EIXO-VAZIO-OU-AMBIGUO** — Eixo sobre coluna com >90% nulos ou tipo inconferível. Sem escape (estrutural). D-113.
- **B-V6-EIXO-CARDINALIDADE-EXCESSO** (escapável) — Cardinalidade individual do eixo > 200 valores únicos. Escape "sei o que estou fazendo" com warning permanente W-V6-EIXO-CARDINALIDADE-FORCADA. D-113.
- **B-V6-EIXOS-IGUAIS** — Eixo1 = Eixo2 (mesmo campo nos dois eixos). Sem escape (invariante matemático · matriz de campo contra si mesmo é diagonal trivial).
- **B-V6-MEDIDA-ID** (escapável) — Campo com subtipo ID (CPF · CNPJ · número de pedido detectado via heurística D-103) usado como Medida com regra Soma ou Média. Escape "este campo é numérico de fato" com warning permanente W-V6-ID-FORCADO. Herança V5 D-103. D-112.
- **B-V6-BOOLEANO-COM-SOMA-OU-MEDIA** — Campo Booleano usado como Medida com regra diferente de Contagem. Sem escape (Booleano só aceita Contagem). D-112.
- **B-V6-ESTADO-COMO-MEDIDA** — Campo categórico/estado/situação usado como Medida. Sem escape · microcopy redirecional "Use este campo como Eixo · para contar ocorrências por combinação, use Medida = Contagem". D-112.
- **B-V6-POR-LINHAS** — Base em formato POR_LINHAS. Sem escape no MVP · redireciona para M2.PIVOT futuro · roadmap P-V6-01-POR-LINHAS-Evo. T-07.
- **B-V6-MATRIZ-CARDINALIDADE-EXTREMA** (escapável) — Produto N × M da matriz > 10.000 células (mesmo após escapes individuais nos eixos). Escape "sei o que estou fazendo" com warning permanente W-V6-MATRIZ-FORCADA. D-120.
- **B-V6-MATRIZ-VAZIA** — Todas as células ausentes após filtro de nulos (caso-limite improvável · salvaguarda estrutural). Sem escape. D-120.
- **B-V6-MEDIDA-NUMERICA-AUSENTE** — Medida = Soma ou Média declarada mas nenhum campo numérico válido na base. Sem escape · microcopy redirecional para Contagem. D-112.
- **B-V6-MOTOR-INFERIU-TIPO-INCOMPATIVEL** — Motor_base inferiu tipo estrutural incompatível com escolha do usuário · discordância não foi escapada. Sem escape · força revisão.
- **B-V6-MINIMO-OPERACIONAL** — Base com < 5 registros válidos após exclusão de nulos nos eixos. Sem escape. Espelho V5.

**Warnings estruturais (8 · exigem confirmação do usuário ou registram decisão não-default relevante):**

- **W-V6-CHAVE-NAO-UNICA** — Pré-agregado declarado mas par (Eixo1, Eixo2) tem duplicidade detectada (estrutural). D-111.
- **W-V6-SOMA-SOBRE-RELATIVA** — Medida = Soma sobre campo classificado como Relativo. Cálculo matematicamente possível mas interpretação analítica questionável. D-112.
- **W-V6-EIXO-CARDINALIDADE-P2** — Cardinalidade individual do eixo entre 31-100 valores únicos · alerta leve · "matriz ficará grande". D-113.
- **W-V6-EIXO-CARDINALIDADE-P3** — Cardinalidade individual do eixo entre 101-200 valores únicos · alerta forte · exige confirmação do usuário · microcopy "matriz ficará muito grande · considere agrupar valores". D-113.
- **W-V6-CELULA-PRESENTE-SEM-VALOR** — ≥ 1 célula presente com Valor da Medida null (raro em Pré-agregado). Célula classificada como `PRESENTE_SEM_VALOR` (especial paralela). Não entra em ranking. D-115.
- **W-V6-MATRIZ-P2** — Cardinalidade da matriz (N × M) entre 901-2.500 · paginação do coração visual ativada automaticamente. D-120.
- **W-V6-MATRIZ-P3** — Cardinalidade da matriz entre 2.501-10.000 · exige confirmação do usuário · streaming ativado na exportação Excel. D-120.
- **W-V6-FAIXAS-EDITADAS** — Usuário alterou o padrão de Faixas de Participação (default 5 faixas 0/20/40/60/80/100). D-116.

**Warnings permanentes (5 · escapes de bloqueios · marcam decisão consciente):**

- **W-V6-EIXO-FORCADO-CATEGORICO** (permanente) — Usuário forçou uso de campo NUMERICO_CONTINUO como Eixo via escape. D-113.
- **W-V6-EIXO-CARDINALIDADE-FORCADA** (permanente) — Usuário forçou eixo com > 200 valores únicos via escape. D-113.
- **W-V6-ID-FORCADO** (permanente) — Usuário forçou uso de campo detectado como subtipo ID como Medida via escape "este campo é numérico de fato". Herança V5 D-103. D-112.
- **W-V6-MATRIZ-FORCADA** (permanente) — Usuário forçou execução com matriz > 10.000 células via escape. D-120.
- **W-V6-EIXO-ORDEM-MANUAL** (permanente) — Usuário reordenou manualmente eixo temporal ou ordinal via drag-and-drop. Espelho V8 D-074. D-115.

**Informativos (17):**

- **W-V6-MODO-INFERIDO** — Usuário aceitou default declarado do motor para Modo da Base (Transacional × Pré-agregado). D-111.
- **W-V6-MEDIDA-RELATIVA** — Campo classificado como Relativo sendo usado como Medida · interpretação da participação tem natureza específica. D-112.
- **W-V6-MEDIDA-NAO-ADITIVA** — Campo classificado como Não-aditivo (subtipo estoque/contagem) sendo usado como Medida · interpretação cuidadosa. D-112.
- **W-V6-MEDIDA-TIPO-DECL** — Usuário aceitou default declarado do motor para Tipo do Campo da Medida. D-112.
- **W-V6-MEDIDA-REGRA-DECL** — Usuário aceitou default declarado do motor para Regra de Agregação da Medida. D-112.
- **W-V6-EIXO-TEMPORAL** — Eixo declarado sobre campo classificado como TEMPORAL · aceito com microcopy redirecional "Para análise de evolução temporal, considere V3 ou V8". D-113.
- **W-V6-MULTIABA-ESCOLHA** — Registro da aba escolhida em arquivo multi-aba. T-07.
- **W-V6-ESTRUTURA-INFERIDA** — Usuário aceitou default declarado do motor_base para estrutura POR_COLUNAS vs POR_LINHAS. T-07.
- **W-V6-EIXO-NULO-EXCLUIDO** — ≥ 1 linha com nulo em Eixo1 ou Eixo2 foi excluída antes do cálculo do produto cartesiano observado · contagem agregada em diagnóstico. D-114.
- **W-V6-EIXO-ORDEM-CRONOLOGICA** — Eixo detectado como TEMPORAL · ordem default ajustada para cronológica crescente (herança do reconhecedor pt-BR/pt-EN de D-026). D-115.
- **W-V6-RANKING-EMPATE-GERAL** — > 50% das células estão empatadas no Valor da Medida · ranking segue níveis 2-4 de desempate (alfabético + inserção). D-115.
- **W-V6-FRONTEIRA-CLASSIFICACAO** — Empate exato na fronteira entre classes (ex: duas células com 80% acumulado exato sendo uma Dominante e outra Relevante) · ordenação estável do ranking desempata. D-115.
- **W-V6-LIMIAR-DOMINANTE-EDITADO** — Usuário editou o Limiar Dominante para valor diferente do default 20%. D-116.
- **W-V6-LIMIAR-RESIDUAL-EDITADO** — Usuário editou o Limiar Residual para valor diferente do default 2%. D-116.
- **W-V6-THRESHOLD-LEITURA-EDITADO** — Usuário editou threshold de leitura qualitativa da matriz (Concentrada · Dispersa · Esparsa · Assimétrica · Com lacunas). D-117.
- **W-V6-TOPN-EDITADO** — Usuário editou Top-N do Bloco 4 do Resumo Executivo (default 10). D-117.
- **W-V6-VALOR-NAO-NUMERICO** — ≥ 1 linha com valor não-numérico no campo Medida que passou da pré-validação · excluída do cálculo com contagem agregada em diagnóstico. Espelho V5.

### Warnings de motor

- **W-B01** — Inferência semântica detectou coluna boolean disfarçada de float64 (valores em {0,1,NaN} tratados como boolean, não numeric — D-008). Requisito herdado pela Fundação v2.

### Warnings de motor_upload (Fundação · G-FUND parte 1 · D-135 ratificada)

- **W-U-ENCODING-FALLBACK** — Arquivo CSV lido com fallback latin-1 após falha utf-8 · INFORMATIVO
- **W-U-SEP-FALLBACK** — Separador CSV inferido como `;` após falha do default `,` · INFORMATIVO
- **W-U-ARQUIVO-VAZIO** — Arquivo sem dados após parse · ALERTA_ESTRUTURAL

### Warnings de motor_base (estendidos · G-FUND parte 1)

- **W-B01** — Boolean disfarçado detectado em float64 {0, 1, NaN} · D-008 · INFORMATIVO (já existente · mantido)
- **W-B-MISTO** — Coluna com > 30% de valores em tipos técnicos divergentes · classificada VAZIO_OU_AMBIGUO · ALERTA_ESTRUTURAL
- **W-B-QUASE-VAZIO** — Coluna com > 90% de nulos · classificada VAZIO_OU_AMBIGUO · ALERTA_ESTRUTURAL_LEVE
- **W-B-TEMPORAL-PARCIAL** — Padrão cronológico reconhecido em 50-79% (abaixo do threshold 80%) · INFORMATIVO
- **W-B-ID-DETECTADO** — Subtipo ID detectado · D-103 · INFORMATIVO (consumido por V5 · V6 · V11)

### Warnings de transversais fundamentais (T-AGRUPA · T-DIAG · T-SEMA)

- **W-T-AGRUPA-DUPLICATA-PRE-AGREGADO** — Modo Pré-agregado declarado mas chaves têm duplicatas detectadas no no-op validado · ALERTA_ESTRUTURAL
- **W-T-AGRUPA-REGRA-POR-METRICA** — Contrato Dict (regra por métrica) usado · lista regras efetivas · INFORMATIVO (extensão V9 D-096)
- **W-T-SEMA-METRICA-SEM-SEMANTICA** — Métrica em contrato 2 sem semântica declarada · default NEUTRA aplicado · INFORMATIVO

---

## 7. Decisões e infraestrutura

### `D-XXX` 📌

Numeração sequencial **global** de decisões registradas em `DECISIONS.md`. Não reinicia por visão, não reaproveita números (mesmo se uma decisão for revogada). Decisões registradas até agora: **D-001 a D-032**. A mais recente é **D-032** (Bloqueios operacionais e diretrizes de performance da V2). A fundacional do método v2 é **D-014** (Reforma pós-DCVs). Reversões justificadas pelo Princípio C.5: D-001 → D-022, D-002 → D-024, D-004 → D-023.

### `UploadResult` 🔧

Contrato Pydantic — saída padrão do `motor_upload`. Na v1 (em `/legacy/`), campos: `file_name`, `preview` (5 linhas), `arquivo_bytes` (D-007), `aba_selecionada`, `abas_disponiveis`. **Será reformulado no G-FUND** com base nos requisitos dos 10 DCVs.

### `MotorResult` 🔧

Contrato Pydantic — saída padrão do `motor_base`. Na v1, campos: DataFrame completo, `column_meta`, `warnings`. **Será reformulado no G-FUND**.

### `VNResult` 🔧

Contrato Pydantic genérico — saída padrão de cada `visao_vN`. Definido no G-FUND para manter padrão consistente entre as 10 visões.

### `BloqueioOperacional` 🆕📌 (D-134)

Contrato Pydantic único compartilhado por todas as 11 visões. Materialização arquitetural do padrão MBO (C.D4 · D-127). Campos: `codigo` (padrão B-VN-DESCRITOR) · `condicao_disparo` (microcopy) · `escapavel` · `escape_acionado` · `warning_pos_escape` · `contexto_disparo` (Dict flexível para campos V-específicos).

Specs S-VN declaram matriz de bloqueios V-específica como lista de dicionários. Motor instancia na ordem declarada. exportacao.py consome sem conhecer visão-origem · aba Diagnóstico consolida bloqueios de qualquer visão sem código específico. Reduz custo de contexto para IA receptiva (D-130).

Formalizado em **D-134**.

### `CASOS_ESPERADOS` 📌

Aba especial dentro de cada base sintética (`base_vN.xlsx`) documentando o **gabarito auditado**: para cada caso, o resultado esperado da visão. Permite validação automatizada e alimenta a Validação Visual da Usuária.

### `Pendência P-NN`

Numeração local dentro de uma spec ou DCV. Quando uma pendência é fechada por uma decisão global D-XXX, a entrada D-XXX cita a P-NN original (ex: "fecha P-01 do DCV-V2"). Pendências abertas do método novo ficam listadas na aba 5 da planilha com prefixo temático (P-G1 para pendências globais, P-V2-NN para pendências específicas da V2, etc.).

---

## 8. Papéis

### `Usuária` — Elaine Melo 📌

Produto, estratégia, aprovação final. Operação solo. Única pessoa que **aprova** DCVs, specs, wireframes, bases e Validação Visual.

### `Arquiteto` — Claude no Projects 📌

Produção de artefatos técnicos, manutenção de coerência documental, proposição de decisões com trade-offs, condução metodológica. Opera sempre no painel de Projects com os documentos fixos carregados.

### `Claude Code`

Execução de blocos de implementação em sessão dedicada, a partir de prompts produzidos pelo Arquiteto. Não tem acesso ao contexto do Arquiteto — depende inteiramente do prompt recebido.

### `ChatGPT`

Analista técnico de apoio para rascunhos iniciais de DCV prévio. Opera sob diretriz da Usuária. **Não gera artefato técnico canônico** — isso é função do Arquiteto, que refina o prévio produzido.

### `Gamma`

Ferramenta de **formatação de documentos apresentáveis finais** (Blueprint polido, material externo). **Não gera artefato técnico do projeto.** Restrição formalizada em D-006 e ampliada em D-014. Princípio A.3.

---

## 9. Fontes de verdade (hierarquia)

| Fonte | Papel |
|---|---|
| **Blueprint (Gamma)** | Fonte estratégica do produto — só consulta, não geração |
| **CONTEXT.md** | Método, regras permanentes, arquitetura |
| **DECISIONS.md** | Log cronológico de decisões + porquê |
| **TabloFlow_Estado_do_Projeto.xlsx** | Estado vivo (status, fila, pendências) |
| **DCVs em `/specs/dcv/`** | Compreensão validada de cada visão |
| **Specs em `/specs/`** | Contratos + regras + wireframe funcional por visão |
| **GLOSSARIO.md** | Este arquivo — definições de termo e nomenclatura |

**Regras de conflito:**

- Se CONTEXT e planilha divergirem sobre regra permanente → CONTEXT prevalece
- Se CONTEXT e planilha divergirem sobre estado atual → planilha prevalece
- Se Blueprint e spec local divergirem, spec prevalece para execução; Blueprint prevalece para intenção
- Se DCV e spec divergirem → DCV prevalece (DCV é o requisito; spec é a implementação)
- Se spec e código divergirem → investigar antes de assumir prevalência

---

## 10. Convenções de comunicação

### "Fecha o bloco" / "Kit de encerramento" 📌

Comando da Usuária para acionar o ritual de encerramento de conversa. O Arquiteto entrega os 8 itens do kit — ver Instruções do Projeto §Ritual de encerramento.

### "Valide o estado" 📌

Comando da Usuária no início de uma conversa nova. Aciona o **Ritual de Abertura**: Arquiteto lê os documentos fixos, valida coerência, confirma próximo passo operacional.

### "DCV prévio X pronto" / "DCV-VN para refinar"

Usuária sinaliza que o DCV prévio da visão N está pronto e encaminha ao Arquiteto para refino. A conversa seguinte é dedicada a esse refino (bloco DCV-VN).

### `Padrão de condução DCV` 🆕📌

Padrão operacional do Arquiteto em sessões de refino de DCV (blocos `DCV-VN` e `DCV-OPN`), formalizado em **D-019**. 10 elementos: validação de estado na abertura, fila racionalizada de pendências, uma pendência por vez com opções explícitas e trade-offs, Princípio C.5 como primeira lente, confirmação explícita antes de avançar, mini status-check a cada 3 pendências, abertura para correção de enquadramento (sem defensividade), identificação proativa de decisões transversais, fechamento proativo com kit de encerramento, DCV final em prosa como último ato ou como entregável da próxima sessão. Ver Instruções do Projeto §Padrão de condução em sessões de DCV.

### `Kit de encerramento` (formato D-020) 🆕

A partir de D-020 (18/04/2026), o kit de encerramento entrega **arquivos canônicos atualizados como artefatos prontos para download**, não mais como instruções de edição. A Usuária baixa CONTEXT.md, DECISIONS.md, GLOSSARIO.md, Instruções do Projeto e planilha atualizados, e substitui diretamente no painel do Projects. Elimina risco cumulativo de erro de transcrição. Condição operacional: últimas versões aprovadas precisam estar no painel no início da sessão.

### `Default declarado` 🆕📌

Padrão derivado do Princípio C.5, cristalizado na Sessão 1 do DCV-V2 (D-024, D-025, D-026, D-027, D-029). Consiste em: motor propõe um default analítico, mas torna a decisão **visível na configuração antes da execução**, com opção fácil de alterar. Honra C.5 sem virar fricção UX. Default silencioso no motor (revelado só no diagnóstico pós-execução) viola C.5; default declarado em interface satisfaz C.5. Candidato a princípio formal quando aparecer em mais visões — registrado em CONTEXT §9 Camada C.

### `Vocabulário dual técnico/exibição` 🆕

Padrão de design consolidado na Sessão 1 do DCV-V2: o contrato técnico do motor usa nomes neutros e simétricos (ex: `AUSENTE_ORIGEM`, `AUSENTE_COMPARADO`), enquanto a exibição ao usuário usa linguagem de negócio (ex: "Apareceu no Comparado", "Saiu / Não está no Comparado"). Já era visível no vocabulário Origem/Comparado (técnico) vs "Comparar de"/"Comparar com" (UX). D-022 e D-023 reforçam o padrão para classificações estruturais.

### `Classificação estrutural` 🆕📌 (V2)

Categorias mutuamente exclusivas que classificam cada registro do MotorResult da V2 conforme presença e nulidade nos dois lados (D-022 + D-023):

| Contrato técnico | Exibição ao usuário | Diferença e variação |
|---|---|---|
| `PRESENTE_AMBOS` | (omitido — caso normal) | Calculadas |
| `AUSENTE_ORIGEM` | "Apareceu no Comparado" | `None` (sem dado na Origem) |
| `AUSENTE_COMPARADO` | "Saiu / Não está no Comparado" | `None` (sem dado no Comparado) |
| `NULO_ORIGEM` | "Valor nulo na Origem" | `None` (linha existe, valor em branco) |
| `NULO_COMPARADO` | "Valor nulo no Comparado" | `None` |
| `NULO_AMBOS` | "Valor nulo em ambos" | `None` |

Distinção AUSENTE_* vs NULO_*: AUSENTE significa "linha não existe nesta base" (resultado de outer join); NULO significa "linha existe, mas valor numérico está em branco". Visualmente: `None` por nulo aparece como "—" ou "(nulo)"; `None` por ausência aparece como "(não consta)".

### `Inconsistência leve vs estrutural` 🆕📌 (transversal — D-021)

Fronteira que organiza tratamento de inconsistências entre Origem e Comparado em qualquer visão com consolidação cruzada (Família A, possível herança em outras famílias).

**Leve** (4 casos taxativos — motor ajusta sem perguntar e registra como `AJUSTE_LEVE` no Diagnóstico):
1. Diferença de ordem de colunas
2. Espaços, acentos ou case diferente quando conteúdo idêntico após normalização
3. Tipos numéricos compatíveis (int/float, mesma escala)
4. Linhas em branco ou nulos isolados em coluna

**Estrutural** (tudo o mais — motor para na configuração e abre painel de resolução, registra como `DECISAO_USUARIO`): nível de agrupamento divergente, coluna ausente em uma base, tipo incompatível, valor único de coluna discriminadora divergente, ordem de magnitude radicalmente diferente.

Padrão "ajusta cedo, evidencia tarde" abolido por C.5.

### `Retroação diferida` 🆕📌

Padrão de método consolidado para tratamento de referências cruzadas entre DCVs aprovados em momentos distintos. Quando um DCV posterior estabelece relação com uma visão de DCV já aprovado, a adaptação do DCV anterior (inclusão de bloco "Relação com V[N]" ou similar) é **registrada como tarefa diferida** para a próxima revisão natural dessa visão (Spec S-V[N] ou atualização de DCV por demanda), **não é sessão dedicada imediata**.

Racional: continuar produzindo DCVs novos é mais valioso que revisitar DCV já aprovado para ajuste cosmético de enquadramento. A informação do par cruzado vive primeiro no DCV mais recente (que tem o contexto analítico completo); quando a visão anterior for revisitada, a retroação é aplicada então.

**Aplicações consolidadas:**
- **V11 → V1** — DCV-V11 aprovado em 19/04/2026; bloco "Relação com V11" em §2 do DCV-V1 fica como tarefa diferida (D-058). Execução: próxima revisão natural de V1. **Status: aberta.**
- **V3 → V8** — DCV-V3 refinado em 19/04/2026; registrada em D-060 como diferida. **Cumprida antecipadamente no DCV-V8 refinado (19/04/2026)** — §2.3 do DCV-V8 contém bloco "Relação com V3" simétrico ao §2.3 do DCV-V3. DCV-V3 aprovado pode ter §2.3 atualizado no próximo toque natural (retirar "a confirmar em DCV-V8" — ajuste cosmético). **Status: cumprida.**
- **V7 → V9** — DCV-V7 refinado em 19/04/2026; tabela comparativa V7×V9 no §2.3 continha 3 células marcadas *(a confirmar em DCV-V9)* (unidade analítica · classificação · tratamento de T-AGRUPA). Registrada em D-081 como diferida com cumprimento esperado em sequência direta. **Cumprida no DCV-V9 refinado (19/04/2026)** — §2.3 do DCV-V9 contém bloco "Relação com V7" simétrico ao §2.3 do DCV-V7; 3 células preenchidas: (a) unidade analítica V9 = Identificador (Global) · Identificador + Agrupadores (Segmentado); (b) classificação V9 = Líder · Especialista · Equilibrado · Retaguarda; (c) T-AGRUPA em V9 = consumida com 5 regras por métrica. D-081 mantida como contexto histórico (decisão de diferir em vez de antecipar permanece válida); cumprimento via D-091. **Status: cumprida.**

Padrão aplicável a futuros pares autônomos da mesma família (outras famílias que venham a ter pares autônomos).

### `Herança adaptada à natureza analítica` 🆕📌

Padrão de método consolidado no refino DCV-V8 (D-073). Visões da mesma família conceitual **não herdam padrões cegamente** de uma visão para outra; herdam o que cabe à natureza analítica específica de cada uma. Quando uma decisão estrutural tomada na primeira visão de uma família não se encaixa na lógica da segunda visão, a divergência é **justificada e registrada explicitamente**.

**Exemplo canônico (V3 × V8):** V3 bloqueia intervalo efetivo em < 3 pontos (precisa de 3+ pontos para leitura de tendência entre pares consecutivos); V8 bloqueia em < 2 (classificação de presença no ponto é estruturalmente válida a partir de 2 pontos, mesmo que leitura de ciclo de vida fique limitada). Esta divergência **não é inconsistência de método** — é aplicação honesta de C.5 a cada natureza analítica. A decisão D-073 formaliza o padrão para uso em futuras heranças entre visões da mesma família.

**10 aplicações documentadas até o refino DCV-V9 (19/04/2026):**

1. V3 × V8 · intervalo mínimo (< 3 vs < 2) — D-073
2. V7 · taxonomia 3 classes vs V8 4 classes — D-086
3. V7 · T-RANK com 4 níveis adaptados (vs default D-041 de 3) — D-088
4. V9 · não-normalização de escalas (vs V7 desvio percentual) — D-094
5. V9 · score parcial com K < N (vs NULO_MEDIDA binário V7) — D-095
6. V9 · T-RANK desempate V9-específico (vs V7-específico) — D-096
7. V9 · T-SEMA por métrica com efeito no cálculo (vs V7 apenas visual) — D-093
8. V9 · Variação Máxima de Posição como métrica ordinal (vs desvio percentual V7 · vs IQR V5 futura) — D-097
9. V9 · taxonomia 4 classes primárias (vs V7 3 classes · vs V8 4+1 consolidada) — D-098
10. V9 · escala de cardinalidade multi-eixo independente (vs V7 hierárquica-aditiva · vs V8 matricial multiplicativa) — D-100

Padrão derivado de C.5 — registrado em CONTEXT §9 Camada C como um dos 3 derivados práticos (junto com default declarado e warning vs conteúdo).

### `O que é warning em uma visão pode ser conteúdo em outra` 🆕📌

Padrão de método consolidado no refino DCV-V8 (D-076). Fenômenos estruturais (ausência, lacuna, inconsistência) podem ter **tratamento radicalmente diferente em visões distintas da mesma família** — o que em uma é warning informativo auditável, em outra pode ser conteúdo analítico primário.

**Exemplo canônico (V3 × V8):** em V3, "ausência do agrupador em ponto específico" é flag informativa auditável (`ausencia_ponto`, AJUSTE_LEVE) que não afeta cálculo — warning W-V3-AGRUP-AUSENCIA-PONTO (D-065). Em V8, "ausência da entidade no ponto" é **conteúdo analítico primário** — classificação Ausente (T-03 V8, D-072), contada, classificada, exibida na Matriz de Presença, sem gerar warning (motor está fazendo exatamente o que a visão pede).

**Mesmo dado de entrada, mesma detecção mecânica, papéis completamente diferentes.** O padrão respeita C.5: cada visão declara explicitamente o que o motor faz com cada fenômeno, sem assumir que "ausência é sempre warning" ou "lacuna é sempre ajuste leve" — a natureza analítica da visão determina.

Padrão derivado de C.5 — registrado em CONTEXT §9 Camada C como um dos 3 derivados práticos.

---

## 10bis. Padrões consolidados formalizados (20/04/2026)

Seção nova criada em 20/04/2026 após formalização efetiva dos 7 padrões consolidados que aguardavam formalização desde o fechamento da Fase 0. Formalização ocorreu na Sessão de Alinhamento Técnico Fase 0 → Fase 1 via D-122 a D-129 (Opção A escolhida pela Usuária). 5 padrões viraram princípios derivados em CONTEXT §9 Camada C · 2 padrões viraram padrões estruturais de produto em CONTEXT §13.

Cada entrada abaixo consolida nome canônico · abreviação quando aplicável · enunciado resumido · escopo · aplicações consolidadas · referência canônica ao D-XXX de origem. Enunciado completo, rationale e impacto no método vivem em CONTEXT.

### `CPCO · Consolidação Pré-Cálculo Obrigatória` 🆕📌 (princípio derivado · CONTEXT §9 Camada C · C.D1)

Princípio derivado formalizado em **D-122**. Toda visão que opera sobre valores consolidáveis declara explicitamente o modo da base (Transacional × Pré-agregado × outros modos específicos da visão) antes do cálculo analítico. T-AGRUPA é invocada obrigatoriamente · operando consolidação real no modo Transacional, ou operando em no-op validado no modo Pré-agregado (verifica unicidade de chave e gera warning estrutural se duplicada). Nenhum cálculo analítico sobre valores ocorre sem essa declaração explícita e sem essa invocação obrigatória.

Deriva de C.2 (nada silencioso) + C.5 (default declarado do modo da base). Escopo: 9 das 11 visões (todas exceto V1 e V11). Adaptável via D-073.

**5 aplicações consecutivas:** V8 D-074 (origem) · V7 D-082 · V9 D-092 · V5 D-102 (adaptação V5-específica em 3 modos sem consolidar valores) · V6 D-111 (consumo padrão · reforça tronco comum).

### `TED · Thresholds Editáveis Declarados` 🆕📌 (princípio derivado · CONTEXT §9 Camada C · C.D2)

Princípio derivado formalizado em **D-123**. Todo parâmetro numérico operacional de uma visão (limiar de classificação, faixa de leitura, critério de outlier, threshold de densidade, tolerância, corte) aparece como default declarado visível na configuração da visão antes da execução, é editável em painel de "Configurações avançadas" com granularidade camada-por-camada, e é persistido em T-MODELO junto com a configuração da visão. Defaults silenciosos no motor (revelados apenas no diagnóstico pós-execução) não são permitidos.

Deriva de C.5 + derivado informal "default declarado" D-024. Escopo: todas as 11 visões com parâmetros numéricos operacionais.

**6 aplicações consecutivas:** V4 D-040 (origem · limiares ABC) · V7 D-084 + D-089 · V8 D-078 · V9 D-097/D-098 · V5 D-104 · V6 D-116 (3 thresholds de densidade + 6 thresholds no Resumo Executivo).

### `BAD · Base Analítica e Diagnóstico` 🆕📌 (princípio derivado · CONTEXT §9 Camada C · C.D3)

Princípio derivado formalizado em **D-124**. A exportação Excel de toda visão substitui a aba "Dados Brutos Processados" por duas abas separadas de papel distinto: Base Analítica (1 linha por unidade analítica consolidada da visão — elemento, célula, observação — com todas as classificações e atributos derivados) e Diagnóstico (sempre última aba · D-017 · contagens estruturais agregadas, ajustes do motor, warnings catalogados, rastreabilidade de transformações). A rastreabilidade dos dados originais vive no Diagnóstico como contagens estruturais, não como cópia linha-a-linha.

Deriva de C.2 (nada silencioso) + economia de exportação. Escopo: todas as 11 visões. Reforça D-017 (Diagnóstico sempre como última aba).

**5 aplicações consecutivas:** V8 D-078 (origem) · V7 D-089 · V9 D-099 · V5 D-108 · V6 D-119. Cada aplicação adapta "unidade analítica" à natureza da visão · V8 = entidade × ponto do eixo · V7 = elemento · V9 = identificador · V5 = observação válida · V6 = célula da matriz.

### `Resumo Executivo em 6 Blocos` 🆕📌 (padrão estrutural de produto · CONTEXT §13.5)

Padrão estrutural de produto formalizado em **D-125**. Toda visão oferece um Resumo Executivo como primeira aba da exportação Excel, estruturado em 6 blocos fixos: (1) Cabeçalho (metadados da execução) · (2) Números-âncora (contagens e totais estruturais da unidade analítica) · (3) Distribuição (como o conteúdo se distribui pela taxonomia) · (4) Elementos destacados (top N por critério declarado) · (5) Leitura qualitativa com síntese (N leituras + default · thresholds editáveis padrão TED) · (6) Qualidade estrutural (warnings, ajustes, integridade · padrão BAD).

Adaptações via D-073 permitidas preservando a espinha de 6 blocos. Supressão de bloco inteiro não é permitida.

**7 aplicações consecutivas:** V4 D-044 (origem · 5 leituras qualitativas) · V3 · V8 (Bloco 4 como "movimentações do intervalo") · V7 · V9 · V5 (Bloco 4 como "valores destacados" em 3 sub-blocos) · V6 (Bloco 4 com sub-bloco 4b · ausências destacadas).

### `Coração Visual da Visão` 🆕📌 (padrão estrutural de produto · CONTEXT §13.6)

Padrão estrutural de produto formalizado em **D-126**. Toda visão declara uma aba da exportação Excel como Coração Visual · a aba que materializa visualmente a contribuição analítica primária da visão em formato gráfico ou matricial adequado à natureza analítica. Aba obrigatória, nomeada conforme a identidade da visão, contém o ativo visual primário (gráfico nativo Excel, tabela matricial formatada, ou combinação).

**7 aplicações consecutivas:** V4 Composição Principal · V7 Mapa de Grupos · V8 Matriz de Presença · V9 Mapa de Perfil · V5 Mapa de Distribuição · V10 Curva Pareto · V6 Matriz de Cruzamento.

**Retroação diferida:** V1, V2 e V11 ganham declaração formal de Coração Visual nas Specs S-V2, S-V1, S-V11 (Fase 2). Candidatos naturais: Matriz de Confronto V2 · Mapa de Conciliação V1 · Mapa de Aderência V11.

### `MBO · Matriz de Bloqueios Operacionais` 🆕📌 (princípio derivado · CONTEXT §9 Camada C · C.D4)

Princípio derivado formalizado em **D-127**. Toda visão declara uma matriz de bloqueios operacionais estruturais numerados no formato **B-VN-NOME** em seção dedicada do DCV e da Spec. Cada bloqueio declara: (a) condição estrutural que o aciona, (b) comportamento padrão (recusa de execução), (c) escapável × não-escapável, (d) microcopy de explicação, (e) warning associado quando escape é acionado. Nenhum comportamento de caso-limite pode ser inventado pelo motor · ou há comportamento declarado, ou há bloqueio declarado.

Deriva de C.3 (sem invenção de comportamento). Padrão de nomenclatura: B-VN-DESCRITOR (VN = V2..V11 · DESCRITOR = UPPERCASE com hífen). Exemplos: B-V5-CAMPO-PRINCIPAL-NAO-NUMERICO · B-V6-EIXOS-IGUAIS · B-V8-BASE-VAZIA · B-V9-MINIMO-OPERACIONAL.

**5 aplicações consecutivas:** V7 §8.1 · V8 §8 · V9 §7 · V5 §7 (12 bloqueios) · V6 §7 D-120 (13 bloqueios).

### `ECP · Escala de Cardinalidade com Patamares` 🆕📌 (princípio derivado · CONTEXT §9 Camada C · C.D5)

Princípio derivado formalizado em **D-128**. Toda visão declara uma escala de cardinalidade em 3+ eixos de cardinalidade relevantes à sua natureza analítica, cada eixo estruturado em patamares numerados sequencialmente no formato P1 normal · P2 alerta leve · P3 alerta forte · P4 bloqueio escapável. A estrutura adaptativa dos eixos é justificada via D-073 conforme a natureza analítica da visão. Nenhuma visão herda cegamente a estrutura de eixos de outra visão · cada declaração é ato de design que afirma a natureza analítica da visão.

Deriva de C.1 (determinismo absoluto) + aplicação estrutural de D-073 (meta-padrão).

**5 aplicações com estruturas distintas:**
- V7 hierárquica-aditiva (Elementos dentro de grupos)
- V8 multiplicativa (entidades × pontos do eixo = células da matriz)
- V9 multi-eixo independente ortogonal (elementos · métricas · agrupadores)
- V5 multi-eixo independente ortogonal alinhada com V9 (observações · agrupador · diversidade)
- V6 bivariada simultânea com produto da matriz como eixo V6-específico (Eixo1 individual · Eixo2 individual · Matriz produto)

---

## 11. Termos a evitar (anti-glossário)

Termos que já apareceram mas que **não devem ser usados** no método atual:

- ❌ **"Dados Brutos Processados" (como aba da exportação Excel)** 🆕 — apareceu em múltiplos prévios da Fase 0 como aba proposta para copiar os dados originais com classificações anexadas. Formalmente rejeitada em **D-124** (padrão BAD · Base Analítica e Diagnóstico) após 5 aplicações consecutivas de descarte em favor de duas abas separadas de papel distinto: **Base Analítica** (1 linha por unidade analítica consolidada da visão) + **Diagnóstico** (contagens estruturais agregadas, sempre última aba por D-017). Rationale: aba Dados Brutos Processados seria redundante (usuário já tem o arquivo original) e economicamente custosa em bases volumosas. Rastreabilidade vive no Diagnóstico como contagens estruturais, não como cópia linha-a-linha. Ver §10bis · entrada BAD.
- ❌ **"Spec final"** — toda spec é potencialmente revisável; usar "spec aprovada" + data
- ❌ **"V2 está pronta"** — usar critério: DCV aprovado + Spec aprovada (com wireframe) + Base + Código + App + Validação Visual
- ❌ **"Confiar no Gamma como spec"** — Gamma é formatação de documento apresentável, nunca gerador de artefato técnico
- ❌ **"N-Motores" · "G-MOT" · "B-NR" · "V-Nb" · "N-VN" · "V-0c" · "T-XXX"** — todos descontinuados; ver seção 3
- ❌ **"Onda padrão" · "Onda futura"** — substituído por "ordem por famílias conceituais"
- ❌ **"Funcionou em teste então está pronto"** — princípios B.3 e B.4 são absolutos
- ❌ **"Esqueleto de tela"** — substituído por "wireframe funcional" (termo canônico no CONTEXT v2)
- ❌ **"Líder Geral"** (V9) — ambíguo com "Líder" oficial (classe primária V9); texto explicativo pode aparecer, rótulo oficial do motor é apenas "Líder" (prévio 6.6 · T-01 V9)
- ❌ **"Baixo Desempenho"** (V9) — interpretativo; "Retaguarda" é rótulo neutro de posição no ranking, não juízo de desempenho (prévio 6.6 · T-01 V9 · padrão D-087 de rótulos descritivos)
- ❌ **"Ponto forte / ponto fraco"** (V9) — interpretativo; rótulos V9 descritivos ("maior desvio positivo", "Posição 1") em vez de interpretativos (padrão V7 D-087 preservado · T-01 V9)
- ❌ **"Percentil"** como rótulo oficial (V9) — V9 é normativa em **posição/rank**, não percentil. "Percentil" pode aparecer como comunicação explicativa em texto pedagógico, mas nunca como rótulo oficial de campo, coluna ou saída. Alternativa futura em P-V9-09-Evo como indicador complementar (prévio 4.4 · T-01 V9)
- ❌ **"Peso por métrica"** em UI do MVP (V9) — V9 é equal-weighted por arquitetura; MVP não tem pesos. Não usar em UI para não gerar expectativa. Pesos ficam em P-V9-01-Evo (prévio 4.5 · T-06 V9)
- ❌ **"Aglutinador"** — usado no DCV prévio da V3 para o que o TabloFlow chama de "agrupador" (termo canônico §5). Desalinhamento corrigido no refino DCV-V3 (T-01). Termo nunca foi canônico em nenhum documento aprovado — registrado aqui apenas para evitar reaparecimento em próximos prévios.
- ❌ **"Recorrente" · "Recuperado" · "Perdido"** — usados no DCV prévio da V8 para as classes de presença por ponto. Substituídos no refino DCV-V8 (D-072) por **Contínuo · Retornou · Ausente** respectivamente. Rationale da troca: (1) "Recorrente" carrega carga de frequência/ritmo que exagera o escopo da classificação — que é microscópica (ponto atual vs ponto anterior apenas), não macroscópica; "Contínuo" descreve o que o motor observa sem extrapolar. (2) "Recuperado" carrega voz passiva + agência ("o sistema recuperou") que soa estranho em domínios além de carteira de clientes (SKU recuperado?); "Retornou" é voz ativa neutra funcionando em todos os domínios. (3) "Perdido" carrega semântica de churn negativa; "Ausente" é descritivo neutro. **Termos descartados podem sobreviver em microcopy de produto como contexto explicativo** ("análise de perdas" = filtro sobre Ausente), **nunca no contrato técnico do motor**. "Ativa/Inativa" também permanecem não oficiais (prévio V8 já explicita).
- ❌ **"Período" (como vocabulário estrutural V8)** — usado em todo o prévio V8. Substituído por **"Ponto do eixo"** (termo canônico D-061 unificado entre V3 e V8) no vocabulário estrutural. Rationale: "Período" restringe indevidamente à semântica temporal, inadequado em eixos lógico/ordinal ou manual. "Ponto do eixo" é abstrato e funciona em todos os tipos de eixo. **Rótulo "Período" permitido em tela** apenas quando o eixo detectado for temporal (Spec S-V8 decide microcopy de interface).
- ❌ **"Primeiro valor" (como regra de agregação V8)** — usado no DCV prévio da V8 PARTE 2.7 como uma das 3 opções de agregação. Descartada no refino (D-074). Rationale: "primeiro valor" depende de ordem de leitura — conflita com C.1 (determinismo absoluto) a menos que se declare critério de ordenação, o que reintroduz complexidade sem ganho analítico real. Substituída pelas 5 regras canônicas T-AGRUPA (D-026): soma (default) · média · máximo · mínimo · contagem.

---

**Para sugerir adição ou correção neste glossário:** abrir conversa com o Arquiteto, descrever o termo e o contexto, fechar a conversa com kit de encerramento que inclui a alteração deste arquivo.
