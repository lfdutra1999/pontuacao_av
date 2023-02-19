class Piloto:
    def __init__(self, nome):
        self.nome = nome
        # self.steam_id = steam_id

    def set_id(self, cnx):
        select = "SELECT id FROM pilotos WHERE nome = \'{}\'".format(self.nome)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            self.id = out[0]

    def existe(self, cnx):
        select = "SELECT COUNT(*) FROM pilotos where nome = \'{}\'".format(self.nome)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            if out[0] == 0: return True
            return False

    def criar(self, cnx):
        if self.existe(cnx):
            sql = "INSERT INTO pilotos (nome) VALUES (\'{}\')".format(self.nome)
            with cnx.cursor() as cur:
                cur.execute(sql)
                cnx.commit()
        self.set_id(cnx)