from limite.tela_abstract import TelaAbstract 


class TelaPais(TelaAbstract):

    def tela_opcoes(self):
        print("-------- GERENCIAMENTO DE PAÍSES ----------")
        print('\n')
        print("[1] - Adicionar novo país")
        print("[2] - Listar todos os países")
        print("[3] - Alterar dados de um país")
        print("[4] - Excluir um país")
        print("[0] - Voltar ao Menu Principal")
        print('\n')

        opcao = self.le_num_inteiro_positivo("Escolha a opção: ", [1, 2, 3, 4, 0])
        return opcao

    def pega_dados_pais(self):
        print("-------- DADOS DO PAÍS ----------")
        nome = input("Nome: ")
        
        return {"nome": nome}

    def mostra_pais(self, dados_pais):
        print("\n")
        print(f"ID do país: #{dados_pais['id']}")
        print(f"Nome do país: {dados_pais['nome']}")
        print("\n")

    def seleciona_pais(self):
        id_pais = self.le_num_inteiro_positivo("Digite o ID do país: ")
        return id_pais
