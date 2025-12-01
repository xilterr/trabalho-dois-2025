import FreeSimpleGUI as sg
from abc import ABC, abstractmethod


class TelaAbstract(ABC):

    def __init__(self):
        sg.LOOK_AND_FEEL_TABLE['Creme'] = {
            'BACKGROUND': '#F1D689',
            'TEXT': '#000000',
            'INPUT': '#FFFFFF',
            'TEXT_INPUT': '#000000',
            'SCROLL': '#E3E3E3',
            'BUTTON': ('#000000', '#D2B48C'),
            'PROGRESS': ('#D18C66', '#D0D0D0'),
            'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
        }
        
        sg.theme('Creme')
        
        self.tamanho_janela = (900, 600)
        self.fonte_titulo = ("Helvetica", 20, "bold")
        self.fonte_padrao = ("Helvetica", 12)

    @abstractmethod
    def tela_opcoes(self):
        pass

    def mostra_mensagem(self, mensagem: str):
        titulo = "Atenção"
        if "ERRO" in mensagem.upper():
            sg.popup_error(titulo, mensagem)
        else:
            sg.popup(titulo, mensagem)

    def le_num_inteiro_positivo(self, mensagem: str = "", inteiros_validos: list = None):
        while True:
            valor_lido = sg.popup_get_text(mensagem, title="Entrada de Dados")
            if valor_lido is None: return None
            try:
                valor_int = int(valor_lido)
                if inteiros_validos and valor_int not in inteiros_validos:
                    sg.popup_error(f"Valor inválido. Opções: {inteiros_validos}")
                elif valor_int < 0:
                    sg.popup_error("O valor deve ser positivo.")
                else:
                    return valor_int
            except ValueError:
                sg.popup_error("Valor incorreto. Digite um número inteiro.")

    def cria_input_data(self, key_prefixo):
        dias = [i for i in range(1, 32)]
        meses = [i for i in range(1, 13)]
        anos = [i for i in range(1900, 2026)]
        
        anos.reverse()

        return [
            sg.Combo(dias, size=(5, 1), key=f'{key_prefixo}_dia', readonly=True, default_value=1),
            sg.Text('/'),
            sg.Combo(meses, size=(5, 1), key=f'{key_prefixo}_mes', readonly=True, default_value=1),
            sg.Text('/'),
            sg.Combo(anos, size=(8, 1), key=f'{key_prefixo}_ano', readonly=True, default_value=2000)
        ]

    def cria_input_hora(self, key_prefixo):
        horas = [i for i in range(0, 24)]
        minutos = [f"{i:02d}" for i in range(0, 60)]

        return [
            sg.Combo(horas, size=(5, 1), key=f'{key_prefixo}_hora', readonly=True, default_value=12),
            sg.Text(':'),
            sg.Combo(minutos, size=(5, 1), key=f'{key_prefixo}_minuto', readonly=True, default_value='00')
        ]
