import numpy as np

from src.model.elementoCircuito import ElementoCircuito


class FonteTensao(ElementoCircuito):
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
        ]  # nome: V

    def from_nl(self, nl):
        self.nome = nl[0]
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
        self.tipoFonte = int(nl[3])
        self.parametros = nl[4:]

    def estampa(
        self, G, Ix, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
    ):
        tensao = 0
        noA = self.noPositivo
        noB = self.noNegativo

        if self.tipoFonte == "DC":
            tensao = self.parametros[0]

        if self.tipoFonte == "SIN":
            qntNos = 0
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
                tensao = nivelContinuo + (amplitude * np.sin(fase))
            else:
                tensao = nivelContinuo + (
                    amplitude
                    * np.exp(-coef_alpha * tempo)
                    * np.sin(2 * np.pi * frequencia * tempo + fase)
                )

        if self.tipoFonte == "PULSE":
            qntNos = 0
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
                tensao = valor1

            if tempo <= tempoSubida:
                tensao = valor1 + (((valor1 - valor2) * tempo) / tempoSubida)
            elif tempo <= (tempoSubida + tempoLigado):
                tensao = valor2
            elif tempo <= (tempoSubida + tempoLigado + tempoDescida):
                tensao = valor2 - (
                    ((valor2 - valor1) * (tempo - tempoLigado - tempoSubida))
                    / tempoDescida
                )
            else:
                tensao = valor1

        G[noA, qntNos + posicao] += 1
        G[qntNos + posicao, noA] -= 1
        G[noB, qntNos + posicao] -= 1
        G[qntNos + posicao, noB] += 1

        Ix[qntNos + posicao] -= tensao

        return G, Ix, posicao
