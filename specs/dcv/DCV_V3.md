# DCV-V3 · Análise Sequencial

**Visão:** V3 · Análise Sequencial
**Módulo:** Módulo 1 · TabloAnálise
**Família:** B · Sequência ao longo de eixo ordenado
**Status:** Aprovado
**Data da aprovação:** 19/04/2026
**Sessão de refino:** 1 (sessão única, 13 pendências fechadas)
**Arquivo canônico:** `/specs/dcv/dcv_v3.md`

---

## 1. Propósito da visão

A V3 acompanha como um valor se comporta ao longo de um eixo sequencial ordenado. Responde "como isso evoluiu?" para uma medida numérica segmentada por agrupadores analíticos, ponto a ponto na sequência declarada.

A V3 responde quatro perguntas, nessa ordem de leitura:

1. **Como a medida evoluiu em cada ponto do eixo?** (Trajetória consolidada por agrupador)
2. **Qual foi a variação entre pontos consecutivos?** (Diferença e Variação % por par)
3. **Como classificar essa variação semanticamente?** (Melhorou/Piorou/Estável/Apenas informar conforme semântica declarada da medida)
4. **Qual a tendência ou aderência predominante na sequência?** (Síntese qualitativa sobre o intervalo efetivo)

A V3 é a **primeira visão da Família B · Sequência** e a **primeira consumidora de T-EIXO** da Fundação. Decisões tomadas neste DCV vinculam V8 por herança direta (T-EIXO, vocabulário de tipos de eixo, tratamento de estruturas POR_COLUNAS/POR_LINHAS, mecânica de intervalo De/Até, detecção de lacunas).

A V3 opera sobre uma base consolidada única e aplica o princípio estrutural "consolidar primeiro, calcular depois" (P0.6 do prévio, preservado): pontos do eixo e agrupadores são consolidados via regra de agregação declarada antes de qualquer cálculo de Diferença ou Variação.

---

## 2. Posicionamento analítico

### 2.1 O cenário real que a V3 atende

O cenário típico da V3 é a análise de evolução numérica em rotinas financeiras, contábeis, comerciais e operacionais brasileiras:

- **Receita mensal por centro de custo** ao longo de 12 ou 24 meses
- **Saldo por competência** em contas contábeis ou cliente/fornecedor
- **Volume de vendas por semana** ou por produto em recorte temporal
- **Evolução de KPI operacional** (throughput, taxa de conversão, tempo médio) por quinzena ou mês
- **Custo por etapa** de processo sequencial (projeto, produção, onboarding)
- **Headcount por mês** em plano de crescimento ou reestruturação
- **Número de ocorrências** (chamados, incidentes, aprovações) por período

Em todos esses cenários, o analista humano hoje recorre a gráfico de linha no Excel, Power BI ou tabela dinâmica. A V3 estrutura esse trabalho, preserva a regra analítica declarada (consolidação, semântica, intervalo), e entrega artefato Excel auditável com síntese consolidada.

### 2.2 Relação com V2, V4 e V8

**V3 × V2 (Família A).** V2 confronta dois estados fixos — Orçado × Realizado de um mês, Jan/24 × Jan/25 de uma métrica. V3 acompanha múltiplos pontos ordenados. A pergunta da V2 é "o que mudou entre esses dois pontos?"; a da V3 é "como isso evoluiu ao longo da sequência?". Quando o usuário tem 3 ou mais pontos para analisar, V3 é o caminho natural; com 2 pontos, V2.

**V3 × V4 (Família C).** V4 analisa a forma de um total em um momento específico — como um valor se distribui entre elementos (produto, cliente, centro), sem movimento temporal. V3 analisa como um mesmo recorte se comporta ao longo do tempo. Pergunta da V4: "como esse total está composto agora?". Pergunta da V3: "como esse valor variou ao longo da sequência?". As duas visões convivem em análises complementares: V4 para foto, V3 para filme.

**V3 × V8 (Família B).** A distinção V3 × V8 dentro da Família B está detalhada na §2.3.

### 2.3 Relação com V8 (par autônomo da Família B)

V3 e V8 convivem como par autônomo da Família B — mesma família, problemas analíticos distintos, motores distintos, vocabulário parcialmente compartilhado via T-EIXO.

| Aspecto | V3 · Análise Sequencial | V8 · Recorrência e Ciclo de Vida |
|---|---|---|
| O que rastreia | Valor em cada ponto do eixo | Presença/ausência em cada ponto do eixo |
| Unidade analítica | Agrupador + Ponto do eixo (com valor consolidado) | Agrupador + Ponto do eixo (com status de presença) |
| Classificação do resultado | Aumentou · Reduziu · Estável · Não aplicável (+ semântica: Melhorou/Piorou/Estável/Apenas informar) | Novo · Contínuo · Ausente · Retornou *(a confirmar em DCV-V8)* |
| Transversais comuns | T-EIXO · T-AGRUPA · T-DIAG · T-MODELO · T-PIVOT | T-EIXO · T-AGRUPA · T-DIAG · T-MODELO |
| Tipo de medida | Numérica (valor monetário, quantidade, percentual, índice) | Binária implícita (existência do registro no ponto) |

**Não há substituição de uma pela outra.** O usuário escolhe conscientemente a visão pela pergunta que quer responder: "como esse valor evoluiu ao longo do tempo?" (V3) ou "essa entidade esteve presente ao longo do tempo?" (V8). A fronteira é navegada por microcopy declarativa e autossuficiente em cada visão — nenhuma das duas menciona a outra em interface operacional. Quem precisa entender ambas lê este bloco no DCV. DCV-V8 receberá bloco "Relação com V3" equivalente na próxima revisão (retroação diferida registrada — análoga a V11 retroação sobre V1).

### 2.4 Unidade analítica da V3

Unidade analítica da V3: combinação de **Agrupador + Ponto do eixo**, com valor consolidado pela regra de agregação declarada. Princípio "consolidar primeiro, calcular depois" preservado do prévio P0.6. Consolidação usa T-AGRUPA com regra configurável (soma default); pontos do eixo consolidados após pivot (se POR_LINHAS) e ordenação conforme tipo de eixo declarado.

---

## 3. O que a visão recebe

### 3.1 Estrutura de entrada

Uma base lógica por execução, com uma ou mais abas. O usuário escolhe **uma aba** analisada.

**Formatos suportados (dentro de uma aba):**

- **POR_COLUNAS** — cada ponto do eixo é uma coluna distinta. Exemplo: `Agrupador | Jan | Fev | Mar | Abr`.
- **POR_LINHAS** — pontos do eixo empilhados em linhas, identificados por coluna discriminadora. Exemplo: `Agrupador | Mes | Valor` com `Mes` contendo Jan, Fev, Mar, Abr.

Para POR_LINHAS, motor aplica pivot interno via **T-PIVOT** antes do cálculo sequencial.

**Estrutura declarada pelo usuário com default declarado do motor:**

- Motor detecta sinais na amostragem (nomes de colunas reconhecíveis como "Mes", "Periodo", "Data", "Competencia"; coluna com N ≥ 3 valores de padrão cronológico detectado pelo reconhecedor de D-026) e propõe estrutura.
- Estrutura proposta visível antes da execução, editável em um clique.
- **W-V3-EIXO-ESTRUTURA-INFERIDA** registra aceitação por default sem edição.

**Bloco "Seleção de pontos do eixo em POR_LINHAS":**

