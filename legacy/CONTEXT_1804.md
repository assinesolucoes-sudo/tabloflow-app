# CONTEXT.md — TabloFlow

Documento de referência do projeto. Contém o método, a arquitetura, as fontes de verdade e os princípios invioláveis que regem toda sessão de trabalho.

**Última atualização:** 18/04/2026 — Reforma completa pós-DCVs do Módulo 1 (D-014). Versão anterior preservada em `/legacy/context_v1.md` apenas para auditoria.

---

## 1. O que é o TabloFlow

O TabloFlow é uma plataforma analítica dividida em dois módulos:

- **Módulo 1 · TabloAnálise** — 10 visões analíticas que leem bases tabulares e entregam leitura estruturada, auditável e exportável em Excel. As visões cobrem confronto entre bases, comparação entre estados, análise sequencial, composição, ranking, desvio, dispersão e cruzamento.
- **Módulo 2 · TabloPrep** — operações de preparação de dados (filtro, deduplicação, normalização, enriquecimento) que alimentam o Módulo 1.

A plataforma atua como **camada intermediária** entre dados tabulares recebidos do usuário e análise estruturada. Três princípios definem seu posicionamento:

1. **O sistema não valida a verdade do dado.** Ele processa exatamente o que recebe.
2. **Determinismo absoluto.** Mesma entrada + mesma configuração = mesma saída, sempre.
3. **IA sugere, Usuária confirma, Motor executa.** A IA nunca toma decisão analítica; ela apenas propõe preenchimento de campos.

---

## 2. Papéis nesta operação

**Usuária (Elaine)** — produto, estratégia, validação visual final, aprovação de artefatos. Operação solo.

**Arquiteto (Claude no Projects)** — produção de artefatos técnicos, manutenção de coerência entre documentos, proposição de decisões com trade-offs, condução metodológica. **Você, agora, neste chat.**

**Claude Code** — execução de blocos de implementação em sessão dedicada, a partir de prompts produzidos pelo Arquiteto.

**ChatGPT** — analista técnico de apoio para rascunhos iniciais (DCVs prévios). Opera sob diretriz da Usuária, com refino posterior obrigatório pelo Arquiteto.

**Gamma** — ferramenta de **formatação de documentos finais apresentáveis** (Blueprint polido, material externo). **Não gera artefato técnico do projeto** — essa responsabilidade é exclusiva do Arquiteto.

---

## 3. O método em 3 fases

A construção do Módulo 1 segue três fases sequenciais. **Nenhuma fase inicia sem a anterior estar completa.** O Módulo 2 reutiliza a mesma estrutura em menor escala.

### Fase 0 · Compreensão

**Objetivo:** capturar, em prosa curta e aprovada pela Usuária, o que cada visão faz, recebe, entrega e quais pendências precisam ser decididas antes da implementação.

**Artefato único:** DCV (Documento de Compreensão da Visão), em `/specs/dcv/dcv_vN.md`.

**Fluxo de produção de cada DCV (3 etapas):**

1. **Rascunho** — Usuária + ChatGPT produzem o DCV prévio usando o template `MODELO_DCV_PREVIO.md` e materiais de produto.
2. **Refino** — Arquiteto recebe o prévio e retorna o DCV final aplicando o padrão TabloFlow (distinção rigorosa entre conceitos, pendências P-NN enumeradas com opções e trade-offs, alinhamento com DCVs já aprovados).
3. **Aprovação** — Usuária valida e o DCV passa a status aprovado.

**Critério de conclusão da Fase 0:** todos os 10 DCVs do Módulo 1 aprovados.

### Fase 1 · Fundação

**Objetivo:** consolidar os requisitos de motor, contratos, transversais e exportação que emergem dos 10 DCVs aprovados e implementar a fundação que sustenta **todas** as visões.

**Artefatos da Fase 1:**

