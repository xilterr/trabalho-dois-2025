

class CartaoRepetidoException(Exception):

    def __init__(self):
        self.mensagem = f"Um cartão com mesmo número e bandeira já está cadastrado."
        super().__init__(self.mensagem)
