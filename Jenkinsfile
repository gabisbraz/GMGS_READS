pipeline {
  agent any
  stages {
    stage ('Install Python and Pip') {
      steps {
        sh '''
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip'
        '''
      }
    }
    stage('Install dependecies') {
      steps {
        sh 'pip install --user -r requirements.txt'
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