- **Ativação:** quando coluna discriminadora do eixo tem **10 ou mais valores únicos** (limite configurável na Spec S-V3).
- **Conteúdo:** lista de todos os pontos únicos detectados, pré-selecionados por default (analisar todos).
- **Comportamento:** usuário pode desmarcar subset não desejado; resto segue para pivot.
- **W-V3-EIXO-PONTOS-MUITOS** registra ativação do bloco.
- **Relação com intervalo De/Até (§4.6):** seleção prévia opera antes do pivot; De/Até opera sobre eixo já ordenado. Ambos coexistem. **W-V3-EIXO-SELECAO+INTERVALO** registra uso combinado.

### 3.2 Fora de escopo de entrada

**Múltiplas abas estruturalmente idênticas representando períodos distintos** (ex: uma aba por mês) permanecem fora de escopo da V3 MVP. O cenário é reconhecido e frequente em exportações de ERP brasileiras, mas exige transformação estrutural prévia (empilhamento de abas em uma única estrutura com coluna discriminadora adicional). V3 MVP aceita uma aba única — o usuário consolida os dados antes da análise. Caminho evolutivo registrado em **P-V3-01-Evo** (implementação nativa na V3) e **M2.STACK** (operação candidata do Módulo 2).

Quando o arquivo carregado tem N ≥ 3 abas, a etapa de seleção de aba exibe nota informativa orientativa: *"Se as múltiplas abas deste arquivo representam períodos distintos e você quer analisar evolução entre elas, consolide em uma única aba antes da análise. Versão futura (Módulo 2 · STACK) automatizará esse caminho."* Nota não bloqueia; apenas orienta.

---

## 4. Configuração analítica

A V3 segue o padrão estrutural de produto do CONTEXT §13 (fluxo de etapas progressivas com dependência). O número exato de etapas é decidido no wireframe funcional da Spec S-V3. As **decisões analíticas** que o wireframe respeitará são as seis declarações do usuário descritas nesta seção.

### 4.1 Modo da análise

Dois modos, mutuamente exclusivos por execução:

- **Modo Simples** — um único núcleo (campo principal) acompanhado ao longo da sequência. Pergunta: "como este valor evoluiu ponto a ponto?". Exemplos: valor por mês, saldo por competência, volume por semana.
- **Modo Comparativo** — dois núcleos (Origem e Comparado) confrontados em cada ponto da sequência. Pergunta: "como Comparado se posiciona em relação a Origem ao longo da sequência?". Exemplos: Realizado vs Orçado por mês, Meta vs Realizado por semana.

### 4.2 Campo principal ou núcleos

**Modo Simples:** seleção do **Campo Principal** (a medida analisada).

**Modo Comparativo:** seleção de dois núcleos (**Núcleo Origem** e **Núcleo Comparado**). A comparação central da V3 Comparativa é Comparado − Origem em cada ponto, com classificação semântica herdada de V2 (§5.4).

**Nomeação dos núcleos:** defaults "Origem" e "Comparado", ambos editáveis pelo usuário. Nomes escolhidos aparecem em todos os artefatos produzidos.

### 4.3 Tipo da medida e tratamento por tipo

A V3 herda a taxonomia de **4 tipos de medida consolidada em D-025**:

| Tipo | Comportamento na V3 |
|---|---|
| **Numérico aditivo** (valor monetário, quantidade, saldo, custo, volume) | Executa sem aviso. Diferença e Variação % diretamente aplicáveis |
| **Numérico relativo** (percentual, índice, score) | **Default declarado** com 3 opções: "analisar mesmo assim" (default) · "escolher outra medida" · "agregar por média ponderada antes" (disponível só em Modo Simples; exige campo de peso) |
| **Numérico não-aditivo** | Idêntico ao relativo |
| **Estado/Situação** (categórico) | **Bloqueio operacional com redirecionamento**: "Análise sequencial de valor não se aplica a campos categóricos. Use V8 (Recorrência e Ciclo de Vida) para rastrear trajetória de presença, ou V6 (Relacionamento entre Dimensões) para cruzamento." |

**Modo Comparativo com tipo relativo:** opção "agregar por média ponderada" desativada (comparação é ponto-a-ponto, sem agregação entre pontos). Opções "analisar mesmo assim" e "escolher outra medida" permanecem disponíveis.

**Tipo declarado pelo usuário com default declarado do motor:** motor propõe baseado em heurística de nome de campo e distribuição de valores (compartilhada com V2/V4); valor visível antes da execução, editável em um clique. **W-V3-TIPO-DECL** registra aceitação por default sem edição. **W-V3-TIPO-REL** registra opção do usuário quando tipo relativo/não-aditivo. **W-V3-TIPO-INCOMPAT** é o bloqueio de estado/situação.

**Tratamento de negativos (padrão V4 adaptado para natureza evolutiva da V3 — 2 opções):**

Motor detecta negativos na amostragem após definição da medida; apresenta bloco declarado na configuração:

1. **Analisar com valores líquidos** (default) — soma algébrica preservada; Diferença e Variação % com sinal natural.
2. **Usar valor absoluto** — `|valor|` substitui o valor na análise; sinal preservado em coluna complementar da Base Analítica.

Opção "separar análise em positivos e negativos" da V4 **não se aplica à V3** (V3 analisa evolução por agrupador, não composição sobre universo; separar quebra a sequência do agrupador). **W-V3-NEGATIVOS** registra opção + contagem.

**Tratamento de nulos na medida:**

Registro com valor nulo é preservado na listagem com classificação `NULO_MEDIDA`. Nulo não entra no cálculo — Diferença e Variação % entre ponto com valor e ponto com nulo são registrados como `None` ou "—" no Excel. Se o nulo está entre dois pontos válidos (ex: Jan=100, Fev=nulo, Mar=120), comparação consecutiva salta: Mar vs Jan. Relacionado ao mecanismo de ausência do agrupador em ponto (§4.5). **W-V3-NULL** (informativo) registra contagem; **W-V3-NULL-MASS** (alerta) dispara quando > 20% dos registros têm nulo na medida.

**Contrato `classificacao_medida` da V3:**

| Contrato técnico | Exibição ao usuário |
|---|---|
| `VALOR_VALIDO` | (omitido — caso normal) |
| `VALOR_NEGATIVO` | "Valor negativo" (quando Opção 2 de negativos foi usada) |
| `NULO_MEDIDA` | "Valor nulo na medida" |

Vocabulário idêntico a V4 para consistência entre visões numéricas.

### 4.4 Eixo sequencial — tipos, estrutura e ordenação

**Três tipos canônicos de eixo** declarados na configuração:

| Tipo | O que é | Como o motor detecta | Ordem default |
|---|---|---|---|
| **Temporal** | Eixo com semântica de tempo (data, mês, ano, período) | Reconhecedor de padrões cronológicos pt-BR/pt-EN herdado de D-026 (T-AGRUPA): datas ISO, datas pt-BR, nomes de meses em português e inglês, anos, tokens Q1/Q2/Q3/Q4, formatos "Jan/24", "2024-01" | Cronológica crescente |
| **Lógico/ordinal** | Eixo com ordem declarada no rótulo (etapas, níveis, fases) | Prefixo ou sufixo numérico no rótulo (ex: "Etapa 1: Proposta", "Fase 3", "1º Trimestre") | Pelo prefixo/sufixo numérico crescente; quando não detectado, alfabética crescente |
| **Manual** | Eixo sem ordem inerente detectável | Fallback quando nenhum padrão acima é detectado | Ordem de primeira ocorrência na base original |

