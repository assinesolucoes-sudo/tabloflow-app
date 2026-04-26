# DCV-V7 · Desvio em Relação à Média do Grupo

**Visão:** V7 · Desvio em Relação à Média do Grupo
**Módulo:** Módulo 1 · TabloAnálise
**Família:** D · Posição relativa
**Status:** Aprovado
**Data do aprovação:** 19/04/2026
**Sessão de refino:** 1 (sessão única, 13 pendências fechadas)
**Arquivo canônico:** `/specs/dcv/dcv_v7.md`

---

## 1. Propósito da visão

A V7 responde: **"dentro de cada grupo, como cada elemento se posiciona em relação à média do seu próprio grupo, qual o seu desvio absoluto, qual o seu desvio percentual e como esse desvio deve ser classificado?"**

A visão analisa **posicionamento relativo interno** de elementos dentro de grupos declarados — benchmarking interno automático. A média de referência é calculada a partir dos próprios dados do grupo, sem benchmark externo, sem meta externa e sem comparação temporal. É a **única visão do Módulo 1 que usa o próprio conjunto de dados como referência interna de comparação** (P0.8 do prévio, preservado).

A V7 é a **primeira visão da Família D · Posição relativa**. Decisões tomadas neste DCV orientam V9 (segunda visão da família, a ser refinada em sequência) — bloco de retroação diferida registrado em §11.2.

A V7 opera sobre uma base consolidada única e aplica o princípio estrutural **"consolidar primeiro, calcular depois"** (P0.6 do prévio, preservado): elementos são consolidados dentro de seus grupos via regra de agregação declarada antes de qualquer cálculo de média do grupo ou desvio. Essa ordem é a **blindagem central contra dupla agregação** — armadilha estrutural em que média sobre linhas brutas (em vez de elementos consolidados) produz classificação invertida.

A V7 não diagnostica causa raiz, não declara que um dado está errado e não afirma que estar acima ou abaixo é bom ou ruim por si só. Evidencia o posicionamento relativo; a interpretação causal cabe ao usuário.

---

## 2. Posicionamento analítico

### 2.1 O cenário real que a V7 atende

O cenário típico da V7 é a análise de performance relativa em rotinas contábeis, gerenciais e operacionais brasileiras:

- **Performance de vendedores por região** — quem se destaca ou fica atrás da média da sua região.
- **Custo unitário por linha de produção** — quais linhas operam fora da média de custo do seu setor.
- **Tempo médio de atendimento por filial** — filiais que divergem do padrão da rede.
- **Volume transportado por transportadora em categoria logística** — outliers dentro de cada modal.
- **Produtividade por centro de custo em uma unidade de negócio** — centros fora do padrão interno.
- **Fornecedores por categoria de insumo** — fornecedores com ticket médio divergente do da categoria.
- **Taxa de conversão por vendedor em carteira** — quem está acima ou abaixo da média da equipe.

Em todos esses cenários, o analista humano hoje recorre a ordenação por desvio no Excel com cálculo manual de média por filtro. A V7 estrutura esse trabalho, preserva a regra analítica declarada (consolidação, semântica, tolerância) e entrega artefato Excel auditável com síntese qualitativa por grupo.

### 2.2 Fronteira com V5 e V4 (visões vizinhas)

**V7 × V5 (Família E · Estrutura interna).** V5 analisa dispersão estatística interna de um campo numérico (IQR, Z-score, percentil, detecção de outliers) — o "desvio" em V5 é propriedade estatística derivada do próprio campo. V7 analisa posição relativa de cada elemento à média do grupo declarado — o "desvio" em V7 é distância consolidada em torno de um centro declarado. Aplicação do padrão **"warning em uma visão pode ser conteúdo em outra"** (D-076 / DCV-V8): mesmo campo numérico é substrato estatístico em V5 e input de classificação por tolerância em V7. Quem quer medir dispersão do campo como característica intrínseca usa V5; quem quer classificar elementos em relação à média do grupo usa V7.

**V7 × V4 (Família C · Composição).** V4 analisa como um total se distribui entre elementos — participação %, acumulado, classificação ABC, Curva Pareto (V10). A referência de V4 é o Total Geral; cada elemento é medido pelo "tamanho" dentro do todo. V7 tem referência interna distinta: a média do grupo ao qual o elemento pertence. Pergunta V4: "esse elemento é grande dentro do total?". Pergunta V7: "esse elemento está dentro ou fora do padrão do seu grupo?". Elemento grande em V4 pode ser Na Média em V7 (se o grupo todo é grande); elemento pequeno em V4 pode ser Abaixo em V7 (se o grupo todo é pequeno mas ele é menor ainda). As visões são complementares em análise de portfólio: V4 para mapa de participação, V7 para benchmarking interno por grupo.

Nenhuma dessas fronteiras é navegada em interface operacional. Microcopy declarativa autossuficiente no DCV + nota estática final no Resumo Executivo (Bloco 5, §6.2) redirecionam quando apropriado.

### 2.3 Relação com V9 (par autônomo da Família D)

V7 e V9 convivem como par autônomo da Família D — mesma família, problemas analíticos distintos, motores distintos, vocabulário parcialmente compartilhado (T-SEMA).

**Família D · Posição relativa** — visões que analisam como cada elemento se posiciona em relação a um benchmark calculado internamente sobre os próprios dados. V7 calcula o benchmark como média do grupo ao qual o elemento pertence (desvio univariado); V9 calcula o benchmark como posição consolidada em múltiplas métricas ordenadas com direção declarada (ranking multidimensional). Ambas consomem T-SEMA; V7 também consome T-AGRUPA; V9 também consome T-RANK de forma distinta (ranking multidimensional cross-elementos, não intra-grupo como V7). Não há view especializada entre elas — são visões autônomas da mesma família.

| Aspecto | V7 · Desvio em Relação à Média do Grupo | V9 · Perfil de Ranking por Métricas |
|---|---|---|
| O que rastreia | Desvio de cada Elemento em relação à média do seu Grupo (univariado) | Posição consolidada de cada Elemento em ranking por múltiplas métricas simultâneas (multidimensional) |
| Unidade analítica | Elemento + Grupo (com valor consolidado pela regra de agregação) | Elemento (com posição em cada métrica + score consolidado) *(a confirmar em DCV-V9)* |
| Classificação do resultado | Acima · Na Média · Abaixo (+ atributo Desvio Significativo) | *A confirmar em DCV-V9* — candidatos: Destaque · Padrão · Fragilidade ou faixas por quartil de score consolidado |
| Transversais comuns | T-AGRUPA · T-SEMA · T-RANK · T-DIAG · T-MODELO | T-SEMA · T-RANK · T-DIAG · T-MODELO *(T-AGRUPA: a confirmar em DCV-V9)* |
| Tipo de medida | Uma medida numérica por execução | Múltiplas medidas numéricas (2 a 6) por execução, cada uma com direção declarada |

**Não há substituição de uma pela outra.** O usuário escolhe conscientemente a visão pela pergunta que quer responder: "dentro de cada grupo, quem destoa da média?" (V7) ou "quais elementos se destacam quando consideradas múltiplas métricas simultaneamente?" (V9). A fronteira é navegada por microcopy declarativa e autossuficiente em cada visão — nenhuma das duas menciona a outra em interface operacional. Quem precisa entender ambas lê este bloco no DCV. DCV-V9 receberá bloco "Relação com V7" simétrico na próxima revisão natural (retroação diferida registrada em §11.2 — análoga a V3→V8 em D-060 e V11→V1 em D-058).

