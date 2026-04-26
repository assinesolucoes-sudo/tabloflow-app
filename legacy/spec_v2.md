# spec_v2.md — Visão V2: Análise Comparativa entre Referências ## Identificação - **Código:** V2 - **Nome:** Análise Comparativa entre Referências - **Módulo:** M1 — TabloAnálise - **Arquivo de saída:** `src/visao_v2.py` - **Contrato de entrada:** `MotorResult` (de `motor_base.py`) - **Contrato de saída:** `V2Result` (definido nesta spec) --- ## O que esta visão faz Compara dois estados de um mesmo campo dentro de um mesmo recorte analítico. Os dois estados são chamados de **Referência A** e **Referência B**. O motor calcula a variação absoluta e percentual entre eles, classifica o resultado e organiza a saída por agrupadores definidos pelo usuário. **Pergunta central:** "O que mudou entre A e B — e essa mudança é boa ou ruim?" --- ## Estruturas de Entrada Suportadas A V2 suporta **duas estruturas de entrada**, definidas na Etapa 1.2: ### Estrutura 1 — Por Colunas Os dois estados estão em **colunas separadas** na mesma base. - Exemplo: coluna `Orçado` e coluna `Realizado` na mesma linha. - Cada linha já representa um registro com os dois valores lado a lado. ### Estrutura 2 — Por Linhas Os dois estados estão em **linhas separadas**, identificadas por um campo discriminador. - Exemplo: coluna `Período` com valores `"Jan/24"` e `"Jan/25"` — cada um em uma linha. - O motor agrupa por chave e pivota para comparar os dois valores. > **Regra:** A estrutura de entrada é definida uma única vez na Etapa 1.2 e condiciona > toda a configuração subsequente. Não pode ser alterada após confirmação. --- ## Tipos de Campo Suportados Cada campo comparado tem um **tipo**, que condiciona os cálculos e a classificação: | Tipo | Descrição | Exemplo | |------|-----------|---------| | `VALOR` | Medida numérica absoluta | Receita, Custo, Volume | | `PERCENTUAL` | Valor já em formato percentual | Margem %, Taxa de conversão | | `INDICE` | Número índice ou score | NPS, Rating, Índice de eficiência | > O tipo é definido pelo usuário na sub-etapa 2.1. A IA pode sugerir com base > no nome e nos valores detectados pelo MotorResult. --- ## Semântica do Campo (Interpretação Analítica) Para cada campo comparado, o usuário define a **semântica** — como interpretar a direção da variação: | Semântica | Quando usar | Exemplo | |-----------|-------------|---------| | `MAIOR_E_MELHOR` | Aumento = positivo | Receita, Volume de vendas | | `MENOR_E_MELHOR` | Redução = positivo | Custo, Prazo de entrega | | `NEUTRO` | Variação sem julgamento | Headcount, Quantidade de SKUs | > A semântica é definida por campo. Campos diferentes podem ter semânticas diferentes. --- ## Lógica de Cálculo Para cada registro (linha ou grupo), o motor calcula:
variacao_absoluta = valor_B - valor_A
variacao_percentual = (valor_B - valor_A) / abs(valor_A) # se valor_A != 0

