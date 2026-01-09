"""
TWAP (Time-Weighted Average Price) Strategy Module
Split large orders into smaller chunks over time to minimize market impact
"""

import sys
import time
from datetime import datetime, timedelta
from src.binance_client import BinanceClient
from src.validator import Validator, ValidationError
from src.logger import get_logger

logger = get_logger('TWAP_Strategy')


def execute_twap_strategy(symbol: str, side: str, total_quantity: float,
                          num_orders: int, duration_minutes: int) -> bool:
    """
    Execute TWAP (Time-Weighted Average Price) strategy
    
    Splits a large order into smaller chunks and executes them evenly over time.
    This helps minimize market impact and achieve better average prices.
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        side: Order side (BUY or SELL)
        total_quantity: Total quantity to trade
        num_orders: Number of orders to split into
        duration_minutes: Duration to spread orders over (in minutes)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Validate inputs
        logger.info(f"Validating TWAP strategy parameters...")
        symbol = Validator.validate_symbol(symbol)
        side = Validator.validate_side(side)
        total_quantity = Validator.validate_quantity(total_quantity)
        num_orders, duration_minutes = Validator.validate_twap_params(num_orders, duration_minutes)
        
        # Calculate order parameters
        quantity_per_order = total_quantity / num_orders
        interval_seconds = (duration_minutes * 60) / num_orders
        
        logger.info(f"TWAP Strategy Configuration:")
        logger.info(f"  Total Quantity: {total_quantity}")
        logger.info(f"  Number of Orders: {num_orders}")
        logger.info(f"  Quantity per Order: {quantity_per_order}")
        logger.info(f"  Duration: {duration_minutes} minutes")
        logger.info(f"  Interval: {interval_seconds:.2f} seconds")
        
        # Validate quantity per order
        quantity_per_order = Validator.validate_quantity(quantity_per_order)
        
        # Initialize client
        client = BinanceClient()
        
        # Get current price
        current_price = client.get_current_price(symbol)
        if current_price:
            estimated_total_value = total_quantity * current_price
            logger.info(f"Current price: {current_price}")
            logger.info(f"Estimated total value: {estimated_total_value} USDT")
        
        # Track execution
        executed_orders = []
        total_executed_qty = 0
        total_value = 0
        start_time = datetime.now()
        estimated_end_time = start_time + timedelta(minutes=duration_minutes)
        
        print(f"\n{'='*60}")
        print(f"Starting TWAP execution...")
        print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Estimated end time: {estimated_end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Execute orders
        for i in range(num_orders):
            order_num = i + 1
            logger.info(f"Executing order {order_num}/{num_orders}...")
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Order {order_num}/{num_orders}")
            print(f"  Quantity: {quantity_per_order}")
            
            # Execute market order
            response = client.create_market_order(symbol, side, quantity_per_order)
            
            if response:
                order_id = response.get('orderId')
                executed_qty = float(response.get('executedQty', quantity_per_order))
                avg_price = float(response.get('avgPrice', 0)) if 'avgPrice' in response else current_price
                
                order_value = executed_qty * avg_price if avg_price else 0
                total_executed_qty += executed_qty
                total_value += order_value
                
                executed_orders.append({
                    'order_id': order_id,
                    'quantity': executed_qty,
                    'price': avg_price,
                    'value': order_value,
                    'timestamp': datetime.now()
                })
                
                logger.info(f"Order {order_num} executed: ID={order_id}, Qty={executed_qty}, Price={avg_price}")
                print(f"  ✓ Executed at {avg_price} (Order ID: {order_id})")
                
            else:
                logger.error(f"Order {order_num} failed to execute")
                print(f"  ✗ Execution failed")
                
                # Ask user if they want to continue
                if order_num < num_orders:
                    print(f"\n  Continue with remaining orders? (y/n): ", end='')
                    # For automated execution, we'll continue
                    logger.warning(f"Order {order_num} failed, continuing with remaining orders")
            
            # Wait before next order (except for the last one)
            if order_num < num_orders:
                print(f"  Waiting {interval_seconds:.1f} seconds until next order...")
                time.sleep(interval_seconds)
                print()
        
        # Calculate statistics
        end_time = datetime.now()
        actual_duration = (end_time - start_time).total_seconds() / 60
        average_price = total_value / total_executed_qty if total_executed_qty > 0 else 0
        
        logger.info(f"TWAP execution completed")
        logger.info(f"Total executed quantity: {total_executed_qty}/{total_quantity}")
        logger.info(f"Average execution price: {average_price}")
        logger.info(f"Total value: {total_value} USDT")
        logger.info(f"Actual duration: {actual_duration:.2f} minutes")
        
        # Display summary
        print(f"\n{'='*60}")
        print(f"TWAP EXECUTION SUMMARY")
        print(f"{'='*60}")
        print(f"Symbol:              {symbol}")
        print(f"Side:                {side}")
        print(f"Target Quantity:     {total_quantity}")
        print(f"Executed Quantity:   {total_executed_qty}")
        print(f"Completion:          {(total_executed_qty/total_quantity)*100:.2f}%")
        print(f"Number of Orders:    {len(executed_orders)}/{num_orders}")
        print(f"Average Price:       {average_price:.2f}")
        print(f"Total Value:         {total_value:.2f} USDT")
        print(f"Actual Duration:     {actual_duration:.2f} minutes")
        print(f"{'='*60}")
        
        if executed_orders:
            print(f"\nOrder Details:")
            for idx, order in enumerate(executed_orders, 1):
                print(f"  {idx}. ID: {order['order_id']}, "
                      f"Qty: {order['quantity']}, "
                      f"Price: {order['price']:.2f}, "
                      f"Time: {order['timestamp'].strftime('%H:%M:%S')}")
        
        print(f"\n{'='*60}\n")
        
        return len(executed_orders) > 0
        
    except ValidationError as e:
        logger.log_order_error('TWAP', f"Validation error: {str(e)}")
        print(f"\n✗ Validation Error: {str(e)}")
        return False
    except KeyboardInterrupt:
        logger.warning("TWAP execution interrupted by user")
        print(f"\n\n⚠ Execution interrupted by user")
        print(f"Executed {total_executed_qty}/{total_quantity} ({(total_executed_qty/total_quantity)*100:.2f}%)")
        return False
    except Exception as e:
        logger.log_order_error('TWAP', f"Unexpected error: {str(e)}", exc_info=True)
        print(f"\n✗ Error: {str(e)}")
        return False


def main():
    """Main entry point for CLI"""
    if len(sys.argv) != 6:
        print("Usage: python src/advanced/twap.py <SYMBOL> <SIDE> <TOTAL_QUANTITY> <NUM_ORDERS> <DURATION_MINUTES>")
        print("\nExamples:")
        print("  # Buy 1 BTC split into 10 orders over 60 minutes")
        print("  python src/advanced/twap.py BTCUSDT BUY 1.0 10 60")
        print("\n  # Sell 5 ETH split into 20 orders over 120 minutes")
        print("  python src/advanced/twap.py ETHUSDT SELL 5.0 20 120")
        print("\nParameters:")
        print("  SYMBOL           - Trading pair (e.g., BTCUSDT)")
        print("  SIDE             - BUY or SELL")
        print("  TOTAL_QUANTITY   - Total quantity to trade")
        print("  NUM_ORDERS       - Number of orders to split into (2-100)")
        print("  DURATION_MINUTES - Duration to spread orders over (1-1440)")
        print("\nBenefits:")
        print("  - Minimizes market impact for large orders")
        print("  - Achieves better average execution price")
        print("  - Reduces slippage")
        print("\nNote: Uses market orders, so execution is guaranteed but price varies")
        sys.exit(1)
    
    symbol = sys.argv[1]
    side = sys.argv[2]
    
    try:
        total_quantity = float(sys.argv[3])
        num_orders = int(sys.argv[4])
        duration_minutes = int(sys.argv[5])
    except ValueError as e:
        print(f"✗ Error: Invalid numeric parameters")
        print(f"  {str(e)}")
        sys.exit(1)
    
    # Display strategy summary
    quantity_per_order = total_quantity / num_orders
    interval_seconds = (duration_minutes * 60) / num_orders
    
    print("\n" + "="*60)
    print("TWAP STRATEGY EXECUTION")
    print("="*60)
    print(f"Symbol:             {symbol}")
    print(f"Side:               {side}")
    print(f"Total Quantity:     {total_quantity}")
    print(f"Number of Orders:   {num_orders}")
    print(f"Quantity per Order: {quantity_per_order}")
    print(f"Duration:           {duration_minutes} minutes")
    print(f"Interval:           {interval_seconds:.2f} seconds")
    print("="*60)
    print("\n⚠ This will execute market orders at regular intervals.")
    print("  Press Ctrl+C to stop execution at any time.\n")
    
    # Execute strategy
    success = execute_twap_strategy(
        symbol, side, total_quantity, num_orders, duration_minutes
    )
    
    if success:
        print("TWAP execution completed!")
        print("Check bot.log for detailed information.")
        sys.exit(0)
    else:
        print("TWAP execution failed or incomplete!")
        print("Check bot.log for error details.")
        sys.exit(1)


if __name__ == '__main__':
    main()
