# import os
# import boto3
# from botocore.exceptions import ClientError
# from fastapi import HTTPException
# from dotenv import load_dotenv

# load_dotenv()

# def init_dynamodb():
#     try:
#         dynamodb = boto3.resource('dynamodb',
#             region_name=os.getenv('AWS_REGION'),
#             aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
#             aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
#         )
#         users_table = dynamodb.Table(os.getenv('DYNAMODB_TABLE_NAME_USERS'))
#         sketches_table = dynamodb.Table(os.getenv('DYNAMODB_TABLE_NAME_SKETCHES'))
#         print("Successfully connected to DynamoDB")
#         return users_table, sketches_table
#     except ClientError as e:
#         print(f"Couldn't create DynamoDB client: {e}")
#         raise HTTPException(status_code=500, detail="Failed to connect to DynamoDB")

# users_table, sketches_table = init_dynamodb()


import os
from pocketbase import PocketBase
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

def init_pocketbase():
    try:
        pocketbase_url = os.getenv('POCKETBASE_URL')
        admin_email = os.getenv('POCKETBASE_ADMIN_EMAIL')
        admin_password = os.getenv('POCKETBASE_ADMIN_PASSWORD')
        
        if not all([pocketbase_url, admin_email, admin_password]):
            raise ValueError("POCKETBASE_URL, POCKETBASE_ADMIN_EMAIL, or POCKETBASE_ADMIN_PASSWORD is not set in the environment variables")
        
        print(f"Attempting to connect to PocketBase at: {pocketbase_url}")
        pb = PocketBase(pocketbase_url)
        
        # Authenticate with admin credentials
        pb.admins.auth_with_password(admin_email, admin_password)
        
        print("Successfully connected and authenticated with PocketBase")
        return pb
    except Exception as e:
        print(f"Couldn't connect to PocketBase or authenticate. Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to connect to PocketBase or authenticate: {str(e)}")

pb = init_pocketbase()
