"""
visao_v1.py — V1 · Conciliação de Bases · Família A
Pipeline canônico V1 · 8 etapas · 2 ramos por caso lógico (D-213) · S-V1 v2 §2.1
Determinístico C.1 · zero invenção C.3 · nada silencioso C.2 · preserva e classifica C.5

Fonte autoritativa: /specs/spec_v1.md v2.0 (26/04/2026 noite · pacote único · Caminho A).
Construído na sessão V-V1 (3º quadrado dos 6 do ciclo da V1 · D-158).
"""
from __future__ import annotations

import sys
from datetime import datetime
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field, model_validator

sys.path.insert(0, str(Path(__file__).parent.parent))

from contratos import (  # noqa: E402
    AjusteMotor,
    BloqueioOperacional,
    CabecalhoExecucao,
    CategoriaWarning,
    ColumnMeta,
    CoracaoVisualRef,
    DecisaoUsuario,
    DiagnosticoVN,
    LeituraQualitativa,
    MotorResult,
    MotorResultMeta,
    QualidadeEstrutural,
    ResumoExecutivoPadrao,
    VNResultBase,
    WarningEstrutural,
)
from transversais.t_diag import TDIAG  # noqa: E402
from transversais.t_modelo import ModeloConfig, aplicar_modelo, salvar_modelo  # noqa: E402


# ---------------------------------------------------------------------------
# Enums V1-específicas (S-V1 §1.3 · §1.5 · §1.7 · §1.8 · §1.9 · §1.10)
# ---------------------------------------------------------------------------

class UnidadeCanonica(str, Enum):
    """Enum local · 8 valores canônicos (Bloco 10 do vocabulário bilíngue v4).

    Declarada localmente em V-V1 conforme bifurcação BIF-0 da Ancoragem (Fase 0):
    S-V1 §1.22 declara `UnidadeCanonica` como enum da Fundação · em
    `contratos.py` existe apenas como `Literal[...]` em ColumnMeta.unidade
    e ContratoComparativo.unidade. Modificar contratos.py é vetado pelo
    prompt V-V1 (seção 10.3). Promoção da enum para Fundação é sugestão
    para retrospectiva (refactor cosmético).
    """
    MONETARIO_BRL = "MONETARIO_BRL"
    PERCENTUAL = "PERCENTUAL"
    QUANTIDADE = "QUANTIDADE"
    TEMPO_DIAS = "TEMPO_DIAS"
    TEMPO_HORAS = "TEMPO_HORAS"
    MULTIPLICADOR = "MULTIPLICADOR"
    RAZAO = "RAZAO"
    ADIMENSIONAL = "ADIMENSIONAL"


class CasoLogicoV1(str, Enum):
    """S-V1 §1.3 · D-213 · 2 ramos do pipeline · inferido pelo motor (não declarado)."""
    ABAS_DISTINTAS = "ABAS_DISTINTAS"
    MESMA_ABA_EM_COLUNAS = "MESMA_ABA_EM_COLUNAS"


class ModoMatchV1(str, Enum):
    """S-V1 §1.5 · 4 modos · aplicado em ABAS_DISTINTAS · ignorado em MESMA_ABA_EM_COLUNAS."""
    EXATO = "EXATO"
    CONTEM = "CONTEM"
    INICIA_COM = "INICIA_COM"
    TERMINA_COM = "TERMINA_COM"


class TipoCampoV1(str, Enum):
    """S-V1 §1.7 · taxonomia DCV §4.3 · 7 valores."""
    VALOR_MONETARIO = "VALOR_MONETARIO"
    QUANTIDADE = "QUANTIDADE"
    VOLUME = "VOLUME"
    PERCENTUAL = "PERCENTUAL"
    PRAZO = "PRAZO"
    INDICE = "INDICE"
    ESTADO_SITUACAO = "ESTADO_SITUACAO"


class ClassificacaoRegistroV1(str, Enum):
    """S-V1 §1.8 · 6 valores · em MESMA_ABA_EM_COLUNAS apenas CONCILIADO/DIVERGENTE_VALOR ativos."""
    CONCILIADO = "CONCILIADO"
    DIVERGENTE_VALOR = "DIVERGENTE_VALOR"
    SO_ORIGEM = "SO_ORIGEM"
    SO_COMPARADO = "SO_COMPARADO"
    DIVERGENCIA_DUPLICIDADE = "DIVERGENCIA_DUPLICIDADE"
    DIVERGENCIA_AMBIGUIDADE = "DIVERGENCIA_AMBIGUIDADE"


class StatusCampoV1(str, Enum):
    """S-V1 §1.9 · 6 valores · derivado da tabela §2.4 (independente do caso lógico)."""
    IGUAL = "IGUAL"
    DENTRO_TOLERANCIA = "DENTRO_TOLERANCIA"
    DIVERGENTE = "DIVERGENTE"
    SEM_VALOR_ORIGEM = "SEM_VALOR_ORIGEM"
    SEM_VALOR_COMPARADO = "SEM_VALOR_COMPARADO"
    SEM_VALOR_AMBOS = "SEM_VALOR_AMBOS"


class StatusPonteV1(str, Enum):
    """S-V1 §1.10 · 2 valores · cálculo §2.6 · FECHA por convenção quando len(pontes)==0."""
    FECHA = "FECHA"
    COM_RESIDUO = "COM_RESIDUO"


# ---------------------------------------------------------------------------
# Constantes V1 derivadas das enums
# ---------------------------------------------------------------------------

# Mapeamento default tipo_logico → unidade (S-V1 §1.7 · Bloco 10.1)
DEFAULT_UNIDADE_POR_TIPO: Dict[TipoCampoV1, UnidadeCanonica] = {
    TipoCampoV1.VALOR_MONETARIO: UnidadeCanonica.MONETARIO_BRL,
    TipoCampoV1.QUANTIDADE: UnidadeCanonica.QUANTIDADE,
    TipoCampoV1.VOLUME: UnidadeCanonica.QUANTIDADE,
    TipoCampoV1.PERCENTUAL: UnidadeCanonica.PERCENTUAL,
    TipoCampoV1.PRAZO: UnidadeCanonica.TEMPO_DIAS,
    TipoCampoV1.INDICE: UnidadeCanonica.MULTIPLICADOR,
    TipoCampoV1.ESTADO_SITUACAO: UnidadeCanonica.ADIMENSIONAL,
}

# TED epsilon_por_unidade default (S-V1 §2.8 · Q2.C · D-211)
# 5 entradas explícitas em S-V1 §2.8; 3 omitidas (PERCENTUAL/ADIMENSIONAL/RAZAO)
# defaultam Decimal("0") porque campos com essas unidades são omitidos de pontes (Q1.B · D-210).
DEFAULT_EPSILON_POR_UNIDADE: Dict[UnidadeCanonica, Decimal] = {
    UnidadeCanonica.MONETARIO_BRL: Decimal("0.01"),
    UnidadeCanonica.QUANTIDADE: Decimal("0"),
    UnidadeCanonica.TEMPO_DIAS: Decimal("0"),
    UnidadeCanonica.TEMPO_HORAS: Decimal("0.01"),
    UnidadeCanonica.MULTIPLICADOR: Decimal("0.0001"),
    UnidadeCanonica.PERCENTUAL: Decimal("0"),
    UnidadeCanonica.ADIMENSIONAL: Decimal("0"),
    UnidadeCanonica.RAZAO: Decimal("0"),
}

# Outros TEDs default (S-V1 §2.8)
DEFAULT_CHAVE_NULOS_MAX: Decimal = Decimal("0.50")
DEFAULT_VOLUME_MAX: int = 500_000
DEFAULT_CONCENTRACAO_AGRUPADOR_PRINCIPAL_MIN: Decimal = Decimal("0.70")

# Unidades inelegíveis para Ponte (Q1.B · D-210)
UNIDADES_INELEGIVEIS_PONTE: set = {
    UnidadeCanonica.PERCENTUAL,
    UnidadeCanonica.ADIMENSIONAL,
    UnidadeCanonica.RAZAO,
}

# Ordem canônica para sort determinístico (Q3 · ASCII-strict por nome do enum)
ORDEM_CLASSIFICACAO: Dict[ClassificacaoRegistroV1, int] = {
    ClassificacaoRegistroV1.CONCILIADO: 0,
    ClassificacaoRegistroV1.DIVERGENTE_VALOR: 1,
    ClassificacaoRegistroV1.SO_ORIGEM: 2,
    ClassificacaoRegistroV1.SO_COMPARADO: 3,
    ClassificacaoRegistroV1.DIVERGENCIA_DUPLICIDADE: 4,
    ClassificacaoRegistroV1.DIVERGENCIA_AMBIGUIDADE: 5,
}


# ---------------------------------------------------------------------------
# Contratos V1-específicos (S-V1 §1.1-1.21)
# ---------------------------------------------------------------------------


class AgrupadorMatchV1(BaseModel):
    """S-V1 §1.4 · 1 elemento da chave lógica do match (D-213 ajustado)."""
    model_config = ConfigDict(use_enum_values=False)

    nome_origem: str = Field(..., description="Coluna na aba da Origem")
    nome_comparado: str = Field(
        ...,
        description="Coluna na aba do Comparado · != nome_origem quando MESMA_ABA_EM_COLUNAS",
    )
    rotulo_analitico: str = Field(
        ...,
        description="Nome amigável dado pela Usuária · default = nome_origem · vira título nas Abas 2/3/4",
    )
    modo_match: ModoMatchV1 = Field(
        ...,
        description="Regra declarada de busca · ignorada em MESMA_ABA_EM_COLUNAS · obrigatória em ABAS_DISTINTAS",
    )


class CampoComparadoV1(BaseModel):
    """S-V1 §1.6 · 1 campo a confrontar."""
    model_config = ConfigDict(use_enum_values=False)

    nome_origem: str = Field(..., description="Coluna na aba da Origem")
    nome_comparado: str = Field(..., description="Coluna na aba do Comparado")
    nome_analitico: str = Field(..., description="Nome amigável · vira título nas Abas 2/4/5")
    tipo_logico: TipoCampoV1 = Field(
        ...,
        description="Tipo lógico declarado · 7 valores · taxonomia DCV §4.3",
    )
    unidade: UnidadeCanonica = Field(
        ...,
        description="Default inferido de tipo_logico (Bloco 10.1) · Usuária pode trocar · C.D6",
    )
    tolerancia: Decimal = Field(
        default=Decimal("0"),
        description="Tolerância absoluta no nível da célula (DENTRO_TOLERANCIA) · S-V1 §2.4",
    )

    @model_validator(mode="after")
    def _validar_tolerancia_nao_negativa(self) -> "CampoComparadoV1":
        if self.tolerancia < Decimal("0"):
            raise ValueError(
                f"tolerancia deve ser >= 0 · recebido {self.tolerancia} para campo {self.nome_analitico}"
            )
        return self


class CelulaCampoV1(BaseModel):
    """S-V1 §1.12 · 1 par (Origem, Comparado) de valores para 1 campo em 1 registro."""
    model_config = ConfigDict(use_enum_values=False)

    campo_indice: int = Field(
        ...,
        description="Índice posicional na lista de campos do contrato (0-based)",
    )
    valor_origem: Optional[Decimal] = Field(
        ...,
        description="Valor do lado Origem · None quando ausente · zeros à esquerda preservados em string ao montar chave",
    )
    valor_comparado: Optional[Decimal] = Field(
        ...,
        description="Valor do lado Comparado · None quando ausente",
    )
    diferenca: Optional[Decimal] = Field(
        ...,
        description="valor_origem - valor_comparado · None quando algum lado é None",
    )
    status_campo: StatusCampoV1 = Field(
        ...,
        description="Status da célula · 1 dos 6 valores · derivado da tabela §2.4",
    )


class RegistroConciliadoV1(BaseModel):
    """S-V1 §1.11 · 1 linha do Mapa de Conciliação (Aba 3) · raiz da Aba 4."""
    model_config = ConfigDict(use_enum_values=False)

    chave_consolidada: str = Field(
        ...,
        description=(
            "ABAS_DISTINTAS: concatenação dos valores dos agrupadores de match com '|'. "
            "MESMA_ABA_EM_COLUNAS: concatenação dos valores das colunas de Origem dos agrupadores."
        ),
    )
    valores_agrupadores: Dict[str, str] = Field(
        ...,
        description="rotulo_analitico → valor (sempre str · zeros à esquerda preservados)",
    )
    classificacao_estrutural: ClassificacaoRegistroV1 = Field(
        ...,
        description="1 das 6 classes em ABAS_DISTINTAS · 1 das 2 (CONCILIADO/DIVERGENTE_VALOR) em MESMA_ABA_EM_COLUNAS",
    )
    valores_por_campo: List[CelulaCampoV1] = Field(
        ...,
        description="1 célula por CampoComparadoV1 · ordem espelha config.campos_comparados",
    )
    diferenca_total_registro: Optional[Decimal] = Field(
        ...,
        description=(
            "Soma das diferenças (preservando sinal) multi-campo · None quando classificação ∈ "
            "{SO_ORIGEM, SO_COMPARADO, DIVERGENCIA_DUPLICIDADE, DIVERGENCIA_AMBIGUIDADE}"
        ),
    )
    sigma_diferenca_total_registro: Optional[Decimal] = Field(
        ...,
        description="Soma de |diferenca| multi-campo · None nas mesmas condições",
    )
    variacao_total_registro_pct: Optional[Decimal] = Field(
        ...,
        description=(
            "diferenca_total_registro / Σ valor_origem · None nas mesmas condições · "
            "None se Σ valor_origem == 0 (B-V1-DIV-ZERO)"
        ),
    )
    observacoes: Optional[str] = Field(default=None, description="Notas livres opcionais")


