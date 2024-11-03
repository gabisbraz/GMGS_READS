import mysql.connector
from passlib.context import CryptContext
from loguru import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Usuario:

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

    def criptografar_senha(self, senha: str) -> str:
        """
        CRIPTOGRAFA A SENHA UTILIZANDO O PASSLIB.
        """
        return pwd_context.hash(senha)

    def criar_usuario(
        self, nome: str, username: str, email: str, password: str
    ) -> None:
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
            (
                self.nome,
                self.username,
                self.email,
                self.criptografar_senha(self.password),
            ),
        )
        self.connection.commit()
        logger.info(f"Usuário {self.nome} criado com sucesso!")

    @staticmethod
    def verificar_senha(password_digitada: str, password_armazenada: str) -> bool:
        """
        VERIFICA SE A SENHA DIGITADA É VÁLIDA EM RELAÇÃO À SENHA ARMAZENADA.
        """
        return pwd_context.verify(password_digitada, password_armazenada)
