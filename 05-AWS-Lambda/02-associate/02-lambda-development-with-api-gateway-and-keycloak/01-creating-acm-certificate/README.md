# Creating ACM Certificate for Keycloak

Welcome to our comprehensive guide on securing your Keycloak service with an AWS Certificate Manager (ACM) certificate. This document aims to demystify the process of creating and managing SSL/TLS certificates for your Keycloak deployment, ensuring secure HTTPS connections to AWS Cognito Identity pools. Designed with beginners in mind, our guide walks you through each step with clear examples and best practices, making the journey towards enhanced security an informative and engaging experience.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Concepts](#concepts)
- [Step-by-Step Guide](#step-by-step-guide)
    - [Logging into AWS Certificate Manager](#logging-into-aws-certificate-manager)
    - [Requesting a Public Certificate](#requesting-a-public-certificate)
    - [Validating the Certificate](#validating-the-certificate)
- [Understanding CNAME in DNS](#understanding-cname-in-dns)
    - [How CNAME Works for ACM DNS Validation](#how-cname-works-for-acm-dns-validation)
    - [The Validation Process](#the-validation-process)
- [Best Practices](#best-practices)
- [Key Takeaways](#key-takeaways)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

In the digital era, securing web services is paramount to ensuring data integrity, confidentiality, and trust. AWS Certificate Manager (ACM) offers a streamlined solution for managing SSL/TLS certificates, vital for secure communication. This guide focuses on leveraging ACM to secure Keycloak, an open-source Identity and Access Management solution, with HTTPS service by obtaining and implementing an ACM certificate or a third-party certificate.

## Prerequisites

Before diving into the certificate creation process, ensure you have the following:
- An AWS account with access to the AWS Certificate Manager.
- A domain name for your Keycloak service, e.g., `keycloak.yourdomain.com`.
- Basic familiarity with AWS services and Keycloak.

## Concepts

Understanding the necessity of an ACM Certificate for Keycloak involves delving into the realms of web security and user authentication. Keycloak, as an Identity and Access Management (IAM) tool, plays a crucial role in securing applications by managing users and providing ways to authenticate and authorize them. Here’s why integrating ACM certificates into Keycloak setups is essential:

### Secure Communication

- **HTTPS Over HTTP**: Keycloak deals with sensitive user information and credentials. Using HTTPS (secured by SSL/TLS certificates like those provided by ACM) instead of HTTP ensures that all communications between clients and the Keycloak server are encrypted. This encryption protects against eavesdropping, man-in-the-middle attacks, and data tampering.

### Trust and Credibility

- **Trustworthiness**: An SSL/TLS certificate also serves as a badge of authenticity for your Keycloak server. It assures users that they are communicating with the genuine server. Browsers and clients show visual cues (like a padlock icon) indicating a secure connection, fostering trust in users.

### Regulatory Compliance

- **Compliance with Standards**: Many industries and services are governed by strict regulatory standards that mandate the protection of personal and sensitive data. SSL/TLS encryption is often a requirement under these regulations. By securing Keycloak with an ACM certificate, organizations can meet these compliance requirements.

### Seamless Integration

- **AWS Ecosystem Compatibility**: For services running on AWS, ACM certificates provide a seamless integration path. ACM certificates can be easily attached to AWS services like Elastic Load Balancers (ELB), Amazon CloudFront distributions, and more. This integration facilitates secure Keycloak deployments within the AWS ecosystem without the need for managing SSL/TLS certificates manually.

### Automation and Management

- **Ease of Management**: ACM simplifies the management lifecycle of SSL/TLS certificates by handling renewals and deployments automatically. This reduces the operational burden and the risk of service interruptions due to expired certificates.

### Why Not Self-Signed or Third-Party Certificates?

While Keycloak can technically use any SSL/TLS certificate, including self-signed or those issued by third-party Certificate Authorities (CAs), ACM certificates offer distinct advantages:

- **Trustworthiness**: Self-signed certificates generate browser warnings that can deter users. ACM certificates are issued by a trusted CA, eliminating such warnings.
- **Integration and Automation**: ACM’s tight integration with AWS services and its automated renewal process offer convenience and reliability that self-signed and some third-party certificates cannot match.

## Step-by-Step Guide

### Logging into AWS Certificate Manager

1. Navigate to the AWS Certificate Manager console.
2. From the top navigation bar, select the AWS Region where you plan to deploy Keycloak.

### Requesting a Public Certificate

1. In the left navigation pane, click on **List certificates**.
2. Click **Request** to initiate the process.
   - For AWS Global Regions, select **Request Public certificate**.
   - For AWS China Regions, **Request Public certificate** is your only option; select it.
3. Click **Next**.

#### Entering Domain Information

1. Under the **Domain names** section, enter your Keycloak domain, e.g., `keycloak.yourdomain.com`.
2. For **Select validation method**, choose **DNS validation** (recommended) for easier management and validation.
3. Click **Request** to submit your certificate request.

### Validating the Certificate

After you request a public certificate from AWS Certificate Manager (ACM), the next critical step is validating the certificate. Validation is essential as it proves ownership of the domain names for which you've requested the certificate. ACM supports two methods of validation: DNS validation and email validation. This guide focuses on DNS validation, the recommended approach for its automation and ease of management.

#### DNS Validation

When you choose DNS validation, ACM will generate one or more CNAME (Canonical Name) records that you must add to the DNS configuration for your domain. These records serve to prove to ACM that you control the domain names in your certificate request. Here's how to proceed:

1. **Accessing the Validation Records:**

- After requesting the certificate, navigate to the **Certificates list** in the ACM console.
- Your new certificate request will appear with a status of **Pending validation**.
- Click on the Certificate ID to view its details, where you'll find the DNS validation records under the **Domains** section.

2. **CNAME Records Information:**

- ACM provides you with a CNAME name and a CNAME value for each domain name in your certificate request.
- **CNAME Name**: This is the host name part of the CNAME record you need to add to your DNS configuration.
- **CNAME Value**: This corresponds to the value part of the record, pointing to a unique ACM-provided domain that verifies your control of the domain.

3. **Updating Your DNS Configuration:**

- Log into your domain's DNS provider's management console or website.
- Navigate to the section where you can manage DNS records.
- Create a new CNAME record, entering the CNAME name and value provided by ACM.
- Save the changes to your DNS configuration.

4. **Verification and Certificate Issuance:**

- Once you add the CNAME records to your DNS configuration, ACM begins automatically checking for their presence.
- The verification process may take some time, ranging from a few minutes to 72 hours, depending on the DNS system's propagation time.
- When ACM successfully verifies the domain ownership through the DNS records, it changes the certificate's status from **Pending validation** to **Issued**.
- The ACM console will display the certificate's status as **Issued**, indicating that the certificate is ready to use.

5. **Using the Validated Certificate:**

- With the certificate issued, you can now use it to enable HTTPS for your Keycloak service or any other application.
- If you're using AWS services like Elastic Load Balancing or Amazon CloudFront, you can easily attach the ACM certificate to these services for secure connections.

#### Key Points:

- **Propagation Time**: DNS changes may not be instantly visible worldwide due to DNS propagation delays. Allow some time for the changes to take effect.
- **Record TTL**: Setting a lower Time To Live (TTL) for the CNAME records can help speed up propagation.
- **Validation Period**: ACM certificates require revalidation every year. AWS will notify you when it's time to revalidate your domain.

## Understanding CNAME in DNS

A CNAME record in DNS (Domain Name System) is used to point one domain name (an alias) to another domain name (the canonical name). It's a way of saying, "Hey, when someone looks up this domain name, they should be directed to this other domain name instead." This is particularly useful for ACM's DNS validation process.

### How CNAME Works for ACM DNS Validation

When you request a certificate from ACM and choose DNS validation, ACM uses CNAME records to verify that you control the domain for which you're requesting the certificate. Here's the process simplified:

1. **ACM Generates CNAME Records**: After you request a certificate for your domain (e.g., `keycloak.yourdomain.com`), ACM generates a unique pair of DNS records for you to add to your domain's DNS settings. These records are a specific type of DNS record called a CNAME record.

2. **CNAME Record Structure**:

- **CNAME Name (Alias)**: This is a unique domain name generated by ACM for the validation process. It looks like a series of alphanumeric characters followed by your domain name, e.g., `_x2.acm-validations.aws.yourdomain.com`.
- **CNAME Value (Canonical Name)**: This is the target domain name that ACM checks for validation. It's another unique string provided by ACM, pointing to an AWS-controlled domain, e.g., `_x3.acm-validations.aws`.

### The Validation Process

1. **You Add the Records to Your DNS**: After receiving the CNAME Name and CNAME Value from ACM, you add them to your domain's DNS configuration as a CNAME record. This step is your action to demonstrate control over the domain.

2. **ACM Checks for the Record**: ACM then begins its process of looking for the CNAME record you've added. It queries DNS for the CNAME Name and checks if it resolves to the CNAME Value it provided.

3. **Success Criteria**: If ACM can verify that the CNAME Name resolves to the CNAME Value, it concludes that you have proven control over the domain. This is because only someone with the authority to manage the domain's DNS settings could have added a record that matches ACM's specific validation requirements.

4. **Certificate Issuance**: Once the CNAME records are verified, ACM marks the certificate request as valid and issues the certificate. This certificate can then be used to enable HTTPS for your domain, securing communications to and from your Keycloak server.

## Best Practices

- **DNS Validation**: Opt for DNS validation over email validation for a smoother, more automated process.
- **Region Selection**: Choose the same AWS Region for your ACM certificate as your Keycloak deployment to minimize latency and potential issues.
- **Security**: Regularly monitor and update your certificates to ensure your Keycloak service remains secure against new threats.

## Key Takeaways

- ACM offers a secure and efficient way to manage SSL/TLS certificates for Keycloak.
- DNS validation is the recommended method for its ease of use and automation capabilities.
- Selecting the appropriate AWS Region is crucial for optimal performance and security.

## Conclusion

Securing your Keycloak service with an ACM certificate is an essential step towards safeguarding your digital assets and user data. By following the steps outlined in this guide, you can achieve a secure HTTPS setup, ensuring trusted and encrypted connections. Remember, security is an ongoing process; regularly review and renew your certificates to maintain the highest security standards.

## References

- [AWS Certificate Manager Documentation](https://docs.aws.amazon.com/acm/)
- [Keycloak Official Documentation](https://www.keycloak.org/documentation.html)
- [How to upload an SSL certificate to AWS IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_server-certs.html)
- [Keycloak on AWS](https://aws-samples.github.io/keycloak-on-aws/en/)