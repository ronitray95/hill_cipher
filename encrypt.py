#!/usr/bin/env python3


PIECE_SIZE = 4096
LOCALHOST = '127.0.0.1'
SERVER_PORT = 5000
CIPHER_MATRIX = [
    [-3, -3, -4],
    [0, 1, 1],
    [4, 3, 4]
]

INVERSE_CIPHER = [
    [1, 0, 1],
    [4, 4, 3],
    [-4, -3, -3]
]

CIPHER_ROW_LENGTH = 3
CIPHER_COL_LENGTH = 3
POLY_LENGTH = 4
CRC_POLYNOMIAL = '1011'  # x^3 + x + 1
