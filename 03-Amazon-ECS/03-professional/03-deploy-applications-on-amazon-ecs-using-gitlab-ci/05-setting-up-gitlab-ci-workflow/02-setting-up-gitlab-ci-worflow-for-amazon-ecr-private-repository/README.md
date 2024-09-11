# Setting Up GitHub Actions Workflow for Amazon ECR Private Repository

Welcome to the GitLab CI/CD guide for Amazon ECR (Elastic Container Registry)! This document is designed to help beginners and experienced users alike to understand and implement a continuous integration (CI) pipeline using GitLab CI/CD to build and push Docker images to an Amazon ECR private repository. The aim is to provide a straightforward, step-by-step guide to automate your Docker workflows, enhancing your deployment processes efficiently and securely.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Creating GitLab CI/CD Variables](#creating-gitlab-ci-cd-variables)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Key Takeaways](#key-takeaways)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

GitLab CI/CD offers a powerful, integrated solution to automate software workflows, including CI/CD, testing, and deployment. When combined with Amazon ECR, developers gain the ability to manage their Docker container images securely and efficiently. This guide focuses on creating a GitLab CI/CD pipeline to build and push a Docker image to a private ECR repository upon changes to the main branch.

## Prerequisites

- An AWS account with access to Amazon ECR.
- A GitLab account with a repository for your project.
- Basic knowledge of Docker and AWS services.

## Creating GitLab CI/CD Variables

1. **Access Your GitLab Repository Settings**

- Navigate to your GitLab repository where you want to set up the CI/CD pipeline.
- Click on the **Settings** tab, which you can find at the top of the repository page.

2. **Go to the CI/CD Section**

- On the left sidebar in the Settings tab, find and click on **CI/CD**. This opens a submenu where you can manage variables specifically for GitLab CI/CD.

3. **Add New Variables**

- Click on the **Expand** button next to the **Variables** section.
- Click on the **Add variable** button, which you’ll find on the upper-right corner of the Variables page.

4. **Enter Variable Key and Value**

- In the **Key** field, enter a concise yet descriptive key for your variable. For AWS credentials, you might use `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
- In the **Value** field, paste the corresponding variable value. For example, enter your AWS Access Key ID or AWS Secret Access Key provided by AWS when you created your IAM user.

```plaintext
Key: AWS_ACCESS_KEY_ID
Value: (your AWS access key ID here)
```

```plaintext
Key: AWS_SECRET_ACCESS_KEY
Value: (your AWS secret access key here)
```

- It’s crucial to ensure that these values are entered correctly and match exactly with your AWS credentials, as any mismatch would lead to authentication errors during the CI/CD pipeline.

5. **Save the Variables**

- Click on the **Add variable** button to save the new variables. Once added, the variables are securely stored by GitLab. They will be accessible in your GitLab CI/CD pipeline but not visible in logs or exposed to users.

6. **Use the Variables in Your GitLab CI/CD Pipeline**

- You can reference these variables in your GitLab CI/CD pipeline files using the `$` syntax. For example, when setting up jobs that require AWS credentials, use the variables like this:

```yaml
image: docker:latest

services:
  - docker:dind

variables:
  AWS_ACCESS_KEY_ID: $AWS_ACCESS_KEY_ID
  AWS_SECRET_ACCESS_KEY: $AWS_SECRET_ACCESS_KEY

stages:
  - build
  - push

build:
  stage: build
  script:
    - docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$CI_COMMIT_SHA .
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker push $ECR_REGISTRY/$ECR_REPOSITORY:$CI_COMMIT_SHA
```

- This approach allows your pipeline to authenticate to AWS securely without hardcoding sensitive information into your pipeline files.

## Configuring GitLab CI/CD Pipelines

1. Create a `.gitlab-ci.yml` file in the root directory of your repository.

2. Define your pipeline stages and jobs in the `.gitlab-ci.yml` file. Here’s an example:

```yaml
image: docker:latest

services:
  - docker:dind

variables:
  AWS_ACCESS_KEY_ID: $AWS_ACCESS_KEY_ID
  AWS_SECRET_ACCESS_KEY: $AWS_SECRET_ACCESS_KEY

stages:
  - build
  - push

build:
  stage: build
  script:
    - docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$CI_COMMIT_SHA .
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker push $ECR_REGISTRY/$ECR_REPOSITORY:$CI_COMMIT_SHA
```

## Pipeline Explanation

The `.gitlab-ci.yml` file defines a pipeline with two stages: `build` and `push`. The `build` stage builds a Docker image from your Dockerfile, and the `push` stage pushes the image to your private ECR repository. Here’s a breakdown of each step:

- **Build**: Builds a Docker image from your Dockerfile and tags it with the current commit SHA.
- **Push**: Logs in to the GitLab Container Registry, then pushes the Docker image to your private ECR repository.

## Best Practices

- **Keep Your Variables Secure**: Never hard-code your credentials in your pipeline files. Always use GitLab CI/CD variables.
- **Use Specific AWS IAM Roles**: Assign minimal permissions necessary for your tasks to enhance security.
- **Regularly Update GitLab CI/CD**: Ensure you are using the latest versions of GitLab CI/CD to leverage new features and security patches.

## Key Takeaways

- Automation through GitLab CI/CD can significantly streamline your CI/CD pipelines.
- Integrating Docker with AWS ECR via GitLab CI/CD enhances both security and efficiency.
- Setting up this pipeline requires minimal AWS permissions, aligning with the principle of least privilege.

## Conclusion

Setting up a GitLab CI/CD pipeline to handle Docker images with Amazon ECR simplifies development and deployment processes, securing your container management in a private, scalable environment. By following the steps outlined in this guide, you can achieve a robust and secure automation pipeline that enhances your software development lifecycle.

## References

- [Docker in Docker (dind)](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html#use-docker-in-docker-executor)
- [GitLab Container Registry](https://docs.gitlab.com/ee/user/packages/container_registry/)
- [Gitlab CI: Build & push Docker image to AWS ECR (Elastic Container Registry)](https://www.youtube.com/watch?v=jg9sUceyGaQ&ab_channel=ValentinDespa)
- [GitLab CI Build and Push Docker Image to AWS ECR | GitLab CI CD Docker AWS | Push Image to ECR](https://www.youtube.com/watch?v=dl2Dn1b85nw&ab_channel=DevOpsHint)
- [Deploy to Amazon Elastic Container Service](https://docs.gitlab.com/ee/ci/cloud_deployment/ecs/deploy_to_aws_ecs.html)
- [Automating Deployments to ECS with GitLab CI/CD](https://www.youtube.com/watch?v=Grc_5v4rOFI&ab_channel=GitLabUnfiltered)
- [ECS.gitlab-ci.yml](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/Deploy/ECS.gitlab-ci.yml)
- [Using variables in GitLab CI/CD](https://docs.gitlab.com/ee/ci/variables/)
- [Docker Login](https://docs.docker.com/engine/reference/commandline/login/)
- [Docker Build](https://docs.docker.com/engine/reference/commandline/build/)
- [Docker Push](https://docs.docker.com/engine/reference/commandline/push/)