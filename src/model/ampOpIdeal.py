from src.model.elementoCircuito import ElementoCircuito


class AmpOpIdeal(ElementoCircuito):
    def __init__(self, nome, noPositivo, noNegativo, noSaida):
        super().__init__(nome, noPositivo, noNegativo)
        self.noSaida = noSaida

    def to_nl(self):
        return [self.nome, self.noPositivo, self.noNegativo, self.noSaida]  # nome: O

    def from_nl(self, nl):
        self.nome = nl[0]
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
        self.noSaida = int(nl[3])

    def estampa(
        self, G, Ix, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
    ):
        noA = self.noPositivo
        noB = self.noNegativo
        noC = self.noSaida

        G[0][posicao] -= 1
        G[noC][posicao] += 1
        G[posicao][noA] -= 1
        G[posicao][noB] += 1
