class AmpOpIdeal:
    def __init__(self, noControlePositivo, noControleNegativo, noSaida):
        self.noControlePositivo = noControlePositivo
        self.noControleNegativo = noControleNegativo
        self.noSaida = noSaida

    def to_nl(self):
        return ["O", self.noControlePositivo, self.noControleNegativo, self.noSaida]

    def from_nl(self, nl):
        self.noControlePositivo = int(nl[1])
        self.noControleNegativo = int(nl[2])
        self.noSaida = int(nl[3])
