from nicegui import ui

from src.view.pages.paginaAddComponente import paginaAddComponente
from src.view.pages.paginaAddNetlist import paginaAddNetlist


def abas():
    with ui.tabs().classes("w-full") as tabs:
        aba1 = ui.tab("Adicionar netlist")
        aba2 = ui.tab("Adicionar componentes")

    with ui.tab_panels(tabs, value=aba1).classes("w-full"):
        with ui.tab_panel(aba1) as painel1:
            paginaAddNetlist(painel1)

        with ui.tab_panel(aba2) as painel2:
            paginaAddComponente(painel2)
