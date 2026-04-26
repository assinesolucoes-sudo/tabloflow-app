# MOCKUP-V1 · Conciliação de Bases · α.2

**Sessão:** Mockup-V1 modalidade β.3 (D-203 · gate D-204 cláusula A)
**Data:** 2026-04-26 noite · Sessão Promoção D-202 ✅ concluída
**Status:** α.2 · detalhamento técnico do Arquiteto · aguarda α.3 (aprovação Elaine)

**Cenário 3 declarado:** Elaine passou autonomia para o Arquiteto detalhar Q-A · Q-B · Q-C · Q5 num pacote único. Reação em α.3 cobre o pacote inteiro.

---

## Decisões absorvidas em α.1'

| Pergunta | Resposta | Implicação |
|---|---|---|
| Q1 · Coração Visual | Sem aba/seção dedicada · distribuído | Mapa de Conciliação (aba 3) e Ponte (aba 5) carregam o peso visual |
| Q2 · Resumo Executivo | Mantém 7 seções · reordena | Vira 9 seções com 2 ajustes (Status Ponte sobe · Síntese isola) |
| Q3 · Ponte no Resumo | Sim · síntese compacta + status | Seção 4 do Resumo é Status da Ponte |
| Q4 · Aba 3 | Mapa de Conciliação · todos os registros + classificação | Filtro substitui aba "Divergências" antiga |

Q-A · Q-B · Q-C · Q5 · detalhados pelo Arquiteto neste documento.

---

## 1 · Pegada V2 que se mantém em V1

V1 herda **literalmente** os seguintes elementos visuais e estruturais da V2 atual (pós-Promoção D-202):

### 1.1 · Paleta canônica

- **Default:** Azul executivo (paleta 1 da F-APRESENT capability 1 · D-164)
- 4 paletas alternativas disponíveis (Azul · Verde · Cinza · Vinho executivo) · Usuária escolhe na configuração
- Cor primária = cabeçalhos de seção · cor secundária = zebra · cor de borda = tom escuro da primária

### 1.2 · Estrutura visual de aba bespoke

- Título da aba escrito em A1 com `escrever_titulo_aba` (capability F-APRESENT)
- Subtítulo (timestamp) em A2 · cor secundária discreta
- Cabeçalhos de seção via `_renderizar_cabecalho_secao` · banner colorido cor primária · texto branco
- Cards lado a lado via `_mesclar_card` · 4 cards típicos · bordas finas · rótulo em cima · valor grande embaixo
- Bordas finas via `_bordas_finas(paleta)` · cor de borda escura
- Auto-fit de larguras via `_ajustar_larguras` · min 12 · max 50 · ignora ranges mesclados (regra herdada da Sessão 8.2)
- Linhas de respiro entre seções · altura 8 ou 10
- `sheet_view.showGridLines = False` em abas bespoke

### 1.3 · Estrutura visual de aba tabular

- ListObject Excel nativo via `criar_tabela_executiva` (capability 3 F-APRESENT)
- TotalsRow ativada com fórmulas SUBTOTAL
- TotalsRow herda number_format das células de dados (decisão CO-3/CO-4 do COMENTARIOS_ORFAOS · candidata a D-XXX retroativo · em V1 já vai canônica)
- Zebra automática · cor secundária da paleta
- AutoFilter ativo na header row
- Formato condicional opcional na coluna de variação (semáforo Verde-Amarelo-Vermelho por threshold semântico)

### 1.4 · Vocabulário bilingue · Bloco 1.1

V1 usa o par universal Família A:
- `Origem` (técnico) → "Origem" user-facing · com rótulo amigável editável (default vazio)
- `Comparado` (técnico) → "Comparado" user-facing · com rótulo amigável editável (default vazio)
- Quando rótulo amigável existe (ex: "Razão" e "Balancete") · ele substitui em **toda superfície visível**

Em V1 isto é **sempre relevante** · conciliação tipicamente tem rótulos materiais ("Sistema A" × "Sistema B" · "Razão" × "Balancete" · "ERP" × "Data Warehouse").

### 1.5 · Formatação numérica adaptativa (capability 11 · D-205)

V1 consome `formato_adaptativo_por_unidade` em **todas as colunas de valor**. Tabela default D-205:

| Unidade | Casas decimais | Regra adaptativa | Nota técnica |
|---|---|---|---|
| MONETARIO_BRL | 2 (R$ 1.234,56) | nunca muda | só se Δ centavos for material em % |
| PERCENTUAL | 2 (12,34%) | nunca muda | nunca |
| QUANTIDADE | 0 (1.234) | fração ≥0,5 → 1 casa decimal | variação ≥5% e arredondados iguais |
| TEMPO_DIAS | 0 (5d) | fração → 1 casa decimal | mesma QUANTIDADE |
| TEMPO_HORAS | 0 (5h) | fração → 1 casa decimal | mesma QUANTIDADE |
| MULTIPLICADOR | 2 (2,50×) | nunca muda | extremos |
| RAZAO | 4 (0,1234) | nunca muda | nunca |
| ADIMENSIONAL | 2 | nunca muda | nunca |

