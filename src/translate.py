import logging
import json
import boto3
import os
import todoList
import decimalencoder

translate = boto3.client('translate')
dynamodb = boto3.client('dynamodb')
firehose = boto3.client('firehose')
comprehend = boto3.client('comprehend')

TABLE_NAME = os.getenv('DYNAMODB_TR_TABLE')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(event)
    item = todoList.get_item(event['pathParameters']['id'])
    logger.info(item)
    target_language=event['pathParameters']['language']
    logger.info(target_language)
    
    try:
        # The Lambda function queries the Amazon DynamoDB table to check whether
        # the review has already been translated. If the translated review
        # is already stored in Amazon DynamoDB, the function returns it.
        table_response = dynamodb.get_item(
            TableName=TABLE_NAME,
            Key={
                'review_id': {
                    'S': item['text'],
                },
                'language': {
                    'S': target_language,
                },
            }
        )
        logger.info(table_response)
        if 'Item' in table_response:
            # Creo la esrtuctura de respuesta del tipo todolist
            itemtranslated = {
                'id': item['id'],
                'text': table_response['review'],
                'checked': item['checked']
            }
            response = {
                "statusCode": 200,
                "body": json.dumps(itemtranslated, cls=decimalencoder.DecimalEncoder)
            }
            logger.error(response)
            return response

    except Exception as e:
        # logger.error(response)
        raise Exception("[ErrorMessage]: " + str(e))
  
    try:
        # The Lambda function calls the TranslateText operation and passes the
        # review, the source language, and the target language to get the
        # translated review.
        source_language = comprehend.detect_dominant_language(item['text'])
        logger.info(source_language)
        result = translate.translate_text(Text=item['text'], SourceLanguageCode=source_language, TargetLanguageCode=target_language)
        logging.info("Translation output: " + str(result))
    except Exception as e:
        # logger.error(response)
        raise Exception("[ErrorMessage]: " + str(e))

    try:
        # After the review is translated, the function stores it using
        # the Amazon DynamoDB putItem operation. Subsequent requests
        # for this translated review are returned from Amazon DynamoDB.
        response = dynamodb.put_item(
        TableName=TABLE_NAME,
        Item={
            'review_id': {
                'S': item['text'],
            },
            'language': {
                'S': target_language,
            },
            'review': {
                'S': result.get('TranslatedText')
            }
        }
        )
        logger.info(response)
    except Exception as e:
        logger.error(e)
        raise Exception("[ErrorMessage]: " + str(e))
    # Creo la esrtuctura de respuesta del tipo todolist
    itemtranslated = {
        'id': item['id'],
        'text': result.get('TranslatedText'),
        'checked': item['checked']
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(itemtranslated, cls=decimalencoder.DecimalEncoder)
    }
    logger.error(response)
    return response