"""
Message formatting utilities.
This module contains the MessageFormatter class that handles
consistent formatting of numbers, rates, and amounts throughout the bot.
"""


class MessageFormatter:
    """Class for formatting messages"""
    
    @staticmethod
    def format_rate(rate: float) -> str:
        """Format exchange rate for display"""
        if rate >= 1:
            return f"{rate:,.2f}"
        else:
            return f"{rate:.4f}"
    
    @staticmethod
    def format_amount(amount: float) -> str:
        """Format amount for display"""
        if amount >= 1:
            return f"{amount:,.2f}"
        else:
            return f"{amount:.4f}"
    
    @staticmethod
    def format_exchange_rate(rate: float) -> str:
        """Format exchange rate for conversion display"""
        if rate >= 1:
            return f"{rate:,.4f}"
        else:
            return f"{rate:.6f}"
    
    @staticmethod
    def format_percentage(percentage: float) -> str:
        """Format percentage change"""
        return f"{percentage:+.2f}%"
