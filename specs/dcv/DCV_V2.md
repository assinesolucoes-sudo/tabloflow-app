# DCV-V2 — Análise Comparativa entre Referências

**Visão:** V2 · Família A · Confronto entre universos
**Status:** ✅ Aprovado pela Usuária em 18/04/2026 (Sessão 1 do DCV-V2)
**Histórico:** Refinado em sessão única com 13 pendências fechadas (P-V2-01 a P-V2-13). Decisões transversais associadas: D-021 a D-032. Reversões justificadas: D-001, D-002, D-004 (todas pelo Princípio C.5).

---

## 1. O que a visão faz

A V2 compara dois recortes do mesmo dado e responde: **o que mudou, quanto mudou e como interpretar a mudança no negócio**. A Usuária indica qual é a Origem (referência inicial) e qual é o Comparado (referência seguinte ou paralela), escolhe os agrupadores que definem o nível da análise, e a V2 entrega uma leitura estruturada com diferença, variação percentual e classificação automática para cada combinação.

A comparação é entre **dois estados fixos**, não uma série temporal. Para análise ao longo de eixo ordenado (mês a mês, etapa a etapa), use a V3. Para conciliar duas bases distintas registro a registro, use a V1. Para participação ou Pareto, V4 ou V10.

A V2 se distingue da V1 por operar sobre **uma única base lógica** com dois recortes — não duas bases distintas. Não usa T-DUAL.

## 2. Quando usar

- **Orçado vs Realizado** — quanto cada filial ficou acima ou abaixo do orçamento.
- **Antes vs Depois** — impacto de uma mudança operacional comparando o mesmo período em estados diferentes.
- **Meta vs Resultado** — atingimento por área, produto ou cliente.
- **Mês A vs Mês B** — variação entre dois períodos específicos sem precisar acompanhar a sequência inteira.
- **Filial X vs Filial Y** — confronto entre duas unidades sobre os mesmos KPIs.

## 3. O que a visão precisa receber

### 3.1 Estrutura de entrada

Uma base lógica por execução. Pode ter múltiplas abas; usuário escolhe uma. Não há cruzamento entre abas na V2.

Formatos aceitos:
- **POR_COLUNAS** — os dois estados estão em colunas distintas da mesma base (ex: `Receita_Orcado` e `Receita_Realizado`).
- **POR_LINHAS** — os estados aparecem como valores de uma coluna discriminadora (ex: coluna `Cenario` com valores `"Orcado"` e `"Realizado"`).

Em POR_LINHAS, se a coluna discriminadora tem mais de 2 valores únicos (Modo 4), a V2 pede ao usuário para escolher quais 2 valores comparar antes de processar (D-026).

### 3.2 Tipos de campo

A V2 trabalha com **4 tipos de campo** (D-025), cada um com comportamento específico de cálculo e consolidação:

| Tipo | Cálculo | Consolidação por agrupador | Exemplos |
|---|---|---|---|
| **Numérico aditivo** | Diferença e variação % | Soma (default), via T-AGRUPA configurável (média, máx, mín, contagem) | Receita, custo, quantidade, volume, dias trabalhados, headcount acumulado |
| **Numérico relativo** | Diferença e variação % | **Default declarado**: média simples, com opção de média ponderada por campo ou não consolidar (D-024) | Margem %, taxa de conversão, índice de eficiência, NPS, score |
| **Numérico não-aditivo** | Diferença e variação % | **Default declarado**: média simples, com opção de média ponderada ou não consolidar | Estoque pontual, saldo bancário, headcount em data específica, preço unitário |
| **Estado/Situação** | Sem aritmética; comparação textual ("mudou" / "manteve") | Contagem por categoria | Status de pedido, categoria de produto, classificação manual |

### 3.3 Configuração que o usuário declara

Em sequência (ver §6 sobre etapas progressivas):

