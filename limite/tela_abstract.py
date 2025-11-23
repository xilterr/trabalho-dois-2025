from abc import ABC
from exception.opcao_invalida_exception import OpcaoInvalidaException
from exception.dado_em_branco_exception import DadoEmBrancoException


class TelaAbstract(ABC):

    def mostra_mensagem(self, msg: str):
        print(msg)
        input("Pressione Enter para continuar...")

    def le_num_inteiro_positivo(self, mensagem: str = '', inteiros_validos = []):
        while True:
            valor_lido = input(mensagem)

            try:
                inteiro = int(valor_lido)

            except ValueError:
                print("ERRO: Valor incorreto. Digite apenas números inteiros.")
                continue

            if inteiros_validos and inteiro not in inteiros_validos:
                print(f"ERRO: Valor inválido. As opções permitidas são: {inteiros_validos}")
                continue
            
            if inteiro < 0:
                print("ERRO: O número não pode ser negativo.")
                continue

            return inteiro
