# V-V1 · Auditoria da Base de Fundação · Fase 7

**Sessão:** V-V1 · Fase 7 · auditoria YAML Q1.A
**Produzido por:** Claude Code · 2026-04-26
**Base auditada:** `bases/base_fundacao.xlsx` · abas `dual_origem_crm` (110 linhas) · `dual_comparado_erp` (105 linhas)
**Pretendido:** ler entrada V1 atual de `casos_esperados.yaml` · executar pipeline V-V1 sobre a base · documentar discrepâncias · reescrever entrada V1 coerente com S-V1 v2 + comportamento empírico observado.

---

## 1 · Discrepâncias entre o YAML pré-existente e S-V1 v2

A entrada V1 atual em `casos_esperados.yaml` (linhas 47-78) é pré-D-213. Discrepâncias detectadas:

| # | Item no YAML pré-existente | Realidade S-V1 v2 |
|---|---|---|
| 1 | Cita warning `W-V1-NOME-COLUNA-DIVERGENTE` (V1-A06) | Esse código **não existe** no catálogo W-V1-* (S-V1 §2.7 só lista W-V1-TOL · DUP · AMB · UNIDADE). É lixo herdado de pré-D-213. |
| 2 | "Match exato em ~70% das linhas (65-75%)" (V1-A01) | Empiricamente o match não chega a 65% com a configuração canônica disponível · vide §3 desta auditoria. |
| 3 | "Ambiguidade potencial · 2 pares com match ambíguo" (V1-A05) | Empiricamente há **0 ambiguidade** com agrupador `Conta+Centro_Custo` em modo EXATO. Ambiguidade só aparece em modos não-EXATO. |
| 4 | Não distingue `ABAS_DISTINTAS` vs `MESMA_ABA_EM_COLUNAS` | D-213 introduz 2 ramos lógicos · YAML deve declarar pelo menos `ABAS_DISTINTAS` explícito. |
| 5 | "Resumo Executivo tem 6 blocos" (V1-A07) | Correto (6 blocos da Fundação · §13.5) mas o coração visual é "Mapa de Conciliação" — confirma. |

---

## 2 · Inspeção estrutural da base

### 2.1 · Aba `dual_origem_crm` · 110 linhas

| Coluna | Tipo aparente | Observação |
|---|---|---|
| `Conta` | string `CC-NNNN` | 29 valores únicos · 24 com duplicidade |
| `Centro_Custo` | string categórico | ~6 categorias (COMERCIAL · MARKETING · OPERACOES · RH · etc) |
| `Cliente` | string | Nome amigável do cliente |
| `Valor` | float (R$) | Valor monetário da transação |
| `Data` | string mista | Mistura formatos: `31/01/2025` · `2025-01-31` · `jan/2025` (proposital · stress test) |

### 2.2 · Aba `dual_comparado_erp` · 105 linhas

Estrutura paralela com diferenças:
- Coluna do nome cliente é `Razao_Social` (não `Cliente`) · diferença proposital
- Mesma mistura de formato em `Data`
- 28 valores únicos em `Conta` · 25 com duplicidade

### 2.3 · Hipótese sobre o desenho da base

A base parece ser **transacional** (1 linha = 1 transação contábil) · não cadastral (1 linha = 1 entidade). Por isso `Conta` é altamente repetido. Uniqueness razoável só vem de chave composta `Conta + Centro_Custo + Data` · mas mesmo assim restam ~9 duplicatas em origem.

**Implicação para V-V1:** a base **stresseia DUPLICIDADE detection** mais do que conciliação clássica de saldos. CONCILIADO em modo EXATO é raro neste dataset porque exigiria coincidência exata em todas as colunas-chave declaradas.

---

## 3 · Execução empírica do pipeline V-V1

### 3.1 · Configuração canônica adotada

