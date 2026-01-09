"""
Configuration module for Binance Futures Trading Bot
Handles API credentials and environment settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for bot settings"""
    
    # API Credentials
    API_KEY = os.getenv('BINANCE_API_KEY', '')
    API_SECRET = os.getenv('BINANCE_API_SECRET', '')
    
    # Environment
    USE_TESTNET = os.getenv('BINANCE_TESTNET', 'True').lower() == 'true'
    
    # API Endpoints
    TESTNET_BASE_URL = 'https://testnet.binancefuture.com'
    PRODUCTION_BASE_URL = 'https://fapi.binance.com'
    
    @classmethod
    def get_base_url(cls):
        """Get the appropriate base URL based on environment"""
        return cls.TESTNET_BASE_URL if cls.USE_TESTNET else cls.PRODUCTION_BASE_URL
    
    @classmethod
    def validate_credentials(cls):
        """Validate that API credentials are set"""
        if not cls.API_KEY or not cls.API_SECRET:
            raise ValueError(
                "API credentials not found. Please set BINANCE_API_KEY and "
                "BINANCE_API_SECRET in your .env file"
            )
        
        if cls.API_KEY == 'your_api_key_here':
            raise ValueError(
                "Please replace 'your_api_key_here' with your actual Binance API key"
            )
        
        return True
    
    @classmethod
    def get_environment_name(cls):
        """Get human-readable environment name"""
        return "TESTNET" if cls.USE_TESTNET else "PRODUCTION"


# Trading Parameters
class TradingConfig:
    """Trading-specific configuration"""
    
    # Order execution
    DEFAULT_RECV_WINDOW = 5000  # milliseconds
    
    # TWAP settings
    TWAP_MIN_ORDERS = 2
    TWAP_MAX_ORDERS = 100
    TWAP_MIN_DURATION = 1  # minutes
    TWAP_MAX_DURATION = 1440  # 24 hours
    
    # Grid settings
    GRID_MIN_LEVELS = 2
    GRID_MAX_LEVELS = 50
    
    # Validation
    MIN_QUANTITY = 0.001  # Minimum order quantity
    MAX_PRICE_DEVIATION = 0.2  # 20% max deviation from current price
