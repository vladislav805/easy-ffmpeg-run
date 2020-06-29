from plugins.plugin import Plugin


class Pattern(Plugin):
    type = None

    def __init__(self, args):
        super(Pattern, self).__init__(args)

        self.type = 'glob'

    def is_valid(self) -> bool:
        return True

    def to_string(self) -> list:
        return ['-pattern_type', self.type]
