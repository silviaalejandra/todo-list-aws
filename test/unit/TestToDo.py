# from pprint import pprint
import warnings
import unittest
import boto3
from moto import mock_dynamodb2
import sys
import os
import json
# import random
# import uuid

@mock_dynamodb2
class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        print ('---------------------')
        print ('Start: setUp')
        warnings.filterwarnings(
            "ignore",
            category=ResourceWarning,
            message="unclosed.*<socket.socket.*>")
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message="callable is None.*")
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message="Using or importing.*")
        """Create the mock database and table"""
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.comprehend =  boto3.client(service_name='comprehend', region_name='us-east-1')
        self.translate =  boto3.client(service_name='translate', region_name='us-east-1')
        self.is_local = 'true'
        self.uuid = "123e4567-e89b-12d3-a456-426614174000"
        self.text = "Aprender DevOps y Cloud en la UNIR"
        self.origin_lang = "es"
        self.dest_lang = "it"
        self.traduccion = "Scopri DevOps e Cloud presso UNIR"
        from src.todoList import create_todo_table
        self.table = create_todo_table(self.dynamodb)
        #self.table_local = create_todo_table()
        print ('End: setUp')


    def tearDown(self):
        print ('---------------------')
        print ('Start: tearDown')
        """Delete mock database and table after test is run"""
        self.table.delete()
        print ('Table deleted succesfully')
        #self.table_local.delete()
        self.dynamodb = None
        print ('End: tearDown')


    def test_get_table(self):
        print ('---------------------')
        print ('Start: test_get_table')
        from src.todoList import get_table

        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
        endpoint = os.environ["ENDPOINT_OVERRIDE"]
        os.environ["ENDPOINT_OVERRIDE"] = "http://localhost:8001"
        result = get_table(None)
        self.assertIsNotNone(result)
        os.environ["ENDPOINT_OVERRIDE"] = endpoint
        print ('End: test_get_table')


    def test_table_exists(self):
        print ('---------------------')
        print ('Start: test_table_exists')
        #self.assertTrue(self.table)  # check if we got a result
        #self.assertTrue(self.table_local)  # check if we got a result

        print('Table name:' + self.table.name)
        tableName = os.environ['DYNAMODB_TABLE'];
        # check if the table name is 'ToDo'
        self.assertIn(tableName, self.table.name)
        #self.assertIn('todoTable', self.table_local.name)
        print ('End: test_table_exists')
    

    def test_get_translate(self):
        print ('---------------------')
        print ('Start: test_get_translate')
        from src.todoList import get_translate

        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
        result = get_translate(None)
        self.assertIsNotNone(result)
        print ('End: test_get_translate')


    def test_get_comprehend(self):
        print ('---------------------***---')
        print ('Start: test_get_comprehend')
        from src.todoList import get_comprehend

        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
        result = get_comprehend(None)
        self.assertIsNotNone(result)
        print ('End: test_get comprehend')


    def test_get_todo_error(self):
        print ('---------------------')
        print ('Start: test_get_todo_error')
        # Testing file functions
        from src.todoList import get_item
        
        dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
        # Table mock
        self.assertRaises(TypeError, get_item(None, dynamodb))
        self.assertRaises(Exception, get_item(" ", self.dynamodb))
        self.assertRaises(TypeError, get_item(True, self.dynamodb))
        self.assertRaises(Exception, get_item("", self.dynamodb))
        self.assertRaises(Exception, get_item("50", self.dynamodb))
        self.assertRaises(TypeError, get_item(50, self.dynamodb))
        self.assertRaises(Exception, get_item('', self.dynamodb))
        self.assertRaises(TypeError, get_item('#', self.dynamodb))
        print ('End: test_get_todo_error')


    def test_get_todo(self):
        print ('---------------------')
        print ('Start: test_get_todo')
        from src.todoList import get_item
        from src.todoList import put_item
        
        # Testing file functions
        # Table mock
        responsePut = put_item(self.text, self.dynamodb)
        print ('Response put_item:' + str(responsePut))
        idItem = json.loads(responsePut['body'])['id']
        print ('Id item:' + idItem)
        self.assertEqual(200, responsePut['statusCode'])
        responseGet = get_item(
                idItem,
                self.dynamodb)
        print ('Response Get:' + str(responseGet))
        self.assertEqual(
            self.text,
            responseGet['text'])
        print ('End: test_get_todo')


    def test_put_todo(self):
        print ('---------------------')
        print ('Start: test_put_todo')
        # Testing file functions
        from src.todoList import put_item
        # Table local
        response = put_item(self.text, self.dynamodb)
        print ('Response put_item:' + str(response))
        self.assertEqual(200, response['statusCode'])
        # Table mock
        # self.assertEqual(200, put_item(self.text, self.dynamodb)[
        #                 'ResponseMetadata']['HTTPStatusCode'])
        print ('End: test_put_todo')


    def test_put_todo_error(self):
        print ('---------------------')
        print ('Start: test_put_todo_error')
        # Testing file functions
        from src.todoList import put_item
        
        dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
        # Table mock
        self.assertRaises(Exception, put_item(None, dynamodb))
        self.assertRaises(TypeError, put_item(None, self.dynamodb))
        self.assertRaises(TypeError, put_item('', self.dynamodb))
        self.assertRaises(Exception, put_item(" ", self.dynamodb))
        self.assertRaises(Exception, put_item("45", self.dynamodb))
        self.assertRaises(Exception, put_item(False, self.dynamodb))
        self.assertRaises(TypeError, put_item(False, self.dynamodb))
        print ('End: test_put_todo_error')


    def test_get_languaje(self):
        print ('---------------------')
        print ('Start: test_get_languaje')
        from src.todoList import get_item_languaje
        
        # Testing file functions
        print ('Texto:' + self.text)
        responseLanguaje = get_item_languaje(
                self.text,
                self.comprehend)
        print ('Response Languaje:' + str(responseLanguaje))
        self.assertEqual(responseLanguaje, self.origin_lang)
        print ('End: test_get_languaje')


    def test_get_language_err(self):
        print ('---------------------')
        print ('Start: test_err_get_languaje---------------')
        from src.todoList import get_item_languaje

        self.assertRaises(
            Exception,
            get_item_languaje("*", self.comprehend))
        print ('End: test_err_get_languaje---------------')


    def test_translate_text_err(self):
        print ('---------------------')
        print ('Start: test_err_translate_text')
        from src.todoList import translate_text
        
        self.assertRaises(Exception,
            translate_text(self.text,
                None,
                "es",
                self.translate))
        self.assertRaises(TypeError,
            translate_text(self.text,
                "ii",
                "es",
                self.translate))
        self.assertRaises(Exception,
            translate_text(self.text,
                "ii",
                "es", 
                self.translate))
        print ('End: test_err_translate_text')


    def test_translate_text(self):
        print ('---------------------')
        print ('Start: test_translate_text')
        from src.todoList import translate_text
        
        # Testing file functions
        print ('Texto:' + self.text)
        response = translate_text(
                self.text,
                self.origin_lang,
                self.dest_lang,
                self.translate)
        print ('Response Translate:' + str(response))
        self.assertEqual(response, self.traduccion)
        print ('End: test_translate_text')


   # test por tranlate.py-------------------------
    # ---------------------------------------------
    def test_translate_item(self):
        print ('---------------------')
        print ('Start: test_translate_item')
        from src.todoList import get_item_languaje
        from src.todoList import translate_item
        from src.todoList import put_item

        responsePut = put_item(self.text, self.dynamodb)
        print ('Response PutItem' + str(responsePut))
        idItem = json.loads(responsePut['body'])['id']
        textoItem = json.loads(responsePut['body'])['text']
        print ('Id item:' + idItem)
        # Testing file functions
        # Table mock
        print ('Texto:' + textoItem)
        responseLanguaje = get_item_languaje(
                textoItem,
                self.comprehend)
        
        print ('Response Languaje:' + str(responseLanguaje))
        print ('lenguaje origen:' + self.origin_lang + 
                ' Lenguaje destino:'+self.dest_lang)
        self.assertEqual(responseLanguaje, self.origin_lang)
        
        responseTranslate = translate_item(
                textoItem,
                responseLanguaje,
                self.dest_lang,
                self.translate)
        print ('Response translate:' + str(responseTranslate))
        self.assertEqual(200, responseTranslate['statusCode'])
        print ('End: test_translate_item')


    def test_translate_item_err(self):
        print ('---------------------')
        print ('Start: test_translate_item_err')
        from src.todoList import translate_item
        from src.todoList import put_item

        responsePut = put_item(self.text, self.dynamodb)
        print ('Response PutItem' + str(responsePut))
        idItem = json.loads(responsePut['body'])['id']
        print ('Id item:' + idItem)
        
        self.assertRaises(Exception,
            translate_item(idItem,
                "ii", 
                self.translate,
                self.dynamodb))
                
        self.assertRaises(TypeError,
            translate_item(idItem,
                None, 
                self.translate,
                self.dynamodb))
                
        print ('End: test_err_translate')
 

    def test_update_todo(self):
        print ('---------------------')
        print ('Start: test_update_todo')
        from src.todoList import put_item
        from src.todoList import update_item
        from src.todoList import get_item
        updated_text = "Aprender más cosas que DevOps y Cloud en la UNIR"
        # Testing file functions
        # Table mock
        responsePut = put_item(self.text, self.dynamodb)
        print ('Response PutItem' + str(responsePut))
        idItem = json.loads(responsePut['body'])['id']
        print ('Id item:' + idItem)
        result = update_item(idItem, updated_text,
                            "false",
                            self.dynamodb)
        print ('Result Update Item:' + str(result))
        self.assertEqual(result['text'], updated_text)
        print ('End: test_update_todo')


    def test_update_todo_error(self):
        print ('---------------------')
        print ('Start: atest_update_todo_error')
        from src.todoList import put_item
        from src.todoList import update_item
        updated_text = "Aprender más cosas que DevOps y Cloud en la UNIR"
        # Testing file functions
        # Table mock
        responsePut = put_item(self.text, self.dynamodb)
        print ('Response PutItem' + str(responsePut))
        self.assertRaises(
            Exception,
            update_item(
                updated_text,
                None,
                "false",
                self.dynamodb))
        self.assertRaises(
            TypeError,
            update_item(
                None,
                self.uuid,
                "false",
                self.dynamodb))
        self.assertRaises(
            Exception,
            update_item(
                updated_text,
                self.uuid,
                None,
                self.dynamodb))
        print ('End: atest_update_todo_error')


    def test_delete_todo(self):
        print ('---------------------')
        print ('Start: test_delete_todo')
        from src.todoList import delete_item
        from src.todoList import put_item
        from src.todoList import get_items
        # Testing file functions
        # Table mock
        responsePut = put_item(self.text, self.dynamodb)
        print ('Response PutItem' + str(responsePut))
        idItem = json.loads(responsePut['body'])['id']
        print ('Id item:' + idItem)
        delete_item(idItem, self.dynamodb)
        print ('Item deleted succesfully')
        self.assertTrue(len(get_items(self.dynamodb)) == 0)
        print ('End: test_delete_todo')

    def test_delete_todo_error(self):
        print ('---------------------')
        print ('Start: test_delete_todo_error')
        from src.todoList import delete_item
        
        dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
        
        # Testing file functions
        self.assertRaises(TypeError, delete_item(None, self.dynamodb))
        self.assertRaises(Exception, delete_item(None, dynamodb))
        self.assertRaises(Exception, delete_item(None, self.dynamodb))
        self.assertRaises(Exception, delete_item(" ", self.dynamodb))
        self.assertRaises(Exception, delete_item("45", self.dynamodb))
        print ('End: test_delete_todo_error')


    def test_list_todo(self):
        print ('---------------------')
        print ('Start: test_list_todo')
        from src.todoList import put_item
        from src.todoList import get_items

        # Testing file functions
        # Table mock
        put_item(self.text, self.dynamodb)
        result = get_items(self.dynamodb)
        print ('Response GetItems' + str(result))
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0]['text'] == self.text)
        print ('End: test_list_todo')


if __name__ == '__main__':
    unittest.main()