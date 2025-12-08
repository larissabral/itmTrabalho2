import warnings

# import matplotlib.pyplot as plt
import numpy as np

warnings.filterwarnings("ignore")


def main(arquivo, tempoSimulacao, passo, tolerancia, v0s, vouts):
    netlist = open(arquivo)

    linhas = netlist.readlines()

    qntNos = qntNosCircuito(linhas)

    qntIncognitas = qntIncognitasCircuito(linhas)

    Gn = np.zeros([qntNos + qntIncognitas + 1, qntNos + qntIncognitas + 1])

    In = np.zeros(qntNos + qntIncognitas + 1)

    posicao = 0

    quantidadePontos = int(tempoSimulacao / passo) + 1

    tempo = np.arange(0, quantidadePontos) * passo

    tensoesAnteriores = np.array(v0s.copy())

    resultados = np.zeros([quantidadePontos, qntNos])

    resultados[0] = tensoesAnteriores

    for linha in linhas:
        if not linha.startswith("*") and not linha.startswith("\n"):
            if linha.endswith("\n"):
                linha = linha.replace("\n", "")
            linha = linha.split(" ")
            if linha[0].startswith("R"):
                Gn = adicionarResistor(
                    float(linha[3]), int(linha[1]), int(linha[2]), Gn
                )
            if linha[0].startswith("I"):
                if linha[3] == "DC":
                    In = adicionarFonteCorrenteIndependenteDC(
                        float(linha[4]), int(linha[1]), int(linha[2]), In
                    )
            if linha[0].startswith("V"):
                posicao = posicao + 1
                if linha[3] == "DC":
                    In = adicionarFonteTensaoIndependenteDCValor(
                        float(linha[4]), In, qntNos, posicao
                    )
                    Gn = adicionarFonteTensaoIndependenteDCMatriz(
                        int(linha[1]), int(linha[2]), Gn, qntNos, posicao
                    )
            if linha[0].startswith("G"):
                Gn = adicionarFonteCorrenteControladaPorTensao(
                    float(linha[5]),
                    int(linha[1]),
                    int(linha[2]),
                    int(linha[3]),
                    int(linha[4]),
                    Gn,
                )
            if linha[0].startswith("F"):
                posicao = posicao + 1
                Gn = adicionarFonteCorrenteControladaPorCorrente(
                    float(linha[5]),
                    int(linha[1]),
                    int(linha[2]),
                    int(linha[3]),
                    int(linha[4]),
                    Gn,
                    qntNos,
                    posicao,
                )
            if linha[0].startswith("E"):
                posicao = posicao + 1
                Gn = adicionarFonteTensaoControladaPorTensao(
                    float(linha[5]),
                    int(linha[1]),
                    int(linha[2]),
                    int(linha[3]),
                    int(linha[4]),
                    Gn,
                    qntNos,
                    posicao,
                )
            if linha[0].startswith("H"):
                posicao = posicao + 1
                Gn = adicionarFonteTensaoControladaPorCorrente(
                    float(linha[5]),
                    int(linha[1]),
                    int(linha[2]),
                    int(linha[3]),
                    int(linha[4]),
                    Gn,
                    qntNos,
                    posicao,
                )
                posicao = posicao + 1

    correntesAnteriores = np.copy(In)
    for index, tempoAtual in enumerate(tempo[1:]):
        posicao = qntNos + 1
        tensoesAnteriores = np.concatenate(([0], tensoesAnteriores))

        GnTemporal = np.copy(Gn)
        ITemporal = np.copy(In)

        for linha in linhas:
            if not linha.startswith("*") and not linha.startswith("\n"):
                if linha.endswith("\n"):
                    linha = linha.replace("\n", "")
                linha = linha.split(" ")
                if linha[0].startswith("C"):
                    GnTemporal = adicionarCapacitorMatriz(
                        float(linha[3]), int(linha[1]), int(linha[2]), GnTemporal, passo
                    )
                    ITemporal = adicionarCapacitorValor(
                        float(linha[3]),
                        int(linha[1]),
                        int(linha[2]),
                        ITemporal,
                        passo,
                        tensoesAnteriores,
                    )
                if linha[0].startswith("L"):
                    GnTemporal = adicionarIndutorMatriz(
                        float(linha[3]),
                        int(linha[1]),
                        int(linha[2]),
                        GnTemporal,
                        passo,
                        posicao,
                    )
                    ITemporal = adicionarIndutorValor(
                        float(linha[3]),
                        ITemporal,
                        passo,
                        qntNos,
                        correntesAnteriores,
                        posicao,
                    )
                    posicao = posicao + 1
                if linha[0].startswith("I"):
                    if linha[3] == "SIN":
                        ITemporal = adicionarFonteCorrenteIndependenteSenoidal(
                            float(linha[4]),
                            float(linha[5]),
                            float(linha[6]),
                            float(linha[7]),
                            tempoAtual,
                            int(linha[1]),
                            int(linha[2]),
                            ITemporal,
                        )
                    if linha[3] == "PULSE":
                        ITemporal = adicionarFonteCorrenteIndependentePULSE(
                            float(linha[4]),
                            float(linha[5]),
                            float(linha[6]),
                            float(linha[7]),
                            float(linha[8]),
                            float(linha[9]),
                            float(linha[10]),
                            tempoAtual,
                            int(linha[1]),
                            int(linha[2]),
                            ITemporal,
                        )
                if linha[0].startswith("V"):
                    if linha[3] == "SIN":
                        GnTemporal = adicionarFonteTensaoIndependenteDCMatriz(
                            int(linha[1]), int(linha[2]), GnTemporal, 0, posicao
                        )
                        ITemporal = adicionarFonteTensaoIndependenteSenoidalValor(
                            float(linha[4]),
                            float(linha[5]),
                            float(linha[6]),
                            float(linha[7]),
                            tempoAtual,
                            posicao,
                            ITemporal,
                        )
                    if linha[3] == "PULSE":
                        GnTemporal = adicionarFonteTensaoIndependenteDCMatriz(
                            int(linha[1]), int(linha[2]), GnTemporal, 0, posicao
                        )
                        ITemporal = adicionarFonteTensaoIndependentePULSEValor(
                            float(linha[4]),
                            float(linha[5]),
                            float(linha[6]),
                            float(linha[7]),
                            float(linha[8]),
                            float(linha[9]),
                            float(linha[10]),
                            tempoAtual,
                            posicao,
                            ITemporal,
                        )
                    posicao = posicao + 1
                if linha[0].startswith("K"):
                    GnTemporal = adicionarTransformadorMatriz(
                        int(linha[1]),
                        int(linha[2]),
                        int(linha[3]),
                        int(linha[4]),
                        float(linha[5]),
                        float(linha[6]),
                        float(linha[7]),
                        GnTemporal,
                        posicao,
                        passo,
                    )
                    ITemporal = adicionarTransformadorValor(
                        float(linha[5]),
                        float(linha[6]),
                        float(linha[7]),
                        ITemporal,
                        correntesAnteriores,
                        posicao,
                        qntNos,
                        passo,
                    )
                    posicao = posicao + 2

        if possuiDiodo(linhas):
            e = calcularCircuitoNaoLinear(
                linhas,
                GnTemporal,
                ITemporal,
                tensoesAnteriores,
                tolerancia,
                qntIncognitas,
            )

            resultados[index + 1] = e[:-qntIncognitas]
            correntesAnteriores = e[qntIncognitas:]
        else:
            e = np.linalg.solve(GnTemporal[1:, 1:], ITemporal[1:])
            resultados[index + 1] = e[:-qntIncognitas]
            correntesAnteriores = e[qntIncognitas:]

        tensoesAnteriores = resultados[index + 1]

    resultados = resultados.transpose()
    nosDesejados = list(map(lambda x: x - 1, vouts))

    return resultados[nosDesejados]


