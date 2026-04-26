# DECISIONS.md — TabloFlow

Log central de decisões estruturais e de contrato do projeto. Ordem cronológica reversa (mais recente no topo).

---

## Quando registrar uma decisão aqui

Adicione uma entrada quando a decisão:
- Fecha uma pendência aberta em alguma spec
- Muda contrato, comportamento ou interface entre blocos
- Seria custosa de redescobrir depois ("por que escolhemos X em vez de Y?")
- Tem impacto em mais de uma visão ou em camadas transversais (motores, contratos, fluxo)

**NÃO registrar aqui:**
- Decisões puramente de implementação interna a um bloco (ficam no código/spec)
- Escolhas de nomenclatura local
- Decisões já consolidadas no `CONTEXT.md` (regras) ou na planilha (estado vivo)

A fonte de verdade canônica continua sendo a spec correspondente — este arquivo é o **histórico cronológico** dessas decisões, com a razão por trás delas.

---

## Formato de cada entrada

```
### D-XXX — Título curto da decisão
**Data:** AAAA-MM-DD · **Bloco:** B-N ou Bloco N · **Status:** Fechada / Provisória / Revogada
**Contexto:** Qual problema ou pendência originou a decisão.
**Decisão:** O que foi escolhido, em uma frase.
**Razão:** Por que essa opção e não as alternativas.
**Impacto:** O que muda na implementação · em que arquivos.
**Referência canônica:** Onde a decisão vive como contrato (spec, CONTEXT.md, etc.).
```

Numeração D-XXX é sequencial global do projeto (não reinicia por visão).

---

## Decisões registradas

# Entrada a inserir em DECISIONS.md — TOPO da seção "Decisões registradas"

*(Esta entrada substitui as posições anteriores no topo. D-001 a D-013 permanecem abaixo, intactos. Apenas copiar este bloco para o topo de "Decisões registradas" em DECISIONS.md.)*

---
### D-016 — Unidade de bloco de DCV = visão (não família)
**Data:** 2026-04-18 · **Bloco:** DCV-V1 (parcial) · **Status:** Fechada

**Contexto:** A aba "2. Fase 0 · DCVs" da planilha v2 (pós-D-014) havia proposto "unidade de bloco = família" como hipótese experimental — refinar DCV-V2 e DCV-V1 juntos em uma sessão, na ideia de que a mãe conceitual (V2) e a irmã (V1) da Família A compartilhariam vocabulário e caberiam em uma sessão. A Sessão 1 da Fase 0 iniciou aplicando essa hipótese, com V1 refinada primeiro (por ter pré-requisitos de motor_upload — modo dual — que convém antecipar).

Durante o refino do DCV-V1, a sessão produziu ganho metodológico significativo não previsto: promoção de padrões visuais/UX do Figma Make a diretrizes oficiais (D-015) e formalização do princípio C.5 (TabloFlow analisa, não decide). Isso consumiu ciclo de sessão que seria do refino puro, demonstrando empiricamente que uma sessão de DCV não cabe uma família inteira quando há emergência de decisão de método acontecendo em paralelo.

**Decisão:** Unidade de bloco de DCV = **uma visão**. A hipótese "unidade = família" é revogada antes da primeira sessão completar porque a evidência empírica mostrou inviabilidade. Refino de V2 e V1 exige duas sessões separadas. Aplica-se a todas as famílias conceituais do Módulo 1 — V4+V10 (Família C), V3+V8 (Família B), V7+V9 (Família D), V5+V6 (Família E) também serão refinadas em sessões individuais.

**Razão:** Três motivos convergiram:
1. **Densidade natural do DCV.** Cada DCV tem 8-15 pendências estruturais quando se aplica o padrão TabloFlow com rigor. Dobrar isso em uma sessão ultrapassa a janela de concentração da Usuária e de qualidade do Arquiteto.
2. **Emergência de decisão de método.** Conforme o Arquiteto refina o primeiro DCV, descobertas estruturais (como o reset conceitual de C.5) emergem e precisam ser registradas antes de propagar para o segundo DCV. Fazer os dois em paralelo aumenta risco de aplicar no segundo DCV uma lente que ainda não está estável.
3. **Alinhamento com princípio B.1.** O CONTEXT já diz "um bloco por sessão". "Bloco = família" forçaria exceção a B.1 que a prática mostrou ser desnecessária.

Alternativas consideradas:
- **Manter "unidade = família" e apenas reservar sessões mais longas** — rejeitada porque a Usuária sinalizou fadiga de decisão como risco real, e o Arquiteto também perde qualidade.
- **Unidade = família quando as visões são muito acopladas** — rejeitada por introduzir critério subjetivo que na prática ninguém aplicaria de forma consistente.

**Impacto:**
- CONTEXT v2 §3 (Fase 2) já diz "para cada visão N, cinco artefatos sequenciais". A Fase 0 passa a seguir a mesma lógica: para cada visão N, um bloco DCV-VN. A redação já está compatível — não precisa edição do CONTEXT.
- Planilha v2 aba "2. Fase 0 · DCVs": ajustar linha de próximo passo operacional para refletir "DCV-V1 (continuação) em sessão 2; DCV-V2 em sessão 3". O texto da sessão 1 que mencionava "refino conjunto" precisa ser atualizado para "refino individual por visão, testando família A como piloto — família mostrou não caber em uma sessão".
- Ordem de refino dentro da Família A: V1 primeiro, V2 depois. Ordem baseada em racional da Usuária: V1 antecipa requisitos de motor_upload (modo dual) que entrarão no G-FUND. Ordem de **implementação** na Fase 2 permanece V2→V1 conforme CONTEXT §3 (racional: V2 é mais simples no código, V1 herda vocabulário). Ordem de compreensão ≠ ordem de implementação — registrado também como nuance.
- Famílias seguintes (C, B, D, E) serão refinadas com mesma lógica: uma sessão por DCV.

**Referência canônica:** CONTEXT v2 §3 (Fase 0) · planilha v2 aba "2. Fase 0 · DCVs"
### D-018 — T-DUAL: novo transversal (motor_upload em modo dual)
**Data:** 2026-04-18 · **Bloco:** DCV-V1 (Sessão 1) · **Status:** Fechada

**Contexto:** O DCV-V1 é o primeiro e único do Módulo 1 a exigir que o `motor_upload` aceite dois arquivos simultâneos OU um arquivo com pareamento de duas abas. As outras 9 visões operam sobre uma única base consolidada. Essa necessidade emergiu ao fechar P-V1-01 (fontes de entrada da V1) na Sessão 1 da Fase 0.

**Decisão:** Criar novo transversal **T-DUAL** na Fundação — extensão do `motor_upload` que aceita duas estruturas de entrada:
- Estrutura A: dois arquivos distintos; usuário escolhe uma aba de cada
- Estrutura B: um único arquivo; usuário escolhe duas abas
Ambas produzem um `UploadResult` com referência aos dois lados nomeados (Origem/Comparado ou rótulos editados).

**Razão:** A V1 precisa do modo dual; nenhuma outra visão precisa. Implementar como extensão do `motor_upload` (em vez de motor separado) reaproveita toda a infraestrutura de leitura, detecção de abas, inferência de tipos e diagnóstico. A única lógica nova é o **pareamento** de Origem/Comparado — que é pequena e localizada.

**Impacto:**
- **CONTEXT.md §6** — tabela de transversais ganha linha T-DUAL, marcada como "Usado por: V1" (único usuário).
- **Bloco G-FUND** — escopo do `motor_upload` v2 incorpora T-DUAL como contrato obrigatório.
- **Bloco F-MOT** — implementação contempla T-DUAL junto com a reescrita do `motor_upload`.
- **GLOSSARIO.md** — nova entrada para T-DUAL na seção de transversais.

