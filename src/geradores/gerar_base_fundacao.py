"""
gerar_base_fundacao.py — Gerador determinístico da base sintética de fundação.
14 abas · SEED=42 · D-140 · spec_fundacao.md §H e §I.
"""

SEED = 42
import numpy as np
import random
np.random.seed(SEED)
random.seed(SEED)

import hashlib
import os
import sys
from pathlib import Path
from typing import Optional

import pandas as pd

# ──────────────────────────────────────────────────────────────────────────────
# Vocabulário pt-BR realista (determinístico — listas ordenadas)
# ──────────────────────────────────────────────────────────────────────────────

LOJAS = ["Loja Centro", "Loja Norte", "Loja Sul", "Loja Leste", "Loja Oeste",
         "Loja Alphaville", "Loja Morumbi", "Loja Jardins"]
PRODUTOS_12 = [
    "Camiseta Básica", "Calça Jeans", "Tênis Casual", "Jaqueta Couro",
    "Vestido Floral", "Bermuda Surf", "Polo Lisa", "Sapato Social",
    "Sandália Tiras", "Meia Kit 3", "Cinto Preto", "Boné Aba Reta",
]
CATEGORIAS_3 = ["Vestuário", "Calçados", "Acessórios"]
REGIOES = ["Norte", "Sul", "Leste", "Oeste"]
FILIAIS = [f"Filial {r}{n:02d}" for r in REGIOES for n in range(1, 4)]
TRANSPORTADORAS = ["LogBrasil", "RapidEx", "TransLog", "CargoNorte",
                   "SuperFrete", "EntregaFácil"]
STATUS_ENTREGA = ["Entregue", "Em Trânsito", "Atrasado", "Cancelado", "Devolvido"]
CONTAS = [f"CC-{n:04d}" for n in range(1001, 1051)]
CENTROS_CUSTO = ["ADM", "TI", "RH", "COMERCIAL", "LOGISTICA",
                 "FINANCEIRO", "MARKETING", "OPERACOES"]
CLIENTES = [
    "Martins Distribuidora", "Redes Sul Ltda", "Grupo Nordeste SA",
    "Central Atacado", "Alimentos Norte", "Comércio Pinheiros",
    "Distribuidora ABC", "Varejão Modelo", "Loja das Nações",
    "Top Mercados", "BomPreço Rede", "Hiper Center",
]
FORNECEDORES_OFICIAIS = [
    ("FOR-001", "Têxtil Vale Verde Ltda", "12.345.678/0001-90", "São Paulo", "SP", "Vestuário"),
    ("FOR-002", "Calçados Nordeste SA", "23.456.789/0001-01", "Fortaleza", "CE", "Calçados"),
    ("FOR-003", "Acessórios Premium Ltda", "34.567.890/0001-12", "Rio de Janeiro", "RJ", "Acessórios"),
    ("FOR-004", "Transportes Águia Branca", "45.678.901/0001-23", "Belo Horizonte", "MG", "Logística"),
    ("FOR-005", "Tecidos São João", "56.789.012/0001-34", "Campinas", "SP", "Vestuário"),
    ("FOR-006", "Malhas do Norte Ltda", "67.890.123/0001-45", "Manaus", "AM", "Vestuário"),
    ("FOR-007", "Distribuição Paulista SA", "78.901.234/0001-56", "São Paulo", "SP", "Distribuição"),
    ("FOR-008", "Indústria Sul Têxtil", "89.012.345/0001-67", "Porto Alegre", "RS", "Vestuário"),
    ("FOR-009", "Fornecedor Centro Oeste", "90.123.456/0001-78", "Goiânia", "GO", "Geral"),
    ("FOR-010", "Moda Brasil Ltda", "01.234.567/0001-89", "São Paulo", "SP", "Vestuário"),
    ("FOR-011", "Artigos Esportivos NE", "11.222.333/0001-90", "Recife", "PE", "Esportes"),
    ("FOR-012", "Calçados Premium SP", "22.333.444/0001-01", "São Paulo", "SP", "Calçados"),
    ("FOR-013", "Tecidos Minas SA", "33.444.555/0001-12", "Uberlândia", "MG", "Têxtil"),
    ("FOR-014", "Distribuidora Norte SA", "44.555.666/0001-23", "Belém", "PA", "Distribuição"),
    ("FOR-015", "Grupo Fashion Brasil", "55.666.777/0001-34", "São Paulo", "SP", "Vestuário"),
    ("FOR-016", "Calçados Bahia Ltda", "66.777.888/0001-45", "Salvador", "BA", "Calçados"),
    ("FOR-017", "Têxtil Paraná Indústria", "77.888.999/0001-56", "Curitiba", "PR", "Têxtil"),
    ("FOR-018", "Acessórios Rio Ltda", "88.999.000/0001-67", "Rio de Janeiro", "RJ", "Acessórios"),
    ("FOR-019", "Distribuidora Amazônia", "99.000.111/0001-78", "Manaus", "AM", "Distribuição"),
    ("FOR-020", "Malhas Centro Brasil", "10.111.222/0001-89", "Brasília", "DF", "Vestuário"),
    ("FOR-021", "Indústria Calçadista RS", "21.222.333/0001-90", "Novo Hamburgo", "RS", "Calçados"),
    ("FOR-022", "Fornecedor Premium SP", "32.333.444/0001-01", "São Paulo", "SP", "Geral"),
    ("FOR-023", "Tecidos Vale do Rio", "43.444.555/0001-12", "Americana", "SP", "Têxtil"),
    ("FOR-024", "Artigos Casa e Moda", "54.555.666/0001-23", "São Paulo", "SP", "Vestuário"),
    ("FOR-025", "Grupo Sul Distribuidora", "65.666.777/0001-34", "Porto Alegre", "RS", "Distribuição"),
    ("FOR-026", "Fábrica de Meias Brasil", "76.777.888/0001-45", "São Paulo", "SP", "Acessórios"),
    ("FOR-027", "Couros e Calçados NE", "87.888.999/0001-56", "Campina Grande", "PB", "Calçados"),
    ("FOR-028", "Têxtil Goiana Ltda", "98.999.000/0001-67", "Goiânia", "GO", "Têxtil"),
    ("FOR-029", "Distribuidora Centro SA", "09.000.111/0001-78", "Campo Grande", "MS", "Distribuição"),
    ("FOR-030", "Moda Carioca Ltda", "19.111.222/0001-89", "Rio de Janeiro", "RJ", "Vestuário"),
    ("FOR-031", "Indústria Nordestina SA", "20.222.333/0001-90", "João Pessoa", "PB", "Geral"),
    ("FOR-032", "Calçados Mineiros Ltda", "31.333.444/0001-01", "Belo Horizonte", "MG", "Calçados"),
    ("FOR-033", "Artigos Esportivos Sul", "42.444.555/0001-12", "Florianópolis", "SC", "Esportes"),
    ("FOR-034", "Têxtil Maranhense SA", "53.555.666/0001-23", "São Luís", "MA", "Têxtil"),
    ("FOR-035", "Distribuidora Capixaba", "64.666.777/0001-34", "Vitória", "ES", "Distribuição"),
    ("FOR-036", "Moda Nordeste Fashion", "75.777.888/0001-45", "Fortaleza", "CE", "Vestuário"),
    ("FOR-037", "Acessórios Brasília Ltda", "86.888.999/0001-56", "Brasília", "DF", "Acessórios"),
    ("FOR-038", "Tecidos Amazonas SA", "97.999.000/0001-67", "Manaus", "AM", "Têxtil"),
    ("FOR-039", "Grupo Varejo Brasil", "08.000.111/0001-78", "São Paulo", "SP", "Geral"),
    ("FOR-040", "Distribuidora Piauiense", "18.111.222/0001-89", "Teresina", "PI", "Distribuição"),
]

