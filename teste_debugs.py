import unittest
from unittest.mock import MagicMock
from datetime import date
from controle.controlador_trecho import ControladorTrecho
from entidade.trecho import Trecho
from entidade.cidade import Cidade
from entidade.transporte import Transporte
from entidade.pais import Pais
from entidade.empresa import Empresa
from entidade.tipo_transporte import TipoTransporte

class TestControladorTrechoFinal(unittest.TestCase):

    def setUp(self):
        # Mocks das dependências
        self.mock_sistema = MagicMock()
        self.mock_ctrl_passeio = MagicMock()
        self.mock_ctrl_transporte = MagicMock()
        self.mock_ctrl_cidade = MagicMock()

        # Instancia o Controlador a ser testado
        self.ctrl = ControladorTrecho(
            self.mock_sistema,
            self.mock_ctrl_passeio,
            self.mock_ctrl_transporte,
            self.mock_ctrl_cidade
        )

        # Substitui DAO e Tela internos por Mocks
        self.ctrl._ControladorTrecho__trecho_DAO = MagicMock()
        self.ctrl._ControladorTrecho__tela_trecho = MagicMock()

        # Dados Fake para simulação
        self.pais = Pais(1, "BR")
        self.origem = Cidade(1, "Floripa", self.pais)
        self.destino = Cidade(2, "Curitiba", self.pais)
        self.empresa = Empresa(1, "Viação X", "111", "CNPJ")
        self.transporte = Transporte(1, "Bus Leito", TipoTransporte.onibus, self.empresa)

    def test_1_incluir_trecho(self):
        """Teste CREATE: Incluir Trecho com sucesso"""
        print("Testando INCLUIR trecho...")

        # ARRANGE
        # Simula seleção: 1º Origem, 2º Destino
        self.mock_ctrl_cidade.pega_cidade_por_id.side_effect = [self.origem, self.destino]
        # Simula seleção transporte
        self.mock_ctrl_transporte.pega_transporte_por_id.return_value = self.transporte
        
        # Simula data vinda da tela
        self.ctrl._ControladorTrecho__tela_trecho.pega_dados_trecho.return_value = {"data": date(2023, 12, 25)}
        
        # DAO Vazio para gerar ID 1
        self.ctrl._ControladorTrecho__trecho_DAO.get_all.return_value = []

        # ACT
        self.ctrl.incluir_trecho()

        # ASSERT
        # Verifica se chamou o DAO.add
        self.ctrl._ControladorTrecho__trecho_DAO.add.assert_called_once()
        
        # Verifica dados do objeto salvo
        args, _ = self.ctrl._ControladorTrecho__trecho_DAO.add.call_args
        trecho_salvo = args[0]
        self.assertEqual(trecho_salvo.origem, self.origem)
        self.assertEqual(trecho_salvo.destino, self.destino)
        self.assertEqual(trecho_salvo.transporte, self.transporte)
        print("-> Sucesso: Trecho incluído.")

    def test_2_listar_trechos(self):
        """Teste READ: Listar Trechos"""
        print("Testando LISTAR trechos...")

        # ARRANGE
        trecho_fake = Trecho(1, date(2023,1,1), self.origem, self.destino, self.transporte)
        self.ctrl._ControladorTrecho__trecho_DAO.get_all.return_value = [trecho_fake]

        # ACT
        self.ctrl.listar_trechos()

        # ASSERT
        self.ctrl._ControladorTrecho__tela_trecho.mostra_trecho.assert_called()
        print("-> Sucesso: Dados enviados para tela.")

    def test_3_alterar_trecho(self):
        """Teste UPDATE: Alterar Trecho"""
        print("Testando ALTERAR trecho...")

        # ARRANGE
        trecho_existente = Trecho(1, date(2020,1,1), self.origem, self.destino, self.transporte)
        self.ctrl._ControladorTrecho__trecho_DAO.get_all.return_value = [trecho_existente]
        
        # Tela seleciona ID 1
        self.ctrl._ControladorTrecho__tela_trecho.seleciona_trecho.return_value = 1
        
        # Simula NOVAS escolhas (Inverte cidades e mantem transporte)
        self.mock_ctrl_cidade.pega_cidade_por_id.side_effect = [self.destino, self.origem]
        self.mock_ctrl_transporte.pega_transporte_por_id.return_value = self.transporte
        
        # Nova data
        self.ctrl._ControladorTrecho__tela_trecho.pega_dados_trecho.return_value = {"data": date(2025, 1, 1)}

        # ACT
        self.ctrl.alterar_trecho()

        # ASSERT
        self.ctrl._ControladorTrecho__trecho_DAO.update.assert_called_once()
        # Verifica alteração em memória
        self.assertEqual(trecho_existente.data, date(2025, 1, 1))
        self.assertEqual(trecho_existente.origem, self.destino) # Mudou de Floripa para Curitiba
        print("-> Sucesso: Trecho atualizado.")

    def test_4_excluir_trecho(self):
        """Teste DELETE: Excluir Trecho"""
        print("Testando EXCLUIR trecho...")

        # ARRANGE
        trecho_del = Trecho(1, date(2023,1,1), self.origem, self.destino, self.transporte)
        self.ctrl._ControladorTrecho__trecho_DAO.get_all.return_value = [trecho_del]
        self.ctrl._ControladorTrecho__tela_trecho.seleciona_trecho.return_value = 1

        # ACT
        self.ctrl.excluir_trecho()

        # ASSERT
        # Verifica se removeu pelo ID 1
        self.ctrl._ControladorTrecho__trecho_DAO.remove.assert_called_with(1)
        print("-> Sucesso: Trecho removido.")

if __name__ == '__main__':
    unittest.main(verbosity=2)