from plugins.plugin import Plugin


class Size(Plugin):
    _size = None
    _resolution = None

    def __init__(self, args):
        super(Size, self).__init__(args)

        self._size = args.size

    @staticmethod
    def _parse_dimen(n: str):
        return n.isdigit() or n == '@'

    def _parse(self):
        sizes = self._size.split('x')

        if len(sizes) != 2:
            raise ValueError('Invalid format for --size. Numbers must be separated by x')

        width = self._parse_dimen(sizes[0])
        height = self._parse_dimen(sizes[1])

        if width and height:
            return sizes[0], sizes[1]

        raise ValueError('Invalid values for --size. Both parts must be int (one dimen may be "@" for auto)')

    def validate(self) -> bool:
        try:
            self._parse()
            return True
        except ValueError:
            return False

    def apply_plugin(self, probe):

        self._resolution = []

    def _get_size(self):
        width, height = self._parse()

        if width == '@':
            return

    def to_string(self) -> list:
        return ['-s', *self._resolution]
