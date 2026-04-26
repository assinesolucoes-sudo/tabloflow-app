"""
_auto_validar.py — Auto-validação estrutural da base_fundacao.xlsx.
Uso interno F-BASE · não exportado. Script de pré-entrega.

Valida subset executável antes dos motores rodarem:
  (1) contagem_exata   — len(df) e cardinalidades de colunas
  (2) contagem_categoria — categorias presentes no df
  (3) determinismo_seed  — hash SHA-256 estável em 2 execuções

Não valida (exige motores/exportação):
  warning_presente · bloqueio_emitido · estrutura_saida · inferencia_*
"""

import sys
import os
from pathlib import Path

# Forçar UTF-8 em stdout para suportar caracteres especiais no Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Adicionar src ao path para importar gerar_base_fundacao
SRC_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SRC_ROOT))

from geradores.gerar_base_fundacao import gerar_todos_dataframes, hash_dfs, SEED

import pandas as pd
import numpy as np

PROJECT_ROOT = SRC_ROOT.parent
XLSX_PATH = PROJECT_ROOT / "bases" / "base_fundacao.xlsx"

# ──────────────────────────────────────────────────────────────────────────────
# Contagens de linhas esperadas por aba (D-140)
# ──────────────────────────────────────────────────────────────────────────────

LINHAS_ESPERADAS = {
    "vendas_padrao": (115, 126),          # ±5% de 120
    "vendas_por_colunas": (25, 25),       # exato
    "vendas_pre_agregadas": (50, 50),     # exato
    "operacao_dispersao": (200, 200),     # exato
    "operacao_cruzamento": (171, 189),    # ±5% de 180
    "operacao_perfil_grupo": (143, 158),  # ±5% de 150
    "dual_origem_crm": (110, 110),        # exato
    "dual_comparado_erp": (105, 105),     # exato
    "cadastral_fuzzy": (80, 80),          # exato
    "vendas_volume_alto": (400, 400),     # exato
    "cardinalidade_excessiva": (200, 200),# exato
    "boolean_disfarcado": (60, 60),       # exato
    "eixo_sequencial_lacunas": (80, 80),  # exato
    "eixo_sequencial_completo": (100, 100),# exato
}

ABAS_CANONICAS = list(LINHAS_ESPERADAS.keys())


def _ok(msg: str) -> None:
    print(f"  [OK] {msg}")


def _fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


class Validador:
    def __init__(self):
        self.n_ok = 0
        self.n_fail = 0

    def ok(self, msg: str) -> None:
        self.n_ok += 1
        _ok(msg)

    def fail(self, msg: str) -> None:
        self.n_fail += 1
        _fail(msg)

    def check(self, condicao: bool, msg_ok: str, msg_fail: str) -> None:
        if condicao:
            self.ok(msg_ok)
        else:
            self.fail(msg_fail)


def validar_arquivo_existe(v: Validador) -> dict | None:
    if not XLSX_PATH.exists():
        v.fail(f"Arquivo não encontrado: {XLSX_PATH}")
        return None
    v.ok(f"Arquivo existe: {XLSX_PATH}")
    return True


def carregar_xlsx() -> dict | None:
    try:
        dfs = pd.read_excel(str(XLSX_PATH), sheet_name=None)
        return dfs
    except Exception as e:
        return None


def validar_estrutura_abas(v: Validador, dfs: dict) -> None:
    """Verifica 14 abas canônicas presentes com nomes exatos."""
    abas_presentes = set(dfs.keys())
    abas_esperadas = set(ABAS_CANONICAS)
    faltantes = abas_esperadas - abas_presentes
    extras = abas_presentes - abas_esperadas

    v.check(len(dfs) == 14,
            "14 abas presentes",
            f"Número de abas: {len(dfs)} (esperado 14)")
    v.check(len(faltantes) == 0,
            "Todos os nomes canônicos de abas presentes",
            f"Abas faltantes: {faltantes}")
    if extras:
        v.fail(f"Abas extras não esperadas: {extras}")


