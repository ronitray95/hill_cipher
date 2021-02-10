#!/usr/bin/env python3

import copy
import socket
from _thread import *
from encrypt import *

listenSocket: socket


def startListen():
    while True:
        c, a = listenSocket.accept()
        print('Client', a[0], ':', a[1], 'connected')
        data = (c.recv(PIECE_SIZE)).decode('utf-8')
        start_new_thread(acceptMessage, (c, a, data))
    listenSocket.close()


def acceptMessage(conn, addr, text):
    if text == 'quit':
        return
    text = text.split('\n')
    mat_data = (text[0]).split(' ')
    crc_recv = text[1]
    rows = CIPHER_ROW_LENGTH
    cols = int(len(mat_data)/CIPHER_ROW_LENGTH)
    mat = [None] * cols
    enc_matrix = [copy.deepcopy(mat)]
    for i in range(1, CIPHER_ROW_LENGTH):
        enc_matrix.append(copy.deepcopy(mat))
    x = 0
    for i in range(rows):
        for j in range(cols):
            enc_matrix[i][j] = int(mat_data[x])
            x += 1
    print('Received CRC:', crc_recv)
    print('Received encrypted matrix')
    for m in enc_matrix:
        print(*m, sep=' ', end='')
        print()

    dec_matrix = [copy.deepcopy(mat)]
    for i in range(1, CIPHER_ROW_LENGTH):
        dec_matrix.append(copy.deepcopy(mat))

    for i in range(0, rows):
        for j in range(0, cols):
            dec_matrix[i][j] = 0
            for k in range(0, CIPHER_COL_LENGTH):
                dec_matrix[i][j] += INVERSE_CIPHER[i][k] * enc_matrix[k][j]

    print('\nDecrypted matrix')
    for m in dec_matrix:
        print(*m, sep=' ', end='')
        print()
    dec_str = ''
    inpCRC = ''
    for j in range(0, cols):
        for i in range(0, rows):
            c = chr(dec_matrix[i][j]+64 if dec_matrix[i][j] <= 26 else 32)
            dec_str += c
            inpCRC += f'{dec_matrix[i][j]:05b}'

    inpCRC += crc_recv  # append received CRC to CRC of decrypted data
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

    dec_str = dec_str.strip()
    print('\nDecrypted string:', dec_str)
    if int(inpCRC) == 0:
        print('CRC matches. Data is correct')
    else:
        print('CRC does not match. Data is invalid')


def main():
    global listenSocket
    listenSocket = socket.socket()
    try:
        listenSocket.bind((LOCALHOST, SERVER_PORT))
    except Exception as e:
        print('Bind Failed. Exception occured:', str(e))
        quit()
    listenSocket.listen(4)  # max queued clients=4
    print('Listening on http://' + LOCALHOST + ':' + str(SERVER_PORT))
    start_new_thread(startListen, ())
    print('HIT ENTER TO EXIT')
    input()
    # connectServer()


if __name__ == "__main__":
    main()
