"""
t_diag.py — Coletor canônico de diagnóstico · T-DIAG · D-017
Consolidação de warnings · ajustes · decisões de usuário · bloqueios escapados
em DiagnosticoVN para aba Diagnóstico (sempre última aba).

Nenhuma visão emite warning direto — tudo passa por T-DIAG.
"""
from __future__ import annotations

from typing import List, Optional

from contratos import (
    AjusteMotor,
    BloqueioOperacional,
    CategoriaWarning,
    DecisaoUsuario,
    DiagnosticoVN,
    IntegridadeEstrutural,
    WarningEstrutural,
)


class TDIAG:
    """
    Coletor canônico de diagnóstico para uma execução de visão.

    Uso:
        diag = TDIAG("V3")
        diag.registrar_warning(w)
        diag.registrar_ajuste(a)
        diagnostico = diag.consolidar()
    """

    def __init__(self, visao_id: str) -> None:
        self.visao_id = visao_id
        self._warnings: List[WarningEstrutural] = []
        self._ajustes: List[AjusteMotor] = []
        self._decisoes_usuario: List[DecisaoUsuario] = []
        self._bloqueios_escapados: List[BloqueioOperacional] = []
        self._integridade: Optional[IntegridadeEstrutural] = None

    # ------------------------------------------------------------------
    # Registro
    # ------------------------------------------------------------------

    def registrar_warning(self, w: WarningEstrutural) -> None:
        """Registra warning em ordem de chegada · determinismo C.1."""
        self._warnings.append(w)

    def registrar_ajuste(self, a: AjusteMotor) -> None:
        self._ajustes.append(a)

    def registrar_decisao_usuario(self, d: DecisaoUsuario) -> None:
        self._decisoes_usuario.append(d)

    def registrar_bloqueio_escapado(self, b: BloqueioOperacional) -> None:
        """Registra bloqueio que teve escape acionado · rastreabilidade Seção 4."""
        self._bloqueios_escapados.append(b)

    def setar_integridade(self, i: IntegridadeEstrutural) -> None:
        self._integridade = i

    # ------------------------------------------------------------------
    # Consolidação
    # ------------------------------------------------------------------

    def consolidar(self) -> DiagnosticoVN:
        """
        Produz DiagnosticoVN com ordem determinística C.1.
        Warnings agrupados por CategoriaWarning.value em ordem canônica.
        """
        ordem_categoria = [c.value for c in CategoriaWarning]
        warnings_por_categoria: dict[str, list[WarningEstrutural]] = {
            cat: [] for cat in ordem_categoria
        }
        for w in self._warnings:
            cat_val = w.categoria.value if hasattr(w.categoria, "value") else w.categoria
            if cat_val in warnings_por_categoria:
                warnings_por_categoria[cat_val].append(w)
            else:
                warnings_por_categoria.setdefault(cat_val, []).append(w)

        # Remove categorias sem warnings para mapa enxuto
        warnings_filtrado = {k: v for k, v in warnings_por_categoria.items() if v}

        return DiagnosticoVN(
            ajustes_aplicados=list(self._ajustes),
            warnings_por_categoria=warnings_filtrado,
            decisoes_usuario=list(self._decisoes_usuario),
            bloqueios_informativos=list(self._bloqueios_escapados),
            integridade=self._integridade,
        )

    # ------------------------------------------------------------------
    # Helpers de fábrica para warnings padronizados
    # ------------------------------------------------------------------

    @staticmethod
    def w(
        codigo: str,
        categoria: CategoriaWarning,
        microcopy: str,
        linha_referenciada: Optional[int] = None,
        **contexto,
    ) -> WarningEstrutural:
        """Fábrica de WarningEstrutural · uso conveniente pelos transversais."""
        return WarningEstrutural(
            codigo=codigo,
            categoria=categoria,
            microcopy=microcopy,
            contexto=dict(contexto),
            linha_referenciada=linha_referenciada,
        )
