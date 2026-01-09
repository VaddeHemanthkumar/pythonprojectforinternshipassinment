"""
Test script to verify bot installation and configuration
"""

import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("Testing package imports...")
    
    try:
        import binance
        print("  ✓ python-binance installed")
    except ImportError:
        print("  ✗ python-binance NOT installed")
        return False
    
    try:
        import dotenv
        print("  ✓ python-dotenv installed")
    except ImportError:
        print("  ✗ python-dotenv NOT installed")
        return False
    
    try:
        import requests
        print("  ✓ requests installed")
    except ImportError:
        print("  ✗ requests NOT installed")
        return False
    
    return True


def test_env_file():
    """Test if .env file exists and has required variables"""
    print("\nTesting environment configuration...")
    
    if not os.path.exists('.env'):
        print("  ✗ .env file not found")
        print("    Run: cp .env.example .env")
        print("    Then edit .env with your API credentials")
        return False
    
    print("  ✓ .env file exists")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or api_key == 'your_api_key_here':
        print("  ✗ BINANCE_API_KEY not configured")
        return False
    
    print("  ✓ BINANCE_API_KEY configured")
    
    if not api_secret or api_secret == 'your_api_secret_here':
        print("  ✗ BINANCE_API_SECRET not configured")
        return False
    
    print("  ✓ BINANCE_API_SECRET configured")
    
    testnet = os.getenv('BINANCE_TESTNET', 'True')
    if testnet.lower() == 'true':
        print("  ✓ Using TESTNET (safe for testing)")
    else:
        print("  ⚠ Using PRODUCTION (real money!)")
    
    return True


def test_modules():
    """Test if all bot modules can be imported"""
    print("\nTesting bot modules...")
    
    try:
        from src import config
        print("  ✓ config module")
    except ImportError as e:
        print(f"  ✗ config module: {e}")
        return False
    
    try:
        from src import logger
        print("  ✓ logger module")
    except ImportError as e:
        print(f"  ✗ logger module: {e}")
        return False
    
    try:
        from src import validator
        print("  ✓ validator module")
    except ImportError as e:
        print(f"  ✗ validator module: {e}")
        return False
    
    try:
        from src import binance_client
        print("  ✓ binance_client module")
    except ImportError as e:
        print(f"  ✗ binance_client module: {e}")
        return False
    
    try:
        from src import market_orders
        print("  ✓ market_orders module")
    except ImportError as e:
        print(f"  ✗ market_orders module: {e}")
        return False
    
    try:
        from src import limit_orders
        print("  ✓ limit_orders module")
    except ImportError as e:
        print(f"  ✗ limit_orders module: {e}")
        return False
    
    try:
        from src.advanced import stop_limit
        print("  ✓ stop_limit module")
    except ImportError as e:
        print(f"  ✗ stop_limit module: {e}")
        return False
    
    try:
        from src.advanced import oco
        print("  ✓ oco module")
    except ImportError as e:
        print(f"  ✗ oco module: {e}")
        return False
    
    try:
        from src.advanced import twap
        print("  ✓ twap module")
    except ImportError as e:
        print(f"  ✗ twap module: {e}")
        return False
    
    try:
        from src.advanced import grid
        print("  ✓ grid module")
    except ImportError as e:
        print(f"  ✗ grid module: {e}")
        return False
    
    return True


def test_api_connection():
    """Test API connection (if credentials are configured)"""
    print("\nTesting API connection...")
    
    try:
        from src.binance_client import BinanceClient
        from src.config import Config
        
        # Only test if credentials are configured
        if not Config.API_KEY or Config.API_KEY == 'your_api_key_here':
            print("  ⊘ Skipped (API credentials not configured)")
            return True
        
        client = BinanceClient()
        print("  ✓ API connection successful")
        
        # Try to get BTC price
        price = client.get_current_price('BTCUSDT')
        if price:
            print(f"  ✓ Current BTC price: ${price:,.2f}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ API connection failed: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("BINANCE FUTURES BOT - INSTALLATION TEST")
    print("="*60)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
        print("\n⚠ Please install required packages:")
        print("  pip install -r requirements.txt")
    
    # Test environment
    if not test_env_file():
        all_passed = False
    
    # Test modules
    if not test_modules():
        all_passed = False
    
    # Test API connection
    if not test_api_connection():
        all_passed = False
    
    # Summary
    print("\n" + "="*60)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        print("="*60)
        print("\nYour bot is ready to use!")
        print("\nNext steps:")
        print("  1. Review the README.md for usage examples")
        print("  2. Start with testnet (BINANCE_TESTNET=True)")
        print("  3. Try a simple market order:")
        print("     python src/market_orders.py BTCUSDT BUY 0.001")
    else:
        print("✗ SOME TESTS FAILED")
        print("="*60)
        print("\nPlease fix the issues above before using the bot.")
    
    print()
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
