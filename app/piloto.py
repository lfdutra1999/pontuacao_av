class Piloto:
    def __init__(self, uuid, username=None, password=None, nome=None, sobrenome=None, nickname=None, steamid=None,
                 whatsapp=None, chavepíx=None, cidade=None, estado=None,
                 controlador=None, linkcanal=None, isAdmin=0):
        self.uuid = uuid
        self.username = username
        self.password = password
        self.nome = nome
        self.sobrenome = sobrenome
        self.nickname = nickname
        self.steamid = steamid
        self.whatsapp = whatsapp
        self.chavepix = chavepíx
        if cidade != '' and cidade is not None:
            self.cidade = cidade
        else:
            self.cidade = None
        if estado != '' and estado is not None:
            self.estado = estado
        else:
            self.estado = None
        if controlador != '' and controlador is not None:
            self.controlador = controlador
        else:
            self.controlador = None
        if linkcanal != '' and linkcanal is not None:
            self.linkcanal = linkcanal
        else:
            self.linkcanal = None
        self.isAdmin = isAdmin
        self.foto = None

    def set_informacoes(self, out):
        self.nome = out[0]
        self.sobrenome = out[1]
        self.nickname = out[2]
        self.steamid = out[3]
        self.whatsapp = out[4]
        self.chavepix = out[5]
        if out[6] is not None: self.cidade = out[6]
        if out[7] is not None: self.estado = out[7]
        if out[8] is not None: self.controlador = out[8]
        if out[9] is not None: self.linkcanal = out[9]

    def cadastrar_informacoes(self, nome=None, sobrenome=None, nickname=None, steamid=None, whatsapp=None,
                              chavepíx=None, cidade=None, estado=None,
                              controlador=None, linkcanal=None):
        self.nome = nome
        self.sobrenome = sobrenome
        self.nickname = nickname
        self.steamid = steamid
        self.whatsapp = whatsapp
        self.chavepix = chavepíx
        if cidade != '' and cidade is not None: self.cidade = cidade
        if estado != '' and estado is not None: self.estado = estado
        if controlador != '' and controlador is not None: self.controlador = controlador
        if linkcanal != '' and linkcanal is not None: self.linkcanal = linkcanal

    def select_informacoes(self):
        return "SELECT nome, sobrenome, nickname, steamid, whatsapp, chavepix, cidade, estado, controlador, linkcanal " \
               "FROM piloto_informacoes WHERE piloto_uuid = UUID_TO_BIN(\'{}\')".format(self.uuid)

    def existe(self, cnx):
        select = "SELECT COUNT(*) FROM piloto where uuid = UUID_TO_BIN(\'{}\')".format(self.uuid)
        with cnx.cursor() as cur:
            cur.execute(select)
            out = cur.fetchone()
            if out[0] == 0: return True
            return False

    def criar(self):
        return ["INSERT INTO piloto VALUES (UUID_TO_BIN(\'{uuid}\'), \'{username}\', \'{password}\', {isAdmin})".format(
            uuid=self.uuid,
            username=self.username,
            password=self.password,
            isAdmin=self.isAdmin),
            "INSERT INTO piloto_informacoes (piloto_uuid, nome, sobrenome, nickname, steamid, whatsapp, chavepix, cidade," \
            "estado, controlador, linkcanal) VALUES (UUID_TO_BIN(\'{piloto_uuid}\'), \'{nome}\', \'{sobrenome}\', \'{nickname}\'," \
            " \'{steamid}\', \'{whatsapp}\', \'{chavepix}\', {cidade}, {estado}, {controlador}, {linkcanal})".format(
                piloto_uuid=self.uuid,
                nome=self.nome,
                sobrenome=self.sobrenome,
                nickname=self.nickname,
                steamid=self.steamid,
                whatsapp=self.whatsapp,
                chavepix=self.chavepix,
                cidade="\'{}\'".format(self.cidade) if self.cidade is not None else "Null",
                estado="\'{}\'".format(self.estado) if self.estado is not None else "NULL",
                controlador="\'{}\'".format(self.controlador) if self.controlador is not None else "NULL",
                linkcanal="\'{}\'".format(self.linkcanal) if self.linkcanal is not None else "NULL")
        ]

    def atualiza_info(self, coluna, valor):
        return "UPDATE piloto_informacoes set {coluna}=\'{valor}\'".format(coluna=coluna, valor=valor)

    def serialize(self):
        return {
            "uuid": self.uuid,
            "nome": self.nome,
            "sobrenome": self.sobrenome,
            "nickname": self.nickname,
            "steamid": self.steamid,
            "whatsapp": self.whatsapp,
            "chavepix": self.chavepix,
            "cidade": self.cidade,
            "estado": self.estado,
            "controlador": self.controlador,
            "linkcanal": self.linkcanal,
            "foto": self.foto
        }
