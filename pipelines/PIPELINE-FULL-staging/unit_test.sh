#!/bin/bash

source todo-list-aws/bin/activate
set -x
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "PYTHONPATH: $PYTHONPATH"
export DYNAMODB_TABLE=todoUnitTestsTable
export aws_role=arn:aws:iam::${AWS::AccountId}:role/LabRole
export AWS_ROLE=arn:aws:iam::${AWS::AccountId}:role/LabRole
sh test/unit/localDB.sh
sudo docker ps -a
python test/unit/TestToDo.py
 pip show coverage
coverage run --include=src/todoList.py  test/unit/TestToDo.py
coverage report -m
coverage xml
sudo docker stop dynamodb2
