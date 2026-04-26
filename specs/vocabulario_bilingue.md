# vocabulario_bilingue.md — TabloFlow

Tabela canônica transversal de vocabulário bilingue (técnico canônico ↔ user-facing) do TabloFlow. Consumida por toda P-VN (Spec de Produto · D-158) e aplicada em produção pelo subsistema F-APRESENT (capability 2 · D-159).

**Versão:** v4 · 26/04/2026 noite · estendida em P-V1 (D-209) com 6 classificações V1 (Bloco 3) e 3 warnings V1 (Bloco 6).
**Escopo v4:** Família A (V2 retroativo + V1 com método novo + V11 pendente) + base transversal universal + extensões P-V2 e P-V1.
**Mudanças v3 → v4:**
- Bloco 3 estendido · sub-bloco 3.1 com 6 classificações V1 (Conciliado · Divergente por valor · Saiu do/Só na Origem · Apareceu no/Só no Comparado · Divergência por duplicidade · Divergência por ambiguidade) + função canônica `formatar_classificacao_v1` em F-APRESENT capability 2
- Bloco 6 estendido · sub-bloco 6.1 com 3 warnings V1 (W-V1-TOL · W-V1-DUP · W-V1-AMB) com microcopy padrão "WARNING · {mensagem} · ação sugerida: {ação}"

**Mudanças v2 → v3:** Bloco 9 NOVO (lista negativa expandida + rótulos canônicos · D-179) · Bloco 10 NOVO (Unidades canônicas · D-190 · C.D8).
**Mudanças v1 → v2:**
- Bloco 1 estendido · convenção "Comparar de"/"Comparar com" como par universal Família A
- Bloco 3 estendido · regra de substituição dinâmica de classificações com rótulos amigáveis
- Bloco 8 NOVO · exibição canônica de valores ausentes (`None`)

**Expansão futura:** cada P-VN estende com termos visão-específicos em sua Seção 2. Termos comuns a 2+ visões são consolidados na próxima ALINHA. **3 candidatos a Bloco 11** catalogados em P-V1 §6 ("Status binário com sub-linha de ação" · "Classificação como coluna em aba tabular com semáforo" · "Sub-blocos por entidade configurável") permanecem **parqueados** · promoção avaliada em ALINHA-Auditoria-pós-V11 (D-204 cláusula B).

---

## 1 · Princípio

Toda superfície visível ao cliente (app · Excel · checklist user-facing · microcopy de erro) usa **exclusivamente** vocabulário user-facing declarado nesta tabela. Vocabulário técnico canônico preserva-se em Specs, contratos Pydantic, testes, logs, DECISIONS, código. Vocabulário técnico **nunca** atravessa a fronteira para superfície visível ao cliente.

**Regra de conflito:** se P-VN e esta tabela divergirem sobre um termo · tabela prevalece · P-VN ajusta ou justifica extensão em sua Seção 2 (D-160).

**Regra de expansão:** termo novo em P-VN passa a ser candidato a entrada transversal desta tabela quando se aplica a 2+ visões · Arquiteto consolida no kit δ de ALINHA seguinte.

---

## 2 · Bloco 1 · Stepper (Família A · 4 etapas + Revisão · D-167)

Rótulos de navegação entre etapas do app. Código técnico `E1`-`E5` nunca aparece visível.

| Código técnico | User-facing (padrão Família A) |
|---|---|
| E1 | 1 · Escolher arquivo |
| E2 | 2 · Reconhecer estrutura |
| E3 | 3 · Configurar análise |
| E4 | 4 · Agrupar |
| E5 | Revisar e executar |

**Mudança v1 → v2:** stepper de Família A passou de "5 etapas" canônico (v1) para "4 etapas + Revisão" (v2). Decisão emergente em P-V2 retroativo (D-167) alinha o stepper com o motor real (motor V2 atual não pré-detecta casos estruturais antes da E5 · bloco intermediário condicional parqueado como P-V2-Evo-01 · D-154). Quando bloco intermediário for implementado em evolução futura, stepper ganha 5ª etapa e Revisão vira 6ª · refinamento gera P-V*-Evo, não reescreve esta tabela.

### Bloco 1.1 · Pares de comparação Família A (V2 · V1 · V11)

Pares user-facing universais de Família A para nomeação dos dois lados da comparação:

