# DCV-V6 · Relacionamento entre Dimensões

**Família:** E · Estrutura interna do recorte (2ª e última visão da família · fecha o par autônomo distante · D-110 lado 2)
**Status:** Aprovado
**Sessão de refino:** 20/04/2026 · sessão única · 16 pendências fechadas
**Decisões geradas:** D-111 a D-120 + D-121 (sumário)

---

## 1. Propósito da visão

V6 responde uma pergunta única e bem delimitada: *"como dois campos categóricos se relacionam entre si dentro de uma base, quais combinações concentram mais valor ou volume, quais têm baixa relevância e quais combinações não aparecem na estrutura observada?"*. Ela analisa **cruzamento estrutural**, não movimento, não composição univariada, não posição relativa, não dispersão univariada. O que V6 entrega é a leitura da matriz formada pelo cruzamento de dois campos categóricos — intensidade de cada célula, classificação de densidade, e exposição explícita das lacunas estruturais (combinações ausentes) como conteúdo analítico primário.

V6 não responde perguntas de outras visões: o que mudou entre dois estados pertence à V2; como algo evoluiu ao longo de uma sequência pertence à V3; quanto cada elemento representa dentro de um total pertence à V4 ou V10; quem está acima ou abaixo da média do seu grupo pertence à V7; quem se destaca quando consideradas múltiplas métricas simultâneas pertence à V9; como valores se distribuem estatisticamente em um campo numérico pertence à V5. V6 fica com o terreno distintivo do **cruzamento bivariado categórico** — pergunta natural em análises de portfólio (categoria × região), de estrutura de clientela (segmento × canal), de operações (tipo de transação × natureza contábil).

A V6 mostra o cruzamento. O usuário interpreta a causa. Combinação ausente não é erro, não é obrigatoriedade de negócio, não é anomalia — é fato matemático sobre o produto cartesiano observado. A interpretação fica para o usuário.

---

## 2. Posicionamento analítico

### 2.1 O cenário real que a V6 atende

Análise de cruzamento entre duas dimensões categóricas da mesma base para entender a estrutura do relacionamento: faturamento por Categoria × Região, quantidade de pedidos por Canal × Segmento, valor contábil por Conta × Centro de Custo, ocorrências por Tipo de Evento × Origem. Casos onde o usuário precisa entender:

- Quais combinações concentram valor ou volume (Dominante)
- Quais combinações têm peso intermediário (Relevante)
- Quais combinações são residuais na matriz (Residual)
- Quais combinações **não aparecem** no cruzamento observado (Ausente)
- Como a matriz se comporta globalmente (densidade, concentração, simetria entre eixos)

V6 é segunda e última visão da **Família E · Estrutura interna do recorte** (reformulada em D-110). V5 (dispersão univariada numérica) é a outra visão da família. V5 e V6 são **operacionalmente distantes** — não compartilham transversais centrais, não navegam fronteira em interface operacional, e a relação entre as duas é tratada de forma enxuta nesta família (§2.3).

### 2.2 Fronteiras com visões vizinhas

**V6 × V4 (Composição).** V4 mostra composição univariada ordenada: quanto cada elemento representa do total geral, com Curva ABC e Curva Pareto destacando os que compõem maior fatia. V6 mostra cruzamento bivariado: como dois campos categóricos se relacionam entre si, com densidade por célula, lacunas estruturais e classificação por combinação. Quem responde *"quais fornecedores concentram meu faturamento?"* usa V4 (agrupador único, medida numérica, Curva ABC). Quem responde *"como o faturamento se distribui na matriz Categoria × Fornecedor — quais cruzamentos concentram valor e quais cruzamentos não existem?"* usa V6. Apesar de V6 importar vocabulário semelhante (Dominante/Residual), a natureza analítica é distinta: V4 ordena N elementos em um eixo; V6 cruza N × M células numa matriz onde células ausentes *são conteúdo*.

**V6 × V10 (Pareto).** V10 é view especializada sobre V4 Modo 2 (composição com corte Pareto 80/95). V6 nunca é view especializada de ninguém — autônoma na Família E. Quem quer *"20% das combinações que concentram 80% do valor da matriz"* está oscilando entre os dois: V6 não aplica corte Pareto como critério central (aplica critério por célula, por ausência, por cardinalidade da matriz); V10 é sobre elementos univariados, não sobre células de matriz. A fronteira é *operação monovariada × operação bivariada*.

**V6 × V8 (Recorrência e Ciclo de Vida).** Ambas têm matriz visual como coração. V8 é Entidade × Ponto do Eixo (coluna temporal ordenada); V6 é Categoria1 × Categoria2 (duas categorias sem ordem inerente). V8 detecta presença/ausência de entidade em pontos ordenados (evolução no tempo); V6 detecta presença/ausência de cruzamentos na matriz (lacunas estruturais). V8 consome T-EIXO; V6 não consome nada que ordene os eixos. Aplicação de D-076: ausência é conteúdo primário em ambas, com naturezas distintas (em V8, entidade ausente no tempo = mudança; em V6, célula ausente = lacuna estrutural).

**V6 × V7/V9 (Posição relativa).** V7 e V9 trabalham com campo numérico + benchmark interno; V6 trabalha com matriz bivariada categórica + medida opcional. Quem pensa *"quero ver como valor médio varia por Categoria × Região"* oscila entre: V7 (se Categoria é Elemento e Região é Grupo, desvio da média do grupo), V6 (se Categoria e Região são os dois eixos do cruzamento, densidade da célula com medida = Média), ou V9 (se há várias métricas a rankear). V7/V9 produzem posição relativa do elemento frente a benchmark interno; V6 produz intensidade da combinação categórica frente ao total da matriz.

V6 também se distingue trivialmente de V2 (comparação entre estados), V3 (sequência ordenada) e V1/V11 (confronto entre bases) pela natureza estrutural — todas essas visões operam sobre objeto diferente de uma matriz categórica bivariada intra-base. Nenhuma dessas fronteiras é navegada em interface operacional. Microcopy declarativa autossuficiente em cada bloco · sem botão "ir para V4" · sem sugestão "experimente também V8".

### 2.3 Relação com V5 (par autônomo da Família E)

V6 e V5 convivem como visões da Família E · Estrutura interna do recorte. As duas operam sobre recortes distintos da base — V6 bivariado categórico (cruzamento de dois campos categóricos por execução), V5 univariado numérico (um campo numérico por execução). Não compartilham transversais centrais nem apresentam fronteira navegada operacionalmente. O que une V6 e V5 na mesma família é o nível mais abstrato: ambas expõem propriedades estruturais internas de um recorte da base sem comparar com referência externa, sem benchmark interno por grupo, sem eixo ordenado, sem total geral. DCV-V5 §2.3 declarou que V6 declararia seu posicionamento simétrico nesta família quando refinado — **V6 declara aqui**, fechando o par autônomo distante da Família E dos dois lados.

A diferença substantiva entre Família E e as Famílias B (V3/V8 · par operacional próximo via T-EIXO) e D (V7/V9 · par operacional próximo via T-AGRUPA + T-SEMA + T-RANK) justifica a adaptação no método de posicionamento de família formalizada em D-110: famílias com par operacionalmente próximo merecem tabela de retroação diferida com células *(a confirmar)* (D-060 V3→V8 · D-081 V7→V9); Família E com par operacionalmente distante merece declaração enxuta de convivência sem retroação diferida formal. Aplicação do padrão "herança adaptada à natureza analítica" (D-073) ao próprio método de posicionamento de família honrada dos dois lados. **Nenhum D-XXX de retroação gerado neste refino.** **Família E fechada em Fase 0 após aprovação deste DCV · último DCV da Fase 0 · após V6 aprovada, Fase 0 · Compreensão está CONCLUÍDA.**

