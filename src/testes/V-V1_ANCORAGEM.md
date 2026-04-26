# V-V1 · Ancoragem Obrigatória · Fase 0

**Sessão:** V-V1 · Motor da V1 · Conciliação de Bases · 3º quadrado dos 6 (D-158)
**Produzido por:** Claude Code · executor · 2026-04-26
**Fonte canônica deste eco:** S-V1 v2.0 (`/specs/spec_v1.md`) · 1.466 linhas · pacote único · Caminho A
**Suite de partida real:** 745/746 verde · 1 vermelho pré-existente identificado e isolado de V-V1 (vocabulário · drift residual)
**Ambiente:** working copy não-versionada (não-git · documentado em V-V1_RELATORIO.md)

> Este documento é o eco em prosa parafraseada (não copy-paste) dos contratos · enums · bloqueios · warnings · thresholds e pipeline da S-V1 v2 · conforme requerido pela Fase 0 do prompt V-V1. Não introduz invenção sobre a spec; apenas declara o entendimento do executor para auditoria do Arquiteto.

---

## 2.1 · Eco dos 13 contratos críticos

### `ConciliacaoV1Result` (S-V1 §1.1)

Contrato principal de saída do motor V1 · estende `VNResultBase` da Fundação · única classe que `visao_v1.py` produz e que `app_v1.py` + `exportacao_v1.py` consumirão. Carrega 4 dimensões analíticas: a taxa (via `contagem_por_classificacao`), a granularidade registro-a-registro (via `classificacao_por_registro` ordenada · 1 entrada por registro), o achatado por campo (via `valor_por_campo`), e a Ponte (via `pontes` + `status_ponte_geral`). Faz 7 invariantes Pydantic: somas batem, listas batem, em MESMA_ABA_EM_COLUNAS as 4 classes inaplicáveis ficam zeradas e cobertura é `None`. Não infere caso lógico (recebe inferido de fora) · não consolida silenciosamente (preserva e classifica · C.5) · não inclui DataFrame bruto (apenas `base_analitica` herdada de `VNResultBase`).

### `ConciliacaoRealizadaV1` (S-V1 §1.2)

Sub-contrato declarativo do que foi efetivamente executado. Captura a ortogonalidade D-213: **físico** (`n_arquivos ∈ {1, 2}`) × **lógico** (`caso_logico_inferido ∈ {ABAS_DISTINTAS, MESMA_ABA_EM_COLUNAS}`) → 4 casos válidos. Carrega rótulos UX da Origem/Comparado, lista de até 5 agrupadores de match, lista de até 10 campos comparados, lista de 0-5 agrupadores executivos, e as 3 contagens estruturais (`n_registros_origem`, `n_registros_comparado`, `n_processados`). Não declara modo de match no nível do contrato (cada agrupador carrega o seu) · não faz validação cross-aba (delegado ao motor na Etapa 2).

### `RegistroConciliadoV1` (S-V1 §1.11)

Uma linha do "Mapa de Conciliação" (Aba 3 do Excel) e raiz da Aba 4 (Análise Analítica). Une chave consolidada (string concatenada com `|` · zeros à esquerda preservados) · valores dos agrupadores (dict `rotulo_analitico → valor str`) · classificação estrutural (1 das 6 ou das 2 conforme caso lógico) · lista de células (1 por campo) · 3 totais agregados (`diferenca_total_registro`, `sigma_diferenca_total_registro`, `variacao_total_registro_pct`) que ficam `None` em registros que não têm par 1-para-1 (SO_ORIGEM · SO_COMPARADO · DIVERGENCIA_DUPLICIDADE · DIVERGENCIA_AMBIGUIDADE) ou em divisão por zero. Não calcula nada por si só · é um contêiner de dados pós-processados.

### `CelulaCampoV1` (S-V1 §1.12)

Uma célula do Mapa = 1 par (Origem, Comparado) para 1 campo em 1 registro. Carrega `campo_indice` (int posicional na lista de campos do contrato) · valores (`Decimal` · ambos opcionais) · diferença (também opcional) · status do campo (1 das 6 enums `StatusCampoV1`). Não codifica unidade na célula (vem do `CampoComparadoV1` referenciado por índice).

### `CoberturaV1` (S-V1 §1.13)

Métrica simétrica de match entre as duas bases · usada na §6 do Resumo Executivo. 6 campos: `n_origem_com_par`, `n_origem_sem_par`, `cobertura_origem_pct`, mais a tripla simétrica do lado Comparado. Em ABAS_DISTINTAS é populado · em MESMA_ABA_EM_COLUNAS o contrato é `Optional[CoberturaV1] = None` (cobertura é trivialmente 100% por construção · informação ausente vira `None` · não Decimal('1')). Não codifica taxa global · isso é derivado em outra seção.

