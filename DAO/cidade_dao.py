from DAO.dao_abstract import DAO
from entidade.cidade import Cidade


class CidadeDAO(DAO):

    def __init__(self):
        super().__init__('cidades.pkl')

    def add(self, cidade: Cidade):
        if((cidade is not None)
           and isinstance(cidade, Cidade)
           and isinstance(cidade.id, int)):
            super().add(cidade)

    def update(self, cidade: Cidade):
        if((cidade is not None)
           and isinstance(cidade, Cidade)
           and isinstance(cidade.id, int)):
            super().update(cidade)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)
