"""
Currency data constants and mappings.
This module contains all currency-related constants including
currency codes, names, symbols, and flag emojis.
"""


class CurrencyData:
    """Class to handle currency data and constants"""
    
    CURRENCIES = [
        'khr',  # Cambodia - Cambodian Riel
        'usd',  # USA - US Dollar
        'cny',  # China - Chinese Yuan Renminbi
        'jpy',  # Japan - Japanese Yen
        'krw',  # South Korea - South Korean Won
        'thb',  # Thailand - Thai Baht
        'vnd',  # Vietnam - Vietnamese Dong
        'mmk',  # Myanmar - Burmese Kyat
        'bnd',  # Brunei - Bruneian Dollar
        'lak',  # Laos - Lao Kip
        'sgd',  # Singapore - Singapore Dollar
        'myr',  # Malaysia - Malaysian Ringgit
        'idr',  # Indonesia - Indonesian Rupiah
        'aud',  # Australia - Australian Dollar
        'nzd',  # New Zealand - New Zealand Dollar
        'chf',  # Switzerland - Swiss Franc
        'eur',  # Europe - Euro
        'gbp',  # UK - British Pound
        'inr'   # India - Indian Rupee
    ]
    
    CURRENCY_NAMES = {
        'khr': 'Cambodian Riel',
        'usd': 'US Dollar',
        'cny': 'Chinese Yuan Renminbi',
        'jpy': 'Japanese Yen',
        'krw': 'South Korean Won',
        'thb': 'Thai Baht',
        'vnd': 'Vietnamese Dong',
        'mmk': 'Burmese Kyat',
        'bnd': 'Bruneian Dollar',
        'lak': 'Lao Kip',
        'sgd': 'Singapore Dollar',
        'myr': 'Malaysian Ringgit',
        'idr': 'Indonesian Rupiah',
        'aud': 'Australian Dollar',
        'nzd': 'New Zealand Dollar',
        'chf': 'Swiss Franc',
        'eur': 'Euro',
        'gbp': 'British Pound',
        'inr': 'Indian Rupee'
    }
    
    CURRENCY_SYMBOLS = {
        'khr': '៛',    # Cambodia Riel
        'usd': '$',    # US Dollar
        'cny': '¥',    # Chinese Yuan
        'jpy': '¥',    # Japanese Yen
        'krw': '₩',    # South Korean Won
        'thb': '฿',    # Thai Baht
        'vnd': '₫',    # Vietnamese Dong
        'mmk': 'K',    # Myanmar Kyat
        'bnd': 'B$',   # Brunei Dollar
        'lak': '₭',    # Lao Kip
        'sgd': 'S$',   # Singapore Dollar
        'myr': 'RM',   # Malaysian Ringgit
        'idr': 'Rp',   # Indonesian Rupiah
        'aud': 'A$',   # Australian Dollar
        'nzd': 'NZ$',  # New Zealand Dollar
        'chf': 'CHF',  # Swiss Franc
        'eur': '€',    # Euro
        'gbp': '£',    # British Pound
        'inr': '₹'     # Indian Rupee
    }
    
    FLAG_EMOJIS = {
        'khr': '🇰🇭',  # Cambodia
        'usd': '🇺🇸',  # USA
        'cny': '🇨🇳',  # China
        'jpy': '🇯🇵',  # Japan
        'krw': '🇰🇷',  # South Korea
        'thb': '🇹🇭',  # Thailand
        'vnd': '🇻🇳',  # Vietnam
        'mmk': '🇲🇲',  # Myanmar
        'bnd': '🇧🇳',  # Brunei
        'lak': '🇱🇦',  # Laos
        'sgd': '🇸🇬',  # Singapore
        'myr': '🇲🇾',  # Malaysia
        'idr': '🇮🇩',  # Indonesia
        'aud': '🇦🇺',  # Australia
        'nzd': '🇳🇿',  # New Zealand
        'chf': '🇨🇭',  # Switzerland
        'eur': '🇪🇺',  # Europe
        'gbp': '🇬🇧',  # UK
        'inr': '🇮🇳'   # India
    }
    
    @classmethod
    def get_currencies(cls) -> list:
        """Get list of all supported currency codes"""
        return cls.CURRENCIES.copy()
    
    @classmethod
    def get_flag_emoji(cls, currency_code: str) -> str:
        """Get flag emoji for currency code"""
        return cls.FLAG_EMOJIS.get(currency_code.lower(), '💱')
    
    @classmethod
    def get_currency_symbol(cls, currency_code: str) -> str:
        """Get currency symbol for currency code"""
        return cls.CURRENCY_SYMBOLS.get(currency_code.lower(), '$')
    
    @classmethod
    def get_currency_name(cls, currency_code: str) -> str:
        """Get full currency name for currency code"""
        return cls.CURRENCY_NAMES.get(currency_code.lower(), 'Unknown Currency')
    
    @classmethod
    def is_supported_currency(cls, currency_code: str) -> bool:
        """Check if currency code is supported"""
        return currency_code.lower() in cls.CURRENCIES
