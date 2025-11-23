from entidade.pessoa import Pessoa
from datetime import date


class Participante(Pessoa):

    def __init__(self, id, nome, telefone, cpf_passaporte: str, data_nascimento: date):
        super().__init__(id, nome, telefone)
        self.__cpf_passaporte = cpf_passaporte
        self.__data_nascimento = data_nascimento

    @property
    def cpf_passaporte(self):
        return self.__cpf_passaporte

    @cpf_passaporte.setter
    def cpf_passaporte(self, cpf_passaporte):
        self.__cpf_passaporte = cpf_passaporte

    @property
    def data_nascimento(self):
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento):
        self.__data_nascimento = data_nascimento
    