### 2.4 Posicionamento V6 na Família E

V6 e V5 expõem propriedades estruturais internas de um recorte da base — mas de objetos estruturalmente distintos. V5 opera sobre **uma série de observações numéricas** (univariada); V6 opera sobre **uma matriz de interseções entre duas dimensões categóricas** (bivariada). Em V5, a unidade analítica é a observação individual do campo numérico. Em V6, a unidade analítica é a **célula da matriz** — cada slot no cruzamento (Eixo1=X ∧ Eixo2=Y) do produto cartesiano observado. Esta é a primeira visão do Módulo 1 em que a unidade analítica inclui objetos **calculados como ausentes** a partir do cruzamento — aplicação pura do padrão D-076 ("ausência como conteúdo primário").

### 2.5 Unidade analítica da V6

A unidade analítica da V6 é a **célula** da matriz — cada slot representado pelo par (Eixo1=X, Eixo2=Y) no produto cartesiano observado. V6 não consolida valores por linha individual da base (como V5 faz); V6 consolida valores **por célula** e classifica **cada célula**.

Esta unidade é distintiva em relação às outras famílias:
- V4/V10 (Composição) · unidade é elemento ordenável (1 dimensão)
- V7 (Desvio) · unidade é Elemento+Grupo (chave composta com grupo interno)
- V8 (Recorrência) · unidade é Entidade+PontoDoEixo (chave composta com eixo ordenado)
- V9 (Ranking) · unidade é Identificador com múltiplas métricas
- V5 (Distribuição) · unidade é observação individual (não consolidada)
- **V6 (Relacionamento) · unidade é célula na matriz de cruzamento (chave composta categórica não-ordenada, que inclui células ausentes calculadas)**

A consequência operacional: V6 consome T-AGRUPA com consumo **padrão** (não adaptação V5-específica · ver §4.2) — é o caso típico da família de consumidoras V4/V7/V8/V9, não o caso especial de V5 via D-073.

---

## 3. O que a visão recebe

### 3.1 Estrutura de entrada

V6 aceita **apenas estrutura POR_COLUNAS no MVP**. Base chega em formato plano com pelo menos 3 colunas: coluna Eixo 1 (categórica-elegível) · coluna Eixo 2 (categórica-elegível) · opcionalmente coluna Campo Numérico da Medida quando a Medida escolhida não for Contagem.

**POR_LINHAS fora de escopo MVP.** Bloqueio B-V6-POR-LINHAS com microcopy redirecional: *"V6 MVP aceita apenas estrutura POR_COLUNAS · base em formato long precisa de pivot prévio · considere M2.PIVOT futuro"*. Roadmap P-V6-01-POR-LINHAS-Evo preserva o gancho.

Detecção de POR_LINHAS vs POR_COLUNAS é responsabilidade do motor_base com default declarado editável (motor propõe POR_COLUNAS quando ambíguo; usuário confirma ou altera).

### 3.2 Multi-aba

Arquivo com múltiplas abas disponível · usuário escolhe uma aba em etapa dedicada da configuração. Escolha registrada em Parâmetros com W-V6-MULTIABA-ESCOLHA (informativo).

**Empilhamento de múltiplas abas estruturalmente idênticas** (ex: uma aba por mês) fica em roadmap **P-V6-02-MULTIABA-Evo** ligado a **M2.STACK** (D-063). V6 se junta a V3 (P-V3-01-Evo) e V8 (P-V8-01-Evo) como 3º consumidor futuro declarado do mesmo M2.STACK — reforça o candidato arquitetural para G-FUND decidir posicionamento (transversal da Fundação · parte de M2 · capability compartilhada).

### 3.3 Campos obrigatórios

**Eixo 1 e Eixo 2** · ambos obrigatórios · ambos precisam ser classificados como categórico-elegíveis pelo motor_base (§4.5a) · o mesmo campo não pode ocupar os dois eixos simultaneamente (B-V6-EIXOS-IGUAIS).

**Medida** · tipo de medida é obrigatório. 3 tipos canônicos V6 MVP: Contagem (default quando não há campo numérico selecionado) · Soma · Média. Quando Medida = Soma ou Média, **Campo Numérico** é obrigatório (§4.4).

### 3.4 Fora de escopo de entrada

- Campos com menos de 5 registros válidos após exclusão de nulos nos eixos (bloqueio B-V6-MINIMO-OPERACIONAL).
- Mais de 2 eixos simultâneos (V6 é bivariada por execução · matrizes 3D fora de escopo permanente).
- Análise comparativa entre duas matrizes (roadmap P-V6-07-EVOLUCAO-ENTRE-EXECUCOES-Evo).
- Regras de agregação Máximo e Mínimo (roadmap P-V6-04-MAX-MIN-Evo).

---

## 4. Configuração analítica

### 4.1 Modo da base · Transacional × Pré-agregado (D-111)

V6 tem 2 modos canônicos de base, declarados pelo usuário na configuração com default declarado pelo motor:

| Modo | Descrição | T-AGRUPA |
|---|---|---|
| **Transacional** (default) | Múltiplas linhas podem cair na mesma célula Eixo1+Eixo2 | Consolida via regra de agregação correspondente à Medida (Contagem/Soma/Média) |
| **Pré-agregado** | Cada célula Eixo1+Eixo2 já vem como linha única com valor consolidado | No-op validado · verifica unicidade do par Eixo1+Eixo2 |

**Default declarado via heurística do motor_base:** se a média de linhas por par (Eixo1, Eixo2) na amostragem ≥ 1.5, motor propõe Transacional; caso contrário, Pré-agregado. Proposta visível na configuração antes da execução, editável em um clique. W-V6-MODO-INFERIDO (informativo) registra aceitação por default.

**Warnings:**
- W-V6-CHAVE-NAO-UNICA (estrutural): Pré-agregado declarado mas há duplicidade no par (Eixo1, Eixo2).

### 4.2 T-AGRUPA em V6 · 9ª consumidora com consumo padrão (D-111)

V6 entra como **9ª consumidora de T-AGRUPA** com consumo **padrão** (não adaptação V5-específica).

- Modo Transacional → T-AGRUPA aplica regra de agregação sobre Eixo1+Eixo2 conforme Medida escolhida (Contagem = count de linhas · Soma = sum do campo numérico · Média = avg do campo numérico)
- Modo Pré-agregado → T-AGRUPA em no-op validado (verifica unicidade · sem consolidação)

**Regras oficiais V6 MVP:** 3 das 5 regras canônicas de T-AGRUPA (Contagem · Soma · Média). Máximo e Mínimo ficam em roadmap P-V6-04-MAX-MIN-Evo.

**Padrão "consolidação obrigatória pré-cálculo com blindagem contra dupla agregação"** — 5ª aplicação consecutiva (V8 D-074 · V7 D-082 · V9 D-092 · V5 D-102 · **V6 D-111**). Candidato muito forte à formalização efetiva em CONTEXT §9 Camada C.

### 4.3 Multi-aba (ratificação §3.2)

Ver §3.2. V6 MVP aceita escolha explícita de uma aba por execução. Empilhamento multi-aba em roadmap P-V6-02-MULTIABA-Evo ligado a M2.STACK.

### 4.4 Tipos de medida V6 · separação tipo de campo × regra de agregação (D-112)

