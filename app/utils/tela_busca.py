import flet as ft
from app import Livro, buscar_livro_e_mostrar  # Importação relativa

def tela_busca(page: ft.Page):
    """
    Função que constrói e retorna o conteúdo da página de busca de livros, com um estilo semelhante à tela de login.
    """
    page.title = "Tela de Busca de Livros"
    page.window_width = 480
    page.window_height = 800
    page.bgcolor = "#FFFFFF"  # Define a cor de fundo da página

    # Instancia o objeto Livro
    livro_instance = Livro("app/data/books.csv")

    # Campo de pesquisa
    input_pesquisa = ft.TextField(
        label="Título do livro", 
        width=300, 
        border=ft.InputBorder.UNDERLINE
    )

    # Defina uma variável `resultado` para exibir as informações do livro
    resultado = ft.Column([])  # Inicialmente vazia, será preenchida após a busca

    # Botão de pesquisa
    botao_pesquisa = ft.ElevatedButton(
        text="Buscar", 
        on_click=lambda e: buscar_livro_e_mostrar(page, livro_instance, input_pesquisa, resultado),
        color="black",  
        bgcolor="#D6E0E2",  
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(font_family="Sen Extra Bold", weight="bold")
        )
    )

    # Botão para voltar à página inicial (opcional)
    botao_voltar = ft.ElevatedButton(
        text="Voltar para a Página Inicial",
        on_click=lambda _: page.go("/"),  # Supondo que "/" seja a rota inicial
        color="black",  
        bgcolor="#D6E0E2",  
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(font_family="Sen Extra Bold", weight="bold")
        )
    )

    # Main container that will hold all elements for the search
    content = ft.Container(
        bgcolor="#FFFFFF",  # White background for the container
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text("Buscar Livro", size=50, weight="bold", color="#03103F"),
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
        )
    )

    # Ensuring that the content stretches to fill the entire width and height of the screen
    return ft.Container(
        expand=True,  # This will make the container cover the entire screen width and height
        bgcolor="#FFFFFF",  # White background to fill the screen
        content=ft.Row(
            [content],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True  # Ensure it stretches across the screen
        )
    )
