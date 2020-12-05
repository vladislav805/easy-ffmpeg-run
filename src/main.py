from argparse import ArgumentParser

from plugins.pattern import Pattern
from plugins.size import Size
from plugins.speed import Speed
from config import Config


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file or '%screen' for grab x11", required=True)
    parser.add_argument("-o", "--output", help="Output file", required=True)
    parser.add_argument("--pattern", help="Pattern (glob) for grab multiple files")
    parser.add_argument("--speed", type=float, help="Speed up/down; value <1 = slower, >1 = faster")
    # parser.add_argument("--start", help="Timecode of start position")
    # parser.add_argument("--duration", help="Timecode of duration of fragment regarding start")
    # parser.add_argument("--end", help="Timecode of end position")
    parser.add_argument("--size", help="Resize video to specified size in format WxH (W or H may be @ for aut value)")
    # parser.add_argument("--scale", help="Resize video by scale factor (e.g. 1920x1080, with --scale 0.5 = 960x540)")

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    runner = Config(args.input, args.output)

    plugins = {
        'speed': Speed,
        'size': Size,
        'pattern': Pattern,
    }

    for key in plugins.keys():
        if getattr(args, key) is not None:
            plugin = plugins[key](args)
            runner.add_plugin(plugin)

    runner.run()

