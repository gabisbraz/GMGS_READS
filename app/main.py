import flet as ft
import os
import datetime
import sys
from pathlib import Path
from flet import Theme


# Define the directory root for image loading
DIR_ROOT = str(Path(__file__).parents[0])
if DIR_ROOT not in sys.path:
    sys.path.append(DIR_ROOT)

from src.pages.busca_livros_sugestao import busca_livros_sugestao
from src.classes.livros import Livro


def render_rating_stars(average_rating):

    if average_rating != None:
        # Converte a avaliação média para o número de estrelas
        full_stars = int(average_rating)  # Estrelas preenchidas
        half_star = (
            float(average_rating) - full_stars >= 0.5
        )  # Meia estrela se a média tiver uma fração >= 0.5
        empty_stars = (
            5 - full_stars - int(half_star)
        )  # Estrelas vazias para completar 5

        stars = []
        # Adiciona as estrelas cheias
        stars.extend([ft.Icon(ft.icons.STAR, color="gold") for _ in range(full_stars)])
        # Adiciona a meia estrela, se necessário
        if half_star:
            stars.append(ft.Icon(ft.icons.STAR_HALF, color="gold"))
        # Adiciona as estrelas vazias
        stars.extend(
            [ft.Icon(ft.icons.STAR_BORDER, color="gold") for _ in range(empty_stars)]
        )

        return stars
    else:
        stars = []
        stars.extend([ft.Icon(ft.icons.STAR_BORDER, color="gold") for _ in range(5)])
        return stars


