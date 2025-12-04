from src.model.elementoCircuito import ElementoCircuito


class FonteCorrenteControladaCorrente(ElementoCircuito):
    def __init__(
        self,
        nome="",
        noCorrentePositivo=0,
        noCorrenteNegativo=0,
        noControlePositivo=0,
        noControleNegativo=0,
        ganhoCorrente=0,
    ):
        super().__init__(nome, noCorrentePositivo, noCorrenteNegativo)
        self.noCorrentePositivo = noCorrentePositivo
        self.noCorrenteNegativo = noCorrenteNegativo
        self.noControlePositivo = noControlePositivo
        self.noControleNegativo = noControleNegativo
        self.ganhoCorrente = ganhoCorrente

    def to_nl(self):
        return [
            self.nome,  # nome: F
            self.noCorrentePositivo,
            self.noCorrenteNegativo,
            self.noControlePositivo,
            self.noControleNegativo,
            self.ganhoCorrente,
        ]

    def from_nl(self, nl):
        self.nome = nl[0]
        self.noCorrentePositivo = int(nl[1])
        self.noCorrenteNegativo = int(nl[2])
        self.noControlePositivo = int(nl[3])
        self.noControleNegativo = int(nl[4])
        self.ganhoCorrente = int(nl[5])

    def estampa(
        self, G, Ix, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
    ):
        noA = self.noCorrentePositivo
        noB = self.noCorrenteNegativo
        noC = self.noControlePositivo
        noD = self.noControleNegativo

        posicao += 1

        ix = qntNos + posicao

        G[noA, ix] += self.ganhoCorrente
        G[noB, ix] -= self.ganhoCorrente
        G[noC, ix] += 1
        G[noD, ix] -= 1
        G[ix, noC] -= 1
        G[ix, noD] += 1

        return G, Ix, posicao
