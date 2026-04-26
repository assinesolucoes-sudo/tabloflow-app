# DCV-V9 · Perfil de Ranking por Métricas

**Visão:** V9 · Perfil de Ranking por Métricas
**Módulo:** Módulo 1 · TabloAnálise
**Família:** D · Posição relativa
**Status:** Aprovado
**Data aprovação:** 19/04/2026
**Sessão de refino:** 1 (sessão única, 12 pendências fechadas)
**Arquivo canônico:** `/specs/dcv/dcv_v9.md`

**Substrato herdado:**
- **DCV-V7 aprovado** (19/04/2026 · D-081 a D-090 · 13 pendências) — primeira visão da Família D · precedente DIRETO · substrato §2.3 simétrico
- **DCV-V4 aprovado** (19/04/2026) — precedente de múltiplas medidas (Modo 3) · comparação par-a-par entre medidas
- **DCV-V8 aprovado** (19/04/2026) — padrão "herança adaptada à natureza analítica" (D-073) · padrão "warning vs conteúdo" (D-076)
- **CONTEXT.md** (v19/04/2026 pós DCV-V7) — T-RANK com 6 consumidoras · T-SEMA como transversal consumido · padrão default declarado sistematizado

---

## 1. Propósito da visão

A V9 responde: **"dentro do meu conjunto de elementos, quem se destaca em cada métrica, quem apresenta melhor posicionamento consolidado e quem demonstra perfil de liderança, especialização, equilíbrio ou retaguarda?"**

A visão analisa **posicionamento relativo multidimensional** — benchmarking interno em múltiplas métricas simultâneas. Para cada Identificador, calcula Posição em cada métrica configurada (respeitando Direção declarada por métrica), consolida as Posições em Score Consolidado (média aritmética simples), calcula Variação Máxima de Posição entre métricas, e classifica o Identificador em uma de 4 classes de perfil: Líder, Especialista, Equilibrado ou Retaguarda. É **visão autônoma da Família D** (não view especializada sobre V7; par autônomo — §2.3).

A V9 opera sobre um conjunto único por execução (Global) ou segmentada por Agrupador (Segmentado). Aplica o princípio **"consolidar primeiro, ranquear depois"**: Identificadores com duplicidade no dado de entrada são consolidados via T-AGRUPA com regra de agregação declarada **por métrica** antes de qualquer ordenação.

A V9 não diagnostica causa raiz, não declara que um perfil é bom ou ruim por si só, e não afirma que liderança em ranking implica superioridade operacional. Evidencia o posicionamento relativo; a interpretação causal cabe ao usuário.

---

## 2. Posicionamento analítico

### 2.1 O cenário real que a V9 atende

A V9 atende o uso contábil, gerencial e operacional típico de análise comparativa multidimensional de desempenho:

- **Perfil de vendedores** em carteira considerando faturamento, ticket médio, taxa de conversão, tempo de ciclo — quem lidera em todas, quem especializa em uma, quem equilibra.
- **Portfólio de produtos** com margem, giro, retorno por metro quadrado, crescimento YoY — Líderes do portfólio × Especialistas de nicho × Retaguarda para revisão.
- **Comparação de filiais** em indicadores heterogêneos (receita · custo operacional · NPS · tempo médio de atendimento) com direções distintas.
- **Ranking de fornecedores** em custo, prazo, qualidade, flexibilidade — compor perfil consolidado com direções declaradas por métrica.
- **Priorização de campanhas de marketing** por ROI, alcance, engajamento, taxa de conversão simultâneos.

Em todos esses cenários, o analista humano hoje recorre a planilhas com colunas de ranking por métrica + média das posições manual. A V9 estrutura esse trabalho, garante consolidação antes de ranquear (evitando dupla agregação), respeita direções declaradas por métrica, e entrega saída Excel com Mapa de Perfil auditável.

### 2.2 Fronteira com V4 e V5 (visões vizinhas)

**V9 × V4 (Família C · Composição).** V4 analisa composição: quanto cada elemento representa do total geral (participação), com ou sem curva de concentração (ABC/Pareto). Mesmo quando opera em Modo 3 (Comparação de Distribuição com múltiplas medidas), o que V4 entrega é **posição de cada elemento dentro do total de cada medida separadamente** + classe ABC por medida + atributo de divergência par-a-par contra medida de referência (D-042). V4 responde *"quanto esse elemento pesa no total da métrica X?"* e *"a dominância em Receita se traduz em dominância em Margem?"*.

V9 não rastreia participação no total. V9 consolida **múltiplas métricas num score único por elemento** via média de posições e classifica o elemento pelo **perfil combinado** das posições (Líder · Especialista · Equilibrado · Retaguarda). V9 responde *"quem se destaca quando considerados N indicadores simultaneamente com direções distintas?"*.

Diferenças concretas na natureza analítica (aplicação de D-073):

| Eixo | V4 Modo 3 (Comparação de Distribuição) | V9 (Ranking Multidimensional) |
|---|---|---|
| Referência | Total Geral de cada medida separadamente | Posição dentro do conjunto por métrica, combinada em score |
| Direção das medidas | Todas com leitura "maior participação = mais relevante" | Cada métrica com direção declarada (Maior/Menor-é-melhor) |
| Medida de referência | Existe, com 3 papéis (ordenação, leitura, eixo de comparação par-a-par) | Não existe — todas as métricas contribuem igualmente para o score |
| Saída por elemento | Classe ABC por medida + divergência composta + delta de ranking | Posição por métrica + score consolidado + variação máxima de posição + classe de perfil |
| Pergunta respondida | "Onde está a concentração e onde as medidas divergem?" | "Quem tem o melhor perfil consolidado considerando direções distintas?" |

Elemento que é Classe A em V4 Modo 3 (domina o total de Receita) pode ser Especialista em V9 (líder em Receita, retaguarda em Margem, meio em Volume — alta variação de posições). Elemento Classe B em V4 pode ser Líder em V9 (top em todas as 4 métricas por pouca margem cada). **As visões são complementares em portfólio: V4 para mapa de participação com divergência entre medidas; V9 para perfil consolidado com direções heterogêneas.**

**V9 × V5 (Família E · Estrutura interna).** V5 analisa **dispersão estatística interna de um campo numérico**: IQR, Z-score, percentil, detecção de outliers. O que V5 entrega é propriedade estatística derivada do próprio campo — cauda longa, simetria, concentração de valores, distância de ponto extremo à massa. V5 opera sobre **um campo por execução**, olhando para como os valores se distribuem dentro dele.

V9 opera sobre **múltiplas métricas simultâneas**, mas não extrai propriedade estatística de nenhuma delas: para V9, cada métrica é apenas **critério de ordenação**; o que importa é a **posição consolidada** do elemento cross-métricas. V9 não calcula IQR, não detecta outliers, não classifica por Z-score.

Aplicação do padrão **"warning em uma visão pode ser conteúdo em outra"** (D-076, análogo V7 × V5): métrica com valores muito dispersos (outliers) em V5 é **conteúdo primário** (elemento outlier é o destaque analítico); a mesma métrica em V9 é **input de ordenação** — o valor extremo empurra o elemento para o topo/base do ranking daquela métrica, afetando seu score consolidado, mas V9 não sinaliza "outlier" como atributo da saída. Quem quer medir dispersão de um indicador como característica intrínseca usa V5; quem quer ranquear elementos considerando múltiplos indicadores simultâneos usa V9.

Caso típico de confusão: *"Quais vendedores são outliers em performance?"* — se a pergunta é sobre **uma única métrica** (só faturamento), usar V5 (dispersão estatística); se é sobre **combinação de múltiplos indicadores** (faturamento × ticket médio × conversão com direções declaradas), usar V9 (perfil consolidado).

**V9 × V7 (já tratado em §2.3).** Fronteira V9 × V7 é tratada em §2.3 (par autônomo da Família D). Nenhuma outra seção deste DCV revisita a fronteira entre as duas — microcopy operacional é declarativa autossuficiente em cada visão.

Nenhuma dessas fronteiras é navegada em interface operacional. Microcopy declarativa autossuficiente no DCV + nota estática final no Resumo Executivo (Bloco 5 · §5.9) redirecionam quando apropriado.

### 2.3 Relação com V7 (par autônomo da Família D)

V7 e V9 convivem como par autônomo da Família D — mesma família, problemas analíticos distintos, motores distintos, vocabulário parcialmente compartilhado (T-SEMA · T-RANK · T-AGRUPA).

**Família D · Posição relativa** — visões que analisam como cada elemento se posiciona em relação a um benchmark calculado internamente sobre os próprios dados. V7 calcula o benchmark como média do grupo ao qual o elemento pertence (desvio univariado intra-grupo); V9 calcula o benchmark como posição consolidada em múltiplas métricas ordenadas com direção declarada (ranking multidimensional cross-elementos). Ambas consomem T-SEMA; V7 também consome T-AGRUPA e T-RANK (este com regra de desempate V7-específica); V9 também consome T-AGRUPA e T-RANK (este com regra de desempate V9-específica). Não há view especializada entre elas — são visões autônomas da mesma família.

