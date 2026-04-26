# DCV-V8 · Recorrência e Ciclo de Vida

**Família B · Sequência ao longo de eixo ordenado · segunda visão da família**

**Data aprovação:** 19/04/2026 · Sessão única · 12 pendências fechadas (T-01 a T-12) · Padrão D-019 aplicado.

**Status:** Aprovado

**Substrato herdado:**
- **DCV-V3 aprovado** (19/04/2026 · D-059 a D-070 · 13 pendências) — primeira da Família B; substrato de T-EIXO, estrutura, intervalo, padrões de Resumo Executivo e warnings.
- **DCV-V11 aprovado** (19/04/2026 · D-058) — padrão par autônomo de família.
- **DCV-V4 aprovado** (19/04/2026) — padrão default declarado sistematizado + Resumo Executivo 6 blocos (D-044) + bloqueios operacionais (D-032/D-043).
- **CONTEXT.md** (v19/04/2026 pós DCV-V3) — T-EIXO formalizada (D-061), T-PIVOT três semânticas, M2.STACK candidato.

---

## 1. Propósito da visão

A V8 responde: **"quem apareceu, quem permaneceu, quem saiu, quem voltou ao longo de um eixo sequencial ordenado?"**

A visão analisa **existência e continuidade** de entidades rastreadas, não valor. Produz uma matriz de presença (Entidades × Pontos do eixo), classifica cada par em uma de 4 classes primárias (Novo, Contínuo, Retornou, Ausente) e, consolidadamente no intervalo, pode atribuir classificação adicional Constante (entidade presente em todos os pontos). Entrega Resumo Executivo narrativo do ciclo de vida observado, Matriz de Presença como coração visual, e estrutura auditável em 7 abas de Excel.

A V8 não diagnostica causa raiz, não declara que ausência é erro, não afirma que voltar é bom ou sair é ruim. Evidencia o ciclo observado; a interpretação causal cabe ao usuário.

---

## 2. Posicionamento analítico

### 2.1 O cenário real que a V8 atende

V8 atende ao uso contábil/gerencial típico de acompanhamento de **ciclo de vida de entidades** num recorte ordenado:

- **Carteira de clientes ativos** mês a mês (quem entrou, quem saiu, quem voltou após ausência).
- **Ciclo de produtos no catálogo** (SKU novo, SKU contínuo, SKU descontinuado).
- **Monitoramento de fornecedores** (relação contínua × eventual).
- **Retenção de colaboradores** (entrou, permaneceu, saiu).
- **Ciclo de contratos/apólices** renovados trimestre a trimestre.

Exemplo concreto: empresa de serviços rastreando 500 clientes mês a mês ao longo de 12 meses — quantos clientes novos entraram em junho, quantos dos de janeiro ainda estão em dezembro, quantos voltaram após ausência, quantos foram perdidos no recorte recente.

### 2.2 Relação com V6 e território analítico vizinho

V6 é **cruzamento de dois campos categóricos num universo estático** (matriz cliente × produto com ambos em linhas/colunas). V8 é **rastreamento de entidade ao longo de eixo ordenado** — presença em cada ponto, com semântica sequencial entre pontos ("mês seguinte", "fase seguinte"). V6 expõe onde há ocorrência; V8 expõe **como a ocorrência evoluiu ao longo do tempo**. O **eixo ordenado** é o que distingue — sem ordem, não há recorrência/retorno/perda.

V1/V11 (Família A · Confronto) não têm sobreposição substantiva — operam sobre duas bases; V8 opera sobre base única sequencial.

### 2.3 Relação com V3 (par autônomo da Família B)

V3 e V8 convivem como par autônomo da Família B — mesma família, problemas analíticos distintos, motores distintos, vocabulário parcialmente compartilhado via T-EIXO.

| Aspecto | V3 · Análise Sequencial | V8 · Recorrência e Ciclo de Vida |
|---|---|---|
| O que rastreia | Valor em cada ponto do eixo | Presença/ausência em cada ponto do eixo |
| Unidade analítica | Agrupador + Ponto do eixo (com valor consolidado) | Entidade + Ponto do eixo (+ Agrupadores ativos opcionais) |
| Classificação do resultado | Aumentou · Reduziu · Estável · Não aplicável (+ semântica) | Novo · Contínuo · Retornou · Ausente (por ponto) + Constante (consolidada) |
| Transversais comuns | T-EIXO · T-AGRUPA · T-DIAG · T-MODELO · T-PIVOT · T-SEMA | T-EIXO · T-AGRUPA · T-DIAG · T-MODELO · T-PIVOT (sem T-SEMA) |
| Tipo de medida | Numérica (valor, quantidade, percentual, índice) | Binária implícita (existência do registro no ponto) · medida numérica opcional apenas contextual |

**Não há substituição de uma pela outra.** O usuário escolhe conscientemente a visão pela pergunta que quer responder: "como esse valor evoluiu ao longo do tempo?" (V3) ou "essa entidade esteve presente ao longo do tempo?" (V8). A fronteira é navegada por microcopy declarativa e autossuficiente em cada visão — nenhuma das duas menciona a outra em interface operacional. Quem precisa entender ambas lê este bloco.

**Este bloco cumpre a retroação diferida registrada em D-060** (V3→V8). Paralelo à retroação V11→V1 registrada em D-058, ainda aberta para próxima revisão natural de V1.

**Observação: T-SEMA não se aplica a V8.** Presença/ausência não tem direção inerente de "melhor/pior" universal — ganhar 50 clientes e perder 30 pode ser ótimo (crescimento de carteira) ou péssimo (churn alto mascarado), depende do contexto. Decidir por default teria que decidir pelo usuário uma das duas interpretações — viola C.5. Semântica fica fora do escopo do motor V8; leitura qualitativa do resultado fica com o usuário (Bloco 5 do Resumo Executivo apresenta leitura de ciclo de vida com faixas editáveis — não semântica direcional).

### 2.4 Unidade analítica da V8

Unidade analítica da V8: combinação de **Entidade + Ponto do eixo + Agrupadores ativos** (quando há). Princípio "consolidar primeiro, classificar depois" preservado do prévio PARTE 4.3. Consolidação via T-AGRUPA aplicada sempre (independentemente do modo transacional ou pré-agregado declarado); classificação de presença (§5) aplicada após consolidação.

**Distinção entidade × agrupador:** entidade é o que está sendo rastreado (unidade primária, obrigatória, uma só por execução — cliente, produto, SKU, contrato); agrupadores são recortes opcionais pelos quais o rastreamento é segmentado (região, filial, canal). Mesma entidade pode ter classificações diferentes em grupos distintos (ex: cliente X presente em todos os meses em Sudeste, ausente nos últimos 3 em Nordeste).

---

## 3. O que a visão recebe

### 3.1 Estrutura de entrada

Uma base lógica por execução, com uma ou mais abas. O usuário escolhe **uma aba** analisada.

**Formatos suportados (dentro de uma aba):**

- **POR_COLUNAS** — cada ponto do eixo é uma coluna distinta. Exemplo: `Cliente | Jan | Fev | Mar | Abr` (valores ou presença binária nas células; vazios indicam ausência).
- **POR_LINHAS** — pontos do eixo empilhados em linhas, identificados por coluna discriminadora. Exemplo: `Cliente | Mes | Valor` com `Mes` contendo Jan, Fev, Mar, Abr (linha existe para cada ocorrência presente da entidade em cada ponto).

Para POR_LINHAS, motor aplica pivot interno via **T-PIVOT** antes da construção da matriz de presença (pivot dentro da terceira semântica formalizada em D-062: pontos do eixo).

**Base transacional plana** (`Cliente | Data | Valor_transação`) é reconhecida pelo motor como **POR_LINHAS** natural — a coluna do eixo (Data) é simultaneamente a coluna discriminadora. T-07 (§4.1) trata a distinção transacional × pré-agregada e suas implicações de consolidação; estruturalmente ambos passam pelo mesmo pivot interno.

