
pipeline {
    agent any

    triggers {
        // Run every day at 12:00 PM (noon), India time
        cron('H 12 * * *')
    }

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
            echo 'Pipeline execution completed. Sending QA email...'

            script {
                def status = currentBuild.currentResult ?: 'UNKNOWN'

                def emailBody = """
                <html>
                <body>
                    <h2>Daily Playwright QA Report</h2>
                    <p><b>Project:</b> ${env.JOB_NAME}</p>
                    <p><b>Build Number:</b> #${env.BUILD_NUMBER}</p>
                    <p><b>Build Status:</b> ${status}</p>
                    <p><b>Build Date:</b> ${new Date()}</p>
                    <p><b>Tests:</b> Check the attached HTML report and console output.</p>
                    <p><b>Jenkins Build:</b>
                    <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                    <p>Regards,<br>QA Team</p>
                </body>
                </html>
                """

                try {
                    emailext(
                        to: 'himanshumangla6@gmail.com, atesting339@gmail.com',
                        subject: "Daily QA Report - ${env.JOB_NAME} - Build #${env.BUILD_NUMBER} - ${status}",
                        mimeType: 'text/html',
                        body: emailBody,
                        attachmentsPattern: 'reports/**/daily-qa-report.html'
                    )

                    echo 'Email extension step completed without throwing an error.'
                } catch (Exception e) {
                    echo "Email notification failed: ${e.getMessage()}"
                }
            }
        }

        success {
            echo 'All tests passed successfully!'
        }

        failure {
            echo 'Build failed. Please check the Console Output.'
        }
    }
}