# Ruído para cadastral_fuzzy (40 "ruidosas" correspondentes às 40 oficiais)
RUIDOS_FORNECEDOR = [
    # abreviação
    ("FOR-001", "Têxtil Vale Verde", "12345678000190", "São Paulo", "SP", "Vestuário"),
    # erro de digitação
    ("FOR-002", "Calçados Nordeste SA", "23.456.789/0001-01", "Fortleza", "CE", "Calçados"),
    # ordem invertida
    ("FOR-003", "Premium Acessórios Ltda", "34.567.890/0001-12", "Rio de Janeiro", "RJ", "Acessórios"),
    # acento diferente
    ("FOR-004", "Transportes Aguia Branca", "45.678.901/0001-23", "Belo Horizonte", "MG", "Logística"),
    # CNPJ sem formatação
    ("FOR-005", "Tecidos São João", "56789012000134", "Campinas", "SP", "Vestuário"),
    # abreviação Ltda
    ("FOR-006", "Malhas do Norte Ltda.", "67.890.123/0001-45", "Manaus", "AM", "Vestuário"),
    # erro de digitação
    ("FOR-007", "Distribuição Paulista SA", "78901234000156", "Sao Paulo", "SP", "Distribuição"),
    # abreviação
    ("FOR-008", "Ind. Sul Têxtil", "89.012.345/0001-67", "Porto Alegre", "RS", "Vestuário"),
    # sem acento
    ("FOR-009", "Fornecedor Centro Oeste", "90123456000178", "Goiania", "GO", "Geral"),
    # typo
    ("FOR-010", "Moda Brasil Ltda", "01234567000189", "Sao Paulo", "SP", "Vestuário"),
    # ordem invertida
    ("FOR-011", "NE Artigos Esportivos", "11.222.333/0001-90", "Recife", "PE", "Esportes"),
    # abreviação
    ("FOR-012", "Calçados Prem. SP", "22333444000101", "São Paulo", "SP", "Calçados"),
    # typo
    ("FOR-013", "Tecidos Minas SA", "33.444.555/0001-12", "Uberlandia", "MG", "Têxtil"),
    # sem espaço
    ("FOR-014", "DistribuidoraNorteSA", "44555666000123", "Belém", "PA", "Distribuição"),
    # abreviação
    ("FOR-015", "Grp. Fashion Brasil", "55.666.777/0001-34", "São Paulo", "SP", "Vestuário"),
    # acento diferente
    ("FOR-016", "Calcados Bahia Ltda", "66777888000145", "Salvador", "BA", "Calçados"),
    # ordem parcial
    ("FOR-017", "Têxtil Paraná Ind.", "77.888.999/0001-56", "Curitiba", "PR", "Têxtil"),
    # typo
    ("FOR-018", "Acessórios Rio Ltda", "88999000000167", "Rio de Janero", "RJ", "Acessórios"),
    # sem acento
    ("FOR-019", "Distribuidora Amazonia", "99.000.111/0001-78", "Manaus", "AM", "Distribuição"),
    # abreviação
    ("FOR-020", "Malhas C. Brasil", "10111222000189", "Brasília", "DF", "Vestuário"),
    # typo
    ("FOR-021", "Ind. Calçadista RS", "21.222.333/0001-90", "Novo Hamburgo", "RS", "Calçados"),
    # sem Ltda
    ("FOR-022", "Fornecedor Premium SP", "32333444000101", "São Paulo", "SP", "Geral"),
    # ordem
    ("FOR-023", "Vale do Rio Tecidos", "43.444.555/0001-12", "Americana", "SP", "Têxtil"),
    # abreviação
    ("FOR-024", "Art. Casa e Moda", "54555666000123", "São Paulo", "SP", "Vestuário"),
    # typo
    ("FOR-025", "Grupo Sul Dist.", "65.666.777/0001-34", "Porto Alegre", "RS", "Distribuição"),
    # sem acento
    ("FOR-026", "Fabrica de Meias Brasil", "76777888000145", "São Paulo", "SP", "Acessórios"),
    # ordem
    ("FOR-027", "Calçados NE Couros", "87.888.999/0001-56", "Campina Grande", "PB", "Calçados"),
    # sem acento
    ("FOR-028", "Textil Goiana Ltda", "98999000000167", "Goiânia", "GO", "Têxtil"),
    # abreviação
    ("FOR-029", "Dist. Centro SA", "09000111000178", "Campo Grande", "MS", "Distribuição"),
    # typo
    ("FOR-030", "Moda Carioca Ltda", "19.111.222/0001-89", "Rio de Janiero", "RJ", "Vestuário"),
    # sem acento
    ("FOR-031", "Industria Nordestina SA", "20222333000190", "João Pessoa", "PB", "Geral"),
    # abreviação
    ("FOR-032", "Calc. Mineiros Ltda", "31.333.444/0001-01", "BH", "MG", "Calçados"),
    # typo
    ("FOR-033", "Art. Esportivos Sul", "42444555000112", "Florianópolis", "SC", "Esportes"),
    # sem acento
    ("FOR-034", "Textil Maranhense SA", "53.555.666/0001-23", "São Luís", "MA", "Têxtil"),
    # ordem
    ("FOR-035", "Capixaba Distribuidora", "64666777000134", "Vitória", "ES", "Distribuição"),
    # typo
    ("FOR-036", "Moda Nordeste Fahsion", "75.777.888/0001-45", "Fortaleza", "CE", "Vestuário"),
    # abreviação
    ("FOR-037", "Acess. Brasília Ltda", "86888999000156", "Brasília", "DF", "Acessórios"),
    # sem acento
    ("FOR-038", "Tecidos Amazonas SA", "97.999.000/0001-67", "Manaus", "AM", "Têxtil"),
    # typo
    ("FOR-039", "Grp. Varejo Brasil", "08000111000178", "São Paulo", "SP", "Geral"),
    # sem acento
    ("FOR-040", "Distribuidora Piauiense", "18111222000189", "Teresina", "PI", "Distribuição"),
]

