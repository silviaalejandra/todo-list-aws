#!/bin/bash

source todo-list-aws/bin/activate
set -x
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "PYTHONPATH: $PYTHONPATH"
export DYNAMODB_TABLE=todoUnitTestsTable
export aws_key_id=ASIAXKUUA7O3QX4EZRDO
export aws_key=dhD6jEwmIm2ILhprYlAKB+yJnT/tqL6E1/fZv6mg
export aws_token=FwoGZXIvYXdzEAgaDEDeJc+pXVbxCbQEFCLLAdCwos/TKT5DB4qsg3nYwacigix1SdJkb55L8UyHmVFlvH055xpn0THSnLyubSxx3dIa8G9IK9uSV4NRef5UxsnbfqnolGJSMW4xlkc2BOwqUrWw8FZFO3dxvP8MVDg7roo2kXtxaDk413RhbTcnqyv7DLNsN0mcDD9ikuCD1cHtVA6IBRKHVQKOBZ7i4KUIdtLH38dAnUouz08NVl138ut8/ebsLTpQF19lGTANZd83iuxb/VoAHlCowb6IHclq44yXLUyPsOOL6t5fKL/Fp48GMi3DkMhgmlGJH3dmj3gkgFxl9agNnRu6h0f7dfPp3+P2e5+fLDi0L//d7UwVmyI=
export aws_role=arn:aws:iam::503895358391:role/LabRole
python test/unit/TestToDo.py
pip show coverage
coverage run --include=src/todoList.py  test/unit/TestToDo.py
coverage report -m
coverage xml