Para V1 · unidade default tipicamente **MONETARIO_BRL** (conciliação contábil · auditoria · banco) · mas TODAS as 8 unidades devem funcionar (V1 é Família A · contrato C.D8 universal).

### 1.6 · Leitura qualitativa parametrizada

V2 fecha o Resumo Executivo com leitura qualitativa de prosa (função `_construir_leitura_qualitativa_v2` promovida em D-202 etapa 6 para `apresentacao/templates/familia_a/leitura_qualitativa.py`). V1 herda o **padrão** mas ganha conteúdo próprio · ver §3.5.

---

## 2 · Estrutura macro de 6 abas confirmada

| # | Nome user-facing | Natureza | Contexto V1-específico |
|---|---|---|---|
| 1 | Resumo Executivo | Bespoke · narrativa · 9 seções | Cliente bate o olho · KPI primário Taxa de Conciliação |
| 2 | Resumo por Agrupador | Tabular (ListObject) · **condicional** | Aparece só quando agrupador executivo configurado · D-V1-GRU |
| 3 | Mapa de Conciliação | Tabular (ListObject) · **todos os registros** | 1 linha por registro · classificação como coluna · filtro padrão |
| 4 | Análise Analítica | Tabular (ListObject) · **detalhe por campo** | 1 linha por registro · cada campo comparado em colunas (Origem · Comparado · Diferença · Status) |
| 5 | Ponte de Conciliação | Bespoke · decomposição matemática | Saldo Origem → ajustes → Saldo Comparado · status binário · explica diferença |
| 6 | Diagnóstico | Bespoke · 6 seções | Configuração · warnings · totais técnicos · auditoria · TED |

**Ordem é fixa** · não muda em runtime (mesmo se a Aba 2 for omitida por não-configuração · as outras seguem sequência).

**Aba 2 condicional:** quando agrupadores do Resumo Executivo não foram configurados · aba não é criada · ordem das demais não muda · Aba 3 segue sendo "Mapa de Conciliação".

**Q-C resolvida (distinção Mapa × Análise Analítica):**

A diferença é de **grão por coluna** · não de grão por linha:

- **Aba 3 · Mapa** · 1 linha por registro · colunas = identificadores + Classificação + 1 coluna consolidada por campo (Diferença total) · grão de leitura macro · filtro "Classificação" é a chave de uso · cliente vê 1000 registros · filtra "Divergente por valor" · vê 47 · vai pra ação
- **Aba 4 · Análise Analítica** · 1 linha por registro · colunas = identificadores + **expansão por campo comparado** (Valor Origem · Valor Comparado · Diferença · Status do campo) × N campos · grão de leitura por campo · cliente abre essa aba quando precisa entender porque um registro divergiu em qual campo específico

Não são redundantes · são duas leituras diferentes do mesmo conjunto. Mapa = "quais registros" · Análise = "em quais campos cada registro divergiu".

Detalhe: se a configuração tiver **só 1 campo comparado** · Aba 4 colapsa para 4 colunas extras (Valor Origem · Valor Comparado · Diferença · Status) e fica próxima do Mapa · mas ainda assim ela tem o **detalhamento por campo** que o Mapa não tem (Mapa usa Diferença consolidada). Em qualquer caso · as 2 abas continuam distinguíveis.

---

## 3 · Aba 1 · Resumo Executivo · 9 seções

Ordem definitiva pós-reordenação. Cada seção abaixo tem · linha por linha · o que aparece · com microcopy literal e formatação.

### 3.1 · Seção 1 · Cabeçalho identificador

**Ocupa:** A1:H4 (4 linhas)

**Linha A1:** título da aba
- Texto: `Conciliação de Bases · {origem_ux} × {comparado_ux}`
- Exemplo render: `Conciliação de Bases · Razão × Balancete`
- Cor de fundo · primária da paleta · texto branco · bold · altura 28
- Quando rótulo amigável vazio · cai para `Conciliação de Bases · Origem × Comparado`

**Linha A2:** subtítulo · cor secundária · texto cinza médio
- `Gerado em {DD/MM/AAAA} às {HH:MM}`
- Origem: Arquivo *{nome_arquivo_origem}* · Aba *{nome_aba_origem}*
- Comparado: Arquivo *{nome_arquivo_comparado}* · Aba *{nome_aba_comparado}*
- Quando estrutura B (1 arquivo · 2 abas) · linha única: `Arquivo *{nome_arquivo}* · Origem aba *{aba1}* · Comparado aba *{aba2}*`

**Linha A3:** modelo aplicado (se houver T-MODELO)
- `Modelo de configuração: *{nome_modelo}*` · texto cinza · pequeno
- Quando vazio · linha não aparece · seção tem 3 linhas em vez de 4

