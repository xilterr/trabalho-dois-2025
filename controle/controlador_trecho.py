from entidade.trecho import Trecho
from limite.tela_trecho import TelaTrecho
from exception.opcao_invalida_exception import OpcaoInvalidaException
from exception.dado_em_branco_exception import DadoEmBrancoException
from controle.controlador_passeio import ControladorPasseio
from controle.controlador_transporte import ControladorTransporte
from DAO.trecho_dao import TrechoDAO


class ControladorTrecho:

    def __init__(self,
                controlador_sistema,
                controlador_passeio: ControladorPasseio,
                controlador_transporte: ControladorTransporte
                ):
        self.__trechos = []
        self.__tela_trecho = TelaTrecho()
        self.__controlador_sistema = controlador_sistema
        self.__controlador_passeio = ControladorPasseio
        self.__controlador_transporte = ControladorTransporte
        self.__trecho_DAO = TrechoDAO()

    def gera_id(self):
        lista_trechos = self.__trecho_DAO.get_all()

        if not lista_trechos:
            return 1

        maior_id = 1 + max([t.id for t in lista_trechos])
        return maior_id

    def pega_trecho_por_id(self):
        self.listar_trechos()
        id_selecionado = self.__tela_trecho.seleciona_trecho()

        if not self.__trecho_DAO.get_all():
            return None

        for trecho in self.__trecho_DAO.get_all():
            if trecho.id == id_selecionado:
                return trecho

        self.__tela_trecho.mostra_mensagem("ATENÇÃO: Trecho com este ID não foi encontrado.")
        return None

    def incluir_trecho(self): 
        dados_trecho = self.__tela_trecho.pega_dados_trecho()

        if dados_trecho is None:
            return

        try:
            if (not dados_trecho["data"] or 
                not dados_trecho["origem"] or 
                not dados_trecho["destino"]
                ):
                raise DadoEmBrancoException()

            novo_id = self.gera_id()
            novo_trecho = Trecho(
                novo_id,
                dados_trecho["data"],
                dados_trecho["origem"],
                dados_trecho["destino"],
                dados_trecho["transporte"]
            )
            
            self.__trecho_DAO.add(novo_trecho)
            self.__tela_trecho.mostra_mensagem(f"O trecho #{novo_trecho.id} foi cadastrado com sucesso!")

        except DadoEmBrancoException as e:
            self.__tela_trecho.mostra_mensagem(f"ERRO: {e}")

    def listar_trechos(self):
        if not self.__trecho_DAO.get_all():
            self.__tela_trecho.mostra_mensagem("ATENÇÃO: Não há trechos cadastrados")
            return
        else:
            self.__tela_trecho.mostra_mensagem('-------- LISTAGEM DOS TRECHOS ----------')

            for trecho in self.__trecho_DAO.get_all():
                dados_para_mostrar = {
                    "id": trecho.id,
                    "origem": trecho.origem.nome,
                    "destino": trecho.destino.nome,
                    "transporte": trecho.transporte.nome,
                }
                self.__tela_trecho.mostra_trecho(dados_para_mostrar)

    def alterar_trecho(self):
        if not self.__trecho_DAO.get_all():
            self.__tela_trecho.mostra_mensagem("ATENÇÃO: Não há trechos cadastrados")
            return

        try:
            trecho_selecionado = self.pega_trecho_por_id()

            if trecho_selecionado:
                novos_dados_trecho = self.__tela_trecho.pega_dados_trecho()

                if novos_dados_trecho is None:
                    return

                trecho_selecionado.nome = novos_dados_trecho["nome"]
                trecho_selecionado.telefone = novos_dados_trecho["telefone"]
                trecho_selecionado.data_nascimento = novos_dados_trecho["data_nascimento"]
                trecho_selecionado.cpf_passaporte = novos_dados_trecho["cpf_passaporte"]

                self.__trecho_DAO.update(trecho_selecionado)

                self.__tela_trecho.mostra_mensagem("Dados atualizados do trecho:")
                dados_atualizados = {
                    "id": trecho_selecionado.id,
                    "nome": trecho_selecionado.nome,
                    "telefone": trecho_selecionado.telefone,
                    "data_nascimento": trecho_selecionado.data_nascimento,
                    "cpf_passaporte": trecho_selecionado.cpf_passaporte,
                }
                self.__tela_trecho.mostra_trecho(dados_atualizados)
        except OpcaoInvalidaException as e:
            self.__tela_trecho.mostra_mensagem(f"ERRO: {e}")

    def excluir_trecho(self):
        if not self.__trecho_DAO.get_all():
            self.__tela_trecho.mostra_mensagem("ATENÇÃO: Não há trechos cadastrados")
            return

        try:
            trecho_selecionado = self.pega_trecho_por_id()

            if trecho_selecionado:
                self.__trecho_DAO.remove(trecho_selecionado.id)
                self.__tela_trecho.mostra_mensagem(f"O trecho {trecho_selecionado.nome}, "
                                                        f"ID #{trecho_selecionado.id} foi excluído com sucesso!")
        except OpcaoInvalidaException as e:
            self.__tela_trecho.mostra_mensagem(f"ERRO: {e}")

    def retornar(self):
        return

    def abre_tela(self):
        lista_opcoes = {1: self.incluir_trecho, 
                        2: self.listar_trechos,
                        3: self.alterar_trecho,
                        4: self.excluir_trecho,
                        0: self.retornar
                        }

        while True:
            try:
                opcao_escolhida = self.__tela_trecho.tela_opcoes()
                
                if opcao_escolhida == 0:
                    self.retornar()
                    break
                
                funcao_escolhida = lista_opcoes.get(opcao_escolhida)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    raise OpcaoInvalidaException("Opção de menu inválida.")
            except OpcaoInvalidaException as e:
                self.__tela_trecho.mostra_mensagem(f"\nERRO: {e}")