| Aspecto | V9 · Perfil de Ranking por Métricas | V7 · Desvio em Relação à Média do Grupo |
|---|---|---|
| O que rastreia | Posição consolidada de cada Identificador em ranking por múltiplas métricas simultâneas (multidimensional) | Desvio de cada Elemento em relação à média do seu Grupo (univariado) |
| Unidade analítica | Identificador (modo Global) · Identificador + Agrupadores ativos (modo Segmentado) | Elemento + Grupo (com valor consolidado pela regra de agregação) |
| Classificação do resultado | **Líder · Especialista · Equilibrado · Retaguarda** (4 classes com prioridade declarada) | Acima · Na Média · Abaixo (+ atributo Desvio Significativo) |
| Transversais comuns | T-AGRUPA · T-SEMA (por métrica) · T-RANK (cross-elementos) · T-DIAG · T-MODELO | T-AGRUPA · T-SEMA (global) · T-RANK (intra-grupo) · T-DIAG · T-MODELO |
| Tipo de medida | Múltiplas medidas numéricas (2 a 6) por execução, cada uma com direção declarada | Uma medida numérica por execução |

**Não há substituição de uma pela outra.** O usuário escolhe conscientemente a visão pela pergunta que quer responder: *"quais elementos se destacam quando consideradas múltiplas métricas simultaneamente?"* (V9) ou *"dentro de cada grupo, quem destoa da média?"* (V7). A fronteira é navegada por microcopy declarativa e autossuficiente em cada visão — nenhuma das duas menciona a outra em interface operacional. Quem precisa entender ambas lê este bloco no DCV. **Este bloco cumpre a retroação diferida V7→V9 registrada em D-081.**

### 2.4 Unidade analítica da V9

Unidade analítica da V9 é **derivada do Modo de Ranking declarado pelo usuário:**

- **Modo Global** → unidade analítica = **Identificador** (um único ranking sobre todo o conjunto)
- **Modo Segmentado** → unidade analítica = **Identificador + Agrupador ativo** (ranking recalculado dentro de cada valor do agrupador)

No modo Segmentado, mesmo valor do Identificador em diferentes valores do Agrupador é tratado como **duas unidades analíticas distintas** (padrão herdado V7 §4.5): vendedor João em região Sudeste e em região Nordeste gera duas linhas na saída, com posições e scores independentes.

Princípio **"consolidar primeiro, ranquear depois"** preservado do prévio 4.3: consolidação via T-AGRUPA é **obrigatória sempre**, aplicada no Passo 1 do pipeline (§5.2). Quando o modo da base é Pré-agregado, T-AGRUPA roda como **no-op validado** (verifica unicidade sem consolidar); quando é Transacional, consolida efetivamente. A ordem é a **blindagem central contra dupla agregação** — armadilha em que ordenar sobre linhas brutas (sem consolidar o Identificador) corrompe o ranking cross-elementos de todas as métricas.

---

## 3. O que a visão recebe

### 3.1 Estrutura de entrada

Uma base lógica por execução, com uma ou mais abas. O usuário escolhe **uma aba** para análise. O padrão oficial do projeto privilegia a escolha explícita da aba pelo usuário.

Formato de entrada: **tabela plana** com linhas representando registros (Transacional) ou uma linha por Identificador (Pré-agregado). Colunas identificam o Identificador, 2-6 campos numéricos como Métricas, e opcionalmente um campo categórico como Agrupador (obrigatório no modo Segmentado).

### 3.2 Fora de escopo de entrada

- **Identificador composto** (múltiplos campos concatenados como chave) — P-V9-07-Evo · consome T-CONCAT (D-053) quando implementado.
- **Múltiplas abas processadas em conjunto** — usuário escolhe uma aba por execução; multi-aba entra no domínio M2.STACK (D-063) quando o Módulo 2 estiver disponível.
- **Múltiplos Agrupadores no modo Segmentado** — MVP limita a 1 Agrupador ativo; P-V9-08-Evo.

### 3.3 Campos obrigatórios

- **Identificador** — exatamente 1 campo categórico obrigatório (vendedor, produto, filial, cliente, fornecedor, campanha, contrato).
- **Métricas** — 2 a 6 campos numéricos obrigatórios (mínimo estrutural; máximo recomendado; limite absoluto = 10 com alerta forte, bloqueio em 11+).
- **Direção por métrica** — cada métrica declarada deve ter Direção: Maior-é-melhor OU Menor-é-melhor (sem default; declaração obrigatória).

### 3.4 Campos opcionais

- **Agrupador** — obrigatório apenas quando Modo de Ranking = Segmentado; dispensável em Modo Global.

---

## 4. Configuração pelo usuário

### 4.1 Modo da base (Transacional × Pré-agregado) com default declarado

Modo da base declarado pelo usuário em E2 com **default declarado detectado pelo motor** na amostragem (padrão herdado de V7 D-082 · V8 D-074).

**Detecção default:**
- Se motor detecta duplicatas da unidade analítica na amostra → modo **Transacional** proposto como default
- Se unidade analítica é única em 100% dos casos detectados → modo **Pré-agregado** proposto como default

**Modo Transacional:** consolidação via T-AGRUPA obrigatória com regra de agregação declarada **por métrica** (§4.7). Múltiplas linhas da mesma unidade analítica são consolidadas em 1 linha por combinação antes do cálculo de posições.

**Modo Pré-agregado:** T-AGRUPA opera como no-op validado. Motor verifica unicidade no volume completo (não apenas na amostra); se detecta duplicatas inesperadas, dispara bloqueio estrutural **W-V9-MODO-VIOLACAO**.

**Warnings:**
- **W-V9-MODO-TRANS-DEFAULT** (informativo) — modo Transacional aceito sem edição
- **W-V9-MODO-TRANS-CUSTOM** (informativo) — usuário editou para Transacional
- **W-V9-MODO-PREAGG-DEFAULT** (informativo) — modo Pré-agregado aceito sem edição
- **W-V9-MODO-PREAGG-CUSTOM** (informativo) — usuário editou para Pré-agregado
- **W-V9-MODO-VIOLACAO** (bloqueio) — modo Pré-agregado declarado mas duplicatas detectadas

### 4.2 Modo de Ranking (Global × Segmentado) — deriva unidade analítica

Modo de Ranking declarado pelo usuário em E3 com 2 valores oficiais:

- **Global** → unidade analítica = Identificador · ranking único sobre todo o conjunto
- **Segmentado** → unidade analítica = Identificador + Agrupador ativo · ranking recalculado em cada valor do agrupador

**Agrupador obrigatório no modo Segmentado.** Sem Agrupador ativo, modo Segmentado bloqueia a execução.

**Escopo MVP:** 1 Agrupador ativo máximo em Segmentado. Múltiplos Agrupadores entram em P-V9-08-Evo (§12).

**Warnings:**
- **W-V9-RANKING-GLOBAL** (informativo) — modo Global declarado
- **W-V9-RANKING-SEGMENTADO** (informativo) — modo Segmentado declarado com Agrupador ativo
- **W-V9-SEG-SEM-AGRUPADOR** (bloqueio) — modo Segmentado declarado sem Agrupador

### 4.3 Ordem canônica de cálculo · blindagem contra dupla agregação

Armadilha estrutural central da V9 é **dupla agregação** amplificada pela multidimensionalidade — ordenar sobre linhas brutas (sem consolidar Identificador) corrompe o ranking de todas as métricas simultâneas e o score consolidado inteiro.

**Exemplo:** Identificador A aparece em 3 linhas: `Faturamento=[100, 200, 300]`, `Margem=[0.1, 0.2, 0.3]`. Caminho correto (Modo Transacional): consolidar primeiro → `Faturamento=600` (Soma), `Margem=0.2` (Média) → ordenar e posicionar depois. Caminho errado: ordenar sobre linhas brutas → Identificador A "aparece" 3 vezes no ranking, corrompendo posições de todos os outros elementos.

Blindagem é mais crítica em V9 que em V7 porque ranking cross-elementos em universo único amplifica o estrago (em V7, dupla agregação só corrompe o grupo afetado).

Contrato formal em **4 passos canônicos** (§5.2 detalha):

1. **Consolidação da unidade analítica** via T-AGRUPA com regra de agregação declarada por métrica
2. **Ordenação por métrica** respeitando Direção declarada
3. **Atribuição de Posição por métrica** (rank mínimo)
4. **Score Consolidado · Variação Máxima · Classificação**

Nenhum passo pode ser pulado ou reordenado. Implementação na Fundação (F-MOT) precisa blindar em teste unitário que linhas brutas nunca entram no Passo 2.

### 4.4 Direção por métrica (sem default · declaração obrigatória)

Cada métrica tem **Direção obrigatória declarada pelo usuário** em E3. Dois valores oficiais: **Maior-é-melhor** (ordem decrescente na ordenação) · **Menor-é-melhor** (ordem crescente).

**Sem default pré-definido.** Quebra do padrão "default declarado" que se aplicou em T-04 (modo da base, regra de agregação) e T-06 (escalas) e T-10 (thresholds). Justificativa: **Direção é a única decisão em V9 cujo erro inverte o resultado analítico**, não apenas distorce margens. Errar a tolerância em V7 por 1% dá leitura parecida; errar a Direção em V9 produz **ranking 100% invertido** — Líder vira Retaguarda.

