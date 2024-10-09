import flet as ft
from usuario import Usuario  # Importando do arquivo 'usuario.py'

def tela_cadastro(page: ft.Page):
    page.title = "Tela de Cadastro"
    page.window_width = 480
    page.window_height = 800
    page.bgcolor = "#FFFFFF"
    
    def realizar_cadastro(e):
        nome = name_input.value
        username = username_input.value
        email = email_input.value
        password = password_input.value

        # Cria um novo usuário no banco de dados
        novo_usuario = Usuario(nome, username, email, password)
        novo_usuario.salvar()
        resultado.value = f"Usuário {nome} cadastrado com sucesso!"
        resultado.color = "#28a745"  # Verde para sucesso
        page.update()

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
        bgcolor="#A2D2DF", 
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(weight="bold") 
        )
    )
    
    voltar_button = ft.ElevatedButton(
        text="Voltar", 
        on_click=lambda _: page.go("/"),  # Volta para a tela de login
        color="#03103F",  
        bgcolor="#A2D2DF", 
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(weight="bold") 
        )
    )
    
    resultado = ft.Text()

    # Retorna o layout da tela de cadastro para ser usado no `main.py`
    return ft.Row(
        [
            ft.Column(
                [
                    ft.Container(
                        content=ft.Text("Cadastro", size=50, weight="bold", color="#03103F"),
                        margin=ft.margin.only(top=50),  
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
                spacing=30,  
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
