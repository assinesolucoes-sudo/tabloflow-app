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

## D-220 — Cleanup do drift em vocabulario_bilingue.md · sub-sessão Arquiteto · pré-A-V11
Data: 2026-04-26 noite · Bloco: V-V1 (retrospectiva) · Status: Aberta · sub-sessão Arquiteto solo
Contexto: Suite TabloFlow atual tem 1 teste vermelho herdado pré-V-V1 (src/testes/test_apresentacao.py::TestInterfaceVocabulario::test_classificacoes_tem_6_entradas · falha com assert 18 == 6). Identificado por Claude Code em V-V1 Fase 0 (verificação prévia). Análise causal dele: drift residual de sessões anteriores · vocabulary v2 drift mencionado em F-APRESENT P1 da MEMORY.md · expansão de 6 → 18 entradas em vocabulario_bilingue.md Bloco 3 (classificações estruturais) sem atualização do teste correspondente.
Decisão: Sub-sessão Arquiteto solo (10-15 min · sem Claude Code) antes de A-V11 (V11 vai expandir vocabulário ainda mais · acumular drift adicional é antipadrão). Procedimento: (a) ler teste falho · identificar exatamente qual asserção · (b) decidir entre 2 caminhos · (c) aplicar patch · (d) rodar pytest para validar 745+233 = 978 verde + 1 herdado resolvido = 979/979 ✅.
Caminho 1 · atualizar teste para realidade atual · assert len(classificacoes) == 18 · trata vocabulary expandido como correto. Aplicável se as 18 entradas são todas legítimas (V2 + V11 antecipações + V1 + outras visões).
Caminho 2 · cortar entradas espúrias · se após inspeção alguma das 18 for stale ou duplicada · reduz vocabulário. Aplicável se identificadas espúrias.
Decisão entre os dois caminhos é da inspeção · provável Caminho 1 (vocabulary v2 drift sugere expansão legítima · não duplicação).
Razão: Vermelho herdado cumulativo é antipadrão higiênico (próxima sessão pode confundir vermelho herdado com regressão real · perde sinal). Sessão V-V1 demonstrou empiricamente o custo: Claude Code teve que parar e analisar antes de Fase 1 (custo ~5 min de overhead). Cleanup pontual elimina overhead permanente.
Impacto:

Suite passa de 978/979 para 979/979 verde (eliminar 1 vermelho)
vocabulario_bilingue.md Bloco 3 OU teste de interface atualizado conforme caminho escolhido
A-V11 abre com suite limpa · sinal puro
Pré-requisito recomendado de A-V11 (não bloqueio · mas higiene · prioridade média)

Referência canônica: Anomalia 3 da Seção 7 do V-V1_RELATORIO.md · src/testes/test_apresentacao.py::TestInterfaceVocabulario::test_classificacoes_tem_6_entradas · MEMORY.md F-APRESENT P1 (vocabulary v2 drift).

R1-VV-V1 — Pendência de auditoria epistemológica · YAML V1 reescrito · validar em VV-V1
Data: 2026-04-26 noite · Bloco: V-V1 (retrospectiva) · Status: Aberta · resolução em VV-V1 · não-esquecimento C.2
Contexto: Auditoria YAML Q1.A (Fase 7 V-V1) reescreveu entrada V1 do casos_esperados.yaml substituindo expectativa a priori antiga ("Match exato em ~70% das linhas · 65-75%") por snapshot empírico observado (CONCILIADO=0 · DIVERGENCIA_DUPLICIDADE=44 com config canônica Conta+Centro_Custo modo EXATO). Inversão epistemológica: YAML deixa de ser gabarito de design e vira snapshot de comportamento.
Decisão pendente: validar em VV-V1 (Validação Visual com base real cliente) qual dos 3 cenários é verdadeiro:

Cenário A · base de Fundação foi originalmente desenhada para 70% match · regenerou desde então · expectativa antiga ficou stale · entrada nova é correta
Cenário B · base ainda produz 70% match com configuração diferente (talvez Documento+Data em vez de Conta+Centro_Custo) · Claude Code escolheu config que stress-testa DUPLICIDADE em vez de testar conciliação canônica
Cenário C · existe um bug em modo EXATO impedindo CONCILIADO

Razão para adiar: VV-V1 é o ponto natural onde inversão revela-se. Resolver agora exigiria sub-sessão dedicada de auditoria de base (~60-90 min · custo alto) sem dados que diferenciam cenários. Adiar para VV-V1 não é débito esquecido · é decisão consciente · cumpre C.2 pela explicitação.
Plano de resolução em VV-V1:

Usuária carrega base_v1_cliente.xlsx (gerado de base_fundacao.xlsx) no app_v1
Usuária configura conforme microcopy P-V1 (sem direção do Arquiteto sobre escolha de agrupador)
Resultado observado vira evidência:

Se CONCILIADO > 0 com config natural cliente → Cenário B confirmado · sub-sessão de revisão da entrada YAML
Se CONCILIADO = 0 mas resultado parece coerente com base sintética → Cenário A confirmado · entrada YAML nova ratificada
Se anomalia sintática (tipo erro de pipeline · não comportamento esperado) → Cenário C confirmado · sub-sessão investigação
Impacto:

Pendência rastreável · não débito esquecido (cumpre princípio C.2)
Prompt de abertura de VV-V1 carrega referência a esta D-XXX · Usuária e Arquiteto cientes
Resolução absorvida em D-XXX-VV-V1 conforme cenário descoberto
Não bloqueia A-V1 (motor já está pronto · independe da entrada YAML)

Referência canônica: Ressalva R1 da retrospectiva V-V1 · V-V1_AUDITORIA_BASE.md §3 · §4 · entrada V1 atualizada em bases/casos_esperados.yaml · planilha aba 2 V1 ganha nota "VV-V1: validar config canônica" no 6º quadrado.


## D-219 — git init no repositório TabloFlow · pré-A-V1
Data: 2026-04-26 noite · Bloco: V-V1 (retrospectiva) · Status: Aberta · ação Usuária solo
Contexto: Anomalia de ambiente reportada por Claude Code em V-V1 (seção 7 do V-V1_RELATORIO.md): "git status retorna fatal: not a git repository". Etapa de criar branch v-v1 do prompt V-V1 seção 1 foi pulada · trabalhos foram diretos na working copy · sem versionamento entre fases. Sessão V-V1 produziu ~5.000 linhas novas de código + 4 documentos · sem snapshot por fase. Risco de perda de estado em caso de incidente local.
Decisão: Usuária executa solo (5 min · sem necessidade de Claude Code): git init na raiz do repositório · git add . · git commit -m "estado pós-V-V1 · 26/04/2026 noite". Configurar .gitignore mínimo (excluir venv · pycache · .pytest_cache · arquivos de output local). Documentar em CONTEXT §X "Anomalias de ambiente endereçadas".
Razão: Ausência de versionamento Git é débito de processo de gravidade média (não bloqueia · expõe a riscos operacionais). Família A inteira pendente · sem versionamento corre risco de perder progresso. 5 min de execução · benefício imediato (commits entre fases de A-V1 protegem contra trava de Claude Code).
Impacto:

Repositório passa a ter histórico Git
A-V1 pode aplicar branch · commit por fase como salvaguarda interna
D-XXX no kit pós-A-V1 documentando que branch foi usada · estado da working tree preservado
Pré-requisito de A-V1 · timing: imediato pós-retrospectiva V-V1 · antes de qualquer próxima sessão Claude Code

Referência canônica: Anomalia 1 da Seção 7 do V-V1_RELATORIO.md · prompt V-V1 seção 1 (etapa branch).

## D-218 — S-V1 v2 §2.2 estendida · DUPLICIDADE detectada em todos os modos de match · não só EXATO
Data: 2026-04-26 noite · Bloco: V-V1 (retrospectiva) · Status: Fechada · cristalização de BIF-4
Contexto: S-V1 v2 §2.2 declara "Detecta duplicidade ANTES do match" sem especificar se em modo EXATO apenas ou em todos os 4 modos (EXATO · CONTEM · INICIA_COM · TERMINA_COM). Q5 do prompt V-V1 (decisão técnica pura · transparência D-131): ambiguidade definida como "n_candidatos > 1 em qualquer direção em modos não-EXATO" · sem mencionar DUPLICIDADE em não-EXATO. Claude Code (BIF-4) decidiu detectar DUPLICIDADE também em modos não-EXATO usando pré-varredura por chave · racional: "comportamento consistente é mais auditável · chave repetida em 1 lado é DUPLICIDADE independente do modo de match · era exigido por testes de matriz Bloco I (DUPLICIDADE × non-EXATO modes)".
Decisão: Aprovação retroativa de BIF-4 · cristalização da extensão · S-V1 v2 §2.2 ganha clarificação retroativa: "DUPLICIDADE detectada antes do match em todos os 4 modos · independentemente do modo configurado · razão: chave repetida em 1 lado é fenômeno estrutural da base · não comportamento de algoritmo de match". S-V1 v2.0 vira S-V1 v2.1 com ajuste de §2.2 OU adendo -bis retroativo (Arquiteto decide formato em sub-sessão de manutenção). Padrão herdado por V-V11.
Razão: Comportamento implementado é tecnicamente correto · auditável · simétrico entre modos. C.3 (zero invenção) marginalmente violada porque a S-V1 não declarava explicitamente · mas Claude Code declarou e justificou (transparência D-174 cumprida). Cristalizar evita ambiguidade futura · evita V-V11 implementar diferente · evita débito de método.
Impacto:

S-V1 v2 §2.2 ganha clarificação retroativa em sub-sessão de manutenção (junto com D-216 ou D-217 conveniente)
A-V1 docstring de _etapa_4a refletindo a regra
V-V11 herda padrão · documentado no prompt de V-V11 antes de Claude Code abrir
Cristalização documentada em CONTEXT §15.3 ou similar

Referência canônica: BIF-4 do V-V1_RELATORIO.md · visao_v1.py:1089-1308 (_etapa_4a_match_abas_distintas) · S-V1 v2.0 §2.2 · prompt V-V1 seção 1.3 (Q5).

## D-217 — Aba sintética dual_mesma_aba_colunas em base_fundacao.xlsx · pré-VV-V1
Data: 2026-04-26 noite · Bloco: V-V1 (retrospectiva) · Status: Aberta · sub-sessão pendente
Contexto: D-213 introduziu 2 ramos lógicos no pipeline V-V1 (ABAS_DISTINTAS / MESMA_ABA_EM_COLUNAS · 4 casos de upload). Auditoria YAML Q1.A (Fase 7 V-V1) constatou que base_fundacao.xlsx não tem aba projetada para testar MESMA_ABA_EM_COLUNAS (Caso 3 D-213: 1 aba com colunas Origem e Comparado distintas). V-V1 fechou ramo MESMA_ABA com 7 testes unitários sintéticos · sem aba real na base de Fundação · sem entrada em casos_esperados.yaml para esse caso lógico (aba_unica_caso_3: null declarado explicitamente).
Decisão: Sub-sessão dedicada antes de VV-V1: (a) adicionar aba dual_mesma_aba_colunas ao base_fundacao.xlsx com colunas pareadas (ex: Conta_Origem · Centro_Custo_Origem · Valor_Origem · Conta_Comparado · Centro_Custo_Comparado · Valor_Comparado) · ~80-120 linhas conforme padrão F-BASE · seed=42 preservado · (b) estender entrada V1 do YAML para cobrir Caso 3 (5-7 assertions: contagens · warnings DUP/AMB zerados · cobertura None · ponte ajuste_so_*=0) · (c) validar que executar_v1 produz contrato V1 coerente com aba sintética.
Razão: Sem aba real, MESMA_ABA_EM_COLUNAS não pode ser testado em VV-V1 · cliente de conciliação contábil frequentemente trabalha nesse formato (ex: Razao_Out2025 com colunas Saldo_Razao + Saldo_Balancete na mesma linha). É lacuna estrutural · não cosmética. Antecipar pré-VV-V1 evita VV-V1 ser parcial.
Impacto:

Sub-sessão Arquiteto + Claude Code · ~30-45 min Arquiteto + ~60-90 min Claude Code
bases/base_fundacao.xlsx ganha 15ª aba (atualização de D-140 · "14 abas" vira "15 abas" + D-XXX-bis)
bases/casos_esperados.yaml entrada V1 estendida (>= 17 assertions totais · ABAS_DISTINTAS + MESMA_ABA)
Regenerador de F-BASE atualizado para incluir aba nova com determinismo SEED=42
Pré-requisito de VV-V1 · timing: após A-V1 · antes de VV-V1

Referência canônica: BIF-7 do V-V1_RELATORIO.md · V-V1_AUDITORIA_BASE.md §3.4 · §6 · D-213 (4 casos lógicos) · D-140 (14 abas canônicas · invariante) · S-V1 v2.0 §2.1 ramo 4-B.

## D-216 — Contrato CelulaCampoV1 estendido para suportar ESTADO_SITUACAO categórico · pré-VV-V1
Data: 2026-04-26 noite · Bloco: V-V1 (retrospectiva) · Status: Aberta · sub-sessão pendente · prioridade alta
Contexto: S-V1 v2 §1.7 declara TipoCampoV1.ESTADO_SITUACAO (taxonomia DCV §4.3) · §1.6 mapeia default ESTADO_SITUACAO → unidade ADIMENSIONAL · §1.12 declara CelulaCampoV1 com valor_origem: Optional[Decimal] · valor_comparado: Optional[Decimal]. V-V1 implementou conforme: campos numéricos. BIF-6 do V-V1_RELATORIO.md: valores ESTADO_SITUACAO categóricos textuais (ex: "PAGO"/"PENDENTE"/"CANCELADO") são processados como Decimal · strings viram None · status_campo cai em SEM_VALOR_AMBOS silenciosamente. Violação de C.2 (nada silencioso) em cenário comum de conciliação contábil real.
Decisão: Catalogar como pré-requisito de VV-V1 (Validação Visual com base real cliente). Sub-sessão dedicada antes de VV-V1: estender CelulaCampoV1 para suportar valores textuais quando tipo_logico==ESTADO_SITUACAO. Duas opções de design a serem decididas em sub-sessão: (a) campos valor_str_origem: Optional[str] · valor_str_comparado: Optional[str] adicionais à célula · (b) novo contrato CelulaCampoTextoV1 paralelo · RegistroConciliadoV1.valores_por_campo aceita Union dos dois.
Razão: Conciliação contábil real frequentemente compara estados textuais não-numéricos · silenciar isso na V-V1 é débito que afeta diretamente Validação Visual (cliente carrega base · campo status_fatura · resultado todos SEM_VALOR_AMBOS · cliente conclui que sistema está quebrado). C.2 não negociável: ausência de valor numérico em campo categórico não é "valor ausente" · é "tipo incompatível com pipeline numérico" · merece warning explícito ou contrato adequado.
Impacto:

Sub-sessão pré-VV-V1 (cabe entre A-V1 e VV-V1) · 60-90 min Arquiteto · ~2-3h Claude Code
S-V1 v2 §1.12 estendida · vira S-V1 v2.1 OU adendo retroativo -bis
visao_v1.py atualizado · regras de cálculo §2.4 estendida (tabela determinística para campos categóricos)
Suite acrescenta ~10-15 testes específicos para ESTADO_SITUACAO categórico
V-V11 herda padrão (estados de contrato/status são comuns em V11 · aderência cadastral)
Risco se ignorar: VV-V1 falha em primeiro contato com cliente real · sub-sessão reativa custa mais

Sub-sessão prevista: S-V1-Evo-Categorico · pré-requisito explícito de VV-V1 · prioridade alta · não pode ser parqueado.
Referência canônica: BIF-6 do V-V1_RELATORIO.md · S-V1 v2.0 §1.6 · §1.7 · §1.12 · §2.4 · DCV-V1 §4.3 (taxonomia tipos) · CONTEXT §9 Camada A C.2 (nada silencioso).

## D-215 — UnidadeCanonica · promoção retroativa para Fundação · sub-sessão Refactor Dirigido pré-V-V11
Data: 2026-04-26 noite · Bloco: V-V1 (retrospectiva) · Status: Aberta · sub-sessão pendente
Contexto: S-V1 v2 §1.22 declara UnidadeCanonica como enum 8 valores (MONETARIO_BRL · PERCENTUAL · QUANTIDADE · TEMPO_DIAS · TEMPO_HORAS · MULTIPLICADOR · RAZAO · ADIMENSIONAL · catalogados em vocabulario_bilingue Bloco 10). D-202 (Sessão Promoção de Fundação · 26/04 tarde-noite) absorveu ColumnMeta.unidade da V2 mas implementou como Literal[...] · não como enum nominal. V-V1 precisava de UnidadeCanonica como enum · prompt vetou tocar contratos.py · Claude Code declarou enum local em visao_v1.py (BIF-0).
Decisão: Sub-sessão de Refactor Dirigido (D-206) · escopo: promover UnidadeCanonica de enum local em visao_v1.py para enum nominal em contratos.py · alinhar ColumnMeta.unidade e ContratoComparativo.unidade para usar a enum · zero mudança de comportamento observável (suite atual = gabarito). Pré-requisito de V-V11 (V-V11 vai precisar de UnidadeCanonica e não pode declarar 2ª cópia local · violação do princípio anti-duplicação D-202 item 3).
Razão: UnidadeCanonica é candidata canônica a transversal de Fundação (D-204 cláusula B · auditoria pós-V11 ratifica). Antecipar em sub-sessão dirigida pré-V-V11 economiza re-trabalho. Modalidade Refactor Dirigido D-206 aplicável: produto já existe (8 valores estáveis) · refactor é estrutural sem mudança comportamental · suite 978/979 é gabarito objetivo de "pronto".
Salvaguardas obrigatórias (D-206 · 4 pontos):

Suite atual 978/979 (1 vermelho herdado preservado) é gabarito · zero teste novo
Ordem: (a) declarar enum em contratos.py · (b) trocar Literal[...] em ColumnMeta · (c) trocar Literal[...] em ContratoComparativo · (d) remover enum local de visao_v1.py · (e) substituir imports · pytest entre cada etapa
Investigação prévia: Arquiteto produz prompt detalhado pré-existente · Claude Code só executa
Validação pós-refactor: suite verde + 0 testes novos + smoke visual de 5 min Usuária (rodar v2 + v1 em base de teste)

Impacto:

contratos.py ganha enum UnidadeCanonica (8 valores)
ColumnMeta.unidade muda de Literal[...] para UnidadeCanonica
ContratoComparativo.unidade idem
visao_v1.py remove declaração local · imports atualizados
vocabulario_bilingue.md Bloco 10 ratifica fonte canônica
V-V11 abre destravada · sem necessidade de declarar 2ª cópia local
Pré-requisito de V-V11 · timing: após A-V1 + VV-V1 · antes de V-V11

Referência canônica: S-V1 v2.0 §1.22 · BIF-0 do V-V1_RELATORIO.md · visao_v1.py:48-66 (enum local) · D-202 (Promoção de Fundação · UnidadeCanonica como Literal) · D-206 (Refactor Dirigido).

## D-214 — ConciliacaoV1Result.visao redundante com visao_id herdado · padrão divergente V1/V2 cristalizado
Data: 2026-04-26 noite · Bloco: V-V1 (retrospectiva combinada D-155) · Status: Fechada · candidata a normalização ALINHA-Auditoria-pós-V11
Contexto: S-V1 v2.0 §1.1 declarou visao: Literal["V1"] em ConciliacaoV1Result · VNResultBase (Fundação · D-130) já declara visao_id: Literal["V1", "V2", ..., "V11"]. V2Result (visao_v2.py) usa visao_id="V2" herdado · sem campo visao adicional. Conflito de nome detectado pelo Arquiteto durante produção do prompt V-V1 (26/04 noite). Usuária escolheu manter S-V1 v2 como está · ambos declarados (Pydantic permite override de Literal).
Decisão: Aprovação retroativa da escolha · Família A passa a ter padrão divergente V1/V2 sobre nome de campo identificador da visão (V1 declara ambos · V2 herda só visao_id). V-V1 implementa BIF-3 conforme: visao_id: Literal["V1"] (override) E visao: Literal["V1"] (S-V1 §1.1).
Razão: S-V1 v2 só foi aprovada horas antes · correção retroativa cabia em D-XXX simples mas Usuária optou por preservar a Spec aprovada · escolha legítima (Pydantic suporta · sem defeito técnico). Padrão divergente é débito de método de baixa prioridade · não merece sub-sessão própria · cabe na ALINHA-Auditoria-pós-V11 (D-204 cláusula B) quando família inteira for normalizada.
Impacto:

V1 e V2 divergem em nomenclatura de campo identificador da visão · documentar em V-V11 antes de copiar V1 cegamente (V11 deve decidir conscientemente · não herdar)
ALINHA-Auditoria-pós-V11 ganha item: "Normalizar V1.visao vs V2.visao_id · escolher padrão único Família A · estender para Famílias B/C/D/E"
Anotação no prompt de abertura de V-V11: "decidir nomenclatura · não copiar V1 sem confirmação"

Referência canônica: S-V1 v2.0 §1.1 · visao_v1.py:582-697 (ConciliacaoV1Result) · BIF-3 do V-V1_RELATORIO.md · prompt V-V1 seção 1.3 · D-130 (VNResultBase).

## D-213 — 4 casos lógicos de upload V1 · sistema infere automaticamente · sem radio "estrutura"
**Data:** 2026-04-26 · **Bloco:** S-V1 · **Status:** Fechada · estrutural
**Contexto:** S-V1 v1 declarava 2 estruturas de upload (Estrutura A · 2 arquivos · Estrutura B · 1 arquivo com 2 abas) com radio explícito na E1 · espelhando o que o DCV-V1 §3.1 sugeria. Erro: o DCV apresenta 2 estruturas de upload físico mas a S-V1 v1 colapsou isso com a decisão lógica do confronto (mesma aba vs abas distintas). Após reexplicação da Usuária · 4 casos lógicos foram identificados:
- Caso 1 · 2 arquivos · Origem em aba A do arquivo 1 · Comparado em aba B do arquivo 2
- Caso 2 · 1 arquivo (com N abas) · Origem em uma aba · Comparado em outra
- Caso 3 · 1 arquivo · 1 aba · Origem e Comparado em conjuntos de colunas distintos da mesma aba (cada linha é par já casado por construção)
- Caso 4 · 2 arquivos · 1 aba cada · em colunas (combinação rara · matematicamente válida)
Caso fora de escopo MVP (DCV §3.1 reafirmado): 1 aba · em linhas (coluna discriminadora) · exige RESHAPE prévio Módulo 2.
**Decisão:** A V1 separa fisicamente do logicamente:
- E1 (upload): decisão FÍSICA · n_arquivos ∈ {1, 2} · radio simples
- E1_OK (escolher abas): Usuária escolhe 1 ou 2 abas conforme n_arquivos
- E3 (configurar análise): Usuária aponta agrupadores e campos com (coluna_origem, coluna_comparado) · sem radio explícito de "estrutura"
- Sistema infere automaticamente o caso lógico (ABAS_DISTINTAS ou MESMA_ABA_EM_COLUNAS) a partir dos apontamentos
- Casos especiais bloqueados: B-V1-MESMA-COLUNA e B-V1-MISTURA-ABAS
**Razão:** O caso 3 (colunas distintas na mesma aba) é caso muito comum em conciliação contábil real · cliente típico tem `Razao_Out2025` em uma aba com colunas `[CNPJ, Filial, Valor_Razao, Valor_Balancete]` · não precisa nem deveria ser obrigado a fazer RESHAPE. S-V1 v1 errou ao classificar isso como "fora de escopo". Mas o caso fora de escopo (DCV §3.1 · "em linhas com discriminador") permanece fora · esse exige RESHAPE prévio. Inferência automática vs declaração explícita: cliente já está fazendo o trabalho conceitual quando aponta colunas (sabe se é mesma aba ou abas distintas) · radio extra seria redundância. Princípio C.5 atendido (sistema preserva e classifica · só observa apontamentos).
**Impacto:**
- ConciliacaoRealizadaV1: estrutura_entrada removido · n_arquivos + caso_logico_inferido adicionados
- Enum CasoLogicoV1 novo (2 valores)
- Pipeline ramifica em [4-A] ABAS_DISTINTAS · executa match · e [4-B] MESMA_ABA_EM_COLUNAS · pareamento linha-a-linha
- Classificações estruturais: 6 em ABAS_DISTINTAS · 2 ativas + 4 zerados em MESMA_ABA_EM_COLUNAS
- cobertura == None em MESMA_ABA_EM_COLUNAS
- Bloqueios novos: B-V1-MESMA-COLUNA · B-V1-MISTURA-ABAS · B-V1-MESMA-ABA removido
- P-V1 §3.2.1 + §4.2 + §4.7 corrigidas retroativamente em D-212 (consolidada)
**Referência canônica:** S-V1 §1.2 · §1.3 · §2.1 · §2.5 · §3.1 · DCV-V1 §3.1 (entendimento corrigido).

## D-212 — 3 correções retroativas em P-V1 · leiaute alinhado ao app V2 canônico
**Data:** 2026-04-26 · **Bloco:** S-V1 · **Status:** Fechada · correção retroativa
**Contexto:** Durante produção da S-V1 · 3 incoerências entre P-V1 v1.0 (aprovada em D-209) e o leiaute canônico do `app_v2.py` (suite 746/746 verde) foram identificadas:
1. P-V1 §2.7 declarava E4 "Configurações avançadas" com paleta + tratamento nulos + TED · contradizendo o leiaute V2
2. P-V1 §4.5 (Bloco 1 Paleta na E4) contradiz D-175 §5.4 (paleta no rodapé do RESULTADO · trocável a qualquer momento sem reprocessar)
3. P-V1 §4.5 (Bloco 3 TED em sidebar global D-153) contradiz D-178 (TED em expander "⚙️ Configurações avançadas" no topo · sai da sidebar)
P-V1 v1.0 foi produzida sem leitura disciplinada de `app_v2.py` · gerou divergências silenciosas com o leiaute canônico.
**Decisão:** P-V1 §2.7 e §4.5 corrigidas retroativamente em P-V1 v1.1:
- §2.7 mantido em "4 etapas + Revisão" (correto) · stepper canônico V1: "1 · Escolher arquivo(s)" · "2 · Identificar lados" · "3 · Configurar análise" · "4 · Agrupadores executivos" · "Revisar e executar"
- §4.5 corrigido · E4 contém somente "Agrupadores executivos" (multiselect 0-5 · opcional · pode pular)
- §4.5-bis novo · "TED · expander no topo" (paralelo D-178)
- §4.6 atualizado · 5 blocos canônicos paralelos a `_tela_resultado` da V2
- §4.6-bis novo · "Paleta no rodapé do RESULTADO" (paralelo D-175 §5.4)
- §4.1 · header declarado no topo (não sidebar) · TED no expander
- §4.2 corrigido junto com D-213 · Etapa 1 "Escolher arquivo(s)" com radio "Quantos arquivos?"
- §4.7 corrigido junto com D-213 · bloqueios B-V1-MESMA-COLUNA e B-V1-MISTURA-ABAS substituem B-V1-MESMA-ABA
**Razão:** Correções aplicadas a P-V1 antes de S-V1 ser aprovada · evita débito propagado para V-V1 e A-V1. Lição metodológica: P-V1 deveria ter sido produzida com leitura disciplinada de `app_v2.py` desde o início (não só `MOCKUP_V1_alpha2.md` · que cobria Excel mas não app). Catalogada como reforço de método: produção de P-V1 futuras inclui leitura obrigatória de `app_v[N-1].py` se a Família tem visão pioneira já implementada.
**Impacto:**
- P-V1 vira v1.1 · sobrescreve v1.0
- Vocabulário bilingue v4 inalterado (microcopy preserva)
- Arquitetura de abas do Excel inalterada (D-212 toca só app · não Excel)
- Wireframe HTML produzido em S-V1 reflete leiaute corrigido
- Sem mudança em D-209 (que aprovou P-V1 v1.0 · D-212 aplica correções mantendo aprovação)
**Referência canônica:** P-V1 v1.1 §2.7 · §4.1 · §4.2 · §4.5 · §4.5-bis · §4.6 · §4.6-bis · §4.7 · `app_v2.py` `_render_header` + `_tela_e4` + `_tela_resultado`. D-175 + D-178 são origens.

## D-211 — Q2.C · Épsilon da Ponte é TED editável por unidade global · 1 valor por unidade presente
**Data:** 2026-04-26 · **Bloco:** S-V1 · **Status:** Fechada
**Contexto:** P-V1 §3.7 declarou TED `epsilon_ponte` mas deixou TBD se editável e a granularidade. DCV-V1 §6.6 sugeriu fixo. P-V1 evoluiu para TED catalogado. 3 opções avaliadas (Q2.A fixo · Q2.B TED por campo · Q2.C TED por unidade global).
**Decisão:** Q2.C · `epsilon_por_unidade` como `dict[UnidadeCanonica, Decimal]` · TED editável · sidebar (corrigida em D-212 para expander no topo) mostra somente unidades efetivamente em uso pelos campos comparados configurados. Defaults canônicos por unidade: MONETARIO_BRL=0.01 · TEMPO_HORAS=0.01 · MULTIPLICADOR=0.0001 · demais=0. Aplicável C.D6 (DDU): default declarado · evidência visível na Aba 6 §6 · 1 clique para editar.
**Razão:** Equilibra simplicidade da UI (típico ~2-3 unidades em uso · não 8 entradas) com flexibilidade real (cliente avançado pode ajustar). Mantém princípio C.D6 sem exceção.
**Impacto:** campo epsilon_por_unidade em ConfigAplicadaV1 · TEDs catalogados em S-V1 §2.8 · expander populado dinamicamente após Etapa 3.2 · Diagnóstico §6 mostra status Default ou Editado por unidade.
**Referência canônica:** S-V1 §1.18 · §2.6 · §2.8 · §3.6.

