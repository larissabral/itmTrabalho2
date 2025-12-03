from src.model.elementoCircuito import ElementoCircuito


class FonteTensaoControladaCorrente(ElementoCircuito):
    def __init__(
        self,
        nome="",
        noTensaoPositivo=0,
        noTensaoNegativo=0,
        noControlePositivo=0,
        noControleNegativo=0,
        transresistencia=0,
    ):
        super().__init__(nome, noTensaoPositivo, noTensaoNegativo)
        self.noTensaoPositivo = noTensaoPositivo
        self.noTensaoNegativo = noTensaoNegativo
        self.noControlePositivo = noControlePositivo
        self.noControleNegativo = noControleNegativo
        self.transresistencia = transresistencia

    def to_nl(self):
        return [
            self.nome,  # nome: H
            self.noTensaoPositivo,
            self.noTensaoNegativo,
            self.noControlePositivo,
            self.noControleNegativo,
            self.transresistencia,
        ]

    def from_nl(self, nl):
        self.nome = nl[0]
        self.noTensaoPositivo = int(nl[1])
        self.noTensaoNegativo = int(nl[2])
        self.noControlePositivo = int(nl[3])
        self.noControleNegativo = int(nl[4])
        self.transresistencia = int(nl[5])

    def estampa(
        self, G, Ix, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
    ):
        noA = self.noTensaoPositivo
        noB = self.noTensaoNegativo
        noC = self.noControlePositivo
        noD = self.noControleNegativo
        ix = qntNos + posicao
        iy = qntNos + posicao + 1

        G[noA, iy] += 1
        G[noB, iy] -= 1
        G[noC, ix] += 1
        G[noD, ix] -= 1
        G[ix, noC] -= 1
        G[ix, noD] += 1
        G[iy, noA] -= 1
        G[iy, noB] += 1
        G[iy, ix] += self.transresistencia

        return G, Ix, posicao
