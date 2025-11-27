class FonteCorrenteControladaCorrente:
    def __init__(
        self,
        noCorrentePositivo,
        noCorrenteNegativo,
        noControlePositivo,
        noControleNegativo,
        ganhoCorrente,
    ):
        self.noCorrentePositivo = noCorrentePositivo
        self.noCorrenteNegativo = noCorrenteNegativo
        self.noControlePositivo = noControlePositivo
        self.noControleNegativo = noControleNegativo
        self.ganhoCorrente = ganhoCorrente

    def to_nl(self):
        return [
            "F",
            self.noCorrentePositivo,
            self.noCorrenteNegativo,
            self.noControlePositivo,
            self.noControleNegativo,
            self.ganhoCorrente,
        ]

    def from_nl(self, nl):
        self.noCorrentePositivo = int(nl[1])
        self.noCorrenteNegativo = int(nl[2])
        self.noControlePositivo = int(nl[3])
        self.noControleNegativo = int(nl[4])
        self.ganhoCorrente = int(nl[5])