**Linha A4:** respiro · altura 8

### 3.2 · Seção 2 · Taxa de Conciliação · KPI primário

**Ocupa:** banner + número grande + tabela de decomposição

**Banner (1 linha):** `Taxa de Conciliação` · cabeçalho de seção via `_renderizar_cabecalho_secao`

**Card único centralizado (3 linhas):**
- Rótulo: `Taxa de Conciliação Geral`
- Valor: `87,3%` (formato adaptativo PERCENTUAL · 2 casas decimais · D-205)
- Subtexto: `1.247 de 1.428 registros conciliados`

**Tabela de decomposição (8 linhas com header):**

| Classificação | N registros | % do total |
|---|---:|---:|
| Conciliados | 1.247 | 87,3% |
| Divergentes por valor | 89 | 6,2% |
| Só na Origem (ex: "Saiu do Razão") | 47 | 3,3% |
| Só no Comparado (ex: "Apareceu no Balancete") | 32 | 2,2% |
| Divergência por duplicidade | 8 | 0,6% |
| Divergência por ambiguidade de match | 5 | 0,4% |
| **Total processado** | **1.428** | **100,0%** |

**Microcopy nas classificações** consome Bloco 3 do vocabulário bilingue (com substituição dinâmica por rótulo amigável quando declarado · D-167):
- `Só na Origem` ou `Saiu do {origem_ux}` quando rótulo amigável presente
- `Só no Comparado` ou `Apareceu no {comparado_ux}` quando rótulo amigável presente

**Sub-linha condicional** (quando há tolerância absorvida):
- `Dos 1.247 conciliados · 12 tiveram diferença absorvida pela tolerância (soma R$ 8,42)`
- Cor cinza · texto pequeno · só aparece quando aplicável

**Não há decomposição "match exato vs aproximado" no Resumo** (regra DCV-V1 · §6.2 seção 3 nota explícita) · esse detalhe vive no Diagnóstico.

### 3.3 · Seção 3 · Volumetria

**Ocupa:** banner + 3 cards lado a lado (mesmo padrão V2)

**Banner:** `Volumetria`

**3 cards** via `_mesclar_card`:
- Card 1: `Registros · {origem_ux}` · valor: `1.302` (QUANTIDADE adaptativa)
- Card 2: `Registros · {comparado_ux}` · valor: `1.287`
- Card 3: `Processados após match` · valor: `1.428`

**Nota:** "processados após match" pode ser maior que o maior dos dois (registros A + registros B - matches encontrados) · isso é informativo · a comparabilidade é com a Taxa de Conciliação acima.

### 3.4 · Seção 4 · Status da Ponte de Conciliação · NOVO em V1

**Ocupa:** banner + 1 linha grande de status

**Banner:** `Status da Ponte`

**1 linha de status grande** (altura 36 · centralizado · ícone+texto):
- **Caso "Fecha":** ✅ ` Ponte fecha em todos os campos comparados` · cor verde da paleta · bold
- **Caso "Resíduo":** ⚠️ `Resíduo de R$ 142,50 em 2 campo(s) · ver Aba 5 · Ponte de Conciliação` · cor amarela/vermelha · bold

**Sub-linha discreta** (cinza · texto pequeno):
- Quando "Fecha": `A diferença total entre {origem_ux} e {comparado_ux} é decomposta integralmente · ver Aba 5`
- Quando "Resíduo": `Resíduo é a diferença não atribuída aos registros divergentes · investigar na Aba 5`

**Decisão de microcopy:** cliente bate o olho · sabe se a conciliação fechou · sem precisar abrir a Aba 5. Esta é a "promoção" da Ponte que o esboço α.1 da Elaine pediu.

**Cores dos ícones** seguem semântica F-APRESENT (não usar emoji puro · usar ícones via formatação condicional + caractere Unicode com cor da paleta · padrão V2).

### 3.5 · Seção 5 · Valor financeiro por campo comparado

**Ocupa:** banner + tabela (1 linha por campo comparado · até 10 campos)

**Banner:** `Valor por campo comparado`

**Tabela** (header + N linhas):

| Campo | Soma · {origem_ux} | Soma · {comparado_ux} | Diferença líquida | Σ |Diferença| | Tolerância absorvida |
|---|---:|---:|---:|---:|---:|
| Valor Bruto | R$ 1.482.330,00 | R$ 1.481.987,50 | R$ 342,50 | R$ 845,30 | 12 reg · R$ 8,42 |
| Imposto | R$ 211.760,30 | R$ 211.760,30 | R$ 0,00 | R$ 0,00 | — |

**Formatação numérica adaptativa por unidade** · `Valor Bruto` em MONETARIO_BRL (2 casas) · campo de QUANTIDADE seria 0 casas com adaptação · etc. (D-205).

**Coluna "Tolerância absorvida"**: quando 0 · exibe `—` · quando há absorção · `N reg · R$ valor`.

