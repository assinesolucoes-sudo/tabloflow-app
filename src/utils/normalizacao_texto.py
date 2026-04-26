"""
normalizacao_texto.py — Interface centralizada de normalização textual · D-139
Módulo consumido por T-FUZZY e T-CONCAT em F-TRANS.

Decisão D-139: centralizar normalização elimina duplicação e garante
determinismo C.1 — alteração desta normalização exige D-XXX nova por
afetar todos os consumidores (T-FUZZY e T-CONCAT simultaneamente).

AVISO F-MOT: Esta é a interface pública completa com implementação de referência.
F-TRANS irá validar os casos de regressão e estender se necessário.

Algoritmo de normalização (D-026 / F.3 T-FUZZY):
  1. strip()
  2. lower()
  3. remoção de acentos via unicodedata.normalize (substituto de unidecode)
  4. remoção de caracteres não-alfanuméricos exceto espaço
  5. colapso de espaços múltiplos em espaço único
"""
from __future__ import annotations

import re
import unicodedata


def _remover_acentos(texto: str) -> str:
    """Remove acentos e diacríticos via unicodedata NFD."""
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


def normalizar_texto(texto: str) -> str:
    """
    Normalização canônica para T-FUZZY e T-CONCAT · D-139.

    Passos:
      1. strip
      2. lower
      3. remoção de acentos (unicode NFD · substituto de unidecode)
      4. remoção de chars não-alfanuméricos exceto espaço
      5. colapso de espaços múltiplos

    Args:
        texto: String de entrada · qualquer encoding Python (str).

    Returns:
        String normalizada · apenas [a-z0-9 ] · espaços simples.

    Exemplos:
        >>> normalizar_texto("Pão de Açúcar S/A")
        'pao de acucar s a'
        >>> normalizar_texto("JOÃO DA SILVA  ")
        'joao da silva'
        >>> normalizar_texto("12.345.678/0001-90")
        '12345678000190'
    """
    if not isinstance(texto, str):
        texto = str(texto)
    resultado = texto.strip()
    resultado = resultado.lower()
    resultado = _remover_acentos(resultado)
    resultado = re.sub(r"[^a-z0-9\s]", "", resultado)
    resultado = re.sub(r"\s+", " ", resultado).strip()
    return resultado


def extrair_tokens_chave(texto_normalizado: str) -> set[str]:
    """
    Extrai tokens-chave de um texto já normalizado · auxiliar do T-FUZZY.

    Tokens extraídos:
      (a) sequências numéricas com >= 4 dígitos
      (b) sequências alfabéticas maiúsculas (pré-normalização) com >= 3 chars
          → após normalização: sequências alfabéticas com >= 3 chars

    Esta função espera texto já normalizado (lowercase · sem acentos).

    Args:
        texto_normalizado: Texto após normalizar_texto() · apenas [a-z0-9 ].

    Returns:
        Conjunto de tokens-chave · pode ser vazio.

    Exemplos:
        >>> extrair_tokens_chave("cnpj 12345678000190 ltda")
        {'12345678000190', 'cnpj', 'ltda'}
    """
    tokens: set[str] = set()

    # Sequências numéricas >= 4 dígitos
    for match in re.finditer(r"\d{4,}", texto_normalizado):
        tokens.add(match.group())

    # Sequências alfabéticas >= 3 chars
    for match in re.finditer(r"[a-z]{3,}", texto_normalizado):
        tokens.add(match.group())

    return tokens
