import os, sys, ast, traceback, json
from tkinter import filedialog
from copy import deepcopy

# 更改根目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

### ========= 配置区域 =========
# 源代码路径，若更改本文件与src目录相对位置需更改该参数
SRC_PATH = '../src/'
# 玩家代码1文件位置，默认留空时将从命令行参数1或input读取；重写则固定为该文件
PLAYER1_PATH = ''
# 玩家代码2文件位置，默认留空时将从命令行参数2或input读取；重写则固定为该文件
PLAYER2_PATH = ''
# 比赛记录输出位置
OUTPUT_DIR = './output.json'
# 是否用tkinter dialog选择文件
USE_DIALOG = (os.sys.platform == 'win32')
### ========= 配置结束 =========

if '初始配置':
    sys.path.append(os.path.abspath(SRC_PATH))  # 链接src目录
    # 获取初始玩家代码路径
    PLAYERS = [PLAYER1_PATH, PLAYER2_PATH]
    for i in 1, 2:
        if len(sys.argv) > i:
            PLAYERS[i - 1] = PLAYERS[i - 1] or sys.argv[i]
    # 导入模块
    from GameCore import Game
    import config
    from TimeLimit import time_limit
    from HexagonForce import Generate_Hexagon
    if 'disable print':
        import HexagonForce
        HexagonForce.print = lambda *a, **kw: None


class GameWithModule(Game):
    @staticmethod
    def load_module(path):
        """
        加载代码文件并读为玩家模块
        可报错
        """
        filename = os.path.basename(path)

        # 读取代码内容
        with open(path, encoding='utf-8', errors='ignore') as f:
            code = f.read()

        # 尝试解析为AST
        tree = ast.parse(code, filename)

        # 写入模块
        pack = type(ast)('code(%s)' % filename)
        exec(compile(tree, '', 'exec'), pack.__dict__)

        # 检查必要函数
        pack.player_class.player_func

        # 返回
        return pack

    @property
    def map(self):
        return self.get_history()

    def __init__(self, modules, names, params):
        """
        重写初始化
        params:
            modules: 双方玩家模块
            names: 双方姓名
            params: 可重载比赛参数
        """
        # 创建地图
        maps = Generate_Hexagon(7, 0.35, 0.10)

        # 父类初始化
        super().__init__(*names, maps)

        # 尝试实例化玩家类
        players = [None] * 2
        errors = [None] * 2
        for i, mod in enumerate(modules):
            try:
                players[i] = mod.player_class(i)
            except Exception as e:
                errors[i] = e
        endgame, winner = False, None
        if any(errors):
            endgame = True
            if all(errors):
                self.map['result'] = output_error(errors)
            else:
                winner = int(bool(errors[0]))
                self.map['result'] = output_error(errors[1 - winner])
            self.map['result'] = '初始化错误: %s' % self.map['result']

        # 强制初始化
        self.__dict__.update(
            _Game__game_end=endgame,
            _Game__player=players,
            _Game__winner=winner,
        )

    def run(self):
        ''' 按平台规范写入胜者 '''
        if not self._Game__game_end:
            super().run()
        if self._Game__winner not in (0, 1):
            self._Game__winner = None
        self.map['winner'] = self._Game__winner

    def next_step(self):
        """
        报错跳过改为原地抛出异常中断
        """
        map_info1 = deepcopy(self._Game__map)
        map_info2 = deepcopy(self._Game__map)
        with time_limit(self._Game__max_time, "player1"):
            player1_actions = self._Game__player[0].player_func(map_info1)
        with time_limit(self._Game__max_time, "player2"):
            player2_actions = self._Game__player[1].player_func(map_info2)

        # 历史地图字典，存入列表
        self.map["history"].append(
            self._Game__map.update(player1_actions, player2_actions))


def ensure_players():
    """
    确保双方玩家代码正确可读取
    返回玩家模块与名称列表
    """
    PLAYER_MODULES = [None] * 2
    PLAYER_NAMES = ['code'] * 2
    _LAST_DIR = SRC_PATH
    for i in range(2):
        while 1:
            player_name = os.path.basename(PLAYERS[i])
            try:
                mod = GameWithModule.load_module(PLAYERS[i])
            except:
                if PLAYERS[i]:
                    print('*** 玩家%d代码 (%s) 无效，报错如下： ***' % (i + 1, PLAYERS[i]))
                    traceback.print_exc()
                if USE_DIALOG:
                    print('请选择玩家%d代码' % (i + 1))
                    PLAYERS[i] = filedialog.askopenfilename(
                        initialdir=_LAST_DIR,
                        title="选择玩家%d代码" % (i + 1),
                        filetypes=(("py文件", "*.py"), ("全部", "*.*")))
                    _LAST_DIR = os.path.dirname(PLAYERS[i])
                else:
                    PLAYERS[i] = input('请选择玩家%d代码：' % (i + 1))
            else:
                PLAYER_MODULES[i] = mod
                PLAYER_NAMES[i] = player_name
                break

    return PLAYER_MODULES, PLAYER_NAMES


if __name__ == '__main__':
    # 确保玩家代码
    modules, names = ensure_players()

    # 运行游戏
    game = GameWithModule(modules, names, {})
    game.run()

    # 保存记录
    with open(OUTPUT_DIR, 'w', encoding='utf-8') as f:
        json.dump(game.map, f, ensure_ascii=0)
