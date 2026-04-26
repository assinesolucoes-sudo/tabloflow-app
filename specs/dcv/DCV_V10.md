# DCV-V10 — Concentração e Pareto

**Status:** Aprovado
**Data aprovação:** 19/04/2026
**Bloco:** DCV-V10 · Sessão 1 (sessão única)
**Família conceitual:** C · Composição e participação
**Visão-base:** V4 (Composição e Participação) — V10 é view especializada sobre V4 Modo 2 (D-035)

---

## 1. Posicionamento

A V10 é uma visão do Módulo 1 · TabloAnálise focada em **concentração**. Responde a uma pergunta específica: "Quais poucos itens concentram a maior parte do valor?"

Estruturalmente, V10 é **view especializada sobre V4 Modo 2** (D-035). Não tem motor próprio — consome a mesma lógica analítica da V4 (participação, acumulado progressivo, classificação ABC via T-ABC, ranking via T-RANK, consolidação via T-AGRUPA). A diferença está em **produto**: entrada simplificada, narrativa Pareto ("poucos vitais × muitos triviais"), visualização Pareto dedicada e apresentação dicotômica (Classe A vs Demais itens) em vez da classificação tripla A/B/C.

Zero duplicação de lógica entre V4 e V10. Refino posterior na Fase 2 consome a implementação de V4 Modo 2 já feita; o trabalho V10 específico da Fase 2 se concentra em app Streamlit (entrada, microcopy, visualização) e na exportação Excel específica (gráfico nativo Pareto).

## 2. Distinção V10 × V4

V4 responde "como o valor se distribui entre os itens" (distribuição completa, classificação A/B/C). V10 responde "quais poucos itens concentram a maior parte do valor" (foco dicotômico Vitais × Demais).

| Dimensão | V4 (Modo 2) | V10 |
|---|---|---|
| Pergunta analítica | Como se distribuem em A, B e C? | Quem são os vitais? |
| O que a tela destaca | Distribuição completa A/B/C | Classe A (vitais) × Demais itens |
| Narrativa | Curva ABC — priorização, gestão de portfólio | Pareto — poucos vitais, muitos triviais |
| Visualização principal | Tabela ordenada com classificação ABC | Curva Pareto clássica com corte vital/trivial |
| Filtro default | Nenhum | Destaque visual em Classe A via disclosure |
| Limiares visíveis | A e B editáveis (80/95) | Só A editável (80); B oculto fixo em 100% |
| Multi-medida | Modo 3 faz | Não faz — manda para V4 Modo 3 |
| Entrada | 5 etapas com escolha de Modo | 4 etapas sem Modo |

**Pontes explícitas no microcopy:**
- V10 → V4 Modo 2: "Para ver a distribuição completa em três classes (A/B/C), use V4 no Modo 2"
- V10 → V4 Modo 3: "Para comparar o comportamento de duas ou mais medidas, use V4 no Modo 3"
- V10 → V6: "Análise de concentração por participação não se aplica a campos categóricos. Use V6" (herança D-036)

## 3. Objetivo da Visão (bloco de ajuda, CONTEXT §13.1)

Estrutura em 4 seções conforme padrão do produto:

**O que a V10 faz**
A V10 identifica os poucos itens que concentram a maior parte do valor em uma medida. Responde à pergunta "quais são os itens críticos a observar?" organizando os dados pela regra de Pareto: poucos vitais × muitos triviais.

**Quando usar**
Quando a base tem muitos itens (produtos, clientes, regiões, SKUs) e o interesse é identificar rapidamente o subconjunto que concentra a maior parte de uma medida somável: receita, custo, volume, demanda. Casos típicos: priorização de portfólio, foco em clientes-chave, análise de concentração de risco, gestão de estoque.

**O que você vai obter**
Uma curva Pareto com os itens da base ordenados por valor decrescente. O corte entre vitais e demais itens fica em 80% do acumulado (editável). Uma tabela separa os dois grupos. O Excel exportado traz o ranking completo, o resumo por grupo e a curva Pareto em aba dedicada.

