class Etapa:
    def __init__(self, nome, grid_id, temporada_id):
        self.pontos = None
        self.id = None
        self.nome = nome
        self.grid_id = grid_id
        self.temporada_id = temporada_id
        self.multiplicador = 1

    def set_id(self, cnx):
        select = "SELECT id FROM etapas WHERE nome = \'{}\'".format(self.nome)
        print(select)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            self.id = out[0]

    def existe(self, cnx):
        select = "SELECT COUNT(*) FROM etapas where nome = \'{}\'".format(self.nome)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            print(out)
            if out[0] == 0: return True
            return False

    def criar(self, cnx):
        if self.existe(cnx):
            insert = "INSERT INTO etapas(nome, grid_id, temporada_id, multiplicador) VALUES (\'{}\', {}, {}, {})".format(
                self.nome,
                self.grid_id,
                self.temporada_id,
                self.multiplicador)
            with cnx.cursor() as cur:
                cur.execute(insert)
                cnx.commit()
        self.set_id(cnx)

    def pontuacao(self, cnx, posicao, piloto_id):
        insert = "INSERT INTO pontuacao(etapa_id, posicao, piloto_id, pontos) VALUES ({}, {}, {}, {})".format(
            self.id,
            piloto_id,
            posicao,
            self.pontos[posicao - 1][1])
        with cnx.cursor() as cur:
            cur.execute(insert)
            cnx.commit()

    def pontos_etapa(self, cnx):
        select = "SELECT posicao, pontos*{} FROM grid_pontos where grid_id = {}".format(self.multiplicador,
                                                                                        self.grid_id)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchall()
            self.pontos = out

    def print_pontuacao(self, cnx):
        select = "SELECT po.posicao, pi.nome, eq.nome, po.pontos FROM pontuacao po, etapas et, temporadas te, grids gr, pilotos pi, equipes eq, piloto_equipe_temporada pet " \
                 "WHERE po.etapa_id = et.id and et.temporada_id = te.id and et.grid_id = gr.id and po.piloto_id = pi.id and pi.id = pet.piloto_id and eq.id = pet.equipe_id and te.id = pet.temporada_id  " \
                 " and et.id = {} order by po.posicao".format(self.id)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchall()
            return out
            #print("Piloto\tEquipe\tPosicao\tPontos")
            #print("-------------------------------")
            #for i in out:
            #    print("{}\t{}\t{}\t{}".format(i[0], i[1], i[2], i[3]))