class CoberturaV1(BaseModel):
    """S-V1 §1.13 · cobertura simétrica de match · §6 do RE · None em MESMA_ABA_EM_COLUNAS."""
    model_config = ConfigDict(use_enum_values=False)

    n_origem_com_par: int = Field(..., description="N° de registros da Origem que casaram (incluindo dup/amb)")
    n_origem_sem_par: int = Field(..., description="N° de registros SO_ORIGEM")
    cobertura_origem_pct: Decimal = Field(
        ...,
        description="n_origem_com_par / n_registros_origem · proporção [0, 1]",
    )
    n_comparado_com_par: int = Field(..., description="Simétrico ao Origem")
    n_comparado_sem_par: int = Field(..., description="N° de registros SO_COMPARADO")
    cobertura_comparado_pct: Decimal = Field(
        ...,
        description="n_comparado_com_par / n_registros_comparado · proporção [0, 1]",
    )


class ValorPorCampoV1(BaseModel):
    """S-V1 §1.14 · 1 entrada por campo comparado · §5 do RE · §3.2 Aba 2."""
    model_config = ConfigDict(use_enum_values=False)

    nome_analitico: str = Field(..., description="Espelha CampoComparadoV1.nome_analitico")
    unidade: UnidadeCanonica = Field(..., description="Espelha CampoComparadoV1.unidade")
    soma_origem: Decimal = Field(..., description="Σ valor_origem em todos os registros com valor não-None")
    soma_comparado: Decimal = Field(..., description="Σ valor_comparado · idem")
    diferenca_liquida: Decimal = Field(..., description="soma_origem - soma_comparado (preserva sinal)")
    sigma_diferenca: Decimal = Field(
        ...,
        description="Σ |diferenca| · APENAS em registros CONCILIADO ou DIVERGENTE_VALOR (D-213)",
    )
    n_tolerancia_absorvida: int = Field(
        ...,
        description="N° de células com status_campo == DENTRO_TOLERANCIA",
    )
    valor_tolerancia_absorvida: Decimal = Field(
        ...,
        description="Σ |diferenca| das células DENTRO_TOLERANCIA",
    )


class MetricaCampoAgrupadorV1(BaseModel):
    """S-V1 §1.15 · 1 métrica por campo dentro de uma LinhaResumoAgrupadorV1."""
    model_config = ConfigDict(use_enum_values=False)

    nome_analitico: str
    unidade: UnidadeCanonica
    soma_origem: Decimal
    soma_comparado: Decimal
    diferenca_liquida: Decimal
    sigma_diferenca: Decimal


class LinhaResumoAgrupadorV1(BaseModel):
    """S-V1 §1.15 · 1 linha da Aba 2 · 1 valor único do(s) agrupador(es) executivo(s)."""
    model_config = ConfigDict(use_enum_values=False)

    valores_agrupador: Dict[str, str] = Field(
        ...,
        description="nome_coluna → valor único · agrupa registros desta linha",
    )
    n_conciliados: int = Field(..., description="N° de registros CONCILIADO neste agrupamento")
    n_divergentes_valor: int = Field(..., description="N° de registros DIVERGENTE_VALOR")
    n_so_origem: int = Field(..., description="0 em MESMA_ABA_EM_COLUNAS por construção")
    n_so_comparado: int = Field(..., description="0 em MESMA_ABA_EM_COLUNAS por construção")
    metricas_por_campo: List[MetricaCampoAgrupadorV1] = Field(
        ...,
        description="1 entrada por CampoComparadoV1",
    )
    diferenca_liquida_total: Decimal = Field(
        ...,
        description="Σ diferenca_liquida em todas as métricas · usado para ordenação T-RANK",
    )


class PonteCampoV1(BaseModel):
    """S-V1 §1.16 · 1 sub-Ponte por campo elegível (Q1.B omite PERCENTUAL/ADIMENSIONAL/RAZAO)."""
    model_config = ConfigDict(use_enum_values=False)

    nome_analitico: str
    unidade: UnidadeCanonica
    saldo_origem: Decimal = Field(..., description="Σ valor_origem em todos os registros com valor não-None")
    ajuste_so_origem: Decimal = Field(
        ...,
        description="-Σ valor_origem em SO_ORIGEM · Decimal('0') em MESMA_ABA_EM_COLUNAS",
    )
    ajuste_so_comparado: Decimal = Field(
        ...,
        description="+Σ valor_comparado em SO_COMPARADO · Decimal('0') em MESMA_ABA_EM_COLUNAS",
    )
    ajuste_divergentes_valor: Decimal = Field(
        ...,
        description="-Σ diferenca em DIVERGENTE_VALOR (preserva sinal)",
    )
    ajuste_tolerancia_absorvida: Decimal = Field(
        ...,
        description="-Σ diferenca em células DENTRO_TOLERANCIA com diferenca != 0",
    )
    saldo_comparado_esperado: Decimal = Field(
        ...,
        description="saldo_origem + ajuste_so_origem + ajuste_so_comparado + ajuste_divergentes_valor + ajuste_tolerancia_absorvida",
    )
    saldo_comparado_real: Decimal = Field(
        ...,
        description="Σ valor_comparado em todos os registros com valor não-None",
    )
    residuo: Decimal = Field(
        ...,
        description="saldo_comparado_real - saldo_comparado_esperado · esperado ≈ Decimal('0') quando fecha",
    )
    fecha: bool = Field(
        ...,
        description="True quando |residuo| < epsilon_por_unidade[unidade]",
    )


class SinteseDiagnosticoV1(BaseModel):
    """S-V1 §1.17 · 7 contadores para a §8 do Resumo Executivo."""
    model_config = ConfigDict(use_enum_values=False)

    n_tolerancia_absorvida: int = Field(..., description="Total de células DENTRO_TOLERANCIA")
    valor_tolerancia_absorvida: Decimal = Field(..., description="Σ |diferenca| das células DENTRO_TOLERANCIA")
    n_chaves_duplicadas: int = Field(..., description="0 em MESMA_ABA_EM_COLUNAS por construção")
    n_registros_afetados_duplicidade: int = Field(..., description="Idem")
    n_chaves_ambiguas: int = Field(..., description="Idem")
    n_registros_afetados_ambiguidade: int = Field(..., description="Idem")
    n_warnings_ativos: int = Field(..., description="Total de warnings W-V1-* com n_ocorrencias > 0")


class ConfigAplicadaV1(BaseModel):
    """S-V1 §1.18 · reflexo declarativo da config · 12 campos achatados (CONTEXT §15.12)."""
    model_config = ConfigDict(use_enum_values=False)

    arquivo_origem: str
    aba_origem: str
    arquivo_comparado: str
    aba_comparado: str
    n_arquivos: Literal[1, 2]
    caso_logico_inferido: CasoLogicoV1
    agrupadores_match: List[AgrupadorMatchV1]
    campos_comparados: List[CampoComparadoV1]
    agrupadores_resumo_executivo: List[str] = Field(default_factory=list)
    paleta_aplicada: str = Field(
        ...,
        description="Default 'Azul executivo' (P-V1 §4.6-bis · D-212 corrige P-V1 §4.5)",
    )
    epsilon_por_unidade: Dict[UnidadeCanonica, Decimal] = Field(
        ...,
        description="TED Q2.C · só unidades efetivamente em uso são populadas (D-211)",
    )
    defaults_sobrescritos: Dict[str, str] = Field(
        default_factory=dict,
        description="TEDs editados pela Usuária · auditabilidade C.2 · {chave_técnica: valor_aplicado}",
    )
    nulos_por_classificacao: Dict[ClassificacaoRegistroV1, int] = Field(
        default_factory=dict,
        description="Contagem de células None por classificação estrutural",
    )


class LeituraQualitativaV1(BaseModel):
    """S-V1 §1.19 · texto-livre parametrizado · 3 a 6 frases · zero invenção."""
    model_config = ConfigDict(use_enum_values=False)

    texto: str
    faixa_taxa: Literal["ALTA", "MEDIA", "BAIXA"]
    modificadores_aplicados: List[str] = Field(default_factory=list)
    agrupador_principal_citado: Optional[str] = Field(default=None)


class WarningV1(BaseModel):
    """S-V1 §1.20 · estrutura uniforme dos 4 W-V1-* + warnings herdados do motor."""
    model_config = ConfigDict(use_enum_values=False)

    codigo: str = Field(..., description="W-V1-TOL · W-V1-DUP · W-V1-AMB · W-V1-UNIDADE · ou herdado")
    severidade: Literal[
        "INFORMATIVO",
        "AJUSTE_LEVE",
        "ALERTA_ESTRUTURAL",
        "DECISAO_USUARIO",
        "ESCAPE",
    ]
    n_ocorrencias: int = Field(..., description="0 é informação válida · padrão de exibição §2.7")
    detalhes: List[Dict[str, Any]] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validar_codigo_v1(self) -> "WarningV1":
        if not self.codigo.startswith("W-V1-") and not self.codigo.startswith("W-"):
            raise ValueError(
                f"codigo deve começar com 'W-V1-' (próprio) ou 'W-' (herdado do motor) · recebido: {self.codigo}"
            )
        return self


class ModeloAplicadoV1(BaseModel):
    """S-V1 §1.21 · referência a um modelo T-MODELO previamente salvo."""
    model_config = ConfigDict(use_enum_values=False)

    nome_modelo: str
    data_criacao: datetime
    versao_contrato: str


class ConciliacaoRealizadaV1(BaseModel):
    """S-V1 §1.2 · sub-contrato declarativo do que foi efetivamente executado (D-213)."""
    model_config = ConfigDict(use_enum_values=False)

    n_arquivos: Literal[1, 2] = Field(
        ...,
        description="Físico do upload · 1 (arquivo único · com N abas) ou 2 (dois arquivos)",
    )
    arquivo_origem: str = Field(..., description="Nome do arquivo da Origem · em n_arquivos==1 igual a arquivo_comparado")
    aba_origem: str = Field(..., description="Nome da aba da Origem · sempre populado")
    arquivo_comparado: str = Field(..., description="Nome do arquivo do Comparado")
    aba_comparado: str = Field(
        ...,
        description="Nome da aba do Comparado · igual a aba_origem somente em MESMA_ABA_EM_COLUNAS",
    )
    caso_logico_inferido: CasoLogicoV1 = Field(
        ...,
        description="Inferido pelo motor a partir do apontamento dos campos na E3 · não declarado pela Usuária",
    )
    origem_ux: str = Field(..., description="Rótulo amigável editável da Origem · default 'Origem' quando vazio")
    comparado_ux: str = Field(..., description="Rótulo amigável editável do Comparado · default 'Comparado'")
    rotulo_amigavel_declarado: bool = Field(
        ...,
        description="True quando origem_ux != 'Origem' E comparado_ux != 'Comparado' (P-α.3-03)",
    )
    agrupadores_match: List[AgrupadorMatchV1] = Field(..., description="1 a 5 agrupadores · L-V1-D")
    campos_comparados: List[CampoComparadoV1] = Field(..., description="1 a 10 campos · P-V1-10")
    agrupadores_resumo_executivo: List[str] = Field(
        default_factory=list,
        description="0 a 5 agrupadores · 0 = aba Resumo por Agrupador omitida",
    )
    n_registros_origem: int = Field(..., description="Total de registros do lado Origem")
    n_registros_comparado: int = Field(..., description="Total de registros do lado Comparado")
    n_processados: int = Field(
        ...,
        description=(
            "Total após match · ABAS_DISTINTAS = n_origem + n_comparado − n_pares_casados · "
            "MESMA_ABA_EM_COLUNAS = n° de linhas da aba"
        ),
    )

    @model_validator(mode="after")
    def _validar_invariantes_d213(self) -> "ConciliacaoRealizadaV1":
        # Bounds canônicos
        if not (1 <= len(self.agrupadores_match) <= 5):
            raise ValueError(
                f"len(agrupadores_match) deve estar em [1, 5] · recebido {len(self.agrupadores_match)}"
            )
        if not (1 <= len(self.campos_comparados) <= 10):
            raise ValueError(
                f"len(campos_comparados) deve estar em [1, 10] · recebido {len(self.campos_comparados)}"
            )
        if not (0 <= len(self.agrupadores_resumo_executivo) <= 5):
            raise ValueError(
                f"len(agrupadores_resumo_executivo) deve estar em [0, 5] · recebido {len(self.agrupadores_resumo_executivo)}"
            )
        # Coerência n_arquivos · arquivo_origem · arquivo_comparado
        if self.n_arquivos == 1 and self.arquivo_origem != self.arquivo_comparado:
            raise ValueError(
                f"n_arquivos==1 exige arquivo_origem == arquivo_comparado · "
                f"recebido {self.arquivo_origem!r} != {self.arquivo_comparado!r}"
            )
        # Coerência caso_logico × abas
        if self.caso_logico_inferido == CasoLogicoV1.MESMA_ABA_EM_COLUNAS:
            if self.aba_origem != self.aba_comparado:
                raise ValueError(
                    f"MESMA_ABA_EM_COLUNAS exige aba_origem == aba_comparado · "
                    f"recebido {self.aba_origem!r} != {self.aba_comparado!r}"
                )
        else:  # ABAS_DISTINTAS
            if self.aba_origem == self.aba_comparado and self.arquivo_origem == self.arquivo_comparado:
                raise ValueError(
                    f"ABAS_DISTINTAS exige aba_origem != aba_comparado quando mesmo arquivo · "
                    f"recebido aba {self.aba_origem!r}"
                )
        # Coerência rotulo_amigavel_declarado
        esperado = self.origem_ux != "Origem" and self.comparado_ux != "Comparado"
        if self.rotulo_amigavel_declarado != esperado:
            raise ValueError(
                f"rotulo_amigavel_declarado deve ser {esperado} dado origem_ux={self.origem_ux!r} "
                f"e comparado_ux={self.comparado_ux!r} · recebido {self.rotulo_amigavel_declarado}"
            )
        return self


