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

    def search_book_by_title(self, title):
        """
        Recupera um livro específico baseado no título (busca exata).
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM Livros WHERE title = %s LIMIT 1"
            cursor.execute(query, (title,))
            book = cursor.fetchone()
            cursor.close()
            return book
        except mysql.connector.Error as err:
            logger.error(f"Erro ao buscar livro pelo título: {err}")
            return None

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


def buscar_livro_e_mostrar(page, livro_instance, input_pesquisa, resultado):
    """
    Função para buscar um livro pelo título e mostrar os detalhes na interface.
    """
    titulo_pesquisado = input_pesquisa.value
    if not titulo_pesquisado:
        page.snack_bar = ft.SnackBar(
            ft.Text("Por favor, insira um título para a busca.")
        )
        page.snack_bar.open = True
        page.update()
        return

    # Busca o livro pelo título exato
    livro_encontrado = livro_instance.search_book_by_title(titulo_pesquisado)

    if livro_encontrado:
        # Limpa o conteúdo anterior do `resultado`
        resultado.controls.clear()

        # Adiciona as informações detalhadas do livro na interface
        resultado.controls.append(ft.Text(f"ID: {livro_encontrado['bookID']}", size=20))
        resultado.controls.append(
            ft.Text(f"Título: {livro_encontrado['title']}", size=20)
        )
        resultado.controls.append(
            ft.Text(f"Autor: {livro_encontrado['authors']}", size=20)
        )
        resultado.controls.append(
            ft.Text(f"Avaliação: {livro_encontrado['average_rating']}", size=20)
        )
        resultado.controls.append(
            ft.Text(
                f"Data de Publicação: {livro_encontrado['publication_date']}", size=20
            )
        )  # Supondo que exista um campo para a data
        resultado.controls.append(
            ft.Text(f"Número de Páginas: {livro_encontrado['num_pages']}", size=20)
        )  # Supondo que haja um campo de número de páginas

    else:
        # Caso o livro não seja encontrado, exibe uma mensagem de aviso
        resultado.controls.clear()
        page.snack_bar = ft.SnackBar(
            ft.Text("Livro não encontrado no banco de dados."), bgcolor="red"
        )
        page.snack_bar.open = True

    # Atualiza a página para refletir as mudanças
    page.update()


def tela_busca(page: ft.Page):
    """
    Função que constrói e retorna o conteúdo da página de busca de livros.
    """
    page.title = "Tela de Busca de Livros"
    page.window_width = 480
    page.window_height = 800
    page.bgcolor = "#FFFFFF"  # Define a cor de fundo da página

    # Instancia o objeto Livro
    livro_instance = Livro()

    # Campo de pesquisa
    input_pesquisa = ft.TextField(
        label="Título do livro",
        width=300,
        color="#000000",
        label_style=ft.TextStyle(color="#03103F"),
        border=ft.InputBorder.UNDERLINE,
    )

    # Defina uma variável `resultado` para exibir as informações do livro
    resultado = ft.Column([])  # Inicialmente vazia, será preenchida após a busca

    # Botão de pesquisa
    botao_pesquisa = ft.ElevatedButton(
        text="Buscar",
        on_click=lambda e: buscar_livro_e_mostrar(
            page, livro_instance, input_pesquisa, resultado
        ),
        color="black",
        bgcolor="#D6E0E2",
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(font_family="Sen Extra Bold", weight="bold")
        ),
    )

    # Botão para voltar à página inicial (opcional)
    botao_voltar = ft.ElevatedButton(
        text="Voltar para a Página Inicial",
        on_click=lambda _: page.go("/"),  # Supondo que "/" seja a rota inicial
        color="black",
        bgcolor="#D6E0E2",
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(font_family="Sen Extra Bold", weight="bold")
        ),
    )

    # Main container that will hold all elements for the search
    content = ft.Container(
        bgcolor="#FFFFFF",  # White background for the container
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        "Buscar Livro", size=50, weight="bold", color="#03103F"
                    ),
                    margin=ft.margin.only(top=50),
                ),
                input_pesquisa,
                botao_pesquisa,
                botao_voltar,
                resultado,  # Adiciona o campo `resultado` à interface
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,  # Space between the elements
        ),
    )

    # Ensuring that the content stretches to fill the entire width and height of the screen
    return ft.Container(
        expand=True,  # This will make the container cover the entire screen width and height
        bgcolor="#FFFFFF",  # White background to fill the screen
        content=ft.Row(
            [content],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,  # Ensure it stretches across the screen
        ),
        border_radius=ft.border_radius.all(
            20
        ),  # Adiciona bordas arredondadas ao contêiner principal
        border=ft.BorderSide(2, color="#D6E0E2"),
    )
