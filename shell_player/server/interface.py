from .player import Player
from .state import PlayingState, PausedState, StoppedState, ExitState

class Interface:
    def __init__(self, player):
        self.player = player
        self.all_states = {
            'playing_state': PlayingState(player),
            'paused_state': PausedState(player),
            'stopped_state': StoppedState(player),
            'exit_state': ExitState()
        }
        self.state = self.all_states['paused_state']
        self.disp = ''

    def process_msg(self, msg):
        return_state = self.state.process(msg[0], msg[1:])
        self.state = self.all_states[return_state]
        info = self.state.get_info()
        self.disp = self.state.get_disp()
        return not isinstance(self.state, ExitState), info

