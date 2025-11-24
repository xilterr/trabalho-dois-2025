from .pais import Pais

class Cidade:
    def __init__(self, id: int, nome: str, pais: Pais):
        self.__id = id
        self.__nome = nome
        self.__pais = pais

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def pais(self) -> Pais:
        return self.__pais

    @pais.setter
    def pais(self, pais: Pais):
        self.__pais = pais
