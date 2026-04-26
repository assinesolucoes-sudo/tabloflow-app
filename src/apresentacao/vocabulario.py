"""
F-APRESENT · capability 2 · Rótulos user-facing universais (D-160 · D-161).

Consome specs/vocabulario_bilingue.md como fonte canônica · parseia em 7
blocos · expõe API de tradução e validação.

API:
  carregar_vocabulario_bilingue() → dict por bloco (cache module-level)
  traduzir(termo, contexto) → user-facing com fallback "[TERMO]" e warning
  eh_termo_proibido(valor) → None (ok) ou descrição da violação

Regra C.2: fallback NUNCA retorna termo técnico cru sem o marcador [...].
"""
from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Dict, Optional


_logger = logging.getLogger(__name__)

_CAMINHO_VOCABULARIO_PADRAO = Path(__file__).resolve().parent.parent.parent / "specs" / "vocabulario_bilingue.md"

# Chaves canônicas dos blocos retornados por carregar_vocabulario_bilingue
BLOCOS = (
    "stepper",
    "modos_base",
    "classificacoes",
    "tipos_campo",
    "thresholds",
    "warnings",
    "proibidos",
)

# Mapeamento de cabeçalho do markdown → chave de bloco
_CABECALHO_PARA_CHAVE = {
    "bloco 1": "stepper",
    "bloco 2": "modos_base",
    "bloco 3": "classificacoes",
    "bloco 4": "tipos_campo",
    "bloco 5": "thresholds",
    "bloco 6": "warnings",
    "bloco 7": "proibidos",
}

_cache_vocabulario: Optional[Dict[str, Dict[str, str]]] = None
_cache_caminho: Optional[Path] = None


def _chave_do_cabecalho(linha: str) -> Optional[str]:
    """Detecta cabeçalhos `## N · Bloco N · ...` e retorna a chave canônica."""
    texto = linha.strip().lower()
    if not texto.startswith("##"):
        return None
    for cab, chave in _CABECALHO_PARA_CHAVE.items():
        if cab in texto:
            return chave
    return None


def _parsear_tabela_markdown(linhas: list[str]) -> Dict[str, str]:
    """Extrai linhas tabela |a|b| em dict · ignora header e separador."""
    resultado: Dict[str, str] = {}
    for ln in linhas:
        if "|" not in ln:
            continue
        celulas = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(celulas) < 2:
            continue
        chave, valor = celulas[0], celulas[1]
        if not chave or not valor:
            continue
        if chave.lower() in ("código técnico", "padrão técnico") or set(chave) <= {"-", " "}:
            continue
        resultado[chave] = valor
    return resultado


def _parsear_bloco_proibidos(texto: str) -> Dict[str, str]:
    """
    Extrai o bloco 7 (lista negativa) em dict {padrao_proibido: motivo}.

    Cada sub-bloco ### 8.X tem bullets · extraímos literais em ``backticks``.
    Chave = literal extraído · valor = contexto da subseção.
    """
    proibidos: Dict[str, str] = {}

    # Quebra por subseções ### 8.1 · ...
    subsecoes = re.split(r"^### (8\.\d)\s*·\s*(.+?)$", texto, flags=re.MULTILINE)
    # split com 2 grupos: [pre, num1, titulo1, conteudo1, num2, titulo2, conteudo2, ...]
    for i in range(1, len(subsecoes), 3):
        num = subsecoes[i].strip()
        titulo = subsecoes[i + 1].strip()
        conteudo = subsecoes[i + 2] if i + 2 < len(subsecoes) else ""

        motivo = f"{num} · {titulo}"

        # Extrai cada literal em ``backticks``
        for m in re.finditer(r"`([^`]+)`", conteudo):
            literal = m.group(1).strip()
            if not literal:
                continue
            proibidos[literal] = motivo

    return proibidos