PRODUTOS_45 = [
    "Camiseta Básica", "Calça Jeans", "Tênis Casual", "Jaqueta Couro",
    "Vestido Floral", "Bermuda Surf", "Polo Lisa", "Sapato Social",
    "Sandália Tiras", "Meia Kit 3", "Cinto Preto", "Boné Aba Reta",
    "Blusa Manga Longa", "Short Tactel", "Scarpin Fino",
    "Bota Country", "Chinelo Dedo", "Mochila Urbana", "Óculos Escuros",
    "Relógio Analógico", "Bolsa Couro", "Carteira Slim",
    "Casaco Moletom", "Camiseta Regata", "Bermuda Jeans",
    "Legging Fitness", "Top Esportivo", "Tênis Running",
    "Chuteira Campo", "Touca de Frio", "Cachecol Lã",
    "Luva de Couro", "Echarpe Seda", "Pulseira Aço",
    "Anel Prata", "Brinco Argola", "Colar Pedras",
    "Cartão de Visitas", "Kit Meia Invisível", "Meião Esportivo",
    "Cueca Kit 3", "Cueca Boxer", "Sutiã Básico",
    "Calcinha Kit 3", "Pijama Inverno",
]

MESES_PT = [
    "jan/2025", "fev/2025", "mar/2025", "abr/2025",
    "mai/2025", "jun/2025", "jul/2025", "ago/2025",
    "set/2025", "out/2025", "nov/2025", "dez/2025",
]
MESES_ISO = [
    "2025-01", "2025-02", "2025-03", "2025-04",
    "2025-05", "2025-06", "2025-07", "2025-08",
    "2025-09", "2025-10", "2025-11", "2025-12",
]


def _rng() -> np.random.Generator:
    """RNG local com SEED fixo — garante determinismo por aba."""
    return np.random.default_rng(SEED)


def _lognormal(rng: np.random.Generator, n: int, mu: float = 6.0, sigma: float = 1.0) -> np.ndarray:
    return rng.lognormal(mean=mu, sigma=sigma, size=n)