def qntNosCircuito(linhas):
    listaNos = []

    for linha in linhas:
        if not linha.startswith("*") and not linha.startswith("\n"):
            linha = linha.split(" ")
            listaNos.append(linha[1])
            listaNos.append(linha[2])
            if (
                linha[0].startswith("K")
                or linha[0].startswith("G")
                or linha[0].startswith("H")
                or linha[0].startswith("F")
                or linha[0].startswith("E")
            ):
                listaNos.append(linha[3])
                listaNos.append(linha[4])

    qntNos = 0
    for val in listaNos:
        if qntNos < int(val):
            qntNos = int(val)

    return qntNos


def qntIncognitasCircuito(linhas):
    qntIncognitas = 0
    for linha in linhas:
        if not linha.startswith("*") and not linha.startswith("\n"):
            linha = linha.split(" ")
            if (
                linha[0].startswith("V")
                or linha[0].startswith("E")
                or linha[0].startswith("F")
                or linha[0].startswith("L")
            ):
                qntIncognitas = qntIncognitas + 1

            if linha[0].startswith("H") or linha[0].startswith("K"):
                qntIncognitas = qntIncognitas + 2

    return qntIncognitas


def possuiDiodo(linhas):
    for linha in linhas:
        if not linha.startswith("*") and not linha.startswith("\n"):
            if linha.endswith("\n"):
                linha = linha.replace("\n", "")
            linha = linha.split(" ")
            if linha[0].startswith("D"):
                return True

    return False


