class Equipe:
    def __init__(self, nome):
        self.id = None
        self.nome = nome

    def set_id(self, cnx):
        select = "SELECT id FROM equipes WHERE nome = \'{}\'".format(self.nome)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            self.id = out[0]

    def existe(self, cnx):
        select = "SELECT COUNT(*) FROM equipes where nome = \'{}\'".format(self.nome)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            if out[0] == 0: return True
            return False

    def criar(self, cnx):
        if self.existe(cnx):
            insert = "INSERT INTO equipes(nome) VALUES (\'{}\')".format(self.nome)
            with cnx.cursor() as cur:
                cur.execute(insert)
                cnx.commit()
        self.set_id(cnx)

    def serialize(self):
        return {
            "id": self.id,
            "nome": self.nome
        }