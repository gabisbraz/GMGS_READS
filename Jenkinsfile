pipeline {
  agent any
  stages {
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
    stage('Install dependencies') {
      steps {
        sh 'pip3 install -r requirements.txt'
      }
    }
  }
}
