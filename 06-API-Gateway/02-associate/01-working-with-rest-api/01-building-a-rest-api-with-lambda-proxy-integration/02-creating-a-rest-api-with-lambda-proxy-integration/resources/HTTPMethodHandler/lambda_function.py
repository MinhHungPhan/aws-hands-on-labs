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