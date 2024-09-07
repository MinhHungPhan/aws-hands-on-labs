# Setting up GitLab CI Workflow for Amazon ECR Public Repository

Welcome to the guide on setting up a GitLab CI/CD pipeline to build and push Docker images to an Amazon ECR (Elastic Container Registry) Public repository. This document is designed to provide a comprehensive overview of integrating GitLab CI/CD with Amazon ECR, making it an invaluable resource for developers looking to automate their Docker workflows in the AWS cloud environment. Whether you are new to CI/CD processes or looking for specific guidance on using GitLab CI/CD with Amazon ECR, this guide will help you with step-by-step instructions and best practices.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Creating GitLab CI/CD Variables](#creating-gitlab-ci-cd-variables)
- [Configuring GitLab CI/CD Pipeline](#configuring-gitlab-ci-cd-pipeline)
- [Pipeline Explanation](#pipeline-explanation)
- [Best Practices](#best-practices)
- [Key Takeaways](#key-takeaways)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

GitLab CI/CD offers a powerful automation tool to streamline software development workflows, including continuous integration (CI) and continuous deployment (CD). By integrating GitLab CI/CD with Amazon ECR, you can efficiently manage the lifecycle of your Docker images, ensuring that every push to your repository triggers a build and deploy sequence, automatically updating your Docker containers in a secure and scalable manner.

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

- You can reference these variables in your GitLab CI/CD pipeline configuration files using the `$` syntax. For example, when setting up jobs that require AWS credentials, use the variables like this:

```yaml
stages:
  - build
  - push

build:
  stage: build
  script:
    - docker build -t $AWS_REGISTRY/$AWS_REPOSITORY:$CI_COMMIT_SHA .
    - docker login -u $AWS_ACCESS_KEY_ID -p $AWS_SECRET_ACCESS_KEY $AWS_REGISTRY
    - docker push $AWS_REGISTRY/$AWS_REPOSITORY:$CI_COMMIT_SHA

```

- This approach allows your pipeline to authenticate to AWS securely without hardcoding sensitive information into your configuration files.

## Configuring GitLab CI/CD Pipeline

1. Create a `.gitlab-ci.yml` file in the root directory of your repository.

2. Define the stages and jobs for your pipeline. Here’s an example configuration:

```yaml
stages:
  - build
  - push

build:
  stage: build
  script:
    - docker build -t $AWS_REGISTRY/$AWS_REPOSITORY:$CI_COMMIT_SHA .
    - docker login -u $AWS_ACCESS_KEY_ID -p $AWS_SECRET_ACCESS_KEY $AWS_REGISTRY

push:
  stage: push
  script:
    - docker push $AWS_REGISTRY/$AWS_REPOSITORY:$CI_COMMIT_SHA
```

3. Customize the configuration based on your specific requirements, such as adding additional stages or jobs.

## Pipeline Explanation

The `.gitlab-ci.yml` configuration file defines a pipeline with two stages: `build` and `push`. Here’s a breakdown of each job:

- **Build**: Builds a Docker image from your Dockerfile and tags it with the commit SHA.
- **Push**: Pushes the Docker image to the specified ECR repository.

## Best Practices

- **Use Variables for Sensitive Information**: Always store sensitive information such as AWS credentials in GitLab CI/CD variables to secure your pipeline.
- **Keep Docker Images Lean**: Optimize Dockerfile to produce lightweight images, which reduces build time and resource consumption.
- **Regularly Update CI/CD Configuration**: Ensure you are using the latest configuration options and features provided by GitLab CI/CD.

## Key Takeaways

- Automating Docker builds through GitLab CI/CD enhances productivity and ensures consistency.
- Properly managing AWS credentials within GitLab CI/CD variables is crucial for maintaining security.
- Integrating ECR with GitLab CI/CD provides a robust solution for managing Docker containers in the cloud.

## Conclusion

By following this guide, you have learned how to set up a GitLab CI/CD pipeline to automate the building and pushing of Docker images to an Amazon ECR Public repository. This pipeline not only streamlines development processes but also ensures that your container deployments are consistent and secure.

## References

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [Using variables in GitLab CI/CD](https://docs.gitlab.com/ee/ci/variables/)
- [Docker Login](https://docs.docker.com/engine/reference/commandline/login/)
- [Docker Build](https://docs.docker.com/engine/reference/commandline/build/)
- [Docker Push](https://docs.docker.com/engine/reference/commandline/push/)
