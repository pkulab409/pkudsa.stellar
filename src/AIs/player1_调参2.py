from AIs.XHZAI一代 import AI_made_by_xhzgenius as ai
from random import random as rd


#节点空位占的权重 = 1+rd()*5
#铺场转移比例 = 0.3+0.5*rd()
节点空位占的权重 = 1.8
铺场转移比例 = 0.75
# 这个参数还不错，是一代AI里面表现不错的了
print("节点空位占的权重, 铺场转移比例:",节点空位占的权重, 铺场转移比例)

def player_func(map_info, player_id):
    return ai(map_info, player_id, 节点空位占的权重, 铺场转移比例)