## D-210 — Q1.B · Campos PERCENTUAL omitidos da Ponte de Conciliação · nota explicativa
**Data:** 2026-04-26 · **Bloco:** S-V1 · **Status:** Fechada
**Contexto:** P-V1 §3.6 declarou TBD para campos PERCENTUAL na Ponte. Soma de pontos percentuais multi-registro não fecha matematicamente. Q1.A (média ponderada · rótulos adaptados) · Q1.B (omite PERCENTUAL · nota) · Q1.C (soma p.p · nota técnica) avaliadas.
**Decisão:** Q1.B · campos PERCENTUAL não geram sub-Pontes. Aba 5 abre com banner explicativo quando todos os campos são PERCENTUAL. Status da Ponte (Resumo §4) ignora campos PERCENTUAL no cálculo do resíduo geral. Caso degenerado (todos PERCENTUAL · `len(pontes) == 0`) · Status retorna FECHA por convenção (vácuo lógico).
**Razão:** Implementação simples · conservadora · zero risco matemático. Honra C.5 (sistema declara o que não consegue fazer · não inventa cálculo). Cliente típico V1 (conciliação contábil · ERP × DW · folha) tem campos MONETARIO_BRL/QUANTIDADE como primários · PERCENTUAL é raro. Quando aparecer caso real · evolui para Q1.A em P-V1-Evo (média ponderada) sem quebrar contrato.
**Impacto:** invariante Pydantic em ConciliacaoV1Result.pontes · regra em S-V1 §2.6. F-APRESENT capability "Aba 5 bespoke" recebe pontes filtrado · não precisa novo capability adaptativa para PERCENTUAL.
**Referência canônica:** S-V1 §1.1 invariantes · §1.10 StatusPonteV1 · §1.16 PonteCampoV1 · §2.6 cálculo · §3.13 Grupo C checklist VVC.

## D-209 — P-V1 aprovada · 1ª P-VN sob método novo aplicada a visão nova · 8 P-α.3 absorvidas · vocabulario_bilingue estendido para v4
Data: 2026-04-26 noite · Bloco: P-V1 (1º quadrado do ciclo de 6 da V1) · Status: Fechada
Contexto: Sessão Mockup-V1 (D-208) ✅ concluída em 26/04 noite · gate D-203 / D-204 cláusula A satisfeito · A-V1 destrancado. Suite atual 746/746 verde (post-Promoção D-202 · capability 11 D-205 incluída). Mockup canônico MOCKUP_V1_alpha2.md (665 linhas · 13 seções · 8 defaults P-α.3 absorvidos como canônicos). Sessão P-V1 abriu como 1º quadrado da V1 · 1ª P-VN do método novo aplicada a visão nova (P-V2 retroativo de D-167 foi aplicação a visão existente). Modalidade Caminho A (pacote único · paraleliza Mockup-V1).
Decisão: P-V1 aprovada com 1.082 linhas · 5 seções canônicas (Paleta · Vocabulário · Arquitetura de abas · Microcopy · Checklist user-facing) + 5 seções de governança (Pegada V2 herdada · V1-específico catálogo Auditoria-pós-V11 · Ganchos para downstream · Pendências · Status · Referências). Zero P-V1-PROD-NN abertas (8 P-α.3 absorvidas como decididas · referências em P-V1 §8). Aplicação canônica de:

D-158 · ciclo de 6 artefatos · 1º quadrado fechado
D-160 · vocabulário user-facing exclusivo
D-161 · C.D6 DDU · default declarado em paleta + unidade + tolerância
D-164 · 4 paletas executivas
D-165 · Diagnóstico em 6 seções (ordem P-α.3-05: Configuração técnica primeiro)
D-166 · contrato de unidade por campo (18 campos do ConciliacaoV1Result)
D-168 · Azul executivo default universal
D-179 · lista negativa expandida (Bloco 9)
D-205 · capability 11 formato_adaptativo_por_unidade aplicada em todas colunas de valor
D-203/D-204 cláusula A · Mockup-V1 como gate satisfeito
D-208 · Mockup-V1 referência visual canônica

Razão: P-V1 é 2ª aplicação real do método novo da Família A (após V2 retroativa). Modalidade Caminho A (pacote único) validada como economia operacional vs D-019 (uma seção por vez) quando 8 P-α.3 já decididas pré-aprovação · sem necessidade de status-check por seção. Vocabulário bilingue estendido para v4 sem criar Bloco 11 (3 candidatos catalogados em P-V1 §6 ficam parqueados para ALINHA-Auditoria-pós-V11 · disciplina de não promover transversais antes da auditoria de família é vinculante · D-204 cláusula B). Custo da P-V1: ~25-35 min de produção · ~10 min de leitura/aprovação. Custo evitado pelo mockup pré-existente (D-208): retrabalho equivalente ao da V2 (15-25h cirúrgico) · matemática D-203 confirmada empiricamente.
Impacto:

p_v1.md vira /specs/produto/p_v1.md (canônico)
vocabulario_bilingue.md v4 substitui v3 · estende Bloco 3 (sub-blocos 3.0 + 3.1 + 3.2) e Bloco 6 (sub-blocos 6.0 + 6.1) · não cria Bloco 11
Planilha aba 2 V1 vira ✅⬜⬜⬜⬜⬜ (1º de 6 quadrados verde)
Planilha aba 1 linha "V1 sob método novo" atualiza para próxima sessão S-V1
S-V1 destrancado · 2º quadrado da V1 · próxima sessão Arquiteto
8 P-α.3 absorvidas catalogadas em P-V1 §8 · não viram pendências abertas
3 candidatos a Bloco 11 do vocabulário bilingue catalogados em P-V1 §6 · parqueados até ALINHA-Auditoria-pós-V11 (D-204 cláusula B)
Família A modelo agora consolida 12 classificações (6 V2 Bloco 3.0 · 6 V1 Bloco 3.1) + 6 status por campo V1 (Bloco 3.2) · base sólida para V11 herdar via aderência

Referência canônica: /specs/produto/p_v1.md · /specs/vocabulario_bilingue.md v4 · D-208 (mockup gate) · D-167 (precedente P-V2 retroativo) · D-158 (ciclo de 6 artefatos) · D-204 cláusula A satisfeita · D-204 cláusula B parqueada para pós-V11.

## D-208 — Mockup-V1 aprovado · gate D-203 / D-204 cláusula A satisfeito · A-V1 destrancado
**Data:** 2026-04-26 · **Bloco:** Mockup-V1 (modalidade β.3 · D-203) · **Status:** Fechada · vincula P-V1 / S-V1 / A-V1
**Contexto:** D-203 instituiu mockup Excel-alvo como gate operacional para visões pioneiras de cada família (V1 da Família A · V4 da Família C · V3 da B · V7 da D · V5 da E). D-204 cláusula A formalizou o gate como vinculante. Mockup-V1 foi a 1ª aplicação prática da modalidade β.3 (Usuária esboça · Arquiteto detalha · Usuária aprova) · executada em 26/04/2026 noite imediatamente após Sessão Promoção D-202 fechar Camada 2.
**Decisão:** Mockup-V1 (`MOCKUP_V1_alpha2.md` · 665 linhas · 13 seções) aprovado em Caminho A pela Usuária após leitura completa de α.2. 8 pendências P-α.3-01 a P-α.3-08 absorvidas como defaults canônicos (ver tabela em Mockup-V1 §12). Gate D-203 / D-204 cláusula A satisfeito.
**Estrutura aprovada:**
- 6 abas (Resumo Executivo · Resumo por Agrupador condicional · Mapa de Conciliação · Análise Analítica · Ponte de Conciliação · Diagnóstico)
- Resumo Executivo com 9 seções (Cabeçalho · Taxa de Conciliação · Volumetria · Status da Ponte NOVO · Valor por campo · Cobertura · Resumo por agrupador · Síntese Diagnóstico · Configuração) + Leitura Qualitativa fechando
- Coração Visual distribuído (Mapa aba 3 + Ponte aba 5) · sem aba/seção dedicada
- Aba 3 = Mapa de Conciliação com todos os registros + classificação como coluna + filtro padrão
- Aba 4 = Análise Analítica com expansão por campo comparado
- Status da Ponte como seção 4 do Resumo · 1 linha grande de status com ícone+cor
- Leitura qualitativa só no Resumo · mais longa que V2 (cobre 6 classes + Status da Ponte)
**Razão:** 1ª aplicação real da modalidade β.3 confirma a viabilidade operacional do gate (custo ~30-45 min Arquiteto + ~15 min Usuária · vs. potencial 15-25h de retrabalho V2-style sem mockup). Caminho A com leitura completa demonstra que detalhamento técnico do Arquiteto cobriu o esboço da Usuária com fidelidade · sem precisar de iteração.
**Impacto:**
- Gate D-203 satisfeito · A-V1 destrancado
- P-V1 (Spec de Produto) consome `MOCKUP_V1_alpha2.md` como referência canônica · estende Bloco 3 do vocabulário com 6 classificações V1 · pode estender Bloco 10 se necessário
- 8 defaults P-α.3 viram parte canônica do mockup
- Roadmap operacional pós-Mockup-V1: P-V1 → S-V1 → V-V1 → A-V1 → VV-V1 → V11 → Auditoria pós-V11 (D-204 cláusula B · gate antes de Família C)
- Padrões V1-específicos catalogados (§10 do mockup) como candidatos a transversais Família A · revisitados na Auditoria pós-V11
**Referência canônica:** `MOCKUP_V1_alpha2.md` é o mockup aprovado · D-208 vincula gate · D-203 origem · D-204 cláusula A operacionaliza.

## D-207 — Princípios consolidados Família A · 4 lições canônicas para todas as famílias futuras
Data: 2026-04-26 · Bloco: ALINHA-Lições-Família-A · Status: Fechada · canônica · vincula a partir de Família B
Contexto: ALINHA-Lições-Família-A foi convocada explicitamente como sessão de destilação (D-200) das lições acumuladas das Sessões 4-ter / 4-ter-bis / 5 / 6 / 7 / 8 / 8.1 / 8.2 / 8.3 / 8.4. Inventário operacional V2→Fundação produzido na sessão revelou padrões consistentes que se promovem a princípios canônicos para Famílias B/C/D/E.
Decisão: Adoção de 4 princípios canônicos consolidados a partir da Família A:
Princípio 1 · "Excel é o produto · Spec textual não basta"
Toda visão produz Excel · Excel é entrega final · Excel deve ser visto como artefato concreto antes de existir como código. Mockup Excel-alvo (D-203) operacionaliza · gate (D-204 cláusula A) torna obrigatório.
Princípio 2 · "Cada família tem checkpoint estrutural depois da 1ª visão"
Vazamento de camada (visão consumindo o que deveria ser Fundação) só é detectável pós-fato. Auditoria pós-1ª visão (D-204 cláusula B) torna detecção obrigatória · não opcional. ALINHA-Lições-Família-A é a aplicação retroativa deste princípio para a Família A.
Princípio 3 · "Decisão estrutural não pode viver só em comentário de código"
Conhecimento institucional preservado em D-XXX formal · não em "Sessão X · C-N" espalhado em código. D-204 cláusula C torna vinculante · com cleanup retroativo aplicado em D-202.
Princípio 4 · "Refactor ≠ Invenção · método deve diferenciar"
Refactor (promover algo que já funciona) tem critério de pronto objetivo (suite passa) e cerimonial muito menor que invenção (algo novo). Forçar 3 fases D-185 em refactor é over-engineering. Refactor Dirigido (D-206) cristaliza modalidade própria.
Razão: Os 4 princípios surgem de manifestações concretas da Família A (V2 fechada com 4 sub-sessões cirúrgicas · não especulação). Cristalizá-los como princípios protege Famílias B/C/D/E de redescobrir as mesmas lições no próprio retrabalho. Custo da cristalização (esta D-XXX + impacto em CONTEXT/Instruções) é desprezível vs. valor agregado em 4 famílias futuras × 5-10 sessões cada.
Impacto:

CONTEXT v3.5 §18 nova "Princípios consolidados Família A · canônicos para famílias futuras"
Instruções v3.4 referenciam os 4 princípios na seção "Como me usar como Arquiteto"
GLOSSARIO v5 ganha entrada por princípio com referência canônica a esta D-XXX
Quando Família B começar (após V11 fechar) · Arquiteto e Claude Code entram com os 4 princípios já internalizados · zero dependência de redescoberta empírica

Referência canônica: D-207 princípios · D-200 destilação · D-203 / D-204 / D-205 / D-206 operacionalizam.

## D-206 — Padrão de condução "Refactor Dirigido" · 5ª modalidade canônica do método
Data: 2026-04-26 · Bloco: ALINHA-Lições-Família-A · Status: Fechada · padrão de método
Contexto: D-185 cristalizou padrão 3 fases (investigação · implementação · validação humana iterativa) para sessões de natureza "investigação + correção + validação". Aplicado com sucesso em V2 retroativa (Sessões 5 a 8.4). Sessão de Promoção de Fundação (D-202) tem natureza estruturalmente diferente: refactor sobre código que já funciona · suite atual é gabarito · sem invenção · sem descoberta. Aplicar D-185 com 3 fases completas seria over-engineering · cerimonial 6× maior que valor agregado.
Decisão: Adoção de "Refactor Dirigido" como 5ª modalidade canônica do método TabloFlow · ao lado de:

Sessão Marco (ALINHA · D-142 · 4 sub-blocos α/β/γ/δ)
Sessão A-VN (Aplicação de Visão · gate duplo D-174 · 3 fases D-185)
Sub-sessão cirúrgica (correção dirigida pós-Camada 2 · escopo cirúrgico fechado)
Sessão combinada (D-155 · prompt + retrospectiva em 1 bloco)
Refactor Dirigido (NOVO · D-206)

Definição: Sessão Claude Code única · escopo grande mas coerente em natureza (camada/subsistema inteiro) · onde o produto a ser entregue já existe e funciona em alguma forma · refactor promove para arquitetura nova sem mudança de comportamento observável. Critério de pronto objetivo: suite atual passa + validação visual mínima de smoke test em 1 base de teste. Não exige mockup novo. Não exige Camada 2 humana extensa. Não confunde com sessão de invenção.
4 salvaguardas obrigatórias do Refactor Dirigido:

Suite atual é gabarito · zero teste novo necessário · zero invenção · "pronto" = mesmos testes verdes que estavam verdes antes
Ordem interna do refactor protege contra cascata · Claude Code valida pytest entre etapas internas · vermelho para imediatamente · não avança
Investigação prévia feita pelo Arquiteto · Claude Code só executa plano detalhado pré-existente · não descobre estrutura durante execução
Validação pós-refactor é objetiva · suite verde + 1 smoke visual curto (15-20 min Usuária em 1 base de teste) · não Camada 2 humana extensa

Razão: Reconhecer formalmente que retrabalho ≠ invenção é o que permite "produtividade sem perder controle" (declaração explícita da Usuária na ALINHA-Lições-Família-A). 4 salvaguardas tornam Refactor Dirigido seguro sem cerimonial de invenção. 1ª aplicação é D-202 (Sessão Promoção de Fundação · 26/04 noite). Aplicações futuras prováveis: refactor de motor base · reestruturação de F-APRESENT · qualquer promoção em massa de bespoke V-N para capability genérica.
Impacto:

Instruções v3.4 ganham seção "Refactor Dirigido · 5ª modalidade" com as 4 salvaguardas explícitas
CONTEXT v3.5 §15 (conceitos pós-Retroação-V2) ganha sub-item Refactor Dirigido
GLOSSARIO v5 entrada nova
Reconhecível pra Sessão Promoção (D-202) · pra eventual refactor de motor · pra reestruturação F-APRESENT futura

Referência canônica: D-206 padrão · D-185 estendida · D-202 1ª aplicação.

## D-205 — P-37 resolvido · formato adaptativo por unidade · tabela default canônica · Caminho δ
Data: 2026-04-26 · Bloco: ALINHA-Lições-Família-A · Status: Fechada · constitucional (extensão de C.D8) · implementação técnica em D-202
Contexto: P-37 (apresentação numérica esconde precisão real · descoberto na Camada 2 da Sessão 8.4 com base TEMPO_HORAS · linha 5,40h → 5,06h real exibe "5h vs 5h · Diferença -0h · Variação -6,30%") foi catalogado para resolução em D-200 com 4 caminhos iniciais (α arredondar internos · β casas decimais · γ nota técnica · δ formato adaptativo). Caminho α viola C.5 (TabloFlow analisa · nunca decide pelo dado). Caminho β puro deixa TEMPO_HORAS sempre ruidoso quando valor real é inteiro. Caminho γ trata sintoma · não causa. Caminho δ é única solução estrutural.
Decisão: Adoção do Caminho δ · Formato Adaptativo por Unidade. Cada unidade canônica tem regra própria de apresentação que combina:

(a) casas decimais default
(b) regra de adaptação quando valor real tem fração não-trivial
(c) nota técnica condicional quando arredondamento esconde variação material

Tabela default canônica · 8 unidades:
UnidadeCasas decimais defaultRegra adaptativaNota técnicaMONETARIO_BRL2 (R$ 1.234,56)nunca mudasó se Δ centavos for material em %PERCENTUAL2 (12,34%)nunca mudanuncaQUANTIDADE0 (1.234)se valor real tem fração ≥0,5 → 1 casa decimalse variação ≥5% e arredondados ficam iguaisTEMPO_DIAS0 (5d)se fração → 1 casa decimalmesma regra QUANTIDADETEMPO_HORAS0 (5h)se fração → 1 casa decimalmesma regra QUANTIDADEMULTIPLICADOR2 (2,50×)nunca mudasó em casos extremosRAZAO4 (0,1234)nunca mudanuncaADIMENSIONAL2nunca mudanunca
Implementação técnica em D-202 · capability nova em F-APRESENT:

apresentacao/formatos.py ganha formato_adaptativo_por_unidade(valor: float, unidade: str) -> Tuple[str, Optional[str]] retornando (string formatada · nota técnica opcional)
Tabela vira constante _REGRAS_FORMATO_ADAPTATIVO em formatos.py
number_format_valor antigo preservado para compatibilidade · novo dispatcher consome adaptativo quando contexto exige
Templates de apresentação (Saúde da comparação · Resumo Executivo · Matriz · Base Analítica) consomem adaptativo

Razão:

Caminho α (arredondar internos) viola C.5 · TabloFlow estaria mentindo sobre o dado
Caminho β puro (casas decimais fixas) deixa TEMPO_HORAS sempre "5,00h" quando valor real é exatamente 5h · ruído desnecessário
Caminho γ (só nota técnica) trata sintoma · cliente vê alerta sem entender · pode até diminuir confiança no produto
Caminho δ é única solução que respeita C.5 · respeita produto · pensa cada unidade uma vez para sempre · 11 visões herdam

Impacto:

F-APRESENT capability 11 nova · "formato adaptativo por unidade"
D-205 vincula tabela default · Usuária pode propor ajuste por unidade durante D-202 ou em ALINHA futura
Resolve manifestação P-37 da Sessão 8.4 · protege todas as 11 visões e todas as bases futuras de clientes
Vincula a C.D8 (D-190 · Unidade declarada universal) como extensão de apresentação
vocabulario_bilingue v5 ganha referência cruzada Bloco 10 ↔ tabela δ

Referência canônica: P-37 fechada · D-205 nova · C.D8 (D-190) estendida · D-202 implementação técnica.

## D-204 — Cláusulas anti-vazamento Fundação→Visão · tripla proteção A+B+C
Data: 2026-04-26 · Bloco: ALINHA-Lições-Família-A · Status: Fechada · constitucional · vincula a partir de V1
Contexto: Inventário V2→Fundação produzido na ALINHA-Lições-Família-A (D-200) revelou que vazamento Fundação→Visão em V2 não foi acidental · foi consequência de 3 falhas combinadas no método: (1) Spec não enxergava produto Excel · S-V2 falava de contrato + cálculo + wireframe · não de Excel-alvo · Claude Code interpretou Excel a partir de inferências · (2) Não havia checkpoint pós-V2 · ninguém parou e perguntou "isso pertence a V2 ou pertence à Fundação?" depois de V2 fechar · (3) Comentários no código viraram registro silencioso · 86 referências a "Sessão X · C-N" e "D-XXX" espalhadas em V2 substituíram D-XXX formais.
Decisão: Adoção de 3 cláusulas combinadas que tornam vazamento Fundação→Visão impossível ou ruidoso (tripla proteção):
Cláusula A · "Mockup é gate · não recomendação"
Nenhuma sessão A-VN abre sem mockup Excel-alvo aprovado quando a visão é pioneira de família. Mockup ausente bloqueia a sessão · Arquiteto recusa gerar prompt Claude Code até existir.
Operacionalizada por D-203 (escopo β.3 com escape · 5 mockups totais ao longo do projeto).
Cláusula B · "Auditoria estrutural pós-1ª visão de família"
Toda família · ao terminar 1ª visão completa em VV-VN ✅ · entra em sessão obrigatória de auditoria estrutural antes de abrir 2ª visão. Auditoria responde 1 pergunta por arquivo *_vN.py da visão pioneira: "isso aqui pertence a esta visão · ou pertence à Fundação?". Promoções identificadas viram sub-sessão de Promoção · sem promoção identificada, declara-se "auditoria limpa" e segue.
Aplicada retroativamente em ALINHA-Lições-Família-A (essa sessão é a auditoria pós-V2 · ainda que tenha vindo tarde · D-200 inventário é o produto dela). Aplicação futura obrigatória: pós-V11 antes de V4 · pós-V4 antes de V10 · pós-V3 antes de V8 · pós-V7 antes de V9 · pós-V5 antes de V6.
Cláusula C · "Comentário em código não substitui D-XXX"
Comentários do tipo "Sessão X · C-N" ou "D-XXX" no código de produção são marcadores temporários · não documentação. Toda decisão estrutural que aparece como comentário em código deve ter D-XXX correspondente em DECISIONS.md em até 24h após a sessão. Comentário sem D-XXX correspondente é débito de método · catalogado e resolvido na auditoria pós-família (Cláusula B).
Aplicação imediata: 86 comentários históricos atuais em V2 são absorvidos no cleanup da Sessão Promoção (item 7 do inventário · D-202).
Como as 3 cláusulas conversam:
CláusulaQuando atuaTipo de proteçãoA · Mockup é gateAntes de A-VN abrirPreventiva (impede problema de aparecer)B · Auditoria pós-famíliaDepois de 1ª visão fecharDetectiva (descobre problema cedo)C · Comentário ≠ D-XXXDurante sessões + auditoriaEstrutural (preserva conhecimento)
Razão: V2 demonstrou empiricamente as 3 falhas combinadas. Cada cláusula resolve 1 falha · 3 cláusulas combinadas dão tripla proteção. Custo total agregado ~5-7.5h adicionais ao longo do projeto inteiro vs. ~20-40h de retrabalho como aconteceu em V2 (4 sub-sessões cirúrgicas em V2 foram a manifestação · não a cura). Matemática favorável.
Impacto:

CONTEXT v3.5 §17 nova "Cláusulas anti-vazamento Fundação→Visão"
Instruções v3.4 ganham seções "Auditoria estrutural pós-1ª visão de família" e "Comentário ≠ D-XXX"
Padrão D-185 (3 fases) ganha quarta-fase implícita ("auditoria pós-família" como Fase d aplicada apenas no fechamento da 1ª visão de família)
Planilha aba 1 ganha horizonte "Auditoria pós-V11" · "Auditoria pós-V4" · etc.

Referência canônica: D-204 cláusulas · D-203 implementa A · D-202 absorve C · futuras auditorias B aplicadas em todas as famílias.

## D-203 — D-191 promovida · mockup Excel-alvo é gate operacional · escopo β.3 com escape
Data: 2026-04-26 · Bloco: ALINHA-Lições-Família-A · Status: Fechada · vincula a partir de V1
Contexto: D-191 (mockup Excel-alvo · 25/04/2026) foi anotada como proposta provisória · vencimento na ALINHA-Lições-Família-A (D-200). Hoje vence. Sessões 4-ter / 4-ter-bis / 8 / 8.1 / 8.2 / 8.3 / 8.4 demonstraram empiricamente que Spec textual + wireframe HTML não bastam para garantir Excel correto · Claude Code interpreta camada de produto Excel a partir de inferências · descoberta visual tardia gerou 4 sub-sessões cirúrgicas na V2 (~15-25h reais). Provisória está pronta para virar padrão.
Decisão: D-191 vence formalmente. Adotada como gate operacional com escopo β.3 com escape:
Escopo β.3:

Mockup obrigatório antes de qualquer A-VN da 1ª visão de cada família (5 mockups totais ao longo do projeto):

V1 da Família A
V4 da Família C
V3 da Família B
V7 da Família D
V5 da Família E


Visão filha herda visualmente da pioneira:

V11 herda de V1
V10 herda de V4
V8 herda de V3
V9 herda de V7
V6 herda de V5


Escape declarado: se durante trabalho da visão filha aparecer divergência visual material com a mãe · mockup é puxado pontualmente · não regra rígida

Modalidade de produção (β.3):

Usuária esboça seções (o que tem que aparecer · ordem · ênfase · vocabulário desejado)
Arquiteto detalha (vocabulário bilingue · paleta · formatação numérica · contrato unidade D-205 · microcopy)
Usuária aprova o mockup detalhado antes de prompt Claude Code abrir

Gate: Arquiteto recusa gerar prompt Claude Code de A-VN pioneira sem mockup aprovado em mãos. Vincula como Cláusula A da D-204.
Razão: V2 retroativa demonstrou que o ciclo "Spec → Claude Code → Camada 2 reprovada → 4 sub-sessões cirúrgicas" custa ordens de magnitude mais que o ciclo "Mockup → Spec → Claude Code → Camada 2 aprovada em 1 rodada". Custo agregado de mockups β.3 ao longo do projeto: ~2.5h (5 mockups × ~30 min). Custo evitado: ~15-25h por visão × 5 famílias = potencialmente 75-125h de retrabalho. Matemática esmagadora.
Impacto:

Ciclo de 6 artefatos (D-158) ganha gate intermediário entre P-VN e S-VN para visões pioneiras · com Mockup-VN como artefato auxiliar (não 7º quadrado · pré-condição)
CONTEXT v3.5 §15 (conceitos consolidados) ganha "Mockup Excel-alvo · gate β.3"
Instruções v3.4 ganham seção "Mockup Excel-alvo · modalidade β.3" descrevendo papéis (Usuária esboça · Arquiteto detalha · Usuária aprova)
1ª aplicação: V1 da Família A · após Sessão Promoção (D-202) concluída · próximo bloco operacional

Referência canônica: D-191 vence/substituída · D-203 nova · D-204 Cláusula A consome.

## D-202 — Sessão de Promoção de Fundação · Opção D · refactor dirigido em sessão única · 4 salvaguardas
Data: 2026-04-26 · Bloco: ALINHA-Lições-Família-A · Status: Agendada · Marco · execução 26/04 tarde-noite
Contexto: D-197 (débito de Fundação · 25/04/2026) declarou bloqueante pré-V1 com escopo provisório de 5 itens. ALINHA-Lições-Família-A (D-200) foi convocada para refinar escopo. Inventário V2→Fundação produzido na sessão (Bruna leu 9.072 linhas dos arquivos visao_v2.py · exportacao_v2.py · app_v2.py · contratos.py · exportacao.py · motor_base.py · motor_upload.py · spec_v2.md · vocabulario_bilingue.md) revelou 5 itens críticos + 3 itens altos · não 1 como D-197 sugeria. Avaliadas 4 modalidades de execução (Big Bang ingênua / Fatiada por item / 3 sessões por camada / Refactor Dirigido).
Decisão: Sessão de Promoção de Fundação executa em modalidade Refactor Dirigido (D-206) · 1 sessão Claude Code grande · escopo coerente · 4 salvaguardas. Promove os 5 itens críticos + 3 altos do inventário em ordem de refactor protegida contra cascata.
Inventário promovido (8 itens · ordem de refactor):
🔴 Itens críticos (bloqueantes V1):

Cria ContratoComparativo em contratos.py (12 campos · genérico Família A) copiando estrutura de ComparacaoV2 · ComparacaoV2 herda de ContratoComparativo · zero quebra de contrato externo
Adiciona unidade e tipo_campo ao ColumnMeta (camada analítica de coluna em camada estrutural · resolve raiz de D-197)
Move _default_unidade_para_tipo para apresentacao/formatos.py · app_v2 e visao_v2 passam a importar · deduplica entre 2 arquivos
Corrige bugs conhecidos das capabilities 7 e 10 da F-APRESENT (Resumo Executivo serializa chave_agrupadores como str(dict) em fallback · Diagnóstico formata TODOS thresholds como percentual ignorando contrato D-166)
Extrai sub-templates de _renderizar_resumo_executivo_v2 (1.000+ linhas) para apresentacao/templates/familia_a/:

saude_comparacao.py (E2)
concentracao.py (E3a)
onde_se_concentra.py (E3b)
leitura_qualitativa.py (E3c)
variacoes_destaque.py
exportacao_v2.py passa a chamar templates · 1.000 linhas viram ~200



🟠 Itens altos (não bloqueiam V1 mas vão doer):

Promove _construir_leitura_qualitativa_v2 para template parametrizado consumível por V1/V11/restantes · ramificação por unidade + por semântica + por tipo_campo preservada
Resolve P-37 (D-205) · capability 11 nova formato_adaptativo_por_unidade em F-APRESENT · tabela δ canônica
Cleanup dos 86 comentários "Sessão X · C-N" redundantes (Cláusula C de D-204) · cada comentário ou (a) tem D-XXX correspondente · ok mantém · ou (b) é órfão · catalogar como débito ou remover

