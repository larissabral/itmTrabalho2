from src.model.elementoCircuito import ElementoCircuito


class Indutor(ElementoCircuito):
    def __init__(
        self,
        nome="",
        noPositivo=0,
        noNegativo=0,
        indutancia=0,
        correnteInicial=0,
        isTemporal=True,
    ):
        super().__init__(nome, noPositivo, noNegativo)
        self.indutancia = indutancia
        self.correnteInicial = correnteInicial
        self.isTemporal = isTemporal

    def to_nl(self):
        return [
            self.nome,  # nome: L
            self.noPositivo,
            self.noNegativo,
            self.indutancia,
            "IC=" + self.correnteInicial.__str__(),
        ]

    def from_nl(self, nl):
        self.nome = nl[0]
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
        self.indutancia = float(nl[3])
        if len(nl) == 5:
            self.correnteInicial = float(nl[4].replace("IC=", ""))

    def estampa(
        self, G, Ix, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
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
        Ix[posicao] += i_t0

        return G, Ix, posicao
