pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                // Original: checkout from main branch
                git branch: 'main', url: 'https://github.com/rinkugupta3/Playwright_Automation_Azure_BDD_MultipleAppleSearch'
            }
        }

        stage('Set up Virtual Environment') {
            steps {
                bat '''
                    if not exist venv (
                        C:\\Users\\dhira\\AppData\\Local\\Programs\\Python\\Python311\\python.exe -m venv venv
                    )
                '''
            }
        }

        stage('Set up Python environment') {
            steps {
                // Original: upgrade pip
                bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pip install --upgrade pip"
                // Original: install requirements
                bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pip install -r requirements.txt"
                // Original: install pytest-html (fixed typo: pytest.html -> pytest-html)
                bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pip install pytest-html"

                // New: upgrade pip inside venv
                bat 'venv\\Scripts\\python.exe -m pip install --upgrade pip'
                // New: install requirements inside venv
                bat 'venv\\Scripts\\python.exe -m pip install -r requirements.txt'
                // New: install pytest-html inside venv
                bat 'venv\\Scripts\\python.exe -m pip install pytest-html'
            }
        }

        stage('Install Playwright Browsers') {
            steps {
                // Original: install all browsers using global python
                bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m playwright install"
                // New: install chromium inside venv
                bat 'venv\\Scripts\\python.exe -m playwright install chromium'
            }
        }

        stage('main Playwright BDD Tests') {
            steps {
                // Original (commented out - was using global python)
                // bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pytest --html=report_playwright_bdd.html"

                // New: run tests using venv python (avoids langsmith conflict)
                bat 'venv\\Scripts\\python.exe -m pytest'
                bat 'venv\\Scripts\\python.exe -m pytest --html=report_playwright_bdd.html'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            // Original: fixed typo (report_playwright_bdd.html.html -> report_playwright_bdd.html)
            archiveArtifacts artifacts: 'report_playwright_bdd.html, screenshots/**/*', allowEmptyArchive: true
            publishHTML(target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'report_playwright_bdd.html',
                reportName: 'Playwright BDD Test Report'
            ])
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}