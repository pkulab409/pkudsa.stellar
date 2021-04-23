import json
from GameCore import Game
from MapDesign import g_design
from DesignGenerator import DesignGenerator
from HexagonForce import Generate_Hexagon






class Player:
    def __init__(self, player_name: str):
        self.name = player_name
        self.point = 0
        self.history = [] # FOr example: (player, "win")代表和player对战，赢了. 
        self.wins = 0
        self.losses = 0
        self.draws = 0
    
    def small_point(self):
        return sum(h[0].point for h in self.history)
    
    def __lt__(self, p):
        if self.point<p.point:
            return True
        elif self.point>p.point:
            return False
        else:
            return self.small_point()<p.small_point()
    
    def __repr__(self):
        return ("""     ============================================
        Player name: %s   Point: %d     %dW/%dD/%dL
        History: 
        """%(self.name, self.point, self.wins, self.draws, self.losses) + str(
            [(i[0].name, i[1]) for i in self.history]
            ) + "\n"
        )

    
    def win(self, p):
        self.wins += 1
        self.history.append((p, "win"))
        self.point += 3
    
    def lose(self, p):
        self.losses += 1
        self.history.append((p, "lose"))
        self.point += 0
    
    def draw(self, p):
        self.draws += 1
        self.history.append((p, "draw"))
        self.point += 1


def Match(player1: Player, player2: Player):
    cnt = [0, 0]
    for i in range(1):
        # dg = DesignGenerator(bridge=0.8, branch=(2, 4), depth=3)
        g = Game(player1.name, player2.name, Generate_Hexagon(4, 0.20, 0.20))

        fuck = g.run()
        if fuck==0:
            cnt[0] += 1
        elif fuck==1:
            cnt[1] += 1

    if cnt[0]>cnt[1]:
        player1.win(player2)
        player2.lose(player1)
    elif cnt[0]<cnt[1]:
        player2.win(player1)
        player1.lose(player2)
    else:
        player1.draw(player2)
        player2.draw(player1)
    # 导出地图，给可视化
    # with open("output.json", "w") as _f:
    #     json.dump(g.get_history(), _f)
    
        





class Swiss_System:
    def __init__(self, player_list: list):
        self.players = [Player(i) for i in player_list]
        if len(player_list)%2 != 0:
            self.players.append(Player("凑数选手"))
        self.turns = 0
    
    def __repr__(self):
        ans = """⭐======================================================================⭐
        [Swiss System]
        Turns: %d\n"""%self.turns
        for i in self.players:
            ans += repr(i)
        return ans
    
    def next_turn(self):
        for i in range(len(self.players)//2):
            player1 = self.players[2*i]
            player2 = self.players[2*i+1]
            Match(player1, player2)
        self.players = sorted(self.players, reverse=True)
        self.turns += 1
        print(self)

if __name__ == "__main__": # 测试代码
    a = Swiss_System(["player2", "player1测试名字", "player2", "player2", "noob"])
    for i in range(3):
        a.next_turn()