class Pais:
    def __init__(self, id: int, nome: str):
        self.__id = id
        self.__nome = nome

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    def __str__(self):
        return f"ID: {self.id} | País: {self.nome}"
