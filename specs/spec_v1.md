# s_v1.md — Conciliação de Bases · Spec Técnica

**Visão:** V1 · Família A · Confronto entre universos · Conciliação de Bases
**Bloco:** S-V1 · 2º quadrado dos 6 do ciclo da V1 (D-158)
**Versão:** v2.0 · 26/04/2026 noite · pacote único · Caminho A · pós-correção de leiaute V2 e casos lógicos de upload
**Status:** **aguardando aprovação** da Usuária
**DCV consumido:** `/specs/dcv/dcv_v1.md` · aprovado 18/04/2026
**P-V1 consumida:** `/specs/produto/p_v1.md` · aprovado 26/04/2026 noite (D-209) · com 3 correções retroativas (D-212)
**Mockup consumido:** `MOCKUP_V1_alpha2.md` · aprovado 26/04/2026 noite (D-208)
**Vocabulário consumido:** `/specs/vocabulario_bilingue.md` v4 · 10 blocos
**Fundação consumida:** `spec_fundacao.md` · 5 subsistemas (G-FUND · F-MOT · F-TRANS · F-EXP · F-APRESENT capabilities 1-11)
**Precedente paralelo:** `app_v2.py` (estrutura canônica · suite 746/746 verde) + `/specs/spec_v2.md` v1.1

**Fonte autoritativa de:** contratos lógicos Pydantic da V1 · regras de cálculo · pipeline determinístico (2 ramos · ABAS_DISTINTAS / MESMA_ABA_EM_COLUNAS) · catálogo de bloqueios B-V1-* · catálogo de warnings W-V1-* · TED V1 · wireframe funcional textual · checklist VVC derivado.

**Regra de conflito (CONTEXT §5):** se P-V1 e S-V1 divergirem sobre vocabulário · microcopy · arquitetura de abas · contrato de unidade · paleta → P-V1 prevalece (com correções D-212 aplicadas). Se divergirem sobre contrato lógico · regra de cálculo · invariante matemático · wireframe funcional → S-V1 prevalece.

---

## Preâmbulo operacional

Esta S-V1 aplica os 3 requisitos D-130 integrais (visão analítica): `model_config` com `use_enum_values=False` · `Field(..., description=...)` em todo campo · método `.para_contexto_ia()` herdado de `VNResultBase` sem re-override (D-144 · V1 é analítica). Aplica os 7 padrões §13 (objetivo · fluxo · T-MODELO · view especializada · RE 6 Blocos · Coração Visual · Excel é produto · D-163) e os 8 derivados §9 Camada C (CPCO · TED · BAD · MBO · ECP · DDU · Motor primeiro · Unidade declarada). Estrutura canônica em 3 seções obrigatórias (CONTEXT §15.3) reforçada por checklist VVC derivado mecanicamente (§3.10 · D-148 · 5 templates).

**Decisões de produto fechadas nesta S-V1:**

- **Q1 (D-210)** · Campos PERCENTUAL omitidos da Ponte · nota explicativa fixa
- **Q2 (D-211)** · Épsilon da Ponte é TED editável por unidade global · 1 valor por unidade presente
- **Q3 (D-213)** · V1 tem 4 casos lógicos de upload (1·2·3·4) · sistema infere automaticamente do apontamento dos campos · não há radio "estrutura A/B"
- **D-212** · 3 correções retroativas em P-V1 catalogadas (TED em expander no topo · paleta no rodapé do RESULTADO · E4 contém só "Agrupadores executivos")

**O que esta S-V1 NÃO faz:**

- Não duplica arquitetura de abas do Excel (P-V1 §3 é fonte autoritativa)
- Não duplica microcopy do Excel (P-V1 §4 é fonte autoritativa)
- Não duplica contrato de unidade por campo do Excel (P-V1 §3.8)
- Não duplica catálogo de paletas (F-APRESENT capability 1)

S-V1 declara contratos Pydantic novos · regras de cálculo determinísticas · invariantes matemáticos · wireframe funcional textual com mapeamento literal para microcopy de P-V1 (com D-212 aplicada).

---

## Seção 1 · Contratos lógicos

### 1.1 · `ConciliacaoV1Result` — contrato principal

Contrato de saída do motor V1. Estende `VNResultBase` (Fundação · D-130). É o único contrato que `visao_v1.py` produz e que `app_v1.py` + `exportacao_v1.py` consomem.

```python
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field

class ConciliacaoV1Result(VNResultBase):
    """
    Resultado canônico da V1 · Conciliação de Bases.

    Produz leitura estruturada do confronto entre Origem e Comparado
    em 4 dimensões (taxa · concentração · registro a registro · ponte).

    Aplicação direta de C.5 (sistema preserva e classifica · não consolida)
    e C.D8 (toda comparação numérica declara unidade explícita).
    """
    model_config = ConfigDict(arbitrary_types_allowed=True, use_enum_values=False)

    visao: Literal["V1"] = Field(
        default="V1",
        description="Identificador fixo · V1 · única visão que produz este contrato"
    )
    conciliacao_realizada: ConciliacaoRealizadaV1 = Field(
        ...,
        description="Declaração da conciliação executada · Origem · Comparado · estrutura · agrupadores · campos comparados · caso lógico inferido"
    )
    classificacao_por_registro: list[RegistroConciliadoV1] = Field(
        ...,
        description="1 entrada por registro processado · resultado do match (ou linha-a-linha · caso 3) + classificação estrutural + classificação por campo · ordem determinística"
    )
    contagem_por_classificacao: dict[ClassificacaoRegistroV1, int] = Field(
        ...,
        description="Contagem das classificações estruturais · 6 chaves quando caso ABAS_DISTINTAS · 4 chaves quando caso MESMA_ABA_EM_COLUNAS · zero preservado · D-209 + D-213"
    )
    cobertura: Optional[CoberturaV1] = Field(
        ...,
        description="Cobertura de match por base · útil para auditoria assimétrica · §6 do Resumo Executivo · None quando caso MESMA_ABA_EM_COLUNAS (cobertura 100% por construção · informação ausente vira None · não Decimal('1'))"
    )
    valor_por_campo: list[ValorPorCampoV1] = Field(
        ...,
        description="1 entrada por campo comparado declarado · até 10"
    )
    resumo_por_agrupador_executivo: Optional[list[LinhaResumoAgrupadorV1]] = Field(
        default=None,
        description="1 linha por valor único do(s) agrupador(es) executivo(s) · None quando agrupadores executivos não configurados · ordenação T-RANK por |Diferença líquida| desc"
    )
    pontes: list[PonteCampoV1] = Field(
        ...,
        description="1 entrada por campo comparado elegível para Ponte · campos PERCENTUAL/ADIMENSIONAL/RAZAO omitidos por Q1.B · D-210"
    )
    status_ponte_geral: StatusPonteV1 = Field(
        ...,
        description="Status binário consolidado da Ponte · FECHA quando todas as pontes elegíveis fecham dentro do épsilon · COM_RESIDUO caso contrário · D-210"
    )
    sintese_diagnostico: SinteseDiagnosticoV1 = Field(
        ...,
        description="4 contadores de Síntese exibidos no §8 do Resumo Executivo"
    )
    config_aplicada: ConfigAplicadaV1 = Field(
        ...,
        description="Reflexo declarativo da configuração efetivamente usada"
    )
    leitura_qualitativa: LeituraQualitativaV1 = Field(
        ...,
        description="Bloco de prosa parametrizado · gerado por construir_leitura_qualitativa_v1"
    )
    warnings_emitidos: list[WarningV1] = Field(
        default_factory=list,
        description="Warnings W-V1-TOL · W-V1-DUP · W-V1-AMB · W-V1-UNIDADE · podem incluir warnings herdados do motor"
    )
    modelo_aplicado: Optional[ModeloAplicadoV1] = Field(
        default=None,
        description="Referência a T-MODELO quando modelo salvo foi aplicado"
    )
```

**Invariantes:**

- `len(classificacao_por_registro)` ≥ 1 (motor recusa execução se 0 registros)
- `sum(contagem_por_classificacao.values()) == len(classificacao_por_registro)`
- `len(valor_por_campo) == len(conciliacao_realizada.campos_comparados)`
- `len(pontes) == len([c for c in campos_comparados if c.unidade ∉ {PERCENTUAL, ADIMENSIONAL, RAZAO}])`
- Toda chave de `contagem_por_classificacao` ∈ enum `ClassificacaoRegistroV1`
- Quando `caso_logico_inferido == MESMA_ABA_EM_COLUNAS`: `contagem_por_classificacao[SO_ORIGEM] == 0` E `contagem_por_classificacao[SO_COMPARADO] == 0` E `contagem_por_classificacao[DIVERGENCIA_DUPLICIDADE] == 0` E `contagem_por_classificacao[DIVERGENCIA_AMBIGUIDADE] == 0`
- Quando `caso_logico_inferido == MESMA_ABA_EM_COLUNAS`: `cobertura == None`

### 1.2 · `ConciliacaoRealizadaV1` · declaração da conciliação executada (D-213)

