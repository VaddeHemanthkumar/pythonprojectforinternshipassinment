"""
Binance API Client Wrapper
Handles communication with Binance Futures API
"""

import time
import hmac
import hashlib
from urllib.parse import urlencode
from typing import Dict, Any, Optional
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

from src.config import Config
from src.logger import get_logger

logger = get_logger('BinanceClient')


class BinanceClient:
    """Wrapper for Binance Futures API client"""
    
    def __init__(self):
        """Initialize Binance client"""
        # Validate credentials
        Config.validate_credentials()
        
        # Initialize client
        try:
            self.client = Client(
                Config.API_KEY,
                Config.API_SECRET,
                testnet=Config.USE_TESTNET
            )
            
            env = Config.get_environment_name()
            logger.info(f"Binance client initialized successfully ({env})")
            
            # Test connection
            self._test_connection()
            
        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {str(e)}", exc_info=True)
            raise
    
    def _test_connection(self):
        """Test API connection"""
        try:
            # Test connectivity
            self.client.ping()
            logger.info("API connection test successful")
            
            # Get server time
            server_time = self.client.get_server_time()
            logger.debug(f"Server time: {server_time}")
            
        except BinanceAPIException as e:
            logger.error(f"API connection test failed: {e.message}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}", exc_info=True)
            raise
    
    def get_symbol_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get symbol information
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Symbol info dict or None if not found
        """
        try:
            logger.log_api_call('futures_exchange_info', {'symbol': symbol})
            exchange_info = self.client.futures_exchange_info()
            
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol:
                    logger.debug(f"Symbol info retrieved for {symbol}")
                    return s
            
            logger.warning(f"Symbol {symbol} not found in exchange info")
            return None
            
        except BinanceAPIException as e:
            logger.error(f"Failed to get symbol info: {e.message}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"Error getting symbol info: {str(e)}", exc_info=True)
            return None
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """
        Get current market price for symbol
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Current price or None if error
        """
        try:
            logger.log_api_call('futures_symbol_ticker', {'symbol': symbol})
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            logger.debug(f"Current price for {symbol}: {price}")
            return price
            
        except BinanceAPIException as e:
            logger.error(f"Failed to get current price: {e.message}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"Error getting current price: {str(e)}", exc_info=True)
            return None
    
    def get_account_balance(self) -> Optional[Dict[str, Any]]:
        """
        Get account balance
        
        Returns:
            Account balance info or None if error
        """
        try:
            logger.log_api_call('futures_account_balance')
            balance = self.client.futures_account_balance()
            logger.debug(f"Account balance retrieved")
            return balance
            
        except BinanceAPIException as e:
            logger.error(f"Failed to get account balance: {e.message}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"Error getting account balance: {str(e)}", exc_info=True)
            return None
    
    def create_market_order(self, symbol: str, side: str, quantity: float) -> Optional[Dict[str, Any]]:
        """
        Create market order
        
        Args:
            symbol: Trading pair symbol
            side: BUY or SELL
            quantity: Order quantity
            
        Returns:
            Order response or None if error
        """
        try:
            logger.log_api_call('futures_create_order', {
                'symbol': symbol,
                'side': side,
                'type': 'MARKET',
                'quantity': quantity
            })
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            
            logger.debug(f"Market order created: {order}")
            return order
            
        except BinanceOrderException as e:
            logger.error(f"Order failed: {e.message}", exc_info=True)
            return None
        except BinanceAPIException as e:
            logger.error(f"API error: {e.message}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"Error creating market order: {str(e)}", exc_info=True)
            return None
    
    def create_limit_order(self, symbol: str, side: str, quantity: float, price: float, 
                          time_in_force: str = 'GTC') -> Optional[Dict[str, Any]]:
        """
        Create limit order
        
        Args:
            symbol: Trading pair symbol
            side: BUY or SELL
            quantity: Order quantity
            price: Limit price
            time_in_force: Time in force (GTC, IOC, FOK)
            
        Returns:
            Order response or None if error
        """
        try:
            logger.log_api_call('futures_create_order', {
                'symbol': symbol,
                'side': side,
                'type': 'LIMIT',
                'quantity': quantity,
                'price': price,
                'timeInForce': time_in_force
            })
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                quantity=quantity,
                price=price,
                timeInForce=time_in_force
            )
            
            logger.debug(f"Limit order created: {order}")
            return order
            
        except BinanceOrderException as e:
            logger.error(f"Order failed: {e.message}", exc_info=True)
            return None
        except BinanceAPIException as e:
            logger.error(f"API error: {e.message}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"Error creating limit order: {str(e)}", exc_info=True)
            return None
    
    def create_stop_limit_order(self, symbol: str, side: str, quantity: float,
                               stop_price: float, price: float,
                               time_in_force: str = 'GTC') -> Optional[Dict[str, Any]]:
        """
        Create stop-limit order
        
        Args:
            symbol: Trading pair symbol
            side: BUY or SELL
            quantity: Order quantity
            stop_price: Stop trigger price
            price: Limit price
            time_in_force: Time in force
            
        Returns:
            Order response or None if error
        """
        try:
            logger.log_api_call('futures_create_order', {
                'symbol': symbol,
                'side': side,
                'type': 'STOP',
                'quantity': quantity,
                'stopPrice': stop_price,
                'price': price,
                'timeInForce': time_in_force
            })
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP',
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
                timeInForce=time_in_force
            )
            
            logger.debug(f"Stop-limit order created: {order}")
            return order
            
        except BinanceOrderException as e:
            logger.error(f"Order failed: {e.message}", exc_info=True)
            return None
        except BinanceAPIException as e:
            logger.error(f"API error: {e.message}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"Error creating stop-limit order: {str(e)}", exc_info=True)
            return None
    
    def cancel_order(self, symbol: str, order_id: int) -> Optional[Dict[str, Any]]:
        """
        Cancel an order
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID to cancel
            
        Returns:
            Cancel response or None if error
        """
        try:
            logger.log_api_call('futures_cancel_order', {
                'symbol': symbol,
                'orderId': order_id
            })
            
            result = self.client.futures_cancel_order(
                symbol=symbol,
                orderId=order_id
            )
            
            logger.debug(f"Order cancelled: {result}")
            return result
            
        except BinanceAPIException as e:
            logger.error(f"Failed to cancel order: {e.message}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"Error cancelling order: {str(e)}", exc_info=True)
            return None
    
    def get_order_status(self, symbol: str, order_id: int) -> Optional[Dict[str, Any]]:
        """
        Get order status
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID
            
        Returns:
            Order status or None if error
        """
        try:
            logger.log_api_call('futures_get_order', {
                'symbol': symbol,
                'orderId': order_id
            })
            
            order = self.client.futures_get_order(
                symbol=symbol,
                orderId=order_id
            )
            
            logger.debug(f"Order status: {order}")
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Failed to get order status: {e.message}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"Error getting order status: {str(e)}", exc_info=True)
            return None
