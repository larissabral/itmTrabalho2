class Diodo:
    def __init__(self, noPositivo, noNegativo):
        self.noPositivo = noPositivo
        self.noNegativo = noNegativo

    def to_nl(self):
        return ["D", self.noPositivo, self.noNegativo]

    def from_nl(self, nl):
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
