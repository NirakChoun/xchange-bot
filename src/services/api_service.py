"""
API service module for handling external API calls.
This module contains the APIService class that handles all
interactions with the currency exchange rate API.
"""

import requests
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class APIService:
    """Service class for handling API calls"""
    
    BASE_URL = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies"
    
    @staticmethod
    async def get_current_rates() -> Optional[Dict]:
        """Get current USD exchange rates"""
        try:
            response = requests.get(f"{APIService.BASE_URL}/usd.json")
            if response.status_code == 200:
                return response.json()
            logger.warning(f"API returned status code: {response.status_code}")
            return None
        except requests.RequestException as e:
            logger.error(f"Error fetching current rates: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching current rates: {e}")
            return None
    
    @staticmethod
    async def get_historical_rates(date: str) -> Optional[Dict]:
        """Get historical USD exchange rates for a specific date"""
        try:
            url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date}/v1/currencies/usd.json"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            logger.warning(f"Historical API returned status code: {response.status_code} for date: {date}")
            return None
        except requests.RequestException as e:
            logger.error(f"Error fetching historical rates for {date}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching historical rates for {date}: {e}")
            return None