Prévio misturava dois planos conceituais distintos: tipo de campo (natureza semântica) e regra de agregação (operação aplicada). D-112 separa em aplicação do padrão D-025/D-036 (5ª aplicação cross-visão após V4/V7/V8/V9/V5).

**§4.4a · Tipos de campo aceitos como Medida em V6** (tabela D-025 adaptada):

| Tipo do campo | Aceito? | Comportamento |
|---|---|---|
| **Aditivo** (valor monetário, quantidade, volume) | ✅ Sim | Default Soma · execução sem warning |
| **Relativo** (percentual, taxa, índice) | ✅ Sim | Default Média · warning informativo W-V6-MEDIDA-RELATIVA · se usuário escolhe Soma, warning estrutural W-V6-SOMA-SOBRE-RELATIVA |
| **Não aditivo · estoque/contagem distinta** | ✅ Sim | Default Média · warning informativo W-V6-MEDIDA-NAO-ADITIVA |
| **Não aditivo · subtipo ID** (CPF · CNPJ · número de pedido) | 🚫 Bloqueio | B-V6-MEDIDA-ID com escape "este campo é numérico de fato" (W-V6-ID-FORCADO permanente) · heurística herdada de V5 D-103 |
| **Booleano** (flag binário) | ⚠ Condicional | Aceita apenas se Medida = Contagem · bloqueio B-V6-BOOLEANO-COM-SOMA-OU-MEDIA se regra ≠ Contagem |
| **Estado/situação** (categórico) | 🚫 Bloqueio | B-V6-ESTADO-COMO-MEDIDA · microcopy redirecional: *"Use este campo como Eixo · para contar ocorrências por combinação, use Medida = Contagem"* |

**§4.4b · Regras de agregação aceitas em V6 MVP** (3 das 5 canônicas):

| Regra | Campo Numérico? | Uso |
|---|---|---|
| **Contagem** | Dispensável | Frequência de linhas na combinação Eixo1+Eixo2 · default quando não há campo numérico selecionado |
| **Soma** | Obrigatório | Soma do campo numérico na combinação · default quando Medida é Aditiva |
| **Média** | Obrigatório | Média do campo numérico na combinação · default quando Medida é Relativa ou Não-aditiva (estoque/contagem) |

**§4.4c · Detecção de subtipo ID em Medida V6** · heurística herdada V5 D-103. Campo numérico inteiro com cardinalidade ≥ 90% das linhas e (sequência aritmética ≥ 80% OR comprimento fixo 8+ dígitos em 100%). Bloqueio B-V6-MEDIDA-ID com escape. Zero extensão nova para Fundação · motor_upload com detecção de subtipo ID já é requisito via D-103.

**§4.4d · Matriz Medida × Regra · defaults e regras permitidas:**

| Tipo do campo | Default de regra | Regras permitidas |
|---|---|---|
| (sem campo numérico) | Contagem | Contagem |
| Aditivo | Soma | Contagem · Soma · Média |
| Relativo | Média | Contagem · Média · (Soma com warning) |
| Não aditivo · estoque/contagem | Média | Contagem · Média |
| Não aditivo · ID | — (bloqueado) | — |
| Booleano | Contagem | Contagem apenas |
| Estado/situação | — (bloqueado como Medida) | — |

### 4.5 Elegibilidade categórica dos eixos (D-113)

**§4.5a · Classificação estrutural no motor_base** (requisito novo para G-FUND)

Motor_base adiciona campo `tipo_estrutural` em `column_meta` com 5 valores possíveis:

| Tipo estrutural | Critério | Elegível como Eixo V6? |
|---|---|---|
| `CATEGORICO_ELEGIVEL` | Texto, OU numérico com subtipo ID (D-103), OU numérico inteiro com cardinalidade ≤ 200, OU Booleano | ✅ Sim · default |
| `NUMERICO_CONTINUO` | Numérico não-inteiro, OU numérico inteiro com cardinalidade > 200 sem padrão ID | 🚫 Bloqueio · escape disponível |
| `TEMPORAL` | Data/timestamp detectados pelo reconhecedor de padrões pt-BR/pt-EN (D-026) | ⚠ Condicional · aceita com warning |
| `BOOLEANO` | 2 valores únicos (true/false · 0/1 · sim/não) | ✅ Sim (matriz 2×N útil) |
| `VAZIO` / `AMBIGUO` | >90% nulos ou tipo inconferível | 🚫 Bloqueio estrutural sem escape |

Heurística detalhada fica no motor_base (spec_fundacao.md a escrever no G-FUND); V6 consome a classificação.

**§4.5b · Comportamento V6 por tipo estrutural:**
- `CATEGORICO_ELEGIVEL` → aceita sem warning (caso canônico)
- `NUMERICO_CONTINUO` → B-V6-EIXO-NUMERICO-CONTINUO com escape "este campo é categórico de fato" (W-V6-EIXO-FORCADO-CATEGORICO permanente)
- `TEMPORAL` → aceita com W-V6-EIXO-TEMPORAL (informativo) · microcopy redirecional *"Para análise de evolução temporal, considere V3 ou V8"*
- `BOOLEANO` → aceita sem warning (caso legítimo)
- `VAZIO`/`AMBIGUO` → B-V6-EIXO-VAZIO-OU-AMBIGUO sem escape

**§4.5c · Escala de cardinalidade individual do eixo · 4 patamares:**

| Patamar | Cardinalidade | Comportamento |
|---|---|---|
| P1 · Normal | 2-30 | Execução sem warning |
| P2 · Alerta leve | 31-100 | W-V6-EIXO-CARDINALIDADE-P2 (estrutural leve) · microcopy "matriz ficará grande" |
| P3 · Alerta forte | 101-200 | W-V6-EIXO-CARDINALIDADE-P3 (estrutural) · confirmação do usuário |
| P4 · Bloqueio | > 200 | B-V6-EIXO-CARDINALIDADE-EXCESSO · escape "sei o que estou fazendo" (W-V6-EIXO-CARDINALIDADE-FORCADA permanente) |

Cardinalidade combinada (produto Eixo1 × Eixo2) em §8 (escala V6-específica).

**§4.5d · Eixos iguais:** B-V6-EIXOS-IGUAIS sem escape (invariante matemático).

---

## 5. Lógica de processamento

### 5.1 Ordem canônica de cálculo

A V6 processa na seguinte ordem (cada etapa depende da anterior):

1. **Upload** · motor_upload lê arquivo, identifica abas, inicia inferência de tipos
2. **Seleção de aba** · usuário escolhe aba (etapa dedicada · multi-aba)
3. **Leitura do MotorResult** · V6 recebe DataFrame + column_meta com tipo_estrutural
4. **Configuração** · usuário declara Eixos, Medida, Campo Numérico (se aplicável), Modo da base, thresholds, ordenação de exibição
5. **Validação estrutural** · checagem dos 13 bloqueios operacionais
6. **Pré-exclusão de nulos** · linhas com nulo em Eixo1 ou Eixo2 são excluídas (W-V6-EIXO-NULO-EXCLUIDO · informativo)
7. **Consolidação (T-AGRUPA)** · consolida Eixo1+Eixo2 conforme modo da base
8. **Cálculo do produto cartesiano observado** · V_Eixo1 × V_Eixo2 após consolidação
9. **Identificação de células presentes × ausentes** · complemento matemático (§8.4 diretriz 9)
10. **Cálculo do Valor da Medida por célula presente** · Contagem/Soma/Média conforme regra ativa
11. **Cálculo do Total da Matriz** · somatório sobre células presentes
12. **Cálculo da Participação Individual por célula presente**
13. **Ordenação de cálculo** · T-RANK V6-específica em 4 níveis (§5.4)
14. **Cálculo da Participação Acumulada** · progressiva sobre ranking
15. **Aplicação dos limiares e classificação de densidade** · Dominante/Relevante/Residual (§5.5)
16. **Cálculo do atributo derivado `faixa_de_participacao`** · por célula
17. **Cálculo das leituras qualitativas da matriz** · 5 leituras multi-aplicáveis (§5.7 Bloco 5)
18. **Renderização em tela** · matriz + painel lateral + configuração
19. **Exportação para Excel** · 7 abas conforme §5.10

