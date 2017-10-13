import boto3
from project.utils import *

dynamodb = boto3.resource('dynamodb')
test_table = dynamodb.Table('cc414-nb-tests')


def create_test(name, subject, questions):
    item = {
        'id': generate_id(),
        'title': name,
        'subject': subject,
        'questions': questions
    }
    test_table.put_item(Item=item)
    return item


def get_tests():
    response = test_table.scan()
    tests = response['Items']
    return tests


def get_test(test_id):
    response = test_table.get_item(Key={'id': test_id})
    test = response['Item']
    return test


def update_test(test_id, expression, attributes):
    response = test_table.update_item(
        Key={
            'id': test_id
        },
        UpdateExpression=expression,
        ExpressionAttributeValues=attributes,
        ReturnValues='UPDATED_NEW'
    )
    return response


def delete_test(test_id):
    response = test_table.delete_item(Key={'id': test_id})
    return response