### `ValorPorCampoV1` (S-V1 §1.14)

Achatado por campo · 1 entrada por `CampoComparadoV1` · alimenta a §5 do Resumo e a Aba 2 (Análise Analítica). Soma valores de cada lado · diferença líquida · sigma da diferença (apenas em registros conciliados ou divergentes-valor · NÃO em SO_*/duplicidade/ambiguidade) · contadores de tolerância absorvida. A unidade é declarada no contrato · não inferida.

### `LinhaResumoAgrupadorV1` + `MetricaCampoAgrupadorV1` (S-V1 §1.15)

Composto que monta a Aba 2 (Resumo por Agrupador Executivo) e a §7 do Resumo. `LinhaResumoAgrupadorV1` agrupa por valores únicos do(s) agrupador(es) executivo(s); por linha, exibe contadores (`n_conciliados`, `n_divergentes_valor`, `n_so_origem`, `n_so_comparado` · os 2 últimos zerados em MESMA_ABA_EM_COLUNAS por construção) e uma lista de `MetricaCampoAgrupadorV1` (1 por campo comparado) com somas por lado, diferença líquida e sigma. Ordenação T-RANK declarada por `|diferenca_liquida_total|` desc · empate alfabético (P-V1-TEC-03).

### `PonteCampoV1` (S-V1 §1.16)

Sub-Ponte por campo · 1 entrada por campo elegível (Q1.B-D-210: campos PERCENTUAL/ADIMENSIONAL/RAZAO **omitidos** da lista). Calcula `saldo_origem` · 4 ajustes (`so_origem`, `so_comparado`, `divergentes_valor`, `tolerancia_absorvida`) · `saldo_comparado_esperado` · `saldo_comparado_real` · `residuo` · flag `fecha` (compara `|residuo|` com `epsilon_por_unidade[unidade]`). Em MESMA_ABA_EM_COLUNAS, `ajuste_so_origem` e `ajuste_so_comparado` são `Decimal('0')` por construção (não há registros desse tipo). Status binário consolidado vem em `StatusPonteV1`.

### `SinteseDiagnosticoV1` (S-V1 §1.17)

Bloco de 7 contadores que alimenta a §8 do Resumo Executivo: tolerância absorvida (n + valor) · duplicidade (n_chaves + n_registros_afetados · ambos zerados em MESMA_ABA_EM_COLUNAS) · ambiguidade (idem) · n_warnings_ativos. Não decide gravidade · só conta.

### `ConfigAplicadaV1` (S-V1 §1.18)

Reflexo declarativo da configuração efetivamente usada · 12 campos achatados (CONTEXT §15.12) · consumido por F-APRESENT capability 10. Inclui `caso_logico_inferido` (para microcopy "Caso lógico:..."), `paleta_aplicada` (default 'Azul executivo' · escolhida no rodapé do RESULTADO · D-212), `epsilon_por_unidade` (TED Q2.C · só unidades em uso). `defaults_sobrescritos` registra TEDs editados pela Usuária (auditabilidade C.2).

### `LeituraQualitativaV1` (S-V1 §1.19)

Texto-livre parametrizado · 3 a 6 frases · gerado por `construir_leitura_qualitativa_v1` (templates/familia_a/leitura_qualitativa_v1.py). Carrega `texto`, `faixa_taxa` (3 valores), `modificadores_aplicados` (lista de strings · TEDs ativados, etc), `agrupador_principal_citado` (opcional · só se a concentração ultrapassa o TED `concentracao_agrupador_principal_min`). Zero invenção · prosa fixa preenchida com placeholders.

### `WarningV1` (S-V1 §1.20)

Estrutura uniforme dos 4 warnings W-V1-* (e dos warnings herdados do motor). Carrega código, severidade (5 níveis · `INFORMATIVO`/`AJUSTE_LEVE`/`ALERTA_ESTRUTURAL`/`DECISAO_USUARIO`/`ESCAPE`), `n_ocorrencias` (zero é informação válida · §2.7 padrão de exibição) · lista de `detalhes` (dict opcional). Disjunto de `WarningEstrutural` da Fundação · V1 introduz seu próprio contrato com semântica de contagem.

### `ModeloAplicadoV1` (S-V1 §1.21)

3 campos · referência a um modelo T-MODELO previamente salvo: nome, data de criação, versão do contrato. Não faz aplicação por si só (delegado a `aplicar_modelo` em `t_modelo.py` · padrão V2 herdado).

