from abc import ABC, abstractmethod


class ElementoCircuito(ABC):
    def __init__(self, noPositivo, noNegativo):
        self.noPositivo = noPositivo
        self.noNegativo = noNegativo

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
