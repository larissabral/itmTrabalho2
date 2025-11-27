class FonteTensaoControladaCorrente:
    def __init__(
        self,
        noTensaoPositivo,
        noTensaoNegativo,
        noControlePositivo,
        noControleNegativo,
        transresistencia,
    ):
        self.noTensaoPositivo = noTensaoPositivo
        self.noTensaoNegativo = noTensaoNegativo
        self.noControlePositivo = noControlePositivo
        self.noControleNegativo = noControleNegativo
        self.transresistencia = transresistencia

    def to_nl(self):
        return [
            "H",
            self.noTensaoPositivo,
            self.noTensaoNegativo,
            self.noControlePositivo,
            self.noControleNegativo,
            self.transresistencia,
        ]

    def from_nl(self, nl):
        self.noTensaoPositivo = int(nl[1])
        self.noTensaoNegativo = int(nl[2])
        self.noControlePositivo = int(nl[3])
        self.noControleNegativo = int(nl[4])
        self.transresistencia = int(nl[5])