```yaml
caso_logico_inferido: ABAS_DISTINTAS  # n_arquivos=1, abas distintas
agrupadores_match:
  - {nome_origem: "Conta", nome_comparado: "Conta", modo: EXATO}
  - {nome_origem: "Centro_Custo", nome_comparado: "Centro_Custo", modo: EXATO}
campos_comparados:
  - {nome_origem: "Valor", nome_comparado: "Valor", tipo: VALOR_MONETARIO, unidade: MONETARIO_BRL, tolerancia: 0.01}
agrupadores_executivos: ["Centro_Custo"]
epsilon_por_unidade: {MONETARIO_BRL: 0.01}
```

### 3.2 · Saída do `executar_v1()` · contagens

| Classificação | Contagem observada |
|---|---|
| CONCILIADO | **0** |
| DIVERGENTE_VALOR | **10** |
| SO_ORIGEM | **36** |
| SO_COMPARADO | **44** |
| DIVERGENCIA_DUPLICIDADE | **44** |
| DIVERGENCIA_AMBIGUIDADE | **0** |
| **Total registros** | **134** |
| **n_processados (físico)** | **205** (110 origem + 105 comparado − 10 pares matched − 44 dups + ...) |

### 3.3 · Métricas adicionais

- `cobertura_origem_pct`: 100% (todas as 110 origem participam de algum par/dup, dado que `n_origem_sem_par = SO_ORIGEM = 36` e `n_origem_com_par = 110 - 36 = 74`)
- `cobertura_comparado_pct`: 100% análogo
- `diferenca_liquida` (campo Valor): **R$ -106.582,53**
- `status_ponte_geral`: **FECHA** (resíduo R$ 0,00)
- W-V1-TOL: 0 ocorrências
- W-V1-DUP: 44 ocorrências (chaves duplicadas)
- W-V1-AMB: 0 ocorrências

### 3.4 · Caso lógico MESMA_ABA_EM_COLUNAS

A base de Fundação **não tem aba projetada para testar MESMA_ABA_EM_COLUNAS** (D-213 caso 3). A criação de uma aba sintética está fora do escopo de V-V1 (motor) · esta é tarefa para A-V1 ou sub-sessão dedicada antes de VV-V1.

**Lacuna registrada como pré-requisito para A-V1.**

---

## 4 · Entrada V1 reescrita (a substituir no YAML)

Versão coerente com S-V1 v2 e comportamento empírico observado. Faixas de tolerância de ±2 absorvem variações pequenas (zeros à esquerda na Conta, parsing de Data, etc) sem invalidar a auto-validação.