**Fora de escopo da V1/T-DUAL:** estrutura de dados empilhados em uma única aba com coluna discriminadora. Este cenário exige RESHAPE prévio no Módulo 2 e não é suportado pela V1.

**Referência canônica:** `CONTEXT.md` §6 (T-DUAL) · DCV-V1 §3.1 · escopo do F-MOT

---

### D-019 — Padrão de condução do Arquiteto formalizado pela Sessão 2
**Data:** 2026-04-18 · **Bloco:** DCV-V1 (Sessão 2) · **Status:** Fechada

**Contexto:** Ao fim da Sessão 2 da Fase 0, a Usuária observou explicitamente que o padrão de condução do Arquiteto durante o refino da V1 era o comportamento esperado em todas as sessões futuras de DCV. O padrão não estava registrado formalmente; a Sessão 2 materializou-o na prática. Esta decisão formaliza o padrão para que sessões subsequentes (DCV-V2, DCV-V4, DCV-V10, DCV-V3, DCV-V8, DCV-V7, DCV-V9, DCV-V5, DCV-V6, e DCVs de operações do Módulo 2) adotem o mesmo ritmo e qualidade.

**Decisão:** Registrar como padrão de condução do Arquiteto em sessões de DCV-VN os seguintes elementos, validados pela Usuária na Sessão 2:

1. **Validação de estado explícita na abertura** — ler os 4 documentos canônicos + DCV prévio + eventuais parciais; reportar diagnóstico de coerência entre fontes; confirmar próximo passo operacional antes de agir.

2. **Fila racionalizada de pendências** — propor ordem de tratamento com racional (quais primeiro, por quê), não tratar pendências em ordem alfabética ou numérica.

3. **Uma pendência por vez, com opções explícitas** — cada pendência apresentada com (a) problema contextualizado, (b) aplicação do Princípio C.5, (c) 2 a 4 opções nomeadas, (d) trade-offs de cada uma, (e) recomendação com razões, (f) comportamento definido concreto (tabelas, regras, exemplos).

4. **Aplicação sistemática do Princípio C.5** como primeira lente de cada pendência — "o sistema está decidindo por alguém? apenas apresentando achado? pedindo ao usuário decisão natural do problema ou arbitrária?". Revelou-se decisiva em P-V1-05, P-V1-06, P-V1-09, P-V1-10 e na revisão de P-V1-02.

5. **Confirmação da Usuária antes de avançar** — cada pendência fecha com pergunta explícita ("concorda?", "prefere diferente?") e próxima pendência só inicia após confirmação.

6. **Mini status-check a cada 3 pendências fechadas** — resumo curto do que foi decidido, coerência entre as decisões, fila restante, próximas pendências propostas.

7. **Abertura para correção de enquadramento pela Usuária** — quando a Usuária apontar que a lente do Arquiteto está errada (caso P-V1-02 revisada, caso Diagnóstico como última aba), o Arquiteto **reformula a pergunta, confirma entendimento e ajusta as decisões afetadas em cadeia**, sem defensividade.

8. **Proativa identificação de decisões transversais** — quando uma pendência da visão revela padrão que se aplica a outras visões, o Arquiteto explicita e propõe a decisão como transversal (D-XXX), não limitada ao DCV em questão.

9. **Identificação do momento de fechamento** — ao perceber que todas as pendências estruturais estão fechadas, o Arquiteto oferece o kit de encerramento proativamente, não espera pedido.

10. **Produção do DCV final em prosa como último ato da sessão** quando há tempo — ou como entregável da próxima sessão quando não há. Decisão dialogada com a Usuária, não assumida.

**Razão:** A Usuária sinalizou explicitamente que este é o padrão esperado ("gerar esse padrão de comportamento esperado que vc teve quanto a condução — É assim que vejo que evoluímos"). Formalizar o padrão:
- **Calibra expectativas** para sessões futuras de DCV.
- **Reduz variância** entre sessões diferentes do mesmo Arquiteto em conversas distintas (cada conversa é "novo Arquiteto" sem memória da anterior — o padrão escrito é a memória compartilhada).
- **Serve como critério de autoavaliação** do Arquiteto — "estou conduzindo conforme D-019?".
- **Serve como critério da Usuária** para reclamar quando condução foge do padrão.

**Impacto:**
- **Instruções do Projeto** — ganham seção "Padrão de condução em sessões de DCV" referenciando D-019 (ver Item 3 deste kit).
- **CONTEXT.md** — não altera (D-019 é padrão de condução do Arquiteto, não regra permanente de método).
- **GLOSSARIO.md** — nova entrada para "Padrão de condução DCV (D-019)" na seção de convenções de comunicação.

**Nota:** este padrão aplica-se especificamente a **sessões de refino de DCV** (bloco DCV-VN e DCV-OPN). Para outros tipos de bloco (G-FUND, F-*, S-VN, B-VN, V-VN, A-VN), padrões de condução próprios emergirão em suas primeiras execuções e serão formalizados de forma análoga.

**Referência canônica:** Instruções do Projeto §Padrão de condução em sessões de DCV

### D-017 — Diagnóstico sempre como última aba em todas as visões
**Data:** 2026-04-18 · **Bloco:** DCV-V1 (Sessão 2) · **Status:** Fechada

**Contexto:** Durante o refino de L-V1-B (forma da aba de Diagnóstico) na Sessão 2 da Fase 0, o Arquiteto propôs inicialmente que o Diagnóstico da V1 ficasse em **posição 2** do Excel (logo após o Resumo Executivo), com racional de "auditor precisa validar confiabilidade antes de consumir resultado". A Usuária corrigiu o enquadramento: a decisão de posição do Diagnóstico é **transversal a todas as 10 visões**, não específica da V1. O raciocínio de que o usuário consome resultado primeiro e valida processo depois se aplica a qualquer análise do TabloFlow, não só à conciliação.

**Decisão:** O **Diagnóstico é sempre a última aba do Excel exportado**, em todas as 10 visões do Módulo 1 e nas operações do Módulo 2 quando aplicável. Regra transversal aplicada pelo **transversal T-DIAG** (CONTEXT §6) e formalizada como requisito do **bloco F-EXP** (exportação Excel padrão) da Fase 1 · Fundação.

**Razão:** O Diagnóstico cumpre função de auditoria e validação do processamento — é artefato de "caixa-preta aberta" para o usuário que precisa investigar. O fluxo natural de leitura em qualquer análise é: resultado primeiro (para entender o quê), validação depois (para confirmar o como). Colocar Diagnóstico em posição inicial induz leitura invertida que raramente é a desejada, inclusive em auditoria — o auditor ainda prefere ver os números e só abrir o Diagnóstico quando encontra algo a investigar.

Alternativa considerada e descartada:
- **Diagnóstico em posição 2 para auditoria e posição final para outras visões** — rejeitada por inconsistência: usuária que alterna entre visões do TabloFlow aprende padrão de navegação, e padrão inconsistente aumenta atrito cognitivo. Regra única simplifica.

**Impacto:**
- **CONTEXT.md §6** — linha do T-DIAG ganha cláusula adicional: "Aba sempre posicionada no final da estrutura de exportação Excel."
- **Bloco F-EXP da Fase 1** — requisito formalizado na definição da exportação Excel padrão.
- **DCV-V1 §6.1** — estrutura de abas do Excel da V1 reflete Diagnóstico como aba 5 (sem agrupador do Resumo) ou aba 6 (com agrupador do Resumo).
- **GLOSSARIO.md** — entrada de T-DIAG atualizada para refletir posição final obrigatória.
- **Próximos DCVs (V2, V3, V4, V5, V6, V7, V8, V9, V10)** — devem respeitar este padrão sem necessidade de redecisão.
- **Operações do Módulo 2** — regra aplica-se quando produzirem Excel com diagnóstico.

