import boto3
from project.utils import *

dynamodb = boto3.resource('dynamodb')
student_table = dynamodb.Table('cc414-nb-students')
ses = boto3.client('ses')


def create_student(student_email, full_name):
    item = {
        'student_email': student_email,
        'full_name': full_name,
    }
    student_table.put_item(Item=item)
    verify_email(student_email)
    return item


def get_students():
    response = student_table.scan()
    students = response['Items']
    return students


def get_student(student_email):
    response = student_table.get_item(Key={'student_email': student_email})
    student = response['Item']
    return student


def update_student(student_email, expression, attributes):
    response = student_table.update_item(
        Key={
            'student_email': student_email
        },
        UpdateExpression=expression,
        ExpressionAttributeValues=attributes,
        ReturnValues='UPDATED_NEW'
    )
    return response


def delete_student(student_email):
    response = student_table.delete_item(Key={'student_email': student_email})
    return response


def verify_email(address):
    response = ses.verify_email_address(
        EmailAddress=address
    )
    return response
