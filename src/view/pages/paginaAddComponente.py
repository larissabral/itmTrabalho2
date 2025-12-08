import tempfile

import numpy as np
from nicegui import ui
from nicegui.elements.input import Input
from nicegui.elements.label import Label

from src.model.ampOpIdeal import AmpOpIdeal
from src.model.capacitor import Capacitor
from src.model.circuito import Circuito, Metodo
from src.model.diodo import Diodo
from src.model.fonteCorrenteControladaCorrente import FonteCorrenteControladaCorrente
from src.model.fonteCorrenteControladaTensao import FonteCorrenteControladaTensao
from src.model.fonteCorrenteDC import FonteCorrenteDC
from src.model.fonteCorrentePulso import FonteCorrentePulso
from src.model.fonteCorrenteSenoidal import FonteCorrenteSenoidal
from src.model.fonteTensaoControladaCorrente import FonteTensaoControladaCorrente
from src.model.fonteTensaoControladaTensao import FonteTensaoControladaTensao
from src.model.fonteTensaoDC import FonteTensaoDC
from src.model.fonteTensaoPulso import FonteTensaoPulso
from src.model.fonteTensaoSenoidal import FonteTensaoSenoidal
from src.model.indutor import Indutor
from src.model.resistor import Resistor
from src.model.resistorNaoLinear import ResistorNaoLinear
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
    global container_blocos

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
            try:
                simulacao.from_nl(nl)
                sim_state.__setitem__("simulacao_configurada", True)
                bloco_config_simulacao.value = not sim_state["simulacao_configurada"]
                bloco_config_simulacao.update()
                ui.notify("Simulação configurada com sucesso!", color="green")
            except Exception as e:
                ui.notify(f"Erro: {e}", color="negative")
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

    ui.element("div").classes("h-[30px]")

    with ui.row().classes("w-full justify-center"):
        with ui.dropdown_button("Adicionar Componente", icon="add", auto_close=True):
            for componente in CAMPOS_POR_COMPONENTE.keys():
                ui.item(
                    componente,
                    on_click=lambda item=componente: criar_bloco_componente(item),
                )

    container_blocos = ui.column().classes("w-full items-center gap-4 justify-center")

    ui.element("div").classes("h-[30px]")

    with ui.row().classes("w-full justify-center"):
        ui.button("Gerar netlist", on_click=lambda: gerar_netlist_texto()).classes(
            "justify-center"
        )

        ui.button("Simular circuito", on_click=lambda: simular_circuito()).classes(
            "justify-center"
        )


CAMPOS_POR_COMPONENTE = {
    "Resistor": ["Nome", "Nó +", "Nó -", "Resistência (Ω)"],
    "ResistorNaoLinear": [
        "Nome",
        "Nó +",
        "Nó -",
        "V1",
        "I1",
        "V2",
        "I2",
        "V3",
        "I3",
        "V4",
        "I4",
    ],
    "FonteCorrenteDC": ["Nome", "Nó +", "Nó -", "TipoFonte", "Corrente (A)"],
    "FonteCorrenteSenoidal": [
        "Nome",
        "Nó +",
        "Nó -",
        "TipoFonte",
        "NivelContinuo",
        "Amplitude",
        "Frequencia",
        "Atraso",
        "Coef_alpha",
        "Fase",
        "NumeroCiclos",
    ],
    "FonteCorrentePulso": [
        "Nome",
        "Nó +",
        "Nó -",
        "TipoFonte",
        "Valor1",
        "Valor2",
        "Atraso",
        "TempoSubida",
        "TempoDescida",
        "TempoLigado",
        "Periodo",
        "NumeroCiclos",
    ],
    "FonteTensaoDC": ["Nome", "Nó +", "Nó -", "TipoFonte", "Tensão (V)"],
    "FonteTensaoSenoidal": [
        "Nome",
        "Nó +",
        "Nó -",
        "TipoFonte",
        "NivelContinuo",
        "Amplitude",
        "Frequencia",
        "Atraso",
        "Coef_alpha",
        "Fase",
        "NumeroCiclos",
    ],
    "FonteTensaoPulso": [
        "Nome",
        "Nó +",
        "Nó -",
        "TipoFonte",
        "Valor1",
        "Valor2",
        "Atraso",
        "TempoSubida",
        "TempoDescida",
        "TempoLigado",
        "Periodo",
        "NumeroCiclos",
    ],
    "FonteCorrenteControladaTensao": [
        "Nome",
        "Nó Corrente +",
        "Nó Corrente -",
        "Nó Controle +",
        "Nó Controle -",
        "Transcondutância",
    ],
    "FonteCorrenteControladaCorrente": [
        "Nome",
        "Nó Corrente +",
        "Nó Corrente -",
        "Nó Controle +",
        "Nó Controle -",
        "GanhoCorrente",
    ],
    "FonteTensaoControladaTensao": [
        "Nome",
        "Nó Corrente +",
        "Nó Corrente -",
        "Nó Controle +",
        "Nó Controle -",
        "GanhoTensão",
    ],
    "FonteTensaoControladaCorrente": [
        "Nome",
        "Nó Corrente +",
        "Nó Corrente -",
        "Nó Controle +",
        "Nó Controle -",
        "Transresistência",
    ],
    "Capacitor": ["Nome", "Nó +", "Nó -", "Capacitância (F)", "TensãoInicial"],
    "Indutor": ["Nome", "Nó +", "Nó -", "Indutância (H)", "CorrenteInicial"],
    "AmpOpIdeal": ["Nome", "Nó +", "Nó -", "Nó Saída"],
    "Diodo": ["Nome", "Nó +", "Nó -"],
}

