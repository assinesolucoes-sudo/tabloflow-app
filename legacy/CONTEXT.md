# CONTEXT.md — TabloFlow

Documento de referência do projeto. Contém o método, a arquitetura, as fontes de verdade e os princípios invioláveis que regem toda sessão de trabalho.

**Última atualização:** 23/04/2026 — Sessão **A-V2** · 2ª aplicação do padrão "sessão combinada" (produção do prompt + retrospectiva em um único bloco Arquiteto · V-V2 foi a 1ª aplicação · padrão **formalizado em D-155** nesta sessão · convenção Família A desde V-V1/A-V1). Esta sessão produziu:
- **Prompt técnico A-V2** para Claude Code implementar `app_v2.py` Streamlit · 11 telas do wireframe_v2.html · sequência canônica motor_upload → motor_base → executar_v2 → exportar_resultado · gate B.4 inviolável · testes via `streamlit.testing.v1.AppTest`
- **Retrospectiva A-V2** · 301/301 testes verdes (291 anteriores + 10 novos do app_v2) · validação contra Spec §3 + wireframe HTML + restrições invioláveis C.1-C.5 integral
- **5 decisões técnicas puras formalizadas:** **D-152** (`streamlit.testing.v1.AppTest` como convenção de testes de app da Família A · estratégia β validada empiricamente) · **D-153** (TED renderizado em sidebar global em vez de expander na E3 · preserva os 4 requisitos de C.D2 · evita widget-lifecycle churn em transições) · **D-154** (bloco intermediário RESOL_CASO parqueado como P-V2-Evo-01 · motor V2 atual não pré-detecta casos estruturais · revisável pós-VV-V2) · **D-155** (sessão combinada · produção de prompt + retrospectiva em um bloco Arquiteto · convenção Família A desde V-V1/A-V1) · **D-156** (padrão VV-VN · Validação Visual acompanhada modalidade C mista com 3 pontos-chave canônicos · substitui VV solo declarada em §15.1)

**Nova seção §15.8 · Padrão VV-VN (Validação Visual acompanhada)** formaliza modalidade C mista · Arquiteto presente em chat concomitante · Usuária opera silenciosamente com 3 pontos-chave canônicos (pós-processamento · pré-checklist · pós-exportação) + gatilhos livres. Princípio 4 de D-131 preservado · gate B.4 inviolável · Arquiteto não decide ✅/❌. Nova categoria "validação de produto" adicionada ao vocabulário de declaração de conteúdo decisional (§14 · princípio 3).

Padrão D-131 considerado **maduro após 10 aplicações consecutivas** · permanece vigente na Fase 2 sem modificações estruturais (11ª e 12ª aplicações em V-V2 e A-V2 · princípio 3 estendido com 4ª categoria em D-156).

**Fase 1 · Fundação CONCLUÍDA (21/04/2026)** · 5 de 5 blocos verdes. Suite pytest após A-V2: **301/301 verdes** (232 Fundação + 59 visao_v2 + 10 app_v2 · crescimento natural).

**V2 · Análise Comparativa entre Referências · 4 de 5 quadrados verdes:** S-V2 ✅ · base_v2_cliente ✅ · V-V2 ✅ (D-151 · 291 testes) · A-V2 ✅ (D-152-D-156 · 10 testes novos · 301/301 total) · **VV-V2 ⬜** (próxima sessão).

**Próximo bloco operacional:** **VV-V2** · primeira aplicação de D-156 · Usuária carrega `base_v2_cliente.xlsx` no `app_v2.py` · opera silenciosamente · aciona Arquiteto em 3 pontos-chave + gatilhos livres · aprova 4/4 ✅ no checklist derivado de `casos_esperados.yaml` · fecha V2 em 5/5.

Histórico recente (ordem cronológica reversa): A-V2 (esta · 23/04/2026 · D-152/D-153/D-154/D-155/D-156 · 301/301 verdes) · V-V2 (22/04/2026 · D-151 · 291/291 verdes · 1ª aplicação de sessão combinada) · S-V2 (22/04/2026 · 2 sessões · spec_v2.md + wireframe_v2.html + base_v2_cliente + gerar_base_cliente.py · 1ª aplicação de D-147/D-148/D-149) · ALINHA-Fase-1→Fase-2 (21/04/2026 · D-147/D-148/D-149/D-150) · retrospectivas F-BASE/F-EXP/F-TRANS/F-MOT (21/04/2026) · ALINHA-Fundação-Design→F-MOT (21/04/2026 · 2ª aplicação ALINHA · D-142 · D-140 e D-141 retroativas).

---

## 1. O que é o TabloFlow

O TabloFlow é uma plataforma analítica dividida em dois módulos:

- **Módulo 1 · TabloAnálise** — 11 visões analíticas que leem bases tabulares e entregam leitura estruturada, auditável e exportável em Excel. As visões cobrem confronto entre bases, comparação entre estados, análise sequencial, composição, ranking, desvio, dispersão e cruzamento.
- **Módulo 2 · TabloPrep** — operações de preparação de dados (filtro, deduplicação, normalização, enriquecimento) que alimentam o Módulo 1.

A plataforma atua como **camada intermediária** entre dados tabulares recebidos do usuário e análise estruturada. Três princípios definem seu posicionamento:

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

**Fluxo de produção de cada DCV (3 etapas):**

1. **Rascunho** — Usuária + ChatGPT produzem o DCV prévio usando o template `MODELO_DCV_PREVIO.md` e materiais de produto. Exceção formalizada: Arquiteto pode produzir o prévio quando captar o tema melhor em sessão dedicada, mantendo a natureza de "prévio" (pendências abertas, decisões não fechadas).
2. **Refino** — Arquiteto recebe o prévio e retorna o DCV final aplicando o padrão TabloFlow (distinção rigorosa entre conceitos, pendências P-NN enumeradas com opções e trade-offs, alinhamento com DCVs já aprovados).
3. **Aprovação** — Usuária valida e o DCV passa a status aprovado.

**Critério de conclusão da Fase 0:** todos os **11 DCVs** do Módulo 1 aprovados.

**Status atual da Fase 0 · CONCLUÍDA (20/04/2026).** 11 de 11 DCVs aprovados: V2 · V1 · V11 · V4 · V10 · V3 · V8 · V7 · V9 · V5 · V6.

### Fase 1 · Fundação

**Objetivo:** consolidar os requisitos de motor, contratos, transversais e exportação que emergem dos 11 DCVs aprovados e implementar a fundação que sustenta **todas** as visões.

**Artefatos da Fase 1:**

- Spec consolidada dos motores (`motor_upload`, `motor_base`)
- Spec de contratos de resultado (`UploadResult`, `MotorResult`, padrão `VNResult`) com **receptividade a IA declarada** (D-130 · serialização JSON-compatível · enums explícitos · rastreabilidade acessível)
- Spec dos componentes transversais identificados nos DCVs (ver § 6)
- Spec da exportação Excel padrão (estrutura de abas comum · Resumo Executivo em 6 Blocos · Coração Visual · filtros · formatos)
- Base sintética de fundação — única, multi-aba, cobrindo todos os casos de motor identificados nos DCVs
- Implementação de tudo acima em código (`/src/motor_*.py`, `/src/transversais/`, `/src/exportacao.py`)
- Bateria de testes da fundação, validada em base com volume realista

**Critério de conclusão da Fase 1:** motores + contratos + transversais + exportação validados por testes automatizados E por inspeção manual da Usuária da base de fundação processada.

**Status atual da Fase 1 · CONCLUÍDA (21/04/2026).** 5 de 5 blocos verdes (G-FUND · ALINHA-Fundação-Design→F-MOT · F-MOT · F-TRANS · F-EXP · F-BASE). Suite: 232/232 em 4.89s. Artefatos estabilizados em disco · operacional como fundação consumível pela Fase 2.

### Fase 2 · Visões

**Objetivo:** implementar as 11 visões sobre a fundação aprovada, na ordem lógica por famílias conceituais.

**Para cada visão N, cinco artefatos sequenciais:**

1. **Spec da visão** — contém três seções obrigatórias: (a) contratos lógicos, (b) regras de cálculo, (c) **wireframe funcional** (descrição textual ou esquemática do fluxo de tela: estados, configuração, microanálise, exportação). O wireframe funcional recebe aprovação explícita da Usuária antes do código iniciar, mesmo vivendo no mesmo arquivo da Spec — ver princípio B.2. **Para Família A · acompanha `/specs/wireframe_vN.html` como validação visual antecipada** (D-149). **Inclui seção §3.x · Checklist de Validação Visual derivado mecanicamente de `casos_esperados.yaml`** (D-148).
2. **Base sintética específica** da visão — **condicional** ao critério de D-147 (3 perguntas + default declarado). Quando B-VN é dispensado, a visão consome `base_fundacao.xlsx` diretamente.
3. **`visao_vN.py`** — implementação do motor da visão sobre a fundação.
4. **`app_vN.py`** — app Streamlit executando o wireframe funcional aprovado · consome `base_vN_cliente.xlsx` como entrada canônica da Validação Visual (D-149).
5. **Validação Visual** — Usuária carrega `base_vN_cliente.xlsx` no app, marca cada item do checklist derivado em ✅/❌, aprova quando todos os itens estão ✅ (qualquer ❌ dispara investigação conduzida pelo Arquiteto).

**Ordem oficial de implementação por famílias:**

