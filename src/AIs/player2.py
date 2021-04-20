from random import randint as rd

from GameMap import GameMap

from AIs.player_cmy01 import noob_littleAI

# 重要约定！！！
PLAYER_1 = 0
PLAYER_2 = 1

player_func = noob_littleAI

def player_func_un(map_info: GameMap, player_id: int):
    ACTIONS = []
    tmp_left = [i.power[player_id] for i in map_info.nodes]

    # print("I am TESTING!!!",map_info)#测试
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
    # print(ACTIONS)
    return ACTIONS
