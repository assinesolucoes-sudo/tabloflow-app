# CHECKLIST MECÂNICO · Sub-sessão 8.2 · Caminho γ · 3 fixes Camada 2

Gate duplo D-174 · Camada 1 (mecânica · responsabilidade Claude Code).

Camada 2 da Sessão 8.1 reprovou fechamento de V2 retroativa por 7 débitos
remanescentes (P-28..P-34). Caminho γ aprovado pela Usuária: sub-sessão 8.2
dirigida com escopo cirúrgico nos 3 bloqueantes (P-29 + P-30 + P-31). Demais 4
vão para ALINHA-Lições-Família-A (D-200) e backlog evolução.

Estado da suite: **731 / 731 passed** (regressão zero · suite S81 íntegra).

---

## CORREÇÃO 1 (C-1) · P-29 · Tela RESULTADO consome helpers de unidade

**Diagnóstico:** `_tela_resultado` em `src/app_v2.py` (linha 1195) renderizava 4
cards com labels hardcoded ("Total · X", "Diferença", "Variação %") e usava
`_fmt_moeda_br` direto · ignorava `comp.unidade` · com `unidade=PERCENTUAL` a
tela exibia "R$ 21,39" enquanto Excel mostrava "21,39%".

**Solução:**
- [x] Imports adicionados em `src/app_v2.py`: `formatar_diferenca_por_unidade`,
  `formatar_percentual_br`, `formatar_valor_por_unidade`, `label_total_card`,
  `rotulo_diferenca`, `rotulo_variacao`, `valor_total_card`,
  `_LABEL_SEMANTICA_SAUDE`, `_categorias_saude_para_exibir`
- [x] Cards 1-4 da tela RESULTADO consomem helpers · espelho exato do Resumo
  Executivo do Excel (`exportacao_v2.py:1206-1259`):
  - `n_pa` derivado de `v2.base_analitica["diferenca"].dropna().shape[0]`
  - `valor_orig_card`/`valor_comp_card` via `valor_total_card(...)` · divide
    por `n_pa` para PERCENTUAL
  - PERCENTUAL recalcula `dif_card`/`var_card` a partir das médias (não usa
    `ancora.diferenca_total` que é soma)
  - Card 1/2 usam `formatar_valor_por_unidade`
  - Card 3 usa `formatar_diferenca_por_unidade` + label `rotulo_diferenca`
  - Card 4 usa `formatar_percentual_br` + label `rotulo_variacao`
- [x] Bloco "Como os casos se distribuem" agora roteia por `tipo_campo`:
  - `ESTADO_SITUACAO` → mantém distribuição estrutural (texto e tabela
    preservados · regressão zero)
  - Numérico → renderiza "Saúde da comparação" usando
    `distribuicao_classificacoes_semanticas` + `delta_por_classificacao_semantica`
    + `_categorias_saude_para_exibir` · ordem MAIOR/MENOR_MELHOR via chaves
    qualitativas, NEUTRO via chaves neutras
  - PERCENTUAL: 3 colunas (Categoria · Casos · Participação) · oculta Δ total
  - Demais unidades: 4 colunas com Δ total formatado por unidade
- [x] "Variações em destaque" também consome unidade:
  - Headers `rotulo_diferenca(unidade)` e `rotulo_variacao(unidade)`
  - Format de Valor adapta ("R$ %.2f" · "%.2f%%" · "%d" · etc)
  - Diferença em PERCENTUAL multiplica por 100 e usa format `"%+.2f p.p"` →
    renderiza ex.: "-5,23 p.p"
- [x] MONETARIO_BRL · regressão zero confirmada (cards "Total · X" + "R$ X")
- [x] PERCENTUAL · cards "Média · X" + valores "%" · card 3 "Variação absoluta
  (p.p)" + valor "p.p" · suíte verde
- [x] QUANTIDADE · cards "Total · X" + valores inteiros

**Critérios de pronto C-1:**
- [x] Tela RESULTADO com unidade=MONETARIO_BRL preserva visual atual
- [x] Tela RESULTADO com unidade=PERCENTUAL mostra cards "Média · X" + "%"
- [x] Tela RESULTADO com unidade=QUANTIDADE mostra cards "Total · X" + inteiros
- [x] Card 3 mostra "Variação absoluta (p.p)" + "-1,84 p.p" para PERCENTUAL
- [x] Visual da tela RESULTADO bate com visual do Excel exportado
- [x] Bloco "Como os casos se distribuem" vira "Saúde da comparação" para
  numérico · 3 colunas para PERCENTUAL · 4 para outras

---

## CORREÇÃO 2 (C-2) · P-31 · Botões "Salvar como modelo" e "Aplicar modelo"

**Diagnóstico (Etapa 1):** Linhas 347 e 352 de `app_v2.py` continham
`st.button("Aplicar modelo", ...)` e `st.button("Salvar como modelo", ...)`
SEM nenhum `if` ao redor · nenhum callback · nenhum `on_click` · clicar
literalmente não produzia ação.

**Solução (Etapa 2 · CASO A · implementação leve):**
- [x] `import json` adicionado em `src/app_v2.py`
- [x] Conjunto `_MODELO_CHAVES` documenta 19 chaves do session_state que
  compõem um modelo de análise (E2 + E3 + E4 + thresholds editados).
  EXCLUI: v2_result, motor_result, hashes, flags UX