**Estrutura declarada pelo usuário com default declarado do motor.** Motor detecta sinais na amostragem:
- Nomes de colunas reconhecíveis como "Mes", "Periodo", "Data", "Competencia", "Lote", "Etapa", "Fase" → candidatas a coluna discriminadora do eixo em POR_LINHAS.
- Coluna com N ≥ 3 valores únicos de padrão cronológico detectado pelo reconhecedor de D-026 → sinal forte de POR_LINHAS com eixo temporal.
- Múltiplas colunas com rótulos de padrão cronológico (Jan, Fev, Mar ou 01/24, 02/24, 03/24 como cabeçalhos) → sinal forte de POR_COLUNAS.

Estrutura proposta visível antes da execução, editável em um clique. **W-V8-EIXO-ESTRUTURA-INFERIDA** (informativo) registra aceitação por default sem edição.

**Bloco "Seleção de pontos do eixo em POR_LINHAS":**
- **Ativação:** quando coluna discriminadora do eixo tem **10 ou mais valores únicos** (limite configurável na Spec S-V8).
- **Conteúdo:** lista de todos os pontos únicos detectados, pré-selecionados por default (analisar todos).
- **Comportamento:** usuário pode desmarcar subset não desejado; resto segue para pivot.
- **W-V8-EIXO-PONTOS-MUITOS** (informativo) registra ativação.
- **Relação com intervalo De/Até (§4.5):** seleção prévia opera antes do pivot; De/Até opera sobre eixo já ordenado. Ambos coexistem. **W-V8-EIXO-SELECAO+INTERVALO** (informativo) registra uso combinado.

### 3.2 Fora de escopo de entrada

- **Multi-aba como eixo sequencial** (uma aba por mês, por exemplo) — **fora de escopo V8 MVP**. Microcopy no Diagnóstico (ativada quando arquivo carregado tem N ≥ 3 abas): *"Se as múltiplas abas deste arquivo representam pontos distintos do eixo sequencial e você quer analisar recorrência entre eles, consolide em uma única aba antes da análise. Versão futura (Módulo 2 · STACK) automatizará esse caminho."* Roadmap: **P-V8-01-Evo · Múltiplas abas como eixo sequencial**. Aplicação direta do padrão V3 D-063; M2.STACK candidato (D-063) ganha V8 como segunda visão consumidora futura.
- **Duas bases (T-DUAL)** — fora de escopo V8. V8 não é visão de confronto — é visão sequencial sobre base única. Herança natural da posição na Família B, sem microcopy explícita.

---

## 4. Configuração analítica

### 4.1 Modo da base (Transacional × Pré-agregado) e consolidação

**Modo declarado pelo usuário com default declarado do motor.** Motor detecta duplicidade em (Entidade, Ponto do eixo, Agrupadores ativos) na amostragem e propõe modo:

| Sinal detectado | Proposta de modo |
|---|---|
| Nenhuma duplicidade — cada combinação (Entidade, Ponto do eixo, Agrupadores ativos) aparece no máximo 1 vez | **Pré-agregado** |
| Há duplicidade — pelo menos uma combinação aparece 2+ vezes | **Transacional** (default) ou **Pré-agregado com duplicidade** (editável pelo usuário) |

Modo visível na configuração antes da execução, editável em um clique. **W-V8-MODO-INFERIDO** (informativo) registra aceitação por default. Modo é rótulo informativo — não altera mecânica de consolidação.

**Consolidação via T-AGRUPA — lógica única, aplicada sempre.** Independentemente do modo declarado:
- Motor consolida por unidade analítica **(Entidade + Ponto do eixo + Agrupadores ativos)**.
- Quando há **campo de medida opcional declarado** (§4.2): regra de agregação T-AGRUPA consolida múltiplos registros no mesmo par. 5 regras canônicas herdadas de D-026: **soma (default) · média · máximo · mínimo · contagem**. Default pode ser alterado por tipo de medida (§4.2 — relativo/não-aditivo default média).
- Quando **não há campo de medida declarado**: consolidação resolve apenas presença — múltiplos registros no mesmo par viram 1 linha presente na matriz. Regra de agregação não se aplica.

Quando usuário declara modo "pré-agregado" mas motor detecta duplicidade, **W-V8-DUPLICIDADE-PREAGREGADA** (alerta) dispara informando quantos pares têm múltiplas linhas. Usuário aceita e processa com regra escolhida; revisa a base; ou alterna modo (apenas muda rótulo).

**"Primeiro valor" do prévio V8 descartado** em favor das 5 regras T-AGRUPA canônicas. Rationale: "primeiro valor" depende de ordem de leitura — conflita com C.1 (determinismo absoluto) a menos que se declare critério de ordenação, o que reintroduz complexidade sem ganho analítico real.

**Registro no Diagnóstico e aba Parâmetros:** modo declarado · regra de agregação declarada (quando há medida) · linhas originais vs linhas após consolidação · lista de pares com múltiplas linhas consolidadas (quando houver, até limite de exibição).

### 4.2 Campo de medida opcional

**Papel analítico.** Medida é **opcional** e **contextual** — enriquece leitura sem alterar classificação. Aparece na Base Analítica e no Histórico de Presença quando há presença; fica vazia/não aplicável quando há ausência. **Nunca convertida automaticamente em zero.**

**Tipos de medida herdados de D-025 com tratamento adaptado:**

| Tipo | Tratamento V8 | Warning |
|---|---|---|
| **Aditivo** (valor monetário, quantidade, volume) | Execução normal sem aviso. Consolidação com default soma. | — |
| **Relativo** (percentual, taxa, índice normalizado) | Execução com default declarado: regra de agregação default **média** em vez de soma. Usuário pode alterar. | **W-V8-MEDIDA-RELATIVA** (informativo) |
| **Não-aditivo** (score, média já calculada, índice) | Execução com default declarado: regra de agregação default **média**. Alerta de que valor é contextual. | **W-V8-MEDIDA-NAO-ADITIVA** (informativo) |
| **Estado/situação** (categórico — Ativo, Inativo, Cancelado) | Execução com alerta. Valor exibido como categórico na Base Analítica — não agregável. Regra de agregação T-AGRUPA não se aplica; motor exibe primeira ocorrência do par consolidado (ou concatenação — Spec S-V8 decide). | **W-V8-MEDIDA-CATEGORICA** (alerta) |

**Default declarado sobre tipo.** Motor detecta tipo na amostragem (herdando heurísticas D-025/D-036 e reconhecedor de D-026); propõe tipo + tratamento; usuário confirma ou edita em um clique. **W-V8-MEDIDA-TIPO-DECL** (informativo) registra aceitação por default.

**Negativos — não se aplicam a V8.** V8 não calcula Diferença nem Variação % sobre medida. Valores negativos aparecem na Base Analítica como vieram da base original (ou consolidados por T-AGRUPA). Nenhum tratamento específico, nenhum warning. Divergência com V3 (que trata negativos via D-066) justificada pelo padrão "herança adaptada à natureza analítica" (T-06).

**Nulos na medida.** Quando há presença da entidade no ponto mas a medida está nula, motor **preserva o nulo** na Base Analítica (não converte em zero, não exclui a linha). Presença é determinada pela existência do registro, independente da medida estar preenchida. **W-V8-MEDIDA-NULO-COM-PRESENCA** (informativo) registra quantidade de casos.

**Observação sobre estado/situação como medida:** o redirecionamento V8/V6 de D-066 (V3) refere-se à **análise principal** quando a medida é categórica — o usuário quer rastrear "Status do cliente ao longo do tempo", o que V8 atende por natureza (presença com Status como contexto). Usar estado/situação como medida dentro de V8 é funcionalmente distinto (enriquecer Base Analítica com categoria ao lado da presença) e fica permitido com alerta.

