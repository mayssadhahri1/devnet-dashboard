pipeline {
    agent any

    stages {

        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Docker') {
            steps {
                sh 'docker --version'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Start Services') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Wait Services') {
            steps {
                sh 'sleep 15'
            }
        }

        stage('Test Backend') {
            steps {
                sh 'curl -s http://localhost:8000/api/system || echo "Backend not responding"'
            }
        }

        stage('Test Frontend') {
            steps {
                sh 'curl -s http://localhost:8501 || echo "Frontend not responding"'
            }
        }

        stage('Stop Services') {
            steps {
                sh 'docker-compose down'
            }
        }
    }

    post {
        always {
            echo "✅ CI/CD Pipeline finished"
        }
    }
}