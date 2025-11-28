from abc import ABC, abstractmethod


class ElementoCircuito(ABC):
    def __init__(self, noPositivo, noNegativo):
        self.noPositivo = noPositivo
        self.noNegativo = noNegativo

    @abstractmethod
    def to_nl(self):
        """

        Transforma componente em linha de netlist

        """
        pass

    @abstractmethod
    def from_nl(self, nl):
        """

        Recupera componente a partir da netlist

        """
        pass

    @abstractmethod
    def estampa(
        self, G, I, deltaT, tensoesAnteriores, correntesAnteriores, posicao, qntNos
    ):
        """

        - G: matriz de condutâncias
        - I: vetor de correntes
        - deltaT: passo de integração

        """
        pass
