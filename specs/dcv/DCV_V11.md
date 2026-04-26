# DCV-V11 · Conciliação por Aderência

**Visão:** V11 · Conciliação por Aderência
**Módulo:** Módulo 1 · TabloAnálise
**Família:** A · Confronto entre universos
**Status:** Aprovado *
**Data de aprovação:** 19/04/2026
**Sessões de refino:** 2 (19/04/2026)
**Arquivo canônico:** `/specs/dcv/dcv_v11.md`

---

## 1. Propósito da visão

A V11 confronta duas bases lógicas que representam o mesmo universo de dados mas não compartilham chave confiável para relacionar registros. É a visão de conciliação do TabloFlow para o cenário em que o elo analítico entre as bases é valor + contexto textual — histórico, documento, data — em vez de uma chave declarada pelo usuário.

A V11 responde quatro perguntas, nessa ordem de leitura:

1. **Qual a distribuição dos pareamentos por categoria?** (5 categorias: conciliado · divergência de valor · conciliado por valor · pareamento frágil · sem par)
2. **Onde a incerteza está concentrada?** (por agrupador analítico escolhido pelo usuário)
3. **Quais registros especificamente foram pareados, com qual evidência, e quais ficaram sem par?**
4. **Como a diferença total de saldo se decompõe?** (Ponte de Conciliação — opcional)

A V11 é a **terceira visão da Família A** e **par conceitual autônomo de V1** — mesma família, problemas analíticos distintos, motores distintos, vocabulário parcialmente compartilhado. Convivência análoga à de V4 e V10 na Família C, com a diferença de que V11 não é view especializada de V1 (V1 é determinístico por chave declarada; V11 é probabilístico por score de aderência).

A V11 opera por **arquitetura de dois passes texto→valor** — a ordem canônica espelha o fluxo mental do auditor humano na conciliação contábil real: reconhece o fato pelo texto e confere o valor como dado do resultado.

---

## 2. Posicionamento analítico

### 2.1 O cenário real que a V11 atende

O cenário típico da V11 é o cotidiano de áreas contábeis e financeiras brasileiras operando com integrações imperfeitas entre sistemas:

- **Conciliação contábil × financeiro** — extrato financeiro (Protheus, TOTVS, Senior) com `OPERACAO`, `DOCUMENTO`, `PREFIXO/TITULO`, `ENTRADAS`, `SAIDAS`; lançamento contábil do mesmo fato com `HISTORICO`, `LOTE/SUB/DOC/LINHA`, `DEBITO`, `CREDITO`. Nomes diferentes, granularidades diferentes, nenhum campo compartilhado diretamente.
- **Conciliação bancária × sistema** — extrato bancário (Safra, Itaú, Bradesco, BB) com estrutura padrão de banco; sistema interno com outra estrutura. Valor é o elo; contexto textual é evidência.
- **Reconciliação pós-migração** — duas bases do mesmo sistema em versões diferentes, chaves migradas parcialmente.
- **Auditoria cruzada entre departamentos** — folha × contabilidade, comissões × vendas, provisões × liquidações.

Em todos esses cenários, o analista humano hoje faz no Excel um trabalho manual e demorado: abre as duas bases lado a lado, filtra por um valor, procura o mesmo valor no outro lado, lê os textos, decide se é o mesmo fato ou dois fatos de mesmo valor, marca a decisão. A V11 **estrutura esse trabalho** sem substituir a decisão humana: o sistema ranqueia e classifica, o analista confirma e investiga.

### 2.2 Caso-referência real

A V11 foi formalizada a partir da planilha **Conciliacao_Banco_Protheus_Banco_Safra.xlsx** — cenário real de conciliação contábil × bancária usado como gabarito visual e matemático. Contém: aba "Extrato Fin." (1.360 linhas, Protheus), aba "Extrato Contabil" (1.322 linhas, sistema contábil Safra), aba "Divergencias" (49 registros não pareados organizados em dois blocos verticais por lado), aba "Ponte_Conciliacao" com reconciliação de saldo em 3 blocos.

### 2.3 Relação com V1

V1 e V11 convivem como par autônomo da Família A:

| Aspecto | V1 · Conciliação de Bases | V11 · Conciliação por Aderência |
|---|---|---|
| Chave de match | Usuário declara (1 a 5 agrupadores) | Não existe chave confiável |
| Elo primário | Chave textual/numérica igual | Valor igual (dentro de tolerância) + texto contextual próximo |
| Tipo de match | Determinístico | Probabilístico (dois passes, score por aderência) |
| Classificação do resultado | 6 classes estruturais | 5 categorias combinando passe de origem + evidência |
| Ponte de Conciliação | Núcleo matemático (sempre presente) | Complemento opcional (só se saldos declarados) |

