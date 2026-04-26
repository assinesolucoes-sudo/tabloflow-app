# p_v2.md — Spec de Produto da V2 · Análise Comparativa entre Referências

**Visão:** V2 · Família A · Confronto entre universos
**Bloco:** P-V2 retroativo · primeira aplicação do ciclo de 6 artefatos (D-158 · §15.11 do CONTEXT)
**Marco metodológico:** abre **ALINHA-Retroação-V2 antecipada** (D-167) · primeira aplicação operacional do método novo pós-ALINHA-Descoberta-Camada-Produto (D-157 a D-166)

**Documentos consumidos:**
- DCV-V2 aprovado (18/04/2026 · 13 pendências fechadas · D-021 a D-032)
- spec_v2.md aprovada (com refinamentos D-151 · D-153 · D-154 absorvidos · 301/301 testes verdes)
- `/specs/vocabulario_bilingue.md` v1 (tabela canônica transversal · D-160)
- F-APRESENT P0 concluído (capabilities 1-7 disponíveis · 480/480 verdes · 4 amostras aprovadas)
- 14 OBS de VV-V2 original (23/04/2026 manhã · mapa concreto do que precisa mudar na camada de produto)

**Status:** aguarda aprovação da Usuária. Aprovação desta P-V2 desbloqueia:
1. Adendo §2.4 a S-V2 existente (contrato de unidade por campo · D-166) + notas D-165/D-166 nas seções afetadas
2. Refatoração de A-V2 (sessão combinada Claude Code · D-155) consumindo P-V2 + F-APRESENT P0 + separação download/aprovação (D-162)
3. Nova VV-V2 sob modalidade C mista (D-156) operando em VVC (D-162)

**Escopo cirúrgico aprovado pela Usuária (D-167):** P-V2 NOVO · S-V2 PRESERVADA com adendo · B-V2 PRESERVADA (`base_fundacao.xlsx` continua servindo · D-147) · V-V2 PRESERVADO INTEGRALMENTE (motor intacto · 301/301 testes verdes) · A-V2 REFATORADA · VV-V2 NOVA.

**Decisões de produto desta sessão (capturadas antes da redação):**
- **Paleta default:** Azul executivo (universal · todas as 11 visões · sobrescrição via C.D6) · supera D-164 que declarava defaults por visão · formaliza como **D-168** no kit de encerramento
- **Ordem widget de paleta:** Azul · Cinza · Verde · Vinho (sem microcopy semântica · só nomes)
- **Tom do Resumo Executivo:** narrativo descritivo (frases mais longas com contexto explicativo)
- **Stepper:** 4 etapas + Revisão (alinha com motor atual · D-154 parqueia bloco intermediário como P-V2-Evo-01)

---

## Preâmbulo · referências cruzadas

| Item | Onde vive |
|---|---|
| Contrato técnico (`V2Result`, enums, regras de cálculo) | `spec_v2.md` Seção 1 e 2 (preservadas integralmente) |
| Wireframe funcional textual | `spec_v2.md` Seção 3 (preservada · microcopy desta P-V2 substitui rótulos user-facing) |
| Wireframe HTML visual | `/specs/wireframe_v2.html` (preservado · refatoração visual posterior se necessário pela A-V2) |
| Casos esperados (gabarito de validação) | `casos_esperados.yaml` bloco `visoes.V2` (4 assertions · preservado integralmente · D-141) |
| Capabilities de exportação | F-APRESENT P0 (capabilities 1-7) + F-APRESENT P1 quando concluído (capabilities 8-10) |
| Tabela transversal de vocabulário | `/specs/vocabulario_bilingue.md` v1 (consumida e estendida na Seção 2 desta P-V2) |
| Amostras de paleta aplicada | F-APRESENT capability 1 · `/src/apresentacao/paletas.py` + 4 amostras visuais aprovadas em 23/04/2026 |

**Regra de conflito (consolidada · CONTEXT §5):**
- P-V2 vs `vocabulario_bilingue.md` sobre vocabulário transversal → **vocabulário transversal prevalece**
- P-V2 vs S-V2 sobre vocabulário/microcopy/arquitetura de abas → **P-V2 prevalece** (camada de produto é fonte)
- P-V2 vs S-V2 sobre contrato lógico/regra de cálculo → **S-V2 prevalece** (camada técnica é fonte)

---

## Seção 1 · Paleta executiva

### 1.1 · Paleta default da visão

**Default declarado:** Azul executivo.

**Justificativa:** Decisão de método tomada nesta sessão (D-168 a formalizar no kit) supera D-164, que declarava defaults semânticos por visão. Azul como default universal das 11 visões reduz carga cognitiva (uma decisão a menos por P-VN), garante consistência visual cross-visão para clientes que usam múltiplas visões da plataforma, e preserva semântica institucional sem viés (a V2 produz tanto leituras positivas — Realizado superou Orçado — quanto negativas — Realizado abaixo do Orçado, e Azul não pré-julga).

**Aplicação em §13.7 do CONTEXT:** Azul executivo aplicado em cabeçalhos de aba, badges semânticos (cores complementares dentro da paleta), linhas alternadas da Base Analítica, totais dinâmicos, bordas e destaques do Coração Visual.

### 1.2 · Sobrescrição pelo usuário (C.D6 · DDU)

**Aplicação direta de C.D6 (D-161 · Default Declarado Universal):** Usuária pode trocar a paleta no momento da exportação. Widget no app Streamlit:

- Tipo de componente: `st.radio` (4 opções · paleta padrão pré-selecionada)
- Posição: lado direito do botão "Baixar Excel" na E5 · Revisão (separação visual clara do controle de configuração analítica)
- Ordem fixa das opções: **Azul · Cinza · Verde · Vinho**
- Microcopy do widget: "Paleta do Excel" (label) · sem sugestão semântica nas opções (decisão da Usuária)
- Persistência: paleta selecionada vai para `config_usada.paleta_aplicada` · registrada em aba Diagnóstico seção 5 (Configurações avançadas aplicadas · D-165)
- Aplicação da troca: efeito imediato no Excel a baixar · não regenera análise (motor já calculou · paleta é só camada de apresentação)

### 1.3 · Catálogo de paletas (referência · vive em F-APRESENT capability 1)

P-V2 não duplica especificação técnica das paletas. Referência canônica em `/src/apresentacao/paletas.py` (F-APRESENT capability 1 · D-159). Amostras visuais aprovadas em 23/04/2026 (4 amostras · 1 por paleta · consumindo `V2Result` canônico) servem como referência visual desta P-V2 e são compartilhadas entre todas as P-VN.

---

## Seção 2 · Vocabulário bilingue da V2

### 2.1 · Princípio operacional

Toda superfície visível ao cliente da V2 (app Streamlit · Excel exportado · checklist user-facing · mensagens de erro) usa **exclusivamente** o vocabulário user-facing declarado nesta seção. Vocabulário técnico canônico (`AUSENTE_ORIGEM`, `campo_analisado`, `POR_LINHAS`, `B-V2-CAMPO-100-NULO`, etc.) preserva-se em S-V2, contratos Pydantic, testes, logs, código — **nunca** atravessa a fronteira para superfície visível.

### 2.2 · Consumo da tabela canônica transversal

Os blocos abaixo consomem `/specs/vocabulario_bilingue.md` v1 sem modificação:

