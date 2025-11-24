from datetime import date
from entidade.cidade import Cidade
from entidade.transporte import Transporte
from entidade.participante import Participante


class Trecho:

    def __init__(self,
                 id: int,
                 data: date,
                 origem: Cidade,
                 destino: Cidade,
                 transporte: Transporte,
                 ):
        self.__id = id
        self.__data = data
        self.__origem = origem
        self.__destino = destino
        self.__transporte = transporte

    @property
    def id(self):
        return self.__id

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data: date):
        self.__data = data

    @property
    def origem(self):
        return self.__origem

    @origem.setter
    def origem(self, origem: Cidade):
        self.__origem = origem

    @property
    def destino(self):
        return self.__destino

    @destino.setter
    def destino(self, destino: Cidade):
        self.__destino = destino

    @property
    def transporte(self):
        return self.__transporte

    @transporte.setter
    def transporte(self, transporte: Transporte):
        self.__transporte = transporte
