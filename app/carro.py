class Carro:
    def __init__(self, uuid, classe_uuid, nome=None, imagem=None):
        self.uuid = uuid
        self.classe_uuid = classe_uuid
        self.nome = nome
        self.imagem = imagem

    def criar(self):
        return "INSERT INTO carro (uuid, classe_uuid,  nome) VALUES (UUID_TO_BIN(\'{uuid}\'), UUID_TO_BIN(\'{classe_uuid}\'), \'{nome}\')".format(
            uuid=self.uuid, classe_uuid=self.classe_uuid, nome=self.nome)

    def atualizar(self):
        return "UPDATE carro SET nome=\'{nome}\' where BIN_TO_UUID(uuid) = \'{uuid}\'".format(uuid=self.uuid,
                                                                                              nome=self.nome)

    def selecionar(self):
        return "SELECT BIN_TO_UUID(uuid), BIN_TO_UUID(classe_uuid), nome, imagem FROM classe WHERE  BIN_TO_UUID(uuid) = \'{uuid}\'".format(
            uuid=self.uuid)

    def upload_imagem(self, imagem):
        return "UPDATE carro set imagem=\'{imagem}\' WHERE BIN_TO_UUID(uuid) = \'{uuid}\'".format(imagem=imagem,
                                                                                                  uuid=self.uuid)

    def set_informacoes(self, lista):
        self.nome = lista[2]
        self.imagem = lista[3]

    def serialize(self):
        return {
            "uuid": self.uuid,
            "classeUuid": self.classe_uuid,
            "nome": self.nome,
            "imagem": self.imagem
        }
