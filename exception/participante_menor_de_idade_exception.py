

class ParticipanteMenorDeIdadeException(Exception):

    def __init__(self, mensagem="É necessário ter mais de 18 anos para cadastro."):
        super().__init__(mensagem)
