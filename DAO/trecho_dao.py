from DAO.dao_abstract import DAO
from entidade.trecho import Trecho


class TrechoDAO(DAO):

    def __init__(self):
        super().__init__('trechos.pkl')

    def add(self, trecho: Trecho):
        if((trecho is not None)
           and isinstance(trecho, Trecho)
           and isinstance(trecho.id, int)):
            super().add(trecho)

    def update(self, trecho: Trecho):
        if((trecho is not None)
           and isinstance(trecho, Trecho)
           and isinstance(trecho.id, int)):
            super().update(trecho)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)
