from entidade.pessoa import Pessoa


class Empresa(Pessoa):

    def __init__(self, id, nome, telefone, cnpj: str):
        super().__init__(id, nome, telefone)
        self.__cnpj = cnpj

    @property
    def cnpj(self):
        return self.__cnpj

    @cnpj.setter
    def cnpj(self, cnpj):
        self.__cnpj = cnpj