**Obrigatório:**
- Estrutura de entrada (POR_COLUNAS / POR_LINHAS)
- Origem ("Comparar de") e Comparado ("Comparar com"), com rótulos amigáveis editáveis
- Campo a analisar e seu tipo (D-025)
- Semântica do campo (maior é melhor / menor é melhor / neutro)
- Agrupadores (1 a 9, conforme limite progressivo D-027)
- Regra de agregação (T-AGRUPA: soma default, configurável)
- Para tipos numérico relativo e não-aditivo: método de consolidação (D-024)

**Condicional (só aparece quando aciona):**
- Em Modo 4: seleção de 2 estados entre N (D-026)
- Resolução de caso estrutural quando motor detecta divergência (D-021)

## 4. O que a visão entrega

### 4.1 Granularidade do resultado

Uma linha por combinação única de agrupadores. Cada linha contém:

- Valor da Origem
- Valor do Comparado
- Diferença (Comparado − Origem)
- Variação percentual
- **Classificação estrutural** (6 categorias mutuamente exclusivas):
  - `PRESENTE_AMBOS` — registro existe e tem valor em ambos os lados
  - `AUSENTE_ORIGEM` — chave de agrupamento existe só no Comparado (D-022)
  - `AUSENTE_COMPARADO` — chave de agrupamento existe só na Origem (D-022)
  - `NULO_ORIGEM` — chave existe em ambos, valor nulo na Origem (D-023)
  - `NULO_COMPARADO` — chave existe em ambos, valor nulo no Comparado (D-023)
  - `NULO_AMBOS` — chave existe em ambos, valor nulo em ambos
- **Classificação semântica** (apenas tipos numéricos): Positivo / Negativo / Neutro / Não aplicável
- **Flags** de qualidade (warnings disparados para esta linha)

### 4.2 Vocabulário dual

A V2 mantém separação rigorosa entre **contrato técnico** (motor, código, exportação Excel coluna técnica) e **exibição ao usuário** (Resumo Executivo, gráficos, microanálise):

| Contrato técnico | Exibição ao usuário |
|---|---|
| `AUSENTE_ORIGEM` | "Apareceu no Comparado" |
| `AUSENTE_COMPARADO` | "Saiu / Não está no Comparado" |
| `PRESENTE_AMBOS` | (omitido — caso normal) |
| `NULO_ORIGEM` | "Valor nulo na Origem" |
| `NULO_COMPARADO` | "Valor nulo no Comparado" |
| `NULO_AMBOS` | "Valor nulo em ambos" |

Na exibição: `None` por nulo aparece como "—" ou "(nulo)"; `None` por ausência aparece como "(não consta)". Esta separação é princípio de design da V2 herdado da V1.

### 4.3 Tratamento de cálculos

| Situação | valor_origem | valor_comparado | diferença | variacao_percentual | classificacao |
|---|---|---|---|---|---|
| PRESENTE_AMBOS, Origem ≠ 0 | a | b | b−a | (b−a)/a | normal |
| PRESENTE_AMBOS, Origem=0 e Comparado≠0 | 0 | b | b | `None` | dispara W-V2-BZ |
| PRESENTE_AMBOS, ambos = 0 | 0 | 0 | 0 | `0.0` | normal |
| AUSENTE_ORIGEM | `None` | b | `None` | `None` | — |
| AUSENTE_COMPARADO | a | `None` | `None` | `None` | — |
| NULO_ORIGEM | `None` | b | `None` | `None` | — |
| NULO_COMPARADO | a | `None` | `None` | `None` | — |
| NULO_AMBOS | `None` | `None` | `None` | `None` | — |

**Princípios:**
- **D-022** reverte D-001: ausência produz `None`, não 0/-100%. Inventar valor onde não há dado viola C.5.
- **D-023** reverte D-004: nulo no campo permanece no resultado com classificação visível, não é excluído.
- **D-003 confirmada (P-V2-04):** contrato preserva precisão total (float Python nativo). Arredondamento é responsabilidade da camada de exibição (Streamlit, Excel) — 2 casas decimais no Resumo Executivo, formato `0.00%` no Excel com valor completo na célula.

### 4.4 Tratamento de nulo em agrupador

