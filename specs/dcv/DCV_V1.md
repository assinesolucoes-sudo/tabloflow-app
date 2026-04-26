# DCV-V1 · Conciliação de Bases

**Visão:** V1 · Conciliação de Bases
**Módulo:** Módulo 1 · TabloAnálise
**Família:** A · Confronto entre universos
**Status:** Aprovado *
**Data de aprovação:** 18/04/2026
**Sessões de refino:** 2 (Sessões 1 e 2 da Fase 0)
**Arquivo canônico:** `/specs/dcv/dcv_v1.md`

---

## 1. Propósito da visão

A V1 confronta duas bases lógicas e responde, de forma estruturada e auditável, **se elas representam o mesmo universo de dados e onde estão as divergências**. É a visão de conciliação do TabloFlow — o instrumento que o analista usa quando dois sistemas deveriam espelhar a mesma realidade, mas não estão espelhando.

A visão responde quatro perguntas, nessa ordem de leitura:

1. **Qual a taxa geral de conciliação entre as duas bases?**
2. **Onde a divergência está concentrada?** (por agrupador analítico escolhido pelo usuário)
3. **Quais registros especificamente estão divergentes e por quê?**
4. **Como a diferença total se compõe matematicamente?** (Ponte de Conciliação)

A V1 é a única visão do Módulo 1 que opera com **duas bases lógicas simultâneas**. Sua complexidade estrutural está no match entre os dois universos; sua precisão analítica está em preservar toda informação disponível e classificar de forma auditável, nunca consolidar ou interpretar.

---

## 2. Posicionamento analítico

A V1 ocupa o espaço entre dois mundos:

- **A montante:** bases brutas oriundas de ERPs, relatórios, integrações, planilhas operacionais — frequentemente dispersas, com convenções de chave distintas, granularidade diferente
- **A jusante:** decisão humana de conciliação (reconciliar contabilmente, acionar fornecedor, corrigir integração, validar migração)

A V1 **não decide** nada em nome do usuário. Ela estrutura o que antes era feito manualmente no Excel — casa registros, classifica divergências, decompõe a diferença total — e entrega um artefato Excel auditável. O **analista humano** permanece como tomador de decisão.

Casos de uso típicos:

- Conciliação contábil mensal (Razão × Balancete, ou Sistema A × Sistema B)
- Validação de migração entre sistemas
- Auditoria de integração (ERP × Data Warehouse)
- Conciliação bancária (extrato × sistema)
- Conciliação intercompany
- Conferência de folha (sistema de RH × contábil)

---

## 3. O que a visão recebe

### 3.1 Estrutura de entrada (P-V1-01)

A V1 aceita **duas estruturas de upload**:

- **Estrutura A · Dois arquivos distintos** — o usuário sobe dois arquivos separadamente. O sistema lista as abas de cada arquivo. O usuário escolhe uma aba de qualquer arquivo como **Origem** e outra aba (de qualquer arquivo) como **Comparado**.
- **Estrutura B · Um único arquivo com duas abas** — o usuário sobe um único arquivo. O sistema lista todas as abas. O usuário escolhe duas abas do mesmo arquivo.

**Unidade lógica da V1 é a aba.** Cada aba é uma base consolidada pronta para confronto. A dualidade Origem/Comparado se mantém no contrato lógico independentemente da estrutura de arquivo escolhida.

**Nomeação:** defaults "Origem" e "Comparado", ambos **editáveis pelo usuário** na etapa de configuração. Os nomes escolhidos aparecem em todos os artefatos produzidos (colunas do Excel, KPIs do Resumo, Ponte de Conciliação).

**Fora de escopo:** dados empilhados em uma única aba com coluna discriminadora (onde registros de A e B coexistem na mesma lista, distinguidos por uma coluna "Origem/Destino" ou similar) **não** são escopo da V1. O usuário nesse cenário deve usar previamente o **Módulo 2 · TabloPrep** (operação RESHAPE) para separar em duas abas, e depois trazer para a V1.

### 3.2 Papel do Motor de Upload

A V1 nunca acessa arquivo bruto diretamente. Ela consome `UploadResult` e `MotorResult` produzidos pelos motores da Fundação. Na leitura consolidada dos 10 DCVs, emerge um transversal específico desta visão:

**T-DUAL · extensão do `motor_upload` para modo dual.** Aceita estrutura A (dois arquivos) ou estrutura B (um arquivo com duas abas), produzindo um `UploadResult` que carrega a referência aos dois lados nomeados (Origem/Comparado ou rótulos editados pelo usuário). Detalhamento técnico é responsabilidade do G-FUND.

---

## 4. Configuração da análise

A V1 segue o padrão estrutural de produto do CONTEXT §13: **fluxo de etapas progressivas com dependência**. A UI concreta (número exato de etapas, layout de cada uma, transições) é decidida no wireframe funcional da Spec (Fase 2 — ver §11 deste DCV). Aqui ficam registradas as **decisões analíticas** que o wireframe obrigatoriamente respeitará.

