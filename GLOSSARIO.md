# GLOSSARIO.md — TabloFlow

Vocabulário canônico do projeto. Termo → definição curta → referência à fonte de verdade (CONTEXT, DECISIONS, Specs, DCVs).

- **v3 · 23/04/2026** · pós-ALINHA-Descoberta-Camada-Produto · ciclo de 6 artefatos · B.4 desdobrado · vocabulário bilingue formalizado · F-APRESENT na Fundação · Excel como produto
- **v4 · 24/04/2026 · este arquivo** · pós-ALINHA-Retroação-V2 · novo Bloco 15 com 8 verbetes (Gate Duplo · Motor primeiro · TODO-FAPRESENT-CLEANUP · Sanity check numérico · Tela "Resultado da análise" · Capability 11 · Princípio P-UNIF · ALINHA-Retroação-V2) · D-174 a D-185 absorvidas · 11 capabilities F-APRESENT · 7 derivados Camada C
---

## 1 · Quem faz o quê · ciclo de 6 artefatos por visão

Reescrita por D-158 (ciclo de 5 → 6 artefatos · P-VN antes de S-VN).

| Artefato | Produtor | Insumos | Saída | Aprovação |
|---|---|---|---|---|
| **P-VN** | Arquiteto | DCV + `vocabulario_bilingue.md` + F-APRESENT | Spec de Produto (markdown · amostras de paleta em F-APRESENT) | Usuária |
| **S-VN** | Arquiteto | DCV + P-VN + spec_fundacao | Spec técnica + wireframe HTML (Família A) | Usuária |
| **B-VN** | Arquiteto (raro · D-147) | base_fundacao + DCV | base específica + casos | Arquiteto |
| **V-VN** | Claude Code (sessão combinada D-155) | P-VN + S-VN + Fundação | visao_vN.py + testes | Arquiteto (retrospectiva) |
| **A-VN** | Claude Code (sessão combinada D-155) | P-VN + S-VN + V-VN + F-APRESENT | app_vN.py + testes AppTest | Arquiteto (retrospectiva) |
| **VV-VN (VVC)** | Usuária opera silenciosamente | base_vN_cliente | 6º quadrado ✅ | Usuária (gate B.4 camada 1 · Arquiteto NÃO decide ✅/❌) |

**Dependências duras:** P-VN antes de S-VN · S-VN antes de B-VN/V-VN · V-VN testado antes de A-VN · A-VN rodando antes de VV-VN. F-APRESENT P0 concluída antes de P-V1 · F-APRESENT P1 concluída antes de A-V1.

---

## 2 · Blocos e artefatos principais

### ALINHA-Retroação-V2 (D-162 · horizonte firme)
Marco futuro · aplica método novo em V2 · critérios de ativação: V1 aprovada em VVC + V11 aprovada em VVC + Família A completa sob método novo (6/6 quadrados verdes em V1 e V11). Posicionamento: pós-Família A · pré-IA-Família-A. Adiamento formal exige D-XXX (anti-esquecimento silencioso · C.2).

### Contrato de unidade (D-166)
Declaração em P-VN seção 3 da unidade de cada campo exportado: monetário · percentual · contagem · texto · data · classificação · booleano. Ausência de declaração = bug de P-VN · não se exporta campo sem unidade declarada.

### C.D6 · DDU · Default Declarado Universal (D-161)
6º princípio derivado da Camada C. Enunciado: toda vez que o motor tem evidência para sugerir preenchimento, DEVE aplicar default declarado com evidência visível e opção de alterar. Promoção de D-024 (padrão consolidado cristalizado em V2) a princípio universal. Escopo: todas as 11 visões. 5 pontos de aplicação obrigatória: rótulos user-friendly · checkbox base pré-agregada · modo da base · agrupadores candidatos · TED.

### DCV (Documento de Compreensão da Visão)
Artefato único da Fase 0 · 11 DCVs aprovados.

### Diagnóstico (6 seções · D-165)
Estrutura canônica da última aba do Excel executivo (D-017 · 6 seções fixas fundindo Parâmetros + Diagnóstico): (1) Como foi analisado · (2) Ajustes do motor · (3) Pontos de atenção · (4) Decisões do usuário · (5) Configurações avançadas aplicadas · (6) Qualidade estrutural. Aplicação transversal a 11 visões · vive como capability 10 de F-APRESENT.

