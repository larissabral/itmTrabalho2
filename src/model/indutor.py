class Indutor:
    def __init__(self, noPositivo, noNegativo, indutancia, correnteInicial):
        self.noPositivo = noPositivo
        self.noNegativo = noNegativo
        self.indutancia = indutancia
        self.correnteInicial = correnteInicial

    def to_nl(self):
        return [
            "L",
            self.noPositivo,
            self.noNegativo,
            self.indutancia,
            "IC=" + self.correnteInicial,
        ]

    def from_nl(self, nl):
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
        self.indutancia = float(nl[3])
        self.correnteInicial = float(nl[4].replace("IC=", ""))