### 4.1 Agrupadores de match

Definem a **chave lógica do confronto** entre Origem e Comparado. São as colunas que, combinadas, identificam de forma única cada entidade a ser reconciliada.

**Comportamento:**

- Sempre tratados como texto (zeros à esquerda preservados, formatação numérica não normalizada — o usuário pode ter `"0101"` em uma base e `"0101"` na outra; o match deve funcionar)
- Podem ser simples (uma coluna) ou compostos (várias colunas concatenando a chave)
- Definem a granularidade da análise (um par de chaves casa um registro de Origem com um de Comparado)

**Limite MVP:** até **5 agrupadores de match** (L-V1-D). A UI bloqueia a tentativa de configurar o 6º, exibindo mensagem informativa orientando o usuário a avaliar se algum campo pertence a "Agrupadores do Resumo" ou "Filtros", ou se a chave pode ser simplificada. Reavaliação pós-MVP registrada como **P-V1-D-Evo**.

**Cada agrupador carrega:**

- Campo na base Origem
- Campo na base Comparado
- Rótulo analítico (nome dado pelo usuário para este agrupador — ex: "CNPJ do Fornecedor")
- Modo de match

### 4.2 Modos de match (P-V1-02 revisada)

Um modo de match é **regra de busca declarada pelo usuário**, não grau de confiança no resultado. Uma vez que o usuário configura um modo, a regra é parte do contrato declarado da análise. O sistema executa exatamente essa regra.

**Modos disponíveis no MVP:**

| Modo | Comportamento |
|---|---|
| **Exato** (default) | Igualdade total entre chave de Origem e chave de Comparado |
| **Contém** | Chave de Origem contém chave de Comparado (ou vice-versa) |
| **Inicia com** | Chave de Origem inicia com chave de Comparado (ou vice-versa) |
| **Termina com** | Chave de Origem termina com chave de Comparado (ou vice-versa) |

**Nenhum modo produz "match aproximado" como grau de qualidade.** Uma vez que a regra declarada encontra um par único, o par casou — ponto final. Se os valores comparados batem (dentro da tolerância, ver §5.3), o registro é classificado como `Conciliado`, sem asterisco ou ressalva.

**A única situação em que modo não-exato produz classificação diferenciada** é quando a regra encontra **múltiplos candidatos** para a mesma chave — aí o registro é classificado como `Divergência por ambiguidade de match` (ver §5.2).

**Match fuzzy (similaridade com threshold):** registrado como **P-V1-02-Evo** para roadmap pós-MVP. Exige biblioteca externa, introduz UI de threshold numérico, opera por score em vez de determinístico. Usuário que precisa de fuzzy no MVP usa "Contém" como proxy imperfeito ou faz limpeza prévia no Módulo 2. Quando implementado, virá como transversal **T-FUZZY** reutilizável.

### 4.3 Campos comparados (P-V1-05, P-V1-06)

Definem os **valores que serão confrontados** entre Origem e Comparado para cada par de registros casados.

**Cada campo carrega:**

- Campo na base Origem
- Campo na base Comparado
- Nome analítico
- Tipo lógico: Valor Monetário, Quantidade, Volume, Percentual, Prazo, Índice, Estado/Situação
- **Tolerância absoluta** (default zero)

**Limite MVP:** até **10 campos comparados** (herança da V2). Reavaliação pós-MVP registrada como **P-V1-10-Evo**.

**Tolerância por campo (P-V1-05):**

Cada campo comparado declara sua própria tolerância absoluta. Default zero. Regra:

> `|Valor_Origem − Valor_Comparado| ≤ tolerância` → `Conciliado`
> Caso contrário → `Divergente por valor`

A tolerância respeita o Princípio C.5: o sistema não decide sozinho que "uma diferença de R$ 0,01 na verdade é zero" — o usuário declara o critério de materialidade, o sistema aplica. Granularidade por campo resolve o caso de bases multi-métrica (monetário aceita centavos; quantidade não).

Registros classificados como `Conciliado` que tenham diferença absoluta não-zero (mas dentro da tolerância) ganham **flag "Conciliado com diferença dentro da tolerância"** e geram o warning `W-V1-TOL` no Diagnóstico.

**Tolerância percentual:** registrada como **P-V1-05-Evo** para roadmap pós-MVP. O edge case `Valor_Origem = 0` (comum em "Só em B") exige decisão adicional; absoluto cobre 90% dos casos corporativos. Entra quando houver pedido real.

### 4.4 Agrupadores do Resumo Executivo (P-V1-10)

**Conceitualmente distintos dos agrupadores de match.** Esta separação foi confirmada pela Usuária na Sessão 2.