```python
class ConciliacaoRealizadaV1(BaseModel):
    """
    Declara a conciliação que foi efetivamente executada.

    Capta a dualidade T-DUAL através de 2 dimensões ortogonais:
      - n_arquivos (físico do upload · 1 ou 2)
      - caso_logico_inferido (ABAS_DISTINTAS · MESMA_ABA_EM_COLUNAS)

    Combinações válidas (D-213):
      - n_arquivos=2 + ABAS_DISTINTAS  (Caso 1 · clássico)
      - n_arquivos=1 + ABAS_DISTINTAS  (Caso 2 · 1 arquivo · 2 abas)
      - n_arquivos=1 + MESMA_ABA_EM_COLUNAS (Caso 3 · 1 arquivo · 1 aba · pares de colunas)
      - n_arquivos=2 + MESMA_ABA_EM_COLUNAS (Caso 4 · 2 arquivos · 1 aba cada · pares de colunas)
    """
    model_config = ConfigDict(use_enum_values=False)

    n_arquivos: Literal[1, 2] = Field(
        ...,
        description="Físico do upload · decidido na E1 · 1 (arquivo único · com N abas) ou 2 (dois arquivos)"
    )
    arquivo_origem: str = Field(
        ...,
        description="Nome do arquivo da Origem · em n_arquivos==1 · igual a arquivo_comparado"
    )
    aba_origem: str = Field(
        ...,
        description="Nome da aba da Origem · sempre populado"
    )
    arquivo_comparado: str = Field(
        ...,
        description="Nome do arquivo do Comparado · em n_arquivos==1 · igual a arquivo_origem"
    )
    aba_comparado: str = Field(
        ...,
        description="Nome da aba do Comparado · sempre populado · igual a aba_origem somente quando caso_logico_inferido==MESMA_ABA_EM_COLUNAS"
    )
    caso_logico_inferido: CasoLogicoV1 = Field(
        ...,
        description="Caso lógico do confronto · derivado pelo motor a partir do apontamento dos campos na E3 · não declarado pela Usuária"
    )
    origem_ux: str = Field(
        ...,
        description="Rótulo amigável editável da Origem · default 'Origem' quando vazio"
    )
    comparado_ux: str = Field(
        ...,
        description="Rótulo amigável editável do Comparado · default 'Comparado' quando vazio"
    )
    rotulo_amigavel_declarado: bool = Field(
        ...,
        description="True quando origem_ux ≠ 'Origem' E comparado_ux ≠ 'Comparado' · ativa formulação direcional 'Saiu do' / 'Apareceu no' (P-α.3-03)"
    )
    agrupadores_match: list[AgrupadorMatchV1] = Field(
        ...,
        description="1 a 5 agrupadores · L-V1-D · ordem é declarada pela Usuária"
    )
    campos_comparados: list[CampoComparadoV1] = Field(
        ...,
        description="1 a 10 campos · P-V1-10 · ordem é declarada pela Usuária"
    )
    agrupadores_resumo_executivo: list[str] = Field(
        default_factory=list,
        description="0 a 5 agrupadores · 0 = aba Resumo por Agrupador omitida"
    )
    n_registros_origem: int = Field(
        ...,
        description="Total de registros do lado Origem · em MESMA_ABA_EM_COLUNAS é igual a n_processados"
    )
    n_registros_comparado: int = Field(
        ...,
        description="Total de registros do lado Comparado · em MESMA_ABA_EM_COLUNAS é igual a n_processados"
    )
    n_processados: int = Field(
        ...,
        description="Total de registros após match · em ABAS_DISTINTAS = n_origem + n_comparado − n_pares_casados · em MESMA_ABA_EM_COLUNAS = N° de linhas da aba"
    )
```

**Invariantes:**

- 1 ≤ `len(agrupadores_match)` ≤ 5 (B-V1-AGRUPADOR-ZERO · L-V1-D)
- 1 ≤ `len(campos_comparados)` ≤ 10 (B-V1-CAMPO-ZERO · P-V1-10)
- 0 ≤ `len(agrupadores_resumo_executivo)` ≤ 5
- `n_arquivos == 1 → arquivo_origem == arquivo_comparado`
- `caso_logico_inferido == MESMA_ABA_EM_COLUNAS → aba_origem == aba_comparado`
- `caso_logico_inferido == ABAS_DISTINTAS → aba_origem != aba_comparado`
- `rotulo_amigavel_declarado == (origem_ux != "Origem" and comparado_ux != "Comparado")`

### 1.3 · Enum `CasoLogicoV1` · 2 modos do confronto (D-213)

```python
class CasoLogicoV1(str, Enum):
    """
    Caso lógico do confronto · inferido pelo motor a partir do apontamento
    dos agrupadores de match e campos comparados (D-213).

    ABAS_DISTINTAS:
      Origem em uma aba · Comparado em outra · match precisa ser executado
      pelo agrupador para casar linha-a-linha. Cobre Casos 1 e 2 do
      cenário de upload.

    MESMA_ABA_EM_COLUNAS:
      Origem e Comparado coexistem na mesma aba como conjuntos de colunas
      distintos · cada linha já é um par casado por construção · não há
      match a executar. Cobre Casos 3 e 4 do cenário de upload.
    """
    ABAS_DISTINTAS = "ABAS_DISTINTAS"
    MESMA_ABA_EM_COLUNAS = "MESMA_ABA_EM_COLUNAS"
```

**Algoritmo de inferência** (executado no início do pipeline · §2.1 etapa [3]):

```python
def inferir_caso_logico(
    agrupadores_match: list[AgrupadorMatchV1],
    campos_comparados: list[CampoComparadoV1],
    aba_origem: str,
    aba_comparado: str,
) -> CasoLogicoV1:
    """
    Regra:
      - Se aba_origem == aba_comparado E todos os apontamentos
        (agrupadores + campos) declaram coluna_origem != coluna_comparado:
        → MESMA_ABA_EM_COLUNAS
      - Se aba_origem != aba_comparado:
        → ABAS_DISTINTAS
      - Caso degenerado (mesma aba E coluna_origem == coluna_comparado em
        algum apontamento): bloqueio B-V1-MESMA-COLUNA na validação E3
    """
```

### 1.4 · `AgrupadorMatchV1` · 1 entrada da chave de match (D-213 ajustado)

```python
class AgrupadorMatchV1(BaseModel):
    """
    Declara 1 elemento da chave lógica do match.

    Em ABAS_DISTINTAS: nome_origem e nome_comparado são colunas
    de abas distintas · valores casados por busca segundo modo_match.

    Em MESMA_ABA_EM_COLUNAS: nome_origem e nome_comparado são colunas
    distintas da mesma aba · pareadas por linha · modo_match é registrado
    mas não tem efeito (cada linha é par único).
    """
    model_config = ConfigDict(use_enum_values=False)

    nome_origem: str = Field(
        ...,
        description="Coluna na aba da Origem"
    )
    nome_comparado: str = Field(
        ...,
        description="Coluna na aba do Comparado · != nome_origem quando MESMA_ABA_EM_COLUNAS"
    )
    rotulo_analitico: str = Field(
        ...,
        description="Nome amigável dado pela Usuária · default = nome_origem · vira título de coluna nas Abas 2/3/4"
    )
    modo_match: ModoMatchV1 = Field(
        ...,
        description="Regra declarada de busca · ignorada em MESMA_ABA_EM_COLUNAS · obrigatória em ABAS_DISTINTAS"
    )
```

### 1.5 · Enum `ModoMatchV1` · 4 modos canônicos

```python
class ModoMatchV1(str, Enum):
    """
    Modo de match declarado pela Usuária.
    Aplicado apenas em ABAS_DISTINTAS · ignorado em MESMA_ABA_EM_COLUNAS.
    """
    EXATO = "EXATO"           # Igualdade total · default
    CONTEM = "CONTEM"         # Origem contém Comparado (ou vice-versa)
    INICIA_COM = "INICIA_COM"
    TERMINA_COM = "TERMINA_COM"
```

**Microcopy user-facing aplicado por F-APRESENT capability 2:**
- `EXATO` → "Exato (igualdade total)"
- `CONTEM` → "Contém"
- `INICIA_COM` → "Inicia com"
- `TERMINA_COM` → "Termina com"

**P-V1-02-Evo · Match fuzzy (T-FUZZY)** parqueado pós-MVP.

### 1.6 · `CampoComparadoV1` · 1 campo a confrontar

```python
class CampoComparadoV1(BaseModel):
    """
    Declara 1 campo cujos valores serão confrontados entre Origem e Comparado.

    Em ABAS_DISTINTAS: valores comparados após match dos agrupadores.
    Em MESMA_ABA_EM_COLUNAS: valores comparados linha-a-linha (par já casado).
    """
    model_config = ConfigDict(use_enum_values=False)

    nome_origem: str = Field(...)
    nome_comparado: str = Field(...)
    nome_analitico: str = Field(...)
    tipo_logico: TipoCampoV1 = Field(...)
    unidade: UnidadeCanonica = Field(
        ...,
        description="default inferido de tipo_logico (Bloco 10.1) · Usuária pode trocar · C.D6"
    )
    tolerancia: Decimal = Field(default=Decimal("0"))
```

**Invariantes:**
- `tolerancia >= Decimal("0")`
- `nome_origem != nome_comparado` quando `caso_logico_inferido == MESMA_ABA_EM_COLUNAS` (B-V1-MESMA-COLUNA)

### 1.7 · Enum `TipoCampoV1` · taxonomia DCV §4.3

```python
class TipoCampoV1(str, Enum):
    VALOR_MONETARIO = "VALOR_MONETARIO"
    QUANTIDADE = "QUANTIDADE"
    VOLUME = "VOLUME"
    PERCENTUAL = "PERCENTUAL"
    PRAZO = "PRAZO"
    INDICE = "INDICE"
    ESTADO_SITUACAO = "ESTADO_SITUACAO"
```

**Mapeamento default `tipo_logico` → `unidade`** (Bloco 10.1):

| `TipoCampoV1` | `UnidadeCanonica` default |
|---|---|
| VALOR_MONETARIO | MONETARIO_BRL |
| QUANTIDADE | QUANTIDADE |
| VOLUME | QUANTIDADE |
| PERCENTUAL | PERCENTUAL |
| PRAZO | TEMPO_DIAS |
| INDICE | MULTIPLICADOR |
| ESTADO_SITUACAO | ADIMENSIONAL |

### 1.8 · Enum `ClassificacaoRegistroV1` · 6 valores · 4 aplicáveis em MESMA_ABA_EM_COLUNAS

```python
class ClassificacaoRegistroV1(str, Enum):
    """
    Classificação estrutural do registro · 1:1 com Bloco 3.1 do vocabulario v4.

    Em ABAS_DISTINTAS: 6 classes válidas.
    Em MESMA_ABA_EM_COLUNAS: apenas CONCILIADO e DIVERGENTE_VALOR (sem
    SO_ORIGEM/SO_COMPARADO/DIVERGENCIA_DUPLICIDADE/DIVERGENCIA_AMBIGUIDADE).
    """
    CONCILIADO = "CONCILIADO"
    DIVERGENTE_VALOR = "DIVERGENTE_VALOR"
    SO_ORIGEM = "SO_ORIGEM"
    SO_COMPARADO = "SO_COMPARADO"
    DIVERGENCIA_DUPLICIDADE = "DIVERGENCIA_DUPLICIDADE"
    DIVERGENCIA_AMBIGUIDADE = "DIVERGENCIA_AMBIGUIDADE"
```

**Decisão de exibição (D-213):** em MESMA_ABA_EM_COLUNAS · classificações inaplicáveis aparecem na tabela de decomposição do Resumo §2 com `0` preservado (auditabilidade C.2 · ausência é informação · padrão da Família A). F-APRESENT capability 2 dispatches: na Aba 6 · §1 do Diagnóstico · texto "Caso lógico: Mesma aba em colunas · classificações estruturais reduzidas a 4 · DIVERGENCIA_DUPLICIDADE / DIVERGENCIA_AMBIGUIDADE / SO_ORIGEM / SO_COMPARADO não aplicáveis por construção".

### 1.9 · Enum `StatusCampoV1` · 6 status por campo

