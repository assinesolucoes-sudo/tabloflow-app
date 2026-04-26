"""
t_modelo.py — Persistência de configuração com TED obrigatório · T-MODELO · D-015 · F.2
Todas as 11 visões. Cross-visão em view especializada (D-046 · V4 Modo 2 ↔ V10).
Armazenamento: JSON em memória (MVP · sessão Streamlit).
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Tuple

from pydantic import BaseModel, Field

from contratos import CategoriaWarning, UploadResult, WarningEstrutural

# Cross-visão permitida: D-046
_CROSS_VISAO_PERMITIDA: Dict[str, str] = {
    "V4": "V10",
    "V10": "V4",
}


class ThresholdEditavel(BaseModel):
    valor_default: float = Field(..., description="Default original")
    valor_atual: float = Field(..., description="Aplicado · igual ao default ou editado")
    range_permitido: Tuple[float, float] = Field(..., description="Limites editáveis")
    unidade: Optional[Literal["percentual", "absoluto", "multiplicador"]] = None
    descricao_uso: str = Field(..., description="Microcopy para auditoria")
    foi_editado: bool = Field(False)


class ModeloConfig(BaseModel):
    nome_modelo: str = Field(..., description="Nome editável · chave de identificação")
    descricao: Optional[str] = Field(None, description="Opcional · até 500 chars")
    visao_origem: Literal["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11"]
    modo_da_visao: Optional[str] = None
    data_criacao: datetime = Field(default_factory=datetime.now)
    data_ultima_aplicacao: Optional[datetime] = None
    versao_contrato: str = Field("1.0")

    agrupadores: List[str] = Field(default_factory=list)
    campos_principais: Dict[str, str] = Field(default_factory=dict)
    configuracoes_visao: Dict[str, Any] = Field(default_factory=dict)
    thresholds_editaveis: Dict[str, ThresholdEditavel] = Field(default_factory=dict)

    config_t_rank: Optional[Dict] = None
    config_t_agrupa_por_metrica: Optional[Dict] = None
    config_eixo: Optional[Dict] = None
    campos_declarados_por_lado: Optional[Dict] = None


# Armazenamento em memória (MVP)
_STORE: Dict[str, ModeloConfig] = {}


def salvar_modelo(config: ModeloConfig) -> str:
    """Salva modelo e retorna ID canônico."""
    modelo_id = str(uuid.uuid4())
    _STORE[modelo_id] = config
    return modelo_id


def aplicar_modelo(
    modelo_id: str,
    visao_destino: str,
    upload_atual: Optional[UploadResult] = None,
) -> Tuple[Dict[str, Any], List[WarningEstrutural]]:
    """
    Aplica modelo salvo em nova base/visão.
    Retorna (configuração pré-preenchida, warnings).

    Cenários:
      - Estrutura incompatível → BloqueioOperacional como ValueError.
      - Campos parcialmente incompatíveis → W-MOD-PARCIAL.
      - Threshold fora de range → W-MOD-THRESHOLD-FORA-RANGE + reset ao default.
    """
    warnings: List[WarningEstrutural] = []

    if modelo_id not in _STORE:
        raise KeyError(f"Modelo '{modelo_id}' não encontrado.")

    modelo = _STORE[modelo_id]

    # Verifica compatibilidade estrutural
    visao_orig = modelo.visao_origem
    cross_permitida = _CROSS_VISAO_PERMITIDA.get(visao_orig)

    if visao_orig != visao_destino:
        if cross_permitida != visao_destino:
            raise ValueError(
                f"B-T-MODELO-ESTRUTURA-INCOMPATIVEL: "
                f"Modelo criado para {visao_orig} não pode ser aplicado em {visao_destino}."
            )
        # Cross-visão permitida: D-046
        warnings.append(WarningEstrutural(
            codigo=f"W-V{visao_destino}-MOD-CROSS-VISAO",
            categoria=CategoriaWarning.INFORMATIVO,
            microcopy=f"Modelo de {visao_orig} aplicado em {visao_destino} (view especializada).",
            contexto={"visao_origem": visao_orig, "visao_destino": visao_destino},
        ))

    # Verifica compatibilidade de campos com upload_atual
    campos_incompativeis: List[str] = []
    if upload_atual is not None:
        # Obtém colunas disponíveis na base atual
        colunas_disponiveis: set = set()
        if upload_atual.arquivo_unico:
            colunas_disponiveis = set(upload_atual.arquivo_unico.preview.keys())
        elif upload_atual.arquivos_dual:
            for arq in upload_atual.arquivos_dual:
                colunas_disponiveis.update(arq.preview.keys())

        # Verifica agrupadores e campos principais
        todos_campos = list(modelo.agrupadores) + list(modelo.campos_principais.values())
        campos_incompativeis = [c for c in todos_campos if c and c not in colunas_disponiveis]

    if campos_incompativeis:
        warnings.append(WarningEstrutural(
            codigo=f"W-V{visao_destino}-MOD-PARCIAL",
            categoria=CategoriaWarning.INFORMATIVO,
            microcopy=f"Campos do modelo não encontrados na base atual: {campos_incompativeis}. "
                      "Ajuste manualmente.",
            contexto={"campos_incompativeis": campos_incompativeis},
        ))

    # Verifica thresholds fora de range
    thresholds_ajustados: Dict[str, ThresholdEditavel] = {}
    for nome, thr in modelo.thresholds_editaveis.items():
        val = thr.valor_atual
        lo, hi = thr.range_permitido
        if not (lo <= val <= hi):
            warnings.append(WarningEstrutural(
                codigo=f"W-V{visao_destino}-MOD-THRESHOLD-FORA-RANGE",
                categoria=CategoriaWarning.ALERTA_ESTRUTURAL_LEVE,
                microcopy=f"Threshold '{nome}' = {val} fora do range [{lo}, {hi}]. "
                          f"Resetado para default {thr.valor_default}.",
                contexto={"nome": nome, "valor_salvo": val, "range": [lo, hi], "default": thr.valor_default},
            ))
            thresholds_ajustados[nome] = thr.model_copy(
                update={"valor_atual": thr.valor_default, "foi_editado": False}
            )
        else:
            thresholds_ajustados[nome] = thr

    config_preenchida: Dict[str, Any] = {
        "agrupadores": list(modelo.agrupadores),
        "campos_principais": dict(modelo.campos_principais),
        "configuracoes_visao": dict(modelo.configuracoes_visao),
        "thresholds_editaveis": {k: v.model_dump() for k, v in thresholds_ajustados.items()},
        "modo_da_visao": modelo.modo_da_visao,
        "campos_incompativeis": campos_incompativeis,
    }
    if modelo.config_t_rank:
        config_preenchida["config_t_rank"] = modelo.config_t_rank
    if modelo.config_t_agrupa_por_metrica:
        config_preenchida["config_t_agrupa_por_metrica"] = modelo.config_t_agrupa_por_metrica
    if modelo.config_eixo:
        config_preenchida["config_eixo"] = modelo.config_eixo

    # Atualiza data de última aplicação
    _STORE[modelo_id] = modelo.model_copy(
        update={"data_ultima_aplicacao": datetime.now()}
    )

    return config_preenchida, warnings


def listar_modelos_aplicaveis(
    visao: str,
    upload_atual: Optional[UploadResult] = None,
) -> List[ModeloConfig]:
    """Retorna modelos compatíveis com a visão atual."""
    cross_aceita = _CROSS_VISAO_PERMITIDA.get(visao)
    resultado = []
    for modelo in _STORE.values():
        if modelo.visao_origem == visao or modelo.visao_origem == cross_aceita:
            resultado.append(modelo)
    return sorted(resultado, key=lambda m: m.data_criacao)


def limpar_store() -> None:
    """Limpa o store em memória · uso exclusivo em testes."""
    _STORE.clear()
