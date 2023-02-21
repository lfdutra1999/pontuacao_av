class Piloto:
    def __init__(self, nome, steam_id=""):
        self.nome = nome
        self.steam_id = steam_id

    def set_id(self, cnx):
        select = "SELECT id FROM pilotos WHERE nome = \'{}\'".format(self.nome)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            self.id = out[0]

    def set_steam_id(self, cnx):
        select = "SELECT steam_id FROM pilotos WHERE nome = \'{}\'".format(self.nome)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            self.steam_id = out[0]

    def existe(self, cnx):
        select = "SELECT COUNT(*) FROM pilotos where nome = \'{}\'".format(self.nome)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            if out[0] == 0: return True
            return False

    def criar(self, cnx):
        if self.existe(cnx):
            sql = "INSERT INTO pilotos (nome, steam_id) VALUES (\'{}\', \'{}\')".format(self.nome, self.set_steam_id())
            with cnx.cursor() as cur:
                cur.execute(sql)
                cnx.commit()
        else:
            self.set_steam_id(cnx)
        self.set_id(cnx)

    def serialize(self):
        return {
            "Id": self.id,
            "Nome": self.nome,
            "Steam_id": self.steam_id
        }