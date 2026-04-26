# spec_v2.md — Análise Comparativa entre Referências

**Visão:** V2 · Família A · Confronto entre universos
**Bloco:** S-V2 · primeira visão da Fase 2 · ciclo de 6 artefatos (§15 CONTEXT pós-D-158)
**Versão:** v1.1 · adendo retroativo aplicado em 23/04/2026 · noite (Sessão 2 da fila V2 retroativa · ALINHA-Retroação-V2 antecipada · D-167)
**DCV consumido:** `/specs/dcv/dcv_v2.md` · aprovado 18/04/2026 · 13 pendências fechadas (D-021 a D-032)
**P-VN consumida:** `/specs/produto/p_v2.md` · aprovada 23/04/2026 · noite · primeira aplicação operacional do ciclo de 6 artefatos (D-158) · fonte autoritativa de paleta · vocabulário user-facing · arquitetura de abas · contrato de unidade por campo · microcopy · checklist user-facing
**Status:** **aprovada** pela Usuária · tripla aprovação B.2 (contrato + wireframe funcional + wireframe HTML `/specs/wireframe_v2.html` · D-149) · refinada em 22/04/2026 com D-151 (semântica dupla de `campo_analisado` por estrutura · §1.2 e §2.5) emergente de V-V2 · 291/291 testes verdes · refinada em 23/04/2026 manhã com D-153 (TED renderizado em sidebar global em vez de expander na E3 · nota técnica em §3.5) e D-154 (bloco intermediário RESOL_CASO parqueado como P-V2-Evo-01 · motor V2 atual não pré-detecta casos estruturais · nota técnica em §3.7) emergentes de A-V2 · 301/301 testes verdes (291 V-V2 + 10 A-V2) · **refinada em 23/04/2026 noite com D-165** (fusão Parâmetros+Diagnóstico em 1 aba única · §2.9 reescrita · 5 → 4 abas) **· D-166** (contrato de unidade por campo · §2.4-bis NOVA · nota em §2.8 sobre rendering user-facing dos 6 blocos) **· D-168** (Azul executivo é default universal · paleta declarada em P-V2 §1.1 · sem impacto direto nesta Spec técnica · referência cruzada apenas)

**Convenção de versionamento:** numeração de seções existentes preservada. Adendos retroativos pós-aprovação usam sufixo `-bis` (ex: §2.4-bis) para sinalizar inserção pós-aprovação sem renumerar conteúdo original. Especificação canônica de produto vive em P-V2; esta Spec técnica é fonte canônica de contrato lógico e regras de cálculo (regra de conflito CONTEXT §5).

---

## Preâmbulo operacional

Declarações executivas consumidas pelo motor e pela exportação antes da Seção 1. Não substitui as 3 seções canônicas B.2 — é cabeçalho orientador.

| Item | Valor |
|---|---|
| Subclasse de resultado | `V2Result(VNResultBase)` · Seção 1.1 |
| Coração Visual (D-126) | **"Matriz de Confronto"** · tipo `MATRIZ_COLORIDA` · retroação diferida cumprida · ratificado por `V2-A03` do `casos_esperados.yaml` |
| Modo da base (CPCO · C.D1) | **Transacional** (default) · `T-AGRUPA` opera consolidação real · modo **Pré-agregado** aceito via escolha do usuário em E3 quando campo numérico não-aditivo com chave unitária declarada |
| Thresholds editáveis (TED · C.D2) | 4 thresholds declarados · Seção 2.6 |
| Base consumida (D-147) | **`base_fundacao.xlsx`** · abas `vendas_padrao` (principal) e `vendas_por_colunas` (Modo POR_COLUNAS · Modo 4 em aba secundária) · **B-V2 dispensado** (3 perguntas OK) |
| Recorte cliente-friendly (D-149) | `/bases/base_v2_cliente.xlsx` · reempacotamento das 2 abas acima · gerado por `/src/geradores/gerar_base_cliente.py` |
| Wireframe visual (D-149) | `/specs/wireframe_v2.html` · obrigatório Família A · aprovação simultânea |
| Transversais consumidos | `T-AGRUPA` · `T-PIVOT` · `T-SEMA` · `T-DIAG` · `T-MODELO` (5 dos 12) |
| Padrões §13 aplicados | 13.1 · 13.2 · 13.3 · 13.5 (6 blocos) · 13.6 (Coração Visual) · **13.4 não aplicável** (V2 é caso base da Família A · V1 não é view especializada · CONTEXT §4) |
| Bloqueios MBO (C.D4) | 8 códigos `B-V2-*` · Seção 2.5 |
| Warnings | 12 códigos `W-V2-*` · Seção 2.7 |

---

## Seção 1 · Contratos lógicos

Todos os contratos Pydantic aplicam os 3 requisitos D-130 integrais (visão analítica): `model_config` com `use_enum_values=False` e enums serializados como string · `Field(..., description=...)` em todo campo · método `.para_contexto_ia()` herdado de `VNResultBase` sem re-override (D-144 · V2Result é analítico, não operacional).

### 1.1 · `V2Result` — contrato principal

```python
from typing import Literal, List, Dict, Any, Optional, Union
from pydantic import BaseModel, ConfigDict, Field
import pandas as pd
from contratos import VNResultBase, BloqueioOperacional, WarningEstrutural


class V2Result(VNResultBase):
    """
    Resultado da V2 · Análise Comparativa entre Referências.
    Estende VNResultBase (D-130 · BAD · MBO · Coração Visual já inclusos).
    """
    model_config = ConfigDict(arbitrary_types_allowed=True, use_enum_values=False)

    # ---- Identificação fixa da visão ----
    visao_id: Literal["V2"] = Field(
        "V2",
        description="Identificador fixo · V2 · única visão que produz este contrato"
    )

    # ---- Campos V2-específicos ----
    comparacao_realizada: "ComparacaoV2" = Field(
        ...,
        description="Declaração da comparação executada · Origem · Comparado · estrutura · campo · semântica"
    )

    agrupadores_aplicados: List[str] = Field(
        ...,
        description="Lista ordenada dos agrupadores efetivamente usados · 1 a 9 · D-027"
    )

    resolucao_estrutural: Optional["ResolucaoEstruturalV2"] = Field(
        None,
        description="Decisão do usuário em caso estrutural detectado na transição E4→E5 · D-021 · None se nenhum caso detectado"
    )

    distribuicao_classificacoes_estruturais: Dict[str, int] = Field(
        ...,
        description="Contagem das 6 categorias: PRESENTE_AMBOS · AUSENTE_ORIGEM · AUSENTE_COMPARADO · NULO_ORIGEM · NULO_COMPARADO · NULO_AMBOS · categorias com 0 preservadas no contrato · omitidas apenas na exibição"
    )

    distribuicao_classificacoes_semanticas: Optional[Dict[str, int]] = Field(
        None,
        description="Contagem Positivo / Negativo / Neutro / Não aplicável · None quando tipo de campo é Estado/Situação (não tem semântica numérica)"
    )

    numeros_ancora: "NumerosAncoraV2" = Field(
        ...,
        description="4 KPIs do Bloco 2 do Resumo Executivo · estrutura depende do tipo do campo"
    )

    top_variacoes: List["LinhaTopVariacao"] = Field(
        ...,
        description="Top 10 combinações por |Δ| (tipos numéricos) ou top 10 combinações que mudaram (Estado/Situação) · Bloco 4 do Resumo Executivo"
    )

    modelo_aplicado: Optional["ModeloAplicadoV2"] = Field(
        None,
        description="Referência a T-MODELO quando modelo salvo foi aplicado · None se execução fresca"
    )

    # ---- base_analitica · resumo_executivo · coracao_visual · bloqueios_disparados
    # ---- warnings · diagnostico · timestamp_execucao · config_usada · motor_result_meta
    # ---- todos herdados de VNResultBase · D-130 integral ----
```

### 1.2 · `ComparacaoV2` · declaração da comparação executada

