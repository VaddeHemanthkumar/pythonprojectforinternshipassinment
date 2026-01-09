# Binance Futures Order Bot

## Internship Assignment Submission

**Submitted By:** Hemanth Kumar  
**Submission Date:** January 9, 2026  
**Assignment:** Binance Futures Order Bot - CLI Trading Application  
**Duration:** 5 days (~22 hours)  

---

## Assignment Overview

This project was developed as part of my internship assignment to create a comprehensive CLI-based trading bot for Binance USDT-M Futures. The assignment required implementing both core order types and advanced trading strategies with robust validation, error handling, and logging.

### Assignment Requirements Met

✅ **Core Orders (Mandatory - 50%)**
- Market Orders with validation
- Limit Orders with validation

✅ **Advanced Orders (Bonus - 30%)**
- Stop-Limit Orders
- OCO (One-Cancels-the-Other) Orders
- TWAP (Time-Weighted Average Price) Strategy
- Grid Trading Strategy

✅ **Validation & Logging (10%)**
- Comprehensive input validation
- Structured logging with timestamps
- Error tracking and handling

✅ **Documentation & Report (10%)**
- Complete README.md
- Technical implementation details
- Usage examples and testing results

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

### 🎯 Interactive CLI Interface (Easiest - ⭐ Recommended)

**The easiest and most user-friendly way to use the bot!**

```bash
python -m src.cli_interface
```

**Why use the Interactive CLI?**
- 📊 **Menu-driven interface** - No commands to remember
- 💰 **Guided order entry** - Step-by-step prompts for Market & Limit orders
- 📈 **Real-time prices** - View current prices for multiple symbols
- 📋 **Log viewer** - Check recent activity without opening files
- ✅ **Order confirmation** - Review before execution
- 💡 **Smart hints** - Automatic minimum quantity calculations
- 🎓 **Perfect for beginners** - Learn as you trade!

**Example Flow:**
1. Run `python -m src.cli_interface`
2. Select option (e.g., 1 for Market Order)
3. Choose symbol (e.g., BTCUSDT)
4. Choose side (BUY or SELL)
5. Enter quantity
6. Confirm and execute!

**Screenshot:**
```
📊 MAIN MENU
----------------------------------------------------------------------
  1. Market Order (Buy/Sell at current price)
  2. Limit Order (Buy/Sell at specific price)
  3. Stop-Limit Order (Advanced)
  4. OCO Order (Take-Profit + Stop-Loss)
  5. TWAP Strategy (Split large orders)
  6. Grid Trading (Automated range trading)
----------------------------------------------------------------------
  7. View Current Prices
  8. Check Account Balance
  9. View Recent Logs
  0. Exit
----------------------------------------------------------------------
```

---

### Command Line Usage

For advanced users or automation, use direct commands:

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

---

## Submission Summary

### Project Completion Status

| Requirement | Status | Implementation |
|------------|--------|----------------|
| Market Orders | ✅ Complete | Fully functional with validation |
| Limit Orders | ✅ Complete | Supports GTC, IOC, FOK |
| Stop-Limit Orders | ✅ Complete | Bonus feature implemented |
| OCO Orders | ✅ Complete | Bonus feature implemented |
| TWAP Strategy | ✅ Complete | Bonus feature implemented |
| Grid Trading | ✅ Complete | Bonus feature implemented |
| Input Validation | ✅ Complete | Comprehensive validation |
| Error Handling | ✅ Complete | Robust error management |
| Logging System | ✅ Complete | Structured logs with timestamps |
| Documentation | ✅ Complete | README with examples |

### Testing Results

**Test Environment:** Binance Futures Testnet  
**Test Date:** January 9, 2026  
**All Tests:** ✅ PASSED

**Sample Successful Order:**
- Order Type: Market Order
- Symbol: BTCUSDT
- Side: BUY
- Quantity: 0.002 BTC
- Order ID: 11530883024
- Status: Successfully Executed

### Time Investment

- **Day 1-2:** Setup, core orders (10 hours)
- **Day 3-4:** Advanced orders (8 hours)
- **Day 5:** Testing, documentation (4 hours)
- **Total:** ~22 hours

### Key Achievements

1. ✅ Implemented all mandatory features (100%)
2. ✅ Implemented all bonus features (100%)
3. ✅ Comprehensive error handling and validation
4. ✅ Production-quality code structure
5. ✅ Detailed documentation and examples
6. ✅ Successfully tested on Binance Testnet

### Submission Contents

**Code Files:**
- 6 order type implementations
- 4 core modules (config, logger, validator, client)
- Complete test suite

**Documentation:**
- README.md (this file)
- Code comments and docstrings
- Usage examples

**Configuration:**
- .env.example template
- requirements.txt
- .gitignore

---

**Submitted By:** Hemanth Kumar  
**Date:** January 9, 2026  
**Status:** Ready for Evaluation

*This internship assignment demonstrates proficiency in Python, API integration, error handling, and software development best practices.*

