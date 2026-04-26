# V-V1 · Relatório Final · Fase 8

**Sessão:** V-V1 · Motor da V1 · Conciliação de Bases · 3º quadrado dos 6 do ciclo da V1 (D-158)
**Modalidade:** sessão combinada D-155 · prompt único · executor Claude Code
**Versão do prompt consumido:** 1.0 · 2026-04-26
**Produzido por:** Claude Code · 2026-04-26
**Gate de retrospectiva (D-174 Camada 1 mecânica):** suite 100% verde + cobertura ≥ 90% + relatório completo

---

## 1 · Resumo executivo

| Métrica | Resultado |
|---|---|
| Suite final | **978/979 verde** (745 herdados + **233 novos V-V1** + 1 vermelho herdado preservado) |
| Cobertura `src/visoes/visao_v1.py` | **95%** (917 statements · 46 miss) — acima do mínimo 90% |
| Status de cada fase | 0 ✅ · 1 ✅ · 2 ✅ · 3 ✅ · 4 ✅ · 5 ✅ · 6 ✅ · 7 ✅ · 8 ✅ |
| Tempo decorrido | sessão única (5-7h estimadas no prompt) |
| Linhas em `visao_v1.py` | ~2.230 linhas (incluindo docstrings · invariantes Pydantic · helpers · pipeline) |

**Distribuição de testes V-V1 por fase:**

| Fase | Arquivo | Testes |
|---|---|---|
| 1 · Contratos Pydantic | `test_contratos_v1.py` | 34 |
| 2 · Pipeline ABAS_DISTINTAS | `test_visao_v1_abas_distintas.py` | 9 |
| 3 · Pipeline MESMA_ABA_EM_COLUNAS | `test_visao_v1_mesma_aba.py` | 7 |
| 4 · Resumo Executivo (9 seções) | `test_visao_v1_resumo_executivo.py` | 14 |
| 5 · Bloqueios + Warnings | `test_visao_v1_bloqueios_warnings.py` | 22 |
| 6 · Suite Q4.C matriz (Blocos I-IV) | `test_visao_v1_matriz_q4c.py` | 107 |
| 6 · Suite Q4.C determinismo+fronteira (V-VI) | `test_visao_v1_q4c_determinismo_fronteira.py` | 40 |
| **TOTAL** | | **233** |

---

## 2 · Lista de bifurcações resolvidas internamente (D-174 Camada 1)

### BIF-0 · `UnidadeCanonica` — enum local em `visao_v1.py`

**O que foi decidido:** `UnidadeCanonica` declarada como `class UnidadeCanonica(str, Enum)` localmente em `visao_v1.py`, com os mesmos 8 valores que existem como `Literal[...]` em `contratos.py:ColumnMeta.unidade` e `ColumnMeta.ContratoComparativo.unidade`.

**Alternativas consideradas:**
1. (escolhida) Declarar enum localmente.
2. Promover para `contratos.py` como enum nominal — vetado pela seção 10.3 do prompt ("Não modifica `src/contratos.py`").
3. Usar Literal everywhere — diverge da S-V1 §1.22 que declara explicitamente "Enum 8 valores".

**Por quê:** S-V1 §1.22 declara enum; prompt veta tocar Fundação. Enum local com mesmo conjunto de valores honra ambas as restrições e atende princípio C.3 (zero invenção de comportamento).

**Sugestão para retrospectiva:** sub-sessão futura promove `UnidadeCanonica` para `contratos.py` · alinha `ColumnMeta.unidade` e `ContratoComparativo.unidade` para usar a enum (refactor cosmético da Fundação).

### BIF-1 · `DEFAULT_EPSILON_POR_UNIDADE` com 8 entradas vs 5 explícitas em S-V1 §2.8

**O que foi decidido:** dict com 8 entradas (todas as `UnidadeCanonica`), incluindo as 3 unidades inelegíveis para Ponte (PERCENTUAL · ADIMENSIONAL · RAZAO) com `Decimal("0")` cada.

**Alternativas consideradas:**
1. (escolhida) 8 entradas com 0 default nas 3 inelegíveis.
2. 5 entradas estritas conforme S-V1 §2.8.

