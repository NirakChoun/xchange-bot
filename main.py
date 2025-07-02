"""Entry point for XChange Bot"""

import os
import logging
from dotenv import load_dotenv

from src.bot.xchange_bot import XChangeBot

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def main():
    """Main function to run the bot"""
    bot_token = os.getenv("TELEGRAM_BOT_API")
    if not bot_token:
        logger.error("Error: TELEGRAM_BOT_API not found in environment variables")
        exit(1)
    
    bot = XChangeBot(bot_token)
    bot.run()


if __name__ == '__main__':
    main()
