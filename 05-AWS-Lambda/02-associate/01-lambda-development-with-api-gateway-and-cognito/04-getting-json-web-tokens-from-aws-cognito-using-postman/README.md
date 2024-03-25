# Getting JSON Web Tokens from AWS Cognito using Postman

Welcome to this guide on acquiring JSON Web Tokens (JWTs) from AWS Cognito using Postman. This document is designed to be a comprehensive yet straightforward walkthrough for developers, testers, or anyone interested in integrating AWS Cognito with their applications for authentication purposes. Whether you're a beginner or have some experience, this guide aims to provide clear instructions, best practices, and key takeaways to help you seamlessly test and integrate JWTs from AWS Cognito.

## Table of Contents

- [Introduction](#introduction)
- [Setting Up Postman](#setting-up-postman)
- [Creating a Post Request for JWT](#creating-a-post-request-for-jwt)
- [Configuring the Request URL](#configuring-the-request-url)
- [Setting Up Authorization](#setting-up-authorization)
- [Sending the Request and Receiving the JWT](#sending-the-request-and-receiving-the-jwt)
- [Decoding and Understanding the JWT](#decoding-and-understanding-the-jwt)
- [Example](#example)
- [Best Practices](#best-practices)
- [Key Takeaways](#key-takeaways)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

JSON Web Tokens (JWTs) are an open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object. AWS Cognito uses JWTs to allow access to your APIs securely. This guide will walk you through obtaining these tokens using Postman, a popular API client that simplifies the process of making HTTP requests and testing APIs without writing code.

## Setting Up Postman

First, ensure you have Postman installed and set up on your computer. Create a new collection in Postman for organizing your requests related to AWS Cognito. A collection in Postman is a grouping of individual requests that you can execute separately or as part of a series of requests.

Here's a step-by-step guide to create a new collection named "Statistical Calculation":

1. **Open Postman:** Launch the Postman application on your computer.

2. **Create New Collection:**
   - In the sidebar on the left, you will see the "Collections" tab. Hover over it, and you'll notice a "New Collection" button (usually represented by a `+` icon or simply says "New"). Click on it.
   - Alternatively, you can click on the "New" button (a `+` icon) in the top left corner, then select "Collection" from the dropdown menu that appears.

3. **Configure Collection:**
   - A dialog box will appear for creating a new collection.
   - **Name:** Enter the name of your collection as "Statistical Calculation".

![Postman](images/01-postman/01-postman.png)

## Creating a Post Request for JWT

To get a JWT token from AWS Cognito, you'll need to create a POST request. This request will be sent to the AWS Cognito endpoint configured for your application. 

**Example:**

```plaintext
Method: POST
URL: https://<your-cognito-domain>.amazoncognito.com/oauth2/token
Headers: Content-Type: application/x-www-form-urlencoded
Body:
    - grant_type: client_credentials
    - client_id: <your-client-id>
    - scope: <your-scope>
```

Ensure you replace `<your-cognito-domain>`, `<your-client-id>`, and `<your-scope>` with your specific values.

### Step 1: Creating the "Get JWT" POST Request in Postman

1. **Open Postman:** Start by launching Postman on your computer.

2. **Select Your Collection:** Navigate to the collection you created earlier, such as "Statistical Calculation". Click on it to open.

3. **Add a New Request:**

- Inside the collection, click on the `...` button next to the collection name or the "Add Request" button within the collection tab.
- A dialog box will appear. Here, enter the name of your request as "Get JWT".
- Optionally, you can add a description to detail the purpose of this request, such as "This request retrieves a JWT token from AWS Cognito for authorization purposes."
- Click "Save to Statistical Calculation" or the equivalent button to save your request to your chosen collection.

4. **Select the POST Request:**

- With the "Get JWT" request selected, change the HTTP method to POST by clicking the dropdown next to the URL field and selecting "POST".

![Postman](images/01-postman/02-postman.png)

## Configuring the Request URL

### Step 1: Locating the Domain Name

The request URL is composed of your Cognito domain followed by `/oauth2/token`. You can find your Cognito domain in the AWS Cognito console under "App integration" > "Domain name".

1. **Domain Name Settings:**

- Within your user pool dashboard, look for the menu on the left-hand side. Find and click on “App integration” or a similar option.
- Under "App integration", you'll find "Domain name". Click on it to view your domain settings.

2. **View Your Domain:**

On the "Domain name" page, you'll see either:

- **Cognito Domain:** If you're using a domain managed by Cognito, it will be shown here. The format typically looks like `your-domain-prefix.auth.region.amazoncognito.com`, where `your-domain-prefix` is a unique name you chose when setting up the domain, and `region` is your AWS region.

- **Custom Domain:** If you have configured a custom domain for your user pool, it will be displayed here. Custom domains require additional DNS setup and an SSL certificate but offer a branded experience.

![Cognito](images/02-cognito/01-cognito.png)

### Step 2: Building the URL for the POST Request

Now, let's build the URL for your POST request based on the provided details.

1. **Configure the Request Method and URL:**

- Ensure you've selected "POST" as the method.
- Set the URL to your Cognito domain's token endpoint: `https://p2p.auth.eu-west-3.amazoncognito.com/oauth2/token`.

2. **Setting Up the Request Body:**

Since you're using the `client_credentials` grant type, you'll need to adjust the body parameters accordingly:

- Select the "Body" tab below the URL field.
- Choose "x-www-form-urlencoded".
- Enter the following key-value pairs:
    - **Key:** `grant_type` **Value:** `client_credentials`.
    - **Key:** `client_id` **Value:** `1example23456789` (Ensure no '&' at the end; it was meant for concatenation in URLs).
    - **Key:** `scope` **Value:** `MyResourceServerId/StatCalculationsScope`.

![Postman](images/01-postman/03-postman.png)

3. **Configuring Headers:**

Your headers might remain the same as before:
- Click on the "Headers" tab.
- Ensure you have the following entry:
    - **Key:** `Content-Type` **Value:** `application/x-www-form-urlencoded`.

![Postman](images/01-postman/04-postman.png)

## Setting Up Authorization

With `client_credentials`, the authorization typically involves including the `client_id` and `client_secret` directly as part of the authorization header, using Basic Authentication:

- Click on the "Authorization" tab in Postman.
- Select "Basic Auth" from the type dropdown.
- Enter your `client_id` as the Username and your `client_secret` as the Password. If your setup doesn’t use a `client_secret`, consult your Cognito configuration for the correct method of authentication.

![Postman](images/01-postman/05-postman.png)

## Sending the Request and Receiving the JWT

- After setting up the URL, body, headers, and authorization, you can send your request by clicking the "Send" button.
- If everything is set up correctly, you should receive a JWT token in the response. This token can then be used for authorized access to your services.

![Postman](images/01-postman/06-postman.png)

## Decoding and Understanding the JWT

Decoding and understanding a JSON Web Token (JWT) is essential for verifying the integrity of the token, understanding its payload, and ensuring it has been issued by a trusted issuer. JWTs are compact, URL-safe tokens that represent claims between two parties. They are composed of three parts: Header, Payload, and Signature, each base64-url encoded and separated by dots (`.`). Here's a detailed look into decoding and understanding a JWT:

### Decoding the JWT

To decode a JWT, you don't need special tools to simply split the token and decode its Base64Url encoded parts. However, to fully understand and validate it, you might use libraries or online tools like [JWT.io](https://jwt.io/), which not only decode but also help you validate the token's signature and parse the payload.

**Example JWT:**

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvZSBEb2UiLCJpYXQiOjE1MTYyMzkwMjJ9.abc123abc123abc123abc123
```

This JWT is split into three parts: Header, Payload, and Signature.

#### Header

The header typically consists of two parts: the type of the token (`typ`), which is JWT, and the signing algorithm being used (`alg`), such as HS256 (HMAC with SHA-256) or RS256 (RSA Signature with SHA-256).

**Example Header:**

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

#### Payload

The payload contains the claims. Claims are statements about an entity (typically, the user) and additional data. There are three types of claims: registered, public, and private claims.

- **Registered claims:** These are a set of predefined claims which are not mandatory but recommended, to provide a set of useful, interoperable claims. Some of them are: `iss` (issuer), `exp` (expiration time), `sub` (subject), `aud` (audience), etc.
  
- **Public claims:** These can be defined at will by those using JWTs. But to avoid collisions they should be defined in the IANA JSON Web Token Registry or be defined as a URI that contains a collision-resistant namespace.
  
- **Private claims:** These are the custom claims created to share information between parties that agree on using them and are neither registered or public claims.

**Example Payload:**

```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "admin": true,
  "iat": 1516239022
}
```

#### Signature

The signature is used to verify that the sender of the JWT is who it says it is and to ensure that the message wasn't changed along the way. To create the signature part you have to take the encoded header, the encoded payload, a secret, the algorithm specified in the header, and sign that.

### Understanding the JWT

- **Integrity and Authentication:** The signature ensures that the JWT hasn’t been altered. Verifying the signature with the public key confirms its authenticity.
- **Expiration (`exp`):** It's essential to check the `exp` claim to ensure the token hasn't expired.
- **Issuer (`iss`):** This claim indicates who issued the token. Verifying the issuer is crucial for trusting the claims within.
- **Subject (`sub`):** Identifies the principal subject of the JWT, often a user ID or identifier specific to the authentication system.
- **Audience (`aud`):** This claim identifies the recipients that the JWT is intended for. It ensures that the token is sent to the correct party.
- **Issued At (`iat`):** The time the token was issued. It can be used to determine the age of the token.

## Example

Below is an example of a decoded token on jwt.io, related to the project we've been discussing in this tutorial.

![JWT](images/03-jwt.io/01-jwt.png)

## Best Practices

- **Secure Your Secrets:** Never hardcode your client_id and client_secret in your applications. Use environment variables or secrets management services to store them securely.
- **Validate Token:** Always validate the JWT token on your server-side to ensure it's not expired and is signed by a trusted issuer.
- **Scope Management:** Define scopes precisely to limit access to specific resources based on the token.

## Key Takeaways

- Postman simplifies testing AWS Cognito's JWT functionality without writing code.
- Properly setting up the request in Postman involves configuring the URL, setting the correct headers, and using basic authorization with your Cognito credentials.
- JWT tokens can be decoded to reveal important information about the token's permissions and lifespan.

## Conclusion

This guide has walked you through the process of obtaining JWT tokens from AWS Cognito using Postman. With these tokens, you can secure your APIs by ensuring only authenticated users can access them. Remember, understanding and implementing security practices correctly is crucial in protecting your application and its users.

## References

- [AWS Cognito Documentation](https://docs.aws.amazon.com/cognito/index.html)
- [Token endpoint](https://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html)
- [Postman Documentation](https://learning.postman.com/)
- [Introduction to JSON Web Tokens](https://jwt.io/introduction)
- [JWT.io](https://jwt.io/)