### 2.4 Unidade analítica da V7

Unidade analítica da V7: combinação de **Elemento + Grupo**, com valor consolidado pela regra de agregação declarada.

Princípio **"consolidar primeiro, calcular depois"** preservado do prévio §4.3: consolidação via T-AGRUPA aplicada sempre que o modo da base for Transacional (múltiplas linhas por Elemento+Grupo); validada como no-op quando modo for Pré-agregado (1 linha por Elemento+Grupo já no upload). Cálculo de média do grupo sempre opera **sobre elementos consolidados**, nunca sobre linhas brutas.

**Distinção Grupo × Elemento:** Grupo é o campo categórico obrigatório que segmenta a base em unidades independentes de comparação (região, categoria, linha de produção); Elemento é o campo categórico obrigatório que identifica a unidade posicionada dentro do grupo (vendedor, fornecedor, centro de custo). Grupo e Elemento são campos declarados distintos — mesmo grupo comporta múltiplos elementos; mesmo elemento pode aparecer em grupos diferentes (mas é tratado como unidade analítica distinta por grupo).

---

## 3. O que a visão recebe

### 3.1 Estrutura de entrada

Uma base lógica por execução, com uma ou mais abas. O usuário escolhe **uma aba** para análise. O blueprint menciona consolidação de múltiplas abas, mas o padrão oficial do projeto privilegia a escolha explícita da aba pelo usuário na versão consolidada da visão.

Formato de entrada: **tabela plana** com linhas representando registros (Transacional) ou uma linha por combinação (Grupo, Elemento) (Pré-agregado). Colunas identificam Grupo, Elemento, Medida (quando regra ≠ Contagem) e eventualmente campo de peso para Relativa Ponderada (§4.2).

### 3.2 Fora de escopo de entrada

**Múltiplas abas estruturalmente idênticas** representando cortes distintos (ex: aba por período, aba por unidade) permanecem fora de escopo V7 MVP. Transformação estrutural prévia é responsabilidade do usuário (ou da operação M2.STACK candidata, formalizada em D-063). V7 MVP aceita uma aba única.

**Benchmarks externos** (meta declarada, média setorial, referência de indústria) permanecem fora de escopo V7 — a visão é definida por usar a média do grupo calculada sobre os próprios dados. Extensão para benchmarks externos registrada em P-V7-04-Evo.

**Múltiplas medidas por execução** ficam fora de escopo MVP. Usuário executa V7 uma vez por medida. Extensão em P-V7-02-Evo.

---

## 4. Configuração analítica

### 4.1 Modo da base (Transacional × Pré-agregado) e consolidação

Modo da base declarado pelo usuário em E2 (etapa de configuração) com **default declarado detectado pelo motor** na amostragem (padrão herdado de V8 D-074, adaptado à natureza Elemento+Grupo).

**Detecção default:**
- Se motor detecta duplicatas de (Grupo, Elemento) na amostra → modo **Transacional** proposto como default.
- Se (Grupo, Elemento) é único em 100% dos casos detectados → modo **Pré-agregado** proposto como default.

**Modo Transacional:**
Consolidação via **T-AGRUPA obrigatória** com regra de agregação declarada (Soma default, conforme §4.9). Múltiplas linhas de mesma (Grupo, Elemento) são consolidadas em 1 linha por combinação antes do cálculo de média do grupo.

**Modo Pré-agregado:**
Consolidação via **T-AGRUPA como no-op validado**. Motor verifica que unicidade realmente se mantém no volume completo (não apenas na amostra); se detecta duplicatas inesperadas, dispara bloqueio estrutural **W-V7-MODO-VIOLACAO** (usuário declarou Pré-agregado mas base tem duplicatas — motor não pode prosseguir sem confirmação de regra de agregação).

**Warnings:**
- **W-V7-MODO-TRANS-DEFAULT** (informativo) — modo Transacional aceito sem edição.
- **W-V7-MODO-TRANS-CUSTOM** (informativo) — usuário editou para Transacional.
- **W-V7-MODO-PREAGG-DEFAULT** (informativo) — modo Pré-agregado aceito sem edição.
- **W-V7-MODO-PREAGG-CUSTOM** (informativo) — usuário editou para Pré-agregado.
- **W-V7-MODO-VIOLACAO** (bloqueio) — modo Pré-agregado declarado mas duplicatas detectadas.

### 4.2 Campo de medida e tratamento por tipo

Tipo da medida declarado pelo usuário em E3 com **default declarado detectado pelo motor** (padrão D-024 · D-025 refinado em V4 D-036).

**Taxonomia canônica (herança D-025 adaptada V7):**

| Tipo | Default T-AGRUPA | Cálculo da média do grupo | Casos-limite |
|---|---|---|---|
| **Aditiva** | Soma | Média aritmética simples dos elementos consolidados | Negativos preservam sinal (alerta forte); média negativa → grupo Não aplicável |
| **Não-aditiva** | Média | Média aritmética simples dos elementos consolidados | Idem |
| **Relativa** | Média aritmética (default) · **ou** ponderada se campo de peso declarado | Média aritmética (default) · Σ(valor × peso)/Σpeso (ponderada) | Idem + alerta forte sobre média aritmética de taxas (W-V7-RELATIVA-MEDIA-ARIT) |
| **Estado/Situação** | N/A | **Bloqueio** com redirecionamento V6 | — |

**Contagem** é regra de agregação especial que **dispensa campo de medida** (§4.9). Quando regra = Contagem, campo Medida fica inaplicável; cálculo opera sobre contagem de linhas por (Grupo, Elemento).

**Tratamento de valores negativos na medida:**
Negativos são preservados (não zerados, não filtrados, não convertidos). Motor dispara **W-V7-NEG-MEDIDA** (alerta forte) sinalizando presença. Efeito no cálculo do desvio percentual: preserva sinal matemático; grupos com média do grupo negativa recebem classificação especial **Não aplicável** (ver §5.3) — desvio absoluto é calculado normalmente, desvio percentual calcula mas fica contraintuitivo, por isso classificação do grupo vira Não aplicável para evitar interpretação errada. **W-V7-GRUPO-MEDIA-NEG** (alerta forte) registra cada grupo afetado.

**Média ponderada em tipo Relativa:**
Média aritmética de taxas sem ponderação pode distorcer resultado quando volumes diferem significativamente entre elementos. Motor expõe em E3: *"Tipo Relativa detectado. Média de taxas sem ponderação pode distorcer o cálculo. Declarar campo de peso (quantidade, volume) para média ponderada? Opcional."* Se usuário declara campo de peso, motor aplica Σ(valor × peso)/Σpeso. **W-V7-RELATIVA-MEDIA-ARIT** (alerta forte) registra default aritmético aceito; **W-V7-RELATIVA-MEDIA-POND** (informativo) registra ponderação declarada.

**Redirecionamento Estado/Situação → V6:**
Motor detecta sinais (coluna com ≤5 valores únicos numéricos, valores 0/1 ou 0/1/2, nome "Status"/"Situação"/"Estado") e bloqueia: *"O tipo 'Estado/Situação' detectado/declarado não é analisável por V7 (desvio de média). Para cruzamento de dimensões categóricas, considere V6 · Relacionamento entre Dimensões."* **W-V7-MEDIDA-ESTADO** (bloqueio). Detecção com confirmação do usuário antes do bloqueio evita falso positivo.

