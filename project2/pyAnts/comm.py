from ctypes import CDLL, c_int, c_char_p, pointer, create_string_buffer
from .globals import MAX_NAME_LENGTH
from collections import namedtuple
from os import environ

MAXPENDING = 10
NM_NEW_POSITION = 1
NM_COLOR_W = 2
NM_COLOR_B = 3
NM_REQUEST_MOVE = 4
NM_PREPARE_TO_RECEIVE_MOVE = 5
NM_REQUEST_NAME = 6
NM_QUIT = 7


if "LD_LIBRARY_PATH" not in environ:
    raise ImportError("LD_LIBRARY_PATH must be set to the location of libcomm.so before running!")

comm_lib = CDLL('libcomm.so')


def listenToSocket(port, mySocket):
    """
    Creates a socket and starts to listen (used by server)
    :param port:
    :param mySocket:
    :return:
    """
    sock = c_int(mySocket)
    comm_lib.listenToSocket(c_char_p(port.encode()), pointer(sock))
    return sock.value


def acceptConnection(mySocket):
    """
    Accepts new connections (used by server)
    :param mySocket:
    :return:
    """
    return comm_lib.acceptConnection(c_int(mySocket))


def connectToTarget(port, ip, mySocket):
    """
    Connects to a server (used by client)
    :param port:
    :param ip:
    :param mySocket:
    :return:
    """
    sock = c_int(mySocket)
    comm_lib.connectToTarget(c_char_p(port.encode()), c_char_p(ip.encode()), pointer(sock))
    return sock.value


def sendMsg(msg, mySocket):
    """
    Sends a network message (one char)
    :param msg:
    :param mySocket:
    :return:
    """
    return comm_lib.sendMsg(c_int(msg), c_int(mySocket))


def recvMsg(mySocket):
    """
    Receives a network message
    :param mySocket:
    :return:
    """
    return comm_lib.recvMsg(c_int(mySocket))


def sendMove(moveToSend, mySocket):
    """
    Sends a move via mySocket
    :param moveToSend:
    :param mySocket:
    :return:
    """
    return comm_lib.sendMove(pointer(moveToSend), c_int(mySocket))


def getMove(moveToGet, mySocket):
    """
    Receives a move from mySocket
    :param moveToGet:
    :param mySocket:
    :return:
    """
    return comm_lib.getMove(pointer(moveToGet), c_int(mySocket))


def sendName(textToSend, mySocket):
    """
    Used to send agent's name to server
    :param textToSend:
    :param mySocket:
    :return:
    """
    if len(textToSend) > MAX_NAME_LENGTH:
        print("Name is too big!")
        return

    return comm_lib.sendName(c_char_p(textToSend.encode()), c_int(mySocket))


def getName(mySocket):
    """
    Used to receive agent's name
    :param mySocket:
    :return:
    """
    buffer = create_string_buffer(MAX_NAME_LENGTH + 1)
    ret = comm_lib.getName(pointer(buffer), c_int(mySocket))
    return namedtuple('Ret', 'status, name')(ret, buffer.value.decode())


def sendPosition(posToSend, mySocket):
    """
    Used to send position struct
    :param posToSend:
    :param mySocket:
    :return:
    """
    return comm_lib.sendPosition(pointer(posToSend), c_int(mySocket))


def getPosition(posToGet, mySocket):
    """
    Used to receive position struct
    :param posToGet:
    :param mySocket:
    :return:
    """
    comm_lib.getPosition(pointer(posToGet), c_int(mySocket))
