# spec_base_v2.md — Bloco B-2: Base Sintética de Validação da V2

## Identificação
- **Bloco:** B-2
- **Arquivo de saída:** `bases/base_v2.xlsx`
- **Script gerador:** `bases/gerar_base_v2.py`
- **Propósito:** base sintética de validação da Visão V2 (Análise Comparativa entre Referências)
- **Consumida por:** `src/visao_v2.py` (já implementada) e futuro `src/app_v2.py`
- **Dependências:** `openpyxl`, `pandas`

---

## Objetivo

Produzir uma base Excel sintética, em domínio de Vendas, que permita validar de ponta a ponta
a Visão V2 (Análise Comparativa entre Referências) — cobrindo as duas estruturas de entrada
(POR_COLUNAS e POR_LINHAS), os três tipos de campo (VALOR, INDICE, PERCENTUAL pode ser
simulado por Ticket Médio), as três semânticas (MAIOR_E_MELHOR, MENOR_E_MELHOR, NEUTRO)
e todas as seis classificações possíveis (MELHORA, PIORA, SEM_VARIACAO, VARIACAO_NEUTRA,
SURGIMENTO, DESAPARECIMENTO), além dos warnings W01–W05 previstos em `spec_v2.md`.

A base é **cirurgicamente construída** — cada linha tem um propósito de validação declarado
na coluna `caso_esperado`, e o volume total fica na faixa de **150–250 linhas** por aba para
simular um caso corporativo realista sem inflar desnecessariamente.

---

## Estrutura do arquivo

O arquivo `base_v2.xlsx` deve conter **4 abas**:

### Aba 1 — `POR_COLUNAS_TEMPORAL`
Estrutura POR_COLUNAS, comparação temporal (Jan/24 vs. Jan/25).

### Aba 2 — `POR_COLUNAS_PLAN_REAL`
Estrutura POR_COLUNAS, comparação Planejado vs. Real (Orçado vs. Realizado).

### Aba 3 — `POR_LINHAS_TEMPORAL`
Estrutura POR_LINHAS, com coluna discriminadora `Periodo` contendo `"Jan/24"` e `"Jan/25"`.

### Aba 4 — `POR_LINHAS_PLAN_REAL`
Estrutura POR_LINHAS, com coluna discriminadora `Cenario` contendo `"Orcado"` e `"Realizado"`.

> **Regra:** cada aba deve ser autossuficiente — os dados de uma aba não dependem de outra.

---

## Domínio de negócio

**Vendas corporativas** com a seguinte estrutura conceitual:

- **Agrupadores (dimensões):**
  - `Filial` — 5 valores: `"SP"`, `"RJ"`, `"MG"`, `"RS"`, `"PR"`
  - `Linha_Produto` — 4 valores: `"Eletronicos"`, `"Vestuario"`, `"Alimentos"`, `"Casa"`
  - `Canal` — 3 valores: `"Loja"`, `"Online"`, `"Distribuidor"`
  - `Vendedor_ID` — alta cardinalidade (60+ valores únicos) — usado para acionar W02

- **Campos de medida (cobrindo os 3 tipos da V2):**
  - `Receita` — tipo `VALOR`, semântica `MAIOR_E_MELHOR` (R$, numérico positivo)
  - `Volume` — tipo `VALOR`, semântica `MAIOR_E_MELHOR` (unidades vendidas, inteiro positivo)
  - `Ticket_Medio` — tipo `INDICE`, semântica `MAIOR_E_MELHOR` (R$, numérico positivo)

> Ticket Médio é mantido como `INDICE` (não como `VALOR`) para forçar a validação do
> comportamento quando o campo não é aditivo — isso atende à nota da V2 sobre o resumo
> por agrupador em campos não-VALOR.

---

## Abas POR_COLUNAS — estrutura detalhada

### Aba 1 — `POR_COLUNAS_TEMPORAL` (~180 linhas)

