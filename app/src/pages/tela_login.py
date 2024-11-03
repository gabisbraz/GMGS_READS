import sys
import base64

from pathlib import Path

import flet as ft

DIR_ROOT = str(Path(__file__).parents[2])
if DIR_ROOT not in sys.path:
    sys.path.append(DIR_ROOT)

from src.classes.usuario import buscar_usuario, Usuario


def tela_login(page: ft.Page):

    page.title = "Tela de Login"
    page.window_width = 480
    page.window_height = 800
    page.bgcolor = "#FFFFFF"

    page.fonts = {
        "Sen Extra Bold": "fonts/Sen-ExtraBold.ttf",
        "Sen Medium": "fonts/Sen-Medium.ttf",
    }

    with open("assets/kids_reading.png", "rb") as file:
        image_kids_reading = file.read()

    def realizar_login(e):
        username = username_input.value
        password = password_input.value

        # # Busca o usuário no banco de dados
        # usuario_encontrado = buscar_usuario(username)

        if True:
            # Verifica se a senha está correta
            if True:
                # if Usuario.verificar_senha(password, usuario_encontrado["password"]):
                # Redireciona para a tela de sucesso
                page.go("/login_sucesso")
            else:
                # Exibe o aviso de senha incorreta
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(
                        "Senha incorreta. Tente novamente.", color="#FFFFFF"
                    ),
                    bgcolor="#dc3545",  # Fundo vermelho para erro
                )
                page.snack_bar.open = True
        else:
            # Exibe o aviso de usuário não encontrado
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Usuário não encontrado.", color="#FFFFFF"),
                bgcolor="#dc3545",  # Fundo vermelho para erro
            )
            page.snack_bar.open = True

        page.update()

    # Componentes da tela de login
    username_input = ft.TextField(
        label="Usuário",
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

    login_button = ft.ElevatedButton(
        text="Concluir",
        on_click=realizar_login,
        color="black",
        bgcolor="#D6E0E2",
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(font_family="Sen Extra Bold", weight="bold")
        ),
    )

    signup_button = ft.ElevatedButton(
        text="Cadastrar-se",
        on_click=lambda _: page.go("/signup"),  # Redireciona para a tela de cadastro
        color="black",
        bgcolor="#D6E0E2",
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(font_family="Sen Extra Bold", weight="bold")
        ),
    )

    resultado = ft.Text()

    content = ft.Container(
        bgcolor="#FFFFFF",  # Fundo branco
        border_radius=ft.border_radius.all(20),  # Bordas arredondadas
        padding=20,  # Adiciona um espaçamento interno
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        "Login",
                        size=50,
                        weight="bold",
                        color="#03103F",
                        font_family="Sen Extra Bold",
                    ),
                    margin=ft.margin.only(top=40),
                ),
                ft.Container(
                    content=ft.Image(
                        src_base64=base64.b64encode(image_kids_reading).decode("utf-8"),
                        width=300,
                        height=300,
                    ),
                    alignment=ft.alignment.center,
                ),
                username_input,
                password_input,
                login_button,
                signup_button,
                resultado,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,  # Espaço entre os elementos
        ),
    )

    return ft.Container(
        expand=True,  # Faz com que o contêiner preencha toda a tela
        bgcolor="#FFFFFF",  # Fundo branco para toda a tela
        border_radius=ft.border_radius.all(20),  # Bordas arredondadas na tela
        padding=20,
        content=ft.Row(
            [content],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,  # Faz com que o conteúdo se expanda na tela
        ),
    )


import flet as ft


def tela_login_sucesso(page: ft.Page):
    page.title = "Login Bem-Sucedido"
    page.window.width = 480
    page.window.height = 800
    page.bgcolor = "#FFFFFF"

    def handle_navigation(e, page):
        index = e.control.selected_index
        if index == 0:
            page.go("/explore")
        elif index == 1:
            page.go("/recommendations")
        elif index == 2:
            page.go("/profile")

    # Define a barra de navegação com destinos
    navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Explore"),
            ft.NavigationBarDestination(icon=ft.icons.BOOKMARK_BORDER, label="Rec."),
            ft.NavigationBarDestination(
                icon=ft.icons.PERSON_OFF_OUTLINED, label="Profile"
            ),
        ],
        on_change=lambda e: handle_navigation(e, page),
    )

    # Função para tratar a navegação baseada no índice selecionado