**Não há substituição de uma pela outra.** O usuário escolhe conscientemente no momento da análise: V1 quando **tem** chave; V11 quando seu elo é valor + contexto. A fronteira é navegada por microcopy declarativa e autossuficiente em cada visão — nenhuma das duas menciona a outra em interface operacional; quem precisa entender ambas lê este bloco no DCV. DCV-V1 receberá bloco "Relação com V11" equivalente na próxima revisão (retroação registrada).

---

## 3. O que a visão recebe

### 3.1 Estrutura de entrada (T-DUAL)

A V11 compartilha com V1 a transversal **T-DUAL** (formalizada em D-018):

- **Estrutura A · Dois arquivos distintos** — usuário sobe dois arquivos separadamente; escolhe uma aba de cada como **Origem** e **Comparado**.
- **Estrutura B · Um único arquivo com duas abas** — usuário sobe um arquivo; escolhe duas abas do mesmo arquivo.

**Unidade lógica da V11 é a aba.** Dualidade Origem/Comparado se mantém no contrato lógico independentemente da estrutura de arquivo.

**Nomeação dos lados:** defaults "Origem" e "Comparado", ambos editáveis pelo usuário. Nomes escolhidos aparecem em todos os artefatos produzidos. Microcopy de configuração nomeia explicitamente a direção do processamento: "Origem = base investigada (onde começa cada busca de pareamento); Comparado = base de busca (onde o sistema procura candidatos)." Texto declarativo, sem sugerir V1.

### 3.2 Fora de escopo de entrada

Dados empilhados numa aba única com coluna discriminadora permanecem **fora de escopo da Família A** (herança V1). Requer operação RESHAPE prévia no Módulo 2 (ver §9).

---

## 4. Configuração analítica

A V11 segue o padrão estrutural de produto do CONTEXT §13 (fluxo de etapas progressivas com dependência). O número exato de etapas é decidido no wireframe funcional da Spec (Fase 2). As **decisões analíticas** que o wireframe respeitará são as cinco declarações do usuário descritas nesta seção.

### 4.1 Mapeamento semântico de valor

Declaração do usuário sobre qual coluna de uma base representa o mesmo fato financeiro que qual coluna da outra, considerando dualidade (ENTRADAS/SAIDAS ↔ DEBITO/CREDITO), valor único ↔ dualistas, e polaridade.

**Estrutura do contrato:**

- **Um mapeamento analítico como critério principal** + N campos de valor como leitura opcional (ponto-a-ponto; a regra de dualidade — múltiplas correspondências via mesmo mapeamento — fica como P-V11-XX-Evo).
- **Quatro combinações declarativas** cobrem o espaço de possibilidades de estrutura de valor nos dois lados:

| Combinação | Lado A | Lado B | Exemplo |
|---|---|---|---|
| Dual × Dual | ENTRADAS/SAIDAS | DEBITO/CREDITO | Financeiro × Contábil clássico |
| Dual × Único | ENTRADAS/SAIDAS | VALOR_LIQUIDO | Banco × relatório interno |
| Único × Dual | VALOR | DEBITO/CREDITO | Sistema consolidado × razão |
| Único × Único | VALOR_A | VALOR_B | Duas tabelas já consolidadas |

- **Polaridade por correspondência** — usuário declara se o par (ENTRADAS ↔ DEBITO) tem mesma polaridade ou polaridade invertida. No cenário contábil mais comum, débitos contábeis correspondem a saídas financeiras (inversão implícita), mas o sistema não assume: pergunta.
- **Default declarado com heurística de inferência** — motor propõe preenchimento baseado em (i) nomes de colunas reconhecíveis (ENTRADA, SAIDA, DEBITO, CREDITO, VALOR), (ii) distribuição de sinais (se uma coluna tem só positivos e outra só negativos, infere dualidade). Valor proposto **visível na configuração antes da execução**, editável com um clique (padrão "default declarado" — D-024).

Warning **W-V11-MAP-INFERIDO** — registra no Diagnóstico quando o mapeamento foi aceito por default sem edição explícita; permite auditoria pós-análise.

### 4.2 Composição de campos contextuais

