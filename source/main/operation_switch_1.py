from imbalance_overtaken_signal import imb_overtake_trading_signal
import time
ticker_list=["HK33HKD","GBPJPY","EURUSD","USDJPY","AUDUSD","XAUUSD"]
m="1"

def run_script(m,ticker_list):  
    
    for t in ticker_list: 
        imb_overtake_trading_signal(t,"OANDA","1")
    
    
for _ in range(5):
    run_script(m,ticker_list)
    time.sleep(60)
