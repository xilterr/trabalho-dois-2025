from limite.tela_abstract import TelaAbstract 
from datetime import date


class TelaParticipante(TelaAbstract):

    def tela_opcoes(self):
        print("-------- GERENCIAMENTO DOS PARTICIPANTES ----------")
        print('\n')
        print("[1] - Adicionar novo Participante")
        print("[2] - Listar todos os Participantes")
        print("[3] - Alterar dados de um Participante")
        print("[4] - Excluir um Participante")
        print("[0] - Voltar ao Menu Principal")
        print('\n')

        opcao = self.le_num_inteiro_positivo("Escolha a opção: ", [1, 2, 3, 4, 0])
        return opcao

    def pega_dados_participante(self):
        print("-------- DADOS DO PARTICIPANTE ----------")
        nome = input("Nome: ")
        telefone = self.le_num_inteiro_positivo("Telefone: ")
        try:
            str_data_nasc = input("Data de Nascimento (AAAA-MM-DD): ")
            ano, mes, dia = map(int, str_data_nasc.split('-'))
            data_nascimento = date(ano, mes, dia)
        except ValueError:
            self.mostra_mensagem("ERRO: Formato de data inválido. Use AAAA-MM-DD.")
            return None

        cpf_passaporte = input("CPF ou passaporte: ")
        print('\n')

        return {"nome": nome,
                "telefone": telefone,
                "data_nascimento": data_nascimento,
                "cpf_passaporte": cpf_passaporte,
                }

    def mostra_participante(self, dados_participante):
        print(f"ID do participante: #{dados_participante['id']}")
        print(f"Nome do participante: {dados_participante['nome']}")
        print(f"Telefone do participante: {dados_participante['telefone']}")
        print(f"Data de Nascimento: {dados_participante['data_nascimento'].strftime('%d/%m/%Y')}")
        print(f"CPF/Passaporte do participante: {dados_participante['cpf_passaporte']}")
        print("\n")

    def seleciona_participante(self):
        id_participante = self.le_num_inteiro_positivo("Digite o ID do participante: ")
        return id_participante
