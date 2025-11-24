import unittest
from unittest.mock import MagicMock
from datetime import date
from controle.controlador_participante import ControladorParticipante
from entidade.participante import Participante
from entidade.cartao_credito import CartaoCredito

class TestControladorParticipanteCartao(unittest.TestCase):

    def setUp(self):
        # 1. Mocks do Sistema
        self.mock_sistema = MagicMock()
        
        # 2. Instancia o Controlador
        self.ctrl = ControladorParticipante(self.mock_sistema)

        # 3. Substitui DAO e Tela internos por Mocks
        self.ctrl._ControladorParticipante__participante_DAO = MagicMock()
        self.ctrl._ControladorParticipante__tela_participante = MagicMock()

        # 4. Cria um Participante Fake para os testes
        self.participante = Participante(1, "João", "9999", "CPF123", date(2000, 1, 1))
        
        # Configura o DAO para sempre retornar nosso participante fake nas buscas internas
        self.ctrl._ControladorParticipante__participante_DAO.get_all.return_value = [self.participante]
        
        # Configura a tela para selecionar o ID 1 (nosso participante) sempre que pedir participante
        self.ctrl._ControladorParticipante__tela_participante.seleciona_participante.return_value = 1

    def test_adicionar_cartao_sucesso(self):
        """Teste: Adicionar um cartão válido"""
        print("Testando ADICIONAR cartão...")

        # ARRANGE
        # Simula dados do cartão vindos da tela
        dados_cartao = {"numero": "12345678", "bandeira": "Visa"}
        self.ctrl._ControladorParticipante__tela_participante.pega_dados_cartao.return_value = dados_cartao
        
        # Garante que lista começa vazia
        self.participante._Participante__cartoes = [] 

        # ACT
        self.ctrl.adicionar_cartao()

        # ASSERT
        # 1. Verifica se o cartão entrou na lista do objeto
        self.assertEqual(len(self.participante.cartoes), 1)
        cartao_adicionado = self.participante.cartoes[0]
        self.assertEqual(str(cartao_adicionado.numero), "12345678")
        self.assertEqual(cartao_adicionado.bandeira, "Visa")
        
        # 2. Verifica se o DAO atualizou o PARTICIPANTE (que contem a lista)
        self.ctrl._ControladorParticipante__participante_DAO.update.assert_called_with(self.participante)
        print("-> Sucesso: Cartão adicionado e participante atualizado.")

    def test_adicionar_cartao_duplicado(self):
        """Teste: Bloquear adição de cartão idêntico"""
        print("Testando BLOQUEIO de cartão duplicado...")

        # ARRANGE
        # Já existe um cartão na lista
        cartao_existente = CartaoCredito(1, 1234, "Master")
        self.participante.cartoes.append(cartao_existente)
        
        # Usuário tenta adicionar o mesmo
        dados_duplicados = {"numero": "1234", "bandeira": "Master"}
        self.ctrl._ControladorParticipante__tela_participante.pega_dados_cartao.return_value = dados_duplicados

        # ACT
        self.ctrl.adicionar_cartao()

        # ASSERT
        # Lista não deve crescer
        self.assertEqual(len(self.participante.cartoes), 1)
        
        # DAO não deve ser chamado
        self.ctrl._ControladorParticipante__participante_DAO.update.assert_not_called()
        
        # Verifica se chamou mostra_mensagem (tratamento da exceção)
        self.ctrl._ControladorParticipante__tela_participante.mostra_mensagem.assert_called()
        print("-> Sucesso: Duplicidade bloqueada.")

    def test_listar_cartoes(self):
        """Teste: Listar cartões existentes"""
        print("Testando LISTAR cartões...")

        # ARRANGE
        c1 = CartaoCredito(1, 1111, "Visa")
        c2 = CartaoCredito(2, 2222, "Elo")
        self.participante._Participante__cartoes = [c1, c2]

        # ACT
        self.ctrl.listar_cartoes()

        # ASSERT
        # Verifica se o metodo de mostrar cartão foi chamado 2 vezes
        self.assertEqual(self.ctrl._ControladorParticipante__tela_participante.mostra_cartao.call_count, 2)
        print("-> Sucesso: Cartões listados.")

    def test_excluir_cartao_sucesso(self):
        """Teste: Excluir um cartão existente"""
        print("Testando EXCLUIR cartão...")

        # ARRANGE
        c1 = CartaoCredito(10, 1234, "Visa")
        self.participante.cartoes.append(c1)
        
        # Simula usuário escolhendo o ID 10 na tela de seleção de CARTÃO
        self.ctrl._ControladorParticipante__tela_participante.seleciona_cartao.return_value = 10

        # ACT
        # Passamos None porque sua definição atual pede um argumento 'participante' extra
        self.ctrl.excluir_cartao(None)

        # ASSERT
        # 1. Lista deve estar vazia
        self.assertEqual(len(self.participante.cartoes), 0)
        
        # 2. DAO deve ser atualizado
        self.ctrl._ControladorParticipante__participante_DAO.update.assert_called_with(self.participante)
        print("-> Sucesso: Cartão removido.")

    def test_excluir_cartao_inexistente(self):
        """Teste: Tentar excluir um cartão que não existe"""
        print("Testando EXCLUIR cartão inexistente...")

        # ARRANGE
        c1 = CartaoCredito(10, 1234, "Visa")
        self.participante.cartoes.append(c1)
        
        # Simula usuário escolhendo ID 99 (que não existe)
        self.ctrl._ControladorParticipante__tela_participante.seleciona_cartao.return_value = 99

        # ACT
        self.ctrl.excluir_cartao(None)

        # ASSERT
        # Lista continua igual
        self.assertEqual(len(self.participante.cartoes), 1)
        
        # Verifica se mostrou mensagem de erro (gerada pela Exception capturada)
        self.ctrl._ControladorParticipante__tela_participante.mostra_mensagem.assert_called()
        print("-> Sucesso: Erro tratado corretamente.")

if __name__ == '__main__':
    unittest.main(verbosity=2)