componentes_ui = []
container_blocos = None


def criar_bloco_componente(nome_componente):
    campos = CAMPOS_POR_COMPONENTE[nome_componente]

    with container_blocos:
        with ui.card().classes("shadow-lg rounded-lg") as bloco:
            with ui.row().classes("items-center gap-4 w-full justify-center"):
                estado = {"editavel": True}

                inputs = []

                inputs.append(ui.label(nome_componente))

                for campo in campos:
                    if campo == "TipoFonte":
                        if (
                            nome_componente == "FonteCorrenteDC"
                            or nome_componente == "FonteTensaoDC"
                        ):
                            inp = ui.label("DC")
                        elif (
                            nome_componente == "FonteCorrenteSenoidal"
                            or nome_componente == "FonteTensaoSenoidal"
                        ):
                            inp = ui.label("SIN")
                        else:
                            inp = ui.label("PULSE")
                    else:
                        inp = ui.input(
                            campo,
                            validation={"Campo obrigatório": lambda value: bool(value)},
                        ).style("width: 130px")
                    inputs.append(inp)

                botao_salvar = ui.button("Salvar").props(
                    f'color={"blue" if not estado["editavel"] else "green"}'
                )

                botao_excluir = ui.button("Excluir", color="red")

                def salvar():
                    estado["editavel"] = False
                    for fields in inputs:
                        if isinstance(fields, Input):
                            fields.disable()
                    botao_salvar.text = "Editar"
                    botao_salvar.props("color=blue")
                    botao_salvar.update()

                def editar():
                    estado["editavel"] = True
                    for fields in inputs:
                        if isinstance(fields, Input):
                            fields.enable()
                    botao_salvar.text = "Salvar"
                    botao_salvar.props("color=green")
                    botao_salvar.update()

                def clique_salvar_editar():
                    if estado["editavel"]:
                        if not validar_campos(inputs):
                            return
                        salvar()
                    else:
                        editar()

                def excluir():
                    bloco.delete()
                    componentes_ui.remove(bloco)

                botao_salvar.on_click(clique_salvar_editar)
                botao_excluir.on_click(excluir)

            componentes_ui.append(bloco)

            bloco.meta = {
                "nome": nome_componente,
                "inputs": inputs[1:],
            }


def validar_campos(inputs):
    for field in inputs:
        if isinstance(field, Input):
            if not field.validate():
                ui.notify(f"Preencha o campo: {field.label}", color="red")
                return False
    return True


def selecionar_componente(nome):
    ui.notify(f"Componente selecionado: {nome}")


def processar_componentes():
    circuito.elementos = []

    for bloco in componentes_ui:
        adicionar_componente_circuito(bloco)


