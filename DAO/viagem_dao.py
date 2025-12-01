from DAO.dao_abstract import DAO
from entidade.viagem import Viagem


class ViagemDAO(DAO):

    def __init__(self):
        super().__init__('viagem.pkl')

    def add(self, viagem: Viagem):
        if((viagem is not None)
           and isinstance(viagem, Viagem)
           and isinstance(viagem.id, int)):
            super().add(viagem)

    def update(self, viagem: Viagem):
        if((viagem is not None)
           and isinstance(viagem, Viagem)
           and isinstance(viagem.id, int)):
            super().update(viagem)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)