**Casos especiais:** - `valor_A == 0` e `valor_B != 0` → variação percentual = `None`, flag `SURGIMENTO` - `valor_A != 0` e `valor_B == 0` → variação percentual = `-100%`, flag `DESAPARECIMENTO` - `valor_A == 0` e `valor_B == 0` → variação = `0`, classificação = `SEM_VARIACAO` --- ## Classificação por Registro Cada registro recebe uma **classificação** baseada na variação e na semântica: | Classificação | Condição | Semântica aplicável | |---------------|----------|---------------------| | `MELHORA` | Variação na direção positiva | MAIOR_E_MELHOR ou MENOR_E_MELHOR | | `PIORA` | Variação na direção negativa | MAIOR_E_MELHOR ou MENOR_E_MELHOR | | `SEM_VARIACAO` | variacao_absoluta == 0 | Todas | | `VARIACAO_NEUTRA` | Qualquer variação | NEUTRO | | `SURGIMENTO` | valor_A == 0, valor_B != 0 | Todas | | `DESAPARECIMENTO` | valor_A != 0, valor_B == 0 | Todas | > Quando há múltiplos campos comparados, cada campo recebe sua própria classificação. > O registro não tem uma classificação global — cada campo é independente. --- ## Contrato de Saída — V2Result (Pydantic) ```python from pydantic import BaseModel from typing import Optional, List, Literal class RegistroComparado(BaseModel): agrupadores: dict[str, str] # ex: {"Filial": "SP", "Produto": "X"} campo: str # nome analítico do campo tipo_campo: Literal["VALOR", "PERCENTUAL", "INDICE"] semantica: Literal["MAIOR_E_MELHOR", "MENOR_E_MELHOR", "NEUTRO"] valor_a: Optional[float] valor_b: Optional[float] variacao_absoluta: Optional[float] variacao_percentual: Optional[float] # None se valor_A == 0 classificacao: Literal[ "MELHORA", "PIORA", "SEM_VARIACAO", "VARIACAO_NEUTRA", "SURGIMENTO", "DESAPARECIMENTO" ] flag: Optional[str] # "SURGIMENTO", "DESAPARECIMENTO" ou None class ResumoAgrupador(BaseModel): agrupador: str # nome do campo agrupador valor: str # valor do agrupador campo: str total_a: float total_b: float variacao_absoluta: float variacao_percentual: Optional[float] classificacao_predominante: str # classificação mais frequente no grupo class V2Result(BaseModel): visao: str = "V2" nome_visao: str = "Análise Comparativa entre Referências" estrutura_entrada: Literal["POR_COLUNAS", "POR_LINHAS"] nome_referencia_a: str # ex: "Orçado", "Jan/24" nome_referencia_b: str # ex: "Realizado", "Jan/25" campos_comparados: List[str] # nomes analíticos dos campos agrupadores: List[str] # nomes dos campos agrupadores registros: List[RegistroComparado] resumo_por_agrupador: List[ResumoAgrupador] total_registros: int total_melhoras: int total_pioras: int total_sem_variacao: int total_surgimentos: int total_desaparecimentos: int warnings: List[str] errors: List[str] success: bool
Parâmetros de Configuração (Etapas)

Etapa 1 — Upload e Estrutura

1.1 — Upload e Identificação

Recebe o arquivo via MotorResult
A IA analisa o MotorResult e sugere: estrutura de entrada, nomes das referências,
campos candidatos a comparação e agrupadores
1.2 — Estrutura de Entrada

Usuário confirma ou altera: POR_COLUNAS ou POR_LINHAS
Se POR_LINHAS: usuário define o campo discriminador e os dois valores que identificam A e B
Etapa 2 — Configuração Principal

2.1 — Definição dos Campos de Comparação

Se estrutura = POR_COLUNAS:

Usuário seleciona: coluna A, coluna B, nome analítico do campo, tipo do campo
Pode adicionar múltiplos campos (cada par de colunas = um campo comparado)
Se estrutura = POR_LINHAS:

Usuário seleciona: campo de valor, nome analítico, tipo do campo
O motor usa o discriminador definido em 1.2 para separar A e B
2.2 — Interpretação Analítica do Campo

Para cada campo, usuário define a semântica: MAIOR_E_MELHOR, MENOR_E_MELHOR ou NEUTRO
A IA sugere com base no nome analítico do campo
2.3 — Agrupadores da Análise

Usuário seleciona os campos categóricos que segmentam a análise
Mínimo: 0 agrupadores (análise global)
Máximo recomendado: 3 agrupadores
Os agrupadores aparecem tanto na tela quanto na exportação Excel
Etapa 3 — Análise em Tela (Microanálise Prévia)

Exibe antes da exportação:

Tabela com todos os registros: agrupadores | campo | valor A | valor B | variação abs | variação % | classificação
Totalizadores: total de melhoras, pioras, sem variação, surgimentos, desaparecimentos
Resumo por agrupador (se agrupadores configurados): total A, total B, variação, classificação predominante
Warnings ativos (ex: registros com valor_A = 0)
Etapa 4 — Exportação Excel

Estrutura de 4 abas:

Análise Detalhada Todos os registros com classificação por campo Resumo por Agrupador Consolidação por cada agrupador configurado Surgimentos e Desaparecimentos Registros com flags especiais Parâmetros Configuração usada: estrutura, campos, semânticas, agrupadores
Nome do arquivo: V2_[nome_da_visao_editavel]_[data].xlsx
O usuário pode escolher o padrão visual (tema claro ou escuro) antes de exportar.

Limitadores Técnicos

Máximo de campos comparados 10 Erro se ultrapassado Máximo de agrupadores 5 Warning se > 3 Máximo de registros 500.000 Erro se ultrapassado valor_A == 0 — variacao_percentual = None, flag ativo Campos não numéricos selecionados — Erro de validação Estrutura POR_LINHAS sem discriminador — Erro de configuração
## Warnings e Errors

### Warnings (não bloqueiam execução)
- **W01** — Registro com valor nulo em A ou B (excluído da análise) · também dispara se >20% de nulos no campo
- **W02** — Agrupador com cardinalidade > 50 valores únicos
- **W03** — Mais de 3 agrupadores configurados (pode impactar legibilidade)
- **W04** — Registros com valor_A = 0 detectados (variação % não calculável)
- **W05** — Estrutura POR_LINHAS: valores do discriminador não balanceados (A tem mais registros que B ou vice-versa)
- **W06** — Estrutura POR_LINHAS: N registros sem par detectados e tratados como SURGIMENTO (sem A) ou DESAPARECIMENTO (sem B) *[novo · ver D-P01]*
- **W07** — Resumo por agrupador de campo PERCENTUAL/INDICE usa média simples — para análise rigorosa, considere ponderação manual *[novo · ver D-P02]*

### Errors (bloqueiam execução)
- **E01** — Nenhum campo de comparação configurado
- **E02** — Campo selecionado não é numérico
- **E03** — Estrutura POR_LINHAS: discriminador não encontrado na base
- **E04** — Estrutura POR_LINHAS: valor de referência A ou B não encontrado no discriminador
- **E05** — Número de registros excede 500.000
- **E06** — Número de campos comparados excede 10

---

## Decisões Tomadas no Bloco B-2 (17/04/2026)

Pendências discutidas e fechadas durante a construção da `base_v2.xlsx`. Implementação obrigatória conforme abaixo.

### D-P01 — POR_LINHAS sem par → tratar como SURGIMENTO/DESAPARECIMENTO
Quando a estrutura POR_LINHAS resultar em registros sem par após o pivot:
- Registro presente apenas em A (sem B) → classificação = `DESAPARECIMENTO`, flag = `DESAPARECIMENTO`, valor_b = 0, variacao_percentual = -1.0
- Registro presente apenas em B (sem A) → classificação = `SURGIMENTO`, flag = `SURGIMENTO`, valor_a = 0, variacao_percentual = None
- Disparar warning W06 com a contagem de registros nessa situação
- **Razão:** preserva o registro · consistente com a regra de zeros já definida · alinhado ao perfil de uso (analista quer ver "SKU novo apareceu")

### D-P02 — Agregador PERCENTUAL/INDICE no resumo → média simples + warning
No `ResumoAgrupador`, para campos do tipo PERCENTUAL ou INDICE:
- `total_a` e `total_b` recebem **média simples** dos valores no grupo (não soma)
- Disparar warning W07 obrigatoriamente sempre que houver pelo menos um campo PERCENTUAL ou INDICE com agrupadores configurados
- **Comportamento provisório** — revisitar em Fase 3 se reclamação de usuária aparecer (alternativa futura: média ponderada com campo de peso configurável)

