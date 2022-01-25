# import json
import logging
# import boto3
import todoList
# import decimalencoder

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)


def translate(event, context):
    # comprehend = boto3.client(service_name='comprehend')
    # translate = boto3.client(service_name='translate')

    logging.info('inicio traducciones --------------------')
    logging.info(event)
    # data = json.loads(event['body'])
    # logging.info('data --------------------')
    # logging.info(data)
    if 'id' not in event['pathParameters'] or 
            'language' not in event['pathParameters']:
        logging.error("Validation Failed")
        raise Exception("Couldn't translate the todo item.")
        # SG20220117 Se elimina debido a la salida por el rise exception
        # return

    result = todoList.translate_item(
        event['pathParameters']['id'], event['pathParameters']['language']  # ,
        # translate, comprehend
    )
    # create a response
    logging.info('resultado de la salida')
    logging.info(result)
    # response = {
    #    "statusCode": 200,
    #    "body": json.dumps(result,
    #                       cls=decimalencoder.DecimalEncoder)
    # }

    # return response
    return result