### 4.3 Eixo sequencial — tipos, estrutura e ordenação

**Três tipos canônicos de eixo** (herança integral T-EIXO · D-061):

| Tipo | O que é | Como o motor detecta | Ordem default |
|---|---|---|---|
| **Temporal** | Eixo com semântica de tempo (data, mês, ano, período) | Reconhecedor de padrões cronológicos pt-BR/pt-EN herdado de D-026 (T-AGRUPA): datas ISO, datas pt-BR, nomes de meses em português e inglês, anos, tokens Q1/Q2/Q3/Q4, formatos "Jan/24", "2024-01" | Cronológica crescente |
| **Lógico/ordinal** | Eixo com ordem declarada no rótulo (etapas, níveis, fases, lotes numerados) | Prefixo ou sufixo numérico no rótulo (ex: "Etapa 1: Kickoff", "Fase 3", "Lote 7", "1º Trimestre") | Pelo prefixo/sufixo numérico crescente; quando não detectado, alfabética crescente |
| **Manual** | Eixo sem ordem inerente detectável | Fallback quando nenhum padrão acima é detectado | Ordem de primeira ocorrência na base original |

**Tipo declarado pelo usuário com default declarado do motor.** Motor detecta padrões na amostragem e propõe tipo; tipo proposto visível antes da execução, editável em um clique. Quando detecção falha, default é "manual". Quando múltiplos padrões são detectados simultaneamente, prioridade: temporal > lógico/ordinal > manual. **W-V8-EIXO-TIPO-INFERIDO** (informativo) registra aceitação por default.

**Ordem final sempre confirmada pelo usuário.** Motor sugere ordem conforme tipo; usuário pode reordenar manualmente (mecânica de UI para Spec S-V8 — drag-and-drop ou equivalente). Reordenação manual sobre eixo temporal ou ordinal dispara **W-V8-EIXO-ORDEM-MANUAL** (informativo).

**Herança de D-026 (T-AGRUPA):** T-EIXO consome o reconhecedor de padrões cronológicos pt-BR/pt-EN de T-AGRUPA. Mesmo mecanismo que ordena cronologicamente em V2/V4 e serve ao tipo temporal em V3. Zero duplicação.

### 4.4 Lacuna do eixo × Ausência da entidade no ponto × Granularidade mista

V8 distingue **três fenômenos estruturalmente diferentes**:

**(a) Lacuna do eixo (macroscópica) — herdada de V3.** Ponto ausente no universo consolidado como um todo. Detecção automática depende do tipo de eixo:

| Tipo de eixo | Detecção automática | Referência |
|---|---|---|
| Temporal | Sim | Sequência canônica derivada do padrão detectado |
| Lógico/ordinal com prefixo numérico | Sim | Sequência 1, 2, 3, ..., N |
| Lógico/ordinal sem prefixo numérico | Não | Sem referência semântica |
| Manual | Não | Ordem é declaração, não inferência |

Quando detecção feita, lista de pontos ausentes vai ao Diagnóstico (categoria AJUSTE_LEVE) e dispara **W-V8-EIXO-LACUNA** (informativo). Densidade alta: **W-V8-EIXO-LACUNA-MASSIVA** (alerta, não bloqueio) dispara quando > 30% dos pontos esperados estão ausentes. Threshold 30% configurável na Spec S-V8.

**Impacto analítico:** matriz de presença usa apenas os pontos existentes do eixo efetivo. Auditoria textual na Base Analítica pode indicar "entre Fev e Mai o eixo tem lacuna" para contexto do leitor.

**(b) Ausência da entidade no ponto (microscópica) — conteúdo analítico primário da V8.** Entidade sem ocorrência em ponto específico do eixo efetivo, classificada pela taxonomia §5.2:
- **Ausente** — ausente no ponto atual, presente em pelo menos um ponto anterior dentro do intervalo.
- Entidade ausente em **todos** os pontos do intervalo efetivo dentro de um grupo **não ocupa linha** na matriz daquele grupo (economia de matriz).

Diferença substantiva com V3 (D-065): em V3 "ausência do agrupador em ponto" era flag informativa (`ausencia_ponto`, AJUSTE_LEVE); em V8 é **conteúdo analítico primário**, classificado, contado e exibido. **Sem warning** — motor está fazendo exatamente o que a visão pede. Padrão "o que é warning em uma visão pode ser conteúdo em outra" cristalizado aqui (ver GLOSSARIO §10).

**(c) Granularidade mista no eixo (específica de eixo temporal) — alerta forte com confirmação obrigatória.** Detecção automática quando motor identifica 2 ou mais granularidades distintas na coluna do eixo temporal (mistura de datas diárias e rótulos mensais; mistura de mensal e trimestral; mistura de diário e semanal).

Comportamento:
- Motor exibe alerta visual na configuração com amostra dos valores detectados em cada granularidade.
- Usuário é obrigado a confirmar explicitamente antes de prosseguir ("Confirmo analisar com granularidade mista — entendo que isso pode inflar cardinalidade de pontos e produzir classificações inesperadas").
- Após confirmação, motor processa com os rótulos como estão (sem correção automática — C.5).
- **W-V8-EIXO-GRANULARIDADE-MISTA** (alerta) registra confirmação.

Alternativas orientativas exibidas no próprio alerta:
- Corrigir na base antes de carregar.
- Usar M2.NORMALIZE quando disponível (roadmap futuro).
- Aceitar com confirmação e processar com os rótulos atuais.

Para eixos lógico/ordinal e manual, "granularidade mista" não se aplica (não há referência de granularidade em eixos não-temporais) — sem warning.

### 4.5 Intervalo De/Até

**Papel analítico.** De/Até define o subset de pontos do eixo que entra na construção da matriz de presença. Aplicado **após** pivot (§3.1) e ordenação do eixo (§4.3). Entidades ausentes em todos os pontos do intervalo efetivo **não ocupam linha** na matriz (economia de matriz — §4.4b).

**Default declarado.** Campo **De** preenchido com o primeiro ponto da base consolidada (ordem conforme tipo de eixo); campo **Até** preenchido com o último ponto. Ambos visíveis na configuração antes da execução, editáveis em um clique. **W-V8-INTERVALO-DEFAULT** (informativo) registra aceitação sem edição.

**Intervalo declarado vs intervalo efetivo** — preservados separadamente (herança V3 D-064). Declarado persiste em T-MODELO e aba Parâmetros; efetivo é o que o motor aplicou após ajustes-limite. Quando diferirem, Diagnóstico registra ambos; aba Parâmetros lista lado a lado.

**Mínimos operacionais em V8:**

| Cenário | Comportamento | Rationale |
|---|---|---|
| Intervalo efetivo < 2 pontos | **Bloqueio operacional** — **W-V8-PONTOS-MIN** | Com 1 ponto só, toda entidade é Novo e não há comparação; resultado analiticamente vazio |
| Intervalo efetivo = 2 pontos | **Executa com alerta** — **W-V8-PONTOS-LIMITADO** (alerta) | Classificação válida estruturalmente (Novo/Contínuo/Retornou/Ausente no ponto 2); leitura de ciclo de vida limitada |
| Intervalo efetivo ≥ 3 pontos | Execução normal, sem alerta | Leitura completa do ciclo (entrada, continuidade, retorno, perda, consolidação Constante) |

**Divergência com V3** (que bloqueia em < 3): V3 calcula variação entre pares (precisa de 3+ para leitura de tendência); V8 classifica presença no ponto (conteúdo válido a partir de 2). Aplicação do padrão **"herança adaptada à natureza analítica"** formalizado na sessão V8 (ver GLOSSARIO §10).

**Comportamentos-limite:**

