# p_v1.md — Conciliação de Bases · Spec de Produto

**Visão:** V1 · Família A · Confronto entre universos · Conciliação de Bases
**Bloco:** P-V1 · 1º quadrado dos 6 do ciclo da V1 (D-158)
**Versão:** v1.1 · 26/04/2026 noite (correções retroativas D-212 aplicadas em §2.7 · §4.5 · novos §4.5-bis e §4.6-bis)
**Status:** **aprovada** (D-209 aprovou v1.0 · D-212 aplicou correções retroativas mantendo aprovação)
**DCV consumido:** `/specs/dcv/dcv_v1.md` · aprovado 18/04/2026 · 13 pendências fechadas (P-V1-01 a P-V1-10 + L-V1-A · L-V1-B · L-V1-D · L-V1-E)
**Mockup consumido:** `MOCKUP_V1_alpha2.md` · aprovado 26/04/2026 noite (D-208 · gate D-203 / D-204 cláusula A satisfeito · 8 defaults P-α.3 absorvidos como canônicos)
**Vocabulário consumido:** `/specs/vocabulario_bilingue.md` v3 · 10 blocos (estende-se aqui na Seção 2)
**Capabilities F-APRESENT consumidas:** 1-11 (P0 + P1 + capability 11 promovida em D-205)

**Fonte autoritativa de:** paleta executiva default · vocabulário user-facing da V1 · arquitetura de abas do Excel · contrato de unidade por campo · colunas adaptativas · microcopy de telas e Excel · checklist user-facing (esqueleto · operacional aguarda VVP).

**Regra de conflito (CONTEXT §5):** se P-V1 e S-V1 divergirem sobre vocabulário · microcopy · arquitetura de abas · contrato de unidade · paleta → P-V1 prevalece. Se divergirem sobre contrato lógico · regra de cálculo · invariante matemático → S-V1 prevalece.

---

## Preâmbulo · pegada V2 herdada literalmente

V1 herda da V2 pós-Promoção D-202 (suite 746/746) os seguintes elementos visuais e estruturais sem reescrever:

- **Paleta canônica** · 4 paletas executivas (Azul · Verde · Cinza · Vinho) · F-APRESENT capability 1
- **Helpers de F-APRESENT** · `escrever_titulo_aba` · `_renderizar_cabecalho_secao` · `_mesclar_card` · `_bordas_finas` · `_ajustar_larguras` · `criar_tabela_executiva` · `_calcular_altura_leitura_qualitativa`
- **Estrutura visual de aba bespoke** · título A1 · subtítulo A2 · banners de seção · cards · respiros entre seções · `sheet_view.showGridLines = False`
- **Estrutura visual de aba tabular** · ListObject Excel nativo · TotalsRow ativa · zebra · AutoFilter · TotalsRow herdando number_format das células de dados
- **Capability 11 · `formato_adaptativo_por_unidade`** · D-205 · aplicada em todas as colunas de valor
- **Contrato de unidade declarado por campo** · D-166 · 8 valores canônicos (MONETARIO_BRL · PERCENTUAL · QUANTIDADE · TEMPO_DIAS · TEMPO_HORAS · MULTIPLICADOR · RAZAO · ADIMENSIONAL)
- **Diagnóstico como última aba** · D-017 · invariante transversal a 11 visões
- **Vocabulário user-facing exclusivo em superfície cliente** · D-160 · zero vazamento técnico
- **Substituição dinâmica por rótulo amigável** · Bloco 3 do `vocabulario_bilingue.md` v2 · Família A inteira

V1-específico (genuinamente novo) catalogado na Seção 6 deste documento.

---

## 1 · Paleta executiva

### 1.1 · Default declarado

**Default V1:** **Azul executivo** (paleta 1 de F-APRESENT capability 1).

Aplicação de D-168 · Azul é default universal das 11 visões · P-V1 não justifica paleta semântica por visão · simplificação consolidada após P-V2 retroativa.

### 1.2 · Catálogo disponível e ordem do widget

Usuária escolhe na Etapa 4 (Configurações avançadas) · widget `radio` com 4 opções · ordem fixa **Azul · Cinza · Verde · Vinho** (sem microcopy semântica · só nomes · D-168). Aplica C.D6 · DDU · default declarado pré-selecionado · usuário sobrescreve com 1 clique.

| # | Nome | Onde aparece quando selecionada |
|---|---|---|
| 1 | Azul executivo (default) | Cabeçalhos de seção · banners · TotalsRow · zebra · bordas |
| 2 | Cinza executivo | Idem |
| 3 | Verde executivo | Idem |
| 4 | Vinho executivo | Idem |

### 1.3 · Pontos de aplicação

Paleta selecionada aplicada em:

- Cabeçalhos de seção via `_renderizar_cabecalho_secao` · banner colorido cor primária · texto branco
- Cabeçalho de tabelas via `criar_tabela_executiva` · ListObject style associado
- Zebra automática · cor secundária da paleta
- TotalsRow · cor primária com texto branco
- Bordas finas via `_bordas_finas(paleta)` · cor de borda escura
- Cards via `_mesclar_card` · borda fina · header com cor primária discreta
- Caracteres de status (✅ ⚠️) · cor da semântica dentro da paleta · não emoji bruto · padrão V2 (decisão P-α.3-02)

### 1.4 · Registro em metadado

A paleta selecionada é metadado do Excel gerado · registrada na Seção 9.1 do Resumo Executivo (Sub-bloco 9 · Configuração aplicada · linha "Paleta executiva: {nome}") e na Seção 1 do Diagnóstico (Configuração técnica completa · valor literal do enum interno).

---

## 2 · Vocabulário bilingue da V1

V1 consome `/specs/vocabulario_bilingue.md` v3 (10 blocos) e estende:

- **Bloco 3** · classificações estruturais · ganha as **6 classes V1** abaixo
- **Bloco 6** · warnings universais · ganha 3 warnings V1-específicos (W-V1-TOL · W-V1-DUP · W-V1-AMB)
- **Bloco 1** · stepper · V1 mantém padrão Família A "4 etapas + Revisão" (D-167) com adaptação para natureza dual

Termos puramente V1 (Status da Ponte · Cobertura por base · Síntese da Ponte) são declarados aqui como vocabulário V1 · candidatos a transversal Família A em ALINHA-Auditoria-pós-V11 (Seção 6 deste documento).

### 2.1 · Pares de comparação Família A · Origem × Comparado

V1 herda integralmente o Bloco 1.1 do vocabulário bilingue v2:

| Código técnico | User-facing widget E2 | User-facing após escolha |
|---|---|---|
| `Origem` | "Comparar de" | "Origem" (com rótulo amigável editável ao lado) |
| `Comparado` | "Comparar com" | "Comparado" (com rótulo amigável editável ao lado) |

**Substituição dinâmica:** quando Usuária declara rótulos amigáveis (ex: Origem = "Razão" · Comparado = "Balancete"), esses rótulos viram referência canônica em todo app e Excel · termos técnicos "Origem" e "Comparado" só aparecem entre parênteses como subtítulo se rótulos amigáveis em branco.

**Em V1 isto é sempre relevante** · conciliação tipicamente tem rótulos materiais (Sistema A × Sistema B · Razão × Balancete · ERP × Data Warehouse · Extrato × Sistema). A maior parte dos clientes V1 declara rótulos amigáveis · default vazio é fallback.

### 2.2 · Bloco 3 estendido · 6 classificações estruturais V1

Estende o Bloco 3 do `vocabulario_bilingue.md` v3. Os enums Pydantic ficam em `ConciliacaoV1Result.classificacao_registro` · valores literais a serem formalizados em S-V1.

| Código técnico | User-facing (sem rótulo amigável) | User-facing (com rótulo amigável) | Cor da paleta |
|---|---|---|---|
| `CONCILIADO` | "Conciliado" | "Conciliado" (rótulo igual · classe positiva) | Verde da paleta |
| `DIVERGENTE_VALOR` | "Divergente por valor" | "Divergente por valor" (rótulo igual) | Amarelo/laranja da paleta |
| `SO_ORIGEM` | "Só na Origem" | "Saiu do {origem_ux}" (ex: "Saiu do Razão") | Vermelho da paleta |
| `SO_COMPARADO` | "Só no Comparado" | "Apareceu no {comparado_ux}" (ex: "Apareceu no Balancete") | Vermelho da paleta |
| `DIVERGENCIA_DUPLICIDADE` | "Divergência por duplicidade" | "Divergência por duplicidade" (rótulo igual) | Amarelo/laranja da paleta |
| `DIVERGENCIA_AMBIGUIDADE` | "Divergência por ambiguidade de match" | "Divergência por ambiguidade de match" (rótulo igual) | Amarelo/laranja da paleta |

**Decisão P-α.3-03 absorvida (default canônico):**

- Quando rótulo amigável **declarado** (Origem ≠ "Origem" · Comparado ≠ "Comparado"): usa formulação direcional **"Saiu do" / "Apareceu no"** · alinha com Bloco 3 do vocabulário bilingue v2.
- Quando rótulo amigável **vazio** (defaults técnicos): usa formulação genérica **"Só na Origem" / "Só no Comparado"** · evita "Saiu do Origem" que soa estranho.
- A regra de despacho é determinística e implementada em F-APRESENT capability 2 · função `formatar_classificacao_v1(classificacao, origem_ux, comparado_ux) -> str`.

**Sub-classificação "Conciliado com tolerância absorvida"** · não é uma 7ª classe · é flag visual sobre `CONCILIADO`. Aparece em:

- Sub-linha cinza no Resumo Executivo Seção 2 (Taxa de Conciliação · "Dos N conciliados · M tiveram diferença absorvida pela tolerância")
- Coluna "Observações" do Mapa de Conciliação (Aba 3) · texto: `Tolerância absorvida: R$ {valor}`
- Listada na Seção 2 do Diagnóstico (Tolerâncias absorvidas · detalhe completo)

### 2.3 · Microcopy de Status da Ponte (NOVO em V1)

Status binário derivado de `ponte_v1.fecha_geral: bool` (a ser formalizado em S-V1):

| Estado | Microcopy curto (Resumo §4) | Microcopy expandido (Aba 5 cabeçalho) | Cor / ícone |
|---|---|---|---|
| Fecha | "Ponte fecha em todos os campos comparados" | "Ponte fecha em todos os campos · diferença total decomposta integralmente" | Verde da paleta · ✅ Unicode (decisão P-α.3-02) |
| Resíduo | "Resíduo de R$ {valor} em {N} campo(s) · ver Aba 5 · Ponte de Conciliação" | "Resíduo R$ {valor} não atribuído · investigar componentes na Aba 5" | Amarelo/vermelho da paleta · ⚠️ Unicode |

**Sub-linha discreta** (cinza · texto pequeno · abaixo do status):

- Quando "Fecha": *"A diferença total entre {origem_ux} e {comparado_ux} é decomposta integralmente · ver Aba 5"*
- Quando "Resíduo": *"Resíduo é a diferença não atribuída aos registros divergentes · investigar na Aba 5"*

