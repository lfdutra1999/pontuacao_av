class Pista:
    def __init__(self, uuid, nome=None, pais=None, imagem=None):
        self.uuid = uuid
        self.nome = nome
        self.pais = pais
        self.imagem = imagem

    def criar(self):
        return "INSERT INTO pista (uuid, nome, pais) VALUES (UUID_TO_BIN(\'{uuid}\'), \'{nome}\', \'{pais}\')".format(
            uuid=self.uuid, nome=self.nome, pais=self.pais)

    def atualizar(self):
        return "UPDATE pista SET nome=\'{nome}\', pais=\'{pais}\' where BIN_TO_UUID(uuid) = \'{uuid}\'".format(
            uuid=self.uuid, nome=self.nome, pais=self.pais)

    def selecionar(self):
        return "SELECT BIN_TO_UUID(uuid), nome, pais, imagem FROM pista WHERE  BIN_TO_UUID(uuid) = \'{uuid}\'".format(
            uuid=self.uuid)

    def upload_imagem(self, imagem):
        return "UPDATE pista set imagem=\'{imagem}\' WHERE BIN_TO_UUID(uuid) = \'{uuid}\'".format(imagem=imagem,
                                                                                                  uuid=self.uuid)

    def set_informacoes(self, lista):
        self.nome = lista[1]
        self.pais = lista[2]
        self.imagem = lista[3]

    def serialize(self):
        return {
            "uuid": self.uuid,
            "nome": self.nome,
            "pais": self.pais,
            "imagem": self.imagem
        }
