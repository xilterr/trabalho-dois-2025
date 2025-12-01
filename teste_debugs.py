from datetime import date, time

# --- IMPORTAÇÕES DAS ENTIDADES ---
from entidade.participante import Participante
from entidade.pais import Pais
from entidade.cidade import Cidade
from entidade.passeio import Passeio

# --- IMPORTAÇÕES DOS DAOS ---
from DAO.participante_dao import ParticipanteDAO
from DAO.cidade_dao import CidadeDAO
from DAO.passeio_dao import PasseioDAO

# --- IMPORTAÇÕES DOS CONTROLADORES ---
from controle.controlador_passeio import ControladorPasseio
from controle.controlador_cidade import ControladorCidade
from controle.controlador_participante import ControladorParticipante
from controle.controlador_pais import ControladorPais

class SistemaStub:
    def __init__(self):
        self.participante_dao = ParticipanteDAO()
        self.cidade_dao = CidadeDAO()
        self.passeio_dao = PasseioDAO()
        
        self.controlador_pais = ControladorPais(self)
        
        self.controlador_participante = ControladorParticipante(self)
        self.controlador_cidade = ControladorCidade(self, self.controlador_pais)
        
        self.controlador_passeio = ControladorPasseio(self, 
                                                      self.controlador_cidade, 
                                                      self.controlador_participante)

    def abre_tela(self):
        print("--- Fim do Teste (Retornou ao Menu Principal Simulado) ---")
        exit(0)

def popular_dados_para_teste(sistema):
    print(">>> Criando dados de cenário (IDs 1 e 2)...")

    # CORREÇÃO AQUI: Adicionado ID 1 para o País
    brasil = Pais(1, "Brasil")
    
    c1 = Cidade(1, "Rio de Janeiro", brasil)
    c2 = Cidade(2, "Salvador", brasil)
    
    sistema.cidade_dao.add(c1)
    sistema.cidade_dao.add(c2)
    print("OK: Cidades cadastradas (IDs 1 e 2).")

    p1 = Participante(1, "Carlos Viajante", "1111-1111", "CPF123", date(1990, 5, 10))
    p2 = Participante(2, "Ana Turista", "2222-2222", "CPF456", date(1995, 8, 20))
    
    sistema.participante_dao.add(p1)
    sistema.participante_dao.add(p2)
    print("OK: Participantes cadastrados (IDs 1 e 2).")

    pass1 = Passeio(1, "Cristo Redentor", c1, time(9, 0), time(12, 0), 150.00)
    pass2 = Passeio(2, "Pelourinho Histórico", c2, time(14, 0), time(17, 0), 80.00)

    sistema.passeio_dao.add(pass1)
    sistema.passeio_dao.add(pass2)
    print("OK: Passeios cadastrados (IDs 1 e 2).")

if __name__ == "__main__":
    sistema = SistemaStub()
    
    try:
        popular_dados_para_teste(sistema)
    except Exception as e:
        print(f"Aviso: {e}")
        print("Provavelmente os dados já existem ou erro de PK.")

    print("\n### INICIANDO TELA DE PASSEIOS (PySimpleGUI) ###")
    sistema.controlador_passeio.abre_tela()