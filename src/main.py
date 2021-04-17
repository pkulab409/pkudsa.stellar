from GameCore import Game
from MapDesign import g_design

MAX_TIME = 999999
MAX_TURN = 10

if __name__ == '__main__':
    g = Game('human', 'human', MAX_TIME, MAX_TURN, g_design)
    print(f"{g.run()} wins!")
