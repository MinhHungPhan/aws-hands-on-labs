# Calling API Gateway with JSON Web Token (JWT)

Welcome to this tutorial on securing your API Gateway with JSON Web Tokens (JWT)! In today's digital age, protecting your APIs is crucial to ensure data integrity and confidentiality. This guide will walk you through the steps of using JWT for authenticating API calls, making your digital services more secure and reliable. Whether you're a beginner or looking to refresh your knowledge, this guide aims to provide you with a clear understanding of JWT authentication and its application.

## Table of Contents

- [Introduction](#introduction)
- [What is JWT?](#what-is-jwt)
- [Calling API Gateway with JWT](#calling-api-gateway-with-jwt)
  - [Generating a New JWT with Keycloak](#step-1-generating-a-new-jwt-with-keycloak)
  - [Making a GET Request](#step-2-making-a-get-request-with-jwt)
  - [Validate the Response](#step-3-validate-the-response)
- [Best Practices](#best-practices)
- [Key Takeaways](#key-takeaways)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

JSON Web Tokens (JWT) offer a compact and self-contained way to securely transmit information between parties. By using JWT, you can validate the authenticity of requests made to your API Gateway, ensuring that only authorized users can access your backend services. This guide covers everything you need to know to implement JWT in your API calls, from generating tokens with Keycloak to validating them and making authenticated requests.

## What is JWT?

JWT is a standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object. This information can be verified and trusted because it is digitally signed. JWTs can be signed using a secret (with the HMAC algorithm) or a public/private key pair using RSA or ECDSA.

## Calling API Gateway with JWT

### Step 1: Generating a New JWT with Keycloak

To generate a new JWT using Keycloak, follow these steps:

1. **Access Keycloak Admin Console:** Log in to the Keycloak Admin Console and navigate to the client configuration page.

2. **Client Credentials:** Ensure your client is set to use the `Client ID` and `Client Secret` for authentication.

3. **Prepare Authentication Request:** Formulate a POST request to Keycloak's token endpoint, typically found at `https://<your-keycloak-domain>/auth/realms/<your-realm>/protocol/openid-connect/token`.

4. **Receive and Store JWT:** The response will contain a `access_token` field with your JWT. Securely store this token for use in authenticating your API requests.

#### Example POST Request for JWT Generation

```http
Method: POST
URL: https://<your-keycloak-domain>/auth/realms/<your-realm>/protocol/openid-connect/token
Headers: Content-Type: application/x-www-form-urlencoded
Body:
    - grant_type: client_credentials
    - client_id: <your-client-id>
    - client_secret: <your-client-secret>
```

### Step 2: Making a GET Request with JWT

After obtaining a valid JWT, you can use it to make authenticated requests to your API Gateway. Follow these steps to ensure your request is correctly authenticated:

1. **Open Your Request Tool:** Use a tool like Postman or a programming library that allows you to make HTTP requests.

2. **Create a New GET Request:** Set up a new GET request in your chosen tool. 

3. **Enter API Gateway URL:** In the request URL field, enter the URL of your API Gateway endpoint. For example: `https://9vmjo6cp6d.execute-api.eu-west-3.amazonaws.com`.

4. **Add Authorization Header:** Navigate to the headers section of your request setup. Add a new header with the key `Authorization`. For its value, type `Bearer ` followed by your JWT token. Ensure there is a space between "Bearer" and your token. It should look something like this: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`.

5. **Send the Request:** Execute the GET request by hitting the "Send" button or its equivalent in your tool.

6. **Inspect the Response:** If your request is successful, you will receive a response from the API. This response will contain the data you requested. If there is an issue with your JWT or if it has expired, you might receive an error indicating that authentication has failed.

#### Example GET Request with Authorization Header

```http
GET /api/data HTTP/1.1
Host: 9vmjo6cp6d.execute-api.eu-west-3.amazonaws.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Step 3: Validate the Response

1. **Success Verification:** If the request is successful, you will receive a status code of `200 OK` along with the expected data in the response body. The data format (e.g., JSON, XML) and the specific content will depend on your API's design and the endpoint you're accessing.

2. **Inspect the Data:** Carefully review the data returned by the API to ensure it matches your expectations based on the request you made. For instance, if you requested statistical information, verify that the response contains the correct statistics and that they are accurately formatted.

3. **Error Handling:** If you receive an error response (e.g., a `401 Unauthorized` status code), it indicates that the JWT was not accepted, possibly due to expiration or incorrect formatting. In such cases, revisit the steps for generating a new JWT and ensure that it is correctly included in the `Authorization` header.

#### Example Response for a Successful Request

```json
{
  "fibonacci_sequence": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
}
```

This example shows a successful JSON response from the API, including a status code of `200` and a body containing the requested data.

## Best Practices

- **Secure Token Storage:** Ensure JWTs are stored securely to prevent unauthorized access.
- **Token Expiry:** Implement token expiration to minimize the impact of a compromised token.
- **HTTPS:** Use HTTPS to encrypt the transmission of JWTs between the client and server.

## Key Takeaways

- JWTs are a powerful tool for authenticating API requests.
- Setting up JWT authentication involves creating a token issuer and configuring your API Gateway.
- Always follow best practices to ensure the security of your JWT implementation.

## Conclusion

By securing your API Gateway with JWT, you enhance the security of your digital services, ensuring that only authenticated users can access them. This guide has outlined the steps and best practices for using JWT in your API calls. With this knowledge, you're well-equipped to implement JWT authentication in your projects.

## References

- [Introduction to JSON Web Tokens](https://jwt.io/introduction/)
- [JWT authorizers](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html)