Quando o agrupador tem valor nulo em alguma linha (ex: coluna "Filial" vazia), a linha **entra na análise** sob rótulo `(sem valor)` para aquele agrupador (D-023). Isso preserva o dado e torna o nulo visível e separável, sem inventar valor para o agrupador.

## 5. Regras estruturais

### 5.1 Comparação sempre entre dois estados fixos

Exatamente 2 estados por execução. Em POR_LINHAS Modo 4 (>2 valores únicos), motor pede escolha do usuário com:

- Ordenação inteligente da lista (numérico crescente · cronológica para datas e períodos pt-BR/pt-EN reconhecíveis · alfabética crescente como fallback)
- Default declarado: extremos (primeiro e último na ordenação aplicada)
- Estados não escolhidos: excluídos do MotorResult, registrados no Diagnóstico
- Limite operacional: ≥51 valores dispara W-V2-NMANY com sugestão de filtro prévio; ≤1 valor dispara erro (W-V2-N1, W-V2-N0)

### 5.2 Ordem dos estados

| UX | Motor | Fórmula |
|---|---|---|
| "Comparar de" | Origem | Δ = Comparado − Origem |
| "Comparar com" | Comparado | Δ% = (Comparado − Origem) ÷ Origem |

Vocabulário fixo. Origem/Comparado é vocabulário técnico do motor; "Comparar de"/"Comparar com" é vocabulário UX.

### 5.3 Consolidação obrigatória antes de comparar

Unidade da análise: **agrupadores + estado**. Regra: consolidar primeiro, comparar depois.

T-AGRUPA (transversal da Fundação) faz a consolidação. Para tipos numérico aditivo: regra de agregação configurável (soma default). Para tipos numérico relativo e não-aditivo: ver §3.3 (D-024 — default declarado entre média simples, ponderada ou não consolidar).

### 5.4 Limite de agrupadores (D-027)

Limite progressivo, não trava rígida:

| N° agrupadores | Comportamento |
|---|---|
| 1-3 | Normal, sem aviso |
| 4-5 | Aviso visível com estimativa de linhas |
| 6-8 | Confirmação obrigatória extra com checkbox "entendo o impacto" |
| 9+ | Bloqueio com mensagem clara + sugestão de V6 (Relacionamento entre Dimensões) + opção "remover agrupadores" |

Estimativa de linhas (cardinalidade × cardinalidade × ...) calculada em tempo real conforme usuário adiciona/remove agrupadores. W-V2-AGRUP-MUITOS dispara para ≥6 agrupadores efetivamente usados.

### 5.5 Inconsistência estrutural entre Origem e Comparado (D-021)

A V2 distingue dois tipos de inconsistência, com tratamento diferente:

**Inconsistências leves** (4 casos taxativos): motor ajusta sem perguntar e registra no Diagnóstico como `AJUSTE_LEVE`:
1. Diferença de ordem de colunas entre Origem e Comparado
2. Espaços, acentos ou case diferente em nomes de coluna ou em valores categóricos quando o conteúdo é idêntico após normalização
3. Tipos numéricos compatíveis (int/float, mesma escala)
4. Linhas em branco ou nulos isolados dentro de uma coluna

**Inconsistências estruturais** (tudo o mais): motor para no fim da Etapa 4 e abre painel de resolução com opções específicas ao caso. Usuário escolhe → escolha vai para a Aba 4 Parâmetros como configuração explícita → motor executa → Diagnóstico registra como `DECISAO_USUARIO`. Casos típicos:
- Nível de agrupamento diferente entre Origem e Comparado
- Coluna presente em uma base e ausente na outra
- Tipo de campo incompatível
- Valor único da coluna discriminadora (POR_LINHAS) divergente entre o que o usuário escolheu e o que existe na base
- Ordem de magnitude radicalmente diferente entre estados (sugestão de unidade incompatível)

A V2 abandona o padrão "ajusta cedo, evidencia tarde" do prévio original — viola C.5 porque a decisão analítica (qual nível consolidar) acontece silenciosamente antes de o usuário poder reverter sem refazer a análise.

