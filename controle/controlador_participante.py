from entidade.participante import Participante
from entidade.cartao_credito import CartaoCredito
from limite.tela_participante import TelaParticipante
from exception.opcao_invalida_exception import OpcaoInvalidaException
from exception.participante_repetido_exception import ParticipanteRepetidoException
from exception.dado_em_branco_exception import DadoEmBrancoException
from exception.cartao_repetido_exception import CartaoRepetidoException
from exception.cartao_inexistente_exception import CartaoInexistenteException
from DAO.participante_dao import ParticipanteDAO


class ControladorParticipante:

    def __init__(self, controlador_sistema):
        self.__tela_participante = TelaParticipante()
        self.__controlador_sistema = controlador_sistema
        self.__participante_DAO = ParticipanteDAO()

    @property
    def tela_participante(self):
        return self.__tela_participante

    def gera_id(self):
        lista_participantes = self.__participante_DAO.get_all()

        if not lista_participantes:
            return 1

        maior_id = 1 + max([p.id for p in lista_participantes])
        return maior_id

    def gera_id_cartao(self, participante):
        if not participante.cartoes:
            return 1
        return max([c.id for c in participante.cartoes]) + 1

    def pega_participante_por_id(self):
        dados_lista = []
        for p in self.__participante_DAO.get_all():
            dados_lista.append({
                "id": p.id,
                "nome": p.nome,
                "telefone": p.telefone,
                "data_nascimento": p.data_nascimento,
                "cpf_passaporte": p.cpf_passaporte
            })

        id_selecionado = self.__tela_participante.seleciona_participante(dados_lista)

        if id_selecionado is None:
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
        dados_lista = []
        for p in self.__participante_DAO.get_all():
            dados_lista.append({
                "id": p.id,
                "nome": p.nome,
                "telefone": p.telefone,
                "data_nascimento": p.data_nascimento,
                "cpf_passaporte": p.cpf_passaporte
            })
            
        self.__tela_participante.seleciona_participante(dados_lista)

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

    def adicionar_cartao(self):
        self.__tela_participante.mostra_mensagem("\n--- ADICIONAR CARTÃO DE CRÉDITO ---")
        participante = self.pega_participante_por_id()
        if not participante:
            return

        dados_cartao = self.__tela_participante.pega_dados_cartao()
        if not dados_cartao:
            return

        try:
            if not dados_cartao["numero"] or not dados_cartao["bandeira"]:
                raise DadoEmBrancoException()

            for cartao in participante.cartoes:
                if (str(cartao.numero) == str(dados_cartao["numero"]) and 
                    cartao.bandeira.lower() == dados_cartao["bandeira"].lower()):
                    raise CartaoRepetidoException()

            novo_id_cartao = self.gera_id_cartao(participante)
            novo_cartao = CartaoCredito(
                novo_id_cartao,
                dados_cartao["numero"],
                dados_cartao["bandeira"]
            )

            participante.cartoes.append(novo_cartao)
            self.__participante_DAO.update(participante)
            self.__tela_participante.mostra_mensagem("Cartão adicionado com sucesso!")

        except (DadoEmBrancoException, CartaoRepetidoException) as e:
            self.__tela_participante.mostra_mensagem(f"ERRO: {e}")

    def listar_cartoes(self):
        print("\n--- LISTAR CARTÕES ---")
        participante = self.pega_participante_por_id()
        if not participante:
            return

        if not participante.cartoes:
            self.__tela_participante.mostra_mensagem("Este participante não possui cartões cadastrados.")
            return

        for cartao in participante.cartoes:
            dados_cartao = {
                "id": cartao.id,
                "numero": cartao.numero,
                "bandeira": cartao.bandeira
            }
            self.__tela_participante.mostra_cartao(dados_cartao)

    def excluir_cartao(self, participante):
        participante = self.pega_participante_por_id()
        if not participante:
            return

        if not participante.cartoes:
            self.__tela_participante.mostra_mensagem("Este participante não possui cartões para excluir.")
            return

        for cartao in participante.cartoes:
            dados = {"id": cartao.id,
                     "numero": cartao.numero,
                     "bandeira": cartao.bandeira
                     }
            self.__tela_participante.mostra_cartao(dados)

        id_cartao = self.__tela_participante.seleciona_cartao()

        try:
            cartao_para_remover = None
            
            for cartao in participante.cartoes:
                if cartao.id == id_cartao:
                    cartao_para_remover = cartao
                    break
            
            if cartao_para_remover:
                participante.cartoes.remove(cartao_para_remover)
                self.__participante_DAO.update(participante)
                self.__tela_participante.mostra_mensagem("Cartão removido com sucesso!")
            else:
                raise CartaoInexistenteException()

        except CartaoInexistenteException as e:
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
