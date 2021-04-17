class Node:

    def __init__(self, index: int, spawn_rate: float = 0.01, casualty_rate: float = 0, owner: int = 0,
                 supply_limit: float = 100):
        self.index = index  # 节点的编号
        self.spawn_rate = spawn_rate  # 节点自己生产的速率
        self.casualty_rate = casualty_rate  # 战损比，定义不明，总之与战斗有关
        self.supply_limit = supply_limit  # 允许的无惩罚兵力上限
        self.path_to = {}
        # 存储连接的其他节点信息,示例:{1:1.2,2:2.3}意思是这个节点可以去1号，过路费1.2,以此类推

        self.troop = [0, 0, 0]  # 当前的兵力数列表，分别代表:player_1,player_2
        self.owner = owner  # 归属于哪个势力

    def __repr__(self):
        ans = "-----Node info: "
        ans += "Node number(ID): " + str(self.index) + "-----\n"
        ans += "Node owner: " + str(self.owner) + "\n"
        ans += "Node power: player_1 " + str(self.troop[1]) + ", player_2 " + str(self.troop[2]) + "\n"
        ans += "Node is connected to: "
        ans += repr(self.get_next()) + "\n\n"
        return ans

    def __hash__(self):
        return hash(self.index)

    def set_connection(self, next_node_index: int, travel_cost: float):
        self.path_to[next_node_index] = travel_cost  # 添加连接的节点

    def get_next(self):  # 返回所有连接的节点编号
        lst = []
        for number in self.path_to.keys():
            lst.append(number)
        return lst

    def get_nextCost(self, next_):
        return self.path_to[next_]
