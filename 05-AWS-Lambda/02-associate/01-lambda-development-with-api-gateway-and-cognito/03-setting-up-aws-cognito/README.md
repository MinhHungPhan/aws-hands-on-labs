# Setting Up AWS Cognito

Welcome to our comprehensive guide on setting up AWS Cognito for Lambda Authentication. This document aims to provide you with a step-by-step tutorial on how to use AWS Cognito, a robust service offered by Amazon Web Services that facilitates authentication capabilities for your applications. Whether you're looking to implement username and password authentication or utilize JWT tokens for serverless applications, AWS Cognito offers a variety of authentication models to suit your needs. By the end of this guide, you'll be equipped with the knowledge to securely authenticate API requests to your Lambda functions using AWS Cognito.

## Table of Contents

- [Introduction](#introduction)
- [Understanding AWS Cognito](#understanding-aws-cognito)
- [Creating a User Pool](#creating-a-user-pool)
- [Configuring App Integration](#configuring-app-integration)
- [Configuring Hosted UI](#configuring-hosted-ui)
- [Best Practices](#best-practices)
- [Key Takeaways](#key-takeaways)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

AWS Cognito is a comprehensive service designed to handle user authentication and access for your applications. It supports a wide range of authentication methods, including social identity providers like Google or Facebook, as well as traditional username and password methods. This guide focuses on client credential-based authentication, which is considered one of the most secure ways to validate API calls. Our goal is to make this setup process accessible to beginners, providing clear examples and explanations along the way.

## Understanding AWS Cognito

AWS Cognito provides a scalable and secure user directory that can handle user management, authentication, and access control. It allows developers to add user sign-up, sign-in, and access control to web and mobile apps quickly and easily. The service supports federated authentication, allowing you to delegate authentication to external identity providers.

## Creating a User Pool

To get started, you'll need to create a Cognito User Pool. Follow these steps:

### Step 1: Configure Sign-in Experience

When setting up the sign-in experience, you have the option to choose how users will authenticate with your application. For this tutorial:

- **Cognito user pool sign-in options:** Select **Username** as the primary method for users to sign in. This simplifies the authentication process by allowing users to sign in with a unique username.

### Step 2: Configure Security Requirements

Security is a critical aspect of any authentication service. To keep things simple for this tutorial:

- **Password policy mode:** Use **Cognito Defaults**. This enforces a standard level of password complexity without additional configuration.
- **Multi-factor authentication (MFA):** Select **No MFA** to avoid adding an extra layer of security through a second factor, simplifying the user experience for this setup.
- **User account recovery:** Uncheck this option. This means users won't be able to recover their accounts if they forget their login details in this basic setup.

### Step 3: Configure Sign-up Experience

The sign-up experience determines how new users can create accounts:

- **Self-service sign-up:** Uncheck this option. This prevents the public from being able to sign up for an account freely, which is important if you're not ready to open your app to the public or are managing user creation through an admin process.
- **Required attributes:** No attributes are set as required at this stage, offering maximum flexibility for user data.
- **Cognito-assisted verification and confirmation**: Uncheck this option, simplifying the process by not requiring email or phone verification upon account creation.

### Step 4: Configure Message Delivery

For applications that require sending emails (e.g., for verification or notifications), AWS Cognito provides options for email delivery:

- **Email provider:** Choose **Send email with Cognito** to use AWS Cognito's built-in email capability.
- **FROM email address:** Use a predefined email address such as **no-reply@verificationemail.com**. This address will be used as the sender for all emails sent by Cognito.

### Step 5: Integrate Your App

Integrating your app with the Cognito user pool is the final step in the setup process:

- **User pool name:** Give your user pool a name, for example, **MyUserPool**. This helps identify the pool within your AWS environment.
- **Initial app client:**
    - **App type:** Choose **Public client** to indicate that the client application will be accessible publicly, suitable for apps where the client credentials are distributed with the app.
    - **App client name:** Name your app client, such as **MyPublicAppClient**. This name is used for identifying the app client within Cognito.
    - **Client secret:** Check the option to **Generate a client secret**. This secret will be used as part of the authentication process, adding an extra layer of security. It is important to securely store this secret, as it is needed to authenticate your app client with AWS Cognito.
- **Advanced app client settings:** Leave as default. This keeps the advanced security features and configurations at their default settings.
- **Attribute read and write permissions:** Leave as default. This step controls what attributes the app client can read and write, but for simplicity, the default settings are retained.

### Step 6: Review and Create

Before finalizing the creation of your user pool, review all the configurations to ensure they meet your application's requirements. Once confirmed, proceed to create the user pool. This step finalizes the setup and prepares your AWS Cognito environment to start handling authentication requests for your application.

## Configuring App Integration

App integration in AWS Cognito is crucial for enabling your application to authenticate users and provide them with the appropriate access. This process involves setting up a Cognito domain and a resource server. Here's a detailed guide to each step:

### Step 1: Create Cognito Domain

**Why do we need to create a Cognito Domain?**

A Cognito domain provides a dedicated endpoint for your user pool where your app users can go to sign in and sign up. Think of it as the address of your online store where customers know they can find you. Just as your store needs a recognizable address for customers to visit, your app needs a unique domain where users can authenticate themselves.

**Real-world analogy:** Imagine you've opened a new coffee shop. To let people know where to find you, you'd put up a sign with your shop name (e.g., "CoffeeCorner"). This name helps customers locate you. Similarly, a Cognito domain helps users find where to log in or register for your application.

- **Cognito domain:** Enter a domain prefix that's unique to your user pool, such as `p2p`. This will be part of the URL used for authentication flows.

### Step 2: Create Resource Server

**Why do we need to create a Resource Server?**

A resource server is where your protected resources, such as user data or APIs, reside. In the context of authentication and authorization, it's the server your application queries to get the user data or validate permissions after a user is authenticated. Creating a resource server in Cognito allows you to define custom scopes and permissions tailored to your application's needs.

**Real-world analogy:** Think of the resource server as the back office of your coffee shop where you keep your recipes and customer records. Only employees (authenticated users) with the right key (token with appropriate scopes) can access this office and use or view the sensitive information (resources).

- **Resource server name:** Name your resource server, such as `MyResourceServer`.
- **Resource server identifier:** This is a unique identifier for your resource server, like `MyResourceServerId`. It's used internally by AWS Cognito to manage access to your resources.

### Step 3: Create Scopes (Optional)

**Why do we need to create Scopes?**

Scopes define the specific actions or access levels that an authenticated user is allowed to have. By creating custom scopes, you effectively create "keys" that unlock different levels of access or permissions within your application.

**Real-world analogy:** Back to the coffee shop analogy, imagine you have different keys for different parts of your shop. One key allows access to the front of the shop (basic user access), another to the back office (admin access), and another for the supply room (special permissions). Scopes work similarly by defining what parts of your application or which actions an authenticated user can access or perform.

- **Custom scopes:**
    - **Scope name:** `StatCalculationsScope`. This scope might allow access to perform statistical calculations within your app.
    - **Description:** `Stat Calculations Scope`. Provides a clear description of what the scope allows within the context of your application.

## Configuring Hosted UI

Configuring the Hosted UI in AWS Cognito is an essential step in managing how users interact with your authentication system. Below, we delve into the details of configuring the Hosted UI, supported by analogies to make complex concepts more understandable.

After navigating to the **App Integration** section and selecting your **App client**, you'll need to configure several components of the Hosted UI to ensure a smooth authentication process for your users.

### Step 1: Add Callback URL

**Why do we need to Add a Callback URL?**

Think of the callback URL as the specific place inside the coffee shop where customers go after they've ordered at the counter. It's where they wait for their order to be ready and where the barista will call out their name.

**Real-world analogy:** Imagine you're in a coffee shop, and after ordering, you're directed to pick up your coffee from the end of the counter. In digital terms, `google.com` serves as that spot in our simplified example, signifying where users are directed after logging in.

- **For simplicity:** Use `google.com` as the URL. This is akin to directing all guests to a central, well-known location after they check in.

### Step 2: Specify Identity Providers

**Why do we need to Specify Identity Providers?**

Choosing an identity provider is like deciding who is allowed to verify the currency or credit cards in your coffee shop. By selecting "Cognito user pool," you're essentially saying that only the customers who've been verified by your trusted provider can place an order.

**Real-world analogy:** It's like allowing only those with a membership card or those recognized by the coffee shop's loyalty program to make a purchase. This ensures that everyone in the shop is a verified member.

- **In our case:** Select "Cognito user pool" to indicate that we are using AWS Cognito's built-in system to verify and manage our customers' identities, much like relying on a trusted and familiar staff to recognize and serve members in our coffee shop.

### Step 3: Specify OAuth 2.0 Grant Types

**Why do we need to Specify OAuth 2.0 Grant Types?**

Grant types in OAuth 2.0 dictate how a customer (application) requests access (authorization) to the coffee shop's resources (APIs/data). "Client credentials" is a method where the application acts on its own behalf, similar to a coffee shop vendor automatically placing an order for supplies based on inventory levels.

**Real-world analogy:** Imagine a coffee machine that automatically orders beans from the supplier when it's running low, without requiring manual input from the barista or manager. By selecting "Client credentials," we establish this direct, automated communication between the coffee shop's system and the supplier.

- **In our case:** Select "Client credentials" to indicate that the app is requesting access on its own behalf, not on behalf of a user.

### Step 4: Specify Custom Scopes

- **In the drop-down list:** Select "MyResourceServerId/StatCalculationsScope" to define the precise area of your application that the token grants access to, ensuring users can only access the resources they're authorized to use.

## Best Practices

- **Minimum Permission Principle**: Always grant the least privileges necessary for a task to enhance security.
- **Secure Storage of Secrets**: Store sensitive information like client secrets securely using AWS Secrets Manager.
- **Utilize Federated Identities for Flexibility**: Consider federated identities for user authentication to simplify access for users already using services like Google or Facebook.

## Key Takeaways

- **Centralized User Management:** AWS Cognito User Pools serve as the backbone for centralized user management, enabling secure sign-up, sign-in, and access control.
- **Simplified Authentication Flow:** Proper configuration of domains and callback URLs ensures a seamless authentication experience for users.
- **Custom Access Control:** Utilizing Resource Servers and Custom Scopes allows for detailed control over user permissions and resource access.
- **Security and Flexibility:** Choosing the appropriate Identity Providers and OAuth 2.0 Grant Types aligns your app's security needs with its operational requirements.

### Conclusion

This guide has provided a foundational understanding of configuring AWS Cognito for authentication, emphasizing essential aspects like user management, security, and seamless authentication flows. With AWS Cognito's capabilities, you can ensure your application offers a secure and efficient user experience. As you progress, keep in mind the importance of adapting to changing needs and continuously enhancing security and usability.

## References

- [AWS Cognito Documentation](https://docs.aws.amazon.com/cognito/index.html)
- [User pool app clients](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-client-apps.html)
- [The OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749#section-2.1)