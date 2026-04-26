"""Templates parametrizados de Família A (V1/V2/V11) · D-202 etapa 5.

5 sub-templates extraídos de `visoes.exportacao_v2._renderizar_resumo_executivo_v2`
para consumibilidade por V1/V11 e futuras visões da Família A.

Helpers visuais compartilhados em `_shared.py` (cabeçalho de seção · seção
como tabela · cards · bordas · helpers de altura).
"""

from .leitura_qualitativa import construir_leitura_qualitativa
from .saude_comparacao import renderizar_saude_comparacao
from .concentracao import renderizar_concentracao
from .onde_se_concentra import renderizar_onde_se_concentra
from .variacoes_destaque import (
    renderizar_grafico_variacoes,
    renderizar_variacoes_destaque,
)

__all__ = [
    "construir_leitura_qualitativa",
    "renderizar_saude_comparacao",
    "renderizar_concentracao",
    "renderizar_onde_se_concentra",
    "renderizar_grafico_variacoes",
    "renderizar_variacoes_destaque",
]
