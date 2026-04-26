# DCV-V5 · Comportamento e Dispersão

**Família:** E · Estrutura interna do recorte (1ª visão da família · D-110)
**Status:** Aprovado
**Sessão de aprovação:** 19/04/2026 · sessão única · 15 pendências fechadas
**Decisões geradas:** D-102 a D-110

---

## 1. Propósito da visão

V5 responde uma pergunta única e bem delimitada: *"como os valores de um campo numérico se distribuem dentro de um conjunto de observações?"*. Ela analisa **forma**, não movimento, não composição, não posição relativa. O que V5 entrega é a leitura estatística da forma dos dados — onde está o centro da distribuição, qual é o grau de dispersão, qual é a simetria, e quais valores são atípicos segundo critério estatístico configurável.

V5 não responde perguntas de outras visões: o que mudou entre dois estados pertence à V2; como algo evoluiu ao longo de uma sequência pertence à V3; quanto cada elemento representa dentro de um total pertence à V4; quem está acima ou abaixo da média do seu grupo pertence à V7; quem se destaca quando consideradas múltiplas métricas simultâneas pertence à V9. V5 fica com o terreno tradicional da estatística descritiva univariada — o que pacotes estatísticos e a função "Descriptive Statistics" do Excel cobrem, mas com a estrutura do TabloFlow: configuração progressiva, default declarado, diagnóstico transparente, exportação Excel auditável.

A V5 mostra o resultado. O usuário investiga a causa. Outlier estatístico não é erro de origem, não é anomalia automática, não é fato de negócio — é fato matemático sobre a distribuição observada. A interpretação fica para o usuário.

---

## 2. Posicionamento analítico

### 2.1 O cenário real que a V5 atende

Análise solo de um campo numérico para entender seu comportamento estatístico: faturamento por transação, prazo de pagamento por nota fiscal, quantidade vendida por pedido, custo unitário por componente, tempo de processamento por chamado, valor de compra por fornecedor. Casos onde o usuário precisa entender:

- Onde está a massa dos valores (média · mediana · moda)
- Quão dispersos os valores estão (DP · variância · IQR · CV · amplitude)
- Se a distribuição é simétrica ou assimétrica (skewness)
- Quais registros fogem do padrão esperado (outliers)
- Como esses comportamentos diferem entre segmentos (Modo Segmentado por Agrupador)

V5 é primeira visão da **Família E · Estrutura interna do recorte** (reformulada nesta sessão · D-110), única família ainda totalmente em aberto na Fase 0. V6 (matriz de cruzamento entre dois campos categóricos) é a outra visão da família e será refinada após V5. V5 e V6 são **operacionalmente distantes** — não compartilham transversais centrais, não navegam fronteira em interface operacional, e a relação entre as duas é tratada de forma enxuta nesta família (§2.3).

### 2.2 Fronteiras com visões vizinhas

**V5 × V7 (Família E × Família D · Posição relativa).** A palavra "desvio" aparece nas duas visões com sentidos diferentes. Em V5, "desvio" é propriedade estatística derivada do próprio campo — desvio padrão é o cálculo de dispersão em torno do centro. Em V7, "desvio" é distância de cada elemento à média do grupo declarado. Quem mede dispersão como característica intrínseca do campo usa V5; quem classifica elementos pela distância à média do grupo usa V7. Aplicação direta do padrão "warning em uma visão pode ser conteúdo em outra" (D-076 · DCV-V8): mesmo campo numérico é substrato estatístico em V5 e input de classificação por tolerância em V7. Esta fronteira já está formalizada simetricamente em DCV-V7 §2.2.

**V5 × V9 (Família E × Família D · Posição relativa).** V5 opera sobre **um campo por execução**, olhando para como os valores se distribuem dentro dele. V9 opera sobre **múltiplas métricas simultâneas**, mas não extrai propriedade estatística de nenhuma delas — cada métrica é apenas critério de ordenação. Em V5, outliers são **conteúdo analítico primário** (o destaque é o registro outlier · sua identificação é o resultado). Em V9, valores extremos são **input de ordenação** que empurram o ranking sem virar atributo da saída — V9 não classifica nada como "outlier", apenas usa o valor extremo na composição do score consolidado. Aplicação simétrica de D-076. Esta fronteira já está formalizada em DCV-V9 §2.2.

**V5 × V4 (Família E × Família C · Composição).** Ambas as visões podem ser invocadas por quem pensa "concentração", mas operam sobre objetos diferentes. V4 mostra **concentração da participação no total** — quanto cada elemento representa do total geral, com Curva ABC e Curva Pareto destacando os elementos que compõem maior fatia do total. V5 mostra **concentração estatística do campo** — se os valores observados se agrupam fortemente em torno do centro (CV baixo · alta concentração estatística) ou se espalham (CV alto · alta dispersão estatística). Quem responde *"esse fornecedor é grande no meu total de compras?"* usa V4 (peso no total). Quem responde *"os valores das compras desse fornecedor variam muito entre transações?"* usa V5 (dispersão estatística do campo "Valor da Compra"). Esta é a primeira formalização desse lado da fronteira (V4 não menciona V5 explicitamente).

Nenhuma dessas fronteiras é navegada em interface operacional. Microcopy declarativa autossuficiente em cada bloco · sem botão "ir para V7" · sem sugestão "experimente também V4". Quem precisa entender as diferenças lê este DCV.

### 2.3 Relação com V6 (par autônomo da Família E)

V5 e V6 convivem como visões da Família E · Estrutura interna do recorte. As duas operam sobre recortes distintos da base — V5 univariado numérico (um campo numérico por execução), V6 bivariado categórico (cruzamento de dois campos categóricos por execução). Não compartilham transversais centrais nem apresentam fronteira navegada operacionalmente. O que une V5 e V6 na mesma família é o nível mais abstrato: ambas **expõem propriedades estruturais internas** de um recorte da base sem comparar com referência externa, sem benchmark interno por grupo, sem eixo ordenado, sem total geral. DCV-V6 declarará seu posicionamento simétrico nesta família quando refinado.

A diferença substantiva entre Família E e as Famílias B (V3/V8 · par operacional próximo via T-EIXO) e D (V7/V9 · par operacional próximo via T-AGRUPA + T-SEMA + T-RANK) justifica esta adaptação no método de posicionamento de família: famílias com par operacionalmente próximo merecem tabela de retroação diferida com células *(a confirmar)*; Família E com par operacionalmente distante merece declaração enxuta de convivência. Aplicação do padrão "herança adaptada à natureza analítica" (D-073) ao próprio método de posicionamento de família — não há retroação diferida formal V5→V6 análoga a D-060 (V3→V8) ou D-081 (V7→V9). O gancho metodológico fica preservado pela nota acima.

### 2.4 Unidade analítica da V5

Unidade analítica da V5 é **a observação individual no campo numérico principal** — cada linha da base que tem valor válido (não-nulo · numérico) no campo principal é uma observação no conjunto sob análise.

Esta posição é distintiva de V5 em relação a V4/V7/V9, onde a unidade analítica é uma **chave consolidada** (Elemento+Grupo em V7 · Identificador em V9 · Elemento por Medida em V4). V5 não consolida valores: 100 vendas de R$ 50 e 1 venda de R$ 5.000 entram no cálculo como **101 observações** (100 valores em R$ 50 e 1 em R$ 5.000), nunca como 1 valor consolidado de R$ 10.000 ou 51 linhas com agregação.

A consequência operacional: T-AGRUPA em V5 nunca consolida valores. Em V5, T-AGRUPA tem semântica V5-específica (§4.1) — modo no-op puro (granularidade individual · default), modo de validação de chave (granularidade declarada como consolidada), e modo de particionamento por Agrupador (Modo Segmentado · particiona observações por valor único do Agrupador sem consolidar dentro do segmento).

---

## 3. O que a visão recebe

### 3.1 Estrutura de entrada

Uma base lógica por execução. Pode ter uma única aba ou múltiplas abas com escolha de aba pelo usuário. Pode ter campo principal já existente ou campo principal calculado a partir de outras colunas (via M2.CALC futuro · MVP exige campo já existente). Pode ter Modo Global (sem segmentação) ou Modo Segmentado (com Agrupador único · §4.4).

### 3.2 Campos obrigatórios

