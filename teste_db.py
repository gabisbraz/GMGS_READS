import mysql.connector
import pandas as pd


# Estabelecer uma conexão com o banco de dados
def create_connection():
    connection = mysql.connector.connect(
        host="db-nxt-reads.ctj2rmaeyrwc.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Admin123",
        database="next_reads_database",
    )
    return connection


def create_table(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
CREATE TABLE IF NOT EXISTS Livros (
    bookID INT PRIMARY KEY,
    title VARCHAR(255),
    authors VARCHAR(255),
    average_rating FLOAT,
    isbn VARCHAR(20),
    isbn13 VARCHAR(20),
    language_code VARCHAR(10),
    num_pages INT,
    ratings_count INT,
    text_reviews_count INT,
    publication_date DATE,
    publisher VARCHAR(255)
);
"""
    )
    connection.commit()  # Commit para garantir que a tabela seja criada


def insert_record(connection, record):
    cursor = connection.cursor()
    query = """
        INSERT INTO Livros (bookID, title, authors, average_rating, isbn, isbn13, language_code, num_pages, ratings_count, text_reviews_count, publication_date, publisher)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, record)
    connection.commit()  # Commit para garantir que a inserção seja salva


def delete_record(connection):
    cursor = connection.cursor()
    query = "DELETE FROM Livros"
    cursor.execute(query)
    connection.commit()


def select_records(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Livros")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def insert_multiple_records(connection, records):
    cursor = connection.cursor()
    query = """
        INSERT INTO Livros (bookID, title, authors, average_rating, isbn, isbn13, language_code, num_pages, ratings_count, text_reviews_count, publication_date, publisher)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(query, records)
    connection.commit()  # Commit para garantir que a inserção seja salva


# Função principal para executar o código
if __name__ == "__main__":
    conn = create_connection()
    create_table(conn)  # Criar a tabela se não existir

    # Limpar a tabela Livros
    delete_record(conn)

    data = pd.read_csv("app/data/books.csv")

    df = pd.DataFrame(data)

    # Converter os dados do DataFrame em uma lista de tuplas para inserção
    records_to_insert = list(df.itertuples(index=False, name=None))

    # Inserir múltiplos registros na tabela
    insert_multiple_records(conn, records_to_insert)

    # Exibir os registros inseridos
    select_records(conn)

    # Fechar a conexão
    conn.close()