**Tipo declarado pelo usuário com default declarado do motor.** Motor detecta padrões na amostragem e propõe tipo; tipo proposto visível antes da execução, editável em um clique. Quando detecção falha, default é "manual". Quando múltiplos padrões são detectados simultaneamente, prioridade: temporal > lógico/ordinal > manual. **W-V3-EIXO-TIPO-INFERIDO** registra aceitação por default.

**Ordem final sempre confirmada pelo usuário.** Motor sugere ordem conforme tipo; usuário pode reordenar manualmente (drag-and-drop ou equivalente — decisão de UI da Spec S-V3). Reordenação manual sobre eixo temporal/ordinal dispara **W-V3-EIXO-ORDEM-MANUAL** (informativo) — auditoria quando ordem não-canônica produz resultado inesperado.

**Herança de D-026 (T-AGRUPA):** T-EIXO consome o reconhecedor de padrões cronológicos pt-BR/pt-EN de T-AGRUPA. O mesmo mecanismo que ordena cronologicamente em V2, V4 e demais visões que consolidam serve ao tipo temporal do eixo em V3 e V8. Zero duplicação.

### 4.5 Lacunas no eixo — detecção e tratamento

A V3 distingue dois fenômenos:

**Lacuna do eixo (macroscópica)** — ponto ausente no universo consolidado como um todo. Detecção automática depende do tipo de eixo:

| Tipo de eixo | Detecção automática | Referência |
|---|---|---|
| Temporal | Sim | Sequência canônica derivada do padrão detectado |
| Lógico/ordinal com prefixo numérico | Sim | Sequência 1, 2, 3, ..., N |
| Lógico/ordinal sem prefixo numérico | Não | Sem referência semântica |
| Manual | Não | Ordem é declaração, não inferência |

Quando detecção feita, lista de pontos ausentes vai ao Diagnóstico (categoria AJUSTE_LEVE) e dispara **W-V3-EIXO-LACUNA** (informativo).

**Ausência do agrupador em ponto (microscópica)** — agrupador específico sem valor em ponto específico, enquanto outros agrupadores têm valor lá. Detecção automática independe do tipo de eixo (comparação, para cada agrupador, entre pontos presentes e conjunto total do eixo efetivo). Vai ao Diagnóstico (AJUSTE_LEVE) e dispara **W-V3-AGRUP-AUSENCIA-PONTO**.

**Impacto analítico — zero no cálculo, visibilidade sim.** Lacunas não preenchem zero nem criam pontos artificiais (P0 do prévio preservado). Cálculo segue a ordem dos pontos válidos disponíveis — comparação consecutiva naturalmente pula lacunas (Fev → Mai quando Mar e Abr ausentes).

**Duas flags estruturais no resultado:**

| Flag | Significado |
|---|---|
| `lacuna_anterior` | Verdadeiro quando o ponto imediatamente anterior (na sequência canônica do eixo) está ausente |
| `ausencia_ponto` | Verdadeiro quando o agrupador tem pelo menos um ponto ausente dentro do intervalo efetivo, no registro seguinte à ausência |

Flags produzem coluna textual informativa na Base Analítica ("Ponto anterior ausente no eixo" ou "Ausência anterior do agrupador"). Não afetam cálculos de Diferença, Variação, Classificação.

**Densidade — alerta sem bloqueio.** **W-V3-EIXO-LACUNA-MASSIVA** (alerta) dispara quando > 30% dos pontos esperados no eixo temporal ou ordinal com prefixo numérico estão ausentes. Não bloqueia; apenas sinaliza ao usuário que base pode estar degradada. Eixo manual e ordinal sem prefixo nunca disparam este warning (sem referência). Threshold 30% configurável na Spec S-V3.

### 4.6 Intervalo De/Até

**Papel analítico.** De/Até define o subset de pontos do eixo que entra no cálculo da análise sequencial. Aplicado **após** pivot (§4.4) e ordenação do eixo. Agrupadores ausentes em todos os pontos do intervalo não aparecem no resultado. Comparação consecutiva dentro do intervalo segue a ordem dos pontos disponíveis neste subset.

**Default declarado.** Campo **De** preenchido com o primeiro ponto da base consolidada (ordem conforme tipo de eixo); campo **Até** preenchido com o último ponto. Ambos visíveis na configuração antes da execução, editáveis em um clique. **W-V3-INTERVALO-DEFAULT** registra aceitação sem edição.

**Intervalo declarado vs intervalo efetivo.** Intervalo declarado é o que o usuário configurou (preservado em T-MODELO e aba Parâmetros). Intervalo efetivo é o que o motor aplicou após eventuais ajustes-limite. Quando diferirem, Diagnóstico registra ambos; aba Parâmetros lista lado a lado.

**Comportamentos-limite:**

| Cenário | Comportamento | Categoria T-DIAG | Warning |
|---|---|---|---|
| De < primeiro ponto disponível | Ajuste para primeiro ponto disponível | AJUSTE_LEVE | **W-V3-INTERVALO-AJUSTE-INICIO** |
| Até > último ponto disponível | Ajuste para último ponto disponível | AJUSTE_LEVE | **W-V3-INTERVALO-AJUSTE-FIM** |
| De > Até (invertido) | Bloqueio operacional | — | **W-V3-INTERVALO-INVALIDO** |
| Intervalo efetivo < 3 pontos | Bloqueio operacional | — | **W-V3-PONTOS-MIN** |
| De = Até | Bloqueio pelo mínimo 3 pontos | — | **W-V3-PONTOS-MIN** |

**Relação com mínimo de 3 pontos (P0.7 do prévio).** O mínimo aplica-se ao intervalo efetivo após pivot, seleção prévia de pontos e De/Até. Se qualquer operação reduz o universo efetivo abaixo de 3, bloqueio dispara.

**Persistência em T-MODELO.** Modelo persiste intervalo declarado (não o efetivo, que depende da base do momento). Ao aplicar modelo em base diferente, ajustes-limite podem disparar naturalmente — comportamento já coberto pelo padrão AJUSTE_LEVE.

### 4.7 Agrupadores

Os agrupadores são as dimensões pelas quais a evolução é segmentada (produto, cliente, centro, categoria, filial, conta contábil). A V3 adapta a escala progressiva de D-027/V4 para sua natureza (granularidade agrupador × ponto multiplica linhas):

| N° agrupadores | Comportamento |
|---|---|
| 1-3 | Normal, sem aviso |
| 4-5 | Aviso + estimativa de linhas em tempo real |
| 6-7 | Confirmação obrigatória extra (**W-V3-AGRUP-MUITOS**) |
| 8+ | **Bloqueio** com sugestão: "para cruzamento multidimensional considere V6 ou V9; para análise sequencial, reduza dimensões" |

Corte mais conservador que V4 (V4 bloqueia em 9+): V3 multiplica linhas por pontos do eixo, amplificando impacto de cardinalidade alta.

**Colisão eixo × agrupador.** Mesmo campo declarado simultaneamente como eixo e agrupador é bloqueio operacional **W-V3-EIXO-AGRUP-COLISAO**. Motor não corrige silenciosamente (não tem base para decidir qual das declarações é a correta) — pede ajuste do usuário.

