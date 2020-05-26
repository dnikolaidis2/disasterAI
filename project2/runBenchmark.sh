#!/bin/bash

./runClient.sh -depth 5 >> client.txt &
./client > /dev/null &

./server -g 100 -s