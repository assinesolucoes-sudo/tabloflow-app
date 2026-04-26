"""
Gera as 3 amostras oficiais da Sub-sessão 8.4 (P-36 · gráfico no fim).

Produz arquivos:
  - amostras/V2_S84_MONETARIO_BRL.xlsx · gráfico movido para depois de
    Qualidade estrutural · cabeçalho "Variações em destaque · gráfico"
  - amostras/V2_S84_PERCENTUAL.xlsx    · idem
  - amostras/V2_S84_QUANTIDADE.xlsx    · idem · sanity

Reaproveita 100% das bases S81/S82/S83 (geradoras + config + helpers).
"""
from __future__ import annotations

import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parent.parent
_SRC = _RAIZ / "src"
sys.path.insert(0, str(_SRC))

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
    saida = _RAIZ / "amostras" / f"V2_S84_{sufixo}.xlsx"
    saida.parent.mkdir(parents=True, exist_ok=True)
    res = exportar_resultado_v2(v2, str(saida), paleta_nome="azul")
    print(f"  -> {saida.name} | {res.tamanho_bytes:,} bytes | {res.numero_abas} abas")
    return saida


if __name__ == "__main__":
    print("Gerando amostras Sub-sessão 8.4 (S84) · 1 fix · sufixo S84 ...")
    _gerar("MONETARIO_BRL", "MONETARIO_BRL")
    _gerar("PERCENTUAL", "PERCENTUAL")
    _gerar("QUANTIDADE", "QUANTIDADE")
    print("Concluído.")
