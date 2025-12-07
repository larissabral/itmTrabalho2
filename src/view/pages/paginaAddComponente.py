import enum

from nicegui import ui

from src.model.circuito import Circuito, Metodo
from src.model.simulacao import Simulacao

circuito = Circuito([], 0, 0, Metodo.BACKWARD_EULER)
simulacao = Simulacao()

sim_state = {
    "tempo_total": None,
    "passo": None,
    "passos_internos": None,
    "metodo": "BE",
    "uic": False,
    "simulacao_configurada": False,
}


def paginaAddComponente(painel):
    def configurar_simulacao():
        nl = [
            ".TRAN",
            tempo_total.value,
            passo.value,
            metodo.value,
            passos_internos.value,
            text_uic,
        ]
        if tempo_total.validate() and passo.validate() and passos_internos.validate():
            simulacao.from_nl(nl)
            sim_state.__setitem__("simulacao_configurada", True)
            bloco_config_simulacao.value = not sim_state["simulacao_configurada"]
            bloco_config_simulacao.update()
            ui.notify("Simulação configurada com sucesso!", color="green")
        else:
            ui.notify("Preencha todos os campos!", color="red")

    with ui.row().classes("w-full justify-center"):

        with ui.expansion(
            "Configurações da Simulação",
            icon="tune",
            value=not sim_state["simulacao_configurada"],
        ).classes(
            "w-full justify-center max-w-3xl text-2xl shadow-lg rounded-lg"
        ) as bloco_config_simulacao:
            with ui.row().classes("w-full justify-center"):
                with ui.card().classes("w-[900px] max-w-full p-6"):
                    with ui.row().classes("w-full gap-4 justify-center"):
                        with ui.column():
                            tempo_total = (
                                ui.input(
                                    "Tempo total de simulação (s)",
                                    placeholder="ex: 2.0",
                                    validation={
                                        "Campo obrigatório": lambda value: bool(value)
                                    },
                                    value=sim_state["tempo_total"],
                                    on_change=lambda e: sim_state.__setitem__(
                                        "tempo_total", e.value
                                    ),
                                )
                                .props("type=number")
                                .style("min-width: 250px")
                            )
                            passo = (
                                ui.input(
                                    "Passo de simulação (s)",
                                    placeholder="ex: 0.0001",
                                    validation={
                                        "Campo obrigatório": lambda value: bool(value)
                                    },
                                )
                                .props("type=number")
                                .style("min-width: 250px")
                            )
                        ui.element("div").classes("w-[30px]")
                        with ui.column():
                            metodo = ui.select(
                                ["BE", "FE", "TRAP"],
                                label="Método de integração",
                                value="BE",
                            ).style("min-width: 250px")
                            passos_internos = (
                                ui.input(
                                    "Número de passos internos",
                                    placeholder="ex: 1",
                                    validation={
                                        "Campo obrigatório": lambda value: bool(value)
                                    },
                                )
                                .props("type=number")
                                .style("min-width: 250px")
                            )

                    uic = ui.checkbox(
                        "UIC (usar condições iniciais durante a simulação)"
                    ).classes("text-sm")

                    text_uic = ""
                    if uic.value:
                        text_uic = "UIC"

                    with ui.row().classes("w-full justify-center"):
                        ui.button(
                            "Salvar", on_click=lambda: configurar_simulacao()
                        ).classes("primary")

    with ui.row().classes("w-full justify-center"):
        with ui.dropdown_button("Adicionar Componente", icon="add", auto_close=True):
            for componente in Componente:
                ui.item(
                    componente.value,
                    on_click=lambda c=componente: selecionar_componente(c.value),
                )

    with ui.row().classes("w-full justify-center"):
        ui.button("Gerar netlist", on_click=lambda: gerar_netlist_texto()).classes(
            "justify-center"
        )

        ui.button("Simular circuito", on_click=lambda: simular_circuito()).classes(
            "justify-center"
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


def gerar_netlist_texto():
    if not circuito.elementos:
        ui.notify("Adicione componentes para gerar netlist!", color="red")
    else:
        # gera netlist: circuito.to_nl().append(simulacao.to_nl())
        ui.notify("Netlist gerada!", color="green")


def simular_circuito():
    if not sim_state["simulacao_configurada"]:
        ui.notify("Configure os parâmetros da simulação antes de simular!", color="red")
    elif not circuito.elementos:
        ui.notify("Adicione componentes para simular o circuito!", color="red")
    else:
        ui.notify("Simulação em andamento...")
        circuito.resolver(simulacao)
