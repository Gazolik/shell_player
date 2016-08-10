from multiprocessing.connection import Client
import sys
import os

address = ('localhost', 6000)
conn = Client(address, authkey='s'.encode(encoding='UTF-8'))

msg = {}
msg['pid'] = os.getppid()
msg['args'] = sys.argv[1:]
conn.send(msg)
