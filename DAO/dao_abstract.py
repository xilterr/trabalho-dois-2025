import pickle
from abc import ABC, abstractmethod
from exception.opcao_invalida_exception import OpcaoInvalidaException


class DAO(ABC):

    @abstractmethod
    def __init__(self, datasource=''):
        self.__datasource = datasource
        self.__cache = []
        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()

    def __dump(self):
        pickle.dump(self.__cache, open(self.__datasource, 'wb'))

    def __load(self):
        self.__cache = pickle.load(open(self.__datasource, 'rb'))

    def add(self, obj):
        self.__cache.append(obj)
        self.__dump()

    def update(self, obj):
        try:
            for index, item in enumerate(self.__cache):
                if item.id == obj.id:
                    self.__cache[index] = obj
                    self.__dump()
                    return
        except OpcaoInvalidaException("Não foi possível atualizar: ID não encontrado."):
            pass

    def get(self, key):
        try:
            for obj in self.__cache:
                if obj.id == key:
                    return obj
            return None
        except OpcaoInvalidaException("Item não encontrado com este ID."):
            pass

    def remove(self, key):
        try:
            for obj in self.__cache:
                if obj.id == key:
                    self.__cache.remove(obj)
                    self.__dump()
                    return
        except OpcaoInvalidaException("Não foi possível remover: ID não encontrado."):
            pass

    def get_all(self):
        return self.__cache
