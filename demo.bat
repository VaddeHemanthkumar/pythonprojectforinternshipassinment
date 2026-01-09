@echo off
REM Binance Futures Trading Bot - Interactive Demo
REM This script demonstrates all features of the trading bot

echo.
echo ============================================================
echo    BINANCE FUTURES TRADING BOT - INTERACTIVE DEMO
echo ============================================================
echo.
echo This trading bot supports 6 types of orders:
echo.
echo   1. Market Orders       - Immediate execution
echo   2. Limit Orders        - Execute at specific price
echo   3. Stop-Limit Orders   - Triggered orders
echo   4. OCO Orders          - Take-profit + Stop-loss
echo   5. TWAP Strategy       - Split large orders over time
echo   6. Grid Trading        - Automated range trading
echo.
echo ============================================================
echo.

:menu
echo.
echo What would you like to do?
echo.
echo   1 - Show Market Orders help
echo   2 - Show Limit Orders help
echo   3 - Show Stop-Limit Orders help
echo   4 - Show OCO Orders help
echo   5 - Show TWAP Strategy help
echo   6 - Show Grid Trading help
echo   7 - Run Market Order example (needs API keys)
echo   8 - Run Limit Order example (needs API keys)
echo   9 - View bot.log
echo   0 - Exit
echo.
set /p choice="Enter your choice (0-9): "

if "%choice%"=="1" goto market_help
if "%choice%"=="2" goto limit_help
if "%choice%"=="3" goto stoplimit_help
if "%choice%"=="4" goto oco_help
if "%choice%"=="5" goto twap_help
if "%choice%"=="6" goto grid_help
if "%choice%"=="7" goto market_example
if "%choice%"=="8" goto limit_example
if "%choice%"=="9" goto view_log
if "%choice%"=="0" goto end
goto menu

:market_help
echo.
echo ============================================================
echo MARKET ORDERS - Help
echo ============================================================
python -m src.market_orders
echo.
pause
goto menu

:limit_help
echo.
echo ============================================================
echo LIMIT ORDERS - Help
echo ============================================================
python -m src.limit_orders
echo.
pause
goto menu

:stoplimit_help
echo.
echo ============================================================
echo STOP-LIMIT ORDERS - Help
echo ============================================================
python -m src.advanced.stop_limit
echo.
pause
goto menu

:oco_help
echo.
echo ============================================================
echo OCO ORDERS - Help
echo ============================================================
python -m src.advanced.oco
echo.
pause
goto menu

:twap_help
echo.
echo ============================================================
echo TWAP STRATEGY - Help
echo ============================================================
python -m src.advanced.twap
echo.
pause
goto menu

:grid_help
echo.
echo ============================================================
echo GRID TRADING - Help
echo ============================================================
python -m src.advanced.grid
echo.
pause
goto menu

:market_example
echo.
echo ============================================================
echo MARKET ORDER EXAMPLE
echo ============================================================
echo.
echo This will place a BUY order for 0.001 BTCUSDT at market price
echo Make sure you have configured your API keys in .env file!
echo.
set /p confirm="Continue? (y/n): "
if /i "%confirm%"=="y" (
    python -m src.market_orders BTCUSDT BUY 0.001
) else (
    echo Order cancelled.
)
echo.
pause
goto menu

:limit_example
echo.
echo ============================================================
echo LIMIT ORDER EXAMPLE
echo ============================================================
echo.
echo This will place a BUY order for 0.001 BTCUSDT at $40,000
echo Make sure you have configured your API keys in .env file!
echo.
set /p confirm="Continue? (y/n): "
if /i "%confirm%"=="y" (
    python -m src.limit_orders BTCUSDT BUY 0.001 40000
) else (
    echo Order cancelled.
)
echo.
pause
goto menu

:view_log
echo.
echo ============================================================
echo BOT LOG (Last 30 lines)
echo ============================================================
echo.
if exist bot.log (
    powershell -Command "Get-Content bot.log -Tail 30"
) else (
    echo No log file found. Run an order first to generate logs.
)
echo.
pause
goto menu

:end
echo.
echo ============================================================
echo Thank you for using Binance Futures Trading Bot!
echo ============================================================
echo.
echo For more information:
echo   - Read DEMO.md for usage guide
echo   - Read README.md for full documentation
echo   - Read QUICK_REFERENCE.md for command reference
echo.
pause
exit