- **Bloco 1 · Stepper Família A** (consumido como base · ver §4.2 desta P-V2 com adaptação para 4 etapas + Revisão)
- **Bloco 2 · Modos da base** (TRANSACIONAL/PRE_AGREGADO traduzidos)
- **Bloco 3 · Classificações estruturais** (V2 é a primeira consumidora · canoniza o padrão para V1/V11)
- **Bloco 4 · Tipos de campo** (taxonomia D-025 traduzida)
- **Bloco 5 · Thresholds TED** (4 thresholds da V2 traduzidos · ver §2.5 abaixo)
- **Bloco 7 · Termos proibidos** (lista negativa · checklist de conformidade · ver §2.8 abaixo)

### 2.3 · Vocabulário V2-específico · Origem e Comparado

A V2 trabalha com dois lados de um único dado. Vocabulário dual (técnico contratual ↔ user-facing) consolidado:

| Código técnico (S-V2) | User-facing app (sempre) | User-facing Excel (sempre) |
|---|---|---|
| `Origem` | "Comparar de" (label do widget) · "Origem" (após escolha · com rótulo amigável editável pela Usuária ao lado) | Rótulo amigável da Usuária (ex: "Orçado", "Antes", "Mês A", "Filial X") · "Origem" como subtítulo entre parênteses se rótulo não declarado |
| `Comparado` | "Comparar com" (label do widget) · "Comparado" (após escolha · com rótulo amigável editável pela Usuária ao lado) | Rótulo amigável da Usuária (ex: "Realizado", "Depois", "Mês B", "Filial Y") · "Comparado" como subtítulo entre parênteses se rótulo não declarado |
| `origem_rotulo_tecnico` | (nunca aparece) | (nunca aparece) |
| `origem_rotulo_ux` | "Comparar de" / rótulo amigável | Rótulo amigável da Usuária |
| `comparado_rotulo_tecnico` | (nunca aparece) | (nunca aparece) |
| `comparado_rotulo_ux` | "Comparar com" / rótulo amigável | Rótulo amigável da Usuária |

**Princípio operacional:** quando a Usuária declara rótulos amigáveis (ex: "Orçado" para Origem · "Realizado" para Comparado), esses rótulos viram a referência canônica de exibição em todo o app e em todo o Excel. Os termos técnicos "Origem" e "Comparado" só aparecem entre parênteses como subtítulo se a Usuária deixar os rótulos amigáveis em branco. Aplicação reforçada do princípio C.5 — sistema apresenta o vocabulário da Usuária, não impõe o seu.

### 2.4 · Vocabulário V2-específico · Classificações estruturais

V2 é a primeira visão a consumir o Bloco 3 da tabela canônica. Replicável em V1 e V11 com adaptação leve.

| Código técnico (enum) | User-facing app (Resumo · Coração Visual · Base Analítica) | User-facing Excel (badges · diagnóstico) | Microcopy contextual |
|---|---|---|---|
| `PRESENTE_AMBOS` | "Presente nos dois lados" | "Presente nos dois lados" | (omitido na exibição · caso normal · só contado no bloco 3 do Resumo Executivo) |
| `AUSENTE_ORIGEM` | "Apareceu no Comparado" | "Apareceu no Comparado" | "Esta combinação existe no Comparado mas não na Origem" (tooltip ou nota de rodapé) |
| `AUSENTE_COMPARADO` | "Saiu da Origem" | "Saiu da Origem" | "Esta combinação existe na Origem mas não no Comparado" (tooltip ou nota de rodapé) |
| `NULO_ORIGEM` | "Sem valor na Origem" | "Sem valor na Origem" | "Combinação presente nos dois lados · valor numérico ausente na Origem" |
| `NULO_COMPARADO` | "Sem valor no Comparado" | "Sem valor no Comparado" | "Combinação presente nos dois lados · valor numérico ausente no Comparado" |
| `NULO_AMBOS` | "Sem valor nos dois lados" | "Sem valor nos dois lados" | "Combinação presente nos dois lados · valor numérico ausente em ambos" |

**Quando rótulos amigáveis estão declarados** (ex: Origem = "Orçado" · Comparado = "Realizado"), a microcopy substitui dinamicamente:
- "Apareceu no Realizado" (em vez de "Apareceu no Comparado")
- "Saiu do Orçado" (em vez de "Saiu da Origem")
- "Sem valor no Orçado" (em vez de "Sem valor na Origem")
- etc.

Substituição feita por F-APRESENT capability 2 (rótulos user-facing universais · D-160) consumindo `comparacao_realizada.origem_rotulo_ux` e `comparado_rotulo_ux`.

**Exibição de valores `None`:** sempre como **"—"** em qualquer aba do Excel (consistência cross-visão · padrão herdável). Em situações específicas onde origem do `None` é semanticamente importante (Diagnóstico aba 4 da V2), microcopy adiciona contexto: "— (não consta)" para ausência · "— (sem valor)" para nulo. Nunca exibir `None`, `null`, `NaN`, `nan`, `(null)` ou string vazia.

### 2.5 · Vocabulário V2-específico · Tipos de campo (consome Bloco 4)

| Código técnico (S-V2 · enum) | User-facing app (E3 widget) | User-facing Excel (Parâmetros) | Microcopy contextual de seleção (E3) |
|---|---|---|---|
| `NUMERICO_ADITIVO` | "Valor somável" | "Valor somável (numérico aditivo)" | "Receita, custo, quantidade, volume · valores que fazem sentido somar entre combinações" |
| `NUMERICO_RELATIVO` | "Valor percentual ou taxa" | "Valor percentual ou taxa (numérico relativo)" | "Margem %, taxa, índice, NPS, score · valores que precisam de método de consolidação declarado" |
| `NUMERICO_NAO_ADITIVO` | "Indicador não somável" | "Indicador não somável (numérico não-aditivo)" | "Saldo bancário, estoque, preço unitário · valores pontuais que não devem ser somados" |
| `ESTADO_SITUACAO` | "Categoria ou rótulo" | "Categoria ou rótulo (estado/situação)" | "Status, classificação · sem cálculo aritmético · comparação textual entre os dois lados" |

### 2.6 · Vocabulário V2-específico · Thresholds TED (consome Bloco 5)

4 thresholds editáveis da V2 (S-V2 §2.6) traduzidos para sidebar global (D-153):

| Código técnico | Label sidebar | Microcopy de ajuda contextual | Unidade exibida |
|---|---|---|---|
| `limiar_estabilidade_pct` | "Limite de estabilidade" | "Variações com módulo abaixo deste limite são classificadas como 'Estável' no Resumo Executivo." | `1%` (não `0.01`) |
| `limiar_nulo_massivo_pct` | "Limite de nulos massivos" | "Acima deste percentual de nulos no campo, o sistema sinaliza qualidade de dado deteriorada." | `20%` (não `0.20`) |
| `limite_valores_discriminador_alerta` | "Limite de valores na coluna de comparação" | "Quando a coluna de comparação tem mais valores únicos que este limite, o sistema sugere filtragem prévia." | `50` (contagem) |
| `limite_variacao_extrema_pct` | "Limite de variação extrema" | "Variações com módulo acima deste limite recebem destaque visual de atenção no Resumo Executivo." | `1000%` (não `10.0`) |

**Persistência (S-V2 §2.6 preservada):** valores efetivos persistidos em `config_usada` e registrados em `bloco_5_leitura_qualitativa.thresholds_usados`. Flag `alguma_leitura_alterada_por_edicao` marca quando edição mudou classificação qualitativa.

