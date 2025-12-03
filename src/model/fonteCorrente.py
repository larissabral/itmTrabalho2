import numpy as np

from src.model.elementoCircuito import ElementoCircuito


class FonteCorrente(ElementoCircuito):
    def __init__(
        self,
        nome="",
        noPositivo=0,
        noNegativo=0,
        tipoFonte="",
        parametros=None,
        tempoAtual=0,
    ):
        super().__init__(nome, noPositivo, noNegativo)
        self.tipoFonte = tipoFonte
        self.parametros = parametros
        self.tempoAtual = tempoAtual

    def to_nl(self):
        return [
            self.nome,
            self.noPositivo,
            self.noNegativo,
            self.tipoFonte,
            self.parametros,
        ]  # nome: I

    def from_nl(self, nl):
        self.nome = nl[0]
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
        self.tipoFonte = int(nl[3])
        self.parametros = nl[4:]

    def estampa(
        self, G, Ix, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
    ):
        noA = self.noPositivo
        noB = self.noNegativo
        corrente = 0

        if self.tipoFonte == "DC":
            corrente = self.parametros[0]

        if self.tipoFonte == "SIN":
            nivelContinuo = float(self.parametros[0])  # A0
            amplitude = float(self.parametros[1])
            frequencia = float(self.parametros[2])
            atraso = float(self.parametros[3])  # atraso do sinal ta
            coef_alpha = float(self.parametros[4])  # coeficiente de amortecimento
            fase = float(self.parametros[5])
            numeroCiclos = float(self.parametros[6])

            tempo = self.tempoAtual - atraso
            fase = fase * (np.pi / 180)
            tempoFinal = atraso + (numeroCiclos / frequencia)

            if self.tempoAtual < atraso or self.tempoAtual > tempoFinal:
                corrente = nivelContinuo + (amplitude * np.sin(fase))
            else:
                corrente = nivelContinuo + (
                    amplitude
                    * np.exp(-coef_alpha * tempo)
                    * np.sin(2 * np.pi * frequencia * tempo + fase)
                )

        if self.tipoFonte == "PULSE":
            valor1 = float(self.parametros[0])
            valor2 = float(self.parametros[1])
            atraso = float(self.parametros[2])
            tempoSubida = float(self.parametros[3])
            tempoDescida = float(self.parametros[4])
            tempoLigado = float(self.parametros[5])
            periodo = float(self.parametros[6])
            numeroCiclos = float(self.parametros[7])

            if tempoSubida == 0:
                tempoSubida = deltaT

            if tempoDescida == 0:
                tempoDescida = deltaT

            tempo = (self.tempoAtual - atraso) % periodo

            if atraso >= self.tempoAtual:
                corrente = valor1

            if tempo <= tempoSubida:
                corrente = valor1 + (((valor1 - valor2) * tempo) / tempoSubida)
            elif tempo <= (tempoSubida + tempoLigado):
                corrente = valor2
            elif tempo <= (tempoSubida + tempoLigado + tempoDescida):
                corrente = valor2 - (
                    ((valor2 - valor1) * (tempo - tempoLigado - tempoSubida))
                    / tempoDescida
                )
            else:
                corrente = valor1

        Ix[noA] -= corrente
        Ix[noB] += corrente
