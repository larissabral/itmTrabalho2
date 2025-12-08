from nicegui import ui

from src.view.components.header import header
from src.view.pages.abas import abas


@ui.page("/")
def main_page():
    header()

    abas()


ui.run(port=8080, reload=False)
