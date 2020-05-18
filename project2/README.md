# TUC-Ants v1.01 COMP417-AI, Spring 2020
Affiliation: Technical University of Crete, Greece
Customized by Charilaos Akasiadis
Based on TUC Half-Checkers (COMP417-AI Project 2012)
by Ioannis Skoulakis

## Python Interface



## Requirements:

* Linux operating system
* libgtk2.0-dev
* Cython *for python interface*

## Compilation

`make [all]`  - to build client and server and libraries
`make client` - to build just the client
`make server` - to build just the server
`make guiServer` - to build just the guiServer
`make lib` - to build the libraries used by the Python interface

## Execution

`./guiServer`
`./server [-p port] [-g number_of_games] [-s (swap color after 
						   each game)]`
`./client [-i ip] [-p port]`
`chmod +x runClient.sh && ./runClient.sh [-h] [-i ip] [-p port]` - Python client

## Changes in last version

* Client sends the desired move to server and server 
	 executes doMove. Server sends new position to clients
	 after every move made.