| Código técnico | User-facing widget E2 | User-facing após escolha |
|---|---|---|
| `Origem` | "Comparar de" (label do widget) | "Origem" (com rótulo amigável editável ao lado) |
| `Comparado` | "Comparar com" (label do widget) | "Comparado" (com rótulo amigável editável ao lado) |

**Substituição por rótulos amigáveis:** quando Usuária declara rótulos amigáveis (ex: Origem = "Orçado" · Comparado = "Realizado"), esses rótulos viram referência canônica de exibição em todo app e Excel. Termos técnicos "Origem" e "Comparado" só aparecem entre parênteses como subtítulo se rótulos amigáveis em branco. Aplicação reforçada de C.5.

---

## 3 · Bloco 2 · Modos da base

| Código técnico | User-facing |
|---|---|
| TRANSACIONAL | Base transacional (uma linha por lançamento) |
| PRE_AGREGADO | Base pré-agregada (uma linha por combinação) |
| INDIVIDUAL | Granularidade individual |
| CONSOLIDADA | Granularidade por chave |

---

## 4 · Bloco 3 · Classificações estruturais

### Bloco 3.0 · V2 (par universal Família A · base do padrão)

Enums do contrato Pydantic V2Result · traduzidos em superfície cliente.

| Código técnico | User-facing (sem rótulo amigável) | User-facing (com rótulo amigável) |
|---|---|---|
| PRESENTE_AMBOS | "Presente nos dois lados" | "Presente nos dois lados" (omitido na exibição · caso normal) |
| AUSENTE_ORIGEM | "Apareceu no Comparado" | "Apareceu no [rótulo Comparado]" (ex: "Apareceu no Realizado") |
| AUSENTE_COMPARADO | "Saiu da Origem" | "Saiu do [rótulo Origem]" (ex: "Saiu do Orçado") |
| NULO_ORIGEM | "Sem valor na Origem" | "Sem valor no [rótulo Origem]" (ex: "Sem valor no Orçado") |
| NULO_COMPARADO | "Sem valor no Comparado" | "Sem valor no [rótulo Comparado]" (ex: "Sem valor no Realizado") |
| NULO_AMBOS | "Sem valor nos dois lados" | "Sem valor nos dois lados" |

**Mudança v1 → v2:** regra de substituição dinâmica formalizada. F-APRESENT capability 2 (rótulos user-facing universais · D-160) consome `comparacao_realizada.origem_rotulo_ux` e `comparado_rotulo_ux` para fazer a substituição. Aplicação canônica para Família A inteira (V2 retroativo · V1 com adaptação T-DUAL · V11 com adaptação por aderência).

### Bloco 3.1 · V1 · 6 classificações estruturais (NOVO em v4 · D-209)

Enums do contrato Pydantic `ConciliacaoV1Result.classificacao_registro` · traduzidos em superfície cliente. Padrão paralelo ao Bloco 3.0 · adaptado à natureza de conciliação dual (T-DUAL · 2 bases lógicas).

| Código técnico | User-facing (sem rótulo amigável) | User-facing (com rótulo amigável) | Cor da paleta |
|---|---|---|---|
| `CONCILIADO` | "Conciliado" | "Conciliado" (rótulo igual · classe positiva) | Verde da paleta |
| `DIVERGENTE_VALOR` | "Divergente por valor" | "Divergente por valor" (rótulo igual) | Amarelo/laranja da paleta |
| `SO_ORIGEM` | "Só na Origem" | "Saiu do [rótulo Origem]" (ex: "Saiu do Razão") | Vermelho da paleta |
| `SO_COMPARADO` | "Só no Comparado" | "Apareceu no [rótulo Comparado]" (ex: "Apareceu no Balancete") | Vermelho da paleta |
| `DIVERGENCIA_DUPLICIDADE` | "Divergência por duplicidade" | "Divergência por duplicidade" (rótulo igual) | Amarelo/laranja da paleta |
| `DIVERGENCIA_AMBIGUIDADE` | "Divergência por ambiguidade de match" | "Divergência por ambiguidade de match" (rótulo igual) | Amarelo/laranja da paleta |

