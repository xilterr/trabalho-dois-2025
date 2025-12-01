import FreeSimpleGUI as sg
from limite.tela_abstract import TelaAbstract


class TelaEmpresa(TelaAbstract):

    def __init__(self):
        super().__init__()

    def tela_opcoes(self) -> int:
        layout_botoes = [
            [sg.Button("Adicionar nova empresa", key=1, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Listar todas as empresas", key=2, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Alterar dados de uma empresa", key=3, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Excluir uma empresa", key=4, size=(40, 2), font=self.fonte_padrao)]
        ]

        layout = [
            [sg.Text("GERENCIAMENTO DE EMPRESAS", font=self.fonte_titulo, justification='center', expand_x=True)],
            [sg.VPush()],
            [sg.Column(layout_botoes, justification='center', element_justification='center')],
            [sg.VPush()],
            [sg.Button("Voltar", key=0, size=(15, 1), button_color=('white', '#B22222'), font=self.fonte_padrao), sg.Push()]
        ]

        window = sg.Window('Empresas', layout, size=self.tamanho_janela, element_justification='center')
        button, values = window.read()
        window.close()

        if button is None or button == 0:
            return 0
        return button

    def pega_dados_empresa(self):
        layout = [
            [sg.Text("DADOS DA EMPRESA", font=self.fonte_titulo)],
            [sg.Text("Nome:", size=(15, 1), font=self.fonte_padrao), sg.InputText(key='nome', font=self.fonte_padrao, expand_x=True)],
            [sg.Text("Telefone:", size=(15, 1), font=self.fonte_padrao), sg.InputText(key='telefone', font=self.fonte_padrao, expand_x=True)],
            [sg.Text("CNPJ:", size=(15, 1), font=self.fonte_padrao), sg.InputText(key='cnpj', font=self.fonte_padrao, expand_x=True)],
            [sg.VPush()],
            [sg.Button("Cancelar", key='Cancelar', size=(15, 1), button_color=('white', '#B22222'), font=self.fonte_padrao),
             sg.Push(),
             sg.Button("Confirmar", key='Confirmar', size=(15, 1), button_color=('white', '#006400'), font=self.fonte_padrao)]
        ]

        window = sg.Window('Cadastro de Empresa', layout, size=self.tamanho_janela)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None
            
            if event == 'Confirmar':
                if values['nome'] and values['cnpj'] and values['telefone']:
                    window.close()
                    return {"nome": values['nome'], "cnpj": values['cnpj'], "telefone": values['telefone']}
                else:
                    sg.popup_error("Todos os campos devem ser preenchidos.", font=self.fonte_padrao)

    def seleciona_empresa(self, dados_empresas: list) -> int:
        tabela_dados = []
        for e in dados_empresas:
            tabela_dados.append([e['id'], e['nome'], e['cnpj'], e['telefone']])

        colunas = ["ID", "Nome", "CNPJ", "Telefone"]

        layout = [
            [sg.Text("SELEÇÃO DE EMPRESA", font=self.fonte_titulo, justification='center', expand_x=True)],
            [sg.Table(values=tabela_dados, headings=colunas, 
                      auto_size_columns=False,
                      col_widths=[5, 30, 20, 15],
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

        window = sg.Window('Lista de Empresas', layout, size=self.tamanho_janela, resizable=True)

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

    def mostra_empresa(self, dados_empresa):
        msg = f"ID: {dados_empresa['id']}\nNome: {dados_empresa['nome']}\nCNPJ: {dados_empresa['cnpj']}\nTelefone: {dados_empresa['telefone']}"
        sg.popup('Dados da Empresa', msg, font=self.fonte_padrao)
