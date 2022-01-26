#!/bin/bash
# Se instancia el docker de dynamoBD para las pruebas 
#  de regresion que requieren una base local

systemctl status docker
## Crear red de docker
su docker network create samtest

## Levantar el contenedor de dynamodb en la red de sam con el nombre de dynamodb
su docker run -p 8001:8000 --network samtest --name dynamodb2 -d amazon/dynamodb-local

## Crear la tabla en local, para poder trabajar localmemte
su aws dynamodb create-table --table-name localtest-DynamoDbTable --region us-east-1 --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --endpoint-url http://localhost:8001

su docker ps -a