| Ordem | Família | Visões | Racional |
|---|---|---|---|
| 1 | A · Confronto | V2 → V1 → V11 | V2 compara dois estados; V1 estende para duas bases com chave; V11 trata duas bases sem chave via aderência |
| 2 | C · Composição | V4 → V10 | V4 cobre composição completa incluindo ABC; V10 é especialização Pareto |
| 3 | B · Sequência | V3 → V8 | V3 acompanha valor em eixo ordenado; V8 acompanha presença no mesmo eixo |
| 4 | D · Posição relativa | V7 → V9 | V7 é desvio simples da média do grupo; V9 é ranking multidimensional |
| 5 | E · Estrutura interna do recorte | V5, V6 | V5 univariado numérico (dispersão e outliers); V6 bivariado categórico (cruzamento). Par operacionalmente distante — sem transversais centrais comuns |

**Bloco IA-Família-A** (D-130) · após Família A validada (V2 · V1 · V11 aprovadas em Fase 2) · adiciona Papel A (sugestão de preenchimento de configuração pré-execução) e Papel B (leitura em linguagem natural do resultado estruturado) às 3 visões da Família A. Papel C (recomendação de qual visão usar) fica em bloco separado IA-Meta após Família C validada.

**Critério de conclusão da Fase 2:** 11 visões com Validação Visual registrada na planilha (aba 2 · Painel da fase ativa · 5 quadrados ✅ por visão).

**Condução da Fase 2 · §15.** Processo operacional completo formalizado em §15 · ciclo de 5 artefatos por visão · convenções de Spec · critério de base · derivação do checklist · wireframe HTML · plano de ~6 sessões por visão. Padrão D-131 permanece vigente sem modificações estruturais (10ª aplicação em ALINHA-Fase-1→Fase-2 e segue na Fase 2 inteira).

---

## 4. Famílias conceituais do Módulo 1

As 11 visões se agrupam em 5 famílias conceituais. Essa divisão guia a reutilização de transversais e a ordem de implementação.

- **Família A · Confronto entre universos** — V2 (dois estados de uma base), V1 (duas bases com chave), V11 (duas bases sem chave, por aderência). Família mais rica do Módulo 1 em função do peso do confronto no uso contábil brasileiro. V1 e V11 compartilham T-DUAL mas operam com motores distintos (V1 match determinístico por chave declarada; V11 match probabilístico por aderência contextual). Não há relação de view especializada entre V1 e V11 como V4↔V10; são visões autônomas da mesma família com problemas analíticos distintos.
- **Família B · Sequência ao longo de eixo ordenado** — V3 (valor no tempo), V8 (presença no tempo). Visões autônomas (não há view especializada entre elas), unidas por consumo de T-EIXO. V3 rastreia valor em cada ponto do eixo e classifica estruturalmente (Aumentou/Reduziu/Estável/Não aplicável) com camada semântica via T-SEMA; V8 rastreia presença/ausência em cada ponto e classifica em 4 classes primárias por ponto (Novo · Contínuo · Retornou · Ausente) + Constante como classificação consolidada do intervalo (D-072). V8 não consome T-SEMA — presença/ausência não tem direção universal (D-071). Vocabulário declarativo autossuficiente em cada visão — fronteira V3×V8 navegada no DCV, não em interface operacional (análogo V11↔V1 · D-058). DCV-V3 estabelece padrão de T-EIXO herdado por V8. DCV-V8 cumpre retroação diferida D-060 em seu §2.3 (bloco "Relação com V3" simétrico).
- **Família C · Composição e participação** — V4 (participação, ABC, multi-métrica), V10 (Pareto puro). *Sobreposição conceitual significativa entre V4 e V10 — V10 é, em larga medida, caso particular de V4 modo 2.*
- **Família D · Posição relativa** — V7 (desvio da média do grupo), V9 (ranking multidimensional). Visões que analisam como cada elemento se posiciona em relação a um benchmark calculado internamente sobre os próprios dados. V7 calcula o benchmark como média do grupo ao qual o elemento pertence (desvio univariado intra-grupo); V9 calcula o benchmark como posição consolidada em múltiplas métricas ordenadas com direção declarada (ranking multidimensional cross-elementos). Ambas consomem T-SEMA (V7 com efeito apenas visual D-087 · V9 com efeito direto no cálculo D-093 · aplicação canônica do padrão D-073 "herança adaptada à natureza analítica"); ambas consomem T-AGRUPA (V7 com regra única · V9 com regra independente por métrica D-092); ambas consomem T-RANK (V7 intra-grupo D-088 · V9 cross-elementos-dentro-do-agrupador D-096). **Não há view especializada entre elas** — são visões autônomas da mesma família com problemas analíticos distintos, unidas por "benchmark interno sobre os próprios dados" como posicionamento da família. Vocabulário declarativo autossuficiente em cada visão. DCV-V9 §2.3 cumpre a retroação diferida D-081 com §2.3 "Relação com V7" simétrico (D-091). **Família D fechada em Fase 0** após aprovação do DCV-V9.
- **Família E · Estrutura interna do recorte** — V5 (dispersão e outliers · estatística descritiva univariada de um campo numérico), V6 (cruzamento de dois campos categóricos). Visões que **expõem propriedades estruturais internas de um recorte da base** sem comparar com referência externa, sem benchmark interno por grupo, sem eixo ordenado, sem total geral. V5 opera sobre **um campo numérico** (univariado); V6 opera sobre **dois campos categóricos cruzados** (bivariado). Família com par operacionalmente distante — V5 e V6 não compartilham transversais centrais e não navegam fronteira em interface operacional. Adaptação D-073 ao próprio método de posicionamento de família: famílias com par operacional próximo (B · D) merecem tabela de retroação diferida com células *(a confirmar)* (D-060 e D-081); famílias com par operacional distante (E) merecem declaração enxuta de convivência sem retroação diferida formal (D-110 lado 1 via V5 · D-121 lado 2 via V6 cumprindo o gancho). **Família E fechada em Fase 0.**

---

## 5. Fontes de verdade

Hierarquia autoritativa dos documentos do projeto:

| Fonte | Papel | Autoridade |
|---|---|---|
| **Blueprint (Gamma)** | Referência estratégica completa das visões, mantida pela Usuária | Intenção |
| **CONTEXT.md** (este) | Método, arquitetura, princípios invioláveis | Regra permanente |
| **DECISIONS.md** | Log cronológico de decisões com rationale | Histórico e porquê |
| **TabloFlow_Estado_do_Projeto.xlsx** | Estado vivo · 5 abas com papéis explícitos · aba 1 Onde estou no todo (Horizontes Futuros · D-150) · aba 2 Painel da fase ativa (dashboard da Fase 2 · 5 quadrados por visão) · aba 3 Detalhe técnico das visões · abas 4-5 arquivo das Fases 0-1 | Estado atual |
| **DCVs em `/specs/dcv/`** | Compreensão validada de cada visão | Requisito (o quê) |
| **Specs em `/specs/`** | Contratos + regras + wireframe funcional por visão | Implementação (o como) |
| **Wireframes visuais em `/specs/wireframe_vN.html`** | Representação visual do wireframe funcional para validação antecipada (D-149 · obrigatório Família A · opcional demais) | Apoio à aprovação da Usuária |
| **`/bases/base_fundacao.xlsx`** | Dataset sintético único da Fundação · 14 abas SEED=42 · fonte de verdade para testes automatizados (D-140) | Estado atual |
| **`/bases/casos_esperados.yaml`** | Gabarito canônico de validação · 61 assertions · consumido em 3 pontos (F-BASE · F-MOT/F-TRANS · checklist de Validação Visual Fase 2 via D-148) | Regra permanente |
| **`/bases/base_vN_cliente.xlsx`** | Recorte cliente-friendly de `base_fundacao.xlsx` (D-149) · arquivo canônico de entrada para Validação Visual · Fase 2 | Apoio à Validação Visual |
| **GLOSSARIO.md** | Vocabulário canônico do projeto | Terminologia |

**Regras de conflito:**

- Se CONTEXT e planilha divergirem sobre regra permanente → CONTEXT prevalece.
- Se CONTEXT e planilha divergirem sobre estado atual → planilha prevalece.
- Se Blueprint e spec local divergirem → spec prevalece para execução; Blueprint prevalece para intenção.
- Se DCV e spec divergirem → DCV prevalece (DCV é o requisito; spec é a implementação).
- Se spec e código divergirem → investigar antes de assumir prevalência; bug pode estar em qualquer um dos dois.
- Se `base_fundacao.xlsx` e `base_vN_cliente.xlsx` divergirem → base mestre prevalece (D-149 · cliente é recorte mecânico · regenerar se divergir).

---

## 6. Componentes transversais identificados

Durante a leitura consolidada dos DCVs emergiram os seguintes componentes compartilhados entre visões. Todos entraram no escopo da Fase 1 (Fundação) e estão **implementados e testados em F-TRANS**:

