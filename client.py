#!/usr/bin/env python3

import socket
from _thread import *
import re
import copy
from encrypt import *

serverSocket: socket


def enterCommand():
    inpCRC = ''
    cmd = input()
    cmd = cmd.upper()
    cmd = cmd.strip()
    rx = re.compile('^[A-Za-z ]+$')
    lst = rx.findall(cmd)
    if len(lst) == 0 or len(lst[0]) != len(cmd):
        print('Invalid input. Must contain only letters and spaces')
        serverSocket.send(str.encode('quit'))
        return
    l = len(cmd)
    cols = int(
        l/CIPHER_COL_LENGTH) if l % CIPHER_COL_LENGTH == 0 else int(l/CIPHER_COL_LENGTH)+1
    mat = [None] * cols
    matrix = [copy.deepcopy(mat)]
    for i in range(1, CIPHER_ROW_LENGTH):
        matrix.append(copy.deepcopy(mat))
    rows = len(matrix)
    x = 0
    for j in range(0, cols):
        for i in range(0, rows):
            if x >= l or cmd[x] == ' ':
                matrix[i][j] = 27
            else:
                matrix[i][j] = ord(cmd[x]) - 64
            inpCRC += f'{matrix[i][j]:05b}'
            x += 1

    # append POLY_LENGTH-1 extra zeroes for extra POLY_LENGTH degree CRC function
    inpCRC += ('0' * (POLY_LENGTH-1))
    while len(inpCRC) >= POLY_LENGTH:
        if inpCRC[0] == '0':
            inpCRC = inpCRC[1:]
            continue
        d = inpCRC[0:POLY_LENGTH]
        newll = []
        for j in range(POLY_LENGTH):
            newll.append('0' if d[j] == CRC_POLYNOMIAL[j] else '1')
        crc = (''.join(newll))
        inpCRC = crc+inpCRC[POLY_LENGTH:]
    print('CRC is', inpCRC)
    # inpCRC contains the final CRC value

    enc_matrix = [copy.deepcopy(mat)]  # PENGUINS ARE ONE TO ONE
    for i in range(1, CIPHER_ROW_LENGTH):
        enc_matrix.append(copy.deepcopy(mat))

    for i in range(0, rows):
        for j in range(0, cols):
            enc_matrix[i][j] = 0
            for k in range(0, CIPHER_COL_LENGTH):
                enc_matrix[i][j] += CIPHER_MATRIX[i][k] * matrix[k][j]
    # print(enc_matrix)
    enc_msg = ''
    for i in range(0, rows):
        for j in range(0, cols):
            enc_msg += str(enc_matrix[i][j]) + ' '
    enc_msg = enc_msg.strip()
    serverSocket.send(str.encode(enc_msg+'\n'+inpCRC))
    # print(enc_msg)


def main():
    global serverSocket
    serverSocket = socket.socket()
    try:
        serverSocket.connect((LOCALHOST, SERVER_PORT))
    except Exception as e:
        print('Exception occured:', str(e))
        quit()
    print(f'Connected to server on {LOCALHOST}:{SERVER_PORT}')
    enterCommand()


if __name__ == "__main__":
    main()