**Referência canônica:** `CONTEXT.md` §6 (T-DIAG) · `DCV-V1` §6.1 e §10.1 · escopo do bloco F-EXP no G-FUND

---

### D-015 — Padrões visuais/UX do Figma Make: Camada A (método) × Camada B (sugestão)
**Data:** 2026-04-18 · **Bloco:** DCV-V1 (parcial) · **Status:** Fechada

**Contexto:** Durante a Sessão 1 da Fase 0, a Usuária compartilhou o arquivo `DCV_PREVIO_M1_V1_FIGMA.md`, consolidando dois documentos internos do wireframe navegável da V1 produzido no Figma Make: `PADRAO_IA_TABLOFLOW.md` (padrão visual/funcional das sugestões de IA) e `TEMPLATE_PROMPT_VISOES.md` (template para gerar wireframes das outras visões mantendo consistência). Esses arquivos descrevem elementos que o Arquiteto inicialmente interpretou como "diretrizes oficiais": botão "Objetivo da Visão" com 4 seções expansíveis, stepper progress, accordion progressivo, sistema de Modelos Salvos, sistema de Sugestões de IA com padrão visual roxo-azul, paleta de cores semântica (verde/laranja/azul/vermelho/slate).

O Arquiteto propôs inicialmente promover todos esses elementos a diretrizes vinculantes no CONTEXT, o que teria antecipado Fase 3 (IA) e Frente A (Identidade Visual) — ambas parqueadas — e expandido significativamente o escopo da Fundação.

A Usuária corrigiu o enquadramento, distinguindo: existem **padrões estruturais do produto** (coisas que todas as 10 visões vão oferecer por serem características do TabloFlow) e **sugestões visuais** (cores, gradientes, componentes shadcn, copywriting específico — que são propostas a avaliar quando Fase 3 e Frente A forem executadas).

**Decisão:** Separação formal em duas camadas:

**Camada A — Padrões estruturais de produto (entram no método TabloFlow):**

Três elementos são promovidos a característica obrigatória de toda visão do Módulo 1:
1. **"Objetivo da Visão"** — bloco de ajuda contextual em cada visão, explicando ao usuário o que a visão faz, quando usar, o que vai obter e como funciona. É parte do produto.
2. **Fluxo de etapas progressivas** — cada visão tem sequência de etapas com dependência (etapa N só abre quando N-1 fecha), e permite voltar para editar etapa anterior com aviso de impacto nas seguintes.
3. **Salvar modelo de configuração** — toda visão permite ao usuário salvar a configuração aplicada como modelo reutilizável, e aplicar modelo salvo em novo uso.

Registrados no CONTEXT v2 como novo §13 "Padrões estruturais de produto entre visões" (redação completa no Item 2 do kit). Registro é **neutro em tecnologia, linguagem visual e componente** — descreve o que o produto oferece, não como aparece na tela.

Novo transversal adicionado ao escopo do G-FUND: **T-MODELO** (contrato de salvar/aplicar modelo de configuração). Os demais elementos são comportamento de UI e ficam na Spec de cada visão (Fase 2).

**Camada B — Sugestões visuais (ficam como referência, não vinculam):**

Os seguintes elementos do Figma Make ficam registrados como **referência navegável autorizada do wireframe V1**, sem vincular o método:
- Paleta de cores específica (roxo-azul IA, verde sucesso, laranja atenção, azul info, vermelho erro, slate neutro)
- Componentes shadcn escolhidos
- Copywriting específico
- Gradientes, ícones Sparkles
- Stepper horizontal com check verde
- Layout de cards brancos com bordas coloridas

Esses ficam no wireframe referenciado no DCV-V1. Quando Fase 3 (IA) e Frente A (Identidade Visual) forem executadas — ambas parqueadas no método — poderão adotar integralmente, parcialmente ou substituir essas sugestões.

**Camada C (clareza adicional) — Fase 3 e Frente A seguem parqueadas:**

- **Sistema de Sugestões de IA** (UX e lógica da camada IA) continua em Fase 3 · `⬜ Não iniciado`. O DCV-V1 apenas registra "a IA, quando vier, opera a partir do contrato estrutural declarado pelo usuário na Etapa 1 (arquivos + abas + nomes Origem/Comparado)".
- **Paleta canônica e identidade visual** continuam em Frente A · `⚠️ Em andamento`.

**Razão:** A correção da Usuária evita três erros estruturais que o Arquiteto estava prestes a cometer:
1. Antecipar Fase 3 sem método, introduzindo decisão de UX de IA fora de contexto adequado.
2. Antecipar Frente A, cristalizando paleta de cores que ainda não foi validada pela identidade primária.
3. Inflar o escopo da Fundação com 3 transversais (T-MODELO, T-UISTATE, T-IA-HINTS) quando apenas um (T-MODELO) é realmente transversal de dado, e os outros dois são comportamento de UI que pertence à Spec de cada visão.

A separação A/B/C preserva o que é real padrão de produto (3 elementos) e descarta o que é só sugestão visual estética (cores, componentes, copy específico).

**Impacto:**
- CONTEXT v2 ganha §13 "Padrões estruturais de produto entre visões" (redação no Item 2)
- Escopo do G-FUND (Fase 1) ganha T-MODELO como transversal novo. Escopo de transversais atualizado em CONTEXT §6 e planilha aba "4. Motores e Transversais"
- GLOSSARIO ganha entradas: "Objetivo da Visão", "Fluxo de etapas progressivas", "Modelo de configuração", "Wireframe Figma V1 (referência)", "T-MODELO"
- Arquivos `PADRAO_IA_TABLOFLOW.md` e `TEMPLATE_PROMPT_VISOES.md` ficam fora do repositório do projeto — permanecem no Figma Make como referência do wireframe. Não há criação de `/docs/padroes/` como o Arquiteto chegou a considerar.
- Fase 3 e Frente A permanecem com status atual na planilha (sem mudança).

**Referência canônica:** CONTEXT v2 §13 (novo) · GLOSSARIO §"Padrões estruturais do produto" (novo) · planilha v2 aba "4. Motores e Transversais" (T-MODELO adicionado)

### D-014 — Reforma do método pós-DCVs do Módulo 1: três fases, Fundação única, ordem por famílias
**Data:** 2026-04-18 · **Bloco:** (decisão de método, sem bloco Claude Code) · **Status:** Fechada

**Contexto:** Entre 17 e 18 de abril de 2026, a Usuária produziu — com apoio do ChatGPT como analista técnico (D-012) — os 10 DCVs prévios do Módulo 1 (V1 a V10). Ao revisar o conjunto completo pela primeira vez, três problemas estruturais do método anterior ficaram evidentes:

1. **A "onda padrão" (V2, V4, V7, V6, V10) herdada do planejamento estratégico não refletia dependência lógica entre visões.** Era uma escolha de priorização de valor de negócio, não de sequência técnica. A leitura consolidada dos 10 DCVs revelou que as visões se agrupam em **5 famílias conceituais** (Confronto, Sequência, Composição, Posição relativa, Estrutura interna), e que dentro de cada família há uma visão "mãe" e uma "irmã" — construir a mãe primeiro economiza trabalho na irmã. A ordem por famílias emergiu como mais barata que a ordem por prioridade.

2. **Os motores atuais (`motor_upload`, `motor_base`), já em auditoria pela D-013, claramente não servem aos requisitos consolidados dos 10 DCVs.** Eles foram construídos para a V2 antiga (hoje em `/legacy/`) e não cobrem: consolidação configurável pré-análise com regra de agregação (exigida por V2, V3, V4, V6, V7, V8, V9, V10), pivot automático POR_LINHAS → POR_COLUNAS (V2, V3, V4), eixo sequencial ordenado com intervalo De/Até (V3, V8), classificação categórica semântica para uso como eixo (V6, V7), e diagnóstico estrutural obrigatório padronizado (todos). O bloco `G-MOT` previsto pela D-011 assumia "auditoria que pode ou não exigir reescrita"; a realidade é que a reescrita é certa.