| Sigla | Nome | Usado por |
|---|---|---|
| **T-AGRUPA** | Consolidação por agrupadores antes do cálculo, com regra de agregação configurável (soma, média, máx, mín, contagem). Reconhece padrões cronológicos pt-BR/pt-EN para ordenação inteligente quando aplicável (D-026). Suporta modo **no-op validado** quando base é declarada Pré-agregada (V7 D-082 · V8 D-074 · V9 D-092). V7 estende com **média ponderada opcional por campo de peso** em tipo Relativa (D-083). **V9 estende para aceitar regra de agregação independente por métrica** via dicionário `{metrica: regra}` em vez de regra única (D-092) — primeira consumidora com contrato multi-regra. **V5 estende com semântica V5-específica em 3 modos** (D-102). **V6 entra como 9ª consumidora com consumo padrão** (D-111) — reforço do tronco comum da família V4/V7/V8/V9. Padrão formalizado como **CPCO · Consolidação Pré-Cálculo Obrigatória** em D-122 (§9 Camada C). | TODAS — exceto V1 e V11 (que preservam registros individuais em vez de consolidar) |
| **T-DIAG** | Diagnóstico estrutural obrigatório (aba no Excel + seção no Resumo Executivo). **Aba sempre posicionada como última aba do Excel** (regra transversal D-017). Suporta categorias `AJUSTE_LEVE` (motor ajustou sem perguntar) e `DECISAO_USUARIO` (usuário escolheu em caso estrutural) — D-021. **Serialização JSON-compatível obrigatória para receptividade a IA** (D-130). | TODAS |
| **T-SEMA** | Semântica maior-é-melhor / menor-é-melhor / neutro. **Não aplicável a V8** — presença/ausência não tem direção universal (D-071). **V7 como sexta consumidora** com efeito apenas em visualização e ordem de apresentação do Resumo Executivo — cálculo sempre simétrico, independente de T-SEMA declarada (D-087). **V9 como sétima consumidora** com contrato distinto: **por métrica (2-6 direções simultâneas)** com **efeito direto no cálculo** — a Direção declarada determina a ordem de ordenação (decrescente × crescente) de cada métrica, que determina Posição → Score → Classificação; **sem default, declaração obrigatória por métrica** (D-093 · aplicação de D-073). | V2, V3, V7, V9 |
| **T-EIXO** | Eixo sequencial ordenado com intervalo De/Até, sem preenchimento de lacunas. **3 tipos canônicos** (temporal · lógico/ordinal · manual) com default declarado pelo motor e ordem final sempre confirmada pelo usuário. Herança do reconhecedor de padrões cronológicos pt-BR/pt-EN de D-026 (T-AGRUPA) para o tipo temporal — zero duplicação. Detecção de lacunas depende do tipo (automática em temporal e ordinal com prefixo numérico; não em ordinal sem prefixo nem manual). Intervalo declarado vs efetivo preservados separadamente para auditoria. Formalizado em D-061 (origem DCV-V3) | V3, V8 |
| **T-RANK** | Ranking determinístico com regra de desempate. Configurável via parâmetro `regra_desempate` opcional (D-041). Regra default de 3 níveis: (1) valor decrescente, (2) concatenação de agrupadores alfabética case-insensitive, (3) ordem de inserção original. Tolerância 1e-9 para floating point. **V7 como sexta consumidora** com regra V7-específica 4 níveis (D-088). **V9 como sétima consumidora** com regra V9-específica 4 níveis + novo escopo `cross_elementos_dentro_do_agrupador` (D-096). **V6 como oitava consumidora** com regra V6-específica 4 níveis (D-115). | V1, V4, V7, V9, V10, V11, V6 |
| **T-ACUM** | Acumulado progressivo monotônico | V4, V10 |
| **T-ABC** | Classificação A/B/C por limiares de acumulado | V4, V10 |
| **T-PIVOT** | Pivot POR_LINHAS → POR_COLUNAS. **Três semânticas de pivot formalizadas**: estados empilhados para Modo 4 V2 (D-026) · multi-medida para V4 com empilhamento de medidas distintas (D-039) · **pontos do eixo para V3** com empilhamento de valores do eixo sequencial (D-062). | V2, V3, V4 |
| **T-DUAL** | Extensão do motor_upload para modo dual: 2 arquivos OU 1 arquivo com 2 abas. Produz UploadResult com Origem/Comparado nomeados (D-018) | V1, V11 |
| **T-MODELO** | Salvar e aplicar configuração como modelo reutilizável (padrão estrutural de produto, §13.3). **Persistência obrigatória de thresholds editáveis** (D-123 · padrão TED). | TODAS |
| **T-FUZZY** | Similaridade textual entre strings. Algoritmo híbrido: similaridade por trigramas de caracteres + presença de tokens-chave. Pesos internos fixos encapsulados (não expostos ao usuário). Normalização prévia interna (lowercase · remoção de acentos · remoção de caracteres não-alfanuméricos exceto espaço). API pura determinística: `(texto_A, texto_B) → score ∈ [0,1]`. Confirmado como transversal da Fundação em D-052 | V11 (MVP) · V1 (roadmap P-V1-02-Evo) |
| **T-CONCAT** **Fundação (D-135)** | Composição/concatenação declarada de múltiplos campos-fonte em campo textual único. Até 3 campos-fonte · separador fixo espaço · assimetria permitida (lados podem compor com quantidades diferentes) · tratamento de nulos (campos nulos pulados · todos nulos resulta em string vazia). Implementação na Fundação como transversal fundamental em F-TRANS · V11 consome no MVP · extração futura para M2.CONCAT reusa código sem reescrita (renomeação apenas). | V11 (MVP) · M2.CONCAT (futuro) |
| ~~**M2.STACK**~~ | **Movido para M2 (D-135)** — empilhamento de múltiplas abas estruturalmente idênticas fora do escopo da Fundação. V3 · V6 · V8 mantêm multi-aba como roadmap pós-MVP conforme DCVs aprovados (P-V3-01-Evo · P-V8-01-Evo · P-V6-02-MULTIABA-Evo). Operação M2 futura · posicionamento confirmado. | V3, V8, V6 (roadmap M2) |

Os **12 transversais da Fundação** (T-AGRUPA · T-DIAG · T-SEMA · T-EIXO · T-RANK · T-ACUM · T-ABC · T-PIVOT · T-DUAL · T-MODELO · T-FUZZY · T-CONCAT) estão implementados em `/src/transversais/` com testes verdes (F-TRANS · 127 testes).

**Requisitos novos consolidados em V6 para a Fundação (já implementados):**

1. **motor_base com `column_meta.tipo_estrutural`** (5 valores enum: `CATEGORICO_ELEGIVEL` · `NUMERICO_CONTINUO` · `TEMPORAL` · `BOOLEANO` · `VAZIO_OU_AMBIGUO`) como metadado estrutural de coluna · D-113 · D-133 · D-146.

2. **exportacao.py com formatação condicional de matriz** + **ColumnChart empilhado 100% nativo Excel** + **paginação de matriz grande** · D-118.

3. **exportacao.py com aba "Combinações Ausentes"** como template específico V6 · D-119.

**Requisito de receptividade a IA (D-130) · refinado em D-144:**

4. Contratos da Fundação com receptividade a IA declarada. **Result types analíticos** (VNResultBase · MotorResult) mantêm 3 requisitos integrais (Pydantic BaseModel + model_config · Field com description · `.para_contexto_ia()`). **Result types operacionais** (ExportacaoResult) mantêm 2 requisitos (dispensa `.para_contexto_ia()` por ausência de caso de uso analítico). Ratificado em código em F-MOT e F-EXP.

---

## 7. Tipos de bloco de execução

Um bloco é uma sessão de trabalho dedicada a um artefato específico. **Nunca misturar tipos diferentes na mesma sessão.**

| Prefixo | Significado | Fase |
|---|---|---|
| `DCV-VN` | Refino do DCV prévio da visão N pelo Arquiteto | Fase 0 |
| `DCV-OPN` | DCV equivalente para operação N do Módulo 2 | Fase 0 (M2) |
| `G-FUND` | Gate de Fundação: consolidação de requisitos dos DCVs e definição do escopo de motores, contratos, transversais e exportação | Fase 1 |
| `ALINHA-<Marco>→<próximo>` | Sessão dedicada ao fechar Marco (D-142) · 4 sub-blocos α·β·γ·δ | Transversal |
| `F-MOT` | Implementação dos motores da Fundação | Fase 1 |
| `F-TRANS` | Implementação dos transversais | Fase 1 |
| `F-EXP` | Implementação da exportação Excel padrão | Fase 1 |
| `F-BASE` | Geração da base sintética de Fundação | Fase 1 |
| `IA-Família-A` | Implementação de Papel A + Papel B da IA em V2, V1, V11 pós-validação | Pós-Fase 2 parcial |
| `IA-Meta` | Implementação de Papel C da IA (recomendação de visão) | Pós-Família C validada |
| `S-VN` | Spec da visão N (contrato + regras + wireframe funcional + checklist derivado + wireframe HTML Família A) | Fase 2 |
| `B-VN` | Base sintética da visão N (condicional a D-147) | Fase 2 |
| `V-VN` | Implementação de `visao_vN.py` | Fase 2 |
| `A-VN` | Implementação de `app_vN.py` | Fase 2 |

**Blocos descontinuados** (existiram em versões anteriores do método, preservados aqui apenas para leitura de histórico): `B-NR` · `V-Nb` · `N-Motores` · `G-MOT` · `N-VN` · `V-0c` · `T-XXX` · "onda padrão".

---

## 8. Estrutura de pastas

