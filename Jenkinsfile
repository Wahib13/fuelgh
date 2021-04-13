pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                cd cd_scripts
                bat 'build_script.bat'
            }
        }
    }
}