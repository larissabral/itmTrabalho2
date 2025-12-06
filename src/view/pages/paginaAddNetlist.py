import os
import tempfile
from pathlib import Path

from nicegui import ui

from src.controller.simulador import Simulador


def paginaAddNetlist(painel):
    base_dir = Path(__file__).resolve().parents[2]
    caminho_arquivo = os.path.join(base_dir, "view/especsNetlist.txt")

    def ler_conteudo_arquivo(nomeArquivo):
        try:
            with open(nomeArquivo, "r") as arquivo:
                return arquivo.read()
        except FileNotFoundError:
            return f"Erro: O arquivo '{nomeArquivo}' não foi encontrado."
        except Exception as e:
            return f"Ocorreu um erro: {e}"

    with ui.dialog() as modal_especs:
        with ui.card():
            texto_modal_especs = ler_conteudo_arquivo(caminho_arquivo)
            ui.markdown(texto_modal_especs)
            ui.button("Fechar", on_click=modal_especs.close).classes(
                "w-full justify-center"
            )

    ui.element("div").classes("h-[20px]")

    with ui.row().classes("w-full justify-center"):
        ui.label("Carregue o arquivo ou escreva a netlist para simular.").classes(
            "text-lg text-gray-600 text-center"
        )
        ui.button("Especificações da netlist", on_click=modal_especs.open)

    ui.element("div").classes("h-[50px]")

    with ui.row().classes("w-full justify-center"):
        with ui.card():
            ui.label("Carregar arquivo:").classes("text-lg font-bold")
            ui.upload(
                max_files=1,
                auto_upload=True,
                on_upload=lambda e: submeter_netlist_arquivo(e),
            ).classes("border p-4 rounded-md").props('accept=".txt"')

        ui.element("div").classes("w-[30px]")
        ui.separator().props("vertical")
        ui.element("div").classes("w-[30px]")

        with ui.card():
            ui.label("Ou copiar netlist:").classes("text-lg font-bold mt-4")
            texto = ui.textarea(placeholder="Digite aqui sua netlist...").classes(
                "w-full h-40 border rounded-md p-2"
            )

            # TODO: verificar texto vazio

            ui.button(
                "Submeter", on_click=lambda: submeter_netlist_texto(texto.value)
            ).classes("w-full justify-center")


def submeter_netlist_arquivo(evento):
    ui.notify(
        f"Netlist submetida a partir de arquivo {evento.file.name}! Simulando circuito..."
    )
    try:
        temp_path = os.path.join(tempfile.gettempdir(), evento.file.name)

        with open(temp_path, "wb") as f:
            f.write(evento.file._data)

        resultado = Simulador().simular_from_nl(temp_path)

        baixa_resultado(resultado)

        # ui.notify(f"{resultado}")

    except Exception as e:
        ui.notify(f"Ocorreu um erro na simulação: {e}", color="negative")
        print(e)


def submeter_netlist_texto(texto):
    try:
        if not texto.strip():
            ui.notify("O texto está vazio!", color="negative")
            return

        ui.notify("Netlist enviada! Simulando circuito...")

        temp_path = os.path.join(tempfile.gettempdir(), "netlist_texto.txt")

        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(texto)

        resultado = Simulador().simular_from_nl(temp_path)

        baixa_resultado(resultado)

        ui.notify("Simulação concluída com sucesso!", color="green")

        # ui.notify(str(resultado))

    except Exception as e:
        ui.notify(f"Ocorreu um erro na simulação: {e}", color="negative")
        print(e)


def baixa_resultado(resultado):
    tmp_path_resultado = tempfile.mktemp(suffix=".txt")

    with open(tmp_path_resultado, "w", encoding="utf-8") as f:
        f.write(resultado)

    ui.download(tmp_path_resultado, filename="resultado_simulacao.txt")
