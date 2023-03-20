class Grid:
    def __init__(self, uuid, temporada_uuid=None, nome=None, simulador=None, dia_da_semana=None, link_onboard=None):
        self.uuid = uuid
        self.temporada_uuid = temporada_uuid
        self.nome = nome
        self.simulador = simulador
        self.dia_da_semana = dia_da_semana
        self.link_onboard = link_onboard

    def existe(self, cnx):
        select = "SELECT COUNT(*) FROM grids where nome = \'{}\'".format(self.nome)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            if out[0] == 0: return True
            return False

    def selecionar(self):
        return "SELECT BIN_TO_UUID(uuid), BIN_TO_UUID(temporada_uuid), nome, simulador, dia_da_semana, link_onboard " \
               "FROM grid WHERE BIN_TO_UUID(uuid) = \'{uuid}\'".format(uuid=self.uuid)

    def criar(self):
        return "INSERT INTO grid VALUES (UUID_TO_BIN(\'{uuid}\'), UUID_TO_BIN(\'{temporada_uuid}\'), \'{nome}\', \'{simulador}\'," \
               " \'{dia_da_semana}\', \'{link_onboard}\')".format(uuid=self.uuid, temporada_uuid=self.temporada_uuid,
                                                                  nome=self.nome, simulador=self.simulador,
                                                                  dia_da_semana=self.dia_da_semana,
                                                                  link_onboard=self.link_onboard)

    def atualizar(self):
        return "UPDATE grid SET temporada_uuid=UUID_TO_BIN(\'{temporada_uuid}\'), nome=\'{nome}\', simulador=\'{simulador}\'," \
               " dia_da_semana=\'{dia_da_semana}\', link_onboard=\'{link_onboard}\' WHERE BIN_TO_UUID(uuid) = \'{uuid}\'".format(
            uuid=self.uuid, temporada_uuid=self.temporada_uuid, nome=self.nome, simulador=self.simulador,
            dia_da_semana=self.dia_da_semana,
            link_onboard=self.link_onboard)

    def set_informacoes(self, lista):
        self.temporada_uuid = lista[1]
        self.nome = lista[2]
        self.simulador = lista[3]
        self.dia_da_semana = lista[4]
        self.link_onboard = lista[5]

    def pontuacao_piloto(self, cnx):
        select = "SELECT eq.nome, pi.nome, SUM(po.pontos) FROM pontuacao po, pilotos pi, etapas et, temporadas te, grids gr, " \
                 "equipes eq, piloto_equipe_temporada pet, baterias ba WHERE ba.etapa_id = et.id and po.bateria_id = ba.id and " \
                 "et.temporada_id = te.id and et.grid_id = gr.id and po.piloto_id = pi.id and pet.piloto_id = pi.id and pet.equipe_id = eq.id " \
                 "and pet.temporada_id = te.id and gr.id = {} group by eq.nome, pi.nome order by sum(pontos) desc".format(
            self.id)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchall()
            lista = self.add_posicao(out)
            retorno = []
            for linha in lista:
                retorno.append(self.serialize_pontuacao(linha))
            return retorno

    def add_posicao(self, lst):
        posicao = 1
        retorno = []
        for linha in lst:
            row = [posicao]
            for data in linha:
                row.append(data)
            retorno.append(row)
        return retorno

    def serialize(self):
        return {
            "uuid": self.uuid,
            "temporada_uuid": self.temporada_uuid,
            "nome": self.nome,
            "simulador": self.simulador,
            "diaDaSemana": self.dia_da_semana,
            "linkOnboard": self.link_onboard
        }

    def serialize_pontuacao(self, lst):
        posicao = lst[0]
        equipe = lst[1]
        piloto = lst[2]
        pontos = lst[3]
        return {
            "posicao": posicao,
            "equipe": equipe,
            "piloto": piloto,
            "pontos": pontos
        }