**Colunas:**
| Coluna | Tipo | Descrição |
|---|---|---|
| `Filial` | text | Agrupador nível 1 |
| `Linha_Produto` | text | Agrupador nível 2 |
| `Canal` | text | Agrupador nível 3 |
| `Vendedor_ID` | text | Agrupador de alta cardinalidade (para W02) |
| `Receita_Jan24` | numeric | Valor A — Receita em Jan/24 |
| `Receita_Jan25` | numeric | Valor B — Receita em Jan/25 |
| `Volume_Jan24` | numeric | Valor A — Volume em Jan/24 |
| `Volume_Jan25` | numeric | Valor B — Volume em Jan/25 |
| `Ticket_Medio_Jan24` | numeric | Valor A — Ticket Médio em Jan/24 |
| `Ticket_Medio_Jan25` | numeric | Valor B — Ticket Médio em Jan/25 |
| `caso_esperado` | text | Descrição do cenário que esta linha valida |

### Aba 2 — `POR_COLUNAS_PLAN_REAL` (~180 linhas)

**Colunas:** mesma estrutura da Aba 1, mas com os pares `_Orcado` / `_Realizado`:
- `Receita_Orcado` / `Receita_Realizado`
- `Volume_Orcado` / `Volume_Realizado`
- `Ticket_Medio_Orcado` / `Ticket_Medio_Realizado`
- + agrupadores + `caso_esperado`

---

## Abas POR_LINHAS — estrutura detalhada

### Aba 3 — `POR_LINHAS_TEMPORAL` (~200 linhas, formato empilhado)

**Colunas:**
| Coluna | Tipo | Descrição |
|---|---|---|
| `Filial` | text | Agrupador |
| `Linha_Produto` | text | Agrupador |
| `Canal` | text | Agrupador |
| `Vendedor_ID` | text | Agrupador (para W02) |
| `Periodo` | text | **Discriminador** — valores: `"Jan/24"` ou `"Jan/25"` |
| `Receita` | numeric | Campo de valor |
| `Volume` | numeric | Campo de valor |
| `Ticket_Medio` | numeric | Campo de valor (INDICE) |
| `caso_esperado` | text | Descrição do cenário |

> Cada chave única (Filial + Linha_Produto + Canal + Vendedor_ID) aparece, em regra,
> duas vezes — uma com `Periodo = "Jan/24"` e outra com `Periodo = "Jan/25"` —
> EXCETO nos casos propositais de W05 (registros sem par).

### Aba 4 — `POR_LINHAS_PLAN_REAL` (~200 linhas)

**Colunas:** mesma estrutura da Aba 3, mas com discriminador `Cenario`
contendo `"Orcado"` e `"Realizado"`.

---

## Cenários obrigatórios por aba

Cada aba deve conter, **no mínimo**, pelo menos uma linha (ou par de linhas, no POR_LINHAS)
para cada um dos cenários abaixo. A coluna `caso_esperado` identifica o cenário. Use os
rótulos exatos listados para permitir validação automatizada.

### Classificações (5 casos obrigatórios + 1 derivado)

| Rótulo `caso_esperado` | Descrição | Como construir |
|---|---|---|
| `MELHORA_CLARA` | Valor B > Valor A (direção positiva para MAIOR_E_MELHOR) | Ex.: Receita_A=1000, Receita_B=1300 |
| `PIORA_CLARA` | Valor B < Valor A (direção negativa para MAIOR_E_MELHOR) | Ex.: Receita_A=1500, Receita_B=900 |
| `SEM_VARIACAO` | Valor A == Valor B, ambos > 0 | Ex.: Receita_A=1200, Receita_B=1200 |
| `SURGIMENTO` | Valor A == 0 (ou nulo), Valor B > 0 | Ex.: Receita_A=0, Receita_B=800 |
| `DESAPARECIMENTO` | Valor A > 0, Valor B == 0 (ou nulo) | Ex.: Receita_A=950, Receita_B=0 |
| `ZERO_ZERO` | Valor A == 0 e Valor B == 0 (classificação SEM_VARIACAO) | Ex.: Receita_A=0, Receita_B=0 |