**Conversão obrigatória (D-166 · contrato de unidade):** valores armazenados como proporção decimal (`0.01`) na S-V2 são **convertidos para percentual com símbolo `%`** na exibição user-facing pela F-APRESENT capability 5. Princípio reforçado: P-V2 declara unidade de exibição · S-V2 declara unidade de armazenamento · F-APRESENT faz a conversão.

### 2.7 · Vocabulário V2-específico · Modo 4 e estados

| Código técnico (S-V2) | User-facing app (E2) | User-facing Excel |
|---|---|---|
| `Modo 4` | (nunca aparece como "Modo 4") · widget aparece naturalmente quando coluna tem 3+ valores | (nunca aparece como "Modo 4") |
| Detecção de POR_LINHAS com 3+ valores únicos | "A coluna escolhida tem [N] valores diferentes. Selecione 2 para comparar:" | "Estados comparados: [valor1] vs [valor2] (entre [N] disponíveis)" no Diagnóstico |
| `estados_disponiveis` | "Valores disponíveis" (lista do widget) | "Valores disponíveis na base" (Diagnóstico aba) |
| `estados_escolhidos` | (não exibido como termo · só os 2 valores escolhidos aparecem nos rótulos) | (idem · valores escolhidos viram os rótulos das colunas no Excel) |
| `estados_nao_escolhidos` | (não exibido na configuração) | "Valores não comparados nesta análise" (Diagnóstico aba · seção 1 Como foi analisado · D-165) |

**Microcopy de ordenação inteligente (D-026):** quando motor aplica ordenação cronológica/numérica/alfabética, exibe nota declarativa abaixo do widget de seleção: "Ordenação aplicada: [cronológica · numérica · alfabética]". Quando aplica ordenação alfabética por mistura de tipos (W-V2-MIX), exibe: "Ordenação alfabética aplicada · valores na coluna mistos detectados".

### 2.8 · Vocabulário V2-específico · Warnings e bloqueios

12 warnings W-V2-* da S-V2 §2.7 + 8 bloqueios B-V2-* da S-V2 §2.5 traduzidos para superfície cliente. Padrão consome Bloco 6 do `vocabulario_bilingue.md`.

**Warnings (12 · superfície user-facing):**

| Código técnico (nunca exibido) | User-facing (sempre exibido) |
|---|---|
| `W-V2-AUSENTE-EM-UM-LADO` | "Combinações presentes em apenas um dos lados detectadas: [N] ocorrência(s)" |
| `W-NULO-MEDIDA` | "Valores ausentes detectados no campo analisado: [N] ocorrência(s)" |
| `W-V2-BZ` | "Variação % não calculável quando Origem é zero e Comparado não é zero · [N] ocorrência(s)" |
| `W-V2-NULL-MASS` | "Qualidade de dado deteriorada · acima de [TED]% do campo analisado tem valor ausente" |
| `W-V2-AGG` | "Método de consolidação aplicado: [método] · [N] combinações afetadas" |
| `W-V2-MIX` | "Coluna de comparação tem valores de tipos mistos · ordenação alfabética aplicada" |
| `W-V2-NMANY` | "Coluna de comparação tem [N] valores · acima do limite de [TED] · considere filtragem prévia" |
| `W-V2-AGRUP-MUITOS` | "[N] agrupadores selecionados · análise com granularidade fina · confirme que é o que pretende" |
| `W-V2-MOD-PARCIAL` | "Modelo aplicado parcialmente · [N] de [Total] campos casaram · ajustar manualmente os demais" |
| `W-V2-MOD-INCOMP` | "Modelo incompatível com a estrutura desta base · etapas dependentes foram zeradas" |
| `W-V2-AJUSTE-LEVE` | "Ajuste automático aplicado: [tipo do ajuste] · [N] ocorrência(s)" |
| `W-V2-DECISAO-USUARIO` | "Decisão registrada para caso estrutural: [tipo do caso] · escolha aplicada: [escolha]" |
| `W-V2-PAGREG-DUP` | "Duplicidade detectada na chave da base pré-agregada · método aplicado: SOMA" |

**Bloqueios (10 · superfície user-facing):**

| Código técnico (nunca exibido) | Mensagem user-facing |
|---|---|
| `B-V2-ARQUIVO-ILEGIVEL` | "Não foi possível ler o arquivo · formato não suportado ou arquivo corrompido. Verifique o arquivo e tente novamente." |
| `B-V2-ESTRUTURA-INVALIDA` | "A aba escolhida não tem dados ou não tem coluna numérica esperada. Verifique a aba e selecione outra se necessário." |
| `B-V2-DISCRIMINADOR-0` | "A coluna de comparação está vazia · não é possível comparar. Escolha outra coluna ou outra aba." |
| `B-V2-DISCRIMINADOR-1` | "A coluna de comparação tem apenas 1 valor único · não é possível comparar dois estados. Escolha outra coluna." |
| `B-V2-CAMPO-100-NULO` | "O campo analisado está totalmente vazio em [Origem · Comparado] · não é possível calcular. Escolha outro campo." |
| `B-V2-AGRUP-EXCESSO` | "Você selecionou [N] agrupadores · acima do máximo de 9. Para cruzamento multidimensional considere a V6." |
| `B-V2-PESO-INVALIDO` | "O campo de peso escolhido tem todos os valores zero ou negativos · não é possível calcular média ponderada. Escolha outro campo de peso." |
| `B-V2-CONSOL-IMPOSSIVEL` | "Você escolheu não consolidar mas declarou agrupadores · não é possível processar. Remova os agrupadores ou escolha outro método de consolidação." |
| `B-V2-RESULTADO-EXCEDE` | "A análise gera mais de 500.000 linhas no resultado · acima do limite operacional. Reduza agrupadores ou aplique filtros prévios." |
| `B-V2-CASO-ESTRUTURAL-CANCELADO` | "Análise cancelada por sua escolha no painel de resolução de caso estrutural. Ajuste a configuração e tente novamente." |

### 2.9 · Lista negativa · termos proibidos em superfície cliente da V2

Aplicação direta do Bloco 7 do `vocabulario_bilingue.md`. **Nunca podem aparecer** em nenhuma superfície cliente (app · Excel · checklist · mensagens):

**2.9.1 · Nomes de atributo Python literais:** `campo_analisado`, `origem_rotulo_ux`, `comparado_rotulo_ux`, `origem_rotulo_tecnico`, `comparado_rotulo_tecnico`, `limiar_estabilidade_pct`, `limite_valores_discriminador_alerta`, `tipo_estrutural`, `classificacao_estrutural`, `classificacao_semantica`, `chave_agrupadores`, `valor_origem`, `valor_comparado`, `variacao_percentual`, `comparacao_realizada`, `agrupadores_aplicados`, `resolucao_estrutural`, `distribuicao_classificacoes_estruturais`, `bloco_5_leitura_qualitativa`, `config_usada`, `modelo_aplicado`, `metodo_consolidacao_relativo`, `regra_agregacao`, qualquer outro nome de atributo do contrato Pydantic.

