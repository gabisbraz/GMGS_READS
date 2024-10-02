pipeline {
  agent any
  stages {
    stage('Install pip3') {
      steps {
        // Atualiza os pacotes e instala o pip
        sh 'sudo apt-get update && sudo apt-get install -y python3-pip'
      }
    }

    stage('Install dependencies') {
      steps {
        // Instala as dependências do projeto
        sh 'pip3 install -r requirements.txt'
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