---

## 2.2 · Eco das 5 enums V1-específicas

### `CasoLogicoV1` (§1.3 · 2 valores)

`ABAS_DISTINTAS` (Origem em uma aba · Comparado em outra · match precisa ser executado) · `MESMA_ABA_EM_COLUNAS` (cada linha já é par casado por construção · não há match a executar). Inferido pelo motor na Etapa 3 · não declarado pela Usuária. Cobertura D-213 dos 4 casos físicos é via combinação ortogonal com `n_arquivos ∈ {1, 2}`.

### `TipoCampoV1` (§1.7 · 7 valores)

`VALOR_MONETARIO` · `QUANTIDADE` · `VOLUME` · `PERCENTUAL` · `PRAZO` · `INDICE` · `ESTADO_SITUACAO`. Taxonomia DCV §4.3 · cada tipo tem unidade default mapeada (Bloco 10.1 · ver §1.7 da spec).

### `ClassificacaoRegistroV1` (§1.8 · 6 valores)

`CONCILIADO` · `DIVERGENTE_VALOR` · `SO_ORIGEM` · `SO_COMPARADO` · `DIVERGENCIA_DUPLICIDADE` · `DIVERGENCIA_AMBIGUIDADE`. Em ABAS_DISTINTAS · todas as 6 são possíveis. Em MESMA_ABA_EM_COLUNAS · só CONCILIADO e DIVERGENTE_VALOR são alcançáveis · as 4 outras ficam contagem 0 preservada (auditabilidade C.2 · ausência é informação · padrão Família A).

### `StatusCampoV1` (§1.9 · 6 valores)

`IGUAL` · `DENTRO_TOLERANCIA` · `DIVERGENTE` · `SEM_VALOR_ORIGEM` · `SEM_VALOR_COMPARADO` · `SEM_VALOR_AMBOS`. Aplicável aos 2 casos lógicos no nível da célula (não da linha). Tabela determinística de derivação em §2.4 (independente do caso lógico).

### `StatusPonteV1` (§1.10 · 2 valores)

`FECHA` (todas as pontes elegíveis fecham dentro do épsilon · também por convenção quando `len(pontes) == 0`) · `COM_RESIDUO` (≥ 1 ponte não-fecha). Cálculo agregado conforme §2.6 da spec.

---

## 2.3 · Eco dos 12 bloqueios B-V1-*

Lista canônica · S-V1 §2.5 · pós-D-213. Cada linha = condição → escapável · microcopy resumido.

| Código | Condição (resumida) | Escapável | Microcopy resumido |
|---|---|---|---|
| `B-V1-NO-UPLOAD` | E1 sem arquivo carregado | Não | "Faça upload das bases para começar" |
| `B-V1-AGRUPADOR-ZERO` | `len(agrupadores_match)==0` na E3 | Não | "Configure ao menos 1 agrupador de match" |
| `B-V1-AGRUPADOR-EXCEDE` | tentativa de adicionar 6º agrupador | Não · L-V1-D | "Limite de 5 agrupadores de match no MVP" |
| `B-V1-CAMPO-ZERO` | `len(campos_comparados)==0` na E3.2 | Não | "Configure ao menos 1 campo comparado" |
| `B-V1-CAMPO-EXCEDE` | tentativa de adicionar 11º campo | Não · P-V1-10-Evo | "Limite de 10 campos comparados no MVP" |
| `B-V1-MESMA-COLUNA` | apontamento `nome_origem == nome_comparado` na mesma aba | Não · estrutural | "A coluna de Origem e Comparado é a mesma · escolha colunas distintas" |
| `B-V1-MISTURA-ABAS` | apontamentos misturam abas inconsistentemente | Não · estrutural | "Apontamentos precisam ser todos da mesma aba ou todos de abas distintas" |
| `B-V1-CHAVE-INVALIDA` | coluna-agrupador tem ≥ TED `chave_nulos_max` (50%) de nulos | Sim | "A coluna {nome} tem {N}% vazios · escolha outra" |
| `B-V1-MOTOR-INFERIU-INCOMPATIVEL` | tipo declarado pela Usuária ≠ tipo inferido pelo motor | Sim · default Usuária prevalece | "Inferido {tipo_inferido}, declarado {tipo_escolhido} · revise" |
| `B-V1-RESULTADO-EXCEDE` | `n_processados > 500.000` (TED `volume_max`) | Sim · ECP P4 | "{N} registros excede 500.000 · simplifique chave ou filtre" |
| `B-V1-DIV-ZERO` | `Σ valor_origem == 0` em variação pct | — não bloqueia · campo recebe `None` | (não exibe · célula vazia) |
| `B-V1-MOTOR-FALHOU` | exception não-tratada no pipeline · catch-all | Não · contato suporte | "Erro inesperado · {detalhe} · contate suporte" |