### Excel executivo (D-163 · D-166)
**Produto principal do TabloAnálise.** Não é entregável técnico. Cliente recebe, apresenta em reunião, decide a partir dele, compartilha. Qualidade do Excel é critério primário de sucesso do TabloFlow. Estrutura canônica de 4 abas (Resumo Executivo narrativo · Coração Visual da visão · Base Analítica · Diagnóstico 6 seções · D-165). 4 requisitos de interatividade: tabela Excel nativa + totais dinâmicos · formatação monetária BR + percentual · colunas adaptativas · contrato de unidade por campo.

### F-APRESENT (D-159 · NOVO)
5º subsistema da Fundação · camada de apresentação executiva · adição (não reescrita). Código em `/src/apresentacao/`. 10 capabilities P0/P1 consumidas transversalmente por 11 visões. Executado em bloco Claude Code dedicado antes de P-V1.

### P-VN (Spec de Produto · D-158 · NOVO)
Novo artefato da Fase 2 · produzido **antes** de S-VN. 5 seções canônicas: (1) Paleta executiva selecionada · (2) Vocabulário bilingue da visão · (3) Arquitetura de abas do Excel · (4) Microcopy de telas · (5) Checklist user-facing. Ciclo da Fase 2 passa de 5 para 6 artefatos. Nomenclatura: `P-VN` (paralelo a S-VN · V-VN · A-VN).

### Paleta executiva (D-164)
Catálogo canônico de 4 paletas para Excel executivo: (1) Azul executivo · institucional padrão · (2) Verde executivo · crescimento/positivo · (3) Cinza executivo · sóbrio/auditoria · (4) Vinho executivo · peso/atenção sem alarmismo. Implementada em F-APRESENT capability 1. Default por visão declarado em P-VN seção 1. Defaults Família A: Cinza para V1 · V11 · V2 retroagida. Usuária pode sobrescrever no momento da exportação (aplica C.D6).

### Validação Visual Construtora (VVC · D-162)
Camada 1 de B.4 desdobrado. Quem opera: Usuária construtora. Base: `base_vN_cliente.xlsx` (sintética). Vocabulário permitido: técnico OU user-facing. Checklist: técnico · derivação mecânica do YAML (D-148 · 5 templates). Modalidade: C mista com Arquiteto presente (D-156). Gate: 6º quadrado ✅ · desbloqueia próxima visão. **Não atesta prontidão para cliente final.** Criterios: checklist ✅ + Excel inspecionado + paleta aplicada + gate desacoplado (download livre) + registro na planilha.

### Validação Visual de Produto (VVP · D-162 · horizonte parqueado)
Camada 2 de B.4 desdobrado. Quem opera: cliente final real. Base: bases reais. Vocabulário permitido: exclusivamente user-facing. Checklist: derivado de `vocabulario_bilingue.md`. Ativação: pós-Família A completa em VVC. Critérios: checklist user-facing ✅ · cliente opera sem assistência · Excel clareza standalone · 3 vertical-alvos testados · registro na planilha aba 1 Zona 3. Sessão futura "Definição operacional VVP" produz protocolo.

### Vocabulário bilingue (D-160)
Tabela canônica transversal técnico ↔ user-facing em `/specs/vocabulario_bilingue.md`. 7 blocos: stepper · modos da base · classificações estruturais · tipos de campo · thresholds · warnings · **termos proibidos**. Consumida por P-VN e aplicada por F-APRESENT capability 2. Regra: vocabulário técnico **nunca** atravessa a fronteira para superfície cliente.

### VV-VN
Validação Visual da visão N. Em V3 deste GLOSSARIO refere-se exclusivamente à **camada VVC** (D-156 · D-162). Modalidade C mista · 3 pontos-chave canônicos (pós-processamento · pré-checklist · pós-exportação) + gatilhos livres. Duração ~1h visão nova · ~40min subsequentes. Gate B.4 camada 1 inviolável: Arquiteto NÃO decide ✅/❌.

---

## 3 · Blocos preservados

(Listagem curta · detalhes no CONTEXT §7)

- **DCV-VN · DCV-OPN** · refino de DCV (Fase 0 + M2)
- **G-FUND · F-MOT · F-TRANS · F-EXP · F-BASE** · Fundação original (CONCLUÍDOS)
- **F-APRESENT** · 5º subsistema da Fundação (NOVO · D-159)
- **ALINHA-<Marco>→<próximo>** · fechamento de Marco (D-142 · 4 aplicações)
- **IA-Família-A · IA-Meta** · Papel A/B/C da IA (D-130)
- **P-VN · S-VN · B-VN · V-VN · A-VN · VV-VN** · ciclo de 6 artefatos por visão (D-158)