def validar_contagem_linhas(v: Validador, dfs: dict) -> None:
    """contagem_exata: len(df) dentro dos limites declarados por aba."""
    for aba, (min_l, max_l) in LINHAS_ESPERADAS.items():
        if aba not in dfs:
            v.fail(f"Aba {aba} ausente · não é possível verificar linhas")
            continue
        n = len(dfs[aba])
        v.check(min_l <= n <= max_l,
                f"{aba}: {n} linhas (esperado {min_l}-{max_l})",
                f"{aba}: {n} linhas FORA do esperado {min_l}-{max_l}")


def validar_cardinalidades(v: Validador, dfs: dict) -> None:
    """contagem_exata sobre cardinalidade de colunas chave."""

    # V2-A04: Mes tem 2 meses distintos
    if "vendas_padrao" in dfs:
        card = dfs["vendas_padrao"]["Mes"].nunique()
        v.check(card == 2,
                f"vendas_padrao: Mes tem {card} estados distintos (esperado 2)",
                f"vendas_padrao: Mes tem {card} estados (esperado 2)")

    # V3-A01: eixo_sequencial_completo tem 12 meses
    if "eixo_sequencial_completo" in dfs:
        card = dfs["eixo_sequencial_completo"]["Mes"].nunique()
        v.check(card == 12,
                f"eixo_sequencial_completo: {card} meses distintos (esperado 12)",
                f"eixo_sequencial_completo: {card} meses (esperado 12)")

    # V3-A02: eixo_sequencial_lacunas tem 10 meses (faltam 2025-03 e 2025-07)
    if "eixo_sequencial_lacunas" in dfs:
        card = dfs["eixo_sequencial_lacunas"]["Mes"].nunique()
        v.check(card == 10,
                f"eixo_sequencial_lacunas: {card} meses distintos (esperado 10)",
                f"eixo_sequencial_lacunas: {card} meses (esperado 10)")

        # Verifica que 2025-03 e 2025-07 realmente não estão
        meses = set(dfs["eixo_sequencial_lacunas"]["Mes"].unique())
        lacunas_ok = ("2025-03" not in meses and "2025-07" not in meses)
        v.check(lacunas_ok,
                "eixo_sequencial_lacunas: 2025-03 e 2025-07 ausentes (lacunas corretas)",
                f"eixo_sequencial_lacunas: lacunas incorretas — meses presentes: {sorted(meses)}")

    # V6-A01 e V6-A02: Filial=8 e Transportadora=6
    if "operacao_cruzamento" in dfs:
        card_fil = dfs["operacao_cruzamento"]["Filial"].nunique()
        card_tra = dfs["operacao_cruzamento"]["Transportadora"].nunique()
        v.check(card_fil == 8,
                f"operacao_cruzamento: {card_fil} filiais distintas (esperado 8)",
                f"operacao_cruzamento: {card_fil} filiais (esperado 8)")
        v.check(card_tra == 6,
                f"operacao_cruzamento: {card_tra} transportadoras distintas (esperado 6)",
                f"operacao_cruzamento: {card_tra} transportadoras (esperado 6)")

    # V7-A01: 4 regiões
    if "operacao_perfil_grupo" in dfs:
        card_reg = dfs["operacao_perfil_grupo"]["Regiao"].nunique()
        v.check(card_reg == 4,
                f"operacao_perfil_grupo: {card_reg} regiões (esperado 4)",
                f"operacao_perfil_grupo: {card_reg} regiões (esperado 4)")

    # V10-A02: 45 Produtos distintos em vendas_volume_alto
    if "vendas_volume_alto" in dfs:
        card_prod = dfs["vendas_volume_alto"]["Produto"].nunique()
        v.check(card_prod == 45,
                f"vendas_volume_alto: {card_prod} produtos distintos (esperado 45)",
                f"vendas_volume_alto: {card_prod} produtos (esperado 45)")

    # V5-A02: 1 linha com Prazo_Dias=350
    if "operacao_dispersao" in dfs:
        n_extremo = (dfs["operacao_dispersao"]["Prazo_Dias"] == 350).sum()
        v.check(n_extremo == 1,
                f"operacao_dispersao: {n_extremo} linha com Prazo_Dias=350 (esperado 1)",
                f"operacao_dispersao: {n_extremo} linhas com Prazo_Dias=350 (esperado 1)")

    # cardinalidade_excessiva: Filial tem 85 categorias
    if "cardinalidade_excessiva" in dfs:
        card_cat = dfs["cardinalidade_excessiva"]["Filial"].nunique()
        v.check(card_cat == 85,
                f"cardinalidade_excessiva: {card_cat} filiais (esperado 85 - dispara B-CARD-EXCESSIVA)",
                f"cardinalidade_excessiva: {card_cat} filiais (esperado 85)")

    # cadastral_fuzzy: 40 oficiais + 40 ruidosas = 80 linhas com 40 IDs únicos
    if "cadastral_fuzzy" in dfs:
        n_linhas = len(dfs["cadastral_fuzzy"])
        v.check(n_linhas == 80,
                f"cadastral_fuzzy: {n_linhas} linhas (40 oficiais + 40 ruidosas)",
                f"cadastral_fuzzy: {n_linhas} linhas (esperado 80)")

    # boolean_disfarcado: coluna Ativo tem exatamente 4 valores distintos
    if "boolean_disfarcado" in dfs:
        vals = set(dfs["boolean_disfarcado"]["Ativo"].unique())
        esperados = {"Sim", "Não", "Ativo", "Inativo"}
        v.check(vals == esperados,
                f"boolean_disfarcado: Ativo tem valores {sorted(vals)} (correto)",
                f"boolean_disfarcado: Ativo tem {sorted(vals)} (esperado {sorted(esperados)})")

    # dual_origem_crm: coluna Razao_Social NÃO existe (é Cliente)
    if "dual_origem_crm" in dfs:
        v.check("Cliente" in dfs["dual_origem_crm"].columns,
                "dual_origem_crm: campo Cliente presente",
                "dual_origem_crm: campo Cliente AUSENTE")
        v.check("Razao_Social" not in dfs["dual_origem_crm"].columns,
                "dual_origem_crm: Razao_Social ausente (correto — só no Comparado)",
                "dual_origem_crm: Razao_Social presente indevidamente")

    # dual_comparado_erp: coluna Razao_Social existe (sinônimo de Cliente → gera warning)
    if "dual_comparado_erp" in dfs:
        v.check("Razao_Social" in dfs["dual_comparado_erp"].columns,
                "dual_comparado_erp: Razao_Social presente (sinonimo de Cliente - W-V1-NOME-COLUNA-DIVERGENTE)",
                "dual_comparado_erp: Razao_Social AUSENTE (esperado para exercitar warning)")

    # V2-A04: vendas_padrao NULOS em Vendas = 3-4
    if "vendas_padrao" in dfs:
        n_null = dfs["vendas_padrao"]["Vendas"].isna().sum()
        v.check(3 <= n_null <= 5,
                f"vendas_padrao: {n_null} NULOS em Vendas (esperado 3-5)",
                f"vendas_padrao: {n_null} NULOS em Vendas (esperado 3-5)")