| Cenário | Comportamento | Categoria T-DIAG | Warning |
|---|---|---|---|
| De < primeiro ponto disponível | Ajuste para primeiro ponto disponível | AJUSTE_LEVE | **W-V8-INTERVALO-AJUSTE-INICIO** |
| Até > último ponto disponível | Ajuste para último ponto disponível | AJUSTE_LEVE | **W-V8-INTERVALO-AJUSTE-FIM** |
| De > Até (invertido) | Bloqueio operacional | — | **W-V8-INTERVALO-INVALIDO** |
| Intervalo efetivo < 2 pontos | Bloqueio operacional | — | **W-V8-PONTOS-MIN** |
| Intervalo efetivo = 2 pontos | Execução com alerta | — | **W-V8-PONTOS-LIMITADO** |
| De = Até | Bloqueio pelo mínimo 2 pontos | — | **W-V8-PONTOS-MIN** |

**Persistência em T-MODELO.** Modelo persiste intervalo declarado (não o efetivo, que depende da base do momento). Ao aplicar modelo em base diferente, ajustes-limite podem disparar naturalmente — comportamento já coberto pelo padrão AJUSTE_LEVE.

### 4.6 Agrupadores (opcionais)

Quando usuário declara agrupadores, toda lógica de classificação é recalculada **dentro de cada grupo separadamente**. Mesma entidade pode ser classificada diferentemente em grupos distintos.

**Escala progressiva herdada V3/V4 com ajuste V8:**

| N° agrupadores | Comportamento |
|---|---|
| 1-3 | Normal, sem aviso |
| 4-5 | Aviso + estimativa de linhas em tempo real |
| 6 | Confirmação obrigatória extra (**W-V8-AGRUP-MUITOS-CONFIRMA**, alerta) |
| 7+ | **Bloqueio** (**W-V8-AGRUP-MUITOS**) com sugestão: "para cruzamento multidimensional considere V6 ou V9; para análise de recorrência, reduza dimensões" |

Corte um passo mais conservador que V3 (V3 bloqueia em 8+): em V8 agrupadores multiplicam grupos únicos, que multiplicam matriz (N grupos × entidades × pontos).

**Colisões bloqueadas:**

| Cenário | Warning | Rationale |
|---|---|---|
| Mesmo campo declarado como eixo e entidade | **W-V8-EIXO-ENTIDADE-COLISAO** | Rastreamento circular (entidade rastreada ao longo de si mesma) |
| Mesmo campo declarado como agrupador e entidade | **W-V8-AGRUP-ENTIDADE-COLISAO** | Segmentação circular (entidade segmentada por si mesma) |
| Mesmo campo declarado como eixo e agrupador | **W-V8-EIXO-AGRUP-COLISAO** | Herança V3 D-070 |

Motor não corrige silenciosamente — pede ajuste do usuário.

### 4.7 Modelo de configuração (T-MODELO)

Herda padrão D-030: persiste **configuração lógica**, nunca dado. Persiste: entidade declarada, eixo + tipo + ordem confirmada, estrutura (POR_COLUNAS/POR_LINHAS), seleção prévia de pontos se aplicada, intervalo declarado, modo (transacional/pré-agregado), regra de agregação quando aplicável, agrupadores com rótulos, tipo da medida declarado (quando há), ordem da matriz se editada, faixas de leitura descritiva se editadas. Não persiste: arquivo bruto, aba, filtros pós-execução, resultado anterior, dados sensíveis.

V8 é **visão autônoma** (não forma par de view especializada com nenhuma outra visão). Modelos V8 são aplicáveis apenas em V8. V8 não participa do padrão cross-visão (D-046) — diferente de V4 Modo 2 ↔ V10.

---

## 5. Lógica de processamento

### 5.1 Ordem canônica de cálculo

1. Upload → UploadResult.
2. Seleção de aba → MotorResult.
3. Sugestão da IA para preenchimento da configuração.
4. Confirmação da entidade.
5. Confirmação do eixo sequencial (tipo + ordem).
6. Confirmação da estrutura (POR_COLUNAS/POR_LINHAS).
7. Seleção prévia de pontos (se ativada).
8. Pivot interno via T-PIVOT (se POR_LINHAS).
9. Confirmação do modo (transacional/pré-agregado).
10. Confirmação do campo de medida opcional + tipo + regra de agregação (se aplicável).
11. Confirmação dos agrupadores (se houver).
12. Confirmação do intervalo De/Até.
13. Validações de colisão (eixo × entidade, agrupador × entidade, eixo × agrupador).
14. Aplicação de ajustes-limite do intervalo + registro declarado vs efetivo.
15. Pré-validação de volume (entidades × pontos × grupos).
16. Consolidação T-AGRUPA por (Entidade, Ponto do eixo, Agrupadores).
17. Construção da matriz de presença.
18. Classificação por ponto (Novo/Contínuo/Retornou/Ausente).
19. Cálculo das métricas por entidade (taxa de presença, primeiro/último ponto, sequência máxima, classificação atual).
20. Classificação consolidada do intervalo (Constante, quando aplicável).
21. Filtragem de entidades 100% ausentes por grupo (economia de matriz).
22. Ordenação tripla da matriz (classificação atual → taxa de presença → alfabética).
23. Geração do V8Result.
24. Renderização em tela.
25. Exportação para Excel.

### 5.2 Classificação por ponto do eixo (4 classes)

| Classe | Condição formal |
|---|---|
| **Novo** | Presente no ponto atual · sem presença em nenhum ponto anterior dentro do intervalo efetivo |
| **Contínuo** | Presente no ponto atual · presente no ponto imediatamente anterior (comparação consecutiva) |
| **Retornou** | Presente no ponto atual · ausente no ponto imediatamente anterior · presente em pelo menos um ponto anterior dentro do intervalo |
| **Ausente** | Ausente no ponto atual · presente em pelo menos um ponto anterior dentro do intervalo |

**Entidade ausente em todos os pontos do recorte efetivo** (quando aparece só em outros grupos) não ocupa linha na matriz daquele grupo.

**Entidade presente no primeiro ponto do intervalo efetivo** = **Novo** (sem histórico anterior dentro do intervalo). Entidade ausente no primeiro ponto que aparecerá depois não tem classificação nesse primeiro ponto (não aparece na matriz daquele ponto até sua primeira ocorrência).

### 5.3 Classificação consolidada do intervalo

| Classe consolidada | Condição |
|---|---|
| **Constante** | Entidade presente em **todos** os pontos do intervalo efetivo |
| (não aplicável) | Qualquer outro padrão — campo `classificacao_consolidada` = Null |

Classes consolidadas adicionais (Intermitente, Decrescente, Sazonal) ficam como **P-V8-02-Evo**.

### 5.4 Classificação atual da entidade

**Classificação atual = classificação da entidade no último ponto do intervalo efetivo.** Rótulo para uso no Resumo Executivo (Bloco 3) e microcopy executiva.

### 5.5 Vocabulário dual técnico/exibição

| Contrato técnico | Exibição ao usuário |
|---|---|
| `NOVO` | Novo |
| `CONTINUO` | Contínuo |
| `RETORNOU` | Retornou |
| `AUSENTE` | Ausente |
| `CONSTANTE` | Constante |

Padrão consolidado em V2/V4 preservado. Contratos técnicos em maiúsculas; exibição capitalizada natural.

**Termos descartados** do prévio V8: "Recorrente" (→ Contínuo), "Recuperado" (→ Retornou), "Perdido" (→ Ausente). Podem sobreviver em microcopy de produto como contexto explicativo ("análise de perdas" = filtro sobre Ausente), nunca no contrato do motor. "Ativa/Inativa" permanecem **não oficiais** (prévio explicita).

---

## 6. O que a visão entrega

### 6.1 Estrutura do resultado (V8Result)

**Granularidade-base da V8:**

