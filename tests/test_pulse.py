import os

from src.controller.simulador import Simulador

BASE = os.path.dirname(__file__)


def test_pulse():
    netlist_path = os.path.join(BASE, "netlists", "pulse.net")
    gabarito_path = os.path.join(BASE, "resultados", "pulse.sim")

    resultados = Simulador().simular_from_nl(netlist_path)

    with open(gabarito_path) as gabarito:
        assert resultados == gabarito.read()
