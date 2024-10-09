import pandas as pd
from tinydb import TinyDB, Query
from loguru import logger
import flet as ft

db_livros = TinyDB("livros.json")


class Livro:
    """
    CLASSE PARA GERENCIAR A BASE DE DADOS DE LIVROS E REALIZAR CONSULTAS.

    SE O BANCO DE DADOS ESTIVER VAZIO, ELE SERÁ POPULADO A PARTIR DE UM ARQUIVO CSV.
    """

    def __init__(self, csv_file: str):
        """
        INICIALIZA A CLASSE 'LIVRO' E POPULA O BANCO DE DADOS SE ESTIVER VAZIO.

        ARGUMENTOS:
        - csv_file: O CAMINHO PARA O ARQUIVO CSV COM OS DADOS DOS LIVROS.
        """
        if len(db_livros) == 0:
            logger.info(
                "Banco de dados de livros está vazio. Populando com dados do CSV..."
            )
            self.popular_db(csv_file)
        else:
            logger.info("Banco de dados de livros já está populado.")

    def popular_db(self, csv_file: str):
        """
        POPULA O BANCO DE DADOS A PARTIR DE UM ARQUIVO CSV.

        ARGUMENTOS:
        - csv_file: O CAMINHO PARA O ARQUIVO CSV COM OS DADOS DOS LIVROS.
        """
        try:
            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                db_livros.insert(
                    {
                        "bookID": row["bookID"],
                        "title": row["title"],
                        "authors": row["authors"],
                        "average_rating": row["average_rating"],
                        "isbn": row["isbn"],
                        "isbn13": row["isbn13"],
                        "language_code": row["language_code"],
                        "num_pages": row["num_pages"],
                        "ratings_count": row["ratings_count"],
                        "text_reviews_count": row["text_reviews_count"],
                        "publication_date": row["publication_date"],
                        "publisher": row["publisher"],
                    }
                )
            logger.info("Banco de dados populado com sucesso!")
        except FileNotFoundError:
            logger.error("Arquivo CSV não encontrado!")
        except Exception as e:
            logger.error(f"Erro ao popular o banco de dados: {e}")

    def buscar_livro(self, titulo: str):
        """
        BUSCA UM LIVRO NO BANCO DE DADOS PELO TÍTULO.

        ARGUMENTOS:
        - titulo: O TÍTULO DO LIVRO A SER BUSCADO.

        RETORNA:
        - UM DICIONÁRIO COM AS INFORMAÇÕES DO LIVRO SE ENCONTRADO, SENÃO UM AVISO.
        """
        LivroQuery = Query()
        livro = db_livros.search(LivroQuery.title == titulo)
        if livro:
            return livro[0]
        else:
            logger.warning(f"Livro '{titulo}' não encontrado.")
            return None


# FUNÇÃO PARA MOSTRAR UM ALERTA DE LIVRO NÃO ENCONTRADO
def mostrar_alerta_livro_nao_encontrado(page: ft.Page, titulo: str):
    """
    MOSTRA UM ALERTA QUANDO O LIVRO NÃO É ENCONTRADO.

    ARGUMENTOS:
    - page: OBJETO DA PÁGINA ATUAL DO FLET.
    - titulo: O TÍTULO DO LIVRO NÃO ENCONTRADO.
    """
    alerta = ft.AlertDialog(
        title=ft.Text("Livro não encontrado"),
        content=ft.Text(f"Não foi possível encontrar o livro com título '{titulo}'."),
        actions=[ft.TextButton("OK", on_click=lambda _: fechar_alerta(page))],
    )
    page.dialog = alerta
    alerta.open = True
    page.update()


# FUNÇÃO PARA FECHAR O ALERTA
def fechar_alerta(page: ft.Page):
    """
    FECHA O ALERTA ABERTO.

    ARGUMENTOS:
    - page: OBJETO DA PÁGINA ATUAL DO FLET.
    """
    page.dialog.open = False
    page.update()


# FUNÇÃO QUE LIDA COM A PESQUISA DO LIVRO
def buscar_livro_e_mostrar(
    page: ft.Page, livro_instance: Livro, input_pesquisa: ft.TextField
):
    """
    REALIZA A BUSCA PELO LIVRO E MOSTRA AS INFORMAÇÕES NA TELA.

    ARGUMENTOS:
    - page: OBJETO DA PÁGINA DO FLET.
    - livro_instance: INSTÂNCIA DA CLASSE LIVRO PARA REALIZAR A BUSCA.
    - input_pesquisa: CAMPO DE TEXTO ONDE O USUÁRIO DIGITA O TÍTULO DO LIVRO.
    """
    titulo = input_pesquisa.value
    livro = livro_instance.buscar_livro(titulo)

    if livro:
        # MOSTRA INFORMAÇÕES DO LIVRO ENCONTRADO
        page.add(
            ft.Column(
                [
                    ft.Text(f"Livro encontrado: {livro['title']}", size=24),
                    ft.Text(f"Autor(es): {livro['authors']}", size=18),
                    ft.Text(f"Avaliação: {livro['average_rating']}", size=18),
                    ft.Text(f"ISBN: {livro['isbn']}", size=18),
                    ft.Text(f"Editora: {livro['publisher']}", size=18),
                    # Adicione outras informações aqui conforme necessário
                ],
                spacing=10,
            )
        )
    else:
        # MOSTRA ALERTA DE LIVRO NÃO ENCONTRADO
        mostrar_alerta_livro_nao_encontrado(page, titulo)


# FUNÇÃO PRINCIPAL PARA INICIALIZAR A INTERFACE
def main(page: ft.Page):
    """
    FUNÇÃO PRINCIPAL PARA CONSTRUIR A INTERFACE DE BUSCA DE LIVROS.

    ARGUMENTOS:
    - page: OBJETO DA PÁGINA PRINCIPAL DO FLET.
    """
    # INSTANCIAR O OBJETO LIVRO
    livro_instance = Livro("app/data/books.csv")

    # CAMPO DE PESQUISA
    input_pesquisa = ft.TextField(label="Buscar livro pelo título", width=400)

    # BOTÃO DE PESQUISA
    botao_pesquisa = ft.ElevatedButton(
        "Buscar",
        on_click=lambda e: buscar_livro_e_mostrar(page, livro_instance, input_pesquisa),
    )

    # ADICIONA O CAMPO E O BOTÃO À PÁGINA
    page.add(
        ft.Column(
            [
                ft.Text("Sistema de Consulta de Livros", size=30),
                input_pesquisa,
                botao_pesquisa,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


# EXECUTA A APLICAÇÃO FLET
if __name__ == "__main__":
    ft.app(target=main)