**2.9.2 · Enums em caps:** `POR_COLUNAS`, `POR_LINHAS`, `PRESENTE_AMBOS`, `AUSENTE_ORIGEM`, `AUSENTE_COMPARADO`, `NULO_ORIGEM`, `NULO_COMPARADO`, `NULO_AMBOS`, `TRANSACIONAL`, `PRE_AGREGADO`, `NUMERICO_ADITIVO`, `NUMERICO_RELATIVO`, `NUMERICO_NAO_ADITIVO`, `ESTADO_SITUACAO`, `MEDIA_SIMPLES`, `MEDIA_PONDERADA`, `NAO_CONSOLIDAR`, `MATRIZ_COLORIDA`, qualquer outro enum.

**2.9.3 · Códigos internos do projeto:** `D-021`, `D-024`, `D-151`, `D-167`, `P-V2-Evo-01`, `OBS-VV-V2-01`, `T-AGRUPA`, `T-PIVOT`, `T-SEMA`, `T-MODELO`, `F-MOT`, `F-APRESENT`, `B-V2-*`, `W-V2-*`, `C.D6`, `DDU`, qualquer código de método interno.

**2.9.4 · Serializações técnicas cruas:** `datetime.datetime(2026, 4, 23, 14, 32, 11)`, dict Python serializado como string (`{'visao': 'V2', ...}`), tipos Pydantic em representação debug (`<V2Result object at 0x7f...>`).

**2.9.5 · Fração decimal apresentada como percentual:** `0.0109` ou `0.01` sem conversão e sem símbolo `%`. Sempre exibir como `1,09%` ou `1%` com símbolo (D-166 · contrato de unidade).

**2.9.6 · Fonte monoespaçada em área executiva:** Resumo Executivo, Coração Visual, Base Analítica usam tipografia executiva da paleta (capability 9 de F-APRESENT P1). Monoespaçada permitida apenas no Diagnóstico quando referência técnica já traduzida.

**Violação de qualquer regra desta seção = bug.** Checklist VVC inclui inspeção visual cruzada com esta lista negativa.

---

## Seção 3 · Arquitetura de abas do Excel

### 3.1 · Estrutura canônica de 4 abas (D-165 · pós-fusão Parâmetros+Diagnóstico)

A V2 retroativa exporta Excel com **4 abas em ordem fixa** · alinhada com a estrutura canônica do TabloAnálise pós-D-165:

| # | Aba (nome user-facing) | Propósito | Tipo de aba |
|---|---|---|---|
| 1 | **Resumo Executivo** | Narrativa executiva em 6 blocos · primeira leitura · sem fórmulas · prosa | Narrativa (D-125 · §13.5 · renderizada por F-APRESENT capability 7) |
| 2 | **Matriz de Confronto** | Coração Visual da V2 · matriz colorida agrupadores × (Origem · Comparado · Δ · Δ%) com formatação condicional por semântica | Coração Visual (D-126 · §13.6 · tipo `MATRIZ_COLORIDA`) |
| 3 | **Base Analítica** | Linha por combinação de agrupadores · tabela executiva interativa · totais dinâmicos · auditoria completa | Tabular interativa (D-166 · §13.7 · `ListObject` openpyxl) |
| 4 | **Diagnóstico** | 6 seções narrativas fundindo Parâmetros + Diagnóstico técnico (D-165) · última aba (D-017) | Narrativa estruturada (D-165 · F-APRESENT capability 10 · P1) |

**Mudança vs S-V2 §2.9 (que declarava 5 abas):** D-165 fundiu "Parâmetros" e "Diagnóstico" do esquema antigo em uma única aba "Diagnóstico" com 6 seções user-facing. Aplicação canônica para todas as 11 visões.

**Princípio C.2 reforçado:** filtros ativos em todas as abas tabulares (Matriz de Confronto · Base Analítica). Resumo Executivo e Diagnóstico não têm filtros (são narrativas).

### 3.2 · Aba 1 · Resumo Executivo · 6 blocos preenchidos (D-125 · D-031)

**Renderização:** prosa executiva user-facing por F-APRESENT capability 7 · **tom narrativo descritivo** (decisão da Usuária · frases mais longas com contexto explicativo · evita lista de bullets · evita JSON dump).

**Bloco 1 · Cabeçalho da análise**

> "Comparação entre [rótulo Origem ou "Origem"] e [rótulo Comparado ou "Comparado"] aplicada ao campo [nome user-facing do campo], processada em [data · hora]. Análise estruturada por [N] agrupador(es): [lista de agrupadores user-facing]. Tipo do campo analisado: [tipo user-facing] · semântica declarada: [maior é melhor · menor é melhor · neutro]."

Quando rótulos amigáveis declarados (caso comum): "Comparação entre Orçado e Realizado aplicada ao campo Receita..."

**Bloco 2 · Números-âncora**

Para tipos numéricos (aditivo · relativo · não-aditivo):

> "O total consolidado [user-facing Origem] alcançou [valor monetário formatado BR]. O total consolidado [user-facing Comparado] alcançou [valor monetário formatado BR], representando uma [diferença consolidada formatada] em relação à [user-facing Origem] — equivalente a uma variação de [variação % formatada] no consolidado da análise."

Para tipo Estado/Situação: bloco adaptado:

> "A análise comparou [N] combinações entre [user-facing Origem] e [user-facing Comparado]. Foram identificadas [M] combinações com mudança de estado e [K] combinações estáveis, representando uma taxa de mudança de [%] no consolidado."

**Bloco 3 · Distribuição de classificações estruturais**

> "Das [Total] combinações analisadas, [N1] estão presentes nos dois lados, [N2] aparecem somente no [user-facing Comparado], [N3] saíram do [user-facing Origem], e [N4 + N5 + N6] apresentam valores ausentes (sem valor na Origem, no Comparado ou em ambos). A presença em apenas um lado representa [%] do total — atenção para investigação destes casos no detalhamento abaixo."

Categorias com 0 ocorrências omitidas da exibição (preservadas no contrato).

**Bloco 4 · Maiores variações destacadas**

> "As 10 combinações com maior impacto absoluto na análise lideram-se por [agrupador1] com diferença de [valor formatado] ([%] de variação), seguido por [agrupador2] com [valor formatado] ([%]). [Continuação descritiva quando há clusters de magnitude similar.] Detalhe completo das demais combinações disponível na aba Base Analítica."

Para Estado/Situação: lista das categorias mais afetadas pelas mudanças, em prosa.

**Bloco 5 · Leitura qualitativa**

> "A leitura qualitativa do consolidado classifica esta análise como [Positivo · Negativo · Neutro · Não aplicável], aplicando os limites de estabilidade ([X%]) e variação extrema ([Y%]) configurados nos thresholds. [Comentário sobre se algum limite foi customizado pela Usuária e qual o impacto da customização na classificação · só aparece se houve edição.]"

**Bloco 6 · Qualidade estrutural**

> "Esta análise registrou [N] ajustes automáticos do motor durante a preparação da base e [M] decisões da usuária em casos estruturais detectados. Foram identificados [K] alertas de qualidade de dado, sendo [Kc] críticos para revisão. Detalhamento completo de cada ajuste, decisão e alerta disponível na aba Diagnóstico."

Quando 0 ajustes / 0 decisões / 0 alertas:

> "Esta análise foi processada sem ajustes automáticos do motor, sem casos estruturais que exigissem decisão da usuária, e sem alertas de qualidade de dado. Detalhamento completo na aba Diagnóstico."

**Formatação Resumo Executivo:**
- Tipografia executiva da paleta (capability 9 P1 · fontes serifadas para títulos · sans-serif para corpo)
- Hierarquia de títulos: H1 (nome da visão) · H2 (cada bloco) · H3 (subseções dentro do bloco quando aplicável)
- Negrito reservado para números-âncora e nomes de agrupadores em destaque
- Sem fonte monoespaçada
- Sem listas de bullets · prosa contínua

