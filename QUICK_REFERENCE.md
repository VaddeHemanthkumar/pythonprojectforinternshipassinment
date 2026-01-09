# Binance Futures Bot - Quick Reference Guide

## Quick Start (3 Steps)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
```bash
# Copy template
cp .env.example .env

# Edit .env and add your API credentials
# Get testnet keys from: https://testnet.binancefuture.com/
```

### 3. Test Installation
```bash
python test_installation.py
```

---

## Command Reference

### Market Orders
```bash
# Syntax
python src/market_orders.py <SYMBOL> <SIDE> <QUANTITY>

# Examples
python src/market_orders.py BTCUSDT BUY 0.01
python src/market_orders.py ETHUSDT SELL 0.1
```

### Limit Orders
```bash
# Syntax
python src/limit_orders.py <SYMBOL> <SIDE> <QUANTITY> <PRICE> [TIME_IN_FORCE]

# Examples
python src/limit_orders.py BTCUSDT BUY 0.01 40000
python src/limit_orders.py ETHUSDT SELL 0.1 3000 GTC
```

### Stop-Limit Orders
```bash
# Syntax
python src/advanced/stop_limit.py <SYMBOL> <SIDE> <QUANTITY> <STOP_PRICE> <LIMIT_PRICE>

# Examples
python src/advanced/stop_limit.py BTCUSDT BUY 0.01 41000 41100
python src/advanced/stop_limit.py BTCUSDT SELL 0.01 39000 38900
```

### OCO Orders
```bash
# Syntax
python src/advanced/oco.py <SYMBOL> <SIDE> <QUANTITY> <TP_PRICE> <STOP_PRICE> <STOP_LIMIT_PRICE>

# Example
python src/advanced/oco.py BTCUSDT SELL 0.01 42000 38000 37900
```

### TWAP Strategy
```bash
# Syntax
python src/advanced/twap.py <SYMBOL> <SIDE> <TOTAL_QTY> <NUM_ORDERS> <DURATION_MIN>

# Examples
python src/advanced/twap.py BTCUSDT BUY 1.0 10 60
python src/advanced/twap.py ETHUSDT SELL 5.0 20 120
```

### Grid Trading
```bash
# Syntax
python src/advanced/grid.py <SYMBOL> <LOWER_PRICE> <UPPER_PRICE> <LEVELS> <QTY_PER_LEVEL>

# Examples
python src/advanced/grid.py BTCUSDT 38000 42000 10 0.01
python src/advanced/grid.py ETHUSDT 2800 3200 20 0.1
```

---

## Common Symbols

| Symbol    | Description           |
|-----------|-----------------------|
| BTCUSDT   | Bitcoin / USDT        |
| ETHUSDT   | Ethereum / USDT       |
| BNBUSDT   | Binance Coin / USDT   |
| ADAUSDT   | Cardano / USDT        |
| DOGEUSDT  | Dogecoin / USDT       |
| XRPUSDT   | Ripple / USDT         |
| SOLUSDT   | Solana / USDT         |
| MATICUSDT | Polygon / USDT        |

---

## Order Types Explained

### Market Order
- **Executes:** Immediately at current price
- **Use When:** You want guaranteed execution
- **Risk:** Price slippage

### Limit Order
- **Executes:** Only at specified price or better
- **Use When:** You want price control
- **Risk:** May not fill

### Stop-Limit Order
- **Executes:** Limit order triggered at stop price
- **Use When:** Stop-loss or breakout entry
- **Risk:** May not fill in fast markets

### OCO (One-Cancels-Other)
- **Executes:** Two orders, one cancels the other when filled
- **Use When:** Managing risk on existing position
- **Risk:** Requires manual monitoring

### TWAP Strategy
- **Executes:** Splits order over time
- **Use When:** Large orders to minimize impact
- **Risk:** Price may move against you

### Grid Trading
- **Executes:** Multiple orders at price levels
- **Use When:** Range-bound markets
- **Risk:** Requires capital for all levels

---

## Time in Force Options

