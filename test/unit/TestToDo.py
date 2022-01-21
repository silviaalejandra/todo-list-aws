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
        #self.assertEqual(200, put_item(self.text, self.dynamodb)[
        #                 'ResponseMetadata']['HTTPStatusCode'])
        print ('End: test_put_todo')


    def test_put_todo_error(self):
        print ('---------------------')
        print ('Start: test_put_todo_error')
        # Testing file functions
        from src.todoList import put_item
        
        # Table mock
        self.assertRaises(Exception, put_item(None, self.dynamodb))
        self.assertRaises(Exception, put_item("", self.dynamodb))
        self.assertRaises(Exception, put_item(" ", self.dynamodb))
        self.assertRaises(Exception, put_item("45", self.dynamodb))
        self.assertRaises(Exception, put_item(45, self.dynamodb))
        self.assertRaises(TypeError, put_item(True, self.dynamodb))
        print ('End: test_put_todo_error')


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


    def test_get_todo_error(self):
        print ('---------------------')
        print ('Start: test_get_todo_error')
        # Testing file functions
        from src.todoList import get_item
        
        # Table mock
        self.assertRaises(Exception, get_item(None, self.dynamodb))
        self.assertRaises(Exception, get_item(" ", self.dynamodb))
        self.assertRaises(TypeError, get_item(True, self.dynamodb))
        self.assertRaises(Exception, get_item("", self.dynamodb))
        self.assertRaises(Exception, get_item("50", self.dynamodb))
        self.assertRaises(Exception, get_item(50, self.dynamodb))
        self.assertRaises(Exception, get_item('', self.dynamodb))
        self.assertRaises(TypeError, get_item('#', self.dynamodb))
        print ('End: test_get_todo_error')


    # test por tranlate.py-------------------------
    # ---------------------------------------------
    def test_languaje(self):
        print ('---------------------')
        print ('Start: test_get_languaje---------------')
        from src.todoList import get_item_languaje
        
        # create an STS client object that represents a live connection to the 
        # STS service
        # sts_client = boto3.client('sts')
        # Call the assume_role method of the STSConnection object and pass the role
        # ARN and a role session name.
        # assumed_role_object=sts_client.assume_role(
        # RoleArn=os.environ['aws_role'],
        # RoleSessionName="LabRole"
        # )
        # From the response that contains the assumed role, get the temporary 
        # credentials that can be used to make subsequent API calls
        # credentials=assumed_role_object['Credentials']
        # session=boto3.session(region_name='us-east-1',
        # aws_access_key_id=credentials['AccessKeyId'],
        # aws_secret_access_key=credentials['SecretAccessKey'],
        # aws_session_token=credentials['SessionToken'])
        # comprehend = session.client('comprehend')
        comprehend = boto3.client('comprehend', region_name='us-east-1')
        # Testing file functions
        # Table mock
        print ('Texto:' + self.text)
        responseLanguaje = get_item_languaje(
                self.text,
                comprehend)
        print ('Response Languaje:' + str(responseLanguaje))
        self.assertEqual(200, responseLanguaje['statusCode'])
        self.assertEqual(responseLanguaje,self.origin_lang)
        print ('End: test_get_languaje---------------')


    # test por tranlate.py-------------------------
    # ---------------------------------------------
    def test_translate(self):
        print ('---------------------')
        print ('Start: test_translate---------------')
        from src.todoList import get_item_languaje
        from src.todoList import translate_item
        # create an STS client object that represents a live connection to the 
        # STS service
        sts_client = boto3.client('sts')
        # Call the assume_role method of the STSConnection object and pass the role
        # ARN and a role session name.
        assumed_role_object=sts_client.assume_role(
            RoleArn=os.environ['aws_role'],
            RoleSessionName="LabRole"
        )
        # From the response that contains the assumed role, get the temporary 
        # credentials that can be used to make subsequent API calls
        credentials=assumed_role_object['Credentials']
        comprehend = boto3.client('comprehend',
                    region_name='us-east-1',
                    aws_access_key_id=credentials['AccessKeyId'],
                    aws_secret_access_key=credentials['SecretAccessKey'],
                    aws_session_token=credentials['SessionToken']
                )
        translate = boto3.client('translate',
                    region_name='us-east-1',
                    aws_access_key_id=credentials['AccessKeyId'],
                    aws_secret_access_key=credentials['SecretAccessKey'],
                    aws_session_token=credentials['SessionToken']
                )
        # Testing file functions
        # Table mock
        print ('Texto:' + self.text)
        responseLanguaje = get_item_languaje(
                self.text,
                comprehend)
        print ('Response Languaje:' + str(responseLanguaje))
        print ('lenguaje origen:' + self.origin_lang + 
                ' Lenguaje destino:'+self.dest_lang)
        self.assertEqual(responseLanguaje,self.origin_lang)
        responseTranslate = translate_item(
                self.text,
                self.origin_lang,
                self.dest_lang,
                translate)
        print ('Response translate:' + str(responseTranslate))
        self.assertEqual(responseTranslate,self.traduccion)
        print ('End: test_translate---------------')

    
    # test por tranlate.py-------------------------
    # ---------------------------------------------
    def test_getlang_err(self):
        print ('---------------------')
        print ('Start: test_err_get_languaje---------------')
        from src.todoList import get_item_languaje
        # create an STS client object that represents a live connection to the 
        # STS service
        sts_client = boto3.client('sts')
        # Call the assume_role method of the STSConnection object and pass the role
        # ARN and a role session name.
        assumed_role_object=sts_client.assume_role(
            RoleArn=os.environ['aws_role'],
            RoleSessionName="LabRole"
        )
        # From the response that contains the assumed role, get the temporary 
        # credentials that can be used to make subsequent API calls
        credentials=assumed_role_object['Credentials']
        comprehend = boto3.client('comprehend',
                    region_name='us-east-1',
                    aws_access_key_id=credentials['AccessKeyId'],
                    aws_secret_access_key=credentials['SecretAccessKey'],
                    aws_session_token=credentials['SessionToken']
                )
        translate = boto3.client('translate',
                    region_name='us-east-1',
                    aws_access_key_id=credentials['AccessKeyId'],
                    aws_secret_access_key=credentials['SecretAccessKey'],
                    aws_session_token=credentials['SessionToken']
                )
        self.assertRaises(
            Exception,
            get_item_languaje(" ", comprehend))
        print ('End: test_err_get_languaje---------------')
    # ---------------------------------------------


    # test por tranlate.py-------------------------
    # ---------------------------------------------
    def test_translate_err(self):
        print ('---------------------')
        print ('Start: test_err_translate---------------')
        from src.todoList import translate_item
        # create an STS client object that represents a live connection to the 
        # STS service
        sts_client = boto3.client('sts')
        # Call the assume_role method of the STSConnection object and pass the role
        # ARN and a role session name.
        assumed_role_object=sts_client.assume_role(
            RoleArn=os.environ['aws_role'],
            RoleSessionName="LabRole"
        )
        # From the response that contains the assumed role, get the temporary 
        # credentials that can be used to make subsequent API calls
        credentials=assumed_role_object['Credentials']
        translate = boto3.client('translate',
                    region_name='us-east-1',
                    aws_access_key_id=credentials['AccessKeyId'],
                    aws_secret_access_key=credentials['SecretAccessKey'],
                    aws_session_token=credentials['SessionToken']
                )
        self.assertRaises(
            Exception,
            translate_item("prueba",
                " ", 
                "it",
                translate))
        self.assertRaises(
            Exception,
            translate_item("prueba",
                "es", 
                " ",
                translate))
        self.assertRaises(
            Exception,
            translate_item(None,
                " ", 
                "it",
                translate))
        print ('End: test_err_translate---------------')
    # ---------------------------------------------
 

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
        # Testing file functions
        self.assertRaises(TypeError, delete_item(None, self.dynamodb))
        self.assertRaises(Exception, delete_item(None, self.dynamodb))
        self.assertRaises(Exception, delete_item(" ", self.dynamodb))
        self.assertRaises(Exception, delete_item("45", self.dynamodb))
        self.assertRaises(Exception, delete_item(45, self.dynamodb))
        print ('End: test_delete_todo_error')



if __name__ == '__main__':
    unittest.main()