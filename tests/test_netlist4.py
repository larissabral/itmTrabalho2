import os

import numpy as np

from src.controller.simulador import Simulador

BASE = os.path.dirname(__file__)


def test_netlist4():
    # ('./netlist4.txt',2, 0.5e-4, 1e-4, [0,0,0], [1,3])
    netlist_path = os.path.join(BASE, "netlists", "netlist4.txt")
    gabarito_path = os.path.join(BASE, "resultados", "resultado4.txt")

    resultados = Simulador().simular_from_nl(netlist_path)

    with open(gabarito_path) as gabarito:
        # print(gabarito.read())
        # print(resultados)
        assert np.array_equal(resultados, gabarito.read())
        # assert np.allclose(resultados,gabarito.read())
