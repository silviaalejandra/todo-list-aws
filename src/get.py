import json
import logging
import decimalencoder
import todoList

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get(event, context):
    # create a response
    logger.info(event)
    item = todoList.get_item(event['pathParameters']['id'])
    if item:
        response = {
            "statusCode": 200,
            "body": json.dumps(item,
                               cls=decimalencoder.DecimalEncoder)
        }
    else:
        response = {
            "statusCode": 404,
            "body": ""
        }
    return response
