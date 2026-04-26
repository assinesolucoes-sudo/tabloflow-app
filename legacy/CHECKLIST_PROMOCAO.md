# Checklist de Promoção · D-202 · Refactor Dirigido

Sessão Claude Code · 2026-04-26 · 8 etapas + entrega.

| # | Etapa | Status | Verificação |
|---|-------|--------|-------------|
| 1 | `ContratoComparativo` em `contratos.py` · `ComparacaoV2` herda | ✅ | `from contratos import ContratoComparativo` OK; suite 731/731 verde após etapa |
| 2 | `tipo_campo` e `unidade` Optional em `ColumnMeta` | ✅ | Campos com default `None` · zero quebra · 731/731 verde |
| 3 | `default_unidade_para_tipo_campo` movido para `apresentacao/formatos.py` | ✅ | `_default_unidade_para_tipo` e `_unidade_default_por_tipo` removidos de `visoes/visao_v2.py` e `app_v2.py` · teste atualizado para importar do novo local · 731/731 verde |
| 4 | Bugs cap 7 (`renderizar_resumo_executivo` dict) + cap 10 (`renderizar_diagnostico` thresholds) corrigidos | ✅ | Cap 7 trata dict como pares legíveis em `_formatar_valor_com_heuristica` · Cap 10 consome `formatar_threshold_por_contrato` · `_THRESHOLDS_CONTRATO` promovido para `apresentacao.formatos.THRESHOLDS_CONTRATO_FUNDACAO` · 731/731 verde |
| 5 | Sub-templates extraídos em `apresentacao/templates/familia_a/` | ✅ | 5 arquivos novos: `leitura_qualitativa.py` · `saude_comparacao.py` · `concentracao.py` · `onde_se_concentra.py` · `variacoes_destaque.py` + `_shared.py` (helpers) · `exportacao_v2.py` reduzido de 2313 → 1352 linhas (−961) |
| 6 | `construir_leitura_qualitativa` parametrizada | ✅ | Parte de etapa 5 · função recebe `unidade · tipo_campo · semantica · ancora · dist_sem · delta_sem · base_analitica · concentracao · onde_se_concentra · origem_ux · comparado_ux` (sem `V2Result`) |
| 7 | Capability 11 `formato_adaptativo_por_unidade` (D-205) | ✅ | Tabela `_REGRAS_FORMATO_ADAPTATIVO` + função pública + 15 testes novos · suite 746/746 verde |
| 8 | Cleanup de comentários "Sessão X · C-N" órfãos | ✅ | 6 comentários trimados (prefixos temporais removidos · conteúdo técnico preservado) · 9 órfãos catalogados em `COMENTARIOS_ORFAOS_V2.md` · 17 mantidos por referenciarem D-XXX ou P-XX · suite 746/746 verde |

## Linhas modificadas

| Arquivo | Antes | Depois | Diff |
|---------|-------|--------|------|
| `src/visoes/exportacao_v2.py`        | 2313 | 1352 | **−961** |
| `src/visoes/visao_v2.py`             | 1827 | 1719 | −108 |
| `src/app_v2.py`                      | 1924 | 1909 | −15 |
| `src/contratos.py`                   |  679 |  819 | +140 |
| `src/apresentacao/formatos.py`       |  371 |  516 | +145 |
| `src/apresentacao/__init__.py`       |  133 |  140 | +7 |
| `src/apresentacao/diagnostico_narrativo.py` | 889 |  893 | +4 |
| `src/apresentacao/resumo_executivo.py` | 597 | 614 | +17 |
| `src/apresentacao/templates/__init__.py` | 0 |  10 | +10 |
| `src/apresentacao/templates/familia_a/__init__.py` | 0 |  26 | +26 |
| `src/apresentacao/templates/familia_a/_shared.py` | 0 | 243 | +243 |
| `src/apresentacao/templates/familia_a/leitura_qualitativa.py` | 0 | 193 | +193 |
| `src/apresentacao/templates/familia_a/saude_comparacao.py` | 0 | 208 | +208 |
| `src/apresentacao/templates/familia_a/concentracao.py` | 0 | 58 | +58 |
| `src/apresentacao/templates/familia_a/onde_se_concentra.py` | 0 | 208 | +208 |
| `src/apresentacao/templates/familia_a/variacoes_destaque.py` | 0 | 249 | +249 |
| `src/testes/test_v2_s8.py`           | 845 | 845 | 0 (apenas import alterado) |
| `src/testes/test_formato_adaptativo.py` (novo) | 0 | 109 | +109 |

## Critério de pronto

- ✅ Suite 731 anterior + 15 testes novos = **746/746 verde**
- ✅ 8 itens binários ✅
- ⚠ Smoke visual `streamlit run`: **não executado** (ambiente sem display interativo nesta sessão · validação Camada 2 humana)
- ✅ Diffs de linhas conferem: `exportacao_v2.py` reduzido em 961 linhas (target era 900-1100); `app_v2.py` reduzido em 15 linhas (target era ~30 · variação por escopo de cleanup conservador)
