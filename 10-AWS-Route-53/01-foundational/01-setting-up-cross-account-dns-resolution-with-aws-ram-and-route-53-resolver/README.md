# Setting Up Cross-Account DNS Resolution with AWS RAM and Route 53 Resolver

Welcome to the comprehensive guide on configuring cross-account DNS resolution using AWS Resource Access Manager (RAM) and Route 53 Resolver! This document is designed to help you set up and manage DNS resolution across multiple AWS accounts, specifically focusing on private hosted zones. By following this guide, you will learn how to leverage AWS RAM and Route 53 Resolver to create a seamless, secure, and scalable DNS architecture that meets your organizational needs. This guide includes detailed steps, best practices, and a sequence diagram to ensure a smooth setup process.

## Table of Contents

- [Introduction](#introduction)
- [Components of Route 53 Resolver](#components-of-route-53-resolver)
- [Sequence Diagram and Setup Steps](#sequence-diagram-and-setup-steps)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

In a multi-account AWS environment, ensuring seamless and secure DNS resolution across accounts can be complex. AWS Route 53 Resolver, combined with AWS Resource Access Manager (RAM), offers a robust solution to enable cross-account DNS resolution, specifically for private hosted zones. By leveraging Route 53 Resolver and RAM, you can streamline DNS management, enhance resource accessibility, and maintain control over private domain resolutions within and across your accounts. This guide provides a step-by-step walkthrough of configuring cross-account DNS resolution, highlighting essential concepts, setup requirements, and best practices to build a scalable and efficient DNS architecture tailored to your organizational needs.

## Components of Route 53 Resolver

### Inbound and Outbound Endpoints

- **Inbound Endpoint**: Receives DNS queries from external sources (such as other AWS accounts) and resolves them within AWS.
- **Outbound Endpoint**: Forwards DNS queries from AWS to external DNS servers.

### Resolver Rules

Resolver rules specify how Route 53 Resolver handles queries:
- **Forward Rules**: Forward DNS queries for specific domains to designated endpoints.
- **System Rules**: Automatically route queries within AWS (e.g., for AWS services).

## Sequence Diagram and Setup Steps

Below is the sequence diagram illustrating the setup process for cross-account DNS resolution. This includes:

- **Configuring AWS RAM sharing** across three accounts: Account A, Account B, and the Shared Services Account.
- **Setting up the Route 53 Resolver Inbound Endpoint** in the Shared Services Account.
- **Configuring resolver rules** in each account.
- **Establishing private hosted zone delegation** to ensure seamless DNS resolution across accounts.

```mermaid
sequenceDiagram
    participant User as User
    participant AccountA as Account A
    participant AccountB as Account B
    participant SharedServices as Shared Services Account
    participant RAMA as AWS RAM (Account A)
    participant RAMB as AWS RAM (Account B)
    participant RAMSS as AWS RAM (Shared Services Account)
    participant VPCResolver as Route 53 Resolver Inbound Endpoint (DNS VPC, Shared Services Account)
    participant PrivateZoneA as Private Hosted Zone: interne.cloud.kientree.com (Account A)
    participant PrivateZoneB as Private Hosted Zone: devops.interne.cloud.kientree.com (Account B)
    participant PrivateZoneSS as Private Hosted Zone: interne.cloud.kientree.com (Shared Services Account)

    Note over User: Step 1: Configure RAM Sharing in Each Account

    User ->> RAMA: Share Private Hosted Zone (Account A) with Account B and Shared Services Account
    RAMA -->> User: Confirm sharing of Private Hosted Zone (Account A) with specified accounts

    User ->> RAMB: Share Private Hosted Zone (Account B) with Account A and Shared Services Account
    RAMB -->> User: Confirm sharing of Private Hosted Zone (Account B) with specified accounts

    User ->> RAMSS: Share Private Hosted Zone (Shared Services) with Account A and Account B
    RAMSS -->> User: Confirm sharing of Private Hosted Zone (Shared Services) with specified accounts

    Note over User: Step 2: Set Up Route 53 Resolver Inbound Endpoint in Shared Services Account
    User ->> SharedServices: Create DNS VPC and Subnets
    SharedServices ->> VPCResolver: Create Route 53 Resolver Inbound Endpoint
    VPCResolver -->> SharedServices: Configure endpoint with IPs in multiple subnets for high availability
    
    Note over User: Step 3: Set Security Groups for Inbound Endpoint
    User ->> VPCResolver: Attach security group allowing DNS traffic (UDP & TCP on port 53) from VPCs in Account A and Account B

    Note over User: Step 4: Configure Resolver Rules in Each Account
    User ->> AccountA: Create resolver rule for interne.cloud.kientree.com
    AccountA ->> AccountA: Forward DNS queries to IPs of Resolver Inbound Endpoint in Shared Services Account
    AccountA ->> AccountA: Associate resolver rule with VPC A

    User ->> AccountB: Create resolver rule for interne.cloud.kientree.com
    AccountB ->> AccountB: Forward DNS queries to IPs of Resolver Inbound Endpoint in Shared Services Account
    AccountB ->> AccountB: Associate resolver rule with VPC B

    User ->> SharedServices: Create resolver rules for cloud.kientree.com, interne.cloud.kientree.com, and kientree.com
    SharedServices ->> SharedServices: Associate resolver rules with VPCs in Shared Services Account

    Note over User: Step 5: Configure Private Hosted Zone Delegation
    User ->> PrivateZoneSS: Add delegation records for subdomains in Account A and Account B
    PrivateZoneSS ->> PrivateZoneA: Delegate records for subdomains under interne.cloud.kientree.com in Account A
    PrivateZoneSS ->> PrivateZoneB: Delegate records for devops.interne.cloud.kientree.com in Account B

    Note over User: Setup Complete
```

### Explanation of Each Step

1. **Step 1: Configure RAM Sharing in Each Account**:

- **Account A** shares its private hosted zone with **Account B** and the **Shared Services Account**.
- **Account B** shares its private hosted zone with **Account A** and the **Shared Services Account**.
- The **Shared Services Account** shares its private hosted zone with **Account A** and **Account B**.
- This setup enables all accounts to access each other’s private hosted zones.

2. **Step 2: Set Up Route 53 Resolver Inbound Endpoint in Shared Services Account**:

- The user creates a **DNS VPC** in the Shared Services Account with **subnets in multiple Availability Zones** for high availability.
- Within this VPC, the user configures a **Route 53 Resolver Inbound Endpoint**.

3. **Step 3: Set Security Groups for Inbound Endpoint**:

- The user attaches a **security group** to the Inbound Endpoint, allowing DNS traffic (UDP and TCP on port 53) from **VPCs in Account A and Account B**.

4. **Step 4: Configure Resolver Rules in Each Account**:

- **Account A** and **Account B** create **resolver rules** for `interne.cloud.kientree.com` that forward queries to the IP addresses of the **Resolver Inbound Endpoint** in the Shared Services Account.
- The **Shared Services Account** configures resolver rules for `cloud.kientree.com`, `interne.cloud.kientree.com`, and `kientree.com`, associating them with its VPCs.

5. **Step 5: Configure Private Hosted Zone Delegation**:

- The user adds **delegation records** in the Shared Services Account’s private hosted zone (`interne.cloud.kientree.com`) to route specific subdomains to private hosted zones in **Account A** and **Account B**.
- These delegation records direct queries for subdomains, such as `devops.interne.cloud.kientree.com`, to the appropriate private hosted zone in Account B.

## How It Works?

Here is an example of how an EC2 instance in Account A queries a domain name in Account B, and the traffic is forwarded to the Route 53 Resolver Inbound Endpoint in the Shared Services Account, which then resolves the query:

```mermaid
sequenceDiagram
    participant EC2 as EC2 Instance (VPC A, Account A)
    participant VPCResolver as VPC DNS Resolver (VPC A, Account A)
    participant ResolverInbound as Route 53 Resolver Inbound Endpoint (DNS VPC, Shared Services Account)
    participant PrivateZoneShared as Private Hosted Zone: interne.cloud.kientree.com (Shared Services Account)
    participant PrivateZoneB as Private Hosted Zone: devops.interne.cloud.kientree.com (Account B)

    EC2 ->> VPCResolver: Query devops.interne.cloud.kientree.com
    VPCResolver ->> VPCResolver: Check resolver rule for interne.cloud.kientree.com
    VPCResolver ->> ResolverInbound: Forward query to Route 53 Resolver Inbound Endpoint in DNS VPC, Shared Services Account
    
    ResolverInbound ->> ResolverInbound: Validate request origin from VPC A in Account A
    ResolverInbound ->> PrivateZoneShared: Query Private Hosted Zone for interne.cloud.kientree.com
    PrivateZoneShared ->> PrivateZoneShared: Check delegation record for devops subdomain
    PrivateZoneShared ->> PrivateZoneB: Forward query to Private Hosted Zone in Account B
    PrivateZoneB -->> PrivateZoneShared: Resolve IP for devops.interne.cloud.kientree.com
    
    PrivateZoneShared -->> ResolverInbound: Return resolved IP
    ResolverInbound -->> VPCResolver: Return IP for devops.interne.cloud.kientree.com
    VPCResolver -->> EC2: Return IP for devops.interne.cloud.kientree.com
    
    EC2 ->> devops.interne.cloud.kientree.com: Establish connection to resolved IP
```

### Explanation of Key Steps

1. **EC2 Instance Query**:

- The EC2 instance in VPC A (Account A) initiates a DNS query for `devops.interne.cloud.kientree.com`.

2. **VPC DNS Resolver**:

- The VPC DNS Resolver in VPC A checks the resolver rule for `interne.cloud.kientree.com`.
- It forwards the query to the Route 53 Resolver Inbound Endpoint in the DNS VPC of the Shared Services Account.

3. **Route 53 Resolver Inbound Endpoint**:

- The Resolver Inbound Endpoint validates the request origin from VPC A in Account A.
- It queries the Private Hosted Zone for `interne.cloud.kientree.com` in the Shared Services Account.

4. **Private Hosted Zone in Shared Services Account**:

- The Private Hosted Zone checks the delegation record for the `devops` subdomain.
- It forwards the query to the Private Hosted Zone in Account B.

5. **Private Hosted Zone in Account B**:

- The Private Hosted Zone in Account B resolves the IP address for `devops.interne.cloud.kientree.com`.
- It returns the resolved IP to the Private Hosted Zone in the Shared Services Account.

6. **Return Resolved IP**:

- The Private Hosted Zone in the Shared Services Account returns the resolved IP to the Resolver Inbound Endpoint.
- The Resolver Inbound Endpoint returns the IP to the VPC DNS Resolver in VPC A.
- The VPC DNS Resolver returns the IP to the EC2 instance.

7. **Establish Connection**:

- The EC2 instance establishes a connection to the resolved IP for `devops.interne.cloud.kientree.com`.

## References

- [AWS Route 53 Resolver Documentation](https://docs.aws.amazon.com/route53/latest/dnsresolver/)
- [AWS Private Hosted Zones Documentation](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-private.html)
- [AWS Resource Access Manager Documentation](https://docs.aws.amazon.com/ram/latest/userguide/)