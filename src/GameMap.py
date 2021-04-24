from MapDesign import g_design
from Node import Node
from config import POWER_LIMIT, INIT_POWER_1, INIT_POWER_2

# 重要约定！！！
PLAYER_1 = 0
PLAYER_2 = 1


class GameMap:
    def __init__(self, design: dict):
        """GameMap class的初始化，根据地图字典，生成地图。

            nodes存储了地图的所有节点，而具体数据存储在各个node中，详细数据请参见Node class

            需要主要的是，nodes[0]为无用节点，仅作为占位使用，对于节点的计数从1开始，这是为了与node.number属性保持一致
        Args:
            design (dict): 地图文件中的字典
        """
        self.xy = design["xy"]
        design = design["design"]
        self.N = len(design) # 节点数，增加代码可读性
        self.nodes = [Node(i) for i in range(self.N+2)]
        self.nodes[1].set_power(INIT_POWER_1, True)
        self.nodes[self.N].set_power(INIT_POWER_2, True)

        for number in design.keys():
            for nextnumber in design[number].keys():
                self.nodes[number].set_connection(
                    nextnumber, float(design[number][nextnumber]))

    def __repr__(self):
        """用于打印地图信息，面向调试

        Returns:
            str: 返回地图信息的字符串
        """
        ans = []
        for i in self.nodes[1:]:
            ans.append(repr(i))
        return "\n".join(ans) + "\n"


    def __judge(self, player_actionlist: list, tmp_player_id: int):
        """此函数用于判断当回合派遣兵力是否合法
        传入参数为玩家当回合所有操作的表，如：[[1,2,5.0],[1,3,4.0],[2,3,6.0]]
        若派遣兵力总数大于该节点兵力则引发 RuntimeError

        Args:
            player_actionlist (list): 包含若干玩家操作元组的列表
            tmp_player_id (int, optional): 玩家的id {player1: 0, player2: 1}.

        Raises:
            RuntimeError: Judgement!!! Invalid input type!
            RuntimeError: Judgement!!! Invalid input length!
            RuntimeError: [description]
            RuntimeError: [description]
            RuntimeError: [description]
            RuntimeError: [description]
            RuntimeError: [description]
            RuntimeError: [description]   这一部分最后再写（
        """
        # 检查输入是否是list
        if not isinstance(player_actionlist, list):
            raise RuntimeError('Judgement!!! Invalid input type!')
        sentPower = {}  # sentPower[i]代表每个节点派出去多少兵
        for player_action in player_actionlist:
            # 检测输入action是否是元组，并且长度为3
            if not isinstance(player_action, tuple):
                raise RuntimeError("Judgement!!! Invalid input type! ")
            if len(player_action) != 3:
                raise RuntimeError("Judgement!!! Invalid input length! ")
            # 判断action的三个参数类型是否正确
            if not isinstance(player_action[0], int):
                raise RuntimeError("Judgement!!! Invalid input type! ")
            if not isinstance(player_action[1], int):
                raise RuntimeError("Judgement!!! Invalid input type! ")
            if not (isinstance(player_action[2], float) or isinstance(player_action[2], int)):
                raise RuntimeError("Judgement!!! Invalid input type! ")
            # 判断action是否越界操作
            if player_action[2] <= 0:
                raise RuntimeError("Judgement!!! Invalid input value(<=0)! ")
            if player_action[0] < 1 or player_action[0] > self.N:
                raise RuntimeError(
                    'Judgement!!! Invalid input target(out of range): %s' % str(player_action))

            # 检查move操作是否使得其余节点越界
            if player_action[0] not in sentPower:
                sentPower[player_action[0]] = player_action[2]
            else:
                sentPower[player_action[0]] += player_action[2]
        for i in sentPower:
            if sentPower[i] >= self.nodes[i].power[tmp_player_id]:
                raise RuntimeError('Judgement!!! Invalid move:no enough power: player%d'%tmp_player_id)

    def __move(self, tmp_player_id: int, player_action: tuple):
        """这是为兵力调用函数

            函数首先对于单个操作的合法性进行了判断，然后在操作地图，完成移动
        Args:
            tmp_player_id (int, optional): 玩家的id {player1: 0, player2: 1}
            player_action (tuple): 包含若干玩家操作元组

        Raises:
            RuntimeError: [description]
            RuntimeError: [description]
            RuntimeError: [description]
            RuntimeError: [description]     错误最后再写
        """
        start = player_action[0]
        end = player_action[1]
        power = player_action[2]
        # 输入是否合法
        if not (isinstance(tmp_player_id, int) and isinstance(start, int) and isinstance(end, int) and
                (isinstance(power, float) or isinstance(power, int))):
            raise RuntimeError('invalid input type: %s' % str(player_action))
        # 派出兵力点不属于该玩家
        if self.nodes[start].belong != tmp_player_id:
            raise RuntimeError(
                'invalid move: wrong basement: %s' % str(player_action))
        # power超过兵力上限
        if self.nodes[start].power[tmp_player_id] <= power:
            raise RuntimeError(
                'invalid input value(too much): %s' % str(player_action))
        # 目标兵力节点与派出点不相连
        if end not in self.nodes[start].get_next():
            raise RuntimeError(
                'invalid move: no connection: %s' % str(player_action))

        # 以下为行动主体函数
        tmp_pw = list(self.nodes[start].power)
        tmp_pw[tmp_player_id] -= power
        self.nodes[start].set_power(tuple(tmp_pw), False)

        # 以根号作为兵力损耗的单位并且家手过路费
        tmp_pw = list(self.nodes[end].power)
        power -= power ** 0.5 - self.nodes[start].get_nextCost(end)
        power = max(power, 0)  # 兵力损耗至小于零时，相当于兵力为零
        tmp_pw[tmp_player_id] += power
        self.nodes[end].set_power(tuple(tmp_pw), False)

    def __combat(self):
        """调用每个节点的combatInNode()函数，完成战斗过程，战斗细节参见Node.combatInNode()函数
        """
        for node in self.nodes:
            node.combatInNode()

    def __natality(self):
        """这是用来给地图中的每个节点生产新兵力的函数

            这里采用了Logistic增长函数的差分表达，时间单位是1回合，具体计算方法是：x = x + (power_limit - x) * x * spawn_rate (x是当前战力)

            对于开发人员，需要注意每个节点预设的增长率要根据给该节点预设的战力上限来设置，它们的乘积应小于1,也即:spawn_rate * power_limit < 1

            对于AI而言，最大收益显然是power = power_limit / 2
        """
        for n in self.nodes:
            new0 = n.power[0]
            new1 = n.power[1]  # 两个临时变量

            if new0<n.power_limit:
                new0 = n.power[0] + n.spawn_rate / n.power_limit * \
                    (n.power_limit - n.power[0]) * n.power[0]
            else:
                new0 = n.power_limit+(new0-n.power_limit)*n.despawn_rate
            if new1<n.power_limit:
                new1 = n.power[1] + n.spawn_rate / n.power_limit * \
                    (n.power_limit - n.power[1]) * n.power[1]
            else:
                new1 = n.power_limit+(new1-n.power_limit)*n.despawn_rate
            
            n.set_power((new0, new1), False)

    def update(self, player1_actions, player2_actions):
        """这是用来更新地图的函数，将作用于所有的节点，逻辑是先judge，再move，再combat，再natality

        Args:
            player1_actions (list): 包含若干player1操作元组的列表
            player2_actions (list): 包含若干player2操作元组的列表

        Returns:
            list: 用于可视化的一个列表，里面包含三个字典
        """
        try:
            self.__judge(player1_actions, 0)
        except:
            player1_actions = []
        try:
            self.__judge(player2_actions, 1)
        except:
            player2_actions = []

        for action in player1_actions:
            self.__move(0, action)
        for action in player2_actions:
            self.__move(1, action)
            
        ans = [self.export_battle_as_dic(player1_actions,player2_actions)]

        self.__combat()
        ans.append(self.export_battle_as_dic())
        self.__natality()
        ans.append(self.export_battle_as_dic())
        return ans #返回一个三元列表，里面是代表本回合可视化的三个字典

    def end_early(self):
        """判断当前局面上是否有胜者出现

        Returns:
            int: [-1: 平局, 0: player1获胜, 1:player2获胜 , None: 未结束]
        """
        if self.nodes[1].belong == 1 and self.nodes[self.N].belong == 0:
            return -1
        if self.nodes[self.N].belong == 0:
            return 0
        if self.nodes[1].belong == 1:
            return 1

        return None

    def high_score(self):
        """判断当前局面上那一方的分数更高，判断逻辑是：先判断哪一方占有节点数量多，若一样多，则判断总power高者

        Returns:
            int: [0: player1获胜, 1:player2获胜, None: 未结束, -1: 和局],
            str: [胜利方式, 节点数胜利, 兵力数胜利]
        """
        n_node1, n_node2, n_army1, n_army2 = 0, 0, 0, 0  # 分别表示两位玩家的占领节点数量，以及节点内总兵力
        for i in range(1, self.N+1):
            if self.nodes[i].belong == 0:
                n_node1 += 1
                # .power中,[0]是玩家1的兵力,[1]是玩家2的兵力
                n_army1 += self.nodes[i].power[0]
            elif self.nodes[i].belong == 1:
                n_node2 += 1
                n_army2 += self.nodes[i].power[1]
        if n_node1 > n_node2:
            return 0, "回合上限到！比拼节点数！"
        elif n_node1 < n_node2:
            return 1, "回合上限到！比拼节点数！"
        elif n_army1 > n_army2:
            return 0, "回合上限到！节点数相同，比拼总兵力！"
        elif n_army1 < n_army2:
            return 1, "回合上限到！节点数相同，比拼总兵力！"
        else:
            return -1, "回合上限到！节点数相同，总兵力也相同！和局！！"

    def export_battle_as_dic(self, action_lst_1: list = [], action_lst_2: list = []):
        """将当前map返回为字典，适用于实现可视化的调试函数

        Args:
            action_lst_1 (list): 包含若干player1操作元组的列表
            action_lst_2 (list): 包含若干player2操作元组的列表

        Returns:
            dict: 包含map每一回合战斗信息的字典，不包含地图本身的节点连接情况等等常量
        """
        return {
            # 是三元tuple
            "power": {i: self.nodes[i].power for i in range(1, self.N+1)},
            # 是0or1
            "owner": {i: self.nodes[i].belong for i in range(1, self.N+1)},
            # 存储连接的其他节点信息,示例:{1:1.2, 2:2.3}意思是这个节点可以去1号，过路费1.2,以此类推
            
            "actions": {
                1: action_lst_1,  # 三元元组的列表
                2: action_lst_2
            }
        }
    
    def export_map_as_dic(self):
        """将当前map返回为字典，适用于实现可视化的调试函数

        Returns:
            dict: 包含map地图本身的节点连接情况等等常量的字典
        """
        return {
            "edges": {i: self.nodes[i].get_next() for i in range(1, self.N+1)},
            # 是float
            "limit": {i: self.nodes[i].power_limit for i in range(1, self.N+1)},
            "xy": self.xy,  # 地图每个节点可视化的坐标
        }
