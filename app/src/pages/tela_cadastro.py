import sys
import base64

from pathlib import Path

import flet as ft

DIR_ROOT = str(Path(__file__).parents[2])
if DIR_ROOT not in sys.path:
    sys.path.append(DIR_ROOT)

from src.classes.usuario import (
    Usuario,
)


def tela_cadastro(page: ft.Page, db_connection):
    page.title = "Tela de Cadastro"
    page.window_width = 480
    page.window_height = 800
    page.bgcolor = "#FFFFFF"  # Configura o fundo branco para a página

    page.fonts = {
        "Sen Extra Bold": "fonts/Sen-ExtraBold.ttf",
        "Sen Medium": "fonts/Sen-Medium.ttf",
    }

    with open("assets/ebook.png", "rb") as file:
        image_ebook = file.read()

    def realizar_cadastro(e):
        nome = name_input.value
        username = username_input.value
        email = email_input.value
        password = password_input.value

        # Cria um novo usuário no banco de dados
        novo_usuario = Usuario(nome, username, email, password)
        novo_usuario.salvar()
        page.go("/cadastro_sucesso")

    # Componentes da tela de cadastro
    name_input = ft.TextField(
        label="Nome",
        width=300,
        color="#000000",
        label_style=ft.TextStyle(color="#03103F"),
        border=ft.InputBorder.UNDERLINE,
    )

    username_input = ft.TextField(
        label="Usuário",
        width=300,
        color="#000000",
        label_style=ft.TextStyle(color="#03103F"),
        border=ft.InputBorder.UNDERLINE,
    )

    email_input = ft.TextField(
        label="E-mail",
        width=300,
        color="#000000",
        label_style=ft.TextStyle(color="#03103F"),
        border=ft.InputBorder.UNDERLINE,
    )

    password_input = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        width=300,
        color="#000000",
        label_style=ft.TextStyle(color="#03103F"),
        border=ft.InputBorder.UNDERLINE,
    )

    signup_button = ft.ElevatedButton(
        text="Concluir",
        on_click=realizar_cadastro,
        color="#03103F",
        bgcolor="#D6E0E2",
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(font_family="Sen Extra Bold", weight="bold")
        ),
    )

    voltar_button = ft.ElevatedButton(
        text="Voltar",
        on_click=lambda _: page.go("/"),  # Volta para a tela de login
        color="black",
        bgcolor="#D6E0E2",
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(font_family="Sen Extra Bold", weight="bold")
        ),
    )

    resultado = ft.Text()

    # Container principal para os elementos de cadastro
    content = ft.Container(
        bgcolor="#FFFFFF",  # Fundo branco
        border_radius=ft.border_radius.all(20),  # Bordas arredondadas
        padding=20,  # Espaçamento interno
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        "Cadastro",
                        size=40,
                        weight="bold",
                        color="#03103F",
                        font_family="Sen Extra Bold",
                    ),
                    margin=ft.margin.only(top=10),
                ),
                ft.Container(
                    content=ft.Image(
                        src_base64=base64.b64encode(image_ebook).decode("utf-8"),
                        width=250,  # Reduzir o tamanho para melhorar o layout
                        height=250,
                    ),
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(
                        bottom=10
                    ),  # Margem inferior para espaçamento
                ),
                name_input,
                username_input,
                email_input,
                password_input,
                ft.Container(content=signup_button, margin=ft.margin.only(top=10)),
                ft.Container(content=voltar_button, margin=ft.margin.only(top=10)),
                resultado,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,  # Espaço entre os elementos
        ),
    )

    # Retorna o layout com fundo branco que preenche a tela inteira
    return ft.Container(
        expand=True,  # Certifica-se de que o fundo preencha toda a tela
        bgcolor="#FFFFFF",  # Fundo branco que cobre toda a tela
        border_radius=ft.border_radius.all(20),  # Bordas arredondadas no layout
        padding=20,
        content=ft.Row(
            [content],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,  # Garante que o conteúdo seja centralizado e preencha o espaço
        ),
    )


def tela_cadastro_sucesso(page: ft.Page):
    page.title = "Cadastro Bem-Sucedido"
    page.window_width = 480
    page.window_height = 800
    page.bgcolor = "#FFFFFF"

    with open("assets/welcome.png", "rb") as file:
        image_welcome = file.read()

    content = ft.Container(
        bgcolor="#FFFFFF",
        border_radius=ft.border_radius.all(20),  # Bordas arredondadas
        padding=20,  # Preenchimento interno para evitar que o conteúdo encoste nas bordas
        border=ft.BorderSide(
            2, color="#D6E0E2"
        ),  # Adiciona uma borda visível para destacar o arredondamento
        content=ft.Column(
            [
                ft.Text(
                    "Bem vindo(a)!",
                    size=40,
                    weight="bold",
                    color="black",
                    font_family="Sen Extra Bold",
                ),
                ft.Text(
                    "Cadastro realizado com sucesso!",
                    size=25,
                    weight="bold",
                    color="black",
                    font_family="Sen Extra Bold",
                ),
                ft.Image(
                    src_base64=base64.b64encode(image_welcome).decode("utf-8"),
                    width=300,
                    height=300,
                ),
                ft.ElevatedButton(
                    text="Voltar à página inicial",
                    on_click=lambda _: page.go("/"),
                    color="black",
                    bgcolor="#D6E0E2",
                    width=280,  # Ajuste da largura do botão
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(
                            font_family="Sen Extra Bold", weight="bold"
                        )
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centraliza os elementos verticalmente
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            spacing=20,  # Espaçamento entre os elementos
        ),
    )

    return ft.Container(
        expand=True,
        bgcolor="#FFFFFF",
        content=ft.Row(  # Centraliza o conteúdo horizontalmente e verticalmente
            [content],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,  # Expande para preencher a tela inteira
        ),
        border_radius=ft.border_radius.all(
            20
        ),  # Adiciona bordas arredondadas ao contêiner principal
        border=ft.BorderSide(
            2, color="#D6E0E2"
        ),  # Adiciona uma borda ao redor do layout principal
    )