**Regra de despacho condicional** (P-V1 §2.2 · F-APRESENT capability 2):
- Quando rótulo amigável **declarado** (Origem ≠ "Origem" · Comparado ≠ "Comparado"): `SO_ORIGEM` e `SO_COMPARADO` usam formulação direcional **"Saiu do" / "Apareceu no"** · alinha com Bloco 3.0
- Quando rótulo amigável **vazio** (defaults técnicos): usa formulação genérica **"Só na Origem" / "Só no Comparado"** · evita "Saiu do Origem" que soa estranho

Função canônica em F-APRESENT capability 2:

```python
def formatar_classificacao_v1(
    classificacao: Literal["CONCILIADO", "DIVERGENTE_VALOR", "SO_ORIGEM",
                          "SO_COMPARADO", "DIVERGENCIA_DUPLICIDADE",
                          "DIVERGENCIA_AMBIGUIDADE"],
    origem_ux: str,      # "Origem" se vazio, ou rótulo amigável declarado
    comparado_ux: str,   # "Comparado" se vazio, ou rótulo amigável declarado
    rotulo_amigavel_declarado: bool  # True se Usuária editou rótulo
) -> str:
    # Despacho determinístico conforme tabela acima
```

**Sub-classificação "Conciliado com tolerância absorvida"** · não é uma 7ª classe · é flag visual sobre `CONCILIADO`. Microcopy de exibição em P-V1 §2.2.

### Bloco 3.2 · V1 · 6 status por campo (Aba 4 · Análise Analítica)

Enum `StatusCampoV1` · usado na coluna `Status · {campo}` da Aba 4. Distinção em relação ao Bloco 3.1: classificação é por **registro** · status é por **campo dentro do registro**.

| Código técnico | User-facing (sem rótulo amigável) | User-facing (com rótulo amigável) | Cor da paleta |
|---|---|---|---|
| `IGUAL` | "Igual" | "Igual" | Verde |
| `DENTRO_TOLERANCIA` | "Dentro da tolerância" | "Dentro da tolerância" | Verde |
| `DIVERGENTE` | "Divergente" | "Divergente" | Amarelo |
| `SEM_VALOR_ORIGEM` | "Sem valor na Origem" | "Sem valor no [rótulo Origem]" | Cinza |
| `SEM_VALOR_COMPARADO` | "Sem valor no Comparado" | "Sem valor no [rótulo Comparado]" | Cinza |
| `SEM_VALOR_AMBOS` | "Sem valor nos dois lados" | "Sem valor nos dois lados" | Cinza |

Substituição dinâmica em SEM_VALOR_ORIGEM/SEM_VALOR_COMPARADO idêntica à regra do Bloco 3.0 (NULO_ORIGEM/NULO_COMPARADO).

Análogos em V11 (aderência contextual) ganham entradas próprias em P-V11 · consome este padrão como modelo (Bloco 3.0 + 3.1 + 3.2 conjunto · 12 classificações Família A consolidadas pós-V1).

---

## 5 · Bloco 4 · Tipos de campo (taxonomia D-025)

| Código técnico | User-facing |
|---|---|
| NUMERICO_ADITIVO | Valor somável (receita · quantidade) |
| NUMERICO_RELATIVO | Valor percentual ou taxa |
| NUMERICO_NAO_ADITIVO | Indicador não somável (preço unitário · média) |
| CATEGORICO | Categoria ou rótulo |
| BOOLEANO | Sim/Não |
| ESTADO_SITUACAO | Categoria ou rótulo (estado/situação) |

---

## 6 · Bloco 5 · Thresholds (TED · C.D2)

Labels da sidebar global (D-153) consomem este bloco.

| Código técnico | User-facing |
|---|---|
| limiar_estabilidade_pct | Limite de estabilidade (variações menores são "estável") |
| limite_variacao_extrema | Limite de variação extrema (variações maiores são destacadas) |
| limiar_nulo_massivo_pct | Limite de nulos massivos (acima sinaliza qualidade deteriorada) |
| limite_valores_discriminador_alerta | Limite de valores na coluna de comparação (acima sugere filtragem) |

Unidade explícita obrigatória (D-166): percentual exibido como `1%` · não `0.01`.

---

## 7 · Bloco 6 · Warnings universais (padrão de nomeação user-facing)

### Bloco 6.0 · Padrão universal

Warnings seguem padrão técnico `W-V*-CATEGORIA-ESPECIFICADOR` · exibidos em superfície cliente via tradução.

