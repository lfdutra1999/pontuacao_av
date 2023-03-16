class Pilotos:
    def __init__(self, pilotos=None):
        self.pilotos = pilotos

    def select_pilotos(self):
        return "SELECT BIN_TO_UUID(uuid), username, isAdmin FROM piloto"

    def set_pilotos(self, pilotos):
        self.pilotos = pilotos

    def serialize(self):
        pilotos = []
        for piloto in self.pilotos:
            pilotos.append(
                {
                    "uuid": piloto[0],
                    "username": piloto[1],
                    "isAdmin": piloto[2]
                }
            )
        return pilotos