class Simulacao:
    def __init__(self, tempoTotal, passo, metodoIntegracao, passosInternos):
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
        self.metodoIntegracao = nl[3]
        self.passosInternos = int(nl[4])