```yaml
  V1:
    descricao: "Confronto entre bases · Família A · D-213 · S-V1 v2.0 · 2 ramos lógicos (ABAS_DISTINTAS · MESMA_ABA_EM_COLUNAS)"
    abas_consumidas: ["dual_origem_crm", "dual_comparado_erp"]
    aba_unica_caso_3: null  # MESMA_ABA_EM_COLUNAS · base atual não tem aba dedicada · pré-req A-V1
    config_canonica:
      caso_logico_inferido: "ABAS_DISTINTAS"
      agrupadores_match:
        - {nome_origem: "Conta", nome_comparado: "Conta", modo: "EXATO"}
        - {nome_origem: "Centro_Custo", nome_comparado: "Centro_Custo", modo: "EXATO"}
      campos_comparados:
        - {nome: "Valor", tipo: "VALOR_MONETARIO", unidade: "MONETARIO_BRL", tolerancia: 0.01}
      agrupadores_executivos: ["Centro_Custo"]
    assertions:
      - id: "V1-A01"
        tipo: "contagem_categoria"
        descricao: "ABAS_DISTINTAS · DIVERGENTE_VALOR · faixa empírica (config canônica)"
        classificacao: "DIVERGENTE_VALOR"
        esperado: {min: 8, max: 12}
      - id: "V1-A02"
        tipo: "contagem_categoria"
        descricao: "ABAS_DISTINTAS · SO_ORIGEM · faixa empírica"
        classificacao: "SO_ORIGEM"
        esperado: {min: 34, max: 38}
      - id: "V1-A03"
        tipo: "contagem_categoria"
        descricao: "ABAS_DISTINTAS · SO_COMPARADO · faixa empírica"
        classificacao: "SO_COMPARADO"
        esperado: {min: 42, max: 46}
      - id: "V1-A04"
        tipo: "contagem_categoria"
        descricao: "ABAS_DISTINTAS · DIVERGENCIA_DUPLICIDADE · base é heavily duplicated em Conta"
        classificacao: "DIVERGENCIA_DUPLICIDADE"
        esperado: {min: 42, max: 46}
      - id: "V1-A05"
        tipo: "contagem_categoria"
        descricao: "ABAS_DISTINTAS · CONCILIADO · esperado 0 com modo EXATO (pareamento perfeito raro)"
        classificacao: "CONCILIADO"
        esperado: {min: 0, max: 2}
      - id: "V1-A06"
        tipo: "contagem_categoria"
        descricao: "ABAS_DISTINTAS · DIVERGENCIA_AMBIGUIDADE · 0 em modo EXATO (set semantics · S-V1 §2.2)"
        classificacao: "DIVERGENCIA_AMBIGUIDADE"
        esperado: {valor: 0}
      - id: "V1-A07"
        tipo: "warning_presente"
        descricao: "W-V1-DUP · base tem chaves duplicadas em ambos lados (44 chaves)"
        esperado: {warning_code: "W-V1-DUP", min: 42, max: 46}
      - id: "V1-A08"
        tipo: "warning_presente"
        descricao: "W-V1-TOL · 0 ocorrências (base sem matches dentro de tolerância)"
        esperado: {warning_code: "W-V1-TOL", valor: 0}
      - id: "V1-A09"
        tipo: "warning_presente"
        descricao: "W-V1-AMB · 0 ocorrências em modo EXATO"
        esperado: {warning_code: "W-V1-AMB", valor: 0}
      - id: "V1-A10"
        tipo: "estrutura_saida"
        descricao: "Coração Visual · Mapa de Conciliação · 6 blocos do RE da Fundação"
        esperado: {resumo_blocos: 6, coracao_visual: "Mapa de Conciliação"}
      - id: "V1-A11"
        tipo: "status_ponte"
        descricao: "Status da Ponte com configuração canônica · esperado FECHA (resíduo absorvido por SO_*)"
        esperado: {status: "FECHA"}
      - id: "V1-A12"
        tipo: "diferenca_liquida"
        descricao: "Σ origem − Σ comparado · faixa empírica · valor negativo (Comparado > Origem)"
        esperado: {min: -120000.0, max: -90000.0, unidade: "MONETARIO_BRL"}
```

---

## 5 · Resumo das mudanças no YAML

| Mudança | Razão |
|---|---|
| Removido `W-V1-NOME-COLUNA-DIVERGENTE` (V1-A06 antigo) | Warning não existe em S-V1 v2 |
| Adicionado `caso_logico_inferido: "ABAS_DISTINTAS"` no contrato | D-213 introduz 2 ramos · YAML deve declarar |
| Adicionado bloco `config_canonica` | Reprodutibilidade: testes podem reconstruir o cenário canônico |
| 12 assertions cobrindo 6 classes + 3 warnings + estrutura + ponte + diff_liquida | Cobertura completa do contrato V1 |
| `aba_unica_caso_3: null` documentado | Lacuna conhecida · pré-req A-V1 |
| Faixas (`min`/`max`) ao invés de valores exatos | Robustez a pequenas variações de parsing (Data mista) |

---

## 6 · Lacuna documentada

**MESMA_ABA_EM_COLUNAS não tem aba na base de Fundação.** Para fechar a cobertura matricial empírica, A-V1 (ou sessão dedicada antes de VV-V1) deve adicionar uma aba sintética ao `base_fundacao.xlsx` (sugestão: `dual_mesma_aba_colunas`) com colunas duplicadas (Conta_Origem · Conta_Comparado · Valor_Origem · Valor_Comparado etc) e estender a entrada V1 do YAML para cobrir esse caso lógico. Tarefa registrada como **pré-requisito A-V1** · não-V-V1.

---

*Fim da auditoria · Fase 7 concluída · próximo passo: substituir entrada V1 no YAML e validar parseamento.*
