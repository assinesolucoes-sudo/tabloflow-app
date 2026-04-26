"""
t_fuzzy.py — Similaridade textual híbrida · T-FUZZY · D-050/D-052/D-138 · F.3
Algoritmo: trigramas (Jaccard) + tokens-chave. Pesos fixos internos (D-138).
API pura determinística: (texto_A, texto_B) → FuzzyScore ∈ [0, 1].
Proibido: fuzzywuzzy · rapidfuzz · jellyfish (D-138 · implementação declarada).
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Set

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.normalizacao_texto import extrair_tokens_chave, normalizar_texto

# Pesos internos fixos · D-138 · calibração da Fundação · alteração exige D-XXX
_PESO_TRIGRAMAS: float = 0.65
_PESO_TOKENS: float = 0.35
_BOOST_FATOR: float = 1.15
_BOOST_MIN_SCORE_TRIGRAMAS: float = 0.40


class FuzzyScore(BaseModel):
    score: float = Field(..., ge=0.0, le=1.0, description="Score em [0, 1]")
    texto_a_normalizado: str
    texto_b_normalizado: str
    tokens_chave_compartilhados: List[str]
    trigramas_comuns: int
    trigramas_total: int


def _gerar_trigramas(texto: str) -> Set[str]:
    """Gera conjunto de trigramas de caracteres a partir de texto normalizado."""
    if len(texto) < 3:
        return {texto} if texto else set()
    return {texto[i: i + 3] for i in range(len(texto) - 2)}


def calcular_score(texto_a: str, texto_b: str) -> FuzzyScore:
    """
    Função pura determinística · sem estado · sem side effects.
    API canônica: (texto_A, texto_B) → FuzzyScore.

    Algoritmo (D-138):
      1. Normalização interna via normalizacao_texto.py
      2. score_trigramas = Jaccard(trigramas_A, trigramas_B)
      3. tokens-chave: sequências numéricas >=4 dígitos + alphabéticas >=3 chars
      4. score_tokens = |tokens_A ∩ tokens_B| / max(|tokens_A ∪ tokens_B|, 1)
      5. score = 0.65 * trigramas + 0.35 * tokens
      6. Boost 15% se >=1 token compartilhado E score_trigramas >= 0.40
    """
    norm_a = normalizar_texto(texto_a)
    norm_b = normalizar_texto(texto_b)

    # Trigramas
    tri_a = _gerar_trigramas(norm_a)
    tri_b = _gerar_trigramas(norm_b)
    intersecao_tri = tri_a & tri_b
    uniao_tri = tri_a | tri_b
    n_comuns = len(intersecao_tri)
    n_total = len(uniao_tri)
    score_tri = n_comuns / n_total if n_total > 0 else (1.0 if not norm_a and not norm_b else 0.0)

    # Tokens-chave
    tokens_a = extrair_tokens_chave(norm_a)
    tokens_b = extrair_tokens_chave(norm_b)
    tokens_compartilhados = sorted(tokens_a & tokens_b)
    uniao_tokens = tokens_a | tokens_b
    score_tok = len(tokens_a & tokens_b) / max(len(uniao_tokens), 1)

    # Score combinado
    score_final = _PESO_TRIGRAMAS * score_tri + _PESO_TOKENS * score_tok

    # Boost condicional
    if tokens_compartilhados and score_tri >= _BOOST_MIN_SCORE_TRIGRAMAS:
        score_final = min(1.0, score_final * _BOOST_FATOR)

    return FuzzyScore(
        score=round(score_final, 6),
        texto_a_normalizado=norm_a,
        texto_b_normalizado=norm_b,
        tokens_chave_compartilhados=tokens_compartilhados,
        trigramas_comuns=n_comuns,
        trigramas_total=n_total,
    )


def extrair_tokens_chave_fuzzy(texto_normalizado: str) -> Set[str]:
    """
    Auxiliar exposto para debug.
    Reutiliza implementação canônica de normalizacao_texto.py.
    """
    return extrair_tokens_chave(texto_normalizado)
