"""
Visão V2 — Análise Comparativa entre Referências

Compara dois estados (Referência A e Referência B) de campos numéricos,
calculando variação absoluta, percentual e classificando o resultado.
"""

from __future__ import annotations

from collections import Counter
from typing import Literal, Optional

import pandas as pd
from pydantic import BaseModel


# ─────────────────────────────────────────────────────────────────────────────
# Modelos de Saída
# ─────────────────────────────────────────────────────────────────────────────


class RegistroComparado(BaseModel):
    agrupadores: dict[str, str]
    campo: str
    tipo_campo: Literal["VALOR", "PERCENTUAL", "INDICE"]
    semantica: Literal["MAIOR_E_MELHOR", "MENOR_E_MELHOR", "NEUTRO"]
    valor_a: Optional[float]
    valor_b: Optional[float]
    variacao_absoluta: Optional[float]
    variacao_percentual: Optional[float]
    classificacao: Literal[
        "MELHORA", "PIORA", "SEM_VARIACAO", "VARIACAO_NEUTRA", "SURGIMENTO", "DESAPARECIMENTO"
    ]
    flag: Optional[str]


class ResumoAgrupador(BaseModel):
    agrupador: str
    valor: str
    campo: str
    total_a: float
    total_b: float
    variacao_absoluta: float
    variacao_percentual: Optional[float]
    classificacao_predominante: str


class V2Result(BaseModel):
    visao: str = "V2"
    nome_visao: str = "Análise Comparativa entre Referências"
    estrutura_entrada: Literal["POR_COLUNAS", "POR_LINHAS"]
    nome_referencia_a: str
    nome_referencia_b: str
    campos_comparados: list[str]
    agrupadores: list[str]
    registros: list[RegistroComparado]
    resumo_por_agrupador: list[ResumoAgrupador]
    total_registros: int
    total_melhoras: int
    total_pioras: int
    total_sem_variacao: int
    total_surgimentos: int
    total_desaparecimentos: int
    warnings: list[str]
    errors: list[str]
    success: bool


# ─────────────────────────────────────────────────────────────────────────────
# Helpers internos
# ─────────────────────────────────────────────────────────────────────────────


def _calcular_variacao(
    valor_a: Optional[float],
    valor_b: Optional[float],
) -> tuple[Optional[float], Optional[float], Optional[str]]:
    """
    Calcula variacao_absoluta, variacao_percentual e flag para um par (A, B).

    Casos especiais:
    - Ambos None → (None, None, None)
    - A=0, B=0 → (0.0, 0.0, None)
    - A=0, B≠0 → variacao_percentual=None, flag=SURGIMENTO
    - A≠0, B=0 → variacao_percentual=-1.0, flag=DESAPARECIMENTO
    - Demais → cálculo padrão com 4 casas decimais

    Returns:
        Tupla (variacao_absoluta, variacao_percentual, flag).
    """
    if valor_a is None and valor_b is None:
        return None, None, None

    va: float = valor_a if valor_a is not None else 0.0
    vb: float = valor_b if valor_b is not None else 0.0

    if va == 0.0 and vb == 0.0:
        return 0.0, 0.0, None

    variacao_absoluta = vb - va
    flag: Optional[str] = None
    variacao_percentual: Optional[float] = None

    if va == 0.0 and vb != 0.0:
        flag = "SURGIMENTO"
    elif va != 0.0 and vb == 0.0:
        flag = "DESAPARECIMENTO"
        variacao_percentual = -1.0
    else:
        variacao_percentual = round((vb - va) / abs(va), 4)

    return variacao_absoluta, variacao_percentual, flag


