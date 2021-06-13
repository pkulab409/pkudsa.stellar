from GameCore import Game
from HexagonForce import Generate_Hexagon
from DesignGenerator import DesignGenerator
from typing import List, Optional, Tuple, Callable
import os
import json

if 'disable print':

    class fake_out:
        def __getattr__(self, a):
            return lambda *a, **k: 0

    def deco_print(func):
        def inner(*a, **k):
            k['file'] = k.get('file', sys.__stdout__)
            return func(*a, **k)

        return inner

    import sys
    sys.stdout = fake_out()
    print = deco_print(print)

ROOT_DIR='D:/_test'

rule1 = \
[
    {"name":"四分之一决赛", "winner": "半决赛", "loser": "GG"},
    {"name":"半决赛", "winner": "决赛", "loser": "季军争夺赛"},
    {"name":"决赛", "winner": "冠军", "loser": "亚军"},
    {"name":"季军争夺赛", "winner": "季军", "loser": "GG"},

]

rule2 = \
[
    {"name":"第一轮", "winner": "第二轮胜组", "loser": "第二轮败组首阶段"},
    {"name":"第二轮败组首阶段", "winner": "第二轮败组次阶段", "loser": "GG"},
    {"name":"第二轮胜组", "winner": "第三轮胜组", "loser": "第二轮败组次阶段"},
    {"name":"第二轮败组次阶段", "winner": "第三轮败组首阶段", "loser": "GG"},
    {"name":"第三轮败组首阶段", "winner": "第三轮败组次阶段", "loser": "GG"},
    {"name":"第三轮胜组", "winner": "决赛", "loser": "第三轮败组次阶段"},
    {"name":"第三轮败组次阶段", "winner": "决赛", "loser": "季军"},
    {"name":"决赛", "winner": "冠军", "loser": "亚军"},
]


class EliminationGame:

    def __init__(self, participants: List[str], map_generator: Callable, repeat: int=5):
        """Initialize an elimination game

        Args:
            participants (List[str]): List of bots names in ./AIs directory
            map_generator (Callable): A callable object returns a map design
            repeat (int, optional): The number of rounds in each match. Defaults to 5.

        Raises:
            RuntimeError: Number of bots is not 8
        """
        if len(participants) != 8:
            raise RuntimeError("Too few or many participants")
        self.participants = participants
        self.repeat = repeat
        self.map_generator = map_generator

    def match(self, player1_index: int, player2_index: int, round_name):
        match_name = self.participants[player1_index] + " - " + self.participants[player2_index]
        print("-"*40)
        print(f"{self.participants[player1_index]} VS {self.participants[player2_index]}")
        score = [0, 0]
        player1 = self.participants[player1_index]
        player2 = self.participants[player2_index]
        input()
        for turn in range(self.repeat):
            g = Game(player1, player2, self.map_generator())
            winner = g.run()
            history = g.get_history()
            print(winner)
            if winner == 0:
                print(self.participants[player1_index])
            elif winner == 1:
                print(self.participants[player2_index])
            json_path = os.path.join(ROOT_DIR,
                                     f"{round_name}/{match_name}/{turn}.json")
            os.makedirs(os.path.dirname(json_path), exist_ok=1)
            with open(json_path, "w") as file:
                json.dump(history, file)

            if winner == 0 or winner == 1:
                score[winner] += 1
                if score[winner] > self.repeat // 2 + 1:
                    break
        #while score[0] == score[1]:
        print(f"{score[0]} -- {score[1]}")
        return (player1_index, player2_index) if score[0] > score[1] else (player2_index, player1_index)

    def make_group(self, index_list: List[int]):
        length = len(index_list)
        assert length in (2, 4, 8)
        # return list(zip(index_list[:length//2], index_list[-1:length//2 - 1:-1]))
        return list(index_list[i:i + 2] for i in range(0, length, 2))

    def match_all(self, index_list: List[int], info):
        if not os.path.exists(f"{info['name']}"):
            os.mkdir(f"{info['name']}")
        print("="*40)
        print(info["name"])
        print("本轮参赛：", index_list)
        group = self.make_group(index_list)
        print("对阵情况：", group)
        res = list(list(x) for x in zip(*map(lambda pair: self.match(*pair, info["name"]), group)))
        print(f"胜者：{res[0]} -> {info['winner']}")
        print(f"败者：{res[1]} -> {info['loser']}")
        return res

    def single_elimination(self):
        """single elimination game

        Returns:
            str: The winner's name
        """
        fourth_winners = self.match_all([*range(8)], rule1[0])[0]
        semi_winners, semi_losers = self.match_all(fourth_winners, rule1[1])
        first, second = self.match_all(semi_winners, rule1[2])
        third = self.match_all(semi_losers, rule1[3])[0]
        print("="*40)
        print("冠军", self.participants[first[0]])
        print("亚军", self.participants[second[0]])
        print("季军", self.participants[third[0]])

    def double_elimination(self):
        """Double elimination game
        see https://zh.wikipedia.org/wiki/%E5%8F%8C%E8%B4%A5%E6%B7%98%E6%B1%B0%E5%88%B6#/media/File:DoubleElim.jpg
        Returns:
            List[str]: [1st place, 2nd place, 3rd place, 4th place]
        """
        winners, losers = self.match_all([*range(8)], rule2[0])

        losers = self.match_all(losers, rule2[1])[0]
        winners, winner_losers = self.match_all(winners, rule2[2])
        losers = self.match_all(winner_losers + losers, rule2[3])[0]

        third, fourth = self.match_all(losers, rule2[4])
        first, second = self.match_all(winners, rule2[5])
        second, third = self.match_all(second + third, rule2[6])
        first, second = self.match_all(second + first, rule2[7])

        return [*map(lambda x: self.participants[x], first + second + third + fourth)]

if __name__ == "__main__":
    ai_list = [
        "delta",
        "victor",
        "papa",
        "520",
        "yankee",
        "777",
        "404",
        "2333"
    ]
    ai_list = ['stupidAI']*8

    e = EliminationGame(ai_list, lambda:  Generate_Hexagon(7, 0.35, 0.10), 11)
    a = e.single_elimination()