**Campo Principal** · campo numérico sobre o qual a análise estatística é realizada. Único campo obrigatório (Modo Global). Em Modo Segmentado, **Agrupador** também é obrigatório (§4.4).

### 3.3 Tipos de medida aceitos em V5 (D-103)

Aplicação do padrão "herança adaptada à natureza analítica" (D-073) à tabela canônica de tipos de campo (D-025 sistematizado em V4 D-036). Espelha V7 D-083 ao excluir Booleano:

| Tipo | Aceito em V5? | Tratamento |
|---|---|---|
| **Aditivo** (faturamento · quantidade · horas) | ✅ Sim | Cálculo padrão sem warning específico |
| **Relativo** (margem % · taxa · preço médio · CV) | ✅ Sim | Cálculo padrão + warning informativo W-V5-RELATIVO sobre interpretação |
| **Não aditivo** (estoque · contagem distinta · ID) | ⚠ Condicional | Cálculo padrão se subtipo é estoque ou contagem; **bloqueio se subtipo é ID** detectado por heurística (§3.4) com escape "este campo é numérico de fato"; warning W-V5-NAO-ADITIVO |
| **Booleano** (flag · indicador binário disfarçado) | 🚫 Não · bloqueio estrutural | Bloqueio B-V5-CAMPO-BOOLEANO com microcopy "V5 não opera sobre campo booleano (apenas dois valores). Para análise de presença/ausência, considere V8" |

### 3.4 Detecção de subtipo ID (D-103 · requisito novo para Fundação)

Subtipo "ID disfarçado de número" (CPF · CNPJ · número de pedido · ID sequencial) é tecnicamente numérico mas semanticamente categórico. IQR/DP sobre IDs não tem interpretação útil. V5 detecta via heurística declarada (extensão da inferência semântica D-008 do motor_upload da Fundação):

**Critério da heurística:** campo numérico inteiro com cardinalidade ≥ 90% das linhas e (a) sequência aritmética detectável (incrementos de 1 ou constantes em ≥ 80% das diferenças consecutivas) **ou** (b) comprimento numérico fixo (CPF · CNPJ · códigos com 8+ dígitos com mesma quantidade de dígitos em 100% das linhas).

**Comportamento:** quando detectado · bloqueio B-V5-CAMPO-ID com microcopy de redirecionamento + opção "este campo é numérico de fato" (escape · marca warning permanente W-V5-ID-FORCADO no diagnóstico). Honra C.5 — sistema sinaliza, não decide; oferece escape consciente.

### 3.5 Fora de escopo de entrada

- Campos texto · categórico puro · data/timestamp · binário (0/1) — bloqueio estrutural pré-V5.
- Campos com menos de 5 registros válidos (após exclusão de nulos) — bloqueio B-V5-MINIMO-OPERACIONAL.
- Múltiplos campos principais simultâneos (V5 é univariada por execução).
- Análise comparativa entre dois recortes do mesmo campo (modo dual · ex: "antes vs depois") — fora do MVP · roadmap P-V5-COMPARACAO-DISTRIBUICOES-Evo.

---

## 4. Configuração analítica

### 4.1 Modo da base · granularidade declarada (D-102 · aplicação D-073)

V5 declara explicitamente a **granularidade da base** em duas dimensões:

| Granularidade | Significado | Default declarado | T-AGRUPA aplicada |
|---|---|---|---|
| **Individual** | Cada linha é uma observação individual (ex: extrato de transações · uma linha por venda) | ✅ Default declarado · editável | Modo no-op puro (passa o conjunto adiante) |
| **Consolidada por chave** | Cada linha é uma observação consolidada por chave declarada (ex: planilha com 1 linha por filial-mês contendo soma do faturamento) | Editável | Modo de validação de chave (verifica unicidade da chave declarada · gera warning estrutural W-V5-CHAVE-NAO-UNICA se duplicada) |

**Em nenhum modo V5 consolida valores.** O modo da base em V5 declara como interpretar a granularidade da entrada — não autoriza o motor a agregar valores. Quando granularidade é Consolidada por chave, a chave de consolidação (campo ou conjunto de campos) é declarada pelo usuário, e T-AGRUPA verifica unicidade sem operar agregação.

Esta posição diverge das visões V4/V7/V8/V9 onde T-AGRUPA consolida valores ativamente · diferença justificada pela natureza analítica de V5 (estatística descritiva univariada · qualquer agregação de valores deforma a distribuição observada). Aplicação canônica do padrão "herança adaptada à natureza analítica" (D-073). É a 4ª aplicação consecutiva do padrão "consolidação obrigatória pré-cálculo com blindagem contra dupla agregação" — V5 herda **a estrutura** (declaração explícita do modo + validação + T-AGRUPA aplicada + diagnóstico) sem herdar **o comportamento de consolidar valores**.

**Warning W-V5-GRANULARIDADE-SUSPEITA** (informativo · não bloqueia) é emitido quando o motor detecta possível incompatibilidade entre granularidade declarada e estrutura observada (ex: usuário declarou granularidade individual mas existe coluna ID claramente identificadora indicando granularidade consolidada).

### 4.2 T-AGRUPA em V5 · três modos (D-102)

V5 é a 8ª consumidora de T-AGRUPA (após V2 · V3 · V4 · V8 · V7 · V9 · V10 indiretamente via V4) com contrato V5-específico:

- **Modo no-op puro** · granularidade individual declarada (default) · T-AGRUPA passa o conjunto de observações adiante sem operar.
- **Modo de validação de chave** · granularidade consolidada declarada · T-AGRUPA verifica unicidade da chave declarada · emite warning estrutural se duplicada.
- **Modo de particionamento por Agrupador** · Modo Segmentado declarado (independente da granularidade) · T-AGRUPA particiona o conjunto de observações por valor único do Agrupador, sem consolidar valores dentro do segmento.

**Em nenhum modo V5 calcula soma · média · máximo · mínimo · contagem como agregação de valores.** A regra de agregação que define T-AGRUPA em V4/V7/V8/V9 não se aplica em V5.

CONTEXT §6 atualizada para refletir V5 como nova consumidora com semântica V5-específica.

### 4.3 Modo da Visão · Global × Segmentado

V5 opera em dois modos:

| Modo | Comportamento | Default |
|---|---|---|
| **Global** | Análise sobre o conjunto inteiro de observações válidas · uma única distribuição consolidada · uma única classificação de outliers | ✅ Default declarado · editável |
| **Segmentado** | Análise particionada por Agrupador · uma distribuição independente por segmento · classificação de outliers recalculada dentro de cada segmento | Editável |

Modo Global é default declarado porque é o caso mais comum em uso descritivo univariado (*"qual é o perfil deste campo no conjunto?"*). Padrão "default declarado" (D-024 sistematizado em V4) · ~10ª aplicação consecutiva.

### 4.4 Agrupador no Modo Segmentado

Em Modo Segmentado, **um único Agrupador** é obrigatório (MVP) · campo categórico que particiona o conjunto de observações em segmentos independentes de análise. Multi-agrupador (até 2-3 agrupadores) fica em roadmap (P-V5-MULTI-AGRUP-Evo). Espelha V9 (1 Agrupador no MVP) e V7 (Grupo único) com simetria estrutural.

**Restrições do Agrupador:**

- Campo principal não pode ser Agrupador (bloqueio B-V5-CAMPO-PRINCIPAL-COMO-AGRUP).
- Agrupador é campo categórico (texto ou numérico discreto com cardinalidade limitada · campo numérico contínuo bloqueia · B-V5-AGRUPADOR-NUMERICO).
- Agrupador com > 30% de valores nulos bloqueia (B-V5-AGRUPADOR-NULO-EXCESSIVO · segmentação degenerada).

### 4.5 Escala de cardinalidade do Agrupador (Modo Segmentado)

Patamares (eixo 2 da escala de cardinalidade · §8.1):

| Patamar | Faixa | Comportamento |
|---|---|---|
| Ideal | ≤ 50 segmentos | Sem alerta |
| Atenção | 51-200 | Alerta leve · W-V5-AGRUP-CARDINALIDADE-MEDIA |
| Crítico | 201-500 | Alerta forte · W-V5-AGRUP-CARDINALIDADE-ALTA |
| Excessivo | > 500 | Bloqueio · B-V5-AGRUP-EXCESSO |