Permite que o usuário declare a concatenação de múltiplos campos de uma base em texto único comparável ao texto contextual da outra. Caso típico: `HISTORICO` contábil vs `OPERACAO + DOCUMENTO + PREFIXO/TITULO` financeiro.

**Escopo MVP:**

- Até **5 campos contextuais** por lado.
- Até **3 campos-fonte** por composição.
- **Separador fixo: espaço**, visível no preview da configuração.
- **Assimetria permitida** — um lado pode ter campo único e o outro composto dos 3; ou ambos compostos de quantidades diferentes.
- **Tratamento de nulos:** campos nulos são pulados silenciosamente; a composição se reduz à concatenação dos campos não-nulos. Se todos os campos componentes forem nulos, o texto resultante é string vazia (registra-se warning).

**Implementação técnica:** nativa em V11 MVP com **código estruturado para extração futura como transversal T-CONCAT** (candidato da Fundação — D-053). Zero duplicação arquitetural com operação futura M2.CONCAT; posicionamento final (transversal puro · parte de M2 · capability compartilhada) fica para o G-FUND.

Warnings:
- **W-V11-COMP-CAMPOS-NULOS** — registra casos onde a composição resultou em string vazia por nulos em todos os campos componentes.
- **W-V11-SEM-CONTEXTO** — dispara quando o usuário configurou menos de 2 campos contextuais por lado; score fica dependente de poucos sinais e é informado proativamente.

### 4.3 Tolerância de valor

Herança direta da V1 (P-V1-05): **tolerância absoluta**, default zero, configurável por campo de valor. Parâmetro **único com papel duplo**, declarado em microcopy:

- **No Passe 1** (texto→valor em registros com texto alto): filtra candidatos cujo valor está dentro da tolerância do valor investigado.
- **No Passe 2** (resíduos por valor): mesma tolerância define o que conta como "mesmo valor".

Microcopy na configuração: "Tolerância aplicada: tanto na checagem de valor após match textual quanto na busca por valor entre os registros sem par textual. Valores típicos: 0,00 para dados contábeis; 0,50 a 2,00 para conciliação bancária."

Warning **W-V11-TOL** — material (não só informativo): registra no Diagnóstico os registros cujo match foi afetado pela tolerância (valor não exato, mas dentro da margem), com soma da diferença absorvida. Analista audita.

Tolerância percentual fica como P-V11-XX-Evo (análogo a P-V1-05-Evo).

### 4.4 Score de aderência e limiares de confiança

**Algoritmo do score de aderência textual** (híbrido, encapsulado em T-FUZZY — transversal da Fundação · D-052):

- **Similaridade por trigramas de caracteres** — overlap de sequências de 3 caracteres entre os dois textos normalizados.
- **Presença de tokens-chave** — sequências numéricas ≥ 4 dígitos e sequências alfabéticas maiúsculas ≥ 3 caracteres consecutivos. Tokens presentes nos dois lados aumentam score.
- **Pesos internos fixos**, calibrados na implementação da Fundação, **não expostos ao usuário** (complexidade encapsulada na transversal).
- **Normalização prévia interna**: lowercase · remoção de acentos · remoção de caracteres não-alfanuméricos exceto espaço. Encapsulada em T-FUZZY; analista não configura, Diagnóstico registra.
- **API:** função pura `(texto_A, texto_B) → score ∈ [0, 1]`, determinística.

**Agregação entre campos contextuais:** scores parciais por par de campos, agregados com **média ponderada** em V11. Pesos entre campos **configuráveis com default declarado** — heurística de distintividade (campos com maior cardinalidade relativa têm peso maior, refletindo maior informação discriminativa). Usuário vê pesos na configuração, edita com slider, warning **W-V11-PESOS-CUSTOM** registra customização.

**Dois limiares independentes, editáveis, com default declarado:**

- **Limiar Passe 1 — default 0,70** — score mínimo para considerar que há "evidência textual forte o suficiente para guiar a busca de valor". Ajustável.
- **Limiar Passe 2 — default 0,30** — score mínimo para considerar que há "evidência textual mínima complementando a correspondência de valor". Ajustável independentemente do Passe 1.

Warnings **W-V11-LIMIAR-P1-CUSTOM** e **W-V11-LIMIAR-P2-CUSTOM** registram customizações no Diagnóstico.

### 4.5 Agrupadores do Resumo Executivo (opcional)

Análogo a V1: 0 a 5 agrupadores para consolidar a leitura por recorte (conta contábil, filial, centro de custo, tipo de operação). Se configurado, ativa aba dedicada "Resumo por Agrupador" (ver §6.2).