### 4.8 Semântica da medida (T-SEMA) e evolução complementar (Modo Comparativo)

**Semântica da medida (T-SEMA consumido por V2, V3, V7, V9).** Usuário declara: **maior-é-melhor · menor-é-melhor · neutro**. Motor propõe default declarado baseado em heurística de nome de campo (compartilhada com V2); editável em um clique. **W-V3-SEMA-DECL** registra aceitação por default; **W-V3-SEMA-CUSTOM** registra edição.

**Semântica é da medida, não da direção da comparação** (princípio V2 preservado). Exemplo: "Realizado > Orçado" em Receita é positivo; "Realizado > Orçado" em Custo é negativo — a diferença está na natureza da medida.

**Evolução complementar de Origem e Comparado no Modo Comparativo.** Opção declarada na configuração (seção "Configurações avançadas" ou equivalente na Spec S-V3). **Default: desligada.** Quando ligada, Base Analítica ganha duas colunas adicionais "Evolução Origem (ponto anterior)" e "Evolução Comparado (ponto anterior)"; aba Comparação entre Referências Consecutivas (dentro da Base Analítica) ganha leitura de evolução individual. Não afeta classificação semântica principal (que é sempre sobre o par Origem vs Comparado no ponto). **W-V3-COMP-EVOLUCAO** registra ligação.

### 4.9 Regra de agregação (T-AGRUPA)

Múltiplos registros podem cair no mesmo par (agrupador, ponto do eixo). Regra de agregação declarada pelo usuário consolida antes do cálculo:

- Soma (default)
- Média
- Máximo
- Mínimo
- Contagem (quando aplicável)

Aplicada via T-AGRUPA.

### 4.10 Modelo de configuração (T-MODELO)

Herda padrão D-030: persiste **configuração lógica**, nunca dado. Persiste: modo, campo principal ou núcleos, tipo da medida declarado, semântica declarada, eixo + tipo + ordem confirmada, estrutura (POR_COLUNAS/POR_LINHAS), seleção prévia de pontos se aplicada, intervalo declarado, agrupadores com rótulos, regra de agregação, opções declaradas para tipo relativo/não-aditivo e negativos, evolução complementar se ligada, faixas de leitura descritiva se editadas. Não persiste: arquivo bruto, aba, filtros pós-execução, resultado anterior, dados sensíveis.

---

## 5. Lógica de processamento

### 5.1 Ordem canônica de cálculo

A V3 segue ordem determinística (princípio C.1), preservando ordem do prévio PARTE 6 com ajustes do refino:

1. Upload (motor_upload)
2. Normalização estrutural inicial (motor_base)
3. Seleção da aba pelo usuário
4. Configuração completa (modo, medida, tipo, semântica, eixo, estrutura, agrupadores, intervalo, regras)
5. Seleção prévia de pontos em POR_LINHAS (se ativada, §3.1)
6. Pivot POR_LINHAS → POR_COLUNAS (T-PIVOT, se aplicável)
7. Consolidação por agrupadores + ponto do eixo (T-AGRUPA com regra de agregação declarada)
8. Ordenação do eixo conforme ordem final confirmada pelo usuário
9. Aplicação do intervalo De/Até (§4.6)
10. Cálculo sequencial por agrupador (Diferença, Variação %, classificação estrutural)
11. Aplicação da semântica (classificação semântica via T-SEMA)
12. Geração da saída final (V3Result)

Essa ordem é preservada para evitar divergência entre tela, motor e Excel.

### 5.2 Cálculo sequencial — Modo Simples

Para cada combinação de agrupadores, ao longo do eixo ordenado dentro do intervalo efetivo:

- `valor` = valor consolidado no ponto
- `valor_anterior` = valor consolidado no ponto consecutivo anterior (ou None se não existir na sequência)
- `diferenca` = valor − valor_anterior (ou None se valor_anterior é None ou se há lacuna intervindo)
- `variacao_pct` = diferenca / valor_anterior (regra de divisão por zero: valor_anterior = 0 e valor ≠ 0 → None/"não aplicável"; ambos = 0 → 0%)
- `classificacao_estrutural` ∈ {AUMENTOU, REDUZIU, ESTAVEL, NAO_APLICAVEL} (tolerância 1e-9 absoluto para ESTAVEL, herança T-RANK D-041)

### 5.3 Cálculo sequencial — Modo Comparativo

Para cada combinação de agrupadores, em cada ponto do eixo ordenado dentro do intervalo efetivo:

- `valor_origem` = valor consolidado do Núcleo Origem no ponto
- `valor_comparado` = valor consolidado do Núcleo Comparado no ponto
- `diferenca` = valor_comparado − valor_origem
- `variacao_pct` = diferenca / valor_origem (regra de divisão por zero: valor_origem = 0 e valor_comparado ≠ 0 → None/"não aplicável"; ambos = 0 → 0%)
- `classificacao_estrutural` ∈ {AUMENTOU, REDUZIU, ESTAVEL, NAO_APLICAVEL}

Quando evolução complementar ligada, duas colunas adicionais por agrupador:
- `evolucao_origem_anterior` = valor_origem_ponto_atual − valor_origem_ponto_anterior
- `evolucao_comparado_anterior` = valor_comparado_ponto_atual − valor_comparado_ponto_anterior

### 5.4 Classificação semântica (T-SEMA)

Derivada da classificação estrutural × semântica declarada:

| Estrutural | Maior-é-melhor | Menor-é-melhor | Neutra |
|---|---|---|---|
| AUMENTOU | Melhorou | Piorou | Aumentou |
| REDUZIU | Piorou | Melhorou | Reduziu |
| ESTAVEL | Estável | Estável | Estável |
| NAO_APLICAVEL | Não aplicável | Não aplicável | Não aplicável |

Vocabulário exibido ao usuário segue a semântica declarada.

### 5.5 Agrupador com menos de 3 pontos efetivos

Agrupador cujo número de pontos efetivos (após consolidação, pivot, seleção prévia e De/Até) é menor que 3 aparece na Base Analítica com flag estrutural "Agrupador com < 3 pontos efetivos" mas **sem colunas de Diferença, Variação % e Classificação**. Comparação consecutiva exige ≥ 2 pares, ou seja 3 pontos no mínimo. **W-V3-AGRUP-POUCOS-PONTOS** (informativo) registra contagem de agrupadores afetados.

Isto é filtragem de agrupador específico, não bloqueio global. O bloqueio global **W-V3-PONTOS-MIN** aplica-se ao intervalo efetivo (§4.6), não ao agrupador isolado.

---

## 6. O que a visão entrega

### 6.1 Estrutura do resultado (V3Result)

Granularidade base: 1 linha por combinação de **agrupadores + ponto do eixo**.

Colunas do V3Result:

| Coluna | Conteúdo |
|---|---|
| Agrupadores (N colunas) | Valores dos agrupadores declarados |
| Ponto do eixo | Valor do eixo |
| Valor (Modo Simples) · Valor Origem + Valor Comparado (Modo Comparativo) | Valores consolidados |
| Valor anterior (Modo Simples) | Valor do ponto anterior na sequência |
| Diferença | Calculada conforme §5.2/5.3 |
| Variação % | Calculada com regra de divisão por zero |
| Classificação estrutural | AUMENTOU/REDUZIU/ESTAVEL/NAO_APLICAVEL |
| Classificação semântica | Melhorou/Piorou/Estável/Apenas informar (conforme T-SEMA) |
| Flags estruturais | `lacuna_anterior`, `ausencia_ponto` (textual unificado na Base Analítica) |
| classificacao_medida | VALOR_VALIDO (omitido) / VALOR_NEGATIVO / NULO_MEDIDA |
| Evolução Origem · Evolução Comparado (opcional) | Apenas quando evolução complementar ligada (§4.8) |
| Intervalo ativo | Flag booleana para exibir registros dentro do intervalo efetivo |

