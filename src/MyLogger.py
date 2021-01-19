# ===================================================================================
import logging
import coloredlogs
import time
import math
import sys
import os
import inspect
from memory_profiler import profile
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
        if not os.path.exists("../data/"):
            os.makedirs("../data/")
        handler = logging.FileHandler('../data/output.log', 'w', 'utf-8')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s : %(levelname)s : %(message)s', datefmt='%Y/%m/%d %H:%M:%S'))
        logger.addHandler(handler)
        # logger.warning = self.warning
        logger._log = self._log
        self.stack = {}
        self.stacklevel = 0
# ===================================================================================
    @classmethod
    def GetInstance(cls, level='INFO'):
        if not hasattr(cls, "this_"):
            cls.this_ = cls(level=level)
        return cls.this_
# ===================================================================================
    @classmethod
    def deco(cls, func):
        callstack = inspect.stack()[1].code_context[0]
        callstack = callstack[callstack.find("def ")+4:]
        callstack = callstack[:callstack.find("("):]
        def decowrapper(*args,**kwargs):
            cls.GetInstance().begin(callstack)
            ret = func(*args,**kwargs)
            cls.GetInstance().finish()
            return ret
        return decowrapper
# ===================================================================================
    def begin(self, callstack):
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
        stack = self.stack[self.stacklevel].copy()
        del stack['start']
        self.info(stack)
# ===================================================================================
    def finish(self):
        for i in range(1,self.stacklevel+1,1):
            start = self.stack[i]['start']
            elapsedTime = math.floor(time.time() - start)
            self.stack[i]['elapsedTime'] = elapsedTime
        stack = self.stack[self.stacklevel].copy()
        del stack['start']
        self.info(stack)
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
if __name__ == "__main__":
    mylogger = mylogger('DEBUG')
    @mylogger.deco
    def critical():
        mylogger.critical("This is CRITICAL.")
    @mylogger.deco
    def error():
        mylogger.error("This is ERROR.")
    @mylogger.deco
    def warning():
        mylogger.warning("This is WARNING.")
    @mylogger.deco
    def info():
        mylogger.info("This is INFO.")
    @mylogger.deco
    def debug():
        mylogger.debug("This is DEBUG.")
    @mylogger.deco
    def test():
        critical()
        error()
        warning()
        info()
        debug()
    test()
#============================================================================================================================================================================================================================================================
