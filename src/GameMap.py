from Node import Node


class GameMap:
    def __init__(self, design):  # 由于地图是固定的，因此init不需要参数。
        self.__nodes = [Node(i) for i in range(len(design) + 1)]
        self.nodes[1].change_owner(0)
        self.nodes[1].power = [100, 0]
        self.nodes[len(design)].change_owner(1)
        self.nodes[len(design)].power = [0, 100]

        for number in design.keys():
            for nextnumber in design[number].keys():
                self.__nodes[number].set_connection(nextnumber, design[number][nextnumber])
        # initialize according to the map design

    def __repr__(self):  # 方便测试时打印地图
        ans = []
        for i in self.nodes[1::]:
            ans.append(repr(i))
        return "\n".join(ans)

    @property
    def nodes(self):
        return self.__nodes

    def __judge(self, player_actionlist: list, tmp_player_id: int = 0):
        """
        此函数用于判断当回合派遣兵力是否合法
        传入参数为玩家当回合所有操作的表，如：[[1,2,5.0],[1,3,4.0],[2,3,6.0]]
        若派遣兵力总数大于该节点兵力则引发 RuntimeError
        """
        dic = {}  # dic[i]代表每个节点派出去多少兵
        for player_action in player_actionlist:
            if player_action[0] not in dic:
                dic[player_action[0]] = player_action[2]
            else:
                dic[player_action[0]] += player_action[2]
        # print(dic)
        for i in dic:
            if dic[i] >= self.__nodes[i].power[tmp_player_id]:
                raise RuntimeError('Judgement!!! Invalid move:no enough power')

    def __move(self, player: int, player_action: tuple):
        """此函数为兵力调用函数，输入参数为玩家（player_1 或 player_2)和玩家操作（list)
            进行兵力调用时，该函数对每个玩家各执行一次即
            move('player_1',player_action1)
            move('player_2',player_action2)
            此函数并不涉及战斗部分，仅作用于兵力调用过程
            此函数将直接将地图进行更新
            需要调用地图复制函数copy()记录上局状态[summary]

        Args:
            player ([type]): [description]
            player_action ([type]): [description]
        """
        tmp_player_id = player
        # 临时变量，把传入的player字符串变成玩家编号
        copyMapNodes = self.nodes
        start = player_action[0]
        end = player_action[1]
        power = player_action[2]
        if not (isinstance(player, int) and isinstance(start, int) and isinstance(end, int) and (
                isinstance(power, float) or isinstance(power, int))):  # 输入是否合法
            raise RuntimeError('invalid input: %s' % str(player_action))
        if copyMapNodes[start].belong != tmp_player_id:  # 派出兵力点不属于该玩家
            raise RuntimeError('invalid move: wrong basement: %s' % str(player_action))
        if end not in copyMapNodes[start].get_next():  # 目标兵力节点与派出点不相连
            raise RuntimeError('invalid move: no connection: %s' % str(player_action))
        if power >= copyMapNodes[start].power[tmp_player_id]:  # 派出兵力大于等于存在兵力
            raise RuntimeError('invalid move: no enough power: %s' % str(player_action)
                               + str(self)  # 测试
                               )

        # 以下为行动主体函数
        temp = copyMapNodes[start].power
        temp[tmp_player_id] -= power
        self.__nodes[start].power = temp
        # 以根号作为兵力损耗的单位并且家手过路费
        power -= (power ** 0.5 + copyMapNodes[start].get_nextCost(end))
        power = 0.0 if power < 0 else power  # 兵力损耗至小于零时，相当于兵力为零
        temp = copyMapNodes[end].power
        temp[tmp_player_id] += power
        self.__nodes[start].power = temp

    def __combat(self):
        """第一部分为战斗过程，第二部分为战斗结算和归属变更
        """

        def combat_inner(nd):

            de = min(nd.power)
            nd.power = [(nd.power[0] ** 2 - de ** 2) ** 0.5, (nd.power[1] ** 2 - de ** 2) ** 0.5]

            # result of combat
            p1 = nd.power[0]
            p2 = nd.power[1]
            if p1 == 0 and p2 == 0:
                nd.change_owner(-1)  # 中立：-1
            elif p1 == 0 and nd.belong == 0:
                nd.change_owner(1)
            elif p2 == 0 and nd.belong == 1:
                nd.change_owner(0)

        for node in self.__nodes:
            combat_inner(node)

    def __natality(self):
        """遍历每个节点将节点双方战力更改为增长或衰减后的战力

            ！！非常重要！！为了使该函数按预期工作，在初始化地图时，给每个节点预设的
            增长率要根据给该节点预设的战力上限来设置，它们的乘积应小于1
            也即，spawn_rate * power_limit < 1
            若增长率设得过大，将会产生严重后果！

            self为一个GampMap。

            以player_1为例，设计逻辑是，
            n.power[0]（新）- n.power[0]（旧）
            = 每回合power增长量
            = 节点增长率 * (上限 - n.power[0]（旧）)

            对于一个节点来说，节点增长率spawn_rate是恒定的，
            而 n.power[0]（旧）越接近上限，(上限 - n.power[0]（旧）) 就会越小，
            每回合增长量就会越小。

            当n.power[0]（旧）等于上限时，(上限 - n.power[0]（旧）) 等于0，
            不增长。

            当n.power[0]（旧）大于上限时，(上限 - n.power[0]（旧）) 为负数，
            每回合增长量小于0，出现衰减。

            ！！攻城方在战力小于上限时不会增长，但在战力大于上限时仍会衰减。

            提示：每回合增长量是n.power[0]（旧）的二次函数，
            当n.power[0]（旧）等于上限一半时，该二次函数取最大值，
            所以，如果要维持一个节点的最大产出，该节点的战力应该保持在该节点战力上限的1/2，
            超过的战力可以及时派出去。
        """
        for n in self.nodes:
            if n.belong == 0:
                n.power[0] = n.power[0] + n.spawn_rate * \
                             (n.power_limit - n.power[0]) * n.power[0]
                if n.power[1] > n.power_limit:
                    n.power[1] = n.power[1] + n.spawn_rate * \
                                 (n.power_limit - n.power[1]) * n.power[1]
            if n.belong == 1:
                n.power[1] = n.power[1] + n.spawn_rate * \
                             (n.power_limit - n.power[1]) * n.power[1]
                if n.power[0] > n.power_limit:
                    n.power[0] = n.power[0] + n.spawn_rate * \
                                 (n.power_limit - n.power[0]) * n.power[0]

    def update(self, player1_actions, player2_actions):
        """[summary]

        Args:
            player1_actions ([type]): [description]
            player2_actions ([type]): [description]
        """

        self.__judge(player1_actions)
        self.__judge(player2_actions)

        for action in player1_actions:
            self.__move(0, action)
        for action in player2_actions:
            self.__move(1, action)

        self.__combat()
        self.__natality()

    def end_early(self):
        """
        :return: 1, 2 if one player wins by occupying the opposite's base, None otherwise
        Node[0]和Node[N-1]分别是player1和player2的基地
        请将以下代码替换interface1.1.py中，GameMap类end_early()方法中的pass
        """

        if self.nodes[0].belong == 'player2':
            return 1
        elif self.nodes[-1].belong == 'player1':
            return 2
        else:
            return None

    def high_score(self):
        """

        :return: 'player1', 'player2' if one player has higher final score, otherwise None
        先比较哪一方占领的节点数目多；如果两方占领的节点数目相等，那么比较剩余总兵力的多少
        """
        n_node1, n_node2, n_army1, n_army2 = 0, 0, 0, 0  # 分别表示两位玩家的占领节点数量，以及节点内总兵力
        for i in range(0, len(self.__nodes)):
            if self.nodes[i].belong == 'player1':
                n_node1 += 1
                # .power中,[0]是玩家1的兵力,[1]是玩家2的兵力
                n_army1 += self.nodes[i].power[0]
            elif self.nodes[i].belong == 'player2':
                n_node2 += 1
                n_army2 += self.nodes[i].power[1]
        if n_node1 > n_node2:
            return 'player1'
        elif n_node1 < n_node2:
            return 'player2'
        elif n_army1 > n_army2:
            return 'player1'
        elif n_army1 < n_army2:
            return 'player2'
        else:
            return None