```python
class ComparacaoV2(BaseModel):
    model_config = ConfigDict(use_enum_values=False)

    estrutura_entrada: Literal["POR_COLUNAS", "POR_LINHAS"] = Field(
        ...,
        description="POR_COLUNAS quando Origem e Comparado são colunas · POR_LINHAS quando são valores de uma coluna discriminadora"
    )

    origem_rotulo_tecnico: str = Field(
        ...,
        description="Nome da coluna (POR_COLUNAS) ou valor da coluna discriminadora (POR_LINHAS) · Origem"
    )
    comparado_rotulo_tecnico: str = Field(
        ...,
        description="Nome da coluna (POR_COLUNAS) ou valor da coluna discriminadora (POR_LINHAS) · Comparado"
    )
    origem_rotulo_ux: str = Field(
        ...,
        description="Rótulo amigável editável pela Usuária · exibido como 'Comparar de: {ux}'"
    )
    comparado_rotulo_ux: str = Field(
        ...,
        description="Rótulo amigável editável pela Usuária · exibido como 'Comparar com: {ux}'"
    )

    coluna_discriminadora: Optional[str] = Field(
        None,
        description="Nome da coluna discriminadora · obrigatório quando estrutura_entrada=POR_LINHAS · None em POR_COLUNAS"
    )
    modo_4_ativado: bool = Field(
        False,
        description="True quando coluna_discriminadora tem >2 valores únicos e usuário escolheu 2 · D-026"
    )
    estados_nao_escolhidos: List[str] = Field(
        default_factory=list,
        description="Valores da coluna discriminadora excluídos quando modo_4_ativado · registrados no Diagnóstico · vazio em modo normal"
    )

    campo_analisado: str = Field(
        ...,
        description=(
            "Nome do campo sobre o qual Δ e Δ% são calculados. "
            "Semântica dupla por estrutura (D-151): "
            "em POR_LINHAS é nome de coluna real do DataFrame (ex: 'Vendas'); "
            "em POR_COLUNAS é nome conceitual do campo comparado (ex: 'Receita' "
            "quando origem_rotulo_tecnico='Receita_Orcado' e "
            "comparado_rotulo_tecnico='Receita_Realizado') · não corresponde a "
            "coluna real do df nesta estrutura."
        )
    )
    tipo_campo: Literal[
        "NUMERICO_ADITIVO", "NUMERICO_RELATIVO", "NUMERICO_NAO_ADITIVO", "ESTADO_SITUACAO"
    ] = Field(
        ...,
        description="4 tipos canônicos · D-025 · determina comportamento de cálculo e consolidação"
    )
    semantica_campo: Literal["MAIOR_MELHOR", "MENOR_MELHOR", "NEUTRO"] = Field(
        ...,
        description="Semântica via T-SEMA · determina cor/classificação Positivo/Negativo/Neutro · irrelevante para ESTADO_SITUACAO"
    )

    regra_agregacao: Literal["SOMA", "MEDIA", "MAXIMO", "MINIMO", "CONTAGEM"] = Field(
        "SOMA",
        description="Regra T-AGRUPA · default SOMA para NUMERICO_ADITIVO · configurável"
    )
    metodo_consolidacao_relativo: Optional[Literal[
        "MEDIA_SIMPLES", "MEDIA_PONDERADA", "NAO_CONSOLIDAR"
    ]] = Field(
        None,
        description="Obrigatório para NUMERICO_RELATIVO e NUMERICO_NAO_ADITIVO · D-024 · default declarado MEDIA_SIMPLES · None para ADITIVO e ESTADO_SITUACAO"
    )
    campo_peso: Optional[str] = Field(
        None,
        description="Nome do campo de peso · obrigatório quando metodo_consolidacao_relativo=MEDIA_PONDERADA · None caso contrário"
    )
```

### 1.3 · `ResolucaoEstruturalV2` · decisão do usuário em caso estrutural

```python
class ResolucaoEstruturalV2(BaseModel):
    model_config = ConfigDict(use_enum_values=False)

    tipo_caso: Literal[
        "NIVEL_AGRUPAMENTO_DIFERENTE",
        "COLUNA_PRESENTE_EM_UM_LADO",
        "TIPO_CAMPO_INCOMPATIVEL",
        "VALOR_UNICO_DIVERGENTE",
        "ORDEM_MAGNITUDE_DIVERGENTE",
    ] = Field(..., description="Tipo do caso estrutural detectado · D-021")

    opcoes_oferecidas: List[str] = Field(
        ...,
        description="Opções específicas apresentadas ao usuário no painel de resolução · fechadas por tipo de caso"
    )
    escolha_usuario: str = Field(..., description="Opção efetivamente escolhida pelo usuário")

    contexto_caso: Dict[str, Any] = Field(
        default_factory=dict,
        description="Valores observados que dispararam o caso · nomes de coluna · contagens · amostras"
    )

    registrada_como: Literal["DECISAO_USUARIO"] = Field(
        "DECISAO_USUARIO",
        description="Fixo · D-021 · registrada no Diagnóstico como DECISAO_USUARIO · distinta de AJUSTE_LEVE"
    )
```

### 1.4 · `NumerosAncoraV2` · 4 KPIs do Bloco 2 (Resumo Executivo)

```python
class NumerosAncoraV2(BaseModel):
    """
    Bloco 2 do Resumo Executivo · 4 KPIs em destaque · D-031.
    Estrutura varia conforme tipo_campo · discriminator via tipo_campo de ComparacaoV2.
    """
    model_config = ConfigDict(use_enum_values=False)

    # Variante numérica (NUMERICO_ADITIVO · NUMERICO_RELATIVO · NUMERICO_NAO_ADITIVO)
    total_origem: Optional[float] = Field(
        None,
        description="Total consolidado da Origem · None para ESTADO_SITUACAO"
    )
    total_comparado: Optional[float] = Field(
        None,
        description="Total consolidado do Comparado · None para ESTADO_SITUACAO"
    )
    diferenca_total: Optional[float] = Field(
        None,
        description="total_comparado - total_origem · None para ESTADO_SITUACAO"
    )
    variacao_total_pct: Optional[float] = Field(
        None,
        description="diferenca_total / total_origem · None quando total_origem = 0 ou ESTADO_SITUACAO"
    )

    # Variante ESTADO_SITUACAO (substitui os 4 KPIs numéricos quando tipo é ESTADO_SITUACAO)
    total_combinacoes_analisadas: Optional[int] = Field(
        None,
        description="Contagem de combinações analisadas · preenchido apenas para ESTADO_SITUACAO"
    )
    combinacoes_com_mudanca: Optional[int] = Field(
        None,
        description="Combinações em que estado Origem ≠ estado Comparado · apenas para ESTADO_SITUACAO"
    )
    combinacoes_estaveis: Optional[int] = Field(
        None,
        description="Combinações em que estado Origem = estado Comparado · apenas para ESTADO_SITUACAO"
    )
    pct_mudanca: Optional[float] = Field(
        None,
        description="combinacoes_com_mudanca / total_combinacoes_analisadas · apenas para ESTADO_SITUACAO"
    )
```

Invariante de preenchimento: exatamente um dos dois grupos é preenchido (numérico · 4 primeiros campos) ou (estado · 4 últimos campos). Validação no motor antes de instanciar.

### 1.5 · `LinhaTopVariacao` · linha do top 10 (Bloco 4 RE)

```python
class LinhaTopVariacao(BaseModel):
    model_config = ConfigDict(use_enum_values=False)

    chave_agrupadores: Dict[str, Any] = Field(
        ...,
        description="Valores dos agrupadores que identificam a combinação · ex: {'Filial': 'SP', 'Produto': 'A'}"
    )
    valor_origem: Optional[float] = Field(
        None,
        description="None quando AUSENTE_ORIGEM ou NULO_ORIGEM · D-022/D-023 · preserva invisibilidade vs. zero inventado (C.5)"
    )
    valor_comparado: Optional[float] = Field(None, description="None quando AUSENTE_COMPARADO ou NULO_COMPARADO")
    diferenca: Optional[float] = Field(None, description="None quando qualquer lado ausente ou nulo · nunca 0 inventado")
    variacao_percentual: Optional[float] = Field(
        None,
        description="None para qualquer AUSENTE/NULO · None quando valor_origem=0 e valor_comparado≠0 · dispara W-V2-BZ"
    )
    classificacao_estrutural: Literal[
        "PRESENTE_AMBOS", "AUSENTE_ORIGEM", "AUSENTE_COMPARADO",
        "NULO_ORIGEM", "NULO_COMPARADO", "NULO_AMBOS"
    ] = Field(..., description="Uma das 6 categorias mutuamente exclusivas · D-022/D-023")
    classificacao_semantica: Optional[Literal["POSITIVO", "NEGATIVO", "NEUTRO", "NAO_APLICAVEL"]] = Field(
        None,
        description="Aplicada quando tipo_campo é numérico · None quando ESTADO_SITUACAO · NAO_APLICAVEL quando variacao_percentual é None"
    )
    estado_origem: Optional[str] = Field(
        None,
        description="Estado textual da Origem · preenchido apenas quando tipo_campo=ESTADO_SITUACAO"
    )
    estado_comparado: Optional[str] = Field(
        None,
        description="Estado textual do Comparado · preenchido apenas quando tipo_campo=ESTADO_SITUACAO"
    )
```

### 1.6 · `ModeloAplicadoV2` · referência a T-MODELO