E3 apresenta cada métrica com seletor de Direção **em branco** e exige seleção antes de avançar para E4. Sem detecção automática por nome da métrica (rejeitada pelos mesmos motivos de V7 D-087 — "tempo médio de atendimento" menor-é-melhor × "tempo de vida útil" maior-é-melhor; padrão de nome não resolve com confiança).

**Tensão com C.5 reconhecida:** declaração obrigatória é fricção UX. Alternativa "default Maior-é-melhor" seria mais amigável mas embute decisão silenciosa do sistema em 50% dos casos. Escolha pela fricção é aplicação estrita de C.5 — em V9, a gravidade da inversão justifica o custo UX.

**Warnings:**
- **W-V9-DIRECAO-FALTANDO** (bloqueio) — bloqueia avanço de E3 se qualquer métrica está sem Direção declarada
- **W-V9-DIRECAO-DECLARADA** (informativo) — registra a configuração de Direção por métrica

### 4.5 Nome analítico por métrica (default declarado editável)

Cada métrica tem campo `nome_analitico` que default é o nome da coluna na base, editável em E3. Aplica padrão V7 D-082. Visível em E3 ao lado do seletor de Direção (mesma linha).

**Warnings:**
- **W-V9-NOME-DEFAULT** (informativo) — nome analítico aceito da coluna original
- **W-V9-NOME-CUSTOM** (informativo) — pelo menos 1 nome editado

### 4.6 Semântica da métrica (T-SEMA · sétima consumidora · contrato distinto vs V7)

V9 é **sétima consumidora de T-SEMA** (depois de V2, V3, V7) com contrato distinto das anteriores.

**Distinção estrutural vs V7 (D-087):** V7 tem T-SEMA **global com efeito apenas visual** (cálculo é simétrico, independente de semântica). V9 tem T-SEMA **por métrica com efeito direto no cálculo** — a Direção declarada determina a ordem de ordenação (decrescente × crescente), que determina a Posição, que determina o Score e a Classificação. Em V9, T-SEMA **é parâmetro estrutural do cálculo**, não camada visual sobre cálculo simétrico.

Esta divergência é aplicação direta do padrão **"herança adaptada à natureza analítica"** (D-073): V7 tem 1 medida e direção pode ser abstraída do cálculo; V9 tem 2-6 métricas e direção é **condição necessária** para ordenar cada uma. Natureza analítica distinta → contrato distinto justificado.

**Quadro comparativo de consumo T-SEMA:**

| Visão | Escopo | Efeito no cálculo | Default |
|---|---|---|---|
| V2 | Global (1 medida) | Afeta interpretação (direção de variação entre estados) | Neutro |
| V3 | Global (1 medida) | Afeta interpretação (direção de evolução no eixo) | Neutro |
| V7 | Global (1 medida) | **Não afeta cálculo** — apenas visualização e ordem de apresentação | Neutro |
| **V9** | **Por métrica (2-6)** | **Afeta cálculo** — determina ordem de ordenação de cada métrica | **Sem default · obrigatório** |

**Efeito visual em V9 permanece:**
- Posição 1 destacada como "líder daquela métrica" independentemente da direção (mapeamento visual coerente em ambas as direções)
- Coluna da métrica na saída mostra ícone indicando Direção declarada (↑ Maior-é-melhor · ↓ Menor-é-melhor) — detalhe final em S-V9

**Persistência em T-MODELO:** Direção por métrica persiste no modelo como par Métrica↔Direção. Ao aplicar modelo em nova base, motor procura métricas por nome; se não encontrada, **W-V9-MODELO-METRICA-AUSENTE** (alerta) pede seleção manual.

### 4.7 Regra de agregação (T-AGRUPA · sétima consumidora · regra por métrica)

V9 consome T-AGRUPA com **regra de agregação declarada independentemente por métrica**. Padrão herdado V7 D-082 adaptado: em V7 há 1 medida, 1 regra; em V9 há 2-6 métricas, cada uma com regra própria.

**5 regras oficiais:**

| Regra | Dispensa métrica? | Default por tipo |
|---|---|---|
| **Soma** | Não | Aditiva |
| **Média** | Não | Não-aditiva · Relativa |
| **Máximo** | Não | — (usuário declara) |
| **Mínimo** | Não | — (usuário declara) |
| **Contagem** | Sim | — (caso especial, análogo V7 §4.7) |

**Default declarado por métrica na amostragem** (herança V7 D-082 adaptada): motor detecta tipo da métrica (Aditiva · Não-aditiva · Relativa — taxonomia D-025) e propõe regra default em E3; usuário confirma ou edita cada uma independentemente.

**Contrato T-AGRUPA V9 (extensão do contrato existente):** aceita dicionário `{metrica: regra}` em vez de regra única (extensão do contrato D-082). F-TRANS (Fundação) absorve a extensão.

**Warnings:**
- **W-V9-AGREG-DEFAULT** (informativo) — regras de agregação aceitas como default em todas as métricas
- **W-V9-AGREG-CUSTOM** (informativo) — pelo menos uma regra editada pelo usuário

### 4.8 Limites operacionais das métricas

Escala em 5 patamares:

| N Métricas | Comportamento | Warning |
|---|---|---|
| 0-1 | **Bloqueio estrutural** — V9 não pode operar sem multidimensionalidade | W-V9-METRICAS-INSUFICIENTES |
| 2 | Executa com alerta · Variação Máxima com interpretação reduzida | W-V9-METRICAS-MIN |
| 3-6 | Normal | — |
| 7-10 | Alerta forte · confirmação recomendada | W-V9-METRICAS-EXCESSO-AVISO |
| 11+ | **Bloqueio** | W-V9-METRICAS-INVIAVEL |

Patamar "2 com alerta" respeita mínimo matemático mas sinaliza limitação; patamar "11+ bloqueio" é limite operacional (tela ilegível, score disperso).

### 4.9 Escalas heterogêneas entre métricas · V9 não normaliza

**V9 não normaliza valores de métrica em nenhuma hipótese.** Escalas heterogêneas entre métricas (ex: Faturamento em R$ de milhões, Taxa de Conversão em decimais, Tempo Médio em minutos) são **neutralizadas pela natureza ordinal da Posição** — o substrato do score consolidado é a Posição, não o valor. Duas métricas de escalas completamente diferentes contribuem igualmente para o score porque o que entra no cálculo é a Posição do elemento em cada uma, não o valor. Esta posição respeita C.5: sistema não toma decisão de transformação de escala sobre o dado do usuário; escalas permanecem exatamente como recebidas, e a visão se adapta ao dado recebido.

**Alternativas avaliadas e rejeitadas no MVP:**

| Alternativa | Por que foi rejeitada | P-V9-XX-Evo |
|---|---|---|
| Z-score por métrica | Pressupõe distribuição normal; decide silenciosamente transformar o dado; posições ordinais já neutralizam escalas | P-V9-03-Evo |
| Min-max [0,1] | Elimina invariância a outliers; transformação silenciosa contra C.5 | P-V9-04-Evo |
| Log-scale | Pressupõe distribuição log-normal; não aplicável a métricas zero ou negativas | P-V9-05-Evo |
| Ranking padronizado (Posição/N) | Transformação monotônica; adiciona complexidade sem ganho | P-V9-06-Evo |
| Score composto ponderado sobre valores normalizados | Descaracteriza V9 — vira outra visão (convergente a V4 Modo 3) | Fora de escopo V9 (candidato a nova visão) |

**Warning de heterogeneidade detectada:** motor aplica teste de razão de amplitude — detecta heterogeneidade quando `max(amplitude_por_metrica) / min(amplitude_por_metrica) > 1000` (3 ordens de grandeza). Threshold 1.000× é generoso e editável em "Configurações avançadas" de E3.

- **W-V9-ESCALAS-HETEROGENEAS** (informativo) — detectada diferença ≥ 1.000× entre amplitudes de métricas; lembra usuário que score é por posição

### 4.10 Pesos por métrica · fora de escopo MVP

A V9 não aplica pesos por métrica no score consolidado nesta versão. Todas as métricas têm o mesmo peso (equal-weighted) por arquitetura. Pesos por métrica ficam registrados em **P-V9-01-Evo** para evolução futura, com análise cuidadosa para não borrar fronteira V9 × V4 Modo 3. Peso automático seria decisão silenciosa do sistema (viola C.5); peso manual declarado é sub-caso de "score composto ponderado" — nova visão futura, não extensão de V9.

### 4.11 Modelo de configuração (T-MODELO)

V9 consome T-MODELO como todas as 11 visões (CONTEXT §13.3).

**Persiste:** Identificador, lista de Métricas ativas (nome analítico + Direção + regra de agregação), Modo da base, Modo de Ranking, Agrupador ativo (se Segmentado), thresholds customizados (Líder, Retaguarda, Especialista, leitura qualitativa).

**Não persiste:** dado fonte, resultado do cálculo.

