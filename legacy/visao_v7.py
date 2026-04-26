"""
Visão V7 — Desvio em Relação à Média do Grupo.

Entrada : MotorResult + ConfigV7
Saída   : V7Result com registros por elemento, resumo por grupo,
          warnings e errors, sem geração de arquivo Excel.
"""
from __future__ import annotations

from typing import List, Optional

import pandas as pd
from pydantic import BaseModel

from motor_base import ColumnMeta, MotorResult  # noqa: F401 — contrato externo


# ---------------------------------------------------------------------------
# Modelos Pydantic (definidos na spec — não alterar nomes/campos)
# ---------------------------------------------------------------------------

class ConfigV7(BaseModel):
    campo_grupo: str
    campo_medida: str
    nome_analitico: str
    tolerancia_pct: float = 5.0


class ElementoDesvio(BaseModel):
    grupo: str
    elemento: str
    valor: float
    media_grupo: float
    desvio_absoluto: float
    desvio_percentual: Optional[float]
    classificacao: str  # "ACIMA" | "NA_MEDIA" | "ABAIXO"


class ResumoGrupo(BaseModel):
    grupo: str
    media: float
    total_registros: int
    acima: int
    na_media: int
    abaixo: int
    maior_desvio_positivo: Optional[float]
    maior_desvio_negativo: Optional[float]


class V7Result(BaseModel):
    registros: List[ElementoDesvio]
    resumo_por_grupo: List[ResumoGrupo]
    total_registros: int
    grupos_processados: int
    warnings: List[str]
    errors: List[str]
    success: bool


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _r(value: float) -> float:
    """Arredonda para 4 casas decimais."""
    return round(value, 4)


def _falha(errors: List[str], warnings: List[str], msg: str) -> V7Result:
    errors.append(msg)
    return V7Result(
        registros=[],
        resumo_por_grupo=[],
        total_registros=0,
        grupos_processados=0,
        warnings=warnings,
        errors=errors,
        success=False,
    )


def _classificar(
    desvio_absoluto: float,
    desvio_percentual: Optional[float],
    media_grupo: float,
    valor: float,
    tolerancia_pct: float,
) -> str:
    """Retorna 'ACIMA', 'NA_MEDIA' ou 'ABAIXO' conforme spec."""
    if media_grupo == 0.0:
        if valor == 0.0:
            return "NA_MEDIA"
        return "ACIMA" if valor > 0 else "ABAIXO"

    # media_grupo != 0 → desvio_percentual está disponível
    assert desvio_percentual is not None
    if abs(desvio_percentual) <= tolerancia_pct:
        return "NA_MEDIA"
    return "ACIMA" if desvio_absoluto > 0 else "ABAIXO"


# ---------------------------------------------------------------------------
# Função principal
# ---------------------------------------------------------------------------

