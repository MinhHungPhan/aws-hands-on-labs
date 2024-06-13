# Updating GitHub Actions Workflow to Deploy ECS Task Definition to Amazon ECS

Welcome to this guide on updating your GitHub Actions workflow to deploy an ECS Task Definition to Amazon ECS. This document will guide you through the process, providing step-by-step instructions, examples, and best practices to ensure a smooth deployment.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Updating GitHub Actions Workflow](#updating-github-actions-workflow)
    - [Step 1: Rename the Workflow File](#step-1-rename-the-workflow-file)
    - [Step 2: Define Environment Variables](#step-2-define-environment-variables)
    - [Step 3: Output Image URI](#step-3-output-image-uri)
    - [Step 4: Update ECS Task Definition](#step-4-update-ecs-task-definition)
    - [Step 5: Deploy ECS Task Definition](#step-5-deploy-ecs-task-definition)
- [Best Practices](#best-practices)
- [Key Takeaways](#key-takeaways)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

This guide will help you update your GitHub Actions workflow to deploy an ECS Task Definition to Amazon ECS. GitHub Actions enables you to automate software workflows, making it a powerful tool for continuous integration and continuous deployment (CI/CD). By the end of this guide, you will have a workflow that builds your Docker image, pushes it to Amazon ECR, and updates your ECS service.

## Prerequisites

Before you begin, ensure you have the following prerequisites:

1. An AWS account with necessary permissions to create and manage ECS resources.
2. AWS CLI configured on your local machine.
3. A GitHub repository for your project.
4. Docker installed on your local machine.

## Updating GitHub Actions Workflow

The following example workflow demonstrates how to build a container image and push it to Amazon ECR. It then updates the task definition with the new image ID, and deploys the task definition to Amazon ECS. Ensure that you provide your own values for all the variables in the `env` key of the workflow.

### Step 1: Rename the Workflow File

- Rename the workflow file from `docker-build-push.yml` to `deploy-to-ecs.yml`.

- Update the name of the GitHub Actions workflow:

```yaml
name: Deploy to Amazon ECS
```

### Step 2: Define Environment Variables

Define environment variables in your workflow file (`deploy-to-ecs.yml`):

```yaml
name: Deploy to Amazon ECS
on:
  push:
    branches:
      - main
env:
  AWS_REGION: ${{ vars.AWS_REGION }}            # set this to your preferred AWS region, e.g. us-west-1
  ECR_REPOSITORY: ${{ vars.ECR_REPOSITORY }}    # set this to your Amazon ECR repository name
  ECS_SERVICE: ${{ vars.ECS_SERVICE }}          # set this to your Amazon ECS service name
  ECS_CLUSTER: ${{ vars.ECS_CLUSTER }}          # set this to your Amazon ECS cluster name
  ECS_TASK_DEFINITION: ${{ vars.ECS_TASK_DEFINITION }} # set this to the path to your Amazon ECS task definition file, e.g. .aws/task-definition.json
  CONTAINER_NAME: ${{ vars.CONTAINER_NAME }}    # set this to the name of the container in the containerDefinitions section of your task definition

# ... existing code ...
```

### Step 3: Output Image URI

Add a command to output the image URI to the GitHub Actions output:

```yaml
# ... existing code ...
      - name: Build, tag, and push docker image to Amazon ECR
        id: build-image
        env:
          REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          REPOSITORY: ${{ vars.ECR_REPOSITORY }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $REGISTRY/$REPOSITORY:$IMAGE_TAG .
          docker push $REGISTRY/$REPOSITORY:$IMAGE_TAG
          echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT
# ... existing code ...
```

In this workflow:

- The `$GITHUB_OUTPUT` is a special environment variable in GitHub Actions that you can use to set the output of a step. This output can then be used by subsequent steps within the same job. By writing to this variable, you can pass data between steps in a GitHub Actions workflow.
- The `echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT` line sets the `image` output variable for the `build-image` step.
- This output can then be accessed in subsequent steps using `${{ steps.build-image.outputs.image }}`.

### Step 4: Update ECS Task Definition

Update the ECS task definition with the new image ID:

```yaml
# ... existing code ...
      - name: Fill in the new image ID in the Amazon ECS task definition
        id: task-def
        uses: aws-actions/amazon-ecs-render-task-definition@c804dfbdd57f713b6c079302a4c01db7017a36fc
        with:
          task-definition: ${{ env.ECS_TASK_DEFINITION }}
          container-name: ${{ env.CONTAINER_NAME }}
          image: ${{ steps.build-image.outputs.image }}
# ... existing code ...
```

### Step 5: Deploy ECS Task Definition

Deploy the updated ECS task definition to Amazon ECS:

```yaml
# ... existing code ...
      - name: Deploy Amazon ECS task definition
        uses: aws-actions/amazon-ecs-deploy-task-definition@df9643053eda01f169e64a0e60233aacca83799a
        with:
          task-definition: ${{ steps.task-def.outputs.task-definition }}
          service: ${{ env.ECS_SERVICE }}
          cluster: ${{ env.ECS_CLUSTER }}
          wait-for-service-stability: true
```

## Best Practices

- **Security**: Ensure your AWS credentials are stored securely in GitHub Secrets.
- **Docker Layers**: Use multi-stage builds in Docker to minimize image size and improve build times.
- **CI/CD**: Regularly update and maintain your CI/CD pipeline to incorporate best practices and new features.

## Key Takeaways

- GitHub Actions is a powerful tool for automating your deployment pipeline.
- Securely store your AWS credentials in GitHub Secrets.
- Automate the build, push, and deployment process to minimize manual intervention.

## Conclusion

Updating your GitHub Actions workflow to deploy an ECS Task Definition to Amazon ECS streamlines your deployment process, ensuring consistent and reliable deployments. By following this guide, you can set up an automated workflow that builds, pushes, and deploys your Docker images to ECS.

## References

- [Deploying to Amazon Elastic Container Service](https://docs.github.com/en/actions/deployment/deploying-to-your-cloud-provider/deploying-to-amazon-elastic-container-service)
- [Workflow commands for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions)
- [Amazon ECS "Render Task Definition" Action for GitHub Actions](https://github.com/aws-actions/amazon-ecs-render-task-definition)
- [Amazon ECS "Deploy Task Definition" Action for GitHub Actions](https://github.com/aws-actions/amazon-ecs-deploy-task-definition)