### 4.3 Ordem canônica de cálculo · blindagem contra dupla agregação

A armadilha estrutural central da V7 é **dupla agregação** — calcular média do grupo sobre linhas brutas em vez de elementos consolidados, produzindo classificação invertida. Exemplo: base com VendedorA aparecendo em 2 linhas (100 e 200) e VendedorB em 1 linha (300). Caminho correto: VendedorA consolidado=300, VendedorB=300 → média=300, ambos Na Média. Caminho com dupla agregação: média=(100+200+300)/3=200 → VendedorA "Acima", VendedorB "Acima". Inversão total.

Contrato formal em 4 passos (§5.1 detalha):

1. **Consolidação Elemento+Grupo** via T-AGRUPA conforme regra de agregação declarada.
2. **Média do Grupo** sobre elementos consolidados.
3. **Desvios** absoluto e percentual por elemento.
4. **Classificação** por tolerância + **Ranking** intra-grupo.

Nenhum passo pode ser pulado ou reordenado. Implementação na Fundação (F-MOT) precisa blindar em teste unitário que linhas brutas nunca entram no cálculo da média.

### 4.4 Tolerância e Zona de Média

**Tolerância** é parâmetro declarado pelo usuário em E3 que define a **Zona de Média** — região classificatória em que elementos são classificados como Na Média.

**Default declarado:** ±5% simétrico, em unidade de desvio percentual. Valor canônico fixo, não adaptativo, não dependente de tipo de medida. Visível em E3, editável a qualquer momento antes da execução.

**Formato:** ±N% (simétrico único). Tolerância assimétrica (+M% / −P%) ou em unidade absoluta ficam fora de escopo — Tolerância assimétrica violaria a regra de que T-SEMA não afeta cálculo (T-06); Tolerância absoluta perderia comparabilidade entre grupos de escalas distintas.

**Aplicação:** elemento com `|desvio_percentual| ≤ N` → Na Média; caso contrário → Acima (desvio_percentual > +N) ou Abaixo (desvio_percentual < −N).

**Papel duplo:** (1) define classe Na Média (taxonomia §5.2); (2) define atributo derivado **Desvio Significativo** = Classificação ∈ {Acima, Abaixo} (§5.2).

**Warnings:**
- **W-V7-TOLERANCIA-DEFAULT** (informativo) — ±5% aceito sem edição.
- **W-V7-TOLERANCIA-CUSTOM** (informativo) — usuário editou para valor distinto.

**Casos em que Tolerância não se aplica:** grupos com classificação Não aplicável (média negativa, média zero — §5.3) não passam pela verificação de Tolerância; elementos NULO_MEDIDA também não.

### 4.5 Agrupamento: Grupo e Elemento como campos obrigatórios

**Grupo** é campo categórico obrigatório. Cada valor único forma um grupo independente de comparação.

**Elemento** é campo categórico obrigatório, distinto de Grupo. Identifica a unidade posicionada dentro do grupo.

Nenhum dos dois é opcional — sem Grupo, a V7 deixa de ser benchmarking por grupo; sem Elemento, a unidade analítica colapsa.

Códigos e textos com aparência numérica podem ser usados como Grupo ou Elemento se o Motor Base os classificar como categóricos.

### 4.6 Semântica da medida (T-SEMA)

V7 é sexta consumidora de T-SEMA (ao lado de V2, V3, V9). Três valores oficiais: **Maior-é-melhor · Menor-é-melhor · Neutro**.

**Default:** Neutro, editável em E3.

**Efeito no cálculo: nenhum.** Motor classifica simetricamente em Acima/Na Média/Abaixo com base em `|desvio_percentual|` ante Tolerância, independentemente de T-SEMA. Esta decisão trava a simetria da Tolerância (§4.4) e mantém determinismo do cálculo.

**Efeito na visualização:** mapeamento de cores canônico.
- Maior-é-melhor → Acima associado à cor positiva do sistema · Abaixo à cor negativa · Na Média neutra.
- Menor-é-melhor → Acima associado à cor negativa · Abaixo à positiva · Na Média neutra.
- Neutro → Acima e Abaixo com mesma cor direcional neutra (azul claro/escuro ou similar) · Na Média cinza.

**Efeito no Resumo Executivo:** ordem de apresentação no Bloco 2 Números-âncora adaptada à semântica (maior-é-melhor → maior desvio positivo primeiro; menor-é-melhor → maior desvio negativo primeiro; Neutro → positivo primeiro por convenção). Rótulos dos Blocos 2 e 4 mantidos descritivos e neutros ("maior desvio positivo", "maior desvio negativo", "Top 5 maior desvio positivo") — não interpretativos ("ponto forte", "ponto fraco").

**Persistência em T-MODELO:** sim, padrão V2/V3/V8.

**Warnings:**
- **W-V7-SEMA-DEFAULT** (informativo) — Neutro aceito sem edição.
- **W-V7-SEMA-CUSTOM** (informativo) — editado para Maior/Menor-é-melhor.

### 4.7 Regra de agregação (T-AGRUPA)

V7 consome T-AGRUPA com **default declarado Soma** (padrão V3/V4/V8 consolidado em D-026). Três opções oficiais: **Soma · Média · Contagem**.

**Regra especial Contagem:** dispensa campo de medida. Cálculo opera sobre contagem de linhas por (Grupo, Elemento). E3 apresenta regra de agregação **antes** ou simultaneamente ao campo de medida; campo Medida fica condicionalmente obrigatório (obrigatório quando regra ∈ {Soma, Média}, inaplicável quando regra = Contagem).

**Default adaptado por tipo de medida:**
- Aditiva → Soma.
- Não-aditiva → Média.
- Relativa → Média (aritmética default, ponderada opcional §4.2).

Essa adaptação é coerente com §4.2 e garante que default de agregação respeite natureza do tipo.

### 4.8 Agrupadores adicionais · fora de escopo MVP

V7 MVP opera com **exatamente 1 campo de Grupo + 1 campo de Elemento**. Agrupadores múltiplos (análogos a V4/V8) ficam fora do escopo — adicionariam complexidade de apresentação (tabelas aninhadas) e ambiguidade de leitura ("desvio intra-grupo em qual nível?"). Extensão futura registrada em P-V7-XX-Evo se demanda surgir.

### 4.9 Modelo de configuração (T-MODELO)

V7 consome T-MODELO como todas as 11 visões (§13.3 do CONTEXT).

**Persiste:** campo de Grupo, campo de Elemento, campo de Medida (com tipo), regra de agregação, tolerância, semântica, modo da base, thresholds de leitura customizados (se houve), campo de peso (se usado em Relativa Ponderada).

**Não persiste:** dado fonte (cada uso faz novo upload), pontos efetivos detectados, resultado do cálculo.

**Aplicação em nova base:** campos mapeados por nome; se campo não encontrado, aviso em E3 solicitando seleção manual.

---

## 5. Lógica de processamento

### 5.1 Ordem canônica de cálculo (4 passos)

Implementação na Fundação deve respeitar rigorosamente:

**Passo 1 · Consolidação Elemento+Grupo (T-AGRUPA)**
- Entrada: base analítica normalizada
- Operação: agrupar por (Grupo, Elemento); aplicar regra de agregação declarada
- Saída: base consolidada com 1 linha por (Grupo, Elemento) — `valor_consolidado_elemento`

**Passo 2 · Média do Grupo**
- Entrada: base consolidada do Passo 1
- Operação: para cada Grupo, calcular média aritmética simples de `valor_consolidado_elemento` (ou ponderada quando Relativa com campo de peso)
- Saída: 1 `media_grupo` por Grupo

**Passo 3 · Desvios por Elemento**
- Entrada: base consolidada (Passo 1) + `media_grupo` (Passo 2)
- Operação: para cada (Grupo, Elemento):
  - `desvio_absoluto` = `valor_consolidado_elemento` − `media_grupo`
  - `desvio_percentual` = (`desvio_absoluto` / `media_grupo`) × 100 (com regra de média zero §5.3)
- Saída: base enriquecida com desvios

**Passo 4 · Classificação + Ranking**
- Entrada: base enriquecida + Tolerância declarada
- Operação: classificar cada Elemento (§5.2); ranquear intra-grupo por magnitude do desvio percentual (§5.4)
- Saída: V7Result completo

Ordem preserva consistência entre motor, tela e Excel (prévio §5, adaptado).

### 5.2 Taxonomia oficial V7

| Nível | Valor | Tipo | Quando |
|---|---|---|---|
| Classificação primária (por elemento) | **Acima** | Classe mutuamente exclusiva | `desvio_percentual > +Tolerância` |
| Classificação primária (por elemento) | **Na Média** | Classe mutuamente exclusiva | `|desvio_percentual| ≤ Tolerância` |
| Classificação primária (por elemento) | **Abaixo** | Classe mutuamente exclusiva | `desvio_percentual < −Tolerância` |
| Classificação especial (por elemento) | **NULO_MEDIDA** | Paralela (substitui primária) | Consolidação T-AGRUPA retornou nulo |
| Classificação especial (por grupo) | **Não aplicável** | Paralela (substitui primárias de todos elementos do grupo) | Média do grupo < 0 · média = 0 (homogênea ou heterogênea) |
| Atributo derivado (por elemento) | **Desvio Significativo** | Boolean | Classificação ∈ {Acima, Abaixo} |
| Leitura qualitativa (por grupo) | **Grupo Homogêneo · Assimétrico Acima · Assimétrico Abaixo · Polarizado · Misto** | Leitura de síntese com faixas editáveis | §6.2 Bloco 5 (não estrutural no V7Result) |

**3 classes primárias + 2 classificações especiais + 1 atributo derivado + 5 leituras qualitativas no Resumo Executivo.** Estrutura enxuta adaptada à natureza univariada da V7, coerente com padrão "herança adaptada à natureza analítica" (D-073): V7 tem 3 classes pela natureza univariada contínua, V8 tem 4 classes pela natureza sequencial com estados qualitativamente distintos. Divergência justificada pelo substrato analítico, não por inconsistência.

**Desvio Significativo é atributo derivado**, não classe independente — aba Excel "Desvios Significativos" (§6.3) é recorte filtrado, não cálculo autônomo.

### 5.3 Casos-limite matemáticos

Matriz completa de 6 casos, blindando cálculo determinístico e evitando bugs silenciosos:

| Caso | Classificação | Cálculo | Warning |
|---|---|---|---|
| Grupo com média negativa | Não aplicável (grupo inteiro) | Desvios calculados mas grupo não classificado | W-V7-GRUPO-MEDIA-NEG (alerta forte) |
| Grupo com média zero + todos elementos=0 | Não aplicável (grupo) | Desvio=0 para todos | W-V7-GRUPO-MEDIA-ZERO-HOMO (alerta forte) |
| Grupo com média zero + heterogêneo | Não aplicável (grupo) | Desvio absoluto calculado, % indefinido | W-V7-GRUPO-MEDIA-ZERO-HETERO (alerta forte) |
| Grupo unitário (1 elemento) | Na Média por definição (elemento) + flag baixa utilidade | Desvio=0 | W-V7-GRUPO-UNITARIO (alerta) |
| Grupo com todos valores iguais à média | Na Média (todos elementos) | Desvio=0 para todos | W-V7-GRUPO-HOMOGENEO (informativo) |
| Elemento com consolidação nula | NULO_MEDIDA (elemento) | Não calculado | W-V7-NULO-MEDIDA (alerta forte) |

**Princípio subjacente:** classificação especial "Não aplicável" aplica ao grupo inteiro quando **cálculo percentual é matematicamente indefinido ou não-interpretável** (média negativa ou zero); NULO_MEDIDA aplica por elemento quando **consolidação retornou nulo**. Grupo unitário e grupo homogêneo não são casos de cálculo impossível — são resultados analíticos legítimos (baixa utilidade comparativa vs homogeneidade perfeita), mantidos em Na Média com warnings apropriados.

**V7Result preserva** `desvio_absoluto` e `desvio_percentual` computados mesmo em casos Não aplicável, para que usuário possa inspecionar no Excel; campo `classificacao` registra o status especial.

### 5.4 Ranking intra-grupo (T-RANK)

V7 é sexta consumidora de T-RANK (adicionada a V1/V4/V9/V10/V11). Contrato transversal herdado de D-041 com regra de desempate específica V7.

**Critério de ordenação:** magnitude (módulo) do desvio percentual decrescente. Posição 1 no grupo é o elemento que mais se afasta da média, em qualquer direção. Coerente com atributo Desvio Significativo (T-01) — ranking destaca primeiro os elementos fora da Zona de Média, depois os próximos ao limiar, por último os mais centrais.

**Regra de desempate (4 níveis) — adaptação V7 de D-041 pelo padrão "herança adaptada à natureza analítica" (D-073):**

1. `abs(desvio_percentual)` decrescente (magnitude)
2. `abs(desvio_absoluto)` decrescente (desempate por magnitude em unidades absolutas)
3. Nome do Elemento alfabético case-insensitive
4. Ordem de inserção original

**Tolerância floating point:** 1e-9 (herança D-041).

**Escopo:** intra-grupo exclusivamente. Ranking global (cross-grupo) fora de escopo V7 — preserva posicionamento da visão (benchmarking interno). Aba Detalhe (§6.3) preserva colunas `desvio_absoluto` e `desvio_percentual` com sinal para reordenação manual no Excel se usuário quiser leitura alternativa. Redirecionamento declarativo para V9 (ranking multidimensional consolidado) registrado na nota estática final do Bloco 5 do Resumo Executivo.

**Casos sem ranking:** elementos NULO_MEDIDA e elementos em grupos Não aplicável não recebem ranking (sem desvio calculado, ranking não se aplica).

**Warning:** **W-V7-RANK-EMPATE** (informativo) registra empates resolvidos em cada nível.

---

## 6. O que a visão entrega

### 6.1 Estrutura do resultado (V7Result)

Granularidade-base do V7Result: **1 linha por combinação Elemento + Grupo**.

Contrato:

```
V7Result:
  detalhe_elemento[]:  # 1 linha por (Grupo, Elemento)
    grupo: str
    elemento: str
    valor_consolidado: float | None
    media_grupo: float | None
    desvio_absoluto: float | None
    desvio_percentual: float | None
    classificacao: enum [Acima, Na_Media, Abaixo, NULO_MEDIDA, Nao_Aplicavel]
    desvio_significativo: bool  # derivado: classificacao ∈ {Acima, Abaixo}
    ranking_no_grupo: int | None  # None quando sem ranking
  resumo_grupo[]:  # 1 linha por Grupo
    grupo: str
    n_elementos: int
    media_grupo: float | None
    status_grupo: enum [Calculado, Nao_Aplicavel]
    pct_acima: float
    pct_na_media: float
    pct_abaixo: float
    pct_nulo_medida: float
    maior_desvio_pos: float | None
    maior_desvio_neg: float | None
    amplitude_desvio: float | None  # maior - menor dentro do grupo
    leitura_qualitativa: enum [Homogeneo, Assimetrico_Acima, Assimetrico_Abaixo, Polarizado, Misto, Nao_Aplicavel]
  sintese:
    n_grupos_total: int
    n_grupos_calculados: int
    n_grupos_nao_aplicavel: int
    distribuicao_leituras: dict
    thresholds_ativos: dict  # default ou custom
  parametros_execucao:
    grupo: str  # campo declarado
    elemento: str
    medida: str | None  # None se regra = Contagem
    tipo_medida: enum [Aditiva, Nao_Aditiva, Relativa, Contagem]  # Contagem como tipo implícito quando regra = Contagem
    regra_agregacao: enum [Soma, Media, Contagem]
    campo_peso: str | None  # usado quando Relativa + ponderada
    tolerancia: float
    semantica: enum [Maior_Melhor, Menor_Melhor, Neutro]
    modo_base: enum [Transacional, Pre_Agregado]
  diagnostico:
    warnings: list
    ajustes_leves: list
    decisoes_usuario: list
    linhas_originais: int
    linhas_consolidadas: int
```

### 6.2 Resumo Executivo — 6 blocos fixos (padrão D-044)

**Bloco 1 · Cabeçalho**
Nome da visão, base analisada (arquivo + aba), Grupo, Elemento, Medida + tipo, regra de agregação, tolerância, semântica declarada, modo da base, N de Grupos, N de Elementos, data/hora.

**Bloco 2 · Números-âncora**
- N Total de Elementos · N Total de Grupos · N Grupos Não aplicável
- N Elementos Na Média · N Elementos Acima · N Elementos Abaixo · N Elementos NULO_MEDIDA
- Maior desvio percentual positivo (elemento, grupo, %) · Maior desvio percentual negativo (elemento, grupo, %) — **ordem adaptada a T-SEMA** (§4.6)
- N Elementos com Desvio Significativo · % do total

**Bloco 3 · Distribuição de classificações**
Contagem e % por classe primária (Acima · Na Média · Abaixo) e especiais (NULO_MEDIDA · Não aplicável). Breakdown por grupo quando N_grupos ≤ 10; quando N_grupos > 10, breakdown apenas para top 5 grupos com maior amplitude de desvio.

**Bloco 4 · Elementos destacados**
- Top 5 com maior desvio percentual positivo
- Top 5 com maior desvio percentual negativo
- Top 5 elementos com maior magnitude (|desvio%|) — cruzando grupos
- Top 3 grupos com maior amplitude de desvio · Top 3 grupos com menor amplitude
- Rótulos descritivos neutros (§4.6).

**Bloco 5 · Leitura descritiva por grupo + síntese agregada**

*Parte 5A · Leitura por grupo (tabela)* — 1 linha por grupo com: Grupo · Leitura qualitativa · % Acima · % Na Média · % Abaixo · N Elementos. Ordenada por status Não aplicável último; entre calculados por N_elementos decrescente ou alfabético (decisão final em Spec S-V7).

*Parte 5B · Síntese agregada* — narrativa textual consolidando a distribuição das leituras entre grupos. Exemplo: *"Dos 12 grupos analisados: 8 são Homogêneos (67%), 3 são Assimétricos Abaixo (25%), 1 é Polarizado (8%). 2 grupos foram classificados como Não aplicável (cálculo estrutural limitado)."*

*Parte 5C · Thresholds ativos* — resumo dos thresholds em uso: *"Thresholds ativos: Homogêneo ≥70% Na Média · Assimétrico ≥60% em uma direção · Polarizado ≥25% em cada direção · [Default / Customizado]."*

*Parte 5D · Nota estática final:* *"Para análise aprofundada de dispersão estatística interna dos grupos (IQR, outliers, distribuição), considere V5 · Comportamento e Dispersão. Para ranking consolidado de elementos com múltiplas métricas e direções declaradas, considere V9 · Perfil de Ranking por Métricas."*

**5 leituras qualitativas de grupo (candidatas + Não aplicável):**

| Leitura | Condição default | Métrica-base |
|---|---|---|
| **Grupo Homogêneo** | ≥ 70% dos elementos são Na Média | % Na Média por grupo |
| **Grupo Assimétrico Acima** | ≥ 60% dos elementos são Acima OU Acima/(Acima+Abaixo) ≥ 75% | % Acima e proporção |
| **Grupo Assimétrico Abaixo** | ≥ 60% dos elementos são Abaixo OU Abaixo/(Acima+Abaixo) ≥ 75% | % Abaixo e proporção |
| **Grupo Polarizado** | Acima ≥ 25% E Abaixo ≥ 25% | N Acima e N Abaixo |
| **Grupo Misto** | Nenhuma das acima | residual |
| **Grupo Não aplicável** | status_grupo = Não aplicável | estrutural (§5.3) |

**Ordem de teste (lógica de resolução):** Não aplicável → Polarizado → Assimétrico Acima/Abaixo → Homogêneo → Misto.

**Thresholds editáveis** em "Configurações avançadas" de E3/E5. **W-V7-LEITURA-DEFAULT** registra defaults aceitos; **W-V7-LEITURA-CUSTOM** registra thresholds editados.

**Bloco 6 · Qualidade estrutural**
N ajustes leves · N alertas · N elementos NULO_MEDIDA · N grupos Não aplicável (decomposto por causa: média negativa, média zero homogênea, média zero heterogênea) · N grupos unitários · N grupos homogêneos · modo declarado · tipo da medida declarado · thresholds customizados (se houve) · campo de peso usado (se houve).

### 6.3 Exportação Excel — 6 abas oficiais

| # | Aba | Conteúdo |
|---|---|---|
| 1 | **Resumo Executivo** | 6 blocos do §6.2 |
| 2 | **Mapa de Grupos** | 1 linha por Grupo: Grupo · N Elementos · Média · Maior desvio+/- · Amplitude · N Acima/Na Média/Abaixo · Leitura qualitativa · status. Ordenação default por amplitude de desvio decrescente (grupos mais dispersos primeiro) |
| 3 | **Detalhe por Elemento** | Base analítica completa: 1 linha por (Grupo, Elemento) com valor_consolidado, media_grupo, desvio_absoluto, desvio_percentual, classificação, ranking_no_grupo. Ordenação default: Grupo alfabético → ranking_no_grupo crescente |
| 4 | **Desvios Significativos** | Recorte filtrado: elementos com desvio_significativo=True; mesmas colunas da aba Detalhe; ordenação por magnitude do desvio percentual decrescente **cruzando grupos** (destaca extremos da análise inteira) |
| 5 | **Parâmetros** | Configuração declarada vs efetiva: grupo, elemento, medida + tipo, regra de agregação, tolerância, semântica, modo, thresholds de leitura customizados, campo de peso |
| 6 | **Diagnóstico** | Todos warnings + categoria T-DIAG (AJUSTE_LEVE / DECISAO_USUARIO) + linhas originais vs consolidadas + lista de grupos Não aplicável com causa + elementos NULO_MEDIDA — **sempre última aba (D-017)** |