🟡 Item deferido (decisão consciente):

D-189 (compressão silenciosa de vocabulário) · NÃO entra na Sessão Promoção · família A não precisa de CATEGORICO/BOOLEANO no tipo_campo · decisão fica para abertura de Família B (composição · onde categóricos podem ser eixo)

4 salvaguardas obrigatórias (definidas em D-206):

Suite atual 731 verde é gabarito de pronto · sem testes novos exigidos · refactor pronto = 731 testes seguem verdes
Ordem de refactor protege contra cascata · contratos primeiro (não toca código de execução) → apresentação (consome contratos novos) → cleanup · pytest entre etapas · vermelho para imediatamente
Investigação prévia já feita · inventário D-200 · Claude Code só executa plano · não descobre estrutura
Validação pós-refactor objetiva · suite verde + 1 base TEMPO_HORAS no app · 15-20 min Usuária · não Camada 2 humana extensa

Razão:

Inventário D-200 mostrou que escopo era 5× maior que D-197 sugeria · 1 sessão dedicada de 60-90 min era ingenuidade
Big Bang sem critério de pronto seria catastrófico
5 sub-sessões fragmentadas replicariam padrão 8.1-8.4 que cansou Usuária
3 sessões por camada (Opção C) trazem cerimonial 6× maior que valor agregado
Refactor Dirigido (D-206) aproveita que retrabalho ≠ invenção · suite atual é gabarito objetivo · sem cerimonial de invenção
Declaração explícita da Usuária: "produtivo sem perder controle"

Timeline: 26/04 tarde-noite (decisão da Usuária · sem ajuste).
Impacto:

1 prompt único Claude Code (~3-4h execução)
1 camada 2 curta (~15-20 min Usuária)
V1 destrancada após validação
CONTEXT v3.5 §16 reescrita (substitui escopo D-197 com escopo D-202 detalhado)
Suite cresce em ~10-15 testes (helpers de formato adaptativo · novos testes de templates)
exportacao_v2.py reduz de 2.313 linhas para ~1.200-1.400
app_v2.py reduz ~30 linhas (deduplicação _unidade_default_por_tipo)
Cleanup de 86 comentários históricos
D-197 substituída por D-202 (escopo refinado · modalidade Refactor Dirigido D-206)

Próximo passo após D-202 fechar: Mockup-V1 produzido em modalidade β.3 (D-203) · depois P-V1 / S-V1 / B-V1 (dispensada · base_fundacao) / V-V1 / A-V1 / VV-V1.
Referência canônica: D-200 inventário · D-202 escopo refactor · D-197 vence/substituída · D-206 modalidade · D-205 P-37 absorvido · D-203 mockup pré-V1 · D-204 cláusulas anti-vazamento.

### D-201 — V2 retroativa fechada como ✅✅✅✅✅✅ · 1ª aplicação da Família A sob método novo concluída
**Data:** 2026-04-25 · noite · **Bloco:** ALINHA-Descoberta-Unidade · **Status:** Fechada · Marco operacional
**Contexto:** ALINHA-Descoberta-Unidade abriu em 25/04/2026 manhã (Sessão 7) consolidando 5 evoluções de produto V2 + 13 D-XXX (D-186 a D-198). Sessão 8 (tarde) implementou Camada 1 (725 testes verdes · 5 evoluções E1-E3c). Camada 2 da Sessão 8 reprovou por 6 achados visuais críticos. Sessão 8.1 (fim de tarde) corrigiu os 6 (731 testes verdes). Camada 2 da Sessão 8.1 reprovou fechamento por 7 débitos remanescentes (P-28 a P-34) · D-198 declarou que V2 NÃO fecha em 25/04 manhã. Sub-sessões 8.2 + 8.3 + 8.4 (noite) corrigiram os 3 bloqueantes (P-29 · P-30 · P-31) e 2 achados emergentes (P-35 regressão default · P-36 gráfico sobrepondo). Camada 2 final validou Excel produto + tela RESULTADO + Saúde da comparação + Concentração + Onde se concentra + Leitura qualitativa + Variações em destaque · 5 evoluções todas funcionais nas 3 unidades testadas (MONETARIO_BRL · PERCENTUAL · QUANTIDADE) e em TEMPO_HORAS adicionalmente. P-37 (achado estrutural transversal de produto · descoberto na validação TEMPO_HORAS) catalogado para D-200 · não-bloqueante porque motor está matematicamente correto.
**Decisão:** V2 retroativa **FECHADA** com status ✅✅✅✅✅✅ · 6 quadrados verdes:
- ✅ P-V2 (Spec de Produto · 23/04 noite)
- ✅ S-V2 (Spec técnica · 22/04 + adendo §2.4)
- ✅ B-V2 (base · base_fundacao + bases percentual + horas + quantidade testadas)
- ✅ V-V2 (motor · 731 testes verdes · NEUTRA expandida D-187 · 12/12 T-SEMA cobertura · cache D-186)
- ✅ A-V2 (app + Excel · 5 evoluções E1-E3c · helpers de unidade · gráfico reposicionado · Leitura qualitativa robusta)
- ✅ VV-V2 (Validação Visual Construtora · Camada 2 da Usuária aprovou · 4 sessões iterativas com investigação dirigida + correção dirigida + validação humana)
**Razão:**
- 1ª aplicação completa do ciclo de 6 artefatos D-158 sob método novo (com gate duplo D-174 · padrão 3 fases D-185 · investigação dirigida + escopo consolidado + validação humana iterativa)
- 7 P- catalogados como backlog estrutural (P-28 · P-31 · P-32 · P-33 · P-34 · P-37) com encaminhamento claro · não-bloqueantes para fechar V2
- Lição metodológica fundamental confirmada: gate duplo D-174 funciona apenas se Camada 2 humana for executada com tempo · paciência · base real do cliente · não só base sintética
- D-185 padrão 3 fases evitou correções fragmentadas mesmo em sub-sessões iterativas (8.1 · 8.2 · 8.3 · 8.4 · cada uma com escopo cirúrgico fechado)
- Usuária aplicou critério de produto correto (D-198) ao recusar fechamento prematuro · Arquiteto revisou · alinhou
**Impacto:**
- Planilha aba 2 · V2 vai de ⚠️⚠️ para ✅✅✅✅✅✅
- ALINHA-Descoberta-Unidade fechada de fato (não mais "parcialmente fechada")
- Próximo Marco: ALINHA-Lições-Família-A (D-200) · agendada para 26/04/2026 manhã
- Próxima sessão operacional após ALINHA: Sessão de Promoção de Fundação (resolve D-197 + P-37 cross-visão)
- V1 e V11 da Família A só iniciam após Promoção de Fundação concluída
**Referência canônica:** D-201 · D-198 (fechada como satisfeita) · D-194 (5 evoluções implementadas) · planilha v4.

---

### D-200 — ALINHA-Lições-Família-A formalmente agendada · 26/04/2026 manhã · cabeça fresca · pauta consolidada
**Data:** 2026-04-25 · noite · **Bloco:** ALINHA-Lições-Família-A · **Status:** Agendada · Marco
**Contexto:** D-193 declarou roadmap operacional pós-V2 com ALINHA-Lições-Família-A como próximo Marco após V2 fechar. Com V2 fechada em D-201 · ALINHA-Lições-Família-A passa de "agendada para depois de V2 fechar" para "agendada formalmente para 26/04/2026 manhã". Cabeça fresca · 90-120 min · padrão D-142 com 4 sub-blocos α/β/γ/δ.
**Decisão:** ALINHA-Lições-Família-A **agendada para 26/04/2026 manhã** com pauta consolidada:

**Pauta principal · D-197 · Promoção de Fundação (BLOQUEANTE pré-V1):**
1. Avaliar se `unidade` deve viver em contrato genérico de Fundação (campo em ColumnMeta · ou EspecificacaoCampo nova) · não só em ComparacaoV2
2. Promover lógica de despacho por unidade (que hoje vive em exportacao_v2.py) para capability genérica de F-APRESENT
3. Promover template de Leitura qualitativa para consumível por V1/V11/restantes
4. Garantir que tela RESULTADO consome helpers automaticamente em V1/V11 (não só V2)
5. Adicionar smoke tests visuais cross-visão (D-196 estendido)

**Pauta complementar · 5 itens estruturais:**
6. **P-37 · INSIGHT CRÍTICO de produto** (NOVO · agora em D-200 com prioridade ALTA): "O sistema está calculando com base nos valores reais e exibindo arredondado no resumo" · 4 caminhos de solução (α arredondar internos · β casas decimais · γ nota técnica · δ formato adaptativo por unidade). Decisão única cross-visão · resolução na sessão de Promoção de Fundação.
7. **D-189 · Compressão silenciosa de vocabulário** · decisão: restaurar CATEGORICO/BOOLEANO ao contrato · OU manter 4 valores documentando · OU outra arquitetura
8. **D-191 · Mockup Excel-alvo (provisória)** · vence aqui · vira padrão operacional ou é descartada com razão registrada
9. **3 ajustes UI pós-V2** · P-28 (Revisar e executar não mostra tudo) · P-32 (Nome conceitual sem propósito · provável remoção) · P-33 (ordem widgets E3 · unidade junto de tipo)
10. **Lições acumuladas Sessões 4-ter / 4-ter-bis / 5 / 6 / 7 / 8 / 8.1 / 8.2 / 8.3 / 8.4** · o que aprendemos sobre método

**Pauta provisória · pode entrar se houver tempo:**
11. **Lição metodológica P-37:** "Bateria de fechamento aritmético cross-linhas é teste obrigatório · NÃO opcional · para qualquer visão numérica" · D-174 ganha sub-camada nova (extends D-196 smoke visual)
12. **P-31 · UX nova de Salvar/Aplicar modelo** · decisão entre persistência local em pasta (α) ou SQLite (β) · pode virar sessão dedicada pós-Promoção de Fundação

**Resultado esperado da ALINHA:**
- 5-10 D-XXX novas (D-202 a D-211 aproximadamente)
- Modelo recalibrado para Família A
- Próxima sessão operacional definida (Sessão de Promoção de Fundação)
- Backlog dos 7 P- atualizado com encaminhamento concreto

**Razão:**
- D-193 declarou explicitamente o roadmap pós-V2 · D-200 honra esse roadmap
- Cabeça fresca de manhã é exigência metodológica · ALINHA é trabalho cognitivo denso · não cabe no fim de dia exausto
- Pauta consolidada antes da sessão (esta D-200) garante que ALINHA produz decisão · não só conversa exploratória
**Impacto:**
- Planilha aba 1 · "Próximo Passo" muda de "Sub-sessão 8.2" para "ALINHA-Lições-Família-A · 26/04 manhã"
- CONTEXT v3.4 §16 ganha referência a D-200 como Marco confirmado (não mais "agendada provisoriamente")
- D-200 abre como próxima conversa
**Referência canônica:** D-200 · D-193 (sequência declarada) · D-197 (débito de Fundação a resolver) · D-201 (V2 fechada · destrava ALINHA).

---

### D-199 — Sub-sessões 8.2 + 8.3 + 8.4 · 5 fixes aplicados em 4 rodadas · método 3 fases (D-185) confirmado em escala
**Data:** 2026-04-25 · noite · **Bloco:** ALINHA-Descoberta-Unidade · **Status:** Fechada · histórico operacional
**Contexto:** Após Camada 2 da Sessão 8.1 ter reprovado fechamento de V2 por 7 débitos (P-28 a P-34 · D-198), foram executadas 3 sub-sessões cirúrgicas adicionais para corrigir os 3 bloqueantes + 2 achados emergentes descobertos durante validação.

**Sub-sessão 8.2 (Caminho γ inicial):** 3 fixes propostos (P-29 + P-31 + P-30). Camada 2 da Usuária validou empiricamente:
- C-1 · P-29 (tela RESULTADO consome unidade) · ✅ FUNCIONOU
- C-2 · P-31 (Salvar/Aplicar modelo) · ❌ Solução errada · download/upload JSON em vez de UX nativa (nome digitado + lista) · DEFERIDO para D-200
- C-3 · P-30 (wrap_text Leitura qualitativa) · ❌ PIOROU · texto continuou cortando + linhas vizinhas infladas
- **P-35 NOVO · regressão emergente** · default automático Unidade↔tipo_campo quebrou após fix C-1

**Sub-sessão 8.3 (correção dirigida da 8.2):** 2 fixes (P-30 refeito + P-35 restaurado). Suite 731 verde · regressão zero. Camada 2 da Usuária validou:
- P-30 · ✅ texto cabe inteiro · vizinhas preservadas · cálculo de altura robusto (90 chars/linha · margem 1.4x · 16pt/linha · range 55-220pt)
- P-35 · ✅ default automático restaurado · diagnóstico Streamlit testing 6 cenários verdes · fix técnico: capturar tipo_anterior antes do st.radio · ao detectar mudança, resetar AS DUAS keys (`unidade` E `sel_unidade`) ao default
- **P-36 NOVO · achado emergente** · BarChart "Variações em destaque" ancorado em L42 col D com 6.3" altura · sobrepõe Leitura qualitativa (L53-54) e Qualidade estrutural (L56-57)

**Sub-sessão 8.4 (correção dirigida do P-36):** 1 fix (P-36 reposicionar gráfico). Caminho α (gráfico vai depois de Qualidade estrutural · vira último bloco do Resumo Executivo · ganha cabeçalho próprio "Variações em destaque · gráfico"). Camada 2 da Usuária validou:
- P-36 · ✅ Excel V2_S84 com ordem nova · gráfico isolado no fim · sem sobreposição
- Validação adicional em TEMPO_HORAS (4ª unidade testada · não estava nas amostras oficiais) descobriu **P-37 NOVO · INSIGHT CRÍTICO de produto** · não-bloqueante (motor matematicamente correto · arredondamento de apresentação esconde variações materiais)

**Decisão:** D-199 formaliza as 3 sub-sessões como aplicação canônica em escala do padrão D-185 (Fase a investigação · Fase b implementação escopo fechado · Fase c validação humana). 4 rodadas iterativas (8.1 · 8.2 · 8.3 · 8.4) · cada uma com escopo cirúrgico fechado · 5 P- bloqueantes resolvidos no total + 3 P- emergentes descobertos via Camada 2 humana.

**Razão:**
- Sub-sessões cirúrgicas (não combinadas) protegem método de fragmentação · cada rodada tem escopo fechado · sem ajuste incremental durante execução
- Camada 2 humana é instrumento essencial · descobriu 3 dos 7 achados resolvidos hoje (P-29 originalmente · P-35 emergente da S82 · P-36 emergente da S83)
- Iteração 8.1 → 8.2 → 8.3 → 8.4 é exemplo positivo de método · cada sub-sessão fechou seu escopo sem regressão · custo total ~6h reais distribuídas em 4 rodadas
- Achados emergentes (P-35 · P-36 · P-37) sempre via Camada 2 humana · NUNCA via suite mecânica (731 testes verdes não pegaram nenhum dos 3) · reforça D-196 e motiva ampliação dela em D-200

**Impacto:**
- Suite final · 731 testes verdes · regressão zero ao longo de 4 sub-sessões
- 3 amostras oficiais finais · V2_S84_{MONETARIO_BRL,PERCENTUAL,QUANTIDADE}.xlsx (S82 · S83 obsoletas)
- 5 fixes implementados em src/visoes/exportacao_v2.py (Saúde 3/4 cols · Onde se concentra Δ médio · template Leitura qualitativa · contrair_de · cálculo robusto wrap_text · reposicionamento gráfico)
- 1 fix em src/app_v2.py (cards consomem unidade + reset duplo de keys ao trocar tipo_campo)
- Padrão de sub-sessões cirúrgicas iterativas validado em escala · candidato a virar template em CONTEXT §15 (D-200 pode formalizar)

**Referência canônica:** D-199 · D-185 (padrão aplicado) · D-201 (V2 fechada como resultado) · CHECKLIST_MECANICO_S82/S83/S84.md.

### D-198 — V2 retroativa NÃO fecha em 25/04/2026 · 7 débitos pós-Camada 2 movem decisão de Marco para sub-sessão 8.2 e ALINHA-Lições-Família-A
Data: 2026-04-25 · Bloco: ALINHA-Descoberta-Unidade · Status: Fechada · vigora a partir da Sessão 8.1
Contexto: Sessão 8 entregou Camada 1 verde (725 testes) com 5 evoluções de produto V2 (E1 unidade · E2 Saúde da comparação · E3a Concentração · E3b Onde se concentra · E3c Leitura qualitativa). Camada 2 (Usuária) reprovou o produto com unidade=PERCENTUAL por 6 achados visuais críticos. Sessão 8.1 corrigiu os 6 (suite 731 verde · 3 amostras V2_S81 validadas pelo Arquiteto e pela Usuária). Camada 2 da Sessão 8.1 revelou 7 débitos remanescentes (P-28 a P-34) que não foram cobertos pelo escopo das Sessões 8 e 8.1: tela RESULTADO do app não consome unidade (P-29 · ALTA bloqueante) · botões "Salvar como modelo" e "Aplicar modelo" não funcionam (P-31 · ALTA bloqueante) · Leitura qualitativa não quebra texto no Excel (P-30 · MÉDIA) · tela "Revisar e executar" omite Comparar de/com e Unidade (P-28 · MÉDIA) · "Nome conceitual do campo" inerte (P-32 · MÉDIA) · ordem dos widgets E3 desorganizada (P-33 · BAIXA) · motor não infere unidade automaticamente (P-34 · BAIXA · evolução).
Decisão: V2 retroativa NÃO fecha em 25/04/2026. Status mantém ✅✅✅✅⚠️⚠️ (Excel funcional · UI ainda em débito). Usuária declarou explicitamente: "Não está fechada · tem todos aqueles pontos que eu te passei lá em cima · qual é o prudente? A tela no percentual ainda está aparecendo em reais · isso é grave. Tem aqueles campos que não estão funcionais... A célula da explicação não está funcionando."
Encaminhamento dos 7 débitos:

P-29 + P-31 + P-30 · Sub-sessão 8.2 dirigida (Caminho γ recomendado pela Usuária · escopo cirúrgico) · Claude Code corrige · Camada 2 valida · V2 fecha em sessão única amanhã ou ainda hoje à noite
P-28 + P-32 + P-33 · ALINHA-Lições-Família-A (D-200 nova · agendada) · ajustes de UI da tela do app
P-34 · Backlog evolução pós-Família-A · sessão dedicada de inferência inteligente de unidade
Razão:
Critério mecânico (suite 731 verde · Excel coerente) é insuficiente para declarar V2 fechada · critério real é "produto funcional ponta a ponta" (Usuária pode demonstrar V2 sem fricção)
Botão visível que não funciona é pior que feature ausente (P-31)
Tela mostrando R$ em PERCENTUAL após Excel correto cria dissonância de produto · Usuária não pode demonstrar V2 percentual sem explicar bug (P-29)
Usuária aplicou critério correto · Arquiteto havia inicialmente puxado fechamento prematuro · revisão alinhada
Impacto:
Planilha (aba 2) · V2 segue ⚠️⚠️ · não vai pra ✅✅✅✅✅✅ até sub-sessão 8.2 fechar
Próximo passo declarado: sub-sessão 8.2 (Caminho γ) → fecha V2 → ALINHA-Lições-Família-A → recalibração modelo → V1 sob método novo
D-174 gate duplo confirmado novamente · Camada 2 humana descobriu o que Camada 1 mecânica não viu · 3ª aplicação do princípio (após cache D-186 e achado-mãe unidade D-190)
Referência canônica: D-198 · próxima conversa abre como sub-sessão 8.2.


### D-197 — Débito de Fundação · trabalho da Sessão 8 NÃO foi feito como F-APRESENT genérica · helpers de unidade vivem em formatos.py mas pontos de consumo são bespoke em V2
Data: 2026-04-25 · Bloco: ALINHA-Descoberta-Unidade · Status: Fechada · DÉBITO CRÍTICO PRÉ-V1
Contexto: Sessão 8 implementou campo unidade em ComparacaoV2 (V2-específico · não em camada de Fundação) · adicionou helpers em src/apresentacao/formatos.py (bom · F-APRESENT) · MAS os pontos de consumo dos helpers são bespoke em src/visoes/exportacao_v2.py e src/app_v2.py (V2-específico · não capability genérica de F-APRESENT). Consequência estrutural: V1 e V11 (próximas visões da Família A) NÃO consomem unidade automaticamente · vão herdar o bug original (formatação hardcoded R$) por default. Trabalho de Fundação foi parcial · quando deveria ter sido total. Usuária identificou explicitamente: "lá atrás você falou pra mim que algumas coisas que o Claude estava corrigindo, ele não estava ajustando a Fundação, aos nossos mecanismos de contratos transversais... isso é muito importante, espero que esteja mapeado · a gente vai ter que tratar isso tudo antes de ir pra V1."
Decisão: formalizar como DÉBITO DE FUNDAÇÃO bloqueante pré-V1. Antes de iniciar V1 ou V11, sessão dedicada de promoção de unidade para Fundação genérica deve acontecer. Escopo provisório dessa sessão (será refinado na ALINHA-Lições-Família-A · D-200):

Avaliar se unidade deve viver em contrato genérico de Fundação (ex: campo em ColumnMeta ou em uma EspecificacaoCampo nova) · não só em ComparacaoV2
Promover _montar_colunas_matriz (que hoje vive em exportacao_v2.py) · ou pelo menos sua lógica de despacho por unidade · para capability genérica de F-APRESENT (capability 4/5 · D-166)
Promover _construir_leitura_qualitativa_v2 para template parametrizado consumível por V1/V11/restantes · ou pelo menos extrair o gerador de microcopy
Garantir que tela RESULTADO do app (e demais telas equivalentes em V1/V11) consome os helpers automaticamente · sem hardcode de unidade
Adicionar smoke tests visuais cross-visão (não só V2)
Razão:


Sessão 7 fez ALINHA leve · ficou explícito que cascata em V1/V11 ficaria pra retrospectiva. Sessão 8 e 8.1 implementaram patch tático em V2 · não promoção arquitetural · risco de Fundação foi assumido conscientemente
Risco se materializa agora: ao começar V1 ou V11, mesmos bugs de unidade vão aparecer · validação Camada 2 vai falhar igual · ciclo de correção tática se repete · método quebra
D-197 fica explícita para ALINHA-Lições-Família-A (D-200) consumir como ponto principal de pauta
Impacto:
ALINHA-Lições-Família-A (D-200) ganha sub-bloco específico "Promoção de unidade para Fundação genérica" como pauta obrigatória
D-197 protege V1 de iniciar prematuramente · V1 só inicia após sessão de promoção de Fundação ter ocorrido
Nota explícita em CONTEXT v3.4 §16 (nova) · "débitos de Fundação a resolver pré-V1"
Referência canônica: CONTEXT v3.4 §16 · ALINHA-Lições-Família-A pauta · D-197.


### D-196 — 6 smoke tests visuais de Excel adicionados em src/testes/test_v2_s8_smoke_visual.py · proteção contra regressão de unidade
Data: 2026-04-25 · Bloco: Sessão 8.1 · Status: Fechada
Contexto: Sessão 8 entregou 725 testes verdes mas Camada 2 (Usuária) descobriu que o Excel produzido com unidade=PERCENTUAL exibia "R$" em todos os lugares · valores absurdos (Média = 69.767%) · cabeçalho "p.p" com formato "%". Suite mecânica não pegou porque testes validavam estrutura/contrato · não valor renderizado em célula. Gap de método: D-174 Camada 1 mecânica é insuficiente quando o sintoma é "número absurdo na apresentação".
Decisão: criar arquivo novo src/testes/test_v2_s8_smoke_visual.py com 6 testes de smoke que abrem amostra in-memory · leem valor de célula-chave · aplicam number_format manualmente · assertam range realista. Cobertura:

PERCENTUAL · Card Média parsável como % · range 5-100%
PERCENTUAL · célula Diferença em Matriz · formato "p.p" · valor pré-multiplicado por 100 (range -100 a +100)
MONETARIO_BRL · Card Total parsável como R$ · range R$ 100-1.000.000
QUANTIDADE · Card Total · inteiro >= 0
PERCENTUAL · Saúde da comparação SEM coluna Δ total
MONETARIO_BRL · Saúde da comparação MANTÉM coluna Δ total (regressão zero)
Razão:


Smoke visual é a primeira linha de defesa contra "Camada 1 verde · Camada 2 reprovada" identificado nesta sessão
6 testes cobrem cenários críticos sem ser exaustivo · trade-off entre cobertura e custo de manutenção
Padrão pode ser estendido para V1/V11 quando ALINHA-Lições-Família-A formalizar promoção de Fundação (D-197)
Impacto:
Suite total · 725 → 731 (725 testes pré + 6 smoke novos)
Test pattern reusável: pytest src/testes/test_v2_s8_smoke_visual.py valida 6 cenários canônicos em ~3s
Lição estende D-174 · gate duplo Camada 1 ganha sub-camada "smoke visual mínimo"
Referência canônica: src/testes/test_v2_s8_smoke_visual.py · D-196.


### D-195 — Bifurcação D-1 da Sessão 8 (formato p.p) · resolvida na Sessão 8.1 com multiplicação em F-APRESENT + formato literal
Data: 2026-04-25 · Bloco: Sessão 8.1 · Status: Fechada · resolve débito da Sessão 8
Contexto: Sessão 8 entregou Camada 1 com formato '+0.00%' para coluna "Variação absoluta (p.p)" · cabeçalho declarava "p.p" mas valor era renderizado como "%". Bifurcação D-1 foi declarada explicitamente no CHECKLIST_MECANICO_S8.md · Claude Code argumentou que aplicar formato literal "p.p" mostraria "0,05 p.p" (sem multiplicar por 100) · violando expectativa de leitura. Solução pragmática inicial foi usar +0.00% com cabeçalho "p.p" · mas isso foi reprovado pela Usuária na pré-validação do Arquiteto: "+5,00% em coluna 'p.p' é dissonante · mistura unidades de leitura · não passa".
Decisão: F-APRESENT multiplica por 100 ao escrever célula quando unidade=PERCENTUAL · formato Excel é '+0.00" p.p";[Red]-0.00" p.p";-' literal · sem multiplicação automática nativa do Excel.
Implementação:

Helper novo valor_diferenca_para_celula(valor_raw, unidade) em src/apresentacao/formatos.py · multiplica por 100 quando unidade=PERCENTUAL · preserva valor para outras unidades
_NF_DIFERENCA["PERCENTUAL"] atualizado para formato literal "p.p"
_aplicar_formatos_tabela em exportacao_v2.py rescala valores pré-existentes para tag=diferenca + unidade=PERCENTUAL
Cards · tabela "Variações em destaque" · BarChart x_axis · todos consomem helper
Razão:
Cabeçalho "Variação absoluta (p.p)" e valor "+5,00 p.p" formam contrato visual coerente com cliente
Cliente lendo "+5,00%" e "+5,00 p.p" tira interpretações analíticas diferentes (multiplicativa vs aditiva)
Multiplicação em F-APRESENT preserva motor intocado (motor armazena fração 0.05) · responsabilidade fica em camada de apresentação · alinhado com C.D8 (D-190)
Impacto:
Excel V2_S81_PERCENTUAL.xlsx · coluna p.p mostra "-1,84 p.p", "+5,00 p.p", etc · validado por Arquiteto e Usuária
src/apresentacao/formatos.py · novo helper público
Bifurcação D-1 da Sessão 8 fechada
Referência canônica: src/apresentacao/formatos.py · D-195.


### D-194 — Sessão 8 + Sessão 8.1 · 5 evoluções de produto V2 implementadas (E1 unidade · E2 Saúde · E3a Concentração · E3b Onde se concentra · E3c Leitura qualitativa)
Data: 2026-04-25 · Bloco: ALINHA-Descoberta-Unidade · Status: Fechada · pós-Sessão 8.1
Contexto: Sessão 7 (ALINHA-Descoberta-Unidade) consolidou 5 evoluções de produto V2 a serem executadas em rodada única (D-185 fase b). Sessão 8 implementou as 5 + 56 testes novos (725 total verde). Sessão 8.1 corrigiu 7 achados visuais descobertos na Camada 2 (suite 731 verde + 3 amostras V2_S81 validadas).
Decisão: 5 evoluções formalizadas como entregue em produto V2 retroativo:

