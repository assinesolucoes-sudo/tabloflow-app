"""Sub-template Família A · Leitura qualitativa · D-202 etapa 5.

Construa leitura qualitativa em 2-4 sentenças condicionais a partir de
parâmetros explícitos (sem acoplamento a V2Result · genérico Família A).

Movido e parametrizado de `visoes.exportacao_v2._construir_leitura_qualitativa_v2`
em D-202 etapa 5/6.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from apresentacao.formatos import (
    formatar_diferenca_por_unidade,
    formatar_percentual_br,
    valor_total_card,
)

from ._shared import contrair_de


def construir_leitura_qualitativa(
    *,
    unidade: str,
    tipo_campo: str,
    semantica: str,
    ancora: Any,
    dist_sem: Optional[Dict[str, int]],
    delta_sem: Optional[Dict[str, float]],
    base_analitica: Any,
    concentracao: Optional[Dict[str, Any]],
    onde_se_concentra: Optional[Dict[str, Any]],
    origem_ux: str,
    comparado_ux: str,
) -> str:
    """E3c · constrói leitura qualitativa em 2-4 sentenças condicionais.

    Parâmetros explícitos (D-202):
      - unidade · tipo_campo · semantica · valores do ContratoComparativo
      - ancora · objeto NumerosAncora-like (duck-typed) com:
          total_origem · total_comparado · diferenca_total · variacao_total_pct
          total_combinacoes_analisadas · combinacoes_com_mudanca ·
          combinacoes_estaveis · pct_mudanca
      - dist_sem · dict {classif_semantica → contagem}
      - delta_sem · dict {classif_semantica → soma de Δ}
      - base_analitica · DataFrame-like (consultado apenas para len de 'diferenca')
      - concentracao · dict E3a (top_5_pct · interpretacao)
      - onde_se_concentra · dict E3b (top · agrupador)
      - origem_ux · comparado_ux · rótulos amigáveis

    PERCENTUAL usa Média + Variação relativa (não Δ total em p.p somados,
    que viola C.D3) e omite magnitudes entre parênteses dos casos.
    """
    # Variante ESTADO_SITUACAO · template separado
    if tipo_campo == "ESTADO_SITUACAO":
        total_comb = getattr(ancora, "total_combinacoes_analisadas", 0) or 0
        mudaram = getattr(ancora, "combinacoes_com_mudanca", 0) or 0
        estaveis = getattr(ancora, "combinacoes_estaveis", 0) or 0
        if total_comb == 0:
            return "Análise sem combinações para leitura qualitativa."
        pct = getattr(ancora, "pct_mudanca", 0) or 0
        partes: List[str] = []
        if mudaram > 0:
            partes.append(
                f"{mudaram:,} combinação(ões) mudaram de estado "
                f"({formatar_percentual_br(pct, conversao_fracao=True)} do total)".replace(",", ".")
            )
        if estaveis > 0:
            partes.append(
                f"{estaveis:,} permaneceram estáveis".replace(",", ".")
            )
        if not partes:
            return "Nenhuma combinação foi analisada nesta comparação."
        return ", ".join(partes) + "."

    # Variante numérica
    sentencas: List[str] = []
    dist_sem = dist_sem or {}
    delta_sem = delta_sem or {}

    # Sentença 1 · resultado agregado · ramifica por unidade
    dif = getattr(ancora, "diferenca_total", None)
    var = getattr(ancora, "variacao_total_pct", None)

    if unidade == "PERCENTUAL":
        n_pa = 0
        if base_analitica is not None and "diferenca" in getattr(base_analitica, "columns", []):
            n_pa = int(base_analitica["diferenca"].dropna().shape[0])
        media_orig = valor_total_card(getattr(ancora, "total_origem", None), n_pa, unidade)
        media_comp = valor_total_card(getattr(ancora, "total_comparado", None), n_pa, unidade)
        if media_orig is not None and media_comp is not None and media_orig != 0:
            var_pct = (media_comp - media_orig) / media_orig
            if var_pct == 0:
                sentencas.append(
                    f"A Média de {comparado_ux} ficou em "
                    f"{formatar_percentual_br(media_comp, conversao_fracao=True)} "
                    f"contra {formatar_percentual_br(media_orig, conversao_fracao=True)} "
                    f"em {origem_ux} · sem variação relativa"
                )
            else:
                substantivo = "alta" if var_pct > 0 else "queda"
                sentencas.append(
                    f"A Média de {comparado_ux} ficou em "
                    f"{formatar_percentual_br(media_comp, conversao_fracao=True)} "
                    f"contra {formatar_percentual_br(media_orig, conversao_fracao=True)} "
                    f"em {origem_ux}, uma {substantivo} relativa de "
                    f"{formatar_percentual_br(abs(var_pct), conversao_fracao=True)}"
                )
        elif media_comp is not None and media_orig is not None:
            sentencas.append(
                f"A Média de {comparado_ux} ficou em "
                f"{formatar_percentual_br(media_comp, conversao_fracao=True)}"
            )
    else:
        if dif is not None and var is not None and var != 0:
            var_str = formatar_percentual_br(abs(var), conversao_fracao=True)
            delta_str = formatar_diferenca_por_unidade(dif, unidade)
            if dif > 0:
                sentencas.append(
                    f"O {comparado_ux} superou {contrair_de(origem_ux)} em {var_str} "
                    f"no agregado ({delta_str})"
                )
            else:
                sentencas.append(
                    f"O {comparado_ux} ficou abaixo {contrair_de(origem_ux)} em {var_str} "
                    f"no agregado ({delta_str})"
                )
        elif dif is not None and dif == 0:
            sentencas.append(
                f"O {comparado_ux} ficou idêntico ao agregado de {origem_ux}"
            )

    # Sentença 2 · composição
    if semantica == "NEUTRO":
        cima = int(dist_sem.get("AUMENTOU", 0))
        baixo = int(dist_sem.get("REDUZIU", 0))
        delta_cima = float(delta_sem.get("AUMENTOU", 0.0))
        delta_baixo = float(delta_sem.get("REDUZIU", 0.0))
        verbo_cima = "aumentaram"
        verbo_baixo = "reduziram"
    else:
        cima = int(dist_sem.get("POSITIVO", 0))
        baixo = int(dist_sem.get("NEGATIVO", 0))
        delta_cima = float(delta_sem.get("POSITIVO", 0.0))
        delta_baixo = float(delta_sem.get("NEGATIVO", 0.0))
        verbo_cima = "melhoraram"
        verbo_baixo = "pioraram"
    if cima > 0 and baixo > 0:
        if unidade == "PERCENTUAL":
            sentencas.append(
                f"o saldo é resultado de movimentos opostos: {cima} caso(s) {verbo_cima} "
                f"contra {baixo} caso(s) que {verbo_baixo}"
            )
        else:
            sentencas.append(
                f"o saldo é resultado de movimentos opostos: {cima} caso(s) {verbo_cima} "
                f"({formatar_diferenca_por_unidade(delta_cima, unidade)}) "
                f"contra {baixo} caso(s) que {verbo_baixo} "
                f"({formatar_diferenca_por_unidade(delta_baixo, unidade)})"
            )

    # Sentença 3 · concentração (apenas alta ou moderada)
    if concentracao and concentracao.get("interpretacao") in ("alta", "moderada"):
        top5 = concentracao.get("top_5_pct")
        if top5 is not None:
            sentencas.append(
                f"a variação está concentrada em poucos casos · "
                f"5 deles explicam {formatar_percentual_br(top5, conversao_fracao=True)} "
                f"do impacto"
            )

    # Sentença 4 · direção dominante
    if onde_se_concentra and len(onde_se_concentra.get("top", []) or []) >= 2:
        top_alta = next((t for t in onde_se_concentra["top"] if (t.get("delta") or 0) > 0), None)
        top_baixa = next((t for t in onde_se_concentra["top"] if (t.get("delta") or 0) < 0), None)
        if top_alta and top_baixa:
            sentencas.append(
                f"com {top_alta['categoria']} puxando para cima e "
                f"{top_baixa['categoria']} para baixo"
            )

    if not sentencas:
        return "Análise sem dados significativos para leitura qualitativa."

    if len(sentencas) == 1:
        return sentencas[0] + "."

    primeira = sentencas[0]
    seguintes = sentencas[1:]
    junta = ", ".join(seguintes)
    if junta:
        return primeira + ", " + junta + "."
    return primeira + "."