### 4.6 Tratamento de segmento pequeno (Modo Segmentado)

Aplicação do mínimo operacional V5 (5 registros) por segmento, com tratamento em camadas:

| N do segmento | Comportamento |
|---|---|
| < 5 | Bloqueio individual do segmento (não calcula métricas estatísticas · linha aparece com classificação especial NAO_CALCULADO no Resumo por Segmento) + warning W-V5-SEGMENTO-INSUFICIENTE · cálculo prossegue nos demais segmentos |
| 5-29 | Cálculo padrão + alerta forte W-V5-SEGMENTO-PEQUENO ("limitação estatística") |
| ≥ 30 | Cálculo padrão sem warning |

Honra C.5 com gradação de sinalização e D-073 (mínimo operacional V5 = 5 aplica também a segmentos · consistência interna).

### 4.7 Tratamento de nulos no campo principal (D-073 · 4ª aplicação consecutiva do padrão)

Nulos no campo principal são **ignorados no cálculo** estatístico e registrados como **contagem agregada no diagnóstico**. Em Modo Segmentado, contagem por segmento. N válido (após exclusão de nulos) é o que conta para o mínimo operacional (5) e para o alerta de N pequeno (até 30).

**Adaptação V5 do padrão V4/V7/V9:** em V5, NULO_MEDIDA aparece como **contagem agregada em diagnóstico**, não como classificação por linha (porque V5 não tem unidade analítica "linha-elemento" como V4/V7/V9). 4ª aplicação consecutiva do padrão "tratamento explícito de nulos com classificação especial paralela".

**Warnings:**
- W-V5-NULOS-EXCLUIDOS (informativo) quando ≥ 1 nulo no campo principal.
- W-V5-NULOS-EXCESSIVOS (alerta) quando ≥ 30% dos registros têm nulo.
- B-V5-NULOS-EXCESSIVOS-CRITICO (bloqueio) quando > 80% dos registros têm nulo (impossibilidade analítica).

### 4.8 Tratamento de duplicidade (formalização de §2.4 + T-04)

Duplicidade no campo principal é **preservada como distribuição observada** (nunca consolidação). Três linhas com valor 50 são três observações em 50. Sem warning em duplicidade pura (comportamento esperado da visão).

**Concentração extrema** dispara warning W-V5-CONCENTRACAO-EXTREMA (informativo) quando ≥ 90% das observações estão no mesmo valor único (distribuição quase-degenerada · IQR/DP perdem sentido prático). Caso de distribuição inteiramente degenerada (todos os valores idênticos · DP = 0 · IQR = 0) bloqueia (B-V5-DISTRIBUICAO-DEGENERADA).

### 4.9 Tratamento de zeros

Zero é valor válido por **default declarado · editável**. Opção "Tratar zeros como valores ausentes (excluir do cálculo)" disponível em E2/E3 · default desativada. Quando ativada, zeros são tratados igual a nulos (ignorados + contados em diagnóstico separado · "X observações com zero excluídas a pedido do usuário · Y observações válidas") + warning permanente W-V5-ZEROS-COMO-NULOS.

Padrão "default declarado editável" honra C.5 (sistema oferece escolha · não decide silenciosamente) e cobre o caso "zero como placeholder de ausência" (estoque "não preenchido" registrado como 0).

### 4.10 Critérios de outlier · 3 critérios com defaults declarados editáveis (D-104)

V5 trabalha com 3 critérios de detecção de outliers · um critério ativo por execução · cada critério tem threshold configurável com default declarado · todos editáveis em **Configurações avançadas** no MVP:

| Critério | Default declarado | Range editável | Origem do default |
|---|---|---|---|
| **IQR (Tukey)** | multiplicador 1,5 | 1,0 a 3,0 (passo 0,1) | Tukey clássico · padrão de literatura |
| **Z-score** | \|z\| > 3 | 1,5 a 4,0 (passo 0,1) | Confirmação clássica (~99,7% em distribuição normal) |
| **Percentil** | P5 / P95 | P1/P99 · P5/P95 · P10/P90 (3 opções discretas) ou par customizado simétrico | Escolha de sensibilidade equilibrada |

**Configurações avançadas** mostra o threshold ativo do critério escolhido com slider/dropdown editável + opção "voltar ao default". Diagnóstico registra threshold ativo na execução. Warning W-V5-THRESHOLD-NAO-DEFAULT (informativo) quando usuário edita.

5ª aplicação consecutiva do padrão "thresholds multi-camada editáveis em Configurações avançadas" (V4 D-040 · V7 D-084/D-089 · V8 D-078 · V9 D-097/D-098 · **V5 D-104**) · candidato muito forte à formalização efetiva no próximo ajuste do CONTEXT.

### 4.11 T-MODELO em V5 (extensão D-104)

T-MODELO em V5 persiste:
- Critério ativo (IQR · Z-score · Percentil)
- Threshold ativo do critério escolhido (multiplicador IQR · limiar Z · par de percentis)
- Thresholds dos critérios não-ativos (preservados para troca rápida em re-execução)
- Outras configurações da V5 (campo principal · agrupador · nome analítico · modo da visão · granularidade · binning escolhido · etc) cobertas pelo padrão T-MODELO geral

---

## 5. Lógica de processamento

### 5.1 Lista oficial de métricas calculadas (13 · D-073 · adaptação V5)

V5 calcula 13 métricas estatísticas oficiais (11 do prévio + Amplitude + Skewness · D-105):

| Métrica | Fórmula | Caso-limite |
|---|---|---|
| Média | `Σx / N` | — |
| Mediana | valor central da lista ordenada (média dos dois centrais se N par) | — |
| Moda | valor(es) mais frequente(s) · tratamento múltiplo em §5.3 | — |
| Desvio Padrão (amostral) | `√(Σ(x-média)² / (N-1))` · default amostral · opção avançada para populacional | DP = 0 quando todos os valores são iguais |
| Variância (amostral) | `Σ(x-média)² / (N-1)` | Variância = 0 quando todos os valores são iguais |
| IQR | `Q3 - Q1` | IQR = 0 quando ≥ 50% dos valores são iguais ao centro |
| Q1 | 1º quartil (P25) | — |
| Q3 | 3º quartil (P75) | — |
| Mínimo | valor mínimo | — |
| Máximo | valor máximo | — |
| Amplitude | `Máximo - Mínimo` | — |
| Coeficiente de Variação | `DP / |Média|` quando média ≠ 0 | indefinido quando média = 0 (renderiza "—") |
| Skewness (amostral) | `[N / ((N-1)(N-2))] × Σ((xᵢ - média) / s)³` onde s é DP amostral · N ≥ 3 | indefinido quando N < 3 (renderiza "—") |

Curtose · MAD · percentis intermediários (P10 · P90 etc) ficam em roadmap (P-V5-CURTOSE-Evo · P-V5-MAD-Evo · P-V5-PERCENTIS-INTERMEDIARIOS-Evo).

### 5.2 Skewness · cálculo + classificação automática (D-105)

Skewness calculado pela fórmula amostral padrão (§5.1). Classificação automática em 3 faixas com thresholds default declarados editáveis:

| Faixa | Critério | Rótulo |
|---|---|---|
| Aproximadamente simétrica | \|skew\| < 0,5 | "Distribuição aproximadamente simétrica" |
| Moderadamente assimétrica | 0,5 ≤ \|skew\| < 1,0 | "Distribuição moderadamente assimétrica" (positiva/negativa conforme sinal) |
| Fortemente assimétrica | \|skew\| ≥ 1,0 | "Distribuição fortemente assimétrica" (positiva/negativa conforme sinal) |

Thresholds 0,5 e 1,0 são padrão estatístico aceito (não inventados) · default declarado editável em Configurações avançadas (6ª aplicação consecutiva do padrão T-08). Esta classificação alimenta o Bloco 5 do Resumo Executivo (leitura "Assimétrica") · §5.7.

### 5.3 Moda múltipla · tratamento em 4 camadas (D-105)

