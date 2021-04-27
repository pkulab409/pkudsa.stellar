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
    def __init__(self, filename1: str, filename2: str, map_args: dict):
        """初始化一局游戏，具体规则请参见文档（文档组加油！

        Args:
            filename1 (str): 玩家1的脚本
            filename2 (str): 玩家2的脚本目录
            map_args (dict): 包含地图配置的字典
        """
        self.__max_time = config.MAX_TIME
        self.__map = GameMap(map_args)
        self.__winner = None
        self.__game_end = False
        self.__game_end_reason = "游戏未结束。"
        self.__max_turn = config.MAX_TURN
        self.__player = []
        self.__history_map = {
            "map": self.__map.export_map_as_dic(),
            "player_name": {0: filename1, 1: filename2, -1: "No player(draw)", None: "玩家函数错误" },
            "result": "游戏还没结束。",
            "history": [self.__map.update([], [])]
        }#开局的地图也要记录

        try:
            exec("""from AIs.{} import player_class as player_class1
self.addPlayer(player_class1(0))""".format(filename1))
        except:
            # if function is not found, the opposite wins
            self.__winner = 1
            self.__game_end = True

        try:
            exec("""from AIs.{} import player_class as player_class2
self.addPlayer(player_class2(1))""".format(filename2))
        except:
            if self.__game_end:
                # both players fail to write a correct function, no one wins
                self.__winner = None
            else:
                self.__winner = 0
                self.__game_end = True

    def addPlayer(self, player):
        self.__player.append(player)

    def next_step(self):
        """这里是对局面进行一次更新，询问两方玩家获得actionList，然后调用update()
        """
        map_info1 = deepcopy(self.__map)
        map_info2 = deepcopy(self.__map)
        if True: # 测试代码，测试的时候改成False
            try:
                with time_limit(self.__max_time, "player1"):
                    player1_actions = self.__player[0].player_func(map_info1)
            except Exception:
                print("Player func 1 error!")
                player1_actions = []
        else:
            with time_limit(self.__max_time, "player1"):
                player1_actions = self.__player[0].player_func(map_info1)
            # 这里是否应该捕捉到异常之后直接判负?
        try:
            with time_limit(self.__max_time, "player2"):
                player2_actions = self.__player[1].player_func(map_info1)
        except Exception:
            print("Player func 2 error!")
            player2_actions = []
        if self.__game_end:
            return

        # 历史地图字典，存入列表
        self.__history_map["history"].append(
            self.__map.update(player1_actions, player2_actions)
        )

    def run(self):
        """这是运行接口，将返回胜利者

        Returns:
            str: 胜利者, 0, 1, or -1
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
                if self.__winner==0:
                    self.__game_end_reason = (
                        "Player2(%s)的基地被打爆了！"%self.__history_map["player_name"][1]
                    )
                if self.__winner==1:
                    self.__game_end_reason = (
                        "Player1(%s)的基地被打爆了！"%self.__history_map["player_name"][0]
                    )
                if self.__winner==-1:
                    self.__game_end_reason = (
                        "双方玩家的基地同时被打爆了！"
                    )
                    self.__winner = self.__map.high_score()[0]
                    assert self.__winner in (0, 1, -1)
                break
        else:
            self.__winner, self.__game_end_reason = self.__map.high_score()
        
        # 游戏已结束
        self.__history_map["result"] = (
            self.__game_end_reason + "\n"
            + self.__history_map["player_name"][self.__winner] + "获胜！"
        )
        
        return self.__winner

    def get_history(self):
        return self.__history_map