**Aba Mapa de Grupos substitui "Resumo por Grupo" do prévio** — absorve conteúdo original e adiciona amplitude + leitura qualitativa + status.

**Aba Dados Brutos do prévio descartada** (herança V8 D-078) — aba Detalhe por Elemento cobre auditoria analítica; Diagnóstico registra "linhas originais vs consolidadas" para rastreabilidade.

**Aba Desvios Significativos preservada como recorte filtrado** (não cálculo autônomo) — ordenação cross-grupos por magnitude, mas preservando coluna Grupo para cada linha; elementos NULO_MEDIDA e em grupos Não aplicável não aparecem (sem desvio significativo por definição).

**Filtros ativos em todas as 6 abas** (padrão D-017). **Tela e Excel não divergem** (princípio prévio §10.1 + D-017).

---

## 7. Warnings catalogados (35)

### 7.1 Bloqueios (6 com código W-V7-* + bloqueios estruturais numerados em §8)

- **W-V7-MODO-VIOLACAO** — Modo Pré-agregado declarado mas duplicatas detectadas (§4.1).
- **W-V7-MEDIDA-ESTADO** — Tipo Estado/Situação detectado/declarado; redirecionamento V6 (§4.2).
- **W-V7-GRUPOS-INVIAVEL** — Cardinalidade do Grupo > 1.000 (§8).
- **W-V7-ELEMENTOS-INSUFICIENTES** — Todos os grupos com < 2 elementos válidos (§8).
- **W-V7-VOLUME-INVIAVEL** — Total > 1.000.000 elementos (§8).

### 7.2 Alertas (11)

**Alertas fortes (8):**
- **W-V7-NEG-MEDIDA** — presença de valores negativos na medida (§4.2).
- **W-V7-GRUPO-MEDIA-NEG** — grupo com média negativa; classificação Não aplicável (§5.3).
- **W-V7-GRUPO-MEDIA-ZERO-HOMO** — grupo com média zero e todos elementos=0 (§5.3).
- **W-V7-GRUPO-MEDIA-ZERO-HETERO** — grupo com média zero heterogênea (§5.3).
- **W-V7-RELATIVA-MEDIA-ARIT** — média aritmética aceita em tipo Relativa sem ponderação (§4.2).
- **W-V7-NULO-MEDIDA** — elemento com consolidação nula (§5.3).
- **W-V7-GRUPOS-CRITICO** — cardinalidade do Grupo 201-1.000 (§8).
- **W-V7-VOLUME-ALERTA** — total 200.001-500.000 (§8).
- **W-V7-VOLUME-CRITICO** — total 500.001-1.000.000 (§8).

**Alertas regulares (3):**
- **W-V7-GRUPO-UNITARIO** — grupo com 1 elemento; flag baixa utilidade comparativa (§5.3).
- **W-V7-GRUPOS-MUITOS-ALERTA** — cardinalidade do Grupo 51-200 (§8).
- **W-V7-GRUPO-CRITICO** — grupo com 10.000+ elementos (§8).

### 7.3 Informativos (18)

- **W-V7-MODO-TRANS-DEFAULT** · **W-V7-MODO-TRANS-CUSTOM** · **W-V7-MODO-PREAGG-DEFAULT** · **W-V7-MODO-PREAGG-CUSTOM** (§4.1)
- **W-V7-TIPO-DEFAULT** · **W-V7-TIPO-CUSTOM** (§4.2)
- **W-V7-RELATIVA-MEDIA-POND** (§4.2)
- **W-V7-TOLERANCIA-DEFAULT** · **W-V7-TOLERANCIA-CUSTOM** (§4.4)
- **W-V7-SEMA-DEFAULT** · **W-V7-SEMA-CUSTOM** (§4.6)
- **W-V7-GRUPO-HOMOGENEO** (§5.3)
- **W-V7-RANK-EMPATE** (§5.4)
- **W-V7-LEITURA-DEFAULT** · **W-V7-LEITURA-CUSTOM** (§6.2 Bloco 5)
- **W-V7-GRUPOS-MUITOS-AVISO** · **W-V7-GRUPO-VOLUMOSO** · **W-V7-VOLUME-AVISO** (§8)

---

## 8. Bloqueios operacionais e escala de cardinalidade

### 8.1 Bloqueios estruturais (12)

1. Arquivo ilegível ou corrompido
2. Estrutura inválida (arquivo vazio, aba sem dado, sem coluna numérica quando regra ≠ Contagem)
3. Nenhum campo categórico elegível como Grupo
4. Nenhum campo categórico elegível como Elemento (distinto do Grupo)
5. Nenhum campo numérico elegível como Medida (quando regra ∈ {Soma, Média})
6. Medida com 100% de nulos
7. Menos de 2 elementos válidos por grupo em TODOS os grupos (**W-V7-ELEMENTOS-INSUFICIENTES**)
8. Tipo de medida = Estado/Situação (**W-V7-MEDIDA-ESTADO** · redirecionamento V6)
9. Modo Pré-agregado declarado mas duplicatas detectadas (**W-V7-MODO-VIOLACAO**)
10. Tolerância inválida (≤ 0 ou ≥ 1000%)
11. Cardinalidade do campo Grupo > 1.000 (**W-V7-GRUPOS-INVIAVEL**)
12. Total de elementos > 1.000.000 (**W-V7-VOLUME-INVIAVEL** · limite físico Excel)

### 8.2 Escala de cardinalidade V7 · 3 eixos hierárquicos

**V7 tem natureza hierárquica-aditiva** (elementos dentro de grupos, não cruzados com), diferente de V8 (matricial multiplicativa). Escala adaptada.

**Eixo 1 · Cardinalidade do campo Grupo (N grupos):**

| Patamar | Comportamento | Warning |
|---|---|---|
| 1-20 | Normal | — |
| 21-50 | Aviso informativo | W-V7-GRUPOS-MUITOS-AVISO |
| 51-200 | Alerta · confirmação recomendada | W-V7-GRUPOS-MUITOS-ALERTA |
| 201-1.000 | Alerta forte · confirmação obrigatória · sugere campo alternativo | W-V7-GRUPOS-CRITICO |
| 1.001+ | **Bloqueio** | W-V7-GRUPOS-INVIAVEL |

**Eixo 2 · Elementos por grupo:**

| Patamar | Comportamento | Warning |
|---|---|---|
| Todos grupos < 2 elementos | **Bloqueio** | W-V7-ELEMENTOS-INSUFICIENTES |
| Grupos com < 3 elementos (heterogêneo) | Aviso por grupo | W-V7-GRUPO-UNITARIO (§5.3 cobre 1-elemento) |
| Grupo com 500+ elementos | Aviso informativo | W-V7-GRUPO-VOLUMOSO |
| Grupo com 10.000+ elementos | Alerta | W-V7-GRUPO-CRITICO |

**Eixo 3 · Total de elementos:**

