import mysql.connector
from loguru import logger
import flet as ft


class Livro:
    """
    Classe para gerenciar a base de dados de livros e realizar consultas.
    """

    def __init__(self):
        """
        Inicializa a classe 'Livro' e estabelece conexão com o banco de dados.
        """
        self.connection = self.create_connection()

    def create_connection(self):
        """
        Cria a conexão com o banco de dados MySQL.
        """
        try:
            connection = mysql.connector.connect(
                host="database-1.ctj2rmaeyrwc.us-east-1.rds.amazonaws.com",
                user="admin",
                password="admin123",
                database="nxt_reads_db",
            )
            logger.info("Conexão estabelecida com sucesso!")
            return connection
        except mysql.connector.Error as err:
            logger.error(f"Erro ao conectar ao banco de dados: {err}")
            return None

    def get_book(self):
        """
        Recupera os detalhes de um livro específico.
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT bookID, title, authors, average_rating FROM Livros LIMIT 10"
            )
            book = cursor.fetchall()
            cursor.close()
            return book
        except mysql.connector.Error as err:
            logger.error(f"Erro ao recuperar detalhes do livro: {err}")
            return None


def discover_livros(page: ft.Page):
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

    livro_instance = Livro()

    livros = livro_instance.get_book()

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
