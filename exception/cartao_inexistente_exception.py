

class CartaoInexistenteException(Exception):

    def __init__(self, mensagem="Cartão com este ID não existe."):
        super().__init__(mensagem)
