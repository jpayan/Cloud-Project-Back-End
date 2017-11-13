import boto3
import re
from boto3.dynamodb.conditions import Key, Attr
from project.utils import get_test_name, generate_code

dynamodb = boto3.resource('dynamodb')
applied_test_table = dynamodb.Table('cc414-nb-applied-tests')
ses = boto3.client('ses')


def create_applied_tests(payload):
    item = {
        'student_email': payload['student_email'],
        'test_id': payload['test_id'],
        'grade': payload['grade'],
        'state': payload['state'],
        'answers': payload['answers']
    }
    test_name = get_test_name(payload['test_id'])
    code = generate_code(test_name, payload['student_email'])
    item['code'] = code
    applied_test_table.put_item(Item=item)
    send_code(payload['student_email'], code)
    return item


def get_test_id_by_code(code):
    response = applied_test_table.scan(FilterExpression=Attr('code').eq(code))
    applied_test = response['Items'][0]
    test_id = applied_test['test_id']
    return test_id


def get_applied_tests_by_test(test_id):
    response = applied_test_table.scan(FilterExpression=Key('test_id').eq(test_id))
    applied_tests = response['Items']
    return applied_tests


def get_applied_tests_by_student(student_email):
    response = applied_test_table.scan(FilterExpression=Key('student_email').eq(student_email))
    applied_tests = response['Items']
    return applied_tests


def update_applied_test(payload):
    if 'token' in payload or re.match(r'set answers=:a', payload['expression']):
        response = applied_test_table.update_item(
            Key={
                'test_id': payload['test_id'],
                'student_email': payload['student_email']
            },
            UpdateExpression=payload['expression'],
            ExpressionAttributeValues=payload['attributes'],
            ReturnValues='ALL_NEW'
        )
    else:
        response = {
            'Status': 403,
            'Message': 'You are not authorized to do this action.'
        }
    return response


def delete_applied_test(payload):
    response = applied_test_table.delete_item(
        Key={'test_id': payload['test_id'], 'student_email': payload['student_email']})
    return response


def send_code(address, code):
    response = ses.send_email(
        Source='jpayan@cetys.edu.mx',
        Destination={
            'ToAddresses': [
                address
            ]
        },
        Message={
            'Subject': {
                'Data': 'Test Code'
            },
            'Body': {
                'Text': {
                    'Data': code
                }
            }
        }
    )
    return response
