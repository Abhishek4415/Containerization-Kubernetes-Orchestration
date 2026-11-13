

pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'abhishek4410/devops-flask'
        IMAGE_TAG = "${BUILD_NUMBER}"

        // Kubernetes configuration exported from Ubuntu WSL2
        KUBECONFIG = 'C:/Users/Public/minikube-wsl-kubeconfig.yaml'
    }

    options {
        skipDefaultCheckout(true)
    }

    stages {

        // 1. Checkout source code from GitHub
        stage('Checkout') {
            steps {
                checkout scm
                echo 'Source code downloaded successfully.'
            }
        }

        // 2. Build Docker image and push to Docker Hub
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
                        set -e

                        echo "Building Docker image..."

                        docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} .

                        echo "Logging in to Docker Hub..."

                        printf '%s' "$DH_TOKEN" | docker login \
                            -u "$DH_USER" \
                            --password-stdin

                        echo "Pushing Docker image..."

                        docker push ${DOCKER_IMAGE}:${IMAGE_TAG}

                        docker logout
                    '''
                }
            }
        }

        // 3. Verify Kubernetes connection
        stage('Verify Kubernetes Connection') {
            steps {
                sh '''
                    set -e

                    echo "Checking Kubernetes context..."

                    kubectl config current-context

                    echo "Checking Kubernetes nodes..."

                    kubectl get nodes

                    echo "Kubernetes connection successful."
                '''
            }
        }

        // 4. Deploy application to Kubernetes
        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    set -e

                    echo "Deploying application..."

                    echo "Applying Kubernetes Deployment..."

                    sed "s|devops-flask:1.0|${DOCKER_IMAGE}:${IMAGE_TAG}|g" \
                        k8s/deployment.yaml | kubectl apply -f -

                    echo "Applying Kubernetes Service..."

                    kubectl apply -f k8s/service.yaml

                    echo "Waiting for deployment rollout..."

                    kubectl rollout status deployment/flask-deployment \
                        --timeout=180s

                    echo "Application deployed successfully."
                '''
            }
        }

        // 5. Verify final deployment
        stage('Verify Deployment') {
            steps {
                sh '''
                    echo "Checking deployments..."

                    kubectl get deployments

                    echo "Checking pods..."

                    kubectl get pods -o wide

                    echo "Checking services..."

                    kubectl get services
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: CI/CD pipeline completed successfully!'
            echo 'Docker image built, pushed and deployed to Kubernetes.'
        }

        failure {
            echo 'FAILED: CI/CD pipeline execution failed.'
            echo 'Check the Jenkins Console Output for details.'
        }

        always {
            echo 'Jenkins pipeline execution completed.'
        }
    }
}