### 5.6 Agrupador vs Filtro

- **Agrupador** define a estrutura da análise (uma linha de saída por combinação).
- **Filtro** é recorte de visualização aplicado no Excel pós-execução, não muda a análise.

Filtro não entra na configuração da V2. Excel exporta com filtros ativos em todas as abas; usuário aplica como quiser.

## 6. Etapas progressivas (D-029)

A V2 organiza a configuração em **5 etapas sequenciais** + **1 bloco intermediário condicional**. Mecânica progressiva (CONTEXT §13.2): etapa N só fica disponível quando N-1 está concluída; usuário pode voltar para editar etapa anterior; sistema avisa impacto nas etapas seguintes ao editar; etapas concluídas mostram resumo compacto.

### Etapa 1 — Origem dos dados

**Ações do usuário:** subir arquivo (Excel ou CSV) e, se Excel multi-aba, escolher a aba.

**Validações automáticas:** arquivo legível, formato suportado, tem dado mínimo.

**Resumo ao concluir:** "Arquivo: [nome] · Aba: [nome] · [N] linhas detectadas"

**Invalidação:** mudar arquivo ou aba invalida E2-E5.

### Etapa 2 — Estrutura da comparação

**Ações do usuário:** indicar POR_COLUNAS ou POR_LINHAS; em POR_LINHAS escolher coluna discriminadora; em Modo 4 escolher 2 valores entre N; em POR_COLUNAS escolher 2 colunas como Origem e Comparado; definir rótulos amigáveis para Origem/Comparado.

**Resumo:** "Comparar de: [rótulo] · Comparar com: [rótulo] · Estrutura: [tipo] [+ Modo 4 se aplicável]"

**Invalidação:** mudar estrutura ou Origem/Comparado invalida E3-E5.

### Etapa 3 — O que comparar

**Ações do usuário:** escolher campo a analisar; escolher tipo (D-025); definir semântica; se tipo é numérico relativo ou não-aditivo, escolher método de consolidação (D-024 — default declarado); se tipo é Estado/Situação, fluxo simplificado sem semântica nem consolidação numérica.

**Resumo:** "Campo: [nome] · Tipo: [tipo] · Semântica: [direção] · Consolidação: [método se aplicável]"

**Invalidação:** mudar campo ou tipo invalida E4-E5.

### Etapa 4 — Como agrupar

**Ações do usuário:** selecionar agrupadores (1-9, D-027); escolher regra de agregação (T-AGRUPA); ver estimativa de linhas em tempo real; em zona 4-5 ler aviso simples; em zona 6-8 marcar checkbox de confirmação obrigatória.

**Resumo:** "Agrupadores: [lista] · Agregação: [método] · Estimativa: [N] linhas"

**Invalidação:** mudar agrupadores ou agregação invalida E5.

### Bloco intermediário — Resolução de casos estruturais

**Quando aparece:** durante transição E4 → E5, motor analisa as bases conforme configuração e detecta inconsistência estrutural não-leve (D-021).

**Ações do usuário:** ler o caso detectado; escolher entre as opções específicas oferecidas pelo motor; confirmar.

**Resumo:** "Caso estrutural [tipo] resolvido: [escolha do usuário]"

Se nenhum caso estrutural detectado, este bloco não aparece.

### Etapa 5 — Revisão e execução

**Ações do usuário:** ver preview compacto da configuração completa (resumo das E1-E4 + bloco de resolução se houve); navegar entre etapas pelo stepper se quiser editar; confirmar e processar; aguardar execução; receber resultado.

**Estado preservado** em mudanças (não obriga redigitar campos não afetados quando uma etapa anterior é editada).

## 7. Modelo de configuração — T-MODELO (D-030)

Toda execução da V2 pode ser salva como modelo reutilizável.

