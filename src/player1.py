from random import randint as rd
from GameMap import GameMap


def player_func(map_info: GameMap, player_id: int):
    ACTIONS = []
    tmp_left = [i.troop[player_id] for i in map_info.nodes()]

    def isValid(action):
        a, b, c = action
        if map_info.nodes[a].belong != player_id:
            return False
        if b not in map_info.nodes[a].get_next():
            return False
        if tmp_left[a] <= c:
            return False
        tmp_left[a] -= c
        return True

    for i in range(1000):
        tmp_action = (rd(1, 4), rd(1, 4), rd(1, 100))
        if isValid(tmp_action):
            ACTIONS.append(tmp_action)

    print("my action:", ACTIONS)
    return ACTIONS