**Microcopy do header**:
- `Diferença líquida` · em PERCENTUAL vira `Diferença em p.p.` (Bloco 10.2 vocabulário · variação_percentual_label)
- `Σ |Diferença|` · sempre técnico mas claro · texto pequeno entre parênteses do header pode ter `(soma absoluta · auditoria)` · TBD em α.3

### 3.6 · Seção 6 · Cobertura por base

**Ocupa:** banner + 2 cards lado a lado

**Banner:** `Cobertura por base`

**2 cards** via `_mesclar_card`:
- Card 1: `Cobertura · {origem_ux}` · valor: `1.255 de 1.302 (96,4%)`
- Card 2: `Cobertura · {comparado_ux}` · valor: `1.255 de 1.287 (97,5%)`

**Nota** (texto pequeno cinza abaixo dos cards):
- `Cobertura mede quantos registros de cada base encontraram par no match. Útil para auditoria assimétrica.`

### 3.7 · Seção 7 · Resumo por agrupador executivo · CONDICIONAL

**Ocupa:** banner + tabela quando configurado · ausente quando não

**Aparece somente quando** o usuário configurou agrupadores do Resumo Executivo (P-V1-10 do DCV).

**Banner:** `Resumo por {nome_agrupador_executivo}`
- Quando 2 agrupadores: `Resumo por {agrupador_1} × {agrupador_2}`

**Tabela** (header + linhas ordenadas por |Diferença líquida| desc · empate alfabético):

| {agrupador} | N Conciliados | N Divergentes | Diferença líquida |
|---|---:|---:|---:|
| Filial 03 - Belém | 247 | 18 | R$ 142,30 |
| Filial 01 - Recife | 312 | 12 | R$ 87,90 |
| **Total** | **559** | **30** | **R$ 230,20** |

**TotalsRow ativa** · soma cada coluna numérica.

**Espelho compacto da Aba 2** · esta tabela tem só as 4 colunas essenciais · Aba 2 expande com colunas por campo comparado.

### 3.8 · Seção 8 · Síntese do Diagnóstico

**Ocupa:** banner + 4 linhas curtas

**Banner:** `Síntese do Diagnóstico`

**4 linhas** (em formato "rótulo · valor · ação"):
- `Tolerância absorvida · 12 registros · R$ 8,42 · ver Aba 6`
- `Duplicidades detectadas · 3 chaves afetando 8 registros · ver Aba 6`
- `Ambiguidades de match · 2 chaves afetando 5 registros · ver Aba 6`
- `Warnings · 3 ativos · ver Aba 6`

**Quando categoria está zerada** · linha aparece com `0` e sem `· ver Aba 6` · ex: `Duplicidades detectadas · 0`. Manter as 4 linhas é importante para auditabilidade · cliente vê que a verificação foi feita mesmo quando nada foi encontrado.

**Status da Ponte NÃO repete aqui** · ele já tem seção própria (§3.4). Síntese cobre só os 4 itens listados.

### 3.9 · Seção 9 · Configuração aplicada

**Ocupa:** banner + 3 sub-blocos

**Banner:** `Configuração aplicada`

**Sub-bloco 9.1 · Agrupadores de match** (1 linha)
- Texto: `Agrupadores de match: Filial — Contém · CNPJ — Exato · Documento — Exato`

**Sub-bloco 9.2 · Agrupadores do Resumo** (1 linha · condicional)
- Texto: `Agrupadores do Resumo: Filial · Centro de Custo`
- Quando não configurado: linha não aparece

**Sub-bloco 9.3 · Campos comparados** (1 linha por campo)
- Texto: `Campo: Valor Bruto · tipo Monetário · tolerância R$ 0,01`
- Cor cinza · texto pequeno

**Sub-bloco 9.4 · Modelo aplicado** (1 linha · condicional)
- Texto: `Modelo de configuração: {nome_modelo} (criado em {data}) · reaplicação regenera este Resumo idêntico`
- Quando vazio · linha não aparece

### 3.10 · Leitura Qualitativa · texto consolidado · fim da Aba 1

**Ocupa:** banner + bloco de prosa (altura calculada via `_calcular_altura_leitura_qualitativa`)

**Banner:** `Leitura Qualitativa`

**Bloco de prosa parametrizado** · 3 a 6 frases · gerado pela função `construir_leitura_qualitativa_v1` (a ser criada · paralela à `construir_leitura_qualitativa_v2` que está em `templates/familia_a/leitura_qualitativa.py` pós-D-202).

**Estrutura semântica do texto** (não literal · gerado dinamicamente):

> A conciliação entre {origem_ux} e {comparado_ux} apresenta taxa geral de **87,3%**. Dos {N} registros processados, a maioria está conciliada · {Y} registros divergem por valor com diferença líquida de **R$ {valor}** concentrada em {agrupador_principal}. {N} registros aparecem só na {origem_ux} e {N} só no {comparado_ux}, sugerindo {leitura_estrutural}. A Ponte de Conciliação {fecha/tem resíduo de R$ X em N campo(s)}, indicando que {leitura_da_ponte}. Casos de duplicidade ({N}) e ambiguidade de match ({N}) merecem atenção · ver Diagnóstico.

