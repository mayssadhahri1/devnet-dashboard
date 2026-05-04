pipeline {
    agent {
        label 'built-in'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Info') {
            steps {
                sh 'echo "🚀 DevNet CI/CD Running"'
            }
        }

        stage('Build Docker') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Run Containers') {
            steps {
                sh 'docker compose up -d'
            }
        }

        stage('Test Backend') {
            steps {
                sh 'curl http://host.docker.internal:8000/api/system'
            }
        }

        stage('Test Frontend') {
            steps {
                sh 'curl http://host.docker.internal:8501'
            }
        }

        stage('Stop') {
            steps {
                sh 'docker compose down'
            }
        }
    }
}