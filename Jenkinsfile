pipeline {
    agent any

    environment {
        BACKEND_URL = "http://localhost:8000"
        FRONTEND_URL = "http://localhost:8501"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "📥 Cloning repository..."
                git branch: 'main',
                    url: 'https://github.com/mayssadhahri1/devnet-dashboard.git'
            }
        }

        stage('Info') {
            steps {
                sh 'echo 🚀 DevNet CI/CD Pipeline Started'
            }
        }

        stage('List Project Files') {
            steps {
                sh 'ls -la'
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
                sh 'sleep 15'
            }
        }

        stage('Test Backend') {
            steps {
                sh '''
                echo "🔎 Testing Backend..."
                curl -s $BACKEND_URL/api/system || echo "❌ Backend not responding"
                '''
            }
        }

        stage('Test Frontend') {
            steps {
                sh '''
                echo "🔎 Testing Frontend..."
                curl -s $FRONTEND_URL || echo "❌ Frontend not responding"
                '''
            }
        }

        stage('Stop Services') {
            steps {
                sh 'docker compose down'
            }
        }
    }

    post {
        success {
            echo "✅ CI/CD PIPELINE SUCCESS"
        }
        failure {
            echo "❌ CI/CD PIPELINE FAILED"
        }
        always {
            echo "🏁 Pipeline finished"
        }
    }
}