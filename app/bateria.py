class Bateria:
    def __init__(self, nome, etapa_id=0, multiplicador=1):
        self.nome = nome
        self.etapa_id = etapa_id
        self.multiplicador = multiplicador
        self.id = None
        self.pontos = None

    def set_id(self, cnx):
        select = "SELECT id FROM baterias WHERE nome = \'{}\'".format(self.nome)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            self.id = out[0]

    def set_multiplicador(self, cnx):
        select = "SELECT multiplicador FROM baterias WHERE nome = \'{}\'".format(self.nome)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            self.multiplicador = out[0]

    def existe(self, cnx):
        select = "SELECT COUNT(*) FROM baterias where nome = \'{}\'".format(self.nome)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            if out[0] == 0: return True
            return False

    def criar(self, cnx):
        if self.existe(cnx):
            insert = "INSERT INTO baterias(nome, etapa_id, multiplicador) VALUES (\'{}\', {}, {})".format(
                self.nome,
                self.etapa_id,
                self.multiplicador)
            with cnx.cursor() as cur:
                cur.execute(insert)
                cnx.commit()
        else:
            self.set_multiplicador(cnx)
        self.set_id(cnx)
        self.pontos_bateria(cnx)

    def pontuacao(self, cnx, posicao, piloto_id):
        insert = "INSERT INTO pontuacao(bateria_id, posicao, piloto_id, pontos) VALUES ({}, {}, {}, {})".format(
            self.id,
            posicao,
            piloto_id,
            self.pontos[posicao - 1][1])
        with cnx.cursor() as cur:
            cur.execute(insert)
            cnx.commit()

    def pontos_bateria(self, cnx):
        select = "SELECT gp.posicao, gp.pontos*e.multiplicador*{} FROM grid_pontos gp, etapas e, baterias b where gp.grid_id = e.grid_id " \
                 "and e.id = b.etapa_id and b.id = {}".format(self.multiplicador, self.id)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchall()
            self.pontos = out

    def pontuacao_bateria(self, cnx):
        select = "SELECT po.posicao, pi.nome, eq.nome, po.pontos FROM pontuacao po, baterias ba, temporadas te, grids gr, pilotos pi, equipes eq, etapas et, " \
                 "piloto_equipe_temporada pet WHERE po.bateria_id = ba.id and et.temporada_id = te.id and et.grid_id = gr.id and po.piloto_id = pi.id " \
                 "and pi.id = pet.piloto_id and eq.id = pet.equipe_id and te.id = pet.temporada_id and ba.etapa_id = et.id and ba.id = {} order by po.posicao".format(self.id)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchall()
            retorno = []
            for linha in out:
                retorno.append(self.serialize_pontuacao(linha))
            return retorno

    def serialize_pontuacao(self, list):
        posicao = list[0]
        nome = list[1]
        equipe = list[2]
        pontos = list[3]
        return {
            "posicao": posicao,
            "nome": nome,
            "equipe": equipe,
            "pontos": pontos
        }