def _inject_nulls(arr: list, pct: float, rng: np.random.Generator) -> list:
    """Injeta nulos em `pct` das posições (em cópia)."""
    n = len(arr)
    n_null = max(1, int(n * pct))
    indices = rng.choice(n, size=n_null, replace=False)
    result = list(arr)
    for i in indices:
        result[i] = None
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Aba 1 · vendas_padrao · 120 linhas
# ──────────────────────────────────────────────────────────────────────────────

def gerar_aba_vendas_padrao(rng: np.random.Generator) -> pd.DataFrame:
    """POR_LINHAS · 2 meses · 12 produtos × 5 lojas × 2 meses = 120 registros.
    Ausentes: 3 produtos de Jan não têm par em Fev (2-4 ausentes).
    NULO_MEDIDA: 3-4 em Vendas."""
    registros = []
    meses = ["2025-01", "2025-02"]
    produtos = PRODUTOS_12
    lojas = LOJAS[:5]
    cat_map = {p: CATEGORIAS_3[i % 3] for i, p in enumerate(produtos)}

    vendas_base = _lognormal(rng, len(produtos), mu=6.0, sigma=1.0)

    for mes in meses:
        for i, prod in enumerate(produtos):
            for loja in lojas:
                vendas_val = float(round(vendas_base[i] * rng.uniform(0.8, 1.2), 2))
                margem_val = float(round(vendas_val * rng.uniform(0.1, 0.35), 2))
                qtd_val = int(rng.integers(5, 80))
                registros.append({
                    "Mes": mes,
                    "Loja": loja,
                    "Produto": prod,
                    "Categoria": cat_map[prod],
                    "Vendas": vendas_val,
                    "Margem": margem_val,
                    "Quantidade": qtd_val,
                })

    df = pd.DataFrame(registros)
    # Remover todos os registros de Fev para 3 produtos específicos
    # Isso cria produtos "ausentes em um lado" detectáveis no nível de Produto
    prods_ausentes_fev = PRODUTOS_12[-3:]  # últimos 3 produtos sem registro em Fev
    mask_remover = (df["Mes"] == "2025-02") & (df["Produto"].isin(prods_ausentes_fev))
    df = df[~mask_remover].reset_index(drop=True)

    # Injetar 3-4 NULO_MEDIDA em Vendas
    null_indices = rng.choice(len(df), size=4, replace=False)
    for idx in null_indices:
        df.at[idx, "Vendas"] = None

    # Garantir exatamente 120 linhas (preencher se necessário após remoções)
    while len(df) < 120:
        df = pd.concat([df, df.sample(1, random_state=SEED)], ignore_index=True)
    df = df.iloc[:120].reset_index(drop=True)

    return df


# ──────────────────────────────────────────────────────────────────────────────
# Aba 2 · vendas_por_colunas · 25 linhas × 14 colunas
# ──────────────────────────────────────────────────────────────────────────────

def gerar_aba_vendas_por_colunas(rng: np.random.Generator) -> pd.DataFrame:
    """POR_COLUNAS · meses como colunas · T-PIVOT · 25 produtos × 14 colunas."""
    produtos = PRODUTOS_12[:25] if len(PRODUTOS_12) >= 25 else (PRODUTOS_12 * 3)[:25]
    cat_map = {p: CATEGORIAS_3[i % 3] for i, p in enumerate(produtos)}
    # 12 meses + Produto + Categoria = 14 colunas
    dados = {"Produto": produtos, "Categoria": [cat_map[p] for p in produtos]}
    vendas_base = _lognormal(rng, len(produtos) * 12, mu=6.0, sigma=0.8).reshape(len(produtos), 12)
    for j, mes in enumerate(MESES_PT):
        col = [float(round(vendas_base[i, j], 2)) for i in range(len(produtos))]
        dados[mes] = col
    df = pd.DataFrame(dados)
    return df


# ──────────────────────────────────────────────────────────────────────────────
# Aba 3 · vendas_pre_agregadas · 50 linhas
# ──────────────────────────────────────────────────────────────────────────────

def gerar_aba_vendas_pre_agregadas(rng: np.random.Generator) -> pd.DataFrame:
    """Dados já agregados por Produto · cenário-limite CPCO."""
    produtos = PRODUTOS_12[:25] if len(PRODUTOS_12) >= 25 else (PRODUTOS_12 * 5)[:50]
    produtos = (PRODUTOS_12 * 5)[:50]
    cat_map = {p: CATEGORIAS_3[i % 3] for i, p in enumerate(PRODUTOS_12)}
    vendas = _lognormal(rng, 50, mu=7.0, sigma=1.2)
    margem = vendas * rng.uniform(0.1, 0.3, 50)
    qtd = rng.integers(50, 500, 50)
    records = []
    for i in range(50):
        p = produtos[i]
        records.append({
            "Produto": p,
            "Categoria": cat_map[p],
            "Vendas_Total": float(round(vendas[i], 2)),
            "Margem_Total": float(round(margem[i], 2)),
            "Quantidade_Total": int(qtd[i]),
        })
    return pd.DataFrame(records)


# ──────────────────────────────────────────────────────────────────────────────
# Aba 4 · operacao_dispersao · 200 linhas
# ──────────────────────────────────────────────────────────────────────────────

