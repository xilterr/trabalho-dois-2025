from DAO.dao_abstract import DAO
from entidade.pais import Pais


class PaisDAO(DAO):

    def __init__(self):
        super().__init__('pais.pkl')

    def add(self, pais: Pais):
        if((pais is not None)
           and isinstance(pais, Pais)
           and isinstance(pais.id, int)):
            super().add(pais)

    def update(self, pais: Pais):
        if((pais is not None)
           and isinstance(pais, Pais)
           and isinstance(pais.id, int)):
            super().update(pais)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)
