import FreeSimpleGUI as sg
from datetime import datetime, date
from limite.tela_abstract import TelaAbstract


class TelaViagem(TelaAbstract):

    def __init__(self):
        super().__init__()

    def tela_opcoes(self) -> int:
        layout = [
            [sg.Text('GERENCIAMENTO DE VIAGENS', font=self.fonte_titulo, justification='center', expand_x=True)],
            [sg.VPush()],
            [sg.Frame('Viagem', [
                [sg.Button('Incluir Viagem', key=1, size=(20, 1), font=self.fonte_padrao), sg.Button('Listar Viagens', key=2, size=(20, 1), font=self.fonte_padrao)],
                [sg.Button('Alterar Viagem', key=3, size=(20, 1), font=self.fonte_padrao), sg.Button('Excluir Viagem', key=4, size=(20, 1), font=self.fonte_padrao)],
                [sg.Button('Relatório de Passeios', key=17, size=(42, 1), font=self.fonte_padrao, button_color=('white', '#DAA520'))]
            ], element_justification='center', expand_x=True)],

            [sg.Frame('Participantes & Cidades', [
                [sg.Button('Add Participante', key=5, size=(18, 1), font=self.fonte_padrao), sg.Button('Remover Partic.', key=6, size=(18, 1), font=self.fonte_padrao), sg.Button('Listar Partic.', key=7, size=(18, 1), font=self.fonte_padrao)],
                [sg.Button('Add Cidade', key=8, size=(18, 1), font=self.fonte_padrao), sg.Button('Remover Cidade', key=9, size=(18, 1), font=self.fonte_padrao), sg.Button('Listar Cidades', key=10, size=(18, 1), font=self.fonte_padrao)]
            ], element_justification='center', expand_x=True)],

            [sg.Frame('Itinerário (Passeios & Trechos)', [
                [sg.Button('Add Passeio', key=11, size=(18, 1), font=self.fonte_padrao), sg.Button('Remover Passeio', key=12, size=(18, 1), font=self.fonte_padrao), sg.Button('Listar Passeios', key=13, size=(18, 1), font=self.fonte_padrao)],
                [sg.Button('Add Trecho', key=14, size=(18, 1), font=self.fonte_padrao), sg.Button('Remover Trecho', key=15, size=(18, 1), font=self.fonte_padrao), sg.Button('Listar Trechos', key=16, size=(18, 1), font=self.fonte_padrao)]
            ], element_justification='center', expand_x=True)],
            
            [sg.VPush()],
            [sg.Button('Voltar', key=0, size=(15, 1), button_color=('white', '#B22222'), font=self.fonte_padrao), sg.Push()]
        ]

        window = sg.Window('Sistema de Viagens', layout, size=self.tamanho_janela)

        button, values = window.read()
        window.close()

        if button is None or button == 0:
            return 0
        return button

    def pega_dados_viagem(self):
        linha_inicio = [sg.Text("Data Início:", size=(15, 1), font=self.fonte_padrao)] + self.cria_input_data('inicio')
        linha_fim = [sg.Text("Data Fim:", size=(15, 1), font=self.fonte_padrao)] + self.cria_input_data('fim')

        layout = [
            [sg.Text('DADOS DA VIAGEM', font=self.fonte_titulo)],
            [sg.Text('Nome da Viagem:', size=(15, 1), font=self.fonte_padrao), sg.InputText(key='nome', font=self.fonte_padrao, expand_x=True)],
            linha_inicio,
            linha_fim,
            [sg.VPush()],
            [sg.Button('Cancelar', key='Cancelar', size=(15, 1), button_color=('white', '#B22222'), font=self.fonte_padrao),
             sg.Push(),
             sg.Button('Confirmar', key='Confirmar', size=(15, 1), button_color=('white', '#006400'), font=self.fonte_padrao)]
        ]

        window = sg.Window('Cadastro de Viagem', layout, size=self.tamanho_janela)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancelar':
                window.close()
                return None
            
            if event == 'Confirmar':
                try:
                    nome = values['nome']
                    d_ini = int(values['inicio_dia'])
                    m_ini = int(values['inicio_mes'])
                    a_ini = int(values['inicio_ano'])
                    data_inicio = date(a_ini, m_ini, d_ini)

                    d_fim = int(values['fim_dia'])
                    m_fim = int(values['fim_mes'])
                    a_fim = int(values['fim_ano'])
                    data_fim = date(a_fim, m_fim, d_fim)
                    
                    window.close()
                    return {"nome": nome, "data_inicio": data_inicio, "data_fim": data_fim}
                except ValueError:
                    sg.popup_error("Data inválida.", font=self.fonte_padrao)

    def mostra_viagem(self, dados_viagem):
        msg = f"ID: {dados_viagem['id']}\n" \
              f"Nome: {dados_viagem['nome']}\n" \
              f"Início: {dados_viagem['data_inicio'].strftime('%d/%m/%Y')}\n" \
              f"Fim: {dados_viagem['data_fim'].strftime('%d/%m/%Y')}"
        sg.popup('Detalhes da Viagem', msg, font=self.fonte_padrao)

    def seleciona_viagem(self, dados_viagens: list) -> int:
        tabela_dados = []
        for v in dados_viagens:
            tabela_dados.append([v['id'], v['nome'], v['data_inicio'].strftime('%d/%m/%Y'), v['data_fim'].strftime('%d/%m/%Y')])

        colunas = ["ID", "Nome", "Início", "Fim"]

        layout = [
            [sg.Text("SELEÇÃO DE VIAGEM", font=self.fonte_titulo, justification='center', expand_x=True)],
            [sg.Table(values=tabela_dados, headings=colunas, 
                      auto_size_columns=False,
                      col_widths=[5, 30, 12, 12],
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

        window = sg.Window('Lista de Viagens', layout, size=self.tamanho_janela, resizable=True)

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

    def seleciona_passeio_para_adicionar(self, passeios_disponiveis):
        lista_display = [f"{p.id}: {p.atracao} ({p.cidade.nome}) - R${p.valor}" for p in passeios_disponiveis]
        
        if not lista_display:
            sg.popup("Não há passeios disponíveis para as cidades desta viagem.", font=self.fonte_padrao)
            return None

        layout = [
            [sg.Text('Selecione o Passeio para adicionar:', font=self.fonte_titulo)],
            [sg.Listbox(values=lista_display, size=(80, 20), key='lb_passeios', font=self.fonte_padrao)],
            [sg.VPush()],
            [sg.Button('Cancelar', key='Cancelar', size=(15, 1), button_color=('white', '#B22222'), font=self.fonte_padrao),
             sg.Push(),
             sg.Button('Confirmar', key='Confirmar', size=(15, 1), button_color=('white', '#006400'), font=self.fonte_padrao)]
        ]

        window = sg.Window('Seleção de Passeio', layout, size=self.tamanho_janela)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None
            
            if event == 'Confirmar':
                selecao = values['lb_passeios']
                if selecao:
                    str_selecionada = selecao[0]
                    id_selecionado = int(str_selecionada.split(':')[0])
                    window.close()
                    return id_selecionado
                else:
                    sg.popup_error("Selecione um item da lista.", font=self.fonte_padrao)

    def seleciona_participantes_para_passeio(self, participantes_da_viagem):
        if not participantes_da_viagem:
            sg.popup("Não há participantes na viagem para selecionar.", font=self.fonte_padrao)
            return []

        lista_display = [f"{p.id}: {p.nome}" for p in participantes_da_viagem]
        
        layout = [
            [sg.Text('Selecione os participantes (Segure Ctrl para múltiplos):', font=self.fonte_titulo)],
            [sg.Listbox(values=lista_display, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(80, 20), key='lb_part', font=self.fonte_padrao)],
            [sg.VPush()],
            [sg.Button('Cancelar', key='Cancelar', size=(15, 1), button_color=('white', '#B22222'), font=self.fonte_padrao),
             sg.Push(),
             sg.Button('Confirmar', key='Confirmar', size=(15, 1), button_color=('white', '#006400'), font=self.fonte_padrao)]
        ]

        window = sg.Window('Participantes do Passeio', layout, size=self.tamanho_janela)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return []
            
            if event == 'Confirmar':
                selecionados_str = values['lb_part']
                ids_selecionados = []
                for s in selecionados_str:
                    ids_selecionados.append(int(s.split(':')[0]))
                
                window.close()
                return ids_selecionados

    def pega_dados_trecho(self, cidades_disponiveis):
        lista_cidades = [f"{c.id}: {c.nome}" for c in cidades_disponiveis]
        linha_data = [sg.Text("Data do Trecho:", size=(15, 1), font=self.fonte_padrao)] + self.cria_input_data('data')

        layout = [
            [sg.Text('NOVO TRECHO', font=self.fonte_titulo)],
            linha_data,
            [sg.Text('Origem:', size=(15, 1), font=self.fonte_padrao), sg.Combo(lista_cidades, key='origem', size=(30, 1), readonly=True, font=self.fonte_padrao)],
            [sg.Text('Destino:', size=(15, 1), font=self.fonte_padrao), sg.Combo(lista_cidades, key='destino', size=(30, 1), readonly=True, font=self.fonte_padrao)],
            [sg.VPush()],
            [sg.Button('Cancelar', key='Cancelar', size=(15, 1), button_color=('white', '#B22222'), font=self.fonte_padrao),
             sg.Push(),
             sg.Button('Confirmar', key='Confirmar', size=(15, 1), button_color=('white', '#006400'), font=self.fonte_padrao)]
        ]

        window = sg.Window('Cadastro de Trecho', layout, size=self.tamanho_janela)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None
            
            if event == 'Confirmar':
                try:
                    d = int(values['data_dia'])
                    m = int(values['data_mes'])
                    a = int(values['data_ano'])
                    data = date(a, m, d)
                    
                    if not values['origem'] or not values['destino']:
                        sg.popup_error("Selecione Origem e Destino.", font=self.fonte_padrao)
                        continue
                    
                    origem_id = int(values['origem'].split(':')[0])
                    destino_id = int(values['destino'].split(':')[0])

                    window.close()
                    return {"data": data, "origem_id": origem_id, "destino_id": destino_id}
                
                except ValueError:
                    sg.popup_error("Data inválida.", font=self.fonte_padrao)

    def mostra_trecho(self, dados_trecho):
        msg = f"ID: {dados_trecho['id']}\n" \
              f"Data: {dados_trecho['data']}\n" \
              f"Rota: {dados_trecho['origem']} -> {dados_trecho['destino']}\n" \
              f"Transporte: {dados_trecho['transporte']}"
        sg.popup('Dados do Trecho', msg, font=self.fonte_padrao)
