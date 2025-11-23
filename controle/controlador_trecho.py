from entidade.trecho import Trecho
from limite.tela_trecho import TelaTrecho
from exception.opcao_invalida_exception import OpcaoInvalidaException
from .controlador_passeio import ControladorPasseio
from .controlador_transporte import ControladorTransporte
from .controlador_participante import ControladorParticipante


class ControladorTrecho:

    def __init__(self, controlador_sistema, ctr_passeio: ControladorPasseio, 
                 ctr_transporte: ControladorTransporte, ctr_participante: ControladorParticipante):
        self.__trechos: list[Trecho] = []
        self.__tela_trecho = TelaTrecho()
        self.__controlador_sistema = controlador_sistema
        self.__controlador_passeio = ctr_passeio
        self.__controlador_transporte = ctr_transporte
        self.__controlador_participante = ctr_participante
        self.__proximo_id = 1

    def gera_id(self):
        id_gerado = self.__proximo_id
        self.__proximo_id += 1
        return id_gerado

    def pega_trecho_por_id(self, id: int) -> Trecho:
        for trecho in self.__trechos:
            if trecho.id == id:
                return trecho
        return None

    def incluir_trecho(self):
        self.__controlador_passeio.listar_cidades_disponiveis()
        self.__controlador_transporte.listar_transportes()

        dados = self.__tela_trecho.pega_dados_trecho()
        if dados:
            origem = self.__controlador_passeio.pega_cidade_por_id(dados["id_origem"])
            destino = self.__controlador_passeio.pega_cidade_por_id(dados["id_destino"])
            transporte = self.__controlador_transporte.pega_transporte_por_id(dados["id_transporte"])

            if origem and destino and transporte:
                novo_id = self.gera_id()
                novo_trecho = Trecho(novo_id, dados["data_viagem"], origem, destino, transporte, dados["valor"])
                self.__trechos.append(novo_trecho)
                self.__tela_trecho.mostra_mensagem("Trecho incluído com sucesso!")
            else:
                self.__tela_trecho.mostra_mensagem("ERRO: Cidade de origem, destino ou transporte não encontrado(s).")
    
    def listar_trechos(self):
        self.__tela_trecho.mostra_lista_trechos(self.__trechos)

    def definir_status_compra(self):
        self.listar_trechos()
        if not self.__trechos: return

        try:
            id_trecho = self.__tela_trecho.seleciona_trecho()
            trecho = self.pega_trecho_por_id(id_trecho)
            if trecho:
                status = self.__tela_trecho.pega_status_compra()
                trecho.compra_efetuada = status
                self.__tela_trecho.mostra_mensagem("Status da compra atualizado com sucesso!")
            else:
                self.__tela_trecho.mostra_mensagem("ATENÇÃO: Trecho não encontrado.")
        except OpcaoInvalidaException as e:
            self.__tela_trecho.mostra_mensagem(f"ERRO: {e}")

    def definir_responsavel_compra(self):
        self.listar_trechos()
        if not self.__trechos: return

        try:
            id_trecho = self.__tela_trecho.seleciona_trecho()
            trecho = self.pega_trecho_por_id(id_trecho)
            if trecho:
                self.__controlador_participante.listar_participantes()
                id_participante = self.__tela_trecho.le_num_inteiro_positivo("Digite o ID do participante responsável: ")
                participante = self.__controlador_participante.pega_participante_por_id(id_participante)
                if participante:
                    trecho.responsavel_compra = participante
                    self.__tela_trecho.mostra_mensagem("Responsável pela compra definido com sucesso!")
                else:
                    self.__tela_trecho.mostra_mensagem("ATENÇÃO: Participante não encontrado.")
            else:
                self.__tela_trecho.mostra_mensagem("ATENÇÃO: Trecho não encontrado.")
        except OpcaoInvalidaException as e:
            self.__tela_trecho.mostra_mensagem(f"ERRO: {e}")

    def abre_tela(self):
        lista_opcoes = {
            1: self.incluir_trecho,
            2: self.listar_trechos,
            5: self.definir_status_compra,
            6: self.definir_responsavel_compra
        }
        while True:
            try:
                opcao = self.__tela_trecho.tela_opcoes()
                if opcao == 0: break
                funcao = lista_opcoes.get(opcao)
                if funcao: funcao()
                else: raise OpcaoInvalidaException("Opção de menu inválida.")
            except OpcaoInvalidaException as e:
                self.__tela_trecho.mostra_mensagem(f"ERRO: {e}")
