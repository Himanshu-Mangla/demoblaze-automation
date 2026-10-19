
pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('Check Python') {
            steps {
                bat '"C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                bat '"C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pip install -r requirements.txt'
                bat '"C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m playwright install chromium'
            }
        }

        stage('Run Tests') {
            steps {
                withCredentials([
                    string(credentialsId: 'VALID_USERNAME', variable: 'VALID_USERNAME'),
                    string(credentialsId: 'VALID_PASSWORD', variable: 'VALID_PASSWORD'),
                    string(credentialsId: 'INVALID_USERNAME', variable: 'INVALID_USERNAME'),
                    string(credentialsId: 'INVALID_PASSWORD', variable: 'INVALID_PASSWORD')
                ]) {
                    bat '"C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pytest -v'
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
        }
        success {
            echo 'All tests passed successfully!'
        }
        failure {
            echo 'Build failed. Please check the Console Output.'
        }
    }
}
