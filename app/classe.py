class Classe:
    def __init__(self, uuid, nome=None):
        self.uuid = uuid
        self.nome = nome
        self.imagem = None

    def criar(self):
        return "INSERT INTO classe VALUES (UUID_TO_BIN(\'{uuid}\'), \'{nome}\')".format(uuid=self.uuid, nome=self.nome)

    def atualizar(self):
        return "UPDATE classe SET nome=\'{nome}\' where BIN_TO_UUID(uuid) = \'{uuid}\'".format(uuid=self.uuid,
                                                                                               nome=self.nome)
    def selecionar(self):
        return "SELECT BIN_TO_UUID(uuid), nome, imagem FROM classe WHERE  BIN_TO_UUID(uuid) = \'{uuid}\'".format(uuid=self.uuid)

    def upload_imagem(self, imagem):
        return "UPDATE classe set imagem=\'{imagem}\' WHERE BIN_TO_UUID(uuid) = \'{uuid}\'".format(imagem=imagem, uuid=self.uuid)

    def set_informacoes(self, lista):
        self.nome = lista[1]
        self.imagem = lista[2]

    def serialize(self):
        return {
            "uuid": self.uuid,
            "nome": self.nome,
            "imagem": self.imagem
        }
