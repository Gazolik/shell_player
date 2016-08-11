
#interface state
class State:
    def __init__(self, player):
        self.player = player
        self.actions = {
            'close': self.close
        }
        self.name = 'abstract_state'


    def process(self, action, *args):
        return_state = self.name
        if action not in self.actions.keys():
            print('unavailable action in this state')
        else:
            return_state = self.actions[action](args)
        return return_state

    def close(self, *args):
        print(args)
        self.player.stop()
        return 'exit_state'

# play/pause state parent
class DynamicState(State):
    def __init__(self, player):
        State.__init__(self, player)
        self.name = 'dynamic_state'
        self.actions['stop'] = self.stop
        self.actions['info'] = self.info_track
        self.actions['next'] = self.next_track
        self.actions['prev'] = self.prev_track
        self.actions['goto'] = self.goto_track


    def stop(self, *args):
        self.player.stop()
        return 'stopped_state'

    def info_track(self, *args):
        info = self.player.playing.get_info()
        return self.name

    def next_track(self, *args):
        self.player.play_rel(1)
        return 'playing_state'

    def prev_track(self, *args):
        self.player.play_rel(-1)
        return 'playing_state'

    def goto_track(self, *args):
        if args[0].isdigit():
            self.player.play_abs(int(args[0]))
        else :
            self.player.play_rel(int(args[0]))
        return 'playing_state'

class PlayingState(DynamicState):
    def __init__(self, player):
        DynamicState.__init__(self, player)
        self.name = 'playing_state'
        self.actions['pause'] = self.pause

    def pause(self, *args):
        self.player.pause()
        return 'paused_state'

    # info to return
    def get_info(self):
        return "Actually playing {}"#.format(player.playing.title)

    # info to display in prompt
    def get_disp(self):
        return "Play: MUSICTITLE"

class PausedState(DynamicState):
    def __init__(self, player):
        DynamicState.__init__(self, player)
        self.name = 'paused_state'
        self.actions['play'] = self.play

    def play(self, *args):
        self.player.play()
        return 'playing_state'

    def get_info(self):
        return "Paused  {}"#.format(player.playing.title)
    
    # info to display in prompt
    def get_disp(self):
        return "Pause: MUSICTITLE"


class StoppedState(State):
    def __init__(self, player):
        State.__init__(self, player)
        self.name = 'stopped_state'

    def get_info(self):
        return "Stopped !"
    
    # info to display in prompt
    def get_disp(self):
        return "Stopped"


class ExitState:
    def __init__(self):
        self.name = 'exit_state'

    def get_info(self):
        return 'Exiting'

    def get_disp(self):
        return ''
