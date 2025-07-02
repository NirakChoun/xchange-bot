"""Keyboard builder utility for creating inline keyboards"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class KeyboardBuilder:
    """Class for building inline keyboards"""
    
    @staticmethod
    def get_main_menu_keyboard() -> InlineKeyboardMarkup:
        """Get the main menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("💱 Live Rates", callback_data="rates"),
                InlineKeyboardButton("🌍 Currencies", callback_data="currency")
            ],
            [
                InlineKeyboardButton("📊 Trends", callback_data="trends"),
                InlineKeyboardButton("🔄 Convert", callback_data="convert_help")
            ],
            [
                InlineKeyboardButton("ℹ️ Help", callback_data="help")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
        """Get back to main menu keyboard"""
        keyboard = [[InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]]
        return InlineKeyboardMarkup(keyboard)
