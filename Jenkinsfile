pipeline {
    agent any

    environment {
        APP_REPO = 'https://github.com/MominaRizwan/Assignment3'
        TEST_REPO = 'https://github.com/MominaRizwan/Test-cases'
        TEST_IMAGE = 'gaming-ecommerce-tests'
    }

    stages {
        stage('Clean Existing Containers') {
            steps {
                echo '🧹 Cleaning old containers...'
                sh '''
                    docker-compose -p ecommerce_pipeline -f app/docker-compose.yml down || true
                    docker stop gaming-app || true
                    docker rm gaming-app || true
                '''
            }
        }

        stage('Checkout App Repository') {
            steps {
                dir('app') {
                    git branch: 'main', url: "${APP_REPO}"
                }
            }
        }

        stage('Start Application with Docker Compose') {
            steps {
                dir('app') {
                    echo '🐳 Starting app using docker-compose...'
                    sh 'docker-compose -p ecommerce_pipeline up -d --build --remove-orphans'

                    echo '⏳ Waiting for app to be ready...'
                    sh 'sleep 10'
                }
            }
        }

        stage('Checkout and Build Test Image') {
            steps {
                dir('tests') {
                    git branch: 'main', url: "${TEST_REPO}"
                    echo '🐳 Building test image...'
                    sh 'docker build -t ${TEST_IMAGE} .'
                }
            }
        }

        stage('Run Tests Against App') {
            steps {
                echo '🚀 Running tests against the app...'
                sh 'docker run --rm --network host ${TEST_IMAGE}'
            }
        }

        stage('Clean Up') {
            steps {
                echo '🧽 Cleaning up dangling images...'
                sh 'docker image prune -f'
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Please check logs above.'
        }
    }
}
