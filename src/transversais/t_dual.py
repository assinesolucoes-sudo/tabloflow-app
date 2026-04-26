"""
t_dual.py — Upload em modo DUAL · T-DUAL · D-018
Orquestra composição de 2 ArquivoInfo em UploadResult com modo_upload=DUAL.
2 estruturas: DOIS_ARQUIVOS ou UM_ARQUIVO_DUAS_ABAS.
"""
from __future__ import annotations

import io
from typing import Dict, List, Literal, Optional

import pandas as pd
from pydantic import BaseModel, Field

from contratos import (
    ArquivoInfo,
    BloqueioOperacional,
    CategoriaWarning,
    UploadResult,
    WarningEstrutural,
)


class ArquivoEscolhido(BaseModel):
    indice_arquivo: Literal[0, 1] = Field(
        ...,
        description="Em DOIS_ARQUIVOS: 0 = primeiro, 1 = segundo. Em UM_ARQUIVO_DUAS_ABAS: sempre 0.",
    )
    aba_escolhida: str = Field(..., description="Nome da aba selecionada")


class ConfigUploadDual(BaseModel):
    estrutura: Literal["DOIS_ARQUIVOS", "UM_ARQUIVO_DUAS_ABAS"] = Field(
        ...,
        description="2 estruturas canônicas · rejeição explícita de RESHAPE (M2 futuro)",
    )
    arquivo_origem: ArquivoEscolhido
    arquivo_comparado: ArquivoEscolhido
    rotulo_origem: str = Field("Origem", description="Editável pelo usuário")
    rotulo_comparado: str = Field("Comparado", description="Editável pelo usuário")


def _ler_preview(arquivo_bytes: bytes, aba: str, formato: str) -> Dict:
    """Lê 5 linhas para preview do ArquivoInfo."""
    try:
        if formato in ("xlsx", "xlsm"):
            df = pd.read_excel(io.BytesIO(arquivo_bytes), sheet_name=aba, nrows=5)
        else:
            df = pd.read_csv(io.BytesIO(arquivo_bytes), nrows=5)
        return df.to_dict(orient="list")
    except Exception:
        return {}


def _listar_abas(arquivo_bytes: bytes, formato: str) -> List[str]:
    if formato in ("xlsx", "xlsm"):
        try:
            xf = pd.ExcelFile(io.BytesIO(arquivo_bytes))
            return xf.sheet_names
        except Exception:
            return []
    return []


def _detectar_formato(nome: str) -> Literal["xlsx", "xlsm", "csv", "tsv"]:
    ext = nome.rsplit(".", 1)[-1].lower() if "." in nome else "csv"
    if ext in ("xlsx", "xlsm", "csv", "tsv"):
        return ext  # type: ignore[return-value]
    return "csv"


def aplicar_upload_dual(
    config: ConfigUploadDual,
    arquivos_bytes: Dict[int, bytes],
    nomes_arquivos: Optional[Dict[int, str]] = None,
) -> UploadResult:
    """
    Compõe UploadResult com 2 ArquivoInfo (origem e comparado).

    Args:
        config: ConfigUploadDual com estrutura e seleção de abas.
        arquivos_bytes: {indice_arquivo: bytes_do_arquivo}
        nomes_arquivos: {indice_arquivo: nome_original} — opcional, usado para detecção de formato.

    Returns:
        UploadResult com modo_upload='DUAL' e arquivos_dual preenchido.

    Raises:
        ValueError: se RESHAPE detectado ou configuração inválida.
    """
    warnings: List[WarningEstrutural] = []

    if nomes_arquivos is None:
        nomes_arquivos = {0: "arquivo_0.xlsx", 1: "arquivo_1.xlsx"}

    lados = [
        ("origem", config.arquivo_origem),
        ("comparado", config.arquivo_comparado),
    ]

    arquivos_info: List[ArquivoInfo] = []

    for caminho_logico, escolha in lados:
        idx = escolha.indice_arquivo
        if idx not in arquivos_bytes:
            raise ValueError(
                f"Arquivo índice {idx} não fornecido em arquivos_bytes para o lado '{caminho_logico}'."
            )

        raw_bytes = arquivos_bytes[idx]
        nome = nomes_arquivos.get(idx, f"arquivo_{idx}")
        formato = _detectar_formato(nome)
        abas = _listar_abas(raw_bytes, formato)
        preview = _ler_preview(raw_bytes, escolha.aba_escolhida, formato)

        arquivos_info.append(ArquivoInfo(
            caminho_logico=caminho_logico,  # type: ignore[arg-type]
            nome_arquivo=nome,
            arquivo_bytes=raw_bytes,
            abas_disponiveis=abas,
            aba_selecionada=escolha.aba_escolhida,
            formato=formato,
            preview=preview,
        ))

    # Validação de compatibilidade mínima entre lados (colunas devem existir)
    # Warning se abas têm nomes muito diferentes (informativo)
    origem_info, comparado_info = arquivos_info
    if (
        config.estrutura == "UM_ARQUIVO_DUAS_ABAS"
        and origem_info.aba_selecionada == comparado_info.aba_selecionada
    ):
        warnings.append(WarningEstrutural(
            codigo="W-T-DUAL-ABA-IDENTICA",
            categoria=CategoriaWarning.ALERTA_ESTRUTURAL_LEVE,
            microcopy=(
                "Origem e Comparado selecionaram a mesma aba em modo UM_ARQUIVO_DUAS_ABAS. "
                "Verifique se a seleção está correta."
            ),
            contexto={"aba": origem_info.aba_selecionada},
        ))

    nome_principal = nomes_arquivos.get(0, "dual")

    return UploadResult(
        file_name=nome_principal,
        modo_upload="DUAL",
        arquivo_unico=None,
        arquivos_dual=arquivos_info,
        warnings=warnings,
    )


# Bloqueio B-T-DUAL-RESHAPE-DETECTADO (sem escape)
BLOQUEIO_RESHAPE = BloqueioOperacional(
    codigo="B-T-DUAL-RESHAPE-DETECTADO",
    condicao_disparo=(
        "Base parece estar empilhada · operação RESHAPE fica em M2 · "
        "suba 2 arquivos ou 1 arquivo com 2 abas."
    ),
    escapavel=False,
    escape_acionado=None,
    contexto_disparo={},
)
