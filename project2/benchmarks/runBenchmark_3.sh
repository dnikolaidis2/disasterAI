#!/bin/bash

./runClient.sh -depth 6 -name test3_2 -p 6004 -minimaxstats >> test3_client2.txt &
./runClient.sh -depth 6 -nqsearch -name test3_1 -p 6004 -minimaxstats >> test3_client1.txt &

./server -g 200 -s -p 6004