```python
class ModeloAplicadoV2(BaseModel):
    model_config = ConfigDict(use_enum_values=False)

    nome_modelo: str = Field(..., description="Nome salvo do modelo T-MODELO aplicado")
    data_criacao_modelo: datetime = Field(..., description="Data de criação original do modelo")
    campos_casados: int = Field(..., description="Quantidade de campos do modelo que casaram com a nova base")
    campos_nao_casados: List[str] = Field(
        default_factory=list,
        description="Lista de campos do modelo sem correspondência · vazio quando 100% casou"
    )
    tipo_aplicacao: Literal["COMPLETA", "PARCIAL", "INCOMPATIVEL"] = Field(
        ...,
        description="COMPLETA quando todos os campos casaram · PARCIAL dispara W-V2-MOD-PARCIAL · INCOMPATIVEL dispara W-V2-MOD-INCOMP e zera etapas dependentes"
    )
```

### 1.7 · Contratos consumidos da Fundação (referência sem redeclaração)

| Contrato | Fonte | Uso em V2 |
|---|---|---|
| `VNResultBase` | `contratos.py` | Classe base · carrega D-130 integral |
| `BloqueioOperacional` | `contratos.py` · D-134 | Instanciado 8× no catálogo B-V2-* (Seção 2.5) |
| `WarningEstrutural` | `contratos.py` | Instanciado até 12× no catálogo W-V2-* (Seção 2.7) |
| `DiagnosticoVN` | `contratos.py` | Preenchido por T-DIAG · alimenta aba Diagnóstico (última aba · D-017) |
| `ResumoExecutivoPadrao` | `contratos.py` · D-125 | 6 blocos preenchidos pela V2 (Seção 2.8) |
| `CoracaoVisualRef` | `contratos.py` · D-126 | `nome_aba="Matriz de Confronto"` · `tipo="MATRIZ_COLORIDA"` |
| `MotorResultMeta` | `contratos.py` | Subset do MotorResult sem o DataFrame · populado pelo motor_base antes do V-V2 |
| `AjusteMotor` | `contratos.py` | Usado em `DECISAO_USUARIO` (D-021) · alimenta diagnostico.ajustes |

---

## Seção 2 · Regras de cálculo

Pipeline determinístico (C.1) · cada etapa declarada com entrada e saída · zero invenção de comportamento (C.3).

### 2.1 · Pipeline canônico end-to-end

```
[motor_upload + motor_base produziu base_processada + column_meta]
                        │
                        ▼
      ┌─────────────────────────────────────────┐
      │ Etapa A · Preparação da base             │
      │ · se POR_LINHAS: T-PIVOT(semântica 1)    │
      │   converte para POR_COLUNAS              │
      │ · se POR_COLUNAS: no-op                  │
      │ · Modo 4 aplicado ANTES do pivot         │
      │   (filtra coluna discriminadora aos      │
      │   2 valores escolhidos)                  │
      └─────────────────────────────────────────┘
                        │
                        ▼
      ┌─────────────────────────────────────────┐
      │ Etapa B · Detecção de casos              │
      │ estruturais (D-021)                      │
      │ · 5 tipos taxativos · Seção 2.4          │
      │ · se detectado: para e abre painel       │
      │ · se resolvido: ResolucaoEstruturalV2    │
      │   registrada em diagnostico como         │
      │   DECISAO_USUARIO                        │
      │ · inconsistências leves (4 tipos) são    │
      │   ajustadas automaticamente como         │
      │   AJUSTE_LEVE em diagnostico             │
      └─────────────────────────────────────────┘
                        │
                        ▼
      ┌─────────────────────────────────────────┐
      │ Etapa C · Consolidação pré-cálculo       │
      │ (CPCO · C.D1)                            │
      │ · modo Transacional: T-AGRUPA real       │
      │   com regra_agregacao declarada          │
      │ · modo Pré-agregado: T-AGRUPA no-op      │
      │   valida unicidade de chave              │
      │   (agrupadores + estado) · duplicata     │
      │   → W-V2-PAGREG-DUP · motor recai        │
      │   em SOMA                                │
      │ · tipo NUMERICO_RELATIVO ou              │
      │   NUMERICO_NAO_ADITIVO: aplica           │
      │   metodo_consolidacao_relativo           │
      │   (D-024 · MEDIA_SIMPLES default)        │
      │ · nulo em agrupador → rótulo             │
      │   '(sem valor)' · D-023                  │
      └─────────────────────────────────────────┘
                        │
                        ▼
      ┌─────────────────────────────────────────┐
      │ Etapa D · Cálculo comparativo            │
      │ · outer join (agrupadores) entre         │
      │   consolidado Origem e consolidado       │
      │   Comparado                              │
      │ · classificação estrutural 6 categorias  │
      │   (D-022/D-023 · Seção 2.2)              │
      │ · Δ e Δ% com regras de None              │
      │   (nunca zero inventado · C.5)           │
      │ · base_analitica produzida (BAD · C.D3)  │
      └─────────────────────────────────────────┘
                        │
                        ▼
      ┌─────────────────────────────────────────┐
      │ Etapa E · Camada semântica (T-SEMA)      │
      │ · apenas tipos numéricos                 │
      │ · aplica MAIOR_MELHOR / MENOR_MELHOR /   │
      │   NEUTRO sobre Δ                          │
      │ · classifica em Positivo / Negativo /    │
      │   Neutro / Não aplicável                 │
      │ · limiar de estabilidade: ±1% default    │
      │   (TED · editável · Seção 2.6)           │
      │ · tipo ESTADO_SITUACAO pula esta etapa   │
      └─────────────────────────────────────────┘
                        │
                        ▼
      ┌─────────────────────────────────────────┐
      │ Etapa F · Agregações para exportação     │
      │ · Bloco 2 · NumerosAncoraV2              │
      │ · Bloco 3 · distribuicao estruturais     │
      │ · Bloco 4 · top 10 variações             │
      │ · Bloco 5 · distribuicao semântica +     │
      │   leitura qualitativa com TED            │
      │ · Bloco 6 · qualidade estrutural (BAD)   │
      │ · T-DIAG preenche diagnostico            │
      └─────────────────────────────────────────┘
                        │
                        ▼
      V2Result instanciado · valida invariantes · devolvido
```

### 2.2 · Classificação estrutural · 6 categorias mutuamente exclusivas (D-022 · D-023)

Para cada linha do outer join (chave = tupla de agrupadores):

| Origem presente? | Comparado presente? | Origem nulo? | Comparado nulo? | Classificação | `valor_origem` | `valor_comparado` |
|---|---|---|---|---|---|---|
| sim | sim | não | não | `PRESENTE_AMBOS` | valor | valor |
| sim | sim | **sim** | não | `NULO_ORIGEM` | `None` | valor |
| sim | sim | não | **sim** | `NULO_COMPARADO` | valor | `None` |
| sim | sim | **sim** | **sim** | `NULO_AMBOS` | `None` | `None` |
| não | sim | — | — | `AUSENTE_ORIGEM` | `None` | valor |
| sim | não | — | — | `AUSENTE_COMPARADO` | valor | `None` |

Regras de `diferenca` e `variacao_percentual`:

| Caso | diferenca | variacao_percentual |
|---|---|---|
| `PRESENTE_AMBOS` · origem ≠ 0 | `valor_comparado - valor_origem` | `(comp - orig) / orig` |
| `PRESENTE_AMBOS` · origem = 0 · comparado ≠ 0 | `valor_comparado` | `None` · dispara `W-V2-BZ` |
| `PRESENTE_AMBOS` · ambos = 0 | `0.0` | `0.0` (estável) |
| qualquer AUSENTE_* | `None` | `None` |
| qualquer NULO_* | `None` | `None` |

**Proibido em qualquer cenário:** inventar 0 para lado ausente · tratar `None` como zero · aplicar `-100%` para ausência · C.5 + D-022 + D-023.

### 2.3 · Consolidação pré-cálculo (CPCO · C.D1) · modo da base

| Modo | Quando aplica | Operação |
|---|---|---|
| **Transacional** (default) | Base tem múltiplas linhas por chave-agrupadores · operação agregável | T-AGRUPA real · aplica `regra_agregacao` · resultado: 1 linha por chave por estado |
| **Pré-agregado** | Base já tem 1 linha por chave-agrupadores · usuário declara explicitamente em E3 | T-AGRUPA no-op com validação · se duplicata de chave detectada → `W-V2-PAGREG-DUP` · motor recai em `SOMA` · registra em diagnostico |

Tipos relativo e não-aditivo seguem `metodo_consolidacao_relativo` (D-024):

- `MEDIA_SIMPLES` (default declarado) · aplica média aritmética sobre os valores consolidáveis
- `MEDIA_PONDERADA` · requer `campo_peso` · dispara `B-V2-PESO-INVALIDO` se pesos zerados ou negativos
- `NAO_CONSOLIDAR` · motor recusa agrupadores > 0 · B-V2-CONSOL-IMPOSSIVEL (Seção 2.5)

