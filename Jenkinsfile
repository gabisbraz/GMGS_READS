pipeline {
  agent any
  stages {
    stage ('Instalar dependências') {
      steps {
        script {
          sh '''
          pip install --no-cache-dir -r requirements.txt
          '''
        }
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