---

## 4 · Princípios invioláveis

10 princípios · 3 camadas · 6 derivados formalizados. Detalhes em CONTEXT §9.

**Camada A:** A.1 (3 fases) · A.2 (DCV primeiro) · A.3 (Arquiteto único gerador)

**Camada B:** B.1 (um bloco por sessão) · **B.2 (P-VN 5 seções + S-VN 3 seções · tripla aprovação em Família A)** · B.3 (base ≥50 linhas) · **B.4 desdobrado em VVC + VVP (D-162)**

**Camada C:** C.1 (determinismo) · C.2 (nada silencioso) · C.3 (sem invenção) · C.4 (D-XXX) · C.5 (TabloFlow não decide)

**Derivados formalizados:** CPCO (C.D1 · D-122) · TED (C.D2 · D-123 · D-153 · D-160 · D-161) · BAD (C.D3 · D-124 · D-165) · MBO (C.D4 · D-127 · D-134) · ECP (C.D5 · D-128) · **DDU (C.D6 · D-161 · NOVO)**

**Derivados informais:** herança adaptada (D-073) · warning×conteúdo (D-076)

---

## 5 · Vocabulário por visão

(Seções herdadas da v2 · preservadas integralmente · vocabulário canônico V1 · V2 · V3 · V4 · V5 · V6 · V7 · V8 · V9 · V10 · V11 · anti-glossário por visão · consulta nas respectivas seções do GLOSSARIO original · nenhuma alteração nesta v3 exceto adição de verbetes comuns aos quais cada visão referencia via `vocabulario_bilingue.md`.)

---

## 6 · Componentes transversais (T-*)

(Seções herdadas da v2 · T-AGRUPA · T-DIAG · T-SEMA · T-EIXO · T-RANK · T-ACUM · T-ABC · T-PIVOT · T-DUAL · T-MODELO · T-FUZZY · T-CONCAT · 12 transversais implementados em F-TRANS · nenhuma alteração nesta v3.)

---

## 7 · Camadas Figma Make (D-015)

(Herdada da v2. A Frente A permanece parqueada · wireframes HTML de Família A são Camada B neutra · D-149.)

---

## 8 · Modos da base (taxonomia · D-025)

(Herdada da v2. Aplicação user-facing agora consome `vocabulario_bilingue.md` Bloco 2.)

---

## 9 · Glossário de tipos estruturais de coluna (D-113 · D-133 · D-146)

(Herdada da v2 · 5 valores do enum `tipo_estrutural` em motor_base · aplicação user-facing consome `vocabulario_bilingue.md`.)

---

## 10 · Padrões estruturais de produto (§13 do CONTEXT · 7 padrões · D-163 adicionou 13.7)

- **13.1 · Objetivo da Visão** · bloco de ajuda contextual
- **13.2 · Fluxo de etapas progressivas**
- **13.3 · T-MODELO · Modelo de configuração**
- **13.4 · View especializada** (D-035 · D-046)
- **13.5 · Resumo Executivo em 6 Blocos** (D-125 · renderizado em prosa executiva user-facing por F-APRESENT capability 7)
- **13.6 · Coração Visual da Visão** (D-126)
- **13.7 · Excel executivo é produto** 🆕 (D-163 · D-166 · inclui paleta aplicada + arquitetura de abas canônica + tabela nativa com totais + formatação monetária/percentual + colunas adaptativas + contrato de unidade + badges + hierarquia tipográfica + vocabulário user-facing exclusivo)

**Retroação diferida formalizada** (D-060/D-091/D-121) · todos os pares autônomos de família têm §2.3 simétrico aprovado.

---

## 11 · Anti-glossário · termos descartados ou descontinuados

Termos que **não devem** ser usados. Preservados aqui para leitura de histórico e para identificação rápida em refatorações.

### 11.1 · Termos descontinuados por bloco/decisão de método

