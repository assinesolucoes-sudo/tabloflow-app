# CHECKLIST MECÂNICO · Sub-sessão 8.4 · Reposicionar gráfico (P-36)

Gate duplo D-174 · Camada 1 (mecânica · responsabilidade Claude Code).

Camada 2 humana da S83 reportou: P-30 ✅ resolvido · P-35 ✅ resolvido · P-36
NOVO (BarChart "Variações em destaque" 16cm × 22cm ancorado entre tabela top
e Leitura qualitativa sobrepunha L53-54 e L56-57). Decisão Caminho α: mover
bloco gráfico para o final do Resumo Executivo com cabeçalho próprio.

Estado da suite: **731 / 731 passed** (regressão zero · suite S83 íntegra).

---

## CORREÇÃO ÚNICA (C-1) · P-36 · Reposicionar gráfico para o fim

**Diagnóstico (Fase a · D-185):** Tudo está em uma função única
`_renderizar_resumo_executivo_v2` em `src/visoes/exportacao_v2.py`
(linha 1201). Ordem antiga (S83) era sequencial:

1. Cabeçalho/data (1219-1236)
2. Números principais cards (1238-1294)
3. Saúde / Concentração / Onde se concentra (1296-1318)
4. **Variações em destaque · TABELA** (1320-1415)
5. **Tabela auxiliar (sem cabeçalho de seção) + BarChart** (bloco
   `if top_list:`) — `chart.height=16cm` × `chart.width=22cm` ancorado
   em `D{linha_aux_header + 2}` ≈ L42, estendia até ~L72 (≈30 linhas
   Excel a 0.529cm/linha 15pt) · sobrepunha Leitura qualitativa (L53)
   e Qualidade estrutural (L56)
6. Leitura qualitativa (1497-1526)
7. Qualidade estrutural (1528-1554)

`linha = linha_aux_dados_fim + 2` (pulava só a tabela auxiliar até L50,
não o gráfico flutuante de 30 linhas). Tabela auxiliar e BarChart estão
no MESMO bloco `if top_list:` · `criar_grafico_top_variacoes` é importado
de capability 11 (linha 57 do arquivo).

**Solução (Fase b · estrutural · não cosmética):**

- [x] Bloco `if top_list:` removido da posição entre passo 4 (tabela top)
  e passo 5 (Leitura qualitativa) · `exportacao_v2.py:1417-1495` extraídas
- [x] Nova seção 7 inserida APÓS Qualidade estrutural · antes de
  `_ajustar_larguras` e `freeze_panes`:
  ```
  if top_list:
      linha = _renderizar_cabecalho_secao(
          ws, linha, 1, LARGURA_UTIL,
          "Variações em destaque · gráfico", paleta,
      )
      linha_aux_header = linha
      # ... header estilizado (Rótulo · Diferença) com fill cor_secundaria
      # + font cor_destaque + bordas + alignment ...
      # ... 10 linhas de dados (top_list) com zebra + bordas ...
      chart = criar_grafico_top_variacoes(
          ws, anchor_cell=f"D{linha_aux_header}",
          dados_range=f"A{linha_aux_header}:B{linha_aux_dados_fim}",
          ...
      )
      chart.height = 16  # cm preservado
      chart.width = 22   # cm preservado
      linha = max(linha_aux_dados_fim, linha_aux_header + 12) + 3
  ```
- [x] Cabeçalho da seção usa `_renderizar_cabecalho_secao` (mesma função das
  demais seções) → mesmo style: fill `paleta.cor_primaria` · font branca
  negrito · h=22pt · merge A:H
- [x] Header da tabela auxiliar agora estilizado (não mais texto cru): fill
  `paleta.cor_secundaria` + font `paleta.cor_destaque` negrito + bordas +
  alignment left/right · padrão consistente com o header da tabela top
- [x] Body da tabela auxiliar com zebra + bordas finas · alignment
  proper (rótulo left, diferença right)
- [x] BarChart ancorado em `D{linha_aux_header}` (à direita da tabela aux ·
  col D · mesma linha do header) · tamanho 8.7" × 6.3" preservado