| Cenário | Comportamento | Warning |
|---|---|---|
| 1 moda | Retorna o valor único · sem flag | — |
| 2-5 modas | Retorna lista de valores · flag distribuição multimodal | W-V5-MULTIMODAL (informativo) |
| ≥ 6 modas | Retorna apenas contagem ("≥ 6 modas detectadas") + nota interpretativa "distribuição com muitos valores empatados em frequência máxima · provavelmente sem moda dominante" | W-V5-MULTIMODAL-EXCESSIVA (informativo) |
| Caso degenerado · todos valores únicos com frequência 1 | Retorna "sem moda" + nota "todos os valores observados ocorrem com mesma frequência · moda não tem interpretação útil" | W-V5-SEM-MODA-DEFINIDA (informativo) |

### 5.4 Desvio padrão amostral × populacional (D-105)

Default declarado: DP **amostral (n-1)** · base assumida como amostra (não censo total).

Opção avançada "tratar como população" disponível em Configurações avançadas quando o usuário sabe que a base é o universo declarado (ex: análise de desempenho de todos os 50 vendedores da empresa · não amostra de população maior). Quando ativada · cálculo muda para n · warning W-V5-DP-POPULACIONAL (informativo · permanente).

### 5.5 Taxonomia oficial V5 (D-105 + T-03 vocabulário dual)

Estrutura: 3 classes primárias por registro + 1 classificação especial paralela + 2 atributos derivados por registro + 5 leituras qualitativas de conjunto + Equilibrada como default sem destaque.

**Classes primárias por registro · vocabulário dual técnico/exibição:**

| Técnico (motor · contrato · Base Analítica) | Exibição (microcopy de tela · Resumo Executivo) |
|---|---|
| `NORMAL` | "Dentro do padrão" |
| `OUTLIER_SUPERIOR` | "Acima do limite" |
| `OUTLIER_INFERIOR` | "Abaixo do limite" |

**Classificação especial paralela:**

`VALOR_NAO_NUMERICO` · linha tem valor não-numérico no campo principal que escapou da pré-validação do upload (texto · "N/A" como string · etc). Linha aparece na Base Analítica com esta classe · contada em diagnóstico agregado · não entra no cálculo estatístico (igual a nulo · com nome distinto para auditoria). Warning W-V5-VALOR-NAO-NUMERICO (informativo) quando ≥ 1.

**Atributos derivados por registro:**

- **Distância do Limite** · numérico · aplicável a todos os registros:
  - Outlier Superior: `valor - Limite Superior` (positivo)
  - Outlier Inferior: `Limite Inferior - valor` (positivo)
  - Normal: `min(Limite Superior - valor, valor - Limite Inferior)` (negativo · indica margem para se tornar outlier)
  - Critério Z-score: distância em unidades de DP.
  - Critério Percentil: distância em centiles.
- **Faixa Percentual** · em qual decil/quartil o valor caiu (P0-P10 · P10-P25 · P25-P50 · P50-P75 · P75-P90 · P90-P100) · útil para leitura comparativa rápida.

**Leituras qualitativas de conjunto · 5 leituras multi-aplicáveis + 1 default sem destaque:**

| Leitura | Critério | Threshold |
|---|---|---|
| **Concentrada** | CV < 0,3 (default declarado editável) | T-08 · 7ª aplicação |
| **Dispersa** | CV ≥ 0,7 (default declarado editável) | T-08 · 7ª aplicação |
| **Assimétrica** | \|skewness\| ≥ 0,5 (já decidido em §5.2) | — |
| **Multimodal** | ≥ 2 modas detectadas (já decidido em §5.3) | — |
| **Com cauda relevante** | ≥ 5% de outliers detectados (default declarado editável) | T-08 · 7ª aplicação |
| **Equilibrada** (default sem destaque) | 0,3 ≤ CV < 0,7 e nenhuma outra leitura ativa | — |

Cada conjunto pode receber **múltiplas leituras simultâneas** (ex: Dispersa + Assimétrica + Multimodal) · não mutuamente exclusivas. Em Modo Segmentado, cada segmento recebe seu próprio conjunto de leituras (permite comparar perfis).

### 5.6 Tabela canônica das classes (formato espelho V7 §5.2 · V9 §5.6)

| Classe / Atributo | Código técnico | Microcopy de exibição | Critério |
|---|---|---|---|
| Classe primária | `NORMAL` | "Dentro do padrão" | Valor entre Limite Inferior e Limite Superior |
| Classe primária | `OUTLIER_SUPERIOR` | "Acima do limite" | Valor > Limite Superior do critério ativo |
| Classe primária | `OUTLIER_INFERIOR` | "Abaixo do limite" | Valor < Limite Inferior do critério ativo |
| Especial paralela | `VALOR_NAO_NUMERICO` | "Valor não-numérico" | Linha com valor não-numérico que passou da pré-validação |
| Atributo derivado | `distancia_limite` | "Distância do Limite" | Numérico · cálculo conforme §5.5 |
| Atributo derivado | `faixa_percentual` | "Faixa Percentual" | Decil/quartil (P0-P10 · P10-P25 · etc) |
| Leitura de conjunto | `CONCENTRADA` | "Distribuição concentrada" | CV < 0,3 |
| Leitura de conjunto | `DISPERSA` | "Distribuição dispersa" | CV ≥ 0,7 |
| Leitura de conjunto | `ASSIMETRICA_POSITIVA` / `ASSIMETRICA_NEGATIVA` | "Distribuição assimétrica" (positiva/negativa) | \|skewness\| ≥ 0,5 conforme §5.2 |
| Leitura de conjunto | `MULTIMODAL` | "Distribuição multimodal" | ≥ 2 modas conforme §5.3 |
| Leitura de conjunto | `COM_CAUDA_RELEVANTE` | "Distribuição com cauda relevante" | ≥ 5% de outliers |
| Leitura de conjunto | `EQUILIBRADA` (default) | "Distribuição equilibrada" | 0,3 ≤ CV < 0,7 e nenhuma outra leitura ativa |

### 5.7 Resumo Executivo · 6 blocos fixos (D-106 · 6ª aplicação consecutiva do padrão D-044)

Padrão "Resumo Executivo em 6 blocos fixos" tem 6 aplicações consecutivas (V4 · V3 · V8 · V7 · V9 · **V5**) e é candidato muito forte à formalização em CONTEXT §13 como padrão estrutural de produto.

**Bloco 1 · Cabeçalho** · identificação da execução. Conteúdo V5: campo principal · nome analítico · unidade · modo da visão (Global/Segmentado · com Agrupador se aplicável) · critério de outlier ativo + threshold · modo da base (granularidade) · timestamp · N total · N válido (após nulos).

**Bloco 2 · Números-âncora** · adaptação D-073 com 2 camadas em Modo Segmentado (D-106):

- **Camada agregada do conjunto** · 3 âncoras de "saúde geral": N total observações válidas · N de outliers totais (somados entre segmentos) · N de segmentos analisados.
- **Camada por segmento** · tabela compacta com 1 linha por segmento (Média · Mediana · DP · CV · % outliers do segmento) · ordenada por critério escolhido em E5 (default declarado: alfabético do agrupador).

Em Modo Global, Bloco 2 mostra apenas as 5-7 métricas-síntese (Média · Mediana · DP · IQR · CV · N de outliers · % de outliers · N total).

**Bloco 3 · Distribuição** · como observações se distribuem em classes:
- Distribuição por classe primária (% NORMAL · % OUTLIER_SUPERIOR · % OUTLIER_INFERIOR · % VALOR_NAO_NUMERICO se aplicável)
- Distribuição por Faixas (histograma simplificado em tela · §5.8)
- Distribuição por Faixa Percentual (P0-P10 · P10-P25 · etc)

**Bloco 4 · Valores destacados** · adaptação D-073 (V5 não tem "elemento" rotulado) · 3 sub-blocos (D-106):

- **Sub-bloco 4a · Top-N valores** · default N=5 editável (1 a 20) em Configurações avançadas (8ª aplicação T-08). Mostra: posição (rank · 1 a 5) · valor · classe primária · distância do limite/centro · linha de origem na base. Em Modo Segmentado: top-N **por segmento**.
- **Sub-bloco 4b · Bottom-N valores** · espelho de 4a · 5 menores valores observados. Em Modo Segmentado: bottom-N **por segmento**.
- **Sub-bloco 4c · Outliers detectados** · todos os outliers (Superior + Inferior · ordenados por distância do limite decrescente) · sem limite default · com paginação se > 50. Mostra: classe (Superior/Inferior) · valor · distância do limite · linha de origem · segmento (se aplicável). Se nenhum: frase "Nenhum outlier detectado pelo critério ativo".

