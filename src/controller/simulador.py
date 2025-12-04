from src.model.ampOpIdeal import AmpOpIdeal
from src.model.capacitor import Capacitor
from src.model.circuito import Circuito, Metodo
from src.model.diodo import Diodo
from src.model.fonteCorrenteControladaCorrente import FonteCorrenteControladaCorrente
from src.model.fonteCorrenteControladaTensao import FonteCorrenteControladaTensao
from src.model.fonteCorrenteDC import FonteCorrenteDC
from src.model.fonteCorrentePulso import FonteCorrentePulso
from src.model.fonteCorrenteSenoidal import FonteCorrenteSenoidal
from src.model.fonteTensaoControladaCorrente import FonteTensaoControladaCorrente
from src.model.fonteTensaoControladaTensao import FonteTensaoControladaTensao
from src.model.fonteTensaoDC import FonteTensaoDC
from src.model.fonteTensaoPulso import FonteTensaoPulso
from src.model.fonteTensaoSenoidal import FonteTensaoSenoidal
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

        indice = 0
        qntNos = 0
        while linhas:
            if not linhas[indice].startswith("*") and not linhas[0].startswith("\n"):
                qntNos = int(linhas[indice][0])
                break
            indice += 1

        qntIncognitas = qntIncognitasCircuito(linhas)

        circuito = Circuito([], qntNos, qntIncognitas, Metodo.BACKWARD_EULER)

        simulacao = Simulacao()

        print("Simulação configurada. Implementando elementos...")

        for linha in linhas[indice + 1 :]:
            if not linha.startswith("*") and not linha.startswith("\n"):

                if linha.endswith("\n"):
                    linha = linha.replace("\n", "")

                linha = linha.split(" ")

                elemento = linha[0]

                if elemento.startswith("R"):
                    circuito.adiciona_componente(Resistor().from_nl(linha))
                elif elemento.startswith("N"):
                    circuito.possuiElementoNaoLinear = True
                    circuito.adiciona_componente(ResistorNaoLinear().from_nl(linha))
                elif elemento.startswith("I"):
                    if linha[3] == "DC":
                        circuito.adiciona_componente(FonteCorrenteDC().from_nl(linha))
                    elif linha[3] == "SIN":
                        circuito.adiciona_componente(
                            FonteCorrenteSenoidal().from_nl(linha)
                        )
                    elif linha[3] == "PULSE":
                        circuito.adiciona_componente(
                            FonteCorrentePulso().from_nl(linha)
                        )
                elif elemento.startswith("V"):
                    if linha[3] == "DC":
                        circuito.adiciona_componente(FonteTensaoDC().from_nl(linha))
                    elif linha[3] == "SIN":
                        circuito.adiciona_componente(
                            FonteTensaoSenoidal().from_nl(linha)
                        )
                    elif linha[3] == "PULSE":
                        circuito.adiciona_componente(FonteTensaoPulso().from_nl(linha))
                elif elemento.startswith("G"):
                    circuito.adiciona_componente(
                        FonteCorrenteControladaTensao().from_nl(linha)
                    )
                elif elemento.startswith("F"):
                    circuito.adiciona_componente(
                        FonteCorrenteControladaCorrente().from_nl(linha)
                    )
                elif elemento.startswith("E"):
                    circuito.adiciona_componente(
                        FonteTensaoControladaTensao().from_nl(linha)
                    )
                elif elemento.startswith("H"):
                    circuito.adiciona_componente(
                        FonteTensaoControladaCorrente().from_nl(linha)
                    )
                elif elemento.startswith("C"):
                    circuito.adiciona_componente(Capacitor().from_nl(linha))
                elif elemento.startswith("L"):
                    circuito.adiciona_componente(Indutor().from_nl(linha))
                elif elemento.startswith("O"):
                    circuito.adiciona_componente(AmpOpIdeal().from_nl(linha))
                elif elemento.startswith("D"):
                    circuito.possuiElementoNaoLinear = True
                    circuito.adiciona_componente(Diodo().from_nl(linha))
                elif elemento.startswith(".TRAN"):
                    simulacao.from_nl(linha)
                else:
                    raise ValueError(
                        f"Componente não implementado ou não reconhecido: {elemento}"
                    )

        print("Elementos adicionados. Resolvendo circuito...")

        resultados = circuito.resolver(simulacao)

        print("Circuito resolvido.")

        resultados = resultados.transpose()

        return resultados
