class Resistor:
    def __init__(self, resistencia, noPositivo, noNegativo):
        self.resistencia = resistencia
        self.noPositivo = noPositivo
        self.noNegativo = noNegativo

    def to_nl(self):
        return ["R", self.noPositivo, self.noNegativo, self.resistencia]

    def from_nl(self, nl):
        self.resistencia = float(nl[3])
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
