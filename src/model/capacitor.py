from src.model.elementoCircuito import ElementoCircuito


class Capacitor(ElementoCircuito):
    def __init__(self, noPositivo, noNegativo, capacitancia, tensaoInicial):
        super().__init__(noPositivo, noNegativo)
        self.capacitancia = capacitancia
        self.tensaoInicial = tensaoInicial

    def to_nl(self):
        return [
            "C",
            self.noPositivo,
            self.noNegativo,
            self.capacitancia,
            "IC=" + self.tensaoInicial,
        ]

    def from_nl(self, nl):
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
        self.capacitancia = float(nl[3])
        self.tensaoInicial = float(nl[4].replace("IC=", ""))

    def estampa(self, G, I, deltaT, tensoesAnteriores, correntesAnteriores):
        noA = self.noPositivo
        noB = self.noNegativo
        capacitancia_equivalente = self.capacitancia / deltaT
        corrente = capacitancia_equivalente * (
            tensoesAnteriores[noA] - tensoesAnteriores[noB]
        )

        G[noA, noA] += capacitancia_equivalente
        G[noA, noB] -= capacitancia_equivalente
        G[noB, noA] -= capacitancia_equivalente
        G[noB, noB] += capacitancia_equivalente

        I[noA] += corrente
        I[noB] -= corrente
