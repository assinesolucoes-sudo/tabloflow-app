"""
contratos.py — Contratos de dados da Fundação TabloFlow · Fase 1
D-130: receptividade a IA declarada · Pydantic v2 · JSON-compatível · enums string

Contratos canônicos:
  UploadResult · MotorResult · VNResultBase · DiagnosticoVN
Contratos compartilhados:
  BloqueioOperacional · WarningEstrutural · ColumnMeta · AjusteMotor ·
  DecisaoUsuario · IntegridadeEstrutural
Contratos de motor:
  MotorConfig · ConfigExportacao
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field, field_serializer, model_validator


# ---------------------------------------------------------------------------
# Enums (str para serialização JSON-compatível · D-130)
# ---------------------------------------------------------------------------

class TipoEstruturalEnum(str, Enum):
    """D-113 · D-133 · 5 valores canônicos de tipo estrutural de coluna."""
    CATEGORICO_ELEGIVEL = "CATEGORICO_ELEGIVEL"
    NUMERICO_CONTINUO = "NUMERICO_CONTINUO"
    TEMPORAL = "TEMPORAL"
    BOOLEANO = "BOOLEANO"
    VAZIO_OU_AMBIGUO = "VAZIO_OU_AMBIGUO"


class TipoTecnicoEnum(str, Enum):
    """Tipo técnico inferido de pandas · 7 valores."""
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    BOOL = "bool"
    DATETIME = "datetime"
    OBJECT = "object"
    MIXED = "mixed"


class TipoSemanticoEnum(str, Enum):
    """Tipo semântico derivado do tipo técnico · 6 valores."""
    NUMERIC = "numeric"
    BOOLEAN = "boolean"
    TEMPORAL = "temporal"
    TEXTUAL = "textual"
    CATEGORICO_BAIXA_CARD = "categorico_baixa_card"
    MISTO = "misto"


class PadraoCronologicoEnum(str, Enum):
    """D-026 · 7 padrões cronológicos reconhecidos pt-BR/pt-EN."""
    ISO_DATE = "ISO_DATE"
    PT_BR_DATE = "PT_BR_DATE"
    MONTH_NAME_PT = "MONTH_NAME_PT"
    MONTH_NAME_EN = "MONTH_NAME_EN"
    COMPACT_MONTHYEAR = "COMPACT_MONTHYEAR"
    YEAR_ONLY = "YEAR_ONLY"
    Q_TRIMESTRE = "Q_TRIMESTRE"


class CategoriaWarning(str, Enum):
    """6 categorias canônicas de warning · vocabulário fechado · D-017."""
    INFORMATIVO = "informativo"
    AJUSTE_LEVE = "ajuste_leve"
    ALERTA_ESTRUTURAL_LEVE = "alerta_estrutural_leve"
    ALERTA_ESTRUTURAL = "alerta_estrutural"
    DECISAO_USUARIO = "decisao_usuario"
    ESCAPE_ACIONADO = "escape_acionado"


# ---------------------------------------------------------------------------
# Contratos compartilhados base
# ---------------------------------------------------------------------------

class WarningEstrutural(BaseModel):
    model_config = ConfigDict(use_enum_values=False)

    codigo: str = Field(..., description="Código do warning · padrão W-VN-DESCRITOR · ex: 'W-B01'")
    categoria: CategoriaWarning = Field(..., description="Categoria · vocabulário fechado de 6 valores")
    microcopy: str = Field(..., description="Texto descritivo visível ao usuário")
    contexto: Dict[str, Any] = Field(
        default_factory=dict,
        description="Campos relacionados · contagens · valores observados"
    )
    linha_referenciada: Optional[int] = Field(
        None,
        description="Índice da linha da base onde o warning foi gerado · quando aplicável"
    )


class BloqueioOperacional(BaseModel):
    """D-134 · contrato único compartilhado por todas as visões e motores."""
    model_config = ConfigDict(use_enum_values=False)

    codigo: str = Field(
        ...,
        description="Padrão B-VN-DESCRITOR · ex: 'B-V6-EIXO-NUMERICO-CONTINUO' · 'B-B-BASE-MUITO-GRANDE'"
    )
    condicao_disparo: str = Field(..., description="Microcopy descritivo · visível ao usuário")
    escapavel: bool = Field(..., description="True se o usuário pode forçar execução com warning permanente")
    escape_acionado: Optional[bool] = Field(
        None,
        description="Preenchido quando escapavel=True e usuário decidiu escapar"
    )
    warning_pos_escape: Optional[str] = Field(
        None,
        description="Código do warning permanente emitido quando escape é acionado"
    )
    contexto_disparo: Dict[str, Any] = Field(
        default_factory=dict,
        description="Campos relacionados · contagens · valores observados no disparo"
    )


class AjusteMotor(BaseModel):
    tipo_ajuste: str = Field(
        ...,
        description="'INTERVALO_AJUSTADO_INICIO' · 'LINHA_EXCLUIDA_NULO' · 'COLUNA_RENOMEADA' · etc."
    )
    linhas_afetadas: int = Field(..., description="Número de linhas afetadas pelo ajuste")
    descricao: str = Field(..., description="Descrição textual do ajuste aplicado · C.2 nada silencioso")


class DecisaoUsuario(BaseModel):
    contexto: str = Field(
        ...,
        description="'threshold_dominante_editado' · 'escape_cardinalidade_acionado' · etc."
    )
    valor_default: Any = Field(..., description="Valor padrão antes da edição do usuário")
    valor_escolhido: Any = Field(..., description="Valor efetivamente aplicado pelo usuário")
    justificativa_opcional: Optional[str] = Field(
        None,
        description="Justificativa opcional fornecida pelo usuário"
    )


class IntegridadeEstrutural(BaseModel):
    total_linhas_base_original: int = Field(..., description="Total de linhas antes de qualquer processamento")
    total_linhas_processadas: int = Field(..., description="Total de linhas após exclusões de parse")
    total_linhas_excluidas: int = Field(..., description="Total de linhas excluídas durante o processamento")
    motivo_exclusao_por_categoria: Dict[str, int] = Field(
        default_factory=dict,
        description="Mapeamento motivo → contagem de linhas excluídas por esse motivo"
    )


# ---------------------------------------------------------------------------
# ColumnMeta · A.3
# ---------------------------------------------------------------------------

class ColumnMeta(BaseModel):
    """Metadados estruturais de coluna · produzido pelo motor_base para toda coluna · D-133."""
    model_config = ConfigDict(use_enum_values=False)

    nome: str = Field(..., description="Nome da coluna na base processada")
    tipo_tecnico: TipoTecnicoEnum = Field(
        ...,
        description="Tipo técnico inferido: int · float · string · bool · datetime · object · mixed"
    )
    tipo_semantico: TipoSemanticoEnum = Field(
        ...,
        description="Tipo semântico: numeric · boolean · temporal · textual · categorico_baixa_card · misto"
    )
    tipo_estrutural: TipoEstruturalEnum = Field(
        ...,
        description="D-113 · D-133 · sempre computado pelo motor_base sobre coluna completa · 5 valores"
    )
    subtipo_id_detectado: bool = Field(
        ...,
        description="D-103 · sempre computado em int/string com alta cardinalidade · heurística B.4"
    )
    null_count: int = Field(..., description="Quantidade de valores nulos · inclui null-strings normalizados")
    cardinalidade: int = Field(..., description="Quantidade de valores únicos não-nulos na coluna")
    eh_candidato_categorico: bool = Field(
        ...,
        description="True se a coluna tem cardinalidade adequada para uso como agrupador categórico"
    )
    padrao_cronologico_detectado: Optional[PadraoCronologicoEnum] = Field(
        None,
        description="D-026 · 7 padrões reconhecidos · None se threshold < 50% · TEMPORAL se >= 80%"
    )
    ordem_insercao: int = Field(
        ...,
        description="Índice posicional da coluna na base original · começa em 0 · auditoria"
    )
    tipo_campo: Optional[Literal[
        "NUMERICO_ADITIVO", "NUMERICO_RELATIVO", "NUMERICO_NAO_ADITIVO", "ESTADO_SITUACAO"
    ]] = Field(
        None,
        description=(
            "Camada analítica · 4 tipos canônicos D-025 · None quando não inferível · "
            "promovido para Fundação em D-202 · motor_base atual NÃO infere · "
            "preenchido quando declarado via UI ou heurística futura (P-34 deferido)"
        ),
    )
    unidade: Optional[Literal[
        "MONETARIO_BRL",
        "PERCENTUAL",
        "QUANTIDADE",
        "TEMPO_DIAS",
        "TEMPO_HORAS",
        "MULTIPLICADOR",
        "RAZAO",
        "ADIMENSIONAL",
    ]] = Field(
        None,
        description=(
            "Unidade canônica do campo · D-190 C.D8 · None quando não inferível · "
            "promovido para Fundação em D-202 · motor_base atual NÃO infere · "
            "preenchido quando declarado via UI ou heurística futura (P-34 deferido)"
        ),
    )


# ---------------------------------------------------------------------------
# ArquivoInfo e UploadResult · A.2
# ---------------------------------------------------------------------------

class ArquivoInfo(BaseModel):
    """Metadados e bytes de um arquivo carregado · parte de UploadResult."""
    model_config = ConfigDict(use_enum_values=False)

    caminho_logico: Literal["origem", "comparado", "unico"] = Field(
        ...,
        description="Papel lógico do arquivo · T-DUAL: 'origem' ou 'comparado' · simples: 'unico'"
    )
    nome_arquivo: str = Field(..., description="Nome do arquivo físico incluindo extensão")
    arquivo_bytes: bytes = Field(
        ...,
        description="D-007 · conteúdo completo do arquivo preservado em memória para motor_base"
    )
    abas_disponiveis: List[str] = Field(
        ...,
        description="Lista de abas disponíveis · apenas Excel · vazia para CSV/TSV"
    )
    aba_selecionada: str = Field(
        ...,
        description="Nome da aba selecionada · string vazia para CSV/TSV"
    )
    formato: Literal["xlsx", "xlsm", "csv", "tsv"] = Field(
        ...,
        description="Formato do arquivo detectado pela extensão"
    )
    preview: Dict[str, List] = Field(
        ...,
        description="5 linhas como dict column→[values] · orientação 'list' · auditoria rápida"
    )
    encoding_detectado: Optional[str] = Field(
        None,
        description="Encoding detectado · relevante para CSV/TSV"
    )
    separador_csv: Optional[str] = Field(
        None,
        description="Separador inferido via csv.Sniffer · apenas CSV/TSV"
    )


class UploadResult(BaseModel):
    """Resultado do motor_upload · consumido pelo motor_base · A.2."""
    model_config = ConfigDict(use_enum_values=False)

    file_name: str = Field(..., description="Nome do arquivo principal (primeiro arquivo em modo DUAL)")
    modo_upload: Literal["SIMPLES", "DUAL"] = Field(
        ...,
        description="T-DUAL · V1/V11 = DUAL · demais = SIMPLES · declarado pelo chamador · motor não infere"
    )
    arquivo_unico: Optional[ArquivoInfo] = Field(
        None,
        description="Preenchido em modo SIMPLES · None em DUAL"
    )
    arquivos_dual: Optional[List[ArquivoInfo]] = Field(
        None,
        description="2 entradas em modo DUAL · [origem, comparado] · None em SIMPLES"
    )
    timestamp_upload: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp da operação de upload"
    )
    warnings: List[WarningEstrutural] = Field(
        default_factory=list,
        description="Warnings emitidos · W-U-ENCODING-FALLBACK · W-U-SEP-FALLBACK · W-U-ARQUIVO-VAZIO"
    )


# ---------------------------------------------------------------------------
# MotorResult · A.3
# ---------------------------------------------------------------------------

class MotorResult(BaseModel):
    """Resultado do motor_base · consumido por todas as 11 visões · A.3."""
    model_config = ConfigDict(arbitrary_types_allowed=True, use_enum_values=False)

    df: pd.DataFrame = Field(
        ...,
        description="DataFrame completo processado · D-007 · tipo arbitrário pandas"
    )
    column_meta: Dict[str, ColumnMeta] = Field(
        ...,
        description="Metadados estruturais por coluna · chave = nome da coluna · D-133 sempre computado"
    )
    modo_upload: Literal["SIMPLES", "DUAL"] = Field(
        ...,
        description="Modo de upload que originou este MotorResult"
    )
    origem_comparado_map: Optional[Dict[int, Literal["origem", "comparado"]]] = Field(
        None,
        description="Quando DUAL · mapeia índice de linha ao caminho_logico · None em SIMPLES"
    )
    total_linhas_originais: int = Field(
        ...,
        description="Total de linhas no(s) arquivo(s) original(is) antes de processamento"
    )
    total_linhas_processadas: int = Field(
        ...,
        description="Total de linhas no DataFrame após exclusões de parse"
    )
    timestamp_processamento: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp da execução do motor_base"
    )
    warnings: List[WarningEstrutural] = Field(
        default_factory=list,
        description="Warnings emitidos pelo motor_base · W-B01 · W-B-MISTO · W-B-QUASE-VAZIO · etc."
    )
    bloqueios: List[BloqueioOperacional] = Field(
        default_factory=list,
        description="Bloqueios operacionais emitidos · B-B-BASE-MUITO-GRANDE · B-CARD-EXCESSIVA · etc."
    )

    @field_serializer("df")
    def _serializar_df(self, df: pd.DataFrame) -> List[Dict]:
        """Serialização segura do DataFrame · D-130 · apenas amostra de 5 linhas."""
        return df.head(5).to_dict(orient="records")

    @field_serializer("timestamp_processamento")
    def _serializar_timestamp(self, ts: datetime) -> str:
        return ts.isoformat()

    def _resumir_estatisticas(self) -> Dict[str, Any]:
        """Sumário estatístico por coluna · sem o DataFrame bruto."""
        resumo: Dict[str, Any] = {}
        for col_name, meta in self.column_meta.items():
            col_resumo: Dict[str, Any] = {
                "tipo_estrutural": meta.tipo_estrutural.value,
                "null_count": meta.null_count,
                "cardinalidade": meta.cardinalidade,
                "subtipo_id_detectado": meta.subtipo_id_detectado,
            }
            if col_name in self.df.columns:
                series = self.df[col_name].dropna()
                if meta.tipo_tecnico in (TipoTecnicoEnum.INT, TipoTecnicoEnum.FLOAT) and len(series) > 0:
                    try:
                        col_resumo["min"] = float(series.min())
                        col_resumo["max"] = float(series.max())
                        col_resumo["media"] = float(series.mean())
                    except (TypeError, ValueError):
                        pass
            resumo[col_name] = col_resumo
        return resumo

    def para_contexto_ia(self) -> Dict[str, Any]:
        """D-130 · subset otimizado para contexto IA · sem df bruto · com sumário estatístico."""
        return {
            "column_meta": {k: v.model_dump() for k, v in self.column_meta.items()},
            "total_linhas": self.total_linhas_processadas,
            "modo_upload": self.modo_upload,
            "amostra_5_linhas": self.df.head(5).to_dict(orient="records"),
            "estatisticas_sumarias": self._resumir_estatisticas(),
            "warnings": [w.model_dump() for w in self.warnings],
        }


# ---------------------------------------------------------------------------
# DiagnosticoVN · A.6
# ---------------------------------------------------------------------------

class DiagnosticoVN(BaseModel):
    """Coletor unificado de diagnóstico · alimenta aba Diagnóstico via T-DIAG · D-017."""
    model_config = ConfigDict(use_enum_values=False)

    ajustes_aplicados: List[AjusteMotor] = Field(
        default_factory=list,
        description="Seção 1 · ajustes aplicados pelo motor sem intervenção do usuário · C.2"
    )
    warnings_por_categoria: Dict[str, List[WarningEstrutural]] = Field(
        default_factory=dict,
        description="Seção 2 · warnings agrupados por CategoriaWarning.value"
    )
    decisoes_usuario: List[DecisaoUsuario] = Field(
        default_factory=list,
        description="Seção 3 · decisões do usuário (defaults editados · thresholds · escapes)"
    )
    bloqueios_informativos: List[BloqueioOperacional] = Field(
        default_factory=list,
        description="Seção 4 · bloqueios escapados registrados para rastreabilidade"
    )
    integridade: Optional[IntegridadeEstrutural] = Field(
        None,
        description="Seção 5 · integridade estrutural · total de linhas · exclusões por categoria"
    )


# ---------------------------------------------------------------------------
# VNResultBase · A.4
# ---------------------------------------------------------------------------

class MotorResultMeta(BaseModel):
    """Subset de metadados do MotorResult para consumo nos VNResult · sem o DataFrame."""
    model_config = ConfigDict(use_enum_values=False)

    total_linhas_originais: int = Field(..., description="Total de linhas antes do processamento")
    total_linhas_processadas: int = Field(..., description="Total de linhas após o processamento")
    modo_upload: Literal["SIMPLES", "DUAL"] = Field(..., description="Modo de upload utilizado")
    timestamp_processamento: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp do processamento do motor_base"
    )
    warnings_motor: List[WarningEstrutural] = Field(
        default_factory=list,
        description="Warnings emitidos pelo motor_base"
    )


class CabecalhoExecucao(BaseModel):
    visao: str = Field(..., description="Identificador da visão · ex: 'V2'")
    data_execucao: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp da execução da visão"
    )
    modo_upload: Literal["SIMPLES", "DUAL"] = Field(..., description="Modo de upload")
    agrupadores: List[str] = Field(default_factory=list, description="Agrupadores configurados")
    medida_principal: Optional[str] = Field(None, description="Campo de medida principal")


class LeituraQualitativa(BaseModel):
    classificacao_ativa: str = Field(..., description="Classificação qualitativa do conjunto analisado")
    thresholds_usados: Dict[str, float] = Field(
        default_factory=dict,
        description="TED D-123 · thresholds editados ou default aplicados"
    )
    alguma_leitura_alterada_por_edicao: bool = Field(
        ...,
        description="True se algum threshold foi editado alterando a leitura qualitativa"
    )


class QualidadeEstrutural(BaseModel):
    total_warnings: int = Field(..., description="Contagem total de warnings emitidos")
    warnings_por_categoria: Dict[str, int] = Field(
        default_factory=dict,
        description="Contagem de warnings por categoria"
    )
    ajustes_aplicados: int = Field(..., description="Contagem de ajustes aplicados pelo motor")
    tem_bloqueios_escapados: bool = Field(..., description="True se algum bloqueio foi escapado")


class ResumoExecutivoPadrao(BaseModel):
    """D-125 · 6 blocos fixos · adaptações via D-073 permitidas preservando a espinha."""
    model_config = ConfigDict(use_enum_values=False)

    bloco_1_cabecalho: CabecalhoExecucao = Field(
        ...,
        description="Bloco 1 · metadados da execução: visão · data · modo · agrupadores · medida"
    )
    bloco_2_numeros_ancora: Dict[str, Union[float, int, str]] = Field(
        ...,
        description="Bloco 2 · contagens e totais estruturais da unidade analítica da visão"
    )
    bloco_3_distribuicao: Dict[str, Any] = Field(
        ...,
        description="Bloco 3 · distribuição do conteúdo analítico pela taxonomia da visão"
    )
    bloco_4_elementos_destacados: Dict[str, Any] = Field(
        ...,
        description="Bloco 4 · elementos identificados como dignos de atenção pelo motor"
    )
    bloco_5_leitura_qualitativa: LeituraQualitativa = Field(
        ...,
        description="Bloco 5 · classificação qualitativa com thresholds editáveis TED"
    )
    bloco_6_qualidade_estrutural: QualidadeEstrutural = Field(
        ...,
        description="Bloco 6 · warnings · ajustes do motor · integridade do dado · BAD C.D3"
    )


class CoracaoVisualRef(BaseModel):
    """D-126 · referência declarativa ao Coração Visual · exportacao.py implementa."""
    nome_aba: str = Field(..., description="Nome da aba que é o Coração Visual da visão")
    tipo: Literal[
        "BARRAS", "BARRAS_LINHA", "COLUMN_EMPILHADO_100",
        "MATRIZ_COLORIDA", "HISTOGRAMA", "TABELA_HEATMAP"
    ] = Field(..., description="Tipo do visual do Coração Visual")
    capabilities_requeridas: List[str] = Field(
        default_factory=list,
        description="Capabilities de exportação requeridas · ex: 'formatacao_condicional'"
    )


class VNResultBase(BaseModel):
    """
    Classe base abstrata para resultados de visões analíticas · D-130.
    Toda V{N}Result herda desta classe e adiciona campos específicos.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True, use_enum_values=False)

    visao_id: Literal["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11"] = Field(
        ...,
        description="Identificador da visão que produziu este resultado"
    )
    config_usada: Dict[str, Any] = Field(
        ...,
        description="Config persistível · T-MODELO · TED D-123 · serializada junto ao resultado"
    )
    motor_result_meta: MotorResultMeta = Field(
        ...,
        description="Subset de metadados do MotorResult · sem o DataFrame bruto"
    )
    timestamp_execucao: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp da execução da visão"
    )

    base_analitica: pd.DataFrame = Field(
        ...,
        description="Padrão BAD · D-124 · 1 linha por unidade analítica com classificações derivadas"
    )
    resumo_executivo: ResumoExecutivoPadrao = Field(
        ...,
        description="6 blocos fixos · D-125 · adaptações via D-073 preservando a espinha"
    )
    coracao_visual: CoracaoVisualRef = Field(
        ...,
        description="Referência declarativa · D-126 · exportacao.py implementa"
    )

    bloqueios_disparados: List[BloqueioOperacional] = Field(
        default_factory=list,
        description="Padrão MBO · D-127 · contrato único D-134 · matrix declarada na Spec S-VN"
    )
    warnings: List[WarningEstrutural] = Field(
        default_factory=list,
        description="Warnings emitidos durante a execução da visão"
    )
    diagnostico: DiagnosticoVN = Field(
        ...,
        description="T-DIAG · alimenta aba Diagnóstico · sempre última aba · D-017"
    )

    def para_contexto_ia(self) -> Dict[str, Any]:
        """D-130 · Papel B · subset para leitura em linguagem natural do resultado pela IA."""
        return {
            "visao_id": self.visao_id,
            "config_usada": self.config_usada,
            "resumo_executivo": self.resumo_executivo.model_dump(),
            "coracao_visual": self.coracao_visual.model_dump(),
            "bloqueios_escapados": [
                b.model_dump() for b in self.bloqueios_disparados if b.escape_acionado
            ],
            "warnings": [w.model_dump() for w in self.warnings],
            "amostra_base_analitica": self.base_analitica.head(20).to_dict(orient="records"),
        }


