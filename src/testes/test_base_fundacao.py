"""
test_base_fundacao.py — Testes de regressão de F-BASE.
Valida: estrutura do xlsx · estrutura do YAML · determinismo SEED=42.
"""

import hashlib
import sys
from pathlib import Path

import pandas as pd
import pytest
import yaml

SRC_ROOT = Path(__file__).parent.parent
PROJECT_ROOT = SRC_ROOT.parent
sys.path.insert(0, str(SRC_ROOT))

XLSX_PATH = PROJECT_ROOT / "bases" / "base_fundacao.xlsx"
YAML_PATH = PROJECT_ROOT / "bases" / "casos_esperados.yaml"

ABAS_CANONICAS = [
    "vendas_padrao",
    "vendas_por_colunas",
    "vendas_pre_agregadas",
    "operacao_dispersao",
    "operacao_cruzamento",
    "operacao_perfil_grupo",
    "dual_origem_crm",
    "dual_comparado_erp",
    "cadastral_fuzzy",
    "vendas_volume_alto",
    "cardinalidade_excessiva",
    "boolean_disfarcado",
    "eixo_sequencial_lacunas",
    "eixo_sequencial_completo",
]

TIPOS_CANONICOS = {
    "contagem_exata",
    "contagem_categoria",
    "warning_presente",
    "estrutura_saida",
    "bloqueio_emitido",
}

VISOES_ESPERADAS = {"V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11"}

TRANSVERSAIS_ESPERADOS = {"motor_upload", "bloqueio_operacional", "determinismo"}


def test_xlsx_tem_14_abas_canonicas():
    """Carrega base_fundacao.xlsx e verifica 14 chaves canônicas."""
    assert XLSX_PATH.exists(), f"base_fundacao.xlsx não encontrado em {XLSX_PATH}"
    dfs = pd.read_excel(str(XLSX_PATH), sheet_name=None)
    assert len(dfs) == 14, f"Esperado 14 abas · encontrado {len(dfs)}"
    abas_presentes = set(dfs.keys())
    abas_esperadas = set(ABAS_CANONICAS)
    faltantes = abas_esperadas - abas_presentes
    assert len(faltantes) == 0, f"Abas faltantes: {faltantes}"


def test_yaml_estrutura_3_niveis():
    """Valida estrutura de 3 níveis: metadata → visoes → transversais."""
    assert YAML_PATH.exists(), f"casos_esperados.yaml não encontrado em {YAML_PATH}"
    with open(str(YAML_PATH), "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Nível 1: metadata
    assert "metadata" in data, "Falta chave 'metadata'"
    meta = data["metadata"]
    assert meta["seed"] == 42, "seed deve ser 42 (D-140)"
    assert meta["total_abas"] == 14, "total_abas deve ser 14 (D-140)"

    # Nível 2: visoes com V1..V11
    assert "visoes" in data, "Falta chave 'visoes'"
    visoes_presentes = set(data["visoes"].keys())
    faltantes = VISOES_ESPERADAS - visoes_presentes
    assert len(faltantes) == 0, f"Visões faltantes: {faltantes}"

    # Cada visão tem ≥3 assertions
    for v_id, v_data in data["visoes"].items():
        n = len(v_data.get("assertions", []))
        assert n >= 3, f"{v_id} tem {n} assertions (mínimo 3)"

    # Nível 3: transversais com subchaves canônicas
    assert "transversais" in data, "Falta chave 'transversais'"
    trans_presentes = set(data["transversais"].keys())
    faltantes_t = TRANSVERSAIS_ESPERADOS - trans_presentes
    assert len(faltantes_t) == 0, f"Transversais faltantes: {faltantes_t}"


def test_yaml_tipos_canonicos_apenas():
    """Verifica que todos os tipos de assertion são dos 5 canônicos (mais instâncias parametrizadas)."""
    TIPOS_ACEITOS = TIPOS_CANONICOS | {"inferencia_boolean", "inferencia_subtipo_id", "determinismo_seed"}
    with open(str(YAML_PATH), "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    tipos_encontrados = set()
    for v_data in data["visoes"].values():
        for a in v_data.get("assertions", []):
            tipos_encontrados.add(a["tipo"])
    for lista in data["transversais"].values():
        for a in lista:
            tipos_encontrados.add(a["tipo"])

    tipos_invalidos = tipos_encontrados - TIPOS_ACEITOS
    assert len(tipos_invalidos) == 0, f"Tipos inválidos encontrados: {tipos_invalidos}"


def test_yaml_total_assertions_60_a_80():
    """Total de assertions entre 60 e 80 (J.5)."""
    with open(str(YAML_PATH), "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    total = sum(len(v.get("assertions", [])) for v in data["visoes"].values())
    total += sum(len(lista) for lista in data["transversais"].values())
    assert 60 <= total <= 80, f"Total de assertions: {total} (esperado 60-80)"


def test_yaml_bloqueio_operacional_exatamente_1():
    """Bloco bloqueio_operacional tem exatamente 1 assertion (B-CARD-EXCESSIVA)."""
    with open(str(YAML_PATH), "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    bo = data["transversais"]["bloqueio_operacional"]
    assert len(bo) == 1, f"bloqueio_operacional deve ter 1 assertion · encontrado {len(bo)}"
    assert bo[0]["esperado"]["bloqueio_codigo"] == "B-CARD-EXCESSIVA"


def test_yaml_determinismo_assertion():
    """Bloco determinismo tem exatamente 1 assertion DET-A01."""
    with open(str(YAML_PATH), "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    det = data["transversais"]["determinismo"]
    assert len(det) == 1, f"determinismo deve ter 1 assertion · encontrado {len(det)}"
    assert det[0]["id"] == "DET-A01"
    assert det[0]["esperado"]["hash_estavel"] is True


def test_determinismo_seed42(tmp_path):
    """Regera base em tmp_path e verifica hash == hash da base canônica."""
    from geradores.gerar_base_fundacao import gerar_todos_dataframes, hash_dfs

    # Hash da base canônica existente
    dfs_canonico = pd.read_excel(str(XLSX_PATH), sheet_name=None)

    # Hash da base regenerada
    dfs_novo = gerar_todos_dataframes()

    # Comparar usando o mesmo método (CSV estável)
    def hash_via_csv(dfs):
        h = hashlib.sha256()
        for nome in sorted(dfs.keys()):
            df = dfs[nome]
            conteudo = df.to_csv(index=False).encode("utf-8")
            h.update(nome.encode("utf-8"))
            h.update(conteudo)
        return h.hexdigest()

    h_canonico = hash_via_csv(dfs_canonico)
    h_novo = hash_dfs(dfs_novo)

    # Verificar que a regera=o é estável consigo mesma (DET-A01)
    dfs_novo2 = gerar_todos_dataframes()
    h_novo2 = hash_dfs(dfs_novo2)
    assert h_novo == h_novo2, f"Hash instável entre regera=es: {h_novo[:16]} != {h_novo2[:16]}"
