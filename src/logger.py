"""
Logging module for Binance Futures Trading Bot
Provides structured logging with timestamps and error tracking
"""

import logging
import os
from datetime import datetime


class BotLogger:
    """Custom logger for the trading bot"""
    
    def __init__(self, name='BinanceBot', log_file='bot.log'):
        """
        Initialize logger
        
        Args:
            name: Logger name
            log_file: Path to log file
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            return
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler - detailed logging
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        
        # Console handler - important messages only
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(detailed_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message, exc_info=False):
        """Log error message with optional exception info"""
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message, exc_info=False):
        """Log critical message with optional exception info"""
        self.logger.critical(message, exc_info=exc_info)
    
    def log_order(self, order_type, symbol, side, quantity, price=None, **kwargs):
        """
        Log order placement
        
        Args:
            order_type: Type of order (MARKET, LIMIT, etc.)
            symbol: Trading pair symbol
            side: BUY or SELL
            quantity: Order quantity
            price: Order price (optional)
            **kwargs: Additional order parameters
        """
        msg = f"{order_type} Order - Placing {side} order for {quantity} {symbol}"
        if price:
            msg += f" at {price}"
        
        if kwargs:
            msg += f" | Additional params: {kwargs}"
        
        self.info(msg)
    
    def log_order_success(self, order_type, order_id, response=None):
        """
        Log successful order placement
        
        Args:
            order_type: Type of order
            order_id: Order ID from exchange
            response: Full API response (optional)
        """
        msg = f"{order_type} Order - Order placed successfully: Order ID {order_id}"
        self.info(msg)
        
        if response:
            self.debug(f"Full response: {response}")
    
    def log_order_error(self, order_type, error_msg, exc_info=False):
        """
        Log order error
        
        Args:
            order_type: Type of order
            error_msg: Error message
            exc_info: Include exception traceback
        """
        msg = f"{order_type} Order - Error: {error_msg}"
        self.error(msg, exc_info=exc_info)
    
    def log_validation_error(self, field, value, reason):
        """
        Log validation error
        
        Args:
            field: Field that failed validation
            value: Invalid value
            reason: Reason for failure
        """
        msg = f"Validation Error - {field}='{value}': {reason}"
        self.error(msg)
    
    def log_api_call(self, endpoint, params=None):
        """
        Log API call
        
        Args:
            endpoint: API endpoint
            params: Request parameters
        """
        msg = f"API Call - {endpoint}"
        if params:
            # Mask sensitive data
            safe_params = {k: v for k, v in params.items() if k not in ['signature', 'apiKey']}
            msg += f" | Params: {safe_params}"
        
        self.debug(msg)


# Create default logger instance
default_logger = BotLogger()


def get_logger(name='BinanceBot'):
    """
    Get a logger instance
    
    Args:
        name: Logger name
        
    Returns:
        BotLogger instance
    """
    return BotLogger(name)