| Patamar | Comportamento | Warning |
|---|---|---|
| ≤ 50.000 | Normal | — |
| 50.001 - 200.000 | Aviso | W-V7-VOLUME-AVISO |
| 200.001 - 500.000 | Alerta forte · confirmação recomendada | W-V7-VOLUME-ALERTA |
| 500.001 - 1.000.000 | Alerta forte · confirmação obrigatória | W-V7-VOLUME-CRITICO |
| 1.000.001+ | **Bloqueio** | W-V7-VOLUME-INVIAVEL |

### 8.3 Diretrizes de performance (9)

**Herdadas de V3/V8 (7):**

1. Pré-validação de volume antes de alocação pesada (total de elementos pré-checado).
2. Índices hash para consolidação T-AGRUPA (grouping por (Grupo, Elemento) sem sort global).
3. Filtro de casos estruturalmente inválidos cedo no pipeline (grupos Não aplicável não entram em cálculo de ranking).
4. Cálculo em memória com estruturas colunares.
5. Ordenação estável determinística (critério T-RANK com tolerância 1e-9).
6. Diagnóstico em streaming (warnings coletados durante pipeline).
7. Geração Excel com openpyxl em modo otimizado quando volume > 100.000 linhas.

**Específicas V7 (2 novas):**

8. **Particionamento por grupo antes de cálculos derivados** — amplitude, leitura qualitativa, ranking_no_grupo computados **dentro de cada grupo** isoladamente; permite paralelização futura.
9. **Leitura qualitativa calculada em passe único** sobre distribuições de classificação por grupo — teste ordenado (Não aplicável → Polarizado → Assimétrico Acima/Abaixo → Homogêneo → Misto) sem cálculos redundantes.

---

## 9. Fronteira com Módulo 2 (TabloPrep)

V7 opera sobre base consolidada única. Operações de preparação que podem alimentar V7 ficam no domínio do Módulo 2 (TabloPrep):

- **Empilhamento multi-aba** (cenários onde dados vêm em abas separadas por período, unidade, etc.) — M2.STACK candidata (D-063).
- **Normalização textual de Grupo e Elemento** (padronização de nomes antes do grouping) — M2.NORMALIZE candidata (D-057).
- **Deduplicação prévia** (se base Transacional tem registros repetidos estruturalmente) — operação M2 futura.

V7 MVP não implementa essas operações. Microcopy em nota de seleção de aba orienta o usuário quando N ≥ 3 abas detectadas.

---

## 10. Pontos de atenção (riscos analíticos conhecidos)

**Dupla agregação.** Armadilha estrutural central. Implementação precisa blindar em teste unitário que média do grupo **nunca** é calculada sobre linhas brutas. §4.3 e §5.1 formalizam a ordem.

**Grupos de escalas muito diferentes.** Desvio percentual é comparável entre grupos, mas desvio absoluto não. Ranking intra-grupo mitiga; usuário consciente do trade-off pode alternar ordenação no Excel.

**Média aritmética de taxas.** Tipo Relativa sem ponderação distorce quando volumes diferem. §4.2 oferece campo de peso opcional com alerta forte explícito.

**Grupos pequenos com média instável.** Grupos com 2-3 elementos têm média fortemente influenciada por um outlier. Warnings alertam; interpretação é do usuário.

**Interpretação da direção do desvio.** Sistema apresenta sinal matemático (Acima = +%, Abaixo = −%); interpretação de "bom/ruim" é atribuída pela T-SEMA em camada visual (cor, ordem de apresentação), não no cálculo.

**Elementos com mesmo nome em grupos distintos.** A unidade analítica é (Grupo, Elemento) — mesmo nome de elemento em grupos distintos é tratado como duas unidades analíticas independentes. Comportamento esperado; Diagnóstico não sinaliza.

---

## 11. Relação com Fundação e retroação sobre V9

### 11.1 Requisitos novos para a Fundação

G-FUND precisa absorver os seguintes requisitos originados em V7:

- **T-AGRUPA** com no-op validado quando modo = Pré-agregado (F-MOT).
- **T-RANK** com regra_desempate parametrizável em 4 níveis para V7 (extensão de D-041 — F-TRANS).
- **T-SEMA** com 3 valores (Maior/Menor/Neutro) — mesma implementação V2/V3/V9 (F-TRANS).
- **T-AGRUPA** com suporte a média ponderada por campo de peso (extensão; F-TRANS).
- **Detecção automática de duplicatas** em amostragem para default declarado de modo (F-MOT).
- **Classificação especial Não aplicável por grupo** e **NULO_MEDIDA por elemento** como valores válidos do campo `classificacao` no V7Result (F-MOT).
- **Particionamento por grupo** como pré-requisito arquitetural antes de cálculos derivados (F-MOT).
- **Exportação Excel com 6 abas** incluindo aba Mapa de Grupos aninhada apenas se houver sub-agrupadores futuros (F-EXP).

### 11.2 Retroação sobre V9 (registrada)

DCV-V9 receberá §2.3 "Relação com V7" simétrico ao §2.3 deste DCV na sua próxima revisão natural — refino DCV-V9, em sequência direta após aprovação deste DCV-V7. Análogo a retroação V3→V8 registrada em D-060 (cumprida antecipadamente em D-073 porque V3 já estava aprovada); retroação V11→V1 permanece aberta (D-058).

Neste caso V7→V9 a retroação é cumprida na ordem natural do refino, sem pausa adicional. DCV-V9 absorve a tabela comparativa V7×V9 (com células hoje marcadas *(a confirmar)* preenchidas) e o parágrafo de família.

---

## 12. Roadmap pós-MVP (P-V7-XX-Evo)

| ID | Evolução | Origem no refino | Rationale |
|---|---|---|---|
| **P-V7-01-Evo** | Detecção automática de campo de peso adequado em tipo Relativa | T-05 | Default hoje é média aritmética; detecção automática seria melhoria UX |
| **P-V7-02-Evo** | Múltiplas medidas por execução | prévio §3.3 rejeitado MVP | Comparar desvio em 2-3 medidas simultaneamente por elemento |
| **P-V7-03-Evo** | Tolerância por grupo (não uniforme) | T-06 rejeitado | Grupos de escalas muito diferentes com tolerâncias distintas |
| **P-V7-04-Evo** | Benchmarks externos (meta declarada × calculada) | prévio P0.8 · V7 é "interna" por definição | Extensão com meta externa opcional |
| **P-V7-05-Evo** | Ranking global opcional (cross-grupo) | T-10 rejeitado | Caso de uso "ranking geral" com manutenção do intra-grupo |
| **P-V7-06-Evo** | Leituras qualitativas de grupo com mais classes | T-08/T-11 rejeitado | Granularidade fina adicional (Levemente Assimétrico etc.) |

---

## 13. Nomenclatura oficial da V7

Termos oficiais consolidados em T-01 da sessão de refino:

