from datetime import date
from entidade.viagem import Viagem
from entidade.dia_de_viagem import DiaDeViagem
from limite.tela_viagem import TelaViagem
from exception.opcao_invalida_exception import OpcaoInvalidaException


class ControladorViagem:

    def __init__(self,
                 controlador_sistema,
                 controlador_participante,
                 controlador_passeio
                 ):
        self.__viagens: list[Viagem] = []
        self.__tela_viagem = TelaViagem()
        self.__controlador_sistema = controlador_sistema
        self.__controlador_participante = controlador_participante
        self.__controlador_passeio = controlador_passeio

    def gera_id(self):
        self.__id_atual += 1
        id_gerado = self.__id_atual
        return id_gerado

    def pega_viagem_por_id(self, id: int):
        for viagem in self.__viagens:
            if viagem.id == id:
                return viagem
        return None

    def incluir_viagem(self):
        dados_viagem = self.__tela_viagem.pega_dados_viagem()
        if not dados_viagem:
            return 

        novo_id = self.gera_id()
        nova_viagem = Viagem(novo_id, dados_viagem["nome"], dados_viagem["data_inicio"], dados_viagem["data_fim"])
        self.__viagens.append(nova_viagem)
        self.__tela_viagem.mostra_mensagem("Viagem criada com sucesso!")

    def listar_viagens(self):
        if not self.__viagens:
            self.__tela_viagem.mostra_mensagem("Nenhuma viagem cadastrada.")
            return

        for viagem in self.__viagens:
            self.__tela_viagem.mostra_viagem(str(viagem))   

    def gerenciar_viagem_selecionada(self, viagem: Viagem):
        lista_opcoes = {
            1: self.adicionar_participante_viagem,
            # 2: self.adicionar_passeio_viagem,
            # 3: self.adicionar_trecho_viagem,
            4: self.listar_detalhes_viagem,
        }

        while True:
            try:
                opcao = self.__tela_viagem.tela_opcoes_gerenciar(viagem.nome)
                if opcao == 0:
                    break

                funcao_escolhida = lista_opcoes.get(opcao)
                if funcao_escolhida:
                    funcao_escolhida(viagem)
                else:
                    raise OpcaoInvalidaException("Opção de menu inválida.")
            except OpcaoInvalidaException as e:
                self.__tela_viagem.mostra_mensagem(f"ERRO: {e}")

    def adicionar_participante_viagem(self, viagem: Viagem):
        self.__controlador_participante.listar_participantes()
        
        try:
            id_participante = self.__tela_viagem.seleciona_item("Digite o ID do participante a ser adicionado: ")
            participante = self.__controlador_participante.pega_participante_por_id(id_participante)

            if participante:
                data_inicio_viagem = viagem.data_inicio
                data_nascimento = participante.data_nascimento

                idade = (data_inicio_viagem.year - data_nascimento.year - 
                         ((data_inicio_viagem.month, data_inicio_viagem.day) < 
                          (data_nascimento.month, data_nascimento.day)))
                
                viagem.add_participante(participante)
                self.__tela_viagem.mostra_mensagem("Participante adicionado à viagem com sucesso!")
            else:
                self.__tela_viagem.mostra_mensagem("ATENÇÃO: Participante não encontrado.")
        except OpcaoInvalidaException as e:
            self.__tela_viagem.mostra_mensagem(f"ERRO: {e}")

    def listar_detalhes_viagem(self, viagem: Viagem):
        self.__tela_viagem.mostra_detalhes_viagem(viagem)

    def abre_tela(self):
        lista_opcoes = {
            1: self.incluir_viagem,
            2: self.listar_viagens,
        }
        while True:
            try:
                opcao = self.__tela_viagem.tela_opcoes_principal()
                if opcao == 0:
                    break
                
                if opcao == 3:
                    self.listar_viagens()
                    if self.__viagens:
                        id_viagem = self.__tela_viagem.seleciona_item("Digite o ID da viagem que deseja gerenciar: ")
                        viagem_selecionada = self.pega_viagem_por_id(id_viagem)
                        if viagem_selecionada:
                            self.gerenciar_viagem_selecionada(viagem_selecionada)
                        else:
                            self.__tela_viagem.mostra_mensagem("ATENÇÃO: Viagem não encontrada.")
                    continue

                funcao_escolhida = lista_opcoes.get(opcao)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    raise OpcaoInvalidaException("Opção de menu inválida.")
            
            except OpcaoInvalidaException as e:
                self.__tela_viagem.mostra_mensagem(f"ERRO: {e}")
