from src.model.elementoCircuito import ElementoCircuito


class Resistor(ElementoCircuito):
    def __init__(self, resistencia, noPositivo, noNegativo):
        super().__init__(noPositivo, noNegativo)
        self.resistencia = resistencia

    def to_nl(self):
        return ["R", self.noPositivo, self.noNegativo, self.resistencia]

    def from_nl(self, nl):
        self.resistencia = float(nl[3])
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])

    def estampa(self, G, I, deltaT, tensoesAnteriores, correntesAnteriores):
        noA = self.noPositivo
        noB = self.noNegativo
        condutancia = 1 / self.resistencia

        G[noA, noA] += condutancia
        G[noA, noB] -= condutancia
        G[noB, noA] -= condutancia
        G[noB, noB] += condutancia
