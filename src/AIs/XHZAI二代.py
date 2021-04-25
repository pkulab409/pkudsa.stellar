from GameMap import GameMap
#from config import POWER_LIMIT
POWER_LIMIT = 100

def AI_made_by_xhzgenius(map_info: GameMap, player_id: int, 
节点空位占的权重: float = 1.8, 铺场转移比例: float = 0.8, 开始铺场的最小兵力: int = 20):
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
        
    #danger_lst = sorted(danger, key = lambda x: -danger[x] )
    #niubility_lst = sorted(niubility, key = lambda x: -niubility[x] )
    # 所有节点，按照危险程度和牛逼程度排序
    def choose_target(y: int):
        nodey = map_info.nodes[y]
        if nodey.belong==player_id:
            if need_help[y]:
                return -999999999
            else:
                return (
                    999999999+
                    d[y][ENEMY_BASE]-
                    (POWER_LIMIT-nodey.power[player_id])*0.02*节点空位占的权重
                )
        return nodey.power[1-player_id]+d[y][ENEMY_BASE]

    priority = [choose_target(i) for i in range(1, map_info.N+1)] # 每个节点的估值，数值越小越优先
    #print("Danger:", danger)
    #print("NB", niubility)

    def decay(a: int, x: int, y: int):
        return a-a**0.5-map_info.nodes[x].get_nextCost(y)

    def Judge_node(x: int):
        if danger[x]>niubility[x]:
            need_help[x] = True
            return (x, "defend", danger[x]-niubility[x])
        if niubility[x]<=开始铺场的最小兵力:
            return (x, "wait")
        y_lst = sorted(map_info.nodes[x].get_next(), 
            key = lambda x:priority[x]
        )
        y_lst_chosen = list(filter(lambda x: priority[x]<999900000, y_lst))###
        #print(x,y)
        #print(decay(niubility[x]-10,x,y))
        target_lst = []
        if len(y_lst_chosen)==0:
            target_lst.append(y_lst[0])
        else:
            for y in y_lst_chosen:
                if decay(niubility[x]*铺场转移比例/len(y_lst_chosen),x,y) > map_info.nodes[y].power[1-player_id]:
                    target_lst.append(y)
        return (x, "expand", niubility[x]*铺场转移比例/max(len(y_lst_chosen),1), target_lst)



    # 开始行动
    for x in my_nodes:
        x_action = Judge_node(x.number)
        #print(x.number, x_action)
        if x_action[1]=="wait":
            continue
        elif x_action[1]=="defend":
            pass
        elif x_action[1]=="expand":
            for y in x_action[3]:
                ACTIONS.append((x_action[0], y, x_action[2]))

    #print(ACTIONS)
    return ACTIONS

def player_func(map_info, player_id):
    return AI_made_by_xhzgenius(map_info, player_id)