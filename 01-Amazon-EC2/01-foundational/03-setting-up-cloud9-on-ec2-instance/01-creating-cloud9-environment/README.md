# Setting Up AWS Cloud9 Environment

Welcome to the setup guide for AWS Cloud9 using the AWS Management Console. This README will guide you through creating a Cloud9 environment, configuring it with an EC2 instance, and ensuring you're ready to start developing on this powerful cloud-based IDE.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Access the Cloud9 Service](#access-the-cloud9-service)
- [Create a New Environment](#create-a-new-environment)
- [Configure EC2 Instance Settings](#configure-ec2-instance-settings)
- [Configure Network Settings](#configure-network-settings)
- [Review and Create](#review-and-create)
- [Start Using Cloud9](#start-using-cloud9)
- [Key Points](#key-points)
- [Conclusion](#conclusion)
- [References](#references)

## Prerequisites

- An active AWS account.
- Basic familiarity with AWS services.

## Access the Cloud9 Service

1. Log in to your AWS Management Console.
2. Navigate to the "Services" menu and select "Cloud9" under "Developer Tools".

## Create a New Environment

1. Click on the "Create environment" button.
2. Enter a name for your environment, such as `Sandbox`.
3. Optionally, provide a description.

## Configure EC2 Instance Settings

1. Choose "Create a new EC2 instance for environment (direct access)".
2. Select the "t2.micro" instance type.
3. Choose "Ubuntu Server 22.04 LTS" as the platform.
4. Set the cost-saving feature to define the idle time before stopping the instance automatically.

## Configure Network Settings

1. Ensure your EC2 instance is within the default VPC.
2. Use a public subnet for the instance.
3. Verify that the subnet’s settings include "Enable auto-assign public IPv4 address". This setting allows your EC2 instance to be accessed from the internet, which is crucial for Cloud9.

## Review and Create

1. Review all the settings to ensure they are correct.
2. Click "Next Step", then review your settings again and click "Create environment".

## Start Using Cloud9

- Once the environment is set up, the Cloud9 IDE will open in your browser.
- Explore the IDE features including the code editor, debugger, and terminal.

## Key Points

- Ensure the instance is associated with a security group that allows necessary traffic (HTTP, HTTPS, SSH).
- Confirm that your environment is in a public subnet with "Auto-assign Public IP" enabled if internet access is needed.

## Conclusion

You now have a fully functional AWS Cloud9 environment set up via the AWS Management Console. This setup provides a flexible and efficient platform for developing applications in the cloud.

## References

- [AWS Cloud9 User Guide](https://docs.aws.amazon.com/cloud9/)
- [AWS EC2 User Guide for Linux Instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)