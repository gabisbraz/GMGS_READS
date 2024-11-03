import mysql.connector
from loguru import logger


def get_cover_url(isbn):
    return f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"


class Livro:

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

    def search_books_by_title(self, title_part):
        """
        Busca livros pelo título parcial no banco de dados.
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = (
                "SELECT bookID, title, authors FROM Livros WHERE title LIKE %s LIMIT 5"
            )
            cursor.execute(query, ("%" + title_part + "%",))
            books = cursor.fetchall()
            cursor.close()
            return books
        except mysql.connector.Error as err:
            logger.error(f"Erro ao buscar livros: {err}")
            return []

    def search_random_books(self):
        """
        Busca 50 livros aleatoriamente no banco de dados.
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = (
                "SELECT bookID, title, authors, average_rating, isbn, isbn13, num_pages, ratings_count, publication_date "
                "FROM Livros ORDER BY RAND() LIMIT 50"
            )
            cursor.execute(query)
            books = cursor.fetchall()
            cursor.close()
            return books
        except mysql.connector.Error as err:
            logger.error(f"Erro ao buscar livros aleatórios: {err}")
            return []

    def get_book_by_id(self, book_id):
        """
        Retorna todas as informações de um livro com base no ID fornecido.
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM Livros WHERE bookID = %s"
            cursor.execute(query, (book_id,))
            book = cursor.fetchone()  # Use fetchone() para obter um único registro
            cursor.close()
            if book:
                return book
            else:
                logger.warning(f"Nenhum livro encontrado com o ID: {book_id}")
                return None
        except mysql.connector.Error as err:
            logger.error(f"Erro ao buscar livro pelo ID {book_id}: {err}")
            return None

    def create_shelf(self, user_id, shelf_name):
        """
        Cria uma nova estante para o usuário.
        """
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO EstanteUsuario (usuario_id, nome) VALUES (%s, %s)"
            cursor.execute(query, (user_id, shelf_name))
            self.connection.commit()
            cursor.close()
            logger.info(f"Estante '{shelf_name}' criada com sucesso!")
        except mysql.connector.Error as err:
            logger.error(f"Erro ao criar estante: {err}")

    def get_user_shelves(self, user_id):
        """
        Retorna todas as estantes de um usuário com base no ID do usuário fornecido.
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT estante_id, nome FROM EstanteUsuario WHERE usuario_id = %s"
            cursor.execute(query, (user_id,))
            shelves = cursor.fetchall()
            cursor.close()
            return shelves
        except mysql.connector.Error as err:
            logger.error(f"Erro ao buscar estantes do usuário {user_id}: {err}")
            return []

    def add_book_to_shelf(
        self,
        estante_id,
        livro_id,
        porcentagem=0,
        comecou_leitura=None,
        terminou_leitura=None,
        nota=None,
    ):
        """
        Adiciona um livro a uma estante específica do usuário com dados adicionais de leitura.
        """
        try:
            cursor = self.connection.cursor()

            # SQL para inserir os dados na tabela EstanteLivros
            query = """
                INSERT INTO EstanteLivros (estante_id, livro_id, porcentagem, comecou_leitura, terminou_leitura, nota)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            # Executa a consulta passando os novos parâmetros
            cursor.execute(
                query,
                (
                    estante_id,
                    livro_id,
                    porcentagem,
                    comecou_leitura,
                    terminou_leitura,
                    nota,
                ),
            )

            # Confirma a transação
            self.connection.commit()
            cursor.close()

            # Mensagem de sucesso no log
            logger.info(
                f"Livro {livro_id} adicionado à estante {estante_id} com sucesso com progresso {porcentagem}%, nota {nota}!"
            )

        except mysql.connector.Error as err:
            # Mensagem de erro no log em caso de falha
            logger.error(f"Erro ao adicionar livro à estante: {err}")

    def get_user_shelves(self, user_id):
        """
        Retorna todas as estantes de um usuário.
        """
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM EstanteUsuario WHERE usuario_id = %s", (user_id,))
        shelves = cursor.fetchall()
        cursor.close()
        return shelves

    def get_books_in_shelf(self, estante_id):
        """
        Retorna todos os livros de uma estante específica.
        """
        cursor = self.connection.cursor(dictionary=True)
        query = """
            SELECT l.bookID, l.title, l.isbn FROM Livros l
            JOIN EstanteLivros el ON l.bookID = el.livro_id
            WHERE el.estante_id = %s
        """
        cursor.execute(query, (estante_id,))
        books = cursor.fetchall()
        cursor.close()
        return books

    def get_user_current_readings(self, user_id):
        """
        Retorna os livros que o usuário está lendo (progresso entre 0 e 100%).
        """
        cursor = self.connection.cursor(dictionary=True)

        query = """
        SELECT Livros.title, Livros.authors, Livros.isbn, EstanteLivros.porcentagem
        FROM Livros
        INNER JOIN EstanteLivros ON Livros.bookID = EstanteLivros.livro_id
        INNER JOIN EstanteUsuario ON EstanteLivros.estante_id = EstanteUsuario.estante_id
        WHERE EstanteUsuario.usuario_id = %s
        ORDER BY EstanteLivros.porcentagem DESC
        """
        cursor.execute(query, (user_id,))
        books = cursor.fetchall()
        cursor.close()
        return books


# Exemplo de uso
if __name__ == "__main__":
    livro_manager = Livro()

    # Busca um livro aleatório
    random_books = livro_manager.search_random_books()
    for book in random_books:
        print(book)

    # Busca um livro específico pelo ID
    book_id_to_search = 1  # Exemplo de ID
    book_details = livro_manager.get_book_by_id(book_id_to_search)
    if book_details:
        print("\nDetalhes do livro encontrado:")
        print(book_details)
    else:
        print("\nLivro não encontrado.")
