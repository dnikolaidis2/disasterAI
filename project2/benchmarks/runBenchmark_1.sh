#!/bin/bash

./runClient.sh -depth 6 -name test1_2 -p 6002 -minimaxstats >> test1_client2.txt &
./runClient.sh -depth 6 -nindanger -nenamsse -nqsearch -name test1_1 -p 6002 -minimaxstats >> test1_client1.txt &

./server -g 200 -s -p 6002