### 6.2 Resumo Executivo — 6 blocos fixos adaptados por modo

Aplica padrão consolidado V4 §9.2 / V11 §6.1 adaptado aos dois modos da V3.

**Bloco 1 · Cabeçalho da análise** (constante)
Título amigável · modo analítico (Simples/Comparativo) · medida (Modo Simples) ou núcleos Origem/Comparado (Modo Comparativo) · eixo sequencial + tipo · intervalo efetivo · agrupadores · data/hora.

**Bloco 2 · Números-âncora** (adaptado por modo)
- **Modo Simples:** N° de agrupadores analisados · N° de pontos no intervalo efetivo · Total Geral do intervalo · Variação média dos pares consecutivos · Agrupador de maior variação agregada (+ valor) · Agrupador de menor variação agregada (+ valor).
- **Modo Comparativo:** N° de agrupadores · N° de pontos · Diferença total consolidada (Comparado − Origem) · Variação % consolidada · Agrupador com maior divergência absoluta (+ valor) · Agrupador com menor divergência (+ valor).

**Bloco 3 · Distribuição de classificações estruturais** (adaptado por modo)
- Ambos os modos: contagem e % por classificação estrutural (Aumentou · Reduziu · Estável · Não aplicável) sobre o total de pares consecutivos do resultado.
- Quando semântica ≠ neutra: segunda linha com contagem por classificação semântica (Melhorou · Piorou · Estável · Não aplicável).

**Bloco 4 · Elementos destacados** (adaptado por modo)
- **Modo Simples:** top 10 agrupadores por variação agregada absoluta (decrescente em módulo) — colunas: agrupador, primeiro valor, último valor, diferença agregada, variação % agregada, classificação semântica predominante.
- **Modo Comparativo:** top 10 agrupadores por divergência absoluta em algum ponto — colunas: agrupador, ponto, Origem, Comparado, diferença, variação %, classificação semântica.

**Bloco 5 · Leituras descritivas de síntese** (com faixas editáveis; padrão V4 Bloco 5)

- **Modo Simples — Leitura de tendência** por agrupador, sintetizada no intervalo:
  - Crescente (default): > 70% dos pares consecutivos com classificação AUMENTOU
  - Decrescente (default): > 70% REDUZIU
  - Estável (default): > 70% ESTAVEL
  - Mista (default): nenhuma das anteriores

- **Modo Comparativo — Leitura de aderência** entre Origem e Comparado ao longo da sequência:
  - Aderente (default): > 70% dos pontos com |Variação %| ≤ 5% (tolerância editável)
  - Divergente: caso contrário

- **Faixas editáveis** em "Configurações avançadas" da configuração. Microcopy explícito: *"Estas faixas afetam apenas a frase de síntese do Bloco 5. Os cálculos principais (Diferença, Variação %, Classificação estrutural e semântica) não são afetados."* **W-V3-LEITURA-CUSTOM** registra customização.

- **Nota estática final do Bloco 5** (integra T-12):

  > *Variações expressivas observadas ao longo da sequência merecem investigação especializada: V5 · Comportamento e Dispersão avalia se um ponto está fora do padrão estatístico do agrupador (outlier via IQR, Z-score, percentil); V7 · Desvio em Relação à Média do Grupo avalia se o agrupador como um todo desvia significativamente do comportamento dos pares.*

  Nota declarativa, sem condição de disparo.

**Bloco 6 · Qualidade estrutural** (resumo do Diagnóstico)
Lista resumida dos warnings disparados na execução, organizados por tipo (Bloqueios · Alertas · Informativos). Remete à aba Diagnóstico para detalhe completo.

### 6.3 Exportação Excel — 7 abas

Herda regra transversal **D-017 (Diagnóstico sempre última aba)**. Tela e Excel nunca divergem (princípio PARTE 9 do prévio preservado).

| Ordem | Aba | Conteúdo | Condicional? |
|---|---|---|---|
| 1 | **Resumo Executivo** | 6 blocos (§6.2) | Sempre |
| 2 | **Trajetória Consolidada** | Trajetória ponto a ponto por agrupador (POR_COLUNAS natural: agrupador × ponto do eixo, valor consolidado) | Sempre |
| 3 | **Recorte ponto a ponto** | Pares consecutivos pré-calculados — uma linha por par (ponto_de → ponto_ate) por agrupador. Filtros Excel nativos permitem ao usuário restringir exibição a subset (§6.4) | Sempre |
| 4 | **Resumo por Agrupador** | Síntese por agrupador: total agregado, variação agregada, classificação predominante, N° pontos efetivos, tendência/aderência | **Condicional** · aparece quando há ≥ 2 agrupadores declarados |
| 5 | **Base Analítica** | Granularidade agrupador × ponto com todas as colunas do V3Result (§6.1) | Sempre |
| 6 | **Parâmetros** | Configuração da análise + intervalo declarado vs efetivo + faixas de leitura se customizadas + data/hora | Sempre |
| 7 | **Diagnóstico** | Warnings e ajustes (última aba por D-017) | Sempre |

**Filtros nativos do Excel ativos em todas as abas** (herança V1/V4 · princípio do prévio PARTE 9).

### 6.4 Aba "Recorte ponto a ponto"

Aba adicional dedicada à exploração interativa de recortes do eixo. Uma linha por par consecutivo (ponto_de → ponto_ate) por agrupador, com todas as colunas calculadas pelo motor:

- Agrupadores · Ponto de · Ponto até · Valor em De · Valor em Até · Diferença · Variação % · Classificação estrutural · Classificação semântica · Flags estruturais

**Uso típico:** usuário filtra "Ponto de" ≥ Jan e "Ponto até" ≤ Abr → vê todos os pares consecutivos Jan→Fev, Fev→Mar, Mar→Abr de cada agrupador.

**Nota no topo da aba** (linha 1):

> *Esta aba lista todos os pares consecutivos do eixo com cálculo individual por agrupador. Use os filtros do Excel nas colunas "Ponto de" e "Ponto até" para restringir a leitura ao recorte desejado. Para análise agregada de um subset específico (Total, Variação % e síntese sobre Jan-Abr como conjunto), execute nova análise no TabloFlow ajustando o intervalo De/Até.*

**Decisão de escopo.** MVP entrega aba estática com filtros nativos (**Implementação 1**). Recorte com síntese agregada recalculada dentro do Excel fica registrado como **P-V3-02-Evo · Aba parametrizável com recálculo dinâmico**.

---

## 7. Warnings catalogados (27)

Warnings V3 consolidados no refino.

### 7.1 Bloqueios (7)

