import flet as ft
from usuario import buscar_usuario, Usuario  # Importando do arquivo 'usuario.py'

def tela_login(page: ft.Page):
    page.title = "Tela de Login"
    page.window_width = 480
    page.window_height = 800
    page.bgcolor = "#FFFFFF"
    
    def realizar_login(e):
        username = username_input.value
        password = password_input.value

        # Busca o usuário no banco de dados
        usuario_encontrado = buscar_usuario(username)

        if usuario_encontrado:
            # Verifica se a senha está correta
            if Usuario.verificar_senha(password, usuario_encontrado["password"]):
                resultado.value = f"Bem-vindo, {usuario_encontrado['nome']}!"
                resultado.color = "#28a745"  # Verde para sucesso
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
        color="#03103F",  
        bgcolor="#A2D2DF",  
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(weight="bold") 
        )
    )
    
    signup_button = ft.ElevatedButton(
        text="Cadastrar-se", 
        on_click=lambda _: page.go("/signup"),  # Redireciona para a tela de cadastro
        color="#03103F",  
        bgcolor="#A2D2DF", 
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(weight="bold") 
        )
    )
    
    resultado = ft.Text()

    # Retorna o layout da tela de login para ser usado no `main.py`
    return ft.Row(
        [
            ft.Column(
                [
                    ft.Container(
                        content=ft.Text("Login", size=50, weight="bold", color="#03103F"),
                        margin=ft.margin.only(top=50),  
                    ),
                    username_input,
                    password_input,
                    login_button,
                    signup_button,
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
