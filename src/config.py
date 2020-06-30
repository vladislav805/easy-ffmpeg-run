import subprocess
import re
import sys

from plugins.pattern import Pattern
from plugins.plugin import Plugin
from plugins.speed import Speed
from utils import parse_time, check_file, Exist, print_error, print_confirm


class Config:
    input_filename = None
    output_filename = None

    plugins = []

    def __init__(self, input_file: str, output_file: str):
        self.input_filename = input_file
        self.output_filename = output_file

        self._check_files()

    def _check_files(self):
        input_status = check_file(self.input_filename)

        is_pattern = self.get_plugin(Pattern)

        if is_pattern is None:
            if input_status == Exist.NOT_EXISTS:
                print_error('input file "{0}" not exists'.format(self.input_filename))
            if input_status == Exist.DIR:
                print_error('input file "{0}" is directory'.format(self.input_filename))

        output_status = check_file(self.output_filename)

        if output_status is Exist.DIR:
            print_error('output file "{0}" is directory'.format(self.output_filename))

        if output_status is Exist.EXISTS:
            ans = print_confirm('output file "{0}" already exists. Overwrite?'.format(self.output_filename))
            if ans is False:
                print('Cancelled')
                exit(0)

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
                match = re.search(r', ([\d.]+) tbr', line, flags=re.IGNORECASE)
                if match:
                    self._frames = float(match[1])

            if line.startswith('frame'):
                status = re.search(
                    r'frame=([\d\s]+).*size=([\d\skmB]+).*time=([\d:.]+).*speed=([\s\d.]+)x',
                    line,
                    flags=re.IGNORECASE
                )

                frame = int(status[1].strip())
                size = status[2].strip()
                time = parse_time(status[3])
                speed = float(status[4].strip())

                sys.stdout.write('Processing... {0}%, speed {1}x\r'.format(
                    self._get_percent(frame, size, time, speed),
                    speed
                ))