class ConciliacaoV1Result(VNResultBase):
    """S-V1 §1.1 · contrato principal de saída do motor V1.

    Estende VNResultBase (Fundação · D-130). Carrega 4 dimensões: taxa,
    granularidade registro-a-registro, achatado por campo, Ponte. Aplica
    invariantes pós-construção (model_validator).
    """
    model_config = ConfigDict(arbitrary_types_allowed=True, use_enum_values=False)

    visao_id: Literal["V1"] = Field("V1", description="Override · única V1 produz este contrato")
    visao: Literal["V1"] = Field(
        default="V1",
        description="Identificador fixo · V1 · S-V1 v2 §1.1 (escolha Usuária 26/04 noite · campo redundante mantido)",
    )

    conciliacao_realizada: ConciliacaoRealizadaV1 = Field(
        ...,
        description="Declaração da conciliação executada · D-213",
    )
    classificacao_por_registro: List[RegistroConciliadoV1] = Field(
        ...,
        description="1 entrada por registro · ordem determinística canônica (Q3)",
    )
    contagem_por_classificacao: Dict[ClassificacaoRegistroV1, int] = Field(
        ...,
        description=(
            "6 chaves em ABAS_DISTINTAS · 6 chaves com 4 zerados em MESMA_ABA_EM_COLUNAS (D-213) · "
            "zero preservado · D-209"
        ),
    )
    cobertura: Optional[CoberturaV1] = Field(
        ...,
        description="None em MESMA_ABA_EM_COLUNAS (cobertura 100% por construção · não Decimal('1'))",
    )
    valor_por_campo: List[ValorPorCampoV1] = Field(
        ...,
        description="1 entrada por campo comparado declarado · até 10",
    )
    resumo_por_agrupador_executivo: Optional[List[LinhaResumoAgrupadorV1]] = Field(
        default=None,
        description="None quando agrupadores executivos não configurados · ordenado T-RANK desc",
    )
    pontes: List[PonteCampoV1] = Field(
        ...,
        description="Campos PERCENTUAL/ADIMENSIONAL/RAZAO omitidos por Q1.B · D-210",
    )
    status_ponte_geral: StatusPonteV1 = Field(
        ...,
        description="Consolidado conforme §2.6 · FECHA por convenção quando len(pontes)==0",
    )
    sintese_diagnostico: SinteseDiagnosticoV1 = Field(...)
    config_aplicada: ConfigAplicadaV1 = Field(...)
    leitura_qualitativa: LeituraQualitativaV1 = Field(...)
    warnings_emitidos: List[WarningV1] = Field(
        default_factory=list,
        description="W-V1-TOL/DUP/AMB/UNIDADE + warnings herdados do motor",
    )
    modelo_aplicado: Optional[ModeloAplicadoV1] = Field(default=None)

    @model_validator(mode="after")
    def _validar_invariantes_principal(self) -> "ConciliacaoV1Result":
        # I1 · classificacao_por_registro >= 1 (motor recusa execução se 0)
        if len(self.classificacao_por_registro) < 1:
            raise ValueError(
                "len(classificacao_por_registro) deve ser >= 1 · motor recusa execução com 0 registros"
            )
        # I2 · soma das contagens == len(classificacao)
        soma_contagens = sum(self.contagem_por_classificacao.values())
        if soma_contagens != len(self.classificacao_por_registro):
            raise ValueError(
                f"sum(contagem_por_classificacao) ({soma_contagens}) != len(classificacao_por_registro) "
                f"({len(self.classificacao_por_registro)})"
            )
        # I3 · len(valor_por_campo) == len(campos_comparados)
        n_campos = len(self.conciliacao_realizada.campos_comparados)
        if len(self.valor_por_campo) != n_campos:
            raise ValueError(
                f"len(valor_por_campo) ({len(self.valor_por_campo)}) != len(campos_comparados) ({n_campos})"
            )
        # I4 · len(pontes) == campos elegíveis (não-PERCENTUAL/ADIMENSIONAL/RAZAO)
        n_pontes_esperadas = len(
            [c for c in self.conciliacao_realizada.campos_comparados if c.unidade not in UNIDADES_INELEGIVEIS_PONTE]
        )
        if len(self.pontes) != n_pontes_esperadas:
            raise ValueError(
                f"len(pontes) ({len(self.pontes)}) != n_campos_eleg√≠veis ({n_pontes_esperadas}) · "
                f"unidades inelegíveis: {UNIDADES_INELEGIVEIS_PONTE}"
            )
        # I5 · todas as chaves em enum (Pydantic já valida via type) · garantia explícita
        for chave in self.contagem_por_classificacao:
            if not isinstance(chave, ClassificacaoRegistroV1):
                raise ValueError(
                    f"chave de contagem_por_classificacao deve ser ClassificacaoRegistroV1 · recebido {type(chave)}"
                )
        # I6 · Em MESMA_ABA_EM_COLUNAS · 4 contagens zeradas
        if self.conciliacao_realizada.caso_logico_inferido == CasoLogicoV1.MESMA_ABA_EM_COLUNAS:
            zerados_obrigatorios = (
                ClassificacaoRegistroV1.SO_ORIGEM,
                ClassificacaoRegistroV1.SO_COMPARADO,
                ClassificacaoRegistroV1.DIVERGENCIA_DUPLICIDADE,
                ClassificacaoRegistroV1.DIVERGENCIA_AMBIGUIDADE,
            )
            for c in zerados_obrigatorios:
                if self.contagem_por_classificacao.get(c, 0) != 0:
                    raise ValueError(
                        f"MESMA_ABA_EM_COLUNAS exige contagem[{c.value}] == 0 · "
                        f"recebido {self.contagem_por_classificacao.get(c, 0)}"
                    )
            # I7 · Em MESMA_ABA_EM_COLUNAS · cobertura == None
            if self.cobertura is not None:
                raise ValueError(
                    "MESMA_ABA_EM_COLUNAS exige cobertura == None · cobertura 100% por construção (não Decimal('1'))"
                )
        return self


# ---------------------------------------------------------------------------
# Helpers privados (preencher nas Fases 2-5)
# ---------------------------------------------------------------------------


class ParCasado(BaseModel):
    """Output interno da Etapa 4 · não exposto no contrato final."""
    model_config = ConfigDict(use_enum_values=False)

    chave_consolidada: str
    valores_agrupadores: Dict[str, str]
    tipo: Literal["MATCHED", "SO_ORIGEM", "SO_COMPARADO", "DUPLICIDADE", "AMBIGUIDADE"]
    indice_origem: Optional[int] = Field(default=None)
    indice_comparado: Optional[int] = Field(default=None)
    candidatos_origem: List[int] = Field(default_factory=list)
    candidatos_comparado: List[int] = Field(default_factory=list)


def _to_decimal_unidade(
    valor: Any,
    unidade: UnidadeCanonica,
) -> Optional[Decimal]:
    """Q2 · Decimal-na-fronteira · float→Decimal preservando precisão.

    Trata None/NaN/string-vazia como ausência (None). Mantém precisão original
    via str() (não quantiza por unidade · spec não especifica casas decimais).
    """
    if valor is None:
        return None
    if isinstance(valor, Decimal):
        return valor
    if isinstance(valor, float) and pd.isna(valor):
        return None
    if isinstance(valor, str) and valor.strip() == "":
        return None
    try:
        # Q2 Decimal-na-fronteira · str() preserva representação
        return Decimal(str(valor))
    except (ValueError, ArithmeticError, TypeError):
        return None


def _eh_valor_ausente(valor: Any) -> bool:
    """True quando valor é None, NaN, ou string vazia."""
    if valor is None:
        return True
    if isinstance(valor, float) and pd.isna(valor):
        return True
    if isinstance(valor, str) and valor.strip() == "":
        return True
    return False


def _str_chave(valor: Any) -> str:
    """Converte valor para string chave de match · preserva zeros à esquerda · None → ''."""
    if _eh_valor_ausente(valor):
        return ""
    if isinstance(valor, float):
        # Inteiro-valued float vira "123" não "123.0"
        if valor.is_integer():
            return str(int(valor))
        return str(valor)
    return str(valor)


def _make_motor_meta(motor_result: MotorResult) -> MotorResultMeta:
    """Constroi MotorResultMeta a partir de MotorResult · padrão V2 herdado."""
    return MotorResultMeta(
        total_linhas_originais=motor_result.total_linhas_originais,
        total_linhas_processadas=motor_result.total_linhas_processadas,
        modo_upload=motor_result.modo_upload,
        timestamp_processamento=motor_result.timestamp_processamento,
        warnings_motor=list(motor_result.warnings),
    )


_SEVERIDADE_POR_CATEGORIA: Dict[str, str] = {
    CategoriaWarning.INFORMATIVO.value: "INFORMATIVO",
    CategoriaWarning.AJUSTE_LEVE.value: "AJUSTE_LEVE",
    CategoriaWarning.ALERTA_ESTRUTURAL_LEVE.value: "ALERTA_ESTRUTURAL",
    CategoriaWarning.ALERTA_ESTRUTURAL.value: "ALERTA_ESTRUTURAL",
    CategoriaWarning.DECISAO_USUARIO.value: "DECISAO_USUARIO",
    CategoriaWarning.ESCAPE_ACIONADO.value: "ESCAPE",
}


def _flatten_warnings(warnings_motor: List[WarningEstrutural]) -> List[WarningV1]:
    """Converte WarningEstrutural (Fundação) → WarningV1 · agrupa por código · n_ocorrencias."""
    grupos: Dict[str, List[WarningEstrutural]] = {}
    for w in warnings_motor:
        grupos.setdefault(w.codigo, []).append(w)
    out: List[WarningV1] = []
    for codigo in sorted(grupos.keys()):
        lista = grupos[codigo]
        cat_value = (
            lista[0].categoria.value if hasattr(lista[0].categoria, "value") else str(lista[0].categoria)
        )
        severidade = _SEVERIDADE_POR_CATEGORIA.get(cat_value, "INFORMATIVO")
        # Verifica se codigo bate com pattern aceito por WarningV1; "W-..." sempre passa.
        if not codigo.startswith("W-"):
            continue
        out.append(
            WarningV1(
                codigo=codigo,
                severidade=severidade,  # type: ignore[arg-type]
                n_ocorrencias=sum(1 for _ in lista),
                detalhes=[w.contexto for w in lista if w.contexto],
            )
        )
    return out


