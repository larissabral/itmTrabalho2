import enum

import numpy as np


class Metodo(enum.Enum):
    TRAPEZOIDAL = "TRAP"
    FORWARD_EULER = "FE"
    BACKWARD_EULER = "BE"


class Circuito:
    def __init__(
        self,
        elementos,
        qntNos,
        qntIncognitas,
        metodoIntegracao,
        possuiElementoNaoLinear=False,
    ):
        self.possuiElementoNaoLinear = possuiElementoNaoLinear
        self.elementos = elementos
        self.qntNos = qntNos
        self.qntIncognitas = qntIncognitas
        self.metodoIntegracao = metodoIntegracao

    def to_nl(self) -> str:
        netlist = f"{self.qntNos}\n"
        for elemento in self.elementos:
            if hasattr(elemento, "to_nl"):
                netlist += elemento.to_nl() + "\n"
        return netlist

    def adiciona_componente(self, componente):
        self.elementos.append(componente)

    def inicializar_matrizes(self):
        n = self.qntIncognitas + self.qntNos + 1

        G = np.zeros((n, n))
        Ix = np.zeros(n)

        return G, Ix

    def resolver(self, simulacao):
        qntIncognitas = self.qntIncognitas
        qntNos = self.qntNos

        Gn, Ix = self.inicializar_matrizes()
        posicao = 0

        tempoSimulacao = simulacao.tempoTotal
        passo = simulacao.passo
        tolerancia = simulacao.passosInternos

        quantidadePontos = int(tempoSimulacao / passo) + 1

        tempo = np.arange(0, quantidadePontos) * passo

        tensoesAnteriores = []

        resultados = np.zeros([quantidadePontos, qntNos])

        resultados[0] = tensoesAnteriores

        for elemento in self.elementos:
            if not hasattr(elemento, "isTemporal") and not hasattr(
                elemento, "isNaoLinear"
            ):
                Gn, Ix, posicao = elemento.estampa(
                    Gn, Ix, passo, [], [], posicao, qntNos
                )

        correntesAnteriores = np.copy(Ix)

        for index, tempoAtual in enumerate(tempo[1:]):
            posicao = qntNos + 1

            GnTemporal = np.copy(Gn)
            ITemporal = np.copy(Ix)

            tensoesAnteriores = np.concatenate(([0], tensoesAnteriores))

            for elemento in self.elementos:
                if hasattr(elemento, "isTemporal") and not hasattr(
                    elemento, "isNaoLinear"
                ):
                    elemento.tempoAtual = tempoAtual

                    GnTemporal, ITemporal, posicao = elemento.estampa(
                        GnTemporal,
                        ITemporal,
                        passo,
                        tensoesAnteriores,
                        correntesAnteriores,
                        posicao,
                        qntNos,
                    )

            if self.possuiElementoNaoLinear:
                e = self.calcularCircuitoNaoLinear(
                    GnTemporal, ITemporal, tensoesAnteriores, tolerancia, qntIncognitas
                )

                resultados[index + 1] = e[:-qntIncognitas]
                correntesAnteriores = e[qntIncognitas:]
            else:
                e = np.linalg.solve(GnTemporal[1:, 1:], ITemporal[1:])
                resultados[index + 1] = e[:-qntIncognitas]
                correntesAnteriores = e[qntIncognitas:]

            tensoesAnteriores = resultados[index + 1]

        resultados = resultados.transpose()

        return resultados

    # TODO: Verificar Newton-Raphson
    def calcularCircuitoNaoLinear(
        self, GnTemporal, ITemporal, tensoesAnteriores, tolerancia, qntIncognitas
    ):
        iteracoes = 1000

        matriz, vetor = np.copy(GnTemporal), np.copy(ITemporal)

        while iteracoes > 0:
            for elemento in self.elementos:
                if hasattr(elemento, "isNaoLinear"):
                    matriz, vetor, posicao = elemento.estampa(
                        matriz, vetor, 0, tensoesAnteriores, [], 0, self.qntNos
                    )

            resultadoParcial = np.linalg.solve(matriz[1:, 1:], vetor[1:])

            diferenca = np.max(
                np.abs(tensoesAnteriores[1:] - resultadoParcial[:-qntIncognitas])
            )

            if diferenca < tolerancia:
                break

            tensoesAnteriores = np.concatenate(([0], resultadoParcial[:-qntIncognitas]))
            iteracoes = iteracoes - 1
            matriz, vetor = np.copy(GnTemporal), np.copy(ITemporal)

        return np.linalg.solve(matriz[1:, 1:], vetor[1:])
