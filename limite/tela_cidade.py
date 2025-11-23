from limite.tela_abstract import TelaAbstract 


class TelaCidade(TelaAbstract):

    def tela_opcoes(self):
        print("-------- GERENCIAMENTO DE CIDADES ----------")
        print('\n')
        print("[1] - Adicionar nova cidade")
        print("[2] - Listar todas as cidades")
        print("[3] - Alterar dados de uma cidade")
        print("[4] - Excluir uma cidade")
        print("[0] - Voltar ao Menu Principal")
        print('\n')

        opcao = self.le_num_inteiro_positivo("Escolha a opção: ", [1, 2, 3, 4, 0])
        return opcao

    def pega_dados_cidade(self):
        print("-------- DADOS DA CIDADE ----------")
        nome = input("Nome: ")
        
        return {"nome": nome}

    def mostra_cidade(self, dados_pais):
        print("\n")
        print(f"ID: #{dados_pais['id']}")
        print(f"Nome da cidade: {dados_pais['nome']}")
        print(f"Nome do país: {dados_pais['pais_nome']}")
        print("\n")

    def seleciona_cidade(self):
        id_cidade = self.le_num_inteiro_positivo("Digite o ID da cidade: ")
        return id_cidade
