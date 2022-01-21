import os
import boto3
import time
import uuid
import json
import functools
from botocore.exceptions import ClientError


def get_table(dynamodb=None):   # pragma: no cover
    if not dynamodb:
        URL = os.environ['ENDPOINT_OVERRIDE']
        if URL:
            print('URL dynamoDB:'+URL)
            boto3.client = functools.partial(boto3.client, endpoint_url=URL)
            boto3.resource = functools.partial(boto3.resource,
                                               endpoint_url=URL)
        dynamodb = boto3.resource("dynamodb")
    # fetch todo from the database
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    return table


def get_item(key, dynamodb=None):
    table = get_table(dynamodb)
    try:
        result = table.get_item(
            Key={
                'id': key
            }
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        if 'Item' in result:
            print('Result getItem:'+str(result))
            return result['Item']
        return


def get_items(dynamodb=None):
    table = get_table(dynamodb)
    # fetch todo from the database
    result = table.scan()
    return result['Items']


def put_item(text, dynamodb=None):
    table = get_table(dynamodb)
    timestamp = str(time.time())
    print('Table name:' + table.name)
    item = {
        'id': str(uuid.uuid1()),
        'text': text,
        'checked': False,
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }
    try:
        # write the todo to the database
        table.put_item(Item=item)
        # create a response
        response = {
            "statusCode": 200,
            "body": json.dumps(item)
        }

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response


# obtengo lenguaje dominante
def get_item_languaje(text, comprehend=None):  # pragma: no cover
    if not comprehend:
        comprehend = boto3.client('comprehend')
    try:
        # source_language es inferido con el servicio comprehend de AWS
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html
        result = comprehend.detect_dominant_language(
            Text=text
        )

        # Ordeno la lista de lenguajes por el mejor score
        order_languaje = sorted(
                result["Languages"],
                key=lambda k: k['Score'],
                reverse=True)

        # Obtengo el primero de la lista ordenada
        thelangcode = order_languaje[0]['LanguageCode']

        # create a response
        response = {
            "statusCode": 200,
            "body": json.dumps(thelangcode)
        }
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response


# Traduzco el texto ingresado
def translate_item(text, lang, langdest, translate=None):  # pragma: no cover
    if not translate:
        translate = boto3.client('translate')
    try:
        result = translate.translate_text(
                    Text=text,
                    SourceLanguageCode=lang,
                    TargetLanguageCode=langdest
                )

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return result.get('TranslatedText')


def update_item(key, text, checked, dynamodb=None):
    table = get_table(dynamodb)
    timestamp = int(time.time() * 1000)
    # update the todo in the database
    try:
        result = table.update_item(
            Key={
                'id': key
            },
            ExpressionAttributeNames={
              '#todo_text': 'text',
            },
            ExpressionAttributeValues={
              ':text': text,
              ':checked': checked,
              ':updatedAt': timestamp,
            },
            UpdateExpression='SET #todo_text = :text, '
                             'checked = :checked, '
                             'updatedAt = :updatedAt',
            ReturnValues='ALL_NEW',
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return result['Attributes']


def delete_item(key, dynamodb=None):
    table = get_table(dynamodb)
    # delete the todo from the database
    try:
        table.delete_item(
            Key={
                'id': key
            }
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return


def create_todo_table(dynamodb):
    # For unit testing
    tableName = os.environ['DYNAMODB_TABLE']
    print('Creating Table with name:' + tableName)
    table = dynamodb.create_table(
        TableName=tableName,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName=tableName)
    if (table.table_status != 'ACTIVE'):
        raise AssertionError()   # pragma: no cover

    return table
