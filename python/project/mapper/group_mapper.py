import boto3
from boto3.dynamodb.conditions import Key, Attr
from project.utils import *

dynamodb = boto3.resource('dynamodb')
group_table = dynamodb.Table('cc414-nb-groups')


def create_group(teacher_id, name, students):
    item = {
        'teacher_id': teacher_id,
        'name': name,
        'students': students
    }
    group_table.put_item(Item=item)
    return item


def get_groups(teacher_id):
    response = group_table.scan(
        FilterExpression=Key('teacher_id').eq(teacher_id)
    )
    groups = response['Items']
    return groups


def get_group(name, teacher_id):
    response = group_table.get_item(
        Key={
            'name': name,
            'teacher_id': teacher_id
        }
    )
    group = response['Item']
    return group


def update_group(name, teacher_id, expression, attributes):
    response = group_table.update_item(
        Key={
            'name': name,
            'teacher_id': teacher_id
        },
        UpdateExpression=expression,
        ExpressionAttributeValues=attributes,
        ReturnValues='UPDATED_NEW'
    )
    return response


def delete_group(name, teacher_id):
    response = group_table.delete_item(
        Key={
            'name': name,
            'teacher_id': teacher_id
        }
    )
    return response