def carregar_vocabulario_bilingue(
    caminho: Optional[Path] = None,
) -> Dict[str, Dict[str, str]]:
    """
    Lê e parseia vocabulario_bilingue.md · retorna dict por bloco.

    Estrutura de retorno:
    {
        "stepper":        {"E1": "Escolher arquivo", ...},
        "modos_base":     {"TRANSACIONAL": "Base transacional ...", ...},
        "classificacoes": {"PRESENTE_AMBOS": "Presente nos dois lados", ...},
        "tipos_campo":    {"NUMERICO_ADITIVO": "Valor somável (...)", ...},
        "thresholds":     {"limiar_estabilidade_pct": "Limite de estabilidade (...)", ...},
        "warnings":       {"W-V*-AUSENCIA-*": "Ausência detectada em [detalhe]", ...},
        "proibidos":      {padrao: "motivo", ...},
    }

    Cache module-level · uma leitura por processo para o mesmo caminho.
    Warning em log se caminho inexistente · FileNotFoundError se inválido.
    """
    global _cache_vocabulario, _cache_caminho

    destino = caminho if caminho is not None else _CAMINHO_VOCABULARIO_PADRAO

    if _cache_vocabulario is not None and _cache_caminho == destino:
        return _cache_vocabulario

    if not destino.exists():
        _logger.warning(
            "vocabulario_bilingue.md não encontrado em %s · F-APRESENT exige o arquivo",
            destino,
        )
        raise FileNotFoundError(f"vocabulario_bilingue.md ausente: {destino}")

    texto = destino.read_text(encoding="utf-8")

    # Inicializa estrutura
    resultado: Dict[str, Dict[str, str]] = {chave: {} for chave in BLOCOS}

    # Parsing linha-a-linha · identificando bloco ativo
    linhas = texto.splitlines()
    bloco_atual: Optional[str] = None
    buffer_bloco: list[str] = []
    buffer_texto: list[str] = []  # para proibidos · precisa do texto bruto

    def flush_bloco() -> None:
        if bloco_atual is None:
            return
        if bloco_atual == "proibidos":
            resultado["proibidos"].update(_parsear_bloco_proibidos("\n".join(buffer_texto)))
        else:
            resultado[bloco_atual].update(_parsear_tabela_markdown(buffer_bloco))

    for linha in linhas:
        nova_chave = _chave_do_cabecalho(linha)
        if nova_chave is not None:
            flush_bloco()
            bloco_atual = nova_chave
            buffer_bloco = []
            buffer_texto = []
            continue
        if bloco_atual is not None:
            buffer_bloco.append(linha)
            buffer_texto.append(linha)

    flush_bloco()

    # Validação C.2: blocos esperados presentes
    for chave in BLOCOS:
        if not resultado[chave]:
            _logger.warning(
                "bloco '%s' do vocabulario_bilingue.md veio vazio · formato pode ter mudado",
                chave,
            )

    _cache_vocabulario = resultado
    _cache_caminho = destino
    return resultado


def _limpar_cache() -> None:
    """Helper de teste · invalida cache para permitir reload."""
    global _cache_vocabulario, _cache_caminho
    _cache_vocabulario = None
    _cache_caminho = None


def traduzir(
    termo_tecnico: str,
    contexto: Optional[str] = None,
    vocabulario: Optional[Dict[str, Dict[str, str]]] = None,
) -> str:
    """
    Traduz termo técnico para user-facing.

    `contexto` opcional restringe busca a um bloco específico (ex:
    "classificacoes", "modos_base", "thresholds").

    Fallback (C.2): termo ausente retorna "[TERMO]" com marcador literal e
    emite warning em log. NUNCA retorna o termo cru sem colchetes · isso
    seria fallback silencioso.
    """
    if vocabulario is None:
        vocabulario = carregar_vocabulario_bilingue()

    if contexto is not None:
        bloco = vocabulario.get(contexto, {})
        if termo_tecnico in bloco:
            return bloco[termo_tecnico]
        _logger.warning(
            "tradução ausente · contexto='%s' · termo='%s' · fallback [%s]",
            contexto, termo_tecnico, termo_tecnico,
        )
        return f"[{termo_tecnico}]"

    # Sem contexto: tenta todos os blocos exceto "proibidos"
    for chave, bloco in vocabulario.items():
        if chave == "proibidos":
            continue
        if termo_tecnico in bloco:
            return bloco[termo_tecnico]

    _logger.warning(
        "tradução ausente · termo='%s' · todos os blocos · fallback [%s]",
        termo_tecnico, termo_tecnico,
    )
    return f"[{termo_tecnico}]"


# ---------------------------------------------------------------------------
# Detecção de termos proibidos (bloco 7 · lista negativa)
# ---------------------------------------------------------------------------

# Padrões regex complementares ao dict "proibidos"
_REGEX_DATETIME_PY = re.compile(r"datetime\.datetime\s*\(")
_REGEX_DICT_PY = re.compile(r"\{\s*['\"]\w+['\"]\s*:")
_REGEX_LISTA_PY = re.compile(r"\[\s*['\"][^'\"]+['\"]\s*,")
_REGEX_CODIGO_D = re.compile(r"\bD-\d{2,}\b")
_REGEX_CODIGO_PVN = re.compile(r"\bP-V\d+-[A-Za-z0-9\-]+\b")
_REGEX_CODIGO_OBS = re.compile(r"\bOBS-VV-V\d+-\d+\b")
_REGEX_CODIGO_T = re.compile(r"\bT-[A-Z]{3,}\b")
_REGEX_CODIGO_F = re.compile(r"\bF-[A-Z]{3,}\b")
_REGEX_CAPS_SNAKE = re.compile(r"\b[A-Z]{3,}(?:_[A-Z0-9]+)+\b")

