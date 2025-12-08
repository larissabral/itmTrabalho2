from src.model.elementos.elementoCircuito import ElementoCircuito


class FonteTensaoControladaTensao(ElementoCircuito):
    def __init__(
        self,
        nome="",
        noTensaoPositivo=0,
        noTensaoNegativo=0,
        noControlePositivo=0,
        noControleNegativo=0,
        ganhoTensao=0,
    ):
        super().__init__(nome, noTensaoPositivo, noTensaoNegativo)
        self.noTensaoPositivo = noTensaoPositivo
        self.noTensaoNegativo = noTensaoNegativo
        self.noControlePositivo = noControlePositivo
        self.noControleNegativo = noControleNegativo
        self.ganhoTensao = ganhoTensao

    def to_nl(self):
        return [
            self.nome,  # nome: E
            self.noTensaoPositivo,
            self.noTensaoNegativo,
            self.noControlePositivo,
            self.noControleNegativo,
            self.ganhoTensao,
        ]

    def from_nl(self, nl):
        self.nome = nl[0]
        self.noTensaoPositivo = int(nl[1])
        self.noTensaoNegativo = int(nl[2])
        self.noControlePositivo = int(nl[3])
        self.noControleNegativo = int(nl[4])
        self.ganhoTensao = float(nl[5])
        return self

    def estampa(
        self, G, Ix, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
    ):
        noA = self.noTensaoPositivo
        noB = self.noTensaoNegativo
        noC = self.noControlePositivo
        noD = self.noControleNegativo

        posicao += 1

        ix = qntNos + posicao

        G[noA, ix] += 1
        G[noB, ix] -= 1
        G[ix, noA] -= 1
        G[ix, noB] += 1
        G[ix, noC] += self.ganhoTensao
        G[ix, noD] -= self.ganhoTensao

        return G, Ix, posicao