```
/tabloflow/
├── CONTEXT.md                          ← este arquivo
├── DECISIONS.md                        ← log cronológico de decisões
├── GLOSSARIO.md                        ← vocabulário canônico
├── Instrucoes_do_Projeto.md            ← como operar o projeto (Arquiteto + Usuária)
├── TabloFlow_Estado_do_Projeto.xlsx    ← estado vivo · 5 abas com papéis explícitos
│
├── /specs/
│   ├── /dcv/                           ← DCVs aprovados (Fase 0)
│   │   ├── dcv_v1.md ... dcv_v11.md
│   │   └── MODELO_DCV_PREVIO.md        ← template para Usuária + ChatGPT
│   ├── spec_fundacao.md                ← spec consolidada de motores + contratos + transversais + exportação (Fase 1)
│   ├── spec_v1.md ... spec_v11.md      ← specs das visões (Fase 2)
│   └── wireframe_v1.html ... wireframe_v11.html  ← wireframes visuais acompanhando Specs (D-149 · obrigatório Família A)
│
├── /src/
│   ├── motor_upload.py                 ← Fundação
│   ├── motor_base.py                   ← Fundação
│   ├── contratos.py                    ← Fundação (receptividade a IA declarada · D-130/D-144)
│   ├── exportacao.py                   ← Fundação (11 capabilities · 4 camadas topológicas)
│   ├── /transversais/                  ← 12 T-* implementados (F-TRANS)
│   ├── /utils/                         ← normalizacao_texto.py · reconhecedor_cronologico.py
│   ├── /geradores/                     ← gerar_base_fundacao.py · _auto_validar.py · gerar_base_cliente.py (D-149)
│   ├── visao_v1.py ... visao_v11.py    ← Fase 2
│   ├── app_v1.py ... app_v11.py        ← Fase 2
│   └── testes/                         ← 232 testes verdes (Fase 1 · cresce na Fase 2)
│
├── /bases/
│   ├── base_fundacao.xlsx              ← dataset sintético único · 14 abas · SEED=42 (D-140 · fonte única de verdade)
│   ├── casos_esperados.yaml            ← gabarito canônico · 61 assertions (D-141)
│   └── base_v1_cliente.xlsx ... base_v11_cliente.xlsx  ← recortes cliente-friendly para Validação Visual (D-149)
│
├── /legacy/
│   ├── context_v1.md                   ← CONTEXT anterior à D-014
│   ├── glossario_v1.md                 ← GLOSSARIO anterior à D-014
│   └── (artefatos pré-DCV preservados apenas para auditoria)
│
├── /files/                             ← material de produto da Usuária (Blueprint, diretrizes)
└── /.claude/, /.vscode/                ← configuração de ambiente
```

---

## 9. Princípios invioláveis

Dez princípios invioláveis organizados em três camadas, estendidos por **5 princípios derivados formalizados em 20/04/2026** que operacionalizam a Camada C. Rationale e histórico preservados em DECISIONS.md.

### Camada A · Princípios de método

**A.1 — Três fases sequenciais, sem sobreposição.**  
Fase 0 (Compreensão) → Fase 1 (Fundação) → Fase 2 (Visões). Nenhuma fase inicia sem a anterior estar 100% concluída. Tentar antecipar uma fase produz retrabalho, não velocidade.

**A.2 — Toda visão começa com DCV aprovado.**  
Sem DCV aprovado em `/specs/dcv/dcv_vN.md`, nenhuma spec, base ou código pode ser escrito para a visão. Aplica-se igualmente a novas visões, reescritas e evoluções significativas.

**A.3 — Arquiteto é o único gerador de artefato técnico.**  
Specs, bases sintéticas, prompts de bloco e refino de DCVs são produzidos pelo Arquiteto. ChatGPT apoia no rascunho de DCV prévio sob diretriz da Usuária. Gamma é ferramenta de formatação de documento final, nunca gerador de contrato técnico.

### Camada B · Princípios de artefato

**B.1 — Um bloco por sessão.**  
Cada sessão de trabalho (Claude Code, Arquiteto, ChatGPT) executa exatamente um tipo de bloco. Misturar tipos gera artefato inconsistente e decisão acoplada.

**B.2 — Spec tem três seções obrigatórias, incluindo wireframe funcional.**  
Contratos lógicos, regras de cálculo e **wireframe funcional** (esqueleto de tela em prosa ou textual, descrevendo estados, fluxo de configuração, microanálise e exportação). Spec sem qualquer uma das três seções está incompleta. O wireframe funcional é artefato destacado dentro do bloco S-VN: mesmo vivendo no mesmo arquivo da Spec, ele recebe **aprovação explícita da Usuária antes do código iniciar**. Essa dupla aprovação (contrato + wireframe) garante que UX e lógica nasçam juntas, não se divergindo no app. **Para Família A · dupla aprovação reforçada por wireframe visual HTML acompanhando** (D-149).

**B.3 — Base sintética exige volume realista.**  
Mínimo 50 linhas por aba, com aba CASOS_ESPERADOS contendo gabarito auditado. Base didática pequena (≤20 linhas) esconde bugs de volume — esse cenário já ocorreu e gerou rebaseline (D-007). **Na Fase 2 · critério D-147 decide se a visão consome `base_fundacao.xlsx` diretamente (default declarado quando 3 perguntas passam) ou se B-VN produz base específica.**

**B.4 — Nenhum artefato é concluído sem Validação Visual.**  
Para apps da Fase 2: Usuária carrega `base_vN_cliente.xlsx` (D-149) no app, processa, marca o checklist derivado de `casos_esperados.yaml` em ✅/❌ (D-148), valida clareza de campos e exportação Excel. Sem Validação Visual registrada na planilha (aba 2 · 5 quadrados ✅), a visão não é concluída. Testes automatizados não substituem essa etapa.

### Camada C · Princípios de operação

**C.1 — Determinismo absoluto nos motores.**  
Mesma entrada + mesma configuração → mesma saída, sempre. Qualquer não-determinismo (ordenação instável, dependência de floating point sem controle, seed não fixada em geradores) é bug.

**C.2 — Nada silencioso.**  
Todo ajuste estrutural aplicado pelo motor (pivot, consolidação, tratamento de nulos, correção de inconsistência) deve aparecer no diagnóstico. Nenhuma transformação invisível.

**C.3 — Sem invenção de comportamento.**  
Se a spec ou o DCV são ambíguos sobre um ponto, o Arquiteto ou Claude Code **pergunta**. Não inventa comportamento padrão, não "assume que a Usuária quer X". Ambiguidade vira pendência P-NN na spec ou decisão D-XXX em DECISIONS.md.

**C.4 — Decisão estrutural vira D-XXX.**  
Toda escolha que: (a) fecha pendência de spec, (b) muda contrato entre blocos, (c) seria custosa de redescobrir depois, ou (d) afeta mais de uma visão — vira entrada numerada em DECISIONS.md com rationale.

**C.5 — TabloFlow analisa sobre o dado informado, nunca decide por ele.**

O TabloFlow é meio de campo entre dados dispersos (ERPs, relatórios multiprocessos) e a análise humana — ocupa o espaço que hoje é ocupado pelo Excel. Sua função é estruturar o que hoje é feito manualmente, nunca tomar decisão analítica em nome do usuário. Toda análise opera sobre o que o usuário declarou (estrutura, agrupadores, regras, campos, tolerâncias). O sistema executa exatamente o que foi declarado, preserva o que encontrou e classifica de forma auditável — nunca interpreta, supõe ou corrige silenciosamente o dado. Quando houver ambiguidade de comportamento entre "o sistema decide X" e "o sistema apresenta o caso para o usuário ver", a escolha correta é sempre a segunda.

### Camada C · Princípios derivados formalizados (20/04/2026)

5 princípios derivados de C.1, C.2, C.3 e C.5 formalizados em 20/04/2026 via D-122 a D-128.

**C.D1 · CPCO — Consolidação Pré-Cálculo Obrigatória** (D-122)

*Enunciado:* Toda visão que opera sobre valores consolidáveis declara explicitamente o modo da base (Transacional × Pré-agregado × outros modos específicos da visão) antes do cálculo analítico. T-AGRUPA é invocada obrigatoriamente — operando consolidação real no modo Transacional, ou operando em no-op validado no modo Pré-agregado (verifica unicidade de chave e gera warning estrutural se duplicada). Nenhum cálculo analítico sobre valores ocorre sem essa declaração explícita e sem essa invocação obrigatória.

*Deriva de:* C.2 (nada silencioso) + C.5 (default declarado do modo da base).  
*Escopo:* 9 das 11 visões (todas exceto V1 e V11). Adaptável via D-073.

**C.D2 · TED — Thresholds Editáveis Declarados** (D-123)

*Enunciado:* Todo parâmetro numérico operacional de uma visão (limiar de classificação, faixa de leitura, critério de outlier, threshold de densidade, tolerância, corte) aparece como default declarado visível na configuração da visão antes da execução, é editável em painel de "Configurações avançadas" com granularidade camada-por-camada, e é persistido em T-MODELO junto com a configuração da visão. Defaults silenciosos no motor (revelados apenas no diagnóstico pós-execução) não são permitidos.

*Deriva de:* C.5 + derivado informal "default declarado" D-024.  
*Escopo:* Todas as 11 visões com parâmetros numéricos operacionais.

**C.D3 · BAD — Base Analítica e Diagnóstico** (D-124)

*Enunciado:* A exportação Excel de toda visão substitui a aba "Dados Brutos Processados" (cópia dos dados originais com classificações anexadas) por duas abas separadas de papel distinto: **Base Analítica** (1 linha por unidade analítica consolidada da visão — elemento, célula, observação — com todas as classificações e atributos derivados) e **Diagnóstico** (sempre última aba · D-017 · contagens estruturais agregadas, ajustes do motor, warnings catalogados, rastreabilidade de transformações). A rastreabilidade dos dados originais vive no Diagnóstico como contagens estruturais, não como cópia linha-a-linha.

*Deriva de:* C.2 (nada silencioso — rastreabilidade no Diagnóstico) + economia de exportação.  
*Escopo:* Todas as 11 visões.

**C.D4 · MBO — Matriz de Bloqueios Operacionais** (D-127)