### 4.6 Reconciliação de saldo (opcional) — campos da Ponte

Etapa final da configuração, explicitamente opcional. Quatro campos numéricos digitados pelo usuário:

- Saldo anterior Origem
- Saldo anterior Comparado
- Saldo final Origem
- Saldo final Comparado

Microcopy: "Declare saldo anterior e saldo final para cada lado se quiser gerar a Ponte de Conciliação. Deixe em branco se a análise é só dos movimentos."

Etapa em branco → Ponte não é gerada; aba é omitida; bloco síntese no Resumo Executivo é omitido; Diagnóstico registra "Ponte de Conciliação não incluída — saldos não declarados na configuração."

Referência a coluna de saldo (primeiro/último valor) é **P-V11-XX-Evo**.

---

## 5. Pipeline de processamento

### 5.1 Arquitetura de dois passes texto→valor

A V11 adota **ordem canônica fixa**, sem configuração de ordem (fixa para determinismo · C.1 · auditabilidade plena):

**Passe 1 · Por texto, confere valor** — para cada registro da Base Investigada, calcula scores de aderência textual contra todos os registros disponíveis na Base de Busca. Se o melhor score ≥ Limiar P1, confirma candidato, confere valor: se valor bate dentro da tolerância → **Conciliado**; se valor não bate → **Divergência de valor**. Alocação consome o registro da Base de Busca; próxima iteração usa pool reduzido. Estratégia: **guloso com ordem por "melhor score disponível"** — a iteração pega o par (registro_origem, registro_busca) com maior score global em cada rodada, remove os dois da fila, repete. Empate no score resolvido por T-RANK (D-041). Global ótimo (algoritmo Húngaro) fica como P-V11-XX-Evo.

**Passe 2 · Por valor, com texto complementar** — sobre os resíduos do Passe 1, cada registro da Base Investigada ainda sem par busca candidatos por **valor** (dentro da tolerância). Se há candidato: calcula score textual entre eles. Se score ≥ Limiar P2 → **Conciliado por valor** (evidência textual complementar). Se score < Limiar P2 → **Pareamento frágil** (valor bate mas sem evidência textual suficiente). Mesma estratégia gulosa.

**Resíduos após os dois passes** — registros de qualquer lado sem par caem em **Sem par**.

### 5.2 Taxonomia de resultado (5 categorias)

| # | Categoria | Passe de origem | Condição |
|---|---|---|---|
| 1 | Conciliado pleno | Passe 1 | score texto ≥ Limiar P1 · valor dentro da tolerância |
| 2 | Divergência de valor | Passe 1 | score texto ≥ Limiar P1 · valor fora da tolerância |
| 3 | Conciliado por valor | Passe 2 | valor dentro da tolerância · score texto ≥ Limiar P2 |
| 4 | Pareamento frágil | Passe 2 | valor dentro da tolerância · score texto < Limiar P2 |
| 5 | Sem par | — | sem correspondência nos dois passes |

### 5.3 Visibilidade ao usuário

C.5 aplicado: **ordem dos passes declarada na configuração** com microcopy explicativa (diagrama simples do fluxo); **Diagnóstico registra contagem por passe**; **KPI principal decomposto por categoria** no Resumo Executivo — taxa global de pareamento + taxas por categoria, sem síntese imposta pelo sistema.

### 5.4 Ambiguidade estrutural (valor repetido)

Em V1 duplicidade de chave é achado analítico que vira divergência. Em V11 valor repetido é esperado — mesmo R$ 6.700,00 pode aparecer 8 vezes no financeiro e 5 vezes no contábil. O trabalho da V11 é **resolver** esses pareamentos por aderência contextual. A estratégia gulosa descrita em §5.1 já lida com isso; empate de score resolvido por T-RANK.

Warning **W-V11-MULT-CAND** — registra casos com N ≥ 2 candidatos por registro resolvidos por score.
Warning **W-V11-VALOR-REPETIDO-MASS** — dispara quando > 30% dos valores aparecem 3+ vezes em alguma das bases; sinaliza cenário de ambiguidade estrutural alta e sugere revisão manual mais extensa.

---

## 6. Saída da visão (resultado estruturado)

### 6.1 Estrutura de abas do Excel

Padrão **6 abas** quando configurada com todos os opcionais; **4 abas** quando configurada sem agrupadores executivos e sem Ponte:

| Ordem | Aba | Aparece | Pergunta que responde |
|---|---|---|---|
| 1 | Resumo Executivo | Sempre | Como se distribuíram os pareamentos e qual a evidência? |
| 2 | Resumo por Agrupador | Se configurado | Como se distribui por Conta/Filial/etc.? |
| 3 | Pareamentos | Sempre | Quais registros casaram, com qual score e qual categoria? |
| 4 | Sem par | Sempre | Quais registros ficaram sem par em cada lado? |
| 5 | Ponte de Conciliação | Se saldos declarados | Como a diferença de saldo se decompõe? |
| 6 | Diagnóstico | Sempre | Como o sistema processou a análise? |

Diagnóstico é sempre a última aba (D-017 — regra transversal do Módulo 1).

### 6.2 Aba 1 · Resumo Executivo

Estrutura herdada de V1 §6.2 com adaptações V11-específicas (7 seções):

**Seção 1 · Cabeçalho identificador** — nomes de Origem/Comparado, arquivo(s), aba(s), data/hora, modelo aplicado (T-MODELO).

**Seção 2 · Volumetria** — registros em cada lado; total de pareamentos efetivos; total em "Sem par".

**Seção 3 · KPI principal — Taxa de pareamento por aderência**, com decomposição sempre exibida pelas 5 categorias:

| Categoria | N registros | % do total |
|---|---|---|
| Conciliado pleno | N | X% |
| Divergência de valor | P | Z% |
| Conciliado por valor | Q | W% |
| Pareamento frágil | R | V% |
| Sem par | S | U% |

Sub-informação: "N registros tiveram diferença absorvida pela tolerância (soma R$ X)" — quando aplicável, via W-V11-TOL.

**Não há síntese imposta pelo sistema.** "Taxa de pareamento" é a soma das 4 primeiras categorias. O analista lê decomposição e decide qual categoria examinar.

**Seção 4 · Valor financeiro por campo** — soma de cada lado, diferença líquida, soma absoluta das diferenças, por campo de valor declarado.

**Seção 5 · Cobertura por base** — registros de Origem com par (A de N, X%), registros de Comparado com par (B de M, Y%).

**Seção 5B · Bloco síntese da Ponte** — quando aplicável, 3-4 linhas resumindo Diferença de saldo anterior · Impacto líquido dos movimentos únicos · Conferência. Aba 5 traz detalhe.

**Seção 6 · Resumo por agrupador executivo** (se configurado) — tabela espelho compacto da aba 2.

**Seção 6B · Síntese do Diagnóstico** — N registros com tolerância absorvida, N com múltiplos candidatos, N com score customizado, N com limiar customizado, status da Ponte. Detalhe completo vive na aba 6.

**Seção 7 · Configuração aplicada** — mapeamento semântico, composição de campos, critério de similaridade (limiares), tolerâncias, pesos entre campos. Fecha auditabilidade; reaplicação via T-MODELO regenera o mesmo Resumo.

### 6.3 Aba 2 · Resumo por Agrupador (condicional)

Aparece se o usuário configurou agrupadores executivos. Colunas por agrupador + métricas (contagem por categoria, taxa local de pareamento, soma de valores por lado, diferença líquida, diferença absoluta).

**Ordenação default:** maior |Diferença líquida consolidada| primeiro (T-RANK, empate por ordem alfabética do primeiro agrupador).

### 6.4 Aba 3 · Pareamentos

Todos os pareamentos resolvidos, uma linha por pareamento. **Ordem canônica:** por categoria (Conciliado → Divergência de valor → Conciliado por valor → Pareamento frágil), dentro de cada categoria por score decrescente, empate por T-RANK (linha original crescente).

**Colunas (blocos):**

- **Identificador:** `Linha_orig` (na Base Investigada) · `Linha_busca` (na Base de Busca).
- **[Origem] — todas as colunas originais da base Origem** (prefixo `[Origem]` para desambiguar colisões de nome).
- **Separador visual** (coluna vazia estreita).
- **[Comparado] — todas as colunas originais da base Comparado** (prefixo `[Comparado]`).
- **Valores conciliados:** `Valor_orig` · `Valor_busca` · `Diferença` · `Tolerância_absorveu` (sim/não).
- **Evidência textual:** `Texto_composto_orig` · `Texto_composto_busca` · `Score_aderência` · `Categoria`.
- **Warnings da linha:** concat de flags W-V11-* aplicáveis àquela linha (separador `·`).

Motivo da estrutura completa (todas as colunas originais, não subset): auditabilidade máxima; sistema não decide o que é "colateral" para o analista.