### Warnings (5 casos obrigatórios)

| Rótulo `caso_esperado` | Warning esperado | Como construir |
|---|---|---|
| `W01_NULOS_ALTOS` | W01 — >20% nulos em A ou B | Marcar ~25% das linhas com valores nulos no campo Receita |
| `W02_CARDINALIDADE` | W02 — agrupador com >50 valores únicos | Usar `Vendedor_ID` com 60+ valores distintos |
| `W03_MUITOS_AGRUPADORES` | W03 — >3 agrupadores (validação na config, não na base) | Documentar no `caso_esperado` que a base permite configurar 4 agrupadores simultâneos |
| `W04_VALOR_A_ZERO` | W04 — registros com valor_A=0 (cobre variação % não calculável) | Já coberto pelo cenário `SURGIMENTO` |
| `W05_SEM_PAR` | W05 — em POR_LINHAS, registro sem contraparte | Uma chave aparece só como `"Jan/24"` OU só como `"Jan/25"` (nunca ambos) |

> **Nota:** W04 é naturalmente satisfeito pelo cenário `SURGIMENTO`. Marcar pelo menos
> 3 linhas com esse padrão para garantir detecção robusta.

### Cenários de VARIACAO_NEUTRA

Para validar a semântica `NEUTRO`, incluir pelo menos **5 linhas** com variação
evidente (tanto positiva quanto negativa) marcadas como `VARIACAO_NEUTRA_CANDIDATA`.
Na configuração da V2, o usuário escolherá semântica `NEUTRO` para algum campo
para validar esse caminho. Como a base não tem um campo naturalmente "neutro"
(Receita, Volume e Ticket Médio são todos MAIOR_E_MELHOR no domínio de Vendas),
**a validação de VARIACAO_NEUTRA é feita via configuração do usuário**, não via
campo específico da base.

### Cenários de distribuição normal

O restante das linhas (~70% da base) deve simular variações realistas com
`caso_esperado = "NORMAL"` — combinações orgânicas de MELHORA e PIORA, com
magnitudes variadas (pequenas, médias, grandes), garantindo que o resumo por
agrupador tenha diversidade analítica.

---

## Regras de geração

### 1. Reprodutibilidade
- Usar `random.seed(42)` e `numpy.random.seed(42)` no script gerador
- A base gerada deve ser **idêntica** em execuções sucessivas

### 2. Ordem de geração por aba
1. Gerar todos os cenários obrigatórios primeiro (classificações + warnings) com rótulo correto em `caso_esperado`
2. Completar com linhas `NORMAL` até atingir o volume-alvo (~180 linhas POR_COLUNAS, ~200 POR_LINHAS)
3. Embaralhar a ordem das linhas com `df.sample(frac=1, random_state=42).reset_index(drop=True)` — assim os casos-limite ficam espalhados, simulando uma base real

### 3. Consistência entre abas POR_COLUNAS e POR_LINHAS
- As abas POR_LINHAS **não precisam** ter os mesmos dados numéricos das abas POR_COLUNAS
- Cada par (temporal / plan-real) é independente entre as duas estruturas
- Mas os agrupadores e a lógica dos cenários são os mesmos

### 4. Valores realistas
- `Receita`: entre R$ 500 e R$ 50.000 (exceto casos de zero/surgimento)
- `Volume`: entre 10 e 2.000 unidades (inteiro)
- `Ticket_Medio`: entre R$ 20 e R$ 500
- Variações entre A e B: tipicamente entre -40% e +60% (exceto casos-limite)

### 5. Nulos
- No cenário `W01_NULOS_ALTOS`, usar `None` (Python) — `openpyxl` escreve como célula vazia
- Fora desse cenário, não inserir nulos aleatórios (base limpa)