def gerar_aba_operacao_dispersao(rng: np.random.Generator) -> pd.DataFrame:
    """Univariado numérico · Prazo_Dias · outliers."""
    # Núcleo ~180 linhas normal μ=18 σ=4
    nucleo = rng.normal(18, 4, 180).clip(4, 40).round(0).astype(int)
    # Outliers à direita ~15 linhas: 45-120
    out_dir = rng.integers(45, 121, 15)
    # Outliers à esquerda ~5 linhas: 1-3
    out_esq = rng.integers(1, 4, 4)
    # Valor extremo isolado
    extremo = np.array([350])
    prazo = np.concatenate([nucleo, out_dir, out_esq, extremo])
    n = len(prazo)

    filiais = rng.choice(FILIAIS, size=n)
    regioes = [f.split()[1][:4] for f in filiais]
    peso = _lognormal(rng, n, mu=2.5, sigma=0.5)
    frete = peso * rng.uniform(1.5, 4.0, n)
    status = rng.choice(STATUS_ENTREGA, size=n)

    df = pd.DataFrame({
        "Filial": filiais,
        "Regiao": regioes,
        "Status_Entrega": status,
        "Prazo_Dias": prazo.tolist(),
        "Peso_Kg": [float(round(v, 2)) for v in peso],
        "Valor_Frete": [float(round(v, 2)) for v in frete],
    })
    return df


# ──────────────────────────────────────────────────────────────────────────────
# Aba 5 · operacao_cruzamento · 180 linhas
# ──────────────────────────────────────────────────────────────────────────────

def gerar_aba_operacao_cruzamento(rng: np.random.Generator) -> pd.DataFrame:
    """Bivariado · Filial × Transportadora · células ausentes (~14)."""
    filiais_8 = FILIAIS[:8]
    transp_6 = TRANSPORTADORAS[:6]
    registros = []
    for fil in filiais_8:
        for tra in transp_6:
            # ~14 células ausentes = não gerar alguns pares
            if rng.random() < 0.23:
                continue
            n_registros = int(rng.integers(3, 9))
            for _ in range(n_registros):
                frete = float(round(float(_lognormal(rng, 1, mu=5.0, sigma=0.7)[0]), 2))
                prazo = int(rng.integers(1, 21))
                peso = float(round(float(_lognormal(rng, 1, mu=2.0, sigma=0.5)[0]), 2))
                registros.append({
                    "Filial": fil,
                    "Transportadora": tra,
                    "Regiao": fil.split()[1][:4],
                    "Prazo_Dias": prazo,
                    "Peso_Kg": peso,
                    "Valor_Frete": frete,
                    "Status_Entrega": rng.choice(STATUS_ENTREGA),
                })
    df = pd.DataFrame(registros)
    # Garantir ~180 linhas
    while len(df) < 175:
        extra = pd.DataFrame([{
            "Filial": rng.choice(filiais_8),
            "Transportadora": rng.choice(transp_6),
            "Regiao": rng.choice(REGIOES),
            "Prazo_Dias": int(rng.integers(1, 21)),
            "Peso_Kg": float(round(float(_lognormal(rng, 1, mu=2.0, sigma=0.5)[0]), 2)),
            "Valor_Frete": float(round(float(_lognormal(rng, 1, mu=5.0, sigma=0.7)[0]), 2)),
            "Status_Entrega": rng.choice(STATUS_ENTREGA),
        }])
        df = pd.concat([df, extra], ignore_index=True)
    df = df.iloc[:180].reset_index(drop=True)
    return df


# ──────────────────────────────────────────────────────────────────────────────
# Aba 6 · operacao_perfil_grupo · 150 linhas
# ──────────────────────────────────────────────────────────────────────────────

def gerar_aba_operacao_perfil_grupo(rng: np.random.Generator) -> pd.DataFrame:
    """V7 · V9 · 4 regiões · grupos de 3-5 filiais · métricas Prazo_Dias e Peso_Kg."""
    records = []
    # 4 regiões com 3-4 filiais cada = ~14 filiais × ~10 registros = 140 → completar para 150
    filiais_por_regiao = {
        "Norte": FILIAIS[:3],
        "Sul": FILIAIS[3:7],   # 4 filiais
        "Leste": FILIAIS[7:10],
        "Oeste": FILIAIS[10:12],  # 2 filiais → W-V7-GRUPO-TAMANHO-INSUFICIENTE
    }
    transportadoras_por_filial = {}
    for reg, fils in filiais_por_regiao.items():
        for f in fils:
            transportadoras_por_filial[f] = rng.choice(TRANSPORTADORAS)

    for reg, fils in filiais_por_regiao.items():
        media_reg = rng.uniform(15, 25)
        for fil in fils:
            n = int(rng.integers(8, 14))
            for _ in range(n):
                prazo = float(round(rng.normal(media_reg, 3.0), 1))
                prazo = max(1.0, prazo)
                peso = float(round(float(_lognormal(rng, 1, mu=2.0, sigma=0.4)[0]), 2))
                peso = None if rng.random() < 0.04 else peso  # NULO em métrica secundária
                records.append({
                    "Filial": fil,
                    "Regiao": reg,
                    "Transportadora": transportadoras_por_filial[fil],
                    "Prazo_Dias": prazo,
                    "Peso_Kg": peso,
                    "Valor_Frete": float(round(rng.uniform(50, 500), 2)),
                })
    df = pd.DataFrame(records)
    while len(df) < 148:
        df = pd.concat([df, df.sample(1, random_state=SEED)], ignore_index=True)
    df = df.iloc[:150].reset_index(drop=True)
    return df


