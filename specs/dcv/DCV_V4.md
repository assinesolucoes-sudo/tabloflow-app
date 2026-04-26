# DCV-V4 — Composição e Participação

**Documento de Compreensão da Visão · V4 · Família C · Composição**

**Status:** Aprovado · **Versão:** 19/04/2026 (sessão única DCV-V4)
**Origem:** DCV prévio produzido pela Usuária com apoio do ChatGPT · refinado pelo Arquiteto em 13 pendências fechadas
**Decisões geradas:** 10 D-XXX (1 transversal forte · 1 transversal de Fundação · 8 específicas V4 ou secundárias)
**Warnings catalogados:** 20 W-V4-* (4 bloqueios · 4 alertas · 12 informativas)

---

## 1. O que a visão faz

A V4 analisa como um total é composto e onde está a concentração. Mostra quanto cada elemento representa do todo, quem domina, quem é residual, e se a estrutura está concentrada em poucos ou distribuída entre muitos. No modo Comparação, evidencia se a relevância de um elemento em uma medida se mantém nas demais.

A V4 analisa **forma**, não movimento. Não responde o que mudou entre dois estados (V2), nem como algo evoluiu ao longo de uma sequência (V3). Responde a estrutura de um total em um momento.

## 2. Quando usar

Use a V4 quando quiser entender a **forma** de um total em um momento específico. Casos típicos:

- Composição de receita por produto
- Participação de clientes no faturamento
- Concentração de custo por centro
- Priorização de portfólio por Curva ABC
- Verificação se dominância em Receita se traduz em dominância em Margem

Distinção V4 × V10 · V2 · V3:

- **V2**: confronto entre dois estados de uma base (Orçado × Realizado). Pergunta "o que mudou". A V4 não compara estados.
- **V3**: sequência ao longo de eixo ordenado (receita mês a mês). Pergunta "como evoluiu". A V4 observa um ponto no tempo.
- **V10**: view especializada sobre V4 Modo 2 (Curva ABC). Oferece entrada simplificada focada em Pareto com microcopy e visualização dedicados a "poucos vitais × muitos triviais". Consome a mesma lógica da V4, sem reimplementação.

## 3. O que você obtém

Por agrupador: valor consolidado, participação percentual, posição no ranking, participação acumulada. No modo Curva ABC, classificação A/B/C por concentração. No modo Comparação de Distribuição, a mesma análise aplicada a várias medidas lado a lado, com indicação de divergência entre elas. Exportação Excel com rastreabilidade completa; aba de Diagnóstico sempre ao final (D-017).

## 4. Como funciona

Você sobe a base, escolhe a aba e o modo analítico, seleciona a medida (ou medidas) e os agrupadores. O sistema consolida os dados por agrupador antes de calcular qualquer participação — garantindo que Participação = Valor Consolidado ÷ Total Geral. A ordenação é sempre por valor decrescente. No modo ABC, você define os limiares (padrão 80% / 95%) e recebe a classificação. No modo Comparação, você escolhe uma medida de referência para orientar a leitura visual — os cálculos de cada medida permanecem independentes.

---

## 5. Modos da visão

### 5.1 Modo 1 · Composição Simples

Entrega: valor consolidado, participação %, ranking, participação acumulada. Sem classificação ABC.

Usar quando o objetivo é entender a estrutura do total sem priorização formal.

### 5.2 Modo 2 · Curva ABC

Entrega tudo do Modo 1 + classificação ABC por concentração acumulada. Limiares default declarados na configuração: A = 80%, B = 95%, C = acima de 95% (editáveis na E4).

Usar quando o objetivo é priorização, gestão de portfólio, foco operacional e leitura de concentração.

### 5.3 Modo 3 · Comparação de Distribuição

Entrega tudo do Modo 2 aplicado separadamente a cada medida selecionada. Adiciona:

- Comparação par-a-par da classe de cada elemento contra medida de referência
- Síntese de divergência (gap máximo entre classes do elemento)
- Delta de ranking como informação complementar

Usar quando o objetivo é entender se a relevância de um elemento em uma medida se traduz em relevância nas demais. Exemplo: "Um elemento que domina em Receita também domina em Margem?"

---

## 6. Estrutura de entrada

Uma base lógica por execução, com uma ou mais abas. O usuário escolhe a aba analisada.

### 6.1 Formatos suportados

**POR_COLUNAS** — cada medida é uma coluna distinta.