| Padrão técnico | Padrão user-facing |
|---|---|
| W-V*-AUSENCIA-* | "Ausência detectada em [detalhe]" |
| W-V*-NULO-* | "Valor ausente em [detalhe]" |
| AJUSTE_LEVE-* | "Ajuste automático aplicado · [detalhe]" |
| DECISAO_USUARIO-* | "Decisão do usuário necessária · [detalhe]" |

Expansão por visão: cada P-VN declara warnings V-específicos na sua Seção 2 aplicando o padrão de tradução acima.

**Padrão de microcopy expandido** (P-V1 · D-209): `WARNING · {mensagem técnica} · ação sugerida: {ação}`. Warnings com 0 ocorrências aparecem na Seção 5 do Diagnóstico com texto "*W-V*-XXX · 0 ocorrências · nenhuma a reportar*" · auditabilidade preservada (princípio C.2 · ausência é informação).

### Bloco 6.1 · V1 · 3 warnings catalogados (NOVO em v4 · D-209)

Warnings catalogados no contrato `ConciliacaoV1Result.warnings` · canonicamente registrados em `casos_esperados.yaml` (entrada V1 · a ser criada em B-V1 condicional ou na criação direta · S-V1).

| Código técnico | Microcopy user-facing (Diagnóstico §5) | Quando dispara |
|---|---|---|
| `W-V1-TOL` | "Tolerância absorveu diferenças · {N} registro(s) classificado(s) como Conciliado tinham diferença absoluta não-zero dentro da tolerância configurada · ação sugerida: revisar tolerância na Aba 6 · §6 Thresholds" | ≥ 1 registro conciliado com diferença absorvida |
| `W-V1-DUP` | "Duplicidade em chaves · {N} chave(s) duplicada(s) na [origem_ux] ou [comparado_ux] · ação sugerida: revisar dado de entrada ou consolidar antes do upload" | ≥ 1 chave duplicada em qualquer lado |
| `W-V1-AMB` | "Ambiguidade em match não-exato · {N} chave(s) produzindo múltiplos candidatos com modo de match Contém / Inicia com / Termina com · ação sugerida: revisar critério de match ou simplificar chave" | ≥ 1 chave com múltiplos candidatos no modo configurado |

**Substituição dinâmica:** `[origem_ux]` e `[comparado_ux]` substituídos por rótulos amigáveis quando declarados (idêntico à regra Bloco 3 · F-APRESENT capability 2).

**Warnings herdados do motor (Fundação):** se houver no processamento V1 (ex: `W-B01` · inferência de boolean disfarçado · D-008) · listados após os 3 V1 na Seção 5 do Diagnóstico.

---

## 8 · Bloco 7 · Termos proibidos em superfície cliente (lista negativa)

Lista de padrões que **nunca** podem aparecer em superfície visível ao cliente (app · Excel · checklist · mensagens). Autoridade equivalente à lista positiva. Violação = bug.

### 8.1 · Nomes de atributo Python literais

Qualquer identificador em `snake_case` que seja nome de atributo de contrato Pydantic ou função interna do motor. **Proibidos:**

- `campo_analisado`
- `origem_rotulo_ux` · `origem_rotulo_tecnico`
- `comparado_rotulo_ux` · `comparado_rotulo_tecnico`
- `limiar_estabilidade_pct`
- `limite_variacao_extrema`
- `tipo_estrutural`
- `classificacao_estrutural` · `classificacao_semantica`
- `chave_agrupadores` · `valor_origem` · `valor_comparado` · `variacao_percentual`
- Qualquer outro nome de atributo interno

### 8.2 · Enums em caps

Strings em maiúsculas com underscore que são valores de enum do contrato:

- `POR_COLUNAS` · `POR_LINHAS`
- `PRESENTE_AMBOS` · `AUSENTE_ORIGEM` · `AUSENTE_COMPARADO` · `NULO_ORIGEM` · `NULO_COMPARADO` · `NULO_AMBOS`
- `TRANSACIONAL` · `PRE_AGREGADO`
- `NUMERICO_ADITIVO` · `NUMERICO_RELATIVO` · `NUMERICO_NAO_ADITIVO` · `ESTADO_SITUACAO`
- `MEDIA_SIMPLES` · `MEDIA_PONDERADA` · `NAO_CONSOLIDAR`
- `MATRIZ_COLORIDA`
- Qualquer outro enum

