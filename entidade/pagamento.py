from datetime import date
from enum import Enum
from typing import Optional
from .pessoa import Pessoa


class MetodoPagamento(Enum):

    DINHEIRO = 1
    PIX = 2
    CREDITO = 3

class BandeiraCartao(Enum):

    VISA = 1
    MASTERCARD = 2
    ELO = 3

class Pagamento:

    def __init__(self,
                 valor: float,
                 data_pagamento: date,
                 metodo: MetodoPagamento,
                 pagador: Optional[Pessoa] = None,
                 dados_pix: dict = None,
                 dados_credito: dict = None
                 ):
        self.__valor = valor
        self.__data_pagamento = data_pagamento
        self.metodo = metodo
        self.pagador = pagador
        self.dados_pix = dados_pix
        self.dados_credito = dados_credito

