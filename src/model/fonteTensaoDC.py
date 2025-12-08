from src.model.elementoCircuito import ElementoCircuito


class FonteTensaoDC(ElementoCircuito):
    def __init__(self, nome="", noPositivo=0, noNegativo=0, tipoFonte="DC", tensao=0):
        super().__init__(nome, noPositivo, noNegativo)
        self.tipoFonte = tipoFonte
        self.tensao = tensao

    def to_nl(self):
        return [
            self.nome,
            self.noPositivo,
            self.noNegativo,
            self.tipoFonte,
            self.tensao,
        ]  # nome: V

    def from_nl(self, nl):
        self.nome = nl[0]
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
        self.tipoFonte = nl[3]
        self.tensao = float(nl[4])
        return self

    def estampa(
        self, G, Ix, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
    ):
        tensao = self.tensao
        noA = self.noPositivo
        noB = self.noNegativo

        posicao += 1

        G[noA, qntNos + posicao] += 1
        G[qntNos + posicao, noA] -= 1
        G[noB, qntNos + posicao] -= 1
        G[qntNos + posicao, noB] += 1

        Ix[qntNos + posicao] -= tensao

        return G, Ix, posicao
