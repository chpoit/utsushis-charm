class MissingTranslationError(Exception):
    def __init__(self, lang) -> None:
        super().__init__(
            f'The language "{lang}" has not gotten a translation yet, feel free to submit one.'
        )
