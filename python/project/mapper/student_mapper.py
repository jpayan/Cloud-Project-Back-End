import boto3
from project.utils import *

dynamodb = boto3.resource('dynamodb')
student_table = dynamodb.Table('cc414-nb-students')
ses = boto3.client('ses')


def create_student(email, full_name):
    item = {
        'email': email,
        'full_name': full_name,
    }
    student_table.put_item(Item=item)
    verify_email(email)
    return item


def get_students():
    response = student_table.scan()
    tests = response['Items']
    return tests


def get_student(email):
    response = student_table.get_item(Key={'email': email})
    test = response['Item']
    return test


def update_student(email, expression, attributes):
    response = student_table.update_item(
        Key={
            'email': email
        },
        UpdateExpression=expression,
        ExpressionAttributeValues=attributes,
        ReturnValues='UPDATED_NEW'
    )
    return response


def delete_student(email):
    response = student_table.delete_item(Key={'email': email})
    return response


def verify_email(address):
    response = ses.verify_email_address(
        EmailAddress=address
    )
    return response
