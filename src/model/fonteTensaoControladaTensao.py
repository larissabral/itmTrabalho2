class FonteTensaoControladaTensao:
    def __init__(
        self,
        noTensaoPositivo,
        noTensaoNegativo,
        noControlePositivo,
        noControleNegativo,
        ganhoTensao,
    ):
        self.noTensaoPositivo = noTensaoPositivo
        self.noTensaoNegativo = noTensaoNegativo
        self.noControlePositivo = noControlePositivo
        self.noControleNegativo = noControleNegativo
        self.ganhoTensao = ganhoTensao

    def to_nl(self):
        return [
            "E",
            self.noTensaoPositivo,
            self.noTensaoNegativo,
            self.noControlePositivo,
            self.noControleNegativo,
            self.ganhoTensao,
        ]

    def from_nl(self, nl):
        self.noTensaoPositivo = int(nl[1])
        self.noTensaoNegativo = int(nl[2])
        self.noControlePositivo = int(nl[3])
        self.noControleNegativo = int(nl[4])
        self.ganhoTensao = int(nl[5])
