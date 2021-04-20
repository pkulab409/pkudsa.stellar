from GameMap import GameMap
from config import POWER_LIMIT

def AI_made_by_xhzgenius(map_info: GameMap, player_id: int):
    ACTIONS = []
    # Bellman-Ford求最短路径长度
    d = [[999999999 for j in range(1,map_info.N+11)] for i in range(1,map_info.N+11)]
    for i in range(1,map_info.N+1):
        for j in range(1,map_info.N+1):
            if i==j:
                d[i][j] = 0
            elif j in map_info.nodes[i].get_next():
                d[i][j] = 1
    for i in range(1,map_info.N+1):
        for j in range(1,map_info.N+1):
            for k in range(1,map_info.N+1):
                d[i][j] = min(d[i][j],d[i][k]+d[k][j])
    # 现在，d就是最短路径长度数组


    # 判断整个局势
    ENEMY_BASE = map_info.N if player_id==0 else 1
    my_nodes = []
    enemy_nodes = [] # List of Nodes
    danger = {}
    need_help = {} # Dict of bools
    niubility = {} # Dict of ints
    for i in map_info.nodes:
        danger[i.number] = 0
        if i.belong==player_id:
            my_nodes.append(i)
            need_help[i.number] = False
            niubility[i.number] = i.power[player_id]
        for j in i.get_next():
            danger[i.number] += map_info.nodes[j].power[1-player_id]
            pass
        if i.belong==1-player_id:
            enemy_nodes.append(i)
        
    danger_lst = sorted(danger, key = lambda x: -danger[x] )
    niubility_lst = sorted(niubility, key = lambda x: -niubility[x] )
    # 所有节点，按照危险程度和牛逼程度排序

    #print("Danger:", danger)
    #print("NB", niubility)

    def decay(a: int, x: int, y: int):
        return a-a**0.5-map_info.nodes[x].get_nextCost(y)

    def Judge_node(x: int):
        if danger[x]>niubility[x]:
            need_help[x] = True
            return (x, "defend", danger[x]-niubility[x])
        if niubility[x]<=10:
            return (x, "wait")
        y = min(map_info.nodes[x].get_next(), 
            key = choose_target
        )
        #print(x,y)
        #print(decay(niubility[x]-10,x,y))
        if decay(niubility[x]/2,x,y) > map_info.nodes[y].power[1-player_id]:
            return (x, "expand", niubility[x]/2, y)
        return (x, "wait")

    def choose_target(y: int):
        nodey = map_info.nodes[y]
        if nodey.belong==player_id:
            if need_help[y]:
                return -999999999
            else:
                return (
                    999999999+
                    d[y][ENEMY_BASE]-
                    (POWER_LIMIT-nodey.power[player_id])*0.02
                )
        return nodey.power[1-player_id]+d[y][ENEMY_BASE]


    # 开始行动
    for x in my_nodes:
        x_action = Judge_node(x.number)
        #print(x.number, x_action)
        if x_action[1]=="wait":
            continue
        elif x_action[1]=="defend":
            pass
        elif x_action[1]=="expand":
            ACTIONS.append((x_action[0], x_action[3], x_action[2]))

    #print(ACTIONS)
    return ACTIONS
