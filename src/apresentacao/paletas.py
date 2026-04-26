"""
F-APRESENT · capability 1 · Catálogo de 4 paletas executivas (D-164).

Catálogo fechado · Azul · Verde · Cinza · Vinho executivo. Adicionar paleta
exige decisão D-XXX nova.

Tipografia: Calibri família única · estável em Excel cross-plataforma.
Tamanhos padrão: titulo 14 · secao 12 · corpo 11 · auxiliar 9.

A aplicação é MARCAÇÃO no estágio P0: aplicar_paleta registra o nome da
paleta como propriedade do workbook para rastreabilidade · não reformata
abas já escritas. As capabilities 3/4/5/7 consultam a paleta via
parâmetro explícito.
"""
from dataclasses import dataclass
from typing import Dict, Literal, Optional

from openpyxl import Workbook


NomePaleta = Literal["azul", "verde", "cinza", "vinho"]


@dataclass(frozen=True)
class Paleta:
    """Uma paleta executiva do catálogo canônico F-APRESENT (D-164).

    Imutável · hasheável · serve como parâmetro semântico para capabilities
    3/4/5/7. Todas as cores são hex RGB sem '#'.
    """
    nome: NomePaleta
    rotulo_user_facing: str
    semantica: str
    uso_sugerido: str

    cor_primaria: str
    cor_secundaria: str
    cor_texto_sobre_primaria: str
    cor_destaque: str
    cor_neutra_escura: str
    cor_neutra_clara: str

    fonte_familia: str
    fonte_tamanho_titulo: int
    fonte_tamanho_secao: int
    fonte_tamanho_corpo: int
    fonte_tamanho_auxiliar: int

    estilo_tabela: str  # TableStyleInfo name · consumido por capability 3


_TIPOGRAFIA_PADRAO = dict(
    fonte_familia="Calibri",
    fonte_tamanho_titulo=14,
    fonte_tamanho_secao=12,
    fonte_tamanho_corpo=11,
    fonte_tamanho_auxiliar=9,
)


CATALOGO_PALETAS: Dict[str, Paleta] = {
    "azul": Paleta(
        nome="azul",
        rotulo_user_facing="Azul executivo",
        semantica="Institucional padrão",
        uso_sugerido="Default universal · reuniões de diretoria · relatórios formais",
        cor_primaria="1F4E79",
        cor_secundaria="DDEBF7",
        cor_texto_sobre_primaria="FFFFFF",
        cor_destaque="0B2D4C",
        cor_neutra_escura="2F2F2F",
        cor_neutra_clara="BFBFBF",
        estilo_tabela="TableStyleMedium2",
        **_TIPOGRAFIA_PADRAO,
    ),
    "verde": Paleta(
        nome="verde",
        rotulo_user_facing="Verde executivo",
        semantica="Sustentabilidade · equilíbrio",
        uso_sugerido="Relatórios de performance positiva · ESG · operacional",
        cor_primaria="2E7D4F",
        cor_secundaria="E2F0E6",
        cor_texto_sobre_primaria="FFFFFF",
        cor_destaque="1B4D30",
        cor_neutra_escura="2F2F2F",
        cor_neutra_clara="BFBFBF",
        estilo_tabela="TableStyleMedium4",
        **_TIPOGRAFIA_PADRAO,
    ),
    "cinza": Paleta(
        nome="cinza",
        rotulo_user_facing="Cinza executivo",
        semantica="Neutro sóbrio",
        uso_sugerido="Relatórios monocromáticos · impressão preto e branco · apresentações densas",
        cor_primaria="595959",
        cor_secundaria="EDEDED",
        cor_texto_sobre_primaria="FFFFFF",
        cor_destaque="2F2F2F",
        cor_neutra_escura="1A1A1A",
        cor_neutra_clara="D9D9D9",
        estilo_tabela="TableStyleMedium1",
        **_TIPOGRAFIA_PADRAO,
    ),
    "vinho": Paleta(
        nome="vinho",
        rotulo_user_facing="Vinho executivo",
        semantica="Gravidade · alta senioridade",
        uso_sugerido="Relatórios de comitê · auditoria · posicionamento executivo elevado",
        cor_primaria="6D1F2D",
        cor_secundaria="F2E1E4",
        cor_texto_sobre_primaria="FFFFFF",
        cor_destaque="3F0F19",
        cor_neutra_escura="2F2F2F",
        cor_neutra_clara="BFBFBF",
        estilo_tabela="TableStyleMedium3",
        **_TIPOGRAFIA_PADRAO,
    ),
}


_MARCADOR_PALETA_NO_WORKBOOK = "tabloflow_paleta_nome"


def aplicar_paleta(workbook: Workbook, paleta: Paleta) -> None:
    """Aplica a paleta ao workbook como marcação semântica rastreável.

    Neste estágio P0 a aplicação é MARCAÇÃO. O nome da paleta é gravado
    em workbook.custom_doc_props (quando disponível) ou como atributo
    de instância `_tabloflow_paleta_nome`. Não reformata abas já escritas.

    Falha explícita (C.2):
      - workbook None → TypeError
      - paleta None ou fora do catálogo → ValueError
    """
    if workbook is None:
        raise TypeError("workbook não pode ser None em aplicar_paleta")
    if paleta is None:
        raise ValueError("paleta não pode ser None em aplicar_paleta")
    if paleta.nome not in CATALOGO_PALETAS:
        raise ValueError(
            f"paleta '{paleta.nome}' não está no catálogo canônico "
            f"(D-164 · catálogo fechado com 4 entradas)"
        )
    setattr(workbook, _MARCADOR_PALETA_NO_WORKBOOK, paleta.nome)


def paleta_aplicada(workbook: Workbook) -> Optional[str]:
    """Retorna o nome da paleta marcada no workbook · None se ausente."""
    if workbook is None:
        return None
    return getattr(workbook, _MARCADOR_PALETA_NO_WORKBOOK, None)


def obter_paleta(nome: str) -> Paleta:
    """Atalho: `CATALOGO_PALETAS[nome]` com erro explícito se ausente."""
    if nome not in CATALOGO_PALETAS:
        raise ValueError(
            f"paleta '{nome}' desconhecida · opções: {sorted(CATALOGO_PALETAS.keys())}"
        )
    return CATALOGO_PALETAS[nome]
