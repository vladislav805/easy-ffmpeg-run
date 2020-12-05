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


def print_progressbar(done, total, prefix='', suffix='', decimals=1, length=100, fill='#', space=' ', print_end='\r'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character █ (Str)
        print_end   - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    done = min(done, total)
    percent = ("{0:." + str(decimals) + "f}").format(100 * (done / float(total)))
    filled_length = int(length * done // total)
    bar = Fore.LIGHTGREEN_EX + fill * filled_length + Fore.GREEN + space * (length - filled_length - 1) + Style.RESET_ALL
    print(f'\r{prefix} [{bar}] {percent}% {suffix}', end=print_end)

    # Print new line on complete
    if done >= total:
        print()
