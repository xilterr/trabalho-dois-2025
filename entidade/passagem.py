from entidade.trecho import Trecho
from entidade.empresa import Empresa
from entidade.participante import Participante
from entidade.transporte import Transporte


class Passagem:

    def __init__(self,
                 id: int,
                 trecho: Trecho,
                 transporte: Transporte,
                 empresa: Empresa,
                 valor_total: float,
                 participante_pagante: Participante,
                 participante_passagem: Participante
                 ):
        self.__id = id
        self.__trecho = trecho
        self.__transporte = transporte
        self.__empresa = empresa
        self.__valor_total = valor_total
        self.__participante_pagante = participante_pagante
        self.__participante_passagem = participante_passagem
        self.__valor_pago = 0.0
        self.__compra_realizada = False
        self.__pagamentos = []

    @property
    def id(self):
        return self.__id

    @property
    def trecho(self):
        return self.__trecho

    @trecho.setter
    def trecho(self, trecho: Trecho):
        self.__trecho = trecho

    @property
    def transporte(self):
        return self.__transporte

    @transporte.setter
    def transporte(self, transporte: Transporte):
        self.__transporte = transporte

    @property
    def empresa(self):
        return self.__empresa

    @empresa.setter
    def empresa(self, empresa: Empresa):
        self.__empresa = empresa

    @property
    def valor_total(self):
        return self.__valor_total

    @valor_total.setter
    def valor_total(self, valor_total: float):
        self.__valor_total = valor_total

    @property
    def valor_pago(self):
        return self.__valor_pago

    @valor_pago.setter
    def valor_pago(self, valor_pago: float):
        self.__valor_pago = valor_pago

    @property
    def participante_pagante(self):
        return self.__participante_pagante

    @participante_pagante.setter
    def participante_pagante(self, participante_pagante: Participante):
        self.__participante_pagante = participante_pagante

    @property
    def participante_passagem(self):
        return self.__participante_passagem

    @participante_passagem.setter
    def participante_passagem(self, participante_passagem: Participante):
        self.__participante_passagem = participante_passagem

    @property
    def compra_realizada(self):
        return self.__compra_realizada

    @compra_realizada.setter
    def compra_realizada(self, status: bool):
        self.__compra_realizada = status

    @property
    def pagamentos(self):
        return self.__pagamentos
