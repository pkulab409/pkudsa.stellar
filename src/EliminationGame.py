from GameCore import Game
from HexagonForce import Generate_Hexagon
from DesignGenerator import DesignGenerator
from typing import List, Optional, Tuple, Callable
import os, json

ROOT_PATH = r'D:/dir_test'


class EliminationGame:
    def dump_record(self, tag, plr_idx, round_idx, record):
        plr_names = [self.participants[i] for i in plr_idx]
        vs_group = f'{plr_idx[0]}.{plr_names[0]} vs. {plr_idx[1]}.{plr_names[1]}'
        output_dir = os.path.join(ROOT_PATH, tag, vs_group,
                                  f'{round_idx:02d}.json')
        os.makedirs(os.path.dirname(output_dir), exist_ok=1)
        with open(output_dir, 'w', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=0, separators=',:')
    
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
    
    def match(self, player1_index: int, player2_index: int):
        score = [0, 0]
        player1 = self.participants[player1_index]
        player2 = self.participants[player2_index]
        for turn in range(self.repeat):
            g = Game(player1, player2, self.map_generator())
            winner = g.run()
            self.dump_record(self.tag, (player1_index, player2_index), turn,
                             g.get_history())
            if winner == 0 or winner == 1:
                score[winner] += 1
                if score[winner] > self.repeat // 2 + 1:
                    break
        #while score[0] == score[1]:
        return (player1_index, player2_index) if score[0] > score[1] else (player2_index, player1_index)
    
    def make_group(self, index_list: List[int]):
        length = len(index_list)
        assert length in (2, 4, 8)
        return list(zip(index_list[:length//2], index_list[-1:length//2 - 1:-1]))
    
    def match_all(self, index_list: List[int], tag='default'):
        self.tag = tag # match context
        group = self.make_group(index_list)
        return list(list(x) for x in zip(*map(lambda pair: self.match(*pair), group)))
    
    def single_elimination(self):
        """single elimination game

        Returns:
            str: The winner's name
        """
        fourth_winners = self.match_all([*range(8)], 'a. 8进4')[0]
        semi_winners, semi_losers = self.match_all(fourth_winners, 'b. 半决赛')
        final_winner = self.match_all(semi_winners, 'c. 决赛')[0]
        third = self.match_all(semi_losers, 'd. 季军')[0]
        return self.participants[final_winner[0]]

    def double_elimination(self):
        """Double elimination game
        see https://zh.wikipedia.org/wiki/%E5%8F%8C%E8%B4%A5%E6%B7%98%E6%B1%B0%E5%88%B6#/media/File:DoubleElim.jpg
        Returns:
            List[str]: [1st place, 2nd place, 3rd place, 4th place]
        """
        winners, losers = self.match_all([*range(8)])

        losers = self.match_all(losers)[0]
        winners, winner_losers = self.match_all(winners)
        losers = self.match_all(winner_losers + losers)[0]

        third, fourth = self.match_all(losers)
        first, second = self.match_all(winners)
        second, third = self.match_all(second + third)
        first, second = self.match_all(second + first)

        return [*map(lambda x: self.participants[x], first + second + third + fourth)]

if __name__ == "__main__":
    ai_list = [
        "player1_调参1",
        "player1_调参2",
        "player1测试名字",
        "player2",
        "凑数选手",
        "凑数选手",
        "凑数选手",
        "凑数选手",
    ]

    #e = EliminationGame(ai_list, DesignGenerator(0.8, (2, 4), 3), 5)
    e = EliminationGame(ai_list, lambda:  Generate_Hexagon(7, 0.35, 0.10), 5)
    a = e.single_elimination()
    print(a)
