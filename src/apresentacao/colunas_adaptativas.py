"""
F-APRESENT · capability 6 · Colunas adaptativas (D-166 req 2).

Abas tabulares montadas dinamicamente conforme V{N}Result.config_usada.
Declaração das colunas é pura (funções `condicao`, sem side effects) ·
avaliação é determinística (C.1).

Helpers de condição cobrem 90% dos casos · lambdas ad-hoc cobrem o resto.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Literal, Optional


_logger = logging.getLogger(__name__)


UnidadeCampo = Literal[
    "monetario",
    "percentual",
    "contagem",
    "texto",
    "data",
    "classificacao",
    "booleano",
]

FuncaoTotalColuna = Literal[
    "sum", "average", "count", "countNums",
    "min", "max", "stdDev", "var", "custom", "none",
]

CondicaoInclusao = Callable[[Dict[str, Any]], bool]


@dataclass(frozen=True)
class ColunaAdaptativa:
    """
    Declaração de uma coluna no esquema de exportação de uma visão.

    Consumida por F-APRESENT capability 6. Condicional na config usada
    pela execução · avaliada em tempo de montagem (não de declaração).
    """
    identificador: str
    cabecalho_user_facing: str
    unidade: UnidadeCampo
    condicao: CondicaoInclusao
    funcao_total: FuncaoTotalColuna = "none"
    custom_total_formula: Optional[str] = None
    ordem_sugerida: int = 100


def sempre() -> CondicaoInclusao:
    """Condição helper: coluna sempre incluída."""
    return lambda cfg: True


def se_config_igual(chave: str, valor: Any) -> CondicaoInclusao:
    """Condição helper: incluir se config_usada[chave] == valor."""
    return lambda cfg: cfg.get(chave) == valor


def se_config_diferente(chave: str, valor: Any) -> CondicaoInclusao:
    """Condição helper: incluir se config_usada[chave] != valor."""
    return lambda cfg: cfg.get(chave) != valor


def se_config_presente(chave: str) -> CondicaoInclusao:
    """Condição helper: incluir se chave existe em config_usada com valor truthy."""
    return lambda cfg: bool(cfg.get(chave))


def montar_colunas_adaptativas(
    config_usada: Dict[str, Any],
    esquema_colunas: List[ColunaAdaptativa],
) -> List[ColunaAdaptativa]:
    """
    Avalia cada ColunaAdaptativa.condicao contra config_usada.

    Propriedades:
      - Determinístico (C.1) · mesma entrada produz mesma ordem
      - Ordem: sort estável por ordem_sugerida · ordem de declaração desempata
      - Lista vazia resultante emite warning (provável bug de config/declaração)

    Retorna subset ordenado.
    """
    if not isinstance(esquema_colunas, list):
        raise TypeError("esquema_colunas deve ser lista de ColunaAdaptativa")
    if not isinstance(config_usada, dict):
        raise TypeError("config_usada deve ser dict")

    incluidas: List[tuple[int, int, ColunaAdaptativa]] = []
    for indice, coluna in enumerate(esquema_colunas):
        try:
            incluir = bool(coluna.condicao(config_usada))
        except Exception as exc:
            _logger.warning(
                "condicao da coluna '%s' levantou exceção %s · excluindo coluna (C.2)",
                coluna.identificador, exc,
            )
            continue
        if incluir:
            incluidas.append((coluna.ordem_sugerida, indice, coluna))

    incluidas.sort(key=lambda t: (t[0], t[1]))
    resultado = [t[2] for t in incluidas]

    if not resultado:
        _logger.warning(
            "montar_colunas_adaptativas retornou lista vazia · "
            "config_usada=%s · esquema com %d colunas",
            config_usada, len(esquema_colunas),
        )
    return resultado
