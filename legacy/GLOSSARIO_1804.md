# GLOSSARIO.md — TabloFlow

Glossário completo de termos, nomenclaturas e convenções do projeto.

A versão **compacta** vive na aba "6. Glossário" da planilha `TabloFlow_Estado_do_Projeto.xlsx` para consulta rápida durante o trabalho operacional. Esta aqui é a versão **completa**, com exemplos e referências cruzadas — usada por sessões Claude Code, pelo Arquiteto, e como material de onboarding.

**Última atualização:** 18/04/2026 — v2 pós-D-014 (reforma do método). Versão anterior preservada em `/legacy/glossario_v1.md` apenas para auditoria.

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

Primeira fase do método TabloFlow. **Objetivo:** aprovar os 10 DCVs do Módulo 1. **Critério de conclusão:** os 10 DCVs aprovados pela Usuária. Nenhuma outra fase inicia sem isso (princípio A.1). Definida no CONTEXT v2 §3.

### `Fase 1 · Fundação` 📌

Segunda fase do método. **Objetivo:** consolidar os requisitos comuns dos 10 DCVs aprovados e implementar a fundação que serve as 10 visões (motores, contratos, transversais, exportação Excel padrão). **Critério de conclusão:** motores + transversais + exportação validados por testes automatizados E inspecionados pela Usuária sobre a base de fundação multi-visão. Definida no CONTEXT v2 §3.

### `Fase 2 · Visões` 📌

Terceira fase do método. **Objetivo:** implementar as 10 visões sobre a Fundação aprovada, na ordem lógica por famílias. Para cada visão, 5 artefatos sequenciais: Spec (com wireframe funcional) → Base → `visao_vN.py` → `app_vN.py` → Validação Visual. **Critério de conclusão por visão:** Validação Visual registrada na planilha.

### `Família conceitual` 📌

Agrupamento de visões que compartilham natureza analítica. 5 famílias no Módulo 1:

- **Família A · Confronto entre universos** — V2 (dois estados de uma base), V1 (duas bases)
- **Família B · Sequência ao longo de eixo ordenado** — V3 (valor no tempo), V8 (presença no tempo)
- **Família C · Composição e participação** — V4 (participação, ABC, multi-métrica), V10 (Pareto)
- **Família D · Posição relativa** — V7 (desvio da média do grupo), V9 (ranking multidimensional)
- **Família E · Estrutura interna** — V5 (dispersão e outliers), V6 (cruzamento de 2 categóricos)

A ordem de implementação segue A → C → B → D → E, porque começar pela família mais simples dentro de cada par gera transversais que a irmã reusa.

### `Wireframe funcional` 🆕📌

Descrição textual ou esquemática do fluxo de tela da visão: estados, configuração progressiva, microanálise, exportação. **Seção obrigatória da Spec** (princípio B.2 do CONTEXT v2) — não é bloco separado, mas recebe **aprovação explícita da Usuária antes do código iniciar**, dentro do mesmo bloco S-VN. Garante que UX e contrato lógico nasçam juntos, não se divergindo no app.

### `Validação Visual` 📌

Etapa exclusiva da Usuária (princípio B.4 do CONTEXT). Consiste em: carregar a base sintética oficial no app Streamlit, processar cada aba, comparar com o gabarito CASOS_ESPERADOS, confirmar clareza de campos e coerência de exportação Excel. Sem essa etapa documentada na planilha, app não é considerado concluído.

### `Rebaseline`

Processo de "zerar a contagem do que está concluído" quando se descobre que artefatos antigos não passaram pelo método atual. Já aconteceu **três vezes**:

- 17/04/2026 (D-005) — V4, V6, V7 e specs antigas dos motores
- 17/04/2026 (D-013) — V2 (aplicação retroativa após adoção do método DCV)
- 18/04/2026 (D-014) — método inteiro (todas as visões), após leitura consolidada dos 10 DCVs prévios

---

## 2. Blocos de execução (ativos)

Um bloco é uma sessão de trabalho dedicada a um artefato específico. **Nunca misturar tipos** na mesma sessão (princípio B.1).

### `DCV-VN` 📌

Refino pelo Arquiteto do DCV prévio da visão N. Produz o DCV final em `/specs/dcv/dcv_vN.md`. Output vai para aprovação da Usuária antes de virar canônico.

### `DCV-OPN`

Equivalente do DCV para operações do Módulo 2 (TabloPrep). Ex: DCV-OP-FILTER, DCV-OP-DEDUP. Ainda não ativos — começam após Módulo 1 avançar na Fase 2.

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

### `V-VN` 🆕

Implementação de `visao_vN.py`. Executado em Claude Code. Consome contratos da Fundação (MotorResult) e entrega VNResult padronizado.

### `A-VN` 🆕

Implementação de `app_vN.py` (Streamlit) executando o wireframe funcional aprovado. Consome `visao_vN.py`. Precede Validação Visual.

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

