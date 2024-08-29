from datetime import datetime
import inspect

FORMAT = "%Y-%m-%d %H:%M:%S"
RESET_ANSI = '\033[0m'
FUNCTION_ANSI = '\033[35m'

"""
Level 0 for DEBUG+
Level 1 for INFO+
Level 2 for SUCCESS+
Level 3 for WARN+
"""
LEVEL = 0

class Logger():

    @staticmethod
    def format_time():
        return datetime.now().strftime(FORMAT)

    @staticmethod
    def get_caller_function_name():
        frame = inspect.stack()[2]
        return frame.function

    @staticmethod
    def debug(message):
        if LEVEL in [0]:
            func_name = Logger.get_caller_function_name()
            print(f"\033[33m{Logger.format_time()}{RESET_ANSI} DEBUG {FUNCTION_ANSI}{func_name} {RESET_ANSI}{message}")

    @staticmethod
    def info(message):
        if LEVEL in [0, 1]:
            func_name = Logger.get_caller_function_name()
            print(f"\033[33m{Logger.format_time()}{RESET_ANSI} \033[36mINFO {FUNCTION_ANSI}{func_name} {RESET_ANSI}{message}")

    @staticmethod
    def success(message):
        if LEVEL in [0, 1, 2]:
            func_name = Logger.get_caller_function_name()
            print(f"\033[33m{Logger.format_time()}{RESET_ANSI} \033[32mSUCCESS {FUNCTION_ANSI}{func_name} {RESET_ANSI}{message}")

    @staticmethod
    def warn(message):
        if LEVEL in [0, 1, 2, 3]:
            func_name = Logger.get_caller_function_name()
            print(f"\033[33m{Logger.format_time()}{RESET_ANSI} \033[34mWARN {FUNCTION_ANSI}{func_name} {RESET_ANSI}{message}")

    @staticmethod
    def error(message):
        if LEVEL in [0, 1, 2, 3, 4]:
            func_name = Logger.get_caller_function_name()
            print(f"\033[33m{Logger.format_time()}{RESET_ANSI} \033[31mERROR {FUNCTION_ANSI}{func_name} {RESET_ANSI}{message}")
