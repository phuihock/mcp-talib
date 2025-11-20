import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from mcp_talib.indicators import registry
from mcp_talib.models.market_data import MarketData
import json

async def run_all_indicators():
    test_data = [10.0, 12.0, 11.0, 13.0, 14.0, 15.0, 14.0, 16.0, 15.0, 17.0, 
                 18.0, 17.0, 19.0, 20.0, 19.0, 21.0, 22.0, 23.0, 24.0, 25.0, 
                 24.0, 26.0, 27.0]
    
    market_data = MarketData(close=test_data)
    
    print("Testing indicators directly...")
    
    # Test SMA
    sma_indicator = registry.get_indicator("sma")
    if sma_indicator:
        result = await sma_indicator.calculate(market_data, {"timeperiod": 10})
        print(f"SMA: {result.success}")
        if result.success:
            print(f"  First 5 values: {result.values['sma'][:5]}")
        else:
            print(f"  Error: {result.error_message}")
    
    # Test EMA
    ema_indicator = registry.get_indicator("ema")
    if ema_indicator:
        result = await ema_indicator.calculate(market_data, {"timeperiod": 10})
        print(f"EMA: {result.success}")
        if result.success:
            print(f"  First 5 values: {result.values['ema'][:5]}")
        else:
            print(f"  Error: {result.error_message}")
    
    # Test RSI
    rsi_indicator = registry.get_indicator("rsi")
    if rsi_indicator:
        result = await rsi_indicator.calculate(market_data, {"timeperiod": 14})
        print(f"RSI: {result.success}")
        if result.success:
            print(f"  First 5 values: {result.values['rsi'][:5]}")
        else:
            print(f"  Error: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(run_all_indicators())
