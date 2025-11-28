from src.model.elementoCircuito import ElementoCircuito


class Indutor(ElementoCircuito):
    def __init__(self, noPositivo, noNegativo, indutancia, correnteInicial):
        super().__init__(noPositivo, noNegativo)
        self.indutancia = indutancia
        self.correnteInicial = correnteInicial

    def to_nl(self):
        return [
            "L",
            self.noPositivo,
            self.noNegativo,
            self.indutancia,
            "IC=" + self.correnteInicial,
        ]

    def from_nl(self, nl):
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
        self.indutancia = float(nl[3])
        self.correnteInicial = float(nl[4].replace("IC=", ""))

    def estampa(
        self, G, I, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
    ):
        noA = self.noPositivo
        noB = self.noNegativo

        indutancia_equivalente = self.indutancia / deltaT

        G[noA, posicao] += 1
        G[noB, posicao] -= 1
        G[posicao, noA] -= 1
        G[posicao, noB] += 1
        G[posicao, posicao] += indutancia_equivalente

        i_t0 = correntesAnteriores[posicao - qntNos] * indutancia_equivalente
        I[posicao] += i_t0