def _classificar(
    variacao_absoluta: Optional[float],
    flag: Optional[str],
    semantica: str,
) -> str:
    """
    Retorna a classificação analítica de um registro com base na variação e semântica.

    Args:
        variacao_absoluta: Diferença B - A.
        flag: "SURGIMENTO", "DESAPARECIMENTO" ou None.
        semantica: "MAIOR_E_MELHOR", "MENOR_E_MELHOR" ou "NEUTRO".

    Returns:
        String de classificação conforme o contrato V2Result.
    """
    if flag == "SURGIMENTO":
        return "SURGIMENTO"
    if flag == "DESAPARECIMENTO":
        return "DESAPARECIMENTO"
    if variacao_absoluta is None or variacao_absoluta == 0.0:
        return "SEM_VARIACAO"
    if semantica == "NEUTRO":
        return "VARIACAO_NEUTRA"
    if semantica == "MAIOR_E_MELHOR":
        return "MELHORA" if variacao_absoluta > 0 else "PIORA"
    # MENOR_E_MELHOR
    return "MELHORA" if variacao_absoluta < 0 else "PIORA"


def _variacao_percentual_resumo(
    total_a: float,
    total_b: float,
    tipo_campo: str,
    regs_grupo: list[RegistroComparado],
) -> Optional[float]:
    """
    Calcula variacao_percentual para o resumo por agrupador.

    VALOR: variação sobre o total (soma).
    PERCENTUAL / INDICE: média das variações percentuais dos registros individuais.

    Returns:
        Variação percentual do grupo ou None se incalculável.
    """
    if tipo_campo in ("PERCENTUAL", "INDICE"):
        pcts = [r.variacao_percentual for r in regs_grupo if r.variacao_percentual is not None]
        if not pcts:
            return None
        return round(sum(pcts) / len(pcts), 4)

    if total_a == 0.0 and total_b == 0.0:
        return 0.0
    if total_a == 0.0:
        return None
    return round((total_b - total_a) / abs(total_a), 4)