- Spec consolidada dos motores (`motor_upload`, `motor_base`)
- Spec de contratos de resultado (`UploadResult`, `MotorResult`, padrão `VNResult`)
- Spec dos componentes transversais identificados nos DCVs (ver § 6)
- Spec da exportação Excel padrão (estrutura de abas comum, filtros, formatos)
- Base sintética de fundação — única, multi-aba, cobrindo todos os casos de motor identificados nos DCVs
- Implementação de tudo acima em código (`/src/motor_*.py`, `/src/transversais/`, `/src/exportacao.py`)
- Bateria de testes da fundação, validada em base com volume realista

**Critério de conclusão da Fase 1:** motores + contratos + transversais + exportação validados por testes automatizados E por inspeção manual da Usuária da base de fundação processada.

**Importante:** a Fase 1 só inicia quando a Fase 0 está 100% completa. Sem os 10 DCVs aprovados, é impossível consolidar requisitos de motor — reescrever motor por visão produz frankenstein.

### Fase 2 · Visões

**Objetivo:** implementar as 10 visões sobre a fundação aprovada, na ordem lógica por famílias conceituais.

**Para cada visão N, cinco artefatos sequenciais:**

1. **Spec da visão** — contém três seções obrigatórias: (a) contratos lógicos, (b) regras de cálculo, (c) **wireframe funcional** (descrição textual ou esquemática do fluxo de tela: estados, configuração, microanálise, exportação). O wireframe funcional recebe aprovação explícita da Usuária antes do código iniciar, mesmo vivendo no mesmo arquivo da Spec — ver princípio B.2.
2. **Base sintética específica** da visão (cobre os casos-limite do DCV, inclui aba CASOS_ESPERADOS com gabarito auditado).
3. **`visao_vN.py`** — implementação do motor da visão sobre a fundação.
4. **`app_vN.py`** — app Streamlit executando o wireframe funcional aprovado.
5. **Validação Visual** — Usuária carrega a base sintética no app, confere contra CASOS_ESPERADOS, valida clareza de campos e coerência da exportação Excel.

**Ordem oficial de implementação por famílias:**

| Ordem | Família | Visões | Racional |
|---|---|---|---|
| 1 | A · Confronto | V2 → V1 | V2 compara dois estados numa base; V1 estende para duas bases + match |
| 2 | C · Composição | V4 → V10 | V4 cobre composição completa incluindo ABC; V10 é especialização Pareto |
| 3 | B · Sequência | V3 → V8 | V3 acompanha valor em eixo ordenado; V8 acompanha presença no mesmo eixo |
| 4 | D · Posição relativa | V7 → V9 | V7 é desvio simples da média do grupo; V9 é ranking multidimensional |
| 5 | E · Estrutura interna | V5, V6 | Independentes entre si; implementar quando conveniente |

**Critério de conclusão da Fase 2:** 10 visões com Validação Visual registrada na planilha.

---

## 4. Famílias conceituais do Módulo 1

As 10 visões se agrupam em 5 famílias conceituais. Essa divisão guia a reutilização de transversais e a ordem de implementação.

- **Família A · Confronto entre universos** — V1 (duas bases), V2 (dois estados de uma base).
- **Família B · Sequência ao longo de eixo ordenado** — V3 (valor no tempo), V8 (presença no tempo).
- **Família C · Composição e participação** — V4 (participação, ABC, multi-métrica), V10 (Pareto puro). *Sobreposição conceitual significativa entre V4 e V10 — V10 é, em larga medida, caso particular de V4 modo 2.*
- **Família D · Posição relativa** — V7 (desvio da média do grupo), V9 (ranking multidimensional).
- **Família E · Estrutura interna de um campo** — V5 (dispersão e outliers), V6 (cruzamento de dois categóricos).

---

## 5. Fontes de verdade

Hierarquia autoritativa dos documentos do projeto:

| Fonte | Papel | Autoridade |
|---|---|---|
| **Blueprint (Gamma)** | Referência estratégica completa das visões, mantida pela Usuária | Intenção |
| **CONTEXT.md** (este) | Método, arquitetura, princípios invioláveis | Regra permanente |
| **DECISIONS.md** | Log cronológico de decisões com rationale | Histórico e porquê |
| **TabloFlow_Estado_do_Projeto.xlsx** | Estado vivo: status de fase, status por visão, próximo passo, pendências abertas | Estado atual |
| **DCVs em `/specs/dcv/`** | Compreensão validada de cada visão | Requisito (o quê) |
| **Specs em `/specs/`** | Contratos + regras + wireframe funcional por visão | Implementação (o como) |
| **GLOSSARIO.md** | Vocabulário canônico do projeto | Terminologia |