### 3.3 · Aba 2 · Matriz de Confronto · Coração Visual (D-126 · §13.6)

**Nome canônico:** "Matriz de Confronto" (ratificado por `V2-A03` do `casos_esperados.yaml` · cumpre retroação diferida D-126 para a V2).

**Tipo:** `MATRIZ_COLORIDA` · `capabilities_requeridas=["formatacao_condicional", "congelar_paineis"]`

**Estrutura visual:**
- Linhas: 1 por combinação única de agrupadores (mesma granularidade da Base Analítica)
- Colunas: agrupadores (esquerda) + 4 colunas de comparação (Origem · Comparado · Δ · Δ%) + classificação estrutural (direita)
- Cabeçalhos: paleta executiva aplicada (Azul default · cor de fundo + texto branco)
- Painéis congelados: cabeçalho da tabela + colunas de agrupadores
- Formatação condicional aplicada por semântica T-SEMA:
  - Quando "maior é melhor" e Δ positivo: verde da paleta
  - Quando "maior é melhor" e Δ negativo: vermelho da paleta
  - Quando "menor é melhor" e Δ positivo: vermelho da paleta
  - Quando "menor é melhor" e Δ negativo: verde da paleta
  - Quando "neutro": cinza neutro da paleta · sem juízo de valor
  - Variação % com módulo > `limite_variacao_extrema_pct` (TED): destaque visual de atenção (borda ou fundo) sem viés positivo/negativo
- Coluna de classificação estrutural com badge user-facing (capability 8 · F-APRESENT P1) · cores coerentes com paleta selecionada

**Filtros ativos** em todas as colunas tabulares (capability 3 · F-APRESENT P0 com `Table.autoFilter` forçado).

**Totais dinâmicos** (capability 3 · D-166): linha de totais da tabela com função declarada por coluna na §3.5 desta P-V2.

### 3.4 · Aba 3 · Base Analítica (C.D3 · BAD)

**Estrutura tabular completa:** 1 linha por combinação única de agrupadores. Tabela Excel nativa (`ListObject` · capability 3 · D-166) com:

- Filtros ativos por default em todas as colunas
- Linha de totais dinâmicos no rodapé (recalcula com filtros aplicados)
- Linhas alternadas com paleta selecionada (efeito zebra leve)
- Painel congelado no cabeçalho

Granularidade idêntica à Matriz de Confronto · Base Analítica é a versão completa para auditoria, Matriz de Confronto é a versão visual sintética.

### 3.5 · Contrato de unidade por campo (D-166)

Declaração obrigatória para cada campo exportado nas abas tabulares. F-APRESENT capability 4 (formatação monetária BR) e capability 5 (formatação percentual com conversão fração→%) consomem este contrato.

**Aba 2 · Matriz de Confronto:**

| Campo (técnico) | Nome user-facing (coluna) | Unidade | Função de total | Notas |
|---|---|---|---|---|
| `chave_agrupadores[i]` (i = 1..N) | Nome user-facing do agrupador i (declarado pela Usuária na E4) | Texto | `none` | Coluna de chave · sem total |
| `valor_origem` | Rótulo amigável Origem (ou "Origem") | Monetário BR (`R$ #.##0,00`) ou contagem (`#.##0`) conforme tipo do campo | `sum` (aditivo) · `average` (relativo · não-aditivo) · `none` (estado) | Capability 4 |
| `valor_comparado` | Rótulo amigável Comparado (ou "Comparado") | Monetário BR ou contagem (idem `valor_origem`) | `sum` / `average` / `none` (idem) | Capability 4 |
| `diferenca` | "Diferença (Δ)" | Monetário BR ou contagem (idem) | `sum` / `average` / `none` (idem) | Capability 4 · sinal preservado |
| `variacao_percentual` | "Variação (%)" | Percentual (`0,00%`) com conversão fração→% | `none` (variações % não somam · `average` enganoso) | Capability 5 · D-166 |
| `classificacao_estrutural` | "Classificação" | Texto (badge) | `none` | Capability 8 · P1 |

**Aba 3 · Base Analítica:** mesmas colunas da Matriz de Confronto + colunas auxiliares:

| Campo (técnico) | Nome user-facing (coluna) | Unidade | Função de total | Notas |
|---|---|---|---|---|
| `classificacao_semantica` | "Leitura semântica" | Texto (badge) | `none` | Aparece só para tipos numéricos · ausente para `ESTADO_SITUACAO` |
| `flags` | "Alertas" | Texto (lista de warnings traduzidos) | `none` | Microcopy do §2.8 desta P-V2 |

### 3.6 · Colunas adaptativas declaradas (D-166 · capability 6)

Estrutura da aba Base Analítica e Matriz de Confronto **monta-se dinamicamente** conforme `V2Result.config_usada`:

**Caso 1 · POR_COLUNAS:** colunas `estado_origem` e `estado_comparado` **omitidas** (campo conceitual nunca tem coluna real associada · OBS-11g de VV-V2). Cabeçalhos das colunas `valor_origem` e `valor_comparado` recebem direto os rótulos amigáveis.

**Caso 2 · POR_LINHAS:** colunas `estado_origem` e `estado_comparado` **incluídas** com valores escolhidos no Modo 4. Cabeçalhos recebem rótulos amigáveis + estado entre parênteses (ex: "Orçado (Jan/2026)").

**Caso 3 · Tipo `ESTADO_SITUACAO`:** coluna `variacao_percentual` **omitida** (variação % não se aplica a categórico). Coluna `diferenca` substituída por "Mudança" com valores "Mudou" · "Manteve" · "—".

**Caso 4 · Coluna constante nula em todas as linhas:** **omitida** (sem valor analítico). Exceção: se a coluna está declarada como agrupador essencial pela Usuária (E4), aparece com aviso na aba Diagnóstico.

**Princípio operacional:** F-APRESENT capability 6 monta a estrutura · `exportacao.py` consome decisão · A-V2 não interfere na escolha de colunas.

### 3.7 · Aba 4 · Diagnóstico · 6 seções (D-165)

Última aba · obrigatória (D-017) · 6 seções narrativas fundindo Parâmetros + Diagnóstico antigo. Renderizada por F-APRESENT capability 10 (P1).

| Seção | Conteúdo | Origem dos dados |
|---|---|---|
| 1 · Como foi analisado | Arquivo · aba escolhida · estrutura (POR_COLUNAS / POR_LINHAS) · rótulos Origem/Comparado declarados · valores escolhidos (Modo 4 quando aplicável) · agrupadores · regra de agregação · método de consolidação · semântica · tipo do campo | `comparacao_realizada` + `config_usada` + `agrupadores_aplicados` |
| 2 · Ajustes do motor | Lista de `AJUSTE_LEVE` aplicados pelo motor (tipo de ajuste · onde ocorreu · volume afetado) · prosa narrativa | `diagnostico.ajustes` · filtrado por categoria `AJUSTE_LEVE` |
| 3 · Pontos de atenção | Warnings W-V2-* com tradução user-facing (§2.8 desta P-V2) · agrupados por categoria (qualidade · estrutural · cálculo) | `diagnostico.warnings` · tradução via F-APRESENT capability 2 |
| 4 · Decisões do usuário | Lista de `DECISAO_USUARIO` registradas (caso estrutural detectado · escolha aplicada) · prosa narrativa | `diagnostico.ajustes` · filtrado por categoria `DECISAO_USUARIO` · `resolucao_estrutural` |
| 5 · Configurações avançadas aplicadas | Thresholds TED efetivos (com indicação se foram editados pela Usuária ou se mantiveram default) · paleta selecionada · modelo aplicado se houve | `bloco_5_leitura_qualitativa.thresholds_usados` + `config_usada.paleta_aplicada` + `modelo_aplicado` |
| 6 · Qualidade estrutural | Total de warnings · contagem por categoria · ajustes resolvidos · tem bloqueios escapados (sempre `Não` para V2) · tempo por etapa do motor | `bloco_6_qualidade_estrutural` + `motor_meta.tempo_por_etapa` |