**Bloco 5 · Leitura qualitativa com síntese** · 5 leituras qualitativas + síntese narrativa (§5.5). Em Modo Segmentado: leituras por segmento com microcopy comparativa cross-segmentos. Síntese narrativa: 1-2 frases interpretativas geradas a partir das leituras ativas (ex: *"Distribuição dispersa com assimetria positiva forte e cauda relevante de outliers superiores · Mediana significativamente menor que a Média sugere concentração no inferior com poucos valores muito altos"*).

**Bloco 6 · Qualidade estrutural** · saúde do diagnóstico (padrão · sem decisão substantiva específica V5). Conteúdo: warnings ativados (contagem por gravidade) · thresholds não-default usados · ajustes feitos · alertas de N pequeno · alertas de cardinalidade de Agrupador · porcentagem de nulos excluídos · porcentagem de zeros tratados como ausentes (se aplicável).

### 5.8 Mapa de Distribuição · coração visual da V5 (D-107)

V5 tem como **coração visual** a aba **"Mapa de Distribuição"** (alinhamento com Mapa de Grupos V7 · Mapa de Perfil V9 · Matriz de Presença V8). Aba dedicada com **Histograma** + **Tabela detalhada de Distribuição por Faixas**:

**Histograma:** gráfico nativo Excel via `openpyxl` (`BarChart` com bins) · gráfico primário no topo da aba.

**Tabela detalhada · 6 colunas:**

| Coluna | Conteúdo |
|---|---|
| Faixa | Identificador da faixa (Faixa 1 · Faixa 2 · etc) |
| Limite Inferior | Limite inferior da faixa (numérico) |
| Limite Superior | Limite superior da faixa (numérico) |
| Frequência | Quantidade absoluta de observações na faixa |
| % do Total | Frequência / N · ×100% |
| % Acumulada | Soma cumulativa de % do Total |

Coluna adicional opcional: "Tem outlier nesta faixa?" (sim/não · só nas faixas terminais).

Em Modo Segmentado: 1 conjunto (Histograma + tabela) por segmento, separados visualmente no Excel.

**Boxplot fica em roadmap** (P-V5-BOXPLOT-Evo) por complexidade técnica de implementação via openpyxl.

### 5.9 Regra de binning automático (D-107)

**Default declarado:** Regra de Sturges · `k = ⌈log2(N) + 1⌉`. Universal · razoável para 90% dos casos.

**Opções em Configurações avançadas:** Sturges (default) · Freedman-Diaconis (`largura = 2 × IQR / N^(1/3)` · robusto a outliers) · Scott (`largura = 3,5 × DP / N^(1/3)`) · número fixo (10 · 15 · 20 · 25 · 30 · 50).

9ª aplicação consecutiva do padrão "default declarado editável".

### 5.10 Estrutura Excel oficial V5 (D-108)

6 abas em Modo Global · 7 abas em Modo Segmentado · regra D-017 honrada (Diagnóstico sempre última aba):

| # | Aba | Modo Global | Modo Segmentado | Conteúdo |
|---|---|---|---|---|
| 1 | **Resumo Executivo** | ✅ | ✅ | 6 blocos (§5.7) |
| 2 | **Mapa de Distribuição** | ✅ | ✅ (1 conjunto por segmento) | Histograma + Tabela detalhada (§5.8) |
| 3 | **Resumo por Segmento** | ❌ | ✅ | 1 linha por segmento (Média · Mediana · DP · CV · % outliers) · ordenação configurável |
| 4 (3 em Global) | **Outliers** | ✅ | ✅ | Lista de outliers · classe · valor · Distância do Limite · linha original · segmento (se aplicável) |
| 5 (4 em Global) | **Base Analítica** | ✅ | ✅ | 1 linha por observação · campo principal + classe primária + atributos derivados (Distância do Limite · Faixa Percentual) + segmento (se aplicável) + linha original |
| 6 (5 em Global) | **Parâmetros** | ✅ | ✅ | Configurações ativas: campo · modo · critério + threshold · binning · agrupador · thresholds editados · granularidade declarada |
| 7 (6 em Global) | **Diagnóstico** (última · D-017) | ✅ | ✅ | Warnings ativados · ajustes · contagens (nulos · não-numéricos · zeros tratados como ausentes · etc) · saúde estrutural |

### 5.11 Aba "Dados Brutos do prévio descartada" (D-108 · 4ª aplicação consecutiva)

V5 não tem aba "Dados Brutos" · linhas originais aparecem na **Base Analítica** (aba 5 em Global · 5 em Segmentado · com colunas adicionais de classificação) · contagens estruturais (N total · N válido · N nulos · N não-numérico) aparecem no **Diagnóstico**. Rastreabilidade plena · sem aba duplicada.

4ª aplicação consecutiva do padrão "Dados Brutos descartada em favor de Base Analítica + Diagnóstico" (V8 D-078 · V7 D-089 · V9 D-099 · **V5 D-108**) · candidato muito forte à formalização efetiva no próximo ajuste do CONTEXT.

---

## 6. Contrato V5Result (síntese)

```
V5Result {
  metadata: {
    campo_principal: str,
    nome_analitico: str,
    unidade_medida: str,
    modo_visao: 'global' | 'segmentado',
    agrupador: str | None,
    granularidade_base: 'individual' | 'consolidada',
    chave_consolidacao: list[str] | None,
    criterio_outlier_ativo: 'iqr' | 'zscore' | 'percentil',
    threshold_ativo: dict,  # ex: {'multiplicador_iqr': 1.5}
    binning: 'sturges' | 'freedman-diaconis' | 'scott' | 'fixo:N',
    n_total: int,
    n_valido: int,
    n_nulos: int,
    n_nao_numericos: int,
    n_zeros_excluidos: int,  # 0 se opção não ativada
  },
  
  metricas_globais: {  # apenas em modo_visao='global'
    media: float, mediana: float, moda: list[float] | None, modas_em_excesso: bool,
    dp: float, variancia: float, iqr: float, q1: float, q3: float,
    minimo: float, maximo: float, amplitude: float,
    cv: float | None,  # None se média = 0
    skewness: float | None,  # None se N < 3
    classificacao_skewness: 'aproximadamente_simetrica' | 'moderadamente_assimetrica_positiva' | ...,
    leituras_qualitativas: list[str],  # multi-aplicáveis · 'EQUILIBRADA' default sem destaque
  },
  
  metricas_por_segmento: {  # apenas em modo_visao='segmentado'
    [segmento_id]: {
      n_segmento: int,
      n_valido_segmento: int,
      status_segmento: 'CALCULADO' | 'NAO_CALCULADO',  # NAO_CALCULADO se N<5
      ... # mesma estrutura de metricas_globais quando CALCULADO
    }
  },
  
  observacoes: [  # 1 por linha original com valor válido
    {
      linha_origem: int,
      valor: float,
      classe_primaria: 'NORMAL' | 'OUTLIER_SUPERIOR' | 'OUTLIER_INFERIOR' | 'VALOR_NAO_NUMERICO',
      distancia_limite: float | None,
      faixa_percentual: 'P0-P10' | 'P10-P25' | ...,
      segmento_id: str | None,  # apenas em modo_visao='segmentado'
    }
  ],
  
  distribuicao_faixas: {  # multi-segmento em modo_visao='segmentado'
    [segmento_id | 'global']: list[{
      faixa_id: int, limite_inferior: float, limite_superior: float,
      frequencia: int, pct_total: float, pct_acumulada: float,
      tem_outlier: bool
    }]
  },
  
  outliers: list[  # consolidados de todos os segmentos em modo_visao='segmentado'
    {
      linha_origem: int, valor: float,
      classe: 'OUTLIER_SUPERIOR' | 'OUTLIER_INFERIOR',
      distancia_limite: float,
      segmento_id: str | None
    }
  ],
  
  resumo_executivo: ResumoExecutivo6Blocos,  # padrão D-044 · §5.7
  diagnostico: Diagnostico,  # padrão T-DIAG · D-017 · §5.7 Bloco 6
  parametros: dict,  # configurações ativas para aba Parâmetros do Excel
}
```

---

