from random import randint as rd
from GameMap import GameMap

def player_func(map_info,player_id): #辅助函数
    ACTIONS = []
    tmp_left = [i.power[player_id] for i in map_info.nodes]

    def isValid(action):
        a, b, c = action
        if map_info.nodes[a].belong != player_id:
            return False
        if b not in map_info.nodes[a].get_next():
            return False
        if tmp_left[a] <= c + 0.01:
            return False
        tmp_left[a] -= c
        return True

    for i in range(1000):
        tmp_action = (rd(1, len(map_info.nodes) - 1), rd(1, len(map_info.nodes) - 1), rd(1, 1000) / 10)
        if isValid(tmp_action):
            ACTIONS.append(tmp_action)

    # 随机出兵
    return ACTIONS

class player_class: #格式要求
    def __init__(self, player_id:int):
        self.player_id = player_id

    def player_func(self, map_info:GameMap):
        return player_func(map_info, self.player_id)