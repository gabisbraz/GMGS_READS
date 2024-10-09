import flet as ft
from tela_login import tela_login  # Importa a tela de login
from tela_cadastro import tela_cadastro  # Importa a tela de cadastro

def main(page: ft.Page):
    # Define the screen layout
    def home_screen(page: ft.Page):
        page.window_width = 480
        page.window_height = 800
        page.window_resizable = False  # Impede que a janela seja redimensionada
        page.window_always_on_top = True  # Opcional, mantém a janela no topo
        
        # Background image
        background_container = ft.Container(
            width=480,
            height=800,
            image_src="app/assets/image.png",  # Replace with the correct image path
            image_fit=ft.ImageFit.COVER  # Image covers the entire background
        )
        
        # "NXT Reads" text group
        text_group = ft.Column(
            [
                # Custom font size and font family for "NXT"
                ft.Text("NXT", size=60, weight="bold", color="black", font_family="Verdana"),
                
                # Custom font size and font family for "Reads"
                ft.Text("Reads", size=60, weight="bold", color="black", font_family="Verdana"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,  # No space between "NXT" and "Reads"
        )

        # Buttons group
        buttons_group = ft.Column(
            [
                ft.ElevatedButton(
                    text="Login", 
                    on_click=lambda _: page.go("/login"),
                    bgcolor="#D6E0E2", 
                    color="black",
                    #width=200,  # Set the width of the button
                    height=60,  # Set the height of the button
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=30, font_family="Arial", weight="bold")  # Font size and family
                    )
                ),
                
                ft.ElevatedButton(
                    text="Cadastre-se", 
                    on_click=lambda _: page.go("/signup"),
                    bgcolor="#D6E0E2", 
                    color="black",
                    #width=200,  # Set the width of the button
                    height=60,  # Set the height of the button
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=30, font_family="Arial", weight="bold")  # Font size and family
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=40,  # Space between the buttons
        )

        # Combine text and buttons, but keep them visually separate
        content = ft.Column(
            [
                # Add some margin to the top of the "NXT Reads" text group
                ft.Container(
                    content=text_group,
                    margin=ft.margin.only(top=90),
                ),
                
                # Space between text and buttons group
                buttons_group
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=120,  # Space between the text group and buttons group
        )
        
        # Stack background and content
        return ft.Stack(
            [
                background_container,  # Background image
                ft.Container(content=content, alignment=ft.alignment.center)  # Centralize the content
            ]
        )

    def route_change(route):
        page.theme_mode = ft.ThemeMode.LIGHT
        page.bgcolor = "#FFFFFF"
        page.views.clear()

        # Define routes for login and signup
        if page.route == "/":
            page.views.append(ft.View("/", [home_screen(page)]))  # Home screen
        elif page.route == "/login":
            page.views.append(ft.View("/login", [tela_login(page)]))  # Login screen
        elif page.route == "/signup":
            page.views.append(ft.View("/signup", [tela_cadastro(page)]))  # Signup screen

        page.update()

    page.on_route_change = route_change
    page.go("/")  # Initial route is the home screen

# Initialize the app
ft.app(target=main)
