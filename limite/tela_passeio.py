from datetime import datetime
from limite.tela_abstract import TelaAbstract


class TelaPasseio(TelaAbstract):

    def tela_opcoes(self) -> int:
        print("\n" + "=" * 30)
        print("GESTÃO DE PASSEIOS".center(30))
        print("=" * 30)
        print("[1] - Adicionar Novo Passeio")
        print("[2] - Listar Todos os Passeios")
        print("[3] - Alterar um Passeio")
        print("[4] - Excluir um Passeio")
        print("[0] - Voltar ao Menu Principal")
        print("=" * 30)
        return self.le_num_inteiro_positivo("Escolha uma opção: ", [1, 2, 3, 4, 0])

    def pega_dados_passeio(self) -> dict:
        print("\n--- DADOS DO PASSEIO ---")
        nome = input("Nome do Passeio: ")
        atracao = input("Atração Turística Principal: ")
        
        id_cidade = self.le_num_inteiro_positivo("Digite o ID da cidade do passeio: ")
        
        try:
            str_inicio = input("Horário de Início (AAAA-MM-DD HH:MM): ")
            horario_inicio = datetime.strptime(str_inicio, '%Y-%m-%d %H:%M')
            
            str_fim = input("Horário de Fim (AAAA-MM-DD HH:MM): ")
            horario_fim = datetime.strptime(str_fim, '%Y-%m-%d %H:%M')
            
            valor = float(input("Valor do Passeio (ex: 150.50): "))

            return {
                "nome": nome,
                "atracao": atracao,
                "id_cidade": id_cidade,
                "horario_inicio": horario_inicio,
                "horario_fim": horario_fim,
                "valor": valor
            }
        except ValueError:
            self.mostra_mensagem("ERRO: Formato de data/hora ou valor inválido.")
            return None

    def mostra_passeio(self, dados_passeio):
        print("\n")
        print(f"  ID do Passeio: {dados_passeio['id']}")
        print(f"  Nome do Passeio: {dados_passeio['nome']}")
        print(f"  Atração Principal: {dados_passeio['atracao_turistica']}")
        print(f"  Cidade: {dados_passeio['cidade_nome']}")
        print(f"  País: {dados_passeio['pais_nome']}")
        print(f"  Horário de Início: {dados_passeio['horario_inicio']}")
        print(f"  Horário de Fim: {dados_passeio['horario_fim']}")
        print(f"  Valor por Pessoa: R$ {dados_passeio['valor_passeio']:.2f}")
        print("\n")

    def seleciona_passeio(self) -> int:
        return self.le_num_inteiro_positivo("Digite o ID do passeio que deseja selecionar: ")
