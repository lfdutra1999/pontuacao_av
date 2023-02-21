class Grid:
    def __init__(self, nome, simulador="", pontos=0):
        self.nome = nome
        self.simulador = simulador
        self.pontos = pontos

    def set_id(self, cnx):
        select = "SELECT id FROM grids WHERE nome = \'{}\'".format(self.nome)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            self.id = out[0]

    def existe(self, cnx):
        select = "SELECT COUNT(*) FROM grids where nome = \'{}\'".format(self.nome)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            if out[0] == 0: return True
            return False

    def criar(self, cnx):
        if self.existe(cnx):
            insert = "INSERT INTO grids (nome, simulador) VALUES (\'{}\', \'{}\')".format(self.nome, self.simulador)
            with cnx.cursor() as cur:
                cur.execute(insert)
                cnx.commit()
            self.set_id(cnx)
            valores = ""
            for ponto in self.pontos:
                if ponto[0] == 1:
                    valores = "({}, {}, {})".format(self.id, ponto[0], ponto[1])
                else:
                    valores += ",({}, {}, {})".format(self.id, ponto[0], ponto[1])
            insert = "INSERT INTO grid_pontos(grid_id, posicao, pontos) VALUES {}".format(valores)
            with cnx.cursor() as cur:
                cur.execute(insert)
                cnx.commit()
        self.set_id(cnx)

    def pontuacao_piloto(self, cnx):
        select = "SELECT eq.nome, pi.nome, SUM(po.pontos) FROM pontuacao po, pilotos pi, etapas et, temporadas te, grids gr, " \
                 "equipes eq, piloto_equipe_temporada pet, baterias ba WHERE ba.etapa_id = et.id and po.bateria_id = ba.id and " \
                 "et.temporada_id = te.id and et.grid_id = gr.id and po.piloto_id = pi.id and pet.piloto_id = pi.id and pet.equipe_id = eq.id " \
                 "and pet.temporada_id = te.id and gr.id = {} group by eq.nome, pi.nome order by sum(pontos) desc".format(self.id)
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
