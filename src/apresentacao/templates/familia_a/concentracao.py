"""Sub-template Família A · Concentração · D-202 etapa 5.

Movido e parametrizado de
`visoes.exportacao_v2._renderizar_secao_concentracao`.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from openpyxl.worksheet.worksheet import Worksheet

from apresentacao.formatos import formatar_percentual_br

from ._shared import renderizar_secao_como_tabela


def renderizar_concentracao(
    *,
    ws: Worksheet,
    linha: int,
    largura_util: int,
    concentracao: Optional[Dict[str, Any]],
    paleta,
) -> int:
    """E3a · 'Concentração' · oculta quando concentracao=None ou <5 PRESENTE_AMBOS."""
    if not concentracao:
        return linha

    n_pa = int(concentracao.get("n_casos", 0))
    top5 = concentracao.get("top_5_pct")
    top10 = concentracao.get("top_10_pct")
    interp = concentracao.get("interpretacao", "distribuida")

    linhas_texto: List[str] = []
    linhas_texto.append(
        "As 5 maiores variações (de "
        f"{n_pa:,} casos)".replace(",", ".") +
        f" explicam {formatar_percentual_br(top5, conversao_fracao=True)} do impacto."
    )
    if top10 is not None:
        linhas_texto.append(
            f"As 10 maiores explicam {formatar_percentual_br(top10, conversao_fracao=True)} do impacto."
        )

    if interp == "alta":
        microcopy = "→ Atenção concentrada nos extremos."
    elif interp == "moderada":
        microcopy = "→ Concentração moderada nos maiores."
    else:
        microcopy = "→ Variação distribuída por todo o conjunto · sem outliers dominantes."
    linhas_texto.append(microcopy)

    linhas_conteudo: List[Tuple] = [(t,) for t in linhas_texto]
    return renderizar_secao_como_tabela(
        ws, linha, "Concentração", linhas_conteudo,
        col_inicial=1, col_final=largura_util,
        paleta=paleta, aplicar_zebra=True,
    )
