#!/bin/bash

./runClient.sh -depth 6 -name test5_2 -p 6006 -minimaxstats >> test5_client2.txt &
./runClient.sh -depth 6 -nalphabeta -name test5_1 -p 6006 -minimaxstats >> test5_client1.txt &

./server -g 10 -s -p 6006