**Decisão P-α.3-01 absorvida:** banner da seção é `Status da Ponte` (curto · não "Status da Ponte de Conciliação" que repete o nome da aba).

**Decisão P-α.3-02 absorvida:** ícones são caracteres Unicode (✅ ⚠️) com cor da paleta aplicada via formatação · não emoji bruto · alinha com padrão V2 que já usa Unicode em badges (cabeçalhos · TotalsRow). Implementação em F-APRESENT capability 9 (badges semânticos · P1).

### 2.4 · Microcopy de Status por campo na Ponte (Aba 5)

Para cada sub-Ponte (1 por campo comparado):

| Estado | Microcopy curto | Cor / ícone |
|---|---|---|
| Fecha (resíduo absoluto < ε) | "Campo fecha · resíduo absorvido pela tolerância" | Verde · ✅ |
| Resíduo > ε | "Resíduo R$ {valor} não atribuído · investigar" | Amarelo · ⚠️ |
| Caso especial · 0 divergentes mas resíduo > ε | "Atenção: 0 registros divergentes mas Ponte mostra resíduo · revise tolerâncias na Aba 6 · Diagnóstico" | Vermelho · ⚠️ |

### 2.5 · Status por campo no Mapa Analítico (Aba 4)

Coluna `Status · {campo}` da Aba 4 · valores canônicos:

| Código técnico | User-facing | Cor (formato condicional) |
|---|---|---|
| `IGUAL` | "Igual" | Verde da paleta |
| `DENTRO_TOLERANCIA` | "Dentro da tolerância" | Verde da paleta |
| `DIVERGENTE` | "Divergente" | Amarelo da paleta |
| `SEM_VALOR_ORIGEM` | "Sem valor na Origem" / "Sem valor no {origem_ux}" | Cinza |
| `SEM_VALOR_COMPARADO` | "Sem valor no Comparado" / "Sem valor no {comparado_ux}" | Cinza |
| `SEM_VALOR_AMBOS` | "Sem valor nos dois lados" | Cinza |

Substituição dinâmica por rótulo amigável aplicada em SEM_VALOR_ORIGEM e SEM_VALOR_COMPARADO · idêntica à regra do Bloco 3 do vocabulário bilingue v2 · NULO_ORIGEM/NULO_COMPARADO. F-APRESENT capability 2 estende para V1.

### 2.6 · Bloco 6 estendido · 3 warnings V1

Padrão Bloco 6 · `WARNING · {mensagem técnica} · ação sugerida: {ação}`. Os 3 warnings V1 são catalogados em `casos_esperados.yaml` (entrada V1 a ser criada em B-V1 · condicional D-147) e implementados conforme padrão V2.

| Código técnico | Microcopy user-facing (Diagnóstico §5) | Quando dispara |
|---|---|---|
| `W-V1-TOL` | "Tolerância absorveu diferenças · {N} registro(s) classificado(s) como Conciliado tinham diferença absoluta não-zero dentro da tolerância configurada · ação sugerida: revisar tolerância na Aba 6 · §6 Thresholds" | ≥ 1 registro conciliado com diferença absorvida |
| `W-V1-DUP` | "Duplicidade em chaves · {N} chave(s) duplicada(s) na {origem_ux} ou {comparado_ux} · ação sugerida: revisar dado de entrada ou consolidar antes do upload" | ≥ 1 chave duplicada em qualquer lado |
| `W-V1-AMB` | "Ambiguidade em match não-exato · {N} chave(s) produzindo múltiplos candidatos com modo de match Contém / Inicia com / Termina com · ação sugerida: revisar critério de match ou simplificar chave" | ≥ 1 chave com múltiplos candidatos no modo configurado |

**Padrão de exibição:** warnings com 0 ocorrências aparecem na Seção 5 do Diagnóstico com texto "*W-V1-XXX · 0 ocorrências · nenhuma a reportar*" · auditabilidade preservada (princípio C.2 · ausência é informação · padrão V2).

### 2.7 · Stepper · 4 etapas + Revisão · adaptação Família A para V1 (corrigida em D-212)

V1 mantém o padrão "4 etapas + Revisão" (D-167) com conteúdo adaptado à dualidade T-DUAL e refletindo o leiaute canônico do `app_v2.py` (suite 746/746 verde):

| Etapa | Título user-facing | Conteúdo |
|---|---|---|
| 1 | Escolher arquivo(s) | Decisão física do upload (1 ou 2 arquivos · radio simples · D-213) · escolha de 1 ou 2 abas no E1_OK · sem radio "Estrutura A/B" |
| 2 | Identificar lados | Rótulos amigáveis Origem/Comparado · campos editáveis · default "Origem"/"Comparado" quando vazio |
| 3 | Configurar análise | Agrupadores de match (até 5) · campos comparados (até 10 · com tipo + tolerância + unidade) · caso lógico inferido automaticamente em info-box (D-213 · ABAS_DISTINTAS ou MESMA_ABA_EM_COLUNAS) |
| 4 | Agrupadores executivos | OPCIONAL · 0 a 5 agrupadores executivos · default vazio · pode pular (aba "Resumo por Agrupador" do Excel não é gerada) · botão "Pular · ir direto para Revisar" |
| Revisão | Revisar e executar | 5 colunas-resumo (Arquivo · Lados · Agrupadores match · Campos comparados · Agrupadores executivos) · botão "Processar análise" |

**Regra de invalidação cascata** (padrão V2 · §3.10 de spec_v2.md): editar etapa N invalida etapas N+1 a 4 + Revisão. RESULTADO é estado pós-processamento · regenerado quando qualquer etapa anterior é editada.

**Bloco intermediário condicional · parqueado como P-V1-Evo-RESOL-CASO:** se motor V1 detectar caso estrutural pré-execução (ex: detecta que ambas as bases têm estrutura empilhada com coluna discriminadora · L-V1 fora de escopo) · pode disparar tela intermediária de redirecionamento. No MVP V1 isto não acontece · motor processa a base como recebida · stepper permanece 4+Revisão. Paralelo a P-V2-Evo-01 (D-154).

**Correção retroativa D-212 aplicada:** versão original (v1.0) declarava E4 com "Paleta · tratamento de nulos · TED" · contradizendo D-175 §5.4 (paleta no rodapé do RESULTADO) e D-178 (TED em expander no topo). Correção: E4 contém **somente** "Agrupadores executivos". Paleta vai para rodapé do RESULTADO (§4.6-bis). TED vai para expander no topo (§4.5-bis).

### 2.8 · Tabela de classificação técnica → user-facing consolidada

Resumo de despacho para F-APRESENT capability 2 (`formatar_classificacao_v1`):

```
def formatar_classificacao_v1(
    classificacao: Literal["CONCILIADO", "DIVERGENTE_VALOR", "SO_ORIGEM",
                          "SO_COMPARADO", "DIVERGENCIA_DUPLICIDADE",
                          "DIVERGENCIA_AMBIGUIDADE"],
    origem_ux: str,      # "Origem" se vazio, ou rótulo amigável
    comparado_ux: str,   # "Comparado" se vazio, ou rótulo amigável
    rotulo_amigavel_declarado: bool  # True se Usuária editou rótulo
) -> str:
    # SO_ORIGEM e SO_COMPARADO trocam de formulação
    # quando rótulo amigável declarado
```

### 2.9 · Termos novos V1 catalogados em vocabulario_bilingue (proposta)

Itens cuja absorção em `vocabulario_bilingue.md` v4 (próxima versão) é proposta nesta P-V1:

- **Bloco 3 estendido** · 6 classificações V1 com substituição condicional (Seção 2.2 acima · adendo retroativo ao Bloco 3)
- **Bloco 6 estendido** · 3 warnings V1 (W-V1-TOL · W-V1-DUP · W-V1-AMB · Seção 2.6 acima)
- **Bloco 11 NOVO (candidato · não promovido nesta P-V1)** · "Status binário com sub-linha de ação" (padrão Status da Ponte · candidato Família A · vide Seção 6 deste documento)

A absorção formal acontece quando P-V1 for aprovada · executada no kit de encerramento desta sessão.

---

## 3 · Arquitetura de abas do Excel

### 3.1 · Estrutura macro · 6 abas (1 condicional)

Ordem fixa · Aba 2 condicional ao agrupador executivo configurado.

| # | Nome user-facing (A1) | Natureza | Aparece | Pergunta que responde |
|---|---|---|---|---|
| 1 | Resumo Executivo | Bespoke · 9 seções narrativas | Sempre | Qual o resultado geral da conciliação? |
| 2 | Resumo por Agrupador | Tabular ListObject · expandido | Quando agrupador do Resumo configurado | Como se distribui por Filial / Conta / Centro de Custo? |
| 3 | Mapa de Conciliação | Tabular ListObject · todos os registros | Sempre | Quais registros · em que classificação? |
| 4 | Análise Analítica | Tabular ListObject · expansão por campo | Sempre | Em que campo cada registro divergiu? |
| 5 | Ponte de Conciliação | Bespoke · decomposição vertical | Sempre | Como a diferença total se compõe matematicamente? |
| 6 | Diagnóstico | Bespoke · 6 seções | Sempre · ÚLTIMA (D-017) | Como o sistema processou a análise? |

**Quando Aba 2 omitida:** ordem das demais não muda · Aba 3 segue sendo "Mapa de Conciliação" · documento Excel tem 5 abas em vez de 6.

**Distinção Mapa × Análise Analítica (Aba 3 vs 4):** diferença é de **grão por coluna** · não de grão por linha. Ambas têm 1 linha por registro. Mapa tem 1 coluna consolidada por registro (Diferença total · Σ |Diferença|). Análise Analítica tem 4 colunas por campo comparado (Valor Origem · Valor Comparado · Diferença · Status). Mapa = "quais registros divergem" · Análise = "em qual campo cada registro divergiu". Não são redundantes · são duas leituras complementares (Mockup §2 confirmou em α.2 com aprovação α.3).

### 3.2 · Aba 1 · Resumo Executivo · 9 seções

Ordem definitiva pós-reordenação Mockup α.1' (Q2 + Q3 + Status Ponte sobe · Síntese isola · 7 → 9 seções).

#### 3.2.1 · Seção 1 · Cabeçalho identificador (4 linhas máx · 3 linhas mín)

- Linha 1 (A1) · Título: `Conciliação de Bases · {origem_ux} × {comparado_ux}` · cor primária · branco · bold · altura 28
- Linha 2 (A2) · Subtítulo · cor secundária discreta · variantes por combinação `n_arquivos × caso_logico_inferido` (D-213):
  - **Caso 1** (`n_arquivos==2` · `ABAS_DISTINTAS`): `Gerado em {DD/MM/AAAA} às {HH:MM} · Origem: {nome_arquivo_origem} · {nome_aba_origem} · Comparado: {nome_arquivo_comparado} · {nome_aba_comparado}`
  - **Caso 2** (`n_arquivos==1` · `ABAS_DISTINTAS`): `Gerado em {DD/MM/AAAA} às {HH:MM} · Arquivo: {nome_arquivo} · Origem: {nome_aba_origem} · Comparado: {nome_aba_comparado}`
  - **Caso 3** (`n_arquivos==1` · `MESMA_ABA_EM_COLUNAS`): `Gerado em {DD/MM/AAAA} às {HH:MM} · Arquivo: {nome_arquivo} · Aba: {nome_aba} · Origem e Comparado em colunas distintas`
  - **Caso 4** (`n_arquivos==2` · `MESMA_ABA_EM_COLUNAS`): `Gerado em {DD/MM/AAAA} às {HH:MM} · Arquivo Origem: {nome_arquivo_origem} · {nome_aba_origem} · Arquivo Comparado: {nome_arquivo_comparado} · {nome_aba_comparado} · Pares já casados por construção`
