pipeline {
    agent any

    environment {
        HEADLESS = 'true'  // Run tests in headless mode
        PYTHON_VERSION = '3.11' // Specify the desired Python version
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout from the specified branch
                git branch: 'main', url: 'https://github.com/rinkugupta3/Playwright_Automation_Azure_BDD_MultipleAppleSearch'
            }
        }

        stage('Set up Python environment') {
            steps {
                script {
                    // Install Python dependencies
                    sh "python3 -m pip install --upgrade pip"
                    sh "python3 -m pip install -r requirements.txt"
                    sh "python3 -m pip install pytest-html"
                }
            }
        }

        stage('Create Pip Cache Directory') {
            steps {
                script {
                    // Create a cache directory for Python packages if it doesn't exist
                    sh "mkdir -p .pip_cache || echo 'Cache directory already exists'"
                }
            }
        }

        stage('Install Playwright Browsers') {
            steps {
                script {
                    // Install Playwright browsers along with required dependencies
                    sh "python3 -m playwright install --with-deps"
                }
            }
        }

        stage('Run Playwright BDD Tests') {
            steps {
                script {
                    // Run Playwright BDD tests in headless mode
                    sh "HEADLESS=true python3 -m pytest --html=report_playwright_bdd.html --maxfail=3 --disable-warnings -v"
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            // Archive both the report and screenshots
            archiveArtifacts artifacts: 'report_playwright_bdd.html, screenshots/**/*', allowEmptyArchive: true
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
