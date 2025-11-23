from limite.tela_abstract import TelaAbstract
from entidade.tipo_transporte import TipoTransporte


class TelaTransporte(TelaAbstract):

    def tela_opcoes(self) -> int:
        print("\n" + "=" * 30)
        print("GESTÃO DE TRANSPORTES".center(30))
        print("=" * 30)
        print("[1] - Adicionar Novo Transporte")
        print("[2] - Listar Todos os Transportes")
        print("[3] - Alterar um Transporte")
        print("[4] - Excluir um Transporte")
        print("[0] - Voltar ao Menu Principal")
        print("=" * 30)
        return self.le_num_inteiro_positivo("Escolha uma opção: ", [1, 2, 3, 4, 0])

    def pega_dados_transporte(self):
        print("\n--- DADOS DO TRANSPORTE ---")
        nome = input("Nome do Transporte: ")

        return {"nome": nome}

    def mostra_tipos_transporte(self, lista_tipos):
        print("\n--- TIPOS DE TRANSPORTE DISPONÍVEIS ---")
        for dados in lista_tipos:
            print(f"[{dados['value']}] - {dados['nome']}")
        print("---------------------------------------")

    def mostra_transporte(self, dados_transporte):
        print("\n")
        print(f"ID do transporte: #{dados_transporte['id']}")
        print(f"Nome do transporte: {dados_transporte['nome']}")
        print(f"Tipo do Transporte: {dados_transporte['tipo']}")
        print(f"Empresa do Transporte: {dados_transporte['empresa']}")
        print("\n")

    def seleciona_transporte(self):
        transporte_selecionado = self.le_num_inteiro_positivo("Digite o ID do transporte: ")
        return transporte_selecionado
