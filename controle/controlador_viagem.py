from datetime import date
from entidade.viagem import Viagem
from entidade.trecho import Trecho
from limite.tela_viagem import TelaViagem
from DAO.viagem_dao import ViagemDAO
from exception.opcao_invalida_exception import OpcaoInvalidaException
from exception.dado_em_branco_exception import DadoEmBrancoException
from exception.data_incompativel_exception import DataIncompativelException
from exception.participante_repetido_exception import ParticipanteRepetidoException
from exception.cidade_repetida_exception import CidadeRepetidoException


class ControladorViagem:

    def __init__(self, controlador_sistema):
        self.__tela_viagem = TelaViagem()
        self.__controlador_sistema = controlador_sistema
        self.__controlador_participante = controlador_sistema.controlador_participante
        self.__controlador_cidade = controlador_sistema.controlador_cidade
        self.__controlador_passeio = controlador_sistema.controlador_passeio
        self.__controlador_transporte = controlador_sistema.controlador_transporte
        self.__viagem_DAO = ViagemDAO()

    def gera_id(self):
        lista = self.__viagem_DAO.get_all()
        if not lista:
            return 1
        return max([v.id for v in lista]) + 1

    def gera_id_trecho(self, viagem):
        if not viagem.trechos:
            return 1
        return max([t.id for t in viagem.trechos]) + 1

    def pega_viagem_por_id(self):
        dados_lista = []
        for v in self.__viagem_DAO.get_all():
            dados_lista.append({
                "id": v.id,
                "nome": v.nome,
                "data_inicio": v.data_inicio,
                "data_fim": v.data_fim
            })
        
        id_selecionado = self.__tela_viagem.seleciona_viagem(dados_lista)
        
        if id_selecionado is None:
            return None

        viagem = self.__viagem_DAO.get(id_selecionado)
        
        if not viagem:
            self.__tela_viagem.mostra_mensagem("ATENÇÃO: Viagem não encontrada.")
            return None
        return viagem

    def valida_datas(self, data_inicio, data_fim):
        hoje = date.today()
        if data_inicio < hoje:
            raise DataIncompativelException("A data de início deve ser a partir de hoje.")
        
        if data_fim <= data_inicio:
            raise DataIncompativelException("A data final deve ser posterior à data de início.")

    def incluir_viagem(self):
        dados = self.__tela_viagem.pega_dados_viagem()
        if not dados:
            return

        try:
            if not dados["nome"]:
                raise DadoEmBrancoException()

            self.valida_datas(dados["data_inicio"], dados["data_fim"])

            novo_id = self.gera_id()
            nova_viagem = Viagem(
                novo_id,
                dados["nome"],
                dados["data_inicio"],
                dados["data_fim"]
            )

            self.__viagem_DAO.add(nova_viagem)
            self.__tela_viagem.mostra_mensagem("Viagem criada com sucesso! Próximo passo: Adicionar Participantes.")

        except DadoEmBrancoException or DataIncompativelException as e:
             self.__tela_viagem.mostra_mensagem(f"ERRO: {e}")

    def listar_viagens(self):
        dados_lista = []
        for v in self.__viagem_DAO.get_all():
            dados_lista.append({
                "id": v.id,
                "nome": v.nome,
                "data_inicio": v.data_inicio,
                "data_fim": v.data_fim
            })
        self.__tela_viagem.seleciona_viagem(dados_lista)

    def alterar_viagem(self):
        viagem = self.pega_viagem_por_id()
        if not viagem:
            return

        try:
            dados = self.__tela_viagem.pega_dados_viagem()
            if not dados:
                return
            
            self.valida_datas(dados["data_inicio"], dados["data_fim"])
            
            viagem.nome = dados["nome"]
            viagem.data_inicio = dados["data_inicio"]
            viagem.data_fim = dados["data_fim"]
            
            self.__viagem_DAO.update(viagem)
            self.__tela_viagem.mostra_mensagem("Viagem alterada com sucesso.")

        except DataIncompativelException as e:
            self.__tela_viagem.mostra_mensagem(f"ERRO: {e}")

    def excluir_viagem(self):
        viagem = self.pega_viagem_por_id()
        if not viagem:
            return

        self.__viagem_DAO.remove(viagem.id)
        self.__tela_viagem.mostra_mensagem("Viagem excluída com sucesso.")

    def adicionar_participante_viagem(self):
        viagem = self.pega_viagem_por_id()
        if not viagem:
            return

        participante = self.__controlador_participante.pega_participante_por_id()
        if not participante:
            return

        try:
            for p in viagem.participantes:
                if p.id == participante.id:
                    raise ParticipanteRepetidoException(participante.nome)

            nasc = participante.data_nascimento
            inicio = viagem.data_inicio
            idade = inicio.year - nasc.year - ((inicio.month, inicio.day) < (nasc.month, nasc.day))

            if idade < 18:
                self.__tela_viagem.mostra_mensagem("ERRO: O participante deve ter 18 anos completos na data de início.")
                return

            viagem.participantes.append(participante)
            self.__viagem_DAO.update(viagem)
            self.__tela_viagem.mostra_mensagem("Participante adicionado! Próximo passo sugerido: Adicionar Cidades.")

        except ParticipanteRepetidoException as e:
            self.__tela_viagem.mostra_mensagem(f"ERRO: {e}")

    def listar_participantes_viagem(self):
        viagem = self.pega_viagem_por_id()
        if not viagem:
            return
        
        if not viagem.participantes:
            self.__tela_viagem.mostra_mensagem("Nenhum participante nesta viagem.")
            return

        dados_lista = []
        for p in viagem.participantes:
             dados_lista.append({
                 "id": p.id, "nome": p.nome, "cpf_passaporte": p.cpf_passaporte,
                 "telefone": p.telefone, "data_nascimento": p.data_nascimento
             })
        
        self.__controlador_participante.tela_participante.seleciona_participante(dados_lista)

    def remover_participante_viagem(self):
        viagem = self.pega_viagem_por_id()
        if not viagem:
            return

        if not viagem.participantes:
            self.__tela_viagem.mostra_mensagem("Nenhum participante nesta viagem.")
            return

        dados_lista = []
        for p in viagem.participantes:
             dados_lista.append({
                 "id": p.id, "nome": p.nome, "cpf_passaporte": p.cpf_passaporte,
                 "telefone": p.telefone, "data_nascimento": p.data_nascimento
             })
        
        id_p = self.__controlador_participante.tela_participante.seleciona_participante(dados_lista)
        
        if id_p is None: return

        for p in viagem.participantes:
            if p.id == id_p:
                viagem.participantes.remove(p)
                self.__viagem_DAO.update(viagem)
                self.__tela_viagem.mostra_mensagem("Participante removido.")
                return
        
        self.__tela_viagem.mostra_mensagem("Participante não encontrado na viagem.")

    def adicionar_cidade_viagem(self):
        viagem = self.pega_viagem_por_id()
        if not viagem:
            return

        cidade = self.__controlador_cidade.pega_cidade_por_id()
        if not cidade:
            return

        try:
            for c in viagem.cidades:
                if c.id == cidade.id:
                    raise CidadeRepetidoException(cidade.nome)

            viagem.cidades.append(cidade)
            self.__viagem_DAO.update(viagem)
            self.__tela_viagem.mostra_mensagem("Cidade adicionada! Próximo passo sugerido: Adicionar Passeios.")

        except CidadeRepetidoException as e:
            self.__tela_viagem.mostra_mensagem(f"ERRO: {e}")

    def listar_cidades_viagem(self):
        viagem = self.pega_viagem_por_id()
        if not viagem:
            return

        if not viagem.cidades:
            self.__tela_viagem.mostra_mensagem("Nenhuma cidade nesta viagem.")
            return

        dados_lista = []
        for c in viagem.cidades:
            dados_lista.append({
                "id": c.id,
                "nome": c.nome,
                "pais_nome": c.pais.nome
            })
        
        self.__controlador_cidade.tela_cidade.seleciona_cidade(dados_lista)

    def remover_cidade_viagem(self):
        viagem = self.pega_viagem_por_id()
        if not viagem:
            return
        
        if not viagem.cidades:
            self.__tela_viagem.mostra_mensagem("Nenhuma cidade.")
            return

        dados_lista = []
        for c in viagem.cidades:
            dados_lista.append({
                "id": c.id,
                "nome": c.nome,
                "pais_nome": c.pais.nome
            })
        
        id_c = self.__controlador_cidade.tela_cidade.seleciona_cidade(dados_lista)
        
        if id_c is None: return

        for c in viagem.cidades:
            if c.id == id_c:
                viagem.cidades.remove(c)
                self.__viagem_DAO.update(viagem)
                self.__tela_viagem.mostra_mensagem("Cidade removida.")
                return
        self.__tela_viagem.mostra_mensagem("Cidade não encontrada na viagem.")

    def adicionar_passeio_viagem(self):
        viagem = self.pega_viagem_por_id()
        if not viagem:
            return

        if not viagem.cidades or not viagem.participantes:
            self.__tela_viagem.mostra_mensagem("É necessário ter Cidades e Participantes na viagem.")
            return

        todos_passeios = self.__controlador_passeio._ControladorPasseio__passeio_DAO.get_all()
        
        passeios_filtro = []
        ids_cidades_viagem = [c.id for c in viagem.cidades]

        if todos_passeios:
            for p in todos_passeios:
                if p.cidade.id in ids_cidades_viagem:
                    passeios_filtro.append(p)

        id_passeio = self.__tela_viagem.seleciona_passeio_para_adicionar(passeios_filtro)
        if not id_passeio:
            return

        passeio_obj = next((p for p in passeios_filtro if p.id == id_passeio), None)

        if any(p.id == passeio_obj.id for p in viagem.passeios):
             self.__tela_viagem.mostra_mensagem("ERRO: Passeio já incluso nesta viagem.")
             return

        ids_parts = self.__tela_viagem.seleciona_participantes_para_passeio(viagem.participantes)
        
        if not ids_parts:
            self.__tela_viagem.mostra_mensagem("ERRO: O passeio deve ter pelo menos 1 participante.")
            return

        for id_p in ids_parts:
            part = next((p for p in viagem.participantes if p.id == id_p), None)
            if part and part not in passeio_obj.participantes:
                passeio_obj.participantes.append(part)
        
        self.__controlador_passeio._ControladorPasseio__passeio_DAO.update(passeio_obj)

        viagem.passeios.append(passeio_obj)
        self.__viagem_DAO.update(viagem)
        self.__tela_viagem.mostra_mensagem("Passeio adicionado! Próximo passo sugerido: Trechos.")

    def listar_passeios_viagem(self):
        viagem = self.pega_viagem_por_id()
        if not viagem:
            return
        if not viagem.passeios:
            self.__tela_viagem.mostra_mensagem("Nenhum passeio nesta viagem.")
            return
        
        dados_lista = []
        for p in viagem.passeios:
            dados_lista.append({
                "id": p.id, "atracao": p.atracao, "cidade": p.cidade.nome,
                "horario_inicio": p.horario_inicio, "horario_fim": p.horario_fim, "valor": p.valor
            })
        self.__controlador_passeio.tela_passeio.seleciona_passeio(dados_lista)

    def remover_passeio_viagem(self):
        viagem = self.pega_viagem_por_id()
        if not viagem:
            return
        
        if not viagem.passeios:
            self.__tela_viagem.mostra_mensagem("Nenhum passeio.")
            return
        
        dados_lista = []
        for p in viagem.passeios:
            dados_lista.append({
                "id": p.id, "atracao": p.atracao, "cidade": p.cidade.nome,
                "horario_inicio": p.horario_inicio, "horario_fim": p.horario_fim, "valor": p.valor
            })
        
        id_p = self.__controlador_passeio.tela_passeio.seleciona_passeio(dados_lista)
        if id_p is None: return
        
        passeio_alvo = next((p for p in viagem.passeios if p.id == id_p), None)
        
        if passeio_alvo:
            viagem.passeios.remove(passeio_alvo)
            self.__viagem_DAO.update(viagem)
            self.__tela_viagem.mostra_mensagem("Passeio removido.")
        else:
            self.__tela_viagem.mostra_mensagem("Passeio não encontrado.")

    def adicionar_trecho_viagem(self):
        viagem = self.pega_viagem_por_id()
        if not viagem:
            return

        if not viagem.cidades:
            self.__tela_viagem.mostra_mensagem("Necessário cidades cadastradas para criar trechos.")
            return

        dados = self.__tela_viagem.pega_dados_trecho(viagem.cidades)
        if not dados:
            return
        
        if dados["origem_id"] == dados["destino_id"]:
            self.__tela_viagem.mostra_mensagem("ERRO: Origem e Destino devem ser diferentes.")
            return
            
        origem = next((c for c in viagem.cidades if c.id == dados["origem_id"]), None)
        destino = next((c for c in viagem.cidades if c.id == dados["destino_id"]), None)
        
        transporte = self.__controlador_transporte.pega_transporte_por_id()

        if not origem or not destino or not transporte:
            self.__tela_viagem.mostra_mensagem("Dados inválidos ou cancelados.")
            return

        novo_id = self.gera_id_trecho(viagem)
        
        novo_trecho = Trecho(
            novo_id, 
            dados["data"], 
            origem, 
            destino, 
            transporte
        )
        
        viagem.trechos.append(novo_trecho)
        self.__viagem_DAO.update(viagem)
        self.__tela_viagem.mostra_mensagem("Trecho adicionado com sucesso.")

    def listar_trechos_viagem(self):
        viagem = self.pega_viagem_por_id()
        if not viagem:
            return
        if not viagem.trechos:
            self.__tela_viagem.mostra_mensagem("Nenhum trecho cadastrado.")
            return
        
        for t in viagem.trechos:
            self.__tela_viagem.mostra_trecho({
                "id": t.id,
                "data": t.data.strftime('%d/%m/%Y'),
                "origem": t.origem.nome, 
                "destino": t.destino.nome, 
                "transporte": t.transporte.nome
            })

    def remover_trecho_viagem(self):
        viagem = self.pega_viagem_por_id()
        if not viagem:
            return
        self.listar_trechos_viagem()
        
        id_t = self.__tela_viagem.le_num_inteiro_positivo("ID do Trecho a remover: ")
        
        trecho_alvo = next((t for t in viagem.trechos if t.id == id_t), None)
        if trecho_alvo:
            viagem.trechos.remove(trecho_alvo)
            self.__viagem_DAO.update(viagem)
            self.__tela_viagem.mostra_mensagem("Trecho removido.")
        else:
             self.__tela_viagem.mostra_mensagem("Trecho não encontrado.")

    def relatorio_passeios(self):
        viagens = self.__viagem_DAO.get_all()
        if not viagens:
            self.__tela_viagem.mostra_mensagem("Nenhuma viagem registrada.")
            return

        contagem = {}
        for v in viagens:
            for p in v.passeios:
                nome_completo = f"{p.atracao} ({p.cidade.nome})"
                contagem[nome_completo] = contagem.get(nome_completo, 0) + 1

        if not contagem:
            self.__tela_viagem.mostra_mensagem("Nenhum passeio realizado em nenhuma viagem.")
            return

        mais_visitado = max(contagem, key=contagem.get)
        menos_visitado = min(contagem, key=contagem.get)
        
        msg = f"--- RELATÓRIO DE PASSEIOS ---\n\n"
        msg += f"Mais visitado: {mais_visitado} -> {contagem[mais_visitado]} visitas\n"
        msg += f"Menos visitado: {menos_visitado} -> {contagem[menos_visitado]} visitas"
        
        self.__tela_viagem.mostra_mensagem(msg)

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
            1: self.incluir_viagem,
            2: self.listar_viagens,
            3: self.alterar_viagem,
            4: self.excluir_viagem,
            5: self.adicionar_participante_viagem,
            6: self.remover_participante_viagem,
            7: self.listar_participantes_viagem,
            8: self.adicionar_cidade_viagem,
            9: self.remover_cidade_viagem,
            10: self.listar_cidades_viagem,
            11: self.adicionar_passeio_viagem,
            12: self.remover_passeio_viagem,
            13: self.listar_passeios_viagem,
            14: self.adicionar_trecho_viagem,
            15: self.remover_trecho_viagem,
            16: self.listar_trechos_viagem,
            17: self.relatorio_passeios,
            0: self.retornar
        }

        while True:
            try:
                opcao = self.__tela_viagem.tela_opcoes()
                if opcao == 0:
                    self.retornar()
                    break
                
                funcao = lista_opcoes.get(opcao)
                if funcao:
                    funcao()
                else:
                    raise OpcaoInvalidaException("Opção inválida.")
            
            except OpcaoInvalidaException as e:
                self.__tela_viagem.mostra_mensagem(f"ERRO: {e}")
