import numpy as np

from src.model.elementoCircuito import ElementoCircuito


class FonteTensaoSenoidal(ElementoCircuito):
    def __init__(
        self,
        nome="",
        noPositivo=0,
        noNegativo=0,
        tipoFonte="SIN",
        tempoAtual=0,
        nivelContinuo=0,
        amplitude=0,
        frequencia=0,
        atraso=0,
        coef_alpha=0,
        fase=0,
        numeroCiclos=0,
        isTemporal=True,
    ):
        super().__init__(nome, noPositivo, noNegativo)
        self.tipoFonte = tipoFonte
        self.tempoAtual = tempoAtual
        self.isTemporal = isTemporal
        self.nivelContinuo = nivelContinuo
        self.amplitude = amplitude
        self.frequencia = frequencia
        self.atraso = atraso
        self.coef_alpha = coef_alpha
        self.fase = fase
        self.numeroCiclos = numeroCiclos

    def to_nl(self):
        return [
            self.nome,
            self.noPositivo,
            self.noNegativo,
            self.tipoFonte,
            self.nivelContinuo,
            self.amplitude,
            self.frequencia,
            self.atraso,
            self.coef_alpha,
            self.fase,
            self.numeroCiclos,
        ]  # nome: V

    def from_nl(self, nl):
        self.nome = nl[0]
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
        self.tipoFonte = int(nl[3])
        self.nivelContinuo = float(nl[4])  # A0
        self.amplitude = float(nl[5])
        self.frequencia = float(nl[6])
        self.atraso = float(nl[7])  # atraso do sinal ta
        self.coef_alpha = float(nl[8])  # coeficiente de amortecimento
        self.fase = float(nl[9])
        self.numeroCiclos = float(nl[10])
        return self

    def estampa(
        self, G, Ix, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
    ):
        noA = self.noPositivo
        noB = self.noNegativo

        qntNos = 0
        nivelContinuo = self.nivelContinuo
        amplitude = self.amplitude
        frequencia = self.frequencia
        atraso = self.atraso
        coef_alpha = self.coef_alpha
        fase = self.fase
        numeroCiclos = self.numeroCiclos

        tempo = self.tempoAtual - atraso
        fase = fase * (np.pi / 180)
        tempoFinal = atraso + (numeroCiclos / frequencia)

        if self.tempoAtual < atraso or self.tempoAtual > tempoFinal:
            tensao = nivelContinuo + (amplitude * np.sin(fase))
        else:
            tensao = nivelContinuo + (
                amplitude
                * np.exp(-coef_alpha * tempo)
                * np.sin(2 * np.pi * frequencia * tempo + fase)
            )

        G[noA, qntNos + posicao] += 1
        G[qntNos + posicao, noA] -= 1
        G[noB, qntNos + posicao] -= 1
        G[qntNos + posicao, noB] += 1

        Ix[qntNos + posicao] -= tensao

        posicao += 1

        return G, Ix, posicao
