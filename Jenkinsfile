pipeline {
    agent {
        docker { image 'python:3.8-slim-buster' }
    }
    stages {
        stage('test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pip install -r requirements_test.txt'
                sh 'pytest'
            }
        }
    }
}