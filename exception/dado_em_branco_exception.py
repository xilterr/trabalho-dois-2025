

class DadoEmBrancoException(Exception):

    def __init__(self, mensagem="Os campos com asterisco (*) são obrigatórios."):
        super().__init__(mensagem)
