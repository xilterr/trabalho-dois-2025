from limite.tela_abstract import TelaAbstract 


class TelaSistema(TelaAbstract):

    def tela_opcoes(self) -> str:
        print("\n" + "=" * 30)
        print("SISTEMA DE GERENCIAMENTO DE VIAGENS".center(30))
        print("=" * 30)
        print("[1] - Gerenciar Participantes")
        print("[2] - Gerenciar Empresas")
        print("[3] - Gerenciar Países")
        print("[4] - Gerenciar Cidades")
        print("[5] - Gerenciar Transportes")
        print("[0] - Sair do Sistema")
        print("=" * 30) 

        opcao = self.le_num_inteiro_positivo("Escolha a opção: ", [1, 2, 3, 4, 5, 0])

        return opcao
