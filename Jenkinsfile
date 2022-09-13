pipeline {
    agent { docker { image 'python:3.8-slim-buster' } }
    stages {
        stage('test') {
            steps {
                sh 'python --version'
                sh 'apt install -y --no-install-recommends postgresql-client postgresql-contrib libpq-dev build-essential pkg-config libxml2-dev libxmlsec1-dev libxmlsec1-openssl apache2 apache2-dev git'
                sh 'pip install -r requirements.txt'
                sh 'pip install -r requirements_test.txt'
                sh 'pytest'
            }
        }
    }
}