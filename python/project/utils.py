import binascii
import boto3
import datetime
import os
import time
import uuid
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
test_table = dynamodb.Table('cc414-nb-tests')
teacher_table = dynamodb.Table('cc414-nb-teachers')


def decode_string(string):
    return string.replace('\%', '\s')


def get_test_name(test_id):
    response = test_table.scan(FilterExpression=Key('test_id').eq(test_id))
    test = response['Items'][0]
    test_name = test['title']
    return test_name


def generate_id(prefix):
    uid = prefix + str(uuid.uuid4())[:4]
    return uid


def generate_question_ids(test_id, questions):
    last_id = 0
    new_questions = []

    for index, question in enumerate(questions):
        if 'question_id' in question:
            question_id = int(question['question_id'][-1])
            last_id = last_id if last_id > question_id else question_id
        else:
            new_questions.append(index)

    for question_index in new_questions:
        last_id += 1
        questions[question_index]['question_id'] = test_id + '-' + str(last_id)

    return questions


def generate_code(test_name, student_email):
    code = test_name[0:2].upper() + student_email[0:2].upper() + binascii.b2a_hex(os.urandom(3))
    return code


def get_datetime():
    timestamp = time.time()
    date_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')
    return date_time


def get_timestamp_from_datetime(date_time):
    timestamp = time.mktime(datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S.%f').timetuple())
    return timestamp


def validate_access_token(payload):
    valid = False
    if 'teacher' in payload:
        ep_teacher = payload['teacher']
        if 'teacher_id' in ep_teacher and 'access_token' in ep_teacher:
            response = teacher_table.get_item(Key={'teacher_id': ep_teacher['teacher_id']})
            db_teacher = response['Item']
            db_access_token = db_teacher['access_token']
            ep_access_token = ep_teacher['access_token']

            last_logged_in = get_timestamp_from_datetime(db_teacher['last_logged_in'])
            expires_in = int(db_teacher['expires_in'])
            expiration_date = last_logged_in + expires_in

            if time.time() < expiration_date:
                if db_access_token == ep_access_token:
                    valid = True
    return valid