def adicionar_componente_circuito(bloco):
    nome_componente = bloco.meta["nome"]
    valores = []

    for comp in bloco.meta["inputs"]:
        if isinstance(comp, Input):
            valores.append(comp.value)

        elif isinstance(comp, Label):
            valores.append(comp.text)

    if nome_componente == "Resistor":
        circuito.adiciona_componente(Resistor().from_nl(valores))
    elif nome_componente == "ResistorNaoLinear":
        circuito.possuiElementoNaoLinear = True
        circuito.adiciona_componente(ResistorNaoLinear().from_nl(valores))
    elif nome_componente == "FonteCorrenteDC":
        circuito.adiciona_componente(FonteCorrenteDC().from_nl(valores))
    elif nome_componente == "FonteCorrenteSenoidal":
        circuito.adiciona_componente(FonteCorrenteSenoidal().from_nl(valores))
    elif nome_componente == "FonteCorrentePulso":
        circuito.adiciona_componente(FonteCorrentePulso().from_nl(valores))
    elif nome_componente == "FonteTensaoDC":
        circuito.adiciona_componente(FonteTensaoDC().from_nl(valores))
    elif nome_componente == "FonteTensaoSenoidal":
        circuito.adiciona_componente(FonteTensaoSenoidal().from_nl(valores))
    elif nome_componente == "FonteTensaoPulso":
        circuito.adiciona_componente(FonteTensaoPulso().from_nl(valores))
    elif nome_componente == "FonteCorrenteControladaTensao":
        circuito.adiciona_componente(FonteCorrenteControladaTensao().from_nl(valores))
    elif nome_componente == "FonteCorrenteControladaCorrente":
        circuito.adiciona_componente(FonteCorrenteControladaCorrente().from_nl(valores))
    elif nome_componente == "FonteTensaoControladaTensao":
        circuito.adiciona_componente(FonteTensaoControladaTensao().from_nl(valores))
    elif nome_componente == "FonteTensaoControladaCorrente":
        circuito.adiciona_componente(FonteTensaoControladaCorrente().from_nl(valores))
    elif nome_componente == "Capacitor":
        circuito.adiciona_componente(Capacitor().from_nl(valores))
    elif nome_componente == "Indutor":
        circuito.adiciona_componente(Indutor().from_nl(valores))
    elif nome_componente == "AmpOpIdeal":
        circuito.adiciona_componente(AmpOpIdeal().from_nl(valores))
    elif nome_componente == "Diodo":
        circuito.possuiElementoNaoLinear = True
        circuito.adiciona_componente(Diodo().from_nl(valores))
    else:
        ui.notify("Ocorreu um erro ao adicionar componente ao circuito!", color="red")


def gerar_netlist_texto():
    processar_componentes()
    if not circuito.elementos:
        ui.notify("Adicione componentes para gerar netlist!", color="red")
    else:
        circuito.calculaQntIncognitasENos()
        circuito.simulacao = simulacao
        netlist = circuito.to_nl()

        baixa_netlist(netlist)

        ui.notify("Netlist gerada!", color="green")


def simular_circuito():
    if sim_state["simulacao_configurada"]:
        processar_componentes()
        if not circuito.elementos:
            ui.notify("Adicione componentes para simular o circuito!", color="red")
        else:
            ui.notify("Simulação em andamento...")
            try:
                circuito.simulacao = simulacao
                resultado = circuito.resolver()
                resultado = resultado.transpose()
                baixa_resultado(resultado)

                ui.notify("Simulação concluída com sucesso!", color="green")

            except Exception as e:
                ui.notify(f"Ocorreu um erro na simulação: {e}", color="negative")
                print(e)

    else:
        ui.notify("Configure os parâmetros da simulação antes de simular!", color="red")


def baixa_resultado(resultado):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")

    np.savetxt(temp.name, resultado, fmt="%.10f")

    ui.download(temp.name, filename="resultado_simulacao.txt")


def baixa_netlist(netlist):
    linhas_formatadas = []

    for item in netlist:
        if isinstance(item, list):
            linhas_formatadas.append(" ".join(str(x) for x in item))
        else:
            linhas_formatadas.append(str(item))

    texto_netlist = "\n".join(linhas_formatadas)

    temp = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt")
    temp.write(texto_netlist)
    temp.close()

    ui.download(temp.name, filename="netlist.txt")
