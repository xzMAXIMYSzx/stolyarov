stage('Setup') {
    steps {
        echo 'Установка зависимостей...'
        bat '''
            chcp 65001
            set PYTHONIOENCODING=utf-8
            set PYTHONUTF8=1
            "C:\\python\\python.exe" -m pip install --upgrade pip
            "C:\\python\\python.exe" -m pip install -r requirements.txt
        '''
    }
}

stage('Run Tests') {
    steps {
        echo 'Запуск тестов...'
        bat '''
            chcp 65001
            set PYTHONIOENCODING=utf-8
            set PYTHONUTF8=1
            "C:\\python\\python.exe" -m pytest test_shoporg.py -v --junitxml=test-results.xml
        '''
    }
    post {
        always {
            junit 'test-results.xml'
        }
    }
}
