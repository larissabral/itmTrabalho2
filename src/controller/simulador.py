from src.model.capacitor import Capacitor
from src.model.circuito import Circuito, Metodo
from src.model.diodo import Diodo
from src.model.fonteCorrente import FonteCorrente
from src.model.fonteCorrenteControladaCorrente import FonteCorrenteControladaCorrente
from src.model.fonteCorrenteControladaTensao import FonteCorrenteControladaTensao
from src.model.fonteTensao import FonteTensao
from src.model.fonteTensaoControladaCorrente import FonteTensaoControladaCorrente
from src.model.fonteTensaoControladaTensao import FonteTensaoControladaTensao
from src.model.indutor import Indutor
from src.model.resistor import Resistor
from src.model.resistorNaoLinear import ResistorNaoLinear
from src.model.simulacao import Simulacao


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

            if linha[0].startswith("H"):
                qntIncognitas = qntIncognitas + 2

    return qntIncognitas


class Simulador:
    def __init__(self):
        pass

    def simular_from_nl(self, arquivo):
        netlist = open(arquivo)

        linhas = netlist.readlines()

        qntNos = 0
        if not linhas[0].startswith("*") and not linhas[0].startswith("\n"):
            qntNos = int(linhas[0][0])

        qntIncognitas = qntIncognitasCircuito(linhas)

        circuito = Circuito([], qntNos, qntNos + qntIncognitas, Metodo.BACKWARD_EULER)

        simulacao = Simulacao()
        indice = -1
        while linhas:
            if linhas[indice].startswith(".TRAN"):
                simulacao.from_nl(linhas[indice])
            else:
                indice -= 1

        for linha in linhas:
            if not linha.startswith("*") and not linha.startswith("\n"):
                if linha.endswith("\n"):
                    linha = linha.replace("\n", "")
                linha = linha.split(" ")
                elemento = linha[0]
                if elemento.startswith("R"):
                    circuito.adiciona_componente(Resistor().from_nl(linha))
                if elemento.startswith("N"):
                    circuito.adiciona_componente(ResistorNaoLinear().from_nl(linha))
                if elemento.startswith("I"):
                    circuito.adiciona_componente(FonteCorrente().from_nl(linha))
                if elemento.startswith("V"):
                    circuito.adiciona_componente(FonteTensao().from_nl(linha))
                if elemento.startswith("G"):
                    circuito.adiciona_componente(
                        FonteCorrenteControladaTensao().from_nl(linha)
                    )
                if elemento.startswith("F"):
                    circuito.adiciona_componente(
                        FonteCorrenteControladaCorrente().from_nl(linha)
                    )
                if elemento.startswith("E"):
                    circuito.adiciona_componente(
                        FonteTensaoControladaTensao().from_nl(linha)
                    )
                if elemento.startswith("H"):
                    circuito.adiciona_componente(
                        FonteTensaoControladaCorrente().from_nl(linha)
                    )
                if elemento.startswith("C"):
                    circuito.adiciona_componente(Capacitor().from_nl(linha))
                if elemento.startswith("L"):
                    circuito.adiciona_componente(Indutor().from_nl(linha))
                if elemento.startswith("D"):
                    circuito.adiciona_componente(Diodo().from_nl(linha))

        resultados = circuito.resolver(simulacao)

        resultados = resultados.transpose()

        return resultados
