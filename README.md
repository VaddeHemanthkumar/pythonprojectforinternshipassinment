# Binance Futures Trading Bot

A CLI-based automated trading bot for Binance USDT-M Futures with support for multiple order types.

## Author
**Hemanth Kumar**  
Internship Project - January 2026

## Overview

This project was developed as part of my internship assignment to create a comprehensive trading bot for Binance Futures. The bot supports both basic and advanced order types with robust error handling and logging.

### What I Built

During this internship, I implemented:
- Core order types (Market & Limit orders)
- Advanced trading strategies (Stop-Limit, OCO, TWAP, Grid)
- Input validation system
- Comprehensive logging
- CLI interface

## Features

### Core Orders
- **Market Orders** - Execute trades immediately at current market price
- **Limit Orders** - Place orders at specific price levels

### Advanced Orders
- **Stop-Limit Orders** - Trigger limit orders when stop price is reached
- **OCO (One-Cancels-the-Other)** - Simultaneous take-profit and stop-loss orders
- **TWAP Strategy** - Time-Weighted Average Price execution for large orders
- **Grid Trading** - Automated buy-low/sell-high within price ranges

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API credentials
cp .env.example .env
# Edit .env with your Binance API keys
```

## Configuration

Get your API keys from [Binance Futures Testnet](https://testnet.binancefuture.com/)

Edit `.env`:
```
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
BINANCE_TESTNET=True
```

## Usage

### Market Orders
```bash
python -m src.market_orders BTCUSDT BUY 0.002
```

### Limit Orders
```bash
python -m src.limit_orders BTCUSDT BUY 0.002 90000
```

### Advanced Orders
```bash
# Stop-Limit
python -m src.advanced.stop_limit BTCUSDT SELL 0.002 89000 88900

# OCO
python -m src.advanced.oco BTCUSDT SELL 0.002 95000 88000 87900

# TWAP
python -m src.advanced.twap BTCUSDT BUY 0.01 5 10

# Grid Trading
python -m src.advanced.grid BTCUSDT 88000 94000 5 0.002
```

## Project Structure

```
src/
├── config.py           # Configuration management
├── logger.py           # Logging system
├── validator.py        # Input validation
├── binance_client.py   # API wrapper
├── market_orders.py    # Market order implementation
├── limit_orders.py     # Limit order implementation
└── advanced/
    ├── stop_limit.py   # Stop-limit orders
    ├── oco.py          # OCO orders
    ├── twap.py         # TWAP strategy
    └── grid.py         # Grid trading
```

## Development Notes

### Challenges Faced

1. **Minimum Order Size**: Initially struggled with Binance's $100 minimum order requirement. Learned to calculate proper quantities based on current prices.

2. **Precision Handling**: Had to implement proper decimal precision for different trading pairs (e.g., BTCUSDT requires max 3 decimal places).

3. **Error Handling**: Spent time implementing comprehensive error handling for API failures, network issues, and validation errors.

4. **Logging System**: Designed a structured logging system that logs to both file and console with different verbosity levels.

## Testing

Tested on Binance Futures Testnet with various scenarios:
- ✅ All order types working
- ✅ Input validation functioning correctly
- ✅ Error handling tested with invalid inputs
- ✅ Logging captures all activities

```bash
# Run installation test
python test_installation.py
```

## Lessons Learned

- Understanding Binance Futures API requirements and limitations
- Importance of input validation in financial applications
- Proper error handling and logging practices
- Working with real-time market data
- Implementing trading strategies programmatically

## Known Limitations

- OCO orders require manual monitoring (Binance Futures API limitation)
- Grid trading doesn't auto-replace filled orders (future enhancement)
- Minimum order value of $100 USDT required by Binance

## Future Improvements

- Add WebSocket support for real-time updates
- Implement position tracking and P&L calculation
- Add email/Telegram notifications
- Create web dashboard for monitoring
- Add backtesting capabilities

## Dependencies

- `python-binance` - Official Binance API wrapper
- `python-dotenv` - Environment variable management
- `requests` - HTTP library

## Safety & Disclaimer

⚠️ **Important**: 
- Always test on testnet first
- Never share your API keys
- Only trade with funds you can afford to lose
- This is an educational project

## Resources

- [Binance Futures API Documentation](https://binance-docs.github.io/apidocs/futures/en/)
- [Binance Testnet](https://testnet.binancefuture.com/)
- [python-binance Documentation](https://python-binance.readthedocs.io/)

## License

This project was created for educational purposes as part of an internship assignment.

## Acknowledgments

- Binance for providing comprehensive API documentation
- python-binance library maintainers
- My internship supervisor for guidance

---

**Note**: This project demonstrates practical implementation of trading algorithms and API integration. All testing was done on Binance Testnet with no real funds at risk.

*Last Updated: January 2026*
