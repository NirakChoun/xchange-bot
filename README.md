# 💱 XChange Bot

A modern, feature-rich Telegram bot for real-time currency exchange rates and conversions. Built with Python and the python-telegram-bot library, XChange Bot provides live exchange rates, currency trends, and instant conversions for 19+ major world currencies.

**🤖 Try the bot: [t.me/BotXChangeBot](https://t.me/BotXChangeBot)**

## ✨ Features

- **💱 Live Exchange Rates**: Get real-time USD-based exchange rates for 19+ currencies
- **🔄 Currency Conversion**: Convert between any supported currency pairs instantly  
- **📊 Trend Analysis**: View 7-day currency trends with percentage changes
- **🌍 Multi-Currency Support**: Supports major currencies from Asia, Europe, Americas, and Oceania
- **🎯 Interactive Interface**: Easy-to-use inline keyboard buttons and command interface
- **📱 Mobile-Friendly**: Optimized for mobile Telegram clients

## 🌐 Supported Currencies

- **Asian**: KHR (Cambodia), CNY (China), JPY (Japan), KRW (South Korea), THB (Thailand), VND (Vietnam), MMK (Myanmar), SGD (Singapore), MYR (Malaysia), IDR (Indonesia), INR (India), LAK (Laos)
- **Western**: USD (USA), EUR (Europe), GBP (UK), CHF (Switzerland), AUD (Australia), NZD (New Zealand) 
- **Other**: BND (Brunei)

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- A Telegram Bot Token (from [@BotFather](https://t.me/botfather))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/NirakChoun/xchange-bot.git
   cd xchange-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   TELEGRAM_BOT_API=your_telegram_bot_token_here
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

## 🏗️ Project Structure

```
xchange-bot/
├── src/
│   ├── bot/
│   │   ├── __init__.py
│   │   └── xchange_bot.py          # Main bot class and handlers
│   ├── data/
│   │   ├── __init__.py
│   │   └── currency_data.py        # Currency constants and helpers
│   ├── services/
│   │   ├── __init__.py
│   │   └── api_service.py          # API service for exchange rates
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── formatter.py            # Message formatting utilities
│   │   └── keyboard_builder.py     # Inline keyboard builders
│   └── handlers/
│       └── __init__.py             # Future handler extensions
├── main.py                         # Application entry point
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Project configuration
└── README.md                       # This file
```

## 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message and main menu |
| `/rates` | View live exchange rates (USD base) |
| `/currency` | List all supported currencies |
| `/trends` | View 7-day currency trends |
| `/convert <amount> <from> <to>` | Convert between currencies |
| `/help` | Show help information |

### Usage Examples

```
/convert 100 USD EUR
/convert 50.5 EUR JPY  
/convert 1000 KHR USD
```

## 🔧 Technical Details

### Architecture

The bot follows a modular architecture with clear separation of concerns:

- **`XChangeBot`**: Main bot class handling all commands and callbacks
- **`CurrencyData`**: Centralized currency information and constants
- **`APIService`**: Handles all external API calls for exchange rates
- **`MessageFormatter`**: Consistent formatting for all bot responses
- **`KeyboardBuilder`**: Creates inline keyboards for interactive UI

### Data Source

- **Current Rates**: Uses the free [Currency API](https://github.com/fawazahmed0/currency-api) by @fawazahmed0
- **Historical Data**: Fetches historical rates for trend analysis
- **Update Frequency**: Real-time data fetched on each request

### Key Features Implementation

- **Async/Await**: Full asynchronous support for better performance
- **Error Handling**: Comprehensive error handling and user-friendly messages  
- **Logging**: Structured logging for monitoring and debugging
- **Modular Design**: Easy to extend and maintain codebase

## 🛠️ Development

### Code Style

The project follows Python best practices:
- Type hints for better code documentation
- Docstrings for all classes and methods
- Modular design with single responsibility principle
- Async/await for I/O operations

### Dependencies

- `python-telegram-bot>=22.2`: Telegram Bot API wrapper
- `requests>=2.32.4`: HTTP requests for API calls
- `python-dotenv>=1.1.1`: Environment variable management
- `aiohttp>=3.12.13`: Async HTTP client support

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📞 Support

If you encounter any issues or have questions:
1. Check the existing issues on GitHub
2. Create a new issue with detailed information
3. Include logs and steps to reproduce any bugs

---

**Made with ❤️ for the Telegram community**