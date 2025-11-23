from abc import ABC


class Pessoa(ABC):
    
    def __init__(self, id: str, nome: str, telefone: int):
            self.__id = id
            self.__nome = nome
            self.__telefone = telefone

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome
    
    @property
    def telefone(self):
        return self.__telefone

    @id.setter
    def id(self, id: str):
        self.__id = id

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @telefone.setter
    def telefone(self, telefone: int):
        self.__telefone = telefone
