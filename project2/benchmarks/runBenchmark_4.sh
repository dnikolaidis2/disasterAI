#!/bin/bash

./runClient.sh -depth 6 -name test4_2 -p 6005 -perf >> test4_client2.txt &
./runClient.sh -depth 6 -nqsearch -name test4_1 -p 6005 -perf >> test4_client1.txt &

./server -g 200 -s -p 6005