**Aplicação em nova base:** métricas mapeadas por nome; se não encontradas, **W-V9-MODELO-METRICA-AUSENTE** (alerta) pede seleção manual. Aplicação em visão específica (não cross-visão) — V9 não forma par de view especializada com nenhuma outra visão.

---

## 5. Lógica de processamento

### 5.1 Requisitos mínimos e alertas

**Requisitos mínimos (bloqueios):**
- 1 campo categórico elegível como Identificador
- 2 métricas numéricas válidas
- Direção declarada em todas as métricas
- 2 Identificadores válidos no conjunto analisado (após consolidação)

**Mínimos recomendados (alertas):**
- 5 Identificadores para leitura de ranking estável
- 3 métricas para leitura multidimensional robusta

**Alertas não bloqueantes:**
- Identificador com duplicidade (tratada por consolidação T-AGRUPA)
- Métrica com nulos parciais
- Métrica zerada em todos os registros
- Alta cardinalidade de agrupadores no modo Segmentado
- Grupos com poucos elementos no modo Segmentado
- Métricas com escalas muito diferentes

### 5.2 Ordem canônica de cálculo (4 passos)

Implementação na Fundação deve respeitar rigorosamente:

**Passo 1 · Consolidação da unidade analítica (T-AGRUPA)**
- Entrada: base analítica normalizada
- Operação: agrupar pela unidade analítica (Identificador OU Identificador+Agrupador); aplicar regra de agregação declarada por métrica
- Saída: base consolidada com 1 linha por unidade analítica — `valor_consolidado_por_metrica[]`

**Passo 2 · Ordenação por métrica**
- Entrada: base consolidada do Passo 1
- Operação: para cada métrica, ordenar pelos valores consolidados respeitando Direção (Maior-é-melhor → decrescente; Menor-é-melhor → crescente)
- Saída: sequência ordenada de unidades analíticas por métrica

**Passo 3 · Atribuição de Posição por métrica (rank mínimo)**
- Entrada: sequência ordenada do Passo 2
- Operação: atribuir Posição usando rank mínimo — elementos empatados em valor consolidado recebem mesma Posição (a menor disponível)
- Saída: base enriquecida com `posicao_por_metrica`

**Passo 4 · Score Consolidado · Variação Máxima · Classificação**
- Entrada: base enriquecida do Passo 3 + Direção × tolerâncias de classificação
- Operação: calcular Score Consolidado, Melhor/Pior Posição, Variação Máxima de Posição; classificar unidade analítica em Líder/Especialista/Equilibrado/Retaguarda respeitando prioridade
- Saída: V9Result completo

Ordem preserva consistência entre motor, tela e Excel. Nenhum passo pode ser pulado ou reordenado.

### 5.3 Score Consolidado (média aritmética simples das posições válidas)

**Score Consolidado = média aritmética simples das Posições por Métrica.** Para cada Identificador:

```
score_consolidado = soma(posicao_por_metrica_valida) / N_metricas_validas
```

Quanto **menor** o score, **melhor** o posicionamento geral. Equal-weighted é arquitetura da visão: qualquer ponderação embute decisão sobre o dado do usuário (viola C.5) ou descaracteriza V9 como visão autônoma.

**Alternativas avaliadas e rejeitadas no MVP:**

| Alternativa | Por que foi rejeitada | Candidato |
|---|---|---|
| Soma das posições | Matematicamente idêntica à média × N fixo; menos interpretável | Fora de P-V9 (equivalente) |
| Mediana das posições | Descarta extremos; distorce sinal de especialização | Nova visão futura |
| Média geométrica | Penaliza desproporcionalmente posições ruins; complexidade sem ganho | P-V9-0X-Evo |
| Média ponderada | Embute hierarquia entre métricas — viola C.5 | P-V9-01-Evo |

**Tratamento de nulos em 2 camadas (herança V7 D-085 adaptada via D-073):**

| Cenário | Tratamento | Classificação final | Warning |
|---|---|---|---|
| Valor em todas N métricas | Score normal sobre N | Elegível: 4 classes | — |
| Valor em K de N métricas (K ≥ 1) | **Score parcial sobre K** · elemento permanece no ranking | Elegível: 4 classes | W-V9-METRICA-PARCIAL (alerta) |
| 0 valores válidos nas N métricas | Sem score, sem posições | **NULO_MEDIDA** | W-V9-ELEMENTO-NULO (alerta forte) |
| Métrica 100% nula | Bloqueio em E3 · usuário remove ou cancela | — | W-V9-METRICA-TOTAL-NULA (bloqueio) |
| Métrica 100% zerada | Prossegue · não discrimina (todos Pos 1) | Classificações válidas | W-V9-METRICA-ZERADA (alerta forte) |

**Divergência vs V7 justificada (D-073):** V7 tem 1 medida (nulo nela = NULO_MEDIDA binário); V9 tem 2-6 métricas (nulo em K parciais ainda permite score sobre K válidas). Herança adaptada à natureza analítica.

**Caveat declarado ao usuário:** score parcial é **menos comparável** a score completo. Elemento com menos métricas válidas tem menos "sinal multidimensional". W-V9-METRICA-PARCIAL expõe o fato; interpretação é do usuário.

### 5.4 Regra de empate de Posição (rank mínimo) + desempate visual (4 níveis)

**Posição por Métrica usa rank mínimo.** Para cada métrica, elementos com mesmo valor consolidado recebem **mesma Posição** — a menor disponível. Elementos subsequentes recebem rank continuando a partir de `(quantidade_de_elementos_anteriores + 1)` — não do rank do empate. Equivalente ao método `RANK()` em SQL padrão e `pandas.Series.rank(method='min')`.

**Exemplo.** Conjunto de 6 elementos em métrica Faturamento (Maior-é-melhor):

| Elemento | Faturamento | Posição |
|---|---|---|
| A | 500 | 1 |
| B | 500 | 1 |
| C | 500 | 1 |
| D | 400 | 4 |
| E | 300 | 5 |
| F | 200 | 6 |

A, B, C empatam → todos recebem Pos 1. D recebe Pos 4 (não Pos 2), refletindo 3 elementos à frente. Total de posições = N elementos mesmo com empate no topo. Empate é **preservado como fato analítico**, não desempatado artificialmente.

**Desempate visual determinístico em 4 níveis** (para ordenação de linhas na saída Excel e tela — não afeta classificação):

1. **Score Consolidado crescente** (menor = primeiro na ordem visual = melhor posicionamento)
2. **Variação Máxima de Posição crescente** (elemento mais equilibrado primeiro quando scores empatam)
3. **Nome do Identificador alfabético** case-insensitive
4. **Ordem de inserção original**

Tolerância floating point: 1e-9 (herança D-041 · D-088).

**V9 é sétima consumidora de T-RANK** com regra V9-específica em 4 níveis. Extensão do contrato D-041: enum `escopo` ganha novo valor `cross_elementos_dentro_do_agrupador` para modo Segmentado — distinto de `intra_grupo` de V7 e `global` de V4/V10.

**Empate no score consolidado não é desempatado para classificação** — dois elementos com mesmo score podem **ambos** ser Líderes (se caem no top 20%). Desempate é puramente cosmético para ordenação visual.

**Warning:**
- **W-V9-RANK-EMPATE** (informativo) — registra ocorrência de empate no Passo 3 ou no score

### 5.5 Variação Máxima de Posição (indicador de especialização × equilíbrio)

**Variação Máxima de Posição** é a amplitude ordinal das posições de um Identificador através de suas métricas válidas:

```
variacao_maxima = max(posicao_por_metrica_valida) − min(posicao_por_metrica_valida)
```

Unidade: número inteiro positivo (ou zero).

**Interpretação ordinal:**
- **Variação = 0** — elemento com mesma posição em todas as métricas válidas · perfil perfeitamente equilibrado (sinal matemático forte)
- **Variação baixa** (em relação ao tamanho do conjunto) — perfil equilibrado
- **Variação alta** — perfil especialista (líder numa, retaguarda noutra)

Interpretação de "alta × baixa" é **relativa ao tamanho do conjunto**, não ao número de métricas: em conjunto de 100, variação 30 é moderada; em conjunto de 10, variação máxima possível é 9. Por isso threshold Especialista (§5.6) é percentual do total, não valor absoluto.

**Alternativas avaliadas e rejeitadas:**

| Alternativa | Por que foi rejeitada | Candidato |
|---|---|---|
| Desvio padrão das posições | Pressupõe distribuição; σ frágil com N pequeno (2-6); menos interpretável | P-V9-0X-Evo |
| Amplitude normalizada ((pior−melhor)/(N−1)) | Perde grão interpretativo; threshold Especialista já normaliza | P-V9-0X-Evo (baixa) |
| Coeficiente de variação | Numericamente ruim com médias baixas; interpretação confusa | Não candidato |
| Diferença pior − mediana | Descarta lado "bom"; perde simetria | P-V9-0X-Evo |

**Casos-limite:**