Warning **W-V11-PAREAMENTO-LARGO** — dispara quando o Excel gerado ultrapassa 50 colunas; sugere analista configurar subset na próxima execução (default persiste em "todas as colunas").

### 6.5 Aba 4 · Sem par

Registros que não foram pareados em nenhum dos dois passes. **Estrutura em dois blocos verticais**, espelhando o caso-referência Protheus × Safra:

- **Bloco 1:** Título "Registros de [Origem] sem par em [Comparado]" + cabeçalhos de colunas da base Origem + lista dos registros (ordem original da aba-fonte).
- **Linha em branco + separador visual.**
- **Bloco 2:** Título "Registros de [Comparado] sem par em [Origem]" + cabeçalhos de colunas da base Comparado + lista dos registros.

Nomes de blocos usam os nomes customizados via T-02 (se editados).

### 6.6 Aba 5 · Ponte de Conciliação (condicional)

Aparece apenas se os quatro campos de saldo foram declarados. Estrutura em 3 blocos herdada do caso-referência:

**Bloco 1 · Diferença de saldo anterior**
- Saldo anterior [Origem]: R$ X
- Saldo anterior [Comparado]: R$ Y
- Diferença de saldo anterior ([Origem] − [Comparado]): R$ (X − Y)

**Bloco 2 · Impacto líquido dos movimentos únicos**
- Soma dos movimentos só em [Origem]: R$ Z
- Soma dos movimentos só em [Comparado]: R$ W
- Impacto líquido ([Origem] − [Comparado]): R$ (Z − W)

**Bloco 3 · Conferência**
- Saldo final [Origem]: R$ A
- Saldo final [Comparado]: R$ B
- Diferença final real ([Origem] − [Comparado]): R$ (A − B)
- Diferença final esperada (Diferença saldo anterior + Impacto líquido): R$ ((X − Y) + (Z − W))
- **Conferência** (Diferença real − Diferença esperada): precisa zerar. ✓ fecha · ⚠ resíduo.

Épsilon: R$ 0,01 para conferência.

Microcopy declarativa no topo da aba (sem referência a V1): "A Ponte reconcilia o saldo inicial e final de cada lado com o impacto dos movimentos únicos. Complementar aos pareamentos."

Warning **W-V11-PONTE-RESIDUO** — dispara se Bloco 3 não zera. Indica movimento conciliado com divergência de valor absorvendo parte da diferença, ou inconsistência entre saldos declarados e movimentos da base.

### 6.7 Aba 6 · Diagnóstico (T-DIAG)

Padrão T-DIAG da Fundação, com conteúdo V11-específico em 6 seções:

**Seção 1 · Estrutura detectada** — Base (Origem/Comparado), arquivo, aba, linhas, colunas, data/hora.

**Seção 2 · Inferência de tipos** — colunas efetivamente usadas pela V11 com tipo inferido, nulos, cardinalidade, observação.

**Seção 3 · Configuração aplicada** — 3.1 Mapeamento semântico (colunas de valor mapeadas + polaridade + se foi default ou editado — W-V11-MAP-INFERIDO), 3.2 Composição de campos (declarações, campos-fonte, separador), 3.3 Tolerância por campo, 3.4 Score (pesos entre campos, limiares P1 e P2, customizações — W-V11-PESOS-CUSTOM, W-V11-LIMIAR-*), 3.5 Agrupadores executivos, 3.6 Saldos declarados para Ponte (se aplicável), 3.7 Modelo aplicado.

**Seção 4 · Processamento por passe**
- Passe 1: N tentativas, M matches com score ≥ Limiar P1, distribuição de scores.
- Passe 2: N resíduos processados, M matches com score ≥ Limiar P2, distribuição de scores.
- Registros sem par após os dois passes: Origem (N), Comparado (M).
- Tempo por passe e tempo total (diretrizes de performance D-032).

**Seção 5 · Higiene textual aplicada** — nota informativa: "T-FUZZY aplicou lowercase, remoção de acentos e remoção de caracteres não-alfanuméricos antes do cálculo de similaridade." Linha informativa única, não configurável.

**Seção 6 · Warnings disparados** — listagem de todos os warnings V11 com contagem e referência à linha/aba do detalhamento. Inclui eventual microcopy "Baixa aderência generalizada — operação NORMALIZE (Módulo 2, futuro) aborda esse caso quando disponível" se W-V11-MATCH-FRACO-MASS dispara.

---

## 7. Warnings catalogados (12)

