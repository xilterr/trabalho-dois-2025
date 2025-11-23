from datetime import date
from limite.tela_abstract import TelaAbstract
from entidade.viagem import Viagem


class TelaViagem(TelaAbstract):

    def tela_opcoes_principal(self) -> int:
        print("\n" + "="*30)
        print("GERENCIAR VIAGENS".center(30))
        print("="*30)
        print("[1] - Criar Nova Viagem")
        print("[2] - Listar Todas as Viagens")
        print("[3] - Selecionar e Gerenciar uma Viagem")
        print("[0] - Voltar ao Menu Principal")
        print("="*30)
        return self.le_num_inteiro_positivo("Escolha uma opção: ", [1, 2, 3, 0])

    def tela_opcoes_gerenciar(self, nome_viagem: str) -> int:
        print("\n" + "="*30)
        print(f"VIAGEM: {nome_viagem.upper()}".center(30))
        print("="*30)
        print("[1] - Adicionar Participantes")
        print("[2] - Listar Detalhes da Viagem")
        print("[3] - Gerenciar Itinerário")
        print("[0] - Voltar")
        print("="*30)   
        return self.le_num_inteiro_positivo("Escolha uma opção: ", [1, 2, 3, 0])

    def tela_opcoes_itinerario(self) -> int:
        print("\n" + "-- Menu Itinerário --".center(30))
        print("[1] - Adicionar Dia de Viagem")
        print("[2] - Adicionar Passeio a um Dia")
        print("[3] - Listar Itinerário Completo")
        print("[0] - Voltar")
        print("="*30)
        return self.le_num_inteiro_positivo("Escolha uma opção: ", [1, 2, 3, 0])

    def pega_dados_viagem(self) -> dict:
        print("\n--- DADOS DA VIAGEM ---")
        nome = input("Nome da viagem: ")
        try:
            ano_i, mes_i, dia_i = map(int, input("Data de início (AAAA-MM-DD): ").split('-'))
            data_inicio = date(ano_i, mes_i, dia_i)
            ano_f, mes_f, dia_f = map(int, input("Data de fim (AAAA-MM-DD): ").split('-'))
            data_fim = date(ano_f, mes_f, dia_f)
            return {"nome": nome, "data_inicio": data_inicio, "data_fim": data_fim}
        except ValueError:
            self.mostra_mensagem("Formato de data inválido! Use AAAA-MM-DD.")
            return None

    def pega_dados_dia_viagem(self) -> dict:
        print("\n--- Novo Dia de Viagem ---")
        try:
            ano, mes, dia = map(int, input("Data (AAAA-MM-DD): ").split('-'))
            data = date(ano, mes, dia)
            id_cidade = self.le_num_inteiro_positivo("Digite o ID da cidade principal para este dia: ")
            return {"data": data, "id_cidade": id_cidade}
        except ValueError:
            self.mostra_mensagem("ERRO: Formato de data inválido.")
            return None

    def mostra_itinerario(self, viagem: Viagem):
        print("\n" + f"--- Itinerário da Viagem: {viagem.nome} ---".center(40))
        if not viagem.itinerario.dias_de_viagem:
            self.mostra_mensagem("Nenhum dia cadastrado no itinerário.")
        else:
            for dia in viagem.itinerario.dias_de_viagem:
                print(dia) 
                if dia.passeios:
                    print("Passeios neste dia:")
                    for passeio in dia.passeios:
                        print(str(passeio).replace("\n", "\n    "))
                else:
                    print("(Nenhum passeio neste dia)")
        print("-" * 40)

    def mostra_viagem(self, dados_viagem: str):
        print(dados_viagem)

    def mostra_detalhes_viagem(self, viagem: Viagem):
        print("\n" + "-"*30)
        print(f"DETALHES DA VIAGEM: {viagem.nome}")
        print(f"Período: {viagem.data_inicio} a {viagem.data_fim}")
        
        print("\nParticipantes:")
        if not viagem.participantes:
            print("Nenhum participante adicionado.")
        else:
            for part in viagem.participantes:
                print(f"Nome: {part.nome}, ID: #{part.id})")
        
        print("-"*30)

    def seleciona_item(self, mensagem: str) -> int:
        return self.le_num_inteiro_positivo(mensagem)