### 8.3 · Códigos internos do projeto

- `D-XXX` (ex: `D-021` · `D-167`)
- `P-V*-Evo-NN` (ex: `P-V2-Evo-01`)
- `OBS-VV-V*-NN`
- Códigos de transversais (`T-AGRUPA` · `T-PIVOT` · `T-SEMA` · etc.)
- Códigos de subsistemas (`F-MOT` · `F-TRANS` · `F-EXP` · `F-BASE` · `F-APRESENT`)
- Códigos de bloqueio (`B-V*-*`)
- Códigos de warning (`W-V*-*`)
- Códigos de princípio (`C.D6` · `DDU`)

### 8.4 · Serializações técnicas cruas

- `datetime.datetime(2026, 4, 23, 14, 32, 11)` · serializado cru
- Python dict serializado como string (`{'visao': 'V2', 'data_execucao': ...}`)
- Tipos Pydantic em representação debug (`<V2Result object at 0x7f...>`)

### 8.5 · Fração decimal apresentada como percentual

`0.0109` ou `0.01` sem conversão e sem símbolo `%`. Sempre exibir como `1,09%` ou `1%` com símbolo (D-166 · contrato de unidade · F-APRESENT capability 5 faz a conversão).

### 8.6 · Fonte monoespaçada em área executiva

Resumo Executivo · Coração Visual · Base Analítica usam tipografia executiva da paleta (capability 9 de F-APRESENT P1). Monoespaçada permitida apenas no Diagnóstico quando referência técnica já traduzida.

---

## 9 · Bloco 8 · Exibição canônica de valores ausentes (NOVO em v2)

Decisão consolidada em P-V2 retroativo (D-167) · candidato a aplicação cross-visão para todas as 11 visões.

**Padrão único de exibição:**

| Origem do `None` no contrato | Exibição user-facing (cross-visão) | Microcopy contextual (quando origem é semanticamente importante) |
|---|---|---|
| Ausência estrutural (chave existe em um lado · não no outro) | `—` | "— (não consta)" no Diagnóstico |
| Nulo no campo (chave existe nos dois lados · valor numérico ausente) | `—` | "— (sem valor)" no Diagnóstico |
| Cálculo impossível (ex: variação % com Origem=0 e Comparado≠0 · `W-V2-BZ`) | `—` | "— (não calculável)" quando relevante |

**Proibições reforçadas:** nunca exibir `None`, `null`, `NaN`, `nan`, `(null)`, string vazia, `0` (quando significa ausência), `-100%` (quando significa cálculo impossível). Inventar valor onde não há dado viola C.5 (D-022 · D-023 reforçados).

**Aplicação operacional:** F-APRESENT capability 4 (formatação monetária BR) e capability 5 (formatação percentual) tratam `None` como `—` por default. Capability 10 (diagnóstico narrativo · P1) adiciona microcopy contextual quando a origem do `None` carrega informação relevante.

---
## Bloco 9 · Lista negativa expandida + rótulos de semântica (D-179 · NOVO · 24/04/2026)
Esta seção formaliza 9 categorias de vazamento técnico proibido em superfícies user-facing (Excel + app Streamlit) e os rótulos canônicos da semântica de campo (semantica_campo).

9.1 · Lista negativa expandida · 9 categorias proibidas
Cada categoria abaixo é proibida em superfícies user-facing. F-APRESENT capability 2 (traduzir) deve detectar e bloquear · com warning estrutural se vazamento detectado.
#Categoria proibidaExemplo proibidoTradução obrigatória / ação1Snake_case técnicoCentro_Custo · tipo_campo · valor_origemTradução para forma legível (Centro de Custo · Tipo de medida · Valor (origem)) via vocabulário canônico2Códigos de avisos/warningsV2-A01 · W-V2-PAGREG-DUP · T-SEMA · MBO-NFicam apenas em log técnico · nunca em superfície user-facing3Identificadores Pydantic literaisMAIOR_MELHOR · NUMERICO_ADITIVO · POSITIVO · PRESENTE_AMBOSTradução para rótulo legível (ver Bloco 9.2 abaixo + tabelas existentes)4dict serializado / JSON cru{'campo_x': 100, 'campo_y': 200}Renderização tabular ou prosa · nunca dict cru visível5Enums caps sem traduçãoSOMA · MEDIA · MEDIA_PONDERADATradução para forma legível (Soma · Média · Média ponderada)6Valores nulos visíveisNULL · null · NaN · nan · (null) · NoneSempre — ou microcopy contextual (— (não consta) para ausência · — (sem valor) para nulo · — (não aplicável) para irrelevância)7Nomes em colchetes/parênteses técnicos[campo_x] · <valor> · (legacy_field)Removidos · sem decoração técnica8Frações cruas em vez de percentual0.03622154 em célula que devia mostrar variação %Sempre formatado como 3,62% (formato BR · F-APRESENT capability 5)9Aspas literais em texto user-facing"Receita Realizado" em label/títuloSem aspas em UI · aspas só quando o texto realmente é uma citação
Operacionalização:

F-APRESENT capability 2 ganha função validar_zero_vazamento(texto, contexto) → List[Vazamento] · usada em testes
Testes de F-APRESENT incluem matriz de 9 categorias × 4 superfícies (Excel · st.dataframe · st.markdown · st.metric)
Sessão F-APRESENT-cleanup (D-180) absorve esta extensão · capability 2 estendida lá


9.2 · Rótulos canônicos de semantica_campo (T-SEMA)
Tradução obrigatória dos 3 valores canônicos do contrato Pydantic ComparacaoV2.semantica_campo (Literal["MAIOR_MELHOR", "MENOR_MELHOR", "NEUTRO"]) para superfícies user-facing.
Valor canônico (contrato)Rótulo user-facing (rádio na Etapa 3)Rótulo curto (resumo / Diagnóstico)MAIOR_MELHORSubir é bom (maior é melhor)Subir é bomMENOR_MELHORSubir é ruim (menor é melhor)Subir é ruimNEUTRONeutro · sem viésNeutro
Pergunta canônica acima do rádio: "Subir é bom, ruim ou neutro?"

9.3 · Rótulos canônicos de classificacao_semantica (T-SEMA · saída do motor)
Quando o motor classifica uma variação semanticamente (T-SEMA contrato 1 · spec_fundacao §D.3), os 4 valores canônicos do enum têm rótulo user-facing único cross-visão.
Valor canônicoRótulo user-facing (badge / célula)Cor associada (paleta-dependente)POSITIVOMelhorouVerde da paletaNEGATIVOPiorouVermelho da paletaNEUTROEstávelCinza/azul-claro da paletaNAO_APLICAVELNão aplicávelSem fill (texto cinza)
Rótulos derivados da tabela canônica T-SEMA contrato 1 (spec_fundacao §D.3):
Estrutural ↓ × Semântica →MAIOR_MELHORMENOR_MELHORNEUTROAUMENTOUMelhorou (verde)Piorou (vermelho)Aumentou (cinza)REDUZIUPiorou (vermelho)Melhorou (verde)Reduziu (cinza)ESTAVELEstávelEstávelEstávelNAO_APLICAVELNão aplicávelNão aplicávelNão aplicável

9.4 · Rótulos canônicos de tipo_campo (Etapa 3 · pergunta "Como esse campo se comporta?")
Valor canônicoRótulo user-facing (rádio na Etapa 3)NUMERICO_ADITIVOValor somável (receita, custo, quantidade, volume)NUMERICO_RELATIVOValor percentual ou taxa (margem %, taxa, índice)NUMERICO_NAO_ADITIVOIndicador não somável (saldo, estoque, preço unitário)ESTADO_SITUACAOCategoria ou rótulo (status, classificação)

9.5 · Rótulos canônicos de regra_agregacao (T-AGRUPA · derivado de tipo_campo)
Valor canônicoRótulo user-facingSOMASomaMEDIAMédiaMAXIMOMáximoMINIMOMínimoCONTAGEMContagem

9.6 · Rótulos canônicos de metodo_consolidacao_relativo
Aplicável apenas a tipo_campo ∈ {NUMERICO_RELATIVO, NUMERICO_NAO_ADITIVO}.
Valor canônicoRótulo user-facingMEDIA_SIMPLESMédia simples (default declarado)MEDIA_PONDERADAMédia ponderada por outro campoNAO_CONSOLIDARNão consolidar (mostrar valor por linha)

Fim do Bloco 9. Total acrescentado: 6 sub-blocos (9.1 a 9.6) com 9 categorias proibidas + 4 tabelas de rótulos canônicos.