| Visão | Granularidade | Conteúdo |
|---|---|---|
| **Visão periódica** | 1 linha por (Entidade, Ponto do eixo, Agrupadores ativos) | Presença/ausência · classificação por ponto · valor da medida opcional quando há presença |
| **Visão consolidada** | 1 linha por (Entidade, Agrupadores ativos) | Quantidade de pontos presentes/ausentes · taxa de presença · primeiro/último ponto · sequência máxima de continuidade · classificação atual · classificação consolidada do intervalo |

**Contrato `matriz_celula` no V8Result:**

- **Presente com classificação por ponto:** `{"presente": true, "classe": "NOVO" | "CONTINUO" | "RETORNOU", "medida": valor | null}`
- **Ausente com histórico prévio:** `{"presente": false, "classe": "AUSENTE", "medida": null}`
- **Ponto anterior à primeira aparição:** `{"presente": false, "classe": null, "medida": null}` — entidade ainda não entrou no intervalo; célula vazia sem classificação.

Representação visual concreta (pontos, cores, símbolos) fica para **Spec S-V8** — DCV define apenas contrato lógico.

**Campos principais do V8Result:**

| Campo | Descrição |
|---|---|
| `entidade` | Rótulo declarado |
| `ponto_eixo` | Ponto do eixo (visão periódica) |
| `agrupadores` | Combinação dos agrupadores ativos |
| `presente` | bool |
| `classificacao_ponto` | NOVO · CONTINUO · RETORNOU · AUSENTE · null |
| `classificacao_consolidada` | CONSTANTE · null (só preenchida na visão consolidada) |
| `classificacao_atual` | Classificação no último ponto do intervalo efetivo |
| `medida_valor` | Valor consolidado da medida opcional (null quando ausência ou nulo) |
| `taxa_presenca` | % de pontos presentes sobre pontos do intervalo efetivo (visão consolidada) |
| `primeiro_ponto` · `ultimo_ponto` | Primeiros e últimos pontos de presença no intervalo (visão consolidada) |
| `sequencia_max_continuidade` | Maior sequência contígua de presença (visão consolidada) |

### 6.2 Matriz de Presença

**Estrutura lógica:**
- **Linhas:** entidades do recorte ativo (uma linha por entidade × grupo quando há agrupadores).
- **Colunas:** pontos do eixo do intervalo efetivo (ordem conforme tipo do eixo + ordem confirmada).
- **Células:** contrato lógico do §6.1.

**Matriz aninhada por grupo.** Quando há agrupadores ativos, estrutura hierárquica: para cada grupo único (combinação dos agrupadores ativos), uma matriz (entidades × pontos) independente. Mesma entidade em grupos diferentes pode ter classificações diferentes. Mecânica de UI (aba por grupo, expandir/colapsar, grupo dominante, etc.) para Spec S-V8.

**Ordenação da matriz em 3 níveis:**

1. **Primária — por classificação atual da entidade**, default declarado: **Constante → Contínuo → Retornou → Novo → Ausente**. Editável em um clique (drag-and-drop, menu, Spec S-V8 decide). **W-V8-MATRIZ-ORDEM-CUSTOM** (informativo) registra edição.
2. **Secundária — taxa de presença decrescente** dentro de cada classe. Fixa, não configurável.
3. **Terciária — alfabética da entidade** (desempate C.1). Fixa.

**Rationale do default primário:** começa pelas entidades mais estáveis (Constante) e termina pelas que requerem atenção (Ausente — saídas recentes). Leitura narrativa "quem ficou → quem entrou → quem voltou → quem estreou → quem saiu".

**Paginação:** threshold padrão **100 entidades por página** (configurável na Spec S-V8). Base com ≤ 100: exibe tudo em página única. Base com > 100: paginação obrigatória. **W-V8-MATRIZ-PAGINACAO** (informativo) registra ativação.

**Escala de cardinalidade de entidades:**

| N entidades por grupo | Comportamento | Warning |
|---|---|---|
| 1-100 | Normal | — |
| 100-500 | Paginação | W-V8-MATRIZ-PAGINACAO |
| 500-2000 | Paginação + alerta | **W-V8-ENTIDADES-MUITAS** (alerta) |
| 2000-10.000 | Confirmação obrigatória | **W-V8-ENTIDADES-CRITICO** (alerta forte) |
| 10.000+ | **Bloqueio** | **W-V8-ENTIDADES-INVIAVEL** |

### 6.3 Resumo Executivo — 6 blocos fixos

Estrutura herdada D-044 (V4/V11/V3) adaptada V8:

**Bloco 1 · Cabeçalho**
Nome da visão, base analisada (arquivo + aba), entidade rastreada, eixo sequencial (nome + tipo), intervalo declarado (e efetivo se diferiu), agrupadores ativos (se há), campo de medida opcional (se há).

**Bloco 2 · Números-âncora**
Total de entidades analisadas · Total de pontos do eixo no intervalo efetivo · Taxa média de presença (%) · N de entidades Constantes · N de entidades com classificação atual = Ausente no último ponto.

**Bloco 3 · Distribuição de classificações no último ponto**
Novo · Contínuo · Retornou · Ausente — contagem e percentual da distribuição das entidades na classificação atual (último ponto efetivo). Linha adicional para Constante no intervalo (classificação consolidada). Quando há agrupadores ativos, distribuição também por grupo.

**Bloco 4 · Elementos destacados**
Top 5 maior continuidade · Top 5 presença mais irregular · Top 5 Novas no último ponto · Top 5 Ausentes no último ponto (churn recente) · grupo com maior e menor taxa média de presença (quando há agrupadores).

**Bloco 5 · Leitura descritiva do ciclo de vida (faixas editáveis)**

| Leitura | Condição default | Rationale |
|---|---|---|
| **Estável** | > 60% das entidades têm classificação consolidada Constante OU têm taxa de presença ≥ 80% | Maioria com presença consistente |
| **Rotativa** | Entidades Novas no último ponto + Ausentes no último ponto ≥ 30% do total | Alta dinâmica de entrada/saída recente |
| **Em retração** | Ausentes no último ponto > Novas em fator ≥ 1.5 | Saídas substantivamente maiores que entradas |
| **Em expansão** | Novas no último ponto > Ausentes em fator ≥ 1.5 | Entradas substantivamente maiores que saídas |
| **Mista** | Nenhuma das acima se aplica isoladamente | Ciclo heterogêneo sem leitura dominante |

Thresholds (60%, 80%, 30%, 1.5) **editáveis** em "Configurações avançadas". **W-V8-LEITURA-DEFAULT** (informativo) registra aceitação; **W-V8-LEITURA-CUSTOM** (informativo) registra edição.

**Nota estática final do Bloco 5:** *"Para análise aprofundada de padrões de entrada/saída por segmento de grupo ou cruzamento multidimensional, considere V6 (cruzamento de categóricos) ou V9 (ranking multidimensional)."* Microcopy declarativa — não redireciona silenciosamente.

**Bloco 6 · Qualidade estrutural**
Quantidade de ajustes leves (AJUSTE_LEVE do Diagnóstico) · quantidade de alertas · presença de lacunas do eixo (quantidade + densidade %) · presença de granularidade mista (flag + confirmação do usuário) · duplicidade em base pré-agregada (quando houve) · modo declarado · regra de agregação quando aplicável.

### 6.4 Exportação Excel — 7 abas oficiais

