# DECISIONS.md — TabloFlow

Log central de decisões estruturais e de contrato do projeto. Ordem cronológica reversa (mais recente no topo).

---

## Quando registrar uma decisão aqui

Adicione uma entrada quando a decisão:
- Fecha uma pendência aberta em alguma spec
- Muda contrato, comportamento ou interface entre blocos
- Seria custosa de redescobrir depois ("por que escolhemos X em vez de Y?")
- Tem impacto em mais de uma visão ou em camadas transversais (motores, contratos, fluxo)

**NÃO registrar aqui:**
- Decisões puramente de implementação interna a um bloco (ficam no código/spec)
- Escolhas de nomenclatura local
- Decisões já consolidadas no `CONTEXT.md` (regras) ou na planilha (estado vivo)

A fonte de verdade canônica continua sendo a spec correspondente — este arquivo é o **histórico cronológico** dessas decisões, com a razão por trás delas.

---

## Formato de cada entrada

```
### D-XXX — Título curto da decisão
**Data:** AAAA-MM-DD · **Bloco:** B-N ou Bloco N · **Status:** Fechada / Provisória / Revogada
**Contexto:** Qual problema ou pendência originou a decisão.
**Decisão:** O que foi escolhido, em uma frase.
**Razão:** Por que essa opção e não as alternativas.
**Impacto:** O que muda na implementação · em que arquivos.
**Referência canônica:** Onde a decisão vive como contrato (spec, CONTEXT.md, etc.).
```

Numeração D-XXX é sequencial global do projeto (não reinicia por visão).
---

## Nota de sessão · 23/04/2026 · VV-V2

Sessão de descoberta estrutural · 14 OBS formalizadas · 12 decisões tomadas pela Usuária · consolidadas em `VV-V2-Descoberta-Consolidada.md` (no painel do projeto) · formalização em D-XXX numeradas acontece em ALINHA-Descoberta-Camada-Produto (próxima sessão · Marco D-142 · 4ª aplicação emergente). Decisões tomadas (referência rápida · nomenclatura provisória):

- DEC-01 · Excel = produto (veículo principal de entrega)
- DEC-02 · 4 paletas executivas canônicas (Azul · Verde · Cinza · +1)
- DEC-03 · Parâmetros+Diagnóstico fundem em "Diagnóstico" (6 seções · user-facing)
- DEC-04 · Excel interativo (totais dinâmicos · colunas adaptativas · formatação)
- DEC-05 · Opção B confirmada · V2 MVP técnico · ALINHA-Retroação-V2 horizonte
- DEC-06 · Vocabulário bilingue obrigatório (técnico canônico vs user-facing)
- DEC-07 · Novo artefato P-VN · Fase 2 com 6 artefatos por visão
- DEC-08 · Novo bloco F-APRESENT · subsistema de apresentação na Fundação
- DEC-09 · Default declarado D-024 universal (toda sugestão com evidência)
- DEC-10 · B.4 desdobra em 2 camadas (Validação Visual Construtora + Produto)
- DEC-11 · Próxima sessão é ALINHA-Descoberta-Camada-Produto
- DEC-12 · 14 OBS formalizadas como material de abertura do ALINHA

Planilha aba 2 · V2 passa de ✅✅✅✅⬜ para ✅✅✅✅⚠️ (MVP técnico). Planilha aba 1 · novo horizonte ALINHA-Retroação-V2 inserido na Zona 1. Suite pytest continua 301/301 verde (motor correto · descoberta é de camada nova).

---
## D-156 — Padrão VV-VN · Validação Visual acompanhada modalidade C mista com 3 pontos-chave
Data: 2026-04-23 · Bloco: A-V2 (retrospectiva · sessão combinada 2ª aplicação) · Status: Fechada · vigora a partir da VV-V2

Contexto: §15.1 declarava Validação Visual como sessão solo da Usuária · carregar
base_vN_cliente, marcar checklist ✅/❌, disparar investigação em sessão separada
se ❌. Retrospectiva A-V2 revelou limitação do formato solo: (a) investigação
reativa em sessão separada perde contexto de operação ao vivo, (b) sugestões
emergentes durante VV ficam órfãs (sem canal imediato para virar P-VN-Evo ou
D-XXX), (c) Usuária declarou em A-V2 necessidade de apoio e espaço para
sugestões durante operação · não só pós-fato. D-131 princípio 4 (Usuária não lê
código) continua vigente · mudança é sobre presença do Arquiteto, não sobre
papel da Usuária.

Decisão: Substituir Validação Visual solo por bloco VV-VN · Validação Visual
acompanhada · modalidade C mista · Arquiteto presente em chat concomitante ·
Usuária opera silenciosamente com 3 pontos-chave canônicos + gatilhos livres.
3 pontos-chave: (1) pós-processamento Tela 8 · (2) pré-checklist Tela 9 ·
(3) pós-exportação Excel. Gatilhos livres: travamento · observações · diagnóstico
de ❌. 4 tipos de intervenção do Arquiteto: apoio operacional · resolução de ❌ ·
sugestão emergente (absorção silenciosa OU P-VN-Evo-NN OU D-XXX) · encerramento.
Preserva gate B.4 e D-148 integralmente · Arquiteto NÃO decide ✅/❌.

Nova categoria em D-131 princípio 3: "validação de produto" junta-se a (negócio ·
técnica pura · execução de código supervisionada) como quarto tipo de conteúdo
sinalizável na abertura de sessão. Nomeação canônica: VV-VN (ex: VV-V2 · VV-V1 ·
VV-V11).

Razão: (1) Padrão D-131 já demonstrou em 10 aplicações que a didática
técnico-decisional se beneficia de presença concomitante do Arquiteto · VV-VN é
a extensão natural desse princípio para o único bloco do ciclo que até então era
solo. (2) Sugestões de refinamento emergem com alta probabilidade durante primeira
operação real de produto · formato solo perde essas sugestões ou as transforma em
sessão reativa (custo maior). (3) Princípio 5 de D-131 (transparência mútua sobre
calibração) aplica-se diretamente. (4) Modalidade C mista preserva autonomia da
Usuária · Arquiteto não interfere em cada clique · só nos 3 pontos-chave +
gatilhos · evita patologia de sessão tutelada. (5) Gate B.4 inviolável · Arquiteto
pode comentar mas NÃO decide ✅/❌.

Maturação: padrão considerado maduro após VV-V2 · VV-V1 · VV-V11 (Família A
completa · mesmo critério de D-131 com 9 aplicações). Revisável se sessão VV-VN
sistematicamente exceder 2h ou se intervenção do Arquiteto virar rotineira a
ponto de a modalidade C colapsar em tutoria passo-a-passo.

Impacto:
- CONTEXT §15.1 · tabela "Quem faz o quê" · linha reescrita (participação
  Arquiteto passa de "nenhuma" para "presente em chat modalidade C")
- CONTEXT §15.2 · plano operacional · VV-VN substitui "Validação Visual" na tabela
- CONTEXT §15.8 · nova seção formaliza padrão VV-VN integralmente
- CONTEXT §14 princípio 3 · 4ª categoria "validação de produto" adicionada
- Instrucoes_do_Projeto.md · tabela tipos de bloco · VV-VN adicionado ·
  "Como me usar" ganha comando "Conduzir VV-VN" · "Não fazer" · item sobre não
  decidir ✅/❌ como Arquiteto + não colapsar modalidade C em tutoria
- GLOSSARIO.md · verbete "Validação Visual" reformulado como "VV-VN" · novo
  verbete "Validação de Produto" (frente parqueada distinta) · verbetes V-VN e
  A-VN atualizados com referência a D-155
- Frente parqueada "Validação de Produto" (bases reais · pós-Família A) permanece
  distinta · VV-VN usa base_vN_cliente sintética

Referência canônica: A-V2 retrospectiva · CONTEXT §15.1 e §15.8 · §14 · D-131
(princípio 3 estendido · princípio 4 preservado) · D-148 (derivação do checklist
preservada) · B.4 (gate preservado) · D-155 (sessão combinada · precedente
metodológico de evolução do formato de sessão na Fase 2)


## D-155 — Padrão sessão combinada · produção do prompt + retrospectiva em 1 bloco Arquiteto · convenção Família A
Data: 2026-04-23 · Bloco: A-V2 (retrospectiva) · Status: Fechada · vigora desde V-V1/A-V1

Contexto: §15.1 original declarava V-VN e A-VN como 2 sessões cada (1 produção
de prompt · 1 retrospectiva pós-Claude Code) · totalizando 4 sessões Arquiteto
por visão. V-V2 (22/04/2026) foi conduzida em sessão combinada por exceção
operacional (Usuária sinalizou fluidez de fazer num bloco só) · produziu D-151
naturalmente na retrospectiva. A-V2 (23/04/2026 · esta) repetiu o padrão ·
segunda aplicação consecutiva · agora formalizada.

Decisão: Convenção Família A (V-V1 · A-V1 · V-V11 · A-V11 e demais visões se
padrão for herdado): produção do prompt técnico + retrospectiva acontecem no
MESMO bloco Arquiteto · sessão combinada. Fluxo: Arquiteto produz prompt →
pausa para Usuária copiar e executar em sessão Claude Code (terminal dedicado) →
Usuária retorna ao chat com artefatos gerados → Arquiteto valida contra Spec,
identifica D-XXX candidatas, entrega kit D-033 ao final. Zero obrigatoriedade
do padrão para Módulos/famílias posteriores · decisão restrita a Família A com
revisão após V11 validada.

Razão: (1) Sessões combinadas de V-V2 e A-V2 demonstraram empiricamente que o
contexto da produção do prompt se mantém quente durante a retrospectiva ·
Arquiteto recém-produziu o prompt · lembra exatamente das decisões e fronteiras
· retrospectiva fica mais precisa que quando separada por outra sessão
intermediária. (2) Redução de ~1 sessão por bloco (V-VN e A-VN) · plano
operacional Família A revisado de ~6 sessões para ~5 sessões por visão (§15.2
atualizado). (3) Compatível com D-131 (princípio 5 · transparência mútua sobre
calibração · natural após 2 aplicações bem-sucedidas). (4) Custo baixo ·
benefício alto · nenhum risco estrutural identificado. (5) Usuária declarou
preferência pelo formato · pedido explícito de formalização ao invés de
parquear para 3ª aplicação.

Alternativas consideradas: (a) parquear decisão para após V-V1 · rejeitada por
Usuária pedir formalização agora · (b) revogar retroativamente V-V2/A-V2 como
exceção · rejeitada por evidência empírica positiva (D-151 bem formulada · 301
testes verdes · 10 testes novos de app_v2 · sem regressão em 291 anteriores) ·
(c) manter como convenção Fase 2 inteira sem restrição a Família A · rejeitada
por precaução metodológica (Famílias posteriores podem ter natureza diferente ·
melhor revisitar com dados).

Impacto:
- CONTEXT §15.1 · tabela "Quem faz o quê" · V-VN e A-VN declaradas como "sessão
  combinada · D-155"
- CONTEXT §15.2 · plano operacional revisado · V-VN e A-VN passam de 2 para 1
  sessão · total Família A passa de ~6 para ~5 sessões por visão
- CONTEXT §15.9 · retrospectivas pós-Claude Code · nota sobre convenção Família A
- Instrucoes_do_Projeto.md · tabela tipos de bloco · V-VN e A-VN ganham menção a
  "sessão combinada D-155"
- GLOSSARIO.md · verbetes V-VN e A-VN reformulados com convenção D-155
- D-131 princípio 5 · aplicação natural · calibração aprendida formalizada

Maturação: padrão considerado maduro após Família A completa (V-V1/A-V1 ·
V-V11/A-V11). Revisável se (a) bloco emergir decisão pesada que exija sessão
dedicada para cada lado · (b) Claude Code tiver problemas recorrentes exigindo
iteração longa (pode fazer sentido ter o bloco de retrospectiva em sessão
separada com tempo para absorver resultados).

Referência canônica: V-V2 (22/04/2026 · 1ª aplicação) · A-V2 (23/04/2026 · 2ª
aplicação · esta) · CONTEXT §15.1 e §15.2 e §15.9 · D-131 (complementaridade)


## D-154 — Bloco intermediário RESOL_CASO parqueado como P-V2-Evo-01 · motor V2 atual não pré-detecta casos estruturais
Data: 2026-04-23 · Bloco: A-V2 (retrospectiva) · Status: Fechada · P-V2-Evo-01 aberta

Contexto: Spec V2 §3.7 declara "Bloco intermediário · transição E4 → E5 · motor
detecta inconsistência estrutural" como mecanismo canônico (D-021 · D-029).
Implementação de app_v2.py deixa tela RESOL_CASO no dispatcher mas não é acionada
no fluxo atual. Comentário no código declara: "motor não pré-detecta casos
estruturais · C.3 · não inventar". Investigação em visao_v2.py confirma: motor
trata ResolucaoEstruturalV2 como entrada opcional em config["resolucao_estrutural"],
não como output de detecção pré-execução. Spec §2.4 lista 5 casos estruturais
com comportamento "motor para · abre painel · registra como DECISAO_USUARIO" mas
esse mecanismo não está implementado em visao_v2.py atual.

Decisão: Reconhecer formalmente que a detecção de casos estruturais pré-execução
NÃO está implementada em V2 na primeira rodada da Fase 2. Fluxo atual V2: (a)
casos leves absorvidos silenciosamente (AJUSTE_LEVE via T-DIAG · warnings) · (b)
casos estruturais graves viram bloqueios MBO · Tela 10. A ponte entre motor e
Tela 5 (Spec §3.7) fica parqueada como P-V2-Evo-01 · revisável após VV-V2
confirmar se a lacuna gera ❌. Spec §3.7 ganha nota técnica · mantém-se válida
como roadmap · não como contrato vigente do MVP V2.

Razão: (1) Princípio C.3 · não inventar comportamento sem que contrato suporte.
Claude Code seguiu a orientação correta no prompt ("parar e sinalizar em vez de
fabricar lógica"). (2) VV-V2 vai revelar se a lacuna importa na prática · 4
assertions V2-A01/A02/A03/A04 do YAML não exigem o mecanismo de resolução.
(3) Implementar o fluxo completo agora exigiria alterar contratos da Fundação
(motor precisaria pausar · retomar) · viola C.4 (decisão estrutural de grande
porte em retrospectiva · inadequado). (4) Spec §3.7 continua válida como roadmap.
(5) Princípio de default declarado D-024 aplicado ao escopo · V2 MVP dispensa o
bloco intermediário · V2 maduro revisita.

Opções de implementação quando P-V2-Evo-01 for reaberta (não-decididas agora):
(a) Separar executar_v2 em duas fases: detectar_casos_estruturais(motor_result,
config) → lista pré-detecção + executar_v2(motor_result, config, resolucoes) →
execução com decisões · (b) Emitir exceção tipada CasoEstruturalDetectado que o
app captura e renderiza como Tela 5 · (c) Campo no V2Result tipo caso_pendente
que sinaliza "parar e perguntar". Decisão fica para D-YYY quando P-V2-Evo-01 for
reaberta.

Impacto:
- spec_v2.md §3.7 ganha nota técnica D-154 com "P-V2-Evo-01 · mecanismo
  parqueado · revisável pós-VV-V2"
- visao_v2.py · nenhuma alteração (comportamento atual é correto dado o contrato
  declarado)
- app_v2.py · comentário existente em _dispatch RESOL_CASO continua válido ·
  referenciar D-154 em pós-edição se revisão natural acontecer
- Planilha aba 3 · linha V2 · nota técnica "P-V2-Evo-01 · resolução de casos
  estruturais parqueada"
- Se VV-V2 disparar ❌ relacionado a este tópico · D-154 é revogada por D-YYY e
  mecanismo é implementado

Status de implementação: P-V2-Evo-01 aberta · aguarda VV-V2 para decidir se
revisita ou permanece parqueada.

Referência canônica: spec_v2.md §3.7 (com nota técnica D-154) · visao_v2.py
linha 614 (_etapa_a_preparar_base) · app_v2.py _dispatch RESOL_CASO ·
D-021/D-029 (precedentes originais do mecanismo) · C.3/C.4 (princípios aplicados)


## D-153 — TED renderizado em sidebar global em vez de expander na E3
Data: 2026-04-23 · Bloco: A-V2 (retrospectiva) · Status: Fechada · vigora em Família A desde A-V2

Contexto: Spec V2 §3.5 declarou "Abrir 'Configurações avançadas' (collapsible)"
dentro da Etapa 3. Implementação de app_v2.py renderiza TED em sidebar global
sempre visível (_render_sidebar_ted chamada em main antes do dispatch) · não em
expander interno a E3. Caption em E3 (linha 709 de app_v2.py) declara a mudança
explicitamente para a Usuária: "Configurações avançadas (TED · thresholds
editáveis) disponíveis na barra lateral à esquerda." Justificativa técnica do
Claude Code: "widget-lifecycle churn do AppTest quando widgets com key=
aparecem/somem em transições".

Decisão: Formalizar como refinamento da regra TED (C.D2): TED é renderizado em
sidebar global para todos os apps da Fase 2 · não em expander interno a etapa
específica. Convenção Família A inteira (apps V1 e V11 quando implementados
seguem o mesmo padrão). Spec V2 §3.5 recebe nota técnica D-153 (paralelo a
D-151 em §1.2). Specs S-V1 e S-V11 (a produzir) declaram sidebar global desde
o início. app_v2.py não precisa ajuste · já está correto.

Razão: (1) Divergência é de LOCALIZAÇÃO · não de contrato. Os 4 requisitos da
regra TED (C.D2) são preservados integralmente: defaults declarados (sidebar
mostra defaults) · editável por camada (disponível desde E1) · persistido em
config_usada (passa por _construir_config) · sem defaults silenciosos no motor.
(2) Widget-lifecycle em Streamlit é mecânica real · widgets com key= que
aparecem/somem durante transições geram re-inicialização · 10 testes AppTest
validaram empiricamente que sidebar resolve. (3) Sidebar global dá MAIS
visibilidade ao TED, não menos · contribui para princípio C.5 (defaults
visíveis sempre). (4) Padrão de correção absorvida com D-XXX quando afeta
visões futuras — precedente F-EXP D-143 · D-151 em V-V2 · consistência
metodológica. (5) Princípio C.4 · decisão estrutural vira D-XXX mesmo sendo
técnica pura sem impacto de negócio.

Impacto:
- spec_v2.md §3.5 ganha nota técnica D-153 em Configurações avançadas
- CONTEXT §9 Camada C · C.D2 (TED) · nota "rendering em sidebar global · D-153"
- CONTEXT §15.3 · convenções de Spec S-VN · TED declarado em sidebar global
- Instrucoes_do_Projeto.md · "Não fazer" · item sobre não renderizar TED em
  expander interno a etapa
- Próximas Specs (S-V1, S-V11) declaram sidebar global desde a produção
- app_v2.py · nenhuma alteração necessária · implementação já está correta

Referência canônica: app_v2.py linha 304 (_render_sidebar_ted) · app_v2.py
linha 707-712 (caption em E3 apontando para sidebar) · spec_v2.md §3.5 (nota
técnica D-153) · CONTEXT §9 C.D2 (regra TED preservada) · D-143/D-151
(precedentes de correções absorvidas como D-XXX)


## D-152 — streamlit.testing.v1.AppTest como convenção de testes de app da Família A
Data: 2026-04-23 · Bloco: A-V2 (retrospectiva) · Status: Fechada · vigora em Família A desde A-V2

Contexto: Sessão A-V2 é a primeira aplicação de app Streamlit da Fase 2.
Estratégia β (streamlit.testing.v1.AppTest) foi proposta como decisão técnica
pura pré-prompt (confirmada pela Usuária antes da produção do prompt A-V2).
Agora validada empiricamente com 10 testes verdes cobrindo startup · 2 fluxos
felizes (POR_LINHAS e POR_COLUNAS) · P4 bloqueio · gate B.4 · invalidação
cascata · TED persistido · Tela ERRO · ordenação inteligente Modo 4. Suite
total passou de 291/291 (pós-V-V2) para 301/301 (pós-A-V2) · crescimento
natural sem regressão.

Decisão: Adotar streamlit.testing.v1.AppTest como convenção de testes de app da
Família A inteira (A-V2 · A-V1 · A-V11). Testes mínimos por app: startup · 2
fluxos felizes (cobrindo variantes estruturais da visão) · 1 bloqueio MBO
específico · gate B.4 validado empiricamente · invalidação cascata · TED
persistido · ≥ 1 assertion mecânica do casos_esperados.yaml · Tela ERRO · ≥ 8
testes totais. Precedente A-V2: 10 testes (acima do mínimo). Revisável após
Família A validada · pode precisar complementar com Playwright/E2E se cenário
de browser real emergir (decisão via D-YYY se houver).

Razão: (1) Stdlib oficial Streamlit desde versão 1.28 · zero dependência nova ·
compatível com pyproject.toml existente. (2) Determinístico (C.1) · compatível
com pytest existente · roda na mesma suite · tempo total compatível com a
Fundação (4.89s para 232 testes · +10 testes em tempo desprezível). (3) Cobre
widgets · estados · transições · suficiente para o nível de asserção que faz
sentido em produto solo. (4) Precedente empírico da convenção D-148 aplicado ao
método — padrão decidido com base em evidência de uma aplicação. (5) Alternativas
Playwright/Selenium descartadas como convenção default · overkill para 11 telas
· excesso de manutenção · podem ser acionadas caso-a-caso se cenário específico
exigir.

Impacto:
- CONTEXT §15.3 · convenções de Spec S-VN · testes de app declarados como
  streamlit.testing.v1.AppTest
- Instrucoes_do_Projeto.md · "Não fazer" · item sobre não usar Playwright/Selenium
  sem D-YYY
- GLOSSARIO.md · verbete A-VN atualizado com referência a D-152
- Prompt A-V1 (futuro) herda estrutura de 9 testes mínimos do prompt A-V2
- app_v1.py e app_v11.py (futuros) seguirão mesmo padrão
- Suite pytest cresce naturalmente · meta: +10 testes por app_vN · alvo
  V2+V1+V11 = 330 testes · viável dentro de < 10s

Referência canônica: src/testes/test_app_v2.py (10 testes verdes) · prompt
A-V2 (estratégia β declarada) · Spec V2 (§3.9 checklist derivado que vira
assertion mecânica em 1 teste) · CONTEXT §15.3 (convenções)

## D-151 — Semântica de `campo_analisado` em POR_COLUNAS vs. POR_LINHAS · refinamento da Spec V2 §1.2 e §2.5
Data: 2026-04-22 · Bloco: V-V2 · Status: Fechada
Contexto: Durante implementação de visao_v2.py em sessão Claude Code, surgiu
ambiguidade estrutural latente na Spec V2: o `campo_analisado` (Spec §1.2)
tem semânticas diferentes nas duas estruturas de entrada · em POR_LINHAS é
nome de coluna real do DataFrame (ex: `Vendas` na aba `vendas_padrao`) · em
POR_COLUNAS é nome conceitual do campo que está sendo comparado (ex:
`Receita` quando origem_rotulo_tecnico=`Receita_Orcado` e
comparado_rotulo_tecnico=`Receita_Realizado`). A Spec §2.5 declarou
`B-V2-CAMPO-100-NULO` quando "campo analisado tem 100% de nulos em um lado"
e `B-V2-ESTRUTURA-INVALIDA` quando "campo numérico esperado" não disponível
sem distinguir o que é "o campo" em POR_COLUNAS · onde o campo conceitual
não corresponde a uma coluna real verificável por `campo not in df.columns`.

Decisão: Em POR_LINHAS, `campo_analisado` é coluna real e
`B-V2-ESTRUTURA-INVALIDA` valida ausência via `campo not in df.columns`. Em
POR_COLUNAS, `campo_analisado` é nome conceitual (rótulo apresentado no
Resumo Executivo) e a validação de existência se aplica aos dois rótulos
técnicos · `origem_rotulo_tecnico not in df.columns` e
`comparado_rotulo_tecnico not in df.columns` (já cobertos por outros
bloqueios). `B-V2-CAMPO-100-NULO` em POR_COLUNAS valida nulos sobre as duas
colunas técnicas (origem e comparado) · não sobre o campo conceitual.

Razão: (1) Distinção semântica não foi declarada explicitamente na Spec por
omissão · não por intenção contrária. (2) Tratar uniformemente as duas
estruturas levaria a falsos bloqueios em POR_COLUNAS legítimos (campo
conceitual nunca está como coluna do df). (3) Implementação do Claude Code
durante V-V2 convergiu para esta interpretação naturalmente · 291/291 testes
verdes confirmam estabilidade do comportamento. (4) Precedente F-EXP D-143/
D-144 e F-BASE D-145/D-146 manda formalizar quando ambiguidade estrutural
emerge da implementação · esta é a primeira aplicação na Fase 2 · padrão
preservado.

Impacto:
- spec_v2.md §1.2 ganha nota explicativa em ComparacaoV2.campo_analisado
  esclarecendo as duas semânticas (a aplicar no kit V-V2)
- spec_v2.md §2.5 · B-V2-CAMPO-100-NULO e B-V2-ESTRUTURA-INVALIDA ganham
  nota técnica sobre comportamento por estrutura de entrada
- Visões futuras da Família A (V1 e V11) herdam consideração análoga
  quando relevante · V1 opera em base DUAL com nomes por lado declarados
  (D-018 · §F.1 spec_fundacao) · V11 idem · semântica dual já é nativa
  · D-151 não exige refino antecipado para essas visões · resolver na S-V1
  e S-V11 se relevante
- Princípio C.3 reforçado · ambiguidade estrutural latente promovida a
  D-XXX em vez de absorvida silenciosamente
- Próximas Specs de visão (S-V1 a S-V11) ganham consideração explícita de
  semânticas de campo por estrutura de entrada quando aplicável

Referência canônica: spec_v2.md §1.2 e §2.5 (com nota técnica) · visao_v2.py
_etapa_a_preparar_base() linha 614 · D-143/D-144/D-145/D-146 (precedentes
metodológicos)

### D-150 — Seção "Horizontes Futuros" na aba 1 da planilha · 19 horizontes em 3 zonas · atualização manual pela Usuária
**Data:** 2026-04-21 · **Bloco:** ALINHA-Fase-1→Fase-2 · sub-bloco γ · **Status:** Fechada · vigora imediatamente no kit δ
**Contexto:** Áudios da Usuária em β desta sessão (terceira e quarta mensagens) expressaram necessidade de visibilidade macro do projeto além da fase ativa · "pontos macros para ter visão do todo". A planilha tinha (aba 1 · D-132) dashboard da fase ativa com barras de progresso · bom para fase em curso · não atendia necessidade de ver **para onde o projeto vai no todo · incluindo fases ainda não endereçadas pelo método** (exemplos do áudio · decisão de linguagem de produção · fase de produtização · identidade visual ativada · lançamento). Primeira proposta (Roadmap Macro com barras de progresso por marco) recalibrada após áudio da Usuária · (a) preenchimento manual pela Usuária exige estrutura simples · barras com recálculo seriam fricção operacional · (b) macro deve ser qualitativo · não quantitativo · "um norte de quando as coisas vão acontecer". Quarta mensagem aprovou lista completa de 19 horizontes cobrindo do hoje ao lançamento público.
**Decisão:** Aba 1 reestruturada como **"Onde estou no todo"** · contém (ordem vertical): Cabeçalho do projeto (fase ativa + última atualização) · Próximo Passo Operacional (bloco destacado verde) · **Seção "Horizontes futuros · o que ainda vem"** (tabela de 3 colunas · 19 linhas em 3 zonas visuais com cores) · Vocabulário de status. Horizontes em 3 zonas:

**Zona 1 · Construção do produto** (11 linhas · azul claro): Família A V2·V1·V11 validadas → Bloco IA-Família-A → Família C V4·V10 → Bloco IA-Meta → Família B V3·V8 → Família D V7·V9 → Família E V5·V6 → Módulo 1 concluído → Módulo 2 DCVs → Módulo 2 Fundação+Operações → Módulo 2 concluído.

**Zona 2 · Produtização** (4 linhas · amarelo claro): Decisão de linguagem de produção → Frente A Identidade Visual ativada → Validação de Produto com bases reais → Arquitetura de produtização.

**Zona 3 · Go-to-market** (4 linhas · rosa claro): Estratégia comercial/posicionamento/precificação → Beta fechado com clientes piloto → Ajustes pós-beta → Lançamento público do TabloFlow.

Vocabulário canônico de status: ▶ Próximo · ⏸ Aguardando · ⏸ Parqueada · ⏸ Não iniciado · ⚠️ Em andamento · ✅ Concluído. Coluna "Quando entra" em linguagem declarativa sem datas absolutas. Atualização manual pela Usuária · ~10s por sessão · mudança apenas do status da coluna 3 quando um horizonte se ativa ou conclui.

Reestruturação integral da planilha em 5 abas com papéis explícitos: (1) Onde estou no todo · (2) Painel da fase ativa · (3) Detalhe técnico das visões · (4) Fase 0 concluída (arquivo) · (5) Fase 1 concluída (arquivo). Aba 2 materializa dashboard da Fase 2 com 11 visões × 5 quadrados cada (Spec+Wireframe · Base · visão.py · app · Validação Visual) · marcadores ⬜/⚠️/✅ · totalizadores por família e fase. Aba 3 materializa referência técnica · consulta pontual · raramente editada. **Frente nova "Validação de Produto com bases reais de cliente"** formalizada como parqueada · inicia após Família A validada · distinta de Validação Visual (mecânica · Fase 2) · valida adequação a cenário real.
**Razão:** (1) Princípio 2 de D-131 (acompanhamento visual primário) estendido de escala fase-a-fase para escala macro-do-projeto · Usuária abre planilha e em 3 seções (Próximo Passo · Horizontes · fase ativa) tem visão temporal completa. (2) Formato qualitativo · tabular · sem barras · compatível com preenchimento manual sem atrito. (3) 19 horizontes cobrem construção + produtização + go-to-market · lacuna anterior (fases não-endereçadas pelo método) fechada. (4) Validação de Produto como frente distinta preserva clareza de B.4 (Validação Visual valida mecânica) sem misturar com validação de adequação real (que tem natureza diferente · bases de cliente real · decisões de negócio). (5) Status canônico alinhado com vocabulário existente · zero termo novo. (6) Reestruturação em 5 abas com papéis explícitos responde a nota da Usuária "que eu não sou técnica saiba exatamente onde estou" · cada aba tem função única e linguagem de uso · não técnica.
**Impacto:**
- Planilha `TabloFlow_Estado_do_Projeto.xlsx` reestruturada integralmente · 5 abas com nomes explícitos · entregue como arquivo completo no kit desta sessão (item 5 do D-033 · exceção da regra de "edições rotineiras" porque a mudança é estrutural)
- Dashboard da Fase 1 antigo (seção "Progresso da Fase 1") migra para aba 5 como arquivo histórico
- CONTEXT.md §5 Fontes de verdade · referência à planilha atualizada mencionando 5 abas com papéis explícitos e frente nova "Validação de Produto"
- CONTEXT.md §14 princípio 2 reescrito · dashboard da fase ativa vive na aba 2 · Horizontes Futuros na aba 1
- CONTEXT.md §15 novo formaliza processo da Fase 2 incluindo convenções de acompanhamento operacional (§15.10)
- Instrucoes_do_Projeto.md "O que fica no painel" atualizado · "Fechar conversa com kit" ganha nota sobre mudança estrutural da planilha
- Cada sessão da Fase 2 dispara edições rotineiras: mudança de quadrado na aba 2 · atualização de "Próximo Passo Operacional" na aba 1 · mudança eventual de status de Horizonte · instruções no kit D-033
- Ao entrar na Fase 3 (M2 · IA-Meta · produtização) Usuária pode pedir "nova análise da planilha" · Arquiteto repropõe reorganização mantendo filosofia de papéis explícitos
**Referência canônica:** áudios da Usuária em β desta sessão (21/04/2026) · D-131 princípio 2 (acompanhamento visual primário) · D-132 (dashboard visual da Fase 1 · absorvido pela reestruturação) · CONTEXT §5 · §14 · §15.10

---

### D-149 — Recorte cliente-friendly `base_vN_cliente.xlsx` + wireframe visual HTML · convenções operacionais da Fase 2
**Data:** 2026-04-21 · **Bloco:** ALINHA-Fase-1→Fase-2 · sub-bloco γ · **Status:** Fechada · vigora a partir de S-V2
**Contexto:** Áudio da Usuária em β desta sessão (segunda mensagem) trouxe duas demandas não antecipadas nas convenções iniciais: **(a)** Arquivo único específico da visão para Validação Visual · "como se fosse o cliente ali validando" · carregar `base_fundacao.xlsx` com 14 abas no `app_vN.py` para validar 1 visão gera fricção · cenário realista de uso é upload de arquivo menor contendo só a(s) aba(s) da visão; **(b)** Validação antecipada de tela · wireframe funcional textual da Spec é suficiente para contrato lógico · mas Usuária declarou precisar ver visualmente o fluxo antes de aprovar · especialmente em S-V2 como primeira visão · princípio B.2 exige aprovação explícita do wireframe antes do código iniciar · mas forma da validação visual do wireframe não estava declarada. Ambas as demandas são operacionais · não alteram contrato da Fundação · consumidas 11 vezes na Fase 2.
**Decisão:** Dois mecanismos operacionais canônicos na Fase 2:

**1 · `base_vN_cliente.xlsx` · recorte cliente-friendly por visão:**
- Para cada visão N da Fase 2, gerar arquivo `/bases/base_vN_cliente.xlsx` contendo apenas a(s) aba(s) declarada(s) como consumida(s) em D-147
- Zero geração de conteúdo novo · zero risco de divergência · reempacotamento mecânico das abas correspondentes da `base_fundacao.xlsx` (ou de `base_vN.xlsx` quando B-VN existir)
- Arquivo usado pela Usuária na Validação Visual (simula upload de cliente real)
- `base_fundacao.xlsx` permanece fonte única de verdade para testes automatizados (F-MOT/F-TRANS/F-EXP/F-BASE) e para o `casos_esperados.yaml`
- Script de geração: `/src/geradores/gerar_base_cliente.py` · criado em sub-tarefa de S-V2 (primeira aplicação) · reutilizável para V1 · V11 · demais visões

**2 · Wireframe visual em HTML · convenção de Spec S-VN (obrigatório Família A):**
- Cada Spec S-VN acompanha artefato complementar `/specs/wireframe_vN.html` · HTML estático mínimo (1 arquivo · sem build · abre em qualquer browser)
- Representa os estados e transições do wireframe funcional textual (Seção §3 da Spec) em formato visual básico · tela por etapa · botões nomeados · microcopy visível · transições anotadas
- Neutro em identidade visual (Frente A parqueada · D-015 Camada B) · foco em **fluxo + estrutura de tela**, não em estética
- Aprovação da Usuária acontece simultânea à aprovação da Spec textual · dupla aprovação B.2 preservada e reforçada
- Caso a identidade visual (Frente A) seja ativada depois, o HTML fica obsoleto cosmeticamente mas o fluxo funcional permanece válido e não precisa ser regerado
- **Obrigatório em S-V2, S-V1, S-V11** (Família A · estabelece padrão visual) · **opcional a partir de S-V3** · avaliado caso a caso se HTML agrega valor real · default declarado pós-Família A é manter HTML para visões de fluxo novo ou visualmente complexo · dispensável para visões cuja Spec textual já é suficientemente clara

**Razão:** (1) Base cliente-friendly reduz fricção de validação sem custo real · recorte mecânico da base mestre · zero duplicação de verdade. (2) Wireframe visual HTML responde a demanda legítima de validação antecipada de tela · formato escolhido (HTML estático) minimiza dependência externa · vive no painel · renderiza no Projects. (3) Alternativa Figma descartada como obrigatório · exigiria ferramenta externa fora do fluxo canônico · Figma Make permanece como referência de identidade visual parqueada (D-015 Camada B) · Usuária pode usar Figma em paralelo se preferir (Opção α da proposta original). (4) Obrigatoriedade só em Família A porque é o momento de calibrar o padrão visual · demais visões decidem caso a caso se HTML agrega valor real (princípio de default declarado D-024 adaptado).
**Impacto:**
- CONTEXT §3 Fase 2 · cláusula de Spec S-VN referencia D-149 (wireframe HTML) e D-147 (base consumida)
- CONTEXT §3 Fase 2 · cláusula de Validação Visual referencia `base_vN_cliente.xlsx` como arquivo de entrada canônico
- CONTEXT §5 Fontes de verdade · 2 linhas novas (wireframes HTML · base_vN_cliente.xlsx)
- CONTEXT §9 Camada B · princípio B.2 reforçado com referência a HTML Família A · princípio B.4 reforçado com referência a `base_vN_cliente.xlsx`
- CONTEXT §15.5 formaliza recorte cliente-friendly · §15.6 formaliza wireframe visual HTML
- Instrucoes_do_Projeto.md "O que fica no painel" · adições · Instrucoes "Não fazer" · item sobre não modificar `base_vN_cliente.xlsx` diretamente
- `/bases/base_v2_cliente.xlsx` · `/bases/base_v1_cliente.xlsx` · `/bases/base_v11_cliente.xlsx` gerados no início da Fase 2 da Família A
- Script de geração `/src/geradores/gerar_base_cliente.py` · produzido em sub-tarefa da sessão de S-V2 (primeira aplicação)
- `/specs/wireframe_v2.html` acompanha `/specs/spec_v2.md` · similar para V1 e V11
- Planilha aba 2 · coluna "Base" absorve `base_fundacao` ou `base_vN.xlsx` · mas na prática a Validação Visual usa o cliente

**Nota de revisão:** vigora a partir de S-V2 (primeira aplicação). Ajustes pós-V2 tratados como refinamento da decisão, não como revogação. Particularmente · obrigatoriedade do wireframe HTML apenas em Família A é sujeita a reavaliação após ciclo completo de V2 (se Usuária sinalizar que texto da Spec basta · pode ser descontinuado para visões posteriores via D-YYY).

**Referência canônica:** áudio da Usuária em β desta sessão (21/04/2026) · CONTEXT §3 Fase 2 · §15.5 · §15.6 · princípio B.2 (dupla aprovação contrato+wireframe) · D-015 (Camadas Figma Make · A vinculante / B não-vinculante) · D-140 (`base_fundacao.xlsx` como fonte única) · D-147 (base consumida por visão)

---

### D-148 — Mapa de derivação do checklist de Validação Visual · 5 templates canônicos + estrutura + convenções operacionais
**Data:** 2026-04-21 · **Bloco:** ALINHA-Fase-1→Fase-2 · sub-bloco γ · **Status:** Fechada · vigora a partir de S-V2
**Contexto:** D-141 (20/04/2026) declarou que o checklist de Validação Visual da Fase 2 é derivado mecanicamente das assertions de `casos_esperados.yaml` por visão (Ponto 3 de consumo do YAML). Princípio 4 de D-131 exige que a Usuária não leia código · apenas marque checklist derivado. CONTEXT §3 Fase 2 e princípio B.4 exigem Validação Visual como gate final de aprovação. Mas a **regra de derivação exata** não foi materializada em D-141 · ficou para a Fase 2 operacionalizar quando chegasse a hora. Em β.4 desta sessão a regra foi consolidada · 5 tipos canônicos de assertion (§J.3 da spec_fundacao) mapeiam para 5 templates de pergunta binária · checklist vira seção dedicada do wireframe funcional em cada Spec + checkbox list visível no `app_vN.py` antes da exportação Excel.
**Decisão:** Ponto 3 de consumo de `casos_esperados.yaml` materializado como 4 elementos canônicos:

**1 · 5 templates canônicos de pergunta · lista fechada** (1:1 com os 5 tipos canônicos de assertion de §J.3):

- `contagem_exata` → "O resultado mostra exatamente {esperado.valor} {entidade} em {coluna|aba|agrupador}?"
- `contagem_categoria` → "O resultado mostra entre {esperado.min} e {esperado.max} {entidade} em {coluna|aba}?" (variante pct: "entre {min_pct}% e {max_pct}%")
- `warning_presente` → "O warning `{warning_code}` aparece no Diagnóstico com {min}–{max} ocorrência(s)?"
- `estrutura_saida` → "O Excel tem Resumo Executivo com {resumo_blocos} blocos e aba Coração Visual nomeada '{coracao_visual}'?" (+ outros pares chave/valor presentes em `esperado`)
- `bloqueio_emitido` → "Ao rodar a visão, o BloqueioOperacional de código `{bloqueio_codigo}` foi emitido conforme esperado?"

Tipos parametrizados (§J.3) consumidos com templates derivados · `inferencia_boolean` · `inferencia_subtipo_id` · `determinismo_seed`. Extensão do conjunto fechado de 5 templates exige D-YYY nova.

**2 · Estrutura do checklist · 2 lugares canônicos:**
- (a) Seção §3.x do wireframe funcional da Spec S-VN · aprovável pela Usuária junto do wireframe · dupla aprovação contrato+wireframe preservada (B.2)
- (b) Interface do `app_vN.py` como checkbox list visível antes da exportação Excel · paridade wireframe↔app

**3 · Convenções operacionais:**
- Arquiteto produz o checklist durante S-VN (não Claude Code · não Usuária)
- Derivação 1:1 entre assertions do YAML e itens do checklist
- Item não-coberto por assertion não pode ser adicionado ad-hoc ao checklist · deve virar assertion nova no YAML + regenerar (integridade de D-141 ponto 3)
- Mudança substancial em assertion durante Fase 2 vira kit D-033 simultâneo em Spec + app + YAML
- Resultado da Validação Visual binário por item: ✅ (confere) ou ❌ (não confere). Qualquer ❌ dispara investigação do Arquiteto (bug de código · lacuna de Spec · interpretação divergente · M4 da D-131).

**4 · Formato canônico do checklist na Spec** · seção §3.x da Spec S-VN · estrutura:
```
## Checklist de Validação Visual V{N}

Protocolo: Usuária carrega {base consumida · D-147} no app_vN.py,
processa a(s) aba(s) declarada(s), marca cada item como ✅ ou ❌.
Derivado mecanicamente de casos_esperados.yaml bloco visoes.V{N}.

[ ] Item 1 · {template aplicado a assertion 1}
[ ] Item 2 · {template aplicado a assertion 2}
...
[ ] Item N · {template aplicado a assertion N}

Aprovação final: todos ✅ → visão aprovada · Validação Visual
registrada na aba 2 da planilha (5º quadrado ✅). Qualquer ❌
→ Arquiteto investiga em sessão dedicada.
```

**Exemplo aplicado a V2** (derivação das 4 assertions V2-A01 a V2-A04): 4 assertions → 4 itens de checklist. Demonstração integral em β.4.3 da sessão ALINHA-Fase-1→Fase-2 · preservada como referência.

**Razão:** (1) D-141 ponto 3 é o mecanismo operacional de princípio 4 de D-131 e de B.4 · regra de derivação tem de ser explícita para Validação Visual acontecer sem ambiguidade. (2) Templates canônicos fechados garantem uniformidade entre as 11 visões · Usuária lê sempre a mesma estrutura de pergunta. (3) Derivação 1:1 preserva o YAML como fonte única · nada pode ser validado visualmente sem estar no gabarito. (4) Obrigar item ad-hoc a virar assertion nova reforça C.2 (nada silencioso · tudo que importa ao motor também importa ao gabarito). (5) Consumido 11 vezes · custoso de redescobrir ou deixar informal.
**Impacto:**
- CONTEXT §3 Fase 2 · seção "Validação Visual" referencia D-148 como regra de derivação
- CONTEXT §15.7 formaliza o checklist de Validação Visual derivado mecanicamente · 5 templates · estrutura · convenções
- CONTEXT §14 princípio 4 reescrito · mencionando D-148 como materialização do mecanismo
- Instrucoes_do_Projeto.md · "gerar Spec de visão" menciona Seção §3.x Checklist como entregável obrigatório · "Não fazer" ganha item sobre não adicionar item ad-hoc ao checklist
- Cada Spec S-VN produz a seção §3.x aplicando os 5 templates
- Cada `app_vN.py` implementa o checkbox list com os itens derivados
- Quando `casos_esperados.yaml` muda durante Fase 2 · kit D-033 regenera simultaneamente Spec · app · YAML
- Extensão do conjunto fechado de 5 templates (novo tipo de assertion + novo template) exige D-YYY

**Nota de revisão:** vigora a partir de S-V2 (primeira aplicação). Ajustes pós-V2 tratados como refinamento da decisão, não como revogação.

**Referência canônica:** β.4 desta sessão · `spec_fundacao.md` §J.3 · §J.4 · D-141 · D-131 princípio 4 · CONTEXT §3 Fase 2 · §15.7 · princípio B.4

---

### D-147 — Critério decisório "base específica da visão" vs. "consumir base_fundacao.xlsx" · 3 perguntas + default declarado
**Data:** 2026-04-21 · **Bloco:** ALINHA-Fase-1→Fase-2 · sub-bloco γ · **Status:** Fechada · vigora a partir de S-V2
**Contexto:** Com a Fundação concluída (Fase 1 · 21/04/2026 · `base_fundacao.xlsx` entregue com 14 abas cobrindo cenários de todas as 11 visões · §I.13 mapeia aba→visão), emerge questão operacional da Fase 2 · cada visão pode consumir a base mestre diretamente ou precisa de base específica B-VN dedicada? CONTEXT §3 Fase 2 lista B-VN como bloco canônico da sequência de 5 artefatos por visão · mas não declarava critério de decisão entre "B-VN é dispensável" e "B-VN é necessário". Princípio B.3 exige ≥50 linhas com gabarito auditado · `base_fundacao.xlsx` já cumpre. A pergunta concreta é quando a cobertura/volume/independência da base mestre bastam para Validação Visual e quando a visão precisa de complemento. Varredura na Família A (β.3.2 desta sessão) evidenciou que V2·V1·V11 têm cobertura suficiente em `base_fundacao.xlsx` (cenários consumidos · volume · estabilidade) · mas o critério precisa ser explícito para as 11 visões · senão cada Spec reabre a discussão.
**Decisão:** Cada Spec S-VN declara explicitamente qual é a base consumida pela visão aplicando o critério de 3 perguntas:

**Pergunta 1 · Cobertura de cenários** · as assertions de `casos_esperados.yaml` do bloco `visoes:V{N}` cobrem os casos-limite do DCV-VN? Se sim, não há lacuna; se não, listar casos não-cobertos e avaliar Pergunta 2.

**Pergunta 2 · Volume para Validação Visual** · o volume das abas consumidas é confortável para inspeção humana (≥50 linhas · permite observar dispersão, padrões, outliers)? Se sim, base mestre suficiente; se não, gerar B-VN.

**Pergunta 3 · Independência de evolução** · a Fase 2 pode precisar modificar a base dessa visão no futuro sem afetar a base mestre compartilhada? Se sim (cenário volátil V-específico), B-VN útil; se não, base mestre suficiente.

**Default declarado:** se todas as 3 respostas forem "base mestre suficiente", B-VN é dispensado · `visao_vN.py` consome `base_fundacao.xlsx` diretamente · Spec declara: "Base consumida: `base_fundacao.xlsx` · abas: {lista}". Se qualquer resposta exigir base complementar, B-VN é bloco dedicado · produz `base_vN.xlsx` em `/bases/` · Spec declara: "Base específica: `base_vN.xlsx` · cobertura complementar: {lista}".

**Aplicação preliminar Família A:** V2 (`vendas_padrao` 120 linhas · 4 assertions cobrem Modo 4/Ausente/NULO_MEDIDA/estrutura) · V1 (par DUAL 215 linhas · 6 assertions cobrem match exato/divergência/só-em-lado/ambiguidade/sinônimo) · V11 (`cadastral_fuzzy` 80 + par DUAL · assertions cobrem zona cinza/rejeitado/CNPJ misto/token-chave) — **todas as 3 têm B-VN dispensado** · consomem `base_fundacao.xlsx` diretamente.

**Razão:** (1) Fase 2 precisa de regra de decisão explícita para não reabrir a discussão em cada visão · consumo é 11 vezes. (2) `base_fundacao.xlsx` foi desenhada (§I) com cobertura multi-visão explícita · desperdiçar esse investimento gerando B-VN redundantes contraria CPCO (C.D1 aplicado ao próprio método). (3) Princípio de default declarado D-024 aplicado ao método · default é "consumir base mestre" porque foi para isso que ela foi construída · B-VN vira exceção declarada. (4) Custo de B-VN desnecessário · sessão adicional sem ganho · risco de divergência entre base específica e mestre (duas verdades). (5) Flexibilidade preservada · B-VN pode ser adicionado retroativamente se Validação Visual revelar lacuna.
**Impacto:**
- CONTEXT §3 Fase 2 · cláusula B-VN reescrita explicitando que B-VN é condicional ao critério de D-147
- CONTEXT §15.4 formaliza o critério de 3 perguntas + default declarado + aplicação Família A
- CONTEXT §9 Camada B · princípio B.3 reforçado com menção a D-147
- Instrucoes_do_Projeto.md · seção "gerar base de visão" atualizada · linguagem "discrimino entre consumir base_fundacao e gerar B-VN"
- Cada Spec S-VN declara resposta às 3 perguntas + base consumida (seção 0 · cabeçalho operacional)
- Planilha aba 2 · coluna "Base" recebe "base_fundacao" ou "base_vN.xlsx" como valor canônico
- Princípio 4 de D-131 preservado · Validação Visual usa o checklist derivado do YAML (D-148) independentemente da base consumida

**Nota de revisão:** vigora a partir de S-V2 (primeira aplicação). Ajustes pós-V2 tratados como refinamento da decisão, não como revogação.

**Referência canônica:** β.3 desta sessão · CONTEXT §3 Fase 2 · §15.4 · `spec_fundacao.md` §I.13 · D-140 (base_fundacao) · D-141 (casos_esperados) · D-024 (default declarado · derivado informal)

### D-146 — Enum canônico de tipo_estrutural no casos_esperados.yaml · correção de esqueleto §J.2
Data: 2026-04-21 · Bloco: retrospectiva F-BASE · Status: Fechada

Contexto: §J.2 da spec_fundacao.md declarava esqueleto de
casos_esperados.yaml com linhas 1955 (V11-A02) e 1972 (MU-A02) usando
`tipo_estrutural: "ID"`. Essa formulação contradizia duas declarações
canônicas da mesma spec:
(1) §A linha 126 · ColumnMeta declara tipo_estrutural como
    Literal["CATEGORICO_ELEGIVEL", "NUMERICO_CONTINUO", "TEMPORAL",
    "BOOLEANO", "VAZIO_OU_AMBIGUO"] · enum fechado de 5 valores ·
    "ID" não faz parte do conjunto;
(2) §C linha 409-410 · classificar_tipo_estrutural retorna
    "CATEGORICO_ELEGIVEL" explicitamente quando subtipo_id_detectado
    é True · regra canônica "ID é categórico apesar de int".

Ao produzir casos_esperados.yaml em F-BASE (21/04/2026), o Claude Code
identificou a contradição implicitamente e produziu o YAML coerente
com §A/§C · assertion V11-A02 entregue como `{tipo_estrutural:
"CATEGORICO_ELEGIVEL", subtipo_id_detectado: true}` · assertions
MU-A02/MU-A04 idem. A coerência foi ratificada pela suite pytest
7/7 verde na regressão de F-BASE. Ambiguidade latente do esqueleto
§J.2 revelada na implementação · mesmo precedente de D-143.

Decisão: formaliza-se que o campo `tipo_estrutural` em qualquer
assertion do casos_esperados.yaml SEMPRE usa um dos 5 valores do
enum canônico declarado em §A linha 126:
 · CATEGORICO_ELEGIVEL
 · NUMERICO_CONTINUO
 · TEMPORAL
 · BOOLEANO
 · VAZIO_OU_AMBIGUO

Representação de ID segue a regra de §C: `tipo_estrutural:
"CATEGORICO_ELEGIVEL"` + `subtipo_id_detectado: true`. Formulações
anteriores do esqueleto §J.2 ficam obsoletas · o esqueleto corrigido
nesta sessão é a referência canônica. Extensão do enum (novo valor)
exige D-YYY adicional.

Razão:
(1) Enum canônico de §A é a fonte de verdade do sistema de tipos ·
qualquer artefato derivado (como o casos_esperados.yaml) deve refletir
esse enum sem invenção de valores paralelos.
(2) A regra "ID é categórico apesar de int" é explícita em §C ·
introduzir "ID" como valor de tipo_estrutural teria criado enum
paralelo com semântica conflitante (tipo_estrutural vs.
subtipo_id_detectado passariam a carregar a mesma informação em
campos diferentes).
(3) O Claude Code resolveu a ambiguidade sem consultar porque a
resolução correta era unívoca · exatamente o caso previsto por
princípio C.3 quando o contrato declarado em outro lugar da mesma
spec permite inferir o comportamento correto. Formalização aqui
evita que futura spec de visão (Fase 2) copie o esqueleto §J.2
e reintroduza o mesmo valor inválido.
(4) Decisão tem escopo limitado ao artefato casos_esperados.yaml
e a quaisquer YAMLs derivados (checklist de Validação Visual da
Fase 2 · D-141 ponto 3) · não afeta §A nem §C que já estavam
corretos.

Impacto: spec_fundacao.md §J.2 atualizada · linhas do esqueleto de
V11-A02 e MU-A02 corrigidas · nota formal de D-146 adicionada ao
final do esqueleto §J.2. casos_esperados.yaml em /bases/ permanece
como está · já coerente. Nenhuma alteração em código de motor_base
ou classificar_tipo_estrutural. Testes existentes continuam verdes
(232/232 em 4.89s).

Referência canônica: spec_fundacao.md §J.2 (esqueleto corrigido +
nota de D-146 ao final) · CONTEXT.md cabeçalho (breve menção) ·
Instrucoes_do_Projeto.md seção "O que NÃO fazer" (novo item sobre
não usar tipo_estrutural: "ID").

### D-145 — Tolerância amostral em tamanhos declarados em §H.5
Data: 2026-04-21 · Bloco: retrospectiva F-BASE · Status: Fechada

Contexto: spec_fundacao.md §H.5 declara inventário canônico de 14
abas com coluna "Tamanho" especificando número fechado de linhas
por aba (ex: vendas_padrao 120 · operacao_cruzamento 180 ·
operacao_perfil_grupo 150) · total declarado como "~2.063 linhas
agregadas" com til literal. D-140 cristaliza 4 invariantes de
reprodutibilidade: (1) arquivo único · (2) inventário 14 abas ·
(3) SEED=42 · (4) nomes canônicos.

F-BASE (21/04/2026) entregou base_fundacao.xlsx com 14 abas
canônicas · SEED=42 · inventário fiel · 12 de 14 abas com tamanho
exato (contrato respeitado) · duas divergências: operacao_cruzamento
175 linhas (-5 · -2.8%) e operacao_perfil_grupo 148 linhas (-2 ·
-1.3%). Total agregado 1853 vs ~2063 declarado (-10%). Claude Code
documentou divergências como "referência aproximada" no comentário
do YAML.

Ambiguidade latente revelada: o til aplicado ao total sugere
tolerância no agregado, mas os valores por aba em coluna "Tamanho"
eram apresentados como números fechados. A questão estrutural: um
número por aba em §H.5 é contrato fechado (imutável sem D-YYY ·
exige regeneração com outro algoritmo) ou alvo com tolerância
operacional?

Análise das divergências mostrou que operacao_cruzamento e
operacao_perfil_grupo estão sujeitos a invariantes categóricos
fixos que restringem amostragem: Filial=8 · Transportadora=6 ·
Regiao=4 (todos contratos fechados em §I exercitados por assertions
V6/V7/V9) · warnings esperados como W-V9-SEGMENTO-TAMANHO-
INSUFICIENTE exigem segmento com <3 filiais · combinações dessas
restrições tornam certos números exatos inatingíveis sem violar
contrato semântico. Mesmo precedente da correção (b) em F-BASE
(cardinalidade 41→45 produtos · 80→85 filiais ajustou algoritmo
para respeitar §H.5 · mas apenas dentro do que era atingível sem
colisão).

Decisão: formaliza-se que valores na coluna "Tamanho" de §H.5
são alvos com tolerância operacional de aproximadamente ±3%
quando invariantes categóricos declarados em §H.5/§I e warnings
esperados restringem a amostragem. Contratos fechados (imutáveis
sem D-YYY) permanecem:
 (a) inventário de 14 abas (D-140 invariante 2)
 (b) nomes canônicos das abas (D-140 invariante 4)
 (c) cardinalidades categóricas declaradas (ex: Filial=8,
     Transportadora=6, Regiao=4, Produto=45, agrupador=85)
 (d) SEED=42 (D-140 invariante 3)
Sob tolerância ficam apenas os totais de linhas por aba em §H.5.
O til literal do total agregado ("~2.063") propaga-se aos valores
individuais.

Base F-BASE atual (1853 linhas · hash aa960eef...5a3b20fe)
permanece como base canônica. As 2 divergências (operacao_cruzamento
-5, -2.8% · operacao_perfil_grupo -2, -1.3%) estão dentro da
tolerância declarada · não exigem regeneração.

Razão:
(1) Contratos que vivem em §H.5 servem dois propósitos distintos:
inventário/nomes/cardinalidades são contratos estruturais fixos
exercitados por assertions que comparam contagens exatas
(V2-A04, V4-A02, V6-A01, V6-A02, V7-A01, V3-A01) · totais de
linhas por aba não são exercitados por assertions (nenhuma
assertion em casos_esperados.yaml verifica "vendas_padrao tem
exatamente 120 linhas") · servem como referência de volume para
o gerador, não como contrato semântico de negócio.
(2) Regenerar a base para corrigir 7 linhas (-0.4% do total)
seria desproporcional · custo de invalidar o hash SHA-256
aa960eef... vs. benefício zero para assertions · princípio
pragmatismo arquitetural.
(3) Formalização evita que futura regeneração tropece no mesmo
ponto · Claude Code ou sucessor saberão que diferença de 3%
nos tamanhos por aba é aceitável desde que invariantes
categóricos e warnings sejam preservados.
(4) Decisão não abre brecha para aceitar qualquer divergência ·
limita-se a ~3% explicitamente · e só quando invariantes
categóricos/warnings restringem amostragem · divergência que
excedesse a tolerância ou que violasse invariante categórico
exigiria D-YYY nova.

Impacto: spec_fundacao.md §H.5 recebe nota formal de D-145 após
a tabela de invariantes · total atual da base (1853 linhas) e
hash SHA-256 registrados. CONTEXT.md cabeçalho menciona a
tolerância. Instrucoes_do_Projeto.md seção "O que NÃO fazer"
ganha item sobre não tratar tamanhos por aba como contratos
fechados. Nenhuma alteração em gerar_base_fundacao.py ou
_auto_validar.py. Testes existentes continuam verdes (232/232
em 4.89s) · test_base_fundacao.py já não assertiona tamanhos
específicos.

Referência canônica: spec_fundacao.md §H.5 (nota formal após
invariantes D-140) · CONTEXT.md cabeçalho (breve menção).

### D-144 — Escopo arquitetural de D-130 · Result types operacionais vs analíticos
Data: 2026-04-21 · Bloco: retrospectiva F-EXP · Status: Fechada

Contexto: D-130 (20/04/2026) declarou receptividade a IA nos contratos
da Fundação com 3 requisitos concretos: (a) Pydantic BaseModel com
model_config para enums como string explícita · (b) todo campo com
Field(..., description=...) para schema auto-documentado · (c) método
.para_contexto_ia() em VNResultBase e MotorResult. F-MOT (21/04/2026)
implementou os 3 requisitos integralmente em UploadResult, MotorResult,
VNResultBase e DiagnosticoVN. F-EXP (21/04/2026) revelou lacuna em
contratos.py · ExportacaoResult declarado em §EXP.2 da spec consolidada
não havia sido criado em F-MOT · Claude Code corrigiu a lacuna criando
o contrato em F-EXP.

Ao avaliar a aplicação de D-130 ao novo Result type, emergiu distinção
arquitetural não explicitada antes: ExportacaoResult materializa
operação técnica (sucesso/falha de gerar xlsx · metadados de operação
como caminho_arquivo · tamanho_bytes · numero_abas · tempo_geracao_segundos
· warnings_gerados · capabilities_acionadas) · não materializa resultado
analítico que IA precise interpretar. Papel B da IA (leitura em linguagem
natural do resultado) opera sobre VNResult de uma visão · não sobre
sucesso de uma operação de exportação. Aplicar .para_contexto_ia() a
ExportacaoResult não tem caso de uso real.

Decisão: refina-se o escopo de D-130 distinguindo dois tipos de Result
types da Fundação:

1. Result types analíticos · materializam resultado de visão ou de
processo analítico que vai alimentar IA em Papel A (sugestão pré-
execução), Papel B (leitura natural pós-execução) ou Papel C
(recomendação de visão). Mantêm os 3 requisitos integrais de D-130:
- (a) Pydantic BaseModel com model_config para enums como string
- (b) Field(..., description=...) em todos os campos
- (c) método .para_contexto_ia() implementado
Escopo atual: VNResultBase · MotorResult.

2. Result types operacionais · materializam operação técnica
(serialização de saída · status de processo · metadados de execução)
que não tem caso de uso analítico de IA. Mantêm 2 dos 3 requisitos:
- (a) Pydantic BaseModel com model_config
- (b) Field(..., description=...) em todos os campos
- (c) DISPENSA .para_contexto_ia() por ausência de caso de uso
Escopo atual: ExportacaoResult.

Razão:
(1) Aplicar .para_contexto_ia() a Result type operacional gera código
inerte sem consumidor previsto · viola princípio de pragmatismo
arquitetural · cada requisito da Fundação deve ter razão de ser
declarada.
(2) D-130 foi formulada com Result types analíticos em mente
(VNResultBase e MotorResult eram os contratos conhecidos no momento
da formulação) · ExportacaoResult emergiu na implementação F-EXP e
revelou que a generalização "todos os Result types da Fundação têm
os 3 requisitos" precisava de refinamento.
(3) Field(..., description=...) preservado por consistência arquitetural
· schema auto-documentado vale para todos os contratos da Fundação
independentemente do consumidor previsto.
(4) Decisão é refinamento de escopo · não revogação de D-130 · a
classificação aqui criada (analítico vs operacional) também serve
para futuros Result types que emergirem na Fase 2 (visões individuais
podem produzir Result types operacionais auxiliares · ex: relatórios
de validação de modelo T-MODELO · que igualmente dispensariam
.para_contexto_ia()).

Impacto: ExportacaoResult em /src/contratos.py implementa apenas (a)
e (b) de D-130 · sem .para_contexto_ia(). Futuras adições de Result
types à Fundação ou às visões individuais devem declarar explicitamente
sua categoria (analítico ou operacional) e implementar D-130 conforme
o escopo refinado aqui. Bloco IA-Família-A (D-130) não consome
ExportacaoResult · permanece consumindo VNResultBase de V2/V1/V11
como originalmente previsto.

Referência canônica: CONTEXT.md §6 requisito 4 (D-130) atualizado com
nota sobre D-144 · Instrucoes_do_Projeto.md seção "Decisão estrutural
estratégica consolidada em 20/04/2026" atualizada · spec_fundacao.md
§EXP.2 (declaração de ExportacaoResult vive aqui · F-EXP implementou).

### D-143 — Descarte de openpyxl write_only em workbook com gráficos nativos
Data: 2026-04-21 · Bloco: retrospectiva F-EXP · Status: Fechada

Contexto: spec_fundacao.md §EXP.6 ponto 2 declarava a estratégia de
streaming para abas grandes da exportação Excel: "openpyxl modo
write_only para abas com > 10000 linhas (Base Analítica de V5/V6/V8
em bases grandes). Abas menores (Resumo · Parâmetros · Diagnóstico)
em modo padrão. Decisão fica transparente via capability adequada."

Ao implementar exportacao.py em F-EXP, o Claude Code identificou
incompatibilidade técnica conhecida do openpyxl: o modo write_only
ativado no Workbook (Workbook(write_only=True)) impede adicionar
gráficos via openpyxl.chart.* no mesmo workbook · o atributo _charts
do worksheet em modo write_only não suporta operações de chart
addition. Como F-EXP implementa 11 capabilities incluindo
CAP-BARCHART-NATIVO (V4·V10·V5·V7), CAP-COLUMNCHART-EMPILHADO-100
(V6), CAP-LINECHART-NATIVO (V10·V8·V3), CAP-COMBO-BAR-LINE (V10
Curva Pareto com 2 eixos Y) e CAP-HISTOGRAMA-BINS (V5) · todas
materializando o Coração Visual de cada visão (D-126 · padrão
estrutural §13.6) · usar write_only inviabilizaria os gráficos
nativos do mesmo workbook. A spec carregava contradição técnica
latente entre §EXP.6 ponto 2 (streaming via write_only) e §EXP.3
capabilities 4-10 (gráficos nativos no mesmo workbook).

Decisão: descarta-se write_only como mecanismo de streaming em
workbook que contém gráficos nativos. Substituição por ws.append()
linha-a-linha como mecanismo de escrita eficiente em memória ainda
que não streaming verdadeiro. ws.append() opera em modo padrão do
Workbook · compatível com gráficos nativos · mantém eficiência
razoável em abas com volume típico do produto (Base Analítica
V5/V6/V8 raramente ultrapassa 50000 linhas em bases reais
declaradas pela spec §H).

§EXP.6 ponto 2 da spec fica obsoleto na formulação atual e deve
ser atualizado em sub-tarefa do prompt F-BASE (ver Instruções
do Projeto seção "Abertura da próxima conversa") · nova
formulação:

"Streaming vs build-in-memory: openpyxl modo padrão (não write_only)
para todas as abas · escrita via ws.append() linha-a-linha em abas
grandes (Base Analítica de V5/V6/V8) garante eficiência razoável
em memória · write_only descartado por incompatibilidade conhecida
com gráficos nativos (D-143). Para abas > 100000 linhas em bases
reais, paginação via CAP-PAGINACAO-MATRIZ é a estratégia
declarada · não streaming."

Razão:
(1) Preservação do valor de negócio · Coração Visual D-126 é padrão
estrutural de produto formalizado · gráficos nativos materializam
visualmente a contribuição analítica primária de 7 visões (V4·V10·
V5·V7·V6·V8·V3) · descartá-los em favor de streaming técnico seria
inversão de prioridades.
(2) Princípio C.3 sem invenção de comportamento · spec declarava
duas exigências mutuamente incompatíveis (write_only + gráficos
nativos no mesmo workbook) · resolução pragmática preserva a
exigência de produto e ajusta a exigência técnica.
(3) ws.append() é mecanismo conhecido e documentado do openpyxl
para escrita eficiente · não introduz dependência nova · não muda
contrato público de exportar_resultado() · suite de testes de F-EXP
verificou compatibilidade.
(4) Princípio C.4 decisão estrutural vira D-XXX · descarte de
mecanismo nomeado pela spec é decisão estrutural · merece registro
formal mesmo sendo decisão técnica pura sem impacto de negócio.
(5) Roadmap futuro · se openpyxl resolver a incompatibilidade
write_only × charts em versão posterior, ou se houver migração
para biblioteca alternativa (xlsxwriter foi descartado em §EXP.6
ponto 1 · nova avaliação fica em P-EXP-01-Evo se demanda
emergir), D-143 pode ser revisitada.

Impacto: exportacao.py em /src/ usa openpyxl modo padrão (não
write_only) em todas as 11 capabilities · escrita eficiente via
ws.append() linha-a-linha em abas com Base Analítica · suite de
27 testes de F-EXP cobre o comportamento. spec_fundacao.md §EXP.6
ponto 2 atualizado em sub-tarefa do prompt F-BASE Claude Code.
Nenhum efeito em F-MOT, F-TRANS ou F-BASE futuro.

Referência canônica: spec_fundacao.md §EXP.6 ponto 2 (a atualizar
em F-BASE) · /src/exportacao.py implementação · CONTEXT.md
"O que NÃO fazer" atualizado com proibição explícita de write_only
+ charts no mesmo workbook · Instrucoes_do_Projeto.md mesmo
arquivo seção "O que NÃO fazer".

## D-142 — Padrão ALINHA · sessão dedicada de alinhamento ao fechar Marco
Data: 2026-04-21 · Bloco: ALINHA-Fundação-Design→F-MOT · Status: Fechada

Contexto: Projeto TabloFlow opera por blocos sequenciais com kit de encerramento 
D-033 ao final de cada bloco. O padrão D-033 funciona bem para blocos rotineiros 
(refino de DCV · sub-bloco de G-FUND · sessão de spec). Porém, ao fechar um Marco 
grande (fim de fase · conclusão de subsistema de design · transição entre modos 
operacionais), o kit de encerramento do último bloco dessa sequência fica 
insuficiente: emergem simultaneamente (a) necessidade de consolidação retrospectiva 
de múltiplos artefatos · (b) formalização de decisões técnicas pendentes que 
ficaram latentes · (c) transferência organizada de contexto para o modo 
operacional seguinte (frequentemente diferente do anterior · ex: Arquiteto → 
Claude Code). Duas ocorrências na história do projeto materializaram essa 
necessidade:

1ª ocorrência · Sessão Fase 0 → Fase 1 (20/04/2026) · produziu D-130 · D-131 · 
   D-132 em bloco pós-aprovação do 11º DCV · entrou em padrão sem nome · 
   retroativamente categorizada como ALINHA-Fase-0→Fase-1.

2ª ocorrência · esta sessão · ALINHA-Fundação-Design→F-MOT (21/04/2026) · 
   consolida 3 partes de spec_fundacao em arquivo único · formaliza D-140 · 
   D-141 · produz talk-through operacional de Claude Code · formaliza o próprio 
   padrão como D-142.

Decisão: formaliza-se o padrão ALINHA como tipo de bloco canônico, operando em 
complemento (não substituição) ao padrão D-033:

1. Gatilho · ALINHA é acionada quando se fecha um Marco · não quando se fecha 
um bloco rotineiro. Marco é definido por 3 critérios cumulativos: (a) encerra 
uma fase ou subsistema de design inteiro · (b) dispara transição para modo 
operacional diferente (ex: Arquiteto → Claude Code · Fase 0 → Fase 1 · design 
→ implementação) · (c) acumulou ≥ 3 decisões ou artefatos pendentes de 
consolidação.

2. Escopo canônico da sessão ALINHA · 4 sub-blocos sequenciais (nomeados α · β 
· γ · δ):

   α · Consolidação retrospectiva · unificação de artefatos produzidos em 
   múltiplas sessões anteriores em artefato único coerente (ex: 3 partes de 
   spec → spec consolidada) · eliminação de referências estruturais residuais 
   · validação cross-cuts.

   β · Talk-through operacional · transferência estruturada de contexto para 
   o modo operacional seguinte · protocolo, pré-requisitos técnicos, situações 
   de exceção, canal de retaguarda. Entregáveis concretos (ex: prompts prontos 
   para copy/paste · arranjo de sessões paralelas).

   γ · Formalização de decisões técnicas latentes · identificação e consolidação 
   de decisões que ficaram implícitas nas sessões anteriores do Marco · 
   produção de entradas D-XXX com rationale completo.

   δ · Kit de encerramento D-033 · aplicação integral do padrão D-033 com 
   atualização de todos os documentos canônicos em estado consolidado 
   pós-Marco. Prompt de abertura da próxima sessão é tipicamente dual: 
   (d1) prompt para modo operacional seguinte (ex: Claude Code) · (d2) prompt 
   para sessão de retrospectiva do Arquiteto quando o modo seguinte concluir.

3. Ordem dos sub-blocos · α primeiro (consolidação é pré-requisito para tudo 
que vem depois) · β ou γ indiferentes entre si · δ sempre último. Mini 
status-check entre sub-blocos recomendado mas não obrigatório (depende da 
densidade percebida).

4. Conteúdo decisional típico · seguindo princípio 3 de D-131: tipicamente 
0 decisões de negócio · 1-3 decisões técnicas puras (formalização das 
pendências de γ) · 0 execuções de código (validação fica para a retrospectiva 
pós-modo-seguinte).

5. Sessão ALINHA é nomeada com sufixo direcional · "ALINHA-<Marco fechado>
→<próximo modo>" · ex: "ALINHA-Fase-0→Fase-1" · "ALINHA-Fundação-Design→F-MOT". 
Esse nomeador serve para o painel do Projects saber a natureza da sessão 
de imediato.

Razão:
(1) Kit D-033 sozinho é insuficiente em fechamento de Marco porque mistura-se 
consolidação retrospectiva com transferência prospectiva de contexto · ALINHA 
segrega os dois em sub-blocos.
(2) Padrão já se repetiu duas vezes sem nome · terceira repetição sem 
formalização gera retrabalho cognitivo do Arquiteto descobrindo o mesmo 
fluxo a cada Marco.
(3) Princípio C.4 aplicado a metadecisão de método · decisões estruturais 
sobre o próprio método viram D-XXX como qualquer outra.
(4) Complementaridade com D-033 · ALINHA não substitui o padrão do kit de 
encerramento · envelopa-o como último sub-bloco (δ).
(5) Sessão ALINHA é tipicamente longa · 4 sub-blocos em sequência · mas evita 
fragmentação em múltiplas sessões menores porque o ganho do fechamento de 
Marco acontece pelo fluxo contínuo entre retrospectiva, prospectiva e 
consolidação.

Impacto:
- CONTEXT.md §11.1 nova · "Padrão ALINHA · sessão dedicada ao fechar Marco" 
  insere definição canônica de gatilho, escopo, 4 sub-blocos, ordem, conteúdo 
  decisional, nomeação, aplicações históricas, Marcos futuros identificados, 
  e complementaridade com D-033.
- CONTEXT.md §14 "Complementaridade com outros padrões" · ajuste para incluir 
  D-142 na lista de padrões complementares a D-131.
- Instrucoes_do_Projeto.md ganha seção própria "Padrão ALINHA · sessão dedicada 
  ao fechar Marco (D-142)" + passo 5 no ritual de abertura (identificar se a 
  sessão é ALINHA) + linha nova em "Não fazer" (não acionar ALINHA para 
  fechamento rotineiro).
- GLOSSARIO.md §1 · 2 verbetes novos · "Marco" (3 critérios cumulativos) · 
  "Padrão ALINHA" (4 sub-blocos · aplicações históricas).
- GLOSSARIO.md §2 · 1 verbete novo · "ALINHA-<Marco>→<próximo>" como tipo de 
  bloco de execução transversal.
- Marcos futuros identificados: (a) fechamento de F-MOT + F-TRANS + F-EXP + 
  F-BASE = fechamento da Fase 1 inteira · dispara ALINHA-Fase-1→Fase-2 · 
  (b) fechamento da Família A em Fase 2 · dispara ALINHA-Família-A→IA-Família-A 
  · (c) fechamento do Módulo 1 inteiro (pós-11 visões validadas) · dispara 
  ALINHA-M1→M2.
- Padrão D-131 de condução da Fase 1 permanece vigente e é respeitado em 
  sub-blocos de ALINHA (declaração de conteúdo decisional na abertura · 
  princípio 3 · aplicado nesta sessão como exemplo vivo).
- Precedente da 1ª ocorrência (Sessão Fase 0 → Fase 1 · 20/04/2026) 
  retroativamente categorizada como ALINHA-Fase-0→Fase-1 · decisões D-130 · 
  D-131 · D-132 emergidas naquela sessão ratificam o valor do padrão.

Referência canônica: CONTEXT §11.1 (definição canônica do padrão ALINHA) · 
§14 (complementaridade com D-131) · D-033 (kit de encerramento base · 
envelopado como sub-bloco δ) · D-131 (condução da Fase 1 · princípio 3 
aplicado em declaração de conteúdo decisional) · D-140 e D-141 (decisões 
produzidas no sub-bloco γ desta sessão · prova operacional do padrão) · 
esta sessão ALINHA-Fundação-Design→F-MOT como 2ª aplicação do padrão.


## D-141 — `casos_esperados.yaml` como artefato canônico de validação da base de fundação
Data: 2026-04-20 · Bloco: G-FUND · parte 3 · Status: Fechada

Contexto: G-FUND parte 3 §J precisava resolver 3 decisões técnicas puras sobre o artefato de validação da base de fundação: (a) formato do arquivo · (b) estrutura canônica · (c) pontos de consumo no ciclo de vida. Princípio 5 de D-131 aplicado · formato teve bifurcação real (JSON × YAML × MD estruturado) · Arquiteto sinalizou decisão com justificativa em vez de apresentar opção porque a escolha não afeta negócio.

Decisão: `/bases/casos_esperados.yaml` é o artefato canônico de validação do TabloFlow · 4 elementos cristalizados:

1. Formato YAML (não JSON · não MD estruturado). Rationale: YAML é legível por humano + parsing nativo Python (`pyyaml`) + suporta comentários + blocos multi-linha naturais. JSON descartado (sem comentários · aspas/vírgulas ruidosas). MD estruturado descartado (exige parser customizado · inviável para testes de regressão).

2. Estrutura canônica em 3 níveis: `metadata` (versão base · seed · total_abas · total_linhas) → `visoes:` (bloco por visão de V1 a V11 com assertions e aba principal/secundária/consumidas) → `transversais` (assertions transversais · motor_upload · bloqueio_operacional · determinismo).

3. 5 tipos de assertion canônicos · lista fechada: `contagem_exata` · `contagem_categoria` · `warning_presente` · `estrutura_saida` · `bloqueio_emitido`. Tipos adicionais parametrizados (`inferencia_boolean` · `inferencia_subtipo_id` · `determinismo_seed`) são instâncias dos 5 canônicos aplicadas a metadados. Extensão do conjunto canônico (novo tipo) exige D-YYY nova.

4. 3 pontos de consumo no ciclo de vida: (ponto 1) F-BASE · Claude Code consome como contrato de saída da base · auto-validação estrutural antes da entrega · (ponto 2) F-MOT/F-TRANS · testes automatizados de regressão consomem como gabarito de comportamento · quebra de assertion quebra o teste · (ponto 3) Fase 2 · checklist de Validação Visual por visão é derivado mecanicamente das assertions da respectiva visão em `casos_esperados.yaml` · princípio 4 de D-131 preservado (Usuária marca checklist · não lê código).

Razão: (1) Artefato consumido em 3 pontos distintos do ciclo exige forma única rastreável · YAML é padrão de facto para fixtures de teste em Python com zero dependência nova. (2) Estrutura em 3 níveis com tipos fechados garante que assertions futuras caibam no esqueleto sem ambiguidade semântica · mudança de estrutura exige D-YYY. (3) Derivação mecânica para Validação Visual da Fase 2 operacionaliza princípio 4 de D-131 sem exigir que Usuária leia código. (4) Profundidade A de sessão (H.1 implícita) · spec parte 3 declara estrutura · arquivo completo com 60-80 assertions é gerado em F-BASE pelo Claude Code.

Impacto:
- spec_fundacao.md parte 3 §J declara formato · estrutura · 5 tipos canônicos · 3 pontos de consumo
- Caminho canônico: /bases/casos_esperados.yaml
- F-BASE (bloco operacional futuro) recebe requisito explícito · gerar arquivo completo a partir do esqueleto declarado em §J.2 e dos cenários declarados em §I
- F-MOT/F-TRANS (blocos operacionais futuros) incluem dependência `pyyaml` em requirements · testes consomem o arquivo
- Fase 2 · Spec de cada visão documenta mapeamento de derivação do checklist a partir das assertions da visão
- CONTEXT.md §3 Fase 2 seção Validação Visual referencia D-141 como origem do checklist derivado (atualização implícita absorvida em próximos kits)
- Instrucoes_do_Projeto.md § "Não fazer" ganha linha: "Não alterar formato ou estrutura do casos_esperados.yaml sem D-XXX nova" (aplicado no kit desta sessão)
- Extensão do conjunto de 5 tipos canônicos de assertion exige D-YYY nova

Referência canônica: spec_fundacao.md parte 3 §J · D-131 princípio 4 (Validação Visual derivada) · D-140 (base de fundação consome e é consumida por casos_esperados.yaml)

## D-140 — `base_fundacao.xlsx` como dataset único multi-aba · 14 abas canônicas · SEED=42 como invariante
Data: 2026-04-20 · Bloco: G-FUND · parte 3 · Status: Fechada

Contexto: G-FUND parte 3 §H precisava resolver 4 decisões técnicas puras sobre arquitetura do dataset sintético de fundação: (a) arquivo único multi-aba × múltiplos arquivos temáticos · (b) dimensões (linhas · cardinalidades · distribuições) · (c) domínio simulado de referência · (d) tratamento do modo DUAL. Decisão consolidada declarada como invariante porque consumo cross-bloco (F-BASE gera · F-MOT/F-TRANS testam · Fase 2 valida) exige cristalização de escopo.

Decisão: `base_fundacao.xlsx` é o dataset sintético único da Fundação · 5 elementos cristalizados como invariantes:

1. Arquivo único multi-aba · caminho canônico `/bases/base_fundacao.xlsx`. Não múltiplos arquivos temáticos. Alinhado com CONTEXT §3 e estrutura de pastas. Renomeação do arquivo exige D-YYY.

2. Inventário canônico de 14 abas (ver spec_fundacao.md parte 3 §H.5): vendas_padrao · vendas_por_colunas · vendas_pre_agregadas · operacao_dispersao · operacao_cruzamento · operacao_perfil_grupo · dual_origem_crm · dual_comparado_erp · cadastral_fuzzy · vendas_volume_alto · cardinalidade_excessiva · boolean_disfarcado · eixo_sequencial_lacunas · eixo_sequencial_completo. Adição ou remoção de aba exige D-YYY e atualização de casos_esperados.yaml.

3. SEED=42 · semente aleatória fixa · invariante de reprodutibilidade C.1. Alteração exige D-YYY e regeneração integral da base. Executada duas vezes com SEED=42 a base produz DataFrames com hash estável (assertion DET-A01 em casos_esperados.yaml).

4. T-DUAL tratado via 2 abas dedicadas (dual_origem_crm + dual_comparado_erp) formando 1 par DUAL único compartilhado entre V1 e V11. Não 2 pares separados. Valida que o contrato T-DUAL é idempotente entre as duas visões · reduz ~100 linhas de base duplicada.

5. Vocabulário misto pragmático em pt-BR (não domínio único fechado) · 4 domínios mapeados: Vendas varejo (V2/V3/V4/V8/V10) · Conciliação financeira (V1/V11) · Operação/logística (V5/V6/V7/V9) · Cadastral (V11 T-FUZZY). Reconhecedor pt-BR/pt-EN (D-026) exercitado em datas. Unidades monetárias em R$.

Dimensões calibradas para 3 objetivos simultâneos (volume realista · cobertura de patamares ECP · auditabilidade manual): padrão 80-120 linhas por aba · cenário volume alto 300-500 linhas · distribuição log-normal (μ=6, σ=1) em campos numéricos · 5-8% de NULO_MEDIDA · 2-4% de Ausente em agrupador.

Razão: (1) F-BASE é bloco único de Claude Code que precisa de spec operacional (Profundidade A decidida em H) · inventário fechado e seed fixa eliminam ambiguidade sem inflar a spec com valores concretos. (2) Consumo cross-bloco (F-BASE · F-MOT · F-TRANS · Fase 2) exige que essas 4-5 dimensões sejam cristalizadas · mudança em qualquer delas sem D-YYY quebraria assertions em cadeia. (3) Determinismo C.1 absoluto exige seed fixa · 42 é convenção comum sem significado semântico · substituível por outro inteiro positivo se necessário (via D-YYY). (4) 14 abas foi o número que emergiu da cobertura completa dos 11 cenários de visão + 3 abas de motor puro (boolean_disfarcado · cardinalidade_excessiva · par DUAL compartilhado) · tentar reduzir corta cobertura · tentar ampliar adiciona redundância.

Impacto:
- spec_fundacao.md parte 3 §H declara inventário · SEED=42 · dimensões · domínios · T-DUAL
- F-BASE (bloco operacional futuro · Claude Code · após F-MOT · F-TRANS · F-EXP) recebe inventário como contrato de saída · script de auto-validação roda contra casos_esperados.yaml (D-141) antes de entregar
- F-MOT (próximo bloco) pode usar mini-datasets artificiais para testes unitários até F-BASE rodar · testes de integração aguardam base_fundacao.xlsx pronto
- F-TRANS idem F-MOT
- F-EXP consome casos de cada aba para validar capabilities contra estruturas reais · ativação final em Fase 2 com base_fundacao
- Fase 2 · cada visão carrega base_fundacao.xlsx (ou subset) no app · Validação Visual derivada de casos_esperados.yaml
- Instrucoes_do_Projeto.md § "Não fazer" ganha linha: "Não alterar SEED=42 nem inventário das 14 abas sem D-XXX nova" (aplicado no kit desta sessão)
- CONTEXT.md §3 Fase 1 ordem dos blocos · F-BASE marcado como "consome spec parte 3 · produz base_fundacao.xlsx + casos_esperados.yaml completo · auto-validação" (atualização absorvida no kit desta sessão)

Referência canônica: spec_fundacao.md parte 3 §H · §I (cobertura por visão · consumo do inventário) · §J (casos_esperados.yaml · D-141) · CONTEXT §3 (ordem dos blocos · F-BASE) · D-141 (artefato consumido em 3 pontos)

### D-139 — Módulo /src/utils/normalizacao_texto.py centralizado · consumido por T-FUZZY e T-CONCAT
Data: 2026-04-20 · Bloco: G-FUND · parte 2 · Status: Fechada
Contexto: Durante especificação de T-FUZZY (F.3) e T-CONCAT (F.4) em G-FUND parte 2, emergiu que ambos transversais precisam de normalização textual idêntica: lowercase · unidecode (remoção de acentos) · remoção de caracteres não-alfanuméricos exceto espaço · colapso de espaços múltiplos. T-FUZZY aplica normalização internamente antes de calcular trigramas e extrair tokens-chave. T-CONCAT aplica normalização condicionalmente quando normalizar=True (caso de uso V11 alimentando T-FUZZY downstream). Implementar normalização duplicada em 2 módulos cria risco arquitetural: divergência sutil entre T-FUZZY e T-CONCAT tornaria composição + scoring determinísticos individualmente mas divergentes em composição · quebra determinismo C.1 quando T-CONCAT alimenta T-FUZZY.
Decisão: Módulo /src/utils/normalizacao_texto.py centraliza a função normalizar_texto(texto: str) -> str consumida por T-FUZZY (internamente antes de trigramas e tokens) e por T-CONCAT (condicionalmente via parâmetro normalizar: bool). Implementação única · testes de regressão únicos · alteração da normalização exige D-XXX nova por afetar ambos os consumidores simultaneamente.
Razão: (1) Zero duplicação arquitetural · padrão consolidado do projeto (D-026 T-AGRUPA → T-EIXO reconhecedor pt-BR/pt-EN · D-052 T-FUZZY encapsulado · D-135 T-CONCAT apto a virar M2.CONCAT). (2) Determinismo absoluto C.1 blindado · composição T-CONCAT + T-FUZZY em V11 usa a mesma normalização em ambas as pontas · impossível divergência. (3) Extensão futura de normalização (ex: unificação de abreviações como operação M2.NORMALIZE) entra em módulo separado sem tocar a normalização básica · roadmap preservado.
Impacto:

spec_fundacao.md parte 2 · §F.3 (T-FUZZY) e §F.4 (T-CONCAT) referenciam o módulo centralizado
/src/utils/normalizacao_texto.py entra como requisito F-TRANS (implementado antes de T-FUZZY e T-CONCAT em ordem de dependência)
Testes de regressão de F-TRANS incluem casos canônicos da normalização (acentos pt-BR · caracteres especiais · espaços múltiplos · strings vazias · None)
Alteração futura da normalização dispara revisão conjunta de T-FUZZY e T-CONCAT

Referência canônica: spec_fundacao.md parte 2 §F.3 · §F.4 · /src/utils/normalizacao_texto.py (a ser implementado em F-TRANS)

### D-138 — Pesos internos fixos de T-FUZZY · calibração da Fundação
Data: 2026-04-20 · Bloco: G-FUND · parte 2 · Status: Fechada
Contexto: D-052 (T-FUZZY confirmado como transversal da Fundação) declarou que "pesos internos fixos · calibrados na implementação · não expostos ao usuário". G-FUND parte 2 §F.3 especifica os valores concretos da calibração: 0.65 para componente trigramas · 0.35 para componente tokens-chave · boost multiplicativo de 1.15 quando pelo menos 1 token-chave é compartilhado AND score_trigramas ≥ 0.4. Esta decisão formaliza esses valores como calibração oficial da Fundação · evita que cada consumidor (V11 MVP · V1 roadmap via P-V1-02-Evo) "ajuste" pesos localmente criando divergência.
Decisão: Pesos internos de T-FUZZY fixados na Fundação com os seguintes valores canônicos:

Componente trigramas (Jaccard): peso 0.65
Componente tokens-chave (Jaccard sobre tokens extraídos): peso 0.35
Boost condicional: multiplicador 1.15 aplicado quando tokens_compartilhados >= 1 AND score_trigramas >= 0.4 · limitado superiormente a 1.0 (clamp)

Extração de tokens-chave (definição canônica):

Sequências numéricas de 4+ dígitos consecutivos (ex: "12345" · "2024")
Sequências alfabéticas maiúsculas de 3+ caracteres consecutivos antes da normalização (ex: "CNPJ" · "DOC")

Alteração desses valores exige D-XXX nova porque afeta resultados reproduzíveis de todos os consumidores · quebra de contrato implícita dos scores publicados em Diagnóstico de V11.
Razão: (1) Princípio C.1 · determinismo absoluto · pesos públicos declarados permitem reprodutibilidade e auditoria. (2) Princípio C.5 · pesos encapsulados (não expostos ao usuário na UI) honram "TabloFlow analisa sobre o dado informado · nunca decide por ele" · complexidade do algoritmo de similaridade textual não é zona de decisão analítica do usuário. (3) Teste de regressão blindado em F-TRANS · cenário canônico Protheus × Safra do DCV-V11 produz scores esperados documentados · qualquer alteração de peso quebra teste e força D-XXX nova. (4) Formalização previne "ajustes" locais por consumidores futuros (V1 roadmap · M2.NORMALIZE futuro) · T-FUZZY é caixa-preta homogênea.
Impacto:

spec_fundacao.md parte 2 §F.3 declara pesos como calibração fixa
F-TRANS implementa T-FUZZY com esses valores hardcoded (não configuráveis)
Testes de regressão em /src/testes/test_t_fuzzy.py incluem casos canônicos com scores esperados documentados
Documentação em comentário do módulo /src/transversais/t_fuzzy.py referencia D-138 como fonte de verdade dos pesos
V11 aba Diagnóstico linha informativa única registra: "Normalização textual e cálculo de score aplicados pela transversal T-FUZZY (pesos internos calibrados na Fundação · D-138)"

Referência canônica: spec_fundacao.md parte 2 §F.3 · D-052 (T-FUZZY confirmado) · /src/transversais/t_fuzzy.py (a ser implementado em F-TRANS)

### D-137 — Enum escopo de T-RANK com 3 valores canônicos
Data: 2026-04-20 · Bloco: G-FUND · parte 2 · Status: Fechada
Contexto: D-041 formalizou T-RANK configurável com parâmetro regra_desempate. D-096 (V9 sétima consumidora) adicionou novo escopo cross_elementos_dentro_do_agrupador distinguindo-o de intra_grupo (V7) e global (V4/V10/V11). Os 3 escopos estavam documentados em DECISIONS e GLOSSARIO mas sem formalização do enum canônico no contrato da Fundação · G-FUND parte 2 §E.2 especifica o contrato ConfigRank com enum explícito.
Decisão: Enum escopo de T-RANK declarado na Fundação com 3 valores canônicos:

global · ranking cross-toda-a-base sem segmentação · usado por V4 · V10 · V11
intra_grupo · ranking dentro de grupo onde Grupo forma unidade analítica com o Elemento (campo dedicado · consolidação Elemento+Grupo) · usado por V7
cross_elementos_dentro_do_agrupador · ranking cross-elementos dentro de recorte definido por agrupador onde o agrupador apenas segmenta (consolidação é Identificador+Agrupador · cálculo de posições é cross-elementos) · usado por V9 Modo Segmentado

Distinção semântica entre intra_grupo e cross_elementos_dentro_do_agrupador é importante · não é apenas nomenclatura. Contrato declara explicitamente · evita confusão em implementação F-TRANS e em futuras visões consumidoras.
Extensão futura do enum (ex: novo escopo para visão futura fora do Módulo 1) entra via adição ao enum sem quebra de contrato (backward-compatible desde que valor existente não seja removido).
Razão: (1) Contratos da Fundação precisam ser explícitos em enums · D-130 (receptividade IA) exige valores string documentados via Field(..., description=...) para schema auto-documentado. (2) Distinção semântica V7 (Grupo interno) × V9 Segmentado (Agrupador externo) só fica clara com nomenclatura distinta · eliminação de ambiguidade. (3) V6 (oitava consumidora · D-115) usa escopo global no MVP · Modo Segmentado em roadmap P-V6-05-SEGMENTADO-Evo provavelmente consumirá cross_elementos_dentro_do_agrupador · enum aceita sem extensão. (4) Visões V1 e V11 (consumidoras de T-RANK em contexto probabilístico) usam global nativamente · sem necessidade de escopo adicional.
Impacto:

spec_fundacao.md parte 2 §E.2 declara enum com 3 valores
F-TRANS implementa T-RANK com enum Literal["global", "intra_grupo", "cross_elementos_dentro_do_agrupador"] em ConfigRank
GLOSSARIO §4 T-RANK entrada já registra o novo escopo (herança D-096) · sem mudança adicional necessária
Testes de regressão de T-RANK em F-TRANS cobrem os 3 escopos com casos canônicos derivados de V4 · V7 · V9
Extensão futura por visão nova segue padrão "herança adaptada à natureza analítica" D-073

Referência canônica: spec_fundacao.md parte 2 §E.2 · D-041 (T-RANK configurável) · D-088 (V7 intra_grupo) · D-096 (V9 escopo novo) · D-115 (V6 global)

### D-136 — F-EXP como bloco único sem divisão em sub-blocos · decisão de negócio M2 da D-131
Data: 2026-04-20 · Bloco: G-FUND · parte 2 · Status: Fechada
Contexto: M2 da D-131 (posicionamento técnico-decisional da Fase 1) exigia decisão de negócio sobre divisão ou não de F-EXP em sub-blocos. Tradução decisional: "em que ordem o Coração Visual de cada visão fica disponível · qual visão prioriza em termos de valor de negócio?". G-FUND parte 2 §EXP.4 apresentou 3 opções com trade-offs e recomendação do Arquiteto:

Opção A · bloco único · todas as 11 visões prontas juntas · simples · espera mais longa · consistência visual
Opção B · 3 sub-blocos (F-EXP-CORE + F-EXP-CHARTS + F-EXP-MATRIX) · Família A pronta primeiro · Validação Visual cedo · recomendação do Arquiteto
Opção C · 2 sub-blocos (CORE + VISUAL) · maior cobertura no primeiro sub-bloco · V10/V5/V6/V8 esperam

Usuária decidiu Opção A em 20/04/2026 durante fechamento da G-FUND parte 2.
Decisão: F-EXP é implementado como bloco único de Claude Code · não dividido em sub-blocos. As 11 capabilities (CAP-TABELA-FORMATADA · CAP-RESUMO-EXECUTIVO · CAP-DIAGNOSTICO · CAP-BARCHART-NATIVO · CAP-COLUMNCHART-EMPILHADO-100 · CAP-LINECHART-NATIVO · CAP-COMBO-BAR-LINE · CAP-FORMATACAO-CONDICIONAL-MATRIZ · CAP-HISTOGRAMA-BINS · CAP-PAGINACAO-MATRIZ · CAP-AUTOFILTER) são implementadas em sequência dentro do mesmo bloco · F-BASE começa apenas quando F-EXP inteiro está completo · Fase 2 abre com S-V2 (Spec V2 · Família A) apenas depois que F-BASE fecha.
Roadmap linear da Fase 1 preservado: F-MOT → F-TRANS → F-EXP (único) → F-BASE → Fase 2 Família A.
Razão (Opção A escolhida pela Usuária): (1) Simplicidade arquitetural · um único bloco de Claude Code · uma única revisão integrada · elimina risco de divergência entre sub-blocos. (2) Consistência visual · todas as 11 visões saem com o mesmo nível de polimento e atenção · nenhuma fica "provisoriamente pronta" esperando refinamento posterior. (3) Sem retrabalho de sub-blocos · capabilities complexas (CAP-COMBO-BAR-LINE para V10 · CAP-FORMATACAO-CONDICIONAL-MATRIZ para V6) podem revelar ajustes necessários nas capabilities universais (CAP-RESUMO-EXECUTIVO · CAP-TABELA-FORMATADA) que seriam aplicados em sub-bloco anterior já "fechado" na Opção B. (4) Previsibilidade de cronograma · bloco único tem 1 ponto de conclusão · 1 Validação Visual por visão na Fase 2 · matriz de estado simples.
Trade-off aceito pela Usuária: Família A (V2 · V1 · V11) consome apenas 4 capabilities (1 · 2 · 3 · 11) mas espera as 11 capabilities estarem prontas antes de poder ser testada. Bloco IA-Família-A (D-130) acontece após validação visual de V2 · V1 · V11 · como originalmente previsto · sem ajuste de roadmap.
Impacto:

spec_fundacao.md parte 2 §EXP.4 registra decisão tomada · §EXP.3 capabilities não sofrem alteração de escopo
CONTEXT §3 Fase 1 · ordem dos blocos atualizada · F-EXP marcado como "bloco único (D-136)"
CONTEXT §14 · M2 da D-131 marcado como "RESOLVIDO em G-FUND parte 2 · D-136" com tradução decisional preservada
Planilha · dashboard visual da Fase 1 · F-EXP como 1 barra de progresso (sem sub-barras)
Prompt de abertura de F-EXP (bloco operacional futuro · após F-MOT · F-TRANS · G-FUND parte 3) referencia D-136 como fonte da decisão de escopo único
Princípio 4 de D-131 (Validação Visual como único mecanismo de aprovação) permanece servido · apenas com timing diferente da Opção B

Referência canônica: spec_fundacao.md parte 2 §EXP.4 · CONTEXT §3 (Fase 1 · ordem dos blocos) · §14 (M2 da D-131 resolvido) · D-131 (condução Fase 1 · M2 identificado) · D-132 (dashboard visual Fase 1)

## D-135 — Decisão mista de posicionamento · T-CONCAT na Fundação · M2.STACK em M2
Data: 2026-04-20 · Bloco: G-FUND · parte 1 · Status: Fechada

Contexto: T-CONCAT e M2.STACK marcados como "candidatos" em CONTEXT §6 desde V11 D-053 (T-CONCAT) e V3 D-063 (M2.STACK · posteriormente confirmado com V8 D-074 e V6 D-111 como 3 consumidores). Posicionamento final adiado para G-FUND conforme CONTEXT §6. M1 da D-131 (posicionamento T-CONCAT/M2.STACK · decisão de negócio com tradução "quando V3, V6, V8 ganham multi-aba"). Durante G-FUND parte 1 Tópico G, Arquiteto apresentou 3 opções arquiteturais (A · ambos Fundação · B · ambos M2 · C · capability compartilhada) com trade-offs de roadmap e complexidade + opção mista recomendada. Usuária aprovou decisão mista.

Decisão: Posicionamento diferenciado · T-CONCAT na Fundação (Posição 1) · M2.STACK em M2 (Posição 2).

T-CONCAT · Fundação:
- Transversal fundamental implementado em F-TRANS
- Código vive em `/src/transversais/t_concat.py`
- V11 consome no MVP (Família A)
- Dimensões herdadas de D-053 + refino DCV-V11 T-04: até 3 campos-fonte · separador fixo espaço · assimetria permitida · tratamento de nulos (campos nulos pulados · todos nulos resulta em string vazia)
- Implementação com estrutura apta para renomeação/extração futura para M2.CONCAT sem reescrita · zero duplicação arquitetural coerente com intenção original de D-053
- API pura determinística consumida por V11 e por T-FUZZY (a jusante · via normalização textual)

M2.STACK · M2:
- Fora do escopo da Fundação · Fase 1 não implementa
- Fica como operação M2 confirmada · implementação em bloco dedicado pós-Módulo 1
- V3 · V6 · V8 mantêm multi-aba como roadmap pós-MVP exatamente como declarado nos DCVs aprovados (P-V3-01-Evo · P-V8-01-Evo · P-V6-02-MULTIABA-Evo) · nenhuma mudança downstream
- M2 futuro implementa do zero com contexto completo do Módulo 2 (operações de preparação de dados)

Razão: (1) T-CONCAT tem consumidor MVP (V11) e implementação simples (concatenar 2-3 strings com separador) · custo marginal na Fundação é baixo. (2) M2.STACK tem 3 consumidores em roadmap (V3/V6/V8 · nenhum MVP) e implementação complexa (detecção estrutural entre abas · tratamento de divergência · vocabulário · bloco de confirmação · warnings específicos) · implementar na Fundação adicionaria 3-4 semanas sem urgência de entrega. (3) DCVs de V3/V6/V8 declararam explicitamente multi-aba como fora do escopo MVP · Opção B para M2.STACK ratifica decisão anterior · Opção A/C revisaria sem justificativa de negócio nova. (4) Princípio A.1 (3 fases sequenciais) permite posicionamento diferenciado por componente sem ferir coerência · T-CONCAT e M2.STACK têm perfis distintos (simplicidade vs complexidade · MVP vs roadmap) · decisão mista é arquiteturalmente honesta. (5) M2 futuro herdará T-CONCAT pronto (renomeação para M2.CONCAT) · risco de divergência de interface mitigado pela disciplina de extração declarada em D-053.

Impacto:
- spec_fundacao.md parte 1 · seção G (decisão de roadmap) · seção F da parte 2 terá especificação completa de T-CONCAT como transversal de composição
- CONTEXT §6 · tabela de transversais · T-CONCAT muda de "candidato" para "Fundação (D-135)" com dimensões consolidadas · M2.STACK sai da tabela de transversais e vira nota de "movido para M2 (D-135)"
- CONTEXT §14 · M1 marcado como RESOLVIDO em G-FUND parte 1
- GLOSSARIO §4 · entrada T-CONCAT reformulada (candidato → Fundação confirmada) · entrada M2.STACK reformulada (candidato → M2 confirmado · fora do escopo Fundação)
- Instruções do Projeto · seção "O que NÃO fazer" ganha linha: "Não tratar M2.STACK como candidato da Fundação"
- Planilha aba 3 · linha T-CONCAT muda status para "Fundação confirmada · especificar em G-FUND parte 2" · linha M2.STACK removida da tabela de transversais da Fundação e anotada como "movida para M2"
- F-TRANS ganha 12º transversal a implementar: T-CONCAT (além de T-AGRUPA · T-DIAG · T-SEMA · T-EIXO · T-RANK · T-ACUM · T-ABC · T-PIVOT · T-DUAL · T-MODELO · T-FUZZY)
- Roadmap posterior · M2 começa com T-CONCAT já pronto (renomeação) + M2.STACK para implementar do zero

Referência canônica: spec_fundacao.md parte 1 §G · CONTEXT §6 · §14 · GLOSSARIO §4 · Instruções do Projeto "O que NÃO fazer" · TabloFlow_Estado_do_Projeto.xlsx aba 3

---

## D-134 — BloqueioOperacional como contrato único compartilhado · materialização arquitetural do padrão MBO
Data: 2026-04-20 · Bloco: G-FUND · parte 1 · Status: Fechada

Contexto: Padrão MBO · Matriz de Bloqueios Operacionais formalizado em D-127 como princípio derivado C.D4 da Camada C. Enunciado declara que cada bloqueio tem (a) condição estrutural, (b) comportamento padrão, (c) escapável × não-escapável, (d) microcopy, (e) warning associado quando escape é acionado. A formalização deixou em aberto a materialização arquitetural · "como isso vira código na Fundação · contratos específicos por visão ou contrato único compartilhado". Durante G-FUND parte 1 Tópico A.4 · definição de VNResultBase, a pergunta precisa ser respondida porque bloqueios aparecem no contrato VNResultBase e na aba Diagnóstico consolidada.

Decisão: BloqueioOperacional é Pydantic BaseModel único compartilhado por todas as 11 visões. Campos:
- codigo: str (padrão B-VN-DESCRITOR · ex: "B-V6-EIXO-NUMERICO-CONTINUO")
- condicao_disparo: str (microcopy descritivo · visível ao usuário)
- escapavel: bool
- escape_acionado: Optional[bool]
- warning_pos_escape: Optional[str] (código do warning permanente quando escape é acionado · respeita C.2 nada silencioso)
- contexto_disparo: Dict[str, Any] (campos relacionados · contagens · valores observados)

Specs S-VN (Fase 2) declaram a matriz de bloqueios V-específica como lista de dicionários com esses campos. Motor da visão instancia BloqueioOperacional preenchido na ordem declarada. exportacao.py consome a lista sem conhecer a visão-origem · aba Diagnóstico consolida bloqueios de qualquer visão sem código específico por visão.

Razão: (1) Padrão MBO é estrutural · declara que todas as visões têm matriz de bloqueios com mesma forma (a-e) · forma compartilhada exige contrato compartilhado · princípio de consistência. (2) exportacao.py consome bloqueios na aba Diagnóstico · se cada visão tivesse contrato próprio, exportacao precisaria conhecer 11 contratos distintos · overhead arquitetural desnecessário. (3) IA receptiva (D-130) tem acesso a estrutura uniforme · leitura em linguagem natural do resultado da visão (Papel B futuro) consome BloqueioOperacional do mesmo jeito em V1 que em V6 · reduz custo de contexto para IA. (4) Princípio C.1 (determinismo) · mesma estrutura de bloqueio na mesma situação · mesmo vocabulário de codigo · mesma forma de contexto_disparo · auditabilidade uniforme cross-visão. (5) Desvios por visão (ex: V6 precisa de bloqueio específico com matriz Eixo1×Eixo2 no contexto_disparo) acomodados no campo contexto_disparo: Dict[str, Any] · flexibilidade V-específica sem fragmentar contrato.

Impacto:
- spec_fundacao.md parte 1 §A.5 (BloqueioOperacional como contrato único)
- spec_fundacao.md parte 1 §A.4 (VNResultBase inclui bloqueios_disparados: List[BloqueioOperacional])
- Specs S-VN da Fase 2 declaram matriz de bloqueios V-específica como lista de dicionários preenchendo os 6 campos
- exportacao.py (Fase 1 · spec em parte 2) consome List[BloqueioOperacional] de qualquer visão sem código específico
- Aba Diagnóstico ganha Seção 4 "Bloqueios escapados" uniforme cross-visão
- Padrão MBO (C.D4 · D-127) ganha materialização arquitetural explícita na Fundação
- Princípio B.2 (spec com 3 seções) implicitamente reforçado · seção de regras da Spec S-VN inclui declaração formal da matriz de bloqueios V-específica

Referência canônica: spec_fundacao.md parte 1 §A.5 · CONTEXT §9 Camada C · MBO · C.D4 · D-127

---

## D-133 — column_meta.tipo_estrutural sempre computado pelo motor_base · determinismo de metadados
Data: 2026-04-20 · Bloco: G-FUND · parte 1 · Status: Fechada

Contexto: Requisito column_meta.tipo_estrutural declarado em D-113 (origem V6) como 5 valores enum no motor_base. DCV-V6 declarou que "heurística detalhada fica no motor_base · V6 apenas consome a classificação". Questão em aberto no G-FUND: motor_base computa tipo_estrutural sempre (em toda coluna · independente de qual visão vai consumir) ou só quando a visão ativa pede (lazy)? Decisão relevante para M3 da D-131 (camada de inferência · tradução de negócio "V11 na Família A junto com V2/V1 ou no final?"). Mesma questão se aplica ao metadado subtipo_id_detectado (D-103 · origem V5 · consumido V6 D-112 · consumido V11 para campo-chave de matching).

Decisão: motor_base computa tipo_estrutural e subtipo_id_detectado em TODA coluna do DataFrame, sempre, independente da visão ativa. Não é lazy. Não é opcional. Ambos os metadados aparecem populados em ColumnMeta para toda coluna em todo MotorResult.

Razão: (1) Princípio C.1 (determinismo absoluto) · mesmo input deve produzir mesmo MotorResult · incluindo metadados não consumidos pela visão ativa · usuário trocar de visão não pode mudar MotorResult. (2) Princípio C.2 (nada silencioso) · se um metadado é relevante para alguma visão, deve estar visível sempre · tornar computação condicional cria estado divergente entre sessões. (3) Custo computacional é O(n) por coluna · desprezível mesmo em bases de 500K linhas (limite saudável do motor_base) · trade-off "economizar computando só quando pede" não compensa a confusão de estado. (4) M3 da D-131 · a questão "em qual camada tipo_estrutural é inferido" tem única resposta tecnicamente correta: motor_base · porque a inferência exige a coluna completa (amostragem de 5 linhas do preview do motor_upload é insuficiente para thresholds de 80% · cardinalidade · detecção de padrões aritméticos). Decidir inferir em motor_upload seria tecnicamente errado. (5) Consequência de negócio (tradução D-131): V11 fica disponível na Família A junto com V2 e V1 sem atraso · não há dependência adicional a implementar pós-Fundação.

Impacto:
- spec_fundacao.md parte 1 §A.3 (ColumnMeta declara tipo_estrutural e subtipo_id_detectado como campos obrigatórios)
- spec_fundacao.md parte 1 §C.2 (heurística tipo_estrutural) · §C.3 (matriz column_meta) referem-se a computação sempre executada
- CONTEXT §14 · M3 marcado como RESOLVIDO em G-FUND parte 1 como decisão técnica pura · consequência de negócio registrada (V11 sem atraso)
- Família A fica com 3 visões sem dependências técnicas adicionais · roadmap de Fase 2 preservado
- F-MOT (implementação do motor_base) recebe requisito explícito · sem ramificação condicional por visão ativa
- Princípio C.D1 (CPCO · D-122) reforçado por D-133 · consolidação pré-cálculo depende de metadados estáveis

Referência canônica: spec_fundacao.md parte 1 §A.3 · §C.2 · CONTEXT §9 C.1 · C.2 · §14 M3

## D-132 — Dashboard visual da Fase 1 na aba 1 da planilha · progresso por bloco com barras visuais
Data: 2026-04-20 · Bloco: Sessão de Alinhamento Fase 0 → Fase 1 · Status: Fechada
Contexto: Durante o Item 4 da sessão, a Usuária sinalizou que a planilha atual (4 abas organizadas por fase/bloco com notas em prosa nas colunas de status) funcionou bem na Fase 0 porque o artefato era DCV (prosa aprovável pela Usuária), mas na Fase 1 os blocos são técnicos (código, transversais, capabilities de exportação, base sintética) e ela quer visualizar progresso sem depender de entender cada termo técnico. 4 opções de layout analisadas (α manter layout atual · β barra de progresso na própria aba 3 · γ dashboard visual na aba 1 + aba 3 mantém granularidade técnica · δ dashboard externo à planilha). Usuária escolheu Opção γ após recomendação do Arquiteto.
Decisão: Aba 1 · Visão Geral da planilha ganha seção nova "Progresso da Fase 1 · Fundação" abaixo da seção atual "Próximo passo operacional". Seção contém 5 linhas (uma por bloco · G-FUND · F-MOT · F-TRANS · F-EXP · F-BASE) com 3 colunas: (a) nome do bloco, (b) barra visual via caracteres Unicode de bloco cheio/vazio (`█` e `░` · 16 caracteres de largura total), (c) % numérico de conclusão. Linha de totalizador "Fase 1 · Fundação" exibe média dos 5 blocos. Aba 3 · Fase 1 · Fundação mantém granularidade técnica (transversais individuais, capabilities individuais, critérios de transição, notas técnicas) como referência detalhada. Atualização sincronizada das duas abas em cada kit de encerramento de sessão da Fase 1. Padrão aplicável depois à Fase 2 (11 linhas · uma por visão).
Razão: (1) Responde exatamente a demanda da Usuária por acompanhamento mais visual · aba 1 é a primeira aba aberta na planilha · progresso fica lido em 3 segundos sem depender de vocabulário técnico. (2) Preserva aba 3 como referência técnica · respeita zona de conforto declarada da Usuária (negócio, não código) sem descaracterizar a camada técnica que o Arquiteto e Claude Code vão consumir na execução. (3) Custo de sincronização entre aba 1 e aba 3 é do Arquiteto (instruções de edição claras no kit de encerramento), não da Usuária. (4) Padrão replicável para Fase 2 com mesma estrutura · zero retrabalho conceitual quando a fase mudar.
Impacto:
Planilha aba 1 · seção nova "Progresso da Fase 1 · Fundação" implementada no kit de encerramento desta sessão (pré-populada com 0% em todos os 5 blocos · G-FUND abre em 0%)
Planilha aba 3 · mantida como está · pré-populada com estrutura que receberá os 12 transversais + ~8 capabilities + 5 critérios de transição conforme G-FUND consolida
Kit de encerramento D-033 ganha sub-item novo em cada sessão da Fase 1 · atualizar % por bloco + regenerar barras visuais · absorvido no fluxo padrão de instruções de edição
Padrão aplicável em Fase 2 · 11 linhas por visão · mesma estrutura (% numérico + barra Unicode)
Referência canônica: TabloFlow_Estado_do_Projeto.xlsx aba 1 · D-131 (padrão de condução Fase 1 · este dashboard é materialização do princípio 2) · CONTEXT §11 ritual de encerramento

## D-131 — Padrão de condução da Fase 1 · Didática técnico-decisional para Usuária não-técnica
Data: 2026-04-20 · Bloco: Sessão de Alinhamento Fase 0 → Fase 1 · Status: Fechada
Contexto: A Fase 1 tem natureza fundamentalmente diferente da Fase 0: artefatos são código (não prosa), executor principal é Claude Code (não Arquiteto), validação depende de testes + inspeção técnica (não aprovação de DCV). A Usuária declarou explicitamente que tem visão de negócio e não de desenvolvimento técnico. Método D-019 + D-034 + D-033 foi desenhado para refino de DCV · Fase 1 precisa de adaptação didática. Durante a sessão de alinhamento a Usuária levantou 3 questões convergentes: (1) acompanhamento visual na planilha (resolvida em D-132), (2) momento em que discussões técnicas vão chegar à mesa dela, (3) didática geral da fase. Esta decisão consolida a didática da Fase 1.
Decisão: Formalização do padrão "Condução em Fase Técnica com Usuária Não-Técnica" aplicável a G-FUND, F-MOT, F-TRANS, F-EXP, F-BASE · 5 princípios operacionais:

Princípio 1 · Tradução obrigatória técnico → decisional. Qualquer decisão técnica que impacte negócio (prazo, roadmap, disponibilidade de visão, experiência do usuário final) é traduzida para linguagem decisional antes de ser apresentada à Usuária. Usuária nunca precisa entender vocabulário técnico (camada de motor, openpyxl, transversal, contrato serializável) para decidir. Decisões técnicas puras (sem impacto de negócio) são resolvidas pelo Arquiteto sem consulta.

Princípio 2 · Acompanhamento visual primário · técnico secundário. Aba 1 da planilha materializa progresso visual · demais abas materializam detalhe técnico. Usuária abre a planilha e entende progresso em 3 segundos (D-132).

Princípio 3 · Sinalização proativa de densidade técnica. Toda sessão da Fase 1 abre com declaração explícita sobre seu conteúdo decisional: "X decisões de negócio · Y decisões técnicas puras que eu resolvo · Z execuções de código supervisionadas". Usuária entra na sessão sabendo seu papel esperado.

Princípio 4 · Validação visual como único mecanismo de aprovação da Usuária. Na Fase 2, Usuária não lê código · carrega base sintética no app e marca checklist derivado do DCV aprovado + CASOS_ESPERADOS (princípio B.4 do CONTEXT já formalizado). Na Fase 1, validação acontece em 1 momento único · inspeção manual da base de fundação processada no fechamento de F-BASE. Nenhuma sessão da Fase 1 exige que a Usuária leia código.

Princípio 5 · Transparência mútua sobre calibração. Usuária sinaliza quando Arquiteto explica demais algo técnico desnecessário · Arquiteto sinaliza quando percebe decisão técnica pura que também deveria ser trazida com opção. Feedback mútuo nas primeiras sessões da Fase 1 ajusta calibração · padrão só é considerado estabilizado após 2-3 sessões aplicadas.

4 momentos técnicos previstos na Fase 1 que exigem tradução princípio 1:
(M1) G-FUND · posicionamento T-CONCAT e M2.STACK (decisão de roadmap · quando V3/V6/V8 ganham multi-aba)
(M2) G-FUND · divisão ou não de F-EXP em sub-blocos (decisão de ordem de disponibilidade dos Corações Visuais)
(M3) F-MOT · camada onde column_meta.tipo_estrutural é inferido (decisão de quando V11 fica disponível na Família A)
(M4) Fase 2 · Validação Visual de cada visão com checklist de aspectos derivado de DCV + CASOS_ESPERADOS

Razão: (1) A Usuária declarou explicitamente o escopo de sua zona de decisão (negócio) e o que não é (desenvolvimento). Método que exige migração dessa zona é método que ignora realidade operacional. (2) Padrões D-019/D-034/D-033 funcionaram para Fase 0 porque DCV é prosa aprovável por não-técnico · Fase 1 produz artefato técnico e precisa de ponte didática. (3) Princípio 1 é o coração do padrão · os outros 4 são ferramentas que o operacionalizam. (4) Princípio 5 reconhece que calibração exata só emerge em uso · não tenta definir tudo a priori.
Impacto:
Instrucoes_do_Projeto.md · seção nova "Condução da Fase 1" com os 5 princípios + 4 momentos técnicos previstos
CONTEXT §11 ritual de encerramento ganha nota de complementaridade com D-131 (encerramento da Fase 1 aplica os 5 princípios)
Padrão D-019 permanece para eventuais refinos de DCV futuros (DCV-OPN do Módulo 2) · padrão D-131 é complementar · não substituto
Arquiteto incorpora princípios 1, 2, 3, 5 no padrão de condução de toda sessão da Fase 1 · princípio 4 é aplicado apenas na Fase 2
Calibração revisitada proativamente após 2-3 sessões da Fase 1 aplicadas · eventual D-XXX de refino se necessário
Referência canônica: Instrucoes_do_Projeto.md seção "Condução da Fase 1" · CONTEXT §11 · D-132 (dashboard · materialização do princípio 2)

## D-130 — Receptividade a IA nos contratos da Fundação · implementação pós-Família A validada · ratificação do princípio 3 de CONTEXT §1
Data: 2026-04-20 · Bloco: Sessão de Alinhamento Fase 0 → Fase 1 · Status: Fechada
Contexto: Durante o Item 5 desta sessão, a Usuária questionou o timing da Frente IA declarado inicialmente na planilha ("⏸ Parqueada · ativar quando uma família inteira de visões estiver validada · provavelmente após Família A"). Em resposta, o Arquiteto apresentou camada didática (3 papéis da IA no TabloFlow: A · assistiva de configuração · B · interpretativa de resultado · C · assistiva de escopo) e separou a questão em duas decisões: (a) decisão estrutural obrigatória no G-FUND sobre receptividade nos contratos · (b) decisão deferível sobre timing da implementação. Usuária confirmou aceitação de ambas as decisões após análise.
Decisão: Duas decisões consolidadas:

(a) G-FUND declara receptividade a IA nos contratos da Fundação. Concretamente: UploadResult, MotorResult, padrão VNResult e T-DIAG devem ser estruturados, serializáveis (JSON-compatível com enums explícitos), com rastreabilidade e metadados acessíveis em forma que permita consumo futuro por camada de IA. Nenhuma implementação de IA acontece na Fase 1 · apenas declaração de contrato apto. Isso é o que o princípio 3 de CONTEXT §1 ("IA sugere, Usuária confirma, Motor executa") operacionaliza em nível técnico.

(b) Implementação de IA acontece em bloco dedicado após a Família A validada. Bloco tentativo nomeado "IA-Família-A" · adiciona Papel A (sugestão de preenchimento de configuração antes da execução) e Papel B (leitura em linguagem natural do resultado estruturado) a V2, V1 e V11. Papel C (recomendação de qual visão usar) é bloco separado · eventualmente após Família C validada.

Razão: (1) Custo marginal de declarar receptividade agora é baixo · a maioria dos contratos já precisa ser estruturada e serializável por outros motivos (export Excel determinística, testes automatizados, coerência entre blocos). Custo de não declarar é alto · integrar IA depois exigiria refatoração de contratos em cada visão implementada. (2) Implementar IA antes de validar motor é risco real de produto · IA em cima de motor não-validado verbaliza bug em linguagem convincente e usuário acredita. Validar motor + visões primeiro é disciplina de produto. (3) Papel C (recomendação de visão) precisa de repertório de pelo menos uma família completa para funcionar bem · prematuro antes de Família A. (4) Operação solo da Usuária + Fase 2 da Família A ativa = concorrência de contexto se IA rodasse em paralelo · sequenciamento reduz carga operacional.
Impacto:
G-FUND ganha tópico novo · "Receptividade a IA nos contratos" · subitem do tópico Contratos de Dados (tópico A da agenda proposta no Item 4 da sessão de alinhamento)
Contratos UploadResult, MotorResult, VNResult, T-DIAG declarados no spec_fundacao.md incluem requisito explícito de serialização JSON-compatível e rastreabilidade para consumo futuro de IA
Nenhum bloco F-* novo é criado na Fase 1
Planilha aba 1 · nota da Frente IA atualizada: "⏸ Parqueada · receptividade declarada nos contratos da Fundação (G-FUND) · implementação em bloco IA-Família-A após V2+V1+V11 validadas"
CONTEXT §1 princípio 3 permanece como está (já correto em linguagem de produto) · sem reescrita
Roadmap posterior · Papel C da IA (recomendação de visão) fica em bloco separado IA-Meta após Família C validada · timing a confirmar
Referência canônica: CONTEXT §1 princípio 3 · spec_fundacao.md (G-FUND) · TabloFlow_Estado_do_Projeto.xlsx aba 1 seção Frentes Paralelas

Status update (21/04/2026): Ratificada em código em F-MOT · contratos.py 
implementou os 3 requisitos concretos (Pydantic BaseModel com model_config 
· Field com description · método .para_contexto_ia() em VNResultBase e 
MotorResult) · 71 testes verdes validaram serialização JSON-compatível.

## D-129 — Sumário da formalização dos 7 padrões consolidados · Sessão de Alinhamento Fase 0 → Fase 1
Data: 2026-04-20 · Bloco: Sessão de Alinhamento Fase 0 → Fase 1 · Status: Fechada
Contexto: Sessão de Alinhamento Técnico Fase 0 → Fase 1 (20/04/2026 · bloco próprio sem prefixo G-*, F-*, S-*) consumiu os 7 padrões consolidados que estavam marcados como "candidatos muito fortes à formalização efetiva" em CONTEXT §9 Camada C desde o fechamento da Fase 0. A Usuária escolheu Opção A (formalizar agora nesta sessão via D-XXX dedicados · 7 entradas D-122 a D-128 produzidas em sequência · mini status-check ao meio confirmou orçamento saudável).
Decisão: 7 padrões consolidados formalizados como princípios/padrões nominais do método TabloFlow:

D-122 · Padrão 1 · Consolidação Pré-Cálculo Obrigatória (CPCO) · §9 Camada C
D-123 · Padrão 2 · Thresholds Editáveis Declarados (TED) · §9 Camada C
D-124 · Padrão 3 · Base Analítica e Diagnóstico (BAD) · §9 Camada C
D-125 · Padrão 4 · Resumo Executivo em 6 Blocos · §13 padrão estrutural de produto
D-126 · Padrão 5 · Coração Visual da Visão · §13 padrão estrutural de produto
D-127 · Padrão 6 · Matriz de Bloqueios Operacionais (MBO) · §9 Camada C
D-128 · Padrão 7 · Escala de Cardinalidade com Patamares (ECP) · §9 Camada C

Distribuição estrutural: 5 princípios derivados em §9 Camada C (CPCO, TED, BAD, MBO, ECP) · 2 padrões estruturais de produto em §13 (Resumo Executivo em 6 Blocos, Coração Visual da Visão).

Razão da escolha da Opção A: (1) Contexto quente dos 7 padrões em memória operacional permitia enunciação mais precisa que em sessão futura. (2) Orçamento da sessão reflexiva suportou os 8 D-XXX sem pressão. (3) G-FUND se beneficia diretamente · consome os 7 padrões como regras nomeadas em vez de re-derivar. (4) Fase 2 fica padronizada desde a primeira Spec (S-V2). (5) Risco de "formalização eterna" eliminado.

Impacto:
CONTEXT §9 Camada C reescrito · 5 novos princípios derivados com enunciado formal, rationale, escopo, relação com princípios existentes, aplicações consolidadas, exceções permitidas, impacto no método
CONTEXT §13 reescrito · 2 novos padrões estruturais de produto adicionados aos 4 já existentes · total 6 padrões formalizados
GLOSSARIO §10 ampliado · entradas canônicas para cada um dos 7 padrões formalizados (nome, abreviação quando aplicável, enunciado resumido, aplicações, referência canônica ao D-XXX)
GLOSSARIO §11 anti-glossário · "Dados Brutos Processados" formalmente rejeitado em favor do padrão BAD
Método TabloFlow ganha vocabulário operacional · Arquiteto, Claude Code e ChatGPT consultam padrões por nome canônico
G-FUND recebe input mais firme · 7 padrões formalizados consumidos como requisitos nomeados
Fase 2 recebe padronização a priori · S-V2 aplica os 7 padrões com base nominal declarada
Retroação para V2/V1/V11 · Coração Visual dessas 3 visões declarado formalmente nas Specs S-V2, S-V1, S-V11 (candidatos: Matriz de Confronto V2 · Mapa de Conciliação V1 · Mapa de Aderência V11)
Padrão "default declarado" D-024 permanece como derivado informal citado no rationale de D-122 e D-123 · formalização adicional fica disponível como candidato futuro

Sessão de Alinhamento · status: Item 1 (retrospectiva) concluído · Item 2 (estado consolidado) concluído · Item 3 (formalização) concluído com D-122 a D-129 · Item 4 (plano operacional Fase 1) concluído · Item 5 (pontos de atenção) concluído · questões convergentes da Usuária resolvidas em D-130 (IA), D-131 (didática Fase 1), D-132 (dashboard).

Próximo bloco operacional após esta sessão: G-FUND (abertura · consumindo 7 padrões formalizados + 11 DCVs aprovados + receptividade a IA declarada + padrão de condução D-131 aplicado).

Referência canônica: CONTEXT §9 Camada C · §13 · GLOSSARIO §10 · §11 · D-122 a D-128 (decisões componentes desta formalização) · D-130 · D-131 · D-132 (decisões convergentes desta sessão)

## D-128 — Padrão 7 · Escala de Cardinalidade em Eixos com Patamares Numerados
Data: 2026-04-20 · Bloco: Sessão de Alinhamento Fase 0 → Fase 1 · Status: Fechada
Contexto: 5 aplicações com variações adaptativas (V7 hierárquica-aditiva · V8 multiplicativa · V9 multi-eixo independente ortogonal · V5 multi-eixo independente alinhada com V9 · V6 bivariada simultânea com produto da matriz como eixo V6-específico). Cada aplicação adaptada via D-073 à natureza analítica específica · padrão meta-adaptativo. Formalizado nesta sessão via Opção A.
Nome canônico: Escala de Cardinalidade com Patamares (abreviação: ECP)
Enunciado: Toda visão declara uma escala de cardinalidade em 3+ eixos de cardinalidade relevantes à sua natureza analítica, cada eixo estruturado em patamares numerados sequencialmente no formato P1 normal · P2 alerta leve · P3 alerta forte · P4 bloqueio escapável. Cada patamar tem faixa numérica declarada e comportamento declarado (sem alerta · warning informativo · warning estrutural · bloqueio B-VN-CARDINALIDADE com escape). A estrutura adaptativa dos eixos é justificada via D-073 (hierárquica · multiplicativa · multi-eixo independente · bivariada simultânea · outras) conforme a natureza analítica da visão. Nenhuma visão herda cegamente a estrutura de eixos de outra visão · cada declaração é ato de design que afirma a natureza analítica da visão.
Rationale: O padrão é meta-adaptativo · declara a estrutura (3+ eixos · patamares numerados · P1-P4 · adaptação D-073 obrigatória) mas não o comportamento concreto (que varia por visão). Elimina risco de visão sem previsão de comportamento em cardinalidade extrema. Força cada visão a se posicionar conscientemente sobre sua natureza analítica.
Escopo de aplicação: Todas as visões que processam volume significativo de dados (todas as 11). Formalização como regra de método em §9 Camada C com estrutura adaptativa declarada.
Relação com princípios existentes: Meta-padrão · aplicação estrutural de D-073 (herança adaptada à natureza analítica). Deriva de C.1 (determinismo absoluto · cardinalidade afeta performance que afeta determinismo em volumes extremos). Conecta-se com D-127 "Matriz de Bloqueios Operacionais" · patamar P4 materializa-se como bloqueio B-VN-CARDINALIDADE-EXTREMA escapável. Conecta-se com diretrizes de performance declaradas por visão.
Aplicações consolidadas na Fase 0: 5 com estruturas distintas · V7 hierárquica-aditiva · V8 multiplicativa · V9 multi-eixo independente ortogonal · V5 multi-eixo independente ortogonal alinhado com V9 · V6 bivariada simultânea com produto da matriz como eixo V6-específico.
Exceções permitidas (adaptações via D-073): Estrutura dos eixos varia por visão (adaptação é obrigatória, não opcional) · número mínimo de eixos = 3 · sem máximo declarado · faixas numéricas dos patamares variam por eixo e por visão · número de patamares P1-P4 é padrão · variações (3 · 5 patamares) permitidas com justificativa.
Impacto no método:
G-FUND · motor_base registra cardinalidade dos eixos como metadado estrutural disponível para cada visão · column_meta.cardinalidade: int · base_meta.n_linhas: int · métricas derivadas calculadas uma vez no upload
Fase 2 · Spec de cada visão (S-VN) inclui seção dedicada à Escala de Cardinalidade com os 3+ eixos declarados, patamares P1-P4, comportamento por patamar
Testes por visão cobrem cardinalidade em cada patamar
Wireframe funcional inclui microcopy de explicação da cardinalidade em interface
Referência canônica: CONTEXT §9 Camada C · GLOSSARIO §10 (Padrões consolidados · entrada "Escala de Cardinalidade com Patamares")

## D-127 — Padrão 6 · Matriz de Bloqueios Operacionais Numerados
Data: 2026-04-20 · Bloco: Sessão de Alinhamento Fase 0 → Fase 1 · Status: Fechada
Contexto: 5 aplicações consecutivas (V7 §8.1 · V8 §8 · V9 §7 · V5 §7 · V6 §7 D-120) cristalizaram padrão estrutural de declaração de bloqueios operacionais numerados por visão. Formalizado nesta sessão via Opção A.
Nome canônico: Matriz de Bloqueios Operacionais (abreviação: MBO)
Enunciado: Toda visão declara uma matriz de bloqueios operacionais estruturais numerados no formato B-VN-NOME em seção dedicada do DCV e da Spec. Cada bloqueio declara: (a) condição estrutural que o aciona (verificável deterministicamente sobre a base recebida), (b) comportamento padrão (recusa de execução), (c) se é escapável (usuário confirma execução sob responsabilidade, com warning específico) ou não-escapável (recusa absoluta, execução impossível), (d) microcopy de explicação ao usuário, (e) warning associado quando escape é acionado. Nenhum comportamento de caso-limite pode ser inventado pelo motor em tempo de execução · se situação estrutural não está coberta por bloqueio declarado nem por comportamento normal declarado, a visão não é implementada até que o DCV cubra.
Rationale: O padrão deriva de C.3 (sem invenção de comportamento). Elimina o risco de motor tomar decisão silenciosa em caso-limite · ou há comportamento declarado, ou há bloqueio declarado · não há terceira opção. A numeração sequencial B-VN-NOME torna cada bloqueio rastreável em spec, código, warnings e testes. Escape explícito preserva autonomia do usuário sem violar C.5.
Escopo de aplicação: Todas as 11 visões. Formalização como regra de método em §9 Camada C.
Relação com princípios existentes: Deriva de C.3 (sem invenção de comportamento). Reforça B.2 (wireframe funcional · bloqueios são visíveis em interface). Conecta-se com T-DIAG (bloqueios acionados entram no Diagnóstico) e com D-123 "Thresholds Editáveis" (alguns bloqueios têm thresholds editáveis).
Aplicações consolidadas na Fase 0: 5 consecutivas · V7 §8.1 · V8 §8 · V9 §7 · V5 §7 (12 bloqueios) · V6 §7 D-120 (13 bloqueios).
Padrão de nomenclatura: B-VN-DESCRITOR onde VN é o código da visão (V2, V3, ..., V11) e DESCRITOR é o nome canônico do bloqueio em UPPERCASE com hífen. Exemplos reais da Fase 0: B-V5-CAMPO-PRINCIPAL-NAO-NUMERICO · B-V6-EIXOS-IGUAIS · B-V8-BASE-VAZIA · B-V9-MINIMO-OPERACIONAL.
Exceções permitidas (adaptações via D-073): Número de bloqueios varia por natureza analítica da visão (V7 = 6 · V5 = 12 · V6 = 13) · sem mínimo ou máximo universal. Proporção escapáveis × não-escapáveis varia por visão. Estrutura adicional (classes especiais · situações excepcionais · V6 declara 43 warnings totais) é permitida como extensão honesta · matriz de bloqueios é o núcleo.
Impacto no método:
G-FUND · motor_base e contratos consomem este padrão · MotorResult suporta campo bloqueios_acionados: list[str] com rastreabilidade · contrato de warnings distingue bloqueio acionado (recusa) × bloqueio com escape acionado (execução + warning)
Fase 2 · Spec de cada visão (S-VN) inclui seção §7 ou §8 dedicada à Matriz de Bloqueios Operacionais · pré-validação estrutural implementada antes do cálculo analítico · testes cobrem cada bloqueio
Wireframe funcional inclui microcopy de explicação de cada bloqueio visível em interface
Warnings · B-VN-NOME com escape acionado gera warning W-VN-NOME-ESCAPE (estrutural, registrado no Diagnóstico)
Referência canônica: CONTEXT §9 Camada C · GLOSSARIO §10 (Padrões consolidados · entrada "Matriz de Bloqueios Operacionais")

## D-126 — Padrão 5 · Coração Visual da Visão (padrão estrutural de produto)
Data: 2026-04-20 · Bloco: Sessão de Alinhamento Fase 0 → Fase 1 · Status: Fechada
Contexto: 7 aplicações consecutivas (V4 Composição Principal · V7 Mapa de Grupos · V8 Matriz de Presença · V9 Mapa de Perfil · V5 Mapa de Distribuição · V10 Curva Pareto · V6 Matriz de Cruzamento) cristalizaram padrão de que cada visão declara uma aba Excel dedicada como materialização visual da contribuição analítica primária. Formalizado nesta sessão via Opção A.
Nome canônico: Coração Visual da Visão
Enunciado: Toda visão declara uma aba da exportação Excel como Coração Visual · a aba que materializa visualmente a contribuição analítica primária da visão em formato gráfico ou matricial adequado à natureza analítica. Esta aba é obrigatória, nomeada conforme a identidade da visão ("Matriz de Presença", "Mapa de Grupos", "Curva Pareto", etc.), e contém o ativo visual primário (gráfico nativo Excel, tabela matricial formatada, ou combinação) que o usuário abre primeiro depois do Resumo Executivo para ler o conteúdo analítico em forma visual.
Rationale: O padrão é estrutura de produto. Entrega ao usuário um ponto focal visual por visão · depois de ler o Resumo Executivo (narrativa), o Coração Visual entrega a leitura estrutural em forma gráfica/matricial. Força cada visão a responder concretamente "qual é o ativo visual primário desta visão?" durante a Fase 0, evitando que a Fase 2 produza aba "Gráficos" genérica que não casa com a natureza analítica.
Escopo de aplicação: Todas as 11 visões. Formalização como padrão estrutural de produto · vive em CONTEXT §13 junto com os 4 padrões já formalizados e com D-125.
Relação com princípios existentes: Padrão estrutural de produto (§13). Deriva de C.2 (nada silencioso · o conteúdo analítico primário tem materialização visual dedicada) + B.2 (wireframe funcional declara a forma do Coração Visual). Conecta-se com requisitos específicos de exportacao.py por tipo de Coração Visual (BarChart para V5 · formatação condicional para V6 · LineChart para V8 · etc.).
Aplicações consolidadas na Fase 0: 7 consecutivas · V4 Composição Principal (barras + tabela) · V7 Mapa de Grupos (tabela com faixas formatadas) · V8 Matriz de Presença (matriz com formatação condicional) · V9 Mapa de Perfil (tabela multi-métrica com heatmap) · V5 Mapa de Distribuição (Histograma + tabela por faixas) · V10 Curva Pareto (barras + linha) · V6 Matriz de Cruzamento (matriz formatada + ColumnChart empilhado).
Retroação diferida · V1, V2 e V11 ainda sem Coração Visual declarado explicitamente (foram as 3 primeiras visões da Fase 0 · DCV-V2 formalizou estrutura Excel sem nomeação de coração visual porque padrão ainda não havia cristalizado). Declaração formal acontece na produção das Specs S-V2, S-V1, S-V11 (candidatos naturais: Matriz de Confronto para V2 · Mapa de Conciliação para V1 · Mapa de Aderência para V11).
Exceções permitidas (adaptações via D-073): Formato adaptado à natureza analítica (cada Coração Visual tem formato próprio · não há forma universal) · visões sem valor numérico primário (V2, V1, V11) podem ter Coração Visual em formato de matriz de resultado · limitações técnicas (V6 ColumnChart empilhado 100% como alternativa a heatmap real não suportado em openpyxl · D-118) resolvem-se via alternativa análoga declarada.
Impacto no método:
G-FUND · exportacao.py consome este padrão como requisito · cada aba de Coração Visual pode ter template específico com capabilities declaradas (BarChart com bins · formatação condicional de matriz · ColumnChart empilhado 100% · heatmap nativo via conditional_formatting · LineChart)
Fase 2 · Spec de cada visão (S-VN) declara formalmente o Coração Visual · nome da aba, formato, capabilities de exportacao.py consumidas, relação com outras abas
Retroação diferida · V2, V1, V11 ganham declaração formal de Coração Visual nas respectivas Specs S-VN
Princípio B.2 reforçado · wireframe funcional declara explicitamente o Coração Visual
Referência canônica: CONTEXT §13 (padrão estrutural de produto) · GLOSSARIO §10 (Padrões consolidados · entrada "Coração Visual da Visão")

## D-125 — Padrão 4 · Resumo Executivo em 6 Blocos Fixos (padrão estrutural de produto)
Data: 2026-04-20 · Bloco: Sessão de Alinhamento Fase 0 → Fase 1 · Status: Fechada
Contexto: 7 aplicações consecutivas (V4 · V3 · V8 · V7 · V9 · V5 · V6) do padrão cristalizado em D-044 (origem V4). Padrão aguardava formalização como padrão estrutural de produto em §13 desde V9 (5ª aplicação). Formalizado nesta sessão via Opção A.
Nome canônico: Resumo Executivo em 6 Blocos
Enunciado: Toda visão oferece um Resumo Executivo como primeira aba da exportação Excel, estruturado em 6 blocos fixos na seguinte ordem: Bloco 1 · Cabeçalho (metadados da execução · visão · data · modo · agrupadores · medida principal) · Bloco 2 · Números-âncora (contagens e totais estruturais da unidade analítica da visão) · Bloco 3 · Distribuição (como o conteúdo analítico se distribui pela taxonomia da visão) · Bloco 4 · Elementos destacados (o que o motor identificou como digno de atenção · top N por critério declarado) · Bloco 5 · Leitura qualitativa com síntese (classificação qualitativa do conjunto analisado · N leituras possíveis + 1 default · thresholds editáveis em Configurações avançadas) · Bloco 6 · Qualidade estrutural (warnings estruturais catalogados · ajustes do motor · integridade do dado analisado). Adaptações via D-073 permitidas quando a natureza analítica da visão exige sub-blocos dedicados ou reformulação de bloco, preservando a espinha de 6 blocos.
Rationale: O padrão é estrutura de produto, não regra operacional. Entrega previsibilidade ao usuário · independente de qual visão ele executa, sabe onde encontrar cada tipo de informação. Entrega narrativa analítica consistente · a sequência "cabeçalho → números → distribuição → destaques → leitura → qualidade" espelha como um analista lê qualquer relatório. Formalização em §13 equipara este padrão aos 4 já formalizados (Objetivo da Visão, Fluxo Progressivo, T-MODELO, View Especializada).
Escopo de aplicação: Todas as 11 visões. Formalização como padrão estrutural de produto, não regra de método · vive em CONTEXT §13.
Relação com princípios existentes: Padrão estrutural de produto (§13), não regra de método (§9). Consome padrão "Thresholds Editáveis Declarados" (D-123) no Bloco 5. Consome T-SEMA na ordem de apresentação quando aplicável (V2, V3, V7, V9). Adaptável via D-073.
Aplicações consolidadas na Fase 0: 7 consecutivas · V4 D-044 (origem · 5 leituras qualitativas) · V3 · V8 (Bloco 4 como "movimentações do intervalo") · V7 · V9 · V5 (Bloco 4 reformulado como "valores destacados" em 3 sub-blocos) · V6 (Bloco 4 com sub-bloco 4b dedicado a ausências destacadas).
Exceções permitidas (adaptações via D-073): Sub-bloco dedicado (Bloco X pode ganhar sub-bloco Xb quando a natureza analítica da visão expõe conteúdo primário que não cabe no bloco matriz · V6 Bloco 4b · ausências destacadas). Reformulação de bloco (Bloco X pode ser reformulado em múltiplos sub-blocos paralelos quando a unidade analítica da visão não é "elemento" rotulado · V5 Bloco 4 como "valores destacados" em 3 sub-blocos). Camadas no Bloco 2 (Bloco 2 pode ter 2 camadas de números-âncora quando a visão opera em múltiplos modos · V5 Modo Segmentado). Adaptações preservam a espinha de 6 blocos · supressão de bloco inteiro não é permitida.
Impacto no método:
G-FUND · exportacao.py consome este padrão como requisito de template · cada aba "Resumo Executivo" segue o esqueleto de 6 blocos
Fase 2 · Spec de cada visão (S-VN) declara o conteúdo específico de cada bloco · wireframe funcional inclui Resumo Executivo como aba obrigatória
Consumo de outros padrões · Bloco 5 consome D-123 (thresholds editáveis) · Bloco 6 consome D-124 (rastreabilidade via Diagnóstico)
Referência canônica: CONTEXT §13 (padrão estrutural de produto) · GLOSSARIO §10 (Padrões consolidados · entrada "Resumo Executivo em 6 Blocos")

## D-124 — Padrão 3 · Base Analítica e Diagnóstico (BAD) · substitui aba Dados Brutos Processados
Data: 2026-04-20 · Bloco: Sessão de Alinhamento Fase 0 → Fase 1 · Status: Fechada
Contexto: 5 aplicações consecutivas (V8 D-078 · V7 D-089 · V9 D-099 · V5 D-108 · V6 D-119) cristalizaram padrão estrutural de exportação Excel que descarta sistematicamente a aba "Dados Brutos Processados" proposta em vários prévios. Formalizado nesta sessão via Opção A.
Nome canônico: Base Analítica e Diagnóstico (abreviação: BAD)
Enunciado: A exportação Excel de toda visão substitui a aba "Dados Brutos Processados" (cópia dos dados originais com classificações anexadas) por duas abas separadas de papel distinto: Base Analítica (1 linha por unidade analítica consolidada da visão · elemento · célula · observação · com todas as classificações e atributos derivados) e Diagnóstico (sempre última aba · D-017 · contagens estruturais agregadas, ajustes do motor, warnings catalogados, rastreabilidade de transformações). A rastreabilidade dos dados originais vive no Diagnóstico como contagens estruturais, não como cópia linha-a-linha.
Rationale: O padrão deriva de C.2 (nada silencioso · toda transformação aparece no diagnóstico) combinado com economia de exportação. Abas "Dados Brutos Processados" em bases volumosas tornam o arquivo Excel gigante e redundante (o usuário já tem o arquivo original). Base Analítica entrega o grão analítico real da visão (pós-consolidação T-AGRUPA, pós-classificação) · Diagnóstico entrega auditoria estrutural agregada. Juntos substituem a aba redundante.
Escopo de aplicação: Toda visão com aba Diagnóstico (todas as 11).
Relação com princípios existentes: Deriva de C.2 (nada silencioso) + economia de exportação. Reforça regra D-017 (Diagnóstico sempre como última aba). Conecta-se com T-DIAG (contrato de Diagnóstico consome este padrão).
Aplicações consolidadas na Fase 0: 5 consecutivas · V8 D-078 (origem) · V7 D-089 · V9 D-099 · V5 D-108 · V6 D-119. Cada aplicação adapta "unidade analítica" à natureza da visão · V8 = entidade × ponto do eixo · V7 = elemento · V9 = identificador · V5 = observação válida · V6 = célula da matriz (presente ou ausente).
Exceções permitidas: Nenhuma exceção estrutural conhecida na Fase 0. Visões de confronto V1 e V11 preservam registros individuais · mas isso não conflita com o padrão, porque "preservar registros individuais" é o papel da Base Analítica de V1/V11 (cada linha é um match ou não-match com suas classificações).
Impacto no método:
G-FUND · exportacao.py consome este padrão como requisito de template · estrutura de abas padrão: Resumo Executivo + coração visual + abas analíticas específicas + Base Analítica + Parâmetros + Diagnóstico (última)
Fase 2 · Spec de cada visão (S-VN) declara estrutura de Base Analítica (colunas, 1 linha por quê) e seções do Diagnóstico (categorias de ajuste, warnings aplicáveis)
Eliminação formal · aba "Dados Brutos Processados" proposta em prévios entra no anti-glossário geral (termo rejeitado em favor do padrão BAD)
Referência canônica: CONTEXT §9 Camada C · GLOSSARIO §10 (Padrões consolidados · entrada "Base Analítica e Diagnóstico") · GLOSSARIO §11 anti-glossário (termo "Dados Brutos Processados" rejeitado)

## D-123 — Padrão 2 · Thresholds Editáveis Declarados (TED) em Configurações avançadas
Data: 2026-04-20 · Bloco: Sessão de Alinhamento Fase 0 → Fase 1 · Status: Fechada
Contexto: 6 aplicações consecutivas (V4 D-040 · V7 D-084 + D-089 · V8 D-078 · V9 D-097/D-098 · V5 D-104 · V6 D-116) cristalizaram padrão estrutural de apresentação e persistência de parâmetros numéricos operacionais. Formalizado nesta sessão via Opção A.
Nome canônico: Thresholds Editáveis Declarados (abreviação: TED)
Enunciado: Todo parâmetro numérico operacional de uma visão (limiar de classificação, faixa de leitura, critério de outlier, threshold de densidade, tolerância, corte) aparece como default declarado visível na configuração da visão antes da execução, é editável em painel de "Configurações avançadas" com granularidade camada-por-camada, e é persistido em T-MODELO junto com a configuração da visão. Defaults silenciosos no motor (revelados apenas no diagnóstico pós-execução) não são permitidos.
Rationale: Deriva de C.5 (TabloFlow analisa sobre o dado informado, nunca decide por ele) combinado com o derivado "default declarado" D-024. Elimina decisão analítica tomada pelo motor sem visibilidade · usuário recebe uma classificação sem saber que o threshold era X em vez de Y. A camada editável permite que o motor proponha defaults razoáveis (economia cognitiva do usuário) sem transferir a decisão analítica para o motor.
Escopo de aplicação: Toda visão com parâmetros numéricos operacionais. Cobre todas as 11 visões em alguma dimensão (mesmo V2/V1/V11 com tolerâncias).
Relação com princípios existentes: Deriva de C.5 + derivado "default declarado" D-024. Conecta-se com T-MODELO (persistência obrigatória dos thresholds editados). Padrão de UX consolidado · afeta wireframe funcional de toda visão.
Aplicações consolidadas na Fase 0: 6 consecutivas · V4 D-040 (origem · limiares ABC) · V7 D-084 + D-089 (faixas de desvio) · V8 D-078 (thresholds de leitura qualitativa) · V9 D-097/D-098 (faixas multi-métrica) · V5 D-104 (3 critérios de outlier com defaults por critério) · V6 D-116 (3 thresholds de densidade + 6 thresholds no Resumo Executivo).
Exceções permitidas: Nenhuma exceção estrutural conhecida na Fase 0. Thresholds com valor fixo por razão matemática (ex: tolerância 1e-9 em T-RANK para floating point) não entram neste padrão · são constantes de implementação, não parâmetros operacionais.
Impacto no método:
G-FUND · T-MODELO como transversal da Fundação consome este padrão · contrato de serialização precisa suportar thresholds por visão com tipagem declarada (faixa numérica × enum × string)
Fase 2 · Spec de cada visão (S-VN) declara todos os thresholds operacionais com default + faixa válida + warning quando editado · wireframe funcional inclui painel de Configurações avançadas como elemento obrigatório
Warning transversal consolidado · W-VIEW-LEITURA-DEFAULT (aceitação do default) + W-VIEW-LEITURA-CUSTOM (edição pelo usuário · registra valor aplicado para auditoria)
Referência canônica: CONTEXT §9 Camada C · GLOSSARIO §10 (Padrões consolidados · entrada "Thresholds Editáveis Declarados")

## D-122 — Padrão 1 · Consolidação Pré-Cálculo Obrigatória (CPCO) com blindagem contra dupla agregação
Data: 2026-04-20 · Bloco: Sessão de Alinhamento Fase 0 → Fase 1 · Status: Fechada
Contexto: 5 aplicações consecutivas (V8 D-074 · V7 D-082 · V9 D-092 · V5 D-102 com adaptação V5-específica · V6 D-111 com consumo padrão) cristalizaram padrão estrutural. Padrão aguardava formalização efetiva desde V8 (24h depois de sua cristalização). Formalizado nesta sessão via Opção A.
Nome canônico: Consolidação Pré-Cálculo Obrigatória (abreviação: CPCO)
Enunciado: Toda visão que opera sobre valores consolidáveis declara explicitamente o modo da base (Transacional × Pré-agregado × outros modos específicos da visão) antes do cálculo analítico. T-AGRUPA é invocada obrigatoriamente · operando consolidação real no modo Transacional, ou operando em no-op validado no modo Pré-agregado (verifica unicidade de chave e gera warning estrutural se duplicada). Nenhum cálculo analítico sobre valores ocorre sem essa declaração explícita e sem essa invocação obrigatória.
Rationale: Deriva de C.2 (nada silencioso) combinado com C.5 (default declarado do modo da base). Elimina dupla agregação invisível · base já consolidada sendo consolidada de novo pela visão, produzindo resultado numericamente correto mas semanticamente errado. A blindagem via no-op validado em Pré-agregado torna o comportamento explícito e auditável.
Escopo de aplicação: Toda visão que opera sobre valores consolidáveis. Cobre 9 das 11 visões (todas exceto V1 e V11, que preservam registros individuais em vez de consolidar).
Relação com princípios existentes: Deriva de C.2 + C.5. Reforça padrão "default declarado" D-024. Pode ser adaptado via D-073 (herança adaptada à natureza analítica) · caso canônico · V5 nunca consolida valores, apenas valida chave ou particiona (D-102).
Aplicações consolidadas na Fase 0: 5 consecutivas · V8 D-074 (origem) · V7 D-082 · V9 D-092 · V5 D-102 com adaptação V5-específica em 3 modos · V6 D-111 com consumo padrão (reforça tronco comum).
Exceções permitidas: Adaptação via D-073 quando a natureza analítica da visão torna a consolidação de valores incompatível com o método analítico (caso V5). A adaptação preserva a estrutura do padrão (declaração explícita do modo · validação · T-AGRUPA invocada · diagnóstico) sem preservar o comportamento de consolidar valores. Adaptações futuras devem ser justificadas via D-XXX específico com rationale analítico.
Impacto no método:
G-FUND · T-AGRUPA como transversal da Fundação consome este padrão como requisito · contrato precisa suportar modo Transacional + modo no-op validado + extensões já declaradas (V9 multi-regra por métrica · V5 3 modos V5-específicos · V7 média ponderada opcional)
Fase 2 · Spec de cada visão (S-VN) declara explicitamente modo da base e invocação de T-AGRUPA no contrato lógico · seção obrigatória do wireframe funcional: escolha explícita de modo com default declarado editável em um clique
Warning transversal consolidado · W-VIEW-MODO-INFERIDO (informativo, default aceito) + W-VIEW-CHAVE-NAO-UNICA (estrutural, duplicidade detectada em Pré-agregado)
Referência canônica: CONTEXT §9 Camada C · GLOSSARIO §10 (Padrões consolidados · entrada "Consolidação Pré-Cálculo Obrigatória")

## D-121 — Sumário do refino DCV-V6 · 16 pendências fechadas em sessão única · Família E fechada · Fase 0 CONCLUÍDA
Data: 2026-04-20 · Bloco: DCV-V6 (sessão única) · Status: Fechada
Contexto: Refino DCV-V6 executado em sessão única (20/04/2026) seguindo padrão D-019 + D-034 + D-033. 16 pendências originais trabalhadas (T-01 a T-16 · Bloco A · posicionamento + Bloco B · entrada + Bloco C · cálculo + Bloco D · saída), todas fechadas, nenhuma deferida. Padrão de condução D-019 aplicado integralmente: ritual de abertura com leitura dos 4 documentos canônicos + 4 DCVs anexados (prévio V6 · V5 V8 V4 aprovados), fila racionalizada em 4 blocos, uma pendência por vez com opções explícitas e C.5 como primeira lente, mini status-checks a cada ~3 pendências, sinalização de densidade D-034 no 3º status-check com recomendação de continuar em sessão única (aprovada pela Usuária). Ao final, a Usuária solicitou sessão intermediária de alinhamento técnico Fase 0 → Fase 1 antes de abrir o G-FUND.
Decisão: DCV-V6 refinado. Consolida 16 pendências estruturais com 10 decisões específicas (D-111 a D-120) mais esta (D-121) como sumário + fechamento da Família E + fechamento da Fase 0. Família E · Estrutura interna do recorte fechada com par autônomo distante confirmado dos dois lados (V5 §2.3 lado 1 por D-110 · V6 §2.3 lado 2 por D-121). **Fase 0 · Compreensão CONCLUÍDA** com 11 de 11 DCVs aprovados (V2 · V1 · V11 · V4 · V10 · V3 · V8 · V7 · V9 · V5 · V6). Próximo bloco operacional: **Sessão de Alinhamento Técnico Fase 0 → Fase 1** (antes do G-FUND · decisão da Usuária em 20/04/2026 · bloco próprio sem prefixo G-*, F-*, S-*).
10 decisões consolidadas do refino:
#TemaReferênciaT-01§2.3 simétrico a V5 · convivência Família E sem retroação diferida formalD-121 · dcv_v6.md §2.3 · CONTEXT §4 · GLOSSARIO §1T-02Fronteiras V6×V4 · V6×V10 · V6×V8 · V6×V7/V9 em prosa declarativa autossuficientedcv_v6.md §2.2 (aplicação de padrão D-076 + D-073 · não gera D-XXX)T-03Vocabulário canônico V6 (~24 termos em 5 categorias) + vocabulário dual 6 pares + anti-glossário 6 termosdcv_v6.md §13 · GLOSSARIO seção 5.V6 nova · §11 anti-glossárioT-04Modo da base V6 em 2 modos canônicos + T-AGRUPA 9ª consumidora com consumo padrão + multi-aba em roadmapD-111 · dcv_v6.md §4.1 · §4.2 · §4.3T-05Tipos de medida V6 · separação tipo de campo × regra de agregação · 5 tipos + 3 regras MVP + subtipo ID herdado + Booleano condicional + Estado bloqueadoD-112 · dcv_v6.md §4.4T-06Classificação categórico-elegível no motor_base como metadado estrutural (requisito novo G-FUND) + escala de cardinalidade individual 4 patamaresD-113 · dcv_v6.md §4.5T-07Estrutura POR_COLUNAS no MVP · POR_LINHAS em roadmap · multi-aba com escolha explícita · empilhamento via M2.STACK futurosem D-XXX · ratificação T-04/T-06T-08Unidade analítica V6 = célula da matriz + produto cartesiano observado restrito + classificação estrutural Presente × Ausente + Base Analítica 1 linha por célulaD-114 · dcv_v6.md §2.5 · §4.7T-09V6 como 8ª consumidora de T-RANK · regra V6-específica 4 níveis · separação ordenação de cálculo × exibição · Participação null em ausentesD-115 · dcv_v6.md §5.3 · §5.4 · §5.9T-10Taxonomia oficial V6 · 3 classes primárias de densidade com vocabulário dual + 2 especiais paralelas + 1 atributo derivado + 3 thresholds editáveisD-116 · dcv_v6.md §5.5 · §5.6T-11Resumo Executivo V6 em 6 blocos fixos · 7ª aplicação consecutiva D-044 · 6 defaults editáveis no ResumoD-117 · dcv_v6.md §5.7T-12Matriz de Cruzamento como coração visual V6 · 7ª aplicação consecutiva do padrão coração visual · requisito novo para exportacao.pyD-118 · dcv_v6.md §5.8 · §5.9T-13Estrutura Excel V6 · 7 abas fixas + Combinações Ausentes dedicada + Dados Brutos descartada (5ª aplicação)D-119 · dcv_v6.md §5.10 · §5.11T-1413 bloqueios operacionais + escala de cardinalidade em 3 eixos com produto da matriz como eixo V6-específico + 9 diretrizes de performanceD-120 · dcv_v6.md §7 · §8T-15Roadmap pós-MVP com 11 candidatos P-V6-XX-Evo + anti-roadmap com 4 itensdcv_v6.md §9 · §9.1 (consolidação · não gera D-XXX)T-16Consolidação de 43 warnings + bloqueios (13 B + 8 estruturais + 5 permanentes + 17 informativos)dcv_v6.md §10
Razão: (1) Sessão única validou pela 7ª vez consecutiva (V10 · V3 · V8 · V7 · V9 · V5 · V6) que refino denso pode caber em uma sessão quando o prévio é maduro (V6 tinha Partes 0-16 já normativas · apenas precisando formalização no padrão TabloFlow) e a maioria das pendências herda padrões consolidados pós-D-073. (2) Família E fechada em Fase 0 com 2 visões aprovadas (V5 e V6) · par autônomo operacionalmente distante confirmado dos dois lados. Adaptação D-073 ao método de posicionamento de família validada pela segunda vez (V5 D-110 lado 1 · V6 §2.3 lado 2). (3) Fase 0 · Compreensão fechada com 11 de 11 DCVs aprovados. Módulo 1 tem compreensão consolidada e aprovada pela Usuária. (4) 7 padrões consolidados atingem aplicações muito fortes com esta sessão · prontos para formalização efetiva no próximo ajuste estrutural do CONTEXT: padrão "consolidação obrigatória pré-cálculo" · 5 aplicações consecutivas (V8 D-074 · V7 D-082 · V9 D-092 · V5 D-102 · V6 D-111); padrão "thresholds multi-camada editáveis" · 6 aplicações consecutivas (V4 D-040 · V7 D-084 · V8 D-078 · V9 D-097 · V5 D-104 · V6 D-116); padrão "Dados Brutos descartada" · 5 aplicações consecutivas (V8 D-078 · V7 D-089 · V9 D-099 · V5 D-108 · V6 D-119); padrão "Resumo Executivo em 6 blocos fixos" D-044 · 7 aplicações consecutivas (V4 · V3 · V8 · V7 · V9 · V5 · V6) · candidato muito forte à formalização em CONTEXT §13 como padrão estrutural de produto; padrão "coração visual da visão" · 7 aplicações consecutivas (V4 · V7 · V8 · V9 · V5 · V10 · V6); padrão "matriz de bloqueios numerados" · 5 aplicações consecutivas (V7 · V8 · V9 · V5 · V6); padrão "escala de cardinalidade em eixos com patamares numerados" · 5 aplicações (V7 hierárquica · V8 multiplicativa · V9/V5 multi-eixo independente · V6 bivariada simultânea). (5) Padrão "herança adaptada à natureza analítica" D-073 ganha 5 novas aplicações documentadas com V6 · atinge ~15 aplicações totais · padrão meta-adaptativo cristalizado do método TabloFlow. (6) 3 requisitos novos para Fundação consolidados em V6: motor_base com metadado `column_meta.tipo_estrutural` (5 valores enum · D-113); exportacao.py com formatação condicional de matriz + ColumnChart empilhado 100% + paginação de matriz grande (D-118); exportacao.py com Combinações Ausentes como aba dedicada em template V6 (D-119). Nenhum é requisito disruptivo · todos extensões incrementais coerentes com requisitos V5 (motor_upload subtipo ID) e V8 (streaming para matriz · paginação). (7) M2.STACK (D-063) ganha V6 como 3º consumidor futuro declarado (P-V6-02-MULTIABA-Evo) · pressão significativa no G-FUND para posicionamento definitivo. (8) Kit D-033 completo em sessão única validado pela 7ª vez consecutiva · padrão de método TabloFlow estabilizado.
Impacto:

11 de 11 DCVs aprovados na Fase 0 → **Fase 0 · Compreensão CONCLUÍDA**
Fila remanescente Fase 0 · vazia · fechamento da fase
Família E · Estrutura interna do recorte com as duas visões aprovadas · par autônomo distante fechado dos dois lados
43 warnings V6 catalogados · maior volume do projeto (V3=27 · V7=35 · V8=37 · V5=37 · V9=40 · V6=43)
T-AGRUPA ganha V6 como 9ª consumidora com consumo padrão (não adaptação V5-específica) · contrato sem extensão nova · reforço do tronco comum da família V4/V7/V8/V9
T-RANK ganha V6 como 8ª consumidora com regra V6-específica 4 níveis · contrato sem extensão nova
7 padrões consolidados prontos para formalização efetiva · decisão de formalizar via D-XXX dedicados ou ajuste estrutural do CONTEXT fica para Sessão de Alinhamento Fase 0 → Fase 1
Padrão D-073 atinge ~15 aplicações documentadas · padrão meta-adaptativo cristalizado
Próximo bloco: **Sessão de Alinhamento Técnico Fase 0 → Fase 1** (antes de G-FUND)

Referência canônica: /specs/dcv/dcv_v6.md · D-111 a D-120 · CONTEXT §3 Fase 0 marcada como CONCLUÍDA · §4 Família E fechada · §6 T-AGRUPA (V6 9ª consumidora) · §6 T-RANK (V6 8ª consumidora) · §9 Camada C com 7 padrões consolidados prontos para formalização · GLOSSARIO §1 Fase 0 · §4 T-AGRUPA · §4 T-RANK · seção 5.V6 nova · §6 Warnings V6 · §11 anti-glossário V6.

## D-120 — Bloqueios operacionais V6 + escala de cardinalidade em 3 eixos com produto da matriz como eixo V6-específico + 9 diretrizes de performance
Data: 2026-04-20 · Bloco: DCV-V6 (sessão única) · Status: Fechada
Contexto: Prévio V6 §12 lista 6 "alertas e observações não bloqueantes" em linguagem genérica sem matriz de bloqueios estruturais numerados e sem patamares operacionais como V7 §8.1 · V8 §8 · V9 §7 · V5 §7/§8 têm. Precisa consolidar bloqueios, cardinalidade e performance em formato padronizado. Refino T-14 consolidou os 3 sub-temas.
Decisão: DCV-V6 §7 declara 13 bloqueios operacionais estruturais numerados (análogo V7/V8/V9/V5): B-V6-EIXO-NUMERICO-CONTINUO (escapável) · B-V6-EIXO-VAZIO-OU-AMBIGUO · B-V6-EIXO-CARDINALIDADE-EXCESSO (escapável) · B-V6-EIXOS-IGUAIS · B-V6-MEDIDA-ID (escapável) · B-V6-BOOLEANO-COM-SOMA-OU-MEDIA · B-V6-ESTADO-COMO-MEDIDA · B-V6-POR-LINHAS · B-V6-MATRIZ-CARDINALIDADE-EXTREMA (escapável) · B-V6-MATRIZ-VAZIA · B-V6-MEDIDA-NUMERICA-AUSENTE · B-V6-MOTOR-INFERIU-TIPO-INCOMPATIVEL · B-V6-MINIMO-OPERACIONAL. §8 declara escala de cardinalidade em 3 eixos independentes (aplicação D-073 ao método de escala · natureza bivariada simultânea · diferente de V5 multi-eixo independente ortogonal · diferente de V7 hierárquica-aditiva · diferente de V8 multiplicativa): Eixo 1 · Cardinalidade de Eixo 1 em 4 patamares (P1 2-30 · P2 31-100 · P3 101-200 · P4 >200 escapável); Eixo 2 · Cardinalidade de Eixo 2 patamares idênticos · independente; Eixo 3 · Cardinalidade da Matriz (produto N × M · eixo estrutural V6-específico) em 4 patamares (P1 ≤ 900 · P2 901-2.500 · P3 2.501-10.000 · P4 > 10.000 escapável). §8.4 declara 9 diretrizes de performance (7 herdadas V3/V7/V8/V9/V5 + 2 específicas V6: cálculo do produto cartesiano observado em passe único após consolidação T-AGRUPA · detecção de células ausentes via complemento matemático |V_Eixo1| × |V_Eixo2| − presentes · O(1) em vez de O(N×M) enumerativo).
Estrutura multi-eixo com produto da matriz como eixo V6-específico (aplicação D-073): V6 é distinta de V7 (hierárquica-aditiva: elementos dentro de grupos), V8 (matricial multiplicativa), V9/V5 (eixos ortogonais independentes). Em V6 os dois eixos individuais têm natureza independente mas a cardinalidade combinada (produto) forma um terceiro eixo estrutural próprio que escala multiplicativamente. Custo computacional escala como O(N log N) para ordenação + O(N) para varredura.
Razão: (1) Padrão de bloqueios numerados consolidado em V7/V8/V9/V5/V6 (5 aplicações · cada uma adaptada à natureza analítica). (2) Padrão de escalas de cardinalidade com patamares numerados consolidado em V7/V8/V9/V5/V6 (5 aplicações). (3) Variação nova em V6 (produto da matriz como eixo estrutural próprio) coerente com natureza bivariada · aplicação canônica D-073. (4) Diretrizes de performance como tronco comum (7 herdadas) + específicas V6 (2) reforça uniformidade + adaptação justificada. (5) Bloqueios estruturais numerados evitam que implementação invente comportamentos em casos-limite (C.3 honrado).
Impacto:

dcv_v6.md §7 (13 bloqueios) · §8 (escala 3 eixos · 9 diretrizes performance)
F-MOT (Fundação) recebe requisitos de 13 pré-validações estruturais V6
F-EXP (Fundação) recebe requisito de paginação de matriz grande (extensão requisito V8 streaming · 2ª aplicação após Matriz de Presença V8)
F-TRANS (Fundação) recebe requisito de ordenação O(N log N) reutilizada para ranking
Total de warnings V6 atinge 43 com esta pendência (13 bloqueios · 8 estruturais · 5 permanentes · 17 informativos · maior volume do projeto)
Padrão "escala de cardinalidade em eixos com patamares numerados" consolida com 5 aplicações (V7 hierárquico-aditiva · V8 multiplicativa · V9 multi-eixo independente · V5 multi-eixo independente alinhada com V9 · V6 bivariada simultânea com produto da matriz como eixo V6-específico) — cada aplicação adaptada via D-073 · padrão meta-adaptativo

Referência canônica: /specs/dcv/dcv_v6.md §7 · §8 · CONTEXT §9 Camada C (15ª aplicação D-073)

## D-119 — Estrutura Excel V6 · 7 abas fixas + Combinações Ausentes dedicada + "Dados Brutos Processados" descartada (5ª aplicação consecutiva)
Data: 2026-04-20 · Bloco: DCV-V6 (sessão única) · Status: Fechada
Contexto: Prévio V6 §10.2 propõe 4 abas (Matriz de Cruzamento · Ranking de Combinações · Combinações Ausentes · Dados Brutos Processados) sem Resumo Executivo separado · sem Parâmetros · sem Diagnóstico. Rompe com padrão consolidado de 6 abas padrão (Resumo · coração visual · Análise substantiva · Parâmetros · Base Analítica · Diagnóstico última aba por D-017) presente em V4 (6 abas) · V7 (6 abas) · V9 (6 abas) · V10 (6 abas) · V5 (6 abas) · V8 (7 abas) · V3 (7 abas). Refino T-13 alinhou V6 ao padrão consolidado preservando a especificidade (Combinações Ausentes como aba dedicada distintiva V6).
Decisão: DCV-V6 §5.10 declara estrutura Excel oficial V6 com 7 abas fixas (V6 MVP sem Modo Segmentado · portanto sem variação dinâmica por modo como V5/V8): (1) Resumo Executivo · (2) Matriz de Cruzamento · coração visual V6 · (3) Ranking de Combinações · (4) Combinações Ausentes · aba dedicada distintiva V6 · aplicação canônica D-076 cristalizada em aba própria · análoga à aba "Movimentações" específica V8 (D-078) · (5) Base Analítica · (6) Parâmetros · (7) Diagnóstico (sempre última · D-017). §5.11 declara aba "Dados Brutos Processados do prévio descartada" em favor de Base Analítica (1 linha por célula presente ou ausente · com classificações) + Diagnóstico (contagens estruturais agregadas).
5ª aplicação consecutiva do padrão "Dados Brutos descartada em favor de Base Analítica + Diagnóstico" (V8 D-078 · V7 D-089 · V9 D-099 · V5 D-108 · V6 D-119) → pronto para formalização efetiva no próximo ajuste do CONTEXT §9 Camada C.
Modo Segmentado V6 fica em roadmap P-V6-05-SEGMENTADO-Evo · permitiria aba "Resumo por Segmento" condicional (análogo V5 D-108) · fora do MVP.
Razão: (1) Regra D-017 (Diagnóstico sempre última aba) é transversal invariante — V6 não pode romper. (2) Resumo Executivo separado + Matriz de Cruzamento (coração visual) + Parâmetros + Base Analítica + Diagnóstico formam o "esqueleto padrão" que dá consistência cross-visão. (3) Combinações Ausentes como aba própria preserva especificidade V6 + cristaliza aplicação D-076 em aba dedicada · análoga à aba Movimentações V8. (4) Aba Dados Brutos seria redundante em V6 (Base Analítica já tem 1 linha por célula · Diagnóstico tem contagens estruturais) · 5ª aplicação consecutiva do padrão de descarte consolida-o como padrão de método pronto para formalização efetiva.
Impacto:

dcv_v6.md §5.10 (estrutura Excel) · §5.11 (Dados Brutos descartada)
F-EXP (Fundação) recebe requisito: template Excel V6 com aba "Combinações Ausentes" dedicada (análoga "Movimentações" V8)
CONTEXT §9 Camada C atualizada (padrão "Dados Brutos descartada" com 5ª aplicação consecutiva · pronto para formalização efetiva)

Referência canônica: /specs/dcv/dcv_v6.md §5.10 · §5.11 · CONTEXT §9 Camada C

## D-118 — Matriz de Cruzamento como coração visual V6 · 7ª aplicação consecutiva do padrão coração visual · requisito novo para exportacao.py da Fundação
Data: 2026-04-20 · Bloco: DCV-V6 (sessão única) · Status: Fechada
Contexto: Prévio V6 §10.3 lista Matriz de Cruzamento como Aba 1 do Excel com conteúdo mínimo ("tabela matricial · valor da medida por célula · formatação coerente com classificação"). Não declarada como coração visual · sem estrutura técnica explícita (paginação · gráfico nativo · formatação condicional · tratamento de matriz grande). Padrão consolidado pós-D-073 é cada visão ter uma aba declarada como "coração visual" que materializa visualmente a contribuição analítica primária (V8 Matriz de Presença · V7 Mapa de Grupos · V9 Mapa de Perfil · V5 Mapa de Distribuição · V4 Composição Principal · V10 Curva Pareto · 6 aplicações consecutivas). V6 precisa do seu coração visual. Refino T-12 identificou Matriz de Cruzamento como candidato natural.
Decisão: DCV-V6 §5.8 declara "Matriz de Cruzamento" como coração visual da V6 — aba dedicada com 4 componentes: (1) Tabela matricial principal · Eixo 1 nas linhas · Eixo 2 nas colunas · Valor da Medida em cada célula · células ausentes com marcador visual distinto ("—" ou fundo cinza-claro · honra D-023 V2 null ≠ 0) · formatação condicional por classe de densidade (Dominante verde-intenso · Relevante verde-médio · Residual cinza · Ausente fundo diferenciado · PRESENTE_SEM_VALOR amarelo claro) · (2) Totais marginais opcionais (linha de totais por coluna + coluna de totais por linha + canto total geral · default ligado editável em Configurações avançadas · 11ª aplicação do padrão "default declarado editável") · (3) Gráfico nativo Excel · ColumnChart empilhado 100% via openpyxl (heatmap nativo não suportado · ColumnChart é alternativa análoga ao Mapa de Perfil V9 · 1 série por valor de Eixo 2 · 1 categoria por valor de Eixo 1 · altura da barra representa total por Eixo 1 · empilhamento representa composição por Eixo 2 · permite leitura visual de concentração e assimetria por Eixo) · (4) Paginação automática quando matriz > 30×30 células (aprox. limite legível · paginar eixos em blocos de 20×20 com notas de navegação).
Heatmap real (quando openpyxl oferecer suporte nativo ou alternativa viável) fica em roadmap P-V6-06-HEATMAP-NATIVO-Evo.
Requisito novo para Fundação (G-FUND): exportacao.py ganha capability de tabela matricial com formatação condicional por valor de célula (regras derivadas de classificação) + ColumnChart empilhado 100% nativo Excel (já suportado · zero workaround) + paginação de matriz grande com numeração de blocos (extensão do requisito V8 de streaming para abas pesadas).
Razão: (1) Padrão "coração visual da visão" atinge 7 aplicações consecutivas (V4/V7/V8/V9/V5/V10/V6) · candidato muito forte à formalização em CONTEXT §13 como padrão estrutural de produto (análogo aos 4 já formalizados: Objetivo da Visão · Fluxo Progressivo · T-MODELO · View Especializada). (2) Matriz de Cruzamento é literalmente o objeto analítico primário V6 · coração visual natural. (3) ColumnChart empilhado 100% é alternativa pragmática ao heatmap nativo · permite comunicação visual de concentração e assimetria sem workaround técnico via openpyxl. (4) Formatação condicional por classe de densidade cria coerência visual direta com Base Analítica · zero divergência tela/Excel (princípio das 11 visões). (5) Paginação automática > 30×30 protege legibilidade em matrizes grandes. (6) Heatmap real em roadmap preserva o gancho para evolução quando biblioteca oferecer suporte.
Impacto:

dcv_v6.md §5.8 (coração visual · 4 componentes) · §5.9 (ordenação de exibição da matriz)
Requisito novo para Fundação (G-FUND): exportacao.py ganha capability de formatação condicional de matriz + ColumnChart empilhado 100% + paginação de matriz grande (extensão do requisito V8)
CONTEXT §9 Camada C atualizada (padrão "coração visual da visão" com 7ª aplicação consecutiva · pronto para formalização em §13 como padrão estrutural de produto)

Referência canônica: /specs/dcv/dcv_v6.md §5.8 · §5.9 · CONTEXT §9 Camada C · §13 (pronto para formalização)

## D-117 — Resumo Executivo V6 em 6 blocos fixos · adaptação D-073 do padrão D-044 · 7ª aplicação consecutiva
Data: 2026-04-20 · Bloco: DCV-V6 (sessão única) · Status: Fechada
Contexto: Prévio V6 não tem Resumo Executivo como aba própria no Excel. §9 declara apenas uma "análise em tela" com matriz + painel lateral com indicadores dispersos (total de combinações possíveis · top combinações · lista de ausentes). §10.2 lista as 4 abas oficiais como Matriz · Ranking · Ausentes · Dados Brutos — sem Resumo Executivo, sem Parâmetros, sem Diagnóstico. Rompe estruturalmente com padrão consolidado pós-D-044 (V4 · V3 · V8 · V7 · V9 · V5 · 6 aplicações consecutivas). V6 como 7ª aplicação consecutiva cristaliza o padrão como candidato muito forte à formalização em CONTEXT §13 como padrão estrutural de produto. Refino T-11 formalizou Resumo Executivo V6 em 6 blocos com adaptações D-073 honestas à natureza bivariada.
Decisão: DCV-V6 §5.7 declara Resumo Executivo V6 em 6 blocos fixos (aplicação D-044 · 7ª consecutiva):
Bloco 1 · Cabeçalho · identificação da execução V6. Conteúdo: nome analítico dos Eixos · Tipo de Medida + nome analítico da Medida · Campo Numérico (quando aplicável) · Modo da base · Cardinalidade de cada eixo e da matriz · Limiares ativos · Ordenação de exibição ativa · Timestamp · total de linhas processadas · total de linhas com nulo excluídas.
Bloco 2 · Números-âncora · 6 métricas-síntese da matriz (V6 MVP sem Modo Segmentado · adaptação V5 D-106 de 2 camadas não se aplica): N de células possíveis (|V_Eixo1| × |V_Eixo2|) · N de células presentes · N de células ausentes · Densidade da matriz (N presentes / N possíveis · %) · Concentração no topo (participação cumulativa das N% primeiras onde N = limiar Dominante default 20%) · Total da Medida (somatório sobre células presentes).
Bloco 3 · Distribuição · como células se distribuem em classes: distribuição por classe de densidade (% DOMINANTE · % RELEVANTE · % RESIDUAL sobre presentes) + distribuição estrutural (% PRESENTE · % AUSENTE · % PRESENTE_SEM_VALOR sobre total do produto cartesiano observado) + distribuição por Faixa de Participação.
Bloco 4 · Destaques da matriz · adaptação D-073 da estrutura V4/V7/V9 em 2 sub-blocos: Sub-bloco 4a · Top-N combinações presentes (default N=10 editável 1-50 · 10ª aplicação consecutiva do padrão "default declarado editável") com posição · Eixo1=X · Eixo2=Y · Valor · Participação · Acumulada · Classe; Sub-bloco 4b · Combinações ausentes destacadas ordenadas por (Total do Eixo1 + Total do Eixo2) decrescente (heurística: ausências em eixos "grandes" sinalizam lacunas analiticamente mais relevantes) · se > 50 · paginação ou top-50 com redirecionamento para aba Combinações Ausentes · se zero · frase "Matriz densa · zero combinações ausentes no produto cartesiano observado".
Bloco 5 · Leitura qualitativa com síntese · 5 leituras multi-aplicáveis + Equilibrada default: Concentrada (Concentração no topo ≥ 50%) · Dispersa (Densidade ≥ 75% AND Concentração no topo ≤ 25%) · Esparsa (Densidade ≤ 30%) · Assimétrica por Eixo (top-5 linhas ≥ 80% OR top-5 colunas ≥ 80%) · Com lacunas estruturais relevantes (≥ 20% de células ausentes em combinações de alto total) · Equilibrada (nenhuma outra leitura ativa). Cada matriz pode receber múltiplas leituras simultâneas. Síntese narrativa de 1-2 frases interpretativas gerada das leituras ativas.
Bloco 6 · Qualidade estrutural · saúde do diagnóstico: warnings ativados (contagem por gravidade: X estruturais · Y informativos · Z permanentes) · thresholds não-default usados · ajustes feitos (linhas com nulo excluídas · consolidação T-AGRUPA: N linhas → M células) · alertas de cardinalidade (P2 · P3 · P4 escapado se aplicável) · alertas de escape ativado (subtipo ID · NUMERICO_CONTINUO como Eixo · cardinalidade forçada).
§5.7a declara 6 defaults declarados editáveis no Resumo Executivo em Configurações avançadas: Top-N Bloco 4a (10 · livre 1-50) + 5 thresholds de leitura qualitativa (Concentrada · Dispersa · Esparsa · Assimétrica · Com lacunas relevantes).
Razão: (1) 7ª aplicação consecutiva cristaliza o padrão para formalização em CONTEXT §13 como padrão estrutural de produto. (2) Adaptações D-073 honestas à natureza bivariada categórica: Bloco 2 com 6 métricas-síntese específicas de matriz (não traduzíveis para V4/V5/V7 · ex: Densidade da matriz · Concentração no topo); Bloco 4 com sub-bloco 4b dedicado a ausências destacadas (vs bottom-N numérico) reflete a natureza V6 onde ausência é conteúdo primário. (3) Leituras qualitativas específicas (Concentrada · Dispersa · Esparsa · Assimétrica por Eixo · Com lacunas estruturais relevantes) são vocabulário analítico bivariado · alinha V6 com V5 (5 leituras) V7 (5 leituras) V9 (5 leituras). (4) 6 thresholds editáveis no Resumo Executivo honram C.5 sistematicamente (default declarado · editável · não silencioso).
Impacto:

dcv_v6.md §5.7 (6 blocos) · §5.7a (6 defaults editáveis)
Padrão "Resumo Executivo em 6 blocos fixos" atinge 7 aplicações consecutivas (V4 · V3 · V8 · V7 · V9 · V5 · V6) · pronto para formalização efetiva em CONTEXT §13 como padrão estrutural de produto (análogo aos 4 já formalizados: Objetivo da Visão · Fluxo Progressivo · Modelo T-MODELO · View Especializada)
Padrão "default declarado editável" atinge ~11ª aplicação extensa em V6 com 6 thresholds novos no Resumo Executivo

Referência canônica: /specs/dcv/dcv_v6.md §5.7 · CONTEXT §9 Camada C · §13 (pronto para formalização)

## D-116 — Taxonomia oficial V6 · 3 classes primárias de densidade com vocabulário dual + 2 especiais paralelas + 1 atributo derivado + 3 thresholds editáveis · 6ª aplicação consecutiva do padrão "thresholds multi-camada editáveis"
Data: 2026-04-20 · Bloco: DCV-V6 (sessão única) · Status: Fechada
Contexto: Prévio V6 Parte 6 lista 4 classes paralelas (Dominante · Relevante · Residual · Ausente) misturando planos conceituais distintos (estrutural × densidade). §3.3 declara limiares fixos 20% Dominante e 2% Residual sem default declarado editável · rompendo com padrão consolidado de 5 aplicações consecutivas (V4 D-040 limiares ABC · V7 D-084 Tolerância + D-089 leituras qualitativas · V8 D-078 thresholds de ciclo · V9 D-097/D-098 8 thresholds · V5 D-104 3 critérios de outlier). Sem vocabulário dual técnico/exibição. Sem atributo derivado. T-08/D-114 resolveu arquiteturalmente a separação estrutural × densidade; refino T-10 materializa na taxonomia final espelhando padrão V5/V7/V9.
Decisão: DCV-V6 §5.5 declara taxonomia oficial V6 com estrutura paralela V5/V7/V9: 3 classes primárias por célula + 2 classificações especiais paralelas + 1 atributo derivado por célula. Classes primárias de densidade (aplicáveis apenas a células presentes · vocabulário dual técnico/exibição): DOMINANTE · "No topo" / "Núcleo da matriz" (célula presente com Participação Acumulada ≤ limiar Dominante · default 20%) · RELEVANTE · "Corpo" / "Intermediária" (célula presente que não é Dominante nem Residual) · RESIDUAL · "Periférica" / "Cauda" (célula presente com Participação Individual < limiar Residual · default 2%). Classificações especiais paralelas (estruturais · não-densidade): AUSENTE · "Não observada" / "Sem ocorrência" (célula pertence ao produto cartesiano observado · T-08/D-114 · mas não aparece em nenhuma linha da base · aplicação canônica D-076 · conteúdo primário, não warning) · PRESENTE_SEM_VALOR · "Presente sem valor" (célula presente estruturalmente mas com Valor da Medida null · caso raro em Pré-agregado · T-09/D-115 · não entra em ranking de densidade). Atributo derivado por célula: faixa_de_participacao · enum de 6 valores · TOPO (0-20%) · ALTO (20-40%) · MEDIO (40-60%) · BAIXO (60-80%) · CAUDA (80-100%) · SEM_FAIXA (células ausentes ou presentes sem valor). Não declarado "Distância do Limite" como atributo (como V5/V7 fazem) porque em V6 o limiar é cumulativo (Dominante por acumulado), não absoluto · distância do limiar não tem mesma interpretabilidade imediata. faixa_de_participacao é análogo a Faixa Percentual V5 · aplicação D-073.
§5.5a declara 3 defaults declarados editáveis em Configurações avançadas: Limiar Dominante (acumulado · default 20% · livre 5-50%) · Limiar Residual (individual · default 2% · livre 0.5-10%) · Faixas de participação (default 5 faixas 0/20/40/60/80/100 · opções 3 faixas · 4 faixas · 5 faixas default · 10 faixas decis). 6ª aplicação consecutiva do padrão "thresholds multi-camada editáveis em Configurações avançadas" (V4 D-040 · V7 D-084 · V8 D-078 · V9 D-097 · V5 D-104 · V6 D-116).
§5.5b declara racional do limiar Dominante = 20% acumulado: default V6 diverge de V4/V10 (80% Classe A · ABC clássico) por natureza analítica. V6 é bivariada e matrizes densas têm muitas células competindo próximas ao topo · corte rigoroso (20%) destaca genuinamente o núcleo da matriz · onde está concentrado valor real. Valores ABC clássicos (80%/95%) em V6 dariam classificação pouco útil (maioria das células virariam Dominante). Aplicação D-073 "herança adaptada à natureza analítica" · 13ª aplicação documentada.
§5.6 declara tabela canônica das classes em formato espelho V5 §5.6 / V7 §5.2 / V9 §5.6.
Razão: (1) Estrutura paralela V5/V7/V9 dá taxonomia oficial completa e consistente cross-visão. (2) Vocabulário dual técnico/exibição completo herda T-03/§13.2 e aplica operacionalmente em classes (microcopy "No topo"/"Cauda" nunca "bom"/"ruim" · honra anti-glossário T-03). (3) Separação classes de densidade × classes especiais paralelas honra T-08/D-114 (classificação estrutural × densidade) operacionalmente. (4) 6 thresholds editáveis = 6ª aplicação consecutiva do padrão (pronto para formalização efetiva em CONTEXT §9 Camada C como padrão derivado de C.5 + D-024 "default declarado"). (5) Atributo derivado faixa_de_participacao adaptado à natureza V6 (não copia cegamente V5 "Distância do Limite" · aplicação D-073). (6) Racional do 20% declarado (não arbitrariamente copiado) honra transparência metodológica.
Impacto:

dcv_v6.md §5.5 (taxonomia) · §5.5a (thresholds editáveis) · §5.5b (racional do 20%) · §5.6 (tabela canônica formato espelho V5/V7/V9)
Padrão "thresholds multi-camada editáveis em Configurações avançadas" atinge 6 aplicações consecutivas (V4 · V7 · V8 · V9 · V5 · V6) · pronto para formalização efetiva em CONTEXT §9 Camada C
Padrão "default declarado" (D-024) aplicado em ~11ª dimensão acumulada em V6 (combinando T-04/T-05/T-06/T-07/T-09/T-10 · múltiplas dimensões)
Padrão D-073 "herança adaptada à natureza analítica" atinge 13ª aplicação documentada (Dominante 20% vs V4 80% · atributo faixa_de_participacao vs V5 "Distância do Limite")
Padrão estrutural de taxonomia (primárias + especiais paralelas + atributo derivado + vocabulário dual) reafirmado pela 5ª vez consecutiva (V7 · V8 · V9 · V5 · V6)

Referência canônica: /specs/dcv/dcv_v6.md §5.5 · §5.6 · CONTEXT §9 Camada C (13ª aplicação D-073)

## D-115 — V6 como 8ª consumidora de T-RANK · regra V6-específica em 4 níveis · separação ordenação de cálculo × exibição · Participação null em ausentes
Data: 2026-04-20 · Bloco: DCV-V6 (sessão única) · Status: Fechada
Contexto: Prévio V6 §4.6 declara regra de desempate em 2 níveis (Eixo1 alfabético → Eixo2 alfabético) insuficiente vs padrão consolidado de 4 níveis (V7 D-088 · V9 D-096). Prévio §4.5/§9 mistura ordenação de cálculo (usada em ranking e classificação) com ordenação de exibição (usada no coração visual · tela) sem formalizar qual é default onde. Refino T-09 separou os 2 planos e elevou T-RANK V6 a 4 níveis espelhando V7/V9.
Decisão: DCV-V6 §5.4 declara V6 como 8ª consumidora de T-RANK com regra V6-específica em 4 níveis (aplicação D-073 · paridade estrutural V7/V9): nível 1 Valor da Medida decrescente · nível 2 valor alfabético de Eixo 1 crescente (case-insensitive) · nível 3 valor alfabético de Eixo 2 crescente (case-insensitive) · nível 4 ordem de inserção da primeira ocorrência do par (Eixo1=X ∧ Eixo2=Y) na base ativa crescente. Tolerância 1e-9 para floating point (herança T-RANK default). Escopo = global no MVP (células do produto cartesiano observado · modo Segmentado em roadmap P-V6-05-SEGMENTADO-Evo).
§5.9 declara separação explícita entre ordenação de cálculo (T-RANK determinística · usada em ranking, participação acumulada, classificação de densidade) e ordenação de exibição da matriz (default declarado editável em 3 opções: alfabética crescente default · por total do eixo · manual · para TEMPORAL detectado muda para cronológica crescente com W-V6-EIXO-ORDEM-CRONOLOGICA informativo · 9ª aplicação do padrão "default declarado editável"). Reordenação manual sobre eixo temporal/ordinal dispara W-V6-EIXO-ORDEM-MANUAL (informativo · espelho V8 D-074).
§5.3 declara participação percentual sobre células presentes: denominador = Total da Matriz (somatório do Valor da Medida sobre células com classificação estrutural PRESENTE) · células ausentes com Participação = null · Participação Acumulada = null (honra D-023 V2 · null nunca convertido em zero).
§5.4 declara 3 casos-limite explícitos com warnings correspondentes: Caso 1 · Todas as células empatadas em valor · ranking segue exclusivamente níveis 2-4 · W-V6-RANKING-EMPATE-GERAL informativo quando > 50% das células estão empatadas; Caso 2 · Valor nulo em Medida · classificação estrutural = PRESENTE_SEM_VALOR (especial paralela · T-10) · células no final do ranking · W-V6-CELULA-PRESENTE-SEM-VALOR estrutural; Caso 3 · Empate na fronteira de classificação · ordenação estável do ranking desempata · W-V6-FRONTEIRA-CLASSIFICACAO informativo quando ocorre empate exato.
Razão: (1) Paridade estrutural com V7/V9 em 4 níveis reforça T-RANK como contrato estável. V7/V9 usam 4 níveis por natureza multidimensional; V6 usa 4 níveis por natureza bivariada categórica; V4/V10 usam 3 níveis default (caso monovariado); é padrão hierárquico coerente · natureza analítica determina adaptação · não arbitrariedade. (2) Nível 4 com "ordem de inserção da primeira ocorrência do par" é distinção V6-específica importante porque após consolidação por célula, "ordem de inserção da célula" é ordem de aparecimento do par na base (não ordem da linha consolidada) · preciso para determinismo absoluto (C.1). (3) Separação ordenação de cálculo × exibição resolve ambiguidade estrutural do prévio §9 e torna V6 implementável sem decisão silenciosa do Claude Code na Fase 2. (4) Matriz visual ordenada por valor vira tabela achatada ilegível (ordem sem semântica no eixo · dificulta leitura bidimensional) · separação é necessária para coração visual funcionar. (5) Participação null em células ausentes honra D-023 V2 (null ≠ 0) consistentemente · 5ª aplicação documentada (V2 · V5 · V8 · V6 em T-08 · V6 em T-09). (6) Casos-limite explícitos evitam invenção de comportamento pelo Claude Code (C.3).
Impacto:

dcv_v6.md §5.3 (participação) · §5.4 (T-RANK 4 níveis + casos-limite) · §5.9 (ordenação de exibição · 3 opções default declarado editável)
T-RANK ganha V6 como 8ª consumidora · contrato sem extensão nova (reaplicação de padrão 4 níveis adaptado já formalizado em V7 D-088 e V9 D-096)
Padrão "default declarado editável" atinge 9ª aplicação consecutiva (ordenação de exibição V6 · ordem de Eixo 1 e Eixo 2)
D-023 V2 (null nunca convertido em zero) ganha 5ª aplicação documentada (V2 · V5 · V8 · V6 T-08 · V6 T-09)
Padrão D-076 (ausência como conteúdo primário) recebe aplicação consistente em participação (null em ausente · não 0)
Padrão D-073 "herança adaptada à natureza analítica" ganha 12ª aplicação documentada (T-RANK V6 4 níveis bivariado)

Referência canônica: /specs/dcv/dcv_v6.md §5.3 · §5.4 · §5.9 · CONTEXT §6 T-RANK · §9 Camada C

## D-114 — Unidade analítica V6 = célula da matriz · produto cartesiano observado restrito · classificação estrutural Presente × Ausente como camada primária separada da densidade · aplicação canônica D-076
Data: 2026-04-20 · Bloco: DCV-V6 (sessão única) · Status: Fechada
Contexto: Prévio V6 trata unidade analítica em 3 lugares distintos com tensões: §4.2 declara "Eixo 1 + Eixo 2" como unidade analítica · §4.3 declara "produto cartesiano observado" sem definição precisa · §7.1 declara "1 linha por combinação Eixo 1 + Eixo 2" como granularidade do resultado. Prévio Parte 6 lista 4 classes paralelas (Dominante/Relevante/Residual/Ausente) misturando planos conceituais distintos: estrutural (presente × ausente) × densidade (dominante/relevante/residual). V6 também é a primeira visão do Módulo 1 onde a unidade analítica inclui objetos calculados como ausentes a partir do cruzamento · precisa formalização.
Decisão: DCV-V6 §2.5 formaliza unidade analítica V6 = célula da matriz (cada slot no par Eixo1=X ∧ Eixo2=Y no produto cartesiano observado · chave composta categórica não-ordenada que inclui células ausentes calculadas). Distinção vs outras famílias declarada: V4/V10 unidade é elemento ordenável (1 dimensão) · V7 unidade é Elemento+Grupo (chave composta com grupo interno) · V8 unidade é Entidade+PontoDoEixo (chave composta com eixo ordenado) · V9 unidade é Identificador com múltiplas métricas · V5 unidade é observação individual (não consolidada) · V6 unidade é célula na matriz de cruzamento (chave composta categórica não-ordenada, que inclui células ausentes calculadas).
§4.7a formaliza produto cartesiano observado restrito: V_Eixo1 × V_Eixo2 onde V_Eixo1 = {valores únicos em Eixo1 na base ativa após exclusão de nulos} e V_Eixo2 idem (não produto teórico entre domínios completos declarados externamente). Cardinalidade total de células = |V_Eixo1| × |V_Eixo2|. Nulos nos eixos pré-excluídos antes do cálculo com W-V6-EIXO-NULO-EXCLUIDO (informativo · contagem de linhas excluídas registrada em diagnóstico). Domínio declarado pelo usuário (caso: usuário declara "Eixo2 tem domínio conhecido {A,B,C,D} mesmo que base só mostre {A,B,C}" · para detectar ausência de D como lacuna de negócio, não como lacuna puramente observada) fica em roadmap P-V6-03-DOMINIO-DECLARADO-Evo.
§4.7b separa classificação estrutural (PRESENTE × AUSENTE · camada primária) da classificação de densidade (DOMINANTE/RELEVANTE/RESIDUAL · aplicável apenas a presentes · taxonomia final em §5.5 por D-116): Célula PRESENTE (combinação aparece ≥ 1 linha da base ativa) · Célula AUSENTE (par pertence a V_Eixo1 × V_Eixo2 mas não aparece em nenhuma linha da base ativa).
§4.7c formaliza consolidação V6 por aplicação T-04/D-111 + T-05/D-112: Modo Transacional default · múltiplas linhas com mesmo par consolidadas via T-AGRUPA conforme regra derivada da Medida (Contagem/Soma/Média); Modo Pré-agregado · T-AGRUPA em no-op validado (verifica unicidade · W-V6-CHAVE-NAO-UNICA estrutural se duplicidade). Em ambos os casos, produto cartesiano observado é calculado depois da consolidação · garante que V_Eixo1 e V_Eixo2 refletem valores únicos reais.
§4.7d declara granularidade do resultado: Base Analítica V6 tem 1 linha por célula (presente ou ausente · total = |V_Eixo1| × |V_Eixo2|), com colunas: Eixo1 · Eixo2 · Valor da Medida (numérico se presente · null se ausente · nunca zero substituindo null · honra D-023 V2) · Classificação estrutural (Presente × Ausente) · Classificação de densidade (Dominante/Relevante/Residual · null se ausente · taxonomia final em T-10/D-116) · Participação (% do total de células presentes · null se ausente) · Participação Acumulada (cumulativa sobre células presentes ordenadas · null se ausente) · Ranking (1 a N entre células presentes · null se ausente). Paralelo ao padrão V8 (Base Analítica com linhas de ausência · D-078) e V5 (Base Analítica com classificação especial paralela · D-108).
Aplicação canônica de D-076: V6 é primeira visão onde a unidade analítica inclui objetos calculados como ausentes · ausência não é warning, é metade da unidade analítica · supera V8 em clareza (em V8 ausência compete com Novo/Contínuo/Retornou; em V6 ausência é estruturalmente metade da análise).
Razão: (1) Célula como unidade analítica dá nitidez conceitual que o prévio deixou latente · alinha V6 com padrão pós-D-073 de unidade analítica explicitamente nomeada em cada visão. T-03 declarou célula como termo canônico no vocabulário V6; T-08 materializa operacionalmente. (2) Produto cartesiano observado restrito é a interpretação mais simples, mais auditável, e a que o prévio sugere · honra C.5 (sistema opera sobre o dado declarado, não sobre o dado teórico). (3) Separação classificação estrutural × densidade resolve mistura de planos do prévio Parte 6 · cria paralelo cross-visão com V5/V7/V8/V9 (classes primárias + especiais paralelas). (4) Ausência como conteúdo primário é aplicação canônica mais forte de D-076 documentada · V6 é a expressão mais completa do padrão. (5) Null em células ausentes honra D-023 V2 consistentemente (nulo nunca tratado como zero · incluir ausente no denominador da participação seria tratá-la como zero). (6) Base Analítica 1 linha por célula (presente ou ausente) habilita rastreabilidade plena e é paralelo direto do que V5/V8 fazem.
Impacto:

dcv_v6.md §2.5 (unidade analítica) · §4.7a (produto cartesiano observado) · §4.7b (classificação estrutural Presente × Ausente) · §4.7c (consolidação V6 aplicação T-04+T-05) · §4.7d (granularidade do resultado)
Padrão D-076 atinge 4 aplicações documentadas (V8 origem · V5 "outliers primários em V5 × input de ordenação em V9" · V9 · V6) · em V6 chega à expressão mais completa (aba Excel dedicada em D-119 · sub-bloco Resumo Executivo próprio em D-117 · classificação estrutural como camada primária · Base Analítica 1 linha por célula ausente)
Padrão D-023 V2 (null nunca convertido em zero) atinge 4 aplicações documentadas (V2 origem · V5 · V8 · V6)
Roadmap V6 ganha P-V6-03-DOMINIO-DECLARADO-Evo (domínio teórico vs observado)
Nenhum requisito novo para Fundação (produto cartesiano observado é cálculo simples intra-V6 · não requer extensão de motor_base nem T-PIVOT nem novos transversais)

Referência canônica: /specs/dcv/dcv_v6.md §2.5 · §4.7 · CONTEXT §9 Camada C (D-076 aplicação canônica mais forte)

## D-113 — Classificação categórico-elegível formalizada no motor_base como metadado estrutural · requisito novo para Fundação (column_meta.tipo_estrutural) · escala de cardinalidade individual do eixo em 4 patamares · 6ª aplicação consecutiva do padrão "escala de cardinalidade com patamares numerados"
Data: 2026-04-20 · Bloco: DCV-V6 (sessão única) · Status: Fechada
Contexto: Prévio V6 §2.2 menciona elegibilidade categórica ("ambos devem ser elegíveis como campos categóricos · se o Motor Base os classificar como categóricos") mas não define critério operacional. Prévio §4.7 declara "campo com mais de 200 valores distintos por eixo → alerta forte · motor deve sugerir alternativa" sem patamares estruturados com bloqueio. V6 é a primeira visão onde o eixo precisa ser explicitamente categórico (campo numérico contínuo como Eixo produz matriz 1000×1000 com 1 observação por célula · resultado sem sentido). Outras visões aceitam qualquer coisa como agrupador sem precisar distinguir. Refino T-06 formalizou classificação categórico-elegível como metadado estrutural do motor_base (requisito novo G-FUND) + escala de cardinalidade individual em 4 patamares.
Decisão: DCV-V6 §4.5a declara requisito novo para G-FUND: motor_base ganha campo tipo_estrutural em column_meta com 5 valores enum: CATEGORICO_ELEGIVEL (texto não-numérico, OU numérico com subtipo ID detectado D-103, OU cardinalidade ≤ 200 em numéricos inteiros, OU Booleano · aceito como Eixo V6 default sem warning); NUMERICO_CONTINUO (numérico não-inteiro, OU numérico inteiro com cardinalidade > 200 sem padrão ID · bloqueio B-V6-EIXO-NUMERICO-CONTINUO com escape "este campo é categórico de fato" · marca W-V6-EIXO-FORCADO-CATEGORICO permanente); TEMPORAL (data/timestamp detectados pelo reconhecedor de padrões pt-BR/pt-EN de D-026 · aceito com W-V6-EIXO-TEMPORAL informativo e microcopy redirecional "Datas/timestamps podem ser usadas em V6 como eixo categórico (cada valor único é uma categoria). Para análise de evolução temporal, considere V3 ou V8"); BOOLEANO (2 valores únicos true/false · 0/1 · sim/não · aceito sem warning · caso legítimo · matriz 2×N útil); VAZIO/AMBIGUO (coluna com > 90% nulos ou tipo inconferível · bloqueio B-V6-EIXO-VAZIO-OU-AMBIGUO · sem escape estrutural). A heurística detalhada de classificação fica no motor_base (spec_fundacao.md a escrever no G-FUND); V6 apenas consome a classificação.
§4.5b declara comportamento V6 por tipo estrutural detectado (5 casos acima mapeados para: aceita sem warning · bloqueio com escape · aceita com warning · aceita sem warning · bloqueio sem escape).
§4.5c declara escala de cardinalidade individual do eixo em 4 patamares numerados (espelho padrão V7 D-089 / V8 D-079 / V9 / V5 D-109): P1 · Normal · 2 a 30 valores únicos · execução sem warning; P2 · Alerta leve · 31 a 100 · W-V6-EIXO-CARDINALIDADE-P2 informativo · microcopy "matriz ficará grande"; P3 · Alerta forte · 101 a 200 · W-V6-EIXO-CARDINALIDADE-P3 estrutural · execução confirmada pelo usuário · microcopy "matriz ficará muito grande · considere agrupar valores"; P4 · Bloqueio · > 200 · B-V6-EIXO-CARDINALIDADE-EXCESSO · escape disponível "sei o que estou fazendo" · marca W-V6-EIXO-CARDINALIDADE-FORCADA permanente. Cardinalidade combinada (produto Eixo1 × Eixo2) recebe escala própria V6-específica em D-120 (T-14).
§4.5d declara B-V6-EIXOS-IGUAIS (um campo não pode ocupar os dois eixos) sem escape · invariante matemático (matriz de campo contra si mesmo é diagonal trivial).
Razão: (1) Alinha com arquitetura Fundação única · motor_base é o lugar canônico para classificação estrutural de campos · D-008 (inferência semântica) e D-103 (subtipo ID) já vivem lá · tipo_estrutural é terceira camada coerente. (2) Metadado útil para V6 e para M2 (certamente precisará) e visões futuras · implementação de 1 dia de Claude Code quando chegar a Fase 1. (3) Mesma classificação usada em sentidos opostos em V5 Medida (bloqueia subtipo ID) × V6 Eixo (aceita subtipo ID) · aplicação canônica de D-073 "herança adaptada à natureza analítica" cross-uso · exemplo hierárquico-metodológico do padrão. (4) Tratamento TEMPORAL com redirecionamento V3/V8 preserva fronteiras operacionais declarativas (sem link operacional · microcopy autossuficiente · padrão cross-visão). (5) Tratamento BOOLEANO como caso legítimo (matriz 2×N · ex: "Ativo/Inativo × Região") é pragmático e útil. (6) Escape em NUMERICO_CONTINUO honra C.5 em casos-limite reais (códigos de produto com > 200 SKUs claramente categóricos · bloqueio absoluto decidiria por alguém). (7) Escala de cardinalidade em 4 patamares numerados espelha padrão cross-visão · 6ª aplicação consecutiva (V7 · V8 · V9 · V5 individual · V6 individual · V6 da matriz em D-120 seria 7ª).
Impacto:

dcv_v6.md §4.5a (classificação motor_base) · §4.5b (comportamento V6) · §4.5c (escala cardinalidade individual) · §4.5d (eixos iguais)
Requisito novo para Fundação (G-FUND): motor_base com metadado column_meta.tipo_estrutural (5 valores enum · heurística detalhada fica em spec_fundacao.md)
Padrão "escala de cardinalidade em eixos com patamares numerados" atinge 6ª aplicação consecutiva
Padrão D-073 aplicação cross-uso documentada (mesmo metadado usado em sentidos opostos V5/V6 para subtipo ID) · exemplo canônico
Este é o primeiro de 3 requisitos novos para Fundação vindos de V6 (depois de 5ª aplicação de "consolidação pré-cálculo" em D-111 e herança de detecção de subtipo ID em D-112)

Referência canônica: /specs/dcv/dcv_v6.md §4.5 · CONTEXT §6 motor_base · §9 Camada C

## D-112 — Tipos de medida V6 · separação dos planos tipo de campo D-025 × regra de agregação T-AGRUPA · 5ª aplicação consecutiva do padrão "tratamento por tipo de campo"
Data: 2026-04-20 · Bloco: DCV-V6 (sessão única) · Status: Fechada
Contexto: Prévio V6 §2.3 declara "3 tipos oficiais de medida: Contagem · Soma · Média" misturando dois planos conceituais distintos: tipo do campo (natureza semântica · D-025 sistematizada em V4 D-036 · espelhada em V5 D-103 · V7 D-083 · V8 §4.2) e regra de agregação (operação T-AGRUPA). Prévio §4.8 trata "Soma sobre campo de percentual/índice" como warning sem matriz estruturada de tipos de campo aceitos. Rompe com padrão consolidado em 4 aplicações (V4 · V7 · V8 · V5). Refino T-05 separou os planos e formalizou tratamento por tipo de campo.
Decisão: DCV-V6 §4.4 separa explicitamente os 2 planos conceituais. §4.4a declara tabela de tipos de campo aceitos como Medida em V6 (aplicação D-025 adaptada): Aditivo · aceito · default Soma · execução normal sem warning; Relativo · aceito · default Média · warning informativo W-V6-MEDIDA-RELATIVA sobre interpretação · se usuário escolhe Soma, warning estrutural W-V6-SOMA-SOBRE-RELATIVA; Não aditivo subtipo estoque/contagem · aceito · default Média · warning informativo W-V6-MEDIDA-NAO-ADITIVA; Não aditivo subtipo ID (CPF · CNPJ · número de pedido) · bloqueio B-V6-MEDIDA-ID com escape "este campo é numérico de fato" · warning permanente W-V6-ID-FORCADO se ativado · heurística de detecção herdada de V5 D-103 (campo numérico inteiro com cardinalidade ≥ 90% das linhas + sequência aritmética ≥ 80% OR comprimento fixo 8+ dígitos em 100% das linhas) · zero extensão nova para Fundação; Booleano · aceita apenas se Medida = Contagem (interpretação trivial: proporção de flag=1 por combinação) · bloqueio B-V6-BOOLEANO-COM-SOMA-OU-MEDIA se regra ≠ Contagem; Estado/situação (categórico) · bloqueio B-V6-ESTADO-COMO-MEDIDA com microcopy de redirecionamento "Use este campo como Eixo 1 ou Eixo 2 · para comparar cruzamentos entre estados, considere V8 · para contar ocorrências por combinação, use Medida = Contagem e escolha dois campos categóricos como eixos".
§4.4b declara 3 regras de agregação aceitas em V6 MVP (Contagem dispensa campo numérico · frequência de linhas · default quando não há campo numérico selecionado; Soma obrigatório campo numérico · default quando Medida é Aditiva; Média obrigatório campo numérico · default quando Medida é Relativa ou Não-aditiva subtipo aceito). Máximo/Mínimo (regras oficiais T-AGRUPA em V4/V7/V8/V9/V5) ficam fora de escopo V6 MVP · roadmap P-V6-04-MAX-MIN-Evo. Racional: V6 é matriz com foco em intensidade/concentração da combinação · Máx/Mín na célula produzem leitura confusa · V6 MVP fica com 3 regras que cobrem 95% dos casos.
§4.4c declara detecção de subtipo ID em Medida V6 como herança direta de V5 D-103 com bloqueio + escape · zero extensão nova para Fundação (motor_upload com detecção de subtipo ID já é requisito via D-103 · extensão D-008).
§4.4d declara matriz canônica Medida × Regra de Agregação com defaults declarados e regras permitidas: sem campo numérico → default Contagem, permitido apenas Contagem; Aditivo → default Soma, permitido Contagem/Soma/Média; Relativo → default Média, permitido Contagem/Média/(Soma com warning estrutural); Não aditivo estoque/contagem → default Média, permitido Contagem/Média; Não aditivo ID → bloqueado; Booleano → default Contagem, permitido apenas Contagem; Estado/situação → bloqueado como Medida.
Razão: (1) Separação tipo de campo × regra de agregação é padrão cross-visão consolidado em 4 aplicações (V4 · V7 · V8 · V5) · V6 é 5ª aplicação · pronto para formalização em CONTEXT §6 como contrato canônico T-AGRUPA + tipos de campo. (2) Contagem como caso especial que dispensa campo numérico herda tratamento de V4/V7/V8/V9 · consistência cross-visão. (3) Subtipo ID herdado de V5 D-103 · zero extensão para Fundação (motor_upload já tem detecção como requisito). (4) Booleano tratado pragmaticamente: aceita com Contagem (caso útil real · "quantas linhas têm flag = 1 por combinação") · bloqueia Soma/Média (casos sem sentido · somar booleans da célula é o mesmo que Contagem filtrando flag=1 · média de booleans é taxa mas sem semântica clara). (5) Estado/situação com microcopy de redirecionamento sensata (se o campo é categórico, vira eixo · se quer contar, use Contagem). (6) Máx/Mín em roadmap é honesto ao escopo MVP · V6 Máx/Mín em célula têm leitura analítica fraca · quem precisa está geralmente pensando V4/V7/V5.
Impacto:

dcv_v6.md §4.4 (4 subseções: tipos de campo · regras de agregação · detecção subtipo ID · matriz Medida × Regra)
Padrão D-025/D-036 "tratamento por tipo de campo cross-visão" atinge 5 aplicações consecutivas (V4 D-036 · V7 D-083 · V8 §4.2 · V5 D-103 · V6 D-112) · candidato forte à formalização em CONTEXT §6 como contrato canônico
Zero extensão nova para Fundação (detecção de subtipo ID já é requisito via D-103)
T-AGRUPA em V6 usa 3 das 5 regras canônicas (Contagem · Soma · Média) · Máx/Mín em roadmap P-V6-04-MAX-MIN-Evo
3 bloqueios catalogados (B-V6-MEDIDA-ID · B-V6-BOOLEANO-COM-SOMA-OU-MEDIA · B-V6-ESTADO-COMO-MEDIDA) e 6 warnings catalogados em §10

Referência canônica: /specs/dcv/dcv_v6.md §4.4 · CONTEXT §6 T-AGRUPA · §9 Camada C

## D-111 — Modo da base V6 declarado em 2 modos canônicos (Transacional default × Pré-agregado) · T-AGRUPA como 9ª consumidora com consumo padrão · multi-aba em roadmap · 5ª aplicação consecutiva do padrão "consolidação obrigatória pré-cálculo"
Data: 2026-04-20 · Bloco: DCV-V6 (sessão única) · Status: Fechada
Contexto: Prévio V6 §2.1 declara modo da base (transacional · pré-agregada) em texto genérico sem escolha explícita do usuário com default declarado pelo motor. §2.4 fala em "consolidar primeiro, classificar depois" sem invocar T-AGRUPA formalmente. Multi-aba mencionada como "refinamento futuro" sem formalização do caso MVP (escolha de 1 aba) vs caso avançado (empilhar abas). Rompe com padrão cross-visão consolidado pós-V5: modo da base como escolha explícita com default declarado + T-AGRUPA invocada formalmente + blindagem contra dupla agregação via no-op validado · 4 aplicações consecutivas (V8 D-074 · V7 D-082 · V9 D-092 · V5 D-102 com adaptação V5-específica via D-073). Refino T-04 formalizou modo da base V6 + T-AGRUPA como 9ª consumidora com consumo padrão (não adaptação V5-específica · V6 é caso típico da família V4/V7/V8/V9 · reforço do tronco comum).
Decisão: DCV-V6 §4.1 declara 2 modos canônicos V6: Transacional (default quando média de linhas por par Eixo1+Eixo2 ≥ 1.5 na amostragem · múltiplas linhas podem cair na mesma célula · T-AGRUPA consolida via regra de agregação correspondente à medida escolhida); Pré-agregado (quando média de linhas por par < 1.5 · cada célula Eixo1+Eixo2 já vem como linha única com valor consolidado · T-AGRUPA em modo no-op validado · verifica unicidade do par e gera W-V6-CHAVE-NAO-UNICA estrutural se duplicidade detectada). Default proposto pelo motor via heurística de cardinalidade · visível na configuração antes da execução · editável em um clique · W-V6-MODO-INFERIDO informativo quando aceito por default.
§4.2 declara V6 como 9ª consumidora de T-AGRUPA com consumo padrão (não adaptação V5-específica): Modo Transacional → regra de agregação aplicada sobre Eixo1+Eixo2 conforme Medida escolhida (Contagem = count de linhas · Soma = sum do campo numérico · Média = avg do campo numérico · conforme T-05/D-112); Modo Pré-agregado → no-op validado (verifica unicidade · sem operação de agregação). Contrato T-AGRUPA sem extensão nova · V6 reforça tronco comum da família V4/V7/V8/V9 · 5ª aplicação consecutiva do padrão "consolidação obrigatória pré-cálculo com blindagem contra dupla agregação".
§4.3 e §3.2 declaram multi-aba com escolha explícita de 1 aba por execução no MVP (etapa dedicada · obrigatória mesmo se arquivo tem apenas 1 aba) · empilhamento de múltiplas abas estruturalmente idênticas fica em roadmap P-V6-02-MULTIABA-Evo ligado a M2.STACK (D-063 · V6 vira 3º consumidor futuro declarado junto com V3 P-V3-01-Evo e V8 P-V8-01-Evo · pressão adicional no G-FUND para posicionamento definitivo).
Razão: (1) V6 é caso típico da família V4/V7/V8/V9 (consolidação por célula) · consumo padrão é aplicação honesta da natureza analítica · V5 foi o caso especial via D-073 (V5 nunca consolida valores por natureza estatística descritiva univariada) · V6 reforça o tronco comum. (2) Default declarado via heurística honra C.5 plenamente (motor propõe · usuário vê antes da execução · usuário confirma ou edita) · zero default silencioso. (3) Blindagem contra dupla agregação explícita via no-op validado em Pré-agregado. (4) 5ª aplicação consecutiva cristaliza o padrão como candidato muito forte à formalização efetiva em CONTEXT §9 Camada C como derivado de C.2 (nada silencioso) + C.5 (default declarado do modo da base) + padrão "default declarado" D-024. (5) M2.STACK ganha V6 como 3º consumidor futuro declarado · pressão significativa no G-FUND para posicionamento definitivo (transversal da Fundação × parte de M2 × capability compartilhada).
Impacto:

dcv_v6.md §4.1 (modo da base) · §4.2 (T-AGRUPA V6 9ª consumidora consumo padrão) · §4.3 (multi-aba) · §3.2 (multi-aba detalhe)
T-AGRUPA ganha V6 como 9ª consumidora com consumo padrão · contrato sem extensão nova (reforço do tronco comum · não adaptação V5-específica)
Padrão "consolidação obrigatória pré-cálculo com blindagem contra dupla agregação" atinge 5 aplicações consecutivas (V8 D-074 · V7 D-082 · V9 D-092 · V5 D-102 · V6 D-111) · pronto para formalização efetiva em CONTEXT §9 Camada C
M2.STACK ganha V6 como 3º consumidor futuro declarado (P-V6-02-MULTIABA-Evo · junto com V3 P-V3-01-Evo e V8 P-V8-01-Evo) · pressão adicional no G-FUND
2 warnings catalogados (W-V6-MODO-INFERIDO informativo · W-V6-CHAVE-NAO-UNICA estrutural)

Referência canônica: /specs/dcv/dcv_v6.md §4.1 · §4.2 · §4.3 · CONTEXT §6 T-AGRUPA · §9 Camada C

## D-110 — Sumário do refino DCV-V5 · 15 pendências fechadas em sessão única · Família E reformulada
Data: 2026-04-19 · Bloco: DCV-V5 (sessão única) · Status: Fechada
Contexto: Refino DCV-V5 executado em sessão única (19/04/2026) seguindo padrão D-019 + D-034 + D-033. 15 pendências originais trabalhadas (T-01 a T-15), todas fechadas, nenhuma deferida. Padrão de condução D-019 aplicado integralmente: ritual de abertura com leitura dos 4 documentos canônicos + 4 DCVs anexados (prévio V5, V7 aprovado, V9 aprovado, V4 aprovado), fila racionalizada em 4 blocos (A · Posicionamento e fronteira · B · Entrada e estrutura analítica · C · Cálculo e classificação · D · Saída e operação), uma pendência por vez com opções explícitas e C.5 como primeira lente, mini status-checks a cada ~3 pendências, sinalização de densidade D-034 no 3º status-check com recomendação de continuar em sessão única (aprovada pela Usuária).
Decisão: DCV-V5 refinado. Consolida 15 pendências estruturais com 8 decisões específicas (D-102 a D-109) mais esta (D-110) como sumário + reformulação da Família E. Família E reformulada de "Estrutura interna de um campo" para "Estrutura interna do recorte" — formulação anterior tinha imprecisão (V6 é bivariada · não "de um campo"). Nova formulação cobre V5 univariado numérico e V6 bivariado categórico. Adaptação D-073 ao próprio método de posicionamento de família: famílias com par operacionalmente próximo (B · D) merecem tabela de retroação diferida com células (a confirmar) (D-060 V3→V8 · D-081 V7→V9); famílias com par operacionalmente distante (E) merecem declaração enxuta de convivência sem retroação diferida formal. DCV-V5 §2.3 declara convivência na família + nota de "DCV-V6 declarará seu posicionamento simétrico quando refinado" — sem D-XXX de retroação. Família D · Posição relativa fechada em Fase 0 após aprovação do DCV-V9 em 19/04/2026. Próxima Fase 0: DCV-V6 (segunda e última visão da Família E · Estrutura interna do recorte · fecha a Fase 0 · G-FUND abre em sequência direta).
8 decisões consolidadas do refino:
#TemaReferênciaT-01Família E reformulada + §2.3 enxuto sem retroação diferida formal V5→V6D-110 · dcv_v5.md §2.3 · CONTEXT §4 · GLOSSARIO §1T-023 fronteiras V5×V7 · V5×V9 · V5×V4 em prosa declarativa autossuficientedcv_v5.md §2.2 (aplicação de padrão D-076 + D-073 · não gera D-XXX)T-03Vocabulário canônico V5 (~24 termos em 5 categorias) + vocabulário dual 6 pares + anti-glossário 5 termosdcv_v5.md §13 · GLOSSARIO seção 5.V5 nova · §11 anti-glossárioT-04Modo da base V5 em granularidade (Individual default declarado × Consolidada por chave) + T-AGRUPA semântica V5-específica em 3 modos (nunca consolida valores)D-102 · dcv_v5.md §4.1 · §4.2T-05Tipos de medida em V5 · Aditivo/Relativo aceitos · Não aditivo condicional com detecção de subtipo ID · Booleano bloqueadoD-103 · dcv_v5.md §3.3 · §3.4T-06Modo da Visão Global × Segmentado · 1 Agrupador no MVP · escala de cardinalidade graduada · tratamento de segmento pequeno em camadasdcv_v5.md §4.3 · §4.4 · §4.5 · §4.6 (aplicação de padrões consolidados · não gera D-XXX)T-07Tratamento de nulos (ignorados + contagem agregada) · duplicidade (preservada como distribuição observada) · zeros (default declarado editável)dcv_v5.md §4.7 · §4.8 · §4.9 (aplicação de padrões · não gera D-XXX)T-083 critérios de outlier (IQR · Z-score · Percentil) com defaults declarados editáveis em Configurações avançadasD-104 · dcv_v5.md §4.10 · §4.11T-0913 métricas oficiais (11 do prévio + Amplitude + Skewness) · classificação automática de assimetria · moda múltipla em 4 camadas · DP amostral defaultdcv_v5.md §5.1 · §5.2 · §5.3 · §5.4 (aplicação de padrões · não gera D-XXX)T-10Taxonomia oficial V5: 3 classes primárias com vocabulário dual + 1 classe especial paralela (VALOR_NAO_NUMERICO) + 2 atributos derivados (Distância do Limite · Faixa Percentual) + 5 leituras qualitativas multi-aplicáveis + Equilibrada como default sem destaqueD-105 · dcv_v5.md §5.5 · §5.6T-11Resumo Executivo V5 com 6 blocos (6ª aplicação D-044) · Bloco 2 com 2 camadas em Modo Segmentado · Bloco 4 reformulado como "valores destacados" em 3 sub-blocosD-106 · dcv_v5.md §5.7T-12Mapa de Distribuição como coração visual V5 (Histograma + Tabela detalhada) · Sturges como default declarado editável · Boxplot em roadmap · requisito novo para exportacao.pyD-107 · dcv_v5.md §5.8 · §5.9T-13Estrutura Excel V5 · 6 abas em Global / 7 em Segmentado · "Resumo por Segmento" condicional · "Dados Brutos do prévio" descartada (4ª aplicação consecutiva)D-108 · dcv_v5.md §5.10 · §5.11T-1412 bloqueios operacionais + escala de cardinalidade em 3 eixos multi-dimensionais independentes (alinhada com V9) + 9 diretrizes de performance (7 herdadas + 2 específicas V5)D-109 · dcv_v5.md §7 · §8T-15Roadmap pós-MVP com 13 candidatos P-V5-XX-Evo + anti-roadmap com 2 itens (Imputação automática de nulos · Limpeza/remoção automática de outliers)dcv_v5.md §9 · §9.1 (consolidação de candidatos já rastreados · não gera D-XXX)
Razão: (1) Sessão única validou pela 6ª vez consecutiva (V10 · V3 · V8 · V7 · V9 · V5) que refino denso pode caber em uma sessão quando o prévio é maduro (V5 tinha Partes 0-14 já normativas) e a maioria das pendências herda padrões consolidados. (2) Família E fechada em Fase 0 com apenas V6 restante — a última visão com DCV não refinado. (3) Contrato de T-AGRUPA estendido pela segunda vez estruturalmente (primeira foi V9 com regra por métrica · D-092; segunda é V5 com 3 modos que nunca consolidam valores · D-102) — cada extensão justificada explicitamente via padrão "herança adaptada à natureza analítica" D-073 (11ª aplicação documentada). (4) 4 padrões consolidados ganham aplicações muito fortes a formalização efetiva no próximo ajuste estrutural do CONTEXT: "consolidação obrigatória pré-cálculo" (4ª aplicação V8/V7/V9/V5) · "thresholds multi-camada editáveis" (5ª aplicação V4/V7/V8/V9/V5) · "Dados Brutos descartada" (4ª aplicação V8/V7/V9/V5) · "Resumo Executivo em 6 blocos" D-044 (6ª aplicação V4/V3/V8/V7/V9/V5 · candidato forte à formalização em CONTEXT §13 como padrão estrutural de produto). (5) Kit D-033 completo em sessão única validado pela sexta vez consecutiva.
Impacto:

1 DCV aprovado a mais → 10 de 11 DCVs aprovados na Fase 0 (V2 · V1 · V11 · V4 · V10 · V3 · V8 · V7 · V9 · V5) após aprovação formal deste
Fila remanescente Fase 0: V6 · 1 DCV · Família E · fecha a Fase 0
Família E · Estrutura interna do recorte com primeira visão aprovada (reformulada nesta sessão)
~37 warnings V5 catalogados · V5 na faixa alta do projeto (V7 = 35 · V8 = 37 · V9 = 40 · V5 ≈ 37)
T-AGRUPA ganha V5 como 8ª consumidora com semântica V5-específica em 3 modos · em nenhum modo V5 consolida valores
Padrão "herança adaptada à natureza analítica" D-073 ganha 5 novas aplicações (T-AGRUPA semântica V5-específica · NULO_MEDIDA agregada em diagnóstico · Bloco 4 "valores destacados" sem unidade analítica rotulada · escala multi-eixo independente alinhada com V9 · método de posicionamento de família operacionalmente distante) → 11 aplicações documentadas
Padrão "default declarado" aplicado em ~10 dimensões V5 (granularidade da base · modo da visão · 3 thresholds de critério · binning · 3 leituras qualitativas · DP amostral × populacional · Top-N Bloco 4 · zeros como ausentes · ordenação Resumo por Segmento)
4 padrões consolidados com candidatura muito forte à formalização efetiva no próximo ajuste do CONTEXT (consolidação obrigatória pré-cálculo · thresholds multi-camada editáveis · Dados Brutos descartada · Resumo Executivo 6 blocos)
2 requisitos novos para a Fundação (G-FUND): motor_upload com detecção de subtipo ID (extensão D-008) · exportacao.py com Histograma nativo Excel via openpyxl
Próximo bloco: DCV-V6 (segunda visão da Família E · fecha a Fase 0 · G-FUND abre em sequência direta)

Referência canônica: /specs/dcv/dcv_v5.md · D-102 a D-109 · CONTEXT §4 Família E reformulada · §6 T-AGRUPA · §9 Camada C (11ª aplicação D-073 · 4 padrões candidatos muito fortes à formalização) · GLOSSARIO §1 Família E · §4 T-AGRUPA · seção 5.V5 nova · §6 Warnings V5 · §11 anti-glossário V5

## D-109 — Bloqueios operacionais V5 + escala de cardinalidade em 3 eixos multi-dimensionais independentes + 9 diretrizes de performance
Data: 2026-04-19 · Bloco: DCV-V5 (sessão única) · Status: Fechada
Contexto: Prévio V5 Parte 11 lista alertas não bloqueantes em linguagem genérica sem matriz de bloqueios estruturais numerados e sem patamares operacionais como V7 §8.1 · V8 §8 · V9 §7 têm. Precisa consolidar bloqueios, cardinalidade e performance em formato padronizado. Refino T-14 consolidou os 3 sub-temas.
Decisão: DCV-V5 §7 declara 12 bloqueios operacionais estruturais numerados (análogo V7/V8/V9): B-V5-CAMPO-PRINCIPAL-NAO-NUMERICO · B-V5-CAMPO-BOOLEANO · B-V5-CAMPO-ID (escapável) · B-V5-MINIMO-OPERACIONAL · B-V5-AGRUP-EXCESSO · B-V5-CAMPO-PRINCIPAL-COMO-AGRUP · B-V5-AGRUPADOR-NULO-EXCESSIVO · B-V5-DISTRIBUICAO-DEGENERADA · B-V5-NULOS-EXCESSIVOS-CRITICO · B-V5-AGRUPADOR-NUMERICO · B-V5-MULTIPLOS-CRITERIOS-SIMULTANEOS · B-V5-MOTOR-INFERIU-TIPO-INCOMPATIVEL. §8 declara escala de cardinalidade em 3 eixos multi-dimensionais independentes (alinhada com V9 · não hierárquico-aditivo de V7 · não multiplicativo de V8): Eixo 1 · N observações válidas em 6 patamares · Eixo 2 · Cardinalidade do Agrupador em 4 patamares · Eixo 3 · Diversidade do campo principal (cardinalidade de valores únicos como % de N válido) em 3 patamares. §8.4 declara 9 diretrizes de performance (7 herdadas V3/V8/V7/V9 + 2 específicas V5: detecção de subtipo ID executada uma vez no upload e cálculo de skewness em passe único integrado com média e DP).
Estrutura multi-eixo independente (aplicação D-073): V5 é distinta de V7 (hierárquica-aditiva: elementos dentro de grupos), V8 (matricial multiplicativa), e similar a V9 (eixos ortogonais). Em V5 os 3 eixos são recortes ortogonais do dado — crescem independentemente. Custo computacional escala como O(N log N) para ordenação + O(N) para varredura de métricas.
Razão: (1) Padrão de bloqueios numerados consolidado em V7/V8/V9/V5 (4 aplicações · cada uma adaptada à natureza analítica). (2) Padrão de escalas de cardinalidade com patamares numerados consolidado em V7/V8/V9/V5 (4 aplicações). (3) Diretrizes de performance como tronco comum (7 herdadas) + específicas V5 (2) reforça uniformidade + adaptação justificada. (4) Bloqueios estruturais numerados evitam que implementação invente comportamentos em casos-limite (C.3 honrado).
Impacto:

dcv_v5.md §7 (12 bloqueios) · §8 (escala 3 eixos · 9 diretrizes performance)
F-MOT (Fundação) recebe requisitos de 12 pré-validações estruturais
F-EXP (Fundação) recebe requisito: matriz pivotada em passe único para aba Mapa de Distribuição
F-TRANS (Fundação) recebe requisito: ordenação O(N log N) reutilizada para quartis/percentis/skewness
Total de warnings V5 atinge ~37 com esta pendência (12 bloqueios · 10 alertas · 15 informativos)
Padrão "escala de cardinalidade em eixos com patamares numerados" consolida com 4 aplicações (V7 hierárquico-aditiva · V8 multiplicativa · V9 multi-eixo independente · V5 multi-eixo independente alinhada com V9) — cada aplicação adaptada via D-073

Referência canônica: /specs/dcv/dcv_v5.md §7 · §8 · CONTEXT §9 Camada C (11ª aplicação D-073)

## D-108 — Estrutura Excel V5 · 6 abas em Global / 7 em Segmentado · "Dados Brutos do prévio" descartada (4ª aplicação consecutiva)
Data: 2026-04-19 · Bloco: DCV-V5 (sessão única) · Status: Fechada
Contexto: Prévio V5 §9.2 propõe 4 abas (Resumo Estatístico · Distribuição por Faixas · Detalhamento por Registro · Outliers) sem Resumo Executivo separado · sem Parâmetros · sem Diagnóstico. Rompe com padrão consolidado de 6 abas (Resumo · Coração visual · Análise substantiva · Parâmetros · Base Analítica · Diagnóstico última aba por D-017) presente em V4 (6 abas) · V7 (6 abas) · V9 (6 abas) · V10 (6 abas) · V8 (7 abas) · V3 (7 abas). Refino T-13 alinhou V5 ao padrão consolidado.
Decisão: DCV-V5 §5.10 declara estrutura Excel oficial V5 com 6 abas em Modo Global / 7 abas em Modo Segmentado (variação dinâmica pela aba "Resumo por Segmento" condicional ao modo · espelha V8 com aba Movimentações condicional): (1) Resumo Executivo · (2) Mapa de Distribuição · coração visual V5 · (3) Resumo por Segmento (apenas Segmentado) · (4) Outliers · (5) Base Analítica · (6) Parâmetros · (7) Diagnóstico (sempre última · D-017). §5.11 declara aba "Dados Brutos do prévio descartada" em favor de Base Analítica (linhas originais com classificações) + Diagnóstico (contagens estruturais agregadas).
4ª aplicação consecutiva do padrão "Dados Brutos descartada em favor de Base Analítica + Diagnóstico" (V8 D-078 · V7 D-089 · V9 D-099 · V5 D-108) → candidato muito forte à formalização efetiva no próximo ajuste do CONTEXT §9 Camada C.
Razão: (1) Regra D-017 (Diagnóstico sempre última aba) é transversal invariante — V5 não pode romper. (2) Resumo Executivo separado + Parâmetros + Base Analítica + Diagnóstico formam o "esqueleto padrão" que dá consistência cross-visão. (3) Aba Dados Brutos seria redundante em V5 (Base Analítica já tem 1 linha por observação · Diagnóstico tem contagens estruturais) · 4ª aplicação consecutiva do padrão de descarte consolida-o como padrão de método. (4) "Resumo por Segmento" condicional ao modo honra C.5 (não aparece com conteúdo vazio em Modo Global).
Impacto:

dcv_v5.md §5.10 (estrutura Excel) · §5.11 (Dados Brutos descartada)
F-EXP (Fundação) recebe requisito: suporte a variação dinâmica de número de abas conforme modo da visão (V5 · V8 · outras futuras)
CONTEXT §9 Camada C atualizada (padrão "Dados Brutos descartada" com 4ª aplicação consecutiva · candidato muito forte à formalização)

Referência canônica: /specs/dcv/dcv_v5.md §5.10 · §5.11 · CONTEXT §9 Camada C

## D-107 — Mapa de Distribuição como coração visual V5 · Histograma + Tabela detalhada · Sturges como default declarado editável de binning · Boxplot em roadmap · requisito novo para Fundação
Data: 2026-04-19 · Bloco: DCV-V5 (sessão única) · Status: Fechada
Contexto: Prévio V5 §6.6 menciona "histograma simplificado em tela e distribuição por faixas na exportação" mas não destaca uma aba como coração visual. Padrão consolidado pós-D-073 é cada visão ter uma aba declarada como "coração visual" que materializa visualmente a contribuição analítica primária (V8 Matriz de Presença · V7 Mapa de Grupos · V9 Mapa de Perfil · V4 Composição Principal · V10 Curva Pareto). V5 precisa do seu coração visual. Refino T-12 identificou Mapa de Distribuição como candidato natural.
Decisão: DCV-V5 §5.8 declara "Mapa de Distribuição" como coração visual da V5 — aba dedicada do Excel com Histograma (gráfico nativo via openpyxl BarChart com bins) + Tabela detalhada de Distribuição por Faixas (6 colunas: Faixa · Limite Inferior · Limite Superior · Frequência · % do Total · % Acumulada · coluna opcional "Tem outlier nesta faixa?"). Em Modo Segmentado, 1 conjunto (gráfico + tabela) por segmento separados visualmente. §5.9 declara regra de binning automático: Sturges como default declarado editável (k = ⌈log2(N) + 1⌉) · Configurações avançadas oferece Sturges (default) · Freedman-Diaconis (robusto a outliers) · Scott · número fixo (10/15/20/25/30/50). 9ª aplicação consecutiva do padrão "default declarado editável". Boxplot fica em roadmap (P-V5-BOXPLOT-Evo) por complexidade técnica de implementação via openpyxl (Boxplot nativo Excel só em 2016+ com limitações · openpyxl não suporta diretamente).
Razão: (1) Histograma é visualização universal de distribuição univariada · intuitivo para usuário não-estatístico · padrão de literatura e prática. (2) Tabela detalhada ao lado do gráfico cobre auditoria (cada barra corresponde a uma linha da tabela). (3) Sturges como default cobre 90% dos casos com simplicidade. (4) Nome "Mapa de Distribuição" alinha com família de nomes dos corações visuais (Mapa de Grupos · Mapa de Perfil · Matriz de Presença). (5) Boxplot adicionaria valor (comparação cross-segmentos visual) mas o risco técnico de quebrar a sessão via openpyxl inviabiliza no MVP · roadmap preserva o gancho.
Impacto:

dcv_v5.md §5.8 (Mapa de Distribuição · coração visual) · §5.9 (regra de binning)
Requisito novo para Fundação (G-FUND): exportacao.py ganha capability de Histograma nativo Excel via openpyxl BarChart com bins · aba "Mapa de Distribuição" como template padrão da V5
P-V5-BOXPLOT-Evo registrado em roadmap
9ª aplicação consecutiva do padrão "thresholds multi-camada editáveis / default declarado editável" (embora neste caso seja opção discreta · não threshold numérico · a aplicação se dá pelo mesmo princípio UX de default + edição em Configurações avançadas)

Referência canônica: /specs/dcv/dcv_v5.md §5.8 · §5.9 · CONTEXT §6 (exportacao.py capabilities)

## D-106 — Resumo Executivo V5 com 6 blocos · adaptação D-073 do padrão D-044 · 6ª aplicação consecutiva
Data: 2026-04-19 · Bloco: DCV-V5 (sessão única) · Status: Fechada
Contexto: Padrão "Resumo Executivo em 6 blocos fixos" (D-044 · iniciado em V4) tem 5 aplicações consecutivas anteriores (V4 · V3 · V8 · V7 · V9) e é candidato forte à formalização em CONTEXT §13 como padrão estrutural de produto. V5 é a 6ª aplicação consecutiva — precisa adaptar dois blocos à natureza analítica específica de V5: Bloco 2 (Números-âncora) em Modo Segmentado e Bloco 4 (Elementos destacados) que em V4/V7/V9 trata elementos rotulados mas em V5 não há unidade analítica rotulada.
Decisão: DCV-V5 §5.7 declara Resumo Executivo V5 com 6 blocos fixos (padrão D-044): (1) Cabeçalho · padrão · (2) Números-âncora com 2 camadas em Modo Segmentado (Camada agregada do conjunto: N total · N outliers totais · N segmentos + Camada por segmento: tabela compacta com Média · Mediana · DP · CV · % outliers por segmento) — em Modo Global apenas as 5-7 métricas-síntese · (3) Distribuição · % por classe primária + Distribuição por Faixas + Faixa Percentual · (4) Valores destacados em 3 sub-blocos (4a Top-N valores · 4b Bottom-N valores · 4c Outliers detectados · default N=5 editável em Configurações avançadas · 8ª aplicação consecutiva do padrão T-08 · em Modo Segmentado Top-N/Bottom-N por segmento não do conjunto) — adaptação D-073 porque V5 não tem unidade analítica rotulada como V4/V7/V9 · (5) Leitura qualitativa com síntese · 5 leituras qualitativas + síntese narrativa · por segmento em Segmentado · (6) Qualidade estrutural · padrão.
6ª aplicação consecutiva do padrão "Resumo Executivo em 6 blocos fixos" D-044 (V4 · V3 · V8 · V7 · V9 · V5) → candidato muito forte à formalização em CONTEXT §13 como padrão estrutural de produto (análogo aos 4 já formalizados: Objetivo da Visão · Fluxo de etapas progressivas · Modelo de configuração · View especializada entre visões da mesma família).
Razão: (1) Padrão D-044 consolidado em 6 aplicações consecutivas · cada uma adaptada via D-073 à natureza analítica (V5 adapta Bloco 2 com 2 camadas e Bloco 4 como "valores destacados"). (2) Bloco 2 em Modo Segmentado com 2 camadas honra C.5 — não decide pelo usuário qual ângulo importa (agregado × por segmento) · oferece os dois sem misleading. (3) Bloco 4 como "valores destacados" em 3 sub-blocos (Top-N · Bottom-N · Outliers) cobre o papel de "elementos destacados" de V4/V7/V9 em natureza univariada descritiva — Top-N por segmento evita dominação de segmentos com escala maior. (4) N=5 como default declarado editável segue padrão T-08.
Impacto:

dcv_v5.md §5.7 (Resumo Executivo · 6 blocos V5)
CONTEXT §13 ganha candidatura muito forte à formalização do padrão "Resumo Executivo em 6 blocos fixos" como padrão estrutural de produto (próximo ajuste estrutural)
CONTEXT §9 Camada C atualizada (6ª aplicação consecutiva D-044)
GLOSSARIO seção 5.V5 com entrada "Top-N · Bottom-N · Outliers detectados" (Bloco 4 V5)
F-EXP (Fundação) recebe requisito: renderização Excel do Bloco 2 com 2 camadas em Modo Segmentado + Bloco 4 em 3 sub-blocos com paginação se Outliers > 50

Referência canônica: /specs/dcv/dcv_v5.md §5.7 · CONTEXT §9 Camada C · §13 (candidato à formalização)

## D-105 — Taxonomia oficial V5 · 3 classes primárias com vocabulário dual + 1 especial paralela + 2 atributos derivados + 5 leituras qualitativas multi-aplicáveis
Data: 2026-04-19 · Bloco: DCV-V5 (sessão única) · Status: Fechada
Contexto: Prévio V5 §6.2 propõe 3 classes (Normal · Outlier Superior · Outlier Inferior) sem classificação especial paralela · sem atributos derivados · sem leituras qualitativas de conjunto formalizadas. Estrutura mais enxuta que padrão consolidado pós-D-073 (V7: 3 primárias + 2 especiais + 1 derivado + 5 leituras · V8: 4 + 1 · V9: 4 + 1 + 5 leituras · V4: 3 ABC + 1 + atributos compostos). Refino T-10 consolidou taxonomia V5 robusta com adaptação D-073.
Decisão: DCV-V5 §5.5 e §5.6 declaram taxonomia oficial V5 com 4 camadas:

3 classes primárias por registro com vocabulário dual técnico/exibição (T-03): NORMAL ↔ "Dentro do padrão" · OUTLIER_SUPERIOR ↔ "Acima do limite" · OUTLIER_INFERIOR ↔ "Abaixo do limite".
1 classificação especial paralela por registro: VALOR_NAO_NUMERICO — linha tem valor não-numérico no campo principal que escapou da pré-validação do upload · contada em diagnóstico agregado · não entra no cálculo estatístico · W-V5-VALOR-NAO-NUMERICO. Adaptação V5 do padrão NULO_MEDIDA · em V4/V7/V9 NULO_MEDIDA aparece como classificação por linha; em V5 NULO genuíno aparece como contagem agregada em diagnóstico (porque V5 não tem "linha-elemento" rotulada como V4/V7/V9), enquanto VALOR_NAO_NUMERICO é a única classe especial paralela por linha.
2 atributos derivados por registro: Distância do Limite (numérico · aplicável a todos os registros · positivo para outliers indicando extremidade · negativo para Normais indicando margem para virar outlier · em Z-score distância em DP · em Percentil distância em centiles) e Faixa Percentual (categórico · 6 faixas P0-P10 · P10-P25 · P25-P50 · P50-P75 · P75-P90 · P90-P100).
5 leituras qualitativas de conjunto multi-aplicáveis + Equilibrada como default sem destaque: Concentrada (CV < 0,3) · Dispersa (CV ≥ 0,7) · Assimétrica (|skewness| ≥ 0,5 · com sinal) · Multimodal (≥ 2 modas) · Com cauda relevante (≥ 5% de outliers) · Equilibrada (0,3 ≤ CV < 0,7 e nenhuma outra leitura ativa). Leituras são multi-aplicáveis (podem coexistir · não mutuamente exclusivas) — Dispersa + Assimétrica + Multimodal é combinação válida. Thresholds CV (0,3 e 0,7) e cauda (5%) são default declarado editável em Configurações avançadas (7ª aplicação consecutiva do padrão T-08). Em Modo Segmentado, cada segmento recebe seu próprio conjunto de leituras independente.

Razão: (1) Padrão "taxonomia robusta com classes + especiais paralelas + atributos derivados + leituras de conjunto" consolidado em V7/V8/V9 · 4ª aplicação em V5 com adaptação D-073. (2) Vocabulário dual técnico/exibição evita inversão silenciosa entre motor/contrato e microcopy de tela. (3) Distância do Limite é útil para auditoria (quão extremo é cada outlier?) e investigação (quão perto cada Normal está de virar outlier?) · custo de cálculo trivial. (4) Faixa Percentual é leitura rápida sem custo de cálculo extra (já computada para percentis Q1/Q3/P5/P95). (5) Leituras multi-aplicáveis (não mutuamente exclusivas como em V9 com prioridade Líder/Especialista/Equilibrado/Retaguarda) refletem natureza descritiva de V5 — uma distribuição pode ser genuinamente Dispersa + Assimétrica + Multimodal simultaneamente · forçar prioridade perderia informação.
Impacto:

dcv_v5.md §5.5 (taxonomia oficial) · §5.6 (tabela canônica das classes)
GLOSSARIO seção 5.V5 nova com 22 entradas (Classes primárias V5 · VALOR_NAO_NUMERICO · Distância do Limite · Faixa Percentual · Leituras qualitativas de conjunto · etc)
Warnings catalogados: W-V5-VALOR-NAO-NUMERICO (informativo)
Thresholds editáveis novos (3): CV-Concentrada (0,3) · CV-Dispersa (0,7) · Cauda-Relevante (5%) · 7ª aplicação consecutiva do padrão T-08
Contrato V5Result (§6 do DCV) reflete 4 camadas da taxonomia
GLOSSARIO §11 anti-glossário ganha 5 termos rejeitados V5 (Erro/Anomalia como sinônimo de outlier · Distribuição normal sem qualificar · Limpeza/correção de outliers · Distribuição típica/comportamento esperado sem qualificar · Filtragem de outliers)

Referência canônica: /specs/dcv/dcv_v5.md §5.5 · §5.6 · GLOSSARIO seção 5.V5

## D-104 — 3 critérios de outlier em V5 com defaults declarados editáveis em Configurações avançadas · 5ª aplicação consecutiva do padrão "thresholds multi-camada editáveis"
Data: 2026-04-19 · Bloco: DCV-V5 (sessão única) · Status: Fechada
Contexto: Prévio V5 §6.3 fixa defaults (IQR 1,5 · Z-score |z|>3 · Percentil P5/P95) e declara "configurável futuramente (não agora)" para Z-score e Percentil. IQR fica completamente fixo em 1,5. Esta posição conflita com padrão consolidado "thresholds multi-camada editáveis em Configurações avançadas" com 4 aplicações anteriores (V4 D-040 limiares ABC · V7 D-084 Tolerância + D-089 leituras qualitativas · V8 D-078 thresholds de leitura de ciclo · V9 D-097/D-098 8 thresholds editáveis). V5 com 3 critérios de outlier é o caso mais natural possível para o padrão — literatura e prática usam configurações alternativas com frequência (1,0 × IQR sensível · 2,0-3,0 × IQR extremo · |z|>2 alerta · |z|>3 confirmação · P1/P99 vs P5/P95 vs P10/P90). Default silencioso fixo violaria C.5 (usuário não vê threshold ativo · não sabe que poderia ter ajustado · o que conta como outlier muda materialmente conforme critério). Refino T-08 alinhou V5 ao padrão consolidado.
Decisão: DCV-V5 §4.10 declara 3 critérios de outlier com defaults declarados editáveis em Configurações avançadas:
CritérioDefault declaradoRange editávelIQR (Tukey)multiplicador 1,51,0 a 3,0 (passo 0,1)Z-score|z| > 31,5 a 4,0 (passo 0,1)PercentilP5/P95P1/P99 · P5/P95 · P10/P90 (3 opções discretas) ou par customizado simétrico
Configuração principal (E5) mostra critério escolhido + threshold ativo. Botão "Configurações avançadas" abre painel secundário com slider/dropdown editável + opção "voltar ao default". Diagnóstico registra threshold ativo na execução. Warning W-V5-THRESHOLD-NAO-DEFAULT (informativo) quando usuário edita. §4.11 declara T-MODELO V5 persiste: critério ativo · threshold ativo do critério escolhido · thresholds dos critérios não-ativos (preservados para troca rápida em re-execução) · outras configurações padrão T-MODELO geral. Bloqueio B-V5-MULTIPLOS-CRITERIOS-SIMULTANEOS impede aplicar 2+ critérios simultaneamente em uma execução.
5ª aplicação consecutiva do padrão "thresholds multi-camada editáveis em Configurações avançadas" (V4 D-040 · V7 D-084/D-089 · V8 D-078 · V9 D-097/D-098 · V5 D-104) → candidato muito forte à formalização efetiva no próximo ajuste do CONTEXT §9 Camada C.
Razão: (1) Padrão consolidado em 5 aplicações · honra C.5 (default declarado visível + edição disponível em painel secundário) · honra princípio "default declarado" (D-024) sem virar fricção UX. (2) Adaptação V5 (3 conjuntos de thresholds · 1 ativo por execução) é natural ao caso. (3) Ranges propostos cobrem literatura estatística estabelecida sem excesso de opções. (4) Percentil em opções discretas (P1/P99 · P5/P95 · P10/P90) evita escolha errática · par customizado simétrico disponível para usuário avançado. (5) T-MODELO preservando thresholds não-ativos permite troca rápida de critério em re-execução sem reconfigurar.
Impacto:

dcv_v5.md §4.10 (3 critérios com defaults editáveis) · §4.11 (T-MODELO V5 · persistência estendida)
CONTEXT §9 Camada C atualizada (padrão "thresholds multi-camada editáveis" com 5ª aplicação consecutiva · candidato muito forte à formalização)
GLOSSARIO seção 5.V5 com entrada "Critério de Outlier" + "Limite Inferior / Superior"
Warning W-V5-THRESHOLD-NAO-DEFAULT (informativo) catalogado
Bloqueio B-V5-MULTIPLOS-CRITERIOS-SIMULTANEOS catalogado

Referência canônica: /specs/dcv/dcv_v5.md §4.10 · §4.11 · CONTEXT §9 Camada C

## D-103 — Tipos de medida em V5 · Aditivo/Relativo aceitos · Não aditivo condicional com detecção de subtipo ID · Booleano bloqueado · aplicação D-073
Data: 2026-04-19 · Bloco: DCV-V5 (sessão única) · Status: Fechada
Contexto: D-025 (Sessão 1 DCV-V2) formalizou 4 tipos de campo que a plataforma reconhece e D-036 (DCV-V4) sistematizou tratamento por tipo com default declarado. V7 D-083 excluiu Booleano da natureza analítica de V7 ("média de 0/1 vira proporção · não desvio em torno de centro") · aplicação canônica de D-073. V5 precisa fazer o mesmo exercício: dos 4 tipos (Aditivo · Relativo · Não aditivo · Booleano), quais fazem sentido estatisticamente como campo principal de análise descritiva univariada com detecção de outliers? Prévio V5 §2.2 é genérico — diz "numéricos aceitos · texto/categórico/data/binário não aceitos" sem distinção fina. Refino T-05 consolidou.
Decisão: DCV-V5 §3.3 declara tabela oficial de tipos V5:

Aditivo (faturamento · quantidade · horas) → ✅ aceito · cálculo padrão sem warning específico.
Relativo (margem % · taxa · preço médio · CV) → ✅ aceito · cálculo padrão + warning informativo W-V5-RELATIVO sobre interpretação (V5 mede dispersão dos valores como observados · não dispersão ponderada por volume).
Não aditivo (estoque · contagem distinta · ID) → ⚠ condicional · cálculo padrão se subtipo é estoque ou contagem + warning informativo W-V5-NAO-ADITIVO · bloqueio se subtipo é ID detectado por heurística (§3.4).
Booleano (flag · indicador binário disfarçado) → 🚫 bloqueio estrutural B-V5-CAMPO-BOOLEANO com microcopy "V5 não opera sobre campo booleano (apenas dois valores). Para análise de presença/ausência, considere V8".

DCV-V5 §3.4 declara detecção de subtipo ID via heurística (extensão da inferência semântica D-008 do motor_upload da Fundação): campo numérico inteiro com cardinalidade ≥ 90% das linhas + (a) sequência aritmética detectável (incrementos de 1 ou constantes em ≥ 80% das diferenças consecutivas) ou (b) comprimento numérico fixo (8+ dígitos com mesma quantidade em 100% das linhas). Quando detectado, bloqueio B-V5-CAMPO-ID com escape "este campo é numérico de fato" disponível (warning permanente W-V5-ID-FORCADO no diagnóstico quando ativado).
Razão: (1) Espelho direto de V7 D-083 · aplicação canônica de D-073 (herança adaptada à natureza analítica). (2) Booleano não cabe em V5 estatisticamente (distribuição é trivialmente bimodal · IQR 0 ou 1 · outliers não existem entre dois valores possíveis) — redirecionar para V8 (presença/ausência por ponto) é coerente com a natureza de cada visão. (3) Subtipo ID dentro de Não aditivo exige tratamento específico — IQR sobre CPFs não faz sentido · tratar "Não aditivo" em bloco seria impreciso (estoque e contagem são legítimos). (4) Heurística declarada · auditável · com escape consciente honra C.5 (sistema sinaliza · não decide · usuário tem escape). (5) Extensão da inferência semântica D-008 do motor_upload aproveita arquitetura existente · zero novo requisito arquitetural estrutural.
Impacto:

dcv_v5.md §3.3 (tipos aceitos/rejeitados) · §3.4 (heurística de detecção de ID)
Requisito novo para Fundação (G-FUND): motor_upload com detecção de subtipo ID dentro da inferência semântica existente (extensão de D-008)
Warnings catalogados: W-V5-RELATIVO · W-V5-NAO-ADITIVO · W-V5-ID-FORCADO (3)
Bloqueios catalogados: B-V5-CAMPO-BOOLEANO · B-V5-CAMPO-ID (escapável) (2)
Padrão D-073 ganha aplicação V5 = V7 simétrica (ambas excluem Booleano pela mesma justificativa com adaptação ao domínio analítico específico)

Referência canônica: /specs/dcv/dcv_v5.md §3.3 · §3.4 · CONTEXT §6 (motor_upload · capabilities) · DECISIONS D-008 (inferência semântica original) · D-083 (V7 precedente)

## D-102 — Modo da base V5 declarado em granularidade · T-AGRUPA com semântica V5-específica em 3 modos · 4ª aplicação consecutiva do padrão "consolidação obrigatória pré-cálculo" adaptada por D-073
Data: 2026-04-19 · Bloco: DCV-V5 (sessão única) · Status: Fechada
Contexto: Prévio V5 §4.3 e §10 propõem explicitamente "a V5 não deve consolidar linhas duplicadas automaticamente · os registros entram na análise exatamente como chegaram · duplicidades fazem parte da distribuição observada · o motor não agrega automaticamente linhas para 'corrigir' comportamento". Esta posição conflita com padrão consolidado "consolidação obrigatória pré-cálculo com blindagem contra dupla agregação" com 3 aplicações anteriores (V8 D-074 · V7 D-082 · V9 D-092) onde T-AGRUPA roda sempre — consolida em modo Transacional e roda como no-op validado em modo Pré-agregado. Análise do conflito revelou confusão conceitual no prévio: "consolidar" significa duas coisas distintas — (a) consolidação por chave de agregação que deforma distribuição se aplicada antes da estatística descritiva (o que o prévio teme, corretamente); (b) consolidação como contrato de unidade analítica (validar unicidade da chave em base pré-agregada · no-op operacional). A unidade analítica de V5 não é "Vendedor + Mês" — é a observação individual no campo numérico. V5 olha para o conjunto de valores como observados · qualquer agregação de valores deforma. Refino T-04 alinhou V5 ao padrão consolidado com adaptação D-073.
Decisão: DCV-V5 §4.1 declara modo da base V5 em dimensão de granularidade declarada (não regra de agregação como em V4/V7/V8/V9):

Granularidade Individual (default declarado editável) — cada linha é uma observação individual (ex: extrato de transações · uma linha por venda). T-AGRUPA em modo no-op puro (passa o conjunto adiante sem operar).
Granularidade Consolidada por chave — cada linha é uma observação consolidada por chave declarada (ex: planilha com 1 linha por filial-mês). Usuário declara chave de consolidação. T-AGRUPA em modo validação de chave (verifica unicidade · gera warning estrutural W-V5-CHAVE-NAO-UNICA se duplicada).

DCV-V5 §4.2 declara T-AGRUPA em V5 · semântica V5-específica em 3 modos: (a) no-op puro · (b) validação de chave · (c) particionamento por Agrupador (Modo Segmentado · sem consolidar valores dentro do segmento). Em nenhum modo V5 consolida valores. A regra de agregação (soma · média · máximo · mínimo · contagem) que define T-AGRUPA em V4/V7/V8/V9 não se aplica em V5. Warning W-V5-GRANULARIDADE-SUSPEITA (informativo · não bloqueia) é emitido quando motor detecta possível incompatibilidade entre granularidade declarada e estrutura observada.
V5 é 8ª consumidora de T-AGRUPA com contrato V5-específico — CONTEXT §6 atualizada para refletir.
4ª aplicação consecutiva do padrão "consolidação obrigatória pré-cálculo com blindagem contra dupla agregação" (V8 D-074 · V7 D-082 · V9 D-092 · V5 D-102) → candidato muito forte à formalização efetiva no próximo ajuste do CONTEXT §9 Camada C. Aplicação canônica de D-073 (herança adaptada à natureza analítica): V5 herda a estrutura (declaração explícita do modo + validação + T-AGRUPA aplicada + diagnóstico) sem herdar o comportamento de consolidar valores (que destruiria análise descritiva univariada).
Razão: (1) Posição do prévio está corretamente motivada pelo risco de deformação da distribuição, mas operacionalmente rompe com padrão consolidado ao não ter declaração explícita de granularidade. A reformulação aceita ambas as preocupações: V5 nunca consolida valores (honra a preocupação do prévio) · mas declara granularidade e valida chave quando aplicável (honra o padrão consolidado). (2) Caso "base já agregada por design" (ex: planilha com 1 linha por filial contendo soma do faturamento mensal) precisa de tratamento — usuário esperando analisar dispersão das vendas individuais pode ter 50 valores em vez de 200.000 originais · warning W-V5-GRANULARIDADE-SUSPEITA sinaliza a possível confusão. (3) Modo de particionamento por Agrupador sem consolidação preserva observações individuais dentro de cada segmento — coerente com natureza descritiva. (4) Default declarado Individual cobre o caso comum (extratos · listagens) · escape consciente para Consolidada evita decisão silenciosa.
Impacto:

dcv_v5.md §4.1 (modo da base · granularidade declarada) · §4.2 (T-AGRUPA V5-específica em 3 modos)
CONTEXT §6 atualizada · T-AGRUPA ganha V5 como 8ª consumidora com semântica V5-específica em 3 modos · em nenhum modo V5 consolida valores · divergência canônica via D-073 documentada
CONTEXT §9 Camada C atualizada · padrão "consolidação obrigatória pré-cálculo" com 4ª aplicação consecutiva · candidato muito forte à formalização efetiva
GLOSSARIO §4 · entrada T-AGRUPA estendida com "Aplicação em V5 (D-102)" e tabela dos 3 modos V5-específicos
GLOSSARIO seção 5.V5 · entradas "Modo da Base" · "Granularidade da base" · "Unidade analítica V5"
Warnings catalogados: W-V5-CHAVE-NAO-UNICA · W-V5-GRANULARIDADE-SUSPEITA (2)

Referência canônica: /specs/dcv/dcv_v5.md §4.1 · §4.2 · CONTEXT §6 T-AGRUPA · §9 Camada C (padrão "consolidação obrigatória pré-cálculo" com 4ª aplicação consecutiva)

### D-101 — Sumário do refino DCV-V9 · 12 pendências fechadas em sessão única
Data: 2026-04-19 · Bloco: DCV-V9 (sessão única) · Status: Fechada
Contexto: Refino DCV-V9 executado em sessão única (19/04/2026) seguindo padrão D-019 + D-034 + D-033. 12 pendências originais trabalhadas (T-01 a T-12), todas fechadas, nenhuma deferida. Padrão de condução D-019 aplicado integralmente: ritual de abertura com leitura dos 4 documentos canônicos + 4 DCVs anexados (prévio V9, V7 aprovado, V8 aprovado, V4 aprovado), fila racionalizada em 4 blocos (A · Posicionamento e fronteira · B · Entrada e estrutura · C · Cálculo e classificação · D · Saída e operação), uma pendência por vez com opções explícitas e C.5 como primeira lente, mini status-checks a cada ~3 pendências, sinalização de densidade D-034 no 3º status-check com recomendação de continuar em sessão única (aprovada pela Usuária).
Decisão: DCV-V9 refinado. Consolida 12 pendências estruturais com 10 decisões específicas (D-091 a D-100) mais esta (D-101) como sumário. 40 warnings V9 catalogados (12 bloqueios · 11 alertas · 17 informativos — V9 na faixa alta do projeto entre V8 com 37 e V7 com 35). Família D · Posição relativa fechada em Fase 0 após aprovação deste DCV (V7 e V9 ambas aprovadas). Próxima Fase 0: DCV-V5 (Família E · Estrutura interna, primeira de duas visões da família; V6 fecha a Fase 0).
10 decisões consolidadas do refino:
#TemaReferênciaT-01Vocabulário canônico V9 (18 termos oficiais + anti-glossário com 5 rejeitados)dcv_v9.md §13 (consolidação terminológica, não gera D-XXX)T-02Posicionamento Família D + §2.3 "Relação com V7" simétrico + cumprimento D-081D-091 · dcv_v9.md §2.3 · dcv_v7.md §2.3 (3 células preenchidas)T-03Fronteira V9 × V4 · V9 × V5 · nota V9 × V7dcv_v9.md §2.2 (aplicação de padrão, não gera D-XXX)T-04Modo da base + Modo de Ranking (derivação da unidade analítica) + consolidação obrigatória em 4 passos + regras de agregação independentes por métricaD-092 · dcv_v9.md §4.1 · §4.2 · §4.3 · §4.7T-05Múltiplas métricas + direção obrigatória sem default + T-SEMA múltiplo com efeito no cálculo + limites operacionais 2-10D-093 · dcv_v9.md §4.4 · §4.5 · §4.6 · §4.8T-06Escalas heterogêneas + não-normalização como posição estrutural + 5 alternativas rejeitadas + teste de razão de amplitude 1000×D-094 · dcv_v9.md §4.9 · §4.10T-07Score consolidado (média aritmética simples) + 4 alternativas rejeitadas + tratamento de nulos em 2 camadas (score parcial × NULO_MEDIDA)D-095 · dcv_v9.md §5.3T-08Rank mínimo + desempate visual 4 níveis + V9 como sétima consumidora T-RANK com regra V9-específica + novo escopo cross_elementos_dentro_do_agrupadorD-096 · dcv_v9.md §5.4T-09Variação Máxima de Posição + 4 alternativas rejeitadas + threshold Especialista 50% default declarado editávelD-097 · dcv_v9.md §5.5T-10Taxonomia oficial (4+1+5) + critérios percentuais default declarados editáveis + expansão por empate + arredondamento ceil em N pequenoD-098 · dcv_v9.md §5.6T-11Resumo Executivo 6 blocos (padrão D-044) + Excel 6 abas com Mapa de Perfil como coração visual V9 + Dados Brutos descartada + nota estática redirecionamento V5/V7/V4D-099 · dcv_v9.md §5.7 · §5.8 · §5.9T-1212 bloqueios operacionais + escala multi-eixo independente + 9 diretrizes performance (7 herdadas + 2 V9) + 11 candidatos P-V9-XX-EvoD-100 · dcv_v9.md §7 · §8 · §12
Razão: (1) Sessão única validou novamente que refino denso pode caber em uma sessão quando o prévio é maduro taxonomicamente (V9 tinha Parte 6.6/6.7 já normativa com 4 classes) e a maioria das pendências herda padrões consolidados (V7 para modo da base, V4 para defaults declarados, D-073 para herança adaptada). (2) Retroação diferida V7→V9 cumprida na sessão natural do refino (D-091 · padrão previsto em D-081 "cumprimento em sequência direta") — as 3 células marcadas (a confirmar em DCV-V9) no DCV-V7 aprovado ficam preenchidas, par autônomo Família D fechado dos dois lados. (3) Contrato de T-SEMA estendido estruturalmente pela primeira vez — V9 é a primeira consumidora com contrato por métrica e efeito direto no cálculo; divergência vs V7 D-087 justificada explicitamente via padrão "herança adaptada à natureza analítica" D-073 (10ª aplicação documentada). (4) Kit D-033 completo em sessão única validado pela quinta vez consecutiva (precedentes V10 · V3 · V8 · V7 · V9) — padrão operacional consolidado.
Impacto:

1 DCV aprovado a mais → 9 de 11 DCVs aprovados na Fase 0 (V2, V1, V11, V4, V10, V3, V8, V7, V9) após aprovação formal deste
Fila remanescente Fase 0: V5 → V6 (2 DCVs, Família E · Estrutura interna)
Família D · Posição relativa fechada em Fase 0 (ambas as visões com DCV aprovado)
40 warnings V9 catalogados · V9 na faixa alta do projeto (V8=37, V7=35)
T-AGRUPA ganha V9 como consumidora com regra de agregação independente por métrica (contrato multi-regra inédito)
T-SEMA ganha V9 como sétima consumidora com contrato por métrica + efeito direto no cálculo (primeira com esse contrato · aplicação D-073)
T-RANK ganha V9 como sétima consumidora com regra V9-específica em 4 níveis + novo escopo cross_elementos_dentro_do_agrupador
Padrão "herança adaptada à natureza analítica" D-073 ganha 6 novas aplicações (ver D-091 a D-100)
Padrão "default declarado" aplicado em 7 dimensões V9 (modo da base, regra de agregação por métrica, nome analítico por métrica, threshold Líder 20%, threshold Retaguarda 20%, threshold Especialista 50%, thresholds de 5 leituras qualitativas)
Padrão "consolidação obrigatória pré-cálculo" com 3ª ocorrência consecutiva (V8 D-074 · V7 D-082 · V9 D-092) — candidato forte à formalização em CONTEXT §9
Padrão "Dados Brutos descartada em favor de Base Analítica + Diagnóstico" com 3 aplicações consecutivas (V8 D-078 · V7 D-089 · V9 D-099) — candidato à formalização
Padrão "Resumo Executivo 6 blocos D-044" com 5ª aplicação consolidada — candidato à formalização em CONTEXT §13
Próximo bloco: DCV-V5 (primeira visão da Família E · Estrutura interna)

Referência canônica: /specs/dcv/dcv_v9.md · D-091 a D-100 · CONTEXT §4 Família D · §6 T-AGRUPA/T-SEMA/T-RANK · GLOSSARIO §4 T-AGRUPA/T-SEMA/T-RANK · §5.V9 · §6 Warnings V9 · §10 Retroação diferida V7→V9 cumprida · §11 anti-glossário V9

### D-100 — Bloqueios operacionais V9 + escala de cardinalidade multi-eixo + 9 diretrizes de performance + roadmap P-V9-XX-Evo com 11 candidatos
Data: 2026-04-19 · Bloco: DCV-V9 (sessão única) · Status: Fechada
Contexto: Prévio V9 (Parte 2.7, 7.3, 15, 16) lista alertas não bloqueantes e pontos de atenção em linguagem genérica, sem matriz de bloqueios estruturais e sem patamares operacionais numerados como V7 §8.1 e V8 §8. Precisa consolidar bloqueios, cardinalidade, performance e roadmap em formato padronizado. Refino T-12 consolidou os 4 sub-temas.
Decisão: DCV-V9 §7 declara 12 bloqueios operacionais estruturais numerados (análogo V7 §8.1). §8.1 declara escala de cardinalidade em 3 eixos multi-dimensionais independentes (N Identificadores em 7 patamares · N Métricas em 5 patamares · Cardinalidade do Agrupador em 4 patamares). §8.4 declara 9 diretrizes de performance (7 herdadas V3/V8/V7 + 2 específicas V9: ordenação por métrica paralelizável + matriz pivotada Identificador × Métrica em passe único). §12 declara roadmap P-V9-XX-Evo com 11 candidatos consolidados do refino (pesos por métrica · detecção automática de Direção opt-in · normalizações Z-score/Min-max/Log-scale · ranking padronizado · identificador composto · múltiplos agrupadores · percentil complementar · comparação entre períodos · leituras mais granulares).
Estrutura multi-eixo independente (aplicação D-073): V9 é distinta de V7 (hierárquica-aditiva: elementos dentro de grupos) e V8 (matricial multiplicativa: matriz aninhada). Em V9, os 3 eixos (Identificadores · Métricas · Agrupadores) são recortes ortogonais do dado — crescem independentemente, combinam-se sem aninhamento obrigatório. Custo computacional escala como O(N · M log N).
Anti-roadmap registrado: "Score composto ponderado sobre valores normalizados" — descaracterizaria V9 (convergeria em V4 Modo 3 ou vira nova visão). Registrado explicitamente fora do escopo V9 para memória institucional.
Razão: (1) Padrão de escalas de cardinalidade com patamares numerados consolidado em V7/V8/V9 (3 aplicações · cada uma adaptada à natureza analítica D-073). (2) Diretrizes de performance como tronco comum (7 herdadas) + específicas V9 (2) reforça uniformidade + adaptação justificada. (3) Roadmap com rastreio de origem (pendência T-XX) mantém rastreabilidade de decisões rejeitadas no MVP para evolução futura — memória institucional sólida. (4) Bloqueios estruturais numerados evitam que implementação invente comportamentos em casos-limite (C.3 honrado).
Impacto:

dcv_v9.md §7 (12 bloqueios) · §8 (escala 3 eixos · 9 diretrizes performance) · §12 (11 candidatos P-V9-XX-Evo)
F-MOT (Fundação) recebe requisitos de 12 pré-validações estruturais
F-EXP (Fundação) recebe requisito: matriz pivotada em passe único para aba Mapa de Perfil
F-TRANS (Fundação) recebe requisito: ordenação por métrica como passe independente (candidato a paralelização futura)
Total de warnings V9 atinge 40 com esta pendência (12 bloqueios · 11 alertas · 17 informativos)
CONTEXT §4 Família D atualizada (aplicação D-073 na escala de cardinalidade — 3 famílias com 3 estruturas distintas de escala documentadas)

Referência canônica: /specs/dcv/dcv_v9.md §7 · §8 · §12 · CONTEXT §9 Camada C (candidato a formalização de padrão de escala)

### D-099 — Resumo Executivo V9 6 blocos + Exportação Excel 6 abas com Mapa de Perfil como coração visual + Dados Brutos descartada + nota estática redirecionamento
Data: 2026-04-19 · Bloco: DCV-V9 (sessão única) · Status: Fechada
Contexto: Prévio V9 (Parte 7.3, 10.2) declara 10 indicadores principais sem estrutura 6 blocos D-044 e 4 abas oficiais (Ranking Completo · Resumo por Classificação · Perfil por Métrica · Dados Brutos) sem Resumo Executivo como 1ª aba, sem Diagnóstico obrigatório como última (D-017), e com Dados Brutos preservada. Padrão consolidado V4/V3/V8/V7: 6 blocos + 6 abas + Diagnóstico última + Dados Brutos descartada. Refino T-11 consolidou estrutura completa aplicando o padrão com adaptações V9.
Decisão consolidada:
Resumo Executivo · 6 blocos fixos (padrão D-044 adaptado):

Bloco 1 Cabeçalho · Bloco 2 Números-âncora (N por classe + Melhor/Pior Score + Maior/Menor Variação Máxima) · Bloco 3 Distribuição das 4 classes primárias (com breakdown condicional por agrupador no modo Segmentado) · Bloco 4 Elementos destacados (Top 5 Líderes + Top 5 Retaguarda + Top 3 Especialistas + Top 3 Equilibrados + Top 3 Pos 1 por métrica) · Bloco 5 Leitura qualitativa do conjunto + síntese agregada + thresholds ativos + nota estática de redirecionamento (V5 · V7 · V4 com linguagem declarativa) · Bloco 6 Qualidade estrutural (decomposição por cobertura K parcial).

Exportação Excel · 6 abas oficiais: Resumo Executivo · Ranking Completo · Perfil por Métrica (aba única com blocos empilhados por métrica) · Mapa de Perfil (matriz Identificador × Métrica com valor = Posição, coloração condicional respeitando Direção, destaque de Pos 1 e Pior Posição · coração visual V9) · Parâmetros · Diagnóstico última (D-017). Aba Dados Brutos do prévio descartada (herança V8 D-078 · V7 D-089 · 3ª aplicação consecutiva do padrão).
Mapa de Perfil como coração visual V9: análogo estrutural a Matriz de Presença V8 (D-077) e Mapa de Grupos V7 (D-089) — peça de valor única que só a visão produz. Linhas predominantemente em cor positiva = Líderes; predominantemente em cor negativa = Retaguarda; com forte variação de cor = Especialistas. Transforma leitura multidimensional em leitura visual imediata.
Nota estática de redirecionamento (Bloco 5 Parte 5D):

"Para análise de dispersão estatística interna de uma métrica individual (IQR, outliers, distribuição), considere V5 · Comportamento e Dispersão. Para análise de desvio intra-grupo em uma única medida contra a média do grupo, considere V7 · Desvio em Relação à Média do Grupo. Para análise de participação de elementos no total com comparação de distribuição entre medidas, considere V4 · Composição e Participação."

Nota aparece apenas no Resumo Executivo Bloco 5 Parte 5D, nunca em interface operacional (E1-E5). Padrão consolidado V7 D-089.
Razão: (1) Padrão 6 blocos D-044 consolidado agora em 5 visões (V4 · V3 · V8 · V7 · V9) — candidato forte à formalização em CONTEXT §13 como padrão estrutural de produto. (2) Mapa de Perfil como coração visual multidimensional — V9 é a única visão que pode entregar "perfil visual" por elemento em N dimensões simultâneas; formato matriz pivotada é expressão direta da natureza analítica. (3) Aba Dados Brutos descartada pelo mesmo rationale V8/V7 (Base Analítica cobre auditoria; Diagnóstico registra linhas originais vs consolidadas) — 3ª aplicação consecutiva do padrão, candidato à formalização. (4) Nota estática com 3 redirecionamentos ordenados por proximidade analítica (V5 e V7 são Família D/E próximas; V4 é Família C complementar) — linguagem declarativa autossuficiente.
Impacto:

dcv_v9.md §5.7 (6 blocos · padrão D-044) · §5.8 (6 abas com Mapa de Perfil) · §5.9 (nota estática)
F-EXP (Fundação) recebe requisito: aba Mapa de Perfil como matriz pivotada com coloração condicional por célula + destaques de extremos · capability generalizada capaz de servir V7 Mapa de Grupos + V8 Matriz de Presença + V9 Mapa de Perfil
CONTEXT §9 Camada C ganha registro do padrão "Dados Brutos descartada" com 3 aplicações consecutivas (candidato a formalização)
CONTEXT §13 eventualmente ganha padrão "Resumo Executivo 6 blocos" como estrutura formal de produto (5 aplicações consolidadas)

Referência canônica: /specs/dcv/dcv_v9.md §5.7 · §5.8 · §5.9

### D-098 — Taxonomia oficial V9 · 4 classes primárias com prioridade declarada + NULO_MEDIDA especial + 5 leituras qualitativas de conjunto + critérios percentuais default declarados editáveis + expansão por empate + arredondamento ceil em N pequeno
Data: 2026-04-19 · Bloco: DCV-V9 (sessão única) · Status: Fechada
Contexto: Prévio V9 (Parte 6.6, 6.7, 6.8) declara normativamente 4 classes (Líder · Especialista · Equilibrado · Retaguarda) + prioridade (Líder → Retaguarda → Especialista → Equilibrado) + critérios 20%/20%/50%, sem marcar editabilidade, sem tratamento de casos-limite (N pequeno, empates no corte), sem leitura qualitativa de conjunto. V7 D-086 consolidou padrão em 3 camadas (primárias + especiais + leitura qualitativa). Refino T-10 aplicou o padrão com adaptações V9.
Decisão: Taxonomia oficial V9 em 3 camadas complementares:
Camada 1 · Classes primárias (4 mutuamente exclusivas, aplicadas por prioridade Líder → Retaguarda → Especialista → Equilibrado):

Líder — score_consolidado ≤ percentil_20 (top 20%)
Retaguarda — score_consolidado ≥ percentil_80 (bottom 20%)
Especialista — variacao_maxima_posicao ≥ 50% × N_elementos_validos, desde que não já Líder ou Retaguarda
Equilibrado — residual

Camada 2 · Classificação especial paralela: NULO_MEDIDA — elemento com 0 métricas válidas (§5.3 Camada 2). Não entra no cálculo de percentis; conjunto analisado efetivo = N total − N NULO_MEDIDA.
Camada 3 · Leitura qualitativa de conjunto (Resumo Executivo Bloco 5): 5 leituras (Homogêneo ≥70% Equilibrados · Concentrado N Líderes+Retaguarda ≥50% · Especializado ≥30% Especialistas · Misto residual · Degenerado N<5 ou ≥30% NULO_MEDIDA). Ordem de teste: Degenerado → Especializado → Concentrado → Homogêneo → Misto.
Critérios percentuais default declarados editáveis (padrão V7 D-084 · V4 D-040):

Líder: 20% default · faixa 5-40% (threshold_lider_pct)
Retaguarda: 20% default · faixa 5-40% (threshold_retaguarda_pct)
Especialista: 50% default · faixa 30-70% (threshold_especialista_pct · já em D-097)

Constraint operacional: lider_pct + retaguarda_pct ≤ 90% (garante pelo menos 10% para Equilibrado/Especialista). Violação → W-V9-THRESHOLDS-INVALIDOS (bloqueio em E3).
Caso-limite · conjunto com N < 5 elementos válidos: executa com alerta forte (W-V9-CONJUNTO-PEQUENO já em D-097) aplicando arredondamento ceil nos thresholds para garantir pelo menos 1 Líder e 1 Retaguarda (N=3 · top 20% = ceil(0,6) = 1). Arredondamento canônico deterministico (C.1).
Caso-limite · empate no score no ponto de corte: expansão por empate — elemento na fronteira com score empatado com imediatamente posterior entra na mesma classe. Classes podem crescer além do threshold. W-V9-CLASSE-EXPANDIDA-POR-EMPATE (informativo) registra. Aplicação direta de C.5 (não decidir arbitrariamente entre equivalentes matemáticos).
Rejeitados explicitamente: (a) extensão para 5 classes (Super Líder · Líder · Especialista · Equilibrado · Retaguarda) — granularidade já comunicada pelo Score Consolidado e Variação; (b) thresholds fixos não editáveis — violaria C.5; (c) corte arbitrário entre empates em favor da ordem alfabética no ponto de corte — decide entre equivalentes.
Razão: (1) Padrão "herança adaptada à natureza analítica" D-073 aplicado (9ª aplicação): V7 tem 3 classes primárias (univariada contínua com direção); V8 tem 4 por ponto + 1 consolidada (sequencial com estados qualitativos); V9 tem 4 classes primárias combinando dois eixos (score + variação) — natureza multidimensional produz 4. (2) Prioridade Líder → Retaguarda → Especialista → Equilibrado respeita hierarquia de leitura executiva (extremos de score primeiro; dispersão depois; residual por último). Prioridade explícita elimina ambiguidade quando elemento qualifica em múltiplas. (3) Expansão por empate é aplicação estrita de C.5 em ponto delicado — cortar arbitrariamente entre scores idênticos embute decisão do sistema sobre equivalentes matemáticos. (4) ceil em N pequeno garante que Líder/Retaguarda tenham pelo menos 1 elemento (não degeneram para 0 quando N×20% < 1). (5) Leitura qualitativa de conjunto no Bloco 5 análoga V7 Bloco 5 (D-086) e V8 Bloco 5 (D-078) — padrão de produto consistente.
Contrato V9Result (síntese):

classificacao enum 5 valores: Lider · Especialista · Equilibrado · Retaguarda · Nulo_Medida
leitura_conjunto enum 5 valores no nível do conjunto
classe_expandida_por_empate bool no nível do conjunto

Impacto:

dcv_v9.md §5.6 (taxonomia em 3 camadas · critérios · casos-limite)
F-MOT (Fundação) recebe requisitos: (1) cálculo de percentis com arredondamento ceil, (2) regra de expansão por empate no ponto de corte, (3) prioridade de classe primária em 4 níveis, (4) leitura qualitativa de conjunto em passe único com ordem de teste fixa
GLOSSARIO §5.V9 ganha entradas "Classes primárias V9" · "Prioridade de classificação" · "NULO_MEDIDA V9" · "Leituras qualitativas de conjunto V9" · "Expansão por empate" · "Arredondamento ceil em N pequeno"
10 warnings novos catalogados (thresholds default/custom · leitura default/custom · classe expandida · thresholds inválidos · elementos insuficientes reforço · conjunto homogêneo)

Referência canônica: /specs/dcv/dcv_v9.md §5.6

### D-097 — Variação Máxima de Posição V9 · amplitude ordinal pior−melhor + 4 alternativas rejeitadas + threshold Especialista 50% default declarado editável + casos-limite
Data: 2026-04-19 · Bloco: DCV-V9 (sessão única) · Status: Fechada
Contexto: Prévio V9 (Parte 6.5) declara fórmula pior_posicao − melhor_posicao e interpretação (alta = especialização; baixa = equilíbrio). Parte 6.7 cita threshold Especialista "≥ 50% do total de elementos válidos" sem marcar editabilidade, sem rationale, sem tratamento de score parcial e casos-limite (N pequeno, conjunto homogêneo, elemento com K=1 métrica). Refino T-09 formalizou indicador completo aplicando padrões consolidados.
Decisão: Variação Máxima de Posição = max(posicao_por_metrica_valida) − min(posicao_por_metrica_valida), calculada apenas sobre métricas em que o elemento tem posição válida (§5.3 Camada 1 cobertura parcial). Unidade: número inteiro positivo (ou zero). Indicador ordinal de especialização × equilíbrio relativo ao tamanho do conjunto.
Alternativas avaliadas e rejeitadas no MVP:
AlternativaPor que foi rejeitadaP-V9-XX-EvoDesvio padrão das posiçõesPressupõe distribuição; σ frágil com N pequeno (2-6 métricas)P-V9-0X-EvoAmplitude normalizada (pior−melhor)/(N−1)Perde grão interpretativo; threshold Especialista já normaliza implicitamenteP-V9-0X-Evo (baixa)Coeficiente de variaçãoNumericamente ruim com médias baixasNão candidatoDiferença pior − medianaDescarta lado "bom"; perde simetriaP-V9-0X-Evo
Threshold Especialista: 50% default declarado editável (padrão V7 D-084 · V4 D-040):

Default 50% (threshold_especialista_pct) · faixa aceitável 30%-70%
Rationale 50%: meio do conjunto é ponto de corte simétrico e interpretável ("variação atravessa metade do ranking")
Valores <30% tornam Especialista muito frequente (sinal dilui); >70% tornam raro (perde utilidade)
Modo Segmentado: threshold calculado por agrupador
W-V9-THRESHOLD-ESPECIALISTA-DEFAULT (informativo) · W-V9-THRESHOLD-ESPECIALISTA-CUSTOM (informativo)

Casos-limite:

N = 2 elementos: variação máxima possível = 1; executa com alerta forte (W-V9-CONJUNTO-PEQUENO)
Conjunto homogêneo (todos empatados em todas métricas): variação = 0 para todos (W-V9-CONJUNTO-HOMOGENEO informativo)
Elemento com K = 1 métrica válida: variação = 0 (falso equilíbrio); não elegível a Especialista (sinal de dispersão não existe sobre 1 dimensão)
Elemento NULO_MEDIDA: variação indefinida (sem posições)

Exposição na saída: V9Result preserva 3 colunas por elemento (melhor_posicao, pior_posicao, variacao_maxima_posicao · int nullable cada). Aba Ranking Completo permite usuário ordenar visualmente por variação para inspecionar especialistas mesmo fora da classificação oficial.
Razão: (1) Padrão "herança adaptada à natureza analítica" D-073 aplicado (8ª aplicação): V5 futura usará IQR/Z-score (normalização estatística intra-campo); V7 usa desvio percentual (normalização implícita por grupo via média); V9 usa amplitude ordinal pior−melhor (substrato ordinal do score). Cada uma justificada pela natureza analítica. (2) Amplitude simples combina interpretabilidade ordinal (variação 11 = "elemento varia 11 posições"), invariância à distribuição (não pressupõe normal), adequação a N pequeno de métricas (2-6). (3) Threshold 50% em "Configurações avançadas" aplica padrão D-044 (defaults declarados editáveis) sem fricção UX para maioria dos casos. (4) Elemento K=1 não elegível a Especialista blinda contra falso equilíbrio — sinal de dispersão requer pelo menos 2 dimensões. (5) Casos-limite com warnings (CONJUNTO-PEQUENO · CONJUNTO-HOMOGENEO) sinalizam limitação de leitura sem mascarar o fato (C.5).
Contrato V9Result:
elementos[]:
  melhor_posicao: int | None  # min sobre métricas válidas
  pior_posicao: int | None    # max sobre métricas válidas
  variacao_maxima_posicao: int | None  # pior − melhor
Impacto:

dcv_v9.md §5.5 (Variação Máxima + alternativas + threshold + casos-limite)
Bloco 4 do Resumo Executivo inclui Top 3 maior variação + Top 3 menor variação (entre elementos com K=N métricas)
F-MOT recebe requisito: cálculo de Variação Máxima sobre métricas válidas + regra especial K=1 não elegível a Especialista
4 warnings novos: W-V9-CONJUNTO-PEQUENO (alerta forte), W-V9-CONJUNTO-HOMOGENEO (informativo), W-V9-THRESHOLD-ESPECIALISTA-DEFAULT (informativo), W-V9-THRESHOLD-ESPECIALISTA-CUSTOM (informativo)

Referência canônica: /specs/dcv/dcv_v9.md §5.5

### D-096 — V9 como sétima consumidora de T-RANK · regra de desempate V9-específica em 4 níveis + novo escopo cross_elementos_dentro_do_agrupador + rank mínimo formalizado
Data: 2026-04-19 · Bloco: DCV-V9 (sessão única) · Status: Fechada
Contexto: Prévio V9 (Parte 6.3) declara rank mínimo para Posição por Métrica + desempate visual em 2 níveis (valor bruto, alfabético). CONTEXT §6 T-RANK lista V9 como consumidora sem detalhar regra V9-específica. V7 D-088 consolidou aplicação de T-RANK em 4 níveis adaptada via D-073. Refino T-08 formalizou V9 como sétima consumidora com regra própria, adicionou nível 3 para determinismo absoluto (C.1), e formalizou distinção empate-no-cálculo × empate-visual.
Decisão: V9 é sétima consumidora de T-RANK com contrato em 2 contextos de uso:
(a) Atribuição de Posição por Métrica (Passo 3 do pipeline): rank mínimo — elementos com mesmo valor consolidado em uma métrica recebem mesma Posição (a menor disponível); elementos subsequentes continuam a partir de N_anteriores + 1. Equivalente a pandas.Series.rank(method='min') e SQL RANK(). Empate é preservado como fato analítico, não desempatado artificialmente.
(b) Desempate visual determinístico das linhas (ordenação no Excel e tela) em 4 níveis:

Score Consolidado crescente (menor = primeiro na ordem visual)
Variação Máxima de Posição crescente (elemento mais equilibrado primeiro quando scores empatam)
Nome do Identificador alfabético case-insensitive
Ordem de inserção original

Tolerância floating point: 1e-9 (herança D-041 · D-088).
Adaptação vs V7 D-088: nível 2 V7 é abs(desvio_absoluto) (magnitude em unidades absolutas); nível 2 V9 é Variação Máxima de Posição crescente — captura intuição de "quando score é igual, equilíbrio desempata". Elemento com score 2,0 e variação 1 aparece antes de elemento com score 2,0 e variação 5.
Novo escopo adicionado ao enum escopo de T-RANK: cross_elementos_dentro_do_agrupador (modo Segmentado V9) — distinto de intra_grupo (V7, com Grupo como campo dedicado formando unidade Elemento+Grupo) e global (V4/V10/V11 · sem segmentação). Modo Global V9 usa global; modo Segmentado V9 usa o novo escopo.
Distinção empate-no-cálculo × empate-visual:

Empate de valor consolidado em uma métrica → rank mínimo preservado na Posição (não desempatado)
Empate de score consolidado → não é desempatado para classificação (dois elementos com mesmo score podem ambos ser Líderes se caem no top 20%)
Empate de score consolidado → desempate aplicado apenas para ordenação visual das linhas

Razão: (1) Padrão "herança adaptada à natureza analítica" D-073 (10ª aplicação documentada): D-041 default em 3 níveis (valor → agrupadores → inserção); V7 em 4 níveis (|%| → |abs| → Elemento alfabético → inserção); V9 em 4 níveis adaptados (score → variação → Identificador alfabético → inserção). Cada adaptação justificada. (2) Rank mínimo preserva sinal analítico do empate em vez de artificializar ordem — se 3 elementos estão "empatados em Pos 1", todos recebem Pos 1 no cálculo. (3) Variação Máxima como nível 2 (em vez de alfabético direto) preserva informação analítica de dispersão antes de cair em desempate textual — elemento mais equilibrado é visualmente "primeiro" entre scores iguais. (4) Novo escopo cross_elementos_dentro_do_agrupador ≠ intra_grupo V7 porque em V7 o Grupo forma unidade analítica com o Elemento (consolidação é Grupo+Elemento · cálculo de média é intra-grupo); em V9 o Agrupador apenas segmenta o conjunto (consolidação é Identificador+Agrupador · cálculo de posições é cross-elementos dentro do recorte do agrupador). Distinção semântica clara no contrato. (5) Desacoplamento empate-cálculo × empate-visual respeita C.5 — sistema não "decide" quem é melhor entre empates no score; preserva equivalência e apenas ordena visualmente com critério determinístico (C.1).
Contrato T-RANK atualizado (extensão D-041 · D-088):
T-RANK(elementos, criterio_principal, regra_desempate, escopo)
  escopo = enum [global, intra_grupo, cross_elementos_dentro_do_agrupador]
  regra_desempate = lista de critérios nomeados específica da visão
  tolerancia_float = 1e-9
Impacto:

dcv_v9.md §5.4 (rank mínimo + desempate 4 níveis + distinção cálculo × visual)
CONTEXT §6 T-RANK atualizado: V9 adicionada como 7ª consumidora com regra V9-específica + novo escopo
GLOSSARIO §4 T-RANK ganha bloco "Aplicação em V9" com contrato em 2 contextos
F-TRANS (Fundação) recebe requisito: T-RANK aceita novo escopo cross_elementos_dentro_do_agrupador
W-V9-RANK-EMPATE (informativo) catalogado

Referência canônica: /specs/dcv/dcv_v9.md §5.4 · CONTEXT §6 T-RANK · D-041 (contrato transversal base) · D-088 (adaptação V7)

### D-095 — Score Consolidado V9 · média aritmética simples das posições válidas + 4 alternativas rejeitadas + tratamento de nulos em 2 camadas (score parcial × NULO_MEDIDA)
Data: 2026-04-19 · Bloco: DCV-V9 (sessão única) · Status: Fechada
Contexto: Prévio V9 (Parte 6.4) declara normativamente média aritmética simples das posições como score consolidado; Parte 6.10 cita tratamento de nulos genérico ("não converter em zero, registrar, preservar rastreabilidade") sem tratamento estrutural de nulos parciais vs totais. V7 D-085 estabeleceu NULO_MEDIDA como binário (1 medida). V9 precisa decidir: elemento com K < N métricas válidas continua no ranking com score parcial, ou vira NULO_MEDIDA inteiro? Refino T-07 formalizou score + alternativas + tratamento de nulos em 2 camadas.
Decisão: Score Consolidado = média aritmética simples das Posições por Métrica válidas de cada Identificador:
score_consolidado = soma(posicao_por_metrica_valida) / N_metricas_validas_do_elemento
Quanto menor, melhor o posicionamento geral. Equal-weighted por arquitetura (pesos em P-V9-01-Evo).
Alternativas avaliadas e rejeitadas no MVP:
AlternativaPor que foi rejeitadaCandidatoSoma das posiçõesMatematicamente idêntica à média × N fixo (transformação monotônica); menos interpretávelFora de P-V9 (equivalente)Mediana das posiçõesDescarta extremos — elemento Pos 1 em 2 métricas e Pos 50 em 3 teria mediana 50 (ignora liderança); distorce especializaçãoNova visão futuraMédia geométricaPenaliza posições ruins desproporcionalmente; interpretação não-ordinal em espaço de posiçõesP-V9-0X-EvoMédia ponderada com pesos por métricaEmbute hierarquia entre métricas — viola C.5 ou descaracteriza V9P-V9-01-Evo
Tratamento de nulos em 2 camadas (herança V7 D-085 adaptada via D-073):
Camada 1 · Cobertura parcial (K < N métricas válidas, K ≥ 1) — Score parcial com warning:

Elemento permanece no ranking com score calculado sobre K válidas
n_metricas_validas registrado por elemento no V9Result
W-V9-METRICA-PARCIAL (alerta regular) sinaliza ao usuário
Caveat declarado: score parcial é menos comparável; elemento com K=1 tem variação 0 "falsa" e não é elegível a Especialista (D-097)

Camada 2 · Cobertura zero (0 métricas válidas) — NULO_MEDIDA:

Elemento sem nenhum valor válido em nenhuma das N métricas (consolidação T-AGRUPA retornou nulo em todas)
Classificação = NULO_MEDIDA (especial paralela · D-098)
Não entra no ranking; não recebe Posição em nenhuma métrica; score nulo
Não entra no cálculo de percentis 20/80 (conjunto analisado efetivo = N total − N NULO_MEDIDA)
W-V9-ELEMENTO-NULO (alerta forte)
V9Result preserva o elemento com campos nulos para auditoria (C.5 — não sumir silenciosamente)

Casos adicionais:

Métrica 100% nula: bloqueio em E3 (W-V9-METRICA-TOTAL-NULA) — usuário decide remover a métrica ou cancelar execução; manter degeneraria todos os elementos em NULO_MEDIDA
Métrica 100% zerada: prossegue com alerta forte (W-V9-METRICA-ZERADA) — métrica não discrimina (todos elementos recebem Pos 1 naquela métrica), mas execução permanece viável

Divergência vs V7 D-085 justificada (D-073 · 5ª aplicação V9): V7 tem 1 medida (nulo nela = NULO_MEDIDA binário · elemento sai do ranking). V9 tem 2-6 métricas (nulo em 1 de 4 ainda permite score sobre 3 válidas). Descartar elemento com K < N seria descartar informação analítica legítima; absorver silenciosamente mudaria interpretação do score sem aviso. Solução em 2 camadas respeita natureza multidimensional sem mascarar o fato.
Razão: (1) Média simples é a única agregação que não embute hierarquia entre métricas — padrão C.5 equal-weighted explícito. (2) Interpretabilidade "score 1,0 = primeiro em tudo; score 3,5 = média de 3ª-4ª posição" é transparente; soma daria "score 14 em 4 métricas = quarto lugar médio" menos intuitivo apesar de equivalente. (3) Score parcial preserva sinal das métricas válidas em vez de descartar elemento — decisão C.5 pura (não decidir que "falta de dados = dados zerados"). (4) NULO_MEDIDA apenas quando 0 válidas é honesto sobre limite do cálculo — elemento sem qualquer dimensão não tem score definível. (5) Métrica 100% nula como bloqueio (não alerta) porque manter degenera execução inteira — decisão forçada em E3 é única saída clean. (6) Métrica 100% zerada prossegue porque é caso analítico legítimo (métrica que não discrimina ainda contribui ao ranking — todos empatados em Pos 1 daquela métrica).
Contrato V9Result:
elementos[]:
  score_consolidado: float | None  # None quando NULO_MEDIDA
  n_metricas_validas: int  # 0 quando NULO_MEDIDA
  classificacao: enum [Lider, Especialista, Equilibrado, Retaguarda, Nulo_Medida]
Impacto:

dcv_v9.md §5.3 (score + alternativas + 2 camadas de nulos)
F-MOT (Fundação) recebe requisito: pré-validação de cobertura de nulos por elemento e por métrica antes do Passo 2 (ordenação)
5 warnings novos: W-V9-METRICA-PARCIAL (alerta), W-V9-ELEMENTO-NULO (alerta forte), W-V9-METRICA-TOTAL-NULA (bloqueio), W-V9-METRICA-ZERADA (alerta forte), W-V9-SCORE-CALCULADO (informativo)
GLOSSARIO §5.V9 ganha entradas "Score Consolidado" · "Score parcial" · "NULO_MEDIDA V9"
Padrão "herança adaptada à natureza analítica" D-073 ganha 5ª aplicação V9

Referência canônica: /specs/dcv/dcv_v9.md §5.3

### D-094 — Escalas heterogêneas entre métricas V9 · posição estrutural sobre não-normalização + 5 alternativas de normalização rejeitadas no MVP + teste de razão de amplitude 1000× + pesos por métrica fora de escopo
Data: 2026-04-19 · Bloco: DCV-V9 (sessão única) · Status: Fechada
Contexto: Prévio V9 (Parte 2.7, 4.5, 4.6) cita escalas heterogêneas como alerta + declara "motor não normaliza valores automaticamente" + cita pesos por métrica como fora de escopo MVP, sem justificar arquiteturalmente nem listar alternativas avaliadas. Refino T-06 formalizou posição estrutural + alternativas rejeitadas + warning de heterogeneidade detectada + ratificação sobre pesos.
Decisão: V9 não normaliza valores de métrica em nenhuma hipótese. Escalas heterogêneas entre métricas (Faturamento em R$ de milhões, Taxa em decimais, Tempo em minutos) são neutralizadas pela natureza ordinal da Posição — o substrato do score consolidado é a Posição, não o valor. Duas métricas de escalas completamente diferentes contribuem igualmente para o score porque o que entra no cálculo é a Posição do elemento em cada uma, não o valor. Posição respeita C.5: sistema não toma decisão de transformação de escala sobre o dado do usuário.
Alternativas de normalização avaliadas e rejeitadas no MVP:
AlternativaPor que foi rejeitadaP-V9-XX-EvoZ-score por métricaPressupõe distribuição normal (raro em indicadores de negócio); decide silenciosamente transformar o dado; posições ordinais já neutralizam escalasP-V9-03-EvoMin-max [0,1]Elimina invariância a outliers extremos; transformação silenciosa contra C.5P-V9-04-EvoLog-scalePressupõe distribuição log-normal; não aplicável a métricas zero ou negativasP-V9-05-EvoRanking padronizado (Posição/N)Transformação monotônica; adiciona complexidade sem ganho analíticoP-V9-06-Evo (baixa)Score composto ponderado sobre valores normalizadosDescaracteriza V9 — converge em V4 Modo 3 ou vira nova visãoFora de escopo V9 (candidato a nova visão)
Warning de heterogeneidade detectada · sinaliza sem corrigir (padrão V7 W-V7-NEG-MEDIDA): motor aplica teste de razão de amplitude — max(amplitude_por_metrica) / min(amplitude_por_metrica) > 1000 (3 ordens de grandeza). Threshold 1.000× é generoso (captura casos reais como Faturamento em milhões × Taxa em decimais sem falso positivo) e editável em "Configurações avançadas" de E3. W-V9-ESCALAS-HETEROGENEAS (informativo) lembra usuário que score é por posição, não valor absoluto; Diagnóstico lista amplitudes por métrica.
Pesos por métrica fora de escopo MVP (confirmação):

V9 aplica equal-weighted por arquitetura — todas as métricas contribuem igualmente para o Score Consolidado
Peso automático = decisão silenciosa do sistema sobre hierarquia entre métricas (viola C.5)
Peso manual declarado = sub-caso de "score composto ponderado" que descaracterizaria V9
P-V9-01-Evo registra para evolução futura com análise cuidadosa da fronteira V9 × V4 Modo 3

Razão: (1) Ordinalidade é arquitetura elegante de C.5 — transforma fraqueza aparente ("escalas diferentes distorcem") em virtude estrutural ("posições neutralizam escalas por construção"). Precedente em V4 (participação %), V7 (desvio percentual), mas V9 é a primeira que faz isso pela natureza ordinal pura sem transformação explícita do valor. (2) Valor consolidado da métrica é preservado lado a lado com posição em todas as abas onde métricas aparecem (Ranking Completo, Perfil por Métrica) — usuário inspeciona o valor bruto que gerou aquela posição. Transparência total (C.2 · C.5). (3) Alternativas de normalização rejeitadas todas têm em comum a violação C.5 (decidir transformar o dado sem declaração explícita do usuário) ou descaracterização V9 (score ponderado vira outra visão). Registro explícito em tabela mantém rastreabilidade para evolução futura. (4) Threshold 1.000× é generoso — em prática real, casos detectados são genuinamente heterogêneos (R$ × %); conjuntos com métricas de mesma ordem de grandeza não disparam. (5) Pesos fora de escopo confirma posição estrutural — V9 é equal-weighted "by design", pesos entrariam como extensão futura com análise dedicada.
Padrão "herança adaptada à natureza analítica" D-073 (7ª aplicação V9): V5 futura trabalhará dispersão estatística (IQR/Z-score/percentil · normalização estatística intra-campo); V7 usa desvio percentual (normalização por grupo via média); V9 explicitamente evita normalização (posição ordinal pura). Três abordagens distintas à "heterogeneidade de escalas" justificadas pela natureza analítica.
Impacto:

dcv_v9.md §4.9 (não-normalização + 5 alternativas + warning de heterogeneidade) · §4.10 (pesos fora de escopo)
Contrato V9Result preserva valor_consolidado_por_metrica E posicao_por_metrica em colunas paralelas (nunca descarta valor)
F-MOT (Fundação) recebe requisito: teste de razão de amplitude como pré-processamento antes do Passo 2 (ordenação)
P-V9-XX-Evo ganha 4 candidatos (P-V9-03-Evo a P-V9-06-Evo) + 1 referência (score composto ponderado como candidato a nova visão)
W-V9-ESCALAS-HETEROGENEAS (informativo) catalogado

Referência canônica: /specs/dcv/dcv_v9.md §4.9 · §4.10

### D-093 — T-SEMA V9 · sétima consumidora com contrato distinto (por métrica + efeito direto no cálculo) + direção obrigatória sem default + limites 2-10 métricas + nome analítico editável
Data: 2026-04-19 · Bloco: DCV-V9 (sessão única) · Status: Fechada
Contexto: Prévio V9 (Parte 2.3, 2.4) declara 2-6 métricas com "direção obrigatória" + (Parte 6.2) mecânica "Maior-é-melhor → decrescente; Menor-é-melhor → crescente", sem formalizar contrato T-SEMA, sem decidir default da direção, sem limites operacionais claros. V7 D-087 estabeleceu T-SEMA como efeito apenas visual (cálculo simétrico). V9 precisa decidir: T-SEMA afeta cálculo ou só visualização? Por métrica ou global? Qual default? Refino T-05 consolidou 4 decisões articuladas.
Decisão: V9 é sétima consumidora de T-SEMA com contrato estruturalmente distinto das anteriores:
(1) Por métrica (2-6 direções simultâneas) com efeito direto no cálculo:

Cada Métrica tem Direção declarada: Maior-é-melhor (ordem decrescente na ordenação → Posição 1 = maior valor) ou Menor-é-melhor (crescente → Posição 1 = menor valor)
T-SEMA afeta cálculo diretamente — a Direção é o que determina a ordem de ordenação → Posição → Score → Classificação
Distinção formalizada vs V7 D-087 (T-SEMA global, apenas visual) via padrão "herança adaptada à natureza analítica" D-073: V7 tem 1 medida e pode abstrair T-SEMA do cálculo (classificação simétrica); V9 tem 2-6 métricas e precisa da Direção para ordenar cada uma (direcional por construção)

(2) Sem default · declaração obrigatória do usuário em E3:

Quebra do padrão "default declarado" que se aplica em outras pendências V9 (modo da base · regra de agregação · thresholds)
Justificativa: Direção é a única decisão em V9 cujo erro inverte o ranking 100% (Líder vira Retaguarda)
E3 apresenta cada métrica com seletor de Direção em branco e exige seleção antes de avançar
Sem detecção automática por nome da métrica (rejeitada pelos mesmos motivos V7 D-087: "tempo médio de atendimento" menor-é-melhor × "tempo de vida útil" maior-é-melhor)
Tensão com C.5 reconhecida: declaração obrigatória é fricção UX; alternativa "default Maior-é-melhor" embutiria decisão silenciosa em 50% dos casos. Escolha pela fricção é aplicação estrita de C.5 — em V9, a gravidade da inversão justifica o custo UX
P-V9-02-Evo registra detecção automática por nome opt-in (usuário pede sugestão, motor propõe, usuário confirma) como evolução futura

(3) Nome analítico por métrica editável (default declarado):

Cada Métrica tem nome_analitico com default = nome da coluna na base, editável em E3
Padrão V7 D-082 aplicado (nome editável como parte da declaração da visão)
Visível em E3 ao lado do seletor de Direção

(4) Limites operacionais de métricas em 5 patamares (estrutura escalonada padrão V7/V8):

0-1: bloqueio estrutural (W-V9-METRICAS-INSUFICIENTES · ranking monomensional não é V9)
2: alerta (W-V9-METRICAS-MIN · Variação Máxima com interpretação reduzida · mínimo matemático)
3-6: normal
7-10: alerta forte (W-V9-METRICAS-EXCESSO-AVISO · confirmação recomendada)
11+: bloqueio (W-V9-METRICAS-INVIAVEL · tela ilegível, score disperso)

Quadro comparativo de consumo T-SEMA:
VisãoEscopoEfeito no cálculoDefaultV2Global (1 medida)Afeta interpretaçãoNeutroV3Global (1 medida)Afeta interpretaçãoNeutroV7Global (1 medida)Não afeta cálculo — apenas visualização e ordem de apresentaçãoNeutroV9Por métrica (2-6)Afeta cálculo — determina ordem de ordenação de cada métricaSem default · obrigatório
Efeito visual em V9:

Posição 1 destacada como "líder daquela métrica" independentemente da direção (mapeamento visual coerente em ambas)
Coluna da métrica na saída Excel com ícone ↑ Maior-é-melhor / ↓ Menor-é-melhor indicando Direção declarada (rótulo descritivo, não interpretativo · padrão D-087)
Persistida em T-MODELO como par Métrica↔Direção

Razão: (1) Padrão "herança adaptada à natureza analítica" D-073 (4ª aplicação V9): V7 pode abstrair T-SEMA do cálculo porque 1 medida + classificação simétrica = independência. V9 não pode porque multiplicidade de métricas com direções distintas é a própria natureza da visão — sem Direção declarada, não há como ordenar. Divergência vs V7 é aplicação honesta do padrão, não inconsistência. (2) Sem default em E3 é aplicação estrita de C.5: "default Maior-é-melhor" seria mais amigável mas embute decisão silenciosa em 50% dos casos (quando métrica é menor-é-melhor). Gravidade do erro (ranking 100% invertido) justifica fricção UX. (3) Detecção automática por nome (A3 em T-05) rejeitada pelos mesmos motivos V7 D-087 — heurística incorreta em casos ambíguos como "tempo". Extensão opt-in em P-V9-02-Evo com confirmação obrigatória preserva opção futura sem comprometer C.5 no MVP. (4) Limite 11+ bloqueia por razão operacional real — tela ilegível + score disperso (dilui sinal em 11+ dimensões) + custo computacional amplificado. Não é regra paternalista; é limite estrutural honesto. (5) Nome analítico editável (não apenas nome da coluna) dá autonomia ao usuário sobre vocabulário da saída — importante quando nome da coluna é técnico/abreviado.
Extensão do contrato T-SEMA (F-TRANS):
T-SEMA aceita:
  # V2/V3/V7 (anterior)
  valor_unico: enum [Maior_Melhor, Menor_Melhor, Neutro]

  # V9 (nova)
  lista_por_metrica: list[{metrica: str, direcao: enum [Maior_Melhor, Menor_Melhor]}]
  # Sem Neutro em V9 — Neutro não ordena
Impacto:

dcv_v9.md §4.4 (Direção por métrica) · §4.5 (Nome analítico) · §4.6 (T-SEMA contrato V9) · §4.8 (limites operacionais)
CONTEXT §6 T-SEMA atualizado: V9 como 7ª consumidora com contrato distinto + nota sobre efeito no cálculo
GLOSSARIO §4 T-SEMA ganha bloco "Aplicação em V9" com 4 aspectos (contrato por métrica · sem default · efeito no cálculo · persistência em T-MODELO)
F-TRANS (Fundação) recebe requisito: T-SEMA aceita lista [metrica, direcao] em vez de valor único
Spec S-V9 recebe requisito: wireframe E3 com seletor de Direção em branco por métrica + ícone ↑/↓ na saída
7 warnings novos: W-V9-DIRECAO-FALTANDO (bloqueio), W-V9-DIRECAO-DECLARADA, W-V9-NOME-DEFAULT, W-V9-NOME-CUSTOM, W-V9-METRICAS-INSUFICIENTES (bloqueio), W-V9-METRICAS-MIN (alerta), W-V9-METRICAS-EXCESSO-AVISO (alerta forte), W-V9-METRICAS-INVIAVEL (bloqueio)
P-V9-02-Evo registrado (detecção automática opt-in)

Referência canônica: /specs/dcv/dcv_v9.md §4.4 · §4.5 · §4.6 · §4.8 · CONTEXT §6 T-SEMA · D-087 (V7 contrato base) · D-073 (padrão de herança adaptada)

### D-092 — Modo da base V9 (Transacional × Pré-agregado) + Modo de Ranking como derivação da unidade analítica + consolidação obrigatória em 4 passos com blindagem contra dupla agregação + regras de agregação independentes por métrica
Data: 2026-04-19 · Bloco: DCV-V9 (sessão única) · Status: Fechada
Contexto: Prévio V9 (Parte 2.6, 4.2, 4.3, 6.1) tem 4 pontos dispersos tratando duplicidade do identificador + unidade analítica como "Identificador ou Identificador + Agrupadores" + princípio "consolidar primeiro" sem formalização de modo da base formal + consolidação "quando houver duplicidade" (condicional). V7 D-082 e V8 D-074 consolidaram modo da base formal + consolidação obrigatória + 4 passos canônicos + blindagem contra dupla agregação. V9 precisa herdar o padrão e resolver 3 lacunas estruturais (L1 modo formal, L2 unidade analítica, L3 T-AGRUPA condicional × obrigatória) + estender T-AGRUPA para regra por métrica. Refino T-04 consolidou 4 decisões articuladas.
Decisão consolidada:
(1) Modo da base formal com default declarado (herança V7 D-082 · V8 D-074):

Transacional (múltiplas linhas por unidade analítica · T-AGRUPA consolida)
Pré-agregado (1 linha por unidade analítica · T-AGRUPA como no-op validado)
Default detectado pelo motor na amostragem: duplicatas detectadas → Transacional; unicidade 100% → Pré-agregado
Visível em E2, editável em um clique
5 warnings: W-V9-MODO-TRANS-DEFAULT/CUSTOM · W-V9-MODO-PREAGG-DEFAULT/CUSTOM · W-V9-MODO-VIOLACAO (bloqueio) — Pré-agregado declarado mas duplicatas detectadas no volume completo

(2) Unidade analítica derivada do Modo de Ranking (em vez de campo separado dual):

Modo Global → unidade analítica = Identificador (ranking único sobre todo o conjunto)
Modo Segmentado → unidade analítica = Identificador + Agrupador ativo (ranking recalculado dentro de cada valor do agrupador)
Agrupador obrigatório no modo Segmentado (W-V9-SEG-SEM-AGRUPADOR bloqueio se ausente)
MVP limita 1 Agrupador ativo; múltiplos em P-V9-08-Evo
Mesmo Identificador em diferentes valores do Agrupador = 2 unidades analíticas distintas (padrão V7 §4.5 adaptado)
2 warnings: W-V9-RANKING-GLOBAL, W-V9-RANKING-SEGMENTADO (informativos)

(3) T-AGRUPA obrigatória sempre com no-op validado em Pré-agregado (blindagem contra dupla agregação):

Ordem canônica em 4 passos (§5.2 do DCV-V9):

Consolidação da unidade analítica via T-AGRUPA com regra declarada por métrica
Ordenação por métrica respeitando Direção declarada
Atribuição de Posição por métrica (rank mínimo)
Score Consolidado · Variação Máxima · Classificação


Nenhum passo pode ser pulado ou reordenado
F-MOT blinda em teste unitário que linhas brutas nunca entram no Passo 2
Armadilha amplificada vs V7: em V7, dupla agregação corrompe um grupo; em V9, corrompe ranking cross-elementos inteiro (todas as métricas · todos os elementos)

(4) Regras de agregação independentes por métrica (extensão T-AGRUPA):

Contrato T-AGRUPA passa a aceitar dicionário {metrica: regra} em vez de regra única
5 regras oficiais: Soma · Média · Máximo · Mínimo · Contagem (Contagem como caso especial que dispensa campo de medida, análogo V7 §4.7)
Default declarado por tipo de métrica (taxonomia D-025): Aditiva → Soma · Não-aditiva → Média · Relativa → Média
Cada métrica configurada independentemente em E3
2 warnings: W-V9-AGREG-DEFAULT (informativo) · W-V9-AGREG-CUSTOM (informativo)

Razão: (1) Padrão "consolidação obrigatória pré-cálculo com blindagem contra dupla agregação" ganha 3ª ocorrência consecutiva (V8 D-074 · V7 D-082 · V9 D-092) — candidato forte à formalização em CONTEXT §9 Camada B/C (derivado de C.2 + C.5). (2) Derivação de unidade analítica a partir do Modo de Ranking (em vez de declaração dual) fecha L2 com elegância — uma declaração do usuário (Modo) produz uma unidade analítica determinística, sem ambiguidade. (3) Blindagem contra dupla agregação em V9 é mais crítica que em V7/V8 porque ranking cross-elementos amplifica o estrago — formalização em 4 passos no DCV + requisito explícito para F-MOT em teste unitário previne bug estrutural. (4) Regra de agregação independente por métrica é extensão natural do contrato T-AGRUPA existente (em V7 há 1 medida, 1 regra; em V9 há 2-6 métricas, cada uma com regra própria) — primeira consumidora com contrato multi-regra; adaptação justificada pela natureza analítica V9. (5) MVP limita 1 Agrupador ativo no modo Segmentado pela mesma lógica V7 §4.8 — tabelas aninhadas e ambiguidade de leitura ("ranking em qual nível?") aumentam complexidade UX sem clareza de ganho; extensão em P-V9-08-Evo preserva opção futura.
Padrão "herança adaptada à natureza analítica" D-073 (6ª aplicação V9): V7 tem 1 medida · 1 regra de agregação (D-082); V9 tem 2-6 métricas · 1 regra por métrica (D-092). Extensão justificada.
Contrato T-AGRUPA atualizado (F-TRANS · extensão D-082):
T-AGRUPA aceita:
  # V4/V7/V8 (anterior)
  regra_unica: enum [Soma, Media, Maximo, Minimo, Contagem]

  # V9 (nova)
  regras_por_metrica: dict[str, enum]  # {nome_metrica: regra}
Impacto:

dcv_v9.md §4.1 (modo da base) · §4.2 (Modo de Ranking deriva unidade analítica) · §4.3 (ordem canônica 4 passos · blindagem) · §4.7 (regras de agregação por métrica)
CONTEXT §6 T-AGRUPA atualizado: V9 como consumidora com extensão para regra por métrica
GLOSSARIO §4 T-AGRUPA ganha bloco "Aplicação em V9" com contrato multi-regra
F-MOT (Fundação) recebe requisitos: (1) detecção de duplicatas em amostragem para default declarado de modo, (2) validação de unicidade no volume completo quando Pré-agregado, (3) 4 passos canônicos blindados em teste unitário
F-TRANS (Fundação) recebe requisito: T-AGRUPA aceita dicionário {metrica: regra}
9 warnings novos catalogados (5 modo + 2 ranking + 1 seg-sem-agrupador bloqueio + 2 agregação default/custom)
CONTEXT §9 Camada C sinaliza padrão "consolidação obrigatória pré-cálculo" com 3 aplicações consecutivas (candidato a formalização)

Referência canônica: /specs/dcv/dcv_v9.md §4.1 · §4.2 · §4.3 · §4.7 · CONTEXT §6 T-AGRUPA · D-082 (V7 contrato base) · D-074 (V8 modo da base) · D-025 (taxonomia de tipos de medida)

### D-091 — Cumprimento da retroação diferida V7→V9 · §2.3 "Relação com V7" simétrico + fechamento do par autônomo Família D dos dois lados + 3 células do §2.3 V7 preenchidas
Data: 2026-04-19 · Bloco: DCV-V9 (sessão única) · Status: Fechada
Contexto: D-081 (refino DCV-V7 · 19/04/2026) registrou retroação diferida V7→V9 como aberta com cumprimento esperado em sequência direta — DCV-V7 §2.3 contém tabela comparativa V7×V9 de 5 linhas com 3 células marcadas (a confirmar em DCV-V9): (a) unidade analítica V9, (b) classificação do resultado V9, (c) aplicação de T-AGRUPA em V9. Opção C1 adotada em D-081 (diferida com cumprimento esperado) em vez de C2 (cumprimento antecipado), preservando honestidade sobre especulação vs decisão refinada. Refino DCV-V9 é a sessão natural do cumprimento, T-02 é a pendência que formaliza.
Decisão: DCV-V9 §2.3 contém bloco "Relação com V7" espelho estrutural do §2.3 do DCV-V7 com as 3 células preenchidas com base nas decisões tomadas no próprio refino V9:
Célula do §2.3 V7EraFica (preenchido por D-091)OrigemUnidade analítica V9(a confirmar em DCV-V9)Identificador (modo Global) · Identificador + Agrupadores ativos (modo Segmentado)D-092 · dcv_v9.md §4.2Classificação do resultado V9A confirmar — candidatos: Destaque · Padrão · Fragilidade ou faixas por quartilLíder · Especialista · Equilibrado · Retaguarda (4 classes mutuamente exclusivas com prioridade declarada Líder→Retaguarda→Especialista→Equilibrado)D-098 · dcv_v9.md §5.6T-AGRUPA em V9(a confirmar em DCV-V9)Sim — consumida com 5 regras (Soma · Média · Máximo · Mínimo · Contagem), independentemente por métricaD-092 · dcv_v9.md §4.7
Observação sobre candidata rejeitada "Destaque · Padrão · Fragilidade": especulação do §2.3 V7 (quando V9 ainda não tinha refino), hipoteticamente mais análoga à taxonomia V7 simétrica (Acima · Na Média · Abaixo). Prévio V9 adotou normativamente outra taxonomia (Líder · Especialista · Equilibrado · Retaguarda), coerente com a natureza multidimensional — score consolidado + variação máxima de posição produzem 4 classes distintas. Especialista em particular não tem contrapartida em V7 — é fenômeno exclusivo de ranking multidimensional. Divergência justificada pelo padrão "herança adaptada à natureza analítica" D-073: natureza univariada V7 → 3 classes por desvio direcional; natureza multidimensional V9 → 4 classes por combinação score+dispersão.
Estrutura do §2.3 DCV-V9 · espelho do §2.3 V7 com inversão de colunas (V9 à esquerda, V7 à direita — conveniência de leitura):
Parágrafo de abertura declarando par autônomo Família D (espelho fiel do V7).
Parágrafo de definição da Família D (cópia fiel do V7 para coerência entre documentos).
Tabela comparativa V9×V7 (5 linhas: O que rastreia · Unidade analítica · Classificação · Transversais comuns · Tipo de medida) — idêntica à tabela V7 com linhas preenchidas.
Parágrafo de fechamento sobre microcopy declarativa autossuficiente + nota explícita "Este bloco cumpre a retroação diferida V7→V9 registrada em D-081".
Razão: (1) Padrão de retroação diferida V7→V9 executado como planejado em D-081 — cumprimento em sequência direta sem pausa adicional, diferente de V11→V1 onde V1 já está aprovada e a retroação permanece em espera. (2) Preenchimento das 3 células com decisões refinadas (não especulação) respeita a filosofia de D-081 — só fecha o par depois que V9 tem DCV refinado. (3) Estrutura espelho (tabela inversa + parágrafos simétricos) garante coerência documental entre os dois DCVs da família — quem leia V7 vê V9 detalhada e vice-versa. (4) D-081 permanece registrada como contexto histórico (decisão de diferir em vez de antecipar segue válida); cumprimento via D-091 esclarece o status — não revogação, cumprimento. (5) Família D fechada em Fase 0 após aprovação deste DCV (V7 e V9 ambas aprovadas) — próximo bloco é DCV-V5 (Família E).
Impacto:

dcv_v9.md §2.3 (bloco "Relação com V7" simétrico com 3 células preenchidas)
dcv_v7.md §2.3 fica sem células pendentes na próxima iteração natural (células (a confirmar em DCV-V9) podem ser substituídas pelos valores preenchidos aqui)
CONTEXT §4 Família D atualizada com detalhes de ambas as visões e marca família fechada em Fase 0
GLOSSARIO §10 "Retroação diferida": V7→V9 marcada como cumprida (status muda de "aberta com cumprimento esperado em sequência direta" para "cumprida"); V11→V1 permanece aberta
GLOSSARIO §5.V9 ganha entrada "Família D · Posição relativa · par autônomo com V7"
D-081 ganha nota de status: "cumprida por D-091" (mantém registro histórico · decisão original não revogada)
Padrão "par autônomo de família com retroação simétrica" consolidado em 3 pares documentados: V11↔V1 (ainda aberta · D-058) · V3↔V8 (cumprida antecipadamente · D-073) · V7↔V9 (cumprida em sequência natural · D-091)

Referência canônica: /specs/dcv/dcv_v9.md §2.3 · /specs/dcv/dcv_v7.md §2.3 · CONTEXT §4 · GLOSSARIO §10 · D-081 (registro original da retroação) · D-058 (V11→V1 em aberto) · D-060/D-073 (V3→V8 cumprimento antecipado)

### D-090 — Sumário do refino DCV-V7 · 13 pendências fechadas em sessão única
**Data:** 2026-04-19 · **Bloco:** DCV-V7 (sessão única) · **Status:** Fechada

**Contexto:** Refino DCV-V7 executado em sessão única (19/04/2026) seguindo padrão D-019 + D-034 + D-033. 13 pendências originais trabalhadas (T-01 a T-13), todas fechadas, nenhuma deferida. Padrão de condução D-019 aplicado integralmente: ritual de abertura com leitura dos 4 documentos canônicos + 4 DCVs anexados (prévio V7, V3 aprovado, V8 aprovado, V4 aprovado), fila racionalizada em 4 blocos (A · Posicionamento e fronteira · B · Cálculo e regras estruturais · C · Classificação, semântica e ranking · D · Saída e operação), uma pendência por vez com opções explícitas e C.5 como primeira lente, mini status-checks a cada ~3 pendências, sinalização de densidade D-034 no 3º status-check com recomendação de continuar em sessão única (aprovada pela Usuária).

**Decisão:** **DCV-V7 refinado.** Consolida 13 pendências estruturais com 9 decisões específicas (D-081 a D-089) mais esta (D-090) como sumário. 35 warnings V7 catalogados (6 bloqueios · 11 alertas · 18 informativos — V7 entre V3 com 27 e V8 com 37). Próxima Fase 0: **DCV-V9** (Família D · Posição relativa, segunda e última da família · cumprimento da retroação diferida D-081).

**13 decisões consolidadas do refino:**

| # | Tema | Referência |
|---|---|---|
| T-01 | Vocabulário canônico V7 (12 termos: Grupo, Elemento, Medida, Tolerância, Zona de Média, etc.) | dcv_v7.md §13 (consolidação terminológica, não gera D-XXX) |
| T-02 | Posicionamento Família D + retroação diferida V9 | D-081 · dcv_v7.md §2.3 · §11.2 |
| T-03 | Fronteira V7 × V5 e V7 × V4 | dcv_v7.md §2.2 (aplicação de padrão §2, não gera D-XXX) |
| T-04 | Consolidação Elemento+Grupo + 4 passos canônicos + blindagem dupla agregação | D-082 · dcv_v7.md §4.1 · §4.3 · §5.1 |
| T-05 | Tipos de medida V7 com tratamento adaptado + ponderada opcional em Relativa | D-083 · dcv_v7.md §4.2 |
| T-06 | Tolerância ±5% default declarado simétrico percentual | D-084 · dcv_v7.md §4.4 |
| T-07 | Casos-limite matemáticos (matriz de 6 casos + NULO_MEDIDA + Não aplicável) | D-085 · dcv_v7.md §5.3 |
| T-08 | Taxonomia oficial V7 (3+2+1 · leitura qualitativa no Bloco 5) | D-086 · dcv_v7.md §5.2 · §6.2 |
| T-09 | T-SEMA V7 (visual/ordem · não cálculo) | D-087 · dcv_v7.md §4.6 |
| T-10 | T-RANK V7 intra-grupo (sexta consumidora · 4 níveis desempate) | D-088 · dcv_v7.md §5.4 |
| T-11 + T-12 + T-13 | Resumo Executivo 6 blocos + Excel 6 abas + bloqueios/performance/roadmap | D-089 · dcv_v7.md §6.2 · §6.3 · §8 · §12 |

**Razão:** (1) Sessão única validou que refino denso pode caber em uma sessão quando prévio é maduro terminológicamente (V7 tinha PARTE 13 nomenclatura já consolidada) e a maioria das pendências herda padrões consolidados (V4 para tipos de medida · V3 para ordem canônica de cálculo · V8 para modo Transacional×Pré-agregado · D-024 default declarado · D-073 herança adaptada). (2) Retroação diferida V7→V9 registrada como "aberta com cumprimento esperado em sequência direta" — contexto diferente de V8→V3 (onde V3 já estava aprovada e cumprimento antecipado fez sentido); V9 ainda não refinada, especular §2.3 V9 seria prematuro. (3) Blindagem contra dupla agregação cristalizada em §1 · §4.3 · §5.1 · §10 do DCV — armadilha estrutural de alto risco formalmente documentada. (4) Kit D-033 completo em sessão única validado pela quarta vez consecutiva (precedentes V10 · V3 · V8 · V7).

**Impacto:**
- 1 DCV aprovado a mais → **8 de 11 DCVs aprovados** na Fase 0 (V2, V1, V11, V4, V10, V3, V8, V7) após aprovação formal deste
- Fila remanescente Fase 0: **V9 → V5 → V6** (3 DCVs)
- Família D · Posição relativa **primeira visão com DCV aprovado** (V9 próxima fecha a família)
- 35 warnings V7 catalogados · V7 na faixa média entre V3 (27) e V8 (37)
- T-SEMA ganha V7 como sexta consumidora efetiva com efeito apenas visual
- T-RANK ganha V7 como sexta consumidora com regra de desempate V7-específica em 4 níveis (adaptação D-041 via D-073)
- T-AGRUPA ganha modo no-op validado generalizado (V7 D-082 · V8 D-074)
- Padrão default declarado aplicado em 6 dimensões V7 (modo, tipo da medida, regra de agregação, tolerância, semântica, thresholds de leitura)
- Próximo bloco: DCV-V9 (cumprimento retroação D-081 · fechamento Família D)

**Referência canônica:** `/specs/dcv/dcv_v7.md` · D-081 a D-089 · CONTEXT §4 Família D · §6 T-AGRUPA/T-SEMA/T-RANK · GLOSSARIO §4 T-AGRUPA/T-SEMA/T-RANK · §5.V7 · §6 Warnings V7 · §10 Retroação diferida

---

### D-089 — Resumo Executivo V7 + Excel 6 abas + bloqueios operacionais + 9 diretrizes performance + roadmap P-V7-XX-Evo
**Data:** 2026-04-19 · **Bloco:** DCV-V7 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V7 PARTE 7 descreve indicadores principais e leitura executiva em 3 passos sem estrutura 6 blocos D-044. PARTE 10 declara 4 abas Excel (Detalhe · Resumo por Grupo · Desvios Significativos · Dados Brutos) sem Resumo Executivo nem Diagnóstico obrigatório. PARTE 2.8 e PARTE 12 listam alertas sem patamares. Refino T-11+T-12+T-13 consolidou estrutura completa aplicando padrão D-044 + D-017 + precedentes V3 D-069/D-070 e V8 D-078/D-079 adaptados à natureza univariada V7.

**Decisão consolidada de T-11+T-12+T-13 (3 pendências consolidadas em 1 D-XXX pela natureza unificada de "saída e operação"):**

**Resumo Executivo · 6 blocos fixos adaptados** (padrão D-044):
- Bloco 1 Cabeçalho · Bloco 2 Números-âncora com ordem adaptada a T-SEMA · Bloco 3 Distribuição (com breakdown condicional: completo ≤10 grupos, top 5 mais dispersos > 10 grupos) · Bloco 4 Elementos destacados (top 5 por direção + top 3 grupos mais/menos dispersos) · **Bloco 5 Leitura descritiva por grupo + síntese agregada** (5 leituras qualitativas: Homogêneo · Assimétrico Acima · Assimétrico Abaixo · Polarizado · Misto · + Não aplicável estrutural, thresholds 70%/60%/75%/25% editáveis) · Bloco 6 Qualidade estrutural.

**Exportação Excel · 6 abas oficiais:** Resumo Executivo · **Mapa de Grupos** (substitui Resumo por Grupo do prévio, adiciona amplitude + leitura qualitativa + status) · Detalhe por Elemento · Desvios Significativos (recorte filtrado, não cálculo autônomo) · Parâmetros · **Diagnóstico última (D-017)**. **Aba Dados Brutos do prévio descartada** (herança V8 D-078). Total 6 abas (menor que V3/V8 com 7 pela natureza univariada simpler).

**Bloqueios operacionais · 12 estruturais** (6 com código W-V7-* + 6 estruturais numerados): W-V7-MODO-VIOLACAO, W-V7-MEDIDA-ESTADO, W-V7-GRUPOS-INVIAVEL, W-V7-ELEMENTOS-INSUFICIENTES, W-V7-VOLUME-INVIAVEL + arquivo/estrutura/ausência-de-campo/nulos-100%/tolerância-inválida.

**Escala de cardinalidade V7 · 3 eixos HIERÁRQUICOS** (diferente da V8 multiplicativa — V7 é hierárquica-aditiva: elementos dentro de grupos, não cruzados): Eixo 1 Grupo (1-20 normal · 51-200 alerta · 1.001+ bloqueio) · Eixo 2 Elementos por grupo (<2 bloqueio · 500+ aviso · 10.000+ alerta) · Eixo 3 Total de elementos (≤50K normal · 500K-1M alerta forte · >1M bloqueio limite físico Excel).

**Diretrizes de performance · 9** (7 herdadas V3/V8 + 2 específicas V7): (8) particionamento por grupo antes de cálculos derivados, (9) leitura qualitativa em passe único com ordem de teste fixa.

**Roadmap P-V7-XX-Evo · 6 candidatos:** P-V7-01 detecção automática de peso em Relativa · P-V7-02 múltiplas medidas · P-V7-03 tolerância por grupo · P-V7-04 benchmarks externos · P-V7-05 ranking global · P-V7-06 mais classes qualitativas.

**Razão:** (1) Padrão 6 blocos D-044 consolidado em V4/V11/V3/V8 — uniformidade entre visões. (2) Aba Mapa de Grupos é coração visual V7 análogo a Matriz de Presença V8 e Recorte ponto a ponto V3 — peça de valor única. (3) Dados Brutos descartada pelo mesmo rationale V8 D-078 (Base Analítica cobre auditoria; dados brutos pertencem ao upload). (4) Escala hierárquica reflete natureza aditiva V7 × natureza matricial multiplicativa V8 — patamares mais generosos justificados por ausência de matriz aninhada. (5) 9 diretrizes mantêm uniformidade com V3/V8 + 2 específicas V7 atendem particularidade da visão (particionamento por grupo blinda contra cálculo cross-grupo acidental). (6) Roadmap documenta caminhos explicitamente considerados e rejeitados no MVP — memória institucional.

**Impacto:**
- dcv_v7.md §6.2 (Resumo Executivo 6 blocos) · §6.3 (Excel 6 abas) · §8 (bloqueios + escala + diretrizes) · §12 (roadmap)
- F-EXP (Fase 1) recebe requisitos V7: aba Mapa de Grupos com ordenação default por amplitude decrescente · aba Desvios Significativos com ordenação cross-grupos por magnitude · aba Parâmetros com campos V7-específicos · 6 abas padrão com Diagnóstico última (D-017)
- F-MOT (Fase 1) recebe requisitos V7: particionamento por grupo · leitura qualitativa em passe único com ordem de teste fixa · pré-validação de volume · detecção de duplicatas em amostragem para default de modo
- GLOSSARIO §5.V7 ganha entradas "Leituras qualitativas de grupo" · "Mapa de Grupos" · "Aba Dados Brutos V7 — descartada" · "Escala de cardinalidade V7 · 3 eixos hierárquicos"
- GLOSSARIO §6 Warnings V7 ganha bloco completo (35 warnings)
- 2 warnings novos T-11: W-V7-LEITURA-DEFAULT · W-V7-LEITURA-CUSTOM
- 10 warnings novos T-13: W-V7-GRUPOS-MUITOS-AVISO/ALERTA/CRITICO/INVIAVEL · W-V7-ELEMENTOS-INSUFICIENTES · W-V7-GRUPO-VOLUMOSO/CRITICO · W-V7-VOLUME-AVISO/ALERTA/CRITICO/INVIAVEL

**Referência canônica:** `/specs/dcv/dcv_v7.md` §6 · §8 · §12 · GLOSSARIO §5.V7 · §6 Warnings V7

---

### D-088 — T-RANK V7 · sexta consumidora · ordenação por magnitude intra-grupo · regra de desempate em 4 níveis (herança adaptada D-041 via D-073)
**Data:** 2026-04-19 · **Bloco:** DCV-V7 (sessão única) · **Status:** Fechada

**Contexto:** Prévio §6.9 declara ranking por desvio percentual decrescente intra-grupo; §6.10 declara desempate em 2 níveis (maior absoluto → alfabético). CONTEXT §6 T-RANK lista consumidoras (V1, V4, V9, V10, V11) sem V7. Refino T-10 adicionou V7 como sexta consumidora e adaptou regra de desempate D-041 à natureza analítica V7.

**Decisão:** V7 é **sexta consumidora de T-RANK**. Critério de ordenação: **magnitude (módulo) do desvio percentual decrescente** — posição 1 no grupo é o elemento que mais se afasta da média em qualquer direção. Escolha por magnitude (em vez de sinal preservado como no prévio §6.9) casa com atributo Desvio Significativo (T-01): ranking destaca primeiro elementos fora da Zona de Média, depois próximos ao limiar, por último centrais. Ranking com sinal (prévio literal) forçaria interpretação direcional que T-09 (T-SEMA) decidiu não entrar no cálculo.

**Regra de desempate V7 · 4 níveis** (adaptação D-041 via padrão "herança adaptada à natureza analítica" D-073 · D-041 não se aplica 1:1 porque V7 não tem "concatenação de agrupadores"):

1. `abs(desvio_percentual)` decrescente (magnitude)
2. `abs(desvio_absoluto)` decrescente (desempate por magnitude em unidades absolutas)
3. Nome do Elemento alfabético case-insensitive
4. Ordem de inserção original

Tolerância floating point: 1e-9 (herança D-041). 4 níveis em vez de 3 (prévio) ou 3 (D-041 default) blindam determinismo absoluto (C.1).

**Escopo intra-grupo exclusivamente.** Ranking global (cross-grupo) **fora de escopo V7** — preserva posicionamento analítico (benchmarking interno); mistura de grupos de escalas diferentes seria pergunta de V9 (ranking multidimensional). Aba Detalhe preserva colunas `desvio_absoluto` e `desvio_percentual` com sinal para reordenação manual do usuário no Excel. Redirecionamento declarativo para V9 registrado na nota estática final do Bloco 5 do Resumo Executivo.

**Casos sem ranking:** elementos NULO_MEDIDA e elementos em grupos Não aplicável (T-05/T-07) não recebem ranking — sem desvio calculado ou sem classificação primária, ranking não se aplica.

**Razão:** (1) Adaptação via D-073 é o padrão consolidado para conflitos entre contratos transversais default e necessidade específica de visão — D-041 declara explicitamente "configurável via parâmetro regra_desempate"; V7 passa parâmetro próprio. (2) Ordenação por magnitude respeita disjunção cálculo × semântica decidida em T-06/T-09 — se T-SEMA não entra no cálculo, ranking direcional (positivo primeiro) seria ranking semântico, contradição. (3) Nível 2 por desvio absoluto captura intuição do prévio §6.10 (elementos com mesmo % mas magnitudes absolutas diferentes devem ser ordenados pela magnitude) — preserva decisão analítica do autor. (4) Ranking global fora de escopo preserva o posicionamento "benchmarking interno" como diferencial V7; oferecer global (mesmo com warning) criaria rota de uso que descaracteriza a visão.

**Impacto:**
- dcv_v7.md §5.4 · §6.1 (contrato V7Result com `ranking_no_grupo` nullable quando classificação especial)
- CONTEXT §6 T-RANK atualizado (V7 adicionada como 6ª consumidora com regra V7-específica)
- GLOSSARIO §4 T-RANK ganha bloco "Aplicação em V7" com 4 níveis detalhados
- F-TRANS (Fase 1) recebe requisito: T-RANK com parâmetro `regra_desempate` aceitando lista de critérios nomeados + `escopo` enum {global, intra_grupo}
- W-V7-RANK-EMPATE (informativo) formalizado

**Referência canônica:** `/specs/dcv/dcv_v7.md` §5.4 · CONTEXT §6 T-RANK · D-041 (contrato transversal base)

---

### D-087 — T-SEMA V7 · sexta consumidora · default Neutro · efeito apenas em visualização e ordem de apresentação · cálculo simétrico preservado
**Data:** 2026-04-19 · **Bloco:** DCV-V7 (sessão única) · **Status:** Fechada

**Contexto:** Prévio §2.7 declara 3 semânticas (Acima positivo · Acima negativo · Neutro) e afirma "não altera cálculo; afeta apenas leitura visual, coloração e destaque". CONTEXT §6 T-SEMA lista V7 como consumidora (V2, V3, V7, V9). Refino T-09 formalizou contrato V7-específico de T-SEMA consolidando o princípio disjunção cálculo × interpretação.

**Decisão:** V7 é **sexta consumidora efetiva de T-SEMA** com 3 valores oficiais (Maior-é-melhor · Menor-é-melhor · Neutro). **Default Neutro**, editável em E3. **Efeito no cálculo: nenhum** — motor classifica simetricamente em Acima/Na Média/Abaixo com base em `|desvio_percentual|` ante Tolerância, independentemente de T-SEMA declarada. Esta decisão **trava a simetria da Tolerância** (T-06) e mantém determinismo total do cálculo.

**Efeitos concretos de T-SEMA em V7:**

(1) **Mapeamento de cores canônico:**
- Maior-é-melhor → Acima associado à cor positiva do sistema · Abaixo à cor negativa · Na Média neutra
- Menor-é-melhor → Acima associado à cor negativa · Abaixo à positiva · Na Média neutra
- Neutro → Acima e Abaixo com mesma cor direcional neutra · Na Média cinza

Paleta concreta é responsabilidade da Spec S-V7 e da identidade visual (Frente A); T-SEMA cristaliza apenas o mapeamento lógico.

(2) **Ordem de apresentação no Bloco 2 do Resumo Executivo:**
- Maior-é-melhor → maior desvio positivo primeiro (destaque)
- Menor-é-melhor → maior desvio negativo primeiro
- Neutro → maior desvio positivo primeiro (convenção)

(3) **Rótulos descritivos neutros preservados** nos Blocos 2 e 4 — "maior desvio positivo", "Top 5 maior desvio negativo" · **não** interpretativos ("ponto forte", "ponto fraco"). Motor apresenta fatos matemáticos; interpretação fica com o usuário.

(4) **Persistência em T-MODELO:** sim, padrão V2/V3/V8.

**Warnings:** W-V7-SEMA-DEFAULT (Neutro aceito) · W-V7-SEMA-CUSTOM (editado).

**Razão:** (1) Default Neutro é o único default que não assume direção sobre o dado do usuário — único compatível com C.5. Detecção por tipo de medida (A3 rejeitada) embutiria arbitrariedade ("quantidade vendida → maior-é-melhor" é óbvio, mas "tempo médio" é Aditiva/Não-aditiva e a detecção proporia errado). (2) Declaração obrigatória (A2 rejeitada) cria fricção UX sem ganho — usuário que sabe escolhe, usuário que não sabe trava. (3) Efeito zero no cálculo mantém determinismo C.1 e desacopla T-06 (tolerância simétrica) de T-09 — Tolerância assimétrica baseada em T-SEMA faria semântica afetar cálculo, contradizendo o próprio prévio §2.7. (4) Ordem adaptada (B1.2) é efeito visual legítimo que respeita semântica sem alterar cálculo — apenas sequência de apresentação muda. (5) Rótulos descritivos (B2.1 preferido a B2.2 interpretativo) — "Top 5 pontos fortes" embute leitura de negócio; "Top 5 maior desvio positivo" apresenta fato. Disjunção cálculo × interpretação preservada em todas as camadas.

**Impacto:**
- dcv_v7.md §4.6 (T-SEMA completo) · §6.1 (contrato com campo `semantica`) · §6.2 (Bloco 2 com ordem adaptada · rótulos descritivos)
- CONTEXT §6 T-SEMA atualizado (V7 confirmada · nota sobre efeito apenas visual)
- GLOSSARIO §4 T-SEMA ganha bloco "Aplicação em V7" com 4 efeitos concretos
- Frente A (identidade visual) recebe requisito: paleta com 3 eixos de cor (positiva · negativa · neutra) aplicáveis conforme T-SEMA
- Spec S-V7 recebe requisito: wireframe com cores por T-SEMA · Bloco 2 do Resumo Executivo com ordem dinâmica
- 2 warnings novos: W-V7-SEMA-DEFAULT · W-V7-SEMA-CUSTOM

**Referência canônica:** `/specs/dcv/dcv_v7.md` §4.6 · CONTEXT §6 T-SEMA · GLOSSARIO §4 T-SEMA

---

### D-086 — Taxonomia oficial V7 · 3 classes primárias mutuamente exclusivas + 2 classificações especiais paralelas + 1 atributo derivado + 5 leituras qualitativas de grupo no Bloco 5 (padrão V4/V8) · herança adaptada D-073
**Data:** 2026-04-19 · **Bloco:** DCV-V7 (sessão única) · **Status:** Fechada

**Contexto:** T-01 canonizou 3 classes V7 (Acima · Na Média · Abaixo) + atributo Desvio Significativo. T-05 e T-07 adicionaram classificações especiais paralelas (NULO_MEDIDA por elemento · Não aplicável por grupo). V8 D-072 formalizou 4 classes por ponto + Constante consolidada. Refino T-08 consolidou taxonomia V7 completa à luz de todas as decisões anteriores e rejeitou extensão para 5 classes ou classificação estrutural de grupo no V7Result.

**Decisão:** Taxonomia oficial V7 em **três camadas complementares**:

**Camada 1 · Classes primárias por elemento (3 mutuamente exclusivas):**
- **Acima** (`desvio_percentual > +Tolerância`)
- **Na Média** (`|desvio_percentual| ≤ Tolerância`)
- **Abaixo** (`desvio_percentual < −Tolerância`)

**Camada 2 · Classificações especiais (paralelas, substituem primária):**
- **NULO_MEDIDA** (por elemento, quando T-AGRUPA retornou nulo · herança V4 D-038)
- **Não aplicável** (por grupo, quando média < 0 ou = 0 · T-05/T-07)

**Camada 3 · Atributo derivado por elemento:**
- **Desvio Significativo** = boolean (`Classificação ∈ {Acima, Abaixo}`)

**Camada 4 · Leitura qualitativa por grupo (no Resumo Executivo Bloco 5, não estrutural no V7Result):**
- **Grupo Homogêneo · Grupo Assimétrico Acima · Grupo Assimétrico Abaixo · Grupo Polarizado · Grupo Misto** (5 leituras editáveis) · + **Grupo Não aplicável** (estrutural). Thresholds detalhados em D-089.

**Rejeitados explicitamente:** (a) extensão para 5 classes primárias (Muito Acima · Acima · Na Média · Abaixo · Muito Abaixo) — magnitude de desvio já comunicada pelo valor numérico e pelo ranking (D-088); (b) 5 classes com opção configurável em "Configurações avançadas" — branching de contrato no V7Result aumenta complexidade F-MOT e T-MODELO sem ganho analítico claro; (c) classificação estrutural de grupo no V7Result com valores fixos — arbitrariedade embutida no motor violaria C.5; faixas editáveis no Bloco 5 transferem decisão ao usuário.

**Razão:** (1) Padrão "herança adaptada à natureza analítica" (D-073) aplicado explicitamente: V7 tem 3 classes pela natureza univariada contínua (direção + magnitude no eixo único da medida); V8 tem 4 classes pela natureza sequencial com estados qualitativamente distintos (Novo ≠ Contínuo ≠ Retornou ≠ Ausente). Divergência justificada, não inconsistência. (2) Atributo derivado `Desvio Significativo` (em vez de classe independente) mantém taxonomia enxuta e respeita prévio §6.8 ("todo Acima ou Abaixo já é, por definição, Desvio Significativo"). (3) Classificações especiais paralelas (NULO_MEDIDA · Não aplicável) substituem classe primária no campo único `classificacao` do V7Result — contrato enxuto com enum de 5 valores possíveis. (4) Leitura qualitativa por grupo no Bloco 5 (camada 4) vs classificação estrutural no V7Result — coerência direta com V4 Bloco 5 (Concentrada · Equilibrada · Pulverizada com faixas · D-044) e V8 Bloco 5 (Estável · Rotativa · etc. com thresholds · D-078). Faixas editáveis respeitam C.5; motor propõe, usuário refina.

**Contrato V7Result (síntese):**
**Impacto:**
- dcv_v7.md §5.2 (taxonomia oficial em tabela consolidada) · §6.1 (contrato V7Result) · §6.2 (Bloco 5 com 5 leituras)
- F-MOT (Fase 1) recebe requisito: V7Result com campo `classificacao` enum de 5 valores · campo `status_grupo` enum de 2 valores · leitura qualitativa calculada após classificação com ordem de teste fixa
- GLOSSARIO §5.V7 ganha entradas "Classes primárias V7" · "NULO_MEDIDA" · "Não aplicável" · "Desvio Significativo" · "Leituras qualitativas de grupo"
- Padrão "herança adaptada à natureza analítica" (D-073) aplicado pela terceira vez documentada (V3×V8 intervalo · V7 taxonomia · V7 T-RANK)

**Referência canônica:** `/specs/dcv/dcv_v7.md` §5.2 · §5.3 · §6.1 · §6.2

---

### D-085 — Casos-limite matemáticos V7 · matriz de 6 casos · Não aplicável por grupo (média < 0 · = 0) · NULO_MEDIDA por elemento · grupo unitário e homogêneo preservados como Na Média
**Data:** 2026-04-19 · **Bloco:** DCV-V7 (sessão única) · **Status:** Fechada

**Contexto:** Prévio §4.6 e §6.5 tratam alguns casos-limite em prosa pontual sem matriz estruturada. Refino T-07 formalizou matriz completa de 6 casos-limite para blindar implementação contra bugs silenciosos, aplicando lente C.5 a cada caso.

**Decisão:** Matriz oficial de 6 casos-limite V7:

| Caso | Classificação | Cálculo | Warning |
|---|---|---|---|
| Grupo com média negativa | Não aplicável (grupo inteiro) | Desvios calculados mas grupo não classificado | W-V7-GRUPO-MEDIA-NEG (alerta forte) |
| Grupo com média=0 + todos elementos=0 | Não aplicável (grupo) | Desvio=0 para todos | W-V7-GRUPO-MEDIA-ZERO-HOMO (alerta forte) |
| Grupo com média=0 heterogênea | Não aplicável (grupo) | Desvio absoluto calculado, % indefinido | W-V7-GRUPO-MEDIA-ZERO-HETERO (alerta forte) |
| Grupo unitário (1 elemento) | **Na Média** por definição (elemento) + flag baixa utilidade | Desvio=0 | W-V7-GRUPO-UNITARIO (alerta) |
| Grupo com todos valores iguais à média | **Na Média** (todos elementos) | Desvio=0 para todos | W-V7-GRUPO-HOMOGENEO (informativo) |
| Elemento com consolidação nula | **NULO_MEDIDA** (elemento) | Não calculado | W-V7-NULO-MEDIDA (alerta forte) |

**Princípios subjacentes (aplicação de C.5 por caso):**

(1) **Classificação Não aplicável = cálculo matematicamente indefinido ou não-interpretável.** Aplica ao **grupo inteiro** (não por elemento) porque desvio percentual com base matemática problemática torna leitura do grupo como um todo não-interpretável; marcar elementos individualmente geraria resultados contraditórios dentro do mesmo grupo.

(2) **NULO_MEDIDA = classificação por elemento** quando consolidação T-AGRUPA retornou nulo (todas linhas da combinação Elemento+Grupo tinham nulo na medida). Herança integral V4 D-038.

(3) **Grupo unitário = caso legítimo, não erro.** Empresa com 1 fornecedor em categoria de nicho, único vendedor em região pequena — cálculo é trivialmente definido (desvio=0 = Na Média); problema é interpretativo ("está na média de um grupo de si próprio"), não matemático. Preservar como Na Média + warning informa sem mascarar. Rejeita bloqueio ou remoção (B3) — decide pelo usuário que grupo não vale análise; rejeita Não aplicável (B2) — transmite "não calculei" quando cálculo é correto.

(4) **Todos valores iguais à média = homogeneidade perfeita, resultado analítico válido.** Leitura de negócio útil (rateio por critério fixo suspeito, cumprimento rígido de orçamento). Warning ativo comunica; ausência silenciosa (C2 rejeitada) viola C.2.

(5) **V7Result preserva desvio_absoluto e desvio_percentual calculados mesmo em casos Não aplicável** para que usuário possa inspecionar no Excel; campo `classificacao` registra status especial. Motor não apaga dado; sinaliza e preserva.

**Razão:** (1) Matriz estruturada blinda implementação — cada omissão vira bug no motor. (2) Classificação Não aplicável por grupo é coerente com T-05 (estabelecido para média negativa) — mesma camada, mesmo mecanismo, extensão natural para média zero. (3) Distinção rigorosa entre 5 estados possíveis de classificação (3 primárias + NULO_MEDIDA + Não aplicável) simplifica contrato V7Result (enum único). (4) Preservação de grupo unitário e homogêneo com warnings apropriados respeita C.5 sem decidir pelo usuário; C.2 (nada silencioso) atendido via warnings ativos.

**Impacto:**
- dcv_v7.md §5.3 (matriz completa com rationale) · §5.2 (taxonomia consolidada) · §6.1 (contrato V7Result com enum de 5 valores)
- F-MOT (Fase 1) recebe requisito: detecção de cada caso com lógica específica · ordem de teste determinística · preservação de desvios calculados mesmo em casos especiais
- GLOSSARIO §5.V7 ganha entrada "Casos-limite matemáticos V7 · matriz de 6 casos"
- 5 warnings novos T-07: W-V7-GRUPO-MEDIA-ZERO-HOMO · W-V7-GRUPO-MEDIA-ZERO-HETERO · W-V7-GRUPO-UNITARIO · W-V7-GRUPO-HOMOGENEO · W-V7-NULO-MEDIDA

**Referência canônica:** `/specs/dcv/dcv_v7.md` §5.3

---

### D-084 — Tolerância V7 · default declarado ±5% simétrico em desvio percentual · unidade única · papel duplo (classifica Na Média + define Desvio Significativo)
**Data:** 2026-04-19 · **Bloco:** DCV-V7 (sessão única) · **Status:** Fechada

**Contexto:** Prévio §2.6 declara Tolerância padrão ±5% sem mencionar padrão "default declarado" (D-024). §6.7 e §6.8 formalizam uso em prosa. Refino T-06 formalizou contrato completo de Tolerância aplicando C.5 e decidindo disjunção com T-SEMA.

**Decisão:** **Tolerância** é parâmetro declarado pelo usuário em E3 que define a **Zona de Média** (região classificatória onde elementos são Na Média). Três decisões encadeadas:

(1) **Default fixo declarado ±5%** (rejeitadas: detecção adaptativa baseada em dispersão observada A2; default por tipo de medida A3). Valor canônico editável em E3. W-V7-TOLERANCIA-DEFAULT (informativo) registra aceitação sem edição; W-V7-TOLERANCIA-CUSTOM (informativo) registra edição.

(2) **Simétrica única (±N%)** (rejeitadas: assimétrica opcional B2; assimétrica ligada a T-SEMA B3). Tolerância assimétrica (+M% / −P%) baseada em T-SEMA faria semântica afetar cálculo — **violação direta do princípio T-SEMA estabelecido no prévio §2.7 e formalizado em T-09/D-087**. Simplicidade UX + coerência com V2/V11.

(3) **Unidade única em desvio percentual** (rejeitadas: desvio absoluto C2; configurável C3). Desvio percentual é comparável entre grupos com médias muito diferentes — único critério consistente dado que grupos V7 tipicamente têm escalas distintas. Desvio absoluto perderia comparabilidade; abrir opção configurável (C3) introduziria ambiguidade de contrato (ranking T-10 seria por % ou absoluto?).

**Papel duplo da Tolerância** (análogo a V11 T-05 · tolerância com papel duplo em D-054):
- Define classe **Na Média** (taxonomia §5.2)
- Define atributo derivado **Desvio Significativo** (= Classificação ∈ {Acima, Abaixo})

Limiar é o mesmo nos dois papéis — dualidade trivial, não ambígua.

**Casos onde Tolerância não se aplica** (cruzamento com T-05/T-07):
- Grupos com classificação Não aplicável (média negativa · média zero) — tolerância não opera
- Elementos NULO_MEDIDA — sem desvio calculado

**Razão:** (1) ±5% tem tradição em análises financeiras/gerenciais brasileiras (faixa de aceitação em desvio orçamentário, variação mês a mês em KPI); funciona como ponto de partida reconhecido. (2) Default adaptativo (A2) esconderia cálculo estatístico no default e quebraria reprodutibilidade entre análises — viola determinismo. (3) Assimetria criaria complexidade UX significativa com ganho marginal — mesmo resultado obtido com tolerância simétrica mais ampla e interpretação visual pelo usuário. (4) Percentual único mantém sistema V7 internamente consistente (Tolerância em %, Desvio Significativo em %, ranking por magnitude de % em D-088).

**Impacto:**
- dcv_v7.md §4.4 (Tolerância) · §13 (nomenclatura com Tolerância + Zona de Média como termos distintos)
- F-MOT (Fase 1) recebe requisito: validação de Tolerância em intervalo (0, 1000%) com rejeição fora disso
- GLOSSARIO §5.V7 ganha entradas "Tolerância" e "Zona de Média"
- Spec S-V7 recebe requisito: E3 com campo único de Tolerância (não duplo)
- 2 warnings novos: W-V7-TOLERANCIA-DEFAULT · W-V7-TOLERANCIA-CUSTOM
- Decisão trava relação T-06 ↔ T-09 (Tolerância simétrica ↔ T-SEMA não afeta cálculo)

**Referência canônica:** `/specs/dcv/dcv_v7.md` §4.4 · §5.2

---

### D-083 — Tipos de medida V7 · taxonomia D-025 herdada adaptada · tratamento específico por tipo · média ponderada opcional em Relativa · bloqueio Estado com redirecionamento V6
**Data:** 2026-04-19 · **Bloco:** DCV-V7 (sessão única) · **Status:** Fechada

**Contexto:** Prévio §2.4 lista tipos de medida ("valor · quantidade · tempo · taxa · índice · métrica contínua") sem distinção de tratamento. §4.5 e §6.5 tratam negativos e média zero em prosa pontual. V4 (D-036/D-038), V3 (D-066), V8 (D-075) consolidaram taxonomia de tipos com tratamento adaptado. Refino T-05 consolidou aplicação V7 com 4 decisões encadeadas.

**Decisão:** V7 adota **taxonomia D-025 refinada por V4 D-036** (4 tipos) com tratamento adaptado à natureza "desvio de média do grupo":

| Tipo | Default T-AGRUPA | Média do grupo | Casos-limite |
|---|---|---|---|
| **Aditiva** | Soma | Aritmética simples dos consolidados | Negativos preservam sinal · média negativa → grupo Não aplicável |
| **Não-aditiva** | Média | Aritmética simples dos consolidados | Idem |
| **Relativa** | Média (aritmética default) | Aritmética (default) · **ou** ponderada se campo de peso declarado | Idem + alerta forte sobre média aritmética de taxas |
| **Estado/Situação** | N/A | **Bloqueio** com redirecionamento V6 | — |

**4 decisões consolidadas:**

(1) **Aplicação integral adaptada dos 4 tipos** (A1; rejeitadas: A2 banir Relativa; A3 tratar tudo igual). Cada tipo tem default de regra de agregação próprio na T-AGRUPA — respeita natureza matemática da medida.

(2) **Tratamento de negativos em alerta forte + classificação Não aplicável para grupo com média negativa** (B-I; rejeitadas: B-II bloqueio absoluto; B-III alerta light sem tratamento especial). Sinal do desvio percentual inverte quando média < 0; grupo inteiro vira Não aplicável (T-05 introduz; T-07 estende para média zero). W-V7-NEG-MEDIDA (alerta forte presença) + W-V7-GRUPO-MEDIA-NEG (alerta forte por grupo afetado).

(3) **Média ponderada opcional em Relativa via campo de peso declarado** (C1; rejeitadas: C2 ponderada obrigatória; C3 fixa aritmética). Default é aritmética com W-V7-RELATIVA-MEDIA-ARIT (alerta forte explícito sobre distorção potencial de taxas sem peso); se usuário declara campo de peso, motor aplica Σ(valor × peso)/Σpeso com W-V7-RELATIVA-MEDIA-POND (informativo). Microcopy em E3 expõe: *"Média de taxas sem ponderação pode distorcer o cálculo. Declarar campo de peso? Opcional."*

(4) **Bloqueio Estado/Situação com redirecionamento V6** (D1 · herança V3/V4). Detecção por sinais (≤5 valores únicos numéricos, 0/1 ou 0/1/2, nome "Status"/"Situação"). W-V7-MEDIDA-ESTADO (bloqueio) com redirecionamento declarativo.

**Razão:** (1) Coerência estrutural com V3/V4/V8 — mesmo vocabulário de tipos, padrão "default declarado" aplicado. (2) Banir Relativa (A2) tira casos de uso reais importantes (margem por vendedor, taxa de conversão por canal). (3) Força Soma default para taxa (A3) produziria resultado sem sentido matemático — violação direta de C.5. (4) Ponderada obrigatória em Relativa (C2) adiciona fricção UX pesada e pode bloquear análise legítima quando usuário sabe que taxas são comparáveis (mesmo volume). (5) Preservar sinal matemático em negativos respeita determinismo; Não aplicável para grupo com média negativa evita leitura contraintuitiva sem violar C.2.

**Impacto:**
- dcv_v7.md §4.2 (tabela completa de 4 tipos × tratamento V7) · §5.3 (casos-limite relacionados)
- F-MOT (Fase 1) recebe requisitos: detecção de tipo na amostragem · default de regra T-AGRUPA adaptado por tipo · suporte a média ponderada em T-AGRUPA (extensão V7 · primeiro uso do projeto) · detecção e bloqueio de Estado/Situação
- GLOSSARIO §4 T-AGRUPA atualizado (modo no-op validado + média ponderada em Relativa)
- GLOSSARIO §5.V7 ganha entrada "Média ponderada em Relativa"
- 7 warnings novos T-05: W-V7-TIPO-DEFAULT · W-V7-TIPO-CUSTOM · W-V7-NEG-MEDIDA · W-V7-GRUPO-MEDIA-NEG · W-V7-RELATIVA-MEDIA-ARIT · W-V7-RELATIVA-MEDIA-POND · W-V7-MEDIDA-ESTADO

**Referência canônica:** `/specs/dcv/dcv_v7.md` §4.2 · §5.3

---

### D-082 — Modo da base V7 (Transacional × Pré-agregado) + consolidação obrigatória Elemento+Grupo + 4 passos canônicos · blindagem contra dupla agregação (herança adaptada V8 D-074)
**Data:** 2026-04-19 · **Bloco:** DCV-V7 (sessão única) · **Status:** Fechada

**Contexto:** Planilha aba 2 L9 registra armadilha central V7: *"consolidar Elemento + Grupo antes de calcular média do grupo — dupla agregação é armadilha"*. Prévio §4.3 e §6.2 declaram ordem correta em prosa. V8 D-074 formalizou modo declarado (Transacional × Pré-agregado) com consolidação única via T-AGRUPA. Refino T-04 consolidou contrato formal V7 aplicando C.5 e blindando implementação.

**Decisão:** Contrato formal V7 em 3 camadas:

**Camada 1 · Modo da base declarado com default detectado** (herança adaptada V8 D-074 via padrão D-073):
- Motor detecta sinais na amostragem: duplicatas de (Grupo, Elemento) → modo **Transacional** default; unicidade 100% → modo **Pré-agregado** default
- Modo visível em E2, editável em um clique
- **Transacional**: T-AGRUPA obrigatório com regra declarada (Soma default)
- **Pré-agregado**: T-AGRUPA como **no-op validado** — motor verifica unicidade no volume completo (não só amostra); se detecta duplicatas → bloqueio W-V7-MODO-VIOLACAO (motor não prossegue sem confirmação de regra)

**Camada 2 · Regra de agregação (T-AGRUPA)** consolidada:
- 3 opções oficiais: Soma · Média · Contagem
- Default Soma declarado (coerente com V3/V4/V8)
- **Contagem dispensa campo de medida** — campo Medida condicionalmente obrigatório (obrigatório quando regra ∈ {Soma, Média}, inaplicável quando = Contagem). E2 apresenta regra antes ou simultaneamente ao campo de medida.

**Camada 3 · Ordem canônica de cálculo em 4 passos numerados** (§5.1 do DCV):
  **Exemplo concreto da armadilha (registrado no DCV §1 · §4.3 · §10):**
- Base: VendedorA 2 linhas (100, 200), VendedorB 1 linha (300), VendedorC 1 linha (400), Grupo=Sudeste
- **Correto:** VendedorA consolidado=300, B=300, C=400 → Média=333,33 → VendedorA desvio=−33,33 → Abaixo
- **Dupla agregação:** Média=(100+200+300+400)/4=250 → VendedorA desvio=+50 → Acima
- Classificação invertida. Blindagem é obrigatória em teste unitário.

**Razão:** (1) C.5 direto — consolidação implícita sobre linhas brutas seria decisão analítica oculta do motor; ordem formalizada em 4 passos numerados torna auditável. (2) Modo declarado com detecção default respeita padrão "default declarado" D-024 e permite comunicar ao usuário no Diagnóstico qual foi a natureza da base. (3) Padrão "herança adaptada" D-073 aplicado explicitamente — V7 herda mecanismo V8 (modo declarado · consolidação única) adaptado à natureza Elemento+Grupo (V8 era Entidade+Ponto_do_eixo). (4) Contagem dispensa campo de medida respeita C.5 — forçar usuário a declarar medida quando quer contagem é fricção UX irrelevante; análogo a V4 Modo 1 sem valor. (5) 4 passos numerados são testáveis em unitário — cada passo tem entrada/operação/saída explícita; dupla agregação é detectável em code review.

**Impacto:**
- dcv_v7.md §1 · §4.1 (modo declarado) · §4.3 (contrato 4 passos) · §4.9 (regra de agregação) · §5.1 (ordem canônica detalhada) · §10 (armadilha com exemplo)
- F-MOT (Fase 1) recebe requisitos críticos: T-AGRUPA com modo no-op validado (confirmação de unicidade em volume completo) · detecção de duplicatas na amostragem para default · 4 passos implementados em pipeline com asserções de ordem · **teste unitário mandatório** de caminho correto vs dupla agregação em base de fixture
- GLOSSARIO §4 T-AGRUPA ganha bloco sobre modo no-op validado generalizado
- GLOSSARIO §5.V7 ganha entradas "Modo da base" · "Dupla agregação" · "Unidade analítica"
- 5 warnings novos T-04: W-V7-MODO-TRANS-DEFAULT · W-V7-MODO-TRANS-CUSTOM · W-V7-MODO-PREAGG-DEFAULT · W-V7-MODO-PREAGG-CUSTOM · W-V7-MODO-VIOLACAO (bloqueio)

**Referência canônica:** `/specs/dcv/dcv_v7.md` §1 · §4.1 · §4.3 · §5.1 · §10

---

### D-081 — Posicionamento Família D · Posição relativa + par autônomo V7×V9 + retroação diferida V7→V9 registrada (padrão D-058/D-060)
**Data:** 2026-04-19 · **Bloco:** DCV-V7 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V7 não menciona Família D nem V9 (PARTE 15 cita apenas "não substitui V2/V4/V5/V9" genericamente). V7 é primeira visão da Família D · Posição relativa (segunda é V9). Precedentes consolidados de abertura de família: V2 (Família A · D-006), V4 (Família C · D-035), V11 §2.3 (Família A expandida · D-058), V3 §2.3 (Família B · D-060), V8 §2.3 (D-071). Refino T-02 aplicou o padrão.

**Decisão:** **Família D · Posição relativa** definida como: *"visões que analisam como cada elemento se posiciona em relação a um benchmark calculado internamente sobre os próprios dados. V7 calcula o benchmark como média do grupo ao qual o elemento pertence (desvio univariado intra-grupo); V9 calcula o benchmark como posição consolidada em múltiplas métricas ordenadas com direção declarada (ranking multidimensional cross-elementos). Ambas consomem T-SEMA; V7 também T-AGRUPA e T-RANK. Não há view especializada entre elas — são visões autônomas da mesma família com problemas analíticos distintos."*

**§2.3 do DCV-V7 contém tabela comparativa V7×V9 de 5 linhas** + parágrafo de fechamento sobre microcopy declarativa autossuficiente:

| Aspecto | V7 | V9 |
|---|---|---|
| O que rastreia | Desvio de cada Elemento em relação à média do seu Grupo (univariado) | Posição consolidada em múltiplas métricas simultâneas (multidimensional) |
| Unidade analítica | Elemento + Grupo | Elemento *(a confirmar em DCV-V9)* |
| Classificação | Acima · Na Média · Abaixo + Desvio Significativo | *A confirmar em DCV-V9* |
| Transversais comuns | T-AGRUPA · T-SEMA · T-RANK · T-DIAG · T-MODELO | T-SEMA · T-RANK · T-DIAG · T-MODELO *(T-AGRUPA a confirmar)* |
| Tipo de medida | Uma medida por execução | Múltiplas (2-6) com direção declarada por métrica |

**Retroação diferida registrada:** DCV-V9 receberá §2.3 "Relação com V7" simétrico na próxima revisão natural — refino DCV-V9, em sequência direta após aprovação deste DCV-V7. Opção C1 adotada (diferida registrada) em vez de C2 (cumprimento antecipado). Contexto diferente de V8→V3 (onde V3 já estava aprovada quando V8 foi refinada · cumprimento antecipado em D-073 fez sentido); neste caso V7→V9, V9 está em prévio não refinado — especular §2.3 V9 agora seria prematuro. Padrão V11→V1 (D-058 · ainda aberta) valida retroação diferida quando visão de destino não tem DCV aprovado.

**Microcopy em tela e Excel: nenhuma menção a V9** em interface operacional (padrão consolidado V11/V3/V8). Resumo Executivo Bloco 5 terá nota estática final redirecionando para V5 e V9 (detalhe em D-089).

**Razão:** (1) Padrão V11↔V1 (D-058) · V3↔V8 (D-060) · V8↔V3 (D-073) validado 3 vezes — aplicação intacta à Família D garante coerência estrutural entre famílias. (2) Microcopy declarativa sem redirecionamento em interface respeita C.5 — sistema não tenta "saber" qual visão é a certa, apresenta vocabulário claro; usuário escolhe. (3) Frase âncora "benchmark interno sobre os próprios dados" é o diferencial central V7 (prévio P0.8) e é também diferencial V9 — benchmarks externos seriam domínio de outra visão hipotética. Distinção univariado × multidimensional é o recorte natural entre V7 e V9. (4) Retroação diferida (C1) em vez de cumprimento antecipado (C2) respeita que V9 ainda não tem contexto refinado — 3 células *(a confirmar)* na tabela são honestas em vez de especulativas. (5) Padrão **diferida com cumprimento esperado em sequência direta** é nuance específica V7→V9 — V9 é próximo DCV da fila Fase 0, então o cumprimento acontece na ordem natural do método sem pausa adicional (diferente de V11→V1 onde V1 já está aprovada e retroação fica realmente em espera).

**Impacto:**
- dcv_v7.md §2.3 (tabela V7×V9 + vocabulário declarativo) · §11.2 (retroação diferida registrada)
- CONTEXT §4 Família D expandida de "uma linha" para descrição análoga às Famílias A/B/C
- GLOSSARIO §5.V7 ganha entrada "Família D · Posição relativa · par autônomo com V9"
- GLOSSARIO §10 "Retroação diferida" registra V7→V9 como aberta (com cumprimento esperado em sequência direta)
- DCV-V9 (próximo refino) herda padrão com retroação natural · absorve §2.3 completo simétrico no seu próprio refino

**Referência canônica:** `/specs/dcv/dcv_v7.md` §2.3 · §11.2 · CONTEXT §4 · GLOSSARIO §10

---
### D-080 — Sumário do refino DCV-V8 · 12 pendências fechadas em sessão única
**Data:** 2026-04-19 · **Bloco:** DCV-V8 (sessão única) · **Status:** Fechada

**Contexto:** Refino DCV-V8 executado em sessão única (19/04/2026) seguindo padrão D-019. 12 pendências originais trabalhadas (T-01 a T-12), todas fechadas, nenhuma deferida. Padrão de condução D-019 aplicado integralmente: ritual de abertura com leitura dos 4 documentos canônicos + 4 DCVs anexados (prévio V8, V3 aprovado, V4 aprovado, V11 aprovado), fila racionalizada em 4 blocos (A · Posicionamento e fronteira · B · Eixo e intervalo · C · Dados · D · Saída e operação), uma pendência por vez com opções explícitas e C.5 como primeira lente, mini status-checks a cada ~3 pendências, sinalização de densidade D-034 no 3º status-check com recomendação de continuar em sessão única (aprovada pela Usuária).

**Decisão:** **DCV-V8 refinado.** Consolida 12 pendências estruturais com 9 decisões específicas (D-071 a D-079) mais esta (D-080) como sumário. 37 warnings V8 catalogados (9 bloqueios · 10 alertas · 18 informativos — maior volume até agora). Próxima Fase 0: **DCV-V7** (Família D · Posição relativa, primeira da família).

**12 decisões consolidadas do refino:**

| # | Tema | Referência |
|---|---|---|
| T-01 | Vocabulário canônico V8 (Ponto do eixo, Entidade, Agrupador) | dcv_v8.md §13 (consolidação terminológica) |
| T-02 | Posicionamento Família B + retroação D-060 cumprida + T-SEMA fora V8 | D-071 · dcv_v8.md §2 |
| T-03 | Taxonomia oficial (Novo · Contínuo · Retornou · Ausente) + Constante | D-072 · dcv_v8.md §5.2, §5.3 |
| T-04 | Herança T-EIXO integral | dcv_v8.md §4.3 (aplicação D-061) |
| T-05 | Estrutura POR_COLUNAS/POR_LINHAS + seleção prévia + multi-aba fora MVP | dcv_v8.md §3 (aplicação D-062/D-063) |
| T-06 | Intervalo De/Até + mínimo 2 pontos + padrão "herança adaptada" | D-073 · dcv_v8.md §4.5 |
| T-07 | Modo Transacional × Pré-agregado + consolidação única T-AGRUPA | D-074 · dcv_v8.md §4.1 |
| T-08 | Medida opcional + tipos + negativos não aplicáveis | D-075 · dcv_v8.md §4.2 |
| T-09 | Lacuna × Ausência × Granularidade mista + padrão "warning vs conteúdo" | D-076 · dcv_v8.md §4.4 |
| T-10 | Matriz de Presença + ordenação default editável + aninhamento por grupo | D-077 · dcv_v8.md §6.2 |
| T-11 | Resumo Executivo 6 blocos + Excel 7 abas + Dados Brutos descartada | D-078 · dcv_v8.md §6.3, §6.4 |
| T-12 | Bloqueios operacionais + performance + roadmap P-V8-XX-Evo | D-079 · dcv_v8.md §4.6, §7, §8, §12 |

**Razão:** (1) Sessão única validou que refino denso pode caber em uma sessão quando a maioria das pendências herda padrões consolidados (V3 como substrato direto, V4 para Resumo Executivo 6 blocos, V11 para par autônomo, C.5 como lente default). (2) Retroação diferida V3→V8 (D-060) cumprida antecipadamente no próprio refino V8 — §2.3 do DCV-V8 contém bloco "Relação com V3" simétrico. (3) **Dois padrões de método novos cristalizados na sessão** — "herança adaptada à natureza analítica" (D-073) e "warning em uma visão vs conteúdo em outra" (D-076) — ambos derivados práticos de C.5 registrados em CONTEXT §9 Camada C e GLOSSARIO §10. (4) Padrão D-033 de kit completo em sessão única validado novamente (precedente V10 · V3 · V8 consolidado).

**Impacto:**
- 1 DCV aprovado a mais → **7 de 11 DCVs aprovados** na Fase 0 (V2, V1, V11, V4, V10, V3, V8) após aprovação formal deste
- Fila remanescente Fase 0: **V7 → V9 → V5 → V6** (4 DCVs, Famílias D e E)
- Família B · Sequência **fechada em Fase 0** (ambas as visões com DCV aprovado)
- 37 warnings V8 catalogados — maior volume de warnings do projeto
- 2 novos padrões de método derivados de C.5 formalizados
- Retroação diferida V3→V8 marcada cumprida; V11→V1 permanece aberta
- M2.STACK candidato agora tem 2 consumidoras futuras formalizadas (V3 P-V3-01-Evo + V8 P-V8-01-Evo)
- T-EIXO consolidada como formalizada com 2 consumidoras ativas na Fase 0
- Próximo bloco: DCV-V7 (Família D · Posição relativa — primeira da família, precedente de abertura análogo a V2, V4, V3)

**Referência canônica:** `/specs/dcv/dcv_v8.md` · D-071 a D-079 · CONTEXT §4 Família B · §6 T-SEMA/M2.STACK · §9 Camada C · GLOSSARIO §5.V8 · §6 Warnings V8 · §10 padrões de método

---

### D-079 — Bloqueios operacionais V8 · 9 bloqueios · escala em 3 eixos · 7 diretrizes de performance · roadmap
**Data:** 2026-04-19 · **Bloco:** DCV-V8 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V8 tinha regras dispersas sobre cardinalidade (PARTE 4.6 — alerta não-bloqueante), requisitos mínimos (PARTE 2.8), e sem seção dedicada a bloqueios operacionais ou performance. Refino T-12 consolidou bloqueios herdados de V3/V4 (D-070/D-032/D-043) + específicos V8 emergentes + diretrizes de performance adaptadas + roadmap P-V8-XX-Evo.

**Decisão:** V8 formaliza **9 bloqueios operacionais** + **10 alertas** + **18 informativos** = **37 warnings V8**. Escala de cardinalidade inédita em **3 eixos multiplicativos** (entidades × pontos do eixo × grupos) com 5 patamares operacionais: ≤15K normal · 15K-100K aviso · 100K-500K confirmação · 500K-1M crítico · >1M bloqueio. Escala de entidades adicional (100/500/2000/10.000) e de pontos do eixo (bloqueio em 200+). Escala de agrupadores mais conservadora que V3 (V8 bloqueia em 7+ vs V3 em 8+) porque agrupadores V8 multiplicam grupos. 3 colisões bloqueadas (eixo×entidade, agrupador×entidade, eixo×agrupador). 7 diretrizes de performance (5 herdadas V3 + 2 novas V8: lazy rendering da matriz, streaming Excel para abas pesadas). Roadmap P-V8-XX-Evo com 5 evoluções (multi-aba, classes consolidadas adicionais, reordenação manual, sazonalidade, intervalo médio).

**Razão:** (1) Aplicar padrão V3/V4 (D-070/D-032) para uniformidade entre visões. (2) Escala em 3 eixos específica V8 reflete natureza estrutural distinta — V4 é dimensão única, V3 é agrupadores × pontos, V8 adiciona entidades como eixo adicional multiplicativo. Limite 1M células = limite físico Excel (~1.048.576 linhas) — não é decisão analítica, é capacidade da ferramenta. (3) Escala de agrupadores mais conservadora respeita amplificação V8 (N grupos × entidades × pontos = matriz aninhada multiplicada). (4) Lazy rendering e streaming Excel são novas diretrizes V8 porque matriz de presença pode ter volume muito superior a V3 (sem consolidação de valor como V3 faz — V8 preserva par a par). (5) Roadmap 5 evoluções balanceia escopo enxuto MVP com caminhos claros de evolução.

**Impacto:**
- dcv_v8.md §4.6 (agrupadores + colisões), §7.1 (9 bloqueios), §7.2 (10 alertas), §7.3 (18 informativos), §8 (7 diretrizes performance), §12 (roadmap)
- GLOSSARIO §6 Warnings V8 ganha bloco completo (37 warnings)
- GLOSSARIO §5.V8 ganha entradas "Escala de cardinalidade em 3 eixos multiplicativos" e "Colisões bloqueadas"
- F-MOT (Fase 1) recebe requisitos: pré-validação de volume antes de alocação, lazy rendering, filtro de ausência total cedo no pipeline
- F-EXP (Fase 1) recebe requisitos: streaming Excel (openpyxl write-only mode) para abas pesadas quando volume > 100K linhas

**Referência canônica:** `/specs/dcv/dcv_v8.md` §4.6, §7, §8, §12 · GLOSSARIO §6 Warnings V8

---

### D-078 — Resumo Executivo V8 · 6 blocos com leitura de ciclo de vida (5 classes) · Excel 7 abas · Dados Brutos descartada
**Data:** 2026-04-19 · **Bloco:** DCV-V8 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V8 não tinha seção estruturada de Resumo Executivo — apenas indicadores dispersos em PARTE 7.3 e leitura executiva em PARTE 7.4. Excel do prévio declarava 4 abas (Histórico de Presença · Resumo por Entidade · Movimentações · Dados Brutos) sem Resumo Executivo nem Diagnóstico obrigatórios (padrão Fundação D-017). Refino T-11 consolidou estrutura completa aplicando padrão V4/V11/V3 (D-044 · D-069) + resolveu divergência estrutural com 4 → 7 abas + rejeitou Dados Brutos com rationale.

**Decisão:** Resumo Executivo V8 segue padrão consolidado D-044 adaptado: **6 blocos fixos** (Cabeçalho · Números-âncora · Distribuição de classificações · Elementos destacados · Leituras descritivas · Qualidade estrutural). **Bloco 5 com leitura de ciclo de vida em 5 classes qualitativas mutuamente exclusivas:** Estável (>60% Constante OU taxa ≥ 80%) · Rotativa (Novas+Ausentes último ponto ≥ 30%) · Em retração (Ausentes > Novas fator ≥1.5) · Em expansão (Novas > Ausentes fator ≥1.5) · Mista. Thresholds editáveis (60%, 80%, 30%, 1.5) em "Configurações avançadas". Nota estática final redireciona V6/V9 para análises aprofundadas (análoga à nota V5/V7 de D-068 V3).

Estrutura de **7 abas do Excel**: Resumo Executivo · **Matriz de Presença (aba 2, aninhada por grupo quando há agrupadores)** · Histórico de Presença · Resumo por Entidade · **Movimentações (preservada do prévio como insight específico V8)** · Parâmetros · **Diagnóstico (última, D-017)**. **Aba Dados Brutos do prévio descartada** — Base Analítica cobre auditoria analítica; dados brutos normalizados são parte do upload, não da visão V8; Diagnóstico registra "linhas originais vs consolidadas" para auditoria.

**Razão:** (1) Padrão 6 blocos V4/V11/V3 consolidado — uniformidade entre visões; usuário que usa V2/V3/V4/V10/V11 reconhece estrutura em V8. (2) Aba Movimentações preservada como insight analítico único da V8 — "o que mudou no último ponto?" não cabe naturalmente em Resumo Executivo (que é síntese) nem em Base Analítica (que é granular). (3) Aba Matriz de Presença como aba dedicada reflete o papel central da matriz na V8 (coração visual da visão). (4) Dados Brutos descartada por preservar escopo V8 ("estruturar análise, não validar a verdade do dado" — princípio do prévio) e evitar redundância com Base Analítica. (5) Leitura de ciclo de vida em 5 classes aplica C.5 via faixas editáveis — motor propõe classificação qualitativa, usuário ajusta thresholds se caso de uso diverge. (6) Nota V6/V9 estática (não condicional a threshold) respeita padrão "microcopy declarativa autossuficiente".

**Impacto:**
- dcv_v8.md §6.3 (6 blocos), §6.4 (7 abas)
- F-EXP (Fase 1) recebe requisitos: aba Matriz de Presença com aninhamento por grupo + aba Movimentações específica V8 + 7 abas padrão com Diagnóstico última (D-017) + filtros ativos em todas
- GLOSSARIO §5.V8 ganha entradas "Leitura de ciclo de vida", "Movimentações (V8)", "Aba Dados Brutos do prévio V8 — descartada"
- 3 warnings novos V8: W-V8-LEITURA-DEFAULT, W-V8-LEITURA-CUSTOM (e outros capturados em T-12)

**Referência canônica:** `/specs/dcv/dcv_v8.md` §6.3, §6.4 · GLOSSARIO §5.V8

---

### D-077 — Matriz de Presença V8 · contrato lógico da célula · ordem default declarada editável · paginação · aninhamento por grupo
**Data:** 2026-04-19 · **Bloco:** DCV-V8 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V8 tratou matriz em 3 seções curtas (PARTE 9.2 linhas×colunas, PARTE 9.3 ordem fixa "Constante → Recorrente → Recuperado → Novo → Perdido" não configurável, PARTE 9.4 paginação 100 entidades). Refino T-10 formalizou contrato lógico da célula, inverteu decisão de ordem fixa em favor de default declarado editável, traduziu vocabulário para canônico T-03 (Contínuo/Retornou/Ausente), e formalizou aninhamento por grupo quando há agrupadores ativos.

**Decisão:** Matriz de Presença com **contrato lógico explícito da célula** no V8Result (`matriz_celula`): presente com classificação por ponto (Novo/Contínuo/Retornou com medida opcional) · ausente com histórico prévio (Ausente com medida null) · antes da primeira aparição (célula vazia sem classificação). Representação visual concreta fica para Spec S-V8.

**Ordem tripla determinística:**
1. **Primária — classificação atual**, default declarado editável: **Constante → Contínuo → Retornou → Novo → Ausente**. Inversão da decisão do prévio (ordem fixa) em favor de default declarado + edição em um clique (padrão D-024). W-V8-MATRIZ-ORDEM-CUSTOM registra edição.
2. **Secundária — taxa de presença decrescente** dentro de cada classe. Fixa.
3. **Terciária — alfabética da entidade**. Fixa (desempate C.1).

**Paginação:** threshold **100 entidades por grupo** (configurável Spec S-V8). W-V8-MATRIZ-PAGINACAO registra ativação. Escala de cardinalidade de entidades completada em D-079 (T-12).

**Matriz aninhada por grupo:** quando há agrupadores ativos, matriz estruturada hierarquicamente — para cada grupo único, uma matriz (entidades × pontos) independente. Mesma entidade em grupos diferentes pode ter classificações diferentes (preserva PARTE 2.6 do prévio). Mecânica de UI fica para Spec S-V8.

**Razão:** (1) Ordem fixa do prévio decide pelo usuário qual hierarquia de leitura é "a principal" — viola C.5. Analista fazendo churn quer Ausente primeiro; gerente fazendo onboarding quer Novo primeiro. Default declarado com edição preserva autonomia. (2) Default "Constante → Contínuo → Retornou → Novo → Ausente" escolhido por hierarquia estrutural de continuidade: começa pelos mais estáveis, termina pelos mais voláteis — leitura narrativa "quem ficou → quem entrou → quem voltou → quem estreou → quem saiu" funciona para leitura executiva sequencial. (3) Ordem secundária por taxa de presença decrescente destaca entidades com maior peso analítico em cada classe. (4) Alfabética como terceira preserva determinismo C.1. (5) Matriz aninhada por grupo preserva especificidade V8 declarada no prévio (PARTE 2.6) — mesma entidade pode ser classificada diferentemente em grupos distintos.

**Impacto:**
- dcv_v8.md §6.1 (granularidade periódica × consolidada), §6.2 (contrato matriz + ordem + paginação + aninhamento)
- F-MOT (Fase 1) recebe contrato V8Result com `matriz_celula` formalizado + ordenação tripla determinística
- F-EXP (Fase 1) recebe Matriz de Presença como aba dedicada com aninhamento por grupo
- GLOSSARIO §5.V8 ganha entradas "Matriz de Presença", "Ordenação tripla da matriz"
- Spec S-V8 recebe: representação visual concreta da célula · mecânica de reordenação das classes · mecânica de aninhamento por grupo · threshold de paginação configurável
- 3 warnings V8: W-V8-MATRIZ-ORDEM-CUSTOM, W-V8-MATRIZ-PAGINACAO, W-V8-ENTIDADES-MUITAS (complementares a D-079)

**Referência canônica:** `/specs/dcv/dcv_v8.md` §6.1, §6.2 · GLOSSARIO §5.V8

---

### D-076 — Ausência da entidade no ponto V8 é conteúdo primário · lacuna do eixo herdada V3 · granularidade mista alerta forte · padrão "warning vs conteúdo"
**Data:** 2026-04-19 · **Bloco:** DCV-V8 (sessão única) · **Status:** Fechada

**Contexto:** Três fenômenos de ausência convergem na V8: lacuna do eixo (macroscópica, herdada V3 D-065), ausência da entidade no ponto (microscópica, antecipada em §11.2 DCV-V3 como "insumo para classificação Ausente"), granularidade mista no eixo (específica V8, não tratada em V3). Prévio V8 PARTE 4.4 declarava "ausência = parte da matriz lógica" sem formalizar mecânica; PARTE 4.5 tratava granularidade mista como alerta não-bloqueante. Refino T-09 formalizou os 3 fenômenos separadamente e cristalizou padrão de método novo.

**Decisão:** V8 distingue **3 fenômenos estruturalmente diferentes**:

**(a) Lacuna do eixo (macroscópica)** — herdada integralmente de V3. Detecção dependente do tipo (temporal e ordinal com prefixo: sim; ordinal sem prefixo e manual: não). W-V8-EIXO-LACUNA informativo; W-V8-EIXO-LACUNA-MASSIVA alerta quando > 30%.

**(b) Ausência da entidade no ponto (microscópica)** — **promovida a conteúdo analítico primário da V8**. Em V3 era flag informativa AJUSTE_LEVE (ausencia_ponto); em V8 é **classificação Ausente** (uma das 4 classes primárias, T-03 V8). **Sem warning** — motor está fazendo exatamente o que a visão pede. **Economia de matriz:** entidade com 100% ausências em grupo específico não ocupa linha naquele grupo (comportamento esperado, sem warning).

**(c) Granularidade mista em eixo temporal** — **alerta forte com confirmação obrigatória** (elevada do prévio V8 que propunha alerta simples). Motor exibe amostra dos valores em cada granularidade; usuário obrigado a confirmar antes de prosseguir; sem correção automática (C.5). W-V8-EIXO-GRANULARIDADE-MISTA. Conceito não se aplica a eixos lógico/ordinal ou manual.

**Padrão de método novo cristalizado:** "**o que é warning em uma visão pode ser conteúdo em outra**" — fenômenos estruturais podem ter papéis radicalmente diferentes entre visões da mesma família. Mesmo dado de entrada, mesma detecção mecânica, papéis diferentes. Registrado em CONTEXT §9 Camada C como derivado de C.5 e GLOSSARIO §10 como padrão de método consolidado.

**Razão:** (1) Lacuna macroscópica continua estrutural como em V3 — fato da base independente do conteúdo analítico da visão. (2) Ausência microscópica **é** o conteúdo analítico primário da V8 — V8 existe para classificar presença/ausência; não faria sentido tratar como warning aquilo que a visão está fundamentalmente fazendo. Cumprimento da antecipação §11.2 DCV-V3. (3) Granularidade mista elevada a alerta com confirmação obrigatória porque em V8 pode inflar cardinalidade de pontos (entidade "presente em 15/03" e "presente em Março" vira 2 pontos distintos indevidos) — risco de resultado enganoso significativo que alerta simples (prévio) não captura adequadamente. (4) Correção automática de granularidade violaria C.5 — motor não tem base para decidir qual granularidade é "a correta". (5) Economia de matriz otimiza exibição sem perder informação — entidades 100% ausentes em grupo específico não carregam conteúdo analítico útil naquele grupo.

**Impacto:**
- dcv_v8.md §4.4 (3 fenômenos distintos) · §5.2 (economia de matriz)
- CONTEXT §9 Camada C ganha padrão "o que é warning em uma visão pode ser conteúdo em outra" como derivado de C.5
- GLOSSARIO §5.V8 ganha entradas "Granularidade mista no eixo", "Economia de matriz"
- GLOSSARIO §10 ganha entrada "O que é warning em uma visão pode ser conteúdo em outra" como padrão de método
- 3 warnings V8: W-V8-EIXO-LACUNA (informativo), W-V8-EIXO-LACUNA-MASSIVA (alerta), W-V8-EIXO-GRANULARIDADE-MISTA (alerta)
- Cumprimento da antecipação §11.2 DCV-V3 sobre "detecção de lacunas como insumo para classificação Ausente"

**Referência canônica:** `/specs/dcv/dcv_v8.md` §4.4, §5.2 · CONTEXT §9 · GLOSSARIO §10 "O que é warning em uma visão pode ser conteúdo em outra"

---

### D-075 — Medida opcional V8 · taxonomia D-025 com tratamento adaptado · default de agregação por tipo · negativos não aplicáveis
**Data:** 2026-04-19 · **Bloco:** DCV-V8 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V8 tratou medida em PARTE 2.5 (opcional, não altera classificação, ausência → vazio não zero) e PARTE 4.7 (não-aditivo gera alerta genérico). Refino T-08 formalizou herança da taxonomia D-025 (4 tipos) com tratamento adaptado à natureza contextual V8, decidiu tratamento de negativos, e fechou ambiguidade sobre estado/situação como medida V8 (redirecionamento V8/V6 de D-066 refere-se à análise principal, não uso como medida contextual).

**Decisão:** V8 herda taxonomia D-025 (aditivo · relativo · não-aditivo · estado/situação) com **tratamento adaptado à natureza contextual** (medida V8 não altera classificação — é enriquecimento visual):

- **Aditivo:** execução normal, default soma. Sem warning.
- **Relativo:** default declarado com regra de agregação **média** em vez de soma (somar percentuais não tem sentido analítico). W-V8-MEDIDA-RELATIVA informativo.
- **Não-aditivo:** default declarado com **média** + alerta de que valor é contextual. W-V8-MEDIDA-NAO-ADITIVA informativo.
- **Estado/situação (categórico):** execução com alerta; valor categórico exibido na Base Analítica, não agregável; regra T-AGRUPA não aplica (motor exibe primeira ocorrência ou concatenação — Spec S-V8 decide). W-V8-MEDIDA-CATEGORICA alerta.

**Default declarado sobre tipo** (herança D-025): motor detecta tipo na amostragem e propõe; usuário confirma ou edita. W-V8-MEDIDA-TIPO-DECL.

**Negativos — não se aplicam a V8.** V8 não calcula Diferença/Variação sobre medida (classificação é por presença). Valores negativos aparecem como vieram da base. Sem warning. Divergência com V3 (D-066 trata negativos com 2 opções) justificada via padrão "herança adaptada à natureza analítica" (D-073).

**Nulos com presença preservados.** Quando há presença da entidade mas medida é nula, motor preserva nulo na Base Analítica (não vira zero, não exclui linha). Presença depende da existência do registro, independente da medida. W-V8-MEDIDA-NULO-COM-PRESENCA informativo.

**Estado/situação como medida V8 aceito com alerta.** Esclarecimento importante: o redirecionamento V8/V6 de D-066 (V3 bloqueia estado/situação e sugere V8/V6) refere-se à **análise principal** — usuário quer rastrear "Status do cliente ao longo do tempo", o que V8 atende por natureza. Usar estado/situação **como medida opcional** dentro de V8 é funcionalmente distinto (enriquecer Base Analítica com categoria ao lado da presença) e fica permitido com alerta.

**Razão:** (1) Padrão D-025 (4 tipos) herdado mantém consistência entre visões. (2) Tratamento mais leniente em V8 respeita natureza contextual da medida — não entra em cálculo, então critérios estritos de V3/V4 (onde medida é central) não cabem. (3) Default de agregação variável por tipo (soma para aditivo, média para relativo/não-aditivo) aplica C.5: motor propõe tratamento apropriado ao tipo detectado; usuário ajusta se necessário. (4) Negativos não aplicáveis porque V8 não faz cálculo que precisaria de decisão sobre líquido vs absoluto — aplica padrão "herança adaptada". (5) Nulos preservados respeitam distinção do prévio entre "não houve presença" (ausência) e "houve presença sem valor registrado" (nulo). (6) Estado/situação aceito com alerta respeita C.5 — não bloqueia uso potencialmente legítimo; usuário decide se enriquecimento categórico é útil.

**Impacto:**
- dcv_v8.md §4.2 (medida opcional completa com tabela de tipos + nulos)
- Contrato V8Result: campo `medida_valor` e comportamento com nulos formalizado
- F-MOT (Fase 1) recebe requisito: default de agregação varia por tipo detectado (soma para aditivo, média para relativo/não-aditivo)
- F-EXP (Fase 1) recebe requisito: exibição de medida contextual na Base Analítica e Histórico de Presença com nulos preservados
- GLOSSARIO §5.V8 ganha entrada "Medida contextual V8"
- 5 warnings V8: W-V8-MEDIDA-TIPO-DECL, W-V8-MEDIDA-RELATIVA, W-V8-MEDIDA-NAO-ADITIVA, W-V8-MEDIDA-CATEGORICA (alerta), W-V8-MEDIDA-NULO-COM-PRESENCA
- D-025 (4 tipos de medida) **sem alterações** — V8 é consumidora, não formalizadora

**Referência canônica:** `/specs/dcv/dcv_v8.md` §4.2 · GLOSSARIO §5.V8 Medida contextual V8

---

### D-074 — Modos da base V8 · declarado com default declarado · consolidação única via T-AGRUPA com 5 regras canônicas · "primeiro valor" descartado
**Data:** 2026-04-19 · **Bloco:** DCV-V8 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V8 PARTE 2.7 declarou dois modos (Transacional e Pré-agregado) com regra "consolidar primeiro, classificar depois" mas sem especificar onde/como o modo entra no fluxo. PARTE 2.7 final listou 3 regras de agregação (soma · média · **primeiro valor**) com pendência aberta: onde aplica? Quando? Em qual campo? Refino T-07 formalizou mecânica completa e rebateu "primeiro valor" por conflito com C.1.

**Decisão:** **Modo declarado pelo usuário com default declarado do motor.** Motor detecta duplicidade em (Entidade, Ponto do eixo, Agrupadores ativos) na amostragem: nenhuma duplicidade → propõe Pré-agregado; há duplicidade → propõe Transacional (editável). W-V8-MODO-INFERIDO registra aceitação. **Modo é rótulo informativo** — não altera mecânica de consolidação.

**Consolidação via T-AGRUPA é lógica única, aplicada sempre**, independentemente do modo declarado. Motor consolida por unidade (Entidade + Ponto do eixo + Agrupadores ativos). Regra de agregação aplica-se **apenas quando há medida opcional declarada** — quando não há medida, consolidação resolve apenas presença (múltiplos registros no mesmo par → 1 par presente na matriz).

**5 regras canônicas T-AGRUPA** (herança D-026): **soma (default) · média · máximo · mínimo · contagem**. Default pode variar por tipo de medida (ver D-075: relativo/não-aditivo → default média).

**"Primeiro valor" do prévio descartado.** Rationale: depende de ordem de leitura — conflita com C.1 (determinismo absoluto) a menos que se declare critério de ordenação, o que reintroduz complexidade sem ganho analítico real. "Primeiro" raramente tem significado real — normalmente quando se quer "primeiro", quer-se "primeiro cronologicamente" (já coberto por ordenação do eixo) ou "valor mais representativo" (nenhum dos dois é "primeiro" puro).

**Duplicidade em modo declarado pré-agregado** dispara W-V8-DUPLICIDADE-PREAGREGADA (alerta, não bloqueio). Usuário aceita e processa com regra escolhida, revisa a base, ou alterna modo (apenas muda rótulo; mecânica é a mesma).

**Registro no Diagnóstico e aba Parâmetros:** modo declarado · regra de agregação (quando há medida) · linhas originais vs linhas após consolidação · lista de pares com múltiplas linhas consolidadas (até limite de exibição).

**Razão:** (1) Detecção automática de modo respeita C.5 — motor declara o que viu (duplicidades detectadas), usuário confirma; não decide pelo usuário qual modo é "a verdade". (2) Consolidação única simplifica motor — uma rotina alimentada por uma regra de agregação; modo vira rótulo semântico. (3) Aplicação condicional da regra (só com medida) respeita especificidade V8: presença é binária, não se agrega; só medida numérica faz sentido agregar. (4) 5 regras T-AGRUPA canônicas mantêm consistência com V2/V3/V4 — zero duplicação conceitual. (5) "Primeiro valor" descartado porque violaria C.1 sem ganho analítico — substituído por opções determinísticas. (6) Duplicidade em pré-agregado como alerta (não bloqueio) respeita uso legítimo (dois canais reportando mesma entidade no mesmo mês, por exemplo).

**Impacto:**
- dcv_v8.md §4.1 (modo + consolidação completa)
- F-MOT (Fase 1) recebe requisito: motor V8 consome T-AGRUPA com 5 regras canônicas, aplicação condicional à presença de medida
- F-EXP (Fase 1) recebe requisito: aba Parâmetros V8 registra modo + regra + auditoria de consolidação
- T-MODELO persiste: modo declarado + regra de agregação (quando aplicável)
- GLOSSARIO §5.V8 ganha entradas "Modo Transacional vs Modo Pré-agregado", "Regra de agregação V8 — aplicação condicional"
- 2 warnings V8: W-V8-MODO-INFERIDO (informativo), W-V8-DUPLICIDADE-PREAGREGADA (alerta)
- T-AGRUPA em CONTEXT §6 e GLOSSARIO §4 **sem alterações** — V8 é consumidora, não formalizadora

**Referência canônica:** `/specs/dcv/dcv_v8.md` §4.1

---

### D-073 — Intervalo De/Até V8 · mínimo de 2 pontos (alerta, não bloqueio) · divergência justificada com V3 · padrão "herança adaptada à natureza analítica"
**Data:** 2026-04-19 · **Bloco:** DCV-V8 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V8 PARTE 2.4 declarou intervalo De/Até obrigatório; PARTE 2.8 estabeleceu mínimo operacional 2 pontos com alerta (recomendado 3). V3 (D-064) bloqueia em < 3 pontos efetivos. Divergência direta prévio V8 × V3 que precisava ser decidida: harmonizar V8 com V3 (bloquear em < 3) ou preservar especificidade V8 (alerta em 2)? Refino T-06 formalizou intervalo completo com comportamentos-limite, harmonizou comportamentos-limite com V3, e resolveu divergência preservando especificidade V8 via novo padrão de método.

**Decisão:** V8 **executa com alerta em 2 pontos efetivos**; bloqueia em < 2. Divergência explícita com V3 (que bloqueia em < 3) justificada pela natureza analítica distinta: V3 calcula Diferença e Variação entre pares consecutivos — com 2 pontos só há 1 par, insuficiente para leitura de tendência; V8 classifica presença no ponto — com 2 pontos, ponto 1 (Novo) e ponto 2 (Contínuo/Novo/Ausente) produzem classificação estruturalmente válida, ainda que leitura de ciclo de vida fique limitada.

**Default declarado De/Até** (mesma mecânica V3): De = primeiro ponto da base consolidada, Até = último ponto. Ambos visíveis antes da execução, editáveis em um clique. W-V8-INTERVALO-DEFAULT registra aceitação.

**Intervalo declarado vs intervalo efetivo** preservados separadamente (herança V3 D-064). Declarado persiste em T-MODELO e aba Parâmetros; efetivo é o aplicado após ajustes-limite. Aba Parâmetros lista ambos lado a lado quando diferirem.

**6 comportamentos-limite com warnings:** De < primeiro ponto → W-V8-INTERVALO-AJUSTE-INICIO (AJUSTE_LEVE) · Até > último ponto → W-V8-INTERVALO-AJUSTE-FIM (AJUSTE_LEVE) · De > Até → W-V8-INTERVALO-INVALIDO (bloqueio) · efetivo < 2 → W-V8-PONTOS-MIN (bloqueio) · efetivo = 2 → W-V8-PONTOS-LIMITADO (alerta) · De = Até → W-V8-PONTOS-MIN.

**Padrão de método novo cristalizado:** "**herança adaptada à natureza analítica**" — visões da mesma família herdam padrões **com adaptação justificada** quando a natureza analítica de cada uma difere. Herança não é cópia cega. Registrado em CONTEXT §9 Camada C como derivado de C.5 e GLOSSARIO §10 como padrão de método consolidado.

**Razão:** (1) Bloqueio em < 2 é limite estrutural real V8 — com 1 ponto toda entidade é Novo, resultado analiticamente vazio. Isso não é decisão pelo usuário; é piso estrutural. (2) Em 2 pontos há conteúdo analítico real — bloquear decidiria pelo usuário que "ciclo de vida de 2 pontos não vale", o que em V8 não é verdade. Alerta (W-V8-PONTOS-LIMITADO) sinaliza limitação sem impedir. (3) Harmonizar com V3 (bloquear em < 3) seria cópia cega — natureza analítica V3 (comparação entre pares, precisa 3+) não se aplica a V8 (classificação no ponto, válida a partir de 2). (4) Default declarado De/Até aplica padrão D-024. (5) Preservação declarado vs efetivo permite auditoria — usuário vê o que pediu e o que motor aplicou. (6) Padrão "herança adaptada" formaliza princípio para uso em Famílias D e E futuras (V7/V9, V5/V6): herança não é cópia cega, é aplicação do que cabe à natureza analítica.

**Impacto:**
- dcv_v8.md §4.5 (intervalo De/Até completo com comportamentos-limite e mínimos V8)
- CONTEXT §9 Camada C ganha padrão "herança adaptada à natureza analítica" como derivado de C.5
- GLOSSARIO §10 ganha entrada "Herança adaptada à natureza analítica"
- GLOSSARIO §5.V8 ganha referências ao padrão
- 6 warnings V8: W-V8-INTERVALO-DEFAULT, W-V8-INTERVALO-AJUSTE-INICIO, W-V8-INTERVALO-AJUSTE-FIM, W-V8-INTERVALO-INVALIDO (bloqueio), W-V8-PONTOS-MIN (bloqueio), W-V8-PONTOS-LIMITADO (alerta)
- F-EXP (Fase 1) recebe requisito: aba Parâmetros V8 lista intervalo declarado e efetivo lado a lado
- T-MODELO persiste intervalo declarado V8 (não efetivo)

**Referência canônica:** `/specs/dcv/dcv_v8.md` §4.5 · CONTEXT §9 · GLOSSARIO §10 "Herança adaptada à natureza analítica"

---

### D-072 — Taxonomia oficial V8 · 4 classes por ponto (Novo · Contínuo · Retornou · Ausente) + Constante consolidada · adoção D-060 sobre prévio
**Data:** 2026-04-19 · **Bloco:** DCV-V8 (sessão única) · **Status:** Fechada

**Contexto:** Divergência real entre prévio V8 e antecipação D-060 (§2.3 DCV-V3): prévio declarou "Recorrente · Recuperado · Perdido" para 3 das 4 classes primárias + Constante consolidada; D-060 antecipou "Contínuo · Retornou · Ausente" (marcada como "a confirmar em DCV-V8"). Ambos vocabulários têm mérito; refino T-03 precisou decidir entre eles e fechar caso-limite (ausente agora, nunca esteve no intervalo).

**Decisão:** Taxonomia oficial V8 **adota D-060 sobre prévio** nos 3 termos divergentes. **4 classes primárias por ponto do eixo:** **Novo · Contínuo · Retornou · Ausente** (mutuamente exclusivas). **1 classe consolidada do intervalo:** **Constante** (entidade presente em todos os pontos do intervalo efetivo).

**Definições formais:**
- **Novo:** presente no ponto atual · sem presença em nenhum ponto anterior dentro do intervalo efetivo.
- **Contínuo:** presente no ponto atual · presente no ponto imediatamente anterior.
- **Retornou:** presente no ponto atual · ausente no ponto imediatamente anterior · com histórico prévio dentro do intervalo.
- **Ausente:** ausente no ponto atual · presente em pelo menos um ponto anterior do intervalo.
- **Constante** (consolidada): presente em **todos** os pontos do intervalo efetivo.

**Casos-limite fechados:**
- **Entidade presente no primeiro ponto do intervalo efetivo** = **Novo** (sem histórico anterior dentro do intervalo).
- **Entidade ausente no primeiro ponto que aparecerá depois** — não tem classificação nesse primeiro ponto (não aparece na matriz daquele ponto até sua primeira ocorrência).
- **Entidade ausente em todos os pontos do recorte efetivo** dentro de um grupo (quando aparece só em outros grupos) — **não ocupa linha** na matriz daquele grupo (economia de matriz, T-09 D-076).

**Vocabulário dual técnico/exibição:**
- Contratos técnicos em maiúsculas: `NOVO` · `CONTINUO` · `RETORNOU` · `AUSENTE` · `CONSTANTE` · `Null` (não aplicável para consolidada).
- Exibição capitalizada natural: Novo · Contínuo · Retornou · Ausente · Constante.

**Classificação atual:** classificação da entidade no **último ponto do intervalo efetivo** (rótulo para Resumo Executivo Bloco 3 e microcopy executiva).

**Termos descartados do prévio V8** (para anti-glossário §11):
- "Recorrente" → substituído por "Contínuo". Rationale: "Recorrente" exagera o escopo microscópico da classificação (ponto atual vs anterior apenas) introduzindo carga de frequência/ritmo; "Contínuo" descreve o que o motor observa sem extrapolar.
- "Recuperado" → substituído por "Retornou". Rationale: "Recuperado" carrega voz passiva + agência ("o sistema recuperou") que soa estranho em domínios além de carteira de clientes (SKU recuperado?); "Retornou" é voz ativa neutra.
- "Perdido" → substituído por "Ausente". Rationale: "Perdido" carrega carga de churn negativa; "Ausente" é descritivo neutro.
- Termos descartados podem sobreviver em microcopy de produto como contexto explicativo ("análise de perdas" = filtro sobre Ausente), **nunca no contrato técnico do motor**.
- "Ativa/Inativa" permanecem não oficiais (prévio já explicita).

**Confirma §2.3 do DCV-V3 aprovado:** a marcação "a confirmar em DCV-V8" sai; tabela §2.3 pode ter ajuste cosmético no próximo toque natural do DCV-V3 (não é refino, é limpeza editorial).

**Razão:** (1) Neutralidade declarativa preservada — cada rótulo descreve o que o motor observa sem extrapolar frequência, agência ou juízo de valor. Aplica C.5 — sistema não decide pelo usuário que "Recorrente" é positivo ou "Perdido" é negativo; apresenta fato estrutural. (2) Funciona uniformemente em todos os domínios — "Retornou" funciona para cliente, SKU, contrato, fornecedor, colaborador; "Recuperado" funciona apenas em alguns domínios. (3) Vocabulário dual técnico/exibição preserva padrão consolidado V2/V4 (D-022, D-023, D-038). (4) Casos-limite fechados com rationale explícito eliminam ambiguidade operacional para a implementação. (5) Cumprimento antecipado da antecipação D-060 — §2.3 DCV-V3 deixa de ter "a confirmar" pendente.

**Impacto:**
- dcv_v8.md §5.2 (4 classes por ponto), §5.3 (Constante consolidada), §5.4 (classificação atual), §5.5 (vocabulário dual), §13 (nomenclatura oficial V8)
- Contrato V8Result: campos `classificacao_ponto`, `classificacao_consolidada`, `classificacao_atual` com valores canônicos
- CONTEXT §4 Família B atualizada com classificações V8 concretas
- F-MOT (Fase 1) recebe taxonomia como contrato rígido
- F-EXP (Fase 1) recebe rótulos canônicos para as 7 abas do Excel
- GLOSSARIO §5.V8 ganha entradas "Classificação por ponto (V8)", "Classificação consolidada (V8)", "Classificação atual (V8)", "Vocabulário dual técnico/exibição (V8)"
- GLOSSARIO §11 anti-glossário ganha 3 termos V8 descartados (Recorrente, Recuperado, Perdido) + nota sobre Período não estrutural
- DCV-V3 §2.3 pode ser atualizado no próximo toque natural (retirar "a confirmar em DCV-V8")
- Sem warnings associados — classificação é conteúdo analítico primário, não ajuste estrutural (padrão D-076)

**Referência canônica:** `/specs/dcv/dcv_v8.md` §5.2, §5.3, §5.4, §5.5, §13 · GLOSSARIO §5.V8 Classificação por ponto (V8) · §11 anti-glossário

---

### D-071 — Posicionamento V8 na Família B · cumprimento da retroação diferida D-060 · T-SEMA fora de escopo V8 · fronteira com V6
**Data:** 2026-04-19 · **Bloco:** DCV-V8 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V8 tinha PARTE 1 curta sobre o que a visão faz, sem seção estruturada de posicionamento analítico comparável ao §2 dos DCVs V3/V4/V10/V11 aprovados. Três elementos faltavam: (a) §2 estruturado com cenário real + fronteira + unidade analítica, (b) bloco "Relação com V3" que cumprisse a retroação diferida registrada em D-060, (c) fronteira com V6 (cruzamento V6 × rastreamento sequencial V8 pode confundir usuário leigo). Refino T-02 formalizou seção completa aplicando padrão V3/V4/V10/V11 e incluiu decisão substantiva sobre T-SEMA.

**Decisão:** DCV-V8 §2 estruturado em 4 subseções: §2.1 cenário real, §2.2 relação com V6 e território vizinho, §2.3 relação com V3 (par autônomo da Família B — **cumpre retroação D-060**), §2.4 unidade analítica.

**Cumprimento antecipado da retroação diferida D-060:** §2.3 do DCV-V8 contém bloco "Relação com V3" simétrico ao §2.3 do DCV-V3 — tabela comparativa de 5 linhas (o que rastreia, unidade analítica, classificação, transversais comuns, tipo de medida) + parágrafo de fechamento sobre vocabulário declarativo autossuficiente. Padrão V11↔V1 (D-058) replicado. **Status da retroação V3→V8 passa de "aberta para próxima revisão natural de V8" a "cumprida".**

**T-SEMA fora de escopo V8 — decisão substantiva.** Presença/ausência não tem direção inerente de "melhor/pior" universal. Ganhar 50 clientes e perder 30 pode ser ótimo (crescimento de carteira) ou péssimo (churn alto mascarado) — depende do contexto de negócio. Decidir por default teria que decidir pelo usuário uma das duas interpretações, violando C.5. Semântica fica fora do escopo do motor V8; **leitura qualitativa do resultado** (Bloco 5 Resumo Executivo — leitura de ciclo de vida com 5 classes qualitativas e faixas editáveis, D-078) substitui semântica direcional. CONTEXT §6 T-SEMA ganha nota explícita "Não aplicável a V8".

**Fronteira com V6 declarativa em §2.2:** V6 é cruzamento de dois campos categóricos num universo estático (matriz cliente × produto); V8 é rastreamento de entidade ao longo de eixo **ordenado** (presença em cada ponto, com semântica sequencial entre eles). V6 expõe onde há ocorrência; V8 expõe **como a ocorrência evoluiu**. Eixo ordenado distingue — sem ordem, não há recorrência/retorno/perda.

**Unidade analítica da V8:** Entidade + Ponto do eixo + Agrupadores ativos (opcionais). Especificidade V8 relevante: **entidade** (unidade rastreada, uma só, obrigatória) é distinta de **agrupadores** (dimensões opcionais de segmentação). Mesma entidade pode ter classificações diferentes em grupos distintos. Em V3, não há distinção entidade/agrupador — só agrupadores e medida.

**Razão:** (1) Padrão §2 estruturado consolidado em V3/V4/V10/V11 garante coerência entre famílias. (2) Cumprimento antecipado da retroação D-060 respeita GLOSSARIO §10 "Retroação diferida" sem precisar de sessão dedicada futura. (3) T-SEMA fora de escopo V8 é **decisão substantiva** que aplica C.5 — V8 não decide pelo usuário se mudança de presença é positiva ou negativa; apresenta fato e oferece leitura qualitativa editável. Alternativa rejeitada (T-SEMA com semântica "maior-é-melhor = mais entidades presentes") decidiria pelo usuário uma interpretação única. (4) Fronteira com V6 em microcopy declarativa (§2.2, não em tela) respeita padrão D-060/D-058 — sistema não redireciona silenciosamente em interface operacional; usuário lê o DCV quando quer entender ambas. (5) Distinção entidade vs agrupadores explicitada porque V3 não tem essa distinção — registro evita dúvida futura na Fundação (motor V8 trata entidade diferente dos agrupadores).

**Impacto:**
- dcv_v8.md §2 completo (4 subseções)
- CONTEXT §4 Família B expandida com classificações V8 concretas
- CONTEXT §6 T-SEMA ganha nota "Não aplicável a V8"
- GLOSSARIO §4 T-SEMA ganha nota detalhada "Não aplicável a V8" com rationale
- GLOSSARIO §5.V8 ganha entradas "Recorrência e Ciclo de Vida", "Entidade (V8)"
- GLOSSARIO §10 "Retroação diferida" marcada V3→V8 como cumprida (V11→V1 permanece aberta)
- Retroação V11→V1 permanece para próxima revisão natural de V1 (padrão D-058 preservado)

**Referência canônica:** `/specs/dcv/dcv_v8.md` §2 · CONTEXT §4, §6 · GLOSSARIO §4 T-SEMA · §5.V8 · §10 Retroação diferida


### D-070 — Bloqueios operacionais V3 · 10 bloqueios · 7 diretrizes de performance
**Data:** 2026-04-19 · **Bloco:** DCV-V3 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V3 não tinha seção dedicada a bloqueios — menções dispersas (P0.7 mínimo 3 pontos; PARTE 2.3.5 colisão eixo/agrupador; PARTE 8.2/8.4 divisão por zero como classificação). Refino T-14 consolidou bloqueios herdados de D-032/D-043 + específicos V3 emergentes do refino + diretrizes de performance adaptadas.

**Decisão:** V3 formaliza **10 bloqueios operacionais** (7 herdados/adaptados de D-032/D-043 + 3 novos específicos V3) + **7 diretrizes de performance** (5 herdadas + 2 novas V3). Bloqueios específicos V3 novos: W-V3-PONTOS-MIN (intervalo efetivo < 3 pontos), W-V3-INTERVALO-INVALIDO (De > Até), W-V3-EIXO-AGRUP-COLISAO (mesmo campo declarado como eixo e agrupador). Escala de agrupadores: 1-3 normal · 4-5 aviso · 6-7 confirmação (W-V3-AGRUP-MUITOS alerta) · **8+ bloqueio** (mais conservador que V4 — V3 multiplica linhas por pontos do eixo, amplificando cardinalidade). Diretrizes novas: pré-validação de intervalo antes do processamento pesado · pré-cálculo vetorizado da aba "Recorte ponto a ponto".

**Razão:** (1) Aplicar padrão V4/V11 (D-032, D-043) para uniformidade entre visões. (2) Corte de agrupadores em 8+ reflete especificidade V3: granularidade agrupador × ponto do eixo. Em V4, 5000 agrupadores × 3 medidas = 15K linhas; em V3, 5000 agrupadores × 100 pontos = 500K linhas — corte mais conservador protege performance. (3) Colisão eixo × agrupador como bloqueio (não correção silenciosa) aplica C.5: motor não tem base para decidir qual das duas declarações é correta, qualquer correção inventaria comportamento. Prévio PARTE 2.3.5 deixou aberto; decisão aqui fecha. (4) Pré-validação de intervalo evita processamento pesado que depois bloqueia no fim — diretriz de experiência do usuário.

**Impacto:**
- dcv_v3.md §4.7 (escala de agrupadores + colisão), §7.1 (7 bloqueios), §15.2 (7 diretrizes performance)
- GLOSSARIO §6 ganha bloco Warnings V3 com 7 bloqueios + 3 alertas + 17 informativos = 27 warnings V3
- F-EXP (Fase 1) recebe requisito de pré-validação de intervalo e pré-cálculo vetorizado da aba 3 V3
- Spec S-V4 futura pode herdar o padrão se V4 ganhar similar requisito (não previsto hoje)

**Referência canônica:** `/specs/dcv/dcv_v3.md` §4.7, §7.1, §15.2 · GLOSSARIO §6 Warnings V3

---

### D-069 — Resumo Executivo V3 · 6 blocos adaptados por modo · 7 abas Excel · aba "Recorte ponto a ponto"
**Data:** 2026-04-19 · **Bloco:** DCV-V3 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V3 PARTE 9 listou 6 abas (Resumo Executivo · Trajetória Consolidada · Comparação entre Referências Consecutivas · Base Analítica · Alertas e Diagnóstico · Parâmetros) em prosa solta sem detalhamento. PARTE 12 · P-01 deixou como pendência aberta a "estrutura exploratória da aba de recorte no Excel". Refino T-13 consolidou estrutura completa aplicando padrão V4/V11 (6 blocos + faixas editáveis) + resolveu pendência do prévio.

**Decisão:** Resumo Executivo V3 segue padrão consolidado D-044 (V4) / V11 §6.1 adaptado aos dois modos da V3: **6 blocos fixos** (Cabeçalho · Números-âncora · Distribuição de classificações · Elementos destacados · Leituras descritivas de síntese com faixas editáveis · Qualidade estrutural). Bloco 5 Simples = Leitura de tendência (Crescente/Decrescente/Estável/Mista, default > 70% dos pares na classificação); Bloco 5 Comparativo = Leitura de aderência (Aderente > 70% dos pontos com |Variação| ≤ 5% / Divergente). Tolerância editável; percentual 70% fixo. Nota estática final do Bloco 5 redireciona V5/V7 para análise de variação expressiva (integra T-12).

Estrutura de **7 abas do Excel**: Resumo Executivo · Trajetória Consolidada · **Recorte ponto a ponto (nova)** · Resumo por Agrupador (condicional ≥ 2 agrupadores) · Base Analítica · Parâmetros · **Diagnóstico (última, D-017)**. Nova aba "Recorte ponto a ponto" entrega exploração interativa via **Implementação 1** (aba estática pré-calculada com todos os pares consecutivos + filtros nativos Excel). Recálculo dinâmico dentro do Excel fica como **P-V3-02-Evo**.

**Razão:** (1) Padrão 6 blocos V4/V11 consolidado — uniformidade entre visões; usuário que usa V2/V4/V11 reconhece estrutura em V3. (2) Nota V5/V7 estática (não condicional a threshold) aplica C.5: threshold arbitrário de "variação extrema" decidiria pelo usuário; nota declarativa apenas informa caminho. (3) Implementação 1 (filtros nativos) resolve 80% do caso com 5% do custo; Implementação 3 (pré-cálculo de todos os subsets com lookup por fórmula) tem custo quadrático em N pontos e fica para evolução validada por uso. (4) Aba "Recorte ponto a ponto" preserva princípio "tela e Excel nunca divergem" (prévio PARTE 9) porque toda célula é calculada pelo motor Python, filtros Excel apenas exibem subset sem recalcular.

**Impacto:**
- dcv_v3.md §6 completo (6 blocos §6.2, 7 abas §6.3, aba "Recorte ponto a ponto" §6.4)
- F-EXP (Fase 1) recebe requisito: aba "Recorte ponto a ponto" com estrutura pré-calculada de pares consecutivos · filtros ativos em todas as 7 abas
- Roadmap V3 ganha P-V3-02-Evo (aba parametrizável com recálculo dinâmico)
- GLOSSARIO §5.V3 ganha entradas "Leitura de tendência", "Leitura de aderência", "Recorte ponto a ponto"
- W-V3-LEITURA-CUSTOM registrado

**Referência canônica:** `/specs/dcv/dcv_v3.md` §6.2, §6.3, §6.4 · GLOSSARIO §5.V3

---

### D-068 — Ruptura/descontinuidade fora de escopo V3 permanente · redirecionamento declarativo V5/V7
**Data:** 2026-04-19 · **Bloco:** DCV-V3 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V3 PARTE 7.2 declarou explicitamente "A V3 não trabalha com ruptura como classificação oficial nesta versão". Refino T-12 formalizou essa decisão com racional analítico e registrou permanentemente (não apenas "nesta versão").

**Decisão:** Ruptura/descontinuidade **fora de escopo V3 permanente** (não apenas MVP). §10 Pontos de atenção do DCV refinado explicita racional: V3 rastreia evolução de valor em eixo ordenado (Diferença e Variação % entre consecutivos); variação extrema é fenômeno analítico melhor atendido por outras visões pelo ângulo correto — **V5 · Dispersão e Outliers** (estatístico: IQR, Z-score, percentil) e **V7 · Desvio da Média do Grupo** (comparativo: desvio em relação aos pares). Adicionar "ruptura" em V3 duplicaria conceito sem precisão analítica nova. Sem roadmap P-V3-XX-Evo próprio (não é evolução futura, é escopo definido).

Microcopy orientativa integrada ao **Bloco 5 do Resumo Executivo** (nota estática final, sempre presente, sem condição de disparo): "Variações expressivas observadas ao longo da sequência merecem investigação especializada: V5 (outlier estatístico), V7 (desvio comparado ao grupo)."

**Razão:** (1) Distinção honesta: V3 tem território analítico claro (evolução numérica); ruptura como fenômeno distinto está em V5 e V7. Duplicar seria sobreposição arquitetural. (2) Opção rejeitada de threshold automático (ex: Variação % > 200% dispara flag RUPTURA) viola C.5 — decidir pelo usuário o que é extremo. (3) Opção rejeitada de roadmap aberto cria dívida futura sem racional analítico (V5/V7 já cobrem o tema). (4) Nota declarativa no Resumo Executivo aplica padrão de "microcopy declarativa autossuficiente" consolidado em T-02 — orienta sem redirecionar silenciosamente.

**Impacto:**
- dcv_v3.md §10 (Pontos de atenção) · parágrafo dedicado
- dcv_v3.md §6.2 Bloco 5 · nota estática final integrada
- Sem novo warning V3 (variação grande é resultado legítimo, não ajuste estrutural — não pertence ao Diagnóstico)
- Sem roadmap P-V3-XX-Evo próprio para ruptura
- V5 e V7 DCVs futuros ganham reconhecimento explícito de serem o "destino" conceitual de análise de variação expressiva — validação no refino delas

**Referência canônica:** `/specs/dcv/dcv_v3.md` §10 · §6.2 Bloco 5

---

### D-067 — Modo Comparativo V3: T-SEMA integralmente herdado + evolução complementar opcional com default desligado
**Data:** 2026-04-19 · **Bloco:** DCV-V3 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V3 PARTE 8.3 declarou "aplicar classificação semântica herdada da V2" sem especificar qual. PARTE 8.5 mencionou evolução complementar de A e B como "leitura complementar" sem fechar mecânica (P-02 do prévio). Refino T-11 formalizou herança completa de T-SEMA (V2, V3, V7, V9) e decidiu comportamento da evolução complementar.

**Decisão:** V3 **herda integralmente T-SEMA** (D-024 padrão). Semântica declarada pelo usuário (maior-é-melhor · menor-é-melhor · neutro) com default declarado do motor baseado em heurística de nome de campo (compartilhada com V2). Classificação estrutural (AUMENTOU · REDUZIU · ESTAVEL · NAO_APLICAVEL) sempre calculada; classificação semântica derivada da tabela estrutural × semântica (Melhorou/Piorou/Estável/Apenas informar com semântica não-neutra; Aumentou/Reduziu/Estável com neutra). **Semântica é da medida, não da direção da comparação** — princípio V2 preservado.

**Evolução complementar de Origem e Comparado no Modo Comparativo:** opção declarada na configuração, **default desligado**. Quando ligada, Base Analítica ganha duas colunas adicionais "Evolução Origem (ponto anterior)" e "Evolução Comparado (ponto anterior)". Não afeta classificação semântica principal (sempre sobre par Origem vs Comparado no ponto).

**Razão:** (1) T-SEMA já está em CONTEXT §6 como transversal de V2, V3, V7, V9. V3 absorver significa herdar, não reinventar. (2) Semântica da medida (não da direção) foi princípio consolidado em V2 — "Realizado > Orçado" em Receita é positivo, em Custo é negativo; a diferença está na natureza da medida. (3) Evolução complementar default desligado respeita prévio PARTE 8.3 que define regra central do Comparativo como "comparação Origem vs Comparado em cada ponto, com mesma lógica semântica da V2" — evolução individual é opcional, não o coração. (4) Opção rejeitada de ligar por default engorda Excel/tela sem necessidade do uso primário.

**Impacto:**
- dcv_v3.md §4.8 (configuração semântica + evolução complementar) · §5.4 (tabela de classificação semântica) · §6.1 (colunas condicionais no V3Result)
- Warnings W-V3-SEMA-DECL, W-V3-SEMA-CUSTOM, W-V3-COMP-EVOLUCAO
- T-SEMA em CONTEXT §6 e GLOSSARIO §4 **sem alterações** — V3 é consumidora, não formalizadora
- GLOSSARIO §5.V3 ganha entradas "Classificação estrutural vs semântica" e "Evolução complementar"

**Referência canônica:** `/specs/dcv/dcv_v3.md` §4.8, §5.4, §6.1

---

### D-066 — Tipos de medida e negativos na V3 (herança V4 adaptada) + redirecionamento estado/situação para V8/V6
**Data:** 2026-04-19 · **Bloco:** DCV-V3 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V3 PARTE 2.2 listou tipos ("Numéricos: valor monetário, quantidade, saldo, custo, volume, percentual, índice/score; Qualitativo: estado/situação") sem tratamento por tipo. Diferença notável: prévio **aceita** estado/situação em V3 (tratamento ambíguo), enquanto V2/V4 bloqueiam. Refino T-10 aplicou taxonomia consolidada D-025 + padrão V4 adaptado para natureza evolutiva V3.

**Decisão:** V3 herda taxonomia D-025 (4 tipos: aditivo · relativo · não-aditivo · estado/situação). Tratamento por tipo adaptado para V3: aditivo executa sem aviso; relativo/não-aditivo recebe **default declarado com 3 opções** ("analisar mesmo assim" default, "escolher outra medida", "agregar por média ponderada antes" — disponível só em Modo Simples com campo de peso); **estado/situação é bloqueio operacional com redirecionamento V8/V6** (coerente com fronteira V3×V8 fechada em T-02). Modo Comparativo com relativo: opção de média ponderada desativada (comparação ponto-a-ponto, não agrega entre pontos).

**Negativos: 2 opções** (não 3 como V4): "analisar com valores líquidos" (default) · "usar valor absoluto". Opção V4 "separar análise em positivos e negativos" não se aplica a V3 (V3 é evolução por agrupador, não composição sobre universo — separar quebra sequência).

**Contrato `classificacao_medida` V3** idêntico V4: VALOR_VALIDO/VALOR_NEGATIVO/NULO_MEDIDA. Nulos na medida preservados com classificação; excluídos do cálculo; Diferença/Variação entre ponto válido e ponto nulo = None (comparação consecutiva pula naturalmente, mecanismo similar ao de ausência do agrupador de D-065).

**Razão:** (1) Padrão default declarado consolidado em D-024/D-036 estendido. (2) Estado/situação bloqueia em V2/V4 com redirecionamento V6 porque análise numérica não se aplica a categórico; em V3, redirecionamento natural é V8 (rastrear presença/trajetória de estado ao longo do tempo) ou V6 (cruzar com outra dimensão) — fronteira V3×V8 fechada em T-02 valida. Opção rejeitada de "criar Modo 3 V3 para estado/situação" duplicaria V8. (3) Só 2 opções para negativos reflete natureza V3: evolução por agrupador, não composição.

**Impacto:**
- dcv_v3.md §4.3 (tipos + negativos + nulos com `classificacao_medida`)
- Warnings W-V3-TIPO-DECL, W-V3-TIPO-REL, W-V3-NEGATIVOS, W-V3-TIPO-INCOMPAT (bloqueio), W-V3-NULL, W-V3-NULL-MASS
- D-025 (4 tipos de medida) **sem alterações** — V3 é consumidora
- GLOSSARIO §5.V3 ganha entrada sobre redirecionamento estado/situação para V8/V6

**Referência canônica:** `/specs/dcv/dcv_v3.md` §4.3

---

### D-065 — Lacunas no eixo × ausência do agrupador: detecção por tipo de eixo + flags estruturais no V3Result
**Data:** 2026-04-19 · **Bloco:** DCV-V3 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V3 PARTE 2.3.10 declarou "A V3 não preenche lacunas com zero e não cria pontos artificiais; sequência é formada apenas pelos pontos existentes". Exemplo: Jan→Fev→Mar→Mai→Jun, comparações padrão Fev vs Jan, Mar vs Fev, Mai vs Mar, Jun vs Mai. Mas deixou aberto: detecção de lacuna pelo motor, registro no Diagnóstico, impacto analítico, densidade de lacunas, e distinção **lacuna-do-eixo × lacuna-do-agrupador** (fenômenos semanticamente distintos não tratados pelo prévio). Refino T-09 formalizou.

**Decisão:** V3 distingue dois fenômenos:

**Lacuna do eixo (macroscópica):** ponto ausente no universo consolidado como um todo. Detecção automática depende do tipo de eixo (T-05): temporal → sim (comparação com sequência canônica); ordinal com prefixo numérico → sim (sequência 1,2,3,...N); ordinal sem prefixo e manual → não (sem referência semântica). Warning **W-V3-EIXO-LACUNA** (informativo, AJUSTE_LEVE).

**Ausência do agrupador em ponto (microscópica):** agrupador específico sem valor em ponto específico, enquanto outros agrupadores têm valor lá. Detecção independe do tipo de eixo. Warning **W-V3-AGRUP-AUSENCIA-PONTO** (informativo, AJUSTE_LEVE).

**Impacto analítico: zero no cálculo.** Comparação consecutiva pula lacunas (princípio do prévio preservado). **Visibilidade sim** — duas flags estruturais novas no V3Result: `lacuna_anterior` (ponto anterior ausente do eixo) e `ausencia_ponto` (ausência anterior do agrupador). Produzem coluna textual informativa na Base Analítica sem alterar cálculos de Diferença/Variação/Classificação.

**Densidade > 30% pontos esperados ausentes** dispara **W-V3-EIXO-LACUNA-MASSIVA** (alerta, não bloqueio — usuário pode ter razão analítica legítima). Só em eixos com detecção ativa. Threshold 30% configurável na Spec S-V3.

**Razão:** (1) Distinção lacuna-do-eixo × lacuna-do-agrupador preserva clareza analítica — fenômenos com implicações distintas (estrutural da base vs ciclo de vida natural do agrupador). (2) Detecção dependente do tipo de eixo é honesta: motor não inventa referência quando não tem (eixo manual, ordinal sem prefixo). (3) Flag estrutural sem alterar cálculo aplica C.2 (nada silencioso) + C.5 (não decide pelo usuário — apresenta). (4) Alerta em vez de bloqueio para densidade alta respeita autonomia analítica do usuário — histórico de loja nova, sazonalidade natural são casos legítimos.

**Impacto:**
- dcv_v3.md §4.5 (duas categorias de lacuna + detecção por tipo + flags)
- dcv_v3.md §6.1 (V3Result ganha colunas "Flags estruturais" e textual unificada)
- F-EXP (Fase 1) recebe requisito: flags estruturais produzem coluna textual na Base Analítica
- GLOSSARIO §5.V3 ganha entrada "Lacuna do eixo vs Ausência do agrupador em ponto"
- 3 warnings V3 novos: W-V3-EIXO-LACUNA, W-V3-AGRUP-AUSENCIA-PONTO, W-V3-EIXO-LACUNA-MASSIVA

**Referência canônica:** `/specs/dcv/dcv_v3.md` §4.5, §6.1

---

### D-064 — Intervalo De/Até V3: papel analítico, default declarado, comportamentos-limite
**Data:** 2026-04-19 · **Bloco:** DCV-V3 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V3 PARTE 2.3.9 declarou "intervalo De/Até definido pelo usuário afeta o cálculo da análise principal" sem especificar papel analítico (subset vs truncamento), default, comportamentos-limite (De antes do primeiro ponto, Até depois do último, De > Até), relação com mínimo de 3 pontos, relação com seleção prévia de pontos de T-06. Refino T-08 formalizou.

**Decisão:** De/Até define o **subset de pontos do eixo** que entra no cálculo da análise sequencial (não truncamento pós-cálculo). Aplicado após pivot (T-06) e ordenação do eixo (T-05). Agrupadores ausentes em todos os pontos do intervalo não aparecem no resultado.

**Default declarado:** De = primeiro ponto da base consolidada; Até = último ponto. Ambos visíveis na configuração, editáveis em um clique. W-V3-INTERVALO-DEFAULT registra aceitação sem edição.

**Intervalo declarado vs intervalo efetivo:** preservados separadamente. Declarado persiste em T-MODELO e aba Parâmetros; efetivo (após ajustes-limite) registrado em aba Parâmetros quando diferiu. Comportamentos-limite: De < primeiro ponto disponível → ajuste para primeiro + W-V3-INTERVALO-AJUSTE-INICIO (AJUSTE_LEVE); Até > último → ajuste + W-V3-INTERVALO-AJUSTE-FIM (AJUSTE_LEVE); De > Até → **bloqueio W-V3-INTERVALO-INVALIDO**; intervalo efetivo < 3 pontos → bloqueio **W-V3-PONTOS-MIN**. Mínimo de 3 pontos (P0.7) aplica-se ao intervalo efetivo.

**Razão:** (1) Papel analítico de "subset do eixo" preserva princípio do prévio ("afeta o cálculo") — truncamento pós-cálculo faria Total Geral de síntese divergir de expectativa do usuário. (2) Default declarado aplica padrão D-024. (3) Separação declarado vs efetivo permite auditoria: usuário vê o que pediu e o que o motor aplicou lado a lado. (4) Ajustes-limite como AJUSTE_LEVE (não bloqueio) são respeitosos — usuário pediu Jan/22 mas base começa em Mar/23 é caso comum (histórico incompleto); motor processa o que pode e registra. (5) De > Até é bloqueio porque é erro de declaração, não comportamento-limite legítimo.

**Impacto:**
- dcv_v3.md §4.6 (intervalo De/Até completo com comportamentos-limite)
- 5 warnings V3: W-V3-INTERVALO-DEFAULT, W-V3-INTERVALO-AJUSTE-INICIO, W-V3-INTERVALO-AJUSTE-FIM, W-V3-INTERVALO-INVALIDO (bloqueio), W-V3-PONTOS-MIN (bloqueio — compartilhado com T-06)
- F-EXP (Fase 1) recebe requisito: aba Parâmetros lista intervalo declarado e efetivo lado a lado
- T-MODELO persiste intervalo declarado (não efetivo, que depende da base do momento)
- GLOSSARIO §5.V3 ganha entrada "Intervalo declarado vs Intervalo efetivo"

**Referência canônica:** `/specs/dcv/dcv_v3.md` §4.6

---

### D-063 — Multi-aba como eixo sequencial fora de escopo V3 MVP · P-V3-01-Evo · M2.STACK candidato
**Data:** 2026-04-19 · **Bloco:** DCV-V3 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V3 PARTE 2.1 mencionou "múltiplas abas representando períodos, desde que o usuário confirme" como formato aceito, mas sem especificar detecção, mecânica, ou escopo. Cenário real frequente: exportação ERP brasileira com aba por mês (Jan_2024, Fev_2024, ...). Refino T-07 decidiu escopo MVP + roadmap + candidato M2.

**Decisão:** Multi-aba como eixo sequencial **fora de escopo V3 MVP**. V3 MVP aceita **uma única aba** (consistente com V2, V4, V5, V6, V7, V8, V9, V10; distinto da Família A V1/V11 que usam T-DUAL para 2 abas). Roadmap: **P-V3-01-Evo · Múltiplas abas como eixo sequencial** (implementação futura via extensão análoga a T-DUAL mas sequencial, N abas = N pontos do eixo).

**Registrado M2.STACK como candidato** (análogo funcional a T-CONCAT candidato de D-053). M2.STACK = empilhamento de múltiplas abas estruturalmente idênticas em uma única aba com coluna discriminadora adicional contendo nome da aba de origem. Posicionamento final (transversal puro da Fundação · parte de M2 · capability compartilhada) a decidir no G-FUND ou no refino DCV-OPN correspondente.

Microcopy no Diagnóstico (ativada quando arquivo carregado tem N ≥ 3 abas): *"Se as múltiplas abas deste arquivo representam períodos distintos e você quer analisar evolução entre elas, consolide em uma única aba antes da análise. Versão futura (Módulo 2 · STACK) automatizará esse caminho."* Nota orientativa, não bloqueio.

**Razão:** (1) Aplica padrão V1/V11 (RESHAPE fora de escopo com microcopy + roadmap + M2 candidato). (2) V3 MVP com uma aba cobre 80% dos casos (dados vindos de SQL, data warehouse, relatório consolidado). (3) Implementar multi-aba nativo no MVP adicionaria ~5 pendências ao G-FUND (detecção de estrutura idêntica, tratamento de divergência, vocabulário, bloco de confirmação, warnings) sem justificativa analítica distinta de V1/V11 (que excluem RESHAPE por mesma lógica estrutural: transformação prévia é território M2). (4) M2.STACK candidato preserva caminho evolutivo — zero duplicação arquitetural futura.

**Impacto:**
- dcv_v3.md §3.2 (fora de escopo de entrada) · §9 (fronteira M2 tripla: STACK, RESHAPE, NORMALIZE)
- CONTEXT §6 ganha **M2.STACK** como candidato (segundo candidato junto de T-CONCAT)
- GLOSSARIO §4 ganha entrada M2.STACK candidato
- Planilha aba 3 ganha linha para M2.STACK candidato (posicionamento final G-FUND)
- Roadmap V3: P-V3-01-Evo

**Referência canônica:** `/specs/dcv/dcv_v3.md` §3.2, §9 · CONTEXT §6 · GLOSSARIO §4 M2.STACK

---

### D-062 — Estruturas POR_COLUNAS/POR_LINHAS da V3 · seleção de pontos · T-PIVOT terceira semântica
**Data:** 2026-04-19 · **Bloco:** DCV-V3 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V3 PARTE 2.3.7 listou "eixo pode estar em colunas ou em linhas" sem especificar mecânica, quando dispara pivot, como T-PIVOT é consumido, se há bloco de seleção análogo a V4 §6.2, default declarado. Refino T-06 formalizou aplicando padrão V4 adaptado.

**Decisão:** V3 aceita **duas estruturas canônicas** declaradas na configuração: **POR_COLUNAS** (cada ponto do eixo é coluna distinta) e **POR_LINHAS** (pontos empilhados com coluna discriminadora). Em POR_LINHAS, motor aplica pivot via **T-PIVOT** antes do cálculo. Estrutura declarada pelo usuário com default declarado do motor (detecção baseada em nomes de colunas reconhecíveis + N ≥ 3 valores de padrão cronológico). Warning W-V3-EIXO-ESTRUTURA-INFERIDA.

**Bloco "Seleção de pontos do eixo em POR_LINHAS":** ativado quando discriminadora tem **10 ou mais valores únicos** (limite configurável na Spec). Lista todos os pontos pré-selecionados; usuário pode desmarcar subset antes do pivot. Warning W-V3-EIXO-PONTOS-MUITOS. Coexiste com De/Até (operam em momentos distintos: seleção antes do pivot, De/Até depois da ordenação); W-V3-EIXO-SELECAO+INTERVALO registra uso combinado.

**T-PIVOT formaliza terceira semântica:** estados (V2, D-026) · medidas (V4, D-039) · **pontos do eixo (V3, esta decisão)**. Não é extensão estrutural — motor opera sobre dimensão em coluna discriminadora qualquer; esta decisão formaliza a terceira semântica no vocabulário da Fundação.

**Razão:** (1) Padrão V4 §6.2 adaptado — bloco de seleção ativa diferença semântica ("pontos do eixo" vs "medidas"), evita colisão vocabular deliberada (como V4 fez com "Modo 4" V2). (2) Limite de 10 pontos reflete ergonomia UI: acima disso, cabeçalhos de coluna ficam cramped; usuário vai querer filtrar. (3) Default declarado aplica D-024. (4) Seleção prévia + De/Até são mecanismos complementares — seleção é escolha estrutural (não-contígua possível), De/Até é recorte contíguo ordenado.

**Impacto:**
- dcv_v3.md §3.1 (estruturas + seleção prévia) · §4.7 (colisão eixo × agrupador como bloqueio — ver D-070)
- CONTEXT §6 T-PIVOT ganha terceira semântica formalizada
- GLOSSARIO §4 T-PIVOT reescrita com 3 semânticas
- GLOSSARIO §5.V3 ganha entradas "Coluna discriminadora do eixo" e "Bloco 'Seleção de pontos do eixo em POR_LINHAS'"
- 4 warnings V3: W-V3-EIXO-PIVOT, W-V3-EIXO-PONTOS-MUITOS, W-V3-EIXO-ESTRUTURA-INFERIDA, W-V3-EIXO-SELECAO+INTERVALO

**Referência canônica:** `/specs/dcv/dcv_v3.md` §3.1 · CONTEXT §6 T-PIVOT · GLOSSARIO §4 T-PIVOT

---

### D-061 — T-EIXO formalizada · 3 tipos canônicos · default declarado · herança D-026
**Data:** 2026-04-19 · **Bloco:** DCV-V3 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V3 PARTE 2.3.6 listou 3 tipos de eixo (temporal · lógico/ordinal · manual) sem especificar mecânica de cada, detecção, default, vocabulário, relação com ordenação (PARTE 2.3.8: "IA pode sugerir, usuário pode ajustar, motor respeita ordem final confirmada"). Refino T-05 formalizou T-EIXO como transversal da Fundação, decidiu mecânica completa, vincula V8.

**Decisão:** T-EIXO formalizada com **3 tipos canônicos**:
- **Temporal** — reconhecedor de padrões cronológicos pt-BR/pt-EN **herdado de D-026 (T-AGRUPA)** sem reimplementação. Zero duplicação arquitetural.
- **Lógico/ordinal** — detecção de prefixo ou sufixo numérico no rótulo; ordem default pelo numérico; alfabética quando prefixo não detectado.
- **Manual** — fallback quando nenhum padrão detectado; ordem de primeira ocorrência.

**Tipo declarado pelo usuário com default declarado do motor.** Prioridade quando múltiplos padrões detectados simultaneamente: temporal > lógico/ordinal > manual. **Ordem final sempre confirmada pelo usuário** (princípio P0.5 do prévio preservado). Reordenação manual sobre eixo temporal/ordinal dispara W-V3-EIXO-ORDEM-MANUAL (auditoria). Aceitação do tipo por default dispara W-V3-EIXO-TIPO-INFERIDO.

**Lacuna detectada automaticamente em temporal e ordinal com prefixo (por comparação com sequência canônica); não em manual ou ordinal sem prefixo** (sem referência semântica).

**Decisão vincula V8:** V8 (próxima da Família B) herda os 3 tipos, detecção herdada, vocabulário unificado, padrão W-V{N}-EIXO-* análogo.

**Razão:** (1) Formalização transversal de Fundação análoga a D-041 (T-RANK). T-EIXO era transversal com dimensões preliminares em CONTEXT §6; esta decisão completa. (2) Herança direta de D-026 (T-AGRUPA) para temporal elimina duplicação — mesmo reconhecedor que ordena cronologicamente em V2/V4 serve ao eixo temporal de V3/V8. (3) Default declarado respeita C.5 via padrão D-024 — motor detecta e propõe, usuário confirma ou edita. (4) Ordem final sempre confirmada respeita princípio P0.5 do prévio e C.5 — motor não impõe ordem sem confirmação. (5) Detecção de lacuna dependente do tipo é honesta — não inventar referência onde não há.

**Impacto:**
- dcv_v3.md §4.4 (tipos + detecção + ordem) · §4.5 (lacunas dependentes de tipo)
- CONTEXT §6 T-EIXO reescrita com dimensões formalizadas (D-061 referenciada)
- GLOSSARIO §4 T-EIXO reescrita completamente com 3 tipos, default declarado, herança D-026
- GLOSSARIO §5.V3 ganha entradas "Tipo do eixo" e "Ponto do eixo" como termos canônicos
- Planilha aba 3 L23 (T-EIXO): passa de preliminar a formalizada
- 2 warnings V3: W-V3-EIXO-TIPO-INFERIDO, W-V3-EIXO-ORDEM-MANUAL
- DCV-V8 futuro herda integralmente (zero retrabalho conceitual)

**Referência canônica:** `/specs/dcv/dcv_v3.md` §4.4, §4.5 · CONTEXT §6 T-EIXO · GLOSSARIO §4 T-EIXO

---

### D-060 — Posicionamento da Família B · Sequência (V3 × V8) + retroação diferida sobre DCV-V8
**Data:** 2026-04-19 · **Bloco:** DCV-V3 (sessão única) · **Status:** Fechada

**Contexto:** Prévio V3 não mencionou V8 em nenhum momento (PARTE 1.2 cobriu apenas distinção V3 × V2). V3 é primeira da Família B · Sequência; precedentes V11 §2.3 (Família A) e V4 §2 (Família C) cristalizaram o padrão: DCV da primeira visão de família carrega posicionamento analítico da família inteira + distinção vocabular entre suas visões. Refino T-02 formalizou Família B aplicando o padrão.

**Decisão:** Família B · Sequência ao longo de eixo ordenado definida como "visões que acompanham como algo se comporta ao longo de eixo sequencial ordenado; V3 rastreia valor, V8 rastreia presença/ausência; ambas consomem T-EIXO". V3 e V8 são **visões autônomas** (não há view especializada entre elas), unidas por consumo de T-EIXO. Vocabulário declarativo autossuficiente em cada visão — nenhuma menciona a outra em interface operacional. Quem precisa entender ambas lê o DCV.

DCV-V3 §2.3 contém tabela comparativa V3 × V8 de 5 linhas (o que rastreia, unidade analítica, classificação do resultado, transversais comuns, tipo de medida) + parágrafo de fechamento sobre vocabulário declarativo. Classificação V8 "Novo · Contínuo · Ausente · Retornou" marcada *(a confirmar em DCV-V8)*.

**Retroação diferida registrada:** DCV-V8 (próximo refino da Família B) receberá bloco "Relação com V3" simétrico ao §2.3 deste DCV. Execução na próxima revisão natural de V8 (DCV-V8 ou Spec S-V8), **não é sessão dedicada imediata**. Aplica padrão consolidado em D-058 (V11↔V1).

**Razão:** (1) Padrão V11↔V1 (D-058) validado; aplicar intacto à Família B garante coerência estrutural entre famílias. (2) Microcopy declarativa sem redirecionamento em interface respeita C.5 — sistema não tenta "saber" qual visão é a certa, apresenta vocabulário claro; quem escolhe é o usuário. (3) Opção rejeitada de microcopy cruzada em tela ("esta visão rastreia valor; para presença use V8") diverge de V11 e introduz inconsistência de padrão. (4) Retroação diferida respeita hierarquia Fase 0 — produzir DCVs novos é mais valioso que revisitar aprovado para ajuste cosmético.

**Impacto:**
- dcv_v3.md §2.3 (tabela V3 × V8 + vocabulário declarativo) · §11.2 (retroação diferida registrada)
- CONTEXT §4 Família B expandida de "uma linha" para descrição análoga à Família A
- GLOSSARIO §5.V3 ganha entrada "Família B · Sequência ao longo de eixo ordenado"
- GLOSSARIO §10 ganha entrada "Retroação diferida" como padrão de método consolidado (V11→V1 em D-058; V3→V8 agora)
- DCV-V8 futuro herda padrão com retroação natural

**Referência canônica:** `/specs/dcv/dcv_v3.md` §2.3, §11.2 · CONTEXT §4

---

### D-059 — Sumário do refino DCV-V3 · 13 pendências fechadas em sessão única
**Data:** 2026-04-19 · **Bloco:** DCV-V3 (sessão única) · **Status:** Fechada

**Contexto:** Refino DCV-V3 executado em sessão única (19/04/2026) seguindo padrão D-019. Mapa de 14 pendências originais reduzido a 13 efetivas (T-04 absorvida em T-03 — posicionamento analítico + casos de uso reais consolidados em §2 único, economizando bloco sem perder conteúdo). Padrão de condução D-019 aplicado integralmente: ritual de abertura com leitura dos 4 documentos canônicos + 4 DCVs anexados, fila racionalizada de pendências em 4 blocos (A · Fronteira · B · T-EIXO · C · Semântica, modos, cálculo · D · Saída e operação), uma pendência por vez com opções explícitas e C.5 como primeira lente, mini status-checks a cada ~3 pendências, sinalização de densidade no 3º status-check (D-034) com recomendação de 2 sessões (rejeitada pela Usuária; continuou em sessão única com kit completo).

Sessão foi densa — 13 pendências + 2 momentos de elicitação substantiva (T-13 sobre aba "Recorte ponto a ponto", onde a Usuária pediu áudio e direcionou a decisão para Implementação 1 com roadmap Implementação 3). Kit completo D-033 produzido na mesma sessão, testando limite de janela de contexto.

**Decisão:** **DCV-V3 refinado.** Consolida 13 pendências estruturais com 11 decisões específicas (D-060 a D-070) mais esta (D-059) como sumário. 27 warnings V3 catalogados (7 bloqueios · 3 alertas · 17 informativos). Próxima Fase 0: **DCV-V8** (Família B · Sequência) herda T-EIXO formalizada aqui, vocabulário da família, retroação diferida registrada.

**13 decisões consolidadas do refino:**

| # | Tema | Referência |
|---|---|---|
| T-01 | Vocabulário: aglutinador → agrupador | dcv_v3.md §13 (não gera D-XXX; consolidação terminológica) |
| T-02 | Posicionamento Família B + V3 × V8 | D-060 · dcv_v3.md §2.3 |
| T-03+T-04 | Fronteira V3 × V2 × V4 + casos de uso reais | dcv_v3.md §2.1, §2.2 (não gera D-XXX; aplicação de padrão §2) |
| T-05 | Tipos de eixo + default declarado + herança D-026 | D-061 · dcv_v3.md §4.4 |
| T-06 | POR_COLUNAS/POR_LINHAS + seleção de pontos + T-PIVOT | D-062 · dcv_v3.md §3.1 |
| T-07 | Multi-aba fora de escopo MVP + M2.STACK candidato | D-063 · dcv_v3.md §3.2, §9 |
| T-08 | Intervalo De/Até + comportamentos-limite | D-064 · dcv_v3.md §4.6 |
| T-09 | Lacunas eixo × agrupador + flags estruturais | D-065 · dcv_v3.md §4.5 |
| T-10 | Tipos de medida + negativos + redirecionamento estado/situação | D-066 · dcv_v3.md §4.3 |
| T-11 | Modo Comparativo: T-SEMA + evolução complementar | D-067 · dcv_v3.md §4.8, §5.4 |
| T-12 | Ruptura fora de escopo V3 + nota V5/V7 | D-068 · dcv_v3.md §10 |
| T-13 | Resumo Executivo + 7 abas + aba "Recorte ponto a ponto" | D-069 · dcv_v3.md §6 |
| T-14 | Bloqueios operacionais + performance | D-070 · dcv_v3.md §4.7, §7.1, §15.2 |

**Razão:** (1) Sessão única validou que refino denso pode caber em uma sessão se a maioria das pendências herda padrões consolidados (V4/V11 como substrato, C.5 como lente default, D-026 como capability reaproveitada para T-EIXO temporal). (2) T-04 absorvida em T-03 foi refinamento do método — "dois blocos fazem trabalho parecido" reconhecido cedo e consolidado. (3) Kit D-033 completo em sessão única estabelece precedente para refinos de densidade média-alta com padrões fortes de herança (V4→V10 precedente + V3 agora). Refinos com decisões mais pioneiras (V2 primeira do método; V11 com motor probabilístico inédito) justificam 2 sessões.

**Impacto:**
- 1 DCV aprovado a mais → **6 de 11 DCVs aprovados** na Fase 0 (V2, V1, V11, V4, V10, V3) após aprovação formal deste
- Fila remanescente Fase 0: **V8 → V7 → V9 → V5 → V6** (5 DCVs)
- T-EIXO formalizada como transversal de Fundação (D-061) — quarta transversal formalizada no projeto (além de T-RANK por D-041, T-FUZZY por D-052, padrão default declarado por D-024)
- M2.STACK registrado como candidato de M2 — segundo candidato junto de T-CONCAT (D-053)
- Próximo bloco: DCV-V8 (herda T-EIXO integralmente; retroação natural registrada)

**Referência canônica:** `/specs/dcv/dcv_v3.md` · D-060 a D-070 · CONTEXT §6 T-EIXO · GLOSSARIO §4 T-EIXO + §5.V3 + §6 Warnings V3


### D-058 — DCV-V11 aprovado · sumário da sessão 2 do refino · retroação sobre V1 registrada
**Data:** 2026-04-19 · **Bloco:** DCV-V11 (sessão 2 de 2) · **Status:** Fechada

**Contexto:** Sessão 2 do DCV-V11 (19/04/2026) executou o Bloco C do refino (T-09, T-10, T-12), consolidando as 4 pendências remanescentes após a sessão 1 ter fechado Blocos A e B em modo parcial (D-054). Padrão D-019 aplicado. Produziu DCV refinado final em prosa (`dcv_v11.md`) com 13 decisões consolidadas, submetido à aprovação da Usuária, e kit D-033 completo (CONTEXT v6, GLOSSARIO v6, planilha, D-XXX, prompt da próxima sessão).

**Decisão:** DCV-V11 **aprovado** ao fim da sessão 2. Fase 0 avança: 5 de 11 DCVs aprovados (V1, V2, V4, V10, V11). Próximo DCV em fila: V3 (Família B · Sequência). Retroação registrada: DCV-V1 aprovado não menciona V11 (V11 não existia na data); bloco "Relação com V11" curto em §2 do DCV-V1 fica como tarefa diferida — execução na próxima revisão natural de V1 (S-V1 ou atualização por demanda), não é sessão dedicada imediata. D-054 (que estava Provisória aguardando aprovação do DCV final) é promovido a Fechada por esta entrada.

**3 pendências fechadas na sessão 2 (Bloco C):**

| Tema | Resolução |
|---|---|
| T-09 Estrutura de abas do Excel | 6 abas canônicas (Resumo Executivo · Resumo por Agrupador condicional · Pareamentos · Sem par · Ponte condicional · Diagnóstico) · aba única "Pareamentos" com todas as colunas originais de ambos os lados (prefixo `[Origem]`/`[Comparado]` + separador visual) · ordem canônica por categoria (Conciliado → Divergência de valor → Conciliado por valor → Pareamento frágil) depois score decrescente · aba "Sem par" em dois blocos verticais espelhando caso-referência Protheus × Safra · novo W-V11-PAREAMENTO-LARGO (>50 colunas) |
| T-10 Ponte de Conciliação opcional | Aba autônoma condicional à declaração de saldos + bloco síntese de 3-4 linhas no Resumo Executivo (Seção 5B) · ausência da Ponte sinalizada no Diagnóstico sem conotação de dado faltando · microcopy declarativa sem referência a V1 (coerente com T-01) · 4 campos numéricos digitados (saldo anterior/final × Origem/Comparado) em etapa opcional "Reconciliação de saldo" · estrutura em 3 blocos (diferença saldo anterior · impacto líquido · conferência) herdada do caso-referência · referência a coluna de saldo como P-V11-04-Evo · novo W-V11-PONTE-RESIDUO (Bloco 3 não zera) |
| T-12 Fronteira com Módulo 2 | Higiene textual básica (lowercase · acentos · não-alfanuméricos) encapsulada em T-FUZZY, invisível ao usuário, registrada no Diagnóstico em linha informativa única · transformações semânticas (abreviações, stop-words, regex) ficam para M2.NORMALIZE futuro · NORMALIZE fora do escopo V11 MVP · microcopy no Diagnóstico sinaliza M2.NORMALIZE como opção futura condicional a alta incidência de "Pareamento frágil" · RESHAPE mantém exclusão herdada de V1 · CONCAT já absorvido em T-04 (D-053) |

**13 decisões totais do refino:**

| # | Tema | Sessão | Referência |
|---|---|---|---|
| T-00 | Arquitetura de dois passes texto→valor | 1 | D-051 |
| T-05 | Tolerância com papel duplo | 1 | D-054 resumo |
| T-02 | Nomeação default dos lados | 1 | D-054 resumo |
| T-01 | Fronteira V1/V11 navegável | 1 | D-054 resumo |
| T-03 | Mapeamento semântico de valor | 1 | D-054 resumo |
| T-04 | Composição de campos contextuais (T-CONCAT) | 1 | D-053 · D-054 resumo |
| T-06 + T-11 | Algoritmo de score + T-FUZZY confirmado | 1 | D-052 · D-054 resumo |
| T-07 | Estratégia de alocação (guloso) | 1 | D-054 resumo |
| T-08 | Classificação e taxonomia de 5 categorias | 1 | D-051 · D-054 resumo |
| T-09 | Estrutura de abas do Excel | 2 | esta entrada |
| T-10 | Ponte de Conciliação opcional | 2 | esta entrada |
| T-12 | Fronteira com Módulo 2 | 2 | esta entrada |

**Razão:** (1) Aprovação formal do DCV-V11 consolida a 5ª visão aprovada da Fase 0, fechando totalmente a Família A (V2 + V1 + V11) antes de abrir a Família B — ordem estabelecida em D-048. (2) Bloco C concentrou decisões de saída e fronteira, naturalmente mais leves que Bloco B (coração técnico), permitindo sessão 2 carregar também produção do kit D-033 completo sobre decisões já cristalizadas. (3) Retroação sobre V1 registrada como diferida (não imediata) respeita hierarquia de prioridades da Fase 0 — continuar produzindo DCVs novos é mais valioso que revisitar DCV já aprovado para ajuste cosmético de enquadramento.

**Impacto:**
- `/specs/dcv/dcv_v11.md` criado (arquivo canônico do DCV aprovado)
- Planilha aba 2 L8 (V11): DCV refinado → ✅ · DCV aprovado → ✅ + nota resumida
- Planilha aba 1 L10 (próximo passo): DCV-V3 (Família B · Sequência)
- CONTEXT v6 publicado (cabeçalho atualizado + §6 T-FUZZY/T-CONCAT)
- GLOSSARIO v6 publicado (cabeçalho + §4 + §5.V11 consolidada + §6 warnings V11 consolidados)
- D-054 promovida de Provisória a Fechada
- Retroação diferida: bloco "Relação com V11" em §2 do DCV-V1 (tarefa registrada)

**Referência canônica:** `/specs/dcv/dcv_v11.md` · D-051 · D-052 · D-053 · D-054 · D-055 · D-056 · D-057

---

### D-057 — Fronteira V11 × Módulo 2 (T-12): higiene textual encapsulada em T-FUZZY; NORMALIZE fora de V11 MVP
**Data:** 2026-04-19 · **Bloco:** DCV-V11 (sessão 2 de 2) · **Status:** Fechada

**Contexto:** T-12 do prévio mapeou 3 cenários V11↔M2: RESHAPE (herdado de V1, exclusão estrutural mantida), CONCAT (resolvido em D-053 · T-CONCAT candidato) e NORMALIZE (transformações textuais). Refino T-12 resolveu NORMALIZE aplicando lente C.5 à distinção entre higiene processual (como o algoritmo lê) e transformação semântica (decisão analítica sobre o conteúdo).

**Decisão:** Higiene textual básica (lowercase · remoção de acentos · remoção de caracteres não-alfanuméricos exceto espaço) **encapsulada em T-FUZZY**, aplicada invisivelmente antes do cálculo de similaridade, registrada no Diagnóstico em linha informativa única (não configurável). Transformações semânticas (unificação de abreviações declaradas, remoção de stop-words customizadas, substituição por regex, truncamento de campo) ficam **fora do escopo V11 MVP**, reservadas para operação candidata **M2.NORMALIZE** do Módulo 2 futuro. Microcopy no Diagnóstico (Seção 6) sinaliza M2.NORMALIZE como opção futura **condicional a alta incidência de "Pareamento frágil"** indicando padronização textual inconsistente — não preventivo na configuração. RESHAPE permanece exclusão herdada de V1.

**Razão:** (1) Distinção é o limite exato que C.5 desenha: higiene processual não é decisão analítica (lowercase não muda significado, só muda "como o algoritmo lê"), logo pode ser encapsulada como comportamento invisível e obrigatório; transformação semântica altera conteúdo (abreviações viram expansões, tokens viram outros tokens), logo é decisão do analista e pertence a operação declarada. (2) Encapsular higiene em T-FUZZY garante comportamento idêntico em V11 e V1-futuro (P-V1-02-Evo) sem reexposição como configuração. (3) Opção descartada "higiene configurável com checkbox" é falso respeito a C.5 — usuário que desligaria está se tirando do tiro; default "ligado" essencialmente reproduz comportamento encapsulado com overhead de UI. (4) Microcopy condicional (só quando Diagnóstico mostra alta incidência de Pareamento frágil) evita poluir configuração com opção que quase nunca é acionada.

**Impacto:**
- T-FUZZY (D-052) recebe especificação explícita da normalização interna no DCV-V11 §4.4 e §5.V11 · GLOSSARIO §4 · CONTEXT §6
- `/specs/dcv/dcv_v11.md` §9 documenta quadro único V11↔M2 (RESHAPE · CONCAT · NORMALIZE)
- GLOSSARIO §5.V11 ganha entrada "Higiene textual vs NORMALIZE" cristalizando a distinção
- G-FUND recebe requisito: T-FUZZY implementa normalização interna com 3 passos fixos (lowercase · acentos · não-alfanuméricos); especificação de M2.NORMALIZE fica para quando M2 for construído (herdará decisão)
- Sem novos warnings específicos (comportamento encapsulado não gera warning próprio; Diagnóstico registra em linha informativa)

**Referência canônica:** `/specs/dcv/dcv_v11.md` §4.4, §9 · GLOSSARIO §4 T-FUZZY · GLOSSARIO §5.V11 "Higiene textual vs NORMALIZE" · D-052

---

### D-056 — Ponte de Conciliação da V11 (T-10): aba autônoma condicional + bloco síntese no Resumo Executivo
**Data:** 2026-04-19 · **Bloco:** DCV-V11 (sessão 2 de 2) · **Status:** Fechada

**Contexto:** T-10 do prévio tratava a Ponte como "opcional", reconhecendo que em V11 a reconciliação de saldo é estrutura diferente da de V1 (complementar, não critério de fechamento), e que exige input adicional do usuário (saldos declarados). Refino T-10 resolveu 4 sub-decisões: (a) aba ou bloco, (b) condição de aparição, (c) microcopy, (d) posicionamento dos campos de saldo na configuração.

**Decisão:** Ponte da V11 implementada como **aba autônoma "Ponte de Conciliação"** (herança estrutural de V1 §6.6) **condicional à declaração dos 4 campos de saldo** (saldo anterior Origem/Comparado + saldo final Origem/Comparado), **com bloco síntese de 3-4 linhas no Resumo Executivo** (Seção 5B) espelhando compacto da aba. Quando saldos não declarados: aba omitida, bloco omitido, Diagnóstico registra "Ponte de Conciliação não incluída — saldos não declarados na configuração" (sem conotação de dado faltando). Microcopy declarativa sem referência a V1. 4 campos numéricos digitados em etapa opcional "Reconciliação de saldo" ao final da configuração (após mapeamento · composição · tolerância · score). Referência a coluna de saldo fica como **P-V11-04-Evo**. Estrutura em 3 blocos herdada do caso-referência Protheus × Safra: Diferença de saldo anterior · Impacto líquido dos movimentos únicos · Conferência (precisa zerar). Novo warning **W-V11-PONTE-RESIDUO** dispara se Bloco 3 não zera.

**Razão:** (1) Aba autônoma + síntese no Resumo Executivo (Opção C) preserva coerência estrutural com V1 (em V1 Ponte é aba 5; em V11 continua aba separada mas condicional) sem engolir o Resumo Executivo com detalhe completo da reconciliação. Impressão/compartilhamento isolado da Ponte fica viável. (2) Condição de aparição por declaração dos saldos (Opção B, sem checkbox explícito) aplica C.5: o ato de declarar **é** o sinal de intenção; checkbox adicional é redundância UX; placeholder quando vazio sugere dado ausente quando foi escolha legítima. (3) Microcopy declarativa sem menção a V1 (Opção B) é coerente com D-054 resumo T-01 (vocabulário declarativo não-negativo, sem redirecionamento algorítmico entre visões). (4) 4 campos digitados (Opção C) no MVP em vez de referência a coluna evita complexidade desproporcional (como definir "primeiro" valor da coluna? por data? por ordem de linha?); roadmap P-V11-04-Evo preserva caminho futuro. (5) Estrutura em 3 blocos herdada do caso-referência Protheus × Safra é gabarito matemático validado — reinventar estrutura seria invenção de comportamento (C.3).

**Impacto:**
- `/specs/dcv/dcv_v11.md` §4.6 especifica etapa opcional de Reconciliação de saldo · §6.2 Seção 5B síntese no Resumo · §6.6 aba Ponte completa
- GLOSSARIO §5.V11 ganha entrada "Ponte de Conciliação V11" distinguindo de Ponte V1
- Novo warning W-V11-PONTE-RESIDUO registrado no GLOSSARIO §6 Warnings V11
- Roadmap V11 ganha P-V11-04-Evo (referência a coluna de saldo)
- F-EXP (Fase 1) recebe requisito: exportação V11 emite aba Ponte condicionalmente baseado em flag `ponte_incluida` do resultado
- Fase 2 (S-V11): wireframe funcional precisa desenhar etapa opcional "Reconciliação de saldo" + apresentar aba Ponte condicional na tela

**Referência canônica:** `/specs/dcv/dcv_v11.md` §4.6, §6.2 Seção 5B, §6.6 · GLOSSARIO §5.V11 "Ponte de Conciliação V11" · GLOSSARIO §6 W-V11-PONTE-RESIDUO

---

### D-055 — Estrutura de abas do Excel da V11 (T-09): 6 abas canônicas, Pareamentos única com todas as colunas, Sem par em dois blocos
**Data:** 2026-04-19 · **Bloco:** DCV-V11 (sessão 2 de 2) · **Status:** Fechada

**Contexto:** T-09 do prévio propunha 6-7 abas candidatas com 4 sub-decisões abertas. Sessão 1 (D-051, T-08 em D-054 resumo) já cristalizou a perspectiva de produto: aba única "Pareamentos" com filtros por categoria + aba "Sem par" separada + KPI decomposto sem síntese imposta. T-09 da sessão 2 traduziu essa perspectiva em estrutura detalhada de abas, colunas e ordem canônica.

**Decisão:** Excel exportado da V11 em **6 abas canônicas** (5 quando sem agrupadores executivos; 4 quando também sem Ponte): (1) Resumo Executivo · (2) Resumo por Agrupador (condicional, se configurado) · (3) Pareamentos · (4) Sem par · (5) Ponte de Conciliação (condicional, se saldos declarados — ver D-056) · (6) Diagnóstico. Diagnóstico sempre última (regra D-017). Aba "Pareamentos" **única com todas as colunas originais das duas bases** (prefixos `[Origem]` e `[Comparado]` para desambiguar colisões + separador visual + novo warning **W-V11-PAREAMENTO-LARGO** quando Excel >50 colunas). Ordem canônica de linhas: por categoria (Conciliado → Divergência de valor → Conciliado por valor → Pareamento frágil), dentro de cada categoria por score decrescente, empate por T-RANK (linha original crescente). Aba "Sem par" em **dois blocos verticais** espelhando caso-referência Protheus × Safra: Bloco 1 "Registros de [Origem] sem par em [Comparado]" + Bloco 2 "Registros de [Comparado] sem par em [Origem]", cada bloco com cabeçalhos próprios e ordem original da aba-fonte.

**Razão:** (1) Opção "Pareamentos única com todas as colunas" (em vez de split Pareamentos × Candidatos ou duplicar "Análise Analítica" estilo V1 §6.5) é tradução estrutural direta de D-051 + T-08: a taxonomia de 5 categorias **é** o achado analítico, não estrutura escondida; analista filtra no Excel para recortar por categoria. Preservar todas as colunas originais é C.5 aplicado: sistema não decide o que é "colateral" para o analista; o custo de largura é compensado pelo warning informativo sugerindo configuração de subset na próxima execução (default persiste em "todas"). (2) Ordem canônica por categoria (em vez de por score global ou por ordem original) transforma a leitura da aba em "aqui o esperado, aqui o estruturalmente diferente, aqui o que precisa revisão" — a taxonomia vira eixo de navegação. (3) Aba "Sem par" separada em dois blocos verticais herda estrutura validada do caso-referência Protheus × Safra — analistas de conciliação reconhecem o formato. Unificar em aba única com coluna "Lado" discriminadora seria mais compacto mas quebra reconhecimento do padrão. (4) Resumo por Agrupador e Ponte condicionais (só aparecem quando configurados) aplicam C.5: presença é sinal de configuração do usuário; ausência não é "falta" nem placeholder.

**Impacto:**
- `/specs/dcv/dcv_v11.md` §6 especifica estrutura de 6 abas canônicas com ordem, colunas e ordenação
- GLOSSARIO §5.V11 ganha entrada "Taxonomia de 5 categorias" (já referenciada em D-051) cristalizando que a taxonomia estrutura a aba Pareamentos
- Novo warning W-V11-PAREAMENTO-LARGO registrado no GLOSSARIO §6 Warnings V11
- F-EXP (Fase 1) recebe requisito: exportação V11 emite 4-6 abas condicionalmente; ordem canônica de linhas por categoria é lógica V11-específica (não encapsulada em transversal, pois depende da taxonomia V11 que não existe em outras visões)
- Fase 2 (S-V11): wireframe funcional desenha preview da estrutura de abas; validação visual confere contra gabarito Protheus × Safra

**Referência canônica:** `/specs/dcv/dcv_v11.md` §6.1 a §6.5 · GLOSSARIO §5.V11 "Taxonomia de 5 categorias" · GLOSSARIO §6 W-V11-PAREAMENTO-LARGO

### D-054 — DCV-V11 sessão 1 · 9 de 13 pendências fechadas · sessão 2 agendada para Bloco C + kit
**Data:** 2026-04-19 · **Bloco:** DCV-V11 (sessão 1 de 2) · **Status:** Provisória (consolida quando sessão 2 encerrar com DCV aprovado)

**Contexto:** Sessão 1 do DCV-V11 (19/04/2026) executou o refino do DCV prévio da V11 (produzido em D-047). Padrão D-019 + D-034 aplicado. Fila de 12 temas do prévio (D-049) ampliada para 13 após T-00 emergir como pendência estruturante no próprio refino (não existia no prévio). Densidade prevista como alta confirmou-se; Cenário 3 adotado no 2º status-check — fechar coração técnico (Bloco B integral) nesta sessão e deixar Bloco C + kit completo para sessão 2.

**Decisão:** Sessão 1 fecha 9 de 13 pendências (Bloco A integral + Bloco B integral). Encerramento em modo parcial — **não produz kit de encerramento padrão D-033 nem DCV refinado final**. Apenas DECISIONS.md recebe atualização nesta sessão (esta entrada + D-051, D-052, D-053). Sessão 2 executará Bloco C (T-09, T-10, T-12), produzirá DCV refinado final em prosa, e entregará kit D-033 completo (CONTEXT v6, GLOSSARIO regenerado, planilha, D-XXX remanescentes, prompt da sessão seguinte). DCV final da sessão 2 é submetido à aprovação da Usuária.

**9 pendências fechadas na sessão 1:**

| Tema | Resolução |
|---|---|
| T-00 Arquitetura de passes (nova em refino) | Opção A · Dois passes sequenciais canônicos em ordem fixa texto→valor. Taxonomia de 5 categorias: Pleno · Divergência de valor · Por valor com texto complementar · Por valor sem evidência textual · Divergência pura. Detalhamento em D-051 |
| T-05 Tolerância de valor | Herança direta de P-V1-05 (absoluta, default zero, por campo de valor) · parâmetro único com papel duplo declarado em microcopy (classifica no Passe 1, filtra no Passe 2) · microcopy com sugestão contextual visível (0,00 contábil · 0,50-2,00 bancário) · W-V11-TOL material |
| T-02 Nomeação default dos lados | Opção C · Defaults "Origem"/"Comparado" (herança V1) + microcopy de configuração que nomeia direção texto→valor. Nomes editáveis; propagam a todos artefatos |
| T-01 Fronteira V1/V11 navegável | Opção B + A1/B1 · Microcopy V11 autossuficiente + bloco "Relação com V1" curto no Objetivo da Visão · nenhuma visão sugere a outra (sem redirecionamento algorítmico) · vocabulário declarativo não-negativo. **Retroação diferida:** DCV-V1 precisa receber bloco "Relação com V11" equivalente quando revisitado ou na S-V1 |
| T-03 Mapeamento semântico de valor | Uma declaração de critério + N campos de valor como leitura opcional · ponto-a-ponto (regra dualidade fica P-V11-XX-Evo) · inferência via default declarado com heurística (nomes de coluna + distribuição de sinais) · declaração estruturada assimétrica (4 combinações: Dual×Dual, Dual×Único, Único×Dual, Único×Único) · polaridade por correspondência · W-V11-MAP-INFERIDO |
| T-04 Composição de campos contextuais | Nativa no MVP com código estruturado para extração futura como transversal de Fundação **T-CONCAT** (candidato, ver D-053) · 5 campos contextuais no MVP · até 3 campos por composição · separador espaço fixo visível no preview · assimetria permitida · nulos pulados (composição se reduz) · W-V11-COMP-CAMPOS-NULOS e W-V11-SEM-CONTEXTO |
| T-06+T-11 Algoritmo de score + T-FUZZY | Algoritmo híbrido trigramas + tokens-chave · scores parciais por campo, média ponderada · pesos internos do algoritmo fixos (encapsulados em T-FUZZY) · pesos entre campos default declarado editável (heurística de distintividade) · limiar Passe 1 default 0,70 editável · limiar Passe 2 default 0,30 editável independente · **T-FUZZY confirmado como transversal da Fundação** (ver D-052) · W-V11-PESOS-CUSTOM, W-V11-LIMIAR-P1-CUSTOM, W-V11-LIMIAR-P2-CUSTOM |
| T-07 Estratégia de alocação | Guloso com ordem por "melhor score disponível" nos dois passes · pré-cálculo da matriz de scores seguido de alocação gulosa · empate resolvido por T-RANK D-041 · W-V11-ALLOC-EMPATE · global ótimo como P-V11-XX-Evo |
| T-08 Classificação + taxonomia de produto | Nomenclatura de produto: Conciliado · Divergência de valor · Conciliado por valor · Pareamento frágil · Sem par · KPI decomposto (taxa global de pareamento + taxas por categoria, sem síntese imposta) · filtros ativos em aba única "Pareamentos" + aba "Sem par" separada · 12 warnings catalogados (W-V11-DIV-VALOR, W-V11-FRAGIL, W-V11-SCORE-LIMITE janela ±0,05, W-V11-VALOR-REPETIDO-MASS 30%, W-V11-SEM-CONTEXTO <2 campos + os anteriores) |

**4 pendências remanescentes para sessão 2:**
- T-09 · Estrutura de abas do Excel (detalhamento de colunas, cabeçalhos, ordem)
- T-10 · Ponte de Conciliação opcional (aba ou bloco, condicional, microcopy)
- T-12 · Fronteira com Módulo 2 (NORMALIZE; CONCAT já parcialmente absorvido em T-04)

**Razão:** (1) Preservação integral das 9 decisões na única fonte canônica estável disponível antes do fim da sessão (DECISIONS.md), garantindo que sessão 2 abra com estado reconstruído via leitura normal do ritual de abertura. (2) Kit completo adiado para sessão 2 evita fragmentação — CONTEXT, GLOSSARIO e DCV refinado merecem ser produzidos juntos quando todas as 13 decisões estão consolidadas, para eliminar risco de divergência sutil de vocabulário entre GLOSSARIO produzido antes do DCV em prosa. (3) DCV parcial como artefato foi descartado — violaria princípio de DCV como artefato terminado e aprovado.

**Impacto:**
- DECISIONS.md recebe entradas D-051, D-052, D-053 e esta (D-054) nesta sessão
- CONTEXT.md, GLOSSARIO.md, planilha e dcv_v11.md ficam inalterados até kit da sessão 2
- CONTEXT §6 e GLOSSARIO §4 continuam registrando T-FUZZY como "🆕 candidato" até kit da sessão 2; hierarquia de fontes de verdade (CONTEXT §5) resolve: DECISIONS.md carrega informação mais recente quando há transição de estado
- Próxima sessão abre com prompt explicitando modo parcial da sessão 1 e escopo da sessão 2
- Retroação registrada para execução futura: bloco "Relação com V11" no DCV-V1

**Referência canônica:** esta entrada · D-051 (T-00) · D-052 (T-FUZZY) · D-053 (T-CONCAT) · DCV prévio V11 · DCV-V11 finalizado entregue na sessão 2

---

### D-053 — T-CONCAT registrado como candidato a transversal da Fundação (composição de campos)
**Data:** 2026-04-19 · **Bloco:** DCV-V11 (sessão 1 de 2) · **Status:** Provisória (confirmação no G-FUND)

**Contexto:** Refino T-04 (composição de campos contextuais) na sessão 1 do DCV-V11 identificou que a operação de composição/concatenação de múltiplos campos-fonte em um campo contextual único é capability que (a) V11 precisa nativamente no MVP — operação central do cenário Protheus × Safra onde `HISTORICO` contábil corresponde a `OPERACAO + DOCUMENTO` financeiro; (b) Módulo 2 · TabloPrep terá como operação independente (CONCAT) quando for construído. Duas rotas: duplicação de lógica (V11 implementa local, M2.CONCAT reimplementa depois) ou extração em transversal compartilhado. Refino escolheu extração.

**Decisão:** T-CONCAT entra na lista de transversais do CONTEXT §6 (a ser atualizado no kit da sessão 2) com marcação "🆕 candidato". Paralelo a T-FUZZY pré-D-050 no enquadramento metodológico, com diferença: T-FUZZY nasceu candidato aguardando confirmação no refino DCV-V11 (confirmado em D-052); T-CONCAT nasce candidato aguardando decisão arquitetural no G-FUND (posicionamento como transversal puro, parte de M2, ou operação compartilhada). Consumo V11 no MVP opera sobre a mesma implementação que eventualmente virará M2.CONCAT — zero duplicação.

**Razão:** (1) Composição é operação de preparação conceitualmente, mas V11 não pode esperar M2 existir para funcionar (cenário Protheus × Safra é o caso-referência que motivou a V11). (2) Implementar nativo e depois reimplementar em M2 geraria duplicação arquitetural — padrão que D-050 (T-FUZZY) justamente evitou para V1↔V11. (3) Marcar como candidato preserva a decisão definitiva para o G-FUND, onde o posicionamento na arquitetura geral (transversal da Fundação, M2 adiantado, ou capability compartilhada) será decidido com visão consolidada dos 11 DCVs.

**Impacto (todos para o kit da sessão 2):**
- CONTEXT §6 ganha linha T-CONCAT com marcação "🆕 candidato" e nota sobre posicionamento a decidir no G-FUND
- GLOSSARIO §4 ganha entrada T-CONCAT candidato com dimensões (campos-fonte, separador, tratamento de nulos) conforme decidido em T-04
- G-FUND recebe tema "posicionamento de T-CONCAT: transversal puro · parte de M2 · capability compartilhada"

**Referência canônica:** D-054 · CONTEXT §6 (pós-kit sessão 2) · GLOSSARIO §4 (pós-kit sessão 2) · dcv_v11.md §8 (pós-kit sessão 2)

---

### D-052 — T-FUZZY confirmado como transversal da Fundação (promove D-050)
**Data:** 2026-04-19 · **Bloco:** DCV-V11 (sessão 1 de 2) · **Status:** Fechada

**Contexto:** D-050 (19/04/2026, sessão de abertura V11) registrou T-FUZZY como transversal **candidato** da Fundação, com confirmação definitiva condicionada ao refino DCV-V11 (temas T-06 algoritmo de score e T-11 escopo arquitetural). Refino executado na sessão 1 do DCV-V11 fechou todas as dimensões técnicas necessárias para confirmação: algoritmo híbrido trigramas + tokens-chave (Sub-decisão T-06.1), pesos internos fixos encapsulados (T-06.3 nível A), API definida `(texto_A, texto_B) → score ∈ [0,1]`, normalização interna encapsulada, determinismo absoluto (C.1).

**Decisão:** T-FUZZY **confirmado** como transversal da Fundação. D-050 (status Provisória) é promovido para Fechada via esta entrada. Marcação "🆕 candidato" em CONTEXT §6 e GLOSSARIO §4 será removida no kit da sessão 2 (T-FUZZY passa a aparecer como transversal regular).

**Dimensões confirmadas do T-FUZZY:**
- **Algoritmo:** híbrido (similaridade por trigramas de caracteres + presença de tokens-chave — sequências numéricas ≥ 4 dígitos e sequências alfabéticas maiúsculas ≥ 3 caracteres consecutivos)
- **Pesos internos:** fixos, calibrados na implementação, não expostos ao usuário (complexidade encapsulada na transversal)
- **Normalização prévia:** lowercase + remoção de caracteres especiais mantendo alfanuméricos e espaço
- **API:** função pura `(texto_A, texto_B) → score ∈ [0,1]`, determinística
- **Consumo V11 (MVP):** aplicado por par de campos contextuais (scores parciais agregados com média ponderada em V11)
- **Consumo V1 (P-V1-02-Evo):** disponível quando match fuzzy for ativado em V1; zero retrabalho

**Razão:** (1) O algoritmo híbrido definido em T-06 tem complexidade suficiente para merecer encapsulamento — implementar localmente em V11 (e depois em V1) duplicaria a calibração do peso trigramas × tokens-chave, com risco arquitetural de divergência sutil. (2) Reúso previsto em V1 justifica posicionamento na Fundação em vez de módulo V11-local. (3) Determinismo e auditabilidade são preservados pela API pura sem estado.

**Impacto (todos para o kit da sessão 2):**
- CONTEXT §6: linha T-FUZZY perde marcação "🆕 candidato" e ganha status regular; coluna "Usado por" confirma "V11 (MVP) · V1 (P-V1-02-Evo)"
- GLOSSARIO §4: entrada T-FUZZY perde marcação provisória; dimensões consolidadas no texto
- G-FUND: T-FUZZY entra no escopo de implementação como transversal da Fundação com contrato especificado
- D-050 marcado como "Promovida a Fechada por D-052"

**Referência canônica:** D-050 (contexto) · D-051 (arquitetura de passes que define papel do score) · D-054 · CONTEXT §6 (pós-kit sessão 2) · GLOSSARIO §4 (pós-kit sessão 2)

---

### D-051 — V11 adota arquitetura de dois passes texto→valor como contrato analítico canônico
**Data:** 2026-04-19 · **Bloco:** DCV-V11 (sessão 1 de 2) · **Status:** Fechada

**Contexto:** DCV prévio V11 (D-047, produzido pelo Arquiteto na sessão de abertura) tratava valor como elo primário rígido: só entra candidato se valor bate (dentro da tolerância), score textual ranqueava entre candidatos de mesmo valor. No refino da sessão 1 do DCV-V11, a Usuária identificou que esse enquadramento exclui um caso analítico crítico do mundo real da conciliação contábil: registro do financeiro com histórico/documento/data que bate perfeitamente com registro do contábil, **mas valor diferente**. Ex.: baixa feita errada, imposto não calculado na hora da baixa, rateio contábil que separou valor único do financeiro em N lançamentos de valores distintos. A divergência de valor **é exatamente o achado analítico**. Excluir esse par violaria o propósito da visão. Frequência do caso no cenário real ("muita frequência, muita frequência") e peso do cenário contábil na V11 (caso-referência Protheus × Safra) elevaram o tema a pré-requisito da visão, não evolução.

**Decisão:** V11 opera com **dois passes sequenciais obrigatórios na ordem fixa texto→valor** como contrato analítico canônico do MVP. Arquitetura deixa de ser "valor como elo primário" e passa a ser "texto identifica o fato; valor verifica a consistência do fato".

**Arquitetura de passes:**

**Passe 1 · Elo por aderência textual (primário).** Motor parte dos campos contextuais. Para cada registro da Origem, busca na Comparado registros com score textual acima do limiar de entrada (default 0,70). Quando encontra match, confronta valor:
- Diferença ≤ tolerância → **Pareamento Pleno** (apresentado como "Conciliado" na UI)
- Diferença > tolerância → **Pareamento com divergência de valor** (apresentado como "Divergência de valor" na UI — achado analítico central da visão)

**Passe 2 · Elo por valor (secundário, sobre o que sobrou).** Sobre registros sem par no Passe 1, motor busca por valor (dentro da tolerância). Quando encontra, classifica por aderência textual do candidato:
- Score textual ≥ limiar Passe 2 (default 0,30) → **Pareamento por valor com texto complementar** (apresentado como "Conciliado por valor")
- Score textual < limiar Passe 2 → **Pareamento por valor sem evidência textual** (apresentado como "Pareamento frágil")

**Passe 3 · O que sobra vira divergência pura** (apresentado como "Sem par"). Pode ser "Só em Origem" ou "Só em Comparado".

**Taxonomia oficial da V11:**

| Categoria técnica | Nome de produto | Passe | Condição |
|---|---|---|---|
| 1. Pleno | Conciliado | 1 | texto score ≥ 0,70 + valor dentro de tolerância |
| 2. Divergência de valor | Divergência de valor | 1 | texto score ≥ 0,70 + valor fora de tolerância |
| 3. Por valor com texto complementar | Conciliado por valor | 2 | valor dentro de tolerância + texto score ≥ 0,30 |
| 4. Por valor sem evidência textual | Pareamento frágil | 2 | valor dentro de tolerância + texto score < 0,30 |
| 5. Divergência pura | Sem par | — | sem par nos dois passes |

**Visibilidade ao usuário (C.5):** ordem dos passes declarada na configuração da V11 com microcopy explicativa; Diagnóstico registra contagem por passe; KPI do Resumo Executivo decomposto por categoria (taxa global de pareamento + taxas por categoria — sem síntese imposta).

**Razão:** (1) A arquitetura de dois passes texto→valor espelha o fluxo mental do auditor humano na conciliação contábil real: reconhece o fato pelo texto (histórico, documento, referências) e confere o valor como dado do resultado. (2) Cobre o cenário Protheus × Safra que motivou a formalização da V11. (3) Determinismo e auditabilidade máximos — ordem canônica fixa permite ao usuário reconstruir o processo do motor ("Passe 1 achou texto bom, Passe 2 rodou nos que sobraram"). (4) Alternativas consideradas e rejeitadas: ordem configurável (prematura no MVP), execução paralela com prioridade (violaria C.1 por auditabilidade baixa), manter como no prévio (excluiria o caso-referência real). (5) Taxonomia de 5 categorias emerge naturalmente da arquitetura — cada categoria tem leitura analítica própria, não é complexidade gratuita.

**Impacto:**
- Reescreve enquadramento de T-03 (mapeamento semântico deixa de ser "elo primário" e passa a ser "confronto de valor pós-identificação textual"); T-05 (tolerância com papel duplo estruturalmente confirmado); T-06 (score com dois limiares independentes); T-08 (taxonomia de 5 categorias); T-09 (estrutura de abas do Excel reflete categorias — sessão 2)
- DCV prévio (D-047) deixa de ser espinha dorsal única do refino — T-00 entra como pendência estruturante anterior às demais
- Dimensões do T-FUZZY ficam definidas pela arquitetura de passes (D-052 consolida)
- CONTEXT §4 (Família A) pode ganhar nota sobre a diferença arquitetural V1/V11 (V1: determinístico por chave; V11: dois passes com score — kit sessão 2)
- Warning W-V11-SCORE-LIMITE registra casos de fronteira em qualquer dos dois limiares (janela ±0,05)

**Referência canônica:** esta entrada · D-054 (sumário da sessão 1) · dcv_v11.md §5 Pipeline (pós-kit sessão 2) · dcv_v11.md §6 Saída (pós-kit sessão 2)

### D-050 — T-FUZZY registrado como transversal candidato da Fundação (aguarda refino DCV-V11)
**Data:** 2026-04-19 · **Bloco:** Revisão de Escopo V1 / Abertura V11 · **Status:** Provisória (confirmação no refino DCV-V11)

**Contexto:** V11 · Conciliação por Aderência (D-047) exige similaridade textual entre strings para calcular score de aderência contextual — é o parâmetro analítico central da visão. V1 tem match fuzzy registrado no roadmap como **P-V1-02-Evo** (implementação via transversal T-FUZZY quando houver pedido real). V11 pré-data essa evolução: ela **precisa** de similaridade textual para existir no MVP. Duas opções: (a) criar T-FUZZY na Fundação agora, antecipando P-V1-02-Evo, com consumo V11 no MVP e disponibilização V1 quando a evolução for ativada; (b) V11 implementa localmente, T-FUZZY futuro absorve via extração. Opção (a) elimina retrabalho e coerência arquitetural.

**Decisão:** T-FUZZY entra na lista de transversais do CONTEXT §6 com marcação "🆕 candidato". Criação definitiva aguarda confirmação no refino DCV-V11 (temas T-06 e T-11 do prévio). Dimensões a decidir no refino: algoritmo (Jaccard/Levenshtein/substring/híbrido), score único vs composto, pesos fixos vs editáveis, faixas de classificação.

**Razão:** (1) Registrar como candidato no CONTEXT §6 evita esquecimento mas preserva a autoridade do refino DCV-V11 sobre dimensões técnicas do componente. (2) Coerente com o padrão "default declarado" (família D-024): componente declarado antes da execução; dimensões configuráveis emergem do refino. (3) Se confirmado, unifica a implementação para V1 e V11 na Fundação — evita risco arquitetural de divergência sutil que a família de view especializada D-035 justamente evita.

**Impacto:**
- CONTEXT §6 ganha linha T-FUZZY com marcação `🆕 candidato` e coluna "Usado por: V11 (MVP) · V1 (roadmap P-V1-02-Evo)"
- GLOSSARIO §4 ganha entrada T-FUZZY candidato com dimensões a decidir
- Refino DCV-V11 (próxima sessão) tem T-FUZZY como tema de decisão explícita (temas T-06 e T-11 do prévio)
- Eventual descarte ou reescopo sai do refino como nova decisão D-XXX revogando esta

**Referência canônica:** CONTEXT §6 · GLOSSARIO §4 · DCV prévio V11 seções T-06, T-11, §8

---

### D-049 — Mapa estrutural preliminar da V11 (12 temas para o refino DCV-V11)
**Data:** 2026-04-19 · **Bloco:** Revisão de Escopo V1 / Abertura V11 · **Status:** Fechada

**Contexto:** Com V11 formalmente no escopo (D-047) e ordem Fase 0 definida (D-048), a sessão de abertura de escopo mapeou os temas estruturais que o refino DCV-V11 terá que trabalhar. Mapa produzido antes do DCV prévio formal, serve como espinha dorsal do prévio e antecipa a fila racionalizada que o refino (padrão D-019) usará.

**Decisão:** 12 temas estruturais registrados como roteiro do DCV prévio V11 e fila preliminar do refino DCV-V11. Organização em 3 blocos (fronteira com V1 · arquitetura do match · arquitetura do resultado). Cada tema classificado por natureza de herança (forte V1 · parcial · V11-original).

**12 temas:**

| # | Tema | Natureza | Herança |
|---|---|---|---|
| T-01 | Fronteira V1/V11 navegável (microcopy, redirecionamento) | Produto | V11-original |
| T-02 | Nomeação default dos lados da entrada (Origem/Comparado ou alternativa) | Produto | Forte V1 |
| T-03 | Contrato de mapeamento semântico de valor | Motor (central) | V11-original |
| T-04 | Composição de campos contextuais (concatenação declarada) | Configuração | V11-original |
| T-05 | Tolerância de valor | Configuração | Forte V1 (P-V1-05) |
| T-06 | Algoritmo de score e faixas de confiança | Motor (central) | V11-original |
| T-07 | Estratégia de alocação (guloso × global ótimo) | Motor | V11-original |
| T-08 | Classificação sem evidência contextual | Contrato de saída | V11-original |
| T-09 | Estrutura de abas do Excel (Candidatos vs Divergências) | Produto | Parcial V1 |
| T-10 | Ponte de Conciliação opcional | Produto | Parcial V1 |
| T-11 | T-FUZZY como transversal da Fundação | Arquitetura transversal | V11-original |
| T-12 | Fronteira com Módulo 2 (CONCAT, NORMALIZE) | Arquitetura | Parcial V1 |

**Razão:** (1) Mapa cristalizado a partir do diálogo real da Usuária na sessão — captura fronteiras, decisões estruturais, casos-limite e o cenário real Protheus × Safra que serviu de gabarito. (2) Organização em blocos facilita priorização no refino (T-01 a T-03 são pré-requisito dos demais; T-06 é "coração técnico" que vira conhecido pelos anteriores). (3) Classificação por herança permite ao refino acelerar os temas forte/parcial e concentrar orçamento de kit nos V11-originais. (4) Densidade esperada alta, comparável à V4 (primeira visão da Família C) — 10 pendências estruturais acumuladas (12 menos 2 de herança forte imediata).

**Impacto:**
- DCV prévio V11 (`DCV_PREVIO_M1_V11.md`) estrutura suas seções conforme o mapa
- Refino DCV-V11 (próxima sessão) abre a fila respeitando a ordem do mapa (T-01 a T-12), com negociação da ordem no próprio refino se necessário
- Se a densidade prevista se confirmar alta no 3º status-check (D-034), recomendação de separar kit será ativada

**Referência canônica:** DCV prévio V11 §12 · mapa nesta sessão

---

### D-048 — Ordem de refino da Fase 0 ajustada: V11 antes de V3 (Família A fecha antes de abrir Família B)
**Data:** 2026-04-19 · **Bloco:** Revisão de Escopo V1 / Abertura V11 · **Status:** Fechada

**Contexto:** Com V11 entrando no escopo do Módulo 1 (D-047), a ordem de refino Fase 0 — V1 ✅ → V2 ✅ → V4 ✅ → V10 ✅ → V3 → V8 → V7 → V9 → V5 → V6 — precisou acomodar a nova visão. Três opções: (a) antes de V3 — fecha Família A antes de abrir Família B; (b) por último, depois de V6 — não atrasa Família B; (c) paralelo com V3 — ganha paralelismo mas mistura contextos de família.

**Decisão:** Opção (a) — V11 entra **antes de V3**. Ordem final de refino Fase 0: V1 ✅ → V2 ✅ → V4 ✅ → V10 ✅ → **V11** → V3 → V8 → V7 → V9 → V5 → V6. Ordem de implementação Fase 2 Família A: **V2 → V1 → V11**.

**Razão:** (1) Família A fica fechada antes da mudança de família — padrão coerente com tratamento da V10 (fechou Família C inteira antes de pensar em Família B). (2) V11 compartilha T-DUAL com V1 — trabalhar enquanto V1 ainda está fresco na cabeça é mais eficiente para o refino. (3) Possível retroação sobre V1: ao definir V11, podem emergir ajustes pequenos no DCV-V1 (microcopy que diferencia as duas, redirecionamento entre visões, vocabulário). Ajustes ficam pendentes por menos tempo.

**Impacto:**
- CONTEXT §3 Fase 2 tabela de ordem Família A: V2 → V1 → V11
- Planilha aba 2 (Fase 0 · DCVs): linha V11 posicionada entre V10 e V3
- Planilha aba 4 (Fase 2 · Visões): linha V11 posicionada após V1 na Família A
- G-FUND aguarda 11 DCVs aprovados (não 10)

**Referência canônica:** CONTEXT §3 Fase 2 · CONTEXT §4 · planilha abas 2 e 4

---

### D-047 — V11 · Conciliação por Aderência entra no escopo do Módulo 1 como 11ª visão (Família A)
**Data:** 2026-04-19 · **Bloco:** Revisão de Escopo V1 / Abertura V11 · **Status:** Fechada

**Contexto:** Ao fim da Sessão DCV-V10 (19/04/2026), a Usuária sinalizou tema deixado passar durante DCV-V1 a ser avaliado antes de avançar para Família B: cenário real cotidiano em áreas contábeis e financeiras brasileiras — conciliação entre duas bases **sem chave confiável**, onde o elo primário é valor e a ligação depende de aderência textual (histórico, documento, data). Apresentado caso real Protheus × Safra (1.360 × 1.322 linhas, aba Divergências com 49 registros não-pareados em duas seções, aba Ponte de Conciliação fechando matemática de saldos). Análise conjunta identificou 3 razões estruturais para não tratar como modo de V1: (a) motor diferente — V1 determinístico por chave, V11 probabilístico por score; (b) saída diferente — classificações binárias em V1 × faixas de confiança em V11; (c) UX diferente — chave em V1 × mapeamento semântico + composição contextual em V11. Forçar como modo de V1 geraria frankenstein (metade do motor, contrato e UX ramificados por `if modo`).

**Decisão:** V11 · Conciliação por Aderência entra no escopo do Módulo 1 como 11ª visão, integrando a Família A como visão autônoma (não como view especializada). Nomenclatura: **V11** (inteiro, mantendo padrão V1-V10; parentesco com V1 registrado na Família A, não no número — análogo a V10 que não é "V4.1"). Ordem Família A: V2 → V1 → V11. V1 e V11 compartilham T-DUAL mas operam motores distintos.

**Exceção metodológica (prévio produzido pelo Arquiteto):** nesta sessão excepcional, Arquiteto produziu o DCV prévio V11 em vez do ChatGPT, porque a sessão de abertura de escopo capturou o tema com maior profundidade. A exceção não altera o papel canônico do ChatGPT nos demais DCVs — é caso específico onde o enquadramento emergiu no diálogo Arquiteto × Usuária e preservá-lo em artefato imediato evita perda. Prévio preserva natureza de "prévio" (pendências T-XX abertas, decisões não fechadas — o refino subsequente aplica o padrão D-019 normalmente).

**Razão:** (1) Cenário identificado é real, relevante e estruturalmente distinto da V1 — não cabe como modo, não cabe no Módulo 2. (2) Família A com 3 visões reflete o peso real do confronto no uso contábil brasileiro (V2 estado×estado, V1 bases com chave, V11 bases sem chave). (3) V11 como visão autônoma (não view especializada D-035) porque não é caso particular de V1 — é problema analítico diferente, reaproveita só T-DUAL. (4) Nomenclatura V11 coerente com precedente V10 (Pareto, view especializada de V4) que também não se chamou "V4.1". (5) Exceção do prévio pelo Arquiteto formalizada no CONTEXT §2 e §3 Fase 0 preserva qualidade do artefato sem abrir precedente permissivo.

**Impacto:**
- CONTEXT: §1 (11 visões), §2 (exceção formalizada), §3 Fase 0 (11 DCVs), Fase 2 ordem V2→V1→V11, §4 Família A com 3 visões, §6 T-DUAL estendido, §7 `dcv_v11.md`, §13.4 cláusula "V11 não é view especializada"
- GLOSSARIO: cabeçalho; Família A; T-AGRUPA (V1 e V11 não usam); T-RANK (V11 incluída); T-DUAL (V11 incluída); T-MODELO (11 visões); §5.V11 nova com 4 termos; warnings V11 candidatos
- Instruções do Projeto: 11 visões · ordem Fase 2 · ordem refino Fase 0 · menção à exceção
- Planilha: aba 1 (método em 3 fases reflete 11 DCVs; próximo passo = DCV-V11); aba 2 (linha V11 entre V10 e V3, prévio ✅); aba 4 (linha V11 após V1 Família A)
- Novo artefato: `DCV_PREVIO_M1_V11.md` (entregue como arquivo nesta sessão)
- Decisões conexas: D-048 (ordem), D-049 (mapa estrutural), D-050 (T-FUZZY candidato)

**Referência canônica:** CONTEXT §1, §2, §3, §4, §13.4 · GLOSSARIO §1 (Família), §4 (T-DUAL), §5.V11 · `DCV_PREVIO_M1_V11.md`

### D-046 — Modelos T-MODELO em view especializada: compartilhamento cross-visão com mapeamento declarado (transversal §13.4)
**Data:** 2026-04-19 · **Bloco:** DCV-V10 · **Status:** Fechada

**Contexto:** CONTEXT §13.4 (instituído em D-035) estabeleceu o padrão "view especializada sobre visão-base" para V4 Modo 2 ↔ V10 (Família C) com precedente de V2 ↔ V1 via T-DUAL (Família A). Faltava resolver como T-MODELO (D-030) se comporta entre as duas visões do par: modelo salvo em V4 Modo 2 aplicável em V10? Configurações específicas de cada uma (V4 tem limiar B; V10 tem cardinalidade visual e faixas de leitura V10) como convertem? Decisão precisa ser transversal porque aplicará também a V2 ↔ V1 quando DCV-V1 for executado.

**Decisão:** Modelos são **mutuamente aplicáveis cross-visão** em pares de view especializada, via mapeamento declarado (3 categorias de parâmetros). Aplicação intra-visão transfere tudo direto; aplicação cross-visão dispara diálogo de confirmação.

**Mapeamento de parâmetros:**
- **Transferidos** (comuns às duas visões): medida, agrupadores, regra de agregação, limiar A, tipo de medida, tratamento de negativos, seleção de medida em POR_LINHAS
- **Com default da visão-destino** (específicos da origem sem equivalente): em V10, cardinalidade visual = 50 e faixas de leitura = default; em V4 Modo 2, limiar B = 95
- **Descartados** (específicos da origem não aplicáveis): V10 → V4 Modo 2 descarta cardinalidade visual e faixa de corte; V4 Modo 2 → V10 descarta limiar B

**Casos não aplicáveis:** modelos de V4 Modo 1 ou V4 Modo 3 **não** convertem com V10. A regra é estrita: só pares que são literalmente "view especializada" convertem. Modos irmãos da mesma visão-base (ex: V4 Modo 1 × V4 Modo 2) não formam par.

**Interface:** lista de modelos aplicáveis em cada visão do par exibe os modelos cross-visão com badge discreto identificando a origem. Warning W-{visao}-MODELO-CONVERTIDO (informativa, simétrico) registra aplicação cross-visão com lista de parâmetros defaulted e descartados.

**Razão:** (1) Coerente com D-035 — V10 é view especializada; separar modelos negaria a especialização. (2) Padrão "default declarado" (família D-024) aplica-se naturalmente à aplicação de modelo: diálogo declara tudo, nada silencioso — C.5 honrado. (3) Decisão transversal: resolve agora para V4↔V10 e estabelece precedente reutilizável para V2↔V1 via T-DUAL (Família A) quando DCV-V1 for executado.

**Impacto:**
- CONTEXT §13.4 ganha cláusula "Modelos (T-MODELO) em view especializada" com princípios e contrato
- GLOSSARIO §5.V10 ganha entrada "Modelo cross-visão"
- GLOSSARIO §6 (Warnings V10) cataloga W-V10-MODELO-CONVERTIDO
- T-MODELO (Fundação) precisa expor `visao_origem`, `visoes_aplicaveis` (lista computada), parâmetros categorizados (comuns · específicos origem · específicos destino) — requisito novo para G-FUND
- Aplicabilidade atual: V4 Modo 2 ↔ V10
- Aplicabilidade futura: V2 ↔ V1 via T-DUAL, a confirmar em DCV-V1

**Referência canônica:** CONTEXT §13.4 · DCV-V10 §10.4 · GLOSSARIO §5.V10

---

### D-045 — DCV-V10 refinado: view especializada sobre V4 Modo 2 consolidada (10 pendências)
**Data:** 2026-04-19 · **Bloco:** DCV-V10 · **Status:** Fechada

**Contexto:** DCV prévio da V10 foi produzido antes de D-035 (que formalizou V10 como view especializada sobre V4 Modo 2) e assumia V10 como visão autônoma com motor próprio. Sessão DCV-V10 realinhou o prévio ao novo escopo, consolidando 10 pendências V10-específicas (P-V10-01 a P-V10-10). Como V10 herda integralmente da V4 (D-036 tipos, D-038 nulos/negativos, D-040 limiares, D-041 T-RANK, D-043 bloqueios, D-030 T-MODELO, D-044 Resumo Executivo), sessão foi curta e densidade baixa-média.

**Decisão:** V10 consolidada como view especializada sobre V4 Modo 2 com identidade de produto distinta (entrada simplificada, narrativa Pareto, visualização dedicada). 10 pendências resolvidas com as escolhas a seguir.

**Pendências resolvidas:**

| Pendência | Resolução |
|---|---|
| P-V10-01 Escopo | Opção B · view especializada com identidade de produto (entrada, narrativa, visualização próprias) |
| P-V10-02 Preset de limiares | Opção B · T-ABC 80/95 internamente; UI colapsa B+C em "Demais itens"; só limiar A editável em V10 |
| P-V10-03 Entrada simplificada | Opção B · 4 etapas (fusão E2+E3 de V4 em "Estrutura e medida") |
| P-V10-04 Escopo de medidas | Opção A · exatamente 1 medida; ponte para V4 Modo 3 quando usuária quer multi-medida |
| P-V10-05 Filtro visual Classe A | Opção C · disclosure Vitais/Demais com contagem visível; nada escondido |
| P-V10-06 Visualização Pareto | Curva clássica no topo largura total; cardinalidade 50 configurável em avançadas; tooltip no hover |
| P-V10-07 Microcopy | 6 peças consolidadas com voz descritiva, vocabulário Pareto, pontes explícitas V4 Modo 2/Modo 3/V6 |
| P-V10-08 Resumo Executivo | 6 blocos herdados D-031/D-044 adaptados + leitura secundária "Corte" V10-nova (folgado/apertado/empate) |
| P-V10-09 Exportação Excel | 6 abas: Resumo · Análise · Curva Pareto (com gráfico nativo) · Base · Parâmetros · Diagnóstico |
| P-V10-10 T-MODELO | Compartilhamento cross-visão V4 Modo 2 ↔ V10 → virou transversal de método (D-046) |

**Razão:** (1) D-035 já estabeleceu V10 como view especializada — todas as decisões honram a decisão-mãe. (2) Padrão "default declarado" (família D-024/D-025/D-026/D-036/D-038/D-040) aplicado sistematicamente em V10 (limiar A editável, cardinalidade visual editável, faixas de leitura editáveis, bloco declarado de negativos herdado, bloco declarado de tipo relativo herdado). (3) Disclosure Vitais/Demais em vez de filtro default (P-V10-05) é a leitura mais rigorosa de C.5 entre as opções — nada escondido, contagem sempre visível. (4) Apresentação dicotômica na UI (Classe A × Demais itens) com T-ABC computando A/B/C por baixo é separação limpa entre cálculo (compartilhado com V4) e apresentação (V10-específica) — coerente com view especializada.

**Impacto:**
- `/specs/dcv/dcv_v10.md` criado com DCV completo refinado em prosa
- DCV-V10 aprovação registrada na aba 2 da planilha
- Aba 2 da planilha: V10 refinado ✅, aguardando aprovação da Usuária
- Aba 3 da planilha: T-ABC, T-ACUM, T-RANK, T-MODELO ganham nota sobre uso V10 (já registravam; texto expandido)
- GLOSSARIO ganha §5.V10 com 7 entradas V10 (Vitais, Demais itens, Curva Pareto V10, Limiar A V10, Fronteira, Leitura de Corte, Cardinalidade visual, Modelo cross-visão)
- GLOSSARIO §6 cataloga 5 warnings V10: W-V10-CURVA-TRUNC · W-V10-CORTE-APERTADO · W-V10-CLASSE-A-VAZIA · W-V10-BASE-MINIMA · W-V10-MODELO-CONVERTIDO (este último simétrico também em V4)
- Entrada "Classe ABC" reformulada dando rótulos explícitos à dicotomia V10
- Requisitos novos para G-FUND registrados no DCV-V10 §15: (a) gráfico nativo Pareto no Excel via openpyxl (combo chart + linhas de referência); (b) formatação de separador Vital/Demais na Análise Principal; (c) T-MODELO com mapeamento cross-visão (detalhado em D-046)
- Entrada para Fase 2 · S-V10: wireframe funcional, tipografia, UX do diálogo de modelo cross-visão, tecnologia do gráfico na tela (Plotly ou Altair provavelmente)

**Referência canônica:** `/specs/dcv/dcv_v10.md` (todo o documento)


## Decisões registradas

### D-044 — Resumo Executivo da V4: 6 blocos adaptados por modo + faixas de leitura editáveis
**Data:** 2026-04-19 · **Bloco:** DCV-V4 · **Status:** Fechada

**Contexto:** D-031 (V2) consolidou padrão "Resumo Executivo = 6 blocos fixos" com adaptação por natureza analítica. V4 precisava instanciar o padrão. O prévio V4 (Parte 9.3) descrevia conteúdo genericamente. Também faltava decidir se faixas de síntese (concentrada/equilibrada/pulverizada; coerência alta/média/baixa) do Bloco 5 são fixas ou editáveis.

**Decisão:** Resumo Executivo da V4 mantém estrutura de 6 blocos da D-031, com conteúdo adaptado por modo (1 / 2 / 3). Faixas de leitura de síntese do Bloco 5 são editáveis em "Configurações avançadas" na E5 (recolhida por default).

**6 blocos:**
1. Cabeçalho da análise (constante)
2. Números-âncora (4 KPIs adaptados por modo)
3. Distribuição de classificações estruturais (ausente no Modo 1; A/B/C no Modo 2; Igual/Divergente/Alta divergência/Ausência parcial no Modo 3)
4. Elementos destacados (top 10 por participação / Classe A + fronteira / alta divergência)
5. Leituras descritivas de síntese (concentração Modos 1/2; coerência Modo 3)
6. Qualidade estrutural (resumo do Diagnóstico)

**Faixas editáveis (Bloco 5):**
- Leitura de concentração (Modos 1/2): top 20% > 80% = concentrada · 40%-80% = equilibrada · < 40% = pulverizada
- Leitura de coerência (Modo 3): > 70% Igual = alta · 40%-70% = média · < 40% = baixa
- Microcopy explícito: "Estas faixas afetam apenas a frase de síntese do Bloco 5. Os cálculos principais (participação, classificação ABC, divergência) não são afetados."

W-V4-LEITURA-CUSTOM registra customização.

**Razão:** Leituras descritivas com critério matemático explícito (não opinativo) honram padrão D-031 ("Resumo apresenta fatos, não interpretação"). Edição em "avançado" honra C.5 (default declarado + opção fácil) sem sobrecarregar E5 para uso padrão. Divergência par-a-par (D-042) naturalmente insere-se no Bloco 4 (elementos destacados com alta divergência).

**Impacto:**
- DCV-V4 §9.2 documenta os 6 blocos adaptados
- Spec da V4 (Fase 2) detalha layout, microcopy, UI das configurações avançadas
- F-EXP implementa template Aba 1 com 6 blocos (3 variantes por modo)
- V10 (view especializada) adapta Bloco 5 para narrativa Pareto (fica para DCV-V10)

**Referência canônica:** DCV-V4 §9.2

---

### D-043 — Bloqueios operacionais da V4 + Total Geral=0 adaptativo por causa + herança de diretrizes de performance
**Data:** 2026-04-19 · **Bloco:** DCV-V4 · **Status:** Fechada

**Contexto:** D-032 fechou para V2 oito bloqueios operacionais + sete diretrizes de performance. V4 precisa consolidar quais herda, quais adapta, quais são novos. Tema adicional: Total Geral = 0 quebra matemática de participação (divisão por zero) e o prévio V4 (Parte 11) tratava como "alerta não-bloqueante" — tratamento incompatível com matemática de participação.

**Decisão:** V4 tem **12 bloqueios operacionais** (8 herdados de D-032 com ajustes + 4 V4-específicos novos). Total=0 tem **bloqueio adaptativo por causa** (3 microcopies). **7 diretrizes de performance** de D-032 herdadas integralmente.

**12 bloqueios:**
1. Arquivo ilegível/corrompido (herdado)
2. Estrutura inválida (herdado)
3. Coluna discriminadora POR_LINHAS 0 ou 1 valor único (herdado — W-V4-N0/W-V4-N1)
4. Medida com 100% de nulos (adaptado de "Origem ou Comparado" para "Medida")
5. Mais de 9 agrupadores (herdado via D-027)
6. Média ponderada com pesos todos zerados ou negativos (herdado, aplicável quando opção da P-02/D-036 for escolhida)
7. Falha estrutural não-recuperável na transição E4→E5 (herdado)
8. Análise gera >500.000 linhas (herdado)
9. **Novo:** Total Geral = 0 (W-V4-TOTAL-ZERO)
10. **Novo:** Modo 3 com <2 medidas selecionadas (W-V4-MEDIDAS-MIN)
11. **Novo:** Tipo de medida = Estado/Situação (redireciona para V6)
12. **Novo:** Limiares ABC inválidos (A ≥ B ou fora de 0-100)

**Total=0 — 3 causas identificadas:**
- Base toda nula → "Nenhum registro válido. Verifique a base."
- Cancelamento pos/neg → "Total Geral zero por cancelamento. Separar em positivos e negativos permite analisar cada universo." + link para reexecutar com opção D-038
- Outro → "Total Geral zero. Verifique a base ou o filtro aplicado."

W-V4-TOTAL-ZERO registra causa + sugestão.

**Razão:** Bloqueios operacionais são proteção do sistema, não decisão analítica — C.5 satisfeito quando mensagem explica motivo e sugere caminho. Causa adaptativa no Total=0 transforma "erro" em "próximo passo". Herança integral de diretrizes de performance evita redundância — F-MOT aplica as mesmas diretrizes indistintamente para V2 e V4. Volume de V4 (sem produto cartesiano de estados) raramente aciona limite 500K, mas manter para coerência.

**Impacto:**
- DCV-V4 §10 documenta os 12 bloqueios
- Spec da V4 (Fase 2) detalha mensagens específicas
- F-MOT aplica 7 diretrizes de D-032 sem modificação
- F-EXP (Diagnóstico) registra tempo por etapa (herdado)

**Referência canônica:** DCV-V4 §8.6 e §10

---

### D-042 — Modo 3 da V4: divergência composta + ausência entre medidas + heterogeneidade com default declarado
**Data:** 2026-04-19 · **Bloco:** DCV-V4 · **Status:** Fechada

**Contexto:** Pendência inédita sem precedente em V1/V2. O prévio V4 (Parte 6.4) definia divergência (Igual/Divergente/Alta divergência) como comparação de classe ABC entre duas medidas — regra par-a-par sem tratamento para N≥2 medidas, sem tratamento de ausência entre medidas (elemento existe em uma medida, não em outra), sem tratamento para heterogeneidade de tipos (aditivo + relativo no mesmo Modo 3). Três sub-pendências (9a, 9b, 9c) compartilhando contrato de resultado e exibição.

**Decisão:** Modo 3 adota **divergência composta em dois níveis** + marcador `—` para ausência + default declarado para heterogeneidade de tipos. Medida de referência ganha **3º papel** (eixo de comparação par-a-par).

**9a — Divergência composta:**

Par-a-par contra medida de referência (coluna por medida não-referência):
- Mesma classe → Igual
- 1 nível de diferença → Divergente
- 2 níveis → Alta divergência
- Ref tem classe, outra `—` → Ausente na [nome_medida]
- Ref `—`, outra tem classe → Ausente na medida de referência
- Ambas `—` → Elemento fora do Modo 3

Síntese geral (gap máximo):
- gap = 0 → Igual
- gap = 1 → Divergente
- gap ≥ 2 → Alta divergência
- Algum `—` → Ausência parcial

**9b — Ausência com marcador `—`:**
Elemento sem valor ou valor nulo em uma medida recebe marcador `—` naquela medida (preservado na análise, não excluído). Categorias de divergência adaptadas. W-V4-MD3-AUSENTE contabiliza.

**9c — Heterogeneidade de tipos:**
Motor detecta na E3 após seleção. Bloco declarado com 3 opções: "Entendo, prosseguir" (default) / "Remover medidas incompatíveis" / "Cancelar". W-V4-MD3-HETERO registra escolha.

**Razão:** Divergência composta preserva narrativa par-a-par (A2 pura) E síntese para Resumo Executivo (A1 pura) — cobre usos analíticos distintos sem duplicação de cálculo. Medida de referência já existia no prévio com 2 papéis (ordenação, leitura); promover a eixo de comparação aproveita o conceito. Marcador `—` honra C.5 (preserva fato, não exclui). Heterogeneidade com default declarado aplica padrão cristalizado em D-024/D-025/D-026. Delta de ranking (prévio Parte 6.4) permanece complementar.

**Impacto:**
- DCV-V4 §8.3 documenta as 3 regras
- Contrato MotorResult da V4 ganha `classificacao_divergencia_ref_por_medida` + `classificacao_divergencia_geral`
- 2 warnings novos: W-V4-MD3-AUSENTE, W-V4-MD3-HETERO
- Spec da V4 (Fase 2) detalha UX da medida de referência + bloco de heterogeneidade
- Aba Excel "Comparação de Distribuição" tem colunas: classe por medida + divergência par-a-par + delta ranking + divergência geral

**Referência canônica:** DCV-V4 §8.3

---

### D-041 — T-RANK configurável com regra de desempate default de 3 níveis
**Data:** 2026-04-19 · **Bloco:** DCV-V4 · **Status:** Fechada

**Contexto:** V4 é a primeira visão a consumir T-RANK no refino da Fase 0. Prévio V4 (Parte 5.5) definia regra local ("maior valor; empate alfabético"). Mas T-RANK é transversal da Fundação — decisão fixa requisitos do G-FUND. Adicionalmente: V9 (ranking multidimensional, refino futuro) provavelmente exigirá regra diferente.

**Decisão:** T-RANK aceita parâmetro `regra_desempate` opcional. Default fixado pela V4 (e consumido por V10) — regra de 3 níveis:

1. Valor agregado decrescente
2. Em empate: concatenação dos agrupadores na ordem declarada pelo usuário, ordem alfabética crescente, case-insensitive, acentos normalizados
3. Em empate ainda: ordem de inserção da linha original

Tolerância para floating point: 1e-9 absoluto. Se tolerância resolve, não é empate real.

Visões posteriores (V9 provável) podem sobrescrever via parâmetro.

W-V4-EMPATE (informativa) registra casos com resolução por regra secundária ou terciária.

**Razão:** Parametrização é barata (um argumento no contrato do transversal) e preserva flexibilidade para Fase 1 sem decidir agora o que V9 precisará. Tolerância de floating point evita falso empate por imprecisão numérica. Desempate totalmente determinístico (3 níveis) honra princípio C.1 — sortio ou não-determinismo seriam bugs. Decisão é transversal porque fixa contrato da Fundação, não apenas V4.

**Impacto:**
- CONTEXT §6 atualizado: linha T-RANK ganha descrição da configurabilidade + regra default
- GLOSSARIO §4 atualizado: T-RANK reformulado
- G-FUND incorpora requisito de T-RANK parametrizado
- V4, V10 consomem default sem customização
- V9 (futuro) configurará regra própria
- W-V4-EMPATE catalogada

**Referência canônica:** DCV-V4 §8.4 · CONTEXT §6 (T-RANK) · GLOSSARIO §4 (T-RANK)

---

### D-040 — Limiares ABC com default declarado (80/95) + limiares globais Modo 3 + herança V10
**Data:** 2026-04-19 · **Bloco:** DCV-V4 · **Status:** Fechada

**Contexto:** Prévio V4 (Parte 4.2) definia limiares ABC como "padrão sugerido: A = até 80%, B = até 95%, C = acima de 95%". Vocabulário pré-D-024 (não aplicava padrão "default declarado"). Decisão adicional: Modo 3 com múltiplas medidas — limiares iguais ou por medida? Decisão correlata: V10 (view especializada por D-035) herda os mesmos valores?

**Decisão:** Default declarado de limiares A = 80%, B = 95%, visíveis e editáveis na E4 (condicional ao Modo 2 ou 3). No Modo 3, limiares são **globais** (mesmos para todas as medidas selecionadas). V10 (view especializada) herda os mesmos defaults; diferença está em visualização e microcopy, não nos números.

**Detalhes:**
- Texto visível na UI: "Limiares padrão: 80% para Classe A, 95% para Classe B. Você pode ajustar conforme sua política de priorização."
- Validação: 0 < A < B < 100 (se inválido, bloqueia botão "Continuar")
- W-V4-ABC-CUSTOM (informativa) registra quando limiares diferentes do default foram usados
- V10 diferencia-se apenas pela narrativa ("poucos vitais × muitos triviais"), filtro visual em Classe A, visualização Pareto dedicada

**Razão:** Aplicação direta do padrão cristalizado em D-024/D-025/D-026/D-027/D-029 (default declarado). Limiares globais no Modo 3 preservam **comparabilidade da divergência** (D-042) — se Produto X é A em Receita com limiar 80 e B em Margem com limiar 70, a divergência fica contaminada pela configuração. Usuário avançado que precisa de limiares distintos por medida roda execuções V4 separadas. Defaults compartilhados V4/V10 porque "20%" de Pareto é resultado (quantos elementos caem em A), não parâmetro de entrada.

**Impacto:**
- DCV-V4 §8.5 documenta limiares e validação
- Spec da V4 (Fase 2) detalha UX do bloco de limiares na E4
- T-ABC (Fundação) consome parâmetro; default 80/95 na ausência
- V10 (DCV-V10 futuro) herda por referência
- W-V4-ABC-CUSTOM catalogada

**Referência canônica:** DCV-V4 §8.5

---

### D-039 — POR_LINHAS na V4: "Seleção de medidas em POR_LINHAS" + requisito T-PIVOT multi-medida
**Data:** 2026-04-19 · **Bloco:** DCV-V4 · **Status:** Fechada

**Contexto:** D-026 cristalizou para V2 o tratamento de POR_LINHAS (Modo 4 com ordenação inteligente, default declarado, 4 warnings, T-PIVOT com parâmetro "valores selecionados"). V4 aplicação direta, mas com diferença estrutural importante: V2 pivota **estados** da mesma medida; V4 pivota **medidas** distintas. Modo 3 da V4 já trabalha com múltiplas medidas — vocabulário "Modo 4" da V2 colide com "Modo 1/2/3" da V4.

**Decisão:** Adotar vocabulário "Seleção de medidas em POR_LINHAS" (não "Modo 4") com comportamento condicionado pelo Modo analítico:

| Modo V4 | Seleção mínima | Default declarado |
|---|---|---|
| 1 | 1 medida | Primeira na ordenação inteligente |
| 2 | 1 medida | Primeira na ordenação inteligente |
| 3 | 2 ou mais | Todas pré-selecionadas |

Ordenação inteligente herdada de D-026. Warnings herdados: W-V4-N0 (bloqueio), W-V4-N1 (bloqueio), W-V4-MIX (aviso), W-V4-NMANY (aviso). Novo: W-V4-MEDIDAS-MIN (bloqueio — Modo 3 com <2 medidas selecionadas).

**Requisito novo para G-FUND:** T-PIVOT precisa suportar **pivot multi-medida** (não apenas multi-estado como em D-026). Entrada para G-FUND formalizar na Fase 1.

**Razão:** "Modo 4" na V2 é nome específico para comportamento específico — reusar o nome na V4 com lógica diferente (condicionada por Modo analítico, não fixa em "escolher 2") polui GLOSSARIO e confunde usuária. Vocabulário neutro e descritivo separa cleanly. Pivot multi-medida é extensão natural de T-PIVOT — mesma mecânica, eixo diferente (medidas em vez de estados). Honra C.5 (seleção visível, default declarado).

**Impacto:**
- DCV-V4 §6.1 e §6.2 documentam tratamento
- CONTEXT §6 atualizado: linha T-PIVOT ganha extensão multi-medida
- GLOSSARIO §4 atualizado: T-PIVOT com duas extensões
- G-FUND incorpora requisito de pivot multi-medida
- 5 warnings herdados de D-026 + 1 novo (W-V4-MEDIDAS-MIN)
- Termo "Seleção de medidas em POR_LINHAS" entra no GLOSSARIO §5.V4

**Referência canônica:** DCV-V4 §6.1, §6.2 · CONTEXT §6 (T-PIVOT) · GLOSSARIO §4 (T-PIVOT), §5.V4

---

### D-038 — V4: tratamento de nulo na medida, nulo em agrupador e valores negativos
**Data:** 2026-04-19 · **Bloco:** DCV-V4 · **Status:** Fechada

**Contexto:** Três tensões entrelaçadas: prévio V4 (Parte 5.1) diz "consolidar antes de calcular" sem tratar nulo na medida; Parte 11 lista "presença de valores negativos" como alerta não-bloqueante sem regra concreta; V4 introduz cenário inédito (negativos em cálculo de participação podem produzir valores fora de 0-100%, soma ≠ 100%). D-023 (V2) resolveu nulos — reutilizável. Negativos não têm precedente.

**Decisão:** Contrato `classificacao_medida` da V4 com 3 valores: `VALOR_VALIDO`, `VALOR_NEGATIVO`, `NULO_MEDIDA`. Tratamentos:

**Nulo na medida (NULO_MEDIDA):** excluído do cálculo (Total Geral não inclui; participação = None) mas preservado na listagem com classificação visível. W-V4-NULL (contagem) + W-V4-NULL-MASS (>20% dos registros).

**Nulo em agrupador:** rótulo `(sem valor)` na coluna do agrupador. Linha entra na análise normalmente (participa do Total Geral, recebe participação, entra em ABC). W-V4-AGRUP-SEMVALOR registra contagem.

**Negativos (VALOR_NEGATIVO):** motor detecta na pré-consolidação E3. **Bloco declarado** com 3 opções:
1. "Analisar com valores líquidos" (default) — soma algébrica; participação pode ser negativa ou >100%
2. "Separar análise em positivos e negativos" — duas tabelas com Total próprio; participação dentro de cada universo soma 100%
3. "Usar valor absoluto" — |valor| para ranking/participação; sinal preservado em coluna complementar

W-V4-NEGATIVOS registra opção escolhida + contagem.

**Razão:** Herança de D-023 para nulos é direta (V2 e V4 compartilham lógica — preservar com classificação visível). Negativos são caso novo; 3 opções cobrem interpretações analíticas legítimas (estorno contábil é realidade cotidiana). Bloqueio rígido frustra; execução silenciosa viola C.5. Default declarado aplica padrão D-024 para matemática ambígua. Contrato `classificacao_medida` unificado (não 2 contratos separados) simplifica visualização e Diagnóstico.

**Impacto:**
- DCV-V4 §8.2 documenta os 3 tratamentos e o contrato
- Contrato MotorResult da V4 ganha `classificacao_medida` (enum de 3 valores)
- 4 warnings novos: W-V4-NULL, W-V4-NULL-MASS, W-V4-AGRUP-SEMVALOR, W-V4-NEGATIVOS
- Spec da V4 detalha UX do bloco declarado de negativos na E3
- Padrão "default declarado" para matemática ambígua reforçado

**Referência canônica:** DCV-V4 §8.2

---

### D-037 — Objetivo da Visão V4 + 5 etapas progressivas
**Data:** 2026-04-19 · **Bloco:** DCV-V4 · **Status:** Fechada

**Contexto:** CONTEXT §13.1 (D-015) exige Objetivo da Visão como bloco de ajuda com 4 seções (o que faz · quando usar · o que obtém · como funciona). CONTEXT §13.2 exige Fluxo de etapas progressivas. Prévio V4 (Parte 4.1) lista ações sem agrupamento em etapas. V4 precisa consolidar ambos antes da Spec (Fase 2). Modo (1/2/3) é decisão estrutural V4-específica ausente em V2 — onde encaixar nas etapas?

**Decisão:** V4 organiza configuração em **5 etapas** (paridade com V2) com **Modo aninhado na E2 (Estrutura e modo)**. Hook para bloco condicional E4→E5 reservado para resolução de pré-condições (Total=0 e outros — formalização final na Spec S-V4).

**5 etapas:**
1. **Origem dos dados** — upload + aba
2. **Estrutura e modo** — POR_COLUNAS/POR_LINHAS + Modo 1/2/3 + Seleção de medidas em POR_LINHAS (se aplicável)
3. **Medida(s) e tipo** — medida(s) + tipo + default declarado para relativo/não-aditivo + bloqueio para Estado/Situação + medida de referência (Modo 3) + default declarado para negativos
4. **Agrupadores e classificação** — agrupadores (1-8 com avisos; 9+ bloqueia) + regra de agregação + estimativa de linhas + limiares ABC (Modo 2/3)
5. **Revisão e execução** — preview + faixas de leitura de síntese (Configurações avançadas) + detecção de pré-condições + Processar

Mecânica de invalidação em cadeia herdada de D-029.

**Conteúdo canônico do Objetivo da Visão:** aprovado nas 4 seções (ver DCV-V4 §§1-4). Distinção V4≠V2≠V3, posicionamento V10 como view especializada, vocabulário consolidado.

**Razão:** Paridade de 5 etapas com V2 preserva ritmo de produto (usuário aprende uma mecânica e aplica em todas as visões). Modo aninhado com Estrutura na E2 faz sentido conceitual ("como estão meus dados × como quero enxergar"). Limiares ABC com agrupadores (E4) porque ABC é regra de corte sobre a distribuição dos agrupadores, não sobre medidas. Hook para bloco condicional E4→E5 espelha padrão D-029 da V2 sem antecipar decisão.

**Impacto:**
- DCV-V4 §7 documenta as 5 etapas
- DCV-V4 §§1-4 documentam o conteúdo canônico do Objetivo da Visão
- Spec da V4 (Fase 2) detalha layout do stepper, microcopy, mensagens de erro
- Bloco condicional E4→E5 fica como hook a formalizar na S-V4
- Padrão "5 etapas + Modo na E2" candidato a referência para visões com dimensão analítica (V3, V9 prováveis)

**Referência canônica:** DCV-V4 §§1-4, §7

---

### D-036 — Tipos de medida na V4: default declarado por tipo (extensão da família D-024/D-025)
**Data:** 2026-04-19 · **Bloco:** DCV-V4 · **Status:** Fechada

**Contexto:** Prévio V4 (Parte 3.3) usa vocabulário pré-D-025: lista "medidas potencialmente inadequadas (percentual, média, índice já calculado)" com regra "pode executar, responsabilidade do usuário". Parece C.5 à primeira vista, mas na verdade viola — motor calcula participação sobre campo onde matemática é enganosa e usuário só vê depois. V4 é a primeira visão a integrar a taxonomia D-025 em contexto de participação (cálculo ÷ Total Geral) — diferente de V2 (comparação de estados).

**Decisão:** V4 integra os 4 tipos da D-025 com tratamento por tipo:

- **Numérico aditivo**: executa sem aviso
- **Numérico relativo** e **Numérico não-aditivo**: bloco declarado na E3 com 3 opções:
  1. "Analisar mesmo assim" (default)
  2. "Escolher outra medida"
  3. "Agregar por média ponderada antes de calcular participação" (Modo 1 apenas; desativa ABC; exige campo de peso)
- **Estado/Situação**: bloqueio operacional com redirecionamento: "composição por participação não se aplica a campos categóricos. Use V6."

No Modo 3, regra aplica-se por medida (cada medida passa pelo bloco individualmente). Heterogeneidade entre medidas tratada separadamente (D-042).

W-V4-TIPO-DECL (informativa) registra opção escolhida.

**Razão:** Aplicação direta do padrão "default declarado" cristalizado em D-024. Bloqueio para Estado/Situação não viola C.5 — bloqueio operacional quando matemática não existe (soma de categorias não é operação válida). Terceira opção (média ponderada antes) cobre caso analítico real (margem média ponderada por receita, muito comum em contabilidade brasileira). Desativação de ABC na opção 3 é natural: média ponderada produz uma linha por agrupador, ABC perderia sentido.

**Impacto:**
- DCV-V4 §6.3 documenta tratamento
- Spec da V4 (Fase 2) detalha UI do bloco declarado na E3
- motor_upload (Fundação) herda heurística + confirmação de tipo (requisito da V2 + V4)
- W-V4-TIPO-DECL catalogada
- Estado/Situação redireciona explicitamente para V6 — estabelece padrão de "fronteira entre visões com mensagem construtiva"
- Extensão formal da família D-024/D-025 — padrão "default declarado" agora consolidado em duas famílias conceituais (A e C)

**Referência canônica:** DCV-V4 §6.3

---

### D-035 — V4 × V10: V10 como view especializada sobre V4 Modo 2 (decisão transversal)
**Data:** 2026-04-19 · **Bloco:** DCV-V4 · **Status:** Fechada

**Contexto:** Três fontes apontavam para tensão sem resolvê-la: CONTEXT §4 ("sobreposição significativa entre V4 e V10 — V10 é, em larga medida, caso particular de V4 modo 2"); planilha aba 5 P-G1 ("V10 é visão independente ou modo de V4? Decidir no G-FUND"); DCV prévio V4 trata V10 como inexistente. Afeta o que V4 precisa entregar no Modo 2 e escopo do G-FUND. Decisão adiada produziria duas respostas possíveis para cada pendência seguinte (Modo 2, ABC, ranking).

**Decisão:** V4 implementa os 3 modos (Composição Simples, Curva ABC, Comparação de Distribuição) incluindo ABC canônico no Modo 2. **V10 é view especializada sobre V4 Modo 2** — consome a mesma lógica da V4 com preset Pareto (80/95), filtro visual em Classe A, microcopy dedicado ("poucos vitais × muitos triviais") e visualização Pareto própria (curva Pareto clássica com corte vital/trivial).

V10 preserva identidade de produto (entrada simplificada, narrativa Pareto) sem duplicar lógica analítica. G-FUND formaliza contrato: "T-ABC + T-ACUM + T-RANK consumidos por V4 e V10 com a mesma lógica; V10 é view especializada sobre V4 Modo 2".

**Razão:** Três motivos convergem:

1. **C.5 aplicado ao método.** Opções rejeitadas ("V4 absorve V10" / "V4 + V10 com implementações paralelas") decidem silenciosamente questões que deveriam ser explícitas. "V10 como view especializada" declara a fronteira sem esconder escolha.

2. **Precedente da Família A.** V2 é caso base, V1 é extensão via T-DUAL (duas bases). Família C seguir o mesmo padrão (V4 caso base, V10 especialização) mantém coerência metodológica.

3. **Economia de refino do DCV-V10 seguinte.** V10 herda de V4: tipos de medida (D-036), nulos/negativos (D-038), limiares ABC (D-040), T-RANK (D-041), bloqueios operacionais (D-043), T-MODELO (padrão D-030). DCV-V10 foca nas diferenças específicas: preset Pareto, microcopy, visualização dedicada. Sessão curta provável.

**Impacto:**
- Planilha aba 5 P-G1 fecha (resolvida por D-035)
- CONTEXT ganha §13.4 "View especializada entre visões da mesma família" documentando o padrão (Família A com T-DUAL + Família C com V10 view)
- Padrão candidato a referência para pares conceitualmente próximos em outras famílias
- G-FUND: T-ABC, T-ACUM, T-RANK recebem como requisito o suporte a V10 sem reimplementação
- Fase 2: V10 (ordem) consome lógica V4 Modo 2 já implementada
- Escopo da Família C consolidado

**Referência canônica:** DCV-V4 §2 (distinção V4×V10) · CONTEXT §13.4 · planilha aba 5 (P-G1 fechada)

### D-034 — Densidade de decisões durante refino: sinalização no 3º status-check
**Data:** 2026-04-19 · **Bloco:** (decisão de método, fora de bloco específico) · **Status:** Fechada

**Contexto:** A Sessão 1 do DCV-V2 (18/04/2026) gerou 12 decisões transversais — densidade ~2x maior que a Sessão 2 do DCV-V1. O kit de encerramento estourou o orçamento de ferramentas em 3 tentativas consecutivas, exigindo sessão dedicada exclusivamente para finalização. Conversa pós-fechamento revelou que o gargalo não era previsível antes da sessão começar — depende da densidade de decisões transversais que emergem, e essa densidade só fica clara conforme a sessão avança.

**Decisão:** O Arquiteto sinaliza explicitamente a densidade da sessão **no 3º mini status-check** (após ~9 pendências fechadas) com formato:
> "Densidade desta sessão: [X] decisões transversais até aqui. Estimativa de orçamento de kit: [alto/médio/baixo]. Recomendo [continuar / fechar refino aqui e abrir sessão dedicada ao kit]."

A Usuária decide se continua ou separa. Se separar, kit vira sessão dedicada exclusiva. Se continuar e estourar mesmo assim, sessão vira "kit incompleto" e seguimos com sessão de finalização.

**Razão:** Combinada com D-033 (novo formato do kit que libera ~30-40% do orçamento), Opção A é mais barata que kit incremental (Opção B) que adicionaria overhead em todas as sessões para resolver problema que vai ocorrer só em sessões densas. Sinalização proativa no 3º status-check dá controle informado à Usuária sem mudar o ritmo da maioria das sessões. Formaliza o comportamento que já adotamos reativamente.

**Impacto:**
- Padrão de condução D-019 ganha um elemento adicional: no 3º status-check (~9 pendências), incluir estimativa de orçamento de kit.
- Não há mudança em CONTEXT (D-019 vive nas Instruções do Projeto, não no CONTEXT).
- Instruções do Projeto §Padrão de condução em sessões de DCV ganham menção a este comportamento.
- Caso prático esperado: DCV-V4 (3 modos + ABC + ranking + sobreposição com V10) tem chance real de exigir sinalização.

**Referência canônica:** Instruções do Projeto §Padrão de condução em sessões de DCV (item adicional)

---

### D-033 — Reorganização do kit de encerramento: divisão entre arquivos completos e instruções de edição
**Data:** 2026-04-19 · **Bloco:** (decisão de método, fora de bloco específico) · **Status:** Fechada

**Contexto:** A Sessão 1 do DCV-V2 mostrou que o formato D-020 (todos os 5 arquivos canônicos como artefatos completos) era caro demais em ferramentas para sessões de densidade alta. Análise pós-fechamento identificou que a planilha sozinha consome 30-40% do orçamento de ferramentas do kit por exigir openpyxl + preservação de estilos + validação multi-aba. DECISIONS.md também é caro mas previsível. CONTEXT.md tem custo médio mas dificuldade alta para a Usuária editar manualmente (mudanças em várias seções não-contíguas). GLOSSARIO acumula mudanças que muitas vezes não são significativas o suficiente para justificar regeneração.

**Decisão:** Reorganizar o kit de encerramento em duas categorias:

**Itens produzidos pelo Arquiteto (arquivo completo para download):**
- CONTEXT.md (sempre que houver mudança)
- Artefato da sessão (DCV, Spec, Base, Prompt — quando aplicável)
- GLOSSARIO.md (apenas quando acumular mudanças significativas — gatilhos abaixo)
- Instruções do Projeto (apenas se houver mudança de método)
- Prompt da próxima conversa (texto inline)

**Itens instruídos pelo Arquiteto, aplicados pela Usuária:**
- DECISIONS.md (Arquiteto entrega entradas D-XXX em texto pronto para colar + lista de status changes em entradas antigas)
- Planilha (Arquiteto entrega instruções de edição: aba, célula, valor novo)

**Gatilhos para regenerar GLOSSARIO completo:**
- 5+ termos novos acumulados desde a última atualização
- Reformulação de tabela importante (como tabela de tipos de campo D-025)
- 8+ warnings novos catalogados
- Novo padrão consolidado que merece entrada própria
- Termo descontinuado que precisa entrar no anti-glossário

Quando nenhum gatilho dispara, Arquiteto sinaliza "GLOSSARIO inalterado nesta sessão" e Usuária não precisa baixar nada. Quando algum dispara, Arquiteto sinaliza proativamente.

**Razão:** Divisão respeita o que é caro vs barato em cada lado: planilha e DECISIONS são fáceis de editar manualmente (cells e blocos de texto), mas caros de produzir como arquivo. CONTEXT e DCV são difíceis de editar manualmente (mudanças em seções múltiplas, prosa estruturada longa), mas o custo de produzir como arquivo se justifica. Decisão devolve à Usuária controle visual sobre o que muda na planilha e no DECISIONS — onde "ver o que mudou" importa mais. Libera 30-40% do orçamento de ferramentas para uso em DCV mais cuidadoso, validação extra e margem para sessões densas.

**Impacto:**
- CONTEXT §11 (Ritual de encerramento de sessão) reescrito refletindo nova divisão
- Instruções do Projeto §Ritual de encerramento de conversa reescrito refletindo nova divisão
- Formato D-020 anterior absorvido por este — não revogado, mas refinado
- A partir desta decisão (próximo bloco DCV-V4), todas as sessões aplicam o novo formato

**Referência canônica:** CONTEXT §11 · Instruções do Projeto §Ritual de encerramento de conversa

### D-032 — Bloqueios operacionais e diretrizes de performance da V2
**Data:** 2026-04-18 · **Bloco:** DCV-V2 (Sessão 1) · **Status:** Fechada

**Contexto:** O DCV prévio da V2 deixou abertas duas pendências relacionadas: P-04 ("limite de bloqueio por inconsistência extrema — casos onde execução deve parar ainda não definidos") e P-07 ("performance — bases grandes são padrão, motor deve ser otimizado, evitar recomputação"). Ambas precisavam ser fechadas no DCV para que F-MOT e G-FUND tivessem requisitos claros — sem decisão aqui, motor nasceria sem critério de quando parar e sem orientação técnica de performance.

**Decisão:** Definir 8 casos de bloqueio operacional + 7 diretrizes de performance para a Fundação.

**Bloqueios operacionais** (param execução independentemente de decisão da Usuária, sempre com mensagem clara + sugestão):
1. Arquivo ilegível ou corrompido
2. Estrutura inválida: arquivo vazio, aba sem dado, sem coluna numérica detectada quando esperada
3. Coluna discriminadora POR_LINHAS com 0 ou 1 valor único (W-V2-N0, W-V2-N1)
4. Campo analisado com 100% de nulos em Origem ou Comparado
5. Mais de 9 agrupadores declarados (D-027)
6. Pesos todos zerados ou negativos quando média ponderada escolhida (D-024)
7. Falha estrutural não-recuperável detectada na transição E4→E5
8. Análise gera mais de 500.000 linhas no resultado (limite operacional)

**Diretrizes de performance para o G-FUND/F-MOT:**
1. Leitura de arquivo: stream/chunked quando possível
2. Pivot/merge: índices pandas eficientes; outer join obrigatório (P-V2-02) otimizado
3. Estimativa de linhas (D-027): cardinalidades multiplicadas, não produto cartesiano real
4. Cálculos vetorizados (numpy), nunca loop linha-a-linha
5. Cache de execução por hash de configuração + base — mecânica fica para Fundação
6. Limite operacional de 500K linhas no resultado
7. Diagnóstico inclui métricas de tempo por etapa do motor

**Razão:** Bloqueios são decisões operacionais (proteção do sistema), não analíticas — Princípio C.5 não é violado quando motor explica o motivo e sugere caminho. Limite de 500K linhas é arbitrário mas defensível: Excel suporta ~1M linhas por aba, mas além de 500K a UX da V2 fica inviável (rolagem hostil, exportação lenta). Performance entra como diretriz e não como trava porque otimização específica é responsabilidade do F-MOT na Fundação, não do DCV da V2.

**Impacto:**
- Spec da V2 (Fase 2) detalha mensagens específicas de cada bloqueio
- F-MOT incorpora as 7 diretrizes como requisitos de implementação
- F-EXP (exportação Excel) precisa registrar tempo por etapa no Diagnóstico
- W-V2-N0 e W-V2-N1 (já definidas em D-026) são reusadas como gatilhos de bloqueio

**Referência canônica:** DCV-V2 §10 e §11

---

### D-031 — Conteúdo canônico do Resumo Executivo da V2
**Data:** 2026-04-18 · **Bloco:** DCV-V2 (Sessão 1) · **Status:** Fechada

**Contexto:** O DCV prévio da V2 (P-01) deixou aberto o conteúdo do Resumo Executivo: "estrutura definida, conteúdo ainda não fechado". Era preciso fechar para a Spec da Fase 2 ter input concreto. Sem definição, cada implementação criaria um Resumo Executivo diferente — perdendo padrão entre visões.

**Decisão:** Resumo Executivo da V2 tem **6 blocos fixos** em ordem de leitura:
1. **Cabeçalho da análise** — título amigável, campo, agrupadores, data/hora
2. **Números-âncora** — 4 KPIs em destaque (Total Origem, Total Comparado, Diferença total, Variação total %)
3. **Distribuição de classificações estruturais** — contagem das 6 categorias do contrato (PRESENTE_AMBOS, AUSENTE_*, NULO_*)
4. **Maiores variações** — top 10 combinações com maior |Δ|
5. **Distribuição de comportamento (semântica aplicada)** — Positivo/Negativo/Neutro/Não aplicável (apenas tipos numéricos)
6. **Qualidade estrutural** — resumo executivo do que aparece no Diagnóstico (casos resolvidos, ajustes leves, warnings com contagem)

Para tipo Estado/Situação: blocos 2, 4 e 5 têm formato adaptado (combinações com mudança em vez de variação numérica).

**Razão:** 6 blocos cobrem o ciclo natural de leitura do analista corporativo: identificar análise → ver totais → ver distribuição → ver outliers → entender comportamento → auditar qualidade. Resumo Executivo apresenta **fatos**, não interpretação opinativa — honra C.5 ao não dizer "a empresa piorou" mas "Total Comparado é R$ 1.2M menor (-15%)". Categorias zeradas omitidas da exibição (mas presentes no contrato) reduz ruído visual sem perder informação técnica.

**Impacto:**
- DCV-V2 §8.1 documenta os 6 blocos
- Spec da V2 (Fase 2) detalha layout, microcopy, cores
- F-EXP (exportação Excel) implementa template Aba 1 com os 6 blocos
- Padrão de "6 blocos" pode ser referência para Resumo Executivo de outras visões (com adaptação por natureza analítica)

**Referência canônica:** DCV-V2 §8.1

---

### D-030 — Modelo de configuração da V2: persistência lógica, não dado
**Data:** 2026-04-18 · **Bloco:** DCV-V2 (Sessão 1) · **Status:** Fechada

**Contexto:** CONTEXT §13.3 (D-015) define que toda visão permite salvar e aplicar configuração como modelo reutilizável via T-MODELO. Faltava decidir, para a V2 especificamente, **o que persistir** no modelo e **como aplicar** em nova base. Sem essa decisão, T-MODELO fica abstrato demais para implementação.

**Decisão:** Modelo da V2 persiste **apenas configuração lógica**, nunca dado fonte.

**Persiste:** identificação (nome, descrição, datas), tipo de estrutura (POR_COLUNAS/POR_LINHAS), nome da coluna discriminadora, rótulos amigáveis Origem/Comparado, valores escolhidos em Modo 4, nome do campo + tipo + semântica, método de consolidação + campo de peso (se média ponderada), lista ordenada de agrupadores, regra de agregação, decisão de resolução estrutural se houve.

**Não persiste:** arquivo bruto, nome do arquivo, aba selecionada, filtros pós-execução, resultado da análise anterior.

**Aplicação em nova base:** sistema tenta casar nomes salvos com colunas da nova base. Se todos casam → E2-E4 pré-preenchidas. Se algum não casa → aviso "Modelo aplicou parcialmente, ajustar manualmente" (W-V2-MOD-PARCIAL). Se estrutura incompatível → avisa, zera etapas dependentes (W-V2-MOD-INCOMP). Diagnóstico registra: "Modelo aplicado: [nome] · Campos casados: [N/total] · Ajustes manuais: [lista]".

**Razão:** Persistir só configuração lógica honra C.5 — modelo reproduz a **declaração** da Usuária, não o resultado. Aplicação não decide silenciosamente: divergência vira ajuste manual visível. Aba 4 Parâmetros do Excel sempre registra o estado **efetivo** da execução, não o original do modelo — preserva auditabilidade. Persistir dado fonte (alternativa rejeitada) violaria privacidade, inflaria armazenamento, e quebraria o princípio de "modelo é receita, não prato pronto".

**Impacto:**
- DCV-V2 §7 documenta o contrato de persistência
- T-MODELO (Fundação) ganha contrato concreto: serializar/desserializar essa estrutura
- 2 warnings novos: W-V2-MOD-PARCIAL, W-V2-MOD-INCOMP
- Spec da V2 (Fase 2) detalha UX de "Salvar como modelo" (E5) e "Aplicar modelo" (E1)
- Persistência de armazenamento (local/navegador/backend) fica para Fundação decidir

**Referência canônica:** DCV-V2 §7

---

### D-029 — Etapas progressivas da V2: 5 etapas + bloco intermediário condicional
**Data:** 2026-04-18 · **Bloco:** DCV-V2 (Sessão 1) · **Status:** Fechada

**Contexto:** CONTEXT §13.2 (D-015) define etapas progressivas como padrão estrutural obrigatório, mas o número e nome das etapas é específico de cada visão. O DCV prévio da V2 listava as ações em 2.4 (Configuração do usuário) sem agrupamento ou ordenação. Era preciso decidir granularidade da V2 antes da Spec, porque a Spec precisa do esqueleto para desenhar o wireframe.

**Decisão:** A V2 organiza configuração em **5 etapas sequenciais** + **1 bloco intermediário condicional**:

1. **Origem dos dados** — upload + escolha de aba
2. **Estrutura da comparação** — POR_COLUNAS/POR_LINHAS + Origem/Comparado + Modo 4 + rótulos
3. **O que comparar** — campo + tipo (D-025) + semântica + consolidação se aplicável (D-024)
4. **Como agrupar** — agrupadores (1-9, D-027) + regra de agregação + estimativa de linhas + confirmações de zona
5. **Revisão e execução** — preview da configuração + processar

**Bloco intermediário (não-numerado):** entre E4 e E5, motor analisa as bases e detecta inconsistência estrutural (D-021). Se detectada não-leve, abre painel de resolução com opções específicas. Se não detectada, fluxo segue direto.

Mecânica de invalidação em cadeia definida: mudar arquivo (E1) invalida tudo; mudar estrutura (E2) invalida E3-E5; mudar campo/tipo (E3) invalida E4-E5; mudar agrupadores (E4) invalida E5. Estado preservado em mudanças (não obriga redigitar campos não afetados).

**Razão:** 5 etapas dão equilíbrio: cada etapa tem propósito único (não amontoa decisões), defaults declarados ficam visíveis em etapas separadas (E3 consolidação, E4 estimativa) honrando C.5, casos estruturais ficam isolados em bloco condicional (não confunde fluxo normal). Alternativa de 3 etapas amplas misturava 6 ações na E2; alternativa de 7 etapas granulares cansava o usuário corporativo. Padrão "5 + bloco condicional" é candidato a referência para outras visões com ajuste por complexidade.

**Impacto:**
- DCV-V2 §6 documenta as etapas
- Spec da V2 (Fase 2) detalha layout do stepper, microcopy, mensagens de erro
- Wireframe funcional (S-V2) materializa a UX das etapas
- Pode ser herdado/adaptado por outras visões (V3, V4, V5, V6, V7, V8, V9, V10)

**Referência canônica:** DCV-V2 §6

---

### D-028 — Conteúdo canônico do Objetivo da Visão V2
**Data:** 2026-04-18 · **Bloco:** DCV-V2 (Sessão 1) · **Status:** Fechada

**Contexto:** CONTEXT §13.1 (D-015) define "Objetivo da Visão" como bloco de ajuda contextual obrigatório de toda visão, com 4 seções (o que faz · quando usar · o que obtém · como funciona). Faltava o **conteúdo concreto** para a V2. Sem definição, cada implementação inventaria texto próprio — perdendo coerência de produto e potencialmente desalinhando vocabulário.

**Decisão:** Aprovar conteúdo canônico das 4 seções para a V2, escrito em linguagem de negócio e usando vocabulário consolidado nas decisões anteriores (Origem/Comparado técnico, "Comparar de"/"Comparar com" UX, Modo 4, classificação estrutural, default declarado, tipos de campo D-025).

Conteúdo aprovado vive em DCV-V2 §1, §2, §3 e §6 (as 4 seções correspondem a "O que a visão faz", "Quando usar", "O que você obtém", "Como funciona").

**Razão:** Conteúdo aprovado no DCV evita duas patologias: (1) implementação inventando texto inconsistente com o método; (2) revisão tardia no app forçando reescrita de microcopy quando código já está pronto. Distinção explícita V2 ≠ V1 ≠ V3 ≠ V4/V10 ajuda usuário a escolher visão certa logo de cara. Tom de analista corporativo (não programador) honra o público-alvo.

**Impacto:**
- DCV-V2 §§1-3 e §6 documentam o conteúdo
- Spec da V2 (Fase 2) usa este conteúdo como input do componente "Objetivo da Visão" da UI
- Estabelece padrão de redação para Objetivo da Visão das outras 9 visões

**Referência canônica:** DCV-V2 §§1-3, §6

---

### D-027 — Limite de agrupadores: progressivo (1-3 normal, 4-5 aviso, 6-8 confirmação, 9+ bloqueio)
**Data:** 2026-04-18 · **Bloco:** DCV-V2 (Sessão 1) · **Status:** Fechada

**Contexto:** O DCV prévio da V2 (2.3.5) impunha trava rígida em 5 agrupadores: "máximo 5; excedeu → bloqueia". Em conflito com legado (W03 antiga era warning >3, sem trava) e com Princípio C.5 (trava arbitrária no produto viola C.5 quando há razão analítica plausível para ultrapassar). Cada agrupador adicional multiplica a granularidade do resultado — 5 agrupadores cobrem 95% dos casos corporativos, mas o caso 6 ou 7 existe e travar arbitrariamente frustra usuário corporativo.

**Decisão:** Limite progressivo, não trava rígida:

| N° agrupadores | Comportamento |
|---|---|
| 1-3 | Normal, sem aviso |
| 4-5 | Aviso visível + estimativa de linhas |
| 6-8 | Confirmação obrigatória extra (checkbox "entendo o impacto") |
| 9+ | Bloqueio com mensagem + sugestão de V6 + opção "remover agrupadores" |

Estimativa de linhas (cardinalidade × cardinalidade × ...) calculada em tempo real conforme usuário adiciona/remove agrupadores. W-V2-AGRUP-MUITOS dispara para ≥6 agrupadores efetivamente usados.

**Razão:** Bloqueio em 9 não é arbitrário: 5 cobrem 95% dos casos; 6-8 cobrem casos avançados legítimos (análise multidimensional fina); 9+ é estatisticamente território de pivot table que deveria estar em ferramenta dedicada (V6 Relacionamento entre Dimensões ou Power BI). Bloqueio é operacional (proteção do produto), não analítico — encaminha para V6 em vez de só negar. Avisos crescentes respeitam autonomia do usuário sem ignorar realidade operacional. Padrão coerente com P-V2-07 (W-V2-NMANY: aviso para >50 valores em coluna discriminadora — mesma lógica de "permite mas avisa").

**Impacto:**
- W03 antiga (>3 com warning) abandonada → substituída por W-V2-AGRUP-MUITOS (≥6) com lógica diferente
- DCV-V2 §5.4 documenta a regra
- Spec da V2 (Fase 2) implementa contador + estimativa em tempo real na E4
- Estimativa de cardinalidade vira requisito da Fundação (G-FUND/F-MOT)
- Padrão herdável por outras visões com cruzamentos múltiplos (V4, V6, V7, V9)

**Referência canônica:** DCV-V2 §5.4

---

### D-026 — Modo 4: tratamento de POR_LINHAS com >2 estados na coluna discriminadora
**Data:** 2026-04-18 · **Bloco:** DCV-V2 (Sessão 1) · **Status:** Fechada

**Contexto:** O DCV prévio da V2 (2.3.1) dizia apenas "se houver mais [que 2 estados] → usuário escolhe", sem detalhamento. O termo "Modo 4" já estava no GLOSSARIO como herança da V1 do método, mas comportamento concreto (quando detectar, como apresentar opções, ordenação, default, limites) ainda não estava definido. Sem decisão, cada implementação criaria UX diferente.

**Decisão:** Quando motor detecta POR_LINHAS com **3 ou mais valores únicos** na coluna discriminadora, ativa bloco de seleção de estados na E2.

**Ordenação inteligente:**
- Valores numéricos: crescente
- Datas válidas: cronológica crescente
- Período textual reconhecível pt-BR/pt-EN (Jan/24, Fev/24...): cronológica crescente
- Texto livre não cronológico: alfabética crescente
- Misto/inválido: alfabética + warning W-V2-MIX

**Default declarado:** extremos (primeiro e último na ordenação aplicada). Visível com texto "Sugestão: comparar [primeiro] vs [último]. [Alterar]". Usuário aceita ou troca.

**Estados não escolhidos:** excluídos do MotorResult, registrados no Diagnóstico.

**Limites operacionais:**
- N > 50 → W-V2-NMANY: sugere filtragem prévia
- N = 1 → W-V2-N1: erro, impossível comparar
- N = 0 → W-V2-N0: erro, estrutura inválida

**Razão:** Honra C.5 (motor não escolhe quais 2 estados, só apresenta). Ordenação inteligente é serviço útil que não decide nada analítico. Default em extremos cobre o caso mais comum (variação total) sem impedir escolha customizada. Limite de 50 + sugestão alinha com padrão "permite mas avisa" da P-V2-08. Bloqueio em 0/1 valores é operacional. Reconhecer padrões cronológicos pt-BR/pt-EN sem inventar ordem para texto ambíguo previne falsos cronológicos perigosos.

**Impacto:**
- DCV-V2 §3.1 e §5.1 documentam comportamento
- 4 warnings novos: W-V2-MIX, W-V2-NMANY, W-V2-N1, W-V2-N0
- T-PIVOT (Fundação) ganha requisito: aceitar parâmetro "valores selecionados da coluna discriminadora"
- motor_upload (Fundação) reconhece padrão cronológico pt-BR e pt-EN para ordenação inteligente — requisito propagado para G-FUND
- Spec da V2 (Fase 2) implementa UI da E2 com lista ordenada + busca para N alto

**Referência canônica:** DCV-V2 §3.1, §5.1

---

### D-025 — Tipos de campo da V2: 4 tipos consolidados (aditivo, relativo, não-aditivo, estado)
**Data:** 2026-04-18 · **Bloco:** DCV-V2 (Sessão 1) · **Status:** Fechada

**Contexto:** O DCV prévio da V2 (2.2) listava 6 tipos sem dizer como cada um se comporta no cálculo. O GLOSSARIO listava 7 tipos com comportamento parcial, mas com ambiguidades ("Prazo/Tempo" pode ser aditivo ou não dependendo do uso) e fragmentações artificiais ("Quantidade" vs "Volume" — ambos aditivos puros). Sem consolidação, contrato MotorResult não saberia ramo lógico para decidir cálculos default e exportação.

**Decisão:** A V2 trabalha com **4 tipos de campo** consolidados:

| Tipo | Cálculo | Consolidação por agrupador | Exemplos |
|---|---|---|---|
| **Numérico aditivo** | Diferença e variação % | Soma (default), via T-AGRUPA configurável | Receita, custo, quantidade, volume, dias trabalhados, headcount acumulado |
| **Numérico relativo** | Diferença e variação % | Default declarado: média simples + ponderada/não consolidar (D-024) | Margem %, taxa, índice, score, NPS |
| **Numérico não-aditivo** | Diferença e variação % | Default declarado: média simples + ponderada/não consolidar | Estoque pontual, saldo bancário, headcount em data, preço unitário |
| **Estado/Situação** | Sem aritmética; comparação textual ("mudou"/"manteve") | Contagem por categoria | Status, categoria, classificação manual |

Para tipos numérico relativo e não-aditivo: ativam UI de "Como consolidar?" (D-024) com defaults declarados. Para Estado/Situação: fluxo simplificado sem semântica nem cálculo numérico, comparação direta valor textual Origem vs Comparado, resumo executivo adaptado.

Heurística automática (motor sugere tipo provável a partir do nome do campo + dados, usuário confirma) entra como requisito da Spec, não detalhe deste DCV.

**Razão:** Consolidar em 4 tipos elimina fragmentação artificial (Quantidade vs Volume) e ambiguidade (Prazo/Tempo cai em aditivo OU não-aditivo conforme uso real, com tratamento de ambiguidade declarada honrando C.5). Tipo "Numérico não-aditivo" novo cobre caso "estoque pontual" que GLOSSARIO antigo não cobria com clareza. Estado/Situação dentro do escopo da V2 inicial mantém visão como genuinamente comparativa textual também — não restringe o produto a numérico apenas.

**Impacto:**
- GLOSSARIO §5 será atualizado substituindo tabela de 7 tipos por tabela de 4 tipos
- DCV-V2 §3.2 documenta a tabela consolidada
- Vocabulário base (4 tipos) é candidato a herança para outras visões com campo numérico configurável (V3, V4, V5, V6, V7, V8, V9, V10)
- Tratamento de ambiguidade (heurística + default declarado) entra como requisito da Spec da V2 (Fase 2)
- Contrato MotorResult precisa do enum de 4 valores

**Referência canônica:** DCV-V2 §3.2 · GLOSSARIO §5 (atualizado)

---

### D-024 — Consolidação de PERCENTUAL/INDICE: 3 opções declaradas (revoga D-002)
**Data:** 2026-04-18 · **Bloco:** DCV-V2 (Sessão 1) · **Status:** Fechada

**Contexto:** A D-002 (17/04/2026), com status provisório, decidia que campos PERCENTUAL/INDICE consolidados por agrupador receberiam média simples como default + warning W07. Problema: viola Princípio C.5 (formalizado depois) — usuário pode achar que está vendo "margem média da empresa" quando está vendo "média aritmética das margens das filiais ignorando peso comercial". Em contexto contábil/financeiro essa diferença pode ser de 5-10 pontos percentuais. Default silencioso + warning pós-execução é exatamente o padrão "ajusta cedo, evidencia tarde" que P-V2-01/D-021 rejeitou.

**Decisão:** Revogar D-002. Quando usuário seleciona campo de tipo Numérico relativo OU Numérico não-aditivo (D-025) **E** configurou ≥1 agrupador, a Etapa 3 apresenta **bloco de consolidação visível** com 3 opções:

1. **Média simples** (default declarado, pré-selecionada com texto explícito na UI)
2. **Média ponderada** por campo (usuário escolhe campo de peso entre os campos numéricos da base)
3. **Não consolidar** (Resumo Executivo apresenta detalhamento por agrupador sem linha de total)

**Tratamento de pesos** (média ponderada):
- Algum peso nulo → linha excluída do cálculo, registrado no Diagnóstico
- Todos os pesos zero → impossível ponderar, motor para e pede confirmação (cai como caso estrutural pela D-021)
- Pesos negativos → motor para e pede confirmação

Configuração persiste no MotorConfig e vai para a Aba 4 Parâmetros do Excel. Diagnóstico registra qual método foi aplicado. **W07 antiga renomeada para W-V2-AGG** com semântica diferente: informativa ("aplicada [método] para campo [tipo] [nome]"), não alerta de surpresa.

**Razão:** C.5 não exige decisão explícita do usuário em tudo — exige que decisões analíticas sejam **visíveis e revertíveis** antes da execução. Default declarado em interface satisfaz isso; default silencioso no motor não. Diferença entre A (manter D-002) e C é arquitetural, não técnica: no final, motor pode aplicar média simples nos dois casos. Mas em A o motor decidiu; em C o usuário viu, foi informado e teve a chance de mudar. Estabelece padrão "default declarado" que se cristalizou nesta sessão como princípio operacional aplicado também em D-025, D-026, D-027.

**Impacto:**
- D-002 vira "Revogada por D-024"
- W07 antiga renomeada → W-V2-AGG (informativa)
- Etapa de Configuração (E3) ganha bloco de consolidação visível para tipos relativo/não-aditivo
- Categorias AUSENTE_*/NULO_* (P-V2-02, P-V2-03) explicitamente fora do cálculo de consolidação
- Spec da V2 (Fase 2) detalha UX do bloco de consolidação
- Padrão "default declarado" emerge como candidato a princípio formal (a confirmar em sessões futuras)

**Referência canônica:** DCV-V2 §3.2, §3.3 · CONTEXT §9 Camada C (revisão futura para princípio "default declarado")

---

### D-023 — Tratamento de nulo no campo analisado e em agrupadores (reverte D-004)
**Data:** 2026-04-18 · **Bloco:** DCV-V2 (Sessão 1) · **Status:** Fechada

**Contexto:** A D-004 (17/04/2026) decidia, no contexto da V2 antiga, que registro com nulo em A ou B é **excluído** da análise + warning W01. O DCV prévio da V2 não trata nulos explicitamente — lacuna estrutural. Princípio C.5 (formalizado depois) rejeita exclusão silenciosa: usuário pode querer ver "este SKU tem valor nulo no Realizado, vou investigar" — exatamente como queria ver SURGIMENTO/DESAPARECIMENTO. Exclusão de cálculo é necessária (não dá para somar None com 5), mas exclusão da listagem do resultado é decisão analítica que esconde fato relevante.

Distinção importante mantida na decisão: **ausência de registro** (linha não existe em uma das bases — tratado por D-022) ≠ **valor nulo** (linha existe mas valor está em branco) ≠ **valor zero** (tratado normalmente em cálculos).

**Decisão:** Revogar D-004. Adicionar **3 categorias** ao contrato `classificacao_estrutural`:

| Contrato técnico | Exibição ao usuário |
|---|---|
| `NULO_ORIGEM` | "Valor nulo na Origem" |
| `NULO_COMPARADO` | "Valor nulo no Comparado" |
| `NULO_AMBOS` | "Valor nulo em ambos" |

Registros com classificação NULO_* **excluem do cálculo** (diferença e variação ficam None) mas **mantêm o registro na listagem** com classificação visível.

**Nulo em agrupador** (caso lateral): linha entra na análise sob rótulo `(sem valor)` para aquele agrupador. Diagnóstico reporta volume.

**Visualmente:** None por nulo aparece como "—" ou "(nulo)"; None por ausência aparece como "(não consta)". Dado bruto é igual; classificacao_estrutural carrega o significado.

**Warnings:** W-V2-NULL (contagem por classificação NULO_*) + W-V2-NULL-MASS (>20% dos registros do campo com nulo, sinaliza qualidade deteriorada — herdada da W01 antiga reformulada).

**Razão:** Honra C.5 ao apresentar fato em vez de esconder. Distinção AUSENTE_* (D-022) vs NULO_* preserva diferença analítica: AUSENTE_* significa "linha não está nesta base" (descontinuação?); NULO_* significa "linha presente, valor não preenchido" (erro de digitação? processo incompleto?). Tratamento de nulo em agrupador como `(sem valor)` em vez de excluir torna o nulo visível e separável sem inventar valor — coerente com o princípio aplicado em P-V2-02 (None em vez de 0).

**Impacto:**
- D-004 vira "Revogada por D-023"
- Contrato `classificacao_estrutural` ganha 3 categorias novas (chega a 6 categorias totais com as de D-022)
- 2 warnings novos: W-V2-NULL, W-V2-NULL-MASS
- Lógica do motor: outer join com classificação dual (presença + nulidade), cálculos só em PRESENTE_AMBOS
- Diagnóstico (aba final) ganha 2 blocos: nulos no campo + nulos em agrupadores
- DCV-V2 §3.1, §3.4, §4.4 documentam o tratamento

**Referência canônica:** DCV-V2 §4.3, §4.4

---

### D-022 — Registros sem par em outer join: vocabulário dual + None em vez de 0/-100% (reverte D-001)
**Data:** 2026-04-18 · **Bloco:** DCV-V2 (Sessão 1) · **Status:** Fechada

**Contexto:** A D-001 (17/04/2026) decidia que registro presente apenas em A → DESAPARECIMENTO (valor_b=0, variacao_pct=-1.0); presente apenas em B → SURGIMENTO (valor_a=0, variacao_pct=None) + warning W06. O DCV prévio da V2 (2.3.6) usa vocabulário diferente ("Não realizado" / "Novo / Surgiu") — conceito igual, vocabulário não simétrico (um é negação, outro é positivo) e ambíguo ("Novo" sugere temporalidade que a V2 não pressupõe). Princípio C.5 rejeita inventar `valor_b=0` para dar conta da matemática quando não há dado — viola "TabloFlow analisa sobre o dado informado, nunca decide por ele".

**Decisão:** Revogar D-001. Adotar **vocabulário dual** (técnico no contrato + humano na exibição):

| Contrato técnico | Exibição ao usuário |
|---|---|
| `AUSENTE_ORIGEM` | "Apareceu no Comparado" |
| `AUSENTE_COMPARADO` | "Saiu / Não está no Comparado" |
| `PRESENTE_AMBOS` | (omitido — caso normal) |

Para AUSENTE_*: `valor_origem` ou `valor_comparado` = `None` (não 0); `diferenca` = `None`; `variacao_percentual` = `None`. **Outer join obrigatório** preserva todos os registros.

**Variação percentual em PRESENTE_AMBOS** (fechando ambiguidade da 2.3.7 do prévio):
- Origem ≠ 0 → calcula
- Origem = 0 e Comparado ≠ 0 → `None` + emite **W-V2-BZ** (Base Zero, novo warning)
- Ambos = 0 → 0.0

**Warning W06 antiga renomeada para W-V2-EST** — contagem de registros AUSENTE_* no Diagnóstico, com lista detalhada por agrupador.

**Razão:** Contrato precisa ser estável e neutro para sustentar 10 visões da Fundação; exibição precisa ser de negócio. Separação contrato/exibição já é regra em outros pontos (Origem/Comparado vs "Comparar de"/"Comparar com"). Vocabulário simétrico funciona para qualquer par de estados (Orçado/Realizado, Antes/Depois, Meta/Resultado), não só "Antes/Depois". Reverter D-001 (None em vez de 0/-100%) honra C.5: colocar 0 onde não há dado **inventa valor** — exatamente o que C.5 proíbe. None preserva o fato: "não havia dado para calcular".

**Impacto:**
- D-001 vira "Revogada por D-022"
- Contrato `classificacao_estrutural` ganha 3 categorias (PRESENTE_AMBOS, AUSENTE_ORIGEM, AUSENTE_COMPARADO)
- 2 warnings novos: W-V2-EST (substitui W06), W-V2-BZ (novo)
- Lógica do motor: outer join obrigatório + classificação por presença
- DCV-V2 §4.1, §4.2, §4.3 documentam o tratamento
- Princípio "vocabulário dual técnico/exibição" reforçado como padrão consolidado

**Referência canônica:** DCV-V2 §4.1, §4.2, §4.3

---

### D-021 — Inconsistência estrutural Origem×Comparado: fronteira leve vs estrutural (transversal)
**Data:** 2026-04-18 · **Bloco:** DCV-V2 (Sessão 1) · **Status:** Fechada

**Contexto:** O DCV prévio da V2 (P0.3 + 2.3.8) definia: "sistema executa → ajusta com estratégia segura → registra → evidencia" para inconsistências estruturais. Exemplo dado: Origem agrupado em Produto, Comparado em Produto+Filial → motor "consolida para o nível comum" sem perguntar. Esse padrão **viola Princípio C.5**: a decisão analítica (qual nível consolidar) acontece silenciosamente antes de o usuário poder reverter sem refazer a análise. Diagnóstico pós-execução é tarde demais — decisão importante aconteceu no momento errado (configuração) e foi revelada no momento errado (depois). Mas regra de "sempre perguntar" criaria atrito UX excessivo para casos triviais.

**Decisão:** Distinguir dois tipos de inconsistência com tratamento diferente. Decisão **transversal** — propaga para qualquer visão que receba múltiplas fontes ou faça consolidação cruzada (Família A é principal sentidora; outras famílias herdam quando aplicável).

**Inconsistências leves** (4 casos taxativos, motor ajusta sem perguntar + registra como `AJUSTE_LEVE`):
1. Diferença de ordem de colunas
2. Espaços, acentos ou case diferente em nomes/valores quando conteúdo é idêntico após normalização
3. Tipos numéricos compatíveis (int/float, mesma escala)
4. Linhas em branco ou nulos isolados em coluna

**Inconsistências estruturais** (tudo o mais — motor para no fim da E4 e abre painel de resolução com opções específicas):
- Nível de agrupamento diferente (exemplo do prévio)
- Coluna presente em uma base e ausente na outra
- Tipo de campo incompatível (texto vs numérico)
- Valor único da coluna discriminadora divergente
- Ordem de magnitude radicalmente diferente entre estados

Usuário escolhe → escolha vai para Aba 4 Parâmetros como configuração explícita → motor executa → Diagnóstico registra como `DECISAO_USUARIO`.

**Padrão "ajusta cedo, evidencia tarde" abolido** para a V2 e para toda a Fundação por C.5.

**Razão:** C.5 não diz "sistema sempre pergunta" — diz "sistema apresenta o caso em vez de decidir silenciosamente". Os 4 casos leves são transformações **sem decisão analítica** (não há outra resposta plausível, motor consolidando é exatamente o que o usuário esperaria). Os casos estruturais envolvem **escolha entre alternativas analíticas válidas** — exatamente onde C.5 diz "apresenta, não decide". Lista taxativa evita discussão por caso na Spec e na implementação. Cenário não listado entra como estrutural por default (princípio da prudência alinhado a C.5).

**Impacto:**
- DCV-V2 §5.5 documenta a fronteira
- T-DIAG (Fundação) ganha categorias `AJUSTE_LEVE` e `DECISAO_USUARIO` no Diagnóstico
- Bloco intermediário entre E4 e E5 da V2 (D-029) é onde a resolução acontece
- Padrão herdável por outras visões com consolidação cruzada
- Substitui o padrão do prévio P0.3 + 2.3.8 ("ajusta cedo, evidencia tarde")

**Referência canônica:** DCV-V2 §5.5 · CONTEXT §9 Camada C (Princípio C.5 reforçado)

---

### D-020 — Kit de encerramento entrega arquivos prontos, não instruções de edição
**Data:** 2026-04-18 · **Bloco:** DCV-V1 (Sessão 2) · **Status:** Fechada

**Contexto:** A Sessão 2 da Fase 0 (refino do DCV-V1) produziu três decisões transversais (D-017, D-018, D-019) mais um DCV completo, gerando kit de encerramento com múltiplos ajustes simultâneos em CONTEXT.md, DECISIONS.md, GLOSSARIO.md, Instruções do Projeto e planilha. O modelo vigente do kit entregava **instruções de edição** ("adicionar tal seção no CONTEXT §6", "colar tal entrada no topo de DECISIONS", "alterar tal célula da planilha"). A Usuária identificou que aplicar múltiplas edições manuais em múltiplos arquivos longos, sessão após sessão, aumenta probabilidade de erro de transcrição acumulativo — uma célula atualizada errada, uma seção colada no lugar errado, uma entrada esquecida. O risco é real e cresce com a quantidade de sessões. O episódio imediatamente anterior (planilha antiga em vez da planilha reestruturada) concretizou o risco: o Arquiteto operou sobre modelo desatualizado porque o painel do Projects não continha a última versão substituída.

**Decisão:** O kit de encerramento de toda sessão que gerar decisão, artefato ou mudança de estado entrega **os arquivos canônicos atualizados como artefatos prontos para download**, não mais como instruções de edição. Os 8 itens do ritual passam a ser:

| Item | Formato novo |
|---|---|
| 1. DECISIONS.md atualizado | arquivo .md completo pronto para substituir no painel |
| 2. CONTEXT.md atualizado | arquivo .md completo pronto para substituir no painel |
| 3. Instruções do Projeto atualizadas | arquivo .md completo pronto para substituir no painel |
| 4. Planilha atualizada | arquivo .xlsx completo pronto para substituir no painel |
| 5. Artefato produzido na sessão | arquivo(s) específico(s) — DCV, spec, base, prompt (já era assim) |
| 6. GLOSSARIO.md atualizado | arquivo .md completo pronto para substituir no painel |
| 7. Prompt de abertura da próxima conversa | texto inline (não é arquivo, é para colar) |
| 8. Ordem de aplicação | simplificada: baixar todos → substituir de uma vez no painel |

**Condição operacional:** para produzir os arquivos completos, o Arquiteto precisa das **últimas versões anexadas** no painel do Projects no início da sessão. Se faltar alguma, pede antes de começar o ritual de abertura (reforço do ritual existente).

**Razão:**
1. **Elimina risco cumulativo de erro de transcrição.** Arquivo completo ou está certo ou não está — não há edição parcial que possa falhar silenciosamente em uma linha entre centenas.
2. **Acelera o fechamento da sessão para a Usuária.** Antes: ler 8 blocos de instruções + aplicar em 5 arquivos diferentes. Depois: baixar 5 arquivos + substituir no painel.
3. **Torna o painel do Projects espelho fiel do kit.** Qualquer sessão posterior abre o ritual de abertura lendo os arquivos canônicos e encontra o estado consolidado pelo kit anterior — sem depender de edições manuais intermediárias da Usuária.
4. **Dá ao Arquiteto responsabilidade total pela coerência.** Se uma seção do CONTEXT depende de uma entrada nova do GLOSSARIO que depende de uma nova decisão D-XXX, o Arquiteto garante essa coerência no momento de produzir os arquivos — em vez de terceirizar para a Usuária executar 3 edições em 3 arquivos diferentes sem errar.

Alternativas consideradas e descartadas:
- **Manter instruções e acrescentar validação automatizada** — rejeitada: adiciona complexidade sem resolver a causa-raiz (edição manual em arquivos longos).
- **Entregar arquivos apenas quando a sessão for "grande"** — rejeitada: critério subjetivo ("grande") que na prática seria aplicado de forma inconsistente. Regra única é mais simples.

**Impacto:**
- **Instruções do Projeto** §Ritual de encerramento de conversa reescrita incorporando o novo formato.
- **CONTEXT.md** §11 (Ritual de encerramento de sessão) atualizado para refletir o padrão novo.
- **Esta Sessão 2 já aplica o padrão retroativamente** — o kit entregue nesta sessão usa arquivos prontos, substituindo a entrega anterior feita como instruções.
- **Todas as sessões futuras** seguem este padrão. Ritual de abertura ganha verificação explícita de que as últimas versões dos documentos canônicos estão no painel.

**Referência canônica:** Instruções do Projeto §Ritual de encerramento · CONTEXT.md §11

---
### D-019 — Padrão de condução do Arquiteto formalizado pela Sessão 2
**Data:** 2026-04-18 · **Bloco:** DCV-V1 (Sessão 2) · **Status:** Fechada

**Contexto:** Ao fim da Sessão 2 da Fase 0, a Usuária observou explicitamente que o padrão de condução do Arquiteto durante o refino da V1 era o comportamento esperado em todas as sessões futuras de DCV. O padrão não estava registrado formalmente; a Sessão 2 materializou-o na prática. Esta decisão formaliza o padrão para que sessões subsequentes (DCV-V2, DCV-V4, DCV-V10, DCV-V3, DCV-V8, DCV-V7, DCV-V9, DCV-V5, DCV-V6, e DCVs de operações do Módulo 2) adotem o mesmo ritmo e qualidade.

**Decisão:** Registrar como padrão de condução do Arquiteto em sessões de DCV-VN os seguintes elementos, validados pela Usuária na Sessão 2:

1. **Validação de estado explícita na abertura** — ler os 4 documentos canônicos + DCV prévio + eventuais parciais; reportar diagnóstico de coerência entre fontes; confirmar próximo passo operacional antes de agir.
2. **Fila racionalizada de pendências** — propor ordem de tratamento com racional (quais primeiro, por quê), não tratar pendências em ordem alfabética ou numérica cega.
3. **Uma pendência por vez, com opções explícitas** — cada pendência apresentada com (a) problema contextualizado, (b) aplicação do Princípio C.5, (c) 2 a 4 opções nomeadas, (d) trade-offs de cada uma, (e) recomendação com razões, (f) comportamento definido concreto.
4. **Aplicação sistemática do Princípio C.5** como primeira lente de cada pendência. Revelou-se decisiva em P-V1-05, P-V1-06, P-V1-09, P-V1-10 e na revisão de P-V1-02.
5. **Confirmação da Usuária antes de avançar** — cada pendência fecha com pergunta explícita e próxima pendência só inicia após confirmação.
6. **Mini status-check a cada 3 pendências fechadas** — resumo do que foi decidido, coerência entre decisões, fila restante.
7. **Abertura para correção de enquadramento pela Usuária** — quando a Usuária apontar que a lente do Arquiteto está errada, o Arquiteto reformula sem defensividade e ajusta decisões afetadas em cadeia.
8. **Proativa identificação de decisões transversais** — quando uma pendência da visão revela padrão aplicável a outras visões, o Arquiteto explicita e propõe como decisão transversal (D-XXX).
9. **Identificação do momento de fechamento** — ao perceber que pendências estruturais estão fechadas, o Arquiteto oferece o kit de encerramento proativamente.
10. **Produção do DCV final em prosa como último ato da sessão** quando há tempo; como entregável da próxima sessão quando não há.

**Razão:** A Usuária sinalizou explicitamente: "gerar esse padrão de comportamento esperado que vc teve quanto a condução — É assim que vejo que evoluímos". Formalizar calibra expectativas para sessões futuras, reduz variância entre sessões diferentes (cada conversa é "novo Arquiteto" sem memória), serve como critério de autoavaliação do Arquiteto e como critério da Usuária para apontar desvios.

**Impacto:**
- **Instruções do Projeto** ganham seção "Padrão de condução em sessões de DCV" referenciando D-019.
- **GLOSSARIO.md** ganha entrada "Padrão de condução DCV" na seção de convenções.
- Aplica-se especificamente a sessões DCV-VN e DCV-OPN. Outros tipos de bloco (G-FUND, F-*, S-VN, B-VN, V-VN, A-VN) terão padrões próprios formalizados em suas primeiras execuções.

**Referência canônica:** Instruções do Projeto §Padrão de condução em sessões de DCV

---
### D-018 — T-DUAL: novo transversal (motor_upload em modo dual)
**Data:** 2026-04-18 · **Bloco:** DCV-V1 (Sessão 1) · **Status:** Fechada

**Contexto:** O DCV-V1 é o primeiro e único do Módulo 1 a exigir que o `motor_upload` aceite dois arquivos simultâneos OU um arquivo com pareamento de duas abas. As outras 9 visões operam sobre uma única base consolidada. Essa necessidade emergiu ao fechar P-V1-01 (fontes de entrada da V1) na Sessão 1 da Fase 0.

**Decisão:** Criar novo transversal **T-DUAL** na Fundação — extensão do `motor_upload` que aceita duas estruturas de entrada:
- **Estrutura A**: dois arquivos distintos; usuário escolhe uma aba de cada
- **Estrutura B**: um único arquivo; usuário escolhe duas abas

Ambas produzem um `UploadResult` com referência aos dois lados nomeados (Origem/Comparado ou rótulos editados pelo usuário).

**Razão:** A V1 precisa do modo dual; nenhuma outra visão precisa. Implementar como extensão do `motor_upload` (em vez de motor separado) reaproveita toda a infraestrutura de leitura, detecção de abas, inferência de tipos e diagnóstico. A única lógica nova é o **pareamento** de Origem/Comparado — que é pequena e localizada.

**Impacto:**
- **CONTEXT.md §6** — tabela de transversais ganha linha T-DUAL, marcada como "Usado por: V1".
- **Bloco G-FUND** — escopo do `motor_upload` v2 incorpora T-DUAL como contrato obrigatório.
- **Bloco F-MOT** — implementação contempla T-DUAL junto com a reescrita do `motor_upload`.
- **GLOSSARIO.md** — nova entrada para T-DUAL.

**Fora de escopo da V1/T-DUAL:** estrutura de dados empilhados em uma única aba com coluna discriminadora. Este cenário exige RESHAPE prévio no Módulo 2 e não é suportado pela V1.

**Referência canônica:** `CONTEXT.md` §6 (T-DUAL) · DCV-V1 §3.1 · escopo do F-MOT

---
### D-017 — Diagnóstico sempre como última aba em todas as visões
**Data:** 2026-04-18 · **Bloco:** DCV-V1 (Sessão 2) · **Status:** Fechada

**Contexto:** Durante o refino de L-V1-B (forma da aba de Diagnóstico) na Sessão 2 da Fase 0, o Arquiteto propôs inicialmente que o Diagnóstico da V1 ficasse em **posição 2** do Excel (logo após o Resumo Executivo), com racional de "auditor precisa validar confiabilidade antes de consumir resultado". A Usuária corrigiu o enquadramento: a decisão de posição do Diagnóstico é **transversal a todas as 10 visões**, não específica da V1. O raciocínio de que o usuário consome resultado primeiro e valida processo depois se aplica a qualquer análise do TabloFlow, não só à conciliação.

**Decisão:** O **Diagnóstico é sempre a última aba do Excel exportado**, em todas as 10 visões do Módulo 1 e nas operações do Módulo 2 quando aplicável. Regra transversal aplicada pelo **transversal T-DIAG** (CONTEXT §6) e formalizada como requisito do **bloco F-EXP** (exportação Excel padrão) da Fase 1 · Fundação.

**Razão:** O Diagnóstico cumpre função de auditoria e validação do processamento — é artefato de "caixa-preta aberta" para o usuário que precisa investigar. O fluxo natural de leitura em qualquer análise é: resultado primeiro (para entender o quê), validação depois (para confirmar o como). Colocar Diagnóstico em posição inicial induz leitura invertida que raramente é a desejada, inclusive em auditoria — o auditor ainda prefere ver os números e só abrir o Diagnóstico quando encontra algo a investigar.

Alternativa considerada e descartada:
- **Diagnóstico em posição 2 para auditoria e posição final para outras visões** — rejeitada por inconsistência: usuária que alterna entre visões do TabloFlow aprende padrão de navegação, e padrão inconsistente aumenta atrito cognitivo. Regra única simplifica.

**Impacto:**
- **CONTEXT.md §6** — linha do T-DIAG ganha cláusula adicional: "Aba sempre posicionada como última aba por regra transversal."
- **Bloco F-EXP da Fase 1** — requisito formalizado na definição da exportação Excel padrão.
- **DCV-V1 §6.1** — estrutura de abas do Excel da V1 reflete Diagnóstico como aba final.
- **GLOSSARIO.md** — entrada de T-DIAG atualizada.
- **Próximos DCVs** (V2, V3, V4, V5, V6, V7, V8, V9, V10) — devem respeitar este padrão sem necessidade de redecisão.
- **Operações do Módulo 2** — regra aplica-se quando produzirem Excel com diagnóstico.

**Referência canônica:** `CONTEXT.md` §6 (T-DIAG) · DCV-V1 §6.1 e §10.1 · escopo do F-EXP

---
### D-016 — Unidade de bloco de DCV = visão (não família)
**Data:** 2026-04-18 · **Bloco:** DCV-V1 (parcial) · **Status:** Fechada

**Contexto:** A aba "2. Fase 0 · DCVs" da planilha v2 (pós-D-014) havia proposto "unidade de bloco = família" como hipótese experimental — refinar DCV-V2 e DCV-V1 juntos em uma sessão, na ideia de que a mãe conceitual (V2) e a irmã (V1) da Família A compartilhariam vocabulário e caberiam em uma sessão. A Sessão 1 da Fase 0 iniciou aplicando essa hipótese, com V1 refinada primeiro (por ter pré-requisitos de motor_upload — modo dual — que convém antecipar).

Durante o refino do DCV-V1, a sessão produziu ganho metodológico significativo não previsto: promoção de padrões visuais/UX do Figma Make a diretrizes oficiais (D-015) e formalização do princípio C.5 (TabloFlow analisa, não decide). Isso consumiu ciclo de sessão que seria do refino puro, demonstrando empiricamente que uma sessão de DCV não cabe uma família inteira quando há emergência de decisão de método acontecendo em paralelo.

**Decisão:** Unidade de bloco de DCV = **uma visão**. A hipótese "unidade = família" é revogada antes da primeira sessão completar porque a evidência empírica mostrou inviabilidade. Refino de V2 e V1 exige duas sessões separadas. Aplica-se a todas as famílias conceituais do Módulo 1 — V4+V10 (Família C), V3+V8 (Família B), V7+V9 (Família D), V5+V6 (Família E) também serão refinadas em sessões individuais.

**Razão:** Três motivos convergiram:
1. **Densidade natural do DCV.** Cada DCV tem 8-15 pendências estruturais quando se aplica o padrão TabloFlow com rigor. Dobrar isso em uma sessão ultrapassa a janela de concentração da Usuária e de qualidade do Arquiteto.
2. **Emergência de decisão de método.** Conforme o Arquiteto refina o primeiro DCV, descobertas estruturais (como o reset conceitual de C.5) emergem e precisam ser registradas antes de propagar para o segundo DCV. Fazer os dois em paralelo aumenta risco de aplicar no segundo DCV uma lente que ainda não está estável.
3. **Alinhamento com princípio B.1.** O CONTEXT já diz "um bloco por sessão". "Bloco = família" forçaria exceção a B.1 que a prática mostrou ser desnecessária.

Alternativas consideradas:
- **Manter "unidade = família" e apenas reservar sessões mais longas** — rejeitada porque a Usuária sinalizou fadiga de decisão como risco real, e o Arquiteto também perde qualidade.
- **Unidade = família quando as visões são muito acopladas** — rejeitada por introduzir critério subjetivo que na prática ninguém aplicaria de forma consistente.

**Impacto:**
- CONTEXT v2 §3 (Fase 2) já diz "para cada visão N, cinco artefatos sequenciais". A Fase 0 passa a seguir a mesma lógica: para cada visão N, um bloco DCV-VN. A redação já está compatível — não precisa edição do CONTEXT.
- Planilha v2 aba "2. Fase 0 · DCVs": ajustar linha de próximo passo operacional para refletir "DCV-V1 (continuação) em sessão 2; DCV-V2 em sessão 3". O texto da sessão 1 que mencionava "refino conjunto" precisa ser atualizado para "refino individual por visão, testando família A como piloto — família mostrou não caber em uma sessão".
- Ordem de refino dentro da Família A: V1 primeiro, V2 depois. Ordem baseada em racional da Usuária: V1 antecipa requisitos de motor_upload (modo dual) que entrarão no G-FUND. Ordem de **implementação** na Fase 2 permanece V2→V1 conforme CONTEXT §3 (racional: V2 é mais simples no código, V1 herda vocabulário). Ordem de compreensão ≠ ordem de implementação — registrado também como nuance.
- Famílias seguintes (C, B, D, E) serão refinadas com mesma lógica: uma sessão por DCV.

**Referência canônica:** CONTEXT v2 §3 (Fase 0) · planilha v2 aba "2. Fase 0 · DCVs"

### D-015 — Padrões visuais/UX do Figma Make: Camada A (método) × Camada B (sugestão)
**Data:** 2026-04-18 · **Bloco:** DCV-V1 (parcial) · **Status:** Fechada

**Contexto:** Durante a Sessão 1 da Fase 0, a Usuária compartilhou o arquivo `DCV_PREVIO_M1_V1_FIGMA.md`, consolidando dois documentos internos do wireframe navegável da V1 produzido no Figma Make: `PADRAO_IA_TABLOFLOW.md` (padrão visual/funcional das sugestões de IA) e `TEMPLATE_PROMPT_VISOES.md` (template para gerar wireframes das outras visões mantendo consistência). Esses arquivos descrevem elementos que o Arquiteto inicialmente interpretou como "diretrizes oficiais": botão "Objetivo da Visão" com 4 seções expansíveis, stepper progress, accordion progressivo, sistema de Modelos Salvos, sistema de Sugestões de IA com padrão visual roxo-azul, paleta de cores semântica (verde/laranja/azul/vermelho/slate).

O Arquiteto propôs inicialmente promover todos esses elementos a diretrizes vinculantes no CONTEXT, o que teria antecipado Fase 3 (IA) e Frente A (Identidade Visual) — ambas parqueadas — e expandido significativamente o escopo da Fundação.

A Usuária corrigiu o enquadramento, distinguindo: existem **padrões estruturais do produto** (coisas que todas as 10 visões vão oferecer por serem características do TabloFlow) e **sugestões visuais** (cores, gradientes, componentes shadcn, copywriting específico — que são propostas a avaliar quando Fase 3 e Frente A forem executadas).

**Decisão:** Separação formal em duas camadas:

**Camada A — Padrões estruturais de produto (entram no método TabloFlow):**

Três elementos são promovidos a característica obrigatória de toda visão do Módulo 1:
1. **"Objetivo da Visão"** — bloco de ajuda contextual em cada visão, explicando ao usuário o que a visão faz, quando usar, o que vai obter e como funciona. É parte do produto.
2. **Fluxo de etapas progressivas** — cada visão tem sequência de etapas com dependência (etapa N só abre quando N-1 fecha), e permite voltar para editar etapa anterior com aviso de impacto nas seguintes.
3. **Salvar modelo de configuração** — toda visão permite ao usuário salvar a configuração aplicada como modelo reutilizável, e aplicar modelo salvo em novo uso.

Registrados no CONTEXT v2 como novo §13 "Padrões estruturais de produto entre visões" (redação completa no Item 2 do kit). Registro é **neutro em tecnologia, linguagem visual e componente** — descreve o que o produto oferece, não como aparece na tela.

Novo transversal adicionado ao escopo do G-FUND: **T-MODELO** (contrato de salvar/aplicar modelo de configuração). Os demais elementos são comportamento de UI e ficam na Spec de cada visão (Fase 2).

**Camada B — Sugestões visuais (ficam como referência, não vinculam):**

Os seguintes elementos do Figma Make ficam registrados como **referência navegável autorizada do wireframe V1**, sem vincular o método:
- Paleta de cores específica (roxo-azul IA, verde sucesso, laranja atenção, azul info, vermelho erro, slate neutro)
- Componentes shadcn escolhidos
- Copywriting específico
- Gradientes, ícones Sparkles
- Stepper horizontal com check verde
- Layout de cards brancos com bordas coloridas

Esses ficam no wireframe referenciado no DCV-V1. Quando Fase 3 (IA) e Frente A (Identidade Visual) forem executadas — ambas parqueadas no método — poderão adotar integralmente, parcialmente ou substituir essas sugestões.

**Camada C (clareza adicional) — Fase 3 e Frente A seguem parqueadas:**

- **Sistema de Sugestões de IA** (UX e lógica da camada IA) continua em Fase 3 · `⬜ Não iniciado`. O DCV-V1 apenas registra "a IA, quando vier, opera a partir do contrato estrutural declarado pelo usuário na Etapa 1 (arquivos + abas + nomes Origem/Comparado)".
- **Paleta canônica e identidade visual** continuam em Frente A · `⚠️ Em andamento`.

**Razão:** A correção da Usuária evita três erros estruturais que o Arquiteto estava prestes a cometer:
1. Antecipar Fase 3 sem método, introduzindo decisão de UX de IA fora de contexto adequado.
2. Antecipar Frente A, cristalizando paleta de cores que ainda não foi validada pela identidade primária.
3. Inflar o escopo da Fundação com 3 transversais (T-MODELO, T-UISTATE, T-IA-HINTS) quando apenas um (T-MODELO) é realmente transversal de dado, e os outros dois são comportamento de UI que pertence à Spec de cada visão.

A separação A/B/C preserva o que é real padrão de produto (3 elementos) e descarta o que é só sugestão visual estética (cores, componentes, copy específico).

**Impacto:**
- CONTEXT v2 ganha §13 "Padrões estruturais de produto entre visões" (redação no Item 2)
- Escopo do G-FUND (Fase 1) ganha T-MODELO como transversal novo. Escopo de transversais atualizado em CONTEXT §6 e planilha aba "4. Motores e Transversais"
- GLOSSARIO ganha entradas: "Objetivo da Visão", "Fluxo de etapas progressivas", "Modelo de configuração", "Wireframe Figma V1 (referência)", "T-MODELO"
- Arquivos `PADRAO_IA_TABLOFLOW.md` e `TEMPLATE_PROMPT_VISOES.md` ficam fora do repositório do projeto — permanecem no Figma Make como referência do wireframe. Não há criação de `/docs/padroes/` como o Arquiteto chegou a considerar.
- Fase 3 e Frente A permanecem com status atual na planilha (sem mudança).

**Referência canônica:** CONTEXT v2 §13 (novo) · GLOSSARIO §"Padrões estruturais do produto" (novo) · planilha v2 aba "4. Motores e Transversais" (T-MODELO adicionado)

### D-014 — Reforma do método pós-DCVs do Módulo 1: três fases, Fundação única, ordem por famílias
**Data:** 2026-04-18 · **Bloco:** (decisão de método, sem bloco Claude Code) · **Status:** Fechada

**Contexto:** Entre 17 e 18 de abril de 2026, a Usuária produziu — com apoio do ChatGPT como analista técnico (D-012) — os 10 DCVs prévios do Módulo 1 (V1 a V10). Ao revisar o conjunto completo pela primeira vez, três problemas estruturais do método anterior ficaram evidentes:

1. **A "onda padrão" (V2, V4, V7, V6, V10) herdada do planejamento estratégico não refletia dependência lógica entre visões.** Era uma escolha de priorização de valor de negócio, não de sequência técnica. A leitura consolidada dos 10 DCVs revelou que as visões se agrupam em **5 famílias conceituais** (Confronto, Sequência, Composição, Posição relativa, Estrutura interna), e que dentro de cada família há uma visão "mãe" e uma "irmã" — construir a mãe primeiro economiza trabalho na irmã. A ordem por famílias emergiu como mais barata que a ordem por prioridade.

2. **Os motores atuais (`motor_upload`, `motor_base`), já em auditoria pela D-013, claramente não servem aos requisitos consolidados dos 10 DCVs.** Eles foram construídos para a V2 antiga (hoje em `/legacy/`) e não cobrem: consolidação configurável pré-análise com regra de agregação (exigida por V2, V3, V4, V6, V7, V8, V9, V10), pivot automático POR_LINHAS → POR_COLUNAS (V2, V3, V4), eixo sequencial ordenado com intervalo De/Até (V3, V8), classificação categórica semântica para uso como eixo (V6, V7), e diagnóstico estrutural obrigatório padronizado (todos). O bloco `G-MOT` previsto pela D-011 assumia "auditoria que pode ou não exigir reescrita"; a realidade é que a reescrita é certa.

3. **Havia ambiguidade estrutural sobre onde viviam decisões de UX.** A Spec antiga carregava contratos Pydantic e regras de cálculo, mas deixava UX implícita — o que gerava descoberta tardia de lacunas apenas no app Streamlit, quando era caro mudar. Vários DCVs (notadamente V3 e V8) já traziam descrição de fluxo de tela embutida, mas sem padrão. A Usuária propôs uma etapa explícita de "UX estrutural" antes do código.

**Decisão:** Reforma estrutural do método em quatro eixos:

**Eixo 1 — Três fases sequenciais substituem a noção de "ondas".**
- **Fase 0 · Compreensão** — produzir os 10 DCVs aprovados. Mantém o fluxo 3 etapas da D-012 (Usuária + ChatGPT → Arquiteto refina → Usuária aprova).
- **Fase 1 · Fundação** — consolidar, especificar e implementar motores + contratos + transversais + exportação Excel padrão, a partir dos requisitos unificados dos 10 DCVs. Substitui e amplia o escopo do antigo `G-MOT`.
- **Fase 2 · Visões** — implementar as 10 visões sobre a Fundação aprovada, na ordem lógica por famílias.

Nenhuma fase inicia sem a anterior estar 100% completa.

**Eixo 2 — Ordem de implementação das visões por famílias conceituais** (substitui a "onda padrão"):
1. Família A · Confronto → V2, V1
2. Família C · Composição → V4, V10
3. Família B · Sequência → V3, V8
4. Família D · Posição relativa → V7, V9
5. Família E · Estrutura interna → V5, V6

Racional: começar pela família cuja "mãe" é mais simples, e pela família que produz transversais reutilizáveis (T-AGRUPA, T-DIAG, T-PIVOT saem da Família A; T-ABC, T-ACUM, T-RANK saem da Família C; T-EIXO sai da Família B).

**Eixo 3 — Esqueleto de tela vira seção obrigatória da Spec, não bloco separado.** Toda Spec passa a ter três seções fixas: (a) contratos lógicos, (b) regras de cálculo, (c) esqueleto de tela. A Usuária avaliou essa abordagem mais barata que criar um bloco `EV-N` separado, porque (i) vários DCVs já trazem material para o esqueleto, (ii) mantém contrato e UX no mesmo documento auditável, (iii) reduz pontos de parada no fluxo.

**Eixo 4 — Consolidação documental limpa, histórico preservado em DECISIONS.**
- `CONTEXT.md` reescrito do zero: 14 regras numeradas acumuladas viram 10 princípios em 3 camadas (método, artefato, operação). Versão anterior preservada em `/legacy/context_v1.md`.
- `GLOSSARIO.md` reescrito refletindo o vocabulário novo. Termos descontinuados (B-NR, V-Nb, N-Motores, onda padrão, N-VN, V-0c, G-MOT) ficam como nota histórica curta, com referência à decisão que os descontinuou.
- Planilha reestruturada com colunas refletindo as 3 fases; linhas de visões na ordem por famílias; abas Motores/Transversais/Glossário atualizadas.
- Instruções do Projeto reescritas do zero em paralelo ao CONTEXT v2.
- `DECISIONS.md` **preservado integralmente** — D-001 a D-013 mantêm seu valor histórico e ficam abaixo desta entrada.

**Razão:** As três descobertas (ordem errada, motores inservíveis, UX órfã) compartilham uma causa comum: o método anterior evoluiu por emenda em vez de por revisão estrutural. Toda vez que um problema aparecia, uma regra nova era adicionada ao CONTEXT — acumulamos 14 regras, vários tipos de bloco descontinuados, uma "onda padrão" que perdeu função. O custo de continuar emendando é maior que o custo de reescrever o método agora, porque os 10 DCVs prontos dão pela primeira vez visibilidade consolidada sobre tudo que precisa existir. Adiar a reforma significaria construir a Fase 1 sobre um método que já sabemos que não serve — exatamente o erro que a D-011 e a D-013 já corrigiram em contextos menores.

Alternativas consideradas e descartadas:
- **Preservar as 14 regras e apenas adicionar as novas** — rejeitada porque o objetivo é sair do acúmulo, não aumentá-lo (Opção B escolhida pela Usuária).
- **Implementar V2 sobre motores atuais e reescrever motores depois** — rejeitada porque produziria retrabalho certo em V2 quando os motores forem reescritos.
- **Criar bloco "EV-N" separado para esqueleto de tela** — rejeitada pela Usuária: adiciona parada no fluxo e separa UX de contrato que deveriam nascer juntos.

**Impacto:**

*Artefatos novos:*
- `CONTEXT.md` v2 (este documento substitui completamente o anterior)
- `GLOSSARIO.md` v2
- `TabloFlow_Estado_do_Projeto.xlsx` v2 (estrutura reorganizada por fases)
- Instruções do Projeto v2 (no painel do Projects)

*Artefatos preservados em `/legacy/`:*
- `context_v1.md` (CONTEXT anterior à D-014)
- `glossario_v1.md` (GLOSSARIO anterior à D-014)
- Artefatos pré-DCV já movidos por D-009 e D-013

*Artefatos que permanecem inalterados:*
- `DECISIONS.md` — apenas ganha esta entrada no topo. D-001 a D-013 permanecem íntegros.
- Os 10 DCVs prévios em `/specs/dcv/` — são insumo para o refino pelo Arquiteto na Fase 0, não são substituídos.

*Nomenclatura de blocos:*
- Novos: `G-FUND`, `F-MOT`, `F-TRANS`, `F-EXP`, `F-BASE`, `S-VN`, `B-VN`, `V-VN`, `A-VN`
- Descontinuados (apenas para leitura de histórico): `B-NR`, `V-Nb`, `N-Motores`, `G-MOT`, `N-VN`, `V-0c`, `T-XXX` (este último porque transversais agora são identificados no G-FUND e implementados na Fase 1, não extraídos tardiamente)

*Decisões anteriores que permanecem válidas mas operam sob o método novo:*
- D-001 a D-004 (decisões de comportamento da V2) — ficam como **diretrizes a serem incorporadas** no DCV-V2 aprovado e na spec_v2 produzida na Fase 2.
- D-006 (Gamma descontinuado como gerador) — ampliada: Gamma agora é ferramenta de formatação de documento apresentável final; nunca gera artefato técnico.
- D-007, D-008 (correções de motor_base) — historicamente relevantes. Na prática, o motor novo da Fase 1 não herda o código atual; herda o aprendizado (inferência semântica de boolean disfarçado, necessidade de `arquivo_bytes` no UploadResult) como requisito a cobrir.
- D-009, D-013 (artefatos movidos para /legacy/) — permanecem. `/legacy/` continua sendo a pasta-arquivo do projeto.
- D-010 (regeneração planejada de base_v2) — absorvida: base_v2 será gerada do zero na Fase 2 via bloco `B-V2` a partir do DCV-V2 aprovado e da spec_v2.
- D-011 (DCV como etapa obrigatória) — mantida. É princípio A.2 do CONTEXT v2.
- D-012 (ChatGPT como analista técnico prévio) — mantida sem alteração.

**Pendências abertas criadas por esta decisão:**
- Produzir `MODELO_DCV_PREVIO.md` em `/specs/dcv/` (D-012 previu, mas o arquivo ainda não existe formalmente — será necessário para futuros DCVs do Módulo 2).
- Decidir durante F-MOT se V10 é implementada como visão independente ou como preset/modo de V4. Essa decisão virá naturalmente quando chegarmos na Família C da Fase 2, informada pelo DCV-V4 e DCV-V10 já refinados.

**Referência canônica:** `CONTEXT.md` (v2, este repositório) · `TabloFlow_Estado_do_Projeto.xlsx` (v2) · Instruções do Projeto (v2, painel do Projects)

---

### D-013 — V2 movida para `/legacy/` por aplicação retroativa da Regra 13
**Data:** 2026-04-17 · **Bloco:** (decisão de processo, sem bloco Claude Code) · **Status:** Fechada
**Contexto:** Após adoção do método DCV (D-011) e do fluxo ChatGPT-Arquiteto-Usuária para produção de DCVs (D-012), ficou evidente que manter a V2 em status misto (spec ✅ + base 🔶 + visão 🔶 + app 🔶) era incoerente com a nova diretriz de "começar pelo DCV". A V2 nunca chegou a ter as decisões D-001..D-004 implementadas no código. Manter o legado como base para o trabalho novo (via blocos B-2R "regeneração de base" e V-2b "correção de visão") forçaria o método antigo de "evolução incremental sobre artefato pré-DCV" — exatamente o que o novo método rejeita. A Usuária aplicou retroativamente a mesma lógica da D-009 (que tratou V4, V6, V7) e moveu manualmente todos os artefatos da V2 para `/legacy/`.
**Decisão:** Aplicar à V2 o mesmo tratamento dado a V4/V6/V7 pela D-009. Artefatos `spec_v2.md`, `visao_v2.py`, `app_v2.py`, `base_v2.xlsx` (e quaisquer outros artefatos da V2 ainda em `/specs/`, `/src/`, `/bases/`) movidos para `/legacy/`. A nova V2 será **construída do zero** a partir do DCV-V2 aprovado, seguindo o fluxo padrão pós-DCV. Decisões D-001 a D-004 e D-010 permanecem **válidas como diretrizes** que o DCV-V2 deve incorporar — elas representam trabalho intelectual sobre comportamento, não sobre implementação (que nunca chegou a ser feita).
**Razão:** Coerência com D-009. O método novo (DCV → spec → base → código → app → validação) não admite caminho intermediário "evolutivo" sobre artefato pré-DCV. Tentar tal caminho seria recriar o problema que a D-011 resolveu estruturalmente. Custo de descarte é menor que parece — o trabalho de spec da V2 anterior nunca foi implementado, então não há código a ser perdido. As decisões intelectuais (D-001..D-004, D-010) são preservadas porque foram registradas em DECISIONS.md, não no código.
**Impacto:**
- Pasta `/legacy/` agora contém os artefatos pré-rebaseline de V2 + V4 + V6 + V7 + specs antigas dos motores
- Tipos de bloco `B-NR` (regeneração de base) e `V-Nb` (correção de visão) ficam **descontinuados**: não há mais cenário em que façam sentido no método novo
- Planilha `TabloFlow_Estado_do_Projeto.xlsx`:
  - V2 com todas as 9 colunas (DCV até IA) marcadas como ⬜ Não iniciado, exceto coluna 0. DCV que fica 🟦 Aguardando DCV
  - Próximo Passo Operacional reformulado: B-2R e V-2b removidos da fila; implementação da V2 vira parte do ciclo padrão pós-G-MOT (spec → base → código → app)
  - Aba "5. Glossário" marca B-NR e V-Nb como descontinuados
  - Aba "4. Motores e Transversais": status de código dos motores volta para 🔶 EM AUDITORIA porque serão reauditados no G-MOT contra requisitos consolidados dos DCVs aprovados (não há mais como considerá-los "Concluído" sem essa auditoria)
- DCV-V2 ad-hoc construído na conversa de 17/04/2026 vira **insumo** para o DCV-V2 final (não substitui)
- Fase 0 (Blueprint) muda para ⚠️ Em andamento — diretrizes de produto detalhadas estão sendo produzidas pela Usuária a cada DCV
**Referência canônica:** `/legacy/` (arquivos da V2 movidos para lá) · planilha § Módulo 1 (linha V2) · D-009 (precedente metodológico)

---

### D-012 — ChatGPT como analista técnico prévio para DCVs
**Data:** 2026-04-17 · **Bloco:** (decisão de processo, sem bloco Claude Code) · **Status:** Fechada
**Contexto:** Após aprovação do DCV como etapa zero obrigatória do método (D-011), surgiu a questão de quem produz o **rascunho inicial** de cada DCV. Produzir todos pelo Arquiteto exigiria muitas sessões dedicadas no Projects, com atraso significativo da fila operacional. A Usuária propôs usar ChatGPT como analista técnico de apoio, com ela validando o rascunho antes de encaminhar ao Arquiteto.
**Decisão:** Adotar fluxo em 3 etapas para produção de cada DCV:
1. **Usuária + ChatGPT** produzem o **DCV prévio** (rascunho), usando o template `MODELO_DCV_PREVIO.md` e materiais de produto (Blueprint da visão + diretriz da Usuária)
2. **Arquiteto (Claude no Projects)** recebe o DCV prévio, refina aplicando o método TabloFlow (formato padrão, distinção rigorosa Estado/Agrupador/Filtro, contratos Pydantic identificados, pendências P-NN com opções e trade-offs), devolve **DCV final** em prosa
3. **Usuária aprova** → DCV vira `dcv_vN.md` em `/specs/compreensao/` e a coluna "0. DCV" da planilha vira `✅ Aprovado`
**Razão:** Usar ChatGPT como gerador de rascunho aproveita capacidade técnica da Usuária e reduz carga sobre o Arquiteto, sem violar o método: o Arquiteto continua sendo quem aplica o padrão TabloFlow e quem identifica considerações técnicas que escapam ao analista de apoio. Usuária permanece como ponto de decisão final. Alternativa de "Arquiteto produz tudo do zero" foi rejeitada por gargalo de tempo. Alternativa de "ChatGPT produz e Usuária aprova direto" foi rejeitada por bypassar o filtro técnico do Arquiteto (que conhece o método, motores, decisões anteriores).
**Impacto:**
- Novo arquivo `MODELO_DCV_PREVIO.md` em `/specs/compreensao/` — template usado pela Usuária com o ChatGPT
- Fluxo de cada DCV-VN passa por 3 etapas (prévio → refinado → aprovado), não 1
- Nenhuma alteração em código ou contratos
**Referência canônica:** `/specs/compreensao/MODELO_DCV_PREVIO.md` · D-011 (que define o que é DCV)

---

### D-011 — Adoção do DCV (Documento de Compreensão da Visão) como etapa zero obrigatória
**Data:** 2026-04-17 · **Bloco:** (decisão de processo) · **Status:** Fechada
**Contexto:** Durante o planejamento do Bloco B-2R (regeneração da base_v2.xlsx), a conversa entre Arquiteto e Usuária precisou ser refeita 3 vezes em 5 turnos: a cada documento novo de produto fornecido (Blueprint Gamma → diretriz da Usuária), o desenho da base sintética mudava substancialmente. A Usuária identificou que o método TabloFlow, mesmo com 12 regras estabelecidas, não tinha uma etapa formal de **alinhamento de compreensão da visão antes de qualquer geração de spec/base/código**. Esse mesmo problema havia gerado a V4 "concluída" sem auditoria adequada, levando à decisão D-009 de mover artefatos para `/legacy/` e refazer do zero.
**Decisão:** Criar a etapa **DCV (Documento de Compreensão da Visão)** como pré-requisito obrigatório de qualquer visão. O DCV é um documento curto em prosa, vivendo em `/specs/compreensao/dcv_vN.md`, que captura: (1) o que a visão faz em uma frase de negócio na voz da Usuária, (2) o que a visão precisa receber, (3) o que a visão precisa entregar, (4) pendências enumeradas que precisam de decisão antes de qualquer outra coisa. Sem DCV aprovado pela Usuária, nenhuma outra etapa da visão pode iniciar. Adotada como **Regra 13** do CONTEXT.md. Decisão complementar: novo bloco **G-MOT (Gate de Motores)**, registrado como **Regra 14**, obriga auditoria dos motores contra requisitos consolidados de uma onda de DCVs aprovados antes da implementação de qualquer `visao_vN.py` da onda.
**Razão:** Sem alinhamento de compreensão prévio, o Arquiteto trabalha com uma versão parcial da visão e produz spec/base que parecem corretas mas escondem lacunas — só descobertas em runtime ou em validação visual, gerando ciclos de retrabalho caros. O DCV transforma essa fase de "validação acidental por proposta" em "alinhamento explícito", permitindo que pendências sejam fechadas no nível certo (compreensão) antes de descer para spec (contrato) e código (implementação). Custo estimado por visão: ~30–60 minutos de conversa + 1 sessão de Arquiteto. Ganho: zero ciclos de retrabalho de spec/base. Como o DCV exige antecedência (Cenário C aprovado), permite também que o bloco G-MOT veja todos os requisitos de motor de uma onda completa antes de mexer nos motores — eliminando o risco de motor "frankenstein" construído um remendo por vez.
**Impacto:**
- `CONTEXT.md` ganha **Regra 13** (DCV obrigatório) e **Regra 14** (G-MOT como gate)
- `CONTEXT.md` § 11 (Tipos de bloco) ganha 3 novos: `DCV-VN`, `DCV-OPN`, `G-MOT`
- `CONTEXT.md` § 5 (Fontes de verdade) acrescenta DCVs em `/specs/compreensao/` à hierarquia
- `CONTEXT.md` § 6 (Estrutura de pastas) acrescenta `/specs/compreensao/`
- Planilha `TabloFlow_Estado_do_Projeto.xlsx` ganha:
  - Coluna **"0. DCV"** antes de "1. Spec" nas abas Módulo 1 e Módulo 2
  - Status **🟦 Aguardando DCV** (novo, na Legenda de Status)
  - Aba **"5. Glossário"** (incluindo nomenclatura DCV, G-MOT, etc.)
  - Bloco G-MOT registrado na aba "4. Motores e Transversais"
  - Próximo Passo Operacional reformulado para refletir onda padrão (V2, V4, V7, V6, V10) → G-MOT → implementação
- Novo arquivo na raiz: `GLOSSARIO.md` (versão completa do glossário)
- Bloco antigo `N-Motores` (que estava sem prioridade) é **substituído pelo G-MOT** com escopo claro
- Onda padrão de DCVs definida: **V2, V4, V7, V6, V10** (as 5 primeiras da fila estratégica)
**Referência canônica:** `CONTEXT.md` § 7 (Regras 13 e 14) · `CONTEXT.md` § 11 (novos tipos de bloco) · `/specs/compreensao/` (pasta dos DCVs)

### D-010 — Regeneração planejada de base_v2.xlsx no padrão fundido
**Data:** 2026-04-17 · **Bloco:** (planejamento, antes de bloco formal) · **Status:** Fechada (planejamento) / execução pendente
**Contexto:** Durante organização documental pós-Bloco 8, descoberta da `spec_base_v2.md` (arquivo de 17/04 11:15, gerada pelo Gamma antes do método TabloFlow estar consolidado). Essa spec planejava uma base de volume realista (150–250 linhas por aba, cobertura explícita de W02 e W05, domínio de Vendas corporativas). A `base_v2.xlsx` efetivamente gerada no Bloco B-2 ficou com volume didático (12–16 linhas por aba, sem W02 nem W05), focada em gabarito auditável (30 casos em aba CASOS_ESPERADOS). Após instituída a **Regra 9** (validação exige mínimo 50 linhas), a base atual violaria a regra.
**Decisão:** Regenerar `base_v2.xlsx` **fundindo** o melhor das duas abordagens:
- **Da spec_base_v2 Gamma:** volume 150–250 linhas/aba, cobertura de W02 (cardinalidade alta) e W05 (POR_LINHAS sem par), reprodutibilidade via seed fixa, script gerador versionado
- **Da base_v2.xlsx atual:** aba CASOS_ESPERADOS separada com gabarito auditado, aba README, multi-tipo com PERCENTUAL e INDICE (não só Vendas puro)
- **Incorporar decisões D-001 a D-004** (warnings W06 e W07 que não existiam quando a spec Gamma foi escrita)
Executar antes do Bloco V-2b.
**Razão:** Base subdimensionada esconde bugs de volume na visão (como escondeu no motor_base, origem do V-0c). Rodar V-2b com base atual arrisca validação insuficiente. Regeneração cumpre Regra 9 e incorpora todo o aprendizado pós-B-2.
**Impacto:**
- Nova `specs/spec_base_v2.md` a produzir (a antiga foi movida para `/legacy/spec_base_v2_gamma.md`)
- Novo `bases/gerar_base_v2.py` (script versionado, determinístico)
- `bases/base_v2.xlsx` atual será preservada como `/legacy/base_v2_v1.xlsx` quando a nova for gerada
- Aba CASOS_ESPERADOS da nova base terá volume proporcionalmente maior (mais casos auditados)
**Pendências vinculadas:** execução depende de planejamento da nova spec (em andamento) e aprovação da Usuária antes da geração do arquivo.
**Referência canônica:** este D-010 · nova `specs/spec_base_v2.md` (a produzir)

---

### D-009 — Reset de V4, V6, V7: artefatos legados movidos para /legacy/, serão refeitos do zero
**Data:** 2026-04-17 · **Bloco:** (decisão manual, sem bloco Claude Code) · **Status:** Fechada
**Contexto:** Após o rebaseline do projeto (D-005, D-006) e a identificação de que specs geradas pelo Gamma não seguem o método TabloFlow, decidiu-se que V4, V6 e V7 não seriam reaproveitadas via edição incremental da versão antiga.
**Decisão:** Todos os artefatos legados dessas três visões (`spec_v4.md`, `spec_v6.md`, `spec_v7.md`, `visao_v4.py`, `visao_v6.py`, `visao_v7.py`, `app_v4.py`, `base_v4.csv`) foram movidos para a pasta `/legacy/` na raiz do projeto. Essas visões serão refeitas **do zero** (não evoluídas) em blocos do tipo `N-V[N]`, usando o Blueprint (Gamma) como única fonte estratégica e o `spec_v2.md` + `base_v2.xlsx` como referência de padrão.
**Razão:** Refazer do zero evita que vieses e lacunas da geração antiga se propaguem silenciosamente para a versão nova. Evolução incremental de spec ruim tende a carregar omissões invisíveis, que só aparecem como bug em runtime (exatamente o cenário do Bloco 8). Reconstrução aplica o método TabloFlow desde a linha 1 do novo artefato.
**Impacto:**
- `/legacy/` contém os artefatos pré-rebaseline de V4, V6, V7 + as specs de motores antigas
- `/specs/`, `/src/` e `/bases/` contêm apenas artefatos do método novo
- Planilha reflete "Não iniciado" para V4, V6, V7 em todas as colunas
- Nenhum código em `/src/` depende de `/legacy/`
**Próximos blocos relacionados:**
- N-V4 (após V-2b e regeneração da base_v2) — reescrever spec_v4 + gerar base_v4.xlsx do zero
- N-V7 (depois) — idem
- N-V6 (depois) — idem
- N-Motores (futuro, sem prioridade definida) — reescrever specs dos motores no padrão V2 (código já validado em V-0c)
**Referência canônica:** pasta `/legacy/` · `CONTEXT.md` § 6 (Estrutura de pastas)

---

### D-008 — Inferência semântica reconhece boolean disfarçado em float64
**Data:** 2026-04-17 · **Bloco:** V-0c · **Status:** Fechada
**Contexto:** Ao corrigir o truncamento em motor_base (ver D-007), o teste C03 de `teste_motores.py` passou de verde para vermelho. Causa-raiz: Excel serializa colunas booleanas com nulos como float64 (1.0, 0.0, NaN), e a função `_infer_type_from_series` tinha early-return para `'numeric'` assim que `is_numeric_dtype` era True, antes de checar se os valores não-nulos estavam contidos em {0, 1}. O C03 passava antes por acidente: o bug do preview stringificava os valores, e o fluxo caía em outro ramo que produzia `'boolean'`. Com o fix, a stringificação sumiu e a limitação apareceu.
**Decisão:** Adicionada regra de inferência semântica em `_infer_type_from_series`: antes do early-return `'numeric'`, se o dtype é numérico E os valores não-nulos estão contidos em {0, 1, 0.0, 1.0, True, False} E existe pelo menos um nulo → retornar `'boolean'`. `BOOL_MAP` foi expandido para incluir as chaves `"1.0"` e `"0.0"` para conversão consistente. Novo warning W-B01 é emitido quando essa detecção dispara, alertando o usuário para confirmar a intenção analítica.
**Razão:** O `motor_base` faz inferência **semântica** (analítica), não apenas técnica. Uma coluna `{0, 1, NaN}` classificada como numeric permitiria agregações estatísticas inválidas sobre um flag (média, desvio padrão de um booleano), o que contradiria o propósito do motor. Manter o comportamento "certo pelo motivo certo" — antes estava certo por acidente (bug mascarando). Alternativa de aceitar `'numeric'` foi rejeitada por fragilizar o uso analítico em todas as visões que dependem dessa inferência.
**Impacto:**
- `motor_base.py` — nova ramificação em `_infer_type_from_series` + warning W-B01 emitido em `_build_column_meta`
- `BOOL_MAP` estendido com `"1.0"` e `"0.0"`
- `teste_motores.py` C03 continua passando (retorna `'boolean'` agora pelo motivo certo)
- Novo warning W-B01 no vocabulário do MotorResult
**Pendências menores:**
- Validar se teste C03 verifica explicitamente a emissão de W-B01 (não só o tipo). Não bloqueante — pode ser fechado quando `spec_motor_base.md` e `spec_validacao_motores.md` forem reescritas no padrão V2 (bloco N-Motores).
- W-B01 ainda não está catalogado em `spec_motor_base.md` (spec legada em auditoria).
**Risco conhecido:** falso positivo raro — uma coluna numérica real cujos valores coincidentemente sejam {0, 1} + nulos seria classificada como boolean. Aceitável no contexto analítico.
**Referência canônica:** `src/motor_base.py` § `_infer_type_from_series` e `_build_column_meta` · `src/teste_motores.py` § caso_b03

---

### D-007 — Correção do truncamento em motor_base + campo `arquivo_bytes` no UploadResult
**Data:** 2026-04-17 · **Bloco:** V-0c · **Status:** Fechada
**Contexto:** Bug crítico identificado no Bloco 8: `motor_base.py` construía o DataFrame interno do `MotorResult` apenas a partir de `upload_result.preview` (5 linhas). Todas as visões recebiam DataFrame truncado. Os 21 testes de `teste_motores.py` passavam porque usavam bases ≤5 linhas, então o truncamento nunca virava observável (causa da Regra 9 do CONTEXT.md). No diagnóstico do V-0c, descoberto que `UploadResult` tinha apenas `file_name` (string) e `preview` (5 linhas) — não havia `arquivo_bytes` nem caminho. Impossível corrigir só em `motor_base.py`.
**Decisão:** Adicionado campo `arquivo_bytes: Optional[bytes]` ao contrato `UploadResult` em `motor_upload.py`, populado via `path.read_bytes()` em `process_file`. `motor_base.py` passa a construir `df` via `pd.read_excel(BytesIO(upload_result.arquivo_bytes), sheet_name=aba_selecionada)` para Excel ou `pd.read_csv` para CSV. Guarda de erro adicionada caso `arquivo_bytes` venha vazio. Lógica de análise (inferência de tipos, null_count, candidatos categóricos) preservada sem alteração. Novo teste B13 em `teste_motores.py` com base sintética de 60 linhas e asserção crítica `assert len(motor_result.df) == 60` como regressão permanente.
**Razão:** A regra canônica do projeto é "Arquivo bruto → Motor de Upload → UploadResult → Motor Base". Um `UploadResult` sem os bytes do arquivo era um **bug de contrato**, não um recurso a preservar. Alternativa de passar bytes como argumento separado ao motor_base foi rejeitada por forçar todos os callers (apps, testes, blocos futuros) a carregar bytes separadamente — quebraria a cadeia canônica e multiplicaria retrabalho linearmente a cada visão nova.
**Impacto:**
- `src/motor_upload.py` — campo novo em `UploadResult`, populado em 3 branches (CSV, multi-sheet stub, Excel)
- `src/motor_base.py` — leitura completa via BytesIO substituindo leitura de preview
- `src/teste_motores.py` — novo caso B13 adicionado à lista `casos`
- `specs/spec_motor_upload.md` — contrato atualizado com nota de concessão pragmática da Fase 2
- Workaround D-005 em `src/app_v2.py` — **agora obsoleto**, deve ser removido no Bloco V-2b
**Consequência:** `motor_upload.py` e `motor_base.py` (código) saíram de "Legado em auditoria" para "Concluído" na planilha. As specs correspondentes (`spec_motor_upload.md`, `spec_motor_base.md`, `spec_validacao_motores.md`) permanecem em auditoria até o bloco N-Motores.
**Resultado dos testes:**
- Baseline (antes): 21/21 ✅
- Após fix motor_base (sem D-008): 20/21 ❌ (C03 quebrou — endereçado em D-008)
- Após D-008: 21/21 ✅
- Com B13 adicionado: 22/22 ✅
**Referência canônica:** `src/motor_upload.py` § `UploadResult` · `src/motor_base.py` § construção de df · `specs/spec_motor_upload.md`

---

### D-006 — Gamma descontinuado como gerador de artefatos
**Data:** 2026-04-17 · **Bloco:** (decisão de processo, pós-Bloco 8) · **Status:** Fechada
**Contexto:** Specs geradas pelo Gamma (V4, V6, V7, motores, base_v2 inicial) não seguem o padrão consolidado do projeto. Uso do Gamma para esse fim foi metodologicamente incorreto — o Gamma é repositório estratégico, não ferramenta de produção de contratos técnicos.
**Decisão:** Gamma volta ao papel original (repositório de Blueprint estratégico). Toda geração de specs, bases sintéticas e prompts de bloco passa a ser responsabilidade do **Arquiteto** (Claude no Projects), com validação da Usuária.
**Razão:** Garantir que todo artefato do projeto passe pelo mesmo método — contratos Pydantic explícitos, pendências fechadas antes de implementação, casos-limite enumerados. O Gamma não produz artefatos nesse padrão.
**Impacto:** Nenhuma spec nova vem do Gamma. Specs legadas serão reescritas uma a uma no padrão V2 à medida que a visão correspondente for ser trabalhada. Esta decisão virou a **Regra 8** do CONTEXT.md.
**Referência canônica:** `CONTEXT.md` § 7 (Regra 8) · Instruções do Projects

---

### D-005 — Rebaseline do projeto pós-Bloco 8
**Data:** 2026-04-17 · **Bloco:** (decisão de processo, pós-Bloco 8) · **Status:** Fechada
**Contexto:** Descoberta no Bloco 8 de bug crítico em `motor_base` (truncamento em 5 linhas) + 4 divergências em `visao_v2.py` (D-001 a D-004 não implementadas) + identificação de que specs geradas pelo Gamma não passaram pelo método atual do projeto. Usuária levantou explicitamente a insegurança em considerar artefatos como "concluídos".
**Decisão:** Rebaselinar planilha de estado. Apenas `spec_v2.md` + `base_v2.xlsx` permanecem como "Concluído" no momento do rebaseline. Todos os demais artefatos existentes passam para status "Legado — em auditoria" até revisão individual. Criada nova categoria de status na planilha: 🔶 EM AUDITORIA (entre ✅ Concluído e ⬜ Não iniciado).
**Razão:** O método TabloFlow (specs com contratos Pydantic, bases sintéticas multi-aba com CASOS_ESPERADOS, decisões registradas em DECISIONS.md) foi consolidado apenas a partir do Bloco B-2. Artefatos anteriores não podem ser tratados como auditados sem passar por esse processo. Manter como "Concluído" seria auto-engano estrutural.
**Impacto:**
- Fila de blocos totalmente reordenada (V-0c → V-2b → N-V4 → N-V7 → N-V6 → Bloco 9)
- Três novos tipos de bloco criados: V-Nb (correção), N-VN (reescrita do zero), N-Motores (reescrita de specs de motor)
- Criadas as Regras 7, 8, 9 do CONTEXT.md como lições estruturais desse incidente
**Referência canônica:** `CONTEXT.md` § 7 (Regras 7, 8, 9) · planilha `TabloFlow_Estado_do_Projeto.xlsx` (coluna Status rebaselinada)

---

### D-004 — Nulo nunca é tratado como zero na V2
**Data:** 2026-04-17 · **Bloco:** B-2 · **Status:** ❌ Revogada por D-023 (2026-04-18, DCV-V2 Sessão 1). Princípio C.5 (formalizado depois) rejeitou a exclusão silenciosa: registros com nulo no campo agora permanecem no resultado com classificação NULO_* visível. Decisão original abaixo preservada para histórico.
**Contexto:** Spec V2 definia comportamento para zeros (SURGIMENTO/DESAPARECIMENTO) mas era omissa sobre nulos. Base de validação `base_v2.xlsx` expôs casos de nulo (SKU-101, SKU-103, SKU-202) que forçavam decisão.
**Decisão:** Registro com nulo em A ou B é excluído da análise — não entra em `registros` nem em contagens. Warning W01 ampliado para cobrir tanto registros individuais com nulo quanto >20% de nulos no campo.
**Razão:** Tratar nulo como zero seria inventar valor — viola o princípio determinístico do TabloFlow. Excluir + avisar preserva auditabilidade.
**Impacto:** `visao_v2.py` deve filtrar nulos antes do cálculo · W01 cobre 2 cenários distintos.
**Status de implementação:** ⚠️ **Não implementada** em `visao_v2.py` — identificada como divergência no Bloco 8. Corrigir em V-2b.
**Referência canônica:** `specs/spec_v2.md` § Decisões Tomadas no Bloco B-2 · D-P05.

---

### D-003 — `variacao_percentual` não é arredondada no contrato V2Result
**Data:** 2026-04-17 · **Bloco:** B-2 · **Status:** ✅ Fechada · Confirmada pelo DCV-V2 (P-V2-04, 2026-04-18). Decisão honrada como diretriz do DCV-V2 §4.3: contrato preserva precisão total, exibição arredonda (Streamlit 2 casas, Excel formato `0.00%` com valor completo na célula). Sem necessidade de nova D-XXX.
**Contexto:** Spec V2 deixava em aberto o nº de casas decimais para `variacao_percentual`. Gabarito da `base_v2.xlsx` usou 6 casas como referência neutra.
**Decisão:** Contrato `RegistroComparado.variacao_percentual` preserva precisão total (float Python nativo). Arredondamento é responsabilidade da camada de exibição (`app_v2.py`) e da exportação Excel.
**Razão:** Arredondar no contrato perde informação irreversivelmente. Cada camada de saída pode ter precisão diferente conforme a necessidade.
**Impacto:** `visao_v2.py` retorna float sem arredondamento · `app_v2.py` formata para exibição · exportação Excel usa formato de célula (`0.0%` ou `0.00%`).
**Status de implementação:** ⚠️ **Não implementada** em `visao_v2.py` — identificada como divergência no Bloco 8 (motor faz `round(..., 4)` dentro do contrato). Corrigir em V-2b.
**Referência canônica:** `specs/spec_v2.md` § Decisões Tomadas no Bloco B-2 · D-P04.

---

### D-002 — Resumo PERCENTUAL/INDICE usa média simples + warning obrigatório
**Data:** 2026-04-17 · **Bloco:** B-2 · **Status:** ❌ Revogada por D-024 (2026-04-18, DCV-V2 Sessão 1). Default silencioso de média simples + warning pós-execução violava Princípio C.5 ("ajusta cedo, evidencia tarde"). D-024 substitui por 3 opções declaradas (média simples default visível + média ponderada + não consolidar). Decisão original abaixo preservada para histórico.
**Contexto:** Soma de campos PERCENTUAL e INDICE no `ResumoAgrupador` não tem significado matemático. Aba `POR_COLUNAS_MULTI_TIPO` da `base_v2.xlsx` forçou o tema (mistura VALOR, PERCENTUAL, INDICE).
**Decisão:** No `ResumoAgrupador`, para campos PERCENTUAL ou INDICE: `total_a` e `total_b` recebem média simples dos valores no grupo. Warning W07 obrigatório sempre que houver pelo menos um campo desses tipos com agrupadores configurados.
**Razão:** Bloquear o resumo (alternativa C) frustra o usuário comum. Média ponderada (alternativa B) exige campo de peso adicional — adiciona configuração na Etapa 2 e pode confundir. Média simples + aviso explícito é o equilíbrio entre utilidade e honestidade.
**Impacto:** Lógica de `ResumoAgrupador` ramifica por tipo de campo · W07 sempre dispara nesse caso.
**Status provisório:** Revisitar em Fase 3 (UX) se reclamação de usuária aparecer. Alternativa futura: média ponderada com campo de peso configurável pelo usuário.
**Status de implementação:** ⚠️ **Não implementada** em `visao_v2.py` — W07 nunca é emitido hoje. Corrigir em V-2b.
**Referência canônica:** `specs/spec_v2.md` § Decisões Tomadas no Bloco B-2 · D-P02.

---

### D-001 — POR_LINHAS sem par tratado como SURGIMENTO/DESAPARECIMENTO
**Data:** 2026-04-17 · **Bloco:** B-2 · **Status:** ❌ Revogada por D-022 (2026-04-18, DCV-V2 Sessão 1). Inventar `valor_b=0` e `variacao_pct=-1.0` para registros sem par viola Princípio C.5 — coloca valor onde não há dado. D-022 substitui por classificação dual (AUSENTE_ORIGEM/AUSENTE_COMPARADO no contrato, exibição amigável separada) com valores `None` honestos. Decisão original abaixo preservada para histórico.
**Contexto:** Spec V2 não definia comportamento quando estrutura POR_LINHAS resultava em registros sem par após o pivot (presente em A mas não em B, ou vice-versa). Decisão pendente desde a spec original.
**Decisão:** Registro presente apenas em A → `DESAPARECIMENTO` (valor_b=0, variacao_pct=-1.0). Registro presente apenas em B → `SURGIMENTO` (valor_a=0, variacao_pct=None). Warning W06 (novo) reporta a contagem.
**Razão:** Preserva o registro · consistente com a regra de zeros já definida na spec · alinhado ao perfil de uso (analista corporativo *quer* ver "SKU novo apareceu em Jan/25"). Alternativa de excluir + warning esconderia eventos analíticos legítimos.
**Impacto:** Pivot em `visao_v2.py` deve preservar todos os registros · novo warning W06 entra na lista de warnings da V2.
**Status de implementação:** ⚠️ **Parcialmente implementada** em `visao_v2.py` — o outer merge preserva registros, mas W06 não é emitido. Corrigir em V-2b.
**Referência canônica:** `specs/spec_v2.md` § Decisões Tomadas no Bloco B-2 · D-P01.

---

## Convenções

- **Numeração D-XXX:** sequencial global. Não reaproveitar números mesmo se uma decisão for revogada.
- **Status `Revogada`:** quando uma decisão for substituída, marcar a antiga como Revogada (sem deletar) e registrar a nova com referência cruzada.
- **Status `Provisória`:** decisão tomada com ressalva explícita de revisão futura. Indicar em qual fase ou condição revisar.
- **Mapeamento de pendências de spec:** quando uma decisão fecha uma pendência local da spec (ex: D-P01 da V2), citar como `§ ... · D-P01` para preservar o link.
- **Campo "Status de implementação":** quando a decisão é de contrato mas a implementação está pendente em alguma visão/módulo, indicar explicitamente. Especialmente relevante para D-001 a D-004 enquanto V-2b não é executado.

---

## Decisões em aberto (não registradas como D-XXX)

Pendências que ainda não viraram decisão fechada:

- **P03 (da spec_v2.md)** — validar com usuárias se o limite de 10 campos comparados é adequado. Aguarda validação de produto. Não bloqueia implementação atual.
