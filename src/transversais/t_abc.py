"""
t_abc.py — Classificação ABC por limiares de acumulado · T-ABC · D-040 · E.4
Defaults TED 80%/95% editáveis. Modo DICOTOMICO_V10 (D-045).
"""
from __future__ import annotations

from typing import Dict, List, Literal, Optional, Tuple

import pandas as pd
from pydantic import BaseModel, Field

from contratos import CategoriaWarning, WarningEstrutural


class ConfigABC(BaseModel):
    coluna_acumulado: str = Field(
        ..., description="Coluna produzida por T-ACUM · participacao_acumulada"
    )
    limiar_A: float = Field(80.0, description="TED · default 80% · range 50-95%")
    limiar_B: float = Field(95.0, description="TED · default 95% · range limiar_A+1% até 99%")
    modo: Literal["ABC_COMPLETO", "DICOTOMICO_V10"] = Field("ABC_COMPLETO")
    coluna_grupo_para_limiares_globais: Optional[str] = Field(
        None, description="V4 Modo 3 · limiares cross-medida"
    )
    coluna_rank: Optional[str] = Field(None, description="Para ordenação ao classificar")


class ABCResult(BaseModel):
    coluna_classe_adicionada: str
    contagem_por_classe: Dict[str, int]
    limiar_A_aplicado: float
    limiar_B_aplicado: float
    warnings_gerados: List[WarningEstrutural]


def aplicar_abc(
    df: pd.DataFrame,
    config: ConfigABC,
    nome_visao: str,
    nome_coluna_classe: str = "classe_abc",
) -> Tuple[pd.DataFrame, ABCResult]:
    """
    Classifica linhas em A/B/C (ou VITAL/DEMAIS em modo V10) por limiar de acumulado.
    Pré-condição: coluna_acumulado já calculada por T-ACUM.

    Bloqueio: limiar_A >= limiar_B → ValueError.
    """
    warnings: List[WarningEstrutural] = []

    # Validação de limiares
    limiar_B_efetivo = 100.0 if config.modo == "DICOTOMICO_V10" else config.limiar_B
    if config.limiar_A >= limiar_B_efetivo:
        raise ValueError(
            f"B-V{nome_visao}-ABC-LIMIARES-INVALIDOS: "
            f"limiar_A ({config.limiar_A}) >= limiar_B ({limiar_B_efetivo}). "
            "Classifique A < B para garantir ordenação válida."
        )

    # Warnings TED
    if config.limiar_A != 80.0:
        warnings.append(WarningEstrutural(
            codigo=f"W-V{nome_visao}-ABC-LIMIAR-CUSTOM",
            categoria=CategoriaWarning.INFORMATIVO,
            microcopy=f"Limiar A editado de 80% para {config.limiar_A}%.",
            contexto={"limiar_A": config.limiar_A, "default": 80.0},
        ))
    if config.modo == "ABC_COMPLETO" and config.limiar_B != 95.0:
        warnings.append(WarningEstrutural(
            codigo=f"W-V{nome_visao}-ABC-LIMIAR-B-CUSTOM",
            categoria=CategoriaWarning.INFORMATIVO,
            microcopy=f"Limiar B editado de 95% para {config.limiar_B}%.",
            contexto={"limiar_B": config.limiar_B, "default": 95.0},
        ))

    df_resultado = df.copy()

    # Ordena pelo rank se disponível
    if config.coluna_rank and config.coluna_rank in df_resultado.columns:
        df_resultado = df_resultado.sort_values(config.coluna_rank).reset_index(drop=True)

    def _classificar_linha(acum: float) -> str:
        if acum <= config.limiar_A or (acum - config.limiar_A) < 1e-9:
            return "A" if config.modo == "ABC_COMPLETO" else "VITAL"
        if acum <= limiar_B_efetivo or (acum - limiar_B_efetivo) < 1e-9:
            return "B" if config.modo == "ABC_COMPLETO" else "DEMAIS"
        return "C" if config.modo == "ABC_COMPLETO" else "DEMAIS"

    df_resultado[nome_coluna_classe] = df_resultado[config.coluna_acumulado].apply(_classificar_linha)

    contagem = df_resultado[nome_coluna_classe].value_counts().to_dict()

    # Alerta classe vazia
    if config.modo == "ABC_COMPLETO":
        for cls in ("A", "B"):
            if contagem.get(cls, 0) == 0:
                warnings.append(WarningEstrutural(
                    codigo=f"W-V{nome_visao}-ABC-CLASSE-VAZIA",
                    categoria=CategoriaWarning.ALERTA_ESTRUTURAL,
                    microcopy=f"Classe {cls} ficou vazia. Distribuição muito pulverizada.",
                    contexto={"classe_vazia": cls},
                ))

    return df_resultado, ABCResult(
        coluna_classe_adicionada=nome_coluna_classe,
        contagem_por_classe=dict(sorted(contagem.items())),
        limiar_A_aplicado=config.limiar_A,
        limiar_B_aplicado=limiar_B_efetivo,
        warnings_gerados=warnings,
    )
