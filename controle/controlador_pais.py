from entidade.pais import Pais
from limite.tela_pais import TelaPais
from exception.opcao_invalida_exception import OpcaoInvalidaException
from exception.dado_em_branco_exception import DadoEmBrancoException
from exception.pais_repetido_exception import PaisRepetidoException
from DAO.pais_dao import PaisDAO


class ControladorPais:

    def __init__(self, controlador_sistema):
        self.__tela_pais = TelaPais()
        self.__controlador_sistema = controlador_sistema
        self.__pais_DAO = PaisDAO()

    def gera_id(self):
        lista_paises = self.__pais_DAO.get_all()

        if not lista_paises:
            return 1

        maior_id = 1 + max([p.id for p in lista_paises])
        return maior_id

    def pega_pais_por_id(self):
        self.listar_pais()
        id_selecionado = self.__tela_pais.seleciona_pais()

        if not self.__pais_DAO.get_all():
            return None

        for pais in self.__pais_DAO.get_all():
            if pais.id == id_selecionado:
                return pais

        self.__tela_pais.mostra_mensagem("ATENÇÃO: país com este ID não foi encontrado.")
        return None

    def incluir_pais(self): 
        dados_pais = self.__tela_pais.pega_dados_pais()

        if dados_pais is None:
            return

        try:
            if not dados_pais["nome"]:
                raise DadoEmBrancoException()

            for pais in self.__pais_DAO.get_all():
                if pais.nome == dados_pais["nome"]:
                    raise PaisRepetidoException(dados_pais["nome"])

            novo_id = self.gera_id()
            novo_pais = Pais(
                novo_id,
                dados_pais["nome"],
                )
            
            self.__pais_DAO.add(novo_pais)
            self.__tela_pais.mostra_mensagem(f"O país {novo_pais.nome} foi cadastrado com sucesso!")

        except (PaisRepetidoException, DadoEmBrancoException) as e:
            self.__tela_pais.mostra_mensagem(f"ERRO: {e}")

    def listar_pais(self):
        if not self.__pais_DAO.get_all():
            self.__tela_pais.mostra_mensagem("ATENÇÃO: Não há país cadastrado")
            return
        else:
            self.__tela_pais.mostra_mensagem('-------- LISTAGEM DOS PAÍSES ----------')

            for pais in self.__pais_DAO.get_all():
                dados_para_mostrar = {
                    "id": pais.id,
                    "nome": pais.nome
                    }
                self.__tela_pais.mostra_pais(dados_para_mostrar)

    def alterar_pais(self):
        if not self.__pais_DAO.get_all():
            self.__tela_pais.mostra_mensagem("ATENÇÃO: Não há país cadastrado.")
            return

        try:
            pais_selecionado = self.pega_pais_por_id()

            if pais_selecionado:
                novos_dados_pais = self.__tela_pais.pega_dados_pais()

                if novos_dados_pais is None:
                    return

                pais_selecionado.nome = novos_dados_pais["nome"]

                self.__pais_DAO.update(pais_selecionado)

                self.__tela_pais.mostra_mensagem("Dados atualizados do país:")
                dados_atualizados = {
                    "id": pais_selecionado.id,
                    "nome": pais_selecionado.nome,
                }
                self.__tela_pais.mostra_pais(dados_atualizados)
        except OpcaoInvalidaException as e:
            self.__tela_pais.mostra_mensagem(f"ERRO: {e}")

    def excluir_pais(self):
        if not self.__pais_DAO.get_all():
            self.__tela_pais.mostra_mensagem("ATENÇÃO: Não há país cadastrado")
            return

        try:
            pais_selecionado = self.pega_pais_por_id()

            if pais_selecionado:
                self.__pais_DAO.remove(pais_selecionado.id)
                self.__tela_pais.mostra_mensagem(f"O país {pais_selecionado.nome}, "
                                                f"ID #{pais_selecionado.id} foi excluído com sucesso!")
        except OpcaoInvalidaException as e:
            self.__tela_pais.mostra_mensagem(f"ERRO: {e}")

    def retornar(self):
        return

    def abre_tela(self):
        lista_opcoes = {1: self.incluir_pais, 
                        2: self.listar_pais,
                        3: self.alterar_pais,
                        4: self.excluir_pais,
                        0: self.retornar
                        }

        while True:
            try:
                opcao_escolhida = self.__tela_pais.tela_opcoes()
                
                if opcao_escolhida == 0:
                    self.retornar()
                    break
                
                funcao_escolhida = lista_opcoes.get(opcao_escolhida)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    raise OpcaoInvalidaException("Opção de menu inválida.")
            except OpcaoInvalidaException as e:
                self.__tela_pais.mostra_mensagem(f"\nERRO: {e}")
