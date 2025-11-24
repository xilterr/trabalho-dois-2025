from entidade.empresa import Empresa
from entidade.tipo_transporte import TipoTransporte


class Transporte:

    def __init__(
                self,
                id: int,
                nome: str,
                tipo: TipoTransporte,
                empresa: Empresa
                ):
        self.__id = id
        self.__nome = nome
        self.__tipo = tipo
        self.__empresa = empresa

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @property
    def tipo(self):
        return self.__tipo

    @property
    def empresa(self):
        return self.__empresa

    @id.setter
    def id(self, id):
        self.__id = id

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @tipo.setter
    def tipo(self, tipo: TipoTransporte):
        self.__tipo = tipo

    @empresa.setter
    def empresa(self, empresa: Empresa):
        self.__empresa = empresa
