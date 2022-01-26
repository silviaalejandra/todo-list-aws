#!/bin/bash
# Se instancia el docker de dynamoBD para las pruebas 
#  de regresion que requieren una base local
pwd

systemctl status docker
## Crear red de docker

## Levantar el contenedor de dynamodb en la red de sam con el nombre de dynamodb
docker run -p 8002:8000 --network sam --name dynamodb2 -d amazon/dynamodb-local

docker ps -a
