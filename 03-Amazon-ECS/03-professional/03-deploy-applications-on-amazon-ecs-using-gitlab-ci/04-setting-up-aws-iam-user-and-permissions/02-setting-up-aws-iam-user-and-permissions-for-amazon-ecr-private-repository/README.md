# Setting up IAM User and Permissions for Amazon ECR Private Repository

This document provides instructions for setting up IAM permissions to access Amazon Elastic Container Registry Private (ECR Private). These permissions will allow specified AWS IAM users, groups, or roles to perform actions such as pushing and pulling images from ECR Private repositories.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Creating an AWS IAM User](#creating-an-aws-iam-user)
- [Configuring IAM Permissions for Amazon ECR Private](#configuring-iam-permissions-for-amazon-ecr-private)
- [Best Practices](#best-practices)
- [Key Takeaways](#key-takeaways)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

Amazon ECR Private provides a Private Docker container registry for sharing Docker images across organizations or with the Private. Configuring the right IAM permissions is crucial for securing access to your Private repositories and managing who can push new images or pull existing ones.

## Prerequisites

- **AWS Account:** You must have an AWS account and administrative access to manage IAM policies.
- **AWS CLI:** Optionally, have the AWS CLI installed and configured for command-line interactions. [Install AWS CLI](https://aws.amazon.com/cli/).
- **Repository Names:** Know the names of the ECR Private repositories for which you are configuring permissions.

## Creating an AWS IAM User

1. **Log into AWS Management Console**:
  
- Navigate to the IAM dashboard and select “Users” from the sidebar.
   
2. **Add User**:

- Click on “Add user” and enter a user name (e.g., `gitlab-ci`). Select “Programmatic access” as the access type. This setting allows interaction with AWS services through API keys instead of using a password.

3. **Download Credentials**:

- After creating the user, download the CSV file containing the access key ID and secret access key. **Important**: Securely store this file as it contains sensitive information that cannot be retrieved again.

```plaintext
User: gitlab-ci
Access type: Programmatic access
```

## Configuring IAM Permissions for Amazon ECR Private

### Step 1: Log In to AWS Management Console

Access the [AWS Management Console](https://aws.amazon.com/console/) and navigate to the IAM service.

### Step 2: Create or Update IAM Policy

#### To Create a New IAM Policy:

1. **Navigate to Policies** in the IAM dashboard and click **Create policy**.
2. **Choose the JSON tab** and paste the following policy, modifying it as needed for your specific requirements:

```json
{
   "Version":"2012-10-17",
   "Statement":[
      {
         "Sid":"ListImagesInRepository",
         "Effect":"Allow",
         "Action":[
            "ecr:ListImages"
         ],
         "Resource":"arn:aws:ecr:us-east-1:123456789012:repository/my-private-repo"
      },
      {
         "Sid":"GetAuthorizationToken",
         "Effect":"Allow",
         "Action":[
            "ecr:GetAuthorizationToken"
         ],
         "Resource":"*"
      },
      {
         "Sid":"ManageRepositoryContents",
         "Effect":"Allow",
         "Action":[
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:GetRepositoryPolicy",
                "ecr:DescribeRepositories",
                "ecr:ListImages",
                "ecr:DescribeImages",
                "ecr:BatchGetImage",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload",
                "ecr:PutImage"
         ],
         "Resource":"arn:aws:ecr:us-east-1:123456789012:repository/my-private-repo"
      }
   ]
}
```

3. **Review and name your policy** (e.g., `ECRPrivateAccessPolicy`), then create the policy.

### Step 3: Attach Policy to IAM Users, Groups, or Roles

1. **Navigate to Users, Groups, or Roles** in the IAM dashboard.
2. **Select the User, Group, or Role** to which you want to grant ECR Private access.
3. **Attach the previously created or updated policy** to the selected IAM entity.

### Step 4: Verify Permissions

Optionally, test the permissions by using the AWS CLI or the Management Console to perform allowed actions, such as pushing or pulling an image to or from an ECR Private repository.

## Best Practices

- **Use Least Privilege Principle:** Always grant only the permissions necessary to perform the intended tasks.
- **Regularly Review and Update IAM Policies:** As your requirements change, regularly review and adjust IAM policies to ensure they align with current needs.
- **Secure Sensitive Operations:** Consider using Conditions in your IAM policies to restrict sensitive operations based on IP address, VPC, or other attributes.

## Conclusion

By following these steps, you will successfully configure IAM permissions for Amazon ECR Private, ensuring that your Docker images are securely managed and accessed as per your organizational policies and compliance requirements.

## References

- [AWS managed policies for Amazon Elastic Container Registry](https://docs.aws.amazon.com/AmazonECR/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-AmazonEC2ContainerRegistryFullAccess)
- [Amazon Elastic Container Registry Identity-based policy examples](https://docs.aws.amazon.com/AmazonECR/latest/userguide/security_iam_id-based-policy-examples.html)
- [Private repository policies](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-policies.html)
- [Setting a repository policy statement](https://docs.aws.amazon.com/AmazonECR/latest/userguide/set-repository-policy.html)
- [Private repository policy examples](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-policy-examples.html)