- [x] Reserva de linhas vazias após o bloco: `max(linha_aux_dados_fim,
  linha_aux_header + 12) + 3` · cobre tabela (10 itens) e altura do
  gráfico (12 linhas Excel) com 3 linhas finais de respiro

**Verificação via inspeção openpyxl** sobre `V2_S84_*.xlsx`:

Ordem das seções (todas com h=22 · cabeçalhos coloridos):
- [x] L4 · Números principais
- [x] L8 · Saúde da comparação
- [x] L14 · Concentração
- [x] L19 · Onde se concentra · por Filial
- [x] L26 · Variações em destaque (tabela top · sem mudança)
- [x] L39 · Leitura qualitativa (subiu de L53 → L39 · regressão zero S83:
  h=92 · vertical=top · wrap=True · 252 chars MONETARIO/239 PERCENTUAL/
  229 QUANTIDADE)
- [x] L42 · Qualidade estrutural (subiu de L56 → L42)
- [x] L45 · **Variações em destaque · gráfico** (nova seção)
- [x] L46 · header tabela auxiliar (Rótulo · Diferença)
- [x] L47-L56 · 10 linhas de dados
- [x] BarChart anchor=L46 col D · 22cm × 16cm · estende ~30 linhas
  (L46-L76) · NÃO sobrepõe nenhuma seção (todas em L4-L42)

**Critérios de pronto C-1:**
- [x] Excel V2_S84_*.xlsx · ordem das seções correta (1→9)
- [x] BarChart NÃO sobrepõe NENHUMA seção (verificado: gráfico em L46-L76 ·
  todas as seções em L4-L42 · cabeçalho da nova seção em L45)
- [x] Cabeçalho "Variações em destaque · gráfico" mesmo visual das outras
  (vinho · h=22pt · merge A:H · fonte branca negrito)
- [x] Tabela auxiliar agora tem cabeçalho próprio · não está mais "órfã"
- [x] Regressão zero das outras seções (Leitura qualitativa preserva
  h=92pt · vertical=top · wrap=True como na S83)
- [x] Funciona nas 3 unidades (MONETARIO_BRL · PERCENTUAL · QUANTIDADE)

---

## Suite

`python -m pytest -q` → **731 / 731 passed** em ~24s.

Zero teste novo nesta sub-sessão · escopo cirúrgico · correção é puramente
posicional (não altera contratos · não altera semântica de motor).
Verificação P-36 via inspeção openpyxl direto sobre arquivos S84.

## Amostras V2_S84

- `amostras/V2_S84_MONETARIO_BRL.xlsx` · 18.260 bytes · 4 abas · gráfico
  isolado em L45-L76 · seções L4-L42 preservadas
- `amostras/V2_S84_PERCENTUAL.xlsx` · 18.047 bytes · 4 abas · idem
- `amostras/V2_S84_QUANTIDADE.xlsx` · 17.746 bytes · 4 abas · sanity

## App rodando para Camada 2

`streamlit run src/app_v2.py` (porta 8503).

Caminho de validação manual:
1. Upload de base de teste
2. Concluir fluxo até E5 · processar · gerar Excel V2
3. Abrir Resumo Executivo
4. Verificar ordem das seções (Números → Saúde → Concentração → Onde se
   concentra → Variações em destaque → Leitura qualitativa → Qualidade
   estrutural → Variações em destaque · gráfico)
5. Confirmar que BarChart fica isolado no fim · não invade nenhuma seção
6. Confirmar regressão zero das outras seções (visual idêntico ao S83
   exceto a posição do bloco gráfico)

## Bifurcações declaradas

Zero novas. Escopo é só reordenação visual · não altera contratos.

## Escopo fechado

Achados novos (se houver durante Camada 2 desta sub-sessão) viram backlog
para ALINHA-Lições-Família-A (D-200 · 26/04/2026).

## Princípios respeitados

- **D-185** · Fase a investigação precede correção (orquestração mapeada
  antes de mover · diagnóstico reportado)
- **C.1 (determinismo)** · regressão zero das seções não tocadas
  (Leitura qualitativa preserva h=92/top/wrap)
- **D-163** · Excel é o produto · ordem das seções afeta a leitura executiva
- **D-194** · 5 evoluções V2 preservadas · só posição visual de 1 muda
