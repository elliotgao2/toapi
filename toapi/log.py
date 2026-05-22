import logging

import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)


class Logger:
    def __init__(self, name: str, level: int = logging.DEBUG) -> None:
        logging.basicConfig(
            format="%(asctime)s %(message)-10s ",
            datefmt="%Y/%m/%d %H:%M:%S",
        )
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

    def info(self, color: str, kind: str, message: str) -> None:
        self.logger.info(f"{color}[{kind:<8}] OK {message}{Style.RESET_ALL}")

    def error(self, kind: str, message: str) -> None:
        self.logger.error(f"{Fore.RED}[{kind:<8}] FAIL {message}{Style.RESET_ALL}")


logger = Logger(__name__)
