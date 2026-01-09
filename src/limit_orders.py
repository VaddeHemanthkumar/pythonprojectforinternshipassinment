"""
Limit Orders Module
Place orders at specific price levels
"""

import sys
from src.binance_client import BinanceClient
from src.validator import Validator, ValidationError
from src.logger import get_logger

logger = get_logger('LimitOrders')


def execute_limit_order(symbol: str, side: str, quantity: float, price: float,
                       time_in_force: str = 'GTC') -> bool:
    """
    Execute a limit order
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        side: Order side (BUY or SELL)
        quantity: Order quantity
        price: Limit price
        time_in_force: Time in force (GTC, IOC, FOK)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Validate inputs
        logger.info(f"Validating limit order parameters...")
        symbol = Validator.validate_symbol(symbol)
        side = Validator.validate_side(side)
        quantity = Validator.validate_quantity(quantity)
        price = Validator.validate_price(price)
        
        # Log order details
        logger.log_order('LIMIT', symbol, side, quantity, price, timeInForce=time_in_force)
        
        # Initialize client
        client = BinanceClient()
        
        # Get current price for comparison
        current_price = client.get_current_price(symbol)
        if current_price:
            logger.info(f"Current market price for {symbol}: {current_price}")
            price_diff = ((price - current_price) / current_price) * 100
            logger.info(f"Limit price is {price_diff:+.2f}% from current market price")
            
            # Warn if price is far from current price
            if abs(price_diff) > 10:
                logger.warning(
                    f"Limit price ({price}) is {abs(price_diff):.2f}% away from "
                    f"current price ({current_price}). Order may not fill quickly."
                )
        
        # Calculate order value
        order_value = quantity * price
        logger.info(f"Order value: {order_value} USDT")
        
        # Execute order
        logger.info(f"Placing limit order...")
        response = client.create_limit_order(symbol, side, quantity, price, time_in_force)
        
        if response:
            order_id = response.get('orderId')
            status = response.get('status')
            orig_qty = response.get('origQty', quantity)
            
            logger.log_order_success('LIMIT', order_id, response)
            logger.info(f"Order Status: {status}")
            logger.info(f"Original Quantity: {orig_qty}")
            
            print(f"\n✓ Limit order placed successfully!")
            print(f"  Order ID: {order_id}")
            print(f"  Symbol: {symbol}")
            print(f"  Side: {side}")
            print(f"  Quantity: {orig_qty}")
            print(f"  Limit Price: {price}")
            print(f"  Status: {status}")
            print(f"  Time in Force: {time_in_force}")
            
            if current_price:
                print(f"  Current Market Price: {current_price}")
                print(f"  Price Difference: {price_diff:+.2f}%")
            
            if status == 'NEW':
                print(f"\n  Note: Order is pending. It will execute when market price reaches {price}")
            
            return True
        else:
            logger.log_order_error('LIMIT', 'Order placement failed')
            print("\n✗ Limit order failed. Check bot.log for details.")
            return False
            
    except ValidationError as e:
        logger.log_order_error('LIMIT', f"Validation error: {str(e)}")
        print(f"\n✗ Validation Error: {str(e)}")
        return False
    except Exception as e:
        logger.log_order_error('LIMIT', f"Unexpected error: {str(e)}", exc_info=True)
        print(f"\n✗ Error: {str(e)}")
        return False


def main():
    """Main entry point for CLI"""
    if len(sys.argv) < 5 or len(sys.argv) > 6:
        print("Usage: python src/limit_orders.py <SYMBOL> <SIDE> <QUANTITY> <PRICE> [TIME_IN_FORCE]")
        print("\nExamples:")
        print("  python src/limit_orders.py BTCUSDT BUY 0.01 40000")
        print("  python src/limit_orders.py ETHUSDT SELL 0.1 3000 GTC")
        print("\nParameters:")
        print("  SYMBOL        - Trading pair (e.g., BTCUSDT, ETHUSDT)")
        print("  SIDE          - BUY or SELL")
        print("  QUANTITY      - Order quantity (must be > 0)")
        print("  PRICE         - Limit price")
        print("  TIME_IN_FORCE - Optional: GTC (default), IOC, or FOK")
        print("\nTime in Force:")
        print("  GTC - Good Till Cancel (default)")
        print("  IOC - Immediate or Cancel")
        print("  FOK - Fill or Kill")
        sys.exit(1)
    
    symbol = sys.argv[1]
    side = sys.argv[2]
    
    try:
        quantity = float(sys.argv[3])
    except ValueError:
        print(f"✗ Error: QUANTITY must be a valid number, got '{sys.argv[3]}'")
        sys.exit(1)
    
    try:
        price = float(sys.argv[4])
    except ValueError:
        print(f"✗ Error: PRICE must be a valid number, got '{sys.argv[4]}'")
        sys.exit(1)
    
    time_in_force = sys.argv[5] if len(sys.argv) == 6 else 'GTC'
    
    # Validate time in force
    valid_tif = ['GTC', 'IOC', 'FOK']
    if time_in_force.upper() not in valid_tif:
        print(f"✗ Error: TIME_IN_FORCE must be one of {valid_tif}, got '{time_in_force}'")
        sys.exit(1)
    
    time_in_force = time_in_force.upper()
    
    # Display order summary
    print("\n" + "="*60)
    print("LIMIT ORDER PLACEMENT")
    print("="*60)
    print(f"Symbol:        {symbol}")
    print(f"Side:          {side}")
    print(f"Quantity:      {quantity}")
    print(f"Limit Price:   {price}")
    print(f"Time in Force: {time_in_force}")
    print(f"Order Value:   {quantity * price} USDT")
    print("="*60)
    print("\nPlacing order...\n")
    
    # Execute order
    success = execute_limit_order(symbol, side, quantity, price, time_in_force)
    
    if success:
        print("\n" + "="*60)
        print("Order placement completed successfully!")
        print("Check bot.log for detailed information.")
        print("="*60 + "\n")
        sys.exit(0)
    else:
        print("\n" + "="*60)
        print("Order placement failed!")
        print("Check bot.log for error details.")
        print("="*60 + "\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