### 5.2 Produto cartesiano observado (D-114)

Produto cartesiano observado = produto cartesiano entre os **conjuntos de valores que aparecem em cada eixo na base ativa** (não o produto teórico entre domínios completos declarados externamente).

Formalmente · se V_Eixo1 = {valores únicos observados em Eixo1 na base ativa} e V_Eixo2 = {valores únicos observados em Eixo2 na base ativa}:
- Produto cartesiano observado = V_Eixo1 × V_Eixo2
- Cardinalidade total de células = |V_Eixo1| × |V_Eixo2|

Nulos em Eixo1 ou Eixo2 não entram em V_Eixo1 nem V_Eixo2 · são pré-excluídos (§5.1 passo 6) com W-V6-EIXO-NULO-EXCLUIDO (informativo).

**Domínio declarado pelo usuário** (para detectar ausências de negócio, não apenas observadas) fica em roadmap P-V6-03-DOMINIO-DECLARADO-Evo.

### 5.3 Participação percentual e consolidação (D-114 + D-115)

- Denominador da Participação Individual = Total da Matriz (somatório do Valor da Medida sobre todas as células **presentes**)
- Participação de cada célula presente = Valor_celula / Total_da_Matriz × 100
- **Células ausentes · Participação = null** (nunca 0 · honra D-023 V2)

### 5.4 T-RANK V6 · 7ª consumidora com regra V6-específica em 4 níveis (D-115)

V6 entra como **7ª consumidora de T-RANK** com regra V6-específica em 4 níveis (aplicação D-073 · paridade estrutural com V7 D-088 e V9 D-096):

| Nível | Critério | Direção |
|---|---|---|
| 1 | Valor da Medida | Decrescente |
| 2 | Valor alfabético de Eixo 1 | Crescente (case-insensitive) |
| 3 | Valor alfabético de Eixo 2 | Crescente (case-insensitive) |
| 4 | Ordem de inserção da primeira ocorrência do par na base ativa | Crescente |

Tolerância de empate em valor: 1e-9 (herança T-RANK default).

**Participação Acumulada:** calculada progressivamente sobre o ranking resultante · aplicada apenas a células presentes · células ausentes · Participação Acumulada = null.

### 5.5 Taxonomia oficial V6 (D-116)

Estrutura paralela V5/V7/V9: 3 classes primárias de densidade + 2 classificações especiais paralelas + 1 atributo derivado por célula.

**Classes primárias de densidade (vocabulário dual técnico/exibição):**

| Técnico | Exibição | Critério |
|---|---|---|
| `DOMINANTE` | "No topo" / "Núcleo da matriz" | Célula presente · Participação Acumulada ≤ limiar Dominante (default 20%) |
| `RELEVANTE` | "Corpo" / "Intermediária" | Célula presente · nem Dominante nem Residual |
| `RESIDUAL` | "Periférica" / "Cauda" | Célula presente · Participação Individual < limiar Residual (default 2%) |

**Classificações especiais paralelas (estruturais · não-densidade):**

| Técnico | Exibição | Critério |
|---|---|---|
| `AUSENTE` | "Não observada" / "Sem ocorrência" | Célula no produto cartesiano observado sem ocorrência na base (aplicação canônica D-076) |
| `PRESENTE_SEM_VALOR` | "Presente sem valor" | Célula presente estruturalmente com Valor da Medida null (raro em Pré-agregado) |

**Atributo derivado por célula:** `faixa_de_participacao` · enum de 6 valores: TOPO (0-20%) · ALTO (20-40%) · MEDIO (40-60%) · BAIXO (60-80%) · CAUDA (80-100%) · SEM_FAIXA (ausentes ou presentes sem valor).

Não há "Distância do Limite" como atributo (como V5 tem) porque em V6 o limiar é cumulativo (Dominante por acumulado), não absoluto como média/outlier. `faixa_de_participacao` é análogo a Faixa Percentual V5 · honesto ao contexto V6. Aplicação D-073.

### 5.6 Tabela canônica das classes (formato espelho V5/V7/V9)

| Classe / Atributo | Código técnico | Microcopy de exibição | Critério |
|---|---|---|---|
| Classe primária de densidade | `DOMINANTE` | "No topo" / "Núcleo da matriz" | Célula presente · Acumulada ≤ 20% (default editável) |
| Classe primária de densidade | `RELEVANTE` | "Corpo" / "Intermediária" | Célula presente · nem Dominante nem Residual |
| Classe primária de densidade | `RESIDUAL` | "Periférica" / "Cauda" | Célula presente · Individual < 2% (default editável) |
| Especial paralela | `AUSENTE` | "Não observada" / "Sem ocorrência" | Célula no produto cartesiano observado sem ocorrência na base |
| Especial paralela | `PRESENTE_SEM_VALOR` | "Presente sem valor" | Célula presente · Valor da Medida null |
| Atributo derivado | `faixa_de_participacao` | "Faixa de Participação" | Enum 6 valores |

### 5.7 Resumo Executivo · 6 blocos fixos (D-117 · 7ª aplicação consecutiva do padrão D-044)

Padrão "Resumo Executivo em 6 blocos fixos" tem 7 aplicações consecutivas (V4 · V3 · V8 · V7 · V9 · V5 · **V6**) e é candidato muito forte à formalização em CONTEXT §13 como padrão estrutural de produto.

**Bloco 1 · Cabeçalho** · identificação da execução V6. Conteúdo: nome analítico dos Eixos · Tipo de Medida + nome analítico da Medida · Campo Numérico (quando aplicável) · Modo da base · Cardinalidade de cada eixo e da matriz · Limiares ativos · Ordenação de exibição ativa · Timestamp · total de linhas processadas · total de linhas com nulo excluídas.

**Bloco 2 · Números-âncora · 6 métricas-síntese da matriz:**

| # | Métrica | Definição |
|---|---|---|
| 1 | N de células possíveis | \|V_Eixo1\| × \|V_Eixo2\| |
| 2 | N de células presentes | Células com ocorrência na base |
| 3 | N de células ausentes | Células no produto cartesiano observado sem ocorrência |
| 4 | Densidade da matriz | N presentes / N possíveis · % |
| 5 | Concentração no topo | Participação cumulativa das N% primeiras células (N = limiar Dominante default 20%) |
| 6 | Total da Medida | Somatório dos Valores da Medida sobre células presentes |

V6 MVP não tem Modo Segmentado · portanto não há adaptação "camada agregada + camada por segmento" como V5 D-106.

**Bloco 3 · Distribuição** · como células se distribuem em classes:
- Distribuição por classe de densidade (% DOMINANTE · % RELEVANTE · % RESIDUAL sobre presentes)
- Distribuição estrutural (% PRESENTE · % AUSENTE · % PRESENTE_SEM_VALOR sobre total do produto cartesiano observado)
- Distribuição por Faixa de Participação