| # | Aba | Conteúdo |
|---|---|---|
| 1 | **Resumo Executivo** | 6 blocos do §6.3 |
| 2 | **Matriz de Presença** | Matriz entidade × ponto do eixo com classificações por célula; aninhada por grupo quando há agrupadores |
| 3 | **Histórico de Presença** | Visão periódica: 1 linha por (Entidade, Ponto do eixo, Agrupadores); todas as classificações por ponto + medida opcional |
| 4 | **Resumo por Entidade** | Visão consolidada: 1 linha por (Entidade, Agrupadores); taxa, primeiro/último, sequência máxima, classificação atual/consolidada |
| 5 | **Movimentações** | Entidades que mudaram de classificação no último ponto: novas entradas, retornadas, ausentes recentes; agrupadores quando há |
| 6 | **Parâmetros** | Configuração declarada vs efetiva: entidade, eixo (tipo declarado + efetivo), estrutura, intervalo declarado/efetivo, modo, regra de agregação, agrupadores ativos, tipo da medida, ordem da matriz, faixas de leitura editadas |
| 7 | **Diagnóstico** | Todos os warnings disparados + categoria T-DIAG (AJUSTE_LEVE / DECISAO_USUARIO) + quantidade de linhas originais vs consolidadas + lista de lacunas detectadas + confirmação de granularidade mista quando houve — **sempre última aba (D-017)** |

**Dados Brutos do prévio V8 descartada** — Base Analítica dos dois tipos de visão (periódica em aba 3, consolidada em aba 4) cobre a auditoria analítica; dados brutos normalizados são parte do upload, não da visão V8. Diagnóstico registra "linhas originais: X, linhas consolidadas: Y" para auditoria.

**Aba "Entidades Ausentes no Último Período" do prévio V8 descartada** (prévio PARTE 10.4 já registrou a rejeição) — conteúdo absorvido pela aba Movimentações + classificação Ausente na aba Histórico de Presença.

**Filtros ativos em todas as 7 abas** (padrão D-017). **Tela e Excel não divergem** (princípio D-017 + PARTE 10.1 do prévio).

### 6.5 Leitura executiva principal

A leitura oficial da V8 segue a ordem:

1. Presença e ausência ao longo do eixo (Matriz de Presença como âncora).
2. Classificação atual das entidades (último ponto do intervalo).
3. Estabilidade e recorrência no intervalo (indicadores de continuidade e taxa de presença).
4. Destaques de entrada, retorno e perda (entidades Novas, Retornadas, Ausentes no último ponto).

---

## 7. Warnings catalogados (37)

Warnings V8 em 3 categorias.

### 7.1 Bloqueios (9)

| # | Warning | Condição |
|---|---|---|
| 1 | **W-V8-INTERVALO-INVALIDO** | De > Até |
| 2 | **W-V8-PONTOS-MIN** | Intervalo efetivo < 2 pontos |
| 3 | **W-V8-EIXO-ENTIDADE-COLISAO** | Mesmo campo declarado como eixo e entidade |
| 4 | **W-V8-AGRUP-ENTIDADE-COLISAO** | Mesmo campo declarado como agrupador e entidade |
| 5 | **W-V8-EIXO-AGRUP-COLISAO** | Mesmo campo declarado como eixo e agrupador |
| 6 | **W-V8-AGRUP-MUITOS** | 7+ agrupadores declarados |
| 7 | **W-V8-VOLUME-INVIAVEL** | Células totais (entidades × pontos × grupos) > 1.000.000 |
| 8 | **W-V8-ENTIDADES-INVIAVEL** | Entidades por grupo > 10.000 |
| 9 | **W-V8-PONTOS-INVIAVEL** | Pontos do eixo efetivo > 200 |

### 7.2 Alertas (10)

| Warning | Condição |
|---|---|
| **W-V8-PONTOS-LIMITADO** | Intervalo efetivo = 2 pontos |
| **W-V8-DUPLICIDADE-PREAGREGADA** | Duplicidade detectada em modo declarado pré-agregado |
| **W-V8-MEDIDA-CATEGORICA** | Campo de medida do tipo estado/situação |
| **W-V8-EIXO-LACUNA-MASSIVA** | > 30% dos pontos esperados ausentes (só eixos com detecção ativa) |
| **W-V8-EIXO-GRANULARIDADE-MISTA** | 2+ granularidades distintas em eixo temporal |
| **W-V8-ENTIDADES-MUITAS** | 500-2000 entidades por grupo |
| **W-V8-ENTIDADES-CRITICO** | 2000-10.000 entidades por grupo |
| **W-V8-VOLUME-ALTO** | 100.000-500.000 células totais |
| **W-V8-VOLUME-CRITICO** | 500.000-1.000.000 células totais |
| **W-V8-AGRUP-MUITOS-CONFIRMA** | 6 agrupadores declarados (antes do bloqueio em 7+) |

### 7.3 Informativos (18)

| Warning | Condição |
|---|---|
| **W-V8-EIXO-TIPO-INFERIDO** | Tipo de eixo aceito por default sem edição |
| **W-V8-EIXO-ORDEM-MANUAL** | Ordem manual aplicada sobre eixo temporal/ordinal |
| **W-V8-EIXO-ESTRUTURA-INFERIDA** | Estrutura POR_COLUNAS/POR_LINHAS aceita por default |
| **W-V8-EIXO-PONTOS-MUITOS** | Bloco de seleção de pontos ativado (10+ valores únicos) |
| **W-V8-EIXO-SELECAO+INTERVALO** | Seleção prévia combinada com De/Até |
| **W-V8-INTERVALO-DEFAULT** | De/Até aceitos por default sem edição |
| **W-V8-INTERVALO-AJUSTE-INICIO** | De declarado anterior ao primeiro ponto; ajustado |
| **W-V8-INTERVALO-AJUSTE-FIM** | Até declarado posterior ao último ponto; ajustado |
| **W-V8-MODO-INFERIDO** | Modo (transacional/pré-agregado) aceito por default |
| **W-V8-MEDIDA-TIPO-DECL** | Tipo de medida aceito por default |
| **W-V8-MEDIDA-RELATIVA** | Medida tipo relativo detectada; default de agregação alterado para média |
| **W-V8-MEDIDA-NAO-ADITIVA** | Medida tipo não-aditivo detectada; default de agregação alterado para média |
| **W-V8-MEDIDA-NULO-COM-PRESENCA** | N registros com presença + valor nulo na medida |
| **W-V8-EIXO-LACUNA** | Lacunas detectadas no eixo (só eixos com detecção ativa) |
| **W-V8-MATRIZ-ORDEM-CUSTOM** | Ordem da matriz editada pelo usuário |
| **W-V8-MATRIZ-PAGINACAO** | Paginação ativa (> 100 entidades por grupo) |
| **W-V8-LEITURA-DEFAULT** | Faixas de leitura de ciclo de vida aceitas por default |
| **W-V8-LEITURA-CUSTOM** | Faixas de leitura de ciclo de vida editadas |

**Total: 37 warnings V8.**

---

## 8. Diretrizes de performance

Herança V3 (D-070) adaptada V8:

1. **Pré-validação de intervalo antes do processamento pesado** — se intervalo efetivo < 2 ou colisões detectadas, bloquear antes do pivot.
2. **Pré-cálculo vetorizado da matriz de presença** — operação numpy/pandas sobre DataFrame consolidado, não loop por entidade.
3. **Detecção de volume total antes da construção da matriz** — estimativa rápida (entidades × pontos × grupos); se > threshold crítico, bloquear/confirmar antes de alocar memória.
4. **Lazy rendering da Matriz em tela** — renderizar apenas entidades da página corrente.
5. **Exportação Excel em streaming** — abas pesadas (Histórico de Presença, Matriz de Presença) escritas em streaming (openpyxl write-only mode) quando volume > 100.000 linhas.
6. **Índices pré-calculados para tops** — top 5 maior continuidade, top 5 mais irregulares (Resumo Executivo Bloco 4) calculados uma vez na finalização, cached.
7. **Ausência total otimizada** — entidades 100% ausentes em grupo filtradas cedo no pipeline (antes da construção da matriz), não no fim.

---

## 9. Fronteira com Módulo 2 (TabloPrep)

V8 opera sobre **uma base lógica, uma aba**. Transformações prévias são território do M2:

