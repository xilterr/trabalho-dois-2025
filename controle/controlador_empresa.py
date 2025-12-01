from entidade.empresa import Empresa
from limite.tela_empresa import TelaEmpresa
from exception.opcao_invalida_exception import OpcaoInvalidaException
from exception.dado_em_branco_exception import DadoEmBrancoException
from exception.empresa_repetida_exception import EmpresaRepetidoException
from DAO.empresa_dao import EmpresaDAO


class ControladorEmpresa:

    def __init__(self, controlador_sistema):
        self.__tela_empresa = TelaEmpresa()
        self.__controlador_sistema = controlador_sistema
        self.__empresa_DAO = EmpresaDAO()

    def gera_id(self):
        lista_empresas = self.__empresa_DAO.get_all()

        if not lista_empresas:
            return 1

        maior_id = 1 + max([e.id for e in lista_empresas])
        return maior_id

    def pega_empresa_por_id(self):
        dados_lista = []
        for e in self.__empresa_DAO.get_all():
            dados_lista.append({
                "id": e.id,
                "nome": e.nome,
                "cnpj": e.cnpj,
                "telefone": e.telefone
            })
        
        id_selecionado = self.__tela_empresa.seleciona_empresa(dados_lista)

        if id_selecionado is None:
            return None

        for empresa in self.__empresa_DAO.get_all():
            if empresa.id == id_selecionado:
                return empresa
        
        self.__tela_empresa.mostra_mensagem("ATENÇÃO: Empresa com este ID não foi encontrada.")
        return None

    def incluir_empresa(self):
        dados_empresa = self.__tela_empresa.pega_dados_empresa()
        
        if dados_empresa is None:
            return

        try:
            if (not dados_empresa["nome"] or 
                not dados_empresa["cnpj"] or 
                not dados_empresa["telefone"]):
                    raise DadoEmBrancoException

            for empresa in self.__empresa_DAO.get_all():
                if empresa.cnpj == dados_empresa["cnpj"]:
                    raise EmpresaRepetidoException(dados_empresa["cnpj"])

            novo_id = self.gera_id()
            nova_empresa = Empresa(
                novo_id,
                dados_empresa["nome"],
                dados_empresa["telefone"],
                dados_empresa["cnpj"],
            )
            
            self.__empresa_DAO.add(nova_empresa)
            self.__tela_empresa.mostra_mensagem(f"A empresa {nova_empresa.nome} foi cadastrada com sucesso!")

        except (EmpresaRepetidoException, DadoEmBrancoException)  as e:
            self.__tela_empresa.mostra_mensagem(f"ERRO: {e}")

    def listar_empresas(self):
        dados_lista = []
        for e in self.__empresa_DAO.get_all():
            dados_lista.append({
                "id": e.id,
                "nome": e.nome,
                "cnpj": e.cnpj,
                "telefone": e.telefone
            })
            
        self.__tela_empresa.seleciona_empresa(dados_lista)

    def alterar_empresa(self):
        if not self.__empresa_DAO.get_all():
            self.__tela_empresa.mostra_mensagem("ATENÇÃO: Não há empresas cadastradas.")
            return

        try:
            empresa_selecionada = self.pega_empresa_por_id()

            if empresa_selecionada:
                novos_dados_empresa = self.__tela_empresa.pega_dados_empresa()

                if novos_dados_empresa is None:
                    return

                empresa_selecionada.nome = novos_dados_empresa["nome"]
                empresa_selecionada.telefone = novos_dados_empresa["telefone"]
                empresa_selecionada.cnpj = novos_dados_empresa["cnpj"]

                self.__empresa_DAO.update(empresa_selecionada)

                self.__tela_empresa.mostra_mensagem("Dados atualizados da empresa:")
                dados_atualizados = {
                    "id": empresa_selecionada.id,
                    "nome": empresa_selecionada.nome,
                    "telefone": empresa_selecionada.telefone,
                    "cnpj": empresa_selecionada.cnpj,
                }
                self.__tela_empresa.mostra_empresa(dados_atualizados)
        except OpcaoInvalidaException as e:
            self.__tela_empresa.mostra_mensagem(f"ERRO: {e}")

    def excluir_empresa(self):
        if not self.__empresa_DAO.get_all():
            self.__tela_empresa.mostra_mensagem("ATENÇÃO: Não há empresas cadastradas.")
            return

        try:
            empresa_selecionada = self.pega_empresa_por_id()
            if empresa_selecionada:
                self.__empresa_DAO.remove(empresa_selecionada.id)
                self.__tela_empresa.mostra_mensagem(f"A empresa {empresa_selecionada.nome}, "
                                                    f"ID #{empresa_selecionada.id} foi excluída com sucesso!")
        except OpcaoInvalidaException as e:
            self.__tela_empresa.mostra_mensagem(f"ERRO: {e}")

    def retornar(self):
        return

    def abre_tela(self):
        lista_opcoes = {1: self.incluir_empresa,
                        2: self.listar_empresas,
                        3: self.alterar_empresa, 
                        4: self.excluir_empresa,
                        0: self.retornar
                        }   

        while True:
            try:
                opcao_escolhida = self.__tela_empresa.tela_opcoes()
                
                if opcao_escolhida == 0:
                    self.retornar()
                    break
                
                funcao_escolhida = lista_opcoes.get(opcao_escolhida)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    raise OpcaoInvalidaException("Opção de menu inválida.")

            except OpcaoInvalidaException as e:
                self.__tela_empresa.mostra_mensagem(f"\nERRO: {e}")