### D-P04 — variacao_percentual NÃO arredondada no contrato
O contrato `RegistroComparado.variacao_percentual` preserva precisão total (float Python nativo). Arredondamento é responsabilidade da camada de exibição (`app_v2.py`) e da exportação Excel (formato `0.0%` ou `0.00%`).
- **Razão:** arredondar no contrato perde informação irreversivelmente · cada camada de saída pode ter precisão diferente

### D-P05 — Nulo ≠ Zero
Valor nulo (None/NaN) em A ou B **nunca** é tratado como zero.
- Registro com nulo em A ou B → excluído da análise · não entra em `registros` nem nas contagens (`total_melhoras`, etc.)
- Disparar warning W01 (escopo ampliado: agora cobre tanto registros individuais quanto >20% de nulos no campo)
- **Razão:** tratar nulo como zero seria inventar valor · viola o princípio determinístico do TabloFlow · preserva auditabilidade

---

## Pendências em Aberto

### P03 — Limite de campos comparados
Validar com usuárias reais se o limite de 10 campos comparados é adequado para casos corporativos.
- **Status:** aguarda validação de produto · não bloqueia implementação atual
- **Default:** manter 10 conforme limitador técnico vigente
Referência de Implementação

Herda os tipos de campo da V2 (esta é a visão de origem dos tipos)
A V3 herda e expande os tipos desta visão para o contexto sequencial
O contrato MotorResult está em spec_motor_base.md
O contrato UploadResult está em spec_motor_upload.md
Nunca acessar o arquivo bruto diretamente — sempre usar MotorResult
```
## Pendências em Aberto

### P01 — POR_LINHAS sem par (descoberta na spec original)
Definir comportamento quando estrutura POR_LINHAS tem registros sem par
(A sem B ou B sem A).
- Opção a: tratar como SURGIMENTO (sem A) / DESAPARECIMENTO (sem B)
- Opção b: excluir do resultado e contabilizar em warnings
- Recomendação provisória: opção a, por preservar o registro
- Status: não coberto na base_v2.xlsx — todas as abas POR_LINHAS são balanceadas

### P02 — Agregador para PERCENTUAL e INDICE no resumo por agrupador
(descoberta na spec original) Soma não faz sentido semântico para campos do
tipo PERCENTUAL e INDICE.
- Opção a: média simples
- Opção b: média ponderada por um campo de peso a definir pelo usuário
- Opção c: bloquear resumo por agrupador para esses tipos
- Recomendação provisória: opção a (média simples) com warning explícito
- Status: tema forçado pela aba POR_COLUNAS_MULTI_TIPO da base_v2.xlsx

### P03 — Limite de campos comparados (descoberta na spec original)
Validar com o produto se o limite de 10 campos comparados é adequado para
casos reais.
- Status: aguarda validação com usuárias.

### P04 — Arredondamento de variacao_percentual (descoberta no Bloco B-2)
Definir nº de casas decimais para variacao_percentual no V2Result.
- Opção a: 2 casas (ex: 0.15) — formato leitura humana direta
- Opção b: 4 casas (ex: 0.1500) — preserva precisão para gráficos
- Opção c: não arredondar no contrato — deixar formatação para a camada
  de exibição/exportação
- Recomendação provisória: opção c — contrato preserva precisão total,
  app_v2 e exportação Excel formatam para exibição
- Status: gabarito da base_v2.xlsx usa 6 casas como referência neutra

### P05 — Comportamento de zeros vs nulos (descoberta no Bloco B-2)
A spec define SURGIMENTO/DESAPARECIMENTO para zero, mas não define
explicitamente o tratamento de NULL.
- Pergunta: nulo em A ou B deve ser tratado como zero ou como
  registro inválido?
- Recomendação provisória: nulo ≠ zero. Registro com nulo em A ou B
  é excluído e contabilizado em warning W01 (ampliar escopo do W01).
- Status: a base_v2.xlsx tem casos de nulo (SKU-101, SKU-103, SKU-202)
  que forçam essa decisão na implementação.