| Caso | Variação | Tratamento | Warning |
|---|---|---|---|
| N = 2 elementos | Máximo = 1 | Executa com alerta forte; leitura limitada | W-V9-CONJUNTO-PEQUENO (alerta forte) |
| Conjunto homogêneo (todos empatados em todas métricas) | 0 para todos | Todos Equilibrados | W-V9-CONJUNTO-HOMOGENEO (informativo) |
| Elemento com K = 1 métrica válida | 0 (falso equilíbrio) | **Não elegível a Especialista** · elegível Líder/Retaguarda/Equilibrado | W-V9-METRICA-PARCIAL (já em §5.3) |
| Elemento NULO_MEDIDA | Indefinida | Não entra em ranking | W-V9-ELEMENTO-NULO (já em §5.3) |

**Threshold Especialista (default declarado editável):**

Especialista = Identificador com `Variação Máxima ≥ 50% × N_elementos_validos_do_conjunto_analisado`, desde que não já Líder ou Retaguarda.

- Default **50%** declarado, editável em "Configurações avançadas" (`threshold_especialista_pct`)
- Faixa aceitável: 30% (Especialista mais sensível) a 70% (Especialista mais raro)
- Rationale 50%: meio do conjunto é ponto de corte simétrico e interpretável ("variação atravessa metade do ranking")
- Modo Segmentado: threshold calculado por agrupador

**Warnings:**
- **W-V9-THRESHOLD-ESPECIALISTA-DEFAULT** (informativo) — 50% aceito
- **W-V9-THRESHOLD-ESPECIALISTA-CUSTOM** (informativo) — editado

### 5.6 Taxonomia oficial V9 (4 classes primárias + NULO_MEDIDA + 5 leituras qualitativas de conjunto)

**Camada 1 · Classes primárias (4 mutuamente exclusivas, aplicadas por prioridade declarada):**

| # | Classe | Condição |
|---|---|---|
| 1 | **Líder** | `score_consolidado ≤ percentil_20` do conjunto analisado (top 20%) |
| 2 | **Retaguarda** | `score_consolidado ≥ percentil_80` (bottom 20%) |
| 3 | **Especialista** | `variacao_maxima_posicao ≥ 50% × N_elementos_validos`, desde que não já Líder ou Retaguarda |
| 4 | **Equilibrado** | Residual — elemento não classificado em 1, 2 ou 3 |

**Prioridade:** Líder → Retaguarda → Especialista → Equilibrado. Rationale: Líder e Retaguarda são leituras executivas primárias (extremos do score); Especialista é leitura secundária para elementos do meio com alta dispersão de posições; Equilibrado é residual estável.

**Camada 2 · Classificação especial paralela:**

| Classe especial | Condição |
|---|---|
| **NULO_MEDIDA** | Elemento com 0 métricas válidas (§5.3 Camada 2) |

Elemento NULO_MEDIDA não recebe classe primária. V9Result preserva campos nulos; aba Ranking Completo mostra "—" na coluna Classificação. NULO_MEDIDA **não entra** no cálculo dos percentis 20/80 (conjunto analisado = conjunto - NULO_MEDIDA).

**Critérios percentuais · default declarado editável:**

| Threshold | Default | Faixa aceitável | Parâmetro |
|---|---|---|---|
| Líder (top %) | 20% | 5%-40% | `threshold_lider_pct` |
| Retaguarda (bottom %) | 20% | 5%-40% | `threshold_retaguarda_pct` |
| Especialista (% da variação) | 50% | 30%-70% | `threshold_especialista_pct` |

**Constraint operacional:** `threshold_lider_pct + threshold_retaguarda_pct ≤ 90%` (garante pelo menos 10% para Equilibrado/Especialista). Violação → **W-V9-THRESHOLDS-INVALIDOS** (bloqueio em E3).

**Caso-limite · conjunto com N < 5 elementos válidos:**

| N válidos | Tratamento | Warning |
|---|---|---|
| N < 2 | **Bloqueio estrutural** | W-V9-ELEMENTOS-INSUFICIENTES |
| 2 ≤ N ≤ 4 | Executa com alerta forte; arredondamento `ceil` nos thresholds para garantir pelo menos 1 Líder e 1 Retaguarda | W-V9-CONJUNTO-PEQUENO |
| N ≥ 5 | Normal | — |

Arredondamento canônico `ceil` (documentado; determinístico C.1).

**Caso-limite · empates múltiplos no score no ponto de corte percentual:**

Se elemento na fronteira do corte tem score empatado com elemento imediatamente posterior, **ambos entram na mesma classe** (expansão por empate). Justificativa C.5: cortar arbitrariamente entre equivalentes matemáticos embute decisão.

**Implicação:** classes podem ter mais elementos que o threshold declarado.

- **W-V9-CLASSE-EXPANDIDA-POR-EMPATE** (informativo) — registra expansão

**Camada 3 · Leitura qualitativa do conjunto (Resumo Executivo Bloco 5, não estrutural no V9Result):**

| Leitura | Condição default | Métrica-base |
|---|---|---|
| **Conjunto Homogêneo** | ≥ 70% dos elementos são Equilibrados | % Equilibrados |
| **Conjunto Concentrado** | N Líderes + N Retaguarda ≥ 50% do conjunto | Polarização por score |
| **Conjunto Especializado** | ≥ 30% dos elementos são Especialistas | % Especialistas |
| **Conjunto Misto** | Nenhuma das acima | Residual |
| **Conjunto Degenerado** | N < 5 elementos válidos OU ≥ 30% de NULO_MEDIDA | Estrutural |

Thresholds editáveis (`threshold_homogeneo_pct` · `threshold_concentrado_pct` · `threshold_especializado_pct` · `threshold_degenerado_nulos_pct`).

**Ordem de teste:** Degenerado → Especializado → Concentrado → Homogêneo → Misto.

**Warnings:**
- **W-V9-LEITURA-DEFAULT** (informativo) — defaults aceitos
- **W-V9-LEITURA-CUSTOM** (informativo) — editados

### 5.7 Resumo Executivo (6 blocos · padrão D-044)

**Bloco 1 · Cabeçalho**
Nome da visão · base analisada (arquivo + aba) · Identificador · Métricas ativas (lista com Direção por métrica) · Regra de agregação por métrica · Modo de Ranking · Agrupador ativo (quando Segmentado) · Modo da base · Thresholds ativos · N Identificadores analisados · N Métricas · data/hora.

**Bloco 2 · Números-âncora**
- N Total Identificadores · N NULO_MEDIDA · N Válidos (base dos thresholds)
- N Líderes · N Especialistas · N Equilibrados · N Retaguarda
- Melhor Score Consolidado (Identificador + valor) · Pior Score Consolidado
- Maior Variação Máxima de Posição (Identificador + valor) · Menor Variação entre elementos com K = N métricas válidas

**Bloco 3 · Distribuição das 4 classes primárias**
Contagem e % por classe primária + NULO_MEDIDA. No modo Segmentado: breakdown por agrupador quando N_agrupadores ≤ 10; quando > 10, breakdown apenas para top 5 agrupadores com mais Identificadores.

**Bloco 4 · Elementos destacados**
- Top 5 Líderes (score crescente)
- Top 5 Retaguarda (score decrescente)
- Top 3 Especialistas (variação máxima decrescente)
- Top 3 Equilibrados (variação máxima crescente · entre elementos com K = N métricas)
- Para cada métrica ativa: Top 3 Identificadores com Pos 1 (todos empatados em Pos 1 aparecem)

Rótulos descritivos neutros (padrão V7 D-087): "Top 5 elementos com menor score consolidado" em vez de "Top 5 líderes de performance".

**Bloco 5 · Leitura qualitativa do conjunto + síntese agregada + nota de redirecionamento**

*Parte 5A · Leitura qualitativa* — classificação única do conjunto em uma das 5 leituras (§5.6 Camada 3). Modo Segmentado: 1 leitura por agrupador.

*Parte 5B · Síntese narrativa* — texto consolidando a distribuição. Exemplo: *"Dos 40 Identificadores analisados: 8 são Líderes (20%), 8 são Retaguarda (20%), 12 são Especialistas (30%) e 12 são Equilibrados (30%). Conjunto classificado como Especializado — especialização é traço dominante."*

*Parte 5C · Thresholds ativos* — *"Thresholds: Líder ≤ top 20% · Retaguarda ≥ bottom 20% · Especialista com Variação ≥ 50% do conjunto · [Default / Customizado]"*.

*Parte 5D · Nota estática final de redirecionamento:*

> *"Para análise de dispersão estatística interna de uma métrica individual (IQR, outliers, distribuição), considere V5 · Comportamento e Dispersão. Para análise de desvio intra-grupo em uma única medida contra a média do grupo, considere V7 · Desvio em Relação à Média do Grupo. Para análise de participação de elementos no total com comparação de distribuição entre medidas, considere V4 · Composição e Participação."*

Nota aparece **apenas no Resumo Executivo Bloco 5 Parte 5D**, nunca em interface operacional durante configuração.

**Bloco 6 · Qualidade estrutural**
N ajustes leves · N alertas · N Identificadores NULO_MEDIDA · N Identificadores com score parcial (K < N) · decomposição por cobertura (K=1, K=2, ... K=N−1) · N métricas com todos valores zerados · N métricas 100% nulas (bloqueadas em E3) · modo declarado · regra de agregação por métrica · thresholds customizados · detecção de escalas heterogêneas.

