from Node import Node
from typing import Tuple, List


class GameMap:

    def __init__(self, design):  # 由于地图是固定的，因此init不需要参数。
        self.__node_num = len(design)
        self.__nodes = [Node(i) for i in range(self.__node_num)]
        self.__player1_base = 0
        self.__player2_base = self.__node_num - 1
        self.__nodes[self.__player1_base].owner = 1
        self.__nodes[self.__player1_base].troop[1] = 100
        self.__nodes[self.__player2_base].owner = 2
        self.__nodes[self.__player2_base].troop[2] = 100

        for node_index in design.keys():
            for next_node in design[node_index].keys():
                self.__nodes[node_index].set_connection(next_node, design[node_index][next_node])
        # initialize according to the map design

    def nodes(self):
        return self.__nodes

    def check_action(self, action: Tuple[int, int, float], player_id: int):
        if player_id != 1 and player_id != 2:
            raise Exception(f"Who the fuck are you, {player_id}?")
        if not isinstance(action[0], int) or not isinstance(action[1], int):
            raise Exception(f"What on earth makes you think {type(action[0])}, {type(action[1])} are indexes?")
        if not 0 <= action[0] < self.__node_num or not 0 <= action[1] < self.__node_num:
            raise Exception(f"Index {action[0], action[1]} are out of bounds, you idiot.")
        if not action[1] in self.__nodes[action[0]].path_to:
            raise Exception(f"You cannot fly from {action[0]} to {action[1]}. Face it.")
        if not isinstance(action[2], (float, int)):
            raise Exception(f"Troops are not made from {type(action[2])}.")
        if action[2] > self.__nodes[action[0]].troop[player_id]:
            raise Exception(f"You've got only {self.__nodes[action[0]].troop[player_id]} troops in {action[0]}, not {action[2]}.")

    def __repr__(self):  # 方便测试时打印地图
        ans = []
        for i in self.__nodes[1::]:
            ans.append(repr(i))
        return "\n".join(ans)

    def __judge(self, actions: List[Tuple[int, int, float]], player_id: int):
        """
        此函数用于判断当回合派遣兵力是否合法
        传入参数为玩家当回合所有操作的表，如：[[1,2,5.0],[1,3,4.0],[2,3,6.0]]
        若派遣兵力总数大于该节点兵力则引发 RuntimeError
        """
        dic = {}  # dic[i]代表每个节点派出去多少兵
        for action in actions:
            self.check_action(action, player_id)
            if action[0] not in dic:
                dic[action[0]] = action[2]
            else:
                dic[action[0]] += action[2]
        # print(dic)
        for i in dic:
            if dic[i] > self.__nodes[i].troop[player_id]:
                raise RuntimeError('Judgement!!! Invalid move: insufficient army')

    def __move(self, player_id: int, player_action: Tuple[int, int, float]):
        """此函数为兵力调用函数，输入参数为玩家（player_1 或 player_2)和玩家操作（list)
            进行兵力调用时，该函数对每个玩家各执行一次即
            move('player_1',player_action1)
            move('player_2',player_action2)
            此函数并不涉及战斗部分，仅作用于兵力调用过程
            此函数将直接将地图进行更新
            需要调用地图复制函数copy()记录上局状态[summary]

        Args:
            player_id ([type]): [description]
            player_action ([type]): [description]
        """

        start = player_action[0]
        end = player_action[1]
        army = player_action[2]

        # 以下为行动主体函数
        self.__nodes[start].troop[player_id] -= army
        # 以根号作为兵力损耗的单位并且家手过路费
        army -= round(army ** 0.5 + self.__nodes[start].path_to[end], 2)
        army = 0.0 if army < 0.01 else army  # 兵力损耗至小于零时，相当于兵力为零
        self.__nodes[end].troop[player_id] += army

    def __combat(self):
        """第一部分为战斗过程，第二部分为战斗结算和归属变更
        """

        def combat_inner(node: Node):
            if node.troop[1] > node.troop[2]:
                node.troop[1] = round((node.troop[1] ** 2 - node.troop[2] ** 2) ** 0.5, 2)
                node.troop[2] = 0.0
            elif node.troop[2] > node.troop[1]:
                node.troop[2] = round((node.troop[2] ** 2 - node.troop[1] ** 2) ** 0.5, 2)
                node.troop[1] = 0.0
            else:
                node.troop[1] = node.troop[2] = 0.0

            if node.troop[1] > 0.0:
                node.owner = 1
            elif node.troop[2] > 0.0:
                node.owner = 2
            else:
                node.owner = 0

        for node in self.__nodes:
            combat_inner(node)

    def __spawn(self):
        """遍历每个节点将节点双方战力更改为增长或衰减后的战力

            ！！非常重要！！为了使该函数按预期工作，在初始化地图时，给每个节点预设的
            增长率要根据给该节点预设的战力上限来设置，它们的乘积应小于1
            也即，spawn_rate * army_limit < 1
            若增长率设得过大，将会产生严重后果！

            self为一个GampMap。

            以player_1为例，设计逻辑是，
            n.army[0]（新）- n.army[0]（旧）
            = 每回合army增长量
            = 节点增长率 * (上限 - n.army[0]（旧）)

            对于一个节点来说，节点增长率spawn_rate是恒定的，
            而 n.army[0]（旧）越接近上限，(上限 - n.army[0]（旧）) 就会越小，
            每回合增长量就会越小。

            当n.army[0]（旧）等于上限时，(上限 - n.army[0]（旧）) 等于0，
            不增长。

            当n.army[0]（旧）大于上限时，(上限 - n.army[0]（旧）) 为负数，
            每回合增长量小于0，出现衰减。

            ！！攻城方在战力小于上限时不会增长，但在战力大于上限时仍会衰减。

            提示：每回合增长量是n.army[0]（旧）的二次函数，
            当n.army[0]（旧）等于上限一半时，该二次函数取最大值，
            所以，如果要维持一个节点的最大产出，该节点的战力应该保持在该节点战力上限的1/2，
            超过的战力可以及时派出去。
        """
        for node in self.__nodes:
            if node.owner == 1:
                node.troop[0] = node.troop[0] + node.spawn_rate * \
                             (node.supply_limit - node.troop[0]) * node.troop[0]
                if node.troop[1] > node.supply_limit:
                    node.troop[1] = node.troop[1] + node.spawn_rate * \
                                 (node.supply_limit - node.troop[1]) * node.troop[1]
            if node.owner == 2:
                node.troop[1] = node.troop[1] + node.spawn_rate * \
                             (node.supply_limit - node.troop[1]) * node.troop[1]
                if node.troop[0] > node.supply_limit:
                    node.troop[0] = node.troop[0] + node.spawn_rate * \
                                 (node.supply_limit - node.troop[0]) * node.troop[0]

    def update(self, player1_actions: List[Tuple[int, int, float]], player2_actions: List[Tuple[int, int, float]]):
        """[summary]

        Args:
            player1_actions ([type]): [description]
            player2_actions ([type]): [description]
        """

        self.__judge(player1_actions, 1)
        self.__judge(player2_actions, 2)

        for action in player1_actions:
            self.__move(1, action)
        for action in player2_actions:
            self.__move(2, action)

        self.__combat()
        self.__spawn()

    def end_early(self):
        """
        :return: 1, 2 if one player wins by occupying the opposite's base, None otherwise
        Node[0]和Node[N-1]分别是player1和player2的基地
        请将以下代码替换interface1.1.py中，GameMap类end_early()方法中的pass
        """

        if self.__nodes[self.__player1_base].owner == 2:
            return 2
        elif self.__nodes[self.__player2_base].owner == 1:
            return 1
        else:
            return None

    def high_score(self):
        """

        :return: 1, 2 if one player has higher final score, otherwise None
        先比较哪一方占领的节点数目多；如果两方占领的节点数目相等，那么比较剩余总兵力的多少
        """
        n_node1, n_node2, n_army1, n_army2 = 0, 0, 0, 0  # 分别表示两位玩家的占领节点数量，以及节点内总兵力
        for i in range(0, len(self.__nodes)):
            if self.__nodes[i].owner == 1:
                n_node1 += 1
                # .army中,[0]是玩家1的兵力,[1]是玩家2的兵力
                n_army1 += self.__nodes[i].troop[0]
            elif self.__nodes[i].owner == 2:
                n_node2 += 1
                n_army2 += self.__nodes[i].troop[1]
        if n_node1 > n_node2:
            return 1
        elif n_node1 < n_node2:
            return 2
        elif n_army1 > n_army2:
            return 1
        elif n_army1 < n_army2:
            return 2
        else:
            return None
