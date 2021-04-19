class Node:
    def __init__(self, number, spawn_rate=0.01, belong=-1, power_limit=100):
        """生成一个游戏节点，初始化并存储相关信息。

        number: 节点的编号，从1开始\n
        belong: 归属于哪个势力 {-1: 中立, 0:player1 , 1:player2}\n
        power: 当前的兵力数列表 [player1, player2]\n
        spawn_rate: 节点产兵的速率, 产兵规则参见GameMap().__natality()\n
        power_limit: 允许的单个节点无惩罚兵力上限\n
        nextinfo: 存储与其他节点的联系 {节点编号: 过路费...}\n

        Args:
            number (int): 节点的编号\n
            spawn_rate (float, optional): 节点产兵的速率. Defaults to 0.01.\n
            belong (int, optional): 节点归属的势力. Defaults to -1.\n
            power_limit (int, optional): 允许的单个节点无惩罚兵力上限. Defaults to 100.
        """
        self.__number = number
        self.__power = [0, 0]
        self.__belong = belong
        self.__spawn_rate = spawn_rate
        self.__power_limit = power_limit
        self.__nextinfo = {}

    def __repr__(self):
        """用来打印节点的信息

        Returns:
            str: 返回打印出的信息
        """
        ans = "-----Node info: "
        ans += "Node number(ID): " + str(self.number) + "-----\n"
        ans += "Node owner: " + str(self.belong) + "\n"
        ans += "Node power: player1 " + \
            str(self.power[0]) + ", player2 " + str(self.power[1]) + "\n"
        ans += "Node is connected to: "
        ans += repr(self.get_next()) + "\n"
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
    def belong(self):  # int, -1, 0, or 1
        return self.__belong

    def change_owner(self, owner: int):
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

    def combatInNode(self):
        if self.power[0] < self.power[1]:
            self.set_power([0, (self.power[1] ** 2 - self.power[0] ** 2) ** 0.5])
            self.change_owner(1)
        elif self.power[0] > self.power[1]:
            self.set_power([(self.power[0] ** 2 - self.power[1] ** 2) ** 0.5, 0])
            self.change_owner(0)
        else:
            self.set_power([0, 0])
            self.change_owner(-1)