## 7. Bloqueios operacionais (12 estruturais · D-109)

| # | Código | Descrição | Origem |
|---|---|---|---|
| 1 | B-V5-CAMPO-PRINCIPAL-NAO-NUMERICO | Campo principal não é numérico (texto · data · binário puro) | Prévio §2.2 |
| 2 | B-V5-CAMPO-BOOLEANO | Campo principal é booleano (0/1) | T-05 / D-103 |
| 3 | B-V5-CAMPO-ID (escapável) | Campo principal detectado como ID via heurística | T-05 / D-103 |
| 4 | B-V5-MINIMO-OPERACIONAL | N válido < 5 (após exclusão de nulos) | Prévio §2.6 + T-07 |
| 5 | B-V5-AGRUP-EXCESSO | Agrupador com > 500 valores únicos | T-06 |
| 6 | B-V5-CAMPO-PRINCIPAL-COMO-AGRUP | Campo principal selecionado também como agrupador | T-06 |
| 7 | B-V5-AGRUPADOR-NULO-EXCESSIVO | Agrupador com > 30% de valores nulos | D-073 herdado de V4 D-038 |
| 8 | B-V5-DISTRIBUICAO-DEGENERADA | Distribuição inteiramente degenerada (DP = 0 · IQR = 0) | T-07 |
| 9 | B-V5-NULOS-EXCESSIVOS-CRITICO | > 80% dos registros com valor nulo no campo principal | T-07 |
| 10 | B-V5-AGRUPADOR-NUMERICO | Agrupador é campo numérico contínuo | D-073 herdado |
| 11 | B-V5-MULTIPLOS-CRITERIOS-SIMULTANEOS | Tentativa de aplicar 2+ critérios de outlier simultaneamente em uma execução | T-08 |
| 12 | B-V5-MOTOR-INFERIU-TIPO-INCOMPATIVEL | Motor inferiu tipo Booleano ou ID com confiança alta · usuário não confirmou escape | T-05 |

---

## 8. Escala de cardinalidade V5 · 3 eixos multi-dimensionais independentes (D-109)

Espelha V9 (multi-eixo independente · não hierárquico-aditivo de V7 · não multiplicativo de V8). Aplicação D-073.

### 8.1 Eixo 1 · N observações válidas (após exclusão de nulos)

| Patamar | Faixa | Comportamento |
|---|---|---|
| Insuficiente | < 5 | Bloqueio (B-V5-MINIMO-OPERACIONAL) |
| Limitado | 5-29 | Cálculo prossegue + alerta forte (W-V5-N-PEQUENO) |
| Adequado | 30-499 | Cálculo padrão sem alerta |
| Robusto | 500-9.999 | Cálculo padrão · ideal |
| Volumoso | 10.000-99.999 | Cálculo padrão + alerta de performance (W-V5-VOLUME-MEDIO) |
| Extenso | 100.000+ | Cálculo padrão + alerta forte de performance (W-V5-VOLUME-ALTO) |

### 8.2 Eixo 2 · Cardinalidade do Agrupador (Modo Segmentado · ratifica §4.5)

| Patamar | Faixa | Comportamento |
|---|---|---|
| Ideal | ≤ 50 | Sem alerta |
| Atenção | 51-200 | W-V5-AGRUP-CARDINALIDADE-MEDIA |
| Crítico | 201-500 | W-V5-AGRUP-CARDINALIDADE-ALTA |
| Excessivo | > 500 | B-V5-AGRUP-EXCESSO |

### 8.3 Eixo 3 · Diversidade do campo principal (cardinalidade de valores únicos)

| Patamar | Faixa (% de N válido) | Comportamento |
|---|---|---|
| Concentrado | < 10% | Alerta W-V5-DIVERSIDADE-BAIXA · interpretação cuidadosa de IQR/quartis |
| Balanceado | 10-90% | Cálculo pleno · sem alerta |
| Disperso | > 90% | Alerta informativo W-V5-DIVERSIDADE-ALTA · raros valores repetidos · pode acionar W-V5-SEM-MODA-DEFINIDA |

### 8.4 Diretrizes de performance (9 · 7 herdadas + 2 específicas V5)

**Herdadas (de V3/V8/V7/V9):**
1. Cálculo de métricas em passe único sobre o dataset (não múltiplas passagens).
2. Ordenação O(N log N) reutilizada para quartis · percentis · skewness (não recalcular).
3. Particionamento por segmento via groupby único (não loop manual por segmento).
4. Materialização da Base Analítica em DataFrame único antes da exportação.
5. Histograma calculado uma vez · reutilizado em gráfico Excel + tabela detalhada.
6. Diagnóstico construído incrementalmente (não passe final).
7. Configurações avançadas validadas antes da execução (fail fast).

**Específicas V5:**
8. Detecção de subtipo ID (D-103) executada uma vez no upload (parte da inferência semântica D-008) · não recalculada a cada execução da V5.
9. Cálculo de skewness em passe único integrado com cálculo de média e DP (Σ(x-média)³ acumulado durante varredura inicial · não passe extra).

---

## 9. Roadmap pós-MVP P-V5-XX-Evo (13 candidatos)

| # | Código | Tema | Origem |
|---|---|---|---|
| 1 | P-V5-MULTI-AGRUP-Evo | Suporte a 2-3 Agrupadores em Modo Segmentado | T-06 |
| 2 | P-V5-MAD-Evo | Mediana Absoluta de Desvios (MAD) como métrica adicional | T-09 |
| 3 | P-V5-CURTOSE-Evo | Curtose (Kurtosis) como métrica adicional | T-09 |
| 4 | P-V5-PERCENTIS-INTERMEDIARIOS-Evo | Percentis adicionais (P10 · P90 · etc) calculados como atributos derivados | T-09 |
| 5 | P-V5-BOXPLOT-Evo | Boxplot como aba complementar (workaround openpyxl ou imagem renderizada externa) | T-12 |
| 6 | P-V5-CRITERIO-MAD-Evo | 4º critério de detecção de outlier baseado em MAD (`MAD-score` · robusto a outliers extremos) | T-08 + P-V5-MAD-Evo |
| 7 | P-V5-NORMALIDADE-TESTE-Evo | Teste estatístico de normalidade (Shapiro-Wilk · Kolmogorov-Smirnov) com microcopy interpretativa | T-09 |
| 8 | P-V5-COMPARACAO-DISTRIBUICOES-Evo | Comparação de duas distribuições (modo dual · análogo T-DUAL) entre dois recortes do mesmo campo | refino |
| 9 | P-V5-TRANSFORMACAO-LOG-Evo | Opção avançada de transformação logarítmica do campo principal antes da análise | T-09 + T-12 |
| 10 | P-V5-VISUALIZACAO-INTERATIVA-Evo | Versão interativa do histograma em tela (Streamlit nativo · não só Excel) com filtros por classe e por segmento | T-12 |
| 11 | P-V5-INFERENCIA-AUTOMATICA-CRITERIO-Evo | Motor sugere critério de outlier mais adequado com base em propriedades detectadas da distribuição | T-08 + IA assistiva |
| 12 | P-V5-EXPLICACAO-OUTLIER-Evo | Explicação contextual de cada outlier em microcopy gerada por IA assistiva | T-10 |
| 13 | P-V5-DETECCAO-MULTIMODAL-AVANCADA-Evo | Detecção avançada de multimodalidade via kernel density estimation | T-09 |

### 9.1 Anti-roadmap V5 · 2 itens explicitamente fora de escopo

| # | Item | Razão |
|---|---|---|
| 1 | **Imputação automática de valores nulos no campo principal** (substituir nulos por média/mediana/moda/zero antes da análise) | Descaracterizaria V5 como descritiva sobre o dado informado · violaria C.5 (sistema decidir pelo dado · inventar valores). Imputação é decisão do usuário em pré-processamento (M2 · TabloPrep · futuro) · nunca decisão silenciosa do motor V5. |
| 2 | **Limpeza/remoção automática de outliers** (excluir outliers do dataset antes do cálculo · ou gerar aba "dataset limpo") | Descaracterizaria V5 como visão de leitura · não de transformação (prévio §13: "V5 não é detector de erro · validador de dado · ferramenta de limpeza"). V5 sinaliza outliers · usuário decide o que fazer fora da V5. |

