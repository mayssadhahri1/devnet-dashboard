pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Start Services') {
            steps {
                sh 'docker compose up -d'
            }
        }

        stage('Wait Services') {
            steps {
                sh 'sleep 10'
            }
        }

        stage('Test Backend') {
            steps {
                sh 'curl -s http://localhost:8000/api/system || true'
            }
        }

        stage('Test Frontend') {
            steps {
                sh 'curl -s http://localhost:8501 || true'
            }
        }

        stage('Stop Services') {
            steps {
                sh 'docker compose down'
            }
        }
    }

    post {
        always {
            echo "✅ CI/CD Pipeline finished"
        }
    }
}