def calcularCircuitoNaoLinear(
    linhas, Gn, In, tensoesAnteriores, tolerancia, qntIncognitas
):
    iteracoes = 1000

    matriz, vetor = np.copy(Gn), np.copy(In)

    while iteracoes > 0:
        for linha in linhas:
            if not linha.startswith("*") and not linha.startswith("\n"):
                if linha.endswith("\n"):
                    linha = linha.replace("\n", "")
                linha = linha.split(" ")
                if linha[0].startswith("D"):
                    matriz = adicionarDiodoMatriz(
                        int(linha[1]),
                        int(linha[2]),
                        float(linha[3]),
                        float(linha[4]),
                        matriz,
                        tensoesAnteriores,
                    )
                    vetor = adicionarDiodoValor(
                        int(linha[1]),
                        int(linha[2]),
                        float(linha[3]),
                        float(linha[4]),
                        vetor,
                        tensoesAnteriores,
                    )

        resultadoParcial = np.linalg.solve(matriz[1:, 1:], vetor[1:])

        diferenca = np.max(
            np.abs(tensoesAnteriores[1:] - resultadoParcial[:-qntIncognitas])
        )

        if diferenca < tolerancia:
            break

        tensoesAnteriores = np.concatenate(([0], resultadoParcial[:-qntIncognitas]))
        iteracoes = iteracoes - 1
        matriz, vetor = np.copy(Gn), np.copy(In)

    return np.linalg.solve(matriz[1:, 1:], vetor[1:])


def adicionarResistor(resistencia, noA, noB, Gn):
    Gn[noA, noA] = Gn[noA, noA] + 1 / resistencia
    Gn[noA, noB] = Gn[noA, noB] - 1 / resistencia
    Gn[noB, noA] = Gn[noB, noA] - 1 / resistencia
    Gn[noB, noB] = Gn[noB, noB] + 1 / resistencia
    return Gn


def adicionarCapacitorMatriz(capacitancia, noA, noB, Gn, deltaT):
    Gn[noA, noA] = Gn[noA, noA] + capacitancia / deltaT
    Gn[noA, noB] = Gn[noA, noB] - capacitancia / deltaT
    Gn[noB, noA] = Gn[noB, noA] - capacitancia / deltaT
    Gn[noB, noB] = Gn[noB, noB] + capacitancia / deltaT
    return Gn


def adicionarCapacitorValor(capacitancia, noA, noB, In, deltaT, tensoesAnteriores):
    corrente = capacitancia * (tensoesAnteriores[noA] - tensoesAnteriores[noB]) / deltaT
    In[noA] = In[noA] + corrente
    In[noB] = In[noB] - corrente
    return In


def adicionarIndutorMatriz(indutancia, noA, noB, Gn, deltaT, posicao):
    Gn[noA, posicao] = Gn[noA, posicao] + 1
    Gn[noB, posicao] = Gn[noB, posicao] - 1
    Gn[posicao, noA] = Gn[posicao, noA] - 1
    Gn[posicao, noB] = Gn[posicao, noB] + 1
    Gn[posicao, posicao] = Gn[posicao, posicao] + indutancia / deltaT
    return Gn


def adicionarIndutorValor(indutancia, In, deltaT, qntNos, correntesAnteriores, posicao):
    i_t0 = correntesAnteriores[posicao - qntNos] * indutancia / deltaT
    In[posicao] = In[posicao] + i_t0
    return In


def adicionarDiodoMatriz(noA, noB, Is, nVt, Gn, tensoesAnteriores):
    tensao = tensoesAnteriores[noA] - tensoesAnteriores[noB]
    i = Is * np.exp(tensao / nVt)
    condutancia = i / nVt

    if condutancia == 0:
        resistencia = np.inf
    else:
        resistencia = 1.0 / condutancia

    Gn[noA, noA] = Gn[noA, noA] + 1 / resistencia
    Gn[noA, noB] = Gn[noA, noB] - 1 / resistencia
    Gn[noB, noA] = Gn[noB, noA] - 1 / resistencia
    Gn[noB, noB] = Gn[noB, noB] + 1 / resistencia

    return Gn


