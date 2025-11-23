from entidade.transporte import Transporte
from entidade.tipo_transporte import TipoTransporte
from limite.tela_transporte import TelaTransporte
from controle.controlador_empresa import ControladorEmpresa
from exception.opcao_invalida_exception import OpcaoInvalidaException
from exception.dado_em_branco_exception import DadoEmBrancoException
from DAO.transporte_dao import TransporteDAO


class ControladorTransporte:

    def __init__(self, controlador_sistema, controlador_empresa: ControladorEmpresa):
        self.__tela_transporte = TelaTransporte()
        self.__controlador_sistema = controlador_sistema
        self.__controlador_empresa = controlador_empresa
        self.__id_atual = 0
        self.__transporte_DAO = TransporteDAO

    def gera_id(self):
        lista_transportes = self.__transporte_DAO.get_all()

        if not lista_transportes:
            return 1

        maior_id = 1 + max([p.id for p in lista_transportes])
        return maior_id

    def pega_tipo_por_value(self):
        dados_tipos = []
        valores_validos = []
        
        for tipo in TipoTransporte:
            dados_tipos.append({"value": tipo.value, "nome": tipo.name.capitalize()})
            valores_validos.append(tipo.value)

        self.__tela_transporte.mostra_tipos_transporte(dados_tipos)

        valor_lido = self.__tela_transporte.le_num_inteiro_positivo(
            "Digite o número correspondente ao tipo: ", 
            valores_validos
        )

        return TipoTransporte(valor_lido)

    def pega_transporte_por_id(self):
        self.listar_transportes()    
        id_selecionado = self.__tela_transporte.seleciona_transporte()

        if not self.__transporte_DAO.get_all():
            return None

        for transporte in self.__transporte_DAO.get_all():
            if transporte.id == id_selecionado:
                return transporte

        self.__tela_transporte.mostra_mensagem("ATENÇÃO: Transporte com este ID não foi encontrado.")
        return None

    def incluir_transporte(self):
        empresa_selecionada = self.__controlador_empresa.pega_empresa_por_id()
        if empresa_selecionada is None:
            return

        tipo_selecionado = self.pega_tipo_por_value()

        dados_transporte = self.__tela_transporte.pega_dados_transporte()
        if dados_transporte is None:
            return

        try:
            if not dados_transporte["nome"]:
                raise DadoEmBrancoException()

            novo_id = self.gera_id()
            novo_transporte = Transporte(
                novo_id,
                dados_transporte["nome"],
                tipo_selecionado,
                empresa_selecionada
                )
            
            self.__transporte_DAO.add(novo_transporte)
            self.__tela_transporte.mostra_mensagem(f"O transporte {novo_transporte.nome} foi cadastrado com sucesso!")

        except DadoEmBrancoException as e:
            self.__tela_transporte.mostra_mensagem(f"ERRO: {e}")

    def listar_transportes(self):
        if not self.__transporte_DAO.get_all():
            self.__tela_transporte.mostra_mensagem("ATENÇÃO: Não existem transportes cadastrados.")
            return
        else:
            self.__tela_transporte.mostra_mensagem('-------- LISTAGEM DOS TRANSPORTES ----------')

            for transporte in self.__transporte_DAO.get_all():
                dados_para_mostrar = {
                    "id": transporte.id,
                    "nome": transporte.nome,
                    "tipo": transporte.tipo.name.capitalize(), 
                    "empresa": transporte.empresa.nome, 
                }
                self.__tela_transporte.mostra_transporte(dados_para_mostrar)

    def alterar_transporte(self):
        if not self.__transporte_DAO.get_all():
            self.__tela_transporte.mostra_mensagem("ATENÇÃO: Não há transporte cadastrado.")
            return
        
        try:
            transporte_selecionado = self.pega_transporte_por_id()

            if transporte_selecionado:
                novos_dados = self.__tela_transporte.pega_dados_transporte()

                if novos_dados is None:
                    return
                
                transporte_selecionado.nome = novos_dados["nome"]

                self.__transporte_DAO.update(transporte_selecionado)

                self.__tela_transporte.mostra_mensagem("Dados do transporte alterados com sucesso!")
                dados_atualizados = {
                    "id": transporte_selecionado.id,
                    "nome": transporte_selecionado.nome,
                    "tipo": transporte_selecionado.tipo.name.capitalize(),
                    "empresa": transporte_selecionado.empresa.nome
                    }
                self.__tela_transporte.mostra_mensagem('Dados atualizados:')
                self.__tela_transporte.mostra_transporte(dados_atualizados)
        except OpcaoInvalidaException as e:
            self.__tela_transporte.mostra_mensagem(f"ERRO: {e}")

    def excluir_transporte(self):
        if not self.__transporte_DAO.get_all():
            self.__tela_transporte.mostra_mensagem("ATENÇÃO: Não existem transportes cadastrados.")
            return
        
        try:
            transporte = self.pega_transporte_por_id()

            if transporte:
                self.__transporte_DAO.remove(transporte)
                self.__tela_transporte.mostra_mensagem(f"Transporte de ID #{transporte.id} excluído com sucesso!")
            else:
                self.__tela_transporte.mostra_mensagem("ATENÇÃO: Transporte não encontrado.")
        except OpcaoInvalidaException as e:
            self.__tela_transporte.mostra_mensagem(f"ERRO: {e}")

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
            1: self.incluir_transporte,
            2: self.listar_transportes,
            3: self.alterar_transporte,
            4: self.excluir_transporte,
        }
        while True:
            try:
                opcao_escolhida = self.__tela_transporte.tela_opcoes()
                if opcao_escolhida == 0:
                    self.retornar()
                    break
                
                funcao_escolhida = lista_opcoes.get(opcao_escolhida)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    raise OpcaoInvalidaException("Opção de menu inválida.")
            except OpcaoInvalidaException as e:
                self.__tela_transporte.mostra_mensagem(f"ERRO: {e}")
