import numpy as np

from src.model.elementoCircuito import ElementoCircuito


class Diodo(ElementoCircuito):
    def __init__(self, noPositivo, noNegativo):
        super().__init__(noPositivo, noNegativo)

    def to_nl(self):
        return ["D", self.noPositivo, self.noNegativo]

    def from_nl(self, nl):
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])

    def estampa(
        self, G, I, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
    ):
        noA = self.noPositivo
        noB = self.noNegativo

        Is = 3.7751345e-14
        Vt = 25.0e-3

        tensao = tensoesAnteriores[noA] - tensoesAnteriores[noB]
        if tensao > 0.9:
            tensao = 0.9

        i = Is * np.exp(tensao / Vt)

        condutancia = i / Vt
        if condutancia == 0:
            G0 = np.inf
        else:
            G0 = 1.0 / condutancia

        resistencia = 1 / G0
        corrente = i - Is - (condutancia * tensao)

        G[noA, noA] += resistencia
        G[noA, noB] -= resistencia
        G[noB, noA] -= resistencia
        G[noB, noB] += resistencia

        I[noA] -= corrente
        I[noB] += corrente
