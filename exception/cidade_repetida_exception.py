

class CidadeRepetidoException(Exception):

    def __init__(self, nome):
        self.mensagem = f"Uma cidade com nome {nome} já está cadastrada."
        super().__init__(self.mensagem)
