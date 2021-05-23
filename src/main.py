import json
import sys

from GameCore import Game
from MapDesign import g_design
from DesignGenerator import DesignGenerator
from HexagonForce import Generate_Hexagon

cnt = [0, 0]
#player_file1, player_flie2 = sys.argv[1], sys.argv[2]
player_file1, player_flie2 = "XHZAI一代", "XHZAI一代"
print(player_file1, player_flie2)

if __name__ == '__main__':
    for i in range(1):
        # dg = DesignGenerator(bridge=0.8, branch=(2, 4), depth=3)
        g = Game(player_file1, player_flie2, Generate_Hexagon(4, 0.20, 0.20))

        fuck = g.run()
        if fuck == 0:
            cnt[0] += 1
        elif fuck == 1:
            cnt[1] += 1
        # 导出地图，给可视化
        with open("output_lose.json", "w") as _f:
            json.dump(g.get_history(), _f)
        print("now", cnt[0], cnt[1])
        print(g.get_history()["result"])
    print(cnt)

    # print(f"{g.run()} wins!")

