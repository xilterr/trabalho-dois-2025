from datetime import date
from .tela_abstract import TelaAbstract


class TelaTrecho(TelaAbstract):

    def tela_opcoes(self) -> int:
        print("\n" + "=" * 30)
        print("GESTÃO DE TRECHOS DA VIAGEM".center(30))
        print("=" * 30)
        print("[1] - Adicionar Novo Trecho")
        print("[2] - Listar Todos os Trechos")
        print("[3] - Alterar um Trecho")
        print("[4] - Excluir um Trecho")
        print("[5] - Definir Status da Compra")
        print("[6] - Definir Responsável pela Compra")
        print("[0] - Voltar")
        print("=" * 30)
        return self.le_num_inteiro("Escolha uma opção: ", [1, 2, 3, 4, 5, 6, 0])

    def pega_dados_trecho(self) -> dict:
        print("\n--- DADOS DO TRECHO ---")
        try:
            str_data = input("Data do Trecho (AAAA-MM-DD): ")
            ano, mes, dia = map(int, str_data.split('-'))
            data_viagem = date(ano, mes, dia)

            id_origem = self.le_num_inteiro_positivo("Digite o ID da Cidade de Origem: ")
            id_destino = self.le_num_inteiro_positivo("Digite o ID da Cidade de Destino: ")
            id_transporte = self.le_num_inteiro_positivo("Digite o ID do Transporte: ")
            valor = float(input("Valor do trecho (ex: 450.00): "))
            
            return {
                "data_viagem": data_viagem,
                "id_origem": id_origem,
                "id_destino": id_destino,
                "id_transporte": id_transporte,
                "valor": valor
            }
        except (ValueError, TypeError):
            self.mostra_mensagem("ERRO: Formato de dados inválido.")
            return None

    def mostra_lista_trechos(self, trechos: list):
        print("\n--- Lista de Trechos Cadastrados ---")
        if not trechos:
            self.mostra_mensagem("Nenhum trecho cadastrado.")
        else:
            for trecho in trechos:
                print(trecho)

    def seleciona_trecho(self) -> int:
        return self.le_num_inteiro_positivo("Digite o ID do trecho que deseja selecionar: ")

    def pega_status_compra(self) -> bool:
        while True:
            resposta = input("A compra já foi efetuada? (S/N): ").upper()
            if resposta == 'S':
                return True
            elif resposta == 'N':
                return False
            else:
                self.mostra_mensagem("Resposta inválida. Digite 'S' para Sim ou 'N' para Não.")
