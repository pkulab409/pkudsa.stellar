from debugModule.SeleniumClass import SeleniumClass
from debugModule.GameCoreFordebug import GameDebug
from DesignGenerator import DesignGenerator
from MapDesign import g_design2

MAX_TURN = 100 #调试期间允许的最大轮数
MAX_TIME = 999 #调试期间允许的最大单步时间，改时间在mode == 1 or 2 时不生效

# 在这里修改AI的名字
player1 = 'player1'
player2 = 'player2'

# 是否使用随机生成的地图
IF_USED_RANDOM_MAP = False

MODE = 0
# 调试使用的mode
# 0代表AI对战
# 1代表人类与AI对战，此时AI为player1
# 2代表人类与人类对战

if IF_USED_RANDOM_MAP:
    dg = DesignGenerator(bridge=0.8, branch=(2, 4), depth=3)
    if MODE == 0:
        g = GameDebug(player1, player2, MAX_TIME, MAX_TURN, dg.generate()).run()
    elif MODE == 1:
        g = GameDebug(player1, 'HumanDebug', 100, MAX_TURN, dg.generate()).run()
    elif MODE == 2:
        g = GameDebug('HumanDebug', 'HumanDebug', 100, MAX_TURN, dg.generate()).run()
else:
    if MODE == 0:
        g = GameDebug(player1, player2, MAX_TIME, MAX_TURN, g_design2).run()
    elif MODE == 1:
        g = GameDebug(player1, 'HumanDebug', 100, MAX_TURN, g_design2).run()
    elif MODE == 2:
        g = GameDebug('HumanDebug', 'HumanDebug', 100, MAX_TURN, g_design2).run()

input()


# 注意！请使用命令“pip3 install selenium”，如有bug，请向rock_magma反馈