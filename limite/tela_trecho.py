from datetime import date
from .tela_abstract import TelaAbstract


class TelaTrecho(TelaAbstract):

    def tela_opcoes(self) -> int:
        print("-------- GERENCIAMENTO DOS TRECHOS DA VIAGEM ----------")
        print('\n')
        print("[1] - Adicionar novo trecho")
        print("[2] - Listar todos os trechos")
        print("[3] - Alterar um trecho")
        print("[4] - Excluir um trecho")
        print("[0] - Voltar")
        print('\n')
        return self.le_num_inteiro_positivo("Escolha uma opção: ", [1, 2, 3, 4, 0])

    def pega_dados_trecho(self) -> dict:
        print("-------- DADOS DO TRECHO ----------")
        try:
            str_data_trecho = input("Data do trecho (AAAA-MM-DD): ")
            ano, mes, dia = map(int, str_data_trecho.split('-'))
            data_trecho = date(ano, mes, dia)
        except ValueError:
            self.mostra_mensagem("ERRO: Formato de data inválido. Use AAAA-MM-DD.")
            return None

        print('\n')
        return {"data": data_trecho}

    def mostra_trecho(self, dados_trecho):
        print(f"Data: #{dados_trecho['data'].strftime('%d/%m/%Y')}")
        print(f"Cidade origem: {dados_trecho['origem']}")
        print(f"Cidade destino: {dados_trecho['destino']}")
        print(f"Meio de Transporte: {dados_trecho['transporte']}")
        print(f"Empresa: {dados_trecho['empresa']}")
        print("\n")

    def seleciona_trecho(self):
        id_trecho = self.le_num_inteiro_positivo("Digite o ID do trecho que deseja selecionar: ")
        return id_trecho
