# Setting Up API Gateway

Welcome to this comprehensive guide on setting up API Gateway! This document will walk you through the essentials of configuring API Gateway to secure and manage your APIs efficiently. API Gateway acts as a front door to your backend services, enabling you to execute functions, connect to data sources, and apply authentication and authorization mechanisms with ease. This guide is designed to be accessible, providing clear explanations, best practices, and practical examples.

## Table of Contents

- [Introduction](#introduction)
- [Getting Started with API Gateway](#getting-started-with-api-gateway)
- [Testing the Invoke URL](#testing-the-invoke-url)
- [Integrating Lambda Functions](#integrating-lambda-functions)
- [Securing Your API with JWT Authentication](#securing-your-api-with-jwt-authentication)
- [Best Practices](#best-practices)
- [Key Takeaways](#key-takeaways)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

API Gateway is a fully managed service that makes it easier for developers to create, publish, maintain, monitor, and secure APIs at any scale. It acts as a front-end for applications to access data, business logic, or functionality from backend services. This guide aims to simplify the process of setting up API Gateway, integrating it with Lambda functions for serverless execution, and securing your APIs with JWT authentication.

## Getting Started with API Gateway

### Step 1: Create an API

1. **Navigate to API Gateway**: Log in to the AWS Management Console, search for and select API Gateway.

2. **Choose API Type**: API Gateway supports several API types, including HTTP APIs, REST APIs, and WebSocket APIs. For most serverless applications, HTTP APIs offer a simplified setup and lower latency. Click on "Create API" and select the appropriate type.

3. **API Configuration**: 

- **API Name**: Provide a meaningful name that reflects the API's purpose, such as `StatisticsCalculationsAPI`.
- **Protocol**: Choose HTTP or REST, depending on your selection earlier.
- **Endpoint Type**: Select the visibility of the API endpoint, typically `Regional`, `Edge-optimized` (for REST APIs), or `Private`.
- **Description**: Optionally, add a description to document the API's functionality.

### Step 2 (Optional): Configure Routes

1. **Define New Route**: Routes are integral to managing how API requests are directed. Click on "Create Route".

2. **Specify Method and Resource Path**: For instance, a GET method to fetch user data might have a resource path `/users`.

3. **Attach Integrations**: Select or create an integration, such as a Lambda function or HTTP endpoint, that the route will target. This tells API Gateway where to send requests that match this route.

#### Example:

```plaintext
Method: GET
Resource Path: /users/{userId}
Integration: GetUserLambdaFunction
```

At this stage, AWS API Gateway allows you to define how client requests are routed to your backend services. However, for a quick start:

- **Use Default Route**: Stick with the default route provided during the API creation process. The default route is capable of handling basic API requests and can be modified or expanded later as needed.

### Step 3 (Optional): Define Stages

1. **Stage Configuration**: Stages in API Gateway represent different environments (e.g., development, testing, production). Navigate to "Stages" in your API's console.

2. **Create Stage**: Click on "Create Stage". You'll need to provide a stage name, such as `dev` or `prod`.

3. **Stage Settings**: Configure stage settings including logging, throttling, and access policies. This helps in managing how your API behaves in different environments.

4. **Deploy API**: To make your API accessible, deploy it to the stage you've created. This action makes your configurations active and reachable via the stage's URL.

For getting started quickly:

- **Use Default Stage**: API Gateway automatically creates a default stage for your HTTP API. This allows you to deploy and test your API immediately without manual stage configuration.

### Step 4: Review and Create

1. **Review Settings**: Before finalizing your API, review all settings, including routes, integrations, and stage configurations. Ensure everything aligns with your application's requirements and security standards.

2. **Create API**: With everything set up and reviewed, click on "Create API" or "Deploy API" (depending on your process). This action finalizes the creation and deployment of your API.

## Testing the Invoke URL

1. **Locate the Invoke URL**: After creating your API, AWS API Gateway provides an invoke URL. This URL is the endpoint through which your API can be accessed. You can find this URL in the API Gateway console, under the 'Stages' section of your HTTP API.

2. **Use a Tool or Browser for Testing**: You can test the invoke URL using various methods:

- **Browser**: Simply paste the invoke URL into your browser's address bar and press Enter. This method works well for GET requests.

- **Command Line (curl)**: Use a command-line tool like curl to test the API. For example:

```bash
curl -X GET "<your-invoke-URL>"
```

- **Postman**: Postman is a popular tool for testing APIs. Create a new request, set the method to GET (or appropriate method for your route), paste your invoke URL, and send the request.

3. **Expected Response**: Since you're testing with default configurations and potentially without specific routes or integrations set up, the response might be:

```json
{"message":"Not Found"}
```

This response indicates that the API Gateway received your request but didn't find a configured route or backend integration to handle it. It's a default placeholder response, signifying that your API Gateway is operational but needs further configuration to serve meaningful responses.

## Integrating Lambda Functions

After creating your API, the next step is to integrate it with Lambda functions. Integrating AWS Lambda functions with API Gateway enables you to create dynamic, serverless APIs quickly. This integration allows your API to execute code in response to HTTP requests without managing infrastructure.

In this detailed guide, we'll walk through creating a route in API Gateway, attaching a Lambda function to that route, and testing the integration. We’ll use a Lambda function (`statisticalCalculation`) that calculates a factorial, as created in a previous tutorial.

### Step 1: Create a Route for API

1. **Open API Gateway Console**: Navigate to the API Gateway section in the AWS Management Console.
2. **Select Your API**: Choose the API to which you want to add the route.

3. **Create a Route**:

- Click on the “Routes” option from the sidebar.
- Select “Create” or “Create Route”.
- For the HTTP method, choose `GET`.
- Define the resource path, such as `/calculate`. This path will be appended to your API's base URL to form the full endpoint URL.

### Step 2: Create and Attach Integration

Once you've established a route, the next step is to define what happens when a request hits that route. Here, we’ll attach a Lambda function as the backend service.

1. **Specify Integration Details**:

- **Integration Type**: Choose "Lambda Function".
- **AWS Region**: Select the region where your Lambda function resides. For this guide, we’re using `eu-west-3`.
- **Lambda Function**: Use the picker to select your previously created Lambda function, named `statisticalCalculation`.

2. **Invoke Permissions**:

- Before finalizing, ensure to **Grant API Gateway permission to invoke your Lambda function**. This step is crucial for API Gateway to interact with Lambda seamlessly.

### Step 3: Invoke the URL to Test

With your route and integration set up, your API is ready to be tested.

1. **Find the Invoke URL**: In the API Gateway console, navigate to the “Stages” section, select your stage (e.g., default), and copy the Invoke URL provided.

2. **Test the Endpoint**: Copy your Invoke URL and visit it in your browser or use a tool like Postman or curl. For example:

```bash
curl -X GET <Your-Invoke-URL>
```

3. **Expected Result**:
   
- The response should be a JSON object representing the output of your Lambda function. Given the `statisticalCalculation` function's logic, you might see something like:

```json
{"factorial": 720}
```
 
This confirms that your API Gateway is correctly configured to invoke your Lambda function and return the calculated result.

## Best Practices

- **Use Stage Variables**: Stage variables allow you to manage environment-specific configurations, such as endpoints or Lambda function versions.
- **Enable Logging and Monitoring**: Use Amazon CloudWatch to monitor API calls and log requests, responses, and errors for debugging purposes.
- **Implement Throttling**: Protect your backend services by limiting the rate of requests your API can handle.

## Key Takeaways

- API Gateway simplifies the process of deploying and managing APIs.
- Integrating Lambda functions allows for serverless backend logic execution.
- Securing your API with JWT authentication ensures that only authorized users can access your services.

## Conclusion

Setting up API Gateway is a pivotal step in developing scalable and secure applications in the AWS cloud. By following this guide, you've learned how to create an API, integrate it with Lambda functions for serverless computing, and secure it using JWT authentication. Embrace these practices to enhance your application's security, reliability, and efficiency.

## References

- [AWS API Gateway Documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
- [Amazon Cognito Documentation](https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)