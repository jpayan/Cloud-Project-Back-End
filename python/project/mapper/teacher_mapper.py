import uuid
import boto3

ses = boto3.client('ses')

dynamodb = boto3.resource('dynamodb')
test_table = dynamodb.Table('Tests')


def create_table(table_name):
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'S'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'name',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'subject',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'questions',
                    'AttributeType': 'LM'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
    except Exception as e:
        return 'Error: ' + e.message
    else:
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        return {'Success': table_name + ' created successfully.'}


def create_test(name, subject):
    item = {
        'id': generate_id(),
        'name': name,
        'subject': subject
    }
    try:
        test_table.put_item(Item=item)
    except Exception as e:
        return 'Error: ' + e.message
    else:
        send_emails(['jalexpayan@gmail.com', 'jpayan@cetys.edu.mx'])
        return item

def get_tests():
    try:
        response = test_table
    except Exception as e:
        return 'Error: ' + e.message
    else:
        tests = response['Items']
        return tests


def get_test(id):
    try:
        response = test_table.get_item(Key={'id': id})
    except Exception as e:
        return 'Error: ' + e.message
    else:
        test = response['Item']
        return test


def update_test(id, test):
    # Update Test
    pass


def delete_test(id):
    # Delete Test
    pass


def generate_id():
    # Generate UUID for table item
    uid = str(uuid.uuid4())
    return uid