def adicionarDiodoValor(noA, noB, Is, nVt, In, tensoesAnteriores):
    tensao = tensoesAnteriores[noA] - tensoesAnteriores[noB]
    i = Is * np.exp(tensao / nVt)
    condutancia = i / nVt
    corrente = i - Is - (condutancia * tensao)

    In[noA] = In[noA] - corrente
    In[noB] = In[noB] + corrente

    return In


def adicionarFonteCorrenteIndependenteDC(corrente, noA, noB, In):
    In[noA] = In[noA] - corrente
    In[noB] = In[noB] + corrente
    return In


def adicionarFonteCorrenteIndependenteSenoidal(
    valorDC, amplitude, frequencia, fase, tempoAtual, noA, noB, In
):
    tempo = 2 * np.pi * frequencia * tempoAtual
    corrente = (amplitude * np.cos(tempo + (fase * (np.pi / 180)))) + valorDC
    In[noA] = In[noA] - corrente
    In[noB] = In[noB] + corrente
    return In


def adicionarFonteCorrenteIndependentePULSE(
    valor1,
    valor2,
    delay,
    tempoSubida,
    tempoDescida,
    tempoV2,
    periodo,
    tempoAtual,
    noA,
    noB,
    In,
):
    if delay >= tempoAtual:
        In[noA] = In[noA] - valor1
        In[noB] = In[noB] + valor1
        return In

    tempo = (tempoAtual - delay) % periodo

    if tempo <= tempoSubida:
        valor = valor1 + (((valor1 - valor2) * tempo) / tempoSubida)
    elif tempo <= (tempoSubida + tempoV2):
        valor = valor2
    elif tempo <= (tempoSubida + tempoV2 + tempoDescida):
        valor = valor2 - (
            ((valor2 - valor1) * (tempo - tempoV2 - tempoSubida)) / tempoDescida
        )
    else:
        valor = valor1

    In[noA] = In[noA] - valor
    In[noB] = In[noB] + valor
    return In


def adicionarFonteTensaoIndependenteDCMatriz(noA, noB, Gn, qntNos, posicao):
    Gn[noA, qntNos + posicao] = Gn[noA, qntNos + posicao] + 1
    Gn[qntNos + posicao, noA] = Gn[qntNos + posicao, noA] - 1
    Gn[noB, qntNos + posicao] = Gn[noB, qntNos + posicao] - 1
    Gn[qntNos + posicao, noB] = Gn[qntNos + posicao, noB] + 1
    return Gn


def adicionarFonteTensaoIndependenteDCValor(tensao, In, qntNos, posicao):
    In[qntNos + posicao] = In[qntNos + posicao] - tensao
    return In


def adicionarFonteTensaoIndependenteSenoidalValor(
    valorDC, amplitude, frequencia, fase, tempoAtual, posicao, In
):
    tempo = 2 * np.pi * frequencia * tempoAtual
    fase = fase * (np.pi / 180)
    tensao = (amplitude * np.cos(tempo + fase)) + valorDC
    In[posicao] = In[posicao] - tensao
    return In


def adicionarFonteTensaoIndependentePULSEValor(
    valor1,
    valor2,
    delay,
    tempoSubida,
    tempoDescida,
    tempoV2,
    periodo,
    tempoAtual,
    posicao,
    In,
):
    if delay >= tempoAtual:
        In[posicao] = In[posicao] - valor1
        return In

    tempo = (tempoAtual - delay) % periodo

    if tempo <= tempoSubida:
        valor = valor1 + (((valor1 - valor2) * tempo) / tempoSubida)
    elif tempo <= (tempoSubida + tempoV2):
        valor = valor2
    elif tempo <= (tempoSubida + tempoV2 + tempoDescida):
        valor = valor2 - (
            ((valor2 - valor1) * (tempo - tempoV2 - tempoSubida)) / tempoDescida
        )
    else:
        valor = valor1

    In[posicao] = In[posicao] - valor
    return In


def adicionarFonteCorrenteControladaPorTensao(transcondutancia, noA, noB, noC, noD, Gn):
    Gn[noA, noC] = Gn[noA, noC] + transcondutancia
    Gn[noA, noD] = Gn[noA, noD] - transcondutancia
    Gn[noB, noC] = Gn[noB, noC] - transcondutancia
    Gn[noB, noD] = Gn[noB, noD] + transcondutancia
    return Gn


