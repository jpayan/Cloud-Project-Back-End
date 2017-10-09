import uuid
import boto3

ses = boto3.client('ses')

dynamodb = boto3.resource('dynamodb')
test_table = dynamodb.Table('Tests')


def create_test(name, subject):
    item = {
        'id': generate_id(),
        'name': name,
        'subject': subject
    }
    try:
        test_table.put_item(Item=item)
    except Exception as e:
        return 'Error: ' + e.message
    else:
        return item


def get_tests():
    try:
        response = test_table.scan()
    except Exception as e:
        return 'Error: ' + e.message
    else:
        tests = response['Items']
        return tests


def get_test(test_id):
    try:
        response = test_table.get_item(Key={'id': test_id})
    except Exception as e:
        return 'Error: ' + e.message
    else:
        test = response['Item']
        return test


def update_test(test_id, expression, attributes):
    try:
        test_table.update_item(
            Key={
                'id': test_id
            },
            UpdateExpression=expression,
            ExpressionAttributeValues=attributes,
            ReturnValues="UPDATED_NEW"
        )
    except Exception as e:
        return 'Error: ' + e.message
    else:
        return 'Item updated successfully.'


def delete_test(test_id):
    try:
        test_table.delete_item(Key={'id': test_id})
    except Exception as e:
        return 'Error: ' + e.message
    else:
        return 'Item deleted successfully.'


def generate_id():
    uid = str(uuid.uuid4())
    return uid
