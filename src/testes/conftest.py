"""
conftest.py — Configuração do pytest para /src/testes/
Adiciona /src ao sys.path para permitir imports diretos dos módulos da Fundação.
Extendido em F-TRANS para incluir fixtures compartilhadas dos transversais.
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

# Garante que /src está no path (para import de contratos, motor_upload, motor_base)
src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Garante que /src/transversais e /src/utils estão acessíveis
transversais_path = str(Path(__file__).parent.parent / "transversais")
if transversais_path not in sys.path:
    sys.path.insert(0, transversais_path)


# ---------------------------------------------------------------------------
# Fixtures compartilhadas F-TRANS
# ---------------------------------------------------------------------------

@pytest.fixture
def df_vendas():
    """DataFrame simples de vendas · usado por múltiplos transversais."""
    return pd.DataFrame({
        "produto": ["A", "B", "C", "A", "B"],
        "regiao": ["Norte", "Sul", "Norte", "Sul", "Norte"],
        "valor": [100.0, 200.0, 150.0, 120.0, 80.0],
        "qtd": [10, 20, 15, 12, 8],
    })


@pytest.fixture
def df_temporal():
    """DataFrame com coluna temporal em pt-BR · T-AGRUPA e T-EIXO."""
    return pd.DataFrame({
        "mes": ["jan", "fev", "mar", "abr", "mai"],
        "valor": [100.0, 200.0, 150.0, 300.0, 250.0],
    })


@pytest.fixture
def df_pre_agregado():
    """DataFrame já pré-agregado · uma linha por chave · T-AGRUPA modo PRE_AGREGADO."""
    return pd.DataFrame({
        "produto": ["A", "B", "C"],
        "valor": [100.0, 200.0, 150.0],
    })


@pytest.fixture
def df_pre_agregado_com_duplicata():
    """DataFrame pré-agregado mas com duplicata · dispara warning T-AGRUPA."""
    return pd.DataFrame({
        "produto": ["A", "B", "C", "A"],
        "valor": [100.0, 200.0, 150.0, 50.0],
    })