def adicionarFonteCorrenteControladaPorCorrente(
    ganhoCorrente, noA, noB, noC, noD, Gn, qntNos, posicao
):
    ix = qntNos + posicao
    Gn[noA, ix] = Gn[noA, ix] + ganhoCorrente
    Gn[noB, ix] = Gn[noB, ix] - ganhoCorrente
    Gn[noC, ix] = Gn[noC, ix] + 1
    Gn[noD, ix] = Gn[noD, ix] - 1
    Gn[ix, noC] = Gn[ix, noC] - 1
    Gn[ix, noD] = Gn[ix, noD] + 1
    return Gn


def adicionarFonteTensaoControladaPorTensao(
    ganhoTensao, noA, noB, noC, noD, Gn, qntNos, posicao
):
    ix = qntNos + posicao
    Gn[noA, ix] = Gn[noA, ix] + 1
    Gn[noB, ix] = Gn[noB, ix] - 1
    Gn[ix, noA] = Gn[ix, noA] - 1
    Gn[ix, noB] = Gn[ix, noB] + 1
    Gn[ix, noC] = Gn[ix, noC] + ganhoTensao
    Gn[ix, noD] = Gn[ix, noD] - ganhoTensao
    return Gn


def adicionarFonteTensaoControladaPorCorrente(
    transresistencia, noA, noB, noC, noD, Gn, qntNos, posicao
):
    ix = qntNos + posicao
    iy = qntNos + posicao + 1
    Gn[noA, iy] = Gn[noA, iy] + 1
    Gn[noB, iy] = Gn[noB, iy] - 1
    Gn[noC, ix] = Gn[noC, ix] + 1
    Gn[noD, ix] = Gn[noD, ix] - 1
    Gn[ix, noC] = Gn[ix, noC] - 1
    Gn[ix, noD] = Gn[ix, noD] + 1
    Gn[iy, noA] = Gn[iy, noA] - 1
    Gn[iy, noB] = Gn[iy, noB] + 1
    Gn[iy, ix] = Gn[iy, ix] + transresistencia
    return Gn


def adicionarTransformadorMatriz(noA, noB, noC, noD, L1, L2, M, Gn, posicao, deltaT):
    ix = posicao
    iy = posicao + 1
    Gn[noA, ix] = Gn[noA, ix] + 1
    Gn[noB, ix] = Gn[noB, ix] - 1
    Gn[noC, iy] = Gn[noC, iy] + 1
    Gn[noD, iy] = Gn[noD, iy] - 1
    Gn[ix, noA] = Gn[ix, noA] - 1
    Gn[ix, noB] = Gn[ix, noB] + 1
    Gn[iy, noC] = Gn[iy, noC] - 1
    Gn[iy, noD] = Gn[iy, noD] + 1
    Gn[ix, ix] = Gn[ix, ix] + (L1 / deltaT)
    Gn[ix, iy] = Gn[ix, iy] + (M / deltaT)
    Gn[iy, ix] = Gn[iy, ix] + (M / deltaT)
    Gn[iy, iy] = Gn[iy, iy] + (L2 / deltaT)
    return Gn


def adicionarTransformadorValor(
    L1, L2, M, In, correntesAnteriores, posicao, qntNos, deltaT
):
    ix = posicao
    iy = posicao + 1
    correnteIndutor1 = (
        L1 * correntesAnteriores[ix - qntNos - 1]
        + M * correntesAnteriores[iy - qntNos - 1]
    ) / deltaT
    correnteIndutor2 = (
        M * correntesAnteriores[ix - qntNos - 1]
        + L2 * correntesAnteriores[iy - qntNos - 1]
    ) / deltaT
    In[ix] = In[ix] + correnteIndutor1
    In[iy] = In[iy] + correnteIndutor2
    return In


# gerar grafico com vetor de saída:

# with np.printoptions(formatter={'float': '{: 0.8f}'.format}):
#     DELLTA_T = 0.2e-3
#     N_PONTOS = 4 / DELLTA_T + 1
#     figures, axis = plt.subplots(1, 1)
#
#     tempo_total = np.arange(0, N_PONTOS) * DELLTA_T
#     resultado1 = main('./testes/netlist6.txt', 4, 0.2e-3, 1e-4, [0, 0, 0], [1, 2, 3])
#     axis.plot(tempo_total, resultado1[0], tempo_total, resultado1[1], tempo_total, resultado1[2])
#
#     figures.tight_layout()
#     plt.show()
#     plt.close()
