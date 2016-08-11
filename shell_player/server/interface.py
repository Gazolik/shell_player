from .player import Player

class Interface:
    def __init__(self, player):
        self.player = player
        self.actions = {
            'play': self.play,
            'pause': self.pause,
            'stop': self.stop,
            'info' : self.info_track,
            'next' : self.next_track,
            'prev' : self.prev_track,
            'goto' : self.goto_track,
            'close': self.close}
        self.disp = ''

    def process_msg(self, msg):
        if msg[0] not in self.actions.keys():
            info = "Action {} not available".format(msg[0])
            return True, info
        return self.actions[msg[0]](msg[1:])

    def play(self, *args):
        track = self.player.play()
        self.modify_disp('Playing')
        info = "Actually playing {}".format(track)
        return True, info

    def pause(self, *args):
        self.player.pause()
        self.modify_disp('Paused')
        info = "Player paused"
        return True, info

    def stop(self, *args):
        self.player.stop()
        self.modify_disp('Stopped')
        info = "Player stopped"
        return True, info

    def info_track(self, *args):
        info = self.player.playing.info()
        return True, info

    def next_track(self, *args):
        track = self.player.play_rel(1)
        self.modify_disp('Playing')
        info = "Actually playing {}".format(track)
        return True, info

    def prev_track(self, *args):
        track = self.player.play_rel(-1)
        self.modify_disp('Playing')
        info = "Actually playing {}".format(track)
        return True, info

    def goto_track(self, *args):
        if args[0].isdigit():
            track = self.player.play_abs(int(args[0]))
        else :
            track = self.player.play_rel(int(args[0]))
        self.modify_disp('Playing')
        info = "Actually playing {}".format(track)
        return True, info


    def close(self, *args):
        print(args)
        self.player.stop()
        self.modify_disp('')
        info = "Exiting player, good bye !"
        return False, info

    def modify_disp(self, txt):
        print('modify_disp:', txt)
        self.disp = txt
