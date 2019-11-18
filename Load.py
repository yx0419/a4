import boto3

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')


def copyFromOtherS3ToMyS3andLoadToDB():

    # get textdata from class S3
    responseFromGet = s3.Object('css490', 'input.txt').get()

    # copy/store that data into my S3
    var1 = responseFromGet['Body'].read()
    s3.Object('bucket436', 'input.txt').put(Body=var1)

    textdata = var1.decode("utf-8")
    items = textdata.splitlines()

    create_DB()
    table = dynamodb.Table('yunTable')

    for item in items:
        tokens = item.split()  # token: [Alex, Daniel, age=58, id=123]
        firstName = tokens[0]
        lastName = tokens[1]

        key_value_pair = {
            'first_name': firstName,
            'last_name': lastName
        }

        for j in range(2, len(tokens)):
            splitedPair = tokens[j].split("=")
            key_value_pair[splitedPair[0]] = splitedPair[1]

        table.put_item(
            Item=key_value_pair
        )


def create_DB():
    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName='yunTable',
        KeySchema=[
            {
                'AttributeName': 'last_name',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'first_name',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'last_name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'first_name',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='yunTable')

    # Print out some data about the table.
    print(table.item_count)
    return table
    # given input.txt is string text so have to use regular expression to parse it.
