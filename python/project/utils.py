import binascii
import boto3
import datetime
import os
import time
import uuid
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
test_table = dynamodb.Table('cc414-nb-tests')


def get_test_name(test_id):
    response = test_table.scan(FilterExpression=Key('test_id').eq(test_id))
    test = response['Items'][0]
    test_name = test['title']
    return test_name


def generate_id(prefix):
    uid = prefix + str(uuid.uuid4())[:4]
    return uid


def generate_code(test_name, student_email):
    code = test_name[0:2] + student_email[0:2] + binascii.b2a_hex(os.urandom(3))
    return code


def get_time_stamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')
    return st
