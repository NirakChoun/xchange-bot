"""Main XChange Bot class and handlers"""

import logging
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

from ..data.currency_data import CurrencyData
from ..services.api_service import APIService
from ..utils.formatter import MessageFormatter
from ..utils.keyboard_builder import KeyboardBuilder

# Configure logging
logger = logging.getLogger(__name__)


class XChangeBot:
    """Main bot class for XChange currency bot"""
    
    def __init__(self, token: str):
        self.app = ApplicationBuilder().token(token).build()
        self.api_service = APIService()
        self.formatter = MessageFormatter()
        self.keyboard_builder = KeyboardBuilder()
        self.setup_handlers()

    # Event Handlers
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle inline keyboard button presses"""
        query = update.callback_query
        await query.answer()
        
        callback_handlers = {
            "rates": self.button_get_rates,
            "currency": self.button_get_currencies,
            "trends": self.button_get_trends,
            "convert_help": self.button_convert_help,
            "help": self.button_help,
            "main_menu": self.button_main_menu
        }
        
        handler = callback_handlers.get(query.data)
        if handler:
            await handler(update, context)
        else:
            logger.warning(f"Unknown callback data: {query.data}")

    # Button Handlers
    async def button_get_rates(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle rates button press"""
        query = update.callback_query
        
        try:
            data = await self.api_service.get_current_rates()
            if not data:
                await query.edit_message_text(
                    "❌ Sorry, I couldn't fetch the latest rates. Please try again later."
                )
                return
            
            message = self._build_rates_message(data)
            keyboard = self.keyboard_builder.get_back_to_menu_keyboard()
            
            await query.edit_message_text(
                message, 
                parse_mode='Markdown', 
                reply_markup=keyboard
            )
            
        except Exception as e:
            logger.error(f"Error in button_get_rates: {e}")
            await query.edit_message_text(
                "❌ An error occurred while fetching rates. Please try again later."
            )

    async def button_get_currencies(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle currency list button press"""
        query = update.callback_query
        
        message = self._build_currencies_message()
        keyboard = self.keyboard_builder.get_back_to_menu_keyboard()
        
        await query.edit_message_text(
            message, 
            parse_mode='Markdown', 
            reply_markup=keyboard
        )

    async def button_get_trends(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle trends button press"""
        query = update.callback_query
        
        try:
            message = await self._build_trends_message()
            keyboard = self.keyboard_builder.get_back_to_menu_keyboard()
            
            await query.edit_message_text(
                message, 
                parse_mode='Markdown', 
                reply_markup=keyboard
            )
            
        except Exception as e:
            logger.error(f"Error in button_get_trends: {e}")
            await query.edit_message_text(
                "❌ An error occurred while fetching trend data. Please try again later."
            )

    async def button_convert_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle convert help button press"""
        query = update.callback_query
        
        message = self._build_convert_help_message()
        keyboard = self.keyboard_builder.get_back_to_menu_keyboard()
        
        await query.edit_message_text(
            message, 
            parse_mode='Markdown', 
            reply_markup=keyboard
        )

    async def button_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle help button press"""
        query = update.callback_query
        
        message = self._build_help_message()
        keyboard = self.keyboard_builder.get_back_to_menu_keyboard()
        
        await query.edit_message_text(
            message, 
            parse_mode='Markdown', 
            reply_markup=keyboard
        )

    async def button_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle main menu button press"""
        query = update.callback_query
        
        message = self._build_welcome_message(query.from_user.first_name)
        keyboard = self.keyboard_builder.get_main_menu_keyboard()
        
        await query.edit_message_text(
            message, 
            parse_mode='Markdown', 
            reply_markup=keyboard
        )

    # Command Handlers
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command"""
        message = self._build_welcome_message(update.effective_user.first_name)
        keyboard = self.keyboard_builder.get_main_menu_keyboard()
        
        await update.message.reply_text(
            message, 
            parse_mode='Markdown', 
            reply_markup=keyboard
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command"""
        message = self._build_help_message()
        keyboard = self.keyboard_builder.get_back_to_menu_keyboard()
        
        await update.message.reply_text(
            message, 
            parse_mode='Markdown', 
            reply_markup=keyboard
        )

    async def get_currencies(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /currency command - show supported currencies"""
        message = self._build_currencies_message()
        await update.message.reply_text(message, parse_mode='Markdown')

    async def get_rates(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /rates command - show live exchange rates"""
        try:
            data = await self.api_service.get_current_rates()
            if not data:
                await update.message.reply_text(
                    "❌ Sorry, I couldn't fetch the latest rates. Please try again later."
                )
                return
            
            message = self._build_rates_message(data)
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in get_rates: {e}")
            await update.message.reply_text(
                "❌ An error occurred while fetching rates. Please try again later."
            )

    async def get_trends(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /trends command - show currency trends"""
        try:
            message = await self._build_trends_message()
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in get_trends: {e}")
            await update.message.reply_text(
                "❌ An error occurred while fetching trend data. Please try again later."
            )

    async def convert(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /convert command - convert between currencies"""
        try:
            args = context.args
            
            if not args:
                message = self._build_convert_help_message()
                await update.message.reply_text(message, parse_mode='Markdown')
                return
            
            # Validate arguments
            validation_result = self._validate_convert_args(args)
            if validation_result['error']:
                await update.message.reply_text(
                    validation_result['message'], 
                    parse_mode='Markdown'
                )
                return
            
            # Perform conversion
            conversion_result = await self._perform_conversion(
                validation_result['amount'],
                validation_result['from_currency'],
                validation_result['to_currency']
            )
            
            if conversion_result['error']:
                await update.message.reply_text(conversion_result['message'])
                return
            
            message = self._build_conversion_result_message(conversion_result)
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in convert: {e}")
            await update.message.reply_text(
                "❌ An error occurred during conversion. Please try again later."
            )

    # Helper Methods
    def _get_flag_emoji(self, currency_code: str) -> str:
        """Get flag emoji for currency code"""
        return CurrencyData.get_flag_emoji(currency_code)
    
    def _get_currency_symbol(self, currency_code: str) -> str:
        """Get currency symbol for currency code"""
        return CurrencyData.get_currency_symbol(currency_code)
    
    def _build_welcome_message(self, first_name: str) -> str:
        """Build welcome message"""
        return f"""🔄 **Welcome to XChange Bot, {first_name}!**

Your personal currency exchange assistant. Here's what I can do:

💱 **View live exchange rates** for 20+ currencies
🔀 **Convert currencies** instantly
📊 **Track currency trends**
📋 **List supported currencies**

💡 **How to use:**
• Type commands (like /rates, /convert)
• Or use the keyboard buttons below

Use /help to see all available commands.

Ready to start exchanging? 🚀"""
    
    def _build_help_message(self) -> str:
        """Build help message"""
        return """🔄 **XChange Bot Help**

**Available Commands:**
• `/start` - Welcome message and main menu
• `/rates` - View live exchange rates (USD base)
• `/currency` - List all supported currencies
• `/trends` - View 7-day currency trends
• `/convert <amount> <from> <to>` - Convert currencies
• `/help` - Show this help message

**Convert Examples:**
• `/convert 100 USD EUR`
• `/convert 50.5 EUR JPY`
• `/convert 1000 KHR USD`

**Supported Features:**
💱 Live exchange rates for 19 currencies
📊 7-day trend analysis
🔄 Instant currency conversion
🌍 Support for major world currencies

**Need help?** Just use the buttons below or type the commands!"""
    
    def _build_currencies_message(self) -> str:
        """Build currencies list message"""
        message = "🌍 **Supported Currencies:**\n\n"
        
        for code in CurrencyData.get_currencies():
            flag_emoji = self._get_flag_emoji(code)
            currency_name = CurrencyData.get_currency_name(code)
            message += f"{flag_emoji} **{code.upper()}** - {currency_name}\n"
        
        return message
    
    def _build_rates_message(self, data: Dict) -> str:
        """Build exchange rates message"""
        usd_rates = data.get('usd', {})
        date = data.get('date', 'Unknown')
        
        message = f"💱 **Live Exchange Rates (USD Base)**\n"
        message += f"📅 Updated: {date}\n\n"
        
        # Show USD first
        flag_emoji = self._get_flag_emoji('usd')
        message += f"{flag_emoji} **USD** = $1.00 (Base)\n"
        
        # Show other currencies
        for code in CurrencyData.get_currencies():
            if code != 'usd' and code in usd_rates:
                rate = usd_rates[code]
                flag_emoji = self._get_flag_emoji(code)
                formatted_rate = self.formatter.format_rate(rate)
                currency_symbol = self._get_currency_symbol(code)
                message += f"{flag_emoji} **{code.upper()}** = {currency_symbol}{formatted_rate}\n"
        
        message += f"\n💡 *1 USD equals the amounts shown above*"
        return message
    
    async def _build_trends_message(self) -> str:
        """Build currency trends message"""
        days_to_analyze = 7
        
        # Get current rates
        current_data = await self.api_service.get_current_rates()
        if not current_data:
            return "❌ Sorry, I couldn't fetch trend data. Please try again later."
        
        current_rates = current_data.get('usd', {})
        current_date = current_data.get('date', 'Unknown')
        
        # Calculate past date
        try:
            current_datetime = datetime.strptime(current_date, '%Y-%m-%d')
            past_datetime = current_datetime - timedelta(days=days_to_analyze)
            past_date = past_datetime.strftime('%Y-%m-%d')
        except:
            past_date = "2025-06-23"
        
        # Get past rates
        past_data = await self.api_service.get_historical_rates(past_date)
        
        message = f"📊 **Currency Trends (Last {days_to_analyze} Days)**\n\n"
        
        if past_data and past_data.get('usd'):
            past_rates = past_data.get('usd', {})
            message += f"📅 From: {past_date} → {current_date}\n\n"
            
            for code in CurrencyData.get_currencies()[:10]:  # Limit to first 10
                if code != 'usd' and code in current_rates and code in past_rates:
                    current_rate = current_rates[code]
                    past_rate = past_rates[code]
                    change_percent = ((current_rate - past_rate) / past_rate) * 100
                    
                    # Determine trend
                    if change_percent > 0.5:
                        trend_emoji = "📈"
                        trend_text = "Strong"
                    elif change_percent < -0.5:
                        trend_emoji = "📉"
                        trend_text = "Weak"
                    else:
                        trend_emoji = "📊"
                        trend_text = "Stable"
                    
                    flag_emoji = self._get_flag_emoji(code)
                    currency_symbol = self._get_currency_symbol(code)
                    
                    message += f"{flag_emoji} **{code.upper()}** {trend_emoji}\n"
                    message += f"   {currency_symbol}{current_rate:.4f} ({change_percent:+.2f}%) - {trend_text}\n\n"
            
            message += "💡 *Positive % = Currency strengthened vs USD*\n"
            message += "💡 *Negative % = Currency weakened vs USD*"
        else:
            message += "❌ Historical data temporarily unavailable."
        
        return message
    
    def _build_convert_help_message(self) -> str:
        """Build convert help message"""
        currency_list = ", ".join([code.upper() for code in CurrencyData.get_currencies()])
        
        return f"""🔄 **Currency Converter**

**Usage:** `/convert <amount> <from> <to>`

**Examples:**
• `/convert 100 USD EUR` - Convert 100 USD to EUR
• `/convert 50 EUR JPY` - Convert 50 EUR to JPY
• `/convert 1000 KHR USD` - Convert 1000 KHR to USD

**Supported currencies:**
{currency_list}

💡 *Amount can be decimal (e.g., 100.50)*"""
    
    def _validate_convert_args(self, args: List[str]) -> Dict:
        """Validate conversion arguments"""
        if len(args) != 3:
            return {
                'error': True,
                'message': "❌ **Invalid format!**\n\n"
                          "Use: `/convert <amount> <from_currency> <to_currency>`\n"
                          "Example: `/convert 100 USD EUR`"
            }
        
        # Extract and validate amount
        try:
            amount = float(args[0])
        except ValueError:
            return {
                'error': True,
                'message': "❌ **Invalid amount!**\n\n"
                          "Please enter a valid number.\n"
                          "Example: `/convert 100 USD EUR`"
            }
        
        from_currency = args[1].lower()
        to_currency = args[2].lower()
        
        # Validate currencies
        if not CurrencyData.is_supported_currency(from_currency):
            return {
                'error': True,
                'message': f"❌ **'{from_currency.upper()}' is not supported!**\n\n"
                          f"Use `/convert` to see supported currencies."
            }
        
        if not CurrencyData.is_supported_currency(to_currency):
            return {
                'error': True,
                'message': f"❌ **'{to_currency.upper()}' is not supported!**\n\n"
                          f"Use `/convert` to see supported currencies."
            }
        
        return {
            'error': False,
            'amount': amount,
            'from_currency': from_currency,
            'to_currency': to_currency
        }
    
    async def _perform_conversion(self, amount: float, from_currency: str, to_currency: str) -> Dict:
        """Perform currency conversion"""
        # Check if same currency
        if from_currency == to_currency:
            symbol = self._get_currency_symbol(from_currency)
            return {
                'error': False,
                'is_same_currency': True,
                'amount': amount,
                'symbol': symbol,
                'currency': from_currency.upper()
            }
        
        # Get exchange rates
        data = await self.api_service.get_current_rates()
        if not data:
            return {
                'error': True,
                'message': "❌ Sorry, I couldn't fetch exchange rates. Please try again later."
            }
        
        usd_rates = data.get('usd', {})
        date = data.get('date', 'Unknown')
        
        # Calculate conversion
        if from_currency == 'usd':
            if to_currency not in usd_rates:
                return {'error': True, 'message': "❌ Exchange rate not available for this currency pair."}
            converted_amount = amount * usd_rates[to_currency]
        elif to_currency == 'usd':
            if from_currency not in usd_rates:
                return {'error': True, 'message': "❌ Exchange rate not available for this currency pair."}
            converted_amount = amount / usd_rates[from_currency]
        else:
            if from_currency not in usd_rates or to_currency not in usd_rates:
                return {'error': True, 'message': "❌ Exchange rate not available for this currency pair."}
            usd_amount = amount / usd_rates[from_currency]
            converted_amount = usd_amount * usd_rates[to_currency]
        
        return {
            'error': False,
            'is_same_currency': False,
            'amount': amount,
            'converted_amount': converted_amount,
            'from_currency': from_currency,
            'to_currency': to_currency,
            'date': date
        }
    
    def _build_conversion_result_message(self, result: Dict) -> str:
        """Build conversion result message"""
        if result.get('is_same_currency'):
            symbol = result['symbol']
            amount = result['amount']
            currency = result['currency']
            return f"💡 **Same currency!**\n\n" \
                   f"{symbol}{amount:,.2f} {currency} = {symbol}{amount:,.2f} {currency}"
        
        amount = result['amount']
        converted_amount = result['converted_amount']
        from_currency = result['from_currency']
        to_currency = result['to_currency']
        date = result['date']
        
        from_flag = self._get_flag_emoji(from_currency)
        to_flag = self._get_flag_emoji(to_currency)
        from_symbol = self._get_currency_symbol(from_currency)
        to_symbol = self._get_currency_symbol(to_currency)
        
        formatted_amount = self.formatter.format_amount(amount)
        formatted_converted = self.formatter.format_amount(converted_amount)
        
        exchange_rate = converted_amount / amount
        formatted_rate = self.formatter.format_exchange_rate(exchange_rate)
        
        return f"""💱 **Currency Conversion**

{from_flag} **{from_symbol}{formatted_amount} {from_currency.upper()}** 
↓
{to_flag} **{to_symbol}{formatted_converted} {to_currency.upper()}**

📊 **Exchange Rate:** 1 {from_currency.upper()} = {formatted_rate} {to_currency.upper()}
📅 **Updated:** {date}

💡 *Rates are live and may fluctuate*"""

    def setup_handlers(self) -> None:
        """Setup all command and callback handlers"""
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("currency", self.get_currencies))
        self.app.add_handler(CommandHandler("rates", self.get_rates))
        self.app.add_handler(CommandHandler("trends", self.get_trends))
        self.app.add_handler(CommandHandler("convert", self.convert))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CallbackQueryHandler(self.button_callback))

    def run(self) -> None:
        """Start the bot"""
        logger.info("Bot is starting...")
        logger.info("Bot started successfully!")
        self.app.run_polling()