**Sem fonte monoespaçada na aba Diagnóstico** · prosa narrativa user-facing. Quando referência técnica precisa aparecer (ex: nome de campo original da base), entre aspas e em fonte serifada da paleta.

---

## Seção 4 · Microcopy de telas

### 4.1 · Header persistente (todas as etapas)

- **Título da página:** "V2 · Análise Comparativa entre Referências"
- **Botão "Objetivo da Visão"** (§13.1 do CONTEXT · D-028) · abre painel lateral com 4 seções:
  1. **O que faz** · "A V2 compara dois recortes do mesmo dado e responde o que mudou, quanto mudou e como interpretar a mudança no negócio. Você indica qual é a referência inicial e qual é a referência seguinte ou paralela, escolhe os agrupadores que definem o nível da análise, e a V2 entrega uma leitura estruturada com diferença, variação percentual e classificação automática para cada combinação."
  2. **Quando usar** · "Use a V2 para comparar Orçado vs Realizado, Antes vs Depois, Meta vs Resultado, Mês A vs Mês B, Filial X vs Filial Y. Para análise de evolução ao longo de uma sequência inteira (mês a mês, etapa a etapa), use a V3. Para conciliar duas bases distintas registro a registro, use a V1. Para participação ou Pareto, use a V4 ou V10."
  3. **O que você obtém** · "Uma linha por combinação dos agrupadores escolhidos, com valor da Origem, valor do Comparado, diferença, variação percentual e classificação. Excel executivo com Resumo Executivo narrativo, Matriz de Confronto colorida com formatação por semântica, Base Analítica para auditoria, e Diagnóstico estrutural completo na última aba."
  4. **Como funciona** · "Você sobe a base, escolhe a aba, indica como a comparação está estruturada (dois lados em colunas distintas ou empilhados em linhas com coluna identificadora), define o que comparar (campo, tipo, semântica), escolhe os agrupadores, revisa e processa. O sistema consolida os dados antes de comparar, calcula diferenças e variações por combinação, classifica estruturalmente cada uma, e gera o Excel executivo."
- **Botão "Aplicar modelo"** (T-MODELO · D-030) · abre seleção de modelos salvos desta visão
- **Botão "Salvar como modelo"** (T-MODELO) · aparece a partir da E4 concluída
- **Stepper de 4 etapas + Revisão** visível · etapas concluídas em verde · etapa ativa em destaque · etapas futuras travadas

### 4.2 · Stepper user-facing · 4 etapas + Revisão

Decisão consolidada nesta sessão (alinha com motor real · D-154 · bloco intermediário condicional parqueado como P-V2-Evo-01).

**Stepper visível na barra superior em todas as etapas:**

```
1 · Escolher arquivo  →  2 · Reconhecer estrutura  →  3 · Configurar análise  →  4 · Agrupar  →  Revisar e executar
```

Mapeamento técnico interno (S-V2 §3 preservada):
- "1 · Escolher arquivo" = E1 (Origem dos dados)
- "2 · Reconhecer estrutura" = E2 (Estrutura da comparação)
- "3 · Configurar análise" = E3 (O que comparar)
- "4 · Agrupar" = E4 (Como agrupar)
- "Revisar e executar" = E5 (Revisão e execução)

**Mecânica de invalidação preservada (S-V2 §3.10):** mudar uma etapa invalida etapas seguintes · estado preservado quando possível.

### 4.3 · Microcopy E1 · Escolher arquivo

**Título da etapa:** "Escolher arquivo"
**Subtítulo:** "Suba o arquivo Excel ou CSV com os dados que você quer comparar."

**Widget upload:**
- Label: "Arquivo da análise"
- Texto de instrução: "Arraste o arquivo aqui ou clique para escolher · formatos aceitos: .xlsx, .xls, .csv"
- Tamanho máximo declarado: "Tamanho máximo: [X MB]"

**Após upload bem-sucedido:**
- Mensagem de confirmação: "Arquivo carregado: [nome do arquivo] · [N] linhas detectadas"
- Se Excel multi-aba · widget de seleção de aba:
  - Label: "Aba a analisar"
  - Texto: "Este arquivo tem [N] abas. Escolha a aba com os dados a comparar."
  - Default declarado (DDU · C.D6): primeira aba não-vazia · com nota "Sugestão: [nome da aba] · [N] linhas. [Alterar]"

**Resumo ao concluir:** "Arquivo: [nome] · Aba: [nome] · [N] linhas detectadas"

**Botão de avançar:** "Próximo · Reconhecer estrutura"

### 4.4 · Microcopy E2 · Reconhecer estrutura

**Título da etapa:** "Reconhecer estrutura"
**Subtítulo:** "Indique como a comparação está organizada na sua base."

**Widget de estrutura:**
- Label: "Como os dois lados da comparação estão organizados?"
- Opção 1: "Cada lado em uma coluna distinta" (mapeia para POR_COLUNAS) · microcopy: "Ex: coluna 'Orçado' e coluna 'Realizado' lado a lado"
- Opção 2: "Os dois lados empilhados em uma coluna identificadora" (mapeia para POR_LINHAS) · microcopy: "Ex: coluna 'Cenário' com valores 'Orçado' e 'Realizado' nas linhas"
- Default declarado (DDU): motor sugere a estrutura mais provável com base na detecção · widget pré-selecionado · com nota "Sugestão: [estrutura]. [Alterar]"

**Se POR_COLUNAS:**
- Widget Origem: "Comparar de" · dropdown com colunas numéricas detectadas
- Widget Comparado: "Comparar com" · dropdown com colunas numéricas detectadas
- Widget rótulo amigável Origem: "Como chamar este lado? (opcional)" · placeholder "Ex: Orçado, Antes, Mês A"
- Widget rótulo amigável Comparado: "Como chamar este lado? (opcional)" · placeholder "Ex: Realizado, Depois, Mês B"

**Se POR_LINHAS:**
- Widget coluna identificadora: "Em qual coluna estão os dois lados?" · dropdown com colunas categóricas detectadas
- Após escolha · se 2 valores únicos: widget "Comparar de" / "Comparar com" com os 2 valores
- Após escolha · se 3+ valores únicos (Modo 4 · sem mencionar termo técnico):
  - Mensagem: "A coluna [nome] tem [N] valores diferentes. Selecione 2 para comparar:"
  - Widget de seleção dupla: "Comparar de" (dropdown) e "Comparar com" (dropdown)
  - Default declarado (DDU): primeiro e último na ordenação aplicada · com nota "Sugestão: comparar [primeiro] vs [último]. [Alterar]"
  - Nota de ordenação: "Ordenação aplicada: [cronológica · numérica · alfabética]"
