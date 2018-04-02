import logging


class Log(object):
    def __init__(self):
        """
        Level           Value
        CRITICAL	50
        ERROR           40
        WARNING         30
        INFO            20
        DEBUG           10
        NOTSET          0
        """
        self.logger = logging.getLogger('root')
        FORMAT = "[%(asctime)s %(levelname)s %(filename)s:%(lineno)s] - %(funcName)s() %(message)s"
        logging.basicConfig(format=FORMAT)
        self.logger.setLevel(10)