- Linha 3 (A3) · CONDICIONAL · só aparece quando T-MODELO aplicado: `Modelo de configuração: {nome_modelo}`
- Linha 4 · respiro · altura 8

**Decisão P-α.3-08 absorvida:** seção tem 3 linhas mínimo (sem T-MODELO) · 4 linhas máximo (com T-MODELO). Default 3.

#### 3.2.2 · Seção 2 · Taxa de Conciliação · KPI primário

Banner: `Taxa de Conciliação`

**Card único centralizado** (3 linhas via `_mesclar_card`):
- Rótulo: `Taxa de Conciliação Geral`
- Valor: `87,3%` (formato adaptativo PERCENTUAL · 2 casas decimais · capability 11)
- Subtexto: `1.247 de 1.428 registros conciliados`

**Tabela de decomposição** (header + 7 linhas · TotalsRow ativa):

| Classificação | N registros | % do total |
|---|---:|---:|
| Conciliados | 1.247 | 87,3% |
| Divergentes por valor | 89 | 6,2% |
| {Saiu do origem_ux \| Só na Origem} | 47 | 3,3% |
| {Apareceu no comparado_ux \| Só no Comparado} | 32 | 2,2% |
| Divergência por duplicidade | 8 | 0,6% |
| Divergência por ambiguidade de match | 5 | 0,4% |
| **Total processado** | **1.428** | **100,0%** |

**Sub-linha condicional** (cinza · texto pequeno · só aparece quando há absorção):
- `Dos {N} conciliados · {M} tiveram diferença absorvida pela tolerância (soma R$ {valor})`

**Não há decomposição "match exato vs aproximado" no Resumo** (DCV-V1 §6.2 Seção 3 · regra explícita) · esse detalhe vive no Diagnóstico Seção 4.

#### 3.2.3 · Seção 3 · Volumetria

Banner: `Volumetria`

3 cards lado a lado via `_mesclar_card`:
- Card 1: `Registros · {origem_ux}` · valor: `1.302` (QUANTIDADE adaptativa)
- Card 2: `Registros · {comparado_ux}` · valor: `1.287`
- Card 3: `Processados após match` · valor: `1.428`

#### 3.2.4 · Seção 4 · Status da Ponte de Conciliação · NOVO em V1

Banner: `Status da Ponte`

1 linha grande de status (altura 36 · centralizado · ícone+texto via `_mesclar_card` largo):

- Caso Fecha: `✅ Ponte fecha em todos os campos comparados` · cor verde · bold
- Caso Resíduo: `⚠️ Resíduo de R$ {valor} em {N} campo(s) · ver Aba 5 · Ponte de Conciliação` · cor amarela/vermelha · bold

Sub-linha discreta cinza (microcopy ver Seção 2.3 deste documento).

#### 3.2.5 · Seção 5 · Valor financeiro por campo comparado

Banner: `Valor por campo comparado`

Tabela (header + 1 linha por campo comparado · até 10 linhas):

| Campo | Soma · {origem_ux} | Soma · {comparado_ux} | {Diferença líquida \| Variação absoluta (p.p)} | Σ \|Diferença\| | Tolerância absorvida |
|---|---:|---:|---:|---:|---:|

**Adaptação por unidade do campo** (capability 11 · Bloco 10.2 do vocabulário bilingue v3):
- Header da 4ª coluna: `Diferença líquida` (default) · vira `Variação absoluta (p.p)` quando `unidade=PERCENTUAL`
- Coluna `Σ |Diferença|` · sempre presente · texto pequeno do header pode incluir parênteses `(soma absoluta · auditoria)`
- Coluna "Tolerância absorvida" · quando 0 · exibe `—` · quando há absorção · `{N} reg · R$ {valor}`

**TotalsRow ativa** · função SUBTOTAL por coluna · herda number_format (regra V2 herdada · ver Preâmbulo).

**Restrição semântica para PERCENTUAL** (Bloco 10.4 do vocabulário bilingue v3):
- Coluna `Σ |Diferença|` aceitável (soma de p.p absolutos é interpretável como "deslocamento total")
- TotalsRow `Soma · {origem_ux}` para campos PERCENTUAL · vira **Média · {origem_ux}** (Bloco 10.3 · cálculo média ponderada simples · capability `valor_total_card`)

#### 3.2.6 · Seção 6 · Cobertura por base

Banner: `Cobertura por base`

2 cards lado a lado:
- Card 1: `Cobertura · {origem_ux}` · valor: `1.255 de 1.302 (96,4%)`
- Card 2: `Cobertura · {comparado_ux}` · valor: `1.255 de 1.287 (97,5%)`

Nota cinza pequena abaixo dos cards: `Cobertura mede quantos registros de cada base encontraram par no match. Útil para auditoria assimétrica.`

#### 3.2.7 · Seção 7 · Resumo por agrupador executivo · CONDICIONAL

**Aparece somente quando** Usuária configurou agrupadores do Resumo Executivo (P-V1-10 do DCV).

Banner:
- 1 agrupador: `Resumo por {nome_agrupador_executivo}`
- 2 agrupadores: `Resumo por {agrupador_1} × {agrupador_2}`

Tabela compacta (4 colunas essenciais · ordenação por |Diferença líquida| desc · empate alfabético do agrupador):

| {agrupador_1} [× {agrupador_2}] | N Conciliados | N Divergentes | Diferença líquida |
|---|---:|---:|---:|

**TotalsRow ativa** · soma por coluna numérica.

**Espelho compacto da Aba 2** · esta tabela tem 4 colunas essenciais · Aba 2 expande com colunas por campo comparado.

#### 3.2.8 · Seção 8 · Síntese do Diagnóstico

Banner: `Síntese do Diagnóstico`

4 linhas em formato `{rótulo} · {valor} · {ação}`:

- `Tolerância absorvida · {N} registros · R$ {valor} · ver Aba 6`
- `Duplicidades detectadas · {N} chaves afetando {M} registros · ver Aba 6`
- `Ambiguidades de match · {N} chaves afetando {M} registros · ver Aba 6`
- `Warnings · {N} ativos · ver Aba 6`

**Quando categoria zerada** · linha aparece com `0` e sem `· ver Aba 6` · ex: `Duplicidades detectadas · 0`. As 4 linhas sempre aparecem (auditabilidade · C.2).

**Status da Ponte NÃO repete aqui** · ele tem seção própria (Seção 4). Síntese cobre só os 4 itens listados.

#### 3.2.9 · Seção 9 · Configuração aplicada

Banner: `Configuração aplicada`

4 sub-blocos:

- **9.1 · Agrupadores de match** (1 linha): `Agrupadores de match: {Filial — Contém} · {CNPJ — Exato} · {Documento — Exato}`
- **9.2 · Agrupadores do Resumo** (1 linha · CONDICIONAL): `Agrupadores do Resumo: {Filial} · {Centro de Custo}`
- **9.3 · Campos comparados** (1 linha por campo): `Campo: {Valor Bruto} · tipo {Monetário} · unidade {Reais (R$)} · tolerância R$ 0,01`
- **9.4 · Modelo aplicado** (1 linha · CONDICIONAL · só com T-MODELO): `Modelo de configuração: {nome_modelo} (criado em {data}) · reaplicação regenera este Resumo idêntico`

Sub-blocos com texto pequeno cinza · não-banner · auditoria de referência rápida.

#### 3.2.10 · Bloco final · Leitura Qualitativa

Banner: `Leitura Qualitativa`

Bloco de prosa parametrizado · 3 a 6 frases · gerado por `construir_leitura_qualitativa_v1` (template paralelo a `construir_leitura_qualitativa_v2` em `templates/familia_a/leitura_qualitativa.py` pós-D-202).

**Estrutura semântica do texto** (não literal · gerado dinamicamente):

> A conciliação entre {origem_ux} e {comparado_ux} apresenta taxa geral de **{taxa_pct}**. Dos {N} registros processados, a maioria está conciliada · {Y} registros divergem por valor com diferença líquida de **R$ {valor}** {concentrada em {agrupador_principal} | concentrada em {N} agrupadores}. {N} registros aparecem só na {origem_ux} e {N} só no {comparado_ux}, sugerindo {leitura_estrutural}. A Ponte de Conciliação {fecha em todos os campos | tem resíduo de R$ {X} em {N} campo(s)}, indicando que {leitura_da_ponte}. Casos de duplicidade ({N}) e ambiguidade de match ({N}) {merecem atenção · ver Diagnóstico | sem incidências}.

**Regras de variação semântica** (paralelas a V2 · 5 leituras qualitativas):

| Faixa de taxa | Tom | Frase de fechamento |
|---|---|---|
| ≥ 95% | Conciliação satisfatória | "A conciliação geral está satisfatória dentro do critério declarado" |
| 70% – 95% | Análise de divergências localizadas | "Divergências concentradas merecem investigação focada" |
| < 70% | Investigação ampla recomendada | "Conciliação requer investigação ampla antes de reconciliação contábil" |

**Modificadores sobrepostos:**
- Ponte fecha + tolerância absorvida → tom positivo (`reforça fechamento`)
- Ponte com resíduo → tom de alerta (`investigação Aba 5`)
- Duplicidade ≥ 1% das chaves → modificador "qualidade do dado de entrada"
- Ambiguidade ≥ 1% das chaves → modificador "critério de match"

**Decisão P-α.3-06 absorvida (default canônico):** leitura qualitativa **cita o nome do agrupador de maior peso** quando há agrupador executivo configurado E a divergência total é ≥ 70% concentrada nele. Caso contrário · texto genérico "concentrada em {N} agrupadores". Paraleliza V2 (que cita estado de maior variação).

**Decisão Q5 absorvida:** leitura qualitativa **mora apenas no Resumo Executivo** · não criar leituras próprias para Mapa · Ponte · Diagnóstico. Cada aba operacional é auto-explicativa pelo título e estrutura.

**Altura calculada via `_calcular_altura_leitura_qualitativa`** · leitura V1 é tipicamente mais longa que V2 (cobre 6 classes + Status Ponte) · padrão V2 ajusta automaticamente.

### 3.3 · Aba 2 · Resumo por Agrupador · CONDICIONAL

ListObject Excel nativo · 1 linha por valor único do(s) agrupador(es) · ZebraStyle · TotalsRow ativa · AutoFilter ativo.

**Colunas:**