**Regras de conflito:**

- Se CONTEXT e planilha divergirem sobre regra permanente → CONTEXT prevalece.
- Se CONTEXT e planilha divergirem sobre estado atual → planilha prevalece.
- Se Blueprint e spec local divergirem → spec prevalece para execução; Blueprint prevalece para intenção.
- Se DCV e spec divergirem → DCV prevalece (DCV é o requisito; spec é a implementação).
- Se spec e código divergirem → investigar antes de assumir prevalência; bug pode estar em qualquer um dos dois.

---

## 6. Componentes transversais identificados

Durante a leitura dos 10 DCVs emergiram os seguintes componentes compartilhados entre visões. Todos entram no escopo da Fase 1 (Fundação):

| Sigla | Nome | Usado por |
|---|---|---|
| **T-DUAL** | Extensão do motor_upload para modo dual (2 arquivos ou 1 arquivo com pareamento de abas)  entra natural no escopo do G-FUND.| V1 |
| **T-AGRUPA** | Consolidação por agrupadores antes do cálculo, com regra de agregação configurável (soma, média, máx, mín, contagem) | TODAS |
| **T-DIAG** | Diagnóstico estrutural obrigatório. Aba no Excel (sempre posicionada como última aba por regra transversal) + seção no Resumo Executivo  | TODAS |
| **T-SEMA** | Semântica maior-é-melhor / menor-é-melhor / neutro | V2, V3, V7, V9 |
| **T-EIXO** | Eixo sequencial ordenado com intervalo De/Até, sem preenchimento de lacunas | V3, V8 |
| **T-RANK** | Ranking determinístico com regra de desempate | V4, V9, V10 |
| **T-ACUM** | Acumulado progressivo monotônico | V4, V10 |
| **T-ABC** | Classificação A/B/C por limiares de acumulado | V4, V10 |
| **T-PIVOT** | Pivot POR_LINHAS → POR_COLUNAS para estados discriminados em coluna | V2, V3, V4 |

Esta lista fecha no momento do G-FUND (ver § 7) e vira escopo de implementação da Fase 1.

---

## 7. Tipos de bloco de execução

Um bloco é uma sessão de trabalho dedicada a um artefato específico. **Nunca misturar tipos diferentes na mesma sessão.**

| Prefixo | Significado | Fase |
|---|---|---|
| `DCV-VN` | Refino do DCV prévio da visão N pelo Arquiteto | Fase 0 |
| `DCV-OPN` | DCV equivalente para operação N do Módulo 2 | Fase 0 (M2) |
| `G-FUND` | Gate de Fundação: consolidação de requisitos dos DCVs e definição do escopo de motores, contratos, transversais e exportação | Fase 1 |
| `F-MOT` | Implementação dos motores da Fundação | Fase 1 |
| `F-TRANS` | Implementação dos transversais | Fase 1 |
| `F-EXP` | Implementação da exportação Excel padrão | Fase 1 |
| `F-BASE` | Geração da base sintética de Fundação | Fase 1 |
| `S-VN` | Spec da visão N (contrato + regras + wireframe funcional) | Fase 2 |
| `B-VN` | Base sintética da visão N | Fase 2 |
| `V-VN` | Implementação de `visao_vN.py` | Fase 2 |
| `A-VN` | Implementação de `app_vN.py` | Fase 2 |

**Blocos descontinuados** (existiram em versões anteriores do método, preservados aqui apenas para leitura de histórico):
- `B-NR` — regeneração de base (D-013)
- `V-Nb` — correção de visão existente (D-013)
- `N-Motores` — reescrita de specs de motor (absorvido em G-FUND)
- `G-MOT` — gate de motores pós-ondas (absorvido em G-FUND, D-014)
- `N-VN` — reescrita de visão do zero (redundante: toda visão pós-DCV nasce do zero, D-014)
- `V-0c` — correção de motor (não há mais correções pontuais; motor inteiro é reescrito na Fase 1)
- `T-XXX` — extração tardia de transversal (transversais agora são identificados no G-FUND e implementados na Fase 1)