# Enums canônicos conhecidos (bloco 8.2)
_ENUMS_PROIBIDOS = {
    "POR_COLUNAS", "POR_LINHAS",
    "PRESENTE_AMBOS", "AUSENTE_ORIGEM", "AUSENTE_COMPARADO",
    "NULO_ORIGEM", "NULO_COMPARADO", "NULO_AMBOS",
    "TRANSACIONAL", "PRE_AGREGADO", "INDIVIDUAL", "CONSOLIDADA",
    "NUMERICO_ADITIVO", "NUMERICO_RELATIVO", "NUMERICO_NAO_ADITIVO",
    "CATEGORICO", "BOOLEANO",
    "SIMPLES", "DUAL",
}

# Atributos Python literais conhecidos (bloco 8.1)
_ATRIBUTOS_PROIBIDOS = {
    "campo_analisado",
    "origem_rotulo_ux", "origem_rotulo_tecnico",
    "comparado_rotulo_ux", "comparado_rotulo_tecnico",
    "limiar_estabilidade_pct",
    "limite_variacao_extrema",
    "tipo_estrutural",
    "classificacao_estrutural", "classificacao_semantica",
    "chave_agrupadores", "valor_origem", "valor_comparado",
    "variacao_percentual", "diferenca",
    "estrutura_entrada",
}


def eh_termo_proibido(
    valor: str,
    vocabulario: Optional[Dict[str, Dict[str, str]]] = None,
) -> Optional[str]:
    """
    Verifica se um valor contém padrão proibido (bloco 7).

    Retorna None (valor ok) ou string descritiva da violação.

    Padrões verificados:
      - datetime.datetime(...)
      - dict Python serializado
      - Lista Python crua
      - Códigos D-XXX · P-VN-NN · OBS-VV-VN-NN · T-* · F-*
      - Enums canônicos em CAPS_SNAKE_CASE
      - Nomes de atributo Python literais (snake_case da lista canônica)

    Marcador de tradução ausente "[TERMO]" NÃO é violação · é sinal
    intencional (C.2) para que testes de invariante o identifiquem.
    """
    if not isinstance(valor, str):
        return None
    if not valor.strip():
        return None

    # Whitelist: marcador de tradução ausente [...] não é violação,
    # porque capturamos este caso antes (teste de invariante pode
    # detectar marcadores se quiser, via outra função).
    # Aqui só bloqueamos padrões técnicos crus.

    # 8.4 · datetime
    if _REGEX_DATETIME_PY.search(valor):
        return "8.4 · datetime.datetime(...) cru"

    # 8.4 · dict Python
    if _REGEX_DICT_PY.search(valor):
        return "8.4 · dict Python serializado"

    # 8.4 · lista Python
    if _REGEX_LISTA_PY.search(valor):
        return "8.4 · lista Python crua"

    # 8.3 · códigos internos
    if _REGEX_CODIGO_D.search(valor):
        return "8.3 · código D-XXX"
    if _REGEX_CODIGO_PVN.search(valor):
        return "8.3 · código P-VN-NN"
    if _REGEX_CODIGO_OBS.search(valor):
        return "8.3 · código OBS-VV-VN-NN"
    if _REGEX_CODIGO_T.search(valor):
        return "8.3 · código T-XXX"
    if _REGEX_CODIGO_F.search(valor):
        return "8.3 · código F-XXX"

    # 8.2 · enums em caps · checagem por tokens (word boundary)
    tokens = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", valor))
    intersec_enum = tokens & _ENUMS_PROIBIDOS
    if intersec_enum:
        return f"8.2 · enum em caps: {sorted(intersec_enum)[0]}"

    # 8.2 genérico · qualquer CAPS_SNAKE 3+ letras com underscore
    m_caps = _REGEX_CAPS_SNAKE.search(valor)
    if m_caps:
        # Permite alguns ruídos user-facing comuns como "R$" (não casaria)
        return f"8.2 · CAPS_SNAKE genérico: {m_caps.group(0)}"

    # 8.1 · atributos Python · termo isolado (não parte de palavra maior)
    palavras = re.findall(r"[a-z_]+", valor.lower())
    intersec_attr = set(palavras) & _ATRIBUTOS_PROIBIDOS
    if intersec_attr:
        return f"8.1 · atributo Python: {sorted(intersec_attr)[0]}"

    # 8.1 · heurística genérica: snake_case com 2+ underscores
    # (ex: tem_bloqueios_escapados · warnings_por_categoria)
    for palavra in palavras:
        if palavra.count("_") >= 2 and palavra.islower():
            return f"8.1 · snake_case de 3+ partes: {palavra}"

    return None


def contem_marcador_traducao_ausente(valor: str) -> bool:
    """
    Detecta marcador de tradução ausente `[TERMO_TECNICO]`.

    Usado pela suite de invariantes do capability 7 para validar que
    todas as traduções necessárias estão presentes.
    """
    if not isinstance(valor, str):
        return False
    return bool(re.search(r"\[[A-Z][A-Z0-9_]{2,}\]", valor))
