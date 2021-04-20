from debugModule.SeleniumClass import SeleniumClass
from GameCore import Game
from MapDesign import g_design

import json
import os

MAX_TURN = 100 #调试期间允许的最大轮数
MAX_TIME = 999 #调试期间允许的最大单步时间，改时间在mode == 1 or 2 时不生效

class Gamedebug(Game):
    def __init__(self, filename1, filename2, max_time, max_turn, map_args):
        super().__init__(filename1, filename2, max_time, max_turn, map_args)
        history = self.get_history()
        filename = os.path.join(os.path.dirname(__file__), 'debugModule', 'debug.json')
        with open(filename, 'w') as f:
            f.write('')
            json.dump(history, f)
        self.web = SeleniumClass()
        self.web.openJson('debug.json')
        self.

    def historyDebug(self):
        history = self.get_history()
        if len(history) > 2:
            history = history[len(history) - 2:]
        return history

    def run(self):
        for turn in range(MAX_TURN):
            os.system('cls')
            print('=' * 30 + 'debug' + '=' * 30)
            self.next_step()

            history = self.get_history()
            self.web.openJson(history)

            pass

            if self.game_end:
                break
            end_early
            

g = Gamedebug('player1', 'player2', MAX_TIME, MAX_TURN, g_design['design'])