- Widgets de rótulo amigável idênticos ao caso POR_COLUNAS

**Resumo ao concluir:**
- Quando POR_COLUNAS: "Comparar de: [rótulo amigável ou nome da coluna] · Comparar com: [rótulo amigável ou nome da coluna] · Estrutura: dois lados em colunas distintas"
- Quando POR_LINHAS: "Comparar de: [valor escolhido] ([rótulo amigável]) · Comparar com: [valor escolhido] ([rótulo amigável]) · Estrutura: dois lados empilhados na coluna [nome]"

**Botão de avançar:** "Próximo · Configurar análise"

### 4.5 · Microcopy E3 · Configurar análise

**Título da etapa:** "Configurar análise"
**Subtítulo:** "Escolha o campo a analisar e como ele se comporta."

**Widget campo a analisar:**
- Label: "Campo a analisar"
- Dropdown com colunas numéricas (e categóricas se relevante para Estado/Situação)
- Microcopy: "Este é o valor que você quer comparar entre os dois lados."

**Widget tipo do campo (consome §2.5 desta P-V2):**
- Label: "Como esse campo se comporta?"
- 4 opções com descrições do §2.5
- Default declarado (DDU): motor sugere com base no nome do campo + amostra de dados · com nota "Sugestão: [tipo]. [Alterar]"

**Widget semântica:**
- Label: "Subir é bom, ruim ou neutro?"
- 3 opções: "Subir é bom (maior é melhor)" · "Subir é ruim (menor é melhor)" · "Neutro · sem viés"
- Microcopy: "Esta escolha define se variações positivas aparecem em verde ou vermelho."
- Não aparece se tipo é Estado/Situação

**Widget método de consolidação** (só aparece se tipo é Numérico relativo ou Numérico não-aditivo · D-024):
- Label: "Como consolidar este campo quando você agrupa?"
- 3 opções:
  - "Média simples" (default) · microcopy: "Calcula a média aritmética dos valores antes de comparar"
  - "Média ponderada" · microcopy: "Pondera por outro campo · você escolhe qual"
  - "Não consolidar" · microcopy: "Mantém os valores individuais · só funciona sem agrupadores"
- Se "Média ponderada" escolhida: widget adicional "Campo de peso" com dropdown

**Widget modo da base** (consome §2.4 da S-V2 · S-V2 §2.3):
- Label: "Sua base já está pré-agregada (1 linha por combinação)?"
- Toggle on/off
- Default declarado (DDU): motor sugere com base na detecção de unicidade da chave · com nota correspondente
- Microcopy: "Marque se cada combinação dos agrupadores aparece exatamente 1 vez na base. O sistema valida sem alterar os dados."

**Sidebar global · Configurações avançadas (D-153 · sempre visível desde E1):**
- Título: "Configurações avançadas"
- 4 thresholds TED traduzidos (consome §2.6 desta P-V2)
- Cada threshold com label · microcopy de ajuda · valor atual · botão de edição · indicação se foi editado vs default
- Microcopy de aviso: "Edições aqui afetam apenas a leitura qualitativa do Resumo Executivo. Os cálculos principais (Diferença, Variação %, Classificação) não são afetados."

**Resumo ao concluir:** "Campo: [nome] · Tipo: [tipo user-facing] · Semântica: [direção]" + " · Consolidação: [método]" (só se aplicável) + " · Base pré-agregada" (só se marcado)

**Botão de avançar:** "Próximo · Agrupar"

### 4.6 · Microcopy E4 · Agrupar

**Título da etapa:** "Agrupar"
**Subtítulo:** "Defina por quais dimensões a comparação será feita."

**Widget agrupadores:**
- Label: "Agrupar por"
- Multi-select com colunas categóricas detectadas
- Microcopy: "Cada combinação dos agrupadores escolhidos vira uma linha do resultado."

**Estimativa em tempo real (D-027):**
- Aparece logo abaixo do widget conforme Usuária adiciona/remove agrupadores
- Texto: "Estimativa: [N] linhas no resultado"
- Quando entra em zona de aviso (4-5 agrupadores): "[N] linhas estimadas · análise grande"
- Quando entra em zona de confirmação (6-8 agrupadores): "[N] linhas estimadas · análise muito granular" + checkbox: "Entendi o impacto · seguir com [N] agrupadores"
- Quando entra em zona de bloqueio (9+ agrupadores): widget muda para mensagem de bloqueio (microcopy do §2.8 · `B-V2-AGRUP-EXCESSO`)

**Widget regra de agregação:**
- Label: "Como consolidar valores quando há múltiplas linhas por combinação?"
- 5 opções: "Soma" (default · só para Numérico aditivo) · "Média" · "Máximo" · "Mínimo" · "Contagem"
- Default declarado (DDU): por tipo do campo (Soma para aditivo · Média para relativo/não-aditivo · Contagem para Estado/Situação)
- Microcopy: "Esta regra é aplicada antes de comparar entre os dois lados."

**Resumo ao concluir:** "Agrupadores: [lista user-facing] · Agregação: [método] · Estimativa: [N] linhas no resultado"

**Botão de avançar:** "Próximo · Revisar e executar"

### 4.7 · Microcopy Revisar e executar

**Título da etapa:** "Revisar e executar"
**Subtítulo:** "Confira a configuração antes de processar."

**Painel de revisão (preview compacto):**
- Bloco "Arquivo" (resumo E1)
- Bloco "Estrutura" (resumo E2)
- Bloco "O que comparar" (resumo E3)
- Bloco "Agrupadores" (resumo E4)
- Bloco "Configurações avançadas" (thresholds TED · só mostra se algum foi editado)
- Bloco "Modelo aplicado" (só mostra se houve)

Cada bloco com botão "Editar" que volta para a etapa correspondente.

**Antes do botão de processar · widget paleta (§1.2 desta P-V2):**
- Label: "Paleta do Excel"
- 4 opções `st.radio` na ordem **Azul · Cinza · Verde · Vinho**
- Default: Azul (pré-selecionado)
- Sem microcopy semântica (decisão da Usuária)

**Botão principal:** "Processar análise"

**Após processamento bem-sucedido:**
- Mensagem: "Análise processada com sucesso · [N] combinações analisadas em [T] segundos"
- Widget de download: "Baixar Excel" (botão grande · destaque)
- **Separação download/aprovação (D-162):** download disponível imediatamente · independente do checklist de aprovação. Microcopy abaixo do botão: "Você pode baixar e revisar o Excel antes de confirmar a aprovação da análise."
- Painel de checklist user-facing aparece logo abaixo (Seção 5 desta P-V2)

### 4.8 · Microcopy de erros e bloqueios

Bloqueios da §2.8 desta P-V2 renderizam-se como **estado de erro ortogonal** (S-V2 §3.1 preservada):

- Banner vermelho no topo da etapa onde o bloqueio dispara
- Título: "Não foi possível continuar"
- Mensagem user-facing do §2.8 (texto da segunda coluna)
- Botão "Voltar à etapa anterior" ou "Nova análise" conforme tipo do bloqueio
- Sem código técnico exibido (`B-V2-*` nunca aparece)

### 4.9 · Microcopy de warnings (não-bloqueantes)

Warnings da §2.8 renderizam-se como banner amarelo (alerta) ou cinza (informativo):

