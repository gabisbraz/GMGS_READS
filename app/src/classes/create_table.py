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


def main():
    connection = create_connection()

    # Create tables
    create_table_livros(connection)
    create_table_usuarios(connection)
    create_table_estante_usuario(connection)
    delete_table_estante_livros(connection)
    create_table_estante_livros(connection)

    # Fetch and display data from each table
    for table in ["Livros", "Usuarios", "EstanteUsuario", "EstanteLivros"]:
        print(f"\nConteúdo da tabela {table}:")
        df = fetch_data(connection, table)
        print(f"COLUMNS: {list(sorted(df.columns))}")

    # Close connection
    connection.close()


if __name__ == "__main__":
    main()