Dispara `W-V2-AGG` (informativa) sempre que tipo é relativo ou não-aditivo e há ≥1 agrupador · registra no diagnostico o método aplicado · C.2.

### 2.4 · Casos estruturais e inconsistências leves (D-021)

**4 inconsistências leves · motor ajusta sem perguntar · registra como `AJUSTE_LEVE`:**

1. Ordem de colunas diferente entre lados
2. Normalização textual (espaços · acentos · case) quando conteúdo é idêntico após normalização
3. Tipos numéricos compatíveis (int ↔ float · mesma escala)
4. Linhas em branco ou nulos isolados dentro de coluna

**5 casos estruturais · motor para · abre painel · registra como `DECISAO_USUARIO`:**

| Tipo | Condição de disparo | Opções oferecidas |
|---|---|---|
| `NIVEL_AGRUPAMENTO_DIFERENTE` | Um lado tem granularidade mais fina que o outro para os agrupadores escolhidos | (a) agregar lado fino · (b) escolher nível comum · (c) cancelar |
| `COLUNA_PRESENTE_EM_UM_LADO` | Agrupador existe apenas em um lado | (a) remover da análise · (b) cancelar |
| `TIPO_CAMPO_INCOMPATIVEL` | Campo analisado tem tipos estruturais diferentes entre lados (ex: NUMERICO de um lado · CATEGORICO do outro) | (a) tratar como ESTADO_SITUACAO · (b) cancelar |
| `VALOR_UNICO_DIVERGENTE` | Em POR_LINHAS Modo 4 · valor escolhido pelo usuário não existe na base efetivamente processada | (a) escolher outro valor · (b) cancelar |
| `ORDEM_MAGNITUDE_DIVERGENTE` | Total de um lado é ≥ 1000× o do outro (possível unidade divergente) | (a) seguir mesmo assim · (b) rever base · (c) cancelar |

Zero comportamento padrão para esses 5 casos (C.3) · sempre painel · sempre escolha explícita.

### 2.4-bis · Contrato de unidade por campo (D-166 · adendo retroativo)

**Origem da seção:** adendo aplicado em 23/04/2026 noite na Sessão 2 da fila V2 retroativa (ALINHA-Retroação-V2 antecipada · D-167). Decisão D-166 (ALINHA-Descoberta-Camada-Produto · 23/04/2026 manhã) tornou contrato de unidade por campo requisito invariante de toda exportação Excel · S-V2 original (aprovada 22/04/2026) não tinha. Esta §2.4-bis fecha a lacuna sem renumerar §2.4 (Casos estruturais · D-021) já existente.

**Fonte canônica de produto:** P-V2 §3.5 (`/specs/produto/p_v2.md`). Em caso de divergência entre esta §2.4-bis e P-V2 §3.5, **P-V2 §3.5 prevalece** (regra de conflito CONTEXT §5 · P-VN é fonte canônica de produto · S-VN é fonte canônica de contrato lógico). Esta seção declara o contrato em vocabulário técnico para consumo do motor e da exportação · P-V2 §3.5 declara em vocabulário user-facing para consumo da camada de produto.

**Princípio operacional (D-166):** todo campo exportado em qualquer aba tabular (Matriz de Confronto · Base Analítica) tem **unidade declarada** + **função de total declarada**. Ausência de declaração = bug de Spec · não se exporta campo sem contrato. F-APRESENT capability 4 (formatação monetária BR) e capability 5 (formatação percentual com conversão fração→%) consomem este contrato como entrada determinística (C.1 · C.D2).

**7 unidades canônicas do projeto** (referência cross-visão · CONTEXT §13.7):

| Unidade | Tipo de dado | Formato Excel (number_format) | Conversão na exportação |
|---|---|---|---|
| `monetario_br` | `float` | `R$ #,##0.00;[Red](R$ #,##0.00);-` | Nenhuma · valor já é a quantia em reais |
| `percentual` | `float` (fração entre 0 e 1) | `0.00%;[Red]-0.00%;-` | **Fração → percentual** aplicada por F-APRESENT capability 5 (Excel multiplica por 100 internamente quando number_format é `%`) |
| `contagem` | `int` | `#,##0` | Nenhuma |
| `texto` | `str` | `@` | Nenhuma · `None` exibido como `—` (Bloco 8 do `vocabulario_bilingue.md` v2) |
| `data` | `datetime` | `dd/mm/yyyy` | Nenhuma · cru `datetime.datetime(...)` proibido em superfície cliente (Bloco 7 do `vocabulario_bilingue.md` v2) |
| `classificacao` | `str` (enum user-facing) | Texto + badge (capability 8 P1) | Substituição dinâmica enum técnico → rótulo amigável (Bloco 3 estendido do `vocabulario_bilingue.md` v2) |
| `booleano` | `bool` | Texto · "Sim" / "Não" / "—" | `True` → "Sim" · `False` → "Não" · `None` → "—" |

**Contrato V2 · Aba 2 · Matriz de Confronto** (consome P-V2 §3.5 · vocabulário técnico):

| Campo (técnico · `V2Result.matriz_confronto`) | Unidade | Função de total | Notas técnicas |
|---|---|---|---|
| `chave_agrupadores[i]` (i = 1..N) | `texto` | `none` | Coluna de chave · sem total · cabeçalho user-facing declarado pela Usuária na E4 |
| `valor_origem` | `monetario_br` (default) ou `contagem` (quando `tipo_campo` é Contagem) | `sum` (aditivo) · `average` (relativo · não-aditivo) · `none` (estado) | Função de total decorre de `V2Result.config_usada.metodo_consolidacao_relativo`: `SOMA` → `sum` · `MEDIA_PONDERADA` → `average` · `NAO_CONSOLIDAR` → `none` · `ESTADO_SITUACAO` → `none` |
| `valor_comparado` | idem `valor_origem` | idem `valor_origem` | idem |
| `diferenca` | idem `valor_origem` (sinal preservado) | idem `valor_origem` | Calculada como `valor_comparado - valor_origem` · respeita unidade do campo analisado |
| `variacao_percentual` | `percentual` | `none` (variações % não somam · `average` enganoso) | Capability 5 aplica conversão fração→%. `None` quando `valor_origem == 0` (ver `W-V2-BZ` em §2.7) · exibido como `—` |
| `classificacao_estrutural` | `classificacao` | `none` | 6 categorias do `distribuicao_classificacoes_estruturais` · rótulos amigáveis em P-V2 §2 |

**Contrato V2 · Aba 3 · Base Analítica** = colunas da Matriz de Confronto + 2 colunas auxiliares:

| Campo (técnico · `V2Result.base_analitica`) | Unidade | Função de total | Notas técnicas |
|---|---|---|---|
| `classificacao_semantica` | `classificacao` | `none` | Aparece **apenas** quando `tipo_campo ∈ {Soma, Média, Contagem}` · ausente para `ESTADO_SITUACAO` · 4 categorias: Positivo · Negativo · Neutro · Não aplicável |
| `flags` | `texto` | `none` | Lista de warnings traduzidos para microcopy user-facing (P-V2 §2.8) · separador `; ` |

**Aplicação à `exportacao.py`:** o módulo já implementado consome este contrato via parâmetro `contrato_unidade: Dict[str, ContratoUnidade]` que F-APRESENT capability 4/5 montam a partir da declaração desta §2.4-bis + `V2Result.config_usada` (para resolver função de total dinâmica e unidade do `valor_origem`/`valor_comparado` conforme `tipo_campo`). Esta Spec não declara o formato exato do Pydantic `ContratoUnidade` — fica para F-APRESENT P1 capability 4 refinar (decisão técnica pura · resolvida pelo Arquiteto sem novo D-XXX).

**Colunas adaptativas** (D-166 · capability 6) declaradas em P-V2 §3.6 · não duplicadas aqui · S-V2 reconhece como invariante: estrutura monta dinamicamente (POR_LINHAS inclui `estado_origem`/`estado_comparado` · POR_COLUNAS omite · `ESTADO_SITUACAO` omite `variacao_percentual` · coluna constante nula omitida).

**Verificação cruzada com §2.5 (MBO):** nenhum bloqueio B-V2-* novo decorre desta seção. Contrato de unidade é convenção de exportação · não regra de cálculo · não bloqueia análise.

**Verificação cruzada com §2.6 (TED):** nenhum threshold editável novo. Function de total `average` em `valor_origem`/`valor_comparado` é decorrência determinística de `metodo_consolidacao_relativo=MEDIA_PONDERADA` · não threshold.

### 2.5 · Bloqueios operacionais MBO (C.D4) · catálogo B-V2-*

8 bloqueios do DCV §10 instanciados como `BloqueioOperacional` (D-134). Nenhum é escapável (proteção de sistema · não analítico):

