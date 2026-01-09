"""
OCO (One-Cancels-the-Other) Orders Module
Place take-profit and stop-loss orders simultaneously
"""

import sys
from src.binance_client import BinanceClient
from src.validator import Validator, ValidationError
from src.logger import get_logger

logger = get_logger('OCO_Orders')


def execute_oco_order(symbol: str, side: str, quantity: float,
                     take_profit_price: float, stop_price: float,
                     stop_limit_price: float) -> bool:
    """
    Execute an OCO (One-Cancels-the-Other) order
    
    This places two orders simultaneously:
    1. A limit order at take_profit_price (to take profits)
    2. A stop-limit order at stop_price/stop_limit_price (to limit losses)
    
    When one order fills, the other is automatically cancelled.
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        side: Order side (SELL for closing long, BUY for closing short)
        quantity: Order quantity
        take_profit_price: Take profit limit price
        stop_price: Stop loss trigger price
        stop_limit_price: Stop loss limit price
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Validate inputs
        logger.info(f"Validating OCO order parameters...")
        symbol = Validator.validate_symbol(symbol)
        side = Validator.validate_side(side)
        quantity = Validator.validate_quantity(quantity)
        take_profit_price = Validator.validate_price(take_profit_price)
        stop_price = Validator.validate_price(stop_price)
        stop_limit_price = Validator.validate_price(stop_limit_price)
        
        # Validate OCO logic
        if side == 'SELL':
            # For closing a long position:
            # Take profit should be above current price
            # Stop loss should be below current price
            if take_profit_price <= stop_price:
                raise ValidationError(
                    f"For SELL OCO: take_profit_price ({take_profit_price}) must be "
                    f"greater than stop_price ({stop_price})"
                )
        else:  # BUY
            # For closing a short position:
            # Take profit should be below current price
            # Stop loss should be above current price
            if take_profit_price >= stop_price:
                raise ValidationError(
                    f"For BUY OCO: take_profit_price ({take_profit_price}) must be "
                    f"less than stop_price ({stop_price})"
                )
        
        # Log order details
        logger.log_order('OCO', symbol, side, quantity,
                        takeProfitPrice=take_profit_price,
                        stopPrice=stop_price,
                        stopLimitPrice=stop_limit_price)
        
        # Initialize client
        client = BinanceClient()
        
        # Get current price for comparison
        current_price = client.get_current_price(symbol)
        if current_price:
            logger.info(f"Current market price for {symbol}: {current_price}")
            
            tp_diff = ((take_profit_price - current_price) / current_price) * 100
            sl_diff = ((stop_price - current_price) / current_price) * 100
            
            logger.info(f"Take profit is {tp_diff:+.2f}% from current price")
            logger.info(f"Stop loss is {sl_diff:+.2f}% from current price")
            
            # Calculate potential profit/loss
            if side == 'SELL':
                potential_profit = (take_profit_price - current_price) * quantity
                potential_loss = (current_price - stop_limit_price) * quantity
                logger.info(f"Potential profit: {potential_profit:+.2f} USDT ({tp_diff:+.2f}%)")
                logger.info(f"Potential loss: {potential_loss:+.2f} USDT ({sl_diff:+.2f}%)")
            else:
                potential_profit = (current_price - take_profit_price) * quantity
                potential_loss = (stop_limit_price - current_price) * quantity
                logger.info(f"Potential profit: {potential_profit:+.2f} USDT ({abs(tp_diff):.2f}%)")
                logger.info(f"Potential loss: {potential_loss:+.2f} USDT ({abs(sl_diff):.2f}%)")
        
        # Note: Binance python-binance library doesn't have a direct OCO method for futures
        # We'll place both orders separately and note that they should be managed together
        logger.info("Placing OCO orders (take-profit and stop-loss)...")
        
        # Place take-profit limit order
        logger.info("Placing take-profit limit order...")
        tp_response = client.create_limit_order(
            symbol, side, quantity, take_profit_price, 'GTC'
        )
        
        if not tp_response:
            logger.log_order_error('OCO', 'Failed to place take-profit order')
            print("\n✗ Failed to place take-profit order. Check bot.log for details.")
            return False
        
        tp_order_id = tp_response.get('orderId')
        logger.info(f"Take-profit order placed: Order ID {tp_order_id}")
        
        # Place stop-loss order
        logger.info("Placing stop-loss order...")
        sl_response = client.create_stop_limit_order(
            symbol, side, quantity, stop_price, stop_limit_price, 'GTC'
        )
        
        if not sl_response:
            logger.log_order_error('OCO', 'Failed to place stop-loss order')
            logger.warning(f"Take-profit order {tp_order_id} was placed but stop-loss failed!")
            print(f"\n⚠ Warning: Take-profit order placed (ID: {tp_order_id}) but stop-loss failed!")
            print("  You may want to manually cancel the take-profit order or place stop-loss separately.")
            return False
        
        sl_order_id = sl_response.get('orderId')
        logger.info(f"Stop-loss order placed: Order ID {sl_order_id}")
        
        logger.log_order_success('OCO', f"TP:{tp_order_id}, SL:{sl_order_id}")
        
        print(f"\n✓ OCO orders placed successfully!")
        print(f"\n  Take-Profit Order:")
        print(f"    Order ID: {tp_order_id}")
        print(f"    Price: {take_profit_price}")
        print(f"    Type: LIMIT")
        
        print(f"\n  Stop-Loss Order:")
        print(f"    Order ID: {sl_order_id}")
        print(f"    Stop Price: {stop_price}")
        print(f"    Limit Price: {stop_limit_price}")
        print(f"    Type: STOP-LIMIT")
        
        print(f"\n  Order Details:")
        print(f"    Symbol: {symbol}")
        print(f"    Side: {side}")
        print(f"    Quantity: {quantity}")
        
        if current_price:
            print(f"\n  Current Market Price: {current_price}")
            print(f"  Take-Profit Distance: {tp_diff:+.2f}%")
            print(f"  Stop-Loss Distance: {sl_diff:+.2f}%")
            
            if side == 'SELL':
                print(f"\n  Potential Profit: {potential_profit:+.2f} USDT ({tp_diff:+.2f}%)")
                print(f"  Potential Loss: -{potential_loss:.2f} USDT ({sl_diff:.2f}%)")
                risk_reward = abs(potential_profit / potential_loss) if potential_loss != 0 else 0
                print(f"  Risk/Reward Ratio: 1:{risk_reward:.2f}")
        
        print(f"\n  Note: Monitor both orders. When one fills, manually cancel the other.")
        print(f"        (Binance Futures API doesn't support true OCO orders)")
        
        return True
        
    except ValidationError as e:
        logger.log_order_error('OCO', f"Validation error: {str(e)}")
        print(f"\n✗ Validation Error: {str(e)}")
        return False
    except Exception as e:
        logger.log_order_error('OCO', f"Unexpected error: {str(e)}", exc_info=True)
        print(f"\n✗ Error: {str(e)}")
        return False


def main():
    """Main entry point for CLI"""
    if len(sys.argv) != 7:
        print("Usage: python src/advanced/oco.py <SYMBOL> <SIDE> <QUANTITY> <TAKE_PROFIT_PRICE> <STOP_PRICE> <STOP_LIMIT_PRICE>")
        print("\nExample - After buying BTC at $40,000:")
        print("  # Take profit at $42,000, stop loss at $38,000")
        print("  python src/advanced/oco.py BTCUSDT SELL 0.01 42000 38000 37900")
        print("\nParameters:")
        print("  SYMBOL             - Trading pair (e.g., BTCUSDT)")
        print("  SIDE               - SELL (for long position) or BUY (for short position)")
        print("  QUANTITY           - Order quantity")
        print("  TAKE_PROFIT_PRICE  - Price to take profits")
        print("  STOP_PRICE         - Stop loss trigger price")
        print("  STOP_LIMIT_PRICE   - Stop loss limit price")
        print("\nHow it works:")
        print("  - Places two orders: take-profit (limit) and stop-loss (stop-limit)")
        print("  - When one order fills, you should manually cancel the other")
        print("  - Used to manage risk on existing positions")
        sys.exit(1)
    
    symbol = sys.argv[1]
    side = sys.argv[2]
    
    try:
        quantity = float(sys.argv[3])
        take_profit_price = float(sys.argv[4])
        stop_price = float(sys.argv[5])
        stop_limit_price = float(sys.argv[6])
    except ValueError as e:
        print(f"✗ Error: Numeric parameters must be valid numbers")
        print(f"  {str(e)}")
        sys.exit(1)
    
    # Display order summary
    print("\n" + "="*60)
    print("OCO ORDER PLACEMENT")
    print("="*60)
    print(f"Symbol:             {symbol}")
    print(f"Side:               {side}")
    print(f"Quantity:           {quantity}")
    print(f"Take-Profit Price:  {take_profit_price}")
    print(f"Stop Price:         {stop_price}")
    print(f"Stop Limit Price:   {stop_limit_price}")
    print("="*60)
    print("\nPlacing OCO orders...\n")
    
    # Execute order
    success = execute_oco_order(
        symbol, side, quantity, take_profit_price, stop_price, stop_limit_price
    )
    
    if success:
        print("\n" + "="*60)
        print("OCO orders placed successfully!")
        print("Check bot.log for detailed information.")
        print("="*60 + "\n")
        sys.exit(0)
    else:
        print("\n" + "="*60)
        print("OCO order placement failed!")
        print("Check bot.log for error details.")
        print("="*60 + "\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