# ---------------------------------------------------------------------------
# ContratoComparativo · Família A · D-202
# ---------------------------------------------------------------------------

class ContratoComparativo(BaseModel):
    """Configuração analítica genérica da Família A (V1/V2/V11) · D-202.

    Promovido de `visoes.visao_v2.ComparacaoV2` para `contratos.py` em D-202.
    V2 (e futuras V1/V11) herdam desta classe · podendo estender se necessário.
    """
    model_config = ConfigDict(use_enum_values=False)

    estrutura_entrada: Literal["POR_COLUNAS", "POR_LINHAS"] = Field(
        ...,
        description="POR_COLUNAS quando Origem e Comparado são colunas · POR_LINHAS quando são valores de coluna discriminadora",
    )
    origem_rotulo_tecnico: str = Field(
        ...,
        description="Nome da coluna (POR_COLUNAS) ou valor da coluna discriminadora (POR_LINHAS) · Origem",
    )
    comparado_rotulo_tecnico: str = Field(
        ...,
        description="Nome da coluna (POR_COLUNAS) ou valor da coluna discriminadora (POR_LINHAS) · Comparado",
    )
    origem_rotulo_ux: str = Field(
        ...,
        description="Rótulo amigável editável · exibido como 'Comparar de: {ux}'",
    )
    comparado_rotulo_ux: str = Field(
        ...,
        description="Rótulo amigável editável · exibido como 'Comparar com: {ux}'",
    )
    coluna_discriminadora: Optional[str] = Field(
        None,
        description="Nome da coluna discriminadora · obrigatório quando estrutura_entrada=POR_LINHAS · None em POR_COLUNAS",
    )
    modo_4_ativado: bool = Field(
        False,
        description="True quando coluna_discriminadora tem >2 valores únicos e usuário escolheu 2 · D-026",
    )
    estados_nao_escolhidos: List[str] = Field(
        default_factory=list,
        description="Valores da coluna discriminadora excluídos quando modo_4_ativado · registrados no Diagnóstico",
    )
    campo_analisado: str = Field(..., description="Nome do campo sobre o qual Δ e Δ% são calculados")
    tipo_campo: Literal[
        "NUMERICO_ADITIVO", "NUMERICO_RELATIVO", "NUMERICO_NAO_ADITIVO", "ESTADO_SITUACAO"
    ] = Field(..., description="4 tipos canônicos · D-025")
    semantica_campo: Literal["MAIOR_MELHOR", "MENOR_MELHOR", "NEUTRO"] = Field(
        ...,
        description="Semântica via T-SEMA · determina classificação Positivo/Negativo/Neutro",
    )
    unidade: Literal[
        "MONETARIO_BRL",
        "PERCENTUAL",
        "QUANTIDADE",
        "TEMPO_DIAS",
        "TEMPO_HORAS",
        "MULTIPLICADOR",
        "RAZAO",
        "ADIMENSIONAL",
    ] = Field(
        "MONETARIO_BRL",
        description=(
            "Unidade canônica do campo · determina formatação e rótulos das "
            "colunas Diferença e Variação no Excel · D-190 · C.D8"
        ),
    )
    agrupador_destacado: Optional[str] = Field(
        None,
        description=(
            "Agrupador a destacar no bloco 'Onde se concentra' do Resumo "
            "Executivo · default = primeiro de `agrupadores` · D-192 / E3b"
        ),
    )
    regra_agregacao: Literal["SOMA", "MEDIA", "MAXIMO", "MINIMO", "CONTAGEM"] = Field(
        "SOMA",
        description="Regra T-AGRUPA · default SOMA para NUMERICO_ADITIVO · configurável",
    )
    metodo_consolidacao_relativo: Optional[Literal[
        "MEDIA_SIMPLES", "MEDIA_PONDERADA", "NAO_CONSOLIDAR"
    ]] = Field(
        None,
        description="Obrigatório para NUMERICO_RELATIVO e NUMERICO_NAO_ADITIVO · D-024 · None para ADITIVO e ESTADO_SITUACAO",
    )
    campo_peso: Optional[str] = Field(
        None,
        description="Nome do campo de peso · obrigatório quando metodo_consolidacao_relativo=MEDIA_PONDERADA",
    )

    @model_validator(mode="after")
    def _validar_consistencia(self) -> "ContratoComparativo":
        if self.tipo_campo in ("NUMERICO_RELATIVO", "NUMERICO_NAO_ADITIVO"):
            if self.metodo_consolidacao_relativo is None:
                raise ValueError(
                    f"metodo_consolidacao_relativo obrigatório para tipo_campo={self.tipo_campo}"
                )
        elif self.tipo_campo in ("NUMERICO_ADITIVO", "ESTADO_SITUACAO"):
            if self.metodo_consolidacao_relativo is not None:
                raise ValueError(
                    f"metodo_consolidacao_relativo deve ser None para tipo_campo={self.tipo_campo}"
                )
        if self.metodo_consolidacao_relativo == "MEDIA_PONDERADA" and self.campo_peso is None:
            raise ValueError("campo_peso obrigatório quando metodo_consolidacao_relativo=MEDIA_PONDERADA")
        if self.estrutura_entrada == "POR_LINHAS" and self.coluna_discriminadora is None:
            raise ValueError("coluna_discriminadora obrigatória quando estrutura_entrada=POR_LINHAS")
        return self