### 5.8 Exportação Excel (6 abas oficiais)

| # | Aba | Conteúdo |
|---|---|---|
| 1 | **Resumo Executivo** | 6 blocos do §5.7 |
| 2 | **Ranking Completo** | 1 linha por Identificador: Identificador · Agrupador (se Segmentado) · valor consolidado por métrica · Posição por métrica · Melhor/Pior Posição · Variação Máxima · Score Consolidado · Classificação |
| 3 | **Perfil por Métrica** | Aba única com blocos empilhados (1 por métrica) mostrando ranking naquela métrica (Identificador · valor · Posição · Direção declarada) |
| 4 | **Mapa de Perfil** ⭐ | Matriz Identificador × Métrica com valor = Posição · cor de direção (T-SEMA) · destaque de Pos 1 e Pior Posição · coluna Classificação |
| 5 | **Parâmetros** | Configuração declarada vs efetiva completa |
| 6 | **Diagnóstico** | Todos warnings + categoria T-DIAG + linhas originais vs consolidadas + lista de NULO_MEDIDA · score parcial · métricas zeradas/nulas · heterogeneidade |

**Mapa de Perfil é o coração visual V9** — análogo a Matriz de Presença V8 (D-077) e Mapa de Grupos V7 (D-089). Matriz Identificador × Métrica com cores de direção e destaques transforma leitura multidimensional em leitura visual imediata: linhas predominantemente verdes (Maior-é-melhor bem posicionado · Menor-é-melhor bem posicionado mostrado coerentemente) = Líderes; linhas predominantemente vermelhas = Retaguarda; linhas com forte variação de cor = Especialistas.

**Aba Dados Brutos do prévio descartada** (herança V8 D-078 · V7 D-089) — aba Ranking Completo cobre auditoria analítica; Diagnóstico registra "linhas originais vs consolidadas" para rastreabilidade.

**Diagnóstico sempre última aba** (D-017 ratificado).

**Filtros ativos em todas as 6 abas.** Tela e Excel não divergem.

### 5.9 Nota estática final — redirecionamento declarativo

Ver §5.7 Bloco 5 Parte 5D. Redirecionamentos únicos na execução V9, exibidos apenas no Resumo Executivo. Nenhum redirecionamento em configuração (E1-E5) ou outras abas.

---

## 6. Contrato V9Result (síntese)

```
V9Result:
  elementos[]:  # 1 linha por unidade analítica
    identificador: str
    agrupador: str | None  # None no modo Global
    valor_consolidado_por_metrica: dict[str, float | None]  # nome da métrica → valor
    posicao_por_metrica: dict[str, int | None]  # None quando métrica nula para este elemento
    melhor_posicao: int | None
    pior_posicao: int | None
    variacao_maxima_posicao: int | None
    score_consolidado: float | None
    n_metricas_validas: int  # 0 quando NULO_MEDIDA
    classificacao: enum [Lider, Especialista, Equilibrado, Retaguarda, Nulo_Medida]
  conjuntos[]:  # 1 entrada por conjunto analisado (1 no Global · N no Segmentado)
    agrupador: str | None
    n_identificadores_total: int
    n_identificadores_validos: int
    n_nulo_medida: int
    n_lider: int
    n_especialista: int
    n_equilibrado: int
    n_retaguarda: int
    thresholds_ativos: dict
    leitura_conjunto: enum [Homogeneo, Concentrado, Especializado, Misto, Degenerado]
    classe_expandida_por_empate: bool
  sintese:
    n_conjuntos: int  # 1 no Global; N no Segmentado
    distribuicao_leituras: dict
    heterogeneidade_escalas_detectada: bool
  parametros_execucao:
    identificador: str  # campo declarado
    metricas: list[{nome_analitico: str, campo_fonte: str, direcao: enum [Maior_Melhor, Menor_Melhor], regra_agregacao: enum [Soma, Media, Maximo, Minimo, Contagem], tipo_medida: enum}]
    modo_base: enum [Transacional, Pre_Agregado]
    modo_ranking: enum [Global, Segmentado]
    agrupador: str | None
    thresholds: dict  # lider_pct, retaguarda_pct, especialista_pct
    thresholds_leitura: dict  # homogeneo_pct, concentrado_pct, especializado_pct, degenerado_nulos_pct
    threshold_escalas_heterogeneas: float  # default 1000
  diagnostico:
    warnings: list
    ajustes_leves: list
    decisoes_usuario: list
    linhas_originais: int
    linhas_consolidadas: int
```

---

## 7. Bloqueios operacionais (12 estruturais)

| # | Condição | Warning |
|---|---|---|
| 1 | Arquivo ilegível ou corrompido | W-V9-ARQUIVO-INVALIDO |
| 2 | Estrutura inválida (arquivo vazio, aba sem dado, sem coluna numérica para métricas) | W-V9-ESTRUTURA-INVALIDA |
| 3 | Nenhum campo categórico elegível como Identificador | W-V9-SEM-IDENTIFICADOR |
| 4 | Menos de 2 métricas numéricas elegíveis | W-V9-METRICAS-INSUFICIENTES |
| 5 | Pelo menos 1 métrica com Direção não declarada ao entrar em E4 | W-V9-DIRECAO-FALTANDO |
| 6 | Pelo menos 1 métrica com 100% valores nulos (sem decisão em E3) | W-V9-METRICA-TOTAL-NULA |
| 7 | Modo de Ranking = Segmentado declarado sem Agrupador ativo | W-V9-SEG-SEM-AGRUPADOR |
| 8 | Modo da base = Pré-agregado declarado mas duplicatas detectadas | W-V9-MODO-VIOLACAO |
| 9 | Menos de 2 Identificadores válidos no conjunto analisado | W-V9-ELEMENTOS-INSUFICIENTES |
| 10 | Thresholds Líder + Retaguarda > 90% do conjunto | W-V9-THRESHOLDS-INVALIDOS |
| 11 | Mais de 10 métricas ativas | W-V9-METRICAS-INVIAVEL |
| 12 | Total de Identificadores > 1.000.000 (limite físico Excel) | W-V9-VOLUME-INVIAVEL |

---

## 8. Escala de cardinalidade V9 (3 eixos multi-dimensionais)

V9 tem natureza **multi-eixo independente** (Identificadores, Métricas, Agrupadores são recortes ortogonais do dado) — distinta de V7 (hierárquica-aditiva) e V8 (matricial multiplicativa). Escala adaptada (padrão D-073).

### 8.1 Eixo 1 · Cardinalidade do Identificador (N Identificadores válidos)

