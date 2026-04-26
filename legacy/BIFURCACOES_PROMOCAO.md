# Bifurcações · Sessão de Promoção D-202 · 2026-04-26

Decisões tomadas pelo executor (Claude Code) onde o escopo permitia mais de uma
interpretação. Cada bifurcação inclui contexto · escolha feita · critério aplicado.

## B-1 · Localização das capabilities 7 e 10 com bug

**Contexto:** o escopo da Etapa 4 cita `src/apresentacao/exportacao.py` como
local dos bugs `cap_resumo_executivo` (cap 7) e `cap_diagnostico` (cap 10).
Esse arquivo **não existe**. As capabilities estão em
`src/apresentacao/resumo_executivo.py` (cap 7 · função `renderizar_resumo_executivo`)
e `src/apresentacao/diagnostico_narrativo.py` (cap 10 · função `renderizar_diagnostico`).
Há também funções legadas `cap_resumo_executivo` e `cap_diagnostico` em
`src/exportacao.py` (não em `src/apresentacao/`).

**Escolha:** corrigi os bugs nas capabilities da F-APRESENT (`apresentacao/resumo_executivo.py`
e `apresentacao/diagnostico_narrativo.py`), que são as referenciadas pelo
docstring de `exportacao_v2.py:14-22`. As funções legadas em `src/exportacao.py`
não foram tocadas (elas são consumidas por V1/V3..V11 ainda não migradas para
F-APRESENT · seu fix sai da Família A).

**Critério:** o docstring de `exportacao_v2.py` diz "capability 7" e "capability 10"
inequivocamente · a Família A consome `apresentacao.*` · não `exportacao.py`
legado · escopo da sessão é destravar V1/V11 · ambas vão consumir F-APRESENT.

## B-2 · Helpers visuais movidos via aliasing

**Contexto:** Etapa 5 movia helpers visuais (`_bordas_finas`, `_renderizar_cabecalho_secao`,
`_renderizar_secao_como_tabela`, `_calcular_altura_leitura_qualitativa`,
`_mesclar_card`, `_contrair_de`, `_rotular_agrupador`) de `exportacao_v2.py`
para os templates de Família A. Esses helpers ainda são chamados em vários
pontos de `exportacao_v2.py` que **não** estão sendo refatorados (ex.:
`_renderizar_secao_distribuicao_estrutural`, `_renderizar_resumo_executivo_v2`
restante).

**Escolha:** fiz **MOVE com re-export aliasado**. Os helpers vivem agora em
`apresentacao/templates/familia_a/_shared.py` com nomes públicos (`bordas_finas`,
`renderizar_cabecalho_secao`, etc · sem `_` líder). `exportacao_v2.py` importa
e cria alias retro-compatíveis (`_bordas_finas as bordas_finas` reverso) para
os usos remanescentes funcionarem sem reescrita.

**Critério:** suite 731 verde como gabarito (Salvaguarda 1) · zero risco de
regressão · próxima sessão pode renomear chamadores quando estiverem prontos
para refatorar.

## B-3 · `_renderizar_secao_concentracao` simplificada na promoção

**Contexto:** a função original em `exportacao_v2.py` chamava
`_renderizar_cabecalho_secao` ANTES de chamar `_renderizar_secao_como_tabela`
(que ela mesma já chama `_renderizar_cabecalho_secao` internamente). Era
double-render do banner com mesmo conteúdo no mesmo lugar.

**Escolha:** a versão promovida em `apresentacao/templates/familia_a/concentracao.py`
**remove** a chamada redundante. Comportamento idêntico (mesma célula recebe
mesmo banner uma única vez ao invés de duas vezes consecutivas com sobrescrita).

**Critério:** zero efeito observável (suite 731 verde após Etapa 5) · simplifica
código.

## B-4 · Templates de seção mantêm caminho semântico-aware na promoção

**Contexto:** as 4 funções `_renderizar_secao_*` (saude_comparacao, concentracao,
onde_se_concentra, variacoes_destaque) recebem dados específicos de Família A
(distribuição semântica · classificação semântica em 7 valores · etc).

**Escolha:** as funções foram parametrizadas com nomes explícitos (`unidade`,
`semantica`, `dist_sem`, `delta_sem`, `dist_estru`, `concentracao`,
`onde_se_concentra`, `top_list`, `agrupadores`, etc) — **não recebem `V2Result`
diretamente**. V1/V11 podem chamar passando seus próprios objetos equivalentes
ou dicts.

**Critério:** escopo Etapa 5 explicitamente pede "parâmetros explícitos · zero
acoplamento a V2Result · recebe os subobjetos que precisa".

## B-5 · `default_unidade_para_tipo_campo` em `formatos.py` (não `__init__.py`)

**Contexto:** Etapa 3 pedia "Em `src/apresentacao/formatos.py`". Função é mais
analítica (mapeia `tipo_campo` → `unidade` default) do que de formato. Poderia
fazer sentido em `apresentacao/contratos.py` (não existe) ou
`apresentacao/__init__.py`.

**Escolha:** segui o escopo literalmente · está em `formatos.py` · re-exportada
em `apresentacao/__init__.py`.

**Critério:** literalidade do escopo (formato do prompt).

## B-6 · `formatar_threshold_por_contrato` consumido por F-APRESENT cap 10 com fallback

**Contexto:** o vocabulário bilingue tem rótulos próprios para alguns thresholds
(bloco "thresholds"). A capability 10 antes traduzia via vocabulário diretamente.
Após a correção, o rótulo do **contrato** Fundação é canônico (D-166).

**Escolha:** capability 10 prioriza tradução do vocabulário; cai no rótulo do
contrato apenas quando vocabulário retorna marcador (texto começando com `[`).
Isso preserva customizações de vocabulário (testes existentes) e ainda corrige
o bug de unidade quando vocabulário não cobre uma chave.

**Critério:** zero regressão (suite 731 verde) · contrato Fundação como fallback
robusto (D-166).

## B-7 · Capability 11 não substitui `number_format_valor` em produção

**Contexto:** Etapa 7 cria capability 11 (`formato_adaptativo_por_unidade`) com
nota técnica condicional. Escopo orienta: "NÃO substituir uso atual de
`number_format_valor` em produção nesta sessão".

**Escolha:** capability 11 é função pura · adicionada · sem rewire em V2.
V2 atual continua usando `number_format_valor` · `formatar_valor_por_unidade` ·
`formatar_diferenca_por_unidade`. V1/V11 (próximas sessões) podem optar por
consumir a capability 11 (que retorna tupla com nota técnica) quando precisarem
do formato adaptativo decimal.

**Critério:** literalidade do escopo + Salvaguarda 1 (zero regressão observável).

## B-8 · Etapa 8 conservadora · 6 trims em vez de ~30 remoções

**Contexto:** Etapa 8 estimava 30-40 comentários removidos. A análise dos 81
comentários "Sessão X" / "D-1XX" / "D-2XX" mostrou que ~75% referenciam D-XXX
ou P-XX explícitos · entram em "Caso 1 mantém" do escopo. Os candidatos
órfãos legítimos eram ~10.

**Escolha:** removi 6 prefixos temporais redundantes (preservando rationale
técnico do comentário) e catalogei os outros em `COMENTARIOS_ORFAOS_V2.md`
para auditoria humana Camada 2. Não fiz remoção agressiva.

**Critério:** Salvaguarda 1 (gabarito zero regressão) · D-204 cláusula C diz
"comentários históricos viram débito SE ÓRFÃOS" · maioria não é órfã.
