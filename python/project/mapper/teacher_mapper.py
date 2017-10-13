import boto3
from project.utils import *

dynamodb = boto3.resource('dynamodb')
teacher_table = dynamodb.Table('nb-teachers')


def create_teacher(email, full_name, prefix, password, groups, tests):
    item = {
        'id': generate_id(),
        'email': email,
        'full_name': full_name,
        'prefix': prefix,
        'password': password,
        'groups': groups,
        'tests': tests
    }
    teacher_table.put_item(Item=item)
    return item


def get_teachers():
    response = teacher_table.scan()
    tests = response['Items']
    return tests


def get_teacher(teacher_id):
    response = teacher_table.get_item(Key={'id': teacher_id})
    test = response['Item']
    return test


def update_teacher(teacher_id, expression, attributes):
    response = teacher_table.update_item(
        Key={
            'id': teacher_id
        },
        UpdateExpression=expression,
        ExpressionAttributeValues=attributes,
        ReturnValues='UPDATED_NEW'
    )
    return response


def delete_teacher(teacher_id):
    response = teacher_table.delete_item(Key={'id': teacher_id})
    return response