*Enunciado:* Toda visão declara uma matriz de bloqueios operacionais estruturais numerados no formato **B-VN-NOME** em seção dedicada do DCV e da Spec. Cada bloqueio declara: (a) condição estrutural que o aciona, (b) comportamento padrão (recusa de execução), (c) se é escapável ou não-escapável, (d) microcopy de explicação ao usuário, (e) warning associado quando escape é acionado. Nenhum comportamento de caso-limite pode ser inventado pelo motor em tempo de execução — ou há comportamento declarado, ou há bloqueio declarado. Não há terceira opção.

*Deriva de:* C.3 (sem invenção de comportamento).  
*Escopo:* Todas as 11 visões.

**C.D5 · ECP — Escala de Cardinalidade com Patamares** (D-128)

*Enunciado:* Toda visão declara uma escala de cardinalidade em 3+ eixos de cardinalidade relevantes à sua natureza analítica, cada eixo estruturado em patamares numerados sequencialmente no formato P1 normal · P2 alerta leve · P3 alerta forte · P4 bloqueio escapável. A estrutura adaptativa dos eixos é justificada via D-073 conforme a natureza analítica da visão.

*Deriva de:* C.1 (determinismo absoluto) + aplicação estrutural de D-073 (meta-padrão).  
*Escopo:* Todas as 11 visões.

### Camada C · Derivados informais

**Padrão "default declarado"** (cristalizado em V2 · D-024 · referenciado em D-122/D-123/D-147): decisões analíticas relevantes podem ter default proposto pelo motor, desde que o default seja visível na configuração antes da execução, com opção fácil de alterar.

**Padrão "herança adaptada à natureza analítica"** (cristalizado em V8 · D-073 · ~15 aplicações documentadas): visões da mesma família conceitual não herdam padrões cegamente de uma visão para outra; herdam o que cabe à natureza analítica específica.

**Padrão "o que é warning em uma visão pode ser conteúdo em outra"** (cristalizado em V8 · D-076 · 4 aplicações): fenômenos estruturais (ausência, lacuna, inconsistência) podem ter tratamento radicalmente diferente em visões distintas.

---

## 10. Ritual de abertura de sessão do Arquiteto

Toda conversa nova começa com esta sequência:

1. Ler `CONTEXT.md` (este), `DECISIONS.md`, planilha de estado (5 abas) e `GLOSSARIO.md`.
2. Ler o artefato principal da sessão (DCV, spec, base, prompt) se anexado.
3. Validar coerência entre fontes — se houver conflito entre planilha e CONTEXT, sinalizar.
4. Confirmar próximo passo operacional da planilha (aba 1 · "Próximo Passo Operacional") antes de agir.

Na **Fase 1 e Fase 2** o ritual ganha elemento adicional derivado do princípio 3 de D-131 (sinalização proativa de densidade técnica): ao final do ritual de abertura, o Arquiteto declara explicitamente o conteúdo decisional esperado da sessão em 3 categorias · X decisões de negócio (Usuária decide · Arquiteto traduz) · Y decisões técnicas puras (Arquiteto resolve · sinaliza que resolveu) · Z execuções de código supervisionadas.

A Usuária pode acionar esta sequência a qualquer momento dizendo **"valide o estado"**.

---

## 11. Ritual de encerramento de sessão

Quando uma conversa gera decisão, artefato ou mudança de estado, o Arquiteto entrega proativamente o **kit de encerramento** (regra D-020, refinada por D-033). O kit é dividido em duas categorias conforme o que é mais econômico em cada lado:

**Itens produzidos pelo Arquiteto como arquivo completo para download:**

1. **`CONTEXT.md`** · arquivo completo atualizado, sempre que houver mudança de método ou estrutura (declaração explícita "sem mudança" quando não houver).
2. **`Instrucoes_do_Projeto.md`** · arquivo completo atualizado, sempre que houver mudança em método de condução ou como o Arquiteto opera (declaração explícita quando não houver).
3. **Artefato(s) produzido(s) na sessão** · DCV, spec, base sintética, prompt de bloco, wireframe HTML — como arquivos específicos do tipo correto.
4. **`GLOSSARIO.md`** · arquivo completo atualizado **apenas quando acumula mudanças significativas**. Gatilhos: 5+ termos novos · reformulação de tabela importante · 8+ warnings novos · novo padrão consolidado que merece entrada própria · termo descontinuado para o anti-glossário.
5. **`TabloFlow_Estado_do_Projeto.xlsx`** · arquivo completo atualizado **quando há mudança estrutural da planilha** (ex: reestruturação de abas · nova seção canônica · mudança de papel de aba). Em mudanças rotineiras de status · apenas instruções de edição (item 7).
6. **Prompt de abertura da próxima conversa** · texto inline (não é arquivo, é para colar), incluindo nome do próximo bloco e lista de anexos específicos necessários.

**Itens instruídos pelo Arquiteto, aplicados pela Usuária diretamente:**

7. **`DECISIONS.md`** · Arquiteto entrega as **entradas D-XXX em texto pronto para colar no topo** (após o cabeçalho, em ordem cronológica reversa) + lista de quais entradas antigas precisam ter status alterado e como.
8. **Planilha (`TabloFlow_Estado_do_Projeto.xlsx`) · edições rotineiras** · Arquiteto entrega **instruções de edição claras**: aba, linha/célula, valor novo. Inclui sempre instrução para a célula "Próximo Passo Operacional" da aba 1 e para a aba 2 (Painel da fase ativa · quadrados da Fase 2 · totalizadores) quando aplicável.

**Ordem de aplicação:**

1. Baixar arquivos da categoria 1 (CONTEXT, Instruções, artefato da sessão, eventualmente GLOSSARIO ou planilha estrutural)
2. Substituir esses arquivos no painel do Projects de uma vez
3. Aplicar manualmente as entradas D-XXX em DECISIONS.md no painel
4. Aplicar manualmente as instruções de edição na planilha (quando não houver arquivo completo substituindo)
5. Abrir próxima conversa colando o prompt do item 6

**Condição operacional:** para o Arquiteto produzir os arquivos canônicos completos, as últimas versões aprovadas precisam estar no painel do Projects no início da sessão. Se faltar alguma, o Arquiteto pede antes do ritual de abertura prosseguir.

**Sinalização de densidade durante o refino (D-034):** no 3º mini status-check de uma sessão de DCV (após ~9 pendências fechadas), o Arquiteto inclui estimativa do orçamento de kit ("alto/médio/baixo") e recomendação ("continuar / fechar refino aqui e abrir sessão dedicada ao kit").

**Complementaridade com D-131:** o ritual de encerramento de sessões da Fase 1 e Fase 2 aplica os 5 princípios de §14 · em particular, o Painel da fase ativa (aba 2 da planilha) é atualizado em cada kit, e o prompt de abertura da próxima conversa inclui declaração do conteúdo decisional esperado (princípio 3 de D-131).

A Usuária pode acionar este ritual a qualquer momento dizendo **"fecha o bloco"** ou **"kit de encerramento"**.

O Arquiteto oferece o kit proativamente quando percebe que a conversa chegou a um ponto de fechamento.

### 11.1 · Padrão ALINHA · sessão dedicada ao fechar Marco (D-142)

Quando o fechamento não é de um bloco rotineiro mas de um **Marco** (fase inteira · subsistema de design · transição para modo operacional diferente), o kit de encerramento D-033 sozinho é insuficiente. O padrão **ALINHA** formaliza um tipo de sessão dedicada que envelopa o kit D-033 como seu último sub-bloco.

**Gatilho · 3 critérios cumulativos.** ALINHA é acionada quando: (a) encerra-se uma fase inteira ou subsistema de design · (b) a transição seguinte é para um modo operacional diferente (ex: Arquiteto → Claude Code · Fase 0 → Fase 1) · (c) acumulou-se ≥ 3 decisões ou artefatos pendentes de consolidação.

**Escopo canônico · 4 sub-blocos sequenciais nomeados α · β · γ · δ:**

- **α · Consolidação retrospectiva** — unificação de artefatos produzidos em múltiplas sessões anteriores em artefato único coerente · eliminação de referências estruturais residuais · validação cross-cuts
- **β · Talk-through operacional** — transferência estruturada de contexto para o modo operacional seguinte · protocolo · pré-requisitos técnicos · situações de exceção · canal de retaguarda · entregáveis concretos (prompts prontos · arranjos de sessões paralelas)
- **γ · Formalização de decisões técnicas latentes** — identificação e consolidação de decisões que ficaram implícitas nas sessões anteriores do Marco · produção de entradas D-XXX com rationale completo
- **δ · Kit de encerramento D-033** — aplicação integral do padrão D-033 com atualização de todos os documentos canônicos em estado consolidado pós-Marco · prompt de abertura da próxima sessão tipicamente **dual** (d1 · prompt para modo operacional seguinte · d2 · prompt para sessão de retrospectiva do Arquiteto quando o modo seguinte concluir)

**Ordem dos sub-blocos:** α primeiro · δ último · β e γ intercambiáveis entre si. Mini status-check entre sub-blocos recomendado mas não obrigatório.

**Conteúdo decisional típico** (princípio 3 de D-131): 0 decisões de negócio · 1-3 decisões técnicas puras (formalizações de γ · casos reais excederam a estimativa · ALINHA-Fase-1→Fase-2 produziu 4: D-147/D-148/D-149/D-150) · 0 execuções de código (validação fica para a retrospectiva pós-modo-seguinte).

