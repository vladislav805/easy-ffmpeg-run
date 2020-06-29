from plugins.plugin import Plugin


class StartFrom(Plugin):
    time = None

    def __init__(self, args):
        super().__init__(args)
        self.time = args.start

    def to_string(self) -> list:
        return ['-ss', self.time]
