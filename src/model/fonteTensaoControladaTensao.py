from src.model.elementoCircuito import ElementoCircuito


class FonteTensaoControladaTensao(ElementoCircuito):
    def __init__(
        self,
        noTensaoPositivo,
        noTensaoNegativo,
        noControlePositivo,
        noControleNegativo,
        ganhoTensao,
    ):
        super().__init__(noTensaoPositivo, noTensaoNegativo)
        self.noTensaoPositivo = noTensaoPositivo
        self.noTensaoNegativo = noTensaoNegativo
        self.noControlePositivo = noControlePositivo
        self.noControleNegativo = noControleNegativo
        self.ganhoTensao = ganhoTensao

    def to_nl(self):
        return [
            "E",
            self.noTensaoPositivo,
            self.noTensaoNegativo,
            self.noControlePositivo,
            self.noControleNegativo,
            self.ganhoTensao,
        ]

    def from_nl(self, nl):
        self.noTensaoPositivo = int(nl[1])
        self.noTensaoNegativo = int(nl[2])
        self.noControlePositivo = int(nl[3])
        self.noControleNegativo = int(nl[4])
        self.ganhoTensao = int(nl[5])

    def estampa(
        self, G, I, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
    ):
        noA = self.noTensaoPositivo
        noB = self.noTensaoNegativo
        noC = self.noControlePositivo
        noD = self.noControleNegativo
        ix = qntNos + posicao

        G[noA, ix] += 1
        G[noB, ix] -= 1
        G[ix, noA] -= 1
        G[ix, noB] += 1
        G[ix, noC] += self.ganhoTensao
        G[ix, noD] -= self.ganhoTensao
