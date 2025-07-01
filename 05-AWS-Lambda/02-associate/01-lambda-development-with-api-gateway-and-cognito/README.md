# Lambda Development with API Gateway and Cognito

So you want to build a proper serverless API that's actually secure? Yeah, me too. This lab walks through the whole journey of setting up a Lambda function, exposing it through API Gateway, and then locking it down with AWS Cognito authentication. It's honestly one of those "sounds simple but has a million moving parts" kind of projects.

## Table of Contents

- [What We're Building](#what-were-building)
- [Before You Start](#before-you-start)
- [The Journey (aka the folders you'll work through)](#the-journey-aka-the-folders-youll-work-through)
- [Why This Matters](#why-this-matters)
- [Pro Tips](#pro-tips)
- [What You'll Learn](#what-youll-learn)
- [Additional Resources](#additional-resources)

## What We're Building

Basically, we're creating a serverless API that:
- Has actual Lambda functions doing the work
- Uses API Gateway as the front door (because who wants to deal with raw Lambda URLs?)
- Protects everything with Cognito authentication (no more "anyone can call my API" nightmares)
- Uses JWT tokens like a proper modern application

## Before You Start

Make sure you have:
- An AWS account (obviously)
- AWS CLI configured with appropriate permissions
- Postman installed (or curl if you're feeling adventurous)
- Basic understanding of REST APIs and JWT tokens

## The Journey (aka the folders you'll work through)

### 1. [Setting up AWS Lambda](./01-setting-up-aws-lambda/README.md)

First things first - we need to get our Lambda function up and running. This covers the basics of creating functions, testing them, and making sure they actually work before we start adding all the fancy stuff on top.

### 2. [Setting up API Gateway](./02-setting-up-api-gateway/README.md)

Once we have a working Lambda, we need to expose it to the world. API Gateway is AWS's way of saying "here's how you make your Lambda function look like a real REST API." We'll configure endpoints, set up HTTP methods, and connect everything together.

### 3. [Setting up AWS Cognito](./03-setting-up-aws-cognito/README.md)

Here's where things get interesting. Cognito is AWS's identity service - think of it as your bouncer that checks IDs before letting people into your API club. We'll set up user pools, app clients, and all that jazz.

### 4. [Getting JSON Web Tokens from AWS Cognito using Postman](./04-getting-json-web-tokens-from-aws-cognito-using-postman/README.md)

Okay, so we have Cognito set up, but how do we actually get those magical JWT tokens? This section walks through using Postman (because let's be real, we all love Postman) to authenticate and get tokens we can use.

### 5. [Securing API Gateway with AWS Cognito](./05-securing-api-gateway-with-aws-cognito/README.md)

Now for the main event - actually connecting API Gateway to Cognito so that only authenticated users can hit our endpoints. This is where we configure authorizers and make our API actually secure.

### 6. [Calling API Gateway using JSON Web Tokens](./06-calling-api-gateway-using-json-web-tokens/README.md)

The final piece of the puzzle - taking those JWT tokens we got from Cognito and using them to call our protected API endpoints. We'll test everything end-to-end and make sure it all actually works.

## Why This Matters

Look, you could just create a Lambda function and call it directly, but that's not how real applications work. In the real world, you need:
- **Authentication** - knowing who's calling your API
- **Authorization** - controlling what they can do
- **Rate limiting** - preventing abuse
- **Monitoring** - knowing when things break
- **Proper HTTP semantics** - status codes, headers, all that good stuff

This lab shows you how to do it the right way using AWS managed services.

## Pro Tips

- Read through each folder's README before diving in - they build on each other
- Test everything as you go - don't wait until the end to see if it works
- Keep your Postman collections organized - you'll be making a lot of requests
- Don't skip the Cognito setup - it's confusing but crucial

## What You'll Learn

By the end of this lab, you'll know how to:
- Build and deploy Lambda functions
- Configure API Gateway with proper HTTP methods and responses
- Set up Cognito user pools and app clients
- Integrate Cognito with API Gateway for authentication
- Use JWT tokens to call protected APIs
- Debug the inevitable issues that come up (because they always do)

## Support

If you have any questions or need assistance, please feel free to reach out:
- Open an issue in the GitHub repository
- Contact the course maintainers via email at support@kientree.com
- Join our community Slack channel for real-time help

*Fair warning: This isn't a 5-minute tutorial. Plan to spend some quality time with this one, especially if you're new to any of these services. But hey, that's how you actually learn this stuff, right?*