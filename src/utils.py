from os.path import isdir, exists
from enum import Enum
from colorama import Fore, Back, Style

import re
import colorama

colorama.init()


def parse_int(s) -> int:
    return int(s) if s is not None and s.isdigit() else 0


def parse_time(time) -> int:
    res = re.findall(r'((\d{2}):)?(\d{2}):(\d{2})(\.(\d{2}))?', time, flags=re.IGNORECASE)

    if len(res) == 0:
        return 0

    [res] = res

    hours = parse_int(res[1])
    minutes = parse_int(res[2])
    seconds = parse_int(res[3])
    mills = parse_int(res[5])

    time = hours * 3600 + minutes * 60 + seconds

    return time if mills == 0 else time + (mills / (10 ** len(res[5])))


class Exist(Enum):
    NOT_EXISTS = 0
    EXISTS = 1
    DIR = 2


def check_file(path) -> Exist:
    if exists(path):
        return Exist.DIR if isdir(path) else Exist.EXISTS
    return Exist.NOT_EXISTS


def print_error(message: str, exit_code: int = 1) -> None:
    print('{0}Error: {1}{2}'.format(Fore.RED, message, Style.RESET_ALL))
    exit(exit_code)


def print_confirm(message) -> bool:
    ans = None
    while ans not in ('y', 'n'):
        ans = input('{0}{1}{2}'.format(Fore.YELLOW, message, Style.RESET_ALL))

    return ans == 'y'
