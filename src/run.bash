#!/bin/bash

source=("$1.txt")
echo "$source"

python3 parser.py tests/$source
python3 VM.py