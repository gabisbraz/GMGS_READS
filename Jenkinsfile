pipeline {
  agent any
  stages {
    stage ('Instalar dependências') {
      steps {
        script {
          sh '''
          apt install python3.12-venv
          python3 -m venv venv 
          source venv/bin/activate
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
