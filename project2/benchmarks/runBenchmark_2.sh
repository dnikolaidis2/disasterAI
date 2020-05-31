#!/bin/bash

./runClient.sh -depth 6 -name test2_2 -p 6003 -minimaxstats >> test2_client2.txt &
./runClient.sh -depth 6 -nenamsse -nqsearch -name test2_1 -p 6003 -minimaxstats >> test2_client1.txt &

./server -g 200 -s -p 6003