"""Testes capability 11 · `formato_adaptativo_por_unidade` · D-205 · D-202 etapa 7."""
from __future__ import annotations

import pytest

from apresentacao.formatos import formato_adaptativo_por_unidade


class TestCasasDefault:
    def test_monetario_default_2_casas(self):
        texto, nota = formato_adaptativo_por_unidade(1234.5, "MONETARIO_BRL")
        assert texto == "1.234,50"
        assert nota is None

    def test_percentual_default_2_casas(self):
        texto, nota = formato_adaptativo_por_unidade(15.5, "PERCENTUAL")
        assert texto == "15,50%"
        assert nota is None

    def test_quantidade_inteiro_zero_casas(self):
        texto, nota = formato_adaptativo_por_unidade(5.0, "QUANTIDADE")
        assert texto == "5"
        assert nota is None

    def test_tempo_horas_inteiro_sem_casas(self):
        texto, nota = formato_adaptativo_por_unidade(5.0, "TEMPO_HORAS")
        assert texto == "5h"
        assert nota is None

    def test_razao_default_4_casas(self):
        texto, nota = formato_adaptativo_por_unidade(1.2345, "RAZAO")
        assert texto == "1,2345"
        assert nota is None


class TestAdaptativo:
    def test_quantidade_meia_unidade_alterna_para_1_casa(self):
        # Fração ≥0.5 · adapta para 1 casa
        texto, _ = formato_adaptativo_por_unidade(5.5, "QUANTIDADE")
        assert texto == "5,5"

    def test_tempo_horas_fracao_relevante_alterna(self):
        texto, _ = formato_adaptativo_por_unidade(5.6, "TEMPO_HORAS")
        assert texto == "5,6h"

    def test_tempo_dias_fracao_baixa_mantem(self):
        # Fração 0.3 < 0.5 · mantém formato default (zero casas)
        texto, _ = formato_adaptativo_por_unidade(5.3, "TEMPO_DIAS")
        assert texto == "5d"


class TestNotaTecnica:
    def test_tempo_horas_variacao_alta_emite_nota(self):
        # contexto: caller detectou que arredondados ficaram iguais e
        # variação real é -6% · acima do limite 5%.
        texto, nota = formato_adaptativo_por_unidade(
            5.0, "TEMPO_HORAS",
            contexto_variacao_pct=-0.06,
            contexto_arredondados_iguais=True,
        )
        assert texto == "5h"
        assert nota is not None
        assert "5" not in (nota or "").split("·")[0] or "Variação real" in nota
        assert "podem parecer iguais" in nota

    def test_tempo_horas_variacao_baixa_nao_emite(self):
        # 3% < 5% · sem nota
        _, nota = formato_adaptativo_por_unidade(
            5.0, "TEMPO_HORAS",
            contexto_variacao_pct=0.03,
            contexto_arredondados_iguais=True,
        )
        assert nota is None

    def test_tempo_horas_sem_contexto_nao_emite(self):
        # caller não passou contexto · sem nota
        _, nota = formato_adaptativo_por_unidade(5.0, "TEMPO_HORAS")
        assert nota is None

    def test_percentual_nunca_emite_nota(self):
        _, nota = formato_adaptativo_por_unidade(
            5.0, "PERCENTUAL",
            contexto_variacao_pct=0.10,
            contexto_arredondados_iguais=True,
        )
        assert nota is None


class TestCasosBordas:
    def test_none_retorna_traco(self):
        texto, nota = formato_adaptativo_por_unidade(None, "MONETARIO_BRL")
        assert texto == "—"
        assert nota is None

    def test_valor_negativo_preserva_sinal(self):
        texto, _ = formato_adaptativo_por_unidade(-100.50, "MONETARIO_BRL")
        assert texto == "-100,50"

    def test_unidade_desconhecida_cai_em_monetario(self):
        texto, _ = formato_adaptativo_por_unidade(100.0, "BLABLA_INVALIDA")
        # cai em MONETARIO_BRL · 2 casas
        assert texto == "100,00"