# ──────────────────────────────────────────────────────────────────────────────
# Aba 7 · dual_origem_crm · 110 linhas
# ──────────────────────────────────────────────────────────────────────────────

def gerar_aba_dual_origem_crm(rng: np.random.Generator) -> pd.DataFrame:
    """T-DUAL lado Origem · datas em formato misto pt-BR/pt-EN."""
    n_match = 82  # ~70% match exato de 110 + comparado 105
    n_aprox = 4   # match tolerado ≤ R$ 0,01
    n_diverg = 9  # divergência significativa
    n_so_orig = 7  # só na origem
    n_ambig = 2   # ambiguidade
    n_total = n_match + n_aprox + n_diverg + n_so_orig + n_ambig  # = 104 → complementar

    contas = rng.choice(CONTAS[:30], size=n_total)
    centros = rng.choice(CENTROS_CUSTO, size=n_total)
    clientes = rng.choice(CLIENTES, size=n_total)
    valores = _lognormal(rng, n_total, mu=7.5, sigma=1.2)

    # Formatos de data mistos
    formatos_data = ["31/01/2025", "2025-01-31", "jan/2025", "15/02/2025",
                     "2025-02-15", "28/02/2025", "2025-03-10", "mar/2025"]
    datas = [formatos_data[i % len(formatos_data)] for i in range(n_total)]

    records = []
    for i in range(n_total):
        v = float(round(valores[i], 2))
        records.append({
            "Conta": str(contas[i]),
            "Centro_Custo": str(centros[i]),
            "Cliente": str(clientes[i]),
            "Valor": v,
            "Data": datas[i],
        })

    df = pd.DataFrame(records)
    # Injetar 2-3 NULO_MEDIDA em Valor
    null_idx = rng.choice(len(df), size=3, replace=False)
    for idx in null_idx:
        df.at[idx, "Valor"] = None

    # Garantir exatamente 110 linhas
    while len(df) < 110:
        df = pd.concat([df, df.sample(1, random_state=SEED)], ignore_index=True)
    df = df.iloc[:110].reset_index(drop=True)
    return df


# ──────────────────────────────────────────────────────────────────────────────
# Aba 8 · dual_comparado_erp · 105 linhas
# ──────────────────────────────────────────────────────────────────────────────

def gerar_aba_dual_comparado_erp(rng: np.random.Generator) -> pd.DataFrame:
    """T-DUAL lado Comparado · usa Razao_Social em vez de Cliente (sinônimo)."""
    n_total = 103
    contas = rng.choice(CONTAS[:30], size=n_total)
    centros = rng.choice(CENTROS_CUSTO, size=n_total)
    # Usar Razao_Social como sinônimo de Cliente → gera W-V1-NOME-COLUNA-DIVERGENTE
    razao_social = rng.choice(CLIENTES, size=n_total)
    valores = _lognormal(rng, n_total, mu=7.5, sigma=1.2)

    formatos_data = ["2025-01-31", "31/01/2025", "fev/2025", "2025-02-15",
                     "15/03/2025", "mar/2025", "2025-04-01", "abr/2025"]
    datas = [formatos_data[i % len(formatos_data)] for i in range(n_total)]

    records = []
    for i in range(n_total):
        v = float(round(valores[i], 2))
        records.append({
            "Conta": str(contas[i]),
            "Centro_Custo": str(centros[i]),
            "Razao_Social": str(razao_social[i]),  # sinônimo de Cliente
            "Valor": v,
            "Data": datas[i],
        })

    df = pd.DataFrame(records)
    # Garantir exatamente 105 linhas
    while len(df) < 105:
        df = pd.concat([df, df.sample(1, random_state=SEED)], ignore_index=True)
    df = df.iloc[:105].reset_index(drop=True)
    return df


# ──────────────────────────────────────────────────────────────────────────────
# Aba 9 · cadastral_fuzzy · 80 linhas
# ──────────────────────────────────────────────────────────────────────────────

def gerar_aba_cadastral_fuzzy(rng: np.random.Generator) -> pd.DataFrame:
    """V11 · 40 oficiais + 40 ruidosas · CNPJ formato misto."""
    records = []
    for row in FORNECEDORES_OFICIAIS:
        fid, nome, cnpj, cidade, uf, seg = row
        records.append({
            "Fornecedor_ID": fid,
            "Nome_Fornecedor": nome,
            "CNPJ": cnpj,
            "Cidade": cidade,
            "UF": uf,
            "Segmento": seg,
        })
    for row in RUIDOS_FORNECEDOR:
        fid, nome, cnpj, cidade, uf, seg = row
        records.append({
            "Fornecedor_ID": fid,
            "Nome_Fornecedor": nome,
            "CNPJ": cnpj,
            "Cidade": cidade,
            "UF": uf,
            "Segmento": seg,
        })
    df = pd.DataFrame(records)
    return df


# ──────────────────────────────────────────────────────────────────────────────
# Aba 10 · vendas_volume_alto · 400 linhas
# ──────────────────────────────────────────────────────────────────────────────

