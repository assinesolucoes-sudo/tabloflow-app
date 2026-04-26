"""
t_concat.py — Composição declarada de campos-fonte · T-CONCAT · D-053/D-135 · F.4
Até 3 campos-fonte · separador fixo espaço · nulos pulados.
Normalização via normalizacao_texto.py · D-139.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import List, Literal, Optional, Tuple

import pandas as pd
from pydantic import BaseModel, Field, field_validator

sys.path.insert(0, str(Path(__file__).parent.parent))

from contratos import CategoriaWarning, WarningEstrutural
from utils.normalizacao_texto import normalizar_texto


class ConfigConcat(BaseModel):
    campos_fonte: List[str] = Field(
        ...,
        min_length=1,
        max_length=3,
        description="Até 3 campos-fonte · D-053/D-135",
    )
    separador: Literal[" "] = Field(" ", description="Separador fixo espaço · D-135")
    normalizar: bool = Field(
        False,
        description="Se True, aplica normalização para alimentar T-FUZZY",
    )
    tratamento_nulos: Literal["PULAR"] = Field("PULAR", description="D-135 · nulos pulados")


class ConcatResult(BaseModel):
    coluna_concatenada_nome: str
    valores_gerados: int
    valores_vazios_todos_nulos: int
    valores_parcialmente_nulos: int
    warnings_gerados: List[WarningEstrutural]


def aplicar_concat(
    df: pd.DataFrame,
    config: ConfigConcat,
    nome_visao: str,
    nome_coluna_resultado: Optional[str] = None,
) -> Tuple[pd.DataFrame, ConcatResult]:
    """
    Concatena campos_fonte em nova coluna.
    Nulos pulados (PULAR). Todos nulos → string vazia + warning.
    """
    warnings: List[WarningEstrutural] = []

    if nome_coluna_resultado is None:
        chave = "_".join(sorted(config.campos_fonte))
        h = hashlib.md5(chave.encode()).hexdigest()[:6]
        nome_coluna_resultado = f"concat_{h}"

    todos_nulos_count = 0
    parcialmente_nulos_count = 0
    resultados: List[str] = []

    for _, row in df.iterrows():
        componentes: List[str] = []
        n_nulos = 0
        n_campos = len(config.campos_fonte)

        for campo in config.campos_fonte:
            val = row.get(campo)
            if pd.isna(val) or (isinstance(val, str) and val.strip() == ""):
                n_nulos += 1
                continue
            val_str = str(val).strip()
            if config.normalizar:
                val_str = normalizar_texto(val_str)
            componentes.append(val_str)

        resultado = config.separador.join(componentes)

        if n_nulos == n_campos:
            todos_nulos_count += 1
        elif n_nulos > 0:
            parcialmente_nulos_count += 1

        resultados.append(resultado)

    df_resultado = df.copy()
    df_resultado[nome_coluna_resultado] = resultados

    valores_gerados = sum(1 for r in resultados if r != "")

    # Warnings
    if todos_nulos_count > 0:
        warnings.append(WarningEstrutural(
            codigo=f"W-V{nome_visao}-COMP-CAMPOS-NULOS",
            categoria=CategoriaWarning.INFORMATIVO,
            microcopy=f"{todos_nulos_count} linhas com todos os campos-fonte nulos. Resultado: string vazia.",
            contexto={"n_todos_nulos": todos_nulos_count},
        ))

    if parcialmente_nulos_count > 0:
        warnings.append(WarningEstrutural(
            codigo=f"W-V{nome_visao}-COMP-PARCIAL",
            categoria=CategoriaWarning.INFORMATIVO,
            microcopy=f"{parcialmente_nulos_count} linhas com pelo menos 1 campo-fonte nulo (mas não todos).",
            contexto={"n_parcialmente_nulos": parcialmente_nulos_count},
        ))

    # Alerta V11-específico: > 30% com todos nulos
    n_total = len(df_resultado)
    if n_total > 0 and todos_nulos_count / n_total > 0.30:
        warnings.append(WarningEstrutural(
            codigo=f"W-V{nome_visao}-SEM-CONTEXTO",
            categoria=CategoriaWarning.ALERTA_ESTRUTURAL,
            microcopy=(
                f"{todos_nulos_count / n_total:.1%} das linhas sem contexto textual. "
                "Padronização textual inconsistente. Considere M2.NORMALIZE."
            ),
            contexto={"pct_sem_contexto": round(todos_nulos_count / n_total, 4)},
        ))

    return df_resultado, ConcatResult(
        coluna_concatenada_nome=nome_coluna_resultado,
        valores_gerados=valores_gerados,
        valores_vazios_todos_nulos=todos_nulos_count,
        valores_parcialmente_nulos=parcialmente_nulos_count,
        warnings_gerados=warnings,
    )