```
Produto | Receita | Custo | Margem
```

**POR_LINHAS** — medidas empilhadas em linhas, identificadas por coluna discriminadora.

```
Produto | Tipo_Medida | Valor
Arroz   | Receita     | 100
Arroz   | Custo       | 60
Arroz   | Margem      | 40
```

Para POR_LINHAS, o motor realiza pivot interno antes do cálculo.

### 6.2 Seleção de medidas em POR_LINHAS

Quando a coluna discriminadora tem **3 ou mais valores únicos**, o motor ativa o bloco **Seleção de medidas em POR_LINHAS** na E2, após a escolha do Modo analítico.

Lógica condicionada pelo Modo:

| Modo | Seleção mínima | Default declarado |
|---|---|---|
| 1 | 1 medida | Primeira medida na ordenação inteligente |
| 2 | 1 medida | Primeira medida na ordenação inteligente |
| 3 | 2 ou mais medidas | Todas pré-selecionadas |

Ordenação inteligente herdada de D-026 (numérica crescente, cronológica crescente com detecção pt-BR/pt-EN, alfabética, misto → alfabético com W-V4-MIX).

**Nota:** o termo "Modo 4" usado na V2 (seleção entre estados) **não se aplica à V4** — V4 usa "Seleção de medidas em POR_LINHAS", vocabulário específico. Colisão de nomes evitada deliberadamente.

### 6.3 Tipos de medida

A V4 herda a taxonomia consolidada em D-025 (4 tipos: aditivo, relativo, não-aditivo, estado/situação). Tratamento por tipo:

| Tipo | Comportamento na V4 |
|---|---|
| Numérico aditivo | Executa sem aviso (receita, custo, volume, quantidade) |
| Numérico relativo | **Default declarado na E3** com 3 opções: "analisar mesmo assim" (default), "escolher outra medida", "agregar por média ponderada antes" (só Modo 1; exige campo de peso; desativa ABC) |
| Numérico não-aditivo | Idêntico ao relativo |
| Estado/Situação | **Bloqueio operacional** com redirecionamento: "composição por participação não se aplica a campos categóricos. Use V6 (cruzamento de dimensões)." |

No Modo 3, a regra aplica-se **por medida selecionada**. Tipos heterogêneos no Modo 3 disparam W-V4-MD3-HETERO (ver §8.3).

### 6.4 Agrupadores

Os agrupadores representam os elementos cuja composição será analisada (produto, cliente, centro, categoria, filial). A V4 herda **integralmente** a escala progressiva de D-027:

| N° agrupadores | Comportamento |
|---|---|
| 1-3 | Normal, sem aviso |
| 4-5 | Aviso + estimativa de linhas em tempo real |
| 6-8 | Confirmação obrigatória extra (W-V4-AGRUP-MUITOS) |
| 9+ | Bloqueio com sugestão: "para cruzamento multidimensional, considere V6 ou V9" |

Microcopy de bloqueio adaptada para V4 (sugere V6 e V9 em vez de V6 apenas como V2).

---

## 7. Configuração do usuário — 5 etapas progressivas

A V4 estrutura configuração em 5 etapas sequenciais com dependência, conforme padrão §13.2 do CONTEXT e D-029 adaptado. Mecânica de invalidação em cadeia herdada de D-029.

### E1 · Origem dos dados
- Upload do arquivo
- Escolha da aba

### E2 · Estrutura e modo
- Formato de entrada (POR_COLUNAS / POR_LINHAS)
- Modo da visão (1 / 2 / 3)
- Microcopy explicativo do Modo visível (não escondido em tooltip)
- Se POR_LINHAS com 3+ valores na discriminadora: bloco "Seleção de medidas em POR_LINHAS"

### E3 · Medida(s) e tipo
- Seleção da medida (1 para Modo 1/2; 2 ou mais para Modo 3)
- Tipo inferido pelo motor + confirmação do usuário
- Se tipo relativo ou não-aditivo: bloco de default declarado com 3 opções
- Se tipo estado/situação: bloqueio com redirecionamento V6
- Se Modo 3 com tipos heterogêneos: bloco declarado de heterogeneidade (3 opções)
- Se Modo 3: seleção de medida de referência (default: primeira selecionada; editável)
- Se detectados negativos na amostragem: bloco declarado de negativos (3 opções)

