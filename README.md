# Cloud-Native ML Container Engine: Real Estate Price Prediction

This project demonstrates the deployment of a Machine Learning model as a platform-agnostic, serverless microservice using **Python**, **Docker**, and **AWS (Lambda & ECR)**. It bypasses the traditional 250MB AWS Lambda deployment package size limit by packaging heavy data science libraries (`pandas`, `scikit-learn`) into an isolated container.

## 🚀 Architecture Overview

The system is engineered as an autonomous serverless containerized microservice:
1. **Client**: Sends an HTTP POST request containing real estate features via client-side tools (e.g., Windows PowerShell).
2. **AWS API Gateway**: Acts as a low-latency RESTful bridge to forward the payload.
3. **AWS Lambda**: Boots up the autonomous Docker container, parses the event, creates a Pandas DataFrame, and serves predictions using the serialized Scikit-Learn model.
4. **AWS ECR**: Hosts the secure, version-controlled Docker image.

## 🛠️ Tech Stack & Dependencies
- **Core Language**: Python 3.11
- **ML & Data Libraries**: Pandas, Scikit-Learn, Joblib, Numpy
- **Containerization**: Docker (Linux Slim Runtime)
- **Cloud Infrastructure**: AWS Lambda (Container Image Support), AWS ECR, AWS API Gateway

## 📦 Container Configuration (Dockerfile)

```dockerfile
FROM public.ecr.aws/lambda/python:3.11

# Copy source code and the pre-trained model artifact
COPY app.py real_estate_model.joblib ${LAMBDA_TASK_ROOT}/

# Install optimized binary wheels to avoid runtime GCC compilation issues
RUN pip install --no-cache-dir --only-binary=:all: pandas scikit-learn joblib numpy

CMD [ "app.handler" ]
