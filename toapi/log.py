"""
logger.info(Fore.GREEN, 'Sent', 'https://fuck.com/path1 1231 200')
logger.info(Fore.GREEN, 'Received', 'http://127.0.0.1/path2 231 200')
logger.info(Fore.YELLOW, 'Cache', 'Set<https://fuck.com/path1:asdjla:JSON>')
logger.info(Fore.BLUE, 'Storage', 'Get<https://fuck.com/path1:asdjla:HTML>')
logger.info(Fore.CYAN, 'Parsed', 'Item<Post[15]>')
logger.error('Cache', 'Set<https://fuck.com/path1:JSON>')
logger.error('Storage', 'Get<https://fuck.com/path1::HTML>')
logger.error('Parse', 'Item<Post[0]>')
"""
import logging

import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)


class Logger:
    def __init__(self, name, level=logging.DEBUG):
        logging.basicConfig(format='%(asctime)s %(message)-10s ',
                            datefmt='%Y/%m/%d %H:%M:%S')

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

    def info(self, color, type, message):
        self.logger.info(color + '[%-8s] %-2s %s' % (type, 'OK', message) + Style.RESET_ALL)

    def error(self, type, message):
        self.logger.error(Fore.RED + '[%-8s] %-4s %s' % (type, 'FAIL', message) + Style.RESET_ALL)


logger = Logger(__name__)
