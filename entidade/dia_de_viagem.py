from datetime import date
from entidade.cidade import Cidade
from entidade.passeio import Passeio


class DiaDeViagem:

    def __init__(self, id: int, data: date, cidade_principal: Cidade):
        self.__id = id
        self.__data = data
        self.__cidade_principal = cidade_principal
        self.__passeios: list[Passeio] = []

    @property
    def id(self):
        return self.__id

    @property
    def data(self):
        return self.__data

    @property
    def cidade_principal(self):
        return self.__cidade_principal

    @property
    def passeios(self):
        return self.__passeios

    @data.setter
    def data(self, data: date):
        self.__data = data

    @cidade_principal.setter
    def cidade_principal(self, cidade_principal: Cidade):
        self.__cidade_principal = cidade_principal

    def adicionar_passeio(self, passeio: Passeio):
        if isinstance(passeio, Passeio):
            self.__passeios.append(passeio)

    def __str__(self):
        total_passeios = len(self.__passeios)
        return f"  ID: {self.id} | Data: {self.data.strftime('%d/%m/%Y')} | Cidade Principal: {self.cidade_principal.nome} | Passeios: {total_passeios}"
