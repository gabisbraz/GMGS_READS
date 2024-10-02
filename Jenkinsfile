pipeline {
  agent {
    docker {
      image 'python:3.12-slim'  // Usa uma imagem Docker com Python 3.12 e pip pré-instalado
    }
  }
  
  stages {
    stage('Install dependencies') {
      steps {
        // Instala as dependências diretamente no ambiente Docker
        sh 'pip install -r requirements.txt'
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
