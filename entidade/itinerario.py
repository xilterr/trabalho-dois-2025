from entidade.dia_de_viagem import DiaDeViagem
from typing import List


class Itinerario:

    def __init__(self):
        self.__dias_de_viagem: List[DiaDeViagem] = []

    @property
    def dias_de_viagem(self):
        return self.__dias_de_viagem

    def adicionar_dia_viagem(self, dia: DiaDeViagem):
        if isinstance(dia, DiaDeViagem):
            self.__dias_de_viagem.append(dia)
