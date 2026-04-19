import boto3
import json
import os
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    item_id = event['pathParameters']['id']

    try:
        response = table.query(
            KeyConditionExpression=Key('id').eq(item_id)
        )
        items = response['Items']
        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps('Item not found')
            }
        return {
            'statusCode': 200,
            'body': json.dumps(items[0], default=str)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
