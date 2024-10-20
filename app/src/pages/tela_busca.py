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
                host="db-nxt-reads.ctj2rmaeyrwc.us-east-1.rds.amazonaws.com",
                user="admin",
                password="Admin123",
                database="next_reads_database",
            )
            logger.info("Conexão estabelecida com sucesso!")
            return connection
        except mysql.connector.Error as err:
            logger.error(f"Erro ao conectar ao banco de dados: {err}")
            return None

    def get_books(self):
        """
        Recupera uma lista de livros do banco de dados.
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT bookID, title, authors, average_rating FROM Livros LIMIT 10"
            )
            books = cursor.fetchall()
            cursor.close()
            return books
        except mysql.connector.Error as err:
            logger.error(f"Erro ao recuperar livros: {err}")
            return []

    def get_book_details(self, book_id):
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


def tela_busca(page: ft.Page):
    page.title = "Livros"
    livro = Livro()

    def show_book_details(book_id):
        """Exibe os detalhes do livro em uma nova página."""
        book = livro.get_book_details(book_id)
        if book:
            details_page = ft.Column(
                [
                    ft.Text(f"Título: {book['title']}", size=20),
                    ft.Text(f"Autor(es): {book['authors']}", size=16),
                    ft.Text(f"Avaliação Média: {book['average_rating']}", size=14),
                    ft.Text(f"ISBN: {book['isbn']}", size=14),
                    ft.Text(f"ISBN-13: {book['isbn13']}", size=14),
                    ft.Text(f"Linguagem: {book['language_code']}", size=14),
                    ft.Text(f"Número de Páginas: {book['num_pages']}", size=14),
                    ft.Text(
                        f"Contagem de Avaliações: {book['ratings_count']}", size=14
                    ),
                    ft.Text(
                        f"Contagem de Resenhas: {book['text_reviews_count']}", size=14
                    ),
                    ft.Text(f"Data de Publicação: {book['publication_date']}", size=14),
                    ft.Text(f"Editora: {book['publisher']}", size=14),
                    ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: load_books()),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
            # Limpa a página atual e exibe a nova página com detalhes
            page.controls.clear()
            page.controls.append(details_page)
            page.update()
        else:
            logger.error("Livro não encontrado.")

    def load_books():
        """Carrega a lista de livros do banco de dados."""
        page.controls.clear()  # Limpa a página atual
        books = livro.get_books()
        for book in books:
            book_button = ft.ElevatedButton(
                text=book["title"],
                on_click=lambda e, id=book["bookID"]: show_book_details(id),
                bgcolor="#E7E5E2",
                width=350,
                opacity=0.6,
                color="#063E10",
            )
            page.controls.append(book_button)
        page.update()

    load_books()

    # Retornar o contêiner principal que encapsula a lista de livros
    return ft.Container(
        expand=True,
        bgcolor="#FFFFFF",
        content=ft.Column(  # Centraliza o conteúdo verticalmente
            page.controls,  # Adiciona os botões de livro
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        border_radius=ft.border_radius.all(20),  # Adiciona bordas arredondadas
        border=ft.BorderSide(2, color="#D6E0E2"),  # Adiciona uma borda
    )


if __name__ == "__main__":
    ft.app(target=tela_busca)