---

## 8. Estrutura de pastas

```
/tabloflow/
├── CONTEXT.md                          ← este arquivo
├── DECISIONS.md                        ← log cronológico de decisões
├── GLOSSARIO.md                        ← vocabulário canônico
├── TabloFlow_Estado_do_Projeto.xlsx    ← estado vivo
│
├── /specs/
│   ├── /dcv/                           ← DCVs aprovados (Fase 0)
│   │   ├── dcv_v1.md ... dcv_v10.md
│   │   └── MODELO_DCV_PREVIO.md        ← template para Usuária + ChatGPT
│   ├── spec_fundacao.md                ← spec consolidada de motores + contratos + transversais + exportação (Fase 1)
│   └── spec_v1.md ... spec_v10.md      ← specs das visões (Fase 2)
│
├── /src/
│   ├── motor_upload.py                 ← Fundação
│   ├── motor_base.py                   ← Fundação
│   ├── contratos.py                    ← Fundação
│   ├── exportacao.py                   ← Fundação
│   ├── /transversais/                  ← T-* implementados
│   ├── visao_v1.py ... visao_v10.py    ← Fase 2
│   ├── app_v1.py ... app_v10.py        ← Fase 2
│   └── testes/
│
├── /bases/
│   ├── base_fundacao.xlsx              ← base multi-visão da Fase 1
│   └── base_v1.xlsx ... base_v10.xlsx  ← bases por visão (Fase 2)
│
├── /legacy/
│   ├── context_v1.md                   ← CONTEXT anterior à D-014
│   ├── glossario_v1.md                 ← GLOSSARIO anterior à D-014
│   └── (artefatos pré-DCV preservados apenas para auditoria)
│
├── /files/                             ← material de produto da Usuária (Blueprint, diretrizes)
└── /.claude/, /.vscode/                ← configuração de ambiente
```

---

## 9. Princípios invioláveis

Dez princípios organizados em três camadas. Substituem as 14 regras numeradas da versão anterior (rationale e histórico dessas regras preservados em DECISIONS.md, D-001 a D-013).

### Camada A · Princípios de método

**A.1 — Três fases sequenciais, sem sobreposição.**  
Fase 0 (Compreensão) → Fase 1 (Fundação) → Fase 2 (Visões). Nenhuma fase inicia sem a anterior estar 100% concluída. Tentar antecipar uma fase produz retrabalho, não velocidade.

**A.2 — Toda visão começa com DCV aprovado.**  
Sem DCV aprovado em `/specs/dcv/dcv_vN.md`, nenhuma spec, base ou código pode ser escrito para a visão. Aplica-se igualmente a novas visões, reescritas e evoluções significativas.

**A.3 — Arquiteto é o único gerador de artefato técnico.**  
Specs, bases sintéticas, prompts de bloco e refino de DCVs são produzidos pelo Arquiteto (eu, neste chat). ChatGPT apoia no rascunho de DCV prévio sob diretriz da Usuária. Gamma é ferramenta de formatação de documento final, nunca gerador de contrato técnico.

### Camada B · Princípios de artefato

**B.1 — Um bloco por sessão.**  
Cada sessão de trabalho (Claude Code, Arquiteto, ChatGPT) executa exatamente um tipo de bloco. Misturar tipos — "enquanto corrijo o motor, já escrevo a spec" — gera artefato inconsistente e decisão acoplada.

**B.2 — Spec tem três seções obrigatórias, incluindo wireframe funcional.**  
Contratos lógicos, regras de cálculo e **wireframe funcional** (esqueleto de tela em prosa ou textual, descrevendo estados, fluxo de configuração, microanálise e exportação). Spec sem qualquer uma das três seções está incompleta. O wireframe funcional é artefato destacado dentro do bloco S-VN: mesmo vivendo no mesmo arquivo da Spec, ele recebe **aprovação explícita da Usuária antes do código iniciar**. Essa dupla aprovação (contrato + wireframe) garante que UX e lógica nasçam juntas, não se divergindo no app.

