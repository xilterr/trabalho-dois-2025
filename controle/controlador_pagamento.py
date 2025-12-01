from entidade.pagamento import Pagamento
from entidade.metodo_pagamento import MetodoPagamento
from limite.tela_pagamento import TelaPagamento
from exception.opcao_invalida_exception import OpcaoInvalidaException
from exception.dado_em_branco_exception import DadoEmBrancoException
from controle.controlador_viagem import ControladorViagem
from controle.controlador_participante import ControladorParticipante


class ControladorPagamento:

    def __init__(self, controlador_sistema,
                 controlador_viagem: ControladorViagem,
                 controlador_participante: ControladorParticipante
                 ):
        self.__tela_pagamento = TelaPagamento()
        self.__controlador_sistema = controlador_sistema
        self.__controlador_viagem = controlador_viagem
        self.__controlador_participante = controlador_participante

    def gera_id(self, lista_pagamentos):
        if not lista_pagamentos:
            return 1
        
        maior_id = 1 + max([p.id for p in lista_pagamentos])
        return maior_id

    def pega_passagem_na_viagem(self, viagem):
        if not viagem.passagens:
            self.__tela_pagamento.mostra_mensagem("ATENÇÃO: Esta viagem não possui passagens cadastradas.")
            return None

        for pas in viagem.passagens:
            pagante = pas.participante_pagante.nome
            if pas.participante_pagante else "Sem Pagante"
            print(f"ID: {pas.id} | Pagante da Passagem: {pagante} | Valor Total: {pas.valor_total}")
        
        id_selecionado = self.__tela_pagamento.seleciona_passagem_id()

        for passagem in viagem.passagens:
            if passagem.id == id_selecionado:
                return passagem

        self.__tela_pagamento.mostra_mensagem("ATENÇÃO: Passagem com este ID não encontrada na viagem.")
        return None

    def pega_pagamento_na_passagem(self, passagem):
        self.listar_pagamentos_da_passagem(passagem)
        
        if not passagem.pagamentos:
            return None

        id_selecionado = self.__tela_pagamento.seleciona_pagamento()

        for pagamento in passagem.pagamentos:
            if pagamento.id == id_selecionado:
                return pagamento

        self.__tela_pagamento.mostra_mensagem("ATENÇÃO: Pagamento com este ID não foi encontrado.")
        return None

    def incluir_pagamento(self):
        # 1. Seleciona Viagem
        viagem_selecionada = self.__controlador_viagem.busca_viagem_por_id()
        if viagem_selecionada is None:
            return

        # 2. Seleciona Passagem dentro da Viagem
        passagem_selecionada = self.pega_passagem_na_viagem(viagem_selecionada)
        if passagem_selecionada is None:
            return

        # 3. Seleciona Pagante
        pagante_selecionado = self.__controlador_participante.busca_participante_por_id()
        if pagante_selecionado is None:
            return

        # 4. Coleta Dados
        dados_pagamento = self.__tela_pagamento.pega_dados_pagamento()
        if dados_pagamento is None:
            return

        try:
            # Validação simples (exemplo)
            if dados_pagamento["valor_pago"] <= 0:
                raise OpcaoInvalidaException("O valor do pagamento deve ser positivo.")

            novo_id = self.gera_id(passagem_selecionada.pagamentos)

            novo_pagamento = Pagamento(
                id=novo_id,
                modalidade=dados_pagamento["modalidade"],
                data=dados_pagamento["data"],
                viagem=viagem_selecionada,
                pessoa_pagante=pagante_selecionado,
                valor_pago=dados_pagamento["valor_pago"]
            )

            passagem_selecionada.pagamentos.append(novo_pagamento)
            
            # Persistência via ControladorViagem (Aggregate Root)
            self.__controlador_viagem.salvar_viagem(viagem_selecionada)
            
            self.__tela_pagamento.mostra_mensagem("Pagamento realizado com sucesso!")

        except OpcaoInvalidaException as e:
            self.__tela_pagamento.mostra_mensagem(f"ERRO: {e}")

    def listar_pagamentos(self):
        # Wrapper para o menu principal que exige seleção prévia
        viagem_selecionada = self.__controlador_viagem.busca_viagem_por_id()
        if viagem_selecionada is None:
            return
        
        passagem_selecionada = self.pega_passagem_na_viagem(viagem_selecionada)
        if passagem_selecionada is None:
            return

        self.listar_pagamentos_da_passagem(passagem_selecionada)

    def listar_pagamentos_da_passagem(self, passagem):
        # Método auxiliar que recebe o objeto direto
        if not passagem.pagamentos:
            self.__tela_pagamento.mostra_mensagem("ATENÇÃO: Não existem pagamentos nesta passagem.")
            return
        
        self.__tela_pagamento.mostra_mensagem('-------- LISTAGEM DOS PAGAMENTOS ----------')

        for pagamento in passagem.pagamentos:
            dados_para_mostrar = {
                "id": pagamento.id,
                "viagem_titulo": pagamento.viagem.titulo, # Ajuste conforme atributo real de Viagem
                "pagante_nome": pagamento.pessoa_pagante.nome,
                "data": pagamento.data,
                "valor_pago": pagamento.valor_pago,
                "modalidade": pagamento.modalidade.name
            }
            self.__tela_pagamento.mostra_pagamento(dados_para_mostrar)

    def excluir_pagamento(self):
        viagem_selecionada = self.__controlador_viagem.busca_viagem_por_id()
        if viagem_selecionada is None:
            return

        passagem_selecionada = self.pega_passagem_na_viagem(viagem_selecionada)
        if passagem_selecionada is None:
            return

        if not passagem_selecionada.pagamentos:
            self.__tela_pagamento.mostra_mensagem("ATENÇÃO: Não existem pagamentos para excluir.")
            return

        try:
            pagamento = self.pega_pagamento_na_passagem(passagem_selecionada)

            if pagamento:
                passagem_selecionada.pagamentos.remove(pagamento)
                
                # Atualiza arquivo
                self.__controlador_viagem.salvar_viagem(viagem_selecionada)
                
                self.__tela_pagamento.mostra_mensagem(f"Pagamento ID #{pagamento.id} removido com sucesso!")
            
        except OpcaoInvalidaException as e:
            self.__tela_pagamento.mostra_mensagem(f"ERRO: {e}")

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
            1: self.incluir_pagamento,
            2: self.listar_pagamentos,
            3: self.excluir_pagamento,
        }

        while True:
            try:
                opcao_escolhida = self.__tela_pagamento.tela_opcoes()
                
                if opcao_escolhida == 0:
                    self.retornar()
                    break

                funcao_escolhida = lista_opcoes.get(opcao_escolhida)
                
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    raise OpcaoInvalidaException("Opção de menu inválida.")
            
            except OpcaoInvalidaException as e:
                self.__tela_pagamento.mostra_mensagem(f"ERRO: {e}")