- **D-156** · padrão VV-VN · modalidade C mista (opera em VVC após D-162)
- **D-170** (FECHADA · 24/04/2026) · método otimizado de kits · leve vs pesado vs completo · 3 critérios de escolha
- **D-174** · gate duplo de A-VN · camada mecânica (Claude Code) + camada visual (Usuária) · contrato operacional obrigatório
- **D-185** · método de sessões operacionais · padrão 3 fases (investigação · implementação · validação) · sessões de escopo completo em vez de fragmentadas
- **"Ciclo de 5 artefatos"** → descontinuado por **D-158** · substituído por ciclo de 6 artefatos (P-VN antes de S-VN). Não usar "5 quadrados por visão" na planilha · agora são 6 quadrados.
- **"Parâmetros · aba 4 do Excel V2"** → descontinuada por **D-165** · fundida com Diagnóstico · aba única "Diagnóstico" com 6 seções. Em retroação V2: `spec_v2.md` §2.9 · 5 abas passa a 4.
- **"Default declarado" (como padrão informal)** → elevado a princípio derivado universal por **D-161** · agora é `C.D6 · DDU · Default Declarado Universal`. Termo "padrão consolidado D-024" permanece como referência histórica (precedente original).
- **"B-NR" · "V-Nb" · "N-Motores" · "G-MOT" · "N-VN" · "V-0c" · "T-XXX" · "onda padrão"** → descontinuados por D-014 (reforma original do método) · não usar.
- **"Dados Brutos Processados"** → formalmente rejeitada por BAD · C.D3 · D-124. Substituída por Base Analítica + Diagnóstico (última aba).

### 11.2 · Termos descartados por visão

(Herdado da v2 · anti-glossário por visão preservado · V3/V8 particularmente densos.)

### 11.3 · Termos proibidos em superfície cliente (D-160 · Bloco 7 de `vocabulario_bilingue.md`)

**Autoridade equivalente à lista positiva.** Violação = bug em P-VN, S-VN, A-VN ou F-APRESENT.

- Nomes de atributo Python literais (`campo_analisado` · `origem_rotulo_ux` · `limiar_estabilidade_pct` · etc.)
- Enums em caps (`POR_COLUNAS` · `PRESENTE_AMBOS` · `TRANSACIONAL` · etc.)
- Códigos internos do projeto (`D-151` · `P-V2-Evo-01` · `OBS-VV-V2-07` · `T-AGRUPA` · `F-MOT`)
- Serializações técnicas cruas (`datetime.datetime(2026, 4, 23, ...)` · Python dict serializado)
- Fração decimal apresentada como "percentual" (`0.0109` sem conversão · sem símbolo %)
- Fonte monoespaçada em área executiva (exceto Diagnóstico quando referência técnica já traduzida)

Ver `/specs/vocabulario_bilingue.md` Bloco 7 para lista completa e referência canônica.

---

## 12 · Padrões de condução

- **D-019 + D-034** · refino de DCV (Fase 0 · M2 futuramente)
- **D-033** · kit de encerramento de sessão
- **D-131 (estendida por D-156)** · didática técnico-decisional · 5 princípios + 4 categorias de conteúdo (negócio · técnicas puras · execuções de código · **validação de produto**)
- **D-142** · padrão ALINHA · 4 sub-blocos α·β·γ·δ · 4 aplicações (1ª retroativa · 2ª Fundação-Design · 3ª Fase-1→Fase-2 · **4ª Descoberta-Camada-Produto · 1ª emergente**)
- **D-155** · sessão combinada (prompt + retrospectiva em 1 bloco Arquiteto) · aplicável a F-APRESENT · V-VN · A-VN
- **D-156** · padrão VV-VN · modalidade C mista (opera em VVC após D-162)

---

## 13 · Retroações diferidas

**Status pós-ALINHA-Descoberta-Camada-Produto:**

- **V11 → V1** · par autônomo da Família A · **aberta · aguarda paridade sob método novo** (D-058 · preserva simetria após VVC de V1/V11)
- **V3 → V8** · par autônomo da Família B · **cumprida** (D-073 antecipado · D-060)
- **V7 → V9** · par autônomo da Família D · **cumprida** (D-091 · Família D fechada em Fase 0)
- **V5 → V6** · par operacionalmente distante da Família E · **convivência enxuta sem retroação formal** (D-110 · D-121 · Família E fechada em Fase 0)

**Retroação estrutural V2 pós-descoberta:**

- **ALINHA-Retroação-V2** (D-162) · aplica método novo em V2 pós-descoberta · horizonte firme · critérios declarados · pós-Família A validada em VVC · pré-IA-Família-A

