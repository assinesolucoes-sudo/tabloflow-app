# V-V1 · Checklist Mecânico (D-174 Camada 1)

**Sessão:** V-V1 · Motor da V1 · Conciliação de Bases
**Data:** 2026-04-26
**Total checks:** 24/24 ✅

---

## Suite e cobertura

- [✅] Suite pytest `src/testes/` 100% verde sobre os novos · final **978/979** (745 herdados + 233 V1 + 1 vermelho herdado pré-existente preservado)
- [✅] Suite count >= 745 + 150 (mínimo Q4.C declarado no prompt) · final 745 + **233**
- [✅] Cobertura `src/visoes/visao_v1.py` >= 90% · final **95%** (917 stmts · 46 miss)

## Documentos

- [✅] `src/testes/V-V1_ANCORAGEM.md` existe e está completo · eco S-V1 v2 (13 contratos · 5 enums · 12 bloqueios · 4 warnings · 8 thresholds · pipeline 8 etapas · 4 casos D-213)
- [✅] `src/testes/V-V1_AUDITORIA_BASE.md` existe e está completo · 6 seções (discrepâncias YAML · inspeção estrutural · execução empírica · entrada reescrita · resumo · lacunas)
- [✅] `src/testes/V-V1_RELATORIO.md` existe e está completo · 8 seções (resumo · 9 bifurcações · TODO grep · checklist · sugestões · anomalias · próximo passo)
- [✅] `src/testes/CHECKLIST_MECANICO.md` existe (este arquivo)

## Implementação

- [✅] `src/visoes/visao_v1.py` existe (~2.230 linhas)
- [✅] `src/visoes/visao_v1.py` importa sem erro
- [✅] `executar_v1(motor_result, config)` retorna `ConciliacaoV1Result`
- [✅] 7 enums declaradas (5 exigidas + 2 adicionadas por bifurcação): `CasoLogicoV1` · `ModoMatchV1` · `TipoCampoV1` · `ClassificacaoRegistroV1` · `StatusCampoV1` · `StatusPonteV1` · `UnidadeCanonica`
- [✅] 16 contratos Pydantic declarados (S-V1 §1.1, §1.2, §1.4, §1.6, §1.11-1.21 + ParCasado interno)
- [✅] 12 bloqueios B-V1-* implementados e testados (S-V1 §2.5)
- [✅] 4 warnings W-V1-* implementados e testados (S-V1 §2.7)
- [✅] 8 thresholds TED V1 declarados (S-V1 §2.8)

## Pipeline

- [✅] Pipeline 8 etapas implementado (S-V1 §2.1)
- [✅] Ramo ABAS_DISTINTAS funcional (helper `_etapa_4a_match_abas_distintas` · 4 modos de match)
- [✅] Ramo MESMA_ABA_EM_COLUNAS funcional (helper `_etapa_4b_pareamento_linha_a_linha` · invariantes)

## Saída

- [✅] Resumo Executivo com 9 seções mapeáveis (S-V1 §2.10) · 14 testes verificam estrutura
- [✅] `CoracaoVisualRef.nome_aba == "Mapa de Conciliação"` (verificado em test_coracao_visual)

## Determinismo e invariantes

- [✅] Ordenação determinística canônica testada (Q3 · `(ORDEM_CLASSIFICACAO[c], chave_consolidada)` ASCII-strict)
- [✅] Idempotência testada (2 execuções produzem mesma saída · contagens · ordem)
- [✅] Invariantes Pydantic todas testadas (7 invariantes em ConciliacaoV1Result + ConciliacaoRealizadaV1)

## YAML auditoria

- [✅] Entrada V1 do `bases/casos_esperados.yaml` reescrita · 12 assertions coerentes com S-V1 v2
- [✅] `casos_esperados.yaml` parseável (`yaml.safe_load` retorna dict válido com `V1` populado)

## Não-regressão

- [✅] Zero regressão nos 745 testes herdados (suite herdada continua 745 verdes; o 1 vermelho herdado pré-existente · não-V1 · permanece pelos mesmos motivos)

---

## Resumo

✅ **24/24 checkpoints completados.**

V-V1 Camada 1 mecânica (D-174) concluída. Pacote pronto para retrospectiva combinada D-155 com o Arquiteto. Próximo quadrado: A-V1 (4º dos 6 do ciclo V1).