| Conceito | Função | Escopo |
|---|---|---|
| Agrupadores de match | Definem a chave lógica do confronto A × B | Operacional (pré-análise) |
| Agrupadores do Resumo Executivo | Definem o nível de consolidação da análise | Analítico (pós-análise) |

**Os dois tipos têm limites independentes e configuração em etapas separadas.** O usuário escolhe livremente qualquer combinação em cada tipo.

**Limite MVP:** até **5 agrupadores do Resumo Executivo**. Sem Evo registrado no MVP — caso real apareça, trata-se como caso a caso.

**Quando configurados**, disparam a criação de duas estruturas analíticas (§6):

- Seção 6 do Resumo Executivo (tabela consolidada compacta)
- Aba "Resumo por Agrupador" na exportação Excel (tabela expandida)

**Quando não configurados**, as duas estruturas simplesmente não existem — a V1 entrega análise não-consolidada.

### 4.5 Modelo de configuração (T-MODELO, padrão CONTEXT §13.3)

Toda a configuração declarada pelo usuário (agrupadores de match com modos, campos comparados com tolerâncias, agrupadores do Resumo) é **persistível como modelo reutilizável**.

O modelo salva apenas a **configuração lógica** — não salva dados fonte. O usuário pode aplicar o modelo em nova análise (sobre novas bases) e os campos da configuração são pré-preenchidos automaticamente, reproduzindo o mesmo comportamento determinístico (princípio C.1).

Implementação compartilhada via transversal **T-MODELO** da Fundação. Todas as 10 visões usam o mesmo padrão.

---

## 5. Lógica de processamento

### 5.1 Preparação das bases

O motor recebe Origem e Comparado como `UploadResult` (via T-DUAL). Não há consolidação prévia. Não há aplicação de T-AGRUPA. A V1 **preserva toda a informação disponível** — decisão estrutural (ver §5.2).

### 5.2 Match e classificação (P-V1-03+04)

**Regra-mestra:** a V1 **preserva e classifica — nunca consolida automaticamente**. Aplicação direta do Princípio C.5.

**Tabela de classificação por situação:**

| Situação | Classificação do registro | Observação |
|---|---|---|
| Match 1-para-1, valores iguais (ou dentro da tolerância) | `Conciliado` | Flag adicional se diferença absorvida pela tolerância |
| Match 1-para-1, valores diferentes (acima da tolerância) | `Divergente por valor` | Diferença = Valor_Origem − Valor_Comparado |
| Chave em Origem ausente em Comparado | `Só em A` | Valor_Comparado = null |
| Chave em Comparado ausente em Origem | `Só em B` | Valor_Origem = null |
| Chave duplicada em Origem e/ou Comparado | `Divergência por duplicidade` | Todas as ocorrências preservadas |
| Match em modo não-exato produzindo múltiplos candidatos | `Divergência por ambiguidade de match` | Todos os candidatos preservados |

**Consequência arquitetural:** a V1 **não usa o transversal T-AGRUPA**. Consolidar duplicatas antes do confronto apagaria informação de auditoria crítica. Na V1, duplicidade **é** achado analítico, não ruído a eliminar.

**Transparência obrigatória (princípio C.2):** duplicidade e ambiguidade disparam warnings estruturais (`W-V1-DUP`, `W-V1-AMB`) que aparecem em três lugares:

1. Aba de Diagnóstico (detalhamento completo)
2. Bloco síntese do Diagnóstico dentro do Resumo Executivo
3. Flag no registro específico do detalhamento

### 5.3 Cálculo de diferença e aplicação da tolerância

Para cada par de registros casados:

**Para cada campo comparado:**

```
Se Classificacao_Registro ∈ {Só em A, Só em B}:
    Valor_Origem = valor real (ou null)
    Valor_Comparado = valor real (ou null)
    Diferenca = null
    Classificacao_campo = null (não se aplica)

Senão:
    Diferenca = Valor_Origem − Valor_Comparado
    Se |Diferenca| ≤ tolerância do campo:
        Classificacao_campo = Conciliado
        Se Diferenca ≠ 0: flag "Conciliado com diferença dentro da tolerância" + W-V1-TOL
    Senão:
        Classificacao_campo = Divergente por valor
```

**Classificação agregada do registro (P-V1-06):**

- `Conciliado` — todos os campos comparados estão conciliados (dentro da tolerância)
- `Divergente por valor` — pelo menos um campo está divergente por valor
- `Só em A`, `Só em B`, `Divergência por duplicidade`, `Divergência por ambiguidade de match` — classificações estruturais no nível do registro, não aplicáveis por campo

### 5.4 Tratamento de nulos (P-V1-09)

**Null no lado ausente, diferença não calculada.**

Registro `Só em A`:
- `Valor_Origem_<campo>` = valor real
- `Valor_Comparado_<campo>` = `null` (célula vazia no Excel)
- `Diferenca_<campo>` = `null`

