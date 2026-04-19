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
        location_id = items[0]['location_id']
        table.delete_item(
            Key={
                'id': item_id,
                'location_id': int(location_id)
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {item_id} deleted successfully.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item: {str(e)}")
        }
