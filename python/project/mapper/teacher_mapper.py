import boto3
from project.utils import get_time_stamp

dynamodb = boto3.resource('dynamodb')
teacher_table = dynamodb.Table('cc414-nb-teachers')


def create_teacher(payload):
    item = {
        'teacher_id': payload['teacher_id'],
        'full_name': payload['full_name'],
        'access_token': payload['access_token'],
        'last_logged_in': get_time_stamp(),
        'expires_in': payload['expires_in']
    }
    teacher_table.put_item(Item=item)
    return item


def get_teacher(teacher_id):
    response = teacher_table.get_item(Key={'teacher_id': teacher_id})
    teacher = response['Item']
    return teacher


def delete_teacher(teacher_id):
    response = teacher_table.delete_item(Key={'teacher_id': teacher_id})
    return response
