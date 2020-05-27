#!/bin/bash

./runClient.sh -depth 5 >> client1.txt &
./runClient.sh -depth 5 -ev_switch -name basicAgent >> client2.txt &

./server -g 100 -s