```python
class StatusCampoV1(str, Enum):
    """
    Status do registro × campo · espelha Bloco 3.2 do vocabulario v4.
    Aplicável aos 2 casos lógicos (1:1 com células · não com classificação estrutural).
    """
    IGUAL = "IGUAL"
    DENTRO_TOLERANCIA = "DENTRO_TOLERANCIA"
    DIVERGENTE = "DIVERGENTE"
    SEM_VALOR_ORIGEM = "SEM_VALOR_ORIGEM"
    SEM_VALOR_COMPARADO = "SEM_VALOR_COMPARADO"
    SEM_VALOR_AMBOS = "SEM_VALOR_AMBOS"
```

### 1.10 · Enum `StatusPonteV1`

```python
class StatusPonteV1(str, Enum):
    FECHA = "FECHA"
    COM_RESIDUO = "COM_RESIDUO"
```

**Cálculo:** `FECHA` quando todas as pontes elegíveis (não-PERCENTUAL · Q1.B) têm `|residuo| < epsilon_da_unidade`. Caso degenerado (`len(pontes) == 0`) · `FECHA` por convenção.

### 1.11 · `RegistroConciliadoV1`

```python
class RegistroConciliadoV1(BaseModel):
    """1 linha do Mapa de Conciliação (Aba 3) · também base da Aba 4."""
    model_config = ConfigDict(use_enum_values=False)

    chave_consolidada: str = Field(
        ...,
        description="ABAS_DISTINTAS: concatenação dos valores dos agrupadores de match com '|'. MESMA_ABA_EM_COLUNAS: concatenação dos valores das colunas de Origem dos agrupadores (idêntico aos do Comparado por construção)"
    )
    valores_agrupadores: dict[str, str] = Field(
        ...,
        description="rotulo_analitico → valor (sempre str · zeros à esquerda preservados)"
    )
    classificacao_estrutural: ClassificacaoRegistroV1 = Field(
        ...,
        description="1 das 6 classes em ABAS_DISTINTAS · 1 das 2 (CONCILIADO/DIVERGENTE_VALOR) em MESMA_ABA_EM_COLUNAS"
    )
    valores_por_campo: list[CelulaCampoV1] = Field(...)
    diferenca_total_registro: Optional[Decimal] = Field(
        ...,
        description="Soma das diferenças absolutas multi-campo · None quando classificação ∈ {SO_ORIGEM, SO_COMPARADO, DIVERGENCIA_DUPLICIDADE, DIVERGENCIA_AMBIGUIDADE}"
    )
    sigma_diferenca_total_registro: Optional[Decimal] = Field(...)
    variacao_total_registro_pct: Optional[Decimal] = Field(
        ...,
        description="diferenca_total_registro / Σ valor_origem · None nas mesmas condições · None se Σ valor_origem == 0"
    )
    observacoes: Optional[str] = Field(default=None)
```

### 1.12 · `CelulaCampoV1`

```python
class CelulaCampoV1(BaseModel):
    """1 par (Origem, Comparado) de valores para 1 campo comparado em 1 registro."""
    model_config = ConfigDict(use_enum_values=False)

    campo_indice: int = Field(...)
    valor_origem: Optional[Decimal] = Field(...)
    valor_comparado: Optional[Decimal] = Field(...)
    diferenca: Optional[Decimal] = Field(...)
    status_campo: StatusCampoV1 = Field(...)
```

### 1.13 · `CoberturaV1`

```python
class CoberturaV1(BaseModel):
    """
    Cobertura de match por base · §6 do Resumo Executivo.
    None quando MESMA_ABA_EM_COLUNAS (cobertura é trivialmente 100% por construção).
    """
    model_config = ConfigDict(use_enum_values=False)

    n_origem_com_par: int
    n_origem_sem_par: int
    cobertura_origem_pct: Decimal
    n_comparado_com_par: int
    n_comparado_sem_par: int
    cobertura_comparado_pct: Decimal
```

### 1.14 · `ValorPorCampoV1`

```python
class ValorPorCampoV1(BaseModel):
    """1 entrada por campo comparado · §5 do Resumo Executivo · §3.2 Aba 2."""
    model_config = ConfigDict(use_enum_values=False)

    nome_analitico: str
    unidade: UnidadeCanonica
    soma_origem: Decimal
    soma_comparado: Decimal
    diferenca_liquida: Decimal
    sigma_diferenca: Decimal
    n_tolerancia_absorvida: int
    valor_tolerancia_absorvida: Decimal
```

### 1.15 · `LinhaResumoAgrupadorV1` + `MetricaCampoAgrupadorV1`

```python
class LinhaResumoAgrupadorV1(BaseModel):
    """1 linha da Aba 2 · 1 valor único do(s) agrupador(es) executivo(s)."""
    model_config = ConfigDict(use_enum_values=False)

    valores_agrupador: dict[str, str]
    n_conciliados: int
    n_divergentes_valor: int
    n_so_origem: int  # sempre 0 em MESMA_ABA_EM_COLUNAS
    n_so_comparado: int  # idem
    metricas_por_campo: list[MetricaCampoAgrupadorV1]
    diferenca_liquida_total: Decimal

class MetricaCampoAgrupadorV1(BaseModel):
    model_config = ConfigDict(use_enum_values=False)
    nome_analitico: str
    unidade: UnidadeCanonica
    soma_origem: Decimal
    soma_comparado: Decimal
    diferenca_liquida: Decimal
    sigma_diferenca: Decimal
```

### 1.16 · `PonteCampoV1`

```python
class PonteCampoV1(BaseModel):
    """
    1 sub-Ponte · campos PERCENTUAL/ADIMENSIONAL/RAZAO omitidos (Q1.B).

    Em MESMA_ABA_EM_COLUNAS: ajustes de SO_ORIGEM/SO_COMPARADO são
    Decimal('0') porque por construção não há registros desse tipo.
    """
    model_config = ConfigDict(use_enum_values=False)

    nome_analitico: str
    unidade: UnidadeCanonica
    saldo_origem: Decimal
    ajuste_so_origem: Decimal      # Decimal('0') em MESMA_ABA_EM_COLUNAS
    ajuste_so_comparado: Decimal   # idem
    ajuste_divergentes_valor: Decimal
    ajuste_tolerancia_absorvida: Decimal
    saldo_comparado_esperado: Decimal
    saldo_comparado_real: Decimal
    residuo: Decimal
    fecha: bool
```

### 1.17 · `SinteseDiagnosticoV1`

```python
class SinteseDiagnosticoV1(BaseModel):
    """4 contadores · §8 do Resumo Executivo."""
    model_config = ConfigDict(use_enum_values=False)

    n_tolerancia_absorvida: int
    valor_tolerancia_absorvida: Decimal
    n_chaves_duplicadas: int  # sempre 0 em MESMA_ABA_EM_COLUNAS
    n_registros_afetados_duplicidade: int  # idem
    n_chaves_ambiguas: int  # idem
    n_registros_afetados_ambiguidade: int  # idem
    n_warnings_ativos: int
```

### 1.18 · `ConfigAplicadaV1`

```python
class ConfigAplicadaV1(BaseModel):
    """
    Reflexo declarativo da configuração · 12 campos canônicos achatados
    (CONTEXT §15.12) · consumido por F-APRESENT capability 10.
    """
    model_config = ConfigDict(use_enum_values=False)

    arquivo_origem: str
    aba_origem: str
    arquivo_comparado: str
    aba_comparado: str
    n_arquivos: Literal[1, 2]
    caso_logico_inferido: CasoLogicoV1
    agrupadores_match: list[AgrupadorMatchV1]
    campos_comparados: list[CampoComparadoV1]
    agrupadores_resumo_executivo: list[str]
    paleta_aplicada: str = Field(
        ...,
        description="Selecionada no rodapé do RESULTADO (D-212 corrige P-V1 §4.5) · default 'Azul executivo'"
    )
    epsilon_por_unidade: dict[UnidadeCanonica, Decimal] = Field(
        ...,
        description="TED Q2.C (D-211) · só unidades efetivamente em uso são populadas"
    )
    defaults_sobrescritos: dict[str, str] = Field(default_factory=dict)
    nulos_por_classificacao: dict[ClassificacaoRegistroV1, int]
```

### 1.19 · `LeituraQualitativaV1`

```python
class LeituraQualitativaV1(BaseModel):
    """
    Texto-livre parametrizado · 3 a 6 frases · gerado por
    construir_leitura_qualitativa_v1 (templates/familia_a/leitura_qualitativa_v1.py).
    """
    model_config = ConfigDict(use_enum_values=False)

    texto: str
    faixa_taxa: Literal["ALTA", "MEDIA", "BAIXA"]
    modificadores_aplicados: list[str]
    agrupador_principal_citado: Optional[str] = Field(default=None)
```

### 1.20 · `WarningV1`

```python
class WarningV1(BaseModel):
    """Warning emitido durante a análise · §5 do Diagnóstico."""
    model_config = ConfigDict(use_enum_values=False)

    codigo: str
    severidade: Literal["INFORMATIVO", "AJUSTE_LEVE", "ALERTA_ESTRUTURAL", "DECISAO_USUARIO", "ESCAPE"]
    n_ocorrencias: int
    detalhes: list[dict] = Field(default_factory=list)
```

### 1.21 · `ModeloAplicadoV1`

```python
class ModeloAplicadoV1(BaseModel):
    """Referência a T-MODELO."""
    model_config = ConfigDict(use_enum_values=False)

    nome_modelo: str
    data_criacao: datetime
    versao_contrato: str
```

### 1.22 · Contratos consumidos da Fundação (referência sem redeclaração)

| Contrato | Origem | Função na V1 |
|---|---|---|
| `VNResultBase` | Fundação · D-130 | Classe-base de `ConciliacaoV1Result` |
| `UploadResult` | F-MOT · T-DUAL | Estrutura física do upload |
| `MotorResult` | F-MOT | Inferência de tipos por coluna |
| `ColumnMeta` | F-MOT · estendido por D-202 | `tipo_inferido` + `unidade` + `tipo_campo` |
| `BloqueioOperacional` | F-TRANS · C.D4 · D-127 | Catálogo §2.5 |
| `Paleta` · `CATALOGO_PALETAS` | F-APRESENT cap 1 | 4 paletas executivas |
| `UnidadeCanonica` | Fundação · D-202 | Enum 8 valores |

---

## Seção 2 · Regras de cálculo

### 2.1 · Pipeline canônico end-to-end · 2 ramos por caso lógico

V1 é determinística (C.1). Pipeline ramifica após inferência do caso lógico:

```
[1] Leitura  →  [2] Validação E3 (apontamentos)  →  [3] Inferir caso lógico
                                                          ↓
                                          ┌───────────────┴───────────────┐
                                          ▼                               ▼
                              [4-A] Match (ABAS_DISTINTAS)    [4-B] Pareamento linha-a-linha
                                          ↓                               ↓
                                          └───────────────┬───────────────┘
                                                          ▼
                                  [5] Cálculo de diferença · classificação por campo
                                                          ↓
                                  [6] Classificação agregada do registro
                                                          ↓
                                  [7] Agregações (Cobertura · ValorPorCampo · Pontes · Status)
                                                          ↓
                                          [8] Montagem do contrato `ConciliacaoV1Result`
```

**Detalhamento das etapas:**

**[1] Leitura** (consumo de `UploadResult` · T-DUAL)
- 1 ou 2 arquivos lidos via T-DUAL · sem T-AGRUPA
- `MotorResult` carrega `ColumnMeta` por coluna
- Aplica B-V1-NO-UPLOAD se nada foi carregado

**[2] Validação dos apontamentos da E3**
- Verifica que `nome_origem` e `nome_comparado` de cada agrupador/campo existem nas respectivas abas
- Aplica B-V1-MESMA-COLUNA (`nome_origem == nome_comparado` na mesma aba) → bloqueio
- Aplica B-V1-MISTURA-ABAS (apontamentos misturando aba_origem e aba_comparado de forma inconsistente) → bloqueio
- Aplica B-V1-CHAVE-INVALIDA (% de nulos ≥ TED `chave_nulos_max`) → bloqueio escapável

**[3] Inferir caso lógico** (algoritmo §1.3):
- `aba_origem == aba_comparado` E todos os apontamentos válidos → `MESMA_ABA_EM_COLUNAS`
- `aba_origem != aba_comparado` → `ABAS_DISTINTAS`

**[4-A] Match · só em ABAS_DISTINTAS** (§2.2 · DCV §4.2)
- Constrói chave consolidada de cada lado · concatena valores dos agrupadores com `|`
- Detecta duplicidade ANTES do match (chave duplicada na própria base)
- Executa match conforme `modo_match` (4 valores · EXATO / CONTEM / INICIA_COM / TERMINA_COM)
- Detecta ambiguidade DEPOIS do match (1 chave Origem · ≥ 2 candidatos Comparado em modo não-EXATO)

**[4-B] Pareamento linha-a-linha · só em MESMA_ABA_EM_COLUNAS**
- Cada linha da aba é 1 par já casado por construção
- `chave_consolidada` é construída a partir das colunas-Origem dos agrupadores (idêntica às colunas-Comparado por design da Usuária · ela aponta o agrupador como `coluna_X = coluna_X` na E3)
- `modo_match` declarado é registrado em `ConfigAplicadaV1` mas **não aplicado** (nada a buscar · cada linha é único par)
- Não há detecção de duplicidade nem ambiguidade (por construção · cada linha é registro único)

**[5] Cálculo de diferença e classificação por campo** (DCV §5.3)
- Para cada par 1-para-1: para cada `CampoComparadoV1` declarado · `diferenca = valor_origem - valor_comparado`
- Em ABAS_DISTINTAS · registros SO_ORIGEM/SO_COMPARADO/DUPLICIDADE/AMBIGUIDADE têm `valor_*=preserved` (real onde existe · None onde não existe) · `diferenca=None`
- Em MESMA_ABA_EM_COLUNAS · sempre há valor_origem e valor_comparado por construção · pode haver SEM_VALOR_ORIGEM ou SEM_VALOR_COMPARADO no nível da célula (não da linha)
- `Decimal` (precisão financeira)

**[6] Classificação agregada do registro** (P-V1-06)
- Em ABAS_DISTINTAS · regra completa de §2.3 (6 classes)
- Em MESMA_ABA_EM_COLUNAS · regra reduzida: CONCILIADO ou DIVERGENTE_VALOR
  - `CONCILIADO` quando todos os campos têm `status_campo ∈ {IGUAL, DENTRO_TOLERANCIA, SEM_VALOR_AMBOS}`
  - `DIVERGENTE_VALOR` quando algum campo tem `status_campo == DIVERGENTE`
  - Status `SEM_VALOR_ORIGEM`/`SEM_VALOR_COMPARADO` aparecem em células · não promovem registro a SO_ORIGEM/SO_COMPARADO

**[7] Agregações**
- Soma por classificação · em MESMA_ABA_EM_COLUNAS as 4 classes ausentes ficam com `0`
- `cobertura: None` em MESMA_ABA_EM_COLUNAS · populado em ABAS_DISTINTAS
- ValorPorCampoV1 · idêntico nos 2 casos
- Resumo por agrupador executivo · idêntico nos 2 casos
- Pontes · idêntico nos 2 casos · em MESMA_ABA_EM_COLUNAS `ajuste_so_*` é Decimal('0')
- Status da Ponte geral · idêntico nos 2 casos
- Síntese diagnóstico · 4 contadores · em MESMA_ABA_EM_COLUNAS contadores de duplicidade/ambiguidade são `0`
- Leitura qualitativa · template adaptado por caso lógico (frase inicial diferente)

**[8] Montagem do contrato**
- Consolida em `ConciliacaoV1Result`
- Aplica todos os invariantes de §1.1
- Retorna · sem mutação após retorno

**Determinismo:** ordenação determinística por `chave_consolidada` (string) · empate alfabético em LinhaResumoAgrupadorV1.

### 2.2 · Match e detecção de duplicidade/ambiguidade · só em ABAS_DISTINTAS

Algoritmo idêntico ao da S-V1 v1 §2.2 · com nota explícita de que MESMA_ABA_EM_COLUNAS pula esta etapa inteira (`[4-B]` substitui).

```python
def executar_match_abas_distintas(
    origem_df: DataFrame, comparado_df: DataFrame,
    agrupadores: list[AgrupadorMatchV1]
) -> list[ParCasado]:
    chaves_origem = construir_chaves(origem_df, agrupadores, lado="origem")
    chaves_comparado = construir_chaves(comparado_df, agrupadores, lado="comparado")

    # Duplicidade ANTES do match
    duplicadas_origem = detectar_chaves_duplicadas(chaves_origem)
    duplicadas_comparado = detectar_chaves_duplicadas(chaves_comparado)

    if all(a.modo_match == ModoMatchV1.EXATO for a in agrupadores):
        pares = merge_exato(chaves_origem, chaves_comparado)
    else:
        pares = varredura_match(chaves_origem, chaves_comparado, agrupadores)

    # Ambiguidade DEPOIS do match
    pares_ambiguidade = detectar_pares_multiplos(pares)

    return pares
```

**Casos especiais cobertos:** chave duplicada Origem mas não Comparado · chave duplicada em ambas · chave única Origem com 0 candidatos Comparado · chave única com 1 candidato CONTEM · chave única com ≥ 2 candidatos CONTEM. Detalhamento idêntico ao da S-V1 v1 §2.2.

### 2.3 · Classificação agregada do registro

Em ABAS_DISTINTAS:

```python
def classificar_registro_abas_distintas(par: ParCasado, campos: list[CampoComparadoV1]) -> ClassificacaoRegistroV1:
    if par.tipo == "DUPLICIDADE":
        return ClassificacaoRegistroV1.DIVERGENCIA_DUPLICIDADE
    if par.tipo == "AMBIGUIDADE":
        return ClassificacaoRegistroV1.DIVERGENCIA_AMBIGUIDADE
    if par.tipo == "SO_ORIGEM":
        return ClassificacaoRegistroV1.SO_ORIGEM
    if par.tipo == "SO_COMPARADO":
        return ClassificacaoRegistroV1.SO_COMPARADO

    statuses = [calcular_status_campo(par, c) for c in campos]
    if any(s == StatusCampoV1.DIVERGENTE for s in statuses):
        return ClassificacaoRegistroV1.DIVERGENTE_VALOR
    return ClassificacaoRegistroV1.CONCILIADO
```

Em MESMA_ABA_EM_COLUNAS:

```python
def classificar_registro_mesma_aba(linha: dict, campos: list[CampoComparadoV1]) -> ClassificacaoRegistroV1:
    statuses = [calcular_status_campo_linha(linha, c) for c in campos]
    if any(s == StatusCampoV1.DIVERGENTE for s in statuses):
        return ClassificacaoRegistroV1.DIVERGENTE_VALOR
    # CONCILIADO inclui IGUAL · DENTRO_TOLERANCIA · SEM_VALOR_AMBOS
    return ClassificacaoRegistroV1.CONCILIADO
```

### 2.4 · Derivação de `StatusCampoV1` por célula

Tabela determinística idêntica à da S-V1 v1 §2.4 · independente do caso lógico:

| `valor_origem` | `valor_comparado` | Condição | `status_campo` |
|---|---|---|---|
| None | None | — | SEM_VALOR_AMBOS |
| None | qualquer | — | SEM_VALOR_ORIGEM |
| qualquer | None | — | SEM_VALOR_COMPARADO |
| not None | not None | `valor_origem == valor_comparado` | IGUAL |
| not None | not None | `0 < |valor_origem - valor_comparado| ≤ tolerancia` | DENTRO_TOLERANCIA |
| not None | not None | `|valor_origem - valor_comparado| > tolerancia` | DIVERGENTE |

### 2.5 · Catálogo de bloqueios B-V1-* (MBO · C.D4 · ampliado para D-213)

