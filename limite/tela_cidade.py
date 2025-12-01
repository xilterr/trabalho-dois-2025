import FreeSimpleGUI as sg
from limite.tela_abstract import TelaAbstract


class TelaCidade(TelaAbstract):

    def __init__(self):
        super().__init__()

    def tela_opcoes(self):
        layout_botoes = [
            [sg.Button("Adicionar nova cidade", key=1, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Listar todas as cidades", key=2, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Alterar dados de uma cidade", key=3, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Excluir uma cidade", key=4, size=(40, 2), font=self.fonte_padrao)]
        ]

        layout = [
            [sg.Text("GERENCIAMENTO DE CIDADES", font=self.fonte_titulo, justification='center', expand_x=True)],
            [sg.VPush()],
            [sg.Column(layout_botoes, justification='center', element_justification='center')],
            [sg.VPush()],
            [sg.Button("Voltar", key=0, size=(15, 1), button_color=('white', '#B22222'), font=self.fonte_padrao), sg.Push()]
        ]

        window = sg.Window('Cidades', layout, size=self.tamanho_janela, element_justification='center')
        button, values = window.read()
        window.close()

        if button is None or button == 0:
            return 0
        return button

    def pega_dados_cidade(self):
        layout = [
            [sg.Text("DADOS DA CIDADE", font=self.fonte_titulo)],
            [sg.Text("Nome:", size=(15, 1), font=self.fonte_padrao), sg.InputText(key='nome', font=self.fonte_padrao, expand_x=True)],
            [sg.VPush()],
            [sg.Button("Cancelar", key='Cancelar', size=(15, 1), button_color=('white', '#B22222'), font=self.fonte_padrao),
             sg.Push(),
             sg.Button("Confirmar", key='Confirmar', size=(15, 1), button_color=('white', '#006400'), font=self.fonte_padrao)]
        ]

        window = sg.Window('Cadastro de Cidade', layout, size=self.tamanho_janela)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None
            
            if event == 'Confirmar':
                if values['nome']:
                    window.close()
                    return {"nome": values['nome']}
                else:
                    sg.popup_error("O nome não pode ser vazio.", font=self.fonte_padrao)

    def seleciona_cidade(self, dados_cidades: list) -> int:
        tabela_dados = []
        for c in dados_cidades:
            tabela_dados.append([c['id'], c['nome'], c['pais_nome']])

        colunas = ["ID", "Nome da Cidade", "País"]

        layout = [
            [sg.Text("SELEÇÃO DE CIDADE", font=self.fonte_titulo, justification='center', expand_x=True)],
            [sg.Table(values=tabela_dados, headings=colunas, 
                      auto_size_columns=False,
                      col_widths=[5, 30, 20],
                      justification='left',
                      num_rows=15,
                      alternating_row_color='#F7F3E8',
                      key='tabela',
                      font=self.fonte_padrao,
                      expand_x=True,
                      expand_y=True,
                      enable_events=True)],
            [sg.VPush()],
            [sg.Button("Cancelar", key='Cancelar', size=(15, 1), button_color=('white', '#B22222'), font=self.fonte_padrao),
             sg.Push(),
             sg.Text("ID Selecionado:", font=self.fonte_padrao),
             sg.InputText(key='id', size=(10, 1), font=self.fonte_padrao),
             sg.Button("Continuar", key='Confirmar', size=(15, 1), button_color=('white', '#006400'), font=self.fonte_padrao)]
        ]

        window = sg.Window('Lista de Cidades', layout, size=self.tamanho_janela, resizable=True)

        while True:
            event, values = window.read()
            
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None
            
            if event == 'tabela' and values['tabela']:
                indice_linha = values['tabela'][0]
                linha_dados = tabela_dados[indice_linha]
                window['id'].update(linha_dados[0])

            if event == 'Confirmar':
                try:
                    valor = int(values['id'])
                    window.close()
                    return valor
                except ValueError:
                    sg.popup_error("Por favor, digite ou selecione um ID válido.", font=self.fonte_padrao)

    def mostra_cidade(self, dados_cidade):
        msg = f"ID: #{dados_cidade['id']}\nNome: {dados_cidade['nome']}\nPaís: {dados_cidade['pais_nome']}"
        sg.popup('Dados da Cidade', msg, font=self.fonte_padrao)
