from datetime import datetime
from limite.tela_abstract import TelaAbstract


class TelaPasseio(TelaAbstract):

    def tela_opcoes(self) -> int:
        print("-------- GERENCIAMENTO DOS PASSEIOS ----------")
        print('\n')
        print("[1] - Adicionar novo Passeio")
        print("[2] - Listar todos os Passeios")
        print("[3] - Alterar dados de um Passeio")
        print("[4] - Excluir um Passeio")
        print("[0] - Voltar ao Menu Principal")
        print('\n')

        opcao = self.le_num_inteiro_positivo("Escolha a opção: ", [1, 2, 3, 4, 0])
        return opcao

    def pega_dados_passeio(self) -> dict:
        print("-------- DADOS DO PASSEIO ----------")
        atracao = input("Atração turística principal: ")
        valor = self.le_num_float_positivo("Valor do passeio: ")

        try:
            str_inicio = input("Horário de Início (HH:MM): ")
            horario_inicio = datetime.strptime(str_inicio, '%H:%M').time()
            
            str_fim = input("Horário de Fim (AAAA-MM-DD HH:MM): ")
            horario_fim = datetime.strptime(str_fim, '%H:%M').time()
        except ValueError:
            self.mostra_mensagem("ERRO: Formato de data/hora ou valor inválido.")
            return None

        return {
            "atracao": atracao,
            "horario_inicio": horario_inicio,
            "horario_fim": horario_fim,
            "valor": valor
            }

    def mostra_passeio(self, dados_passeio):
        print(f"ID: #{dados_passeio['id']}")
        print(f"Atração Principal: {dados_passeio['atracao']}")
        print(f"Cidade: {dados_passeio['cidade']}")
        print(f"País: {dados_passeio['pais']}")
        print(f"Horário de Início: {dados_passeio['horario_inicio']}")
        print(f"Horário de Fim: {dados_passeio['horario_fim']}")
        print(f"Valor por Pessoa: R${dados_passeio['valor']}")
        print("\n")

    def seleciona_passeio(self):
        return self.le_num_inteiro_positivo("Digite o ID do passeio que deseja selecionar: ")