---

## 2.4 · Eco dos 4 warnings W-V1-*

Lista canônica · S-V1 §2.7. Padrão de exibição: warning com 0 ocorrências exibe "0 ocorrências · nenhuma a reportar" (auditabilidade C.2). Em MESMA_ABA_EM_COLUNAS, W-V1-DUP e W-V1-AMB sempre aparecem com 0 + microcopy "não aplicável neste caso lógico (mesma aba em colunas)".

| Código | Severidade | Quando dispara |
|---|---|---|
| `W-V1-TOL` | INFORMATIVO | ≥ 1 registro CONCILIADO com `diferenca ≠ 0` (qualquer caso lógico) |
| `W-V1-DUP` | ALERTA_ESTRUTURAL | ≥ 1 chave duplicada (só em ABAS_DISTINTAS · sempre 0 em MESMA_ABA_EM_COLUNAS) |
| `W-V1-AMB` | ALERTA_ESTRUTURAL | ≥ 1 chave com múltiplos candidatos (só em ABAS_DISTINTAS · idem) |
| `W-V1-UNIDADE` | AJUSTE_LEVE | tipo_logico ↔ unidade declarado divergente da inferência |

---

## 2.5 · Eco dos 8 thresholds TED V1

Lista canônica · S-V1 §2.8 · localização na UI: expander "⚙️ Configurações avançadas" no topo (D-178 revoga D-153). `epsilon_por_unidade` é dict com **só as unidades efetivamente em uso** após Etapa 3.2 (Q2.C · D-211).

| Código técnico | Default | Tipo |
|---|---|---|
| `chave_nulos_max` | `Decimal("0.50")` (50%) | Decimal (proporção) |
| `volume_max` | `500_000` | int |
| `epsilon_por_unidade.MONETARIO_BRL` | `Decimal("0.01")` | Decimal |
| `epsilon_por_unidade.QUANTIDADE` | `Decimal("0")` | Decimal |
| `epsilon_por_unidade.TEMPO_DIAS` | `Decimal("0")` | Decimal |
| `epsilon_por_unidade.TEMPO_HORAS` | `Decimal("0.01")` | Decimal |
| `epsilon_por_unidade.MULTIPLICADOR` | `Decimal("0.0001")` | Decimal |
| `concentracao_agrupador_principal_min` | `Decimal("0.70")` | Decimal (proporção) |

Unidades não-listadas (PERCENTUAL · ADIMENSIONAL · RAZAO) não têm épsilon de Ponte por construção (Q1.B · D-210: campos com essas unidades são omitidos de `pontes`).

---

## 2.6 · Eco do pipeline 8 etapas + ramificação

Pipeline canônico V1 · S-V1 §2.1 · determinístico (C.1). Diagrama textual:

```
[1] Leitura
     ↓
[2] Validação dos apontamentos da E3
     ↓
[3] Inferir caso lógico  (algoritmo §1.3)
     ↓
     ├── caso == ABAS_DISTINTAS ──→ [4-A] Match (chave consolidada · merge_exato OU varredura · detecção dup/amb)
     │                                       ↓
     └── caso == MESMA_ABA_EM_COLUNAS ──→ [4-B] Pareamento linha-a-linha (1 par por linha · sempre MATCHED)
                                                ↓
[5] Cálculo de diferença + status_campo por célula (tabela §2.4 · independente de caso)
     ↓
[6] Classificação agregada do registro
     · ABAS_DISTINTAS: 6 classes (§2.3)
     · MESMA_ABA_EM_COLUNAS: 2 classes (CONCILIADO ou DIVERGENTE_VALOR)
     ↓
[7] Agregações
     · Cobertura: populada em ABAS_DISTINTAS · None em MESMA_ABA_EM_COLUNAS
     · ValorPorCampo: idêntico nos 2 casos
     · Resumo por agrupador executivo: idêntico (None se não configurado)
     · Pontes: idêntico · em MESMA_ABA_EM_COLUNAS ajuste_so_*=Decimal('0')
     · StatusPonteV1 geral · idêntico (FECHA por convenção se len(pontes)==0)
     · SinteseDiagnostico · 4 contadores · em MESMA_ABA_EM_COLUNAS dup/amb=0
     · LeituraQualitativa · template adaptado por caso (frase inicial diferente)
     ↓
[8] Montagem do contrato ConciliacaoV1Result + aplicação de invariantes §1.1 + retorno (sem mutação)
```

