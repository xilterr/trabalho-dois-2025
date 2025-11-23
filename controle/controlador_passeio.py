from entidade.passeio import Passeio
from entidade.cidade import Cidade
from entidade.pais import Pais
from limite.tela_passeio import TelaPasseio
from exception.opcao_invalida_exception import OpcaoInvalidaException
from exception.dado_em_branco_exception import DadoEmBrancoException
from DAO.passeio_dao import PasseioDAO
from controle.controlador_cidade import ControladorCidade
from controle.controlador_participante import ControladorParticipante


class ControladorPasseio:

    def __init__(self, controlador_sistema, controlador_cidade: ControladorCidade, controlador_participante: ControladorParticipante):
        self.__tela_passeio = TelaPasseio()
        self.__controlador_sistema = controlador_sistema
        self.__controlador_cidade = controlador_cidade
        self.__controlador_participante = controlador_participante
        self.__passeio_DAO = PasseioDAO()

    def gera_id(self):
        lista_passeios = self.__passeio_DAO.get_all()

        if not lista_passeios:
            return 1

        maior_id = 1 + max([p.id for p in lista_passeios])
        return maior_id

    def pega_passeio_por_id(self):
        self.listar_passeios()
        id_selecionado = self.__tela_passeio.seleciona_passeio()

        if not self.__passeio_DAO.get_all():
            return None

        for passeio in self.__passeio_DAO.get_all():
            if passeio.id == id_selecionado:
                return passeio

        self.__tela_passeio.mostra_mensagem("ATENÇÃO: Passeio com este ID não foi encontrado.")
        return None

    def incluir_passeio(self):
        dados_passeio = self.__tela_passeio.pega_dados_passeio()

        cidade = self.__controlador_cidade.pega_cidade_por_id()
        pais = cidade.pais.nome

        if dados_passeio is None:
            return

        try:
            if (not dados_passeio["atracao"] or 
                not dados_passeio["horario_inicio"] or 
                not dados_passeio["horario_fim"] or
                not dados_passeio["valor"]):
                    raise DadoEmBrancoException()

            novo_id = self.gera_id()
            novo_passeio = Passeio(
                novo_id,
                dados_passeio["atracao"],
                cidade,
                dados_passeio["horario_inicio"],
                dados_passeio["horario_fim"],
                dados_passeio["valor"],
                )
            
            self.__passeio_DAO.add(novo_passeio)
            self.__tela_passeio.mostra_mensagem(f"O passeio {novo_passeio.atracao} foi cadastrado com sucesso!")

        except DadoEmBrancoException as e:
            self.__tela_passeio.mostra_mensagem(f"ERRO: {e}")

    def listar_passeios(self):
        if not self.__passeio_DAO.get_all():
            self.__tela_passeio.mostra_mensagem("ATENÇÃO: Não há passeios cadastrados")
            return
        else:
            self.__tela_passeio.mostra_mensagem('-------- LISTAGEM DOS PASSEIOS ----------')

            for passeio in self.__passeio_DAO.get_all():
                dados_para_mostrar = {
                    "id": passeio.id,
                    "atracao": passeio.atracao,
                    "cidade": passeio.cidade.nome,
                    "pais": passeio.cidade.pais.nome,
                    "horario_inicio": passeio.horario_inicio,
                    "horario_fim": passeio.horario_fim,
                    "valor": passeio.valor,
                }
                self.__tela_passeio.mostra_passeio(dados_para_mostrar)

    def alterar_passeio(self):
        if not self.__passeio_DAO.get_all():
            self.__tela_passeio.mostra_mensagem("ATENÇÃO: Não há passeios cadastrados.")
            return

        try:
            passeio_selecionado = self.pega_passeio_por_id()

            if passeio_selecionado:
                novos_dados = self.__tela_passeio.pega_dados_passeio()

                if novos_dados is None:
                    return

                passeio_selecionado.atracao = novos_dados["atracao"] 
                passeio_selecionado.horario_inicio = novos_dados["horario_inicio"]
                passeio_selecionado.horario_fim = novos_dados["horario_fim"]
                passeio_selecionado.valor = novos_dados["valor"]

                self.__passeio_DAO.update(passeio_selecionado)

                self.__tela_passeio.mostra_mensagem("Dados do passeio atualizados:")
                
                dados_atualizados = {
                    "id": passeio_selecionado.id,
                    "atracao": passeio_selecionado.atracao,
                    "cidade": passeio_selecionado.cidade.nome,
                    "pais": passeio_selecionado.cidade.pais.nome,
                    "horario_inicio": passeio_selecionado.horario_inicio,
                    "horario_fim": passeio_selecionado.horario_fim,
                    "valor": passeio_selecionado.valor
                }
                self.__tela_passeio.mostra_passeio(dados_atualizados)

        except OpcaoInvalidaException as e:
            self.__tela_passeio.mostra_mensagem(f"ERRO: {e}")

    def excluir_passeio(self):
        if not self.__passeio_DAO.get_all():
            self.__tela_passeio.mostra_mensagem("ATENÇÃO: Não há passeios cadastrados")
            return

        try:
            passeio_selecionado = self.pega_passeio_por_id()

            if passeio_selecionado:
                self.__passeio_DAO.remove(passeio_selecionado.id)
                self.__tela_passeio.mostra_mensagem(f"O passeio '{passeio_selecionado.atracao}', "
                                                    f"ID #{passeio_selecionado.id} foi excluído com sucesso!")
        except OpcaoInvalidaException as e:
            self.__tela_passeio.mostra_mensagem(f"ERRO: {e}")

    def adicionar_participante(self):
        if not self.__passeio_DAO.get_all():
            self.__tela_passeio.mostra_mensagem("ATENÇÃO: Não há passeios cadastrados.")
            return

        passeio_selecionado = self.pega_passeio_por_id()
        if not passeio_selecionado:
            return

        participante_selecionado = self.__controlador_participante.pega_participante_por_id()
        
        if not participante_selecionado:
            return

        if participante_selecionado in passeio_selecionado.participantes:
            self.__tela_passeio.mostra_mensagem("ERRO: Este participante já está neste passeio.")
            return

        passeio_selecionado.participantes.append(participante_selecionado)

        try:
            self.__passeio_DAO.update(passeio_selecionado)
            self.__tela_passeio.mostra_mensagem(f"Sucesso! {participante_selecionado.nome} adicionado ao passeio '{passeio_selecionado.atracao}'.")
        except Exception as e:
            self.__tela_passeio.mostra_mensagem(f"ERRO ao salvar: {e}")

    def remover_participante(self):
        passeio_selecionado = self.listar_participantes()

        id_participante = self.__tela_passeio.le_num_inteiro_positivo("Digite o ID do participante que deseja remover: ")

        participante_para_remover = None
        for p in passeio_selecionado.participantes:
            if p.id == id_participante:
                participante_para_remover = p
                break

        if participante_para_remover:
            try:
                passeio_selecionado.participantes.remove(participante_para_remover)
                self.__passeio_DAO.update(passeio_selecionado)
                self.__tela_passeio.mostra_mensagem(f"Sucesso! {participante_para_remover.nome} removido do passeio.")
            except Exception as e:
                self.__tela_passeio.mostra_mensagem(f"ERRO ao salvar: {e}")
        else:
            self.__tela_passeio.mostra_mensagem("ERRO: Participante com este ID não está na lista deste passeio.")

    def listar_participantes(self):
        if not self.__passeio_DAO.get_all():
            self.__tela_passeio.mostra_mensagem("ATENÇÃO: Não há passeios cadastrados.")
            return

        passeio_selecionado = self.pega_passeio_por_id()
        if not passeio_selecionado:
            return

        if not passeio_selecionado.participantes:
            self.__tela_passeio.mostra_mensagem("ERRO: Não há participantes cadastrados neste passeio.")
            return

        for participante in passeio_selecionado.participantes:
            dados_para_mostrar = {
                "id": participante.id,
                "nome": participante.nome,
                "telefone": participante.telefone,
                "data_nascimento": participante.data_nascimento,
                "cpf_passaporte": participante.cpf_passaporte,
            }

        self.__controlador_participante.tela_participante.mostra_participante(dados_para_mostrar)

        return passeio_selecionado

    def retornar(self):
        return

    def abre_tela(self):
        lista_opcoes = {1: self.incluir_passeio,
                        2: self.listar_passeios,
                        3: self.alterar_passeio,
                        4: self.excluir_passeio
                        }

        while True:
            try:
                opcao_escolhida = self.__tela_passeio.tela_opcoes()
                
                if opcao_escolhida == 0:
                    self.retornar()
                    break
                
                funcao_escolhida = lista_opcoes.get(opcao_escolhida)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    raise OpcaoInvalidaException("Opção de menu inválida.")
            except OpcaoInvalidaException as e:
                self.__tela_passeio.mostra_mensagem(f"\nERRO: {e}")