### 6. Chave única para POR_LINHAS
- A chave analítica de cada registro é `Filial + Linha_Produto + Canal + Vendedor_ID`
- Cada chave deve aparecer **duas vezes** (uma por valor do discriminador),
  exceto no cenário `W05_SEM_PAR` (onde aparece só uma vez)

---

## Contrato do arquivo final

### `base_v2.xlsx` — estrutura
- 4 abas nos nomes especificados
- Linha 1 = cabeçalho (nomes de colunas)
- Linhas 2+ = dados
- Todas as células de `caso_esperado` preenchidas (nunca vazias)
- Formatação: nenhuma (sem cores, bordas ou formatos especiais — arquivo "cru")
- Encoding: UTF-8 (garantir que acentos em "Vestuário" → use "Vestuario" sem acento, ou teste com acento se o motor suportar — **decisão:** usar **sem acentos** para eliminar risco de encoding na validação)

### Distribuição mínima de cenários por aba (cada aba)
| Cenário | Mínimo de linhas |
|---|---|
| `MELHORA_CLARA` | 5 |
| `PIORA_CLARA` | 5 |
| `SEM_VARIACAO` | 3 |
| `SURGIMENTO` | 3 |
| `DESAPARECIMENTO` | 3 |
| `ZERO_ZERO` | 2 |
| `W01_NULOS_ALTOS` | ~25% do total |
| `W02_CARDINALIDADE` | n/a — garantido por Vendedor_ID com 60+ valores |
| `W05_SEM_PAR` (apenas POR_LINHAS) | 6 chaves sem par |
| `NORMAL` | ~70% do total |

---

## Script gerador — `bases/gerar_base_v2.py`

### Responsabilidade
- Construir as 4 abas conforme as regras acima
- Escrever `bases/base_v2.xlsx` usando `pandas.ExcelWriter` com engine `openpyxl`
- Imprimir no console um resumo de geração, por aba:
  - total de linhas
  - contagem de linhas por valor de `caso_esperado`
  - número de valores únicos em `Vendedor_ID` (validar que ≥ 50 para W02)
  - (apenas POR_LINHAS) número de chaves sem par (validar que ≥ 6)

### Estrutura sugerida
```python
# bases/gerar_base_v2.py
import random
import numpy as np
import pandas as pd

SEED = 42

def gerar_aba_por_colunas_temporal() -> pd.DataFrame: ...
def gerar_aba_por_colunas_plan_real() -> pd.DataFrame: ...
def gerar_aba_por_linhas_temporal() -> pd.DataFrame: ...
def gerar_aba_por_linhas_plan_real() -> pd.DataFrame: ...

def validar_aba(df: pd.DataFrame, nome_aba: str, estrutura: str) -> None:
    """Imprime resumo e valida cobertura mínima dos cenários."""
    ...

def main() -> None:
    random.seed(SEED)
    np.random.seed(SEED)

    abas = {
        "POR_COLUNAS_TEMPORAL":   gerar_aba_por_colunas_temporal(),
        "POR_COLUNAS_PLAN_REAL":  gerar_aba_por_colunas_plan_real(),
        "POR_LINHAS_TEMPORAL":    gerar_aba_por_linhas_temporal(),
        "POR_LINHAS_PLAN_REAL":   gerar_aba_por_linhas_plan_real(),
    }

    for nome, df in abas.items():
        estrutura = "POR_LINHAS" if "LINHAS" in nome else "POR_COLUNAS"
        validar_aba(df, nome, estrutura)

    with pd.ExcelWriter("bases/base_v2.xlsx", engine="openpyxl") as writer:
        for nome, df in abas.items():
            df.to_excel(writer, sheet_name=nome, index=False)

    print("\n✅ base_v2.xlsx gerada com sucesso em bases/base_v2.xlsx")

if __name__ == "__main__":
    main()
```

### Validações automáticas do script
Ao final, o script deve imprimir (e abortar com mensagem clara se algo falhar):
- Total de linhas por aba na faixa 150–250
- Todos os cenários obrigatórios presentes com a contagem mínima
- `Vendedor_ID` com ≥ 50 valores únicos em todas as abas
- Em POR_LINHAS: ≥ 6 chaves sem par
- `caso_esperado` sem valores vazios