**Regras de variação semântica** (paralelas a V2):
- Taxa ≥95%: tom de fechamento · "conciliação satisfatória"
- Taxa entre 70%-95%: tom analítico · "divergências localizadas"
- Taxa <70%: tom de alerta · "investigação ampla recomendada"
- Ponte fecha + tolerância absorvida: tom positivo
- Ponte com resíduo: tom de alerta · investigação Aba 5

**Q5 resolvida (decisão final):**

A leitura qualitativa em V1 segue **opção (a)** com extensão · **mora apenas no Resumo Executivo** · mas é **mais longa que V2** porque tem 6 classes de classificação + Status da Ponte para descrever (vs V2 que tem 7 valores semânticos só de variação).

Não criar leituras próprias para Mapa · Ponte · Diagnóstico (opção b descartada). Cada aba operacional é auto-explicativa pelo seu título e estrutura. Leitura concentrada no Resumo evita redundância e mantém o Resumo como única narrativa autoral.

---

## 4 · Aba 2 · Resumo por Agrupador · CONDICIONAL

**Aparece somente quando** o usuário configurou agrupadores do Resumo Executivo. Espelho expandido da Seção 7 da Aba 1.

### 4.1 · Estrutura visual

- ListObject Excel nativo · ZebraStyle · TotalsRow ativa
- 1 linha por valor único do(s) agrupador(es)
- Ordenação default: |Diferença líquida total| desc · empate alfabético

### 4.2 · Colunas

**Identificadores** (1 a 2 colunas dependendo da configuração):
- `{nome_agrupador_1}` · ex: "Filial"
- `{nome_agrupador_2}` · quando 2 agrupadores configurados (ex: "Centro de Custo")

**Métricas estruturais** (4 colunas):
- `N Conciliados`
- `N Divergentes por valor`
- `N Só {origem_ux}` (rótulo amigável aplicado)
- `N Só {comparado_ux}`

**Métricas por campo comparado** (4 colunas × N campos · expansão dinâmica):
- `Soma {origem_ux} · {campo}` · ex: "Soma Razão · Valor Bruto"
- `Soma {comparado_ux} · {campo}`
- `Diferença líquida · {campo}`
- `Σ |Diferença| · {campo}`

**Total geral** (TotalsRow):
- Linha de totais com SUBTOTAL em cada coluna numérica · TotalsRow herda number_format das células de dados

### 4.3 · Filtros e ordenação

- AutoFilter ativo na header
- Filtros úteis pré-pensados: Filial específica · Top 10 por |Diferença|
- Não há formatação condicional aqui (a leitura macro é o número absoluto)

### 4.4 · Microcopy do título da aba

- A1: `Resumo por {nome_agrupador_executivo}` · com par quando 2 agrupadores

---

## 5 · Aba 3 · Mapa de Conciliação

Resposta da Q4 · todos os registros (conciliados + divergentes) · classificação como coluna · filtro padrão.

### 5.1 · Estrutura visual

- ListObject Excel nativo
- 1 linha por registro processado (após match · grão = par registro Origem-Comparado · ou registro órfão de um lado só)
- AutoFilter ativo · cliente filtra por Classificação para isolar "Divergentes por valor" · "Só na Origem" · etc.
- Formato condicional na coluna `Classificação` · semáforo:
 - Verde: `Conciliado`
 - Amarelo: `Divergente por valor` · `Divergência por duplicidade` · `Divergência por ambiguidade`
 - Vermelho: `Só na {origem_ux}` · `Só no {comparado_ux}`

### 5.2 · Colunas

**Identificadores** (N colunas dinâmicas · uma por agrupador de match):
- `{nome_agrupador_1}` · ex: "CNPJ"
- `{nome_agrupador_2}` · ex: "Documento"
- ... até N agrupadores configurados

**Coluna de classificação** (1 coluna · destacada):
- `Classificação` · valores user-facing do Bloco 3 vocabulário (com substituição amigável):
 - `Conciliado`
 - `Divergente por valor`
 - `Saiu do {origem_ux}` ou `Só na {origem_ux}`
 - `Apareceu no {comparado_ux}` ou `Só no {comparado_ux}`
 - `Divergência por duplicidade`
 - `Divergência por ambiguidade de match`

**Métricas consolidadas** (3 colunas · sempre presentes):
- `Diferença total` (soma das diferenças de todos os campos comparados desse registro · MONETARIO_BRL adaptativo)
- `Σ |Diferença|` (soma absoluta · auditoria)
- `Variação total %` (Diferença total / Soma Origem · PERCENTUAL adaptativo)

