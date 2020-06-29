from argparse import ArgumentParser

from plugins.pattern import Pattern
from plugins.size import Size
from plugins.speed import Speed
from config import Config


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file or '%screen' for grab x11", required=True)
    parser.add_argument("-o", "--output", help="Output file", required=True)
    parser.add_argument("--pattern")
    parser.add_argument("--speed", type=float)
    parser.add_argument("--start")
    parser.add_argument("--duration")
    parser.add_argument("--end")
    parser.add_argument("--size")
    parser.add_argument("--scale")

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
            runner.add_plugin(plugins[key](args))

    runner.run()