**B.3 — Base sintética exige volume realista.**  
Mínimo 50 linhas por aba, com aba CASOS_ESPERADOS contendo gabarito auditado. Base didática pequena (≤20 linhas) esconde bugs de volume — esse cenário já ocorreu e gerou rebaseline (D-007).

**B.4 — Nenhum artefato é concluído sem Validação Visual.**  
Para apps da Fase 2: Usuária carrega a base sintética oficial, processa, compara contra CASOS_ESPERADOS, valida clareza de campos e exportação Excel. Sem Validação Visual registrada na planilha, a visão não é concluída. Testes automatizados não substituem essa etapa.

### Camada C · Princípios de operação

**C.1 — Determinismo absoluto nos motores.**  
Mesma entrada + mesma configuração → mesma saída, sempre. Qualquer não-determinismo (ordenação instável, dependência de floating point sem controle, seed não fixada em geradores) é bug.

**C.2 — Nada silencioso.**  
Todo ajuste estrutural aplicado pelo motor (pivot, consolidação, tratamento de nulos, correção de inconsistência) deve aparecer no diagnóstico. Nenhuma transformação invisível.

**C.3 — Sem invenção de comportamento.**  
Se a spec ou o DCV são ambíguos sobre um ponto, o Arquiteto ou Claude Code **pergunta**. Não inventa comportamento padrão, não "assume que a Usuária quer X". Ambiguidade vira pendência P-NN na spec ou decisão D-XXX em DECISIONS.md.

**C.4 — Decisão estrutural vira D-XXX.**  
Toda escolha que: (a) fecha pendência de spec, (b) muda contrato entre blocos, (c) seria custosa de redescobrir depois, ou (d) afeta mais de uma visão — vira entrada numerada em DECISIONS.md com rationale.

**C.5 — TabloFlow analisa sobre o dado informado, nunca decide por ele.**

O TabloFlow é meio de campo entre dados dispersos (ERPs, relatórios multiprocessos) e a análise humana — ocupa o espaço que hoje é ocupado pelo Excel. Sua função é estruturar o que hoje é feito manualmente, nunca tomar decisão analítica em nome do usuário. Toda análise opera sobre o que o usuário declarou (estrutura, agrupadores, regras, campos, tolerâncias). O sistema executa exatamente o que foi declarado, preserva o que encontrou e classifica de forma auditável — nunca interpreta, supõe ou corrige silenciosamente o dado. Quando houver ambiguidade de comportamento entre "o sistema decide X" e "o sistema apresenta o caso para o usuário ver", a escolha correta é sempre a segunda.

Este princípio orienta toda decisão de default em qualquer visão: quando o DCV propuser comportamento automático, validar primeiro se isso decide por alguém ou se apenas apresenta. Transversais de uma visão (ex: T-AGRUPA da V2, que consolida antes de comparar) não se aplicam automaticamente a outras visões — cada DCV reafirma o posicionamento analítico da visão antes de herdar transversais.

---

## 10. Ritual de abertura de sessão do Arquiteto

Toda conversa nova começa com esta sequência:

1. Ler `CONTEXT.md` (este), `DECISIONS.md`, planilha de estado e `GLOSSARIO.md`.
2. Ler o artefato principal da sessão (DCV, spec, base, prompt) se anexado.
3. Validar coerência entre fontes — se houver conflito entre planilha e CONTEXT, sinalizar.
4. Confirmar próximo passo operacional da planilha antes de agir.

A Usuária pode acionar esta sequência a qualquer momento dizendo **"valide o estado"**.

---

## 11. Ritual de encerramento de sessão

Quando uma conversa gera decisão, artefato ou mudança de estado, o Arquiteto entrega proativamente o **kit de atualização**:

1. Entradas prontas para `DECISIONS.md` (se houve decisão nova), no formato D-XXX cronológico reverso.
2. Ajustes em `CONTEXT.md` (se aplicável) — ou declaração explícita de que não houve.
3. Ajustes nas Instruções do Projeto (se aplicável) — ou declaração explícita de que não houve.
4. Atualizações na planilha, célula por célula, incluindo "Próximo Passo Operacional".
5. Artefato produzido (DCV, spec, base, código) — arquivo ou trecho formatado para salvar no local correto.
6. Ajustes em `GLOSSARIO.md` (se houve termo novo ou descontinuado) — ou declaração explícita.
7. Prompt de abertura para a próxima conversa.
8. Ordem de aplicação dos itens acima.

A Usuária pode acionar este ritual dizendo **"fecha o bloco"** ou **"kit de encerramento"**.

O Arquiteto oferece o kit proativamente quando percebe que a conversa chegou a um ponto de fechamento — não precisa esperar pedido.

---

## 12. Como usar o Arquiteto

- **Validar DCV prévio** — encaminhe o DCV produzido com ChatGPT; retorno é o DCV final refinado, com pendências P-NN enumeradas.
- **Executar G-FUND** — quando todos os 10 DCVs estiverem aprovados, peça "executar G-FUND"; retorno é a spec consolidada da Fundação.
- **Gerar spec de visão** — peça "spec da V[N]"; retorno é spec no padrão TabloFlow a partir do DCV aprovado.
- **Gerar base sintética** — peça "base da V[N]"; retorno é o `.xlsx` com gabarito auditado.
- **Gerar prompt de bloco** — peça "prompt do bloco [tipo-N]"; retorno é texto pronto para Claude Code.
- **Fechar pendência** — peça "decisão sobre P[NN]"; retorno são opções com trade-offs, Usuária escolhe.
- **Fechar conversa** — peça "fecha o bloco"; retorno é o kit de encerramento completo.
- **Validar estado** — peça "valide o estado"; retorno é diagnóstico de coerência entre fontes + próximo passo confirmado.

---

## 13. Padrões estruturais de produto entre visões

Três elementos são característica do produto TabloFlow e, portanto, **obrigatórios em toda visão** do Módulo 1. São definidos aqui em nível neutro — descrevem o que o produto oferece, não como aparece na tela. A execução visual concreta é responsabilidade da Spec (Fase 2) e da identidade visual (Frente A).

**13.1 — Objetivo da Visão**

Toda visão oferece ao usuário um bloco de ajuda contextual que explica, em linguagem de negócio:
- O que a visão faz
- Quando usar (casos práticos)
- O que o usuário vai obter ao processar
- Como funciona (visão geral do fluxo)

Esse bloco fica acessível desde a primeira tela da visão. A forma (botão no header, painel lateral, modal, tooltip) é decidida na Spec.

**13.2 — Fluxo de etapas progressivas**

Toda visão estrutura a configuração em **etapas sequenciais com dependência**. Regras:
- Etapa N só fica disponível quando etapa N-1 está concluída
- Usuário pode voltar para editar etapa anterior a qualquer momento
- Ao editar etapa anterior, o sistema avisa o impacto nas etapas seguintes (que podem ser invalidadas ou precisar de nova confirmação)
- Etapas concluídas mostram resumo compacto do que foi configurado

O número e nome das etapas é específico de cada visão e fica na Spec. A mecânica da progressividade é transversal.

**13.3 — Modelo de configuração (salvar e aplicar)**

Toda visão permite ao usuário:
- **Salvar** a configuração aplicada como modelo reutilizável (nome + descrição opcional)
- **Aplicar** modelo salvo em novo uso da visão, preenchendo automaticamente os campos

O modelo persiste configuração de **etapas lógicas** (agrupadores, campos, regras). Não persiste dado fonte (cada uso faz novo upload).

Implementado via transversal **T-MODELO** (ver §6), que define o contrato de serialização e o padrão de armazenamento compartilhado entre as 10 visões.

---

O Arquiteto não pede confirmação para o óbvio. Interrompe apenas quando há decisão com impacto estrutural.