---

## Restrições de implementação

1. **Apenas criar** `bases/gerar_base_v2.py` e executá-lo para produzir `bases/base_v2.xlsx`.
2. **Não modificar** nenhum arquivo existente (`motor_upload.py`, `motor_base.py`, `visao_v2.py`, etc.).
3. **Não implementar** testes da V2 neste bloco — apenas gerar a base.
4. **Não criar** `app_v2.py` — isso é o Bloco 8.
5. **Dependências:** apenas `pandas`, `numpy`, `openpyxl` (já disponíveis no ambiente).
6. **Determinismo:** a base gerada deve ser idêntica em cada execução (seed fixa).

---

## Pendências em aberto (não bloqueiam este bloco)

- **Consistência semântica Ticket_Medio vs. Receita/Volume:** em uma base realista,
  Ticket_Medio = Receita / Volume. Na base sintética, para permitir todos os cenários
  (ex.: Ticket_Medio com variação independente), essa consistência é **relaxada**.
  Documentar no comentário do script que os três campos são gerados **independentemente**
  para fins de teste — isso não afeta a V2 porque cada campo é comparado isoladamente.

- **Encoding de acentos:** decidido usar **sem acentos** nos valores categóricos
  (`"Vestuario"`, `"Eletronicos"`). Se houver necessidade de testar encoding,
  criar uma base auxiliar específica em bloco futuro.

- **Validação contra `visao_v2.py`:** este bloco produz a base. A validação
  ponta-a-ponta (executar V2 sobre cada aba e conferir se as classificações
  correspondem ao `caso_esperado`) será feita em bloco posterior (Bloco B-2b),
  ou embutida como teste manual no Bloco 8 (app_v2.py).

---

## Regras de sessão

1. Leia `CONTEXT.md` e `specs/spec_base_v2.md` antes de começar
2. Leia `specs/spec_v2.md` para entender a visão consumidora (apenas referência — não implementar lógica da V2 aqui)
3. Implemente **apenas** `bases/gerar_base_v2.py`
4. Execute o script e confirme que `bases/base_v2.xlsx` foi criado
5. Imprima o resumo de geração conforme definido acima
6. **Não leia** outros arquivos além dos três acima
7. **Não altere** nenhum arquivo existente

---

## Prompt de abertura para o Claude Code (Bloco B-2)

Cole este prompt ao abrir o Claude Code na pasta `/tabloflow/`:

```
Leia CONTEXT.md e specs/spec_base_v2.md antes de começar.
Leia specs/spec_v2.md apenas como referência do consumidor da base.
Não leia outros arquivos.

Implemente bases/gerar_base_v2.py conforme a spec.

Requisitos:
- Gerar 4 abas (POR_COLUNAS_TEMPORAL, POR_COLUNAS_PLAN_REAL,
  POR_LINHAS_TEMPORAL, POR_LINHAS_PLAN_REAL) no arquivo bases/base_v2.xlsx
- Domínio: Vendas (Receita, Volume, Ticket_Medio)
- 3 campos comparados cobrindo tipos VALOR + VALOR + INDICE
- Agrupadores: Filial, Linha_Produto, Canal, Vendedor_ID
- Volume: 150–250 linhas por aba
- Cobertura obrigatória de TODOS os cenários-limite com rótulo em caso_esperado
- Seed fixa 42 para reprodutibilidade
- Sem acentos nos valores categóricos
- Dependências: pandas, numpy, openpyxl

Ao final:
1. Execute o script
2. Mostre as primeiras 30 linhas de bases/gerar_base_v2.py
3. Imprima o resumo de geração completo (total de linhas por aba + contagem por caso_esperado + n_unicos Vendedor_ID + chaves sem par nas abas POR_LINHAS)
4. Confirme que bases/base_v2.xlsx foi criado
```
