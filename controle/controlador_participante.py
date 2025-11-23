from entidade.participante import Participante
from limite.tela_participante import TelaParticipante
from exception.opcao_invalida_exception import OpcaoInvalidaException
from exception.participante_repetido_exception import ParticipanteRepetidoException
from exception.dado_em_branco_exception import DadoEmBrancoException
from DAO.participante_dao import ParticipanteDAO

class ControladorParticipante:

    def __init__(self, controlador_sistema):
        self.__tela_participante = TelaParticipante()
        self.__controlador_sistema = controlador_sistema
        self.__id_atual = 0
        self.__participante_DAO = ParticipanteDAO()

    def gera_id(self):
        lista_participantes = self.__participante_DAO.get_all()

        if not lista_participantes:
            return 1

        maior_id = 1 + max([p.id for p in lista_participantes])
        return maior_id

    def pega_participante_por_id(self):
        self.listar_participantes()
        id_selecionado = self.__tela_participante.seleciona_participante()

        if not self.__participante_DAO.get_all():
            return None

        for participante in self.__participante_DAO.get_all():
            if participante.id == id_selecionado:
                return participante

        self.__tela_participante.mostra_mensagem("ATENÇÃO: Participante com este ID não foi encontrado.")
        return None

    def incluir_participante(self): 
        dados_participante = self.__tela_participante.pega_dados_participante()

        if dados_participante is None:
            return

        try:
            if (not dados_participante["nome"] or 
                not dados_participante["cpf_passaporte"] or 
                not dados_participante["telefone"] or
                not dados_participante["data_nascimento"]):
                    raise DadoEmBrancoException()

            for participante in self.__participante_DAO.get_all():
                if participante.cpf_passaporte == dados_participante["cpf_passaporte"]:
                    raise ParticipanteRepetidoException(dados_participante["cpf_passaporte"])

            novo_id = self.gera_id()
            novo_participante = Participante(
                novo_id,
                dados_participante["nome"],
                dados_participante["telefone"],
                dados_participante["cpf_passaporte"],
                dados_participante["data_nascimento"]
            )
            
            self.__participante_DAO.add(novo_participante)
            self.__tela_participante.mostra_mensagem(f"O participante {novo_participante.nome} foi cadastrado com sucesso!")

        except (ParticipanteRepetidoException, DadoEmBrancoException) as e:
            self.__tela_participante.mostra_mensagem(f"ERRO: {e}")

    def listar_participantes(self):
        if not self.__participante_DAO.get_all():
            self.__tela_participante.mostra_mensagem("ATENÇÃO: Não há participantes cadastrados")
            return
        else:
            self.__tela_participante.mostra_mensagem('-------- LISTAGEM DOS PARTICIPANTES ----------')

            for participante in self.__participante_DAO.get_all():
                dados_para_mostrar = {
                    "id": participante.id,
                    "nome": participante.nome,
                    "telefone": participante.telefone,
                    "data_nascimento": participante.data_nascimento,
                    "cpf_passaporte": participante.cpf_passaporte,
                }
                self.__tela_participante.mostra_participante(dados_para_mostrar)

    def alterar_participante(self):
        if not self.__participante_DAO.get_all():
            self.__tela_participante.mostra_mensagem("ATENÇÃO: Não há participantes cadastrados")
            return

        try:
            participante_selecionado = self.pega_participante_por_id()

            if participante_selecionado:
                novos_dados_participante = self.__tela_participante.pega_dados_participante()

                if novos_dados_participante is None:
                    return

                participante_selecionado.nome = novos_dados_participante["nome"]
                participante_selecionado.telefone = novos_dados_participante["telefone"]
                participante_selecionado.data_nascimento = novos_dados_participante["data_nascimento"]
                participante_selecionado.cpf_passaporte = novos_dados_participante["cpf_passaporte"]

                self.__participante_DAO.update(participante_selecionado)

                self.__tela_participante.mostra_mensagem("Dados atualizados do participante:")
                dados_atualizados = {
                    "id": participante_selecionado.id,
                    "nome": participante_selecionado.nome,
                    "telefone": participante_selecionado.telefone,
                    "data_nascimento": participante_selecionado.data_nascimento,
                    "cpf_passaporte": participante_selecionado.cpf_passaporte,
                }
                self.__tela_participante.mostra_participante(dados_atualizados)
        except OpcaoInvalidaException as e:
            self.__tela_participante.mostra_mensagem(f"ERRO: {e}")

    def excluir_participante(self):
        if not self.__participante_DAO.get_all():
            self.__tela_participante.mostra_mensagem("ATENÇÃO: Não há participantes cadastrados")
            return

        try:
            participante_selecionado = self.pega_participante_por_id()

            if participante_selecionado:
                self.__participante_DAO.remove(participante_selecionado.id)
                self.__tela_participante.mostra_mensagem(f"O participante {participante_selecionado.nome}, "
                                                        f"ID #{participante_selecionado.id} foi excluído com sucesso!")
        except OpcaoInvalidaException as e:
            self.__tela_participante.mostra_mensagem(f"ERRO: {e}")

    def retornar(self):
        return

    def abre_tela(self):
        lista_opcoes = {1: self.incluir_participante, 
                        2: self.listar_participantes,
                        3: self.alterar_participante,
                        4: self.excluir_participante,
                        0: self.retornar
                        }

        while True:
            try:
                opcao_escolhida = self.__tela_participante.tela_opcoes()
                
                if opcao_escolhida == 0:
                    self.retornar()
                    break
                
                funcao_escolhida = lista_opcoes.get(opcao_escolhida)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    raise OpcaoInvalidaException("Opção de menu inválida.")
            except OpcaoInvalidaException as e:
                self.__tela_participante.mostra_mensagem(f"\nERRO: {e}")