def executar_v7(motor_result: MotorResult, config: ConfigV7) -> V7Result:
    """
    Processa o MotorResult segundo ConfigV7 e devolve um V7Result.

    Valida erros bloqueantes E01–E06, emite warnings W01–W05,
    calcula desvio absoluto/percentual e classifica cada elemento.
    Nenhum arquivo Excel é gerado aqui.
    """
    errors: List[str] = []
    warnings: List[str] = []

    # --- mapa de metadados de colunas ---
    col_meta: dict[str, str] = {col.name: col.type for col in motor_result.columns}

    # E01 — campo_grupo ausente
    if config.campo_grupo not in col_meta:
        return _falha(
            errors, warnings,
            f"E01: campo_grupo '{config.campo_grupo}' não encontrado na base de dados.",
        )

    # E02 — campo_medida ausente
    if config.campo_medida not in col_meta:
        return _falha(
            errors, warnings,
            f"E02: campo_medida '{config.campo_medida}' não encontrado na base de dados.",
        )

    # E03 — campo_medida não é numérico
    if col_meta[config.campo_medida] != "numeric":
        return _falha(
            errors, warnings,
            f"E03: campo_medida '{config.campo_medida}' não é numérico "
            f"(tipo detectado: '{col_meta[config.campo_medida]}').",
        )

    # E04 — campo_grupo é numérico (deve ser categórico)
    if col_meta[config.campo_grupo] == "numeric":
        return _falha(
            errors, warnings,
            f"E04: campo_grupo '{config.campo_grupo}' é numérico; deve ser categórico.",
        )

    # E06 — tolerancia_pct fora do intervalo [0, 100]
    if config.tolerancia_pct < 0 or config.tolerancia_pct > 100:
        return _falha(
            errors, warnings,
            f"E06: tolerancia_pct deve estar entre 0 e 100 "
            f"(recebido: {config.tolerancia_pct}).",
        )

    # --- construir DataFrame ---
    data = motor_result.data
    df: pd.DataFrame = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)

    # W02 — nulos em campo_grupo
    null_grupo = int(df[config.campo_grupo].isna().sum())
    if null_grupo > 0:
        warnings.append(
            f"W02: {null_grupo} registro(s) com valor nulo em "
            f"'{config.campo_grupo}' removido(s)."
        )
        df = df[df[config.campo_grupo].notna()].copy()

    # W01 — nulos em campo_medida
    null_medida = int(df[config.campo_medida].isna().sum())
    if null_medida > 0:
        warnings.append(
            f"W01: {null_medida} registro(s) com valor nulo em "
            f"'{config.campo_medida}' removido(s)."
        )
        df = df[df[config.campo_medida].notna()].copy()

    # E05 — base vazia após limpeza
    if df.empty:
        return _falha(
            errors, warnings,
            "E05: Base de dados vazia após remoção de registros nulos.",
        )

    # W05 — tolerância zero
    if config.tolerancia_pct == 0.0:
        warnings.append(
            "W05: tolerancia_pct = 0 — nenhum registro será classificado como NA_MEDIA."
        )

    # --- processamento por grupo ---
    registros: List[ElementoDesvio] = []
    resumo_por_grupo: List[ResumoGrupo] = []

    for grupo_nome, grupo_df in df.groupby(config.campo_grupo, sort=True):
        media_grupo = _r(float(grupo_df[config.campo_medida].mean()))
        grupo_str = str(grupo_nome)

        # W03 — grupo com 1 único registro
        if len(grupo_df) == 1:
            warnings.append(
                f"W03: Grupo '{grupo_str}' possui apenas 1 registro "
                "— média = próprio valor, desvio = 0."
            )

        # W04 — média do grupo igual a zero
        if media_grupo == 0.0:
            warnings.append(
                f"W04: Grupo '{grupo_str}' possui média = 0 "
                "— desvio_percentual não calculável."
            )

        acima = na_media = abaixo = 0
        desvios_pos: List[float] = []
        desvios_neg: List[float] = []

        for idx, row in grupo_df.iterrows():
            valor = _r(float(row[config.campo_medida]))
            desvio_absoluto = _r(valor - media_grupo)

            if media_grupo != 0.0:
                desvio_percentual: Optional[float] = _r(
                    (desvio_absoluto / abs(media_grupo)) * 100
                )
            else:
                desvio_percentual = None

            classificacao = _classificar(
                desvio_absoluto,
                desvio_percentual,
                media_grupo,
                valor,
                config.tolerancia_pct,
            )

            if classificacao == "ACIMA":
                acima += 1
            elif classificacao == "NA_MEDIA":
                na_media += 1
            else:
                abaixo += 1

            if desvio_absoluto > 0:
                desvios_pos.append(desvio_absoluto)
            elif desvio_absoluto < 0:
                desvios_neg.append(desvio_absoluto)

            registros.append(ElementoDesvio(
                grupo=grupo_str,
                elemento=str(idx),
                valor=valor,
                media_grupo=media_grupo,
                desvio_absoluto=desvio_absoluto,
                desvio_percentual=desvio_percentual,
                classificacao=classificacao,
            ))

        resumo_por_grupo.append(ResumoGrupo(
            grupo=grupo_str,
            media=media_grupo,
            total_registros=len(grupo_df),
            acima=acima,
            na_media=na_media,
            abaixo=abaixo,
            maior_desvio_positivo=_r(max(desvios_pos)) if desvios_pos else None,
            maior_desvio_negativo=_r(min(desvios_neg)) if desvios_neg else None,
        ))

    return V7Result(
        registros=registros,
        resumo_por_grupo=resumo_por_grupo,
        total_registros=len(registros),
        grupos_processados=len(resumo_por_grupo),
        warnings=warnings,
        errors=errors,
        success=True,
    )
