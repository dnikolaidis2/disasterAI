#!/bin/bash

export LD_LIBRARY_PATH=$PWD

python3 client.py "${@}"