3. **Havia ambiguidade estrutural sobre onde viviam decisões de UX.** A Spec antiga carregava contratos Pydantic e regras de cálculo, mas deixava UX implícita — o que gerava descoberta tardia de lacunas apenas no app Streamlit, quando era caro mudar. Vários DCVs (notadamente V3 e V8) já traziam descrição de fluxo de tela embutida, mas sem padrão. A Usuária propôs uma etapa explícita de "UX estrutural" antes do código.

**Decisão:** Reforma estrutural do método em quatro eixos:

**Eixo 1 — Três fases sequenciais substituem a noção de "ondas".**
- **Fase 0 · Compreensão** — produzir os 10 DCVs aprovados. Mantém o fluxo 3 etapas da D-012 (Usuária + ChatGPT → Arquiteto refina → Usuária aprova).
- **Fase 1 · Fundação** — consolidar, especificar e implementar motores + contratos + transversais + exportação Excel padrão, a partir dos requisitos unificados dos 10 DCVs. Substitui e amplia o escopo do antigo `G-MOT`.
- **Fase 2 · Visões** — implementar as 10 visões sobre a Fundação aprovada, na ordem lógica por famílias.

Nenhuma fase inicia sem a anterior estar 100% completa.

**Eixo 2 — Ordem de implementação das visões por famílias conceituais** (substitui a "onda padrão"):
1. Família A · Confronto → V2, V1
2. Família C · Composição → V4, V10
3. Família B · Sequência → V3, V8
4. Família D · Posição relativa → V7, V9
5. Família E · Estrutura interna → V5, V6

Racional: começar pela família cuja "mãe" é mais simples, e pela família que produz transversais reutilizáveis (T-AGRUPA, T-DIAG, T-PIVOT saem da Família A; T-ABC, T-ACUM, T-RANK saem da Família C; T-EIXO sai da Família B).

**Eixo 3 — Esqueleto de tela vira seção obrigatória da Spec, não bloco separado.** Toda Spec passa a ter três seções fixas: (a) contratos lógicos, (b) regras de cálculo, (c) esqueleto de tela. A Usuária avaliou essa abordagem mais barata que criar um bloco `EV-N` separado, porque (i) vários DCVs já trazem material para o esqueleto, (ii) mantém contrato e UX no mesmo documento auditável, (iii) reduz pontos de parada no fluxo.

**Eixo 4 — Consolidação documental limpa, histórico preservado em DECISIONS.**
- `CONTEXT.md` reescrito do zero: 14 regras numeradas acumuladas viram 10 princípios em 3 camadas (método, artefato, operação). Versão anterior preservada em `/legacy/context_v1.md`.
- `GLOSSARIO.md` reescrito refletindo o vocabulário novo. Termos descontinuados (B-NR, V-Nb, N-Motores, onda padrão, N-VN, V-0c, G-MOT) ficam como nota histórica curta, com referência à decisão que os descontinuou.
- Planilha reestruturada com colunas refletindo as 3 fases; linhas de visões na ordem por famílias; abas Motores/Transversais/Glossário atualizadas.
- Instruções do Projeto reescritas do zero em paralelo ao CONTEXT v2.
- `DECISIONS.md` **preservado integralmente** — D-001 a D-013 mantêm seu valor histórico e ficam abaixo desta entrada.

**Razão:** As três descobertas (ordem errada, motores inservíveis, UX órfã) compartilham uma causa comum: o método anterior evoluiu por emenda em vez de por revisão estrutural. Toda vez que um problema aparecia, uma regra nova era adicionada ao CONTEXT — acumulamos 14 regras, vários tipos de bloco descontinuados, uma "onda padrão" que perdeu função. O custo de continuar emendando é maior que o custo de reescrever o método agora, porque os 10 DCVs prontos dão pela primeira vez visibilidade consolidada sobre tudo que precisa existir. Adiar a reforma significaria construir a Fase 1 sobre um método que já sabemos que não serve — exatamente o erro que a D-011 e a D-013 já corrigiram em contextos menores.

Alternativas consideradas e descartadas:
- **Preservar as 14 regras e apenas adicionar as novas** — rejeitada porque o objetivo é sair do acúmulo, não aumentá-lo (Opção B escolhida pela Usuária).
- **Implementar V2 sobre motores atuais e reescrever motores depois** — rejeitada porque produziria retrabalho certo em V2 quando os motores forem reescritos.
- **Criar bloco "EV-N" separado para esqueleto de tela** — rejeitada pela Usuária: adiciona parada no fluxo e separa UX de contrato que deveriam nascer juntos.

**Impacto:**

*Artefatos novos:*
- `CONTEXT.md` v2 (este documento substitui completamente o anterior)
- `GLOSSARIO.md` v2
- `TabloFlow_Estado_do_Projeto.xlsx` v2 (estrutura reorganizada por fases)
- Instruções do Projeto v2 (no painel do Projects)

*Artefatos preservados em `/legacy/`:*
- `context_v1.md` (CONTEXT anterior à D-014)
- `glossario_v1.md` (GLOSSARIO anterior à D-014)
- Artefatos pré-DCV já movidos por D-009 e D-013

*Artefatos que permanecem inalterados:*
- `DECISIONS.md` — apenas ganha esta entrada no topo. D-001 a D-013 permanecem íntegros.
- Os 10 DCVs prévios em `/specs/dcv/` — são insumo para o refino pelo Arquiteto na Fase 0, não são substituídos.

*Nomenclatura de blocos:*
- Novos: `G-FUND`, `F-MOT`, `F-TRANS`, `F-EXP`, `F-BASE`, `S-VN`, `B-VN`, `V-VN`, `A-VN`
- Descontinuados (apenas para leitura de histórico): `B-NR`, `V-Nb`, `N-Motores`, `G-MOT`, `N-VN`, `V-0c`, `T-XXX` (este último porque transversais agora são identificados no G-FUND e implementados na Fase 1, não extraídos tardiamente)

*Decisões anteriores que permanecem válidas mas operam sob o método novo:*
- D-001 a D-004 (decisões de comportamento da V2) — ficam como **diretrizes a serem incorporadas** no DCV-V2 aprovado e na spec_v2 produzida na Fase 2.
- D-006 (Gamma descontinuado como gerador) — ampliada: Gamma agora é ferramenta de formatação de documento apresentável final; nunca gera artefato técnico.
- D-007, D-008 (correções de motor_base) — historicamente relevantes. Na prática, o motor novo da Fase 1 não herda o código atual; herda o aprendizado (inferência semântica de boolean disfarçado, necessidade de `arquivo_bytes` no UploadResult) como requisito a cobrir.
- D-009, D-013 (artefatos movidos para /legacy/) — permanecem. `/legacy/` continua sendo a pasta-arquivo do projeto.
- D-010 (regeneração planejada de base_v2) — absorvida: base_v2 será gerada do zero na Fase 2 via bloco `B-V2` a partir do DCV-V2 aprovado e da spec_v2.
- D-011 (DCV como etapa obrigatória) — mantida. É princípio A.2 do CONTEXT v2.
- D-012 (ChatGPT como analista técnico prévio) — mantida sem alteração.

**Pendências abertas criadas por esta decisão:**
- Produzir `MODELO_DCV_PREVIO.md` em `/specs/dcv/` (D-012 previu, mas o arquivo ainda não existe formalmente — será necessário para futuros DCVs do Módulo 2).
- Decidir durante F-MOT se V10 é implementada como visão independente ou como preset/modo de V4. Essa decisão virá naturalmente quando chegarmos na Família C da Fase 2, informada pelo DCV-V4 e DCV-V10 já refinados.