**Bloco 4 · Destaques da matriz** · adaptação D-073 da estrutura V4/V7/V9 em 2 sub-blocos:

- **Sub-bloco 4a · Top-N combinações presentes** · default N=10 editável (1-50) em Configurações avançadas. Posição · Eixo1=X · Eixo2=Y · Valor · Participação · Acumulada · Classe.
- **Sub-bloco 4b · Combinações ausentes destacadas** · todas as células ausentes · ordenadas por (Total do Eixo1 + Total do Eixo2) decrescente (heurística: ausências em eixos "grandes" aparecem primeiro · sinaliza lacunas analiticamente mais relevantes). Se > 50 ausências · paginação ou top-50 com redirecionamento para aba Combinações Ausentes. Se zero ausências · frase "Matriz densa · zero combinações ausentes".

**Bloco 5 · Leitura qualitativa com síntese** · 5 leituras multi-aplicáveis + Equilibrada default:

| Leitura | Critério (threshold default editável) |
|---|---|
| **Concentrada** | Concentração no topo ≥ 50% |
| **Dispersa** | Densidade ≥ 75% AND Concentração no topo ≤ 25% |
| **Esparsa** | Densidade ≤ 30% |
| **Assimétrica por Eixo** | Top-5 linhas concentram ≥ 80% OR top-5 colunas concentram ≥ 80% |
| **Com lacunas estruturais relevantes** | ≥ 20% de células ausentes em combinações de alto total |
| **Equilibrada** (default sem destaque) | Nenhuma outra leitura ativa |

Cada matriz pode receber múltiplas leituras simultâneas. Síntese narrativa: 1-2 frases interpretativas geradas das leituras ativas.

**Bloco 6 · Qualidade estrutural** · saúde do diagnóstico:
- Warnings ativados (contagem por gravidade)
- Thresholds não-default usados (lista)
- Ajustes feitos (linhas excluídas · consolidação T-AGRUPA: N linhas → M células)
- Alertas de cardinalidade (P2 · P3 · escape P4 se ativado)
- Alertas de escape ativado (subtipo ID · NUMERICO_CONTINUO como Eixo · cardinalidade forçada)

**Defaults declarados editáveis do Resumo Executivo** (6 thresholds):

| Parâmetro | Default | Opções |
|---|---|---|
| Top-N Bloco 4a | 10 | 1-50 |
| Threshold Concentrada | 50% | 30-80% |
| Threshold Dispersa | Densidade ≥ 75% + Concentração ≤ 25% | Editável |
| Threshold Esparsa | Densidade ≤ 30% | 10-50% |
| Threshold Assimétrica | 80% em top-5 | 60-95% |
| Threshold Com lacunas relevantes | 20% em alto total | 10-50% |

### 5.8 Matriz de Cruzamento · coração visual V6 (D-118)

V6 tem como **coração visual** a aba **"Matriz de Cruzamento"** (alinhamento com Mapa de Grupos V7 · Mapa de Perfil V9 · Matriz de Presença V8 · Mapa de Distribuição V5 · Curva Pareto V10 · Composição Principal V4 · 7ª aplicação consecutiva do padrão coração visual).

**Componentes da aba:**

1. **Tabela matricial principal**
   - Eixo 1 nas linhas · Eixo 2 nas colunas · Valor da Medida em cada célula
   - Células ausentes com marcador visual distinto ("—" ou fundo cinza-claro · honra D-023 V2 null ≠ 0)
   - Formatação condicional por classe de densidade: Dominante (verde-intenso) · Relevante (verde-médio) · Residual (cinza) · Ausente (fundo diferenciado) · PRESENTE_SEM_VALOR (amarelo claro)

2. **Totais marginais opcionais** (default ligado, editável): linha de totais por coluna + coluna de totais por linha + canto total geral

3. **Gráfico nativo Excel** · **ColumnChart empilhado 100%** via openpyxl (heatmap real não suportado nativamente · ColumnChart é alternativa análoga a Mapa de Perfil V9)
   - 1 série por valor de Eixo 2
   - 1 categoria por valor de Eixo 1
   - Altura da barra = total por Eixo 1 · empilhamento = composição por Eixo 2
   - Permite leitura visual de concentração e assimetria por Eixo

4. **Paginação** · matriz > 30×30 paginada em blocos de 20×20 com notas de navegação

**Heatmap real** (quando openpyxl oferecer suporte) fica em roadmap P-V6-06-HEATMAP-NATIVO-Evo.

**Requisito novo para Fundação (G-FUND):** `exportacao.py` ganha capability de formatação condicional de matriz + ColumnChart empilhado 100% + paginação de matriz grande (extensão do requisito V8 de streaming para matrizes pesadas).

### 5.9 Ordenação de exibição da matriz (D-115 parte 2)

Default declarado editável em Configurações avançadas · 9ª aplicação consecutiva do padrão "default declarado editável":

| Opção | Ordem de Eixo 1 | Ordem de Eixo 2 |
|---|---|---|
| **Alfabética** (default) | Crescente (case-insensitive) | Crescente (case-insensitive) |
| **Por total do eixo** | Decrescente pela soma da linha | Decrescente pela soma da coluna |
| **Manual pelo usuário** | Drag-and-drop | Drag-and-drop |

Para `TEMPORAL` detectado (T-06) · ordem default muda para **cronológica crescente** (herança do reconhecedor pt-BR/pt-EN de D-026) · W-V6-EIXO-ORDEM-CRONOLOGICA (informativo).

Reordenação manual sobre eixo temporal/ordinal dispara W-V6-EIXO-ORDEM-MANUAL (informativo · espelho V8).

### 5.10 Estrutura Excel oficial V6 (D-119)

7 abas fixas · regra D-017 honrada (Diagnóstico sempre última aba):

| # | Aba | Conteúdo |
|---|---|---|
| 1 | **Resumo Executivo** | 6 blocos fixos (§5.7) |
| 2 | **Matriz de Cruzamento** · coração visual | Tabela matricial formatada + ColumnChart (§5.8) |
| 3 | **Ranking de Combinações** | Todas as células presentes ordenadas · Eixo1 · Eixo2 · Valor · Participação · Acumulada · Ranking · Classe · Faixa |
| 4 | **Combinações Ausentes** | Todas as células ausentes · Eixo1 · Eixo2 · Total do Eixo1 · Total do Eixo2 · flag "Alto total" · aplicação D-076 cristalizada em aba própria |
| 5 | **Base Analítica** | 1 linha por célula (presente OU ausente) · colunas: Eixo1, Eixo2, Valor da Medida (null se ausente), classificação estrutural, classificação de densidade, Participação, Acumulada, Ranking, faixa_de_participacao, linha original |
| 6 | **Parâmetros** | Configurações ativas: Eixos · Medida · Modo da base · limiares · ordenação de exibição · thresholds editados · granularidade declarada |
| 7 | **Diagnóstico** (sempre última · D-017) | Warnings ativados · ajustes · contagens estruturais · escapes ativados |

V6 MVP sem Modo Segmentado · roadmap P-V6-05-SEGMENTADO-Evo permitirá aba "Resumo por Segmento" condicional (análogo V5 D-108).

### 5.11 "Dados Brutos do prévio descartada" (D-119 · 5ª aplicação consecutiva)

V6 não tem aba "Dados Brutos Processados" (§10 do prévio) · linhas originais aparecem na **Base Analítica** (aba 5 · com colunas de classificação) · contagens estruturais aparecem no **Diagnóstico** (aba 7). Rastreabilidade plena sem aba duplicada.

