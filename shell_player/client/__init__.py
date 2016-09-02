#!/usr/bin/python3

import multiprocessing.connection as connection
import sys
import os

class Client:
    def message(args):
        address = ('localhost', 6000)
        conn = connection.Client(address, authkey='s'.encode(encoding='UTF-8'))
        msg = {}
        msg['pid'] = os.getppid()
        msg['args'] = sys.argv[1:]
        conn.send(msg)
        resp = conn.recv()
        print(resp)
        conn.close()
