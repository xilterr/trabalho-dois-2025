from datetime import datetime
from limite.tela_abstract import TelaAbstract
from entidade.metodo_pagamento import MetodoPagamento

class TelaPagamento(TelaAbstract):

    def tela_opcoes(self) -> int:
        print("\n-------- GERENCIAMENTO DE PAGAMENTOS ----------")
        print("[1] - Incluir Novo Pagamento")
        print("[2] - Listar Pagamentos de uma Passagem")
        print("[3] - Excluir Pagamento")
        print("[0] - Retornar")
        
        opcao = self.le_num_inteiro_positivo("Escolha a opção: ", [1, 2, 3, 0])
        return opcao

    def pega_dados_pagamento(self) -> dict:
        print("\n-------- DADOS DO PAGAMENTO ----------")
        
        try:
            str_data = input("Data do Pagamento (DD/MM/AAAA): ")
            data = datetime.strptime(str_data, '%d/%m/%Y').date()
        except ValueError:
            self.mostra_mensagem("ERRO: Formato de data inválido. Use DD/MM/AAAA.")
            return None

        valor_pago = self.le_num_float_positivo("Valor Pago (R$): ")

        print("--- Modalidade ---")
        print("[1] - DINHEIRO")
        print("[2] - PIX")
        print("[3] - CREDITO")
        print("[4] - BOLETO")
        
        opcao_modalidade = self.le_num_inteiro_positivo("Escolha a modalidade: ", [1, 2, 3, 4])
        
        mapa_modalidade = {
            1: MetodoPagamento.DINHEIRO,
            2: MetodoPagamento.PIX,
            3: MetodoPagamento.CREDITO,
        }

        return {
            "data": data,
            "valor_pago": valor_pago,
            "modalidade": mapa_modalidade[opcao_modalidade]
        }

    def mostra_pagamento(self, dados_pagamento: dict):
        print("--------------------------------------")
        print(f"ID: {dados_pagamento['id']}")
        print(f"Pagante: {dados_pagamento['pagante_nome']}")
        print(f"Data: {dados_pagamento['data'].strftime('%d/%m/%Y')}")
        print(f"Valor: R$ {dados_pagamento['valor_pago']:.2f}")
        print(f"Modalidade: {dados_pagamento['modalidade'].name}") 
        print("--------------------------------------")

    def seleciona_pagamento(self) -> int:
        return self.le_num_inteiro_positivo("Digite o ID do pagamento: ")
    
    def seleciona_passagem_id(self) -> int:
        return self.le_num_inteiro_positivo("Digite o ID da Passagem que deseja gerenciar: ")