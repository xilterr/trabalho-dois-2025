

class ParticipanteInexistenteException(Exception):

    def __init__(self, mensagem="Este participante não existe."):
        super().__init__(mensagem)