*Identificadores* (1 ou 2 colunas):
- `{nome_agrupador_1}` · ex: "Filial"
- `{nome_agrupador_2}` (se 2 agrupadores)

*Métricas estruturais* (4 colunas):
- `N Conciliados`
- `N Divergentes por valor`
- `N {Só na Origem | Só {origem_ux}}`
- `N {Só no Comparado | Só {comparado_ux}}`

*Métricas por campo comparado* (4 colunas × N campos · expansão dinâmica · até 10 campos):
- `Soma {origem_ux} · {campo}`
- `Soma {comparado_ux} · {campo}`
- `Diferença líquida · {campo}` (rótulo adaptativo · `Variação absoluta (p.p) · {campo}` para PERCENTUAL)
- `Σ |Diferença| · {campo}`

**TotalsRow ativa** · função SUBTOTAL · herda number_format adaptativo das células de dados.

**Ordenação default:** |Diferença líquida total| desc · empate alfabético.

**A1:** `Resumo por {nome_agrupador_executivo}` (com par "× {agrupador_2}" quando aplicável).

**Filtros pré-pensados** (não bloqueia outros): Filial específica · Top 10 por |Diferença|.

**Sem formatação condicional** nesta aba · leitura macro é o número absoluto · evita ruído visual.

### 3.4 · Aba 3 · Mapa de Conciliação

ListObject Excel nativo · 1 linha por registro processado · todos os registros (Conciliados + Divergentes) · ZebraStyle · TotalsRow ativa · AutoFilter ativo.

**Formato condicional na coluna `Classificação`:**
- Verde: `Conciliado`
- Amarelo: `Divergente por valor` · `Divergência por duplicidade` · `Divergência por ambiguidade`
- Vermelho: `Saiu do {origem_ux}` / `Só na Origem` · `Apareceu no {comparado_ux}` / `Só no Comparado`

**Colunas:**

*Identificadores* (N colunas dinâmicas · 1 por agrupador de match · até 5):
- `{nome_agrupador_1}` · ex: "CNPJ"
- `{nome_agrupador_2}` · etc.

*Coluna de classificação* (1 coluna · destacada · larga):
- `Classificação` · valores user-facing do Bloco 3 estendido (substituição amigável por F-APRESENT capability 2)

*Métricas consolidadas* (3 colunas · sempre presentes):
- `Diferença total` · soma das diferenças de todos os campos comparados desse registro · capability 11 adaptativa
- `Σ |Diferença|` · soma absoluta · auditoria
- `Variação total %` · `Diferença total / Soma Origem` · PERCENTUAL adaptativo

*Coluna Observações* (1 coluna · texto curto · CONDICIONAL · presente quando há ao menos 1 registro com observação):
- Para `Conciliado` com tolerância: `Tolerância absorvida: R$ {valor}`
- Para `Divergência por duplicidade`: `{N} registros na {origem_ux} · {M} no {comparado_ux}`
- Para `Divergência por ambiguidade`: `Match aproximado · {N} candidatos com score equivalente`
- Para outros casos: célula vazia (`—` se nulo · D-198)

**TotalsRow ativa**:
- Identificadores: vazios (TotalsRow não soma texto)
- `Classificação`: vazia (não soma enum)
- `Diferença total`: SUM com format adaptativo
- `Σ |Diferença|`: SUM com format adaptativo
- `Variação total %`: vazia (não faz sentido média/soma de %)
- `Observações`: vazia

**A1:** `Mapa de Conciliação`
**A2 subtítulo:** `1 linha por registro · use o filtro "Classificação" para isolar conciliados ou divergentes`

**Decisão P-α.3-07 absorvida (default canônico):** quando há **0 divergentes** · Aba 3 mantém todas as 1.428 linhas conciliadas (ou o que for o N) · não colapsa para card "Tudo conciliado". Auditabilidade > economia visual. Cliente pode filtrar para "Conciliado" e ver tudo · ou usar a Aba 1 §2 para visão de cima.

### 3.5 · Aba 4 · Análise Analítica

ListObject Excel nativo · 1 linha por registro · expansão por campo comparado em 4 colunas dedicadas. ZebraStyle · AutoFilter ativo.

**Decisão P-α.3-04 absorvida (default canônico):** TotalsRow **desativada** por default. Grão é registro·campo · soma faz menos sentido (Σ Valor Origem do campo Quantidade misturado com Σ Valor Comparado do campo Imposto não tem leitura). Usuária pode ativar manualmente no Excel se quiser somas pontuais.

**Colunas:**

*Identificadores* (mesmas N colunas dinâmicas da Aba 3 · 1 por agrupador de match):
- `{nome_agrupador_1}` · `{nome_agrupador_2}` · ...

*Coluna de classificação* (1 coluna · idêntica à Aba 3):
- `Classificação`

*Bloco por campo comparado* (4 colunas × N campos · expansão dinâmica até 10 campos):

Para cada campo comparado declarado:
- `Valor · {origem_ux} · {campo}` · ex: `Valor · Razão · Valor Bruto`
- `Valor · {comparado_ux} · {campo}`
- `Diferença · {campo}` (rótulo adaptativo · `Variação absoluta (p.p) · {campo}` para PERCENTUAL)
- `Status · {campo}` · valores canônicos da Seção 2.5 deste documento (Igual · Dentro da tolerância · Divergente · Sem valor na Origem · Sem valor no Comparado · Sem valor nos dois lados)

**Formato condicional na coluna `Status · {campo}`** (cada bloco de campo independente):
- Verde: `Igual` · `Dentro da tolerância`
- Amarelo: `Divergente`
- Cinza: `Sem valor na Origem` · `Sem valor no Comparado` · `Sem valor nos dois lados`

**A1:** `Análise Analítica`
**A2 subtítulo:** `1 linha por registro · cada campo comparado em 4 colunas · Origem · Comparado · Diferença · Status`

**Caso especial · 1 único campo comparado:** Aba 4 colapsa para 4 colunas extras (Valor Origem · Valor Comparado · Diferença · Status) e fica próxima do Mapa. Ainda assim mantém o detalhamento por campo (Mapa usa Diferença consolidada). As 2 abas continuam distinguíveis · Aba 4 não desaparece.

### 3.6 · Aba 5 · Ponte de Conciliação

Aba **bespoke** · não tabular · construída como decomposição vertical em forma de ponte (saldo inicial → componentes → saldo final · padrão contábil de "ponte de variação").

**Estrutura por campo comparado** (sub-bloco repetido para cada campo · até 10):

**Cabeçalho da aba (linhas 1-4):**
- A1: `Ponte de Conciliação · Como a diferença total se compõe`
- A2: subtítulo cinza · timestamp + Origem/Comparado (idêntico ao da Aba 1)

**Card grande de status geral (linhas 3-5):**
- 1 card largo (mescla A:H)
- Caso Fecha: `✅ Ponte fecha em todos os campos`
- Caso Resíduo: `⚠️ Resíduo de R$ {valor} em {N} campo(s)`
- Sub-linha: `Diferença total entre {origem_ux} e {comparado_ux}: R$ {valor}`

**Banner de seção principal (linha 6):** `Decomposição por campo comparado`

**Sub-bloco por campo** (estrutura repetida · linha de início varia):

```
Linha N+0  · Mini-banner do campo: `Campo: {nome_campo}` (cor secundária · fundo claro)
Linha N+1  · respiro
Linha N+2  · Header tabela: ["Componente", "Valor"]
Linha N+3  · `Saldo {origem_ux}`                                     | R$ {valor}
Linha N+4  · `(−) Registros só na {origem_ux} ({Saiu do origem_ux})` | -R$ {valor}
Linha N+5  · `(+) Registros só no {comparado_ux} ({Apareceu no})`    | +R$ {valor}
Linha N+6  · `(+/−) Diferenças nos divergentes por valor`            | ±R$ {valor}
Linha N+7  · `(+/−) Tolerância absorvida`                            | ±R$ {valor}
Linha N+8  · `(=) Saldo {comparado_ux} esperado`                     | R$ {valor}
Linha N+9  · `Saldo {comparado_ux} real`                             | R$ {valor}
Linha N+10 · `Resíduo` (real − esperado)                             | R$ {valor}
Linha N+11 · respiro
Linha N+12 · Status do campo: `✅ Campo fecha · resíduo absorvido pela tolerância`
                            ou `⚠️ Resíduo R$ {valor} não atribuído · investigar`
Linha N+13 · respiro · próximo campo começa em N+14
```

**Cores e ênfase:**
- `Saldo {origem_ux}` e `Saldo {comparado_ux}` (linhas N+3 e N+9) · cor primária · bold
- Linha `Resíduo` · cor amarela ou vermelha conforme status · bold
- Linhas intermediárias · texto neutro · números à direita
- Bordas finas em torno do bloco de cada campo · isolam visualmente

**Vocabulário:**
- "Saldo {comparado_ux} esperado" = soma da decomposição · indica o que **deveria** ser
- "Saldo {comparado_ux} real" = valor efetivo · indica o que **é**
- "Resíduo" = real − esperado · diferença não atribuída · auditoria humana investiga

**Caso especial · 0 divergentes mas Ponte mostra resíduo:**
Microcopy adicional sob o status do campo:
- `Atenção: 0 registros divergentes mas Ponte mostra resíduo · revise tolerâncias na Aba 6 · Diagnóstico`

**Quando há ≥ 3 campos comparados:** aba pode ficar comprida. Cada campo continua em sub-bloco próprio · não há agregação. Ponte é "extremamente importante" (declaração da Usuária no esboço α.1) · mantém detalhamento mesmo com aba longa.

**Aplicação de capability 11:** todos os números na Ponte usam `formato_adaptativo_por_unidade` baseado na unidade declarada do campo. Para campos PERCENTUAL · operações da ponte ainda fazem sentido (saldos médios + ajustes em p.p) · mas com rótulos adaptados ("Saldo médio {origem_ux}" em vez de "Saldo {origem_ux}" · TBD em S-V1 se aparecer caso real · default usa rótulos genéricos).

### 3.7 · Aba 6 · Diagnóstico · 6 seções

Aba bespoke · padrão F-APRESENT capability 10 (Diagnóstico narrativo · D-165) · adaptada à natureza V1.

**Decisão P-α.3-05 absorvida (default canônico):** ordem das 6 seções é **Configuração técnica primeiro** · cliente abre Diagnóstico procurando "como foi configurado". Ordem definitiva:

#### 3.7.1 · Seção 1 · Configuração técnica completa

Banner: `Configuração técnica completa`

Detalhamento técnico de tudo que a Aba 1 §9 mostrou em formato user-facing:
- Bases · arquivos · abas · linhas · colunas (estrutura A vs B)
- Modos de match por agrupador (Exato · Contém · Inicia com · Termina com)
- Tolerâncias absolutas por campo
- Estratégia de tratamento de nulos (P-V1-09 · null no lado ausente · diferença = null)
- Critério de match aproximado para casos com múltiplos candidatos (preserva como ambíguo · não casa)
- Paleta executiva selecionada · TED aplicados (se houver)

#### 3.7.2 · Seção 2 · Tolerâncias absorvidas

