from DAO.dao_abstract import DAO
from entidade.transporte import Transporte


class TransporteDAO(DAO):

    def __init__(self):
        super().__init__('transportes.pkl')

    def add(self, transporte: Transporte):
        if((transporte is not None)
           and isinstance(transporte, Transporte)
           and isinstance(transporte.id, int)):
            super().add(transporte)

    def update(self, transporte: Transporte):
        if((transporte is not None)
           and isinstance(transporte, Transporte)
           and isinstance(transporte.id, int)):
            super().update(transporte)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)
