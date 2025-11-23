

class EmpresaRepetidoException(Exception):

    def __init__(self, cnpj):
        self.mensagem = f"Uma Empresa com CNPJ {cnpj} já está cadastrada."
        super().__init__(self.mensagem)
