from plugins.plugin import Plugin


class Speed(Plugin):
    factor = 1

    schema = ''

    def __init__(self, args):
        super().__init__(args)

        factor = args.speed

        self.factor = factor

    def is_valid(self) -> bool:
        if self.factor <= 0:
            raise ValueError('--speed must be greater then 0')
        return True

    def to_string(self) -> list:
        video_factor = 1 / self.factor
        audio_factor = float(self.factor)

        return [
            '-filter_complex', '[0:v]setpts={0}*PTS[v];[0:a]atempo={1}[a]'.format(video_factor, audio_factor),
            '-map', '[v]',
            '-map', '[a]'
        ]
