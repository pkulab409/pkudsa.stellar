import random
from random import randint as rd

from GameMap import GameMap
from MapDesign import g_design1

# 重要约定！！！
PLAYER_1 = 0
PLAYER_2 = 1


def player_func_unused1(x, y):
    return eval(input('请输入一系列操作，如[(1, 2, 40), (1, 3, 23)]\n'))


def player_func_unused2(x, y):  # for testing manually only
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

def noob_littleAI(map_info: GameMap, player_id: int):
    actions=[]
    nodes=map_info.nodes
    def judge_state(map_info:GameMap,player_id:int):
        neutral_num=0
        for node in nodes:
            if node.belong==-1:
                neutral_num+=1
        if neutral_num>2:
            expansion(map_info,player_id)
        else:
            assault(map_info,player_id)

    def defense(map_info,id):
        # make a moderate defense plan
        pass
    def desperate_defense(map_info,id,node):
        # save one node at all cost
        pass
    def expansion(map_info:GameMap,player_id:int):
        # expand the realm at the beginning of the game
        for node in nodes:
            if node.belong==player_id:
                all_clear=True
                for j in node.get_next():
                    nextnode=nodes[j]
                    if nextnode.belong==-1:
                        all_clear=False
                        ready_power=node.power[player_id]/3
                        if ready_power>20: 
                            actions.append((node.number,nextnode.number,ready_power-2))
                if all_clear:
                    j=max(node.get_next()) if player_id==0 else min(node.get_next())
                    nextnode=nodes[j]
                    actions.append((node.number,nextnode.number,node.power[player_id]-10))

                    
                        

    def skirmish(map_info,id):
        # hit and run
        pass
    def assault(map_info:GameMap,player_id:int):
        # make a general assault
        for node in nodes:
            if node.belong==player_id:
                j=max(node.get_next()) if player_id==0 else min(node.get_next())
                nextnode=nodes[j]
                if node.power[player_id]>50:
                    actions.append((node.number,nextnode.number,node.power[player_id]-10))


    def concentrate_assault(map_info,id,node):
        # attack at the same direction at all cost
        pass
    def cheat(map_info,id,cheat_node,real_node):
        # pretend to attack the cheat_node, but launch a stronger assault on the real_node
        pass     

    judge_state(map_info,player_id)   
    return actions



player_func = noob_littleAI