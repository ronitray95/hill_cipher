# Client server architecture using Hill cipher encoding

## About

The client sends text (only alphabets and spaces) to the server after encryption using Hill Cipher. The matrix used to transform the data is in `encrypt.py`. The CRC of the data is also sent to the server which is used for the error checking.

## Execution

`./server.py`

`./client.py`

## Notes

- Lowercase alphabets, if present, are converted to uppercase before sending to server.
- Client quits after sending one message.
- fs
- Server is multithreaded.
- All constants used can be changed in `encrypt.py`.