| Código | Gatilho |
|---|---|
| **W-V3-N0-EIXO** | Coluna discriminadora do eixo POR_LINHAS com 0 valores únicos |
| **W-V3-N1-EIXO** | Coluna discriminadora do eixo POR_LINHAS com 1 valor único |
| **W-V3-AGRUP-MUITOS** (bloqueio 8+) | 8 ou mais agrupadores declarados |
| **W-V3-PONTOS-MIN** | Intervalo efetivo < 3 pontos |
| **W-V3-INTERVALO-INVALIDO** | De > Até (intervalo invertido) |
| **W-V3-TIPO-INCOMPAT** | Medida de tipo estado/situação (redireciona V8/V6) |
| **W-V3-EIXO-AGRUP-COLISAO** | Campo declarado como eixo e agrupador simultaneamente |
| **W-V3-NMANY** | Resultado > 500.000 linhas |

### 7.2 Alertas (3)

| Código | Gatilho |
|---|---|
| **W-V3-AGRUP-MUITOS** (alerta 6-7) | 6 ou 7 agrupadores declarados |
| **W-V3-NULL-MASS** | > 20% dos registros com nulo na medida |
| **W-V3-EIXO-LACUNA-MASSIVA** | > 30% dos pontos esperados no eixo ausentes (só eixos com detecção ativa) |

### 7.3 Informativos (17)

| Código | Gatilho |
|---|---|
| **W-V3-EIXO-TIPO-INFERIDO** | Tipo de eixo aceito por default sem edição |
| **W-V3-EIXO-ORDEM-MANUAL** | Ordem manual aplicada sobre eixo temporal/ordinal |
| **W-V3-EIXO-PIVOT** | Pivot POR_LINHAS → POR_COLUNAS aplicado |
| **W-V3-EIXO-PONTOS-MUITOS** | Bloco de seleção ativado (10+ pontos únicos) |
| **W-V3-EIXO-ESTRUTURA-INFERIDA** | Estrutura aceita por default sem edição |
| **W-V3-EIXO-SELECAO+INTERVALO** | Seleção prévia combinada com De/Até |
| **W-V3-EIXO-LACUNA** | Lacunas detectadas no eixo (só eixos com detecção ativa) |
| **W-V3-AGRUP-AUSENCIA-PONTO** | Par (agrupador × ponto) em ausência |
| **W-V3-AGRUP-POUCOS-PONTOS** | Agrupador com < 3 pontos efetivos (não produz análise sequencial) |
| **W-V3-INTERVALO-DEFAULT** | De/Até aceitos por default sem edição |
| **W-V3-INTERVALO-AJUSTE-INICIO** | De ajustado para primeiro ponto disponível |
| **W-V3-INTERVALO-AJUSTE-FIM** | Até ajustado para último ponto disponível |
| **W-V3-TIPO-DECL** | Tipo de medida aceito por default sem edição |
| **W-V3-TIPO-REL** | Tipo relativo/não-aditivo: opção declarada (analisar/outra/média ponderada) |
| **W-V3-NEGATIVOS** | Opção de negativos declarada (líquidos/absoluto) |
| **W-V3-NULL** | Contagem de registros com nulo na medida |
| **W-V3-SEMA-DECL** | Semântica aceita por default sem edição |
| **W-V3-SEMA-CUSTOM** | Semântica declarada diferente do default proposto |
| **W-V3-COMP-EVOLUCAO** | Evolução complementar de Origem/Comparado ligada |
| **W-V3-LEITURA-CUSTOM** | Faixas de leitura descritiva customizadas (Bloco 5) |

---

## 8. Componentes transversais da Fundação

| Transversal | Uso em V3 | Status |
|---|---|---|
| **T-AGRUPA** | Consolidação por agrupador + ponto do eixo antes do cálculo · reconhecedor pt-BR/pt-EN herdado de D-026 consumido por T-EIXO | Formalizado |
| **T-DIAG** | Aba Diagnóstico última (D-017) · categorias AJUSTE_LEVE e DECISAO_USUARIO | Formalizado |
| **T-SEMA** | Semântica maior-é-melhor / menor-é-melhor / neutro (§4.8, §5.4) | Formalizado |
| **T-EIXO** | Eixo sequencial ordenado com 3 tipos canônicos · **primeira consumidora** · define padrão herdado por V8 | Formalizado (esta decisão) |
| **T-PIVOT** | Pivot POR_LINHAS → POR_COLUNAS · nova semântica: pivot de **pontos do eixo** (terceira além de estados V2 e medidas V4) | Extensão formalizada (requisito G-FUND) |
| **T-MODELO** | Configuração persistível como modelo (§4.10) | Formalizado |

V3 **não usa** T-RANK, T-ACUM, T-ABC, T-DUAL, T-FUZZY, T-CONCAT.

---

## 9. Fronteira com Módulo 2 (TabloPrep)

| Cenário | Status | Tratamento |
|---|---|---|
| **STACK** (múltiplas abas estruturalmente idênticas representando períodos) | Fora de escopo V3 MVP | Consolidação manual prévia no MVP; **M2.STACK candidata** no Módulo 2 futuro |
| **RESHAPE** (dados empilhados em aba única com coluna discriminadora) | Dentro de escopo V3 via POR_LINHAS (§3.1) — quando a discriminadora **é** o eixo sequencial | Nativo V3 via T-PIVOT |
| **NORMALIZE** (transformações textuais semânticas) | Fora de escopo V3 MVP | Eixo manual com valores textuais é aceito sem normalização; transformações semânticas reservadas para M2.NORMALIZE futuro (coerente com decisão D-057) |

**M2.STACK** é operação candidata do Módulo 2 para empilhamento de múltiplas abas estruturalmente idênticas em uma única aba com coluna discriminadora adicional contendo o nome da aba de origem. Consumo futuro: V3 (eixo sequencial multi-aba), potencialmente outras visões. Posicionamento arquitetural — transversal puro da Fundação · parte de M2 · capability compartilhada — a decidir no G-FUND ou no refino DCV-OPN correspondente.

---

## 10. Pontos de atenção (riscos analíticos conhecidos)

- **Ruptura/descontinuidade fora de escopo V3 permanente.** A V3 rastreia evolução de valor em eixo ordenado — variação entre pontos consecutivos é expressa por Diferença e Variação %, sem camada adicional de "salto" ou "colapso". O fenômeno de variação extrema é tratado por outras visões do Módulo 1 pelo ângulo correto: V5 · Comportamento e Dispersão detecta outliers estatisticamente; V7 · Desvio em Relação à Média do Grupo detecta elementos que divergem significativamente do comportamento dos pares. Adicionar "ruptura" em V3 duplicaria conceito sem precisão analítica distinta. Decisão explícita do prévio PARTE 7.2 preservada.

- **Densidade de lacunas.** Bases com > 30% de pontos esperados ausentes no eixo temporal/ordinal podem produzir análise degradada. **W-V3-EIXO-LACUNA-MASSIVA** sinaliza mas não bloqueia — usuário pode ter razão analítica legítima (histórico de entidade nova, sazonalidade natural). Analista decide.

- **Tipos relativos sem agregação explícita.** Somar ou tirar média simples de percentuais/índices/scores pode gerar resultado sem significado analítico. Default declarado com 3 opções (§4.3) coloca a decisão no usuário; **W-V3-TIPO-REL** registra escolha.

- **Agrupadores com poucos pontos efetivos.** Agrupadores com < 3 pontos no intervalo efetivo aparecem na Base Analítica com flag mas sem cálculos sequenciais. **W-V3-AGRUP-POUCOS-PONTOS** registra contagem. Normal em bases com ciclos de vida naturais variados (entidade nova, sazonal, descontinuada).