---

## 10 · Unidades canônicas (D-190 · C.D8)

Tabela canônica das 8 unidades aceitas pelo contrato `ComparacaoV2.unidade` (Sessão 8 · D-194) e equivalentes em V1/V11/restantes (após sessão de Promoção de Fundação · D-197).

### 10.1 · Tabela de unidades

| Valor canônico (contrato) | Rótulo user-facing (selectbox da Etapa 3) | Símbolo característico no Excel | Default inferido a partir de `tipo_campo` |
|---|---|---|---|
| MONETARIO_BRL | Reais (R$) | `R$` | NUMERICO_ADITIVO · NUMERICO_NAO_ADITIVO |
| PERCENTUAL | Percentual (%) | `%` ou `p.p` | NUMERICO_RELATIVO |
| QUANTIDADE | Quantidade absoluta | (número limpo) | (sem default · escolha manual) |
| TEMPO_DIAS | Tempo em dias | `dias` | (sem default · escolha manual) |
| TEMPO_HORAS | Tempo em horas | `h` | (sem default · escolha manual) |
| MULTIPLICADOR | Multiplicador (x) | `x` | (sem default · escolha manual) |
| RAZAO | Razão (decimal) | (4 casas decimais) | (sem default · escolha manual) |
| ADIMENSIONAL | Outro / sem unidade definida | (formato neutro) | ESTADO_SITUACAO |

Pergunta canônica acima do selectbox: **"Em qual unidade o campo é expresso?"**

### 10.2 · Rótulos canônicos das colunas Diferença e Variação por unidade

| Unidade | Rótulo coluna Diferença | Rótulo coluna Variação |
|---|---|---|
| MONETARIO_BRL | Diferença | Variação % |
| PERCENTUAL | **Variação absoluta (p.p)** | **Variação relativa (%)** |
| QUANTIDADE | Diferença | Variação % |
| TEMPO_DIAS | Diferença (dias) | Variação % |
| TEMPO_HORAS | Diferença (h) | Variação % |
| MULTIPLICADOR | Diferença | Variação % |
| RAZAO | Diferença | Variação % |
| ADIMENSIONAL | Diferença | Variação % |

**Razão da exceção PERCENTUAL:** quando o campo é percentual (margem · taxa · índice) · há 2 leituras matematicamente distintas e ambas são executivamente úteis: **absoluta** (margem subiu de 28,99% para 27,15% · isso é -1,84 pontos percentuais · interpretação aditiva) e **relativa** (margem caiu 6,36% relativa à margem original · interpretação multiplicativa). Cliente lendo "1,84%" sem distinção pode confundir absoluta com relativa · gerar decisão errada. Os 2 termos juntos eliminam ambiguidade.

### 10.3 · Rótulo dos cards "Total" no Resumo Executivo por unidade

| Unidade | Rótulo do card | Cálculo do valor exibido |
|---|---|---|
| MONETARIO_BRL | Total · {referência} | Soma dos valores presentes |
| PERCENTUAL | **Média · {referência}** | Média ponderada simples (soma / count_presente) |
| QUANTIDADE | Total · {referência} | Soma dos valores presentes |
| TEMPO_DIAS | Total · {referência} | Soma dos valores presentes |
| TEMPO_HORAS | Total · {referência} | Soma dos valores presentes |
| MULTIPLICADOR | Total · {referência} | Soma dos valores presentes |
| RAZAO | Total · {referência} | Soma dos valores presentes |
| ADIMENSIONAL | Total · {referência} | Soma dos valores presentes |

**Razão da exceção PERCENTUAL:** somar 30% + 25% + 28% = 83% não tem sentido analítico. Para campo percentual o cálculo executivo correto é a Média (não a soma) · e o rótulo precisa refletir essa escolha · daí "Média · {referência}" em vez de "Total · {referência}".

### 10.4 · Restrições semânticas declaradas

- **Saúde da comparação · coluna Δ total** · oculta para `unidade=PERCENTUAL`. Razão: somar Δ em p.p de várias linhas viola C.D3 (representação fiel do dado · soma de p.p não é unidade analiticamente válida).
- **Onde se concentra · coluna Δ** · para `unidade=PERCENTUAL` mostra **Δ médio** (média das diferenças individuais em p.p · faz sentido analítico) · para outras unidades mostra **Δ total** (soma).
- **Leitura qualitativa · valores entre parênteses dos casos** · omitidos para `unidade=PERCENTUAL` (mesma razão acima · soma de p.p não vai entre parênteses).

