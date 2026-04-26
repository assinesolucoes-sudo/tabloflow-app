"""
F-APRESENT · capabilities 4 e 5 · Formatação monetária BR e percentual (D-166).

Constantes canônicas de number_format Excel · helpers que aplicam em iteráveis
de Cell. Nenhuma dependência de Paleta · funções puras.

Princípio D-166:
  - Valor monetário BR sempre com "R$" e separadores locais.
  - Percentual sempre com "%" · conversão fração→percentual NATIVA do Excel
    via formato '0.00%' (0.0108 → "1.08%").
  - Zero representado como "-" (travessão) para leitura executiva limpa.
  - Negativo em vermelho via [Red].
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, Optional, Tuple

from openpyxl.cell.cell import Cell


# Formatos canônicos D-166
FORMATO_MONETARIO_BR = 'R$ #,##0.00;[Red](R$ #,##0.00);-'
FORMATO_PERCENTUAL = '0.00%;[Red]-0.00%;-'
FORMATO_PERCENTUAL_LITERAL = '0.00"%";[Red]-0.00"%";-'
FORMATO_CONTAGEM = '#,##0;[Red]-#,##0;-'
FORMATO_DATA_BR = "dd/mm/yyyy"
FORMATO_DATA_HORA_BR = "dd/mm/yyyy hh:mm"


def _iterar_celulas(fonte: Iterable) -> Iterable[Cell]:
    """Normaliza fonte: aceita Cell, iterável de Cell, ou iterável de iterável."""
    for item in fonte:
        if isinstance(item, Cell):
            yield item
        elif hasattr(item, "__iter__"):
            for sub in item:
                if isinstance(sub, Cell):
                    yield sub


def aplicar_formato_monetario(celulas: Iterable) -> int:
    """
    Aplica FORMATO_MONETARIO_BR a cada célula do iterável.
    Retorna a contagem de células afetadas.

    Não converte valores · apenas number_format. Se célula contém string,
    aplica mesmo assim (Excel ignora · sem raise).
    """
    total = 0
    for celula in _iterar_celulas(celulas):
        celula.number_format = FORMATO_MONETARIO_BR
        total += 1
    return total


def aplicar_formato_percentual(
    celulas: Iterable,
    conversao_fracao: bool = True,
) -> int:
    """
    Aplica formato percentual a cada célula do iterável.

    conversao_fracao=True (padrão): usa '0.00%' · o formato NATIVO do Excel
    multiplica visualmente por 100 (0.0108 → "1.08%"). Valor armazenado
    permanece fração.

    conversao_fracao=False: usa '0.00"%"' · valor literal é exibido com
    sinal "%" ao lado (0.01 armazenado → "0.01%"). Útil quando os dados
    já vêm como percentual inteiro e não como fração.
    """
    formato = FORMATO_PERCENTUAL if conversao_fracao else FORMATO_PERCENTUAL_LITERAL
    total = 0
    for celula in _iterar_celulas(celulas):
        celula.number_format = formato
        total += 1
    return total


def aplicar_formato_contagem(celulas: Iterable) -> int:
    """Formato de contagem inteira com separador BR · negativo em vermelho."""
    total = 0
    for celula in _iterar_celulas(celulas):
        celula.number_format = FORMATO_CONTAGEM
        total += 1
    return total


def aplicar_formato_data_br(celulas: Iterable) -> int:
    """Formato dd/mm/yyyy para datas."""
    total = 0
    for celula in _iterar_celulas(celulas):
        celula.number_format = FORMATO_DATA_BR
        total += 1
    return total


def aplicar_formato_data_hora_br(celulas: Iterable) -> int:
    """Formato dd/mm/yyyy hh:mm para datas com hora."""
    total = 0
    for celula in _iterar_celulas(celulas):
        celula.number_format = FORMATO_DATA_HORA_BR
        total += 1
    return total


def formatar_data_br(data) -> str:
    """
    Converte datetime em string BR "dd/mm/yyyy · hh:mm".

    Usado para renderização de cabeçalhos narrativos (não para células
    com number_format · usar aplicar_formato_data_hora_br nesse caso).
    """
    if data is None:
        return "-"
    return f"{data.day:02d}/{data.month:02d}/{data.year:04d} · {data.hour:02d}:{data.minute:02d}"


def formatar_moeda_br(valor) -> str:
    """
    Converte número em string "R$ 1.234,56" para uso em narrativas.

    Preserva "-" para zero ou None · "(R$ 1.234,56)" para negativos em
    contexto onde vermelho não está disponível (string de narrativa).
    """
    if valor is None:
        return "-"
    try:
        n = float(valor)
    except (TypeError, ValueError):
        return str(valor)
    if n == 0:
        return "-"
    neg = n < 0
    n = abs(n)
    inteiro = int(n)
    centavos = round((n - inteiro) * 100)
    if centavos == 100:
        inteiro += 1
        centavos = 0
    # Separador milhar BR: "."
    inteiro_str = f"{inteiro:,}".replace(",", ".")
    texto = f"R$ {inteiro_str},{centavos:02d}"
    return f"({texto})" if neg else texto


def formatar_percentual_br(valor, conversao_fracao: bool = True) -> str:
    """Converte fração em string "12,34%" para narrativas."""
    if valor is None:
        return "-"
    try:
        n = float(valor)
    except (TypeError, ValueError):
        return str(valor)
    if conversao_fracao:
        n = n * 100
    if n == 0:
        return "-"
    # vírgula como separador decimal BR
    texto = f"{abs(n):.2f}".replace(".", ",")
    return f"-{texto}%" if n < 0 else f"{texto}%"


# ---------------------------------------------------------------------------
# Despacho por unidade (E1 / D-190 · C.D8)
# ---------------------------------------------------------------------------
#
# Tabela canônica: cada unidade declarada em ComparacaoV2.unidade resolve para
# um trio coerente (formato do valor · formato da diferença · formato da variação)
# e dois rótulos user-facing (label da diferença · label da variação).
#
# `MONETARIO_BRL` preserva integralmente o comportamento anterior à Sessão 8:
# qualquer base com unidade default produz Excel idêntico ao da Sessão 4-ter-bis.
# ---------------------------------------------------------------------------


# Formato base do valor (origem · comparado · total) por unidade
_NF_VALOR: dict = {
    "MONETARIO_BRL": FORMATO_MONETARIO_BR,
    "PERCENTUAL":    FORMATO_PERCENTUAL,
    "QUANTIDADE":    FORMATO_CONTAGEM,
    "TEMPO_DIAS":    '#,##0 "dias";[Red]-#,##0 "dias";-',
    "TEMPO_HORAS":   '#,##0 "h";[Red]-#,##0 "h";-',
    "MULTIPLICADOR": '0.00"x";[Red]-0.00"x";-',
    "RAZAO":         '0.0000;[Red]-0.0000;-',
    "ADIMENSIONAL":  '#,##0.00;[Red]-#,##0.00;-',
}

# Formato da DIFERENÇA por unidade
# Sessão 8.1 · C-1: PERCENTUAL usa formato p.p LITERAL · sem multiplicação Excel.
# Caller (F-APRESENT) deve aplicar `valor_diferenca_para_celula` ao valor cru
# antes de escrever na célula · garantindo que cabeçalho ("Variação absoluta (p.p)")
# e valor renderizado ("+5,00 p.p") falem a mesma língua.
_NF_DIFERENCA: dict = {
    "MONETARIO_BRL": FORMATO_MONETARIO_BR,
    "PERCENTUAL":    '+0.00" p.p";[Red]-0.00" p.p";-',
    "QUANTIDADE":    FORMATO_CONTAGEM,
    "TEMPO_DIAS":    '#,##0 "dias";[Red]-#,##0 "dias";-',
    "TEMPO_HORAS":   '#,##0 "h";[Red]-#,##0 "h";-',
    "MULTIPLICADOR": '0.00"x";[Red]-0.00"x";-',
    "RAZAO":         '0.0000;[Red]-0.0000;-',
    "ADIMENSIONAL":  '#,##0.00;[Red]-#,##0.00;-',
}

# Formato da VARIAÇÃO RELATIVA · sempre percentual exceto para ESTADO/ADIMENSIONAL
_NF_VARIACAO: dict = {
    "MONETARIO_BRL": FORMATO_PERCENTUAL,
    "PERCENTUAL":    FORMATO_PERCENTUAL,
    "QUANTIDADE":    FORMATO_PERCENTUAL,
    "TEMPO_DIAS":    FORMATO_PERCENTUAL,
    "TEMPO_HORAS":   FORMATO_PERCENTUAL,
    "MULTIPLICADOR": FORMATO_PERCENTUAL,
    "RAZAO":         FORMATO_PERCENTUAL,
    "ADIMENSIONAL":  FORMATO_PERCENTUAL,
}

_LABEL_DIFERENCA: dict = {
    "MONETARIO_BRL": "Diferença",
    "PERCENTUAL":    "Variação absoluta (p.p)",
    "QUANTIDADE":    "Diferença",
    "TEMPO_DIAS":    "Diferença (dias)",
    "TEMPO_HORAS":   "Diferença (h)",
    "MULTIPLICADOR": "Diferença",
    "RAZAO":         "Diferença",
    "ADIMENSIONAL":  "Diferença",
}

_LABEL_VARIACAO: dict = {
    "MONETARIO_BRL": "Variação %",
    "PERCENTUAL":    "Variação relativa (%)",
    "QUANTIDADE":    "Variação %",
    "TEMPO_DIAS":    "Variação %",
    "TEMPO_HORAS":   "Variação %",
    "MULTIPLICADOR": "Variação %",
    "RAZAO":         "Variação %",
    "ADIMENSIONAL":  "Variação %",
}


# Contrato canônico de thresholds · D-166 · D-202.
# Promovido de `visoes.exportacao_v2._THRESHOLDS_CONTRATO` em D-202.
# Cada chave mapeia para (rótulo user-facing, unidade canônica).
# Unidade "percentual" indica armazenamento em fração (0.01 = 1%) ou
# literal (10.0 = 10%) — heurística de detecção em
# `formatar_threshold_por_contrato`.
THRESHOLDS_CONTRATO_FUNDACAO: Dict[str, Tuple[str, str]] = {
    "limiar_estabilidade_pct":             ("Limite de estabilidade", "percentual"),
    "limiar_nulo_massivo_pct":             ("Limite de nulos massivos", "percentual"),
    "limite_valores_discriminador_alerta": ("Limite de valores na coluna de comparação", "contagem"),
    "limite_variacao_extrema":             ("Limite de variação extrema", "percentual"),
    "limite_variacao_extrema_pct":         ("Limite de variação extrema", "percentual"),
}


def formatar_threshold_por_contrato(
    chave: str,
    valor: Any,
) -> Tuple[str, str]:
    """Formata threshold respeitando o contrato D-166 · D-202.

    Retorna (rótulo user-facing, valor formatado).

    - Chaves desconhecidas caem em humanização best-effort com unidade percentual.
    - Contagens exibem inteiro formatado BR; `None` vira "—".
    - Percentuais: heurística de unidade
        |valor| < 1.0 → fração (0.01 → "1,00%")
        |valor| >= 1.0 → literal (10.0 → "10,00%")
      Resolve descompasso do app_v2 que armazena `limite_variacao_extrema_pct`
      como literal enquanto demais usam fração · sem alterar dado em sessão.
    """
    if chave in THRESHOLDS_CONTRATO_FUNDACAO:
        rotulo, unidade = THRESHOLDS_CONTRATO_FUNDACAO[chave]
    else:
        rotulo = chave.replace("_", " ")
        unidade = "percentual"
    if valor is None:
        return rotulo, "—"
    if unidade == "contagem":
        try:
            v_int = int(valor)
            return rotulo, f"{v_int:,}".replace(",", ".")
        except (TypeError, ValueError):
            return rotulo, str(valor)
    # percentual com heurística fração vs literal
    try:
        v_float = float(valor)
    except (TypeError, ValueError):
        return rotulo, str(valor)
    if abs(v_float) < 1.0:
        return rotulo, formatar_percentual_br(v_float, conversao_fracao=True)
    return rotulo, formatar_percentual_br(v_float / 100.0, conversao_fracao=True)


# ===========================================================================
# Capability 11 · Formato adaptativo por unidade · D-205 · D-202 etapa 7
# ===========================================================================

# Tabela canônica · D-205 · regras de formatação adaptativa por unidade.
# - casas_default: casas decimais aplicadas no formato base.
# - casas_adaptativo: None quando unidade não adapta · int para alternar para
#   esse número de casas quando valor real tem fração ≥0.5.
# - regra_nota_tecnica:
#     "delta_centavos_material_em_pct": MONETARIO · diferença de centavos é
#         pequena em valor absoluto mas pode ser grande em variação relativa.
#     "variacao_geq_5pct_e_arredondados_iguais": QUANTIDADE/TEMPO · valores
#         arredondados podem parecer iguais quando variação real ≥5%.
#     "casos_extremos_apenas": MULTIPLICADOR · só em casos extremos.
#     None: nunca emite nota técnica.
_REGRAS_FORMATO_ADAPTATIVO: Dict[str, Dict[str, Any]] = {
    "MONETARIO_BRL": {
        "casas_default": 2,
        "casas_adaptativo": None,
        "regra_nota_tecnica": "delta_centavos_material_em_pct",
    },
    "PERCENTUAL": {
        "casas_default": 2,
        "casas_adaptativo": None,
        "regra_nota_tecnica": None,
    },
    "QUANTIDADE": {
        "casas_default": 0,
        "casas_adaptativo": 1,
        "regra_nota_tecnica": "variacao_geq_5pct_e_arredondados_iguais",
    },
    "TEMPO_DIAS": {
        "casas_default": 0,
        "casas_adaptativo": 1,
        "regra_nota_tecnica": "variacao_geq_5pct_e_arredondados_iguais",
    },
    "TEMPO_HORAS": {
        "casas_default": 0,
        "casas_adaptativo": 1,
        "regra_nota_tecnica": "variacao_geq_5pct_e_arredondados_iguais",
    },
    "MULTIPLICADOR": {
        "casas_default": 2,
        "casas_adaptativo": None,
        "regra_nota_tecnica": "casos_extremos_apenas",
    },
    "RAZAO": {
        "casas_default": 4,
        "casas_adaptativo": None,
        "regra_nota_tecnica": None,
    },
    "ADIMENSIONAL": {
        "casas_default": 2,
        "casas_adaptativo": None,
        "regra_nota_tecnica": None,
    },
}

# Sufixo de unidade aplicado após o valor formatado (capability 11 só formata
# valor cru · independente de fmt Excel · função pura para uso em prosa).
_SUFIXOS_UNIDADE: Dict[str, str] = {
    "MONETARIO_BRL": "",
    "PERCENTUAL":    "%",
    "QUANTIDADE":    "",
    "TEMPO_DIAS":    "d",
    "TEMPO_HORAS":   "h",
    "MULTIPLICADOR": "x",
    "RAZAO":         "",
    "ADIMENSIONAL":  "",
}


def _formatar_numero_br(valor: float, casas: int) -> str:
    """Formata float com vírgula decimal e ponto de milhar BR."""
    fmt = f"{{:,.{casas}f}}"
    bruto = fmt.format(valor)
    return bruto.replace(",", "@").replace(".", ",").replace("@", ".")


def formato_adaptativo_por_unidade(
    valor: Optional[float],
    unidade: str,
    contexto_variacao_pct: Optional[float] = None,
    contexto_arredondados_iguais: bool = False,
) -> Tuple[str, Optional[str]]:
    """D-205 · capability 11 de F-APRESENT · formato adaptativo por unidade.

    Retorna (string formatada, nota técnica opcional).

    - Casas decimais default por unidade (tabela `_REGRAS_FORMATO_ADAPTATIVO`).
    - Adaptação se unidade tem `casas_adaptativo` e valor real tem fração relevante
      (|fração| ≥ 0.5 → alterna para `casas_adaptativo`).
    - Nota técnica condicional quando o arredondamento esconde variação material:
        "variacao_geq_5pct_e_arredondados_iguais" · QUANTIDADE/TEMPO ·
        contexto_variacao_pct (em decimal · 0.06 = 6%) e
        contexto_arredondados_iguais=True (caller detectou o caso).

    Sinal preservado · prefixo R$ NÃO adicionado (capability monetária dedicada
    em formatar_moeda_br) · função foca em precisão decimal.
    """
    if unidade not in _REGRAS_FORMATO_ADAPTATIVO:
        unidade = "MONETARIO_BRL"
    regras = _REGRAS_FORMATO_ADAPTATIVO[unidade]

    if valor is None:
        return "—", None

    casas = int(regras["casas_default"])
    casas_adapt = regras["casas_adaptativo"]
    if casas_adapt is not None:
        try:
            valor_abs = abs(float(valor))
            fracao = valor_abs - int(valor_abs)
        except (TypeError, ValueError):
            fracao = 0.0
        if fracao >= 0.5 - 1e-9:
            casas = int(casas_adapt)

    sufixo = _SUFIXOS_UNIDADE.get(unidade, "")
    texto = _formatar_numero_br(valor, casas) + sufixo

    nota: Optional[str] = None
    regra = regras.get("regra_nota_tecnica")
    if regra == "variacao_geq_5pct_e_arredondados_iguais":
        if (
            contexto_arredondados_iguais
            and contexto_variacao_pct is not None
            and abs(contexto_variacao_pct) >= 0.05 - 1e-9
        ):
            sinal_pct = formatar_percentual_br(contexto_variacao_pct, conversao_fracao=True)
            nota = (
                f"Variação real é {sinal_pct} · valores arredondados podem parecer iguais"
            )

    return texto, nota


def default_unidade_para_tipo_campo(tipo_campo: str) -> str:
    """Default declarado de `unidade` derivado de `tipo_campo` · D-190 · DDU.

    Movido de `visoes.visao_v2._default_unidade_para_tipo` e
    `app_v2._unidade_default_por_tipo` em D-202 · deduplicação.
    """
    if tipo_campo == "NUMERICO_RELATIVO":
        return "PERCENTUAL"
    if tipo_campo == "ESTADO_SITUACAO":
        return "ADIMENSIONAL"
    return "MONETARIO_BRL"


def number_format_valor(unidade: str) -> str:
    """Number format Excel para valores de origem · comparado · total · totalsRow."""
    return _NF_VALOR.get(unidade or "MONETARIO_BRL", FORMATO_MONETARIO_BR)


def number_format_diferenca(unidade: str) -> str:
    """Number format Excel para a coluna `diferenca` segundo a unidade."""
    return _NF_DIFERENCA.get(unidade or "MONETARIO_BRL", FORMATO_MONETARIO_BR)


def number_format_variacao(unidade: str) -> str:
    """Number format Excel para a coluna `variacao_percentual` segundo a unidade."""
    return _NF_VARIACAO.get(unidade or "MONETARIO_BRL", FORMATO_PERCENTUAL)


def rotulo_diferenca(unidade: str) -> str:
    """Rótulo user-facing da coluna 'Diferença' segundo a unidade."""
    return _LABEL_DIFERENCA.get(unidade or "MONETARIO_BRL", "Diferença")


def rotulo_variacao(unidade: str) -> str:
    """Rótulo user-facing da coluna 'Variação %' segundo a unidade."""
    return _LABEL_VARIACAO.get(unidade or "MONETARIO_BRL", "Variação %")


def label_total_card(unidade: str) -> str:
    """Rótulo do card de total no Resumo Executivo · 'Média' para PERCENTUAL."""
    return "Média" if unidade == "PERCENTUAL" else "Total"


def valor_total_card(total_soma: Optional[float], count_presente: int, unidade: str) -> Optional[float]:
    """Valor exibido no card · média ponderada simples para PERCENTUAL · soma para os demais."""
    if total_soma is None:
        return None
    if unidade == "PERCENTUAL" and count_presente > 0:
        return total_soma / count_presente
    return total_soma


def valor_diferenca_para_celula(valor_raw, unidade: str):
    """
    Sessão 8.1 · C-1 · Converte valor cru de `diferenca` em valor a ser
    escrito na célula Excel, considerando a unidade.

    Para PERCENTUAL: motor armazena `comparado - origem` em fração (ex. -0.05).
    Multiplicamos por 100 aqui (-5.0) para que o formato literal '+0.00" p.p"'
    renderize visualmente "-5,00 p.p" · cabeçalho "Variação absoluta (p.p)"
    fala a mesma língua.

    Para outras unidades: valor preserva (sem multiplicação).
    """
    if valor_raw is None:
        return None
    try:
        v = float(valor_raw)
    except (TypeError, ValueError):
        return valor_raw
    if unidade == "PERCENTUAL":
        return v * 100.0
    return v


def formatar_diferenca_por_unidade(valor, unidade: str) -> str:
    """
    Sessão 8.1 · C-1 · Renderiza valor de DIFERENÇA como string user-facing
    segundo a unidade · com sinal explícito para narrativa (não parênteses).

    Para PERCENTUAL: valor cru é fração (-0.05); renderiza como "-5,00 p.p".
    Para MONETARIO_BRL: "+R$ 981,49" / "-R$ 178,31" (não usa parênteses
    para negativo, evita "((R$ 178,31))" em narrativas que envolvem o valor
    em parênteses adicionais).
    Demais unidades: delega a `formatar_valor_por_unidade` (que já produz
    sinal explícito ou prefixo "-" para negativos).
    """
    if valor is None:
        return "-"
    if unidade == "PERCENTUAL":
        try:
            n = float(valor) * 100.0
        except (TypeError, ValueError):
            return str(valor)
        if n == 0:
            return "-"
        sinal = "-" if n < 0 else "+"
        texto = f"{abs(n):.2f}".replace(".", ",")
        return f"{sinal}{texto} p.p"
    if unidade == "MONETARIO_BRL":
        try:
            n = float(valor)
        except (TypeError, ValueError):
            return str(valor)
        if n == 0:
            return "-"
        sinal = "-" if n < 0 else "+"
        # formatar_moeda_br aceita valor positivo · adiciona sinal explícito
        texto = formatar_moeda_br(abs(n))
        return f"{sinal}{texto}"
    return formatar_valor_por_unidade(valor, unidade)


def formatar_valor_por_unidade(valor, unidade: str) -> str:
    """Renderiza valor escalar como string user-facing segundo a unidade · usado em narrativas."""
    if valor is None:
        return "-"
    if unidade == "MONETARIO_BRL":
        return formatar_moeda_br(valor)
    if unidade == "PERCENTUAL":
        return formatar_percentual_br(valor, conversao_fracao=True)
    try:
        n = float(valor)
    except (TypeError, ValueError):
        return str(valor)
    if n == 0:
        return "-"
    abs_n = abs(n)
    if unidade == "QUANTIDADE":
        inteiro_str = f"{int(round(abs_n)):,}".replace(",", ".")
        return f"-{inteiro_str}" if n < 0 else inteiro_str
    if unidade == "TEMPO_DIAS":
        inteiro_str = f"{int(round(abs_n)):,}".replace(",", ".")
        return f"-{inteiro_str} dias" if n < 0 else f"{inteiro_str} dias"
    if unidade == "TEMPO_HORAS":
        inteiro_str = f"{int(round(abs_n)):,}".replace(",", ".")
        return f"-{inteiro_str} h" if n < 0 else f"{inteiro_str} h"
    if unidade == "MULTIPLICADOR":
        texto = f"{abs_n:.2f}".replace(".", ",")
        return f"-{texto}x" if n < 0 else f"{texto}x"
    if unidade == "RAZAO":
        texto = f"{abs_n:.4f}".replace(".", ",")
        return f"-{texto}" if n < 0 else texto
    # ADIMENSIONAL e fallback
    texto = f"{abs_n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"-{texto}" if n < 0 else texto