- **Eixo manual sem detecção de lacuna.** Motor não tenta inferir ordem canônica de eixos manuais ou ordinais sem prefixo numérico — consequentemente não detecta lacunas nesses tipos. Analista responsável pela integridade da sequência.

- **Colisão eixo × agrupador.** Bloqueio operacional honesto — motor não tem base para decidir qual das duas declarações é correta; pede ajuste.

- **Bases muito extensas.** Granularidade agrupador × ponto multiplica linhas rapidamente. Escala progressiva de agrupadores (§4.7) e bloqueio de 500K linhas (§7.1) protegem. Diretrizes de performance (§11.3) mitigam impacto em processamento.

---

## 11. Relação com Fundação e retroação sobre V8

### 11.1 Requisitos novos para a Fundação

- **T-EIXO como transversal formalizada** — 3 tipos canônicos (temporal · lógico/ordinal · manual) com default declarado pelo motor, detecção herdando reconhecedor pt-BR/pt-EN de D-026 (T-AGRUPA). Implementação compartilhada — zero duplicação. Vincula V8.
- **T-PIVOT com terceira semântica** — além de estados (V2, D-026) e medidas (V4, D-039), T-PIVOT agora suporta pivot de **pontos do eixo** (V3). Não é nova extensão estrutural — motor opera sobre dimensão em coluna discriminadora qualquer; esta decisão formaliza a terceira semântica no vocabulário da Fundação.
- **Contrato V3Result** consolidado (§6.1) com flags estruturais (`lacuna_anterior`, `ausencia_ponto`), campo `classificacao_medida` herdado de V4, e colunas condicionais (evolução complementar).
- **Mecanismo de pré-validação de intervalo antes do processamento pesado** — diretriz de performance aplicável a todas as visões com intervalo/filtro prévio.

### 11.2 Retroação sobre V8 (registrada)

DCV-V8 ainda não refinado. Quando for, herdará:
- Os 3 tipos de eixo (§4.4) com mesma definição e detecção.
- Default declarado para tipo de eixo.
- Mecânica POR_COLUNAS/POR_LINHAS de T-PIVOT adaptada.
- Detecção de lacunas do eixo (§4.5) como insumo para classificação "Ausente" da V8.
- Escala progressiva de agrupadores adaptada à natureza V8.

Bloco "Relação com V3" simétrico ao §2.3 deste DCV fica como tarefa para a próxima revisão natural de V8 (DCV-V8 ou Spec S-V8) — **não é sessão dedicada imediata**. Retroação diferida análoga ao padrão V11↔V1 (D-058).

---

## 12. Roadmap pós-MVP (P-V3-XX-Evo)

- **P-V3-01-Evo · Múltiplas abas como eixo sequencial** — implementação via extensão análoga a T-DUAL mas sequencial (N abas = N pontos do eixo). Dependência: M2.STACK implementada (caminho preferencial via fluxo M2 → M1) ou extensão dedicada no motor_upload (caminho direto).
- **P-V3-02-Evo · Aba parametrizável com recálculo dinâmico** — aba "Recorte ponto a ponto" com síntese agregada recalculada sobre subset selecionado dentro do Excel (Implementação 3 da discussão T-13). Custo quadrático em N pontos; implementar quando uso real validar demanda.
- **P-V3-03-Evo · Reordenação manual de eixo avançada** — refinar mecânica de drag-and-drop e ajuste manual de ordem em eixos grandes (50+ pontos). Decisão de UI da Spec S-V3 inicial pode já cobrir; evolução fica registrada.
- **P-V3-04-Evo · Detecção de sazonalidade e tendência não-linear** — camada analítica avançada sobre a sequência. Território potencial de IA assistiva (Fase 3). Não vinculante.

---

## 13. Nomenclatura oficial da V3

Termos consolidados no refino (vocabulário canônico da V3):

- **Campo Principal** — a medida analisada no Modo Simples
- **Núcleo Origem · Núcleo Comparado** — os dois núcleos confrontados no Modo Comparativo
- **Eixo Sequencial** — a dimensão pela qual a análise ordena os pontos
- **Tipo do Eixo** — temporal · lógico/ordinal · manual
- **Ponto do eixo** — cada valor único do eixo após pivot e ordenação
- **Coluna discriminadora do eixo** — em POR_LINHAS, a coluna que identifica qual ponto cada linha representa
- **Agrupador** — dimensão pela qual a análise segmenta a evolução (D-025, vocabulário canônico do TabloFlow; substitui "aglutinador" do prévio)
- **De · Até** — limites do intervalo configurado
- **Intervalo declarado** — o que o usuário configurou
- **Intervalo efetivo** — o que o motor aplicou após eventuais ajustes-limite
- **Diferença** — variação absoluta entre pontos (consecutivos em Simples; Origem/Comparado em Comparativo)
- **Variação %** — diferença relativa, com regra de divisão por zero
- **Classificação estrutural** — Aumentou · Reduziu · Estável · Não aplicável
- **Classificação semântica** — Melhorou · Piorou · Estável · Apenas informar (ou Aumentou/Reduziu/Estável com semântica neutra)
- **Evolução complementar** — leitura opcional da evolução individual de Origem e Comparado no Modo Comparativo
- **Leitura de tendência** — síntese qualitativa do Modo Simples (Crescente/Decrescente/Estável/Mista)
- **Leitura de aderência** — síntese qualitativa do Modo Comparativo (Aderente/Divergente)
- **Tolerância de aderência** — % de |Variação| considerado aderente (5% default, editável)
- **Lacuna do eixo** — ponto ausente no universo consolidado
- **Ausência do agrupador em ponto** — agrupador sem valor em ponto específico enquanto outros têm
- **Recorte ponto a ponto** — aba do Excel com pares consecutivos filtráveis

Vocabulário dual técnico/exibição preservado onde aplicável (contrato `classificacao_medida`; classificações estrutural vs semântica).

---

## 14. Posicionamento C.5

A V3 foi refinada integralmente sob a lente do princípio C.5 (TabloFlow analisa sobre o dado informado, nunca decide por ele). Manifestações concretas:

- **Três tipos de eixo com default declarado** — motor detecta padrões e propõe; usuário confirma ou edita (§4.4).
- **Estrutura POR_COLUNAS/POR_LINHAS com default declarado** — inferência proposta, não silenciosa (§3.1).
- **Tipos relativo/não-aditivo com default declarado** — 3 opções explícitas em vez de execução silenciosa (§4.3).
- **Negativos com default declarado** — 2 opções em vez de soma algébrica oculta (§4.3).
- **Nulos na medida preservados** — classificação `NULO_MEDIDA` visível; excluídos apenas do cálculo (§4.3).
- **Semântica da medida declarada** — maior/menor/neutro visível, não inferida silenciosamente (§4.8).
- **Lacunas no eixo preservadas** — não preenchidas com zero; detectadas quando possível, registradas em flags sem alterar cálculo (§4.5).
- **Intervalo declarado vs intervalo efetivo preservados separadamente** — ajustes-limite registrados em AJUSTE_LEVE com auditabilidade (§4.6).
- **Colisão eixo × agrupador é bloqueio honesto** — motor não corrige silenciosamente (§4.7).
- **Estado/situação redireciona para V8/V6** — bloqueio com caminho, não cálculo sem significado (§4.3).
- **Ruptura fora de escopo V3 permanente** — território analítico de V5/V7 respeitado (§10).
- **Evolução complementar com default desligado** — regra central do Comparativo preservada (§4.8).
- **Faixas de leitura descritiva editáveis** — síntese qualitativa do Bloco 5 sob controle do usuário (§6.2).
- **Multi-aba fora de escopo com orientação declarativa** — usuário escolhe caminho, não é redirecionado silenciosamente (§3.2).
- **Aba "Recorte ponto a ponto" com filtros nativos** — exploração sob controle do usuário, sem fórmula viva que possa divergir do motor (§6.4).

