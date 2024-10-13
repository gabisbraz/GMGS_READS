import flet as ft
from usuario import buscar_usuario, Usuario  # Importando do arquivo 'usuario.py'

import flet as ft
from usuario import buscar_usuario, Usuario  # Importando do arquivo 'usuario.py'

def tela_login(page: ft.Page):
    page.title = "Tela de Login"
    page.window_width = 480
    page.window_height = 800
    page.bgcolor = "#FFFFFF"  # Set the background color for the entire page

    def realizar_login(e):
        username = username_input.value
        password = password_input.value

        # Busca o usuário no banco de dados
        usuario_encontrado = buscar_usuario(username)

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
        border=ft.InputBorder.UNDERLINE,
    )
    
    password_input = ft.TextField(
        label="Senha", 
        password=True, 
        can_reveal_password=True, 
        width=300, 
        border=ft.InputBorder.UNDERLINE,
    )
    
    login_button = ft.ElevatedButton(
        text="Concluir", 
        on_click=realizar_login, 
        color="black",  
        bgcolor="#D6E0E2",  
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(font_family="Sen Extra Bold", weight="bold")
        )
    )
    
    signup_button = ft.ElevatedButton(
        text="Cadastrar-se", 
        on_click=lambda _: page.go("/signup"),  # Redireciona para a tela de cadastro
        color="black",  
        bgcolor="#D6E0E2", 
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(font_family="Sen Extra Bold", weight="bold")
        )
    )
    
    resultado = ft.Text()

    # Main container that will hold all login elements
    content = ft.Container(
        bgcolor="#FFFFFF",  # White background for the container
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text("Login", size=50, weight="bold", color="#03103F"),
                    margin=ft.margin.only(top=50),  
                ),
                ft.Container(
                    content=ft.Image(
                        src="app/assets/Kids reading.gif",  
                        width=300,
                        height=300
                    ),
                    alignment=ft.alignment.center,
                    #margin=ft.margin.only(top=10, bottom=10)  # Add margin above and below the image
                ),
                username_input,
                password_input,
                login_button,
                signup_button,
                resultado,
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

def tela_login_sucesso(page: ft.Page):
    page.title = "Login Bem-Sucedido"
    page.window_width = 480
    page.window_height = 800
    page.bgcolor = "#FFFFFF"

    content = ft.Container(
        bgcolor="#FFFFFF",
        content=ft.Column(
            [
                ft.Text("Login realizado com sucesso!", size=30, weight="bold", color="black"),
                ft.Image(src="app/assets/Celebration.gif", width=300, height=300),  # Exemplo de GIF ou imagem de sucesso
                ft.ElevatedButton(
                    text="Buscar por livros", 
                    on_click=lambda _: page.go("/busca_livros"),
                    color="black",  
                    bgcolor="#D6E0E2", 
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(font_family="Sen Extra Bold", weight="bold")
                    )
                ),
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