**5ª aplicação consecutiva do padrão "Dados Brutos descartada em favor de Base Analítica + Diagnóstico"** (V8 D-078 · V7 D-089 · V9 D-099 · V5 D-108 · **V6 D-119**) · candidato muito forte à formalização efetiva no próximo ajuste do CONTEXT §9 Camada C.

**Combinações Ausentes como aba dedicada** é distintiva V6 · aplicação D-076 cristalizada em aba própria · análoga à aba "Movimentações" específica V8.

---

## 6. Contrato V6Result (síntese)

A implementação retornará `V6Result` com os seguintes campos:

**Campos estruturais:**
- `eixos: dict` · nome analítico e técnico de Eixo 1 e Eixo 2
- `medida: dict` · tipo · regra de agregação · campo numérico (se aplicável) · nome analítico
- `modo_base: enum` · `TRANSACIONAL | PRE_AGREGADO`
- `limiares: dict` · `dominante` (0-100) · `residual` (0-100) · `faixas_participacao` (lista de cortes)

**Métricas da matriz:**
- `n_celulas_possiveis: int`
- `n_celulas_presentes: int`
- `n_celulas_ausentes: int`
- `densidade: float` (%)
- `concentracao_topo: float` (%)
- `total_matriz: float`
- `leituras_matriz: list` · enum · zero a cinco leituras ativas
- `sintese_narrativa: str`

**Dados por célula (DataFrame):**
- Colunas: `eixo1 · eixo2 · valor_medida · participacao · participacao_acumulada · ranking · classificacao_estrutural · classificacao_densidade · faixa_de_participacao · linha_original`
- Granularidade: 1 linha por célula do produto cartesiano observado (presentes + ausentes)

**Totais marginais (opcional):**
- `totais_por_eixo1: dict` {valor_eixo1: total}
- `totais_por_eixo2: dict` {valor_eixo2: total}

**Diagnóstico:**
- `warnings: list` · cada warning com código · gravidade · contexto · contagem
- `ajustes: list` · AJUSTE_LEVE e DECISAO_USUARIO (padrão T-DIAG D-021)
- `escapes_ativados: list` · subtipo ID · NUMERICO_CONTINUO como Eixo · cardinalidade forçada · etc
- `parametros_ativos: dict` · completo · incluindo thresholds editados

---

## 7. Bloqueios operacionais (13 estruturais · D-120)

| Código | Situação | Escape |
|---|---|---|
| `B-V6-EIXO-NUMERICO-CONTINUO` | Eixo declarado sobre campo NUMERICO_CONTINUO | ✅ "este campo é categórico de fato" |
| `B-V6-EIXO-VAZIO-OU-AMBIGUO` | Eixo sobre coluna >90% nulos ou tipo inconferível | 🚫 |
| `B-V6-EIXO-CARDINALIDADE-EXCESSO` | Cardinalidade individual > 200 | ✅ "sei o que estou fazendo" |
| `B-V6-EIXOS-IGUAIS` | Eixo1 = Eixo2 | 🚫 invariante matemático |
| `B-V6-MEDIDA-ID` | Campo com subtipo ID como Medida (Soma/Média) | ✅ "este campo é numérico de fato" |
| `B-V6-BOOLEANO-COM-SOMA-OU-MEDIA` | Booleano com regra ≠ Contagem | 🚫 |
| `B-V6-ESTADO-COMO-MEDIDA` | Campo categórico como Medida | 🚫 redirecionar para Eixo |
| `B-V6-POR-LINHAS` | Base em formato POR_LINHAS | 🚫 fora MVP |
| `B-V6-MATRIZ-CARDINALIDADE-EXTREMA` | Produto N×M > 10.000 | ✅ "sei o que estou fazendo" |
| `B-V6-MATRIZ-VAZIA` | Todas as células ausentes após filtro | 🚫 |
| `B-V6-MEDIDA-NUMERICA-AUSENTE` | Medida = Soma/Média sem campo numérico válido | 🚫 redirecionar para Contagem |
| `B-V6-MOTOR-INFERIU-TIPO-INCOMPATIVEL` | Tipo inferido incompatível com escolha · sem escape ativo | 🚫 forçar revisão |
| `B-V6-MINIMO-OPERACIONAL` | Base com < 5 registros válidos | 🚫 |

---

## 8. Escala de cardinalidade V6 · 3 eixos com produto da matriz como eixo V6-específico (D-120)

Natureza V6 é **bivariada simultânea** · aplicação D-073 ao método de escala de cardinalidade (diferente de V5 multi-eixo independente ortogonal).

### 8.1 Eixo 1 · Cardinalidade de Eixo 1 (4 patamares)

Ver §4.5c. Patamares P1 (2-30) · P2 (31-100) · P3 (101-200) · P4 (>200 · escapável).

### 8.2 Eixo 2 · Cardinalidade de Eixo 2

Patamares idênticos a Eixo 1 · independentes.

### 8.3 Eixo 3 · Cardinalidade da Matriz (produto N × M · eixo V6-específico)

| Patamar | N × M | Comportamento |
|---|---|---|
| P1 · Normal | ≤ 900 (ex: 30×30) | Execução sem warning |
| P2 · Alerta leve | 901-2.500 (ex: 50×50) | W-V6-MATRIZ-P2 · paginação ativada automaticamente no coração visual |
| P3 · Alerta forte | 2.501-10.000 (ex: 100×100) | W-V6-MATRIZ-P3 · confirmação do usuário · streaming ativado no Excel |
| P4 · Bloqueio | > 10.000 | B-V6-MATRIZ-CARDINALIDADE-EXTREMA · escapável · W-V6-MATRIZ-FORCADA permanente |

### 8.4 Diretrizes de performance (9 · 7 herdadas + 2 V6-específicas)

Herdadas de V3/V7/V8/V9/V5:
1. Consolidação T-AGRUPA em passe único
2. Inferência de tipo de campo em amostragem (não base completa)
3. Cálculo de métricas do Bloco 2 integrado ao passe de classificação
4. Ordenação determinística O(N log N) reutilizada para ranking
5. Paginação de abas pesadas acima de limiar de cardinalidade
6. Streaming de exportação Excel via openpyxl write-only mode em abas > 100.000 linhas
7. Detecção de subtipo ID executada uma vez no upload

Específicas V6:
8. **Cálculo do produto cartesiano observado em passe único** após consolidação T-AGRUPA · evita segundo scan da base
9. **Detecção de células ausentes via complemento matemático** (|V_Eixo1| × |V_Eixo2|) − células presentes · O(1) em vez de O(N×M) enumerativo

---

## 9. Roadmap pós-MVP · 11 candidatos P-V6-XX-Evo

| Código | Item | Origem |
|---|---|---|
| `P-V6-01-POR-LINHAS-Evo` | Aceitar estrutura POR_LINHAS via T-PIVOT 4ª semântica | T-07 |
| `P-V6-02-MULTIABA-Evo` | Empilhamento multi-aba via M2.STACK (3º consumidor futuro) | T-04/T-07 |
| `P-V6-03-DOMINIO-DECLARADO-Evo` | Usuário declara domínio completo de cada eixo para detectar ausências de negócio | T-08 |
| `P-V6-04-MAX-MIN-Evo` | Regras Máximo e Mínimo aceitas em V6 | T-05 |
| `P-V6-05-SEGMENTADO-Evo` | Modo Segmentado por Agrupador adicional (1 matriz por segmento) | T-13 |
| `P-V6-06-HEATMAP-NATIVO-Evo` | Heatmap real quando suporte openpyxl disponível | T-12 |
| `P-V6-07-EVOLUCAO-ENTRE-EXECUCOES-Evo` | Leitura comparativa entre duas execuções V6 | Prévio §16 |
| `P-V6-08-PESOS-POR-EIXO-Evo` | Importância declarada por valor do eixo para leituras qualitativas | Prévio §16 |
| `P-V6-09-VISAO-GRAFICA-COMPLEMENTAR-Evo` | Gráfico secundário (sankey · bubble · treemap) | Prévio §16 |
| `P-V6-10-CARDINALIDADE-EXTREMA-Evo` | Tratamento otimizado de matriz > 10.000 células | Prévio §16 |
| `P-V6-11-LIMIARES-POR-PERCENTIL-Evo` | Limiares Dominante/Residual por percentil da distribuição | Prévio §16 |

