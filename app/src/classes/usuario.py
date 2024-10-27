import mysql.connector
import bcrypt
from loguru import logger


def create_users_table(connection):
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


def create_connection():
    connection = mysql.connector.connect(
        host="database-1.ctj2rmaeyrwc.us-east-1.rds.amazonaws.com",
        user="admin",
        password="admin123",
        database="nxt_reads_db",
    )
    create_users_table(connection)
    return connection


class Usuario:
    """
    CLASSE QUE REPRESENTA UM USUÁRIO.
    """

    def __init__(self, nome: str, username: str, email: str, password: str):
        """
        INICIALIZA UM NOVO OBJETO 'USUARIO'.
        """
        self.nome = nome
        self.username = username
        self.email = email
        self.password = self.criptografar_senha(password)
        self.connection = create_connection()

    def criptografar_senha(self, senha: str) -> bytes:
        """
        CRIPTOGRAFA A SENHA UTILIZANDO O BCRYPT.
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(senha.encode("utf-8"), salt)

    def salvar(self) -> None:
        """
        SALVA O USUÁRIO NO BANCO DE DADOS MySQL.
        """
        cursor = self.connection.cursor()
        query = """
        INSERT INTO Usuarios (nome, username, email, password)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (self.nome, self.username, self.email, self.password.decode("utf-8")),
        )
        self.connection.commit()
        logger.info(f"Usuário {self.nome} criado com sucesso!")

    @staticmethod
    def verificar_senha(password_digitada: str, password_armazenada: str) -> bool:
        """
        VERIFICA SE A SENHA DIGITADA É VÁLIDA EM RELAÇÃO À SENHA ARMAZENADA.
        """
        return bcrypt.checkpw(
            password_digitada.encode("utf-8"), password_armazenada.encode("utf-8")
        )


def criar_usuario(nome: str, username: str, email: str, password: str) -> None:
    """
    CRIA E SALVA UM NOVO USUÁRIO NO BANCO DE DADOS MySQL.
    """
    novo_usuario = Usuario(nome, username, email, password)
    novo_usuario.salvar()


def select_records(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Usuarios")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def buscar_usuario(connection, username: str):
    """
    BUSCA UM USUÁRIO PELO NOME DE USUÁRIO (USERNAME).
    """
    cursor = connection.cursor()
    query = "SELECT * FROM Usuarios WHERE username = %s"
    cursor.execute(query, (username,))
    usuario = cursor.fetchone()  # Retorna apenas um usuário
    if usuario:
        return {
            "id": usuario[0],
            "nome": usuario[1],
            "username": usuario[2],
            "email": usuario[3],
            "password": usuario[4],
        }  # Mapeia os dados do usuário
    return None


if __name__ == "__main__":
    conn = create_connection()
    create_users_table(conn)  # Criar a tabela de usuários se não existir

    select_records(conn)

    # Fechar a conexão
    conn.close()
