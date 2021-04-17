class GameException(Exception):

    def __init__(self):
        pass


class TimeoutException(GameException):

    def __init__(self, msg=''):
        self.msg = msg


