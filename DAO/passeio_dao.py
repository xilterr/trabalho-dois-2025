from DAO.dao_abstract import DAO
from entidade.passeio import Passeio


class PasseioDAO(DAO):

    def __init__(self):
        super().__init__('passeios.pkl')

    def add(self, passeio: Passeio):
        if((passeio is not None) 
           and isinstance(passeio, Passeio) 
           and isinstance(passeio.id, int)):
            super().add(passeio)

    def update(self, passeio: Passeio):
        if((passeio is not None) 
           and isinstance(passeio, Passeio) 
           and isinstance(passeio.id, int)):
            super().update(passeio)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)