### `T-DUAL` 🆕

Extensão do `motor_upload` para aceitar entrada em modo dual, exigida exclusivamente pela V1 (Módulo 1). Aceita duas estruturas:

- **Estrutura A · Dois arquivos distintos** — usuário sobe 2 arquivos separados; sistema lista abas de cada um; usuário escolhe uma aba de cada arquivo como Origem e Comparado
- **Estrutura B · Um único arquivo** — usuário sobe 1 arquivo; sistema lista todas as abas; usuário escolhe 2 abas do mesmo arquivo

Produz `UploadResult` unificado com referência aos dois lados nomeados (defaults Origem/Comparado, editáveis). Usado apenas pela V1 dentro do Módulo 1. **Dados empilhados em uma única aba com coluna discriminadora não são escopo do T-DUAL** — exigem RESHAPE prévio no Módulo 2.

Formalizado em **D-018**.

### `T-AGRUPA` 📌

Consolidação por agrupadores antes do cálculo, com regra de agregação configurável (soma, média, máximo, mínimo, contagem). Usado por **TODAS** as visões. Princípio universal: "consolidar primeiro, calcular depois" — aparece explicitamente em cada um dos 10 DCVs.

### `T-DIAG` 📌

Diagnóstico estrutural obrigatório. **Aba padronizada no Excel exportado, sempre posicionada como última aba por regra transversal (D-017)** + bloco no Resumo Executivo. Registra: inconsistências detectadas, ajustes aplicados pelo motor, impacto, volume afetado. Usado por **TODAS** as visões. Garante o princípio C.2 (nada silencioso).

### `T-SEMA`

Semântica maior-é-melhor / menor-é-melhor / neutro. Regra de interpretação que transforma o resultado matemático em leitura de negócio. Usado por V2, V3, V7, V9. Ex: custo caiu 10% → matematicamente negativo, semanticamente (com "menor é melhor") positivo.

### `T-EIXO`

Eixo sequencial ordenado com intervalo De/Até, sem preenchimento de lacunas. Usado por V3 e V8. A V3 define o padrão (PARTE 2.3 do DCV-V3); V8 reusa. Lacunas não viram ponto analítico; podem ser registradas em diagnóstico.

### `T-RANK`

Ranking determinístico com regra de desempate explícita (maior valor primeiro; empate resolvido por ordem alfabética crescente do identificador). Usado por V4, V9, V10. Reprodutível e auditável.

### `T-ACUM`

Acumulado progressivo monotônico sobre ranking. Usado por V4 (modo 2 e 3) e V10. Requer que T-RANK esteja aplicado primeiro.

### `T-ABC`

Classificação A/B/C por limiares de acumulado. Padrão sugerido: A ≤ 80%, B ≤ 95%, C > 95%. Usado por V4 (modo 2 e 3) e V10. Regra de corte: o item que faz o acumulado atingir ou ultrapassar o limiar pertence à faixa correspondente.

### `T-PIVOT`

Pivot automático POR_LINHAS → POR_COLUNAS quando os estados estão em coluna discriminadora. Usado por V2, V3, V4. Dispara quando o motor detecta estrutura POR_LINHAS na configuração do usuário.

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

### `Tipo de campo`

Classificação técnica que determina como a V2 calcula e classifica. Do DCV-V2 e da diretriz de produto, emergem 3 ramos lógicos:

| Tipo no DCV | Comportamento lógico |
|---|---|
| Valor Monetário | Numérico aditivo — diferença + variação % |
| Quantidade | Numérico aditivo — diferença + variação % |
| Volume | Numérico aditivo — diferença + variação % |
| Percentual | Numérico relativo — análise relativa, soma vira média (W07) |
| Prazo / Tempo | Numérico aditivo — diferença + variação % |
| Índice / Score | Numérico relativo — análise relativa, soma vira média (W07) |
| Estado / Situação | Texto — sem cálculo, só "mudou/não mudou" + classificação semântica |

### `Eixo sequencial` (V3, V8)

Campo que define a sequência ordenada dos pontos analíticos. Pode ser:

- **Temporal** — datas, meses, trimestres
- **Lógico / ordinal** — etapas, ciclos, fases
- **Manual** — ordem definida pelo usuário

O motor respeita a ordem final confirmada pelo usuário (a IA pode sugerir, o usuário pode ajustar).

### `Classe ABC` (V4 modo 2 e 3, V10)

Classificação por acumulado progressivo sobre ranking decrescente. Padrão: A até 80%, B de 80% a 95%, C acima de 95%. Usado para priorização, gestão de portfólio, leitura de concentração.

---

## 6. Warnings (códigos)

Warnings são **alertas não-bloqueantes** emitidos pelo motor ou pela visão. Não são erro — são aviso para o usuário revisar.

### Warnings da V1

