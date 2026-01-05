# Creating a Secret using Secrets Manager

Perfect! So you've got your VPC Interface Endpoint set up and your shiny new customer managed KMS key ready to go. Now comes the fun part - actually storing some secrets! Think of this tutorial as putting your security infrastructure to work. We're going to create and store database credentials in AWS Secrets Manager using the KMS key we created in the previous tutorial.

You know what I love about this step? It's where everything starts clicking together. We're not just storing passwords in plain text somewhere (please tell me you're not doing that!). Instead, we're using enterprise-grade encryption and access controls to protect sensitive information. By the end of this tutorial, you'll have a secure secret that your Lambda functions can retrieve without ever exposing credentials in your code.

## Table of Contents

- [Introduction](#introduction)
- [Why Use AWS Secrets Manager?](#why-use-aws-secrets-manager)
- [Understanding Secret Types](#understanding-secret-types)
- [Prerequisites](#prerequisites)
- [Step-by-Step Guide](#step-by-step-guide)
- [Understanding Secret Policies](#understanding-secret-policies)
- [Testing Secret Access](#testing-secret-access)
- [Secret Rotation Setup](#secret-rotation-setup)
- [Integration with Other Services](#integration-with-other-services)
- [Best Practices](#best-practices)
- [Troubleshooting Common Issues](#troubleshooting-common-issues)
- [Cost Considerations](#cost-considerations)
- [Key Takeaways](#key-takeaways)
- [What's Next?](#whats-next)
- [References](#references)

## Introduction

AWS Secrets Manager is like a digital vault for your sensitive information. Instead of hardcoding database passwords, API keys, or other credentials in your applications, you store them securely in Secrets Manager and let your applications retrieve them at runtime.

The beauty of this approach? Your secrets are encrypted at rest using your customer managed KMS key, encrypted in transit, and you can control exactly who and what can access them. Plus, Secrets Manager can automatically rotate your secrets on a schedule, which is a security best practice that's honestly a pain to implement manually.

In this tutorial, we're going to create a database secret that contains connection credentials for an RDS database. Even though we haven't created the database yet (that's coming in a future tutorial), setting up the secret now will streamline our workflow later.

## Why Use AWS Secrets Manager?

Let me paint you a picture of the old way versus the AWS way:

### The Old Way (Please Don't Do This):

```python
# DON'T DO THIS!
DB_HOST = "mydb.cluster-abc123.us-east-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PASSWORD = "super-secret-password-123"  # Ouch!
```

### The AWS Secrets Manager Way:

```python
# Much better!
import boto3
import json

def get_secret():
    secret_name = "vpc-tutorial/database/credentials"
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

credentials = get_secret()
```

### Benefits of Secrets Manager:

- **No hardcoded credentials** - Secrets live outside your code
- **Encryption at rest and in transit** - Using your KMS key
- **Automatic rotation** - Set it and forget it
- **Fine-grained access control** - Control who can read which secrets
- **Audit trail** - CloudTrail logs every secret access
- **Integration with RDS** - Can automatically manage database credentials
- **Versioning** - Keep track of secret changes
- **Cross-region replication** - Replicate secrets across regions if needed

### When You Might Skip Secrets Manager:

- **Very simple, single-use scripts** - But even then, it's often worth it
- **Cost-sensitive projects** - Though the security benefits usually justify the cost
- **Air-gapped environments** - Where you can't reach AWS APIs

For our VPC tutorial series, Secrets Manager is definitely the right choice. We're building a production-ready architecture, and hardcoded credentials would be a major security vulnerability.

## Understanding Secret Types

Secrets Manager supports different types of secrets, and choosing the right type affects how you create and manage them:

### Database Secrets
- **What they are**: Structured credentials for databases
- **Best for**: RDS, Aurora, Redshift, DocumentDB
- **Features**: Automatic rotation, integration with database services
- **Format**: JSON with standardized fields like `username`, `password`, `host`, `port`
- **This is what we'll create today!**

### API Key Secrets
- **What they are**: Simple key-value pairs or plain text
- **Best for**: Third-party API keys, service tokens
- **Features**: Manual rotation, simple retrieval
- **Format**: Plain text or simple JSON

### Other Credentials
- **What they are**: Any other sensitive information
- **Best for**: SSH keys, certificates, complex configurations
- **Features**: Flexible format, manual management
- **Format**: Whatever you need

For our tutorial, we're creating a database secret because we'll eventually connect to an RDS database, and this type gives us the best integration and automatic rotation capabilities.

## Prerequisites

Before we dive in, make sure you have:

### From Previous Tutorials:
- ✅ **VPC Interface Endpoint** - Set up in the first tutorial
- ✅ **Customer Managed KMS Key** - Created in the previous tutorial
- ✅ **KMS Key alias** - Something like `alias/vpc-tutorial-kms-key`

### AWS Access:
- ✅ **AWS Console access** - With appropriate permissions
- ✅ **AWS CLI configured** - For testing (optional but recommended)

### Information You'll Need:
- **Your KMS key alias** - From the previous tutorial
- **AWS region** - Same region as your VPC endpoint and KMS key
- **Secret name** - We'll use `vpc-tutorial/database/credentials`

Don't worry if you don't have an actual database yet - we're creating the secret structure now and we'll populate it with real values when we set up RDS in a future tutorial.

## Step-by-Step Guide

Alright, let's create our first secret! The process is straightforward, but there are some important decisions to make along the way.

### Step 1: Navigate to Secrets Manager

1. Log into the AWS Management Console
2. Search for **Secrets Manager** in the services search bar
3. Make sure you're in the same region as your VPC endpoint and KMS key
4. You should see the Secrets Manager dashboard

💡 **Pro tip**: If this is your first time in Secrets Manager, you might see a welcome screen with some helpful information. Take a quick look - it's actually pretty useful!

### Step 2: Start Creating the Secret

1. Click the **Store a new secret** button
2. You'll see several secret type options. For our use case, select **Credentials for Amazon RDS database**
3. This gives us the proper JSON structure for database credentials

### Step 3: Configure Secret Details

Now we need to fill in the secret information:

**Username**: Enter `dbadmin` (or whatever you prefer for your database admin user)

**Password**: You have a few options here:
- **Generate password** (recommended) - Let AWS create a strong password
- **Provide password** - Enter your own password

I recommend using the generated password. Click **Generate password** and you'll see options for password complexity:
- **Password length**: Keep the default (32 characters is good)
- **Exclude characters**: You might want to exclude similar characters like `0`, `O`, `l`, `1`
- **Exclude punctuation**: I usually leave this unchecked for maximum security

**Encryption key**: This is the important part! Instead of using the default AWS managed key, select **Choose an encryption key** and pick your customer managed key:
- Select your KMS key alias (something like `alias/vpc-tutorial-kms-key`)

**Database**: For now, select **I will choose the database later** since we haven't created our RDS instance yet.

### Step 4: Configure Secret Information

1. **Secret name**: Use a clear, hierarchical naming convention like:

```sh
vpc-tutorial/database/credentials
```

This naming pattern makes it easy to organize secrets and set up IAM policies.

2. **Description**: Add something helpful like:

```sh
Database credentials for the VPC tutorial series RDS instance
```

3. **Tags**: Add tags for organization and cost tracking:

- `Environment`: `tutorial`
- `Project`: `vpc-endpoints-tutorial`
- `Purpose`: `database-credentials`
- `CreatedBy`: Your name or team

### Step 5: Configure Automatic Rotation (Optional)

For this tutorial, we'll skip automatic rotation to keep things simple, but let me explain the options:

- **Disable automatic rotation** - We'll choose this for now
- **Enable automatic rotation** - You can set this up later when you have an actual database

💡 **Why skip rotation for now?** Automatic rotation requires a Lambda function that can connect to your database and change the password. Since we don't have a database yet, we'll set this up in a later tutorial.

### Step 6: Review and Create

Review your settings:
- **Secret type**: Credentials for Amazon RDS database
- **Encryption**: Your customer managed KMS key
- **Name**: `vpc-tutorial/database/credentials`
- **Rotation**: Disabled (for now)

Click **Store** to create your secret!

### Step 7: Verify Secret Creation

Once created, you should see:
- **Secret ARN**: Something like `arn:aws:secretsmanager:region:account:secret:vpc-tutorial/database/credentials-AbCdEf`
- **Status**: The secret should show as active
- **Encryption**: Should show your KMS key

**Save this information** - you'll need the secret name/ARN for the next tutorials!

## Understanding Secret Policies

Just like KMS keys, secrets can have resource-based policies that control who can access them. Let's understand how this works:

### Default Secret Access

By default, your secret is accessible to:
- **Your AWS account root** - Full access
- **IAM users/roles with appropriate permissions** - Based on IAM policies

### When You Need Secret Policies

You typically add secret policies when you need to:
- **Grant cross-account access** - Let another AWS account access the secret
- **Restrict access further** - Add additional conditions beyond IAM
- **Grant access to AWS services** - Like Lambda functions in different accounts

### Example Secret Policy

Here's what a basic secret policy might look like for granting Lambda access:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowLambdaAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::YOUR-ACCOUNT-ID:role/service-role/your-lambda-role-name"
      },
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "*"
    }
  ]
}
```

I've included a complete secret policy file in this repository (`policies/secret-manager-resource-policy.json`) that shows exactly what you'll need for our upcoming Lambda tutorial. This policy:

- **Grants GetSecretValue permission** - Allows the Lambda role to retrieve secret values
- **Uses service-role/ path** - The standard path for AWS-created Lambda execution roles
- **Applies to all resources** - The `"Resource": "*"` means this policy applies to any secret

**Important notes:**
- Replace `YOUR-ACCOUNT-ID` with your actual AWS account ID
- Replace `your-lambda-role-name` with the actual name of your Lambda execution role
- The `service-role/` path appears when AWS auto-creates the role for you
- You could restrict the `Resource` to specific secret ARNs for tighter security

**For our tutorial**, we don't need a custom secret policy yet. The default access combined with IAM policies will work perfectly for our Lambda functions. However, understanding how secret policies work will be helpful when we create more complex architectures later.

## Testing Secret Access

Let's make sure our secret is working properly and that we can retrieve it:

### Testing via AWS Console

1. **View the secret**: In Secrets Manager, click on your secret name
2. **Check the overview**: Verify the encryption key, tags, and other details
3. **Retrieve secret value**: Click **Retrieve secret value** to see the stored credentials
   - You should see JSON with `username`, `password`, and other fields
   - This proves the secret is properly encrypted and decryptable

### Testing via AWS CLI

If you have the AWS CLI set up, here's how to test programmatically:

```bash
# Retrieve the secret value
aws secretsmanager get-secret-value \
    --secret-id vpc-tutorial/database/credentials \
    --region your-region

# Pretty print just the secret string
aws secretsmanager get-secret-value \
    --secret-id vpc-tutorial/database/credentials \
    --query SecretString \
    --output text | jq .
```

You should see output like:

```json
{
  "username": "dbadmin",
  "password": "your-generated-password",
  "engine": "mysql",
  "host": "localhost",
  "port": 3306,
  "dbInstanceIdentifier": "vpc-tutorial-db"
}
```

**Note**: Some fields like `host` might be placeholder values until we create the actual database.

### Testing via AWS CloudShell

AWS CloudShell is a great way to test without setting up the CLI locally:

1. **Open CloudShell**: Click the CloudShell icon in the AWS console
2. **Run the same CLI commands** as above
3. **Verify you can retrieve the secret** - This confirms your permissions are correct

## Secret Rotation Setup

While we're not enabling rotation right now, let me explain how it works so you understand the complete picture:

### How Automatic Rotation Works

1. **Secrets Manager schedules rotation** - Based on your chosen interval (30, 60, 90 days, etc.)
2. **Lambda function gets triggered** - AWS invokes a rotation function
3. **New credentials get created** - The function creates new database credentials
4. **Database gets updated** - The function updates the database with new credentials
5. **Secret gets updated** - Secrets Manager stores the new credentials
6. **Old credentials get cleaned up** - After verification, old credentials are removed

### Rotation Requirements

To enable rotation, you need:
- **A database** - The actual RDS instance (we'll create this later)
- **A Lambda function** - To perform the rotation (AWS provides templates)
- **Network connectivity** - Lambda must be able to reach the database
- **Proper permissions** - Lambda needs permissions to modify database users

### Setting Up Rotation Later

When we create our RDS database in a future tutorial, we'll come back and enable rotation. The process will be:

1. **Create the RDS instance** - With our VPC and security groups
2. **Deploy the rotation Lambda** - Using AWS-provided templates
3. **Configure network access** - Ensure Lambda can reach the database
4. **Enable rotation** - Set the schedule and test it

For now, just remember that this capability exists - it's one of the major advantages of using Secrets Manager over simple parameter store values.

## Integration with Other Services

One of the best things about Secrets Manager is how well it integrates with other AWS services:

### Lambda Functions
```python
import boto3
import json

def lambda_handler(event, context):
    # Retrieve database credentials
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId='vpc-tutorial/database/credentials')
    secret = json.loads(response['SecretString'])
    
    # Use the credentials
    db_host = secret['host']
    db_user = secret['username']
    db_password = secret['password']
```

### RDS Integration
- **Automatic management** - Secrets Manager can manage RDS master passwords
- **Rotation support** - Built-in rotation for RDS instances
- **Connection strings** - Automatically formatted connection information

### ECS/Fargate

```json
{
  "secrets": [
    {
      "name": "DB_PASSWORD",
      "valueFrom": "arn:aws:secretsmanager:region:account:secret:vpc-tutorial/database/credentials:password::"
    }
  ]
}
```

### CloudFormation/CDK

```yaml
Resources:
  MySecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: vpc-tutorial/database/credentials
      KmsKeyId: !Ref MyKMSKey
```

The integration possibilities are extensive, and we'll use several of these in upcoming tutorials.

## Best Practices

Here are some hard-learned lessons about managing secrets effectively:

### Security Best Practices

- **Use customer managed KMS keys** - Better control and audit capabilities
- **Principle of least privilege** - Only grant access to secrets that are absolutely needed
- **Enable rotation** - Regularly change credentials automatically
- **Use IAM conditions** - Add time-based or IP-based restrictions when appropriate
- **Monitor access** - Set up CloudWatch alarms for unusual secret access patterns

### Naming and Organization

- **Hierarchical naming** - Use patterns like `environment/service/purpose`

```sh
prod/database/master-credentials
dev/api/third-party-keys
staging/cache/redis-auth
```

- **Consistent tagging** - Use tags for environment, cost center, owner
- **Descriptive names** - Make it obvious what the secret contains
- **Avoid sensitive info in names** - Secret names are logged in CloudTrail

### Operational Best Practices

- **Document secret purposes** - Keep a record of what each secret is for
- **Test secret access** - Regularly verify that applications can retrieve secrets
- **Plan for disasters** - Consider cross-region replication for critical secrets
- **Version management** - Use secret versions for rollback capabilities
- **Clean up unused secrets** - Delete secrets that are no longer needed

### Development Workflow

- **Environment-specific secrets** - Don't share secrets between dev/staging/prod
- **Local development** - Use AWS profiles or environment variables for local testing
- **CI/CD integration** - Securely inject secrets into deployment pipelines
- **Code reviews** - Never commit secrets to version control

## Troubleshooting Common Issues

Here are the most common problems I've encountered with Secrets Manager:

### "Access Denied" when retrieving secrets

**Problem**: You get permission errors when trying to access a secret.

**Solutions**:
1. **Check IAM permissions** - Ensure your user/role has `secretsmanager:GetSecretValue`
2. **Verify KMS permissions** - You need `kms:Decrypt` on the encryption key
3. **Check secret policy** - If there's a resource-based policy, ensure it allows access
4. **Region mismatch** - Make sure you're in the correct AWS region

### "Secret not found" errors

**Problem**: Your application can't find the secret.

**Solutions**:
1. **Check the secret name** - Case-sensitive and must be exact
2. **Verify region** - Secrets are region-specific
3. **Check secret status** - Ensure the secret isn't deleted or pending deletion
4. **ARN vs name** - You can use either, but make sure you're using the right format

### KMS decryption failures

**Problem**: Secret exists but can't be decrypted.

**Solutions**:
1. **KMS key permissions** - Verify the key policy allows decryption
2. **Key status** - Ensure the KMS key is enabled
3. **Cross-account issues** - Check both secret and KMS key policies for cross-account access

### Lambda timeout issues

**Problem**: Lambda functions timeout when retrieving secrets.

**Solutions**:
1. **VPC configuration** - If Lambda is in a VPC, ensure it can reach Secrets Manager
2. **Network connectivity** - Check security groups and NACLs
3. **VPC endpoints** - Consider using a VPC endpoint for Secrets Manager
4. **Caching** - Cache secret values to reduce API calls

### Performance concerns

**Problem**: Secret retrieval is slow or expensive.

**Solutions**:
1. **Implement caching** - Don't retrieve secrets on every request
2. **Batch operations** - Retrieve multiple secrets in one call when possible
3. **Connection reuse** - Reuse boto3 clients across Lambda invocations
4. **Monitor costs** - Set up billing alerts for Secrets Manager usage

## Cost Considerations

Let's talk about the costs associated with Secrets Manager:

### Secret Storage Costs
- **$0.40 per secret per month** - Regardless of secret size
- **Prorated daily** - You only pay for the days the secret exists
- **No free tier** - Unlike some AWS services, there's no free usage

### API Request Costs
- **$0.05 per 10,000 API requests** - This includes GetSecretValue, PutSecretValue, etc.
- **Free tier**: 10,000 API calls per month for the first 30 days

### Rotation Costs
- **Lambda function costs** - When rotation functions run
- **Additional API calls** - Rotation generates extra API requests
- **Compute costs** - If rotation Lambda needs significant compute time

### Cost Optimization Tips

- **Implement caching** - Reduce API calls by caching secret values

```python
# Cache secrets for 5 minutes
import time
secret_cache = {}

def get_cached_secret(secret_name, cache_duration=300):
    now = time.time()
    if secret_name in secret_cache:
        cached_time, cached_value = secret_cache[secret_name]
        if now - cached_time < cache_duration:
            return cached_value
    
    # Retrieve and cache
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    secret_cache[secret_name] = (now, response['SecretString'])
    return response['SecretString']
```

- **Consolidate secrets** - Store related credentials in one secret as JSON
- **Clean up unused secrets** - Delete secrets that are no longer needed
- **Monitor usage** - Set up CloudWatch alarms for unexpected API usage

### Estimated Costs for This Tutorial

For our tutorial series, expect minimal costs:
- **One secret**: ~$0.40/month
- **Testing API calls**: Likely within free tier
- **Total monthly cost**: Less than $1

The security benefits far outweigh these minimal costs for any real application.

## Key Takeaways

Let's summarize what we've accomplished and learned:

### ✅ What We Built
- **Secure database secret** - Encrypted with our customer managed KMS key
- **Proper naming structure** - Using hierarchical naming for organization
- **Future-ready setup** - Ready for automatic rotation when we add RDS
- **Integration foundation** - Set up for Lambda and other service integration

### ✅ Key Concepts Mastered
- **Secret types and structure** - Understanding database vs. API key secrets
- **Encryption integration** - How Secrets Manager uses KMS keys
- **Access control** - IAM permissions and resource policies
- **Cost management** - Understanding pricing and optimization strategies

### ✅ Security Improvements
- **No hardcoded credentials** - Eliminated a major security vulnerability
- **Encryption at rest** - Using your own KMS key for full control
- **Audit trail** - Every secret access is logged in CloudTrail
- **Access control** - Fine-grained permissions for secret access

The secret we created today forms the foundation for secure database connectivity in our Lambda functions. No more hardcoded passwords, no more security vulnerabilities from credentials in code!

## What's Next?

Now that we have our secret securely stored, we're ready for the next steps in our tutorial series:

1. **Create Lambda functions** - These will retrieve our secret and use the database credentials
2. **Set up RDS database** - Create the actual database that will use these credentials
3. **Enable automatic rotation** - Set up the Lambda function to rotate our database password
4. **Test end-to-end connectivity** - Verify the complete secure flow from Lambda to RDS
5. **Monitor and optimize** - Set up CloudWatch monitoring for the complete stack

Our next tutorial will focus on creating Lambda functions that can securely retrieve this secret and use it to connect to databases. We'll also cover VPC configuration for Lambda functions and how to ensure they can reach both Secrets Manager and our future RDS instance.

The pieces are really starting to come together - you now have a VPC endpoint for secure communication, a KMS key for encryption, and a secret for storing credentials. Next, we'll put it all to work with some actual compute!

## References

- [AWS Secrets Manager User Guide](https://docs.aws.amazon.com/secretsmanager/latest/userguide/)
- [Use AWS Secrets Manager secrets in AWS Lambda functions](https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_lambda.html)
- [Secret encryption and decryption in AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/security-encryption.html)
- [How do I resolve "KMSAccessDeniedException" errors from AWS Lambda?](https://repost.aws/knowledge-center/lambda-kmsaccessdeniedexception-errors)
- [How do I resolve AWS KMS key access errors after I tried to retrieve an encrypted Secrets Manager secret?](https://repost.aws/knowledge-center/secrets-manager-cross-account-key)
- [AWS Secrets Manager best practices](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- [Managing secrets in AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/managing-secrets.html)
- [AWS Secrets Manager pricing](https://aws.amazon.com/secrets-manager/pricing/)
- [Rotating secrets in AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html)
- [AWS Secrets Manager VPC endpoint](https://docs.aws.amazon.com/secretsmanager/latest/userguide/vpc-endpoint-overview.html)