**Nomeação canônica:** "ALINHA-\<Marco fechado\>→\<próximo modo\>" · ex: `ALINHA-Fase-0→Fase-1` · `ALINHA-Fundação-Design→F-MOT` · `ALINHA-Fase-1→Fase-2`.

**Aplicações históricas:**
- **1ª aplicação · Sessão Fase 0 → Fase 1** · retroativamente categorizada como `ALINHA-Fase-0→Fase-1` · produziu D-130 (receptividade IA) · D-131 (condução Fase 1) · D-132 (dashboard visual)
- **2ª aplicação · `ALINHA-Fundação-Design→F-MOT`** (21/04/2026) · produziu consolidação de `spec_fundacao.md` em arquivo único · talk-through operacional do Claude Code · formalizou D-142 (este próprio padrão) · kit de encerramento D-033 como sub-bloco δ
- **3ª aplicação · `ALINHA-Fase-1→Fase-2`** (21/04/2026) · produziu §15 novo (condução da Fase 2) · reestruturação da planilha em 5 abas com papéis explícitos · D-147/D-148/D-149/D-150 · frente nova "Validação de Produto" parqueada

**Marcos futuros identificados:**
- Fechamento da Família A em Fase 2 (após validação visual de V2 · V1 · V11) → `ALINHA-Família-A→IA-Família-A`
- Fechamento da Fase 2 inteira (após 11 visões validadas) → `ALINHA-Fase-2→IA-Meta` ou `ALINHA-M1→M2` conforme roadmap
- Fechamento do Módulo 1 inteiro → `ALINHA-M1→M2`

**Complementaridade com D-033:** ALINHA não substitui D-033 · envelopa-o como sub-bloco δ. Toda sessão ALINHA termina com kit D-033 completo.

---

## 12. Como usar o Arquiteto

- **Validar DCV prévio** — encaminhe o DCV produzido com ChatGPT; retorno é o DCV final refinado, com pendências P-NN enumeradas (Fase 0 · DCVs OPN do M2).
- **Executar G-FUND** — concluído na Fase 1.
- **Gerar spec de visão** — peça "spec da V[N]"; retorno é Spec no padrão TabloFlow aplicando §13 + §15 + consumindo `spec_fundacao.md` e DCV aprovado.
- **Gerar base específica** — peça "base da V[N]"; retorno é o `.xlsx` com gabarito auditado **quando o critério de D-147 indicar B-VN necessário**. Quando default (base mestre suficiente), gera `base_vN_cliente.xlsx` como recorte cliente-friendly (D-149).
- **Gerar prompt de bloco** — peça "prompt do bloco [tipo-N]"; retorno é texto pronto para Claude Code.
- **Fechar pendência** — peça "decisão sobre P[NN]"; retorno são opções com trade-offs, Usuária escolhe.
- **Fechar conversa** — peça "fecha o bloco" ou "kit de encerramento"; retorno é o kit de encerramento completo.
- **Validar estado** — peça "valide o estado"; retorno é diagnóstico de coerência entre fontes + próximo passo confirmado.
- **Reestruturar planilha** — peça "nova análise da planilha" quando mudança de fase exigir reorganização das 5 abas.

---

## 13. Padrões estruturais de produto entre visões

Seis elementos são característica do produto TabloFlow e, portanto, **obrigatórios em toda visão** do Módulo 1. São definidos aqui em nível neutro — descrevem o que o produto oferece, não como aparece na tela. A execução visual concreta é responsabilidade da Spec (Fase 2) e da identidade visual (Frente A).

**13.1 — Objetivo da Visão**

Toda visão oferece ao usuário um bloco de ajuda contextual que explica, em linguagem de negócio: o que a visão faz · quando usar (casos práticos) · o que o usuário vai obter ao processar · como funciona (visão geral do fluxo). Esse bloco fica acessível desde a primeira tela da visão. A forma (botão no header, painel lateral, modal, tooltip) é decidida na Spec.

**13.2 — Fluxo de etapas progressivas**

Toda visão estrutura a configuração em **etapas sequenciais com dependência**. Regras:
- Etapa N só fica disponível quando etapa N-1 está concluída
- Usuário pode voltar para editar etapa anterior a qualquer momento
- Ao editar etapa anterior, o sistema avisa o impacto nas etapas seguintes (que podem ser invalidadas ou precisar de nova confirmação)
- Etapas concluídas mostram resumo compacto do que foi configurado

**13.3 — Modelo de configuração (salvar e aplicar)**

Toda visão permite ao usuário **Salvar** a configuração como modelo reutilizável e **Aplicar** modelo salvo. O modelo persiste configuração de **etapas lógicas** (agrupadores, campos, regras, thresholds editáveis · padrão TED C.D2). Não persiste dado fonte. Implementado via transversal **T-MODELO**.

**13.4 — View especializada entre visões da mesma família**

Quando duas visões da mesma família são conceitualmente próximas — uma delas é caso particular ou especialização da outra — adotamos o padrão **view especializada sobre visão-base**: a visão mais ampla implementa a lógica canônica, e a visão especializada consome a mesma lógica com preset de parâmetros, filtros implícitos e visualização/microcopy dedicados.

**Precedentes:**
- **Família A** — V2 é caso base; V1 é extensão via T-DUAL. V11 **não** é view especializada de V1.
- **Família C** — V4 é caso base (3 modos); V10 é view especializada sobre V4 Modo 2 com preset Pareto 80/95 (D-035).

**Modelos (T-MODELO) em view especializada** (D-046): mutuamente aplicáveis via mapeamento declarado com diálogo de confirmação quando cross-visão · aplicabilidade atual: V4 Modo 2 ↔ V10.

**13.5 — Resumo Executivo em 6 Blocos** (D-125 · formalizado em 20/04/2026)

Toda visão oferece um Resumo Executivo como **primeira aba da exportação Excel**, estruturado em 6 blocos fixos:

1. **Cabeçalho** — metadados da execução
2. **Números-âncora** — contagens e totais estruturais
3. **Distribuição** — como o conteúdo se distribui pela taxonomia
4. **Elementos destacados** — top N por critério declarado
5. **Leitura qualitativa com síntese** — N leituras + 1 default · TED
6. **Qualidade estrutural** — warnings, ajustes, integridade (BAD)

Adaptações via D-073 permitidas preservando a espinha de 6 blocos.

**13.6 — Coração Visual da Visão** (D-126 · formalizado em 20/04/2026)

Toda visão declara uma aba da exportação Excel como **Coração Visual** — a aba que materializa visualmente a contribuição analítica primária da visão. Aba obrigatória, nomeada conforme a identidade da visão.

*Corações Visuais declarados:* V4 Composição Principal · V7 Mapa de Grupos · V8 Matriz de Presença · V9 Mapa de Perfil · V5 Mapa de Distribuição · V10 Curva Pareto · V6 Matriz de Cruzamento.

*Retroação diferida:* V1, V2 e V11 ganham declaração formal de Coração Visual nas Specs S-V2, S-V1, S-V11 (candidatos naturais: **Matriz de Confronto** V2 · **Mapa de Conciliação** V1 · **Mapa de Aderência** V11).

---

## 14. Condução da Fase 1 · Didática técnico-decisional (D-131)

Padrão formalizado em 20/04/2026 · aplicado em 9 sessões consecutivas na Fase 1 · considerado **maduro após estabilização**. **Vigora integralmente na Fase 2 sem modificações estruturais** (10ª aplicação em ALINHA-Fase-1→Fase-2). Complementar aos padrões D-019 + D-034 + D-033 + D-142.

### 5 princípios operacionais

**Princípio 1 · Tradução obrigatória técnico → decisional** — decisões técnicas com impacto de negócio traduzidas antes de apresentar à Usuária. Decisões técnicas puras resolvidas pelo Arquiteto sem consulta.

**Princípio 2 · Acompanhamento visual primário · técnico secundário** — planilha aba 1 materializa macro (Horizontes Futuros · D-150) · aba 2 materializa fase ativa (Dashboard da Fase 2 · 5 quadrados por visão) · aba 3 materializa detalhe técnico.

**Princípio 3 · Sinalização proativa de densidade técnica** — toda sessão abre com declaração em 3 categorias originais (X negócio · Y técnicas puras · Z execuções de código) **+ 4ª categoria adicionada por D-156** (W validação de produto · acionada em VV-VN quando Usuária opera o app e decide ✅/❌ nos itens do checklist). Nem toda sessão tem as 4 categorias · declaração continua contextual.

**Princípio 4 · Validação visual como único mecanismo de aprovação da Usuária** — Fase 2 · Usuária carrega `base_vN_cliente.xlsx` no app e marca checklist derivado do YAML via D-148. **Usuária não lê código em nenhuma sessão.**

**Princípio 5 · Transparência mútua sobre calibração** — padrão considerado **maduro após 9 aplicações consecutivas** (G-FUND 1/2/3 · retrospectivas F-MOT/F-TRANS/F-EXP/F-BASE · produções de prompt F-EXP/F-BASE). Vigora na Fase 2 sem modificação. Lições consolidadas preservadas nas entradas D-131 de DECISIONS.md.

### Momentos técnicos da Fase 1 · todos RESOLVIDOS

**M1 · G-FUND · posicionamento T-CONCAT e M2.STACK** ✅ **D-135**  
**M2 · G-FUND · divisão ou não de F-EXP** ✅ **D-136** (bloco único validado empiricamente em F-EXP)  
**M3 · F-MOT · camada tipo_estrutural** ✅ **resolvido em G-FUND parte 1 como decisão técnica pura · D-133**  
**M4 · Fase 2 · Validação Visual** · aprovação de produto via checklist derivado · **mecanismo formalizado em D-148**

