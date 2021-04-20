import random
from random import randint as rd

from GameMap import GameMap
from MapDesign import g_design1

# 重要约定！！！
PLAYER_1 = 0
PLAYER_2 = 1

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
                    actions.append((node.number,nextnode.number,node.power[player_id]*3/4))

                    
                        

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