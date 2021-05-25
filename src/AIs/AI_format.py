# 你的AI一定要包含以下的类：

class player_class:
    def __init__(self, player_id:int):
        # 允许玩家在这里初始化并存储一些需要用到的变量，如self.id
        self.player_id = player_id

    def player_func(self, map_info:GameMap):
        # 此处会传入当前局面信息，请在这里写下您AI的主体
        pass

# 具体规则参见开发文档！