**Coluna Observações** (1 coluna · texto curto · presente quando há):
- Para `Conciliado` com tolerância: `Tolerância absorvida: R$ 0,03`
- Para `Divergência por duplicidade`: `2 registros na {origem_ux} · 1 no {comparado_ux}`
- Para `Divergência por ambiguidade`: `Match aproximado · 2 candidatos com score equivalente`
- Para outros casos: vazio

### 5.3 · TotalsRow

- Conta de registros por classificação (via SUBTOTAL com filtro)
- Soma de Diferença total · Σ |Diferença|
- Variação total % na TotalsRow → vazio (não faz sentido média/soma de %)

### 5.4 · Microcopy

- A1: `Mapa de Conciliação`
- A2 subtítulo: `1 linha por registro · use o filtro "Classificação" para isolar conciliados ou divergentes`

---

## 6 · Aba 4 · Análise Analítica

### 6.1 · Estrutura visual

Mesmo padrão da Aba 3 mas com **expansão por campo comparado** · cada campo vira 4 colunas dedicadas.

- ListObject Excel nativo · ZebraStyle · TotalsRow opcional (típico off · grão é registro·campo · soma faz menos sentido)
- 1 linha por registro · igual à Aba 3
- AutoFilter ativo

### 6.2 · Colunas

**Identificadores** (mesmas N colunas dinâmicas da Aba 3 · 1 por agrupador de match):
- `{nome_agrupador_1}` · `{nome_agrupador_2}` · ...

**Coluna de classificação** (mesma da Aba 3 · 1 coluna):
- `Classificação`

**Bloco por campo comparado** (4 colunas × N campos):

Para cada campo comparado declarado (até 10):
- `Valor · {origem_ux} · {campo}` · ex: "Valor · Razão · Valor Bruto"
- `Valor · {comparado_ux} · {campo}`
- `Diferença · {campo}`
- `Status · {campo}` · valores: `Igual` · `Dentro da tolerância` · `Divergente` · `Sem valor na Origem` · `Sem valor no Comparado` · `Sem valor nos dois lados`

### 6.3 · Formato condicional

Na coluna `Status · {campo}`:
- Verde: `Igual` · `Dentro da tolerância`
- Amarelo: `Divergente`
- Cinza: `Sem valor na Origem` · `Sem valor no Comparado` · `Sem valor nos dois lados`

### 6.4 · Microcopy

- A1: `Análise Analítica`
- A2 subtítulo: `1 linha por registro · cada campo comparado em 4 colunas · Origem · Comparado · Diferença · Status`

---

## 7 · Aba 5 · Ponte de Conciliação

A peça que Elaine destacou no esboço α.1 como "extremamente importante · de forma prática · exatamente onde está a diferença".

### 7.1 · Estrutura visual

Aba **bespoke** · não tabular · construída como decomposição vertical em forma de ponte (saldo inicial → componentes → saldo final · padrão contábil de "ponte de variação").

### 7.2 · Layout vertical

**Linha 1 · Título da aba**
- A1: `Ponte de Conciliação · Como a diferença total se compõe`

**Linha 3 · Card grande de status (mesma seção 4 do Resumo · expandido)**
- 1 card largo (mescla A:H)
- Caso "Fecha": ✅ `Ponte fecha em todos os campos`
- Caso "Resíduo": ⚠️ `Resíduo de R$ 142,50 em 2 campo(s)`
- Sub-linha: `Diferença total entre {origem_ux} e {comparado_ux}: R$ 342,50`

**Linha 6 · Banner: `Decomposição por campo comparado`**

**Para cada campo comparado** (sub-bloco repetido):

**Linha 8 · Mini-banner do campo** (cor secundária · fundo claro)
- `Campo: Valor Bruto`

**Linhas 9-15 · Tabela de decomposição** (formato vertical "ponte"):

| Componente | Valor |
|---|---:|
| Saldo {origem_ux} | R$ 1.482.330,00 |
| (−) Registros só na {origem_ux} | R$ -47.330,00 |
| (+) Registros só no {comparado_ux} | R$ +32.987,50 |
| (+/−) Diferenças nos divergentes por valor | R$ -342,50 |
| (+/−) Tolerância absorvida | R$ +8,42 |
| (=) Saldo {comparado_ux} esperado | R$ 1.481.653,42 |
| Saldo {comparado_ux} real | R$ 1.481.987,50 |
| **Resíduo** | **R$ +334,08** |

**Linha 17 · Status do campo**
- Caso fecha (resíduo absoluto < tolerância de fechamento): ✅ `Campo fecha · resíduo absorvido pela tolerância`
- Caso resíduo: ⚠️ `Resíduo R$ +334,08 não atribuído · investigar`

**Linha 19 · respiro** · próximo campo começa em 22

### 7.3 · Cores e ênfase

- "Saldo {origem_ux}" e "Saldo {comparado_ux}" · cor primária · bold
- Linha "Resíduo" · cor amarela ou verde dependendo do status · bold
- Linhas intermediárias · neutras
- Bordas finas em torno do bloco de cada campo · isolam visualmente

