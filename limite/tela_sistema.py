import FreeSimpleGUI as sg
from limite.tela_abstract import TelaAbstract


class TelaSistema(TelaAbstract):

    def __init__(self):
        super().__init__()

    def tela_opcoes(self) -> int:
        layout_botoes = [
            [sg.Button("Gerenciar Participantes", key=1, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Gerenciar Empresas", key=2, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Gerenciar Transportes", key=3, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Gerenciar Países", key=4, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Gerenciar Cidades", key=5, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Gerenciar Passeios", key=6, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Gerenciar Viagens", key=7, size=(40, 2), font=self.fonte_padrao)] 
        ]

        layout = [
            [sg.Text("SISTEMA DE GERENCIAMENTO DE VIAGENS", font=self.fonte_titulo, justification='center', expand_x=True, pad=((0,0), (20, 40)))],
            
            [sg.Column(layout_botoes, justification='center', element_justification='center')],
            
            [sg.VPush()],
            
            [sg.Button("Fechar", key=0, size=(20, 1), button_color=('white', '#B22222'), font=self.fonte_padrao), sg.Push()]
        ]

        window = sg.Window('Menu Principal', layout, size=self.tamanho_janela, element_justification='center')

        button, values = window.read()
        window.close()

        if button is None or button == 0:
            return 0
        
        return button