E1 · Campo unidade em ComparacaoV2 + Diferença/Variação adaptativos · 8 valores canônicos (MONETARIO_BRL · PERCENTUAL · QUANTIDADE · TEMPO_DIAS · TEMPO_HORAS · MULTIPLICADOR · RAZAO · ADIMENSIONAL) · default MONETARIO_BRL · widget novo na Etapa 3 do app · F-APRESENT consulta unidade · rótulos canônicos por unidade (Diferença vs Variação absoluta p.p · Variação % vs Variação relativa)
E2 · "Saúde da comparação" substitui "Como os casos se distribuem" para tipo_campo numérico · ESTADO_SITUACAO mantém comportamento estrutural · NEUTRA exibe AUMENTOU/REDUZIU/ESTAVEL distintos · PERCENTUAL omite coluna Δ total (somar p.p viola C.D3) · rodapé "Não comparáveis" decompõe ausentes/nulos
E3a · Bloco "Concentração" · top 5 e top 10 explicam X% do impacto · microcopy adaptativo (alta ≥80% · moderada ≥50% · distribuída) · oculto se < 5 PRESENTE_AMBOS · oculto para ESTADO_SITUACAO
E3b · "Onde se concentra · Top 3 por agrupador escolhido" · widget novo na Etapa 4 (selectbox agrupador_destacado · default = primeiro escolhido · Usuária pode trocar) · novo campo agrupador_destacado em ComparacaoV2 · top 3 ordenado por |Δ| absoluto · coluna Δ formatada por unidade (Δ médio em p.p para PERCENTUAL · Δ soma para outras)
E3c · Leitura qualitativa enriquecida · template parametrizado · 4 sentenças condicionais consumindo dados de E2/E3a/E3b · helper _contrair_de resolve "de o" → "do" · "de a" → "da" · template específico para PERCENTUAL com Média + Variação relativa
Razão:
ALINHA-Descoberta-Unidade Sessão 7 desenhou escopo completo · execução Sessão 8 + Sessão 8.1 entregou
5 evoluções alinhadas com decisão produto da Usuária ("Resumo Executivo precisa ser scannable em 30 segundos · responder Q1 melhorou/piorou · Q2 concentração · Q3 padrão por dimensão")
Rótulos didáticos confirmados ("Variação absoluta (p.p)" · "Variação relativa (%)") · default Caminho γ híbrido (ALINHA leve + Claude Code curta) cumprido
Impacto:
Excel V2 retroativo · Resumo Executivo reformulado (Saúde · Concentração · Onde se concentra · Leitura qualitativa enriquecida) · cabe nas 4 abas existentes
Contrato ComparacaoV2 ganha 2 campos novos (unidade · agrupador_destacado)
V2Result ganha 3 campos novos (delta_por_classificacao_semantica · concentracao · onde_se_concentra)
src/apresentacao/formatos.py ganha 7 helpers de despacho por unidade
src/app_v2.py ganha 2 widgets novos (sel_unidade · sel_agrupador_destacado)
src/visoes/exportacao_v2.py ganha 5 funções novas + adaptação de cards/tabela/gráfico
src/testes/test_v2_s8.py · 56 testes novos
src/testes/test_v2_s8_smoke_visual.py · 6 smoke tests (D-196)
3 amostras oficiais: amostras/V2_S81_{MONETARIO_BRL,PERCENTUAL,QUANTIDADE}.xlsx
Referência canônica: D-194 · CHECKLIST_MECANICO_S8.md · CHECKLIST_MECANICO_S81.md.


### D-193 — Sequência operacional pós-V2 declarada pela Usuária · ALINHA-Lições-Família-A → recalibração modelo → V1 → V11 → famílias seguintes
Data: 2026-04-25 · Bloco: ALINHA-Descoberta-Unidade · Status: Fechada
Contexto: Usuária declarou explicitamente o roadmap pós-V2 ao consolidar a Sessão 7: "Depois que a gente fechar a V2, a minha ideia é amanhã com a cabeça fresca pegar todas as lições aprendidas e recalibrar o modelo, tentar na V1, tentar na V11, fechando o modelo · 'ah o modelo agora está fechado' · aí a gente segue pras demais famílias."
Decisão: sequência canônica adotada como roadmap operacional declarado:

V2 fecha (sub-sessão 8.2 · D-198) · ✅✅✅✅✅✅ na planilha
ALINHA-Lições-Família-A (D-200) · sessão estrutural · 90-120 min · cabeça fresca · consolida 7 débitos pós-V2 + débito de Fundação D-197 + lição D-191 (mockup Excel-alvo) + lição P-34 (inferência de unidade) · produz modelo recalibrado para Família A · agendada para "manhã de amanhã" pela Usuária
Sessão de Promoção de Fundação (consequência de D-197) · pode ocorrer dentro da ALINHA-Lições-Família-A ou em sessão imediatamente seguinte · promove unidade para contrato genérico · cria capability F-APRESENT que V1/V11 consomem por default
V1 sob método novo · primeira aplicação do modelo recalibrado · Conciliação de Bases · valida que padrões Família A funcionam em outra visão da família
V11 sob método novo · Conciliação por Aderência · 2ª aplicação · modelo Família A fechado se V1 + V11 funcionarem sem retrabalho equivalente ao da V2
Modelo Família A fechado · Marco · viabiliza começar Família B (visões estruturais não-temporais · V3/V4)
Famílias seguintes · B (composição) → C (cronologia) → D (consolidação) → E (alinhamento) · cada uma com sua ALINHA-Lições no fechamento
Razão:


Roadmap explícito da Usuária · não inferido · não negociado · vem da fala dela na Sessão 7
Disciplina de "fechar modelo na Família A antes de avançar" protege famílias seguintes do retrabalho que aconteceu na V2
D-197 (débito de Fundação) é peça-chave dessa sequência · sem ela V1 e V11 quebram da mesma forma que V2
Padrão "ALINHA de fechamento → modelo recalibrado → próximas visões aplicam" estabelece template para futuras transições de família
Impacto:
Planilha aba 1 ganha sequência de Marcos canônica até fechamento da Família A
CONTEXT v3.4 §16 (nova) declara o roadmap como compromisso operacional
D-200 (ALINHA-Lições-Família-A) abre como Marco antecipado quando V2 fechar · não aguarda V1/V11
Próximas conversas: sub-sessão 8.2 → ALINHA-Lições-Família-A → Promoção de Fundação → V1
Referência canônica: CONTEXT §16 · D-193 · D-197 · D-200.


### D-192 — Resumo Executivo de V2 reformulado · 3 blocos novos (Saúde · Concentração · Onde se concentra) · "Como os casos se distribuem" mantido só para ESTADO_SITUACAO
Data: 2026-04-25 · Bloco: ALINHA-Descoberta-Unidade · Status: Fechada · pós-Sessão 8
Contexto: Usuária declarou na Sessão 7 que o bloco "Como os casos se distribuem" hoje exibido no Resumo Executivo da V2 (categorias estruturais PRESENTE_AMBOS/AUSENTE_ORIGEM/etc) faz sentido em V1 (conciliação de bases · "esse registro existe nos dois lados? a chave bate?") mas é ruído em V2 (comparação de 2 estados · onde tudo deveria estar nos dois lados). Cliente executivo precisa ver distribuição semântica (Melhorou · Piorou · Estável) · não estrutural.
Decisão: 4 mudanças no Resumo Executivo da V2 para tipo_campo numérico (NUMERICO_ADITIVO/RELATIVO/NAO_ADITIVO):

Substituir "Como os casos se distribuem" por "Saúde da comparação" (3-4 colunas conforme unidade · Categoria · Casos · Participação · [Δ total para não-PERCENTUAL]) · footer decompõe "Não comparáveis"
Adicionar bloco "Concentração" (microcopy adaptativo sobre concentração das variações em poucos casos) · oculto se <5 PRESENTE_AMBOS
Adicionar bloco "Onde se concentra · Top 3 por agrupador escolhido" (Top 3 categorias por |Δ| absoluto + rodapé com outras) · widget novo na Etapa 4 (agrupador_destacado · default = primeiro escolhido)
Enriquecer "Leitura qualitativa" · template parametrizado consumindo dados dos 3 blocos acima · sentenças condicionais
Para tipo_campo=ESTADO_SITUACAO · "Como os casos se distribuem" original é preservado (ESTADO_SITUACAO não tem semântica Melhorou/Piorou · estrutural ainda é o coração da análise) · função renomeada para _renderizar_secao_distribuicao_estrutural.
Razão:


"Como os casos se distribuem" aparece em ~95-100% como "Presente nos dois lados" para V2 saudável · vira ruído visual
Cliente executivo precisa ler em 30s · 3 blocos novos respondem perguntas "melhorou/piorou? · concentração material? · padrão por dimensão?" que importam para decisão executiva em V2
ESTADO_SITUACAO é caso onde bloco original ainda faz sentido · D-192 não revoga função · só restringe escopo de uso
Impacto:
Excel V2 retroativo · Resumo Executivo reformulado · validado em V2_S81_{MONETARIO_BRL,PERCENTUAL,QUANTIDADE}.xlsx
src/visoes/exportacao_v2.py · 3 funções novas (_renderizar_secao_saude_comparacao · _renderizar_secao_concentracao · _renderizar_secao_onde_se_concentra) · função _renderizar_secao_distribuicao_estrutural preservada para ESTADO_SITUACAO
src/visoes/visao_v2.py · 3 cálculos novos em V2Result (delta_por_classificacao_semantica · concentracao · onde_se_concentra)
src/app_v2.py · widget novo sel_agrupador_destacado na Etapa 4
ComparacaoV2 ganha campo agrupador_destacado: Optional[str]
Referência canônica: D-192 · CHECKLIST_MECANICO_S8.md.


### D-191 — Mockup Excel-alvo precede execução de A-VN · proposta provisória · vence em ALINHA-Lições-Família-A
Data: 2026-04-25 · Bloco: ALINHA-Descoberta-Unidade · Status: Provisória · vence em D-200 (ALINHA-Lições-Família-A)
Contexto: Usuária declarou explicitamente durante a Sessão 7: "a gente sabe que o produto final é o Excel · a gente precisa antes de fazer a validação ali na linha do código · a gente precisa de uma visão do Excel gerado pra aquela visão · pra não perder tanto tempo." Proposta de método: antes de Claude Code escrever código de A-VN, mockup do Excel da visão (manual ou semi-automático) serve de critério visual prévio · Claude Code implementa contra Excel-alvo claro · não contra interpretação livre da Spec.
Decisão: D-191 anotada como proposta provisória de evolução de método. NÃO entra na ALINHA leve da Sessão 7 (escopo focado em fechar V2 · não em método). Vence na ALINHA-Lições-Família-A (D-200) · onde será discutida com lições acumuladas das Sessões 4-ter / 4-ter-bis / 5 / 8 / 8.1 / 8.2.
Razão:

Proposta legítima · alinhada com produto Excel-first do TabloFlow
Mas é decisão de método transversal · afeta todas as visões · merece ALINHA dedicada · não cabe pendurar em sessão operacional V2
ALINHA-Lições-Família-A é o lugar natural para discutir · porque vai consolidar lições de toda a Família A antes de iniciar V1/V11 sob método novo
Impacto:
D-191 fica como pauta obrigatória de D-200
Se aprovada na D-200, vira D-XXX nova com instruções operacionais (formato do mockup · papel do Arquiteto vs Usuária na produção dele · gate de aprovação antes de Claude Code abrir)
Se descartada, D-191 fica revogada com razão registrada
Referência canônica: D-191 (provisória) · D-200 (vence aqui).


### D-190 — C.D8 · Unidade declarada universal · 8º derivado da Camada C
Data: 2026-04-25 · Bloco: ALINHA-Descoberta-Unidade · Status: Fechada · princípio constitucional
Contexto: Investigação meta-estrutural pós-Sessão 5 (Sessão 6 · Fase a) descobriu achado-mãe da Família A: o conceito de "unidade do campo" (R$ vs % vs qtd vs dias vs etc) NÃO existia no contrato ComparacaoV2 nem em qualquer contrato genérico. F-APRESENT formatava todas colunas numéricas como monetário (R$) hardcoded · ignorando tipo_campo · resultando em "R$ 0,21" em campo que era margem percentual (P-25). Bug invisível até a Camada 2 da Sessão 5 expor com base de teste percentual. Cronologia da compressão: DCV-V1 declarava 7 categorias de tipo de campo (Valor Monetário · Quantidade · Volume · Percentual · Prazo · Índice · Estado/Situação) · vocabulario_bilingue.md Bloco 4 declarou 6 (sem CATEGORICO/BOOLEANO) · contrato implementado tem 4 (NUMERICO_ADITIVO · NUMERICO_RELATIVO · NUMERICO_NAO_ADITIVO · ESTADO_SITUACAO) · "unidade" como campo separado simplesmente não existia.
Decisão: C.D8 · Unidade declarada universal · 8º derivado da Camada C (Constituição). Princípio: "Toda comparação numérica em qualquer visão TabloFlow declara explicitamente a unidade do campo analisado · F-APRESENT consulta unidade para escolher formato e rótulos · zero hardcode de unidade em camada de apresentação · zero inferência implícita de unidade por tipo_campo."
Implementação inicial em V2 (Sessão 8 + 8.1):

Campo unidade: Literal[...] em ComparacaoV2 com 8 valores canônicos · default MONETARIO_BRL (preserva comportamento)
Helpers em src/apresentacao/formatos.py (number_format_valor · number_format_diferenca · number_format_variacao · rotulo_diferenca · rotulo_variacao · label_total_card · valor_total_card · valor_diferenca_para_celula · formatar_valor_por_unidade)
Widget novo na Etapa 3 do app (default inferido de tipo_campo · Usuária pode trocar)
Débito de Fundação: implementação atual é V2-específica · não foi promovida para contrato genérico de Fundação (D-197) · ALINHA-Lições-Família-A (D-200) deve resolver isso antes de V1/V11.
Razão:
Princípio constitucional · Camada C · vinculante para todas as 11 visões · zero exceção
Resolve raiz dos achados P-25 (R$ em percentual) · P-26 (Soma e Média idênticos em percentual) · P-27 (Nome conceitual sem propósito)
Compressão silenciosa de vocabulário (D-189) é o sintoma · D-190 é o tratamento da raiz
Alinhado com C.D6 DDU (Default Declarado Universal) · default por tipo_campo + Usuária pode trocar
Impacto:
CONTEXT v3.4 §3 ganha sub-item C.D8
vocabulario_bilingue v4 ganha Bloco 10 (Unidades canônicas)
spec_fundacao.md ganha seção sobre unidade do campo (não só de threshold) · projetada para incorporar na sessão de Promoção de Fundação
D-190 vincula próxima evolução: V1 e V11 abrem com unidade nativa · família B/C/D/E também
Referência canônica: CONTEXT §3 (C.D8) · vocabulario_bilingue Bloco 10 · D-190 · D-197.


### D-189 — Compressão silenciosa de vocabulário identificada · DCV-V1 declarava 7 categorias de tipo de campo · contrato implementou 4 · sem registro de decisão
Data: 2026-04-25 · Bloco: Sessão 6 · investigação meta-estrutural · Status: Fechada · histórica
Contexto: Investigação dirigida da Sessão 6 (Fase a · D-185) sobre achado-mãe da Família A descobriu que houve compressão silenciosa de vocabulário ao longo do tempo. DCV-V1 (linha 122) declarava 7 tipos lógicos de campo (Valor Monetário · Quantidade · Volume · Percentual · Prazo · Índice · Estado/Situação). vocabulario_bilingue.md Bloco 4 consolidou 6 categorias (NUMERICO_ADITIVO · NUMERICO_RELATIVO · NUMERICO_NAO_ADITIVO · CATEGORICO · BOOLEANO · ESTADO_SITUACAO). Contrato ComparacaoV2.tipo_campo aceita apenas 4 (NUMERICO_ADITIVO · NUMERICO_RELATIVO · NUMERICO_NAO_ADITIVO · ESTADO_SITUACAO) · CATEGORICO e BOOLEANO sumiram do contrato sem registro de decisão. UI mistura ainda mais (rótulo "Categoria ou rótulo (status, classificação)" no app é o user-facing canônico de CATEGORICO mas o valor técnico que carrega é ESTADO_SITUACAO).
Decisão: D-189 formaliza a descoberta como achado histórico. NÃO revoga o estado atual (4 valores) · porque é o que está implementado e funciona para V1/V2/V11 da Família A. Vincula resolução completa à ALINHA-Lições-Família-A (D-200) que pode:

Restaurar CATEGORICO e BOOLEANO ao contrato (se outras famílias precisarem)
Manter 4 valores e documentar formalmente a redução (com razão registrada)
Outra arquitetura (ex: 2 contratos · um para Família A · outro para outras famílias)
Razão:
Compressão sem registro é débito de método · não é débito de implementação
Trabalho da Família A não exigiu CATEGORICO/BOOLEANO · então a compressão funcionou de fato
Mas Família B (composição · onde categorias podem ser eixo) ou Família E (alinhamento · onde booleanos podem ser ponto) provavelmente vão precisar
Decisão consciente em D-200 evita que compressão silenciosa se repita em outros vocabulários
Impacto:
Achado histórico registrado · zero mudança imediata em código
ALINHA-Lições-Família-A (D-200) ganha pauta obrigatória "revisão de vocabulario_bilingue Bloco 4 vs contrato implementado"
Lição metodológica: toda compressão de vocabulário canônico exige D-XXX explícita · zero compressão silenciosa daqui pra frente
Referência canônica: D-189 · D-200 (vence aqui).


### D-188 — Convenção numérica do BAD preservada · sinal de Diferença e Variação segue Comparado − Origem · não inverte por semantica_campo · arquiva P-24
Data: 2026-04-25 · Bloco: Sessão 6 · investigação meta-estrutural · Status: Fechada · arquivada
Contexto: Sessão 5 Camada 2 da Usuária (24/04 noite) levantou dissonância visual: linha onde Diferença é -2.307 (vermelho) e Leitura qualitativa é "Melhorou" (verde) na mesma linha · porque convenção atual do BAD é Diferença = Comparado − Origem (sinal matemático cru) · enquanto classificacao_semantica respeita semantica_campo (Melhorou em MENOR_MELHOR quando Realizado < Orçado). Usuária inicialmente questionou: "os sinais de variação e de diferença, eles também precisam seguir a análise semântica." Proposta provisória registrada como P-24.
Decisão: convenção atual preservada por design. P-24 arquivado · não vira pendência. Justificativa:

Diferença é fato matemático cru (preservar C.D3 · BAD como representação fiel do dado)
Inverter sinal por semantica_campo trocaria significado da coluna · "Diferença" deixaria de ser delta matemático e viraria "intensidade da Melhora/Piora com sinal" · viola contrato analítico
Cascata negativa em V1/V11/visões numéricas (todas teriam contratos inconsistentes)
Solução real para a dissonância visual virá em F-APRESENT-cleanup (D-180) ou ALINHA-Lições · pode ser cor da célula consultar classificacao_semantica em vez de sinal numérico (mantém número cru · só pinta diferente) · OU coluna nova "Impacto" derivada · OU outra solução de produto
Razão:
Decisão da Usuária após discussão estruturada · Sessão 6 · "de fato é como os campos ficam ordenados lá com o comparado que vai influenciar · eu acho que a gente mudar esses campos não é legal · eu acho que vale só a questão semântica mesmo"
D-188 fica como rastro explícito para defender a convenção quando questionada de novo no futuro
Impacto:
Zero mudança em código
P-24 arquivado · não vira pendência ativa
D-188 protege C.D3 (BAD como fato cru) de futura tentativa de inversão de sinal
Referência canônica: D-188 · P-24 arquivado.


### D-187 — Bug NEUTRA expandida · classificacao_semantica deixa de colapsar AUMENTOU/REDUZIU/ESTAVEL em "NEUTRO" único · 7 valores canônicos
Data: 2026-04-25 · Bloco: Sessão 5 · resolvido na Sessão 5 · formalizada agora
Contexto: Investigação dirigida da Sessão 5 (Fase a · D-185) sobre P-23 (suposta semântica T-SEMA invertida) refutou hipótese original (D-182) e descobriu bug real distinto. _SEMA_LABEL_TO_CLASS em src/visoes/visao_v2.py:359-365 colapsava 3 estruturais ("Aumentou", "Reduziu", "Estável") em código semântico único "NEUTRO". Para semantica_campo=NEUTRO, contrato T-SEMA (spec_fundacao.md §D.3) exige 4 valores estruturais distintos:

NEUTRA × AUMENTOU → "Aumentou"
NEUTRA × REDUZIU → "Reduziu"
NEUTRA × ESTAVEL → "Estável"
NEUTRA × NAO_APLICAVEL → "Não aplicável"
Mas implementação colapsava todos em "Estável" via fallback · perdendo distinção que o contrato exigia.
Decisão: expandir Literal de classificacao_semantica em V2Result.base_analitica de 4 para 7 valores: POSITIVO · NEGATIVO · NEUTRO · NAO_APLICAVEL · AUMENTOU · REDUZIU · ESTAVEL. _SEMA_LABEL_TO_CLASS reescrito sem colapso. _FALLBACK_CLASSIF_SEMANTICA em exportacao_v2.py ganha 3 traduções novas + mantém "NEUTRO" como legado.
Razão:
Contrato T-SEMA spec_fundacao.md §D.3 é a referência canônica · implementação deve respeitar
Compromete legibilidade analítica de campos sem viés (semantica_campo=NEUTRO) que são cliente legítimo (ex: análise de variação populacional · contagem) onde "subiu" e "desceu" são distinções importantes não-axiológicas
Cobertura T-SEMA estendida para 12/12 (matriz cartesiana · D-183 C.D7) na mesma sessão · garante que regressão não ressurge
Impacto:
src/visoes/visao_v2.py:242 · Literal de classificacao_semantica expandido (7 valores)
src/visoes/visao_v2.py:359-365 · _SEMA_LABEL_TO_CLASS reescrito
src/visoes/exportacao_v2.py:85-90 · _FALLBACK_CLASSIF_SEMANTICA estendido
src/visoes/visao_v2.py:1199 · distribuicao_classificacoes_semanticas expandida para 7 chaves
src/apresentacao/badges.py · AUMENTOU/REDUZIU adicionados como categoria "neutro" (descoberto colateral por Claude Code · não estava no escopo original)
Suite Sessão 5 · 660 → 666 (+6 testes T-SEMA × NEUTRO)
Camada 2 da Sessão 5 (Usuária) validou empiricamente · valores "Aumentou", "Reduziu", "Estável", "Não aplicável" distintos no Excel
Referência canônica: spec_fundacao.md §D.3 · src/visoes/visao_v2.py · D-187 (substitui parcialmente D-182).


### D-186 — Cache do app · gate de stale por hash de config crítica em st.session_state · invalida resultado quando Usuária muda campo na Etapa 3 sem reexecutar
Data: 2026-04-25 · Bloco: Sessão 5 · resolvido na Sessão 5 · formalizada agora
Contexto: Investigação dirigida da Sessão 5 (Fase a · D-185) sobre P-23 reformulou hipótese original (D-182) após Camada 2 empírica da Usuária. Sintoma reportado: trocar rádio "subir é bom/ruim" na Etapa 3 e voltar à tela RESULTADO mostrava classificacao_semantica antiga (não recalculada com config nova). Investigação descobriu: motor V2 estava correto · o que falhava era o app · app_v2.py não invalidava resultado quando campo da Etapa 3 mudava · Usuária via tela com resultado da config anterior achando que era da nova. Bug de UX que viola C.2 (nada silencioso · tela mente sobre estado atual) a nível de interface.
Decisão: implementar gate de stale em app_v2.py · _tela_resultado que detecta mudanças nos campos críticos da config após última execução · marca resultado como stale · força nova execução. Implementação:

Hash determinístico (_hash_config_critica() usando hashlib.sha256) sobre payload (config + nome_arquivo + aba_selecionada)
Hash armazenado em _hash_config_executada no momento da execução bem-sucedida
Gate na tela RESULTADO compara hash atual × hash executado · se diferente: st.warning("⚠️ A configuração foi alterada após a última execução · clique em Executar análise para atualizar") + botão de re-execução
Razão:
Hash determinístico é mais robusto que flag binária · captura QUALQUER mudança em campo crítico (não só semantica_campo) · sem manutenção
Solução foi mais ampla que o requisito original do prompt · escolha consciente de Claude Code · alinhada com princípio "default protege Usuária"
C.2 preservada · Usuária nunca vê resultado stale como se fosse atual
Impacto:
src/app_v2.py · novos defaults _hash_config_executada e função _hash_config_critica() · gate visual em _tela_resultado
Suite Sessão 5 · +2 testes UI (D-186) · validam gate disparando + re-execução limpando estado stale
Camada 2 da Sessão 5 (Usuária) validou empiricamente · "atualizando a página como um todo, a análise semântica ajustou. Pode ser algo relacionado a cache."
Referência canônica: src/app_v2.py · D-186 (resolve sintoma original que era atribuído erroneamente a D-182).

### D-185 — Método de próximas sessões · documentação e investigação precedem ação · sessões de escopo completo em vez de fragmentadas
Data: 2026-04-24 · Bloco: ALINHA-Retroação-V2 · Status: Fechada · vigora a partir da Sessão 5
Contexto: Sessões 4-ter + 4-ter-bis acumularam 23 pontos de correção (P-1 a P-23) descobertos iterativamente pela Usuária ao longo da camada 2 do gate duplo D-174. Padrão observado: cada print revelava defeito novo · cada defeito gerava decisão · cada decisão puxava mais decisão · ao final a Usuária declarou que "se a gente for fazendo, aí é muita coisa pra documentar e quando a gente vai ver tem que voltar e a minha sensação de frustração é muito maior". O problema metodológico é estrutural: sessões de correção reativas são eficientes para Claude Code mas custosas para a Usuária operar (camada 2 do gate). Adicionalmente, descoberta tardia de P-23 (bug estrutural de motor) na 3ª iteração da sessão indica que padrão "corrigir e iterar" mascara raízes em vez de revelá-las.
Decisão: A partir da Sessão 5, adotar 3 fases explícitas em sessões operacionais:
Fase (a) · Investigação e planejamento (precede o prompt para Claude Code):

Investigação dirigida quando há suspeita de bug estrutural · Arquiteto propõe prompt de leitura apenas (sem correção) · Claude Code retorna diagnóstico antes de qualquer correção
Escopo consolidado · Arquiteto propõe ANTES de abrir o prompt toda a lista de pontos que serão cobertos · Usuária valida escopo como um todo · prompt único cobre tudo
Documentação anterior absorvida · todas as decisões estruturais que emergiram de sessões anteriores são formalizadas como D-XXX ANTES da próxima sessão de implementação abrir · não durante

Fase (b) · Implementação Claude Code: prompt único com escopo fechado · sem ajustes incrementais. Se nova questão emerge, vira backlog para sessão seguinte (não puxa o prompt).
Fase (c) · Validação camada 2: Usuária valida o produto entregue · não abre escopo novo. Se aparece defeito durante a validação, abre nova sessão de correção dirigida · não reabre a sessão atual.
Aplicação imediata:

Sessão 5 (correção P-22 + P-23) abre com investigação dirigida primeiro · não com prompt de correção direto
Sessão F-APRESENT-cleanup também segue este padrão · investigação do que está catalogado como TODO + consolidação em prompt único
Sessões de refino de DCV (Fase 0) e sessões de Spec técnica (S-VN) já operam assim · este padrão estende para sessões combinadas D-155 e sub-sessões de correção

Razão:

Ergonomia da Usuária. Camada 2 do gate duplo é trabalho dela · 30 minutos de inspeção visual + correções múltiplas em cascata = 3-4 horas reais · inviável como padrão normal.
Qualidade da correção. Correção por iteração tende a consertar sintomas, não raízes · P-23 (bug de motor) só foi descoberto na 3ª iteração desta sessão · poderia ter sido na 1ª se a investigação precedesse a implementação.
Rastreabilidade. Decisões formalizadas ao longo da sessão (não no final) produzem rastro melhor · evita sensação de acumulação narrada pela Usuária.
Alinhamento com D-142 ALINHA. Sessões de Marco já operam no padrão α·β·γ·δ (consolidação → talk-through → formalização → kit) · D-185 estende princípio similar para sessões operacionais não-Marco.
Declaração explícita da Usuária. "Eu preciso ter certeza que o nosso motor está funcionando de uma forma assertiva. Pra que as próximas visões estejam corretas. E aí eu preciso que você documente bem tudo isso."

Impacto:

Instrucoes_do_Projeto.md v3.3 · nova seção "Condução de sessões operacionais" com padrão 3-fases + revisão de "Ritual de encerramento"
CONTEXT.md v3.3 · §15 ganha §15.14 sobre ordem de condução · §11 ganha referência ao padrão 3-fases
Sessão 5 é a 1ª aplicação · prompt de abertura já no formato novo
Precedente para F-APRESENT-cleanup e todas as A-VN futuras

Referência canônica: Instrucoes_do_Projeto v3.3 seção "Condução de sessões operacionais" · CONTEXT §15.14 · D-142 (precedente ALINHA) · D-185.

### D-184 — ALINHA-Retroação-V2 fechada como Marco antecipado · consolidação da descoberta de bug estrutural de motor
Data: 2026-04-24 · Bloco: ALINHA-Retroação-V2 (próprio) · Status: Fechada · Marco
Contexto: ALINHA-Retroação-V2 estava prevista (D-167) como Marco para ser executada após VV-V2 retroativa concluída (pós-Sessão 5). Materializou-se antecipadamente nesta sessão (24/04/2026 fim da tarde) quando a Usuária declarou que "essa é a sessão mais importante até agora" após a descoberta do P-23 (semântica invertida em T-SEMA · bug estrutural grave em motor V2 que afeta potencialmente 8 das 11 visões).
Decisão: ALINHA-Retroação-V2 formalizada como Marco fechado nesta sessão · aplicando padrão D-142 com 4 sub-blocos:
α · Consolidação retrospectiva (implícita ao longo desta sessão):

Sessão 4-ter (23-24/04 manhã) · implementação F-APRESENT na V2 retroativa · 652/652 verdes · Excel básico funcional · tela Validação Visual ainda técnica
Sessão 4-ter (continuação · 24/04 manhã) · camada 2 revelou 13 pontos (P-1 a P-13) · Usuária optou por reformular em vez de descartar
Sessão 4-ter-bis (24/04 tarde) · 5 correções cirúrgicas C-1 a C-5 · 660/660 verdes · Excel "do jeito que a gente esperava" (declaração Usuária)
Sessão 4-ter-bis camada 2 (24/04 fim da tarde) · descoberta P-22 (gráfico cortando título · pequeno) + P-23 (bug estrutural de motor · grave)

β · Talk-through operacional (consolidado nas decisões D-174 a D-185):

