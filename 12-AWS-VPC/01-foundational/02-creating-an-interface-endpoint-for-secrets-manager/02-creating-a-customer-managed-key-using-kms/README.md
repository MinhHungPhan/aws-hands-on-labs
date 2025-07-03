# Creating a Customer Managed Key using KMS

Alright, so we've got our VPC Interface Endpoint set up from the previous tutorial - nice work! Now, before we start storing secrets and spinning up Lambda functions, we need to talk about encryption. And when it comes to encryption in AWS, that means AWS Key Management Service (KMS). 

In this tutorial, we're going to create a customer managed KMS key that we'll use to encrypt our secrets in AWS Secrets Manager. Why not just use the default AWS managed key? Great question! I'll explain that and walk you through creating your own key that gives you complete control over your encryption.

## Table of Contents

- [Introduction](#introduction)
- [Why Create Your Own KMS Key?](#why-create-your-own-kms-key)
- [Understanding KMS Key Types](#understanding-kms-key-types)
- [Step-by-Step Guide](#step-by-step-guide)
- [Understanding Key Policies](#understanding-key-policies)
- [Testing Your KMS Key](#testing-your-kms-key)
- [Key Rotation and Management](#key-rotation-and-management)
- [Best Practices](#best-practices)
- [Troubleshooting Common Issues](#troubleshooting-common-issues)
- [Cost Considerations](#cost-considerations)
- [Key Takeaways](#key-takeaways)
- [What's Next?](#whats-next)
- [References](#references)

## Introduction

You know what I love about AWS KMS? It takes something as complex as encryption key management and makes it... well, actually pretty straightforward once you understand the basics. Think of KMS as your personal bodyguard for data - it protects your sensitive information and only lets the right people access it.

We're creating this customer managed key because in our upcoming tutorials, we'll be storing database credentials in Secrets Manager, and we want full control over who can encrypt and decrypt those secrets. Plus, it's just good security practice to own your encryption keys when dealing with sensitive data.

## Why Create Your Own KMS Key?

I get this question a lot: "Why not just use the default AWS managed key?" Here's the thing - AWS managed keys are convenient, but they're like using a shared locker at the gym. Sure, it works, but you don't control who else might have access.

### Benefits of Customer Managed Keys:

- **Complete control** - You decide who can use the key, when, and for what
- **Custom key policies** - Set up fine-grained permissions that match your security requirements
- **Audit trail** - CloudTrail logs every single use of your key (great for compliance!)
- **Key rotation** - You control when and how the key gets rotated
- **Cross-account access** - Share the key with other AWS accounts if needed
- **Deletion control** - You can disable or schedule deletion of the key

### When AWS Managed Keys Are Fine:

- **Quick prototyping** - When you're just testing things out
- **Simple use cases** - Single service, single account scenarios
- **Cost sensitivity** - AWS managed keys are free (though you pay for API calls)

For our tutorial series, we're building a production-ready setup, so customer managed keys are definitely the way to go!

## Understanding KMS Key Types

Before we dive into creating our key, let's quickly cover the different types of KMS keys:

### Symmetric Keys
- **What they are**: Single key used for both encryption and decryption
- **Best for**: Most use cases including Secrets Manager, S3, EBS
- **Performance**: Fast and efficient
- **This is what we'll create today!**

### Asymmetric Keys
- **What they are**: Key pair (public/private) for encryption or digital signing
- **Best for**: Cross-account encryption, digital signatures
- **Performance**: Slower than symmetric keys
- **Use case**: When you need to encrypt data outside of AWS

### HMAC Keys
- **What they are**: Keys for generating Hash-based Message Authentication Codes
- **Best for**: Verifying data integrity and authenticity
- **Use case**: API authentication, data verification

For our Secrets Manager use case, we definitely want a symmetric key - it's perfect for encrypting secrets that will be decrypted by our Lambda functions.

## Step-by-Step Guide

Alright, let's get our hands dirty and create this KMS key! The process is pretty straightforward, but there are some important decisions to make along the way.

### Step 1: Navigate to KMS

1. Log into the AWS Management Console
2. Head over to **Key Management Service (KMS)**
3. Make sure you're in the right region (the same one where you created your VPC endpoint)
4. Click on **Customer managed keys** in the left sidebar

### Step 2: Create the Key

1. Click that big **Create key** button
2. For key type, select **Symmetric** (this is what we want for Secrets Manager)
3. For key usage, keep it as **Encrypt and decrypt** (the default)
4. For key material origin, choose **KMS** - this means AWS generates the key material for us
5. For regionality, select **Single-Region key** (unless you specifically need multi-region, which is more expensive)
6. Click **Next**

### Step 3: Add Labels and Description

This step is more important than it looks! Good naming and descriptions will save you headaches later.

1. **Alias**: Give your key a meaningful alias like `secrets-manager-encryption-key` or `vpc-tutorial-kms-key`
   
   💡 **Pro tip**: Aliases are much easier to remember than the actual key IDs, and you can use them in policies and API calls.

2. **Description**: Write something descriptive like "Customer managed key for encrypting secrets in the VPC tutorial series"

3. **Tags**: Add some tags to help with organization and cost tracking:
   - `Environment`: `tutorial` or `dev`
   - `Project`: `vpc-endpoints-tutorial`
   - `Purpose`: `secrets-encryption`

4. Click **Next**

### Step 4: Define Key Administrative Permissions

This is where we decide who can manage the key itself (not who can use it for encryption/decryption).

1. **Key administrators**: Select your IAM user or role. These people can:
   - Modify the key policy
   - Enable/disable the key
   - Schedule key deletion
   - View key details

2. **Key deletion**: I recommend checking the box that says "Allow key administrators to delete this key" - you'll want this flexibility for testing and cleanup

3. Click **Next**

### Step 5: Define Key Usage Permissions

Now we're deciding who can actually use the key to encrypt and decrypt data.

1. **This key can be used by**: Here's where it gets interesting. You'll want to add:
   - **Your IAM user** (so you can test the key)
   - **Lambda execution roles** (for our upcoming Lambda tutorial)
   - **AWS services** that need to use the key on your behalf

2. **Services integrated with KMS**: Make sure to select:
   - **AWS Secrets Manager** (this is crucial for our tutorial!)
   - **AWS Lambda** (for our upcoming Lambda functions)

3. Click **Next**

### Step 6: Review the Key Policy

This is where AWS shows you the JSON policy it's creating based on your selections. It's worth taking a look at this because understanding key policies is super important.

I've included a complete key policy file in this repository (`policies/kms-key-policy.json`) that shows exactly what you'll need for our tutorial series. The policy will look something like this:

```json
{
    "Version": "2012-10-17",
    "Id": "key-consolepolicy-3",
    "Statement": [
        {
            "Sid": "Enable IAM User Permissions",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::YOUR-ACCOUNT-ID:root"
            },
            "Action": "kms:*",
            "Resource": "*"
        },
        {
            "Sid": "Allow Lambda Full Access from account YOUR-ACCOUNT-ID",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::YOUR-ACCOUNT-ID:role/service-role/your-lambda-role-name"
            },
            "Action": "kms:*",
            "Resource": "*"
        },
        {
            "Sid": "AllowSecretsManagerToUseKey",
            "Effect": "Allow",
            "Principal": {
                "Service": "secretsmanager.amazonaws.com"
            },
            "Action": "kms:*",
            "Resource": "*"
        }
    ]
}
```

**What's happening here?**
- **Root permissions**: Your AWS account root always has full access (this is standard and recommended)
- **Lambda role permissions**: The specific Lambda execution role that will decrypt secrets gets full access to the key
- **Secrets Manager service permissions**: AWS Secrets Manager itself needs access to encrypt/decrypt secrets on your behalf

**Important notes:**
- Replace `YOUR-ACCOUNT-ID` with your actual AWS account ID
- Replace `your-lambda-role-name` with the actual name of your Lambda execution role (note the `service-role/` path - this appears when AWS auto-creates the role for you)
- The `kms:*` permissions are broad for tutorial purposes - in production, you'd typically restrict these to specific actions like `kms:Decrypt`, `kms:GenerateDataKey`, etc.

### Step 7: Save Your Key Information

Once the key is created, you'll see a success message with your key details. **Make sure to save this information:**

- **Key ID**: Something like `1234abcd-12ab-34cd-56ef-1234567890ab`
- **Key ARN**: `arn:aws:kms:region:account-id:key/key-id`
- **Alias**: The friendly name you gave it

You'll need this information for the next tutorials in our series!

## Understanding Key Policies

Let me break down key policies in simple terms, because they're actually pretty important to understand.

### Key Policy vs IAM Policy

Think of it this way:
- **Key policies** are like the lock on your front door - they control who can even approach the key
- **IAM policies** are like the permissions people have once they're inside - they control what actions they can perform

Both need to allow access for someone to use your KMS key. It's an AND operation, not an OR.

### Common Key Policy Patterns

**Allow a specific role to use the key:**

```json
{
    "Sid": "AllowLambdaRole",
    "Effect": "Allow",
    "Principal": {
        "AWS": "arn:aws:iam::YOUR-ACCOUNT:role/lambda-secrets-role"
    },
    "Action": [
        "kms:Decrypt",
        "kms:GenerateDataKey"
    ],
    "Resource": "*"
}
```

**Allow Secrets Manager to use the key:**

```json
{
    "Sid": "AllowSecretsManagerAccess",
    "Effect": "Allow",
    "Principal": {
        "Service": "secretsmanager.amazonaws.com"
    },
    "Action": [
        "kms:Decrypt",
        "kms:GenerateDataKey"
    ],
    "Resource": "*"
}
```

## Testing Your KMS Key

Let's make sure our key is working properly! We can do a quick test using the AWS CLI, AWS CloudShell or console.

### Testing via AWS CloudShell

1. **Encrypt some test data:**

First, let's create a test file with some realistic content:

```bash
# Create a test file with secret content
echo "This is a decrypted secret" > plaintext.txt

# Check the content
cat plaintext.txt
```

Now encrypt the file using your KMS key:

```bash
# Encrypt the file content
aws kms encrypt \
    --key-id alias/your-key-alias \
    --plaintext fileb://plaintext.txt \
    --output text \
    --query CiphertextBlob > encrypted-data.txt

# Check the encrypted content (should be base64-encoded ciphertext)
cat encrypted-data.txt
```

2. **Decrypt the data:**

Now let's decrypt the data using a streamlined one-liner command:

```bash
# Decrypt the data in one command using process substitution
aws kms decrypt \
    --ciphertext-blob fileb://<(base64 -d encrypted-data.txt) \
    --output text \
    --query Plaintext | base64 --decode > decrypted-data.txt

# Check the decrypted content
cat decrypted-data.txt
```

You should see your original message: "This is a decrypted secret"

### Testing via Console

1. Go to your KMS key in the console
2. Click on the **Key ID** to open the details
3. In the **General configuration** section, you should see the key is **Enabled**
4. Check the **Key usage** section - it should show recent activity once you start using it

## Key Rotation and Management

One of the best things about customer managed keys is that you control rotation. Here's what you need to know:

### Automatic Key Rotation

1. In your KMS key details, look for **Key rotation**
2. You can enable automatic rotation (recommended for production)
3. AWS will rotate the key material annually
4. **Important**: The key ID and ARN stay the same, so your applications don't break

### Manual Key Rotation

Sometimes you might want to rotate keys manually:
- When you suspect the key might be compromised
- To meet specific compliance requirements
- For testing purposes

### Key Lifecycle Management

Your key can be in several states:
- **Enabled**: Normal operation, can encrypt/decrypt
- **Disabled**: Temporarily suspended, can only decrypt existing data
- **Pending deletion**: 7-30 day waiting period before permanent deletion
- **Scheduled for deletion**: Will be deleted on a specific date

💡 **Pro tip**: Never delete a key unless you're absolutely sure no data is encrypted with it. Deleted keys = permanently inaccessible data!

## Best Practices

Here are some hard-learned lessons about KMS keys:

### Security Best Practices

- **Principle of least privilege**: Only give the minimum permissions needed
- **Separate keys for different purposes**: Don't use the same key for everything
- **Regular access reviews**: Periodically check who has access to your keys
- **Enable CloudTrail**: Log all key usage for auditing
- **Use grants for temporary access**: Instead of modifying policies for short-term access

### Operational Best Practices

- **Meaningful aliases**: Use descriptive names like `prod-secrets-key` instead of `my-key`
- **Consistent tagging**: Tag all your keys with environment, project, and purpose
- **Document key purposes**: Keep a record of what each key is used for
- **Test key access**: Regularly verify that your applications can use the keys
- **Plan for key rotation**: Have a process for rotating keys and updating applications

### Cost Optimization

- **Regional keys**: Use single-region keys unless you specifically need multi-region
- **Monitor usage**: Set up CloudWatch alarms for unusual key usage patterns
- **Clean up unused keys**: Delete keys that are no longer needed (after the waiting period)
- **Consider AWS managed keys**: For simple use cases, they might be sufficient

## Troubleshooting Common Issues

Here are the most common problems I've encountered with KMS keys:

### "Access Denied" when using the key

**Problem**: You get an access denied error when trying to encrypt/decrypt.

**Solution**: Check both the key policy AND your IAM permissions. Both need to allow the action.

### "Key not found" errors

**Problem**: Your application can't find the key.

**Solution**: 
- Verify you're using the correct key ID or alias
- Make sure you're in the right AWS region
- Check that the key hasn't been disabled or deleted

### Lambda function can't decrypt secrets

**Problem**: Your Lambda function gets permission errors when accessing encrypted secrets.

**Solution**: 
- Add the Lambda execution role to the key policy
- Ensure the role has `kms:Decrypt` permissions
- Verify the key is in the same region as your Lambda

## Cost Considerations

Let's talk money - because KMS costs can add up if you're not careful:

### Key Storage Costs
- **Customer managed keys**: $1/month per key
- **AWS managed keys**: Free (but you pay for API calls)

### API Call Costs
- **Free tier**: 20,000 requests per month
- **After free tier**: $0.03 per 10,000 requests

### Optimization Tips
- **Cache decrypted values**: Don't decrypt the same secret over and over
- **Use envelope encryption**: For large data, encrypt a data key instead of the data itself
- **Monitor usage**: Set up billing alerts for KMS costs

For our tutorial series, the costs will be minimal - probably just a few dollars per month at most.

## Key Takeaways

Let's wrap up what we've accomplished:

- ✅ Created a customer managed KMS key for encrypting secrets
- ✅ Configured proper permissions for our upcoming Lambda functions
- ✅ Set up key policies that follow security best practices
- ✅ Established a foundation for secure secret management
- ✅ Prepared for automatic key rotation

The beautiful thing about having your own KMS key is that you're now in complete control of your encryption. No more wondering who else might have access to your secrets!

## What's Next?

Now that we have our KMS key set up, we're ready to move on to the next step in our tutorial series:

1. **Create secrets in Secrets Manager** - We'll use our shiny new KMS key to encrypt database credentials
2. **Create Lambda functions** - These will use our KMS key to decrypt secrets
3. **Set up RDS database** - The target for our secure connection
4. **Test the complete flow** - End-to-end verification that everything works together

Our next tutorial will show you how to create secrets in AWS Secrets Manager using the KMS key we just created. We'll store database credentials that our Lambda function will retrieve later in the series.

## References

- [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/)
- [Key Policies in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html)
- [AWS KMS Best Practices](https://docs.aws.amazon.com/kms/latest/developerguide/best-practices.html)
- [AWS KMS Access Control Overview](https://docs.aws.amazon.com/kms/latest/developerguide/control-access-overview.html)
- [Default key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-default.html)
- [KMS Key Rotation](https://docs.aws.amazon.com/kms/latest/developerguide/rotating-keys.html)
- [AWS KMS Pricing](https://aws.amazon.com/kms/pricing/)
- [Using KMS with AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/security-encryption.html)
- [Troubleshooting KMS](https://docs.aws.amazon.com/kms/latest/developerguide/troubleshooting.html)