**Referência canônica:** `CONTEXT.md` (v2, este repositório) · `TabloFlow_Estado_do_Projeto.xlsx` (v2) · Instruções do Projeto (v2, painel do Projects)

---

### D-013 — V2 movida para `/legacy/` por aplicação retroativa da Regra 13
**Data:** 2026-04-17 · **Bloco:** (decisão de processo, sem bloco Claude Code) · **Status:** Fechada
**Contexto:** Após adoção do método DCV (D-011) e do fluxo ChatGPT-Arquiteto-Usuária para produção de DCVs (D-012), ficou evidente que manter a V2 em status misto (spec ✅ + base 🔶 + visão 🔶 + app 🔶) era incoerente com a nova diretriz de "começar pelo DCV". A V2 nunca chegou a ter as decisões D-001..D-004 implementadas no código. Manter o legado como base para o trabalho novo (via blocos B-2R "regeneração de base" e V-2b "correção de visão") forçaria o método antigo de "evolução incremental sobre artefato pré-DCV" — exatamente o que o novo método rejeita. A Usuária aplicou retroativamente a mesma lógica da D-009 (que tratou V4, V6, V7) e moveu manualmente todos os artefatos da V2 para `/legacy/`.
**Decisão:** Aplicar à V2 o mesmo tratamento dado a V4/V6/V7 pela D-009. Artefatos `spec_v2.md`, `visao_v2.py`, `app_v2.py`, `base_v2.xlsx` (e quaisquer outros artefatos da V2 ainda em `/specs/`, `/src/`, `/bases/`) movidos para `/legacy/`. A nova V2 será **construída do zero** a partir do DCV-V2 aprovado, seguindo o fluxo padrão pós-DCV. Decisões D-001 a D-004 e D-010 permanecem **válidas como diretrizes** que o DCV-V2 deve incorporar — elas representam trabalho intelectual sobre comportamento, não sobre implementação (que nunca chegou a ser feita).
**Razão:** Coerência com D-009. O método novo (DCV → spec → base → código → app → validação) não admite caminho intermediário "evolutivo" sobre artefato pré-DCV. Tentar tal caminho seria recriar o problema que a D-011 resolveu estruturalmente. Custo de descarte é menor que parece — o trabalho de spec da V2 anterior nunca foi implementado, então não há código a ser perdido. As decisões intelectuais (D-001..D-004, D-010) são preservadas porque foram registradas em DECISIONS.md, não no código.
**Impacto:**
- Pasta `/legacy/` agora contém os artefatos pré-rebaseline de V2 + V4 + V6 + V7 + specs antigas dos motores
- Tipos de bloco `B-NR` (regeneração de base) e `V-Nb` (correção de visão) ficam **descontinuados**: não há mais cenário em que façam sentido no método novo
- Planilha `TabloFlow_Estado_do_Projeto.xlsx`:
  - V2 com todas as 9 colunas (DCV até IA) marcadas como ⬜ Não iniciado, exceto coluna 0. DCV que fica 🟦 Aguardando DCV
  - Próximo Passo Operacional reformulado: B-2R e V-2b removidos da fila; implementação da V2 vira parte do ciclo padrão pós-G-MOT (spec → base → código → app)
  - Aba "5. Glossário" marca B-NR e V-Nb como descontinuados
  - Aba "4. Motores e Transversais": status de código dos motores volta para 🔶 EM AUDITORIA porque serão reauditados no G-MOT contra requisitos consolidados dos DCVs aprovados (não há mais como considerá-los "Concluído" sem essa auditoria)
- DCV-V2 ad-hoc construído na conversa de 17/04/2026 vira **insumo** para o DCV-V2 final (não substitui)
- Fase 0 (Blueprint) muda para ⚠️ Em andamento — diretrizes de produto detalhadas estão sendo produzidas pela Usuária a cada DCV
**Referência canônica:** `/legacy/` (arquivos da V2 movidos para lá) · planilha § Módulo 1 (linha V2) · D-009 (precedente metodológico)

---

### D-012 — ChatGPT como analista técnico prévio para DCVs
**Data:** 2026-04-17 · **Bloco:** (decisão de processo, sem bloco Claude Code) · **Status:** Fechada
**Contexto:** Após aprovação do DCV como etapa zero obrigatória do método (D-011), surgiu a questão de quem produz o **rascunho inicial** de cada DCV. Produzir todos pelo Arquiteto exigiria muitas sessões dedicadas no Projects, com atraso significativo da fila operacional. A Usuária propôs usar ChatGPT como analista técnico de apoio, com ela validando o rascunho antes de encaminhar ao Arquiteto.
**Decisão:** Adotar fluxo em 3 etapas para produção de cada DCV:
1. **Usuária + ChatGPT** produzem o **DCV prévio** (rascunho), usando o template `MODELO_DCV_PREVIO.md` e materiais de produto (Blueprint da visão + diretriz da Usuária)
2. **Arquiteto (Claude no Projects)** recebe o DCV prévio, refina aplicando o método TabloFlow (formato padrão, distinção rigorosa Estado/Agrupador/Filtro, contratos Pydantic identificados, pendências P-NN com opções e trade-offs), devolve **DCV final** em prosa
3. **Usuária aprova** → DCV vira `dcv_vN.md` em `/specs/compreensao/` e a coluna "0. DCV" da planilha vira `✅ Aprovado`
**Razão:** Usar ChatGPT como gerador de rascunho aproveita capacidade técnica da Usuária e reduz carga sobre o Arquiteto, sem violar o método: o Arquiteto continua sendo quem aplica o padrão TabloFlow e quem identifica considerações técnicas que escapam ao analista de apoio. Usuária permanece como ponto de decisão final. Alternativa de "Arquiteto produz tudo do zero" foi rejeitada por gargalo de tempo. Alternativa de "ChatGPT produz e Usuária aprova direto" foi rejeitada por bypassar o filtro técnico do Arquiteto (que conhece o método, motores, decisões anteriores).
**Impacto:**
- Novo arquivo `MODELO_DCV_PREVIO.md` em `/specs/compreensao/` — template usado pela Usuária com o ChatGPT
- Fluxo de cada DCV-VN passa por 3 etapas (prévio → refinado → aprovado), não 1
- Nenhuma alteração em código ou contratos
**Referência canônica:** `/specs/compreensao/MODELO_DCV_PREVIO.md` · D-011 (que define o que é DCV)

---