Banner: `Tolerâncias absorvidas`

Lista os N registros classificados como `Conciliado · com tolerância absorvida`:

| Identificadores | Campo | Diferença absorvida | Tolerância configurada |
|---|---|---:|---:|

Quando 0: `Nenhuma tolerância absorvida · todos os registros conciliados têm diferença exata zero`.

#### 3.7.3 · Seção 3 · Duplicidades detectadas

Banner: `Duplicidades detectadas`

Lista chaves duplicadas que geraram classificação `Divergência por duplicidade`:

| Chave (concatenada) | N registros na {origem_ux} | N no {comparado_ux} | Ação sugerida |
|---|---:|---:|---|

Ações sugeridas: `deduplicar antes do upload` · `consolidar (T-AGRUPA prévio em Módulo 2)` · `revisar dado de entrada`.

Quando 0: `Nenhuma duplicidade detectada · chaves únicas em ambas as bases`.

#### 3.7.4 · Seção 4 · Ambiguidades de match

Banner: `Ambiguidades de match`

Lista pares ambíguos onde o sistema teve mais de 1 candidato com score equivalente:

| Chave da {origem_ux} | Chaves candidatas no {comparado_ux} | N candidatos | Resolução aplicada |
|---|---|---:|---|

Resolução aplicada: `preserva como ambíguo · não casa · classificação = Divergência por ambiguidade de match`.

Quando 0: `Nenhuma ambiguidade detectada · todos os matches são determinísticos`.

#### 3.7.5 · Seção 5 · Warnings ativos

Banner: `Warnings`

Lista os 3 warnings catalogados em V1 (ver Seção 2.6 deste documento):

| Código | Microcopy user-facing | Contagem |
|---|---|---:|

Warnings com 0 ocorrências aparecem com texto `0 ocorrências · nenhuma a reportar` · auditabilidade preservada (princípio C.2).

**Warnings herdados do motor (Fundação):** se houver (ex: W-B01 · inferência de boolean disfarçado · D-008) · listados após os 3 V1.

#### 3.7.6 · Seção 6 · Thresholds (TED · D-205) e parâmetros editáveis

Banner: `Thresholds e parâmetros`

Tabela de TED (Thresholds Editáveis Declarados):

| Nome técnico → user-facing | Valor configurado | Valor default | Status |
|---|---|---|---|

Status: `Default` (configurado = default) · `Editado` (configurado ≠ default · destacado visualmente).

Em V1 os TED principais são (a confirmar definitivamente em S-V1):
- `epsilon_ponte` · "Tolerância de fechamento da Ponte" · default `R$ 0,01` para campos MONETARIO_BRL · `0` para outros
- `tolerancia_padrao_<campo>` · "Tolerância padrão do campo {nome}" · default `0` por campo

### 3.8 · Contrato de unidade por campo · D-166

Aplicação canônica do contrato de unidade declarado em Bloco 10 do `vocabulario_bilingue.md` v3 (D-194 · C.D8). Cada campo do contrato V1 declara sua unidade explicitamente · F-APRESENT capability 11 (`formato_adaptativo_por_unidade`) consome para formatação.

#### 3.8.1 · Campos de configuração (declarados pela Usuária)

| Campo do contrato V1 | Unidade canônica | Default inferido | Função de total |
|---|---|---|---|
| `agrupadores_match[*].rotulo_analitico` | (não-numérico · texto) | — | none |
| `campos_comparados[*].nome_analitico` | (não-numérico · texto) | — | none |
| `campos_comparados[*].tipo_logico` | (não-numérico · enum tipo_campo) | — | none |
| `campos_comparados[*].unidade` | (escolha da Usuária · 8 opções) | inferido de `tipo_logico` (Bloco 10.1) | — |
| `campos_comparados[*].tolerancia` | herda unidade do campo | 0 | none |

Inferência de unidade default a partir de `tipo_logico` (Bloco 10.1 do vocabulário bilingue v3):
- `Valor Monetário` → `MONETARIO_BRL`
- `Quantidade` → `QUANTIDADE`
- `Volume` → `QUANTIDADE` (Usuária pode trocar)
- `Percentual` → `PERCENTUAL`
- `Prazo` → `TEMPO_DIAS` (Usuária pode trocar para `TEMPO_HORAS`)
- `Índice` → `MULTIPLICADOR` (Usuária pode trocar para `RAZAO`)
- `Estado/Situação` → `ADIMENSIONAL`

Aplicação de C.D6 (DDU · D-161): default declarado · evidência visível · 1 clique para alterar.

#### 3.8.2 · Campos de saída do motor V1 (consumidos pelas abas)

| Campo do contrato V1Result | Unidade canônica | Função de total | Onde aparece |
|---|---|---|---|
| `valor_origem_<campo>` | herdada de `campos_comparados[i].unidade` | sum (soma da coluna · TotalsRow) | Aba 4 col `Valor · {origem_ux} · {campo}` · Aba 5 saldos |
| `valor_comparado_<campo>` | herdada | sum | Aba 4 col `Valor · {comparado_ux} · {campo}` · Aba 5 saldos |
| `diferenca_<campo>` | herdada · com sinal explícito | sum | Aba 4 col `Diferença · {campo}` · Aba 5 componentes |
| `diferenca_total_registro` | MONETARIO_BRL (consolidação multi-campo) | sum | Aba 3 col `Diferença total` |
| `sigma_diferenca_total_registro` | herdada do registro (consolidada) | sum | Aba 3 col `Σ \|Diferença\|` |
| `variacao_total_registro_pct` | PERCENTUAL | none (não soma %) | Aba 3 col `Variação total %` |
| `taxa_conciliacao_geral` | PERCENTUAL | none | Resumo §2 KPI |
| `cobertura_origem_pct` · `cobertura_comparado_pct` | PERCENTUAL | none | Resumo §6 |
| `n_registros_origem` · `n_registros_comparado` · `n_processados` | QUANTIDADE | sum | Resumo §3 |
| `n_conciliados` · `n_divergentes_*` | QUANTIDADE | sum | Resumo §2 tabela · Aba 2 · Aba 3 |
| `tolerancia_absorvida_<campo>` | herdada | sum | Resumo §5 col `Tolerância absorvida` · Diagnóstico §2 |
| `saldo_origem_<campo>` · `saldo_comparado_real_<campo>` · `saldo_comparado_esperado_<campo>` | herdada | none (saldos · não somáveis em coluna) | Aba 5 Ponte |
| `residuo_<campo>` | herdada | none | Aba 5 Ponte · Diagnóstico §6 |

**Regra de fallback** (C.5 · ausência ≠ erro silencioso): qualquer campo de saída sem `unidade` declarada gera bug de P-V1 · não exporta · S-V1 implementa validação Pydantic.

#### 3.8.3 · Colunas adaptativas declaradas

Aplicação de D-166 · colunas montadas dinamicamente · sem colunas vazias.

| Coluna | Aba | Condição de inclusão |
|---|---|---|
| `Observações` | Aba 3 (Mapa) | ≥ 1 registro com observação não-vazia (tolerância · duplicidade · ambiguidade) |
| `{nome_agrupador_2}` | Abas 2, 3, 4 | 2º agrupador configurado |
| Sub-bloco "9.2 · Agrupadores do Resumo" | Resumo §9 | Agrupador executivo configurado |
| Sub-bloco "9.4 · Modelo aplicado" | Resumo §9 | T-MODELO aplicado |
| Linha A3 (Modelo) | Resumo §1 | T-MODELO aplicado |
| Aba 2 inteira | — | Agrupador executivo configurado |
| Sub-linha "Tolerância absorvida" | Resumo §2 | ≥ 1 registro com tolerância absorvida |
| Coluna "Tolerância absorvida" | Resumo §5 (tabela) | sempre presente · valor `—` quando 0 |
| Linha "(+/−) Tolerância absorvida" | Aba 5 (Ponte) | sempre presente · valor `0` quando aplicável |

#### 3.8.4 · Restrições semânticas para PERCENTUAL

Quando `campos_comparados[i].unidade = PERCENTUAL` (campo raro mas legítimo · ex: conciliação de margens entre dois sistemas):

- Header da coluna `Diferença líquida` · vira `Variação absoluta (p.p)` (Bloco 10.2)
- Header da coluna `Variação total %` na Aba 3 · vira `Variação relativa (%)` para clareza (Bloco 10.2)
- Card "Total · {origem_ux}" · vira "Média · {origem_ux}" com cálculo média ponderada simples (Bloco 10.3 · `valor_total_card`)
- TotalsRow das somas · vira média (Bloco 10.4)
- Coluna `Diferença total` na Aba 3 · oculta (Bloco 10.4 · soma de p.p multi-campo viola C.D3) · substituída por mensagem em Observações: `Variação concentrada em {N} campo(s) percentuais`
- Leitura qualitativa · adaptada (omite valores entre parênteses dos casos · Bloco 10.4)

**Regra de aplicação:** F-APRESENT capability 11 (`formato_adaptativo_por_unidade`) recebe `unidade` por campo e despacha para os helpers da §10.5 do vocabulário bilingue. P-V1 não duplica a lógica · só declara que a regra do Bloco 10 vale.

### 3.9 · Função de total por coluna · D-166

| Aba | Coluna | Função TotalsRow |
|---|---|---|
| 1 (Resumo §2 tabela) | N registros | sum |
| 1 (Resumo §2 tabela) | % do total | sum (=100%) |
| 1 (Resumo §5 tabela) | Soma · {origem_ux} | sum (vira average para PERCENTUAL · §3.8.4) |
| 1 (Resumo §5 tabela) | Soma · {comparado_ux} | sum (vira average para PERCENTUAL) |
| 1 (Resumo §5 tabela) | Diferença líquida | sum |
| 1 (Resumo §5 tabela) | Σ \|Diferença\| | sum |
| 1 (Resumo §5 tabela) | Tolerância absorvida | sum |
| 1 (Resumo §7 tabela) | N Conciliados / N Divergentes | sum |
| 1 (Resumo §7 tabela) | Diferença líquida | sum |
| 2 | Identificadores | none |
| 2 | N Conciliados / N Divergentes / N Só Origem / N Só Comparado | sum |
| 2 | Soma {origem_ux} · {campo} / Soma {comparado_ux} · {campo} | sum (vira average para PERCENTUAL) |
| 2 | Diferença líquida · {campo} / Σ \|Diferença\| · {campo} | sum |
| 3 | Identificadores · Classificação · Observações | none |
| 3 | Diferença total · Σ \|Diferença\| | sum |
| 3 | Variação total % | none (não soma %) |
| 4 | Todas | none (TotalsRow desativada · §3.5) |

---

## 4 · Microcopy de telas (App Streamlit)

Esta seção declara microcopy das telas do app V1. Implementação detalhada (layout · widgets · transições) é responsabilidade de S-V1 (wireframe funcional). P-V1 declara o **texto user-facing canônico**.

### 4.1 · Microcopy global (todas as telas)

