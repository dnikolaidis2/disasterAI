#!/bin/bash

./runClient.sh -depth 6 >> client1.txt &
./runClient.sh -depth 5 -name basicAgent >> client2.txt &

./server -g 100 -s