**Como funciona**
V10 consolida os dados pelos agrupadores escolhidos, calcula a participação de cada item sobre o total da medida, ordena em ranking decrescente e aplica o corte no limiar. A lógica é a mesma da V4 (Análise de Composição) em modo ABC, com apresentação focada em vitais × demais. Se você precisa da distribuição A/B/C completa, use V4 no Modo 2.

## 4. Entradas da visão

### 4.1 Estrutura da base

Herda integralmente V4 (D-037, D-039): POR_COLUNAS ou POR_LINHAS detectados pelo motor; heurística + confirmação da usuária. Seleção de medidas em POR_LINHAS herda D-039 com adaptação V10-específica: **exatamente 1 medida** (radio button, não checkbox). Default declarado: primeira medida na ordenação inteligente (D-026).

### 4.2 Medida analisada

V10 opera com **exatamente 1 medida**. Regra:

- **POR_COLUNAS:** lista de colunas numéricas disponíveis com default declarado (primeira). Radio.
- **POR_LINHAS:** lista de medidas da coluna discriminadora com ordenação inteligente (D-026) e default declarado (primeira). Radio.

**Tipos de medida** herdados da taxonomia D-025:

- **Numérico aditivo:** executa sem aviso.
- **Numérico relativo / Numérico não-aditivo:** bloco declarado na E2 com 3 opções (herança D-036): "Analisar mesmo assim" (default) / "Escolher outra medida" / "Agregar por média ponderada antes de calcular participação" (exige campo de peso; desativa classificação ABC).
- **Estado/Situação:** bloqueio operacional com redirecionamento para V6 (herança D-036).

**Tratamento de negativos** herdado de D-038: motor detecta na pré-consolidação e exibe bloco declarado com 3 opções (Analisar com valores líquidos · Separar em positivos e negativos · Usar valor absoluto). W-V4-NEGATIVOS registra opção escolhida.

**Tratamento de nulos na medida** herdado de D-038: registros com NULO_MEDIDA excluídos do cálculo mas preservados na listagem com classificação visível. Warnings W-V4-NULL e W-V4-NULL-MASS aplicáveis.

### 4.3 Agrupadores e consolidação

Herda integralmente V4:
- Entre **1 e 8 agrupadores** declarados pela usuária (9+ bloqueia — D-027 + D-043 item 5).
- **Regra de agregação** via T-AGRUPA configurável (soma/média/máx/mín/contagem); default soma.
- **Nulo em agrupador** preservado com rótulo `(sem valor)`; entra normalmente no Total Geral (W-V4-AGRUP-SEMVALOR).
- **Estimativa de linhas** calculada via cardinalidade multiplicada (herança D-027 + diretriz de performance 3 de D-032).

### 4.4 Limiar de corte (Classe A)

Diferença-chave em relação a V4 Modo 2:

- V4 Modo 2 expõe **dois limiares** editáveis (A = 80%, B = 95%).
- V10 expõe **apenas o limiar A** editável (default 80%). Limiar B é fixado internamente em 100% e oculto da UI.

Por baixo, T-ABC é chamado com os mesmos defaults de D-040 (80/95). A diferença é exclusivamente de **apresentação**: V10 colapsa visualmente as Classes B e C em "Demais itens". Para ver a distribuição A/B/C completa, usuária é redirecionada a V4 Modo 2 via microcopy explícito.

Validação do limiar A: 0 < A < 100. Editável em "Configurações avançadas" da E3? Não — fica visível direto na E3, com microcopy de contexto.

## 5. Fluxo de configuração em 4 etapas

V10 tem **4 etapas progressivas** (contra 5 de V4). A redução é legítima: Modo é pré-fixado (sempre Modo 2), Medida é única, e isso permite fusão natural de E2+E3 da V4 em uma única etapa "Estrutura e medida".

Mecânica de **invalidação em cadeia** herdada de D-029: editar etapa N invalida N+1 em diante com aviso explícito.

### E1 · Origem dos dados

Idêntica a V4 E1 e V2 E1. Upload de arquivo + seleção de aba. Herança do motor_upload (Fundação).

### E2 · Estrutura e medida

Concentra:

- **Estrutura** — POR_COLUNAS ou POR_LINHAS. Detecção automática + confirmação (herança de V2/V4).
- **Seleção de medidas em POR_LINHAS** (se aplicável) — radio button para exatamente 1 medida, com ordenação inteligente D-026 e default declarado (primeira medida).
- **Medida analisada** — seleção única.
- **Tipo de medida** — 4 tipos (D-025). Numérico relativo/não-aditivo ativa bloco declarado (D-036). Estado/Situação ativa bloqueio com redirecionamento para V6.
- **Bloco declarado de negativos** — quando detectados, 3 opções (herança D-038).

**Microcopy da etapa:**
- Cabeçalho: "Onde está a medida que você quer analisar?"
- Seleção de medida única (POR_LINHAS com múltiplas medidas disponíveis): "Selecione a medida a analisar. V10 responde à pergunta Pareto sobre uma medida. Para comparar o comportamento de duas ou mais medidas, use V4 no Modo 3."

### E3 · Agrupadores e limiar

Concentra:

- **Agrupadores** — 1 a 8, com avisos progressivos; 9+ bloqueia.
- **Regra de agregação** (T-AGRUPA) — soma/média/máx/mín/contagem; default soma.
- **Estimativa de linhas** — calculada e exibida.
- **Limiar A** — campo numérico com default declarado 80%, editável.

**Microcopy da etapa:**
- Cabeçalho: "Como consolidar e onde fazer o corte?"
- Sub-bloco limiar:
  - Título: "Corte vital × demais itens"
  - Campo: "Limiar de corte (%) — padrão 80%"
  - Texto de apoio: "Itens cujo percentual acumulado atinge este limiar formam a Classe A (vitais). Os demais ficam agrupados como 'Demais itens'. Para ver a distribuição completa em três classes (A/B/C), use V4 no Modo 2."

### E4 · Revisão e execução

Concentra:

- **Preview** da configuração.
- **Detecção de pré-condições** — principalmente Total Geral = 0 com bloqueio adaptativo por causa (herança D-043: base toda nula / cancelamento pos-neg / outro).
- **Botão Processar.**
- **Configurações avançadas** (recolhidas por default):
  - **Cardinalidade visual do gráfico Pareto** — default 50, editável.
    Microcopy: "Número máximo de barras individuais no gráfico Pareto (padrão: 50). Itens além deste limite são agregados em uma barra 'Demais'. Isto afeta apenas a visualização — a tabela e o Excel mostram todos os itens."
  - **Faixas de leitura de síntese** (Bloco 5 do Resumo Executivo) — Concentração + Corte, ambas editáveis. Microcopy de escopo: "Estas faixas afetam apenas as frases de síntese do Bloco 5 do Resumo Executivo. Os cálculos principais (participação, classe, curva) não são afetados."

## 6. Lógica analítica (herdada de V4)

A lógica vive em V4 — a listagem abaixo é **referência de consumo**, não especificação nova.

1. **Consolidação** por agrupadores via T-AGRUPA (regra configurável).
2. **Cálculo do Total Geral** da medida.
3. **Cálculo da participação individual** = Valor Agregado ÷ Total Geral.
4. **Ordenação decrescente** via T-RANK com regra de desempate default de 3 níveis (D-041): valor decrescente · concatenação alfabética case-insensitive de agrupadores · ordem de inserção. Tolerância 1e-9 para floating point.
5. **Cálculo do acumulado progressivo** via T-ACUM (monotonicamente crescente).
6. **Classificação ABC** via T-ABC com limiares 80/95 (defaults D-040, editáveis para limiar A).
7. **Apresentação V10:** Classe A exposta explicitamente; Classes B e C colapsadas em "Demais itens" na tela e no Resumo; Análise Principal no Excel mantém coluna "Classe" explícita mas marca "Vital (A)" × "Demais".

Determinismo absoluto garantido (princípio C.1).

## 7. Microanálise na tela

Estrutura em duas zonas empilhadas:

### 7.1 Zona superior · Curva Pareto (largura total)

**Curva Pareto clássica** no topo da microanálise, ocupando largura total. Elementos:

- **Eixo X:** posição no ranking (#1 a #N; até #50 por default com 51+ agregados em "Demais" na visualização).
- **Barras (eixo Y esquerdo):** valor individual por item em ordem decrescente. Classe A em cor primária saturada; Demais itens em tom secundário.
- **Linha (eixo Y direito, 0-100%):** percentual acumulado monotonicamente crescente.
- **Linha horizontal pontilhada** no limiar A efetivo (80% por default ou valor editado).
- **Linha vertical pontilhada** no ponto em que a curva acumulada cruza o limiar.
- **Anotação:** "N itens (X%) concentram Y% do total" — acima da curva, próximo ao ponto de cruzamento.
- **Título dinâmico:** "Curva Pareto · [nome da medida]".
- **Tooltip no hover** das barras: rótulo do item (concatenação dos agrupadores), valor, participação, acumulado, classe.

Se a cardinalidade efetiva ultrapassa o limite visual (default 50), visualização agrega posições 51+ em barra "Demais", mas **curva acumulada sempre vai até 100%**. Warning W-V10-CURVA-TRUNC dispara.

### 7.2 Zona inferior · Seções Vitais/Demais com disclosure

Duas seções empilhadas, ambas com disclosure (acordeão):

**Seção "Vitais · Classe A"** — expandida por default:
- Cabeçalho: "Vitais · Classe A" + "N itens concentram X% do total"
- Lista dos itens com Ranking, Rótulo (concatenação de agrupadores), Valor, Participação, Acumulado

**Seção "Demais itens"** — recolhida por default:
- Cabeçalho sempre visível: "Demais itens · M registros · Y% do total"
- Ao expandir, lista completa dos itens não-vitais

Princípio: **nenhum item escondido.** Disclosure é interação visual, não filtro. Contagem e representatividade dos Demais itens sempre visíveis no cabeçalho.

### 7.3 Casos de borda

- **Classe A vazia** (distribuição pulverizada): seção Vitais vazia com microcopy "Nenhum item concentra até N% do total isoladamente. A distribuição é muito pulverizada — não há vitais claros. Considere usar V4 no Modo 2 para análise de distribuição completa ou reduzir o limiar para identificar os itens mais relevantes." Warning W-V10-CLASSE-A-VAZIA.
- **Classe A com 100%** (base com 1-2 itens): seção Vitais exibe todos; seção Demais fica vazia com microcopy "Todos os itens estão na Classe A. Base pequena demais para análise Pareto significativa." Warning W-V10-BASE-MINIMA.

## 8. Resumo Executivo (6 blocos — herança D-031/D-044 adaptados)

V10 herda a estrutura canônica de 6 blocos de D-031 (V2) e D-044 (V4) com adaptações específicas.

### 8.1 Bloco 1 · Cabeçalho da análise

Padrão D-031. Acrescenta metadado V10: **limiar efetivo usado** (ex.: "Corte em 80% do acumulado").

### 8.2 Bloco 2 · Números-âncora

4 KPIs adaptados à narrativa Pareto:

1. **Total Geral** (valor consolidado da medida)
2. **Total de itens** (cardinalidade após consolidação)
3. **Itens vitais** (número absoluto de itens na Classe A)
4. **Concentração vital** (frase composta: "X% do total em N% dos itens") — a síntese Pareto em números

### 8.3 Bloco 3 · Distribuição de classificações estruturais

Forma compacta com 2 categorias (não 3):

- **Classe A (vitais):** N itens · X% do total
- **Demais itens:** M itens · Y% do total
- **Total:** N+M itens · 100%

### 8.4 Bloco 4 · Elementos destacados

Duas sub-listas:

- **Top 10 vitais** — ordem decrescente, com participação individual e acumulada. Se Classe A tem menos de 10 itens, exibe todos os vitais.
- **Fronteira** — o último item da Classe A + os próximos 3 fora da Classe A. Útil para avaliar se o corte é apertado.

### 8.5 Bloco 5 · Leituras descritivas de síntese

**Leitura principal · Concentração** (herança D-044, microcopy adaptado ao Pareto):

| Faixa (default) | Critério | Microcopy |
|---|---|---|
| Concentrada | top 20% > 80% | "Concentração típica de Pareto. Poucos vitais explicam a maior parte do valor." |
| Equilibrada | 40%-80% | "Concentração moderada. Vitais relevantes, mas distribuição com cauda significativa." |
| Pulverizada | < 40% | "Distribuição pulverizada. Não há vitais claros — Pareto não se aplica fortemente a esta base." |

**Leitura secundária · Corte** (V10-específica, nova):

Observa a diferença entre o último vital e o primeiro não-vital (em pontos percentuais no acumulado):

| Faixa (default) | Critério | Microcopy |
|---|---|---|
| Corte folgado | diferença ≥ 2 pp | "O corte é claro. Há distância visível entre vitais e demais itens." |
| Corte apertado | diferença < 2 pp | "O corte é apertado. O último vital e o primeiro não-vital têm participações próximas — considere inspecionar a fronteira." |
| Empate exato | diferença = 0 | "Há empate exato no corte — regra de desempate determinística aplicada (ver Diagnóstico)." |

Ambas as faixas editáveis em "Configurações avançadas" da E4. Warning W-V10-CORTE-APERTADO dispara quando a leitura secundária indica "corte apertado".

### 8.6 Bloco 6 · Qualidade estrutural

Padrão D-031 sem adaptação V10-específica. Resumo do que aparece no Diagnóstico: casos resolvidos, ajustes leves (T-DIAG), warnings com contagem.

## 9. Exportação Excel (6 abas)

Estrutura padrão Fundação com adaptações V10. D-017 respeitado (Diagnóstico sempre última aba).

1. **Resumo Executivo** — materializa os 6 blocos do §8.
2. **Análise Principal** — ranking completo com colunas Ranking, [Agrupadores], [Medida], Participação, Acumulado, Classe. Linha horizontal separadora entre último vital e primeiro não-vital. Linhas Classe A em cor de fundo suave.
3. **Curva Pareto** — zona superior com **gráfico nativo Excel** (combo chart barras + linha via openpyxl) com linhas de referência no limiar A; zona inferior com dados tabulares (Ranking, Rótulo, Valor, Acumulado). Gráfico respeita cardinalidade visual (50 + agregado "Demais"); tabela sempre exibe todas as posições individuais.
4. **Base Analítica** — dados consolidados pós-T-AGRUPA (insumo do cálculo). Colunas: [Agrupadores], [Medida agregada], classificacao_medida (VALOR_VALIDO / VALOR_NEGATIVO / NULO_MEDIDA).
5. **Parâmetros** — configuração usada: arquivo, aba, estrutura, medida, tipo, tratamento de negativos, agrupadores, regra de agregação, limiar A efetivo, cardinalidade visual, faixas de leitura (default ou customizado), data/hora, usuário, versão V10.
6. **Diagnóstico** (D-017) — warnings disparados com categoria AJUSTE_LEVE/DECISAO_USUARIO (D-021), ajustes aplicados, tempo por etapa (diretriz de performance 7 · D-032), total de registros processados, warnings V10-específicos e herdados V4.

Gráfico nativo Excel é **requisito novo para F-EXP** registrado como entrada para G-FUND. Linha horizontal separadora Vital/Demais na Análise Principal também é capability de formatação nova para F-EXP.

## 10. T-MODELO em V10

Padrão estrutural de produto CONTEXT §13.3. V10 aplica com adaptação de **view especializada**.

### 10.1 Compartilhamento cross-visão V4 Modo 2 ↔ V10

Modelos salvos em V4 Modo 2 são **aplicáveis em V10**, e vice-versa. Ao aplicar cross-visão, T-MODELO dispara diálogo de confirmação declarando:

- **Parâmetros transferidos** (comuns às duas visões): medida, agrupadores, regra de agregação, limiar A, tipo de medida, tratamento de negativos, seleção de medida em POR_LINHAS.
- **Parâmetros com default da visão-destino** (específicos da origem não aplicam): em V10, cardinalidade visual = 50 e faixas de leitura = default; em V4 Modo 2, limiar B = 95.
- **Parâmetros descartados** (específicos da origem sem equivalente): ao aplicar V10 em V4 Modo 2, cardinalidade visual e faixa de corte são descartadas; ao aplicar V4 Modo 2 em V10, limiar B é descartado.

Aplicação **intra-visão** (V4 Modo 2 → V4 Modo 2 · V10 → V10) não dispara diálogo — transfere tudo direto.

### 10.2 Casos não aplicáveis

Modelos de V4 Modo 1 ou V4 Modo 3 **não são aplicáveis em V10**, e vice-versa. Conversão perderia essência analítica:

- Modo 1 não tem componente ABC.
- Modo 3 opera com 2+ medidas; V10 exige exatamente 1.

### 10.3 Sinalização

- Lista de modelos aplicáveis em V10 exibe modelos V4 Modo 2 com badge discreto "de V4 Modo 2". Idem inverso.
- Warning **W-V10-MODELO-CONVERTIDO** (informativa) registra aplicação cross-visão, com lista de parâmetros defaulted e descartados. Warning simétrico registrado em V4 quando modelo V10 é aplicado.

### 10.4 Padrão transversal

A regra de compartilhamento cross-visão estabelecida aqui é **padrão reutilizável para qualquer par de view especializada** (CONTEXT §13.4). Aplicará a V2 ↔ V1 via T-DUAL quando V1 for refinada. Vira cláusula adicional em §13.4.

## 11. Bloqueios operacionais e diretrizes de performance

V10 herda **integralmente** os 12 bloqueios operacionais de V4 (D-043) com adaptação de microcopy para a narrativa Pareto onde aplicável. Principais:

1. Arquivo ilegível/corrompido
2. Estrutura inválida
3. Coluna discriminadora POR_LINHAS 0 ou 1 valor único (W-V4-N0, W-V4-N1)
4. Medida com 100% de nulos
5. Mais de 9 agrupadores
6. Média ponderada com pesos todos zerados ou negativos
7. Falha estrutural não-recuperável na transição E3→E4
8. Análise gera >500.000 linhas
9. Total Geral = 0 (bloqueio adaptativo por causa)
10. **Não aplicável a V10** — Modo 3 com <2 medidas (V10 sempre 1 medida)
11. Tipo de medida = Estado/Situação (redireciona para V6)
12. Limiar A inválido (fora de 0-100)

**Diretrizes de performance** de D-032 herdadas integralmente (7 diretrizes, sem adaptação V10-específica).

## 12. Warnings catalogados na V10

### 12.1 V10-específicos (5)

| Sigla | Categoria | Gatilho |
|---|---|---|
| W-V10-CURVA-TRUNC | Informativa | Visualização agregou itens além do limite de barras na Curva Pareto |
| W-V10-CORTE-APERTADO | Informativa | Diferença < 2 pp no acumulado entre último vital e primeiro não-vital |
| W-V10-CLASSE-A-VAZIA | Informativa | Nenhum item atinge o limiar A isoladamente (distribuição pulverizada) |
| W-V10-BASE-MINIMA | Informativa | Base com 1-2 itens — Pareto não significativo |
| W-V10-MODELO-CONVERTIDO | Informativa | Modelo de outra visão aplicado com mapeamento cross-visão |

### 12.2 Herdados de V4 (aplicáveis quando o gatilho dispara)

W-V4-NULL · W-V4-NULL-MASS · W-V4-AGRUP-SEMVALOR · W-V4-NEGATIVOS · W-V4-TIPO-DECL · W-V4-EMPATE · W-V4-TOTAL-ZERO (microcopy adaptado Pareto) · W-V4-N0 · W-V4-N1 · W-V4-MIX · W-V4-NMANY · W-V4-ABC-CUSTOM (quando limiar A editado pela usuária).

## 13. Contratos

V10 não introduz contrato de motor próprio — consome MotorResult de V4 Modo 2. Contrato de resultado V10-específico (VNResult da V10) é uma **projeção** sobre o MotorResult V4 que substitui a coluna "Classe ABC" (A/B/C) por **"Classe Pareto"** binária (Vital / Demais). Detalhamento em Spec da Fase 2.

Contrato `classificacao_medida` (D-038) é reutilizado integralmente: VALOR_VALIDO / VALOR_NEGATIVO / NULO_MEDIDA.

## 14. Evidência analítica e limites da visão

V10 evidencia: **concentração** de valor sobre uma medida; **distribuição** acumulada em ordem decrescente; **impacto relativo** dos itens; **fronteira** entre vitais e demais.

V10 NÃO: explica causas da concentração; valida qualidade dos dados; trata inconsistências por iniciativa própria (delega à usuária via blocos declarados); interpreta o que "concentrado" significa no negócio.

## 15. Dependências para Fase 1 (G-FUND)

Requisitos novos que V10 coloca para G-FUND — todos derivados de V4 refinado + adaptações V10:

- **Gráfico nativo Excel (Curva Pareto)** via openpyxl: combo chart barras + linha + linhas de referência (horizontal no limiar, vertical no ponto de cruzamento). Linhas de referência podem exigir workaround em openpyxl (série oculta ou anotação textual).
- **Formatação dinâmica de separador Vital/Demais** na Análise Principal: borda espessa entre a última linha de Classe A e a primeira linha de Demais itens.
- **T-MODELO com mapeamento cross-visão** para pares de view especializada (V4 Modo 2 ↔ V10 agora; V2 ↔ V1 futuro). Contrato precisa expor `visao_origem` + `visoes_aplicaveis` + parâmetros categorizados (comuns · específicos origem · específicos destino).

Transversais consumidos sem adaptação nova: T-ABC (defaults 80/95 · D-040), T-ACUM, T-RANK (default 3 níveis · D-041), T-AGRUPA, T-PIVOT (extensão multi-medida · D-039 quando POR_LINHAS), T-DIAG, T-MODELO (base padrão D-030 + extensão cross-visão acima).

## 16. Dependências para Fase 2 (S-V10)

Spec da V10 da Fase 2 precisará detalhar:

- Layout concreto das 4 etapas no Streamlit (wireframe funcional).
- Tipografia, cores, espaçamento do disclosure Vitais/Demais.
- Implementação da Curva Pareto na tela (Plotly ou Altair, provavelmente).
- UX exato do diálogo de aplicação de modelo cross-visão.
- Interação com filtros pós-execução do padrão Fundação.
- Comportamento em responsividade (tela pequena).

## 17. Síntese normativa da visão

A V10 é view especializada sobre V4 Modo 2 que responde à pergunta Pareto — "quais poucos itens concentram a maior parte do valor". Não tem motor próprio; consome a mesma lógica da V4 com preset de parâmetros, apresentação dicotômica (Vitais × Demais) e visualização Pareto dedicada. Preserva identidade de produto sem duplicar implementação.

Honra integralmente C.5: toda simplificação é declarada (nenhum item escondido, disclosure em vez de filtro, microcopy explícito sobre limiar B oculto, pontes para V4 Modo 2/Modo 3 e V6 onde outras visões são mais adequadas). Default declarado aplicado sistematicamente em limiar A, cardinalidade visual, faixas de leitura de síntese.

Estabelece padrão de modelo compartilhado entre visões do par (CONTEXT §13.4), reutilizável para Família A (V2 ↔ V1) no futuro.

---

## Apêndice A · Pendências resolvidas nesta sessão

| Pendência | Título | Resolução |
|---|---|---|
| P-V10-01 | Escopo pós-D-035 | Opção B · view especializada com identidade de produto |
| P-V10-02 | Preset de limiares | Opção B · T-ABC 80/95 internamente; UI colapsa B+C em "Demais itens" |
| P-V10-03 | Entrada simplificada | Opção B · 4 etapas (fusão E2+E3 de V4) |
| P-V10-04 | Escopo de medidas | Opção A · exatamente 1 medida; ponte para V4 Modo 3 |
| P-V10-05 | Filtro visual Classe A | Opção C · disclosure Vitais/Demais; nada escondido |
| P-V10-06 | Visualização Pareto | Curva clássica no topo; cardinalidade 50 configurável; tooltip |
| P-V10-07 | Microcopy dedicado | 6 peças consolidadas |
| P-V10-08 | Resumo Executivo | 6 blocos herdados + leitura secundária "Corte" V10-nova |
| P-V10-09 | Exportação Excel | 6 abas: Resumo · Análise · Curva Pareto (gráfico nativo) · Base · Parâmetros · Diagnóstico |
| P-V10-10 | T-MODELO | Compartilhamento cross-visão V4 Modo 2 ↔ V10 com mapeamento declarado — padrão transversal §13.4 |

## Apêndice B · Pendências para refino futuro (Fase 2)

Nenhuma pendência estrutural aberta. Detalhes de implementação (layout, tipografia, interações visuais, tecnologia do gráfico na tela) ficam para Spec da Fase 2 S-V10.