### E4 · Agrupadores e classificação
- Seleção de agrupadores (1-8 com avisos progressivos; 9+ bloqueia)
- Regra de agregação (soma default; outras conforme T-AGRUPA)
- Estimativa de linhas em tempo real
- Se Modo 2 ou 3: limiares ABC visíveis, editáveis (default 80/95; validação 0 < A < B < 100)
- No Modo 3: limiares globais (mesmos para todas as medidas)

### E5 · Revisão e execução
- Preview completo da configuração
- Seção "Configurações avançadas" (recolhida por default) com faixas de leitura de síntese editáveis
- Detecção de pré-condições de bloqueio (Total=0 etc.)
- Botão "Processar"

**Hook para bloco condicional entre E4-E5:** reservado para casos onde pré-condições detectadas (Total=0 previsível, outras) exijam resolução antes da execução. Formalização final fica para Spec S-V4.

---

## 8. Regras estruturais

### 8.1 Consolidar antes de calcular (princípio fundamental)

A V4 nunca calcula participação sobre dados brutos. Ordem obrigatória:

1. Normalização e pivot (se POR_LINHAS)
2. Consolidação por agrupador (soma default via T-AGRUPA)
3. Cálculo do Total Geral (soma dos valores consolidados, excluindo NULO_MEDIDA)
4. Cálculo da participação (valor_agregado ÷ total_geral × 100)
5. Ordenação por valor decrescente
6. Ranking via T-RANK
7. Participação acumulada progressiva
8. Aplicação de regras do modo (ABC se Modo 2/3; comparação entre medidas se Modo 3)
9. Geração da base final da visão

Unidade analítica: **Agrupador + Medida**.

### 8.2 Tratamento de nulos e negativos

**Nulo na medida (registro existe, valor em branco):**
- Campo `classificacao_medida = NULO_MEDIDA` no contrato
- Exibição: "Valor nulo na medida"
- Excluído do cálculo (Total Geral não o inclui; participação = None)
- Preservado na listagem com classificação visível
- W-V4-NULL (contagem) + W-V4-NULL-MASS se >20% dos registros

**Nulo em agrupador (dimensão em branco):**
- Rótulo `(sem valor)` aplicado na coluna do agrupador
- Linha entra na análise normalmente (participa do Total Geral, recebe participação, entra em ABC)
- W-V4-AGRUP-SEMVALOR registra contagem

**Negativos na medida:**
- Motor detecta na pré-consolidação da E3
- Bloco declarado com 3 opções:
  1. **Analisar com valores líquidos** (default) — soma algébrica; participação pode ser negativa ou >100%; ABC respeita ordenação por valor
  2. **Separar análise em positivos e negativos** — duas tabelas; participação dentro de cada universo soma 100%
  3. **Usar valor absoluto** — |valor| para ranking/participação; sinal preservado em coluna complementar
- Campo `classificacao_medida = VALOR_NEGATIVO` registra no contrato
- W-V4-NEGATIVOS registra opção escolhida + contagem

**Contrato `classificacao_medida` da V4:**

| Contrato técnico | Exibição ao usuário |
|---|---|
| `VALOR_VALIDO` | (omitido — caso normal) |
| `VALOR_NEGATIVO` | "Valor negativo" |
| `NULO_MEDIDA` | "Valor nulo na medida" |

### 8.3 Modo 3 — divergência, ausência entre medidas, heterogeneidade

**Divergência composta (dois níveis):**

**Par-a-par contra medida de referência** (coluna por medida não-referência):

| Situação | Classificação |
|---|---|
| Mesma classe da referência | Igual |
| 1 nível de diferença | Divergente |
| 2 níveis de diferença | Alta divergência |
| Ref tem classe, outra `—` | Ausente na [nome_medida] |
| Ref `—`, outra tem classe | Ausente na medida de referência |
| Ambas `—` | Elemento fora do Modo 3 (aparece na Composição por Dimensão; não na Comparação) |

**Síntese geral do elemento** (gap máximo entre todas as medidas):

| Condição | Classificação geral |
|---|---|
| gap = 0 | Igual |
| gap = 1 | Divergente |
| gap ≥ 2 | Alta divergência |
| Algum `—` em alguma medida | Ausência parcial |

**Medida de referência** (3 papéis no Modo 3):
1. Ordenação visual na tela e Excel
2. Eixo de leitura orientadora
3. Eixo de comparação par-a-par para divergência (novo nesta decisão)

Default: primeira medida selecionada na E3. Usuário pode alterar.

