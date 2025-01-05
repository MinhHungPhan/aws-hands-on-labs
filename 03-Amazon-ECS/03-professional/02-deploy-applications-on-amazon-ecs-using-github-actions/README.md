# Deploy Applications on Amazon ECS Using GitHub Actions

Welcome to the course "Deploy Applications on Amazon ECS Using GitHub Actions." This course is designed to guide you step-by-step through the process of deploying applications on Amazon ECS using GitHub Actions. By the end of this course, you will have a fully automated CI/CD pipeline that can deploy containerized applications to ECS seamlessly.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Sub-directories Overview](#sub-directories-overview)
    - [Setting Up React Project with Create React App](#setting-up-react-project-with-create-react-app)
    - [Creating a Container Image for Amazon ECS](#creating-a-container-image-for-amazon-ecs)
    - [Creating an Elastic Container Registry](#creating-an-elastic-container-registry)
    - [Setting Up AWS IAM User and Permissions](#setting-up-aws-iam-user-and-permissions)
    - [Setting Up GitHub Actions Workflow](#setting-up-github-actions-workflow)
    - [Configuring AWS Credentials for GitHub Actions Using GitHub OIDC Provider](#configuring-aws-credentials-for-github-actions-using-github-oidc-provider)
    - [Deploying to Amazon ECS](#deploying-to-amazon-ecs)
- [Support](#support)
- [Conclusion](#conclusion)

## Introduction

In this course, you will learn how to:

- Set up a React project and containerize it for deployment.
- Create and configure Amazon Elastic Container Registry (ECR) for storing container images.
- Manage AWS IAM users and permissions for secure access.
- Set up and configure GitHub Actions workflows to build, push, and deploy applications to Amazon ECS.
- Deploy applications using modern best practices, including GitHub OIDC for secure AWS access.

By the end of the course, you will have a clear understanding of how to leverage GitHub Actions to deploy applications on Amazon ECS.

## Prerequisites

Before starting, ensure you have:

- A basic understanding of Docker, GitHub, and AWS.
- Docker installed on your local machine.
- An AWS account with access to create and manage resources.
- A GitHub account.
- Basic knowledge of the command line.

## Sub-directories Overview

### [Setting Up React Project with Create React App](01-setting-up-react-project-with-create-react-app/README.md)

In this module, you will learn how to set up a React project using the `create-react-app` tool. React is a popular JavaScript library for building user interfaces, and `create-react-app` is a command-line tool that simplifies the process of setting up a new React project. This module will guide you through the following steps:

- **Creating a React Application**: You will learn how to use `create-react-app` to quickly generate a new React project with a pre-configured build setup.
- **Understanding the Directory Structure**: You will explore the default directory structure of a React project created with `create-react-app`, understanding the purpose of each folder and file.

By the end of this module, you will have a solid foundation for starting a new React project and be familiar with the basic structure and components of a React application.

### [Creating a Container Image for Amazon ECS](02-creating-a-container-image-for-amazon-ecs/README.md)

In this module, you will learn how to build and containerize your React application using Docker. Containerizing your application ensures that it runs consistently across different environments, making it easier to deploy and manage. This module will guide you through the following steps:

- **Building a Docker Image**: You will learn how to create a Dockerfile that defines the environment and dependencies required to run your React application.
- **Optimizing for Production**: You will create a Dockerfile optimized for production environments, ensuring that your application is efficient and secure.

By the end of this module, you will have a Docker image of your React application that is ready to be deployed to Amazon Elastic Container Service (ECS).

### [Creating an Elastic Container Registry](03-creating-an-elastic-container-registry/README.md)

In this module, you will learn how to create and manage an Elastic Container Registry (ECR) on Amazon Web Services (AWS). Amazon ECR is a fully-managed Docker container registry that simplifies the process of storing, managing, and deploying Docker container images. This module is divided into two main sections:

1. **[Creating an Amazon ECR Public Repository](03-creating-an-elastic-container-registry/01-creating-an-amazon-ecr-public-repository/README.md)**: This section will guide you through the steps to set up a public repository in Amazon ECR, allowing you to share your Docker images with other developers and organizations worldwide.
2. **[Creating an Amazon ECR Private Repository](03-creating-an-elastic-container-registry/02-creating-an-amazon-ecr-private-repository/README.md)**: This section will cover the process of setting up a private repository in Amazon ECR, providing a secure environment for storing and managing your Docker images.

By the end of this module, you will have a comprehensive understanding of how to create, configure, and use both public and private repositories in Amazon ECR, enabling you to efficiently manage your containerized applications.

### [Setting Up AWS IAM User and Permissions](04-setting-up-aws-iam-user-and-permissions/README.md)

In this module, you will learn how to set up AWS Identity and Access Management (IAM) users and permissions specifically for Amazon Elastic Container Registry (ECR). AWS IAM is a web service that helps you securely control access to AWS services and resources. Properly configuring IAM users and permissions is crucial for maintaining the security and efficiency of your AWS environment. This module is divided into two main sections:

1. **[Setting Up AWS IAM User and Permissions for Amazon ECR Public Repository](04-setting-up-aws-iam-user-and-permissions/01-setting-up-aws-iam-user-and-permissions-for-amazon-ecr-public-repository/README.md)**: This section will guide you through the process of creating IAM users with the necessary permissions to access and manage public repositories in Amazon ECR.
2. **[Setting Up AWS IAM User and Permissions for Amazon ECR Private Repository](04-setting-up-aws-iam-user-and-permissions/02-setting-up-aws-iam-user-and-permissions-for-amazon-ecr-private-repository/README.md)**: This section will cover the steps to configure IAM users with permissions for accessing and managing private repositories in Amazon ECR.

By the end of this module, you will have a clear understanding of how to create and configure IAM users and permissions tailored for both public and private Amazon ECR repositories, ensuring secure and efficient access management.

### [Setting Up GitHub Actions Workflow](05-setting-up-github-actions-workflow/README.md)

In this module, you will learn how to set up GitHub Actions workflows to automate the process of building and deploying Docker images to Amazon Elastic Container Registry (ECR). GitHub Actions is a powerful CI/CD tool that allows you to automate your software development workflows directly from your GitHub repository. This module is divided into two main sections:

1. **[Setting Up GitHub Actions Workflow for Amazon ECR Public Repository](05-setting-up-github-actions-workflow/01-setting-up-github-actions-worflow-for-amazon-ecr-public-repository/README.md)**: This section will guide you through creating a GitHub Actions workflow to build and push Docker images to a public ECR repository. You will learn how to configure the workflow to automate the entire process, ensuring that your images are always up-to-date.
2. **[Setting Up GitHub Actions Workflow for Amazon ECR Private Repository](05-setting-up-github-actions-workflow/02-setting-up-github-actions-worflow-for-amazon-ecr-private-repository/README.md)**: This section will cover the steps to configure a GitHub Actions workflow for deploying Docker images to a private ECR repository. You will learn how to securely manage credentials and automate the deployment process.

By the end of this module, you will have a comprehensive understanding of how to use GitHub Actions to automate the building and deployment of Docker images to both public and private Amazon ECR repositories, streamlining your CI/CD pipeline.

### [Configuring AWS Credentials for GitHub Actions Using GitHub OIDC Provider](06-configuring-aws-credentials-for-github-actions-using-github-oidc-provider/README.md)

In this module, you will learn how to securely configure AWS credentials for GitHub Actions using GitHub's OpenID Connect (OIDC) provider. This method allows you to manage AWS credentials without storing long-lived secrets in your GitHub repository. By using OIDC, you can leverage short-lived, automatically rotated credentials, enhancing the security of your CI/CD workflows. This module is divided into three main sections:

1. **[Creating OIDC Identity Provider for GitHub Actions](06-configuring-aws-credentials-for-github-actions-using-github-oidc-provider/01-creating-oidc-identity-provider-for-github-actions/README.md)**: This section will guide you through the process of setting up an OIDC identity provider in AWS to trust GitHub Actions.
2. **[Configuring a Role for GitHub OIDC Identity Provider](06-configuring-aws-credentials-for-github-actions-using-github-oidc-provider/02-configuring-a-role-for-github-oidc-identity-provider/README.md)**: You will learn how to create and configure an AWS IAM role that GitHub Actions can assume using the OIDC provider.
3. **[Updating GitHub Actions Workflow to Use GitHub OIDC Identity Provider](06-configuring-aws-credentials-for-github-actions-using-github-oidc-provider/03-updating-github-actions-workflow-to-use-github-oidc-identity-provider/README.md)**: This section will cover the steps to update your GitHub Actions workflows to use the OIDC provider for securely accessing AWS resources.

By the end of this module, you will be able to securely configure and use AWS credentials in your GitHub Actions workflows, leveraging the benefits of GitHub's OIDC provider for enhanced security and ease of management.

### [Deploying to Amazon ECS](07-deploying-to-amazon-ecs/README.md)

In this module, you will learn how to deploy your containerized applications to Amazon Elastic Container Service (ECS) using GitHub Actions. Amazon ECS is a fully managed container orchestration service that simplifies the process of running, managing, and scaling containerized applications. By integrating GitHub Actions with Amazon ECS, you can automate the deployment process, ensuring that your applications are consistently and reliably deployed. This module is divided into two main sections:

1. **[Setting Up GitHub Actions Workflow for Amazon ECR Public Repository](07-deploying-to-amazon-ecs/01-creating-an-ecs-task-definition-cluster-and-service-for-the-fargate-launch-type/README.md)**: This section will guide you through creating a GitHub Actions workflow to build and push Docker images to a public ECR repository, and then deploy the images to an ECS cluster using the Fargate launch type.
2. **[Setting Up GitHub Actions Workflow for Amazon ECR Private Repository](07-deploying-to-amazon-ecs/02-updating-github-actions-workflow-to-deploy-ecs-task-definition-to-amazon-ecs/README.md)**: This section will cover the steps to configure a GitHub Actions workflow for deploying Docker images to a private ECR repository and updating the ECS task definition to deploy the images to an ECS cluster.

By the end of this module, you will have a comprehensive understanding of how to use GitHub Actions to automate the deployment of your containerized applications to Amazon ECS, streamlining your CI/CD pipeline and ensuring efficient and reliable deployments.

## Support

If you have any questions or need assistance, you can:
- Open an issue in the GitHub repository
- Contact the course maintainers via email at support@kientree.com
- Join our community Slack channel for real-time help

## Conclusion

Congratulations on completing the course! You now have the skills to deploy applications on Amazon ECS using GitHub Actions. Keep practicing, and don't hesitate to explore advanced topics like blue/green deployments, monitoring with AWS CloudWatch, and scaling ECS services.