| Option | Description                    | Use Case                    |
|--------|--------------------------------|-----------------------------|
| GTC    | Good Till Cancel               | Default, stays until filled |
| IOC    | Immediate or Cancel            | Fill now or cancel          |
| FOK    | Fill or Kill                   | All or nothing              |

---

## Error Messages & Solutions

| Error                    | Solution                                      |
|--------------------------|-----------------------------------------------|
| "Invalid API key"        | Check .env file, verify API key               |
| "Insufficient balance"   | Deposit funds or reduce quantity              |
| "Symbol not found"       | Use valid USDT-M futures symbol               |
| "Validation error"       | Check parameter format and values             |
| "Connection timeout"     | Check internet and Binance API status         |

---

## File Locations

| File/Directory           | Purpose                                       |
|--------------------------|-----------------------------------------------|
| `src/market_orders.py`   | Market order execution                        |
| `src/limit_orders.py`    | Limit order execution                         |
| `src/advanced/`          | Advanced order types                          |
| `bot.log`                | Execution logs (created after first run)      |
| `.env`                   | API credentials (create from .env.example)    |
| `README.md`              | Full documentation                            |
| `REPORT.md`              | Technical report                              |

---

## Logging

All activities are logged to `bot.log`:
- Order placements
- API calls
- Errors and warnings
- Execution results

**View logs:**
```bash
# Windows
type bot.log

# Linux/Mac
cat bot.log

# View last 20 lines
Get-Content bot.log -Tail 20  # Windows
tail -20 bot.log              # Linux/Mac
```

---

## Safety Tips

1. **Always start with testnet** (BINANCE_TESTNET=True)
2. **Never commit .env file** to version control
3. **Use small quantities** when testing
4. **Monitor bot.log** for errors
5. **Set API key restrictions** (IP whitelist, no withdrawals)
6. **Test each order type** before live trading

---

## Getting Help

1. **Check bot.log** for detailed error messages
2. **Review README.md** for comprehensive documentation
3. **Read REPORT.md** for technical details
4. **Test with test_installation.py**
5. **Verify API credentials** in .env file

---

## Testnet Resources

- **Testnet URL:** https://testnet.binancefuture.com/
- **Get Testnet Funds:** Login and request from faucet
- **API Docs:** https://binance-docs.github.io/apidocs/futures/en/

---

## Quick Troubleshooting

```bash
# Test installation
python test_installation.py

# Check Python version (need 3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Verify .env file exists
ls .env  # Linux/Mac
dir .env # Windows

# Check if modules import correctly
python -c "from src import config; print('OK')"
```

---

## Performance Tips

1. **TWAP:** Use longer intervals for better prices
2. **Grid:** Set levels based on historical volatility
3. **OCO:** Calculate risk/reward ratio before placing
4. **Limit Orders:** Set realistic prices near market

---

## Advanced Usage

### Chain Multiple Orders
```bash
# Buy at market, then set stop-loss
python src/market_orders.py BTCUSDT BUY 0.01
python src/advanced/stop_limit.py BTCUSDT SELL 0.01 39000 38900
```

### Monitor Execution
```bash
# Run order in one terminal
python src/advanced/twap.py BTCUSDT BUY 1.0 10 60

# Watch logs in another terminal
Get-Content bot.log -Wait -Tail 10  # Windows
tail -f bot.log                     # Linux/Mac
```

---

## Project Structure

```
pythonprojectforinternship/
├── src/
│   ├── market_orders.py      # Market orders
│   ├── limit_orders.py       # Limit orders
│   ├── config.py             # Configuration
│   ├── logger.py             # Logging
│   ├── validator.py          # Validation
│   ├── binance_client.py     # API client
│   └── advanced/
│       ├── stop_limit.py     # Stop-limit orders
│       ├── oco.py            # OCO orders
│       ├── twap.py           # TWAP strategy
│       └── grid.py           # Grid trading
├── .env                      # Your API keys (create this)
├── .env.example              # Template
├── requirements.txt          # Dependencies
├── README.md                 # Full documentation
├── REPORT.md                 # Technical report
└── test_installation.py      # Installation test
```

---

**Quick Reference v1.0** | For full documentation see README.md