| Código | Condição (`condicao_disparo`) | Escapável | Warning pós-escape | Contexto típico |
|---|---|---|---|---|
| `B-V2-ARQUIVO-ILEGIVEL` | Arquivo corrompido ou formato não suportado · motor_upload falha | `False` | — | `{formato_detectado, erro_leitura}` |
| `B-V2-ESTRUTURA-INVALIDA` | Aba sem dado · sem coluna numérica quando campo numérico esperado | `False` | — | `{total_linhas_detectadas, colunas_numericas}` |
| `B-V2-DISCRIMINADOR-0` | POR_LINHAS · coluna discriminadora vazia (`W-V2-N0` associado) | `False` | — | `{coluna_discriminadora}` |
| `B-V2-DISCRIMINADOR-1` | POR_LINHAS · coluna discriminadora com 1 valor único (`W-V2-N1` associado) | `False` | — | `{coluna_discriminadora, valor_unico}` |
| `B-V2-CAMPO-100-NULO` | Campo analisado com 100% de nulos em Origem OU Comparado | `False` | — | `{lado_vazio, total_nulos}` |
| `B-V2-AGRUP-EXCESSO` | ≥ 10 agrupadores declarados (D-027 · zona 9+) | `False` | — | `{n_agrupadores, sugestao_v6: true}` |
| `B-V2-PESO-INVALIDO` | Média ponderada · todos os pesos zerados ou negativos (D-024) | `False` | — | `{campo_peso, nulos, negativos}` |
| `B-V2-CONSOL-IMPOSSIVEL` | `metodo_consolidacao_relativo=NAO_CONSOLIDAR` + `agrupadores>0` (D-024) | `False` | — | `{campo, agrupadores_declarados}` |
| `B-V2-RESULTADO-EXCEDE` | Análise gera mais de 500.000 linhas no resultado (limite operacional) | `False` | — | `{linhas_estimadas, limite: 500000}` |
| `B-V2-CASO-ESTRUTURAL-CANCELADO` | Usuário escolheu "cancelar" em caso estrutural (D-021) | `False` | — | `{tipo_caso, contexto_caso}` |

Formato na implementação:

```python
BloqueioOperacional(
    codigo="B-V2-CAMPO-100-NULO",
    condicao_disparo="Campo analisado tem 100% de valores nulos em Origem — impossível calcular.",
    escapavel=False,
    escape_acionado=None,
    warning_pos_escape=None,
    contexto_disparo={"lado_vazio": "origem", "total_nulos": 212},
)
```

**Nota:** o DCV §10 lista 8 bloqueios · aqui aparecem 10 porque `B-V2-CASO-ESTRUTURAL-CANCELADO` e `B-V2-CONSOL-IMPOSSIVEL` ficaram implícitos no DCV (item 6 · item 7). A Spec formaliza como entradas MBO explícitas · alinhado com C.D4 ("não há terceira opção"). Extensão é execução do princípio · não nova decisão.

**Nota técnica (D-151) · comportamento de `B-V2-ESTRUTURA-INVALIDA` e `B-V2-CAMPO-100-NULO` por estrutura de entrada:**

Decorrência da semântica dupla de `campo_analisado` declarada em §1.2:

| Bloqueio | Em POR_LINHAS | Em POR_COLUNAS |
|---|---|---|
| `B-V2-ESTRUTURA-INVALIDA` | Verifica `campo_analisado not in df.columns` (campo é coluna real) | Verifica `origem_rotulo_tecnico not in df.columns` ou `comparado_rotulo_tecnico not in df.columns` (campo conceitual não corresponde a coluna real · validação se aplica aos dois rótulos técnicos) |
| `B-V2-CAMPO-100-NULO` | Verifica % nulos sobre coluna `campo_analisado` filtrada por cada lado da coluna discriminadora | Verifica % nulos sobre as duas colunas técnicas (origem e comparado) · não sobre o campo conceitual |

Razão: tratar uniformemente as duas estruturas levaria a falsos positivos em POR_COLUNAS legítimos, pois o campo conceitual nunca está como coluna do df. Princípio C.3 reforçado · ambiguidade estrutural latente promovida em vez de absorvida silenciosamente.

### 2.6 · Thresholds editáveis declarados (TED · C.D2)

4 thresholds editáveis em "Configurações avançadas" · persistidos em T-MODELO · default declarado antes da execução:

| Threshold | Default | Unidade | Camada | Editável por etapa |
|---|---|---|---|---|
| `limiar_estabilidade_pct` | `0.01` (1%) | proporção | Camada semântica (Etapa E) | Após E3 (tipo numérico confirmado) |
| `limiar_nulo_massivo_pct` | `0.20` (20%) | proporção | Qualidade de dado (Etapa F · Bloco 6) | Após E3 |
| `limite_valores_discriminador_alerta` | `50` | contagem | Estrutura de entrada (Etapa 2) | Após E2 (estrutura confirmada) |
| `limite_variacao_extrema_pct` | `10.0` (1000%) | proporção | Top variações (Bloco 4 RE) · destaca com cor atenção | Após E3 |

Regra TED canônica: default visível na configuração · editável por camada · valor efetivo persistido em `config_usada` e registrado em `bloco_5_leitura_qualitativa.thresholds_usados` · flag `alguma_leitura_alterada_por_edicao` se qualquer edição muda classificação qualitativa.

### 2.7 · Warnings W-V2-* · catálogo

12 warnings do DCV §9 + 1 da Spec (`W-V2-PAGREG-DUP` · modo Pré-agregado com duplicata de chave):

| Código | Quando dispara | Severidade | Contexto |
|---|---|---|---|
| `W-V2-AUSENTE-EM-UM-LADO` | ≥1 linha classificada como `AUSENTE_ORIGEM` ou `AUSENTE_COMPARADO` | Estrutural | Substitui W-V2-EST do DCV · código canônico vindo do YAML · **referenciado por `V2-A01`** |
| `W-NULO-MEDIDA` | ≥1 linha com `NULO_ORIGEM` · `NULO_COMPARADO` ou `NULO_AMBOS` no campo analisado | Estrutural | Warning transversal da Fundação · consumido por V2 · **referenciado por `V2-A02`** |
| `W-V2-BZ` | ≥1 linha `PRESENTE_AMBOS` com Origem=0 e Comparado≠0 | Cálculo | `variacao_percentual` fica `None` |
| `W-V2-NULL-MASS` | `% nulos no campo analisado` > `limiar_nulo_massivo_pct` (TED) | Qualidade | Sinaliza dado deteriorado |
| `W-V2-AGG` | Tipo relativo ou não-aditivo + agrupadores > 0 | Informativa | Registra método consolidação aplicado (D-024) |
| `W-V2-MIX` | Coluna discriminadora POR_LINHAS com tipos mistos | Estrutural | Motor caiu em ordenação alfabética |
| `W-V2-NMANY` | Coluna discriminadora com valores únicos > `limite_valores_discriminador_alerta` (TED) | Estrutural | Sugere filtragem prévia |
| `W-V2-AGRUP-MUITOS` | ≥ 6 agrupadores efetivamente usados (D-027) | Informativa | Confirma granularidade fina |
| `W-V2-MOD-PARCIAL` | T-MODELO aplicado com ≥1 campo não-casado | Modelo | `tipo_aplicacao=PARCIAL` |
| `W-V2-MOD-INCOMP` | T-MODELO aplicado mas estrutura incompatível | Modelo | `tipo_aplicacao=INCOMPATIVEL` · etapas zeradas |
| `W-V2-AJUSTE-LEVE` | Motor aplicou uma das 4 inconsistências leves (D-021) | Informativa | Registra tipo de ajuste · contagem |
| `W-V2-DECISAO-USUARIO` | Usuário resolveu caso estrutural via painel (D-021) | Informativa | Registra tipo de caso · escolha |
| `W-V2-PAGREG-DUP` | Modo Pré-agregado declarado + duplicata de chave detectada | Estrutural | Motor recai em SOMA |

Nota de nomenclatura canônica · o YAML `casos_esperados.yaml` usa `W-V2-AUSENTE-EM-UM-LADO` e `W-NULO-MEDIDA`. A Spec adota essa nomenclatura como canônica · o DCV §9 tinha `W-V2-EST` e `W-V2-NULL` como legado pré-Fundação. **Qualquer divergência · gabarito YAML prevalece** (D-141 · fonte única de verdade para Validação Visual).

### 2.8 · Resumo Executivo · 6 blocos preenchidos (§13.5 · D-125)

