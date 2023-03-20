class Temporada:
    def __init__(self, uuid, nome=None, dt_inicio=None, dt_fim=None):
        self.uuid = uuid
        self.nome = nome
        self.dt_inicio = dt_inicio
        self.dt_fim = dt_fim

    def existe(self, cnx):
        select = "SELECT COUNT(*) FROM temporadas where BIN_TO_UUID(uuid) = \'{}\'".format(self.uuid)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            if out[0] == 0: return True
            return False

    def criar(self):
        return "INSERT INTO temporada VALUES (UUID_TO_BIN(\'{uuid}\'), \'{nome}\', DATE_FORMAT(\'{dt_inicio}\', \"%Y-%m-%d\"), DATE_FORMAT(\'{dt_fim}\', \"%Y-%m-%d\"))".format(
            uuid=self.uuid, nome=self.nome, dt_inicio=self.dt_inicio, dt_fim=self.dt_fim)

    def select(self):
        return "SELECT BIN_TO_UUID(uuid), nome,  DATE_FORMAT(dtInicio, \"%Y-%m-%d\"), DATE_FORMAT(dtFim, \"%Y-%m-%d\") from temporada where BIN_TO_UUID(uuid) = \'{uuid}\'".format(
            uuid=self.uuid)

    def set_informacoes(self, lista):
        self.nome = lista[1]
        self.dt_inicio = lista[2]
        self.dt_fim = lista[3]

    def relacionar_piloto_equipe(self, cnx, piloto_id, equipe_id):
        insert = "INSERT INTO piloto_equipe_temporada(equipe_id, piloto_id, temporada_id) VALUES ({}, {}, {})".format(
            equipe_id, piloto_id, self.id)
        with cnx.cursor() as cur:
            cur.execute(insert)
            cnx.commit()

    def pontos_equipe(self, cnx):
        select = "SELECT eq.nome, sum(po.pontos) FROM pontuacao po, equipes eq, etapas et, temporadas te, pilotos pi, piloto_equipe_temporada pet, baterias ba " \
                 "WHERE po.bateria_id = ba.id AND po.piloto_id = pi.id AND et.temporada_id = te.id AND pet.equipe_id = eq.id AND pet.piloto_id = pi.id " \
                 "AND ba.etapa_id = et.id AND pet.temporada_id = te.id AND te.id = {} group by eq.nome order by sum(po.pontos) desc".format(
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
            "nome": self.nome,
            "dtInicio": self.dt_inicio,
            "dtFim": self.dt_fim
        }
