import uuid
import os, binascii
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
test_table = dynamodb.Table('cc414-nb-tests')


def generate_id():
    uid = str(uuid.uuid4())
    return uid


def get_test_name(test_id):
    response = test_table.scan(
        FilterExpression=Key('test_id').eq(test_id)
    )
    test_name = response['Items'][0]['title']
    return test_name

def generate_code(test_name, student_email):
    code = test_name[0:2] + student_email[0:2] + binascii.b2a_hex(os.urandom(3))
    return code
