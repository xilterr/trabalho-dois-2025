

class OpcaoInvalidaException(Exception):

    def __init__(self, mensagem="Ocorreu um erro de opção inválida."):
        super().__init__(mensagem)
