import flet as ft
from usuario import buscar_usuario, Usuario  # Importando do arquivo 'usuario.py'

import mysql.connector


# Estabelecer uma conexão com o banco de dados
def create_connection():
    connection = mysql.connector.connect(
        host="db-nxt-reads.ctj2rmaeyrwc.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Admin123",
        database="next_reads_database",
    )
    return connection


def tela_login(page: ft.Page):
    page.title = "Tela de Login"
    page.window_width = 480
    page.window_height = 800
    page.bgcolor = "#FFFFFF"  # Define a cor de fundo da página

    page.fonts = {
        "Sen Extra Bold": "app/fonts/Sen-ExtraBold.ttf",
        "Sen Medium": "app/fonts/Sen-Medium.ttf",
    }

    def realizar_login(e):
        username = username_input.value
        password = password_input.value

        # Busca o usuário no banco de dados
        usuario_encontrado = buscar_usuario(create_connection(), username)

        if usuario_encontrado:
            # Verifica se a senha está correta
            if Usuario.verificar_senha(password, usuario_encontrado["password"]):
                # Redireciona para a tela de sucesso
                page.go("/login_sucesso")
            else:
                resultado.value = "Senha incorreta. Tente novamente."
                resultado.color = "#dc3545"  # Vermelho para erro
        else:
            resultado.value = "Usuário não encontrado."
            resultado.color = "#dc3545"  # Vermelho para erro

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

    # Main container that will hold all login elements
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
                        src="app/assets/Kids reading.gif", width=300, height=300
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

    # Garante que o conteúdo preencha toda a largura e altura da tela
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


def tela_login_sucesso(page: ft.Page):
    page.title = "Login Bem-Sucedido"
    page.window_width = 480
    page.window_height = 800
    page.bgcolor = "#FFFFFF"

    content = ft.Container(
        bgcolor="#FFFFFF",
        border_radius=ft.border_radius.all(20),  # Aplica a borda arredondada
        padding=20,  # Adiciona preenchimento interno para que o conteúdo não encoste na borda
        border=ft.BorderSide(
            1, color="#D6E0E2"
        ),  # Adiciona uma borda visível para destacar o arredondamento
        content=ft.Column(
            [
                ft.Text(
                    "Login realizado com sucesso!",
                    size=25,
                    weight="bold",
                    color="black",
                    font_family="Sen Extra Bold",
                ),
                ft.Image(
                    src="app/assets/Celebration.gif", width=300, height=300
                ),  # Exemplo de GIF ou imagem de sucesso
                ft.ElevatedButton(
                    text="Buscar por livros",
                    on_click=lambda _: page.go("/busca_livros"),
                    color="black",
                    bgcolor="#D6E0E2",
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(
                            font_family="Sen Extra Bold", weight="bold"
                        )
                    ),
                ),
                ft.ElevatedButton(
                    text="Voltar à página inicial",
                    on_click=lambda _: page.go("/"),
                    color="black",
                    bgcolor="#D6E0E2",
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(
                            font_family="Sen Extra Bold", weight="bold"
                        )
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
    )

    return ft.Container(
        expand=True,
        bgcolor="#FFFFFF",
        content=ft.Row(  # Centraliza o conteúdo horizontalmente e verticalmente
            [content],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,  # Expande para preencher a tela inteira
        ),
        border_radius=ft.border_radius.all(
            20
        ),  # Adiciona bordas arredondadas ao contêiner principal
        border=ft.BorderSide(
            2, color="#D6E0E2"
        ),  # Adiciona uma borda ao redor do layout principal
    )
