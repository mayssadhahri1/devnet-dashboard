pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Info') {
            steps {
                sh 'echo DevNet CI/CD Running'
            }
        }

        stage('Test Backend') {
            steps {
                sh 'curl http://localhost:8000/api/system || true'
            }
        }

        stage('Test Frontend') {
            steps {
                sh 'curl http://localhost:8501 || true'
            }
        }
    }
}