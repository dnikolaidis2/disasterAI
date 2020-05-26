#!/bin/bash

./runClient.sh -depth 7 &
./client &

./server -g 100 -s