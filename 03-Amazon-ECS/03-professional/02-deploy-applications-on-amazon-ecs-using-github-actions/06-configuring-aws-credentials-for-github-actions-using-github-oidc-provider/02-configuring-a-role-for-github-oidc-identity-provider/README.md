# Configuring a Role for GitHub OIDC Identity Provider

In [the previous tutorial](../01-creating-oidc-identity-provider-for-github-actions/README.md), we covered the steps to create an OpenID Connect (OIDC) Identity Provider for GitHub Actions in AWS. Building on that foundation, this guide will take you through the process of configuring an IAM role that allows GitHub Actions to securely access AWS resources using the OIDC identity provider. By following this guide, you will enable your GitHub workflows to authenticate and assume roles in AWS without the need for static credentials, further enhancing the security and efficiency of your CI/CD pipelines.

## Table of Contents

- [Introduction](#introduction)
- [Understanding IAM Roles and Trust Policies](#understanding-iam-roles-and-trust-policies)
- [Creating an IAM Role for GitHub Actions](#creating-an-iam-role-for-github-actions)
- [Adding a Trust Policy](#adding-a-trust-policy)
- [Assigning Permissions to the Role](#assigning-permissions-to-the-role)
- [Best Practices](#best-practices)
- [Key Takeaways](#key-takeaways)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

Welcome to the guide on configuring a role for the GitHub OIDC Identity Provider in AWS. This document is designed to help developers and DevOps professionals set up and configure an IAM role that allows GitHub Actions to securely access AWS resources using OpenID Connect (OIDC). By the end of this guide, you'll have a clear understanding of how to create an IAM role, set up a trust policy, and assign necessary permissions to enable secure and efficient CI/CD workflows.

## Understanding IAM Roles and Trust Policies

IAM (Identity and Access Management) roles in AWS are sets of permissions that define what actions are allowed and denied by an entity in the AWS environment. A trust policy is an essential part of the role that specifies which identities (such as GitHub Actions) can assume the role.

## Configuring IAM Permissions for Amazon ECR Private

1. **Access the AWS Management Console**:

- Open your web browser and sign in to the [AWS Management Console](https://aws.amazon.com/console/).

2. **Create a New IAM Policy**:

- Navigate to **Policies** in the IAM dashboard and click **Create policy**.
- Choose the **JSON tab** and paste the following policy, modifying it as needed for your specific requirements:

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

3. **Review and Create**: 

- Enter a policy name (e.g., `ECRPrivateAccessPolicy`).
- Review the policy permissions and click on **Create policy**.

## Creating an IAM Role for GitHub Actions

Follow these steps to create an IAM role for GitHub Actions:

1. **Access the AWS Management Console**:

- Open your web browser and sign in to the [AWS Management Console](https://aws.amazon.com/console/).

2. **Navigate to IAM**:

- In the AWS Management Console, select **IAM** (Identity and Access Management) from the services menu.

3. **Create a New Role**:

- Click on **Roles** in the left-hand menu and then click on **Create role**.

4. **Select Trusted Entity**:

- Choose **Web identity** as the type of trusted entity.

5. **Configure the Provider**:

- Select **GitHub** as the provider.
- Choose the appropriate audience (usually `sts.amazonaws.com`).
- Enter your GitHub organization in the appropriate field (e.g., `YOUR_GITHUB_USERNAME`)

6. **Set Permissions**:

- Select the policies that define the permissions for the role. You can attach existing policies or create a custom policy based on your needs.

7. **Review and Create**:

- Enter a role name (e.g. `GitHub-OIDC-Identity-Provider-Role`)
- Review the role configuration and click on **Create role**.

## Adding a Trust Policy

The trust policy allows GitHub Actions to assume the IAM role. Here’s how to add it:

1. **Select the Role**:

- In the IAM dashboard, click on the role you just created.

2. **Edit Trust Relationship**:

- Go to the **Trust relationships** tab and click on **Edit trust relationship**.

3. **Add Trust Policy**:

- Replace the existing policy with the following JSON, modifying the repository and branch as needed:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::YOUR_AWS_ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
          "token.actions.githubusercontent.com:sub": "repo:YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME:ref:refs/heads/YOUR_BRANCH_NAME"
        }
      }
    }
  ]
}
```

4. **Save Changes**:

- Click on **Update policy** to save the changes.

## Assigning Permissions to the Role

Assigning permissions to the role determines what actions the role can perform in AWS:

1. **Attach Policies**:

- In the IAM dashboard, select your role and navigate to the **Permissions** tab.

2. **Add Permissions**:

- Click on **Add permissions** and choose the relevant policies that the role requires. 
- Attach the `ECRPrivateAccessPolicy` policy.

3. **Create Custom Policy** (Optional):

- If you need a custom set of permissions, you can create a new policy. Click on **Create policy**, define the permissions, and attach it to your role.

Example custom policy for limited S3 access:

```json
{
    "Version": "2012-10-17",
    "Statement": [
    {
        "Effect": "Allow",
        "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject"
        ],
        "Resource": [
        "arn:aws:s3:::YOUR_BUCKET_NAME",
        "arn:aws:s3:::YOUR_BUCKET_NAME/*"
        ]
    }
    ]
}
```

## Best Practices

- **Principle of Least Privilege**: Assign only the permissions necessary for the role to perform its tasks.
- **Regular Audits**: Regularly review IAM roles and policies to ensure they meet current security and operational requirements.
- **Monitor Role Usage**: Use AWS CloudTrail to monitor the usage of the IAM roles and detect any unusual activities.

## Key Takeaways

- **Secure Authentication**: Configuring an IAM role with OIDC for GitHub Actions enhances security by removing the need for long-lived credentials.
- **Fine-Grained Access Control**: Use trust policies and permissions to precisely control what actions the GitHub Actions workflows can perform in AWS.
- **Scalable and Maintainable**: Using roles and policies allows for scalable and maintainable security configurations that can adapt to changing requirements.

## Conclusion

Setting up an IAM role for GitHub OIDC Identity Provider is a crucial step towards securing your CI/CD workflows in AWS. By following this guide, you can ensure that your GitHub Actions can securely and efficiently interact with AWS resources, enhancing both security and productivity.

## References

- [Configuring a Role for GitHub OIDC Identity Provider](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html#idp_oidc_Create_GitHub)
- [AWS IAM Roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)
- [Managing OIDC Providers](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)
- [AWS managed policies for Amazon Elastic Container Registry](https://docs.aws.amazon.com/AmazonECR/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-AmazonEC2ContainerRegistryFullAccess)
- [Amazon Elastic Container Registry Identity-based policy examples](https://docs.aws.amazon.com/AmazonECR/latest/userguide/security_iam_id-based-policy-examples.html)
- [Private repository policies](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-policies.html)
- [Setting a repository policy statement](https://docs.aws.amazon.com/AmazonECR/latest/userguide/set-repository-policy.html)
- [Private repository policy examples](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-policy-examples.html)