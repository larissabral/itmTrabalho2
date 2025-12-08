from src.model.elementos.elementoCircuito import ElementoCircuito


class Resistor(ElementoCircuito):
    def __init__(self, nome="", resistencia=0, noPositivo=0, noNegativo=0):
        super().__init__(nome, noPositivo, noNegativo)
        self.resistencia = resistencia

    def to_nl(self):
        return [
            self.nome,
            self.noPositivo,
            self.noNegativo,
            self.resistencia,
        ]  # nome: R

    def from_nl(self, nl):
        self.nome = nl[0]
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
        self.resistencia = float(nl[3])
        return self

    def estampa(
        self, G, Ix, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
    ):
        noA = self.noPositivo
        noB = self.noNegativo
        condutancia = 1 / self.resistencia

        G[noA, noA] += condutancia
        G[noA, noB] -= condutancia
        G[noB, noA] -= condutancia
        G[noB, noB] += condutancia

        return G, Ix, posicao
