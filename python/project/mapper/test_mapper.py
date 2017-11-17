import boto3
import re
from boto3.dynamodb.conditions import Key
from applied_test_mapper import get_test_id_by_code
from project.utils import generate_id, generate_question_ids, validate_access_token
from project.errors import UnauthorizedError

dynamodb = boto3.resource('dynamodb')
test_table = dynamodb.Table('cc414-nb-tests')


def create_test(payload):
    if validate_access_token(payload):
        test_id = generate_id('t')
        questions = payload['questions']

        for index, question in enumerate(questions):
            question['question_id'] = test_id + '-' + str(index + 1)

        item = {
            'test_id': test_id,
            'teacher_id': payload['teacher_id'],
            'title': payload['title'],
            'subject': payload['subject'],
            'confidence': payload['confidence'],
            'tries': payload['tries'],
            'questions': questions
        }
        test_table.put_item(Item=item)
        return item
    else:
        raise UnauthorizedError


def get_test(test_id, teacher_id):
    response = test_table.get_item(Key={'test_id': test_id, 'teacher_id': teacher_id})
    test = response['Item']
    return test


def get_tests_by_teacher(teacher_id):
    response = test_table.scan(FilterExpression=Key('teacher_id').eq(teacher_id))
    tests = response['Items']
    return tests


def get_test_by_code(code):
    test = {}
    test_id = get_test_id_by_code(code)
    if test_id:
        response = test_table.scan(FilterExpression=Key('test_id').eq(test_id))
        test = response['Items'][0]
    return test


def update_test(payload):
    if validate_access_token(payload):
        if re.search(r'questions=:q', payload['expression'], 1):
            payload['attributes'][':q'] = generate_question_ids(payload['test_id'], payload['attributes'][':q'])

        response = test_table.update_item(
            Key={'test_id': payload['test_id'], 'teacher_id': payload['teacher_id']},
            UpdateExpression=payload['expression'],
            ExpressionAttributeValues=payload['attributes'],
            ReturnValues='ALL_NEW'
        )
        return response
    else:
        raise UnauthorizedError()


def delete_test(payload):
    if validate_access_token(payload):
        response = test_table.delete_item(Key={'test_id': payload['test_id'], 'teacher_id': payload['teacher_id']})
        return response
    else:
        raise UnauthorizedError()
