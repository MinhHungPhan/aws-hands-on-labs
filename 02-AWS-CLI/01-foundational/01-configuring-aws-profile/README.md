# Configuring AWS Profile

Welcome to the AWS Profile Configuration Guide! This document aims to simplify the process of managing multiple AWS accounts by guiding you through the creation and usage of AWS CLI profiles. Whether you're a developer, a system administrator, or just starting out with AWS, understanding how to efficiently switch between accounts can greatly enhance your workflow and project management. Let's dive into the essentials of setting up additional AWS profiles, ensuring you have the knowledge to manage your accounts effectively.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Configuring a New AWS Profile](#configuring-a-new-aws-profile)
   - [Install AWS CLI](#install-aws-cli)
   - [Create a New Profile](#create-a-new-profile)
   - [Verify Configuration](#verify-configuration)
   - [Viewing the Files](#viewing-the-files)
   - [Editing the Files](#editing-the-files)
- [Using the New Profile](#using-the-new-profile)
- [Best Practices](#best-practices)
- [Key Takeaways](#key-takeaways)
- [Conclusion](#conclusion)
- [References](#references)

### Introduction

The ability to manage multiple AWS accounts efficiently is crucial for individuals and organizations working on various projects or environments. This guide focuses on setting up AWS CLI profiles, a powerful feature that allows users to switch between accounts quickly and securely. By following this guide, you will learn how to configure, verify, and use additional AWS profiles.

### Prerequisites

- AWS account(s)
- Basic knowledge of terminal or command prompt usage
- AWS CLI installed on your machine

### Configuring a New AWS Profile

#### Install AWS CLI

Before setting up a new profile, ensure the AWS CLI is installed on your system. You can download it from the official AWS website by visiting [AWS CLI installation instructions](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and follow the detailed steps for your operating system.

#### Create a New Profile

To create a new profile, open your terminal or command prompt and execute the following command, replacing `mynewprofile` with your desired profile name:

```sh
aws configure --profile mynewprofile
```

You'll be prompted to enter:
- **AWS Access Key ID**: Your access key.
- **AWS Secret Access Key**: Your secret key.
- **Default region name**: Preferred AWS region (e.g., `us-east-1`).
- **Default output format**: Preferred output format (e.g., `json`).

**Example**:

```sh
aws configure --profile mynewprofile
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-east-1
Default output format [None]: json
```

#### Verify Configuration

Check the `~/.aws/credentials` and `~/.aws/config` files to ensure your new profile is correctly set up. You can edit these files directly for any adjustments.

1. **Navigate to the AWS Folder**: The configuration and credentials files are located in the `.aws` directory within your user's home directory. You can navigate to this directory with the following command:

```sh
cd ~/.aws
```

2. **List Files**: To see the files in the directory, you can use the `ls` command:

```sh
ls
```

You should see `credentials` and `config` files listed.

#### Viewing the Files

1. **View the Credentials File**: Use a text editor or a command like `cat` to view the contents of the `credentials` file. This file stores your access keys.

```sh
cat credentials
```

Example output:

```
[default]
aws_access_key_id = YOUR_DEFAULT_ACCESS_KEY
aws_secret_access_key = YOUR_DEFAULT_SECRET_KEY
[mynewprofile]
aws_access_key_id = YOUR_NEW_ACCESS_KEY
aws_secret_access_key = YOUR_NEW_SECRET_KEY
```

2. **View the Config File**: Similarly, view the `config` file to check region and output format settings.

```sh
cat config
```

Example output:

```
[default]
region = us-east-1
output = json
[profile mynewprofile]
region = eu-west-1
output = text
```

#### Editing the Files

If you need to make any changes to these files, you can do so using a text editor. For example, to edit the `credentials` file, you could use `vi` or another editor of your choice:

```sh
vi credentials
```

Make your changes, save, and exit the editor. Repeat the process for the `config` file if needed:

```sh
vi config
```

### Using the New Profile

To use the new profile, append `--profile mynewprofile` to your AWS CLI commands:

```sh
aws s3 ls --profile mynewprofile
```

This command lists S3 buckets under the account associated with `mynewprofile`.

### Best Practices

- **Security**: Regularly rotate your AWS Access Keys and keep your credentials file secure.
- **Naming Conventions**: Use descriptive names for your profiles to easily remember their associated accounts or purposes.
- **Permissions**: Ensure that the IAM user has the necessary permissions for the intended tasks.

### Key Takeaways

- AWS CLI profiles enable the management of multiple AWS accounts.
- Profiles are configured using `aws configure --profile`.
- Security and naming conventions are crucial for efficient profile management.

### Conclusion

Managing multiple AWS accounts doesn't have to be complex. By leveraging AWS CLI profiles, you can streamline your workflow, enhance security, and switch between accounts with ease. Remember to follow best practices for naming and security to maintain an efficient and secure environment.

### References

- [Configure the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
- [Install or update to the latest version of the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Configuration and credential file settings](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
- [AWS Security Best Practices](https://aws.amazon.com/architecture/well-architected/)