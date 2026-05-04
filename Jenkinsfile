pipeline {
    agent any

    environment {
        BACKEND_URL = "http://localhost:8000"
        FRONTEND_URL = "http://localhost:8501"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "📥 Cloning GitHub repository..."
                git branch: 'main',
                    url: 'https://github.com/mayssadhahri1/devnet-dashboard.git'
            }
        }

        stage('Workspace Check') {
            steps {
                echo "📁 Listing project files..."
                sh 'ls -la'
            }
        }

        stage('Build Docker Images') {
            steps {
                echo "🐳 Building Docker images..."
                sh 'docker compose build'
            }
        }

        stage('Start Services') {
            steps {
                echo "🚀 Starting backend + frontend..."
                sh 'docker compose up -d'
            }
        }

        stage('Wait Services') {
            steps {
                echo "⏳ Waiting services to start..."
                sh 'sleep 15'
            }
        }

        stage('Test Backend') {
            steps {
                echo "🔎 Testing backend..."
                sh 'curl -s $BACKEND_URL/api/system || echo "❌ Backend not reachable"'
            }
        }

        stage('Test Frontend') {
            steps {
                echo "🔎 Testing frontend..."
                sh 'curl -s $FRONTEND_URL || echo "❌ Frontend not reachable"'
            }
        }

        stage('Stop Services') {
            steps {
                echo "🛑 Stopping containers..."
                sh 'docker compose down'
            }
        }
    }

    post {
        success {
            echo "✅ CI/CD SUCCESS - DevNet deployed correctly"
        }
        failure {
            echo "❌ CI/CD FAILED - check logs"
        }
        always {
            echo "🏁 Pipeline finished"
        }
    }
}