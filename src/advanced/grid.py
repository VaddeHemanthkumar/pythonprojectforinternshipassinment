"""
Grid Trading Strategy Module
Automated buy-low/sell-high within a price range
"""

import sys
import time
from datetime import datetime
from typing import List, Dict, Any
from src.binance_client import BinanceClient
from src.validator import Validator, ValidationError
from src.logger import get_logger

logger = get_logger('GridStrategy')


class GridTrader:
    """Grid trading strategy implementation"""
    
    def __init__(self, symbol: str, lower_price: float, upper_price: float,
                 grid_levels: int, quantity_per_level: float):
        """
        Initialize grid trader
        
        Args:
            symbol: Trading pair symbol
            lower_price: Lower bound of grid
            upper_price: Upper bound of grid
            grid_levels: Number of grid levels
            quantity_per_level: Quantity to trade at each level
        """
        self.symbol = symbol
        self.lower_price = lower_price
        self.upper_price = upper_price
        self.grid_levels = grid_levels
        self.quantity_per_level = quantity_per_level
        
        # Calculate grid prices
        self.price_step = (upper_price - lower_price) / (grid_levels - 1)
        self.grid_prices = [
            lower_price + (i * self.price_step)
            for i in range(grid_levels)
        ]
        
        # Track orders
        self.buy_orders: List[Dict[str, Any]] = []
        self.sell_orders: List[Dict[str, Any]] = []
        self.filled_orders: List[Dict[str, Any]] = []
        
        # Client
        self.client = BinanceClient()
        
        logger.info(f"Grid trader initialized:")
        logger.info(f"  Symbol: {symbol}")
        logger.info(f"  Price range: {lower_price} - {upper_price}")
        logger.info(f"  Grid levels: {grid_levels}")
        logger.info(f"  Price step: {self.price_step}")
        logger.info(f"  Quantity per level: {quantity_per_level}")
    
    def setup_grid(self) -> bool:
        """
        Set up initial grid orders
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get current price
            current_price = self.client.get_current_price(self.symbol)
            if not current_price:
                logger.error("Failed to get current price")
                return False
            
            logger.info(f"Current price: {current_price}")
            
            # Validate current price is within grid range
            if current_price < self.lower_price or current_price > self.upper_price:
                logger.warning(
                    f"Current price ({current_price}) is outside grid range "
                    f"({self.lower_price} - {self.upper_price})"
                )
                print(f"\n⚠ Warning: Current price ({current_price}) is outside grid range!")
                print(f"  Grid range: {self.lower_price} - {self.upper_price}")
                print(f"  Consider adjusting your grid parameters.")
            
            print(f"\nSetting up grid orders...")
            print(f"Current price: {current_price}")
            print(f"\nGrid levels:")
            
            # Place buy orders below current price
            # Place sell orders above current price
            for i, price in enumerate(self.grid_prices):
                level_num = i + 1
                
                if price < current_price:
                    # Place buy order
                    logger.info(f"Placing BUY order at level {level_num}: {price}")
                    response = self.client.create_limit_order(
                        self.symbol, 'BUY', self.quantity_per_level, price, 'GTC'
                    )
                    
                    if response:
                        order_id = response.get('orderId')
                        self.buy_orders.append({
                            'order_id': order_id,
                            'price': price,
                            'quantity': self.quantity_per_level,
                            'level': level_num
                        })
                        logger.info(f"BUY order placed: ID={order_id}, Price={price}")
                        print(f"  Level {level_num:2d}: BUY  at {price:10.2f} - Order ID: {order_id}")
                    else:
                        logger.error(f"Failed to place BUY order at {price}")
                        print(f"  Level {level_num:2d}: BUY  at {price:10.2f} - FAILED")
                
                elif price > current_price:
                    # Place sell order
                    logger.info(f"Placing SELL order at level {level_num}: {price}")
                    response = self.client.create_limit_order(
                        self.symbol, 'SELL', self.quantity_per_level, price, 'GTC'
                    )
                    
                    if response:
                        order_id = response.get('orderId')
                        self.sell_orders.append({
                            'order_id': order_id,
                            'price': price,
                            'quantity': self.quantity_per_level,
                            'level': level_num
                        })
                        logger.info(f"SELL order placed: ID={order_id}, Price={price}")
                        print(f"  Level {level_num:2d}: SELL at {price:10.2f} - Order ID: {order_id}")
                    else:
                        logger.error(f"Failed to place SELL order at {price}")
                        print(f"  Level {level_num:2d}: SELL at {price:10.2f} - FAILED")
                
                else:
                    # Price is at current level
                    print(f"  Level {level_num:2d}: ---- at {price:10.2f} - CURRENT PRICE")
            
            total_orders = len(self.buy_orders) + len(self.sell_orders)
            logger.info(f"Grid setup complete: {len(self.buy_orders)} buy orders, {len(self.sell_orders)} sell orders")
            
            print(f"\nGrid setup complete!")
            print(f"  Buy orders:  {len(self.buy_orders)}")
            print(f"  Sell orders: {len(self.sell_orders)}")
            print(f"  Total:       {total_orders}")
            
            return total_orders > 0
            
        except Exception as e:
            logger.error(f"Error setting up grid: {str(e)}", exc_info=True)
            return False
    
    def display_summary(self):
        """Display grid summary"""
        print(f"\n{'='*60}")
        print(f"GRID TRADING SUMMARY")
        print(f"{'='*60}")
        print(f"Symbol:              {self.symbol}")
        print(f"Price Range:         {self.lower_price} - {self.upper_price}")
        print(f"Grid Levels:         {self.grid_levels}")
        print(f"Price Step:          {self.price_step:.2f}")
        print(f"Quantity per Level:  {self.quantity_per_level}")
        print(f"\nActive Orders:")
        print(f"  Buy Orders:        {len(self.buy_orders)}")
        print(f"  Sell Orders:       {len(self.sell_orders)}")
        print(f"  Total Active:      {len(self.buy_orders) + len(self.sell_orders)}")
        print(f"{'='*60}\n")


def execute_grid_strategy(symbol: str, lower_price: float, upper_price: float,
                          grid_levels: int, quantity_per_level: float) -> bool:
    """
    Execute grid trading strategy
    
    Args:
        symbol: Trading pair symbol
        lower_price: Lower bound of grid
        upper_price: Upper bound of grid
        grid_levels: Number of grid levels
        quantity_per_level: Quantity to trade at each level
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Validate inputs
        logger.info(f"Validating grid strategy parameters...")
        symbol = Validator.validate_symbol(symbol)
        lower_price, upper_price = Validator.validate_price_range(lower_price, upper_price)
        grid_levels = Validator.validate_grid_levels(grid_levels)
        quantity_per_level = Validator.validate_quantity(quantity_per_level)
        
        # Create grid trader
        grid_trader = GridTrader(symbol, lower_price, upper_price, grid_levels, quantity_per_level)
        
        # Display grid configuration
        print(f"\n{'='*60}")
        print(f"GRID STRATEGY CONFIGURATION")
        print(f"{'='*60}")
        print(f"Symbol:             {symbol}")
        print(f"Lower Price:        {lower_price}")
        print(f"Upper Price:        {upper_price}")
        print(f"Grid Levels:        {grid_levels}")
        print(f"Price Step:         {grid_trader.price_step:.2f}")
        print(f"Quantity per Level: {quantity_per_level}")
        print(f"{'='*60}")
        
        # Calculate total investment
        total_buy_orders = (grid_levels // 2)  # Approximate
        estimated_investment = total_buy_orders * quantity_per_level * lower_price
        print(f"\nEstimated Investment: ~{estimated_investment:.2f} USDT")
        print(f"(This is approximate, actual may vary based on current price)")
        
        # Set up grid
        print(f"\n{'='*60}")
        success = grid_trader.setup_grid()
        print(f"{'='*60}")
        
        if success:
            grid_trader.display_summary()
            
            print(f"Grid Strategy Notes:")
            print(f"  - Buy orders are placed below current price")
            print(f"  - Sell orders are placed above current price")
            print(f"  - As price moves, orders will fill automatically")
            print(f"  - Monitor filled orders and replace them to maintain the grid")
            print(f"  - This is a basic grid setup; advanced versions would auto-replace orders")
            
            return True
        else:
            logger.error("Failed to set up grid")
            return False
            
    except ValidationError as e:
        logger.log_order_error('GRID', f"Validation error: {str(e)}")
        print(f"\n✗ Validation Error: {str(e)}")
        return False
    except Exception as e:
        logger.log_order_error('GRID', f"Unexpected error: {str(e)}", exc_info=True)
        print(f"\n✗ Error: {str(e)}")
        return False


def main():
    """Main entry point for CLI"""
    if len(sys.argv) != 6:
        print("Usage: python src/advanced/grid.py <SYMBOL> <LOWER_PRICE> <UPPER_PRICE> <GRID_LEVELS> <QUANTITY_PER_LEVEL>")
        print("\nExamples:")
        print("  # Create grid for BTC between $38,000 and $42,000 with 10 levels")
        print("  python src/advanced/grid.py BTCUSDT 38000 42000 10 0.01")
        print("\n  # Create grid for ETH between $2,800 and $3,200 with 20 levels")
        print("  python src/advanced/grid.py ETHUSDT 2800 3200 20 0.1")
        print("\nParameters:")
        print("  SYMBOL              - Trading pair (e.g., BTCUSDT)")
        print("  LOWER_PRICE         - Lower bound of grid")
        print("  UPPER_PRICE         - Upper bound of grid")
        print("  GRID_LEVELS         - Number of grid levels (2-50)")
        print("  QUANTITY_PER_LEVEL  - Quantity to trade at each level")
        print("\nHow it works:")
        print("  - Places buy orders below current price")
        print("  - Places sell orders above current price")
        print("  - Profits from price oscillations within the range")
        print("  - Best for ranging/sideways markets")
        print("\nNote: Ensure you have sufficient balance for all buy orders!")
        sys.exit(1)
    
    symbol = sys.argv[1]
    
    try:
        lower_price = float(sys.argv[2])
        upper_price = float(sys.argv[3])
        grid_levels = int(sys.argv[4])
        quantity_per_level = float(sys.argv[5])
    except ValueError as e:
        print(f"✗ Error: Invalid numeric parameters")
        print(f"  {str(e)}")
        sys.exit(1)
    
    # Execute strategy
    success = execute_grid_strategy(
        symbol, lower_price, upper_price, grid_levels, quantity_per_level
    )
    
    if success:
        print("\n" + "="*60)
        print("Grid strategy setup completed successfully!")
        print("Check bot.log for detailed information.")
        print("="*60 + "\n")
        sys.exit(0)
    else:
        print("\n" + "="*60)
        print("Grid strategy setup failed!")
        print("Check bot.log for error details.")
        print("="*60 + "\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