### Complementaridade com outros padrões

D-131 **complementa** D-019 + D-034 + D-033 + D-142 · não substitui. D-142 (padrão ALINHA) ativa-se adicionalmente em fechamentos de Marco · envelopando D-033 como sub-bloco δ · os 5 princípios de D-131 continuam vigentes dentro de cada sub-bloco α·β·γ·δ de ALINHA.

---

## 15. Condução da Fase 2 · Ciclo de 5 artefatos por visão (formalizado em 21/04/2026)

Seção formalizada em ALINHA-Fase-1→Fase-2 (3ª aplicação do padrão D-142). Consolida o processo operacional completo da Fase 2 incorporando as 4 decisões da sessão (D-147/D-148/D-149/D-150). Complementar a §3 (que declara os 5 artefatos em alto nível) e §14 (que declara a didática técnico-decisional). Padrão D-131 vigora integralmente.

**Nota de revisão:** D-147/D-148/D-149 **vigoram a partir de S-V2 como primeira aplicação · teste operacional · ajustes pós-V2 tratados como refinamento, não revogação**. D-150 vigorou imediatamente (já aplicado na reestruturação da planilha no kit da ALINHA).

### 15.1 · Ciclo canônico por visão · 5 artefatos sequenciais

Para cada visão N da Fase 2, sessão sequencial em ordem fixa (princípio B.1 · um bloco por sessão · zero paralelismo entre visões):

```
S-VN (Spec + wireframe textual + wireframe HTML [Família A] + checklist derivado)
  ↓
B-VN (condicional · critério D-147 · default = dispensado · consome base_fundacao.xlsx)
  ↓
V-VN (visao_vN.py · executado em Claude Code · prompt pelo Arquiteto · retrospectiva)
  ↓
A-VN (app_vN.py · executado em Claude Code · prompt pelo Arquiteto · retrospectiva)
  ↓
Validação Visual (Usuária carrega base_vN_cliente.xlsx · marca checklist ✅/❌)
```

**Dependências duras:** S-VN aprovado antes de B-VN. B-VN (ou confirmação de consumo da base mestre) antes de V-VN. V-VN testado verde antes de A-VN. A-VN rodando antes de Validação Visual.

**Quem faz o quê:**

| Bloco | Executor | Aprovação | Participação da Usuária |
|---|---|---|---|
| S-VN | Arquiteto | Usuária (dupla aprovação contrato + wireframe · B.2 reforçado por HTML em Família A) | Sessão completa · revisa wireframe HTML · aprova checklist |
| B-VN | Arquiteto (raro · só se D-147 exigir) | Usuária (auto-validação contra casos_esperados) | Sessão curta · confirma cobertura |
| V-VN | Claude Code (prompt pelo Arquiteto em sessão combinada · D-155) | Arquiteto valida testes verdes na retrospectiva | Usuária não lê código (princípio 4 D-131) |
| A-VN | Claude Code (prompt pelo Arquiteto em sessão combinada · D-155) | Arquiteto valida App roda na retrospectiva | Usuária não lê código · verá na VV-VN |
| **VV-VN** (Validação Visual acompanhada · D-156) | Usuária opera silenciosamente | Usuária · gate final B.4 · Arquiteto NÃO decide ✅/❌ | Sessão completa · modalidade C mista · 3 pontos-chave canônicos + gatilhos livres |

### 15.2 · Plano operacional · ~6 sessões por visão (Família A · pré-D-155) · ~4 sessões por visão (Família A · pós-D-155)

Estimativa original baseada na análise de β da sessão ALINHA-Fase-1→Fase-2 (β.5.2) · **revisada em 23/04/2026 após D-155** consolidar V-VN e A-VN em sessões combinadas:

| Bloco | Sessões (pré-D-155) | Sessões (pós-D-155 · canônico) | Natureza |
|---|---|---|---|
| S-VN | 1-2 sessões | 1-2 sessões | Produção da Spec · dupla aprovação |
| B-VN | 0 sessões (Família A) · 1 sessão (se D-147 exigir) | idem | Condicional |
| V-VN | 2 sessões (1 prompt · 1 retrospectiva) | **1 sessão combinada** (D-155) | Claude Code + retrospectiva no mesmo bloco Arquiteto |
| A-VN | 2 sessões (1 prompt · 1 retrospectiva) | **1 sessão combinada** (D-155) | Claude Code + retrospectiva no mesmo bloco Arquiteto |
| VV-VN (D-156) | 1 sessão solo | **1 sessão acompanhada modalidade C** | Usuária opera · Arquiteto presente em chat · 3 pontos-chave |

**Total por visão Família A (canônico pós-D-155):** ~4 sessões Arquiteto + 1 sessão VV-VN ≈ **~5 sessões operacionais**.
**Família A inteira (V2 → V1 → V11):** ~15 sessões sequenciais (revisão da estimativa original de 18).
**V2 consumiu:** 2 S-V2 + 1 V-V2 combinada + 1 A-V2 combinada + 1 VV-V2 (a executar) = **5 sessões** · confirma estimativa.

### 15.3 · Convenções de Spec de visão (S-VN)

**Estrutura canônica · 3 seções obrigatórias (B.2) + §13 + §9 Camada C:**

**Seção 1 · Contratos lógicos Pydantic**
- Declaração de `V{N}Result` estendendo `VNResultBase` com estrutura específica da visão
- Requisitos D-130 integrais (analítico): `model_config` para enums como string · `Field(..., description=...)` em todo campo · método `.para_contexto_ia()` implementado
- Contratos auxiliares específicos da visão
- Referência (sem redeclaração) a contratos consumidos da Fundação

**Seção 2 · Regras de cálculo**
- Pipeline determinístico (C.1)
- Consumo de transversais com parâmetros declarados (ver §6)
- Bloqueios operacionais B-VN-* (MBO · C.D4) com 5 campos declarados (condição · comportamento · escapável · microcopy · warning)
- Catálogo de warnings W-VN-*
- Thresholds editáveis declarados (TED · C.D2)
- Consolidação pré-cálculo declarada explicitamente (CPCO · C.D1 · modo da base)

**Seção 3 · Wireframe funcional**
- Descrição textual do fluxo em etapas progressivas (§13.2)
- Estados da tela (vazio · configuração · processamento · resultado · erro)
- Microanálise progressiva
- Estrutura da exportação Excel (lista ordenada de abas · Coração Visual nomeado · §13.5/§13.6)
- **Seção §3.x · Checklist de Validação Visual** derivado de `casos_esperados.yaml` (D-148)
- **Aprovação explícita da Usuária antes do código iniciar** (B.2 · reforçado em Família A por wireframe visual HTML · D-149)

**Checklist §13 · 6 padrões verificados em cada Spec:**
- 13.1 Objetivo da Visão · bloco de ajuda contextual
- 13.2 Fluxo progressivo · N etapas com dependência
- 13.3 T-MODELO · o que persiste / não persiste
- 13.4 View especializada · declaração se aplicável
- 13.5 Resumo Executivo 6 Blocos · blocos preenchidos com conteúdo V-específico
- 13.6 Coração Visual · nome da aba · formato · capability consumida

**Checklist §9 Camada C · 5 derivados verificados:**
- CPCO · modo da base + T-AGRUPA (ou adaptação D-073)
- TED · lista de thresholds editáveis com defaults
- BAD · Base Analítica + Diagnóstico última · sem aba "Dados Brutos"
- MBO · catálogo B-VN-* numerado
- ECP · escala de cardinalidade em patamares V-específica

### 15.4 · Critério de base consumida (D-147)

Cada Spec S-VN declara explicitamente qual base a visão consome aplicando o critério de 3 perguntas:

**Pergunta 1 · Cobertura de cenários** — as assertions de `casos_esperados.yaml` do bloco `visoes:V{N}` cobrem os casos-limite do DCV-VN?

**Pergunta 2 · Volume para Validação Visual** — o volume das abas consumidas é confortável para inspeção humana (≥50 linhas · B.3)?

**Pergunta 3 · Independência de evolução** — a Fase 2 pode precisar modificar a base dessa visão no futuro sem afetar `base_fundacao.xlsx`?

**Default declarado:** todas as 3 respostas = "base mestre suficiente" → B-VN dispensado · Spec declara "Base consumida: `base_fundacao.xlsx` · abas: {lista}". Qualquer exceção → B-VN é bloco dedicado · produz `base_vN.xlsx` em `/bases/`.

**Aplicação Família A:** V2 · V1 · V11 → B-VN dispensado (cobertura + volume + estabilidade OK) · consomem `base_fundacao.xlsx` diretamente. Análise preliminar em β.3.2 da ALINHA · confirmada em cada S-VN.

### 15.5 · Recorte cliente-friendly (D-149)

**Independente de ter B-VN ou não**, cada visão ganha `/bases/base_vN_cliente.xlsx` contendo apenas as abas consumidas · simula upload de cliente real · zero divergência de conteúdo (reempacotamento mecânico da `base_fundacao.xlsx` ou do `base_vN.xlsx` quando B-VN existir).

Gerado por `/src/geradores/gerar_base_cliente.py` em sub-tarefa do bloco S-VN (quando base mestre suficiente) ou como sub-tarefa de B-VN.

`base_vN_cliente.xlsx` é o **arquivo canônico de entrada da Validação Visual** · carregado pela Usuária no `app_vN.py`.

### 15.6 · Wireframe visual HTML (D-149 · obrigatório Família A)

