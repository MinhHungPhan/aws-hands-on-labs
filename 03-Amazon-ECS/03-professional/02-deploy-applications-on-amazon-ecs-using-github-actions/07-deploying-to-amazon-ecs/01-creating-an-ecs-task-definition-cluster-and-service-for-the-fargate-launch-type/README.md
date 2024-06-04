# Creating an ECS Task Definition, Cluster, and Service for the Fargate Launch Type

Welcome to this comprehensive guide on creating a Linux Task for the Fargate Launch Type in Amazon ECS. This document will take you through each step of the process, from setting up your security group to viewing your deployed service.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
    - [Step 1: Create Security Group](#step-1-create-security-group)
    - [Step 2: Creating the `ecsTaskExecutionRole` for Fargate](#step-2-creating-the-ecstaskexecutionrole-for-fargate)
- [Steps to Create a Linux Task for the Fargate Launch Type](#steps-to-create-a-linux-task-for-the-fargate-launch-type)
    - [Step 1: Create the Cluster](#step-1-create-the-cluster)
    - [Step 2: Create a Task Definition](#step-2-create-a-task-definition)
    - [Step 3: Create the Service](#step-3-create-the-service)
    - [Step 4: View Your Service](#step-4-view-your-service)
- [Best Practices](#best-practices)
- [Key Takeaways](#key-takeaways)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

This guide will walk you through creating a task in Amazon ECS using the Fargate launch type. You'll learn how to set up a security group, create a cluster, define a task, and deploy your service. By the end of this guide, you'll have a running service in Amazon ECS.

## Prerequisites

Before you start creating a Linux Task for the Fargate Launch Type, ensure you have completed the following prerequisites:

### Step 1: Create Security Group

The security group you select when creating a service with your task definition must have port 80 open for inbound traffic. Follow these steps to create the necessary security group:

1. Open the [Amazon EC2 Console](https://console.aws.amazon.com/ec2/).
2. In the navigation pane, choose **Security Groups**.
3. Choose **Create security group**.
4. For **Security group name**, enter a name (e.g., `ecs-security-group`).
5. For **Description**, enter a description.
6. For **VPC**, choose the default VPC.
7. Under **Inbound rules**, choose **Add rule**:
   - Type: HTTP
   - Protocol: TCP
   - Port range: 80
   - Source: Anywhere (0.0.0.0/0)
8. Choose **Create security group**.

### Step 2: Creating the `ecsTaskExecutionRole` for Fargate

1. **Open the IAM Console**:

- Navigate to the [IAM Console](https://console.aws.amazon.com/iam/).

2. **Create a New Role**:

- In the navigation pane, choose **Roles**, then **Create role**.
- For **Select type of trusted entity**, choose **AWS service**.
- For **Choose a use case**, choose **Elastic Container Service**, then **Elastic Container Service Task**.
- Choose **Next: Permissions**.

3. **Attach Permissions Policy**:

- In the search box, type `AmazonECSTaskExecutionRolePolicy`.
- Attach the following policy document to the role:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
```

- Select the policy, then choose **Next: Tags**.
- (Optional) Add tags for the role, then choose **Next: Review**.

4. **Name and Create the Role**:

- For **Role name**, enter `ecsTaskExecutionRole`.
- Choose **Create role**.

5. **Trust Relationship**:

- After creating the role, select the role from the list.
- Choose the **Trust relationships** tab, then **Edit trust relationship**.
- Ensure the trust relationship looks like this:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

## Steps to Create a Linux Task for the Fargate Launch Type

### Step 1: Create the Cluster

Create a cluster that uses the default VPC:

1. Open the [Amazon ECS Console](https://console.aws.amazon.com/ecs/v2).
2. From the navigation bar, select the Region to use.
3. In the navigation pane, choose **Clusters**.
4. On the **Clusters** page, choose **Create cluster**.
5. Under **Cluster configuration**, for **Cluster name**, enter a unique name (e.g., `my-fargate-cluster`).
6. (Optional) Enable Container Insights for monitoring.
7. (Optional) Add tags for identification.
8. Choose **Create**.

### Step 2: Create a Task Definition

A task definition is a blueprint for your application. Here’s how to create one:

1. In the navigation pane, choose **Task Definitions**.
2. Choose **Create new Task Definition**.
3. Choose **Create new revision with JSON**.
4. Copy and paste the following example task definition into the box and choose **Save**.

```json
{
    "family": "fargate-task-definition",
    "networkMode": "awsvpc",
    "containerDefinitions": [
        {
            "name": "fargate-container",
            "image": "your-account-id.dkr.ecr.your-region.amazonaws.com:my-ecr-repo:<tag>",
            "cpu": 512,
            "memory": 1024,
            "portMappings": [
                {
                    "containerPort": 80,
                    "hostPort": 80,
                    "protocol": "tcp"
                }
            ],
            "essential": true,
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/fargate-task-definition",
                    "awslogs-region": "your-region",
                    "awslogs-stream-prefix": "ecs"
                }
            }
        }
    ],
    "requiresCompatibilities": ["FARGATE"],
    "cpu": "512",
    "memory": "1024",
    "executionRoleArn": "arn:aws:iam::your-account-id:role/ecsTaskExecutionRole"
}
```

When utilizing the provided JSON configuration for a Fargate task definition, it's important to customize the template to fit your specific AWS environment settings. Ensure you make the following replacements in the JSON snippet:

- **your-account-id**: Replace `your-account-id` with your actual AWS account ID. This ID is unique to your account and is used to construct paths that uniquely identify your resources within AWS.

- **your-region**: Replace `your-region` with the AWS region in which you intend to deploy your Fargate tasks. This region should match the region where your AWS resources, such as ECR repositories and log groups, are located.

By updating these placeholders with your specific details, you can ensure the task definition correctly references your AWS resources and operates within the desired AWS region.

5. Choose **Create**.

### Step 3: Create the Service

Create a service using the task definition:

1. In the navigation pane, choose **Clusters**, then select your cluster.
2. From the **Services** tab, choose **Create**.
3. Under **Deployment configuration**, specify the following:
   - **Task definition**: Select the task definition created earlier.
   - **Service name**: Enter a name for your service.
   - **Desired tasks**: Enter `1`.
4. Under **Networking**, select the appropriate security group ensuring it has port 80 open.
5. Choose **Create**.

### Step 4: View Your Service

View your running service:

1. Open the [Amazon ECS Console](https://console.aws.amazon.com/ecs/v2).
2. In the navigation pane, choose **Clusters**.
3. Select the cluster where you ran the service.
4. In the **Services** tab, choose the service you created.
5. Choose the **Tasks** tab, then select the task in your service.
6. On the task page, under **Public IP**, choose **Open address** to view your running service.

## Best Practices

- **Security**: Always apply the principle of least privilege to IAM roles.
- **Monitoring**: Enable CloudWatch Container Insights for better visibility.
- **Tagging**: Use tags to organize and manage your resources effectively.

## Key Takeaways

- Ensure your security group has port 80 open for inbound traffic.
- Follow the structured steps to create clusters, task definitions, and services.
- Use the AWS Management Console for easy navigation and management of resources.

## Conclusion

Creating a Linux task for the Fargate launch type in Amazon ECS involves setting up a security group, creating a cluster, defining a task, and deploying a service. By following this guide, you should now have a running service accessible via a public IP. Remember to monitor and manage your resources effectively for optimal performance.

## References

- [AWS Fargate Documentation](https://docs.aws.amazon.com/AmazonECS/latest/userguide/what-is-fargate.html)
- [Learn how to create an Amazon ECS Linux task for the Fargate launch type](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/getting-started-fargate.html)
- [Amazon ECS task execution IAM role](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html)
- [Creating an Amazon ECS cluster for the Fargate launch type](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-cluster-console-v2.html)
- [Amazon ECS task definitions](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html)
- [Amazon ECS task definition template](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-definition-template.html)