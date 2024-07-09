# Creating a REST API with Lambda Proxy Integration

Welcome to the second part of our tutorial series on developing serverless REST APIs using AWS Lambda and API Gateway. Building on the Lambda function setup from [the first tutorial](../01-setting-up-a-lambda-function-for-rest-api/README.md), this guide will take you through the steps to integrate your Lambda function with API Gateway. By the end of this tutorial, you will be able to deploy a fully functional REST API that is scalable and cost-efficient.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Creating an API Gateway](#creating-an-api-gateway)
- [Configuring API Methods](#configuring-api-methods)
- [Testing Your API](#testing-your-api)
- [Deploy your API](#deploy-your-api)
- [Best Practices](#best-practices)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

This tutorial focuses on the critical steps of integrating a Lambda function with AWS API Gateway to deploy a REST API. This process is key to leveraging the serverless capabilities of AWS, enabling automatic scaling and simplified API management.

## Prerequisites

Before starting this tutorial, you should have:

- Completed [the previous tutorial](../01-setting-up-a-lambda-function-for-rest-api/README.md) on setting up a Lambda function.

## Creating an API Gateway

To establish the infrastructure for your REST API using Lambda Proxy Integration, follow these steps:

1. **Open the AWS Management Console**:

- Navigate to and open the API Gateway service.

2. **Initiate a New API**:

- Click on **Create API**.
- Select **REST API** from the available options.

3. **Configure Your API**:

- Choose **New API** and provide a descriptive name for your API, such as `LambdaProxyRESTAPI`.
- Select **Regional** as the endpoint type, which optimizes the API for clients located in the same region as the AWS resources.

4. **Create the API**:

- Click on **Create API** to finalize the setup.

## Configuring API Methods

To configure your API to interact with the Lambda function, follow these steps to define resources and methods:

### Create a Resource

1. **Select the Parent Resource**:

- Navigate to your API in the API Gateway console.
- Select the root resource (`/`) and then click `Create Resource`.

2. **Configure the New Resource**:

- Ensure `Proxy resource` is turned off.
- For `Resource path`, keep it as `/`.
- Enter `HTTPMethodHandler` as the `Resource name`.
- Make sure `CORS` (Cross-Origin Resource Sharing) is turned off.
- Click `Create resource`.

### Create an ANY Method for Handling All HTTP Requests

The `ANY` method in API Gateway is a versatile configuration that handles all types of HTTP requests using a single setup. By using the `ANY` method with Lambda Proxy Integration, you simplify API management by routing GET, POST, PUT, DELETE, PATCH, OPTIONS, and HEAD requests directly to a single Lambda function. This approach allows the function to process various requests dynamically, depending on the HTTP method, making your API easier to maintain and more efficient.

1. **Select the New Resource**:

- Choose the `/HTTPMethodHandler` resource that you just created.

2. **Create a New Method**:

- Click on `Actions` > `Create Method`.
- A dropdown will appear; select `ANY` as the method type and confirm.

3. **Configure the Integration**:

- For `Integration type`, choose `Lambda Function`.
- Enable `Lambda Proxy Integration` by turning it on.
- Specify the AWS Region where your Lambda function, `HTTPMethodHandler`, is deployed. This ensures that API Gateway can correctly invoke the Lambda function.
- Input `HTTPMethodHandler` as the name of your Lambda function. This is the function you configured in the previous tutorial to handle various HTTP methods.

4. **Set the Timeout**:

- If you want to use the default timeout value of 29 seconds, keep `Default timeout` turned on.
- For a custom timeout, choose `Default timeout` and enter a value between 50 and 29000 milliseconds.

5. **Complete the Method Setup**:

- Click `Create method`.

## Testing Your API

Testing your API thoroughly is crucial to ensure that it functions correctly and integrates seamlessly with the backend Lambda function. This section provides detailed steps on how to use the API Gateway's built-in testing feature to simulate HTTP requests for each method (GET, POST, PUT, DELETE) and scrutinize the responses.

### Steps to Test Your API

1. **Access the API Gateway Console**:

- Log in to your AWS Management Console.
- Navigate to the API Gateway service.

2. **Select Your API**:

- Choose the API linked to your `HTTPMethodHandler` function.

3. **Test API Methods**:

- For each configured method, use the testing functionality within the API Gateway console to simulate requests.

### Configuring Test Requests for Each Method

**GET Request**

- Typically used to retrieve data.
- Configure any necessary query parameters to test different retrieval scenarios.
- **Example Test Request**:

```json
{
  "httpMethod": "GET",
  "queryStringParameters": {
    "param1": "value1"
  }
}
```

**POST Request**

- Used for creating new resources.
- Include a JSON body with the data to create a new instance.
- **Example Test Request for Creating a New User**:

```json
{
  "httpMethod": "POST",
  "body": "{\"name\": \"John Doe\", \"email\": \"john.doe@example.com\", \"age\": 30, \"isActive\": true}",
  "headers": {
    "Content-Type": "application/json"
  }
}
```

**PUT Request**

- Generally used to update existing resources.
- Pass a JSON body with updated data.
- **Example Test Request for Updating a User's Details**:

```json
{
  "httpMethod": "PUT",
  "body": "{\"name\": \"John Doe\", \"email\": \"john.newemail@example.com\", \"age\": 31, \"isActive\": true}",
  "headers": {
    "Content-Type": "application/json"
  }
}
```

**DELETE Request**

- Used to remove resources.
- Include identifiers such as an ID in the path parameters or the body to specify the resource.
- **Example Test Request**:

```json
{
  "httpMethod": "DELETE",
  "pathParameters": {
    "id": "12345"
  }
}
```

## Deploy your API

- In API Gateway, select `Actions` > `Deploy API`.
- Choose or create a new deployment stage.
- Provide a stage name and configure stage settings.

## Best Practices

- Regularly update and maintain IAM policies and Lambda function permissions.
- Monitor API performance and adjust throttling as necessary to manage load.

## Conclusion

Integrating your Lambda function with API Gateway is a vital step towards deploying a robust and scalable REST API. This tutorial provided the necessary steps to achieve a seamless integration, preparing your serverless application for production.

## References

- [AWS Documentation on API Gateway](https://aws.amazon.com/documentation/apigateway/)
- [Tutorial: Build a Hello World REST API with Lambda proxy integration](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-api-as-simple-proxy-for-lambda.html)


