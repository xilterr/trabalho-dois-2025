import FreeSimpleGUI as sg
from limite.tela_abstract import TelaAbstract
from entidade.tipo_transporte import TipoTransporte


class TelaTransporte(TelaAbstract):

    def __init__(self):
        super().__init__()

    def tela_opcoes(self) -> int:
        layout_botoes = [
            [sg.Button("Adicionar Novo Transporte", key=1, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Listar Todos os Transportes", key=2, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Alterar um Transporte", key=3, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Excluir um Transporte", key=4, size=(40, 2), font=self.fonte_padrao)]
        ]

        layout = [
            [sg.Text("GESTÃO DE TRANSPORTES", font=self.fonte_titulo, justification='center', expand_x=True)],
            [sg.VPush()],
            [sg.Column(layout_botoes, justification='center', element_justification='center')],
            [sg.VPush()],
            [sg.Button("Voltar", key=0, size=(15, 1), button_color=('white', '#B22222'), font=self.fonte_padrao), sg.Push()]
        ]

        window = sg.Window('Transportes', layout, size=self.tamanho_janela, element_justification='center')
        button, values = window.read()
        window.close()

        if button is None or button == 0:
            return 0
        return button

    def pega_dados_transporte(self):
        layout = [
            [sg.Text("DADOS DO TRANSPORTE", font=self.fonte_titulo)],
            [sg.Text("Nome do Transporte:", size=(20, 1), font=self.fonte_padrao), sg.InputText(key='nome', font=self.fonte_padrao, expand_x=True)],
            [sg.VPush()],
            [sg.Button("Cancelar", key='Cancelar', size=(15, 1), button_color=('white', '#B22222'), font=self.fonte_padrao),
             sg.Push(),
             sg.Button("Confirmar", key='Confirmar', size=(15, 1), button_color=('white', '#006400'), font=self.fonte_padrao)]
        ]

        window = sg.Window('Cadastro de Transporte', layout, size=self.tamanho_janela)

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

    def mostra_tipos_transporte(self, lista_tipos):
        tipos_str = [f"{t['nome']}" for t in lista_tipos]
        layout = [
            [sg.Text("Selecione o Tipo de Transporte:", font=self.fonte_titulo)],
            [sg.Listbox(values=tipos_str, size=(40, 10), key='tipo', font=self.fonte_padrao)],
            [sg.VPush()],
            [sg.Button("Cancelar", key='Cancelar', size=(15, 1), button_color=('white', '#B22222'), font=self.fonte_padrao),
             sg.Push(),
             sg.Button("Confirmar", key='Confirmar', size=(15, 1), button_color=('white', '#006400'), font=self.fonte_padrao)]
        ]

        window = sg.Window('Tipos de Transporte', layout, size=self.tamanho_janela)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None
            
            if event == 'Confirmar':
                selecao = values['tipo']
                if selecao:
                    nome_selecionado = selecao[0]
                    for tipo in lista_tipos:
                        if tipo['nome'] == nome_selecionado:
                            window.close()
                            return tipo['value']
                else:
                    sg.popup_error("Selecione um tipo.", font=self.fonte_padrao)

    def seleciona_transporte(self, dados_transportes: list) -> int:
        tabela_dados = []
        for t in dados_transportes:
            tabela_dados.append([t['id'], t['nome'], t['tipo'], t['empresa']])

        colunas = ["ID", "Nome", "Tipo", "Empresa"]

        layout = [
            [sg.Text("SELEÇÃO DE TRANSPORTE", font=self.fonte_titulo, justification='center', expand_x=True)],
            [sg.Table(values=tabela_dados, headings=colunas, 
                      auto_size_columns=False,
                      col_widths=[5, 25, 15, 20],
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

        window = sg.Window('Lista de Transportes', layout, size=self.tamanho_janela, resizable=True)

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

    def mostra_transporte(self, dados_transporte):
        msg = f"ID: #{dados_transporte['id']}\nNome: {dados_transporte['nome']}\nTipo: {dados_transporte['tipo']}\nEmpresa: {dados_transporte['empresa']}"
        sg.popup('Dados do Transporte', msg, font=self.fonte_padrao)
