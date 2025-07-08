from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
)


class Buttons:
    def __init__(self):
        self.remove_keyboard = ReplyKeyboardRemove()

    @staticmethod
    def main_keyboard():
        return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📊 Natijalarim")]])


class InlineButtons:
    def __init__(self):
        self.invitation_buttons = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="📩 Taklif posti", callback_data="invitation")
                ]
            ]
        )

    @staticmethod
    def get_participate_button(token):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🚀 Qatnashish", url=f"https://t.me/ibratmarafon_bot?start={token}")
                ]
            ]
        )

    @staticmethod
    def get_join_channel_buttons(channels: dict) -> InlineKeyboardMarkup:
        inline_buttons = [
            [InlineKeyboardButton(text=channel_name, url=channel_link)]
            for channel_id, (channel_name, channel_link) in channels.items()
        ]
        inline_buttons.append(
            [
                InlineKeyboardButton(
                    text="Ibrat Farzandlari Instagram", url="https://www.instagram.com/ibrat.farzandlari/",
                )
            ]
        )
        inline_buttons.append(
            [
                InlineKeyboardButton(
                    text="Obuna bo'ldim ✅", callback_data="joined"
                )
            ]
        )
        return InlineKeyboardMarkup(inline_keyboard=inline_buttons)
