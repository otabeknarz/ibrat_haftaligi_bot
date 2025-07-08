from aiogram.types import Message

from aiogram.filters import Filter


class TextEqualsFilter(Filter):
    def __init__(self, text: str) -> None:
        self.text = text

    async def __call__(self, message: Message) -> bool:
        return message.text == self.text