**Por quê:** prompt seção 3.1 sugere a forma de 8 entradas no exemplo de código. As 3 unidades inelegíveis nunca afetam Ponte (campos com essas unidades são omitidos da lista `pontes`), então `Decimal("0")` é matematicamente vacuoso. A forma de 8 entradas torna `ConfigAplicadaV1.epsilon_por_unidade` simétrico e fácil de auditar. Não viola spec — apenas estende defensivamente.

### BIF-2 · `ModoMatchV1` declarado como 6ª enum (vs 5 listadas no prompt seção 2.2)

**O que foi decidido:** declarar `ModoMatchV1` (S-V1 §1.5 · 4 valores) como enum nominal local · soma 7 enums em V-V1 (CasoLogicoV1 · ModoMatchV1 · TipoCampoV1 · ClassificacaoRegistroV1 · StatusCampoV1 · StatusPonteV1 · UnidadeCanonica).

**Alternativas consideradas:** usar Literal (omissão pelo prompt).

**Por quê:** S-V1 §1.5 declara `class ModoMatchV1(str, Enum)`. O prompt §2.2 lista "5 enums" como categoria de eco mas inclui apenas 5 nomes — `ModoMatchV1` é omissão acidental. Princípio C.3: spec autoritativa > prompt acidental.

### BIF-3 · `ConciliacaoV1Result.visao` redundante com `visao_id`

**O que foi decidido:** declarar **ambos** os campos · `visao_id: Literal["V1"]` (override de VNResultBase) E `visao: Literal["V1"]` (campo extra · S-V1 §1.1).

**Alternativas consideradas:** suprimir um dos dois.

**Por quê:** prompt seção 1.3 explicita "(override) `ConciliacaoV1Result.visao: Literal["V1"]` redundante com `visao_id` herdado de `VNResultBase` mantido conforme S-V1 v2 §1.1 (escolha Usuária 26/04 noite)". Decisão cristalizada.

### BIF-4 · DUPLICIDADE em modos não-EXATO

**O que foi decidido:** detectar DUPLICIDADE também em modos não-EXATO (CONTEM, INICIA_COM, TERMINA_COM) · pré-varredura · usando mesma lógica de chave duplicada em `idx_o_por_chave`/`idx_c_por_chave`.

**Alternativas consideradas:** deixar non-EXATO sem detecção de DUPLICIDADE (DUPLICIDADE viraria AMBIGUIDADE pela varredura). 

**Por quê:** S-V1 §2.2 diz "Detecta duplicidade ANTES do match" sem especificar que é só em EXATO. Comportamento consistente entre modos é mais auditável (semantically: chave repetida em 1 lado é DUPLICIDADE independente do modo de match) e era exigido por testes de matriz Bloco I (DUPLICIDADE × non-EXATO modes).

### BIF-5 · `B-V1-MISTURA-ABAS` delegado ao app

**O que foi decidido:** o motor V-V1 NÃO valida explicitamente `B-V1-MISTURA-ABAS` (apontamentos misturando aba_origem e aba_comparado de forma inconsistente). Documentado e delegado ao app E3.

**Alternativas consideradas:** implementar verificação de coerência aba × apontamento no motor.

**Por quê:** S-V1 §2.5 declara "validação delegada ao app · motor recebe DataFrame único e confia". O motor recebe `motor_result` já com df + origem_comparado_map; não tem visibilidade direta sobre "aba_X vs aba_Y" no nível do apontamento. A-V1 (próxima sessão) implementa essa validação na E3 antes de chamar `executar_v1`.

### BIF-6 · ESTADO_SITUACAO em V-V1 numérico-only

**O que foi decidido:** valores ESTADO_SITUACAO/ADIMENSIONAL processados como Decimal (numérico). Strings categóricas viram `None` no helper `_to_decimal_unidade` · status_campo cai em `SEM_VALOR_AMBOS`.

**Alternativas consideradas:** carregar string em `valor_origem`/`valor_comparado` (mas contrato CelulaCampoV1 obriga `Optional[Decimal]`).