def show_profile_page(page, user_id):
    # Dados do usuário para o perfil
    user_data = {
        "name": "Taylor Swift",
        "image_url": "perfil.jpeg",  # Substitua pelo caminho da imagem real
        "total_books": 5,
        "estantes": 4,
    }

    # Busca livros que o usuário está atualmente lendo
    table_connection = Livro()
    current_readings = table_connection.get_user_current_readings(user_id)

    book_rows = []
    for book in current_readings:  # Usa a lista de livros em progresso
        img_path = book.get("title", "1984").replace(" ", "_")
        img_path = Path(DIR_ROOT, f"assets/{img_path}_img.png")
        if not os.path.exists(img_path):
            img_path = Path(DIR_ROOT, f"assets/default.png")

        try:
            if book.get("comecou_leitura") != None:
                comeca_day = book.get("comecou_leitura").strftime("%d / %m / %Y")

            else:
                comeca_day = "-"
        except Exception:
            comeca_day = "-"
        try:
            if book.get("terminou_leitura") != None:
                termina_day = book.get("terminou_leitura").strftime("%d / %m / %Y")

            else:
                termina_day = "-"
        except Exception:
            termina_day = "-"

        try:
            if book.get("porcentagem") != None:
                porcent_num = book.get("porcentagem", 100) / 100
                porcent_str = f"{porcent_num} %"
            else:
                porcent_num = 0
                porcent_str = f"0 %"
        except Exception:
            porcent_str = f"0 %"
            porcent_num = 0

        # Aqui você pode construir cada linha para o livro
        book_row = ft.Row(
            controls=[
                ft.Image(
                    src=img_path,
                    width=100,
                    height=150,
                ),
                ft.Column(
                    [
                        ft.Text(
                            book["title"],
                            size=15,
                            weight="bold",
                            width=260,
                            text_align=ft.TextAlign.LEFT,
                        ),
                        ft.Text(
                            book["authors"],
                            size=13,
                            weight="bold",
                            width=260,
                            text_align=ft.TextAlign.LEFT,
                        ),
                        ft.Row(
                            controls=[
                                *render_rating_stars(book.get("nota")),
                                ft.Text(
                                    str(book.get("nota", 0)),
                                    size=12,
                                    weight="bold",
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row(
                            controls=[
                                ft.ProgressBar(
                                    value=porcent_num,
                                    width=100,
                                    height=10,
                                    border_radius=10,
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        porcent_str,
                                        size=12,
                                    ),
                                    alignment=ft.alignment.center_right,
                                ),
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(
                                    comeca_day,
                                    size=12,
                                ),
                                ft.Text(
                                    f" | ",
                                    size=12,
                                ),
                                ft.Text(
                                    termina_day,
                                    size=12,
                                ),
                            ]
                        ),
                    ]
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.VerticalAlignment.START,
        )
        # Adiciona o livro ao histórico de livros
        book_rows.append(book_row)

    # Layout do perfil
    profile_layout = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Image(
                        src=Path(
                            DIR_ROOT,
                            f"assets/perfil.jpeg",
                        ),
                        width=100,
                        height=100,
                        border_radius=70,
                        fit=ft.ImageFit.FIT_WIDTH,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("Bem-vindo(a),", size=16),
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
                    ft.Row(
                        [
                            ft.Text(
                                str(user_data["total_books"]), size=24, weight="bold"
                            ),
                            ft.Text("Livros"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
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
                    ft.Text("Seu histórico", size=20, weight="bold"),
                ]
                + book_rows,
                alignment=ft.MainAxisAlignment.START,
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        scroll=ft.ScrollMode.HIDDEN,
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
            img_path = book.get("title", "1984").replace(" ", "_")
            img_path = Path(DIR_ROOT, f"assets/{img_path}_img.png")
            if not os.path.exists(img_path):
                img_path = Path(DIR_ROOT, f"assets/default.png")
            books_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                controls=[
                                    ft.Image(
                                        src=img_path,
                                        width=100,
                                        height=150,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text(
                                                book["title"],
                                                size=15,
                                                weight="bold",
                                                width=260,
                                                text_align=ft.TextAlign.LEFT,
                                            ),
                                            ft.Text(
                                                book["authors"],
                                                size=13,
                                                weight="bold",
                                                width=260,
                                                text_align=ft.TextAlign.LEFT,
                                            ),
                                            ft.Text(
                                                book["description"],
                                                size=11,
                                                weight="bold",
                                                overflow=ft.TextOverflow.FADE,
                                                width=260,
                                                height=100,
                                                text_align=ft.TextAlign.JUSTIFY,
                                            ),
                                        ]
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.VerticalAlignment.START,
                            ),
                            ft.Divider(height=1, color="grey"),
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


def show_shelves_modal(book, user_id, page):
    """
    Cria e exibe um modal para adicionar um livro a uma estante com a opção de criar nova estante.
    """
    table_connection = Livro()
    shelves = table_connection.get_user_shelves(user_id)

    # Dropdown para selecionar a estante
    shelf_dropdown = ft.Dropdown(
        label="Selecione uma estante",
        options=[ft.dropdown.Option(shelf["nome"]) for shelf in shelves],
        width=300,
    )

    # Campo para nome da nova estante, inicialmente oculto
    new_shelf_name_input = ft.TextField(
        label="Nome da nova estante", width=180, visible=True, border_radius=20
    )

    # Função para criar uma nova estante e atualizar o Dropdown
    def on_create_shelf_click(e):
        if new_shelf_name_input != None:
            if new_shelf_name_input.visible:
                shelf_name = new_shelf_name_input.value
                if shelf_name:
                    try:
                        table_connection.create_shelf(user_id, shelf_name)
                        new_shelf = table_connection.get_user_shelves(user_id)[-1]
                        shelf_dropdown.options.append(
                            ft.dropdown.Option(new_shelf["nome"])
                        )
                        page.update()
                    except Exception as err:
                        page.open(f"Erro ao criar estante: {str(err)}")
            else:
                new_shelf_name_input.visible = True
            page.update()

    # Função para adicionar o livro à estante selecionada
    def add_to_shelf():
        estante_id = shelf_dropdown.value  # Obtém o ID da estante selecionada
        livro_id = book["bookID"]  # ID do livro a ser adicionado

        if not estante_id:
            page.open("Por favor, selecione uma estante antes de adicionar o livro.")
            return

        # Insere o livro na tabela 'EstanteLivros' com valores nulos para os campos adicionais
        try:
            estante_id = table_connection.get_shelf_id_by_name_and_user(estante_id, 1)
            table_connection.add_book_to_shelf(
                estante_id=estante_id,
                livro_id=livro_id,
                comecou_leitura=None,
                terminou_leitura=None,
                porcentagem=None,
                nota=None,
            )
            page.dialog.open = False  # Fecha o modal após a inserção
            page.update()
            print(f"Livro {livro_id} adicionado à estante {estante_id}.")
        except Exception as err:
            print(f"Erro ao adicionar livro à estante: {str(err)}")

    img_path = book.get("title", "1984").replace(" ", "_")
    img_path = Path(DIR_ROOT, f"assets/{img_path}_img.png")
    if not os.path.exists(img_path):
        img_path = Path(DIR_ROOT, f"assets/default.png")

    # Conteúdo do modal
    modal_content = ft.Column(
        controls=[
            ft.Container(
                content=ft.Image(
                    src=img_path,
                    width=130,
                    height=150,
                ),
                bgcolor="grey",
                padding=ft.Padding(left=80, right=80, top=30, bottom=30),
                border_radius=10,
            ),
            ft.Text(
                book["title"],
                size=17,
                weight="bold",
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Divider(height=1, color="grey"),
            shelf_dropdown,
            ft.Divider(height=1, color="grey"),
            ft.Row(
                controls=[
                    new_shelf_name_input,
                    ft.ElevatedButton(
                        "Criar Estante", on_click=on_create_shelf_click, width=100
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.ElevatedButton(
                "Atualizar",
                on_click=lambda e: add_to_shelf(),  # Chamando a função para adicionar à estante
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Criação do modal
    modal = ft.AlertDialog(
        title=ft.Text("Acompanhe suas leituras!"),
        content=modal_content,
        scrollable=ft.ScrollMode.HIDDEN,
    )

    page.overlay.append(modal)
    modal.open = True
    page.update()


def discover_livros(page):

    table_connection = Livro()

    grid_view = ft.GridView(
        spacing=10,
        runs_count=3,
        max_extent=150,
        expand=True,
    )

    livros = table_connection.search_random_books()

    # Add book items to the GridView
    for livro in livros:
        img_path = livro.get("title", "1984").replace(" ", "_")
        img_path = Path(DIR_ROOT, f"assets/{img_path}_img.png")
        if not os.path.exists(img_path):
            img_path = Path(DIR_ROOT, f"assets/default.png")
        grid_view.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Image(
                            src=img_path,
                            width=100,
                            height=100,
                            expand=True,
                        ),
                        ft.Text(
                            livro["title"],
                            size=12,
                            weight="bold",
                            overflow=False,
                            max_lines=1,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                on_click=lambda e, book_id=livro["bookID"]: page.go(f"/book/{book_id}"),
            )
        )

    return grid_view


def avaliar_livro(page, livro, usuario_id):
    """
    Exibe um modal para o usuário avaliar o livro.
    """
    table_connection = Livro()

    livro_info = table_connection.get_book_info(livro["title"])

    if livro_info == None:
        livro_info = {
            "comecou_leitura": datetime.date.today(),
            "terminou_leitura": datetime.date.today(),
            "nota": 0,
            "porcentagem": 0,
        }
    started_date = livro_info.get("comecou_leitura", datetime.date.today())
    finished_date = livro_info.get("terminou_leitura", datetime.date.today())
    nota_input = ft.TextField(
        label="Avaliação (de 1 a 5)",
        keyboard_type="number",
        width=300,
        border_radius=20,
        value=livro_info.get("nota", 0),
        icon=ft.Icon(ft.icons.SCORE_ROUNDED, color="gold"),
    )
    porcent_input = ft.TextField(
        label="Porcentagem de leitura",
        keyboard_type="number",
        width=300,
        border_radius=20,
        value=livro_info.get("porcentagem", 0),
        icon=ft.Icon(ft.icons.SCORE_ROUNDED, color="gold"),
    )

    # Função para atualizar as datas
    def on_date_picker_change(e, field_name):
        nonlocal started_date, finished_date
        if field_name == "start":
            started_date = e.control.value
        elif field_name == "end":
            finished_date = e.control.value

    # Botões de Data
    start_date_picker = ft.ElevatedButton(
        "Iniciou em:",
        icon=ft.icons.CALENDAR_MONTH,
        width=140,
        on_click=lambda e: page.open(
            ft.DatePicker(
                tooltip="Início da Leitura",
                field_label_text="Início da Leitura",
                visible=True,
                value=started_date,
                on_change=lambda e: on_date_picker_change(
                    e, "start"
                ),  # Atualiza a data de início
            ),
        ),
    )
    end_date_picker = ft.ElevatedButton(
        "Terminou em:",
        icon=ft.icons.CALENDAR_MONTH,
        width=140,
        on_click=lambda e: page.open(
            ft.DatePicker(
                tooltip="Término da Leitura",
                field_label_text="Término da Leitura",
                visible=True,
                value=finished_date,
                on_change=lambda e: on_date_picker_change(
                    e, "end"
                ),  # Atualiza a data de término
            ),
        ),
    )

    def on_avaliar_click(e):
        try:
            # Obtém a nota inserida pelo usuário
            nota = float(nota_input.value)

            # Verifica se a nota é válida
            if nota < 1 or nota > 5:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("A avaliação deve ser entre 1 e 5!"), bgcolor="red"
                )
                page.snack_bar.open = True
                page.update()
                return

            list_id = table_connection.get_shelves_by_book_name(livro["title"])

            for id_estante in list_id:
                # Salva a avaliação no banco de dados
                table_connection.update_book_shelf(
                    livro["bookID"],
                    id_estante,
                    nota,
                    porcentagem=int(porcent_input.value),
                    comecou_leitura=started_date,
                    terminou_leitura=finished_date,
                )

            if len(list_id) == 0:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Você precisa adicionar o livro a uma estante!"),
                    bgcolor="red",
                )
                page.snack_bar.open = True
                # Fecha o modal
                page.update()
            else:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Avaliação salva com sucesso!"), bgcolor="green"
                )
                page.snack_bar.open = True
                # Fecha o modal
                page.update()

            print("Avaliação salva com sucesso!")

        except ValueError:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Por favor, insira uma nota válida!"), bgcolor="red"
            )
            page.snack_bar.open = True
            # Caso o usuário insira um valor inválido
            print("Por favor, insira uma nota válida!")

    img_path = livro.get("title", "1984").replace(" ", "_")
    img_path = Path(DIR_ROOT, f"assets/{img_path}_img.png")
    if not os.path.exists(img_path):
        img_path = Path(DIR_ROOT, f"assets/default.png")

    # Conteúdo do modal
    modal_content = ft.Column(
        controls=[
            ft.Container(
                content=ft.Image(
                    src=img_path,
                    width=230,
                    height=300,
                ),
                bgcolor="grey",
                padding=ft.Padding(left=80, right=80, top=10, bottom=10),
                border_radius=20,
            ),
            ft.Text(livro.get("title", "-"), size=17, weight="bold"),
            ft.Text("", size=17, weight="bold"),
            nota_input,
            porcent_input,
            ft.Row(
                controls=[
                    start_date_picker,
                    end_date_picker,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.ElevatedButton(
                "Avaliar",
                on_click=on_avaliar_click,
                width=200,
                bgcolor="gold",
            ),
            ft.Text("\n", size=17, weight="bold"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Criação do modal
    modal = ft.AlertDialog(
        title=ft.Text("Avaliação do Livro", weight="bold"),
        content=modal_content,
        scrollable=ft.ScrollMode.HIDDEN,
    )

    page.overlay.append(modal)
    modal.open = True
    page.update()


def book_details(bookID, page):
    page.title = "NXT Reads"
    page.window.width = 480
    page.window.height = 800
    page.window.resizable = False
    page.theme = Theme(color_scheme_seed="green")
    page.theme_mode = "light"

    table_connection = Livro()
    livro = table_connection.get_book_by_id(bookID)

    usuario_id = 1
    img_path = livro.get("title", "1984").replace(" ", "_")
    img_path = Path(DIR_ROOT, f"assets/{img_path}_img.png")
    if not os.path.exists(img_path):
        img_path = Path(DIR_ROOT, f"assets/default.png")
    genero = livro.get("genres", "-")
    pag = livro.get("num_pages", "-")
    return ft.Container(
        ft.Column(
            controls=[
                ft.Container(
                    content=ft.Image(
                        src=img_path,
                        width=230,
                        height=300,
                    ),
                    bgcolor="grey",
                    padding=ft.Padding(left=80, right=80, top=10, bottom=10),
                    border_radius=20,
                ),
                ft.Text(livro.get("title", "-"), size=24, weight="bold"),
                ft.Divider(height=1, color="grey"),
                ft.Row(
                    controls=[
                        *render_rating_stars(livro.get("average_rating", 0)),
                        ft.Text(
                            str(livro.get("average_rating", "-")),
                            size=12,
                            weight="bold",
                        ),
                        ft.Text(
                            f"{livro.get('ratings_count', '-')} avaliações",
                            size=12,
                            weight="bold",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[
                        ft.Text(
                            f"Gênero: {genero}",
                            size=12,
                            weight="bold",
                        ),
                        ft.Text(
                            f" | ",
                            size=17,
                            weight="bold",
                        ),
                        ft.Text(
                            f"{pag} páginas",
                            size=12,
                            weight="bold",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Divider(height=1, color="grey"),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Adicionar a estante",
                            on_click=lambda e: show_shelves_modal(
                                livro, usuario_id, page
                            ),  # Chama o modal  # Link para pesquisa
                            icon=ft.icons.BOOKMARK_ADDED_ROUNDED,
                            width=150,
                        ),
                        ft.ElevatedButton(
                            "Avaliar",
                            on_click=lambda e: avaliar_livro(page, livro, usuario_id),
                            icon=ft.icons.RATE_REVIEW_ROUNDED,
                            width=150,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text(
                    livro.get("description", "-"),
                    size=12,
                    text_align=ft.TextAlign.JUSTIFY,
                ),
                ft.Text(
                    "Veja mais!",
                    size=17,
                    text_align=ft.TextAlign.JUSTIFY,
                    weight="bold",
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Pesquisar",
                            url=livro.get("search", "-"),
                            icon=ft.icons.SEARCH,
                        ),
                        ft.ElevatedButton(
                            "Google Books",
                            url=livro.get("google_book", "-"),
                            icon=ft.icons.BOOK,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text(f"\n", size=17, weight="bold"),
            ],
            alignment=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.HIDDEN,
        ),
        margin=ft.Margin(left=25, right=25, top=0, bottom=0),
        width=470,
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
        selected_index=1,
    )

    # Container to hold the page content
    container_pagina = ft.Container(expand=True)

    # Route change function
    def route_change(e):
        container_pagina.clean()  # Clear previous controls
        user_id = 1
        if page.route == "/profile":
            container_pagina.content = show_profile_page(page, user_id)
        elif page.route == "/explore":
            container_pagina.content = discover_livros(page)
        elif page.route.startswith("/book/"):
            book_id = int(page.route.split("/")[-1])  # Extract book ID from route
            container_pagina.content = book_details(book_id, page)
        elif page.route == "/shelves":
            container_pagina.content = show_shelves_page(page, user_id)
        elif page.route.startswith("/busca_livro"):
            container_pagina.content = busca_livros_sugestao(page)

        page.update()  # Refresh the page with new content

    # Assign the route change handler
    page.on_route_change = route_change

    # Start the app on the home route
    page.add(container_pagina)  # Add the container to the page
    page.go(route="/explore")  # Initial route


ft.app(target=main)
