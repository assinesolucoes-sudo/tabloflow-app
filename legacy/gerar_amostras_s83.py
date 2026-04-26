"""
Gera as 3 amostras oficiais da Sub-sessão 8.3 (correção dirigida pós-Camada 2 da S82).

Produz arquivos:
  - amostras/V2_S83_MONETARIO_BRL.xlsx · Leitura qualitativa wrap robusto
  - amostras/V2_S83_PERCENTUAL.xlsx    · idem + verificar default unidade
  - amostras/V2_S83_QUANTIDADE.xlsx    · idem · sanity

Reaproveita 100% das bases S81/S82 (geradoras + config + helpers); só muda o
sufixo do arquivo de saída para refletir a nova sub-sessão.
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
    saida = _RAIZ / "amostras" / f"V2_S83_{sufixo}.xlsx"
    saida.parent.mkdir(parents=True, exist_ok=True)
    res = exportar_resultado_v2(v2, str(saida), paleta_nome="azul")
    print(f"  -> {saida.name} | {res.tamanho_bytes:,} bytes | {res.numero_abas} abas")
    return saida


if __name__ == "__main__":
    print("Gerando amostras Sub-sessão 8.3 (S83) · 2 fixes Camada 2 · sufixo S83 ...")
    _gerar("MONETARIO_BRL", "MONETARIO_BRL")
    _gerar("PERCENTUAL", "PERCENTUAL")
    _gerar("QUANTIDADE", "QUANTIDADE")
    print("Concluído.")