---

- **ALINHA-Retroação-V2** (D-162) · aplica método novo em V2 pós-descoberta · horizonte firme · critérios declarados · pós-Família A validada em VVC · pré-IA-Família-A · **5ª aplicação ALINHA · concluída como Marco antecipado em 24/04/2026 · D-184**

---

## 15 · Conceitos novos da ALINHA-Retroação-V2 (24/04/2026)

Esta seção consolida 8 conceitos formalizados no Marco ALINHA-Retroação-V2 (D-184). Cada um materializa lições aprendidas durante as Sessões 4-ter + 4-ter-bis (V2 retroativa · F-APRESENT consumido · descoberta de bug estrutural P-23).

### Gate Duplo (D-174)

Contrato operacional obrigatório de toda A-VN: encerramento depende de **ambas as camadas** aprovarem. Camada 1 (Mecânica · Claude Code automática) · suite pytest 100% verde + CHECKLIST_MECANICO 100% ✅ + amostra Excel + grep TODO-FAPRESENT-CLEANUP + bifurcações declaradas. Camada 2 (Visual · Usuária) · inspeção do Excel (todas abas + paletas) + inspeção do app + sanity check numérico C.D7 + validação contra checklist VVC. Sessão fecha apenas quando ambas aprovam. Caso (b) camada 1 ✅ + camada 2 com defeitos → abre sub-sessão de correção dirigida.

### Motor primeiro, apresentação depois (C.D7 · D-183)

7º princípio derivado da Camada C. Validação empírica de corretude do motor analítico precede validação empírica de apresentação. Excel formatado corretamente com número errado é pior que Excel mal formatado com número certo · porque o primeiro passa despercebido. Operacionalização: VV-VN camada 2 inspeciona Matriz/Coração com sanity check numérico ANTES de Resumo/Diagnóstico · V-VN testes do motor cobrem matriz cartesiana T-SEMA completa (12 casos mínimos) · F-APRESENT capabilities incluem fixture com caso `MENOR_MELHOR`.

### TODO-FAPRESENT-CLEANUP

Comentário de código padronizado · catalogador de débito técnico em `exportacao_vN.py`/`app_vN.py` que deveria estar em F-APRESENT mas foi implementado bespoke em uma visão. META-1 (regra estrutural · D-175) exige que toda implementação bespoke leve este comentário com descrição clara do que promover e para qual capability. Sessão F-APRESENT-cleanup pré-V1 (D-180) executa `grep -r "TODO-FAPRESENT-CLEANUP"` e consome cada ocorrência · promovendo para F-APRESENT. Mecanismo operacional do princípio P-UNIF (D-175).

### Sanity check numérico

Inspeção explícita pela Usuária dos valores calculados pelo motor (não da estética da apresentação) · etapa primária da camada 2 do gate duplo (D-174). Para visões numéricas (8 de 11) · inclui obrigatoriamente verificação de cenário `MENOR_MELHOR` em T-SEMA · onde "subir é ruim" deve produzir cores/classificações invertidas em relação a `MAIOR_MELHOR`. Lição derivada de P-23 (24/04/2026): bug estrutural em motor V2 que 301 testes automatizados não pegaram porque nenhum teste cobria `MENOR_MELHOR`.

### Tela "Resultado da análise" (D-177)

Nome canônico cross-visão da tela final do app · substitui a antiga "Validação Visual" do `app_v2.py` (que era ritual VVC construtor confundido com produto). Microanálise executiva em tela · prévia fiel do Excel antes de baixar · com 4 cards de métricas + tabela de distribuição + tabela de top variações + gráficos inline + leitura qualitativa em prosa + expander de diagnóstico + rodapé com paleta + Baixar Excel. Padrão herdável para todas as 11 visões.

### Capability 11 de F-APRESENT (D-176)

11ª capability canônica do subsistema F-APRESENT (estendendo as 10 P0+P1). Compreende **gráficos executivos** (`/src/apresentacao/graficos.py` · `criar_grafico_distribuicao` PieChart · `criar_grafico_top_variacoes` BarChart horizontal por sinal verde/vermelho/cinza) + **nomenclatura de arquivo** (`/src/apresentacao/nomenclatura.py` · `nomear_excel_executivo` · padrão `{Família} - {Contexto} - {DD-MM-AAAA}.xlsx`). Refinamento pendente em F-APRESENT-cleanup (D-180): parâmetro `unidade_valor` em `criar_grafico_top_variacoes` para aplicar `number_format` correspondente ao eixo.