def validar_categorias(v: Validador, dfs: dict) -> None:
    """contagem_categoria: verificações de distribuição categórica."""

    # V2-A01: elementos ausentes em um lado (Produtos que aparecem só em jan ou só em fev)
    if "vendas_padrao" in dfs:
        df = dfs["vendas_padrao"]
        meses_por_produto = df.groupby("Produto")["Mes"].nunique()
        ausentes = (meses_por_produto == 1).sum()
        v.check(1 <= ausentes <= 6,
                f"vendas_padrao: {ausentes} produtos ausentes em um dos lados (esperado 2-4 ±margem)",
                f"vendas_padrao: {ausentes} produtos ausentes em um lado (esperado 2-4)")

    # cardinalidade_excessiva: 85 categorias únicas → verifica que está acima do threshold MBO
    if "cardinalidade_excessiva" in dfs:
        card = dfs["cardinalidade_excessiva"]["Filial"].nunique()
        v.check(card >= 80,
                f"cardinalidade_excessiva: {card} categorias únicas (≥80 → dispara MBO)",
                f"cardinalidade_excessiva: {card} categorias (esperado ≥80 para MBO)")

    # V9-A01: Transportadora tem 4-6 valores em operacao_perfil_grupo
    if "operacao_perfil_grupo" in dfs:
        card_tra = dfs["operacao_perfil_grupo"]["Transportadora"].nunique()
        v.check(4 <= card_tra <= 6,
                f"operacao_perfil_grupo: {card_tra} transportadoras (esperado 4-6)",
                f"operacao_perfil_grupo: {card_tra} transportadoras (esperado 4-6)")

    # V5-A01: Prazo_Dias com outliers > 40 (excluindo extremo 350) — ~10-20
    if "operacao_dispersao" in dfs:
        df = dfs["operacao_dispersao"]
        outliers_dir = ((df["Prazo_Dias"] > 40) & (df["Prazo_Dias"] < 350)).sum()
        v.check(8 <= outliers_dir <= 25,
                f"operacao_dispersao: {outliers_dir} outliers à direita 40<x<350 (esperado ~15)",
                f"operacao_dispersao: {outliers_dir} outliers à direita (esperado ~15)")