### 7.4 · Quando há ≥3 campos comparados

A aba pode ficar comprida. Cada campo continua em sub-bloco próprio · não há agregação. Elaine chamou Ponte de "extremamente importante" · escolha defensiva é manter detalhamento mesmo que aba fique longa.

### 7.5 · Vocabulário

- "Saldo Origem" técnico vira "Saldo {origem_ux}" user-facing (rótulo amigável aplicado)
- "Saldo Comparado" técnico vira "Saldo {comparado_ux}" user-facing
- "Saldo {comparado_ux} esperado" = soma da decomposição · indica o que **deveria** ser
- "Saldo {comparado_ux} real" = valor efetivo · indica o que **é**
- "Resíduo" = real − esperado · diferença não atribuída · auditoria humana investiga

### 7.6 · Quando há 0 divergentes mas Ponte mostra resíduo

Caso especial · típico de erro de tolerância configurada incorretamente. Microcopy adicional sob o status:
- `Atenção: 0 registros divergentes mas Ponte mostra resíduo · revise tolerâncias na Aba 6 · Diagnóstico`

---

## 8 · Aba 6 · Diagnóstico

Padrão F-APRESENT · 6 seções · igual à Aba 4 da V2 (Diagnóstico V2 · `_renderizar_secao_distribuicao_estrutural` etc.) com adaptação de conteúdo para natureza V1.

### 8.1 · Seção 1 · Configuração técnica completa

**Banner:** `Configuração aplicada · técnica`

Detalhamento técnico de tudo que a Aba 1 §9 mostrou em formato user-facing:
- Modos de match por agrupador (Exato · Contém · Contém-com-aspas · etc.)
- Tolerâncias absolutas e relativas por campo
- Estratégia de tratamento de nulos (P-V1-09)
- Casos de match aproximado: critério usado

### 8.2 · Seção 2 · Tolerâncias absorvidas (detalhe)

**Banner:** `Tolerâncias absorvidas`

Lista os N registros que foram classificados como "Conciliado · com tolerância absorvida".
- Tabela com identificadores · campo · diferença absorvida · tolerância configurada

### 8.3 · Seção 3 · Duplicidades detectadas

**Banner:** `Duplicidades detectadas`

Lista chaves duplicadas que geraram classificação `Divergência por duplicidade`.
- Tabela com chave · N registros na Origem · N no Comparado · ação sugerida (deduplicar antes? consolidar?)

### 8.4 · Seção 4 · Ambiguidades de match

**Banner:** `Ambiguidades de match`

Lista pares ambíguos · onde o sistema teve mais de um candidato com score equivalente.
- Tabela com chave · N candidatos · scores · resolução aplicada (preserva como ambíguo · não casa)

### 8.5 · Seção 5 · Warnings ativos

**Banner:** `Warnings`

Lista 3 warnings catalogados em V1 (W-V1-TOL · W-V1-DUP · W-V1-AMB):
- W-V1-TOL: tolerância configurada acima de Y% · pode esconder erros materiais
- W-V1-DUP: N% das chaves apresentam duplicidade · revisar dado de entrada
- W-V1-AMB: N% das chaves apresentam ambiguidade · revisar critério de match

Padrão de microcopy: `WARNING · {mensagem técnica} · ação sugerida: {ação}`

### 8.6 · Seção 6 · Thresholds (TED · D-205) e parâmetros editáveis

**Banner:** `Thresholds e parâmetros`

Tabela de TED (Thresholds Editáveis Declarados) com:
- Nome técnico → user-facing
- Valor configurado
- Valor default
- Quando "valor configurado ≠ default" · destaque visual

---

## 9 · Resumo de microcopy crítico (referência rápida α.3)

| Elemento | Texto user-facing |
|---|---|
| Título Aba 1 | `Conciliação de Bases · {origem_ux} × {comparado_ux}` |
| KPI primário | `Taxa de Conciliação Geral` |
| Status Ponte fecha | `✅ Ponte fecha em todos os campos comparados` |
| Status Ponte resíduo | `⚠️ Resíduo de R$ X em N campo(s) · ver Aba 5 · Ponte de Conciliação` |
| Classificação Conciliado | `Conciliado` |
| Classificação Divergente valor | `Divergente por valor` |
| Classificação Só Origem | `Só na {origem_ux}` ou `Saiu do {origem_ux}` (rótulo amigável) |
| Classificação Só Comparado | `Só no {comparado_ux}` ou `Apareceu no {comparado_ux}` |
| Classificação Duplicidade | `Divergência por duplicidade` |
| Classificação Ambiguidade | `Divergência por ambiguidade de match` |
| Coluna Diferença em PERCENTUAL | `Diferença em p.p.` |
| Coluna Variação | `Variação` ou unidade-específica (Bloco 10.2) |
| Cards "Total" em PERCENTUAL | `Média · {origem_ux}` (não "Total") |

---

## 10 · O que é V1-específico (não veio da V2)

