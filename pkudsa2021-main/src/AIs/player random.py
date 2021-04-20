import random

from GameMap import GameMap


def player_func(map_info: GameMap, player_id: int):
    actions = []
    for i in range(1, 5):
        if map_info.nodes[i].power[player_id] > 0:
            can = map_info.nodes[i].get_next()
            chosen = []
            for n in range(random.randint(1, len(can))):
                chosen.append(random.choice(can))
            p = []
            for x in range(len(chosen)):
                p.append(random.random() * map_info.nodes[i].power[player_id] / len(chosen))
            for y in range(len(chosen)):
                actions.append((i, chosen[y], p[y]))
    print(actions)
    return actions
