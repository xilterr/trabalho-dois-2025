from datetime import date
from entidade.participante import Participante
from entidade.viagem import Viagem
from entidade.participante import Participante
from entidade.metodo_pagamento import MetodoPagamento 


class Pagamento:

    def __init__(self,
                 id: int,
                 modalidade: MetodoPagamento,
                 data: date,
                 viagem: Viagem,
                 pessoa_pagante: Participante,
                 valor_pago: float                 
                 ):
        self.__id = id
        self.__modalidade = modalidade
        self.__data = data
        self.__viagem = viagem
        self.__pessoa_pagante = pessoa_pagante
        self.__valor_pago = valor_pago

    @property
    def id(self):
        return self.__id

    @property
    def modalidade(self):
        return self.__modalidade

    @modalidade.setter
    def modalidade(self, modalidade: MetodoPagamento):
        self.__modalidade = modalidade

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data: date):
        self.__data = data

    @property
    def viagem(self):
        return self.__viagem

    @viagem.setter
    def viagem(self, viagem: Viagem):
        self.__viagem = viagem

    @property
    def pessoa_pagante(self):
        return self.__pessoa_pagante

    @pessoa_pagante.setter
    def pessoa_pagante(self, pessoa_pagante: Participante):
        self.__pessoa_pagante = pessoa_pagante

    @property
    def valor_pago(self):
        return self.__valor_pago

    @valor_pago.setter
    def valor_pago(self, valor_pago: float):
        self.__valor_pago = valor_pago
