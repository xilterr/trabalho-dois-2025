

class ParticipanteRepetidoException(Exception):

    def __init__(self, cpf_passaporte):
        self.mensagem = f"Um participante com CPF/passaporte {cpf_passaporte} já está cadastrado."
        super().__init__(self.mensagem)