| Bloco | Preenchimento V2 |
|---|---|
| 1 · Cabeçalho | `visao="V2"` · `modo_upload="SIMPLES"` · `agrupadores=[...]` · `medida_principal=campo_analisado` |
| 2 · Números-âncora | `NumerosAncoraV2` · variante numérica ou estado conforme `tipo_campo` |
| 3 · Distribuição | `distribuicao_classificacoes_estruturais` · 6 categorias (0 omitidos na exibição · preservados no contrato) |
| 4 · Elementos destacados | `top_variacoes` · top 10 por `|diferenca|` (numérico) ou por mudança (estado) |
| 5 · Leitura qualitativa | `LeituraQualitativa` · classificação Positivo/Negativo/Neutro/Não aplicável · thresholds usados explícitos · TED |
| 6 · Qualidade estrutural | `QualidadeEstrutural` · total_warnings · warnings por categoria · ajustes (AJUSTE_LEVE + DECISAO_USUARIO) · tem_bloqueios_escapados=`False` (nenhum bloqueio V2 é escapável) |

**Nota D-166 · rendering user-facing dos 6 blocos (adendo retroativo · 23/04/2026 noite):** os 6 blocos do Resumo Executivo são renderizados em **prosa narrativa executiva** pela F-APRESENT capability 7 (D-159) · tom narrativo descritivo (decisão da Usuária em P-V2 §4) · não JSON dump · não lista de bullets. Todos os valores numéricos da prosa consomem o contrato de unidade da §2.4-bis: monetários em `R$ #.##0,00` · variações em `0,00%` (com conversão fração→%) · contagens com separador BR. Microcopy executivo declarada em P-V2 §4.1. `None` exibido como `—` (Bloco 8 do `vocabulario_bilingue.md` v2). Vocabulário técnico canônico (`AUSENTE_ORIGEM`, `POR_COLUNAS`, `B-V2-*`, etc.) **proibido** em superfície cliente · substituição obrigatória por rótulos amigáveis declarados em P-V2 §2 (D-160 · Bloco 7).

### 2.9 · Estrutura da exportação Excel · 4 abas em ordem fixa (D-165 · pós-fusão Parâmetros+Diagnóstico)

**Nota D-165 (adendo retroativo · 23/04/2026 noite):** versão original desta seção declarava **5 abas** com Parâmetros (aba 4) e Diagnóstico (aba 5) separadas. Decisão D-165 (ALINHA-Descoberta-Camada-Produto) **fundiu Parâmetros + Diagnóstico em 1 aba única "Diagnóstico" com 6 seções fixas user-facing** · aplicação canônica para todas as 11 visões · vive como capability 10 de F-APRESENT (P1). Esta §2.9 reescreve a estrutura para 4 abas. Diagnóstico **continua sendo última aba** (D-017 preservado).

| # | Aba | Conteúdo | Observação |
|---|---|---|---|
| 1 | `Resumo Executivo` | 6 blocos preenchidos acima · prosa narrativa executiva (F-APRESENT capability 7) · ver nota D-166 em §2.8 | Primeira aba · §13.5 · D-125 |
| 2 | `Matriz de Confronto` | **Coração Visual · MATRIZ_COLORIDA** · matriz agrupadores × (Origem · Comparado · Δ · Δ%) · formatação condicional por semântica T-SEMA · classificação estrutural explícita por linha · contrato de unidade da §2.4-bis aplicado · colunas adaptativas (P-V2 §3.6) | §13.6 · nome canônico ratificado por `V2-A03` do YAML |
| 3 | `Base Analítica` | 1 linha por combinação de agrupadores · BAD (C.D3) · colunas: agrupadores + valor_origem + valor_comparado + diferenca + variacao_percentual + classificacao_estrutural + classificacao_semantica + flags · contrato de unidade da §2.4-bis aplicado · tabela Excel nativa com `totalsRowShown=True` (D-166 · capability 3 P0) · função de total por coluna conforme §2.4-bis | Consome `base_analitica` herdada de VNResultBase |
| 4 | `Diagnóstico` | **Última aba obrigatória** (D-017) · **6 seções fixas user-facing** (D-165) fundindo o que antes ficava espalhado em Parâmetros + Diagnóstico antigo: (1) Como foi analisado · (2) Ajustes do motor · (3) Pontos de atenção · (4) Decisões do usuário · (5) Configurações avançadas aplicadas · (6) Qualidade estrutural · renderização por F-APRESENT capability 10 (P1) · consome `config_usada` + `comparacao_realizada` + `resolucao_estrutural` + `modelo_aplicado` + T-DIAG + warnings + BAD + paleta selecionada (P-V2 §1.2) | C.D3 · D-017 · D-165 |

**Aba "Parâmetros" (versão pré-D-165) descontinuada.** Conteúdo migrado integralmente para seções 1, 4 e 5 da nova aba "Diagnóstico" sob vocabulário user-facing (sem Python dict serializado · OBS-10c de VV-V2 fechada).

`CoracaoVisualRef` instanciado: `nome_aba="Matriz de Confronto"` · `tipo="MATRIZ_COLORIDA"` · `capabilities_requeridas=["formatacao_condicional", "congelar_paineis", "tabela_nativa_totais", "formatacao_monetaria_br", "formatacao_percentual"]` (capabilities adicionais decorrem de D-166 · F-APRESENT capabilities 3/4/5).

### 2.10 · Padrões §13 aplicados

| Padrão | Aplicação em V2 |
|---|---|
| 13.1 · Objetivo da Visão | Bloco de ajuda contextual acessível desde E1 · 4 seções: o que faz · quando usar · o que obtém · como funciona (conteúdo do DCV §1-§2 resumido) · botão no header |
| 13.2 · Fluxo progressivo | **4 etapas + Revisão** (alinha com motor real · D-167 · estrutura user-facing canônica do stepper Família A · `vocabulario_bilingue.md` v2 Bloco 1) · bloco intermediário RESOL_CASO parqueado como `P-V2-Evo-01` (D-154 · motor V2 atual não pré-detecta casos estruturais) · Seção 3 · mecânica de invalidação declarada por etapa
| 13.3 · T-MODELO | `ModeloAplicadoV2` · persiste E2-E4 + resolução estrutural · NÃO persiste arquivo · aba · resultado · TED editados persistem |
| 13.4 · View especializada | **N/A** · V2 é caso base da Família A · V1 é extensão via T-DUAL · V11 não deriva de V2 · CONTEXT §4 |
| 13.5 · Resumo Executivo 6 Blocos | Seção 2.8 · 6 blocos preenchidos com conteúdo V2-específico |
| 13.6 · Coração Visual | "Matriz de Confronto" · tipo MATRIZ_COLORIDA · Seção 2.9 |

### 2.11 · Checklist §9 Camada C · 5 derivados verificados

| Derivado | Atendimento V2 |
|---|---|
| CPCO · C.D1 | Modo da base declarado (Transacional default · Pré-agregado opcional) · T-AGRUPA invocada obrigatoriamente · no-op validada em Pré-agregado · Seção 2.3 |
| TED · C.D2 | 4 thresholds editáveis declarados (Seção 2.6) · defaults visíveis · persistidos em T-MODELO · sem defaults silenciosos no motor |
| BAD · C.D3 | Aba "Base Analítica" e aba "Diagnóstico" estruturalmente separadas (4 abas pós-D-165 · Seção 2.9 reescrita) · sem aba "Dados Brutos" · rastreabilidade via T-DIAG como contagens · Diagnóstico em 6 seções fixas user-facing (D-165) · MBO sem aba dedicada (`bloqueios` registrados em Diagnóstico seção 3) |
| MBO · C.D4 | 10 bloqueios B-V2-* catalogados com 5 campos cada (Seção 2.5) · nenhum comportamento de caso-limite inventado |
| ECP · C.D5 | Escala de cardinalidade em 3 eixos · Seção 2.12 |

### 2.12 · Escala de cardinalidade V2 (ECP · C.D5)

Adaptação D-073 · V2 tem 3 eixos relevantes dada a natureza comparativa:

**Eixo 1 · Agrupadores simultâneos** (herda D-027 do DCV · já em patamares):

| Patamar | Faixa | Comportamento |
|---|---|---|
| `P1-AGRUP-NORMAL` | 1-3 agrupadores | Normal · sem aviso |
| `P2-AGRUP-ALERTA-LEVE` | 4-5 agrupadores | Aviso visível + estimativa de linhas |
| `P3-AGRUP-ALERTA-FORTE` | 6-8 agrupadores | Confirmação obrigatória + `W-V2-AGRUP-MUITOS` |
| `P4-AGRUP-BLOQUEIO` | ≥ 9 agrupadores | `B-V2-AGRUP-EXCESSO` (não-escapável · bloqueio na zona 10+ conforme DCV §10 item 5) |

**Eixo 2 · Valores únicos da coluna discriminadora (POR_LINHAS):**