### D-011 — Adoção do DCV (Documento de Compreensão da Visão) como etapa zero obrigatória
**Data:** 2026-04-17 · **Bloco:** (decisão de processo) · **Status:** Fechada
**Contexto:** Durante o planejamento do Bloco B-2R (regeneração da base_v2.xlsx), a conversa entre Arquiteto e Usuária precisou ser refeita 3 vezes em 5 turnos: a cada documento novo de produto fornecido (Blueprint Gamma → diretriz da Usuária), o desenho da base sintética mudava substancialmente. A Usuária identificou que o método TabloFlow, mesmo com 12 regras estabelecidas, não tinha uma etapa formal de **alinhamento de compreensão da visão antes de qualquer geração de spec/base/código**. Esse mesmo problema havia gerado a V4 "concluída" sem auditoria adequada, levando à decisão D-009 de mover artefatos para `/legacy/` e refazer do zero.
**Decisão:** Criar a etapa **DCV (Documento de Compreensão da Visão)** como pré-requisito obrigatório de qualquer visão. O DCV é um documento curto em prosa, vivendo em `/specs/compreensao/dcv_vN.md`, que captura: (1) o que a visão faz em uma frase de negócio na voz da Usuária, (2) o que a visão precisa receber, (3) o que a visão precisa entregar, (4) pendências enumeradas que precisam de decisão antes de qualquer outra coisa. Sem DCV aprovado pela Usuária, nenhuma outra etapa da visão pode iniciar. Adotada como **Regra 13** do CONTEXT.md. Decisão complementar: novo bloco **G-MOT (Gate de Motores)**, registrado como **Regra 14**, obriga auditoria dos motores contra requisitos consolidados de uma onda de DCVs aprovados antes da implementação de qualquer `visao_vN.py` da onda.
**Razão:** Sem alinhamento de compreensão prévio, o Arquiteto trabalha com uma versão parcial da visão e produz spec/base que parecem corretas mas escondem lacunas — só descobertas em runtime ou em validação visual, gerando ciclos de retrabalho caros. O DCV transforma essa fase de "validação acidental por proposta" em "alinhamento explícito", permitindo que pendências sejam fechadas no nível certo (compreensão) antes de descer para spec (contrato) e código (implementação). Custo estimado por visão: ~30–60 minutos de conversa + 1 sessão de Arquiteto. Ganho: zero ciclos de retrabalho de spec/base. Como o DCV exige antecedência (Cenário C aprovado), permite também que o bloco G-MOT veja todos os requisitos de motor de uma onda completa antes de mexer nos motores — eliminando o risco de motor "frankenstein" construído um remendo por vez.
**Impacto:**
- `CONTEXT.md` ganha **Regra 13** (DCV obrigatório) e **Regra 14** (G-MOT como gate)
- `CONTEXT.md` § 11 (Tipos de bloco) ganha 3 novos: `DCV-VN`, `DCV-OPN`, `G-MOT`
- `CONTEXT.md` § 5 (Fontes de verdade) acrescenta DCVs em `/specs/compreensao/` à hierarquia
- `CONTEXT.md` § 6 (Estrutura de pastas) acrescenta `/specs/compreensao/`
- Planilha `TabloFlow_Estado_do_Projeto.xlsx` ganha:
  - Coluna **"0. DCV"** antes de "1. Spec" nas abas Módulo 1 e Módulo 2
  - Status **🟦 Aguardando DCV** (novo, na Legenda de Status)
  - Aba **"5. Glossário"** (incluindo nomenclatura DCV, G-MOT, etc.)
  - Bloco G-MOT registrado na aba "4. Motores e Transversais"
  - Próximo Passo Operacional reformulado para refletir onda padrão (V2, V4, V7, V6, V10) → G-MOT → implementação
- Novo arquivo na raiz: `GLOSSARIO.md` (versão completa do glossário)
- Bloco antigo `N-Motores` (que estava sem prioridade) é **substituído pelo G-MOT** com escopo claro
- Onda padrão de DCVs definida: **V2, V4, V7, V6, V10** (as 5 primeiras da fila estratégica)
**Referência canônica:** `CONTEXT.md` § 7 (Regras 13 e 14) · `CONTEXT.md` § 11 (novos tipos de bloco) · `/specs/compreensao/` (pasta dos DCVs)

### D-010 — Regeneração planejada de base_v2.xlsx no padrão fundido
**Data:** 2026-04-17 · **Bloco:** (planejamento, antes de bloco formal) · **Status:** Fechada (planejamento) / execução pendente
**Contexto:** Durante organização documental pós-Bloco 8, descoberta da `spec_base_v2.md` (arquivo de 17/04 11:15, gerada pelo Gamma antes do método TabloFlow estar consolidado). Essa spec planejava uma base de volume realista (150–250 linhas por aba, cobertura explícita de W02 e W05, domínio de Vendas corporativas). A `base_v2.xlsx` efetivamente gerada no Bloco B-2 ficou com volume didático (12–16 linhas por aba, sem W02 nem W05), focada em gabarito auditável (30 casos em aba CASOS_ESPERADOS). Após instituída a **Regra 9** (validação exige mínimo 50 linhas), a base atual violaria a regra.
**Decisão:** Regenerar `base_v2.xlsx` **fundindo** o melhor das duas abordagens:
- **Da spec_base_v2 Gamma:** volume 150–250 linhas/aba, cobertura de W02 (cardinalidade alta) e W05 (POR_LINHAS sem par), reprodutibilidade via seed fixa, script gerador versionado
- **Da base_v2.xlsx atual:** aba CASOS_ESPERADOS separada com gabarito auditado, aba README, multi-tipo com PERCENTUAL e INDICE (não só Vendas puro)
- **Incorporar decisões D-001 a D-004** (warnings W06 e W07 que não existiam quando a spec Gamma foi escrita)
Executar antes do Bloco V-2b.
**Razão:** Base subdimensionada esconde bugs de volume na visão (como escondeu no motor_base, origem do V-0c). Rodar V-2b com base atual arrisca validação insuficiente. Regeneração cumpre Regra 9 e incorpora todo o aprendizado pós-B-2.
**Impacto:**
- Nova `specs/spec_base_v2.md` a produzir (a antiga foi movida para `/legacy/spec_base_v2_gamma.md`)
- Novo `bases/gerar_base_v2.py` (script versionado, determinístico)
- `bases/base_v2.xlsx` atual será preservada como `/legacy/base_v2_v1.xlsx` quando a nova for gerada
- Aba CASOS_ESPERADOS da nova base terá volume proporcionalmente maior (mais casos auditados)
**Pendências vinculadas:** execução depende de planejamento da nova spec (em andamento) e aprovação da Usuária antes da geração do arquivo.
**Referência canônica:** este D-010 · nova `specs/spec_base_v2.md` (a produzir)

---

### D-009 — Reset de V4, V6, V7: artefatos legados movidos para /legacy/, serão refeitos do zero
**Data:** 2026-04-17 · **Bloco:** (decisão manual, sem bloco Claude Code) · **Status:** Fechada
**Contexto:** Após o rebaseline do projeto (D-005, D-006) e a identificação de que specs geradas pelo Gamma não seguem o método TabloFlow, decidiu-se que V4, V6 e V7 não seriam reaproveitadas via edição incremental da versão antiga.
**Decisão:** Todos os artefatos legados dessas três visões (`spec_v4.md`, `spec_v6.md`, `spec_v7.md`, `visao_v4.py`, `visao_v6.py`, `visao_v7.py`, `app_v4.py`, `base_v4.csv`) foram movidos para a pasta `/legacy/` na raiz do projeto. Essas visões serão refeitas **do zero** (não evoluídas) em blocos do tipo `N-V[N]`, usando o Blueprint (Gamma) como única fonte estratégica e o `spec_v2.md` + `base_v2.xlsx` como referência de padrão.
**Razão:** Refazer do zero evita que vieses e lacunas da geração antiga se propaguem silenciosamente para a versão nova. Evolução incremental de spec ruim tende a carregar omissões invisíveis, que só aparecem como bug em runtime (exatamente o cenário do Bloco 8). Reconstrução aplica o método TabloFlow desde a linha 1 do novo artefato.
**Impacto:**
- `/legacy/` contém os artefatos pré-rebaseline de V4, V6, V7 + as specs de motores antigas
- `/specs/`, `/src/` e `/bases/` contêm apenas artefatos do método novo
- Planilha reflete "Não iniciado" para V4, V6, V7 em todas as colunas
- Nenhum código em `/src/` depende de `/legacy/`
**Próximos blocos relacionados:**
- N-V4 (após V-2b e regeneração da base_v2) — reescrever spec_v4 + gerar base_v4.xlsx do zero
- N-V7 (depois) — idem
- N-V6 (depois) — idem
- N-Motores (futuro, sem prioridade definida) — reescrever specs dos motores no padrão V2 (código já validado em V-0c)
**Referência canônica:** pasta `/legacy/` · `CONTEXT.md` § 6 (Estrutura de pastas)

---