Lista do que é genuinamente novo · e portanto novo para Família A · candidato a generalização em P-V1 e potencialmente V11:

1. **6 classes de classificação estrutural** (vs 7 valores semânticos da V2) · Bloco 3 do vocabulário ganha extensão para V1
2. **Coluna "Classificação"** como filtro primário em aba tabular (Mapa) · padrão novo · pode promover para Família A se V11 fizer igual
3. **Status da Ponte** como seção 4 do Resumo · padrão novo · tem 1 linha de status grande
4. **Aba "Ponte de Conciliação"** bespoke · decomposição vertical · padrão novo · genuinamente V1 (V11 não terá Ponte · sua decomposição é diferente · D-051)
5. **Distinção Mapa × Análise Analítica** · 2 abas tabulares com grão por coluna diferente · padrão novo
6. **6 abas (vs 4 V2)** · estrutura macro diferente · operacionaliza P-V1-10 do DCV
7. **Leitura Qualitativa mais longa** · cobre 6 classes + Status da Ponte · paralela mas distinta de V2

---

## 11 · O que é absorvido para vocabulário transversal Família A (candidato)

Em ALINHA pós-V1 (Auditoria pós-V11 · cláusula B de D-204) · podem virar transversais:

- Padrão "Status binário com sub-linha de ação" (`Status da Ponte` em V1 · pode ter análogos em V4/V11)
- Padrão "Classificação como coluna em aba tabular com formato condicional semáforo"
- Padrão "Sub-blocos por entidade configurável em aba bespoke" (Ponte por campo · poderia ser análogo a Composição por dimensão em V4)

Fica catalogado · não decide agora.

---

## 12 · Lista de pendências para α.3

Pontos onde Elaine pode ajustar:

- **P-α.3-01** · Microcopy do banner Seção 4 · `Status da Ponte` vs `Status da Ponte de Conciliação`?
- **P-α.3-02** · Ícone de status · Unicode (✅ ⚠️) ou caractere com cor? Decisão visual.
- **P-α.3-03** · Rótulo das classificações `Só na Origem` vs `Saiu do Origem` · qual é default canônico? (DCV usa "Só em A" · vocabulário Bloco 3 sugere "Saiu do" · pode coexistir: "Saiu do" quando rótulo amigável · "Só na" quando rótulo vazio?)
- **P-α.3-04** · Aba 4 · TotalsRow ativa ou desativada? (proposto desativada · grão registro·campo)
- **P-α.3-05** · Ordem das 6 seções da Aba 6 · Configuração primeiro ou última? (proposto primeiro · cliente abre Diagnóstico procurando "como foi configurado" · DCV original tinha em outra ordem)
- **P-α.3-06** · Leitura qualitativa V1 · pode citar nome do agrupador onde a divergência se concentra? Ou só "concentrada em X agrupadores"? (proposto: cita o de maior peso · paraleliza V2)
- **P-α.3-07** · Quando há **0 divergentes**: Aba 3 (Mapa) ainda tem 1.428 linhas conciliadas · OK manter? Ou Aba 3 colapsa para card "Tudo conciliado · sem registros para mapear"? (proposto: mantém · auditabilidade)
- **P-α.3-08** · Cabeçalho identificador (Seção 1) · 4 linhas é demais quando T-MODELO vazio? Pode colapsar para 2-3? (proposto: 3 linhas mínimo · 4 com modelo)

---

## 13 · Próximos passos pós-α.3

Após Elaine aprovar α.3 (com ou sem ajustes):

1. **Mockup-V1 vira gate aprovado** · Cláusula A de D-204 satisfeita · A-V1 destrancado para abrir
2. **P-V1 · Spec de Produto** · escrita pelo Arquiteto · consome este mockup como referência canônica · estende vocabulário Bloco 3 com classificações V1 · estende Bloco 10 se necessário
3. **S-V1 · Spec técnica** · contratos lógicos (`ContratoComparativo` herdando de `ConciliacaoV1`) · regras de cálculo · wireframe funcional
4. **B-V1 · Base sintética** · condicional D-147 · provavelmente dispensada (V1 consome `base_fundacao.xlsx` via `base_v1_cliente.xlsx`)
5. **V-V1 · `visao_v1.py`** · sessão Claude Code · motor da V1
6. **A-V1 · `app_v1.py`** · sessão Claude Code · app Streamlit aplicando P-V1
7. **VV-V1 · Validação Visual Construtora** · gate Camada 2 humana · 1ª aplicação de método novo da Família A com mockup pré-requisito (D-203 estreia)
8. **Auditoria pós-V1?** · NÃO · V1 não é pioneira de família refactorada · Auditoria pós-família é sobre V11 (que fecha modelo Família A · D-204 cláusula B · ALINHA-Auditoria-pós-V11 · pré-V4)

---

**Fim de α.2.** Elaine reage em α.3 sobre o pacote inteiro · ajustes pontuais ou aprovação direta.
