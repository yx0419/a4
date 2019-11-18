import boto3

from botocore.exceptions import ClientError

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('yunTable')

client = boto3.client('dynamodb')


def deleteS3File():
    s3.Object('bucket436', 'input.txt').delete()  # clears s3 bucket


def delete_DB_Table():

    try:
        response = client.describe_table(TableName='yunTable')
        table.delete()

    except ClientError as ce:
        if ce.response['Error']['Code'] == 'ResourceNotFoundException':
            print("Table yunTable does not exist. Create the table first and try again.")
            return "failed"
