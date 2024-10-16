import flet as ft
from tela_login import tela_login  # Importa a tela de login
from tela_login import tela_login_sucesso
from tela_cadastro import tela_cadastro  # Importa a tela de cadastro
from tela_cadastro import tela_cadastro_sucesso
from tela_busca import tela_busca

def main(page: ft.Page):
    # Define o layout da página

    page.fonts = {
        "Sen Extra Bold": "app/fonts/Sen-ExtraBold.ttf",
        "Sen Medium": "app/fonts/Sen-Medium.ttf"
    }

    def home_screen(page: ft.Page):
        page.window_width = 480
        page.window_height = 800
        page.window_resizable = False  
        page.window_always_on_top = True  

        # Envolve todo o conteúdo em um Container com bordas arredondadas
        content_container = ft.Container(
            expand=True,
            bgcolor="#FFFFFF",  # Define o fundo do Container
            border_radius=ft.border_radius.all(20),  # Define o raio das bordas
            clip_behavior=ft.ClipBehavior.HARD_EDGE,  # Garante que o conteúdo não ultrapasse as bordas
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Welcome to", size=30, weight="bold", color="black", font_family="Sen Extra Bold"),
                                ft.Text("NXT", size=60, weight="bold", color="black", font_family="Sen Extra Bold"),
                                ft.Text("Reads", size=60, weight="bold", color="black", font_family="Sen Extra Bold"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        ),
                    ),
                    ft.Container(
                        content=ft.Image(
                            src="app/assets/Literature.gif",  
                            width=300,
                            height=300
                        ),
                        alignment=ft.alignment.center,
                    ),
                    ft.Text("Find your next favorite book!", size=15, weight="bold", color="black", font_family="Sen Medium"),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.ElevatedButton(
                                    text="Login", 
                                    on_click=lambda _: page.go("/login"),
                                    bgcolor="#D6E0E2", 
                                    color="black",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=15),  # Cantos arredondados nos botões
                                        text_style=ft.TextStyle(size=20, font_family="Sen Extra Bold", weight="bold")
                                    )
                                ),
                                ft.ElevatedButton(
                                    text="Cadastre-se", 
                                    on_click=lambda _: page.go("/signup"),
                                    bgcolor="#D6E0E2", 
                                    color="black",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=15),  # Cantos arredondados nos botões
                                        text_style=ft.TextStyle(size=20, font_family="Sen Extra Bold", weight="bold")
                                    )
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            )
        )
        
        # Retorna o Container com as bordas arredondadas
        return ft.Container(
            expand=True,
            content=content_container,
            alignment=ft.alignment.center
        )

    def route_change(route):
        #page.theme_mode = ft.ThemeMode.LIGHT
        #page.bgcolor = "#FFFFFF" 
        page.views.clear()

        # Define rotas
        if page.route == "/":
            page.views.append(ft.View("/", [home_screen(page)]))  # Tela inicial
        elif page.route == "/login":
            page.views.append(ft.View("/login", [tela_login(page)]))  # Tela de login
        elif page.route == "/signup":
            page.views.append(ft.View("/signup", [tela_cadastro(page)]))  # Tela de cadastro
        elif page.route == "/login_sucesso":
            page.views.append(ft.View("/login_sucesso", [tela_login_sucesso(page)]))
        elif page.route == "/cadastro_sucesso":
            page.views.append(ft.View("/cadastro_sucesso", [tela_cadastro_sucesso(page)]))
        elif page.route == "/busca_livros":
            page.views.append(ft.View("/busca_livros", [tela_busca(page)]))

        page.update()

    page.on_route_change = route_change
    page.go("/")  # Rota inicial

def test_main():
    # Simula a execução do app
    app = ft.app(target=main)
    app.start()

    # Adicione aqui suas verificações, por exemplo, se um elemento está presente
    assert "Hello, Flet!" in app.page.controls[0].content

if __name__ == "__main__":
    test_main()
