import unittest
from unittest.mock import MagicMock
from datetime import time
from controle.controlador_passeio import ControladorPasseio
from controle.controlador_participante import ControladorParticipante
from entidade.passeio import Passeio
from entidade.participante import Participante
from entidade.cidade import Cidade
from entidade.pais import Pais

class TestParticipantesEmPasseio(unittest.TestCase):

    def setUp(self):
        # 1. Cria Mocks para o sistema e controladores vizinhos
        self.mock_sistema = MagicMock()
        self.mock_ctrl_cidade = MagicMock()
        
        # Mockamos o ControladorParticipante inteiro para podermos simular suas respostas
        self.mock_ctrl_participante = MagicMock(spec=ControladorParticipante)
        
        # 2. Instancia o Controlador de Passeio (o alvo do teste)
        self.ctrl_passeio = ControladorPasseio(
            self.mock_sistema, 
            self.mock_ctrl_cidade, 
            self.mock_ctrl_participante
        )

        # 3. Substitui DAO e Tela internos por Mocks (para não salvar nada)
        self.ctrl_passeio._ControladorPasseio__passeio_DAO = MagicMock()
        self.ctrl_passeio._ControladorPasseio__tela_passeio = MagicMock()

        # 4. Cria dados falsos para o cenário
        self.cidade = Cidade(1, "Floripa", Pais(1, "BR"))
        self.passeio = Passeio(1, "Passeio Barco", self.cidade, time(10,0), time(12,0), 50.0)
        self.participante = Participante(10, "João", "999", "123456", "2000-01-01")

        # Configura o DAO para sempre retornar nosso passeio fake
        self.ctrl_passeio._ControladorPasseio__passeio_DAO.get_all.return_value = [self.passeio]
        
        # Configura a tela para sempre selecionar o ID 1 (nosso passeio)
        self.ctrl_passeio._ControladorPasseio__tela_passeio.seleciona_passeio.return_value = 1

    def test_adicionar_participante_ao_passeio(self):
        """Teste: Adicionar um participante a um passeio existente"""
        print("Testando ADICIONAR participante em passeio...")

        # ARRANGE
        # O controlador de participante vai retornar nosso 'João' quando chamado
        self.mock_ctrl_participante.pega_participante_por_id.return_value = self.participante
        
        # Garante lista vazia no inicio
        self.passeio._Passeio__participantes = []

        # ACT
        self.ctrl_passeio.adicionar_participante()

        # ASSERT
        # 1. Verifica se o João entrou na lista do objeto Passeio
        self.assertIn(self.participante, self.passeio.participantes)
        self.assertEqual(len(self.passeio.participantes), 1)
        
        # 2. Verifica se o DAO de Passeio foi chamado para salvar a atualização
        self.ctrl_passeio._ControladorPasseio__passeio_DAO.update.assert_called_with(self.passeio)
        
        print("-> Sucesso: Participante adicionado e passeio atualizado.")

    def test_adicionar_participante_duplicado(self):
        """Teste: Tentar adicionar o mesmo participante duas vezes"""
        print("Testando BLOQUEIO de duplicidade...")

        # ARRANGE
        # João já está na lista
        self.passeio.participantes.append(self.participante)
        
        # Usuário seleciona João de novo
        self.mock_ctrl_participante.pega_participante_por_id.return_value = self.participante

        # ACT
        self.ctrl_passeio.adicionar_participante()

        # ASSERT
        # Lista não deve crescer
        self.assertEqual(len(self.passeio.participantes), 1)
        
        # DAO.update NÃO deve ser chamado
        self.ctrl_passeio._ControladorPasseio__passeio_DAO.update.assert_not_called()
        
        print("-> Sucesso: Duplicidade evitada.")

    def test_remover_participante_do_passeio(self):
        """Teste: Remover participante da lista do passeio"""
        print("Testando REMOVER participante de passeio...")

        # ARRANGE
        # João está na lista
        self.passeio.participantes.append(self.participante)
        
        # Simulamos que o usuário digitou o ID 10 (ID do João) na tela de passeio
        self.ctrl_passeio._ControladorPasseio__tela_passeio.le_num_inteiro_positivo.return_value = 10

        # ACT
        self.ctrl_passeio.remover_participante()

        # ASSERT
        # 1. Lista deve estar vazia
        self.assertNotIn(self.participante, self.passeio.participantes)
        
        # 2. DAO deve ter sido chamado para salvar
        self.ctrl_passeio._ControladorPasseio__passeio_DAO.update.assert_called_with(self.passeio)
        
        print("-> Sucesso: Participante removido e passeio atualizado.")

if __name__ == '__main__':
    unittest.main(verbosity=2)