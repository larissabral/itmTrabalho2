class FonteCorrente:
    def __init__(self, noPositivo, noNegativo, tipoFonte, parametros):
        self.noPositivo = noPositivo
        self.noNegativo = noNegativo
        self.tipoFonte = tipoFonte
        self.parametros = parametros

    def to_nl(self):
        return ["I", self.noPositivo, self.noNegativo, self.tipoFonte, self.parametros]

    def from_nl(self, nl):
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
        self.tipoFonte = int(nl[3])
        self.parametros = nl[4:]