**Heterogeneidade de tipos no Modo 3:**

Motor detecta quando Modo 3 tem medidas de tipos diferentes (ex: aditiva + relativa). Bloco declarado na E3:

- ☑ Entendo, prosseguir (default)
- ☐ Remover medidas incompatíveis
- ☐ Cancelar e reconfigurar

W-V4-MD3-HETERO registra a escolha.

**Warnings do Modo 3:**
- W-V4-MD3-AUSENTE: contagem de elementos com ausência em alguma medida
- W-V4-MD3-HETERO: Modo 3 rodou com tipos heterogêneos + escolha do usuário

### 8.4 Ranking e T-RANK

A V4 é a **primeira visão a consumir T-RANK** da Fundação. Regra default fixada (que vira requisito do G-FUND):

**Regra de desempate default de T-RANK (3 níveis):**

1. Valor agregado decrescente
2. Em empate: concatenação dos agrupadores na ordem declarada pelo usuário, ordem alfabética crescente, case-insensitive, acentos normalizados
3. Em empate ainda: ordem de inserção da linha original

Tolerância para floating point: `1e-9` absoluto. Se tolerância resolve, não é empate real.

T-RANK aceita parâmetro `regra_desempate` opcional — visões posteriores (V9) podem sobrescrever.

W-V4-EMPATE: lista casos com resolução por regra secundária ou terciária.

### 8.5 Limiares ABC (Modos 2 e 3)

- **Default declarado**: A = 80%, B = 95% (visíveis, editáveis na E4)
- Classe A: acumulado ≤ A; Classe B: A < acumulado ≤ B; Classe C: acumulado > B
- Validação: 0 < A < B < 100
- **Modo 3: limiares globais** (mesmos para todas as medidas) — preserva comparabilidade da divergência
- **V10 (view especializada)**: herda os mesmos defaults 80/95; diferença está em visualização e microcopy, não nos números
- W-V4-ABC-CUSTOM registra quando limiares diferentes do default foram usados

### 8.6 Total Geral = 0 (bloqueio adaptativo por causa)

Matemática de participação exige Total Geral ≠ 0. Motor detecta Total=0 após consolidação e antes de calcular participação, identificando a causa:

| Causa | Microcopy do bloqueio |
|---|---|
| Base toda nula (todos valores NULO_MEDIDA) | "Nenhum registro válido. Verifique a base." |
| Cancelamento positivo/negativo | "Total Geral zero por cancelamento. Separar em positivos e negativos permite analisar cada universo." + link para reexecutar com opção da P-04 |
| Outro | "Total Geral zero. Verifique a base ou o filtro aplicado." |

W-V4-TOTAL-ZERO registra causa + sugestão dada.

---

## 9. O que a visão entrega

### 9.1 Granularidade do resultado

- **Modo 1:** 1 linha por combinação de agrupadores
- **Modo 2:** 1 linha por combinação de agrupadores + classe ABC
- **Modo 3:** 1 linha por combinação de agrupadores + colunas por medida (valor, participação, ranking, classe ABC, divergência par-a-par contra referência) + síntese geral de divergência

### 9.2 Resumo Executivo — 6 blocos fixos adaptados por modo

**Bloco 1 · Cabeçalho da análise** (constante)
Título amigável, modo analítico, medida(s) + tipo(s), agrupadores, data/hora.

**Bloco 2 · Números-âncora**

- Modo 1: Total Geral · N° elementos · maior participação individual · top 3 acumulado
- Modo 2: Total Geral · N° elementos · % elementos em Classe A × % total em A · % elementos em Classe C × % total em C
- Modo 3: Total Geral por medida · N° elementos comuns · N° com ausência parcial · % com alta divergência

**Bloco 3 · Distribuição de classificações estruturais**

- Modo 1: ausente (nada a classificar estruturalmente)
- Modo 2: contagem e % total por classe A/B/C + breakdown de concentração
- Modo 3: contagem por classificação geral de divergência (Igual / Divergente / Alta divergência / Ausência parcial)

**Bloco 4 · Elementos destacados**

- Modo 1: top 10 por participação (posição, agrupador, valor, participação %, acumulado %)
- Modo 2: top 10 da Classe A + elementos na fronteira A→B
- Modo 3: top 10 com alta divergência (classe em cada medida + divergência par-a-par)

**Bloco 5 · Leituras descritivas de síntese**

