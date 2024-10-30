import sys
import base64

from pathlib import Path

import flet as ft
import mysql.connector

from loguru import logger


DIR_ROOT = str(Path(__file__).parents[0])
if DIR_ROOT not in sys.path:
    sys.path.append(DIR_ROOT)

from src.pages.tela_login import tela_login, tela_login_sucesso
from src.pages.tela_cadastro import tela_cadastro, tela_cadastro_sucesso
from src.pages.tela_busca import tela_busca
from src.pages.detalhes_livro import detalhes_livro
from src.pages.discover import discover_livros
from src.pages.busca_livros_sugestao import busca_livros_sugestao


def create_connection():
    logger.info("ESTABELECENDO CONEXÃO COM DB")
    connection = mysql.connector.connect(
        host="database-1.ctj2rmaeyrwc.us-east-1.rds.amazonaws.com",
        user="admin",
        password="admin123",
        database="nxt_reads_db",
    )
    logger.info("CONEXÃO ESTABELECIDA COM DB")
    return connection


def main(page: ft.Page):

    page.fonts = {
        "Sen Extra Bold": "fonts/Sen-ExtraBold.ttf",
        "Sen Medium": "fonts/Sen-Medium.ttf",
    }

    with open("assets/literature.png", "rb") as file:
        image = file.read()

    def home_screen(page: ft.Page):
        page.window_width = 480
        page.window_height = 800
        page.window_resizable = False
        page.window_always_on_top = True

        # Envolve todo o conteúdo em um Container com bordas arredondadas
        content_container = ft.Container(
            expand=True,
            bgcolor="#FFFFFF",  # Define o fundo do Container
            border_radius=ft.border_radius.all(20),  # Define o raio das bordas
            clip_behavior=ft.ClipBehavior.HARD_EDGE,  # Garante que o conteúdo não ultrapasse as bordas
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Welcome to",
                                    size=30,
                                    weight="bold",
                                    color="black",
                                    font_family="Sen Extra Bold",
                                ),
                                ft.Text(
                                    "NXT",
                                    size=60,
                                    weight="bold",
                                    color="black",
                                    font_family="Sen Extra Bold",
                                ),
                                ft.Text(
                                    "Reads",
                                    size=60,
                                    weight="bold",
                                    color="black",
                                    font_family="Sen Extra Bold",
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0,
                        ),
                    ),
                    ft.Container(
                        content=ft.Image(
                            src_base64=base64.b64encode(image).decode("utf-8"),
                            width=300,
                            height=300,
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        alignment=ft.alignment.center,
                    ),
                    ft.Text(
                        "Find your next favorite book!",
                        size=15,
                        weight="bold",
                        color="black",
                        font_family="Sen Medium",
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.ElevatedButton(
                                    text="Login",
                                    on_click=lambda _: page.go("/login"),
                                    bgcolor="#D6E0E2",
                                    color="black",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(
                                            radius=15
                                        ),  # Cantos arredondados nos botões
                                        text_style=ft.TextStyle(
                                            size=20,
                                            font_family="Sen Extra Bold",
                                            weight="bold",
                                        ),
                                    ),
                                ),
                                ft.ElevatedButton(
                                    text="Cadastre-se",
                                    on_click=lambda _: page.go("/signup"),
                                    bgcolor="#D6E0E2",
                                    color="black",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(
                                            radius=15
                                        ),  # Cantos arredondados nos botões
                                        text_style=ft.TextStyle(
                                            size=20,
                                            font_family="Sen Extra Bold",
                                            weight="bold",
                                        ),
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
        )

        # Retorna o Container com as bordas arredondadas
        return ft.Container(
            expand=True, content=content_container, alignment=ft.alignment.center
        )

    def route_change(route):
        page.views.clear()

        # Define rotas
        if page.route == "/":
            page.views.append(ft.View("/", [home_screen(page)]))  # Tela inicial
        elif page.route == "/login":
            page.views.append(
                ft.View("/login", [tela_login(page, create_connection())])
            )
        elif page.route == "/signup":
            page.views.append(
                ft.View("/signup", [tela_cadastro(page, create_connection())])
            )
        elif page.route == "/login_sucesso":
            page.views.append(ft.View("/login_sucesso", [tela_login_sucesso(page)]))
        elif page.route == "/cadastro_sucesso":
            page.views.append(
                ft.View(
                    "/cadastro_sucesso",
                    [tela_cadastro_sucesso(page)],
                )
            )
        elif page.route == "/busca_livros":
            page.views.append(ft.View("/busca_livros", [tela_busca(page)]))
        elif page.route == "/discover":
            page.views.append(
                ft.View("/discover", [discover_livros(page, create_connection())])
            )
        elif page.route.startswith("/detalhes_livro/"):
            book_id = page.route.split("/")[-1]
            page.views.append(
                ft.View(
                    f"/detalhes_livro/{book_id}",
                    [detalhes_livro(page, create_connection(), book_id)],
                )
            )
        elif page.route == "/busca_livros_sugestao":
            page.views.append(
                ft.View(
                    "/busca_livros_sugestao",
                    [busca_livros_sugestao(page, create_connection())],
                )
            )

        page.update()

    page.on_route_change = route_change
    page.go("/")  # Rota inicial


ft.app(target=main)
