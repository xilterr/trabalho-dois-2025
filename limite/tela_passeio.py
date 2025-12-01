import FreeSimpleGUI as sg
from datetime import time
from limite.tela_abstract import TelaAbstract


class TelaPasseio(TelaAbstract):

    def __init__(self):
        super().__init__()

    def tela_opcoes(self) -> int:
        layout_botoes = [
            [sg.Button("Adicionar novo Passeio", key=1, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Listar todos os Passeios", key=2, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Alterar dados de um Passeio", key=3, size=(40, 2), font=self.fonte_padrao)],
            [sg.Button("Excluir um Passeio", key=4, size=(40, 2), font=self.fonte_padrao)]
        ]

        layout = [
            [sg.Text("GERENCIAMENTO DE PASSEIOS", font=self.fonte_titulo, justification='center', expand_x=True)],
            [sg.VPush()],
            [sg.Column(layout_botoes, justification='center', element_justification='center')],
            [sg.VPush()],
            [sg.Button("Voltar", key=0, size=(15, 1), button_color=('white', '#B22222'), font=self.fonte_padrao), sg.Push()]
        ]

        window = sg.Window('Passeios', layout, size=self.tamanho_janela, element_justification='center')
        button, values = window.read()
        window.close()

        if button is None or button == 0:
            return 0
        return button

    def pega_dados_passeio(self) -> dict:
        linha_inicio = [sg.Text("Horário Início:", size=(15, 1), font=self.fonte_padrao)] + self.cria_input_hora('inicio')
        linha_fim = [sg.Text("Horário Fim:", size=(15, 1), font=self.fonte_padrao)] + self.cria_input_hora('fim')

        layout = [
            [sg.Text("DADOS DO PASSEIO", font=self.fonte_titulo)],
            [sg.Text("Atração:", size=(15, 1), font=self.fonte_padrao), sg.InputText(key='atracao', font=self.fonte_padrao, expand_x=True)],
            [sg.Text("Valor (R$):", size=(15, 1), font=self.fonte_padrao), sg.InputText(key='valor', font=self.fonte_padrao, expand_x=True)],
            linha_inicio,
            linha_fim,
            [sg.VPush()],
            [sg.Button("Cancelar", key='Cancelar', size=(15, 1), button_color=('white', '#B22222'), font=self.fonte_padrao),
             sg.Push(),
             sg.Button("Confirmar", key='Confirmar', size=(15, 1), button_color=('white', '#006400'), font=self.fonte_padrao)]
        ]

        window = sg.Window('Cadastro de Passeio', layout, size=self.tamanho_janela)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None
            
            if event == 'Confirmar':
                try:
                    atracao = values['atracao']
                    valor = float(values['valor'])
                    
                    h_ini = int(values['inicio_hora'])
                    m_ini = int(values['inicio_minuto'])
                    horario_inicio = time(h_ini, m_ini)

                    h_fim = int(values['fim_hora'])
                    m_fim = int(values['fim_minuto'])
                    horario_fim = time(h_fim, m_fim)

                    if not atracao:
                        raise ValueError("Atração vazia")

                    window.close()
                    return {
                        "atracao": atracao,
                        "horario_inicio": horario_inicio,
                        "horario_fim": horario_fim,
                        "valor": valor
                    }
                except ValueError:
                    sg.popup_error("Dados inválidos. Verifique se os campos estão preenchidos e o valor é numérico.", font=self.fonte_padrao)

    def seleciona_passeio(self, dados_passeios: list) -> int:
        tabela_dados = []
        for p in dados_passeios:
            tabela_dados.append([
                p['id'], 
                p['atracao'], 
                p['cidade'], 
                p['horario_inicio'].strftime('%H:%M'), 
                p['horario_fim'].strftime('%H:%M'), 
                f"R$ {p['valor']:.2f}"
            ])

        colunas = ["ID", "Atração", "Cidade", "Início", "Fim", "Valor"]

        layout = [
            [sg.Text("SELEÇÃO DE PASSEIO", font=self.fonte_titulo, justification='center', expand_x=True)],
            [sg.Table(values=tabela_dados, headings=colunas, 
                      auto_size_columns=False,
                      col_widths=[5, 25, 20, 8, 8, 10],
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

        window = sg.Window('Lista de Passeios', layout, size=self.tamanho_janela, resizable=True)

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

    def mostra_passeio(self, dados_passeio):
        msg = f"ID: {dados_passeio['id']}\n" \
              f"Atração: {dados_passeio['atracao']}\n" \
              f"Cidade: {dados_passeio['cidade']}\n" \
              f"Horário: {dados_passeio['horario_inicio']} - {dados_passeio['horario_fim']}\n" \
              f"Valor: R${dados_passeio['valor']:.2f}"
        sg.popup('Dados do Passeio', msg, font=self.fonte_padrao)
