from src.model.elementoCircuito import ElementoCircuito


class Mosfet(ElementoCircuito):
    def __init__(
        self,
        nome,
        dreno,
        porta,
        fonte,
        tipoCanal,
        W,
        L,
        y,
        K,
        tensaoThevenin,
        noPositivo,
        noNegativo,
    ):
        super().__init__(nome, noPositivo, noNegativo)
        self.dreno = dreno
        self.porta = porta
        self.fonte = fonte
        self.tipoCanal = tipoCanal
        self.W = W
        self.L = L
        self.y = y
        self.K = K
        self.tensaoThevenin = tensaoThevenin

    def to_nl(self):
        return [
            self.nome,  # nome: M
            self.dreno,
            self.porta,
            self.fonte,
            self.tipoCanal,
            self.W,
            self.L,
            self.y,
            self.K,
            self.tensaoThevenin,
        ]

    def from_nl(self, nl):
        self.nome = nl[0]
        self.dreno = int(nl[1])
        self.porta = int(nl[2])
        self.fonte = int(nl[3])
        self.tipoCanal = int(nl[4])
        self.W = int(nl[5])
        self.L = int(nl[6])
        self.y = int(nl[7])
        self.K = int(nl[8])
        self.tensaoThevenin = int(nl[9])
        return self

    def estampa(
        self, G, Ix, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
    ):
        raise NotImplementedError
