import flet as ft
from usuario import Usuario  # Importando do arquivo 'usuario.py'

def tela_cadastro(page: ft.Page):
    page.title = "Tela de Cadastro"
    page.window_width = 480
    page.window_height = 800
    page.bgcolor = "#FFFFFF"  # Configura o fundo branco para a página

    def realizar_cadastro(e):
        nome = name_input.value
        username = username_input.value
        email = email_input.value
        password = password_input.value

        # Cria um novo usuário no banco de dados
        novo_usuario = Usuario(nome, username, email, password)
        novo_usuario.salvar()
        page.go("/cadastro_sucesso")

    # Componentes da tela de cadastro
    name_input = ft.TextField(
        label="Nome", 
        width=300, 
        border=ft.InputBorder.UNDERLINE,
    )
    
    username_input = ft.TextField(
        label="Usuário", 
        width=300, 
        border=ft.InputBorder.UNDERLINE,
    )
    
    email_input = ft.TextField(
        label="E-mail", 
        width=300, 
        border=ft.InputBorder.UNDERLINE,
    )
    
    password_input = ft.TextField(
        label="Senha", 
        password=True, 
        can_reveal_password=True, 
        width=300, 
        border=ft.InputBorder.UNDERLINE,
    )
    
    signup_button = ft.ElevatedButton(
        text="Concluir", 
        on_click=realizar_cadastro, 
        color="#03103F",  
        bgcolor="#D6E0E2", 
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(font_family="Sen Extra Bold", weight="bold")
        )
    )
    
    voltar_button = ft.ElevatedButton(
        text="Voltar", 
        on_click=lambda _: page.go("/"),  # Volta para a tela de login
        color="black",  
        bgcolor="#D6E0E2", 
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(font_family="Sen Extra Bold", weight="bold")
        )
    )
    
    resultado = ft.Text()

    # Container principal para os elementos de cadastro
    content = ft.Container(
        bgcolor="#FFFFFF",  # Fundo branco
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text("Cadastro", size=50, weight="bold", color="#03103F"),
                    margin=ft.margin.only(top=20),  
                ),
                ft.Container(
                    content=ft.Image(
                        src="app/assets/Ebook.gif",  
                        width=300,
                        height=300
                    ),
                    alignment=ft.alignment.center,
                    #margin=ft.margin.only(top=10, bottom=10)  # Add margin above and below the image
                ),
                name_input,
                username_input,
                email_input,
                password_input,
                signup_button,
                voltar_button,
                resultado,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,  # Espaço entre os elementos
        )
    )

    # Retorna o layout com fundo branco que preenche a tela inteira
    return ft.Container(
        expand=True,  # Certifica-se de que o fundo preencha toda a tela
        bgcolor="#FFFFFF",  # Fundo branco que cobre toda a tela
        content=ft.Row(
            [content],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True  # Garante que o conteúdo seja centralizado e preencha o espaço
        )
    )

def tela_cadastro_sucesso(page: ft.Page):
    page.title = "Cadastro Bem-Sucedido"
    page.window_width = 480
    page.window_height = 800
    page.bgcolor = "#FFFFFF"

    content = ft.Container(
        bgcolor="#FFFFFF",
        content=ft.Column(
            [
                ft.Text("Bem vindo(a)!", size=40, weight="bold", color="black"),
                ft.Text("Cadastro realizado com sucesso!", size=25, weight="bold", color="black"),
                ft.Image(src="app/assets/Welcome.gif", width=350, height=350), 
                ft.ElevatedButton(
                    text="Voltar à página inicial", 
                    on_click=lambda _: page.go("/"),
                    color="black",  
                    bgcolor="#D6E0E2", 
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(font_family="Sen Extra Bold", weight="bold")
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

    return ft.Container(
        expand=True,
        bgcolor="#FFFFFF",
        content=ft.Row(
            [content],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )
