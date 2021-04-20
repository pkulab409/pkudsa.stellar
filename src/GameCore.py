from copy import deepcopy
from typing import Optional, Tuple, Any
import json

from GameMap import GameMap
from TimeLimit import time_limit
import config

# 重要约定！！！
PLAYER_1 = 0
PLAYER_2 = 1


class Game:
    def __init__(self, filename1: str, filename2: str, max_time: float, max_turn: int, map_args: dict):
        """初始化一局游戏，具体规则请参见文档（文档组加油！

        Args:
            filename1 (str): 玩家1的脚本
            filename2 (str): 玩家2的脚本目录
            max_time (float): 单步的最大思考时间
            max_turn (int): 允许进行的最大回合数
            map_args (dict): 包含地图配置的字典
        """
        self.__max_time = max_time
        self.__map = GameMap(map_args)
        self.__winner = None
        self.__game_end = False
        self.__max_turn = max_turn

        self.__history_map = [self.__map.update([], [])]#开局的地图也要记录

        try:

            exec("self.player_func1 = __import__('AIs.{}').".format(filename1) + filename1 + '.player_func')
        except:
            # if function is not found, the opposite wins
            self.__winner = 'player2'
            self.__game_end = True

        try:
            exec("self.player_func2 = __import__('AIs.{}').".format(filename2) + filename2 + '.player_func')
        except:
            if self.__game_end:
                # both players fail to write a correct function, no one wins
                self.__winner = None
            else:
                self.__winner = 'player1'
                self.__game_end = True

    def next_step(self):
        """这里是对局面进行一次更新，询问两方玩家获得actionList，然后调用update()
        """
        map_info1 = deepcopy(self.__map)
        map_info2 = deepcopy(self.__map)
        if False: # 测试代码，测试的时候改成False
            try:
                with time_limit(self.__max_time, "player1"):
                    player1_actions = self.player_func1(map_info1,0)
            except Exception:
                print("Player func 1 error!")
                player1_actions = []
        else:
            with time_limit(self.__max_time, "player1"):
                player1_actions = self.player_func1(map_info1,0)
            # 这里是否应该捕捉到异常之后直接判负?
        try:
            with time_limit(self.__max_time, "player2"):
                player2_actions = self.player_func2(map_info2,1)
        except Exception:
            print("Player func 2 error!")
            player2_actions = []
        if self.__game_end:
            return


        self.__history_map.append(
            self.__map.update(player1_actions, player2_actions)
        )

    def run(self):
        """这是运行接口，将返回胜利者

        Returns:
            str: 胜利者
        """
        for turn in range(self.__max_turn):
            if self.__game_end:
                break
            self.next_step()

            #print(self.__map) # 测试代码，记得删
            #print("___________________________________________________________________________")

            end_early = self.__map.end_early()
            if end_early is not None:
                self.__winner = end_early
                self.__game_end = True
                if self.__winner=="draw":
                    self.__winner = None
                break
        else:
            self.__winner = self.__map.high_score()
        return self.__winner

    def get_history(self):
        return self.__history_map