def validar_determinismo(v: Validador) -> None:
    """DET-A01: Execução duas vezes com SEED=42 produz hash idêntico."""
    dfs1 = gerar_todos_dataframes()
    h1 = hash_dfs(dfs1)
    dfs2 = gerar_todos_dataframes()
    h2 = hash_dfs(dfs2)
    v.check(h1 == h2,
            f"DET-A01: Hash estável entre 2 execuções ({h1[:16]}...)",
            f"DET-A01: Hash INSTÁVEL · run1={h1[:16]}... · run2={h2[:16]}...")


def main() -> int:
    print("\n=== _auto_validar.py · F-BASE · Auto-validação estrutural ===\n")
    v = Validador()

    # 1. Arquivo existe
    if not validar_arquivo_existe(v):
        print(f"\n[FAIL {v.n_fail} falhas · {v.n_ok} OK]\n")
        return 1

    # 2. Carregar xlsx
    dfs = carregar_xlsx()
    if dfs is None:
        v.fail("Falha ao carregar base_fundacao.xlsx com pandas")
        print(f"\n[FAIL {v.n_fail} falhas · {v.n_ok} OK]\n")
        return 1
    v.ok(f"base_fundacao.xlsx carregado · {len(dfs)} abas")

    # 3. Estrutura de abas
    print("\n--- Estrutura de abas ---")
    validar_estrutura_abas(v, dfs)

    # 4. Contagem de linhas por aba
    print("\n--- Contagem de linhas por aba ---")
    validar_contagem_linhas(v, dfs)

    # 5. Cardinalidades e assertions estruturais
    print("\n--- Cardinalidades e assertions estruturais ---")
    validar_cardinalidades(v, dfs)

    # 6. Contagens categóricas
    print("\n--- Contagens categóricas ---")
    validar_categorias(v, dfs)

    # 7. Determinismo SEED=42
    print("\n--- Determinismo SEED=42 ---")
    validar_determinismo(v)

    print(f"\n{'='*50}")
    print(f"[OK {v.n_ok} assertions passaram] · [FAIL {v.n_fail} falhas]")
    print(f"{'='*50}\n")
    return 0 if v.n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
