import subprocess
import re

from plugins.pattern import Pattern
from plugins.plugin import Plugin
from plugins.speed import Speed
from probe import Probe
from utils import parse_time, check_file, Exist, print_error, print_confirm, print_progressbar


class Config:
    input_filename = None
    output_filename = None

    plugins = []

    def __init__(self, input_file: str, output_file: str):
        self.input_filename = input_file
        self.output_filename = output_file

    # Check status of input and output files
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
            ans = print_confirm('output file "{0}" already exists. Overwrite? '.format(self.output_filename))
            if ans is False:
                print('Cancelled')
                exit(0)

    def _check_plugins(self):
        try:
            for plugin in self.plugins:
                plugin.validate()
        except Exception as e:
            print_error(e.__str__(), 1)

    # Add plugin for processing video
    def add_plugin(self, plugin: Plugin):
        self.plugins.append(plugin)
        return self

    # Find plugin by type
    def get_plugin(self, plugin_type):
        for plugin in self.plugins:
            if isinstance(plugin, plugin_type):
                return plugin

        return None

    def _apply_plugins(self, probe):
        for plugin in self.plugins:
            plugin.apply_plugin(probe)

    # Make argument chunk with input source
    def _get_source(self) -> list:
        if self.input_filename == '%screen':
            return ['-f', 'x11grab']

        return ['-i', self.input_filename]

    # Make argument chunk with arguments of added plugins
    def _get_args(self) -> list:
        args = []

        for plugin in self.plugins:
            plugin_args = plugin.to_string()
            for arg in plugin_args:
                args.append(arg)

        return args

    # Make command line
    def _get_command(self) -> list:
        return [
            'ffmpeg', '-hide_banner', '-y',
            *self._get_source(),
            *self._get_args(),
            self.output_filename
        ]

    # Fix time while processing run, if changed speed
    def _get_fixed_time_on_run(self, time: int):
        ch_speed = self.get_plugin(Speed)

        if ch_speed is not None:
            time = time * ch_speed.factor

        return time

    _frames = None
    _duration = None

    def run(self):
        # Validate addedd plugins, if error ocurred, exit
        self._check_plugins()

        # Check input files
        self._check_files()

        # Get info about input file
        info = Probe(self.input_filename) if self.get_plugin(Pattern) is None else None

        self._apply_plugins(info)

        cmd = self._get_command()

        print(cmd)
        print_progressbar(6, info.get_duration())
        return None

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        while True:
            line = proc.stdout.readline()

            if not line:
                break

            line = str(line.rstrip())

            if line.startswith('frame'):
                status = re.search(
                    r'frame=([\d\s]+).*size=([\d\skmB]+).*time=([\d:.]+).*speed=([\s\d.]+)x',
                    line,
                    flags=re.IGNORECASE
                )

                time = self._get_fixed_time_on_run(parse_time(status[3]))
                speed = float(status[4].strip())

                print_progressbar(time, self._duration) # , suffix=f"(speed: {speed}x)")
        print()
