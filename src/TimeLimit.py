import _thread
import threading
from contextlib import contextmanager

from GameException import TimeoutException


@contextmanager
def time_limit(seconds, msg=''):
    """这是限制AI运算时间的计时器，使用with结构使用即可

    Args:
        seconds (int): 现实的时间，单位/s
        msg (str, optional): 运行的AI. Defaults to ''.

    Raises:
        TimeoutException: 运行时间超出报错
    """
    timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        raise TimeoutException("Timed out for operation {}".format(msg))
    finally:
        # if the action ends in specified time, timer is canceled
        timer.cancel()
