pipeline {
  agent any
  stages {
    stage('Install pip3') {
      steps {
        sh 'apt-get update && apt-get install -y python3-pip'
      }
    }
    stage('Install dependencies') {
      steps {
        sh 'pip3 install -r requirements.txt'
      }
    }
    stage('version') {
      steps {
        sh 'python3 --version'
      }
    }
    stage('Run Tests') {
      steps {
        sh 'python3 app/test/test_usuario.py'
      }
    }
  }
}
