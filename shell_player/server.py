from multiprocessing.connection import Listener
import threading, time
import os
import signal



Running = False

class Server:
    def __init__(self):
        self.pids = set([])
        self.pids.add(os.getppid())
        self.address = ('localhost', 6000)
        self.listener = Listener(self.address, authkey='s'.encode(encoding='UTF-8'))
        self.shell_file = os.environ['HOME'] + '/.pyplayer'
        self.player = Player()
        self.interface = Interface(self.player)

    def run(self):
        global Running
        Running = True
        cont = True
        watcher = Watcher(self.interface, self.shell_file, self.pids)
        watcher.start()
        while cont:
            conn = self.listener.accept()
            print('Connection from', self.listener.last_accepted)
            msg = conn.recv()
            print(msg)
            self.pids.add(msg['pid'])
            cont = self.interface.process_msg(msg['args'])
        conn.close()
        Running = False
        watcher.join()



class Watcher(threading.Thread):
    def __init__(self, interface, shell_file, pids):
        threading.Thread.__init__(self)
        self.interface = interface
        self.shell_file = shell_file
        self.pids = pids

    def run(self):
        global Running
        displayed = self.interface.disp
        while Running:
            time.sleep(1)
            if displayed != self.interface.disp:
                displayed = self.interface.disp
                print("Disp changed !", displayed)
                with open(self.shell_file, 'w') as f:
                    f.write(displayed)
                for pid in self.pids:
                    print('Send signal to ', pid)
                    os.kill(pid, signal.SIGUSR1)
        with open(self.shell_file, 'w') as f:
            print('Clearing file')
            f.write('')



class Interface:
    def __init__(self, player):
        self.player = player
        self.actions = {
            'play': self.play,
            'pause': self.pause,
            'stop': self.stop,
            'close': self.close}
        self.disp = ''

    def process_msg(self, msg):
        if msg[0] not in self.actions.keys():
            return False
        return self.actions[msg[0]](msg[1:])

    def play(self, *args):
        self.player.play()
        self.modify_disp('Playing')
        return True

    def pause(self, *args):
        self.player.pause()
        self.modify_disp('Paused')
        return True

    def stop(self, *args):
        self.player.stop()
        self.modify_disp('Stopped')
        return True

    def close(self, *args):
        print(args)
        self.player.stop()
        self.modify_disp('')
        print('close')
        return False

    def modify_disp(self, txt):
        print('modify_disp:', txt)
        self.disp = txt
        

class Player:
    def __init__(self):
        self.vlc = None


    def play(self):
        print('playing')

    def stop(self):
        print('stop')

    def pause(self):
        print('pause')


serv = Server()
serv.run()
