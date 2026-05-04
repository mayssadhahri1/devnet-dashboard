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
                sh 'echo "🚀 DevNet CI/CD Pipeline Running"'
            }
        }

        stage('Validate Backend (optional)') {
            steps {
                sh '''
                    echo "Checking backend availability..."
                    curl -s http://localhost:8000/api/system || echo "Backend not running (expected if not started)"
                '''
            }
        }

        stage('Validate Frontend (optional)') {
            steps {
                sh '''
                    echo "Checking frontend availability..."
                    curl -s http://localhost:8501 || echo "Frontend not running (expected if not started)"
                '''
            }
        }
    }

    post {
        always {
            echo "✅ Pipeline finished"
        }
    }
}