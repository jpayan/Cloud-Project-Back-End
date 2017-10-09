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
    # Create Test And save to DynamoDB
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


def send_emails(emails):

    verified_emails = ''
    try:
        for email in emails:
            verified_emails += ses.verify_email_address(
                EmailAddress=email
            )
    except Exception as e:
        return 'Error: ' + e.message

    try:
        ses.send_email(
            Destination={
                'BccAddresses': [
                ],
                'CcAddresses': [
                ],
                'ToAddresses': [
                    'jalexpayan@gmail.com',
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': 'This message body contains HTML formatting. '
                                'It can, for example, contain links like this one:'
                                '<a class="ulink" href="http://docs.aws.amazon.com/ses/latest/DeveloperGuide" target="_blank">'
                                'Amazon SES Developer Guide'
                                '</a>.'
                    },
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': 'This is the message body in text format.',
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': 'Test email',
                },
            },
            ReplyToAddresses=[
            ],
            ReturnPath='',
            ReturnPathArn='',
            Source='jpayan@cetys.edu.mx',
            SourceArn=''
        )
    except Exception as e:
        return 'Error: ' + e.message
