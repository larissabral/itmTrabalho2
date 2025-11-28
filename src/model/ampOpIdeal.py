from src.model.elementoCircuito import ElementoCircuito


class AmpOpIdeal(ElementoCircuito):
    def __init__(self, noPositivo, noNegativo, noSaida):
        super().__init__(noPositivo, noNegativo)
        self.noSaida = noSaida

    def to_nl(self):
        return ["O", self.noPositivo, self.noNegativo, self.noSaida]

    def from_nl(self, nl):
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
        self.noSaida = int(nl[3])

    def estampa(self, G, I, deltaT, tensoesAnteriores, correntesAnteriores):
        # TODO: implementar estampa do ampop
        raise NotImplementedError