Modo 1/2: **Leitura de concentração** baseada em critério matemático explícito (top 20% dos elementos):
- Concentrada (default): top 20% > 80% do total
- Equilibrada (default): 40%-80%
- Pulverizada (default): < 40%

Modo 3: **Leitura de coerência** baseada em % elementos com "Igual":
- Coerência alta (default): > 70%
- Coerência média (default): 40%-70%
- Coerência baixa (default): < 40%

**Faixas editáveis** em "Configurações avançadas" da E5 (Opção B). Microcopy explícito: "Estas faixas afetam apenas a frase de síntese do Bloco 5. Os cálculos principais (participação, classificação ABC, divergência) não são afetados."

W-V4-LEITURA-CUSTOM registra customização.

**Bloco 6 · Qualidade estrutural** (resumo do Diagnóstico)

Registros com NULO_MEDIDA, VALOR_NEGATIVO, rótulo `(sem valor)`, empates resolvidos, limiares ABC customizados, heterogeneidade Modo 3, demais warnings aplicáveis.

### 9.3 Exportação Excel

Herda regra transversal D-017 (**Diagnóstico sempre última aba**). Tela e Excel nunca divergem (princípio P0.4 do prévio, preservado).

| Modo | Abas | Conteúdo |
|---|---|---|
| Modo 1 | 4 abas | Resumo Executivo · Composição por Dimensão · Dados Analíticos · **Diagnóstico** |
| Modo 2 | 5 abas | + Curva ABC Detalhada · **Diagnóstico** |
| Modo 3 | 6 abas | + Curva ABC Detalhada · Comparação de Distribuição · **Diagnóstico** |

**Aba Comparação de Distribuição (Modo 3):**
- Elemento (agrupadores)
- Classe ABC em cada medida
- Ranking em cada medida (delta complementar)
- Divergência par-a-par contra referência (uma coluna por medida não-referência)
- Divergência geral (síntese gap máximo)

---

## 10. Bloqueios operacionais

12 bloqueios definidos (8 herdados de D-032 com ajustes + 4 V4-específicos novos):

1. Arquivo ilegível ou corrompido
2. Estrutura inválida (arquivo vazio, aba sem dado, sem coluna numérica)
3. Coluna discriminadora POR_LINHAS com 0 ou 1 valor único (W-V4-N0 / W-V4-N1)
4. Medida com 100% de nulos
5. Mais de 9 agrupadores declarados
6. Média ponderada com pesos todos zerados ou negativos
7. Falha estrutural não-recuperável na transição E4→E5
8. Análise gera mais de 500.000 linhas no resultado
9. **Total Geral = 0** (W-V4-TOTAL-ZERO — com causa adaptativa)
10. **Modo 3 com <2 medidas selecionadas** (W-V4-MEDIDAS-MIN)
11. **Tipo de medida = Estado/Situação** (bloqueio com redirecionamento V6)
12. **Limiares ABC inválidos** (A ≥ B ou fora de 0-100)

**Diretrizes de performance** herdadas integralmente de D-032 (7 diretrizes sem modificação).

---

## 11. T-MODELO na V4

Herda padrão D-030: persiste **configuração lógica**, nunca dado.

### 11.1 Persiste

| Campo | Observação |
|---|---|
| Identificação | Nome, descrição, datas |
| Estrutura | POR_COLUNAS/POR_LINHAS; discriminadora + medidas selecionadas se desempilhamento |
| Modo da visão | 1 / 2 / 3 |
| Medida(s) | Nomes, tipos declarados, semântica |
| Default declarado para tipo relativo/não-aditivo | Opção escolhida + campo de peso se média ponderada |
| Default declarado para negativos | Opção escolhida |
| Agrupadores | Lista ordenada + rótulos amigáveis |
| Regra de agregação | Soma ou outra via T-AGRUPA |
| Limiares ABC | Sempre persistidos, mesmo quando iguais ao default |
| Medida de referência | Se Modo 3 |
| Faixas de leitura de síntese | Persistidas se editadas |
| Decisão de heterogeneidade | Se aplicou |

### 11.2 Não persiste

- Arquivo bruto · nome do arquivo · aba selecionada · filtros pós-execução · resultado da análise anterior · dados sensíveis

### 11.3 Aplicação em nova base (3 casos V4-específicos)

