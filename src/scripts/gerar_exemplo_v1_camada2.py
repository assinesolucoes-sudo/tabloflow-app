"""
gerar_exemplo_v1_camada2.py — Gera Excel de exemplo para Camada 2 da Usuária.

Uso:
    python src/scripts/gerar_exemplo_v1_camada2.py

Carrega bases/base_fundacao.xlsx · monta config canônica derivada de
casos_esperados.yaml entrada V1 · executa pipeline V1 completo · exporta
Excel em paleta default em outputs/exemplo_v1_camada2.xlsx · paletas
alternativas em outputs/exemplo_v1_camada2_<paleta>.xlsx.

Sessão A-V1 · Fase 8 · facilita Camada 2 (validação visual da Usuária)
do gate duplo D-174.
"""
from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

# Garante que src/ está em path quando script é executado diretamente
_SRC_DIR = Path(__file__).resolve().parents[1]
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from motor_base import processar_base
from motor_upload import ArquivoEntrada, processar_upload
from visoes.exportacao_v1 import exportar_resultado_v1
from visoes.visao_v1 import (
    AgrupadorMatchV1,
    CampoComparadoV1,
    ModoMatchV1,
    TipoCampoV1,
    UnidadeCanonica,
    executar_v1,
)


_REPO_ROOT = Path(__file__).resolve().parents[2]
BASE_PATH = _REPO_ROOT / "bases" / "base_fundacao.xlsx"
OUT_DIR = _REPO_ROOT / "outputs"


def _config_canonica():
    """Config canônica derivada de casos_esperados.yaml entrada V1."""
    return {
        "agrupadores_match": [
            AgrupadorMatchV1(
                nome_origem="Conta", nome_comparado="Conta",
                rotulo_analitico="Conta", modo_match=ModoMatchV1.EXATO,
            ),
            AgrupadorMatchV1(
                nome_origem="Centro_Custo", nome_comparado="Centro_Custo",
                rotulo_analitico="Centro de Custo", modo_match=ModoMatchV1.EXATO,
            ),
        ],
        "campos_comparados": [
            CampoComparadoV1(
                nome_origem="Valor", nome_comparado="Valor",
                nome_analitico="Valor",
                tipo_logico=TipoCampoV1.VALOR_MONETARIO,
                unidade=UnidadeCanonica.MONETARIO_BRL,
                tolerancia=Decimal("0.01"),
            ),
        ],
        "agrupadores_executivos": ["Centro_Custo"],
        "epsilon_por_unidade": {UnidadeCanonica.MONETARIO_BRL: Decimal("0.01")},
        "thresholds": {},
        "origem_ux": "Razão",
        "comparado_ux": "Balancete",
        "arquivo_origem": "base_fundacao.xlsx",
        "arquivo_comparado": "base_fundacao.xlsx",
        "aba_origem": "dual_origem_crm",
        "aba_comparado": "dual_comparado_erp",
        "n_arquivos": 1,
        "paleta_aplicada": "Azul executivo",
    }


def _executar_pipeline_canonico():
    upload_result = processar_upload(
        [
            ArquivoEntrada(
                caminho_fisico=str(BASE_PATH),
                caminho_logico="origem",
                aba_solicitada="dual_origem_crm",
            ),
            ArquivoEntrada(
                caminho_fisico=str(BASE_PATH),
                caminho_logico="comparado",
                aba_solicitada="dual_comparado_erp",
            ),
        ],
        modo="DUAL",
    )
    motor_result = processar_base(upload_result)
    return executar_v1(motor_result, _config_canonica())


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    print(f"Carregando {BASE_PATH} ...")
    v1_result = _executar_pipeline_canonico()

    contagem = v1_result.contagem_por_classificacao
    print(f"Pipeline V1 concluído.")
    print(f"  Caso lógico: {v1_result.conciliacao_realizada.caso_logico_inferido.value}")
    print(f"  Registros processados: {v1_result.conciliacao_realizada.n_processados}")
    print(f"  Status Ponte: {v1_result.status_ponte_geral.value}")
    print(f"  Contagens: {dict((k.value, v) for k, v in contagem.items())}")

    paletas = ["azul", "verde", "cinza", "vinho"]
    for i, paleta in enumerate(paletas):
        if i == 0:
            caminho = OUT_DIR / "exemplo_v1_camada2.xlsx"
        else:
            caminho = OUT_DIR / f"exemplo_v1_camada2_{paleta}.xlsx"
        res = exportar_resultado_v1(
            v1_result=v1_result,
            caminho_saida=str(caminho),
            paleta_nome=paleta,
            origem_rotulo="Razão",
            comparado_rotulo="Balancete",
            arquivo_nome_origem="base_fundacao.xlsx",
            aba_consumida="dual_origem_crm",
            usar_nome_executivo=False,
        )
        print(
            f"Gerado: {caminho.name}  ·  {res.tamanho_bytes:,} bytes  ·  "
            f"{res.numero_abas} abas  ·  paleta {paleta}".replace(",", ".")
        )


if __name__ == "__main__":
    main()
