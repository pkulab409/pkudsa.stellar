from config import SPAWN_RATE,POWER_LIMIT,DESPAWN_RATE

class Node:
    def __init__(self, number, spawn_rate=SPAWN_RATE, belong=-1, power_limit=POWER_LIMIT, despawn_rate = DESPAWN_RATE):
        """生成一个游戏节点，初始化并存储相关信息。

        number: 节点的编号，从1开始\n
        belong: 归属于哪个势力 {-1: 中立, 0:player1 , 1:player2}\n
        power: 当前的兵力数列表 [player1, player2]\n
        spawn_rate: 节点产兵的速率, 产兵规则参见GameMap().__natality()\n
        power_limit: 允许的单个节点无惩罚兵力上限\n
        nextinfo: 存储与其他节点的联系 [节点编号]\n

        Args:
            number (int): 节点的编号\n
            spawn_rate (float, optional): 节点产兵的速率. Defaults to 0.01.\n
            belong (int, optional): 节点归属的势力. Defaults to -1.\n
            power_limit (int, optional): 允许的单个节点无惩罚兵力上限. Defaults to 100.
        """
        self.__number = number
        self.__power = (0, 0) # 重要！！！power现在起是元组类型！！！
        self.__belong = belong
        self.__spawn_rate = spawn_rate
        self.__despawn_rate = despawn_rate
        self.__power_limit = power_limit
        self.__nextinfo = []

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

    @property
    def power(self):
        return self.__power

    @property
    def belong(self):
        return self.__belong

    @property
    def spawn_rate(self):
        return self.__spawn_rate
    
    @property
    def despawn_rate(self):
        return self.__despawn_rate

    @property
    def power_limit(self):
        return self.__power_limit

    def set_connection(self, nodeNumber):
        """设置与当前节点连接的节点，和行进到连接节点的过路费

        Args:
            node_number (int): 连接的节点\n
        Raises:
            RuntimeError: nodeNumber must be int\n
        """
        if not isinstance(nodeNumber, int):
            raise RuntimeError('node_number must be int')
        self.__nextinfo.append(nodeNumber)

    def get_next(self):
        """用于获取当前节点可以通向的节点编号

        Returns:
            list: 当前节点可以通向的节点编号的列表
        """
        lst = []
        for number in self.__nextinfo:
            lst.append(number)
        return lst

    
    def set_power(self, p:tuple, needJudge:bool):
        """用于设置当前节点的战力情况

        Args:
            p (list): 包含双方战力的列表
            needJudge (bool): 是否需要判断更改belong. Defaults to True

        Raises:
            RuntimeError: invalid input type list
            RuntimeError: power must be float tuple.
        """
        if not isinstance(p, tuple):
            raise RuntimeError('invalid input type tuple')
        # if list(map(type, p)) != [float, float]:
        #     raise RuntimeError('power must be float')
        self.__power = p
        if needJudge:
            if self.power[0] < self.power[1]:
                self.__belong = 1
            elif self.power[0] > self.power[1]:
                self.__belong = 0
            else:
                self.__belong = -1

    def combatInNode(self):
        """当前节点内部进行战斗

            战斗规则：

            战斗将在一回合内完成并决出胜者，胜者会又有当前节点的归属，胜者一方的战力会使用兰开斯特平方律calculatePower()计算，也就是(winnerPower ** 2 - loserPower ** 2) ** 0.5，失败一方的战力会清零
        """
        def calculatePower(winnerPower, loserPower):
            return (winnerPower ** 2 - loserPower ** 2) ** 0.5
        if self.power[0] < self.power[1]:
            self.set_power((0.0, calculatePower(self.power[1], self.power[0])), True)
        elif self.power[0] > self.power[1]:
            self.set_power((calculatePower(self.power[0], self.power[1]), 0.0), True)
        else:
            self.set_power((0.0, 0.0), True)
