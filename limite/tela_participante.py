import FreeSimpleGUI as sg
from datetime import datetime, date
from limite.tela_abstract import TelaAbstract


class TelaParticipante(TelaAbstract):

    def __init__(self):
        super().__init__()

    def tela_opcoes(self) -> int:
        layout_botoes = [
            [sg.Button("Incluir Participante", key=1, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Listar Participantes", key=2, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Alterar Participante", key=3, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Excluir Participante", key=4, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Adicionar Cartão de Crédito", key=5, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Listar Cartões", key=6, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Excluir Cartão", key=7, size=(40, 2), font=self.fonte_padrao)]
        ]

        layout = [
            [sg.Text("GERENCIAMENTO DE PARTICIPANTES", font=self.fonte_titulo, justification='center', expand_x=True)],
            [sg.VPush()],
            [sg.Column(layout_botoes, justification='center', element_justification='center')],
            [sg.VPush()],
            [sg.Button("Voltar", key=0, size=(15, 1), button_color=('white', '#B22222'), font=self.fonte_padrao), sg.Push()]
        ]

        window = sg.Window('Participantes', layout, size=self.tamanho_janela, element_justification='center')
        button, values = window.read()
        window.close()

        if button is None or button == 0:
            return 0
        return button

    def seleciona_participante(self, dados_participantes: list) -> int:
        tabela_dados = []
        for p in dados_participantes:
            tabela_dados.append([
                p['id'],
                p['nome'],
                p['cpf_passaporte'],
                p['telefone'],
                p['data_nascimento'].strftime('%d/%m/%Y')
            ])

        colunas = ["ID", "Nome", "CPF/Passaporte", "Telefone", "Nascimento"]

        layout = [
            [sg.Text("SELEÇÃO DE PARTICIPANTE", font=self.fonte_titulo, justification='center', expand_x=True)],
            [sg.Table(values=tabela_dados, headings=colunas,
                      auto_size_columns=False,
                      col_widths=[5, 30, 15, 15, 12],
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

        window = sg.Window('Lista de Participantes', layout, size=self.tamanho_janela, resizable=True)

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

    def pega_dados_participante(self):
        linha_data = [sg.Text("Nascimento:", size=(15, 1), font=self.fonte_padrao)] + self.cria_input_data('nasc')

        layout = [
            [sg.Text("DADOS DO PARTICIPANTE", font=self.fonte_titulo)],
            [sg.Text("Nome:", size=(15, 1), font=self.fonte_padrao), sg.InputText(key='nome', font=self.fonte_padrao, expand_x=True)],
            [sg.Text("CPF/Passaporte:", size=(15, 1), font=self.fonte_padrao), sg.InputText(key='cpf', font=self.fonte_padrao, expand_x=True)],
            [sg.Text("Telefone:", size=(15, 1), font=self.fonte_padrao), sg.InputText(key='telefone', font=self.fonte_padrao, expand_x=True)],
            linha_data,
            [sg.VPush()],
            [sg.Button("Cancelar", key='Cancelar', size=(15, 1), button_color=('white', '#B22222'), font=self.fonte_padrao),
             sg.Push(),
             sg.Button("Confirmar", key='Confirmar', size=(15, 1), button_color=('white', '#006400'), font=self.fonte_padrao)]
        ]

        window = sg.Window('Cadastro de Participante', layout, size=self.tamanho_janela)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None

            if event == 'Confirmar':
                try:
                    nome = values['nome']
                    cpf = values['cpf']
                    telefone = values['telefone']
                    dia = int(values['nasc_dia'])
                    mes = int(values['nasc_mes'])
                    ano = int(values['nasc_ano'])
                    nascimento = date(ano, mes, dia)

                    window.close()
                    return {"nome": nome, "cpf_passaporte": cpf, "telefone": telefone, "data_nascimento": nascimento}
                except ValueError:
                    sg.popup_error("Data inválida ou campos vazios.", font=self.fonte_padrao)

    def pega_dados_cartao(self):
        layout = [
            [sg.Text("DADOS DO CARTÃO", font=self.fonte_titulo)],
            [sg.Text("Número:", size=(15, 1), font=self.fonte_padrao), sg.InputText(key='numero', font=self.fonte_padrao)],
            [sg.Text("Bandeira:", size=(15, 1), font=self.fonte_padrao), sg.InputText_]()
        ]
