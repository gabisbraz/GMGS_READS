pipeline {
  agent any
  stages {
    stage('Install pip') {
      steps {
        // Baixa o instalador do pip e o executa
        sh 'curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py'
        sh 'python3 get-pip.py --user'  // Instala o pip apenas para o usuário
      }
    }
    stage('Install dependencies') {
      steps {
        // Instala as dependências usando o pip instalado
        sh '~/.local/bin/pip3 install --user -r requirements.txt'
      }
    }
    stage('version') {
      steps {
        sh 'python3 --version'
      }
    }
    stage('hello') {
      steps {
        sh 'python3 app/test/test_usuario.py'
      }
    }
  }
}