- **Modelo Modo 2/3 em base sem medidas suficientes:** W-V4-MOD-INCOMP · Modo cai para Modo 1 na sugestão · limiares ABC e medida de referência zerados
- **Modelo com média ponderada sem campo de peso:** W-V4-MOD-PARCIAL · default volta para "analisar mesmo assim"
- **Modelo com limiares ABC customizados:** preservados e reaplicados (política analítica do usuário) · W-V4-ABC-CUSTOM dispara

Diagnóstico registra: "Modelo aplicado: [nome] · Campos casados: [N/total] · Ajustes manuais: [lista]". Aba Parâmetros do Excel registra estado **efetivo**, não original do modelo.

---

## 12. Warnings oficiais da V4

**4 bloqueios:** W-V4-N0 · W-V4-N1 · W-V4-MEDIDAS-MIN · W-V4-TOTAL-ZERO

**4 alertas:** W-V4-NULL-MASS · W-V4-MIX · W-V4-NMANY · W-V4-AGRUP-MUITOS

**12 informativas:** W-V4-TIPO-DECL · W-V4-NULL · W-V4-AGRUP-SEMVALOR · W-V4-NEGATIVOS · W-V4-ABC-CUSTOM · W-V4-EMPATE · W-V4-MD3-AUSENTE · W-V4-MD3-HETERO · W-V4-LEITURA-CUSTOM · W-V4-MOD-PARCIAL · W-V4-MOD-INCOMP

Cada warning rastreável à pendência e decisão de origem. Diagnóstico organiza em 3 seções por tipo.

---

## 13. Nomenclatura oficial da V4

- **Medida** — campo numérico analisado
- **Agrupador** — dimensão de composição
- **Valor Agregado** — resultado da consolidação por agrupador
- **Total Geral** — soma dos valores agregados da medida
- **Participação** — razão Valor Agregado ÷ Total Geral, em percentual
- **Ranking** — posição numérica crescente do elemento na ordenação por Valor Agregado decrescente
- **Participação Acumulada** — soma progressiva das participações na ordem do ranking
- **Classe ABC** — classificação por limiares de acumulado (Modos 2 e 3)
- **Medida de Referência** — medida que orienta ordenação, leitura visual e comparação par-a-par (Modo 3)
- **Divergência** — comparação entre classes ABC do elemento em medidas diferentes
- **Delta de Ranking** — informação complementar de posição entre medidas

Vocabulário dual técnico/exibição preservado onde aplicável (contrato `classificacao_medida`, classificações de divergência).

---

## 14. Posicionamento C.5

A V4 foi refinada integralmente sob a lente do princípio C.5 (TabloFlow analisa sobre o dado informado, nunca decide por ele). Manifestações concretas:

- **Tipos relativo/não-aditivo:** default declarado em vez de execução silenciosa
- **Negativos:** 3 opções declaradas em vez de soma algébrica oculta
- **Nulos na medida:** preservados na listagem com classificação visível; excluídos apenas do cálculo
- **Ausência entre medidas no Modo 3:** categoria dedicada, não exclusão silenciosa
- **Heterogeneidade de tipos no Modo 3:** confirmação explícita do usuário
- **Limiares ABC:** default declarado visível, não oculto no motor
- **Faixas de leitura de síntese:** editáveis com microcopy explícito de que não afetam cálculos principais
- **Total Geral = 0:** bloqueio com causa identificada e sugestão de caminho
- **Estado/Situação:** bloqueio honesto com redirecionamento, não cálculo sem significado

Padrão "default declarado" aplicado sistematicamente — consolidado como derivado de C.5 na V2 (D-024/D-025/D-026/D-027/D-029), estendido à V4.

---

## 15. Integração com Fundação

### 15.1 Transversais consumidos

| Transversal | Papel na V4 |
|---|---|
| T-AGRUPA | Consolidação por agrupador antes do cálculo de participação |
| T-DIAG | Aba de Diagnóstico (última do Excel por D-017), categorias AJUSTE_LEVE e DECISAO_USUARIO |
| T-RANK | Ranking determinístico (default V4 definido aqui — ver §8.4) |
| T-ACUM | Acumulado progressivo monotônico sobre a ordenação por valor decrescente |
| T-ABC | Classificação A/B/C por limiares |
| T-PIVOT | Pivot POR_LINHAS → POR_COLUNAS (parâmetro "valores selecionados" já em D-026; requisito adicional: suporte a pivot multi-medida — novo input para G-FUND) |
| T-MODELO | Salvar/aplicar configuração conforme §11 |

