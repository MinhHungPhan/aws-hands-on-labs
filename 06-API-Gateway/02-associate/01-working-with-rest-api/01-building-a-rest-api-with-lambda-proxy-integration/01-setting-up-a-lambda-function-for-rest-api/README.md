# Setting up a Lambda Function for REST API

Welcome to this comprehensive guide on setting up a Lambda function for building a REST API using AWS Lambda Proxy Integration. This document provides an in-depth introduction to developing serverless APIs with AWS Lambda and API Gateway, simplifying complex concepts through clear explanations and practical examples. By the end of this tutorial, you will gain a solid understanding of how to deploy a scalable REST API using serverless architecture with minimal configuration.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Creating Your First Lambda Function](#creating-your-first-lambda-function)
- [Testing the Lambda Function](#testing-the-lambda-function)
- [Best Practices](#best-practices)
- [Key Takeaways](#key-takeaways)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

AWS Lambda is a serverless computing service that runs your code in response to events and automatically manages the underlying compute resources for you. When combined with AWS API Gateway, you can set up a REST API that triggers Lambda functions in response to HTTP requests without managing servers. This approach is known as Lambda Proxy Integration, where API Gateway passes all the details of the HTTP request to the Lambda function and the function's output is then returned to the API client directly.

## Prerequisites

To get started, you need an AWS account and the AWS CLI installed and configured on your computer. Here’s how to set up:

1. **Create an AWS Account**: If you do not have one, you can sign up for free at [AWS](https://repost.aws/knowledge-center/create-and-activate-aws-account).

2. **Install AWS CLI**: Download and install the AWS Command Line Interface from [aws.amazon.com/cli.](https://aws.amazon.com/cli/)

## Creating Your First Lambda Function

1. **Open the AWS Lambda Console**:

- Log into your AWS account and navigate to the Lambda section.

2. **Create a New Lambda Function**:

- Click on the "Create function" button.
- Select the "Author from scratch" option.
- Enter the function name as `HTTPMethodHandler`.
- For the runtime, choose "Python 3.12".
- Under permissions, select "Create a new role with basic Lambda permissions" to automatically set up a role with the necessary policies for your Lambda function to run.

3. Under **Function code**, in the inline code editor, copy/paste the following code:

```python
import json

def lambda_handler(event, context):
    # Get the HTTP method from the event that API Gateway passes to the Lambda function
    http_method = event['httpMethod']
    
    if http_method == 'GET':
        # Process the GET request
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'GET request processed successfully!'
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    elif http_method == 'POST':
        # Process the POST request
        # You can access the body of the request with event['body']
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'POST request processed successfully!',
                'data': json.loads(event['body'])
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    elif http_method == 'PUT':
        # Process the PUT request
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'PUT request processed successfully!',
                'data': json.loads(event['body'])
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    elif http_method == 'DELETE':
        # Process the DELETE request
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'DELETE request processed successfully!'
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    else:
        # HTTP method not supported
        return {
            'statusCode': 405,
            'body': json.dumps({
                'message': 'Method Not Allowed'
            }),
            'headers': {
                'Content-Type': 'application/json',
                'Allow': 'GET, POST, PUT, DELETE'  # Specifying allowed methods
            }
        }
```

This function demonstrates handling different HTTP methods (GET, POST, PUT, DELETE) within a single Lambda function, which is typical for a RESTful service.

4. Choose **Deploy**.

## Testing the Lambda Function

To ensure that your Lambda function `HTTPMethodHandler` is working correctly, you can create and use test events in the AWS Lambda Console. These test events simulate different types of HTTP requests. Below are the steps and examples to guide you through testing each supported HTTP method.

### Creating Test Events in AWS Lambda Console

1. **Access Your Lambda Function**:

- Navigate to the AWS Lambda Console.
- Open the function `HTTPMethodHandler`.

2. **Configure Test Events**:

- Click on the dropdown next to the "Test" button at the top of the function's page.
- Select "Configure test events".

3. **Create and Save Test Events**:

- Choose "Create new test event".
- Name your test event descriptively, such as `TestGET`, `TestPOST`, etc.
- Enter the JSON for the test event. Below are examples for different HTTP methods.

### Sample Test Events

**Test Event for GET Request**

```json
{
  "httpMethod": "GET",
  "body": "",
  "headers": {}
}
```

**Test Event for POST Request**

```json
{
  "httpMethod": "POST",
  "body": "{\"name\": \"John Doe\", \"age\": 30}",
  "headers": {
    "Content-Type": "application/json"
  }
}
```

**Test Event for PUT Request**

```json
{
  "httpMethod": "PUT",
  "body": "{\"name\": \"Jane Doe\", \"age\": 25}",
  "headers": {
    "Content-Type": "application/json"
  }
}
```

**Test Event for DELETE Request**

```json
{
  "httpMethod": "DELETE",
  "body": "",
  "headers": {}
}
```

4. **Test Your Lambda Function**:

- After creating and saving each test event, select it from the dropdown next to the "Test" button.
- Click "Test" to execute the Lambda function with the selected test event.
- Review the execution result and logs displayed below the code editor to ensure your function behaves as expected for each HTTP method.

## Best Practices

- **Security**: Use AWS IAM roles and policies to securely manage access to your Lambda functions.
- **Error Handling**: Implement comprehensive error handling in your Lambda function to manage different HTTP response codes.
- **Logging and Monitoring**: Utilize AWS CloudWatch to monitor and log API calls and Lambda executions.

## Key Takeaways

- Lambda Proxy Integration simplifies the process of building REST APIs with AWS.
- It allows developers to manage the full request and response lifecycle within their Lambda function.
- This integration is efficient for building scalable and maintainable serverless applications.

## Conclusion

Setting up a Lambda function for REST API deployment through Lambda Proxy Integration offers a robust, scalable, and cost-efficient approach to developing serverless applications. By following this guide, you now have a comprehensive understanding of configuring Lambda functions to handle RESTful services. This foundation prepares you for the next steps, which include integrating these functions with API Gateway to fully deploy your REST APIs.

## References

- [How do I create and activate a new AWS account?](https://repost.aws/knowledge-center/create-and-activate-aws-account)
- [Tutorial: Build a Hello World REST API with Lambda proxy integration](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-api-as-simple-proxy-for-lambda.html)
- [Testing Lambda functions in the console](https://docs.aws.amazon.com/lambda/latest/dg/testing-functions.html)