- **Header da app** (top · paralelo a `_render_header` da V2 · D-212): `TabloFlow · V1 · Conciliação de Bases` (st.title) + linha de 4 botões (Objetivo da Visão · Aplicar modelo · Salvar como modelo · Nova análise) + Stepper horizontal abaixo
- **Botão "Objetivo da Visão"** (CONTEXT §13.1): texto literal: `Objetivo desta análise`
  - Modal/expander aberto: `A V1 confronta duas bases lógicas e responde se elas representam o mesmo universo de dados e onde estão as divergências. Resposta em 4 perguntas: (1) Qual a taxa geral de conciliação? (2) Onde a divergência se concentra? (3) Quais registros divergem e por quê? (4) Como a diferença total se compõe matematicamente?`
- **Estado vazio sem upload:** `Faça upload das bases para começar a conciliação`
- **TED · expander "⚙️ Configurações avançadas" no topo** (D-178 · D-212): primeiro elemento abaixo do header de 4 botões · antes do Stepper · em todas as telas · colapsado por default · ver §4.5-bis para detalhamento

### 4.2 · Etapa 1 · Escolher arquivo(s) · CORRIGIDA em D-213

- **Título:** `Etapa 1 · Escolher arquivo(s)`
- **Subtítulo:** `Suba o(s) arquivo(s) Excel ou CSV com os dados que você quer comparar.`
- **Caption:** `Aceita Excel (.xlsx, .xls) e CSV. Pode ser 1 ou 2 arquivos · você decide abaixo.`
- **Radio principal · decisão FÍSICA do upload (D-213):** `Quantos arquivos você vai usar?`
  - Opção 1: `1 arquivo` (default)
  - Opção 2: `2 arquivos`
- **Help do radio:** `Em 1 arquivo, você escolherá 1 ou 2 abas no próximo passo (Caso 2 ou Caso 3 do confronto). Em 2 arquivos, escolherá 1 aba de cada (Caso 1 ou Caso 4).`
- **Caso n_arquivos == 1:**
  - 1 file_uploader · placeholder `Arraste ou selecione um arquivo Excel/CSV`
- **Caso n_arquivos == 2:**
  - 2 file_uploaders lado a lado:
    - `Arquivo da Origem` · placeholder idêntico
    - `Arquivo do Comparado` · idem
- **Pós-upload (E1_OK):** ver §4.2-bis abaixo · escolha de aba(s)
- **Botões:** `Voltar · trocar arquivo(s)` (esquerda) · `Confirmar e processar bases` (direita · `type="primary"`)

**Correção retroativa D-213:** versão original v1.0 declarava radio "Como suas bases estão organizadas?" com 2 opções estruturais (Em dois arquivos separados / No mesmo arquivo · em duas abas) · misturando decisão física (n_arquivos) com decisão lógica (caso do confronto). Versão v1.1 separa: E1 trata só decisão física · caso lógico do confronto é **inferido automaticamente em E3** a partir dos apontamentos.

### 4.2-bis · E1_OK · Pós-upload · Escolher aba(s) (NOVO em v1.1 · D-213)

- **Caso n_arquivos == 1 · `arquivo` carregado:**
  - Mensagem de sucesso: `Arquivo: {nome_arquivo} · Formato: {formato} · {N} abas detectadas`
  - Multiselect `Qual(is) aba(s) quer comparar?` · `max_selections=2` · default = primeira aba
  - Help: `Escolha 1 aba quando Origem e Comparado estão em colunas distintas dentro da mesma aba (Caso 3). Escolha 2 abas quando Origem em uma aba · Comparado em outra (Caso 2).`
- **Caso n_arquivos == 2 · ambos arquivos carregados:**
  - Mensagem de sucesso: `Arquivos: {nome_origem} ({N} abas) · {nome_comparado} ({M} abas)`
  - 2 selectboxes lado a lado:
    - `Aba do arquivo da Origem` · lista as abas do arquivo Origem
    - `Aba do arquivo do Comparado` · lista as abas do arquivo Comparado
- **Validação para avançar:**
  - n_arquivos==1: `len(escolha_abas) ∈ {1, 2}`
  - n_arquivos==2: ambas abas escolhidas (não-vazias)
- **Botões:** `Voltar · trocar arquivo(s)` · `Confirmar e processar bases` (`type="primary"`)
- **Ao clicar "Confirmar":** processar bases via T-DUAL · transitar para E2

### 4.3 · Etapa 2 · Identificação dos lados

- **Título:** `Etapa 2 · Identificação dos lados`
- **Subtítulo:** `Dê nomes amigáveis às duas bases que você está comparando`
- **Field 1:** `Nome amigável da Origem` · placeholder `Ex: Razão · Sistema A · ERP · Orçado`
- **Field 2:** `Nome amigável do Comparado` · placeholder `Ex: Balancete · Sistema B · DW · Realizado`
- **Nota cinza:** `Esses nomes vão aparecer em todas as telas e no Excel exportado. Se deixar em branco, o sistema usa "Origem" e "Comparado" como padrão.`
- **Botões:** `Voltar` · `Avançar · Etapa 3`

### 4.4 · Etapa 3 · Configuração analítica

#### 4.4.1 · Sub-etapa 3.1 · Agrupadores de match

- **Título:** `Etapa 3 · Configuração analítica`
- **Sub-título da sub-etapa:** `Agrupadores de match · qual a chave para casar registros entre as duas bases?`
- **Pergunta canônica:** `Que coluna(s) identificam de forma única cada registro?`
- **Repeater (até 5 instâncias):**
  - Field 1: `Coluna na {origem_ux}` (dropdown com colunas da aba Origem)
  - Field 2: `Coluna no {comparado_ux}` (dropdown com colunas da aba Comparado)
  - Field 3: `Rótulo analítico` (texto livre · default: nome da Coluna 1) · placeholder `Ex: CNPJ do Fornecedor`
  - Field 4: `Modo de match` (radio · 4 opções):
    - Opção 1 (default): `Exato (igualdade total)`
    - Opção 2: `Contém (chave de um lado contém a do outro)`
    - Opção 3: `Inicia com (chave de um lado inicia com a do outro)`
    - Opção 4: `Termina com (chave de um lado termina com a do outro)`
- **Botão "Adicionar agrupador":** habilitado até atingir 5
- **Mensagem ao tentar 6º:** `Limite de 5 agrupadores de match no MVP. Avalie se algum campo pertence a "Agrupadores do Resumo" ou se a chave pode ser simplificada.`

#### 4.4.2 · Sub-etapa 3.2 · Campos comparados

- **Sub-título:** `Campos comparados · quais valores devem bater entre as duas bases?`
- **Repeater (até 10 instâncias):**
  - Field 1: `Coluna na {origem_ux}`
  - Field 2: `Coluna no {comparado_ux}`
  - Field 3: `Nome analítico do campo` (texto livre) · placeholder `Ex: Valor Bruto · Imposto · Quantidade`
  - Field 4: `Tipo lógico` (radio · 7 opções):
    - `Valor Monetário` · `Quantidade` · `Volume` · `Percentual` · `Prazo` · `Índice` · `Estado/Situação`
  - Field 5: `Unidade` (selectbox · 8 opções do Bloco 10.1 · default inferido do tipo lógico · Bloco 10.1)
  - Field 6: `Tolerância absoluta` (number · default 0 · unidade herdada do campo · ex: `R$ 0,01` para MONETARIO_BRL)
- **Mensagem ao tentar 11º:** `Limite de 10 campos comparados no MVP.`
- **Microcopy de ajuda do tipo Estado/Situação:** `Compara categorias ou rótulos · não calcula diferença numérica`

#### 4.4.3 · Sub-etapa 3.3 · Agrupadores do Resumo Executivo · OPCIONAL

- **Sub-título:** `Agrupadores do Resumo Executivo · quer ver o resultado consolidado por algum recorte?`
- **Microcopy:** `Opcional. Quando configurado, gera tabela consolidada por filial / centro de custo / outro recorte na aba "Resumo por Agrupador".`
- **Repeater (até 5 instâncias):**
  - Field: `Coluna do agrupador` (dropdown · pode ser de qualquer base · texto categórico)
- **Botão "Pular"** · habilita avanço sem configurar (Aba 2 do Excel não é gerada)

### 4.5 · Etapa 4 · Agrupadores executivos · CORRIGIDA em D-212

- **Título:** `Etapa 4 · Agrupadores executivos`
- **Subtítulo:** `Opcional · quer ver o resultado consolidado por algum recorte?`
- **Microcopy explicativa:** `Quando configurado, gera tabela consolidada por filial / centro de custo / outro recorte na aba "Resumo por Agrupador" do Excel.`
- **Multiselect (até 5 · OPCIONAL · default vazio):**
  - Label: `Agrupar Resumo por (0 a 5 colunas)`
  - Help: `Default: nenhum · aba "Resumo por Agrupador" não será gerada · análise consolidada disponível em "Resumo Executivo"`
- **Botões:**
  - `Voltar`
  - `Pular · ir direto para Revisar` (habilita avanço sem configurar agrupador executivo)
  - `Próximo · Revisar e executar` (`type="primary"`)

**Correção retroativa D-212:** versão original (v1.0) declarava nesta etapa "Bloco 1 Paleta · Bloco 2 Tratamento de nulos · Bloco 3 TED · Botão Processar". Versão corrigida tem **somente** o multiselect de agrupadores executivos. Razões:
- Paleta vai para o rodapé do RESULTADO (§4.6-bis · D-175 §5.4 · trocável a qualquer momento sem reprocessar)
- TED vai para o expander "⚙️ Configurações avançadas" no topo de cada tela (§4.5-bis · D-178 revoga D-153)
- Tratamento de nulos não tem opções editáveis no MVP (default herdado do motor · sem toggle informativo redundante)
- Botão "Processar análise" vive na Revisão (E5) · não na E4

### 4.5-bis · TED · expander "⚙️ Configurações avançadas" no topo (NOVO em v1.1 · D-212)

D-178 estabelece TED em **expander no topo de cada tela** · não em sidebar. P-V1 §4.5 v1.0 citava sidebar (D-153 desatualizada) · corrigido aqui.

**Localização:** primeiro elemento abaixo do header de 4 botões · antes do stepper · em todas as telas (vazio · E1_OK · E2 · E3 · E4 · E5 · RESULTADO).

**Estado default:** colapsado.

**Conteúdo (TED globais sempre visíveis):**
- `Limite de células vazias em coluna de chave` · default `50%` · aplicado em B-V1-CHAVE-INVALIDA
- `Limite de registros processados` · default `500.000` · aplicado em B-V1-RESULTADO-EXCEDE
- `Limite de concentração para citar agrupador principal` · default `70%` · aplicado em LeituraQualitativa P-α.3-06

**Conteúdo (TED por unidade · só após E3 populada · Q2.C · D-211):**
- `Tolerância de fechamento da Ponte · {unidade_user_facing}` · 1 entrada por unidade efetivamente em uso nos `campos_comparados` configurados
- Defaults canônicos por unidade declarados em S-V1 §2.8

**Cada item do expander:** label user-facing · valor configurado · valor default · status (`Default` ou `Editado` · destaque visual quando Editado).

