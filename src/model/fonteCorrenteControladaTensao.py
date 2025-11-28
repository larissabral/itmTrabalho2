from src.model.elementoCircuito import ElementoCircuito


class FonteCorrenteControladaTensao(ElementoCircuito):
    def __init__(
        self,
        nome,
        noCorrentePositivo,
        noCorrenteNegativo,
        noControlePositivo,
        noControleNegativo,
        transcondutancia,
    ):
        super().__init__(nome, noCorrentePositivo, noCorrenteNegativo)
        self.noCorrentePositivo = noCorrentePositivo
        self.noCorrenteNegativo = noCorrenteNegativo
        self.noControlePositivo = noControlePositivo
        self.noControleNegativo = noControleNegativo
        self.transcondutancia = transcondutancia

    def to_nl(self):
        return [
            self.nome,  # nome: G
            self.noCorrentePositivo,
            self.noCorrenteNegativo,
            self.noControlePositivo,
            self.noControleNegativo,
            self.transcondutancia,
        ]

    def from_nl(self, nl):
        self.nome = nl[0]
        self.noCorrentePositivo = int(nl[1])
        self.noCorrenteNegativo = int(nl[2])
        self.noControlePositivo = int(nl[3])
        self.noControleNegativo = int(nl[4])
        self.transcondutancia = int(nl[5])

    def estampa(
        self, G, I, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
    ):
        noA = self.noCorrentePositivo
        noB = self.noCorrenteNegativo
        noC = self.noControlePositivo
        noD = self.noControleNegativo

        G[noA, noC] += self.transcondutancia
        G[noA, noD] -= self.transcondutancia
        G[noB, noC] -= self.transcondutancia
        G[noB, noD] += self.transcondutancia
