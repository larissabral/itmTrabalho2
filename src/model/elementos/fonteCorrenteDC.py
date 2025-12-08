from src.model.elementos.elementoCircuito import ElementoCircuito


class FonteCorrenteDC(ElementoCircuito):
    def __init__(
        self,
        nome="",
        noPositivo=0,
        noNegativo=0,
        tipoFonte="DC",
        corrente=0,
        tempoAtual=0,
    ):
        super().__init__(nome, noPositivo, noNegativo)
        self.tipoFonte = tipoFonte
        self.corrente = corrente
        self.tempoAtual = tempoAtual

    def to_nl(self):
        return [
            self.nome,
            self.noPositivo,
            self.noNegativo,
            self.tipoFonte,
            self.corrente,
        ]  # nome: I

    def from_nl(self, nl):
        self.nome = nl[0]
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
        self.tipoFonte = nl[3]
        self.corrente = float(nl[4])
        return self

    def estampa(
        self, G, Ix, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
    ):
        noA = self.noPositivo
        noB = self.noNegativo
        corrente = self.corrente

        Ix[noA] -= corrente
        Ix[noB] += corrente

        return G, Ix, posicao
