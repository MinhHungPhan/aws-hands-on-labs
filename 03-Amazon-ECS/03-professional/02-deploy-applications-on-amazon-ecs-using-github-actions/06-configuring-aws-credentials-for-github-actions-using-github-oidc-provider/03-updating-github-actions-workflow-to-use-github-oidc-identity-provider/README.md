# Updating GitHub Actions Workflow to use GitHub OIDC Identity Provider

This README will guide you through updating your GitHub Actions workflow to use GitHub's OpenID Connect (OIDC) Identity Provider instead of traditional AWS access keys. This change enhances security by eliminating the need to store and manage long-term AWS credentials in GitHub secrets.

## Table of Contents

- [Introduction](#introduction)
- [Benefits of Using OIDC](#benefits-of-using-oidc)
- [Steps to Update the Workflow](#steps-to-update-the-workflow)
    - [Define GitHub Variables](#3-define-github-variables)
    - [Update Your GitHub Actions Workflow](#2-update-your-github-actions-workflow)
    - [Verify and Test](#4-verify-and-test)
- [Key Takeaways](#key-takeaways)
- [Best Practices](#best-practices)
- [References](#references)
- [Conclusion](#conclusion)

## Introduction

Updating your GitHub Actions workflow to use GitHub's OpenID Connect (OIDC) Identity Provider instead of traditional AWS access keys enhances the security of your CI/CD pipelines. This guide provides step-by-step instructions to help you transition to this more secure authentication method, leveraging short-lived tokens and reducing the need for long-term AWS credentials stored as GitHub secrets.

## Benefits of Using OIDC

1. **Enhanced Security**: Reduces the need to store and manage long-term AWS credentials in GitHub secrets.
2. **Automatic Credential Rotation**: Uses short-lived credentials, which are automatically rotated, reducing the risk of credential exposure.
3. **Simplified Management**: Eliminates the need for manual key rotation and management, streamlining the workflow configuration.

## Steps to Update the Workflow

### Define GitHub Variables

Ensure you define the necessary GitHub variables (`AWS_REGION` and `ECR_REPOSITORY`) in your repository settings or in your workflow file directly.

### Update Your GitHub Actions Workflow

Replace the step for configuring AWS credentials in your current workflow with the new step that uses the OIDC provider. This change will allow your workflow to use short-lived credentials provided by AWS STS, enhancing security and reducing the need for long-term access keys.

#### Old Step

```yml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: your-region
```

In the old step, the AWS access keys (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) are stored as secrets in your GitHub repository. This method requires managing and rotating these keys manually, which can be a security risk if the keys are compromised.

#### New Step

```yml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    audience: sts.amazonaws.com
    aws-region: ${{ env.AWS_REGION }}
    role-to-assume: arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/GitHub-OIDC-Identity-Provider-Role
```

In the new step, the workflow uses GitHub's OIDC provider to obtain short-lived credentials from AWS STS. Here's a breakdown of the parameters:

- `audience`: Specifies the audience for the OIDC token, which should be `sts.amazonaws.com` for AWS STS.
- `aws-region`: Specifies the AWS region where your resources are located, referenced from the environment variable `AWS_REGION`.
- `role-to-assume`: The ARN of the IAM role that GitHub Actions will assume using the OIDC token. This role should have the necessary permissions to perform actions in your AWS account.

### Verify and Test

After making these changes, commit and push your workflow file. Monitor the workflow run to ensure it completes successfully and pushes your Docker image to Amazon ECR.

## Best Practices

1. **Use Least Privilege**: Ensure that the IAM role assumed via OIDC has the minimum permissions necessary to perform its tasks. Review and update policies regularly.
2. **Regularly Rotate Secrets**: For any remaining secrets in your GitHub repository, implement a regular rotation policy to further enhance security.
3. **Monitor and Audit**: Enable logging and monitoring for the IAM roles and policies used in your workflows. Regularly audit the logs for any unusual or unauthorized activities.
4. **Environment Variables**: Use GitHub environment variables to manage configuration settings such as AWS region and repository names, keeping the workflow file clean and maintainable.
5. **Keep Dependencies Updated**: Regularly update the GitHub Actions and AWS CLI tools used in your workflows to benefit from the latest features and security patches.

## Key Takeaways

1. **Improved Security**: Transitioning to GitHub's OIDC Identity Provider eliminates the need for long-term AWS access keys, reducing the risk of credential leakage.
2. **Simplified Credential Management**: OIDC provides short-lived, automatically rotated credentials, streamlining the management process.
3. **Easy Integration**: Updating your workflow to use OIDC requires minimal changes, making it easy to enhance security without significant refactoring.

## Conclusion

By following this guide, you have successfully updated your GitHub Actions workflow to utilize GitHub's OIDC Identity Provider for AWS authentication. This change not only enhances the security of your deployment pipeline but also simplifies the management of AWS credentials. With the OIDC-based authentication in place, you can now enjoy a more secure and streamlined CI/CD process.

## References

- [Configuring AWS Credentials GitHub Action](https://github.com/aws-actions/configure-aws-credentials)
- [GitHub OIDC Provider Documentation](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-cloud-providers)