| Patamar | Comportamento | Warning |
|---|---|---|
| N < 2 | **Bloqueio** | W-V9-ELEMENTOS-INSUFICIENTES (#9) |
| 2 ≤ N ≤ 4 | Alerta forte · leitura limitada | W-V9-CONJUNTO-PEQUENO |
| 5-50 | Normal | — |
| 51-500 | Aviso informativo | W-V9-IDENTIFICADORES-MUITOS-AVISO |
| 501-10.000 | Alerta · confirmação recomendada | W-V9-IDENTIFICADORES-MUITOS-ALERTA |
| 10.001-100.000 | Alerta forte · confirmação obrigatória | W-V9-IDENTIFICADORES-CRITICO |
| 100.001-1.000.000 | Alerta forte · performance degradada | W-V9-IDENTIFICADORES-EXTREMO |
| 1.000.001+ | **Bloqueio** | W-V9-VOLUME-INVIAVEL (#12) |

### 8.2 Eixo 2 · N Métricas ativas (ratificado de §4.8)

| Patamar | Comportamento | Warning |
|---|---|---|
| 0-1 | Bloqueio | W-V9-METRICAS-INSUFICIENTES |
| 2 | Alerta | W-V9-METRICAS-MIN |
| 3-6 | Normal | — |
| 7-10 | Alerta forte | W-V9-METRICAS-EXCESSO-AVISO |
| 11+ | Bloqueio | W-V9-METRICAS-INVIAVEL |

### 8.3 Eixo 3 · Cardinalidade do Agrupador (modo Segmentado)

MVP permite 1 Agrupador ativo máximo. Cardinalidade = N valores únicos do agrupador:

| Patamar | Comportamento | Warning |
|---|---|---|
| 1-20 | Normal | — |
| 21-100 | Aviso informativo · muitos grupos separados | W-V9-AGRUPADOR-MUITOS-AVISO |
| 101-500 | Alerta · confirmação recomendada · sugere revisar escopo | W-V9-AGRUPADOR-MUITOS-ALERTA |
| 501+ | Alerta forte · cada grupo com poucos Identificadores; leitura degradada | W-V9-AGRUPADOR-CRITICO |

Não bloqueia por cardinalidade de Agrupador — cada grupo produz sua própria leitura.

### 8.4 Diretrizes de performance (9 diretrizes)

**Herdadas de V3/V8/V7 (7):**
1. Pré-validação de volume antes de alocação pesada
2. Índices hash para consolidação T-AGRUPA (grouping sem sort global)
3. Filtro de casos estruturalmente inválidos cedo (NULO_MEDIDA removidos antes de thresholds)
4. Cálculo em memória com estruturas colunares
5. Ordenação estável determinística (tolerância 1e-9)
6. Diagnóstico em streaming
7. Geração Excel com openpyxl em modo otimizado quando volume > 100.000 linhas

**Específicas V9 (2 novas):**
8. **Ordenação por métrica em paralelo** — as N ordenações (uma por métrica) são independentes; paralelização futura via multiprocessing ou Polars lazy
9. **Matriz pivotada Identificador × Métrica gerada em passe único** — aba Mapa de Perfil gerada diretamente da base consolidada sem pivot auxiliar pandas

---

## 9. Warnings catalogados (40)

### 9.1 Bloqueios (12 · §7)

W-V9-ARQUIVO-INVALIDO · W-V9-ESTRUTURA-INVALIDA · W-V9-SEM-IDENTIFICADOR · W-V9-METRICAS-INSUFICIENTES · W-V9-DIRECAO-FALTANDO · W-V9-METRICA-TOTAL-NULA · W-V9-SEG-SEM-AGRUPADOR · W-V9-MODO-VIOLACAO · W-V9-ELEMENTOS-INSUFICIENTES · W-V9-THRESHOLDS-INVALIDOS · W-V9-METRICAS-INVIAVEL · W-V9-VOLUME-INVIAVEL

### 9.2 Alertas (11)

**Alertas fortes (8):**
- W-V9-ELEMENTO-NULO — elemento com 0 métricas válidas (§5.3)
- W-V9-METRICA-ZERADA — métrica com 100% zeros; não discrimina (§5.3)
- W-V9-CONJUNTO-PEQUENO — N válidos 2-4 (§5.5)
- W-V9-IDENTIFICADORES-CRITICO — 10.001-100.000 (§8.1)
- W-V9-IDENTIFICADORES-EXTREMO — 100.001-1.000.000 (§8.1)
- W-V9-AGRUPADOR-CRITICO — 501+ grupos (§8.3)
- W-V9-METRICAS-EXCESSO-AVISO — 7-10 métricas (§4.8)
- W-V9-MODELO-METRICA-AUSENTE — campo não encontrado ao aplicar T-MODELO (§4.11)

**Alertas regulares (3):**
- W-V9-METRICA-PARCIAL — elemento com K < N métricas válidas (§5.3)
- W-V9-METRICAS-MIN — 2 métricas; Variação Máxima limitada (§4.8)
- W-V9-IDENTIFICADORES-MUITOS-ALERTA — 501-10.000 (§8.1)
- W-V9-AGRUPADOR-MUITOS-ALERTA — 101-500 grupos (§8.3)

### 9.3 Informativos (17)

- W-V9-MODO-TRANS-DEFAULT · W-V9-MODO-TRANS-CUSTOM · W-V9-MODO-PREAGG-DEFAULT · W-V9-MODO-PREAGG-CUSTOM (§4.1)
- W-V9-RANKING-GLOBAL · W-V9-RANKING-SEGMENTADO (§4.2)
- W-V9-DIRECAO-DECLARADA (§4.4)
- W-V9-NOME-DEFAULT · W-V9-NOME-CUSTOM (§4.5)
- W-V9-AGREG-DEFAULT · W-V9-AGREG-CUSTOM (§4.7)
- W-V9-ESCALAS-HETEROGENEAS (§4.9)
- W-V9-RANK-EMPATE (§5.4)
- W-V9-THRESHOLD-LIDER-DEFAULT · W-V9-THRESHOLD-LIDER-CUSTOM · W-V9-THRESHOLD-RETAGUARDA-DEFAULT · W-V9-THRESHOLD-RETAGUARDA-CUSTOM · W-V9-THRESHOLD-ESPECIALISTA-DEFAULT · W-V9-THRESHOLD-ESPECIALISTA-CUSTOM (§5.6)
- W-V9-LEITURA-DEFAULT · W-V9-LEITURA-CUSTOM (§5.6)
- W-V9-CLASSE-EXPANDIDA-POR-EMPATE (§5.6)
- W-V9-CONJUNTO-HOMOGENEO (§5.5)
- W-V9-IDENTIFICADORES-MUITOS-AVISO (§8.1)
- W-V9-AGRUPADOR-MUITOS-AVISO (§8.3)
- W-V9-SCORE-CALCULADO (informativo de execução normal)

---

## 10. Fronteira com Módulo 2 (TabloPrep)

V9 opera sobre base consolidada única. Operações de preparação que podem alimentar V9 ficam no domínio do Módulo 2 (TabloPrep):

- **Identificador composto** (múltiplos campos concatenados como chave única) — P-V9-07-Evo · consome T-CONCAT (D-053)
- **Empilhamento multi-aba** (dados em abas separadas por período/unidade) — M2.STACK candidata (D-063)
- **Normalização textual do Identificador** (padronização de nomes antes do grouping) — M2.NORMALIZE candidata (D-057)
- **Deduplicação prévia** (base Transacional com repetições estruturais) — operação M2 futura

V9 MVP não implementa essas operações. Microcopy em nota de seleção de aba orienta o usuário quando N ≥ 3 abas detectadas.

---

## 11. Pontos de atenção (riscos analíticos conhecidos)

**Dupla agregação amplificada.** Armadilha estrutural central. Em V9 a consequência é mais grave que V7 porque ranking cross-elementos corrompe todos os elementos (não apenas um grupo). §4.3 e §5.2 formalizam a ordem.

**Direção errada invertendo ranking.** Declaração obrigatória sem default é aplicação estrita de C.5 — §4.4 documenta a tensão UX × confiabilidade analítica.

**Score parcial sobre K < N métricas.** Elemento com cobertura menor tem score menos comparável. W-V9-METRICA-PARCIAL sinaliza; interpretação é do usuário. Elemento com K=1 válida não é elegível a Especialista (variação = 0 por construção, não por perfil real).

**Escalas heterogêneas × significado do score.** Posições ordinais neutralizam escalas no cálculo — elemento de Faturamento em milhões contribui igual a elemento de Taxa de Conversão em decimais para o score. W-V9-ESCALAS-HETEROGENEAS sinaliza quando amplitude > 1.000× entre métricas.

**Empates múltiplos em pontos de corte percentual.** Expansão por empate (§5.6) mantém equivalentes matemáticos na mesma classe — classes podem crescer além do threshold declarado. Caso extremo (muitos elementos empatados no topo) é raro mas possível.

**Interpretação de "Especialista" vs "Líder".** Especialista tem baixa prioridade (3ª) — elemento que qualifica simultaneamente a Líder e Especialista é **Líder**, não Especialista. Leitura correta: Especialista é perfil para elementos "do meio" com alta dispersão de posições, não para "estrela em uma métrica mas ruim em outras".

**Métricas com nomes parecidos mas direções opostas.** Exemplo: "tempo de vida útil" (maior-é-melhor) vs "tempo médio de atendimento" (menor-é-melhor). Declaração por métrica é a blindagem; detecção automática por nome foi rejeitada (P-V9-02-Evo com opt-in explícito).

---

## 12. Roadmap pós-MVP (P-V9-XX-Evo)

| ID | Evolução | Origem no refino | Rationale |
|---|---|---|---|
| **P-V9-01-Evo** | Pesos por métrica declarados | T-06 L4 · T-07 L2 | Usuário declara peso de cada métrica; distinto de score composto (nova visão) |
| **P-V9-02-Evo** | Detecção automática de Direção por nome (opt-in) | T-05 L1 | Heurística baseada em padrões ("custo" → menor-é-melhor) com confirmação obrigatória |
| **P-V9-03-Evo** | Normalização Z-score como modo opcional | T-06 L2 | Usuário opta explicitamente; não substitui ordinalidade default |
| **P-V9-04-Evo** | Normalização Min-max como modo opcional | T-06 L2 | Análogo P-V9-03 com min-max |
| **P-V9-05-Evo** | Normalização Log-scale como modo opcional | T-06 L2 | Análogo P-V9-03 com log (para métricas positivas com grande amplitude) |
| **P-V9-06-Evo** | Ranking padronizado (Posição/N) | T-06 L2 | Score com unidade [0,1] para comparação entre conjuntos de tamanhos distintos |
| **P-V9-07-Evo** | Identificador composto (múltiplos campos) | Prévio 2.2 | Consome T-CONCAT (D-053) |
| **P-V9-08-Evo** | Múltiplos Agrupadores no modo Segmentado | T-04 L2 MVP | Segmentação 2+ níveis; requer UX dedicada |
| **P-V9-09-Evo** | Percentil como indicador complementar ao Score | Prévio 4.4 | Saída ganha coluna de percentil do Score (coluna auxiliar) |
| **P-V9-10-Evo** | Comparação do ranking entre períodos distintos | Prévio 16 | Bi-execução com Delta de Posição entre execuções |
| **P-V9-11-Evo** | Leituras qualitativas do conjunto mais granulares | T-10 L6 | 5 leituras atuais → 8-10 nuances (Concentrado no topo · na base · Bipolarizado etc.) |

**Registro de candidata a nova visão (não P-V9):** *"Ranking com pesos ponderados sobre valores normalizados (score composto ponderado)"* — **descaracterizaria V9** (vira outra visão). Registra em **anti-roadmap V9** como fora de escopo por definição.

---

## 13. Nomenclatura oficial da V9

Termos oficiais consolidados em T-01 da sessão de refino:

| Termo oficial | Definição curta |
|---|---|
| **Identificador** | Campo categórico obrigatório que identifica a unidade sendo ranqueada (vendedor, produto, filial, cliente). Exatamente um por execução. |
| **Métrica** | Campo numérico alvo do ranking. 2 mínimo, 6 máximo recomendado (10 absoluto) por execução. |
| **Direção da Métrica** | Declaração obrigatória por métrica: Maior-é-melhor (ordem decrescente) · Menor-é-melhor (ordem crescente). |
| **Agrupador** | Campo categórico opcional que segmenta o conjunto em universos independentes de ranking (modo Segmentado). |
| **Modo de Ranking** | Global (todo o conjunto) · Segmentado (recalcula por agrupador). |
| **Valor Consolidado da Métrica** | Valor da métrica por Identificador após aplicação da regra de agregação. |
| **Posição por Métrica** | Rank do Identificador na métrica após ordenação pela Direção. Rank mínimo em caso de empate. |
| **Score Consolidado** | Média aritmética simples das Posições por Métrica de cada Identificador. Menor = melhor. |
| **Melhor Posição** | Menor valor entre as Posições por Métrica de um Identificador. |
| **Pior Posição** | Maior valor entre as Posições por Métrica de um Identificador. |
| **Variação Máxima de Posição** | Pior Posição − Melhor Posição. Indicador de especialização (alta) × equilíbrio (baixa). |
| **Classificação** | Uma de quatro classes de perfil: Líder · Especialista · Equilibrado · Retaguarda (mutuamente exclusivas, com prioridade declarada). |
| **Líder** | Identificador com Score Consolidado no top 20% do conjunto analisado. |
| **Especialista** | Identificador com Variação Máxima ≥ 50% do total de Identificadores válidos, quando não já Líder ou Retaguarda. |
| **Equilibrado** | Classe residual · não classificado como Líder, Retaguarda ou Especialista. |
| **Retaguarda** | Identificador com Score Consolidado no bottom 20% do conjunto analisado. |
| **Conjunto Analisado** | Modo Global: base inteira. Modo Segmentado: cada grupo separadamente. |
| **NULO_MEDIDA** | Classificação especial paralela · elemento com 0 métricas válidas (substitui classe primária). |

**Sinônimos aceitáveis em microcopy:** "Ranking Consolidado" para "Score Consolidado" em contexto pedagógico; "Perfil" para "Classificação" em rótulo de tela.

**Evitar:**
- **"Líder Geral"** — ambíguo com "Líder" oficial; só em texto explicativo
- **"Baixo Desempenho"** — interpretativo; Retaguarda é rótulo neutro
- **"Ponto forte / ponto fraco"** — interpretativo (padrão D-087)
- **"Percentil"** — comunicação explicativa apenas; não rótulo oficial (V9 é normativo em posição/rank)
- **"Peso por métrica"** — MVP não tem pesos; não usar em UI

---

## 14. Posicionamento C.5

V9 preserva e reforça o princípio C.5 em múltiplos pontos:

- **Consolidação obrigatória da unidade analítica** antes de ranquear — sistema não decide se ordena sobre linhas brutas (§4.3)
- **Modo da base declarado** (Transacional × Pré-agregado) — padrão default declarado com detecção na amostragem (§4.1)
- **Direção por métrica sem default** — gravidade da inversão justifica fricção UX (§4.4)
- **Posições ordinais como substrato do score** — escalas não são normalizadas sem declaração (§4.9)
- **Pesos por métrica fora de escopo** — equal-weighted é arquitetura, não limitação (§4.10)
- **Thresholds de classificação como default declarado editável** — defaults operacionais sem decisão embutida (§5.6)
- **Expansão por empate em pontos de corte** — preserva equivalência matemática em vez de cortar arbitrariamente (§5.6)
- **Score parcial com warning** — preserva elemento com cobertura incompleta sem mascarar (§5.3)
- **Rótulos descritivos neutros** em Resumo Executivo — fato matemático, não interpretação (§5.7 Bloco 4)
- **Nota estática de redirecionamento apenas no Resumo Executivo** — nenhum redirecionamento em configuração (§5.9)

---

## 15. Relação com Fundação e retroação sobre V7

### 15.1 Requisitos novos para a Fundação

G-FUND precisa absorver os seguintes requisitos originados em V9:

- **T-AGRUPA com regra de agregação por métrica** — aceita dicionário `{metrica: regra}` em vez de regra única (extensão V7 D-082 · F-TRANS)
- **T-AGRUPA com no-op validado** quando modo = Pré-agregado (herança V7 D-082 · F-MOT)
- **T-RANK com novo escopo `cross_elementos_dentro_do_agrupador`** para modo Segmentado V9 · distinto de `intra_grupo` V7 e `global` V4/V10 (extensão D-041 · F-TRANS)
- **T-RANK com regra_desempate V9-específica em 4 níveis** (score → variação → alfabético → inserção · extensão D-041 via D-073 · F-TRANS)
- **T-SEMA com contrato por métrica com efeito no cálculo** — primeira consumidora com esse contrato (extensão D-087 via D-073 · F-TRANS)
- **Detecção automática de duplicatas em amostragem** para default declarado de modo (F-MOT)
- **Classificação especial NULO_MEDIDA por elemento** como valor válido do campo `classificacao` no V9Result (F-MOT)
- **Cálculo de percentis com `ceil` para arredondamento** em conjuntos pequenos (F-MOT)
- **Expansão por empate no corte percentual** — regra determinística (F-MOT)
- **Teste de razão de amplitude entre métricas** para detecção de heterogeneidade de escalas (F-MOT)
- **Exportação Excel com 6 abas** incluindo Mapa de Perfil (matriz pivotada com coloração condicional e destaques de extremos · F-EXP)

### 15.2 Retroação sobre V7 (cumprida)

Este DCV cumpre a retroação diferida V7→V9 registrada em D-081. §2.3 preenche as 3 células marcadas *(a confirmar em DCV-V9)* no DCV-V7 aprovado:

- (a) Unidade analítica V9 = **Identificador** (Global) · **Identificador + Agrupadores ativos** (Segmentado)
- (b) Classificação do resultado V9 = **Líder · Especialista · Equilibrado · Retaguarda** (4 classes com prioridade declarada)
- (c) T-AGRUPA em V9 = **Sim — consumida** com 5 regras (Soma · Média · Máximo · Mínimo · Contagem), regra independente por métrica

Fechamento do par autônomo Família D nos dois lados. DCV-V7 aprovado fica sem células pendentes na próxima iteração do kit.

D-081 permanece registrada como contexto histórico · marcada como **cumprida por D-091** em status.

---

## 16. Sumário do refino (12 pendências fechadas em sessão única)

Sessão de refino executada em 19/04/2026 seguindo padrão D-019 + D-034 + D-033. 12 pendências originais trabalhadas (T-01 a T-12), todas fechadas, nenhuma deferida.

| # | Tema | Referência |
|---|---|---|
| T-01 | Vocabulário canônico V9 (18 termos · anti-glossário em 5 itens) | §13 (consolidação terminológica) |
| T-02 | Posicionamento Família D + §2.3 simétrico + cumprimento D-081 | D-091 · §2.3 |
| T-03 | Fronteira V9 × V4 · V9 × V5 · nota V9 × V7 | §2.2 (aplicação de padrão) |
| T-04 | Modo da base + unidade analítica + consolidação obrigatória + regras de agregação por métrica | D-092 · §4.1 · §4.2 · §4.3 · §4.7 |
| T-05 | Múltiplas medidas + direção obrigatória + T-SEMA múltiplo com efeito no cálculo | D-093 · §4.4 · §4.5 · §4.6 · §4.8 |
| T-06 | Escalas heterogêneas + não-normalização + alternativas rejeitadas | D-094 · §4.9 · §4.10 |
| T-07 | Score consolidado (média simples) + alternativas rejeitadas + nulos em 2 camadas | D-095 · §5.3 |
| T-08 | Rank mínimo + desempate visual 4 níveis + T-RANK V9-específico | D-096 · §5.4 |
| T-09 | Variação Máxima + threshold Especialista 50% + casos-limite | D-097 · §5.5 |
| T-10 | Taxonomia 4 classes + critérios percentuais + 5 leituras de conjunto + casos-limite | D-098 · §5.6 |
| T-11 | Resumo Executivo 6 blocos + Excel 6 abas com Mapa de Perfil + nota estática | D-099 · §5.7 · §5.8 · §5.9 |
| T-12 | 12 bloqueios + escala multi-eixo + 9 diretrizes performance + 11 roadmap P-V9 | D-100 · §7 · §8 · §12 |

**Família D · Posição relativa fechada em Fase 0**  (V7 e V9 ambas com DCV aprovado).

**Próxima Fase 0:** DCV-V5 → DCV-V6 (Família E · Estrutura interna, 2 visões). Família E fecha a Fase 0; G-FUND abre em sequência direta.
