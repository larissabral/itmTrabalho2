import os

import numpy as np

from src.controller.simulador import Simulador

BASE = os.path.dirname(__file__)


def test_chua():
    netlist_path = os.path.join(BASE, "netlists", "chua.net")
    gabarito_path = os.path.join(BASE, "resultados", "chua.sim")

    resultados = Simulador().simular_from_nl(netlist_path)

    with open(gabarito_path) as gabarito:
        assert np.array_equal(resultados, gabarito.read())
