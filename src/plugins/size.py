from plugins.plugin import Plugin


class Size(Plugin):
    size = None

    def __init__(self, args):
        super(Size, self).__init__(args)

        self.size = args.size

    def is_valid(self) -> bool:
        sizes = self.size.split('x')

        if len(sizes) != 2:
            raise ValueError('Invalid format for --size. Numbers must be separated by x')

        return sizes[0].isdigit() and sizes[1].isdigit()

    def to_string(self) -> list:
        return ['-s', self.size]
