# ===================================================================================
import logging
import coloredlogs
import time
import math
import sys
# ===================================================================================
logger = logging.getLogger(__file__)
origin_critical = logger.critical
origin_error = logger.error
origin_warning = logger.warning
origin_info = logger.info
origin_debug = logger.debug
origin_log = logger._log
# ===================================================================================
class mylogger:
    def __init__(self, level='INFO'):
        coloredlogs.CAN_USE_BOLD_FONT = True
        coloredlogs.DEFAULT_FIELD_STYLES = {'asctime': {'color': 'green'},
                                            'hostname': {'color': 'magenta'},
                                            'levelname': {'color': 'black', 'bold': True},
                                            'name': {'color': 'blue'},
                                            'programname': {'color': 'cyan'}
                                            }
        coloredlogs.DEFAULT_LEVEL_STYLES = {'critical': {'color': 'red', 'bold': True},
                                            'error': {'color': 'red'},
                                            'warning': {'color': 'yellow'},
                                            'notice': {'color': 'magenta'},
                                            'info': {},
                                            'debug': {'color': 'green'},
                                            'spam': {'color': 'green', 'faint': True},
                                            'success': {'color': 'green', 'bold': True},
                                            'verbose': {'color': 'blue'}
                                            }
        coloredlogs.install(level=level, logger=logger,
                            fmt='[ %(asctime)s ][ %(levelname)s ][ %(funcName)s ][ %(message)s ]', datefmt='%Y/%m/%d %H:%M:%S')
        handler = logging.FileHandler('output.log', 'w', 'utf-8')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s : %(levelname)s : %(message)s', datefmt='%Y/%m/%d %H:%M:%S'))
        logger.addHandler(handler)
        # logger.warning = self.warning
        logger._log = self._log
        self.stack = {}
        self.stacklevel = 0
# ===================================================================================
    def deco(self, func):
        callstack = sys._getframe().f_back.f_code.co_name
        print(callstack)
        def decowrapper(*args,**kwargs):
            self.start(callstack)
            ret = func(*args,**kwargs)
            self.complete()
            return ret
        return decowrapper
# ===================================================================================
    def start(self, callstack):
        func = callstack
        start = time.time()
        self.stacklevel += 1
        self.stack[self.stacklevel] = {}
        self.stack[self.stacklevel]['level'] = self.stacklevel
        self.stack[self.stacklevel]['func'] = func
        self.stack[self.stacklevel]['start'] = math.floor(start)
        for i in range(1,self.stacklevel+1,1):
            start = self.stack[i]['start']
            elapsedTime = math.floor(time.time() - start)
            self.stack[i]['elapsedTime'] = elapsedTime
            self.info(self.stack[i])
# ===================================================================================
    def complete(self):
        for i in range(1,self.stacklevel+1,1):
            start = self.stack[i]['start']
            elapsedTime = math.floor(time.time() - start)
            self.stack[i]['elapsedTime'] = elapsedTime
            self.info(self.stack[i])
        self.stacklevel -= 1
# ===================================================================================
    def critical(self, *args, **kwargs):
        msg = ""
        for arg in args:
            msg += str(arg)
        origin_critical(msg, **kwargs)
# ===================================================================================
    def error(self, *args, **kwargs):
        msg = ""
        for arg in args:
            msg += str(arg)
        origin_error(msg, **kwargs)
# ===================================================================================
    def warning(self, *args, **kwargs):
        msg = ""
        for arg in args:
            msg += str(arg)
        origin_warning(msg, **kwargs)
# ===================================================================================
    def info(self, *args, **kwargs):
        msg = ""
        for arg in args:
            msg += str(arg)
        origin_info(msg, **kwargs)
# ===================================================================================
    def debug(self, *args, **kwargs):
        msg = ""
        for arg in args:
            msg += str(arg)
        origin_debug(msg, **kwargs)
# ===================================================================================
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=3):
        origin_log(level, msg, args, exc_info, extra, stack_info, stacklevel)
# ===================================================================================
# ===================================================================================
if __name__ == "__main__":
    mylogger = mylogger('DEBUG')
    @mylogger.deco
    def test():
        logger.critical("This is CRITICAL.")
        mylogger.critical("This is CRITICAL.")
        logger.error("This is ERROR.")
        mylogger.error("This is ERROR.")
        logger.warning("This is WARNING.")
        mylogger.warning("This is WARNING.")
        logger.info("This is INFO.")
        mylogger.info("This is INFO.")
        logger.debug("This is DEBUG.")
        mylogger.debug("This is DEBUG.")
    test()
#============================================================================================================================================================================================================================================================
