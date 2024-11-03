import flet as ft
from flet import Theme
import sys
from pathlib import Path
from loguru import logger
import datetime
from flet import TextField, ElevatedButton, DatePicker, Slider


# Define the directory root for image loading
DIR_ROOT = str(Path(__file__).parents[0])
if DIR_ROOT not in sys.path:
    sys.path.append(DIR_ROOT)

from src.pages.busca_livros_sugestao import busca_livros_sugestao
from src.classes.livros import Livro


def get_cover_url(isbn):
    return f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"


def show_profile_page(page, user_id):
    # Dados do usuário para o perfil
    user_data = {
        "name": "Taylor Swift",
        "image_url": "perfil.jpeg",  # Substitua pelo caminho da imagem real
        "total_books": 129,
        "total_authors": 100,
        "estantes": 3,
    }

    # Busca livros que o usuário está atualmente lendo
    table_connection = Livro()
    current_readings = table_connection.get_user_current_readings(user_id)

    # Layout do perfil
    profile_layout = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Image(
                        src=user_data["image_url"],
                        width=100,
                        height=100,
                        border_radius=70,
                        fit=ft.ImageFit.FIT_WIDTH,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("Welcome back,", size=16),
                            ft.Text(user_data["name"], size=24, weight="bold"),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=20,
            ),
            ft.Divider(height=10, color="black"),
            ft.Row(
                controls=[
                    ft.Column(
                        [
                            ft.Text(
                                str(user_data["total_books"]), size=24, weight="bold"
                            ),
                            ft.Text("Livros"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                str(user_data["total_authors"]), size=24, weight="bold"
                            ),
                            ft.Text("Autores"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        [
                            ft.Text(str(user_data["estantes"]), size=24, weight="bold"),
                            ft.Text("Estantes"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            ),
            ft.Divider(height=10, color="black"),
            ft.Column(
                controls=[
                    ft.Text("Continue Reading", size=20, weight="bold"),
                ]
                + [
                    ft.Row(
                        controls=[
                            ft.Image(
                                src=get_cover_url(book["isbn"]), width=50, height=70
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(book["title"], size=18, weight="bold"),
                                    ft.Text(book["authors"], size=16),
                                    ft.Container(
                                        content=ft.Text(
                                            f"{book['porcentagem']}%", size=16
                                        ),
                                        alignment=ft.alignment.center_right,
                                    ),
                                    ft.ProgressBar(
                                        value=book["porcentagem"] / 100,
                                        width=100,
                                        height=6,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                    for book in current_readings  # Usa a lista de livros em progresso
                ]
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    return profile_layout


def show_shelves_page(page, user_id):
    """
    Exibe todas as estantes do usuário como abas.
    """
    table_connection = Livro()
    shelves = table_connection.get_user_shelves(user_id)

    # Layout das estantes como abas
    shelves_tabs = ft.Tabs()

    # Função para carregar os livros da estante selecionada
    def load_books(estante_id):
        books = table_connection.get_books_in_shelf(estante_id)
        books_list = ft.Column(
            controls=[
                ft.Text(f"Livros na Estante", size=24, weight="bold"),
            ],
            alignment=ft.MainAxisAlignment.START,
        )

        for book in books:
            books_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Image(
                                src=get_cover_url(book["isbn"]), width=100, height=150
                            ),
                            ft.Text(book["title"], size=18, weight="bold"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    on_click=lambda e, book_id=book["bookID"]: page.go(
                        f"/book/{book_id}"
                    ),
                )
            )

        return books_list

    # Adiciona cada estante como uma aba
    for i, shelf in enumerate(shelves):
        shelves_tabs.tabs.append(
            ft.Tab(
                text=shelf["nome"],
            )
        )

    # Container para o conteúdo inicial da aba
    books_column = ft.Column()

    # Atualiza o conteúdo inicial com a primeira estante
    if shelves:
        books_column = load_books(shelves[0]["estante_id"])

    # Atualiza o conteúdo quando uma aba é selecionada
    def on_tab_change(e):
        selected_tab_index = shelves_tabs.selected_index
        if selected_tab_index >= 0:
            selected_shelf_id = shelves[selected_tab_index]["estante_id"]
            books_column.controls = load_books(selected_shelf_id).controls

        page.update()  # Atualiza a página

    # Conectar a mudança de aba ao evento
    shelves_tabs.on_change = on_tab_change

    return ft.Column(
        controls=[
            ft.Text("Minhas Estantes", size=24, weight="bold"),
            shelves_tabs,
            books_column,  # Adiciona a coluna de livros
        ],
        alignment=ft.MainAxisAlignment.START,
    )


def show_shelf_books(page, estante_id):
    """
    Exibe todos os livros de uma estante específica.
    """
    table_connection = Livro()
    books = table_connection.get_books_in_shelf(estante_id)

    # Lista os livros da estante
    books_list = ft.Column(
        controls=[
            ft.Text(f"Livros na Estante", size=24, weight="bold"),
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    for book in books:
        books_list.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Image(
                            src=get_cover_url(book["isbn"]), width=100, height=150
                        ),  # Coloque a imagem do livro aqui
                        ft.Text(book["title"], size=18, weight="bold"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                on_click=lambda e, book_id=book["bookID"]: page.go(f"/book/{book_id}"),
            )
        )

    return books_list


def show_create_shelf_modal(page, user_id):
    """
    Cria e exibe um modal para que o usuário crie uma nova estante.
    """
    # Contêiner do modal
    shelf_name_input = ft.TextField(label="Nome da Estante", autofocus=True)

    # Função para adicionar a nova estante
    def add_shelf(e):
        shelf_name = shelf_name_input.value
        if shelf_name:
            table_connection = Livro()
            table_connection.create_shelf(user_id, shelf_name)
            page.update()  # Atualiza a página para refletir a nova estante

    def fecha_dialog():
        page.dialog.open = False
        page.update()

    # Conteúdo do modal
    modal_content = ft.Column(
        controls=[
            shelf_name_input,
            ft.ElevatedButton("Criar Estante", on_click=add_shelf),
            ft.ElevatedButton("Fechar", on_click=lambda e: fecha_dialog()),
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    # Criação do modal
    modal = ft.AlertDialog(
        title=ft.Text("Criar Nova Estante"),
        content=modal_content,
    )

    page.dialog = modal
    modal.open = True
    page.update()


def show_shelves_modal(book, user_id, page):
    """
    Cria e exibe um modal mostrando a imagem do livro e todas as estantes do usuário,
    com campos adicionais para inserir progresso, data de início, data de término e nota.
    """
    table_connection = Livro()
    shelves = table_connection.get_user_shelves(user_id)

    # Inputs para os dados adicionais
    progress_input = Slider(value=0, min=0, max=100, label="Porcentagem de Leitura (%)")
    start_date_picker = DatePicker(
        tooltip="Data de Início da Leitura", value=datetime.date.today()
    )
    end_date_picker = DatePicker(tooltip="Data de Término da Leitura")
    rating_input = TextField(label="Nota (0-10)", keyboard_type="number", max_length=2)

    # Função para adicionar o livro na estante selecionada com dados adicionais
    def add_to_shelf(estante_id):
        porcentagem = progress_input.value
        comecou_leitura = start_date_picker.value
        terminou_leitura = end_date_picker.value
        nota = rating_input.value

        # Insere o livro na estante com as informações fornecidas
        table_connection.add_book_to_shelf(
            estante_id,
            book["bookID"],
            porcentagem=porcentagem,
            comecou_leitura=comecou_leitura,
            terminou_leitura=terminou_leitura,
            nota=nota,
        )
        page.dialog.open = False
        page.update()
        logger.info(
            f"Livro {book['bookID']} adicionado à estante {estante_id} com progresso {porcentagem}% e nota {nota}"
        )

    # Conteúdo do modal
    modal_content = ft.Column(
        controls=[
            ft.Text(f"Estantes para o livro: {book['title']}", size=20, weight="bold"),
            ft.Image(
                src="image.jpg", width=100, height=150
            ),  # Coloque a imagem do livro aqui
            ft.Text("Escolha uma estante:", size=18),
            progress_input,
            start_date_picker,
            end_date_picker,
            rating_input,
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    # Adiciona as estantes ao modal com a função de on_click para cada botão
    for shelf in shelves:
        modal_content.controls.append(
            ElevatedButton(
                shelf["nome"],
                on_click=lambda e, estante_id=shelf["estante_id"]: add_to_shelf(
                    estante_id
                ),
            )
        )

    def fecha_dialog():
        page.dialog.open = False
        page.update()

    # Criação do modal
    modal = ft.AlertDialog(
        title=ft.Text("Selecione uma Estante e Insira Detalhes"),
        content=modal_content,
        actions=[ElevatedButton("Fechar", on_click=lambda e: fecha_dialog())],
    )

    page.overlay.append(modal)
    modal.open = True
    page.update()


def discover_livros(page):

    table_connection = Livro()

    grid_view = ft.GridView(spacing=10, runs_count=3, max_extent=150, expand=True)

    livros = table_connection.search_random_books()

    # Add book items to the GridView
    for livro in livros:
        grid_view.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Image(
                            src=get_cover_url(livro["isbn"]),
                            width=100,
                            height=100,
                            expand=True,
                        ),
                        ft.Text(
                            livro["title"],
                            size=18,
                            weight="bold",
                            overflow=False,
                            max_lines=1,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                on_click=lambda e, livro=livro: page.go(f"/book/{livro["bookID"]}"),
            )
        )

    return grid_view


def book_details(bookID, page):
    page.title = "NXT Reads"
    page.window.width = 480
    page.window.height = 800
    page.window.resizable = False
    page.theme = Theme(color_scheme_seed="green")
    page.theme_mode = "light"

    table_connection = Livro()
    livro = table_connection.get_book_by_id(bookID)

    # Exemplo de usuario_id (isto deve ser obtido de alguma forma na sua aplicação)
    usuario_id = 1  # Substitua pelo ID real do usuário

    return ft.Column(
        controls=[
            ft.Image(
                src=get_cover_url(livro["isbn"]), width=200, height=300
            ),  # Imagem da capa do livro
            ft.Text(livro.get("title", "-"), size=24, weight="bold"),  # Título do livro
            ft.ElevatedButton(
                "Estante",
                on_click=lambda e: show_shelves_modal(
                    livro, usuario_id, page
                ),  # Chama o modal
            ),
            ft.ElevatedButton(
                "Criar Nova Estante",
                on_click=lambda e: show_create_shelf_modal(
                    page, usuario_id
                ),  # Chama o modal de criação de estante
            ),
            ft.Text(livro.get("authors", "-"), size=20),  # Autor do livro
            ft.Text(livro.get("average_rating", "-"), size=16),  # Avaliação média
            ft.Text(livro.get("ratings_count", "-"), size=16),  # Contagem de avaliações
            ft.Text(livro.get("num_pages", "-"), size=16),  # Número de páginas
        ],
        alignment=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        width=480,
    )


def main(page: ft.Page):
    page.title = "NXT Reads"
    page.window.width = 480
    page.window.height = 800
    page.window.resizable = False
    page.theme = Theme(color_scheme_seed="green")
    page.theme_mode = "light"

    # AppBar setup
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.BOOK_ROUNDED, color="green"),
        leading_width=40,
        title=ft.Text("NXT Reads"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
    )

    # Navigation Bar setup
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.SEARCH, label="Pesquisar"),
            ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Explorar"),
            ft.NavigationBarDestination(icon=ft.icons.BOOK, label="Estantes"),
            ft.NavigationBarDestination(icon=ft.icons.PERSON, label="Perfil"),
        ],
        on_change=lambda e: page.go(
            route=(
                "/explore"
                if e.data == "1"
                else (
                    "/busca_livro"
                    if e.data == "0"
                    else (
                        "/shelves"
                        if e.data == "2"
                        else ("/profile" if e.data == "3" else "/")
                    )
                )
            )
        ),
        height=70,
    )

    # Home content
    home_content = ft.Column(
        controls=[
            ft.Text("Eterno GMG!", size=20, weight="bold"),
        ],
        alignment="center",
        spacing=10,
    )

    # Container to hold the page content
    container_pagina = ft.Container(expand=True)

    # Route change function
    def route_change(e):
        container_pagina.clean()  # Clear previous controls
        user_id = 1
        if page.route == "/":
            container_pagina.content = home_content
        elif page.route == "/profile":
            container_pagina.content = show_profile_page(page, user_id)
        elif page.route == "/explore":
            container_pagina.content = discover_livros(page)
        elif page.route.startswith("/book/"):
            book_id = int(page.route.split("/")[-1])  # Extract book ID from route
            container_pagina.content = book_details(book_id, page)
        elif page.route == "/shelves":
            container_pagina.content = show_shelves_page(page, user_id)
        elif page.route.startswith("/shelf/"):
            estante_id = int(page.route.split("/")[-1])  # Extract shelf ID from route
            container_pagina.content = show_shelf_books(page, estante_id)
        elif page.route.startswith("/busca_livro"):
            container_pagina.content = busca_livros_sugestao(page)

        page.update()  # Refresh the page with new content

    # Assign the route change handler
    page.on_route_change = route_change

    # Start the app on the home route
    page.add(container_pagina)  # Add the container to the page
    page.go(route="/")  # Initial route


ft.app(target=main)
