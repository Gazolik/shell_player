#!/usr/bin/python3

import sys

if sys.argv[1] == 'start':
    from shell_player.server import Server
    serv = Server(sys.argv[2])
    serv.run()
else:
    from shell_player.client import Client
    Client.message(sys.argv[1:])