**O que persiste no modelo:**
- Identificação: nome (obrigatório), descrição (opcional), data de criação, data de última aplicação
- Etapa 2: tipo de estrutura, nome da coluna discriminadora (POR_LINHAS), rótulos amigáveis, valores escolhidos em Modo 4
- Etapa 3: nome do campo, tipo, semântica, método de consolidação, campo de peso (se média ponderada)
- Etapa 4: lista ordenada de agrupadores, regra de agregação
- Bloco intermediário: decisão de resolução estrutural se houve

**O que NÃO persiste:**
- Arquivo bruto, nome do arquivo
- Aba selecionada (vai vir do novo upload)
- Filtros aplicados no Excel pós-execução
- Resultado da análise anterior

**Aplicação em nova base:**
1. Usuária sobe nova base, escolhe aba
2. Sistema tenta casar nomes salvos com colunas da nova base
3. Se todos casam: E2-E4 pré-preenchidas, usuária avança direto para E5
4. Se algum não casa: aviso "Modelo aplicou parcialmente, ajustar manualmente"
5. Se estrutura incompatível: avisa, zera etapas dependentes, usuária começa da E2

Diagnóstico registra: "Modelo aplicado: [nome] · Campos casados: [N/total] · Ajustes manuais: [lista]"

Honra C.5: modelo persiste só o que a usuária declarou; aplicação não decide silenciosamente — divergência vira ajuste manual; aba 4 Parâmetros do Excel sempre registra o estado efetivo da execução, não o original do modelo.

## 8. Exportação Excel

5 abas obrigatórias, em ordem fixa, com filtros ativos em todas. Diagnóstico **sempre como última aba** (regra transversal D-017 aplicada via T-DIAG).

### Aba 1 — Resumo Executivo (D-031)

6 blocos fixos em ordem de leitura:

1. **Cabeçalho da análise** — título amigável "Comparação: [rótulo Origem] vs [rótulo Comparado]"; campo analisado (nome + tipo + semântica); agrupadores aplicados; data e hora de processamento.

2. **Números-âncora** — 4 KPIs em destaque: Total Origem, Total Comparado, Diferença total, Variação total % (com cor verde/vermelho/cinza pela semântica). Para tipo Estado/Situação, vira: total de combinações analisadas, combinações com mudança, combinações estáveis, % de mudança.

3. **Distribuição de classificações estruturais** — contagem das 6 categorias do contrato. Categorias com 0 registros são omitidas da exibição (mas existem no contrato).

4. **Maiores variações** — top 10 combinações com maior |Δ|. Para Estado/Situação: top 10 combinações que mudaram, com "antes" e "depois".

5. **Distribuição de comportamento (semântica aplicada)** — apenas tipos numéricos: Positivo / Negativo / Neutro / Não aplicável. Limiar de estabilidade default ±1% (configurável em versão futura). Para Estado/Situação: lista das categorias mais afetadas pelas mudanças.

6. **Qualidade estrutural** — resumo executivo do que aparece detalhado no Diagnóstico: casos estruturais resolvidos, ajustes leves, warnings disparados com contagem.

### Aba 2 — Análise Comparativa

Visão principal: uma linha por combinação de agrupadores. Colunas: agrupadores · valor Origem · valor Comparado · diferença · variação % · classificação estrutural · classificação semântica · flags.

Ordenação default: maior impacto (|Δ|). Usuária pode alterar.

### Aba 3 — Base Analítica

Base consolidada usada no cálculo (após T-AGRUPA aplicada), com rastreabilidade.

### Aba 4 — Parâmetros

Toda configuração aplicada na execução: arquivo, aba, estrutura, Origem, Comparado (rótulos e valores), Modo 4 se houve, campo, tipo, semântica, método de consolidação, agrupadores, regra de agregação, decisão de resolução estrutural se houve, modelo aplicado se houve.

### Aba 5 — Diagnóstico da Estrutura

**Última aba do Excel** (regra transversal D-017). Para cada inconsistência ou ajuste:
- Tipo (`AJUSTE_LEVE` ou `DECISAO_USUARIO`)
- Onde ocorreu (etapa, campo, agrupador)
- Ação aplicada
- Impacto
- Volume afetado