### D-008 — Inferência semântica reconhece boolean disfarçado em float64
**Data:** 2026-04-17 · **Bloco:** V-0c · **Status:** Fechada
**Contexto:** Ao corrigir o truncamento em motor_base (ver D-007), o teste C03 de `teste_motores.py` passou de verde para vermelho. Causa-raiz: Excel serializa colunas booleanas com nulos como float64 (1.0, 0.0, NaN), e a função `_infer_type_from_series` tinha early-return para `'numeric'` assim que `is_numeric_dtype` era True, antes de checar se os valores não-nulos estavam contidos em {0, 1}. O C03 passava antes por acidente: o bug do preview stringificava os valores, e o fluxo caía em outro ramo que produzia `'boolean'`. Com o fix, a stringificação sumiu e a limitação apareceu.
**Decisão:** Adicionada regra de inferência semântica em `_infer_type_from_series`: antes do early-return `'numeric'`, se o dtype é numérico E os valores não-nulos estão contidos em {0, 1, 0.0, 1.0, True, False} E existe pelo menos um nulo → retornar `'boolean'`. `BOOL_MAP` foi expandido para incluir as chaves `"1.0"` e `"0.0"` para conversão consistente. Novo warning W-B01 é emitido quando essa detecção dispara, alertando o usuário para confirmar a intenção analítica.
**Razão:** O `motor_base` faz inferência **semântica** (analítica), não apenas técnica. Uma coluna `{0, 1, NaN}` classificada como numeric permitiria agregações estatísticas inválidas sobre um flag (média, desvio padrão de um booleano), o que contradiria o propósito do motor. Manter o comportamento "certo pelo motivo certo" — antes estava certo por acidente (bug mascarando). Alternativa de aceitar `'numeric'` foi rejeitada por fragilizar o uso analítico em todas as visões que dependem dessa inferência.
**Impacto:**
- `motor_base.py` — nova ramificação em `_infer_type_from_series` + warning W-B01 emitido em `_build_column_meta`
- `BOOL_MAP` estendido com `"1.0"` e `"0.0"`
- `teste_motores.py` C03 continua passando (retorna `'boolean'` agora pelo motivo certo)
- Novo warning W-B01 no vocabulário do MotorResult
**Pendências menores:**
- Validar se teste C03 verifica explicitamente a emissão de W-B01 (não só o tipo). Não bloqueante — pode ser fechado quando `spec_motor_base.md` e `spec_validacao_motores.md` forem reescritas no padrão V2 (bloco N-Motores).
- W-B01 ainda não está catalogado em `spec_motor_base.md` (spec legada em auditoria).
**Risco conhecido:** falso positivo raro — uma coluna numérica real cujos valores coincidentemente sejam {0, 1} + nulos seria classificada como boolean. Aceitável no contexto analítico.
**Referência canônica:** `src/motor_base.py` § `_infer_type_from_series` e `_build_column_meta` · `src/teste_motores.py` § caso_b03

---

### D-007 — Correção do truncamento em motor_base + campo `arquivo_bytes` no UploadResult
**Data:** 2026-04-17 · **Bloco:** V-0c · **Status:** Fechada
**Contexto:** Bug crítico identificado no Bloco 8: `motor_base.py` construía o DataFrame interno do `MotorResult` apenas a partir de `upload_result.preview` (5 linhas). Todas as visões recebiam DataFrame truncado. Os 21 testes de `teste_motores.py` passavam porque usavam bases ≤5 linhas, então o truncamento nunca virava observável (causa da Regra 9 do CONTEXT.md). No diagnóstico do V-0c, descoberto que `UploadResult` tinha apenas `file_name` (string) e `preview` (5 linhas) — não havia `arquivo_bytes` nem caminho. Impossível corrigir só em `motor_base.py`.
**Decisão:** Adicionado campo `arquivo_bytes: Optional[bytes]` ao contrato `UploadResult` em `motor_upload.py`, populado via `path.read_bytes()` em `process_file`. `motor_base.py` passa a construir `df` via `pd.read_excel(BytesIO(upload_result.arquivo_bytes), sheet_name=aba_selecionada)` para Excel ou `pd.read_csv` para CSV. Guarda de erro adicionada caso `arquivo_bytes` venha vazio. Lógica de análise (inferência de tipos, null_count, candidatos categóricos) preservada sem alteração. Novo teste B13 em `teste_motores.py` com base sintética de 60 linhas e asserção crítica `assert len(motor_result.df) == 60` como regressão permanente.
**Razão:** A regra canônica do projeto é "Arquivo bruto → Motor de Upload → UploadResult → Motor Base". Um `UploadResult` sem os bytes do arquivo era um **bug de contrato**, não um recurso a preservar. Alternativa de passar bytes como argumento separado ao motor_base foi rejeitada por forçar todos os callers (apps, testes, blocos futuros) a carregar bytes separadamente — quebraria a cadeia canônica e multiplicaria retrabalho linearmente a cada visão nova.
**Impacto:**
- `src/motor_upload.py` — campo novo em `UploadResult`, populado em 3 branches (CSV, multi-sheet stub, Excel)
- `src/motor_base.py` — leitura completa via BytesIO substituindo leitura de preview
- `src/teste_motores.py` — novo caso B13 adicionado à lista `casos`
- `specs/spec_motor_upload.md` — contrato atualizado com nota de concessão pragmática da Fase 2
- Workaround D-005 em `src/app_v2.py` — **agora obsoleto**, deve ser removido no Bloco V-2b
**Consequência:** `motor_upload.py` e `motor_base.py` (código) saíram de "Legado em auditoria" para "Concluído" na planilha. As specs correspondentes (`spec_motor_upload.md`, `spec_motor_base.md`, `spec_validacao_motores.md`) permanecem em auditoria até o bloco N-Motores.
**Resultado dos testes:**
- Baseline (antes): 21/21 ✅
- Após fix motor_base (sem D-008): 20/21 ❌ (C03 quebrou — endereçado em D-008)
- Após D-008: 21/21 ✅
- Com B13 adicionado: 22/22 ✅
**Referência canônica:** `src/motor_upload.py` § `UploadResult` · `src/motor_base.py` § construção de df · `specs/spec_motor_upload.md`

---

### D-006 — Gamma descontinuado como gerador de artefatos
**Data:** 2026-04-17 · **Bloco:** (decisão de processo, pós-Bloco 8) · **Status:** Fechada
**Contexto:** Specs geradas pelo Gamma (V4, V6, V7, motores, base_v2 inicial) não seguem o padrão consolidado do projeto. Uso do Gamma para esse fim foi metodologicamente incorreto — o Gamma é repositório estratégico, não ferramenta de produção de contratos técnicos.
**Decisão:** Gamma volta ao papel original (repositório de Blueprint estratégico). Toda geração de specs, bases sintéticas e prompts de bloco passa a ser responsabilidade do **Arquiteto** (Claude no Projects), com validação da Usuária.
**Razão:** Garantir que todo artefato do projeto passe pelo mesmo método — contratos Pydantic explícitos, pendências fechadas antes de implementação, casos-limite enumerados. O Gamma não produz artefatos nesse padrão.
**Impacto:** Nenhuma spec nova vem do Gamma. Specs legadas serão reescritas uma a uma no padrão V2 à medida que a visão correspondente for ser trabalhada. Esta decisão virou a **Regra 8** do CONTEXT.md.
**Referência canônica:** `CONTEXT.md` § 7 (Regra 8) · Instruções do Projects

---

