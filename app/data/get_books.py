# import requests
import pandas as pd

# import random
# from loguru import logger
# import base64
# from io import BytesIO


# def get_livro(titulo):
#     titulo_formatado = titulo.replace(" ", "+")

#     url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{titulo_formatado}"
#     # url = f"https://openlibrary.org/search.json?title={titulo_formatado}"

#     response = requests.get(url)

#     if response.status_code == 200:
#         dados = response.json()

#         if "items" in dados and len(dados["items"]) > 0:
#             livro = dados["items"][0]["volumeInfo"]

#             title = livro.get("title", "Não disponível")

#             authors = ", ".join(livro.get("authors", ["Não disponível"]))
#             logger.debug(f"AUTOR: {authors}")

#             description = livro.get("description", "Não disponível")
#             logger.debug(f"DESCRIÇÃO: {description}")

#             pageCount = livro.get("pageCount", "Não disponível")
#             logger.debug(f"PÁGINAS: {pageCount}")

#             genero = ", ".join(livro.get("categories", ["Não disponível"]))
#             images1 = livro.get("imageLinks", "Não disponível")
#             try:
#                 if images1:
#                     img = images1.get("thumbnail")
#             except Exception:
#                 img = "Não disponível"

#             isbn = livro.get("industryIdentifiers", "Não disponível")
#             try:
#                 if isbn:
#                     isbn = isbn[0]
#                     isbn_1 = isbn.get("identifier")
#             except Exception:
#                 isbn_1 = "Não disponível"

#             logger.debug(f"GÊNERO: {genero}")

#             canonicalVolumeLink = livro.get("canonicalVolumeLink", ["Não disponível"])

#             valores = [x * 0.5 for x in range(6, 11)]

#             # Escolher um valor aleatório da lista
#             averageRating = random.choice(valores)
#             logger.debug(f"NOTA: {averageRating}")

#             # Escolher um valor aleatório da lista
#             qtd_avaliacoes = random.randint(100, 1000000)

#             return {
#                 "Título": title,
#                 "Autor": authors,
#                 "Descrição": description,
#                 "Páginas": pageCount,
#                 "Gêneros": genero,
#                 "Nota": averageRating,
#                 "Qtd. Avaliações": qtd_avaliacoes,
#                 "Google Book": canonicalVolumeLink,
#                 "Link Imagem": img,
#                 "ISBN": isbn_1,
#             }
#         else:
#             return {
#                 "Título": titulo,
#                 "Autor": "Não encontrado",
#                 "Descrição": "Não disponível",
#                 "Páginas": "Não disponível",
#                 "Gêneros": "Não disponível",
#                 "Nota": "Não disponível",
#                 "Qtd. Avaliações": "Não disponível",
#                 "Google Book": "Não disponível",
#                 "Link Imagem": "Não disponível",
#                 "ISBN": "Não disponível",
#             }
#     else:
#         logger.error(f"Erro na requisição: {response.status_code}")
#         return None


# def processar_livros(arquivo_txt, arquivo_excel):
#     lista_livros = []

#     with open(arquivo_txt, "r") as file:
#         for linha in file:
#             titulo = linha.strip()
#             if titulo:
#                 logger.info(f"Buscando livro: {titulo}...")
#                 dados_livro = get_livro(titulo)
#                 if dados_livro:
#                     lista_livros.append(dados_livro)
#                     logger.success(f"Livro adicionado a lista: {titulo}")

#     df = pd.DataFrame(lista_livros)

#     df.to_excel(arquivo_excel, index=False)
#     logger.success(f"Os dados foram salvos no arquivo {arquivo_excel}.")


# arquivo_txt = "app/data/book.txt"
# arquivo_excel = "app/data/result_API2.xlsx"
# processar_livros(arquivo_txt, arquivo_excel)


# def generate_google_link(marca, modelo):
#     query = f"{marca} {modelo}"
#     google_search_link = f"https://www.google.com/search?q={query.replace(' ', '+')}"
#     return google_search_link


# Cria a coluna 'LINK' com os hyperlinks
df = pd.read_excel("app/data/result_API2.xlsx")

# print(df.columns)

# # df["Pesquisar"] = df.apply(
# #     lambda row: generate_google_link(row["Título"], row["Autor"]), axis=1
# # )


# def get_image(isbn):
#     # Constrói a URL da imagem usando o ISBN fornecido
#     image_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-S.jpg"

#     try:
#         # Faz a requisição HTTP para obter a imagem
#         response = requests.get(image_url)
#         response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

#         # Converte a imagem em base64
#         image_data = BytesIO(response.content)  # Carrega a imagem em memória
#         image_base64 = base64.b64encode(image_data.read()).decode(
#             "utf-8"
#         )  # Codifica em base64
#         return image_base64
#     except requests.exceptions.RequestException:
#         # Em caso de erro, retorna None
#         return None


# df["ISBN"].apply(lambda isbn: get_image(isbn))
# df.to_excel("app/data/result_API2.xlsx", index=False)


import os
import requests
import base64

# Define o caminho para a pasta onde as imagens serão salvas
output_dir = "app/data/book_covers"
os.makedirs(output_dir, exist_ok=True)  # Cria a pasta se ela não existir


def get_image(isbn, title):
    # URL inicial para obter o JSON com a URL da imagem
    image_url = f"https://bookcover.longitood.com/bookcover/{isbn}"

    try:
        # Faz a requisição para obter o JSON com o link da imagem
        response = requests.get(image_url)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

        # Extrai a URL real da imagem
        img_url = response.json().get("url")
        if not img_url:
            return None  # Retorna None se a URL da imagem não estiver disponível

        # Faz uma nova requisição para obter o conteúdo da imagem real
        image_response = requests.get(img_url)
        image_response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

        # Nome do arquivo formatado com título
        image_filename = f"{title}_img.png".replace(
            " ", "_"
        )  # Substitui espaços para evitar problemas no nome do arquivo
        image_path = os.path.join(output_dir, image_filename)

        # Salva o conteúdo da imagem diretamente no arquivo
        with open(image_path, "wb") as f:
            f.write(image_response.content)

        # Converte a imagem em base64 para armazenar no DataFrame
        image_base64 = base64.b64encode(image_response.content).decode("utf-8")
        print(f"SUCESSO - {title}")
        return image_base64
    except requests.exceptions.RequestException:
        print(f"ERRO - {title}")
        # Em caso de erro, retorna None
        return "-"


# Aplica a função get_image ao DataFrame e salva as imagens com o título do livro no nome do arquivo
df["IMAGEM B64"] = df.apply(lambda row: get_image(row["ISBN"], row["Título"]), axis=1)
df.to_excel("app/data/result_API2.xlsx", index=False)