Gate duplo D-174 provou seu valor · pegou bug que 301 testes automatizados não pegaram
F-APRESENT tem dívida técnica formalizada (5 TODOs em código) · sessão dedicada pré-V1 confirmada
Método de próximas sessões reformulado · D-185

γ · Formalização de decisões: 12 D-XXX novas mais 1 promoção (D-170 Provisória → Fechada).
δ · Kit de encerramento: este kit ALINHA-Retroação-V2 (kit pesado · padrão δ de D-142).
Valor desta sessão: validação empírica do método TabloFlow. Gate duplo D-174 identificou bug estrutural em motor que testes automatizados não pegaram. Padrão de correção por iteração demonstrou limite operacional. Resultado: método revisado com aprendizados incorporados, não abandonado. V2 retroativa continua aberta aguardando correção P-22 + P-23 · mas infraestrutura de produto (F-APRESENT consumido · tela Resultado · Gate duplo · princípios de uniformidade) consolidada com qualidade.
Razão:

Todos os 3 critérios de D-142 preenchidos: (a) transição de modo operacional (de correção reativa para investigação dirigida D-185) · (b) fecha subsistema (F-APRESENT aplicado a V2 com qualidade · mesmo com bugs pendentes) · (c) ≥3 pendências estruturais (D-174 a D-185 novas · 12 entradas).
Usuária explicitamente solicitou formalização: "essa sessão foi a mais importante, eu preciso que você documente bem tudo isso".
Momento é transição: próxima sessão tem natureza diferente (investigação de motor · não correção de apresentação) · D-142 prevê exatamente este gatilho.
Antecipação é consistente com ALINHA-Descoberta-Camada-Produto (23/04) · que também foi Marco emergente · D-142 aplicada em condições análogas.
Kit pesado δ formaliza aprendizados com peso simbólico correto · compatível com a declaração da Usuária sobre a importância desta sessão.

Impacto:

12 D-XXX novas (D-174 a D-185) + 1 promoção (D-170 Provisória → Fechada · 3 aplicações)
CONTEXT.md v3.3 com absorção das 13
Instrucoes_do_Projeto.md v3.3 com seção nova "Condução de sessões operacionais" + ajustes em "O que NÃO fazer"
Planilha reestruturada com V2 em status ⚠️ bloqueada por bug de motor P-23 · horizontes atualizados
GLOSSARIO v4 com 8 verbetes novos
vocabulario_bilingue v3 com Bloco 9 (rótulos de semântica · "Subir é bom/ruim/neutro")
Próxima sessão = Sessão 5 · investigação dirigida P-22 + P-23 · formato novo D-185

Referência canônica: DECISIONS D-170 (revisada) · D-174 a D-185 · Instrucoes_do_Projeto v3.3 · CONTEXT v3.3 · Planilha pós-Sessão 4-ter-bis · D-142 (padrão ALINHA invocado).

### D-183 — Princípio "Motor primeiro · apresentação depois" · C.D7 · 7º derivado da Camada C
Data: 2026-04-24 · Bloco: ALINHA-Retroação-V2 · Status: Fechada · promove princípio derivado
Contexto: P-23 (semântica invertida em T-SEMA) foi descoberto na camada 2 do gate duplo de VV-V2 retroativa. O bug afeta classificacao_semantica no V2Result · cálculo analítico · não apenas apresentação. Os 301 testes verdes do motor V2 não pegaram este caso · significa que nenhum teste cobre cenário MENOR_MELHOR em T-SEMA. Consequência grave: F-APRESENT foi implementado e testado durante 3 sessões (P0 · P1 · 4-ter) consumindo V2Result onde classificacao_semantica estava errado desde o início · todo o trabalho de formatação visual/paleta/badges operou sobre dado incorreto e ninguém percebeu porque a estética estava certa.
Decisão: Promover princípio ao catálogo canônico de princípios derivados da Camada C (CONTEXT §9) como C.D7 · Motor primeiro, apresentação depois · 7º derivado formalizado.
Enunciado:

"Validação empírica de corretude do motor analítico precede validação empírica de apresentação. Em qualquer visão, a primeira sessão de validação (VV-VN camada 2) que a Usuária executa deve incluir inspeção explícita dos valores calculados e das classificações semânticas antes da inspeção estética do produto. Excel formatado corretamente com número errado é pior que Excel mal formatado com número certo · porque o primeiro passa despercebido e propaga erro silenciosamente (violação retroativa de C.2)."

Regras operacionais derivadas:

Em VV-VN camada 2, a Usuária inspeciona primeiro a aba Matriz de Confronto / Coração Visual com foco em sanity check numérico e classificatório antes de inspecionar Resumo Executivo ou Diagnóstico. Checklist VVC de cada visão tem seção dedicada "Sanity check de cálculo" · itens primários.
Em A-VN antes do gate duplo, Claude Code deve produzir amostra com tabela de sanity check do motor · ex: 10 combinações escolhidas do DataFrame com classificacao_semantica declarada explicitamente + contraste visual com semantica_campo declarada. Retrospectiva da A-VN inclui esse artefato.
Em V-VN (motor), os testes obrigatórios do motor devem cobrir a matriz cartesiana completa dos campos semânticos estruturais. Para V2: cobrir MAIOR_MELHOR × {AUMENTOU, REDUZIU, ESTAVEL, NAO_APLICAVEL} + MENOR_MELHOR × {AUMENTOU, REDUZIU, ESTAVEL, NAO_APLICAVEL} + NEUTRO × {mesmo} = 12 casos-teste mínimos · cada um com assertion explícito do par (classificacao_estrutural, classificacao_semantica).
Em F-APRESENT, capabilities consomem V2Result confiando no contrato mas testes de capability incluem fixture com caso MENOR_MELHOR · não apenas MAIOR_MELHOR.

Razão:

Lição dolorosa mas clara. P-23 é exatamente o tipo de bug que C.D7 existe para prevenir.
Alinhamento com C.1 (determinismo) e C.5 (TabloFlow analisa sobre o dado informado · nunca decide por ele). Se o motor analisa errado, o determinismo perde valor · C.5 vira fachada.
Extensão natural de BAD · C.D3 (D-124). BAD (Base Analítica e Diagnóstico) é produto final que supõe motor correto · C.D7 é a pré-condição operacional dessa suposição.
Coerência com C.D6 DDU. DDU formaliza "Default Declarado Universal" · C.D7 formaliza "validação do motor precede validação do produto" · ambos materializam C.5 em regras operacionais.
Aplicabilidade cross-visão. Toda visão numérica (8 de 11: V1 · V3 · V4 · V7 · V8 · V9 · V10 · V11 · além de V2) consome T-SEMA · todas herdam C.D7.

Impacto:

CONTEXT §9 · Camada C · catálogo de derivados passa de 6 (C.D1 a C.D6) para 7 (C.D1 a C.D7)
CONTEXT §15.8 (VV-VN camada 2) ganha "Sanity check numérico" como seção primária do checklist VVC
spec_v2.md · seção de testes do motor V2 ganha matriz cartesiana obrigatória T-SEMA · retroação a executar na Sessão 5 de correção P-23
Instrucoes_do_Projeto v3.3 · "O que NÃO fazer" ganha: "Não declarar sessão A-VN/VV-VN concluída sem sanity check numérico explícito sobre caso MENOR_MELHOR quando aplicável"
V-VN futuras (V1 · V11 · V4 · V10 · V3 · V8 · V7 · V9 · V5 · V6) herdam regra · testes do motor cobrem matriz cartesiana T-SEMA
Sessão 5 aplica retroativamente · testes novos de T-SEMA no V2 são pré-requisito de fechamento

Referência canônica: CONTEXT §9 · Camada C · C.D7 · DECISIONS D-183 · spec_v2.md (retroação pendente) · Instrucoes_do_Projeto v3.3.

### D-182 — REVISADA · investigação dirigida da Sessão 5 refutou descrição original · sintoma se decompõe em D-186 (cache) + D-187 (NEUTRA expandida)
Data: 2026-04-25 · Bloco: Sessão 5 · investigação dirigida (D-185) · Status: Fechada · revisada in-place
Contexto: D-182 original (24/04/2026) declarou "P-23 · semântica T-SEMA invertida no motor V2 · criticidade ALTA · bloqueante para fechamento V2 retroativa" baseada em sintoma reportado pela Usuária ("trocar rádio MAIOR_MELHOR/MENOR_MELHOR produzia mesmo resultado errado"). Sessão 5 abriu com investigação dirigida (Fase a · D-185) ANTES de qualquer correção. Diagnóstico Claude Code provou: motor V2 está matematicamente correto · 4 testes verdes cobrem MAIOR/MENOR × AUMENTOU/REDUZIU. Hipóteses A/B/C de D-182 caíram. Usuária validou empiricamente em 2 sub-sessões: o sintoma reportado vinha de cache do app (D-186) · não do motor.
Decisão: D-182 status muda de "Aberta · ALTA · bloqueante" para "Fechada · investigação refutou hipótese". Sintoma original se decompõe em 2 problemas reais distintos:

Cache do app V2 (D-186) · invalida session_state quando campo da Etapa 3 muda
Bug NEUTRA (D-187) · achado novo da investigação · _SEMA_LABEL_TO_CLASS colapsava 3 estruturais em código semântico único · não é o que D-182 supunha mas é bug real
D-182 fica como rastro histórico de "sintoma reportado · investigação reorientou hipótese" · não é revogada (preserva numeração) · ganha nota visível "REVISADA" no título.
Razão:

D-185 padrão 3 fases acaba de pagar dividendo na 1ª aplicação · investigação dirigida descobriu que P-23 era cache + NEUTRA · não T-SEMA invertida · evitou correção em alvo errado
Padrão de revisão in-place (manter numeração · adicionar nota REVISADA) é coerente com D-024 superada por D-161 e padrões similares · revogar e renumerar perde rastro · revisar in-place preserva
Camada 2 do gate D-174 confirmada como instrumento que descobre achados que Camada 1 mecânica não pega · 1ª aplicação clara
Impacto:
D-182 título ganha sufixo "REVISADA · investigação refutou hipótese · raiz real em D-186 (cache) + D-187 (NEUTRA)"
Status muda · vencimento removido (sessão 5 já consumiu · agora redirecionado)
D-186 e D-187 nascem com referência cruzada a D-182
Lição estende D-185 · padrão 3 fases é vinculante para sessões com criticidade ALTA
Referência canônica: D-182 (revisada · status Fechada) · D-186 · D-187 · D-185 (padrão de investigação aplicado).

### D-181 — Débito menor · P-22 · gráfico de variações em destaque cortando título da seção
Data: 2026-04-24 · Bloco: ALINHA-Retroação-V2 · Status: Aberta · vencimento Sessão 5 (junto com P-23)
Contexto: Camada 2 do gate duplo D-174 de VV-V2 retroativa revelou que o BarChart de "Variações em destaque" no Resumo Executivo está sobreposto ao banner de cabeçalho da seção · ancora em posição que invade visualmente o título. Defeito puramente de posicionamento estético · não afeta cálculo nem dado.
Causa técnica provável: âncora do gráfico (anchor_cell=f"D{linha_aux_header}") está colocando o gráfico em cima da linha do banner, não abaixo dele. Cálculo de offset em exportacao_v2.py não reservou espaço vertical suficiente entre o final da tabela top e a área onde o gráfico ancora.
Decisão: P-22 entra na Sessão 5 junto com P-23 · porque ambos serão tratados em mesma sessão de correção dirigida (formato D-185) · economia operacional. Correção mecânica simples: ajustar âncora do BarChart para D{linha_aux_header + offset} · garantir respiro vertical mínimo acima do gráfico · reservar 2-3 linhas vazias entre o banner da seção e a área do gráfico.
Razão:

Sessão 5 já vai abrir para P-23 · custo marginal de incluir P-22 é mínimo
Ambos são correções em exportacao_v2.py · escopo coeso para o Claude Code
P-22 é puramente estético · não bloqueia funcionalidade · não justifica sessão dedicada
Sessão 5 vai consumir testes que rodam o Excel pós-correção · adicionar verificação de posicionamento de gráfico no mesmo ciclo é eficiente

Impacto:

Sessão 5 inclui P-22 no escopo (sem prompt extra)
Teste novo: assertion sobre chart.anchor.from_.row ≥ linha_banner + N mínimo
Após correção, fica como TODO-FAPRESENT-CLEANUP · capability 11 deveria gerenciar offset automaticamente baseado em estrutura de seção (banner + tabela + gráfico)

Referência canônica: DECISIONS D-181 · Sessão 5 (vencimento).

