"""
F-APRESENT · Fundação · Subsistema de apresentação executiva (D-159).

Primitivas transversais consumidas por todas as 11 visões do Módulo 1
para garantir que o Excel entregue ao cliente seja user-facing puro ·
formatado · tabelado · com totais dinâmicos · vocabulário traduzido.

Capabilities P0:
  1. Catálogo de 4 paletas executivas       → paletas.py
  2. Rótulos user-facing universais          → vocabulario.py
  3. Tabela Excel nativa + totais dinâmicos  → tabelas.py
  4. Formatação monetária BR                 → formatos.py
  5. Formatação percentual                   → formatos.py
  6. Colunas adaptativas                     → colunas_adaptativas.py
  7. Resumo Executivo narrativo              → resumo_executivo.py

Capabilities P1:
  8. Badges semânticos                       → badges.py
  9. Hierarquia tipográfica                  → tipografia.py
  10. Diagnóstico narrativo 6 seções         → diagnostico_narrativo.py
"""

from .paletas import (
    CATALOGO_PALETAS,
    Paleta,
    aplicar_paleta,
    obter_paleta,
    paleta_aplicada,
)
from .vocabulario import (
    BLOCOS,
    carregar_vocabulario_bilingue,
    contem_marcador_traducao_ausente,
    eh_termo_proibido,
    traduzir,
)
from .tabelas import (
    FuncaoTotal,
    criar_tabela_executiva,
    estilo_para_paleta,
)
from .formatos import (
    FORMATO_CONTAGEM,
    FORMATO_DATA_BR,
    FORMATO_DATA_HORA_BR,
    FORMATO_MONETARIO_BR,
    FORMATO_PERCENTUAL,
    FORMATO_PERCENTUAL_LITERAL,
    THRESHOLDS_CONTRATO_FUNDACAO,
    aplicar_formato_contagem,
    aplicar_formato_data_br,
    aplicar_formato_data_hora_br,
    aplicar_formato_monetario,
    aplicar_formato_percentual,
    default_unidade_para_tipo_campo,
    formatar_data_br,
    formatar_moeda_br,
    formatar_percentual_br,
    formatar_threshold_por_contrato,
    formato_adaptativo_por_unidade,
)
from .colunas_adaptativas import (
    ColunaAdaptativa,
    CondicaoInclusao,
    UnidadeCampo,
    montar_colunas_adaptativas,
    se_config_diferente,
    se_config_igual,
    se_config_presente,
    sempre,
)
from .resumo_executivo import renderizar_resumo_executivo
from .badges import (
    BadgeStyle,
    CATALOGO_BADGES,
    MAPEAMENTO_V2,
    SEMANTICAS_CANONICAS,
    aplicar_badge,
)
from .tipografia import (
    APLICADORES,
    NIVEIS_CANONICOS,
    aplicar_campo,
    aplicar_hierarquia_tipografica,
    aplicar_nivel,
    aplicar_secao,
    aplicar_titulo_aba,
    aplicar_valor,
    escrever_campo_valor,
    escrever_secao,
    escrever_titulo_aba,
)
from .diagnostico_narrativo import (
    NOMES_SECOES,
    formatar_valor_ou_traco,
    renderizar_diagnostico,
)
from .graficos import (
    criar_grafico_distribuicao,
    criar_grafico_top_variacoes,
    gerar_nome_arquivo,
)

__all__ = [
    # Paletas
    "CATALOGO_PALETAS", "Paleta", "aplicar_paleta", "obter_paleta", "paleta_aplicada",
    # Vocabulário
    "BLOCOS", "carregar_vocabulario_bilingue", "contem_marcador_traducao_ausente",
    "eh_termo_proibido", "traduzir",
    # Tabelas
    "FuncaoTotal", "criar_tabela_executiva", "estilo_para_paleta",
    # Formatos
    "FORMATO_CONTAGEM", "FORMATO_DATA_BR", "FORMATO_DATA_HORA_BR",
    "FORMATO_MONETARIO_BR", "FORMATO_PERCENTUAL", "FORMATO_PERCENTUAL_LITERAL",
    "THRESHOLDS_CONTRATO_FUNDACAO",
    "aplicar_formato_contagem", "aplicar_formato_data_br",
    "aplicar_formato_data_hora_br", "aplicar_formato_monetario",
    "aplicar_formato_percentual", "default_unidade_para_tipo_campo",
    "formatar_data_br", "formatar_moeda_br", "formatar_percentual_br",
    "formatar_threshold_por_contrato", "formato_adaptativo_por_unidade",
    # Colunas adaptativas
    "ColunaAdaptativa", "CondicaoInclusao", "UnidadeCampo",
    "montar_colunas_adaptativas",
    "se_config_diferente", "se_config_igual", "se_config_presente", "sempre",
    # Resumo executivo
    "renderizar_resumo_executivo",
    # Badges (P1)
    "BadgeStyle", "CATALOGO_BADGES", "MAPEAMENTO_V2", "SEMANTICAS_CANONICAS",
    "aplicar_badge",
    # Tipografia (P1)
    "APLICADORES", "NIVEIS_CANONICOS",
    "aplicar_campo", "aplicar_hierarquia_tipografica", "aplicar_nivel",
    "aplicar_secao", "aplicar_titulo_aba", "aplicar_valor",
    "escrever_campo_valor", "escrever_secao", "escrever_titulo_aba",
    # Diagnóstico narrativo (P1)
    "NOMES_SECOES", "formatar_valor_ou_traco", "renderizar_diagnostico",
    # Gráficos + nomenclatura (capability 11 · D-176)
    "criar_grafico_distribuicao", "criar_grafico_top_variacoes", "gerar_nome_arquivo",
]
