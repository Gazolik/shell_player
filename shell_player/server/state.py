
#interface state
class State:
    def __init__(self, player):
        self.player = player
        self.actions = {
            'close': self.close,
            'playlists': self.get_playlists,
            'set_playlist': self.set_playlist,
            'link': self.link
        }
        self.name = 'abstract_state'
        self._out_info = ''

    def process(self, action, args = []):
        return_state = self.name
        if action not in self.actions.keys():
            print('unavailable action in this state')
        else:
            return_state = self.actions[action](args)
        return return_state

    def close(self, *args):
        self.player.stop()
        return 'exit_state'

    def output_info(self):
        info = self._out_info
        self._out_info = ''
        return info

    def set_playlist(self, *args):
        name = args[0]
        if name in self.player.playlists.keys():
            self.player.set_playlist(name)
            self.player.play()
        return 'playing_state'

    def get_playlists(self, *args):
        for pl in self.player.playlists.keys():
            self._out_info += "- {}\n".format(pl)
        return self.name

    def link(self, *args):
        return self.name


# play/pause state parent
class DynamicState(State):
    def __init__(self, player):
        State.__init__(self, player)
        self.name = 'dynamic_state'
        self.actions['stop'] = self.stop
        self.actions['info'] = self.get_info
        self.actions['next'] = self.next_track
        self.actions['prev'] = self.prev_track
        self.actions['goto'] = self.goto_track
        self.actions['vol'] = self.set_volume


    def stop(self, *args):
        self.player.stop()
        return 'stopped_state'

    def info_track(self, *args):
        self._out_info = self.player.playing.playing_track.get_info()

    def next_track(self, *args):
        self.player.play_next()
        return 'playing_state'

    def prev_track(self, *args):
        self.player.play_prev()
        return 'playing_state'

    def goto_track(self, *args):
        if args[0].isdigit():
            self.player.play_index(int(args[0]))
        return 'playing_state'

    def get_info(self, *args):
        raw_info = self.player.get_info()
        info = ""
        info += raw_info['player']
        info += raw_info['playlist']
        info += raw_info['track']
        self._out_info = info
        return self.name

    def set_volume(self, *args):
        volume = int(args[0])
        if volume <= 100 and volume >= 0:
            self.player.set_volume(volume)
        return self.name

class PlayingState(DynamicState):
    def __init__(self, player):
        DynamicState.__init__(self, player)
        self.name = 'playing_state'
        self.actions['pause'] = self.pause

    def pause(self, *args):
        self.player.pause()
        return 'paused_state'
   
    # info to display in prompt
    def get_disp(self):
        actual = self.player.line_playing_info()
        return "Playing: " + actual

class PausedState(DynamicState):
    def __init__(self, player):
        DynamicState.__init__(self, player)
        self.name = 'paused_state'
        self.actions['play'] = self.play

    def play(self, *args):
        self.player.play()
        return 'playing_state'

    # info to display in prompt
    def get_disp(self):
        actual = self.player.line_playing_info()
        return "Pause: " + actual


class StoppedState(State):
    def __init__(self, player):
        State.__init__(self, player)
        self.name = 'stopped_state'

    def get_info(self, *args):
        self._out_info = 'Stopped'
        return self.name
    
    # info to display in prompt
    def get_disp(self):
        return 'Stopped'



class ExitState:
    def __init__(self):
        self.name = 'exit_state'

    def get_info(self, *args):
        self._out_info = 'Exiting'
        return self.name

    def get_disp(self):
        return ''

    def output_info(self):
        return ''
