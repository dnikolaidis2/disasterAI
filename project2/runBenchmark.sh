#!/bin/bash

./runClient.sh -depth 6 -p 6002 -minimaxstats >> client1.txt &
./runClient.sh -depth 6 -nqsearch -name basicAgent -p 6002 -minimaxstats >> client2.txt &

./server -g 500 -s -p 6002