### 10.5 · Helpers de despacho por unidade (F-APRESENT · src/apresentacao/formatos.py · D-194)

Implementação V2-específica (Sessão 8 + 8.1) · candidata a promoção em capability genérica (D-197).

| Helper | Função |
|---|---|
| `number_format_valor(unidade)` | Number format Excel para valor base (origem · comparado · total) |
| `number_format_diferenca(unidade)` | Number format Excel para coluna Diferença (com lógica de sinal explícito + cor) |
| `number_format_variacao(unidade)` | Number format Excel para coluna Variação (sempre `0.00%` exceto ADIMENSIONAL/ESTADO_SITUACAO) |
| `rotulo_diferenca(unidade)` | Rótulo user-facing da coluna Diferença conforme tabela 10.2 |
| `rotulo_variacao(unidade)` | Rótulo user-facing da coluna Variação conforme tabela 10.2 |
| `label_total_card(unidade)` | "Média" para PERCENTUAL · "Total" para resto (tabela 10.3) |
| `valor_total_card(total_soma, count, unidade)` | Calcula valor exibido no card · média ponderada para PERCENTUAL · soma para resto |
| `valor_diferenca_para_celula(valor_raw, unidade)` | Multiplica por 100 quando PERCENTUAL · preserva valor para resto (resolução D-1 · D-195) |
| `formatar_valor_por_unidade(valor, unidade)` | Renderiza valor escalar como string user-facing por unidade (usado em narrativas) |

## 11 · Histórico de versões

- **v1** · 23/04/2026 · ALINHA-Descoberta-Camada-Produto (D-160) · 7 blocos · base Família A
- **v2 · 23/04/2026** · P-V2 retroativo (D-167) · 8 blocos · estende v1 com 3 termos consolidados da Família A:
  - Bloco 1 · stepper de "4 etapas + Revisão" + sub-bloco 1.1 com par "Comparar de"/"Comparar com"
  - Bloco 3 · regra de substituição dinâmica de classificações com rótulos amigáveis
  - Bloco 8 NOVO · exibição canônica de `None` como `—`
- **v3 · 25/04/2026** · ALINHA-Descoberta-Unidade (D-194) · 10 blocos · estende v2 com:
  - Bloco 9 NOVO · lista negativa expandida + rótulos canônicos (D-179) · 9 categorias proibidas + 4 tabelas de rótulos
  - Bloco 10 NOVO · Unidades canônicas (D-190 · C.D8) · 5 sub-blocos (10.1 a 10.5) · 8 valores de unidade · rótulos das colunas Diferença/Variação · rótulos dos cards Total/Média · restrições semânticas para PERCENTUAL · helpers de despacho em F-APRESENT
- **v4 · 26/04/2026 noite · este arquivo** · P-V1 (D-209) · 10 blocos (sem novo bloco · estende 2 existentes) · estende v3 com:
  - Bloco 3 estendido · sub-bloco 3.0 (V2 · base · preservado) · sub-bloco 3.1 NOVO (V1 · 6 classificações de registro com despacho condicional + função canônica `formatar_classificacao_v1`) · sub-bloco 3.2 NOVO (V1 · 6 status por campo da Aba 4)
  - Bloco 6 estendido · sub-bloco 6.0 (padrão universal · preservado · padrão de microcopy expandido com "ação sugerida") · sub-bloco 6.1 NOVO (V1 · 3 warnings catalogados W-V1-TOL · W-V1-DUP · W-V1-AMB)
  - **Não cria Bloco 11.** 3 candidatos a transversal Família A catalogados em P-V1 §6 ("Status binário com sub-linha de ação" · "Classificação como coluna em aba tabular com semáforo" · "Sub-blocos por entidade configurável") permanecem **parqueados** · promoção avaliada em ALINHA-Auditoria-pós-V11 (D-204 cláusula B). Disciplina de não promover transversais antes da auditoria de família é vinculante.

---

*Documento vivo · mantido pelo Arquiteto · atualizado em kit (D-033 ou D-170 leve) sempre que P-VN consolidar termos novos cross-visão.*