| Código | Condição | Comportamento | Escapável | Microcopy user-facing |
|---|---|---|---|---|
| `B-V1-NO-UPLOAD` | E1 sem arquivo carregado | Bloqueia avanço | Não | "Faça upload das bases para começar" |
| `B-V1-AGRUPADOR-ZERO` | `len(agrupadores_match) == 0` na E3 | Bloqueia avanço | Não | "Configure ao menos 1 agrupador de match para casar registros" |
| `B-V1-AGRUPADOR-EXCEDE` | Tentativa de adicionar 6º agrupador | Bloqueia adição UI | Não · L-V1-D | "Limite de 5 agrupadores de match no MVP." |
| `B-V1-CAMPO-ZERO` | `len(campos_comparados) == 0` na E3.2 | Bloqueia avanço | Não | "Configure ao menos 1 campo comparado para a análise" |
| `B-V1-CAMPO-EXCEDE` | Tentativa de adicionar 11º campo | Bloqueia adição UI | Não · P-V1-10-Evo | "Limite de 10 campos comparados no MVP." |
| `B-V1-MESMA-COLUNA` | Apontamento `nome_origem == nome_comparado` na mesma aba | Bloqueia avanço E3→E4 | Não · estrutural | "A coluna de Origem e Comparado é a mesma · isto não é uma comparação · escolha colunas distintas" |
| `B-V1-MISTURA-ABAS` | Apontamentos misturam aba_origem e aba_comparado de forma inconsistente (alguns na mesma · outros em distintas) | Bloqueia avanço E3→E4 | Não · estrutural | "Os apontamentos de Origem e Comparado precisam ser todos da mesma aba · ou todos de abas distintas · não misturar" |
| `B-V1-CHAVE-INVALIDA` | Coluna escolhida como agrupador tem ≥ TED `chave_nulos_max` (default 50%) de nulos | Bloqueia avanço | Sim | "A coluna {nome} tem {N}% de valores vazios e não serve como agrupador de match · escolha outra coluna" |
| `B-V1-MOTOR-INFERIU-INCOMPATIVEL` | Tipo declarado pela Usuária ≠ tipo inferido | Aviso · não bloqueia | Sim · default da Usuária prevalece | "O sistema inferiu que a coluna {nome} é {tipo_inferido} mas você marcou como {tipo_escolhido} · revise" |
| `B-V1-RESULTADO-EXCEDE` | `n_processados > 500.000` (TED `volume_max`) | Bloqueia execução | Sim · ECP P4 | "A análise gerou {N} registros · acima do limite de 500.000 · simplifique a chave ou aplique filtro prévio" |
| `B-V1-DIV-ZERO` | `Σ valor_origem == 0` em `variacao_total_registro_pct` | Não bloqueia · campo recebe `None` | — | (não exibe · célula vazia "—") |
| `B-V1-MOTOR-FALHOU` | Exception não-tratada no pipeline | Bloqueia execução · log do detalhe | Não · contato suporte | "Erro inesperado no processamento · {detalhe técnico} · entre em contato com o suporte" |

**Mudanças desde S-V1 v1:**
- `B-V1-MESMA-ABA` → removido (caso de "mesma aba" com Origem e Comparado **na mesma coluna** vira `B-V1-MESMA-COLUNA`; "mesma aba com colunas distintas" não é mais bloqueado · vira o Caso 3 legítimo)
- `B-V1-MISTURA-ABAS` → novo (apontamentos inconsistentes · D-213)

**Aplicação ECP (C.D5):** `B-V1-RESULTADO-EXCEDE` é P4. `B-V1-CHAVE-INVALIDA` é P3. Demais são P1-P2 ou estruturais não-escaláveis.

### 2.6 · Cálculo do `StatusPonteV1` geral (Q1.B + Q2.C)

Idêntico ao da S-V1 v1 §2.6:

```python
def calcular_status_ponte_geral(pontes, epsilon_por_unidade):
    if len(pontes) == 0:
        return StatusPonteV1.FECHA
    pontes_que_nao_fecham = [p for p in pontes if not p.fecha]
    if len(pontes_que_nao_fecham) == 0:
        return StatusPonteV1.FECHA
    return StatusPonteV1.COM_RESIDUO
```

### 2.7 · Catálogo de warnings W-V1-*

| Código | Microcopy técnica | Severidade | Quando dispara |
|---|---|---|---|
| `W-V1-TOL` | "Tolerância absorveu diferenças" | INFORMATIVO | ≥ 1 registro CONCILIADO com `diferenca ≠ 0` (qualquer caso lógico) |
| `W-V1-DUP` | "Duplicidade em chaves" | ALERTA_ESTRUTURAL | ≥ 1 chave duplicada (só em ABAS_DISTINTAS · sempre 0 ocorrências em MESMA_ABA_EM_COLUNAS) |
| `W-V1-AMB` | "Ambiguidade em match não-exato" | ALERTA_ESTRUTURAL | ≥ 1 chave com múltiplos candidatos (só em ABAS_DISTINTAS · sempre 0 em MESMA_ABA_EM_COLUNAS) |
| `W-V1-UNIDADE` | "Unidade declarada divergente da inferida" | AJUSTE_LEVE | tipo_logico ↔ unidade declarado divergente da inferência |

**Padrão de exibição:** warnings com 0 ocorrências exibem texto auditável "0 ocorrências · nenhuma a reportar". Em MESMA_ABA_EM_COLUNAS · W-V1-DUP e W-V1-AMB sempre aparecem com 0 + microcopy explicativa "não aplicável neste caso lógico (mesma aba em colunas)".

### 2.8 · Thresholds editáveis declarados (TED · C.D2 · D-178 corrigido em P-V1 via D-212)

**Localização:** **expander "⚙️ Configurações avançadas" no topo de cada tela** · D-178 revoga D-153. P-V1 §4.5 corrigida em D-212.

| Código técnico | Label user-facing | Default | Tipo |
|---|---|---|---|
| `chave_nulos_max` | "Limite de células vazias em coluna de chave" | `50%` | Decimal |
| `volume_max` | "Limite de registros processados" | `500.000` | int |
| `epsilon_por_unidade.MONETARIO_BRL` | "Tolerância de fechamento da Ponte · valores monetários" | `Decimal("0.01")` | Decimal |
| `epsilon_por_unidade.QUANTIDADE` | "Tolerância de fechamento da Ponte · quantidades" | `Decimal("0")` | Decimal |
| `epsilon_por_unidade.TEMPO_DIAS` | "Tolerância de fechamento da Ponte · prazos em dias" | `Decimal("0")` | Decimal |
| `epsilon_por_unidade.TEMPO_HORAS` | "Tolerância de fechamento da Ponte · prazos em horas" | `Decimal("0.01")` | Decimal |
| `epsilon_por_unidade.MULTIPLICADOR` | "Tolerância de fechamento da Ponte · índices" | `Decimal("0.0001")` | Decimal |
| `concentracao_agrupador_principal_min` | "Limite de concentração para citar agrupador principal" | `Decimal("0.70")` | Decimal |

**Aplicação Q2.C:** `epsilon_por_unidade` é `dict[UnidadeCanonica, Decimal]` · expander mostra **só as unidades efetivamente em uso** após Etapa 3.2.

### 2.9 · CPCO (C.D1) · modo da base

V1 não usa T-AGRUPA · `modo_base` em `ConfigAplicadaV1` é `"V1_DUAL"` constante · indica modo dual T-DUAL e ausência de consolidação.

Vocabulario_bilingue v4 Bloco 2 ganha entrada `V1_DUAL` → `"Confronto entre 2 bases · sem consolidação"` (extensão a aplicar).

### 2.10 · Resumo Executivo · 9 seções · mapeamento contrato → seção

| Seção P-V1 | Conteúdo · campos do contrato consumidos |
|---|---|
| §1 Cabeçalho identificador | `conciliacao_realizada.{arquivo_*, aba_*, origem_ux, comparado_ux}` · `modelo_aplicado` (cond) |
| §2 Taxa de Conciliação · KPI primário | `taxa_conciliacao_geral = contagem[CONCILIADO] / sum(contagem.values())` · tabela: 6 classes em ABAS_DISTINTAS · 2 ativas + 4 zerados em MESMA_ABA_EM_COLUNAS |
| §3 Volumetria | `n_registros_origem`, `n_registros_comparado`, `n_processados` |
| §4 Status da Ponte | `status_ponte_geral` · `pontes` |
| §5 Valor financeiro por campo | `valor_por_campo[*]` |
| §6 Cobertura por base | `cobertura.*` quando ABAS_DISTINTAS · em MESMA_ABA_EM_COLUNAS exibe seção colapsada com nota "Cobertura 100% por construção (caso: Mesma aba em colunas)" |
| §7 Resumo por agrupador | `resumo_por_agrupador_executivo[*]` quando configurado |
| §8 Síntese do Diagnóstico | `sintese_diagnostico.*` |
| §9 Configuração aplicada | `config_aplicada.*` (incluindo `caso_logico_inferido` em microcopy "Caso lógico: {tradução}") |
| (final) Leitura Qualitativa | `leitura_qualitativa.texto` |

### 2.11 · Estrutura da exportação Excel · 6 abas · mapeamento contrato → aba

Idêntico à S-V1 v1 §2.11 · sem alteração estrutural.

### 2.12 · Padrões §13 aplicados

Idêntico à S-V1 v1 §2.12 · com adendo: §13.4 (View especializada por modo) · V1 tem 2 casos lógicos mas não 2 views distintas · adaptação visual condicional (microcopy do §1 do Diagnóstico declara o caso · estrutura macro preservada).

### 2.13 · Checklist §9 Camada C · 8 derivados verificados

| Derivado | Aplicação V1 | Onde formalizado |
|---|---|---|
| C.D1 · CPCO | V1 não usa T-AGRUPA · `modo_base = V1_DUAL` constante | §2.9 |
| C.D2 · TED | 8 thresholds catalogados · expander no topo (D-178) | §2.8 |
| C.D3 · BAD | Aba 3 (Mapa) + Aba 6 (Diagnóstico · última) | §2.11 |
| C.D4 · MBO | Catálogo §2.5 · 12 bloqueios · todos com 5 campos | §2.5 |
| C.D5 · ECP | `chave_nulos_max` (P3) · `volume_max` (P4) | §2.5 + §2.8 |
| C.D6 · DDU | `unidade` default · `epsilon_por_unidade` default · paleta default Azul · evidência visível | §1.6 + §2.8 |
| C.D7 · Motor primeiro | Matriz cartesiana 2 casos lógicos × 6 classificações × 4 modos × 8 unidades em V-V1 | V-V1 |
| C.D8 · Unidade declarada | `unidade` obrigatório em `CampoComparadoV1`, `ValorPorCampoV1`, `PonteCampoV1` | §1.6 · §1.14 · §1.16 |

### 2.14 · Escala de cardinalidade V1 (ECP · C.D5)

Idêntico à S-V1 v1 §2.14 · sem alteração.

---

## Seção 3 · Wireframe funcional · espelho fiel da estrutura V2 + adaptações V1

**Estrutura macro herdada literalmente do `app_v2.py`** (suite 746/746 verde · canônico):

- Layout top-down em coluna única (`st.set_page_config(layout="wide")`) · sem sidebar lateral
- Header persistente no topo · `st.title()` + linha de 4 botões + Stepper horizontal + `st.divider()`
- TED em expander "⚙️ Configurações avançadas" no topo (D-178 · revoga D-153)
- Cada etapa é uma tela própria com `st.subheader()` + `st.caption()` + conteúdo + `st.divider()` + linha de 2 botões (Voltar/Avançar)
- Stepper só aparece quando `etapa not in ("vazio", "ERRO")`
- Paleta no rodapé do RESULTADO (D-175 §5.4 · D-212 corrige P-V1 §4.5)

### 3.1 · Estados macro · 8 estados · análogos diretos da V2