### 9.1 Anti-roadmap V6 · 4 itens explicitamente fora de escopo permanente

| Item | Por que nunca |
|---|---|
| Sugestão de "combinações que deveriam existir" | V6 não prescreve expectativa de negócio (§8.2 · anti-glossário T-03) |
| Detecção automática de "erro de cadastro" em ausências | V6 não diagnostica causa raiz · ausência é fato matemático |
| Imputação/preenchimento automático de células ausentes | Célula ausente é conteúdo primário (D-076) · preencher elimina o objeto de análise |
| Juízo de valor automático sobre combinações (boa/ruim) | V6 não atribui qualidade · classificação é descritiva |

---

## 10. Warnings catalogados V6 · 43 total (13 bloqueios + 30 warnings)

**Bloqueios estruturais (13)** · ver §7.

**Warnings estruturais (8):** W-V6-CHAVE-NAO-UNICA · W-V6-SOMA-SOBRE-RELATIVA · W-V6-EIXO-CARDINALIDADE-P2 · W-V6-EIXO-CARDINALIDADE-P3 · W-V6-CELULA-PRESENTE-SEM-VALOR · W-V6-MATRIZ-P2 · W-V6-MATRIZ-P3 · W-V6-FAIXAS-EDITADAS.

**Warnings permanentes (5):** W-V6-EIXO-FORCADO-CATEGORICO · W-V6-EIXO-CARDINALIDADE-FORCADA · W-V6-ID-FORCADO · W-V6-MATRIZ-FORCADA · W-V6-EIXO-ORDEM-MANUAL.

**Warnings informativos (17):** W-V6-MODO-INFERIDO · W-V6-MEDIDA-RELATIVA · W-V6-MEDIDA-NAO-ADITIVA · W-V6-MEDIDA-TIPO-DECL · W-V6-MEDIDA-REGRA-DECL · W-V6-EIXO-TEMPORAL · W-V6-MULTIABA-ESCOLHA · W-V6-ESTRUTURA-INFERIDA · W-V6-EIXO-NULO-EXCLUIDO · W-V6-EIXO-ORDEM-CRONOLOGICA · W-V6-RANKING-EMPATE-GERAL · W-V6-FRONTEIRA-CLASSIFICACAO · W-V6-LIMIAR-DOMINANTE-EDITADO · W-V6-LIMIAR-RESIDUAL-EDITADO · W-V6-THRESHOLD-LEITURA-EDITADO · W-V6-TOPN-EDITADO · W-V6-VALOR-NAO-NUMERICO.

V6 tem maior volume de warnings do projeto (43) · coerente com natureza bivariada com múltiplos casos-limite estruturais.

---

## 11. Posicionamento C.5

V6 honra C.5 em múltiplas dimensões:

- **Sistema não decide a granularidade pelo usuário** · modo da base declarado com default visível (D-111)
- **Sistema não decide tipo de campo** · inferência com default visível e escape (D-112/D-113)
- **Sistema não decide elegibilidade categórica** · classificação do motor_base visível e editável (D-113)
- **Sistema não decide limiares de classificação** · 3 thresholds default declarado editáveis (D-116)
- **Sistema não decide leituras qualitativas** · 5 leituras com thresholds editáveis (D-117)
- **Sistema não decide ordenação de exibição** · 3 opções · default declarado (D-115)
- **Sistema não prescreve ausências** · ausência é conteúdo, não erro (D-076 · anti-glossário T-03 · anti-roadmap §9.1)
- **Sistema não atribui juízo** · microcopy neutra (T-03 · vocabulário dual)

~12 dimensões de default declarado aplicadas em V6 · reforço sistemático do padrão D-024.

---

## 12. Relação com Fundação

### 12.1 Transversais consumidos

- **T-AGRUPA** · V6 é 9ª consumidora com consumo padrão (não adaptação V5-específica · D-111)
- **T-RANK** · V6 é 7ª consumidora com regra V6-específica 4 níveis (D-115)
- **T-DIAG** · consumo padrão (categorias AJUSTE_LEVE · DECISAO_USUARIO · D-021)
- **T-MODELO** · consumo padrão (T-MODELO §13.3 · CONTEXT)

### 12.2 Transversais não aplicáveis

- **T-SEMA** · V6 não tem semântica de valor direcional aplicável a cruzamento bivariado categórico
- **T-EIXO** · V6 não consome eixo ordenado (distinção com V3/V8)
- **T-ACUM** · não aplicável (acumulado em V6 é cálculo direto sobre ranking, não transversal)
- **T-ABC** · não aplicável (V6 usa taxonomia própria Dominante/Relevante/Residual com limiares próprios)
- **T-PIVOT** · não consumido no MVP (POR_LINHAS em roadmap)
- **T-DUAL** · não aplicável (V6 é intra-base)
- **T-FUZZY** · não aplicável
- **T-CONCAT** · não aplicável

### 12.3 Requisitos novos para a Fundação (G-FUND)

1. **motor_base com metadado `column_meta.tipo_estrutural`** (5 valores enum · D-113) · requisito útil para V6 e para M2 e visões futuras.
2. **exportacao.py com formatação condicional de matriz** + **ColumnChart empilhado 100%** + **paginação de matriz grande** (D-118) · extensão dos requisitos V8 (streaming de matriz).
3. **exportacao.py com "Combinações Ausentes" como aba dedicada** em template V6 (D-119) · análoga à aba "Movimentações" específica V8.

Nenhum é requisito disruptivo · são extensões incrementais coerentes com requisitos V5 (motor_upload subtipo ID) e V8 (streaming para matriz · paginação).

### 12.4 Aplicações e validações de padrões consolidados

V6 aplica e valida os seguintes padrões do método TabloFlow:

- **Padrão "consolidação obrigatória pré-cálculo"** · 5ª aplicação consecutiva (V8 · V7 · V9 · V5 · V6) → candidato muito forte a formalização
- **Padrão "thresholds multi-camada editáveis"** · 6ª aplicação consecutiva (V4 · V7 · V8 · V9 · V5 · V6) → candidato muito forte a formalização
- **Padrão "Dados Brutos descartada"** · 5ª aplicação consecutiva (V8 · V7 · V9 · V5 · V6) → candidato muito forte a formalização
- **Padrão "Resumo Executivo em 6 blocos fixos"** (D-044) · 7ª aplicação consecutiva (V4 · V3 · V8 · V7 · V9 · V5 · V6) → candidato muito forte a formalização em CONTEXT §13
- **Padrão "coração visual da visão"** · 7ª aplicação consecutiva (V4 · V7 · V8 · V9 · V5 · V10 · V6) → candidato muito forte a formalização em CONTEXT §13
- **Padrão "matriz de bloqueios numerados"** · 5ª aplicação consecutiva (V7 · V8 · V9 · V5 · V6)
- **Padrão "escala de cardinalidade em eixos com patamares numerados"** · 5 aplicações com variações adaptativas (hierárquica V7 · multiplicativa V8 · multi-eixo independente V9/V5 · bivariada simultânea V6)
- **Padrão "herança adaptada à natureza analítica"** (D-073) · ~15 aplicações documentadas · padrão meta-adaptativo cristalizado