### Princípio P-UNIF · Uniformidade Transversal F-APRESENT (D-175)

8º padrão estrutural cross-visão (CONTEXT §13.8). Toda visão consome F-APRESENT · `exportacao_vN.py` consome capabilities · zero formatação direta com openpyxl · zero hardcode de cor/string/formato. Bespoke transitório permitido apenas com comentário `TODO-FAPRESENT-CLEANUP`. Critério de fechamento: A-VN só fecha quando `grep TODO-FAPRESENT-CLEANUP` retorna zero ou todos têm vencimento declarado. Mecanismo operacional: META-1 (rastreabilidade obrigatória).

### ALINHA-Retroação-V2 (Marco · D-184)

5ª aplicação do padrão ALINHA · Marco antecipado fechado em 24/04/2026. Consolida descoberta de bug estrutural P-23 + validação empírica do gate duplo D-174 + reformulação de método (D-185 · padrão 3 fases) + formalização de 12 D-XXX novas (D-174 a D-185) + promoção de D-170 (Provisória → Fechada). Sub-blocos α (consolidação) · β (talk-through) · γ (formalização) · δ (kit pesado). Antecipada porque atendeu os 3 critérios D-142 (transição de modo operacional · fecha subsistema · ≥3 pendências estruturais) e a Usuária explicitamente solicitou formalização.

---

## 16 · Conceitos novos da ALINHA-Descoberta-Unidade · Sessões 6/7/8/8.1 (25/04/2026)

Esta seção consolida 11 conceitos formalizados na ALINHA-Descoberta-Unidade (D-194) · Marco emergente fechado em 25/04/2026. Cada um materializa lições da descoberta meta-estrutural do achado-mãe da Família A (campo `unidade` ausente do contrato) e da implementação das 5 evoluções de produto V2 (E1 a E3c).

### Unidade canônica (C.D8 · D-190)

Atributo declarado de todo campo numérico analisado · determina formatação visual (number_format Excel · rótulo da coluna · rótulo do card) e cálculo derivado (Total vs Média · Diferença vs Variação absoluta em p.p · etc). 8 valores canônicos: **MONETARIO_BRL · PERCENTUAL · QUANTIDADE · TEMPO_DIAS · TEMPO_HORAS · MULTIPLICADOR · RAZAO · ADIMENSIONAL** (catalogados em vocabulario_bilingue Bloco 10). Default declarado (C.D6) inferido de `tipo_campo`: NUMERICO_RELATIVO → PERCENTUAL · NUMERICO_ADITIVO/NAO_ADITIVO → MONETARIO_BRL · ESTADO_SITUACAO → ADIMENSIONAL. Usuária pode trocar com 1 clique.

### Diferença absoluta (p.p)

Para campo com `unidade=PERCENTUAL` · termo canônico user-facing da coluna que mostra `Comparado − Origem` em pontos percentuais. Substitui rótulo "Diferença" do MONETARIO. Exemplo: margem de 28,99% em Janeiro · 27,15% em Fevereiro · Diferença absoluta = -1,84 p.p. Distinta de "Variação relativa (%)" que seria -6,36% (= -1,84 / 28,99). Cliente lendo "p.p" entende interpretação aditiva (subiu/desceu N pontos) · cliente lendo "%" entende interpretação multiplicativa (mudou X% relativo). Confundir as duas é fonte clássica de erro analítico.

### Variação absoluta · Variação relativa

Par de termos canônicos para apresentação de comparações em PERCENTUAL no Resumo Executivo da V2. **Variação absoluta (p.p)** = Δ aditivo em pontos percentuais. **Variação relativa (%)** = Δ multiplicativo (valor relativo à origem). Ambas exibidas lado a lado quando unidade=PERCENTUAL. Para outras unidades (MONETARIO/QUANTIDADE/etc) os rótulos canônicos são "Diferença" e "Variação %" · sem distinção absoluta/relativa porque não faz sentido (R$ 100 de diferença é absoluto · não há leitura "percentual aditiva").

### Saúde da comparação (E2 · D-192)

