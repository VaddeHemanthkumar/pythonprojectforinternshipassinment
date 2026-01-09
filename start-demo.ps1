# Binance Futures Trading Bot - Quick Demo
# This script shows all available commands

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "    BINANCE FUTURES TRADING BOT - STARTED!" -ForegroundColor Green
Write-Host "============================================================`n" -ForegroundColor Cyan

Write-Host "✅ Application Status: READY`n" -ForegroundColor Green

Write-Host "This is a CLI-based trading bot with 6 order types:`n" -ForegroundColor Yellow

# Show all available commands
Write-Host "📋 AVAILABLE COMMANDS:`n" -ForegroundColor Cyan

Write-Host "1️⃣  MARKET ORDERS (Immediate execution)" -ForegroundColor White
Write-Host "   python -m src.market_orders BTCUSDT BUY 0.01`n" -ForegroundColor Gray

Write-Host "2️⃣  LIMIT ORDERS (Specific price)" -ForegroundColor White
Write-Host "   python -m src.limit_orders BTCUSDT BUY 0.01 40000`n" -ForegroundColor Gray

Write-Host "3️⃣  STOP-LIMIT ORDERS (Triggered orders)" -ForegroundColor White
Write-Host "   python -m src.advanced.stop_limit BTCUSDT SELL 0.01 39000 38900`n" -ForegroundColor Gray

Write-Host "4️⃣  OCO ORDERS (Take-profit + Stop-loss)" -ForegroundColor White
Write-Host "   python -m src.advanced.oco BTCUSDT SELL 0.01 42000 38000 37900`n" -ForegroundColor Gray

Write-Host "5️⃣  TWAP STRATEGY (Split large orders)" -ForegroundColor White
Write-Host "   python -m src.advanced.twap BTCUSDT BUY 1.0 10 60`n" -ForegroundColor Gray

Write-Host "6️⃣  GRID TRADING (Automated range trading)" -ForegroundColor White
Write-Host "   python -m src.advanced.grid BTCUSDT 38000 42000 10 0.01`n" -ForegroundColor Gray

Write-Host "============================================================`n" -ForegroundColor Cyan

# Check if API keys are configured
Write-Host "⚙️  CONFIGURATION CHECK:`n" -ForegroundColor Cyan

if (Test-Path ".env") {
    Write-Host "   ✅ .env file exists" -ForegroundColor Green
    
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "your_api_key_here") {
        Write-Host "   ⚠️  API keys not configured yet" -ForegroundColor Yellow
        Write-Host "   📝 Edit .env file and add your Binance Testnet API keys`n" -ForegroundColor Yellow
    } else {
        Write-Host "   ✅ API keys configured`n" -ForegroundColor Green
    }
} else {
    Write-Host "   ❌ .env file not found`n" -ForegroundColor Red
}

Write-Host "============================================================`n" -ForegroundColor Cyan

# Show next steps
Write-Host "🚀 NEXT STEPS:`n" -ForegroundColor Cyan

Write-Host "   1. Get API keys from: https://testnet.binancefuture.com/" -ForegroundColor White
Write-Host "   2. Edit .env file with your API credentials" -ForegroundColor White
Write-Host "   3. Run: python test_installation.py" -ForegroundColor White
Write-Host "   4. Try: python -m src.market_orders BTCUSDT BUY 0.001`n" -ForegroundColor White

Write-Host "============================================================`n" -ForegroundColor Cyan

# Demonstrate help for one command
Write-Host "📖 DEMO: Showing MARKET ORDERS help...`n" -ForegroundColor Yellow
Write-Host "============================================================`n" -ForegroundColor Cyan

python -m src.market_orders 2>&1

Write-Host "`n============================================================`n" -ForegroundColor Cyan

Write-Host "💡 TIP: Run any command without parameters to see its help message`n" -ForegroundColor Yellow

Write-Host "📚 DOCUMENTATION:`n" -ForegroundColor Cyan
Write-Host "   - DEMO.md           - How to use the application" -ForegroundColor White
Write-Host "   - README.md         - Complete documentation" -ForegroundColor White
Write-Host "   - QUICK_REFERENCE.md - Command cheat sheet" -ForegroundColor White
Write-Host "   - INDEX.md          - Documentation index`n" -ForegroundColor White

Write-Host "============================================================`n" -ForegroundColor Cyan
Write-Host "✅ Application is ready! Configure your API keys to start trading." -ForegroundColor Green
Write-Host "============================================================`n" -ForegroundColor Cyan