Warnings V11 consolidados após refino (substitui lista candidata preliminar do GLOSSARIO):

| Código | Tipo | Gatilho |
|---|---|---|
| **W-V11-MAP-INFERIDO** | Informativo | Mapeamento semântico aceito por default sem edição explícita |
| **W-V11-TOL** | Material | Registros cuja correspondência foi viabilizada pela tolerância (valor não exato). Soma da diferença absorvida registrada |
| **W-V11-COMP-CAMPOS-NULOS** | Informativo | Composição contextual resultou em string vazia por nulos em todos os campos componentes |
| **W-V11-SEM-CONTEXTO** | Alerta | Menos de 2 campos contextuais configurados por lado — score depende de poucos sinais |
| **W-V11-PESOS-CUSTOM** | Informativo | Pesos entre campos contextuais customizados pelo usuário |
| **W-V11-LIMIAR-P1-CUSTOM** | Informativo | Limiar do Passe 1 customizado |
| **W-V11-LIMIAR-P2-CUSTOM** | Informativo | Limiar do Passe 2 customizado |
| **W-V11-MULT-CAND** | Informativo | Registros com N ≥ 2 candidatos resolvidos por score + T-RANK |
| **W-V11-VALOR-REPETIDO-MASS** | Alerta | > 30% dos valores aparecem 3+ vezes em alguma das bases (ambiguidade estrutural alta) |
| **W-V11-SCORE-LIMITE** | Informativo | Pareamentos com score na janela ±0,05 da fronteira entre categorias — candidatos a revisão manual |
| **W-V11-ALLOC-EMPATE** | Informativo | Alocação gulosa resolveu empate de score por T-RANK (lista os casos) |
| **W-V11-PAREAMENTO-LARGO** | Informativo | Excel gerado com > 50 colunas na aba Pareamentos — sugere configurar subset na próxima execução |
| **W-V11-PONTE-RESIDUO** | Alerta | Conferência da Ponte (Bloco 3) não zera |

---

## 8. Componentes transversais da Fundação

| Transversal | Uso em V11 | Status |
|---|---|---|
| **T-DUAL** | Entrada dual (duas bases, duas modalidades) | Formalizado · D-018 |
| **T-DIAG** | Aba Diagnóstico última (D-017) | Formalizado |
| **T-MODELO** | Configuração persistível como modelo | Formalizado · D-030 |
| **T-RANK** | Ranqueamento de candidatos por score; desempate na alocação gulosa | Formalizado · D-041 |
| **T-FUZZY** | Similaridade textual híbrida (trigramas + tokens-chave), API pura, pesos encapsulados | **Confirmado** · D-052 |
| **T-CONCAT** | Composição de campos contextuais; consumo V11 compartilhado com M2.CONCAT futuro | **Candidato** · D-053 (posicionamento final no G-FUND) |

V11 **não usa** T-AGRUPA (preserva registros individuais, análogo à V1).

---

## 9. Fronteira com Módulo 2 (TabloPrep)

| Cenário | Status | Tratamento |
|---|---|---|
| **RESHAPE** (bases empilhadas numa aba com coluna discriminadora) | Fora de escopo V11 (herança V1) | Exclusão estrutural no §3.2; M2 resolve antes da análise |
| **CONCAT** (composição de múltiplos campos em texto único) | Nativo V11 MVP | T-CONCAT candidato (D-053); posicionamento final no G-FUND |
| **NORMALIZE** (transformações semânticas declaradas: abreviações, stop-words, regex) | Fora de escopo V11 MVP | Higiene básica (lowercase · acentos · caracteres não-alfanuméricos) encapsulada em T-FUZZY; transformações semânticas ficam para M2 futuro |

Microcopy no Diagnóstico (Seção 6): quando alta incidência de pareamentos na categoria "Pareamento frágil" sinaliza padronização textual inconsistente — nota declarativa orienta analista a considerar operação NORMALIZE futura. Nenhuma sugestão aparece na configuração (não preventivo).

---

## 10. Pontos de atenção (riscos analíticos conhecidos)