- **M2.STACK** (candidato · D-063) — empilhamento de múltiplas abas estruturalmente idênticas em única aba com coluna discriminadora. Dependência de P-V8-01-Evo. V8 é segunda visão consumidora futura (junto com V3).
- **M2.NORMALIZE** (candidato · D-057) — normalização textual e de granularidade. Solução orientativa para W-V8-EIXO-GRANULARIDADE-MISTA quando conteúdo exige normalização de rótulos mistos (ex: consolidar "15/03/2024" em "Mar/2024").
- **M2.RESHAPE** (candidato) — transformação POR_LINHAS ↔ POR_COLUNAS quando estrutura nativa da base não é adequada ao motor.

Microcopy no Diagnóstico quando aplicável orienta sobre caminhos futuros sem bloquear o MVP.

---

## 10. Pontos de atenção (riscos analíticos conhecidos)

- **Classificação "Novo" no primeiro ponto do intervalo efetivo** não implica que a entidade "começou" naquele ponto — apenas que ela não tem histórico anterior **dentro do intervalo recortado**. Base pode ter ocorrências da entidade antes do De que foram excluídas pelo recorte. Auditoria via aba Parâmetros (intervalo declarado vs efetivo).
- **Granularidade mista confirmada pelo usuário** pode produzir classificações inesperadas — mesma entidade presente em "Mar/2024" e "15/03/2024" conta como dois pontos distintos se não for normalizada. Alerta forte com confirmação obrigatória (W-V8-EIXO-GRANULARIDADE-MISTA) serve como sinalização. Correção via M2.NORMALIZE futuro ou ajuste manual da base.
- **Economia de matriz** pode esconder entidade que só aparece em grupos específicos — quando há agrupadores ativos, entidade ausente em todos os pontos de um grupo não ocupa linha daquele grupo. Se usuário quer ver "quais entidades existem no universo total mas não neste grupo", V6 (cruzamento) é o caminho.
- **Classes consolidadas adicionais** (Intermitente, Decrescente, Sazonal) ficaram como P-V8-02-Evo. Padrões de recorrência periódica não são detectados no MVP — base de 12 meses com entidade presente em Jan-Fev-Ago-Dez não é classificada como "Sazonal" no resultado.
- **Campo de medida opcional não afeta classificação** — se o usuário carrega base com medida "Receita" esperando que "valor zero" seja tratado diferentemente de "valor nulo" no ciclo de vida, a expectativa é errada. Presença é binária: existência do registro. Valor é contextual.

---

## 11. Relação com Fundação e retroação sobre V3

### 11.1 Requisitos novos para a Fundação

- **T-EIXO consumido integralmente** — V8 é segunda consumidora (primeira V3). Sem requisitos novos para T-EIXO; V8 herda o que foi formalizado em D-061.
- **T-PIVOT terceira semântica (pontos do eixo)** consumida — V8 é segunda consumidora (primeira V3). Sem requisitos novos.
- **T-AGRUPA com 5 regras canônicas** consumido condicionalmente (apenas quando há medida opcional declarada). Sem requisito novo.
- **Contrato V8Result** consolidado (§6.1) com `matriz_celula` estruturado, `classificacao_ponto`, `classificacao_consolidada`, `classificacao_atual`, `medida_valor`.
- **F-EXP capability adicional:** Matriz de Presença como aba dedicada com aninhamento por grupo (não comum a outras visões); aba Movimentações específica V8; exportação em streaming quando volume alto.
- **F-MOT capability adicional:** pré-validação de volume antes de alocação de matriz; lazy rendering da matriz; detecção de granularidade mista em eixo temporal.

### 11.2 Retroação sobre V3 — cumprimento de D-060

O §2.3 deste DCV **cumpre integralmente a retroação diferida registrada em D-060**. DCV-V3 §2.3 antecipou taxonomia V8 com "a confirmar em DCV-V8" — esta sessão **confirma** Novo · Contínuo · Retornou · Ausente + Constante, sem ajuste cosmético pendente. DCV-V3 aprovado pode ter §2.3 atualizado no kit (retirar "a confirmar") — ajuste cosmético, não substantivo.

---

## 12. Roadmap pós-MVP (P-V8-XX-Evo)

- **P-V8-01-Evo · Múltiplas abas como eixo sequencial** — implementação via extensão análoga a T-DUAL mas sequencial (N abas = N pontos do eixo). Dependência: M2.STACK implementada (caminho preferencial) ou extensão dedicada no motor_upload (caminho direto). Registrado em T-05.
- **P-V8-02-Evo · Classificações consolidadas adicionais** — além de Constante, explorar "Intermitente" (presença irregular), "Decrescente" (taxa de presença em queda), "Sazonal" (padrão periódico detectado). Ficou fora do MVP por opção conservadora (T-03); evolução quando uso real validar demanda.
- **P-V8-03-Evo · Reordenação manual de entidades na Matriz** — drag-and-drop individual além da ordenação automática em 3 níveis. Caso de uso: analista quer destacar entidade específica no topo da leitura. Mecânica complexa para matrizes com 500+ entidades; pós-MVP.
- **P-V8-04-Evo · Sazonalidade e tendência de presença** — camada analítica avançada: detectar padrão periódico em séries de presença/ausência (ex: cliente aparece sempre no quarto trimestre). Território potencial de IA assistiva (Fase 3). Não vinculante.
- **P-V8-05-Evo · Intervalo médio entre aparições como métrica própria** — prévio PARTE 6.7 mencionou como "métrica complementar opcional". MVP não incorporou para manter escopo enxuto; fica como evolução com requisito de contrato específico.

---

## 13. Nomenclatura oficial da V8

Termos consolidados no refino (vocabulário canônico da V8):

- **Entidade** — unidade rastreada (cliente, produto, SKU, fornecedor, contrato, colaborador)
- **Eixo Sequencial** — dimensão pela qual a análise ordena os pontos
- **Tipo do Eixo** — temporal · lógico/ordinal · manual (herdado D-061)
- **Ponto do eixo** — cada valor único do eixo após pivot e ordenação (vocabulário canônico D-061)
- **Coluna discriminadora do eixo** — em POR_LINHAS, coluna que identifica qual ponto cada linha representa
- **Agrupador** — dimensão opcional de segmentação do rastreamento (vocabulário canônico TabloFlow D-025)
- **Modo da base** — Transacional · Pré-agregado (rótulo informativo, lógica de consolidação única)
- **Presença** — existência de pelo menos uma ocorrência válida da entidade no ponto
- **Ausência** — não existência de ocorrência da entidade no ponto
- **De · Até** — limites do intervalo configurado
- **Intervalo declarado** — o que o usuário configurou (persiste em T-MODELO)
- **Intervalo efetivo** — o que o motor aplicou após ajustes-limite
- **Classificação por ponto** — Novo · Contínuo · Retornou · Ausente (4 classes primárias)
- **Classificação consolidada** — Constante (ou não aplicável) no intervalo completo
- **Classificação atual** — classificação da entidade no último ponto do intervalo efetivo
- **Matriz de Presença** — representação bidimensional entidade × ponto do eixo com classificações por célula
- **Taxa de presença** — % de pontos presentes sobre pontos do intervalo efetivo
- **Sequência máxima de continuidade** — maior sequência contígua de presença da entidade no intervalo
- **Lacuna do eixo** — ponto ausente no universo consolidado (macroscópica, herdada V3)
- **Ausência da entidade no ponto** — conteúdo analítico primário V8 (classificação Ausente)
- **Granularidade mista no eixo** — duas ou mais granularidades distintas detectadas em eixo temporal
- **Leitura de ciclo de vida** — síntese qualitativa do Bloco 5 do Resumo Executivo (Estável · Rotativa · Em retração · Em expansão · Mista)
- **Movimentações** — aba dedicada V8: entidades que mudaram de classificação no último ponto

