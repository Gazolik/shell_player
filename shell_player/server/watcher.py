import threading, time, signal, os

class Watcher(threading.Thread):
    def __init__(self, interface, shell_file, pids):
        threading.Thread.__init__(self)
        self.interface = interface
        self.shell_file = shell_file
        self.pids = pids
        self.running = True
        self.displayed = self.interface.disp

    def run(self):
        while self.running:
            time.sleep(1)
            self.interface.update()
            if self.displayed != self.interface.disp:
                print("Disp changed !", self.displayed)
                self.notify_changes()
        with open(self.shell_file, 'w') as f:
            print('Clearing file')
            f.write('')

    def stop(self):
        self.running = False

    def notify_changes(self):
        for pid in self.pids:
            self.displayed = self.interface.disp
            with open(self.shell_file, 'w') as f:
                f.write(self.displayed)
            print('Send signal to ', pid)
            os.kill(pid, signal.SIGUSR1)