# ---------------------------------------------------------------------------
# MotorConfig
# ---------------------------------------------------------------------------

class MotorConfig(BaseModel):
    """Configuração operacional dos motores · parâmetros globais com defaults da Fundação."""
    model_config = ConfigDict(use_enum_values=False)

    limite_linhas_aviso: int = Field(
        500_000,
        description="Linhas acima deste limite geram W-B-BASE-GRANDE · impacto de desempenho esperado"
    )
    limite_linhas_bloqueio: int = Field(
        2_000_000,
        description="Limite absoluto · acima gera B-B-BASE-MUITO-GRANDE sem escape · C.5"
    )
    max_cardinalidade_categorico: int = Field(
        200,
        description="Fronteira int categórico vs contínuo · D-113 · herdada de V6 para consistência"
    )
    threshold_pct_cronologico: float = Field(
        0.80,
        description="Proporção mínima de valores casando padrão para classificar TEMPORAL · D-026"
    )
    threshold_pct_cronologico_parcial: float = Field(
        0.50,
        description="Proporção mínima para W-B-TEMPORAL-PARCIAL sem classificar TEMPORAL"
    )
    threshold_pct_id: float = Field(
        0.90,
        description="Proporção mínima de cardinalidade relativa a não-nulos para candidato ID · D-103"
    )
    threshold_pct_quase_vazio: float = Field(
        0.90,
        description="Proporção de nulos que classifica coluna como VAZIO_OU_AMBIGUO"
    )
    max_amostras_cronologico_base: int = Field(
        1_000,
        description="Tamanho mínimo da amostra · real = max(este, 10% do total) · C.5"
    )
    threshold_cardinalidade_id_string: float = Field(
        0.80,
        description="Proporção mínima de valores únicos em coluna string para candidato ID · D-103"
    )