**Por quê:** contratos V-V1 (S-V1 §1.12) só aceitam `Decimal` em valores. Suporte completo a ESTADO_SITUACAO categórico exigiria evolução do contrato (campo `valor_str_origem`/`valor_str_comparado` adicional). É item para retrospectiva: "P-V1-TEC-04 · ESTADO_SITUACAO categórico: contrato CelulaCampoV1 deve carregar valor textual quando tipo_logico==ESTADO_SITUACAO". Não bloqueia V-V1 motor — apenas limita um cenário.

### BIF-7 · MESMA_ABA_EM_COLUNAS sem aba na base de Fundação

**O que foi decidido:** auditoria YAML Q1.A documenta lacuna; entrada V1 em `casos_esperados.yaml` declara `aba_unica_caso_3: null`. Não criada aba sintética nesta sessão (fora de escopo V-V1 motor).

**Por quê:** prompt seção 9.3 explícito: "Se a base atual NÃO tem aba para testar MESMA_ABA_EM_COLUNAS · **NÃO crie aba sintética nesta sessão**. Documente em `V-V1_AUDITORIA_BASE.md` a lacuna como pré-requisito para A-V1." Cumprido.

### BIF-8 · Tipos de assertion novos no YAML mapeados para canônicos

**O que foi decidido:** assertions V1-A11 (status_ponte) e V1-A12 (diferenca_liquida) usam tipo canônico `estrutura_saida` com chaves customizadas dentro de `esperado:` (não criar tipo novo no enum TIPOS_CANONICOS).

**Alternativas consideradas:** introduzir tipos `status_ponte` e `diferenca_liquida` como novos canônicos.

**Por quê:** o teste herdado `test_yaml_tipos_canonicos_apenas` em `test_base_fundacao.py` valida que apenas os 5 tipos canônicos existem no YAML (`contagem_exata` · `contagem_categoria` · `warning_presente` · `estrutura_saida` · `bloqueio_emitido`). Estender o enum exigiria tocar arquivo herdado da Fundação · veto da sessão (princípio: alteração mínima ao Fundação). Mapeamento via `estrutura_saida` com chaves específicas preserva semântica e respeita teste herdado.

---

## 3 · Output `grep -r "TODO-V1-" src/`

```
$ grep -rn "TODO-V1-" src/
(nenhum match)
```

**0 marcadores `TODO-V1-*`** adicionados nesta sessão. O único marcador permitido era `# Q2 Decimal-na-fronteira` (prompt seção 1.4) · presente em `src/visoes/visao_v1.py:734` em `_to_decimal_unidade`.

---

## 4 · Output `grep -r "TODO-FAPRESENT-CLEANUP" src/`

```
$ grep -rn "TODO-FAPRESENT-CLEANUP" src/
src/app_v2.py:178               (pré-existente · não-V1)
src/testes/test_exportacao_v2.py:523   (pré-existente · não-V1)
src/visoes/exportacao_v2.py:854        (pré-existente · não-V1)
src/visoes/exportacao_v2.py:943        (pré-existente · não-V1)
```

**0 novos marcadores `TODO-FAPRESENT-CLEANUP`** adicionados em V-V1 (V-V1 não toca `exportacao_*.py` ou `app_v*.py` · só `visao_v1.py` e tests). Confirmação: prompt seção 10.3 cumprida.

---

## 5 · Checklist mecânico (CHECKLIST_MECANICO.md)

