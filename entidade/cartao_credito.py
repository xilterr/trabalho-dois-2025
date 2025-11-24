

class CartaoCredito:

    def __init__(self, id: int, numero: int, bandeira: str):
        self.__id = id
        self.__numero = numero
        self.__bandeira = bandeira

    @property
    def id(self):
        return self.__id

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, numero: int):
        self.__numero = numero

    @property
    def bandeira(self):
        return self.__bandeira

    @bandeira.setter
    def bandeira(self, bandeira: str):
        self.__bandeira = bandeira
