import subprocess
import re

from utils import parse_time


class Probe:
    _path = None
    _duration = None
    _frames = None

    def __init__(self, path):
        self._path = path

        self._probe()

    def get_duration(self):
        return self._duration

    def get_frames(self):
        return self._frames

    def _probe(self) -> bool:
        proc = subprocess.Popen(
            ['ffprobe', self._path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )

        while True:
            line = proc.stdout.readline() or False

            if not line:
                break

            line = str(line.rstrip())

            if self._duration is None:
                match = re.search(r'Duration: ([^,]+),', line)
                if match:
                    self._duration = parse_time(match[0])

            if self._frames is None:
                match = re.search(r', ([\d.]+) tbr', line, flags=re.IGNORECASE)
                if match:
                    fps = float(match[1])
                    if self._duration is not None:
                        self._frames = fps * self._duration

        return self._duration is not None and self._frames is not None
