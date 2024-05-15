# Setting Up GitHub Actions Workflow for Amazon ECR Private Repository

Welcome to the GitHub Actions for Amazon ECR (Elastic Container Registry) guide! This document is designed to help beginners and experienced users alike to understand and implement a continuous integration (CI) pipeline using GitHub Actions to build and push Docker images to an Amazon ECR private repository. The aim is to provide a straightforward, step-by-step guide to automate your Docker workflows, enhancing your deployment processes efficiently and securely.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Creating GitHub Secrets](#creating-github-secrets)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Key Takeaways](#key-takeaways)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

GitHub Actions offers a powerful, integrated solution to automate software workflows, including CI/CD, testing, and deployment. When combined with Amazon ECR, developers gain the ability to manage their Docker container images securely and efficiently. This guide focuses on creating a GitHub Actions workflow to build and push a Docker image to a private ECR repository upon changes to the main branch.

## Prerequisites

- An AWS account with access to Amazon ECR.
- A GitHub account with a repository for your project.
- Basic knowledge of Docker and AWS services.

## Creating GitHub Secrets

1. **Access Your GitHub Repository Settings**

- Navigate to your GitHub repository where you want to set up the Actions.
- Click on the **Settings** tab, which you can find at the top of the repository page.

2. **Go to the Secrets Section**

- On the left sidebar in the Settings tab, find and click on **Secrets & Variables**. This opens a submenu where you can manage secrets specifically for GitHub Actions.

3. **Add New Secrets**

- Click on the **New repository secret** button, which you’ll find on the upper-right corner of the Secrets page.
  
4. **Enter Secret Name and Value**

- In the **Name** field, enter a concise yet descriptive name for your secret. For AWS credentials, you might use `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
- In the **Value** field, paste the corresponding secret value. For example, enter your AWS Access Key ID or AWS Secret Access Key provided by AWS when you created your IAM user.

```plaintext
Name: AWS_ACCESS_KEY_ID
Value: (your AWS access key ID here)
```

```plaintext
Name: AWS_SECRET_ACCESS_KEY
Value: (your AWS secret access key here)
```

- It’s crucial to ensure that these values are entered correctly and match exactly with your AWS credentials, as any mismatch would lead to authentication errors during the Actions workflow.

5. **Save the Secret**

- Click on the **Add secret** button to save the new secret. Once added, the secret is encrypted and stored securely by GitHub. It will be accessible in your GitHub Actions workflows but not visible in logs or exposed to users.

6. **Use the Secrets in Your GitHub Actions Workflows**

- You can reference these secrets in your GitHub Actions workflow files using the `secrets` context. For example, when setting up steps that require AWS credentials, use the secrets like this:

```yaml
- name: Login to Amazon ECR
  uses: aws-actions/amazon-ecr-login@v1
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

- This approach allows your workflows to authenticate to AWS securely without hardcoding sensitive information into your workflow files.

## Configuring GitHub Actions Workflows

1. Create a `.github/workflows` directory in your repository if it doesn't exist.

2. Add the `docker-build-push.yml` file to this directory.

3. Structure your GitHub Actions workflows to use the appropriate secrets based on the environment they are deploying to. Here’s how you can set up your workflow file:


```yml
name: Build and Push Docker image to ECR Private
on:
  push:
    branches:
      - main
jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: your-region

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build, tag, and push docker image to Amazon ECR
        env:
          REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          REPOSITORY: my-private-repo
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $REGISTRY/$REPOSITORY:$IMAGE_TAG .
          docker push $REGISTRY/$REPOSITORY:$IMAGE_TAG
```

## Workflow Explanation

The `docker-build-push.yml` workflow file is triggered on every push to the `main` branch of your GitHub repository. It includes several jobs that check out the repository, configure AWS credentials, login to Amazon ECR, build the Docker image, and push it to a specified ECR repository. Here’s a breakdown of each step:

- **Checkout Repository**: Retrieves the latest code from the main branch.
- **Configure AWS Credentials**: Sets up AWS credentials for GitHub Actions, using secrets stored in your GitHub repository.
- **Login to Amazon ECR**: Authenticates with Amazon ECR to enable Docker push actions.
- **Build, Tag, and Push Docker Image**: Builds a Docker image from your Dockerfile, tags it with the current commit SHA, and pushes it to your private ECR repository.

## Best Practices

- **Keep Your Secrets Secure**: Never hard-code your credentials in your workflow files. Always use GitHub secrets.
- **Use Specific AWS IAM Roles**: Assign minimal permissions necessary for your tasks to enhance security.
- **Regularly Update Actions**: Ensure you are using the latest versions of GitHub Actions to leverage new features and security patches.

## Key Takeaways

- Automation through GitHub Actions can significantly streamline your CI/CD pipelines.
- Integrating Docker with AWS ECR via GitHub Actions enhances both security and efficiency.
- Setting up this workflow requires minimal AWS permissions, aligning with the principle of least privilege.

## Conclusion

Setting up a GitHub Actions workflow to handle Docker images with Amazon ECR simplifies development and deployment processes, securing your container management in a private, scalable environment. By following the steps outlined in this guide, you can achieve a robust and secure automation pipeline that enhances your software development lifecycle.

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)
- [Configure AWS Credentials for GitHub Actions](https://github.com/aws-actions/configure-aws-credentials)
- [Checkout V4](https://github.com/actions/checkout)
- [Amazon ECR "Login" Action for GitHub Actions](https://github.com/aws-actions/amazon-ecr-login)