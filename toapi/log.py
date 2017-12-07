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

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.info(message)

    def error(self, type, message):
        self.logger.error(Fore.RED + '[%-8s] %-4s %s' % (type, 'FAIL', message) + Style.RESET_ALL)

    def critical(self, message):
        self.logger.info(message)

    def log(self, color, type, message):
        self.logger.info(color + '[%-8s] %-4s %s' % (type, 'OK', message) + Style.RESET_ALL)


logger = Logger(__name__)

# Usage
# logger.log(Fore.YELLOW, 'Request', 'https://fuck.com/path1 1231 200')
# logger.log(Fore.WHITE, 'Response', 'http://127.0.0.1/path2 231 200')
# logger.log(Fore.GREEN, 'Cache', 'Set<asdjla:JSON>')
# logger.log(Fore.BLUE, 'Storage', 'Get<asdjla:html>')
# logger.log(Fore.CYAN, 'Parse', 'Item<Post>[15]')
# logger.error('Cache', 'Set<asdjla:JSON>')
# logger.error('Storage', 'Get<asdjla:html>')
# logger.error('Parse', 'Item<Post>[0]')