### 4.6 · Tela "Resultado da análise" (Revisão · pós-processamento) · ATUALIZADA em D-212

Padrão D-194 (separação download/aprovação · D-162). Tela é **render do Resumo Executivo no app** com vocabulário user-facing exclusivo.

- **Cabeçalho:** `📊 Resultado da análise` (st.header) + caption `Conciliação entre {origem_ux} e {comparado_ux} · gerada em {timestamp}`
- **5 blocos executivos** (paralelo a `_tela_resultado` da V2):
  - Bloco 1 · Cabeçalho executivo
  - Bloco 2 · Números principais (4 st.metric · Total Origem · Total Comparado · Diferença líquida · **Taxa de Conciliação** com destaque visual)
  - Bloco 3 · Saúde da comparação (tabela com 6 categorias em ABAS_DISTINTAS · 2 ativas + 4 zerados em MESMA_ABA_EM_COLUNAS)
  - Bloco 4 · Status da Ponte (banner ✅ Fecha ou ⚠️ Resíduo)
  - Bloco 5 · Leitura qualitativa + qualidade (avisos + expander "Ver detalhes do diagnóstico")
- **Rodapé com 3 colunas** (D-212 · D-175 §5.4):
  - Botão `← Voltar` (à esquerda)
  - Selectbox `Paleta do Excel` (4 opções · default Azul · D-168) · troca livre · Excel é regenerado quando paleta muda · sem reprocessar a análise
  - Botão `📥 Baixar Excel` (`type="primary"`)
- **Linha à parte:** botão `🔄 Nova análise` (reset completo)

**Decisão D-162 (separação download/aprovação):** o botão "Baixar Excel" gera o arquivo · não declara aprovação. Aprovação (gate B.4 camada 1 · VVC) é evento separado · acontece em VV-V1.

**Correção retroativa D-212:** versão original v1.0 listava paleta na E4 e citava "tabela de decomposição" sem mapear para os 5 blocos canônicos do `_tela_resultado` V2. Versão v1.1 espelha a estrutura V2 com paleta no rodapé.

### 4.6-bis · Paleta no rodapé do RESULTADO · paralelo D-175 §5.4 (NOVO em v1.1 · D-212)

D-175 §5.4 estabelece paleta no rodapé do RESULTADO · trocável a qualquer momento sem reprocessar. P-V1 §4.5 v1.0 citava paleta na E4 · corrigido aqui.

**Localização:** segunda coluna do rodapé do RESULTADO (entre "Voltar" e "Baixar Excel").

**Componente:** `st.selectbox`
- Label: `Paleta do Excel`
- Opções (ordem fixa · D-168): `Azul executivo` (default) · `Cinza executivo` · `Verde executivo` · `Vinho executivo`
- Help: `Escolha a paleta antes de baixar. A troca é livre e não exige reprocessar.`

**Comportamento:**
- Troca não invalida `RESULTADO` (não há reprocessamento)
- Excel é regenerado pelo `_render_botao_download_excel` no momento do clique em "Baixar Excel" · cache por chave composta `(paleta, v2_id)` evita regeneração desnecessária
- Paleta selecionada vai para `ConfigAplicadaV1.paleta_aplicada` · registrada na Aba 6 §1 do Diagnóstico

### 4.7 · Mensagens de erro e bloqueio

| Código técnico | Microcopy user-facing |
|---|---|
| `B-V1-NO-UPLOAD` | "Faça upload das bases para começar" |
| `B-V1-MESMA-COLUNA` | "A coluna de Origem e Comparado é a mesma · isto não é uma comparação · escolha colunas distintas" |
| `B-V1-MISTURA-ABAS` | "Os apontamentos de Origem e Comparado precisam ser todos da mesma aba · ou todos de abas distintas · não misturar" |
| `B-V1-AGRUPADOR-ZERO` | "Configure ao menos 1 agrupador de match para casar registros" |
| `B-V1-CAMPO-ZERO` | "Configure ao menos 1 campo comparado para a análise" |
| `B-V1-CHAVE-INVALIDA` | "A coluna {nome} tem ≥ {N}% de valores vazios e não serve como agrupador de match · escolha outra coluna" |
| `B-V1-MOTOR-INFERIU-INCOMPATIVEL` | "O sistema inferiu que a coluna {nome} é {tipo_inferido} mas você marcou como {tipo_escolhido} · revise" |
| `B-V1-RESULTADO-EXCEDE` | "A análise gerou {N} registros · acima do limite de 500.000 · simplifique a chave ou aplique filtro prévio" |
| `B-V1-MOTOR-FALHOU` | "Erro inesperado no processamento · {detalhe técnico} · entre em contato com o suporte" |

Catálogo a expandir em S-V1 (lista canônica de bloqueios · análoga à de spec_v2.md §3.9).

### 4.8 · Mensagens de warning na tela

Warnings da Seção 2.6 também são exibidos na tela "Resultado da análise" como avisos não-bloqueantes:

- **Padrão visual:** caixa amarela cinza-clara · ícone ⚠️ · texto microcopy + link "Ver detalhes na aba Diagnóstico"
- **Exemplo W-V1-TOL ativo:** `⚠️ Tolerância absorveu diferenças · 12 registros conciliados tinham diferença não-zero dentro da tolerância · ver Aba 6 · §2 do Excel`

### 4.9 · Mensagens informativas (não-bloqueio · não-warning)

- **Sem agrupador executivo configurado:** `Aba "Resumo por Agrupador" não será gerada · análise consolidada disponível em "Resumo Executivo"`
- **0 divergentes:** `Conciliação total · todos os {N} registros casaram dentro da tolerância configurada`
- **Match em modo não-exato com 0 ambiguidades:** `Modo de match não-exato configurado · 0 ambiguidades detectadas`
- **T-MODELO aplicado:** `Modelo "{nome_modelo}" aplicado · campos pré-preenchidos`

---

## 5 · Checklist user-facing · esqueleto

Esta seção declara o **esqueleto** do checklist que a Usuária aplicará em VV-V1 (6º quadrado · gate B.4 camada 1 · D-162 · modalidade C mista com Arquiteto presente · D-156). A operacionalização final (texto definitivo · ordem fina · agrupamento) acontece em **sessão "Definição operacional VVP"** (parqueada · Família A inteira em VVC primeiro).

VV-V1 segue padrão atual (VVC) · checklist técnico derivado mecanicamente do `casos_esperados.yaml` (D-148 · 5 templates). O esqueleto user-facing abaixo é a **versão paralela traduzida** do checklist técnico · proposta para VVP futuro.

### 5.1 · Estrutura do checklist V1

7 grupos de itens · derivados das 4 perguntas canônicas do DCV-V1 §1 + auditabilidade técnica:

#### Grupo A · Estrutura do upload
- [ ] As duas bases foram lidas corretamente (estrutura A ou B identificada · abas escolhidas · linhas/colunas detectadas)
- [ ] Os rótulos amigáveis ({origem_ux} e {comparado_ux}) aparecem em todas as superfícies (Resumo · abas · cards)

#### Grupo B · Taxa de conciliação geral
- [ ] A Taxa de Conciliação está calculada corretamente · Resumo §2 mostra `{N conciliados} / {N processados} = {%}`
- [ ] A tabela de decomposição soma 100% e tem as 6 classes (incluindo zerados como linhas com `0`)
- [ ] Sub-linha de tolerância absorvida aparece quando há absorção · ausente quando não

#### Grupo C · Status da Ponte
- [ ] Resumo §4 mostra Status da Ponte com ícone correto (✅ Fecha ou ⚠️ Resíduo)
- [ ] Quando há resíduo · valor R$ na sub-linha bate com a soma dos resíduos por campo na Aba 5
- [ ] Aba 5 tem 1 sub-Ponte por campo comparado · cada uma com 7 linhas + status

#### Grupo D · Mapa de Conciliação (Aba 3)
- [ ] Aba 3 tem 1 linha por registro processado · contagem total bate com Resumo §2
- [ ] Coluna `Classificação` tem formato condicional Verde/Amarelo/Vermelho aplicado
- [ ] Filtro `Classificação = Divergente por valor` mostra exatamente N linhas onde N bate com Resumo §2

#### Grupo E · Análise Analítica (Aba 4)
- [ ] Aba 4 tem 1 linha por registro · idêntico à Aba 3
- [ ] Para cada campo comparado · há 4 colunas (Valor Origem · Valor Comparado · Diferença · Status)
- [ ] Status por campo aplicado corretamente (registros `Só na Origem` têm Status `Sem valor no Comparado` em todos os campos)

#### Grupo F · Diagnóstico (Aba 6)
- [ ] Diagnóstico é a última aba (D-017 · invariante)
- [ ] Seção 1 (Configuração técnica) mostra paleta · modos de match · tolerâncias · estratégia de nulos
- [ ] Seções 2-4 (Tolerâncias · Duplicidades · Ambiguidades) mostram contagem que bate com a Síntese do Resumo §8
- [ ] Seção 5 (Warnings) lista os 3 warnings V1 com contagem · 0 ocorrências aparecem como linha "0 ocorrências · nenhuma a reportar"
- [ ] Seção 6 (Thresholds) mostra TEDs com status `Default` ou `Editado`

#### Grupo G · Resumo por Agrupador (Aba 2 · CONDICIONAL)
- [ ] Aba 2 existe quando agrupador executivo configurado · ausente quando não
- [ ] Quando presente · linha por valor único do agrupador · ordenação por |Diferença líquida| desc
- [ ] Para cada campo comparado · 4 colunas dedicadas (Soma Origem · Soma Comparado · Diferença líquida · Σ |Diferença|)

### 5.2 · Aplicação operacional (parqueada para VVP)

A versão **operacional definitiva** do checklist user-facing acima · com:

- Texto definitivo de cada item (sem placeholders)
- Microcopy de "✅ aprovado" · "❌ ajustar" · "🔄 inconclusivo · investigar"
- Critério de aprovação global da visão (% mínimo · todos obrigatórios · etc.)

será produzida em sessão "Definição operacional VVP" · executada após Família A completa em VVC (V1 · V11 · V2 retroativo todos validados em VVC). Esta sessão produzirá o protocolo VVP e o checklist V1 definitivo.

Até VVP existir · VV-V1 opera com checklist técnico derivado mecanicamente de `casos_esperados.yaml` (padrão D-148 · D-162) · modalidade C mista (D-156).

### 5.3 · Tradução técnico → user-facing aplicada

O esqueleto acima já consome:
- Bloco 3 estendido (6 classificações V1 · §2.2)
- Bloco 6 estendido (3 warnings V1 · §2.6)
- Bloco 10 (Unidades canônicas · §3.8)
- Pares Origem/Comparado com substituição amigável (§2.1)

Itens técnicos que **não** podem aparecer no checklist user-facing (lista negativa Bloco 7 · D-179):
- Códigos `W-V1-TOL`, `W-V1-DUP`, `W-V1-AMB` (substituídos por microcopy do Bloco 6)
- Enums caps `CONCILIADO`, `DIVERGENTE_VALOR` (substituídos por user-facing do Bloco 3)
- Códigos `B-V1-XXX` (não aparecem em checklist · só em logs)
- Identificadores Pydantic literais
- Fontes monoespaçadas em área executiva

