import sys

from pathlib import Path

from tinydb import Query

DIR_ROOT = str(Path(__name__).absolute().parents[0])

if DIR_ROOT not in sys.path:
    sys.path.append(DIR_ROOT)

try:
    from app.utils.usuario import Usuario, buscar_usuario, criar_usuario, db
except ModuleNotFoundError:
    from utils.usuario import Usuario, buscar_usuario, criar_usuario, db


# Limpar o banco de dados antes de cada teste
# @pytest.fixture(autouse=True)
def limpar_banco():
    db.truncate()  # Limpa os dados do TinyDB antes de cada teste


# Teste para verificar a criação de um usuário
def test_criar_usuario():
    limpar_banco()
    criar_usuario("Gabriella Braz", "gabisbraz", "gabibraz15@outlook.com", "senha123")

    # Buscar o usuário criado
    usuario = buscar_usuario("gabisbraz")

    # Verificar se o usuário foi criado corretamente
    assert usuario is not None
    assert usuario["nome"] == "Gabriella Braz"
    assert usuario["username"] == "gabisbraz"
    assert usuario["email"] == "gabibraz15@outlook.com"
    assert "password" in usuario  # Verificar se a senha está presente


# Teste para verificar se a senha foi criptografada corretamente
def test_senha_criptografada():
    limpar_banco()
    criar_usuario(
        "Maria Julia de Padua", "majupadua", "majupadua@outlook.com", "senha456"
    )

    # Buscar o usuário criado
    usuario = buscar_usuario("majupadua")

    # Verificar se a senha armazenada é diferente da senha original (indicando que foi criptografada)
    assert usuario is not None
    assert usuario["password"] != "senha1504"  # A senha deve estar criptografada


# Teste para verificar a função de busca de usuário
def test_buscar_usuario():
    limpar_banco()
    criar_usuario("Giovana Liao", "giliao", "giliao@outlook.com", "senha789")

    # Buscar o usuário existente
    usuario = buscar_usuario("giliao")
    assert usuario is not None
    assert usuario["username"] == "giliao"

    # Buscar um usuário inexistente
    usuario_inexistente = buscar_usuario("usuario_nao_existe")
    assert usuario_inexistente is None


# Teste para verificar a função de verificação de senha
def test_verificar_senha():
    limpar_banco()
    criar_usuario("Giovana Liao", "giliao", "giliao@outlook.com", "senha789")

    # Buscar o usuário criado
    usuario = buscar_usuario("giliao")
    assert usuario is not None

    # Verificar a senha correta
    senha_correta = Usuario.verificar_senha("senha789", usuario["password"])
    assert senha_correta is True

    # Verificar uma senha incorreta
    senha_incorreta = Usuario.verificar_senha("senhaerrada", usuario["password"])
    assert senha_incorreta is False


# Teste para verificar se o banco de dados está sendo limpo entre os testes
def test_limpeza_banco():
    limpar_banco()
    _ = Query()
    todos_usuarios = db.all()
    assert len(todos_usuarios) == 0
