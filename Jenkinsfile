pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Run') {
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