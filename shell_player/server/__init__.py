import os
from multiprocessing.connection import Listener


from .watcher import Watcher
from .interface import Interface
from .player import Player
from . import vlc

class Server:
    def __init__(self, in_file):
        self.pids = set([])
        self.pids.add(os.getppid())
        self.address = ('localhost', 6000)
        self.listener = Listener(self.address, authkey='s'.encode(encoding='UTF-8'))
        self.shell_file = os.environ['HOME'] + '/.pyplayer'
        self.player = Player(in_file)
        self.interface = Interface(self.player)

    def run(self):
        cont = True
        watcher = Watcher(self.interface, self.shell_file, self.pids)
        watcher.start()
        while cont:
            conn = self.listener.accept()
            print('Connection from', self.listener.last_accepted)
            msg = conn.recv()
            print(msg)
            self.pids.add(msg['pid'])
            cont, info = self.interface.process_msg(msg['args'])
            watcher.notify_changes()
            conn.send(info)
        conn.close()
        watcher.stop()
        watcher.join()
