from entidade.passeio import Passeio
from limite.tela_passeio import TelaPasseio
from exception.opcao_invalida_exception import OpcaoInvalidaException
from entidade.cidade import Cidade
from entidade.pais import Pais


class ControladorPasseio:

    def __init__(self, controlador_sistema):
        self.__passeios: list[Passeio] = []
        self.__tela_passeio = TelaPasseio()
        self.__controlador_sistema = controlador_sistema
        self.__proximo_id = 1
        self.__cidades_disponiveis: list[Cidade] = []
        self.inicializa_cidades_e_paises()

    def inicializa_cidades_e_paises(self):
        pais_br = Pais(1, "Brasil")
        pais_it = Pais(2, "Itália")
        pais_es = Pais(3, "Espanha")
        self.__cidades_disponiveis.append(Cidade(1, "Florianópolis", pais_br))
        self.__cidades_disponiveis.append(Cidade(2, "Rio de Janeiro", pais_br))
        self.__cidades_disponiveis.append(Cidade(3, "Roma", pais_it))
        self.__cidades_disponiveis.append(Cidade(4, "São Paulo", pais_br))
        self.__cidades_disponiveis.append(Cidade(5, "Salvador", pais_br))
        self.__cidades_disponiveis.append(Cidade(6, "Veneza", pais_it))
        self.__cidades_disponiveis.append(Cidade(7, "Florença", pais_it))
        self.__cidades_disponiveis.append(Cidade(8, "Madrid", pais_es))
        self.__cidades_disponiveis.append(Cidade(9, "Barcelona", pais_es))

    def gera_id(self):
        id_gerado = self.__proximo_id
        self.__proximo_id += 1
        return id_gerado

    def pega_passeio_por_id(self, id: int):
        for passeio in self.__passeios:
            if passeio.id == id:
                return passeio
        return None
    
    def pega_cidade_por_id(self, id: int):
        for cidade in self.__cidades_disponiveis:
            if cidade.id == id:
                return cidade
        return None

    def listar_cidades_disponiveis(self):
        self.__tela_passeio.mostra_mensagem("\n--- Cidades Disponíveis ---")
        for cidade in self.__cidades_disponiveis:
            self.__tela_passeio.mostra_mensagem(str(cidade))

    def incluir_passeio(self):
        self.listar_cidades_disponiveis()
        dados = self.__tela_passeio.pega_dados_passeio()
        
        if dados:
            cidade = self.pega_cidade_por_id(dados["id_cidade"])
            if cidade:
                novo_id = self.gera_id()
                novo_passeio = Passeio(novo_id, dados["nome"], dados["atracao"], cidade, 
                                       dados["horario_inicio"], dados["horario_fim"], dados["valor"])
                self.__passeios.append(novo_passeio)
                self.__tela_passeio.mostra_mensagem("Passeio incluído com sucesso!")
            else:
                self.__tela_passeio.mostra_mensagem("ERRO: Cidade não encontrada com o ID fornecido.")

    def listar_passeios(self):
        if not self.__passeios:
            self.__tela_passeio.mostra_mensagem("ATENÇÃO: Não existem passeios cadastrados.")
            return

        self.__tela_passeio.mostra_mensagem('-------- LISTAGEM DOS PASSEIOS ----------')
        
        for passeio in self.__passeios:
            dados_para_tela = {
                "id": passeio.id,
                "nome": passeio.nome,
                "atracao_turistica": passeio.atracao_turistica,
                "cidade_nome": passeio.cidade.nome,
                "pais_nome": passeio.cidade.pais.nome,
                "horario_inicio": passeio.horario_inicio.strftime('%d/%m/%Y %H:%M'),
                "horario_fim": passeio.horario_fim.strftime('%d/%m/%Y %H:%M'),
                "valor_passeio": passeio.valor_passeio
            }
            self.__tela_passeio.mostra_passeio(dados_para_tela)

    def alterar_passeio(self):
        self.listar_passeios()
        if not self.__passeios: return
        
        try:
            id_passeio = self.__tela_passeio.seleciona_passeio()
            passeio = self.pega_passeio_por_id(id_passeio)

            if passeio:
                self.listar_cidades_disponiveis()
                novos_dados = self.__tela_passeio.pega_dados_passeio()
                if novos_dados:
                    nova_cidade = self.pega_cidade_por_id(novos_dados["id_cidade"])
                    if nova_cidade:
                        passeio.nome = novos_dados["nome"]
                        passeio.atracao_turistica = novos_dados["atracao"]
                        passeio.cidade = nova_cidade
                        passeio.horario_inicio = novos_dados["horario_inicio"]
                        passeio.horario_fim = novos_dados["horario_fim"]
                        passeio.valor_passeio = novos_dados["valor"]
                        self.__tela_passeio.mostra_mensagem("Dados do passeio alterados com sucesso!")
                    else:
                        self.__tela_passeio.mostra_mensagem("ERRO: Nova cidade não encontrada.")
            else:
                self.__tela_passeio.mostra_mensagem("ATENÇÃO: Passeio não encontrado.")
        except OpcaoInvalidaException as e:
            self.__tela_passeio.mostra_mensagem(f"ERRO: {e}")

    def excluir_passeio(self):
        self.listar_passeios()
        if not self.__passeios: return
        
        try:
            id_passeio = self.__tela_passeio.seleciona_passeio()
            passeio = self.pega_passeio_por_id(id_passeio)
            if passeio:
                self.__passeios.remove(passeio)
                self.__tela_passeio.mostra_mensagem("Passeio excluído com sucesso!")
            else:
                self.__tela_passeio.mostra_mensagem("ATENÇÃO: Passeio não encontrado.")
        except OpcaoInvalidaException as e:
            self.__tela_passeio.mostra_mensagem(f"ERRO: {e}")

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {1: self.incluir_passeio, 2: self.listar_passeios,
                        3: self.alterar_passeio, 4: self.excluir_passeio}
        while True:
            try:
                opcao = self.__tela_passeio.tela_opcoes()
                if opcao == 0:
                    self.retornar()
                    break
                
                funcao_escolhida = lista_opcoes.get(opcao)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    raise OpcaoInvalidaException("Opção de menu inválida.")
            except OpcaoInvalidaException as e:
                self.__tela_passeio.mostra_mensagem(f"ERRO: {e}")