Registro `Só em B`: análogo, com Origem nullificado.

**Razão:** ausência de registro é fato estrutural, não zero contábil. Preenchê-lo com zero apagaria a distinção crítica entre "existe e vale zero" e "não existe". Null preserva rigorosamente a distinção e integra naturalmente com Excel (funções nativas como SUM ignoram nulls).

---

## 6. Saída da visão (resultado estruturado)

### 6.1 Estrutura de abas do Excel exportado

**6 abas** quando há agrupadores do Resumo Executivo configurados; **5 abas** quando não há. Ordem natural de leitura:

| Ordem | Aba | Aparece | Pergunta que responde |
|---|---|---|---|
| 1 | Resumo Executivo | Sempre | Qual o resultado geral? |
| 2 | Resumo por Agrupador | Se configurado | Como se distribui por Filial/Conta/etc.? |
| 3 | Divergências | Sempre | Quais registros não conciliaram? |
| 4 | Análise Analítica | Sempre | Detalhe completo registro a registro |
| 5 | Ponte de Conciliação | Sempre | Como a diferença total se decompõe? |
| 6 | Diagnóstico | Sempre | Como o sistema processou a análise? |

**Diagnóstico é sempre a última aba.** Esta regra é **transversal a todas as 10 visões** (ver §10.1 — decisão levada ao G-FUND).

### 6.2 Aba 1 · Resumo Executivo (7 seções — P-V1-10)

**Seção 1 · Cabeçalho identificador**
- Nome de Origem (default "Origem", editável)
- Nome de Comparado (default "Comparado", editável)
- Arquivo(s) e aba(s) de cada lado
- Data/hora do processamento
- Modelo de configuração aplicado (se houver, via T-MODELO)

**Seção 2 · Volumetria**
- Registros em Origem: N
- Registros em Comparado: M
- Registros processados após match: P

**Seção 3 · Taxa de conciliação (KPI principal — P-V1-08)**

Taxa única consolidada, número grande em destaque:

> **Taxa de conciliação = (registros conciliados) / (total de registros processados)**

Logo abaixo, **bloco de decomposição pela classificação estrutural do registro**, sempre com as 6 classes (mesmo com zero):

| Classificação | N registros | % do total |
|---|---|---|
| Conciliados | N | X% |
| Divergentes por valor | P | Z% |
| Só em A | Q | W% |
| Só em B | R | V% |
| Divergência por duplicidade | S | U% |
| Divergência por ambiguidade de match | T | K% |

Sub-informação dos conciliados: "Dos N conciliados, M tiveram diferença absorvida pela tolerância (soma R$ X)" — quando aplicável.

**Não há decomposição "match exato vs aproximado" no Resumo.** Conciliados são conciliados, pela regra que o usuário declarou. O detalhamento operacional por modo de match vive no Diagnóstico (§6.7).

**Seção 4 · Valor financeiro por campo comparado**

Para cada campo comparado declarado (até 10):

- Soma Valor_Origem: R$ X
- Soma Valor_Comparado: R$ Y
- Diferença líquida: R$ (X − Y)
- Soma absoluta das diferenças: R$ Z (Σ|Diferenca| registro a registro, exclui nulls)
- Tolerância absorvida: N registros, soma R$ W (se aplicável)

**Seção 5 · Cobertura por base**

- Registros de Origem com par encontrado: A de N (X%)
- Registros de Comparado com par encontrado: B de M (Y%)

Informação útil para auditoria assimétrica.

**Seção 6 · Resumo por agrupador executivo** (se configurado)

Tabela consolidada pelos agrupadores executivos configurados, com colunas de classificação e diferença total. Ordenação default: maior |Diferença líquida consolidada| primeiro (T-RANK aplicado, empate resolvido por ordem alfabética).

Esta tabela é **espelho compacto da aba 2** (Resumo por Agrupador). A aba 2 tem a mesma informação expandida com mais colunas por campo comparado.

**Seção 6B · Síntese do Diagnóstico**

Bloco curto sintetizando o processamento:

- N registros com tolerância absorvida
- N chaves com duplicidade
- N chaves com ambiguidade
- Status da Ponte: "Fecha em todos os campos" ou "Resíduo em N campo(s) — ver Diagnóstico"

Detalhe completo vive na aba 6 (Diagnóstico).

**Seção 7 · Configuração aplicada**

- Agrupadores de match: rótulos e modos (ex: "Filial — Contém; CNPJ — Exato")
- Agrupadores do Resumo Executivo: rótulos
- Campos comparados: nomes, tipos, tolerâncias

Fecha auditabilidade: o Resumo carrega a configuração que o produziu. Reaplicação via T-MODELO regenera o mesmo Resumo.

### 6.3 Aba 2 · Resumo por Agrupador (condicional)

