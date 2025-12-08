from nicegui import ui


def header():
    with ui.element("div").classes("items-center justify-center w-full"):
        with ui.column().classes("items-center"):
            ui.label("Protótipo de Simulador de Circuitos Elétricos").classes(
                "text-5xl font-bold text-center"
            )
            ui.label(
                "Desenvolvido como trabalho final da disciplina de Intrumentação e Técnicas de Medidas em 2025.2"
            ).classes("text-lg text-gray-600 text-center")