---

## 13. Nomenclatura oficial V6

### 13.1 Termos canônicos (~24 termos em 5 categorias)

**Categoria A · Identificação e configuração (6):**
- **Eixo 1** · dimensão categórica nas linhas da matriz
- **Eixo 2** · dimensão categórica nas colunas da matriz
- **Campo Principal** · sinônimo de Eixo quando precisa destacar o papel
- **Medida** · tipo de operação sobre a célula (Contagem · Soma · Média)
- **Tipo de Medida** · classificação semântica do campo (Aditivo · Relativo · Não aditivo · Booleano · Estado)
- **Critério de Classificação** · regra ativa de densidade (limiares Dominante · Residual)

**Categoria B · Estrutura analítica (7):**
- **Combinação** · par de valores (Eixo1=X, Eixo2=Y) · conceito genérico
- **Célula** · slot da matriz no cruzamento (linha Eixo1=X · coluna Eixo2=Y) · unidade analítica posicional
- **Produto Cartesiano Observado** · V_Eixo1 × V_Eixo2 · conjunto de pares possíveis dentro dos valores observados
- **Combinação Presente** · par com ≥ 1 ocorrência na base
- **Combinação Ausente** · par sem ocorrência na base
- **Matriz** · estrutura visual e analítica completa (células presentes + ausentes)
- **Total da Matriz** · somatório do Valor da Medida sobre células presentes

**Categoria C · Métricas por combinação (5):**
- **Valor da Medida** · resultado da operação na célula
- **Participação** · % da célula sobre Total da Matriz
- **Participação Acumulada** · cumulativa no ranking
- **Ranking** · posição na ordenação decrescente por valor
- **Densidade** · métrica de conjunto · % de células presentes sobre produto cartesiano observado

**Categoria D · Classificação (4):**
- **Dominante** · célula presente no topo da Participação Acumulada
- **Relevante** · célula presente nem Dominante nem Residual
- **Residual** · célula presente com Participação Individual abaixo do limiar
- **Ausente** · célula no produto cartesiano observado sem ocorrência

**Categoria E · Saída (2):**
- **Base Analítica** · 1 linha por célula (presente ou ausente) com todas as colunas de classificação
- **Diagnóstico** · aba de saúde estrutural (warnings · ajustes · contagens · escapes)

### 13.2 Vocabulário dual técnico/exibição (6 pares)

| Técnico (motor · contrato · Base Analítica) | Exibição (microcopy · tela · Resumo Executivo) |
|---|---|
| `EIXO_1` / `EIXO_2` | Nome analítico configurado pelo usuário |
| `COMBINACAO` | "Combinação" ou "Cruzamento" (em prosa) |
| `CELULA` | "Célula" (visual) ou "Combinação" (prosa) |
| `DOMINANTE` | "No topo" / "Núcleo da matriz" (nunca "boa") |
| `RESIDUAL` | "Periférica" / "Cauda" (nunca "ruim") |
| `AUSENTE` | "Não observada" / "Sem ocorrência" (nunca "faltante") |

### 13.3 Anti-glossário V6 · 6 termos a evitar

| Termo | Por que evitar | Usar no lugar |
|---|---|---|
| *Faltante* | Sugere obrigatoriedade de existência · prescritivo | *Ausente* · *Não observada* |
| *Deveria existir* | V6 não declara expectativa de negócio | (conceito recusado) |
| *Erro de cruzamento* · *Combinação inválida* | V6 não diagnostica causa | *Combinação ausente* · *Célula vazia* |
| *Dominante = boa* · *Residual = ruim* | V6 não atribui qualidade | Usar código técnico em motor · microcopy neutra em tela |
| *Preenchimento esparso* | Linguagem de banco, não de análise | *Matriz pouco densa* · *Densidade baixa* |
| *Filtrar combinações ausentes* | Ausência é conteúdo primário (D-076) | *Exibir apenas combinações presentes* (com microcopy explícita) |

---

## 14. Decisões geradas · D-111 a D-121

| # | Tema | D-XXX |
|---|---|---|
| T-01 | §2.3 simétrico a V5 · convivência Família E sem retroação formal | sem D-XXX |
| T-02 | Fronteiras V6×V4/V10/V8/V7/V9 em prosa declarativa | sem D-XXX |
| T-03 | Vocabulário canônico V6 em 5 categorias + dual 6 pares + anti-glossário 6 termos | sem D-XXX |
| T-04 | Modo da base V6 + T-AGRUPA 9ª consumidora + multi-aba em roadmap | **D-111** |
| T-05 | Tipos de medida V6 · separação tipo de campo × regra de agregação | **D-112** |
| T-06 | Classificação categórico-elegível no motor_base + cardinalidade individual 4 patamares | **D-113** |
| T-07 | POR_COLUNAS no MVP · POR_LINHAS em roadmap · multi-aba com M2.STACK | sem D-XXX |
| T-08 | Unidade analítica = célula + produto cartesiano observado + classificação estrutural | **D-114** |
| T-09 | T-RANK V6 7ª consumidora 4 níveis + separação cálculo × exibição + Participação null em ausentes | **D-115** |
| T-10 | Taxonomia oficial V6 · 3 primárias + 2 especiais + atributo derivado + 3 thresholds | **D-116** |
| T-11 | Resumo Executivo 6 blocos · 7ª aplicação D-044 | **D-117** |
| T-12 | Matriz de Cruzamento como coração visual · 7ª aplicação do padrão | **D-118** |
| T-13 | Excel 7 abas + Combinações Ausentes dedicada + Dados Brutos descartada (5ª aplicação) | **D-119** |
| T-14 | 13 bloqueios + escala 3 eixos bivariada + 9 diretrizes performance | **D-120** |
| T-15 | Roadmap 11 candidatos + anti-roadmap 4 itens | sem D-XXX |
| T-16 | Consolidação warnings + sumário do refino | **D-121** |

---

## 15. Pendências do refino (histórico)

Todas as 16 pendências T-01 a T-16 foram fechadas em sessão única (20/04/2026) · padrão D-019 + D-034 + D-033 aplicado integralmente · sinalização de densidade no 3º status-check aprovada pela Usuária como "continuar em sessão única".

---

## 16. Referências

- **CONTEXT.md** · §3 Fase 0 · §4 Família E · §6 transversais · §9 Camada C · §13 padrões estruturais de produto
- **DECISIONS.md** · D-111 a D-121 (esta sessão) · D-110 (Família E adaptada · V5) · D-076 (warning vs conteúdo) · D-073 (herança adaptada) · D-044 (Resumo Executivo 6 blocos) · D-041 (T-RANK desempate) · D-025/D-036 (tipos de campo) · D-024 (default declarado) · D-023 (null não é zero) · D-017 (Diagnóstico última aba) · D-008 (inferência semântica) · D-103 (subtipo ID)
- **GLOSSARIO.md** · seção 5.V6 · §1 Família E · §4 T-AGRUPA · §4 T-RANK · §6 Warnings V6 · §11 anti-glossário
- **DCVs aprovados** anexados como precedente · dcv_v5.md · dcv_v8.md · dcv_v4.md
