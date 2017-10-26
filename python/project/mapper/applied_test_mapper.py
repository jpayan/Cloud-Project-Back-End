import boto3
from boto3.dynamodb.conditions import Key, Attr
from project.utils import *

dynamodb = boto3.resource('dynamodb')
applied_test_table = dynamodb.Table('cc414-nb-applied-tests')
ses = boto3.client('ses')


def create_applied_tests(student_email, test_id, code, grade, state):
    item = {
        'student_email': student_email,
        'test_id': test_id,
        'code': code,
        'grade': grade,
        'state': state
    }
    applied_test_table.put_item(Item=item)
    test_name = get_test_name(test_id)
    code = generate_code(test_name, student_email)
    send_code(student_email, code)
    return item

def get_applied_tests_by_test(test_id, student_ids):
    applied_tests = []
    for student_id in student_ids:
        applied_tests.append(get_applied_test(test_id, student_id))
    return applied_tests


def get_applied_tests_by_student(student_ids):
    applied_tests = []
    for student_id in student_ids:
        response = applied_test_table.scan(
            FilterExpression=Key('student-id').eq(student_id)
        )
        applied_tests.append(response['Items'])
    return applied_tests


def get_applied_test(test_id, student_id):
    response = applied_test_table.get_item(
        Key={
            'test-id': test_id,
            'student-id': student_id
        }
    )
    applied_test = response['Item']
    return applied_test


def delete_applied_test(test_id, student_id):
    response = applied_test_table.delete_item(
        Key={
            'test-id': test_id,
            'student-id': student_id
        }
    )
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
            'Subject':{
                'Data': 'Test Code'
            },
            'Body':{
                'Text':{
                    'Data': code
                }
            }
        }
    )
    return response