- Posição: logo abaixo do widget que disparou o warning · ou na E5 · Revisão se warning é de execução
- Título: "Atenção" (alertas) · "Informação" (informativos)
- Mensagem user-facing do §2.8
- Sem código técnico exibido (`W-V2-*` nunca aparece)
- Quando warning permite ação (ex: revisar agrupadores): botão de ação contextual

---

## Seção 5 · Checklist user-facing (esqueleto · aplicação operacional aguarda VVP)

### 5.1 · Princípio

Esta seção define o **esqueleto** do checklist user-facing da V2. **Aplicação operacional** aguarda a sessão futura "Definição operacional VVP" (D-162 · horizonte parqueado pós-Família A em VVC). O checklist técnico do VVC continua sendo o derivado do `casos_esperados.yaml` via 5 templates (D-148).

**Diferença fundamental:**
- **Checklist VVC (técnico · operacional hoje):** Usuária construtora opera · vocabulário técnico permitido · derivado mecânico do YAML · 4 itens da V2 (V2-A01 a V2-A04)
- **Checklist VVP (user-facing · aguarda protocolo):** cliente final opera · vocabulário exclusivamente user-facing · derivado das tabelas de vocabulário bilingue · estrutura definida nesta P-V2

### 5.2 · Estrutura do checklist user-facing da V2

Tradução dos 4 itens do checklist técnico VVC (S-V2 §3.9 · derivados de `V2-A01` a `V2-A04`) para vocabulário user-facing aplicando §2 desta P-V2:

```
Checklist de leitura · V2 · Análise Comparativa entre Referências

[ ] Item 1 · Combinações com presença em apenas um lado
    O Excel mostra entre 2 e 4 combinações marcadas como "Apareceu no
    [Comparado]" ou "Saiu do [Origem]" no campo Produto da análise?
    (Esperado: warning "Combinações presentes em apenas um dos lados
    detectadas" deve aparecer no Diagnóstico)

[ ] Item 2 · Valores ausentes detectados
    O alerta "Valores ausentes detectados no campo analisado" aparece
    no Diagnóstico com 3 ou 4 ocorrências?

[ ] Item 3 · Estrutura do Excel
    O Excel tem a aba "Resumo Executivo" como primeira aba (em prosa
    narrativa · 6 blocos)? E a aba "Matriz de Confronto" logo em seguida
    (com formatação colorida por semântica)?

[ ] Item 4 · Estados comparados
    O resultado mostra exatamente 2 estados sendo comparados (2025-01 e
    2025-02) na coluna identificadora "Mês" da análise?
```

### 5.3 · Critérios de aprovação (consome D-162)

**Aprovação VVP (cliente final · futuro):**
1. Checklist user-facing · todos os itens ✅
2. Excel aberto por executivo sem contexto prévio (teste de clareza standalone)
3. Cliente real opera sem assistência técnica
4. Mínimo 1 base real por vertical-alvo (3 vertical-alvos testados para declarar produto validado)
5. Registro: planilha aba 1 · Zona 3 · linha VVP

**Aprovação VVC (Usuária construtora · operacional hoje):** 5 critérios da D-162 mantidos integralmente · não definidos nesta seção · vivem na S-V2 §3.9 e na convenção VV-VN (D-156).

### 5.4 · Pendência operacional declarada (anti-esquecimento · C.2)

A aplicação operacional desta seção 5 (protocolo de execução de VVP · ferramenta · sessão · registro) será definida em sessão futura "Definição operacional VVP" quando Família A estiver completa em VVC (V2 retroagida + V1 + V11). Esta P-V2 declara a estrutura para garantir que o vocabulário user-facing da V2 esteja disponível quando o protocolo for ativado.

---

## Notas operacionais finais

### Sobre conformidade com `vocabulario_bilingue.md` v1

Esta P-V2 é a primeira aplicação prática da tabela canônica transversal. Aplicação esperada:
- Bloco 1 (stepper): consumido em §4.2 com adaptação para 4 etapas + Revisão (decisão desta sessão)
- Bloco 2 (modos da base): consumido em §4.5 (toggle de pré-agregado)
- Bloco 3 (classificações estruturais): consumido em §2.4 (V2 canoniza padrão para V1/V11)
- Bloco 4 (tipos de campo): consumido em §2.5
- Bloco 5 (thresholds TED): consumido em §2.6
- Bloco 6 (warnings universais): consumido em §2.8 com extensão V2-específica
- Bloco 7 (termos proibidos): consumido em §2.9 com extensão V2-específica

**Termos novos candidatos a entrar na tabela transversal v2** (Arquiteto consolida no kit δ de ALINHA seguinte):
- "Comparar de" / "Comparar com" (Família A inteira usa · candidato a Bloco 1 estendido)
- "Apareceu no [Comparado]" / "Saiu do [Origem]" (substituição dinâmica de classificações com rótulos amigáveis · candidato a Bloco 3 estendido)
- "—" como exibição canônica de `None` (cross-visão · candidato a Bloco novo · "Exibição de valores ausentes")

### Sobre a relação com S-V2 e A-V2

- **S-V2 preservada integralmente** · esta P-V2 não invalida nenhuma decisão da S-V2 · apenas adiciona camada de produto
- **Adendo §2.4 a S-V2** (D-166 · contrato de unidade por campo) será produzido em sessão dedicada após aprovação desta P-V2 · escopo cirúrgico declarado em D-167
- **A-V2 refatorada** consumirá P-V2 + S-V2 + F-APRESENT P0 · sessão combinada Claude Code (D-155) · futura

### Sobre a relação com V1 e V11 (Família A)

A V2 retroativa estabelece o padrão da Família A. V1 e V11 herdarão:
- Vocabulário de Origem/Comparado (§2.3) com adaptação para T-DUAL (duas bases ao invés de dois lados de uma base)
- Vocabulário de classificações estruturais (§2.4) com adaptação:
  - V1: 6 categorias preservadas (Conciliado · Divergente por valor · Só em A · Só em B · Divergência por duplicidade · Divergência por ambiguidade)
  - V11: 5 categorias adaptadas (par exato · par aproximado · sem par lado A · sem par lado B · ambiguidade de match)
- Estrutura do Excel (§3.1) idêntica · Coração Visual específico (Mapa de Conciliação para V1 · Mapa de Aderência para V11)
- Stepper user-facing (§4.2) com adaptação leve (E1 ganha upload duplo via T-DUAL)
- Tom narrativo do Resumo Executivo (§3.2) · idêntico em prosa descritiva
- Princípio Excel é produto (§13.7 · D-163) · idêntico
- Princípio C.D6 (DDU · D-161) · idêntico em todos os pontos de aplicação

### Sobre a evolução desta P-V2

Esta P-V2 é versão 1 (retroativa). Refinamentos emergentes durante:
- A-V2 refatorada (sessão Claude Code futura): podem virar P-V2-Evo-NN
- VV-V2 nova (modalidade C mista): podem virar P-V2-Evo-NN ou D-XXX nova
- Aplicações em V1 e V11: podem retroagir para P-V2 se padrão se consolidar

Convenção de evolução preserva D-167 (escopo cirúrgico) · refinamentos vão para P-V2-Evo-NN sem reescrever esta P-V2 base.

---

*Fim da P-V2 retroativa. Aguardando aprovação da Usuária. Após aprovação, próximo passo operacional é o adendo §2.4 a S-V2 existente (D-166) seguido de sessão combinada Claude Code para A-V2 refatorada.*
