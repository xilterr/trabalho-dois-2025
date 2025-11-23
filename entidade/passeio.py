from datetime import time
from entidade.cidade import Cidade


class Passeio:

    def __init__(self,
                 id: int,
                 atracao: str,
                 cidade: Cidade,
                 horario_inicio: time,
                 horario_fim: time,
                 valor: float,
                 ):
        self.__id = id
        self.__atracao = atracao
        self.__cidade = cidade
        self.__horario_inicio = horario_inicio
        self.__horario_fim = horario_fim
        self.__valor = valor
        self.__participantes = []

    @property
    def id(self):
        return self.__id

    @property
    def atracao(self):
        return self.__atracao

    @property
    def pais(self):
        return self.__pais

    @property
    def cidade(self):
        return self.__cidade

    @property
    def horario_inicio(self):
        return self.__horario_inicio

    @property
    def horario_fim(self):
        return self.__horario_fim

    @property
    def valor(self):
        return self.__valor
        
    @property
    def participantes(self):
        return self.__participantes

    @atracao.setter
    def atracao(self, atracao: str):
        self.__atracao = atracao

    @pais.setter
    def pais(self, pais):
        self.__pais = pais

    @cidade.setter
    def cidade(self, cidade: Cidade):
        self.__cidade = cidade

    @horario_inicio.setter
    def horario_inicio(self, horario_inicio: time):
        self.__horario_inicio = horario_inicio

    @horario_fim.setter
    def horario_fim(self, horario_fim: time):
        self.__horario_fim = horario_fim

    @valor.setter
    def valor(self, valor: float):
        self.__valor = valor
