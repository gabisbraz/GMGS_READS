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

    def get_book(self, book_id):
        """
        Recupera os detalhes de um livro específico.
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Livros WHERE bookID = %s", (book_id,))
            book = cursor.fetchone()
            cursor.close()
            return book
        except mysql.connector.Error as err:
            logger.error(f"Erro ao recuperar detalhes do livro: {err}")
            return None


def detalhes_livro(page: ft.Page, book_id):
    """
    Página que exibe os detalhes de um livro específico baseado no book_id.
    """
    page.title = "Detalhes do Livro"
    page.bgcolor = "#FFFFFF"
    page.window_width = 480
    page.window_height = 800
    page.window_resizable = False
    page.window_always_on_top = True

    livro_instance = Livro()

    livro = livro_instance.get_book(book_id)

    # Exibir detalhes do livro ou uma mensagem de erro caso não seja encontrado
    if livro:
        detalhes = ft.Column(
            [
                ft.Text(f"Título: {livro['title']}", weight="bold"),
                ft.Text(f"Autor(es): {livro['authors']}"),
                ft.Text(f"Avaliação: {livro['average_rating']}"),
                ft.Text(f"Data de Publicação: {livro['publication_date']}"),
                ft.Text(f"Número de Páginas: {livro['num_pages']}"),
                # Adicione mais informações, se necessário
            ],
            spacing=10,
        )
    else:
        detalhes = ft.Text("Livro não encontrado.", size=20, color="red")

    # Botão para voltar à página de login_sucesso
    botao_voltar_login_sucesso = ft.ElevatedButton(
        text="Voltar ao Login",
        on_click=lambda _: page.go("/login_sucesso"),
        bgcolor="#D6E0E2",
        color="black",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            text_style=ft.TextStyle(size=18, font_family="Sen Medium", weight="bold"),
        ),
    )

    # Botão para voltar à lista de livros
    botao_voltar_lista = ft.ElevatedButton(
        text="Voltar",
        on_click=lambda _: page.go("/discover"),
        bgcolor="#D6E0E2",
        color="black",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            text_style=ft.TextStyle(size=18, font_family="Sen Medium", weight="bold"),
        ),
    )

    content = ft.Container(
        bgcolor="#FFFFFF",
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text("Detalhes do Livro", weight="bold", color="black"),
                    margin=ft.margin.only(top=50, bottom=20),
                    padding=ft.padding.only(left=50, right=50),
                ),
                detalhes,
                botao_voltar_login_sucesso,  # Botão para voltar ao login_sucesso
                botao_voltar_lista,  # Botão para voltar à lista de livros
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
