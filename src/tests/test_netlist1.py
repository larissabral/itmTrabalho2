import os

import numpy as np

from src.controller.simulador import Simulador

BASE = os.path.dirname(__file__)


def test_netlist1():
    # ('./netlist1.txt',2, 0.2e-3, 1e-4, [1,0.5], [1,2])
    netlist_path = os.path.join(BASE, "netlists", "netlist1.txt")
    gabarito_path = os.path.join(BASE, "resultados", "resultado1.txt")

    resultados = Simulador().simular_from_nl(netlist_path)

    with open(gabarito_path) as gabarito:
        # print(gabarito.read())
        # print(resultados)
        assert np.array_equal(resultados, gabarito.read())
        # assert np.allclose(resultados,gabarito.read())
