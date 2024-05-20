import json

def fibonacci(n):
    a, b = 0, 1
    sequence = []
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

def lambda_handler(event, context):
    # Extract the 'n' value from the event object; default is 10 if not provided
    n = event.get('n', 10)
    
    # Calculate the Fibonacci sequence up to n
    fib_sequence = fibonacci(n)
    
    # Return the result
    return {
        'statusCode': 200,
        'body': json.dumps({'fibonacci_sequence': fib_sequence})
    }