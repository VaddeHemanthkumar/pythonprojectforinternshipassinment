"""
Enhanced CLI Interface for Binance Futures Trading Bot
Interactive menu-based interface for easier trading

Author: Hemanth Kumar
Date: January 2026
"""

import sys
import os
from src.market_orders import execute_market_order
from src.limit_orders import execute_limit_order
from src.binance_client import BinanceClient
from src.logger import get_logger

logger = get_logger('CLI_Interface')


class TradingBotCLI:
    """Interactive CLI interface for the trading bot"""
    
    def __init__(self):
        """Initialize the CLI interface"""
        self.client = None
        self.current_prices = {}
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print application header"""
        print("\n" + "="*70)
        print("           BINANCE FUTURES TRADING BOT - INTERACTIVE CLI")
        print("="*70)
        print("                    By: Hemanth Kumar")
        print("="*70 + "\n")
    
    def print_menu(self):
        """Display main menu"""
        print("\n📊 MAIN MENU")
        print("-" * 70)
        print("  1. Market Order (Buy/Sell at current price)")
        print("  2. Limit Order (Buy/Sell at specific price)")
        print("  3. Stop-Limit Order (Advanced)")
        print("  4. OCO Order (Take-Profit + Stop-Loss)")
        print("  5. TWAP Strategy (Split large orders)")
        print("  6. Grid Trading (Automated range trading)")
        print("-" * 70)
        print("  7. View Current Prices")
        print("  8. Check Account Balance")
        print("  9. View Recent Logs")
        print("  0. Exit")
        print("-" * 70)
    
    def get_input(self, prompt, input_type=str, default=None):
        """Get validated input from user"""
        while True:
            try:
                value = input(f"{prompt}: ").strip()
                if not value and default is not None:
                    return default
                if input_type == float:
                    return float(value)
                elif input_type == int:
                    return int(value)
                else:
                    return value
            except ValueError:
                print(f"❌ Invalid input. Please enter a valid {input_type.__name__}.")
    
    def get_symbol(self):
        """Get trading symbol from user"""
        print("\n📈 Common Symbols:")
        print("  1. BTCUSDT  2. ETHUSDT  3. BNBUSDT  4. SOLUSDT")
        
        choice = self.get_input("\nEnter symbol number or full symbol (e.g., BTCUSDT)")
        
        symbol_map = {
            '1': 'BTCUSDT',
            '2': 'ETHUSDT',
            '3': 'BNBUSDT',
            '4': 'SOLUSDT'
        }
        
        return symbol_map.get(choice, choice.upper())
    
    def get_side(self):
        """Get order side from user"""
        print("\n📊 Order Side:")
        print("  1. BUY")
        print("  2. SELL")
        
        choice = self.get_input("Select (1 or 2)")
        return 'BUY' if choice == '1' else 'SELL'
    
    def market_order_flow(self):
        """Handle market order flow"""
        self.clear_screen()
        self.print_header()
        print("💰 MARKET ORDER")
        print("="*70)
        
        symbol = self.get_symbol()
        side = self.get_side()
        
        # Show current price
        if not self.client:
            self.client = BinanceClient()
        
        current_price = self.client.get_current_price(symbol)
        if current_price:
            print(f"\n📊 Current {symbol} price: ${current_price:,.2f}")
            min_qty = 100 / current_price
            print(f"💡 Minimum quantity: {min_qty:.4f} (for $100 order)")
        
        quantity = self.get_input("\nEnter quantity", float)
        
        # Confirm order
        print("\n" + "="*70)
        print("ORDER CONFIRMATION")
        print("="*70)
        print(f"  Type:     MARKET ORDER")
        print(f"  Symbol:   {symbol}")
        print(f"  Side:     {side}")
        print(f"  Quantity: {quantity}")
        if current_price:
            print(f"  Est. Value: ${quantity * current_price:,.2f} USDT")
        print("="*70)
        
        confirm = self.get_input("\nConfirm order? (yes/no)", default='no')
        
        if confirm.lower() in ['yes', 'y']:
            print("\n⏳ Executing order...")
            success = execute_market_order(symbol, side, quantity)
            
            if success:
                print("\n✅ Order executed successfully!")
            else:
                print("\n❌ Order failed. Check bot.log for details.")
        else:
            print("\n❌ Order cancelled.")
        
        input("\nPress Enter to continue...")
    
    def limit_order_flow(self):
        """Handle limit order flow"""
        self.clear_screen()
        self.print_header()
        print("📝 LIMIT ORDER")
        print("="*70)
        
        symbol = self.get_symbol()
        side = self.get_side()
        
        # Show current price
        if not self.client:
            self.client = BinanceClient()
        
        current_price = self.client.get_current_price(symbol)
        if current_price:
            print(f"\n📊 Current {symbol} price: ${current_price:,.2f}")
        
        price = self.get_input("\nEnter limit price", float)
        quantity = self.get_input("Enter quantity", float)
        
        # Confirm order
        print("\n" + "="*70)
        print("ORDER CONFIRMATION")
        print("="*70)
        print(f"  Type:     LIMIT ORDER")
        print(f"  Symbol:   {symbol}")
        print(f"  Side:     {side}")
        print(f"  Quantity: {quantity}")
        print(f"  Price:    ${price:,.2f}")
        print(f"  Value:    ${quantity * price:,.2f} USDT")
        if current_price:
            diff = ((price - current_price) / current_price) * 100
            print(f"  Diff:     {diff:+.2f}% from current price")
        print("="*70)
        
        confirm = self.get_input("\nConfirm order? (yes/no)", default='no')
        
        if confirm.lower() in ['yes', 'y']:
            print("\n⏳ Placing order...")
            success = execute_limit_order(symbol, side, quantity, price)
            
            if success:
                print("\n✅ Order placed successfully!")
            else:
                print("\n❌ Order failed. Check bot.log for details.")
        else:
            print("\n❌ Order cancelled.")
        
        input("\nPress Enter to continue...")
    
    def view_prices(self):
        """View current market prices"""
        self.clear_screen()
        self.print_header()
        print("📊 CURRENT MARKET PRICES")
        print("="*70)
        
        if not self.client:
            self.client = BinanceClient()
        
        symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT']
        
        print(f"\n{'Symbol':<15} {'Price':<20} {'Min Quantity':<15}")
        print("-" * 70)
        
        for symbol in symbols:
            price = self.client.get_current_price(symbol)
            if price:
                min_qty = 100 / price
                print(f"{symbol:<15} ${price:>15,.2f}    {min_qty:>10.4f}")
        
        print("-" * 70)
        print("\n💡 Minimum order value: $100 USDT")
        
        input("\nPress Enter to continue...")
    
    def view_logs(self):
        """View recent log entries"""
        self.clear_screen()
        self.print_header()
        print("📋 RECENT LOGS (Last 20 lines)")
        print("="*70 + "\n")
        
        try:
            with open('bot.log', 'r', encoding='utf-8') as f:
                lines = f.readlines()
                recent_lines = lines[-20:] if len(lines) > 20 else lines
                for line in recent_lines:
                    print(line.rstrip())
        except FileNotFoundError:
            print("No log file found. Execute an order first to generate logs.")
        
        input("\n\nPress Enter to continue...")
    
    def run(self):
        """Run the interactive CLI"""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_menu()
            
            choice = self.get_input("\nSelect an option (0-9)")
            
            if choice == '1':
                self.market_order_flow()
            elif choice == '2':
                self.limit_order_flow()
            elif choice == '3':
                print("\n⚠️  Stop-Limit orders: Use command line")
                print("   python -m src.advanced.stop_limit BTCUSDT SELL 0.002 89000 88900")
                input("\nPress Enter to continue...")
            elif choice == '4':
                print("\n⚠️  OCO orders: Use command line")
                print("   python -m src.advanced.oco BTCUSDT SELL 0.002 95000 88000 87900")
                input("\nPress Enter to continue...")
            elif choice == '5':
                print("\n⚠️  TWAP strategy: Use command line")
                print("   python -m src.advanced.twap BTCUSDT BUY 0.01 5 10")
                input("\nPress Enter to continue...")
            elif choice == '6':
                print("\n⚠️  Grid trading: Use command line")
                print("   python -m src.advanced.grid BTCUSDT 88000 94000 5 0.002")
                input("\nPress Enter to continue...")
            elif choice == '7':
                self.view_prices()
            elif choice == '8':
                print("\n⚠️  Account balance: Feature coming soon")
                input("\nPress Enter to continue...")
            elif choice == '9':
                self.view_logs()
            elif choice == '0':
                print("\n👋 Thank you for using Binance Futures Trading Bot!")
                print("="*70 + "\n")
                sys.exit(0)
            else:
                print("\n❌ Invalid option. Please try again.")
                input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    try:
        cli = TradingBotCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        logger.error(f"CLI Error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
