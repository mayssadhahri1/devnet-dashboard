pipeline {
    agent any

    stages {

        stage('Info') {
            steps {
                sh 'echo 🚀 DevNet CI/CD Running'
            }
        }

        stage('Build Docker') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Start Services') {
            steps {
                sh 'docker compose up -d'
            }
        }

        stage('Wait') {
            steps {
                sh 'sleep 15'
            }
        }

        stage('Test Backend') {
            steps {
                sh 'curl -s http://localhost:8000/api/system || echo "Backend down"'
            }
        }

        stage('Test Frontend') {
            steps {
                sh 'curl -s http://localhost:8501 || echo "Frontend down"'
            }
        }

        stage('Stop') {
            steps {
                sh 'docker compose down'
            }
        }
    }

    post {
        always {
            echo "✅ Pipeline finished"
        }
    }
}