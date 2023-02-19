class Temporada:
    def __init__(self, nome):
        self.nome = nome

    def set_id(self, cnx):
        select = "SELECT id FROM temporadas WHERE nome = \'{}\'".format(self.nome)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            self.id = out[0]

    def existe(self, cnx):
        select = "SELECT COUNT(*) FROM temporadas where nome = \'{}\'".format(self.nome)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            if out[0] == 0: return True
            return False

    def criar(self, cnx):
        if self.existe(cnx):
            insert = "INSERT INTO temporadas (nome) VALUES (\'{}\')".format(self.nome)
            with cnx.cursor() as cur:
                cur.execute(insert)
                cnx.commit()
        self.set_id(cnx)

    def relacionar_piloto_equipe(self, cnx, piloto_id, equipe_id):
        insert = "INSERT INTO piloto_equipe_temporada(equipe_id, piloto_id, temporada_id) VALUES ({}, {}, {})".format(
            equipe_id, piloto_id, self.id)
        with cnx.cursor() as cur:
            cur.execute(insert)
            cnx.commit()

    def pontos_equipe(self, cnx):
        select = "SELECT eq.nome, sum(po.pontos) FROM pontuacao po, equipes eq, etapas et, temporadas te, pilotos pi, piloto_equipe_temporada pet " \
                 "WHERE po.etapa_id = et.id AND po.piloto_id = pi.id AND et.temporada_id = te.id AND pet.equipe_id = eq.id AND pet.piloto_id = pi.id " \
                 "AND pet.temporada_id = te.id AND te.id = {} group by eq.nome order by sum(po.pontos) desc".format(self.id)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchall()
            return out
            #print("Equipe\tPontos")
            #print("-------------------------------")
            #for i in out:
            #    print("{}\t{}".format(i[0], i[1]))
