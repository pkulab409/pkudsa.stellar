import json

from GameCore import Game
from MapDesign import g_design
from config import MAX_TIME, MAX_TURN

cnt = [0, 0]

if __name__ == '__main__':
    for i in range(30):
        g = Game('AIs.player1', 'AIs.player2', MAX_TIME, MAX_TURN, g_design['design'])

        fuck = g.run()
        if fuck == "player1":
            cnt[0] += 1
        elif fuck == "player2":
            cnt[1] += 1
            # 导出地图，给可视化
            with open("output_lose.json", "w") as _f:
                json.dump(g.get_history(), _f)
        print("now", cnt[0], cnt[1])
    print(cnt)

    # print(f"{g.run()} wins!")

    # 导出地图，给可视化
    with open("output.json", "w") as _f:
        json.dump(g.get_history(), _f)
