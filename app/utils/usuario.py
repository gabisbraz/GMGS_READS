import bcrypt
from tinydb import TinyDB, Query
from loguru import logger

# Banco de dados (TinyDB)
db = TinyDB("usuarios.json")


class Usuario:
    def __init__(self, nome, username, email, password):
        self.nome = nome
        self.username = username
        self.email = email
        self.password = self.criptografar_senha(password)

    # Método para criptografar a senha
    def criptografar_senha(self, senha):
        # Gerar o salt para a criptografia
        salt = bcrypt.gensalt()
        # Retornar a senha criptografada
        return bcrypt.hashpw(senha.encode("utf-8"), salt)

    # Método para salvar o usuário no banco de dados
    def salvar(self):
        db.insert(
            {
                "nome": self.nome,
                "username": self.username,
                "email": self.email,
                "password": self.password.decode(
                    "utf-8"
                ),  # Decodificar para salvar como string
            }
        )

    # Método estático para verificar a senha
    @staticmethod
    def verificar_senha(password_digitada, password_armazenada):
        return bcrypt.checkpw(
            password_digitada.encode("utf-8"), password_armazenada.encode("utf-8")
        )


# Função para criar e armazenar um novo usuário
def criar_usuario(nome, username, email, password):
    novo_usuario = Usuario(nome, username, email, password)
    novo_usuario.salvar()
    logger.info(f"Usuário {nome} criado com sucesso!")


# Função para buscar um usuário por username
def buscar_usuario(username):
    UsuarioQuery = Query()
    usuario = db.search(UsuarioQuery.username == username)
    if usuario:
        return usuario[0]  # Retorna o primeiro usuário encontrado
    return None


# Exemplo de uso
if __name__ == "__main__":
    # Criar um novo usuário
    criar_usuario("Gabriella Braz", "gabisbraz", "gabibraz15@outlook.com", "senha123")

    # Buscar o usuário pelo username
    usuario_encontrado = buscar_usuario("gabisbraz")
    if usuario_encontrado:
        logger.info(f"Usuário encontrado: {usuario_encontrado}")
        # Verificar a senha
        senha_correta = Usuario.verificar_senha(
            "senha123", usuario_encontrado["password"]
        )
        logger.info("Senha correta!" if senha_correta else "Senha incorreta!")
    else:
        logger.info("Usuário não encontrado.")
