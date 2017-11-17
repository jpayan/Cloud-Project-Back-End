import boto3
from boto3.dynamodb.conditions import Key
from project.utils import validate_access_token, decode_string
from project.errors import UnauthorizedError

dynamodb = boto3.resource('dynamodb')
group_table = dynamodb.Table('cc414-nb-groups')


def create_group(payload):
    if validate_access_token(payload):
        item = {
            'teacher_id': payload['teacher_id'],
            'name': payload['name'],
            'students': payload['students']
        }
        group_table.put_item(Item=item)
        return item
    else:
        raise UnauthorizedError()


def get_groups_by_teacher_id(teacher_id):
    response = group_table.scan(FilterExpression=Key('teacher_id').eq(teacher_id))
    groups = response['Items']
    for group in groups:
        group['name'] = decode_string(group['name'])
    return groups


def get_group(name, teacher_id):
    response = group_table.get_item(Key={'name': name, 'teacher_id': teacher_id})
    group = response['Item']
    group['name'] = decode_string(group['name'])
    return group


def update_group(payload):
    if validate_access_token(payload):
        response = group_table.update_item(
            Key={'name': payload['name'], 'teacher_id': payload['teacher_id']},
            UpdateExpression=payload['expression'],
            ExpressionAttributeValues=payload['attributes'],
            ReturnValues='ALL_NEW'
        )
        response['name'] = decode_string(payload['name'])
        return response
    else:
        raise UnauthorizedError()


def delete_group(payload):
    if validate_access_token(payload):
        response = group_table.delete_item(Key={'name': payload['name'], 'teacher_id': payload['teacher_id']})
        return response
    else:
        raise UnauthorizedError()