### D-180 — Sessão F-APRESENT-cleanup pré-V1 formalizada · consome 5 TODO-FAPRESENT-CLEANUP catalogados
Data: 2026-04-24 · Bloco: ALINHA-Retroação-V2 · Status: Aberta · vencimento entre Sessão 5 (correção motor V2) e P-V1 (1ª sessão de Fase 2 V1)
Contexto: Sessão 4-ter-bis introduziu regra META-1 (rastreabilidade obrigatória) · toda correção bespoke em exportacao_v2.py ou app_v2.py que pertenceria a F-APRESENT leva comentário # TODO-FAPRESENT-CLEANUP: <descrição clara>. Claude Code catalogou 5 ocorrências:
#Arquivo:linha aproximadaPromover para1exportacao_v2.py · ~692Capability 3 · criar_tabela_executiva deveria aplicar number_format à totalsRow herdando de cada coluna2exportacao_v2.py · ~782Capability 3 · idem (Base Analítica)3exportacao_v2.py · ~492Capability 11 · criar_grafico_top_variacoes deveria aceitar parâmetro unidade e aplicar number_format no eixo de valores automaticamente4exportacao_v2.py · ~278Capability nova em F-APRESENT (renderizar_secao_estruturada) · helper _renderizar_secao_como_tabela será consumido por Resumo Executivo e Diagnóstico de todas as visões5app_v2.py · ~150Capability 2 estendida ou capability auxiliar nova (rotular_coluna_tecnica) · helper _rotular_agrupador_ui + tabela de especiais (Centro_Custo · Mes) deve morar no vocabulário canônico F-APRESENT
Decisão D-9 (era informal · só nomenclatura α·β·γ no histórico) formalizada como D-180.
Decisão: Sessão dedicada F-APRESENT-cleanup · consome os 5 TODOs · objetivo único: extrair código bespoke de exportacao_v2.py/app_v2.py e promover para /src/apresentacao/*.py como capabilities ou extensões de capabilities existentes.
Escopo da sessão:

TODO 1+2 → estender capability 3: criar_tabela_executiva aceita parâmetro opcional unidades_por_coluna: Dict[str, str] e aplica number_format correspondente em totalsRow
TODO 3 → estender capability 11: criar_grafico_top_variacoes aceita parâmetro unidade_valor: str e aplica number_format no eixo
TODO 4 → criar capability nova renderizar_secao_estruturada em F-APRESENT (capability 12 · próximo número disponível) · com assinatura genérica (paleta · título · linhas_conteudo · col_inicial · col_final) · resumo_executivo e diagnostico de todas as visões consomem
TODO 5 → estender capability 2: catálogo de especiais (Centro_Custo → Centro de Custo · Mes → Mês) migra para vocabulario_bilingue · função traduzir_coluna_tecnica exportada

Após cleanup:

exportacao_v2.py consome F-APRESENT puro · nenhum bespoke
app_v2.py consome capability 2 estendida para tradução de UI
Todos os 5 TODOs removidos
Suite F-APRESENT cresce com testes novos para capabilities estendidas (11+12 + extensões 2/3/11)
Suite V2 continua passando · agora consumindo F-APRESENT canônico

Pré-requisito: Sessão 5 (correção motor V2 P-22 + P-23) deve ter fechado · porque cleanup vai mexer em apresentação de dados que precisam estar corretos.
Razão:

C.D6 DDU + C.D7 motor primeiro: capabilities precisam ser canônicas antes de V1/V11 abrirem · senão os bespokes da V2 viram precedente para bespokes da V1 · cascata.
Princípio de uniformidade transversal D-175 (NOVO): F-APRESENT só atende a uniformidade se as capabilities cobrirem o que cada visão precisa · 5 TODOs identificam exatamente os 5 gaps.
Padrão de F-APRESENT P0/P1: subsistema foi construído incrementalmente (P0 com 7 capabilities · P1 com 3 mais) · F-APRESENT-cleanup é P2 conceitual · consolida + estende.
Custo de não fazer: V1 vai duplicar cada bespoke da V2 · V11 vai duplicar de novo · em vez de 5 TODOs em 1 visão, vira 55 TODOs em 11 visões. Aritmética simples.

Impacto:

1 sessão Claude Code dedicada · estimativa 60-90 min de execução + camada 2 da Usuária
F-APRESENT v2 (capability 12 nova + extensões em 2/3/11)
Refactor leve em exportacao_v2.py e app_v2.py · troca de bespoke por chamada à capability
Suite total cresce em ~15-25 testes (capabilities novas + integration)
Pré-requisito explicitamente declarado para abertura de P-V1 (Spec produto V1)

Referência canônica: DECISIONS D-180 · D-175 (uniformidade) · D-159 (F-APRESENT P0+P1 · esta seria P2) · 5 TODOs catalogados em código pós-Sessão 4-ter-bis.

### D-179 — Lista negativa expandida · vocabulário bilingue v3 · 8 categorias de vazamento técnico proibido
Data: 2026-04-24 · Bloco: ALINHA-Retroação-V2 · Status: Fechada · estende D-160 · vigora a partir de Sessão 5
Contexto: D-160 (Vocabulário bilingue obrigatório · técnico canônico ↔ user-facing · 22/04/2026) estabeleceu princípio de zero vazamento técnico em superfícies user-facing. Sessão 4-ter + 4-ter-bis revelaram categorias adicionais de vazamento que D-160 não previa explicitamente · descobertas via inspeção visual de Excel e tela do app.
Decisão: Expandir lista negativa de vocabulario_bilingue.md como Bloco 9 (novo) · 8 categorias proibidas em superfícies user-facing:

Snake_case técnico (já em D-160 · agora explícito) · ex: Centro_Custo · tipo_campo · semantica_campo · valor_origem
Códigos de avisos/warnings · ex: V2-A01 · W-V2-PAGREG-DUP · T-SEMA · MBO-N · ficam no log técnico nunca em superfície
Identificadores Pydantic literais · ex: MAIOR_MELHOR · NUMERICO_ADITIVO · POSITIVO · PRESENTE_AMBOS · ficam no contrato nunca em UI
dict serializado / JSON cru · ex: {'campo_x': 100, 'campo_y': 200} · ficam no diagnóstico técnico nunca em Excel/app
Enums caps sem tradução · ex: SOMA · MEDIA · MEDIA_PONDERADA · ficam como tradução user-facing ("Soma" · "Média" · "Média ponderada")
Valores nulos visíveis · ex: NULL · null · NaN · nan · (null) · None · sempre traduzidos para — ou microcopy contextual (ex: — (não consta), — (sem valor))
Nomes em colchetes/parênteses técnicos · ex: [campo_x] · <valor> · (legacy_field) · removidos
Frações cruas em vez de percentual · ex: 0.03622154 em célula de "Variação %" · sempre formatado como 3,62% (formato BR)
Aspas literais em texto user-facing · ex: "Receita Realizado" em label · ficam sem aspas em UI

Aplicação:

vocabulario_bilingue.md ganha Bloco 9 com tabela de proibidos × tradução obrigatória
F-APRESENT capability 2 estende sua função de tradução para detectar e bloquear cada categoria · warning estrutural se vazamento detectado
Testes de F-APRESENT incluem grep automático para cada categoria em outputs Excel e em strings renderizadas via at.dataframe/at.markdown em testes do app
Cada visão futura herda regra · A-VN tem item de checklist mecânico verificando cada categoria

Razão:

D-160 era princípio · D-179 é operacionalização. Princípio sem lista negativa explícita produziu drift em V2 (descoberto na camada 2 · ex: Centro_Custo em header de tabela · 0.03622154 em célula).
Valor da inspeção visual. Camada 2 do gate duplo D-174 catalogou cada categoria empiricamente · esta é a lista que cobriria o que foi encontrado.
C.2 (nada silencioso) aplicado a vocabulário. Vazamento técnico é forma de "decisão silenciosa" do produto · usuário não entende o que está vendo.
Coerência com C.D6 DDU. DDU formaliza "default declarado" · D-179 formaliza "default traduzido" · ambos materializam C.5.

Impacto:

vocabulario_bilingue.md v3 · novo Bloco 9
F-APRESENT capability 2 ganha função validar_zero_vazamento(texto, contexto) → List[Vazamento] · usada em testes
Testes de F-APRESENT crescem com matriz de 9 categorias × 4 superfícies (Excel · st.dataframe · st.markdown · st.metric)
Sessão F-APRESENT-cleanup (D-180) absorve esta extensão · capability 2 estendida lá

Referência canônica: vocabulario_bilingue.md v3 Bloco 9 · D-160 (princípio raiz) · D-179 (operacionalização) · F-APRESENT capability 2.

### D-178 — TED migra de sidebar para expander no topo da tela "Resultado da análise" · revogação parcial de D-153
Data: 2026-04-24 · Bloco: ALINHA-Retroação-V2 · Status: Fechada · revoga parcialmente D-153 · validada empiricamente
Contexto: D-153 (TED em sidebar global · 22/04/2026) decidiu por sidebar global como home dos thresholds editáveis. Sessão 4-ter aplicou e a Usuária reportou na camada 2 (P-1): "o TED na sidebar polui · usuário acaba não vendo · queria ele perto dos resultados". Decisão tomada na sessão: mover TED para expander colapsável no topo da tela "Resultado da análise" · sidebar limpa para futuras configurações globais que não sejam de visão específica.
Decisão: TED de cada visão renderizado como st.expander("⚙️ Configurações avançadas (limites editáveis)", expanded=False) no topo da tela final de produto da visão (V2: tela "Resultado da análise"). Sidebar reservada para configurações globais cross-visão (ex: paleta default global · idioma · perfil de empresa · preferências de exportação).
Aplicação validada empiricamente: Sessão 4-ter-bis aplicou e Usuária aprovou na camada 2 ("TED expander no topo, sidebar limpa, ficou perfeito").
Razão:

Empírico: sidebar saturava com TED + paleta + outras configurações · expander dedicado dá controle visual.
Princípio de proximidade: TED altera resultado · ficar perto do resultado faz sentido cognitivo.
Reversibilidade preservada: sidebar continua disponível para outras coisas · não foi eliminada · só perdeu o TED.
Coerência com TED como C.D2: C.D2 (Thresholds Editáveis Declarados) exige visibilidade · expander colapsável + título descritivo + ícone ⚙️ atende visibilidade sem poluir.
Padrão herdável cross-visão: todas as 11 visões podem aplicar mesmo padrão · TED por visão fica próximo do produto da visão.

Impacto:

D-153 revogada parcialmente · sidebar global continua existindo mas TED migra para expander
app_v2.py aplica padrão na tela "Resultado da análise" (já feito em Sessão 4-ter)
DCV/Spec de cada visão futura aplica mesmo padrão · seção "TED no expander do topo da tela final"
CONTEXT §13.3 (Modelo de configuração) ganha nota: "TED em expander no topo da tela final · não em sidebar"

Referência canônica: DECISIONS D-178 (revoga parcialmente D-153) · CONTEXT §13.3 atualizado · app_v2.py (1ª aplicação validada).

### D-177 — Tela "Validação Visual" reformulada como "Resultado da análise" · microanálise executiva em tela
Data: 2026-04-24 · Bloco: ALINHA-Retroação-V2 · Status: Fechada · revisão substancial de tela do app
Contexto: A tela "Validação Visual" do app_v2.py (estado pré-Sessão 4-ter) renderizava o checklist VVC técnico (códigos V2-A01 · V2-A02 · etc) com botão "Visão aprovada" como gate de download · st.json com dump técnico · estrutura de checklist mecânico. Camada 2 da Sessão 4-ter (P-4) revelou que essa tela era ritual VVC construtor (Fase 2 · Arquiteto+Usuária validando construção) · não produto. Mostrar para usuário final é confundir construção com produto.
Decisão: Tela NÃO removida (correção da percepção inicial do Arquiteto que sugeriu remoção · Usuária recalibrou: "é importante, é como se fosse uma microanálise em tela"). Tela é reformulada com:
Novo nome: "Resultado da análise"
Novo papel: Microanálise executiva em tela · prévia fiel do Excel · antes de baixar.
Saiu:

Checklist com códigos técnicos (V2-A01 · W-V2-*)
Botão "Visão aprovada" e gate de download condicional
st.json com dump técnico
Qualquer rastro de ritual VVC construtor

Entrou:

4 cards de métricas (números-âncora) com st.metric ou layout equivalente
Tabela de distribuição de classificações estruturais
Tabela de top variações em destaque
Gráficos inline (BarChart equivalente ao Excel)
Leitura qualitativa em prosa (espelho do Excel)
Expander "Ver detalhes do diagnóstico" com decisões e thresholds aplicados
Rodapé com dropdown de paleta + botão "Baixar Excel"

Padrão herdável cross-visão: todas as 11 visões terão tela "Resultado da análise" como espelho fiel do Excel · não checklist técnico.
Onde foi parar o checklist VVC:

Continua existindo como ritual construtor externo (Fase 2 · Arquiteto+Usuária) · em markdown · documento de apoio · não em UI de produto
Para V2: substituído pelo CHECKLIST_MECANICO.md que Claude Code produz a cada A-VN (com ~75 itens binários automatizados executados por Claude Code · camada 1 do gate duplo D-174)
Camada 2 do gate duplo D-174 = Usuária inspeciona produto final (Excel + tela "Resultado da análise") com base no checklist VVC do DCV · não dentro do app

Razão:

Recalibração da Usuária: "a tela em si é importante · só não traga os códigos · traga em formato aceitável" · diferenciação entre informação técnica vs apresentação executiva da mesma informação.
C.5 (analisa sobre o dado · nunca decide): tela executiva apresenta o que foi analisado · não pede para o usuário aprovar processo interno.
Princípio "Excel é produto" (D-163): tela final do app deve espelhar o Excel · não ser ritual paralelo.
Separação Fase 2 (construtor) vs runtime (produto): VVC é Fase 2 · não cabe em produto rodando.
Empírico: tela reformulada validada na camada 2 da Sessão 4-ter-bis · "layout executivo, ficou ótimo".

Impacto:

app_v2.py · função _tela_resultado substitui _tela_validacao_visual (já feito em Sessão 4-ter · refinado em 4-ter-bis)
Padrão para 11 visões · cada P-VN seção "Tela final" usa "Resultado da análise" como nome canônico
DCV ganha (em refinos futuros) seção "Tela final no app · Resultado da análise" como cross-visão padrão
CONTEXT §13 (padrões estruturais) ganha princípio implícito: "tela final do app é espelho do Excel · não ritual de validação"

Referência canônica: DECISIONS D-177 · app_v2.py (1ª aplicação) · D-163 (Excel é produto) · D-162 (VVC vs VVP).

### D-176 — Capability 11 de F-APRESENT · Gráficos + nomenclatura executiva
Data: 2026-04-24 · Bloco: ALINHA-Retroação-V2 · Status: Fechada · F-APRESENT cresce de 10 para 11 capabilities
Contexto: F-APRESENT P0+P1 (D-159 · 23/04/2026) entregou 10 capabilities canônicas. Sessão 4-ter implementou V2 consumindo F-APRESENT e identificou 2 gaps estruturais que não cabiam em nenhuma das 10 capabilities existentes:

Gráficos Excel (BarChart · PieChart · LineChart) com paleta aplicada · nenhuma capability atende
Nomenclatura executiva de arquivo Excel (ex: "Análise Comparativa - Janeiro vs Fevereiro - 24-04-2026.xlsx" em vez de v2_export_20260424_173523.xlsx)

Decisão: Criar capability 11 · Gráficos executivos + nomenclatura de arquivo em F-APRESENT.
Localização: /src/apresentacao/graficos.py (parte gráfica) + /src/apresentacao/nomenclatura.py (parte de nome de arquivo).
Interfaces canônicas:
python# /src/apresentacao/graficos.py
def criar_grafico_distribuicao(
    ws, anchor_cell, dados_range, paleta_nome, titulo
) -> PieChart: ...

def criar_grafico_top_variacoes(
    ws, anchor_cell, dados_range, paleta_nome, titulo, unidade_valor="monetario"
) -> BarChart: ...

# /src/apresentacao/nomenclatura.py
def nomear_excel_executivo(
    visao_familia: str,  # "comparativa" | "evolutiva" | etc
    contexto: dict,      # {"origem": "Janeiro 2025", "comparado": "Fevereiro 2025"}
    data_geracao: datetime
) -> str: ...
Default cross-visão:

BarChart horizontal para top variações (verde/vermelho/cinza por sinal)
PieChart para distribuição categórica (somente quando categoria principal < 60%)
Nomenclatura: {Família} - {Contexto} - {Data DD-MM-AAAA}.xlsx

Razão:

Gap claro: F-APRESENT P0+P1 não previu gráficos · descobertos na 1ª aplicação real (V2)
Cross-visão: todas as 11 visões usarão gráficos · capability canônica evita 11 implementações
Nomenclatura executiva: Usuária explicitamente apontou que nome técnico de arquivo (com timestamp ISO) é "vazamento de dev em produto user-facing" (P-12)
Padrão de F-APRESENT preservado: capabilities têm interface estável · injetam paleta · funcionam standalone · capability 11 segue mesmo padrão

Impacto:

F-APRESENT cresce para 11 capabilities (era 10)
Sessão F-APRESENT-cleanup (D-180) inclui refinamento de capability 11 (TODO 3) · criar_grafico_top_variacoes ganha parâmetro unidade_valor opcional para aplicar number_format correspondente no eixo
CONTEXT §6.2 e §15.12 atualizados com 11 capabilities
spec_v2.md e P-V2 ganham seção "Gráficos consumidos via capability 11"

Referência canônica: DECISIONS D-176 · CONTEXT §6.2 e §15.12 atualizados · /src/apresentacao/graficos.py · /src/apresentacao/nomenclatura.py · D-180 (cleanup pendente em capability 11).

### D-175 — Princípio de uniformidade transversal F-APRESENT · 8º padrão estrutural cross-visão
Data: 2026-04-24 · Bloco: ALINHA-Retroação-V2 · Status: Fechada · adiciona 8º padrão a CONTEXT §13
Contexto: Camada 2 da Sessão 4-ter (P-8) capturou observação metodológica da Usuária: "o que está bom em uma aba precisa estar bom em todas · o que está mal em uma aba puxa todas para baixo". Defeitos de formatação descobertos no Resumo Executivo (P-7) eram qualitativamente diferentes dos da Matriz de Confronto (P-9) e dos da Base Analítica · sugerindo que cada implementação de aba estava sendo feita "à parte" e não como aplicação de padrão consolidado.
Decisão: Formalizar P-UNIF · Princípio de Uniformidade Transversal F-APRESENT como 8º padrão estrutural em CONTEXT §13.
Enunciado:

"Toda aba de produto Excel de toda visão consome F-APRESENT · não bespoke. Quando uma capability de F-APRESENT precisa ser estendida para suportar caso novo (ex: totalsRow com formato monetário), a extensão acontece em F-APRESENT · nunca em exportacao_vN.py da visão. Defeito visual em uma aba é defeito de capability de F-APRESENT · correção sobe para F-APRESENT · todas as visões herdam correção automaticamente. Bespoke em exportacao_vN.py é débito técnico explícito (META-1 · TODO-FAPRESENT-CLEANUP) · não solução."

Operacionalização:

exportacao_v2.py/exportacao_v1.py/etc consomem apenas funções de /src/apresentacao/* · zero formatação direta com openpyxl
Toda string visível ao usuário passa por capability 2 (vocabulário bilingue) · zero hardcode
Toda cor passa por paleta canônica (capability 1) · zero RGB hardcoded
Toda formatação numérica passa por capabilities 4 (monetário) ou 5 (percentual) · zero number_format solto
Bespoke transitório permitido apenas com comentário # TODO-FAPRESENT-CLEANUP: <descrição> · sessão F-APRESENT-cleanup (D-180) consome periodicamente

Critério de fechamento: uma visão N só fecha A-VN quando grep -r "TODO-FAPRESENT-CLEANUP" /src/visoes/exportacao_vN.py retorna zero ocorrências · OU quando todas as ocorrências têm vencimento declarado em sessão F-APRESENT-cleanup futura próxima.
Razão:

Empirismo: Sessão 4-ter mostrou que sem P-UNIF, defeitos visuais são corrigidos por visão · não por capability · cresce não-linearmente.
C.D6 DDU paralelo: DDU formaliza "default declarado" · P-UNIF formaliza "default uniforme" · ambos materializam consistência cross-visão.
Aritmética simples: 5 TODOs em 1 visão (V2) viram 55 TODOs em 11 visões se não houver cleanup · custo de manutenção explode.
Coerência com 7 padrões existentes: §13 já tem 7 padrões (Objetivo · Fluxo · Modelo · View especializada · Resumo Executivo · Coração Visual · Excel é produto) · P-UNIF é 8º natural · materializa "Excel é produto" do ponto de vista da implementação.

Impacto:

CONTEXT §13 ganha §13.8 P-UNIF · Princípio de Uniformidade Transversal F-APRESENT (8º padrão)
Instrucoes_do_Projeto v3.3 · "O que NÃO fazer" ganha: "Não implementar formatação visual em exportacao_vN.py sem comentário TODO-FAPRESENT-CLEANUP"
Pré-condição para abertura de A-V1, A-V11, A-VN futuras
Sessão F-APRESENT-cleanup (D-180) executa 1ª limpeza (5 TODOs da V2)
META-1 (rastreabilidade) é o mecanismo operacional de P-UNIF

Referência canônica: CONTEXT §13.8 · DECISIONS D-175 · D-159 (F-APRESENT origem) · D-180 (cleanup operacional).

### D-174 — Gate duplo · Validação Visual de A-VN · Claude Code automática + Usuária visual
Data: 2026-04-24 · Bloco: ALINHA-Retroação-V2 · Status: Fechada · contrato operacional de A-VN
Contexto: Sessão 4-ter (A-V2 retroativa · 1ª aplicação do método novo de Fase 2) declarou conclusão com 626/626 testes verdes em camada automatizada (suíte pytest). Camada 2 (Usuária inspecionando Excel + app) revelou 13 defeitos (P-1 a P-13) que a camada automatizada não pegou. Sessão 4-ter-bis corrigiu 5 grupos · camada 2 revelou mais 4 defeitos (P-14 a P-22). Sessão 4-ter-bis-2 (não chegou a abrir nesta sessão) confirmou descoberta de bug estrutural P-23 que 301 testes do motor + checklist mecânico não pegaram.
Lição: declaração de "sessão concluída" baseada apenas em testes automatizados é insuficiente · validação visual humana é parte essencial do gate de qualidade · principalmente em camada de apresentação (F-APRESENT) e em corretude semântica (T-SEMA).
Decisão: Toda sessão A-VN passa a operar com gate duplo obrigatório antes de declarar conclusão:
Camada 1 · Mecânica (Claude Code automática):

Suite pytest 100% verde (zero regressão · vermelhos pré-existentes catalogados)
CHECKLIST_MECANICO.md com itens binários ✅/❌ derivados do prompt da sessão · 100% ✅
Amostra Excel gerada no padrão da paleta default (Azul) · pelo menos 1 amostra
Output de grep -r "TODO-FAPRESENT-CLEANUP" declarado (zero ou catalogado para cleanup futuro)
Lista de bifurcações onde Claude Code teve que escolher e não tinha clareza · declarada explicitamente

Camada 2 · Visual (Usuária):

Inspeção do Excel produzido (todas as abas · paleta default + paletas alternativas via dropdown)
Inspeção do app rodando (streamlit run src/app_vN.py)
Sanity check numérico explícito (C.D7 · D-183) · principalmente em casos MENOR_MELHOR se aplicável
Validação contra checklist VVC do DCV (Validação Visual Construtora · D-156)
Aprovação explícita ou abertura de sub-sessão de correção dirigida

Sessão fecha apenas quando ambas as camadas aprovam. Caso (a): camada 1 ✅ + camada 2 ✅ → fecha. Caso (b): camada 1 ✅ + camada 2 com defeitos → abre sub-sessão de correção. Caso (c): camada 1 ❌ → Claude Code itera antes de submeter para camada 2.
Razão:

Empirismo dolorso: 3 sessões (4-ter · 4-ter-bis · descoberta P-23) demonstraram que camada 1 sozinha falha em capturar defeitos visuais e semânticos.
Camadas complementares · não substitutivas: camada 1 captura regressão e contrato · camada 2 captura experiência de produto e corretude semântica observável.
Coerência com D-162: VVC (Validação Visual Construtora) já existia como conceito · D-174 formaliza como gate operacional obrigatório.
Coerência com C.5: "TabloFlow analisa sobre o dado · usuário valida o produto" · gate duplo materializa o "usuário valida" como obrigatório.
Custo aceitável: camada 2 da Usuária custa 30-60 min por sessão A-VN · sub-sessão de correção custa 30-90 min · total 1-2.5h por A-VN · vs custo de fechar com bug estrutural não detectado.

Impacto:

Toda A-VN futura segue gate duplo · padrão operacional consolidado
CHECKLIST_MECANICO.md vira artefato canônico de A-VN (não opcional)
DCV ganha seção "Sanity check numérico para camada 2" derivada do contrato T-SEMA
Instrucoes_do_Projeto v3.3 · "Ritual de encerramento" ganha gate duplo explícito
CONTEXT §15.9 (retrospectivas pós-Claude Code) referencia D-174 explicitamente
Sessão F-APRESENT-cleanup (D-180) e Sessão 5 (P-22 + P-23) operam sob D-174

Referência canônica: DECISIONS D-174 · CONTEXT §15.9 · Instrucoes_do_Projeto v3.3 · D-162 (VVC origem conceitual) · D-183 (C.D7 sanity check numérico).


### D-173 — Débito estrutural · A-V2 não consome F-APRESENT na geração do Excel · Sessão 4 entregou integração parcial declarada como concluída
**Data:** 2026-04-24 · **Bloco:** VV-V2 retroativa (Sessão 5 · interrompida por descoberta) · **Status:** Aberta · vencimento em Sessão 4-ter (próxima)

**Contexto:** Sessão 5 (VV-V2 retroativa) aberta em 24/04/2026 tarde. Usuária operou `app_v2.py` · gerou Excel · identificou que o produto final exibe **exatamente os mesmos defeitos mapeados em VV-V2 original de 23/04 manhã** (14 OBS · origem de ALINHA-Descoberta-Camada-Produto). Declaração da Usuária: *"ficou quase 2 dias nisso · está tudo exatamente do mesmo jeito · quero crer que estamos rodando app_v2 em outra versão."*

**Investigação conduzida em chat (24/04 · tarde):**

1. **Leitura de `app_v2.py` (1357 linhas)** · confirma imports só da Fundação original:
   - Linha 30: `from exportacao import exportar_resultado`
   - **Zero** `from apresentacao import ...`
2. **Leitura de `_render_botao_download_excel` (linha 1177-1206)** · confirma chamada única:
   - Linha 1190: `exportar_resultado(v2, caminho)` · função do `exportacao.py` legado da Fundação (F-EXP · Fase 1)
3. **Comentários do próprio `app_v2.py` documentam a lacuna textualmente:**
   - Linha 953: *"Aplicação visual efetiva aguarda extensão de ConfigExportacao (candidato D-XXX)"*
   - Linhas 956-957: *"Config diagnóstico: 12 campos achatados esperados por capability 10. Disponível para consumo quando exportacao.py integrar a capability."*
4. **Leitura de `exportacao.py` legado (linhas 336-397)** · confirma hardcode técnico:
   - `_kv("Modo Upload", cab.modo_upload)` (literal técnico)
   - `for chave, valor in resumo.bloco_2_numeros_ancora.items(): _kv(chave, valor)` (despeja `total_origem`, `total_comparado`, `diferenca_total`, `variacao_total_pct` crus)
   - Zero chamada a `renderizar_resumo_executivo` (capability 7)
   - Zero chamada a `aplicar_formato_monetario` / `aplicar_formato_percentual` (capabilities 4/5)
   - Aba "Parâmetros" ainda criada separada da aba "Diagnóstico" (viola D-165)
5. **Pasta `/src/apresentacao/` existe no disco** (print de 24/04) · 11 arquivos · 10 capabilities implementadas em 23/04/2026 entre 17:55 e 21:39 · confirmado via `__init__.py` exporta API completa (`aplicar_paleta` · `traduzir` · `criar_tabela_executiva` · `aplicar_formato_monetario` · `aplicar_formato_percentual` · `montar_colunas_adaptativas` · `renderizar_resumo_executivo` · `aplicar_badge` · `aplicar_hierarquia_tipografica` · `renderizar_diagnostico`).

**Conclusão do diagnóstico:** F-APRESENT foi implementada corretamente no disco · 306 testes verdes · API exportada pelo `__init__.py` · MAS **nunca foi plugada no caminho de exportação do Excel**. O produto final ainda é gerado 100% pelo `exportacao.py` legado da Fundação (F-EXP · Fase 1 · pré-ALINHA-Descoberta-Camada-Produto). A Sessão 4 (A-V2 refatorada) preparou o app para **um dia** chamar F-APRESENT (ver `_enriquecer_config_usada_pos_pipeline`, linha 947) mas **nunca chamou**. A Sessão 4-bis (D-171 paleta em ConfigExportacao · D-172 router cap_diag) fez arranjos de interface que preparam a tubulação · **não ligam a água**.

**Decisão:** Formalizar como **débito estrutural crítico**. Escopo cirúrgico de resolução (Sessão 4-ter · próxima · sessão combinada Claude Code D-155):

**Entregáveis da Sessão 4-ter:**

1. **Novo `exportacao_v2.py`** em `/src/visoes/` · função `exportar_resultado_v2(v2_result, caminho, paleta_nome, configuracao)` · consome F-APRESENT integralmente:
   - Aba 1 · Resumo Executivo → `renderizar_resumo_executivo(ws, resumo, paleta, vocabulario)` (capability 7)
   - Aba 2 · Matriz de Confronto (Coração Visual V2) → preserva lógica existente de `exportacao.py` legado + `aplicar_titulo_aba` + `aplicar_secao` + `aplicar_badge` nas células de classificação
   - Aba 3 · Base Analítica → `criar_tabela_executiva(ws, range, "BaseAnalitica", totais_por_coluna, paleta_nome)` (capability 3) + `aplicar_formato_monetario`/`aplicar_formato_percentual`/`aplicar_formato_contagem` por coluna conforme contrato de unidade (capabilities 4/5) + `montar_colunas_adaptativas(config_usada, esquema_v2)` (capability 6) · esquema V2 declarado no arquivo
   - Aba 4 · Diagnóstico (ÚLTIMA · D-017 · absorve Parâmetros · D-165) → `renderizar_diagnostico(ws, config_usada, resolucao_estrutural, modelo_aplicado, t_diag, warnings, paleta, vocabulario)` (capability 10)
   - **Zero chamada** a `cap_resumo_executivo`, `_escrever_parametros`, `cap_diagnostico` do `exportacao.py` legado
   - Aplica `aplicar_paleta(wb, paleta)` (capability 1) no workbook antes de salvar
2. **`app_v2.py` · 3 mudanças mínimas:**
   - Linha 30: adicionar `from visoes.exportacao_v2 import exportar_resultado_v2`
   - Linha 1190: substituir `exportar_resultado(v2, caminho)` por `exportar_resultado_v2(v2, caminho, paleta_nome=st.session_state.get("paleta_selecionada", PALETA_DEFAULT))`
   - Remover/simplificar `_enriquecer_config_usada_pos_pipeline` (enriquecimento passa a ser feito dentro do `exportacao_v2` que monta o dict achatado via `_extrair_config_para_diagnostico` já existente no app_v2)
3. **Novo `test_exportacao_v2.py`** · testes de contrato fim-a-fim:
   - Teste 1 · nenhuma célula do Excel exportado contém termo proibido via `eh_termo_proibido` (varre todas as células de todas as abas)
   - Teste 2 · aba "Parâmetros" não existe no workbook exportado
   - Teste 3 · aba "Diagnóstico" existe e é a última
   - Teste 4 · células monetárias têm `number_format` contendo `"R$"` 
   - Teste 5 · células percentuais têm `number_format` contendo `"%"`
   - Teste 6 · workbook exportado tem atributo de paleta marcado via `paleta_aplicada(wb)`
   - Teste 7 · Base Analítica é uma `openpyxl.Table` com `totalsRowShown=True`
4. **Não modificar:** `exportacao.py` legado (preservado intacto para outras visões que ainda dependem dele · migração visão-a-visão) · `visao_v2.py` · `contratos.py` · F-APRESENT (intacta) · P-V2 · S-V2 (adendo §2.4 fica para DEPOIS de D-173 fechada).

**Critério de fechamento de D-173:**
1. `exportacao_v2.py` criado · `test_exportacao_v2.py` verde (7/7 novos + regressão zero nos existentes)
2. Usuária abre Excel exportado pelo app_v2 refatorado e confirma visualmente que:
   - Resumo Executivo está em prosa user-facing (sem chaves técnicas, sem JSON dump)
   - Valores monetários com `R$ 1.037.289,00`
   - Percentuais com `1,09%`
   - Classificações em rótulo amigável (sem `PRESENTE_AMBOS` em caps)
   - Aba Parâmetros ausente
   - Aba Diagnóstico em 6 seções fundidas

**Razão:**
1. **C.4** · débito estrutural que aparece como surpresa em VV exige formalização D-XXX.
2. **C.2** · nada silencioso · os comentários em app_v2 linhas 953/956-957 admitiam a lacuna · deveriam ter virado D-XXX em Sessão 4 · não viraram · formalização retroativa agora honra o princípio.
3. **Escopo cirúrgico** preserva trabalho correto (F-APRESENT isolada · motor V2 · app_v2 estrutura) · foca exclusivamente na **ponte** entre os dois.
4. **Novo arquivo `exportacao_v2.py` em `/src/visoes/`** em vez de modificar `exportacao.py` legado · evita regressão nas outras 10 visões que ainda dependem dele · migração será incremental (cada visão ganha seu `exportacao_vN.py` durante sua A-VN refatorada · `exportacao.py` vira legado aposentado quando todas migrarem).
5. **Testes de contrato fim-a-fim** eliminam a classe de bug descoberta hoje (capability isolada verde ≠ produto final correto) · garantem que o Excel exportado de fato consome F-APRESENT.

**Lição metodológica absorvida:**
- Testes de capability em isolamento verdes NÃO são proxy suficiente de "produto pronto para VV". Testes de contrato fim-a-fim no output real são necessários. Vigora para todas as A-VN futuras (V1 · V11 · V3 · ...).
- Sessões combinadas D-155 devem incluir, na retrospectiva, **abrir o Excel gerado** como item de checklist antes de declarar sessão concluída.

**Impacto:**
- Planilha Aba 1 · Próximo Passo Operacional → Sessão 4-ter
- Planilha Aba 2 · V2 permanece em `✅✅✅✅⚠️▶` · 6º quadrado só avança após Usuária validar Excel gerado pelo app_v2 refatorado
- VV-V2 retroativa original (aberta 24/04 tarde) pausada · retomada após D-173 fechada · OBS-01 · OBS-02 · OBS-03 · OBS-04 registradas mas não consolidadas em kit (aguardam VV-V2 retomada para re-validação no produto corrigido)
- ALINHA-Retroação-V2 (Marco) postergada até VV-V2 retroativa concluída pós-D-173
- `Instrucoes_do_Projeto.md` v3.2 · "O que NÃO fazer" · ganha item: *"Não declarar sessão A-VN concluída sem abrir o Excel gerado para inspeção visual. Testes verdes em capability isolada não substituem inspeção do produto final."*
- CONTEXT v3.2 · §15.9 (Retrospectivas pós-Claude Code · D-155) · ganha item: *"Em sessões A-VN a retrospectiva inclui obrigatoriamente abrir o Excel exportado pelo app_vN refatorado e validar visualmente que Resumo Executivo está em prosa user-facing, valores monetários e percentuais estão formatados, aba Parâmetros ausente, aba Diagnóstico em 6 seções. Sem esse passo, sessão não é concluída."*

**Referência canônica:** DECISIONS D-173 · CONTEXT §15.9 (atualização pendente) · spec_v2.md (será consumida pelo Claude Code) · `exportacao_v2.py` (será criado na Sessão 4-ter).

### D-172 — Adaptador `_extrair_config_para_diagnostico` em `app_v2.py` monta dict canônico de 12 campos para capability 10 · sem mudança em V2Result
**Data:** 2026-04-24 · **Bloco:** Sessão 4-bis (cleanup pós-A-V2 refatorada) · **Status:** Fechada

**Contexto:** Capability 10 de F-APRESENT (`renderizar_diagnostico` · D-165 · renderiza aba Diagnóstico em 6 seções fundidas) espera `config_usada` como dict **achatado** com 12 campos canônicos (arquivo · aba_consumida · modo_base · agrupadores · campo_analisado · tipo_medida · colunas_mapeadas · estados_nao_escolhidos · paleta_aplicada · thresholds_usados · defaults_sobrescritos · nulos_por_classificacao). Na implementação real da V2, esses campos vivem espalhados em múltiplos locais: alguns em `V2Result.config_usada` (dict da config original) · alguns em `V2Result.comparacao_realizada.*` (objeto Pydantic) · alguns em `V2Result.agrupadores_aplicados` · alguns vêm upstream do app (nome do arquivo, aba consumida) · alguns são ausentes no contrato atual (`nulos_por_classificacao` · `defaults_sobrescritos`). Descoberta explícita na Sessão 3 (F-APRESENT P1 · 23/04 noite): capability 10 é **genérica** · aceita dict OU Pydantic via `_get_cfg/_ler_campo` · trata ausência como `—` via `formatar_valor_ou_traco(None, origem)` com microcopy contextual.

**Três opções avaliadas:**

**Opção A · adicionar os 12 campos a `V2Result`** (contrato Pydantic). Contras: cria campos dummy para preencher o que o motor não produz (`nulos_por_classificacao`, `defaults_sobrescritos`) · viola C.3 (invenção de comportamento) · capability 10 deixaria de ser genérica · cada visão teria que estender `VNResult` com 12 campos.

**Opção B · estender capability 10** para conhecer a estrutura de cada `VNResult`. Contras: capability vira dependente de visão · quebra princípio de subsistema transversal (F-APRESENT).

**Opção C · adaptador na A-VN.** Cada `app_vN.py` cria função pequena `_extrair_config_para_diagnostico(vN_result, ...) -> dict` que monta o dict canônico achatado a partir dos múltiplos campos do `VNResult` + parâmetros upstream. Pros: capability 10 permanece genérica · zero mudança em contratos · cada visão decide como preencher campos ausentes (passa `None` · capability renderiza `—`). Contras: duplicação mínima entre visões (4-6 linhas de adaptador por visão).

**Decisão:** Opção C. Adaptador `_extrair_config_para_diagnostico` vive em `app_v2.py` (linhas 970-1016) · assinatura:

```python
def _extrair_config_para_diagnostico(
    v2_result: V2Result,
    paleta_selecionada: str,
    arquivo_nome: str,
    aba_consumida: str,
) -> Dict[str, Any]
```

Mapeamento implementado:
- Seção 1 (Como foi analisado): `arquivo` · `aba_consumida` · `modo_base` (de `config_usada["modo_pre_agregado"]`) · `agrupadores` · `campo_analisado` · `tipo_medida` · `colunas_mapeadas`
- Seção 4 (Decisões do usuário): `estados_nao_escolhidos`
- Seção 5 (Configurações avançadas aplicadas): `paleta_aplicada` · `thresholds_usados` · `defaults_sobrescritos=None` (motor não expõe · capability 10 renderiza `—`)
- Seção 6 (Qualidade estrutural): `nulos_por_classificacao=None` · `total_warnings` · `warnings_por_categoria` · `ajustes_aplicados`

Resultado injetado em `v2_result.config_usada["_config_diagnostico"]` pela função `_enriquecer_config_usada_pos_pipeline` (ver D-171).

**3 testes novos em `test_app_v2.py`:**
- `test_extrair_config_diagnostico_monta_12_chaves_canonicas`
- `test_extrair_config_diagnostico_trata_ausentes_como_None`
- `test_extrair_config_diagnostico_preserva_thresholds_como_dict`

**Razão:**
1. **C.3 · sem invenção.** Motor V2 não mede `nulos_por_classificacao` · não se inventa campo. Capability 10 renderiza `—` (Bloco 8 do vocabulario_bilingue v2).
2. **Separação de responsabilidades.** Capability 10 é transversal (consumida por 11 visões) · adaptador é específico (1 por visão) · cada visão conhece sua própria estrutura de `VNResult`.
3. **Sem mudança em contratos da Fundação.** `V2Result` intacto · 301/301 testes de V-V2 preservados.
4. **Precedente reutilizável.** V1, V11 e demais visões criam seus próprios adaptadores na A-VN correspondente. Documentar padrão em CONTEXT §15.12 (absorção pendente na ALINHA-Retroação-V2).

**Convenção canônica para A-VN futuras:**
Cada `app_vN.py` declara função `_extrair_config_para_diagnostico(vN_result, paleta_selecionada, ...) -> dict` retornando dict com **exatamente** as 12 chaves canônicas. Campos ausentes no contrato real da visão passam `None` · capability 10 trata via `formatar_valor_ou_traco`. Chamada obrigatória em `_enriquecer_config_usada_pos_pipeline` antes de qualquer exportação.

**Impacto:**
- `app_v2.py` · função `_extrair_config_para_diagnostico` (linhas 970-1016) · função `_enriquecer_config_usada_pos_pipeline` (linhas 947-967)
- `test_app_v2.py` · 3 testes novos
- CONTEXT §15.12 ganha nota "Adaptador A-VN específico" (absorção na ALINHA-Retroação-V2)
- Sem mudança em `contratos.py` · `visao_v2.py` · `/src/apresentacao/diagnostico_narrativo.py`

**Referência canônica:** DECISIONS D-172 · app_v2.py linhas 947-1016 · test_app_v2.py · CONTEXT §15.12 (convenção a absorver).

### D-171 — Paleta selecionada propaga via `v2_result.config_usada["paleta_aplicada"]` · sem mudança em ConfigExportacao
**Data:** 2026-04-24 · **Bloco:** Sessão 4-bis (cleanup pós-A-V2 refatorada) · **Status:** Provisória · refinada por D-173

**Contexto:** Sessão 4 (A-V2 refatorada · 24/04 madrugada) deixou lacuna documentada em comentário no código (linhas 947-953 de `app_v2.py`): *"Paleta: aba Parâmetros do Excel consome config_usada · valor registrado. Aplicação visual efetiva aguarda extensão de ConfigExportacao (candidato D-XXX)."* A Sessão 4-bis (24/04 madrugada · mesma sessão combinada) precisou destravar a Sessão 5 (VV-V2) decidindo como a paleta selecionada pela Usuária no sidebar chega até o Excel exportado.

**Duas opções avaliadas:**

**Opção A · estender `ConfigExportacao`** (contrato Pydantic da Fundação) · adicionar campo `paleta_nome: NomePaleta = "azul"` · `exportacao.py` legado passa a consumir `config.paleta_nome`. Pros: contratualmente limpo · campo tipado. Contras: muda contrato de Fundação · afeta todas as 11 visões · exige migração em série · quebra princípio de "V2 retroativa é escopo cirúrgico" (D-167).

**Opção B · usar `v2_result.config_usada["paleta_aplicada"]`** (dict mutável · já existente · sem tipagem) · `app_v2.py` injeta via função `_enriquecer_config_usada_pos_pipeline` depois de `executar_v2` · exportação lê via `v2_result.config_usada.get("paleta_aplicada")`. Pros: zero mudança em contratos · escopo cirúrgico preservado · reversível (D-XXX de evolução pode promover para ConfigExportacao depois). Contras: paleta fica em `Dict[str, Any]` · não tipada · invisível em mypy estrito.

**Decisão:** Opção B. Paleta propaga via dicionário `v2_result.config_usada["paleta_aplicada"]` até a fase V2-retroativa estar fechada. Tipagem forte em `ConfigExportacao` fica parqueada como refinamento futuro (candidato a "D-XXX-Evo · Tipagem de paleta em ConfigExportacao" · só quando mais de 1 visão consumir o caminho · provavelmente pós-V1 ou pós-V11).

**Implementação na Sessão 4-bis:**
- `app_v2.py` linha 947-967 · função `_enriquecer_config_usada_pos_pipeline(v2_result)` chamada logo depois de `executar_v2` bem-sucedido (linha 939)
- Injeta 2 campos em `config_usada`:
  - `"paleta_aplicada"` · valor do `st.session_state["paleta_selecionada"]` (default "Azul")
  - `"_config_diagnostico"` · dict achatado de 12 campos canônicos para capability 10 (ver D-172)
- 3 testes novos em `test_app_v2.py`:
  - `test_enriquecimento_injeta_paleta_default` (sem seleção · injeta "Azul")
  - `test_enriquecimento_preserva_paleta_selecionada` (com seleção · injeta o selecionado)
  - `test_enriquecimento_so_opera_quando_sem_bloqueios` (bloqueio ativo · não enriquece)

**Razão:**
1. **C.3 sem invenção de comportamento** · a estrutura `config_usada` já existia e já era mutável · não inventa ponto de extensão.
2. **Escopo cirúrgico de D-167** · V2 retroativa não deve mexer em contratos da Fundação.
3. **Reversibilidade.** Provisória · promoção a ConfigExportacao tipada continua aberta como evolução.
4. **Desacoplamento de F-APRESENT.** As capabilities 1/3/7/10 recebem `paleta: Paleta` como parâmetro explícito · `obter_paleta(nome)` resolve o nome para instância · não consome `ConfigExportacao`. Logo, tipagem em `ConfigExportacao` não é pré-requisito para F-APRESENT funcionar.

**Refinada por D-173:** A função `exportar_resultado_v2` (criada na Sessão 4-ter · D-173) lerá `paleta_nome` como **parâmetro explícito da chamada** (`exportar_resultado_v2(v2, caminho, paleta_nome=...)`), não via `config_usada`. O campo `config_usada["paleta_aplicada"]` permanece como registro de auditoria (aba Diagnóstico · seção 5 · capability 10) · mas o caminho de renderização do Excel usa parâmetro tipado. Razão: chamada tipada > dicionário estendido quando há oportunidade de tipar na fronteira nova.

**Impacto:**
- `app_v2.py` · função `_enriquecer_config_usada_pos_pipeline` (linhas 947-967)
- `test_app_v2.py` · 3 testes novos
- Sem mudança em `contratos.py` · `motor_base.py` · `exportacao.py` legado · `/src/apresentacao/`
- Refinamento D-173 · parâmetro explícito em `exportar_resultado_v2` (Sessão 4-ter)

**Referência canônica:** DECISIONS D-171 · app_v2.py linhas 947-967 · test_app_v2.py · refinada por D-173.

D-170 — REVISADA · Método otimizado de kits · Provisória → FECHADA · 3 aplicações consolidadas
Data original: 2026-04-24 · Data de revisão: 2026-04-24 (final) · Bloco: Sessão 4 + 4-ter + 4-ter-bis · Status: FECHADA

NOTA DE REVISÃO: D-170 estava marcada como Provisória · revisão prevista para ALINHA-Retroação-V2. ALINHA-Retroação-V2 fechou nesta sessão (D-184) com 3 aplicações de D-170 consolidadas (Sessão 4 + 4-ter + 4-ter-bis com kits leves · ALINHA atual com kit pesado). Promovida para Fechada sem alterações estruturais. Texto original preservado abaixo, atualizado apenas no campo Status e na nota final de aplicação histórica.

Contexto: Durante produção do kit de encerramento da Sessão 4 (A-V2 refatorada · 24/04 madrugada) emergiu tensão entre o ritmo canônico de D-033 (kit completo a cada sessão: CONTEXT + Instruções + GLOSSARIO + DECISIONS + planilha + artefatos) e o ritmo real de uma fila de 5 sessões consecutivas para fechar V2 retroativa. Aplicação integral de D-033 a cada sessão produziria 5 atualizações sucessivas de CONTEXT (v3.2 → v3.3 → v3.4 → v3.5 → v3.6) em 48h · com conteúdo decisional pequeno por sessão intermediária · carga operacional alta sobre a Usuária para Ctrl-C/Ctrl-V de arquivos que mudariam pouco.
Decisão: Em filas de sessões intermediárias (não-Marco · não-ALINHA), aplicar método otimizado de kit:
Kit leve (sessões intermediárias da fila):

Categoria 1 (arquivos para download): apenas artefatos produzidos na sessão (ex: spec nova · wireframe · código novo via Claude Code). Não inclui CONTEXT · Instruções · GLOSSARIO · planilha completa.
Categoria 2 (aplicadas pela Usuária): apenas edições rotineiras da planilha (aba 1 e aba 2 · texto pronto para colar em células específicas) + entradas D-XXX para DECISIONS.md (texto pronto para colar no topo).
Prompt de abertura da próxima conversa inline como sempre.

Kit pesado (apenas em Marco · sub-bloco δ da ALINHA):

Categoria 1: CONTEXT + Instruções + GLOSSARIO + planilha completa + todos os artefatos acumulados · versionados.
Categoria 2: DECISIONS consolidado com todas as D-XXX da fila formalizadas · instruções de edição completas.
Prompt dual · modo operacional seguinte + retrospectiva futura.

Regra de consolidação: todas as D-XXX que emergem em kits leves ficam provisionadas no DECISIONS.md desde a sessão onde emergiram (não ficam silenciosas · C.2 preservado) · mas CONTEXT e Instruções só absorvem no kit pesado seguinte.
Como o Arquiteto decide qual kit usar:

Sessão encerra Marco? → kit pesado (ALINHA · sub-bloco δ · D-142).
Sessão é intermediária dentro de fila declarada (ex: fila de 5 sessões para fechar V2 retroativa · ver D-167)? → kit leve.
Sessão é única e autossuficiente (ex: refino de 1 DCV · 1 decisão isolada)? → kit completo (padrão D-033 original).

Razão:

Ergonomia real da Usuária. Cada substituição de arquivo no painel do Projects é operação manual · 5 em 48h viola princípio 4 de D-131 ("Usuária não lê código · não opera documentação como ritual").
Preservação de C.2. D-XXX vão para DECISIONS a cada sessão · não ficam silenciosas. O que muda é apenas quando CONTEXT/Instruções absorvem · e essa absorção vem com consolidação retrospectiva (α da ALINHA) que produz narrativa mais coerente do que 5 updates incrementais.
Alinhamento com D-142. ALINHA já era o momento canônico de consolidação em Marcos. D-170 formaliza que kits leves são o comportamento normal entre ALINHAs · kit pesado é o comportamento normal em ALINHAs.
Reversibilidade preservada (no original). Era classificada como Provisória · revisão formal em ALINHA-Retroação-V2 (α · retrospectiva). Promovida para Fechada nesta ALINHA com 3 aplicações empíricas validadas.

Impacto:

Instrucoes_do_Projeto.md v3.3 "Ritual de encerramento" ganha subseção "Kit leve vs kit pesado" (absorvida nesta ALINHA-Retroação-V2)
CONTEXT §11 adiciona referência a D-170 (absorvida nesta ALINHA-Retroação-V2)
Sessões 2 (Adendo §2.4 a S-V2), 3 (F-APRESENT P1), 4 (A-V2 refatorada), 4-bis (cleanup D-171/D-172), 4-ter (V2 retroativa F-APRESENT), 4-ter-bis (correções camada 2) operaram em kit leve · kit pesado consolidado nesta ALINHA-Retroação-V2 (sub-bloco δ)
Nenhuma mudança em código

Aplicação histórica consolidada (3 aplicações de kit leve + 1 kit pesado · validação completa):

1ª aplicação: kit da Sessão 4 (A-V2 refatorada · 24/04 madrugada · sem nome formal na época)
2ª aplicação: Sessão 4-bis (mesma madrugada)
3ª aplicação: Sessão 5 (VV-V2 retroativa) · interrompida por descoberta de D-173 · seguida por Sessão 4-ter, 4-ter-bis (24/04)
Kit pesado δ: este kit ALINHA-Retroação-V2

Referência canônica: DECISIONS D-170 (FECHADA) · Instrucoes_do_Projeto v3.3 (absorvida) · CONTEXT §11 (absorvida) · D-184 (ALINHA-Retroação-V2 que consolidou).

### D-169 — Débito técnico formalizado · 13 testes P0 de F-APRESENT em vermelho por drift v1→v2 do vocabulário
**Data:** 2026-04-23 · **Bloco:** Kit de encerramento Sessão 3 V2 retroativa (F-APRESENT P1) · **Status:** Aberta · vencimento na Sessão 4 ou sessão dedicada antes

**Contexto:** Retorno do Claude Code da Sessão 3 (F-APRESENT P1) revelou que o baseline anterior NÃO era 480/480 verdes como declarado no kit de P-V2 retroativo (D-168). Era 467/480 · com 13 testes em `test_apresentacao.py` (P0) já em vermelho desde a evolução do `vocabulario_bilingue.md` v1→v2 consolidada em P-V2 retroativo (D-167). Causas: (1) stepper passou de 5 para 7 entradas · (2) `tipos_campo` passou de 5 para 6 entradas · (3) strings de classificação mudaram (ex: "Apareceu no Comparado" no lugar de "Ausente na origem"). Asserts hardcoded em testes P0 ainda batem em valores v1 · falhas determinísticas. O kit de P-V2 retroativo não sinalizou esses 13 testes em vermelho · violação retroativa de C.2 (nada silencioso) sobre estado da suite.

**Decisão:** Formalizar como **dívida técnica** com vencimento explícito. Atualização dos 13 testes P0 para refletir vocabulário v2 entra como sub-bloco da Sessão 4 (A-V2 refatorada) OU sessão dedicada curta antes da Sessão 4. Não fica em aberto silenciosamente.

**Critério de fechamento de D-169:**
1. Os 13 testes em `test_apresentacao.py` atualizados para asserts compatíveis com `vocabulario_bilingue.md` v2
2. Suite reporta 607/607 verdes (ou número equivalente após eventuais novos testes)
3. Kit de encerramento da sessão que fechar D-169 declara explicitamente o número de testes verdes corrigido

**Razão:** (1) C.2 exige que dívida não desapareça silenciosamente · formalizar como D-XXX é o mecanismo canônico (C.4). (2) 13 testes em vermelho não são regressão da Sessão 3 · não bloqueiam fechamento dela · mas precisam de vencimento explícito. (3) Atualização é mecânica · não é decisão estrutural · cabe naturalmente em sessão Claude Code futura. (4) Kit anterior (D-168 · P-V2 retroativo) deveria ter rodado `pytest` ANTES de declarar 480/480 · processo de validação do kit ganha lição: rodar suite completa antes de declarar baseline.

**Lição metodológica:** Em todos os kits futuros que declararem número de testes verdes, validar com `pytest` ANTES de produzir o kit. Não confiar no número da última sessão sem revalidação. Esta lição vigora para todos os kits a partir de agora · está incorporada em `Instrucoes_do_Projeto.md` v3.2 (seção "Ritual de encerramento de conversa").

**Impacto:**
- CONTEXT v3.2 · §6.2 · nota explícita sobre 594/607 verdes + débito D-169 declarado
- Instrucoes_do_Projeto.md v3.2 · "O que NÃO fazer" · ganha "Não declarar baseline de testes em kit sem rodar pytest completo antes"
- Sessão 4 · sub-bloco curto de cleanup OU sessão dedicada antes
- Sem mudança em código de produção

**Referência canônica:** Output completo do Claude Code da Sessão 3 (`Failed: 13 (pré-existentes · não regressão)`) · DECISIONS D-169 · vencimento na Sessão 4.

### D-168 — Paleta Azul executivo como default universal das 11 visões · supera D-164
**Data:** 2026-04-23 · **Bloco:** P-V2 retroativo (sessão única) · **Status:** Fechada · Supera D-164 parcialmente

**Contexto:** D-164 (ALINHA-Descoberta-Camada-Produto · 23/04/2026 manhã) declarou catálogo de 4 paletas executivas com defaults semânticos por visão (Cinza para V1/V11/V2 · Verde para crescimento · Vinho para desvio). Durante a Decisão 1 da sessão de P-V2 retroativo (23/04/2026 noite), Usuária declarou: "sugiro mantermos o azul como default em todas as visões, mas sempre com a opção do usuário escolher qual que ele prefere · nas opções de check vem primeiro o azul corporativo, cinza, verde e o vinho na ordem".

**Decisão:** Paleta **Azul executivo** passa a ser default universal para todas as 11 visões. Ordem fixa do widget de seleção: **Azul · Cinza · Verde · Vinho** (sem microcopy semântica · só nomes). Sobrescrição pelo usuário preservada via C.D6 (DDU · D-161). Cada P-VN apenas declara "default Azul" na Seção 1, sem precisar justificar paleta semântica por visão.

**Razão:** (1) Reduz carga cognitiva nas P-VNs (uma decisão a menos por visão). (2) Garante consistência visual cross-visão para clientes que usam múltiplas visões. (3) Azul institucional não pré-julga leitura (V2 produz tanto leituras positivas quanto negativas). (4) Decisão da Usuária preserva autoridade sobre camada de produto (B.4 · P-VN é fonte autoritativa de paleta). (5) C.D6 preservado integralmente · usuário escolhe se quiser.

**O que D-164 preserva:**
- Catálogo canônico de 4 paletas · mantido integralmente
- F-APRESENT capability 1 como implementador técnico · mantida
- Aplicação em cabeçalhos · badges · linhas alternadas · totais · bordas · destaques · mantida
- 4 amostras visuais aprovadas em 23/04/2026 manhã · continuam válidas

**O que D-164 supera:**
- Defaults semânticos por visão (Cinza para V1/V11/V2 · Verde · Vinho) · substituído por Azul universal
- Cada P-VN não precisa mais justificar paleta default

**Impacto:**
- P-V2 retroativo Seção 1.1 · Azul declarado como default
- CONTEXT §15.11 (convenções P-VN · Seção 1) · atualizar para refletir default universal
- F-APRESENT capability 1 sem mudança de código (Azul já está no catálogo · só muda o default declarado)
- P-V1 · P-V11 · todas as P-VNs futuras: declaração simplificada de paleta na Seção 1

**Referência canônica:** P-V2 retroativo Seção 1.1 · DECISIONS D-168 · supera D-164 (parcialmente).

---
### D-167 — Antecipação de ALINHA-Retroação-V2 em escopo cirúrgico · V2 retroativo antes de V1/V11
**Data:** 2026-04-23 · **Bloco:** Kit de encerramento de F-APRESENT P0 · **Status:** Fechada

**Contexto:** Durante produção do kit de encerramento de F-APRESENT P0 (23/04/2026 · fim da tarde) · Arquiteto havia assumido P-V1 como próximo bloco operacional com base na ordem declarada em CONTEXT §3 ("V2 → V1 → V11") e nos critérios de ativação de ALINHA-Retroação-V2 declarados em D-162 ("V1 aprovada em VVC · V11 aprovada em VVC · Família A completa sob método novo"). Usuária corrigiu: "estamos no ciclo da V2 · o print Rm × Protheus que mandei é referência da próxima visão (V1) mas estamos em V2 · todo ciclo antigo foi em cima de V2 · e de lá que nasceu ALINHA-Descoberta-Camada-Produto". Declaração de indiferença pela ordem ("por mim tanto faz começar pela V1 ou pela V2") abriu espaço para decisão metodológica.

**Decisão:** Antecipar formalmente ALINHA-Retroação-V2. P-V2 retroativo é a primeira aplicação do ciclo de 6 artefatos (D-158). V1 e V11 ficam para depois.

**Escopo cirúrgico aprovado pela Usuária:**

| Artefato | Ação | Racional |
|---|---|---|
| P-V2 retroativo | **Produzir novo** · 5 seções canônicas (§15.11) | Artefato ausente no ciclo antigo · exigido pelo método novo |
| S-V2 existente | **Preservar** · adicionar adendo de contrato de unidade por campo (D-166 · seção nova §2.4) + notas D-165/D-166 nas seções afetadas | Spec técnica está correta · só faltam refinamentos de D-166/D-165 absorvidos como evolução |
| B-V2 | **Preservar** · `base_fundacao.xlsx` continua servindo (D-147) | Base mestre cobre V2 adequadamente · dispensado conforme critério D-147 |
| V-V2 (motor) | **Preservar integralmente** · 301/301 testes verdes mantidos | Motor está correto · descoberta de ALINHA foi de camada de produto · não de motor |
| A-V2 | **Refatorar** · consumir P-V2 · integrar F-APRESENT P0 (capabilities 1-7) · separar download de aprovação (D-162) | App atual apresenta os defeitos de vocabulário/dump documentados nas 14 OBS de VV-V2 |
| VV-V2 | **Executar nova** · modalidade C mista (D-156) · operar em VVC (D-162) · checklist derivado regenerado do YAML | Validação sob método novo · sobre produto executivo de verdade · fecha gate B.4 camada 1 |

Nome convencional: **"P-V2 retroativo"** / **"A-V2 retroativo"** / **"VV-V2 retroativo"** · preserva memória histórica de que essa V2 já teve ciclo antigo (C.2 · nada silencioso).

**Razão:** (1) Continuidade metodológica natural · toda descoberta de ALINHA-Descoberta-Camada-Produto nasceu sobre V2 · aplicar método novo nela fecha o ciclo da descoberta · V2 vira a prova real de que método funciona. (2) V2 é a dívida técnica mais nítida do projeto (`✅✅✅✅⚠️⬜`) · fechar primeiro limpa a mesa antes de avançar. (3) V2 é analiticamente mais simples que V1 · primeira aplicação de método novo se beneficia de ir na visão de menor complexidade antes de testar em visão com matching + ambiguidade + duplicidade. (4) Escopo cirúrgico preserva trabalho correto da V2 original (motor · 301 testes · base) e foca onde a descoberta de ALINHA exige mudança · honra C.3 (sem invenção de comportamento onde está correto). (5) Usuária declarou indiferença pela ordem · decisão metodológica é do Arquiteto com aprovação explícita.

**Critérios originais de ALINHA-Retroação-V2 (D-162) · superados:** *V1 aprovada em VVC · V11 aprovada em VVC · Família A completa sob método novo.* Esses critérios foram declarados antes de F-APRESENT P0 existir · assumiam que V2 aguardaria calibração do método novo em visões mais recentes. Com F-APRESENT P0 concluído e calibrado (3 correções emergentes absorvidas) · a ordem natural se inverte · V2 retroativa abre o ciclo novo.

**Impacto:**
- CONTEXT §3 atualiza ordem Família A para "V2 retroativo → V1 → V11" + nota explicativa
- CONTEXT §9 B.4 critérios de ativação de ALINHA-Retroação-V2 marcados como "originais D-162 · superados por D-167"
- CONTEXT cabeçalho · "Próximo bloco operacional" passa para P-V2 retroativo
- Planilha aba 1 · "Próximo Passo Operacional" atualizado
- Planilha aba 2 · V2 permanece em `✅✅✅✅⚠️⬜` · 6º quadrado passa a "▶ Próximo" efetivamente · V1 e V11 não são mais "Próximo" imediato
- GLOSSARIO ganha verbete "Retroação de visão" (ou refina "ALINHA-Retroação-V2") · opcional nesta sessão · obrigatório se P-V2 retroativo consolidar convenção

**Referência canônica:** CONTEXT §3 · §9 B.4 · DECISIONS D-167 · D-162 (precedente superado).

### D-166 — Excel interativo · tabela nativa + totais dinâmicos + colunas adaptativas + formatação monetária/percentual + contrato de unidade
**Data:** 2026-04-23 · **Bloco:** ALINHA-Descoberta-Camada-Produto · **Status:** Fechada Adendo aplicado integralmente.

**Contexto:** DEC-04 de VV-V2 + OBS-11 + OBS-12. Declaração da Usuária: *"Usuário não vai digitar fórmula · filtrou, tem que somar embaixo automaticamente"*. Conjunto de defeitos identificados em `base_v2_simulacao.xlsx` processada: autofiltro sem tabela formatada (perde totais dinâmicos) · colunas fixas em vez de adaptativas (`estado_origem` e `estado_comparado` vazias em POR_COLUNAS · OBS-11g) · moeda sem formato BR · percentual exibido em fração decimal 9 casas (OBS-11e · OBS-12d).

**Decisão:** Toda aba tabular do Excel executivo implementa **4 requisitos combinados**:

**Requisito 1 · Tabela Excel nativa com totais dinâmicos** (F-APRESENT capability 3) — `openpyxl.worksheet.table.Table` (ListObject) · `totalsRowShown=True` · função de total por coluna declarada em P-VN (sum · average · count · custom · none) · usuário filtra · totais recalculam nativamente.

**Requisito 2 · Colunas adaptativas ao cenário** (F-APRESENT capability 6) — estrutura montada dinamicamente pelo `exportacao.py` conforme `V{N}Result.config_usada`. V2: POR_COLUNAS omite `estado_origem`/`estado_comparado` · POR_LINHAS inclui. Coluna constante nula não aparece · exceção exige justificativa em P-VN.

**Requisito 3 · Formatação monetária BR e percentual** (F-APRESENT capabilities 4 e 5) — Monetária: `"R$ #,##0.00;[Red](R$ #,##0.00);-"` · Percentual: `"0.00%;[Red]-0.00%;-"` · conversão fração→percentual na exportação · aplicação via `cell.number_format` por coluna declarada em P-VN.

**Requisito 4 · Contrato de unidade declarado por campo** — cada campo exportado tem **unidade declarada** em P-VN seção 3: monetário · percentual · contagem · texto · data · classificação · booleano. Ausência de declaração = bug de P-VN. V2 Spec atual não tem contrato de unidade (§2.4 ausente · OBS-12c) · aplicação em ALINHA-Retroação-V2 · Specs V1/V11 declaram desde início.

Escopo transversal: 11 visões consomem · F-APRESENT capabilities 3/4/5/6 implementam primitivas · P-VN seção 3 declara aplicação por visão.

**Razão:** (1) Declaração da Usuária é clara · totais dinâmicos são requisito de produto · não opção. (2) Colunas vazias (OBS-11g) são manifestação de ausência de adaptatividade · fix estrutural não cosmético. (3) Fração decimal como percentual é bug de formatação · requisito 3 fecha. (4) Contrato de unidade elimina classe inteira de bugs futuros (qualquer campo novo obriga declaração · C.2 nada silencioso aplicado). (5) 4 requisitos são independentes mas reforçam-se mutuamente · cobrem 100% dos defeitos de OBS-11 e OBS-12.

**Impacto:**
- F-APRESENT capabilities 3/4/5/6 especificadas (D-159 declara · D-166 detalha)
- P-VN seção 3 obriga: contrato de unidade + função de total por coluna + colunas adaptativas declaradas
- spec_v2.md §2.4 recebe nota D-166 (aplicação em ALINHA-Retroação-V2)
- Specs V1/V11 declaram contrato de unidade desde início
- Instruções v3 "O que NÃO fazer" ganha "exportar campo sem unidade declarada em P-VN"

**Referência canônica:** F-APRESENT capabilities 3/4/5/6 · P-VN seção 3 · CONTEXT §13.7 · DECISIONS D-166.

---

### D-165 — Fusão Parâmetros+Diagnóstico em aba única "Diagnóstico" · 6 seções user-facing
**Data:** 2026-04-23 · **Bloco:** ALINHA-Descoberta-Camada-Produto · **Status:** Fechada Aplicado em §2.9 reescrita.

**Contexto:** DEC-03 de VV-V2 + OBS-14. Spec V2 §2.9 declara 5 abas com Parâmetros (aba 4) e Diagnóstico (aba 5) separadas. Parâmetros aparece como Python dict serializado em string única truncada (OBS-10c) · vocabulário técnico puro. Diagnóstico atual já prova que `exportacao.py` tem capability narrativa (seções · mensagens user-facing · títulos em português · OBS-14 observação metodológica) · só não foi aplicada uniformemente.

**Decisão:** Estrutura canônica da aba Diagnóstico do Excel executivo passa a ser **1 aba única** com 6 seções fixas em ordem:

| # | Seção | Conteúdo |
|---|---|---|
| 1 | Como foi analisado | Arquivo · aba consumida · estrutura (user-facing) · colunas mapeadas · modo da base detectado · agrupadores · campo analisado · tipo de medida |
| 2 | Ajustes do motor | T-DIAG · AJUSTE_LEVE aplicados · consolidações · warnings de qualidade estrutural |
| 3 | Pontos de atenção | Warnings catalogados · classificação · contagens · exemplos · ação recomendada |
| 4 | Decisões do usuário | DECISAO_USUARIO · resolução estrutural · modelo escolhido · estados Modo 4 |
| 5 | Configurações avançadas aplicadas | TED · thresholds efetivamente usados · defaults vs sobrescrições · paleta selecionada |
| 6 | Qualidade estrutural | Base Analítica + resumo · total_warnings · nulos por classificação · nulos por agrupador · tempo por etapa (user-facing) |

**Aplicação transversal:** estrutura canônica para **todas as 11 visões**. Vive como capability 10 de F-APRESENT (D-159 · Diagnóstico narrativo). P-VN referencia · pode adicionar seção 7+ se visão exigir (justificado) · não pode remover 1-6.

Consequências estruturais: Spec V2 §2.9 · 5 abas passa a 4 abas (Resumo Executivo · Coração Visual · Base Analítica · Diagnóstico) · aplicação efetiva em ALINHA-Retroação-V2. Specs V1/V11 declaram 4 abas desde início. `exportacao.py` capability 10 gera aba única consumindo `config_usada` + `resolucao_estrutural` + `modelo_aplicado` + `T-DIAG` + warnings + BAD. Diagnóstico continua sendo **última aba** (D-017 preservado).

**Razão:** (1) Usuária declarou · estrutura proposta coerente. (2) 6 seções cobrem exatamente o que antes ficava espalhado em Parâmetros (JSON cru) + Diagnóstico (narrativo parcial). (3) Aplicação transversal a 11 visões honra C.2 (nada silencioso · todas as visões entregam diagnóstico completo e legível). (4) D-017 preservado. (5) Capability narrativa já existente prova viabilidade técnica · F-APRESENT generaliza.

**Impacto:**
- spec_v2.md §2.9 recebe nota D-165 (aplicação em ALINHA-Retroação-V2)
- CONTEXT §13.5/§13.6/§13.7 atualiza arquitetura de abas canônica
- F-APRESENT capability 10 (D-159) ganha especificação das 6 seções
- P-VN seção 3 (arquitetura de abas) declara aba Diagnóstico com 6 seções como invariante
- GLOSSARIO atualiza verbete "Diagnóstico" com 6 seções fixas

**Referência canônica:** CONTEXT §13 · F-APRESENT capability 10 · P-VN seção 3 · spec_v2.md §2.9 (nota D-165).

---

### D-164 — 4 paletas executivas canônicas · catálogo e seleção por visão
**Data:** 2026-04-23 · **Bloco:** ALINHA-Descoberta-Camada-Produto · **Status:** Fechada

**Contexto:** DEC-02 de VV-V2 declarou 4 paletas executivas selecionáveis · 3 nomeadas (Azul · Verde · Cinza) · 4ª em aberto. A5 da Onda 2 do ALINHA fechou 4ª = Vinho executivo (análise de lacuna semântica: Azul/Verde/Cinza ficam no "confortável" · Vinho traz peso sem drama · cobertura cultural em relatórios anuais corporativos brasileiros · diferenciação cromática nítida das outras 3).

**Decisão:** Catálogo canônico de 4 paletas executivas vive em F-APRESENT como capability 1 (D-159). Cada P-VN declara paleta **padrão** da visão em Seção 1 · Usuária pode sobrescrever no momento da exportação no app (aplicação de C.D6 · D-161). Paleta selecionada é metadado do Excel gerado · registrado em aba Diagnóstico seção 5.

**Catálogo canônico:**

| # | Nome | Semântica | Uso sugerido |
|---|---|---|---|
| 1 | Azul executivo | Institucional padrão · confiável · neutro-positivo | Default universal · análises descritivas sem viés |
| 2 | Verde executivo | Crescimento · positivo · progresso | Visões com leitura predominantemente positiva (V3 · V4 em contextos de crescimento) |
| 3 | Cinza executivo | Sóbrio · auditoria · fechamento | Visões de controle e conformidade (V2 · V8 · V1) |
| 4 | Vinho executivo | Peso executivo · atenção sem alarmismo | Visões de desvio e dispersão (V5 · V6 · V9) |

**Defaults por visão (declarados em P-VN · primeira aplicação V1):**
- Default V1 · Cinza executivo (conciliação = auditoria)
- Default V11 · Cinza executivo (conciliação por aderência = auditoria)
- Default V2 (retroação) · Cinza executivo
- Defaults demais visões · declarados em P-VN correspondente

**Regra de implementação:** F-APRESENT capability 1 exporta 4 paletas como assets consumíveis pelo `exportacao.py` · seleção no app é widget radio (4 opções · paleta padrão pré-selecionada · aplica C.D6) · paleta selecionada aplicada em cabeçalhos · badges · linhas alternadas · totais · bordas · destaques. Tipografia da paleta (hierarquia) incluída no catálogo.

**Razão:** (1) Catálogo fechado em 4 · não infinito · mantém consistência visual. (2) Default por visão respeita C.D6 e aplica semântica correta por natureza analítica. (3) Cinza como default de V1/V11/V2 · natureza de conciliação/comparação pede sobriedade. (4) Vinho para desvio/dispersão · peso semântico correto. (5) Implementação fora de F-APRESENT capability 1 é anti-C.2 (divergência silenciosa entre visões).

**Impacto:**
- F-APRESENT seção "Catálogo de paletas" · código em `/src/apresentacao/paletas.py`
- P-VN seção 1 (paleta default + sobrescrição)
- app_vN ganha widget de seleção
- aba Diagnóstico seção 5 registra paleta
- GLOSSARIO verbete "Paleta executiva" com 4 entradas

**Referência canônica:** F-APRESENT capability 1 · P-VN seção 1 · DECISIONS D-164.

---

### D-163 — Excel é o produto · declaração estrutural de produto
**Data:** 2026-04-23 · **Bloco:** ALINHA-Descoberta-Camada-Produto · **Status:** Fechada

**Contexto:** DEC-01 de VV-V2. Declaração estrutural da Usuária durante a sessão: *"Excel é o produto · cliente recebe, apresenta, decide a partir dele · tem que encantar · senão ele faz na mão · e o TabloFlow morre"*. Até esta sessão · Excel tratado implicitamente como "entregável" ou "output" · manifestação C das 14 OBS de VV-V2 (Excel como dump estruturado não como produto · OBS-10/11/12/13/14).

**Decisão:** Excel gerado pelo `exportacao.py` (e por F-APRESENT após D-159) é **o produto principal** do TabloAnálise · não entregável · não output · não saída técnica. Cliente recebe, apresenta em reunião, decide a partir dele, compartilha com stakeholders. A app Streamlit é **instrumento de configuração e preparação do Excel** · não é o produto entregue.

**Consequências estruturais imediatas:**
1. Qualidade do Excel é critério primário de sucesso do TabloFlow · não derivado
2. F-APRESENT (D-159) é subsistema-produto · não subsistema técnico · nasce para servir DEC-01
3. P-VN (D-158) dedica seção inteira à narrativa e arquitetura do Excel · não do app
4. Validação Visual (VVC+VVP · D-162) valida majoritariamente o Excel · app é secundário
5. Vocabulário bilingue (D-160) aplica-se com peso máximo no Excel · app pode ter exposição técnica controlada (Usuária construtora)
6. Paletas executivas (D-164) são aplicadas ao Excel primariamente · app herda coerência mas não replica exigências

**Posicionamento na arquitetura:**
- **Módulo 1 · TabloAnálise** · produto entregue = Excel executivo gerado por visão
- **App Streamlit** · configurador · garante Excel sai correto e personalizado
- **Motor** · garante números no Excel estão certos
- **Fundação** · garante infraestrutura transversal (incluindo F-APRESENT para Excel encantar)

**Razão:** (1) Declaração da Usuária é constitutiva · reorienta prioridade de toda camada seguinte. (2) Sem essa declaração · F-APRESENT ficaria subespecificado · P-VN idem. (3) Alinha com realidade de operação de cliente executivo · Excel vai para reunião · app fica no operacional. (4) Critério de sobrevivência do produto ("senão faz na mão · TabloFlow morre") elevado à regra de método.

**Impacto:**
- CONTEXT §1 ganha §1.1 "Excel executivo é o produto"
- CONTEXT §13 ganha padrão 13.7 "Excel executivo é produto"
- GLOSSARIO verbete "Excel executivo"
- Instruções v3 "O que NÃO fazer" ganha "tratar Excel como output técnico"

**Referência canônica:** CONTEXT §1.1 · §13.7 · DECISIONS D-163.

---

### D-162 — B.4 desdobrado em 2 camadas · Validação Visual Construtora + Validação Visual de Produto
**Data:** 2026-04-23 · **Bloco:** ALINHA-Descoberta-Camada-Produto · **Status:** Fechada

**Contexto:** DEC-10 de VV-V2 · manifestação D das 14 OBS (OBS-08 · OBS-09). Princípio B.4 tal como enunciado assume usuário que lê vocabulário técnico · checklist derivado literal do YAML é inexequível por cliente real (itens tipo *"O warning W-V2-AUSENTE-EM-UM-LADO aparece no Diagnóstico com 3-4 ocorrência(s)?"*) · gate B.4 mistura "avançar no fluxo" com "aprovar visão" (OBS-09 · app trata "4 ✅ marcados" = "visão aprovada" = "Excel libera" · essas três coisas não são equivalentes).

**Decisão:** Princípio B.4 desdobra-se em 2 camadas sequenciais com papéis distintos · cada camada tem seu próprio gate · não são substitutas.

**Camada 1 · Validação Visual Construtora (VVC):**
- Quem opera: Usuária construtora (Elaine · operação solo atual)
- Quando: dentro do ciclo de 6 artefatos · VV-VN conforme D-156 reformulado
- Base: `base_vN_cliente.xlsx` (sintética · D-149)
- Vocabulário permitido: técnico OU user-facing (construtora entende ambos)
- Checklist: técnico · derivação mecânica de `casos_esperados.yaml` via 5 templates D-148
- Gate: visão construtoramente validada · 6º quadrado ✅ · desbloqueia próxima visão · **NÃO atesta prontidão para cliente final**
- Modalidade: C mista com Arquiteto presente (D-156 preservado)

**Camada 2 · Validação Visual de Produto (VVP):**
- Quem opera: cliente final real · não Usuária construtora
- Quando: horizonte parqueado · pós-Família A validada · antes de go-to-market
- Base: bases reais de cliente
- Vocabulário permitido: **exclusivamente user-facing**
- Checklist: user-facing · derivado das tabelas de vocabulário bilingue (D-160) · tradução do técnico VVC
- Gate: produto validado para go-to-market · bloqueia lançamento se falhar
- Modalidade: sessão futura dedicada "Definição operacional VVP" · NÃO é escopo deste ALINHA

**Critérios de aprovação VVC:**
1. Checklist técnico derivado (D-148) · todos os itens ✅
2. Excel baixado e inspecionado visualmente · 3 pontos (Coração Visual nomeado · 6 blocos do Resumo Executivo em user-facing · Diagnóstico fundido em 6 seções)
3. Paleta executiva efetivamente aplicada ao Excel
4. Gate desacoplado · download disponível antes de checklist ✅
5. Registro: planilha aba 2 · 6º quadrado ✅

**Critérios de aprovação VVP (declarados para anti-esquecimento · C.2):**
1. Checklist user-facing · todos os itens ✅ por amostra
2. Base real · mínimo 1 por vertical-alvo
3. Cliente real opera sem assistência técnica
4. Excel aberto por executivo sem contexto prévio (teste de clareza standalone)
5. 3 vertical-alvos testados
6. Registro: planilha aba 1 Zona 3 · linha VVP

**Separação estrutural de "baixar Excel" vs "aprovar visão" (OBS-09):** Em VVC · botão "Baixar Excel" deixa de estar atrás do gate de checklist ✅. Excel baixa livremente. Aprovação ✅ é ato separado. Em A-VN a partir de V1 · separação desde início. Em ALINHA-Retroação-V2 · mesma mudança aplicada a `app_v2.py`.

**Critérios de ativação de ALINHA-Retroação-V2:** V1 aprovada em VVC · V11 aprovada em VVC · Família A completa sob método novo · Usuária pode declarar adiamento via D-XXX mas não pular sem decisão formal.

**Razão:** (1) 1 princípio B.4 forçando 2 papéis diferentes é imprecisão estrutural · desdobramento honra C.5. (2) VVP não tem escopo agora mas precisa existir como compromisso declarado · senão desaparece silenciosamente (anti-C.2). (3) Separar baixar de aprovar corrige OBS-09 no nível do princípio · não só de implementação. (4) VVC preserva D-156 integral. (5) Horizonte VVP parqueado junto com go-to-market evita confusão.

**Impacto:**
- CONTEXT §9 B.4 reescrito com 2 camadas e critérios de ambas
- GLOSSARIO 2 verbetes novos (VVC · VVP) com critérios
- Instruções v3 atualiza "O que NÃO fazer" (não confundir camadas · não gatear download)
- Planilha aba 1 Zona 3 ganha linha "Validação Visual de Produto"
- A-V1 implementa separação download/aprovação desde início
- app_v2 recebe ajuste em ALINHA-Retroação-V2

**Referência canônica:** CONTEXT §9 B.4 (2 camadas) · GLOSSARIO verbetes VVC · VVP · D-156 (preservada · opera na camada VVC).

---

### D-161 — C.D6 · DDU · Default Declarado Universal · D-024 promovido a princípio derivado
**Data:** 2026-04-23 · **Bloco:** ALINHA-Descoberta-Camada-Produto · **Status:** Fechada

**Contexto:** DEC-09 de VV-V2 · manifestação B das 14 OBS (OBS-03a · OBS-05). D-024 estava cristalizada para casos específicos (TED · Modo 4 · base consumida). OBS revelaram ausência em: rótulos user-friendly (OBS-03a · campos "Rótulo Origem"/"Rótulo Comparado" vazios · deveriam vir pré-preenchidos com nome da coluna `Orcado`/`Realizado` da base de simulação) · checkbox base pré-agregada (OBS-05 · motor tem evidência de cardinalidade mas não sugere).

**Decisão:** Elevar D-024 de "padrão consolidado" a **princípio derivado universal** da Camada C · equiparável a CPCO · TED · BAD · MBO · ECP. Nomeação canônica: **C.D6 · DDU · Default Declarado Universal**.

**Enunciado C.D6:** *Toda vez que o motor tem evidência para sugerir preenchimento de seletor ou configuração, DEVE aplicar default declarado com a evidência visível ao usuário e opção fácil de alterar. A decisão nunca é silenciosa · o usuário vê o default, vê por que foi sugerido, pode sobrescrever em um clique.*

**Deriva de:** C.2 (nada silencioso) + C.5 (TabloFlow analisa sobre dado informado · nunca decide por ele).

**Escopo:** Todas as 11 visões. Aplicável a qualquer seletor configurável no app.

**5 pontos de aplicação obrigatória identificados (não-exaustivos):**
1. Rótulos user-friendly · pré-preencher com nome da coluna · evidência = cabeçalho original
2. Checkbox base pré-agregada · sugerir baseado em análise de cardinalidade · evidência = "detectamos X linhas com chave única vs Y combinações de agrupadores"
3. Modo da base (TRANSACIONAL vs PRE_AGREGADO) · parcialmente aplicado · reforçar evidência visível
4. Agrupadores candidatos · motor pode sugerir ranking (baixa cardinalidade · repetição estrutural)
5. TED · thresholds editáveis · já aplicado · manter

**Regra de verificação:** cada P-VN declara tabela de seletores user-facing · para cada seletor responde "motor tem evidência?" · se sim · aplica C.D6 · se não · declara porque não aplicar.

**Razão:** (1) Padrão tinha 3 aplicações consolidadas · promoção a universal fecha ambiguidade. (2) C.5 é o coração · sugestão com evidência respeita C.5 (mostra o que viu · não decide · usuário confirma). (3) Completa série de princípios derivados de 20/04/2026 (C.D1-C.D5 · 6ª entrada natural). (4) OBS-03a e OBS-05 teriam sido evitadas se princípio fosse universal desde Spec V2.

**Impacto:**
- CONTEXT §9 Camada C · novo derivado C.D6 · DDU
- §13 checklist de derivados verificados passa de 5 para 6
- GLOSSARIO verbete DDU
- Instruções "O que NÃO fazer" ganha item sobre ausência de C.D6 onde motor tem evidência
- F-APRESENT capability 2 considera C.D6 para rótulos
- D-024 marcada como "Superada por D-161" no histórico

**Referência canônica:** CONTEXT §9 C.D6 · D-024 (precedente original) · DECISIONS D-161.

---

### D-160 — Vocabulário bilingue obrigatório · técnico canônico ↔ user-facing
**Data:** 2026-04-23 · **Bloco:** ALINHA-Descoberta-Camada-Produto · **Status:** Fechada

**Contexto:** DEC-06 de VV-V2 · manifestação A das 14 OBS (9 de 14 · OBS-01/02/04/06/07/10/11/13/14). Vocabulário técnico vaza em 100% das superfícies visíveis ao cliente: `TED · Thresholds editáveis` em sidebar · `E1 · E2 · E3 · E4 · E5` em stepper · `campo_analisado` · `POR_COLUNAS` · `D-151` · `chave` · `Numérico aditivo/relativo/não-aditivo` em Tela 3 · 6 blocos do Resumo Executivo como dumps JSON (`visao`, `data_execucao`, `top_variacoes`, `datetime.datetime(2026, 4, 23, ...)`) · classificações em enum caps (`PRESENTE_AMBOS`, `AUSENTE_ORIGEM`) · variação `0.010889926`.

**Decisão:** Toda superfície visível ao cliente (app · Excel · checklist user-facing · microcopy de erro) usa **exclusivamente** vocabulário user-facing. Vocabulário técnico canônico preserva-se em Specs, contratos Pydantic, testes, logs, DECISIONS, código. Nunca vocabulário técnico atravessa a fronteira para superfície visível.

**Mecanismo de aplicação em 3 camadas:**

1. **Tabela canônica transversal** · vive em `/specs/vocabulario_bilingue.md` · mantida pelo Arquiteto · entradas para enums universais (classificações · semânticas · modos de base · tipos de campo · warnings · stepper) · expansível por visão. v1 cobre Família A (V1 + V11 + pós-retroação V2).
2. **Seção obrigatória em cada P-VN** · tabela de vocabulário bilingue da visão · consome tabela transversal + adiciona termos visão-específicos.
3. **Aplicação em F-APRESENT** · capability 2 consome as duas tabelas acima · aplica em Excel. A-VN importa ao renderizar telas.

**Tabela canônica transversal v1 · 7 blocos (entregue como `/specs/vocabulario_bilingue.md` no kit δ):**
- Bloco 1 · Stepper (5 etapas Família A)
- Bloco 2 · Modos da base
- Bloco 3 · Classificações estruturais (V2 replicável em V1/V11)
- Bloco 4 · Tipos de campo (taxonomia D-025)
- Bloco 5 · Thresholds (TED)
- Bloco 6 · Warnings universais
- Bloco 7 · Termos proibidos em superfície cliente (lista negativa)

**Proibições consolidadas (bloco 7):**
- Nomes de atributo Python literais em superfície cliente (`campo_analisado` · `origem_rotulo_ux` · `limiar_estabilidade_pct`)
- Enums em caps (`POR_COLUNAS` · `PRESENTE_AMBOS`)
- Códigos D-XXX (`D-151`)
- `datetime.datetime(...)` serializado cru
- Fração decimal apresentada como "percentual"
- Python dict serializado em célula

**Razão:** (1) Regra clara · fronteira nítida · impossível ter vazamento silencioso se respeitada. (2) Tabela canônica transversal evita divergência entre visões da mesma família. (3) Primeira aplicação em V1/V11 calibra · V2 absorve em ALINHA-Retroação-V2. (4) Integra com D-159 capability 2 · F-APRESENT é implementador técnico · tabela é fonte. (5) Lista negativa (bloco 7) tem autoridade equivalente à lista positiva · operacionaliza proibições.

**Impacto:**
- `/specs/vocabulario_bilingue.md` v1 criado (entregue no kit δ)
- CONTEXT §5 ganha fonte de verdade · §9 Camada B reforça B.2 · §13 ganha padrão estrutural
- Instruções v3 "O que NÃO fazer" recebe 5 proibições novas
- F-APRESENT capability 2 implementa consumo
- P-VN seção 2 consome
- D-153 refinada · labels TED via vocabulário bilingue

**Referência canônica:** `/specs/vocabulario_bilingue.md` · CONTEXT §5 · §13 · P-VN seção 2.

---

### D-159 — Subsistema F-APRESENT · camada de apresentação executiva na Fundação
**Data:** 2026-04-23 · **Bloco:** ALINHA-Descoberta-Camada-Produto · **Status:** Fechada · P0 ✅ 23/04/2026 fim da tarde · P1 ✅ 23/04/2026 noite/madrugada · subsistema F-APRESENT completo · 10 capabilities operacionais · 594/607 verdes (13 vermelhos pré-existentes formalizados em D-169)

**Contexto:** DEC-08 de VV-V2 · manifestação C das 14 OBS (Excel como dump · OBS-10/11/12/13/14). Precisa formalizar bloco novo da Fundação · escopo · posição relativa a F-MOT/F-TRANS/F-EXP/F-BASE · capabilities iniciais.

**Decisão:** Criar bloco `F-APRESENT` como **5º subsistema da Fundação** (adição · não reescrita dos 4 existentes). Implementado em sessão combinada Claude Code (D-155) antes de P-V1. Capabilities executivas transversais consumidas por todas as 11 visões. Código em `/src/apresentacao/` (diretório novo · precedentes `/src/transversais/` e `/src/geradores/`).

**10 capabilities canônicas (versão MVP · priorizadas por frequência de uso):**

| # | Capability | Prioridade | Consumida por |
|---|---|---|---|
| 1 | Catálogo de 4 paletas (D-164) | P0 | todas |
| 2 | Rótulos user-facing universais (consome D-160) | P0 | todas |
| 3 | Tabela Excel nativa + totais dinâmicos | P0 | todas com abas tabulares |
| 4 | Formatação monetária BR | P0 | todas com valores monetários |
| 5 | Formatação percentual | P0 | todas com variação/taxa |
| 6 | Colunas adaptativas ao cenário | P0 | todas com variantes estruturais |
| 7 | Resumo Executivo narrativo em 6 blocos | P0 | todas |
| 8 | Badges semânticos | P1 | todas com classificação |
| 9 | Hierarquia tipográfica | P1 | todas |
| 10 | Diagnóstico narrativo 6 seções (consome D-165) | P1 | todas |

P0 = MVP bloqueador de P-V1. P1 = bloqueador de A-V1 mas não de P-V1 · pode rodar em paralelo (A6 da Onda 2 · Opção β confirmada).

**Interfaces mínimas por capability (detalhadas em CONTEXT §15.12):**
- Cap 1: classe `Paleta` + `CATALOGO_PALETAS` + `aplicar_paleta(workbook, paleta)`
- Cap 2: `carregar_vocabulario_bilingue()` + `traduzir(termo_tecnico, contexto)`
- Cap 3: `criar_tabela_executiva(ws, range, nome, totais_por_coluna)`
- Cap 4: `FORMATO_MONETARIO_BR` constante + `aplicar_formato_monetario(celulas)`
- Cap 5: `FORMATO_PERCENTUAL` constante + `aplicar_formato_percentual(celulas, conversao_fracao=True)`
- Cap 6: `montar_colunas_adaptativas(config_usada, esquema_colunas)`
- Cap 7: `renderizar_resumo_executivo(ws, resumo, paleta, vocabulario)`
- Cap 8: `aplicar_badge(celula, classificacao, paleta)`
- Cap 9: `aplicar_hierarquia_tipografica(ws, paleta)`
- Cap 10: `renderizar_diagnostico(ws, config_usada, resolucao, modelo, diag, warnings, paleta, vocabulario)`

**Estratégia de testes:** `/src/testes/test_apresentacao.py` · ~200-300 testes incrementais · 3 fixtures canônicas (paleta_azul · paleta_cinza · workbook_exemplo construído a partir de `V2Result` simulado) · 4 tipos de teste (interface · snapshot · regressão · invariantes). Meta pós-P0 ~500 testes · pós-P1 ~550. Regressão obrigatória dos 301 anteriores.

**Gate P0 (abre P-V1):** 7 capabilities P0 implementadas · suite F-APRESENT passando (~200 testes) · amostras geradas (4 Excel de demo · 1 por paleta · consumindo `V2Result` canônico) · inspeção visual pela Usuária · regressão 301 testes anteriores verdes.

**Gate P1 (abre A-V1):** 3 capabilities P1 implementadas · suite completa (~250-300 testes) · regressão completa verde.

**Sequência operacional pós-ALINHA (A6 da Onda 2 · Opção β):**
1. F-APRESENT P0 · ~1 semana Claude Code
2. P-V1 · Arquiteto · consome P0
3. Paralelo: F-APRESENT P1 · ~3-5 dias Claude Code
4. S-V1 · Arquiteto · consome P-V1
5. V-V1 · sessão combinada
6. A-V1 · sessão combinada · consome P-V1 + P0 + P1
7. VV-V1 (VVC)

**Razão:** (1) Camada transversal a 11 visões · domicílio correto é Fundação · não visão a visão. (2) Capabilities são primitivas · P-VN declara quais usar e como · separação de concerns limpa. (3) Priorização P0/P1 dá caminho de desbloqueio mínimo · não obriga implementar tudo antes de P-V1. (4) Paralelismo P1 durante P-V1/S-V1/V-V1 reduz tempo total de Família A · coordenação viável com gate explícito antes de A-V1. (5) `/src/apresentacao/` como diretório novo reflete hierarquia conceitual · F-APRESENT é subsistema · merece pasta.

**Impacto:**
- CONTEXT §6.2 ganha F-APRESENT entre F-EXP e F-BASE (5º subsistema)
- CONTEXT §15.12 convenções de F-APRESENT
- spec_fundacao.md ganha seção F-APRESENT
- Planilha aba 2 ganha linha F-APRESENT (bloco Fundação adicional · status ⬜)
- `/src/apresentacao/` novo diretório
- Prompt Claude Code F-APRESENT · próxima sessão

**Referência canônica:** CONTEXT §6.2 · §15.12 · spec_fundacao.md · `/src/apresentacao/`.

---

### D-158 — Artefato P-VN · Spec de Produto por visão · Fase 2 com 6 artefatos
**Data:** 2026-04-23 · **Bloco:** ALINHA-Descoberta-Camada-Produto · **Status:** Fechada

**Contexto:** DEC-07 de VV-V2. Síntese estrutural das 14 OBS apontou lacuna única: método em 3 fases não tem "desenho de produto" como fase declarada · 4 manifestações (vocabulário vaza · D-024 não universal · Excel como dump · B.4 assume leitor técnico). Precisa formalizar artefato novo com papel, posição no ciclo e relação com S-VN.

**Decisão:** Criar artefato `P-VN` (Spec de Produto) na Fase 2. Ciclo por visão passa de 5 para 6 artefatos:

| Ordem | Artefato | Papel |
|---|---|---|
| 1 | **P-VN** | Spec de Produto · paleta · vocabulário bilingue · arquitetura Excel · microcopy · checklist user-facing |
| 2 | S-VN | Spec técnica · contrato + regras + wireframe funcional |
| 3 | B-VN | Base (condicional · D-147) |
| 4 | V-VN | `visao_vN.py` |
| 5 | A-VN | `app_vN.py` · aplica P-VN + S-VN |
| 6 | VV-VN | VVC (D-162) |

**Ordem P-VN antes de S-VN:** P-VN estabelece vocabulário user-facing e arquitetura de abas → S-VN usa esse vocabulário nos contratos Pydantic. Dupla aprovação B.2 preserva-se · reforço: agora é aprovação de P-VN + S-VN + wireframe HTML (tripla).

**Estrutura obrigatória de P-VN · 5 seções canônicas:**

**Seção 1 · Paleta executiva selecionada**
- 1 das 4 paletas de D-164 · justificativa
- Default por visão (Família A: Cinza · V1 · V11 · V2 retroagida)

**Seção 2 · Vocabulário bilingue da visão**
- Tabela técnico ↔ user-facing
- Consome `/specs/vocabulario_bilingue.md` (D-160)
- Adiciona termos visão-específicos

**Seção 3 · Arquitetura de abas do Excel**
- Ordem · nome user-facing · propósito
- Coração Visual (§13.6)
- Contrato de unidade por campo (D-166)
- Função de total por coluna (D-166)
- Colunas adaptativas declaradas (D-166)

**Seção 4 · Microcopy de telas**
- Títulos · subtítulos · captions · labels · ajudas · erros · warnings

**Seção 5 · Checklist user-facing**
- Esqueleto derivado do checklist técnico VVC
- Tradução via tabela de vocabulário bilingue
- Aplicação operacional definida em sessão futura "Definição operacional VVP"

**Entrega:** markdown consolidado · amostras de paleta aplicada vivem como assets de F-APRESENT capability 1 · P-VN referencia (recomendação γ de A3 · evita duplicação e divergência).

**Razão:** (1) P-VN dá domicílio único ao que hoje vaza por todo lado (9 das 14 OBS). (2) P-VN antes de S-VN garante que vocabulário user-facing molda o contrato · não o contrário · evita retroação constante. (3) 5 seções são mínimo viável · cada uma corresponde a uma classe de OBS observada. (4) Entrega via amostra de F-APRESENT evita redundância · P-VN só referencia a paleta escolhida.

**Impacto:**
- CONTEXT §15.11 convenções de P-VN
- CONTEXT §3 Fase 2 reescrita · 6 artefatos
- `/specs/produto/` novo diretório
- Planilha aba 2 · 6 quadrados por visão
- Instruções v3 "Como me usar" ganha "Gerar P-VN"
- GLOSSARIO verbete P-VN

**Referência canônica:** CONTEXT §15.11 · §3 · GLOSSARIO · `/specs/produto/`.

---

### D-157 — Reforma metodológica · camada de apresentação ausente no método em 3 fases
**Data:** 2026-04-23 · **Bloco:** ALINHA-Descoberta-Camada-Produto · **Status:** Fechada · Marco metodológico

**Contexto:** VV-V2 em 23/04/2026 · Usuária recalibrou a sessão de validação rotineira para descoberta estrutural: *"Essa sessão ela não é uma sessão de validação · ela é a reunião mais importante até aqui · daqui com certeza vão sair decisões que podem voltar em etapas anteriores · preciso da sua ajuda como arquiteto e gestor para entender as fases e otimizar metodologia"*. 14 observações emergiram em 4 manifestações de uma lacuna única:
- **Manifestação A** · Vocabulário técnico vaza em 100% das superfícies (9 OBS)
- **Manifestação B** · Princípio "default declarado" (D-024) não aplicado universalmente (2 OBS)
- **Manifestação C** · Excel tratado como dump estruturado, não como produto (5 OBS)
- **Manifestação D** · Gate B.4 assume usuário que lê vocabulário técnico (2 OBS)

Síntese estrutural: *"O método em 3 fases do TabloFlow não tem uma 'fase de desenho de produto'."*

**Decisão (Marco metodológico · equivalente a D-014):** Método TabloFlow passa a incluir **camada de apresentação executiva** formalizada em 2 frentes complementares:

1. **Fundação ganha subsistema F-APRESENT** (D-159 · adição · não reescrita) · capabilities executivas transversais em `/src/apresentacao/` + catálogo de 4 paletas (D-164) + rótulos user-facing universais (D-160) + colunas adaptativas + tabelas Excel interativas (D-166)

2. **Fase 2 ganha artefato P-VN** (D-158 · Spec de Produto) · ciclo por visão passa de 5 para 6 artefatos · P-VN precede S-VN · cobre paleta · rótulos user-facing · narrativa do Excel · arquitetura de abas · microcopy · checklist user-facing

Esta decisão é **cobertura** · todas as D-158 a D-166 descendem dela.

**Consequências imediatas no método:**
- Excel executivo declarado como produto principal (D-163 · §13.7 novo)
- Princípio B.4 desdobrado em VVC + VVP (D-162)
- D-024 promovido a princípio derivado universal C.D6 DDU (D-161)
- Diagnóstico canonizado em 6 seções user-facing (D-165)
- Excel canonizado como 4 requisitos de interatividade (D-166)

**O que a reforma NÃO invalida:**
- 301 testes verdes continuam verdes · motor V2 calcula certo
- Fundação sólida (F-MOT/F-TRANS/F-EXP/F-BASE) · recebe adição F-APRESENT · não reescrita
- 11 DCVs aprovados · compreensão de negócio intacta
- `casos_esperados.yaml` · gabarito analítico intacto
- Arquitetura em 3 fases · famílias · ciclo de blocos · estruturalmente válida
- Padrões ALINHA · D-033 · D-131 · funcionaram · foi exatamente por isso que a Usuária detectou a lacuna antes de V1 começar

**O que a reforma invalida ou força revisar:**
- Princípio B.4 tal como enunciado · desdobra em 2 camadas (D-162)
- §15.1 do CONTEXT (ciclo de 5 artefatos) · passa a 6 (D-158)
- Spec V2 · ficou em MVP técnico · retroação declarada como horizonte ALINHA-Retroação-V2

**Razão:** (1) 14 OBS consolidadas em 4 manifestações apontam para lacuna única. (2) Motor V2 calcula certo (301 testes) · descoberta é de camada nova · não regressão. (3) Reforma mínima viável · não reescreve Fundação · não invalida DCVs · não toca YAML. (4) Adicionar fase inteira ("Fase 2.5 · Design") foi alternativa descartada · fragmentação desnecessária · adição via P-VN + F-APRESENT preserva estrutura. (5) Sem D-157 como cobertura · D-158 a D-166 ficariam órfãs · sem rationale unificador.

**Impacto:**
- CONTEXT v3 (§1 · §3 · §6 · §9 · §13 · §15)
- DECISIONS D-158 a D-166 descendem desta
- Instruções v3
- GLOSSARIO ~15 verbetes novos
- Planilha reestruturada · 6 quadrados por visão + linha F-APRESENT + horizonte ALINHA-Retroação-V2 + 2 linhas VVP/Definição VVP
- Horizonte firme: `ALINHA-Retroação-V2` · pós-Família A · pré-IA-Família-A

**Referência canônica:** CONTEXT §3 (Fase 2 reescrita) · todas as D-158 a D-166 descendem · DECISIONS D-157.

## D-156 — Padrão VV-VN · Validação Visual acompanhada modalidade C mista com 3 pontos-chave
Data: 2026-04-23 · Bloco: A-V2 (retrospectiva · sessão combinada 2ª aplicação) · **Status:** Fechada · Refinada por D-162 (opera integralmente em VVC · camada 1 de B.4 desdobrado

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

**Nota de status · 23/04/2026 · ALINHA-Descoberta-Camada-Produto:** D-156 refinada por D-162. D-156 opera integralmente na **camada VVC** (primeira camada de B.4 desdobrado · Validação Visual Construtora) · modalidade C mista + 3 pontos-chave + 4 tipos de intervenção preservados · VVP (camada 2) terá protocolo operacional próprio decidido em sessão futura "Definição operacional VVP". D-156 continua vigente na Família A · primeira aplicação real foi em VV-V2 (23/04/2026 · onde a descoberta ocorreu · sessão recalibrada pela Usuária · funcionou exatamente como previsto · modalidade C mista permitiu absorver 14 OBS e 12 DECs no momento certo). Calibração empírica da Família A informará refinamentos se necessário.

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
Data: 2026-04-23 · Bloco: A-V2 (retrospectiva) · **Status:** Fechada · Refinada por D-160/D-161 (labels via vocabulário bilingue · defaults via C.D6)`

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

**Nota de status · 23/04/2026 · ALINHA-Descoberta-Camada-Produto:** D-153 refinada por D-160 e D-161. Decisão técnica de localização (sidebar global) preservada · mas **labels da sidebar** passam a consumir tabela de vocabulário bilingue (D-160 · bloco 5 · thresholds em user-facing) · e **defaults visíveis** na sidebar passam a aplicar C.D6 (D-161) com evidência quando motor tiver. Aplicação efetiva em V1 desde início · V2 em ALINHA-Retroação-V2. OBS-01 (sidebar desconectada visualmente do fluxo) fica em aberto como item de execução de P-V1 (decisão de microcopy e visual · não estrutural).


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
**Data:** 2026-04-21 · **Bloco:** ALINHA-Fase-1→Fase-2 · sub-bloco γ · **Status:** Fechada · Refinada por D-162 (opera na camada VVC)
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
**Nota de status · 23/04/2026 · ALINHA-Descoberta-Camada-Produto:** D-148 refinada por D-162. Checklist derivado continua sendo derivado mecânico do `casos_esperados.yaml` (5 templates canônicos preservados) · passa a ser explicitamente **checklist técnico para VVC** (Validação Visual Construtora · camada 1 de B.4 desdobrado) · não para VVP. Derivação user-facing para VVP será decidida em sessão futura "Definição operacional VVP" (horizonte pós-Família A). D-148 não muda em nada operacional na Família A em curso · continua vigente.
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
**Data:** 2026-04-18 · **Bloco:** DCV-V2 (Sessão 1) · **Status:** Fechada · Superada por D-161 (elevada a princípio derivado universal C.D6 · DDU)

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

**Nota de status · 23/04/2026 · ALINHA-Descoberta-Camada-Produto:** D-024 superada por D-161. Padrão "default declarado" promovido a princípio derivado universal da Camada C (C.D6 · DDU) · enunciado universal · escopo expandido para qualquer seletor configurável em qualquer visão. D-024 permanece no histórico como precedente original (cristalização em V2 · 3 aplicações: TED · Modo 4 · base consumida) · não é revogada · é elevada.
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