| Estado V1 | Análogo V2 | Conteúdo |
|---|---|---|
| `vazio` | `vazio` | Upload de 1 ou 2 arquivos · radio inicial "Quantos arquivos?" |
| `E1_OK` | `E1_OK` | Pós-upload · escolher aba(s) · Confirmar e processar bases |
| `E2` | `E2` reduzido | "Identificar lados" · rótulos amigáveis Origem/Comparado |
| `E3` | `E3` (1 campo) → V1 (N campos + N agrupadores) | "Configurar análise" · agrupadores match + campos comparados |
| `E4` | `E4` (Agrupar) | "Agrupadores executivos" · 0-5 · OPCIONAL · pode pular |
| `E5` | `E5` Revisão | "Revisar e executar" · 5 colunas-resumo + botão Processar |
| `RESULTADO` | `RESULTADO` | 5 blocos executivos + rodapé Voltar/Paleta/Baixar |
| `ERRO` | `ERRO` | Mensagens de bloqueio |

**Estado intermediário `RESOL_CASO` da V2** (para POR_LINHAS multi-valor) · **não existe na V1** · V1 não tem POR_LINHAS no escopo MVP · ramificação `MESMA_ABA_EM_COLUNAS` é detectada automaticamente em E3 sem tela intermediária.

### 3.2 · Header persistente · espelho V2 com 4 botões

Renderizado em todas as telas via função `_render_header()` (paralela à V2):

- `st.title("V1 · Conciliação de Bases")`
- Linha de 4 colunas com botões:
  - Coluna 1: `st.button("Objetivo da Visão")` · expander modal com microcopy
  - Coluna 2: `st.button("Aplicar modelo")` · disabled em estado `vazio` · habilita expander de upload de modelo (T-MODELO · padrão V2)
  - Coluna 3: `st.download_button("Salvar como modelo")` · disabled em etapa < E5 · gera JSON da config corrente
  - Coluna 4: `st.button("Nova análise")` · reset completo
- Stepper horizontal (`st.columns(5)` com markdown bold + marcadores ✅ / ▶ / ·):
  - "1 · Escolher arquivo(s)"
  - "2 · Identificar lados"
  - "3 · Configurar análise"
  - "4 · Agrupadores executivos"
  - "Revisar e executar"
- `st.divider()`

**Microcopy do botão Objetivo da Visão (expander):**

> **O que faz:** confronta duas bases (Origem × Comparado) e responde se elas representam o mesmo universo de dados.
>
> **Quando usar:** Conciliação contábil mensal · Sistema A × Sistema B · validação de migração · auditoria de integração · conciliação bancária.
>
> **O que obtém:** Taxa de Conciliação · Mapa de Conciliação · Análise Analítica por campo · Ponte de Conciliação · Diagnóstico estrutural.
>
> **Como funciona:** você sobe 1 ou 2 arquivos · escolhe abas · identifica lados · declara agrupadores de match e campos comparados. O motor casa registros (modo exato/contém/inicia/termina) ou trata como pares já casados quando você aponta colunas distintas da mesma aba · classifica em 6 categorias (ou 2 reduzidas) · gera Excel executivo de 6 abas.

### 3.3 · TED · expander "⚙️ Configurações avançadas" no topo

Renderizado pela função `_render_expander_ted()` antes do Stepper · paralela à V2 (D-178). Colapsado por default.

Conteúdo:
- 2 colunas com `st.number_input` para os TED globais:
  - `chave_nulos_max` · "Limite de células vazias em coluna de chave"
  - `volume_max` · "Limite de registros processados"
  - `concentracao_agrupador_principal_min` · "Limite de concentração para citar agrupador principal"
- TED por unidade (`epsilon_por_unidade.{UNIDADE}`) · **só aparece quando E3 já foi populada** · uma entrada por unidade efetivamente em uso (Q2.C · D-211)

### 3.4 · Estado `vazio` · Tela de upload (paralela a `_tela_vazio` da V2)

```
st.subheader("Escolher arquivo(s)")
st.markdown("Suba o(s) arquivo(s) Excel ou CSV com os dados que você quer comparar.")
st.caption("Aceita Excel (.xlsx, .xls) e CSV. Pode ser 1 ou 2 arquivos · você decide abaixo.")

# Radio de decisão física do upload
n_arquivos = st.radio(
    "Quantos arquivos você vai usar?",
    [1, 2],
    horizontal=True,
    format_func=lambda n: "1 arquivo" if n == 1 else "2 arquivos",
)

if n_arquivos == 1:
    up = st.file_uploader("Arquivo", type=["xlsx", "xls", "csv", "tsv"])
elif n_arquivos == 2:
    col1, col2 = st.columns(2)
    with col1:
        up_origem = st.file_uploader("Arquivo da Origem", type=[...], key="up_orig")
    with col2:
        up_comparado = st.file_uploader("Arquivo do Comparado", type=[...], key="up_comp")
```

**Validação para E1_OK:**
- 1 arquivo: `up is not None`
- 2 arquivos: `up_origem is not None and up_comparado is not None`
- Se válido · processa via T-DUAL (motor_upload modo dual) · transita para E1_OK

### 3.5 · Estado `E1_OK` · Escolher aba(s)

```
st.subheader("Escolher arquivo(s)")
st.success(f"Arquivo: {nome_arquivo} · Formato: {formato}")  # adaptado para 1 ou 2

# Caso n_arquivos == 1:
abas = upload_result.arquivo_unico.abas_disponiveis
escolha_abas = st.multiselect(
    "Qual(is) aba(s) quer comparar?",
    abas,
    max_selections=2,
    help="Escolha 1 aba (Caso 3 · Origem e Comparado em colunas distintas dentro da mesma aba) "
         "ou 2 abas (Caso 2 · Origem em uma aba · Comparado em outra)."
)

# Caso n_arquivos == 2:
col1, col2 = st.columns(2)
with col1:
    aba_origem = st.selectbox("Aba do arquivo de Origem", abas_arquivo_origem)
with col2:
    aba_comparado = st.selectbox("Aba do arquivo do Comparado", abas_arquivo_comparado)
```

**Validação para E2:**
- 1 arquivo: `len(escolha_abas) ∈ {1, 2}`
- 2 arquivos: `aba_origem != "" and aba_comparado != ""`
- Botões: "Voltar · trocar arquivo(s)" (esquerda) · "Confirmar e processar bases" (direita · `type="primary"`)
- Ao clicar "Confirmar": `processar_base()` cada aba selecionada · transita para E2

### 3.6 · Estado `E2` · Identificar lados

Paralela direta à E2 da V2 (sem POR_LINHAS/POR_COLUNAS · só rótulos amigáveis):

```
st.subheader("Identificar lados")
st.caption("Dê nomes amigáveis para os dois lados da comparação · aparecem no Excel.")

col1, col2 = st.columns(2)
with col1:
    origem_ux = st.text_input("Como chamar a Origem", placeholder="Ex: Razão · Sistema A · ERP")
with col2:
    comparado_ux = st.text_input("Como chamar o Comparado", placeholder="Ex: Balancete · Sistema B · DW")

st.caption("Esses nomes aparecem em todas as telas e no Excel exportado. "
           "Se deixar em branco, o sistema usa 'Origem' e 'Comparado' como padrão.")
```

**Validação para E3:** sempre válido (campos vazios viram defaults). Botões "← Voltar" / "Próximo · Configurar análise".

### 3.7 · Estado `E3` · Configurar análise

3 sub-blocos dentro de uma única tela (paralelo a E3+E4 da V2 mergeado · porque V1 chama agrupadores match aqui · não em etapa própria):

```
st.subheader("Configurar análise")
st.caption("Declare como casar registros e o que comparar entre eles.")

# Sub-bloco 3.1 · Agrupadores de match
st.markdown("##### Agrupadores de match · qual a chave para casar registros entre os dois lados?")
# Repeater com até 5 cards (igual à microcopy P-V1 §4.4.1)
# Cada card: Coluna na Origem · Coluna no Comparado · Rótulo analítico · Modo de match

# Sub-bloco 3.2 · Campos comparados
st.markdown("##### Campos comparados · quais valores devem bater entre os dois lados?")
# Repeater com até 10 cards (igual à microcopy P-V1 §4.4.2)
# Cada card: Coluna na Origem · Coluna no Comparado · Nome analítico · Tipo lógico · Unidade · Tolerância

# Caso lógico inferido (declarado em info-box discreta após a Sub-etapa 3.2)
caso_inferido = inferir_caso_logico(...)
if caso_inferido == ABAS_DISTINTAS:
    st.info("📋 Caso detectado: Origem e Comparado em abas distintas · será executado match para casar registros.")
else:
    st.info("📋 Caso detectado: Origem e Comparado em colunas distintas da mesma aba · cada linha já é um par casado.")
```

**Validação para E4:**
- B-V1-AGRUPADOR-ZERO bloqueia se 0 agrupadores
- B-V1-CAMPO-ZERO bloqueia se 0 campos
- B-V1-MESMA-COLUNA bloqueia se algum apontamento `nome_origem == nome_comparado` na mesma aba
- B-V1-MISTURA-ABAS bloqueia se apontamentos misturam abas inconsistentemente
- B-V1-CHAVE-INVALIDA dispara aviso inline (não bloqueia · pode override)
- W-V1-UNIDADE dispara warning inline (não bloqueia)

Botões "← Voltar" / "Próximo · Agrupadores executivos".

### 3.8 · Estado `E4` · Agrupadores executivos · OPCIONAL (D-212)

Espelha conceitualmente a E4 "Agrupar" da V2 · mas para **agrupadores executivos** da V1 (não agrupadores de análise):

```
st.subheader("Agrupadores executivos")
st.caption("Opcional · quer ver o resultado consolidado por algum recorte?")
st.markdown("Quando configurado, gera tabela consolidada por filial / centro de custo / outro recorte na aba 'Resumo por Agrupador'.")

# Multiselect (até 5 · OPCIONAL · default vazio)
agrupadores_executivos = st.multiselect(
    "Agrupar Resumo por (0 a 5 colunas)",
    colunas_disponiveis,
    default=[],
    max_selections=5,
)

if not agrupadores_executivos:
    st.info("Nenhum agrupador executivo configurado · aba 'Resumo por Agrupador' não será gerada · análise consolidada disponível em 'Resumo Executivo'.")
```

**Validação para E5:** sempre válido (E4 inteira é opcional).

Botões "← Voltar" / "Próximo · Revisar e executar". Botão extra "Pular · ir direto para Revisar" disponível.

**Importante (D-212):** **paleta NÃO está aqui** · vai para o rodapé do RESULTADO espelhando V2.

### 3.9 · Estado `E5` · Revisar e executar

Espelha `_tela_e5` da V2 com 5 colunas-resumo:

```
st.subheader("Revisar e executar")
st.caption("Confira a configuração antes de processar.")

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(f"**Arquivo(s)**\n\n{nomes}\n\nAba(s): ...\n\nCaso: {caso_logico_user_facing}")
with c2:
    st.markdown(f"**Lados**\n\nOrigem: {origem_ux}\n\nComparado: {comparado_ux}")
with c3:
    st.markdown(f"**Agrupadores de match**\n\n{N} agrupadores\n\nChave: {rótulos}")
with c4:
    st.markdown(f"**Campos comparados**\n\n{M} campos\n\n{lista}")
with c5:
    st.markdown(f"**Agrupadores executivos**\n\n{K} configurados\n\n{lista ou '—'}")

st.divider()
col_a, col_b = st.columns(2)
with col_a:
    st.button("← Voltar")
with col_b:
    st.button("Processar análise", type="primary")
```

**Caso lógico user-facing**: "Origem em aba A · Comparado em aba B" (ABAS_DISTINTAS) ou "Mesma aba · em colunas distintas" (MESMA_ABA_EM_COLUNAS).

### 3.10 · Estado `PROCESSANDO` · spinner

Tela curta com spinner e mensagem rotativa:
1. "Lendo bases..."
2. "Validando apontamentos..."
3. "Inferindo caso lógico..."
4. "Casando registros..." (só em ABAS_DISTINTAS)
5. "Calculando diferenças..."
6. "Construindo Ponte de Conciliação..."
7. "Gerando Resumo Executivo..."

Não-cancelável. Erro fatal vira `ERRO`.

### 3.11 · Estado `RESULTADO` · 5 blocos executivos + rodapé com paleta

Espelha `_tela_resultado` da V2 (D-177 · D-175):

**Bloco 1 · Cabeçalho executivo:**
```
st.header("📊 Resultado da análise")
st.caption(f"Conciliação entre **{origem}** e **{comparado}** · gerada em {timestamp}")
```

**Bloco 2 · Números principais (4 st.metric):**
- Card 1: Total · {origem_ux} · `formatar_valor_por_unidade(soma_origem, unidade)` (capability 11)
- Card 2: Total · {comparado_ux}
- Card 3: Diferença líquida · com `delta`
- Card 4: Taxa de Conciliação Geral

(Em V1 o KPI primário **é a Taxa de Conciliação** · não os totais por campo · ajuste mínimo da estrutura V2 que privilegia totais. Solução: 4 cards permanecem · mas o card 4 é a Taxa · maior em destaque visual).

**Bloco 3 · Saúde da comparação · 6 categorias (ou 2 + 4 zerados):**
```
st.markdown("#### Saúde da comparação")
# Tabela com 6 linhas (ABAS_DISTINTAS) ou 2 ativas + 4 zeradas (MESMA_ABA_EM_COLUNAS)
# Coluna: Categoria · Casos · Participação
# Em ABAS_DISTINTAS: Conciliados · Divergentes valor · Saiu do {origem_ux} · Apareceu no {comparado_ux} · Duplicidade · Ambiguidade
# Em MESMA_ABA_EM_COLUNAS: Conciliados · Divergentes valor · (Saiu do/Apareceu no/Duplicidade/Ambiguidade aparecem com 0)
```

**Bloco 4 · Status da Ponte:**
```
# Banner colorido com status binário (✅ Fecha ou ⚠️ Resíduo)
# Sub-linha com microcopy contextual (P-V1 §2.3)
```

**Bloco 5 · Leitura qualitativa + qualidade:**
```
st.markdown("#### Leitura qualitativa")
st.write(v1_result.leitura_qualitativa.texto)

# Avisos
# (idêntico ao padrão V2 · expander "Ver detalhes do diagnóstico")
```

**Rodapé (D-175 · D-212):**
```
st.divider()
c1, c2, c3 = st.columns([1, 1, 2])
with c1:
    st.button("← Voltar")
with c2:
    st.selectbox("Paleta do Excel", PALETAS_DISPONIVEIS)  # ← AQUI · não na E4
with c3:
    st.download_button("📥 Baixar Excel", type="primary")

# Linha à parte
if st.button("🔄 Nova análise"):
    _reset_completo()
```

### 3.12 · Detalhes de estado · invalidação cascata

| Editar... | Invalida... |
|---|---|
| `vazio` (upload) | E1_OK, E2, E3, E4, E5, RESULTADO |
| E1_OK (abas) | E2, E3, E4, E5, RESULTADO |
| E2 (rótulos) | E3, E4, E5, RESULTADO |
| E3 (apontamentos) | E4, E5, RESULTADO |
| E4 (agrupadores executivos) | E5, RESULTADO |
| E5 (revisão) | RESULTADO |

**Implementação Streamlit:** `st.session_state` mantém estado de cada etapa · botão "Editar" reseta downstream para `None`. Padrão V2 herdado.

**Gate B.4 VVC (D-162):**
- Botão `Baixar Excel` no rodapé do RESULTADO é **separado** de aprovação
- Aprovação é evento de VV-V1 (6º quadrado)

### 3.13 · Checklist VVC derivado mecanicamente (D-148 · 5 templates)

Idêntico à S-V1 v1 §3.10 com adições por D-213:

#### Grupo A · Estrutura do upload e contrato

**Template `estrutura_saida`:**
- [ ] `ConciliacaoV1Result.visao == "V1"`
- [ ] `len(agrupadores_match)` ∈ [1, 5]
- [ ] `len(campos_comparados)` ∈ [1, 10]
- [ ] `len(classificacao_por_registro)` ≥ 1
- [ ] `sum(contagem_por_classificacao.values()) == len(classificacao_por_registro)`
- [ ] `len(valor_por_campo) == len(campos_comparados)`
- [ ] `len(pontes) == len([c for c in campos_comparados if c.unidade ∉ {PERCENTUAL, ADIMENSIONAL, RAZAO}])`
- [ ] `caso_logico_inferido` consistente com `aba_origem == aba_comparado`
- [ ] Em `MESMA_ABA_EM_COLUNAS`: contagens de SO_*, DUPLICIDADE, AMBIGUIDADE são todos `0`
- [ ] Em `MESMA_ABA_EM_COLUNAS`: `cobertura == None`

#### Grupo B · Match e classificação

**Template `contagem_categoria` + `contagem_exata`** · idêntico à S-V1 v1 §3.10 + adições:
- [ ] Em `ABAS_DISTINTAS`: 6 classificações estruturais possíveis
- [ ] Em `MESMA_ABA_EM_COLUNAS`: apenas CONCILIADO e DIVERGENTE_VALOR aparecem (4 outras = 0)
- [ ] Algoritmo de inferência §1.3 retorna o caso correto

#### Grupo C · Ponte e Status

Idêntico à S-V1 v1 §3.10:
- [ ] `pontes` não inclui campos PERCENTUAL/ADIMENSIONAL/RAZAO
- [ ] Cálculos da Ponte conforme §1.16
- [ ] `status_ponte_geral` derivado conforme §2.6

#### Grupo D · Bloqueios e warnings

**Template `bloqueio_emitido`:**
- [ ] B-V1-AGRUPADOR-ZERO bloqueia E3→E4 quando 0 agrupadores
- [ ] B-V1-CAMPO-ZERO bloqueia E3→E4 quando 0 campos
- [ ] B-V1-MESMA-COLUNA bloqueia quando `nome_origem == nome_comparado` na mesma aba
- [ ] B-V1-MISTURA-ABAS bloqueia quando apontamentos misturam abas inconsistentemente
- [ ] B-V1-CHAVE-INVALIDA dispara aviso + permite override
- [ ] B-V1-RESULTADO-EXCEDE bloqueia execução quando volume excede

**Template `warning_presente`:**
- [ ] W-V1-TOL emitido quando há tolerância absorvida
- [ ] W-V1-DUP emitido em ABAS_DISTINTAS · sempre 0 em MESMA_ABA_EM_COLUNAS com microcopy explicativa
- [ ] W-V1-AMB · idem
- [ ] W-V1-UNIDADE emitido quando tipo declarado divergente da inferência

#### Grupo E · Estrutura de exportação

Idêntico à S-V1 v1 §3.10.

#### Grupo F · Aprovação explícita da Usuária

Idêntico à S-V1 v1 §3.10.

#### Grupo G · Leiaute do app (NOVO · D-212)

- [ ] App usa layout top-down sem sidebar lateral
- [ ] Header tem 4 botões (Objetivo · Aplicar modelo · Salvar como modelo · Nova análise)
- [ ] Stepper horizontal aparece nos estados não-vazio e não-erro
- [ ] TED em expander "⚙️ Configurações avançadas" no topo · NÃO em sidebar
- [ ] Paleta no rodapé do RESULTADO · NÃO na E4
- [ ] E4 contém só "Agrupadores executivos" · não tem paleta nem nulos avançados

---

## Notas operacionais finais

### Para B-V1 (condicional · D-147)

`base_fundacao.xlsx` cobre cenários V1 inclusive Caso 3 (mesma aba em colunas) · cobertura matricial 2 casos lógicos × 6 classificações × 4 modos × 8 unidades. **Default · B-V1 dispensada**.

`casos_esperados.yaml` ganha entrada V1 com cenários específicos para os 2 casos lógicos.

### Para V-V1 (motor `visao_v1.py`)

Sessão Claude Code dedicada · gate da sessão:
- 100% testes verdes
- Cobertura matricial **2 casos lógicos × 6 classificações × 4 modos × 8 unidades**
- Algoritmo `inferir_caso_logico` testado isoladamente
- Bloqueios B-V1-MESMA-COLUNA e B-V1-MISTURA-ABAS testados

### Para A-V1 (app `app_v1.py`)

Sessão Claude Code dedicada · gate duplo D-174 · **prompt deve consumir `app_v2.py` como referência canônica explícita** (não `wireframe_v2.html` antigo · que era pré-implementação).

**Sanity check numérico explícito (C.D7):** Camada 2 inclui:
- TEMPO_HORAS · formato adaptativo
- PERCENTUAL · Q1.B (Ponte omitida)
- 2 casos lógicos (1 base ABAS_DISTINTAS · 1 base MESMA_ABA_EM_COLUNAS)
- Caso de `0 divergentes` (P-α.3-07)

### Para VV-V1

Modalidade C mista (D-156) · 3 pontos-chave canônicos com adição:
- Pós-processamento (RESULTADO) · KPI principal + Status Ponte + caso lógico declarado
- Pré-checklist · sem induzir resposta
- Pós-exportação (Excel) · 6 abas (ou 5 se sem agrupador executivo) · Coração Visual distribuído

### Decisões registradas nesta S-V1

**D-210 · Q1.B · Campos PERCENTUAL omitidos da Ponte** (ver S-V1 v1 · não alterada)