### D-005 — Rebaseline do projeto pós-Bloco 8
**Data:** 2026-04-17 · **Bloco:** (decisão de processo, pós-Bloco 8) · **Status:** Fechada
**Contexto:** Descoberta no Bloco 8 de bug crítico em `motor_base` (truncamento em 5 linhas) + 4 divergências em `visao_v2.py` (D-001 a D-004 não implementadas) + identificação de que specs geradas pelo Gamma não passaram pelo método atual do projeto. Usuária levantou explicitamente a insegurança em considerar artefatos como "concluídos".
**Decisão:** Rebaselinar planilha de estado. Apenas `spec_v2.md` + `base_v2.xlsx` permanecem como "Concluído" no momento do rebaseline. Todos os demais artefatos existentes passam para status "Legado — em auditoria" até revisão individual. Criada nova categoria de status na planilha: 🔶 EM AUDITORIA (entre ✅ Concluído e ⬜ Não iniciado).
**Razão:** O método TabloFlow (specs com contratos Pydantic, bases sintéticas multi-aba com CASOS_ESPERADOS, decisões registradas em DECISIONS.md) foi consolidado apenas a partir do Bloco B-2. Artefatos anteriores não podem ser tratados como auditados sem passar por esse processo. Manter como "Concluído" seria auto-engano estrutural.
**Impacto:**
- Fila de blocos totalmente reordenada (V-0c → V-2b → N-V4 → N-V7 → N-V6 → Bloco 9)
- Três novos tipos de bloco criados: V-Nb (correção), N-VN (reescrita do zero), N-Motores (reescrita de specs de motor)
- Criadas as Regras 7, 8, 9 do CONTEXT.md como lições estruturais desse incidente
**Referência canônica:** `CONTEXT.md` § 7 (Regras 7, 8, 9) · planilha `TabloFlow_Estado_do_Projeto.xlsx` (coluna Status rebaselinada)

---

### D-004 — Nulo nunca é tratado como zero na V2
**Data:** 2026-04-17 · **Bloco:** B-2 · **Status:** Fechada
**Contexto:** Spec V2 definia comportamento para zeros (SURGIMENTO/DESAPARECIMENTO) mas era omissa sobre nulos. Base de validação `base_v2.xlsx` expôs casos de nulo (SKU-101, SKU-103, SKU-202) que forçavam decisão.
**Decisão:** Registro com nulo em A ou B é excluído da análise — não entra em `registros` nem em contagens. Warning W01 ampliado para cobrir tanto registros individuais com nulo quanto >20% de nulos no campo.
**Razão:** Tratar nulo como zero seria inventar valor — viola o princípio determinístico do TabloFlow. Excluir + avisar preserva auditabilidade.
**Impacto:** `visao_v2.py` deve filtrar nulos antes do cálculo · W01 cobre 2 cenários distintos.
**Status de implementação:** ⚠️ **Não implementada** em `visao_v2.py` — identificada como divergência no Bloco 8. Corrigir em V-2b.
**Referência canônica:** `specs/spec_v2.md` § Decisões Tomadas no Bloco B-2 · D-P05.

---

### D-003 — `variacao_percentual` não é arredondada no contrato V2Result
**Data:** 2026-04-17 · **Bloco:** B-2 · **Status:** Fechada
**Contexto:** Spec V2 deixava em aberto o nº de casas decimais para `variacao_percentual`. Gabarito da `base_v2.xlsx` usou 6 casas como referência neutra.
**Decisão:** Contrato `RegistroComparado.variacao_percentual` preserva precisão total (float Python nativo). Arredondamento é responsabilidade da camada de exibição (`app_v2.py`) e da exportação Excel.
**Razão:** Arredondar no contrato perde informação irreversivelmente. Cada camada de saída pode ter precisão diferente conforme a necessidade.
**Impacto:** `visao_v2.py` retorna float sem arredondamento · `app_v2.py` formata para exibição · exportação Excel usa formato de célula (`0.0%` ou `0.00%`).
**Status de implementação:** ⚠️ **Não implementada** em `visao_v2.py` — identificada como divergência no Bloco 8 (motor faz `round(..., 4)` dentro do contrato). Corrigir em V-2b.
**Referência canônica:** `specs/spec_v2.md` § Decisões Tomadas no Bloco B-2 · D-P04.

---

### D-002 — Resumo PERCENTUAL/INDICE usa média simples + warning obrigatório
**Data:** 2026-04-17 · **Bloco:** B-2 · **Status:** Provisória (revisar Fase 3)
**Contexto:** Soma de campos PERCENTUAL e INDICE no `ResumoAgrupador` não tem significado matemático. Aba `POR_COLUNAS_MULTI_TIPO` da `base_v2.xlsx` forçou o tema (mistura VALOR, PERCENTUAL, INDICE).
**Decisão:** No `ResumoAgrupador`, para campos PERCENTUAL ou INDICE: `total_a` e `total_b` recebem média simples dos valores no grupo. Warning W07 obrigatório sempre que houver pelo menos um campo desses tipos com agrupadores configurados.
**Razão:** Bloquear o resumo (alternativa C) frustra o usuário comum. Média ponderada (alternativa B) exige campo de peso adicional — adiciona configuração na Etapa 2 e pode confundir. Média simples + aviso explícito é o equilíbrio entre utilidade e honestidade.
**Impacto:** Lógica de `ResumoAgrupador` ramifica por tipo de campo · W07 sempre dispara nesse caso.
**Status provisório:** Revisitar em Fase 3 (UX) se reclamação de usuária aparecer. Alternativa futura: média ponderada com campo de peso configurável pelo usuário.
**Status de implementação:** ⚠️ **Não implementada** em `visao_v2.py` — W07 nunca é emitido hoje. Corrigir em V-2b.
**Referência canônica:** `specs/spec_v2.md` § Decisões Tomadas no Bloco B-2 · D-P02.

---

### D-001 — POR_LINHAS sem par tratado como SURGIMENTO/DESAPARECIMENTO
**Data:** 2026-04-17 · **Bloco:** B-2 · **Status:** Fechada
**Contexto:** Spec V2 não definia comportamento quando estrutura POR_LINHAS resultava em registros sem par após o pivot (presente em A mas não em B, ou vice-versa). Decisão pendente desde a spec original.
**Decisão:** Registro presente apenas em A → `DESAPARECIMENTO` (valor_b=0, variacao_pct=-1.0). Registro presente apenas em B → `SURGIMENTO` (valor_a=0, variacao_pct=None). Warning W06 (novo) reporta a contagem.
**Razão:** Preserva o registro · consistente com a regra de zeros já definida na spec · alinhado ao perfil de uso (analista corporativo *quer* ver "SKU novo apareceu em Jan/25"). Alternativa de excluir + warning esconderia eventos analíticos legítimos.
**Impacto:** Pivot em `visao_v2.py` deve preservar todos os registros · novo warning W06 entra na lista de warnings da V2.
**Status de implementação:** ⚠️ **Parcialmente implementada** em `visao_v2.py` — o outer merge preserva registros, mas W06 não é emitido. Corrigir em V-2b.
**Referência canônica:** `specs/spec_v2.md` § Decisões Tomadas no Bloco B-2 · D-P01.

---

## Convenções

- **Numeração D-XXX:** sequencial global. Não reaproveitar números mesmo se uma decisão for revogada.
- **Status `Revogada`:** quando uma decisão for substituída, marcar a antiga como Revogada (sem deletar) e registrar a nova com referência cruzada.
- **Status `Provisória`:** decisão tomada com ressalva explícita de revisão futura. Indicar em qual fase ou condição revisar.
- **Mapeamento de pendências de spec:** quando uma decisão fecha uma pendência local da spec (ex: D-P01 da V2), citar como `§ ... · D-P01` para preservar o link.
- **Campo "Status de implementação":** quando a decisão é de contrato mas a implementação está pendente em alguma visão/módulo, indicar explicitamente. Especialmente relevante para D-001 a D-004 enquanto V-2b não é executado.

---

## Decisões em aberto (não registradas como D-XXX)

Pendências que ainda não viraram decisão fechada:

- **P03 (da spec_v2.md)** — validar com usuárias se o limite de 10 campos comparados é adequado. Aguarda validação de produto. Não bloqueia implementação atual.
