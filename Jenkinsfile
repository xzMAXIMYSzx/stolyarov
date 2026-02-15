pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Клонируем репозиторий...'
                checkout scm
            }
        }
        
        stage('Setup Python') {
            steps {
                echo 'Устанавливаем зависимости...'
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Запускаем тесты...'
                bat 'pytest test_shoporg.py -v --junitxml=test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }
        
        stage('Results') {
            steps {
                echo '✅ Тесты завершены!'
            }
        }
    }
    
    post {
        always {
            echo 'Сборка завершена'
        }
        success {
            echo '✅ Успех!'
        }
        failure {
            echo '❌ Ошибка!'
        }
    }
}