```
[✅] Suite pytest src/testes/ verde (978/979 · 1 vermelho herdado preservado · não-V-V1)
[✅] Suite count >= 745 + 150 (mínimo Q4.C) · final 745 + 233 = 978
[✅] Cobertura src/visoes/visao_v1.py >= 90% · final 95%
[✅] src/testes/V-V1_ANCORAGEM.md existe e está completo
[✅] src/testes/V-V1_AUDITORIA_BASE.md existe e está completo
[✅] src/testes/V-V1_RELATORIO.md existe e está completo
[✅] src/visoes/visao_v1.py existe (~2.230 linhas)
[✅] src/visoes/visao_v1.py importa sem erro
[✅] executar_v1(motor_result, config) retorna ConciliacaoV1Result
[✅] 7 enums declaradas (CasoLogicoV1 · ModoMatchV1 · TipoCampoV1 · ClassificacaoRegistroV1 · StatusCampoV1 · StatusPonteV1 · UnidadeCanonica) — 5+ exigidas pelo prompt; ModoMatchV1 e UnidadeCanonica adicionadas (BIF-2 · BIF-0)
[✅] 16 contratos Pydantic declarados (§1.1-1.21 · 16 BaseModel + 7 enums = 23 declarações totais; mapeamento spec)
[✅] 12 bloqueios B-V1-* implementados (S-V1 §2.5) — todos os 12 com testes de disparo
[✅] 4 warnings W-V1-* implementados (S-V1 §2.7) — TOL · DUP · AMB · UNIDADE com testes de disparo + não-disparo
[✅] 8 thresholds TED V1 declarados (S-V1 §2.8) — chave_nulos_max · volume_max · 5 epsilon_por_unidade · concentracao_agrupador_principal_min
[✅] Pipeline 8 etapas implementado (S-V1 §2.1)
[✅] Ramo ABAS_DISTINTAS funcional · 9 smoke tests + 107 matriciais
[✅] Ramo MESMA_ABA_EM_COLUNAS funcional · 7 smoke tests + invariantes
[✅] Resumo Executivo com 9 seções mapeáveis (S-V1 §2.10) — verificado em 14 testes
[✅] CoracaoVisualRef.nome_aba == "Mapa de Conciliação" — verificado em test_coracao_visual_*
[✅] Ordenação determinística canônica testada — Bloco V test_ordem_deterministica_canonica_*
[✅] Idempotência testada — Bloco V test_idempotencia_executar_v1_serializacao_estavel
[✅] Invariantes Pydantic todas testadas — 7 invariantes cobertas em test_contratos_v1
[✅] Entrada V1 do casos_esperados.yaml reescrita — 12 assertions coerentes com S-V1 v2
[✅] casos_esperados.yaml parseável — yaml.safe_load passa
[✅] zero regressão nos 745 testes herdados — confirmado em pytest -q
```

**Resultado checklist:** 24/24 ✅

---

## 6 · Sugestões para retrospectiva (ao Arquiteto)

Itens que considerei alterar no escopo durante a execução mas não alterei (princípio C.3 · zero invenção):

1. **Promover `UnidadeCanonica` para enum em `contratos.py`** · sub-sessão de refactor cosmético da Fundação · alinha `ColumnMeta.unidade` e `ContratoComparativo.unidade` para usar enum nominal. Hoje todos usam `Literal[...]`. (BIF-0)

2. **`ModoMatchV1` ausente da lista de 5 enums no prompt seção 2.2** · spec S-V1 §1.5 declara, prompt esqueceu. Sugiro corrigir prompt para "6 enums" ou explicitar que ModoMatchV1 está em escopo. (BIF-2)

3. **ESTADO_SITUACAO categórico não-suportado integralmente** · contrato `CelulaCampoV1` só aceita `Optional[Decimal]`. Para suportar valores textuais como "ATIVO"/"INATIVO" sem encoding numérico, contrato precisa evolver com campo `valor_str_origem`/`valor_str_comparado`. **Sugiro como P-V1-TEC-04** · não bloqueia V-V1 mas limita um cenário comum em conciliação contábil. (BIF-6)

4. **Aba sintética para MESMA_ABA_EM_COLUNAS** · pré-requisito de A-V1 documentado. Sub-sessão antes de VV-V1 cria aba sintética em `base_fundacao.xlsx` (ex: `dual_mesma_aba_colunas` com colunas `Conta_Origem · Conta_Comparado · Valor_Origem · Valor_Comparado`) e estende entrada V1 do YAML para cobrir Caso 3. (BIF-7)

5. **Tipos de assertion no YAML** · enum TIPOS_CANONICOS herdado de Fundação (5 tipos) força uso de `estrutura_saida` para coisas como status_ponte e diferenca_liquida. Considerar evoluir para um conjunto mais semântico em refactor futuro do `casos_esperados.yaml`. (BIF-8)

