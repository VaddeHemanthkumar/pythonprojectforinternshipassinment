"""
Validation module for Binance Futures Trading Bot
Validates trading parameters before order execution
"""

import re
from typing import Optional, Tuple
from src.logger import get_logger

logger = get_logger('Validator')


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class Validator:
    """Input validator for trading parameters"""
    
    # Common trading pairs on Binance Futures
    COMMON_SYMBOLS = [
        'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT',
        'XRPUSDT', 'DOTUSDT', 'UNIUSDT', 'SOLUSDT', 'MATICUSDT',
        'LTCUSDT', 'LINKUSDT', 'AVAXUSDT', 'ATOMUSDT', 'ETCUSDT'
    ]
    
    VALID_SIDES = ['BUY', 'SELL']
    VALID_ORDER_TYPES = ['MARKET', 'LIMIT', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET']
    
    @staticmethod
    def validate_symbol(symbol: str) -> str:
        """
        Validate trading symbol
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            
        Returns:
            Validated symbol in uppercase
            
        Raises:
            ValidationError: If symbol is invalid
        """
        if not symbol:
            logger.log_validation_error('symbol', symbol, 'Symbol cannot be empty')
            raise ValidationError("Symbol cannot be empty")
        
        symbol = symbol.upper().strip()
        
        # Check format (should end with USDT for USDT-M futures)
        if not symbol.endswith('USDT'):
            logger.log_validation_error('symbol', symbol, 'Symbol must end with USDT for USDT-M futures')
            raise ValidationError(f"Invalid symbol format: {symbol}. Must end with USDT (e.g., BTCUSDT)")
        
        # Check if it's a known symbol (warning only)
        if symbol not in Validator.COMMON_SYMBOLS:
            logger.warning(f"Symbol {symbol} is not in common symbols list. Proceeding anyway.")
        
        logger.debug(f"Symbol validation passed: {symbol}")
        return symbol
    
    @staticmethod
    def validate_side(side: str) -> str:
        """
        Validate order side
        
        Args:
            side: Order side (BUY or SELL)
            
        Returns:
            Validated side in uppercase
            
        Raises:
            ValidationError: If side is invalid
        """
        if not side:
            logger.log_validation_error('side', side, 'Side cannot be empty')
            raise ValidationError("Side cannot be empty")
        
        side = side.upper().strip()
        
        if side not in Validator.VALID_SIDES:
            logger.log_validation_error('side', side, f'Must be one of {Validator.VALID_SIDES}')
            raise ValidationError(f"Invalid side: {side}. Must be BUY or SELL")
        
        logger.debug(f"Side validation passed: {side}")
        return side
    
    @staticmethod
    def validate_quantity(quantity: float, min_qty: float = 0.001) -> float:
        """
        Validate order quantity
        
        Args:
            quantity: Order quantity
            min_qty: Minimum allowed quantity
            
        Returns:
            Validated quantity
            
        Raises:
            ValidationError: If quantity is invalid
        """
        try:
            quantity = float(quantity)
        except (ValueError, TypeError):
            logger.log_validation_error('quantity', quantity, 'Must be a valid number')
            raise ValidationError(f"Invalid quantity: {quantity}. Must be a number")
        
        if quantity <= 0:
            logger.log_validation_error('quantity', quantity, 'Must be greater than 0')
            raise ValidationError(f"Invalid quantity: {quantity}. Must be greater than 0")
        
        if quantity < min_qty:
            logger.log_validation_error('quantity', quantity, f'Must be at least {min_qty}')
            raise ValidationError(f"Quantity {quantity} is below minimum {min_qty}")
        
        logger.debug(f"Quantity validation passed: {quantity}")
        return quantity
    
    @staticmethod
    def validate_price(price: float, allow_zero: bool = False) -> float:
        """
        Validate price
        
        Args:
            price: Price value
            allow_zero: Whether to allow zero price (for market orders)
            
        Returns:
            Validated price
            
        Raises:
            ValidationError: If price is invalid
        """
        try:
            price = float(price)
        except (ValueError, TypeError):
            logger.log_validation_error('price', price, 'Must be a valid number')
            raise ValidationError(f"Invalid price: {price}. Must be a number")
        
        if not allow_zero and price <= 0:
            logger.log_validation_error('price', price, 'Must be greater than 0')
            raise ValidationError(f"Invalid price: {price}. Must be greater than 0")
        
        if price < 0:
            logger.log_validation_error('price', price, 'Cannot be negative')
            raise ValidationError(f"Invalid price: {price}. Cannot be negative")
        
        logger.debug(f"Price validation passed: {price}")
        return price
    
    @staticmethod
    def validate_price_range(lower_price: float, upper_price: float) -> Tuple[float, float]:
        """
        Validate price range
        
        Args:
            lower_price: Lower bound price
            upper_price: Upper bound price
            
        Returns:
            Tuple of (lower_price, upper_price)
            
        Raises:
            ValidationError: If price range is invalid
        """
        lower_price = Validator.validate_price(lower_price)
        upper_price = Validator.validate_price(upper_price)
        
        if lower_price >= upper_price:
            logger.log_validation_error(
                'price_range',
                f'{lower_price}-{upper_price}',
                'Lower price must be less than upper price'
            )
            raise ValidationError(
                f"Invalid price range: lower={lower_price}, upper={upper_price}. "
                "Lower price must be less than upper price"
            )
        
        logger.debug(f"Price range validation passed: {lower_price} - {upper_price}")
        return lower_price, upper_price
    
    @staticmethod
    def validate_grid_levels(levels: int, min_levels: int = 2, max_levels: int = 50) -> int:
        """
        Validate grid levels
        
        Args:
            levels: Number of grid levels
            min_levels: Minimum allowed levels
            max_levels: Maximum allowed levels
            
        Returns:
            Validated levels
            
        Raises:
            ValidationError: If levels is invalid
        """
        try:
            levels = int(levels)
        except (ValueError, TypeError):
            logger.log_validation_error('grid_levels', levels, 'Must be a valid integer')
            raise ValidationError(f"Invalid grid levels: {levels}. Must be an integer")
        
        if levels < min_levels:
            logger.log_validation_error('grid_levels', levels, f'Must be at least {min_levels}')
            raise ValidationError(f"Grid levels {levels} is below minimum {min_levels}")
        
        if levels > max_levels:
            logger.log_validation_error('grid_levels', levels, f'Must be at most {max_levels}')
            raise ValidationError(f"Grid levels {levels} exceeds maximum {max_levels}")
        
        logger.debug(f"Grid levels validation passed: {levels}")
        return levels
    
    @staticmethod
    def validate_twap_params(num_orders: int, duration_minutes: int) -> Tuple[int, int]:
        """
        Validate TWAP parameters
        
        Args:
            num_orders: Number of orders to split into
            duration_minutes: Duration in minutes
            
        Returns:
            Tuple of (num_orders, duration_minutes)
            
        Raises:
            ValidationError: If parameters are invalid
        """
        try:
            num_orders = int(num_orders)
            duration_minutes = int(duration_minutes)
        except (ValueError, TypeError):
            logger.log_validation_error('twap_params', f'{num_orders}/{duration_minutes}', 'Must be valid integers')
            raise ValidationError("TWAP parameters must be integers")
        
        if num_orders < 2:
            logger.log_validation_error('num_orders', num_orders, 'Must be at least 2')
            raise ValidationError(f"Number of orders {num_orders} must be at least 2")
        
        if num_orders > 100:
            logger.log_validation_error('num_orders', num_orders, 'Must be at most 100')
            raise ValidationError(f"Number of orders {num_orders} exceeds maximum 100")
        
        if duration_minutes < 1:
            logger.log_validation_error('duration_minutes', duration_minutes, 'Must be at least 1 minute')
            raise ValidationError(f"Duration {duration_minutes} must be at least 1 minute")
        
        if duration_minutes > 1440:
            logger.log_validation_error('duration_minutes', duration_minutes, 'Must be at most 1440 minutes (24 hours)')
            raise ValidationError(f"Duration {duration_minutes} exceeds maximum 1440 minutes")
        
        logger.debug(f"TWAP params validation passed: {num_orders} orders over {duration_minutes} minutes")
        return num_orders, duration_minutes
    
    @staticmethod
    def validate_stop_limit_prices(stop_price: float, limit_price: float, side: str) -> Tuple[float, float]:
        """
        Validate stop-limit order prices
        
        Args:
            stop_price: Stop trigger price
            limit_price: Limit order price
            side: Order side (BUY or SELL)
            
        Returns:
            Tuple of (stop_price, limit_price)
            
        Raises:
            ValidationError: If prices are invalid
        """
        stop_price = Validator.validate_price(stop_price)
        limit_price = Validator.validate_price(limit_price)
        side = Validator.validate_side(side)
        
        # For BUY stop-limit: limit_price should be >= stop_price
        # For SELL stop-limit: limit_price should be <= stop_price
        if side == 'BUY' and limit_price < stop_price:
            logger.warning(
                f"BUY stop-limit: limit_price ({limit_price}) < stop_price ({stop_price}). "
                "This may not execute as expected."
            )
        elif side == 'SELL' and limit_price > stop_price:
            logger.warning(
                f"SELL stop-limit: limit_price ({limit_price}) > stop_price ({stop_price}). "
                "This may not execute as expected."
            )
        
        logger.debug(f"Stop-limit prices validation passed: stop={stop_price}, limit={limit_price}")
        return stop_price, limit_price