def _resultado_erro(
    estrutura_entrada: str,
    nome_referencia_a: str,
    nome_referencia_b: str,
    errors: list[str],
    warnings: Optional[list[str]] = None,
) -> V2Result:
    """Constrói um V2Result com success=False."""
    return V2Result(
        estrutura_entrada=estrutura_entrada,
        nome_referencia_a=nome_referencia_a,
        nome_referencia_b=nome_referencia_b,
        campos_comparados=[],
        agrupadores=[],
        registros=[],
        resumo_por_agrupador=[],
        total_registros=0,
        total_melhoras=0,
        total_pioras=0,
        total_sem_variacao=0,
        total_surgimentos=0,
        total_desaparecimentos=0,
        warnings=warnings or [],
        errors=errors,
        success=False,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Preparação POR_COLUNAS
# ─────────────────────────────────────────────────────────────────────────────


def _preparar_por_colunas(
    df: pd.DataFrame,
    campos_comparados: list[dict],
) -> tuple[pd.DataFrame, list[str]]:
    """
    Valida colunas e materializa __val_a__ / __val_b__ para estrutura POR_COLUNAS.

    Args:
        df: DataFrame original do MotorResult.
        campos_comparados: Lista de configurações de campos. Cada item requer
            coluna_a, coluna_b, nome_analitico, tipo_campo e semantica.

    Returns:
        (df_work, erros) — df_work enriquecido com colunas padronizadas e lista
        de erros bloqueantes (E02).
    """
    erros: list[str] = []
    df_work = df.copy()

    for campo in campos_comparados:
        nome = campo["nome_analitico"]
        col_a = campo.get("coluna_a")
        col_b = campo.get("coluna_b")

        for col, ref in [(col_a, "A"), (col_b, "B")]:
            if col not in df.columns:
                erros.append(
                    f"E02 — Coluna '{col}' (referência {ref}, campo '{nome}') não encontrada na base."
                )
            elif not pd.api.types.is_numeric_dtype(df[col]):
                erros.append(
                    f"E02 — Coluna '{col}' (referência {ref}, campo '{nome}') não é numérica."
                )

    if erros:
        return df_work, erros

    for campo in campos_comparados:
        nome = campo["nome_analitico"]
        df_work[f"__val_a__{nome}"] = pd.to_numeric(df_work[campo["coluna_a"]], errors="coerce")
        df_work[f"__val_b__{nome}"] = pd.to_numeric(df_work[campo["coluna_b"]], errors="coerce")

    return df_work, erros


# ─────────────────────────────────────────────────────────────────────────────
# Preparação POR_LINHAS
# ─────────────────────────────────────────────────────────────────────────────


def _preparar_por_linhas(
    df: pd.DataFrame,
    campos_comparados: list[dict],
    campo_discriminador: str,
    valor_referencia_a: str,
    valor_referencia_b: str,
) -> tuple[pd.DataFrame, list[str], list[str]]:
    """
    Valida, pivota e materializa __val_a__ / __val_b__ para estrutura POR_LINHAS.

    Registros sem par (A sem B ou vice-versa) recebem NaN no lado faltante, sendo
    classificados como SURGIMENTO ou DESAPARECIMENTO durante o cálculo de variação.

    Args:
        df: DataFrame original do MotorResult.
        campos_comparados: Lista de configurações. Cada item requer coluna_valor,
            nome_analitico, tipo_campo e semantica.
        campo_discriminador: Coluna que identifica A vs B.
        valor_referencia_a: Valor do discriminador que representa A.
        valor_referencia_b: Valor do discriminador que representa B.

    Returns:
        (df_work, erros, warnings) — df_work pivotado, erros bloqueantes e warnings.
    """
    erros: list[str] = []
    warns: list[str] = []

    # E03 — discriminador não encontrado
    if campo_discriminador not in df.columns:
        erros.append(
            f"E03 — Campo discriminador '{campo_discriminador}' não encontrado na base."
        )
        return df, erros, warns

    valores_distintos = df[campo_discriminador].astype(str).unique().tolist()

    # E04 — valor de referência não encontrado
    if valor_referencia_a not in valores_distintos:
        erros.append(
            f"E04 — Valor de referência A '{valor_referencia_a}' não encontrado "
            f"no discriminador '{campo_discriminador}'."
        )
    if valor_referencia_b not in valores_distintos:
        erros.append(
            f"E04 — Valor de referência B '{valor_referencia_b}' não encontrado "
            f"no discriminador '{campo_discriminador}'."
        )
    if erros:
        return df, erros, warns

    # Validar colunas de valor antes do pivot
    colunas_valor: list[str] = []
    for campo in campos_comparados:
        nome = campo["nome_analitico"]
        col_v = campo.get("coluna_valor")
        if col_v not in df.columns:
            erros.append(
                f"E02 — Coluna de valor '{col_v}' (campo '{nome}') não encontrada na base."
            )
        elif not pd.api.types.is_numeric_dtype(df[col_v]):
            erros.append(
                f"E02 — Coluna de valor '{col_v}' (campo '{nome}') não é numérica."
            )
        else:
            colunas_valor.append(col_v)

    if erros:
        return df, erros, warns

    df_str = df.copy()
    df_str[campo_discriminador] = df_str[campo_discriminador].astype(str)

    df_a = df_str[df_str[campo_discriminador] == valor_referencia_a].drop(
        columns=[campo_discriminador]
    ).reset_index(drop=True)
    df_b = df_str[df_str[campo_discriminador] == valor_referencia_b].drop(
        columns=[campo_discriminador]
    ).reset_index(drop=True)

    # W05 — desbalanceamento
    if len(df_a) != len(df_b):
        warns.append(
            f"W05 — Estrutura POR_LINHAS: valores do discriminador não balanceados "
            f"(A={len(df_a)} registros, B={len(df_b)} registros)."
        )

    # Colunas que formam a chave de junção (dimensões que identificam cada linha)
    cols_valor_set = set(colunas_valor)
    colunas_chave = [c for c in df_a.columns if c not in cols_valor_set]

    if colunas_chave:
        df_merged = pd.merge(
            df_a[colunas_chave + colunas_valor],
            df_b[colunas_chave + colunas_valor],
            on=colunas_chave,
            how="outer",
            suffixes=("__A", "__B"),
        )
    else:
        # Sem dimensões: alinhar por posição, completar com NaN
        max_len = max(len(df_a), len(df_b))
        df_merged = pd.DataFrame()
        for col_v in colunas_valor:
            df_merged[f"{col_v}__A"] = df_a[col_v].reindex(range(max_len))
            df_merged[f"{col_v}__B"] = df_b[col_v].reindex(range(max_len))

    # Materializar __val_a__ e __val_b__
    df_work = df_merged.copy()
    for campo in campos_comparados:
        nome = campo["nome_analitico"]
        col_v = campo["coluna_valor"]
        df_work[f"__val_a__{nome}"] = pd.to_numeric(
            df_work.get(f"{col_v}__A"), errors="coerce"
        )
        df_work[f"__val_b__{nome}"] = pd.to_numeric(
            df_work.get(f"{col_v}__B"), errors="coerce"
        )

    return df_work, erros, warns


# ─────────────────────────────────────────────────────────────────────────────
# Verificação de warnings W01, W02, W04
# ─────────────────────────────────────────────────────────────────────────────


def _verificar_warnings(
    df_work: pd.DataFrame,
    campos_comparados: list[dict],
    agrupadores: list[str],
) -> list[str]:
    """
    Verifica W01 (nulos > 20%), W02 (cardinalidade de agrupadores > 50) e
    W04 (valor_A = 0 detectado).

    Args:
        df_work: DataFrame de trabalho já com colunas __val_a__ e __val_b__.
        campos_comparados: Configuração dos campos comparados.
        agrupadores: Lista de colunas de agrupamento.

    Returns:
        Lista de warnings em formato "Wxx — descrição".
    """
    warns: list[str] = []
    total = len(df_work)
    if total == 0:
        return warns

    for campo in campos_comparados:
        nome = campo["nome_analitico"]
        col_a = f"__val_a__{nome}"
        col_b = f"__val_b__{nome}"

        # W01
        for col, ref in [(col_a, "A"), (col_b, "B")]:
            if col in df_work.columns:
                null_pct = df_work[col].isna().sum() / total
                if null_pct > 0.20:
                    warns.append(
                        f"W01 — Campo '{nome}' (referência {ref}) possui "
                        f"{null_pct:.0%} de valores nulos."
                    )

        # W04
        if col_a in df_work.columns:
            serie_a = pd.to_numeric(df_work[col_a], errors="coerce")
            zeros = int(((serie_a == 0.0) | serie_a.isna()).sum())
            # contar apenas os que são explicitamente 0 (não NaN)
            zeros_explícitos = int((serie_a.fillna(1.0) == 0.0).sum())
            if zeros_explícitos > 0:
                warns.append(
                    f"W04 — Campo '{nome}': {zeros_explícitos} registro(s) com "
                    f"valor_A = 0 (variação percentual não calculável)."
                )

    # W02
    for ag in agrupadores:
        if ag in df_work.columns:
            card = int(df_work[ag].nunique())
            if card > 50:
                warns.append(
                    f"W02 — Agrupador '{ag}' possui cardinalidade alta "
                    f"({card} valores únicos)."
                )

    return warns


# ─────────────────────────────────────────────────────────────────────────────
# Resumo por agrupador
# ─────────────────────────────────────────────────────────────────────────────


def _calcular_resumo(
    registros: list[RegistroComparado],
    agrupadores: list[str],
    campos_comparados: list[dict],
) -> list[ResumoAgrupador]:
    """
    Gera ResumoAgrupador para cada combinação (agrupador × valor × campo).

    Para campos VALOR, totaliza por soma.
    Para campos PERCENTUAL e INDICE, usa média das variações percentuais individuais.

    Args:
        registros: Lista de RegistroComparado já calculados.
        agrupadores: Lista de campos categóricos usados como dimensões.
        campos_comparados: Configuração dos campos (para obter tipo_campo).

    Returns:
        Lista de ResumoAgrupador ordenada por agrupador → valor → campo.
    """
    if not agrupadores or not registros:
        return []

    tipo_por_campo = {c["nome_analitico"]: c["tipo_campo"] for c in campos_comparados}
    resumos: list[ResumoAgrupador] = []

    for ag in agrupadores:
        valores_ag = sorted({r.agrupadores.get(ag, "") for r in registros})

        for val_ag in valores_ag:
            for campo_cfg in campos_comparados:
                nome = campo_cfg["nome_analitico"]
                tipo = tipo_por_campo[nome]

                regs_grupo = [
                    r
                    for r in registros
                    if r.agrupadores.get(ag, "") == val_ag and r.campo == nome
                ]
                if not regs_grupo:
                    continue

                total_a = sum(r.valor_a or 0.0 for r in regs_grupo)
                total_b = sum(r.valor_b or 0.0 for r in regs_grupo)
                variacao_absoluta = total_b - total_a
                variacao_percentual = _variacao_percentual_resumo(
                    total_a, total_b, tipo, regs_grupo
                )

                contagem = Counter(r.classificacao for r in regs_grupo)
                classificacao_predominante = contagem.most_common(1)[0][0]

                resumos.append(
                    ResumoAgrupador(
                        agrupador=ag,
                        valor=val_ag,
                        campo=nome,
                        total_a=total_a,
                        total_b=total_b,
                        variacao_absoluta=variacao_absoluta,
                        variacao_percentual=variacao_percentual,
                        classificacao_predominante=classificacao_predominante,
                    )
                )

    return resumos


# ─────────────────────────────────────────────────────────────────────────────
# Função principal
# ─────────────────────────────────────────────────────────────────────────────


def executar_v2(
    motor_result,
    estrutura_entrada: str,
    nome_referencia_a: str,
    nome_referencia_b: str,
    campos_comparados: list[dict],
    agrupadores: list[str],
    campo_discriminador: str = None,
    valor_referencia_a: str = None,
    valor_referencia_b: str = None,
) -> V2Result:
    """
    Executa a Visão V2 — Análise Comparativa entre Referências.

    Args:
        motor_result: Objeto MotorResult com atributo .df (pd.DataFrame).
        estrutura_entrada: "POR_COLUNAS" ou "POR_LINHAS".
        nome_referencia_a: Nome da Referência A (ex: "Orçado", "Jan/24").
        nome_referencia_b: Nome da Referência B (ex: "Realizado", "Jan/25").
        campos_comparados: Lista de dicts com configuração por campo.
            POR_COLUNAS: {coluna_a, coluna_b, nome_analitico, tipo_campo, semantica}.
            POR_LINHAS:  {coluna_valor, nome_analitico, tipo_campo, semantica}.
        agrupadores: Colunas categóricas para segmentar a análise (0–5).
        campo_discriminador: (POR_LINHAS) Coluna que identifica A vs B.
        valor_referencia_a: (POR_LINHAS) Valor do discriminador que representa A.
        valor_referencia_b: (POR_LINHAS) Valor do discriminador que representa B.

    Returns:
        V2Result com registros, resumos, contadores, warnings e errors.
    """
    warnings_out: list[str] = []
    errors_out: list[str] = []

    # ── E01 ───────────────────────────────────────────────────────────────
    if not campos_comparados:
        errors_out.append("E01 — Nenhum campo de comparação configurado.")
        return _resultado_erro(
            estrutura_entrada, nome_referencia_a, nome_referencia_b, errors_out
        )

    # ── E06 ───────────────────────────────────────────────────────────────
    if len(campos_comparados) > 10:
        errors_out.append(
            f"E06 — Número de campos comparados ({len(campos_comparados)}) excede o limite de 10."
        )
        return _resultado_erro(
            estrutura_entrada, nome_referencia_a, nome_referencia_b, errors_out
        )

    # ── E05 ───────────────────────────────────────────────────────────────
    df: pd.DataFrame = motor_result.df
    if len(df) > 500_000:
        errors_out.append(
            f"E05 — Número de registros ({len(df):,}) excede o limite de 500.000."
        )
        return _resultado_erro(
            estrutura_entrada, nome_referencia_a, nome_referencia_b, errors_out
        )

    # ── W03 ───────────────────────────────────────────────────────────────
    if len(agrupadores) > 3:
        warnings_out.append(
            f"W03 — {len(agrupadores)} agrupadores configurados (recomendado: até 3)."
        )

    # ── Preparação do DataFrame de trabalho ───────────────────────────────
    erros_prep: list[str] = []

    if estrutura_entrada == "POR_COLUNAS":
        df_work, erros_prep = _preparar_por_colunas(df.copy(), campos_comparados)

    elif estrutura_entrada == "POR_LINHAS":
        df_work, erros_prep, warns_linhas = _preparar_por_linhas(
            df.copy(),
            campos_comparados,
            campo_discriminador,
            valor_referencia_a,
            valor_referencia_b,
        )
        warnings_out.extend(warns_linhas)

    else:
        errors_out.append(
            f"Estrutura de entrada inválida: '{estrutura_entrada}'. "
            "Use 'POR_COLUNAS' ou 'POR_LINHAS'."
        )
        return _resultado_erro(
            estrutura_entrada, nome_referencia_a, nome_referencia_b, errors_out
        )

    if erros_prep:
        errors_out.extend(erros_prep)
        return _resultado_erro(
            estrutura_entrada,
            nome_referencia_a,
            nome_referencia_b,
            errors_out,
            warnings_out,
        )

    # ── Warnings W01, W02, W04 ────────────────────────────────────────────
    warnings_out.extend(
        _verificar_warnings(df_work, campos_comparados, agrupadores)
    )

    # ── Geração dos registros ─────────────────────────────────────────────
    registros: list[RegistroComparado] = []

    for _, row in df_work.iterrows():
        agrup_vals: dict[str, str] = {
            ag: str(row[ag]) if ag in row and pd.notna(row[ag]) else ""
            for ag in agrupadores
        }

        for campo_cfg in campos_comparados:
            nome = campo_cfg["nome_analitico"]
            tipo_campo = campo_cfg["tipo_campo"]
            semantica = campo_cfg["semantica"]

            raw_a = row.get(f"__val_a__{nome}")
            raw_b = row.get(f"__val_b__{nome}")

            valor_a: Optional[float] = float(raw_a) if pd.notna(raw_a) else None
            valor_b: Optional[float] = float(raw_b) if pd.notna(raw_b) else None

            variacao_absoluta, variacao_percentual, flag = _calcular_variacao(
                valor_a, valor_b
            )
            classificacao = _classificar(variacao_absoluta, flag, semantica)

            registros.append(
                RegistroComparado(
                    agrupadores=agrup_vals,
                    campo=nome,
                    tipo_campo=tipo_campo,
                    semantica=semantica,
                    valor_a=valor_a,
                    valor_b=valor_b,
                    variacao_absoluta=variacao_absoluta,
                    variacao_percentual=variacao_percentual,
                    classificacao=classificacao,
                    flag=flag,
                )
            )

    # ── Resumo por agrupador ──────────────────────────────────────────────
    resumo_por_agrupador = _calcular_resumo(registros, agrupadores, campos_comparados)

    # ── Contadores ────────────────────────────────────────────────────────
    total_melhoras = sum(1 for r in registros if r.classificacao == "MELHORA")
    total_pioras = sum(1 for r in registros if r.classificacao == "PIORA")
    total_sem_variacao = sum(1 for r in registros if r.classificacao == "SEM_VARIACAO")
    total_surgimentos = sum(1 for r in registros if r.classificacao == "SURGIMENTO")
    total_desaparecimentos = sum(
        1 for r in registros if r.classificacao == "DESAPARECIMENTO"
    )

    return V2Result(
        estrutura_entrada=estrutura_entrada,
        nome_referencia_a=nome_referencia_a,
        nome_referencia_b=nome_referencia_b,
        campos_comparados=[c["nome_analitico"] for c in campos_comparados],
        agrupadores=agrupadores,
        registros=registros,
        resumo_por_agrupador=resumo_por_agrupador,
        total_registros=len(df_work),
        total_melhoras=total_melhoras,
        total_pioras=total_pioras,
        total_sem_variacao=total_sem_variacao,
        total_surgimentos=total_surgimentos,
        total_desaparecimentos=total_desaparecimentos,
        warnings=warnings_out,
        errors=errors_out,
        success=True,
    )
