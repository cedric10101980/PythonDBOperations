# Flask Application with Redis, Docker, and Kubernetes

This README provides a step-by-step guide to creating a Python Flask application that integrates with Redis, is containerized using Docker, and is deployed using Docker Compose and Kubernetes.

---

## Prerequisites

Before starting, ensure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [Pipenv](https://pypi.org/project/pipenv/) or `pip`
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/)
- [Minikube](https://minikube.sigs.k8s.io/docs/) or access to a Kubernetes cluster

---

## 1. Create the Flask Application

### Directory Structure

```
flask_app/
|-- app/
|   |-- __init__.py
|   |-- app.py
|-- requirements.txt
|-- Dockerfile
|-- docker-compose.yml
|-- kubernetes/
|   |-- deployment.yaml
|   |-- service.yaml
|-- README.md
```

### Flask Application Code

#### `app/app.py`

```python
from flask import Flask, jsonify
import redis

app = Flask(__name__)

# Connect to Redis
redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

@app.route('/')
def home():
    redis_client.incr('hits')
    count = redis_client.get('hits')
    return jsonify({"message": "Welcome to the Flask App!", "hits": count})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

#### `requirements.txt`

```
flask
redis
```

---

## 2. Create the Docker Image

#### `Dockerfile`

```dockerfile
# Use official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy application files
COPY ./app /app
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
```

Build the Docker image:

```bash
docker build -t flask-app .
```

---

## 3. Use Docker Compose

#### `docker-compose.yml`

```yaml
version: '3.8'
services:
  flask-app:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - redis
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```
---

## 5. Configure Colima on MAC for Custom CA Certificate

### Steps to Add a Custom CA Certificate

1. Add your custom CA certificate to Colima's trusted certificates:
   - Locate the certificate file (e.g., `my_custom_ca.crt`).
   - Add it to Colima's trusted certificates directory. For example:
     ```bash
     mkdir -p ~/.colima/certs
     cp my_custom_ca.crt ~/.colima/certs/
     ```

2. Restart Colima to apply the changes:
   ```bash
   colima stop
   colima start
   ```

---

Start the application using Docker Compose:

```bash
docker-compose up -d
```

Visit [http://localhost:5000](http://localhost:5000) to see the app running.

---

## 4. Deploy to Kubernetes

### Kubernetes Configuration

#### `kubernetes/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app-deployment
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
        image: flask-app:latest
        ports:
        - containerPort: 5000
      - name: redis
        image: redis:alpine
```

#### `kubernetes/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-app-service
spec:
  selector:
    app: flask-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: LoadBalancer
```

### Deploy to Kubernetes

1. Push your Docker image to a container registry (e.g., Docker Hub):

```bash
docker tag flask-app <your-dockerhub-username>/flask-app:latest
docker push <your-dockerhub-username>/flask-app:latest
```

2. Apply Kubernetes manifests:

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

3. Verify deployment:

```bash
kubectl get pods
kubectl get services
```

4. Access the application using the external IP provided by the LoadBalancer service.

---

## Cleanup

To remove the resources:

```bash
kubectl delete -f kubernetes/deployment.yaml
kubectl delete -f kubernetes/service.yaml
```

To stop the Docker Compose setup:

```bash
docker-compose down
```

---

## Notes

- Ensure the Docker image is rebuilt and pushed whenever changes are made to the Flask application.
- Modify the Kubernetes configuration based on your specific needs, such as resource limits or namespaces.

---

Enjoy building and deploying your Flask application!
# Flask REST API with MongoDB

This project is a Flask-based REST API that interacts with a MongoDB database. It provides endpoints for GET and PUT requests to manage data.

## Project Structure