Aparece apenas se o usuário configurou agrupadores do Resumo Executivo. É **visão analítica expandida por recorte** — o artefato principal para controllers e analistas contábeis que leem resultado por filial, conta contábil, centro de custo.

**Colunas (por agrupador configurado + métricas):**

- Agrupador(es) — uma ou mais colunas conforme configuração
- N total de registros
- Conciliados (contagem)
- Divergentes por valor (contagem)
- Só em A (contagem)
- Só em B (contagem)
- Duplicidade (contagem)
- Ambiguidade (contagem)
- Taxa de conciliação local (%)
- **Para cada campo comparado:**
  - Soma Valor_Origem
  - Soma Valor_Comparado
  - Diferença líquida
  - Diferença absoluta (Σ|Diferenca|)

**Ordenação default:** maior |Diferença líquida consolidada| primeiro. "Consolidada" = soma das diferenças líquidas dos campos monetários (misturar monetário com quantidade no ranking não faz sentido). Empate resolvido por ordem alfabética do primeiro agrupador.

### 6.4 Aba 3 · Divergências

Todos os registros classificados como não-conciliados, com detalhamento completo. Agrupados visualmente pelos agrupadores configurados.

**Classificações incluídas:**
- Divergente por valor
- Só em A
- Só em B
- Divergência por duplicidade
- Divergência por ambiguidade de match

**Colunas:** todas as colunas do detalhamento analítico (ver §6.5), filtradas para classificações não-conciliadas.

### 6.5 Aba 4 · Análise Analítica

Todos os registros processados, com todas as colunas do contrato detalhado.

**Colunas por registro:**

- Colunas de agrupador de match (uma por agrupador configurado)
- **Para cada campo comparado:**
  - Valor_Origem
  - Valor_Comparado
  - Diferenca
  - Classificacao_campo
  - Flag_campo (ex: "Conciliado com diferença dentro da tolerância")
- Classificacao_Registro (agregada)
- Motivo_Registro
- Flags estruturais: Match_Aproximado (reservada — ver nota), Duplicidade, Ambiguidade

**Nota sobre Flag_Match_Aproximado:** coluna **reservada mas não populada** no MVP. A decisão P-V1-02 revisada removeu a flag de qualidade. A coluna existe para receber informação operacional (modo de match usado) caso Spec futura decida popular — mas no contrato atual fica vazia.

### 6.6 Aba 5 · Ponte de Conciliação (P-V1-07)

Reconciliação matemática por campo comparado. **Uma sub-Ponte por campo**, empilhadas verticalmente com título em cada uma. Cada sub-Ponte tem 3 blocos:

**Bloco A · Ponte plana** (7 linhas)

| Linha | Descrição | Valor |
|---|---|---|
| 1 | Soma Valor_Origem (base completa) | R$ X |
| 2 | (−) Registros Só em Origem | −R$ Y |
| 3 | (−) Diferença líquida em Divergentes por valor | −R$ Z |
| 4 | (+) Registros Só em Comparado | +R$ W |
| 5 | = Soma Valor_Comparado (calculado) | R$ V |
| 6 | Soma Valor_Comparado (base real) | R$ V' |
| 7 | **Verificação** | V = V'? |

**Verificação:** ✓ "Ponte fecha" (se |V − V'| ≤ ε) ou ⚠ "Resíduo de R$ (V'−V) — ver nota de rodapé".

**Épsilon:** fixo em R$ 0,01 para campos do tipo "Valor Monetário"; 0 para Quantidade e outros tipos discretos. Sem configuração pelo usuário (evita inflar UI).

**Bloco B · Nota de rodapé** (sempre presente)

> *N registros classificados como Divergência por duplicidade e M registros classificados como Divergência por ambiguidade de match não entram na reconciliação matemática desta Ponte (valores agregados ambíguos). Ver aba "Divergências" para detalhamento registro a registro.*

**Bloco C · Tabela secundária por agrupador do Resumo Executivo** (se configurado)

| Agrupador(es) | Conciliados | Só em A (R$) | Só em B (R$) | Divergente valor (R$) | Diferença líquida (R$) |
|---|---|---|---|---|---|
| F01, CC-100 | 245 | −4.500 | +1.200 | −300 | −3.600 |

Ordenação default: maior |Diferença líquida| primeiro.

### 6.7 Aba 6 · Diagnóstico (L-V1-B)

**Registro estrutural completo do processamento.** Responde à pergunta "como o sistema processou a análise?" em 6 seções temáticas.

**Seção 1 · Estrutura detectada**
Base (Origem/Comparado), Arquivo, Aba, N° de linhas, N° de colunas, Data/hora de leitura.

**Seção 2 · Inferência de tipos**
Coluna, Base, Tipo inferido, N° de nulos, Cardinalidade, Observação (ex: "valores numéricos em {0,1,NaN} — tratado como booleano"). Apenas colunas efetivamente usadas pela V1.

