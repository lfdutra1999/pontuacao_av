class Categoria:
    def __init__(self, uuid, grid_uuid, nome=None, horario=None):
        self.uuid = uuid
        self.grid_uuid = grid_uuid
        self.nome = nome
        self.horario = horario

    def criar(self):
        return "INSERT INTO categoria  VALUES (UUID_TO_BIN(\'{uuid}\'), UUID_TO_BIN(\'{grid_uuid}\'), \'{nome}\', \'{horario}\')".format(
            uuid=self.uuid, grid_uuid=self.grid_uuid, nome=self.nome, horario=self.horario)

    def atualizar(self):
        return "UPDATE categoria SET nome=\'{nome}\', horario=\'{horario}\' where BIN_TO_UUID(uuid) = \'{uuid}\'".format(
            uuid=self.uuid, nome=self.nome, horario=self.horario)

    def selecionar(self):
        return "SELECT BIN_TO_UUID(uuid), BIN_TO_UUID(grid_uuid),nome, horario FROM categoria WHERE BIN_TO_UUID(uuid) = \'{uuid}\'".format(
            uuid=self.uuid)

    # def upload_imagem(self, imagem):
    #     return "UPDATE categoria set imagem=\'{imagem}\' WHERE BIN_TO_UUID(uuid) = \'{uuid}\'".format(imagem=imagem,
    #                                                                                               uuid=self.uuid)

    def set_informacoes(self, lista):
        self.nome = lista[2]
        self.horario = lista[3]


    def serialize(self):
        return {
            "uuid": self.uuid,
            "gridUuid": self.grid_uuid,
            "nome": self.nome,
            "horario": self.horario
        }
