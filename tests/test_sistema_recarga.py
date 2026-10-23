import sys
import unittest
from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA_PROJETO))

from sistema_recarga import (  # noqa: E402
    Sessao,
    busca_sequencial,
    calcular_estatisticas,
    insertion_sort,
)


def criar_sessao(id_sessao, energia, tempo, tarifa):
    return Sessao(
        id_sessao,
        f"Veículo {id_sessao}",
        "Rápido - 22 kW",
        energia,
        tempo,
        tarifa,
        "07/09/2026",
        "Finalizada",
    )


class TesteSistemaRecarga(unittest.TestCase):
    def setUp(self):
        self.sessoes = [
            criar_sessao(30, 45.0, 120, 1.50),
            criar_sessao(10, 12.5, 40, 1.80),
            criar_sessao(20, 28.0, 75, 1.60),
        ]

    def test_calculo_do_custo(self):
        self.assertAlmostEqual(self.sessoes[0].custo, 67.50)

    def test_busca_sequencial(self):
        self.assertEqual(busca_sequencial(self.sessoes, 10), 1)
        self.assertEqual(busca_sequencial(self.sessoes, 99), -1)

    def test_ordenacao_por_id(self):
        insertion_sort(self.sessoes, criterio=1, crescente=True)
        ids = [sessao.id for sessao in self.sessoes]
        self.assertEqual(ids, [10, 20, 30])

    def test_ordenacao_por_energia_decrescente(self):
        insertion_sort(self.sessoes, criterio=2, crescente=False)
        energias = [sessao.energia_kwh for sessao in self.sessoes]
        self.assertEqual(energias, [45.0, 28.0, 12.5])

    def test_estatisticas(self):
        dados = calcular_estatisticas(self.sessoes)
        self.assertEqual(dados["quantidade"], 3)
        self.assertAlmostEqual(dados["energia_total"], 85.5)
        self.assertAlmostEqual(dados["faturamento_total"], 134.8)
        self.assertAlmostEqual(dados["custo_medio"], 134.8 / 3)
        self.assertAlmostEqual(dados["maior_consumo"], 45.0)
        self.assertAlmostEqual(dados["menor_consumo"], 12.5)


if __name__ == "__main__":
    unittest.main()