- **W-V1-TOL** — Tolerância absorveu diferenças em N registros classificados como Conciliado (D-018, P-V1-05)
- **W-V1-DUP** — Duplicidade em N chaves de Origem ou Comparado (P-V1-03+04)
- **W-V1-AMB** — Ambiguidade em N chaves em match não-exato produzindo múltiplos candidatos (P-V1-03+04)


### Warnings da V2 (herdados do legado, a serem confirmados no DCV-V2 refinado)

- **W01** — Mais de 20% de nulos no campo comparado, OU registros individuais com nulo em A ou B (excluídos da análise — D-004)
- **W02** — Agrupador com mais de 50 valores únicos (cardinalidade alta)
- **W03** — Mais de 3 agrupadores configurados pelo usuário
- **W04** — Registros com `valor_A=0` (coberto pelo cenário SURGIMENTO)
- **W05** — Em POR_LINHAS, registro sem contraparte no outro estado (gera SURGIMENTO ou DESAPARECIMENTO — D-001)
- **W06** — Contagem de registros classificados como SURGIMENTO/DESAPARECIMENTO em POR_LINHAS (D-001)
- **W07** — Resumo por agrupador contém campos PERCENTUAL ou INDICE — média simples aplicada em vez de soma (D-002)
- **W08** *(proposto, pendente)* — Coluna discriminadora em POR_LINHAS com mais de 2 valores (Modo 4) — usuário precisa escolher 2
- **W-AGG** *(proposto, pendente)* — Múltiplos registros para a mesma combinação de agrupadores — soma aplicada antes da comparação

### Warnings de motor

- **W-B01** — Inferência semântica detectou coluna boolean disfarçada de float64 (valores em {0,1,NaN} tratados como boolean, não numeric — D-008). Requisito herdado pela Fundação v2.

---

## 7. Decisões e infraestrutura

### `D-XXX` 📌

Numeração sequencial **global** de decisões registradas em `DECISIONS.md`. Não reinicia por visão, não reaproveita números (mesmo se uma decisão for revogada). Decisões registradas até agora: **D-001 a D-014**. A mais recente e fundacional do método atual é **D-014** (Reforma pós-DCVs).

Adicionar entradas de D-017, D-018, D-019 na linha que cita D-XXX:
Decisões registradas até agora: D-001 a D-019. A mais recente é D-019 (Padrão de condução do Arquiteto em sessões de DCV).

### `UploadResult` 🔧

Contrato Pydantic — saída padrão do `motor_upload`. Na v1 (em `/legacy/`), campos: `file_name`, `preview` (5 linhas), `arquivo_bytes` (D-007), `aba_selecionada`, `abas_disponiveis`. **Será reformulado no G-FUND** com base nos requisitos dos 10 DCVs.

### `MotorResult` 🔧

Contrato Pydantic — saída padrão do `motor_base`. Na v1, campos: DataFrame completo, `column_meta`, `warnings`. **Será reformulado no G-FUND**.

### `VNResult` 🔧

Contrato Pydantic genérico — saída padrão de cada `visao_vN`. Definido no G-FUND para manter padrão consistente entre as 10 visões.

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

### "Padrão de condução DCV" (D-019) 📌

Padrão operacional do Arquiteto em sessões de refino de DCV (blocos `DCV-VN` e `DCV-OPN`), formalizado em D-019. 10 elementos: validação de estado na abertura, fila racionalizada, uma pendência por vez com opções e trade-offs, Princípio C.5 como primeira lente, confirmação explícita antes de avançar, mini status-check a cada 3 pendências, abertura para correção de enquadramento, identificação proativa de decisões transversais, fechamento proativo, DCV final em prosa como último ato ou entregável da próxima sessão. Ver Instruções do Projeto §Padrão de condução em sessões de DCV.
---

## 11. Termos a evitar (anti-glossário)

Termos que já apareceram mas que **não devem ser usados** no método atual:

- ❌ **"Spec final"** — toda spec é potencialmente revisável; usar "spec aprovada" + data
- ❌ **"V2 está pronta"** — usar critério: DCV aprovado + Spec aprovada (com wireframe) + Base + Código + App + Validação Visual
- ❌ **"Confiar no Gamma como spec"** — Gamma é formatação de documento apresentável, nunca gerador de artefato técnico
- ❌ **"N-Motores" · "G-MOT" · "B-NR" · "V-Nb" · "N-VN" · "V-0c" · "T-XXX"** — todos descontinuados; ver seção 3
- ❌ **"Onda padrão" · "Onda futura"** — substituído por "ordem por famílias conceituais"
- ❌ **"Funcionou em teste então está pronto"** — princípios B.3 e B.4 são absolutos
- ❌ **"Esqueleto de tela"** — substituído por "wireframe funcional" (termo canônico no CONTEXT v2)

---

**Para sugerir adição ou correção neste glossário:** abrir conversa com o Arquiteto, descrever o termo e o contexto, fechar a conversa com kit de encerramento que inclui a alteração deste arquivo.
