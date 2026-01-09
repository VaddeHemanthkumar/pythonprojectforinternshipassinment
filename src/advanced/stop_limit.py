"""
Stop-Limit Orders Module
Trigger a limit order when a stop price is reached
"""

import sys
from src.binance_client import BinanceClient
from src.validator import Validator, ValidationError
from src.logger import get_logger

logger = get_logger('StopLimitOrders')


def execute_stop_limit_order(symbol: str, side: str, quantity: float,
                             stop_price: float, limit_price: float,
                             time_in_force: str = 'GTC') -> bool:
    """
    Execute a stop-limit order
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        side: Order side (BUY or SELL)
        quantity: Order quantity
        stop_price: Stop trigger price
        limit_price: Limit order price
        time_in_force: Time in force (GTC, IOC, FOK)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Validate inputs
        logger.info(f"Validating stop-limit order parameters...")
        symbol = Validator.validate_symbol(symbol)
        side = Validator.validate_side(side)
        quantity = Validator.validate_quantity(quantity)
        stop_price, limit_price = Validator.validate_stop_limit_prices(stop_price, limit_price, side)
        
        # Log order details
        logger.log_order('STOP-LIMIT', symbol, side, quantity,
                        stopPrice=stop_price, limitPrice=limit_price,
                        timeInForce=time_in_force)
        
        # Initialize client
        client = BinanceClient()
        
        # Get current price for comparison
        current_price = client.get_current_price(symbol)
        if current_price:
            logger.info(f"Current market price for {symbol}: {current_price}")
            
            stop_diff = ((stop_price - current_price) / current_price) * 100
            limit_diff = ((limit_price - current_price) / current_price) * 100
            
            logger.info(f"Stop price is {stop_diff:+.2f}% from current market price")
            logger.info(f"Limit price is {limit_diff:+.2f}% from current market price")
            
            # Provide guidance based on side
            if side == 'BUY':
                if stop_price < current_price:
                    logger.warning(
                        f"BUY stop-limit with stop price ({stop_price}) below current price ({current_price}). "
                        "This will trigger immediately!"
                    )
                else:
                    logger.info(
                        f"BUY stop-limit will trigger when price rises to {stop_price}, "
                        f"then place limit order at {limit_price}"
                    )
            else:  # SELL
                if stop_price > current_price:
                    logger.warning(
                        f"SELL stop-limit with stop price ({stop_price}) above current price ({current_price}). "
                        "This will trigger immediately!"
                    )
                else:
                    logger.info(
                        f"SELL stop-limit will trigger when price drops to {stop_price}, "
                        f"then place limit order at {limit_price}"
                    )
        
        # Execute order
        logger.info(f"Placing stop-limit order...")
        response = client.create_stop_limit_order(
            symbol, side, quantity, stop_price, limit_price, time_in_force
        )
        
        if response:
            order_id = response.get('orderId')
            status = response.get('status')
            orig_qty = response.get('origQty', quantity)
            
            logger.log_order_success('STOP-LIMIT', order_id, response)
            logger.info(f"Order Status: {status}")
            
            print(f"\n✓ Stop-limit order placed successfully!")
            print(f"  Order ID: {order_id}")
            print(f"  Symbol: {symbol}")
            print(f"  Side: {side}")
            print(f"  Quantity: {orig_qty}")
            print(f"  Stop Price: {stop_price}")
            print(f"  Limit Price: {limit_price}")
            print(f"  Status: {status}")
            print(f"  Time in Force: {time_in_force}")
            
            if current_price:
                print(f"\n  Current Market Price: {current_price}")
                print(f"  Stop Price Difference: {stop_diff:+.2f}%")
                print(f"  Limit Price Difference: {limit_diff:+.2f}%")
            
            print(f"\n  How it works:")
            if side == 'BUY':
                print(f"  1. When market price reaches {stop_price} (stop price)")
                print(f"  2. A limit BUY order will be placed at {limit_price}")
                print(f"  3. Order fills when market price drops to {limit_price}")
            else:
                print(f"  1. When market price drops to {stop_price} (stop price)")
                print(f"  2. A limit SELL order will be placed at {limit_price}")
                print(f"  3. Order fills when market price rises to {limit_price}")
            
            return True
        else:
            logger.log_order_error('STOP-LIMIT', 'Order placement failed')
            print("\n✗ Stop-limit order failed. Check bot.log for details.")
            return False
            
    except ValidationError as e:
        logger.log_order_error('STOP-LIMIT', f"Validation error: {str(e)}")
        print(f"\n✗ Validation Error: {str(e)}")
        return False
    except Exception as e:
        logger.log_order_error('STOP-LIMIT', f"Unexpected error: {str(e)}", exc_info=True)
        print(f"\n✗ Error: {str(e)}")
        return False


def main():
    """Main entry point for CLI"""
    if len(sys.argv) < 6 or len(sys.argv) > 7:
        print("Usage: python src/advanced/stop_limit.py <SYMBOL> <SIDE> <QUANTITY> <STOP_PRICE> <LIMIT_PRICE> [TIME_IN_FORCE]")
        print("\nExamples:")
        print("  # Buy when price rises to 41000, with limit at 41100")
        print("  python src/advanced/stop_limit.py BTCUSDT BUY 0.01 41000 41100")
        print("\n  # Sell when price drops to 39000, with limit at 38900")
        print("  python src/advanced/stop_limit.py BTCUSDT SELL 0.01 39000 38900")
        print("\nParameters:")
        print("  SYMBOL        - Trading pair (e.g., BTCUSDT, ETHUSDT)")
        print("  SIDE          - BUY or SELL")
        print("  QUANTITY      - Order quantity")
        print("  STOP_PRICE    - Price that triggers the limit order")
        print("  LIMIT_PRICE   - Limit order price after trigger")
        print("  TIME_IN_FORCE - Optional: GTC (default), IOC, or FOK")
        print("\nUse Cases:")
        print("  BUY Stop-Limit:  Enter position when price breaks above resistance")
        print("  SELL Stop-Limit: Stop-loss to limit losses on a long position")
        sys.exit(1)
    
    symbol = sys.argv[1]
    side = sys.argv[2]
    
    try:
        quantity = float(sys.argv[3])
        stop_price = float(sys.argv[4])
        limit_price = float(sys.argv[5])
    except ValueError as e:
        print(f"✗ Error: Numeric parameters must be valid numbers")
        print(f"  {str(e)}")
        sys.exit(1)
    
    time_in_force = sys.argv[6].upper() if len(sys.argv) == 7 else 'GTC'
    
    # Validate time in force
    valid_tif = ['GTC', 'IOC', 'FOK']
    if time_in_force not in valid_tif:
        print(f"✗ Error: TIME_IN_FORCE must be one of {valid_tif}, got '{time_in_force}'")
        sys.exit(1)
    
    # Display order summary
    print("\n" + "="*60)
    print("STOP-LIMIT ORDER PLACEMENT")
    print("="*60)
    print(f"Symbol:        {symbol}")
    print(f"Side:          {side}")
    print(f"Quantity:      {quantity}")
    print(f"Stop Price:    {stop_price}")
    print(f"Limit Price:   {limit_price}")
    print(f"Time in Force: {time_in_force}")
    print("="*60)
    print("\nPlacing order...\n")
    
    # Execute order
    success = execute_stop_limit_order(
        symbol, side, quantity, stop_price, limit_price, time_in_force
    )
    
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
