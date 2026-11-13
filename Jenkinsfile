
pipeline {
    agent any

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                echo 'Source code downloaded'
            }
        }

        stage('Build and Push Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DH_USER',
                        passwordVariable: 'DH_TOKEN'
                    )
                ]) {
                    sh '''
                        docker build -t "$DH_USER/devops-flask:${BUILD_NUMBER}" .

                        echo "$DH_TOKEN" | docker login \
                            -u "$DH_USER" --password-stdin

                        docker push "$DH_USER/devops-flask:${BUILD_NUMBER}"
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DH_USER',
                        passwordVariable: 'DH_TOKEN'
                    )
                ]) {
                    sh '''
                        sed "s|devops-flask:1.0|$DH_USER/devops-flask:${BUILD_NUMBER}|g" \
                            k8s/deployment.yaml | kubectl apply -f -

                        kubectl apply -f k8s/service.yaml

                        kubectl rollout status deployment/flask-deployment
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Continuous deployment completed successfully!'
        }

        failure {
            echo 'Continuous deployment failed!'
        }

        always {
            echo 'CI/CD pipeline execution completed.'
        }
    }
}
