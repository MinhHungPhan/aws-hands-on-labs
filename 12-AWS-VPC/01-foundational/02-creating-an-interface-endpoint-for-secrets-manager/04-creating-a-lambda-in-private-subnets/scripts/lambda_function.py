import boto3
import socket

def lambda_handler(event, context):
    result = {}

    # 1. DNS resolution test
    try:
        resolved_ip = socket.gethostbyname("secretsmanager.YOUR-REGION.amazonaws.com")
        result["ResolvedSecretsManagerIP"] = resolved_ip
    except Exception as e:
        result["DNSResolutionError"] = str(e)

    # 2. Connectivity test on port 443
    try:
        s = socket.create_connection(("secretsmanager.YOUR-REGION.amazonaws.com", 443), timeout=3)
        result["Port443Connectivity"] = "Success"
        s.close()
    except Exception as e:
        result["Port443Connectivity"] = f"Failed: {e}"

    # 3. Secrets Manager API call
    try:
        client = boto3.client('secretsmanager', region_name='YOUR-REGION')
        response = client.get_secret_value(
            SecretId='arn:aws:secretsmanager:YOUR-REGION:YOUR-ACCOUNT-ID:secret:your-secret-name-XXXXXX'
        )
        result["SecretValue"] = response.get('SecretString')
    except Exception as e:
        result["SecretsManagerError"] = str(e)

    return result