Bloco do Resumo Executivo de V2 que substitui "Como os casos se distribuem" para tipo_campo numérico. Mostra distribuição **semântica** (Melhorou · Piorou · Estável) em vez de estrutural (Presente nos dois lados · Ausente na origem · etc). 3 colunas (Categoria · Casos · Participação) para PERCENTUAL · 4 colunas (+ Δ total) para outras unidades. Footer "Total comparado: X casos · Não comparáveis: Y casos · N sem valor na Origem · M sem valor no Comparado". Para semantica_campo=NEUTRO · categorias AUMENTOU/REDUZIU/ESTAVEL aparecem distintas. Para tipo_campo=ESTADO_SITUACAO · bloco original "Como os casos se distribuem" preservado (estrutural ainda é o coração da análise).

### Concentração (E3a · D-192)

Bloco novo do Resumo Executivo de V2 que mede pareto da variação. Calcula percentual do |Δ| total explicado pelos top 5 e top 10 maiores casos. Microcopy adaptativo: top 5 ≥80% → "Atenção concentrada nos extremos" (interpretação alta) · entre 50-80% → "Concentração moderada nos maiores" (moderada) · <50% → "Variação distribuída por todo o conjunto · sem outliers dominantes" (distribuída). Bloco oculto se há menos que 5 PRESENTE_AMBOS · oculto para tipo_campo=ESTADO_SITUACAO. Cálculo: `abs(diferenca).nlargest(N).sum() / abs(diferenca).sum()`.

### Onde se concentra · Δ médio (E3b · D-192)

Bloco novo do Resumo Executivo de V2 que mostra Top 3 categorias do agrupador escolhido pela Usuária (widget novo na Etapa 4 · `agrupador_destacado`). Ordenado por |Δ| absoluto. Coluna "Δ" formatada por unidade: para MONETARIO/QUANTIDADE/etc é soma do Δ (Δ total); para PERCENTUAL é **Δ médio** (média das diferenças individuais em p.p · porque somar p.p viola C.D3). Coluna "Variação %" mostra variação relativa da categoria. Coluna "Direção" com setas: ↑ Puxa para cima (Δ > 0) · ↓ Puxa para baixo (Δ < 0) · → Estável (Δ ≈ 0). Rodapé "(outras N somam Δ X · sem influência dominante)" ou "(outras N têm Δ médio Y p.p · INFLUÊNCIA DOMINANTE)" se outras categorias somam mais que as top 3.

### Influência dominante

Marca exibida no rodapé do bloco "Onde se concentra" quando a soma das categorias fora do top 3 supera a magnitude do top 3 individual. Sinaliza ao cliente que o conjunto inteiro merece análise · não só os 3 destaques. Comportamento emergente da regra de ordenação por |Δ| absoluto · pode confundir leitura em alguns casos · candidato a refinamento pós-V2 (anotado como observação · não bloqueia fechamento).

### Leitura qualitativa enriquecida (E3c · D-192)

Substituição da Leitura qualitativa antiga (frase genérica "O resultado é misto · há ganhos e perdas distribuídos") por template parametrizado de 2-4 sentenças condicionais. Sentenças derivadas de dados de E2 + E3a + E3b: (1) Resultado agregado · Δ + Variação relativa; (2) Composição · quantos melhoraram vs pioraram + magnitude por unidade; (3) Concentração · top-N explica X% (se ≥50%); (4) Direção dominante · top 1 alta + top 1 baixa por agrupador escolhido. Sentenças condicionais são omitidas quando dado não significativo (não viram "—" nem placeholder). Template específico para PERCENTUAL: usa "Média" + Variação relativa · sem magnitudes em p.p somadas entre parênteses (somar p.p viola C.D3). Helper `_contrair_de` resolve "de o" → "do" / "de a" → "da" automaticamente.

### Stale state (cache do app · D-186)

Estado em que a tela RESULTADO do app exibe dados de uma execução anterior porque a Usuária trocou um campo crítico da configuração (semantica_campo · tipo_campo · agrupadores · etc) sem reexecutar a análise. Detectado por hash determinístico (`_hash_config_critica()` usando hashlib.sha256) sobre payload (config + nome_arquivo + aba_selecionada). Hash armazenado em `_hash_config_executada` no momento da execução bem-sucedida. Gate visual: se hash atual ≠ hash executado · banner amarelo "⚠️ A configuração foi alterada após a última execução · clique em Executar análise para atualizar" + botão de re-execução. Solução protege C.2 (nada silencioso · tela mente sobre estado atual).