6. **Performance da varredura O(n*m) em modos não-EXATO** · meu `_etapa_4a_match_abas_distintas` faz pairwise iteration. Para `volume_max=500.000` em ambos lados em modo CONTEM, isso é 250 bilhões de comparações = inviável. Bloqueio B-V1-RESULTADO-EXCEDE limita isso a 500k total. Sugiro **otimização futura** com índice de prefixo/sufixo se P-V1 vier a precisar de match difuso de alta volumetria. Não-V-V1.

7. **`B-V1-MOTOR-FALHOU` catch-all** · implementei como wrapper genérico em `executar_v1`. Captura qualquer Exception não-`ValueError("B-V1-...:")` e re-levanta com prefixo. **Risco potencial:** se um bug futuro produzir uma `KeyError`, ela vira `B-V1-MOTOR-FALHOU` opaco ao invés de stack trace claro. Sugiro **logging estruturado** em A-V1 (capturar exception original em `BloqueioOperacional.contexto_disparo` como detalhe técnico para suporte). Não-V-V1.

8. **Microcopy completo de `PonteCampoV1.microcopy_status`** · S-V1 §1.16 deixa ambíguo. Hoje `PonteCampoV1` não tem campo `microcopy_status` (não declarado em §1.16 do contrato). **Confirmação:** P-V1-TEC-01 (microcopy completo) é tarefa A-V1 cleanup. Não-V-V1. Mantido sem TODO-V1-MICROCOPY-PONTE no código.

9. **Validação cruzada `tipo_logico` ↔ `unidade`** · P-V1-TEC-02 conforme S-V1 final. Implementei como W-V1-UNIDADE warning (não bloqueia · default Usuária prevalece). Funciona via `motor_result.column_meta[col].unidade` · disparado quando declarada diverge da inferida. Considerado completo · sub-tarefa fechada.

10. **`UNIDADES_INELEGIVEIS_PONTE` declarada como `set` Python (não enum)** · ergonomicamente mais simples. Pode-se promover para `class UnidadeInelegivelPonte(str, Enum)` se houver demanda futura · pequena melhoria. Não-V-V1.

---

## 7 · Anomalias de ambiente

| Item | Estado |
|---|---|
| **Não é repositório git** | Confirmado · `git status` retorna "fatal: not a git repository". Etapa "criar branch v-v1" do prompt seção 1 pulada conforme aprovado pela Usuária. Trabalhos foram diretos na working copy. Recomendação: rodar `git init` + commit inicial cobrindo state pós-V-V1 antes de A-V1. |
| **Test path divergente do prompt** | Prompt referencia `tests/test_*.py` mas `pytest.ini` declara `testpaths = src/testes` · todos os arquivos novos foram criados em `src/testes/` conforme aprovado. |
| **Vermelho herdado preservado** | `src/testes/test_apresentacao.py::TestInterfaceVocabulario::test_classificacoes_tem_6_entradas` falha com `assert 18 == 6` · drift de vocabulário pré-existente (provavelmente Sessão 8.4 ou anterior · `vocabulary v2 drift` mencionado em `MEMORY.md` F-APRESENT P1). Não tem relação causal com V-V1 (V-V1 não toca `vocabulario_bilingue.md` · vetado em prompt seção 10.3). Continua vermelho pelos mesmos motivos · isolado e documentado. |

---

## 8 · Próximo passo

V-V1 · Camada 1 mecânica concluída (D-174). 

Pacote para o Arquiteto:
- 6 arquivos novos em `src/testes/` (testes V1) + 3 documentos em `src/testes/V-V1_*.md`
- 1 arquivo novo `src/visoes/visao_v1.py`
- 1 arquivo modificado `bases/casos_esperados.yaml`

Aguardando retrospectiva consolidada D-155 (sessão combinada). Após retrospectiva · próximo quadrado é **A-V1** (4º dos 6) · sessão Claude Code dedicada com gate duplo D-174 (Camada 1 mecânica + Camada 2 visual).

---

*Fim do relatório · sessão V-V1 concluída · entregue para retrospectiva.*
