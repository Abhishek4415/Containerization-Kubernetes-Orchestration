# Lab 2: Containerization & Kubernetes Orchestration

## 1. Overview

This lab focuses on containerization, Docker image and container management, persistent storage, container networking, and Kubernetes orchestration.

A Python Flask application is containerized using Docker and deployed on a local Kubernetes cluster using Minikube. Docker Compose is used to manage multiple containers, while Jenkins is integrated to automate the continuous deployment workflow.

## 2. Objectives

- Containerize a sample Python application using Docker.
- Build, run, tag, and manage Docker images and containers.
- Use Docker Compose for multi-container applications.
- Demonstrate Docker volumes and bind mounts.
- Configure Docker networking and container communication.
- Deploy applications on Kubernetes using Minikube.
- Implement Kubernetes Deployments and Services.
- Demonstrate scaling, rolling updates, and rollbacks.
- Configure continuous deployment using Jenkins.
- Document commands, configurations, screenshots, and observations.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Windows 11 | Host Operating System |
| WSL2 | Linux environment on Windows |
| Ubuntu 24.04 | Operating System |
| Docker Desktop | Containerization platform |
| Docker Compose | Multi-container management |
| Docker Hub | Docker image registry |
| Python 3.12 | Application development |
| Flask | Python web framework |
| Redis | In-memory data store |
| Kubernetes | Container orchestration |
| Minikube | Local Kubernetes cluster |
| kubectl | Kubernetes command-line tool |
| Jenkins | CI/CD automation |

## 4. Project Structure

```text
lab2-containerization/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── docker-compose.yml
├── Jenkinsfile
├── README.md
│
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
│
├── data/
│
└── documentation/
    ├── commands.txt
    ├── observations.txt
    ├── docker-details.txt
    ├── kubernetes-details.txt
    │
    └── screenshots/
```

## 5. Application Description

A Python Flask web application is developed to demonstrate Docker containerization and Kubernetes deployment.

### Application Features

- Displays a welcome message.
- Shows the application version.
- Provides a health-check endpoint.
- Supports Redis connectivity through a cache endpoint.

### Application Endpoints

| Endpoint | Description |
|---|---|
| `/` | Displays the application homepage |
| `/health` | Checks application health |
| `/cache` | Tests Redis connectivity and increments a visit counter |

### requirements.txt

```text
Flask>=3.0,<4.0
redis>=5.0,<7.0
```

## 6. Experiments Performed

### Experiment 1: Containerize a Sample Application Using Docker

**Objective:** Create a Dockerfile, build a Docker image, run a container, and understand image layers and container behaviour.

**Dockerfile:**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

**Important commands:**

```bash
docker build -t devops-flask:1.0 .
docker images

docker run -d --name devops-container \
-p 5000:5000 devops-flask:1.0

docker ps
docker history devops-flask:1.0
docker logs devops-container

docker stop devops-container
docker start devops-container
docker rm devops-container
```

### Experiment 2: Manage Docker Containers and Images

**Objective:** Manage Docker containers and images, push images to Docker Hub, and configure multi-container applications using Docker Compose.

**Important commands:**

```bash
docker ps
docker ps -a
docker images

docker stop my-container
docker start my-container
docker restart my-container
docker rm my-container

docker tag devops-flask:1.0 YOUR_USERNAME/devops-flask:1.0

docker login
docker push YOUR_USERNAME/devops-flask:1.0

docker compose up -d --build
docker compose ps
docker compose logs
docker compose down
```

**Docker Compose services:**

1. Flask web application.
2. Redis service.

Docker Compose allows both services to run together and communicate using service names.

### Experiment 3: Docker Storage

**Objective:** Demonstrate temporary container-layer data loss and permanent storage using Docker named volumes and bind mounts.

**Storage concepts:**

- Container writable layer: Data associated with a container that is lost when the container is deleted.
- Named volume: Persistent storage managed by Docker.
- Bind mount: Maps a host directory into a container.

**Important commands:**

```bash
docker volume create lab2-data

docker volume ls

docker run --name volume-demo \
-v lab2-data:/data alpine \
sh -c 'echo "Permanent data" > /data/record.txt'

docker rm volume-demo

docker run --rm -v lab2-data:/data \
alpine cat /data/record.txt
```

**Bind mount example:**

```bash
mkdir -p data

echo "Permanent data using bind mount" > data/record.txt

docker run --rm \
-v "$PWD/data:/data" \
alpine cat /data/record.txt
```

### Experiment 4: Docker Networking

**Objective:** Demonstrate communication between two containers using a Docker network, container names, and IP addresses.

**Important commands:**

```bash
docker network create lab2-network

docker network ls

docker run -d --name web-server \
--network lab2-network nginx:alpine

docker run -it --name client-container \
--network lab2-network busybox sh
```

**Communication using container name:**

```bash
wget -qO- http://web-server
```

**Find container IP:**

```bash
docker inspect -f \
'{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web-server
```

**Communication using container IP:**

```bash
wget -qO- http://CONTAINER_IP
```

### Experiment 5: Deploy an Application to Kubernetes

**Objective:** Deploy the Flask application on a Kubernetes cluster using Minikube, Deployment, and Service manifests.

**Important commands:**

```bash
minikube start --driver=docker

minikube status

kubectl get nodes
kubectl get pods -A

minikube image load devops-flask:1.0

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

kubectl get pods
kubectl get deployments
kubectl get services

kubectl describe deployment flask-deployment
```

**Kubernetes resources:**