def gerar_aba_vendas_volume_alto(rng: np.random.Generator) -> pd.DataFrame:
    """Pareto 80/20 · 45 Produtos · log-normal com concentração nos 12 primeiros."""
    n = 400
    produtos = PRODUTOS_45
    # Pareto: primeiros 12 produtos concentram ~80%
    pesos = np.zeros(45)
    pesos[:12] = rng.uniform(5, 15, 12)   # vitais
    pesos[12:] = rng.uniform(0.3, 2.5, 33)  # demais
    pesos = pesos / pesos.sum()

    cat_map = {p: CATEGORIAS_3[i % 3] for i, p in enumerate(produtos)}
    meses_2 = ["2025-01", "2025-02"]

    # Garantir 1 registro para cada um dos 45 produtos (cobertura completa)
    records = []
    for i, prod in enumerate(produtos):
        v_base = _lognormal(rng, 1, mu=6.5, sigma=1.0)[0]
        m_base = v_base * float(rng.uniform(0.1, 0.35))
        records.append({
            "Mes": meses_2[i % 2],
            "Loja": LOJAS[i % len(LOJAS)],
            "Produto": prod,
            "Categoria": cat_map[prod],
            "Vendas": float(round(v_base, 2)),
            "Margem": float(round(m_base, 2)),
            "Quantidade": int(rng.integers(5, 200)),
        })

    # Preencher com distribuição Pareto para os restantes 400-45=355
    n_extra = n - len(produtos)
    prods_escolhidos = rng.choice(produtos, size=n_extra, p=pesos)
    vendas = _lognormal(rng, n_extra, mu=6.5, sigma=1.0)
    margem = vendas * rng.uniform(0.1, 0.35, n_extra)
    qtd = rng.integers(5, 200, n_extra)
    mes_col = rng.choice(meses_2, size=n_extra)
    loja_col = rng.choice(LOJAS, size=n_extra)

    for i in range(n_extra):
        records.append({
            "Mes": mes_col[i],
            "Loja": loja_col[i],
            "Produto": prods_escolhidos[i],
            "Categoria": cat_map[prods_escolhidos[i]],
            "Vendas": float(round(vendas[i], 2)),
            "Margem": float(round(margem[i], 2)),
            "Quantidade": int(qtd[i]),
        })

    df = pd.DataFrame(records)
    # Injetar 5-8% NULO_MEDIDA (sobre linhas acima da cobertura mínima)
    null_idx = rng.choice(len(df), size=int(len(df) * 0.06), replace=False)
    for idx in null_idx:
        df.at[idx, "Vendas"] = None

    return df


# ──────────────────────────────────────────────────────────────────────────────
# Aba 11 · cardinalidade_excessiva · 200 linhas
# ──────────────────────────────────────────────────────────────────────────────

def gerar_aba_cardinalidade_excessiva(rng: np.random.Generator) -> pd.DataFrame:
    """85 categorias no agrupador · dispara BloqueioOperacional B-CARD-EXCESSIVA."""
    n = 200
    # 85 filiais únicas — garantir cobertura completa com 1 registro por filial
    filiais_85 = [f"Unidade-{i:03d}" for i in range(1, 86)]
    records = []
    # Primeiro: 1 registro por filial (85 linhas)
    for fil in filiais_85:
        records.append({
            "Filial": fil,
            "Valor_Frete": float(round(float(_lognormal(rng, 1, mu=6.0, sigma=1.0)[0]), 2)),
            "Prazo_Dias": int(rng.integers(1, 30)),
            "Status_Entrega": rng.choice(STATUS_ENTREGA),
        })
    # Complementar até 200 com escolha aleatória
    n_extra = n - len(filiais_85)
    filial_col = rng.choice(filiais_85, size=n_extra)
    valor = _lognormal(rng, n_extra, mu=6.0, sigma=1.0)
    prazo = rng.integers(1, 30, n_extra)
    for i in range(n_extra):
        records.append({
            "Filial": filial_col[i],
            "Valor_Frete": float(round(valor[i], 2)),
            "Prazo_Dias": int(prazo[i]),
            "Status_Entrega": rng.choice(STATUS_ENTREGA),
        })
    return pd.DataFrame(records)


# ──────────────────────────────────────────────────────────────────────────────
# Aba 12 · boolean_disfarcado · 60 linhas
# ──────────────────────────────────────────────────────────────────────────────

def gerar_aba_boolean_disfarcado(rng: np.random.Generator) -> pd.DataFrame:
    """Coluna Ativo com mistura Sim/Não/Ativo/Inativo · exercita D-008."""
    n = 60
    valores_bool = ["Sim", "Não", "Ativo", "Inativo"]
    pesos_bool = [0.35, 0.35, 0.15, 0.15]
    ativo_col = rng.choice(valores_bool, size=n, p=pesos_bool)
    loja_col = rng.choice(LOJAS, size=n)
    produto_col = rng.choice(PRODUTOS_12, size=n)
    vendas = _lognormal(rng, n, mu=5.5, sigma=0.8)
    records = []
    for i in range(n):
        records.append({
            "Loja": loja_col[i],
            "Produto": produto_col[i],
            "Ativo": ativo_col[i],
            "Vendas": float(round(vendas[i], 2)),
        })
    return pd.DataFrame(records)


# ──────────────────────────────────────────────────────────────────────────────
# Aba 13 · eixo_sequencial_lacunas · 80 linhas
# ──────────────────────────────────────────────────────────────────────────────

