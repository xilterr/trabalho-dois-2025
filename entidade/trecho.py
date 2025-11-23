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
                 valor: float):
        self.__id = id
        self.__data_viagem = data_viagem
        self.__origem = origem
        self.__destino = destino
        self.__meio_transporte = meio_transporte
        self.__valor = valor
        self.__compra_efetuada: bool = False
        self.__responsavel_compra = None

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

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor: float):
        self.__valor = valor

    @property
    def compra_efetuada(self):
        return self.__compra_efetuada

    @compra_efetuada.setter
    def compra_efetuada(self, status: bool):
        self.__compra_efetuada = status

    @property
    def responsavel_compra(self):
        return self.__responsavel_compra

    @responsavel_compra.setter
    def responsavel_compra(self, participante: Participante):
        self.__responsavel_compra = participante

    def __str__(self):
        status_compra = "Sim" if self.compra_efetuada else "Não"
        responsavel = self.responsavel_compra.nome if self.responsavel_compra else "Não definido"
        
        return (f"  ID: {self.id}\n"
                f"  Data: {self.data_viagem.strftime('%d/%m/%Y')}\n"
                f"  Origem: {self.origem.nome}\n"
                f"  Destino: {self.destino.nome}\n"
                f"  Transporte: {self.meio_transporte.nome} ({self.meio_transporte.empresa.nome})\n"
                f"  Valor: R$ {self.valor:.2f}\n"
                f"  Compra Efetuada: {status_compra}\n"
                f"  Responsável pela Compra: {responsavel}\n"
                "  -----------------")
