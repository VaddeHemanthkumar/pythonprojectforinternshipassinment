"""
Market Orders Module
Execute immediate buy/sell orders at current market price

Author: Hemanth Kumar
Date: January 2026
Note: This was my first implementation - took a while to figure out the 
      Binance API requirements, especially the minimum order size!
"""

import sys
from src.binance_client import BinanceClient
from src.validator import Validator, ValidationError
from src.logger import get_logger

logger = get_logger('MarketOrders')


def execute_market_order(symbol: str, side: str, quantity: float) -> bool:
    """
    Execute a market order
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        side: Order side (BUY or SELL)
        quantity: Order quantity
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Validate inputs
        logger.info(f"Validating market order parameters...")
        symbol = Validator.validate_symbol(symbol)
        side = Validator.validate_side(side)
        quantity = Validator.validate_quantity(quantity)
        
        # Log order details
        logger.log_order('MARKET', symbol, side, quantity)
        
        # Initialize client
        client = BinanceClient()
        
        # Get current price for reference
        current_price = client.get_current_price(symbol)
        if current_price:
            logger.info(f"Current market price for {symbol}: {current_price}")
            estimated_value = quantity * current_price
            logger.info(f"Estimated order value: {estimated_value} USDT")
        
        # Execute order
        logger.info(f"Executing market order...")
        response = client.create_market_order(symbol, side, quantity)
        
        if response:
            order_id = response.get('orderId')
            status = response.get('status')
            executed_qty = response.get('executedQty', quantity)
            
            logger.log_order_success('MARKET', order_id, response)
            logger.info(f"Order Status: {status}")
            logger.info(f"Executed Quantity: {executed_qty}")
            
            # Get average fill price if available
            if 'avgPrice' in response:
                avg_price = float(response['avgPrice'])
                logger.info(f"Average Fill Price: {avg_price}")
                total_value = float(executed_qty) * avg_price
                logger.info(f"Total Value: {total_value} USDT")
            
            print(f"\n✓ Market order executed successfully!")
            print(f"  Order ID: {order_id}")
            print(f"  Symbol: {symbol}")
            print(f"  Side: {side}")
            print(f"  Quantity: {executed_qty}")
            print(f"  Status: {status}")
            
            return True
        else:
            logger.log_order_error('MARKET', 'Order execution failed')
            print("\n✗ Market order failed. Check bot.log for details.")
            return False
            
    except ValidationError as e:
        logger.log_order_error('MARKET', f"Validation error: {str(e)}")
        print(f"\n✗ Validation Error: {str(e)}")
        return False
    except Exception as e:
        logger.log_order_error('MARKET', f"Unexpected error: {str(e)}", exc_info=True)
        print(f"\n✗ Error: {str(e)}")
        return False


def main():
    """Main entry point for CLI"""
    if len(sys.argv) != 4:
        print("Usage: python src/market_orders.py <SYMBOL> <SIDE> <QUANTITY>")
        print("\nExamples:")
        print("  python src/market_orders.py BTCUSDT BUY 0.01")
        print("  python src/market_orders.py ETHUSDT SELL 0.1")
        print("\nParameters:")
        print("  SYMBOL   - Trading pair (e.g., BTCUSDT, ETHUSDT)")
        print("  SIDE     - BUY or SELL")
        print("  QUANTITY - Order quantity (must be > 0)")
        sys.exit(1)
    
    symbol = sys.argv[1]
    side = sys.argv[2]
    
    try:
        quantity = float(sys.argv[3])
    except ValueError:
        print(f"✗ Error: QUANTITY must be a valid number, got '{sys.argv[3]}'")
        sys.exit(1)
    
    # Display order summary
    print("\n" + "="*60)
    print("MARKET ORDER EXECUTION")
    print("="*60)
    print(f"Symbol:   {symbol}")
    print(f"Side:     {side}")
    print(f"Quantity: {quantity}")
    print("="*60)
    print("\nExecuting order...\n")
    
    # Execute order
    success = execute_market_order(symbol, side, quantity)
    
    if success:
        print("\n" + "="*60)
        print("Order execution completed successfully!")
        print("Check bot.log for detailed information.")
        print("="*60 + "\n")
        sys.exit(0)
    else:
        print("\n" + "="*60)
        print("Order execution failed!")
        print("Check bot.log for error details.")
        print("="*60 + "\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