Blocos adicionais:
- Nulos no campo analisado (contagem por classificação NULO_*)
- Nulos em agrupadores (contagem por agrupador)
- Estados disponíveis vs comparados (Modo 4)
- Modelo aplicado se houve
- Tempo de processamento por etapa

## 9. Vocabulário de warnings

Catálogo da V2 (12 warnings + heranças):

| Código | Quando dispara | Contexto |
|---|---|---|
| **W-V2-EST** | ≥1 registro com classificação AUSENTE_* | Contagem detalhada por agrupador no Diagnóstico (substitui W06 antiga) |
| **W-V2-BZ** | ≥1 registro PRESENTE_AMBOS com Origem=0 e Comparado≠0 | Variação não calculável (base zero) |
| **W-V2-NULL** | ≥1 registro com classificação NULO_* | Contagem por categoria + lista por agrupador (substitui W01 antiga) |
| **W-V2-NULL-MASS** | >20% dos registros do campo analisado têm nulo | Sinaliza qualidade de dado deteriorada |
| **W-V2-AGG** | Tipo numérico relativo ou não-aditivo + agrupadores | Informativa: registra método de consolidação aplicado (substitui W07 antiga, agora informativa não alerta de surpresa) |
| **W-V2-MIX** | Coluna discriminadora POR_LINHAS com tipos mistos | Motor caiu em ordenação alfabética; pede revisão da base |
| **W-V2-NMANY** | Coluna discriminadora com >50 valores | Sugere filtragem prévia |
| **W-V2-N1** | Coluna discriminadora com 1 valor único | Erro: impossível comparar |
| **W-V2-N0** | Coluna discriminadora vazia | Erro: estrutura inválida |
| **W-V2-AGRUP-MUITOS** | ≥6 agrupadores efetivamente usados | Confirma escolha de granularidade fina |
| **W-V2-MOD-PARCIAL** | Modelo aplicado mas algum campo não casou | Lista campos não-casados |
| **W-V2-MOD-INCOMP** | Modelo aplicado mas estrutura incompatível com nova base | Etapas dependentes zeradas |

## 10. Bloqueios operacionais (D-032)

Casos que param execução independentemente de decisão da usuária. Sempre com mensagem clara + sugestão de próximo passo:

1. Arquivo ilegível ou corrompido
2. Estrutura inválida: arquivo vazio, aba sem dado, sem coluna numérica detectada quando esperada
3. Coluna discriminadora POR_LINHAS com 0 ou 1 valor único (W-V2-N0, W-V2-N1)
4. Campo analisado com 100% de nulos em Origem ou Comparado
5. Mais de 9 agrupadores declarados (D-027)
6. Pesos todos zerados ou negativos quando média ponderada escolhida (D-024)
7. Falha estrutural não-recuperável detectada na transição E4→E5
8. Análise gera mais de 500.000 linhas no resultado (limite operacional)

Bloqueios são **operacionais** (proteção do sistema), não analíticos. Honra C.5 porque motor explica o motivo e sugere caminho — não decide por outro caminho silenciosamente.

## 11. Diretrizes de performance para a Fundação

Não trava no DCV-V2; informa requisitos do G-FUND e F-MOT:

1. Leitura de arquivo: stream/chunked quando possível
2. Pivot/merge: índices pandas eficientes; outer join obrigatório (P-V2-02) otimizado
3. Estimativa de linhas (D-027): cardinalidades multiplicadas, não produto cartesiano real
4. Cálculos vetorizados (numpy), nunca loop linha-a-linha
5. Cache de execução por hash de configuração + base — mecânica fica para Fundação
6. Limite operacional de 500K linhas no resultado (item 8 dos bloqueios)
7. Diagnóstico inclui métricas de tempo por etapa do motor

## 12. Transversais consumidos

A V2 consome os seguintes transversais da Fundação (ver CONTEXT §6):

