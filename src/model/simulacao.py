from src.model.circuito import Metodo


class Simulacao:
    def __init__(
        self,
        tempoTotal=0,
        passo=0,
        metodoIntegracao=Metodo.BACKWARD_EULER,
        passosInternos=0,
    ):
        self.tempoTotal = tempoTotal
        self.passo = passo
        self.metodoIntegracao = metodoIntegracao
        self.passosInternos = passosInternos

    def to_nl(self):
        return [
            ".TRAN",
            self.tempoTotal,
            self.passo,
            self.metodoIntegracao,
            self.passosInternos,
        ]

    def from_nl(self, nl):
        self.tempoTotal = float(nl[1])
        self.passo = float(nl[2])
        self.passosInternos = int(nl[4])
        if self.metodoIntegracao != Metodo.BACKWARD_EULER:
            raise Exception("Metodo de simulacao não implementado")
        return self
