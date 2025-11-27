class ResistorNaoLinear:
    def __init__(self, noPositivo, noNegativo, v1, v2, v3, v4, i1, i2, i3, i4):
        self.noPositivo = noPositivo
        self.noNegativo = noNegativo
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4
        self.i1 = i1
        self.i2 = i2
        self.i3 = i3
        self.i4 = i4

    def to_nl(self):
        return [
            "N",
            self.noPositivo,
            self.noNegativo,
            self.v1,
            self.i1,
            self.v2,
            self.i2,
            self.v3,
            self.i3,
            self.v4,
            self.i4,
        ]

    def from_nl(self, nl):
        self.noPositivo = int(nl[1])
        self.noNegativo = int(nl[2])
        self.v1 = float(nl[3])
        self.i1 = float(nl[4])
        self.v2 = float(nl[5])
        self.i2 = float(nl[6])
        self.v3 = float(nl[7])
        self.i3 = float(nl[8])
        self.v4 = float(nl[9])
        self.i4 = float(nl[10])