| Patamar | Faixa | Comportamento |
|---|---|---|
| `P1-DISCR-NORMAL` | 2 valores | Normal · comparação direta |
| `P2-DISCR-ALERTA-LEVE` | 3-10 valores | Modo 4 normal · usuário escolhe 2 |
| `P3-DISCR-ALERTA-FORTE` | 11-50 valores | Modo 4 + ordenação inteligente obrigatória · W-V2-NMANY NÃO dispara ainda |
| `P4-DISCR-BLOQUEIO-LEVE` | > `limite_valores_discriminador_alerta` (TED=50) | Modo 4 + `W-V2-NMANY` + sugestão de filtro prévio |

**Eixo 3 · Linhas estimadas no resultado (produto de cardinalidades):**

| Patamar | Faixa | Comportamento |
|---|---|---|
| `P1-RES-NORMAL` | ≤ 10.000 | Normal · sem aviso |
| `P2-RES-ALERTA-LEVE` | 10.001 - 100.000 | Aviso: "análise grande" |
| `P3-RES-ALERTA-FORTE` | 100.001 - 500.000 | Aviso forte + confirmação |
| `P4-RES-BLOQUEIO` | > 500.000 | `B-V2-RESULTADO-EXCEDE` · bloqueio não-escapável (DCV §10 item 8) |

Estimativa calculada por multiplicação de cardinalidades (sem materialização · performance item 3 do DCV §11).

---

## Seção 3 · Wireframe funcional

Esqueleto de tela em prosa · descreve fluxo · estados · microcopy · exportação. **Dupla aprovação B.2** (contrato + wireframe funcional) reforçada por `/specs/wireframe_v2.html` (D-149 · Família A obrigatório).

### 3.1 · Estados globais da tela

5 estados + 1 intermediário condicional · mecânica §13.2 · cada etapa concluída mostra resumo compacto · usuário navega via stepper superior.

```
[Vazio]  →  [Configuração E1]  →  [E2]  →  [E3]  →  [E4]
                                                    ↓
                            [Bloco intermediário · condicional · D-021]
                                                    ↓
                                               [E5 · Revisão]
                                                    ↓
                                             [Processando]
                                                    ↓
                                               [Resultado]
```

**Estado Erro** ortogonal: pode aparecer em qualquer etapa quando um `BloqueioOperacional` dispara · mostra `condicao_disparo` + `contexto_disparo` + botão "Voltar à etapa anterior" ou "Nova análise" conforme tipo do bloqueio.

### 3.2 · Header persistente

Presente em todos os estados:

- **Título:** "V2 · Análise Comparativa entre Referências"
- **Botão "Objetivo da Visão"** (§13.1) · abre painel lateral com 4 seções (o que faz · quando usar · o que obtém · como funciona · conteúdo do DCV §1-§2 em linguagem de negócio)
- **Botão "Aplicar modelo"** (T-MODELO) · abre seleção de modelos salvos desta visão
- **Botão "Salvar como modelo"** (T-MODELO) · aparece a partir de E4 concluída
- **Stepper de 5 etapas** visível · etapas concluídas em verde · etapa ativa em destaque · etapas futuras travadas

### 3.3 · Etapa 1 · Origem dos dados

**Ações do usuário:** subir arquivo (Excel ou CSV) · se Excel multi-aba, escolher aba.

**Validações automáticas:**
- Arquivo legível · formato suportado · dado mínimo. Falha → `B-V2-ARQUIVO-ILEGIVEL` ou `B-V2-ESTRUTURA-INVALIDA`.

**Microcopy:**
- Label: "Suba o arquivo que contém os dados a comparar"
- Help text: "Aceita Excel (.xlsx, .xls) e CSV. O arquivo pode ter múltiplas abas — você escolherá qual analisar no próximo passo."

**Resumo ao concluir:** "Arquivo: `{nome}` · Aba: `{aba}` · `{N}` linhas detectadas"

**Invalidação:** mudar arquivo ou aba → E2-E5 zeradas + aviso "Isso vai invalidar as próximas etapas".

### 3.4 · Etapa 2 · Estrutura da comparação

**Ações do usuário:**
1. Escolher POR_COLUNAS ou POR_LINHAS (default: sugestão do motor baseada em detecção de padrão)
2. POR_LINHAS · escolher coluna discriminadora
3. Modo 4 (se >2 valores únicos) · escolher 2 valores · default declarado: extremos por ordenação inteligente (numérico crescente · cronológica · alfabética fallback) · W-V2-NMANY se ultrapassa TED
4. POR_COLUNAS · escolher 2 colunas Origem e Comparado
5. Definir rótulos amigáveis para Origem e Comparado

**Validações automáticas:**
- POR_LINHAS com coluna discriminadora vazia → `B-V2-DISCRIMINADOR-0` (`W-V2-N0`)
- POR_LINHAS com coluna discriminadora · 1 valor único → `B-V2-DISCRIMINADOR-1` (`W-V2-N1`)
- Tipos mistos na coluna discriminadora → `W-V2-MIX`

**Microcopy:**
- POR_COLUNAS radio: "Os dois estados estão em colunas diferentes da mesma base" (ex: `Receita_Orcado` e `Receita_Realizado`)
- POR_LINHAS radio: "Os estados aparecem como valores de uma coluna" (ex: coluna `Cenario` com `Orcado` e `Realizado`)
- Rótulos amigáveis helper: "Como você quer chamar cada estado na apresentação? (ex: 'Orçado 2025' e 'Realizado 2025')"

**Resumo ao concluir:** "Comparar de: `{origem_ux}` · Comparar com: `{comparado_ux}` · Estrutura: `{POR_COLUNAS|POR_LINHAS}` [+ Modo 4 se aplicável · `{N}` valores disponíveis · `{2}` escolhidos]"

**Invalidação:** mudar estrutura ou Origem/Comparado → E3-E5 zeradas.

### 3.5 · Etapa 3 · O que comparar

**Ações do usuário:**
1. Escolher campo a analisar (dropdown)
2. Escolher tipo (D-025): Numérico aditivo · Numérico relativo · Numérico não-aditivo · Estado/Situação (cada opção com microcopy explicativo e exemplos)
3. Definir semântica (T-SEMA): Maior é melhor · Menor é melhor · Neutro · irrelevante se ESTADO_SITUACAO
4. Se tipo relativo ou não-aditivo: escolher método de consolidação (D-024)
   - Default declarado: `MEDIA_SIMPLES`
   - Opções: `MEDIA_SIMPLES` · `MEDIA_PONDERADA` (exige escolher `campo_peso`) · `NAO_CONSOLIDAR`
5. Se modo Pré-agregado aplicável (tipo não-aditivo ou relativo com unicidade declarada): oferecer toggle "Minha base já está pré-agregada (1 linha por chave)"

**Validações automáticas:**
- Campo analisado com 100% de nulos em um dos lados → `B-V2-CAMPO-100-NULO`
- `MEDIA_PONDERADA` com pesos todos zerados ou negativos → `B-V2-PESO-INVALIDO`
- `NAO_CONSOLIDAR` + agrupadores preparados → `B-V2-CONSOL-IMPOSSIVEL` (tardio, aparece em E4)
- `% nulos no campo` > TED `limiar_nulo_massivo_pct` → `W-V2-NULL-MASS`
- Modo Pré-agregado com duplicata detectada em pré-flight → `W-V2-PAGREG-DUP`

**Abrir "Configurações avançadas"** (collapsible): TED dos 4 thresholds · defaults visíveis · edição persiste em T-MODELO.

**Nota técnica (D-153 · A-V2):** na implementação `app_v2.py`, os 4 thresholds editáveis da TED são renderizados em **sidebar global persistente** (sempre visível desde E1) · não em expander interno a E3. A mudança preserva integralmente os 4 requisitos de C.D2 (defaults declarados · editável por camada · persistido em `config_usada` · sem defaults silenciosos no motor) · evita widget-lifecycle churn do Streamlit em transições entre etapas. Convenção herdada por `app_v1.py` e `app_v11.py` (Família A inteira). Microcopy em E3 aponta explicitamente para a sidebar (princípio C.2 preservado).

**Microcopy:**
- Tipo: "Como esse campo se comporta?" · descrições curtas de cada tipo
- Semântica: "Subir é bom, ruim ou neutro?"
- Consolidação: "Como consolidar esse campo quando você agrupa?" (só aparece para tipos relativo/não-aditivo)

**Resumo ao concluir:** "Campo: `{nome}` · Tipo: `{tipo}` · Semântica: `{direção}` [· Consolidação: `{método}`] [· Modo: Pré-agregado]"

**Invalidação:** mudar campo ou tipo → E4-E5 zeradas.

### 3.6 · Etapa 4 · Como agrupar

**Ações do usuário:**
1. Selecionar agrupadores (multi-select · 1 a 9 · D-027)
2. Escolher regra de agregação (T-AGRUPA): Soma · Média · Máximo · Mínimo · Contagem (default: Soma · desabilitada para ESTADO_SITUACAO que sempre conta)
3. Ver estimativa de linhas em tempo real à medida que adiciona/remove agrupadores

