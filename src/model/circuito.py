import enum

import numpy as np


class Metodo(enum.Enum):
    TRAPEZOIDAL = "TRAP"
    FORWARD_EULER = "FE"
    BACKWARD_EULER = "BE"


class Circuito:
    def __init__(self, elementos, qntNos, zeros, metodoIntegracao):
        self.elementos = elementos
        self.qntNos = qntNos
        self.zeros = zeros
        self.metodoIntegracao = metodoIntegracao

    def to_nl(self) -> str:
        netlist = f"{self.zeros}\n"
        for elemento in self.elementos:
            if hasattr(elemento, "to_nl"):
                netlist += elemento.to_nl() + "\n"
        return netlist

    def adiciona_componente(self, componente):
        self.elementos.append(componente)

    def inicializar_matrizes(self):
        n = self.zeros + 1

        G = np.zeros((n, n))
        Ix = np.zeros(n)

        return G, Ix

    def resolver(self, simulacao):
        Gn, Ix = self.inicializar_matrizes()
        posicao = 0

        tempoSimulacao = simulacao.tempoTotal
        passo = simulacao.passo
        tolerancia = simulacao.passosInternos

        quantidadePontos = int(tempoSimulacao / passo) + 1

        tempo = np.arange(0, quantidadePontos) * passo

        resultados = np.zeros([quantidadePontos, self.qntNos])

        pass
