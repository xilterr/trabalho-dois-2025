

class PaisRepetidoException(Exception):

    def __init__(self, nome):
        self.mensagem = f"Um país com nome {nome} já está cadastrado."
        super().__init__(self.mensagem)
