"""
t_sema.py — Classificação semântica maior/menor/neutro · T-SEMA · D-067 · D-087
2 contratos:
  (1) classificar_semantica — semântica única · V3/V7
  (2) classificar_semantica_por_metrica — semântica por Dict · V9
"""
from __future__ import annotations

from typing import Dict, List, Literal, Tuple

from contratos import CategoriaWarning, WarningEstrutural

TipoEstrutural = Literal["AUMENTOU", "REDUZIU", "ESTAVEL", "NAO_APLICAVEL"]
TipoSemantica = Literal["MAIOR_MELHOR", "MENOR_MELHOR", "NEUTRA"]

# Tabela determinística · D-067
_TABELA: Dict[Tuple[str, str], str] = {
    ("AUMENTOU", "MAIOR_MELHOR"): "Melhorou",
    ("AUMENTOU", "MENOR_MELHOR"): "Piorou",
    ("AUMENTOU", "NEUTRA"): "Aumentou",
    ("REDUZIU", "MAIOR_MELHOR"): "Piorou",
    ("REDUZIU", "MENOR_MELHOR"): "Melhorou",
    ("REDUZIU", "NEUTRA"): "Reduziu",
    ("ESTAVEL", "MAIOR_MELHOR"): "Estável",
    ("ESTAVEL", "MENOR_MELHOR"): "Estável",
    ("ESTAVEL", "NEUTRA"): "Estável",
    ("NAO_APLICAVEL", "MAIOR_MELHOR"): "Não aplicável",
    ("NAO_APLICAVEL", "MENOR_MELHOR"): "Não aplicável",
    ("NAO_APLICAVEL", "NEUTRA"): "Não aplicável",
}


def classificar_semantica(
    estrutural: TipoEstrutural,
    semantica: TipoSemantica,
) -> str:
    """
    Contrato 1 · semântica única.
    Retorna rótulo qualitativo determinístico.
    """
    return _TABELA[(estrutural, semantica)]


class ResultadoMetrica:
    """Placeholder · consumidor passa resultado estrutural por métrica."""
    def __init__(self, estrutural: TipoEstrutural) -> None:
        self.estrutural = estrutural


def classificar_semantica_por_metrica(
    resultados: Dict[str, "ResultadoMetrica"],
    semanticas: Dict[str, TipoSemantica],
) -> Tuple[Dict[str, str], List[WarningEstrutural]]:
    """
    Contrato 2 · semântica por métrica · D-087 · D-095.
    Métrica sem semântica declarada recebe NEUTRA + warning W-T-SEMA-METRICA-SEM-SEMANTICA.
    Retorna (Dict[metrica, rótulo], warnings).
    """
    warnings: List[WarningEstrutural] = []
    resultado: Dict[str, str] = {}

    metricas_sem_semantica: List[str] = []

    for metrica, res in resultados.items():
        sem = semanticas.get(metrica)
        if sem is None:
            sem = "NEUTRA"
            metricas_sem_semantica.append(metrica)
        resultado[metrica] = classificar_semantica(res.estrutural, sem)

    if metricas_sem_semantica:
        warnings.append(WarningEstrutural(
            codigo="W-T-SEMA-METRICA-SEM-SEMANTICA",
            categoria=CategoriaWarning.INFORMATIVO,
            microcopy=(
                f"Métricas sem semântica declarada · default NEUTRA aplicado: "
                f"{sorted(metricas_sem_semantica)}"
            ),
            contexto={"metricas": sorted(metricas_sem_semantica)},
        ))

    return resultado, warnings
