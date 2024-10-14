import sys
from pathlib import Path
import flet as ft

DIR_ROOT = str(Path(__name__).absolute().parents[0])
if DIR_ROOT not in sys.path:
    sys.path.append(DIR_ROOT)

try:
    from app.utils.usuario import Usuario, buscar_usuario, criar_usuario, db
except ModuleNotFoundError:
    from utils.usuario import Usuario, buscar_usuario, criar_usuario, db


# FUNÇÃO QUE EXIBE UM ALERTA NA TELA
def mostrar_alerta(page: ft.Page, titulo: str, mensagem: str) -> None:
    """
    EXIBE UM DIÁLOGO DE ALERTA COM TÍTULO E MENSAGEM.

    ARGUMENTOS:
    - page: OBJETO DA PÁGINA ATUAL DO FLET.
    - titulo: TEXTO DO TÍTULO DO ALERTA.
    - mensagem: TEXTO DO CORPO DA MENSAGEM DO ALERTA.
    """

    # FUNÇÃO INTERNA PARA FECHAR O DIÁLOGO DE ALERTA
    def fechar_dialogo(e: ft.ControlEvent) -> None:
        # DEFINE O ATRIBUTO 'OPEN' DO ALERTA COMO FALSO (FECHA O DIÁLOGO)
        alerta.open = False
        page.update()

    # CRIA UM ALERTA UTILIZANDO O COMPONENTE 'ALERTDIALOG' DO FLET
    alerta = ft.AlertDialog(
        title=ft.Text(titulo),
        content=ft.Text(mensagem),
        actions=[
            ft.TextButton("OK", on_click=fechar_dialogo)  # BOTÃO PARA FECHAR O DIÁLOGO
        ],
    )

    # ATRIBUI O ALERTA À PÁGINA E O ABRE
    page.dialog = alerta
    alerta.open = True
    page.update()


def main(page: ft.Page) -> None:
    """
    FUNÇÃO PRINCIPAL QUE CONSTRÓI A INTERFACE DE LOGIN E CADASTRO NO FLET.

    ARGUMENTOS:
    - page: OBJETO DA PÁGINA PRINCIPAL DO FLET.
    """

    # CONFIGURA O TÍTULO E ALINHAMENTO DA PÁGINA
    page.title = "Login e Cadastro"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # FUNÇÃO PARA CADASTRAR UM NOVO USUÁRIO
    def cadastrar_usuario(e: ft.ControlEvent) -> None:
        """
        LIDA COM A LÓGICA DE CADASTRO DE UM NOVO USUÁRIO.

        ARGUMENTOS:
        - e: EVENTO DISPARADO PELO BOTÃO DE CADASTRO.
        """

        # OBTÉM OS VALORES DOS CAMPOS DE TEXTO
        nome = input_nome.value
        username = input_username.value
        email = input_email.value
        password = input_password.value

        # VERIFICA SE TODOS OS CAMPOS ESTÃO PREENCHIDOS
        if not nome or not username or not email or not password:
            mostrar_alerta(page, "Erro", "Por favor, preencha todos os campos.")
            return

        # VERIFICA SE O USUÁRIO JÁ EXISTE NO BANCO DE DADOS
        if buscar_usuario(username):
            mostrar_alerta(page, "Erro", "Usuário já existe.")
            return

        # CRIA UM NOVO USUÁRIO E MOSTRA UMA MENSAGEM DE SUCESSO
        criar_usuario(nome, username, email, password)
        mostrar_alerta(page, "Sucesso", "Usuário cadastrado com sucesso.")

    # CRIA CAMPOS DE ENTRADA DE DADOS PARA NOME, EMAIL E SENHA
    input_nome = ft.TextField(label="Nome", width=300)
    input_username = ft.TextField(label="Username", width=300)
    input_email = ft.TextField(label="Email", width=300)
    input_password = ft.TextField(label="Senha", password=True, width=300)

    # CRIA O BOTÃO DE CADASTRO
    botao_cadastro = ft.ElevatedButton("Cadastrar", on_click=cadastrar_usuario)

    # ADICIONA O CONTEÚDO À PÁGINA (CAMPOS E BOTÃO)
    page.add(
        ft.Column(
            [
                ft.Text("Cadastrar Novo Usuário", size=30),
                input_nome,
                input_username,
                input_email,
                input_password,
                botao_cadastro,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

# EXECUTA A APLICAÇÃO FLET
if __name__ == "__main__":
    ft.app(target=main)
