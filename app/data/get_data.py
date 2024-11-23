import pandas as pd
import requests
import base64


def get_image(isbn):
    # Constrói a URL da imagem usando o ISBN fornecido
    return f"https://covers.openlibrary.org/b/isbn/{isbn}-S.jpg"


df = pd.read_csv("app/data/books.csv")


df["image"] = df["isbn"].apply(lambda isbn: get_image(isbn))

df.to_excel("app/data/books.xlsx", index=False)
print(1)