- **T-AGRUPA** — consolidação obrigatória pré-comparação
- **T-DIAG** — Diagnóstico estrutural obrigatório, sempre como última aba do Excel (D-017)
- **T-SEMA** — semântica maior/menor é melhor / neutro
- **T-PIVOT** — pivot POR_LINHAS → POR_COLUNAS, com parâmetro de "valores selecionados" (requisito propagado por D-026)
- **T-MODELO** — salvar/aplicar configuração como modelo reutilizável (D-030)

A V2 **não** consome T-EIXO, T-RANK, T-ACUM, T-ABC, T-DUAL.

## 13. Requisitos propagados para o G-FUND

Esta visão antecipa para a Fundação os seguintes requisitos:

1. **motor_upload** identifica padrões cronológicos pt-BR e pt-EN para ordenação inteligente em Modo 4 (D-026)
2. **T-PIVOT** aceita parâmetro "valores selecionados da coluna discriminadora" (D-026)
3. **T-AGRUPA** suporta 5 regras de agregação: soma, média, máximo, mínimo, contagem
4. **T-DIAG** suporta categorias `AJUSTE_LEVE` e `DECISAO_USUARIO` (D-021)
5. **Estimativa de cardinalidade** sem materialização do produto cartesiano (D-027)
6. **T-MODELO** persiste apenas configuração lógica, não dado fonte (D-030)
7. **Limite operacional de linhas** no resultado configurável (default 500K, D-032)

## 14. Pendências fechadas (resumo cronológico)

| ID | Tema | Decisão D-XXX |
|---|---|---|
| P-V2-01 | Inconsistência estrutural Origem×Comparado | D-021 (transversal: leve vs estrutural) |
| P-V2-02 | Registros sem par (POR_LINHAS) | D-022 (reverte D-001: None em vez de 0/-100%) |
| P-V2-03 | Nulo no campo e em agrupador | D-023 (reverte D-004: NULO_* visível, `(sem valor)` em agrupador) |
| P-V2-04 | Arredondamento variacao_percentual | D-003 confirmada (contrato sem arredondamento) |
| P-V2-05 | Consolidação PERCENTUAL/INDICE | D-024 (revoga D-002: 3 opções declaradas) |
| P-V2-06 | Tipos de campo | D-025 (4 tipos: aditivo, relativo, não-aditivo, estado) |
| P-V2-07 | Modo 4 (POR_LINHAS >2 estados) | D-026 (ordenação + default extremos + 4 warnings) |
| P-V2-08 | Limite de agrupadores | D-027 (progressivo 1-3/4-5/6-8/9+) |
| P-V2-09 | Objetivo da Visão V2 | D-028 (4 seções de conteúdo canônico) |
| P-V2-10 | Etapas progressivas | D-029 (5 etapas + bloco intermediário condicional) |
| P-V2-11 | Modelo de configuração | D-030 (persiste lógica, não dado) |
| P-V2-12 | Conteúdo do Resumo Executivo | D-031 (6 blocos fixos) |
| P-V2-13 | Bloqueios e performance | D-032 (8 bloqueios + 7 diretrizes performance) |

**Pendências do prévio absorvidas sem virar P-V2:**
- P-02 prévio (lista de métodos de agregação) → absorvida por T-AGRUPA já definida em CONTEXT §6
- P-03 prévio (severidade visual no diagnóstico) → fica para Spec, não é decisão de DCV
- P-05 prévio (UX da ordenação) → fica para Spec
- P-06 prévio (diagnóstico como transversal) → já decidido por D-017

**Observação operacional:** o trecho final do prévio que mencionava "Wireframe Figma da V1" foi engano de redação (copy/paste de template). Wireframe estrutural da V2 será produzido na Fase 2 (bloco S-V2), conforme princípio B.2 do CONTEXT.

## 15. Pendências abertas remanescentes (não bloqueiam)

- **P-V2-old-03** (limite de 10 campos comparados) — herdada da spec antiga, ainda em aberto na planilha aba 5. Não bloqueia implementação inicial; validar com usuárias reais quando V2 chegar à Fase 2.

---

**Aprovado pela Usuária em 18/04/2026.** Próximo bloco: DCV-V3 (Sessão 1).
