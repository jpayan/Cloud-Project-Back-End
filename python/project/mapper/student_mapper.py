import boto3
from group_mapper import get_group
from applied_test_mapper import get_applied_tests_by_student

dynamodb = boto3.resource('dynamodb')
student_table = dynamodb.Table('cc414-nb-students')
ses = boto3.client('ses')


def create_student(payload):
    item = {
        'student_email': payload['student_email'],
        'full_name': payload['full_name']
    }
    student_table.put_item(Item=item)
    verify_email(payload['student_email'])
    return item


def get_student(student_email):
    response = student_table.get_item(Key={'student_email': student_email})
    student = response['Item']
    return student


def get_students_by_group(group_name, teacher_id):
    group = get_group(group_name, teacher_id)
    group_students = group['students']
    students = []

    for student_email in group_students:
        student = get_student(student_email)
        student['applied_tests'] = get_applied_tests_by_student(student_email)
        students.append(student)

    return students


def update_student(payload):
    response = student_table.update_item(
        Key={
            'student_email': payload['student_email']
        },
        UpdateExpression=payload['expression'],
        ExpressionAttributeValues=payload['attributes'],
        ReturnValues='ALL_NEW'
    )
    return response


def delete_student(payload):
    response = student_table.delete_item(Key={'student_email': payload['student_email']})
    return response


def verify_email(address):
    response = ses.verify_email_address(EmailAddress=address)
    return response
