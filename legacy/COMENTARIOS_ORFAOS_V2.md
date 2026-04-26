# Comentários Órfãos · D-202 Etapa 8 · Auditoria Camada 2

Catálogo de comentários que descrevem decisões reais mas **não têm D-XXX
correspondente em DECISIONS.md**. Cada item é candidato a D-XXX retroativo
ou a remoção definitiva.

Status do trim:
- 6 prefixos temporais foram removidos (rationale técnico preservado).
- 9 itens abaixo permanecem como pendência para auditoria humana.

## Pendências (mantidos no código com prefixo trimado)

### CO-1 · `exportacao_v2.py:185` (`_ajustar_larguras` docstring)
**Texto remanescente:** "Pula masters de merges multi-coluna · o texto
de prosa (Leitura qualitativa, banners, narrativas mescladas em A:H)
se estende visualmente pela largura combinada das 8 colunas..."
**Pergunta:** qual decisão isso registrava? · candidato a D-XXX
"Auto-fit de coluna A não considera ranges mesclados" (Sessão 8.2).

### CO-2 · `exportacao_v2.py:765` (number_format diferenca PERCENTUAL)
**Texto remanescente:** "PERCENTUAL + tag 'diferenca': formato 'p.p' literal ·
valor cru (fração) precisa ser pré-multiplicado por 100 para renderizar."
**Pergunta:** qual decisão registrava (era "Sessão 8.1 · C-1")? · pode ser
parte de D-190 (C.D8 · unidade declarada universal) que cobre PERCENTUAL.

### CO-3 · `exportacao_v2.py:842` (totalsRow propaga number_format)
**Texto remanescente:** "Aplica number_format na linha de totais.
`criar_tabela_executiva` adiciona a totalsRow em `linha_fim + 1` com fórmulas
SUBTOTAL, mas não propaga number_format das células de dados."
**Pergunta:** decisão "totalsRow herda fmt da coluna" (Sessão 4-ter-bis · C-1) ·
candidata a D-XXX retroativo ou parte de D-175.

### CO-4 · `exportacao_v2.py:933` (number_format na totalsRow base analítica)
**Texto remanescente:** "number_format na totalsRow."
**Pergunta:** mesmo que CO-3 mas para a aba Base Analítica · poderia consolidar
como uma única decisão D-XXX.

### CO-5 · `exportacao_v2.py:1014` (Diagnóstico V2 bespoke)
**Texto remanescente:** "Cada seção é renderizada como bloco de tabela estilizada
(cabeçalho colorido + zebra + bordas), via helper `_renderizar_secao_como_tabela`."
**Pergunta:** decisão "C-4 (Sessão 4-ter-bis): seção como tabela" · candidata a
D-XXX OU promoção para capability F-APRESENT (já há TODO-FAPRESENT-CLEANUP
mencionando isso).

### CO-6 · `visao_v2.py:1353` (delta vs delta_soma)
**Texto remanescente:** "`delta` preserva soma (compatibilidade legada) ·
F-APRESENT escolhe `delta_soma` ou `delta_medio` conforme unidade."
**Pergunta:** decisão "Sessão 8.1 · C-3: campos novos preservam soma legada" ·
candidata a D-XXX (parte de evolução E3b ou evolução compatibilidade).

### CO-7 · `app_v2.py:1198` (achado de Sessão 3 sobre adaptador)
**Texto original:** "Achado da Sessão 3 (F-APRESENT P1) · aplicado aqui como
adaptador em app_v2."
**Pergunta:** que achado? · candidato a D-XXX retroativo da Sessão 3 (S-VN ou
F-APRESENT P1 conclusão) · não trimado nesta sessão.

### CO-8 · `app_v2.py:1514` (headers user-facing)
**Texto remanescente:** "Headers user-facing: traduz cada agrupador (ex:
'Centro_Custo' → 'Centro de Custo') antes de construir o DataFrame · headers
e formatos consomem unidade (P-29)."
**Pergunta:** "C-5 (Sessão 4-ter-bis)" referenciava qual decisão? · sobre
humanização de nomes técnicos · candidato a D-XXX OU promoção para capability
F-APRESENT (`rotular_agrupador` já está em `apresentacao/templates/familia_a/_shared.py`).

### CO-9 · Conjunto de comentários "Sessão 8.2 · C-2 (P-31)" em `app_v2.py`
**Linhas:** 341, 399, 407, 435 (4 comentários sobre Salvar/Aplicar modelo).
**Texto remanescente:** "Sessão 8.2 · C-2 (P-31) · botão agora abre painel
inline com..." (variantes).
**Pergunta:** P-31 está em DECISIONS.md? · se sim, comentários OK como case 1.
Se não, candidatos a remoção do prefixo "Sessão 8.2 · C-2" mantendo apenas
"(P-31) · ...". Não trimado nesta sessão (ação Camada 2 quando confirmado P-31).

## Considerações para próxima sessão

- Validar se P-29, P-30, P-31, P-35 estão DECISIONS.md como decisões formais.
  Se sim, todos os comentários "Sessão X · C-N (P-NN)" são case 1 (mantém).
  Se não, podem virar bullets em D-XXX retroativo da sessão.
- Considerar decisão arquitetural: TODO-FAPRESENT-CLEANUP em
  `_renderizar_secao_como_tabela` (CO-5) e `rotular_agrupador` (CO-8) sugerem
  promoção para capability F-APRESENT genérica · destrava 1 etapa de simplificação
  de exportacao_v2.py / app_v2.py.
