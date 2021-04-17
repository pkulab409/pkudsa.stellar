from random import randint
from GameMap import GameMap


def player_func(map_info: GameMap, player_id: int):
    actions = []
    k = 2
    for i in range(100):
        a, b, c = randint(0, 4), randint(0, 4), randint(0, 10)
        try:
            map_info.check_action(action=(a, b, c), player_id=player_id)
        except:
            continue
        actions.append((a, b, c))
        k -= 1
        if k == 0: break
    return actions

