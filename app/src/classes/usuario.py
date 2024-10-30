import mysql.connector
from passlib.context import CryptContext  # Import passlib
from loguru import logger

# Setup passlib CryptContext for bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
        self.password = self.criptografar_senha(password)  # Hash the password
        self.connection = create_connection()

    def criptografar_senha(self, senha: str) -> str:
        """
        CRIPTOGRAFA A SENHA UTILIZANDO O PASSLIB.
        """
        return pwd_context.hash(senha)

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
            (self.nome, self.username, self.email, self.password),
        )
        self.connection.commit()
        logger.info(f"Usuário {self.nome} criado com sucesso!")

    @staticmethod
    def verificar_senha(password_digitada: str, password_armazenada: str) -> bool:
        """
        VERIFICA SE A SENHA DIGITADA É VÁLIDA EM RELAÇÃO À SENHA ARMAZENADA.
        """
        return pwd_context.verify(password_digitada, password_armazenada)


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


class Usuario:
    """
    Classe para gerenciar a base de dados de livros e realizar consultas.
    """

    def __init__(self):
        """
        Inicializa a classe 'Livro' e estabelece conexão com o banco de dados.
        """
        self.connection = self.create_connection()

    def create_connection(self):
        """
        Cria a conexão com o banco de dados MySQL.
        """
        try:
            connection = mysql.connector.connect(
                host="database-1.ctj2rmaeyrwc.us-east-1.rds.amazonaws.com",
                user="admin",
                password="admin123",
                database="nxt_reads_db",
            )
            logger.info("Conexão estabelecida com sucesso!")
            return connection
        except mysql.connector.Error as err:
            logger.error(f"Erro ao conectar ao banco de dados: {err}")
            return None

    def get_usuario(self, user):
        """
        Recupera um livro específico baseado no título (busca exata).
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM Usuarios WHERE username = %s"
            cursor.execute(query, (user,))
            book = cursor.fetchone()
            cursor.close()
            return book
        except mysql.connector.Error as err:
            logger.error(f"Erro ao buscar livro pelo título: {err}")
            return None


def buscar_usuario(username: str):
    """
    BUSCA UM USUÁRIO PELO NOME DE USUÁRIO (USERNAME).
    """
    user_conn = Usuario()

    usuario = user_conn.get_usuario(username)
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