**Determinismo:** ordenação canônica de `classificacao_por_registro` por `(ORDEM_CLASSIFICACAO[c], chave_consolidada)` ASCII-strict (Q3) · empate alfabético em `LinhaResumoAgrupadorV1`. Idempotência: 2 execuções da mesma config produzem `model_dump_json()` idêntico (testado na Fase 6).

---

## 2.7 · Eco do mapeamento 4 casos D-213 → 2 ramos pipeline

D-213 reorganiza V1 em 2 dimensões ortogonais: **físico** (`n_arquivos`) × **lógico** (`caso_logico_inferido`). Os 4 casos válidos:

| Caso | n_arquivos | caso_logico_inferido | Origem | Comparado | Ramo pipeline | Usa T-DUAL? |
|---|---|---|---|---|---|---|
| 1 | 2 | ABAS_DISTINTAS | aba A do arquivo 1 | aba B do arquivo 2 | 4-A (match) | Sim · `modo_upload="DUAL"` |
| 2 | 1 | ABAS_DISTINTAS | aba A do arquivo único | aba B do arquivo único | 4-A (match) | Sim · `modo_upload="DUAL"` (T-DUAL aceita 1 arquivo com 2 abas) |
| 3 | 1 | MESMA_ABA_EM_COLUNAS | colunas-Origem da aba X | colunas-Comparado da aba X | 4-B (linha-a-linha) | **Não** · `modo_upload="SIMPLES"` (1 arquivo, 1 aba, motor recebe DataFrame único) |
| 4 | 2 | MESMA_ABA_EM_COLUNAS | colunas-Origem da aba X do arquivo 1 | colunas-Comparado da aba X do arquivo 1 (ou arquivo 2 com aba homônima) | 4-B (linha-a-linha) | Caso raro · semanticamente equivalente ao 3 |

**Caso fora de escopo MVP** (DCV §3.1 reafirmado): 1 aba · em linhas (coluna discriminadora · POR_LINHAS) · exige RESHAPE prévio Módulo 2.

**Ponto de inferência (Etapa 3):**
- Se `aba_origem == aba_comparado` E todos os apontamentos têm `coluna_origem != coluna_comparado` → `MESMA_ABA_EM_COLUNAS`
- Se `aba_origem != aba_comparado` → `ABAS_DISTINTAS`
- Caso degenerado (mesma aba · `coluna_origem == coluna_comparado` em algum apontamento) → `B-V1-MESMA-COLUNA`
- Caso degenerado (apontamentos misturando abas) → `B-V1-MISTURA-ABAS`

---

## 2.8 · Inconsistências internas detectadas durante o eco · 0

Nenhuma inconsistência hard encontrada. **1 ambiguidade soft** identificada para reportar como bifurcação resolvida internamente (não bloqueia execução):

### Bifurcação BIF-0 · `UnidadeCanonica` é enum ou Literal?

**Contexto:** S-V1 §1.22 declara `UnidadeCanonica` como contrato consumido da Fundação · "Enum 8 valores" · D-202. Mas em `src/contratos.py` o que existe é apenas `Literal[...]` 8-valores em `ColumnMeta.unidade` (linhas 203-219) e em `ContratoComparativo.unidade` (linhas 624-639) · não há enum nominal.

**Resolução interna (D-174 Camada 1 · princípio C.3 · zero invenção):** declaro `UnidadeCanonica(str, Enum)` **localmente em `visao_v1.py`** com os mesmos 8 valores do Literal canônico. Razão: S-V1 manda enum · prompt seção 10.3 veta tocar `contratos.py`. Enum local com mesmo conjunto de valores preserva semântica e atende ambas as restrições.

**Sugestão para retrospectiva (não-V-V1):** sub-sessão futura promove `UnidadeCanonica` para enum em `contratos.py` · alinha `ColumnMeta.unidade` e `ContratoComparativo.unidade` para usar a enum (refactor cosmético da Fundação). Esta promoção fora de V-V1 evita poluir esta sessão com mudança em Fundação.

---

## 2.9 · Próximo passo

Fase 1 · Implementar `src/visoes/visao_v1.py` com 22 contratos Pydantic + 5 enums + skeleton de helpers + função pública `executar_v1(motor_result, config)` que ainda lança `NotImplementedError`. Suite-gate da Fase 1: `pytest src/testes/test_contratos_v1.py` ~20-25 verdes · suite total ainda 745 verdes herdados + ~20-25 novos.

---

*Fim do eco · Fase 0 concluída · gate: documento existe e está completo · prosseguir para Fase 1.*
