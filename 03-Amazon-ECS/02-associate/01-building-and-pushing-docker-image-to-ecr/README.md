# Building and Pushing Docker Image to AWS ECR

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Building and Pushing Process](#building-and-pushing-process)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

Amazon Elastic Container Registry (ECR) is a fully managed Docker container registry that makes it easy for developers to store, manage, and deploy Docker container images. This guide provides step-by-step instructions to build a Docker image from your application and push it to an Amazon Web Services (AWS) ECR private repository.

## Prerequisites

Before you begin, ensure you have the following:

1. AWS CLI installed and configured with appropriate permissions.
2. Docker installed on your local machine.
3. An AWS ECR repository created.

## Building and Pushing Process

### 1. Configure AWS CLI

First, configure the AWS CLI with your AWS credentials. Run the following command and follow the prompts to enter your AWS Access Key ID, Secret Access Key, and default region:

```sh
aws configure
```

You will be prompted to enter the following details:

```sh
AWS Access Key ID [None]: <your_access_key_id>
AWS Secret Access Key [None]: <your_secret_access_key>
Default region name [None]: <your_default_region>
Default output format [None]: json
```

### 2. List All ECR Repositories

To list all the repositories in your AWS ECR, you can use the following command:

```sh
aws ecr describe-repositories --region <aws_region>
```

#### Example

For the AWS region `us-east-1`, the command would be:

```sh
aws ecr describe-repositories --region us-east-1
```

If you want to get a simplified list of repository names, you can use this command:

```sh
aws ecr describe-repositories --region us-east-1 --query "repositories[*].repositoryName" --output text
```

### 3. Authenticate Docker with AWS ECR

Retrieve an authentication token and authenticate your Docker client to your ECR registry. Run the following command, replacing `<aws_region>` with your region (e.g., `us-east-1`):

```sh
aws ecr get-login-password --region <aws_region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com
```

### 4. Build Your Docker Image

Navigate to the directory containing your `Dockerfile` and build your Docker image. Replace `<image_name>` with a name for your image:

```sh
docker build -t <image_name> .
```

### 5. Tag Your Docker Image

Tag your image with the ECR repository URI. Replace `<aws_account_id>`, `<aws_region>`, `<repository_name>`, and `<image_name>` as appropriate:

```sh
docker tag <image_name>:latest <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com/<repository_name>:latest
```

### 6. Push Your Docker Image to ECR

Push the tagged image to your ECR repository:

```sh
docker push <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com/<repository_name>:latest
```

### 7. Verify the Image in ECR

You can verify that your image has been successfully pushed to ECR by listing the images in your repository:

```sh
aws ecr list-images --repository-name <repository_name> --region <aws_region>
```

## Conclusion

By following this guide, you have successfully built a Docker image from your application and pushed it to an AWS ECR private repository. With your image stored in ECR, you can now easily manage and deploy it to various AWS services such as Amazon Elastic Kubernetes Service (EKS) or Amazon Elastic Container Service (ECS). Utilizing ECR ensures a seamless and secure integration with your AWS infrastructure, streamlining your containerized application development and deployment process.

## References

- [Creating a container image for use on Amazon ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-container-image.html)
- [Pushing an image to an Amazon ECR private repository](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-push.html)
- [Best practices for container images](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-considerations.html)
- [Deploying to Amazon Elastic Container Service](https://docs.github.com/en/actions/deployment/deploying-to-your-cloud-provider/deploying-to-amazon-elastic-container-service)