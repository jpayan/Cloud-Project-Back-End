import boto3
from boto3.dynamodb.conditions import Key
from applied_test_mapper import get_test_id_by_code
from project.utils import generate_id

dynamodb = boto3.resource('dynamodb')
test_table = dynamodb.Table('cc414-nb-tests')


def create_test(payload):
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


def update_test(test_id, teacher_id, payload):
    response = test_table.update_item(
        Key={'test_id': test_id, 'teacher_id': teacher_id},
        UpdateExpression=payload['expression'],
        ExpressionAttributeValues=payload['attributes'],
        ReturnValues='ALL_NEW'
    )
    return response


def delete_test(test_id, teacher_id):
    response = test_table.delete_item(Key={'test_id': test_id, 'teacher_id': teacher_id})
    return response
