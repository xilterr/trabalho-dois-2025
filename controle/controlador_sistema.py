from controle.controlador_participante import ControladorParticipante
from controle.controlador_viagem import ControladorViagem
from controle.controlador_empresa import ControladorEmpresa
from controle.controlador_pais import ControladorPais
from controle.controlador_passeio import ControladorPasseio
from controle.controlador_transporte import ControladorTransporte
from controle.controlador_cidade import ControladorCidade
from limite.tela_sistema import TelaSistema
from exception.opcao_invalida_exception import OpcaoInvalidaException
from exception.dado_em_branco_exception import DadoEmBrancoException


class ControladorSistema:

    def __init__(self):
        self.__tela_sistema = TelaSistema()
        self.__controlador_participante = ControladorParticipante(self)
        self.__controlador_empresa = ControladorEmpresa(self)
        self.__controlador_transporte = ControladorTransporte(self, self.__controlador_empresa)
        self.__controlador_pais = ControladorPais(self)
        self.__controlador_cidade = ControladorCidade(self, self.__controlador_pais)
        self.__controlador_passeio = ControladorPasseio(self)
        self.__controlador_viagem = ControladorViagem(self,
                                                      self.__controlador_participante,
                                                      self.__controlador_passeio
                                                      )

    @property
    def tela_sistema(self):
        return self.__tela_sistema

    @property
    def controlador_participante(self):
        return self.__controlador_participante

    @property
    def controlador_empresa(self):
        return self.__controlador_empresa

    @property
    def controlador_transporte(self):
        return self.__controlador_transporte

    @property
    def controlador_pais(self):
        return self.__controlador_pais

    @property
    def controlador_passeio(self):
        return self.__controlador_passeio

    @property
    def controlador_viagem(self):
        return self.__controlador_viagem

    def inicializa_sistema(self):
        self.abre_tela()

    def cadastra_participantes(self):
        self.__controlador_participante.abre_tela()

    def cadastra_empresas(self):
        self.__controlador_empresa.abre_tela()

    def cadastra_paises(self):
        self.__controlador_pais.abre_tela()

    def cadastra_cidades(self):
        self.__controlador_cidade.abre_tela()

    def cadastra_transportes(self):
        self.__controlador_transporte.abre_tela()

    def encerra_sistema(self):
        exit(0)

    def abre_tela(self):
        lista_opcoes = {1: self.cadastra_participantes,
                        2: self.cadastra_empresas,
                        3: self.cadastra_paises,
                        4: self.cadastra_cidades,
                        5: self.cadastra_transportes,
                        0: self.encerra_sistema
                        }

        while True:
            try:
                opcao_escolhida = self.__tela_sistema.tela_opcoes()
                if opcao_escolhida is None:
                    raise DadoEmBrancoException()

                if opcao_escolhida == 0:
                    self.encerra_sistema()
                    break
                
                funcao_escolhida = lista_opcoes.get(opcao_escolhida)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    raise OpcaoInvalidaException()

            except OpcaoInvalidaException or DadoEmBrancoException as e:
                self.__tela_sistema.mostra_mensagem(f"\nERRO: {e}")
