import enum

from nicegui import ui


def paginaAddComponente(painel):
    painel.disable()
    with ui.dropdown_button("Adicionar Componente", icon="add", auto_close=True):
        for componente in Componente:
            ui.item(
                componente.value,
                on_click=lambda c=componente: selecionar_componente(c.value),
            )


class Componente(enum.Enum):
    R = "Resistor"
    N = "ResistorNaoLinear"

    I_DC = "FonteCorrenteDC"
    I_SIN = "FonteCorrenteSenoidal"
    I_PULSE = "FonteCorrentePulso"

    V_DC = "FonteTensaoDC"
    V_SIN = "FonteTensaoSenoidal"
    V_PULSE = "FonteTensaoPulso"

    G = "FonteCorrenteControladaTensao"
    F = "FonteCorrenteControladaCorrente"
    E = "FonteTensaoControladaTensao"
    H = "FonteTensaoControladaCorrente"

    C = "Capacitor"
    L = "Indutor"
    AmpOp = "AmpOpIdeal"  # O
    D = "Diodo"


def selecionar_componente(nome):
    ui.notify(f"Componente selecionado: {nome}")
