from datetime import datetime, date
from entidade.participante import Participante
from entidade.trecho import Trecho


class Viagem:
    def __init__(self, id: int, nome: str, data_inicio: date, data_fim: date):
        self.__id = id
        self.__nome = nome
        self.__data_inicio = data_inicio
        self.__data_fim = data_fim
        self.__participantes = []
        self.__cidades = []
        self.__passeios = []
        self.__trechos = []

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if isinstance(nome, str):
            self.__nome = nome

    @property
    def data_inicio(self):
        return self.__data_inicio

    @data_inicio.setter
    def data_inicio(self, data: date):
        if isinstance(data, date):
            self.__data_inicio = data

    @property
    def data_fim(self):
        return self.__data_fim

    @data_fim.setter
    def data_fim(self, data: date):
        if isinstance(data, date):
            self.__data_fim = data

    @property
    def participantes(self):
        return self.__participantes

    @property
    def trechos(self):
        return self.__trechos

    @property
    def cidades(self):
        return self.__cidades

    @property
    def passeios(self):
        return self.__passeios
