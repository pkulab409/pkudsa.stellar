import json

from GameCore import Game
from MapDesign import g_design
from DesignGenerator import DesignGenerator
from HexagonForce import Generate_Hexagon

cnt = [0, 0]

if __name__ == '__main__':
    for i in range(1):
        # dg = DesignGenerator(bridge=0.8, branch=(2, 4), depth=3)
        g = Game('XHZAI一代', 'player2', Generate_Hexagon(4, 0.20, 0.20))

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

    # 导出地图，给可视化
    with open("output.json", "w") as _f:
        json.dump(g.get_history(), _f)