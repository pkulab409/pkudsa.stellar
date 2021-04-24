from GameCore import Game
from HexagonForce import Generate_Hexagon
from DesignGenerator import DesignGenerator
from typing import List, Optional, Tuple, Callable
import os

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
    
    def match(self, player1_index: int, player2_index: int) -> Tuple[int]:
        score = [0, 0]
        player1 = self.participants[player1_index]
        player2 = self.participants[player2_index]
        for turn in range(self.repeat):
            g = Game(player1, player2, self.map_generator())
            winner = g.run()
            if winner == 0 or winner == 1:
                score[winner] += 1
                if score[winner] > self.repeat // 2 + 1:
                    break
        #while score[0] == score[1]:
        return (player1_index, player2_index) if score[0] > score[1] else (player2_index, player1_index)
    
    def make_group(self, index_list: List[int]) -> List[Tuple[int]]:
        length = len(index_list)
        assert length in (2, 4, 8)
        return list(zip(index_list[:length//2], index_list[-1:length//2 - 1:-1]))
    
    def match_all(self, index_list: List[int]):
        group = self.make_group(index_list)
        return list(list(x) for x in zip(*map(lambda pair: self.match(*pair), group)))
    
    def single_elimination(self) -> str:
        """single elimination game

        Returns:
            str: The winner's name
        """
        fourth_winners = self.match_all([*range(8)])[0]
        semi_winners = self.match_all(fourth_winners)[0]
        final_winner = self.match_all(semi_winners)[0]
        return self.participants[final_winner[0]]

    def double_elimination(self) -> List[str]:
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
        "player2",
        "player2",
        "player2",
        "player2",
        "player2",
        "player2",
        "player2",
        "player2",
    ]

    e = EliminationGame(ai_list, DesignGenerator(0.8, (2, 4), 3), 5)
    #e = EliminationGame(ai_list, lambda:  Generate_Hexagon(4, 0.20, 0.20), 5)
    a = e.double_elimination()
    print(a)