| Termo oficial | Definição curta |
|---|---|
| **Grupo** | Campo categórico obrigatório que segmenta a base em unidades independentes de comparação |
| **Elemento** | Unidade categórica posicionada dentro do grupo (vendedor, fornecedor, centro de custo) |
| **Medida** | Campo numérico alvo do cálculo de desvio; opcional quando regra = Contagem |
| **Tipo de Agregação** | Regra de consolidação do Elemento dentro do Grupo (Soma · Média · Contagem) |
| **Média do Grupo** | Média aritmética simples dos Elementos consolidados do grupo (ou ponderada em Relativa) |
| **Desvio Absoluto** | Valor do Elemento − Média do Grupo (mesma unidade da medida) |
| **Desvio Percentual** | (Desvio Absoluto ÷ Média do Grupo) × 100 |
| **Tolerância** | Parâmetro declarado que define a Zona de Média (default ±5%) |
| **Zona de Média** | Região classificatória derivada da Tolerância; elementos dentro são Na Média |
| **Classificação** | Uma de três classes primárias: Acima · Na Média · Abaixo; + classificações especiais NULO_MEDIDA (elemento) e Não aplicável (grupo) |
| **Desvio Significativo** | Atributo derivado: Classificação ∈ {Acima, Abaixo} |
| **Semântica** | Direção de leitura Maior-é-melhor / Menor-é-melhor / Neutro (T-SEMA) |

**Sinônimos aceitáveis em microcopy:** "Faixa de Tolerância" para "Zona de Média" em contexto pedagógico. **Evitar:** "zona de equilíbrio", "região neutra", "alvo", "meta" (implicariam semântica não prevista).

---

## 14. Posicionamento C.5

V7 preserva e reforça o princípio C.5 em múltiplos pontos:

- **Consolidação obrigatória Elemento+Grupo** antes de calcular média — sistema não decide "média sobre linhas brutas é válida" (§4.3).
- **Modo da base declarado** (Transacional × Pré-agregado) — padrão default declarado com detecção na amostragem (§4.1).
- **Tipo da medida declarado** com tratamento adaptado — motor propõe, usuário confirma (§4.2).
- **Tolerância declarada** em Zona de Média com papel duplo — sistema não "decide faixa de normalidade" pelo usuário (§4.4).
- **Semântica T-SEMA declarada** — motor default Neutro; cálculo sempre simétrico (§4.6).
- **Classificação especial Não aplicável** quando cálculo percentual não produz leitura interpretável — sistema não inventa valor em caso indefinido (§5.3).
- **Ranking intra-grupo** preservando posicionamento analítico da visão (benchmarking interno); ranking global fora de escopo (§5.4).
- **Leituras qualitativas de grupo** no Bloco 5 com faixas editáveis — sistema propõe rótulo, usuário refina thresholds; leitura narrativa, não classificação estrutural (§6.2).
- **Microcopy declarativa autossuficiente** em nota estática final do Bloco 5 — redirecionamentos declarativos para V5 e V9; nenhuma visão menciona outra em interface operacional (§6.2 Parte 5D).

---

## 15. Integração com Fundação

### 15.1 Transversais consumidos

- **T-AGRUPA** — consolidação Elemento+Grupo com Soma default (regra declarada); ponderação por campo de peso em Relativa
- **T-SEMA** — default Neutro; afeta visualização e ordem de apresentação, não cálculo
- **T-RANK** — sexta consumidora; ranking intra-grupo por magnitude do desvio percentual com desempate em 4 níveis
- **T-DIAG** — todos os warnings V7 + categorização AJUSTE_LEVE / DECISAO_USUARIO + linhas originais vs consolidadas
- **T-MODELO** — persistência de parâmetros de configuração (padrão §13.3 do CONTEXT)

### 15.2 Transversais não aplicáveis a V7

- **T-EIXO** — V7 não tem eixo sequencial; análise é univariada em snapshot único
- **T-ACUM / T-ABC** — V7 não calcula acumulado nem classifica por limiares de participação
- **T-PIVOT** — V7 opera sobre base plana; não há pivot
- **T-DUAL** — V7 opera sobre base única; não há dualidade de fontes
- **T-FUZZY / T-CONCAT** — V7 não faz match probabilístico nem composição de campos

### 15.3 Diretrizes de performance

9 diretrizes formalizadas em §8.3 (7 herdadas V3/V8 + 2 específicas V7).

---

## 16. Decisões geradas

Refino DCV-V7 gerou 9 decisões específicas em DECISIONS.md (D-081 a D-089) + 1 sumário (D-090):

- **D-081** · Posicionamento Família D + retroação diferida V9 (T-02)
- **D-082** · Modo da base V7 + consolidação obrigatória + 4 passos canônicos (T-04)
- **D-083** · Tipos de medida V7 com tratamento adaptado (T-05)
- **D-084** · Tolerância ±5% default declarado simétrico percentual (T-06)
- **D-085** · Casos-limite matemáticos V7 (matriz de 6 casos + Não aplicável + NULO_MEDIDA) (T-07)
- **D-086** · Taxonomia oficial V7 (3+2+1 · leitura qualitativa no Bloco 5) (T-08)
- **D-087** · T-SEMA aplicada a V7 (visual/ordem · não cálculo) (T-09)
- **D-088** · T-RANK V7 (sexta consumidora · intra-grupo por magnitude · 4 níveis desempate) (T-10)
- **D-089** · Resumo Executivo V7 + 6 abas Excel + bloqueios + diretrizes + roadmap (T-11, T-12, T-13 consolidados)
- **D-090** · Sumário do refino DCV-V7 (13 pendências fechadas em sessão única)

T-01 (vocabulário) e T-03 (fronteiras V5/V4) consolidados sem D-XXX específica — aplicação de padrões já consolidados (§13 e §2.2 respectivamente).

---

## 17. Pendências do refino (histórico)

Fila de 13 pendências trabalhada em 4 blocos:

**Bloco A · Posicionamento e fronteira**
- T-01 · Vocabulário canônico V7
- T-02 · Família D + retroação V9
- T-03 · Fronteira V5 e V4

**Bloco B · Cálculo e regras estruturais**
- T-04 · Consolidação + dupla agregação
- T-05 · Tipos de medida + negativos
- T-06 · Tolerância default declarado
- T-07 · Casos-limite matemáticos

**Bloco C · Classificação, semântica e ranking**
- T-08 · Taxonomia oficial (3 classes + especiais)
- T-09 · T-SEMA (consumidora natural · visual)
- T-10 · T-RANK intra-grupo (sexta consumidora)

**Bloco D · Saída e operação**
- T-11 · Resumo Executivo 6 blocos
- T-12 · Excel 6 abas
- T-13 · Bloqueios + performance + roadmap

Todas fechadas em sessão única.

---

## 18. Referências

- CONTEXT.md §3 (método) · §4 (famílias) · §6 (transversais) · §9 (princípios C.5 + padrões derivados)
- DECISIONS.md D-017 (Diagnóstico última aba) · D-024 (default declarado) · D-025/D-036 (taxonomia de tipos) · D-026 (T-AGRUPA) · D-041 (T-RANK configurável) · D-044 (Resumo 6 blocos) · D-058/D-060 (microcopy declarativa) · D-066 (Não aplicável V3) · D-073 (herança adaptada) · D-076 (warning vs conteúdo) · D-078 (estrutura Excel V8) · D-081 a D-090 (este refino)
- DCV-V3 · precedente direto de abertura de família e 6 blocos Resumo Executivo
- DCV-V8 · precedente de taxonomia com classificação consolidada e retroação diferida cumprida
- DCV-V4 · precedente de taxonomia de tipos de medida com tratamento adaptado
- GLOSSARIO.md §4 T-AGRUPA / T-SEMA / T-RANK / T-DIAG / T-MODELO · §10 padrões de método

---