- [x] Helper `_modelo_atual_bytes()` serializa config corrente como JSON
  (com versão de modelo · `_modelo_versao: 1`)
- [x] Helper `_aplicar_modelo_bytes(data)` parseia JSON e popula
  session_state das chaves conhecidas · espelha `unidade` em `sel_unidade`
  para que o widget E3 leia o valor aplicado
- [x] "Salvar como modelo" agora é um `st.download_button` · arquivo
  `tabloflow_modelo_v2.json` · mantém disabled quando idx_etapa < E5
- [x] "Aplicar modelo" agora abre painel inline com `st.file_uploader`
  (controlado por flag `_show_aplicar_modelo`) · botões "Confirmar
  aplicação" + "Cancelar" · em sucesso, popula state e dispara `st.rerun()`
- [x] Mantém disabled atual ("vazio" para Aplicar · idx_etapa < E5 para
  Salvar) · não altera estados anteriores

**Critérios de pronto C-2 · CASO A:**
- [x] Salvar gera JSON baixável (com versão e 19 chaves)
- [x] Aplicar carrega JSON, popula session_state, redireciona via rerun
- [x] Clicar nos botões NÃO é mais sem feedback

---

## CORREÇÃO 3 (C-3) · P-30 · Leitura qualitativa quebra texto no Excel

**Diagnóstico:** Em `src/visoes/exportacao_v2.py:1471-1476`, a célula da
Leitura qualitativa é renderizada via `_renderizar_secao_como_tabela` que JÁ
aplica `wrap_text=True` · porém Excel não auto-fita altura quando openpyxl
escreve · sem `row_dimensions[].height` explícito o texto fica oculto e
parece que "não está quebrando".

**Solução (revista após Camada 2 reportar regressão):**

A primeira tentativa setou apenas a altura da linha (54px) mas a coluna A
continuava esticada (width=50) porque `_ajustar_larguras` lia o `len(texto)`
da Leitura qualitativa (master de merge A54:H54) e aplicava à coluna A
sozinha. Resultado: coluna A com 50 de largura distorcia toda a planilha
("fica tudo em uma única célula quebrando").

Causa raiz: `_ajustar_larguras` não distinguia masters de merges multi-col
de células singulares · texto de prosa que se estende visualmente por 8
colunas estava esticando uma única coluna.

- [x] Captura `linha_inicial_leitura` antes da chamada
- [x] Identifica linha de conteúdo como `linha_inicial_leitura + 1`
  (cabeçalho ocupa 1 linha)
- [x] Calcula altura proporcional: `chars_por_linha = 100` (estimativa
  conservadora para a largura combinada das 8 colunas após auto-fit) ·
  `num_linhas = max(2, len(frase) // 100 + 2)` ·
  `altura = max(60, num_linhas * 20)`
- [x] Aplica `ws.row_dimensions[linha_conteudo_leitura].height = altura`
- [x] **Fix raiz** · `_ajustar_larguras` agora pula masters de merges
  multi-coluna (`mr.bounds: max_col > min_col`) · usa `merged_cells.ranges`
  para construir conjunto de coordenadas (row, col) a ignorar · evita que
  textos de prosa estiquem a coluna do canto · cobre todas as abas e
  futuras visões VN
- [x] Verificado em V2_S82_*.xlsx: coluna A reduzida de 50 → 16 · linha
  54 com altura=80, wrap_text=True · texto de 229-252 chars cabe sem
  esticar a coluna

**Critérios de pronto C-3:**
- [x] Excel V2_S82_*.xlsx · Leitura qualitativa quebra texto automaticamente
- [x] Altura da linha ajustada para texto caber sem cortar
- [x] Usuária NÃO precisa esticar coluna manualmente
- [x] Visual coerente com cabeçalho vinho da seção (paleta inalterada)

---

## Suite

`python -m pytest src/testes -x -q` → **731/731 passed** em ~24s.

Zero teste novo nesta sub-sessão · escopo cirúrgico · todas as correções são
mecânicas (não alteram contratos ou semântica de motor). Verificação Excel
foi feita por inspeção via openpyxl direto sobre os arquivos S82 gerados.

## Amostras V2_S82

- `amostras/V2_S82_MONETARIO_BRL.xlsx` · 18.243 bytes · 4 abas · regressão zero
- `amostras/V2_S82_PERCENTUAL.xlsx` · 18.029 bytes · 4 abas · cards "Média"
  + "Variação absoluta (p.p)" + Saúde sem Δ total + Leitura qualitativa
  com wrap
- `amostras/V2_S82_QUANTIDADE.xlsx` · 17.732 bytes · 4 abas · sanity

## Bifurcações declaradas

Zero novas. CASO A (implementação leve dos botões modelo) foi entregue ·
não foi necessário recorrer ao CASO B (remoção + TODO).

## Escopo fechado

Demais 4 débitos da Camada 2 da Sessão 8.1 (P-28, P-32, P-33, P-34) seguem
para ALINHA-Lições-Família-A (D-200 · 26/04/2026 manhã) e backlog evolução.
