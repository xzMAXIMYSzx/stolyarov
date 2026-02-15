pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Клонирование репозитория...'
                checkout scm
            }
        }
        
        stage('Setup') {
            steps {
                echo 'Установка зависимостей...'
                bat 'C:\\Users\\MAXIMUS\\AppData\\Local\\Programs\\Python\\Python313\\python.exe -m pip install --upgrade pip'
                bat 'C:\\Users\\MAXIMUS\\AppData\\Local\\Programs\\Python\\Python313\\python.exe -m pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Запуск тестов...'
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
            echo '✅ Все тесты прошли успешно!'
        }
        failure {
            echo '❌ Тесты упали!'
        }
    }
}
