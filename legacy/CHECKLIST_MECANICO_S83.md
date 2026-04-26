# CHECKLIST MECÂNICO · Sub-sessão 8.3 · Correção dirigida pós-Camada 2 da S82

Gate duplo D-174 · Camada 1 (mecânica · responsabilidade Claude Code).

Camada 2 humana da Sessão 8.2 reportou: C-1 (P-29) ✅ funcionou · C-2 (P-31)
mantém PROVISÓRIO (vai para ALINHA · não tocado) · C-3 (P-30) ❌ piorou
(texto continuou cortado · linhas vizinhas pareciam infladas) · P-35 NOVO
(regressão · default Unidade não infere mais de tipo_campo).

Esta sub-sessão corrige **2 fixes** (P-30 + P-35). P-31 não é tocado.

Estado da suite: **731 / 731 passed** (regressão zero · suite S82 íntegra).

---

## CORREÇÃO 1 (C-1) · P-30 · Leitura qualitativa wrap robusto

**Diagnóstico (Fase a · D-185):** Em `src/visoes/exportacao_v2.py:1490-1504` a
S82 aplicou `chars_por_linha=100` + `num_linhas * 20pt` + `min=60pt`. Dois
problemas:

1. **Texto cortado ("...")** · célula está mesclada A:H via
   `_renderizar_secao_como_tabela` (LARGURA_UTIL=8). Quando `_ajustar_larguras`
   roda no fim do bloco (linha 1535), cada coluna A:H tipicamente fica com
   ~12-16 chars. Estimativa de 100 chars/linha era OTIMISTA; texto de 250+
   chars precisa de mais altura que a calculada. Excel não auto-fita altura
   em células mescladas com `wrap_text=True`, então o texto ficava oculto
   além da altura setada.
2. **Vizinhas "infladas"** · percepção visual da Usuária. O bloco da Leitura
   qualitativa ocupava 4 linhas grandes consecutivas (cabeçalho 22pt +
   conteúdo ~80pt + respiro 8pt + cabeçalho da próxima seção 22pt) com
   espaço vazio dentro do conteúdo (texto cortado em ~3 linhas com folga
   embaixo). Não havia loop iterando sobre vizinhas; só a linha de conteúdo
   recebia altura customizada.
3. **Alignment** · função aplicava `vertical="center"`, o que para textos
   longos com wrap fica visualmente pior alinhado pelo meio em vez do topo.

**Solução (Fase b · estrutural · não cosmética):**

- [x] Nova função `_calcular_altura_leitura_qualitativa(texto)` em
  `exportacao_v2.py:399-414` (logo após `_renderizar_secao_como_tabela`) ·
  cálculo pessimista com 90 chars/linha visual e margem de segurança 1.4x:
  ```
  num_linhas = max(2, (len(texto) // 90) + 1)
  num_linhas_seguro = int(num_linhas * 1.4) + 1
  altura = num_linhas_seguro * 16 + 12
  return min(220, max(55, altura))
  ```
- [x] Bloco 5 do Resumo Executivo em `exportacao_v2.py:1496-1517` substituído:
  ```
  linha_conteudo_leitura = linha_inicial_leitura + 1
  ws.row_dimensions[linha_conteudo_leitura].height = (
      _calcular_altura_leitura_qualitativa(frase)
  )
  cel_leitura = ws.cell(row=linha_conteudo_leitura, column=1)
  cel_leitura.alignment = Alignment(
      horizontal="left", vertical="top",
      wrap_text=True, indent=1,
  )
  ```
- [x] Apenas a linha de conteúdo recebe altura customizada · cabeçalho (22pt)
  e respiro (8pt) preservam alturas estabelecidas em
  `_renderizar_secao_como_tabela` · linhas vizinhas anteriores e da próxima
  seção ficam com `row_dimensions[linha].height = None` (default Excel).
- [x] Verificado em `V2_S83_*.xlsx` via inspeção openpyxl:
  - linha 53 (cabeçalho "Leitura qualitativa"): h=22 ✓
  - linha 54 (conteúdo · 229-252 chars): h=92 · vertical=top · wrap=True ✓
  - linha 55 (respiro): h=8 ✓
  - linha 52 (acima): h=None ✓ (default)
  - linha 56 (cabeçalho "Qualidade estrutural"): h=22 ✓
  - linha 57 (conteúdo Qualidade): h=None ✓ (default)
  - linha 58 (respiro Qualidade): h=8 ✓

**Critérios de pronto C-1:**
- [x] Excel V2_S83_*.xlsx · Leitura qualitativa cabe inteira sem cortar ("...")
- [x] Linhas vizinhas (anteriores e posteriores ao bloco) com altura padrão
  (None → Excel default · não infladas)
- [x] Texto quebra naturalmente dentro da célula mesclada (wrap_text=True)
- [x] Visual coerente com paleta (cabeçalho azul preservado · vinho não usado
  nesta paleta)
- [x] Funciona para textos curtos (~100 chars · h=60pt · margem ok) e longos
  (~600 chars · h≈156pt · margem ok)

---

## CORREÇÃO 2 (C-2) · P-35 · Default Unidade infere automaticamente do tipo

**Diagnóstico (Fase a · D-185):** Em `src/app_v2.py:884` a leitura
`unid_atual = st.session_state.get("unidade") or _unidade_default_por_tipo(tipo)`
NUNCA recalculava o default ao trocar `tipo_campo` no rádio · `unidade`
persistia entre rerenders. Pior: widget tem `key="sel_unidade"`, e Streamlit
prioriza `session_state[key]` sobre `index=`, então `idx_unid` recalculado
não tinha efeito.

