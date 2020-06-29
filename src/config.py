import subprocess
import re
import sys

from plugins.plugin import Plugin
from plugins.speed import Speed
from utils import parse_time


class Config:
    input_filename = None
    output_filename = None

    plugins = []

    def __init__(self, input_file: str, output_file: str):
        self.input_filename = input_file
        self.output_filename = output_file

    def add_plugin(self, plugin: Plugin):
        self.plugins.append(plugin)
        return self

    def get_plugin(self, plugin_type):
        for plugin in self.plugins:
            if isinstance(plugin, plugin_type):
                return plugin

        return None

    def _get_source(self) -> list:
        if self.input_filename == '%screen':
            return ['-f', 'x11grab']

        return ['-i', self.input_filename]

    def _get_args(self) -> list:
        args = []

        for plugin in self.plugins:
            args.append(plugin.to_string())

        return args

    def _get_command(self) -> list:
        src = self._get_source()
        args = self._get_args()

        return [src, *args, [self.output_filename]]

    def _get_percent(self, frame: int, size: str, time: int, speed: float):
        duration = self._duration
        frames = self._frames

        ch_speed = self.get_plugin(Speed)

        if ch_speed is not None:
            duration = duration / ch_speed.factor
            frames = frames / ch_speed.factor

        return int(time * 100 / duration)

    _frames = None
    _duration = None

    def run(self):
        cmd_args = [item for sublist in self._get_command() for item in sublist]

        proc = subprocess.Popen(
            ['ffmpeg', '-hide_banner', '-y', *cmd_args],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        while True:
            line = proc.stdout.readline()

            if not line:
                break

            line = str(line.rstrip())

            if self._duration is None:
                match = re.search(r'Duration: ([^,]+),', line)
                if match:
                    self._duration = parse_time(match[0])

            if self._frames is None:
                match = re.search(r', (\d+) tbr', line, flags=re.IGNORECASE)
                if match:
                    self._frames = int(match[1])

            if line.startswith('frame'):
                status = re.search(
                    r'frame=([\d\s]+).*size=([\d\skmB]+).*time=([\d:.]+).*speed=([\s\d.]+)x',
                    line,
                    flags=re.IGNORECASE
                )

                frame = int(status[1])
                size = status[2]
                time = parse_time(status[3])
                speed = float(status[4])

                sys.stdout.write('Processing... {0}%, speed {1}x\r'.format(
                    self._get_percent(frame, size, time, speed),
                    speed
                ))
