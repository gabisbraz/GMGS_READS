import mysql.connector
import pandas as pd


def create_connection():
    connection = mysql.connector.connect(
        host="database-1.ctj2rmaeyrwc.us-east-1.rds.amazonaws.com",
        user="admin",
        password="admin123",
        database="nxt_reads_db",
    )
    return connection


def create_table_livros(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
CREATE TABLE IF NOT EXISTS Livros (
    bookID INT PRIMARY KEY AUTO_INCREMENT,  -- Coluna auto-incrementada para o ID do livro
    title VARCHAR(255),                      -- Título do livro
    authors VARCHAR(255),                    -- Autor do livro
    description TEXT,                        -- Descrição do livro
    num_pages INT,                           -- Páginas do livro
    genres VARCHAR(255),                     -- Gêneros do livro
    average_rating FLOAT,                    -- Nota média do livro
    ratings_count INT,                       -- Quantidade de avaliações
    google_book VARCHAR(255),                -- Link do Google Book
    image_url VARCHAR(255),                  -- Link para a imagem do livro
    isbn VARCHAR(20),                        -- ISBN do livro
    search VARCHAR(255),                     -- Termo de pesquisa relacionado ao livro
    image_ol VARCHAR(255),                   -- Link para a imagem do Open Library
    image_b64 TEXT                           -- Imagem do livro em base64
);
"""
    )
    connection.commit()


def create_table_usuarios(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
CREATE TABLE IF NOT EXISTS Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255),
    username VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);
"""
    )
    connection.commit()


def create_table_estante_usuario(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
CREATE TABLE IF NOT EXISTS EstanteUsuario (
    estante_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    nome VARCHAR(255),
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id)
);
"""
    )
    connection.commit()


def create_table_estante_livros(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
CREATE TABLE IF NOT EXISTS EstanteLivros (
    estante_id INT,
    livro_id INT,
    comecou_leitura DATE,      
    terminou_leitura DATE,      
    porcentagem INT DEFAULT 0,  
    nota DECIMAL(3, 2),         
    PRIMARY KEY (estante_id, livro_id),
    FOREIGN KEY (estante_id) REFERENCES EstanteUsuario(estante_id),
    FOREIGN KEY (livro_id) REFERENCES Livros(bookID)
);
"""
    )
    connection.commit()


def delete_table_estante_livros(connection):
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS EstanteLivros;")
    connection.commit()
    print("Tabela EstanteLivros deletada com sucesso.")


def fetch_data(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name};")
    results = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    return pd.DataFrame(results, columns=column_names)


def delete_all_tables(connection):
    cursor = connection.cursor()
    # Deleta todas as tabelas. Certifique-se de que as tabelas estão na ordem certa,
    # pois tabelas com chaves estrangeiras precisam ser deletadas primeiro.
    cursor.execute(
        "SET FOREIGN_KEY_CHECKS = 0;"
    )  # Desabilita as verificações de chave estrangeira
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table[0]};")
    cursor.execute(
        "SET FOREIGN_KEY_CHECKS = 1;"
    )  # Habilita as verificações de chave estrangeira
    connection.commit()
    print("Todas as tabelas foram deletadas com sucesso.")


def insert_data_to_livros(df, connection):
    cursor = connection.cursor()

    # Mapeamento de colunas do DataFrame para a tabela 'Livros'
    column_mapping = {
        "Título": "title",
        "Autor": "authors",
        "Descrição": "description",
        "Páginas": "num_pages",
        "Gêneros": "genres",
        "Nota": "average_rating",
        "Qtd. Avaliações": "ratings_count",
        "Google Book": "google_book",
        "Link Imagem": "image_url",
        "ISBN": "isbn",
        "Pesquisar": "search",
        "IMAGEM OL": "image_ol",
        "IMAGEM B64": "image_b64",
    }

    # Renomear as colunas do DataFrame de acordo com o mapeamento
    df_renamed = df.rename(columns=column_mapping)

    # Inserir os dados na tabela 'Livros'
    for index, row in df_renamed.iterrows():
        sql = """
        INSERT INTO Livros (title, authors, description, num_pages, genres, 
                            average_rating, ratings_count, google_book, 
                            image_url, isbn, search, image_ol, image_b64)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        values = (
            row["title"],
            row["authors"],
            row["description"],
            row["num_pages"],
            row["genres"],
            row["average_rating"],
            row["ratings_count"],
            row["google_book"],
            row["image_url"],
            row["isbn"],
            row["search"],
            row["image_ol"],
            row["image_b64"],
        )

        cursor.execute(sql, values)

    connection.commit()  # Confirma as mudanças no banco de dados
    print(f"{len(df)} registros inseridos com sucesso na tabela 'Livros'.")


def create_user(connection, user_data):
    cursor = connection.cursor()
    sql = """
    INSERT INTO Usuarios (email, id, nome, password, username)
    VALUES (%s, %s, %s, %s, %s);
    """
    try:
        cursor.execute(sql, user_data)
        connection.commit()
        print("Usuário inserido com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao inserir usuário: {err}")
    finally:
        cursor.close()


def main():
    connection = create_connection()

    # user_data = ("taylor_swift.gmail.com", 1, "Taylor Swift", "123", "Taylor Swift")
    # create_user(connection, user_data)
    # df = pd.read_excel("app/data/result_API2.xlsx")
    # delete_all_tables(connection)

    # create_table_livros(connection)
    # create_table_usuarios(connection)
    # create_table_estante_usuario(connection)
    # create_table_estante_livros(connection)

    # insert_data_to_livros(df, connection=connection)

    # Fetch and display data from each table
    for table in ["Livros", "Usuarios", "EstanteUsuario", "EstanteLivros"]:
        print(f"\nConteúdo da tabela {table}:")
        df = fetch_data(connection, table)
        print(f"COLUMNS: {list(sorted(df.columns))}")
        print(df.head(5))

    # Close connection
    connection.close()


if __name__ == "__main__":
    main()
