import json

def factorial(n):
    """Calculate the factorial of a number n."""
    # Base case: if n is 0, factorial is 1
    if n == 0:
        return 1
    # Recursive case: n! = n * (n-1)!
    else:
        return n * factorial(n - 1)

def lambda_handler(event, context):
    """Handle the incoming request to the Lambda function."""
    # For demonstration, the number is set to 6. In practice, extract it from event object.
    # Example: number = event.get('number', 0)
    result = factorial(6)  # Calculating factorial of 6

    # Return the result as a JSON object
    return {
        'statusCode': 200,
        'body': json.dumps({
            'factorial': result
        })
    }