def _etapa_1_leitura(
    motor_result: MotorResult,
    config: Dict[str, Any],
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Etapa 1 · particiona MotorResult.df em (df_origem, df_comparado).

    DUAL: usa origem_comparado_map para particionar.
    SIMPLES: retorna (df, df) — assume MESMA_ABA_EM_COLUNAS.

    Levanta ValueError com prefixo 'B-V1-NO-UPLOAD' quando df vazio.
    """
    if motor_result is None:
        raise ValueError("B-V1-NO-UPLOAD: motor_result é None · faça upload das bases para começar")
    df = motor_result.df
    if df is None or len(df) == 0:
        raise ValueError(
            "B-V1-NO-UPLOAD: motor_result.df vazio · faça upload das bases para começar"
        )

    if motor_result.modo_upload == "DUAL":
        ocm = motor_result.origem_comparado_map
        if ocm is None:
            # DUAL sem map é estado inválido · fallback: trata df inteiro como Origem · Comparado vazio
            raise ValueError(
                "B-V1-MOTOR-FALHOU: modo_upload=DUAL exige origem_comparado_map populado · recebido None"
            )
        idx_origem = sorted(i for i, papel in ocm.items() if papel == "origem")
        idx_comparado = sorted(i for i, papel in ocm.items() if papel == "comparado")
        df_origem = df.loc[idx_origem].reset_index(drop=True) if idx_origem else df.iloc[0:0].copy()
        df_comparado = df.loc[idx_comparado].reset_index(drop=True) if idx_comparado else df.iloc[0:0].copy()
        return df_origem, df_comparado

    # SIMPLES · MESMA_ABA_EM_COLUNAS · mesmo df dos dois lados
    return df, df


def _etapa_2_validar_apontamentos(
    df_origem: pd.DataFrame,
    df_comparado: pd.DataFrame,
    config: Dict[str, Any],
    caso_logico: CasoLogicoV1,
) -> Tuple[List[BloqueioOperacional], List[WarningV1]]:
    """Etapa 2 · valida agrupadores/campos · dispara bloqueios e warnings.

    Levanta ValueError("B-V1-...: ...") para bloqueios não-escapáveis.
    Retorna (bloqueios_escapados, warnings_v1) para bloqueios escapáveis com
    `escape_acionado` em config.
    """
    agrupadores: List[AgrupadorMatchV1] = config["agrupadores_match"]
    campos: List[CampoComparadoV1] = config["campos_comparados"]
    thresholds: Dict[str, Any] = config.get("thresholds", {})
    escapes: Dict[str, bool] = config.get("escapes", {})
    bloqueios_escapados: List[BloqueioOperacional] = []
    warnings_v1: List[WarningV1] = []

    # B-V1-AGRUPADOR-ZERO / EXCEDE
    if len(agrupadores) == 0:
        raise ValueError("B-V1-AGRUPADOR-ZERO: configure ao menos 1 agrupador de match")
    if len(agrupadores) > 5:
        raise ValueError(
            f"B-V1-AGRUPADOR-EXCEDE: limite de 5 agrupadores no MVP · recebido {len(agrupadores)}"
        )

    # B-V1-CAMPO-ZERO / EXCEDE
    if len(campos) == 0:
        raise ValueError("B-V1-CAMPO-ZERO: configure ao menos 1 campo comparado para a análise")
    if len(campos) > 10:
        raise ValueError(
            f"B-V1-CAMPO-EXCEDE: limite de 10 campos no MVP · recebido {len(campos)}"
        )

    # B-V1-MESMA-COLUNA · só relevante em MESMA_ABA_EM_COLUNAS
    if caso_logico == CasoLogicoV1.MESMA_ABA_EM_COLUNAS:
        for ag in agrupadores:
            if ag.nome_origem == ag.nome_comparado:
                raise ValueError(
                    f"B-V1-MESMA-COLUNA: agrupador '{ag.rotulo_analitico}' aponta a mesma coluna "
                    f"({ag.nome_origem}) em Origem e Comparado · escolha colunas distintas"
                )
        for c in campos:
            if c.nome_origem == c.nome_comparado:
                raise ValueError(
                    f"B-V1-MESMA-COLUNA: campo '{c.nome_analitico}' aponta a mesma coluna "
                    f"({c.nome_origem}) em Origem e Comparado · escolha colunas distintas"
                )

    # Coluna existe em df?
    for ag in agrupadores:
        if ag.nome_origem not in df_origem.columns:
            raise ValueError(
                f"B-V1-MOTOR-FALHOU: coluna '{ag.nome_origem}' (agrupador {ag.rotulo_analitico}) "
                f"ausente em df_origem · colunas disponíveis: {list(df_origem.columns)}"
            )
        if ag.nome_comparado not in df_comparado.columns:
            raise ValueError(
                f"B-V1-MOTOR-FALHOU: coluna '{ag.nome_comparado}' (agrupador {ag.rotulo_analitico}) "
                f"ausente em df_comparado · colunas disponíveis: {list(df_comparado.columns)}"
            )
    for c in campos:
        if c.nome_origem not in df_origem.columns:
            raise ValueError(
                f"B-V1-MOTOR-FALHOU: coluna '{c.nome_origem}' (campo {c.nome_analitico}) "
                f"ausente em df_origem"
            )
        if c.nome_comparado not in df_comparado.columns:
            raise ValueError(
                f"B-V1-MOTOR-FALHOU: coluna '{c.nome_comparado}' (campo {c.nome_analitico}) "
                f"ausente em df_comparado"
            )

    # B-V1-CHAVE-INVALIDA · escapável · TED chave_nulos_max default 50%
    chave_nulos_max = Decimal(str(thresholds.get("chave_nulos_max", DEFAULT_CHAVE_NULOS_MAX)))
    for ag in agrupadores:
        for lado, df_x, col in (
            ("origem", df_origem, ag.nome_origem),
            ("comparado", df_comparado, ag.nome_comparado),
        ):
            if len(df_x) == 0:
                continue
            n_nulos = sum(1 for v in df_x[col] if _eh_valor_ausente(v))
            pct_nulos = Decimal(n_nulos) / Decimal(len(df_x))
            if pct_nulos >= chave_nulos_max:
                msg = (
                    f"B-V1-CHAVE-INVALIDA: coluna '{col}' (lado {lado}) tem "
                    f"{(pct_nulos * 100):.1f}% de valores vazios · escolha outra coluna"
                )
                if escapes.get("B-V1-CHAVE-INVALIDA", False):
                    bloqueios_escapados.append(
                        BloqueioOperacional(
                            codigo="B-V1-CHAVE-INVALIDA",
                            condicao_disparo=msg,
                            escapavel=True,
                            escape_acionado=True,
                            warning_pos_escape="W-V1-ESCAPE-CHAVE-INVALIDA",
                            contexto_disparo={
                                "lado": lado, "coluna": col,
                                "pct_nulos": str(pct_nulos), "threshold": str(chave_nulos_max),
                            },
                        )
                    )
                else:
                    raise ValueError(msg)

    # B-V1-RESULTADO-EXCEDE · escapável · TED volume_max default 500_000
    volume_max = int(thresholds.get("volume_max", DEFAULT_VOLUME_MAX))
    n_potencial = len(df_origem) + len(df_comparado)
    if caso_logico == CasoLogicoV1.MESMA_ABA_EM_COLUNAS:
        n_potencial = len(df_origem)
    if n_potencial > volume_max:
        msg = (
            f"B-V1-RESULTADO-EXCEDE: análise gerou {n_potencial} registros · "
            f"acima do limite de {volume_max} (TED volume_max) · simplifique a chave ou aplique filtro prévio"
        )
        if escapes.get("B-V1-RESULTADO-EXCEDE", False):
            bloqueios_escapados.append(
                BloqueioOperacional(
                    codigo="B-V1-RESULTADO-EXCEDE",
                    condicao_disparo=msg,
                    escapavel=True,
                    escape_acionado=True,
                    warning_pos_escape="W-V1-ESCAPE-RESULTADO-EXCEDE",
                    contexto_disparo={"n_potencial": n_potencial, "volume_max": volume_max},
                )
            )
        else:
            raise ValueError(msg)

    # W-V1-UNIDADE · tipo_logico declarado vs unidade declarada divergente da inferida
    column_meta = motor_result_column_meta_from_config(config)
    for c in campos:
        unidade_inferida = None
        if column_meta is not None:
            meta_o = column_meta.get(c.nome_origem)
            if meta_o is not None and meta_o.unidade is not None:
                unidade_inferida = meta_o.unidade
        if unidade_inferida is not None and unidade_inferida != c.unidade.value:
            warnings_v1.append(
                WarningV1(
                    codigo="W-V1-UNIDADE",
                    severidade="AJUSTE_LEVE",
                    n_ocorrencias=1,
                    detalhes=[{
                        "campo": c.nome_analitico,
                        "unidade_declarada": c.unidade.value,
                        "unidade_inferida": unidade_inferida,
                    }],
                )
            )

    return bloqueios_escapados, warnings_v1


def motor_result_column_meta_from_config(config: Dict[str, Any]) -> Optional[Dict[str, ColumnMeta]]:
    """Extrai column_meta do config (caso o motor_result tenha sido propagado)."""
    return config.get("_column_meta")


def _etapa_3_inferir_caso_logico(
    df_origem: pd.DataFrame,
    df_comparado: pd.DataFrame,
    config: Dict[str, Any],
) -> CasoLogicoV1:
    """Etapa 3 · S-V1 §1.3 · regra:
    - aba_origem == aba_comparado E todos coluna_origem != coluna_comparado → MESMA_ABA_EM_COLUNAS
    - aba_origem != aba_comparado → ABAS_DISTINTAS
    - Caso degenerado (mesma aba · alguma coluna_origem == coluna_comparado) → B-V1-MESMA-COLUNA
    - Apontamentos misturando abas → B-V1-MISTURA-ABAS
    """
    aba_origem = config.get("aba_origem", "")
    aba_comparado = config.get("aba_comparado", "")
    arquivo_origem = config.get("arquivo_origem", "")
    arquivo_comparado = config.get("arquivo_comparado", "")
    agrupadores: List[AgrupadorMatchV1] = config["agrupadores_match"]
    campos: List[CampoComparadoV1] = config["campos_comparados"]

    mesma_aba = (aba_origem == aba_comparado) and (arquivo_origem == arquivo_comparado)
    if mesma_aba:
        # Verificar coluna_origem != coluna_comparado em todos
        for ag in agrupadores:
            if ag.nome_origem == ag.nome_comparado:
                raise ValueError(
                    f"B-V1-MESMA-COLUNA: agrupador '{ag.rotulo_analitico}' aponta mesma coluna em mesma aba"
                )
        for c in campos:
            if c.nome_origem == c.nome_comparado:
                raise ValueError(
                    f"B-V1-MESMA-COLUNA: campo '{c.nome_analitico}' aponta mesma coluna em mesma aba"
                )
        return CasoLogicoV1.MESMA_ABA_EM_COLUNAS
    return CasoLogicoV1.ABAS_DISTINTAS


def _matches_agrupador(
    ag: AgrupadorMatchV1,
    val_o: Any,
    val_c: Any,
    case_sensitive: bool = False,
) -> bool:
    """Q5 · Aplica modo_match a um par de valores. Modos não-EXATO são simétricos."""
    a = _str_chave(val_o)
    b = _str_chave(val_c)
    if not case_sensitive:
        a = a.lower()
        b = b.lower()
    if ag.modo_match == ModoMatchV1.EXATO:
        return a == b
    if ag.modo_match == ModoMatchV1.CONTEM:
        if not a or not b:
            return False
        return a in b or b in a
    if ag.modo_match == ModoMatchV1.INICIA_COM:
        if not a or not b:
            return False
        return a.startswith(b) or b.startswith(a)
    if ag.modo_match == ModoMatchV1.TERMINA_COM:
        if not a or not b:
            return False
        return a.endswith(b) or b.endswith(a)
    return False


def _build_chave_consolidada(row: pd.Series, agrupadores: List[AgrupadorMatchV1], lado: str) -> str:
    """Concatena valores dos agrupadores com '|' · zeros à esquerda preservados."""
    if lado == "origem":
        partes = [_str_chave(row[ag.nome_origem]) for ag in agrupadores]
    else:
        partes = [_str_chave(row[ag.nome_comparado]) for ag in agrupadores]
    return "|".join(partes)


def _build_valores_agrupadores(
    row: pd.Series, agrupadores: List[AgrupadorMatchV1], lado: str
) -> Dict[str, str]:
    """rotulo_analitico → valor (str) · usa coluna do lado especificado."""
    if lado == "origem":
        return {ag.rotulo_analitico: _str_chave(row[ag.nome_origem]) for ag in agrupadores}
    return {ag.rotulo_analitico: _str_chave(row[ag.nome_comparado]) for ag in agrupadores}


def _etapa_4a_match_abas_distintas(
    df_origem: pd.DataFrame,
    df_comparado: pd.DataFrame,
    config: Dict[str, Any],
) -> List[ParCasado]:
    """Etapa 4-A · ABAS_DISTINTAS · Q5 (4 modos) · detecta DUPLICIDADE/AMBIGUIDADE.

    Estratégia:
    - Constrói chave_consolidada por linha em cada lado.
    - Detecta DUPLICIDADE: mesma chave 2+ vezes em pelo menos 1 lado.
    - EXATO em todos agrupadores: merge por chave (set intersection).
    - Não-EXATO: varredura O(n*m) com função _matches_agrupador.
    - AMBIGUIDADE: 1 i_o casa com ≥ 2 j_c (ou vice-versa) em modo não-EXATO.
    """
    agrupadores: List[AgrupadorMatchV1] = config["agrupadores_match"]
    case_sensitive: bool = config.get("thresholds", {}).get("match_case_sensitive", False)

    # Construir chaves
    chaves_origem = [
        _build_chave_consolidada(row, agrupadores, "origem")
        for _, row in df_origem.iterrows()
    ]
    chaves_comparado = [
        _build_chave_consolidada(row, agrupadores, "comparado")
        for _, row in df_comparado.iterrows()
    ]

    # Mapas chave → [índices]
    idx_o_por_chave: Dict[str, List[int]] = {}
    for i, k in enumerate(chaves_origem):
        idx_o_por_chave.setdefault(k, []).append(i)
    idx_c_por_chave: Dict[str, List[int]] = {}
    for j, k in enumerate(chaves_comparado):
        idx_c_por_chave.setdefault(k, []).append(j)

    # Determine all-EXATO
    todos_exato = all(ag.modo_match == ModoMatchV1.EXATO for ag in agrupadores)

    pares: List[ParCasado] = []

    if todos_exato:
        # Merge por chave (set)
        chaves_o_set = set(idx_o_por_chave.keys())
        chaves_c_set = set(idx_c_por_chave.keys())
        intersect = chaves_o_set & chaves_c_set
        so_o_set = chaves_o_set - chaves_c_set
        so_c_set = chaves_c_set - chaves_o_set

        for k in sorted(intersect):
            idxs_o = idx_o_por_chave[k]
            idxs_c = idx_c_por_chave[k]
            valores_ag = _build_valores_agrupadores(df_origem.iloc[idxs_o[0]], agrupadores, "origem")
            if len(idxs_o) > 1 or len(idxs_c) > 1:
                pares.append(ParCasado(
                    chave_consolidada=k,
                    valores_agrupadores=valores_ag,
                    tipo="DUPLICIDADE",
                    candidatos_origem=sorted(idxs_o),
                    candidatos_comparado=sorted(idxs_c),
                ))
            else:
                pares.append(ParCasado(
                    chave_consolidada=k,
                    valores_agrupadores=valores_ag,
                    tipo="MATCHED",
                    indice_origem=idxs_o[0],
                    indice_comparado=idxs_c[0],
                ))

        for k in sorted(so_o_set):
            idxs_o = idx_o_por_chave[k]
            valores_ag = _build_valores_agrupadores(df_origem.iloc[idxs_o[0]], agrupadores, "origem")
            if len(idxs_o) > 1:
                pares.append(ParCasado(
                    chave_consolidada=k,
                    valores_agrupadores=valores_ag,
                    tipo="DUPLICIDADE",
                    candidatos_origem=sorted(idxs_o),
                ))
            else:
                pares.append(ParCasado(
                    chave_consolidada=k,
                    valores_agrupadores=valores_ag,
                    tipo="SO_ORIGEM",
                    indice_origem=idxs_o[0],
                ))

        for k in sorted(so_c_set):
            idxs_c = idx_c_por_chave[k]
            valores_ag = _build_valores_agrupadores(df_comparado.iloc[idxs_c[0]], agrupadores, "comparado")
            if len(idxs_c) > 1:
                pares.append(ParCasado(
                    chave_consolidada=k,
                    valores_agrupadores=valores_ag,
                    tipo="DUPLICIDADE",
                    candidatos_comparado=sorted(idxs_c),
                ))
            else:
                pares.append(ParCasado(
                    chave_consolidada=k,
                    valores_agrupadores=valores_ag,
                    tipo="SO_COMPARADO",
                    indice_comparado=idxs_c[0],
                ))

        return pares

    # Modo não-EXATO · primeiro detecta DUPLICIDADE por chave consolidada (S-V1 §2.2: "ANTES do match")
    chaves_dup_o = {k for k, idxs in idx_o_por_chave.items() if len(idxs) > 1}
    chaves_dup_c = {k for k, idxs in idx_c_por_chave.items() if len(idxs) > 1}
    chaves_com_dup = chaves_dup_o | chaves_dup_c

    rows_o_em_dup: set = set()
    rows_c_em_dup: set = set()
    for k in sorted(chaves_com_dup):
        idxs_o = idx_o_por_chave.get(k, [])
        idxs_c = idx_c_por_chave.get(k, [])
        for i in idxs_o:
            rows_o_em_dup.add(i)
        for j in idxs_c:
            rows_c_em_dup.add(j)
        # Determina valores_agrupadores · prefere lado origem · senão comparado
        if idxs_o:
            valores_ag = _build_valores_agrupadores(df_origem.iloc[idxs_o[0]], agrupadores, "origem")
        else:
            valores_ag = _build_valores_agrupadores(df_comparado.iloc[idxs_c[0]], agrupadores, "comparado")
        pares.append(ParCasado(
            chave_consolidada=k,
            valores_agrupadores=valores_ag,
            tipo="DUPLICIDADE",
            candidatos_origem=sorted(idxs_o),
            candidatos_comparado=sorted(idxs_c),
        ))

    # Varredura pairwise (O(n*m)) · pula linhas com chave duplicada
    candidatos_por_o: Dict[int, List[int]] = {}
    candidatos_por_c: Dict[int, List[int]] = {}
    for i_o in range(len(df_origem)):
        if i_o in rows_o_em_dup:
            continue
        for j_c in range(len(df_comparado)):
            if j_c in rows_c_em_dup:
                continue
            todos_match = True
            for ag in agrupadores:
                val_o = df_origem.iloc[i_o][ag.nome_origem]
                val_c = df_comparado.iloc[j_c][ag.nome_comparado]
                if not _matches_agrupador(ag, val_o, val_c, case_sensitive):
                    todos_match = False
                    break
            if todos_match:
                candidatos_por_o.setdefault(i_o, []).append(j_c)
                candidatos_por_c.setdefault(j_c, []).append(i_o)

    # Classificar cada i_o (excluindo linhas em DUPLICIDADE)
    visitados_c: set = set()
    for i_o in range(len(df_origem)):
        if i_o in rows_o_em_dup:
            continue
        cands = candidatos_por_o.get(i_o, [])
        chave_o = chaves_origem[i_o]
        valores_ag = _build_valores_agrupadores(df_origem.iloc[i_o], agrupadores, "origem")
        if len(cands) == 0:
            pares.append(ParCasado(
                chave_consolidada=chave_o,
                valores_agrupadores=valores_ag,
                tipo="SO_ORIGEM",
                indice_origem=i_o,
            ))
        elif len(cands) == 1:
            j_c = cands[0]
            cands_back = candidatos_por_c.get(j_c, [])
            if len(cands_back) > 1:
                pares.append(ParCasado(
                    chave_consolidada=chave_o,
                    valores_agrupadores=valores_ag,
                    tipo="AMBIGUIDADE",
                    indice_origem=i_o,
                    candidatos_comparado=sorted(cands),
                ))
            else:
                pares.append(ParCasado(
                    chave_consolidada=chave_o,
                    valores_agrupadores=valores_ag,
                    tipo="MATCHED",
                    indice_origem=i_o,
                    indice_comparado=j_c,
                ))
            visitados_c.add(j_c)
        else:
            pares.append(ParCasado(
                chave_consolidada=chave_o,
                valores_agrupadores=valores_ag,
                tipo="AMBIGUIDADE",
                indice_origem=i_o,
                candidatos_comparado=sorted(cands),
            ))
            for j_c in cands:
                visitados_c.add(j_c)

    # SO_COMPARADO · qualquer j_c que não foi visitado e não está em DUPLICIDADE
    for j_c in range(len(df_comparado)):
        if j_c in visitados_c or j_c in rows_c_em_dup:
            continue
        if j_c in candidatos_por_c:
            # Foi candidato de alguém · já contado em AMBIGUIDADE
            continue
        chave_c = chaves_comparado[j_c]
        valores_ag = _build_valores_agrupadores(df_comparado.iloc[j_c], agrupadores, "comparado")
        pares.append(ParCasado(
            chave_consolidada=chave_c,
            valores_agrupadores=valores_ag,
            tipo="SO_COMPARADO",
            indice_comparado=j_c,
        ))

    return pares


def _etapa_4b_pareamento_linha_a_linha(
    df_unico: pd.DataFrame,
    config: Dict[str, Any],
) -> List[ParCasado]:
    """Etapa 4-B · MESMA_ABA_EM_COLUNAS · cada linha = par MATCHED por construção (Q6)."""
    agrupadores: List[AgrupadorMatchV1] = config["agrupadores_match"]
    pares: List[ParCasado] = []
    for idx, row in df_unico.iterrows():
        # Chave construída a partir das colunas-Origem dos agrupadores
        partes = [_str_chave(row[ag.nome_origem]) for ag in agrupadores]
        chave = "|".join(partes)
        valores_ag = {ag.rotulo_analitico: _str_chave(row[ag.nome_origem]) for ag in agrupadores}
        pares.append(ParCasado(
            chave_consolidada=chave,
            valores_agrupadores=valores_ag,
            tipo="MATCHED",
            indice_origem=int(idx),
            indice_comparado=int(idx),
        ))
    return pares


def _calcular_status_campo(
    valor_origem: Optional[Decimal],
    valor_comparado: Optional[Decimal],
    tolerancia: Decimal,
) -> StatusCampoV1:
    """S-V1 §2.4 · tabela determinística independente do caso lógico."""
    if valor_origem is None and valor_comparado is None:
        return StatusCampoV1.SEM_VALOR_AMBOS
    if valor_origem is None:
        return StatusCampoV1.SEM_VALOR_ORIGEM
    if valor_comparado is None:
        return StatusCampoV1.SEM_VALOR_COMPARADO
    if valor_origem == valor_comparado:
        return StatusCampoV1.IGUAL
    diff = abs(valor_origem - valor_comparado)
    if diff <= tolerancia and tolerancia > Decimal("0"):
        return StatusCampoV1.DENTRO_TOLERANCIA
    if diff == Decimal("0"):
        return StatusCampoV1.IGUAL  # caso degenerado já tratado
    return StatusCampoV1.DIVERGENTE


def _etapa_5_calcular_diferencas(
    pares: List[ParCasado],
    df_origem: pd.DataFrame,
    df_comparado: pd.DataFrame,
    config: Dict[str, Any],
    caso_logico: CasoLogicoV1,
) -> List[RegistroConciliadoV1]:
    """Etapa 5 · célula a célula aplica tabela §2.4 · Decimal precisão financeira."""
    campos: List[CampoComparadoV1] = config["campos_comparados"]
    registros: List[RegistroConciliadoV1] = []

    for par in pares:
        celulas: List[CelulaCampoV1] = []
        for k, campo in enumerate(campos):
            valor_o: Optional[Decimal] = None
            valor_c: Optional[Decimal] = None

            if par.tipo == "MATCHED":
                if par.indice_origem is not None:
                    raw_o = df_origem.iloc[par.indice_origem][campo.nome_origem]
                    valor_o = _to_decimal_unidade(raw_o, campo.unidade)
                if par.indice_comparado is not None:
                    raw_c = df_comparado.iloc[par.indice_comparado][campo.nome_comparado]
                    valor_c = _to_decimal_unidade(raw_c, campo.unidade)
            elif par.tipo == "SO_ORIGEM":
                if par.indice_origem is not None:
                    raw_o = df_origem.iloc[par.indice_origem][campo.nome_origem]
                    valor_o = _to_decimal_unidade(raw_o, campo.unidade)
            elif par.tipo == "SO_COMPARADO":
                if par.indice_comparado is not None:
                    raw_c = df_comparado.iloc[par.indice_comparado][campo.nome_comparado]
                    valor_c = _to_decimal_unidade(raw_c, campo.unidade)
            # DUPLICIDADE / AMBIGUIDADE: valor_o = valor_c = None (semântica ambígua · §2.4)

            diferenca: Optional[Decimal] = None
            if valor_o is not None and valor_c is not None:
                diferenca = valor_o - valor_c

            status = _calcular_status_campo(valor_o, valor_c, campo.tolerancia)
            celulas.append(CelulaCampoV1(
                campo_indice=k,
                valor_origem=valor_o,
                valor_comparado=valor_c,
                diferenca=diferenca,
                status_campo=status,
            ))

        # Agregados por registro
        if par.tipo in ("MATCHED",):
            diffs_validos = [c.diferenca for c in celulas if c.diferenca is not None]
            diferenca_total = sum(diffs_validos, Decimal("0")) if diffs_validos else Decimal("0")
            sigma_total = sum((abs(d) for d in diffs_validos), Decimal("0")) if diffs_validos else Decimal("0")
            valores_o = [c.valor_origem for c in celulas if c.valor_origem is not None]
            soma_o = sum(valores_o, Decimal("0")) if valores_o else Decimal("0")
            variacao_pct: Optional[Decimal] = None
            if soma_o != Decimal("0"):
                variacao_pct = diferenca_total / soma_o
        else:
            diferenca_total = None
            sigma_total = None
            variacao_pct = None

        # Classificação preliminar (Etapa 6 finaliza)
        cls_preliminar = ClassificacaoRegistroV1.CONCILIADO  # placeholder
        registros.append(RegistroConciliadoV1(
            chave_consolidada=par.chave_consolidada,
            valores_agrupadores=par.valores_agrupadores,
            classificacao_estrutural=cls_preliminar,
            valores_por_campo=celulas,
            diferenca_total_registro=diferenca_total,
            sigma_diferenca_total_registro=sigma_total,
            variacao_total_registro_pct=variacao_pct,
            observacoes=None,
        ))

    return registros


def _etapa_6_classificar_agregada(
    registros_parciais: List[RegistroConciliadoV1],
    pares: List[ParCasado],
    caso_logico: CasoLogicoV1,
    config: Dict[str, Any],
) -> List[RegistroConciliadoV1]:
    """Etapa 6 · §2.3 · Em ABAS_DISTINTAS aplica 6 classes · em MESMA_ABA aplica 2 classes."""
    out: List[RegistroConciliadoV1] = []
    for reg, par in zip(registros_parciais, pares):
        if caso_logico == CasoLogicoV1.ABAS_DISTINTAS:
            if par.tipo == "DUPLICIDADE":
                cls = ClassificacaoRegistroV1.DIVERGENCIA_DUPLICIDADE
            elif par.tipo == "AMBIGUIDADE":
                cls = ClassificacaoRegistroV1.DIVERGENCIA_AMBIGUIDADE
            elif par.tipo == "SO_ORIGEM":
                cls = ClassificacaoRegistroV1.SO_ORIGEM
            elif par.tipo == "SO_COMPARADO":
                cls = ClassificacaoRegistroV1.SO_COMPARADO
            else:  # MATCHED
                if any(c.status_campo == StatusCampoV1.DIVERGENTE for c in reg.valores_por_campo):
                    cls = ClassificacaoRegistroV1.DIVERGENTE_VALOR
                else:
                    cls = ClassificacaoRegistroV1.CONCILIADO
        else:  # MESMA_ABA_EM_COLUNAS · só CONCILIADO ou DIVERGENTE_VALOR
            if any(c.status_campo == StatusCampoV1.DIVERGENTE for c in reg.valores_por_campo):
                cls = ClassificacaoRegistroV1.DIVERGENTE_VALOR
            else:
                cls = ClassificacaoRegistroV1.CONCILIADO

        # Para classes que não são MATCHED em ABAS_DISTINTAS · zero diferenca_total
        if cls in (
            ClassificacaoRegistroV1.SO_ORIGEM,
            ClassificacaoRegistroV1.SO_COMPARADO,
            ClassificacaoRegistroV1.DIVERGENCIA_DUPLICIDADE,
            ClassificacaoRegistroV1.DIVERGENCIA_AMBIGUIDADE,
        ):
            diff_total = None
            sigma_total = None
            variacao_pct = None
        else:
            diff_total = reg.diferenca_total_registro
            sigma_total = reg.sigma_diferenca_total_registro
            variacao_pct = reg.variacao_total_registro_pct

        out.append(RegistroConciliadoV1(
            chave_consolidada=reg.chave_consolidada,
            valores_agrupadores=reg.valores_agrupadores,
            classificacao_estrutural=cls,
            valores_por_campo=reg.valores_por_campo,
            diferenca_total_registro=diff_total,
            sigma_diferenca_total_registro=sigma_total,
            variacao_total_registro_pct=variacao_pct,
            observacoes=reg.observacoes,
        ))
    return out


def _calcular_cobertura(
    registros: List[RegistroConciliadoV1],
    n_origem: int,
    n_comparado: int,
) -> CoberturaV1:
    """Cobertura simétrica de match · usado em ABAS_DISTINTAS."""
    n_o_sem_par = sum(1 for r in registros if r.classificacao_estrutural == ClassificacaoRegistroV1.SO_ORIGEM)
    n_c_sem_par = sum(1 for r in registros if r.classificacao_estrutural == ClassificacaoRegistroV1.SO_COMPARADO)
    n_o_com_par = max(0, n_origem - n_o_sem_par)
    n_c_com_par = max(0, n_comparado - n_c_sem_par)
    cob_o = (Decimal(n_o_com_par) / Decimal(n_origem)) if n_origem > 0 else Decimal("0")
    cob_c = (Decimal(n_c_com_par) / Decimal(n_comparado)) if n_comparado > 0 else Decimal("0")
    return CoberturaV1(
        n_origem_com_par=n_o_com_par, n_origem_sem_par=n_o_sem_par,
        cobertura_origem_pct=cob_o,
        n_comparado_com_par=n_c_com_par, n_comparado_sem_par=n_c_sem_par,
        cobertura_comparado_pct=cob_c,
    )


def _calcular_valor_por_campo(
    registros: List[RegistroConciliadoV1],
    campos: List[CampoComparadoV1],
) -> List[ValorPorCampoV1]:
    """Σ por campo · sigma APENAS em CONCILIADO + DIVERGENTE_VALOR (D-213)."""
    out: List[ValorPorCampoV1] = []
    classes_com_par = {ClassificacaoRegistroV1.CONCILIADO, ClassificacaoRegistroV1.DIVERGENTE_VALOR}
    for k, campo in enumerate(campos):
        soma_o = Decimal("0")
        soma_c = Decimal("0")
        sigma_d = Decimal("0")
        n_tol = 0
        valor_tol = Decimal("0")
        for r in registros:
            celula = r.valores_por_campo[k]
            if celula.valor_origem is not None:
                soma_o += celula.valor_origem
            if celula.valor_comparado is not None:
                soma_c += celula.valor_comparado
            if r.classificacao_estrutural in classes_com_par and celula.diferenca is not None:
                sigma_d += abs(celula.diferenca)
            if celula.status_campo == StatusCampoV1.DENTRO_TOLERANCIA:
                n_tol += 1
                if celula.diferenca is not None:
                    valor_tol += abs(celula.diferenca)
        out.append(ValorPorCampoV1(
            nome_analitico=campo.nome_analitico,
            unidade=campo.unidade,
            soma_origem=soma_o,
            soma_comparado=soma_c,
            diferenca_liquida=soma_o - soma_c,
            sigma_diferenca=sigma_d,
            n_tolerancia_absorvida=n_tol,
            valor_tolerancia_absorvida=valor_tol,
        ))
    return out


def _calcular_pontes(
    registros: List[RegistroConciliadoV1],
    campos: List[CampoComparadoV1],
    epsilon_por_unidade: Dict[UnidadeCanonica, Decimal],
    caso_logico: CasoLogicoV1,
) -> List[PonteCampoV1]:
    """Calcula 1 PonteCampoV1 por campo elegível (Q1.B omite PERCENTUAL/ADIMENSIONAL/RAZAO)."""
    out: List[PonteCampoV1] = []
    for k, campo in enumerate(campos):
        if campo.unidade in UNIDADES_INELEGIVEIS_PONTE:
            continue
        saldo_o = Decimal("0")
        saldo_c = Decimal("0")
        ajuste_so_o = Decimal("0")
        ajuste_so_c = Decimal("0")
        ajuste_div = Decimal("0")
        ajuste_tol = Decimal("0")
        for r in registros:
            celula = r.valores_por_campo[k]
            if celula.valor_origem is not None:
                saldo_o += celula.valor_origem
            if celula.valor_comparado is not None:
                saldo_c += celula.valor_comparado
            if r.classificacao_estrutural == ClassificacaoRegistroV1.SO_ORIGEM and celula.valor_origem is not None:
                ajuste_so_o += -celula.valor_origem
            if r.classificacao_estrutural == ClassificacaoRegistroV1.SO_COMPARADO and celula.valor_comparado is not None:
                ajuste_so_c += celula.valor_comparado
            if r.classificacao_estrutural == ClassificacaoRegistroV1.DIVERGENTE_VALOR and celula.diferenca is not None:
                ajuste_div += -celula.diferenca
            if celula.status_campo == StatusCampoV1.DENTRO_TOLERANCIA and celula.diferenca is not None and celula.diferenca != Decimal("0"):
                ajuste_tol += -celula.diferenca

        # Em MESMA_ABA_EM_COLUNAS, ajuste_so_* devem ser zero por construção
        if caso_logico == CasoLogicoV1.MESMA_ABA_EM_COLUNAS:
            ajuste_so_o = Decimal("0")
            ajuste_so_c = Decimal("0")

        saldo_esperado = saldo_o + ajuste_so_o + ajuste_so_c + ajuste_div + ajuste_tol
        residuo = saldo_c - saldo_esperado
        eps = epsilon_por_unidade.get(campo.unidade, Decimal("0"))
        fecha = abs(residuo) <= eps if eps > Decimal("0") else residuo == Decimal("0")

        out.append(PonteCampoV1(
            nome_analitico=campo.nome_analitico,
            unidade=campo.unidade,
            saldo_origem=saldo_o,
            ajuste_so_origem=ajuste_so_o,
            ajuste_so_comparado=ajuste_so_c,
            ajuste_divergentes_valor=ajuste_div,
            ajuste_tolerancia_absorvida=ajuste_tol,
            saldo_comparado_esperado=saldo_esperado,
            saldo_comparado_real=saldo_c,
            residuo=residuo,
            fecha=fecha,
        ))
    return out


def _calcular_status_ponte_geral(pontes: List[PonteCampoV1]) -> StatusPonteV1:
    """S-V1 §2.6 · FECHA quando todas fecham · COM_RESIDUO caso contrário · FECHA por convenção quando vazio."""
    if len(pontes) == 0:
        return StatusPonteV1.FECHA
    if all(p.fecha for p in pontes):
        return StatusPonteV1.FECHA
    return StatusPonteV1.COM_RESIDUO


def _calcular_resumo_por_agrupador_executivo(
    registros: List[RegistroConciliadoV1],
    df_origem: pd.DataFrame,
    df_comparado: pd.DataFrame,
    pares: List[ParCasado],
    config: Dict[str, Any],
    caso_logico: CasoLogicoV1,
) -> Optional[List[LinhaResumoAgrupadorV1]]:
    """1 linha por valor único do(s) agrupador(es) executivo(s) · ordenado T-RANK."""
    agrups_exec: List[str] = config.get("agrupadores_executivos", [])
    if len(agrups_exec) == 0:
        return None
    campos: List[CampoComparadoV1] = config["campos_comparados"]

    # Constrói chave-agrupador-executivo por registro a partir do df de origem
    grupos: Dict[Tuple[str, ...], List[int]] = {}  # tuple(valores) → lista de índices em registros
    for i_reg, (par, reg) in enumerate(zip(pares, registros)):
        # Lê valores das colunas dos agrupadores executivos do lado da Origem (quando MATCHED/SO_ORIGEM)
        # ou do Comparado (quando SO_COMPARADO).
        idx_lookup: Optional[int] = None
        df_lookup: Optional[pd.DataFrame] = None
        if par.indice_origem is not None:
            idx_lookup = par.indice_origem
            df_lookup = df_origem
        elif par.indice_comparado is not None:
            idx_lookup = par.indice_comparado
            df_lookup = df_comparado
        else:
            # DUPLICIDADE/AMBIGUIDADE com candidatos · usa primeiro candidato
            if par.candidatos_origem:
                idx_lookup = par.candidatos_origem[0]
                df_lookup = df_origem
            elif par.candidatos_comparado:
                idx_lookup = par.candidatos_comparado[0]
                df_lookup = df_comparado

        if idx_lookup is None or df_lookup is None:
            continue
        valores = tuple(
            _str_chave(df_lookup.iloc[idx_lookup][col]) for col in agrups_exec if col in df_lookup.columns
        )
        if len(valores) != len(agrups_exec):
            # Coluna ausente · pula
            continue
        grupos.setdefault(valores, []).append(i_reg)

    linhas: List[LinhaResumoAgrupadorV1] = []
    for valores_tuple, indices in grupos.items():
        valores_dict = {col: val for col, val in zip(agrups_exec, valores_tuple)}
        sub_regs = [registros[i] for i in indices]
        n_conc = sum(1 for r in sub_regs if r.classificacao_estrutural == ClassificacaoRegistroV1.CONCILIADO)
        n_div = sum(1 for r in sub_regs if r.classificacao_estrutural == ClassificacaoRegistroV1.DIVERGENTE_VALOR)
        n_so_o = sum(1 for r in sub_regs if r.classificacao_estrutural == ClassificacaoRegistroV1.SO_ORIGEM)
        n_so_c = sum(1 for r in sub_regs if r.classificacao_estrutural == ClassificacaoRegistroV1.SO_COMPARADO)

        metricas: List[MetricaCampoAgrupadorV1] = []
        diff_total = Decimal("0")
        for k, campo in enumerate(campos):
            soma_o = Decimal("0")
            soma_c = Decimal("0")
            sigma = Decimal("0")
            for r in sub_regs:
                celula = r.valores_por_campo[k]
                if celula.valor_origem is not None:
                    soma_o += celula.valor_origem
                if celula.valor_comparado is not None:
                    soma_c += celula.valor_comparado
                if celula.diferenca is not None:
                    sigma += abs(celula.diferenca)
            diff_liquida = soma_o - soma_c
            diff_total += diff_liquida
            metricas.append(MetricaCampoAgrupadorV1(
                nome_analitico=campo.nome_analitico,
                unidade=campo.unidade,
                soma_origem=soma_o,
                soma_comparado=soma_c,
                diferenca_liquida=diff_liquida,
                sigma_diferenca=sigma,
            ))

        linhas.append(LinhaResumoAgrupadorV1(
            valores_agrupador=valores_dict,
            n_conciliados=n_conc,
            n_divergentes_valor=n_div,
            n_so_origem=n_so_o if caso_logico == CasoLogicoV1.ABAS_DISTINTAS else 0,
            n_so_comparado=n_so_c if caso_logico == CasoLogicoV1.ABAS_DISTINTAS else 0,
            metricas_por_campo=metricas,
            diferenca_liquida_total=diff_total,
        ))

    # Ordenação T-RANK · |diff_total| desc · empate alfabético (P-V1-TEC-03)
    def _key(linha: LinhaResumoAgrupadorV1):
        return (
            -abs(linha.diferenca_liquida_total),
            tuple(sorted(linha.valores_agrupador.values())),
        )
    return sorted(linhas, key=_key)


def _calcular_sintese(
    registros: List[RegistroConciliadoV1],
    pares: List[ParCasado],
    warnings_emitidos: List[WarningV1],
    caso_logico: CasoLogicoV1,
) -> SinteseDiagnosticoV1:
    """4 contadores · em MESMA_ABA_EM_COLUNAS dup/amb=0 por construção."""
    n_tol = 0
    val_tol = Decimal("0")
    for r in registros:
        for c in r.valores_por_campo:
            if c.status_campo == StatusCampoV1.DENTRO_TOLERANCIA:
                n_tol += 1
                if c.diferenca is not None:
                    val_tol += abs(c.diferenca)

    if caso_logico == CasoLogicoV1.MESMA_ABA_EM_COLUNAS:
        n_chaves_dup = 0
        n_reg_dup = 0
        n_chaves_amb = 0
        n_reg_amb = 0
    else:
        n_chaves_dup = sum(1 for p in pares if p.tipo == "DUPLICIDADE")
        n_reg_dup = sum(
            len(p.candidatos_origem) + len(p.candidatos_comparado) for p in pares if p.tipo == "DUPLICIDADE"
        )
        n_chaves_amb = sum(1 for p in pares if p.tipo == "AMBIGUIDADE")
        n_reg_amb = sum(
            (1 if p.indice_origem is not None else 0) + len(p.candidatos_comparado)
            for p in pares if p.tipo == "AMBIGUIDADE"
        )

    n_warn_ativos = sum(1 for w in warnings_emitidos if w.n_ocorrencias > 0)
    return SinteseDiagnosticoV1(
        n_tolerancia_absorvida=n_tol,
        valor_tolerancia_absorvida=val_tol,
        n_chaves_duplicadas=n_chaves_dup,
        n_registros_afetados_duplicidade=n_reg_dup,
        n_chaves_ambiguas=n_chaves_amb,
        n_registros_afetados_ambiguidade=n_reg_amb,
        n_warnings_ativos=n_warn_ativos,
    )


def _emitir_warnings_pos_pipeline(
    registros: List[RegistroConciliadoV1],
    pares: List[ParCasado],
    caso_logico: CasoLogicoV1,
) -> List[WarningV1]:
    """W-V1-TOL · W-V1-DUP · W-V1-AMB · padrão de exibição §2.7 (zero ocorrências preservado)."""
    out: List[WarningV1] = []
    # W-V1-TOL · ≥ 1 registro CONCILIADO com diferenca != 0
    n_tol = 0
    for r in registros:
        if r.classificacao_estrutural == ClassificacaoRegistroV1.CONCILIADO:
            for c in r.valores_por_campo:
                if c.status_campo == StatusCampoV1.DENTRO_TOLERANCIA:
                    n_tol += 1
    out.append(WarningV1(
        codigo="W-V1-TOL",
        severidade="INFORMATIVO",
        n_ocorrencias=n_tol,
        detalhes=[],
    ))

    # W-V1-DUP · só em ABAS_DISTINTAS · zerado em MESMA_ABA com microcopy explicativa
    if caso_logico == CasoLogicoV1.ABAS_DISTINTAS:
        n_dup = sum(1 for p in pares if p.tipo == "DUPLICIDADE")
    else:
        n_dup = 0
    out.append(WarningV1(
        codigo="W-V1-DUP",
        severidade="ALERTA_ESTRUTURAL",
        n_ocorrencias=n_dup,
        detalhes=([{"caso_logico": caso_logico.value, "nota": "não aplicável neste caso lógico (mesma aba em colunas)"}]
                  if caso_logico == CasoLogicoV1.MESMA_ABA_EM_COLUNAS else []),
    ))

    # W-V1-AMB · análogo
    if caso_logico == CasoLogicoV1.ABAS_DISTINTAS:
        n_amb = sum(1 for p in pares if p.tipo == "AMBIGUIDADE")
    else:
        n_amb = 0
    out.append(WarningV1(
        codigo="W-V1-AMB",
        severidade="ALERTA_ESTRUTURAL",
        n_ocorrencias=n_amb,
        detalhes=([{"caso_logico": caso_logico.value, "nota": "não aplicável neste caso lógico (mesma aba em colunas)"}]
                  if caso_logico == CasoLogicoV1.MESMA_ABA_EM_COLUNAS else []),
    ))

    return out


def _etapa_7_agregacoes(
    registros: List[RegistroConciliadoV1],
    pares: List[ParCasado],
    df_origem: pd.DataFrame,
    df_comparado: pd.DataFrame,
    caso_logico: CasoLogicoV1,
    config: Dict[str, Any],
) -> Tuple[
    Optional[CoberturaV1],
    List[ValorPorCampoV1],
    List[PonteCampoV1],
    StatusPonteV1,
    Optional[List[LinhaResumoAgrupadorV1]],
    SinteseDiagnosticoV1,
    List[WarningV1],
]:
    """Etapa 7 · 6 agregações conforme §2.10 do RE."""
    campos: List[CampoComparadoV1] = config["campos_comparados"]
    eps_config = config.get("epsilon_por_unidade", DEFAULT_EPSILON_POR_UNIDADE)
    # Aceita config tanto com chaves UnidadeCanonica quanto str
    eps: Dict[UnidadeCanonica, Decimal] = {}
    for k, v in eps_config.items():
        unidade_k = k if isinstance(k, UnidadeCanonica) else UnidadeCanonica(k)
        eps[unidade_k] = Decimal(str(v))

    # Cobertura
    if caso_logico == CasoLogicoV1.MESMA_ABA_EM_COLUNAS:
        cobertura = None
    else:
        cobertura = _calcular_cobertura(registros, len(df_origem), len(df_comparado))

    valor_por_campo = _calcular_valor_por_campo(registros, campos)
    pontes = _calcular_pontes(registros, campos, eps, caso_logico)
    status_ponte = _calcular_status_ponte_geral(pontes)
    resumo_agrup = _calcular_resumo_por_agrupador_executivo(
        registros, df_origem, df_comparado, pares, config, caso_logico
    )

    warnings_pipeline = _emitir_warnings_pos_pipeline(registros, pares, caso_logico)
    sintese = _calcular_sintese(registros, pares, warnings_pipeline, caso_logico)

    return cobertura, valor_por_campo, pontes, status_ponte, resumo_agrup, sintese, warnings_pipeline


def _construir_resumo_executivo_padrao(
    motor_result: MotorResult,
    config: Dict[str, Any],
    contagem: Dict[ClassificacaoRegistroV1, int],
    cobertura: Optional[CoberturaV1],
    valor_por_campo: List[ValorPorCampoV1],
    status_ponte: StatusPonteV1,
    sintese: SinteseDiagnosticoV1,
    warnings_emitidos: List[WarningV1],
    caso_logico: CasoLogicoV1,
    n_registros_origem: int,
    n_registros_comparado: int,
) -> ResumoExecutivoPadrao:
    """Constrói o ResumoExecutivoPadrao herdado da Fundação · 6 blocos. Fase 4 expande microcopy."""
    cabecalho = CabecalhoExecucao(
        visao="V1",
        modo_upload=motor_result.modo_upload,
        agrupadores=[a.rotulo_analitico for a in config["agrupadores_match"]],
        medida_principal=(
            config["campos_comparados"][0].nome_analitico if config["campos_comparados"] else None
        ),
    )
    total_reg = sum(contagem.values())
    n_conc = contagem.get(ClassificacaoRegistroV1.CONCILIADO, 0)
    taxa = (Decimal(n_conc) / Decimal(total_reg)) if total_reg > 0 else Decimal("0")

    bloco_2: Dict[str, Any] = {
        "taxa_conciliacao_geral": float(taxa),
        "n_registros_origem": n_registros_origem,
        "n_registros_comparado": n_registros_comparado,
        "n_processados": total_reg,
        "status_ponte_geral": status_ponte.value,
        "caso_logico_inferido": caso_logico.value,
    }

    bloco_3: Dict[str, Any] = {
        cls.value: contagem.get(cls, 0) for cls in ClassificacaoRegistroV1
    }

    bloco_4: Dict[str, Any] = {
        "n_tolerancia_absorvida": sintese.n_tolerancia_absorvida,
        "n_chaves_duplicadas": sintese.n_chaves_duplicadas,
        "n_chaves_ambiguas": sintese.n_chaves_ambiguas,
    }

    if cobertura is not None:
        bloco_4["cobertura_origem_pct"] = float(cobertura.cobertura_origem_pct)
        bloco_4["cobertura_comparado_pct"] = float(cobertura.cobertura_comparado_pct)

    leitura = LeituraQualitativa(
        classificacao_ativa="ALTA" if taxa >= Decimal("0.9") else ("MEDIA" if taxa >= Decimal("0.6") else "BAIXA"),
        thresholds_usados={"taxa_alta": 0.9, "taxa_media": 0.6},
        alguma_leitura_alterada_por_edicao=False,
    )

    n_warnings_ativos = sum(1 for w in warnings_emitidos if w.n_ocorrencias > 0)
    qualidade = QualidadeEstrutural(
        total_warnings=n_warnings_ativos,
        warnings_por_categoria={w.severidade: 1 for w in warnings_emitidos if w.n_ocorrencias > 0},
        ajustes_aplicados=0,
        tem_bloqueios_escapados=False,
    )

    return ResumoExecutivoPadrao(
        bloco_1_cabecalho=cabecalho,
        bloco_2_numeros_ancora=bloco_2,
        bloco_3_distribuicao=bloco_3,
        bloco_4_elementos_destacados=bloco_4,
        bloco_5_leitura_qualitativa=leitura,
        bloco_6_qualidade_estrutural=qualidade,
    )


def _construir_leitura_qualitativa_v1(
    contagem: Dict[ClassificacaoRegistroV1, int],
    caso_logico: CasoLogicoV1,
    config: Dict[str, Any],
) -> LeituraQualitativaV1:
    """Texto-livre parametrizado · 3-6 frases · zero invenção · S-V1 §1.19."""
    total = sum(contagem.values())
    n_conc = contagem.get(ClassificacaoRegistroV1.CONCILIADO, 0)
    taxa = (Decimal(n_conc) / Decimal(total)) if total > 0 else Decimal("0")
    if taxa >= Decimal("0.9"):
        faixa = "ALTA"
    elif taxa >= Decimal("0.6"):
        faixa = "MEDIA"
    else:
        faixa = "BAIXA"

    frase_caso = (
        "A análise foi executada no caso lógico ABAS_DISTINTAS · com match entre as bases."
        if caso_logico == CasoLogicoV1.ABAS_DISTINTAS
        else "A análise foi executada no caso lógico MESMA_ABA_EM_COLUNAS · cada linha é par casado por construção."
    )
    frase_taxa = (
        f"A taxa de conciliação geral é {(taxa * 100):.1f}% · classificação {faixa}."
    )
    n_div = contagem.get(ClassificacaoRegistroV1.DIVERGENTE_VALOR, 0)
    frase_div = (
        f"Foram detectados {n_div} registros com divergência de valor."
        if n_div > 0
        else "Não foram detectados registros com divergência de valor."
    )

    texto = " ".join([frase_caso, frase_taxa, frase_div])
    return LeituraQualitativaV1(
        texto=texto,
        faixa_taxa=faixa,  # type: ignore[arg-type]
        modificadores_aplicados=[],
        agrupador_principal_citado=None,
    )


def _construir_config_aplicada_v1(
    config: Dict[str, Any],
    caso_logico: CasoLogicoV1,
    contagem: Dict[ClassificacaoRegistroV1, int],
    motor_result: MotorResult,
) -> ConfigAplicadaV1:
    """Reflexo declarativo da configuração."""
    eps_config = config.get("epsilon_por_unidade", DEFAULT_EPSILON_POR_UNIDADE)
    eps: Dict[UnidadeCanonica, Decimal] = {}
    for k, v in eps_config.items():
        unidade_k = k if isinstance(k, UnidadeCanonica) else UnidadeCanonica(k)
        eps[unidade_k] = Decimal(str(v))

    return ConfigAplicadaV1(
        arquivo_origem=config.get("arquivo_origem", ""),
        aba_origem=config.get("aba_origem", ""),
        arquivo_comparado=config.get("arquivo_comparado", ""),
        aba_comparado=config.get("aba_comparado", ""),
        n_arquivos=config.get("n_arquivos", 2),
        caso_logico_inferido=caso_logico,
        agrupadores_match=config["agrupadores_match"],
        campos_comparados=config["campos_comparados"],
        agrupadores_resumo_executivo=config.get("agrupadores_executivos", []),
        paleta_aplicada=config.get("paleta_aplicada", "Azul executivo"),
        epsilon_por_unidade=eps,
        defaults_sobrescritos=config.get("defaults_sobrescritos", {}),
        nulos_por_classificacao={cls: 0 for cls in ClassificacaoRegistroV1},
    )


def _etapa_8_montar_contrato(
    motor_result: MotorResult,
    config: Dict[str, Any],
    caso_logico: CasoLogicoV1,
    registros: List[RegistroConciliadoV1],
    cobertura: Optional[CoberturaV1],
    valor_por_campo: List[ValorPorCampoV1],
    pontes: List[PonteCampoV1],
    status_ponte: StatusPonteV1,
    resumo_agrupador: Optional[List[LinhaResumoAgrupadorV1]],
    sintese: SinteseDiagnosticoV1,
    warnings_emitidos: List[WarningV1],
    bloqueios_escapados: List[BloqueioOperacional],
    diag: TDIAG,
    df_origem: pd.DataFrame,
    df_comparado: pd.DataFrame,
) -> ConciliacaoV1Result:
    """Etapa 8 · monta ConciliacaoV1Result com ordenação canônica (Q3) e invariantes."""
    # Ordenação canônica Q3
    registros_ordenados = sorted(
        registros,
        key=lambda r: (ORDEM_CLASSIFICACAO[r.classificacao_estrutural], r.chave_consolidada),
    )

    # Contagem · 6 chaves preservadas (zerados explícitos)
    contagem: Dict[ClassificacaoRegistroV1, int] = {cls: 0 for cls in ClassificacaoRegistroV1}
    for r in registros_ordenados:
        contagem[r.classificacao_estrutural] = contagem.get(r.classificacao_estrutural, 0) + 1

    # ConciliacaoRealizadaV1
    n_origem = len(df_origem) if caso_logico == CasoLogicoV1.ABAS_DISTINTAS else len(df_origem)
    n_comparado = len(df_comparado) if caso_logico == CasoLogicoV1.ABAS_DISTINTAS else len(df_origem)
    n_pares_matched = sum(
        1 for r in registros_ordenados
        if r.classificacao_estrutural in (
            ClassificacaoRegistroV1.CONCILIADO, ClassificacaoRegistroV1.DIVERGENTE_VALOR,
        )
    )
    if caso_logico == CasoLogicoV1.MESMA_ABA_EM_COLUNAS:
        n_processados = len(df_origem)
    else:
        n_processados = n_origem + n_comparado - n_pares_matched

    origem_ux = config.get("origem_ux", "Origem")
    comparado_ux = config.get("comparado_ux", "Comparado")
    rotulo_amig = (origem_ux != "Origem") and (comparado_ux != "Comparado")

    cr = ConciliacaoRealizadaV1(
        n_arquivos=config.get("n_arquivos", 2),
        arquivo_origem=config.get("arquivo_origem", ""),
        aba_origem=config.get("aba_origem", ""),
        arquivo_comparado=config.get("arquivo_comparado", ""),
        aba_comparado=config.get("aba_comparado", ""),
        caso_logico_inferido=caso_logico,
        origem_ux=origem_ux,
        comparado_ux=comparado_ux,
        rotulo_amigavel_declarado=rotulo_amig,
        agrupadores_match=config["agrupadores_match"],
        campos_comparados=config["campos_comparados"],
        agrupadores_resumo_executivo=config.get("agrupadores_executivos", []),
        n_registros_origem=n_origem,
        n_registros_comparado=n_comparado,
        n_processados=n_processados,
    )

    # Resumo Executivo (Fundação) + V1-específico
    resumo_padrao = _construir_resumo_executivo_padrao(
        motor_result, config, contagem, cobertura, valor_por_campo, status_ponte,
        sintese, warnings_emitidos, caso_logico, n_origem, n_comparado,
    )
    leitura_qualitativa_v1 = _construir_leitura_qualitativa_v1(contagem, caso_logico, config)
    config_aplicada = _construir_config_aplicada_v1(config, caso_logico, contagem, motor_result)

    coracao = CoracaoVisualRef(
        nome_aba="Mapa de Conciliação",
        tipo="TABELA_HEATMAP",
        capabilities_requeridas=["formatacao_condicional"],
    )

    # Base analítica · amostra para auditoria
    base_analitica_rows = []
    for r in registros_ordenados[:200]:
        base_analitica_rows.append({
            "chave_consolidada": r.chave_consolidada,
            "classificacao": r.classificacao_estrutural.value,
            "diferenca_total": float(r.diferenca_total_registro) if r.diferenca_total_registro is not None else None,
        })
    base_analitica = pd.DataFrame(base_analitica_rows) if base_analitica_rows else pd.DataFrame(
        [{"chave_consolidada": "", "classificacao": "", "diferenca_total": None}]
    )

    return ConciliacaoV1Result(
        config_usada={
            "agrupadores": [a.rotulo_analitico for a in config["agrupadores_match"]],
            "campos_comparados": [c.nome_analitico for c in config["campos_comparados"]],
            "caso_logico_inferido": caso_logico.value,
            "epsilon_por_unidade": {k.value: str(v) for k, v in config_aplicada.epsilon_por_unidade.items()},
        },
        motor_result_meta=_make_motor_meta(motor_result),
        base_analitica=base_analitica,
        resumo_executivo=resumo_padrao,
        coracao_visual=coracao,
        bloqueios_disparados=bloqueios_escapados,
        warnings=[],  # warnings da Fundação ficam vazios; herdados são em warnings_emitidos
        diagnostico=diag.consolidar(),
        conciliacao_realizada=cr,
        classificacao_por_registro=registros_ordenados,
        contagem_por_classificacao=contagem,
        cobertura=cobertura,
        valor_por_campo=valor_por_campo,
        resumo_por_agrupador_executivo=resumo_agrupador,
        pontes=pontes,
        status_ponte_geral=status_ponte,
        sintese_diagnostico=sintese,
        config_aplicada=config_aplicada,
        leitura_qualitativa=leitura_qualitativa_v1,
        warnings_emitidos=warnings_emitidos,
        modelo_aplicado=None,
    )


# ---------------------------------------------------------------------------
# Função pública principal (entry-point do motor V1)
# ---------------------------------------------------------------------------


def executar_v1(
    motor_result: MotorResult,
    config: Dict[str, Any],
) -> ConciliacaoV1Result:
    """Pipeline canônico V1 · 8 etapas · 2 ramos por caso lógico (D-213) · S-V1 v2 §2.1.

    Determinístico (C.1) · zero invenção de comportamento (C.3) · nada silencioso (C.2).

    Em casos 1/2/4 (D-213): motor_result.modo_upload == "DUAL" · usa origem_comparado_map.
    Em caso 3 (D-213): motor_result.modo_upload == "SIMPLES" · particiona df por colunas.

    Args:
        motor_result: MotorResult vindo do motor_base. Em V1 pode ser SIMPLES ou DUAL.
        config: Dict com chaves canônicas:
            - "agrupadores_match": List[AgrupadorMatchV1] (1-5)
            - "campos_comparados": List[CampoComparadoV1] (1-10)
            - "agrupadores_executivos": List[str] (0-5)
            - "epsilon_por_unidade": Dict[UnidadeCanonica, Decimal] (default DEFAULT_EPSILON_POR_UNIDADE)
            - "thresholds": Dict[str, Any] (chave_nulos_max · volume_max · concentracao_*)
            - "origem_ux": str (default "Origem")
            - "comparado_ux": str (default "Comparado")
            - "arquivo_origem": str
            - "arquivo_comparado": str
            - "aba_origem": str
            - "aba_comparado": str
            - "n_arquivos": Literal[1, 2]
            - "paleta_aplicada": str (default "Azul executivo")
            - "modelo_aplicado": Optional[Dict] (T-MODELO referência)

    Returns:
        ConciliacaoV1Result com pipeline completo executado.

    Raises:
        ValueError: bloqueios não-escapáveis com prefixo 'B-V1-...' na mensagem.
    """
    try:
        return _executar_v1_interno(motor_result, config)
    except ValueError:
        # Bloqueios B-V1-* já são ValueError com prefixo · re-raise direto
        raise
    except Exception as e:  # noqa: BLE001
        # B-V1-MOTOR-FALHOU · catch-all para exceptions inesperadas (S-V1 §2.5)
        raise ValueError(
            f"B-V1-MOTOR-FALHOU: erro inesperado no processamento · {type(e).__name__}: {e} · "
            f"entre em contato com o suporte"
        ) from e


def _executar_v1_interno(
    motor_result: MotorResult,
    config: Dict[str, Any],
) -> ConciliacaoV1Result:
    """Pipeline interno · sem o wrapper catch-all B-V1-MOTOR-FALHOU."""
    # Inicializa coletor de diagnóstico
    diag = TDIAG("V1")

    # Propaga column_meta para validação cruzada
    if motor_result is not None and motor_result.column_meta:
        config = {**config, "_column_meta": motor_result.column_meta}

    # Etapa 1 · Leitura
    df_origem, df_comparado = _etapa_1_leitura(motor_result, config)

    # Etapa 3 (antes de Etapa 2 porque Etapa 2 precisa do caso lógico)
    caso_logico = _etapa_3_inferir_caso_logico(df_origem, df_comparado, config)

    # Etapa 2 · Validação dos apontamentos
    bloqueios_escapados, warnings_validacao = _etapa_2_validar_apontamentos(
        df_origem, df_comparado, config, caso_logico
    )
    for b in bloqueios_escapados:
        diag.registrar_bloqueio_escapado(b)

    # Etapa 4 · Match · ramifica
    if caso_logico == CasoLogicoV1.ABAS_DISTINTAS:
        pares = _etapa_4a_match_abas_distintas(df_origem, df_comparado, config)
    else:
        pares = _etapa_4b_pareamento_linha_a_linha(df_origem, config)

    # Etapa 5 · Cálculo de diferenças (registros parciais)
    registros_parciais = _etapa_5_calcular_diferencas(
        pares, df_origem, df_comparado, config, caso_logico
    )

    # Etapa 6 · Classificação agregada
    registros = _etapa_6_classificar_agregada(
        registros_parciais, pares, caso_logico, config
    )

    # Etapa 7 · Agregações
    cobertura, valor_por_campo, pontes, status_ponte, resumo_agrup, sintese, warnings_pipeline = (
        _etapa_7_agregacoes(registros, pares, df_origem, df_comparado, caso_logico, config)
    )

    # Consolida warnings: validação + pipeline + herdados do motor
    warnings_emitidos: List[WarningV1] = []
    warnings_emitidos.extend(warnings_validacao)
    warnings_emitidos.extend(warnings_pipeline)
    if motor_result is not None and motor_result.warnings:
        warnings_emitidos.extend(_flatten_warnings(motor_result.warnings))

    # Etapa 8 · Montar contrato
    return _etapa_8_montar_contrato(
        motor_result=motor_result,
        config=config,
        caso_logico=caso_logico,
        registros=registros,
        cobertura=cobertura,
        valor_por_campo=valor_por_campo,
        pontes=pontes,
        status_ponte=status_ponte,
        resumo_agrupador=resumo_agrup,
        sintese=sintese,
        warnings_emitidos=warnings_emitidos,
        bloqueios_escapados=bloqueios_escapados,
        diag=diag,
        df_origem=df_origem,
        df_comparado=df_comparado,
    )