**Seção 3 · Configuração aplicada**
Sub-seções:
- 3.1 Agrupadores de match: Rótulo | Campo Origem | Campo Comparado | Modo
- 3.2 Campos comparados: Nome | Campo Origem | Campo Comparado | Tipo | Tolerância
- 3.3 Agrupadores do Resumo Executivo: Rótulo | Campo(s)
- 3.4 Modelo aplicado (se via T-MODELO): Nome | Data de criação

**Seção 4 · Processamento por modo de match**
Agrupador | Modo configurado | N° de pares casados pelo modo | N° produzindo ambiguidade.

**Informação puramente operacional**, sem conotação de qualidade — apenas registra o que a regra fez.

**Seção 5 · Warnings emitidos**

Tabela agregada com linhas por warning, seguida de listagem detalhada de ocorrências quando aplicável.

Warnings formalizados da V1:

| Código | Nome | Quando dispara | Listagem detalhada |
|---|---|---|---|
| `W-V1-TOL` | Tolerância absorveu diferenças | ≥ 1 registro com diferença dentro da tolerância | Chave, campo, diferença absorvida |
| `W-V1-DUP` | Duplicidade em chaves | ≥ 1 chave duplicada em Origem ou Comparado | Chave, base, N° ocorrências, soma do valor |
| `W-V1-AMB` | Ambiguidade em match não-exato | ≥ 1 chave produzindo múltiplos candidatos | Chave Origem, chaves candidatas, campo responsável |

Warnings com zero ocorrências aparecem com "0 ocorrências — nenhuma a reportar" (auditabilidade — ausência é informação).

**Warnings herdados do motor (da Fundação):**
- `W-B01` (inferência de boolean disfarçado, D-008) — a Fundação reavaliará no G-FUND

**Seção 6 · Ponte de Conciliação — nota de resíduo**

Aparece com conteúdo quando há resíduo não-zero em qualquer Ponte:

| Campo comparado | Resíduo (R$) | Causa provável | Registros afetados |
|---|---|---|---|
| Valor_Faturado | 0 | — | Fecha dentro do épsilon |
| Quantidade | 230 | Duplicidade nas chaves X, Y, Z | 6 registros |

Quando todas as Pontes fecham: "Todas as Pontes fecham dentro do épsilon aplicado. Nenhum resíduo a reportar."

---

## 7. Transversais utilizados e não utilizados

Leitura consolidada para o G-FUND (Fase 1):

**Transversais que a V1 usa:**

| Sigla | Nome | Função na V1 |
|---|---|---|
| **T-DUAL** 🆕 | Extensão do motor_upload para modo dual | Única visão que usa — aceita 2 arquivos ou 1 arquivo com 2 abas |
| **T-DIAG** | Diagnóstico estrutural obrigatório | Aba 6 do Excel + seção 6B do Resumo Executivo |
| **T-MODELO** | Salvar/aplicar configuração como modelo | Padrão estrutural de produto (CONTEXT §13.3) |
| **T-RANK** | Ranking determinístico | Ordenação da tabela secundária da Ponte e da aba Resumo por Agrupador |

**Transversais que a V1 NÃO usa (contraste explícito para o G-FUND):**

| Sigla | Por que a V1 não usa |
|---|---|
| ❌ **T-AGRUPA** | V1 preserva e classifica, não consolida (Princípio C.5) |
| ❌ **T-SEMA** | V1 faz conciliação, não avaliação maior/menor/neutro (L-V1-A) |
| ❌ **T-EIXO** | V1 não tem dimensão temporal/sequencial |
| ❌ **T-PIVOT** | V1 não processa estrutura empilhada (exige RESHAPE prévio no Módulo 2) |
| ❌ **T-ACUM** | V1 não produz acumulado progressivo |
| ❌ **T-ABC** | V1 não produz classificação de participação |

---

## 8. Limites da visão

A V1 **não realiza**, por natureza analítica:

- Análise temporal ou sequencial
- Classificação semântica (maior/menor/melhor/pior) — ver §7 e L-V1-A
- Interpretação de tendência
- Decisão automática em nome do usuário (Princípio C.5)
- Consolidação de duplicatas (preserva e classifica)
- Match fuzzy por similaridade (MVP — registrado em P-V1-02-Evo)
- Tolerância percentual (MVP — registrado em P-V1-05-Evo)

---

## 9. Relação com outras visões

**Complementa V2 (Família A):** V1 identifica *que* duas bases divergem; V2 explica *como* um mesmo valor variou entre dois estados de uma única base. Fluxo natural em auditoria: V1 primeiro (conciliar), V2 depois (analisar variação dos conciliados ou dos divergentes).

**Precede análises evolutivas** (V3, V4 da Família C e B): antes de analisar composição ou tendência, é comum validar que a base está consistente — papel da V1.