---

## 10. Warnings catalogados V5

Total estimado: **~37 warnings catalogados** (faixa V7 = 35 · V8 = 37 · V9 = 40 · V5 ≈ 37).

**Bloqueios (12)** — listados em §7.

**Alertas (~10):** W-V5-N-PEQUENO · W-V5-NULOS-EXCESSIVOS · W-V5-AGRUP-CARDINALIDADE-MEDIA · W-V5-AGRUP-CARDINALIDADE-ALTA · W-V5-SEGMENTO-INSUFICIENTE · W-V5-SEGMENTO-PEQUENO · W-V5-MULTIMODAL-EXCESSIVA · W-V5-VOLUME-MEDIO · W-V5-VOLUME-ALTO · W-V5-DIVERSIDADE-BAIXA.

**Informativos (~15):** W-V5-RELATIVO · W-V5-NAO-ADITIVO · W-V5-ID-FORCADO · W-V5-NULOS-EXCLUIDOS · W-V5-CONCENTRACAO-EXTREMA · W-V5-ZEROS-COMO-NULOS · W-V5-THRESHOLD-NAO-DEFAULT · W-V5-MULTIMODAL · W-V5-SEM-MODA-DEFINIDA · W-V5-DP-POPULACIONAL · W-V5-VALOR-NAO-NUMERICO · W-V5-DIVERSIDADE-ALTA · W-V5-CHAVE-NAO-UNICA · W-V5-GRANULARIDADE-SUSPEITA · W-V5-CONFIG-AVANCADA-USADA.

---

## 11. Posicionamento C.5

Aplicações canônicas de C.5 em V5:

1. **Modo da base declarado** (§4.1) — V5 não decide pela granularidade; usuário declara, motor valida. Default declarado seguro (Individual) cobre 90% · escape consciente para Consolidada.
2. **Tipos de medida com bloqueio + escape** (§3.3 · §3.4) — Booleano bloqueado sem exceção (não cabe estatisticamente); ID bloqueado com escape "este campo é numérico de fato" (sistema sinaliza · usuário decide forçar).
3. **Critérios de outlier com defaults declarados editáveis** (§4.10) — V5 não decide qual critério é "o melhor"; oferece 3 defaults consagrados pela literatura, todos editáveis em painel secundário, com diagnóstico registrando threshold ativo.
4. **Tratamento de nulos · zeros · duplicidade** (§4.7-4.9) — V5 não inventa valores · não consolida silenciosamente · sinaliza com warnings + diagnóstico agregado.
5. **Outlier como conteúdo · não correção** (§5.5 + §11 anti-roadmap) — V5 sinaliza outliers como classe primária · nunca remove · nunca interpreta como erro de origem.
6. **Leituras qualitativas multi-aplicáveis** (§5.5 · §5.7 Bloco 5) — V5 não escolhe "a leitura principal" do conjunto · acumula todas as leituras ativas e deixa o usuário interpretar a combinação.

---

## 12. Relação com Fundação

### 12.1 Transversais consumidos

- **T-AGRUPA** · contrato V5-específico (§4.2) · 3 modos (no-op puro · validação de chave · particionamento sem consolidar valores) · em nenhum modo V5 consolida valores. **V5 é a 8ª consumidora de T-AGRUPA**.
- **T-DIAG** · padrão obrigatório (Diagnóstico sempre última aba · D-017).
- **T-MODELO** · persiste critério ativo + threshold ativo + thresholds não-ativos + outras configurações (extensão D-104).

### 12.2 Transversais não aplicáveis a V5

- **T-SEMA** · não aplicável · V5 é descritiva univariada sem direção valorativa intrínseca (campo numérico tem distribuição · não tem "maior é melhor").
- **T-EIXO** · não aplicável · V5 não opera sobre eixo ordenado.
- **T-RANK** · não aplicável · V5 não ranqueia elementos cross-conjunto (Top-N do Bloco 4 é ordenação trivial por valor · não consome T-RANK).
- **T-ACUM · T-ABC · T-PIVOT · T-DUAL · T-FUZZY · T-CONCAT** · não aplicáveis.

### 12.3 Requisitos novos para a Fundação (G-FUND)

1. **`motor_upload`** · extensão da inferência semântica (D-008) com **detecção de subtipo ID** (heurística declarada em §3.4) · usado por V5 para bloqueio B-V5-CAMPO-ID com escape.
2. **`exportacao.py`** · capability **Histograma nativo Excel** via `openpyxl` (`BarChart` com bins) para aba "Mapa de Distribuição" (§5.8). Sem workaround necessário · funcionalidade nativa.
3. **`T-AGRUPA`** · contrato estendido para suportar **3 modos V5-específicos** (no-op puro · validação de chave · particionamento sem consolidar) — modos distintos dos modos V8/V7/V9 (que consolidam valores). Documentação canônica do contrato T-AGRUPA passa a refletir essa pluralidade.

### 12.4 Aplicações e validações de padrões consolidados

- **4ª aplicação consecutiva** do padrão "consolidação obrigatória pré-cálculo com blindagem contra dupla agregação" (V8 D-074 · V7 D-082 · V9 D-092 · **V5 D-102**) — candidato muito forte à formalização.
- **5ª aplicação consecutiva** do padrão "thresholds multi-camada editáveis em Configurações avançadas" (V4 D-040 · V7 D-084 · V8 D-078 · V9 D-097 · **V5 D-104**) — candidato muito forte à formalização.
- **6ª aplicação consecutiva** do padrão "Resumo Executivo em 6 blocos fixos" D-044 (V4 · V3 · V8 · V7 · V9 · **V5**) — candidato muito forte à formalização em CONTEXT §13 como padrão estrutural de produto.
- **4ª aplicação consecutiva** do padrão "Dados Brutos descartada em favor de Base Analítica + Diagnóstico" (V8 D-078 · V7 D-089 · V9 D-099 · **V5 D-108**) — candidato muito forte à formalização.
- **~10ª aplicação** do padrão "default declarado" (D-024 sistematizado V4 · agora aplicado em ~10 dimensões V5: granularidade da base · modo da visão · 3 thresholds de critério · binning · 3 leituras qualitativas · DP amostral × populacional · Top-N Bloco 4 · zeros como ausentes).
- **11ª aplicação documentada** do padrão "herança adaptada à natureza analítica" (D-073) — V5 aplica em: T-AGRUPA semântica V5-específica · NULO_MEDIDA agregada em diagnóstico não por linha · Bloco 4 reformulado como "valores destacados" sem unidade analítica rotulada · escala multi-eixo independente alinhada com V9 · matriz declarativa simétrica vs. assimétrica nos pares de família.

---

## 13. Nomenclatura oficial V5

### 13.1 Termos canônicos (~24 termos em 5 categorias)

**Estrutura analítica (7 termos):**
- `Campo Principal` — campo numérico sobre o qual a análise é realizada
- `Nome Analítico` — rótulo de exibição do campo principal
- `Unidade de Medida` — unidade do campo principal (R$ · % · dias · etc)
- `Modo da Visão` — Global × Segmentado (§4.3)
- `Modo da Base` — Granularidade Individual × Consolidada por chave (§4.1)
- `Agrupador` — campo categórico que segmenta em Modo Segmentado (§4.4)
- `Unidade analítica V5` — observação individual no campo numérico principal (§2.4)

**Métricas estatísticas (12 termos):**
- `Tendência Central` — categoria que reúne Média · Mediana · Moda
- `Média` (aritmética) · `Mediana` · `Moda`
- `Distribuição Multimodal` — distribuição com 2+ modas (§5.3)
- `Dispersão` — categoria que reúne DP · Variância · IQR · CV · Amplitude
- `Desvio Padrão` (amostral default · populacional opção avançada) · `Variância`
- `IQR` (Amplitude Interquartil) · `Q1` · `Q3` · `Quartil`
- `Coeficiente de Variação` (CV) · `Mínimo` · `Máximo` · `Amplitude`
- `Skewness` (Assimetria) — métrica calculada (§5.2)

