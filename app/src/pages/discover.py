import mysql.connector
from loguru import logger
import flet as ft


def discover_livros(page: ft.Page, connection):
    """
    Página para descobrir vários livros com informações básicas.
    Ao clicar em um livro, redireciona para a página de detalhes do livro.
    """
    page.title = "Descobrir Livros"
    page.bgcolor = "#FFFFFF"
    page.window_width = 480
    page.window_height = 800
    page.window_resizable = False
    page.window_always_on_top = True

    cursor = connection.cursor(dictionary=True)
    query = "SELECT bookID, title, authors, average_rating FROM Livros LIMIT 10"
    cursor.execute(query)
    livros = cursor.fetchall()
    cursor.close()

    # Criando uma lista de botões para os livros
    lista_livros = []
    for livro in livros:
        lista_livros.append(
            ft.Container(
                content=ft.ElevatedButton(
                    text=f"{livro['title']} - {livro['authors']}",
                    on_click=lambda e, book_id=livro["bookID"]: page.go(
                        f"/detalhes_livro/{book_id}"
                    ),
                    bgcolor="#D6E0E2",
                    color="black",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        text_style=ft.TextStyle(
                            size=18, font_family="Sen Medium", weight="bold"
                        ),
                    ),
                ),
            )
        )

    content = ft.Container(
        bgcolor="#FFFFFF",
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        "Descobrir Livros", size=40, weight="bold", color="#03103F"
                    ),
                    margin=ft.margin.only(top=50, bottom=20),
                ),
                ft.Column(
                    lista_livros,
                    spacing=10,
                    width=400,
                    height=800,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    # Retorna o conteúdo completo da página
    return ft.Container(
        expand=True,
        bgcolor="#FFFFFF",
        content=ft.Row(
            [content],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        ),
        width=480,
        height=800,
    )
