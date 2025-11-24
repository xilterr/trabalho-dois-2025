from entidade.trecho import Trecho
from limite.tela_trecho import TelaTrecho
from exception.opcao_invalida_exception import OpcaoInvalidaException
from exception.dado_em_branco_exception import DadoEmBrancoException
from controle.controlador_passeio import ControladorPasseio
from controle.controlador_transporte import ControladorTransporte
from controle.controlador_cidade import ControladorCidade
from DAO.trecho_dao import TrechoDAO


class ControladorTrecho:

    def __init__(self,
                controlador_sistema,
                controlador_passeio: ControladorPasseio,
                controlador_transporte: ControladorTransporte,
                controlador_cidade: ControladorCidade
                ):
        self.__trechos = []
        self.__tela_trecho = TelaTrecho()
        self.__controlador_sistema = controlador_sistema
        self.__controlador_passeio = controlador_passeio
        self.__controlador_cidade = controlador_cidade
        self.__controlador_transporte = controlador_transporte
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
        origem = self.__controlador_cidade.pega_cidade_por_id()
        if origem is None:
            return

        destino = self.__controlador_cidade.pega_cidade_por_id()
        if destino is None:
            return

        if origem.id == destino.id:
            #quero que tenha um raise OpcaoInvalidaException, todos erros precisam ser mostrados com exception
            self.__tela_trecho.mostra_mensagem("ERRO: Origem e destino não podem ser iguais.")
            return

        transporte = self.__controlador_transporte.pega_transporte_por_id()
        if transporte is None:
            return

        dados_trecho = self.__tela_trecho.pega_dados_trecho()
        if dados_trecho is None:
            return

        try:
            if not dados_trecho["data"]:
                raise DadoEmBrancoException()

            novo_id = self.gera_id()
            novo_trecho = Trecho(
                novo_id,
                dados_trecho["data"],
                origem,
                destino,
                transporte
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
                    "data": trecho.data,
                    "origem": trecho.origem.nome,
                    "destino": trecho.destino.nome,
                    "transporte": trecho.transporte.nome,
                    "empresa": trecho.transporte.empresa.nome
                }
                self.__tela_trecho.mostra_trecho(dados_para_mostrar)

    def alterar_trecho(self):
        if not self.__trecho_DAO.get_all():
            self.__tela_trecho.mostra_mensagem("ATENÇÃO: Não há trechos cadastrados")
            return

        try:
            trecho_selecionado = self.pega_trecho_por_id()

            if trecho_selecionado:
                nova_origem = self.__controlador_cidade.pega_cidade_por_id()
                if nova_origem is None:
                    return

                novo_destino = self.__controlador_cidade.pega_cidade_por_id()
                if novo_destino is None:
                    return

                if nova_origem.id == novo_destino.id:
                    raise OpcaoInvalidaException("Origem e destino não podem ser iguais.")

                novo_transporte = self.__controlador_transporte.pega_transporte_por_id()
                if novo_transporte is None:
                    return

                novos_dados = self.__tela_trecho.pega_dados_trecho()
                if novos_dados is None:
                    return

                trecho_selecionado.origem = nova_origem
                trecho_selecionado.destino = novo_destino
                trecho_selecionado.transporte = novo_transporte
                trecho_selecionado.data = novos_dados["data"]

                self.__trecho_DAO.update(trecho_selecionado)

                self.__tela_trecho.mostra_mensagem("Dados do trecho atualizados com sucesso!")
                
                dados_atualizados = {
                    "id": trecho_selecionado.id,
                    "data": trecho_selecionado.data,
                    "origem": trecho_selecionado.origem.nome,
                    "destino": trecho_selecionado.destino.nome,
                    "transporte": trecho_selecionado.transporte.nome,
                    "empresa": trecho_selecionado.transporte.empresa.nome
                }
                self.__tela_trecho.mostra_trecho(dados_atualizados)

        except (DadoEmBrancoException, OpcaoInvalidaException) as e:
            self.__tela_trecho.mostra_mensagem(f"ERRO: {e}")

    def excluir_trecho(self):
        if not self.__trecho_DAO.get_all():
            self.__tela_trecho.mostra_mensagem("ATENÇÃO: Não há trechos cadastrados")
            return

        try:    
            trecho_selecionado = self.pega_trecho_por_id()

            if trecho_selecionado:
                self.__trecho_DAO.remove(trecho_selecionado.id)
                self.__tela_trecho.mostra_mensagem(f"O trecho #{trecho_selecionado.id}, foi excluído com sucesso!")
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
                self.__tela_trecho.mostra_mensagem(f"\nERRO: {e}")##
