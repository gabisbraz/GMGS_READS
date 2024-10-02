pipeline {
  agent any
  stages {
    stage('Setup Python Virtual Environment') {
      steps {
        sh 'python3 -m venv venv'  // Cria o ambiente virtual
        sh '. venv/bin/activate'   // Ativa o ambiente virtual
      }
    }
    stage('Install dependencies') {
      steps {
        sh './venv/bin/pip install -r requirements.txt'  // Instala dependências no ambiente virtual
      }
    }
    stage('version') {
      steps {
        sh './venv/bin/python --version'  // Verifica a versão do Python no ambiente virtual
      }
    }
    stage('Run Tests') {
      steps {
        sh './venv/bin/python app/test/test_usuario.py'  // Executa os testes
      }
    }
  }
}
