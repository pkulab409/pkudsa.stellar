class Node:
    def __init__(self, number, spawn_rate=0.01, casualty_rate=0, belong=-1, power_limit=100):
        self.__number = number  # 节点的编号
        self.__spawn_rate = spawn_rate  # 节点自己生产的速率
        self.__casualty_rate = casualty_rate  # 战损比，定义不明，总之与战斗有关
        self.__power_limit = power_limit  # 允许的无惩罚兵力上限
        self.__nextinfo = {}
        # 存储连接的其他节点信息,示例:{1:1.2,2:2.3}意思是这个节点可以去1号，过路费1.2,以此类推

        self.__power = [0, 0]  # 当前的兵力数列表，分别代表:player_1,player_2
        self.__belong = belong  # 归属于哪个势力

    def __repr__(self):
        ans = "-----Node info: "
        ans += "Node number(ID): "+str(self.number)+"-----\n"
        ans += "Node owner: "+str(self.belong)+"\n"
        ans += "Node power: player_1 "+str(self.power[0])+", player_2 "+str(self.power[1])+"\n"
        ans += "Node is connected to: "
        ans += repr(self.get_next())+"\n"
        return ans




    @property
    def number(self):
        return self.__number

    def set_connection(self, node_number, travel_cost):
        self.__nextinfo[node_number] = travel_cost  # 添加连接的节点

    def get_next(self):  # 返回所有连接的节点编号
        lst = []
        for number in self.__nextinfo.keys():
            lst.append(number)
        return lst

    def get_nextCost(self, next_):
        return self.__nextinfo[next_]

    @property
    def belong(self): # int, -1, 0, or 1
        return self.__belong

    def change_owner(self, owner:int):
        self.__belong = owner

    @property
    def spawn_rate(self):
        return self.__spawn_rate

    @property
    def casualty_rate(self):
        return self.__casualty_rate

    @property
    def power_limit(self):
        return self.__power_limit

    @property
    def power(self):
        return self.__power

    def set_power(self, p):
        # 这里需要写判断p输入是否合法的语句，暂时空着
        self.__power = p