**Termos descartados do prévio V8** (registrados no anti-glossário GLOSSARIO §11):
- "Período" → **Ponto do eixo** (termo canônico genérico)
- "Recorrente" → **Contínuo** (no motor)
- "Recuperado" → **Retornou** (no motor)
- "Perdido" → **Ausente** (no motor)
- "Primeiro valor" (como regra de agregação) → descartado em favor das 5 regras T-AGRUPA canônicas
- "Ativa/Inativa" permanecem **não oficiais** (prévio já explicita)

---

## 14. Posicionamento C.5

A V8 foi refinada integralmente sob a lente do princípio C.5 (TabloFlow analisa sobre o dado informado, nunca decide por ele). Manifestações concretas:

- **Três tipos de eixo com default declarado** — motor detecta padrões e propõe; usuário confirma ou edita (§4.3).
- **Estrutura POR_COLUNAS/POR_LINHAS com default declarado** — motor detecta e propõe; usuário confirma ou edita (§3.1).
- **Modo da base com default declarado** — motor detecta duplicidade e propõe; usuário confirma ou edita (§4.1).
- **Intervalo De/Até com default declarado** — motor propõe primeiro/último ponto; usuário confirma ou edita (§4.5).
- **Tipo de medida opcional com default declarado** — motor detecta e propõe tratamento por tipo; usuário confirma (§4.2).
- **Regra de agregação com default declarado variável por tipo** — soma default para aditivo; média default para relativo e não-aditivo (§4.1 + §4.2).
- **Ordem da matriz com default declarado editável** — inversão da decisão do prévio V8 (que propunha ordem fixa) em favor de default declarado com edição em um clique (§6.2).
- **Granularidade mista — alerta com confirmação obrigatória, nunca correção silenciosa** — motor não "conserta" granularidade (§4.4c).
- **Ausência é classificação, não warning** — motor não interpreta causa; classifica e exibe (§4.4b · §5.2).
- **T-SEMA fora de escopo V8** — presença/ausência não tem direção universal; motor não decide "melhor/pior" (§2.3).
- **"Primeiro valor" descartado** — opção do prévio que conflitaria com C.1; substituída por 5 regras T-AGRUPA canônicas explícitas (§4.1).
- **Mínimo de 2 pontos como alerta, não bloqueio** — V8 executa com alerta; usuário decide se a leitura de 2 pontos é suficiente (§4.5).

**Padrões de método novos cristalizados na sessão V8:**
- **Herança adaptada à natureza analítica** (T-06 / §4.5) — visões da mesma família herdam o que cabe à sua lógica; divergência justificada V3 (bloqueia em < 3) × V8 (alerta em < 3, bloqueia em < 2).
- **O que é warning em uma visão pode ser conteúdo em outra** (T-09 / §4.4) — "ausência do agrupador em ponto" é warning em V3, conteúdo analítico primário em V8.

Ambos padrões registrados no GLOSSARIO §10 como padrões de método consolidados.

---

## 15. Integração com Fundação

### 15.1 Transversais consumidos

- **T-EIXO** — consumo integral (D-061). Zero requisito novo.
- **T-AGRUPA** — consumo condicional (apenas quando há medida opcional). 5 regras canônicas.
- **T-PIVOT** — consumo pela terceira semântica (pontos do eixo, D-062). Zero requisito novo.
- **T-DIAG** — consumo integral. Aba última (D-017).
- **T-MODELO** — consumo integral. Persiste configuração lógica; V8 autônoma (sem cross-visão).

### 15.2 Transversais não aplicáveis a V8

- **T-SEMA** — presença/ausência não tem direção universal (§2.3). CONTEXT §6 atualizado com nota.
- **T-DUAL** — V8 opera sobre base única. Sem consumo.
- **T-RANK** — V8 não produz ranking (taxa de presença secundária da matriz é ordenação, não ranking). Sem consumo.
- **T-ACUM** · **T-ABC** — V8 não opera sobre acumulados ou classificação ABC. Sem consumo.
- **T-FUZZY** — V8 opera sobre rótulos declarados; sem match textual aproximado. Sem consumo.
- **T-CONCAT** — V8 opera sobre entidades declaradas; sem composição de campos. Sem consumo.

### 15.3 Diretrizes de performance

7 diretrizes formalizadas em §8.

---

## 16. Decisões geradas

| # | Tema | Referência |
|---|---|---|
| T-01 | Vocabulário canônico V8 (Ponto do eixo, Entidade, Agrupador) | §13 (consolidação terminológica, não gera D-XXX) |
| T-02 | Posicionamento Família B + retroação D-060 cumprida + T-SEMA fora V8 | **D-071** · §2 |
| T-03 | Taxonomia oficial por ponto (Novo · Contínuo · Retornou · Ausente) + Constante | **D-072** · §5.2, §5.3 |
| T-04 | Herança T-EIXO integral | §4.3 (aplicação D-061, não gera D-XXX) |
| T-05 | Estrutura POR_COLUNAS/POR_LINHAS + seleção de pontos + multi-aba fora MVP | §3 (aplicação D-062/D-063, não gera D-XXX) |
| T-06 | Intervalo De/Até + mínimo 2 pontos + padrão "herança adaptada" | **D-073** · §4.5 |
| T-07 | Modo Transacional × Pré-agregado + consolidação única T-AGRUPA + 5 regras | **D-074** · §4.1 |
| T-08 | Medida opcional + tipos + negativos não aplicáveis | **D-075** · §4.2 |
| T-09 | Lacuna × Ausência × Granularidade mista + padrão "warning vs conteúdo" | **D-076** · §4.4 |
| T-10 | Matriz de Presença + ordenação default editável + paginação + aninhamento | **D-077** · §6.2 |
| T-11 | Resumo Executivo 6 blocos + Excel 7 abas + Dados Brutos descartada | **D-078** · §6.3, §6.4 |
| T-12 | Bloqueios operacionais + performance + roadmap P-V8-XX-Evo | **D-079** · §4.6, §6.2, §7, §8, §12 |
| — | Sumário do refino DCV-V8 | **D-080** · este documento completo |

**Total: 10 decisões D-XXX** (D-071 a D-080).

---

## 17. Pendências do refino (histórico)

12 pendências originais trabalhadas em sessão única (T-01 a T-12). Todas fechadas, nenhuma deferida.

**Ordem de tratamento seguindo o padrão D-019:**

**Bloco A · Posicionamento e fronteira:** T-01 · T-02 · T-03.
**Bloco B · Eixo e intervalo (herança T-EIXO):** T-04 · T-05 · T-06.
**Bloco C · Dados da visão:** T-07 · T-08 · T-09.
**Bloco D · Saída e operação:** T-10 · T-11 · T-12.

Mini status-checks conduzidos após T-04, T-07 e T-09 (sinalização de densidade D-034 aplicada no terceiro). Densidade avaliada como média-alta, continuação em sessão única aprovada pela Usuária.

---

## 18. Referências

- CONTEXT.md v19/04/2026 — T-EIXO formalizada em §6, Famílias em §4.
- DECISIONS.md — D-058 (retroação diferida V11→V1), D-060 (Família B V3×V8 com retroação), D-061 (T-EIXO formalizada), D-062 (T-PIVOT terceira semântica), D-063 (M2.STACK candidato), D-064 (intervalo V3), D-065 (lacunas eixo × agrupador V3), D-066 (tipos de medida V3), D-069 (Resumo Executivo V3 + 7 abas), D-070 (bloqueios V3).
- DCV-V3 aprovado — padrão canônico da Família B, substrato de herança.
- DCV-V11 aprovado — padrão par autônomo de família.
- DCV-V4 aprovado — padrão default declarado consolidado + Resumo Executivo 6 blocos (D-044).
- GLOSSARIO.md — vocabulário canônico; §5.V8 nova com ~22 entradas; §6 Warnings V8 com 37 entradas; §10 ganha 2 padrões de método novos.
