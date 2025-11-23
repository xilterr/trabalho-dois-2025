from datetime import date
from typing import List
from entidade.participante import Participante
from entidade.trecho import Trecho
from entidade.itinerario import Itinerario


class Viagem:
    def __init__(self, id: int, nome: str, data_inicio: date, data_fim: date):
        self.__id = id
        self.__nome = nome
        self.__data_inicio = data_inicio
        self.__data_fim = data_fim
        
        self.__participantes: List[Participante] = []
        self.__trechos: List[Trecho] = []
        self.__itinerario: Itinerario = Itinerario()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if isinstance(nome, str):
            self.__nome = nome

    @property
    def data_inicio(self) -> date:
        return self.__data_inicio

    @data_inicio.setter
    def data_inicio(self, data: date):
        if isinstance(data, date):
            self.__data_inicio = data

    @property
    def data_fim(self) -> date:
        return self.__data_fim

    @data_fim.setter
    def data_fim(self, data: date):
        if isinstance(data, date):
            self.__data_fim = data

    @property
    def participantes(self) -> List[Participante]:
        return self.__participantes[:]

    @property
    def trechos(self) -> List[Trecho]:
        return self.__trechos[:]

    @property
    def itinerario(self) -> Itinerario:
        return self.__itinerario

    def add_participante(self, participante: Participante):
        if isinstance(participante, Participante):
            self.__participantes.append(participante)

    def add_trecho(self, trecho: Trecho):
        if isinstance(trecho, Trecho):
            self.__trechos.append(trecho)
            
    def __str__(self) -> str:
        return f"Viagem(ID: {self.id}, Nome: '{self.nome}', De {self.data_inicio} a {self.data_fim})"
