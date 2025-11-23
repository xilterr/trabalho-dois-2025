from datetime import datetime
from entidade.cidade import Cidade
from entidade.participante import Participante


class Passeio:

    def __init__(self,
                 id: int,
                 nome: str,
                 atracao_turistica: str,
                 cidade: Cidade,
                 horario_inicio: datetime,
                 horario_fim: datetime,
                 valor_passeio: float,
                 ):
        self.__id = id
        self.__nome = nome
        self.__atracao_turistica = atracao_turistica
        self.__cidade = cidade
        self.__pais = cidade.pais
        self.__horario_inicio = horario_inicio
        self.__horario_fim = horario_fim
        self.__valor_passeio = valor_passeio
        self.__participantes: list[Participante] = []

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @property
    def atracao_turistica(self):
        return self.__atracao_turistica

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
    def valor_passeio(self):
        return self.__valor_passeio
        
    @property
    def participante(self):
        return self.__participante

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @atracao_turistica.setter
    def atracao_turistica(self, atracao_turistica: str):
        self.__atracao_turistica = atracao_turistica

    @pais.setter
    def pais(self, pais):
        self.__pais = pais

    @cidade.setter
    def cidade(self, cidade: Cidade):
        self.__cidade = cidade

    @horario_inicio.setter
    def horario_inicio(self, horario_inicio: datetime):
        self.__horario_inicio = horario_inicio

    @horario_fim.setter
    def horario_fim(self, horario_fim: datetime):
        self.__horario_fim = horario_fim

    @valor_passeio.setter
    def valor_passeio(self, valor_passeio: float):
        self.__valor_passeio = valor_passeio

    def __str__(self):
        return (f"  ID: {self.id}\n"
                f"  Passeio: {self.nome} ({self.atracao_turistica})\n"
                f"  Local: {self.cidade.nome}, {self.cidade.pais.nome}\n"
                f"  Horário: de {self.horario_inicio.strftime('%d/%m/%Y %H:%M')} a {self.horario_fim.strftime('%d/%m/%Y %H:%M')}\n"
                f"  Valor: R$ {self.valor_passeio:.2f}\n"
                "  -----------------")
