# Deploying Applications on Amazon ECS using Docker Compose

Welcome to our comprehensive guide on deploying applications on Amazon Elastic Container Service (ECS) using Docker Compose. This document is designed to help developers of all skill levels utilize Docker Compose for deploying their containerized applications seamlessly to Amazon ECS and AWS Fargate. Whether you're moving applications from your local development environment to the cloud or scaling your deployments in a production environment, this guide will walk you through the process step-by-step, ensuring a smooth transition and scalable deployment.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Deploying Yelb Locally](#deploying-yelb-locally)
- [Deploying Yelb with Docker Compose on Amazon ECS](#deploying-yelb-with-docker-compose-on-amazon-ecs)
- [Best Practices](#best-practices)
- [Key Takeaways](#key-takeaways)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

Containers have revolutionized the way developers build, package, and deploy applications. Docker, by simplifying access to containerization technology, has played a pivotal role in this transformation. One of Docker's most powerful tools is Docker Compose, a tool for defining and running multi-container Docker applications. With Compose, you can create a YAML file to define the services, networks, and volumes for your application, and with a single command, create and start all the services from your configuration.

Amazon Web Services (AWS) and Docker have collaborated to extend Docker Compose's capabilities to Amazon ECS and AWS Fargate, making it easier than ever for developers to deploy their containerized applications to the cloud. This guide focuses on leveraging Docker Compose for deploying applications on Amazon ECS, enhancing the developer experience, and extending existing investments in containerized applications.

## Prerequisites

Before diving into the deployment process, ensure you have the following prerequisites in place:
- Docker Desktop installed on your workstation.
- An AWS account set up with the necessary permissions to deploy resources on ECS.
- Familiarity with basic Docker concepts and commands.

## Deploying Yelb Locally

### Step 1: Clone the Yelb Repository

First, you need to clone the Yelb repository from GitHub to get the Docker Compose file and other necessary resources for deployment.

```bash
git clone https://github.com/mreferre/yelb
```

### Step 2: Review the Docker Compose File

Navigate to the `platformdeployment/Docker` directory within the cloned repository:

```bash
cd yelb/deployments/platformdeployment/Docker/
```

Now, list the contents of the directory to ensure you have the necessary files:

```bash
ls
```

**Expected Output:**

```
README.md docker-compose.yaml stack-deploy.yaml
```

This output confirms the presence of the `docker-compose.yaml` file among others. The `docker-compose.yaml` file is crucial as it defines the Yelb application's architecture, including the user interface, application server, cache server, and database components.

Take some time to examine the `docker-compose.yaml` file to understand the roles of different services within the application and how they interact with each other. This understanding is key to successfully deploying and managing the application on Amazon ECS.

### Step 3: Deploy Locally

To test the Yelb application locally before deploying it to ECS, run:

```bash
docker-compose up -d
```

Then, navigate to `http://localhost` in your web browser to verify the application is running correctly.

## Deploying Yelb with Docker Compose on Amazon ECS

### Step 1: Create a Docker Context for ECS

A [Docker context](https://docs.docker.com/engine/context/working-with-contexts/) is a powerful feature that allows you to define different environments for running your Docker commands. Essentially, a context stores configuration data for Docker engines to help you manage multiple environments from a single Docker client. By default, Docker commands run against your local Docker engine, but with Docker contexts, you can switch between different Docker engines or environments. This is particularly useful when you need to manage containers in remote environments, such as cloud providers like Amazon ECS.

Creating a Docker context for ECS tells Docker to execute your commands (like deploying applications) on Amazon ECS, leveraging cloud resources instead of your local machine. This enables seamless deployment of containerized applications to the cloud directly from your local Docker CLI, without changing your workflow.

Create a new Docker context that targets Amazon ECS. This context tells Docker to deploy the application to ECS instead of your local Docker environment:

**Command:**

```bash
docker context create ecs myecscontext
```

**Expected Output:**

```
? Create a Docker context using: An existing AWS profile
? Select AWS Profile default
Successfully created ecs context "myecscontext"
```

This output indicates that the Docker context `myecscontext` has been successfully created using your existing AWS profile named `default`. 

> **Note**: It's crucial that the AWS profile used has sufficient permissions to deploy the application on AWS, including creating necessary resources like VPCs, ECS tasks, and Load Balancers.

After creating the context, you can list all your Docker contexts to see the newly created one:

**Command:**

```bash
docker context ls
```

**Expected Output:**

```
NAME                TYPE                DESCRIPTION                               DOCKER ENDPOINT               KUBERNETES ENDPOINT   ORCHESTRATOR
default             moby                Current DOCKER_HOST based configuration   unix:///var/run/docker.sock                         swarm
myecscontext        ecs
```

This output shows that the `myecscontext` (of type `ecs`) is now available alongside the default context.

To set `myecscontext` as the current context, you use the following command:

**Command:**

```bash
docker context use myecscontext
```

**Expected Output:**

```
myecscontext
```

And to confirm that `myecscontext` is now the active context:

**Command:**

```bash
docker context ls
```

**Expected Output:**

```
NAME                TYPE                DESCRIPTION                               DOCKER ENDPOINT               KUBERNETES ENDPOINT   ORCHESTRATOR
default             moby                Current DOCKER_HOST based configuration   unix:///var/run/docker.sock                         swarm
myecscontext *      ecs
```

The asterisk (*) next to `myecscontext` indicates that it is now the active context. This means that Docker commands will now be executed in the context of your AWS environment, leveraging ECS.

### Step 2: Deploy to Amazon ECS

Set the newly created ECS context as the current context and deploy the Yelb application to Amazon ECS using Docker Compose.

```bash
docker context use myecscontext
docker compose up
```

This command transforms your Docker Compose file into an AWS CloudFormation template and deploys it on AWS, leveraging ECS and Fargate.

### Step 3: Verify Deployment

Once the deployment process is complete, Docker will provide an endpoint URL for accessing your deployed Yelb application. Open this URL in a web browser to verify that the application is running on Amazon ECS.

## Best Practices

- **Keep your Docker Compose files version-controlled:** Ensure that your `docker-compose.yml` files are stored in version control to track changes and maintain consistency across environments.
- **Use environment variables for secrets:** Avoid hardcoding sensitive information in your Docker Compose files. Use environment variables to manage secrets securely.
- **Optimize your images for size and speed:** Use multi-stage builds and remove unnecessary files to keep your Docker images lightweight and fast to deploy.

## Key Takeaways

- Docker Compose simplifies defining and running multi-container Docker applications.
- AWS and Docker collaboration extends Docker Compose's capabilities to Amazon ECS, making cloud deployments easier.
- Deploying to ECS involves creating a Docker context for ECS, setting it as the current context, and using `docker compose up` to deploy your application.

## Conclusion

Deploying applications on Amazon ECS using Docker Compose combines the ease of defining multi-container applications with Docker Compose with the scalability and reliability of AWS. This guide aimed to provide you with the knowledge to start deploying your applications to Amazon ECS, leveraging Docker Compose for a seamless development to production workflow. Remember, the journey doesn't end here; continue exploring, experimenting, and optimizing your deployments.

### References

- [Docker Compose documentation](https://docs.docker.com/compose/)
- [Amazon ECS documentation](https://aws.amazon.com/ecs/)
- [AWS Fargate documentation](https://aws.amazon.com/fargate/)
- [Docker contexts](https://docs.docker.com/engine/context/working-with-contexts/)
- [Configuring AWS Profile](https://github.com/MinhHungPhan/aws-hands-on-labs/tree/main/02-AWS-CLI/01-foundational/01-configuring-aws-profile)