**Base para workflow de auditoria:** V1 é frequentemente a primeira análise executada em uma auditoria mensal ou due diligence. Seu resultado filtra e prioriza o restante da investigação.

---

## 10. Decisões transversais geradas pela V1

Decisões da V1 que têm escopo maior que a V1 e devem ser incorporadas pelo G-FUND:

### 10.1 Diagnóstico sempre como última aba em todas as visões

**Âmbito:** transversal. Regra do T-DIAG aplicada ao F-EXP (exportação Excel padrão).

**Racional:** o Diagnóstico é artefato de auditoria/validação. O fluxo natural de leitura é resultado primeiro, validação depois quando necessário. Colocar o Diagnóstico no final respeita esse fluxo em todas as 10 visões.

**Registrada como D-017** (ver DECISIONS.md).

### 10.2 T-DUAL como novo transversal

**Âmbito:** específico da V1 dentro do Módulo 1, mas entra no escopo de implementação do G-FUND como extensão do `motor_upload`. Adicionado à lista de transversais do CONTEXT §6.

### 10.3 T-MODELO obriga-se à V1 desde o MVP

**Âmbito:** transversal aplicado a todas as 10 visões (padrão estrutural de produto, CONTEXT §13.3). A V1 é a primeira a consumir na implementação.

---

## 11. Wireframe funcional — separação DCV × Spec

Esta seção formaliza uma distinção metodológica importante confirmada pela Usuária na Sessão 2.

### 11.1 O que fica no DCV (este documento)

Âncoras estruturais que **vinculam** o wireframe futuro:

- Estrutura de upload em duas modalidades (§3.1)
- Configuração progressiva em etapas com dependência (CONTEXT §13.2)
- Objetivo da Visão como bloco de ajuda contextual (CONTEXT §13.1)
- Modelo de configuração acessível para salvar/aplicar (CONTEXT §13.3 + T-MODELO)
- Limites de cada tipo de agrupador/campo (§4)
- Estrutura de exportação de 5 ou 6 abas (§6)
- Conteúdo obrigatório de cada aba (§6.2 a §6.7)
- Vocabulário de warnings (§6.7)

### 11.2 O que fica na Spec futura (bloco S-V1 da Fase 2)

Decisões de fluxo de tela concreto que o DCV **não fecha**:

- Número exato de etapas da configuração
- Layout de cada etapa (formulário, cards, accordion, etc.)
- Transições entre etapas
- Tela de resultado antes da exportação
- Estados vazios (sem upload) e estados de erro
- Localização precisa do botão "Objetivo da Visão" (header, sidebar, modal)
- Mecânica exata de salvar e aplicar modelo
- Microanálise progressiva (se houver)

**Essas decisões vivem na Spec porque:**

1. Dependem do resultado do G-FUND (contratos técnicos estabilizados da Fundação)
2. Podem dialogar com a Frente A (Identidade Visual) quando executada
3. Podem dialogar com a Fase 3 (IA) quando executada
4. Recebem **aprovação explícita da Usuária** como parte do bloco S-V1, antes do código iniciar (princípio B.2 do CONTEXT)

### 11.3 Referência navegável autorizada (Camada B de D-015)

Wireframe Figma Make: `https://spend-crayon-46234394.figma.site/`

**Não vincula** o wireframe funcional futuro da Spec. Serve como referência visual durante a construção, sob a distinção de D-015:

- **Camada A (vinculante):** padrões estruturais de produto — Objetivo da Visão, etapas progressivas, T-MODELO. Já incorporados neste DCV.
- **Camada B (não-vinculante):** paleta de cores, componentes shadcn, gradientes, ícones Sparkles, copywriting específico. Ficam disponíveis como inspiração; serão avaliados quando Frente A (Identidade Visual) e Fase 3 (IA) forem executadas.

### 11.4 Nota sobre IA

Conforme D-015 Camada C: a **UX e lógica da camada de IA** (Sistema de Sugestões) permanecem parqueadas em Fase 3 (⬜ Não iniciado). Quando implementada, a IA operará **a partir do contrato estrutural declarado pelo usuário** na etapa de upload (arquivos + abas + nomes Origem/Comparado), sugerindo preenchimento das etapas seguintes.

Os motores produzidos no G-FUND devem preservar os metadados que a IA consumirá quando existir — sem antecipar a UX da Fase 3.

---

## 12. Pendências da V1 e status

### 12.1 Pendências estruturais (todas fechadas)

