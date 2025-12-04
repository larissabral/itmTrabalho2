import os

import numpy as np
import pytest

from src.controller.simulador import Simulador

BASE = os.path.dirname(__file__)


# Essa netlist manda informações de componente não implementado: K - transformador
def test_netlist5():
    # ('./netlist5.txt',2, 0.5e-4, 1e-4, [0,0,0], [1,2,3])
    netlist_path = os.path.join(BASE, "netlists", "netlist5.txt")
    # gabarito_path = os.path.join(BASE, 'resultados', 'resultado5.txt')

    with pytest.raises(ValueError) as exception:
        Simulador().simular_from_nl(netlist_path)

    # Compara a mensagem de erro diretamente
    assert str(exception.value).startswith(
        "Componente não implementado ou não reconhecido"
    )
