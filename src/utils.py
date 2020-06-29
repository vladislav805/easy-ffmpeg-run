import re


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
