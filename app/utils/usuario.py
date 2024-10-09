import bcrypt
from tinydb import Query, TinyDB
from loguru import logger

db = TinyDB("usuarios.json")

class Usuario:
    """
    CLASSE QUE REPRESENTA UM USUÁRIO.

    A CLASSE CONTÉM MÉTODOS PARA CRIAR, SALVAR, E VERIFICAR SENHAS.
    """

    def __init__(self, nome: str, username: str, email: str, password: str):
        """
        INICIALIZA UM NOVO OBJETO 'USUARIO'.

        ARGUMENTOS:
        - nome: NOME DO USUÁRIO.
        - username: NOME DE USUÁRIO (LOGIN).
        - email: EMAIL DO USUÁRIO.
        - password: SENHA DO USUÁRIO (ANTES DA CRIPTOGRAFIA).
        """
        self.nome = nome
        self.username = username
        self.email = email
        self.password = self.criptografar_senha(password)

    # MÉTODO PARA CRIPTOGRAFAR A SENHA UTILIZANDO BCRYPT
    def criptografar_senha(self, senha: str) -> bytes:
        """
        CRIPTOGRAFA A SENHA UTILIZANDO O BCRYPT.

        ARGUMENTOS:
        - senha: A SENHA QUE SERÁ CRIPTOGRAFADA.

        RETORNA:
        - A SENHA CRIPTOGRAFADA COMO BYTES.
        """
        # GERA UM SALT ALEATÓRIO PARA A CRIPTOGRAFIA
        salt = bcrypt.gensalt()
        # RETORNA A SENHA CRIPTOGRAFADA
        return bcrypt.hashpw(senha.encode("utf-8"), salt)

    # MÉTODO PARA SALVAR O USUÁRIO NO BANCO DE DADOS
    def salvar(self) -> None:
        """
        SALVA O USUÁRIO NO BANCO DE DADOS TINYDB.
        """
        # INSERE OS DADOS DO USUÁRIO NO BANCO
        db.insert(
            {
                "nome": self.nome,
                "username": self.username,
                "email": self.email,
                "password": self.password.decode(
                    "utf-8"
                ),  # DECODIFICA PARA SALVAR COMO STRING
            }
        )

    # MÉTODO ESTÁTICO PARA VERIFICAR SE A SENHA DIGITADA É VÁLIDA
    @staticmethod
    def verificar_senha(password_digitada: str, password_armazenada: str) -> bool:
        """
        VERIFICA SE A SENHA DIGITADA É VÁLIDA EM RELAÇÃO À SENHA ARMAZENADA.

        ARGUMENTOS:
        - password_digitada: A SENHA DIGITADA PELO USUÁRIO.
        - password_armazenada: A SENHA ARMAZENADA CRIPTOGRAFADA.

        RETORNA:
        - BOOLEANO INDICANDO SE A SENHA ESTÁ CORRETA OU NÃO.
        """
        # COMPARA A SENHA DIGITADA COM A SENHA ARMAZENADA
        return bcrypt.checkpw(
            password_digitada.encode("utf-8"), password_armazenada.encode("utf-8")
        )


def criar_usuario(nome: str, username: str, email: str, password: str) -> None:
    """
    CRIA E SALVA UM NOVO USUÁRIO NO BANCO DE DADOS.

    ARGUMENTOS:
    - nome: NOME DO USUÁRIO.
    - username: NOME DE USUÁRIO (LOGIN).
    - email: EMAIL DO USUÁRIO.
    - password: SENHA DO USUÁRIO (ANTES DA CRIPTOGRAFIA).
    """
    novo_usuario = Usuario(nome, username, email, password)
    novo_usuario.salvar()
    logger.info(f"Usuário {nome} criado com sucesso!")


def buscar_usuario(username: str):
    """
    BUSCA UM USUÁRIO PELO NOME DE USUÁRIO (USERNAME).

    ARGUMENTOS:
    - username: NOME DE USUÁRIO PARA REALIZAR A BUSCA.

    RETORNA:
    - UM DICIONÁRIO COM OS DADOS DO USUÁRIO SE ENCONTRADO, CASO CONTRÁRIO, RETORNA 'None'.
    """
    UsuarioQuery = Query()
    usuario = db.search(UsuarioQuery.username == username)
    if usuario:
        return usuario[0]  # RETORNA O PRIMEIRO USUÁRIO ENCONTRADO
    return None


if __name__ == "__main__":
    # CRIAR UM NOVO USUÁRIO
    criar_usuario("Gabriella Braz", "gabisbraz", "gabibraz15@outlook.com", "senha123")
    criar_usuario("Giovana Liao", "giliao", "giovanaliao@gmail.com", "senha123")

    # BUSCAR O USUÁRIO PELO USERNAME
    usuario_encontrado = buscar_usuario("gabisbraz")
    if usuario_encontrado:
        logger.info(f"Usuário encontrado: {usuario_encontrado}")
        # VERIFICAR SE A SENHA ESTÁ CORRETA
        senha_correta = Usuario.verificar_senha(
            "senha123", usuario_encontrado["password"]
        )
        logger.info("Senha correta!" if senha_correta else "Senha incorreta!")
    else:
        logger.info("Usuário não encontrado.")

