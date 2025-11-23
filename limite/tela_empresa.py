from limite.tela_abstract import TelaAbstract


class TelaEmpresa(TelaAbstract):

    def tela_opcoes(self) -> int:
        print("\n" + "=" * 30)
        print("GESTÃO DE EMPRESAS DE TRANSPORTE".center(30))
        print("=" * 30)
        print("[1] - Adicionar Nova Empresa")
        print("[2] - Listar Todas as Empresas")
        print("[3] - Alterar Dados de uma Empresa")
        print("[4] - Excluir uma Empresa")
        print("[0] - Voltar ao Menu Principal")
        print("=" * 30)

        opcao = self.le_num_inteiro_positivo("Escolha a opção: ", [1, 2, 3, 4, 0])
        return opcao

    def pega_dados_empresa(self, empresa_existente=None) -> dict:
        print("-------- DADOS DO PARTICIPANTE ----------")
        nome = input("Nome: ")
        telefone = self.le_num_inteiro_positivo("Telefone: ")
        cnpj = input("CNPJ: ")
        print('\n')
        return {"nome": nome,
                "telefone": telefone,
                "cnpj": cnpj,
                }

    def mostra_empresa(self, dados_empresa):
        print("\n")
        print(f"ID da empresa: #{dados_empresa['id']}")
        print(f"Nome da empresa: {dados_empresa['nome']}")
        print(f"Telefone da empresa: {dados_empresa['telefone']}")
        print(f"CNPJ da empresa: {dados_empresa['cnpj']}")
        print("\n")

    def seleciona_empresa(self) -> int:
        return self.le_num_inteiro_positivo("Digite o ID da empresa que deseja selecionar: ")