**Outliers (8 termos):**
- `Critério de Outlier` (3 critérios oficiais)
- `IQR / Tukey` — multiplicador 1,5 default editável
- `Z-score` — limiar |z| > 3 default editável
- `Percentil` — cortes P5/P95 default editáveis
- `Limite Inferior` · `Limite Superior` — fronteiras calculadas pelo critério ativo
- `Outlier Superior` (técnico OUTLIER_SUPERIOR · exibição "Acima do limite")
- `Outlier Inferior` (técnico OUTLIER_INFERIOR · exibição "Abaixo do limite")
- `Resumo com Outliers` · `Resumo sem Outliers` — leituras comparativas (no Bloco 5)

**Classificação (4 termos):**
- `Normal` (técnico NORMAL · exibição "Dentro do padrão")
- `VALOR_NAO_NUMERICO` — classificação especial paralela (§5.5)
- `Distância do Limite` — atributo derivado por registro
- `Faixa Percentual` — atributo derivado por registro (P0-P10 · etc)

**Visualização e exportação (3 termos):**
- `Distribuição por Faixas` — histograma com tabela detalhada
- `Histograma` — gráfico nativo Excel da aba "Mapa de Distribuição"
- `Mapa de Distribuição` — coração visual da V5 (aba Excel · §5.8)

### 13.2 Vocabulário dual técnico/exibição (6 pares)

| Técnico (motor · contrato · Base Analítica) | Exibição (microcopy de tela · Resumo Executivo) |
|---|---|
| `OUTLIER_SUPERIOR` | "Acima do limite" |
| `OUTLIER_INFERIOR` | "Abaixo do limite" |
| `NORMAL` | "Dentro do padrão" |
| `IQR` (sigla) | "Amplitude interquartil" |
| `Z-score` | "Distância padronizada" |
| `Coeficiente de Variação` (CV em tabelas) | "Coeficiente de Variação (CV %)" em microcopy explicativo |

### 13.3 Anti-glossário V5 (5 termos a evitar)

| Termo a evitar | Motivo da rejeição |
|---|---|
| **"Erro" / "Anomalia" / "Desvio anormal"** como sinônimo de outlier | V5 não interpreta causa. Outlier estatístico não é erro de origem · não é anomalia automaticamente · é fato matemático |
| **"Distribuição normal"** sem qualificar | Pode confundir "valor não-outlier" (uso V5) com "curva gaussiana" (estatística). V5 não pressupõe normalidade |
| **"Limpeza" / "correção"** de outliers | V5 sinaliza · nunca remove · nunca corrige. Anti-roadmap explícito (§9.1) |
| **"Distribuição típica" / "comportamento esperado"** sem qualificar | Pode soar como julgamento de valor · V5 descreve · não prescreve |
| **"Filtragem"** de outliers | Confunde com filtro de dados. V5 oferece "Resumo sem Outliers" como leitura comparativa · não filtragem |

---

## 14. Decisões geradas

| D-XXX | Tema | Tipo |
|---|---|---|
| **D-102** | Modo da base V5 declarado em granularidade · T-AGRUPA com semântica V5-específica · 4ª aplicação consecutiva do padrão "consolidação obrigatória pré-cálculo" · adaptação D-073 | Transversal (V5 + T-AGRUPA + CONTEXT §6 · §9) |
| **D-103** | Tipos de medida em V5 · Aditivo/Relativo aceitos · Não aditivo condicional com detecção de subtipo ID · Booleano bloqueado · aplicação D-073 herdada de V7 D-083 | Específica V5 + requisito Fundação (motor_upload) |
| **D-104** | 3 critérios de outlier em V5 com defaults declarados editáveis em Configurações avançadas · 5ª aplicação consecutiva do padrão "thresholds multi-camada editáveis" | Específica V5 + CONTEXT §9 (candidato a formalização) |
| **D-105** | Taxonomia oficial V5 · 3 classes primárias com vocabulário dual + 1 especial paralela (VALOR_NAO_NUMERICO) + 2 atributos derivados + 5 leituras qualitativas multi-aplicáveis | Específica V5 + GLOSSARIO 5.V5 |
| **D-106** | Resumo Executivo V5 com 6 blocos · Bloco 2 com 2 camadas em Modo Segmentado · Bloco 4 reformulado como "valores destacados" em 3 sub-blocos · 6ª aplicação consecutiva D-044 | Específica V5 + CONTEXT §13 (candidato a formalização) |
| **D-107** | Mapa de Distribuição como coração visual V5 · Histograma + Tabela detalhada · Sturges como default declarado editável · Boxplot em roadmap · requisito novo para Fundação | Específica V5 + requisito Fundação (exportacao.py) |
| **D-108** | Estrutura Excel V5 · 6 abas em Global / 7 em Segmentado · "Resumo por Segmento" condicional · "Dados Brutos do prévio" descartada · 4ª aplicação consecutiva | Específica V5 + CONTEXT §9 (candidato a formalização) |
| **D-109** | Bloqueios operacionais V5 (12) + escala de cardinalidade em 3 eixos multi-dimensionais independentes + 9 diretrizes de performance (7 herdadas + 2 específicas V5) | Específica V5 |
| **D-110** | Sumário do refino DCV-V5 · 15 pendências fechadas em sessão única · Família E reformulada para "Estrutura interna do recorte" · adaptação D-073 ao método de posicionamento de família · sem retroação diferida formal V5→V6 | Sumário do refino |

---

## 15. Pendências do refino (histórico)

15 pendências fechadas em sessão única (19/04/2026):

- **Bloco A · Posicionamento e fronteira (3):** T-01 (Família E reformulada · §2.3 enxuto sem retroação) · T-02 (3 fronteiras V5×V7/V9/V4 em prosa) · T-03 (vocabulário canônico robusto + dual + anti-glossário)
- **Bloco B · Entrada e estrutura analítica (4):** T-04 (modo da base + T-AGRUPA semântica V5-específica · D-102) · T-05 (tipos de medida · D-103) · T-06 (Modo Global × Segmentado + Agrupador · default declarado) · T-07 (nulos · duplicidade · zeros · 4 warnings novos)
- **Bloco C · Cálculo e classificação (5):** T-08 (3 critérios de outlier · D-104) · T-09 (13 métricas + skewness + moda múltipla + DP amostral) · T-10 (taxonomia oficial · D-105) · T-11 (Resumo Executivo 6 blocos · D-106) · T-12 (Mapa de Distribuição · D-107)
- **Bloco D · Saída e operação (3):** T-13 (estrutura Excel · D-108) · T-14 (bloqueios + cardinalidade + performance · D-109) · T-15 (roadmap 13 candidatos + anti-roadmap 2)

---

## 16. Referências

- **CONTEXT.md** §3 (Fase 0) · §4 (Família E reformulada · D-110) · §6 (T-AGRUPA estendida com V5) · §9 (4ª e 5ª aplicações de padrões) · §13 (Resumo Executivo 6 blocos · candidato muito forte a formalização)
- **DECISIONS.md** D-008 (inferência semântica) · D-017 (Diagnóstico última aba) · D-024 (default declarado) · D-025 (4 tipos de campo) · D-044 (Resumo Executivo 6 blocos) · D-073 (herança adaptada à natureza analítica) · D-076 (warning vs conteúdo) · D-082 (modo no-op validado V7) · D-092 (T-AGRUPA multi-regra V9) · D-102 a D-110 (decisões V5)
- **GLOSSARIO.md** §1 (Família conceitual reformulada · Princípio C.5) · §4 (T-AGRUPA estendida) · seção 5.V5 nova (~24 termos) · §6 Warnings V5 (~37 catalogados) · §10 (vocabulário dual · padrões consolidados) · §11 (anti-glossário V5)
- **TabloFlow_Estado_do_Projeto.xlsx** aba 1 (10 de 11 DCVs aprovados) · aba 2 (V5 refinada) · aba 3 (T-AGRUPA com V5 como 8ª consumidora) · aba 4 (V5 com nota DCV aprovado)
- **DCVs aprovados consultados:** dcv_v7.md (precedente direto · fronteira V5×V7) · dcv_v9.md (precedente direto · fronteira V5×V9 · padrão multi-eixo independente) · dcv_v4.md (precedente de Curva ABC · tipos de medida D-025/D-036)

---

**Fim do DCV-V5.** Aprovado, próxima Fase 0: DCV-V6 (Relacionamento entre Dimensões · matriz de cruzamento entre 2 campos categóricos · fecha a Família E e a Fase 0 · G-FUND abre em sequência direta).