Padrão "default declarado" aplicado sistematicamente — terceira família a consolidá-lo (V2 em D-024, V4 em D-036/D-040, agora V3), candidato forte a formalização como princípio derivado de C.5 no próximo ajuste estrutural do CONTEXT.

---

## 15. Integração com Fundação

### 15.1 Transversais consumidos

Lista consolidada em §8. Novos requisitos para G-FUND:

1. **T-EIXO formalizada** — 3 tipos canônicos com default declarado + herança de D-026 (§4.4)
2. **T-PIVOT com terceira semântica** — pontos do eixo além de estados e medidas (§8)
3. **Contrato V3Result** com flags estruturais (§6.1)
4. **Mecanismo de pré-validação de intervalo** (diretriz transversal de performance)

### 15.2 Diretrizes de performance

7 diretrizes, das quais 5 herdadas de D-032 e 2 novas V3:

1. Amostragem limitada do motor_upload (até 10.000 linhas) — herdado
2. Consolidação antes do cálculo via T-AGRUPA — herdado / princípio P0.6 do prévio
3. Preservação de ordem determinística (tie-break T-RANK D-041) — herdado
4. Streaming de exportação Excel para resultados > 100.000 linhas — herdado
5. Cache de resultado intermediário por sessão — herdado
6. **Pré-validação de intervalo antes do processamento pesado** (novo V3) — motor valida intervalo-invalido e pontos-min antes de executar consolidação + pivot
7. **Pré-cálculo vetorizado da aba "Recorte ponto a ponto"** (novo V3) — N × (M−1) linhas com implementação vetorizada (pandas/numpy)

---

## 16. Decisões geradas

| D-XXX | Tema | Tipo |
|---|---|---|
| D-059 | Sumário do refino DCV-V3 · consolidação de 13 pendências | Consolidação |
| D-060 | Posicionamento da Família B · Sequência (V3 × V8) + retroação diferida | **Transversal** (V3 · V8 · Família B) |
| D-061 | T-EIXO formalizada · 3 tipos canônicos · default declarado · herança D-026 | **Transversal de Fundação** |
| D-062 | Estruturas POR_COLUNAS/POR_LINHAS da V3 + seleção de pontos + T-PIVOT terceira semântica | Específica V3 com requisito G-FUND |
| D-063 | Multi-aba fora de escopo V3 MVP + P-V3-01-Evo + M2.STACK candidato | Decisão de escopo + M2 candidato |
| D-064 | Intervalo De/Até: papel analítico, default declarado, comportamentos-limite | Específica V3 |
| D-065 | Lacunas no eixo × ausência do agrupador: detecção por tipo de eixo + flags estruturais | Específica V3 |
| D-066 | Tipos de medida e negativos na V3 (herança V4 adaptada) + redirecionamento estado/situação para V8/V6 | Específica V3 |
| D-067 | Modo Comparativo: T-SEMA integralmente herdado + evolução complementar opcional com default desligado | Específica V3 |
| D-068 | Ruptura fora de escopo V3 permanente com redirecionamento declarativo para V5/V7 | Decisão de escopo |
| D-069 | Resumo Executivo V3 · 6 blocos adaptados por modo · 7 abas Excel · aba "Recorte ponto a ponto" | Específica V3 |
| D-070 | Bloqueios operacionais V3 · 10 bloqueios · 7 diretrizes de performance | Específica V3 |

Pendências T-01 (vocabulário), T-03+T-04 (fronteira V2/V4/V8 e casos de uso) consolidadas no próprio DCV sem D-XXX própria — decisões não-estruturais de alinhamento terminológico e aplicação de padrão §2.

---

## 17. Pendências do refino (histórico)

13 pendências estruturais fechadas em 1 sessão (19/04/2026):

**Bloco A · Fronteira, vocabulário e fundamentos da família**
- T-01 · Vocabulário: aglutinador → agrupador — §13
- T-02 · Família B · Sequência + posicionamento V3 × V8 — §2.3 · D-060
- T-03+T-04 · Fronteira V3 × V2 × V4 + casos de uso reais — §2.1, §2.2

**Bloco B · T-EIXO (primeira consumidora)**
- T-05 · Tipos de eixo — §4.4 · D-061
- T-06 · POR_COLUNAS/POR_LINHAS + seleção de pontos — §3.1, §4.4 · D-062
- T-07 · Multi-aba fora de escopo MVP + M2.STACK — §3.2, §9 · D-063
- T-08 · Intervalo De/Até — §4.6 · D-064
- T-09 · Lacunas no eixo × ausência do agrupador — §4.5 · D-065

**Bloco C · Semântica, modos e cálculo**
- T-10 · Tipos de medida e negativos — §4.3 · D-066
- T-11 · Modo Comparativo: T-SEMA + evolução complementar — §4.8, §5.4 · D-067
- T-12 · Ruptura fora de escopo V3 — §10 · D-068

**Bloco D · Saída e operação**
- T-13 · Resumo Executivo V3 + 7 abas Excel + aba "Recorte ponto a ponto" — §6 · D-069
- T-14 · Bloqueios operacionais V3 + performance — §4.7, §15.2 · D-070

**Referências cruzadas:** D-058 (retroação diferida V11↔V1 como precedente do padrão V3↔V8) · D-017 (Diagnóstico última aba) · D-024/D-036/D-040 (padrão default declarado) · D-025 (4 tipos de medida) · D-026 (reconhecedor pt-BR/pt-EN em T-AGRUPA, consumido por T-EIXO) · D-027 (escala progressiva de agrupadores) · D-030 (T-MODELO) · D-032 (bloqueios operacionais + performance V2) · D-039 (T-PIVOT multi-medida) · D-041 (T-RANK configurável e tolerância 1e-9) · D-043 (bloqueios V4) · D-044 (Resumo Executivo V4 com faixas editáveis) · D-053 (T-CONCAT candidato como precedente de M2.STACK candidato) · D-057 (higiene textual vs NORMALIZE — coerência com fronteira M2 da V3).

---

## 18. Referências

- **CONTEXT.md** §3 (Fase 0), §4 (Família B), §6 (T-EIXO formalizada, T-PIVOT terceira semântica), §9 (C.5 + padrão default declarado), §13 (padrões estruturais de produto)
- **DECISIONS.md** D-058 (precedente retroação), D-059 a D-070 (decisões deste refino), decisões herdadas referenciadas em §17
- **GLOSSARIO.md** §1 (Família B), §4 (T-EIXO atualizada, T-PIVOT estendida), §5 nova seção V3, §6 warnings V3
- **Planilha TabloFlow_Estado_do_Projeto.xlsx** aba 2 L11 (V3 refinada e aprovada), aba 3 L23 (T-EIXO formalizada), aba 1 L10 (próximo passo DCV-V8)

---

*Fim do DCV-V3.* Arovado, próxima sessão da Fase 0: DCV-V8 (Família B · Sequência — herda T-EIXO desta visão).
