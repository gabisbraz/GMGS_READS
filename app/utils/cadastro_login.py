import flet as ft
from login import tela_login  # Importa a tela de login
from cadastro import tela_cadastro  # Importa a tela de cadastro

def main(page: ft.Page):
    def route_change(route):
        page.theme_mode = ft.ThemeMode.LIGHT
        page.bgcolor = "#FFFFFF"
        # Limpa as views atuais
        page.views.clear()

        # Verifica qual rota foi chamada e exibe a tela correspondente
        if page.route == "/":
            page.views.append(ft.View("/", [tela_login(page)]))  # Mostra a tela de login
        elif page.route == "/signup":
            page.views.append(ft.View("/signup", [tela_cadastro(page)]))  # Mostra a tela de cadastro

        # Atualiza a página para exibir a nova view
        page.update()

    # Define o comportamento quando a rota for alterada
    page.on_route_change = route_change

    # Começa com a tela de login
    page.go("/")  # Define a rota inicial como "/"

# Inicializa a aplicação Flet com a função principal
ft.app(target=main)
