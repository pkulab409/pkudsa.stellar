import random
from random import randint as rd

from GameMap import GameMap

from AIs.AI_made_by_xhzgenius import AI_made_by_xhzgenius

# 重要约定！！！
PLAYER_1 = 0
PLAYER_2 = 1


def player_func_unused1(x, y):
    return eval(input('请输入一系列操作，如[(1, 2, 40), (1, 3, 23)]\n'))


def player_func_unused2(x, y):  # for testing manually only
    ##  very important:
#   测试时输入的样例规定:
#    1 2 30
#    1 3 40
#    qaq
#    返回:[(1,2,30.0),(1,3,40.0)]
    result = []
    print('请分行输入操作,三个数用空格隔开,示例：2 5 80 输入任何字母或非法格式以结束输入:')
    try:
        while True:
            a, b, c = map(int, input().split())
            result.append((a, b, c))
    except Exception:
        print(result)
        return result


def player_func_random1(map_info: GameMap, player_id: int):
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


# 更牛逼的随机AI（红豆泥 ？
def player_func_random2(map_info: GameMap, player_id: int):
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


player_func = player_func_random1
