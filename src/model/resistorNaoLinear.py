import numpy as np

from src.model.elementoCircuito import ElementoCircuito


class ResistorNaoLinear(ElementoCircuito):
    def __init__(self, nome, noPositivo, noNegativo, v1, v2, v3, v4, i1, i2, i3, i4):
        super().__init__(nome, noPositivo, noNegativo)
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4
        self.i1 = i1
        self.i2 = i2
        self.i3 = i3
        self.i4 = i4

    def to_nl(self):
        return [
            self.nome,  # nome: N
            self.noPositivo,
            self.noNegativo,
            self.v1,
            self.i1,
            self.v2,
            self.i2,
            self.v3,
            self.i3,
            self.v4,
            self.i4,
        ]

    def from_nl(self, nl):
        self.nome = nl[0]
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
        self.v1 = float(nl[3])
        self.i1 = float(nl[4])
        self.v2 = float(nl[5])
        self.i2 = float(nl[6])
        self.v3 = float(nl[7])
        self.i3 = float(nl[8])
        self.v4 = float(nl[9])
        self.i4 = float(nl[10])

    def estampa(
        self, G, I, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
    ):
        noA = self.noPositivo
        noB = self.noNegativo
        G0 = 0
        I0 = 0

        tensao = tensoesAnteriores[noA] - tensoesAnteriores[noB]

        if tensao > self.v3:
            G0 = (self.i4 - self.i3) / (self.v4 - self.v3)
            I0 = self.i4 - self.v4

        if self.v2 < tensao <= self.v3:
            G0 = (self.i3 - self.i2) / (self.v3 - self.v2)
            I0 = self.i3 - self.v3

        if tensao <= self.v2:
            G0 = (self.i2 - self.i1) / (self.v2 - self.v1)
            I0 = self.i2 - self.v2

        if G0 == 0:
            resistencia = np.inf
        else:
            resistencia = 1 / G0

        G[noA, noA] += resistencia
        G[noA, noB] -= resistencia
        G[noB, noA] -= resistencia
        G[noB, noB] += resistencia

        I[noA] += I0
        I[noB] -= I0
