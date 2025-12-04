from src.model.elementoCircuito import ElementoCircuito


class FonteTensaoPulso(ElementoCircuito):
    def __init__(
        self,
        nome="",
        noPositivo=0,
        noNegativo=0,
        tipoFonte="PULSE",
        tempoAtual=0,
        valor1=0,
        valor2=0,
        atraso=0,
        tempoSubida=0,
        tempoDescida=0,
        tempoLigado=0,
        periodo=0,
        numeroCiclos=0,
        isTemporal=True,
    ):
        super().__init__(nome, noPositivo, noNegativo)
        self.tipoFonte = tipoFonte
        self.tempoAtual = tempoAtual
        self.valor1 = valor1
        self.valor2 = valor2
        self.atraso = atraso
        self.tempoSubida = tempoSubida
        self.tempoDescida = tempoDescida
        self.tempoLigado = tempoLigado
        self.periodo = periodo
        self.numeroCiclos = numeroCiclos
        self.isTemporal = isTemporal

    def to_nl(self):
        return [
            self.nome,
            self.noPositivo,
            self.noNegativo,
            self.tipoFonte,
            self.valor1,
            self.valor2,
            self.atraso,
            self.tempoSubida,
            self.tempoDescida,
            self.tempoLigado,
            self.periodo,
            self.numeroCiclos,
        ]  # nome: V

    def from_nl(self, nl):
        self.nome = nl[0]
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
        self.tipoFonte = int(nl[3])
        self.valor1 = float(nl[4])
        self.valor2 = float(nl[5])
        self.atraso = float(nl[6])
        self.tempoSubida = float(nl[7])
        self.tempoDescida = float(nl[8])
        self.tempoLigado = float(nl[9])
        self.periodo = float(nl[10])
        self.numeroCiclos = float(nl[11])

    def estampa(
        self, G, Ix, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
    ):
        noA = self.noPositivo
        noB = self.noNegativo

        qntNos = 0

        valor1 = self.valor1
        valor2 = self.valor2
        atraso = self.atraso
        tempoSubida = self.tempoSubida
        tempoDescida = self.tempoDescida
        tempoLigado = self.tempoLigado
        periodo = self.periodo
        # numeroCiclos = self.numeroCiclos
        #
        # tempoTotal = periodo * numeroCiclos

        if tempoSubida == 0:
            tempoSubida = deltaT

        if tempoDescida == 0:
            tempoDescida = deltaT

        tempo = (self.tempoAtual - atraso) % periodo

        if atraso >= self.tempoAtual:
            tensao = valor1

        if tempo <= tempoSubida:
            tensao = valor1 + (((valor1 - valor2) * tempo) / tempoSubida)
        elif tempo <= (tempoSubida + tempoLigado):
            tensao = valor2
        elif tempo <= (tempoSubida + tempoLigado + tempoDescida):
            tensao = valor2 - (
                ((valor2 - valor1) * (tempo - tempoLigado - tempoSubida)) / tempoDescida
            )
        else:
            tensao = valor1

        G[noA, qntNos + posicao] += 1
        G[qntNos + posicao, noA] -= 1
        G[noB, qntNos + posicao] -= 1
        G[qntNos + posicao, noB] += 1

        Ix[qntNos + posicao] -= tensao

        posicao += 1

        return G, Ix, posicao