def gerar_aba_eixo_sequencial_lacunas(rng: np.random.Generator) -> pd.DataFrame:
    """T-EIXO com lacunas · faltam 2025-03 e 2025-07 · W-V3-EIXO-LACUNA (2)."""
    # 12 meses − 2 lacunas = 10 meses × ~8 linhas = 80
    meses_sem_lacuna = [m for m in MESES_ISO if m not in ("2025-03", "2025-07")]
    records = []
    for mes in meses_sem_lacuna:
        n_mes = 8
        vendas = _lognormal(rng, n_mes, mu=6.0, sigma=0.8)
        for i in range(n_mes):
            records.append({
                "Mes": mes,
                "Loja": rng.choice(LOJAS),
                "Produto": rng.choice(PRODUTOS_12),
                "Vendas": float(round(vendas[i], 2)),
                "Quantidade": int(rng.integers(5, 100)),
            })
    df = pd.DataFrame(records)
    df = df.iloc[:80].reset_index(drop=True)
    return df


# ──────────────────────────────────────────────────────────────────────────────
# Aba 14 · eixo_sequencial_completo · 100 linhas
# ──────────────────────────────────────────────────────────────────────────────

def gerar_aba_eixo_sequencial_completo(rng: np.random.Generator) -> pd.DataFrame:
    """T-EIXO caso feliz · 12 meses completos 2025-01 a 2025-12."""
    records = []
    for mes in MESES_ISO:
        n_mes = 9  # 12 × 9 = 108 → fatiado em 100
        vendas = _lognormal(rng, n_mes, mu=6.2, sigma=0.7)
        for i in range(n_mes):
            records.append({
                "Mes": mes,
                "Loja": rng.choice(LOJAS),
                "Produto": rng.choice(PRODUTOS_12),
                "Vendas": float(round(vendas[i], 2)),
                "Quantidade": int(rng.integers(5, 100)),
            })
    df = pd.DataFrame(records)
    df = df.iloc[:100].reset_index(drop=True)
    return df


# ──────────────────────────────────────────────────────────────────────────────
# Orquestrador principal
# ──────────────────────────────────────────────────────────────────────────────

ABAS_ORDEM = [
    ("vendas_padrao", gerar_aba_vendas_padrao),
    ("vendas_por_colunas", gerar_aba_vendas_por_colunas),
    ("vendas_pre_agregadas", gerar_aba_vendas_pre_agregadas),
    ("operacao_dispersao", gerar_aba_operacao_dispersao),
    ("operacao_cruzamento", gerar_aba_operacao_cruzamento),
    ("operacao_perfil_grupo", gerar_aba_operacao_perfil_grupo),
    ("dual_origem_crm", gerar_aba_dual_origem_crm),
    ("dual_comparado_erp", gerar_aba_dual_comparado_erp),
    ("cadastral_fuzzy", gerar_aba_cadastral_fuzzy),
    ("vendas_volume_alto", gerar_aba_vendas_volume_alto),
    ("cardinalidade_excessiva", gerar_aba_cardinalidade_excessiva),
    ("boolean_disfarcado", gerar_aba_boolean_disfarcado),
    ("eixo_sequencial_lacunas", gerar_aba_eixo_sequencial_lacunas),
    ("eixo_sequencial_completo", gerar_aba_eixo_sequencial_completo),
]


def gerar_todos_dataframes() -> dict:
    """Gera os 14 DataFrames com SEED=42 determinístico. Retorna dict nome→df."""
    # Reset global antes de qualquer geração
    np.random.seed(SEED)
    random.seed(SEED)
    rng = np.random.default_rng(SEED)
    resultado = {}
    for nome, func in ABAS_ORDEM:
        # Cada aba recebe o mesmo RNG base — mas como o RNG avança com cada chamada,
        # a ordem é determinística e cada aba consome o estado adiante do anterior.
        resultado[nome] = func(rng)
    return resultado


def gerar_xlsx(caminho_saida: str) -> dict:
    """Gera o arquivo Excel e retorna o dict de DataFrames."""
    dfs = gerar_todos_dataframes()
    Path(caminho_saida).parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(caminho_saida, engine="openpyxl") as writer:
        for nome, df in dfs.items():
            df.to_excel(writer, sheet_name=nome, index=False)
    return dfs


def hash_dfs(dfs: dict) -> str:
    """SHA-256 do conteúdo concatenado de todos os DataFrames."""
    h = hashlib.sha256()
    for nome in sorted(dfs.keys()):
        df = dfs[nome]
        # Usar to_csv para serialização estável (sem dependência de openpyxl)
        conteudo = df.to_csv(index=False).encode("utf-8")
        h.update(nome.encode("utf-8"))
        h.update(conteudo)
    return h.hexdigest()


if __name__ == "__main__":
    import time
    project_root = Path(__file__).parent.parent.parent
    saida = project_root / "bases" / "base_fundacao.xlsx"
    t0 = time.time()
    dfs = gerar_xlsx(str(saida))
    elapsed = time.time() - t0
    total_linhas = sum(len(df) for df in dfs.values())
    sha = hash_dfs(dfs)
    print(f"\n=== base_fundacao.xlsx gerada ===")
    for nome, df in dfs.items():
        print(f"  {nome}: {len(df)} linhas × {len(df.columns)} colunas")
    print(f"\nTotal linhas: {total_linhas}")
    print(f"SHA-256: {sha}")
    print(f"Tempo: {elapsed:.2f}s")
    print(f"Arquivo: {saida}")
