from src.model.elementos.elementoCircuito import ElementoCircuito


class Capacitor(ElementoCircuito):
    def __init__(
        self,
        nome="",
        noPositivo=0,
        noNegativo=0,
        capacitancia=0,
        tensaoInicial=0,
        isTemporal=True,
    ):
        super().__init__(nome, noPositivo, noNegativo)
        self.capacitancia = capacitancia
        self.tensaoInicial = tensaoInicial
        self.isTemporal = isTemporal

    def to_nl(self):
        return [
            self.nome,  # nome: C
            self.noPositivo,
            self.noNegativo,
            self.capacitancia,
            "IC=" + self.tensaoInicial.__str__(),
        ]

    def from_nl(self, nl):
        self.nome = nl[0]
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
        self.capacitancia = float(nl[3])
        if len(nl) == 5:
            self.tensaoInicial = float(nl[4].replace("IC=", ""))
        return self

    def estampa(
        self, G, Ix, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
    ):
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

        Ix[noA] += corrente
        Ix[noB] -= corrente

        return G, Ix, posicao