### Smoke visual (D-196)

Sub-camada do gate D-174 Camada 1 mecânica · adicionada após Sessão 8 entregar 725 testes verdes mas Camada 2 humana descobrir Excel com valores absurdos. Mínimo 4-6 testes em `src/testes/test_vN_smoke_visual.py` que: (1) geram amostra in-memory; (2) lêem valor de célula-chave (cards · primeira linha da Matriz · etc); (3) aplicam number_format manualmente para obter valor visual renderizado; (4) assertam range realista para a unidade declarada. Custo ~3s por suite. Cobre cenários PERCENTUAL · MONETARIO · QUANTIDADE no mínimo. Padrão estende D-174 sem revogar.

### Débito de Fundação (D-197)

Categoria de débito específica para correções que deveriam ter sido feitas em camada de Fundação (contrato genérico · capability F-APRESENT · etc) mas foram implementadas tática-em-V (uma visão específica · sem promoção arquitetural). Risco característico: próximas visões da mesma família (V1 e V11 da Família A) vão herdar exatamente os mesmos bugs porque o trabalho não está disponível por default. Resolução exige sessão dedicada de Promoção de Fundação. Aplicação canônica: implementação do campo `unidade` na Sessão 8 + 8.1 vive em ComparacaoV2 (V2-específico) e helpers vivem em formatos.py (F-APRESENT correto) · MAS pontos de consumo são bespoke em V2 · então V1/V11 não consomem por default. CONTEXT §16 cataloga débitos pré-V1.

### ALINHA-Descoberta-Unidade (Marco · D-194)

5ª aplicação do padrão ALINHA · Marco emergente fechado em 25/04/2026. Consolida descoberta meta-estrutural do achado-mãe da Família A (campo `unidade` ausente · investigação Sessão 6) + implementação das 5 evoluções de produto V2 (Sessões 8 + 8.1) + formalização de 13 D-XXX novas (D-186 a D-198) + revisão de D-182 in-place + descoberta de Débito de Fundação D-197 + agendamento de ALINHA-Lições-Família-A para 26/04/2026 manhã (D-200). Sub-blocos α (consolidação · 24-25/04 progressivo) · β (talk-through · Sessão 7) · γ (formalização · Sessão 8 + 8.1) · δ (kit pesado · 25/04 fim de tarde). Marco emergente porque atendeu os 3 critérios D-142 (transição de modo operacional · fecha gap de unidade transversal · ≥3 pendências estruturais).

---

## 17 · Conceitos provisórios pendentes de decisão em ALINHA-Lições-Família-A

Esta seção mantém visíveis os termos cuja semântica final será decidida em D-200 (ALINHA-Lições-Família-A · agendada para 26/04/2026 manhã).

### Mockup Excel-alvo (D-191 · provisória)

Proposta de método: antes de Claude Code escrever código de A-VN · mockup do Excel da visão (manual ou semi-automático) serve de critério visual prévio · Claude Code implementa contra Excel-alvo claro · não contra interpretação livre da Spec. Argumento da Usuária: "a gente sabe que o produto final é o Excel · a gente precisa antes de fazer a validação ali na linha do código · a gente precisa de uma visão do Excel gerado pra aquela visão · pra não perder tanto tempo." Vence em D-200 · pode virar padrão operacional novo ou ser descartada.

### Inferência inteligente de unidade pelo motor (P-34)

Proposta: motor lê valores reais da coluna + nome da coluna ("Perc_Orcado", "Margem", "Qtd_Vendida") e pré-seleciona unidade com palpite informado. Critérios candidatos: nome contém "perc/margem/taxa/indice" → sugere PERCENTUAL · nome contém "qtd/quant/units" → sugere QUANTIDADE · valores entre 0 e 1 com média 0.1-0.5 → sugere PERCENTUAL · valores inteiros sempre → sugere QUANTIDADE · valores com decimais e magnitude > 100 → sugere MONETARIO_BRL. Critério de UX: motor mostra inferência mas explica · Usuária mantém controle (DDU C.D6 preservada). Não-bloqueante para V1 · evolução pós-Família A.

---

## 14 · Versões históricas deste GLOSSARIO

---

*Documento vivo · mantido pelo Arquiteto · atualizado em kit D-033 sempre que acumular mudanças significativas (5+ termos · reformulação de tabela · termo descontinuado · novo padrão) · referência canônica em CONTEXT §5.*
