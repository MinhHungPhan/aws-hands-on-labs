# Creating a Lambda in a Private Subnet

Great! Now that we've got our VPC Interface Endpoint for Secrets Manager up and running from the previous tutorial, it's time to put it to good use. In this guide, we'll create a Lambda function that lives in a private subnet and uses our shiny new endpoint to securely retrieve secrets. This is where the magic really happens!

## Table of Contents

- [Introduction](#introduction)
- [Why Lambda in Private Subnets?](#why-lambda-in-private-subnets)
- [Prerequisites](#prerequisites)
- [Step-by-Step Guide](#step-by-step-guide)
- [Understanding the Lambda Code](#understanding-the-lambda-code)
- [Testing Your Setup](#testing-your-setup)
- [Troubleshooting Common Issues](#troubleshooting-common-issues)
- [Best Practices](#best-practices)
- [Key Takeaways](#key-takeaways)
- [What's Next?](#whats-next)
- [References](#references)

## Introduction

Alright, so you've successfully created that VPC Interface Endpoint for Secrets Manager (if you haven't, go back and check out the previous tutorial - this builds directly on that!). Now we're going to create a Lambda function that actually uses it.

The cool thing about this setup is that your Lambda will be completely isolated from the public internet, yet it can still retrieve secrets securely through our private endpoint. No internet gateway needed, no NAT gateway costs, and definitely no security concerns about your Lambda reaching out to the public web.

Think of it this way: your Lambda is like a person working in a secure office building (private subnet) who needs to access a secure vault (Secrets Manager). Instead of leaving the building and walking across town (public internet), they use a secure internal tunnel (VPC endpoint) to reach the vault. Much safer and more efficient!

## Why Lambda in Private Subnets?

You might be wondering, "Why put Lambda in a private subnet at all?" Fair question! Here's the deal:

- **Enhanced Security**: Your Lambda can't accidentally make calls to random internet services or be targeted by external threats
- **Compliance Requirements**: Many organizations require that compute resources handling sensitive data stay off the public internet
- **Cost Optimization**: No need for expensive NAT gateways just to reach AWS services
- **Network Control**: You have complete control over what your Lambda can and cannot access
- **Audit Trail**: All network traffic is contained within your VPC, making it easier to monitor and log

The tradeoff? Your Lambda won't be able to reach the public internet for things like downloading packages or calling external APIs. But for our use case of just accessing Secrets Manager, that's perfectly fine!

## Prerequisites

Before we dive in, make sure you have:

- ✅ Completed the previous tutorial on creating a VPC Interface Endpoint for Secrets Manager
- ✅ A VPC with private subnets (ideally in multiple AZs for redundancy)
- ✅ The VPC endpoint from the previous tutorial is working and accessible
- ✅ A secret stored in AWS Secrets Manager that we can test with
- ✅ Basic familiarity with Lambda functions and IAM roles

If you're missing any of these, no worries - just circle back and get them sorted before proceeding.

## Step-by-Step Guide

Okay, let's get our hands dirty! We'll create the Lambda function step by step.

### Step 1: Create the IAM Role

First, we need to create an execution role for our Lambda. This role needs some specific permissions since our Lambda will be running in a VPC and accessing Secrets Manager.

1. Head over to **IAM > Roles** in the AWS Console
2. Click **Create role**
3. Select **AWS service** and then **Lambda**
4. For now, just attach the basic **AWSLambdaBasicExecutionRole** (we'll customize it in a moment)
5. Name it something like `lambda-private-subnet-secrets-role`
6. Create the role

Now comes the important part - we need to attach a custom policy. I've included a policy file in this repository (`iam/lambda-execution-role-policy.json`) that covers all the permissions we need:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateNetworkInterface",
                "ec2:DeleteNetworkInterface", 
                "ec2:DescribeNetworkInterfaces"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt",
                "kms:DescribeKey"
            ],
            "Resource": "arn:aws:kms:your-region:your-account:key/your-key-id"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:DescribeLogGroups",
                "logs:PutRetentionPolicy"
            ],
            "Resource": "*"
        }
    ]
}
```

**What's happening here?**
- The **EC2 permissions** are crucial - Lambda needs these to create network interfaces in your VPC subnets
- The **Secrets Manager permission** lets our Lambda actually retrieve secrets
- The **KMS permissions** are needed because most secrets in Secrets Manager are encrypted with KMS keys. Your Lambda needs to decrypt the secret when retrieving it
- The **CloudWatch Logs permissions** ensure we can see what's happening when our Lambda runs

**Important note about KMS**: You'll need to update the KMS resource ARN in the policy to match the KMS key that's encrypting your secrets. You can find this in the Secrets Manager console when you look at your secret's details, or by checking the actual policy file in this repository which has the specific ARN for our demo setup.

### Step 2: Create the Lambda Function

Now for the fun part - creating the actual Lambda function!

1. Navigate to **Lambda > Functions** in the AWS Console
2. Click **Create function**
3. Choose **Author from scratch**
4. Give it a meaningful name like `secrets-manager-private-test`
5. Choose **Python 3.9** (or whatever your preferred Python version is)
6. For the execution role, select **Use an existing role** and choose the role we just created
7. Click **Create function**

### Step 3: Configure VPC Settings

This is where the private subnet magic happens:

1. In your Lambda function, scroll down to **Configuration**
2. Click on **VPC** in the left sidebar
3. Click **Edit**
4. Select your VPC (the same one where you created the interface endpoint)
5. For subnets, select your **private subnets** only. I recommend choosing subnets in multiple AZs for redundancy
6. For security groups, you have a couple of options:
   - Create a new security group specifically for this Lambda
   - Use an existing security group that allows outbound HTTPS traffic (port 443)

**Security Group Requirements:**
Your Lambda's security group needs these outbound rules:
- **Type**: HTTPS (443)
- **Destination**: Either 0.0.0.0/0 or the security group attached to your VPC endpoint
- **Purpose**: This allows your Lambda to reach the Secrets Manager endpoint

7. Click **Save**

**Heads up**: The first time you save VPC configuration, it might take a few minutes. AWS is creating network interfaces in your subnets behind the scenes.

### Step 4: Add the Lambda Code

Now let's add some code that actually tests our setup. I've created a Python script (`scripts/lambda_function.py`) that does three important things:

1. Tests DNS resolution of the Secrets Manager endpoint
2. Tests network connectivity on port 443
3. Actually tries to retrieve a secret

Here's what the code looks like:

```python
import boto3
import socket

def lambda_handler(event, context):
    result = {}

    # 1. DNS resolution test
    try:
        resolved_ip = socket.gethostbyname("secretsmanager.eu-west-1.amazonaws.com")
        result["ResolvedSecretsManagerIP"] = resolved_ip
    except Exception as e:
        result["DNSResolutionError"] = str(e)

    # 2. Connectivity test on port 443  
    try:
        s = socket.create_connection(("secretsmanager.eu-west-1.amazonaws.com", 443), timeout=3)
        result["Port443Connectivity"] = "Success"
        s.close()
    except Exception as e:
        result["Port443Connectivity"] = f"Failed: {e}"

    # 3. Secrets Manager API call
    try:
        client = boto3.client('secretsmanager', region_name='eu-west-1')
        response = client.get_secret_value(
            SecretId='your-secret-arn-here'  # Replace with your actual secret ARN
        )
        result["SecretValue"] = response.get('SecretString')
    except Exception as e:
        result["SecretsManagerError"] = str(e)

    return result
```

**Important**: Make sure to replace `'your-secret-arn-here'` with the actual ARN of a secret in your Secrets Manager, and update the region if you're not using `eu-west-1`.

1. Copy this code into your Lambda function
2. Click **Deploy** to save the changes

### Step 5: Configure Test Event

Let's create a simple test event:

1. Click **Test** in the Lambda console
2. Choose **Create new test event**
3. Use the default **hello-world** template (the event content doesn't matter for our test)
4. Name it something like `private-subnet-test`
5. Click **Save**

## Understanding the Lambda Code

Let me break down what our test code is actually doing, because each part tells us something important:

### DNS Resolution Test

```python
resolved_ip = socket.gethostbyname("secretsmanager.eu-west-1.amazonaws.com")
```

This checks if our Lambda can resolve the Secrets Manager domain name. If our VPC endpoint is configured correctly with private DNS enabled, this should resolve to a private IP address (something like 10.x.x.x or 172.x.x.x) instead of a public AWS IP.

### Connectivity Test

```python
s = socket.create_connection(("secretsmanager.eu-west-1.amazonaws.com", 443), timeout=3)
```

This verifies that our Lambda can actually establish a TCP connection to the Secrets Manager service on port 443. If this fails, it usually means there's a security group or network ACL issue.

### API Call Test

```python
client = boto3.client('secretsmanager', region_name='eu-west-1')
response = client.get_secret_value(SecretId='your-secret-arn')
```

This is the real test - can our Lambda actually retrieve a secret using the AWS SDK? This tests the full end-to-end functionality.

## Testing Your Setup

Time for the moment of truth! Let's see if everything works:

1. Click **Test** in your Lambda function
2. Watch the execution results

**What you should see if everything is working:**

```json
{
  "ResolvedSecretsManagerIP": "10.0.1.100",
  "Port443Connectivity": "Success", 
  "SecretValue": "{\"username\":\"admin\",\"password\":\"secret123\"}"
}
```

**Key indicators of success:**
- The resolved IP should be a private IP address (10.x.x.x, 172.x.x.x, or 192.168.x.x)
- Port 443 connectivity should show "Success"
- You should see the actual secret value returned

If you see this, congratulations! Your Lambda is successfully using the VPC endpoint to retrieve secrets privately.

## Troubleshooting Common Issues

Don't worry if things don't work perfectly on the first try. Here are the most common issues I've encountered:

### "Task timed out after X seconds"

This usually means your Lambda can't reach the Secrets Manager endpoint at all.

**Check these:**
- Is your Lambda in the correct private subnets?
- Does your Lambda's security group allow outbound HTTPS (port 443)?
- Is the VPC endpoint in the same subnets as your Lambda?
- Are the route tables for your private subnets pointing local traffic to the VPC endpoint?

### "DNS resolution failed"

Your Lambda can't resolve the Secrets Manager domain name.

**Check these:**
- Is "Enable Private DNS" turned on for your VPC endpoint?
- Are you using the correct region in your domain name?
- Check if you have any custom DNS configurations that might interfere

### "Access denied" or permission errors

Your Lambda doesn't have the right permissions.

**Check these:**
- Does your Lambda's execution role include the IAM policy we created?
- Is the secret ARN correct in your code?
- Do you have the right permissions on the secret itself?

### Getting a public IP instead of private IP

This means your traffic is going over the internet instead of through the VPC endpoint.

**Check these:**
- Is "Enable Private DNS" enabled on your VPC endpoint?
- Are there any route table conflicts sending traffic to an internet gateway?

## Best Practices

Here are some tips I've learned the hard way:

### Security

- **Principle of least privilege**: Only give your Lambda permissions to the specific secrets it needs, not all secrets
- **Use separate roles**: Don't reuse Lambda execution roles across different functions with different requirements
- **Monitor access**: Set up CloudWatch alarms for unusual Secrets Manager access patterns

### Reliability  

- **Multi-AZ deployment**: Put your Lambda subnets in multiple availability zones
- **Error handling**: Always wrap your Secrets Manager calls in try-catch blocks
- **Timeout considerations**: VPC Lambdas can take a bit longer to start up, so adjust your timeout accordingly

### Performance

- **Connection reuse**: The boto3 client can be reused across Lambda invocations if you declare it outside the handler
- **Caching**: Consider caching secrets in memory for short periods to reduce API calls (but be careful about secret rotation!)
- **Right-sizing**: VPC Lambdas use a bit more memory for network interfaces, so you might need to bump up your memory allocation

### Cost Optimization

- **No NAT gateway needed**: One of the big wins here is that you don't need expensive NAT gateways
- **Endpoint policies**: Use VPC endpoint policies to restrict access and potentially reduce data transfer costs
- **Regional considerations**: Keep everything in the same region to avoid cross-region data transfer charges

## Key Takeaways

Let's recap what we've accomplished:

- ✅ Created a Lambda function that runs in a private subnet with no internet access
- ✅ Configured proper IAM permissions for VPC-enabled Lambda functions
- ✅ Successfully retrieved secrets through our VPC endpoint without using the public internet
- ✅ Verified that DNS resolution points to private IP addresses
- ✅ Built a foundation for secure, private access to AWS services

The beautiful thing about this setup is that your Lambda function is completely isolated from the public internet, yet it can still access AWS services securely and efficiently through VPC endpoints. This pattern works for many other AWS services too - S3, DynamoDB, SNS, SQS, and more!

## What's Next?

Now that you have a Lambda function successfully accessing Secrets Manager through a VPC endpoint, you might want to:

1. **Connect to an RDS database** - Use the secrets retrieved here to connect to a database in private subnets (hint: that's our next tutorial!)
2. **Add more VPC endpoints** - Set up endpoints for other services your Lambda might need
3. **Implement secret rotation** - Use Lambda to automatically rotate your database credentials
4. **Set up monitoring** - Add CloudWatch dashboards and alarms to monitor your private infrastructure

In our next tutorial, we'll create an RDS database in private subnets and use this Lambda function to connect to it using the credentials we retrieve from Secrets Manager. It's going to be a complete private, secure database access pattern!

## References

- [AWS Lambda VPC Configuration](https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html)
- [VPC Endpoints for Lambda](https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc-endpoints.html)
- [AWS Secrets Manager with VPC Endpoints](https://docs.aws.amazon.com/secretsmanager/latest/userguide/vpc-endpoint-overview.html)
- [Lambda Execution Role Permissions](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html)
- [Troubleshooting Lambda VPC Configuration](https://docs.aws.amazon.com/lambda/latest/dg/troubleshooting-networking.html)
- [Best Practices for Lambda in VPC](https://aws.amazon.com/blogs/compute/announcing-improved-vpc-networking-for-aws-lambda-functions/)