**D-211 · Q2.C · Épsilon TED por unidade global** (ver S-V1 v1 · não alterada)

**D-212 · Correções retroativas em P-V1 · 3 pontos consolidados** (NOVO)

**Contexto:** Durante produção da S-V1 v2 · 3 incoerências entre P-V1 e o leiaute canônico V2 (`app_v2.py` · suite 746/746 verde) foram identificadas:

1. **P-V1 §2.7 · stepper "4 etapas + Revisão":** preservado como verdadeiro · mas conteúdo da E4 estava errado (P-V1 §4.5 declarava "Bloco 1 Paleta")
2. **P-V1 §4.5 · Bloco 1 Paleta na E4:** contradiz D-175 §5.4 (paleta no rodapé do RESULTADO · trocável a qualquer momento sem reprocessar)
3. **P-V1 §4.5 · Bloco 3 TED em sidebar global D-153:** contradiz D-178 (TED em expander "⚙️ Configurações avançadas" no topo · sai da sidebar)

**Decisão:** P-V1 §2.7 e §4.5 corrigidas retroativamente para refletir o leiaute V2 canônico:

- **§2.7 mantido** · 4 etapas + Revisão é correto · stepper canônico V1: "1 · Escolher arquivo(s)" · "2 · Identificar lados" · "3 · Configurar análise" · "4 · Agrupadores executivos" · "Revisar e executar"
- **§4.5 corrigido** · E4 contém **somente** "Agrupadores executivos" (multiselect 0-5 · opcional · pode pular) · sem paleta · sem TED · sem nulos
- **§4.5 corrigido** · Paleta vai para **rodapé do RESULTADO** (selectbox + Baixar Excel · D-175 §5.4)
- **§4.5 corrigido** · TED vai para **expander "⚙️ Configurações avançadas" no topo** de cada tela (D-178)

**Razão:** P-V1 foi produzida sem leitura disciplinada de `app_v2.py` · gerou divergências silenciosas com o leiaute canônico que rodaria. Correções aplicadas a P-V1 antes de S-V1 ser aprovada · evita débito propagado para V-V1 e A-V1.

**Impacto:**
- P-V1 §2.7 microajustada (stepper V1 declarado com nomes literais)
- P-V1 §4.5 reescrita (E4 = só agrupadores executivos · paleta + TED removidas)
- P-V1 ganha §4.5-bis · "TED · expander no topo · paralelo D-178" como nova sub-seção
- P-V1 ganha §4.6-bis · "Paleta no rodapé do RESULTADO · paralelo D-175 §5.4"
- Sem mudança em vocabulário bilingue (microcopy preserva)
- Sem mudança em arquitetura de abas do Excel
- Wireframe HTML produzido nesta sessão reflete leiaute corrigido

**Referência canônica:** §3 desta S-V1 · `app_v2.py` `_render_header` + `_tela_e4` + `_tela_resultado`. D-175 + D-178 são origens.

---

**D-213 · 4 casos lógicos de upload · sistema infere automaticamente · sem radio "estrutura A/B"** (NOVO)

**Contexto:** S-V1 v1 declarava 2 estruturas de upload (Estrutura A · 2 arquivos · Estrutura B · 1 arquivo com 2 abas) com radio explícito na E1 · espelhando o que o DCV-V1 §3.1 sugeria. Erro: o DCV apresenta 2 estruturas de **upload físico** mas a S-V1 v1 colapsou isso com a **decisão lógica do confronto** (mesma aba vs abas distintas). Após reexplicação da Usuária · 4 casos lógicos foram identificados:

- **Caso 1** · 2 arquivos · Origem em aba A do arquivo 1 · Comparado em aba B do arquivo 2
- **Caso 2** · 1 arquivo (com N abas) · Origem em uma aba · Comparado em outra
- **Caso 3** · 1 arquivo · 1 aba · Origem e Comparado em **conjuntos de colunas distintos da mesma aba** (cada linha é par já casado por construção)
- **Caso 4** · 2 arquivos · 1 aba cada · em colunas (combinação rara · matematicamente válida)

Caso fora de escopo MVP (DCV §3.1 reafirmado): 1 aba · em linhas (coluna discriminadora) · exige RESHAPE prévio Módulo 2.

**Decisão:** A V1 separa fisicamente do logicamente:

- **E1 (upload):** decisão **física** · `n_arquivos ∈ {1, 2}` · radio simples
- **E1_OK (escolher abas):** Usuária escolhe 1 ou 2 abas conforme `n_arquivos`
- **E3 (configurar análise):** Usuária aponta agrupadores e campos com `(coluna_origem, coluna_comparado)` · sem radio explícito de "estrutura"
- **Sistema infere automaticamente** o caso lógico (`ABAS_DISTINTAS` ou `MESMA_ABA_EM_COLUNAS`) a partir dos apontamentos:
  - Se `aba_origem == aba_comparado` E todos os apontamentos têm `coluna_origem != coluna_comparado` → `MESMA_ABA_EM_COLUNAS`
  - Se `aba_origem != aba_comparado` → `ABAS_DISTINTAS`
- Casos especiais bloqueados:
  - `B-V1-MESMA-COLUNA` · apontamento com `coluna_origem == coluna_comparado` na mesma aba (não há comparação a fazer)
  - `B-V1-MISTURA-ABAS` · apontamentos inconsistentes (alguns na mesma aba · outros em distintas)

**Impacto no contrato:**
- `ConciliacaoRealizadaV1.estrutura_entrada` (S-V1 v1) → removido
- Adicionado `ConciliacaoRealizadaV1.n_arquivos: Literal[1, 2]`
- Adicionado `ConciliacaoRealizadaV1.caso_logico_inferido: CasoLogicoV1` (enum 2 valores)
- Pipeline (§2.1) ramifica em `[4-A]` (ABAS_DISTINTAS · executa match) e `[4-B]` (MESMA_ABA_EM_COLUNAS · pareamento linha-a-linha)
- Classificações estruturais variam: 6 classes em ABAS_DISTINTAS · 2 ativas + 4 zerados em MESMA_ABA_EM_COLUNAS
- `cobertura == None` em MESMA_ABA_EM_COLUNAS (cobertura é trivialmente 100% · None preserva semântica de "não aplicável")

**Razão:** O caso 3 (colunas distintas na mesma aba) é caso muito comum em conciliação contábil real · cliente típico tem `Razao_Out2025` em uma aba com colunas `[CNPJ, Filial, Valor_Razao, Valor_Balancete]` · não precisa nem deveria ser obrigado a fazer RESHAPE. S-V1 v1 errou ao classificar isso como "fora de escopo". Mas o caso fora de escopo (DCV §3.1 · "em linhas com discriminador") permanece fora · esse exige RESHAPE prévio.

**Inferência automática vs declaração explícita:** Usuária não declara o caso · sistema infere. Razão: cliente já está fazendo o trabalho conceitual quando aponta colunas (sabe se é mesma aba ou abas distintas) · radio extra seria redundância. Princípio C.5 atendido (sistema preserva e classifica · não inventa estrutura · só observa apontamentos).

**Referência canônica:** §1.2 (`ConciliacaoRealizadaV1`) · §1.3 (enum `CasoLogicoV1`) · §2.1 (pipeline 2 ramos) · §2.5 (bloqueios novos) · §3.1 (estados macro) · §3.4-3.7 (telas que materializam o fluxo) · DCV-V1 §3.1 (mantido como referência · com correção do entendimento "mesma aba em colunas dentro do escopo").

---

### Pendências P-V1-TEC abertas (3)

| Código | Tema | Resolução |
|---|---|---|
| `P-V1-TEC-01` | Microcopy completa do `PonteCampoV1.microcopy_status` | A-V1 cleanup |
| `P-V1-TEC-02` | Validação Pydantic cruzada `tipo_logico` ↔ `unidade` · gera W-V1-UNIDADE | V-V1 implementação |
| `P-V1-TEC-03` | Ordenação determinística de `LinhaResumoAgrupadorV1` quando 2+ agrupadores executivos · empate alfabético | V-V1 implementação |

---

## Status e aprovação

**Status:** aguardando aprovação da Usuária.

**Aprovação destrava:** B-V1 (condicional · provavelmente dispensada) ou V-V1 diretamente.

**Após aprovação:**

1. S-V1 v2 vira `/specs/spec_v1.md` (canônico)
2. Wireframe HTML v2 produzido como anexo (`/specs/wireframes/v1.html` · espelho fiel V2)
3. P-V1 §2.7 e §4.5 corrigidas retroativamente conforme D-212 · vira `/specs/produto/p_v1.md` v1.1
4. `vocabulario_bilingue.md` v4 ganha extensão · Bloco 2 entrada `V1_DUAL`
5. Planilha aba 2 V1 vira `✅✅⬜⬜⬜⬜` (2º quadrado verde)
6. DECISIONS ganha D-210 · D-211 · D-212 · D-213
7. Sessão V-V1 abre · 3º quadrado · sessão combinada Claude Code

---

## Referências

- **DCV-V1:** `/specs/dcv/dcv_v1.md` · 13 pendências fechadas · entendimento "mesma aba em colunas" reafirmado dentro do escopo (D-213)
- **P-V1:** `/specs/produto/p_v1.md` · D-209 · §2.7 e §4.5 corrigidas em D-212
- **Mockup-V1:** `MOCKUP_V1_alpha2.md` · D-208
- **Vocabulário bilingue:** `/specs/vocabulario_bilingue.md` v4
- **CONTEXT v3.5:** §15.3 · §15.12 · §13 · §9 Camada C
- **App V2 canônico:** `app_v2.py` · suite 746/746 verde · referência canônica de leiaute (não `wireframe_v2.html` que era pré-implementação)
- **Decisões consumidas:** D-130 · D-148 · D-149 · D-156 · D-158 · D-160 · D-161 · D-162 · D-165 · D-166 · D-167 · D-168 · D-174 · **D-175 (paleta no rodapé)** · **D-178 (TED em expander)** · D-179 · D-185 · D-190 · D-194 · D-202 · D-203 · D-204 cláusula A · D-205 · D-206 · D-209
- **F-APRESENT capabilities consumidas:** 1 · 2 · 3 · 4 · 5 · 7 · 8 · 9 · 10 · 11

---

*Esta S-V1 v2 é fonte autoritativa de contratos lógicos · regras de cálculo · pipeline determinístico (2 ramos) · catálogo de bloqueios e warnings · TED V1 · wireframe funcional textual e checklist VVC derivado da V1 · espelhando estrutura canônica do app V2. A partir de sua aprovação, nenhuma decisão técnica da V1 pode ser alterada sem nova decisão formal registrada em DECISIONS.md.*