| Código | Tema | Status |
|---|---|---|
| P-V1-01 | Fontes de entrada — estrutura dual | ✅ Fechada (Sessão 1) |
| P-V1-02 | Modos de match (revisada) | ✅ Fechada (Sessão 1 + revisão Sessão 2) |
| P-V1-03+04 | Duplicidade e ambiguidade de match | ✅ Fechada (Sessão 1) |
| P-V1-05 | Tolerância de valor | ✅ Fechada (Sessão 2) |
| P-V1-06 | Granularidade da classificação (registro/campo) | ✅ Fechada (Sessão 2) |
| P-V1-07 | Estrutura da Ponte de Conciliação | ✅ Fechada (Sessão 2) |
| P-V1-08 | Taxa de conciliação e decomposição no Resumo | ✅ Fechada (Sessão 2) |
| P-V1-09 | Tratamento de valor em registros sem par | ✅ Fechada (Sessão 2) |
| P-V1-10 | KPIs definitivos do Resumo Executivo | ✅ Fechada (Sessão 2) |
| L-V1-A | V1 não usa semântica maior/menor/neutro | ✅ Fechada (Sessão 2) |
| L-V1-B | Forma da aba de Diagnóstico | ✅ Fechada (Sessão 2) |
| L-V1-D | Limite de agrupadores de match | ✅ Fechada (Sessão 2) |
| L-V1-E | Insumo consolidado para o G-FUND | ✅ Fechada (Sessão 2) |

### 12.2 Pendências de evolução pós-MVP (roadmap)

| Código | Tema | Origem |
|---|---|---|
| P-V1-02-Evo | Match fuzzy (similaridade com threshold) — via T-FUZZY | P-V1-02 |
| P-V1-05-Evo | Tolerância percentual por campo | P-V1-05 |
| P-V1-D-Evo | Reavaliar limite de agrupadores de match em conciliação intercompany/contábil complexa | L-V1-D |
| P-V1-10-Evo | Reavaliar limite de campos comparados | P-V1-10 |

### 12.3 Dependências confirmadas para o G-FUND

| Item | Escopo |
|---|---|
| T-DUAL | Implementação do motor_upload em modo dual |
| T-DIAG | Exportação Excel padrão com Diagnóstico como última aba (D-017) |
| T-MODELO | Contrato de salvar/aplicar modelo de configuração |
| T-RANK | Ranking determinístico com regra de desempate |
| Contrato V1Result | Estrutura detalhada a formalizar na Spec (S-V1), informada pelo contrato genérico VNResult que o G-FUND definir |
| Catálogo de warnings | W-V1-TOL, W-V1-DUP, W-V1-AMB adicionados ao vocabulário |

---

## 13. Histórico de refino

**Sessão 1 · 18/04/2026** (com produção de decisões de método)

- P-V1-01 · fontes de entrada + T-DUAL identificado
- P-V1-02 · modos de match (versão inicial)
- P-V1-03+04 · duplicidade e ambiguidade (unificadas)
- Decisões de método produzidas: D-015 (Camadas Figma Make), D-016 (unidade de bloco = visão)
- Princípio C.5 formalizado no CONTEXT

**Sessão 2 · 18/04/2026** (refino puro)

- P-V1-05 · tolerância absoluta por campo
- P-V1-06 · classificação em dois níveis
- P-V1-09 · null no lado ausente
- L-V1-A · confirmação de não-uso de T-SEMA
- L-V1-D · limite de 5 agrupadores de match
- P-V1-08 · taxa única (com revisão de P-V1-02 removendo flag "Match aproximado")
- P-V1-10 · 7 seções do Resumo Executivo + nova aba "Resumo por Agrupador"
- P-V1-07 · Ponte de Conciliação em 3 blocos
- L-V1-B · Diagnóstico em 6 seções + Diagnóstico como última aba (transversal)
- L-V1-E · consolidação de dependências para o G-FUND

**Decisões transversais derivadas da Sessão 2:**
- D-017 · Diagnóstico sempre como última aba em todas as visões (ver DECISIONS.md)

---

## 14. Referências

- **CONTEXT.md** v2 — §3 (método em 3 fases), §6 (transversais), §9 (princípios invioláveis), §13 (padrões estruturais de produto)
- **DECISIONS.md** — D-011 (método DCV), D-014 (reforma do método), D-015 (Camadas Figma Make), D-016 (unidade de bloco = visão), D-017 (Diagnóstico como última aba)
- **GLOSSARIO.md** v2 — entradas de T-DUAL, T-MODELO, T-DIAG, T-RANK, Princípio C.5
- **Wireframe de referência (Camada B):** https://spend-crayon-46234394.figma.site/
- **Fontes consultadas:** DCV_PREVIO_M1_V1.md (insumo), DCV_PREVIO_M1_V1_FIGMA.md (padrões visuais — Camadas A/B aplicadas), dcv_v1_SESSAO1_parcial.md (estado intermediário)

---

*Este DCV é o artefato consolidado de compreensão da V1. A partir de sua aprovação pela Usuária, nenhuma decisão estrutural da V1 pode ser alterada sem nova decisão formal registrada em DECISIONS.md. Implementações downstream (Spec, base sintética, motor, app) derivam deste documento.*
