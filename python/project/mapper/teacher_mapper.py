import boto3
from project.utils import *

dynamodb = boto3.resource('dynamodb')
teacher_table = dynamodb.Table('cc414-nb-teachers')


def create_teacher(teacher_id, full_name, access_token):
    item = {
        'teacher_id': teacher_id,
        'full_name': full_name,
        'access_token': access_token
    }
    teacher_table.put_item(Item=item)
    return item


def get_teachers():
    response = teacher_table.scan()
    teachers = response['Items']
    return teachers


def get_teacher(teacher_id):
    response = teacher_table.get_item(Key={'teacher_id': teacher_id})
    teacher = response['Item']
    return teacher


def update_teacher(teacher_id, expression, attributes):
    response = teacher_table.update_item(
        Key={
            'teacher_id': teacher_id
        },
        UpdateExpression=expression,
        ExpressionAttributeValues=attributes,
        ReturnValues='UPDATED_NEW'
    )
    return response


def delete_teacher(teacher_id):
    response = teacher_table.delete_item(Key={'teacher_id': teacher_id})
    return response