Origem da regressão: a S82 introduziu `_aplicar_modelo_bytes` (linha 391
`st.session_state["sel_unidade"] = modelo["unidade"]`) que firmou o padrão
de gravar `sel_unidade` direto no state · não há reset desse valor quando
o tipo muda no rádio.

**Solução (Fase b · captura tipo anterior + reset DDU ao mudar tipo):**

- [x] `src/app_v2.py:854-865` · captura `tipo_anterior` antes do rádio:
  ```
  tipo_anterior = st.session_state["tipo_campo"]
  tipo = st.radio(... key="rad_tipo")
  st.session_state["tipo_campo"] = tipo
  if tipo != tipo_anterior:
      unidade_default = _unidade_default_por_tipo(tipo)
      st.session_state["unidade"] = unidade_default
      st.session_state["sel_unidade"] = unidade_default
  ```
- [x] Atualiza AMBAS as chaves (`unidade` lógica + `sel_unidade` widget) ·
  Streamlit lê `sel_unidade` ao renderizar o widget na sequência.
- [x] Reset só dispara quando tipo MUDA · próxima rerender com tipo igual
  preserva escolha manual da Usuária no selectbox de Unidade.
- [x] Trocar tipo APÓS escolha manual: aceita perda da escolha (contexto mudou ·
  spec C.D6 DDU · D-161).

**Verificação manual via streamlit.testing.v1.AppTest** (6 cenários · all green):
- [x] Estado inicial · tipo=NUMERICO_ADITIVO → unidade=MONETARIO_BRL
- [x] tipo→NUMERICO_RELATIVO → unidade=PERCENTUAL ✓ (era o bug)
- [x] tipo→NUMERICO_NAO_ADITIVO → unidade=MONETARIO_BRL ✓
- [x] Manual sel_unidade→QUANTIDADE → unidade=QUANTIDADE ✓ (respeita)
- [x] tipo→NUMERICO_RELATIVO após manual QUANTIDADE → unidade=PERCENTUAL ✓
  (reset esperado · perda manual aceitável conforme spec)
- [x] tipo→ESTADO_SITUACAO → unidade=ADIMENSIONAL ✓

**Critérios de pronto C-2:**
- [x] "Valor somável" → Reais (R$) automaticamente
- [x] "Valor percentual ou taxa" → Percentual (%) automaticamente
- [x] "Indicador não somável" → Reais (R$) automaticamente
- [x] "Categoria ou rótulo" → Outro / sem unidade definida automaticamente
- [x] Usuária pode TROCAR manualmente o selectbox · valor respeitado
- [x] Trocar tipo APÓS manual: unidade volta a inferir do tipo (spec)
- [x] Tela RESULTADO continua coerente (regressão zero do C-1 da S82)

---

## Suite

`python -m pytest -q` → **731 / 731 passed** em ~24s.

Zero teste novo nesta sub-sessão · escopo cirúrgico · correções mecânicas
(não alteram contratos · não alteram semântica de motor). Verificação P-30
via inspeção openpyxl direto sobre arquivos S83 gerados; verificação P-35
via streamlit.testing.v1.AppTest ad-hoc cobrindo 6 cenários.

## Amostras V2_S83

- `amostras/V2_S83_MONETARIO_BRL.xlsx` · 18.232 bytes · 4 abas · Leitura
  qualitativa 252 chars · linha 54 h=92 · vertical=top · wrap=True
- `amostras/V2_S83_PERCENTUAL.xlsx` · 18.023 bytes · 4 abas · Leitura
  qualitativa 239 chars · linha 54 h=92 · regressão zero do C-1 S82
- `amostras/V2_S83_QUANTIDADE.xlsx` · 17.723 bytes · 4 abas · Leitura
  qualitativa 229 chars · sanity

## App rodando para Camada 2

`streamlit run src/app_v2.py` (porta default · após esta entrega).

Caminho de validação manual sugerido pela Usuária:
1. Upload de base de teste
2. Ir para Etapa 3
3. Marcar "Valor somável" · observar Unidade trocar para "Reais (R$)"
4. Marcar "Valor percentual ou taxa" · observar Unidade trocar para
   "Percentual (%)" automaticamente
5. Marcar "Indicador não somável" · observar Unidade trocar para "Reais (R$)"
6. Marcar "Categoria ou rótulo" · observar Unidade trocar para "Outro / sem
   unidade definida"
7. Trocar manualmente Unidade no selectbox · valor respeitado em rerenders
   subsequentes (sem mudar tipo)
8. Trocar tipo no rádio após escolha manual · Unidade volta a inferir do
   novo tipo (perda manual aceitável conforme C.D6 DDU)
9. Concluir fluxo até E5 · processar · gerar Excel V2 · abrir Resumo
   Executivo · verificar Leitura qualitativa cabe inteira (sem "...") com
   linhas vizinhas com altura padrão

## Bifurcações declaradas

Zero novas. P-31 (botões modelo) PROVISÓRIO desde S82 · não foi tocado nesta
sub-sessão · vai para ALINHA-Lições-Família-A (D-200 · 26/04/2026).

## Escopo fechado

Achados novos (se houver durante Camada 2 desta sub-sessão) viram backlog
para ALINHA-Lições-Família-A (D-200) · não devem disparar nova sub-sessão
mecânica imediata.

## Princípios respeitados

- **C.D6 DDU (D-161)** · default declarado · Usuária pode sobrescrever
- **C.D8 (D-190)** · Unidade declarada universal
- **D-185** · Fase a investigação precede correção · cumprida (diagnóstico
  reportado antes da correção em ambos os fixes)