- Deployment: Maintains the desired number of application Pods.
- Pod: Runs the application container.
- Service: Provides a stable network endpoint to access application Pods.

### Experiment 6: Implement Kubernetes Deployment Strategies

**Objective:** Demonstrate scaling, rolling updates, and rollbacks using Kubernetes Deployment.

**Scaling:**

```bash
kubectl scale deployment flask-deployment --replicas=3

kubectl get pods

kubectl scale deployment flask-deployment --replicas=5

kubectl get deployments

kubectl scale deployment flask-deployment --replicas=2
```

**Rolling update:**

```bash
docker build -t devops-flask:2.0 .

minikube image load devops-flask:2.0

kubectl set image deployment/flask-deployment \
flask-app=devops-flask:2.0

kubectl rollout status deployment/flask-deployment
```

**Check rollout history:**

```bash
kubectl rollout history deployment/flask-deployment
```

**Rollback:**

```bash
kubectl rollout undo deployment/flask-deployment

kubectl rollout status deployment/flask-deployment

kubectl describe deployment flask-deployment
```

### Experiment 7: Configure Continuous Deployment

**Objective:** Integrate Jenkins with Docker Hub and Kubernetes to automate application deployment.

**Workflow:**

1. Developer pushes source code to GitHub.
2. Jenkins retrieves the latest source code.
3. Jenkins builds a Docker image.
4. Jenkins pushes the image to Docker Hub.
5. Jenkins applies Kubernetes Deployment and Service manifests.
6. Kubernetes updates the application Pods.

**Jenkins pipeline stages:**

| Stage | Description |
|---|---|
| Checkout | Retrieves application source code from GitHub |
| Build and Push Image | Builds and pushes the Docker image to Docker Hub |
| Deploy to Kubernetes | Applies Kubernetes manifests and verifies rollout |

**Important commands:**

```bash
git add .
git commit -m "Update application"
git push origin main

kubectl get pods
kubectl get deployments
kubectl get services
```

The Jenkinsfile contains the pipeline configuration and automates the Docker image build, registry push, and Kubernetes deployment.

## 7. Kubernetes Configuration

### Deployment Configuration

File: `k8s/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: flask-deployment

spec:
  replicas: 2

  selector:
    matchLabels:
      app: flask-app

  template:
    metadata:
      labels:
        app: flask-app

    spec:
      containers:
        - name: flask-app
          image: devops-flask:1.0
          imagePullPolicy: IfNotPresent

          ports:
            - containerPort: 5000

          env:
            - name: APP_VERSION
              value: "1.0"
```

### Service Configuration

File: `k8s/service.yaml`

```yaml
apiVersion: v1
kind: Service

metadata:
  name: flask-service

spec:
  type: NodePort

  selector:
    app: flask-app

  ports:
    - port: 5000
      targetPort: 5000
      nodePort: 30080
      protocol: TCP
```

## 8. CI/CD Workflow Architecture

```text
Developer
    |
    v
Git Repository
    |
    v
GitHub
    |
    v
Jenkins Pipeline
    |
    v
Docker Image Build
    |
    v
Docker Hub Registry
    |
    v
Kubernetes / Minikube
    |
    v
Deployment
    |
    v
Application Pods
    |
    v
Kubernetes Service
    |
    v
Running Application
```

## 9. Deployment Strategy

The application deployment uses the following Kubernetes strategies:

| Strategy | Description |
|---|---|
| Scaling | Changes the number of application replicas |
| Rolling Update | Gradually replaces old application Pods with new Pods |
| Rollback | Restores a previous Deployment revision |
| Service | Provides a stable endpoint for application access |

## 10. Expected Results

The following results are expected after successful execution:

- Docker image is successfully built.
- Flask application runs inside a Docker container.
- Docker containers and images are managed successfully.
- Docker image is pushed to Docker Hub.
- Docker Compose runs Flask and Redis services.
- Container-layer data loss is demonstrated.
- Named volumes and bind mounts preserve data.
- Two containers communicate through a Docker network.
- Application is deployed on Minikube.
- Kubernetes Pods reach the Running state.
- Application replicas are scaled successfully.
- Rolling updates and rollbacks are demonstrated.
- Jenkins automates Docker image building and Kubernetes deployment.

## 11. Observations

The practical experiments demonstrate the advantages of containerization and orchestration.

Docker provides a consistent environment for running applications, while Docker Compose simplifies the management of multiple containers.

Docker volumes and bind mounts provide persistent data storage, and Docker networking enables communication between containers.

Kubernetes manages application Pods and supports scaling, rolling updates, and rollbacks. Jenkins automates the continuous deployment workflow by integrating GitHub, Docker Hub, and Kubernetes.

## 12. Conclusion

Successfully performed the Containerization and Kubernetes Orchestration lab using Docker, Docker Compose, Docker Hub, Kubernetes, Minikube, and Jenkins.

The practical exercises provided hands-on experience with Docker image creation, container lifecycle management, persistent storage, container networking, Kubernetes deployments, application scaling, rolling updates, rollbacks, and continuous deployment.

## 13. References

- Docker Documentation: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- Docker Storage: https://docs.docker.com/engine/storage/
- Docker Networking: https://docs.docker.com/engine/network/
- Docker Hub: https://hub.docker.com/
- Kubernetes Documentation: https://kubernetes.io/docs/
- Minikube Documentation: https://minikube.sigs.k8s.io/docs/
- Jenkins Documentation: https://www.jenkins.io/doc/
- Flask Documentation: https://flask.palletsprojects.com/
- Redis Documentation: https://redis.io/docs/
