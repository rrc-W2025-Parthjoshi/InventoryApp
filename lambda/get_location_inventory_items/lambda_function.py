import boto3
import json
import os
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    location_id = int(event['pathParameters']['id'])

    try:
        response = table.query(
            IndexName='GSI_location_id_id',
            KeyConditionExpression=Key('location_id').eq(location_id)
        )
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'], default=str)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