Cada Spec S-VN da Família A acompanha `/specs/wireframe_vN.html` · HTML estático mínimo · renderiza tela por etapa · botões nomeados · microcopy visível · transições anotadas.

**Neutro em identidade visual** (Frente A parqueada · D-015 Camada B). Foco em fluxo + estrutura de tela · não estética.

**Aprovação da Usuária simultânea** à aprovação da Spec textual. Dupla aprovação B.2 preservada e reforçada.

**Obsolescência cosmética tolerada** — quando Frente A ativar, wireframe HTML fica cosmeticamente defasado mas fluxo funcional permanece válido. Não requer regeneração.

**Opcional a partir de S-V3** · avaliado caso a caso se HTML agrega valor real. Default declarado pós-Família A é mantido HTML para visões de fluxo novo ou visualmente complexo · dispensável para visões cuja Spec textual já é suficientemente clara.

### 15.7 · Checklist de Validação Visual derivado mecanicamente (D-148)

Cada Spec S-VN contém na seção §3.x o **checklist derivado das assertions de `casos_esperados.yaml` bloco `visoes:V{N}`** via 5 templates canônicos:

| Tipo de assertion | Template de pergunta canônica |
|---|---|
| `contagem_exata` | "O resultado mostra exatamente {esperado.valor} {entidade} em {coluna\|aba\|agrupador}?" |
| `contagem_categoria` | "O resultado mostra entre {esperado.min} e {esperado.max} {entidade} em {coluna\|aba}?" (variante pct) |
| `warning_presente` | "O warning `{warning_code}` aparece no Diagnóstico com {min}–{max} ocorrência(s)?" |
| `estrutura_saida` | "O Excel tem Resumo Executivo com {resumo_blocos} blocos e aba Coração Visual nomeada '{coracao_visual}'?" |
| `bloqueio_emitido` | "Ao rodar a visão, o BloqueioOperacional de código `{bloqueio_codigo}` foi emitido conforme esperado?" |

**Derivação 1:1** entre assertions e itens de checklist. Item não-coberto por assertion **não pode ser adicionado ad-hoc** · deve virar assertion nova no YAML + regenerar (integridade de D-141 ponto 3 preservada · C.2 nada silencioso reforçado).

**Duplo domicílio:** (a) seção §3.x da Spec S-VN (aprovação Usuária junto do wireframe) · (b) interface do `app_vN.py` como checkbox list visível antes da exportação Excel.

**Aprovação da Visão:** todos os itens ✅ · Validação Visual registrada na aba 2 da planilha (5º quadrado ✅). Qualquer ❌ dispara **diagnóstico imediato** pelo Arquiteto na mesma sessão VV-VN (D-156 · M4 de D-131 · bug de código · lacuna de Spec · interpretação divergente).

### 15.8 · Padrão VV-VN · Validação Visual acompanhada modalidade C mista (D-156 · formalizado em 23/04/2026)

Formalizado na retrospectiva A-V2 (2ª aplicação de sessão combinada · D-155). Substitui a formulação original de Validação Visual solo declarada em §15.1 (tabela reescrita acima). Preserva integralmente o gate B.4, o mecanismo de derivação do checklist (D-148), e o princípio 4 de D-131 (Usuária não lê código).

**Natureza:** sessão Arquiteto + Usuária em chat concomitante. Usuária opera o app ao vivo no terminal · Arquiteto presente como apoio · modalidade C mista (Usuária opera silenciosamente · aciona Arquiteto em pontos-chave + gatilhos livres).

**3 pontos-chave canônicos** (Usuária aciona explicitamente):

1. **Pós-processamento** (Tela 8 · Resultado) · Usuária mostra 4 KPIs + Resumo Executivo · Arquiteto comenta aderência à Spec · aponta algo estranho que possa ter passado despercebido
2. **Pré-checklist** (Tela 9 · antes de marcar itens) · Usuária mostra o que o app exibe · Arquiteto comenta sobre a leitura técnica **sem induzir resposta** (Arquiteto não decide ✅/❌ · gate B.4 inviolável)
3. **Pós-exportação** (Excel aberto) · Usuária relata estrutura · abas · Coração Visual · Arquiteto comenta sobre conformidade com §2.9 da Spec

**Gatilhos livres** (fora dos 3 pontos-chave):
- Travamento operacional · "como faço X"
- Observação que Usuária queira registrar · "achei estranho que..."
- Diagnóstico de ❌ · "esse item não bate porque..."

**4 tipos de intervenção do Arquiteto durante a sessão:**

| Tipo | Destino da sugestão |
|---|---|
| **Apoio operacional** | Nenhum · interação passageira |
| **Resolução de ❌** | Diagnóstico imediato · bug volta para Claude Code em sessão posterior · lacuna de Spec vira D-XXX · interpretação divergente ajusta microcopy do checklist ou da Spec |
| **Sugestão emergente** | Absorção silenciosa (registrar nota na sessão) · P-VN-Evo-NN (parqueada para V1/V11 herdarem) · D-XXX (se afeta contrato de forma relevante) |
| **Encerramento** | 4 ✅ → planilha aba 2 · 5º quadrado ✅ · OU Usuária decide parar → reabrir em nova VV-VN depois |

**Gate B.4 inviolável:** Arquiteto pode comentar observações técnicas em qualquer momento mas **NÃO decide ✅/❌** · autoridade de aprovação do produto é 100% da Usuária. Se Arquiteto tem dúvida sobre algo, formula como pergunta técnica · não como recomendação de marcação.

**Nova categoria no vocabulário de declaração de conteúdo decisional (§14 · princípio 3 · D-131):** `validação de produto` passa a ser a **4ª categoria** declarada pelo Arquiteto na abertura da sessão VV-VN · junta-se a (negócio · técnicas puras · execuções de código supervisionadas). Declaração típica VV-VN: "W decisões de negócio · X técnicas puras · 0 execuções de código · 1 validação de produto (Usuária decide 4 itens ✅/❌)".

**Nomeação canônica:** `VV-VN` · ex: `VV-V2` · `VV-V1` · `VV-V11`.

**Maturação:** padrão considerado maduro após VV-V2 · VV-V1 · VV-V11 (Família A completa · mesmo critério de D-131 com 9 aplicações consecutivas). Revisável se sessão VV-VN sistematicamente exceder 2h (indicando apoio excessivo · não Usuária operando de fato) ou se intervenção do Arquiteto virar rotineira a ponto de a modalidade C colapsar em tutoria passo-a-passo.

**Duração esperada:** ~1h para visão nova · ~40min para visões subsequentes da mesma família (herdam familiaridade de operação).

**Distinção de Validação de Produto (§15.10):** VV-VN valida **mecânica** com base sintética · Validação de Produto (horizonte parqueado · pós-Família A) valida **adequação** com bases reais de cliente. Não misturar.

### 15.9 · Retrospectivas pós-Claude Code

Permanecem como na Fase 1 (precedentes F-MOT/F-TRANS/F-EXP/F-BASE): sessão Arquiteto→Arquiteto curta · valida output contra Spec · absorve correções auto-contidas como execução da spec (C.3) · promove a D-XXX apenas quando emerge ambiguidade estrutural latente da Spec ou quando refina escopo de decisão estrutural anterior · kit D-033 isolado.

**Atualização D-155 · convenção Família A:** a retrospectiva de V-VN e A-VN acontece **no mesmo bloco Arquiteto** que produziu o prompt técnico · sessão combinada (produção de prompt → pausa para Claude Code executar no terminal da Usuária → retomada para retrospectiva e kit D-033). Aplicável desde V-V1 / A-V1. Revisável após Família A completa.

### 15.10 · Frente de Validação de Produto (parqueada · distinta de VV-VN)

Frente paralela formalizada em ALINHA-Fase-1→Fase-2 · **inicia após Família A validada** (V2 · V1 · V11 com VV-VN aprovada).

**Distinção crítica:**
- **VV-VN** (B.4 · §15.7 · §15.8 · D-156) · valida **mecânica** · base sintética · checklist derivado do YAML · gate de aprovação de visão · Fase 2
- **Validação de Produto com bases reais de cliente** (frente parqueada) · valida **adequação a cenário real** · base de cliente real · pode revelar gaps de produto / out-of-scope / evolução · decisões de negócio pesadas

Não misturar ambas na mesma sessão. Validação de Produto é horizonte 14 (Zona 2 · Produtização) na aba 1 da planilha (D-150).

### 15.11 · Convenções de acompanhamento operacional

**Aba 1 · Onde estou no todo** (D-150) · Usuária atualiza status dos 19 Horizontes Futuros manualmente (~10s por sessão). Horizonte "Família A validada" passa de ▶ Próximo para ✅ Concluído quando todas as 3 visões da Família A tiverem 5 quadrados ✅.

**Aba 2 · Painel da fase ativa** · Usuária atualiza 5 quadrados por visão a cada sessão concluída (~30s). Totalizadores de família e fase atualizados manualmente.

**Aba 3 · Detalhe técnico das visões** · consulta pontual · atualizada apenas quando Spec de uma visão estiver aprovada (ou quando alguma decisão de Fase 2 demandar).

**Planilha é reestruturada quando muda de fase** · ao início da Fase 3 (Módulo 2 ou IA-Meta), Usuária pode pedir "nova análise da planilha" e o Arquiteto repropõe reorganização das 5 abas mantendo a filosofia de papéis explícitos.

---

O Arquiteto não pede confirmação para o óbvio. Interrompe apenas quando há decisão com impacto estrutural.
