class Capacitor:
    def __init__(self, noPositivo, noNegativo, capacitancia, tensaoInicial):
        self.noPositivo = noPositivo
        self.noNegativo = noNegativo
        self.capacitancia = capacitancia
        self.tensaoInicial = tensaoInicial

    def to_nl(self):
        return [
            "C",
            self.noPositivo,
            self.noNegativo,
            self.capacitancia,
            "IC=" + self.tensaoInicial,
        ]

    def from_nl(self, nl):
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
        self.capacitancia = float(nl[3])
        self.tensaoInicial = float(nl[4].replace("IC=", ""))
