# Creating an Elastic Container Registry

## Table of Contents

- [Introduction](#introduction)
- [What You'll Learn](#what-youll-learn)
- [Prerequisites](#prerequisites)
- [Understanding Amazon ECR](#understanding-amazon-ecr)
- [Repository Types](#repository-types)
- [Module Overview](#module-overview)
    - [Creating an Amazon ECR Public Repository](#creating-an-amazon-ecr-public-repository)
    - [Creating an Amazon ECR Private Repository](#creating-an-amazon-ecr-private-repository)
- [Choosing Between Public and Private Repositories](#choosing-between-public-and-private-repositories)
- [Key Takeaways](#key-takeaways)
- [Next Steps](#next-steps)
- [References](#references)

## Introduction

Welcome to the module on creating and managing Amazon Elastic Container Registry (ECR) repositories! Amazon ECR is a fully managed container registry service that makes it easy to store, manage, share, and deploy container images and artifacts. Whether you're building microservices, maintaining CI/CD pipelines, or distributing container images to your team or the world, ECR provides a secure and scalable solution.

This module will guide you through creating both public and private repositories in Amazon ECR, helping you understand when to use each type and how to configure them for your specific needs.

## What You'll Learn

By completing this module, you will:
- Understand the differences between public and private ECR repositories
- Learn how to create and configure ECR public repositories for sharing images globally
- Learn how to create and configure ECR private repositories for internal use
- Master authentication methods for pushing and pulling container images
- Understand security best practices for container registry management
- Know when to choose public vs. private repositories for your use case

## Prerequisites

Before starting this module, ensure you have:

- **AWS Account**: An active AWS account with appropriate permissions to create ECR repositories
- **AWS CLI**: Installed and configured with valid credentials ([Installation Guide](https://aws.amazon.com/cli/))
- **Docker**: Installed on your local machine ([Docker Installation](https://docs.docker.com/get-docker/))
- **Basic Container Knowledge**: Familiarity with Docker concepts (images, containers, tags)
- **Command Line Experience**: Comfort with terminal/command prompt operations

## Understanding Amazon ECR

Amazon Elastic Container Registry (ECR) is a container registry service that offers several key benefits:

### Key Features

**🔒 Security**
- Integration with AWS Identity and Access Management (IAM) for fine-grained access control
- Encryption at rest using AWS Key Management Service (KMS)
- Image scanning for vulnerabilities
- Private networking via VPC endpoints

**⚡ Performance**
- High availability and scalability
- Fast image push and pull operations
- Integration with Amazon ECS, EKS, and Lambda
- Geo-replication for global distribution

**💰 Cost-Effective**
- Pay only for storage and data transfer
- No upfront costs or minimum fees
- Lifecycle policies to automatically clean up unused images

**🛠️ Integration**
- Native integration with AWS services (ECS, EKS, Fargate, Lambda)
- Works seamlessly with popular CI/CD tools
- Compatible with Docker CLI and Docker Compose

## Repository Types

Amazon ECR offers two types of repositories to meet different use cases:

### Public Repositories

**Use Cases:**
- Open-source projects that need global distribution
- Sharing base images with the developer community
- Public documentation and examples
- Free tier offerings for testing and development

**Characteristics:**
- Accessible to anyone without AWS credentials
- Hosted on `public.ecr.aws` domain
- Free data transfer for pulling images (up to 500 GB/month)
- Ideal for community-driven projects

### Private Repositories

**Use Cases:**
- Internal enterprise applications
- Proprietary software and services
- Production workloads requiring strict access control
- Compliance-regulated environments

**Characteristics:**
- Accessible only with proper AWS authentication
- Hosted on account-specific domains (`<account-id>.dkr.ecr.<region>.amazonaws.com`)
- Full IAM integration for access control
- Enhanced security features (encryption, VPC endpoints)

## Module Overview

This module is divided into two hands-on sections, each focusing on a specific repository type:

### [Creating an Amazon ECR Public Repository](./01-creating-an-amazon-ecr-public-repository/README.md)

In this section, you'll learn:
- How to create a public repository using the AWS Console
- Authentication methods for public ECR
- Pushing Docker images to a public repository
- Configuring repository settings (image scanning, tag immutability)
- Best practices for public image distribution

**What You'll Build:**
A publicly accessible container registry that anyone can pull images from, perfect for open-source projects or sharing base images with the community.

**Time Estimate:** 15-20 minutes

### [Creating an Amazon ECR Private Repository](./02-creating-an-amazon-ecr-private-repository/README.md)

In this section, you'll learn:
- How to create a private repository using the AWS Console
- IAM-based authentication for private repositories
- Pushing and pulling images securely
- Configuring encryption and security settings
- Setting up lifecycle policies for image management

**What You'll Build:**
A secure, private container registry with fine-grained access control, suitable for production applications and sensitive workloads.

**Time Estimate:** 20-25 minutes

## Choosing Between Public and Private Repositories

Use this decision matrix to help determine which repository type fits your needs:

| Factor | Public Repository | Private Repository |
|--------|------------------|-------------------|
| **Visibility** | Anyone can pull images | Only authorized users |
| **Use Case** | Open source, demos, tutorials | Production apps, proprietary code |
| **Cost** | Free data transfer (500 GB/month) | Pay for data transfer |
| **Security** | Basic vulnerability scanning | Full IAM integration, encryption |
| **Access Control** | Public read, authenticated write | Granular IAM policies |
| **Networking** | Internet-based access only | VPC endpoints available |
| **Compliance** | Not suitable for regulated data | Meets compliance requirements |

**Quick Decision Guide:**

Choose **Public Repository** if:
- ✅ You're building open-source projects
- ✅ You want to share base images with the community
- ✅ You need easy, worldwide access without credentials
- ✅ You're creating educational content or demos

Choose **Private Repository** if:
- ✅ You're building production applications
- ✅ You need strict access control
- ✅ You're handling sensitive or proprietary code
- ✅ You require encryption and compliance features
- ✅ You need integration with internal AWS networking (VPC)

## Key Takeaways

After completing this module, you should understand:

1. **Repository Types**: The differences between public and private ECR repositories and when to use each
2. **Authentication**: How to authenticate Docker clients with ECR using AWS CLI
3. **Image Management**: Best practices for tagging, versioning, and organizing container images
4. **Security**: How to implement security controls through IAM, encryption, and image scanning
5. **Cost Optimization**: Using lifecycle policies to manage storage costs
6. **Integration**: How ECR integrates with other AWS services and CI/CD pipelines

## Next Steps

After completing both sections of this module:

1. **Proceed to IAM Setup**: Configure AWS IAM users and permissions for ECR access ([Module 04](../04-setting-up-aws-iam-user-and-permissions/README.md))
2. **Set Up GitHub Actions**: Automate image builds and deployments ([Module 05](../05-setting-up-github-actions-workflow/README.md))
3. **Deploy to ECS**: Use your ECR images in Amazon ECS clusters ([Module 07](../07-deploying-to-amazon-ecs/README.md))

## References

### Official AWS Documentation
- [Amazon ECR User Guide](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
- [Amazon ECR Public Documentation](https://docs.aws.amazon.com/AmazonECR/latest/public/what-is-ecr.html)
- [ECR Best Practices](https://docs.aws.amazon.com/AmazonECR/latest/userguide/best-practices.html)
- [ECR Pricing](https://aws.amazon.com/ecr/pricing/)

### Related AWS Services
- [Amazon ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [Amazon EKS Documentation](https://docs.aws.amazon.com/eks/)
- [AWS IAM Documentation](https://docs.aws.amazon.com/iam/)

### Container Security
- [ECR Image Scanning](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning.html)
- [Container Security Best Practices](https://aws.amazon.com/blogs/containers/top-20-container-security-best-practices/)
- [AWS KMS for ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/encryption-at-rest.html)