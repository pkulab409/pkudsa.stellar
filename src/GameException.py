class TimeoutException(Exception):
    def __init__(self, msg=''):
        """超时Exception

        Args:
            msg (str, optional): 错误信息. Defaults to ''.
        """
        self.msg = msg