---

## 6 · O que é V1-específico · catálogo para ALINHA-Auditoria-pós-V11

Lista do que é genuinamente novo em V1 · candidato a generalização para vocabulário transversal Família A em ALINHA-Auditoria-pós-V11 (D-204 cláusula B). **Cataloga · não promove agora.**

| # | Item | Promoção candidata para |
|---|---|---|
| 1 | 6 classes de classificação estrutural V1 | Vocabulário bilingue Bloco 3 estendido (já feito nesta P-V1 · §2.2) |
| 2 | Coluna "Classificação" como filtro primário em aba tabular (Mapa) | Bloco 11 NOVO do vocabulário bilingue (candidato) · padrão "classificação como coluna em aba tabular com formato condicional semáforo" · pode aplicar V11 |
| 3 | Status binário com sub-linha de ação (Status da Ponte) | Bloco 11 NOVO (candidato) · padrão "Status binário com sub-linha de ação" · pode ter análogos V4/V11 |
| 4 | Aba "Ponte de Conciliação" bespoke · decomposição vertical | V1-específico genuíno · V11 não terá Ponte (decomposição diferente · D-051) · não candidato a transversal |
| 5 | Distinção Mapa × Análise Analítica · 2 abas tabulares com grão por coluna diferente | Padrão arquitetural · candidato a Família A · aplica V11 |
| 6 | 6 abas (vs 4 V2) · estrutura macro diferente | V1-específico operacional (P-V1-10 do DCV) · V11 pode aproximar mas estrutura própria · não candidato direto |
| 7 | Leitura Qualitativa mais longa (cobre 6 classes + Status Ponte) | Específico V1 · paralelo V2 mas distinto · não candidato direto |
| 8 | Sub-blocos por entidade configurável em aba bespoke (Ponte por campo) | Padrão arquitetural · candidato Família A com análogo "Composição por dimensão" V4 |

A absorção formal acontece em ALINHA-Auditoria-pós-V11 · sessão obrigatória pós-fechamento da V11 (D-204 cláusula B · 2ª aplicação · ALINHA-Lições-Família-A foi a 1ª retroativa para V2). Promoções identificadas viram extensões ao `vocabulario_bilingue.md` v4.

---

## 7 · Ganchos para implementação downstream

Esta seção declara o que P-V1 deixa **vinculante** para os artefatos seguintes do ciclo (S-V1 · B-V1 condicional · V-V1 · A-V1 · VV-V1).

### 7.1 · Para S-V1 (Spec técnica · próximo bloco)

S-V1 deve formalizar em contratos Pydantic:

- **Enum `ClassificacaoRegistroV1`** com 6 valores (CONCILIADO · DIVERGENTE_VALOR · SO_ORIGEM · SO_COMPARADO · DIVERGENCIA_DUPLICIDADE · DIVERGENCIA_AMBIGUIDADE) · alinhado com Seção 2.2
- **Enum `StatusCampoV1`** com 6 valores (IGUAL · DENTRO_TOLERANCIA · DIVERGENTE · SEM_VALOR_ORIGEM · SEM_VALOR_COMPARADO · SEM_VALOR_AMBOS) · alinhado com Seção 2.5
- **Contrato `CampoComparadoV1`** com campos: `nome_origem`, `nome_comparado`, `nome_analitico`, `tipo_logico`, `unidade` (8 valores), `tolerancia` (com unidade herdada)
- **Contrato `AgrupadorMatchV1`** com campos: `nome_origem`, `nome_comparado`, `rotulo_analitico`, `modo_match` (4 valores · Exato · Contém · Inicia com · Termina com)
- **Contrato `ConciliacaoV1Result`** com saída completa · campos com `unidade` declarada (Seção 3.8.2)
- **3 warnings catalogados em `casos_esperados.yaml`** (entrada V1 · em B-V1 condicional ou na criação direta) com microcopy do Bloco 6 estendido (Seção 2.6)
- **Bloqueios canônicos** · catálogo numerado análogo ao da V2 (lista da Seção 4.7)
- **Wireframe funcional** consumindo as 4 etapas + Revisão da Seção 2.7
- **Wireframe HTML (família A · D-149)** representando o app

### 7.2 · Para B-V1 (Base sintética · condicional D-147)

Default · dispensada (V1 consome `base_fundacao.xlsx` via `base_v1_cliente.xlsx`). Decisão final em S-V1 quando contrato Pydantic estabilizar e `casos_esperados.yaml` ganhar entrada V1.

### 7.3 · Para V-V1 (motor `visao_v1.py`)

Motor consome `vocabulario_bilingue.md` v3 (com extensão Bloco 3 desta P-V1) e produz `ConciliacaoV1Result` com `unidade` declarada por campo. Aplicação canônica de C.D8 (D-190) · zero código de formatação no motor · só dados + unidade.

### 7.4 · Para A-V1 (app `app_v1.py`)

App consome P-V1 inteira (microcopy literal da Seção 4 · arquitetura de abas da Seção 3 · paleta da Seção 1) + S-V1 (contratos) + V-V1 (motor) + F-APRESENT (capabilities 1-11). Sessão Claude Code dedicada · gate duplo D-174 · Camada 1 mecânica + Camada 2 visual.

**Mockup-V1 (`MOCKUP_V1_alpha2.md` · D-208) é referência visual canônica** · prompt Claude Code da A-V1 anexa P-V1 + Mockup-V1 + S-V1 + DCV-V1.

### 7.5 · Para VV-V1 (Validação Visual Construtora)

Modalidade C mista (D-156) · Arquiteto presente · Usuária opera o app com `base_v1_cliente.xlsx` · marca checklist técnico derivado do YAML em ✅/❌. Esqueleto user-facing da Seção 5 acima é referência paralela · não opera ainda (VVP parqueada).

---

## 8 · Pendências P-V1-PROD-NN

**Zero pendências de produto abertas nesta P-V1.**

As 8 pendências P-α.3 do mockup foram **absorvidas como decididas** com defaults canônicos (declaração da Usuária em 26/04/2026 noite · Caminho A do mockup · esta sessão de produção P-V1 confirmou a absorção sem reabrir). Detalhamento das absorções:

| Pendência | Default canônico absorvido | Onde aparece |
|---|---|---|
| P-α.3-01 · Microcopy banner Seção 4 | `Status da Ponte` (curto) | §3.2.4 + §2.3 |
| P-α.3-02 · Ícone de status | Caractere Unicode (✅ ⚠️) com cor da paleta · não emoji bruto | §1.3 + §2.3 |
| P-α.3-03 · Rótulo Só na Origem vs Saiu do Origem | `Saiu do {origem_ux}` quando rótulo amigável · `Só na Origem` quando vazio | §2.2 |
| P-α.3-04 · Aba 4 TotalsRow | Desativada por default · grão registro·campo | §3.5 + §3.9 |
| P-α.3-05 · Ordem das 6 seções da Aba 6 | Configuração técnica primeiro | §3.7 |
| P-α.3-06 · Leitura qualitativa cita agrupador | Cita o de maior peso quando ≥ 70% concentração | §3.2.10 |
| P-α.3-07 · Mapa com 0 divergentes | Mantém todas as linhas conciliadas · auditabilidade > economia visual | §3.4 |
| P-α.3-08 · Cabeçalho identificador linhas | 3 linhas mínimo · 4 com T-MODELO | §3.2.1 |

---

## 9 · Status e aprovação

**Status:** aguardando aprovação da Usuária.

**Aprovação destrava:** S-V1 · próximo bloco do ciclo de 6 quadrados da V1.

**Após aprovação:**

1. P-V1 vira `/specs/produto/p_v1.md` (canônico)
2. `vocabulario_bilingue.md` v4 absorve extensões: Bloco 3 estendido (6 classificações V1) · Bloco 6 estendido (3 warnings V1)
3. Planilha aba 2 · 1º quadrado da V1 vira ✅ (`✅⬜⬜⬜⬜⬜`)
4. CONTEXT v3.5 ganha referência a P-V1 como 1ª P-VN sob método novo aplicado a visão nova (P-V2 retroativo foi aplicado a visão existente)
5. DECISIONS ganha D-209 · sumário da P-V1 e absorções (canon de transversais Família A pendente até ALINHA-Auditoria-pós-V11)
6. Sessão S-V1 abre · 2ª aplicação real do método novo da Família A após V2 retroativa

---

## 10 · Referências

- **DCV-V1:** `/specs/dcv/dcv_v1.md` · 13 pendências fechadas · 4 perguntas canônicas
- **Mockup-V1:** `MOCKUP_V1_alpha2.md` · 13 seções · 8 P-α.3 absorvidas (D-208)
- **Vocabulário bilingue:** `/specs/vocabulario_bilingue.md` v3 · 10 blocos
- **CONTEXT v3.5:** §15.11 (convenções P-VN) · §15 (ciclo de 6 artefatos) · §13 (padrões estruturais de produto) · §17 (cláusulas anti-vazamento) · §18 (princípios consolidados Família A)
- **DECISIONS canônicas consumidas:**
  - D-158 · artefato P-VN · ciclo de 6 artefatos
  - D-160 · vocabulário bilingue · zero vazamento técnico
  - D-161 · C.D6 · DDU · default declarado universal
  - D-164 · 4 paletas executivas canônicas
  - D-165 · Diagnóstico em 6 seções · última aba
  - D-166 · contrato de unidade por campo
  - D-168 · Azul executivo é default universal
  - D-179 · Bloco 9 · lista negativa expandida
  - D-185 · padrão 3 fases (informa S-V1 · não esta P-V1)
  - D-190 / D-194 / D-205 · contrato de unidade · capability 11 promovida
  - D-200 a D-207 · ALINHA-Lições-Família-A · 4 princípios canônicos · Cláusulas anti-vazamento · Refactor Dirigido (informa governança · não esta P-V1)
  - D-203 / D-204 cláusula A · gate Mockup Excel-alvo
  - D-208 · Mockup-V1 aprovado
- **F-APRESENT capabilities consumidas:** 1 (paletas) · 2 (vocabulário) · 3 (ListObject Excel) · 4 (Diagnóstico narrativo) · 5 (formatação BR) · 7 (resumo executivo prosa) · 8 (cards) · 9 (badges semânticos) · 10 (Diagnóstico 6 seções) · 11 (formato adaptativo por unidade · D-205)
- **Spec V2 como precedente:** `/specs/spec_v2.md` v1.1 · paralelo aplicado · estrutura adaptada à natureza dual e às 6 abas
- **Pegada V2 herdada:** Preâmbulo deste documento

---

*Esta P-V1 é fonte autoritativa de paleta · vocabulário · arquitetura de abas · contrato de unidade · microcopy e checklist user-facing da V1. A partir de sua aprovação, nenhuma decisão de produto da V1 pode ser alterada sem nova decisão formal registrada em DECISIONS.md. Implementações downstream (S-V1, V-V1, A-V1) consomem este documento como referência canônica.*