# ---------------------------------------------------------------------------
# ConfigExportacao
# ---------------------------------------------------------------------------

class ConfigExportacao(BaseModel):
    """Configuração de exportação Excel · consumida por exportacao.py em F-EXP."""
    model_config = ConfigDict(use_enum_values=False)

    nome_arquivo_saida: Optional[str] = Field(
        None,
        description="Nome do arquivo Excel de saída · None = gerado automaticamente com timestamp"
    )
    aplicar_filtros_automaticos: bool = Field(
        True,
        description="Ativa AutoFilter em todas as abas tabulares · padrão do produto"
    )
    congelar_cabecalho: bool = Field(
        True,
        description="Congela linha de cabeçalho em abas tabulares"
    )
    aplicar_formatacao_condicional: bool = Field(
        True,
        description="Ativa formatação condicional quando capability declarada pelo Coração Visual"
    )
    largura_colunas_auto: bool = Field(
        True,
        description="Ajusta largura de colunas automaticamente baseado no conteúdo"
    )
    max_linhas_por_pagina: int = Field(
        50_000,
        description="Limite de linhas por aba · acima este limite ativa paginação"
    )
    # Campos adicionados em F-EXP (§EXP.2) · não existiam em F-MOT · adição não-quebrante
    incluir_graficos_nativos: bool = Field(
        True,
        description="Inclui gráficos openpyxl nativos · False para export rápido sem gráficos"
    )
    paginar_matrizes_grandes: bool = Field(
        True,
        description="Pagina matrizes > 30×30 em abas secundárias · CAP-PAGINACAO-MATRIZ"
    )
    paleta: str = Field(
        "azul",
        description=(
            "D-171/D-168 · Nome da paleta executiva aplicada ao Excel. "
            "Default universal 'azul'. Valores válidos: azul · cinza · "
            "verde · vinho (chaves minúsculas do catálogo F-APRESENT · "
            "D-164). Sobrescrição via C.D6 (DDU) pelo widget do app no "
            "momento da exportação. Validação efetiva em aplicar_paleta "
            "(capability 1 de F-APRESENT) · falha clara se nome inválido."
        )
    )


# ---------------------------------------------------------------------------
# ExportacaoResult · A.5 · D-130
# ---------------------------------------------------------------------------

class ExportacaoResult(BaseModel):
    """
    Resultado da exportação Excel · produzido por exportar_resultado() em F-EXP.
    D-130 · receptividade a IA · sem arbitrary_types · model_dump() JSON-compatível.
    """
    model_config = ConfigDict(use_enum_values=False)

    caminho_arquivo: str = Field(
        ...,
        description="Caminho absoluto do arquivo .xlsx gerado"
    )
    tamanho_bytes: int = Field(
        ...,
        description="Tamanho do arquivo gerado em bytes"
    )
    numero_abas: int = Field(
        ...,
        description="Número de abas criadas no arquivo"
    )
    tempo_geracao_segundos: float = Field(
        ...,
        description="Tempo total de geração do arquivo em segundos"
    )
    warnings_gerados: List[WarningEstrutural] = Field(
        default_factory=list,
        description="Warnings emitidos durante a exportação · C.2 nada silencioso"
    )
    capabilities_acionadas: List[str] = Field(
        default_factory=list,
        description="Capabilities acionadas durante a exportação · auditoria CAP-NN"
    )