### 15.2 Novos requisitos para G-FUND (a formalizar na Fase 1)

1. **T-RANK configurável** com parâmetro `regra_desempate` opcional e default de 3 níveis (§8.4)
2. **T-PIVOT multi-medida** — parâmetro adicional para suportar pivot de medidas empilhadas, não apenas de estados
3. Contrato `classificacao_medida` com 3 valores (VALOR_VALIDO, VALOR_NEGATIVO, NULO_MEDIDA)
4. Diagnóstico padronizado de empates (categoria nova ou extensão de AJUSTE_LEVE)

---

## 16. Decisões geradas

| D-XXX | Tema | Tipo |
|---|---|---|
| D-035 | Relação V4 × V10: V10 como view especializada sobre V4 Modo 2 | **Transversal** (V4 · V10 · G-FUND · Família C) |
| D-036 | Tipos de medida na V4: default declarado por tipo (extensão D-025) | Secundária |
| D-037 | Objetivo da Visão V4 + 5 etapas progressivas + conteúdo canônico | Específica V4 |
| D-038 | Nulos na medida, nulos em agrupador, valores negativos | Específica V4 (análoga D-023) |
| D-039 | POR_LINHAS e seleção de medidas + requisito pivot multi-medida | Específica V4 (análoga D-026) |
| D-040 | Limiares ABC com default declarado (80/95) + limiares globais Modo 3 + herança V10 | Específica V4 |
| D-041 | T-RANK configurável com regra default de 3 níveis | **Transversal de Fundação** |
| D-042 | Modo 3: divergência composta + ausência entre medidas + heterogeneidade | Específica V4 (alto peso) |
| D-043 | Bloqueios operacionais V4 + Total=0 adaptativo + performance | Específica V4 (análoga D-032) |
| D-044 | Resumo Executivo V4 com 6 blocos adaptados + faixas editáveis | Específica V4 (análoga D-031) |

A pendência P-12 (T-MODELO) é consolidada dentro do padrão já documentado em D-030 — não gerou D-XXX própria, referência direta no §11.

---

## 17. Pendências residuais da V4

Nenhuma pendência bloqueante para a implementação da V4 na Fase 2. Itens adiáveis que podem ser refinados sem bloquear o avanço:

- **P-V4-E1 · Pacote visual do Resumo Executivo** — cores, tipografia e layout fino do Bloco 5 das leituras descritivas. Responsabilidade da Spec S-V4 (Fase 2).
- **P-V4-E2 · UI da aba Comparação de Distribuição (Modo 3)** — disposição de medidas lado a lado em Excel com larguras adequadas. Fica para S-V4.
- **P-V4-E3 · Heurística de inferência de tipo de medida** — regras concretas de "como o motor sugere que Margem é relativo e Receita é aditivo". Requisito para motor_upload no G-FUND.
- **P-V4-E4 · Política futura de reuso da lógica ABC com outras visões** — V10 já herda (D-035); V9 pode precisar. Decisão no G-FUND.
- **P-V4-E5 · Estratégia de exibição para bases muito extensas** — paginação/scroll/virtualização da lista de elementos. Fica para S-V4.

---

## 18. Referências cruzadas

- **CONTEXT.md** §3 (Fase 0), §6 (T-RANK atualizado, T-PIVOT estendido), §9 (C.5 + padrão default declarado), §13 (padrões estruturais de produto)
- **DECISIONS.md** D-015 (T-MODELO), D-017 (Diagnóstico última aba), D-019 (padrão condução), D-023 (nulos V2), D-024/D-025/D-026/D-027/D-029 (família default declarado), D-030 (T-MODELO V2), D-031 (Resumo V2), D-032 (bloqueios V2), D-033 (formato kit), D-034 (sinalização densidade), D-035 a D-044 (decisões V4)
- **GLOSSARIO.md** §1 (C.5, Padrão de condução DCV), §5 (4 tipos de medida), §10 (Default declarado, Vocabulário dual)
- **Planilha TabloFlow_Estado_do_Projeto.xlsx** aba 2 (V4 refinada), aba 3 (T-RANK configurável, T-PIVOT multi-medida), aba 5 (D-035 a D-044), aba 6 (vocabulário V4)

---

**Fim do DCV-V4.** Aprovado, virá bloco S-V4 na Fase 2 (Spec + wireframe funcional). Antes disso, DCV-V10 (próxima sessão) herda decisões desta.
