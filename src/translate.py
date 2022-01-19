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
        # The Lambda function calls the TranslateText operation and passes the
        # review, the source language, and the target language to get the
        # translated review.

        # source_language es inferido con el servicio comprehend de AWS
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html
        source_language = comprehend.detect_dominant_language(
            Text = item['text']
        )
        logger.info(source_language)
        result = translate.translate_text(
                    Text=item['text'], 
                    SourceLanguageCode=source_language, 
                    TargetLanguageCode=target_language
                )
        logging.info("Translation output: " + str(result))
    except Exception as e:
        # logger.error(response)
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