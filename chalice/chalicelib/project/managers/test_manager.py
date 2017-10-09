import boto3
from project.models.test import Test

def create_test(name, subject):
    # Create Test And save to DynamoDB
    test = Test(name, subject)
    save_test(test)

def get_test(id):
    # Get Test
    pass

def update_test(id, test):
    # Update Test
    pass

def delete_test(id):
    # Delete Test
    pass

def save_test(test):
    # Save in DynamoDB
    pass