**Validações automáticas / patamares (ECP Seção 2.12 · Eixo 1):**
- `P1-AGRUP-NORMAL` (1-3): sem aviso
- `P2-AGRUP-ALERTA-LEVE` (4-5): banner azul "Granularidade média · estimativa `{N}` linhas"
- `P3-AGRUP-ALERTA-FORTE` (6-8): banner amarelo + checkbox obrigatório "Entendo que a análise terá `{N}` linhas" + `W-V2-AGRUP-MUITOS` disparado
- `P4-AGRUP-BLOQUEIO` (≥9): `B-V2-AGRUP-EXCESSO` · mensagem: "V2 não opera com 9+ agrupadores. Use a V6 para análise de relacionamento entre dimensões, ou remova agrupadores."

**Microcopy:**
- "Agrupador define o nível da análise · uma linha de saída por combinação de agrupadores"
- "Filtro é diferente: apenas recorta a visualização final · no Excel você aplica como quiser"

**Resumo ao concluir:** "Agrupadores: `{lista}` · Agregação: `{método}` · Estimativa: `{N}` linhas"

**Invalidação:** mudar agrupadores ou agregação → E5 zerada.

### 3.7 · Bloco intermediário · Resolução de casos estruturais (D-021)

**Quando aparece:** transição E4 → E5 · motor detecta inconsistência estrutural não-leve (Seção 2.4).

**Comportamento da tela:**
1. Stepper marca E5 como "aguardando"
2. Banner vermelho: "Detectamos uma inconsistência estrutural entre Origem e Comparado · precisa de sua decisão"
3. Card do caso detectado: `tipo_caso` · resumo humano · contexto observado (valores · contagens · exemplos)
4. Radio com opções específicas do tipo (Seção 2.4)
5. Botão "Confirmar e prosseguir" (habilitado após escolha) · botão "Cancelar análise"

**Quando não aparece:** 4 inconsistências leves são ajustadas automaticamente (registra `AJUSTE_LEVE` + dispara `W-V2-AJUSTE-LEVE`) · fluxo segue direto para E5.

**Cancelar análise** · dispara `B-V2-CASO-ESTRUTURAL-CANCELADO` · estado Erro · volta ao início limpando E3-E5.

**Nota técnica (D-154 · A-V2 · pendência P-V2-Evo-01):** a detecção pré-execução de casos estruturais **não está implementada** no `visao_v2.py` atual · o motor trata `ResolucaoEstruturalV2` como entrada opcional em `config["resolucao_estrutural"]`, não como output de detecção. A tela RESOL_CASO existe no dispatcher de `app_v2.py` mas **não é acionada** no fluxo atual · fluxo real: (a) casos leves absorvidos via `AJUSTE_LEVE` + `W-V2-AJUSTE-LEVE` · (b) casos estruturais graves viram bloqueios MBO na Tela 10. Implementação do mecanismo completo "motor pausa → painel → Usuária decide → retoma" exigiria refino de contrato da Fundação (motor com fase de detecção separada · OU exceção tipada · OU campo `caso_pendente` no V2Result) · parqueado como **P-V2-Evo-01** · revisável pós-VV-V2 se a lacuna gerar ❌ no checklist. §3.7 mantém-se válida como roadmap · não como contrato vigente do MVP V2. Princípio C.3 preservado (não inventar comportamento sem contrato).

### 3.8 · Etapa 5 · Revisão e execução

**Visão de tela:**
- Preview compacto das configurações E1-E4 (5 cards horizontais · cada um com botão "Editar" que navega via stepper)
- Bloco de resolução estrutural se houve
- TED efetivos resumidos · botão "Configurações avançadas" reexpansível
- Botão principal: "Processar análise"
- Estado preservado ao editar etapa anterior (não obriga redigitar campos não-afetados)

**Durante processamento:**
- Loader com barra de progresso
- Mensagens por etapa do pipeline (Preparação · Detecção · Consolidação · Cálculo · Semântica · Exportação)
- Tempo estimado

**Resultado:**
- Card de sucesso com 4 números-âncora em destaque
- Botão "Ver Resumo Executivo" (abre preview das 6 seções)
- Botão "Ver Matriz de Confronto" (abre preview do Coração Visual · §13.6)
- Botão "**Validação Visual**" → abre checkbox list do checklist §3.x (Seção 3.9) · obrigatória antes de exportar
- Botão "Baixar Excel" · habilitado apenas quando todos os itens do checklist estão ✅ · **B.4**
- Botão "Nova análise" · volta a E1 preservando modelo atualizado em T-MODELO

### 3.9 · Checklist de Validação Visual V2

**Derivado mecanicamente** de `casos_esperados.yaml` bloco `visoes.V2` via 5 templates canônicos (D-148). 4 assertions → 4 itens 1:1.

**Protocolo:** Usuária carrega `/bases/base_v2_cliente.xlsx` no `app_v2.py` · configura a análise · processa · marca cada item como ✅ ou ❌. Derivado de `casos_esperados.yaml` bloco `visoes.V2` (4 assertions).

```
[ ] Item 1 (V2-A01 · contagem_categoria) · O resultado mostra entre 2 e 4
    elementos ausentes em um lado em Produto na aba vendas_padrao
    (warning associado: W-V2-AUSENTE-EM-UM-LADO)?

[ ] Item 2 (V2-A02 · warning_presente) · O warning W-NULO-MEDIDA aparece no
    Diagnóstico com 3–4 ocorrência(s)?

[ ] Item 3 (V2-A03 · estrutura_saida) · O Excel tem Resumo Executivo com 6
    blocos e aba Coração Visual nomeada "Matriz de Confronto"?

[ ] Item 4 (V2-A04 · contagem_exata) · O resultado mostra exatamente 2
    estados distintos (2025-01 e 2025-02) em Mes na aba vendas_padrao?
```

**Aprovação final:** todos ✅ → visão aprovada · Validação Visual registrada na aba 2 da planilha (5º quadrado ✅). Qualquer ❌ → Arquiteto investiga em sessão dedicada (M4 de D-131 · bug de código · lacuna de Spec · interpretação divergente).

**Regra C.2 reforçada:** item não-coberto por assertion **não pode ser adicionado ad-hoc** ao checklist. Nova assertion vira entrada em `casos_esperados.yaml` + regeneração do checklist (D-148).

### 3.10 · Detalhes de estado · invalidação cascata

| Editar... | Invalida | Motivo |
|---|---|---|
| E1 (arquivo/aba) | E2-E5 | Estrutura da base muda tudo |
| E2 (estrutura/Origem/Comparado) | E3-E5 | Campos disponíveis dependem da estrutura |
| E3 (campo/tipo/semântica/consolidação) | E4-E5 | Agrupadores compatíveis dependem do tipo |
| E4 (agrupadores/agregação) | E5 | Detecção de caso estrutural depende de agrupadores |
| Bloco intermediário | Nada | Decisão registrada · novo processamento reproduz |

Estado preservado por etapa em memória do app · T-MODELO persiste apenas ao salvar explicitamente (13.3).

---

## Notas operacionais finais

**Sobre nomenclatura:** sempre que o DCV-V2 §9 (warnings) diverge do `casos_esperados.yaml`, o YAML prevalece (D-141 · fonte única). Ajustes nesta Spec seguem o YAML · não introduzem novas nomenclaturas.

**Sobre retroação diferida D-126:** a declaração formal do Coração Visual "Matriz de Confronto" **cumpre a retroação** para a V2. V1 e V11 seguem padrão análogo nas próximas Specs (candidatos: Mapa de Conciliação · Mapa de Aderência).

**Sobre TED:** 4 thresholds apenas · não misturar com parâmetros de configuração de análise (campo, semântica, método consolidação) · esses são configurações obrigatórias · não thresholds editáveis. TED é para parâmetros numéricos cuja mudança afeta leitura qualitativa.

**Sobre Modo 4:** `estados_nao_escolhidos` vai para o Diagnóstico mas **não contamina** `base_analitica` — apenas os 2 estados escolhidos entram no cálculo. Isso preserva determinismo (C.1) e rastreabilidade (C.2).

**Sobre performance (DCV §11):** requisitos já estão absorvidos na Fundação (`exportacao.py` · `motor_base.py`) · esta Spec apenas consome. Item 8 (limite 500K) materializado como `B-V2-RESULTADO-EXCEDE`.

**Sobre P-V2-old-03 (limite de 10 campos comparados):** pendência aberta no DCV §15 · **não entra nesta Spec** · V2 atual analisa 1 campo por execução · multi-campo fica para futura evolução com DCV-V2.1 próprio.

---

