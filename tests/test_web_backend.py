import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app


class TestBackendWeb(unittest.TestCase):
    def setUp(self):
        app.sessoes.clear()
        self.dados = dict(id='30', veiculo='Veículo A', tipo_carregador='Rápido - 22 kW', energia_kwh='45',
                          tempo_minutos='120', tarifa_kwh='1.5', data='2026-10-16', status='Finalizada')

    def test_fluxo_completo(self):
        for id_, energia, tempo, tarifa in [(30,45,120,1.5),(10,12.5,40,1.8),(20,28,75,1.6)]:
            app.criar_sessao(dict(self.dados,id=str(id_),energia_kwh=energia,tempo_minutos=tempo,tarifa_kwh=tarifa))
        self.assertEqual(app.busca_sequencial(app.sessoes,10),1)
        self.assertEqual(app.busca_sequencial(app.sessoes,99),-1)
        app.insertion_sort(app.sessoes,3,True)
        self.assertEqual([s.id for s in app.sessoes],[10,20,30])
        self.assertAlmostEqual(app.calcular_estatisticas(app.sessoes)['faturamento_total'],134.8)

    def test_duplicado_nao_altera_lista(self):
        app.criar_sessao(self.dados)
        with self.assertRaises(ValueError): app.criar_sessao(self.dados)
        self.assertEqual(len(app.sessoes),1)

    def test_numeros_invalidos(self):
        for valor in ('-1','nan','inf','texto','1000001'):
            with self.subTest(valor=valor),self.assertRaises(ValueError):
                app.criar_sessao(dict(self.dados,energia_kwh=valor))
        self.assertEqual(app.sessoes,[])

    def test_campos_invalidos(self):
        for campo,valor in [('id','0'),('id','2.5'),('veiculo','  '),('data','2026-02-30'),('status','Inválido'),('tipo_carregador','Inválido')]:
            with self.subTest(campo=campo),self.assertRaises(ValueError):
                app.criar_sessao(dict(self.dados,**{campo:valor}))

    def test_virgula_e_zero(self):
        resultado=app.criar_sessao(dict(self.dados,energia_kwh='12,5',tarifa_kwh='0'))
        self.assertEqual(resultado['energia_kwh'],12.5)
        self.assertEqual(resultado['custo'],0)

    def test_ordem_estavel(self):
        app.criar_sessao(self.dados)
        app.criar_sessao(dict(self.dados,id='10'))
        app.insertion_sort(app.sessoes,2)
        self.assertEqual([s.id for s in app.sessoes],[30,10])

if __name__=='__main__': unittest.main()
