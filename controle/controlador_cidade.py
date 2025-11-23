from entidade.pais import Pais
from entidade.cidade import Cidade
from limite.tela_cidade import TelaCidade
from exception.opcao_invalida_exception import OpcaoInvalidaException
from exception.dado_em_branco_exception import DadoEmBrancoException
from exception.cidade_repetida_exception import CidadeRepetidoException
from controle.controlador_pais import ControladorPais
from DAO.cidade_dao import CidadeDAO


class ControladorCidade:

    def __init__(self, controlador_sistema, controlador_pais: ControladorPais):
        self.__cidade_DAO = CidadeDAO()
        self.__tela_cidade = TelaCidade()
        self.__controlador_sistema = controlador_sistema
        self.__controlador_pais = controlador_pais
        self.__id_atual = 0

    def gera_id(self):
        lista_cidades = self.__cidade_DAO.get_all()

        if not lista_cidades:
            return 1

        maior_id = 1 + max([p.id for p in lista_cidades])
        return maior_id

    def pega_cidade_por_id(self):
        self.listar_cidade()
        id_selecionado = self.__tela_cidade.seleciona_cidade()

        if not self.__cidade_DAO.get_all():
            return None

        for cidade in self.__cidade_DAO.get_all():
            if cidade.id == id_selecionado:
                return cidade

        self.__tela_cidade.mostra_mensagem("ATENÇÃO: cidade com este ID não foi encontrado.")
        return None

    def incluir_cidade(self): 
        pais_selecionado = self.__controlador_pais.pega_pais_por_id()
        if pais_selecionado is None:
            return

        dados_cidade = self.__tela_cidade.pega_dados_cidade()
        if dados_cidade is None:
            return

        try:
            if not dados_cidade["nome"]:
                raise DadoEmBrancoException()

            for cidade in self.__cidade_DAO.get_all():
                if cidade.nome == dados_cidade["nome"]:
                    raise CidadeRepetidoException(dados_cidade["nome"])

            novo_id = self.gera_id()
            nova_cidade = Cidade(
                novo_id,
                dados_cidade["nome"],
                pais_selecionado
                )
            
            self.__cidade_DAO.add(nova_cidade)
            self.__tela_cidade.mostra_mensagem(f"A cidade {nova_cidade.nome} foi cadastrada com sucesso!")

        except (CidadeRepetidoException, DadoEmBrancoException) as e:
            self.__tela_cidade.mostra_mensagem(f"ERRO: {e}")

    def listar_cidade(self):
        if not self.__cidade_DAO.get_all():
            self.__tela_cidade.mostra_mensagem("ATENÇÃO: Não há cidade cadastrada")
            return
        else:
            self.__tela_cidade.mostra_mensagem('-------- LISTAGEM DAS CIDADES ----------')

            for cidade in self.__cidade_DAO.get_all():
                dados_para_mostrar = {
                    "id": cidade.id,
                    "nome": cidade.nome,
                    "pais_nome": cidade.pais.nome
                    }
                self.__tela_cidade.mostra_cidade(dados_para_mostrar)

    def alterar_cidade(self):
        if not self.__cidade_DAO.get_all():
            self.__tela_cidade.mostra_mensagem("ATENÇÃO: Não há cidade cadastrada.")
            return

        try:
            cidade_selecionada = self.pega_cidade_por_id()

            if cidade_selecionada:
                novos_dados_cidade = self.__tela_cidade.pega_dados_cidade()

                if novos_dados_cidade is None:
                    return

                cidade_selecionada.nome = novos_dados_cidade["nome"]

                self.__cidade_DAO.update(cidade_selecionada)

                self.__tela_cidade.mostra_mensagem("Dados atualizados da cidade:")
                dados_atualizados = {
                    "id": cidade_selecionada.id,
                    "nome": cidade_selecionada.nome,
                    "pais_nome": cidade_selecionada.pais.nome
                }
                self.__tela_cidade.mostra_cidade(dados_atualizados)
        except OpcaoInvalidaException as e:
            self.__tela_cidade.mostra_mensagem(f"ERRO: {e}")

    def excluir_cidade(self):
        if not self.__cidade_DAO.get_all():
            self.__tela_cidade.mostra_mensagem("ATENÇÃO: Não há cidade cadastrada")
            return

        try:
            cidade_selecionada = self.pega_cidade_por_id()

            if cidade_selecionada:
                self.__cidade_DAO.remove(cidade_selecionada)
                self.__tela_cidade.mostra_mensagem(f"A cidade {cidade_selecionada.nome}, "
                                                f"ID #{cidade_selecionada.id} foi excluída com sucesso!")
        except OpcaoInvalidaException as e:
            self.__tela_cidade.mostra_mensagem(f"ERRO: {e}")

    def retornar(self):
        return

    def abre_tela(self):
        lista_opcoes = {1: self.incluir_cidade, 
                        2: self.listar_cidade,
                        3: self.alterar_cidade,
                        4: self.excluir_cidade,
                        0: self.retornar
                        }

        while True:
            try:
                opcao_escolhida = self.__tela_cidade.tela_opcoes()
                
                if opcao_escolhida == 0:
                    self.retornar()
                    break
                
                funcao_escolhida = lista_opcoes.get(opcao_escolhida)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    raise OpcaoInvalidaException("Opção de menu inválida.")
            except OpcaoInvalidaException as e:
                self.__tela_cidade.mostra_mensagem(f"\nERRO: {e}")
