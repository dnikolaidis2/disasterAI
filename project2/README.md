# TUC-Ants v1.01 COMP417-AI, Spring 2020
This is the a Python implementation of an agent for the game TUC-Ants for the course COMP417. 

Affiliation: Technical University of Crete, Greece
Customized by Charilaos Akasiadis
Based on TUC Half-Checkers (COMP417-AI Project 2012)
by Ioannis Skoulakis

## Python Interface
The Python interface for the game hooks into the *comm* and *board* parts of the C code by 
compiling them into a shared object and calling the native C code. Compiling the libraries 
is a requirement for running the python agent and setting the LD_LIBRARY_PATH environment variable
to the path of the .so files is also required. The script *runClient.sh* will take care off 
loading the environment variable for you and pass any arguments you have on to the script.


## Requirements:

* Linux operating system
* libgtk2.0-dev
* Cython *for python interface*

## Compilation

`make [all]`  - to build client and server and libraries

`make client` - to build just the client

`make server` - to build just the server

`make guiServer` - to build just the guiServer

`make lib` - to build the libraries **required** by the Python interface

## Execution

`./guiServer`

`./server [-p port] [-g number_of_games] [-s (swap color after 
						   each game)]`
						   
`./client [-i ip] [-p port]`

Python agent:

```
chmod +x runClient.sh && client.py [-h] [-i ip] [-p port] [-name NAME] [-depth DEPTH]
                                   [-nalphabeta] [-qsearch] [-nindanger] [-nenamsse]
                                   [-minimaxstats] [-perf]
```
## Changes in last version

* Client sends the desired move to server and server 
	 executes doMove. Server sends new position to clients
	 after every move made.