- **Valores repetidos em alta proporção** (> 30% com 3+ ocorrências) aumentam ambiguidade estrutural. Warning W-V11-VALOR-REPETIDO-MASS sinaliza; analista pode filtrar ou refinar agrupadores.
- **Tolerância elevada gera falsos positivos de valor.** Microcopy orienta valor típico por contexto.
- **Composição contextual com campos nulos reduz qualidade do score.** W-V11-COMP-CAMPOS-NULOS e W-V11-SEM-CONTEXTO sinalizam.
- **Bases com histórico codificado** (abreviações internas, códigos numéricos) podem produzir scores artificialmente baixos — Diagnóstico sinaliza se muitos pareamentos ficam na categoria "Pareamento frágil"; analista pode acionar NORMALIZE futuro no M2.
- **Análise é orientada à descoberta, não à validação determinística.** Revisão manual da aba Pareamentos (especialmente categorias 2, 3 e 4) é parte do ciclo de uso — não é erro a evitar. C.5 aplicado: sistema apresenta, analista decide.

---

## 11. Relação com Fundação e retroação sobre V1

### 11.1 Requisitos novos para a Fundação

- **T-FUZZY como transversal** (confirmado · D-052) — implementação encapsulada da similaridade textual híbrida. Disponível para V1 via P-V1-02-Evo quando ativado (zero duplicação).
- **T-CONCAT candidato** (D-053) — posicionamento a decidir no G-FUND.
- **Extensão T-DUAL** — já formalizada em D-018; V11 usa sem novas exigências.
- **T-MODELO** — configurações V11 são persistíveis como modelo (padrão geral).
- **Motor probabilístico com arquitetura de dois passes** — alocação gulosa com T-RANK no desempate; API determinística.

### 11.2 Retroação sobre V1 (registrada)

DCV-V1 aprovado não menciona V11 (V11 ainda não existia na data de aprovação). Retroação pendente: adicionar bloco "Relação com V11" curto em §2 (Posicionamento analítico) do DCV-V1, com vocabulário declarativo simétrico ao §2.3 deste DCV. Execução: na próxima revisão natural de V1 (S-V1 ou atualização de DCV por demanda), **não é sessão dedicada imediata**.

---

## 12. Roadmap pós-MVP (P-V11-XX-Evo)

- **P-V11-01-Evo · Match por composição de lançamentos** — um registro corresponde à soma de múltiplos registros do outro lado (problema de subset sum).
- **P-V11-02-Evo · Alocação global ótima** — substituição do guloso por algoritmo Húngaro quando relevante.
- **P-V11-03-Evo · Tolerância percentual** — análogo a P-V1-05-Evo.
- **P-V11-04-Evo · Referência a coluna de saldo** — Ponte configurável via coluna de saldo + seleção de linha (primeiro/último), em vez de 4 campos digitados.
- **P-V11-05-Evo · Regra de dualidade** — múltiplas correspondências de valor via mesmo mapeamento (um único mapeamento cobrindo ENTRADAS → DEBITO e SAIDAS → CREDITO como regra geral).
- **P-V11-06-Evo · Aprendizado de mapeamento pós-revisão manual** — sistema aprende padrão quando usuário corrige pareamentos (depende da Fase 3 · IA).

---

## 13. Pendências do refino (histórico)

13 pendências estruturais fechadas em 2 sessões (19/04/2026):

**Bloco A · Fronteira e arquitetura da entrada** (Sessão 1)
- T-00 · Arquitetura de dois passes — D-051
- T-05 · Tolerância de valor com papel duplo — §4.3
- T-02 · Nomeação default dos lados — §3.1
- T-01 · Fronteira V1/V11 navegável — §2.3

**Bloco B · Coração técnico** (Sessão 1)
- T-03 · Mapeamento semântico de valor — §4.1
- T-04 · Composição de campos contextuais (T-CONCAT candidato) — §4.2 · D-053
- T-06 + T-11 · Algoritmo de score + T-FUZZY confirmado — §4.4 · D-052
- T-07 · Estratégia de alocação (guloso com ordem por melhor score) — §5.1
- T-08 · Classificação e taxonomia de produto (5 categorias) — §5.2

**Bloco C · Saída e fronteira** (Sessão 2)
- T-09 · Estrutura de abas do Excel — §6
- T-10 · Ponte de Conciliação opcional — §6.6 · §4.6
- T-12 · Fronteira com Módulo 2 — §9

**Referências cruzadas:** D-047 (V11 no escopo) · D-048 (ordem de refino) · D-049 (mapa de 12 temas) · D-050 (T-FUZZY candidato) · D-051 (dois passes) · D-052 (T-FUZZY confirmado) · D-053 (T-CONCAT candidato) · D-054 (sumário sessão 1) · D-055 (Bloco C · sumário sessão 2).

---

*DCV aprovado após 2 sessões de refino (19/04/2026). Próxima sessão da Fase 0: DCV-V3 (Família B · Sequência).*
