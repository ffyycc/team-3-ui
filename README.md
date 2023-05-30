# House Price Prediction - Deployment with Docker and AWS (ECS & ECR)

This README illustrates the process of deploying a House Price Prediction application using Docker, AWS Elastic Container Service (ECS) and Elastic Container Registry (ECR). This Streamlit-based application provides a user-friendly interface for predicting house prices based on different parameters, such as location, number of bathrooms, and number of living rooms.

## Prerequisites

- Docker installed on your machine
- AWS CLI installed and configured with your AWS credentials
- All project files available locally

## Overview of the Deployment Process

1. **Build the Docker Image:** Using Docker, we package the application and its dependencies into a Docker image based on the instructions provided in the Dockerfile.

2. **Test the Docker Image Locally:** The Docker image is run locally to ensure everything is working as expected.

3. **Push the Docker Image to AWS ECR:** We then push the Docker image to AWS's Elastic Container Registry (ECR). ECR is a fully-managed Docker container registry that makes it easy for developers to store, manage, and deploy Docker container images.

We create two ECR repositories: **group3-project-pipeline** and **group3-project-ui**. The first repository is used to store the Docker image for the pipeline, while the second repository is used to store the Docker image for the web application. 

For pipeline repo, you can view it on:
https://github.com/ffyycc/team-3-pipeline

Then, we tag the Docker image and push it to the ECR repository:

```bash
docker tag group3-project-pipeline:latest <account_id>.dkr.ecr.<region>.amazonaws.com/group3-project-pipeline:latest
docker push <account_id>.dkr.ecr.<region>.amazonaws.com/group3-project-pipeline:latest
```

4. **Deploy the Docker Image on AWS ECS:** Finally, the Docker image is deployed to the Elastic Container Service (ECS), AWS's highly scalable, high performance container orchestration service. ECS allows you to easily run and scale containerized applications on AWS.

This process enables the application to run on a scalable, managed service in AWS, without the need for you to handle the underlying infrastructure. Users can access the application via a web interface and adjust various parameters to get custom house price predictions.

It needs permission to read model from s3 bucket. The model is stored in the S3 bucket named: **group-3-models**

Our name for ECS service is **group3-ui**

You can also view the application at the following URL: http://group3-ui-1338407947.us-east-2.elb.amazonaws.com/
