"""
visao_v2.py — V2 · Análise Comparativa entre Referências · Família A
Pipeline canônico V2 · 6 etapas A-F · Spec §2.1
Determinístico C.1 · zero invenção de comportamento C.3 · nada silencioso C.2
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field, model_validator

sys.path.insert(0, str(Path(__file__).parent.parent))

from apresentacao.formatos import default_unidade_para_tipo_campo
from contratos import (
    AjusteMotor,
    BloqueioOperacional,
    CabecalhoExecucao,
    CategoriaWarning,
    ContratoComparativo,
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
from transversais.t_agrupa import consolidar_com_modo
from transversais.t_diag import TDIAG
from transversais.t_modelo import ModeloConfig, aplicar_modelo, salvar_modelo
from transversais.t_sema import classificar_semantica

# ---------------------------------------------------------------------------
# Contratos V2-específicos
# ---------------------------------------------------------------------------


class ModeloAplicadoV2(BaseModel):
    model_config = ConfigDict(use_enum_values=False)

    nome_modelo: str = Field(..., description="Nome salvo do modelo T-MODELO aplicado")
    data_criacao_modelo: datetime = Field(..., description="Data de criação original do modelo")
    campos_casados: int = Field(..., description="Quantidade de campos do modelo que casaram com a nova base")
    campos_nao_casados: List[str] = Field(
        default_factory=list,
        description="Lista de campos do modelo sem correspondência · vazio quando 100% casou",
    )
    tipo_aplicacao: Literal["COMPLETA", "PARCIAL", "INCOMPATIVEL"] = Field(
        ...,
        description="COMPLETA quando todos os campos casaram · PARCIAL dispara W-V2-MOD-PARCIAL · INCOMPATIVEL dispara W-V2-MOD-INCOMP",
    )


class ComparacaoV2(ContratoComparativo):
    """Configuração analítica V2 · D-202 · subclasse fina de `ContratoComparativo`.

    A partir de D-202 toda a configuração comparativa vive em
    `contratos.ContratoComparativo` (Família A genérica). V2 herda sem
    estender · presente para nominação V2-específica e futuras extensões.
    """
    pass


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
        description="Opções específicas apresentadas ao usuário no painel de resolução",
    )
    escolha_usuario: str = Field(..., description="Opção efetivamente escolhida pelo usuário")
    contexto_caso: Dict[str, Any] = Field(
        default_factory=dict,
        description="Valores observados que dispararam o caso",
    )
    registrada_como: Literal["DECISAO_USUARIO"] = Field(
        "DECISAO_USUARIO",
        description="Fixo · D-021 · registrada no Diagnóstico como DECISAO_USUARIO",
    )


class NumerosAncoraV2(BaseModel):
    model_config = ConfigDict(use_enum_values=False)

    # Variante numérica
    total_origem: Optional[float] = Field(None, description="Total consolidado da Origem · None para ESTADO_SITUACAO")
    total_comparado: Optional[float] = Field(None, description="Total consolidado do Comparado · None para ESTADO_SITUACAO")
    diferenca_total: Optional[float] = Field(None, description="total_comparado - total_origem · None para ESTADO_SITUACAO")
    variacao_total_pct: Optional[float] = Field(
        None,
        description="diferenca_total / total_origem · None quando total_origem=0 ou ESTADO_SITUACAO",
    )

    # Variante ESTADO_SITUACAO
    total_combinacoes_analisadas: Optional[int] = Field(
        None,
        description="Contagem de combinações analisadas · apenas para ESTADO_SITUACAO",
    )
    combinacoes_com_mudanca: Optional[int] = Field(
        None,
        description="Combinações em que estado Origem ≠ estado Comparado · apenas para ESTADO_SITUACAO",
    )
    combinacoes_estaveis: Optional[int] = Field(
        None,
        description="Combinações em que estado Origem = estado Comparado · apenas para ESTADO_SITUACAO",
    )
    pct_mudanca: Optional[float] = Field(
        None,
        description="combinacoes_com_mudanca / total_combinacoes_analisadas · apenas para ESTADO_SITUACAO",
    )

    @model_validator(mode="after")
    def _validar_grupos_exclusivos(self) -> "NumerosAncoraV2":
        grupo_num = any(
            v is not None
            for v in [self.total_origem, self.total_comparado, self.diferenca_total, self.variacao_total_pct]
        )
        grupo_est = any(
            v is not None
            for v in [
                self.total_combinacoes_analisadas,
                self.combinacoes_com_mudanca,
                self.combinacoes_estaveis,
                self.pct_mudanca,
            ]
        )
        if grupo_num and grupo_est:
            raise ValueError(
                "NumerosAncoraV2: grupos numérico e estado/situação são mutuamente exclusivos"
            )
        return self


class LinhaTopVariacao(BaseModel):
    model_config = ConfigDict(use_enum_values=False)

    chave_agrupadores: Dict[str, Any] = Field(
        ...,
        description="Valores dos agrupadores que identificam a combinação",
    )
    valor_origem: Optional[float] = Field(
        None,
        description="None quando AUSENTE_ORIGEM ou NULO_ORIGEM · C.5",
    )
    valor_comparado: Optional[float] = Field(None, description="None quando AUSENTE_COMPARADO ou NULO_COMPARADO")
    diferenca: Optional[float] = Field(None, description="None quando qualquer lado ausente ou nulo")
    variacao_percentual: Optional[float] = Field(
        None,
        description="None para AUSENTE/NULO · None quando valor_origem=0 e valor_comparado≠0 · dispara W-V2-BZ",
    )
    classificacao_estrutural: Literal[
        "PRESENTE_AMBOS",
        "AUSENTE_ORIGEM",
        "AUSENTE_COMPARADO",
        "NULO_ORIGEM",
        "NULO_COMPARADO",
        "NULO_AMBOS",
    ] = Field(..., description="Uma das 6 categorias mutuamente exclusivas · D-022/D-023")
    classificacao_semantica: Optional[
        Literal[
            "POSITIVO", "NEGATIVO", "NEUTRO", "NAO_APLICAVEL",
            "AUMENTOU", "REDUZIU", "ESTAVEL",
        ]
    ] = Field(
        None,
        description=(
            "Aplicada quando tipo_campo é numérico · None quando ESTADO_SITUACAO. "
            "Para semantica_campo=NEUTRO os 4 estruturais aparecem distintos "
            "(AUMENTOU/REDUZIU/ESTAVEL/NAO_APLICAVEL · D-187)."
        ),
    )
    estado_origem: Optional[str] = Field(
        None,
        description="Estado textual da Origem · preenchido apenas quando tipo_campo=ESTADO_SITUACAO",
    )
    estado_comparado: Optional[str] = Field(
        None,
        description="Estado textual do Comparado · preenchido apenas quando tipo_campo=ESTADO_SITUACAO",
    )


class V2Result(VNResultBase):
    """Resultado da V2 · Análise Comparativa entre Referências."""

    model_config = ConfigDict(arbitrary_types_allowed=True, use_enum_values=False)

    visao_id: Literal["V2"] = Field("V2", description="Identificador fixo · V2")

    comparacao_realizada: ComparacaoV2 = Field(
        ...,
        description="Declaração da comparação executada · Origem · Comparado · estrutura · campo · semântica",
    )
    agrupadores_aplicados: List[str] = Field(
        ...,
        description="Lista ordenada dos agrupadores efetivamente usados · 1 a 9 · D-027",
    )
    resolucao_estrutural: Optional[ResolucaoEstruturalV2] = Field(
        None,
        description="Decisão do usuário em caso estrutural · None se nenhum caso detectado",
    )
    distribuicao_classificacoes_estruturais: Dict[str, int] = Field(
        ...,
        description="Contagem das 6 categorias estruturais · zeros preservados no contrato",
    )
    distribuicao_classificacoes_semanticas: Optional[Dict[str, int]] = Field(
        None,
        description="Contagem Positivo / Negativo / Neutro / Não aplicável · None para ESTADO_SITUACAO",
    )
    delta_por_classificacao_semantica: Optional[Dict[str, float]] = Field(
        None,
        description=(
            "Soma de `diferenca` agrupada por classificacao_semantica · usado pelo "
            "bloco 'Saúde da comparação' · None para ESTADO_SITUACAO · D-192 / E2"
        ),
    )
    concentracao: Optional[Dict[str, Any]] = Field(
        None,
        description=(
            "Concentração das variações · pct do |Δ| total explicado pelos top-N "
            "maiores · {'top_5_pct', 'top_10_pct', 'interpretacao'} · None para "
            "ESTADO_SITUACAO ou quando há <5 PRESENTE_AMBOS · D-192 / E3a"
        ),
    )
    onde_se_concentra: Optional[Dict[str, Any]] = Field(
        None,
        description=(
            "Top 3 categorias do `agrupador_destacado` por |Δ| absoluto · com "
            "rodapé de outras N · None para ESTADO_SITUACAO · D-192 / E3b"
        ),
    )
    numeros_ancora: NumerosAncoraV2 = Field(
        ...,
        description="4 KPIs do Bloco 2 do Resumo Executivo",
    )
    top_variacoes: List[LinhaTopVariacao] = Field(
        ...,
        description="Top 10 combinações por |Δ| (numérico) ou por mudança (Estado/Situação)",
    )
    modelo_aplicado: Optional[ModeloAplicadoV2] = Field(
        None,
        description="Referência a T-MODELO quando modelo foi aplicado · None se execução fresca",
    )


# ---------------------------------------------------------------------------
# ECP · Escala de cardinalidade (§2.12)
# ---------------------------------------------------------------------------


def _classificar_patamar_agrupadores(n: int) -> str:
    if n <= 3:
        return "P1-AGRUP-NORMAL"
    elif n <= 5:
        return "P2-AGRUP-ALERTA-LEVE"
    elif n <= 8:
        return "P3-AGRUP-ALERTA-FORTE"
    return "P4-AGRUP-BLOQUEIO"


def _classificar_patamar_discriminador(n_valores: int, ted_limite: int) -> str:
    if n_valores <= 2:
        return "P1-DISCR-NORMAL"
    elif n_valores <= 10:
        return "P2-DISCR-ALERTA-LEVE"
    elif n_valores <= ted_limite:
        return "P3-DISCR-ALERTA-FORTE"
    return "P4-DISCR-BLOQUEIO-LEVE"


def _classificar_patamar_resultado(n_linhas_estimadas: int) -> str:
    if n_linhas_estimadas <= 10_000:
        return "P1-RES-NORMAL"
    elif n_linhas_estimadas <= 100_000:
        return "P2-RES-ALERTA-LEVE"
    elif n_linhas_estimadas <= 500_000:
        return "P3-RES-ALERTA-FORTE"
    return "P4-RES-BLOQUEIO"


# ---------------------------------------------------------------------------
# Constantes internas
# ---------------------------------------------------------------------------

_CATS_ESTRUTURAIS: List[str] = [
    "PRESENTE_AMBOS",
    "AUSENTE_ORIGEM",
    "AUSENTE_COMPARADO",
    "NULO_ORIGEM",
    "NULO_COMPARADO",
    "NULO_AMBOS",
]

_REGRA_MAP: Dict[str, str] = {
    "SOMA": "soma",
    "MEDIA": "media",
    "MAXIMO": "maximo",
    "MINIMO": "minimo",
    "CONTAGEM": "contagem",
}

_SEMA_V2_TO_TSEMA: Dict[str, str] = {
    "MAIOR_MELHOR": "MAIOR_MELHOR",
    "MENOR_MELHOR": "MENOR_MELHOR",
    "NEUTRO": "NEUTRA",
}

_SEMA_LABEL_TO_CLASS: Dict[str, str] = {
    # MAIOR_MELHOR / MENOR_MELHOR · qualitativo (T-SEMA traduz estrutural × semantica)
    "Melhorou": "POSITIVO",
    "Piorou": "NEGATIVO",
    # NEUTRA · 4 estruturais distintos (D-187 · não colapsa em "NEUTRO")
    "Aumentou": "AUMENTOU",
    "Reduziu": "REDUZIU",
    "Estável": "ESTAVEL",
    "Não aplicável": "NAO_APLICAVEL",
}


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------


def _make_motor_meta(motor_result: MotorResult) -> MotorResultMeta:
    return MotorResultMeta(
        total_linhas_originais=motor_result.total_linhas_originais,
        total_linhas_processadas=motor_result.total_linhas_processadas,
        modo_upload=motor_result.modo_upload,
        timestamp_processamento=motor_result.timestamp_processamento,
        warnings_motor=list(motor_result.warnings),
    )


def _flatten_warnings(diagnostico: DiagnosticoVN) -> List[WarningEstrutural]:
    result: List[WarningEstrutural] = []
    for warns in diagnostico.warnings_por_categoria.values():
        result.extend(warns)
    return result


def _resolver_agrupador_destacado(
    agrupadores: List[str],
    config: Dict[str, Any],
) -> Optional[str]:
    """Resolve `agrupador_destacado` válido ou None se não há agrupadores · E3b."""
    declarado = config.get("agrupador_destacado")
    if declarado and declarado in agrupadores:
        return declarado
    if agrupadores:
        return agrupadores[0]
    return None


def _make_comparacao_from_config(config: Dict[str, Any]) -> ComparacaoV2:
    tipo = config.get("tipo_campo", "NUMERICO_ADITIVO")
    unidade = config.get("unidade") or default_unidade_para_tipo_campo(tipo)
    agrupadores = config.get("agrupadores", []) or []
    destacado = _resolver_agrupador_destacado(agrupadores, config)
    return ComparacaoV2(
        estrutura_entrada=config.get("estrutura_entrada", "POR_COLUNAS"),
        origem_rotulo_tecnico=config.get("origem_rotulo_tecnico", "Origem"),
        comparado_rotulo_tecnico=config.get("comparado_rotulo_tecnico", "Comparado"),
        origem_rotulo_ux=config.get("origem_rotulo_ux", "Origem"),
        comparado_rotulo_ux=config.get("comparado_rotulo_ux", "Comparado"),
        coluna_discriminadora=config.get("coluna_discriminadora"),
        modo_4_ativado=config.get("modo_4_ativado", False),
        estados_nao_escolhidos=config.get("estados_nao_escolhidos", []),
        campo_analisado=config.get("campo_analisado", ""),
        tipo_campo=tipo,
        semantica_campo=config.get("semantica_campo", "NEUTRO"),
        unidade=unidade,
        agrupador_destacado=destacado,
        regra_agregacao=config.get("regra_agregacao", "SOMA"),
        metodo_consolidacao_relativo=config.get("metodo_consolidacao_relativo"),
        campo_peso=config.get("campo_peso"),
    )


def _make_empty_ancora(config: Dict[str, Any]) -> NumerosAncoraV2:
    tipo = config.get("tipo_campo", "NUMERICO_ADITIVO")
    if tipo == "ESTADO_SITUACAO":
        return NumerosAncoraV2(
            total_combinacoes_analisadas=0,
            combinacoes_com_mudanca=0,
            combinacoes_estaveis=0,
            pct_mudanca=0.0,
        )
    return NumerosAncoraV2()


def _resultado_bloqueado(
    motor_result: MotorResult,
    config: Dict[str, Any],
    t_diag: TDIAG,
    bloqueios: List[BloqueioOperacional],
) -> V2Result:
    diagnostico = t_diag.consolidar()
    warns = _flatten_warnings(diagnostico)
    try:
        comparacao = _make_comparacao_from_config(config)
    except Exception:
        comparacao = ComparacaoV2(
            estrutura_entrada="POR_COLUNAS",
            origem_rotulo_tecnico="Origem",
            comparado_rotulo_tecnico="Comparado",
            origem_rotulo_ux="Origem",
            comparado_rotulo_ux="Comparado",
            campo_analisado=config.get("campo_analisado", ""),
            tipo_campo="NUMERICO_ADITIVO",
            semantica_campo="NEUTRO",
        )

    thresholds = config.get("thresholds", {})
    resumo = ResumoExecutivoPadrao(
        bloco_1_cabecalho=CabecalhoExecucao(
            visao="V2",
            modo_upload=motor_result.modo_upload,
            agrupadores=config.get("agrupadores", []),
            medida_principal=config.get("campo_analisado"),
        ),
        bloco_2_numeros_ancora={},
        bloco_3_distribuicao={cat: 0 for cat in _CATS_ESTRUTURAIS},
        bloco_4_elementos_destacados={"top_variacoes": []},
        bloco_5_leitura_qualitativa=LeituraQualitativa(
            classificacao_ativa="BLOQUEADO",
            thresholds_usados={k: float(v) for k, v in thresholds.items() if isinstance(v, (int, float))},
            alguma_leitura_alterada_por_edicao=False,
        ),
        bloco_6_qualidade_estrutural=QualidadeEstrutural(
            total_warnings=len(warns),
            warnings_por_categoria={},
            ajustes_aplicados=len(diagnostico.ajustes_aplicados),
            tem_bloqueios_escapados=False,
        ),
    )

    resolucao_raw = config.get("resolucao_estrutural")
    resolucao = None
    if resolucao_raw and isinstance(resolucao_raw, dict):
        try:
            resolucao = ResolucaoEstruturalV2(**resolucao_raw)
        except Exception:
            pass

    return V2Result(
        visao_id="V2",
        config_usada=config,
        motor_result_meta=_make_motor_meta(motor_result),
        base_analitica=pd.DataFrame(),
        resumo_executivo=resumo,
        coracao_visual=CoracaoVisualRef(
            nome_aba="Matriz de Confronto",
            tipo="MATRIZ_COLORIDA",
            capabilities_requeridas=["formatacao_condicional", "congelar_paineis"],
        ),
        bloqueios_disparados=bloqueios,
        warnings=warns,
        diagnostico=diagnostico,
        comparacao_realizada=comparacao,
        agrupadores_aplicados=config.get("agrupadores", []),
        resolucao_estrutural=resolucao,
        distribuicao_classificacoes_estruturais={cat: 0 for cat in _CATS_ESTRUTURAIS},
        distribuicao_classificacoes_semanticas=None,
        delta_por_classificacao_semantica=None,
        concentracao=None,
        onde_se_concentra=None,
        numeros_ancora=_make_empty_ancora(config),
        top_variacoes=[],
        modelo_aplicado=None,
    )


def _restaurar_nulos_todo_nulo(
    df_cons: pd.DataFrame,
    df_orig_side: pd.DataFrame,
    agrupadores: List[str],
    campo: str,
) -> pd.DataFrame:
    """Restaura NaN para grupos cujo campo_analisado era todo-nulo no lado original.

    T-AGRUPA com 'soma' retorna 0 para grupos all-NaN (pandas default).
    Este helper corrige isso preservando NaN (C.5).
    """
    if campo not in df_orig_side.columns:
        return df_cons
    if not agrupadores:
        if df_orig_side[campo].isna().all():
            df_cons = df_cons.copy()
            df_cons[campo] = float("nan")
        return df_cons

    null_flags = (
        df_orig_side.groupby(agrupadores, sort=False)[campo]
        .apply(lambda s: s.isna().all())
        .reset_index()
    )
    null_flags.columns = list(agrupadores) + ["_todo_nulo"]

    df_cons = df_cons.merge(null_flags, on=agrupadores, how="left")
    df_cons.loc[df_cons["_todo_nulo"] == True, campo] = float("nan")
    df_cons = df_cons.drop(columns=["_todo_nulo"]).reset_index(drop=True)
    return df_cons


def _consolidar_media_ponderada(
    df: pd.DataFrame,
    agrupadores: List[str],
    campo_val: str,
    campo_peso: str,
    t_diag: TDIAG,
) -> Tuple[pd.DataFrame, Optional[BloqueioOperacional]]:
    """Média ponderada por grupo · D-024."""
    pesos_validos = df[campo_peso].dropna()
    if len(pesos_validos) == 0 or (pesos_validos <= 0).all():
        bl = BloqueioOperacional(
            codigo="B-V2-PESO-INVALIDO",
            condicao_disparo=(
                f"Média ponderada: todos os valores de '{campo_peso}' são nulos, "
                "zerados ou negativos — impossível calcular."
            ),
            escapavel=False,
            escape_acionado=None,
            warning_pos_escape=None,
            contexto_disparo={
                "campo_peso": campo_peso,
                "nulos": int(df[campo_peso].isna().sum()),
                "negativos": int((df[campo_peso].fillna(0) <= 0).sum()),
            },
        )
        return df.head(0)[agrupadores + [campo_val]], bl

    df = df.copy()
    df["_wprod"] = df[campo_val] * df[campo_peso]
    df["_wpeso"] = df[campo_peso]

    if agrupadores:
        agg = df.groupby(agrupadores, sort=False).agg(
            _wprod=("_wprod", "sum"),
            _wpeso=("_wpeso", "sum"),
        ).reset_index()
    else:
        agg = pd.DataFrame({
            "_wprod": [df["_wprod"].sum()],
            "_wpeso": [df["_wpeso"].sum()],
        })

    agg[campo_val] = agg["_wprod"] / agg["_wpeso"]
    cols = list(agrupadores) + [campo_val] if agrupadores else [campo_val]
    return agg[cols].reset_index(drop=True), None


# ---------------------------------------------------------------------------
# Etapa A · Preparação da base
# ---------------------------------------------------------------------------


def _etapa_a_preparar_base(
    motor_result: MotorResult,
    config: Dict[str, Any],
    t_diag: TDIAG,
) -> Tuple[pd.DataFrame, List[BloqueioOperacional]]:
    """Filtra df para discriminador escolhido (POR_LINHAS) ou no-op (POR_COLUNAS)."""
    df = motor_result.df.copy()
    bloqueios: List[BloqueioOperacional] = []

    # B-V2-ARQUIVO-ILEGIVEL: df vazio indica base não legível
    if df.empty:
        bloqueios.append(BloqueioOperacional(
            codigo="B-V2-ARQUIVO-ILEGIVEL",
            condicao_disparo="Base de dados vazia ou não legível pelo motor.",
            escapavel=False,
            escape_acionado=None,
            warning_pos_escape=None,
            contexto_disparo={
                "formato_detectado": motor_result.modo_upload,
                "erro_leitura": "DataFrame vazio após processamento",
            },
        ))
        return df, bloqueios

    campo = config.get("campo_analisado", "")
    tipo_campo = config.get("tipo_campo", "NUMERICO_ADITIVO")
    estrutura = config.get("estrutura_entrada", "POR_COLUNAS")

    # B-V2-ESTRUTURA-INVALIDA: apenas POR_LINHAS; em POR_COLUNAS o campo é nome conceptual
    if estrutura != "POR_COLUNAS" and campo not in df.columns:
        bloqueios.append(BloqueioOperacional(
            codigo="B-V2-ESTRUTURA-INVALIDA",
            condicao_disparo=f"Campo analisado '{campo}' não encontrado na base.",
            escapavel=False,
            escape_acionado=None,
            warning_pos_escape=None,
            contexto_disparo={
                "total_linhas_detectadas": len(df),
                "colunas_numericas": [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])],
            },
        ))
        return df, bloqueios

    if estrutura == "POR_LINHAS":
        coluna_disc = config.get("coluna_discriminadora", "")
        if not coluna_disc or coluna_disc not in df.columns:
            bloqueios.append(BloqueioOperacional(
                codigo="B-V2-DISCRIMINADOR-0",
                condicao_disparo=f"Coluna discriminadora '{coluna_disc}' não encontrada ou vazia.",
                escapavel=False,
                escape_acionado=None,
                warning_pos_escape=None,
                contexto_disparo={"coluna_discriminadora": coluna_disc},
            ))
            return df, bloqueios

        valores_disc = df[coluna_disc].dropna().unique()

        if len(valores_disc) == 0:
            bloqueios.append(BloqueioOperacional(
                codigo="B-V2-DISCRIMINADOR-0",
                condicao_disparo=f"Coluna discriminadora '{coluna_disc}' está completamente vazia.",
                escapavel=False,
                escape_acionado=None,
                warning_pos_escape=None,
                contexto_disparo={"coluna_discriminadora": coluna_disc},
            ))
            return df, bloqueios

        if len(valores_disc) == 1:
            bloqueios.append(BloqueioOperacional(
                codigo="B-V2-DISCRIMINADOR-1",
                condicao_disparo=(
                    f"Coluna discriminadora '{coluna_disc}' tem apenas 1 valor único — "
                    "impossível comparar dois estados."
                ),
                escapavel=False,
                escape_acionado=None,
                warning_pos_escape=None,
                contexto_disparo={
                    "coluna_discriminadora": coluna_disc,
                    "valor_unico": str(valores_disc[0]),
                },
            ))
            return df, bloqueios

        # W-V2-MIX · tipos mistos
        tipos_presentes = set(type(v).__name__ for v in valores_disc)
        if len(tipos_presentes) > 1:
            t_diag.registrar_warning(TDIAG.w(
                "W-V2-MIX",
                CategoriaWarning.ALERTA_ESTRUTURAL,
                f"Coluna discriminadora '{coluna_disc}' tem tipos mistos: {sorted(tipos_presentes)}. "
                "Motor usa ordenação alfabética.",
                coluna_discriminadora=coluna_disc,
                tipos_detectados=sorted(tipos_presentes),
            ))

        # W-V2-NMANY
        limite_alerta = int(config.get("thresholds", {}).get("limite_valores_discriminador_alerta", 50))
        if len(valores_disc) > limite_alerta:
            t_diag.registrar_warning(TDIAG.w(
                "W-V2-NMANY",
                CategoriaWarning.ALERTA_ESTRUTURAL,
                f"Coluna discriminadora '{coluna_disc}' tem {len(valores_disc)} valores únicos "
                f"(acima do limite de {limite_alerta}). Considere filtrar previamente.",
                coluna_discriminadora=coluna_disc,
                n_valores=len(valores_disc),
                limite=limite_alerta,
            ))

        # W-V2-AGRUP-MUITOS
        agrupadores = config.get("agrupadores", [])
        if len(agrupadores) >= 6:
            t_diag.registrar_warning(TDIAG.w(
                "W-V2-AGRUP-MUITOS",
                CategoriaWarning.INFORMATIVO,
                f"Análise com {len(agrupadores)} agrupadores simultâneos — granularidade fina confirmada.",
                n_agrupadores=len(agrupadores),
            ))

        # Modo 4: registrar estados excluídos
        estados_nao_escolhidos = config.get("estados_nao_escolhidos", [])
        if config.get("modo_4_ativado", False) and estados_nao_escolhidos:
            linhas_excluidas = int(df[df[coluna_disc].isin(estados_nao_escolhidos)].shape[0])
            t_diag.registrar_ajuste(AjusteMotor(
                tipo_ajuste="MODO_4_ESTADOS_EXCLUIDOS",
                linhas_afetadas=linhas_excluidas,
                descricao=(
                    f"Modo 4: estados não escolhidos excluídos da análise: "
                    f"{estados_nao_escolhidos}"
                ),
            ))

        # Filtrar para os 2 valores escolhidos
        orig_tech = config.get("origem_rotulo_tecnico", "")
        comp_tech = config.get("comparado_rotulo_tecnico", "")
        df = df[df[coluna_disc].isin([orig_tech, comp_tech])].copy()

    else:
        # POR_COLUNAS: W-V2-AGRUP-MUITOS check
        agrupadores = config.get("agrupadores", [])
        if len(agrupadores) >= 6:
            t_diag.registrar_warning(TDIAG.w(
                "W-V2-AGRUP-MUITOS",
                CategoriaWarning.INFORMATIVO,
                f"Análise com {len(agrupadores)} agrupadores simultâneos — granularidade fina confirmada.",
                n_agrupadores=len(agrupadores),
            ))

    return df, bloqueios


# ---------------------------------------------------------------------------
# Etapa B · Detecção de casos estruturais
# ---------------------------------------------------------------------------


def _etapa_b_detectar_casos_estruturais(
    df: pd.DataFrame,
    config: Dict[str, Any],
    t_diag: TDIAG,
) -> Tuple[Optional[ResolucaoEstruturalV2], List[BloqueioOperacional]]:
    """Detecta e registra casos estruturais (D-021). Verifica cancelamento do usuário."""
    bloqueios: List[BloqueioOperacional] = []

    resolucao_raw = config.get("resolucao_estrutural")
    resolucao: Optional[ResolucaoEstruturalV2] = None

    if resolucao_raw and isinstance(resolucao_raw, dict):
        escolha = resolucao_raw.get("escolha_usuario", "")
        if escolha == "cancelar":
            bloqueios.append(BloqueioOperacional(
                codigo="B-V2-CASO-ESTRUTURAL-CANCELADO",
                condicao_disparo="Usuário cancelou a análise no painel de resolução estrutural.",
                escapavel=False,
                escape_acionado=None,
                warning_pos_escape=None,
                contexto_disparo={
                    "tipo_caso": resolucao_raw.get("tipo_caso", ""),
                    "contexto_caso": resolucao_raw.get("contexto_caso", {}),
                },
            ))
            return None, bloqueios

        try:
            resolucao = ResolucaoEstruturalV2(**resolucao_raw)
            t_diag.registrar_warning(TDIAG.w(
                "W-V2-DECISAO-USUARIO",
                CategoriaWarning.DECISAO_USUARIO,
                f"Caso estrutural '{resolucao.tipo_caso}' resolvido pelo usuário: '{resolucao.escolha_usuario}'.",
                tipo_caso=resolucao.tipo_caso,
                escolha_usuario=resolucao.escolha_usuario,
            ))
            t_diag.registrar_decisao_usuario(DecisaoUsuario(
                contexto=f"caso_estrutural_{resolucao.tipo_caso}",
                valor_default="cancelar",
                valor_escolhido=resolucao.escolha_usuario,
            ))
        except Exception:
            pass

    # 4 ajustes leves automáticos (D-021): aplicar como AJUSTE_LEVE
    agrupadores = config.get("agrupadores", [])
    leves_aplicados = 0
    for col in agrupadores:
        if col in df.columns:
            n_nulos = int(df[col].isna().sum())
            if n_nulos > 0:
                # Ajuste 4: nulos isolados em agrupador → '(sem valor)'
                leves_aplicados += 1

    if leves_aplicados > 0:
        t_diag.registrar_warning(TDIAG.w(
            "W-V2-AJUSTE-LEVE",
            CategoriaWarning.AJUSTE_LEVE,
            f"{leves_aplicados} ajuste(s) leve(s) aplicado(s): nulos em agrupadores substituídos por '(sem valor)'.",
            n_ajustes=leves_aplicados,
            tipo_ajuste="nulos_em_agrupador",
        ))

    return resolucao, bloqueios


# ---------------------------------------------------------------------------
# Etapa C · Consolidação pré-cálculo
# ---------------------------------------------------------------------------


def _etapa_c_consolidar_pre_calculo(
    df: pd.DataFrame,
    config: Dict[str, Any],
    t_diag: TDIAG,
) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame], List[BloqueioOperacional]]:
    """Retorna (df_orig_consolidado, df_comp_consolidado, bloqueios)."""
    bloqueios: List[BloqueioOperacional] = []
    agrupadores: List[str] = config.get("agrupadores", [])
    campo: str = config["campo_analisado"]
    tipo_campo: str = config.get("tipo_campo", "NUMERICO_ADITIVO")
    estrutura: str = config.get("estrutura_entrada", "POR_COLUNAS")
    orig_tech: str = config.get("origem_rotulo_tecnico", "")
    comp_tech: str = config.get("comparado_rotulo_tecnico", "")
    coluna_disc: str = config.get("coluna_discriminadora", "")
    metodo_consol: Optional[str] = config.get("metodo_consolidacao_relativo")
    campo_peso: Optional[str] = config.get("campo_peso")
    modo_pre_ag: bool = config.get("modo_pre_agregado", False)

    # Determinar regra de agregação
    if tipo_campo == "ESTADO_SITUACAO":
        regra_t_agrupa = "primeiro"
    else:
        regra_raw = config.get("regra_agregacao", "SOMA")
        regra_t_agrupa = _REGRA_MAP.get(regra_raw, "soma")

    modo_base = "PRE_AGREGADO" if modo_pre_ag else "TRANSACIONAL"

    # W-V2-AGG: tipo relativo/não-aditivo com agrupadores
    if tipo_campo in ("NUMERICO_RELATIVO", "NUMERICO_NAO_ADITIVO") and len(agrupadores) > 0:
        t_diag.registrar_warning(TDIAG.w(
            "W-V2-AGG",
            CategoriaWarning.INFORMATIVO,
            f"Campo '{campo}' é {tipo_campo}. Método de consolidação aplicado: "
            f"'{metodo_consol or 'MEDIA_SIMPLES'}' com agrupadores {agrupadores}.",
            tipo_campo=tipo_campo,
            metodo=metodo_consol or "MEDIA_SIMPLES",
            agrupadores=agrupadores,
        ))

    # Separar lados
    if estrutura == "POR_LINHAS":
        cols_necessarias = agrupadores + [campo]
        if campo_peso and campo_peso in df.columns:
            cols_necessarias = agrupadores + [campo, campo_peso]
        cols_disponiveis = [c for c in cols_necessarias if c in df.columns]
        df_orig_side = df[df[coluna_disc] == orig_tech][cols_disponiveis].copy()
        df_comp_side = df[df[coluna_disc] == comp_tech][cols_disponiveis].copy()
    else:
        # POR_COLUNAS
        if orig_tech not in df.columns or comp_tech not in df.columns:
            bloqueios.append(BloqueioOperacional(
                codigo="B-V2-ESTRUTURA-INVALIDA",
                condicao_disparo=(
                    f"Coluna(s) de comparação não encontradas: "
                    f"'{orig_tech}' ou '{comp_tech}'."
                ),
                escapavel=False,
                escape_acionado=None,
                warning_pos_escape=None,
                contexto_disparo={
                    "total_linhas_detectadas": len(df),
                    "colunas_numericas": [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])],
                },
            ))
            return None, None, bloqueios
        cols_orig = agrupadores + [orig_tech]
        cols_comp = agrupadores + [comp_tech]
        if campo_peso and campo_peso in df.columns:
            cols_orig = agrupadores + [orig_tech, campo_peso]
            cols_comp = agrupadores + [comp_tech, campo_peso]
        df_orig_side = df[[c for c in cols_orig if c in df.columns]].copy()
        df_comp_side = df[[c for c in cols_comp if c in df.columns]].copy()
        df_orig_side = df_orig_side.rename(columns={orig_tech: campo})
        df_comp_side = df_comp_side.rename(columns={comp_tech: campo})

    # Substituir nulos em agrupadores por '(sem valor)' · D-023
    for side_df in [df_orig_side, df_comp_side]:
        for col in agrupadores:
            if col in side_df.columns:
                side_df[col] = side_df[col].fillna("(sem valor)")

    # B-V2-CAMPO-100-NULO
    for label, side_df in [("origem", df_orig_side), ("comparado", df_comp_side)]:
        if campo in side_df.columns:
            total = len(side_df)
            nulos = int(side_df[campo].isna().sum())
            if total > 0 and nulos == total:
                bloqueios.append(BloqueioOperacional(
                    codigo="B-V2-CAMPO-100-NULO",
                    condicao_disparo=(
                        f"Campo '{campo}' tem 100% de valores nulos em '{label}' "
                        "— impossível calcular."
                    ),
                    escapavel=False,
                    escape_acionado=None,
                    warning_pos_escape=None,
                    contexto_disparo={"lado_vazio": label, "total_nulos": nulos},
                ))
                return None, None, bloqueios

    # Consolidação
    if metodo_consol == "MEDIA_PONDERADA" and campo_peso:
        df_orig_cons, bl = _consolidar_media_ponderada(
            df_orig_side, agrupadores, campo, campo_peso, t_diag
        )
        if bl:
            return None, None, [bl]
        df_comp_cons, bl = _consolidar_media_ponderada(
            df_comp_side, agrupadores, campo, campo_peso, t_diag
        )
        if bl:
            return None, None, [bl]

    elif metodo_consol == "MEDIA_SIMPLES" and tipo_campo in ("NUMERICO_RELATIVO", "NUMERICO_NAO_ADITIVO"):
        df_orig_cons, w_orig = consolidar_com_modo(df_orig_side, agrupadores, "media", modo_base)
        df_comp_cons, w_comp = consolidar_com_modo(df_comp_side, agrupadores, "media", modo_base)
        for w in w_orig + w_comp:
            if "DUPLICATA" in w.codigo or "PRE_AGREGADO" in w.codigo:
                t_diag.registrar_warning(TDIAG.w(
                    "W-V2-PAGREG-DUP",
                    CategoriaWarning.ALERTA_ESTRUTURAL,
                    "Modo Pré-agregado declarado mas duplicata de chave detectada. Motor recai em consolidação.",
                    codigo_original=w.codigo,
                ))
            else:
                t_diag.registrar_warning(w)

    else:
        df_orig_cons, w_orig = consolidar_com_modo(
            df_orig_side[[c for c in df_orig_side.columns if c in agrupadores + [campo]]],
            agrupadores,
            regra_t_agrupa,
            modo_base,
        )
        df_comp_cons, w_comp = consolidar_com_modo(
            df_comp_side[[c for c in df_comp_side.columns if c in agrupadores + [campo]]],
            agrupadores,
            regra_t_agrupa,
            modo_base,
        )
        for w in w_orig + w_comp:
            if "DUPLICATA" in w.codigo or "PRE_AGREGADO" in w.codigo:
                t_diag.registrar_warning(TDIAG.w(
                    "W-V2-PAGREG-DUP",
                    CategoriaWarning.ALERTA_ESTRUTURAL,
                    "Modo Pré-agregado declarado mas duplicata de chave detectada. Motor recai em consolidação.",
                    codigo_original=w.codigo,
                ))
            else:
                t_diag.registrar_warning(w)

    # Restaurar NaN para grupos all-null (C.5 · None ≠ 0)
    if tipo_campo != "ESTADO_SITUACAO":
        df_orig_cons = _restaurar_nulos_todo_nulo(df_orig_cons, df_orig_side, agrupadores, campo)
        df_comp_cons = _restaurar_nulos_todo_nulo(df_comp_cons, df_comp_side, agrupadores, campo)

    # W-V2-NULL-MASS
    limiar_nulo = float(config.get("thresholds", {}).get("limiar_nulo_massivo_pct", 0.20))
    for label, side_df_orig, side_cons in [
        ("origem", df_orig_side, df_orig_cons),
        ("comparado", df_comp_side, df_comp_cons),
    ]:
        if campo in side_df_orig.columns:
            total = len(side_df_orig)
            nulos = int(side_df_orig[campo].isna().sum())
            if total > 0 and (nulos / total) > limiar_nulo:
                t_diag.registrar_warning(TDIAG.w(
                    "W-V2-NULL-MASS",
                    CategoriaWarning.ALERTA_ESTRUTURAL_LEVE,
                    f"Campo '{campo}' em '{label}' tem {nulos}/{total} nulos "
                    f"({100 * nulos / total:.1f}% > {100 * limiar_nulo:.0f}% limiar).",
                    campo=campo,
                    lado=label,
                    pct_nulos=round(nulos / total, 4),
                    limiar=limiar_nulo,
                ))

    return df_orig_cons, df_comp_cons, bloqueios


# ---------------------------------------------------------------------------
# Etapa D · Cálculo comparativo
# ---------------------------------------------------------------------------


def _etapa_d_calcular_comparativo(
    df_orig: pd.DataFrame,
    df_comp: pd.DataFrame,
    config: Dict[str, Any],
    t_diag: TDIAG,
) -> pd.DataFrame:
    """Outer join + classificação estrutural 6 categorias + Δ e Δ%."""
    agrupadores: List[str] = config.get("agrupadores", [])
    campo: str = config["campo_analisado"]
    tipo_campo: str = config.get("tipo_campo", "NUMERICO_ADITIVO")
    orig_col = campo + "_origem"
    comp_col = campo + "_comparado"

    if agrupadores:
        merged = df_orig.merge(
            df_comp,
            on=agrupadores,
            how="outer",
            suffixes=("_origem", "_comparado"),
            indicator=True,
        )
    else:
        # Sem agrupadores: não há chave de join, criar linhas artificialmente
        df_o = df_orig.copy()
        df_c = df_comp.copy()
        df_o["_merge_key"] = 0
        df_c["_merge_key"] = 0
        merged = df_o.merge(df_c, on="_merge_key", how="outer", suffixes=("_origem", "_comparado"), indicator=True)
        merged = merged.drop(columns=["_merge_key"])

    merged = merged.sort_values(agrupadores if agrupadores else []).reset_index(drop=True)

    # Classificação estrutural
    def _classif(row: pd.Series) -> str:
        merge_val = row.get("_merge", "both")
        if merge_val == "left_only":
            return "AUSENTE_COMPARADO"
        if merge_val == "right_only":
            return "AUSENTE_ORIGEM"
        v_o = row.get(orig_col)
        v_c = row.get(comp_col)
        o_null = v_o is None or (isinstance(v_o, float) and pd.isna(v_o))
        c_null = v_c is None or (isinstance(v_c, float) and pd.isna(v_c))
        if o_null and c_null:
            return "NULO_AMBOS"
        if o_null:
            return "NULO_ORIGEM"
        if c_null:
            return "NULO_COMPARADO"
        return "PRESENTE_AMBOS"

    merged["classificacao_estrutural"] = merged.apply(_classif, axis=1)
    merged = merged.drop(columns=["_merge"])

    # Renomear para valor_origem / valor_comparado
    rename_map: Dict[str, str] = {}
    if orig_col in merged.columns:
        rename_map[orig_col] = "valor_origem"
    if comp_col in merged.columns:
        rename_map[comp_col] = "valor_comparado"
    # Campos sem sufixo (quando 0 agrupadores e POR_COLUNAS)
    if campo + "_origem" not in merged.columns and campo in df_orig.columns:
        if campo in merged.columns:
            rename_map[campo] = "valor_origem"
    merged = merged.rename(columns=rename_map)

    # Garantir colunas existentes
    for col in ["valor_origem", "valor_comparado"]:
        if col not in merged.columns:
            merged[col] = float("nan")

    # Para ESTADO_SITUACAO: mover para estado_origem / estado_comparado
    if tipo_campo == "ESTADO_SITUACAO":
        merged["estado_origem"] = merged["valor_origem"].astype(object).where(
            merged["classificacao_estrutural"].isin(["PRESENTE_AMBOS", "AUSENTE_COMPARADO", "NULO_ORIGEM"]),
            other=None,
        )
        merged["estado_comparado"] = merged["valor_comparado"].astype(object).where(
            merged["classificacao_estrutural"].isin(["PRESENTE_AMBOS", "AUSENTE_ORIGEM", "NULO_COMPARADO"]),
            other=None,
        )
        merged["valor_origem"] = float("nan")
        merged["valor_comparado"] = float("nan")
        merged["diferenca"] = float("nan")
        merged["variacao_percentual"] = float("nan")
        merged["classificacao_semantica"] = None
        return merged

    merged["estado_origem"] = None
    merged["estado_comparado"] = None

    # Δ e Δ% (apenas PRESENTE_AMBOS) · C.5 · D-022/D-023
    bz_disparado = False

    def _delta_row(row: pd.Series) -> Tuple[Any, Any]:
        if row["classificacao_estrutural"] != "PRESENTE_AMBOS":
            return None, None
        v_o = row["valor_origem"]
        v_c = row["valor_comparado"]
        if pd.isna(v_o) or pd.isna(v_c):
            return None, None
        diferenca = float(v_c) - float(v_o)
        if float(v_o) == 0 and float(v_c) != 0:
            return float(v_c), None  # W-V2-BZ: variacao fica None
        if float(v_o) == 0 and float(v_c) == 0:
            return 0.0, 0.0
        return diferenca, diferenca / float(v_o)

    deltas = merged.apply(_delta_row, axis=1, result_type="expand")
    merged["diferenca"] = deltas[0]
    merged["variacao_percentual"] = deltas[1]

    # Detectar W-V2-BZ
    bz_mask = (
        (merged["classificacao_estrutural"] == "PRESENTE_AMBOS")
        & (merged["valor_origem"].fillna(1) == 0)
        & (merged["valor_comparado"].fillna(0) != 0)
    )
    n_bz = int(bz_mask.sum())
    if n_bz > 0:
        t_diag.registrar_warning(TDIAG.w(
            "W-V2-BZ",
            CategoriaWarning.ALERTA_ESTRUTURAL_LEVE,
            f"{n_bz} linha(s) com Origem=0 e Comparado≠0 — variação percentual indefinida (None).",
            n_linhas=n_bz,
        ))

    # W-V2-AUSENTE-EM-UM-LADO
    ausentes = merged["classificacao_estrutural"].isin(["AUSENTE_ORIGEM", "AUSENTE_COMPARADO"])
    n_ausentes = int(ausentes.sum())
    if n_ausentes > 0:
        t_diag.registrar_warning(TDIAG.w(
            "W-V2-AUSENTE-EM-UM-LADO",
            CategoriaWarning.ALERTA_ESTRUTURAL,
            f"{n_ausentes} combinação(ões) ausente(s) em um dos lados da comparação.",
            n_ausentes=n_ausentes,
        ))

    # W-NULO-MEDIDA
    nulos = merged["classificacao_estrutural"].isin(["NULO_ORIGEM", "NULO_COMPARADO", "NULO_AMBOS"])
    n_nulos = int(nulos.sum())
    if n_nulos > 0:
        t_diag.registrar_warning(TDIAG.w(
            "W-NULO-MEDIDA",
            CategoriaWarning.ALERTA_ESTRUTURAL,
            f"{n_nulos} linha(s) com nulo(s) na medida '{campo}'.",
            n_ocorrencias=n_nulos,
            campo=campo,
        ))

    merged["classificacao_semantica"] = None
    return merged


# ---------------------------------------------------------------------------
# Etapa E · Camada semântica
# ---------------------------------------------------------------------------


def _etapa_e_camada_semantica(
    base_analitica: pd.DataFrame,
    config: Dict[str, Any],
    t_diag: TDIAG,
) -> pd.DataFrame:
    """Aplica T-SEMA sobre Δ% · classifica POSITIVO/NEGATIVO/NEUTRO/NAO_APLICAVEL."""
    tipo_campo: str = config.get("tipo_campo", "NUMERICO_ADITIVO")
    if tipo_campo == "ESTADO_SITUACAO":
        return base_analitica

    semantica_v2: str = config.get("semantica_campo", "NEUTRO")
    semantica_tsema: str = _SEMA_V2_TO_TSEMA.get(semantica_v2, "NEUTRA")
    limiar: float = float(config.get("thresholds", {}).get("limiar_estabilidade_pct", 0.01))

    def _classif_sem(row: pd.Series) -> Optional[str]:
        vp = row.get("variacao_percentual")
        if vp is None or (isinstance(vp, float) and pd.isna(vp)):
            tipo_estru = "NAO_APLICAVEL"
        elif abs(float(vp)) <= limiar:
            tipo_estru = "ESTAVEL"
        elif float(vp) > limiar:
            tipo_estru = "AUMENTOU"
        else:
            tipo_estru = "REDUZIU"
        label = classificar_semantica(tipo_estru, semantica_tsema)
        return _SEMA_LABEL_TO_CLASS.get(label, "NAO_APLICAVEL")

    base_analitica = base_analitica.copy()
    base_analitica["classificacao_semantica"] = base_analitica.apply(_classif_sem, axis=1)
    return base_analitica


# ---------------------------------------------------------------------------
# Etapa F · Agregações para exportação
# ---------------------------------------------------------------------------


def _etapa_f_agregacoes_resumo(
    base_analitica: pd.DataFrame,
    config: Dict[str, Any],
    t_diag: TDIAG,
) -> Tuple[
    NumerosAncoraV2,
    Optional[Dict[str, int]],
    Optional[Dict[str, float]],
    Optional[Dict[str, Any]],
    Optional[Dict[str, Any]],
    List[LinhaTopVariacao],
    LeituraQualitativa,
    QualidadeEstrutural,
]:
    """Constrói NumerosAncoraV2, distribuições, concentração, onde-se-concentra,
    top_variacoes, leitura qualitativa e qualidade estrutural."""
    tipo_campo: str = config.get("tipo_campo", "NUMERICO_ADITIVO")
    agrupadores: List[str] = config.get("agrupadores", [])
    limiar_variacao: float = float(config.get("thresholds", {}).get("limite_variacao_extrema_pct", 10.0))
    thresholds = config.get("thresholds", {})

    # Distribuição estrutural
    dist_estru: Dict[str, int] = {cat: 0 for cat in _CATS_ESTRUTURAIS}
    if not base_analitica.empty and "classificacao_estrutural" in base_analitica.columns:
        for cat, cnt in base_analitica["classificacao_estrutural"].value_counts().items():
            dist_estru[cat] = int(cnt)

    # NumerosAncoraV2
    if tipo_campo == "ESTADO_SITUACAO":
        pa_mask = base_analitica.get("classificacao_estrutural", pd.Series(dtype=str)) == "PRESENTE_AMBOS"
        total_comb = len(base_analitica)
        pa_rows = base_analitica[pa_mask] if not base_analitica.empty else base_analitica

        mudancas = 0
        estaveis = 0
        if not pa_rows.empty and "estado_origem" in pa_rows.columns and "estado_comparado" in pa_rows.columns:
            mudancas = int(
                (pa_rows["estado_origem"].fillna("") != pa_rows["estado_comparado"].fillna("")).sum()
            )
            estaveis = int(
                (pa_rows["estado_origem"].fillna("") == pa_rows["estado_comparado"].fillna("")).sum()
            )

        pct_mud = (mudancas / total_comb) if total_comb > 0 else 0.0
        ancora = NumerosAncoraV2(
            total_combinacoes_analisadas=total_comb,
            combinacoes_com_mudanca=mudancas,
            combinacoes_estaveis=estaveis,
            pct_mudanca=round(pct_mud, 4),
        )
        dist_sem: Optional[Dict[str, int]] = None
    else:
        if not base_analitica.empty and "valor_origem" in base_analitica.columns:
            vo = base_analitica["valor_origem"].dropna()
            vc = base_analitica["valor_comparado"].dropna()
            total_orig = float(vo.sum()) if len(vo) > 0 else None
            total_comp = float(vc.sum()) if len(vc) > 0 else None
            dif_total: Optional[float] = None
            var_total: Optional[float] = None
            if total_orig is not None and total_comp is not None:
                dif_total = total_comp - total_orig
                if total_orig != 0:
                    var_total = dif_total / total_orig
        else:
            total_orig = None
            total_comp = None
            dif_total = None
            var_total = None

        ancora = NumerosAncoraV2(
            total_origem=total_orig,
            total_comparado=total_comp,
            diferenca_total=dif_total,
            variacao_total_pct=var_total,
        )

        # Distribuição semântica · 7 chaves canônicas (D-187 · NEUTRA preserva
        # AUMENTOU/REDUZIU/ESTAVEL distintos)
        dist_sem = {
            "POSITIVO": 0, "NEGATIVO": 0, "NEUTRO": 0, "NAO_APLICAVEL": 0,
            "AUMENTOU": 0, "REDUZIU": 0, "ESTAVEL": 0,
        }
        if not base_analitica.empty and "classificacao_semantica" in base_analitica.columns:
            for cat, cnt in base_analitica["classificacao_semantica"].value_counts().items():
                if cat and cat in dist_sem:
                    dist_sem[cat] = int(cnt)

    # E2 · Δ por classificacao_semantica (apenas ramo numérico)
    delta_sem: Optional[Dict[str, float]] = None
    if tipo_campo != "ESTADO_SITUACAO":
        delta_sem = {
            "POSITIVO": 0.0, "NEGATIVO": 0.0, "NEUTRO": 0.0, "NAO_APLICAVEL": 0.0,
            "AUMENTOU": 0.0, "REDUZIU": 0.0, "ESTAVEL": 0.0,
        }
        if (
            not base_analitica.empty
            and "diferenca" in base_analitica.columns
            and "classificacao_semantica" in base_analitica.columns
        ):
            grouped = (
                base_analitica.dropna(subset=["diferenca"])
                .groupby("classificacao_semantica")["diferenca"]
                .sum()
            )
            for cat, soma in grouped.items():
                if cat and cat in delta_sem:
                    delta_sem[cat] = float(soma)

    # E3a · Concentração das variações (top 5 e top 10 por |Δ|)
    concentracao: Optional[Dict[str, Any]] = None
    if tipo_campo != "ESTADO_SITUACAO" and not base_analitica.empty and "diferenca" in base_analitica.columns:
        abs_dif = base_analitica["diferenca"].dropna().abs()
        n_pa = int(len(abs_dif))
        total_abs = float(abs_dif.sum())
        if n_pa >= 5 and total_abs > 0:
            top5 = float(abs_dif.nlargest(5).sum() / total_abs)
            top10: Optional[float] = None
            if n_pa >= 10:
                top10 = float(abs_dif.nlargest(10).sum() / total_abs)
            if top5 >= 0.80:
                interp = "alta"
            elif top5 >= 0.50:
                interp = "moderada"
            else:
                interp = "distribuida"
            concentracao = {
                "top_5_pct": round(top5, 4),
                "top_10_pct": round(top10, 4) if top10 is not None else None,
                "n_casos": n_pa,
                "interpretacao": interp,
            }

    # E3b · Onde se concentra · top 3 categorias do agrupador destacado
    onde_se_concentra: Optional[Dict[str, Any]] = None
    if tipo_campo != "ESTADO_SITUACAO" and not base_analitica.empty and "diferenca" in base_analitica.columns:
        agrupador_dest = _resolver_agrupador_destacado(agrupadores, config)
        if agrupador_dest and agrupador_dest in base_analitica.columns:
            grouped = (
                base_analitica.dropna(subset=["diferenca"])
                .groupby(agrupador_dest, dropna=False)["diferenca"]
                .agg(["sum", "count"])
                .reset_index()
            )
            if not grouped.empty:
                grouped = grouped.rename(columns={"sum": "_sum", "count": "_count"})
                grouped["_abs"] = grouped["_sum"].abs()
                grouped = grouped.sort_values("_abs", ascending=False).reset_index(drop=True)

                # Soma absoluta de origem por categoria, para calcular variação relativa
                vo_por_cat: Dict[Any, float] = {}
                if "valor_origem" in base_analitica.columns:
                    vo_por_cat = (
                        base_analitica.groupby(agrupador_dest, dropna=False)["valor_origem"]
                        .sum(min_count=1)
                        .to_dict()
                    )

                top3_df = grouped.head(3)
                outras_df = grouped.iloc[3:]
                top: List[Dict[str, Any]] = []
                for _, row in top3_df.iterrows():
                    cat = row[agrupador_dest]
                    delta_sum = float(row["_sum"])
                    count_cat = int(row["_count"]) if not pd.isna(row["_count"]) else 0
                    delta_medio = (delta_sum / count_cat) if count_cat > 0 else 0.0
                    base_orig = vo_por_cat.get(cat, None)
                    var_rel: Optional[float] = None
                    if base_orig is not None and not pd.isna(base_orig) and base_orig != 0:
                        var_rel = float(delta_sum / base_orig)
                    cat_render = (
                        "(sem categoria)" if (cat is None or (isinstance(cat, float) and pd.isna(cat)))
                        else str(cat)
                    )
                    # `delta` preserva soma (compatibilidade legada) ·
                    # F-APRESENT escolhe `delta_soma` ou `delta_medio`
                    # conforme unidade.
                    top.append({
                        "categoria": cat_render,
                        "delta": delta_sum,
                        "delta_soma": delta_sum,
                        "delta_medio": delta_medio,
                        "count": count_cat,
                        "variacao_relativa": var_rel,
                    })
                outras_count = int(len(outras_df))
                outras_delta_soma = float(outras_df["_sum"].sum()) if outras_count > 0 else 0.0
                outras_count_obs = int(outras_df["_count"].sum()) if outras_count > 0 else 0
                outras_delta_medio = (
                    outras_delta_soma / outras_count_obs if outras_count_obs > 0 else 0.0
                )
                # outras_dominante: |soma das outras| supera o |delta| do menor top 3
                outras_dominante = False
                if outras_count > 0 and len(top3_df) > 0:
                    menor_top = float(top3_df["_abs"].min())
                    if abs(outras_delta_soma) > menor_top:
                        outras_dominante = True
                onde_se_concentra = {
                    "agrupador": agrupador_dest,
                    "top": top,
                    "outras_count": outras_count,
                    "outras_delta_soma": outras_delta_soma,
                    "outras_delta_medio": outras_delta_medio,
                    "outras_dominante": outras_dominante,
                }

    # Top 10 variações
    top_variacoes: List[LinhaTopVariacao] = []
    if not base_analitica.empty:
        if tipo_campo == "ESTADO_SITUACAO":
            # Top 10 mudanças de estado
            pa_mask = base_analitica.get("classificacao_estrutural", pd.Series(dtype=str)) == "PRESENTE_AMBOS"
            if pa_mask.any():
                mudou_mask = (
                    base_analitica.loc[pa_mask, "estado_origem"].fillna("")
                    != base_analitica.loc[pa_mask, "estado_comparado"].fillna("")
                )
                top_df = base_analitica[pa_mask][mudou_mask].head(10)
            else:
                top_df = pd.DataFrame()
        else:
            if "diferenca" in base_analitica.columns:
                top_df = (
                    base_analitica.dropna(subset=["diferenca"])
                    .assign(_abs_dif=lambda d: d["diferenca"].abs())
                    .sort_values("_abs_dif", ascending=False)
                    .drop(columns=["_abs_dif"])
                    .head(10)
                )
            else:
                top_df = pd.DataFrame()

        def _safe_float(v: Any) -> Optional[float]:
            if v is None:
                return None
            try:
                return None if pd.isna(float(v)) else float(v)
            except (TypeError, ValueError):
                return None

        def _safe_opt_str(v: Any) -> Optional[str]:
            if v is None:
                return None
            try:
                if pd.isna(v):
                    return None
            except (TypeError, ValueError):
                pass
            return str(v)

        for _, row in top_df.iterrows():
            chave = {k: row[k] for k in agrupadores if k in row.index}
            top_variacoes.append(LinhaTopVariacao(
                chave_agrupadores=chave,
                valor_origem=_safe_float(row.get("valor_origem")),
                valor_comparado=_safe_float(row.get("valor_comparado")),
                diferenca=_safe_float(row.get("diferenca")),
                variacao_percentual=_safe_float(row.get("variacao_percentual")),
                classificacao_estrutural=str(row.get("classificacao_estrutural", "PRESENTE_AMBOS")),
                classificacao_semantica=_safe_opt_str(row.get("classificacao_semantica")),
                estado_origem=_safe_opt_str(row.get("estado_origem")),
                estado_comparado=_safe_opt_str(row.get("estado_comparado")),
            ))

    # LeituraQualitativa
    classif_ativa = "Resultado Estável"
    if tipo_campo != "ESTADO_SITUACAO" and dist_sem is not None:
        total_class = sum(dist_sem.values())
        if total_class > 0:
            pct_pos = dist_sem.get("POSITIVO", 0) / total_class
            pct_neg = dist_sem.get("NEGATIVO", 0) / total_class
            if pct_pos >= 0.60:
                classif_ativa = "Melhoria Geral"
            elif pct_neg >= 0.60:
                classif_ativa = "Deterioração Geral"
            elif pct_pos > 0 or pct_neg > 0:
                classif_ativa = "Resultado Misto"
    elif tipo_campo == "ESTADO_SITUACAO":
        if ancora.pct_mudanca is not None and ancora.pct_mudanca > 0.5:
            classif_ativa = "Alta Taxa de Mudança de Estado"
        elif ancora.pct_mudanca is not None and ancora.pct_mudanca > 0:
            classif_ativa = "Mudanças Parciais"
        else:
            classif_ativa = "Estados Estáveis"

    leitura = LeituraQualitativa(
        classificacao_ativa=classif_ativa,
        thresholds_usados={
            k: float(v) for k, v in (thresholds or {}).items() if isinstance(v, (int, float))
        },
        alguma_leitura_alterada_por_edicao=False,
    )

    # Saneamento · garantir tipos serializáveis JSON
    if onde_se_concentra and "outras_count" in onde_se_concentra:
        onde_se_concentra["outras_count"] = int(onde_se_concentra["outras_count"])

    # QualidadeEstrutural
    diag_parcial = t_diag.consolidar()
    warns_flat = _flatten_warnings(diag_parcial)
    warns_por_cat: Dict[str, int] = {}
    for w in warns_flat:
        cat = w.categoria.value if hasattr(w.categoria, "value") else str(w.categoria)
        warns_por_cat[cat] = warns_por_cat.get(cat, 0) + 1
    qualidade = QualidadeEstrutural(
        total_warnings=len(warns_flat),
        warnings_por_categoria=warns_por_cat,
        ajustes_aplicados=len(diag_parcial.ajustes_aplicados),
        tem_bloqueios_escapados=False,
    )

    return (
        ancora,
        dist_sem,
        delta_sem,
        concentracao,
        onde_se_concentra,
        top_variacoes,
        leitura,
        qualidade,
    )


# ---------------------------------------------------------------------------
# Função pública principal
# ---------------------------------------------------------------------------


def executar_v2(
    motor_result: MotorResult,
    config: Dict[str, Any],
) -> V2Result:
    """
    Pipeline canônico V2 · 6 etapas A-F · Spec §2.1.
    Determinístico (C.1) · zero invenção de comportamento (C.3) · nada silencioso (C.2).
    """
    t_diag = TDIAG("V2")
    bloqueios: List[BloqueioOperacional] = []

    agrupadores: List[str] = config.get("agrupadores", [])
    tipo_campo: str = config.get("tipo_campo", "NUMERICO_ADITIVO")
    metodo_consol: Optional[str] = config.get("metodo_consolidacao_relativo")
    thresholds: Dict[str, Any] = config.get("thresholds", {})

    # ---- Verificações iniciais de bloqueio ----

    # B-V2-AGRUP-EXCESSO
    if len(agrupadores) >= 10:
        bloqueios.append(BloqueioOperacional(
            codigo="B-V2-AGRUP-EXCESSO",
            condicao_disparo=(
                f"V2 não opera com {len(agrupadores)} agrupadores (máximo: 9). "
                "Use a V6 para análise de relacionamento entre dimensões."
            ),
            escapavel=False,
            escape_acionado=None,
            warning_pos_escape=None,
            contexto_disparo={"n_agrupadores": len(agrupadores), "sugestao_v6": True},
        ))
        return _resultado_bloqueado(motor_result, config, t_diag, bloqueios)

    # B-V2-CONSOL-IMPOSSIVEL
    if metodo_consol == "NAO_CONSOLIDAR" and len(agrupadores) > 0:
        bloqueios.append(BloqueioOperacional(
            codigo="B-V2-CONSOL-IMPOSSIVEL",
            condicao_disparo=(
                f"Método 'NAO_CONSOLIDAR' é incompatível com agrupadores declarados: {agrupadores}."
            ),
            escapavel=False,
            escape_acionado=None,
            warning_pos_escape=None,
            contexto_disparo={
                "campo": config.get("campo_analisado", ""),
                "agrupadores_declarados": agrupadores,
            },
        ))
        return _resultado_bloqueado(motor_result, config, t_diag, bloqueios)

    # ---- T-MODELO (opcional) ----
    modelo_config_raw: Optional[Dict[str, Any]] = config.get("modelo_aplicado")
    modelo_aplicado_v2: Optional[ModeloAplicadoV2] = None
    if modelo_config_raw and isinstance(modelo_config_raw, dict):
        modelo_id = modelo_config_raw.get("modelo_id", "")
        try:
            config_modelo, warns_modelo = aplicar_modelo(modelo_id, "V2", None)
            # Verificar compatibilidade de campos com colunas disponíveis
            colunas_df = set(motor_result.df.columns)
            campos_modelo = list(config_modelo.get("agrupadores", [])) + list(
                config_modelo.get("campos_principais", {}).values()
            )
            campos_nao_casados = [c for c in campos_modelo if c and c not in colunas_df]
            campos_casados = len(campos_modelo) - len(campos_nao_casados)

            if campos_nao_casados:
                tipo_ap: Literal["COMPLETA", "PARCIAL", "INCOMPATIVEL"] = "PARCIAL"
                t_diag.registrar_warning(TDIAG.w(
                    "W-V2-MOD-PARCIAL",
                    CategoriaWarning.INFORMATIVO,
                    f"Modelo aplicado com {len(campos_nao_casados)} campo(s) não encontrado(s) "
                    f"na base atual: {campos_nao_casados}.",
                    campos_nao_casados=campos_nao_casados,
                ))
            else:
                tipo_ap = "COMPLETA"

            modelo_salvo = None
            from transversais.t_modelo import _STORE as _MODELO_STORE
            modelo_salvo = _MODELO_STORE.get(modelo_id)

            modelo_aplicado_v2 = ModeloAplicadoV2(
                nome_modelo=modelo_salvo.nome_modelo if modelo_salvo else modelo_id,
                data_criacao_modelo=modelo_salvo.data_criacao if modelo_salvo else datetime.now(),
                campos_casados=max(0, campos_casados),
                campos_nao_casados=campos_nao_casados,
                tipo_aplicacao=tipo_ap,
            )
            if tipo_ap == "INCOMPATIVEL":
                t_diag.registrar_warning(TDIAG.w(
                    "W-V2-MOD-INCOMP",
                    CategoriaWarning.ALERTA_ESTRUTURAL,
                    "Modelo aplicado incompatível com a estrutura atual — etapas dependentes zeradas.",
                    modelo_id=modelo_id,
                ))

        except (KeyError, ValueError) as exc:
            t_diag.registrar_warning(TDIAG.w(
                "W-V2-MOD-INCOMP",
                CategoriaWarning.ALERTA_ESTRUTURAL,
                f"Modelo '{modelo_id}' incompatível ou não encontrado: {exc}",
                modelo_id=modelo_id,
            ))
            modelo_aplicado_v2 = ModeloAplicadoV2(
                nome_modelo=modelo_id,
                data_criacao_modelo=datetime.now(),
                campos_casados=0,
                campos_nao_casados=[],
                tipo_aplicacao="INCOMPATIVEL",
            )

    # ---- Etapa A ----
    df, bl_a = _etapa_a_preparar_base(motor_result, config, t_diag)
    if bl_a:
        bloqueios.extend(bl_a)
        return _resultado_bloqueado(motor_result, config, t_diag, bloqueios)

    # ---- Etapa B ----
    resolucao, bl_b = _etapa_b_detectar_casos_estruturais(df, config, t_diag)
    if bl_b:
        bloqueios.extend(bl_b)
        return _resultado_bloqueado(motor_result, config, t_diag, bloqueios)

    # ---- Etapa C ----
    df_orig, df_comp, bl_c = _etapa_c_consolidar_pre_calculo(df, config, t_diag)
    if bl_c or df_orig is None or df_comp is None:
        bloqueios.extend(bl_c or [])
        return _resultado_bloqueado(motor_result, config, t_diag, bloqueios)

    # B-V2-RESULTADO-EXCEDE (pré-join · estimativa conservadora n_orig × n_comp)
    _n_orig = len(df_orig)
    _n_comp = len(df_comp)
    _estimado = _n_orig * _n_comp
    if _estimado > 500_000:
        bloqueios.append(BloqueioOperacional(
            codigo="B-V2-RESULTADO-EXCEDE",
            condicao_disparo=(
                f"Estimativa de {_estimado:,} combinações ({_n_orig} × {_n_comp}) "
                "excede o limite de 500.000 linhas."
            ),
            escapavel=False,
            escape_acionado=None,
            warning_pos_escape=None,
            contexto_disparo={"linhas_estimadas": _estimado, "limite": 500_000},
        ))
        return _resultado_bloqueado(motor_result, config, t_diag, bloqueios)

    # ---- Etapa D ----
    base_analitica = _etapa_d_calcular_comparativo(df_orig, df_comp, config, t_diag)

    # ---- Etapa E ----
    base_analitica = _etapa_e_camada_semantica(base_analitica, config, t_diag)

    # ---- Etapa F ----
    (
        ancora,
        dist_sem,
        delta_sem,
        concentracao,
        onde_se_concentra,
        top_variacoes,
        leitura_qual,
        qualidade_est,
    ) = _etapa_f_agregacoes_resumo(base_analitica, config, t_diag)

    # ---- Consolidar diagnóstico final ----
    diagnostico = t_diag.consolidar()
    warns_finais = _flatten_warnings(diagnostico)

    # ---- Distribuição estrutural ----
    dist_estru: Dict[str, int] = {cat: 0 for cat in _CATS_ESTRUTURAIS}
    if "classificacao_estrutural" in base_analitica.columns:
        for cat, cnt in base_analitica["classificacao_estrutural"].value_counts().items():
            dist_estru[str(cat)] = int(cnt)

    # ---- Resumo Executivo (6 blocos) ----
    resumo = ResumoExecutivoPadrao(
        bloco_1_cabecalho=CabecalhoExecucao(
            visao="V2",
            modo_upload=motor_result.modo_upload,
            agrupadores=agrupadores,
            medida_principal=config.get("campo_analisado"),
        ),
        bloco_2_numeros_ancora=ancora.model_dump(exclude_none=True),
        bloco_3_distribuicao=dist_estru,
        bloco_4_elementos_destacados={"top_variacoes": [t.model_dump() for t in top_variacoes]},
        bloco_5_leitura_qualitativa=leitura_qual,
        bloco_6_qualidade_estrutural=qualidade_est,
    )

    comparacao = _make_comparacao_from_config(config)

    return V2Result(
        visao_id="V2",
        config_usada=config,
        motor_result_meta=_make_motor_meta(motor_result),
        timestamp_execucao=datetime.now(),
        base_analitica=base_analitica,
        resumo_executivo=resumo,
        coracao_visual=CoracaoVisualRef(
            nome_aba="Matriz de Confronto",
            tipo="MATRIZ_COLORIDA",
            capabilities_requeridas=["formatacao_condicional", "congelar_paineis"],
        ),
        bloqueios_disparados=bloqueios,
        warnings=warns_finais,
        diagnostico=diagnostico,
        comparacao_realizada=comparacao,
        agrupadores_aplicados=agrupadores,
        resolucao_estrutural=resolucao,
        distribuicao_classificacoes_estruturais=dist_estru,
        distribuicao_classificacoes_semanticas=dist_sem,
        delta_por_classificacao_semantica=delta_sem,
        concentracao=concentracao,
        onde_se_concentra=onde_se_concentra,
        numeros_ancora=ancora,
        top_variacoes=top_variacoes,
        modelo_aplicado=modelo_aplicado_v2,
    )
