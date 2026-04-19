import boto3
import json
import os
import uuid

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])

    try:
        data = json.loads(event['body'])
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad request. Please provide the data.')
        }

    unique_id = str(uuid.uuid4())

    try:
        table.put_item(
            Item={
                'id': unique_id,
                'item_name': data['item_name'],
                'item_description': data['item_description'],
                'item_qty_on_hand': int(data['item_qty_on_hand']),
                'item_price': str(data['item_price']),
                'location_id': int(data['location_id'])
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {unique_id} added successfully.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding item: {str(e)}")
        }
