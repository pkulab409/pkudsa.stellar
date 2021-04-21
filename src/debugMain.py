from debugModule.SeleniumClass import SeleniumClass
from debugModule.GameCoreFordebug import GameDebug
from DesignGenerator import DesignGenerator
from HexagonForce import Generate_Hexagon
from MapDesign import g_design2

MAX_TURN = 100 #调试期间允许的最大轮数
MAX_TIME = 999 #调试期间允许的最大单步时间，改时间在mode == 1 or 2 时不生效

# 在这里修改AI的名字
player1 = 'player1'
player2 = 'player2'

# 使用何种地图生成器
# 0代表随机地图生成器
# 1代表六边形随机地图
# 2代表六边形固定地图
MAP_MODE= 2

MODE = 0
# 调试使用的mode
# 0代表AI对战
# 1代表人类与AI对战，此时AI为player1
# 2代表人类与人类对战

dg = DesignGenerator(bridge=0.8, branch=(2, 4), depth=3)
generate = {
    0: dg.generate(),
    1: Generate_Hexagon(4, 0.20, 0.20),
    2: g_design2
}


if MODE == 0:
    g = GameDebug(player1, player2, MAX_TIME, MAX_TURN, generate[MAP_MODE]).run()
elif MODE == 1:
    g = GameDebug(player1, 'HumanDebug', 100, MAX_TURN, generate[MAP_MODE]).run()
elif MODE == 2:
    g = GameDebug('HumanDebug', 'HumanDebug', 100, MAX_TURN, generate[MAP_MODE]).run()


input()# 使程序暂停，避免浏览器自动关闭


# 注意！请使用命令“pip3 install selenium”，如有bug，请向rock_magma反馈