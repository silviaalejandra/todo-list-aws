import os
import boto3
import time
import uuid
import json
import functools
import logging
from botocore.exceptions import ClientError, ParamValidationError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_table(dynamodb=None):
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


def get_comprehend(comprehend=None):
    if not comprehend:
        comprehend = boto3.client(service_name='comprehend')
        # print('Instanciado--------------')
    logger.info(comprehend)
    return comprehend


def get_translate(translate=None):
    if not translate:
        translate = boto3.client(service_name='translate')
        # print('Instanciado--------------')
    logger.info(translate)
    return translate


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


def get_item_languaje(text, comprehend=None):
    comprehend = get_comprehend(comprehend)
    logger.info(comprehend)
    try:
        logger.info("Detect text lang: " + str(text))
        response = comprehend.detect_dominant_language(
                Text=text
        )
    except ClientError as e:
        logger.exception("Couldn't detect languages.")
        print(e.response['Error']['Message'])
    else:
        languages = response['Languages']
        logger.info("Detected %s languages.", len(languages))

        # Ordeno la lista de lenguajes por el mejor score
        order_languaje = sorted(
                response['Languages'],
                key=lambda k: k['Score'],
                reverse=True)
        # Obtengo el primero de la lista ordenada
        thelangcode = order_languaje[0]['LanguageCode']
        return str(thelangcode)


def translate_text(text, s_lang, t_lang, translate=None):
    logging.info('get translateclient --------------------')
    translate = get_translate(translate)
    logger.info(translate)

    try:
        logger.info(translate)
        logger.info("texto: " + text)
        logger.info("Lenguaje entrada: " + str(s_lang))
        logger.info("Lenguaje salida: " + str(t_lang))

        response = translate.translate_text(
                Text=text,
                SourceLanguageCode=s_lang,
                TargetLanguageCode=t_lang
        )
    except ClientError as e:
        logger.exception("No fue posible realizar la traduccion")
        print(e.response['Error']['Message'])
    except ParamValidationError:
        logger.exception("Problemas de parametros")
    else:
        logger.info("traduccion.")
        logger.info(response)
        return str(response['TranslatedText'])


# Traduzco el texto ingresado
# pre requisitos: ID y Lenguaje
def translate_item(key, language, translate=None, dynamodb=None):
    logging.info('inicio translate --------------------')
    table = get_table(dynamodb)
    logging.info('get table --------------------')
    logging.info(table)

    try:
        logging.info('get item --------------------')
        item = table.get_item(
            Key={
                'id': key
            }
        )
        thetext = item['Item']['text']
        logging.info(item)
        logging.info(thetext)
        logging.info('source languaje --------------------')
        source_language = get_item_languaje(
                        thetext
        )
        logging.info(source_language)

        translateresult = translate_text(
                thetext,
                source_language,
                language
        )
        logging.info("Translation output: " + str(translateresult))

        # Creo la esrtuctura de respuesta del tipo todolist
        # temtranslated = {
        #    'id': key,
        #    'text': translateresult,
        #    'checked':item['Item']['checked']
        # }
        item['Item']['text'] = translateresult

        response = {
            "statusCode": 200,
            # "body": json.dumps(itemtranslated, 
            #       cls=decimalencoder.DecimalEncoder)
            "body": json.dumps(item['Item'])
        }
        # logger.info(response)
        logging.info(response)

    except ClientError as e:
        logger.exception("Couldn't translate.")
        print(e.response['Error']['Message'])
    else:
        return response


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
