"""
Gera as 3 amostras oficiais da Sessão 8.2 (sub-sessão γ · 3 fixes Camada 2).

Produz arquivos:
  - amostras/V2_S82_MONETARIO_BRL.xlsx · receitas R$ 500-2500 (regressão zero)
  - amostras/V2_S82_PERCENTUAL.xlsx    · margens fração 0.08-0.45 (P-29 + P-30)
  - amostras/V2_S82_QUANTIDADE.xlsx    · unidades inteiras 50-1500 (sanity)

Reaproveita 100% das bases S81 (geradoras + config + helpers); só muda o
sufixo do arquivo de saída para refletir a nova sub-sessão.
"""
from __future__ import annotations

import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parent.parent
_SRC = _RAIZ / "src"
sys.path.insert(0, str(_SRC))

# Reaproveita geradoras + helpers de configuração da S81
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gerar_amostras_s8 import (  # noqa: E402
    _GERADORES,
    _config,
    _motor_result,
)
from visoes.exportacao_v2 import exportar_resultado_v2  # noqa: E402
from visoes.visao_v2 import executar_v2  # noqa: E402


def _gerar(unidade: str, sufixo: str) -> Path:
    df = _GERADORES[unidade]()
    cfg = _config(unidade=unidade, campo=f"Campo · {sufixo}")
    v2 = executar_v2(_motor_result(df), cfg)
    saida = _RAIZ / "amostras" / f"V2_S82_{sufixo}.xlsx"
    saida.parent.mkdir(parents=True, exist_ok=True)
    res = exportar_resultado_v2(v2, str(saida), paleta_nome="azul")
    print(f"  -> {saida.name} | {res.tamanho_bytes:,} bytes | {res.numero_abas} abas")
    return saida


if __name__ == "__main__":
    print("Gerando amostras Sessão 8.2 (S82) · 3 fixes Camada 2 · sufixo S82 ...")
    _gerar("MONETARIO_BRL", "MONETARIO_BRL")
    _gerar("PERCENTUAL", "PERCENTUAL")
    _gerar("QUANTIDADE", "QUANTIDADE")
    print("Concluído.")
