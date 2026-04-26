"""
Gera as 3 amostras oficiais da Sessão 8.1 (correção dirigida pós-Camada 2).

Produz arquivos:
  - amostras/V2_S81_MONETARIO_BRL.xlsx · receitas R$ 500-2500
  - amostras/V2_S81_PERCENTUAL.xlsx    · margens em fração 0.08-0.45
  - amostras/V2_S81_QUANTIDADE.xlsx    · unidades inteiras 50-1500

Sessão 8.1 · C-5: cada amostra usa BASE distinta, realista para sua unidade,
para que os cards "Total"/"Média" e "Variação absoluta" rendam números
plausíveis (não 69.767% como na S8 original que usava base 80-200 para tudo).
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

_SRC = Path(__file__).parent / "src"
sys.path.insert(0, str(_SRC))

from contratos import (
    ColumnMeta,
    MotorResult,
    TipoEstruturalEnum,
    TipoSemanticoEnum,
    TipoTecnicoEnum,
)
from visoes.exportacao_v2 import exportar_resultado_v2
from visoes.visao_v2 import executar_v2


def _col_meta(nome: str, tipo_estrutural: str = "NUMERICO_CONTINUO") -> ColumnMeta:
    return ColumnMeta(
        nome=nome,
        tipo_tecnico=TipoTecnicoEnum("float" if tipo_estrutural == "NUMERICO_CONTINUO" else "string"),
        tipo_semantico=(
            TipoSemanticoEnum("numeric")
            if tipo_estrutural == "NUMERICO_CONTINUO"
            else TipoSemanticoEnum("categorico_baixa_card")
        ),
        tipo_estrutural=TipoEstruturalEnum(tipo_estrutural),
        subtipo_id_detectado=False,
        null_count=0,
        cardinalidade=10,
        eh_candidato_categorico=tipo_estrutural == "CATEGORICO_ELEGIVEL",
        padrao_cronologico_detectado=None,
        ordem_insercao=0,
    )


def _motor_result(df: pd.DataFrame) -> MotorResult:
    col_meta = {}
    for i, col in enumerate(df.columns):
        if pd.api.types.is_numeric_dtype(df[col]):
            meta = _col_meta(col, "NUMERICO_CONTINUO")
        else:
            meta = _col_meta(col, "CATEGORICO_ELEGIVEL")
        meta = meta.model_copy(update={
            "nome": col, "ordem_insercao": i,
            "null_count": int(df[col].isna().sum()),
            "cardinalidade": int(df[col].nunique()),
        })
        col_meta[col] = meta
    return MotorResult(
        df=df,
        column_meta=col_meta,
        modo_upload="SIMPLES",
        total_linhas_originais=len(df),
        total_linhas_processadas=len(df),
    )


def _config(
    unidade: str,
    campo: str,
    semantica: str = "MAIOR_MELHOR",
    agrupadores: Optional[List[str]] = None,
    agrupador_destacado: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "estrutura_entrada": "POR_COLUNAS",
        "origem_rotulo_tecnico": "Origem",
        "comparado_rotulo_tecnico": "Comparado",
        "origem_rotulo_ux": "Janeiro 2025",
        "comparado_rotulo_ux": "Fevereiro 2025",
        "coluna_discriminadora": None,
        "modo_4_ativado": False,
        "estados_nao_escolhidos": [],
        "campo_analisado": campo,
        "tipo_campo": "NUMERICO_ADITIVO",
        "semantica_campo": semantica,
        "unidade": unidade,
        "regra_agregacao": "SOMA",
        "metodo_consolidacao_relativo": None,
        "campo_peso": None,
        "modo_pre_agregado": False,
        "agrupadores": agrupadores or ["Filial", "Produto"],
        "agrupador_destacado": agrupador_destacado or "Filial",
        "resolucao_estrutural": None,
        "thresholds": {
            "limiar_estabilidade_pct": 0.01,
            "limiar_nulo_massivo_pct": 0.20,
            "limite_valores_discriminador_alerta": 50,
            "limite_variacao_extrema_pct": 10.0,
        },
        "modelo_aplicado": None,
    }


_FILIAIS = ["SP", "MG", "RJ", "BA", "PR"]
_PRODUTOS = ["Produto A", "Produto B", "Produto C", "Produto D"]
_BONUS_FILIAL = {"SP": 1.30, "MG": 0.85, "RJ": 1.05, "BA": 0.78, "PR": 0.95}


def _df_monetario() -> pd.DataFrame:
    """Receitas em R$ · valores 500-2500 · variação plausível por filial."""
    import random
    random.seed(42)
    rows: List[Dict[str, Any]] = []
    for filial in _FILIAIS:
        bonus = _BONUS_FILIAL[filial]
        for produto in _PRODUTOS:
            for _ in range(5):
                origem = float(random.uniform(500, 2500))
                comparado = origem * bonus + random.uniform(-150, 150)
                rows.append({
                    "Filial": filial,
                    "Produto": produto,
                    "Origem": round(origem, 2),
                    "Comparado": round(comparado, 2),
                })
    return pd.DataFrame(rows)


def _df_percentual() -> pd.DataFrame:
    """
    Margens em fração decimal · valores 0.08-0.45 · variação ±10 p.p.

    Sessão 8.1 · 1 obs por (Filial, Produto) · evita SOMA agregar margens
    (5 amostras × 0.265 → 1.325 avg que faria Card Média mostrar 132% ao
    invés de 26%). Para PERCENTUAL realista, cada linha é uma taxa medida
    no nível do grupo · 20 linhas no total.
    """
    import random
    random.seed(42)
    rows: List[Dict[str, Any]] = []
    for filial in _FILIAIS:
        bonus = _BONUS_FILIAL[filial]
        for produto in _PRODUTOS:
            origem = round(float(random.uniform(0.08, 0.45)), 4)
            ruido = float(random.uniform(-0.10, 0.10))
            deslocamento_filial = (bonus - 1.0) * 0.05
            comparado = max(0.01, min(0.99, origem + ruido + deslocamento_filial))
            rows.append({
                "Filial": filial,
                "Produto": produto,
                "Origem": origem,
                "Comparado": round(comparado, 4),
            })
    return pd.DataFrame(rows)


def _df_quantidade() -> pd.DataFrame:
    """Unidades vendidas · inteiros 50-1500 · variação plausível."""
    import random
    random.seed(42)
    rows: List[Dict[str, Any]] = []
    for filial in _FILIAIS:
        bonus = _BONUS_FILIAL[filial]
        for produto in _PRODUTOS:
            for _ in range(5):
                origem = int(random.uniform(50, 1500))
                comparado = int(origem * bonus + random.uniform(-100, 100))
                comparado = max(0, comparado)
                rows.append({
                    "Filial": filial,
                    "Produto": produto,
                    "Origem": origem,
                    "Comparado": comparado,
                })
    return pd.DataFrame(rows)


_GERADORES = {
    "MONETARIO_BRL": _df_monetario,
    "PERCENTUAL":    _df_percentual,
    "QUANTIDADE":    _df_quantidade,
}


def _gerar(unidade: str, sufixo: str) -> Path:
    df = _GERADORES[unidade]()
    cfg = _config(unidade=unidade, campo=f"Campo · {sufixo}")
    v2 = executar_v2(_motor_result(df), cfg)
    saida = Path(__file__).parent / "amostras" / f"V2_S81_{sufixo}.xlsx"
    saida.parent.mkdir(parents=True, exist_ok=True)
    res = exportar_resultado_v2(v2, str(saida), paleta_nome="azul")
    print(f"  -> {saida.name} | {res.tamanho_bytes:,} bytes | {res.numero_abas} abas")
    return saida


if __name__ == "__main__":
    print("Gerando amostras Sessão 8.1 (S81) · bases adequadas por unidade ...")
    _gerar("MONETARIO_BRL", "MONETARIO_BRL")
    _gerar("PERCENTUAL", "PERCENTUAL")
    _gerar("QUANTIDADE", "QUANTIDADE")
    print("Concluído.")
