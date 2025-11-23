from datetime import date
from entidade.cidade import Cidade
from entidade.transporte import Transporte
from entidade.participante import Participante


class Trecho:

    def __init__(self,
                 id: int,
                 data_viagem: date,
                 origem: Cidade,
                 destino: Cidade,
                 meio_transporte: Transporte,
                 ):
        self.__id = id
        self.__data_viagem = data_viagem
        self.__origem = origem
        self.__destino = destino
        self.__meio_transporte = meio_transporte

    @property
    def id(self):
        return self.__id

    @property
    def data_viagem(self):
        return self.__data_viagem

    @data_viagem.setter
    def data_viagem(self, data_viagem: date):
        self.__data_viagem = data_viagem

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
    def meio_transporte(self):
        return self.__meio_transporte

    @meio_transporte.setter
    def meio_transporte(self, meio_transporte: Transporte):
        self.__meio_transporte = meio_transporte
