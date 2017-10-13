import boto3
from project.utils import *

dynamodb = boto3.resource('dynamodb')
student_table = dynamodb.Table('cc414-nb-students')


def create_student(email, full_name):
    item = {
        'id': generate_id(),
        'email': email,
        'full_name': full_name,
    }
    student_table.put_item(Item=item)
    return item


def get_students():
    response = student_table.scan()
    tests = response['Items']
    return tests


def get_student(student_id):
    response = student_table.get_item(Key={'id': student_id})
    test = response['Item']
    return test


def update_student(student_id, expression, attributes):
    response = student_table.update_item(
        Key={
            'id': student_id
        },
        UpdateExpression=expression,
        ExpressionAttributeValues=attributes,
        ReturnValues='UPDATED_NEW'
    )
    return response


def delete_student(student_id):
    response = student_table.delete_item(Key={'id': student_id})
    return response
